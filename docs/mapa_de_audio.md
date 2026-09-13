# Mapa de Áudio — Montador de Itens (Capítulo 2)

> Derivado dos nomes dos arquivos de `assets/audio/` (lista de 13/09/2026). Todo som passa pelo módulo `Som.play(evento, contexto)`; nenhum outro trecho do código chama `new Audio()`. Variantes `_01.._NN` do mesmo evento são sorteadas, sem repetir a última tocada. Nomes de arquivo são usados exatamente como estão (case-sensitive no GitHub Pages).

## Eixos do sistema

- **Núcleo** (`itemClass.core` do catalog.js): `danodeataque` = AD · `poderdehabilidade` = AP · `tank` = Vitalidade. O único item "AD e AP" (Filhote de Garrabrasa) sorteia entre AD e AP.
- **Tier** (`tier`): Lendário tem som próprio ao entrar no Build (`ui_build_mod_add_legendary_*`), tocado no lugar do `build_item_add` genérico; Consumível/Distribuído/Trinket usam o clique neutro.
- **Item específico** (`nameEn` normalizado: minúsculas, sem espaços, apóstrofos, vírgulas ou acentos): fala rara do lojista ao adicionar ao Build — toca junto com o som do tier, com prioridade sobre a fala genérica.
- **Efeito Especial** (`specialEffects`, normalizado da mesma forma): fala do lojista ao selecionar o filtro daquele efeito.

## Tabela evento → arquivos

| Evento | Quando dispara | Arquivos | Nº |
|---|---|---|---|
| `build:close` | sair da tela Build | `build_close.mp3` | 1 |
| `build:item_add` | item não Lendário entra no Build | `build_item_add_01.mp3`, `build_item_add_02.mp3`, `build_item_add_03.mp3`, `build_item_add_04.mp3` | 4 |
| `build:open` | entrar na tela Build | `build_open_01.mp3`, `build_open_02.mp3`, `build_open_03.mp3`, `build_open_04.mp3`, `build_open_05.mp3`, `build_open_06.mp3` | 6 |
| `catalog:close` | sair do Catálogo | `close_catalog.mp3` | 1 |
| `catalog:open` | tela de entrada → Catálogo (destrava o áudio) | `open_catalog.mp3` | 1 |
| `lojista:build_add:item:bloodthirster` |  | `shopkeeper_build_add_bloodthirster_01.mp3` | 1 |
| `lojista:build_add:item:heartsteel` |  | `shopkeeper_build_add_heartsteel_01.mp3` | 1 |
| `lojista:build_add:item:infinityedge` |  | `shopkeeper_build_add_infinityedge_01.mp3` | 1 |
| `lojista:build_add:item:jakshotheprotean` |  | `shopkeeper_build_add_jakshotheprotean_01.mp3` | 1 |
| `lojista:build_add:item:rabadonsdeathcap` |  | `shopkeeper_build_add_rabadonsdeathcap_01.mp3` | 1 |
| `lojista:build_add:item:rylaiscrystalscepter` |  | `shopkeeper_build_add_rylaiscrystalscepter_01.mp3` | 1 |
| `lojista:efeito_select:danoaolongodotempo` | chip de Efeito Especial correspondente é selecionado | `shopkeeper_build_efeitosespeciais_danoaolongodotempo_select_01.mp3`, `shopkeeper_build_efeitosespeciais_danoaolongodotempo_select_02.mp3` | 2 |
| `lojista:efeito_select:lentidao` | chip de Efeito Especial correspondente é selecionado | `shopkeeper_build_efeitosespeciais_lentidao_select_01.mp3` | 1 |
| `lojista:tag_open:AD` | abrir o grupo de filtro / escolher um filtro do núcleo — [A CONFIRMAR com o Leo na Fase 4: grupo ou chip?] | `shopkeeper_tag_open_danodeataque_01.mp3`, `shopkeeper_tag_open_danodeataque_02.mp3`, `shopkeeper_tag_open_danodeataque_03.mp3`, `shopkeeper_tag_open_danodeataque_04.mp3`, `shopkeeper_tag_open_danodeataque_05.mp3` | 5 |
| `lojista:tag_open:AP` | abrir o grupo de filtro / escolher um filtro do núcleo — [A CONFIRMAR com o Leo na Fase 4: grupo ou chip?] | `shopkeeper_tag_open_poderdehabilidade_01.mp3`, `shopkeeper_tag_open_poderdehabilidade_02.mp3`, `shopkeeper_tag_open_poderdehabilidade_03.mp3`, `shopkeeper_tag_open_poderdehabilidade_04.mp3`, `shopkeeper_tag_open_poderdehabilidade_05.mp3` | 5 |
| `lojista:tag_open:Vitalidade` | abrir o grupo de filtro / escolher um filtro do núcleo — [A CONFIRMAR com o Leo na Fase 4: grupo ou chip?] | `shopkeeper_tag_open_tank_01.mp3`, `shopkeeper_tag_open_tank_02.mp3`, `shopkeeper_tag_open_tank_03.mp3`, `shopkeeper_tag_open_tank_04.mp3`, `shopkeeper_tag_open_tank_05.mp3` | 5 |
| `build:add_legendary:AD` | item Lendário entra no Build (substitui build:item_add) | `ui_build_mod_add_legendary_danodeataque.mp3` | 1 |
| `build:add_legendary:AP` | item Lendário entra no Build (substitui build:item_add) | `ui_build_mod_add_legendary_poderdehabilidade.mp3` | 1 |
| `build:add_legendary:Vitalidade` | item Lendário entra no Build (substitui build:item_add) | `ui_build_mod_add_legendary_tank.mp3` | 1 |
| `catalog:hover:AD` | mouse entra num card do Catálogo (cooldown de 150 ms para não metralhar) | `ui_catalog_mod_hover_danodeataque_01.mp3`, `ui_catalog_mod_hover_danodeataque_02.mp3`, `ui_catalog_mod_hover_danodeataque_03.mp3`, `ui_catalog_mod_hover_danodeataque_04.mp3`, `ui_catalog_mod_hover_danodeataque_05.mp3`, `ui_catalog_mod_hover_danodeataque_06.mp3`, `ui_catalog_mod_hover_danodeataque_07.mp3`, `ui_catalog_mod_hover_danodeataque_08.mp3`, `ui_catalog_mod_hover_danodeataque_09.mp3`, `ui_catalog_mod_hover_danodeataque_10.mp3`, `ui_catalog_mod_hover_danodeataque_11.mp3` | 11 |
| `catalog:hover:AP` | mouse entra num card do Catálogo (cooldown de 150 ms para não metralhar) | `ui_catalog_mod_hover_poderdehabilidade_01.mp3`, `ui_catalog_mod_hover_poderdehabilidade_02.mp3`, `ui_catalog_mod_hover_poderdehabilidade_03.mp3`, `ui_catalog_mod_hover_poderdehabilidade_04.mp3`, `ui_catalog_mod_hover_poderdehabilidade_05.mp3`, `ui_catalog_mod_hover_poderdehabilidade_06.mp3`, `ui_catalog_mod_hover_poderdehabilidade_07.mp3`, `ui_catalog_mod_hover_poderdehabilidade_08.mp3`, `ui_catalog_mod_hover_poderdehabilidade_09.mp3`, `ui_catalog_mod_hover_poderdehabilidade_10.mp3`, `ui_catalog_mod_hover_poderdehabilidade_11.mp3` | 11 |
| `catalog:hover:Vitalidade` | mouse entra num card do Catálogo (cooldown de 150 ms para não metralhar) | `ui_catalog_mod_hover_tank_01.mp3`, `ui_catalog_mod_hover_tank_02.mp3`, `ui_catalog_mod_hover_tank_03.mp3`, `ui_catalog_mod_hover_tank_04.mp3`, `ui_catalog_mod_hover_tank_05.mp3`, `ui_catalog_mod_hover_tank_06.mp3`, `ui_catalog_mod_hover_tank_07.mp3`, `ui_catalog_mod_hover_tank_08.mp3`, `ui_catalog_mod_hover_tank_09.mp3`, `ui_catalog_mod_hover_tank_10.mp3` | 10 |
| `catalog:tag_select` | clique em qualquer chip de filtro | `ui_catalog_tag_select_01.mp3`, `ui_catalog_tag_select_02.mp3`, `ui_catalog_tag_select_03.mp3`, `ui_catalog_tag_select_04.mp3`, `ui_catalog_tag_select_05.mp3`, `ui_catalog_tag_select_06.mp3` | 6 |
| `catalog:click:neutro (tiers Consumível, Distribuído, Trinket)` | clique num card do Catálogo (marca para o Build) | `ui_shop_click_consumivel_distribuido_talisma.mp3` | 1 |
| `catalog:click:AD` | clique num card do Catálogo (marca para o Build) | `ui_shop_click_danodeataque.mp3` | 1 |
| `catalog:click:AP` | clique num card do Catálogo (marca para o Build) | `ui_shop_click_poderdehabilidade.mp3` | 1 |
| `catalog:click:Vitalidade` | clique num card do Catálogo (marca para o Build) | `ui_shop_click_tank.mp3` | 1 |

## Normalização de chaves (itens e efeitos)

```js
const chave = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]/g,'');
// 'Jak\'Sho, The Protean' → 'jakshotheprotean' · 'Dano ao Longo do Tempo' → 'danoaolongodotempo'
```

## Regras de reprodução

- Nada toca antes do clique em "Entrar na loja" (política de autoplay dos navegadores).
- Volume geral e mudo persistem em `localStorage` (`som.volume`, `som.mudo`).
- Falas do lojista não se sobrepõem: se uma fala estiver tocando, a nova fala espera ou é descartada (decidir na Fase 4); sons de interface podem se sobrepor.
- Hover e clique têm cooldown por evento para não disparar em rajada ao rolar a lista.

## Texturas (assets/textures)

- `shopitem_papertexture01_psd.png`
- `shopitem_papertexture02_psd.png`
- `shopitem_papertexture03_psd.png`
