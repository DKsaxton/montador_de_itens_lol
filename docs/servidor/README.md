# Servidor das builds publicadas (Supabase) — passo a passo

O Montador é uma página estática. Para publicar e buscar builds ele usa um projeto gratuito no Supabase
(banco Postgres com API pronta). A página só precisa de duas coisas públicas: a URL do projeto e a chave
"anon". Tudo o que protege as builds (quem pode atualizar/apagar) fica dentro do banco, no `supabase.sql`.

## 1. Criar o projeto
1. Em https://supabase.com/dashboard, clique em **New project**.
2. Organização: a sua. **Name**: `montador-de-itens`. **Database password**: gere uma e guarde (a página não usa).
   **Region**: `South America (São Paulo)`. Plano **Free**. Clique em **Create new project** e espere ~2 minutos.

## 2. Criar as tabelas e funções
1. No menu da esquerda, **SQL Editor** → **New query**.
2. Abra `docs/servidor/supabase.sql`, copie o arquivo inteiro, cole no editor e clique em **Run**.
   Deve terminar com "Success. No rows returned". Pode rodar de novo sem problema.

## 3. Pegar a URL e a chave pública
1. Menu da esquerda, **Project Settings** (engrenagem) → **API** (ou **Data API**).
2. Copie **Project URL** (algo como `https://abcdefghijklmnop.supabase.co`).
3. Em **API Keys**, copie a chave **publishable** (`sb_publishable_...`; nos projetos antigos chama-se anon/public e começa com `eyJ`).
   Nunca a **secret** (`sb_secret_...`) nem a `service_role`: essas são secretas e não vão para a página. Se uma delas vazar, revogue-a ali mesmo.

## 4. Colocar na página
Abra `data/servidor.js` e preencha:

```js
window.SERVIDOR = {
  url: "https://SEU-PROJETO.supabase.co",
  anonKey: "eyJ...",
};
```

Salve e recarregue o Montador. A aba **Públicas** liga sozinha quando os dois campos estão preenchidos.
Sem eles (ou sem internet) a página continua funcionando com as builds locais.

## Aviso do verificador de segurança
O Supabase tem um verificador (Security Advisor). O SQL já segue o que ele pede: a view lê com a permissão de quem consulta (`security_invoker`), e o público só enxerga as colunas públicas — o hash do segredo nunca sai.

## O que o SQL cria
- `builds`: as builds publicadas (nome, descrição, campeão, modo, 3 marcadores, caixas, patch do catálogo,
  versão, autor, data de criação/atualização, contadores) e o **hash** do segredo de quem publicou.
- `eventos`: cada visualização ou cópia com data, para o "Popular hoje / da semana".
- `builds_publicas`: a view que a página lê (tudo menos o hash, com `pop_dia` e `pop_semana`).
- Funções: `publicar_build` (nova ou atualização com o segredo; valida nome, descrição, itens e 3 marcadores;
  gera o ID curto; soma a versão), `apagar_build` (com o segredo), `registrar_evento` (visualização / cópia).
- Ninguém escreve nas tabelas direto: RLS ligado, e a chave pública só enxerga a view e as funções.

## Manutenção (futuro)
- A única coisa que cresce é a tabela `eventos` (uma linha por visualização ou cópia). Os totais de cada build
  ficam em `builds`, então os eventos antigos podem ir embora sem perder nada.
- `docs/servidor/limpeza.sql` tem as duas formas: **à mão** (uma linha que apaga eventos com mais de 30 dias) e
  **automática** (um bloco que agenda a limpeza diária com o pg_cron do próprio Supabase; roda uma vez e esquece).
- Para ver o tamanho: painel do Supabase → Table Editor → `eventos` mostra a contagem; ou a consulta comentada no
  final do `limpeza.sql`. No plano Free o banco tem 500 MB; cada evento ocupa menos de 100 bytes.
- Apagar uma build publicada: pelo botão Excluir do Montador no navegador que a publicou (usa o segredo). Se o
  segredo se perdeu (outro navegador, cache limpo), apague no painel: Table Editor → `builds` → linha → Delete.

