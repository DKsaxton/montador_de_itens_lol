# Corta as texturas para a proporcao do card (5:3), reduz para 800x480 e grava JPG.
#
# Mede o brilho da faixa onde o texto do item vai (terco central-esquerdo). Duas coisas
# saem dessa medida, nenhuma escolhida no olho:
#   1. imagens escuras demais levam uma gama que levanta o meio-tom ate o material
#      aparecer (alvo 88) Ã¢â‚¬â€ sem isso os canos de Zaun e as tabuas de Bilgewater viram mancha;
#   2. abaixo de 110 o card pede tinta clara; acima, tinta escura.
Add-Type -AssemblyName System.Drawing

# Caminhos relativos a raiz do repositorio.
$raiz    = Split-Path -Parent $PSScriptRoot
$origem  = Join-Path $raiz "assets\regioes\texturas"
$destino = Join-Path $raiz "assets\regioes\cards"
$dados   = Join-Path $raiz "data\regioes.js"
if (-not (Test-Path $destino)) { New-Item -ItemType Directory -Path $destino | Out-Null }

$LARG = 800; $ALT = 480; $QUAL = 70
$ALVO_DET = 22.0     # detalhe fino desejado (diferenca media entre pixels vizinhos)
$DET_MIN = 0.72; $DET_MAX = 1.60   # limites do contraste: menos lava, mais serrilha
$ALVO = 88            # brilho desejado para as imagens escuras
$GAMA_MIN = 0.40      # nao levanta mais do que isso: acima disso aparece ruido

$codec = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
$par = New-Object System.Drawing.Imaging.EncoderParameters 1
$par.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter ([System.Drawing.Imaging.Encoder]::Quality), $QUAL

function Recorte($src) {
  $alvo = $LARG / $ALT
  if (($src.Width / $src.Height) -gt $alvo) { $cw = [int]($src.Height * $alvo); $ch = $src.Height }
  else { $cw = $src.Width; $ch = [int]($src.Width / $alvo) }
  @([int](($src.Width - $cw) / 2), [int](($src.Height - $ch) / 2), $cw, $ch)
}

# Contraste em torno do cinza medio, para igualar a intensidade entre as regioes.
function Matriz($c, $centro) {
  $cm = New-Object System.Drawing.Imaging.ColorMatrix
  $cm.Matrix00 = $c; $cm.Matrix11 = $c; $cm.Matrix22 = $c; $cm.Matrix33 = 1.0; $cm.Matrix44 = 1.0
  $t = ($centro / 255.0) * (1 - $c)          # gira em torno da media, nao do cinza medio
  $cm.Matrix40 = $t; $cm.Matrix41 = $t; $cm.Matrix42 = $t
  $cm
}

# Segundo passe: o contraste entra DEPOIS da gama, senao o GDI esmaga o preto
# das imagens escuras e nao sobra o que levantar.
function Contrastar($bmp, $c, $centro) {
  if ($c -eq 1.0) { return $bmp }
  $out = New-Object System.Drawing.Bitmap $bmp.Width, $bmp.Height
  $g = [System.Drawing.Graphics]::FromImage($out)
  $ia = New-Object System.Drawing.Imaging.ImageAttributes
  $ia.SetColorMatrix((Matriz $c $centro))
  $g.DrawImage($bmp, (New-Object System.Drawing.Rectangle 0, 0, $bmp.Width, $bmp.Height), 0, 0, $bmp.Width, $bmp.Height, [System.Drawing.GraphicsUnit]::Pixel, $ia)
  $g.Dispose(); $bmp.Dispose()
  $out
}

# Cor media da imagem. Serve de tom do papel nas regioes que nao tem brasao
# oficial para eu ler a cor (Ixtal e o Vazio).
function CorMedia($bmp) {
  $r = 0.0; $g = 0.0; $b = 0.0; $n = 0
  for ($x = 4; $x -lt $bmp.Width - 4; $x += 9) {
    for ($y = 4; $y -lt $bmp.Height - 4; $y += 9) {
      $p = $bmp.GetPixel($x, $y); $r += $p.R; $g += $p.G; $b += $p.B; $n++
    }
  }
  "#{0:x2}{1:x2}{2:x2}" -f [int]($r / $n), [int]($g / $n), [int]($b / $n)
}

# Detalhe fino: diferenca media de brilho entre pixels vizinhos na horizontal.
function Detalhe($bmp) {
  $soma = 0.0; $n = 0
  for ($y = 4; $y -lt $bmp.Height - 6; $y += 5) {
    $ant = $null
    for ($x = 4; $x -lt $bmp.Width - 6; $x += 5) {
      $p = $bmp.GetPixel($x, $y)
      $l = 0.2126 * $p.R + 0.7152 * $p.G + 0.0722 * $p.B
      if ($null -ne $ant) { $soma += [math]::Abs($l - $ant); $n++ }
      $ant = $l
    }
  }
  [math]::Round($soma / $n, 2)
}

function Desenha($src, $w, $h, $gama) {
  $r = Recorte $src
  $bmp = New-Object System.Drawing.Bitmap $w, $h
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
  $ia = New-Object System.Drawing.Imaging.ImageAttributes
  if ($gama -ne 1.0) { $ia.SetGamma($gama) }
  $g.DrawImage($src, (New-Object System.Drawing.Rectangle 0, 0, $w, $h), $r[0], $r[1], $r[2], $r[3], [System.Drawing.GraphicsUnit]::Pixel, $ia)
  $g.Dispose()
  $bmp
}

# Media do brilho num retangulo dado em fracoes da imagem.
function MedirZona($bmp, $x0, $x1, $y0, $y1) {
  $soma = 0.0; $n = 0
  for ($x = [int]($bmp.Width * $x0); $x -lt [int]($bmp.Width * $x1); $x += 6) {
    for ($y = [int]($bmp.Height * $y0); $y -lt [int]($bmp.Height * $y1); $y += 6) {
      $p = $bmp.GetPixel($x, $y)
      $soma += (0.2126 * $p.R + 0.7152 * $p.G + 0.0722 * $p.B); $n++
    }
  }
  [math]::Round($soma / $n, 1)
}

# O rodape (preco e tier) fica mais embaixo e a esquerda que o corpo do texto,
# e em Noxus e Bilgewater e justamente onde a imagem escurece. Quem manda e a
# mais escura das duas zonas.
function MedirRodape($bmp) { MedirZona $bmp 0.04 0.50 0.78 0.96 }

# O preco fica no alto a direita do card, e a etiqueta de tier embaixo a direita:
# os dois cantos que o degrade do papel nao alcanca.
function MedirCantoDir($bmp) { MedirZona $bmp 0.58 0.97 0.04 0.30 }

function Medir($bmp) {
  $soma = 0.0; $n = 0
  for ($x = [int]($bmp.Width * 0.04); $x -lt [int]($bmp.Width * 0.58); $x += 6) {
    for ($y = [int]($bmp.Height * 0.18); $y -lt [int]($bmp.Height * 0.82); $y += 6) {
      $p = $bmp.GetPixel($x, $y)
      $soma += (0.2126 * $p.R + 0.7152 * $p.G + 0.0722 * $p.B); $n++
    }
  }
  [math]::Round($soma / $n, 1)
}

$totalAntes = 0; $totalDepois = 0
$medidas = @()

Get-ChildItem $origem -File | Where-Object { $_.Extension -match '\.(png|jpg|jpeg)$' } | Sort-Object Name | ForEach-Object {
  $src = [System.Drawing.Image]::FromFile($_.FullName)

  $previa = Desenha $src 400 240 1.0
  $bruto = Medir $previa
  $det = Detalhe $previa
  $previa.Dispose()
  # o contraste cresce o detalhe quase na mesma proporcao; o passe seguinte confere
  $contraste = [math]::Round([math]::Max($DET_MIN, [math]::Min($DET_MAX, $ALVO_DET / $det)), 3)

  # Duas faixas: a imagem escura sobe ate 88 e continua escura; a de meio-tom
  # (latao, hexteca) so mostra o material na luz, entao sobe ate 148.
  $gama = 1.0; $mira = 0
  if ($bruto -lt ($ALVO - 4)) { $mira = $ALVO }
  elseif ($bruto -lt 118) { $mira = 148 }
  if ($mira) {
    $lo = $GAMA_MIN; $hi = 1.0
    for ($i = 0; $i -lt 7; $i++) {
      $m = ($lo + $hi) / 2
      $p = Desenha $src 400 240 $m
      $v = Medir $p; $p.Dispose()
      if ($v -lt $mira) { $hi = $m } else { $lo = $m }
    }
    $gama = [math]::Round(($lo + $hi) / 2, 3)
  }

  $bmp = Desenha $src $LARG $ALT $gama
  $bmp = Contrastar $bmp $contraste (Medir $bmp)
  $brilho = Medir $bmp

  $nome = [System.IO.Path]::GetFileNameWithoutExtension($_.Name) + ".jpg"
  $saida = Join-Path $destino $nome
  $bmp.Save($saida, $codec, $par)

  $rodape = MedirRodape $bmp
  $direita = MedirCantoDir $bmp
  $detFinal = Detalhe $bmp
  $cor = CorMedia $bmp
  $bmp.Dispose(); $src.Dispose()
  $antes = $_.Length; $depois = (Get-Item $saida).Length
  $totalAntes += $antes; $totalDepois += $depois
  $medidas += [pscustomobject]@{ nome = $nome; brilho = $brilho; rodape = $rodape; direita = $direita; det = $detFinal; cor = $cor }
  "{0,-24} {1,4:N0} KB   detalhe {2,5} -> {3,5} (x{4})   brilho {5,5}  gama {6,5}" -f `
    $nome, ($depois/1KB), $det, $detFinal, $contraste, $brilho, $gama
}

# card sem textura de origem e lixo de uma imagem substituida
$fontes = Get-ChildItem $origem -File | Where-Object { $_.Extension -match '\.(png|jpg|jpeg)$' } |
          ForEach-Object { [System.IO.Path]::GetFileNameWithoutExtension($_.Name) }
Get-ChildItem $destino -Filter *.jpg | Where-Object {
  $fontes -notcontains [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
} | ForEach-Object {
  "  apagado (a textura de origem sumiu): {0}" -f $_.Name
  Remove-Item $_.FullName -Force
}

""
"total: {0:N1} MB -> {1:N0} KB" -f ($totalAntes/1MB), ($totalDepois/1KB)
""





# ---------------------------------------------------------------- data/regioes.js
# Escrito aqui para o app nunca carregar numero digitado a mao: brilho, rodape e
# detalhe sao medidos, e as variantes sao os arquivos que existem de verdade.
# Em PowerShell variavel nao distingue maiuscula: $slug sobrescreveria este mapa.
$MAPA = [ordered]@{
  "Ionia" = "ionia"; "Freljord" = "freljord"; "Noxus" = "noxus"; "Demacia" = "demacia";
  "Targon" = "targon"; "Bilgewater" = "bilgewater"; "The Void" = "void";
  "Shadow Isles" = "shadow-isles"; "Piltover" = "piltover"; "Zaun" = "zaun";
  "Shurima" = "shurima"; "Bandle City" = "bandle-city"; "Ixtal" = "ixtal";
}
$inv = [System.Globalization.CultureInfo]::InvariantCulture
$nomes = $medidas | ForEach-Object { $_.nome.Replace(".jpg", "") }

$linhasMed = $medidas | ForEach-Object {
  '    "{0}": [{1}, {2}, {3}, {4}, "{5}"],' -f $_.nome.Replace(".jpg", ""),
    $_.brilho.ToString($inv), $_.rodape.ToString($inv), $_.direita.ToString($inv), $_.det.ToString($inv), $_.cor
}

$linhasVar = foreach ($regiao in $MAPA.Keys) {
  $pref = $MAPA[$regiao]
  # o arquivo base e os que comecam com o mesmo slug (noxus2, void1, freljord-garra)
  $lista = @($nomes | Where-Object { $_ -eq $pref -or $_ -match ("^" + [regex]::Escape($pref) + "[0-9-]") } | Sort-Object)
  if ($lista.Count -eq 0) { continue }
  '    "{0}": [{1}],' -f $regiao, (($lista | ForEach-Object { '"' + $_ + '"' }) -join ", ")
}

# Regiao no catalogo sem entrada aqui vira aviso. Foi assim que o Ixtal saiu
# calado da lista de variantes em 20/09/2026.
$catJs = Join-Path $raiz "data\catalog.js"
if (Test-Path $catJs) {
  $txt = [System.IO.File]::ReadAllText($catJs)
  $regioesDoCatalogo = [regex]::Matches($txt, '"region":\s*"([^"]+)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
  foreach ($r in $regioesDoCatalogo) {
    if ($r -ne "Runeterra" -and -not $MAPA.Contains($r)) {
      "  AVISO: o catalogo tem a regiao '$r' e este gerador nao a conhece - ela fica sem textura"
    }
  }
}

$js = @(
  "// GERADO por docs/gerar_cards_regiao.ps1 - nao editar a mao.",
  "// medidas[arquivo] = [brilho do corpo, do rodape, do canto direito de cima, detalhe fino, cor media],",
  "// medidos no proprio JPG depois do corte, do levante de meio-tom e do contraste.",
  "// variantes[regiao] = as imagens que existem; o card sorteia entre elas.",
  "window.REGIOES = {",
  "  medidas: {"
) + $linhasMed + @(
  "  },",
  "  variantes: {"
) + $linhasVar + @(
  "  },",
  "};",
  ""
)
[System.IO.File]::WriteAllLines($dados, $js, (New-Object System.Text.UTF8Encoding $false))
"data/regioes.js escrito com {0} imagens" -f $medidas.Count
