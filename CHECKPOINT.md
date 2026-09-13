# Checkpoint — Montador de Itens de LoL (Capítulo 2 · Forjador)
Última atualização: 13/09/2026 — FASE 1 CONCLUÍDA (Opção A aprovada); próxima: Fase 2, tarefa 1

## 1. Objetivo geral
Evoluir o Montador de Itens (index.html) para a versão com identidade visual de loja medieval (Catálogo) e forja (Build), dados do Capítulo 1 (225 itens, patch 16.18.1) via data/catalog.js, sistema de áudio com lojista, e publicação no GitHub Pages — em fases aprovadas por captura de tela.

## 2. Concluído
- Montagem do agente (fora do Code): CLAUDE.md, docs/, data/catalog.js já gerado (225 itens), data/gerar_catalog_json.py, index.html da primeira tentativa como base.

### Fase 1 — Direção de arte
- T1 — Briefing lido (docs/direcao_de_arte.md, docs/PROMPT_Claude_Design_Fase1.md); Leo aprovou seguir sem handoff do Claude Design (13/09/2026). Texturas conferidas: as três são papel amassado quase branco, precisam de tingimento por blend.
- Fase 1, T2 — amostra em docs/amostras/fase1-amostra.html (captura `docs/screenshots/fase1-tarefa2-amostra.png`), duas direções lado a lado, lendo Quebrapassos, Bastão das Eras, Sinal de Sterak e Cristal de Rubi do catalog.js e as três texturas reais (tingidas por multiply sobre a cor do papel: 01 = card, 02 = busca/barra de filtros, 03 = placa de entrada). A = Taverna e pergaminho (papel #e5d3ad, tinta #2c1d12, madeira #3b2617, latão #b6873a, cera #8d2c22; títulos IM Fell English SC, texto Alegreya; selo de cera para tier, faixa lateral na cor da classe, chips como etiquetas de tinta/cera). B = Guilda e latão (papel #d9c59c, madeira #1d1713, latão #c9973f, bronze #7a5a1e; títulos Cinzel, texto Crimson Pro; etiqueta de latão para tier, borda superior na cor da classe, chips como placas de latão). Classe nas duas: AD laranja, AP roxo, Vitalidade verde. Forja igual nas duas (ferro #15110f, brasa #ff7a1e, moldes com rebites, faíscas, interruptores de brasa). Leo escolheu a Opção A em 13/09/2026. Commit "F1-T2".
- T3 — docs/direcao_de_arte.md escrito com a Opção A (paleta com códigos, classe, forja, tipografia, uso de cada textura, anatomia dos componentes, família de animações). FASE 1 CONCLUÍDA em 13/09/2026.

### Fase 0 — Fundação de dados
- T1 — Assets conferidos e commit inicial (`docs/screenshots/fase0-tarefa1-baseline.png`): 82 mp3 batendo um a um com docs/mapa_de_audio.md; 3 texturas; captura de baseline do index.html antigo (227 itens embutidos). Commit ed64738, aprovado pelo Leo.
- T2 — catalog.js regerado e integridade conferida (sem captura: tarefa de dados). Python 3.12.10 via winget; gerador rodado com `PYTHONUTF8=1` (o `print` final quebra no console cp1252; arquivo já escrito antes; script intocado). Saída idêntica ao commitado: 225 itens, 7 avisos, 0 linhas não reconhecidas. Checagem própria: 225 itens, sem duplicatas, sem campo obrigatório vazio, preços e somas de receita batendo, todo Lendário com masterwork. Os achados (Shattered Armguard ausente, Atlas → Missão de Suporte, id de Stat Bonus, Atma's Reckoning) são decisões já tomadas no Capítulo 1 — registradas em docs/decisoes_capitulo1.md, não como pendência.
- T3 — index.html migrado para data/catalog.js (captura `docs/screenshots/fase0-tarefa3-catalogo-migrado.png`), aprovado pelo Leo em 13/09/2026, commit "F0-T3". O que mudou: CATALOG embutido (227 itens) e ITEM_ICONS base64 removidos → `<script src="data/catalog.js">`; index.html de 1,9 MB para 130 KB. Adaptador de esquema no topo do último script: chave do item = `slug` (builds salvas com a chave antiga sem apóstrofo são traduzidas ao carregar; item que não existe mais sai da build); `components`/`buildsInto` resolvidos por nameEn em `componentRefs`/`buildsIntoIds` (peça repetida vira ×N, `combineCost` na última peça, referência fora do catálogo não é exibida); tiers, ordem de tier e modos lidos do catálogo (rótulos agora são os do Capítulo 1: "Starter", "Trinket", "Evolução"...); ícone por `iconUrl` do Data Dragon com reserva de abreviação se a imagem falhar; `masterwork.raw`, `cashback.raw` e `cashback.netGold` nos lugares dos campos antigos. Testado no navegador embutido via servidor local (http.server 8765, config em .claude/launch.json, ignorado no git): 225 cards, console limpo, 0 ícones quebrados (225/225 URLs respondem 200), modal do Atma com "Cinto do Gigante ×2", filtro Lendário 114, Mestre Forjador 109, Reembolso 3000g→2775g (11 itens de transformação gratuita têm cashback.raw = "none" sem netGold: tratados como não reembolsáveis, badge 109), Build por clique 3450g, Calculadora com preços do catálogo, migração de build antiga OK. Do disco (file://, Chrome headless): 225 cards.
- T3b — pedido do Leo (13/09/2026): removido o total de ouro "Opcional" do resumo da Build (itens opcionais não contam para isso). "Total geral" continua somando tudo — confirmar com o Leo se deve excluir os opcionais também. Aprovado em 13/09/2026, commit "F0-T3b".
- T4 — Pages testado (`docs/screenshots/fase0-tarefa4-pages.png`): deploy no ar 30 s após o push; index.html, data/catalog.js, textura, áudio e .nojekyll respondem 200 em https://dksaxton.github.io/montador_de_itens_lol/; DOM do site publicado com 225 cards e contador 225 (Chrome headless — o navegador embutido não tem permissão para o domínio github.io). Do disco (file://) também 225. FASE 0 CONCLUÍDA em 13/09/2026.

## 3. Em andamento
Nada. Próxima: Fase 2, tarefa 1.

## 4. Próximos passos
Fase 2 — Catálogo (loja medieval), sempre com docs/direcao_de_arte.md como régua e o hover intocado. Tarefas pequenas, uma captura cada:
1. Esqueleto na paleta A: fundo de madeira, cabeçalho em tábuas, busca e barra de filtros em papel (texturas 02/03), tipografia IM Fell English SC + Alegreya + Cinzel. Cards ainda os antigos.
2. Card redesenhado (papel 01, faixa de classe, selo de tier para os 11 tiers, preço em cera, atributos com travessão) — hover preservado, brilho em latão.
3. Abas de Classe TODOS · AD · AP · VITALIDADE no topo da listagem (Garrabrasa em AD e AP).
4. Filtros novos: tipo de dano, custo (faixas), maior/menor atributo, eficiência de ouro (com "sem análise" no fim) — mais os existentes.
5. Modal do item em pergaminho (textura 03) mostrando também `mechanics` das habilidades, `costAnalysis` (valor em ouro, eficiência), `apex`, e referências de receita fora do catálogo como nome sem link.
6. Shift pressionado: card mostra os dados completos em vez do resumo.
7. Clique no card marca para o Build; itens já no Build ficam a .45 com carimbo "NO BUILD".
8. Caixa Ápice ao lado do Reembolso (mostra `apex`); eficiência recalculada com Reembolso (`goldValueTotal ÷ netGold`).
9. Animação de clique por tier (11 tiers, uma família — ver direção de arte).
10. Tela de entrada "Entrar na loja" (placa com correntes; o áudio entra na Fase 4).
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
