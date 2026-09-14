# Direção de Arte — Montador de Itens

> Aprovada pelo Leo em 13/09/2026 (Fase 1, Opção A — "Taverna e pergaminho"). Amostra de referência: `docs/amostras/fase1-amostra.html` (coluna A) e `docs/screenshots/fase1-tarefa2-amostra.png`. Este documento só cresce: nada aqui volta atrás sem novo aprovado.

## Briefing (do Leo, 13/09/2026)
- Catálogo = **loja medieval**: papel envelhecido (texturas em assets/textures), madeira, latão, um lojista que fala.
- Build = **forja**: ferro escuro, brasa, faísca, martelo.
- Do HTML anterior, **manter**: o efeito de hover dos ícones (aprovado como "maravilhoso"), a estrutura Catálogo / Build / Calculadora, a biblioteca de builds.
- Do HTML anterior, **abandonar**: a paleta e a aparência dos cards com ícones ("genérico, sem personalidade"); falta de animações.
- Animações de clique diferentes por tier; som por núcleo (AD / AP / Vitalidade) e por tier — ver docs/mapa_de_audio.md.
- Classe como 4 abas (TODOS · AD · AP · VITALIDADE), modelo Deadlock, com cor própria.

## Paleta (Opção A)
| Papel | Uso | Código |
|---|---|---|
| Papel | fundo de card, busca, barra de filtros, placa de entrada, pergaminho da Calculadora | `#e5d3ad` |
| Papel escuro | sombra/borda de papel, fundos secundários | `#cdb689` |
| Borda de papel | contorno dos cards | `#a88f60` |
| Tinta ferrogálica | texto principal sobre papel | `#2c1d12` |
| Tinta suave | texto secundário, nome em inglês, contornos de chip | `#5a4630` |
| Madeira | fundo do Catálogo (tábuas), painéis | `#3b2617` → `#2a1a0f` → `#21130a` (gradiente vertical, veios `rgba(0,0,0,.09)` a cada 11px) |
| Madeira escura | fundo geral da tela | `#1c120b` com linhas finas `#241810` |
| Latão | selo de Lendário, detalhes, títulos sobre madeira | `#b6873a` (claro `#d5b35a`, escuro `#8a5f18`) |
| Cera | preço, chip ativo, botão "Entrar na loja", carimbo "NO BUILD" | `#8d2c22` (borda `#5c150d`, sombra `#4a1109`) |
| Texto sobre madeira | títulos e legendas fora do papel | `#e8d3a2` (títulos), `#b89a66` (legendas), `#d9c08a` (rótulos de seção) |

Classe (`itemClass.core`), iguais no Catálogo e na forja:
| Classe | Cor |
|---|---|
| AD | `#c8641e` (laranja) |
| AP | `#7b4fb5` (roxo místico) |
| Vitalidade | `#4d8b3a` (verde) |
| AD e AP (só Filhote de Garrabrasa) | aparece nas abas AD e AP; faixa dividida laranja/roxo |

Forja (Build):
| Papel | Código |
|---|---|
| Ferro (fundo) | `#1a1614` → `#100d0b`, borda `#3a2f28` |
| Molde vazio | radial `#2b2521` → `#15110f`, rebites `#5a4d42` |
| Brasa | `#ff7a1e` (claro `#ffd27a`, glow `rgba(255,120,30,.55)`) |
| Placa de atributos | `#2a2420` → `#1a1512`, borda `#443a32`, números `#ffb257` |
| Interruptor ligado | trilho `#5a2a10`, botão radial `#ffd08a` → `#ff7a1e` |
| Título da forja | `#e9b36a`, Cinzel maiúsculo espaçado |
| Caixas da build (Fase 3, T5) | Comum ferro claro `#9a8875`; Prioridade latão `#c9973f` (não brasa: cansa os olhos em área grande, decisão do Leo); Opcional aço `#7f8a96`. Brasa `#ff7a1e` só em ações e realces pequenos. |

## Tipografia
- **Títulos** (nome do app, "Catálogo", nome do item no card, botão de entrada): `'IM Fell English SC', 'IM Fell English', Georgia, serif`, peso 400. Tamanhos: app 40px, seção 30px, card 18px.
- **Texto** (atributos, chips, legendas, busca): `'Alegreya', Georgia, serif`. 13–15px; itálico para nome em inglês e legendas.
- **Rótulos gravados** (selos, carimbos, títulos da forja, rótulos de seção): `'Cinzel', serif`, 9–14px, maiúsculas, espaçamento .15–.28em.
- Google Fonts com fallback serif; o app deve continuar legível sem internet (Georgia).

## Texturas e materiais
As três texturas são papel amassado quase branco; nunca usadas cruas. Aplicação: elemento com `background: var(--paper)` e um pseudo-elemento por cima com `background-image` da textura, `background-size: 420px`, `mix-blend-mode: multiply`, `opacity .9`.
- As três texturas são **sorteadas** entre as superfícies de papel (decisão do Leo, 13/09/2026), não fixas por função: card = sorteio estável pelo slug do item (o mesmo item tem sempre o mesmo papel); modal = novo sorteio a cada abertura; busca, painel de filtros e abas de Classe = sorteio ao carregar. No CSS, toda superfície de papel lê `--tex-pick`, gravada pelo JS (`paperFor`/`randomPaper`).
- Madeira e latão são gradientes CSS (sem imagem). Sombras fortes e quentes: `rgba(0,0,0,.55–.7)`.

## Componentes
**Card de item (Catálogo)**: papel (textura 01), borda `#a88f60`, sombra 0 4px 10px; grade 56px (ícone) + texto; faixa vertical de 6px na cor da classe à esquerda; nome em IM Fell English SC 18px, nome em inglês + classe em itálico suave; preço em cera à direita; atributos em lista com travessão "—"; ícone em moldura 2px `#5a4630` sobre `#1b120a`. Tier em **selo** no canto inferior direito: Lendário = cera dourada radial (`#d5b35a` → `#8a5f18`) com letra L; Básico = círculo vazio de tinta suave com B. (Os demais tiers definem seu selo na Fase 2, na mesma lógica: cera colorida para os raros, tinta para os comuns.) Estados: **hover** = o efeito aprovado do HTML anterior (inclinação 3D + brilho), com o brilho na cor de latão claro `rgba(232,200,120,.45)` e contorno `#d8b96a`; **já no Build** = opacidade .45, leve dessaturação, carimbo inclinado "NO BUILD" em cera. O card **não** traz a marca "Mestre Forjador" (decisão do Leo, 13/09/2026): elegibilidade fica no filtro lateral e no modal. Selos por tier (implementado na Fase 2, T2): Lendário e Lendário (Evolução) latão `#b6873a`; Épico e Épico (Evolução) azul `#3f5a8a`; Evolução vinho `#7a2f5a`; Bota `#7a4a2a`; Trinket `#a56a2c`; Consumível `#3d6b4a`; Distribuído `#6f6a66`; Starter e Básico tinta `#5a4630`. Nome limitado a duas linhas; preço nunca desce de linha.

**Chip de filtro**: etiqueta arredondada (999px) com contorno 1.5px de tinta sobre papel; ativo = fundo de cera, texto `#f4e6c4`.

**Abas de Classe**: TODOS em tinta; AD/AP/VITALIDADE com a cor da classe (definir forma na Fase 2, tarefa 3, seguindo a anatomia dos chips).

**Cabeçalho do Catálogo**: painel de madeira (tábuas), título em IM Fell English SC `#e8d3a2` com sombra 0 2px `#1a0d05`, busca em papel (textura 02) com sombra interna.

**Placa de entrada** (implementada na Fase 2, T10; textura sorteada como as demais): papel com borda dupla 3px de tinta suave, correntes (barras listradas `#7a6a4a`/`#3a2e1c`) presas ao topo, título 40px, frase em itálico, botão "Entrar na loja" em cera com relevo (sombra 0 3px `#4a1109`).

**Slot da forja (Build)**: quadrado com raio 6px, fundo radial de ferro, sombra interna funda, rebites nos cantos; preenchido = contorno `#6a3a18` + glow de brasa, ícone a 68% com borda `#7a4a20`, 3 faíscas (`#ffd27a`, sombra `#ff9b2f`); vazio = texto itálico "molde N" em `#5f5248`.

**Placa de atributos da caixa**: ferro escuro com linhas tracejadas `#3a3029`, título Cinzel `#b89a72`, valores `#ffb257`.

**Interruptores (Reembolso, Ápice, Mestre Forjador, Editar)** (Fase 3): trilho 36×19px na barra da build; desligado ferro, ligado brasa com glow; rótulo em Cinzel.

**Controle de som (Fase 4)**: sino de balcão em latão no cabeçalho (brasa na forja) que silencia/reativa, com régua de volume ao lado; riscado quando mudo, apagado antes de entrar na loja.

**Forja consolidada (Fase 3)**: bancadas de ferro com placa de tipo (ferro/latão/aço), moldes com rebites e brasa (placa MF apagada = elegível, acesa = o único item forjado, escolhido clicando no ícone do molde na edição; placa ÁPICE), tooltip e editor de observação em placa de ferro com borda de brasa, placas "Atributos da caixa" e "Atributos da build" (números em brasa clara, MF em latão, Ápice em brasa), picker em papel de balcão. Animações: molde levanta ao pegar, placa de pedra cai ao soltar (bancada treme, baforada de brasa), brasa apaga e placa afunda ao remover; loja ↔ forja com o fundo escurecendo/clareando e a vista subindo/descendo.

## Animações (a definir nas Fases 2–3, dentro desta paleta)
- Catálogo (implementado na Fase 2, T9): uma animação de clique por tier, 350–750 ms, só CSS sobre o DOM — cera derretendo no selo (Lendário e Lendário (Evolução)), carimbo batendo (Starter, Básico), tinta espirrando do ponto do clique (Épico e Épico (Evolução)), página virando (Consumível), sino de balcão (Trinket), moeda girando no ícone (Distribuído), bota batendo (Bota), brasa acendendo no ícone e na faixa (Evolução). Respeita prefers-reduced-motion.
- Forja: pegar = molde acende; arrastar = faíscas seguem; soltar = martelada (som na Fase 4); remover = brasa apaga.
- Transição loja → forja: o papel escurece e o ferro sobe de baixo (sair da loja, entrar na forja).

## Campeão da build (Fase 7, T2 — 14/09/2026)
- Retrato do campeão (Data Dragon, mesma versão do catálogo) em medalhão redondo de 46 px antes do nome da build, borda de latão #c9973f com brilho fraco; na barra da biblioteca, versão de 26 px dentro do botão "Campeão". O seletor é próprio (não o `<select>` do sistema): painel de ferro com busca e lista em 3 colunas, cada campeão com retrato de 30 px em medalhão de latão; o escolhido leva borda de latão e tinta de brasa; "Todos os campeões" ocupa a primeira linha com o símbolo ∞. Sem campeão, nada aparece no cabeçalho (a build vale para todos).

## Arsenais — lista de builds (Fase 7, T3 — 14/09/2026)
- A aba Build abre numa tabela de ferro (mesma placa da forja): cabeçalho gravado em Cinzel (Nome · Campeão · Modo · Itens), linhas com o nome em IM Fell, o retrato do campeão em medalhão de latão de 36 px (∞ para todos), modo e contagem em Alegreya itálico, e duas ações discretas (⧉ ✕). Hover acende o nome em brasa; a build ativa leva um friso de brasa à esquerda. Referência: a tela "Arsenais" do cliente do LoL.
- Na forja, "‹ Arsenais" volta à lista e o nome da build ganha um seletor ▾ (painel de ferro igual ao de campeão) para trocar de build sem sair.
