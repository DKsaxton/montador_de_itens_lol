# Pendências das runas

Arquivo único de tudo o que falta nas runas. Estão aqui:
- os dados da sua fonte, `data/Runas_League_of_Legends.md`;
- o que o app faz errado com eles (o leitor `data/gerar_runas_json.py` e a tela);
- os documentos que ficaram para trás;
- e o histórico do que já foi resolvido.

A fonte é sua: eu leio, aponto e sigo, sem corrigir nada nela. O app mostra o que existe e deixa claro o que não existe.

Última revisão: 23/09/2026 (patch do app: 16.18.1). Nessa data conferi runa por runa contra a Riot e a wiki, com dois céticos em cada divergência (ver "Como foi conferido").

Para ver o que o leitor aponta hoje:

```bash
python data/gerar_runas_json.py
```

## Resumo

| # | Pendência | Quem resolve | Prioridade |
|---|---|---|---|
| F1 | 8 números errados em descrições (o app mostra errado): Osso Revestido 555s, Sexto Sentido 106s, Livro de Feitiços 3s... | Leo (fonte) | **alta** |
| F2 | 2 descrições incompletas (Toque Ígneo, Invocar Aery) | Leo | média |
| F3 | Substituições: Cassiopeia não existe mais; falta o Yorick no Pós-choque; "(exceto Yorick)" se lê ao contrário; mais 4 incompletas | Leo | média |
| F4 | 6 notas técnicas de mecânica que mudou (Conquistador, Ritmo Fatal, Aperto dos Mortos-Vivos...) | Leo | média |
| F5 | 5 notas técnicas com erro de sentido | Leo | baixa |
| F6 | Nomes de campeão, habilidade e item que não são os oficiais em pt-BR (6 runas) | Leo | baixa |
| F7 | Linha `Atributos:`: 7 runas sem ela, 5 com atributo que a runa não mexe, 1 chave crua, 1 critério para decidir | Leo | média |
| F8 | 3 lemas chamados de "oficiais" que não são o texto do cliente (um com erro de grafia na tela) | Leo | baixa |
| F9 | Cabeçalho: nota de Força Adaptativa e definição de "movimento debilitado" | Leo | baixa |
| F10 | Para decidir: notas opcionais (Ritmo Fatal à distância, cura da Fonte da Vida) | Leo | baixa |
| A1 | O leitor joga fora o bloco "Controle de grupo válido" de 5 runas, calado | Forjador | média |
| A2 | Bug nº 35 (novo): o texto perde a primária e a secundária quando a primária está sem runa | Forjador | média |
| A3 | Bug nº 19: "Copiar como texto" do lote não leva runas | Forjador | média |
| A4 | Bug nº 29: build publicada aberta "só para ver" tem as runas editáveis | Forjador | baixa |
| A5 | "(ainda não vale no app)" dá a entender que as outras 13 trocas valem no app, e o app não aplica nenhuma | Forjador | baixa |
| A6 | Documentos desatualizados (o SQL do servidor é o que tem risco) | Forjador | média |

---

## Parte 1: da fonte (`data/Runas_League_of_Legends.md`), quem corrige é o Leo

O número de linha é o do arquivo em 23/09/2026. "Certo" quer dizer o valor da Riot no 16.18.1, que é o patch do app.

### F1. Números errados na descrição (o app mostra o número errado)

| Runa | Linha | No MD | Certo | De onde vem o erro |
|---|---|---|---|---|
| Osso Revestido | 347 | Recarga: **555s** | **55s** | Um 5 a mais. É 55s desde o V12.14. |
| Sexto Sentido | 155 | revela a sentinela por **106s** | **10s** | Um 6 a mais. É 10s desde o lançamento da runa. |
| Livro de Feitiços Deslacrado | 384 | Tempo de Recarga inicial de **3s** | **270s** (4:30) | O texto da Riot tem um marcador sem valor (`@f3@`), que virou "3". O valor vem da wiki (V25.19: "de 240 para 270"). |
| Agilidade nos Pés | 56 | curam em **10 - 130** | **15 - 160** (à distância 9 - 96) | Mudou no V26.16, antes do 16.18. |
| Tônico Triplo | 424 | Elixir da Força: **+5 de DdA ou 9 de PdH** | **+15 de DdA ou +25 de PdH** (25 de Força Adaptativa) | 5/9 nunca foi valor do elixir: é o do fragmento de +9 de Força Adaptativa. Hoje o app mostra 15/25 na ficha do item e 5/9 na ficha da runa. |
| Tônico Triplo | 423 | Elixir da Avareza: concede **40** de ouro | **60** de ouro | Mudou no V25.22. O catálogo de itens já diz 60. |
| Manto de Nimbus | 224 | dura **2.5s** | **2s** | Mudou no V10.21. |
| Ventos Revigorantes | 342 | ao longo de **10.5s** | **10s** | A duração nunca mudou. |

### F2. Descrição incompleta
- **Toque Ígneo** (linha 203): falta a terceira duração oficial, "Dano ao longo do tempo: 1s". Sem ela, quem lê não sabe que o dano contínuo só aplica 1s de queimadura.
- **Invocar Aery** (linha 183): falta a última frase oficial, "Aery não é enviada novamente até que ela retorne a você". É ela que faz as vezes de recarga.

### F3. Substituições automáticas
- **Calçados Mágicos → Reembolso na Cassiopeia não existe mais** (linhas 413 e 528–530). A troca valeu do V14.10 até o 15.24 e saiu no 16.1, quando a Cassiopeia passou a comprar botas. Provas:
  - a passiva dela no Data Dragon 16.18.1 ("Todos os efeitos de Velocidade de Movimento são mais eficazes em Cassiopeia");
  - o arquivo da campeã no cliente do jogo: no 15.24 tem a troca, no 16.1 e no 16.18 não tem.

  O certo é apagar as duas menções. Apagar só o comentário "ainda não está no app" é pior: o leitor passaria a mostrar a troca como valendo.
- **Pós-choque → Aperto dos Mortos-Vivos** (linhas 302 e 520): falta o **Yorick**. Ele tem imobilização e mesmo assim recebe a troca. O arquivo do Yorick no cliente 16.18 tem as duas trocas (Pós-choque e Aprimoramento Glacial).
- **Aprimoramento Glacial → Primeiro Ataque "(exceto Yorick)"** (linhas 383 e 521): a frase se lê ao contrário, como se o Yorick ficasse de fora. O Yorick **também** troca. A linha 382 explica certo, mas não chega ao app (ver A1). Sugestão de texto: "em campeões sem efeito de imobilização e no Yorick".
- **Fonte da Vida → Demolir no Corki**: falta. Está no arquivo do Corki no cliente 16.18 e na wiki (desde o V13.23).
- **Faixa de Fluxo de Mana → Arcanista do Axioma** (linha 518) e **Presença de Espírito → Triunfo** (linha 519): as duas trocas também acontecem **no URF, com qualquer campeão**.
- **Demolir → Fonte da Vida** (linha 515): falta a segunda condição, "ou onde as estruturas não podem ser alvo".
- Só para conhecimento: a página do **Livro de Feitiços Deslacrado** na wiki cita a troca também na Caçada da Lua Sangrenta, um modo de evento. A lista geral de trocas da wiki não cita. O MD (linhas 390 e 526) fala só de URF e Feitiço Supremo.

### F4. Notas técnicas de uma mecânica que mudou

| Runa | Linha | O que a nota diz | Como é hoje |
|---|---|---|---|
| Conquistador | 48 | dano contínuo dá acúmulo "uma vez a cada 5 segundos" | **4 segundos** (V14.24) |
| Ritmo Fatal | 53 | "permite exceder temporariamente o limite de Velocidade de Ataque" | Não excede mais desde que a runa voltou, no V14.19. A velocidade acima do limite só aumenta o dano do disparo. |
| Presença de Espírito | 77 | a regeneração de Mana "não se atualiza enquanto estiver ativo" (formas da Nidalee e do Jayce) | O efeito de regeneração por 4s saiu no V14.19. Hoje a runa restaura na hora, com recarga de 8s, e a nota não se aplica mais. |
| Aperto dos Mortos-Vivos | 292 | à distância, dano e cura "reduzidos pela metade" | **40% de eficácia** (V25.12). A nota contradiz a descrição da própria runa. |
| Tônico de Distorção no Tempo | 432 | metade da cura na hora, vale para biscoito, trava o reuso, corta a cura por tick | Esse é o efeito do V8.22. Hoje é **40% a mais, na hora, só com poções**, sem trava e sem corte (V10.23, V12.7, V14.10). |
| Celeridade | 246 | só amplia os bônus fixos, "não os bônus percentuais" | Amplia também os percentuais: o aditivo quando os outros passam de 5%, e o multiplicativo sempre. |

### F5. Notas técnicas com erro (a mecânica não mudou)
- **Ritmo Fatal** (linha 55): a nota da redução de "1/6 em vez de 1/3" está invertida. Pela wiki, quem recebe o corte é o **ataque à distância** (Velocidade de Ataque × 0,8 e dano × 0,667). O corpo a corpo fica sem corte.
- **Lenda: Espontaneidade** (linha 86): a nota diz que as três Lendas vão "até 10 acúmulos". A **Linhagem vai até 15**, como a própria descrição dela diz na linha 90.
- **Flashtração Hextec** (linha 406): a condição está trocada. O caso é o **Flash sair da recarga** durante a canalização; enquanto o Hexflash ocupa a vaga, o Flash não pode ser usado.
- **Invocar Aery** (linha 188): o exemplo da Nami está invertido. A regra é que não dá para escudar acertando um **aliado** com a Prisão Aquática.
- **Conquistador** (linha 47): as ondas de fogo da Kayle vêm da **passiva** (Ascensão Divina, nível 11), não do supremo.

### F6. Nomes que não são os oficiais em pt-BR
As regras estão certas. Só os nomes foram traduzidos à mão do inglês da wiki. Dois deles são itens do catálogo do app, e procurar pelo nome errado não acha nada.

| Linha | Runa | No MD | Oficial |
|---|---|---|---|
| 40 | Pressione o Ataque | Lightslinger "da Kalista"; Predador Implacável "do Rengar"; "Mordida Dupla do Renekton" | Lightslinger é do **Lucian**; Ruthless Predator é o W do **Renekton**; Twin Bite é da **Shyvana**, e a lista atual da wiki nem a cita |
| 41, 125 | Pressione o Ataque, Colheita Sombria | Revestimento Tóxico (Teemo) | **Tiro Tóxico** |
| 124 | Colheita Sombria | Chama do Brand | **Labareda** |
| 125 | Colheita Sombria | Angústia de Liandry | **Tormento de Liandry** (item do catálogo) |
| 133 | Chuva de Lâminas | Escolha de Cartas; Uivo Primordial; Cinto-Foguete Hextec | **Escolha uma Carta**; **Uivo Primitivo**; **Explocinturão Hextec** (item do catálogo) |
| 146 | Golpe Desleal | Investida do Alistar | **Atropelar** (E) |
| 419 | Reembolso | "Relicário Antigo etc." | Esse item não existe. Os itens do Guardião são Lâmina, Martelo, Berrante e Orbe do Guardião. |
| 459 | Quebra-Galho | Couraça de Sterak; Fúria de Yun Tal; Fome Insaciável do Presságio da Fome | **Sinal de Sterak**; **Flechatroz de Yun Tal**; a passiva Fome da **Fome Eterna** |

### F7. A linha `Atributos:`
- **Sete runas não têm a linha:** Golpe de Misericórdia, Dilacerar, Até a Morte (Precisão / Slot 3), Golpe de Escudo (Determinação / Slot 1), Osso Revestido (Determinação / Slot 2), Livro de Feitiços Deslacrado (Inspiração / Keystone) e Flashtração Hextec (Inspiração / Slot 1). No app, elas aparecem sem a linha de atributos, porque eu não deduzo do texto. A curadoria é sua (18/09/2026). Se a falta for de propósito, dá para escrever `Atributos: —`, mas hoje o leitor mostraria "—" como etiqueta, então isso pede um ajuste meu antes (A1).
- **Cinco runas listam um atributo que não mexem.** A ficha mostra a etiqueta errada, e a busca por esse atributo acha a runa:
  - Absorção Vital (linha 66), "Vida Máxima": ela só cura;
  - Presença de Espírito (linha 74), "Cura": ela só restaura Mana ou Energia;
  - Faixa de Fluxo de Mana (linha 217), "Cura": ela só mexe com Mana;
  - Revitalizar (linha 363), "Vida Máxima": a Vida só aparece como condição (alvo abaixo de 40%);
  - Perspicácia Cósmica (linha 444), "Aceleração de Habilidade": ela dá aceleração de Feitiço de Invocador e de item.
- **Lenda: Linhagem** (linha 91): o atributo está escrito como a chave crua `roubo_vida`, e a ficha mostra a etiqueta "roubo_vida". O certo é "Roubo de Vida", como na linha 460.
- **Critério para você decidir:** o tipo de dano conta como atributo? Pressione o Ataque, Golpe Desleal, Impacto Repentino, Chamuscar e Demolir listam Dano de Ataque ou Poder de Habilidade porque causam dano, mesmo sem escalar com eles. O Ritmo Fatal, que também causa Dano Adaptativo, não lista. Uma regra só resolve as seis.

### F8. Lemas das trilhas
O MD chama os cinco de "Lema oficial". O texto do cliente em pt-BR (`trans-perks.json`, patch 16.18) é outro em três deles:

| Trilha | Linha | No MD | No cliente |
|---|---|---|---|
| Dominação | 110 | "Caçe e Elimine Presas" (erro de grafia: o certo é "Cace", e aparece assim na tela de Runas) | "Caçar e eliminar presa" |
| Feitiçaria | 181 | "Liberte a Destruição" | "Desferir destruição" |
| Inspiração | 375 | "Ultrapasse os Mortais" | "Iludir os meros mortais" |

Precisão ("Torne-se uma Lenda") e Determinação ("Viva Para Sempre") batem, com diferença só de maiúsculas. Você decide se troca pelo texto do cliente ou se tira a palavra "oficial".

### F9. Cabeçalho do arquivo
- **Força Adaptativa** (linha 12): os números estão certos (0,6 e 166,6%), mas o termo não: a proporção vale para quem **concede Força Adaptativa**, não para "Dano Adaptativo". As linhas 15–16 da própria nota dizem que runa de dano adaptativo não precisa de conversão.
- **"Movimento debilitado" = Imobiliza + Lentidão** (linha 23): na página geral de controle de grupo da wiki, a categoria inclui também **Ancoragem** e **Sonolência**. A Velocidade de Aproximação usa esse termo e o próprio MD lista Ancoragem nela (linhas 449–450). Só que a página da Fonte da Vida define o termo como imobilizar + lentidão. As páginas da wiki divergem entre si, e a escolha é sua.

### F10. Para decidir (o MD está certo, mas cabe uma nota)
- **Ritmo Fatal** (linha 50): o MD copia fielmente o texto da Riot, e o texto da Riot está errado para ataque à distância. O jogo usa 4,8% de Velocidade de Ataque por acúmulo (não 4%) e um dano de mais ou menos 6–20 (não 6–24). O dado do jogo no 16.18 e a wiki concordam nisso.
- **Fonte da Vida** (linha 321): o MD não diz quanto a runa cura, e a Riot também não (o texto dela tem um marcador vazio). A wiki dá 10–54,71 em corpo a corpo e 7–38,29 à distância, do nível 1 ao 20.

---

## Parte 2: do app, quem corrige é o Forjador

Cada item vira uma tarefa com o seu aprovado, como sempre.

### A1. O leitor joga fora o bloco "Controle de grupo válido"
O `gerar_runas_json.py` só reconhece `Atributos:`, `Classes:`, `Força Adaptativa destrinchada` e notas que começam com "- ". As **13 linhas** dos blocos "Controle de grupo válido / Inclui / Não inclui / Obs" de 5 runas somem sem virar pendência:
- Golpe Desleal (linhas 139–141);
- Pós-choque (296–298);
- Fonte da Vida (324–325);
- Aprimoramento Glacial (380–382, inclusive a explicação do Yorick);
- Velocidade de Aproximação (449–450).

O conteúdo desses blocos confere com a wiki. É o mesmo defeito do leitor que descartava 4 runas em 18/09: ele ignora o que não entende e não avisa. O conserto é ler o bloco e mostrá-lo na ficha, ou no mínimo contar as linhas que não reconhece e apontar como pendência. Junto, se você quiser o `Atributos: —`: tratar "—" como "vazio de propósito", e não como etiqueta.

### A2. Bug nº 35 (novo, reproduzido em 23/09/2026): o texto perde a primária e a secundária
A linha `RUNAS:` só sai quando alguma runa da primária está escolhida. Com a trilha primária escolhida mas sem runa, e a secundária completa, o texto leva só `RUNAS 2:` e `FRAGMENTOS:`. Na volta, o `normRunas` sem primária descarta também a secundária. Resultado: a página volta só com os fragmentos, sem aviso nenhum. É da mesma família dos nºs 6 e 16. O link e a publicação não têm esse problema.

### A3. Bug nº 19 (a parte das runas): "Copiar como texto" do lote
`loteParaTexto` não chama `linhasDeRunas`. Quem usa o lote como cópia de segurança perde a página de runas, a ordem de habilidades e o Mestre Forjador. A outra metade do nº 19 (várias builds reimportadas viram uma só) não é de runa.

### A4. Bug nº 29: build publicada aberta "só para ver" tem as runas editáveis
A aba Runas não confere se a build é só para ver: `escolherRuna`, a troca de trilha e o Limpar gravam na hora. A grade de habilidades confere. De quebra: abrir uma publicada com o Editar já ligado deixa a build temporária em modo edição (`activateBuild`).

### A5. "(ainda não vale no app)"
O app **não aplica nenhuma** das 14 trocas automáticas. Todas são só um aviso na ficha, e não existe lógica por campeão nem por modo. O sufixo "(ainda não vale no app)" da troca da Cassiopeia dá a entender que as outras 13 valem. Além disso, o `vigente` depende do texto exato de um comentário do MD. Quando a Cassiopeia sair (F3), o sufixo fica sem uso. Proposta: tirar o sufixo e deixar explícito na tela que as trocas são informativas.

### A6. Documentos desatualizados
- **`docs/servidor/supabase.sql` e o README do servidor** não conhecem runas e habilidades. O README manda "colar o supabase.sql inteiro de novo" quando o SQL muda. Seguindo isso hoje, a view pública perde as colunas `runas` e `habilidades`, e as Públicas deixam de mostrar runas, caladas. Ainda ficariam duas versões de `publicar_build`. O `runas_e_habilidades.sql` precisa entrar no `supabase.sql`, ou o README precisa mandar rodá-lo depois. **É o único destes com risco real.**
- **`docs/formato_de_importacao.md`**: a linha 86 diz "Runas ficam de fora", e as linhas 49–54 documentam `RUNAS:`, `RUNAS 2:` e `FRAGMENTOS:`. O prompt pronto para IA não pede runas, e os nomes válidos de runas não estão em nenhuma lista como a de `marcadores.md`.
- **`docs/qa.md`**: não lista as checagens de runa que o roteiro ganhou nas F13-T8, T12 e T13. O roteiro está em dia, o documento não.
- **`docs/direcao_de_arte.md`**: não tem a tela de Runas (cores das trilhas lidas do ícone, a lombada da ficha, a faixa na forja).
- **`index.html`**, comentário do `vagaHtml`: ainda fala de "Absorvição Vital" e de fragmento sem arte. O código está certo, só o comentário é velho.
- **`docs/prompts_claude_design.md`**: o Prompt C (tela de Runas) nunca foi usado e ainda diz "Domínio".

Relacionado, mas não é de runa: no bug nº 13 ("Última atualização" pula ao trocar de build), uma das causas é comparar runas cruas com runas normalizadas. Quando ele for consertado, a parte das runas se resolve junto.

---

## Para conhecimento (não é pendência)

### Como foi conferido (23/09/2026)
- **Fontes:**
  - Data Dragon 16.18.1 em pt-BR (`data/_runesReforged.json`);
  - dados do cliente do jogo pelo CommunityDragon 16.18: `perks.json`, `trans-perks.json` e os arquivos de alguns campeões;
  - wiki oficial em inglês, com o histórico de patches.
- **Nenhuma runa mudou no 26.19:** os arquivos de runas do cliente no 16.18, no 16.19 e no "latest" são idênticos byte a byte.
- **Números:** das 62 descrições, 7 têm número diferente do da Riot: 6 estão em F1 e o Toque Ígneo em F2. O Livro de Feitiços entra em F1 pelo marcador vazio. Os 71 ícones (62 runas e 9 fragmentos) conferem.
- **Leitura:** uma leitura independente do MD bate com o `runas.js` em tudo, menos nos blocos de controle de grupo (A1).
- **Fragmentos:** estão todos certos: composição dos três grupos, valores (Velocidade de Movimento 2,5%, Tenacidade 15%, Vida 65, Escalamento de Vida 10–180) e as linhas "Força Adaptativa destrinchada". Armadura, Resistência Mágica e Escalamento de Resistência ainda existem no dado do cliente, mas não estão em grupo nenhum no 16.18 (os dois primeiros saíram no V14.2). Estão certos em não aparecer.
- **Trabalho feito:** 7 conferências (uma por trilha, fragmentos, e substituições com cabeçalho) e 59 achados. Cada achado passou por dois céticos, com desempate quando discordaram, e **50 foram confirmados**. Reli os 9 derrubados e 4 voltaram: o Corki (com prova do cliente do jogo), a grafia do lema da Dominação, a etiqueta `roubo_vida` e o critério dos atributos. Os outros ficaram em "Para conhecimento". Na Cassiopeia, os céticos corrigiram a causa: a troca não existe mais, e eu conferi isso no cliente. A varredura do repositório juntou 38 registros espalhados.

### Não "corrija" o MD com estes números da wiki
- **Faixas por nível:** a wiki leva a conta até o nível 20 (existe desde o V26.01 para quem completa a missão da rota do Topo). A Riot mostra só até o 18. Por isso a wiki diz, por exemplo, Eletrocutar 70–260, Chuva de Lâminas 2–22,12, Golpe Desleal 10–49,12, Gosto de Sangue 16–42,82 e Escalamento de Vida 10–200. O MD está certo com os números da Riot.
- **Guardião:** a wiki diz 3s de proteção e 2s de escudo, e a Riot diz 2,5s e 1,5s. O arquivo de dados do jogo no 16.18 usa 2,5 e 1,5. Quem erra é a wiki.

### Outras coisas que vale saber
- **`forja-de-runas.html`**, a sua página de estudo, fora do repositório por decisão sua de 20/09: ela tem uma **segunda cópia dos dados das runas**, digitada à mão, e não lê o `runas.js`. O texto é igual ao do app, com duas exceções: ainda diz "Absorvição Vital" (4 lugares) e tem a troca da Cassiopeia ativa. O app não usa essa página.
- Builds publicadas antes de 20/09 só mostram runas depois de republicadas. É por desenho: a coluna nasceu vazia.
- As runas ficam fora do JSON do cliente do LoL (Arsenal), por decisão sua. O cliente não importa runas.
- Os "fragmentos" do Atributo adicional (Stat Bonus) são de **item**, não de runa. Estão em `docs/pendencias_capitulo1.md`, D3.

---

## O que o arquivo tem

5 trilhas · **62 runas** · 9 fragmentos · 14 substituições automáticas. Não são cinco keystones por trilha: são **3 ou 4 keystones e 3 runas em cada um dos três slots**, que é o desenho do jogo. Comparando com o `runesReforged.json` em pt-BR da Riot: **62 de um lado, 62 do outro**, sem diferença em nenhuma direção.

| Trilha | Keystone | Slot 1 | Slot 2 | Slot 3 |
|---|---|---|---|---|
| Precisão | 4 | 3 | 3 | 3 |
| Dominação | 3 | 3 | 3 | 3 |
| Feitiçaria | 4 | 3 | 3 | 3 |
| Determinação | 3 | 3 | 3 | 3 |
| Inspiração | 3 | 3 | 3 | 3 |

### A arte dos fragmentos
Os fragmentos não estão no `runesReforged.json`. A arte deles vem do `perks.json` do CommunityDragon (os dados do próprio cliente do jogo), casada pelo nome em pt-BR. Cada endereço é pedido de verdade antes de entrar, e o que não responder fica sem ícone e vira pendência.

| Fragmento | Arquivo |
|---|---|
| Força Adaptativa | `StatModsAdaptiveForceIcon.png` |
| Velocidade de Ataque | `StatModsAttackSpeedIcon.png` |
| Aceleração de Habilidade | `StatModsCDRScalingIcon.png` |
| Velocidade de Movimento | `StatModsMovementSpeedIcon.png` |
| Vida | `StatModsHealthScalingIcon.png` |
| Escalamento de Vida | `StatModsHealthPlusIcon.png` |
| Tenacidade e Resistência a Lentidão | `StatModsTenacityIcon.png` |

---

## Resolvido (histórico)
- **18/09 — o leitor descartava 4 runas** (Tônico Triplo, Aperto dos Mortos-Vivos, Transcendência, Tempestade Crescente): a descrição delas ocupa mais de uma linha, e o leitor exigia abrir e fechar o colchete na mesma. Por causa disso a troca do Pós-choque parecia apontar "para o nada". Eu cheguei a dizer que podia ser curadoria sua. O leitor agora conta colchetes, e a comparação com o Data Dragon virou pendência automática. 58 → 62. Commit `ed7a42d`.
- **18/09 — "Absorvição Vital" → "Absorção Vital"** no MD, com a sua autorização: era a única runa sem ícone. Foi a única edição que fiz no seu arquivo.
- **20/09 — arte de Vida e de Escalamento de Vida trocada**, achada por você. Eu tinha escrito à mão a tabela nome → arquivo, e o nome do arquivo da Riot engana: Vida usa `HealthScaling` e Escalamento de Vida usa `HealthPlus`. A tabela à mão saiu (commit `a72fe36`).
- **20/09 — runas na build publicada**, pedido seu. No caminho houve o bug de produção "permission denied" (coluna nova fora do grant), consertado no mesmo dia.
- **F12-T2b — faixa de runas vazia aparecendo em toda build** (`hidden` perdia para `display:flex`).
- **F13-T8 (nº 4) — Duplicar e "Copiar e editar" perdiam as runas.** Os quatro caminhos de cópia agora concordam.
- **F13-T10 (nºs 9 e 10) — acessibilidade e resolução alcançam a tela de Runas.**
- **F13-T12 (nºs 6 e 16) — runa fora do 1º slot e fragmento no grupo errado na ida e volta por texto.** A vaga vazia sai como `-`. De brinde: `normRunas` apagava a página inteira quando não havia primária, inclusive os fragmentos.
- **F13-T13 (nº 7) — o link da build não levava runas.** Agora leva runas, habilidades, layout e Mestre Forjador.

## Lições (para não repetir)
- **Um leitor que ignora o que não entende mente por omissão.** Todo padrão que pode não casar precisa de uma contagem por fora que confira o resultado. O A1 é esta mesma lição, de novo.
- **O nome do arquivo da Riot mente.** A única tabela digitada à mão no projeto foi justamente a que errou.
- **O texto da Riot também erra.** Tem marcador vazio (Livro de Feitiços, Fonte da Vida) e número velho (Ritmo Fatal à distância). Quando o texto e o dado do jogo discordam, vale o dado do jogo.
- **Checagem que nunca foi vista falhando não prova nada.** O roteiro de QA comparava o número de chaves das runas (sempre 6) em vez do conteúdo.
