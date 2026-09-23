# Caçada de bugs — 22/09/2026 (F13-T5)

Oito leitores varreram o `index.html` em paralelo, um por subsistema: estado da build, eventos e redesenho, persistência, servidor, runas e habilidades, importar e exportar, catálogo e contas, e CSS e acessibilidade. Cada achado passou por três céticos, cada um com uma lente: se a leitura do código está certa, se o passo a passo acontece mesmo e se outra parte do arquivo já cobre o caso. Só sobrevivia o que resistisse a dois votos.

**Resultado: 40 achados, 33 bugs distintos** depois de juntar os repetidos (o mesmo bug achado por duas ou três frentes). Os céticos derrubaram só um voto em 120, o que é aprovação demais para se confiar sem conferir. Por isso reproduzi os quatro mais graves no app, com clique de verdade, e os quatro se confirmaram.

Status de cada um:
- **REPRODUZIDO** — rodei no app e o erro aconteceu.
- **passou pelos céticos** — três leituras independentes do código concordaram, mas eu ainda não reproduzi.


## Reproduzidos

### 1. Remover dois itens em sequência rápida apaga o item errado: o splice atrasado usa um índice velho

**CONSERTADO na F13-T7 (22/09/2026).** A saída procura o próprio item na hora de sair (`indexOf(entry)`), não a posição guardada 380 ms antes; o item que já está saindo nasce escondido nos redesenhos do meio (`.tile-saindo`) em vez de reaparecer, e um segundo ✕ no mesmo item é ignorado. Conferido em 8 casos, incluindo o mouse de verdade com o segundo clique aos 170 ms.

`index.html:6083` · alta · achado por: Estado da build, Eventos e redesenho

**REPRODUZIDO.** Reproduzido em 22/09: pedi para tirar A e B, o app tirou A e C.

**Como quebra:** Na forja, com Editar ligado, numa caixa com três itens na ordem A, B, C: 1) clique no × do A (ou botão direito sobre ele) — a placa começa a afundar, mas nada é apagado ainda; 2) dentro de 0,38 s clique no × do B. O que acontece: em t=380ms o primeiro finish roda splice(0,1) e tira o A, e renderBuild redesenha a caixa com B no índice 0 e C no índice 1; em t=480ms o segundo finish, que guardou index=1 de quando o B ainda era o segundo, roda splice(1,1) e tira o C. Resultado: o Leo pediu para tirar A e B, o app tirou A e C, o B volta a aparecer e o C some sem ninguém ter pedido. Com só dois itens na caixa o efeito é o oposto: o splice(1,1) cai fora do array e o B simplesmente não sai. O clique no × é da F13-T3, então dois cliques seguidos em meio segundo são o uso normal, não um caso de laboratório. O guarda `!tile.classList.contains("tile-remove")` só cobre clicar duas vezes na MESMA placa (e o CSS já corta isso com pointer-events:none) — ele não cobre a placa vizinha, que é o caso comum.

### 2. Busca por ID inexistente na aba Públicas entra em laço infinito de requisições ao Supabase

**CONSERTADO na F13-T6 (22/09/2026).** O app passa a lembrar os IDs que o servidor já disse que não existem (`publicas.naoExistem`); a favorita que sumiu do site sai dos favoritos; `carregarFavoritas` pede uma vez só; sem internet, um pedido e espera um minuto. O ⟳ esquece tudo e pergunta de novo. Medido: de 117 e 126 pedidos em 5 s para **1**.

`index.html:8726` · alta · achado por: Servidor das builds publicadas, Eventos e redesenho

**REPRODUZIDO.** Reproduzido em 22/09: **117 pedidos ao Supabase em 5 segundos**, com a busca parada.

**Como quebra:** Abrir Builds → aba Públicas → digitar (ou colar) na busca um ID de 6 caracteres hexadecimais que não existe no servidor — um ID apagado, um ID digitado errado, ou até uma palavra que só usa letras a-f, como "cabeça" (o norm() tira o acento e sobra "cabeca", 6 caracteres hex). O guarda da linha 8724 (q não vazio, dados vazio, regex hex, publicaPorId(q) nulo, buscandoId nulo) passa e dispara o GET. A resposta volta [] (ou cai no .catch quando não há internet), o .finally zera publicas.buscandoId e chama renderBuildIndex(), que volta a renderPublicasIndex com a MESMA busca: dados continua vazio, publicaPorId(q) continua nulo, buscandoId já é nulo de novo — e o mesmo GET é disparado outra vez. O ciclo só para se o usuário alterar o texto da busca ou trocar de aba. Enquanto isso a página dispara requisições ao Supabase sem parar (uma por round-trip, indefinidamente) e redesenha a lista inteira a cada volta.

### 3. Favorita apagada do site põe a lista de builds num laço infinito de requisição + redesenho

**CONSERTADO na F13-T6 (22/09/2026).** O app passa a lembrar os IDs que o servidor já disse que não existem (`publicas.naoExistem`); a favorita que sumiu do site sai dos favoritos; `carregarFavoritas` pede uma vez só; sem internet, um pedido e espera um minuto. O ⟳ esquece tudo e pergunta de novo. Medido: de 117 e 126 pedidos em 5 s para **1**.

`index.html:8933` · alta · achado por: Eventos e redesenho, Servidor das builds publicadas

**REPRODUZIDO.** Reproduzido em 22/09: **126 pedidos ao Supabase em 5 segundos**, parado na aba Minhas.

**Como quebra:** Aba Build → lista → aba Públicas: favorite uma build publicada sua (o ID vai para localStorage publicacao.favoritos). Selecione-a e clique em "Excluir do site" (ou "Despublicar" na aba Minhas, ou apague a build local que a publicou — deleteBuild também manda apagar_build). Os três caminhos filtram publicas.lista e publicas.favs, mas NENHUM tira o ID de publicacao.favoritos. Volte para a aba Minhas. renderBuildIndex lê favIds, vê que publicaPorId(fantasma) é null e chama carregarFavoritas(), que pede builds_publicas?id=in.(fantasma) ao Supabase. O servidor devolve [], publicas.favs = favs.concat([]) não muda nada, e a função chama renderBuildIndex() no fim — que encontra o mesmo fantasma e pede de novo. Laço sem saída: uma requisição por ida-e-volta de rede, para sempre, com #bi-rows reescrito a cada volta (a linha selecionada e a posição da lista piscam e o duplo clique numa build fica instável, porque a linha é trocada entre os dois cliques). Como o ID mora no localStorage, o laço volta em toda recarga assim que a aba Build abre na lista, e cada renderBuild()→renderLibrary()→renderBuildIndex() adicional inicia mais uma corrente que nunca morre.

### 4. Duplicar uma build perde a página de runas e a ordem de habilidades (e o Mestre Forjador)

**CONSERTADO na F13-T8 (22/09/2026).** `duplicateBuild` e `copiarPublica` passam a levar runas e ordem de habilidades, e o duplicar leva também o Mestre Forjador (a publicada não guarda esse interruptor — os outros dois caminhos da publicada já nasciam com ele desligado). Conferido em 12 casos: cópia independente da original, duplicar a build que não está ativa, build vazia, "Copiar e editar" de uma publicada real, e recarregar.

**Achado no caminho, e consertado junto:** importar uma build com **Mestre Forjador** ou **campeão** deixava a build nova como rascunho "não salvo" — o importador chamava `saveBuild()`, que com o Editar ligado só marca rascunho. Recarregando e escolhendo sair, os dois se perdiam. Apareceu porque, com o duplicar consertado, o texto exportado passou a levar a linha do Mestre Forjador, e o roteiro de QA travou num aviso de "sair sem salvar?" ao recarregar. Agora `gravarImportado()` grava — a não ser que a pessoa já tenha começado a mexer, e aí o rascunho é dela.

`index.html:9107` · alta · achado por: Estado da build, Runas e habilidades, Servidor das builds publicadas

**REPRODUZIDO.** Reproduzido em 22/09: a cópia nasce com runas vazias, 0 de 6 níveis de habilidade e o Mestre Forjador desligado.

**Como quebra:** 1) Numa build sua, monte a página de runas e a ordem de habilidades na forja; 2) clique em "Duplicar" (botão dup-build, ou "Copiar e editar" no resumo da lista). A cópia abre sem runa nenhuma e com os 18 níveis vazios. Motivo: duplicateBuild só repassa cats, mode, champ e markers para createNewBuild, e createNewBuild nasce com `runas: normRunas(null)` e `habilidades: normHabilidades(null)` (linhas 5962-5963); depois dele só desc e layout são copiados à mão. O mesmo buraco está em copiarPublica (linha 8776): abrir uma build publicada em "Só visualização" MOSTRA as runas e a ordem (abrirPublicaTemporaria copia os dois, linha 8755), e clicar em "Copiar e editar" entrega uma cópia sem eles. Os dois caminhos gêmeos discordam: guardarPublicaNaBiblioteca (linha 8918, o "Importar" do modo Selecionar) e o importador de texto (linhas 9424-9425) copiam runas e habilidades direitinho. Pelo mesmo caminho se perde o interruptor Mestre Forjador: masterwork nem existe em buildResumo, então a cópia sempre nasce com ele desligado e os atributos exibidos mudam.


## Gravidade alta

### 5. Excluir uma build publicada promete tirá-la do site, mas engole a falha do apagar_build

`index.html:5983` · alta · achado por: Servidor das builds publicadas · **passou pelos céticos**

**Como quebra:** Publicar uma build. Depois, sem internet (ou com o Supabase fora do ar / bloqueado por CORS ao abrir do disco), selecionar a build na lista e clicar em Excluir: o confirm diz textualmente "Ela também sai do site." (mesma promessa no lote: "As publicadas também saem do site."). O usuário confirma, a chamada apagar_build é disparada sem await, a rejeição cai num .catch vazio e a execução segue apagando a build local. Resultado: a build some da biblioteca, a publicação continua no ar, nenhuma mensagem aparece — e como o pubId foi apagado junto, o usuário não tem mais como chamar "Excluir do site" nem sabe o ID para procurar na aba Públicas. O retorno também é ignorado: quando apagar_build devolve false (segredo não confere), não há rejeição nenhuma e o silêncio é o mesmo.

### 6. Runa escolhida fora do primeiro slot some sem aviso ao copiar e reimportar a build

**CONSERTADO na F13-T12 (22/09/2026).** Vaga vazia sai como `-`; a primária é lida pelo slot de cada runa; fragmentos sem os `-` (texto antigo) procuram a primeira distribuição em que cada nome cabe no seu grupo. De brinde: página só com fragmentos deixou de ser apagada.

`index.html:6154` · alta · achado por: Importar e exportar, Runas e habilidades · **passou pelos céticos**

**Como quebra:** A lista da trilha primaria e POSICIONAL na leitura (textToBuild: i===0 vira assinatura, i===1 vira slots[0], etc.), mas a escrita compacta os vazios com .filter(Boolean). Passo a passo: na forja, abrir "escolher runas", escolher Precisao, clicar em "Pressione o Ataque" (assinatura), pular o Slot 1 e clicar em "Lenda: Espontaneidade" (Slot 2) e "Golpe de Misericordia" (Slot 3) — o editor permite isso, cada fileira e independente (escolherRuna, linha ~7971). Builds -> Exportar/importar -> "Copiar esta build": sai "RUNAS: Precisao > Pressione o Ataque | Lenda: Espontaneidade | Golpe de Misericordia" (tres nomes para quatro posicoes). Colar esse mesmo texto em "Importar como nova build": a leitura poe "Lenda: Espontaneidade" em slots[0] (Slot 1) e "Golpe de Misericordia" em slots[1] (Slot 2); normRunas confere posicao por posicao (daSlot) e joga as duas fora. A build nova fica so com "Precisao" e nenhuma runa menor, e como acha() encontrou os ids, nada entra em result.unknown — a mensagem diz apenas "Importado: N categoria(s)...", sem um unico aviso. Se a assinatura tambem estiver vazia, a pagina inteira de runas evapora do mesmo jeito.

### 7. O link da build não leva runas nem habilidades, mas a mensagem promete a build inteira

**CONSERTADO na F13-T13 (23/09/2026).** Era pior que o achado: o link também deixava de fora o **layout** e o **Mestre Forjador**. Os quatro entram como campos opcionais (`r`, `h`, `l`, `x`) — link antigo, sem eles, continua abrindo igual. O link cresce ~300 caracteres com a página de runas cheia e as 18 habilidades.

`index.html:6287` · alta · achado por: Runas e habilidades · **passou pelos céticos**

**Como quebra:** 1) Monte uma build com runas e ordem de habilidades. 2) Clique em "Copiar link" (botão link-btn na forja, ou o botão Link no detalhe da lista) — a placa diz "Link copiado — quem abrir recebe esta build na biblioteca". 3) Abra o link em outra aba/navegador: chega nome, modo, campeão, marcadores, descrição, layout e caixas, mas a página de runas e a ordem de habilidades vêm vazias. linkParaBuild (linha 6297) e receberBuildDoLink (linha 6315) também não têm campo para elas, então normRunas(undefined) devolve a página vazia. É o único caminho de exportação que ficou para trás: o texto (linhasDeRunas, linha 6148) e a publicação (p_runas/p_habilidades, linha 6393) levam os dois.

### 8. Com Reembolso ligado a eficiência troca de base e cai: o desconto faz o item parecer pior

`index.html:10023` · alta · achado por: Catalogo, filtros e numeros · **passou pelos céticos**

**Como quebra:** O catálogo traz dois números diferentes: `efficiencyBase` (que em 21 itens já inclui passivas) e `goldValueTotal` (só os atributos). Sem Reembolso o app mostra o primeiro; com Reembolso troca para goldValueTotal/netGold — outra base, não só outro preço. Passo a passo: 1) Entrar na loja, buscar "Limite da Razão"; 2) abrir o pergaminho (clique no ícone) — a linha "Eficiência" diz "118,99% (base, incluindo Duelo)"; 3) fechar, Filtros > Runas > marcar "Aplicar Reembolso aos preços" (preço cai de 2.800g para 2.590g); 4) reabrir o pergaminho: agora, logo abaixo do 118,99%, aparece "Com Reembolso 91,0% (2.356,67g ÷ 2.590g)". Um desconto de 210g derrubou a eficiência em 28 pontos, porque o numerador perdeu o Duelo (3.331,67g virou 2.356,67g). O valor coerente seria 3.331,67 ÷ 2.590 = 128,6%. Acontece em 9 itens (Limite da Razão −28,0; Terminus −16,5; Lâmina da Fúria de Guinsoo −15,5; Dente de Na'Shor; Armadura Sangrenta do Suserano; Acerto de Contas de Atma; Aurônucleo; Manamune; Armadura de Warmog). Efeito colateral: com a ordenação "Eficiência de ouro" esses itens despencam na lista, e o filtro Eficiência de ouro joga Limite da Razão da faixa "100% a 119%" para "80% a 99%" só por ligar o Reembolso.


## Gravidade média

### 9. "Leitura calma" não aumenta praticamente nenhum texto: o app inteiro usa font-size em px

**CONSERTADO na F13-T10 (22/09/2026).** Ver o registro da T10 no CHECKPOINT.

`index.html:2959` · media · achado por: CSS e acessibilidade · **passou pelos céticos**

**Como quebra:** Entrar na loja → botão "A" (Acessibilidade) → marcar "Leitura calma" (o rótulo promete "texto maior"). O interruptor sobe a fonte-base do body de 16px para 17px, mas o index.html tem 364 declarações de font-size em px e ZERO em em/rem — a única exceção é a que o próprio bloco cria na linha 2960 (`body.ac-leitura .card-name { font-size: 1.05em; }`). Resultado: só o nome do item no card do Catálogo cresce (16px → ~17,85px). O nome em inglês (12px, linha 3015), os atributos (13px, linha 3029), o preço (14px, linha 3019), o painel de filtros, o balão do item, a forja inteira, a lista de Builds, as Runas e a Calculadora ficam exatamente do mesmo tamanho. Pior: basta trocar a vista para "só nomes" e nem o nome cresce, porque `body.names-only .card:not(.full) .card-name { font-size: 14.5px; }` (linha 3389) tem especificidade maior (0,4,1) que a regra do interruptor (0,2,1). Quem ligou o ajuste na aba Build não vê uma letra a mais em lugar nenhum.

### 10. "Menos brilho" não apaga o fundo em brasa da forja, que é o item citado no próprio rótulo

**CONSERTADO na F13-T10 (22/09/2026).** Ver o registro da T10 no CHECKPOINT.

`index.html:3601` · media · achado por: CSS e acessibilidade · **passou pelos céticos**

**Como quebra:** Entrar na loja → "A" → marcar "Menos brilho" (rótulo, linha 4705: "tira os halos, o reflexo do card e o fundo em brasa") → aba Builds → abrir uma build na forja. O bloco inteiro do interruptor vive nas linhas 2944-2956 e só toca em `.card-sheen`, `.card-burst`, box-shadow de `.card-surface/.build-cat/.runa/.trilha-btn/.class-tab`, text-shadow dos cards de região e o filter de `.bh-cel.marcada`. Não existe nenhuma regra `body.ac-brilho` para `body.forja` — o gradiente laranja de brasa no rodapé da tela continua aceso igual. Junto com ele sobram, sem cobertura nenhuma, o `box-shadow: 0 0 10px 2px var(--forja-brasa-glow)` da barra de lote (linha 4289), o glow do `.lay-dot` (4570), o `0 0 12px var(--forja-brasa-glow)` do botão primário (3688), o do interruptor ligado (3870) e o da aba ativa (3617). O interruptor limpa o Catálogo e deixa a forja intacta.

### 11. O botão "Buscar de novo no servidor" fica visível na aba Minhas: o hidden perde para o display do .btn

`index.html:4836` · media · achado por: CSS e acessibilidade · **passou pelos céticos**

**Como quebra:** Entrar na loja → aba Builds. A tela abre em "Minhas", e o botão de recarregar (ícone de refresh) aparece ao lado do campo de busca, apesar do atributo `hidden` no HTML. Motivo: `.btn { display: inline-flex; }` (linha 793) é regra de autor e ganha do `[hidden]` da folha do navegador. O `<select id="bi-qtd">` logo ao lado, que também tem `hidden`, some corretamente porque `.build-select` (linha 909) não declara display — então a dupla aparece quebrada, com o botão sozinho. A correção que já existe para esse mesmo problema, `.bi-lote-bar [hidden] { display: none; }` na linha 4288 (com o comentário "o hidden dos botões tem de ganhar do display do .btn"), só vale dentro de `.bi-lote-bar`, e o #bi-refresh está em `.bi-actions` (linha 4812). Clicando nele em "Minhas", `carregarPublicas(true)` (linha 9245) dispara um GET em builds_publicas no Supabase e `renderBuildIndex` retorna na linha 8927 sem usar nada disso — requisição ao servidor e zero retorno na tela. A linha 9239 (`qtd.hidden = refresh.hidden = biView !== "publicas"`) nunca surte efeito nenhum sobre o botão.

### 12. O "Fechar" aparece durante "Publicando a build — Aguarde", e discorda do clique no fundo do diálogo

`index.html:5046` · media · achado por: CSS e acessibilidade · **passou pelos céticos**

**Como quebra:** Com data/servidor.js preenchido: forja → publicar uma build. `publicarBuild` chama `mostrarPub("Publicando a build", "Aguarde")` sem estado (linha 6386), e `mostrarPub` faz `pub-foot.hidden = true` (linha 6369) exatamente para esconder o botão enquanto a requisição corre. Só que `.md-foot-3 { display: flex; ... }` (linha 4479) é regra de autor e ganha do `[hidden]` do navegador — o "Fechar" fica na tela durante toda a espera. E os dois caminhos de fechar discordam: clicar no fundo escuro do diálogo é corretamente bloqueado, porque o handler da linha 9503 testa a PROPRIEDADE `!document.getElementById("pub-foot").hidden`, que é `true`; clicar no botão visível chama `fecharPub()` (linha 9502) e fecha a placa de aguarde. Aí, quando a requisição termina, `mostrarPub(...)` reabre o diálogo sozinho e a placa pisca de volta na cara do usuário. O mesmo vale para "Tirando do site" (linha 6437) e "Excluindo do site" (linha 6454).

### 13. "Última atualização" pula para agora só de trocar de build depois de recarregar a página

`index.html:5748` · media · achado por: Estado da build, Persistencia no navegador · **passou pelos céticos**

**Como quebra:** 1) Publique a build A — o resumo dela na lista diz "Publicada na versão 1"; 2) recarregue a página (F5); 3) na forja, abra o seletor de nome no topo e escolha a build B, sem mexer em nada; 4) volte para a lista e selecione a A. "Última atualização" agora é a hora de agora e a nota virou "Há alterações depois da última publicação (versão 1)", convidando a republicar uma build que ninguém tocou. O que acontece: trocar de build chama gravarBuild() para a A, e a comparação é feita com JSON.stringify de dois objetos montados em ordens de chave diferentes — o de loadBuild (linhas 5857-5874: id, name, seq, mode, ..., patch, revisao, layout, cats) contra o de snapshotActive (linha 5647: id, name, cats, patch, revisao, temp, pubOrigem, layout, seq, ...), que ainda tem `temp` e `pubOrigem` a mais e normaliza `runas`, gravado cru na linha 5867. As strings nunca batem, o `if` sempre dá "mudou" e carimba Date.now(). Da segunda gravação em diante as duas pontas já são snapshots e a comparação volta a funcionar — o código só acerta por acidente, e o comentário logo acima promete justamente o contrário ("não ao só trocar de build").

### 14. Salvar anuncia "salvo", desabilita o botão e desarma o aviso de saída mesmo quando o localStorage recusou a gravação

`index.html:5758` · media · achado por: Persistencia no navegador · **passou pelos céticos**

**Como quebra:** gravarBuild() zera `rascunho.sujo` na linha 5739, ANTES do try, e engole qualquer falha do setItem no catch da linha 5758 sem devolver nada a quem chamou. salvarAgora() (linha 5770) então chama Som.play("build:save") e refletirSalvar("salvo") (linha 5775) incondicionalmente. Passo a passo: (1) Abra o app num navegador em que a escrita no localStorage lança — Firefox com "Bloquear cookies: Todos" para esse site, ou uma aba com dados de site bloqueados; no GitHub Pages isso é uma opção de um clique no cadeado. (2) Monte uma build inteira na forja com o Editar ligado: caixas, itens, observações, runas. O status mostra "alterações não salvas" o tempo todo, então nada parece estranho. (3) Clique em Salvar (ou Ctrl+S). O som de forja toca, o botão Salvar fica desabilitado, o botão Descartar some e o status escreve "salvo". (4) O `beforeunload` da linha 5805 só avisa quando `rascunho.sujo` é true — e ele já foi zerado — então fechar a aba não pergunta nada. (5) Reabra o app: a build inteira não existe. O app afirmou que salvou, tirou o único aviso que protegia o trabalho, e o erro que o usuário precisava ver morreu no catch.

### 15. Excluir a última build própria com uma pública aberta grava builds:[] e faz a build do formato antigo (lol-build-v2) ressuscitar

`index.html:5986` · media · achado por: Persistencia no navegador · **passou pelos céticos**

**Como quebra:** A guarda "sempre sobra pelo menos uma build" conta as builds temporárias de visualização, mas a gravação (linha 5754) as descarta: `builds: library.builds.filter(b => !b.temp)`. Passo a passo: (1) Leo tem exatamente UMA build salva. (2) Vai em Build > lista > aba Públicas e dá duplo clique numa build publicada para olhar; abrirPublicaTemporaria (linha 8751) empurra `{id:"tmp:…", temp:true}` para library.builds, que agora tem 2 entradas. (3) Volta em "Minhas", seleciona a build dele e clica Excluir — o botão está habilitado porque library.builds.length é 2 (linhas 9022 e 9173). (4) deleteBuild filtra a build fora; library.builds = [tmp], length 1, então esta guarda NÃO dispara e nenhuma build nova é criada; gravarBuild() grava `{"builds":[], "activeId":"tmp:…"}`. (5) Leo recarrega a página. Em loadBuild a condição `d.builds.length` (linha 5846) é 0, o bloco inteiro é pulado e a execução cai na migração do formato anterior (linha 5884). (6) Como não existe um único `removeItem` no arquivo, a chave `lol-build-v2` nunca foi apagada desde a migração da Fase 0 — a build velha do HTML anterior volta para a biblioteca como se fosse dele, com nome e caixas antigos. Se a chave antiga não existir, o efeito é outro, mas ainda errado: a biblioteca volta vazia e initBuildBuilder (linha 9459) inventa uma build em branco sem nome.

### 16. Fragmento do Slot 2 volta no Slot 1 e o do Slot 3 e acusado de "nao encontrado no catalogo"

**CONSERTADO na F13-T12 (22/09/2026).** Vaga vazia sai como `-`; a primária é lida pelo slot de cada runa; fragmentos sem os `-` (texto antigo) procuram a primeira distribuição em que cada nome cabe no seu grupo. De brinde: página só com fragmentos deixou de ser apagada.

`index.html:6158` · media · achado por: Importar e exportar · **passou pelos céticos**

**Como quebra:** Mesmo defeito da linha de cima, mas aqui o resultado e um valor ERRADO na tela, nao so a perda. Os tres grupos de fragmento compartilham ids (data/runas.js: "forca-adaptativa" esta no Slot 1 e no Slot 2; "escalamento-de-vida" esta no Slot 2 e no Slot 3). Passo a passo: na pagina de runas, nao escolher nada no "Fragmento - Slot 1", clicar em "Forca Adaptativa" no Slot 2 e em "Vida" no Slot 3. "Copiar esta build" gera "FRAGMENTOS: Forca Adaptativa | Vida" (dois nomes para tres posicoes). Colar em "Importar como nova build": o leitor e posicional por indice (linha 6580, `const f = (RUNAS.fragmentos || [])[i]`), procura "Forca Adaptativa" no grupo 0 — acha, porque o id se repete — e grava no Slot 1; depois procura "Vida" no grupo 1, nao acha, e empurra para result.unknown. A build importada mostra a Forca Adaptativa no slot errado, perde a Vida, e a mensagem acusa "1 nome(s) nao encontrado(s) no catalogo: Vida" — uma runa que existe.

### 17. Observacao com quebra de linha (Shift+Enter) perde as linhas seguintes, ou reescreve a descricao da caixa

`index.html:6189` · media · achado por: Importar e exportar · **passou pelos céticos**

**Como quebra:** O editor de observacao e um <textarea> e o proprio codigo anuncia "Enter salva, Shift+Enter quebra linha" (comentario da linha 7639); closeNoteEditor so faz .trim(), entao o \n do meio fica gravado. O formato texto, porem, e uma linha por item. Passo a passo: na forja com Editar ligado, abrir a observacao de "A Coletora", digitar "segurar ate os 20 min", Shift+Enter, "trocar por Lembranca Mortal contra cura", Enter para salvar. "Copiar esta build" gera duas linhas fisicas para um item so. Colar em "Importar como nova build": a segunda linha nao casa com nenhum cabecalho nem com /^[-.*]/, cai em result.ignored++ e some calada — a observacao da build nova fica so com a primeira linha, sem nenhum aviso. Pior se a segunda linha comecar com "#" (ex.: "#1 contra tanque"): ela vira `current.desc` e sobrescreve a descricao da caixa; comecando com "-", vira um item inexistente e produz um aviso falso de "nome nao encontrado no catalogo".

### 18. A grade de habilidades continua mostrando os ícones do campeão anterior depois de tirar o campeão

`index.html:8263` · media · achado por: Runas e habilidades · **passou pelos céticos**

**Como quebra:** 1) Na forja, com uma build que tenha pontos de habilidade, escolha um campeão (ex.: Ahri) e espere os ícones de Q/W/E/R aparecerem na grade. 2) Abra o seletor de campeão e escolha "Todos os campeões". setBuildChampion(null) chama renderBuildAll → renderBuildSummary, que desenha a grade ANTES (linha 7050, ainda com habArte da Ahri) e só depois chama carregarArteHabilidades, que apaga habArte e volta no `return` sem redesenhar. A grade fica com os ícones da Ahri ao lado do aviso "escolha um campeão para ver os ícones", e continua assim até algo mais disparar renderHabilidades. O mesmo vale ao trocar da build A (com campeão) para a build B (sem campeão) pela lista: a grade da B aparece com a arte do campeão da A. E no caminho sem internet (.catch da linha 8272, "sem internet: ficam as letras") também não ficam as letras: ficam os ícones do campeão antigo.

### 19. "Copiar como texto" de varias builds volta como uma build so na importacao

`index.html:8887` · media · achado por: Importar e exportar · **passou pelos céticos**

**Como quebra:** loteParaTexto diz no comentario que escreve "no mesmo formato de docs/formato_de_importacao.md", mas textToBuild so sabe ler UMA build. Passo a passo: aba Build -> lista -> "Selecionar" -> marcar tres builds -> "Copiar como texto". Colar o resultado em Exportar/importar -> "Importar como nova build". Cada `BUILD:` sobrescreve result.name (e MODO/CAMPEAO/DESCRICAO/LAYOUT idem), entao a build nova recebe o nome da ULTIMA; todas as caixas das tres builds se empilham na mesma build; os MARCADORES das tres entram na mesma fila e normMarkers corta nos tres primeiros; e a linha separadora "========..." cai no ramo `line.startsWith("=")` e vira o marco da ultima caixa da build anterior ("=" x39, porque o replace /^=\s*/ tira so o primeiro). A mensagem diz "Importado: N categoria(s), M item(ns)" sem nenhum aviso. De quebra, loteParaTexto nunca escreve MESTRE FORJADOR, RUNAS, RUNAS 2, FRAGMENTOS nem HABILIDADES — campos que o "Copiar esta build" individual escreve — entao quem usa o lote como backup perde runas, ordem de habilidades e item forjado.

### 20. "Menos movimento" não desliga a chuva de entrada — a animação que o próprio rótulo promete desligar

**CONSERTADO na F13-T10 (22/09/2026).** Ver o registro da T10 no CHECKPOINT.

`index.html:9069` · media · achado por: CSS e acessibilidade · **passou pelos céticos**

**Como quebra:** Entrar na loja → "A" → marcar "Menos movimento" (o rótulo diz: "desliga as animações e as transições — golpes, molduras, chuva e brasas") → ir para a aba Builds. `showBuildScreen("lista")` chama `chuvaDeEntrada(index)` (linha 8606), e essa função só consulta o matchMedia do sistema — nunca olha `body.ac-movimento`. Como a chuva é escrita quadro a quadro em `el.style.maskImage` por requestAnimationFrame (linhas 9078-9083), o `body.ac-movimento * { animation: none !important; transition: none !important; }` da linha 2935 não a alcança: não é animation nem transition, é estilo inline recalculado 60x por segundo. A tela de Builds passa 900 ms sendo revelada por 34 pingos que se abrem. Quem ligou o interruptor justamente por não ter o sistema configurado (o comentário da linha 2934 diz que é para esse caso) continua vendo a maior animação da tela. As outras três animações de JS estão cobertas (fxAcionar por `display:none` no .card-fx, playTierAnimation e o tilt pelas regras de animation/transform) — só a chuva escapa.

### 21. Importar uma build com rascunho aberto grava o rascunho na build antiga sem perguntar

`index.html:9421` · media · achado por: Estado da build · **passou pelos céticos**

**Como quebra:** 1) Na forja da build A, ligue Editar e arraste um item para uma caixa — aparece "alterações não salvas" e o botão Descartar; 2) sem salvar, abra o painel Importar/Exportar (ele fica na própria forja), cole o texto de outra build e clique em Importar. A build nova abre e o rascunho da A foi gravado de vez: o Descartar sumiu e o item indesejado ficou na A para sempre. Motivo: createNewBuild começa com gravarBuild(), que zera rascunho.sujo e espelha o estado ao vivo na biblioteca. Todos os outros caminhos de saída da forja passam por confirmarSaida e perguntam (new-build 9331, dup-build 9333, troca pelo seletor 9299, voltar para a lista 9229, desligar o Editar 9497); o import-btn é o único que não pergunta — e o import do Arsenal.json (linha 9405) tem o mesmo furo.

### 22. Esc para fechar um diálogo da forja também larga a caixa escolhida — o stopPropagation dos diálogos não alcança o listener de captura

`index.html:9575` · media · achado por: Eventos e redesenho · **passou pelos céticos**

**Como quebra:** Na forja, com Editar ligado, clique numa caixa para escolhê-la (a faixa "Forjando em X" acende). Dê duplo clique numa placa para abrir o editor de observação e, em vez de salvar, aperte Esc para cancelar. Este listener está na fase de CAPTURA, então roda antes de qualquer outro: o overlay do pergaminho não está aberto e build.selectedCatId está preenchido, então ele zera a escolha e chama renderBuild(). Só depois o keydown do próprio textarea (linha 7681) roda e fecha o editor. A observação é descartada (certo) e a caixa escolhida some junto (errado, e sem aviso). O próximo clique num item da bandeja não adiciona nada: pisca o aviso "Selecione a caixa e clique num item da lista". Acontece igual com o diálogo de marcador (linha 7033), com o menu de tipo da caixa (linha 8379) e com "Em qual caixa?" (linha 8204): os três chamam e.stopPropagation() para isolar o Esc, mas estão registrados no MESMO document deste listener — stopPropagation não segura irmão no mesmo nó (só stopImmediatePropagation seguraria), e contra fase de captura nem isso serviria. O guarda do #overlay mostra que o caso do pergaminho foi previsto; os outros diálogos não.

### 23. "Puxar da build ativa" na Calculadora soma as alternativas da Escolha 1 e as caixas Opcionais

`index.html:9783` · media · achado por: Catalogo, filtros e numeros · **passou pelos céticos**

**Como quebra:** Todo o resto da forja conta os itens por `itensContados(cat)` (numa "Escolha 1" só o primeiro conta; as demais são trocas para a MESMA vaga). `statsFromBuild` ignora isso e varre `cat.items` inteiro. Passo a passo: 1) Aba Builds > abrir uma build > ligar "Editar"; 2) criar uma caixa e mudar o tipo para "Escolha 1"; 3) marcar nela "Presságio de Randuin" (+350 Vida, +75 Armadura) e depois "Armadura de Espinhos" (+150 Vida, +75 Armadura); 4) a placa da caixa diz "Atributos do padrão (o de cima)" e o painel "Atributos da build" mostra +350 Vida, +75 Armadura — correto; 5) ir para a aba Calculadora e clicar em "Puxar da build ativa"; 6) os campos vêm com Vida total 500 e Armadura 150 — o dobro, somando um item que o usuário escolheu NÃO usar. O mesmo vale para caixas do tipo "Opcional", que o "Total (sem opcionais)" exclui de propósito. Daí para frente todo o veredito da calculadora (vida efetiva, ponto de equilíbrio, dano absorvido) sai calculado em cima de uma build que não existe.

### 24. Eficiência arredondada para exibição não bate com a faixa do filtro nem com o cabeçalho do grupo

`index.html:10008` · media · achado por: Catalogo, filtros e numeros · **passou pelos céticos**

**Como quebra:** O card exibe `fmtEff` (1 casa, arredondando) mas o filtro e o rótulo de grupo testam o número cru. "Joia da Ruína" tem efficiencyBase 99,995 e "Cetro Vampírico" 99,98. Passo a passo: 1) Catálogo > "Ordenar por" > "Eficiência de ouro" (maior primeiro); 2) buscar "Joia da Ruína" — o card mostra "Eficiência de ouro: 100,0%", mas o cabeçalho do grupo acima dele diz "Eficiência: 50 a 99%"; 3) limpar a busca, Filtros > Eficiência de ouro > marcar "100% a 119%"; 4) o contador do topo não inclui Joia da Ruína nem Cetro Vampírico — os dois itens que a tela acabou de anunciar como 100,0% somem da lista; 5) marcar "80% a 99%" e eles reaparecem, ainda exibindo "100,0%".

### 25. Ordenar por atributo lê só o primeiro atributo do item e mistura valor plano com porcentagem na mesma régua

`index.html:10034` · media · achado por: Catalogo, filtros e numeros · **passou pelos céticos**

**Como quebra:** No catálogo, "Penetração Mágica" aparece como `flat` em uns itens e `percent` em outros, e "Sapatos Enfeitiçados" tem as duas (+20 plana e +8%). Passo a passo: 1) Catálogo > Filtros > Atributo > marcar o chip "Penetração Mágica" (a lista fica com 7 itens); 2) clicar em "Maior primeiro"; 3) a ordem sai Cajado do Vazio (+40%), Criptoflora (+30%), Sapatos Enfeitiçados (+20), Chama Sombria (+15), Ápice da Tempestade (+15), Joia da Ruína (+13%), Sapatos do Feiticeiro (+12) — ou seja, 40% e 30% são tratados como "maiores" que 20 pontos planos, que é comparar coisas diferentes; 4) o card de Sapatos Enfeitiçados mostra "Penetração Mágica: +20" e esconde o +8% (o find() para no primeiro), e o filtro/ordenação nunca enxergam o segundo; 5) os cabeçalhos de faixa saem repetidos: "Penetração Mágica: 10 a 14%" (Joia da Ruína) e logo abaixo "Penetração Mágica: 10 a 14" (Sapatos do Feiticeiro), duas faixas com o mesmo intervalo na mesma lista. Mesmo problema em "Velocidade de Movimento" (65 planos x 10%).


## Gravidade baixa

### 26. O botão "Descartar" fica permanente ao lado do "Salvar", mesmo sem nada para descartar

`index.html:4895` · baixa · achado por: CSS e acessibilidade · **passou pelos céticos**

**Como quebra:** Forja → ligar o interruptor "Editar" sem mexer em nada. `body.editando .save-wrap { display: inline-flex; }` (linha 4471) revela a área de salvar, e o "Descartar" aparece junto — mesmo com `hidden` no HTML e com `refletirSalvar` fazendo `dis.hidden = !rascunho.sujo` (linha 5766) a cada mudança. De novo `.btn { display: inline-flex; }` (linha 793) ganha do `[hidden]` do navegador, então a linha 5766 nunca surte efeito nenhum e o botão é permanente. A tela fica se contradizendo: o "Salvar" ao lado está corretamente `disabled` e apagado (linha 5764 + `.btn:disabled { opacity: 0.4 }`), enquanto o "Descartar" está aceso, clicável e com o cursor de mão, oferecendo desfazer o que não existe. Clicando nele, `confirmarSaida(() => {})` (linha 5796) cai no `if (!rascunho.sujo) { depois(); return; }` da linha 5786 e não acontece absolutamente nada — nem diálogo, nem som, nem aviso.

### 27. Com duas abas abertas, a segunda a gravar apaga a build criada na primeira

`index.html:5753` · baixa · achado por: Persistencia no navegador · **passou pelos céticos**

**Como quebra:** gravarBuild() serializa o `library.builds` que a aba tem em memória desde o load e sobrescreve a chave inteira, sem reler o que está gravado e sem ouvinte de evento `storage` (não existe nenhum `addEventListener("storage")` no arquivo). Passo a passo: (1) Abra o index.html na aba 1 e o mesmo index.html na aba 2 (mesma origem — dois arquivos do disco, ou duas abas do GitHub Pages). As duas leem a mesma biblioteca, digamos com as builds A e B. (2) Na aba 1, clique em "Nova" na lista de builds, monte a build C e salve. O localStorage agora tem A, B e C. (3) Volte para a aba 2, que ainda só conhece A e B, e dê duplo clique em qualquer build da lista — activateBuild chama gravarBuild(), que grava `{builds:[A,B]}` por cima. (4) Recarregue qualquer uma das duas abas: a build C sumiu sem aviso nenhum, e não há como desfazer.

### 28. Qualquer "/" na descricao vira quebra de paragrafo ao importar de volta

`index.html:6587` · baixa · achado por: Importar e exportar · **passou pelos céticos**

**Como quebra:** A escrita troca quebra de linha por " / " (linha 6170, com espacos), mas a leitura aceita "/" colado. Passo a passo: na forja, escrever na descricao "Build de poke/sustain para a rota do meio" (um paragrafo so) e salvar. "Copiar esta build" gera "DESCRICAO: Build de poke/sustain para a rota do meio". Colar em "Importar como nova build": a descricao da build nova vira dois paragrafos, "Build de poke" e "sustain para a rota do meio", partidos no meio da palavra. Mesma coisa com "3/0", "AD/AP", "2/3 tanques". A descricao e o texto que aparece na lista de builds e no que e publicado.

### 29. Build publicada aberta em "só visualização" tem as runas editáveis pela aba Runas

`index.html:7992` · baixa · achado por: Runas e habilidades · **passou pelos céticos**

**Como quebra:** 1) Na lista de builds, aba "Publicadas", dê duplo clique numa build publicada que tenha runas: a forja abre com a placa "Só visualização. Esta é a build publicada ...; ela some quando a página recarrega e não pode ser editada" e o interruptor Editar se recusa a ligar (chamarEditarTemp). 2) A faixa de runas aparece com "9/9 · trocar"; clique nela. 3) Na aba Runas, em montar, clique em qualquer runa: escolherRuna → gravarPagina → saveBuild grava na hora (build.editing é falso numa build temp), a faixa muda para 8/9 e a página da build publicada passa a ser outra — sem o Editar nunca ter sido ligado. A grade de habilidades faz o certo no mesmo caso (linha 9546: `if (!build.editing) return;`); a tela de runas não tem guarda nenhuma. Se o Leo clicar em "Copiar e editar" logo em seguida, ele copia a versão alterada achando que é a publicada.

### 30. Descricao e layout importados ficam invisiveis na forja ate o proximo redesenho

`index.html:9423` · baixa · achado por: Importar e exportar · **passou pelos céticos**

**Como quebra:** createNewBuild ja rodou renderBuildAll() antes destas linhas, e depois delas o handler so chama gravarBuild() (que nao redesenha) e, condicionalmente, renderRunasDaForja()/renderHabilidades(). Passo a passo: colar em "Importar como nova build" um texto com "DESCRICAO: ..." e "LAYOUT: Trilha por fases", sem "MESTRE FORJADOR:" e sem "CAMPEAO:" (as duas unicas ramificacoes que chamam renderBuildAll() depois). A build nova e gravada certa, mas a tela continua mostrando o campo de descricao vazio e o seletor marcando "Tabuleiro", e o canvas segue no tabuleiro em vez da trilha — o usuario conclui que essas duas linhas foram ignoradas. Sair para a lista de builds e voltar faz os valores aparecerem.

### 31. "Puxar da build ativa" zera a Vida digitada para 1 quando os itens não dão vida

`index.html:9827` · baixa · achado por: Catalogo, filtros e numeros · **passou pelos céticos**

**Como quebra:** O comentário diz que a vida atual é o piso; o código usa 1 como piso e descarta o que o usuário digitou. Passo a passo: 1) Aba Calculadora, deixar "Vida total" no padrão 2000; 2) na aba Builds, montar uma build só com itens sem Vida — por exemplo "Cota de Malha" (+40 Armadura, nada de vida); 3) voltar à Calculadora e clicar em "Puxar da build ativa"; 4) o campo "Vida total" vira 1; 5) os dois cartões passam a dizer "Vida efetiva 1", "Equilíbrio para 1 de vida: 0 de armadura" e "Sobra armadura: 40 pontos além do equilíbrio" — e o 2000 que estava lá foi perdido, sem desfazer.

### 32. A contagem do seletor "Ordenar pelo atributo" conta ocorrências, não itens

`index.html:9990` · baixa · achado por: Catalogo, filtros e numeros · **passou pelos céticos**

**Como quebra:** "Sapatos Enfeitiçados" tem duas entradas de "Penetração Mágica" (+20 plana e +8%), então o item é contado duas vezes. Passo a passo: 1) Catálogo > "Ordenar por" > "Maior valor do atributo" para o seletor "Ordenar pelo atributo:" aparecer; 2) abrir esse seletor e ler a opção "Penetração Mágica (8 itens)"; 3) Filtros > Atributo > marcar o chip "Penetração Mágica"; 4) o contador do topo diz "7 de 225 itens". O rótulo promete 8, a lista entrega 7.

### 33. fmtG corta o preço com Reembolso em 1 casa e mostra um valor que não existe no catálogo

`index.html:10459` · baixa · achado por: Catalogo, filtros e numeros · **passou pelos céticos**

**Como quebra:** O comentário assume que "o Reembolso deixa meio ouro", mas 17 dos 109 itens com cashback têm quarto de ouro (netGold 2.543,75) e um tem centavos (Força da Trindade, 3.083,03). Passo a passo: 1) Catálogo > Filtros > Runas > marcar "Aplicar Reembolso aos preços"; 2) buscar "Arco do Axioma"; 3) o card mostra o preço "2.543,8g" — número que o catálogo não tem; 4) abrir o pergaminho do mesmo item: a linha "Com Reembolso" imprime "(3.465g ÷ 2.543,75g)", usando `toLocaleString` sem limite de casas. As duas telas mostram preços diferentes para o mesmo campo `cashback.netGold`. O mesmo arredondamento entra em `catTotal`/`buildTotal`, então a soma da caixa na forja também não fecha com a soma dos preços impressos nos itens.


## Fora da varredura — apontado pelo crítico de cobertura, NÃO verificado

> **Ponto 2 (Ápice) conferido na F13-T9, 22/09/2026.** Os cinco exemplos do crítico estavam **errados**: Cinzas do Destino, Cota de Malha, Códex Demoníaco e Cinto do Gigante têm Ápice "igual ao base" no catálogo e o app não mexe neles; as Cinzas nem têm os 80 de PdH citados (têm 30). Só o Elixir da Força se sustentava. Mas passando o leitor em **todos** os 102 itens com Ápice, o problema era real e maior, em outros itens: 9 deles tinham o número do item apagado ou trocado por um menor — Tocha de Chamas Negras (perdia os +80 de PdH por "+20%"), Couraça Protoplasmática (600 → 241 de Vida), Aproximação Invernal (550 → 129 de Vida), Tiara Sussurrante, Jak'Sho, Ímpeto Cósmico, Couraça do Defunto, Trenó do Solstício e Elixir da Força (somava as duas pontas de um "ou"). **Consertado**: o número do Ápice só substitui o do item quando é da mesma grandeza e maior, e alternativas com "ou" não entram. Os outros 93 ficaram iguais. **Continua errado**: Acerto de Contas de Atma mostra 30% de crítico, e o texto diz "50% no total" — só o Ápice estruturado no Capítulo 1 resolve sem adivinhar.

Um último agente leu a lista acima e disse o que nenhum dos oito subsistemas cobriu. Esses pontos não passaram pelos céticos: tratar como pista, não como bug.

Cinco pontos que nenhum dos oito leitores cobriu. Todas as linhas se referem a `C:\Users\user\3D Objects\Captulo 2\montador_de_itens_lol\index.html`. Os casos marcados como conferidos foram lidos no código e no `data/catalog.js`. Os outros são o tipo de bug que tende a aparecer ali.

1. **Módulo `Som` e as falas do lojista (linhas 5285–5460), nenhuma das oito áreas cobre.**
   - **Conferido:** `setMudo` e `setCanal` só gravam o estado e avisam os ouvintes. O único ouvinte é o `refletirSom` (linha 11359), que atualiza a interface. Nada chama `.pause()`. Cenário: o Leo põe um Lendário na build, o lojista começa a falar, o Leo aperta mudo ou desliga o canal "lojista", e a fala continua até o fim.
   - **Provável:** em `tocar`, uma fala do lojista põe `falaLivreEm = Infinity`, e só os eventos `ended` e `error` liberam de novo. `precarregar()` carrega todos os arquivos na hora de destravar. Se um arquivo falhar ali (rede instável no Pages), o `error` dispara antes de existir o listener. Quando essa fala for sorteada, `play()` é rejeitado sem novo `error`, e o lojista fica mudo pelo resto da sessão sem aviso.
   - Os links diretos (`#b=` e outros) chamam `entrarNaLoja(true)` → `Som.destravar()` sem clique do usuário (linha 11378).

2. **O Ápice vira número nos totais: `apexStatsOf` (10062), `apexAttributes` (10084) → `effectiveAttributes` (6725) → `sumAttributes` / `renderBuildTotals` (6799).** O leitor do Catálogo não reportou nada do Ápice. Conferido com o texto real do catálogo:
   - **Cinzas do Destino:** o texto do Ápice diz "+20% de Poder de Habilidade". Como a unidade é diferente da do item, `apexAttributes` troca o "+80 de Poder de Habilidade" por "+20%". Com o Ápice ligado, a build perde 80 de Poder de Habilidade.
   - **Elixir da Força:** o texto diz "+15 de Dano de Ataque ou +25 de Poder de Habilidade". O parser soma os dois.
   - **Cinto do Gigante:** o texto diz "+30% … (50% no total)". O app mostra 30%.
   - **Cota de Malha e Códex Demoníaco:** o "+20 de Velocidade de Movimento" temporário substitui os "+4% de Velocidade de Movimento" do item.
   - **Ápice por cima do Mestre Forjador:** quando os dois mexem no mesmo atributo, o valor do Ápice apaga o total do Mestre Forjador.

3. **A ponte Catálogo → Forja sem trava de "só visualização": `toggleItemInBuild` (10918), clique do card (10711), `initPerguntarCaixa` (8177).** Conferido:
   - Nenhum desses trechos confere `build.temp`.
   - Cenário: abrir uma build pública em "Ver", ir ao Catálogo, clicar num item, escolher uma caixa em "em qual caixa?". O item entra na build que "não pode ser editada". Clicar num item que já está nela o remove sem pergunta.
   - O botão "nova caixa" chama `window.ligarEdicao(true)`, que é o `applyEditing` direto. Isso contorna a trava do interruptor (linha 9496) e liga o Editar numa build temporária.
   - Como `gravarBuild` filtra `temp`, tudo some ao recarregar, calado.

4. **Arrastar e redimensionar: `initCategoryDrag` (7334), `initPicker` (7529), `initCategoryResize` (7472), `moveItem` (6097).** Conferido:
   - O `dragend` só existe no `#build-canvas` (linha 7370). O `#picker-list` fica fora dele (linhas 4986 e 4995).
   - Cenário: arrastar um item do seletor e soltar fora de uma caixa (ou cancelar com Esc). O `dragItemPayload = {from:"picker"}` fica guardado.
   - Depois, arrastar qualquer coisa de fora (texto selecionado, arquivo da área de trabalho) para uma caixa em modo Editar: o `drop` adiciona o item velho.
   - No redimensionar, `left` e `top` são gravados no `mousedown`. Rolar a página durante o arraste do canto deixa a conta de colunas e linhas errada.

5. **A ficha com Shift e o hover nos cards: `applyFullCard` / `initShiftFullCard` (10988–11053) e o efeito de hover (11055–11268).**
   - O card guarda `hoveredCard` como referência ao elemento, e o `render()` recria todos os cards (linhas 10865 e 10880). Depois de trocar Ápice ou Reembolso com o mouse parado, a referência aponta para um card que saiu da tela. A ficha só volta quando o mouse sai e entra de novo.
   - O Ápice ligado pelo Catálogo chama `render()`, mas não `renderBuildAll()`. O Reembolso chama os dois (linhas 10174–10193). Os totais da forja ficam velhos até o próximo redesenho.
   - Tipo de bug: estado de hover preso a elemento velho e duas telas que discordam depois de um interruptor.

## Achado depois da caçada

### 34. A forja em 1280×800 rola de lado quando a build tem o Biscoito Total da Determinação Eterna

**CONSERTADO na F13-T11 (22/09/2026).** A faixa "Atributos da build" passa a deixar o atributo quebrar, como a placa da caixa já fazia. Em fila com quebra, o atributo curto desce inteiro para a linha de baixo; só o que é mais largo que a faixa quebra por dentro — conferido que nenhum atributo curto se parte, em 1280 e 1920.

`index.html:6891` (`statsListHtml` na faixa "Atributos da build") · média · achado na F13-T10 · **REPRODUZIDO**

O atributo do Biscoito no catálogo é uma frase longa ("+30 Vida máxima permanente por biscoito consumido ou vendido (tooltip do cliente, captura do usuário em 12/09/2026: …)"), e a faixa de atributos da build desenha cada atributo sem quebra de linha: um `span` de 1.415px deixa a página com 1.478px numa janela de 1.280. O roteiro de QA não pegou porque a build dele não tem o Biscoito. Conserto no app é deixar o atributo quebrar; o texto do atributo em si é do Capítulo 1.

