# Esquema do catalog.json (Capítulo 2)

Gerado por `gerar_catalog_json.py` a partir do `Catalogo_Itens_LoL.md`. Superconjunto do `CATALOG` embutido no HTML da primeira tentativa: os campos antigos mantêm o nome (`namePt`, `nameEn`, `tier`, `priceGold`, `gameModes`, `components`, `buildsInto`, `attributes`, `abilities`, `attributeCategory`, `recommendedArchetype`, `specialEffects`, `region`, `masterwork`, `cashback`, `notes`); os novos entram ao lado.

```
{ "meta": { patch, itemCount, tiers{}, gameModes{}, attributeCategory[], specialEffects[],
            recommendedArchetype[], region[], itemClass{} },
  "items": [ {
    id            : 3053                      // ID do Data Dragon — chave primária e nome do ícone
    slug          : "steraks-gage"            // compatível com o HTML antigo
    namePt, nameEn, wikiName
    iconUrl       : ".../cdn/<patch>/img/item/<id>.png"
    tier          : "Lendário" | "Épico" | "Básico" | "Starter" | "Bota" | "Consumível" | "Trinket" | "Distribuído" | "Evolução" | "Lendário (Evolução)" | "Épico (Evolução)"
    gameModes     : ["Summoner's Rift", "ARAM", "ARAM: Mayhem"]
    priceGold, priceNote
    condition
    components    : [{namePt, nameEn, priceGold, qty}]   combineCost : 775
    buildsInto    : [{namePt, nameEn, priceGold: null, qty}]
    attributes    : [{raw, value, unit: "flat"|"percent", stat, scaling: ["+15% do PdH"]|null}]
    attributesNote
    abilities     : [{name, nameEn, type: "passiva única"|"ativa única"|..., description (texto oficial pt_BR), mechanics (wiki)}]
    costAnalysis  : {goldValue (texto), goldValueTotal (nº), efficiency (texto), efficiencyBase (nº %), extra[]}
    apex          : texto do Ápice
    notes, aramNotes, mayhemNotes
    attributeCategory[], specialEffects[], recommendedArchetype[]
    itemClass     : {core: "AD"|"AP"|"Vitalidade"|"AD e AP", sums: {AD, Vitalidade, AP}, raw}
    region, regionNote
    masterwork    : null | {eligible, stats: [{stat, base, bonus, total}], raw}
    cashback      : null | {percent, refundGold, netGold, raw}
    sources[]
  } ] }
```

Notas de uso para o HTML:
- Preço com Cash Back = `cashback.netGold` (já calculado no catálogo); Ornn = `masterwork.stats` (sobrescreve `attributes` do mesmo `stat`).
- Ápice é texto livre — a tela "todos os itens no máximo" exibe `apex` ao lado dos atributos; onde houver números estruturados (`costAnalysis.efficiency` no ápice) eles estão no texto.
- Filtros: `tier`, `gameModes`, `itemClass.core`, `attributeCategory`, `specialEffects`, `recommendedArchetype`, `region`, `priceGold`, `attributes[].stat/value` (maior/menor atributo).
- Árvore de build: `components`/`buildsInto` usam `nameEn` como chave; ver Integridade referencial no relatório.
