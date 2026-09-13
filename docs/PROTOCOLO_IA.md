# Protocolo de Contexto e Continuidade de Projeto

**Para a IA que estiver lendo este arquivo:** este documento define como você deve se comportar ao trabalhar neste projeto, com dois objetivos: (1) consumir o mínimo de tokens/contexto necessário e (2) garantir que o progresso do trabalho nunca se perca, mesmo que a sessão seja interrompida, o contexto se esgote, ou a conversa seja encerrada. Aplique estas regras por padrão, sem que seja necessário repeti-las a cada tarefa.

## Como usar este arquivo

Se esta é uma sessão nova e você está lendo este documento agora:
1. Procure, na mesma pasta/projeto, um arquivo chamado `CHECKPOINT.md`.
2. Se ele existir, leia-o por completo antes de fazer qualquer outra coisa — ele contém o estado real e atual do trabalho.
3. Se não existir, comece a criá-lo e mantê-lo a partir de agora, seguindo a Regra 3.

## Regra 1 — Consumir menos tokens/contexto

- Assuma um escopo razoável e execute a tarefa em vez de pedir esclarecimentos triviais; só pergunte quando a ambiguidade puder levar o trabalho na direção errada.
- Leia/processe apenas os trechos de arquivos, logs ou documentos relevantes à tarefa atual — não o conteúdo inteiro, quando for possível isolar a parte relevante.
- Não peça repetição de informações já registradas em `CHECKPOINT.md` ou em outros arquivos do projeto — leia-os diretamente.
- Em tarefas complexas, isole investigações pesadas (buscas extensas, leitura de muitos arquivos, execução de testes) do fluxo principal sempre que a ferramenta permitir, retornando apenas um resumo.
- Não use modos de raciocínio mais profundos/lentos do que a tarefa exige.
- Prefira ações e respostas específicas e acionáveis a explorações abertas e vagas.
- Corrija o rumo assim que perceber um erro de direção, em vez de continuar até o fim por um caminho já sabido errado.
- Mantenha instruções permanentes do projeto (convenções, padrões, preferências) em um arquivo de instruções persistente, mantendo-o enxuto — só o essencial.

## Regra 2 — Nunca perder o progresso

- Todo resultado relevante (código, texto, decisões) deve existir como arquivo real do projeto — nunca apenas dentro do texto da conversa.
- Se houver controle de versão disponível (Git), faça commits frequentes com mensagens descritivas: é a rede de segurança mais confiável que existe, mais permanente do que qualquer mecanismo interno de sessão.
- Mantenha o `CHECKPOINT.md` (Regra 3) sempre atualizado — é o que permite recomeçar em outra sessão, ou com outra IA, sem perder o fio da meada.

## Regra 3 — Protocolo de checkpoint (núcleo deste documento)

**Arquivo:** `CHECKPOINT.md`, na raiz do projeto (ou local equivalente já em uso).

**Quando atualizar, nesta ordem de prioridade:**
1. Imediatamente, se for solicitado algo como "checkpoint" ou "salve o progresso" — gatilho manual, sempre prioritário sobre os demais.
2. Ao concluir cada etapa ou subtarefa logicamente distinta.
3. Antes de qualquer ação arriscada, longa ou difícil de reverter.
4. Se a tarefa for objetivamente quantificável (ex.: "migrar 40 arquivos"), a cada ~10% das unidades concluídas.
5. Nunca estimar "% de progresso" em tarefas abertas ou qualitativas — nesses casos, usar apenas os gatilhos 1–3.

**Como atualizar:** sobrescrever o arquivo inteiro a cada checkpoint. Não duplicar nem acumular versões antigas dentro dele; resumir decisões passadas em vez de colá-las na íntegra.

**Estrutura obrigatória do conteúdo:**

```markdown
# Checkpoint — [nome do projeto/tarefa]
Última atualização: [data/hora ou identificador de sessão]

## 1. Objetivo geral
[o que se está tentando alcançar, em 1-3 frases]

## 2. Concluído
[o que já foi feito e validado]

## 3. Em andamento
[o que está sendo feito agora, e exatamente em que ponto parou]

## 4. Próximos passos
[lista ordenada do que falta fazer]

## 5. Decisões tomadas
[decisões relevantes e o motivo de cada uma]

## 6. Bloqueios / dúvidas em aberto
[o que impede avançar, ou o que precisa de confirmação humana]
```

## Regra 4 — Adaptação por ambiente

- **Com acesso a arquivos e Git:** registrar as Regras 1 e 3 num arquivo de instruções persistente do projeto (ex.: `CLAUDE.md` ou equivalente), para que valham automaticamente em toda sessão futura. Fazer commit do `CHECKPOINT.md` junto com o restante do trabalho a cada atualização relevante. Tratar qualquer mecanismo interno de resumo/compactação de contexto da própria ferramenta como complementar a este protocolo, nunca como substituto.
- **Interface de chat sem acesso a arquivos persistentes entre conversas:** gerar o `CHECKPOINT.md` como arquivo para download a cada atualização, e avisar para reanexá-lo no início de uma conversa nova (ou mantê-lo numa área de conhecimento persistente, se a interface oferecer isso).
- **Qualquer outro ambiente:** usar o mecanismo de armazenamento nativamente persistente disponível, mantendo o nome de arquivo e a estrutura de conteúdo acima para consistência entre ferramentas diferentes.

## Regra 5 — Prioridade

Se, durante a tarefa, uma instrução humana direta conflitar com este protocolo (por exemplo, pedir para não gerar um arquivo específico), essa instrução tem prioridade — este documento é um padrão default, não uma regra absoluta.

---

Mantenha este próprio arquivo enxuto: adicione apenas o que for realmente necessário para orientar o comportamento da IA, sem deixá-lo crescer sem controle.
