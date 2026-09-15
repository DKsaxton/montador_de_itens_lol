-- =====================================================================
-- Montador de Itens de LoL — servidor das builds publicadas (Fase 8)
-- Cole este arquivo inteiro no SQL Editor do Supabase e clique em Run.
-- Pode rodar de novo sem medo: tudo é "if not exists" / "or replace".
-- =====================================================================

create extension if not exists pgcrypto with schema extensions;   -- digest() e gen_random_bytes() vivem em "extensions" no Supabase

-- ---------------------------------------------------------------------
-- Tabela das builds publicadas. O segredo de quem publicou fica só como
-- hash: quem tem o segredo (guardado no navegador do autor) pode atualizar
-- e apagar; todo o resto só lê.
-- ---------------------------------------------------------------------
create table if not exists public.builds (
  id             text primary key,                       -- id curto (6 caracteres), gerado aqui
  nome           text not null,
  descricao      text not null,
  campeao        jsonb,                                   -- {"key":"222","id":"Jinx","name":"Jinx"} ou null (todos)
  modo           text not null default '',
  marcadores     jsonb not null default '[]'::jsonb,      -- os 3 marcadores
  caixas         jsonb not null,                          -- categorias com itens (formato do Montador)
  patch          text not null,                           -- versão do catálogo na publicação (≠ atual → "desatualizada")
  versao         integer not null default 1,              -- soma 1 a cada publicação da mesma build
  autor          text not null default '',
  segredo_hash   text not null,
  criado_em      timestamptz not null default now(),
  atualizado_em  timestamptz not null default now(),
  visualizacoes  integer not null default 0,
  copias         integer not null default 0
);
-- Fase 9: layout de leitura da build (tabuleiro | nucleo | trilha | grade). Pode rodar de novo.
alter table public.builds add column if not exists layout text not null default 'tabuleiro';

-- Eventos de visualização e cópia, para o "popular hoje / da semana".
create table if not exists public.eventos (
  id        bigserial primary key,
  build_id  text not null references public.builds(id) on delete cascade,
  tipo      text not null check (tipo in ('visualizacao', 'copia')),
  quando    timestamptz not null default now()
);
create index if not exists eventos_build_quando on public.eventos (build_id, quando desc);

-- Ninguém mexe nas tabelas direto: só pelas funções abaixo e pela view.
alter table public.builds  enable row level security;
alter table public.eventos enable row level security;
revoke all on public.builds  from anon, authenticated;
revoke all on public.eventos from anon, authenticated;

-- ---------------------------------------------------------------------
-- View pública: tudo menos o hash, com popularidade do dia e da semana.
-- Roda com a permissão de quem lê (security_invoker), como o verificador do
-- Supabase pede; por isso o público ganha SELECT só nas colunas públicas da
-- tabela (o hash do segredo fica de fora) e nos eventos.
-- ---------------------------------------------------------------------
drop policy if exists "leitura publica das builds" on public.builds;
create policy "leitura publica das builds" on public.builds for select to anon, authenticated using (true);
drop policy if exists "leitura publica dos eventos" on public.eventos;
create policy "leitura publica dos eventos" on public.eventos for select to anon, authenticated using (true);
grant select (id, nome, descricao, campeao, modo, marcadores, caixas, patch, versao, autor, criado_em, atualizado_em, visualizacoes, copias, layout)
  on public.builds to anon, authenticated;
grant select on public.eventos to anon, authenticated;

drop view if exists public.builds_publicas;
create view public.builds_publicas with (security_invoker = true) as
select
  b.id, b.nome, b.descricao, b.campeao, b.modo, b.marcadores, b.caixas, b.patch, b.versao, b.autor,
  b.criado_em, b.atualizado_em, b.visualizacoes, b.copias, b.layout,
  coalesce((select count(*) from public.eventos e where e.build_id = b.id and e.quando > now() - interval '1 day'), 0)::int  as pop_dia,
  coalesce((select count(*) from public.eventos e where e.build_id = b.id and e.quando > now() - interval '7 days'), 0)::int as pop_semana
from public.builds b;

grant select on public.builds_publicas to anon, authenticated;

-- ---------------------------------------------------------------------
-- Publicar (nova) ou atualizar (com o segredo). Regras do Leo: itens,
-- nome, descrição e 3 marcadores; senão, erro.
-- ---------------------------------------------------------------------
drop function if exists public.publicar_build(text, text, jsonb, text, jsonb, jsonb, text, text, text, text);
create or replace function public.publicar_build(
  p_nome text, p_descricao text, p_campeao jsonb, p_modo text, p_marcadores jsonb, p_caixas jsonb,
  p_patch text, p_autor text, p_segredo text, p_id text default null, p_layout text default 'tabuleiro'
) returns jsonb
language plpgsql security definer set search_path = public, extensions as $$
declare
  v_id text; v_hash text; v_versao int; v_itens int;
begin
  if coalesce(trim(p_nome), '') = '' then raise exception 'A build precisa de nome.'; end if;
  if coalesce(trim(p_descricao), '') = '' then raise exception 'A build precisa de descrição.'; end if;
  if jsonb_typeof(p_marcadores) <> 'array' or jsonb_array_length(p_marcadores) < 3 then raise exception 'A build precisa dos 3 marcadores.'; end if;
  if jsonb_typeof(p_caixas) <> 'array' then raise exception 'Caixas inválidas.'; end if;
  select coalesce(sum(jsonb_array_length(c->'items')), 0) into v_itens from jsonb_array_elements(p_caixas) c;
  if v_itens = 0 then raise exception 'A build precisa de itens.'; end if;
  if coalesce(p_segredo, '') = '' then raise exception 'Segredo ausente.'; end if;
  v_hash := encode(digest(p_segredo, 'sha256'), 'hex');

  if p_id is null then
    loop
      v_id := lower(substr(encode(gen_random_bytes(6), 'hex'), 1, 6));
      exit when not exists (select 1 from public.builds where id = v_id);
    end loop;
    insert into public.builds (id, nome, descricao, campeao, modo, marcadores, caixas, patch, autor, segredo_hash, layout)
    values (v_id, trim(p_nome), trim(p_descricao), p_campeao, coalesce(p_modo, ''), p_marcadores, p_caixas, p_patch, coalesce(p_autor, ''), v_hash, coalesce(p_layout, 'tabuleiro'));
    v_versao := 1;
  else
    update public.builds
       set nome = trim(p_nome), descricao = trim(p_descricao), campeao = p_campeao, modo = coalesce(p_modo, ''),
           marcadores = p_marcadores, caixas = p_caixas, patch = p_patch, autor = coalesce(p_autor, ''),
           layout = coalesce(p_layout, 'tabuleiro'), versao = versao + 1, atualizado_em = now()
     where id = p_id and segredo_hash = v_hash
     returning id, versao into v_id, v_versao;
    if v_id is null then raise exception 'Build não encontrada ou o segredo não confere.'; end if;
  end if;
  return jsonb_build_object('id', v_id, 'versao', v_versao);
end $$;

create or replace function public.apagar_build(p_id text, p_segredo text) returns boolean
language plpgsql security definer set search_path = public, extensions as $$
declare v_n int;
begin
  delete from public.builds where id = p_id and segredo_hash = encode(digest(p_segredo, 'sha256'), 'hex');
  get diagnostics v_n = row_count;
  return v_n > 0;
end $$;

-- Visualização e cópia: registra o evento e soma no contador.
create or replace function public.registrar_evento(p_id text, p_tipo text) returns void
language plpgsql security definer set search_path = public, extensions as $$
begin
  if p_tipo not in ('visualizacao', 'copia') then raise exception 'Tipo inválido.'; end if;
  insert into public.eventos (build_id, tipo) values (p_id, p_tipo);
  if p_tipo = 'visualizacao' then update public.builds set visualizacoes = visualizacoes + 1 where id = p_id;
  else update public.builds set copias = copias + 1 where id = p_id; end if;
end $$;

grant execute on function public.publicar_build(text, text, jsonb, text, jsonb, jsonb, text, text, text, text, text) to anon, authenticated;
grant execute on function public.apagar_build(text, text) to anon, authenticated;
grant execute on function public.registrar_evento(text, text) to anon, authenticated;
