# Roteiro de QA

Um comando que abre o app, percorre os caminhos de sempre com clique de verdade
e diz o que quebrou.

```bash
python docs/qa_roteiro.py
```

Outras formas:

| Comando | O que faz |
|---|---|
| `python docs/qa_roteiro.py` | esta pasta, servida numa porta livre |
| `python docs/qa_roteiro.py --site` | o que está no ar, no GitHub Pages |
| `python docs/qa_roteiro.py --offline` | pula o que precisa do servidor das builds |
| `python docs/qa_roteiro.py -k marcador` | só o grupo com essa palavra no nome |
| `python docs/qa_roteiro.py --captura x.png` | salva uma captura do catálogo no fim |

Precisa de Chrome instalado e de `pip install websocket-client`. Sai com código
diferente de zero quando alguma checagem falha.

## Por que ele existe

Em 20/09/2026 dois bugs foram parar no ar e quem achou foi o Leo: a aba Públicas
vazia (`permission denied for table builds`) e os marcadores que abriam o
diálogo e não gravavam nada. Nenhum dos dois era difícil de pegar — bastava
abrir o app e fazer o de sempre. Os dois entraram no roteiro como checagem
própria, e é assim que ele cresce: **todo bug que o Leo achar vira uma linha
aqui**, para não achar duas vezes.

Os cliques são de verdade (CDP, `Input.dispatchMouseEvent`), não evento
sintético — evento sintético já passou verde com o drag e o duplo clique
quebrados.

## O que ele confere

**Arquivos** (sem abrir navegador, só quando roda nesta pasta)

- `.nojekyll` existe e nenhum caminho absoluto (`/assets/...`) no HTML.
- Todo `assets/...` citado no index.html existe **com a mesma caixa de letra** —
  o Pages é case-sensitive e o Windows não é, então `Assets/X.PNG` passa aqui e
  quebra lá.
- Todo MP3 do mapa de som existe em `assets/audio`.
- Todo card de região que o `data/regioes.js` aponta existe na pasta.

**Fundação** — 225 itens; as runas contadas pela estrutura batem com o número
que o gerador anotou (foi um leitor calado que escondeu 4 runas em 18/09);
entrar na loja sem exceção.

**Catálogo** — 225 cards desenhados; a busca filtra; a aba de núcleo vira
oficina com o estandarte de 46 px; a aba Todos volta a ser uma grade só.

**Forja** — a build nova nasce com as 8 caixas; item entra na caixa; o modo
leitura esconde os atributos.

**Marcadores** — escolher, o segundo espaço, trocar um já preenchido e tirar no
`×`. O `×` só existe no hover, então o roteiro passa o mouse antes; sem isso o
clique cai num retângulo de tamanho zero e acusa bug que não existe.

**Runas** — a página fecha em 9 de 9 e a faixa aparece na forja.

**Habilidades** — o nível 1 aceita clique (já ficou inalcançável uma vez), o
supremo é recusado no nível 5 e aceito no 6.

**Texto** — exportar e reimportar devolve a mesma build (itens, marcadores,
habilidades e runas).

**Acessibilidade** — os quatro interruptores ligam, o "menos movimento" zera as
transições de verdade, e tudo sobrevive ao recarregar.

**Builds publicadas** — a lista vem do servidor e não traz "permission denied".

**Resoluções** — 2560×1440, 1920×1080 e 1600×900, a ordem do Leo: sem rolagem
horizontal e nada fora da tela.

**Console** — nenhuma exceção e nenhum 404 durante o percurso inteiro.

## Achado na primeira volta — e consertado (21/09/2026)

Com as **38 builds publicadas na tela**, a página travava: o Chrome queimava um
núcleo inteiro e parava de responder por mais de um minuto. Acontecia nas duas
pontas — no navegador do roteiro e no navegador embutido, contra o site no ar.

Causa, medida por dentro: cada marcador de **habilidade** sem a lista do campeão
no cache pedia a lista ao Data Dragon e, na resposta, mandava redesenhar a lista
inteira. 38 linhas × até 3 marcadores = dezenas de pedidos, e cada redesenho
fazia os pedidos de novo. **`renderBuildIndex` rodava ~80 vezes em 4 segundos.**

Conserto: `pedirRedesenho()` junta os pedidos e redesenha **uma vez por quadro**.
De ~80 para **7**, a página continua respondendo e a arte da habilidade chega
igual. Duas checagens novas seguram isso: "sem tempestade de redesenho" e "a
arte da habilidade chega no marcador".

O grupo das públicas continua sendo o **último** do roteiro: é o estado mais
pesado do app, e depois dele qualquer medida sai contaminada.

## O que ele não faz

Não olha. Cor, alinhamento, peso da animação, se o card ficou bonito — isso
continua sendo captura de tela e o aprovado do Leo. O roteiro só garante que o
caminho ainda anda.
