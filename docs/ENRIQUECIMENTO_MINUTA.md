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

### Capítulo "Da Guarnição de Serviço Operacional" (menor fração)

Adicionado em 2026-06-19 como **nó estrutural novo** (não vem do `ro.json`): o CBMRO
não define a guarnição na LOB/minuta (é matéria de regulamento de serviço). Subsídio
**integral do CBMSE — RISD** (Regulamento Interno dos Serviços Diários, BGO 060/2022),
rotulado: Art. 14 (Comandante de Guarnição, 16 incisos) + Art. 15 (Condutor e Operador
de Viatura, 15 incisos). É a menor fração ("equipe da viatura em serviço"), abaixo do
GBM. Definido em `GUARNICAO_CHAPTER` (`minuta_enrichment.py`), montado por
`build_guarnicao_chapter()` e inserido antes das Disposições Finais.

> O **CBMDF** foi incorporado em 2026-06-19 a partir do seu **Regimento Interno**
> (Portaria nº 24/2020), não da LOB: Art. 454 (Comando Operacional, I–VI) → DPO e
> Art. 54 (DESEG, I–VIII) → COT. O `COT_MAP['df']` era vazio no comparativo
> DPO×COT (a LOB do DF não discrimina órgão técnico), mas o RI detalha o DESEG.

## Frente 2 — Bloco 1: Direção Geral/Colegiada (2026-06-28)

Curadoria dos 3 órgãos de direção geral/colegiada que apareciam com "0 estados" no
`/comparar`: `cg` (Comando Geral), `depdec` (Diretoria Estadual de Proteção e Defesa
Civil) e `condeg` (Conselho Deliberativo de Estratégia e Gestão). Só entrou competência
**enumerada e verbatim** do **órgão/colegiado como unidade** — as atribuições pessoais do
Comandante-Geral (cargo) ficaram de fora do comparativo de `cg`.

| Estado | Base legal | Órgão (organ_key) | Itens |
|---|---|---|---|
| CBMMT | RI, Art. 14 | Estado Maior-Geral (cg) | 6 |
| CBMPA | RI, Art. 6 | Comando-Geral / assessoramento (cg) | 3 |
| CBMDF | RI (Portaria nº 24/2020), Art. 58 | Estado-Maior-Geral (cg) | 12 |
| CBMAL | RI, Art. 13 | Coordenadoria Estadual de Defesa Civil (depdec) | 23 |
| CBMGO | Lei nº 18.305/2013, Art. 27 | Comando de Operações de Defesa Civil (depdec) | 5 |
| CBMES | NGA, Art. 3 | Coordenadoria Estadual de Proteção e Defesa Civil (depdec) | 19 |
| CBMAL | RI, Art. 11 | Conselho de Políticas Estratégicas (condeg) | 10 |
| CBMMT | LC nº 775/2023, Art. 15 | Conselho Superior de Bombeiros Militar (condeg) | 9 |

Avaliados e **descartados** neste bloco (motivo):

- **cg — CBMES, NGA, Art. 4**: caput definicional ("Compete ao Comando-Geral o
  planejamento, a coordenação, a orientação e o controle da Corporação…") sem rol de
  incisos. Art. 5 enumera atribuições do **Comandante-Geral (cargo)**, não do órgão.
- **depdec — CBMMA (Maranhão), LOB Art. 54**: meramente remissivo ("a Coordenadoria
  Estadual de Proteção e Defesa Civil… serão estabelecidos em lei específica"); sem rol.
- **depdec — CBMAM (Amazonas), LOB Art. 14**: caput de finalidade da CEDEC, sem incisos
  de competência da unidade enumerados.
- **condeg — CBMMT, RI, Art. 10**: duplica o conteúdo da LOB Art. 15 (mesmo Conselho
  Superior); usada a fonte de hierarquia superior (LC) e descartada a redundância do RI.
- **condeg — demais estados**: a maioria das LOBs/RIs só traz **composição** do conselho
  (membros) e/ou as atribuições do **presidente**, sem enumerar competências do colegiado
  como órgão. `condeg` (Conselho Deliberativo de Estratégia e Gestão) é raro fora do RO;
  os dois achados (AL/MT) são os equivalentes mais próximos com rol verbatim.

## Frente 2 — Bloco 2: Direção Setorial (2026-06-28)

Curadoria dos 8 órgãos de direção setorial que apareciam com "0 estados" no `/comparar`:
`dp` (Diretoria de Pessoal), `deei` (Educação, Ensino e Instrução), `dpof` (Planejamento,
Orçamento e Finanças), `dsap` (Saúde e Assistência ao Pessoal), `dlog` (Logística), `cint`
(Inteligência), `ccs` (Comunicação Social) e `cinf` (Informática). Só entrou competência
**enumerada e verbatim** da **unidade** — atribuições do cargo (Diretor/Comandante/Chefe)
e capítulos meramente definicionais ficaram de fora.

| Estado | Base legal | Órgão (organ_key) | Itens |
|---|---|---|---|
| CBMDF | RI (Portaria nº 24/2020), Art. 127 | Diretoria de Gestão de Pessoal (dp) | 12 |
| CBMPR | Lei nº 22.206/2024, Art. 28 | Diretoria de Pessoal (dp) | 5 |
| CBMMT | RI, Art. 161 | Diretoria de Ensino, Instrução e Pesquisa (deei) | 7 |
| CBMDF | RI (Portaria nº 24/2020), Art. 227 | Diretoria de Ensino (deei) | 10 |
| CBMGO | Lei nº 18.305/2013, Art. 28 | Comando de Ensino Bombeiro Militar (deei) | 2 |
| CBMDF | RI (Portaria nº 24/2020), Art. 187 | Diretoria de Orçamento e Finanças (dpof) | 6 |
| CBMPA | RI, Art. 170 | Diretoria de Finanças (dpof) | 10 |
| CBMAL | RI, Art. 52 | Diretoria de Finanças (dpof) | 17 |
| CBMGO | Lei nº 18.305/2013, Art. 26 | Comando de Gestão e Finanças (dpof) | 6 |
| CBMDF | RI (Portaria nº 24/2020), Art. 154 | Diretoria de Saúde (dsap) | 10 |
| CBMGO | Lei nº 18.305/2013, Art. 32 | Comando de Saúde (dsap) | 3 |
| CBMPR | Lei nº 22.206/2024, Art. 29 | Diretoria de Apoio Logístico e Finanças (dlog) | 4 |
| CBMDF | RI (Portaria nº 24/2020), Art. 218 | Diretoria de Materiais e Serviços (dlog) | 8 |
| CBMPA | RI, Art. 163 | Diretoria de Apoio Logístico (dlog) | 21 |
| CBMMT | RI, Art. 54 | Coordenadoria da Agência Central de Inteligência (cint) | 18 |
| CBMDF | RI (Portaria nº 24/2020), Art. 304 | Centro de Inteligência (cint) | 15 |
| CBMPA | RI, Art. 140 | Centro de Inteligência (cint) | 3 |
| CBMAL | RI, Art. 25 | Assessoria de Inteligência e Contra-Inteligência (cint) | 12 |
| CBMGO | Lei nº 18.305/2013, Art. 29 | Comando de Operações de Inteligência (cint) | 5 |
| CBMMT | RI, Art. 110 | Coordenadoria de Comunicação Social (ccs) | 15 |
| CBMDF | RI (Portaria nº 24/2020), Art. 291 | Centro de Comunicação Social (ccs) | 9 |
| CBMAL | RI, Art. 26 | Assessoria de Relações Públicas e Comunicação Social (ccs) | 7 |
| CBMMT | RI, Art. 129 | Coordenadoria de Tecnologia da Informação (cinf) | 10 |
| CBMDF | RI (Portaria nº 24/2020), Art. 241 | Diretoria de Tecnologia da Informação e Comunicação (cinf) | 8 |

Avaliados e **descartados** neste bloco (motivo):

- **dsap — CBMPA, RI, Art. 194**: caput definicional ("compete realizar o planejamento, a
  gestão e a execução das ações de assistência relacionadas à saúde…"); sem rol de incisos.
- **cinf — CBMPA, RI, Art. 186 (DTIC)**: caput definicional ("planejar, coordenar, executar
  e fiscalizar as atividades relacionadas à tecnologia da informação…"); sem rol.
- **cint — CBMES, NGA, Art. 11 (Assessoria de Inteligência)**: caput de finalidade em uma
  frase ("compete executar atividades relacionadas ao serviço de inteligência…"); sem rol.
- **cinf — CBMAL, RI, Art. 94/95 (Centro de Tecnologia, Informática e Informação)**: Art. 94
  é caput definicional; Art. 95 enumera atribuições do **Comandante (cargo)**, não do órgão.
- **dlog — CBMGO, Lei nº 18.305/2013, Art. 33 (Centro de Manutenção)**: rol restrito à
  manutenção de viaturas/frota, não à direção setorial de logística/suprimento como unidade.
- **dp — CBMGO, Lei nº 18.305/2013, Art. 26**: o rol foi atribuído a `dpof` (órgão "Gestão e
  Finanças" combinado); não duplicado em `dp` para evitar ruído.

## Frente 2 — Bloco 3: Assessoramento/Apoio (2026-06-28)

Curadoria dos 3 órgãos de assessoramento/apoio ao Comando-Geral: `assessorias`
(Assessorias), `gab-cg` (Gabinete do Comandante-Geral) e `ag` (Ajudância-Geral). Domínio
de **match baixo** — estas unidades costumam ser descritas por finalidade, não enumeradas.
Só entrou competência **enumerada e verbatim** do **órgão**.

| Estado | Base legal | Órgão (organ_key) | Itens |
|---|---|---|---|
| CBMGO | Lei nº 18.305/2013, Art. 17 | Assessoria Jurídica (assessorias) | 3 |
| CBMGO | Lei nº 18.305/2013, Art. 18 | Assessoria Parlamentar (assessorias) | 4 |
| CBMDF | RI (Portaria nº 24/2020), Art. 6 | Gabinete do Comandante-Geral (gab-cg) | 6 |
| CBMPA | RI, Art. 107 | Gabinete do Comandante-Geral (gab-cg) | 6 |
| CBMDF | RI (Portaria nº 24/2020), Art. 110 | Ajudância Geral (ag) | 8 |
| CBMMT | RI, Art. 152 | Coordenadoria de Ajudância Geral (ag) | 12 |
| CBMPA | RI, Art. 119 | Ajudância-Geral (ag) | 5 |

Avaliados e **descartados** neste bloco (motivo):

- **gab-cg — CBMMT, RI, Art. 220/221**: Art. 220 é caput de finalidade (uma frase); Art. 221
  enumera competências do **Chefe de Gabinete (cargo)**, não do órgão.
- **gab-cg — CBMSP, Lei nº 616/1974, Art. 221 (CBMRS), CBMGO Art. 16**: gabinetes descritos
  por finalidade/estrutura, sem rol de competências do órgão.
- **assessorias — CBMCE, Lei nº 13.438/2004, Art. 13/14**: Art. 13 é caput definicional;
  Art. 14 enumera competências da **Chefia (cargo)**, não da Assessoria como órgão.
- **assessorias — CBMPE, Lei nº 15.187/2013, Art. 45/46**: Art. 45 é caput definicional;
  Art. 46 é só a estrutura organizacional.
- **assessorias — CBMAL, RI, Art. 15 (Assessoria Técnica)**: caput de finalidade em prosa;
  sem rol de incisos.
- **assessorias — CBMES, NGA, Art. 6/7 (Assessoria Técnica da CEPDEC)**: enumera, mas a
  unidade é assessoria interna da Defesa Civil (escopo `depdec`), não assessoria do
  Comando-Geral; descartada para evitar colisão conceitual.
- **ag — CBMPA, RI, Art. 118 / CBMMT, RI, Art. 151**: capítulos definicionais (finalidade da
  unidade em uma frase); os róis aproveitados são os Arts. 119 e 152, respectivamente.

## Frente 2 — Bloco 4: Correição (2026-06-28)

Curadoria do órgão de correição: `corregedoria` (Corregedoria-Geral). Corregedorias
costumam ter competências **enumeradas** em RI ou portaria própria — domínio de match
plausível. Só entrou competência **enumerada e verbatim** do **órgão** (não do cargo
Corregedor-Geral).

| Estado | Base legal | Órgão (organ_key) | Itens |
|---|---|---|---|
| CBMMT | RI, Art. 16 | Corregedoria-Geral (corregedoria) | 20 |
| CBMDF | RI (Portaria nº 24/2020), Art. 96 | Corregedoria (corregedoria) | 12 |
| CBMAL | RI, Art. 29 | Corregedoria Geral (corregedoria) | 6 |
| CBMPR | Portaria nº 227/2023, Art. 3º | Corregedoria-Geral (corregedoria) | 12 |

Avaliados e **descartados** neste bloco (motivo):

- **CBMMT, RI, Art. 15/19**: Art. 15 é caput definicional (uma frase); Art. 19 enumera
  competências do **Corregedor-Geral (cargo)**, não do órgão. Aproveitado o Art. 16
  (competências da Corregedoria-Geral como órgão).
- **CBMDF, RI, Art. 78**: competências **comuns** a Auditoria/Ouvidoria/Corregedoria/Núcleo de
  Custódia (genéricas de qualquer órgão de controle), não distintivas da Corregedoria.
  Aproveitado o Art. 96 (competências orgânicas próprias).
- **CBMAL, RI, Art. 28/30**: Art. 28 é caput definicional; Art. 30 enumera competências do
  **Corregedor Geral (cargo)**. Aproveitado o Art. 29 (competências do órgão).
- **CBMPR, Lei nº 22.206/2024, Art. 23**: rol de **finalidade** em 3 incisos genéricos
  (assegurar a lei, padronizar procedimentos, realizar correições); aproveitado o rol
  enumerado e distintivo da Portaria nº 227/2023, Art. 3º.
- **CBMPA, RI, Art. 34**: a Corregedoria-Geral como órgão traz apenas 2 incisos definicionais
  (assessorar na disciplina; orientar/prevenir/fiscalizar) — finalidade, não competências
  enumeradas distintivas. O detalhe paraense vive no cargo (Corregedor-Geral, Art. 47) e nas
  seções/núcleos. Descartado.
- **CBMRS, RI (Dec. 53.897/2018), Art. 30**: competências da Corregedoria-Geral descritas em
  **prosa narrativa por subdivisão** (Por meio da DAdm/DJD/DFE… compreendendo: …), não
  decomponíveis em incisos sem cortar/parafrasear. Descartado (mesmo motivo geral do RS).

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
**GO** (Regimento dos Serviços — condensado), **RS** (narrativo por subdivisão) e
**RN** (regulamento raso) ficaram de fora. **SE** — a LOB e o RI orgânico não têm
competências de órgão enumeráveis, mas o **RISD do SE** (serviços diários) forneceu o
capítulo da **Guarnição** (Comandante de Guarnição e Condutor/Operador, ver acima).

## Como ampliar no futuro (se necessário)

1. Para estados de RI **narrativo** (RS, SE, PB…): a única via fiel seria usar o
   **caput** dos artigos (definição concisa, verbatim) como item único de finalidade —
   baixo valor, mas aceitável se quiser representação.
2. Para estados com RI **detalhado ainda não curado**: extrair os incisos verbatim do
   markdown (como foi feito com o CBMAL) e adicionar a `ENRICHMENT`/`ENRICHMENT_ORGAN`.
   Trabalho artesanal por UF.

Após editar `minuta_enrichment.py`, reexecutar `python scripts/build_minuta_structure.py`.
