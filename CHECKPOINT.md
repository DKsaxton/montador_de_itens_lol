# Checkpoint — Montador de Itens de LoL (Capítulo 2 · Forjador)
Última atualização: 13/09/2026 — FASE 0 CONCLUÍDA (T1–T4); próxima: Fase 1, tarefa 1

## 1. Objetivo geral
Evoluir o Montador de Itens (index.html) para a versão com identidade visual de loja medieval (Catálogo) e forja (Build), dados do Capítulo 1 (225 itens, patch 16.18.1) via data/catalog.js, sistema de áudio com lojista, e publicação no GitHub Pages — em fases aprovadas por captura de tela.

## 2. Concluído
- Montagem do agente (fora do Code): CLAUDE.md, docs/, data/catalog.js já gerado (225 itens), data/gerar_catalog_json.py, index.html da primeira tentativa como base.

### Fase 0 — Fundação de dados
- T1 — Assets conferidos e commit inicial (`docs/screenshots/fase0-tarefa1-baseline.png`): 82 mp3 batendo um a um com docs/mapa_de_audio.md; 3 texturas; captura de baseline do index.html antigo (227 itens embutidos). Commit ed64738, aprovado pelo Leo.
- T2 — catalog.js regerado e integridade conferida (sem captura: tarefa de dados). Python 3.12.10 via winget; gerador rodado com `PYTHONUTF8=1` (o `print` final quebra no console cp1252; arquivo já escrito antes; script intocado). Saída idêntica ao commitado: 225 itens, 7 avisos, 0 linhas não reconhecidas. Checagem própria: 225 itens, sem duplicatas, sem campo obrigatório vazio, preços e somas de receita batendo, todo Lendário com masterwork. Os achados (Shattered Armguard ausente, Atlas → Missão de Suporte, id de Stat Bonus, Atma's Reckoning) são decisões já tomadas no Capítulo 1 — registradas em docs/decisoes_capitulo1.md, não como pendência.
- T3 — index.html migrado para data/catalog.js (captura `docs/screenshots/fase0-tarefa3-catalogo-migrado.png`), aprovado pelo Leo em 13/09/2026, commit "F0-T3". O que mudou: CATALOG embutido (227 itens) e ITEM_ICONS base64 removidos → `<script src="data/catalog.js">`; index.html de 1,9 MB para 130 KB. Adaptador de esquema no topo do último script: chave do item = `slug` (builds salvas com a chave antiga sem apóstrofo são traduzidas ao carregar; item que não existe mais sai da build); `components`/`buildsInto` resolvidos por nameEn em `componentRefs`/`buildsIntoIds` (peça repetida vira ×N, `combineCost` na última peça, referência fora do catálogo não é exibida); tiers, ordem de tier e modos lidos do catálogo (rótulos agora são os do Capítulo 1: "Starter", "Trinket", "Evolução"...); ícone por `iconUrl` do Data Dragon com reserva de abreviação se a imagem falhar; `masterwork.raw`, `cashback.raw` e `cashback.netGold` nos lugares dos campos antigos. Testado no navegador embutido via servidor local (http.server 8765, config em .claude/launch.json, ignorado no git): 225 cards, console limpo, 0 ícones quebrados (225/225 URLs respondem 200), modal do Atma com "Cinto do Gigante ×2", filtro Lendário 114, Mestre Forjador 109, Reembolso 3000g→2775g (11 itens de transformação gratuita têm cashback.raw = "none" sem netGold: tratados como não reembolsáveis, badge 109), Build por clique 3450g, Calculadora com preços do catálogo, migração de build antiga OK. Do disco (file://, Chrome headless): 225 cards.
- T3b — pedido do Leo (13/09/2026): removido o total de ouro "Opcional" do resumo da Build (itens opcionais não contam para isso). "Total geral" continua somando tudo — confirmar com o Leo se deve excluir os opcionais também. Aprovado em 13/09/2026, commit "F0-T3b".
- T4 — Pages testado (`docs/screenshots/fase0-tarefa4-pages.png`): deploy no ar 30 s após o push; index.html, data/catalog.js, textura, áudio e .nojekyll respondem 200 em https://dksaxton.github.io/montador_de_itens_lol/; DOM do site publicado com 225 cards e contador 225 (Chrome headless — o navegador embutido não tem permissão para o domínio github.io). Do disco (file://) também 225. FASE 0 CONCLUÍDA em 13/09/2026.

## 3. Em andamento
Nada. Próxima: Fase 1, tarefa 1.


## 4. Próximos passos
Fase 1 — Direção de arte (nada de tela real muda antes do aprovado)
1. Ler docs/direcao_de_arte.md (briefing) e docs/PROMPT_Claude_Design_Fase1.md; perguntar ao Leo se ele traz um handoff do Claude Design (export HTML em docs/amostras/) ou se o Forjador propõe direto. Handoff = referência de estilo, nunca substitui o app.
2. Amostra em docs/amostras/fase1-amostra.html com DUAS opções renderizadas lado a lado: paleta (loja: as três texturas de papel de assets/textures, madeira, latão, tinta ferrogálica; forja: ferro escuro, brasa, faísca), tipografia, um card de item redesenhado (dados reais do catalog.js) e um trecho do Build em tema de forja. Incluir as cores de Classe pedidas pelo Leo: AD laranja, AP roxo místico, Vitalidade verde. Captura + aprovado.
3. Registrar o aprovado em docs/direcao_de_arte.md (paleta com códigos, fontes, uso de cada textura, anatomia do card e da caixa da forja). Commit "Fase 1 concluída". O hover dos ícones é intocável.
Fase 2 — Catálogo (loja medieval). Além do CLAUDE.md, pedidos do Leo em 13/09/2026:
  a. Classe como 4 ABAS no topo do Catálogo, modelo Deadlock: TODOS · AD (laranja) · AP (roxo místico) · VITALIDADE (verde), lendo `itemClass.core`; Filhote de Garrabrasa ("AD e AP") aparece em AD e em AP. As três cores entram na direção de arte da Fase 1.
  b. Análise de custo: filtro/ordenação por eficiência de ouro (`costAnalysis.efficiencyBase`, 210 de 225 itens; os 15 sem valor — pets, consumíveis, trinkets, Stat Bonus, elixires — vão para o fim com "sem análise"). Mostrar `costAnalysis.goldValue` e `efficiency` no modal.
  c. Ápice: caixa de marcação ao lado do Reembolso que mostra cada item nos status máximos, exibindo o campo `apex` (texto do catálogo; 102 itens têm ápice diferente do base, 123 são "igual ao base"). Quebrapassos com teto de 5 campeões já está registrado no `apex` do catálogo.
  d. Atributo adicional (Stat Bonus): o modal deve mostrar o campo `mechanics` da habilidade (lista dos fragmentos Prata/Ouro/Prismático com valores e ouro), que hoje não é exibido (só `description`).
Fase 3 — Build (forja). Além do CLAUDE.md:
  e. Eficiência de ouro por categoria da build: soma de `costAnalysis.goldValueTotal` ÷ soma de `priceGold` dos itens da categoria (só aritmética sobre os campos do catálogo; itens sem análise ficam de fora e a caixa avisa).
  f. Atributo adicional na build: escolher qual fragmento o item concede exige lista estruturada de fragmentos (stat, valor, nível). Hoje é texto em `mechanics` → propor ao Capítulo 1 um campo estruturado antes de implementar; o Forjador não digita a lista à mão.
  g. Visão Ápice na build lê o mesmo campo `apex` (texto), como no CLAUDE.md.
  h. Eficiência de ouro recalculada pelos interruptores (Leo, 13/09/2026): com Reembolso = `goldValueTotal ÷ cashback.netGold` (dá para fazer já); com Mestre Forjador e Ápice depende de campos numéricos que o catálogo não tem → docs/propostas_capitulo1.md. Vale no Catálogo (Fase 2) e na eficiência por categoria da Build (Fase 3).
Fase 4 — Som e lojista · Fase 5 — Calculadora e biblioteca · Fase 6 — Publicação e QA

## 5. Decisões tomadas
- Plataforma: Claude Code na pasta do repositório DKsaxton/montador_de_itens_lol; deploy por GitHub Pages (main, raiz, .nojekyll). Pages ATIVO desde 13/09/2026 (Deploy from a branch, main, / root): https://dksaxton.github.io/montador_de_itens_lol/
- Dados: data/catalog.js gerado, nunca editado à mão; ícones por URL do Data Dragon pelo ID.
- Escopo: só os 225 itens do Capítulo 1. Sem itens removidos, novos ou campeões.
- Animações de clique por tier; áudio por núcleo (hover/clique), por tier (Lendário no Build) e por item (falas raras).
- localStorage permitido (app roda em navegador real).
- Capturas de tela e testes de clique: pelo navegador embutido do Claude Code (pedido do Leo, 13/09/2026). O navegador embutido não carrega arquivos relativos via file:// (inlina o HTML como snapshot), então os testes rodam pelo servidor local `montador` (.claude/launch.json, http.server na porta 8765); o PNG em docs/screenshots/fase-tarefa-descricao.png é gerado pelo Chrome headless direto do disco (1440×900), que também prova o caso "abrir com dois cliques".
- Contagem de áudio: 82 arquivos (o mapa_de_audio.md é a referência).
- Python: 3.12.10 instalado em %LOCALAPPDATA%\Programs\Python\Python312 (winget, autorizado pelo Leo em 13/09/2026). Rodar o gerador com `PYTHONUTF8=1` para evitar erro de encoding no console.
- O Catálogo está fechado no Capítulo 1: achados da integridade que já foram decididos lá ficam em docs/decisoes_capitulo1.md e não são reportados de novo. Nunca corrigir Catalogo_Itens_LoL.md nem o gerador.

## 6. Bloqueios / dúvidas em aberto
- Propostas de adição ao Capítulo 1 em docs/propostas_capitulo1.md (valor em ouro do bônus do Mestre Forjador, ápice estruturado, fragmentos do Stat Bonus). Sem elas, o app mostra o texto do catálogo e só recalcula a eficiência com Reembolso.
- Navegador embutido do Claude Code não suporta window.prompt() (usado hoje pela observação por item na Build, duplo clique). Em navegador real funciona; a Fase 3 troca o prompt por edição na própria tela.
- Nenhuma pendência de dados: os achados da integridade são decisões fechadas do Capítulo 1 (docs/decisoes_capitulo1.md). Única dúvida de fonte aberta lá: lentidão do Scorchclaw Pup (2s vs 3s), marcada [A CONFIRMAR].
- Semântica de `shopkeeper_tag_open_*` (grupo de filtro ou chip?) — perguntar ao Leo na Fase 4.
