# Checkpoint — Montador de Itens de LoL (Capítulo 2 · Forjador)
Última atualização: 13/09/2026 — Fase 0, tarefa 2 concluída; iniciando tarefa 3

## 1. Objetivo geral
Evoluir o Montador de Itens (index.html) para a versão com identidade visual de loja medieval (Catálogo) e forja (Build), dados do Capítulo 1 (225 itens, patch 16.18.1) via data/catalog.js, sistema de áudio com lojista, e publicação no GitHub Pages — em fases aprovadas por captura de tela.

## 2. Concluído
- Montagem do agente (fora do Code): CLAUDE.md, docs/, data/catalog.js já gerado (225 itens), data/gerar_catalog_json.py, index.html da primeira tentativa como base.

### Fase 0 — Fundação de dados
- T1 — Assets conferidos e commit inicial (`docs/screenshots/fase0-tarefa1-baseline.png`): 82 mp3 batendo um a um com docs/mapa_de_audio.md; 3 texturas; captura de baseline do index.html antigo (227 itens embutidos). Commit ed64738, aprovado pelo Leo.
- T2 — catalog.js regerado e integridade conferida (sem captura: tarefa de dados). Python 3.12.10 via winget; gerador rodado com `PYTHONUTF8=1` (o `print` final quebra no console cp1252; arquivo já escrito antes; script intocado). Saída idêntica ao commitado: 225 itens, 7 avisos, 0 linhas não reconhecidas. Checagem própria: 225 itens, sem duplicatas, sem campo obrigatório vazio, preços e somas de receita batendo, todo Lendário com masterwork. Os achados (Shattered Armguard ausente, Atlas → Missão de Suporte, id de Stat Bonus, Atma's Reckoning) são decisões já tomadas no Capítulo 1 — registradas em docs/decisoes_capitulo1.md, não como pendência.

## 3. Em andamento
- T3 — migração do index.html para data/catalog.js (iniciando).
## 4. Próximos passos
Fase 0 — Fundação de dados
3. Migrar index.html: remover CATALOG embutido (227 itens) e ITEM_ICONS base64; carregar data/catalog.js (225 itens); ícones por iconUrl; adaptar o código aos nomes de campo do novo esquema (docs/esquema_catalog.md). Comportamento idêntico ao anterior. Captura + console limpo. Respeitar docs/decisoes_capitulo1.md (id de Stat Bonus é texto; Slightly Magical Footwear é componente alternativo; agrupar Giant's Belt ×2 no Atma's Reckoning).
4. Testar abertura pelo disco e no Pages (https://dksaxton.github.io/montador_de_itens_lol/). Commit "Fase 0 concluída".
Fase 1 — Direção de arte (amostra em docs/amostras/ → aprovação → docs/direcao_de_arte.md)
Fase 2 — Catálogo · Fase 3 — Build · Fase 4 — Som e lojista · Fase 5 — Calculadora e biblioteca · Fase 6 — Publicação e QA

## 5. Decisões tomadas
- Plataforma: Claude Code na pasta do repositório DKsaxton/montador_de_itens_lol; deploy por GitHub Pages (main, raiz, .nojekyll). Pages ATIVO desde 13/09/2026 (Deploy from a branch, main, / root): https://dksaxton.github.io/montador_de_itens_lol/
- Dados: data/catalog.js gerado, nunca editado à mão; ícones por URL do Data Dragon pelo ID.
- Escopo: só os 225 itens do Capítulo 1. Sem itens removidos, novos ou campeões.
- Animações de clique por tier; áudio por núcleo (hover/clique), por tier (Lendário no Build) e por item (falas raras).
- localStorage permitido (app roda em navegador real).
- Capturas de tela e testes de clique: pelo navegador embutido do Claude Code (pedido do Leo, 13/09/2026); a captura é salva em docs/screenshots/fase-tarefa-descricao.png. Chrome headless só como reserva.
- Contagem de áudio: 82 arquivos (o mapa_de_audio.md é a referência).
- Python: 3.12.10 instalado em %LOCALAPPDATA%\Programs\Python\Python312 (winget, autorizado pelo Leo em 13/09/2026). Rodar o gerador com `PYTHONUTF8=1` para evitar erro de encoding no console.
- O Catálogo está fechado no Capítulo 1: achados da integridade que já foram decididos lá ficam em docs/decisoes_capitulo1.md e não são reportados de novo. Nunca corrigir Catalogo_Itens_LoL.md nem o gerador.

## 6. Bloqueios / dúvidas em aberto
- Nenhuma pendência de dados: os achados da integridade são decisões fechadas do Capítulo 1 (docs/decisoes_capitulo1.md). Única dúvida de fonte aberta lá: lentidão do Scorchclaw Pup (2s vs 3s), marcada [A CONFIRMAR].
- Semântica de `shopkeeper_tag_open_*` (grupo de filtro ou chip?) — perguntar ao Leo na Fase 4.
