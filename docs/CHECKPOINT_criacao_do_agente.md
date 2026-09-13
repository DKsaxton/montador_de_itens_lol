# Checkpoint — Agente "Catálogo de Itens LoL" (Capítulo 1)
Última atualização: 12/09/2026 — Capítulo 1 concluído pelo agente; Capítulo 2 iniciado (Lote 0 feito)

## 1. Objetivo geral
**Fase atual — Capítulo 2:** criar o agente (Claude Code) que evolui o build workshop HTML: atualizar dados para o catálogo novo (225 itens, patch 16.18.1), melhorar a UI e adicionar features (Ornn, Cash Back, Ápice, filtros por classe/dano/custo/atributo, etc.).

**Fase concluída — Capítulo 1:** Criar um agente (Projeto do Claude) que gere o Capítulo 1: catalogação .md completa e fiel ao patch atual dos itens de LoL (PC) em Ranqueada/SR, ARAM e ARAM: Mayhem, com scalings, condições, build path, custo, eficiência, região, Mestre Forjador, Cash Back e estado Ápice. Alimenta o Capítulo 2 (build workshop HTML, agente separado).

## 2. Concluído
- Rascunho `Untitled-3.md` lido; triagem: agente de prompt simples, com busca web obrigatória.
- Plataforma definida: Projeto do Claude. Textos PT-BR: oficiais (agente busca).
- Diagnóstico da 1ª tentativa (`Catalogo_Itens_LoL.md`, 219 blocos): formato por item é bom e reaproveitável; falhas foram de processo (modos fora do escopo: Nexus Blitz/Arena em 110+ itens; renomeações silenciosas de 9 itens da lista piloto; Guardião/ARAM a confirmar; sem campos Análise de custo e Ápice).
- `Guia de Campos` e `CLASSES DE ITENS` da 1ª tentativa avaliados: reaproveitáveis como Project knowledge, com revisão (v2).
- Fonte PT-BR encontrada: Data Dragon (Riot) tem `item.json` em pt_BR = nomes/descrições oficiais do cliente. Wiki pt-br da Fandom está desatualizada (ainda cita Míticos) — proibir.

## 3. Em andamento
Nada — Forjador finalizado e aprovado; o trabalho continua no Claude Code.

## 4. Próximos passos
1. (Usuário) Copiar Forjador_montador_de_itens_lol/ por cima do clone do repositório; copiar 84 mp3 e 3 texturas; ativar o GitHub Pages; abrir o Claude Code na pasta e mandar "Leia o CHECKPOINT e execute a próxima tarefa."
2. (Usuário) Corrigir no Capítulo 1, quando quiser, as 3 pendências de integridade que o Forjador vai reportar na Fase 0.

## 5. Decisões tomadas
- Cap. 2: animações de clique por tier (áudio tem eixo por núcleo para hover/clique, por tier para Lendários e por item para falas raras). Escopo = só os 225 itens do Cap. 1; itens removidos/novos proibidos; sem Cap. 3.
- Cap. 2: publicação via GitHub Pages no repositório existente DKsaxton/montador_de_itens_lol (branch main, raiz, .nojekyll). Regras derivadas para o agente: caminhos relativos, nomes de arquivo case-sensitive, áudio destravado por clique inicial (tela "Entrar na loja").
- Cap. 2: plataforma Claude Code (pasta do projeto + CLAUDE.md). Estrutura: index.html + assets/audio + assets/textures + data/catalog.js (JS, não JSON, para abrir via file://). Sons por núcleo mapeados via itemClass.core. Sem recomendação por campeão.
- Cap. 2: ícones por URL do Data Dragon pelo ID (decisão do usuário). Plataforma recomendada: Claude Code (arquivos reais, Git, captura de tela, assets de áudio); entrega vira CLAUDE.md + pasta.
- Cap. 2: esquema do catalog.json é superconjunto do CATALOG antigo para o HTML existente não quebrar.
- Cap. 2: Claude Code (arquivos reais + Git, captura de tela para aprovar UI); entrega em formato CLAUDE.md. Ícones por URL do Data Dragon (sem base64). HTML anterior (index.html, 1,95 MB, JS puro, 3 telas, JSON `CATALOG` embutido) é a base — UI e features agradam, UI a melhorar.
- Cap. 1 fechado pelo agente em 12/09: 225 itens/16 lotes, Opus 5, 1 pendência (lentidão do Garrabrasa 2s vs 3s).
- Listas reconstruídas por pedido de máxima variedade: Categoria de Atributo v3 (28) e Efeitos Especiais v3 (62), ancoradas nas tags do Data Dragon + palavras-chave pt_BR; regra de extensão via Divergências. Classes v2 e exemplos atualizados.
- 2ª simulação (Pistola Laminar, Bastão das Eras, Húbris) revelou: placeholder "0" no Data Dragon (regra adicionada), brasão Blessed Isles → Shadow Isles (Guia), Efeitos Especiais ganha "Cura" e "Restauração de Mana" (28 valores). Classe por soma de ouro decidiu os 3 casos (Pistola → AP por 1.600 vs 1.400).
- Assumido salvo objeção: nomes dos núcleos AD / Vitalidade / AP; Aceleração de Habilidade em "Depende".
- Novo campo Classe (núcleo único AD/Vitalidade/AP, inspirado em Deadlock): decidido pela soma de ouro da Análise de custo, desempates por tipo de dano → utilidade → [A CONFIRMAR]. Aceleração de Habilidade movida para "Depende" (proposta, aguardando ok). CLASSES_DE_ITENS_v2 substitui o esboço.
- Regra global: ARAM confirmado ⇒ ARAM: Mayhem também (mesma loja); Notas de Mayhem só com diferença explícita.
- "Movimento" vira o 6º valor de uso duplo (Categoria se permanente, Efeitos Especiais se condicional); Efeitos Especiais passa a 26 valores. Exemplo do Quebrapassos atualizado.
- Modelo registrado no cabeçalho de cada lote (Patch · Modelo); recomendação: modelo mais forte do plano para Épicos/Lendários, mesmo modelo dentro do lote.
- Contexto aprovado. ARAM/Mayhem como Notas no bloco do item base (229 blocos, não 600).
- Novo campo Ícone (URL Data Dragon por ID) e campo Fontes (URLs abertas + patch) no template — para o Cap. 2 e como trava anti-memória.
- Tarefa aprovada sem alterações (sublotes de Lendários ~15). Agente só executa, sem explicações.
- Stats de referência (proposta revisada, usuário achou 400 PdH/100 Arm alto): Vida 2000 (600 bônus), DdA 100 (40 bônus), PdH 200, Armadura 70 (30 bônus), RM 50 (20 bônus), Mana 1000 (500 bônus), nível 13 — assumido salvo objeção.
- Lote 0 feito nesta conversa em vez de pelo agente (usuário quis a mise-en-place pronta). Na Tarefa do agente, o Lote 0 vira uma checagem rápida de patch (versions.json) + confirmação de que a v2 ainda bate, em vez de reconciliação completa.
- Inclusões aprovadas: Ardent Censer, Spirit Visage, Heartsteel, 4 Guardião, Atma's Reckoning, Stat Bonus, Shattered Armguard (os 7 últimos com tier/modo a confirmar na wiki no Lote 1). Excluído: Cappa Juice.
- Fonte do Data Dragon usada aqui: espelho GitHub noxelisdev/LoL_DDragon (`latest/data/<lang>/item.json`), porque ddragon.leagueoflegends.com está bloqueado no sandbox. O agente final usa o CDN oficial da Riot.
- Filtro de itens: IDs < 10000, mapas 11/12, sem requiredChampion/requiredAlly; IDs 77xxxx (legado), 22xxxx (Arena) ignorados; 12xxxx = variantes ARAM anotadas.
- Perfil aprovado sem alterações (11/09). Lote 0 obrigatório: reconciliação da lista piloto via Data Dragon en_US + pt_BR (nomes oficiais, ID, mapas 11/12) antes de catalogar qualquer item; toda correção de nome só com aprovação.
- Dupla fonte (wiki EN + DDragon pt_BR) porque a wiki pt-br pública está desatualizada e o DDragon tem stats imprecisos — cada fonte cobre o que faz bem.
- Lista piloto como chave primária: o agente nunca renomeia; registra "nome na wiki: X" ao lado e sinaliza.
- Assumido (usuário pode corrigir): uso pessoal; scalings com fórmula bruta + exemplo com stats médios; "Apce" = Ápice.
- Modos de jogo limitados a SR (Ranqueada), ARAM, ARAM: Mayhem — qualquer outro modo é ignorado no campo.

## 6. Bloqueios / dúvidas em aberto
- Nenhum. (Lembrete operacional: ligar a busca web no Claude antes do Lote 1.)
