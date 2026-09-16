# Atalhos na URL (links diretos e capturas)

O app aceita um `#hash` na URL. Todos entram na loja sem a placa de entrada (o áudio fica destravado sem tocar, porque não houve clique).

| Hash | O que faz | Uso |
|---|---|---|
| `#item=<slug>` | abre o pergaminho do item (ex.: `#item=infinity-edge`) | compartilhar um item |
| `#b=<código>` | link com a build inteira dentro (gerado por "Copiar link"); quem abre recebe a build na biblioteca e cai na forja | compartilhar |
| `#build` | abre direto na forja (sem hash, a aba Builds abre na lista "Builds", com a chuva de entrada) | compartilhar / captura |
| `#calc` | abre direto na Calculadora | idem |
| `#apice` | liga a caixa Ápice no Catálogo | idem |
| `#ficha=<slug>` | deixa a ficha completa (Shift) daquele card aberta | captura |
| `#animacoes` | congela um quadro da animação de clique de cada tier | captura |
| `#build-animacoes` | congela a placa caindo e a placa afundando na forja | captura |
| `#build-observacao` | abre o editor de observação no primeiro molde (liga a edição) | captura |
| `#build-apice` | forja com Reembolso e Ápice ligados | captura |
| `#build-exportar` | forja com o painel exportar/importar aberto e o texto da build | captura |

Os slugs são os do `data/catalog.js` (campo `slug`, ex.: `atma-s-reckoning`, `rabadon-s-deathcap`).

## Ajustes ao vivo no console
- `Som.LOJISTA.CHANCE = 1; Som.LOJISTA.INTERVALO_MIN_MS = 0;` — o lojista fala em todo acionamento (para testar).
- `Som.verificar()` — confere que os 82 arquivos de áudio carregam (relata no console).
- `Som.setMudo(true)` / `Som.setVolume(0.5)` — o mesmo que o sino e a régua do cabeçalho.

## Nomes aceitos na importação

Todos os marcadores padrão, habilidades e os 225 nomes de item (pt/en) que a linha `MARCADORES:` e as linhas `- Item` reconhecem estão em [marcadores.md](marcadores.md), gerado por `python docs/gerar_marcadores.py`.
