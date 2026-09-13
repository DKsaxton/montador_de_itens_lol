# Propostas de adição ao Capítulo 1

Dados que o app precisa em forma estruturada e que hoje só existem como texto no Catálogo. O Forjador não digita nenhum deles; até o Capítulo 1 fornecer, a tela mostra o texto como está.

## 1. Eficiência de ouro recalculada pelos interruptores (pedido do Leo, 13/09/2026)
Regra: eficiência = valor em ouro dos atributos ÷ preço pago. Cada interruptor muda um lado da conta.

| Interruptor | O que muda | O que o catálogo já tem em número | O que falta |
|---|---|---|---|
| Reembolso | preço → `cashback.netGold` | `costAnalysis.goldValueTotal`, `cashback.netGold` (120 itens) | nada — dá para calcular já |
| Mestre Forjador | valor em ouro sobe pelos atributos de `masterwork.stats` | `masterwork.stats[].bonus` por atributo (109 itens) | o valor em ouro do bônus: campo numérico `masterwork.bonusGoldTotal` (a regra "1.000g divididos igualmente" está só no texto `masterwork.raw`) ou `costAnalysis.parts[] = {stat, value, gold}` para valorar cada ponto |
| Ápice | atributos nos valores máximos | `apex` (texto; 102 itens com ápice ≠ base) | `apexStats[] = {stat, value, unit}` e `apexGoldValueTotal` (ou `apexEfficiencyBase`) por item |

Enquanto isso (Fase 2, T8b): o app extrai do texto `apex` só os "+N de <atributo>" com sinal e nome conhecido (21 dos 102 itens ganham atributos substituídos; os demais mostram o texto). Com `apexStats[]` no catálogo, a extração é desligada.

Combinações: (valor base + bônus MF, ou valor no ápice) ÷ (preço ou preço líquido).

## 2. Fragmentos do Atributo adicional (Stat Bonus)
Para escolher o fragmento dentro da Build: lista estruturada `fragments[] = {tier: "Prata"|"Ouro"|"Prismático", stat, value, unit, gold}`. Hoje está em texto no `mechanics` da habilidade.
