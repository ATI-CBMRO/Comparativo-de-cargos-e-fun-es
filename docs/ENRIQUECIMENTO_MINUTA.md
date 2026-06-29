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

---

## Camada LOB — /comparar (2026-06-28)

Camada **distinta** do enriquecimento da minuta acima: vive em
`scripts/lob_enrichment.py` (`LOB_ENRICHMENT[(organ_key, state_id)]`), é lida por
`scripts/build_minuta_comparison.py` e preenche, no `/comparar`, a coluna 2 ("LOB do
estado") e a parte LOB da coluna 3 ("LOB + RI"). **Critério mais permissivo** que o da
minuta: além de incisos, admite a **finalidade/caput** (frase de finalidade do órgão)
da Lei de Organização Básica — que é o ganho típico das LOBs modernas. Verbatim, sem
paráfrase; `ro.json`/`comparativo_dpo_cot.json`/`minuta_enrichment.py` não são tocados.

### Lote 1 — AC, AL, AM, AP, BA (55 entradas)

| Estado | Lei (LOB) | Órgãos com entrada | Observação |
|---|---|---|---|
| Acre (AC) | Lei nº 2.009/2008 (alt. Lei nº 4.428/2024) | 4 | LOB enxuta/estrutural; Art. 22 remete competências dos órgãos a instruções normativas do CG. |
| Alagoas (AL) | Lei nº 7.444/2012 | 19 | LOB rica: finalidade por órgão (caput) para quase toda a estrutura. |
| Amazonas (AM) | Lei nº 2.538/1999 | 14 | Finalidade por órgão; AG (Art. 18) tem incisos enumerados (5). |
| Amapá (AP) | LC nº 180/2026 | 2 | LOB nova **remete estrutura/atribuições a decreto** (Art. 6º); só finalidade por categoria. |
| Bahia (BA) | Lei nº 14.572/2023 | 16 | LOB moderna com "tem por finalidade" em quase todos os órgãos. |

**Casos cargo-vs-órgão (finalidade tirada da atribuição do dirigente, não de caput do órgão):**
- `(cg, ac)` — Art. 6º enuncia a competência do **comandante-geral** (a LOB do AC não dá
  finalidade ao "Comando Geral" como unidade). Idem `(cg, am)` Art. 9º e `(cg, al)` Art. 6º
  (descrevem o Comando pelo papel do Comandante Geral, mas em frase de finalidade do órgão).

**LOB remete a decreto/Regimento (detalhe não disponível na lei):**
- **AP** (LC 180/2026) — Art. 6º: estrutura interna e atribuições "definidas por ato do
  Governador"; só há finalidade por **categoria** de órgão. Aproveitadas: direção-geral
  (`cg`, §1º I) e correição/Corregedoria-Geral (`corregedoria`, §5º). Diretorias/Centros
  individuais (RH, logística, finanças, TI, saúde) **sem finalidade própria** → sem entrada.
- **BA** (Lei 14.572/2023) — Art. 7º §2º remete estrutura interna e competências de detalhe
  ao Regimento (Decreto); a finalidade-caput de cada órgão, porém, está na própria LOB e foi
  aproveitada.
- **AC** (Lei 2.009/2008) — Art. 22 (red. Lei 3.105/2015) remete competências/atribuições
  dos órgãos a instruções normativas do CG; só finalidades de `cg`, `assessorias`, `ag`,
  `corregedoria` constam da lei.

**Órgãos sem equivalente na LOB do estado (sem entrada), por estado:**
- **AC**: as Diretorias (DRH, DATOP, DLPF, DEI, DP-planejamento, DS) só têm finalidade
  **coletiva** (Art. 12, "órgãos de direção setorial"), sem caput individual → não mapeadas
  a `dp`/`cot`/`dlog`/`deei`/`dpof`/`dsap`. Sem `condeg`, `cint`, `ccs`, `cinf` próprios.
- **AL**: sem órgão LOB para `dpo`-aéreo à parte (coberto via grupamentos); GBM/GBS/GPA/GOA
  mapeados a `gbm`/`bbs`/`bifea`/`boa`. Sem `cint`/`ccs`/`gab-cg`-distinto-de-CG já cobertos.
  O Centro de Manutenção e Almoxarifado/Aprovisionamento (Arts. 24/27/28) são subórgãos de
  logística → não duplicados em `dlog` (já coberto por Art. 16).
- **AM**: sem `cint`/`ccs`/`condeg`-extra; Comissões (Art. 19) e COBOM (Art. 43) não têm
  `organ_key` próprio. Saúde do AM está embutida na DRH/DL → não há `dsap` autônomo.
- **AP**: ver acima (remete a decreto).
- **BA**: Alto Comando (Art. 9) e Auditoria e Finanças (Art. 26) sem `organ_key` exclusivo —
  `dpof` foi atribuído ao **Departamento de Planejamento** (planejamento+orçamento, Art. 21);
  Auditoria e Finanças fica de fora para não colidir a chave. Centros de Gestão Estratégica
  (Art. 15), Engenharia/Arquitetura (Art. 24) e Gestão de Frota (Art. 27) são subórgãos →
  não duplicados.

### Lote 2 — CE, DF, ES, MA, MG + completa GO (75 entradas no lote; GO recebe +13)

| Estado | Lei (LOB) | Órgãos com entrada | Observação |
|---|---|---|---|
| Ceará (CE) | Lei nº 13.438/2004 | 13 | LOB "por competência": finalidade-caput + incisos em vários órgãos (CAT, Defesa Civil, Logística, Financeiro, Pessoas, Colégio Militar). Nomenclatura própria (Coordenadorias/Células/Núcleos). |
| Distrito Federal (DF) | Lei nº 8.255/1991 | 8 | LOB por finalidade; órgãos de apoio (Academia, Policlínicas) e execução (Comando Operacional) descritos na lei. |
| Espírito Santo (ES) | LC nº 101/1997 (consolidada) | 13 | Finalidade-caput por órgão; os §§ do Art. 13 (DAT/DOp/DAL/DF) e Arts. 17/19/20 são **texto de Lei** (LC 705/2013), não NGA — aproveitados. |
| Maranhão (MA) | Lei nº 10.230/2015 | 18 | LOB rica: competência por órgão (§§ do Art. 13 p/ as 7 Diretorias) + finalidade dos Comandos Operacionais e Batalhões especializados. |
| Minas Gerais (MG) | LC nº 54/1999 | 8 | LOB enxuta: finalidade só de parte dos órgãos (CAT/CSM/ABM/AG c/ incisos; Comando Operacional; BBM/CIA). Diretorias (Art. 17-19) só mencionadas. |
| Goiás (GO) | Lei nº 18.305/2013 | 15 (2 já existiam) | **Completado**: +13 órgãos (CRBM, Correições, Logística, Defesa Civil, Ensino, Inteligência, Saúde, COAér, Chefia de Gabinete, Assessoria Jurídica, Secretaria-Geral, BBM, CIBM). LOB por incisos; `cg`/`dp` da amostra original intocados. |

**Casos cargo-vs-órgão (finalidade tirada da atribuição do dirigente, não de caput do órgão):**
- `(cg, ce)` Art. 8º, `(cg, df)` Art. 9º, `(cg, es)` Art. 10, `(cg, ma)` Art. 6º, `(cg, mg)`
  Art. 12 §1º — todas as LOBs descrevem o "Comando" pelo papel/atribuição do **Comandante-Geral**
  (cargo), não há finalidade-caput para o Comando-Geral como unidade.

**LOB remete a decreto/NGA (detalhe não disponível na lei):**
- **ES** (LC 101/1997) — Arts. 13/24 remetem criação/estrutura das Diretorias e subunidades a
  decreto do Governador; a **competência-caput** de cada Diretoria (DAT/DOp/DAL/DF), porém,
  consta da própria LC (via LC 705/2013) e foi aproveitada. A NGA do CBMES (camada RI) **não**
  foi usada, conforme orientado.
- **DF** (Lei 8.255/1991) — Art. 10-B/34 remetem denominação/estrutura de órgãos a ato do Poder
  Executivo; aproveitada a finalidade-caput que a lei traz para CG, Alto Comando, Controladoria,
  Ajudância, Gabinete, Academia, Policlínicas e Comando Operacional.

**Órgãos sem equivalente na LOB do estado (sem entrada), por estado:**
- **CE**: a Academia de Bombeiro Militar (Art. 29) foi **revogada** (Lei 14.629/2010) → `deei`
  usa o Colégio Militar (Art. 30, "responsável pelo sistema de ensino"). O Núcleo de Resgate e
  Emergência Pré-hospitalar (Art. 23) é operacional, não Saúde/Assistência → sem `dsap`. Núcleo
  do Interior (Art. 20) pareado ao Metropolitano em `crbm`. Sem `cint`/`ccs`/`cinf`/`dpo`-aéreo
  /`gab-cg`/`doe`/`bifea`/`boa`/`cibm` próprios na LOB.
- **DF**: Estado-Maior-Geral (Art. 11, planejamento estratégico) sem `organ_key` próprio (não é
  `dpo` operacional) → sem entrada. Departamentos/Diretorias (Art. 13) genéricos, sem finalidade
  individual → sem `dp`/`dpof`/`dlog`/`cot`/`cint`. Unidades de execução por tipo (§§2º-8º do
  Art. 28) cobertas só por `dpo` (Comando Operacional, §1º) para não pulverizar chaves.
- **ES**: Estado-Maior (Art. 11) é direção-geral de planejamento, sem chave própria → sem entrada
  (CG já cobre o Comando). Sem `dp` autônomo (pessoal está na 1ª Seção do EM / Departamento de RH,
  subórgão). Sem `cint`/`ccs`/`cinf`/`condeg`/`gab-cg`/`doe`/`bbs`/`bifea`/`boa`/`gbm`/`crbm`
  próprios (CBMES não tem comandos regionais na LOB; BBM subordina-se direto ao Comando).
- **MA**: Controladoria (Art. 15, controle financeiro) e Ouvidoria (Art. 16) ≠ Corregedoria
  disciplinar → sem `corregedoria`. Estado-Maior-Geral (Art. 10) sem chave própria. `cot` e `cat`
  ambos remetem à Diretoria de Atividades Técnicas (Art. 13 §5º) → registrada uma vez em `cat`.
  Batalhão Marítimo (§5º) e de Emergências Médicas (§6º) são operacionais sem chave própria.
- **MG**: Auditoria (Art. 16) ≠ Corregedoria → sem `corregedoria`. Estado-Maior (Art. 14) e
  Diretorias de RH/Logística/Contabilidade (Art. 17-19) **só mencionadas, sem finalidade
  individual** → sem `dp`/`dpof`. `cat`/`cot` registrados uma vez em `cat` (CAT, Art. 24). Sem
  `depdec`/`cint`/`ccs`/`cinf`/`condeg`/`gab-cg`/`doe`/`bbs`/`bifea`/`boa`/`gbm` próprios.
- **GO**: Estado Maior-Geral (Art. 14), Ajudância de Ordens (Art. 16) e Academia (Art. 31, apoio)
  e Centro de Manutenção (Art. 33) não receberam chave (ensino já em `deei` via Art. 28; Academia
  é apoio redundante). Comando Operacional de Bombeiros e Cia de Segurança Aeroportuária (Art. 34)
  sem chave própria. Sem `ccs`/`cinf`/`condeg`/`doe`/`cot`/`bbs`/`bifea`/`gbm` na LOB de GO.

### Lote 3 — MS, MT, PA, PB, PE (89 entradas)

| Estado | Lei (LOB) | Órgãos com entrada | Observação |
|---|---|---|---|
| Mato Grosso do Sul (MS) | LC nº 188/2014 (alt. até LC 333/2024) | 17 | LOB moderna: finalidade-caput por órgão ("é órgão de Direção Setorial do sistema...", "competindo-lhe") para toda a estrutura, incl. DPA/DIntel (acrescidas pela LC 323/2023). |
| Mato Grosso (MT) | LC nº 775/2023 (consolidada até LC 806/2024) | 20 | LOB rica: caput de finalidade ("é responsável por...", "presta assessoramento...") em cada Diretoria/órgão; detalhe por cargo remetido a regulamento (Art. 74). |
| Pará (PA) | Lei nº 11.060/2025 | 19 | LOB nova e detalhada: caput de finalidade em quase todos os órgãos; detalhe remetido a regulamento (Art. 67). Texto restaurado da extração OCR (rebaixava maiúsculas). |
| Paraíba (PB) | LC nº 191/2024 | 15 | LOB com "tem por finalidade"/"é responsável por" nas 7 Diretorias + EMG/CRBM/Corregedoria; detalhe remetido ao RGBM (Art. 15, XX). |
| Pernambuco (PE) | Lei nº 15.187/2013 | 18 | LOB por "incumbe-se de..."/"é responsável por..." em quase todos os órgãos; DGP/DLog (Art. 15/17) têm incisos enumerados (3 e 5). |

**Casos cargo-vs-órgão (finalidade tirada da atribuição do dirigente, não de caput do órgão):**
- `(cg, ms)` Art. 8º, `(cg, mt)` Art. 12, `(cg, pa)` Art. 8º, `(cg, pb)` Art. 15, `(cg, pe)`
  Art. 10 — todas as LOBs descrevem o "Comando" pela atribuição/responsabilidade do
  **Comandante-Geral** (cargo); não há finalidade-caput do Comando-Geral como unidade.

**LOB remete a decreto/Regimento (detalhe não disponível na lei):**
- **MT** (LC 775/2023) — Art. 74 remete finalidade/atribuições/competências de detalhe de
  cada unidade a regulamento do Comandante-Geral; o **caput** de cada órgão, porém, consta da
  própria LC e foi aproveitado. A camada RI de MT (`ENRICHMENT_ORGAN`, em `minuta_enrichment.py`)
  é distinta e não foi tocada.
- **PA** (Lei 11.060/2025) — Art. 67 remete atribuições/detalhamento/competências dos órgãos à
  regulamentação; a finalidade-caput de cada órgão consta da Lei e foi aproveitada.
- **PB** (LC 191/2024) — Art. 15, XX remete competências e estrutura pormenorizadas ao
  Regulamento Geral (RGBM); a finalidade-caput de cada Diretoria/órgão consta da LC.

**Órgãos sem equivalente na LOB do estado (sem entrada), por estado:**
- **MS**: Estado-Maior-Geral (Art. 11, gestão administrativa/orçamentária) sem `organ_key`
  próprio (não é `dpo` operacional) → sem entrada; CG já cobre a direção. Sem `dpo`/`doe`/`cat`
  /`ccs`/`bbm`/`cibm`/`bbs` próprios (execução é GBM/SGBM, mapeada em `gbm`; `crbm` usa o CMB,
  Grande Comando). Órgãos de apoio redundantes (CSM, Policlínica, CRAPH, CapMil) são subórgãos de
  `dlog`/`dsap` → não duplicados.
- **MT**: Comando-Geral Adjunto/Chefe do EMG (Art. 17) e EMG (Art. 19) são direção superior de
  controle, sem chave própria → sem entrada. Controladoria/Ouvidoria (Arts. 22-23) ≠ Corregedoria
  → cobertas só pela Corregedoria Geral (Art. 20). Sem `cinf` próprio (TI é seção da Diretoria de
  Administração Institucional) → não duplicado; `dlog` usa essa Diretoria (administração+logística).
  Sem `bbs`/`cibm`/`gbm`/`cat` próprios (BBM cobre a execução; `bifea` usa o BEA).
- **PA**: Estado-Maior Geral (Art. 11) e Departamento-Geral de Administração (Art. 18, dirige as
  Diretorias) sem chave própria → sem entrada (DAL/DF/DTIC/DS já mapeadas individualmente). Grupo
  de Operações Aéreas (Art. 49) **remete atribuições/composição a regulamento** (§ único) → sem
  finalidade-caput, sem `boa`. GMAF/GSE/NAC são especializadas sem chave própria (`bbs` usa o GBS).
  Controladoria Interna (Art. 26) ≠ Corregedoria (usada a Corregedoria-Geral, Art. 15).
- **PB**: **não tem CEDEC** (defesa civil é competência do CG, sem órgão central na LOB) → sem
  `depdec`. Comunicação Social e Inteligência são **coordenadorias do EMG** (5ª e 2ª, subdivisões),
  não órgãos com finalidade própria → sem `ccs`/`cint`. Controladoria Interna (Art. 29) ≠
  Corregedoria → cobertas em separado (CORREG, Art. 30). Execução (BBM/CIBM) sem caput de finalidade
  na LC → sem `bbm`/`gbm`. `dpo` usa o EMG (planejamento estratégico/operacional, 3ª EMG).
- **PE**: **não tem órgão aéreo nem florestal/ambiental** próprio → sem `boa`/`bifea`. DPlaG
  (Planejamento e Gestão, Art. 21) e DF (Finanças, Art. 19) mapeariam ambas a `dpof` → usada a DF;
  DPlaG fica de fora para não colidir a chave. DInter/1 e DInter/2 (Arts. 27/29) são pares regionais
  da DIM → `crbm` registrado uma vez (DIM). `corregedoria` usa o Centro de Justiça e Disciplina
  (Art. 60, PAD/sindicância/IPM); CCI (Art. 64) é controladoria de gestão, fora. `dsap` usa o CAS
  (assistência); CEFD/CPPA são subórgãos de pessoal. Execução por Grupamentos: `gbm`=GB (Art. 83 V),
  `bbs`=GBS (Art. 83 IV); GBI/GBAPH/GBMar sem chave própria.

Ao ampliar (Lotes 4–5), editar `scripts/lob_enrichment.py` e reexecutar
`python scripts/build_minuta_comparison.py` (e `python scripts/_check_lob_merge.py`).
