# Esquema do runas.js

`data/runas.js` define `window.RUNAS`. É gerado por `data/gerar_runas_json.py` a
partir de `data/Runas_League_of_Legends.md` (do Leo), e nunca editado à mão.

```
meta         : { fonte, gerado, patch, trilhas, runas, fragmentos }
trilhas[]    : { id, nome, lema, slots[], iconUrl, cor, riotId }
  slots[]    : { nome, tipo, runas[] }
    runas[]  : { id, nome, descricao, atributos[], classes[], adaptativa, notas[], iconUrl, riotId, cg? }
fragmentos[] : { nome, runas[] }          — três linhas, na ordem do jogo
substituicoes[] : { de, para, quando }
```

- `id` é o slug do nome (`pressione-o-ataque`); é por ele que a build guarda a página.
- `iconUrl` vem do Data Dragon (`runesReforged.json` em pt_BR), casado pelo nome
  oficial; nos fragmentos, o arquivo vem do cliente do jogo (`perks.json` do
  Community Dragon), porque o nome do arquivo da Riot não diz qual é qual.
- `riotId` (F13-T26) é o número que o cliente do jogo usa para montar a página de
  runas: 8000–8400 nas trilhas, 8005/8112/… nas runas, 5001–5013 nos fragmentos.
  Vem das mesmas duas listas, pelo mesmo casamento de nome — nunca digitado. O
  gerador confere que cada runa é da trilha em que o arquivo a pôs e que o
  fragmento de cada linha é um dos que o cliente aceita nela (`perkstyles.json`);
  o que não bater vira pendência no relatório. Não aparece na tela: é para o
  "Enviar ao cliente".
- `cg` (F13-T17) são os blocos de controle de grupo da runa, quando ela tem.
- As listas baixadas ficam em cache em `data/_runesReforged.json` e
  `data/_perks_fragmentos.json`; `--baixar` baixa de novo.
