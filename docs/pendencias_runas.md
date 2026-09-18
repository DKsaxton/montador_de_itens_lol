# Pendências das runas

O que o `data/gerar_runas_json.py` achou em `data/Runas_League_of_Legends.md` e **não corrigiu**. A fonte é sua; eu leio, aponto e sigo — o app mostra o que existe e deixa claro o que não existe.

Rode a qualquer momento para ver a lista atualizada:

```bash
python data/gerar_runas_json.py
```

## O que o arquivo tem

5 trilhas · 58 runas · 9 fragmentos · 14 substituições automáticas.

| Trilha | Keystone | Slot 1 | Slot 2 | Slot 3 |
|---|---|---|---|---|
| Precisão | 4 | 3 | 3 | 3 |
| Dominação | 3 | 3 | 3 | 3 |
| Feitiçaria | 4 | 3 | 2 | 2 |
| Determinação | 2 | 3 | 3 | 3 |
| Inspiração | 3 | 3 | 2 | 3 |

## 1. Sete runas sem a linha `Atributos:`

Todas têm descrição e `Classes:`, mas não dizem que atributo concedem. No app elas vão aparecer sem a linha de atributos — eu não deduzo do texto.

- Precisão / Slot 3: **Golpe de Misericórdia**, **Dilacerar**, **Até a Morte**
- Determinação / Slot 1: **Golpe de Escudo**
- Determinação / Slot 2: **Osso Revestido**
- Inspiração / Keystone: **Livro de Feitiços Deslacrado**
- Inspiração / Slot 1: **Flashtração Hextec**

Reparo que as três de Precisão são amplificadores de dano condicional, e as outras quatro não concedem atributo nenhum de fato — pode ser que a ausência esteja certa. Se for, vale escrever `Atributos: —` para a checagem parar de apontar.

## 2. Uma substituição aponta para runa que não está na lista

```
Pós-choque -> vira Aperto dos Mortos-Vivos em campeões sem efeito de imobilização
```

**Aperto dos Mortos-Vivos** não existe em nenhuma trilha do arquivo. Ele é keystone de Determinação no jogo, e é justamente por isso que Determinação está com **2 keystones em vez de 3**.

## 3. ~~Um nome escrito diferente do oficial~~ — resolvido em 18/09/2026

O arquivo dizia **Absorvição Vital**; no Data Dragon da Riot está **Absorção Vital**, e por isso ela era a única runa sem ícone. Com a sua autorização eu troquei a palavra no markdown. Hoje as **67 runas e fragmentos têm arte**.

## 4. Quatro runas que a Riot tem e o arquivo não

Comparando com o `runesReforged.json` em pt_BR do patch 16.18.1:

**Tônico Triplo · Aperto dos Mortos-Vivos · Transcendência · Tempestade Crescente**

São elas que explicam os slots com 2 runas em vez de 3 (Feitiçaria Slot 2 e 3, Inspiração Slot 2, Determinação Keystone).

Duas ressalvas honestas: o arquivo cita mudanças do patch 26.09 (o Avanço da Tempestade voltando no lugar do Ímpeto Gradual), então ele está adiante do Data Dragon em alguns pontos, e essa comparação não é prova de erro. E o Data Dragon também não é a fonte do projeto — serve só de conferência e de origem dos ícones.

## Como o app lida com isso enquanto não for resolvido

- Runa sem `Atributos:` aparece sem a linha de atributos, não com "nenhum".
- Runa sem ícone aparece com a inicial dentro da moldura, como o catálogo faz com item sem arte. (Hoje nenhuma está nesse caso.)
- A substituição quebrada aparece na ficha da runa como aviso, com o nome que o arquivo pede.

## Os fragmentos e a única tabela escrita à mão

Os fragmentos não estão no `runesReforged.json`: a Riot publica a arte deles em `perk-images/StatMods/`, com nome de arquivo em inglês. A ponte nome → arquivo é a **única coisa digitada à mão no projeto**, e ela mora no `data/gerar_runas_json.py`, não no app. Cada arquivo é pedido de verdade antes de entrar; o que não responder fica sem ícone e vira pendência, em vez de virar imagem quebrada na tela.
