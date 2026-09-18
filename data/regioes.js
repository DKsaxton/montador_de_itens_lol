// GERADO por docs/gerar_cards_regiao.ps1 - nao editar a mao.
// medidas[arquivo] = [brilho do corpo, do rodape, do canto direito de cima, detalhe fino],
// medidos no proprio JPG depois do corte, do levante de meio-tom e do contraste.
// variantes[regiao] = as imagens que existem; o card sorteia entre elas.
window.REGIOES = {
  medidas: {
    "bandle-city": [135.3, 109.7, 96.1, 15.95],
    "bilgewater": [88.8, 46.5, 44.8, 20.97],
    "demacia": [168.5, 124.5, 105.2, 15.01],
    "freljord": [151.5, 141.1, 105, 19.48],
    "freljord-avarosan": [210.2, 181.6, 190.6, 7.82],
    "freljord-garra": [123.3, 94.8, 80.9, 21.92],
    "freljord-garra1": [162.7, 121.1, 105.3, 22.49],
    "freljord-guarda": [87.2, 60, 50.6, 9.39],
    "ionia": [162.8, 84.6, 126.1, 17.68],
    "noxus": [89.5, 62.7, 105.9, 21.55],
    "noxus2": [89.6, 42.9, 66.8, 16.43],
    "piltover": [146.5, 90.8, 77, 7.14],
    "shadow-isles": [87.2, 106, 34.8, 15.43],
    "shurima": [134.8, 84.1, 103.8, 19.37],
    "targon": [158.2, 137.3, 16, 8.45],
    "void": [144.5, 92.7, 45.7, 10.17],
    "void1": [155.4, 124.1, 111.8, 21.84],
    "void2": [163.2, 113.8, 118.6, 19.86],
    "void3": [147.9, 95.1, 65.7, 17.08],
    "zaun": [87.4, 78.7, 58.2, 14.08],
  },
  variantes: {
    "Ionia": ["ionia"],
    "Freljord": ["freljord", "freljord-avarosan", "freljord-garra", "freljord-garra1", "freljord-guarda"],
    "Noxus": ["noxus", "noxus2"],
    "Demacia": ["demacia"],
    "Targon": ["targon"],
    "Bilgewater": ["bilgewater"],
    "The Void": ["void", "void1", "void2", "void3"],
    "Shadow Isles": ["shadow-isles"],
    "Piltover": ["piltover"],
    "Zaun": ["zaun"],
    "Shurima": ["shurima"],
    "Bandle City": ["bandle-city"],
  },
};

