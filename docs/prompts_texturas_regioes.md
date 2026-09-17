# Prompts das texturas de região

Você gera, eu integro. O que importa aqui é **consistência**: dezesseis imagens que pareçam do mesmo conjunto, não dezesseis ilustrações soltas.

## Como usar

1. Cole o **Bloco base** e, logo abaixo, o trecho da região.
2. Peça em **paisagem** (a opção larga). No ChatGPT não dá para escolher a proporção: ele só entrega quadrado, paisagem ou retrato. Paisagem sai em 1536 × 1024, e o corte para a proporção do card é comigo — sobra margem de sobra.
3. Salve o que vier, **sem editar e sem redimensionar**, em `assets/regioes/texturas/<nome>.png` (ou `.jpg`, tanto faz o que ele der), com o nome exato da tabela.
4. Me avise quando tiver algumas prontas. Eu corto, comprimo, meço o peso e monto os cards.

Se a imagem sair com personagem, texto, logo ou moldura desenhada, gere de novo: o card já tem moldura, e o texto é escrito por cima. Vale mandar `sem moldura, sem texto, preencha a imagem toda` como correção — ele costuma obedecer no segundo pedido.

Se ele devolver quadrado mesmo assim, não tem problema: eu corto igual. O que não posso consertar é imagem com moldura desenhada ou com o assunto no meio.

## Bloco base — cole antes de cada região

```
Generate a wide landscape image: a flat top-down photograph of a material surface, seen
straight from above, filling the entire frame from edge to edge, like a close-up of a table,
a wall or a metal plate. Even soft lighting from the upper left, shallow depth, fine grain,
subtle wear. Painterly but realistic, League of Legends splash-art quality.

Do not include people, creatures, faces, text, letters, numbers, logos, emblems, borders,
frames, vignettes or watermarks. Do not put a subject in the middle: keep the central and
left area calm and uncluttered so dark text can be read over it, and concentrate the detail
toward the edges and the lower right corner. Muted values, nothing pure white or pure black.
It should look like a crop out of a much larger surface, with no composition of its own.

The surface is:
```

## As regiões

O nome do arquivo está sem extensão de propósito: use a que o ChatGPT devolver.

| Arquivo | Região | Trecho para colar |
|---|---|---|
| `runeterra` | — | não gere. Runeterra é neutro e continua no papel de sempre |
| `ionia` | Ionia | aged rice paper with a single wide sumi-e ink brushstroke sweeping from the lower left to the upper right, soft magenta and rose pigment bleeding into the fibers, a few cherry petals resting on the surface, warm off-white ground |
| `freljord` | Freljord | thick pale blue glacial ice with internal cracks and trapped air bubbles, frost creeping in from the edges, a strip of worn brown leather and white fur along the bottom edge, cold daylight |
| `noxus` | Noxus | dark iron plate with heavy rivets and hammer marks, deep crimson war banner cloth draped across the left side, dried blood stains soaked into the metal at the bottom, harsh and brutal |
| `demacia` | Demacia | pale grey petricite stone with fine mineral speckles, polished gold filigree inlay running along the edges, clean carved channels, noble and orderly, cool white light |
| `targon` | Targon | pale carved mountain stone in the lower half, deep violet star-filled night sky in the upper strip only, faint cosmic light spilling over the rock, restrained and quiet |
| `bilgewater` | Bilgewater | weathered wet ship deck planks, thick tarred rope laid along the left edge, rust stains, salt crust, dark seawater soaked into the grain, warm rust and burnt orange |
| `void` | The Void | cracked pale bone-grey matter split by a jagged fissure on the right side, violent violet light glowing from inside the crack, organic tendrils of dark purple flesh creeping out, wrong and alive |
| `shadow-isles` | Shadow Isles | rotted grey wood and mossy stone, thick spectral teal mist pouring across the bottom third and glowing from below, dead black branches at the top edge, cold and lifeless |
| `piltover` | Piltover | polished brass plate with a faint hexagonal lattice etched into it, precise machined edges, small exposed gears at the lower right, a soft blue hextech crystal glow from the upper right corner, clean and engineered |
| `zaun` | Zaun | grimy industrial metal plate stained with toxic green chemical residue, riveted pipes and a brass valve along the bottom, dripping luminous green sludge, smog haze at the top, no gold, no polish |
| `shurima` | Shurima | golden sandstone slab with carved hieroglyph bands along the bottom, fine desert sand drifted across the lower edge, gold inlay catching hard sunlight, sun-bleached and dry |
| `bandle-city` | Bandle City | soft felt and woven cloth in lime and moss green, visible hand stitching, small wooden pegs and acorns at the edges, cozy and handmade, warm daylight |

## As três tribos do Freljord

A atmosfera é o que separa as três, não o adereço.

| Arquivo | Tribo | Trecho para colar |
|---|---|---|
| `freljord-avarosan` | Avarosan | clean pale blue ice under open winter sky, smooth untouched frost, cream woven cloth and light fur along the bottom edge, bright, orderly, hopeful |
| `freljord-garra` | Garra do Inverno | rough cracked ice smeared with frozen blood, splintered bone and raw dark hide lashed with cord, gouged claw marks, savage and dirty |
| `freljord-guarda` | Guarda Gélida | black lifeless ice with dull violet light trapped deep inside, sharp frozen shards, no warmth, no texture of cloth or fur, silent and dead |

## O que eu faço quando chegarem

- Corto para a proporção do card e comprimo até um peso que não atrase o site, medindo antes e depois.
- Monto o card por cima: brasão oficial da Riot no canto, faixa limpa para o texto, barra do núcleo na esquerda.
- Meço o peso total do repositório e te digo quanto cresceu.
- Se alguma imagem ficar agitada demais debaixo do texto, eu escureço ou clareio só aquela faixa por CSS, sem mexer no arquivo.
