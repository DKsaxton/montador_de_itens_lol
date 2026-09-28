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
No modo Ícones, o mouse não aciona o golpe do AD nem apaga o ícone (F13-T29,
bug nº 46); nos Cards, o golpe continua.

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

**Rascunho** (F13-T24, bug nº 37) — com o Editar ligado e um item não salvo,
reabrir a build que já está na forja (duplo clique na linha, o Editar do
detalhe) mantém o rascunho; o coração da lista grava na hora sem gravar o
rascunho; e o Descartar continua voltando à cópia salva. Olha o
`rascunho.sujo` e o localStorage, não só a forja: um conserto que gravasse o
rascunho calado também deixaria o item na tela.

**Troca de build** (F13-T25, bug nº 38) — com o rascunho sujo, abrir outra
build pela lista, "+ Nova build" e Importar perguntam Salvar/Descartar como a
forja pergunta, e "Salvar e sair" grava e segue; excluir outra build e digitar
o nome na janela "Falta pouco para publicar" gravam o que é deles sem gravar as
caixas do rascunho; um Ctrl+S com essa janela aberta não solta a cópia (o
que se digita depois ainda grava); e o Enter da lista abre o diálogo com o
foco nele. Cada checagem monta o próprio estado e só responde o diálogo se ele
apareceu, para falhar sozinha no código de antes.

**Salvar** (F13-T31, bug nº 14; o `setItem` da biblioteca recusado) — o Salvar
não diz "salvo" (o botão fica aceso, o aviso de saída armado, sem o som); a placa
explica, com o foco nela; o "Salvar e sair" não sai; o Ctrl+S numa build limpa
não a suja; a cópia na memória não fica com o que não gravou, e o Descartar
descarta de verdade; o coração recusado avisa; a publicação que passou sem
gravar aqui pede para anotar o ID; com a gravação de volta, o aviso some
sozinho e o Salvar salva.

**Publicação órfã** (F13-T34, bug nº 42; servidor simulado, espera encurtada) —
com a publicação no ar, a build não se exclui (lista, forja, lote); despublicar
durante o "Atualizar publicação" espera; publicar durante uma exclusão no ar
espera; se a build some mesmo assim, a publicação recém-criada sai do site.

**Atualização** (F13-T33, bugs nºs 13 e 41) — abrir outra build depois de
recarregar não muda a "Última atualização" (e a publicada continua "Publicada");
uma mudança de verdade ainda carimba; o Mestre Forjador não acende a nota da
publicação; um Salvar durante uma publicação lenta acende; a build migrada do
formato antigo tem data.

**Última build** (F13-T32, bug nº 15) — com uma pública aberta, a última build
própria não se exclui (o Excluir desligado) e o "Fechar visualização" ainda
fecha; a exclusão da última própria não deixa cópia fantasma; com uma
visualização aberta, a ativa gravada é a sua; o Excluir da forja numa
visualização fecha sem perguntar; a biblioteca gravada vazia não traz de volta a
build do formato antigo.

**Publicar** (F13-T30, bugs nºs 11, 12 e 26; servidor simulado) — o hidden
esconde sempre (Descartar sem rascunho, ⟳ em Minhas); o "+ Nova categoria" não
anda quando o rascunho aparece; durante "Publicando…" não há Fechar e o Enter
não manda outro pedido; depois de um erro o Enter fecha a placa; servidor lento:
o Fechar aparece (os 30 s encurtados trocando o relógio da página), a trava
segura e a resposta atrasada vale; a placa atrasada fica por cima do
"Alterações não salvas" e o Esc fecha só ela; ao salvar, o Descartar some na hora.

**Acessibilidade** — os quatro interruptores ligam, o "menos movimento" zera as
transições de verdade, e tudo sobrevive ao recarregar.

**Builds publicadas** — a lista vem do servidor e não traz "permission denied".

**Resoluções** — 2560×1440, 1920×1080 e 1600×900, a ordem do Leo, mais
1280×800 como piso de notebook: sem rolagem horizontal e nada fora da tela.
**Celular não é alvo** (Leo, 21/09/2026: "não tenho a intenção de fazer para o
celular"): o app é ferramenta de mesa, e 375px não entra na conta — medido, a
página abre com viewport de 513px e os cards têm 281px fixos.

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
