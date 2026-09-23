# Decisões herdadas do Capítulo 1 que afetam o app

O Catálogo é do Capítulo 1 e está fechado (225 itens, patch 16.18.1). O que a checagem de integridade do catalog.json aponta abaixo NÃO é pendência: são decisões já tomadas lá (CHECKPOINT do Capítulo 1, 12/09/2026). O app respeita o dado como está.

O que ainda é pendência do Capítulo 1 (dado errado, forma do dado, patch novo, campos a acrescentar) está em `docs/pendencias_capitulo1.md`.

- **Shattered Armguard (ID 2421) não existe no catálogo** — removido de propósito: é a versão pós-uso da Armaguarda da Caçadora, registrada como nota no bloco dela. Amplifying Tome e Cloth Armor continuam listando-o em "Vira em"; o app mostra o nome sem link.
- **World Atlas → "Missão de Suporte"** — destino por transformação, não item. O app mostra o texto como está.
- **Stat Bonus mantém ID 6032** com a anotação da wiki (220000) no próprio campo; o `id` sai como texto, o `iconUrl` usa 6032. O app não depende de `id` numérico.
- **Slightly Magical Footwear** substitui as Botas e lista as 7 botas de tier 2 em "Vira em"; as botas não o listam como componente. Componente alternativo, não obrigatório.
- **Atma's Reckoning** lista Giant's Belt duas vezes (qty 1 + 1): o app agrupa componentes repetidos ao exibir (×2). A soma da receita fecha.
- **Giant's Belt e Cloak of Agility** não listam Atma's Reckoning em "Vira em" (fonte é a seção "Builds Into" da wiki). O app pode derivar o "Vira em" inverso a partir de `components` se precisar.
- **Pets (Gustwalker, Mosstomper, Scorchclaw)** não têm `Atributo[]`; o app mostra as habilidades. Scorchclaw Pup carrega "[A CONFIRMAR]" (lentidão 2s vs 3s) — única dúvida de fonte aberta no Capítulo 1.
