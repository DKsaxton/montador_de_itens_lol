# Marcadores e nomes aceitos na importação

Gerado a partir de `data/catalog.js` (patch 16.18.1, 225 itens) e da lista `MARCADORES` do `index.html`. Não editar à mão: regenerar com o comando no fim.

## Como escrever a linha

```
MARCADORES: AD | Habilidade Q | Gume do Infinito
```

- Até **3** marcadores, separados por ` | `. O 4º em diante é ignorado.
- Maiúsculas/minúsculas e acentos **não importam** (`gume do infinito` = `Gume do Infinito`).
- Um nome que não bate com nenhuma das listas abaixo é **descartado em silêncio** (a build importa, mas sem aquele marcador).
- Os mesmos nomes de item valem nas linhas `- Item` das caixas e em `MESTRE FORJADOR: Item`.
- Habilidade só faz sentido com `CAMPEÃO:` preenchido; sem campeão o marcador aparece só como a letra.

## 1. Marcadores padrão (13)

Escreva exatamente o rótulo (a coluna *id* é só para conferência do arquivo SVG).

| Rótulo | id |
|---|---|
| `AD` | weapon |
| `Vitalidade` | vitality |
| `AP` | spirit |
| `Para novos jogadores` | complexity_1 |
| `Para jogadores intermediários` | complexity_2 |
| `Para jogadores avançados` | complexity_3 |
| `Dano` | damage |
| `Utilidade` | utility |
| `Cura` | healing |
| `Controle de grupo` | crowd_control |
| `Mobilidade` | mobility |
| `Burst` | melee |
| `Debuff` | debuff |

## 2. Habilidades (4)

| Escreva |
|---|
| `Habilidade Q` |
| `Habilidade W` |
| `Habilidade E` |
| `Habilidade R` |

## 3. Itens do catálogo (225)

Vale o nome em português **ou** em inglês; qualquer um dos dois resolve para o mesmo item.

### Starter (16)

| Português | Inglês |
|---|---|
| `Abatedora` | `Cull` |
| `Anel de Doran` | `Doran's Ring` |
| `Arco de Doran` | `Doran's Bow` |
| `Atlas Mundial` | `World Atlas` |
| `Berrante do Guardião` | `Guardian's Horn` |
| `Broto de Esmagamusgo` | `Mosstomper Seedling` |
| `Cria de Andabrisas` | `Gustwalker Hatchling` |
| `Elmo de Doran` | `Doran's Helm` |
| `Escudo de Doran` | `Doran's Shield` |
| `Filhote de Garrabrasa` | `Scorchclaw Pup` |
| `Lacre Sombrio` | `Dark Seal` |
| `Lágrima da Deusa` | `Tear of the Goddess` |
| `Lâmina de Doran` | `Doran's Blade` |
| `Lâmina do Guardião` | `Guardian's Blade` |
| `Martelo do Guardião` | `Guardian's Hammer` |
| `Orbe do Guardião` | `Guardian's Orb` |

### Consumível (7)

| Português | Inglês |
|---|---|
| `Atributo adicional` | `Stat Bonus` |
| `Elixir da Feitiçaria` | `Elixir of Sorcery` |
| `Elixir da Ira` | `Elixir of Wrath` |
| `Elixir de Ferro` | `Elixir of Iron` |
| `Poção com Refil` | `Refillable Potion` |
| `Poção de Vida` | `Health Potion` |
| `Sentinela de Controle` | `Control Ward` |

### Trinket (3)

| Português | Inglês |
|---|---|
| `Alteração Vidente` | `Farsight Alteration` |
| `Lente do Oráculo` | `Oracle Lens` |
| `Sentinela Invisível` | `Stealth Ward` |

### Distribuído (5)

| Português | Inglês |
|---|---|
| `Biscoito Total da Determinação Eterna` | `Total Biscuit of Everlasting Will` |
| `Botas Levemente Mágicas` | `Slightly Magical Footwear` |
| `Elixir da Avareza` | `Elixir of Avarice` |
| `Elixir da Força` | `Elixir of Force` |
| `Elixir da Habilidade` | `Elixir of Skill` |

### Bota (8)

| Português | Inglês |
|---|---|
| `Botas` | `Boots` |
| `Botas da Rapidez` | `Boots of Swiftness` |
| `Botas Galvanizadas de Aço` | `Plated Steelcaps` |
| `Botas Ionianas da Lucidez` | `Ionian Boots of Lucidity` |
| `Grevas do Berserker` | `Berserker's Greaves` |
| `Grevas Vorazes` | `Gluttonous Greaves` |
| `Passos de Mercúrio` | `Mercury's Treads` |
| `Sapatos do Feiticeiro` | `Sorcerer's Shoes` |

### Básico (15)

| Português | Inglês |
|---|---|
| `Adaga` | `Dagger` |
| `Amuleto da Fada` | `Faerie Charm` |
| `Bastão Desnecessariamente Grande` | `Needlessly Large Rod` |
| `Capa da Agilidade` | `Cloak of Agility` |
| `Couraça de Pano` | `Cloth Armor` |
| `Cristal de Rubi` | `Ruby Crystal` |
| `Cristal de Safira` | `Sapphire Crystal` |
| `Espada G. p. C.` | `B. F. Sword` |
| `Espada Longa` | `Long Sword` |
| `Manto Anula-Magia` | `Null-Magic Mantle` |
| `Partícula Brilhante` | `Glowing Mote` |
| `Pérola do Rejuvenescimento` | `Rejuvenation Bead` |
| `Picareta` | `Pickaxe` |
| `Tomo Amplificador` | `Amplifying Tome` |
| `Varinha Explosiva` | `Blasting Wand` |

### Épico (44)

| Português | Inglês |
|---|---|
| `Aljava Vespertina` | `Noonquiver` |
| `Alternador Hextec` | `Hextech Alternator` |
| `Arco Recurvo` | `Recurve Bow` |
| `Armaguarda da Caçadora` | `Seeker's Armguard` |
| `Bandana de Mercúrio` | `Quicksilver Sash` |
| `Barreira Verdejante` | `Verdant Barrier` |
| `Braçadeira Cristalina` | `Crystalline Bracer` |
| `Brasa de Bami` | `Bami's Cinder` |
| `Broquel Glacial` | `Glacial Buckler` |
| `Brutalizador` | `The Brutalizer` |
| `Capa Negatron` | `Negatron Cloak` |
| `Capítulo Perdido` | `Lost Chapter` |
| `Capuz do Espectro` | `Spectre's Cowl` |
| `Carapaça do Vigia` | `Warden's Mail` |
| `Catalisador das Eras` | `Catalyst of Aeons` |
| `Cetro Vampírico` | `Vampiric Scepter` |
| `Chamado do Carrasco` | `Executioner's Calling` |
| `Cintilação Etérea` | `Aether Wisp` |
| `Cinto do Gigante` | `Giant's Belt` |
| `Cinzas do Destino` | `Fated Ashes` |
| `Códex Demoníaco` | `Fiendish Codex` |
| `Colete Espinhoso` | `Bramble Vest` |
| `Cota de Malha` | `Chain Vest` |
| `Couraça Lunar Alada` | `Winged Moonplate` |
| `Espelho de Bandópolis` | `Bandleglass Mirror` |
| `Estilingue do Patrulheiro` | `Scout's Slingshot` |
| `Fago` | `Phage` |
| `Fulgor` | `Sheen` |
| `Gema Ardente` | `Kindlegem` |
| `Hexdrinker` | `Hexdrinker` |
| `Ídolo Proibido` | `Forbidden Idol` |
| `Joia da Ruína` | `Blighting Jewel` |
| `Machado Termestre` | `Hearthbound Axe` |
| `Martelo de Guerra de Caulfield` | `Caulfield's Warhammer` |
| `Máscara Assustadora` | `Haunting Guise` |
| `Orbe do Oblívio` | `Oblivion Orb` |
| `Punhal Serrilhado` | `Serrated Dirk` |
| `Retriz` | `Rectrix` |
| `Salva-Vidas` | `Lifeline` |
| `Sigilo de Aço` | `Steel Sigil` |
| `Tiamat` | `Tiamat` |
| `Tunelizador` | `Tunneler` |
| `Último Sussurro` | `Last Whisper` |
| `Zelo` | `Zeal` |

### Lendário (114)

| Português | Inglês |
|---|---|
| `A Coletora` | `The Collector` |
| `Acerto de Contas de Atma` | `Atma's Reckoning` |
| `Adaga Oscilante Navori` | `Navori Flickerblade` |
| `Alfanje Espectral` | `Spectral Cutlass` |
| `Ampulheta de Zhonya` | `Zhonya's Hourglass` |
| `Anjo Guardião` | `Guardian Angel` |
| `Ápice da Tempestade` | `Stormsurge` |
| `Aproximação Invernal` | `Winter's Approach` |
| `Arco do Axioma` | `Axiom Arc` |
| `Arco-escudo Imortal` | `Immortal Shieldbow` |
| `Armadura de Espinhos` | `Thornmail` |
| `Armadura de Warmog` | `Warmog's Armor` |
| `Armadura Sangrenta do Suserano` | `Overlord's Bloodmail` |
| `Atualizador` | `Actualizer` |
| `Auronúcleo` | `Dawncore` |
| `Aurora e Crepúsculo` | `Dusk and Dawn` |
| `Bandocanos` | `Bandlepipes` |
| `Bastão das Eras` | `Rod of Ages` |
| `Bênção de Mikael` | `Mikael's Blessing` |
| `Cajado Aquafluxo` | `Staff of Flowing Water` |
| `Cajado do Arcanjo` | `Archangel's Staff` |
| `Cajado do Vazio` | `Void Staff` |
| `Canção de Sangue` | `Bloodsong` |
| `Canhão Fumegante` | `Rapid Firecannon` |
| `Capuz da Morte de Rabadon` | `Rabadon's Deathcap` |
| `Cetro de Cristal de Rylai` | `Rylai's Crystal Scepter` |
| `Céu Dividido` | `Sundered Sky` |
| `Chama Sombria` | `Shadowflame` |
| `Chuva de Canivete` | `Stormrazor` |
| `Cicloespada Voltaica` | `Voltaic Cyclosword` |
| `Cimitarra Mercurial` | `Mercurial Scimitar` |
| `Colhedor de Essência` | `Essence Reaver` |
| `Convergência de Zeke` | `Zeke's Convergence` |
| `Coração Congelado` | `Frozen Heart` |
| `Coração de Aço` | `Heartsteel` |
| `Couraça do Defunto` | `Dead Man's Plate` |
| `Couraça Protoplasmática` | `Protoplasm Harness` |
| `Criafendas` | `Riftmaker` |
| `Criassonhos` | `Dream Maker` |
| `Criptoflora` | `Cryptbloom` |
| `Cutelo Negro` | `Black Cleaver` |
| `Dança da Morte` | `Death's Dance` |
| `Dançarina Fantasma` | `Phantom Dancer` |
| `Dardos de Caça-Demônios` | `Fiendhunter Bolts` |
| `Dente de Na'Shor` | `Nashor's Tooth` |
| `Desespero Eterno` | `Unending Despair` |
| `Eclipse` | `Eclipse` |
| `Eco de Luden` | `Luden's Echo` |
| `Ecos de Helia` | `Echoes of Helia` |
| `Égide de Fogo Solar` | `Sunfire Aegis` |
| `Espada do Rei Destruído` | `Blade of The Ruined King` |
| `Explocinturão Hextec` | `Hextech Rocketbelt` |
| `Faca de Statikk` | `Statikk Shiv` |
| `Flechatroz de Yun Tal` | `Yun Tal Wildarrows` |
| `Foco do Horizonte` | `Horizon Focus` |
| `Fome Eterna` | `Endless Hunger` |
| `Força da Natureza` | `Force of Nature` |
| `Força da Trindade` | `Trinity Force` |
| `Furacão de Runaan` | `Runaan's Hurricane` |
| `Glaive Sombria` | `Umbral Glaive` |
| `Gume do Infinito` | `Infinity Edge` |
| `Hexoplaca Experimental` | `Experimental Hexplate` |
| `Hexótica C44` | `Hexoptics C44` |
| `Hidra Profana` | `Profane Hydra` |
| `Hidra Raivosa` | `Ravenous Hydra` |
| `Hidra Titânica` | `Titanic Hydra` |
| `Hino Bélico de Shurelya` | `Shurelya's Battlesong` |
| `Húbris` | `Hubris` |
| `Ímpeto Cósmico` | `Cosmic Drive` |
| `Invadomínio de Zaz'Zak` | `Zaz'Zak's Realmspike` |
| `Jak'Sho, o Inconstante` | `Jak'Sho, The Protean` |
| `Juramento do Cavaleiro` | `Knight's Vow` |
| `Ladrão de Almas de Mejai` | `Mejai's Soulstealer` |
| `Lâmina da Fúria de Guinsoo` | `Guinsoo's Rageblade` |
| `Lâmina Fantasma de Youmuu` | `Youmuu's Ghostblade` |
| `Lança de Shojin` | `Spear of Shojin` |
| `Lembranças do Lorde Dominik` | `Lord Dominik's Regards` |
| `Lembrete Mortal` | `Mortal Reminder` |
| `Limiar da Noite` | `Edge of Night` |
| `Limite da Razão` | `Wit's End` |
| `Maldição Sanguinária` | `Bloodletter's Curse` |
| `Malevolência` | `Malignance` |
| `Manamune` | `Manamune` |
| `Mandato Imperial` | `Imperial Mandate` |
| `Mandíbula de Malmortius` | `Maw of Malmortius` |
| `Manopla dos Glacinatas` | `Iceborn Gauntlet` |
| `Máscara Abissal` | `Abyssal Mask` |
| `Mata-Cráquens` | `Kraken Slayer` |
| `Medalhão dos Solari de Ferro` | `Locket of the Iron Solari` |
| `Morellonomicon` | `Morellonomicon` |
| `Oposição Celestial` | `Celestial Opposition` |
| `Perdição de Lich` | `Lich Bane` |
| `Pistola Laminar Hextec` | `Hextech Gunblade` |
| `Presa da Serpente` | `Serpent's Fang` |
| `Presságio de Randuin` | `Randuin's Omen` |
| `Quebra-Bastião` | `Bastionbreaker` |
| `Quebracascos` | `Hullbreaker` |
| `Quebrapassos` | `Stridebreaker` |
| `Rancor de Serylda` | `Serylda's Grudge` |
| `Redenção` | `Redemption` |
| `Regenerador de Pedra Lunar` | `Moonstone Renewer` |
| `Resplendor Vazio` | `Hollow Radiance` |
| `Rookern Lamúrico` | `Kaenic Rookern` |
| `Sedenta por Sangue` | `Bloodthirster` |
| `Semblante Espiritual` | `Spirit Visage` |
| `Serrespada Quimiopunk` | `Chempunk Chainsword` |
| `Sinal de Sterak` | `Sterak's Gage` |
| `Terminus` | `Terminus` |
| `Tiara Sussurrante` | `Whispering Circlet` |
| `Tocha de Chamas Negras` | `Blackfire Torch` |
| `Tormento de Liandry` | `Liandry's Torment` |
| `Trenó do Solstício` | `Solstice Sleigh` |
| `Turíbulo Ardente` | `Ardent Censer` |
| `Véu da Banshee` | `Banshee's Veil` |

### Evolução (10)

| Português | Inglês |
|---|---|
| `Abraço de Seraph` | `Seraph's Embrace` |
| `Caminho Imortal` | `Immortal Path` |
| `Esmagadores Acorrentados` | `Chainlaced Crushers` |
| `Fimbulwinter` | `Fimbulwinter` |
| `Grevas Bélicas` | `Gunmetal Greaves` |
| `Lucidez Escarlate` | `Crimson Lucidity` |
| `Marcha Célere` | `Swiftmarch` |
| `Mobilização Blindada` | `Armored Advance` |
| `Muramana` | `Muramana` |
| `Sapatos Enfeitiçados` | `Spellslinger's Shoes` |

### Lendário (Evolução) (2)

| Português | Inglês |
|---|---|
| `Dádiva dos Mundos` | `Bounty of Worlds` |
| `Diadema de Canções` | `Diadem of Songs` |

### Épico (Evolução) (1)

| Português | Inglês |
|---|---|
| `Bússola Rúnica` | `Runic Compass` |

## Regenerar

```bash
python docs/gerar_marcadores.py
```
