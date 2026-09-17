"""Baixa os brasões oficiais das regiões (Data Dragon do Legends of Runeterra, da própria Riot)
e tira a paleta de cada um lendo o PNG na mão — sem biblioteca de imagem."""
import io, os, json, zlib, struct, urllib.request, collections

RAIZ = r"C:\Users\user\3D Objects\Captulo 2\montador_de_itens_lol"
DEST = os.path.join(RAIZ, 'assets', 'regioes')
os.makedirs(DEST, exist_ok=True)

BASE = "https://dd.b.pvp.net/latest/core/en_us/img/regions/"

# nome no catálogo do Capítulo 1 → arquivo do brasão na Riot
REGIOES = {
    'Runeterra':     'icon-runeterra.png',
    'Ionia':         'icon-ionia.png',
    'Freljord':      'icon-freljord.png',
    'Noxus':         'icon-noxus.png',
    'Demacia':       'icon-demacia.png',
    'Targon':        'icon-targon.png',
    'Bilgewater':    'icon-bilgewater.png',
    'Shadow Isles':  'icon-shadowisles.png',
    'Piltover':      'icon-piltoverzaun.png',   # a Riot publica Piltover e Zaun num brasão só
    'Zaun':          'icon-piltoverzaun.png',
    'Shurima':       'icon-shurima.png',
    'Bandle City':   'icon-bandlecity.png',
    # 'The Void': a Riot não publica brasão da Vazio nestes endpoints abertos
}

SLUG = {
    'Runeterra': 'runeterra', 'Ionia': 'ionia', 'Freljord': 'freljord', 'Noxus': 'noxus',
    'Demacia': 'demacia', 'Targon': 'targon', 'Bilgewater': 'bilgewater',
    'Shadow Isles': 'shadow-isles', 'Piltover': 'piltover-zaun', 'Zaun': 'piltover-zaun',
    'Shurima': 'shurima', 'Bandle City': 'bandle-city',
}


# ---------------------------------------------------------------- PNG na mão
def le_png(dados):
    """Devolve (largura, altura, lista de pixels RGBA). Só o necessário: 8 bits, cor 6 ou 2."""
    assert dados[:8] == b'\x89PNG\r\n\x1a\n', 'não é PNG'
    i, idat, larg, alt, cor, bits = 8, b'', 0, 0, 0, 0
    while i < len(dados):
        n = struct.unpack('>I', dados[i:i + 4])[0]
        tipo = dados[i + 4:i + 8]
        corpo = dados[i + 8:i + 8 + n]
        if tipo == b'IHDR':
            larg, alt, bits, cor = struct.unpack('>IIBB', corpo[:10])
        elif tipo == b'IDAT':
            idat += corpo
        elif tipo == b'IEND':
            break
        i += 12 + n
    assert bits == 8 and cor in (2, 6), f'formato não suportado: bits={bits} cor={cor}'
    canais = 4 if cor == 6 else 3
    bruto = zlib.decompress(idat)
    linha_bytes = larg * canais
    saida, ant = [], bytearray(linha_bytes)
    p = 0
    for _ in range(alt):
        filtro = bruto[p]; p += 1
        linha = bytearray(bruto[p:p + linha_bytes]); p += linha_bytes
        for x in range(linha_bytes):
            a = linha[x - canais] if x >= canais else 0
            b = ant[x]
            c = ant[x - canais] if x >= canais else 0
            if filtro == 1: linha[x] = (linha[x] + a) & 255
            elif filtro == 2: linha[x] = (linha[x] + b) & 255
            elif filtro == 3: linha[x] = (linha[x] + (a + b) // 2) & 255
            elif filtro == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                linha[x] = (linha[x] + pr) & 255
        saida.append(bytes(linha))
        ant = linha
    return larg, alt, canais, saida


def paleta(caminho, quantos=5):
    """Cores dominantes do brasão, ignorando o transparente e o quase-preto do fundo."""
    larg, alt, canais, linhas = le_png(open(caminho, 'rb').read())
    conta = collections.Counter()
    for linha in linhas:
        for x in range(larg):
            o = x * canais
            r, g, b = linha[o], linha[o + 1], linha[o + 2]
            a = linha[o + 3] if canais == 4 else 255
            if a < 140:
                continue
            if r + g + b < 60:      # preto de contorno
                continue
            # arredonda para juntar tons vizinhos
            conta[(r // 24 * 24, g // 24 * 24, b // 24 * 24)] += 1
    total = sum(conta.values()) or 1
    return [('#%02x%02x%02x' % c, round(n * 100 / total, 1)) for c, n in conta.most_common(quantos)]


if __name__ == '__main__':
    vistos, relatorio = {}, {}
    for nome, arq in REGIOES.items():
        destino = os.path.join(DEST, SLUG[nome] + '.png')
        if not os.path.exists(destino):
            req = urllib.request.Request(BASE + arq, headers={'User-Agent': 'montador-de-itens'})
            with urllib.request.urlopen(req, timeout=30) as r:
                open(destino, 'wb').write(r.read())
        if SLUG[nome] not in vistos:
            vistos[SLUG[nome]] = paleta(destino)
        relatorio[nome] = {'arquivo': 'assets/regioes/' + SLUG[nome] + '.png',
                           'fonte': BASE + arq,
                           'paleta': vistos[SLUG[nome]]}
        print(f"{nome:14s} {os.path.getsize(destino):6d} bytes  " +
              ' '.join(c for c, _ in vistos[SLUG[nome]]))
    io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'paletas.json'), 'w', encoding='utf-8').write(
        json.dumps(relatorio, ensure_ascii=False, indent=1))
    print('\nbrasões em', DEST)
