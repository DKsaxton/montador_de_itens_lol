"""Gera docs/marcadores.md: todos os nomes aceitos na linha MARCADORES (e nas linhas de item)
da importação em texto. Lê data/catalog.js e a lista MARCADORES do index.html — nada digitado à mão.
Uso: python docs/gerar_marcadores.py   (na raiz do repositório)"""
import json, io, re, unicodedata, os
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = io.open(os.path.join(RAIZ, 'data', 'catalog.js'), encoding='utf-8').read()
cat = json.loads(s[s.index('=') + 1:].rstrip().rstrip(';'))
items = cat['items']
html = io.open(os.path.join(RAIZ, 'index.html'), encoding='utf-8').read()
ini = html.index('const MARCADORES = [')
tags = re.findall(r'\{ id: "([^"]+)", label: "([^"]+)" \}', html[ini:html.index('];', ini)])
tiers = ["Starter", "Consumível", "Trinket", "Distribuído", "Bota", "Básico", "Épico", "Lendário", "Evolução"]
def ordem(t): return tiers.index(t) if t in tiers else 99
def sem_acento(x): return unicodedata.normalize('NFD', x).encode('ascii', 'ignore').decode().lower()
por_tier = {}
for it in items: por_tier.setdefault(it['tier'], []).append(it)
L = ["# Marcadores e nomes aceitos na importação\n",
     f"Gerado a partir de `data/catalog.js` (patch {cat['meta'].get('patch', '?')}, {len(items)} itens) e da lista `MARCADORES` do `index.html`. Não editar à mão: regenerar com o comando no fim.\n",
     "## Como escrever a linha\n", "```\nMARCADORES: AD | Habilidade Q | Gume do Infinito\n```\n",
     "- Até **3** marcadores, separados por ` | `. O 4º em diante é ignorado.",
     "- Maiúsculas/minúsculas e acentos **não importam** (`gume do infinito` = `Gume do Infinito`).",
     "- Um nome que não bate com nenhuma das listas abaixo é **descartado em silêncio** (a build importa, mas sem aquele marcador).",
     "- Os mesmos nomes de item valem nas linhas `- Item` das caixas e em `MESTRE FORJADOR: Item`.",
     "- Habilidade só faz sentido com `CAMPEÃO:` preenchido; sem campeão o marcador aparece só como a letra.\n",
     f"## 1. Marcadores padrão ({len(tags)})\n", "Escreva exatamente o rótulo (a coluna *id* é só para conferência do arquivo SVG).\n",
     "| Rótulo | id |\n|---|---|"]
L += [f"| `{lab}` | {i} |" for i, lab in tags]
L += ["\n## 2. Habilidades (4)\n", "| Escreva |\n|---|"] + [f"| `Habilidade {l}` |" for l in "QWER"]
L += [f"\n## 3. Itens do catálogo ({len(items)})\n", "Vale o nome em português **ou** em inglês; qualquer um dos dois resolve para o mesmo item.\n"]
for t in sorted(por_tier, key=lambda t: (ordem(t), t)):
    lst = sorted(por_tier[t], key=lambda x: sem_acento(x['namePt']))
    L += [f"### {t} ({len(lst)})\n", "| Português | Inglês |\n|---|---|"] + [f"| `{it['namePt']}` | `{it['nameEn']}` |" for it in lst] + [""]
L += ["## Regenerar\n", "```bash\npython docs/gerar_marcadores.py\n```\n"]
io.open(os.path.join(RAIZ, 'docs', 'marcadores.md'), 'w', encoding='utf-8', newline='\n').write("\n".join(L))
print(f"docs/marcadores.md: {len(tags)} marcadores, 4 habilidades, {len(items)} itens")
