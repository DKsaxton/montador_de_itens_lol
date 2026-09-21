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
# O Leo abre o app nestas três, nesta ordem de prioridade (20/09/2026).
RESOLUCOES = [(2560, 1440), (1920, 1080), (1600, 900)]

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
            raise RuntimeError(r["exceptionDetails"].get("text", "erro no JS") + " :: " + expr[:80])
        return r["result"].get("value")

    def abrir(self, caminho=""):
        self.envia("Page.navigate", {"url": self.url + caminho})
        fim = time.time() + 30
        while time.time() < fim:
            msg = json.loads(self.ws.recv())
            self._anota(msg)
            if msg.get("method") == "Page.loadEventFired":
                return
        raise RuntimeError("a página não terminou de carregar")

    def caixa(self, seletor):
        return self.js("""(() => { const e = document.querySelector(%s); if (!e) return null;
          e.scrollIntoView({block:'center'}); const r = e.getBoundingClientRect();
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
    p.conta("runas", "a faixa aparece na forja",
            s.js("""(() => { switchTab('build'); showBuildScreen('forja');
              const f = document.querySelector('.build-runas');
              return !!f && !f.hidden && getComputedStyle(f).display !== 'none'; })()"""))


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


def checar_texto(s, p):
    """Exportar e reimportar tem de devolver a mesma build — é como o Leo move
    build entre máquinas e como uma IA gera build para ele."""
    print("\n%sTEXTO%s" % (AMARELO, FIM))
    garantir_build_editavel(s)
    antes = s.js("""(() => { const d = { itens: build.cats.flatMap(c => c.items.map(i => i.itemId)),
      marcadores: build.markers.length, habilidades: (build.habilidades || []).filter(Boolean).length,
      runas: Object.keys(build.runas || {}).length };
      return JSON.stringify(d); })()""")
    texto = s.js("buildToText()")
    s.js("switchTab('build'); showBuildScreen('lista'); document.getElementById('toggle-io').classList.add('active')")
    time.sleep(0.4)
    s.js("document.getElementById('import-text').value = %s" % json.dumps(texto))
    s.js("document.getElementById('import-btn').click()")
    time.sleep(1.4)
    depois = s.js("""(() => { const d = { itens: build.cats.flatMap(c => c.items.map(i => i.itemId)),
      marcadores: build.markers.length, habilidades: (build.habilidades || []).filter(Boolean).length,
      runas: Object.keys(build.runas || {}).length };
      return JSON.stringify(d); })()""")
    p.conta("texto", "exportar e reimportar devolve a mesma build", antes == depois,
            "antes %s / depois %s" % (antes, depois))


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
    p.conta("públicas", "sem tempestade de redesenho", 0 <= n <= 12 and vivo,
            "%s redesenhos; página %s" % (n if n >= 0 else "?", "viva" if vivo else "MUDA"))
    # a arte das habilidades ainda tem de chegar: a letra vira ícone sozinha
    try:
        arte = s.js("""(() => ({ letras: document.querySelectorAll('#bi-rows .mk-letra').length,
          icones: document.querySelectorAll('#bi-rows .mk-hab:not(.mk-letra)').length }))()""")
        p.conta("públicas", "a arte da habilidade chega no marcador",
                arte["letras"] == 0, "%s letras, %s ícones" % (arte["letras"], arte["icones"]))
    except RuntimeError as e:
        p.conta("públicas", "a arte da habilidade chega no marcador", False, str(e)[:80])


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
    for largura, altura in RESOLUCOES:
        s.tela(largura, altura)
        r = s.js(fora_js)
        p.conta("resoluções", "%dx%d sem nada fora da tela" % (largura, altura),
                not r["rolagem"] and not r["fora"],
                "rolagem %s, fora: %s" % (r["rolagem"], ", ".join(r["fora"]) or "nada"))
    s.tela_normal()


def checar_console(s, p):
    print("\n%sCONSOLE%s" % (AMARELO, FIM))
    p.conta("console", "nenhuma exceção durante o roteiro", not s.erros, "; ".join(s.erros[:3]))
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
