# Entrega — Forjador (Capítulo 2) · Claude Code

## O que é esta pasta
É o conteúdo do repositório `montador_de_itens_lol` pronto para o Claude Code. O "agente" é o `CLAUDE.md` (Perfil + Tarefa + Contexto + Formato aprovados), que o Claude Code lê automaticamente ao abrir a pasta. Os demais arquivos são o projeto em si e os documentos de apoio.

## Passo a passo
1. Copie o conteúdo desta pasta por cima do seu clone local de `montador_de_itens_lol` (o `index.html` daqui é o da primeira tentativa, que serve de base).
2. Copie os 80 arquivos .mp3 para `assets/audio/` e as 3 texturas para `assets/textures/` — nomes exatamente como estão (apague os LEIA-ME.txt depois).
3. No GitHub: Settings → Pages → Source "Deploy from a branch" → main → / (root) → Save.
4. Abra o Claude Code na pasta e mande a primeira mensagem: `Leia o CHECKPOINT e execute a próxima tarefa.`
5. A cada captura que ele mostrar: `aprovado` (ou o ajuste). Ele faz commit, push e atualiza o CHECKPOINT sozinho.

## Opcional: Claude Design na Fase 1
Antes de o Forjador começar a Fase 1, você pode fazer a direção de arte no Claude Design (claude.ai/design; Pro/Max, uso medido à parte) com o prompt pronto em `docs/PROMPT_Claude_Design_Fase1.md`. Exporte o HTML para `docs/amostras/` e use o "Handoff to Claude Code". O CLAUDE.md já instrui o Forjador a tratar isso como referência de estilo, não como substituto do app.

## Modelo
Escolha o modelo mais forte do seu plano para as Fases 1–3 (direção de arte, catálogo, forja — é onde o gosto e a coerência visual pesam); as Fases 0, 5 e 6 são mais mecânicas. Não trocar de modelo no meio de uma fase.

## Arquivos
- `CLAUDE.md` — o agente.
- `CHECKPOINT.md` — estado inicial (Fase 0, tarefa 1).
- `index.html` — base (primeira tentativa).
- `data/Catalogo_Itens_LoL.md` (fonte, Cap. 1) · `data/gerar_catalog_json.py` · `data/catalog.js` e `.json` (gerados) · `data/Relatorio_catalogo.md`.
- `docs/mapa_de_audio.md` — 27 eventos, 84 arquivos mapeados (nenhum sem destino).
- `docs/esquema_catalog.md` · `docs/direcao_de_arte.md` (briefing; a Fase 1 preenche) · `docs/PROTOCOLO_IA.md`.
- `.nojekyll` — para o Pages.
