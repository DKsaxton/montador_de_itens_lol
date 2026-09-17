# Prompts para o Claude Design

O que o Design devolver entra aqui como **referência de estilo**, não como app: eu extraio paleta, anatomia e CSS e aplico por cima do `index.html`, que é quem tem os 225 itens, os filtros e o hover aprovado. Salve o HTML que ele gerar em `docs/amostras/` e me avise.

Cada prompt abaixo é para colar inteiro, sozinho, numa conversa nova. O **Bloco 0** vai junto com qualquer um deles: é o contrato que o resultado precisa respeitar.

---

## Bloco 0 — cole isto antes de qualquer prompt

```
CONTEXTO
Estou desenhando pedaços de um app de arquivo único (HTML + CSS + JS, sem build, sem
framework, aberto do disco e publicado no GitHub Pages). É um montador de builds de
League of Legends com duas identidades visuais:
- Catálogo = loja medieval: papel envelhecido, madeira, latão, tinta ferrogálica.
- Build = forja: ferro escuro, brasa, faísca, martelo.

PALETA (use exatamente estes valores)
Papel #e5d3ad · Papel escuro #cdb689 · Borda de papel #a88f60
Tinta #2c1d12 · Tinta suave #5a4630
Madeira #3b2617 → #2a1a0f → #21130a · Madeira escura #1c120b
Latão #b6873a (claro #d5b35a, escuro #8a5f18) · Cera #8d2c22 (texto #f4e6c4)
Títulos sobre madeira #e8d3a2 · Legendas #b89a66
Núcleos: AD #c8641e · AP #7b4fb5 · Vitalidade #4d8b3a
Forja: ferro #1a1614 → #100d0b, borda #3a2f28, brasa #ff7a1e (clara #ffd27a)

TIPOGRAFIA (Google Fonts, já em uso)
Títulos: 'IM Fell English SC'
Texto: 'Alegreya'
Gravado (rótulos em caixa alta, letter-spacing alto): 'Cinzel'

REGRAS DURAS — o resultado é rejeitado se quebrar qualquer uma
1. Só CSS e JS puro. Nada de framework, nada de build, nada de dependência externa
   além das fontes do Google. Um arquivo .html que abre sozinho.
2. ANIMAÇÃO: só `transform` e `opacity` podem animar. Nada de animar width, height,
   top, left, box-shadow, filter, border-color, clip-path ou background. O alvo é
   120 FPS; qualquer coisa que force layout ou repaint está fora.
3. Respeite `@media (prefers-reduced-motion: reduce)`: tudo parado.
4. Nenhum efeito pode cobrir, invadir ou dificultar a leitura do nome do item, do
   preço, do ícone ou dos atributos. Ornamento vive na borda ou fora do card.
5. Variação obrigatória: onde eu pedir N variantes, as N precisam ser
   VISUALMENTE DIFERENTES entre si, não a mesma ideia com outra cor.
6. Não invente dado de item (nome, preço, atributo). Use os exemplos que eu der.

ENTREGA
Um único arquivo .html autocontido, com todas as variantes visíveis lado a lado e
um botão por variante para acioná-la sem depender do mouse. Comente o CSS em
português explicando cada bloco.
```

---

## Prompt A — arte do card por região de Runeterra

O pedido mais novo e o mais promissor. O catálogo tem 13 regiões; 163 itens são de Runeterra e ficam como estão.

```
[cole o Bloco 0 antes]

TAREFA
Desenhar o card de item do catálogo com a identidade visual da REGIÃO do item.
O card base é um retângulo de papel #e5d3ad, borda #a88f60, barra colorida de 4px
na esquerda (cor do núcleo), com: ícone 46x46, nome em 'IM Fell English SC',
nome em inglês em itálico menor, preço em cera no canto direito e uma lista de
2 a 3 atributos.

REGIÕES (e quantos itens cada uma tem no catálogo)
Runeterra 163 — NEUTRA, não muda: papel liso, é a referência do "sem tema"
Ionia 10 · Freljord 8 · Noxus 7 · Demacia 7 · Targon 5 · Bilgewater 5
The Void 5 · Shadow Isles 4 · Piltover 4 · Zaun 3 · Shurima 2 · Bandle City 2

O QUE QUERO
Para cada uma das 12 regiões com tema, uma versão do card que diga de onde ele
vem SEM trocar a estrutura nem prejudicar a leitura. Trabalhe com:
- textura/padrão sutil no papel (o papel continua claro e legível)
- moldura ou cantoneira própria
- um ornamento pequeno no canto
- ajuste de tom do papel, não de cor do texto
Exemplos do que espero de cada uma: Ionia = tinta e pétala, linha limpa;
Noxus = ferro rebitado e mancha escura; Demacia = pedra clara e ouro heráldico;
Freljord = gelo riscado e couro; Piltover = latão e engrenagem fina; Zaun = cano,
válvula e mancha química; Shadow Isles = névoa e osso; Targon = pedra e estrela;
Bilgewater = corda, madeira e anzol; Shurima = arenito e hieróglifo; The Void =
fissura e roxo profundo; Bandle City = feltro e madeira pequena.

MOSTRE
Os 13 cards (12 temáticos + o neutro de Runeterra) lado a lado, com o mesmo item
fictício em todos para dar para comparar: nome "Item de Exemplo", inglês
"Example Item", preço "3.000g", atributos "+55 de Dano de Ataque" e "+18 de
Letalidade". Marque em cada card qual é a região.
```

---

## Prompt B — efeitos de passagem do mouse por núcleo

Já tenho uma versão aprovada por mim (`docs/amostras/fase11-vida-por-nucleo.html`). Mande este prompt se quiser que o Design refaça com mais capricho; cole junto a minha amostra como referência do que já ficou bom.

```
[cole o Bloco 0 antes]

TAREFA
Efeitos de passagem do mouse no card do catálogo, um jeito por núcleo. A duração
de cada animação é FIXA porque casa com o som que toca junto — não mude:

AD — 235 ms. Som: um golpe seco, tom Mi. O card tem que parecer que APANHOU.
     5 variantes: corte diagonal, corte cruzado, estocada entrando pela lateral,
     martelada com onda de choque, e um corte que ABRE o card em duas metades que
     se afastam e voltam a se unir dentro dos mesmos 235 ms.
AP — 520 ms, em dois tempos de 260 ms (o som é ré e depois mi). O efeito é uma
     MOLDURA que se desenha em volta do card no primeiro tempo e ganha ornamento
     no segundo. 4 molduras diferentes, de linguagem arcana e steampunk, puxando
     para Piltover, Zaun e Ionia.
VITALIDADE — 549 ms, em três tempos de 183 ms (o som é tumm · tumm · dó). Também
     é MOLDURA, com gravura. 4 diferentes, temas de proteção e teimosia: alvenaria
     translúcida esverdeada, escudo, folhagem, pedra entalhada.

COMPORTAMENTO
A cada passagem do mouse o card sorteia uma variante do seu núcleo e nunca repete
a anterior. Sortear é obrigatório: duas passadas seguidas no mesmo card têm que
mostrar coisas diferentes.

MOSTRE
Três seções (AD, AP, Vitalidade) com 4 cards cada e uma barra de botões por
seção, um botão por variante, para eu ver uma de cada vez.
```

---

## Prompt C — a tela de Runas e a trilha de habilidades

Fase 11. Eu gero os dados; o Design desenha a tela.

```
[cole o Bloco 0 antes]

TAREFA
Duas telas novas para o mesmo app, na identidade da loja medieval:

1. RUNAS. Uma página de escolha de runas de League of Legends: 5 caminhos
   (Precisão, Domínio, Feitiçaria, Determinação, Inspiração), cada um com 1 runa
   principal escolhida entre 3 ou 4, e 3 fileiras de runas menores com 3 opções
   cada. Mais 3 fragmentos de atributo. Desenhe a grade toda, o estado escolhido
   e o não escolhido, e como fica o resumo depois de montada.
   O jogador escolhe 1 caminho principal e 1 secundário.

2. TRILHA DE HABILIDADES. Uma grade simples de 18 níveis onde se marca qual
   habilidade (Q, W, E, R) sobe em cada nível. Nada ambicioso: a grade bem feita
   já basta. Mostre a grade vazia, a grade preenchida e como ela fica pequena
   dentro de um resumo de build.

MOSTRE
As duas telas uma embaixo da outra, com legendas explicando os estados.
```

---

## Prompt D — a página do catálogo com a cara do núcleo

Já aprovamos o conceito (oficina de fundo + estandarte lateral). Use se quiser que o Design refine.

```
[cole o Bloco 0 antes]

TAREFA
A página do catálogo muda de cara conforme a aba de núcleo escolhida. As abas já
são placas de metal, cada uma com material e símbolo próprios — isso fica. Falta
a PÁGINA embaixo delas:
- fundo de "oficina" por núcleo: AD = aço escovado, AP = veludo com pontos
  arcanos, Vitalidade = carvalho e musgo
- um estandarte de pano vertical na lateral esquerda, com o símbolo e o nome do
  núcleo gravados e a ponta recortada embaixo
- marca d'água grande do símbolo no canto do fundo
- cabeçalhos de seção acompanhando a cor do núcleo
Com a aba "Todos" nada disso aparece: a loja volta ao papel e madeira de sempre.

MOSTRE
Três estados (AD, AP, Vitalidade) e o estado "Todos", cada um com uma faixa de
6 cards de item por cima do fundo, para dar para julgar o contraste e a leitura.
```

---

## Como o retorno entra no projeto

1. Salve o `.html` que o Design gerar em `docs/amostras/` com um nome que diga o que é.
2. Me diga qual arquivo chegou.
3. Eu leio, extraio o que interessa (paleta, medidas, keyframes, anatomia), registro em `docs/direcao_de_arte.md` e aplico no `index.html` por cima do que já existe, sem substituir o app pelo mockup.
4. Capturo, mostro, você aprova, eu commito.
