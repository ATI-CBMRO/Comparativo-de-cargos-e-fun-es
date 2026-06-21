# Enriquecimento da minuta — legislações curadas e avaliadas

Registro das fontes usadas no enriquecimento da minuta do Regimento Interno do
CBMRO (`scripts/minuta_enrichment.py` → `database/minuta_structure.json`) e da
avaliação das demais, para não reabrir a mesma análise.

**Princípio:** só entram competências **enumeradas e verbatim** (incisos limpos,
transcritos da fonte). Texto **condensado/paráfrase** ou **narrativo por subdivisão**
fica fora — incluir exigiria editorializar (viola "verbatim, sem invenção") ou
geraria incisos prolixos que degradam o documento. `ro.json` nunca é tocado.

## Legislações curadas (11) — estado em 2026-06-19

| Fonte | Base legal | Mapeamento | Itens |
|---|---|---|---|
| CBMAL | RI, Arts. 107/114/115 | cargos (CRBM/BBM/CIBM/BBS/BIFEA/BOA) | 109 |
| CBMMT | RI, Art. 236 / Art. 198 | DPO / COT | 16 |
| CBMPR | Lei 22.206/2024, Art. 35 | BBM/CIBM, GOST→BBS, UOA→BOA | 14 |
| CBMSC | Dec. 1.328/2021, Art. 39 / Art. 38 | CRBM / COT | 14 |
| CBMDF | RI (Portaria nº 24/2020), Art. 454 / Art. 54 | DPO (COMOP) / COT (DESEG) | 14 |
| CBMSP | Lei 616/1974, Art. 40 §2º 7 | COT | 5 |
| CBMBA | Lei 14.572/2023, Art. 49 III / IV | DPO / COT | 4 |
| CBMCE | Lei 13.438/2004, Art. 17 | COT | 4 |
| CBMPE | Lei 15.187/2013, Art. 97 | COT | 3 |
| CBMES | NGA — Centro de Atividades Técnicas | COT | 2 |
| CBMPA | Lei 11.060/2025, Art. 16 | DPO | 2 |

`ENRICHMENT` (por cargo) = CBMAL. `ENRICHMENT_ORGAN` (por órgão) = os demais.

> O **CBMDF** foi incorporado em 2026-06-19 a partir do seu **Regimento Interno**
> (Portaria nº 24/2020), não da LOB: Art. 454 (Comando Operacional, I–VI) → DPO e
> Art. 54 (DESEG, I–VIII) → COT. O `COT_MAP['df']` era vazio no comparativo
> DPO×COT (a LOB do DF não discrimina órgão técnico), mas o RI detalha o DESEG.

## Avaliadas e descartadas (com motivo)

**LOBs novas pós-2021 não curadas** — varredura em 2026-06-19. Todas seguem o padrão
das LOBs modernas: **enxutas**, definem cada órgão por finalidade em uma frase e
remetem o detalhe a Regimento/decreto (que não temos). Sem incisos enumeráveis.

| Estado | LOB | Achado |
|---|---|---|
| Sergipe (SE) | Lei 8.979/2022 | Art. 30 define a Diretoria Operacional em **uma frase**; sem rol. |
| Paraíba (PB) | LC 191/2024 | Art. 35 (DAT) é **caput definicional**; sem rol. |
| Goiás (GO) | Lei 21.792/2023 | LOB não enumera; "Regimento dos Serviços" traz só frases-tópico condensadas. |
| Amapá (AP) | LC 180/2026 | A lei **remete a estrutura a decreto** (Art. 6º §2º); só Assessoria Técnica genérica. |

**Outras descartadas anteriormente:**
- **AC, PB** (texto definicional/estrutural — jurisdição, subordinação — não competências).
- **RS** — RI (Dec. 53.897/2018) é rico, mas estrutura as competências em **parágrafos
  longos por subdivisão** (DAdm/DGN/DPIS etc.), não decomponíveis em incisos sem cortar/parafrasear.
- **AM, RN, RJ, PI, MA, MG, MS, RR, TO, AP** — órgãos operacionais/técnicos com
  extração rasa/condensada (1–2 frases-tópico) no `organs_detail`.

**Regimentos Internos avaliados:** dos RIs disponíveis em `database/markdown/`
(AL, DF, ES/NGA, GO, MT, PR, PA, RN, RS, SE), foram **aproveitados** AL, MT, ES e
**DF** (este via RI, 2026-06-19); **PR e PA** já entram pela LOB (RI não tapado);
**GO** (Regimento dos Serviços — condensado), **RS** (narrativo por subdivisão),
**RN** (regulamento raso) e **SE** (RI é regimento de serviço diário — Superior de
Dia etc., sem competências de órgão) ficaram de fora.

## Como ampliar no futuro (se necessário)

1. Para estados de RI **narrativo** (RS, SE, PB…): a única via fiel seria usar o
   **caput** dos artigos (definição concisa, verbatim) como item único de finalidade —
   baixo valor, mas aceitável se quiser representação.
2. Para estados com RI **detalhado ainda não curado**: extrair os incisos verbatim do
   markdown (como foi feito com o CBMAL) e adicionar a `ENRICHMENT`/`ENRICHMENT_ORGAN`.
   Trabalho artesanal por UF.

Após editar `minuta_enrichment.py`, reexecutar `python scripts/build_minuta_structure.py`.
