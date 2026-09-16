# Formato de importação de build

Este arquivo descreve o texto que o Montador de Itens lê em **Builds → Exportar / importar → Importar**. Serve para escrever uma build à mão ou pedir a uma IA que gere uma — cole o texto no campo de importação e a build aparece montada.

Os nomes válidos de item e de marcador estão em [marcadores.md](marcadores.md): 225 itens (português ou inglês), 13 marcadores padrão e as quatro habilidades. Nome que não bate com a lista é ignorado; o resto da build entra normalmente.

## Exemplo completo

```
BUILD: Jinx crítico
MODO: Summoner's Rift
CAMPEÃO: Jinx
MARCADORES: AD | Habilidade Q | Gume do Infinito
DESCRIÇÃO: Crítico puro para a rota inferior. / A Coletora primeiro contra times frágeis.
LAYOUT: Trilha por fases
MESTRE FORJADOR: Gume do Infinito

[PRIORIDADE] Núcleo | 3×1
# comprar sempre nessa ordem
= ~14min · 6.500g
- A Coletora
- Gume do Infinito * segurar até os 20 min
- Dança da Morte

[ESCOLHA 1] 4º item | 1×3
# o de cima é o padrão; os de baixo são trocas para o mesmo espaço
- Espada do Rei Destruído
- Mata-Cráquens
- Sedenta por Sangue

[OPCIONAL] Contra tanque | 2×1
- Arco do Axioma
- Cutelo Negro
```

## Linhas do cabeçalho

Vêm antes da primeira caixa, uma por linha, em qualquer ordem. Só `BUILD:` é obrigatória.

| Linha | O que faz | Valores |
|---|---|---|
| `BUILD:` | nome da build | texto livre |
| `MODO:` | modo de jogo, usado no aviso de item indisponível | `Summoner's Rift`, `ARAM`, `ARAM: Mayhem` |
| `CAMPEÃO:` | campeão em pt-BR, como no cliente | nome do Data Dragon, ex.: `Jinx`, `K'Sante`, `Lee Sin` |
| `MARCADORES:` | até 3, separados por ` \| ` | ver [marcadores.md](marcadores.md) |
| `DESCRIÇÃO:` | texto da build numa linha só | ` / ` separa parágrafos |
| `LAYOUT:` | como a build é exibida | `Tabuleiro` (padrão), `Núcleo + bandeja`, `Trilha por fases`, `Grade categoria × custo` |
| `MESTRE FORJADOR:` | liga o interruptor e escolhe o item forjado | nome de um item da build, ou `sim` |

## Caixas

Uma caixa começa com `[TIPO] Nome | colunas×linhas`. A grade é opcional; sem ela a caixa nasce com 3 colunas.

| Tipo | Efeito |
|---|---|
| `[COMUM]` | caixa normal, conta nos totais |
| `[PRIORIDADE]` | conta nos totais e vira "- PRIORIDADE" no arsenal do cliente |
| `[OPCIONAL]` | fica fora dos totais e do resumo das listas |
| `[ESCOLHA 1]` | pilha de alternativas para o mesmo espaço: só o primeiro item conta |

Dentro da caixa:

| Linha | O que faz |
|---|---|
| `# texto` | descrição da caixa |
| `= texto` | marco ou teto, ex.: `= ~14min · 6.500g` |
| `- Item` | um item; `- Item * observação` grava a nota que aparece ao passar o mouse |

## Regras

- Acentos e maiúsculas não importam nos nomes de item, marcador, modo e layout.
- Item desconhecido é listado no aviso de importação e não entra; a build importa mesmo assim.
- Linha que não é nenhuma das acima é ignorada silenciosamente, então comentários soltos não quebram nada.
- A ordem dos itens dentro da caixa é a ordem de compra que aparece na forja e no arsenal do cliente.
- A build importada entra como rascunho: precisa de **Salvar** para ficar na biblioteca.
- **Runas ficam de fora**: o formato só trata itens do catálogo do Capítulo 1.

## Prompt pronto para uma IA

```
Monte uma build de League of Legends para <campeão> no formato abaixo e responda
só com o bloco de texto, sem comentários.

BUILD: <nome>
MODO: Summoner's Rift
CAMPEÃO: <campeão>
MARCADORES: <até 3 da lista permitida>
DESCRIÇÃO: <uma linha; use " / " para separar parágrafos>

[PRIORIDADE] Núcleo | 3×1
# <quando comprar>
- <item>
- <item>
- <item>

[ESCOLHA 1] 4º item | 1×3
- <item padrão>
- <alternativa>
- <alternativa>

[OPCIONAL] Situacional | 2×1
- <item>
- <item>

Regras: use apenas nomes de itens e marcadores das listas que eu colar a seguir;
não invente item, atributo, preço nem efeito.
```

Cole junto o conteúdo de [marcadores.md](marcadores.md) para a IA ter as listas válidas.
