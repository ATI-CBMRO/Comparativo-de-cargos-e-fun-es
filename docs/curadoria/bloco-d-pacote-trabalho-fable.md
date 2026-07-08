# Bloco D — pacote de trabalho para o Fable (2026-07-08)

> Objetivo deste documento: **reduzir ao mínimo o que o Fable precisa ler do zero**
> pra viabilizar o comparador "Regimento Interno × outros estados" (Bloco D). Não é
> a curadoria em si — é o BRIEFING que corta o trabalho de leitura antes de chamar
> o Fable. Ver `docs/curadoria/bloco-d-esboco-comparador-ri.md` pro objetivo geral
> do bloco (só a tela de comparação — a geração da minuta já existe, ver esse doc).

## Achado que motiva este pacote (conferido em código, 2026-07-08)

Depois da correção do achado MT/SE (`states_data.json`, commit `d74bc67`), só
**5 estados** contam de verdade como "tem Regimento Interno" hoje:
**AL, DF, PR, PA, RS** (`has_regimento: true`). MT e SE saíram dessa lista — os
arquivos deles são na verdade Regulamento Geral e RISD, não Regimento Interno.

A minuta do RO (`database/minuta_structure.json`) tem **27 órgãos**. Cruzando com
o que `scripts/minuta_enrichment.py` (`ENRICHMENT_ORGAN`) já extraiu e citou:

- **22 dos 27 órgãos já têm algum texto de outro estado** transcrito verbatim.
- **20 desses 22 já têm texto de pelo menos um dos 4 estados AL/DF/PR/PA** —
  ou seja, a leitura mais cara (ler o documento inteiro, achar o trecho certo)
  **já foi feita** para a maior parte da minuta.
- **O RS nunca foi lido pra esse fim.** Ele já foi lido uma vez (2026-07-06, ver
  `docs/curadoria/panorama-cobertura.md`), mas só pra extrair o capítulo de
  cerimonial/honras (Cap. VI, Arts. 73–81) para o Regulamento — nunca pra mapear
  órgão por órgão como este bloco precisa.
- **2 órgãos** (`crbm`, `assessorias`) têm texto, mas só de SC/GO — que não
  contam mais como Regimento Interno — então continuam SEM cobertura de um
  estado RI de verdade.
- **5 órgãos não têm nenhum texto ainda**: `bifea`, `cat`, `doe`, `gbm`,
  `guarnicao`.

## As 3 tarefas do Fable, em ordem de custo (mais barata primeiro)

### Tarefa 1 — Classificar o que já existe (revisão, não leitura do zero)

Para os **20 órgãos já cobertos por AL/DF/PR/PA** (lista abaixo), o Fable NÃO
precisa reler os documentos-fonte inteiros — só olhar o trecho já extraído em
`scripts/minuta_enrichment.py` (`ENRICHMENT_ORGAN`) e classificar o nível de
correspondência com o órgão equivalente do RO, na MESMA régua já usada no
Bloco B1-M do Regulamento (`docs/curadoria/panorama-cobertura.md`, legenda
● exata · ◐ parcial · ○ temática · — ausente):

| Órgão RO | Fonte(s) já extraída(s) (AL/DF/PR/PA) |
|---|---|
| dpo | PA (Lei 11.060/2025, Art. 16) · DF (RI, Art. 454) |
| cot | DF (RI, Art. 54) |
| bbm | PR (Lei 22.206/2024, Art. 35, I) |
| cibm | PR (Art. 35, II) |
| bbs | PR (Art. 35, III) |
| boa | PR (Art. 35, IV) |
| cg | PA (RI, Art. 6) · DF (RI, Art. 58) |
| depdec | AL (RI, Art. 13) |
| condeg | AL (RI, Art. 11) |
| dp | DF (RI, Art. 127) · PR (Art. 28) |
| deei | DF (RI, Art. 227) |
| dpof | DF (RI, Art. 187) · PA (RI, Art. 170) · AL (RI, Art. 52) |
| dsap | DF (RI, Art. 154) |
| dlog | PR (Art. 29) · DF (RI, Art. 218) · PA (RI, Art. 163) |
| cint | DF (RI, Art. 304) · PA (RI, Art. 140) · AL (RI, Art. 25) |
| ccs | DF (RI, Art. 291) · AL (RI, Art. 26) |
| cinf | DF (RI, Art. 241) |
| gab-cg | DF (RI, Art. 6) · PA (RI, Art. 107) |
| ag | DF (RI, Art. 110) · PA (RI, Art. 119) |
| corregedoria | DF (RI, Art. 96) · AL (RI, Art. 29) · PR (Portaria 227/2023, Art. 3º) |

**Entregável**: uma tabela por órgão com o nível de correspondência de cada
fonte já citada — sem precisar abrir o PDF de AL/DF/PR de novo (o trecho e a
citação já estão no script).

### Tarefa 2 — Leitura nova, só do RS (o único genuinamente pendente)

O RI do Rio Grande do Sul (Portaria CBMRS nº 001/2025, **96 artigos** — documento
curto) precisa de uma leitura própria pra mapear órgão por órgão, no padrão dos
`docs/curadoria/de-para-*.md` já existentes — mas organizada pelos **27 órgãos
da minuta do RO**, não pelos 15 temas do Regulamento (são taxonomias diferentes;
ver nota de metodologia abaixo). Produzir `docs/curadoria/de-para-ri-rs.md`.

### Tarefa 3 — Checar as 7 lacunas antes de aceitar "pendente"

Antes de marcar `bifea`, `cat`, `doe`, `gbm`, `guarnicao`, `crbm` e
`assessorias` como sem cobertura, o Fable confere especificamente esses 7
órgãos nos 5 documentos de RI (AL, DF, PR, PA, RS) — busca dirigida, não
releitura completa. Se genuinamente não houver nada (como já aconteceu com
uniformes/cerimonial no Regulamento), documentar o motivo e seguir; não é
bloqueante pro Bloco D.

## Nota de metodologia — taxonomia diferente do Regulamento

O Regulamento organiza por **15 temas** (disposicoes-preliminares,
servico-operacional etc.). A minuta do RI organiza pelos **27 órgãos da LOB**
(cg, dpo, cot...). O de-para do RS (Tarefa 2) e a classificação da Tarefa 1
devem usar a chave de ÓRGÃO (`organKey`, a mesma de `minuta_structure.json`),
não os temas do Regulamento — os documentos de-para do Regulamento
(`de-para-mt.md` etc.) servem de MODELO de processo, não de dado reaproveitável
diretamente aqui.

## Achado colateral (não bloqueante, corrigir quando conveniente)

Várias citações em `ENRICHMENT_ORGAN` dizem `"cf. CBMMT, RI, Art. NN"` — mas
depois da correção desta sessão, sabemos que o documento de MT é na verdade o
**Regulamento Geral (Portaria nº 009/BM-8/2013)**, não um Regimento Interno.
A citação deveria dizer `"cf. CBMMT, Regulamento Geral (Portaria nº
009/BM-8/2013), Art. NN"`. Não afeta o Bloco D (MT não é um dos 5 estados RI
usados aqui) — é só uma correção de rótulo pra próxima rodada de limpeza.
