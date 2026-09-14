-- =====================================================================
-- Limpeza dos eventos antigos (visualizações e cópias com mais de 30 dias).
-- Os totais de cada build ficam guardados em builds.visualizacoes/copias;
-- os eventos só servem para o "popular hoje / da semana", então 30 dias basta.
--
-- Opção A — à mão, quando quiser: cole só a linha abaixo no SQL Editor e Run.
-- =====================================================================
delete from public.eventos where quando < now() - interval '30 days';

-- =====================================================================
-- Opção B — automático, uma vez por dia (03:00 UTC). Cole este bloco inteiro
-- e Run uma única vez; depois é só esquecer. Para desligar: select cron.unschedule('limpeza-eventos');
-- =====================================================================
create extension if not exists pg_cron with schema extensions;
select cron.schedule(
  'limpeza-eventos',
  '0 3 * * *',
  $$ delete from public.eventos where quando < now() - interval '30 days' $$
);

-- Conferir o tamanho quando quiser:
-- select count(*) as eventos, pg_size_pretty(pg_total_relation_size('public.eventos')) as tamanho from public.eventos;
