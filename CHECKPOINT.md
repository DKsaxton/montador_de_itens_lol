# Checkpoint — Montador de Itens de LoL (Capítulo 2 · Forjador)
Última atualização: 13/09/2026 — Fase 0, tarefa 1 concluída

## 1. Objetivo geral
Evoluir o Montador de Itens (index.html) para a versão com identidade visual de loja medieval (Catálogo) e forja (Build), dados do Capítulo 1 (225 itens, patch 16.18.1) via data/catalog.js, sistema de áudio com lojista, e publicação no GitHub Pages — em fases aprovadas por captura de tela.

## 2. Concluído
- Montagem do agente (fora do Code): CLAUDE.md, docs/, data/catalog.js já gerado (225 itens), data/gerar_catalog_json.py, index.html da primeira tentativa como base.

### Fase 0 — Fundação de dados
- T1 — Assets conferidos e commit inicial (`docs/screenshots/fase0-tarefa1-baseline.png`): assets/audio tem 82 mp3, todos presentes em docs/mapa_de_audio.md e vice-versa (nenhum sem destino, nenhum vazio, nomes só minúsculos); assets/textures tem as 3 texturas. A captura é o baseline do index.html antigo (227 itens do CATALOG embutido) para comparar na T3. Repositório já existia (origin = DKsaxton/montador_de_itens_lol); a estrutura nova entrou no commit "F0-T1".

## 3. Em andamento
Nada. Próxima: Fase 0, tarefa 2.

## 4. Próximos passos
Fase 0 — Fundação de dados
2. Regerar data/catalog.js e ler data/Relatorio_catalogo.md; reportar ao Leo as 3 pendências de integridade já conhecidas (World Atlas → "Missão de Suporte"; Amplifying Tome e Cloth Armor → Shattered Armguard; Atma's Reckoning ausente do Ingrediente de Giant's Belt e Cloak of Agility) como pendências do Capítulo 1. Depende do Python (ver bloqueios); se não houver Python, usar o catalog.js já gerado e só ler o relatório.
3. Migrar index.html: remover CATALOG embutido (227 itens) e ITEM_ICONS base64; carregar data/catalog.js (225 itens); ícones por iconUrl; adaptar o código aos nomes de campo do novo esquema (docs/esquema_catalog.md). Comportamento idêntico ao anterior. Captura + console limpo.
4. Testar abertura pelo disco e no Pages (após o Leo ativar o Pages). Commit "Fase 0 concluída".
Fase 1 — Direção de arte (amostra em docs/amostras/ → aprovação → docs/direcao_de_arte.md)
Fase 2 — Catálogo · Fase 3 — Build · Fase 4 — Som e lojista · Fase 5 — Calculadora e biblioteca · Fase 6 — Publicação e QA

## 5. Decisões tomadas
- Plataforma: Claude Code na pasta do repositório DKsaxton/montador_de_itens_lol; deploy por GitHub Pages (main, raiz, .nojekyll).
- Dados: data/catalog.js gerado, nunca editado à mão; ícones por URL do Data Dragon pelo ID.
- Escopo: só os 225 itens do Capítulo 1. Sem itens removidos, novos ou campeões.
- Animações de clique por tier; áudio por núcleo (hover/clique), por tier (Lendário no Build) e por item (falas raras).
- localStorage permitido (app roda em navegador real).
- Capturas de tela: geradas com Chrome headless (1440×900) direto do arquivo em disco, salvas em docs/screenshots/fase-tarefa-descricao.png.
- Contagem de áudio: 82 arquivos (CHECKPOINT inicial dizia 80 e ENTREGA dizia 84; o mapa_de_audio.md, com 82, é a referência).

## 6. Bloqueios / dúvidas em aberto
- Python não está instalado nesta máquina (só o alias da Microsoft Store). Necessário para regerar data/catalog.js (T2). Leo: instalar Python 3 (python.org ou Store) ou autorizar seguir com o catalog.js já gerado.
- Semântica de `shopkeeper_tag_open_*` (grupo de filtro ou chip?) — perguntar ao Leo na Fase 4.
- Pages ainda não ativado pelo Leo (Settings → Pages → main / root).
