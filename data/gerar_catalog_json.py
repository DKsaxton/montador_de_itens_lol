#!/usr/bin/env python3
"""
gerar_catalog_json.py — Capítulo 2, Lote 0
Converte Catalogo_Itens_LoL.md (Capítulo 1) em catalog.json (esquema estendido, superconjunto do
CATALOG do HTML anterior) e escreve um relatório de validação.

Uso:  python3 gerar_catalog_json.py Catalogo_Itens_LoL.md catalog.json Relatorio_catalogo.md
Gera também catalog.js (window.CATALOG = ...) ao lado do .json — é o que o index.html carrega via <script>.
"""
import re, sys, json, unicodedata
from collections import Counter, OrderedDict

SRC, OUT, REPORT = (sys.argv + ["Catalogo_Itens_LoL.md", "catalog.json", "Relatorio_Lote0_Cap2.md"])[1:4]

HEADER = re.compile(r"^([^\[\]\n]+?): ([^\[\]\n]+?)\[$")          # "Nome PT: Nome EN["
FIELD  = re.compile(r"^    ([^\[\]]+?): ?(.*)$")                   # "    Campo: valor"
SECTION = re.compile(r"^    (Atributo|Habilidade|Análise de custo|Ápice)\[$")
ABILITY = re.compile(r"^\[(.+?)\]\[(.*)\]$")                        # "[Nome — tipo][texto oficial]"

def num_br(s):
    """'1.273,33' -> 1273.33 ; '3.200' -> 3200 ; '25' -> 25"""
    s = s.strip().replace(".", "").replace(",", ".")
    try:
        v = float(s)
        return int(v) if v.is_integer() else v
    except ValueError:
        return None

def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def split_list(v):
    v = v.strip()
    if v.lower() in ("none", "", "nenhum", "nenhuma"): return []
    return [x.strip() for x in v.split(", ") if x.strip()]

def parse_item_refs(v):
    """'Picareta (Pickaxe) 875g, Jak'Sho, o Inconstante (Jak'Sho, The Protean), +775g' -> refs, combine.
    Nomes PT/EN podem conter vírgulas, por isso a varredura é pelos parênteses, não por split."""
    refs, combine = [], None
    v = v.strip()
    if v.lower() == "none": return refs, combine
    m = re.search(r"[,.]? ?\+([\d.,]+)g$", v)
    if m: combine = num_br(m.group(1)); v = v[:m.start()].rstrip(" ,.")
    pos = 0
    for m in re.finditer(r"\(([^()]+)\)(?: ([\d.,]+)g)?(?: \(x(\d+)\))?", v):
        name_pt = v[pos:m.start()].strip(" ,")
        refs.append({"namePt": name_pt, "nameEn": m.group(1),
                     "priceGold": num_br(m.group(2)) if m.group(2) else None,
                     "qty": int(m.group(3)) if m.group(3) else 1})
        pos = m.end()
    rest = v[pos:].strip(" ,")
    if rest: refs.append({"raw": rest})
    return refs, combine

def parse_attr(line):
    raw = line.strip()
    m = re.match(r"^\+([\d.,]+)(%?)((?: \([^()]+\))*) (?:de|do|da) (.+)$", raw)
    if m:
        return {"raw": raw, "value": num_br(m.group(1)),
                "unit": "percent" if m.group(2) else "flat", "stat": m.group(4),
                "scaling": [x.strip("() ") for x in re.findall(r"\([^()]+\)", m.group(3))] or None}
    return {"raw": raw, "value": None, "unit": None, "stat": raw}

def parse_price(v):
    m = re.match(r"^([\d.,]+)g(?: \((.+)\))?", v.strip())
    if m: return num_br(m.group(1)), (m.group(2) or None)
    return None, v.strip()

def parse_class(v):
    m = re.match(r"^(.+?) \((.+)\)$", v.strip())
    core, sums = (m.group(1), m.group(2)) if m else (v.strip(), "")
    s = {}
    for k, val in re.findall(r"(AD|Vitalidade|AP) ([\d.,]+)g", sums): s[k] = num_br(val)
    return {"core": core, "sums": s, "raw": v.strip(), "tiebreak": sums if not s else None}

def parse_masterwork(v):
    v = v.strip()
    if v.lower() == "none": return None
    elig = v.startswith("Elegível")
    stats = [{"stat": st.strip(), "base": num_br(b), "bonus": num_br(bo), "total": num_br(t)}
             for st, b, bo, t in re.findall(r"([A-Za-zÀ-ú ]+?) ([\d.,]+)%?\(\+([\d.,]+)%?\)=([\d.,]+)", v)]
    return {"eligible": elig, "stats": stats, "raw": v}

def parse_cashback(v):
    v = v.strip()
    if v.lower() == "none": return None
    m = re.match(r"^([\d.,]+)% de ([\d.,]+)g = ([\d.,]+)g \(líquido: ([\d.,]+)g\)", v)
    if m: return {"percent": num_br(m.group(1)), "refundGold": num_br(m.group(3)),
                  "netGold": num_br(m.group(4)), "raw": v}
    return {"raw": v}

def parse_region(v):
    m = re.match(r"^(.+?) \((.+)\)$", v.strip())
    return (m.group(1), m.group(2)) if m else (v.strip(), None)

lines = open(SRC, encoding="utf-8").read().split("\n")
items, unparsed, i = [], [], 0
while i < len(lines):
    h = HEADER.match(lines[i])
    if not h: i += 1; continue
    it = OrderedDict(namePt=h.group(1).strip(), nameEn=h.group(2).strip())
    it["slug"] = slug(it["nameEn"])
    i += 1
    section, last_field = None, None
    while i < len(lines) and lines[i] != "]":
        ln = lines[i]
        if section:
            if ln == "    ]": section = None
            else: it.setdefault("_sec_" + section, []).append(ln)
            i += 1; continue
        m = SECTION.match(ln)
        if m: section = m.group(1); i += 1; continue
        m = FIELD.match(ln)
        if m and not ln.startswith("        "):
            key, val = m.group(1).strip(), m.group(2).strip()
            if ln.startswith("    Notas de ARAM: Mayhem:"):
                key, val = "Notas de ARAM: Mayhem", ln.split("Mayhem:", 1)[1].strip()
            it["_f_" + key] = val; last_field = "_f_" + key
        elif ln.startswith("        ") and last_field:
            it[last_field] += "\n" + ln.strip()          # continuação de campo
        elif ln.strip():
            unparsed.append((it["nameEn"], ln))
        i += 1
    items.append(it)

def build(it):
    f = lambda k, d="none": it.get("_f_" + k, d)
    o = OrderedDict()
    o["id"] = int(f("ID")) if f("ID").isdigit() else f("ID")
    o["slug"] = it["slug"]; o["namePt"] = it["namePt"]; o["nameEn"] = it["nameEn"]
    o["wikiName"] = f("Nome na wiki", None)
    o["iconUrl"] = f("Ícone")
    o["tier"] = f("Tier")
    o["gameModes"] = split_list(f("Modo de jogo"))
    o["priceGold"], o["priceNote"] = parse_price(f("Preço"))
    o["condition"] = None if f("Condição").lower() == "none" else f("Condição")
    o["components"], o["combineCost"] = parse_item_refs(f("Componentes"))
    o["buildsInto"], _ = parse_item_refs(f("Ingrediente"))
    o["attributes"] = [parse_attr(l) for l in it.get("_sec_Atributo", []) if l.strip() and not l.strip().lower().startswith("none")]
    o["attributesNote"] = next((l.strip() for l in it.get("_sec_Atributo", []) if l.strip().lower().startswith("none (")), None)
    abilities, cur = [], None
    for l in it.get("_sec_Habilidade", []):
        s = l.strip()
        if not s or s.lower() == "none": continue
        m = ABILITY.match(s)
        if m:
            head = m.group(1); typ = None
            if " — " in head: head, typ = head.rsplit(" — ", 1)
            mm = re.match(r"^(.+?) \(([^()]+)\)$", head)
            cur = {"name": mm.group(1) if mm else head, "nameEn": mm.group(2) if mm else None,
                   "type": typ, "description": m.group(2), "mechanics": ""}
            abilities.append(cur)
        elif s.startswith("Mecânica (wiki):") and cur is not None:
            cur["mechanics"] = (cur["mechanics"] + "\n" if cur["mechanics"] else "") + s[len("Mecânica (wiki):"):].strip()
        elif cur is not None:
            cur["mechanics"] += "\n" + s
        else:
            unparsed.append((o["nameEn"], l))
    o["abilities"] = abilities
    ca = {"goldValue": None, "efficiency": None, "extra": []}
    for l in it.get("_sec_Análise de custo", []):
        s = l.strip()
        if s.startswith("Valor de Ouro:"): ca["goldValue"] = s.split(":", 1)[1].strip()
        elif s.startswith("Eficiência de Ouro:"): ca["efficiency"] = s.split(":", 1)[1].strip()
        elif s: ca["extra"].append(s)
    m = re.search(r"total ([\d.,]+)g", ca["goldValue"] or "")
    ca["goldValueTotal"] = num_br(m.group(1)) if m else None
    m = re.search(r"([\d.,]+)% \(base\)", ca["efficiency"] or "") or re.search(r"^([\d.,]+)%", ca["efficiency"] or "")
    ca["efficiencyBase"] = num_br(m.group(1)) if m else None
    o["costAnalysis"] = ca
    o["apex"] = "\n".join(l.strip() for l in it.get("_sec_Ápice", []) if l.strip())
    o["notes"] = None if f("Notas").lower() == "none" else f("Notas")
    o["aramNotes"] = None if f("Notas de ARAM").lower() == "none" else f("Notas de ARAM")
    o["mayhemNotes"] = None if f("Notas de ARAM: Mayhem").lower() == "none" else f("Notas de ARAM: Mayhem")
    o["attributeCategory"] = split_list(f("Categoria de Atributo"))
    o["itemClass"] = parse_class(f("Classe"))
    o["recommendedArchetype"] = split_list(f("Arquétipo Recomendado"))
    o["specialEffects"] = split_list(f("Efeitos Especiais"))
    o["region"], o["regionNote"] = parse_region(f("Região"))
    o["masterwork"] = parse_masterwork(f("Mestre Forjador"))
    o["cashback"] = parse_cashback(f("Reembolso (runa Cash Back)"))
    o["sources"] = [s.strip() for s in f("Fontes", "").split(" · ") if s.strip()]
    known = {"ID","Ícone","Tier","Modo de jogo","Preço","Condição","Componentes","Ingrediente","Notas","Notas de ARAM",
             "Notas de ARAM: Mayhem","Categoria de Atributo","Classe","Arquétipo Recomendado","Efeitos Especiais","Região",
             "Mestre Forjador","Reembolso (runa Cash Back)","Fontes","Nome na wiki"}
    o["_unknownFields"] = {k[3:]: v for k, v in it.items() if k.startswith("_f_") and k[3:] not in known}
    return o

out = [build(it) for it in items]
patch = None
for o in out:
    m = re.search(r"/cdn/([\d.]+)/", o["iconUrl"] or "");
    if m: patch = m.group(1); break

def distinct(key):
    c = Counter()
    for o in out:
        for v in o[key]: c[v] += 1
    return c

meta = OrderedDict(patch=patch, itemCount=len(out),
    tiers=dict(Counter(o["tier"] for o in out)),
    gameModes=dict(distinct("gameModes")),
    attributeCategory=sorted(distinct("attributeCategory")),
    specialEffects=sorted(distinct("specialEffects")),
    recommendedArchetype=sorted(distinct("recommendedArchetype")),
    region=sorted({o["region"] for o in out}),
    itemClass=dict(Counter(o["itemClass"]["core"] for o in out)))
json.dump({"meta": meta, "items": out}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
JS = OUT[:-5] + ".js" if OUT.endswith(".json") else OUT + ".js"
open(JS, "w", encoding="utf-8").write("// GERADO por gerar_catalog_json.py a partir do Catalogo_Itens_LoL.md — NÃO EDITAR À MÃO\nwindow.CATALOG = " + json.dumps({"meta": meta, "items": out}, ensure_ascii=False) + ";\n")

# ---------- relatório ----------
R = [f"# Relatório — Lote 0 do Capítulo 2 (catálogo → JSON)", "",
     f"Fonte: `{SRC}` · Patch: **{patch}** · Itens: **{len(out)}** · Saída: `{OUT}`", ""]
R += ["## Tiers", ""] + [f"- {k}: {v}" for k, v in meta["tiers"].items()] + [""]
R += ["## Modos de jogo (contagem de itens)", ""] + [f"- {k}: {v}" for k, v in meta["gameModes"].items()] + [""]
R += ["## Classe (núcleo)", ""] + [f"- {k}: {v}" for k, v in meta["itemClass"].items()] + [""]
R += [f"## Categoria de Atributo — {len(meta['attributeCategory'])} valores em uso", "", ", ".join(f"{k} ({v})" for k, v in sorted(distinct('attributeCategory').items())), ""]
R += [f"## Efeitos Especiais — {len(meta['specialEffects'])} valores em uso", "", ", ".join(f"{k} ({v})" for k, v in sorted(distinct('specialEffects').items())), ""]
R += [f"## Arquétipo Recomendado", "", ", ".join(f"{k} ({v})" for k, v in sorted(distinct('recommendedArchetype').items())), ""]
R += [f"## Região — {len(meta['region'])} valores", "", ", ".join(meta["region"]), ""]
probs = []
for o in out:
    if o["priceGold"] is None: probs.append(f"{o['nameEn']}: preço não numérico ({o['priceNote']})")
    if not o["attributes"] and o["tier"] not in ("Consumível", "Trinket", "Distribuído"): probs.append(f"{o['nameEn']}: sem Atributo[]")
    if any("raw" in c for c in o["components"]): probs.append(f"{o['nameEn']}: componente não parseado")
    if any("raw" in c for c in o["buildsInto"]): probs.append(f"{o['nameEn']}: ingrediente não parseado")
    if any(a["value"] is None for a in o["attributes"]): probs.append(f"{o['nameEn']}: atributo sem valor numérico → {[a['raw'] for a in o['attributes'] if a['value'] is None]}")
    if o["costAnalysis"]["goldValueTotal"] is None and o["attributes"]: probs.append(f"{o['nameEn']}: Valor de Ouro sem 'total Xg'")
    if o["costAnalysis"]["efficiencyBase"] is None and o["attributes"]: probs.append(f"{o['nameEn']}: Eficiência sem % base")
    if o["tier"].startswith("Lendário") and o["masterwork"] is None: probs.append(f"{o['nameEn']}: Lendário sem Mestre Forjador")
    if o["itemClass"]["core"] not in ("AD", "AP", "Vitalidade", "AD e AP"): probs.append(f"{o['nameEn']}: Classe inesperada '{o['itemClass']['core']}'")
    if "[A CONFIRMAR" in json.dumps(o, ensure_ascii=False): probs.append(f"{o['nameEn']}: contém [A CONFIRMAR]")
    if o["_unknownFields"]: probs.append(f"{o['nameEn']}: campos desconhecidos {list(o['_unknownFields'])}")
R += [f"## Avisos de parse — {len(probs)}", ""] + [f"- {p}" for p in probs] + [""]
R += [f"## Linhas não reconhecidas — {len(unparsed)}", ""] + [f"- {n}: `{l.strip()}`" for n, l in unparsed[:60]] + [""]
open(REPORT, "w", encoding="utf-8").write("\n".join(R))
print(f"{len(out)} itens → {OUT}; {len(probs)} avisos; {len(unparsed)} linhas não reconhecidas → {REPORT}")
