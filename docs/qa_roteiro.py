#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Roteiro de QA do Montador de Itens — os caminhos de sempre, percorridos a cada mudança.

    python docs/qa_roteiro.py            # o app desta pasta
    python docs/qa_roteiro.py --site     # o que está no ar, no GitHub Pages
    python docs/qa_roteiro.py -k marcador   # só as checagens com essa palavra

Por que ele existe: em 20/09/2026 dois bugs foram parar no ar e quem achou foi o
Leo — a aba Públicas vazia e os marcadores mudos. Nenhum dos dois era difícil de
pegar: bastava abrir o app e percorrer o de sempre. O roteiro faz isso com
clique de verdade (CDP), porque evento sintético já passou com bug no drag e no
duplo clique.

Ele não substitui o olho: mede o que dá para medir e cala sobre o resto.
Captura de tela e aprovado continuam por fora.

Precisa de: Chrome instalado e `pip install websocket-client`.
"""
import argparse
import atexit
import base64
import json
import os
import re
import socket
import subprocess
import sys
import threading
import time
import urllib.request

import websocket

# O console do Windows nasce em cp1252 e engasga no primeiro acento do relatório.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://dksaxton.github.io/montador_de_itens_lol/"
CHROMES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome",
]
# O Leo abre o app nestas três, nesta ordem de prioridade (20/09/2026). A quarta
# é um piso: notebook comum, conferido mas sem prioridade.
# Celular NÃO é alvo (Leo, 21/09/2026: "não tenho a intenção de fazer para o
# celular") — o app é ferramenta de mesa, e 375px nem entra na conta.
RESOLUCOES = [(2560, 1440), (1920, 1080), (1600, 900), (1280, 800)]

VERDE, VERMELHO, AMARELO, CINZA, FIM = "\033[32m", "\033[31m", "\033[33m", "\033[90m", "\033[0m"


# ---------------------------------------------------------------- resultado
class Placar:
    def __init__(self):
        self.linhas = []

    def conta(self, grupo, nome, ok, detalhe="", pulou=False):
        self.linhas.append((grupo, nome, ok, detalhe, pulou))
        marca = (AMARELO + "–" + FIM) if pulou else ((VERDE + "ok" + FIM) if ok else (VERMELHO + "FALHOU" + FIM))
        print("  %-6s %-44s %s%s%s" % (marca, nome, CINZA, detalhe, FIM))

    @property
    def falhas(self):
        return [l for l in self.linhas if not l[2] and not l[4]]

    def resumo(self):
        passou = sum(1 for l in self.linhas if l[2] and not l[4])
        pulou = sum(1 for l in self.linhas if l[4])
        print("\n" + "=" * 78)
        if self.falhas:
            print("%sFALHOU: %d de %d%s" % (VERMELHO, len(self.falhas), len(self.linhas), FIM))
            for g, n, _, d, _ in self.falhas:
                print("  %s · %s — %s" % (g, n, d))
        else:
            print("%s%d checagens, nenhuma falha%s%s" % (VERDE, passou, (", %d pulada(s)" % pulou) if pulou else "", FIM))
        return 1 if self.falhas else 0


# ---------------------------------------------------------------- servidor
class Servidor:
    """Serve a pasta do projeto numa porta livre, só para o roteiro."""

    def __init__(self):
        import http.server
        s = socket.socket(); s.bind(("127.0.0.1", 0)); self.porta = s.getsockname()[1]; s.close()

        class Mudo(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *a, **k):
                super().__init__(*a, directory=RAIZ, **k)

            def log_message(self, *a, **k):
                pass                      # o relatório é o que importa, não o log

            def handle_one_request(self):
                try:
                    super().handle_one_request()
                except ConnectionError:
                    self.close_connection = True   # o Chrome corta conexão à vontade

        handler = Mudo
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", self.porta), handler)
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.url = "http://127.0.0.1:%d/" % self.porta

    def parar(self):
        self.httpd.shutdown()


# ---------------------------------------------------------------- navegador
class Sessao:
    def __init__(self, url):
        chrome = next((c for c in CHROMES if os.path.exists(c)), None)
        if not chrome:
            sys.exit("Não achei o Chrome. Ajuste CHROMES no topo do arquivo.")
        s = socket.socket(); s.bind(("127.0.0.1", 0)); porta = s.getsockname()[1]; s.close()
        import tempfile
        # perfil próprio: dois Chromes no mesmo user-data-dir e o segundo não sobe
        perfil = tempfile.mkdtemp(prefix="qa-montador-")
        self.proc = subprocess.Popen(
            [chrome, "--headless=new", "--remote-debugging-port=%d" % porta, "--user-data-dir=" + perfil,
             "--window-size=1920,1080", "--no-first-run", "--hide-scrollbars", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        atexit.register(self.fechar)
        alvo = None
        for _ in range(80):
            try:
                alvo = [t for t in json.load(urllib.request.urlopen("http://127.0.0.1:%d/json" % porta))
                        if t["type"] == "page"][0]
                break
            except Exception:
                time.sleep(0.25)
        if not alvo:
            sys.exit("O Chrome não respondeu na porta de depuração.")
        self.ws = websocket.create_connection(alvo["webSocketDebuggerUrl"], suppress_origin=True)
        self.ws.settimeout(90)
        self._id = 0
        self.erros = []
        self.rede = []
        self.dialogos = []
        self.envia("Page.enable"); self.envia("Runtime.enable"); self.envia("Log.enable")
        self.url = url

    def fechar(self):
        try: self.proc.kill()
        except Exception: pass

    def envia(self, metodo, params=None):
        self._id += 1
        self.ws.send(json.dumps({"id": self._id, "method": metodo, "params": params or {}}))
        while True:
            try:
                msg = json.loads(self.ws.recv())
            except websocket.WebSocketTimeoutException:
                # Acontece de verdade: com a lista pública cheia, o renderizador
                # some por mais de um minuto. Vira falha legível, não pilha.
                raise RuntimeError("o navegador parou de responder em %s" % metodo)
            if msg.get("id") == self._id:
                if "error" in msg:
                    raise RuntimeError(msg["error"])
                return msg.get("result", {})
            self._anota(msg)

    def _anota(self, msg):
        if msg.get("method") == "Page.javascriptDialogOpening":
            # Um diálogo nativo (confirm, alert, "sair sem salvar?") trava a
            # página inteira até alguém responder: o roteiro via só "o navegador
            # parou de responder". Agora ele anota qual foi e aceita.
            d = msg["params"]
            self.dialogos.append("%s: %s" % (d.get("type"), (d.get("message") or "")[:80]))
            self._id += 1
            self.ws.send(json.dumps({"id": self._id, "method": "Page.handleJavaScriptDialog",
                                     "params": {"accept": True}}))
            return
        if msg.get("method") == "Runtime.exceptionThrown":
            self.erros.append((msg["params"]["exceptionDetails"].get("text") or "")[:160])
        elif msg.get("method") == "Log.entryAdded":
            e = msg["params"]["entry"]
            if e.get("level") == "error":
                # 404 de arquivo é bug de publicação: o Pages é case-sensitive.
                alvo = e.get("url") or ""
                self.rede.append("%s %s" % (e.get("text", "")[:80], alvo))

    def js(self, expr):
        r = self.envia("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        if "exceptionDetails" in r:
            # "Uncaught" sozinho não diz nada: a mensagem de verdade mora em exception.description
            d = r["exceptionDetails"]
            desc = ((d.get("exception") or {}).get("description") or d.get("text") or "erro no JS").split(chr(10))[0]
            raise RuntimeError(desc + " :: " + expr[:80])
        return r["result"].get("value")

    def abrir(self, caminho=""):
        self.envia("Page.navigate", {"url": self.url + caminho})
        fim = time.time() + 30
        while time.time() < fim:
            try:
                msg = json.loads(self.ws.recv())
            except websocket.WebSocketTimeoutException:
                raise RuntimeError("a página não carregou: %s" % (self.url + caminho)[:90])
            self._anota(msg)
            if msg.get("method") == "Page.loadEventFired":
                return
        raise RuntimeError("a página não terminou de carregar")

    def caixa(self, seletor):
        # Rolar só quando precisa: um scrollIntoView à toa fecha menu ancorado
        # (que escuta scroll de propósito) e o clique seguinte cai no vazio.
        return self.js("""(() => { const e = document.querySelector(%s); if (!e) return null;
          let r = e.getBoundingClientRect();
          if (r.top < 4 || r.bottom > innerHeight - 4 || r.left < 4 || r.right > innerWidth - 4) {
            e.scrollIntoView({block:'center'}); r = e.getBoundingClientRect();
          }
          if (r.width < 1 || r.height < 1) return 'invisivel';
          return [Math.round(r.left + r.width/2), Math.round(r.top + r.height/2)]; })()""" % json.dumps(seletor))

    def hover(self, seletor):
        p = self.caixa(seletor)
        if not isinstance(p, list):
            raise RuntimeError("não achei (ou tem tamanho zero): " + seletor)
        self.envia("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": p[0], "y": p[1]})
        time.sleep(0.25)
        return p

    def clicar(self, seletor, espera=0.4):
        """Clique de verdade. O mouseMoved antes não é enfeite: sem ele, controle
        que só existe no hover tem tamanho zero e o clique cai no vazio."""
        p = self.hover(seletor)
        for tipo in ("mousePressed", "mouseReleased"):
            self.envia("Input.dispatchMouseEvent",
                       {"type": tipo, "x": p[0], "y": p[1], "button": "left", "clickCount": 1})
        time.sleep(espera)

    def tela(self, largura, altura):
        self.envia("Emulation.setDeviceMetricsOverride",
                   {"width": largura, "height": altura, "deviceScaleFactor": 1, "mobile": False})
        time.sleep(0.6)

    def tela_normal(self):
        self.envia("Emulation.clearDeviceMetricsOverride")

    def captura(self, destino, altura=900):
        dados = self.envia("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True,
                           "clip": {"x": 0, "y": 0, "width": 1920, "height": altura, "scale": 1}})["data"]
        with open(destino, "wb") as f:
            f.write(base64.b64decode(dados))

    # ------- atalhos do app
    def entrar(self):
        self.js("document.getElementById('entrar').click(); document.documentElement.style.scrollBehavior='auto'")
        time.sleep(1.8)

    def limpar_memoria(self):
        self.js("localStorage.clear()")
        self.abrir()
        time.sleep(0.8)

    def nova_build(self):
        self.js("switchTab('build'); showBuildScreen('lista')")
        time.sleep(0.5)
        self.js("document.getElementById('new-build').click()")
        time.sleep(1.2)
        self.js("showBuildScreen('forja')")
        time.sleep(0.8)


# ---------------------------------------------------------------- 1. arquivos
def checar_arquivos(p):
    """O que dá para conferir sem abrir o navegador. O Pages é case-sensitive e
    não perdoa nome com uma letra diferente."""
    print("\n%sARQUIVOS%s" % (AMARELO, FIM))
    idx = open(os.path.join(RAIZ, "index.html"), encoding="utf-8").read()

    p.conta("arquivos", ".nojekyll existe", os.path.exists(os.path.join(RAIZ, ".nojekyll")))

    absolutos = re.findall(r'(?:src|href)="(/[^/][^"]*)"', idx)
    p.conta("arquivos", "nenhum caminho absoluto", not absolutos, ", ".join(absolutos[:3]))

    # todo assets/... citado no HTML e no CSS existe, com a mesma caixa de letra
    # Trecho montado em JS (`${...}`) ou com curinga não é arquivo: fica de fora.
    citados = sorted({c for c in re.findall(r'["\'\(](assets/[^"\'\)\s]+)', idx)
                      if "${" not in c and "*" not in c})
    faltando = [c for c in citados if not _existe_exato(c)]
    p.conta("arquivos", "assets citados existem (caixa exata)", not faltando,
            "%d citados; faltam: %s" % (len(citados), ", ".join(faltando[:3]) or "nenhum"))

    # áudio: o mapa vive no index.html e os arquivos na pasta do Leo
    mapa = re.search(r"const SOM_ARQUIVOS = (\{.*?\n\});", idx, re.S)
    if mapa:
        arquivos = sorted({v for lista in json.loads(mapa.group(1)).values() for v in lista})
        sumidos = [a for a in arquivos if not _existe_exato("assets/audio/" + a)]
        p.conta("arquivos", "áudio do mapa existe em assets/audio", not sumidos,
                "%d arquivos; sumiram: %s" % (len(arquivos), ", ".join(sumidos[:3]) or "nenhum"))
    else:
        p.conta("arquivos", "áudio do mapa existe em assets/audio", False, "não achei SOM_ARQUIVOS no index.html")

    # cards de região: o data/regioes.js aponta, a pasta tem de ter
    reg = os.path.join(RAIZ, "data", "regioes.js")
    if os.path.exists(reg):
        corpo = open(reg, encoding="utf-8").read()
        bloco = corpo.split("medidas:", 1)[1].split("variantes:", 1)[0]
        cards = ["assets/regioes/cards/%s.jpg" % n for n in re.findall(r'"([^"]+)":\s*\[', bloco)]
        sumidos = [c for c in cards if not _existe_exato(c)]
        p.conta("arquivos", "cards de região existem", not sumidos,
                "%d cards; sumiram: %s" % (len(cards), ", ".join(sumidos[:2]) or "nenhum"))


def _existe_exato(rel):
    """os.path.exists mente no Windows: 'Assets/X.PNG' passa. Aqui cada pedaço do
    caminho é conferido contra o que a pasta realmente tem."""
    atual = RAIZ
    for pedaco in rel.split("?")[0].split("#")[0].split("/"):
        if not pedaco:
            continue
        try:
            nomes = os.listdir(atual)
        except (NotADirectoryError, FileNotFoundError):
            return False
        if pedaco not in nomes:
            return False
        atual = os.path.join(atual, pedaco)
    return True


# ---------------------------------------------------------------- 2. o app
def checar_fundacao(s, p):
    print("\n%sFUNDAÇÃO%s" % (AMARELO, FIM))
    s.limpar_memoria()
    n = s.js("CATALOG.items.length")
    p.conta("fundação", "225 itens no catálogo", n == 225, "vieram %s" % n)
    # Contadas pela estrutura e conferidas contra o número que o gerador anotou:
    # foi um leitor calado que deixou 4 runas de fora em 18/09/2026.
    r = s.js("""(() => { const n = RUNAS.trilhas.reduce((a, t) =>
        a + t.slots.reduce((b, sl) => b + sl.runas.length, 0), 0);
      return { contadas: n, meta: RUNAS.meta.runas,
               frag: RUNAS.fragmentos.reduce((a, g) => a + g.runas.length, 0),
               metaFrag: RUNAS.meta.fragmentos }; })()""")
    p.conta("fundação", "runas contadas batem com o gerador",
            r["contadas"] == r["meta"] and r["frag"] == r["metaFrag"],
            "%s runas (gerador diz %s), %s fragmentos (diz %s)"
            % (r["contadas"], r["meta"], r["frag"], r["metaFrag"]))
    patch = s.js("CATALOG.meta && CATALOG.meta.patch")
    p.conta("fundação", "o catálogo diz de que patch é", bool(patch), "patch %s" % patch)
    s.entrar()
    p.conta("fundação", "entrar na loja não gera erro", not s.erros, "; ".join(s.erros[:2]))


def checar_catalogo(s, p):
    print("\n%sCATÁLOGO%s" % (AMARELO, FIM))
    n = s.js("document.querySelectorAll('#grid .card').length")
    p.conta("catálogo", "225 cards desenhados", n == 225, "vieram %s" % n)

    s.js("""(() => { const c = document.getElementById('search-input'); c.value = 'doran';
            c.dispatchEvent(new Event('input', {bubbles: true})); })()""")
    time.sleep(0.6)
    achados = s.js("document.querySelectorAll('#grid .card').length")
    p.conta("catálogo", "a busca filtra", 0 < achados < 225, "'doran' → %s itens" % achados)
    s.js("""(() => { const c = document.getElementById('search-input'); c.value = '';
            c.dispatchEvent(new Event('input', {bubbles: true})); })()""")
    time.sleep(0.6)

    s.clicar(".class-tab[data-classe='AD']", 0.8)
    estado = s.js("""(() => { const o = document.getElementById('oficina');
      const e = document.querySelector('.estandarte');
      return { display: getComputedStyle(o).display, faixa: e ? Math.round(e.getBoundingClientRect().width) : 0,
               corpo: [...document.body.classList].filter(c => c.startsWith('nucleo')) }; })()""")
    # A regressão de 18–20/09: a .oficina deixou de ser grid e o estandarte
    # engoliu a largura toda em toda aba de núcleo.
    p.conta("catálogo", "aba de núcleo vira oficina com estandarte",
            estado["display"] == "grid" and estado["faixa"] == 46,
            "display %s, faixa %spx" % (estado["display"], estado["faixa"]))

    s.clicar(".class-tab[data-classe='']", 0.8)
    p.conta("catálogo", "aba Todos volta a ser uma coluna só de grade",
            s.js("getComputedStyle(document.getElementById('oficina')).display") == "block")

    # F13-T9: o Ápice não pode apagar número do item. A Tocha perdia os +80 de PdH
    # (o texto diz "+20% de PdH"), a Couraça Protoplasmática ia de 600 para 241
    # de Vida, e o Elixir da Força somava as duas alternativas de um "ou". E o
    # caminho antigo: o Lacre Sombrio continua indo de 15 para 55 no Ápice.
    # F13-T21: desde o Capítulo 1 de 23/09 o Ápice vem em números (apexNumeric):
    # o total no máximo substitui, o "a mais" soma. A Couraça chega a 841,18 de
    # Vida no nível 13 (a leitura humilde da T9 deixava os 600), a Tocha mantém
    # os +80 e ganha o multiplicador de +20%, e o Atma — o caso que provou que
    # o texto não bastava — chega a 50% de crítico, não 30%.
    ap = s.js("""(() => { const pega = (n) => CATALOG.items.find(i => i.namePt === n);
      const le = (n) => { const it = pega(n); state.applyApex = true;
        const r = effectiveAttributes(it, { itemId: it.slug }).map(a => a.raw); state.applyApex = false; return r; };
      return { tocha: le('Tocha de Chamas Negras'), couraca: le('Couraça Protoplasmática'),
               elixir: le('Elixir da Força'), lacre: le('Lacre Sombrio'), atma: le('Acerto de Contas de Atma') }; })()""")
    p.conta("catálogo", "Ápice não apaga número do item (Tocha +80 e +20%)",
            "+80 de Poder de Habilidade" in ap["tocha"] and "+20% de Poder de Habilidade" in ap["tocha"],
            "Tocha %s" % ap["tocha"][:3])
    p.conta("catálogo", "Ápice usa o total do catálogo (Couraça 841,18; Atma 50%)",
            "+841,18 de Vida" in ap["couraca"] and "+50% de Chance de Acerto Crítico" in ap["atma"],
            "Couraça %s | Atma %s" % (ap["couraca"][:1], [x for x in ap["atma"] if "Crítico" in x]))
    p.conta("catálogo", "Ápice não soma as duas pontas de um \"ou\"", ap["elixir"] == [], str(ap["elixir"]))
    p.conta("catálogo", "Ápice ainda sobe o que é máximo (Lacre 15 → 55)",
            "+55 de Poder de Habilidade" in ap["lacre"], str(ap["lacre"][:1]))

    # F13-T15 (Leo, 23/09: eficiência "com a passiva"): duas regras que valem
    # para o catálogo inteiro. O desconto do Reembolso nunca piora um item — a
    # base antiga derrubava o Limite da Razão de 119% para 91% —, e a caixa com
    # um item só mostra a mesma eficiência da ficha dele, com e sem Reembolso.
    ef = s.js("""(() => { const piora = [], dif = [];
      CATALOG.items.forEach(it => { const val = (on) => { state.applyCashback = on; return [itemEfficiency(it), goldEfficiency([{ itemId: it.slug }]).pct]; };
        const [off, cxOff] = val(false), [on, cxOn] = val(true);
        if (hasCashback(it) && off !== null && on !== null && on < off - 0.05) piora.push(it.namePt);
        if ((off !== null && cxOff !== null && Math.abs(off - cxOff) > 0.06) || (on !== null && cxOn !== null && Math.abs(on - cxOn) > 0.06)) dif.push(it.namePt); });
      state.applyCashback = false; return { piora, dif }; })()""")
    p.conta("catálogo", "o Reembolso nunca piora a eficiência de um item", not ef["piora"],
            ("pioram: " + ", ".join(ef["piora"][:4])) if ef["piora"] else "nenhum dos 225")
    p.conta("catálogo", "caixa de um item só = eficiência da ficha dele", not ef["dif"],
            ("diferem: " + ", ".join(ef["dif"][:4])) if ef["dif"] else "os 225, com e sem Reembolso")
    # F13-T20: o valor em ouro vem pronto do Capítulo 1 (goldValueBase). O
    # contorno da T15 (efficiencyBase × preço) errava por arredondamento em 16
    # itens — o Limite da Razão valia 3.331,72g em vez de 3.331,67g.
    vo = s.js("""(() => { const dif = [], com = [];
      CATALOG.items.forEach(it => { const b = it.costAnalysis && it.costAnalysis.goldValueBase;
        if (typeof b !== 'number') return; com.push(it);
        if (Math.abs(valorEmOuro(it) - b) > 0.001) dif.push(it.namePt + ' ' + valorEmOuro(it).toFixed(2) + '≠' + b); });
      return { n: com.length, dif }; })()""")
    p.conta("catálogo", "valor em ouro = o do catálogo, sem conta por fora", vo["n"] > 200 and not vo["dif"],
            ("diferem: " + "; ".join(vo["dif"][:3])) if vo["dif"] else "%d itens com Valor de Ouro (base)" % vo["n"])
    # F13-T22: o Ápice e o Mestre Forjador mudam o valor em ouro, com os números
    # do catálogo. O Atma no ápice vale 3.866,67g (133,33%); forjado, qualquer
    # Lendário elegível ganha os 1.000g do bônus. E a caixa com um item só
    # continua igual à ficha dele com o Ápice ligado.
    mx = s.js("""(() => { const atma = CATALOG.items.find(i => i.namePt === 'Acerto de Contas de Atma');
      state.applyApex = true; const efAtma = itemEfficiency(atma);
      const dif = [];
      CATALOG.items.forEach(it => { const f = itemEfficiency(it), c = goldEfficiency([{ itemId: it.slug }]).pct;
        if (f !== null && c !== null && Math.abs(f - c) > 0.06) dif.push(it.namePt); });
      state.applyApex = false;
      const alvo = CATALOG.items.find(i => mfEligible(i) && typeof i.costAnalysis.goldValueBase === 'number');
      const antes = build.masterwork; build.masterwork = true;
      const ouro = goldEfficiency([{ itemId: alvo.slug, mf: true }]).gold;
      build.masterwork = antes;
      return { efAtma, dif, alvo: alvo.namePt, ouro, base: alvo.costAnalysis.goldValueBase, bonus: alvo.masterwork.bonusGold }; })()""")
    p.conta("catálogo", "o Ápice muda a eficiência (Atma 133,33%)", abs((mx["efAtma"] or 0) - 133.33) < 0.01,
            "Atma no ápice: %s%%" % mx["efAtma"])
    p.conta("catálogo", "o Mestre Forjador soma o bônus ao item forjado",
            abs(mx["ouro"] - (mx["base"] + (mx["bonus"] or 0))) < 0.01 and (mx["bonus"] or 0) > 0,
            "%s: %sg + %sg = %sg" % (mx["alvo"], mx["base"], mx["bonus"], mx["ouro"]))
    p.conta("catálogo", "caixa de um item só = ficha, também no Ápice", not mx["dif"],
            ("diferem: " + ", ".join(mx["dif"][:4])) if mx["dif"] else "os 225")


def checar_forja(s, p):
    print("\n%sFORJA%s" % (AMARELO, FIM))
    s.nova_build()
    caixas = s.js("build.cats.length")
    p.conta("forja", "nova build nasce com as 8 caixas sugeridas", caixas == 8, "vieram %s" % caixas)

    s.js("build.cats[1].items.push({ itemId: CATALOG.items[0].slug, note: '' }); renderBuildAll()")
    time.sleep(0.5)
    p.conta("forja", "item entra na caixa", s.js("build.cats[1].items.length") == 1)

    # A build nasce em leitura: é o padrão do Leo, "o jogador vê os itens, não os
    # atributos". Os dois lados da regra são conferidos, leitura e edição.
    atributos = """(() => { const t = document.querySelector('.build-totals.show');
      return t ? getComputedStyle(t).display !== 'none' : false; })()"""
    p.conta("forja", "modo leitura esconde os atributos", not s.js(atributos),
            "editando = %s" % s.js("document.body.classList.contains('editando')"))
    s.clicar("#edit-switch", 0.8)
    p.conta("forja", "o Editar liga", s.js("document.body.classList.contains('editando')"))
    p.conta("forja", "e com ele os atributos voltam", s.js(atributos))

    # F13-T3: os dois verbos que estavam escondidos no balão. Como só existem no
    # hover, o mouse passa antes — senão o clique cai num retângulo invisível.
    s.hover(".item-tile")
    p.conta("forja", "os botões do molde aparecem no hover",
            s.js("""(() => { const f = document.querySelector('.item-tile .tile-acoes');
              return !!f && Number(getComputedStyle(f).opacity) > .9
                     && getComputedStyle(f).pointerEvents === 'auto'; })()"""))
    s.clicar(".item-tile .ta-nota", 0.6)
    p.conta("forja", "o ✎ abre a observação",
            s.js("document.getElementById('note-editor').classList.contains('show')"))
    s.js("closeNoteEditor(false)")
    time.sleep(0.4)
    antes = s.js("build.cats[1].items.length")
    s.hover(".item-tile")
    s.clicar(".item-tile .ta-x", 0.6)
    p.conta("forja", "o ✕ tira o item da caixa", s.js("build.cats[1].items.length") == antes - 1,
            "de %s para %s" % (antes, s.js("build.cats[1].items.length")))

    # F13-T7: dois ✕ em 150 ms tiravam o item errado (achado da caçada de bugs).
    # A saída espera a animação; a posição mudava no meio. Pedir A e B tem de
    # deixar o C.
    fim = s.js("""(async () => { const c = build.cats[1]; c.items = [];
      CATALOG.items.filter(i => i.tier === 'Lendário').slice(0, 3).forEach(it => c.items.push({ itemId: it.slug, note: '' }));
      renderBuildAll(); await new Promise(r => setTimeout(r, 400));
      const c3 = c.items[2].itemId;
      removeItemFromCategory(c.id, 0); await new Promise(r => setTimeout(r, 150));
      removeItemFromCategory(c.id, 1); await new Promise(r => setTimeout(r, 900));
      return { sobrou: c.items.map(i => i.itemId), esperado: [c3] }; })()""")
    p.conta("forja", "dois ✕ seguidos tiram os dois pedidos", fim["sobrou"] == fim["esperado"],
            "sobrou %s" % fim["sobrou"])

    # F13-T4: o tipo da caixa deixou de ser um botão que dá a volta olímpica.
    s.clicar(".build-cat:nth-of-type(2) .cat-kind", 0.6)
    menu = s.js("""(() => { const m = document.getElementById('kind-menu');
      if (!m || !m.classList.contains('show')) return null;
      const r = m.getBoundingClientRect();
      return { opcoes: [...m.querySelectorAll('button')].map(b => b.dataset.kind),
               marcado: (m.querySelector('[aria-checked="true"]') || {}).dataset,
               cabe: r.left >= 0 && r.top >= 0 && r.right <= innerWidth + 1 && r.bottom <= innerHeight + 1 }; })()""")
    p.conta("forja", "o tipo da caixa abre um menu com os quatro",
            bool(menu) and menu["opcoes"] == ["comum", "prioridade", "opcional", "escolha"] and menu["cabe"],
            "%s" % (menu or "não abriu"))
    s.clicar('#kind-menu [data-kind="opcional"]', 0.7)
    p.conta("forja", "escolher no menu troca o tipo e fecha",
            s.js("build.cats[1].kind") == "opcional"
            and not s.js("document.getElementById('kind-menu').classList.contains('show')"),
            "ficou %s" % s.js("build.cats[1].kind"))
    s.js("build.cats[1].kind = 'comum'; renderBuild()")


def checar_marcadores(s, p):
    """O bug de 20/09: o diálogo abria, a escolha não gravava. Todo passo aqui é
    clique de verdade, e o × só existe no hover."""
    print("\n%sMARCADORES%s" % (AMARELO, FIM))
    s.js("switchTab('build'); showBuildScreen('forja')")
    time.sleep(0.6)
    s.clicar("#build-marks .mark-slot[data-i='0']")
    p.conta("marcadores", "o diálogo abre", not s.js("document.getElementById('marker-dialog').hidden"))
    s.clicar("#md-tags .md-cell")
    primeiro = s.js("JSON.stringify(build.markers)")
    p.conta("marcadores", "escolher grava na build", s.js("build.markers.length") == 1, primeiro)

    s.clicar("#build-marks .mark-slot[data-i='1']")
    s.clicar("#md-tags .md-cell:nth-child(3)")
    p.conta("marcadores", "o segundo espaço também", s.js("build.markers.length") == 2)

    s.clicar("#build-marks .mark-slot[data-i='0']")
    s.clicar("#md-tags .md-cell:nth-child(5)")
    p.conta("marcadores", "trocar um já preenchido",
            s.js("JSON.stringify(build.markers)") != primeiro and s.js("build.markers.length") == 2)

    s.hover("#build-marks .mark-slot[data-i='1']")
    s.clicar("#build-marks .mark-slot[data-i='1'] .mark-x")
    p.conta("marcadores", "o × tira", s.js("build.markers.length") == 1)


def garantir_build_editavel(s):
    """Runas, habilidades e texto são da build ativa, e a grade de habilidades só
    existe com o Editar ligado. Rodando um grupo sozinho (-k), nada disso existe
    ainda — então o roteiro monta o cenário antes de cobrar."""
    if not s.js("typeof build !== 'undefined' && !!build"):
        s.nova_build()
    else:
        s.js("switchTab('build'); showBuildScreen('forja')")
        time.sleep(0.5)
    if not s.js("document.body.classList.contains('editando')"):
        s.clicar("#edit-switch", 0.8)


def checar_runas(s, p):
    print("\n%sRUNAS%s" % (AMARELO, FIM))
    garantir_build_editavel(s)
    s.js("switchTab('runas')")
    time.sleep(0.8)
    s.js("""(() => { const b = document.querySelector('.runas-modo[data-modo=\"montar\"]');
            if (b) b.click(); })()""")
    time.sleep(0.8)
    # A página só oferece runas depois da trilha primária escolhida, e as da
    # secundária só depois da secundária. Então: trilha, escolhe o que aparecer,
    # secundária, escolhe o que aparecer de novo.
    s.clicar("#runas-trilhas [data-trilha]", 0.6)
    fim = time.time() + 40
    while time.time() < fim:
        # Uma escolha por fileira: toda opção carrega data-escolher, então clicar
        # sempre na primeira "não escolhida" só ficaria trocando a mesma vaga.
        acao = s.js("""(() => {
          for (const sec of document.querySelectorAll('#runas-corpo .runas-slot')) {
            if (sec.querySelector('[data-secundaria]')) {
              if (!sec.querySelector('[data-secundaria].ativa')) {
                sec.querySelector('[data-secundaria]').click();
                return 'secundaria';
              }
              continue;
            }
            if (sec.querySelector('.escolhida')) continue;
            const b = sec.querySelector('[data-escolher]:not(.bloqueada)');
            if (b) { b.click(); return 'runa'; }
          }
          return ''; })()""")
        if not acao:
            break
        time.sleep(0.25)
    cheias = s.js("""(() => { const p = paginaDaBuild();
      return (p.assinatura ? 1 : 0) + p.slots.filter(Boolean).length
           + p.secundarios.filter(Boolean).length + p.fragmentos.filter(Boolean).length; })()""")
    p.conta("runas", "a página fecha em 9 de 9", cheias == 9, "%s de 9" % cheias)
    # F13-T18: o app não aplica as trocas automáticas, só avisa — e a tela diz isso.
    # No Resumido, que é onde as linhas "Vira…" aparecem (em Ícones o card não
    # tem texto, e a legenda some junto de propósito).
    s.js("document.querySelector('.runas-vista[data-vista=resumido]').click(); 'ok'")
    time.sleep(0.4)
    rodape_montar = s.js("""(() => { const r = document.querySelector('#runas-corpo .runas-rodape');
      return !!r && getComputedStyle(r).display !== 'none' && r.textContent.includes('O app só avisa'); })()""")
    p.conta("runas", "a faixa aparece na forja",
            s.js("""(() => { switchTab('build'); showBuildScreen('forja');
              const f = document.querySelector('.build-runas');
              return !!f && !f.hidden && getComputedStyle(f).display !== 'none'; })()"""))
    # F13-T17: o bloco "Controle de grupo válido" do markdown sumia no leitor,
    # calado — a ficha do Golpe Desleal nunca mostrou a lista.
    s.js("switchTab('runas'); 'ok'")
    time.sleep(0.6)
    s.js("""(() => { const b = document.querySelector('.runas-modo[data-modo="ler"]'); if (b) b.click(); })()""")
    time.sleep(0.5)
    s.js("document.querySelector('.runas-vista[data-vista=completo]').click(); 'ok'")
    time.sleep(0.4)
    s.js("""(() => { const t = [...document.querySelectorAll('#runas-trilhas [data-trilha]')]
      .find(b => b.dataset.trilha === 'dominacao'); if (t) t.click(); })()""")
    time.sleep(0.6)
    cg = s.js("""(() => { const a = [...document.querySelectorAll('article.runa')].find(e => e.title === 'Golpe Desleal');
      const c = a && a.querySelector('.cg');
      return { visivel: !!c && getComputedStyle(c).display !== 'none', texto: c ? c.textContent : '' }; })()""")
    p.conta("runas", "a ficha mostra o controle de grupo válido",
            cg["visivel"] and "Inclui" in cg["texto"] and "Cripple" in cg["texto"],
            "Golpe Desleal, modo Completo" if cg["visivel"] else "o bloco não aparece")
    rodape_ler = s.js("""(() => { const r = document.querySelector('#runas-corpo .runas-rodape');
      return !!r && getComputedStyle(r).display !== 'none' && r.textContent.includes('O app só avisa'); })()""")
    p.conta("runas", "a tela diz que as trocas “Vira…” são só aviso", rodape_montar and rodape_ler,
            "no Ler e no Montar" if rodape_montar and rodape_ler
            else "falta no " + " e no ".join(n for n, ok in (("Montar", rodape_montar), ("Ler", rodape_ler)) if not ok))


def checar_fragmento(s, p):
    """F13-T23: o Atributo adicional guarda o fragmento escolhido (entry.frag)."""
    print("\n%sFRAGMENTO DO ATRIBUTO ADICIONAL%s" % (AMARELO, FIM))
    s.nova_build()
    if not s.js("document.body.classList.contains('editando')"):
        s.clicar("#edit-switch", 0.8)
    s.js("""(() => { const c = build.cats[3]; c.items = [{ itemId: 'stat-bonus', note: '' }, { itemId: 'stat-bonus', note: 'segundo' }];
      switchTab('build'); showBuildScreen('forja'); renderBuildAll(); return 'ok'; })()""")
    time.sleep(0.8)
    sel = s.js("'.build-cat[data-cat-id=\"' + build.cats[3].id + '\"] .item-tile'")
    s.clicar(sel + " .item-icon", 0.8)
    n = s.js("document.getElementById('escolher-fragmento').hidden ? 0 : document.querySelectorAll('#fr-lista [data-frag]').length")
    p.conta("fragmento", "clicar no ícone abre a escolha dos fragmentos", n > 30, "%s fragmentos na lista" % n)
    if n:
        s.clicar('#fr-lista [data-frag="Ouro · Vida"]', 0.8)
    s.js("(() => { build.cats[3].items[1].frag = 'Prata · Swiftness'; renderBuildAll(); return 'ok'; })()")
    t = s.js("""(() => { const cx = build.cats[3]; return { f: cx.items.map(e => e.frag || null),
      attrs: sumAttributes(cx.items).map(x => x.stat + '|' + x.unit + '|' + x.value), ouro: goldEfficiency(cx.items).gold }; })()""")
    p.conta("fragmento", "o fragmento entra nos atributos e no ouro",
            t["f"] == ["Ouro · Vida", "Prata · Swiftness"] and "Vida|flat|375" in t["attrs"] and "Velocidade de Ataque|percent|10" in t["attrs"]
            and abs(t["ouro"] - 1650) < 0.01, "%s · %sg" % (t["attrs"], t["ouro"]))
    # Os caminhos que listam os campos da entrada um a um: texto, lote, link e servidor.
    s.js("gravarBuild(); 'ok'")
    v = s.js("""(() => { const quer = JSON.stringify(['Ouro · Vida', 'Prata · Swiftness']);
      const deTexto = (txt) => JSON.stringify(textToBuild(txt).cats.flatMap(c => c.items).filter(e => e.itemId === 'stat-bonus').map(e => e.frag || null));
      const b = library.builds.find(x => x.id === build.id);
      const lk = linkParaBuild('#' + buildParaLink(b).split('#')[1]);
      const sv = caixasDoServidor(caixasParaServidor(build.cats), []);
      const so = (cats) => JSON.stringify(cats.flatMap(c => c.items).filter(e => e.itemId === 'stat-bonus').map(e => e.frag || null));
      return { texto: deTexto(buildToText()) === quer, lote: deTexto(loteParaTexto([build.id]).split(String.fromCharCode(10) + String.fromCharCode(10) + '=====')[0]) === quer,
               link: so(lk.cats) === quer, servidor: so(sv) === quer }; })()""")
    p.conta("fragmento", "o fragmento viaja no texto, no lote, no link e na publicação", all(v.values()),
            ", ".join(k for k, ok in v.items() if not ok) or "os quatro")


def checar_habilidades(s, p):
    print("\n%sHABILIDADES%s" % (AMARELO, FIM))
    garantir_build_editavel(s)
    # O nível 1 já ficou inalcançável uma vez, por causa do rótulo transbordando.
    s.clicar(".bh-cel[data-hab='Q'][data-nivel='1']")
    p.conta("habilidades", "nível 1 aceita clique", (s.js("build.habilidades[0]") or "") == "Q",
            "ficou %r" % s.js("build.habilidades[0]"))
    s.clicar(".bh-cel[data-hab='R'][data-nivel='5']")
    p.conta("habilidades", "supremo recusado no nível 5", (s.js("build.habilidades[4]") or "") != "R")
    s.clicar(".bh-cel[data-hab='R'][data-nivel='6']")
    p.conta("habilidades", "supremo aceito no nível 6", (s.js("build.habilidades[5]") or "") == "R")

    # F13-T8: duplicar perdia runas, habilidades e Mestre Forjador (caçada de bugs).
    antes = s.js("""(() => { build.masterwork = true; gravarBuild();
      return { hab: build.habilidades.map(x => x || '-').join(''), runas: JSON.stringify(build.runas), id: build.id }; })()""")
    s.js("duplicateBuild(build.id)")
    time.sleep(0.6)
    depois = s.js("({ hab: build.habilidades.map(x => x || '-').join(''), runas: JSON.stringify(build.runas), id: build.id, mf: !!build.masterwork })")
    p.conta("habilidades", "duplicar leva habilidades, runas e Mestre Forjador",
            depois["id"] != antes["id"] and depois["hab"] == antes["hab"] and depois["runas"] == antes["runas"] and depois["mf"],
            "habilidades %s" % depois["hab"])


def checar_texto(s, p):
    """Exportar e reimportar tem de devolver a mesma build — é como o Leo move
    build entre máquinas e como uma IA gera build para ele."""
    print("\n%sTEXTO%s" % (AMARELO, FIM))
    # sempre uma build nova, com as 8 caixas: herdar a do grupo anterior fazia o
    # teste depender da ordem (rodando só -k texto, não havia caixa nem item)
    s.nova_build()
    garantir_build_editavel(s)
    # F13-T12: a comparação antiga contava as CHAVES do objeto de runas — sempre
    # 6 — e não via runa sumindo. Agora compara o conteúdo, com a pior página:
    # Slot 1 da primária vazio e fragmento do Slot 1 vazio. Era exatamente aí
    # que a ida e volta perdia runas (a escrita espremia os vazios e a leitura
    # confiava na posição).
    s.js("""(() => { const t = RUNAS.trilhas[0], t2 = RUNAS.trilhas[1];
      const F = RUNAS.fragmentos;
      // itens: texto sem item é recusado pelo importador, e aí não há ida e volta
      if (!build.cats.some(c => c.items.length))
        build.cats[3].items = CATALOG.items.filter(i => i.tier === 'Lendário').slice(0, 3).map(it => ({ itemId: it.slug, note: '' }));
      build.runas = normRunas({ primaria: t.id, assinatura: t.slots[0].runas[0].id,
        slots: ['', t.slots[2].runas[0].id, t.slots[3].runas[0].id],
        secundaria: t2.id, secundarios: [t2.slots[1].runas[0].id, t2.slots[3].runas[0].id],
        fragmentos: ['', F[1].runas[0].id, F[2].runas[0].id] });
      gravarBuild(); return 'ok'; })()""")
    RETRATO = """(() => JSON.stringify({ itens: build.cats.flatMap(c => c.items.map(i => i.itemId)),
      marcadores: build.markers, habilidades: build.habilidades, runas: normRunas(build.runas) }))()"""
    antes = s.js(RETRATO)
    id_antes = s.js("build.id")
    texto = s.js("buildToText()")
    s.js("switchTab('build'); showBuildScreen('lista'); document.getElementById('toggle-io').classList.add('active')")
    time.sleep(0.4)
    s.js("document.getElementById('import-text').value = %s" % json.dumps(texto))
    s.js("document.getElementById('import-btn').click()")
    time.sleep(1.4)
    depois = s.js(RETRATO)
    importou = s.js("build.id") != id_antes
    if not importou:
        det = "a importação NÃO criou build nova: comparar seria comparar a build com ela mesma"
    elif antes == depois:
        det = "itens, marcadores, habilidades e runas iguais"
    else:
        a, d = json.loads(antes), json.loads(depois)
        det = "; ".join("%s: %s → %s" % (k, json.dumps(a[k], ensure_ascii=False)[:90], json.dumps(d[k], ensure_ascii=False)[:90])
                        for k in a if a[k] != d[k])
    p.conta("texto", "exportar e reimportar devolve a mesma build", importou and antes == depois, det)

    # F13-T12: texto exportado ANTES do conserto espremia as vagas vazias, e o
    # formato promete que dá para importar só os fragmentos. Os dois voltavam
    # sem runa nenhuma — e "Vida" era acusada de "não encontrada".
    texto_velho = chr(10).join(["BUILD: t", "[COMUM] Core | 3x1", "- Abatedora",
        "RUNAS: Precisão > Pressione o Ataque | Lenda: Espontaneidade | Golpe de Misericórdia",
        "FRAGMENTOS: Força Adaptativa | Vida"])
    velho = s.js("""(() => { const r = textToBuild(%s);
      const p = normRunas(r.runas); return { slots: p.slots, frag: p.fragmentos, unknown: r.unknown }; })()""" % json.dumps(texto_velho))
    p.conta("texto", "texto antigo (vagas espremidas) e só fragmentos voltam inteiros",
            velho["slots"][1:] == ["lenda-espontaneidade", "golpe-de-misericordia"] and "vida" in velho["frag"] and not velho["unknown"],
            "slots %s, fragmentos %s, não encontrei %s" % (velho["slots"], velho["frag"], velho["unknown"]))

    # F13-T13: o LINK da build é o outro jeito de mandá-la para alguém, e ele
    # não levava runas, habilidades, layout nem Mestre Forjador — mas a placa
    # promete "quem abrir recebe esta build". Aqui o link é aberto numa página
    # nova, como quem recebe, e comparado campo a campo.
    CAMPOS = """(() => JSON.stringify({ itens: build.cats.flatMap(c => c.items.map(i => [i.itemId, i.note || '', !!i.mf])),
      runas: normRunas(build.runas), habilidades: normHabilidades(build.habilidades),
      layout: layoutValido(build.layout), mestre: !!build.masterwork, modo: build.mode || '', desc: build.desc || '',
      marcadores: build.markers }))()"""
    s.js("""(() => { const t = RUNAS.trilhas[2];
      build.runas = normRunas({ primaria: t.id, assinatura: t.slots[0].runas[1].id, slots: [t.slots[1].runas[0].id, '', t.slots[3].runas[1].id],
        fragmentos: [RUNAS.fragmentos[0].runas[1].id, '', RUNAS.fragmentos[2].runas[0].id] });
      build.habilidades = normHabilidades(['Q','E','W','Q','Q','R','Q','E','Q','E','R','E','E','W','W','R','W','W']);
      build.layout = Object.keys(LAYOUTS).find(k => k !== 'tabuleiro');
      build.masterwork = true; build.desc = 'descrição do link';
      const c = build.cats.find(c => c.items.length); if (c) { c.items[0].note = 'observação'; c.items[0].mf = true; }
      gravarBuild(); return 'ok'; })()""")
    enviado = s.js(CAMPOS)
    link = s.js("buildParaLink(library.builds.find(b => b.id === build.id))")
    # página NOVA: trocar só o "#" não recarrega o documento, e aí ninguém "recebe"
    s.abrir("?link=1#" + link.split("#", 1)[1])
    time.sleep(1.2)
    s.entrar()
    recebido = s.js(CAMPOS)
    veio_do_link = s.js("build.id.startsWith('l-')")
    if not veio_do_link:
        det = "a build ativa não é a recebida pelo link (id %s)" % s.js("build.id")
    elif enviado == recebido:
        det = "runas, habilidades, layout, Mestre Forjador, itens e observações; link de %d caracteres" % len(link)
    else:
        a, b = json.loads(enviado), json.loads(recebido)
        det = "; ".join("%s: %s → %s" % (k, json.dumps(a[k], ensure_ascii=False)[:60], json.dumps(b[k], ensure_ascii=False)[:60]) for k in a if a[k] != b[k])
    p.conta("texto", "o link leva a build inteira (quem abre recebe tudo)", veio_do_link and enviado == recebido, det)

    # F13-T8: importar tem de CRIAR uma build nova (senão a comparação acima
    # passa sem testar nada) e ela tem de nascer GRAVADA — com Mestre Forjador e
    # campeão, o importador deixava rascunho, e recarregar perdia os dois.
    s.js("""(async () => { await Campeoes.carregar(); build.champion = Campeoes.porNome('Jinx');
      build.masterwork = true; gravarBuild(); return 'ok'; })()""")
    id_origem = s.js("build.id")
    texto = s.js("buildToText()")
    s.js("document.getElementById('import-text').value = %s" % json.dumps(texto))
    s.js("document.getElementById('import-btn').click()")
    time.sleep(2.5)                       # o campeão chega pelo Data Dragon, depois
    r = s.js("""(() => { const salva = library.builds.find(b => b.id === build.id) || {};
      return { nova: build.id !== %s, sujo: rascunho.sujo,
               mfSalvo: !!salva.masterwork, campeaoSalvo: salva.champion ? salva.champion.name : null }; })()""" % json.dumps(id_origem))
    p.conta("texto", "importar cria uma build nova", r["nova"])
    p.conta("texto", "a build importada nasce gravada (Mestre Forjador e campeão)",
            r["nova"] and not r["sujo"] and r["mfSalvo"] and r["campeaoSalvo"] == "Jinx",
            "rascunho sujo=%s, MF gravado=%s, campeão gravado=%s" % (r["sujo"], r["mfSalvo"], r["campeaoSalvo"]))


def checar_exclusao(s, p):
    """F13-T14: excluir uma build publicada prometia "ela também sai do site" e,
    se o servidor falhasse, apagava daqui calada — a publicação ficava no ar e o
    ID dela sumia. O servidor é SIMULADO: o pedido apagar_build nunca sai deste
    navegador, e o confirm é respondido pelo roteiro."""
    print(chr(10) + "%sEXCLUSÃO%s" % (AMARELO, FIM))
    s.js("""(() => { window.__fetchOrig = window.fetch; window.__confirmOrig = window.confirm;
      window.fetch = function (u, ...a) {
        if (String(u).includes('apagar_build')) return Promise.reject(new TypeError('Failed to fetch'));
        return window.__fetchOrig.call(this, u, ...a); };
      window.__confirms = []; window.__respostas = [true, false];   // sim ao Excluir; não a "apagar só daqui"
      window.confirm = (m) => { window.__confirms.push(m); return window.__respostas.length ? window.__respostas.shift() : false; };
      return 'ok'; })()""")
    s.nova_build()
    bid = s.js("""(() => { build.name = 'Publicada de teste'; build.pubId = 'qa0000';
      build.cats[3].items = CATALOG.items.slice(0, 2).map(i => ({ itemId: i.slug, note: '' })); gravarBuild(); return build.id; })()""")
    s.nova_build()
    s.js("switchTab('build'); showBuildScreen('lista'); biSelected = %s; renderBuildIndex(); 'ok'" % json.dumps(bid))
    time.sleep(0.5)
    s.js("""(() => { const b = [...document.querySelectorAll('[data-act="del"]')][0]; if (b) b.click(); return !!b; })()""")
    time.sleep(1.0)
    r = s.js("""(() => ({ ficou: library.builds.some(b => b.id === %s),
      pub: (library.builds.find(b => b.id === %s) || {}).pubId || null, perguntas: window.__confirms }))()""" % (json.dumps(bid), json.dumps(bid)))
    p.conta("exclusão", "servidor fora do ar: a publicada não some calada",
            len(r["perguntas"]) == 2 and "continua no site" in r["perguntas"][1],
            (r["perguntas"][1][:70] if len(r["perguntas"]) > 1 else "só %d pergunta(s)" % len(r["perguntas"])))
    p.conta("exclusão", "dizendo não, a build fica, com o ID guardado", r["ficou"] and r["pub"] == "qa0000")
    s.js("window.fetch = window.__fetchOrig; window.confirm = window.__confirmOrig; 'ok'")


def checar_acessibilidade(s, p):
    print("\n%sACESSIBILIDADE%s" % (AMARELO, FIM))
    s.js("switchTab('catalog')")
    time.sleep(0.5)
    s.clicar("#acess-btn")
    for chave in ("movimento", "brilho", "leitura", "daltonismo"):
        s.clicar("#ac-" + chave, 0.25)
    ligadas = s.js("[...document.body.classList].filter(c => c.startsWith('ac-')).length")
    p.conta("acessibilidade", "os quatro interruptores ligam", ligadas == 4, "%s de 4" % ligadas)
    p.conta("acessibilidade", "menos movimento zera as transições",
            s.js("""(() => { const c = document.querySelector('.card-surface');
              return !c || /^0s/.test(getComputedStyle(c).transitionDuration); })()"""))
    # F13-T10: cada interruptor cumpre o que o próprio rótulo promete.
    s.nova_build()
    s.js("build.cats[1].items = CATALOG.items.slice(0, 2).map(it => ({ itemId: it.slug, note: '' })); renderBuildAll(); 'ok'")
    time.sleep(0.4)
    tam = s.js("""(() => { const t = document.querySelector('.item-tile .tile-name');
      return t ? parseFloat(getComputedStyle(t).fontSize) : 0; })()""")
    p.conta("acessibilidade", "leitura calma aumenta o nome no molde da forja", tam >= 12, "%spx" % tam)
    s.js("""(() => { window.__choveu = false; const o = new MutationObserver(() => {
        if (document.querySelector('.chovendo')) window.__choveu = true; });
      o.observe(document.body, { subtree: true, attributes: true, attributeFilter: ['class'] });
      switchTab('catalog'); switchTab('build'); showBuildScreen('lista'); return 'ok'; })()""")
    time.sleep(1.2)
    p.conta("acessibilidade", "menos movimento para a chuva de entrada", not s.js("window.__choveu"))
    s.js("switchTab('build'); showBuildScreen('forja'); 'ok'")
    time.sleep(0.5)
    brilho = s.js(r"""(() => {
      const quente = (x) => { const m = x.match(/rgba?\((\d+), (\d+), (\d+)/); if (!m) return false;
        const [r, g, b] = m.slice(1).map(Number); return r > 200 && g > 60 && g < 200 && b < 90; };
      let n = 0;
      document.querySelectorAll('body *').forEach(e => { const r = e.getBoundingClientRect(); if (r.width < 1) return;
        const bs = getComputedStyle(e).boxShadow; if (!bs || bs === 'none') return;
        if (bs.split(/,(?![^(]*\))/).some(x => !/inset/.test(x) && quente(x) && !/0px 0px 0px/.test(x.replace(/rgba?\([^)]*\)/, '')))) n++; });
      return { halos: n, brasa: /255, 110, 30/.test(getComputedStyle(document.body).backgroundImage) }; })()""")
    p.conta("acessibilidade", "menos brilho apaga a brasa e os halos da forja",
            brilho["halos"] == 0 and not brilho["brasa"], "%s halo(s), brasa=%s" % (brilho["halos"], brilho["brasa"]))
    s.abrir()
    time.sleep(1.0)
    s.entrar()
    p.conta("acessibilidade", "os ajustes sobrevivem ao recarregar",
            s.js("[...document.body.classList].filter(c => c.startsWith('ac-')).length") == 4)
    s.js("localStorage.removeItem('acessibilidade')")


def checar_publicas(s, p, online):
    print("\n%sBUILDS PUBLICADAS%s" % (AMARELO, FIM))
    if not online:
        p.conta("públicas", "a lista vem do servidor", True, "pulada (--offline)", pulou=True)
        return
    s.js("switchTab('build'); showBuildScreen('lista')")
    time.sleep(0.6)
    # F13-T2: contar os redesenhos. Eram ~80 em 4 segundos, com a página morta —
    # cada marcador de habilidade pedia a lista inteira de volta.
    s.js("""(() => { window.__redesenhos = 0; const f = window.renderBuildIndex;
      window.renderBuildIndex = function (...a) { window.__redesenhos++; return f.apply(this, a); };
      return 'ok'; })()""")
    s.js("""document.querySelector('.bi-tab[data-view=\"publicas\"]').click()""")
    # A lista vem do Supabase e traz o retrato de cada campeão do Data Dragon:
    # depende de rede, então espera até aparecer em vez de cronometrar no chute.
    estado = {"linhas": 0, "texto": ""}
    fim = time.time() + 30
    while time.time() < fim:
        try:
            estado = s.js("""(() => { const l = document.getElementById('bi-rows');
              return { linhas: l.querySelectorAll('.bi-row').length,
                       texto: l.innerText.replace(/\\s+/g, ' ').slice(0, 90) }; })()""")
        except RuntimeError as e:
            estado = {"linhas": 0, "texto": str(e)[:90]}
        if estado["linhas"]:
            break
        time.sleep(2)
    # Foi exatamente isto que ficou quebrado em 20/09: a view caiu inteira porque
    # faltava o grant das colunas novas, e a lista veio vazia com um aviso.
    p.conta("públicas", "a lista vem do servidor", estado["linhas"] > 0,
            "%d builds — %s" % (estado["linhas"], estado["texto"]))
    p.conta("públicas", "nenhum 'permission denied'", "permission denied" not in estado["texto"].lower())

    time.sleep(3)
    try:
        n = s.js("window.__redesenhos")
        vivo = s.js("document.querySelectorAll('#bi-rows .bi-row').length") > 0
    except RuntimeError as e:
        n, vivo = -1, False
    # O número varia com a rede: é um redesenho por quadro em que chega a lista
    # de habilidades de algum campeão, então 6 com cache quente e 15 com cache
    # frio, nas mesmas 42 builds. O que se pega aqui é a disparada — eram ~80 e
    # subindo até a página morrer —, não um valor exato.
    p.conta("públicas", "sem tempestade de redesenho", 0 <= n <= 30 and vivo,
            "%s redesenhos; página %s" % (n if n >= 0 else "?", "viva" if vivo else "MUDA"))
    # a arte das habilidades ainda tem de chegar: a letra vira ícone sozinha
    try:
        arte = s.js("""(() => ({ letras: document.querySelectorAll('#bi-rows .mk-letra').length,
          icones: document.querySelectorAll('#bi-rows .mk-hab:not(.mk-letra)').length }))()""")
        p.conta("públicas", "a arte da habilidade chega no marcador",
                arte["letras"] == 0, "%s letras, %s ícones" % (arte["letras"], arte["icones"]))
    except RuntimeError as e:
        p.conta("públicas", "a arte da habilidade chega no marcador", False, str(e)[:80])

    # F13-T6: os dois laços de pedidos ao Supabase achados pela caçada de bugs
    # (117 e 126 pedidos em 5 s). Conta os pedidos que o app faz sozinho,
    # parado, depois de uma ação só.
    s.js("""(() => { window.__pedidos = 0; if (!window.__fetchEspiado) { const f = window.fetch;
      window.fetch = function (u, ...a) { if (String(u).includes('supabase')) window.__pedidos++;
        return f.call(this, u, ...a); }; window.__fetchEspiado = true; } return 'ok'; })()""")
    s.js("""(() => { const c = document.getElementById('bi-search'); c.value = 'cabeca';
      c.dispatchEvent(new Event('input', { bubbles: true })); return 'ok'; })()""")
    time.sleep(4)
    n = s.js("window.__pedidos")
    p.conta("públicas", "busca por ID que não existe não vira laço", n <= 1, "%s pedido(s) em 4 s" % n)
    s.js("""(() => { const c = document.getElementById('bi-search'); c.value = '';
      c.dispatchEvent(new Event('input', { bubbles: true })); return 'ok'; })()""")

    s.js("localStorage.setItem('publicacao.favoritos', JSON.stringify(['ffffff'])); window.__pedidos = 0; 'ok'")
    s.js("""document.querySelector('.bi-tab[data-view="minhas"]').click(); 'ok'""")
    time.sleep(4)
    n = s.js("window.__pedidos")
    p.conta("públicas", "favorita apagada do site não vira laço", n <= 1,
            "%s pedido(s) em 4 s; favoritos agora: %s" % (n, s.js("favoritosIds()")))


def checar_resolucoes(s, p):
    print("\n%sRESOLUCOES (1440, depois 1080, depois 900)%s" % (AMARELO, FIM))
    s.js("switchTab('catalog')")
    time.sleep(0.5)
    fora_js = """(() => {
      const mau = [];
      document.querySelectorAll('.card, .build-cat, .runa, .trilha-btn, .bh-grade, .oficina, .top-inner')
        .forEach(el => { const r = el.getBoundingClientRect();
          if (r.width > 0 && (r.right > innerWidth + 1 || r.left < -1))
            mau.push(el.className.split(' ')[0]); });
      return { rolagem: document.documentElement.scrollWidth > innerWidth + 1,
               fora: [...new Set(mau)].slice(0, 4) }; })()"""
    # Até 22/09 só o catálogo era medido, e a forja em 1280 rolava de lado sem
    # ninguém ver. Agora as três telas, em cada resolução — e com a PIOR build
    # que o catálogo permite, escolhida pelos dados: o item com o atributo mais
    # longo (o Biscoito, 255 caracteres, estourava a faixa da build em 1280) e o
    # de nome mais longo, mais alguns para encher as fileiras. Medir com uma
    # build comportada é o jeito de não achar nada. E no pior ESTADO também: a
    # faixa de atributos só aparece com o Editar ligado (F12), e a primeira
    # versão desta checagem media em modo leitura — passou com o bug lá dentro.
    s.nova_build()
    if not s.js("document.body.classList.contains('editando')"):
        s.clicar("#edit-switch", 0.8)
    pior = s.js("""(() => {
      const maiorAttr = (it) => Math.max(0, ...(it.attributes || []).map(a => (a.stat || '').length));
      const porAttr = CATALOG.items.slice().sort((a, b) => maiorAttr(b) - maiorAttr(a))[0];
      const porNome = CATALOG.items.slice().sort((a, b) => b.namePt.length - a.namePt.length)[0];
      const lend = CATALOG.items.filter(i => i.tier === 'Lendário').slice(0, 5);
      const c = build.cats[3];
      c.items = [porAttr, porNome, ...lend].map(it => ({ itemId: it.slug, note: 'observação de teste' }));
      renderBuildAll();
      return porAttr === porNome ? porAttr.namePt : porAttr.namePt + ' / ' + porNome.namePt; })()""")
    # Runas no pior modo também: o Completo (etiquetas, notas, controle de grupo
    # abertos), em cada trilha. Até a F13-T17 elas eram medidas em Ícones, e a
    # etiqueta que estourava o card com a Leitura calma ficava escondida.
    trilhas = s.js("RUNAS.trilhas.map(t => t.id)")
    # E com a Leitura calma ligada, que é o texto maior que o app tem: medir com
    # ela depender de um grupo anterior tê-la deixado ligada é medir por sorte.
    tinha_leitura = s.js("document.body.classList.contains('ac-leitura')")
    s.js("document.body.classList.add('ac-leitura'); 'ok'")
    for largura, altura in RESOLUCOES:
        s.tela(largura, altura)
        ruins = []
        for tela, cmd in (("catálogo", "switchTab('catalog')"), ("forja", "switchTab('build'); showBuildScreen('forja')"),
                          ("runas", "switchTab('runas')")):
            s.js(cmd + "; 'ok'")
            time.sleep(0.4)
            passos = [None]
            if tela == "runas":
                s.js("""(() => { const b = document.querySelector('.runas-modo[data-modo="ler"]'); if (b) b.click();
                  document.querySelector('.runas-vista[data-vista=completo]').click(); })()""")
                passos = trilhas
            for t in passos:
                if t:
                    s.js("""(() => { const b = [...document.querySelectorAll('#runas-trilhas [data-trilha]')]
                      .find(x => x.dataset.trilha === %s); if (b) b.click(); })()""" % json.dumps(t))
                    time.sleep(0.3)
                r = s.js(fora_js)
                if r["rolagem"] or r["fora"]:
                    ruins.append("%s%s (%s)" % (tela, " / " + t if t else "", ", ".join(r["fora"]) or "rolagem"))
                    break
        p.conta("resoluções", "%dx%d sem nada fora da tela" % (largura, altura), not ruins,
                ("catálogo, forja e runas (Completo, cinco trilhas), com Leitura calma e " + pior) if not ruins else "; ".join(ruins))
    if not tinha_leitura:
        s.js("document.body.classList.remove('ac-leitura'); 'ok'")
    s.js("switchTab('catalog'); 'ok'")
    s.tela_normal()


def checar_console(s, p):
    print("\n%sCONSOLE%s" % (AMARELO, FIM))
    p.conta("console", "nenhuma exceção durante o roteiro", not s.erros, "; ".join(s.erros[:3]))
    if s.dialogos:
        print("  %sdiálogos nativos que apareceram e foram aceitos: %s%s" % (CINZA, "; ".join(s.dialogos[:4]), FIM))
    # 404 de arquivo é o bug clássico do Pages: nome com outra caixa de letra.
    # o favicon.ico não existe de propósito: o 404 dele não é arquivo perdido
    quatro04 = [r for r in s.rede if "404" in r and "favicon" not in r]
    p.conta("console", "nenhum arquivo faltando (404)", not quatro04, "; ".join(quatro04[:3]))


# ---------------------------------------------------------------- principal
GRUPOS = [
    ("catálogo", checar_catalogo),
    ("forja", checar_forja),
    ("marcadores", checar_marcadores),
    ("runas", checar_runas),
    ("habilidades", checar_habilidades),
    ("texto", checar_texto),
    ("fragmento", checar_fragmento),
    ("exclusão", checar_exclusao),
    ("acessibilidade", checar_acessibilidade),
    ("resoluções", checar_resolucoes),
    # Por último de propósito: com as 38 builds publicadas na tela, o navegador
    # fica pesado, e daí em diante qualquer medida sai contaminada.
    ("públicas", checar_publicas),
]


def main():
    ap = argparse.ArgumentParser(description="Roteiro de QA do Montador de Itens")
    ap.add_argument("--site", action="store_true", help="roda contra o GitHub Pages em vez desta pasta")
    ap.add_argument("--offline", action="store_true", help="pula o que precisa do servidor das builds")
    ap.add_argument("-k", metavar="PALAVRA", help="só os grupos cujo nome contém a palavra")
    ap.add_argument("--captura", metavar="ARQUIVO", help="salva uma captura do catálogo no fim")
    args = ap.parse_args()

    p = Placar()
    servidor = None
    if args.site:
        url = SITE
        print("Alvo: %s%s%s" % (CINZA, url, FIM))
    else:
        servidor = Servidor()
        url = servidor.url
        print("Alvo: %sesta pasta, servida em %s%s" % (CINZA, url, FIM))
        checar_arquivos(p)

    s = Sessao(url)
    try:
        s.abrir()
        checar_fundacao(s, p)
        for nome, fn in GRUPOS:
            if args.k and args.k.lower() not in nome.lower():
                continue
            # Grupo que estoura vira falha dele, não fim do roteiro: eu quero o
            # relatório inteiro, não o primeiro tropeço.
            try:
                if nome == "públicas":
                    fn(s, p, not args.offline)
                else:
                    fn(s, p)
            except Exception as e:
                p.conta(nome, "o grupo rodou até o fim", False,
                        "%s: %s" % (type(e).__name__, str(e)[:110]))
        checar_console(s, p)
        if args.captura:
            # A captura é cortesia: se o navegador já estiver ruim, não é ela que
            # vai decidir se o roteiro passou.
            try:
                s.js("switchTab('catalog')")
                time.sleep(0.8)
                s.captura(args.captura)
                print("\ncaptura em %s" % args.captura)
            except Exception as e:
                print("\nsem captura: %s" % str(e)[:80])
    finally:
        s.fechar()
        if servidor:
            servidor.parar()
    sys.exit(p.resumo())


if __name__ == "__main__":
    main()
