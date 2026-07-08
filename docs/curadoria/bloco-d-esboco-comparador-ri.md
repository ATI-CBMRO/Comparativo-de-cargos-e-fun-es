# Bloco D — Comparador do Regimento Interno (esboço, 2026-07-08)

> Status: ESBOÇO — falta planejar direito (metodologia igual ao B1-M) antes de
> executar. Não começar a codar direto a partir deste arquivo.

## ⚠️ O que este bloco NÃO precisa fazer (esclarecido em 2026-07-08)

A geração da minuta do Regimento Interno **com base em outros estados já existe**
e não faz parte do escopo deste bloco. A página `/minuta` (`MinutaWizard.jsx`) já
gera a minuta completa do CBMRO enriquecida com texto VERBATIM de **13 estados**
(AL, BA, CE, DF, ES, GO, MT, PA, PE, PR, SC, SE, SP), via
`scripts/minuta_enrichment.py` (`ENRICHMENT_ORGAN`) — é inclusive uma feature
mais antiga que a do Regulamento. O Bloco D cuida SÓ da tela de **comparação**
(item 3 abaixo); os itens 1 e 2 (curadoria + script de build) existem apenas
pra alimentar essa tela nova com o campo `alternatives` que falta hoje, não pra
gerar a minuta em si (que já está pronta).

## Origem do pedido

Ao reorganizar o menu lateral em 2 trilhas (Regimento Interno × Regulamento Geral,
Bloco C), o Wândrio notou uma assimetria: a trilha do Regulamento tem uma tela
"Comparar Regulamento" (nossa minuta, dispositivo por dispositivo, ao lado do texto
verbatim de cada estado, com selo de correspondência exata/parcial/temática) — a
trilha do Regimento Interno **não tem equivalente**. A tela que existe lá
("Subsídio à Minuta", `/comparar`) é outra coisa: uma tabela-matriz de estrutura
organizacional (órgão/cargo/atribuições) entre os 27 estados — não compara o TEXTO
da nossa minuta com o de outros estados, artigo por artigo.

## Achado técnico (verificado, não é suposição)

`database/minuta_structure.json` **não tem** o campo `alternatives` que
`regulamento_structure.json` tem — ou seja, o RI nunca passou pela curadoria
dispositivo-a-dispositivo (de-para com nível de correspondência) que o Regulamento
recebeu no Bloco B1-M. `MinutaDiagrams.jsx`/`commandChart`, por outro lado, É gerado
a partir de `organs_detail/ro.json` — a estrutura real da LOB de Rondônia — por isso
foi movido pra aba "Geral" do menu (não pertence à trilha de comparação com outros
estados).

## O que esse bloco precisaria (mesmo tamanho do B1-M + B2 + B4, replicado pro RI)

1. **Curadoria (Fable)** — de-para dispositivo→tema para os **7 estados com Regimento
   Interno** (ver `database/states_data.json`, stat `has_regimento`), com nível de
   correspondência (exata/parcial/temática), seguindo a MESMA metodologia do B1-M
   (candidatos automáticos → de-para validado pelo Wândrio → transcrição verbatim →
   `verificar_verbatim.py`).
2. **Script de build** — análogo a `build_regulamento_structure.py`, populando
   `alternatives` em `minuta_structure.json` (ou um arquivo irmão, a decidir) a
   partir da curadoria acima.
3. **Tela nova** — `MinutaRIComparator.jsx` (ou reaproveitar `MinutaComparator.jsx`
   com um modo novo), clonando o padrão visual/interação de `RegulamentoComparator.jsx`
   (sumário de capítulos, coluna RO × coluna do estado selecionado, chips de estado,
   selo de correspondência, impressão).
4. **Nav** — novo item na trilha "Regimento Interno" (ex.: "Comparar Regimento
   Interno"), paralelo a "Comparar Regulamento".

## Perguntas em aberto para a rodada de planejamento com o Fable

- Os 7 estados com RI são suficientes, ou vale a pena também aproveitar LOBs de
  outros estados como fonte "temática" (nível mais fraco), como se fez no Regulamento
  com estados que não tinham Regulamento próprio?
- `Subsídio à Minuta` (a matriz atual) continua existindo em paralelo, ou este novo
  comparador a substitui? (Recomendação preliminar: manter as duas — servem
  perguntas diferentes — mas confirmar com o Wândrio.)
- O `alternatives` novo entra no MESMO `minuta_structure.json` (como fez o Regulamento
  com o dele) ou em arquivo separado, dado que `minuta_structure.json` já é grande e
  tem histórico de uso por `buildArticles`/`minutaArticles.js`?

## Pré-requisito descoberto depois (2026-07-08): auditoria de classificação

Antes mesmo de iniciar o Bloco D, foi confirmado um problema na classificação de tipo
de documento (`parse_doc_type` em `scripts/build_states_data.py`) que também afeta a
confiabilidade de QUALQUER comparador futuro — ver seção correspondente no
`CLAUDE.md` ("Classificação de tipo de documento — auditoria pendente"). Resumo: MT e
SE mostram "Regimento Interno" em `states_data.json`, mas o conteúdo real (já
descoberto pela curadoria do Regulamento) é outro. Os 18 estados fora da curadoria do
Regulamento nunca tiveram o conteúdo conferido — só o nome do arquivo. Corrigir isso
(ou pelo menos deixar visível o que foi/não foi verificado, ex. numa tabela
LOB×RI×Regulamento por estado) é pré-requisito de confiança antes de ampliar a
curadoria pro Bloco D.

## Pacote de trabalho pro Fable (2026-07-08)

Ver `docs/curadoria/bloco-d-pacote-trabalho-fable.md` — já reduz o escopo real:
depois da correção MT/SE, só 5 estados contam como Regimento Interno (AL, DF,
PR, PA, RS); 4 deles já têm texto extraído pra 20 dos 27 órgãos da minuta (não
precisa reler os documentos, só classificar o nível de correspondência); só o
RS precisa de leitura nova (documento curto, 96 artigos).

## Não fazer sem planejar

Este bloco NÃO deve ser iniciado direto em código — precisa da mesma disciplina do
B1-M (candidatos → de-para → validação do Wândrio → transcrição verbatim →
verificação) para não entregar uma tela vazia ou com comparações erradas. Planejar
com o Fable quando for a vez.
