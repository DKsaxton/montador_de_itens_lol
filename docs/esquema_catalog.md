# Esquema do catalog.json (Capítulo 2)

Gerado por `gerar_catalog_json.py` a partir do `Catalogo_Itens_LoL.md`. Superconjunto do `CATALOG` embutido no HTML da primeira tentativa: os campos antigos mantêm o nome (`namePt`, `nameEn`, `tier`, `priceGold`, `gameModes`, `components`, `buildsInto`, `attributes`, `abilities`, `attributeCategory`, `recommendedArchetype`, `specialEffects`, `region`, `masterwork`, `cashback`, `notes`); os novos entram ao lado.

```
{ "meta": { patch, itemCount, tiers{}, gameModes{}, attributeCategory[], specialEffects[],
            recommendedArchetype[], region[], itemClass{},
            statPrices      : [{stat, unit, gold (nº), reference, raw}]     // 21 linhas, wiki "Gold efficiency"   (23/09/2026)
            masterworkPrices: [{stat, gold (nº | null), raw}] },            // 7 linhas, Ornn#Notes; Vida é variável (23/09/2026)
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
    costAnalysis  : {goldValue (texto), goldValueTotal (nº), efficiency (texto), efficiencyBase (nº %), extra[],
                     goldValueStats (nº | null) — só Atributo[], igual à tabela da wiki          (23/09/2026)
                     goldValueBase  (nº | null) — numerador da efficiencyBase (com o que o artigo conta)}
    apex          : texto do Ápice
    apexNumeric   : null | {stats: [{stat, value, unit: "flat"|"percent", mode: "total"|"extra", note}],
                            goldValue (nº | null), goldValueRaw, efficiency (nº % | null), efficiencyRaw}   (23/09/2026)
                    // null = Ápice "igual ao base"; goldValue/efficiency null com Raw = valor condicional ("sem teto…", "525g se…")
    fragments     : null | [{tier: "Prata"|"Ouro"|"Prismático", name (EN, fragmento composto) | null,
                             stats: [{stat, value, unit, note}], gold (nº | null), goldRaw, raw}]      // só o Atributo adicional (23/09/2026)
    notes, aramNotes, mayhemNotes
    attributeCategory[], specialEffects[], recommendedArchetype[]
    itemClass     : {core: "AD"|"AP"|"Vitalidade"|"AD e AP", sums: {AD, Vitalidade, AP}, raw}
    region, regionNote
    masterwork    : null | {eligible, stats: [{stat, base, bonus, total}], raw, bonusGold (nº | null; 1.000 nos 109 elegíveis — 23/09/2026)}
    cashback      : null | {percent, refundGold, netGold, raw}
    sources[]
  } ] }
```

Notas de uso para o HTML:
- Preço com Cash Back = `cashback.netGold` (já calculado no catálogo); Ornn = `masterwork.stats` (sobrescreve `attributes` do mesmo `stat`).
- Ápice: `apex` é o texto; desde 23/09/2026 os números estão em `apexNumeric` (atributo no máximo, se é o total ou "a mais", valor em ouro e eficiência no ápice). "total" substitui o atributo do item; "extra" soma a ele (às vezes em outra unidade).
- Valor em ouro: `goldValueBase` é o que a eficiência base usa (com a passiva, como o artigo da wiki); `goldValueStats` é só dos atributos (como a tabela da wiki). O antigo `goldValueTotal` fica como estava (em 19 itens ele é só atributos, em 5 inclui o efeito).
- Filtros: `tier`, `gameModes`, `itemClass.core`, `attributeCategory`, `specialEffects`, `recommendedArchetype`, `region`, `priceGold`, `attributes[].stat/value` (maior/menor atributo).
- Árvore de build: `components`/`buildsInto` usam `nameEn` como chave; ver Integridade referencial no relatório.
