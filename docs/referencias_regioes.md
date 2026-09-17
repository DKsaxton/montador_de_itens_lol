# Banco de referências — regiões de Runeterra

Nada aqui é escolha de gosto: o brasão vem da Riot e a paleta foi lida de dentro do próprio brasão.

## De onde vêm os brasões

Data Dragon do **Legends of Runeterra**, que é da Riot e é aberto:

```
https://dd.b.pvp.net/latest/core/en_us/img/regions/icon-<regiao>.png
```

A lista de regiões e o caminho de cada ícone saem de `https://dd.b.pvp.net/latest/core/en_us/data/globals-en_us.json`, chave `regions`.

Os arquivos já estão no projeto, em `assets/regioes/`, com nomes em minúsculas e hífen.

**O Data Dragon do League of Legends não tem brasão de região.** Ele serve campeões, itens, runas, magias e mapas. Por isso a fonte é o Data Dragon do LoR.

## Duas ressalvas

1. **Piltover e Zaun dividem um brasão.** A Riot publica um só, `icon-piltoverzaun.png`. Os dois cards usam o mesmo símbolo e se separam pela paleta: Piltover puxa para o ouro, Zaun para o laranja sujo e o metal escuro.
2. **O Vazio não tem brasão publicado** nesses endpoints abertos, nem no LoR nem no Data Dragon do LoL. O símbolo do card de The Void é o único inventado, e está marcado como tal no canvas.

## Paleta de cada região

As três primeiras cores dominantes lidas do PNG do brasão, ignorando o transparente e o preto de contorno.

| Região | Itens | Cor 1 | Cor 2 | Cor 3 | Arquivo |
|---|---|---|---|---|---|
| Runeterra | 163 | `#907848` | `#a89048` | `#604830` | `runeterra.png` |
| Ionia | 10 | `#c04878` | `#d890a8` | `#d8a8c0` | `ionia.png` |
| Freljord | 8 | `#60c0f0` | `#90d8f0` | `#c0d8f0` | `freljord.png` |
| Noxus | 7 | `#c04848` | `#a83030` | `#781818` | `noxus.png` |
| Demacia | 7 | `#d8c090` | `#f0d8d8` | `#d8d8c0` | `demacia.png` |
| Targon | 5 | `#6030d8` | `#9060f0` | `#7848f0` | `targon.png` |
| Bilgewater | 5 | `#a84830` | `#c06030` | `#d87848` | `bilgewater.png` |
| The Void | 5 | `#7c1f7a` | `#5a1560` | `#b055c0` | sem brasão oficial |
| Shadow Isles | 4 | `#00a890` | `#007848` | `#00c0a8` | `shadow-isles.png` |
| Piltover | 4 | `#d8a848` | `#f09060` | `#d8c030` | `piltover-zaun.png` |
| Zaun | 3 | `#f09060` | `#d8a848` | `#7a5a20` | `piltover-zaun.png` |
| Shurima | 2 | `#f0d830` | `#d8c030` | `#d8a818` | `shurima.png` |
| Bandle City | 2 | `#a8c000` | `#90a800` | `#c0d848` | `bandle-city.png` |

## O que a paleta corrigiu

Três regiões que eu tinha desenhado pelo palpite e estavam erradas:

- **Targon** é roxo forte, não azul-noite com estrelas.
- **Bilgewater** é ferrugem e laranja queimado, não madeira com verde-água.
- **Bandle City** é verde-limão, não feltro bege.

E duas que estavam perto mas fracas: Shadow Isles é verde-água profundo, não verde claro; Shurima é ouro puro, não areia.

## Como regenerar

```bash
python docs/gerar_brasoes.py
```

Baixa os brasões que faltarem em `assets/regioes/` e imprime a paleta de cada um. Não sobrescreve o que já está lá.
