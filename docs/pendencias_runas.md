# Pendências das runas

O que o `data/gerar_runas_json.py` achou em `data/Runas_League_of_Legends.md` e **não corrigiu**. A fonte é sua; eu leio, aponto e sigo — o app mostra o que existe e deixa claro o que não existe.

Rode a qualquer momento para ver a lista atualizada:

```bash
python data/gerar_runas_json.py
```

## O que o arquivo tem

5 trilhas · **62 runas** · 9 fragmentos · 14 substituições automáticas. Cinco keystones por trilha? Não: **3 ou 4 keystones e 3 runas em cada um dos três slots**, que é o desenho do jogo.

| Trilha | Keystone | Slot 1 | Slot 2 | Slot 3 |
|---|---|---|---|---|
| Precisão | 4 | 3 | 3 | 3 |
| Dominação | 3 | 3 | 3 | 3 |
| Feitiçaria | 4 | 3 | 3 | 3 |
| Determinação | 3 | 3 | 3 | 3 |
| Inspiração | 3 | 3 | 3 | 3 |

Comparando com o `runesReforged.json` em pt_BR da Riot: **62 de um lado, 62 do outro, sem diferença em nenhuma direção.**

## 1. Sete runas sem a linha `Atributos:`

Todas têm descrição e `Classes:`, mas não dizem que atributo concedem. No app elas aparecem sem a linha de atributos — eu não deduzo do texto.

- Precisão / Slot 3: **Golpe de Misericórdia**, **Dilacerar**, **Até a Morte**
- Determinação / Slot 1: **Golpe de Escudo**
- Determinação / Slot 2: **Osso Revestido**
- Inspiração / Keystone: **Livro de Feitiços Deslacrado**
- Inspiração / Slot 1: **Flashtração Hextec**

Leo confirmou em 18/09/2026 que a curadoria é manual. Se a ausência for proposital, vale escrever `Atributos: —` para a checagem parar de apontar.

## 2. ~~Uma substituição aponta para runa que não está na lista~~ — era bug meu

O `Pós-choque -> vira Aperto dos Mortos-Vivos` parecia apontar para runa inexistente. O Aperto dos Mortos-Vivos **sempre esteve no arquivo**; quem não o via era o meu leitor. Ver a seção abaixo.

## 3. ~~Um nome escrito diferente do oficial~~ — resolvido em 18/09/2026

O arquivo dizia **Absorvição Vital**; no Data Dragon da Riot está **Absorção Vital**, e por isso ela era a única runa sem ícone. Com a sua autorização eu troquei a palavra no markdown. Hoje as **67 runas e fragmentos têm arte**.

## 4. ~~Quatro runas que a Riot tem e o arquivo não~~ — era bug meu, corrigido em 18/09/2026

Eu relatei que faltavam **Tônico Triplo, Aperto dos Mortos-Vivos, Transcendência e Tempestade Crescente**, e cheguei a dizer que a diferença podia ser curadoria do Leo. Estava errado nas duas coisas.

As quatro sempre estiveram no `Runas_League_of_Legends.md`. O que acontecia é que a descrição delas ocupa **mais de uma linha** — o colchete abre numa linha e fecha três ou quatro abaixo — e o meu leitor exigia abrir e fechar na mesma. Ele descartava a runa em silêncio e, de quebra, grudava as linhas de continuação como "notas técnicas" da runa anterior.

O leitor agora conta colchetes até fecharem. E a comparação com o Data Dragon, que antes era uma nota solta neste arquivo, virou **pendência do gerador**: se a Riot tiver uma runa que o arquivo não tem, isso aparece toda vez que você rodar, em vez de virar uma frase que alguém explica.

A lição, escrita para não repetir: **um leitor que ignora o que não entende mente por omissão.** Todo padrão que pode não casar precisa de uma contagem do lado de fora que confira o resultado.

## Como o app lida com isso enquanto não for resolvido

- Runa sem `Atributos:` aparece sem a linha de atributos, não com "nenhum".
- Runa sem ícone aparece com a inicial dentro da moldura, como o catálogo faz com item sem arte. (Hoje nenhuma está nesse caso.)
- A substituição quebrada aparece na ficha da runa como aviso, com o nome que o arquivo pede.

## Os fragmentos e a tabela que eu não devia ter escrito

Os fragmentos não estão no `runesReforged.json`: a Riot publica a arte deles em `perk-images/StatMods/`, com nome de arquivo em inglês. Eu escrevi a ponte nome → arquivo **à mão**, e troquei duas (Leo achou em 20/09/2026).

O motivo do erro vale guardar: **o nome do arquivo da Riot mente.** O fragmento **Vida** (+65) usa `StatModsHealthScalingIcon.png`, e **Escalamento de Vida** (+10-180 por nível) usa `StatModsHealthPlusIcon.png` — o contrário do que qualquer um leria nos nomes.

A tabela não existe mais. Quem diz qual arquivo é de qual fragmento agora é o `perks.json` do Community Dragon, que carrega os dados do próprio cliente do jogo, casado pelo nome em pt-BR. Cada URL continua sendo pedida de verdade antes de entrar; o que não responder fica sem ícone e vira pendência.

| Fragmento | Arquivo |
|---|---|
| Força Adaptativa | `StatModsAdaptiveForceIcon.png` |
| Velocidade de Ataque | `StatModsAttackSpeedIcon.png` |
| Aceleração de Habilidade | `StatModsCDRScalingIcon.png` |
| Velocidade de Movimento | `StatModsMovementSpeedIcon.png` |
| Vida | `StatModsHealthScalingIcon.png` |
| Escalamento de Vida | `StatModsHealthPlusIcon.png` |
| Tenacidade e Resistência a Lentidão | `StatModsTenacityIcon.png` |
