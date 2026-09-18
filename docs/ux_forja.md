# O que confunde na forja

Levantamento feito antes de mexer em qualquer coisa (Fase 12, T2). Cada ponto tem o que é, por que confunde e onde está a prova no código — nada aqui é palpite sobre gosto, é coisa que dá para verificar abrindo o app.

Ordenado pelo que eu acho que dói mais. A ordem de execução é sua.

## 1. Tudo fica trancado até você achar o interruptor "Editar"

Abrindo uma build, não dá para renomear caixa, criar caixa, arrastar item nem remover nada. O único aviso é uma frase que aparece **no card vazio** (`body:not(.editando) .build-empty::after`) — e ele some no instante em que a build tem uma caixa. Ou seja: quem mais precisa do aviso (quem abriu uma build já montada e quer mexer) é exatamente quem não o vê.

**Proposta:** o aviso sai do card vazio e vira uma faixa junto do interruptor, visível sempre que a edição está desligada. Uma linha: "Modo leitura — ligue Editar para mexer".

## 2. Três verbos escondidos num balão

Duplo clique abre a observação do item, botão direito remove, arrastar move para outra caixa. As três coisas existem só no tooltip que aparece parando o mouse sobre o item (`.tt-hint`). Quem não para o mouse, não descobre; quem descobre, precisa lembrar.

**Proposta:** o item ganha, no hover, dois botões pequenos — observação e remover — e o arrastar continua existindo para quem já sabe. Verbo visível não tira o atalho de ninguém.

## 3. O rótulo da caixa é um botão que dá a volta

`COMUM` → `PRIORIDADE` → `OPCIONAL` → `ESCOLHA 1` → `COMUM`, um clique de cada vez. Parece etiqueta e é controle. E para voltar um passo você dá a volta inteira.

**Proposta:** clique abre um menuzinho com os quatro, com o atual marcado. Continua um clique para abrir, e some a volta olímpica.

## 4. Adicionar item pede um passo invisível antes

Para o clique no catálogo marcar um item, é preciso **antes** selecionar a caixa na forja. Sem caixa selecionada, o clique abre a ficha do item — e parece que não funcionou. A faixa "Forjando em X" (F10-T3) resolve o *depois*: ela só aparece quando você já acertou.

**Proposta:** sem caixa selecionada, o clique no item pergunta em qual caixa colocar, em vez de abrir a ficha. E o seletor "Marcar em" ganha um estado de convite quando está vazio.

## 5. O que você edita não está salvo

Em modo Editar as mudanças ficam em rascunho: `saveBuild()` só marca "não salvo" e quem grava é o botão Salvar (ou Ctrl+S). Existe o aviso ao sair, mas o estado "tem coisa não salva" mora numa palavra pequena ao lado do botão.

**Proposta:** com rascunho sujo, o botão Salvar fica aceso e a barra ganha uma marca clara. Nada de salvar sozinho — a decisão de quando gravar é sua, e mudá-la seria mexer no que já foi aprovado.

## 6. Os marcadores não dizem para que servem

Três espaços com `+`. O que eles fazem — filtrar na lista, aparecer na vitrine, e serem obrigatórios para publicar — não está escrito em lugar nenhum da forja.

**Proposta:** uma linha de ajuda ao lado do rótulo, como a que o popup de publicação já usa.

## 7. A alça de redimensionar não tem pista

A caixa encaixa em ¼, ⅓, ½ e 1/1, mas isso só está no `title` da alça. Sem arrastar, ninguém sabe que existe.

**Proposta:** a alça fica visível (não só no hover) enquanto a edição está ligada.

---

## O que eu não vou mexer sem você mandar

- O interruptor Editar em si: ele foi decisão sua na Fase 3 (dois modos, visualização e edição).
- O rascunho não virar gravação automática.
- O efeito de hover dos ícones, a estrutura de três telas e a biblioteca — intocáveis por regra.
