# Prompt para o Claude Design — Fase 1 (direção de arte)

> Cole no Claude Design (claude.ai/design) junto com: as 3 texturas de papel, a captura do HTML atual (Montador de Itens) e o trecho de itens abaixo. Itere com comentários e sliders; quando gostar, Export → HTML autônomo para docs/amostras/ e "Handoff to Claude Code".

---

Quero a direção de arte de um app pessoal chamado **Montador de Itens** (League of Legends). Ele tem duas telas com identidades diferentes e uma terceira neutra:

- **Catálogo = loja medieval.** Papel envelhecido (anexei 3 texturas reais que devem ser usadas), madeira escura, latão, tinta ferrogálica, selos de cera. Há um lojista que fala (áudio) — a interface pode sugerir a presença dele (balcão, placa, letreiro), sem desenhar personagem.
- **Build = forja.** Ferro escuro, brasa, faísca, martelo e bigorna; slots de item como moldes de metal.
- **Calculadora** = pergaminho de contas, neutra, na família da loja.

O que NÃO quero: o visual atual (anexei a captura) — cards escuros genéricos, paleta azul/dourada padrão de "site de jogo", sem personalidade. O que quero MANTER da versão atual: o efeito de hover nos ícones dos itens (o ícone reage ao mouse) — não precisa reproduzir, só não conflitar.

Produza uma **página de amostra**, não o app inteiro, com estes elementos lado a lado:
1. Cabeçalho do Catálogo com o título e a busca.
2. Um **card de item** em três estados: normal, com o mouse em cima, e "já está no Build" (opacidade reduzida). Use estes itens reais (não invente dados):
   - Quebrapassos (Stridebreaker) — Lendário — 3.300g — +40 de Dano de Ataque, +25% de Velocidade de Ataque, +450 de Vida — núcleo AD
   - Bastão das Eras (Rod of Ages) — Lendário — 2.600g — +45 de Poder de Habilidade, +350 de Vida, +500 de Mana — núcleo AP
   - Sinal de Sterak (Sterak's Gage) — Lendário — 3.200g — +400 de Vida, +20% de Tenacidade — núcleo Vitalidade
   - Cristal de Rubi (Ruby Crystal) — Básico — 400g — +150 de Vida — núcleo Vitalidade
   Os três núcleos (AD, AP, Vitalidade) e o tier (Básico, Épico, Lendário…) precisam ser reconhecíveis à primeira vista por cor ou selo.
3. Um chip de filtro em dois estados (inativo, ativo).
4. Um trecho do **Build na forja**: 6 slots de item, dois preenchidos, com o total de atributos ao lado, e um interruptor "Mestre Forjador" e outro "Reembolso".
5. A tela de entrada: uma porta/placa com o botão "Entrar na loja".

Me dê **duas direções** lado a lado (por exemplo, uma mais "taverna e pergaminho", outra mais "guilda e latão"), com sliders para tom do papel, saturação da brasa e tipografia dos títulos. Português do Brasil em todos os textos. Ícones dos itens podem ser quadrados neutros — no app real eles vêm de URL.
