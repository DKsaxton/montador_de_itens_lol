#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera data/runas.js a partir de data/Runas_League_of_Legends.md.

Mesmo contrato do gerar_catalog_json.py: a fonte e o markdown, o app nunca
recebe dado digitado a mao, e o que faltar vira pendencia relatada aqui em vez
de ser inventado.

O icone de cada runa vem do Data Dragon da Riot (runesReforged.json em pt_BR),
casado pelo NOME oficial. Runa que nao casar fica sem icone e aparece no
relatorio — nunca chuto o id da Riot.

Uso:
    python data/gerar_runas_json.py            # usa o cache, se houver
    python data/gerar_runas_json.py --baixar   # rebaixa o runesReforged.json
"""
import io
import json
import os
import difflib
import re
import sys
import unicodedata
import urllib.request
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
ICONES = os.path.join(AQUI, "_icones_trilha")
FONTE = os.path.join(AQUI, "Runas_League_of_Legends.md")
SAIDA = os.path.join(AQUI, "runas.js")
CACHE = os.path.join(AQUI, "_runesReforged.json")
CATALOG = os.path.join(AQUI, "catalog.js")
DD = "https://ddragon.leagueoflegends.com/cdn/{v}/data/pt_BR/runesReforged.json"
DD_IMG = "https://ddragon.leagueoflegends.com/cdn/img/"
STATMODS = DD_IMG + "perk-images/StatMods/"
# Os fragmentos nao estao no runesReforged.json. Quem diz qual arquivo pertence a
# qual fragmento e o perks.json do Community Dragon, que carrega os dados do
# proprio cliente do jogo. E precisa ser ele: o NOME DO ARQUIVO da Riot mente —
# "Vida" usa StatModsHealthScalingIcon e "Escalamento de Vida" usa
# StatModsHealthPlusIcon, o contrario do que os nomes sugerem. Eu tinha digitado
# essa tabela a mao e troquei os dois (Leo achou em 20/09/2026).
CDRAGON = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/pt_br/v1/perks.json"
CACHE_FRAG = os.path.join(AQUI, "_perks_fragmentos.json")


def slug(texto):
    """Slug sem acento, igual ao do catálogo: minúsculas e hífens."""
    base = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", base.lower())).strip("-")


def chave(texto):
    """Chave de comparação de nomes: sem acento, sem pontuação, sem espaço."""
    base = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", base.lower())


# --------------------------------------------------------------- leitura
def ler_linhas():
    with io.open(FONTE, encoding="utf-8") as f:
        return [l.rstrip("\n") for l in f]


def recorta(linhas, abre, fecha_col=0):
    """Devolve as linhas de dentro de um bloco `abre` até o fechamento na coluna dada."""
    ini = next(i for i, l in enumerate(linhas) if l.startswith(abre))
    prof = 0
    for j in range(ini, len(linhas)):
        prof += linhas[j].count("{") - linhas[j].count("}")
        if j > ini and prof == 0:
            return linhas[ini + 1:j]
    raise ValueError("bloco %r não fecha" % abre)


RE_TRILHA = re.compile(r'^\s{8}(?P<nome>[^(\[]+?)\s*\(Lema oficial:\s*"(?P<lema>[^"]+)"\)\[\s*$')
RE_SLOT = re.compile(r"^\s{12}(?P<nome>Keystone|Slot \d)\[\s*$")
RE_RUNA = re.compile(r"^\s{16}(?P<nome>[^\[]+?)\[(?P<resto>.*)$")
RE_FRAG_SLOT = re.compile(r"^\s{4}(?P<nome>Slot \d)\[\s*$")
RE_FRAG_RUNA = re.compile(r"^\s{8}(?P<nome>[^\[]+?)\[(?P<resto>.*)$")
RE_CAMPO = re.compile(r"^\s+(?P<campo>Atributos|Classes|Força Adaptativa destrinchada[^:]*):\s*(?P<valor>.+)$")
RE_NOTA = re.compile(r"^\s+-\s+(?P<texto>.+)$")


def le_runas(linhas, re_runa, pendencias, onde):
    """Le uma sequencia de runas com seus campos indentados.

    A descricao pode ocupar VARIAS linhas: ha runas cujo colchete so fecha tres
    ou quatro linhas abaixo (Transcendencia, Tonico Triplo, Aperto dos
    Mortos-Vivos, Tempestade Crescente). O leitor antigo exigia abrir e fechar
    na mesma linha e descartava essas runas caladamente — e ainda grudava as
    linhas de continuacao como "notas tecnicas" da runa anterior.
    """
    runas, atual = [], None
    vazios = set()
    i, n = 0, len(linhas)
    while i < n:
        linha = linhas[i]
        m = re_runa.match(linha)
        if m:
            nome = m.group("nome").strip()
            resto = m.group("resto")
            # junta ate os colchetes fecharem
            partes, saldo = [resto], 1 + resto.count("[") - resto.count("]")
            while saldo > 0 and i + 1 < n:
                i += 1
                partes.append(linhas[i].strip())
                saldo += linhas[i].count("[") - linhas[i].count("]")
            desc = " ".join(p for p in partes if p).strip()
            if desc.endswith("]"):
                desc = desc[:-1].strip()
            elif saldo > 0:
                pendencias.append("%s: o colchete de %r não fecha" % (onde, nome))
            atual = {
                "id": slug(nome), "nome": nome, "descricao": desc,
                "atributos": [], "classes": [], "adaptativa": "", "notas": [],
            }
            if not desc:
                pendencias.append("%s: %s está sem descrição" % (onde, nome))
            runas.append(atual)
            i += 1
            continue
        if atual is not None:
            m = RE_CAMPO.match(linha)
            if m:
                campo, valor = m.group("campo"), m.group("valor").strip()
                if campo == "Atributos":
                    # "—" = a runa não dá nem escala com atributo nenhum, de
                    # propósito (Leo, 23/09/2026): lista vazia, sem pendência.
                    if valor in ("—", "-"):
                        vazios.add(id(atual))
                        valor = ""
                    atual["atributos"] = [x.strip() for x in valor.split(",") if x.strip()]
                elif campo == "Classes":
                    atual["classes"] = [x.strip() for x in valor.split(",") if x.strip()]
                else:
                    atual["adaptativa"] = valor
                i += 1
                continue
            m = RE_NOTA.match(linha)
            if m and "Notas técnicas" not in linha:
                atual["notas"].append(m.group("texto").strip())
        i += 1
    for r in runas:
        if not r["atributos"] and id(r) not in vazios:
            pendencias.append("%s: %s está sem Atributos" % (onde, r["nome"]))
        if not r["classes"]:
            pendencias.append("%s: %s está sem Classes" % (onde, r["nome"]))
    return runas


def le_trilhas(linhas, pendencias):
    trilhas, trilha, slot = [], None, None
    buffer, dono = [], None

    def fecha():
        if dono is not None:
            dono["runas"] = le_runas(buffer, RE_RUNA, pendencias, "%s / %s" % (trilha["nome"], dono["nome"]))

    for l in linhas:
        m = RE_TRILHA.match(l)
        if m:
            fecha(); buffer, dono = [], None
            trilha = {"id": slug(m.group("nome")), "nome": m.group("nome").strip(),
                      "lema": m.group("lema").strip(), "slots": []}
            trilhas.append(trilha)
            continue
        m = RE_SLOT.match(l)
        if m:
            fecha(); buffer = []
            dono = {"nome": m.group("nome"), "tipo": "keystone" if m.group("nome") == "Keystone" else "slot", "runas": []}
            trilha["slots"].append(dono)
            continue
        buffer.append(l)
    fecha()
    return trilhas


def le_fragmentos(linhas, pendencias):
    fragmentos, atual, buffer = [], None, []

    def fecha():
        if atual is not None:
            atual["runas"] = le_runas(buffer, RE_FRAG_RUNA, pendencias, "Fragmentos / %s" % atual["nome"])

    for l in linhas:
        m = RE_FRAG_SLOT.match(l)
        if m:
            fecha(); buffer = []
            atual = {"nome": m.group("nome"), "runas": []}
            fragmentos.append(atual)
            continue
        buffer.append(l)
    fecha()
    return fragmentos


RE_SUBST = re.compile(r"^\s{4}(?P<de>.+?)\s*->\s*vira\s+(?P<para>.+?)(?:\s+(?P<quando>(?:em|no|na|nos|nas) .+))?\s*$")


def le_substituicoes(linhas):
    fora = False
    subs = []
    for l in linhas:
        if l.strip().startswith("--"):
            # o bloco final do markdown é o que ainda não vale no app
            if "ainda não está no app" in l:
                fora = True
            continue
        m = RE_SUBST.match(l)
        if m:
            subs.append({"de": m.group("de").strip(), "para": m.group("para").strip(),
                         "quando": (m.group("quando") or "").strip(), "vigente": not fora})
    return subs


# --------------------------------------------------------------- ícones
def patch_do_catalogo():
    try:
        dados = json.loads(io.open(CATALOG, encoding="utf-8").read().split("=", 1)[1].rstrip().rstrip(";"))
        return dados["meta"]["patch"]
    except Exception:
        return None


def baixa_runes(patch, forcar):
    if os.path.exists(CACHE) and not forcar:
        return json.load(io.open(CACHE, encoding="utf-8"))
    url = DD.format(v=patch)
    print("  baixando %s" % url)
    with urllib.request.urlopen(url, timeout=30) as r:
        dados = json.loads(r.read().decode("utf-8"))
    io.open(CACHE, "w", encoding="utf-8").write(json.dumps(dados, ensure_ascii=False))
    return dados


def arte_dos_fragmentos(forcar):
    """chave do nome -> arquivo do icone, direto do cliente do jogo."""
    if os.path.exists(CACHE_FRAG) and not forcar:
        return json.load(io.open(CACHE_FRAG, encoding="utf-8"))
    print("  baixando %s" % CDRAGON)
    req = urllib.request.Request(CDRAGON, headers={"User-Agent": "montador-de-itens-lol (uso pessoal)"})
    with urllib.request.urlopen(req, timeout=40) as r:
        dados = json.loads(r.read().decode("utf-8"))
    mapa = {}
    for p in dados:
        if 5000 <= p.get("id", 0) <= 5020 and p.get("iconPath"):
            mapa[chave(p.get("name", ""))] = p["iconPath"].split("/")[-1]
    io.open(CACHE_FRAG, "w", encoding="utf-8").write(json.dumps(mapa, ensure_ascii=False))
    return mapa


def mapa_de_icones(runes):
    """chave normalizada -> (caminho do ícone, nome como a Riot escreve)."""
    mapa, oficiais = {}, {}
    for trilha in runes:
        mapa[chave(trilha["name"])] = trilha["icon"]
        oficiais[chave(trilha["name"])] = trilha["name"]
        for slot in trilha["slots"]:
            for r in slot["runes"]:
                mapa[chave(r["name"])] = r["icon"]
                oficiais[chave(r["name"])] = r["name"]
    return mapa, oficiais


# --------------------------------------------------------------- cor da trilha
# A cor de cada trilha é LIDA do PNG oficial dela, não escolhida no olho — o
# mesmo caminho dos brasões das regiões (docs/gerar_brasoes.py, que também
# decodifica PNG em Python puro, sem dependência).
def cor_da_trilha(url, nome):
    import importlib.util
    cam = os.path.join(RAIZ, "docs", "gerar_brasoes.py")
    spec = importlib.util.spec_from_file_location("brasoes", cam)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if not os.path.isdir(ICONES):
        os.makedirs(ICONES)
    destino = os.path.join(ICONES, slug(nome) + ".png")
    if not os.path.exists(destino):
        with urllib.request.urlopen(url, timeout=30) as r:
            io.open(destino, "wb").write(r.read())
    cores = mod.paleta(destino, 3)
    return cores[0][0] if cores else None


# --------------------------------------------------------------- main
def main():
    forcar = "--baixar" in sys.argv
    linhas = ler_linhas()
    pendencias = []

    trilhas = le_trilhas(recorta(linhas, "Runas Primarias{"), pendencias)
    fragmentos = le_fragmentos(recorta(linhas, "Runas Terciarias (Fragmentos){"), pendencias)
    substituicoes = le_substituicoes(recorta(linhas, "Substituicoes Automaticas{"))

    patch = patch_do_catalogo()
    icones, nomes_riot, sem_icone = {}, {}, []
    if patch:
        try:
            icones, nomes_riot = mapa_de_icones(baixa_runes(patch, forcar))
        except Exception as e:
            pendencias.append("ícones do Data Dragon não vieram (%s); as runas ficam sem ícone" % e)
    else:
        pendencias.append("patch do catálogo não encontrado; as runas ficam sem ícone")

    def veste(r):
        cam = icones.get(chave(r["nome"]))
        if cam:
            r["iconUrl"] = DD_IMG + cam
        else:
            sem_icone.append(r["nome"])
        return r

    for t in trilhas:
        cam = icones.get(chave(t["nome"]))
        if cam:
            t["iconUrl"] = DD_IMG + cam
            try:
                cor = cor_da_trilha(t["iconUrl"], t["nome"])
                if cor:
                    t["cor"] = cor
            except Exception as e:
                pendencias.append("cor da trilha %s não pôde ser lida do ícone (%s)" % (t["nome"], e))
        elif icones:
            sem_icone.append("(trilha) " + t["nome"])
        for s in t["slots"]:
            s["runas"] = [veste(r) for r in s["runas"]]
    # fragmentos: o arquivo de cada um vem do cliente do jogo, e ainda assim
    # cada URL e pedida de verdade antes de entrar
    try:
        arte = arte_dos_fragmentos(forcar)
    except Exception as e:
        arte = {}
        pendencias.append("lista de arte dos fragmentos nao veio (%s); eles ficam sem icone" % e)
    conferidas = {}
    for f in fragmentos:
        for r in f["runas"]:
            arquivo = arte.get(chave(r["nome"]))
            if not arquivo:
                pendencias.append("o fragmento %r nao tem arte na lista do cliente do jogo" % r["nome"])
                continue
            if arquivo not in conferidas:
                url = STATMODS + arquivo
                try:
                    with urllib.request.urlopen(url, timeout=20) as resp:
                        conferidas[arquivo] = url if resp.status == 200 and len(resp.read()) > 100 else None
                except Exception as e:
                    conferidas[arquivo] = None
                    pendencias.append("a arte do fragmento %r nao respondeu (%s)" % (r["nome"], e))
            if conferidas[arquivo]:
                r["iconUrl"] = conferidas[arquivo]

    # --- integridade 1: a substituição automática aponta para runa que existe? ---
    nomes = {chave(r["nome"]) for t in trilhas for s in t["slots"] for r in s["runas"]}
    nomes |= {chave(r["nome"]) for f in fragmentos for r in f["runas"]}
    # O RE_SUBST corta o destino na primeira preposição: "Tônico de Distorção no
    # Tempo no ARAM" sai como "Tônico de Distorção" + "no Tempo no ARAM". Quando o
    # destino lido não é runa, vale o nome de runa mais longo que começa ali, e o
    # resto volta para a condição. Se nenhum casar, a checagem abaixo acusa.
    por_tamanho = sorted({r["nome"] for t in trilhas for s in t["slots"] for r in s["runas"]}, key=len, reverse=True)
    for sub in substituicoes:
        if chave(sub["para"]) in nomes:
            continue
        inteiro = (sub["para"] + " " + sub["quando"]).strip()
        for n in por_tamanho:
            if inteiro == n or inteiro.startswith(n + " "):
                sub["para"], sub["quando"] = n, inteiro[len(n):].strip()
                break
    for sub in substituicoes:
        for lado in ("de", "para"):
            if chave(sub[lado]) not in nomes:
                pendencias.append("substituição \"%s -> %s\": %r não existe na lista de runas"
                                  % (sub["de"], sub["para"], sub[lado]))

    # --- integridade 2: falta alguma runa que a Riot tem? ---
    # Esta é a checagem que teria pegado o leitor descartando as runas de
    # descrição multilinha (18/09/2026). Antes ela era uma nota solta num doc,
    # e eu tratei a diferença como curadoria do Leo. Agora é pendência.
    if icones:
        nomes_meus = {chave(r["nome"]) for t in trilhas for s2 in t["slots"] for r in s2["runas"]}
        for ch, nome_riot in nomes_riot.items():
            if ch in {chave(t["nome"]) for t in trilhas}:
                continue                       # é nome de trilha, não de runa
            if ch not in nomes_meus:
                pendencias.append("a Riot tem %r e o arquivo não — confira se o leitor não a perdeu" % nome_riot)

    # --- integridade 3: o nome bate com o oficial da Riot? ---
    # Não corrijo nada: o markdown é a fonte. Só aponto o mais parecido, que é
    # onde costuma estar o erro de digitação.
    if icones:
        oficiais = {}
        for t in trilhas:
            for s in t["slots"]:
                for r in s["runas"]:
                    if "iconUrl" not in r:
                        oficiais[r["nome"]] = None
        todos = list(icones.keys())
        for nome in oficiais:
            perto = difflib.get_close_matches(chave(nome), todos, 1, 0.75)
            if perto:
                pendencias.append("%r não existe no Data Dragon; lá está escrito %r"
                                  % (nome, nomes_riot[perto[0]]))

    total = sum(len(s["runas"]) for t in trilhas for s in t["slots"])
    dados = {
        "meta": {
            "fonte": "data/Runas_League_of_Legends.md",
            "gerado": date.today().isoformat(),
            "patch": patch,
            "trilhas": len(trilhas),
            "runas": total,
            "fragmentos": sum(len(f["runas"]) for f in fragmentos),
        },
        "trilhas": trilhas,
        "fragmentos": fragmentos,
        "substituicoes": substituicoes,
    }

    js = "window.RUNAS = " + json.dumps(dados, ensure_ascii=False, indent=1) + ";\n"
    io.open(SAIDA, "w", encoding="utf-8", newline="\n").write(js)

    print("data/runas.js gerado")
    print("  %d trilhas, %d runas, %d fragmentos, %d substituições"
          % (len(trilhas), total, dados["meta"]["fragmentos"], len(substituicoes)))
    for t in trilhas:
        print("  %-12s %s" % (t["nome"], " · ".join("%s %d" % (s["nome"], len(s["runas"])) for s in t["slots"])))
    if sem_icone:
        print("\n  sem ícone do Data Dragon (%d): %s" % (len(sem_icone), ", ".join(sem_icone)))
    if pendencias:
        print("\n  PENDÊNCIAS (%d):" % len(pendencias))
        for p in pendencias:
            print("   - %s" % p)
    else:
        print("\n  integridade: nenhuma pendência")


if __name__ == "__main__":
    main()
