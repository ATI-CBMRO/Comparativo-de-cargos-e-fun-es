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

### Lote 4 — PI, PR, RJ, RN, RR (53 entradas)

| Estado | Lei (LOB) | Órgãos com entrada | Observação |
|---|---|---|---|
| Piauí (PI) | Lei nº 5.949/2009 (alt. Lei nº 7.772/2022) | 12 | LOB com finalidade-caput por órgão ("é órgão de direção setorial...", "incumbe-se de..."); detalhe de atribuições remetido ao RACBMEPI (Art. 48). |
| Paraná (PR) | Lei nº 22.206/2024 | 15 | LOB moderna e detalhada, com incisos enumerados na maioria dos órgãos; números de artigo confirmados contra o site oficial do CBMPR, pois a extração em markdown intercala blocos de "Art. N." soltos no rodapé de página, fora de ordem 1:1 com os parágrafos. |
| Rio de Janeiro (RJ) | Lei nº 250/1979 | 11 | LOB antiga e fundacional (CBERJ); finalidade-caput por órgão ("é o Órgão de Direção Setorial do sistema..."), sem incisos enumerados na maior parte. |
| Rio Grande do Norte (RN) | LC nº 230/2002 (alt. até LC 791/2025) | 1 | LOB extremamente sucinta — trata sobretudo de efetivo/quadros/transição da PM; estrutura dos órgãos é deixada a decreto do Poder Executivo (Art. 20). Único órgão com finalidade própria na lei é o Conselho Superior (Art. 9º). |
| Roraíma (RR) | LC nº 52/2001 (consolidada até LC nº 265/2018) | 14 | LOB rica e detalhada, com estrutura em níveis (direção superior/setorial/execução); usado o texto CONSOLIDADO (redação mais recente de cada artigo alterado, não a redação original revogada). |

**Casos cargo-vs-órgão (finalidade tirada da atribuição do dirigente, não de caput do órgão):**
- `(cg, rj)` Art. 9º — a LOB do CBERJ descreve o "Comando" pela atribuição/responsabilidade do
  **Comandante-Geral** (cargo); não há finalidade-caput do Comando-Geral como unidade.

**LOB remete a decreto/Regimento (detalhe não disponível na lei):**
- **PI** (Lei 5.949/2009 alt. 7.772/2022) — Art. 48 remete o detalhamento de atribuições dos
  órgãos ao Regulamento da Administração do CBMEPI (RACBMEPI); a finalidade-caput de cada órgão
  consta da própria lei e foi aproveitada.
- **RN** (LC 230/2002) — Art. 20 remete a criação, transformação, extinção, denominação,
  localização e estruturação de TODOS os órgãos de direção/assessoramento/execução a decreto do
  Poder Executivo — o caso mais extremo de deferência a decreto observado nos quatro lotes; por
  isso a LOB de RN só rendeu 1 entrada (Conselho Superior, Art. 9º).
- **RR** (LC 52/2001) — várias Diretorias subordinadas ao Estado-Maior Geral Bombeiro-Militar
  (Art. 27: DPL, DIE, DEIOp, DAL, DPST, DACRP, DGOF, DCI) têm, na lei, apenas a estrutura
  (subórgãos) listada, sem caput de finalidade individual; usado o texto estrutural disponível
  ("tem a seguinte estrutura") como `finalidade` mínima verbatim, sem invenção de competências.

**Órgãos sem equivalente na LOB do estado (sem entrada), por estado:**
- **PI**: Estado-Maior-Geral (Art. 28-A, direção de planejamento) sem chave própria → sem
  entrada (CG/Diretorias já cobrem a estrutura). Núcleo de Investigação e Prevenção de Incêndios
  (Art. 35) é subórgão técnico redundante de `cot` → não duplicado. Sem `cint`/`ccs`/`cinf`/
  `gab-cg`/`doe`/`cibm`/`bifea`/`boa`/`corregedoria` próprios na LOB.
- **PR**: Estado-Maior (Art. 14) é direção de planejamento sem chave própria → sem entrada.
  Assessoria Estratégica (Art. 17) e Secretaria do Comando-Geral (Art. 19) colidiriam com
  `assessorias`/`gab-cg` já preenchidas por órgãos mais específicos (Consultoria Institucional,
  Art. 20; Gabinete, Art. 15) → não duplicadas. Comissões (Art. 21) e Assessorias Militares
  (Art. 22) são órgãos colegiados/de ligação sem finalidade-caput própria → sem entrada. Sem
  `depdec`/`cint`/`cinf`/`doe`/`gbm` próprios na LOB.
- **RJ**: Estado-Maior-Geral (Art. 13) é órgão de planejamento sem chave própria → sem entrada.
  Sem `depdec`/`condeg`/`cint`/`cinf`/`gab-cg`/`doe`/`cibm`/`gbm`/`bifea`/`boa`/`corregedoria`
  próprios na LOB de 1979 (estrutura muito mais simples que as LOBs recentes).
- **RN**: lei não nomeia individualmente nenhum outro órgão de direção/execução (Art. 20 remete
  tudo a decreto) → sem `cg`/`dp`/`deei`/`dpof`/`dsap`/`dlog`/`dpo`/`doe`/`cot`/`cat`/`cint`/
  `ccs`/`cinf`/`crbm`/`bbm`/`cibm`/`bbs`/`bifea`/`boa`/`gbm`/`corregedoria`/`assessorias`/
  `gab-cg`/`ag`/`depdec`.
- **RR**: Estado Maior Geral Bombeiro-Militar (Art. 26) é "OBM de Atuação Colegiada" com
  Diretorias operacionais subordinadas e emite diretrizes — não se ajusta ao padrão de
  `condeg` (conselho puramente consultivo/deliberativo) → sem entrada; documentado como
  EXCLUÍDO, não como esquecimento. Colisão em `ccs`: Assessoria de Comunicação e Imprensa do
  Gabinete (Art. 18) vs. Diretoria de Assuntos Civis e Relações Públicas - DACRP (Art. 34) →
  usada a DACRP (órgão de Diretoria, mais robusto na estrutura) e a ACI do Gabinete deixada de
  fora para não duplicar a chave. Sem `crbm`/`bbm`/`cibm`/`bbs`/`bifea`/`boa`/`gbm`/
  `gab-cg`/`assessorias` próprios — a lei não dá finalidade-caput a esses níveis (`doe` usa o
  Comando Operacional da Capital e do Interior, Art. 37).

### Lote 5 — RS, SE, SP, TO (+ SC completo) (62 entradas)

| Estado | Lei (LOB) | Órgãos com entrada | Observação |
|---|---|---|---|
| Rio Grande do Sul (RS) | Dec. nº 53.897/2018 (regulamenta a LC nº 14.920/2016) | 9 | Decreto regulamentador enxuto: finalidade-caput por artigo, sem incisos enumerados; competências de detalhe das Divisões/OBM remetidas ao Regimento Interno do CBMRS (não disponível no corpus). |
| Sergipe (SE) | Lei nº 8.979/2022 | 16 | LOB moderna por Diretorias ("é responsável pela gestão, planejamento, coordenação, execução, fiscalização e controle de..."); finalidade-caput por órgão, sem incisos por Diretoria (exceção: Alto-Comando, Art. 20, com incisos). |
| São Paulo (SP) | Lei nº 616/1974 | 9 | LOB da Polícia Militar do Estado de São Paulo como um todo; o Corpo de Bombeiros é Seção II (Art. 38-43), subordinado ao Comando Geral da PM. `cg` usa o Comando do Corpo de Bombeiros (Art. 39, específico do CB); demais entradas (DP, DF, DAL, DE, DS, AG) são Diretorias/órgãos de toda a PM-SP, ao nível hierárquico equivalente ao do CBMRO, mantidas como camada de referência. |
| Tocantins (TO) | LC nº 131/2021 | 17 | LOB moderna por "Unidades Administrativas" (Direção Superior/Setorial/Assessoramento Geral/Apoio/Execução); finalidade-caput por artigo, com incisos só no Comando de Correição e Disciplina (Art. 12) e na Assessoria de Inteligência (Art. 19, I). |
| Santa Catarina (SC) — completa | Dec. nº 1.328/2021 (regulamenta a LC nº 724/2018) | +13 (total 15) | Completa as 2 entradas já existentes (`cg`, `dp`); demais órgãos têm finalidade-caput com incisos detalhados no Título III ("DOS ÓRGÃOS DE DIREÇÃO/APOIO/EXECUÇÃO"). |

**Casos de tiering / órgão guarda-chuva (uma única chave para órgão que combina mais de uma competência):**
- `(dlog, rs)` Art. 12 — o "Departamento Administrativo" do CBMRS combina recursos humanos,
  orçamento/finanças, logística/patrimônio e TI num único órgão; mapeado em `dlog` por ser a
  competência citada com maior peso estrutural na lei; RS não tem `dp`/`dpof`/`cinf` próprios
  por essa razão (ficariam duplicados do mesmo caput).
- `(dlog, to)` Art. 18, III e `(dpof, to)` Art. 15 — TO desdobra a competência financeiro-
  patrimonial em dois níveis (Comando de Gestão de Recursos Financeiros e Patrimoniais, e sua
  Diretoria de Logística e Patrimônio subordinada); usado o nível de Comando para `dpof`
  (citação mais geral, com "orçamento, finanças, logística e infraestrutura") e o nível de
  Diretoria para `dlog` (citação específica de "logística e patrimônio"), evitando duplicar o
  mesmo caput nas duas chaves.
- `(dp, to)` usa o Comando de Gestão de Pessoas (Art. 14, nível de Comando) em vez da Diretoria
  de Administração e Gestão de Pessoas subordinada (Art. 18, I) — critério já usado no Lote 2
  (GO): preferir o nível de Comando quando tem finalidade-caput própria.
- `(dsap, sc)` Art. 36 — a "Diretoria de Urgência e Emergência" do CBMSC é o órgão mais próximo
  de saúde/assistência (atendimento pré-hospitalar/integração com sistema de saúde) entre as
  Diretorias setoriais; mapeada em `dsap` por analogia funcional, embora o nome não use
  "Saúde".
- `(dlog, sc)` Art. 37 — a "Diretoria de Logística e Finanças" do CBMSC combina logística,
  patrimônio, TI e telecomunicações num único órgão; mapeada em `dlog` (mesmo critério do RS),
  SC não recebe `dpof`/`cinf` próprios por essa razão.

**Casos cargo-vs-órgão / colisão entre dois órgãos pela mesma chave (escolha do mais específico):**
- `(deei, sc)` — colisão entre a Diretoria de Instrução e Ensino (Art. 35) e o CEBM (Centro de
  Ensino Bombeiro Militar, Art. 40); usada a Diretoria (órgão de direção setorial com
  finalidade-caput mais abrangente: formação, aperfeiçoamento, pesquisa, gestão do
  conhecimento), CEBM deixado de fora para não duplicar a chave.
- `(assessorias, sc)` — colisão entre a Assessoria Jurídica (Art. 32) e as 3 Assessorias
  Especiais (Integração de Serviços Auxiliares, Assuntos Institucionais, Inovação — Art. 43-46);
  usada a Assessoria Jurídica por ser a mais diretamente análoga ao padrão "Assessoria Jurídica"
  já usado como `assessorias` em outros estados; as 3 Assessorias Especiais ficaram fora.
- `(assessorias, to)` Art. 19, II — Assessoria Jurídica, sem colisão.

**LOB remete a decreto/Regimento (detalhe não disponível na lei):**
- **RS** (Dec. 53.897/2018) — após os Art. 12, 13, 14, 15, 19, 20 e 21, o texto remete
  expressamente as competências de detalhe das Divisões e dos OBM ao Regimento Interno do
  CBMRS (não disponível no corpus); por isso quase todas as entradas de RS têm
  `competencias: []`, com `finalidade` extraída do caput do artigo regulamentador.
- **SE** (Lei 8.979/2022) — Art. 4º, parágrafo único, remete a estrutura interna e as
  competências de detalhe das Diretorias ao Regimento Interno do CBMSE; entradas de SE são, em
  sua maioria, finalidade-caput sem incisos (exceções: Alto-Comando, Art. 20, com incisos
  próprios na lei).

**Órgãos sem equivalente na LOB do estado (sem entrada), por estado:**
- **RS**: lei muito enxuta — sem `depdec`/`cint`/`ccs`/`cinf`/`cat`/`doe`/`cibm`/`bbs`/
  `bifea`/`boa`/`gbm`/`assessorias` próprios; estrutura interna das Divisões remetida ao
  Regimento Interno (não disponível).
- **SE**: Controladoria Interna (Art. 16) e Ouvidoria-Geral (Art. 17) sem chave própria entre as
  26 → sem entrada. Sem `depdec`/`cat`/`cint`/`cinf`/`doe`/`cibm`/`bifea`/`boa`/`dsap`
  próprios na lei.
- **SP**: a lei é da Polícia Militar como um todo; órgãos PM-wide sem equivalente CB-exclusivo
  específico foram, ainda assim, mantidos (DP/DF/DAL/DE/DS/AG, Art. 14-19) por serem o nível
  hierárquico de apoio ao qual o CB efetivamente se reporta (Art. 26 confirma que essas
  Diretorias atendem a toda a PM, sem órgão equivalente próprio do CB). Sem `depdec`/`condeg`/
  `corregedoria`/`cot`/`cat`/`cint`/`ccs`/`cinf`/`crbm`/`assessorias`/`gab-cg`/`dpo`/`doe`
  próprios e exclusivos do CB na Lei 616/1974.
- **TO**: Assessoria de Gestão Estratégica (Art. 19, IV) e Comissões (Art. 19, VII) sem chave
  própria → sem entrada. Academia de Formação de Bombeiros (Art. 21, II) e Colégios Militares
  (Art. 21, III) colidiriam com `deei` já preenchida pela Diretoria de Ensino e Pesquisa (Art.
  18, II) → não duplicadas. Assessoria Parlamentar (Art. 21, IV) sem chave própria → sem
  entrada. Sem `cat`/`doe`/`cibm`/`bbs`/`bifea`/`boa`/`gbm` próprios na lei.
- **SC (completo)**: Controladoria Interna (Art. 29) sem chave própria → sem entrada.
  Coordenadorias Operacionais (Art. 41) são grupos de trabalho consultivos sem finalidade-caput
  própria de órgão → sem entrada. BBM Comando e Serviços e BBM Ajuda Humanitária (Art. 53-54)
  sem chave própria entre as 26 → sem entrada. Sem `depdec`/`dpof`/`cinf`/`dpo`/`doe`/`cat`/
  `cibm`/`bbs`/`bifea`/`gbm`/`gab-cg` próprios na completação deste lote (já cobertos ou sem
  equivalente).

### Cobertura final (encerramento da curadoria por estado)

Com o Lote 5, a camada LOB cobre os **26 estados não-RO** (todos com pelo menos 1 entrada) e os
**26 órgãos da LOB do CBMRO**, totalizando **338 entradas**. Cobertura por órgão (estados/26):
`cg` 23, `deei` 23, `ag` 22, `dlog` 21, `dp` 19, `crbm` 18, `corregedoria` 18, `dpof` 17, `cot` 17,
`dsap` 16, `condeg` 15, `assessorias` 15, `gab-cg` 15, `bbm` 13, `depdec` 10, `cint` 10, `cinf` 10,
`dpo` 11, `bbs` 9, `boa` 7, `ccs` 6, `bifea` 6, `gbm` 6, `cat` 5, `cibm` 4, `doe` 2. Órgãos com baixa
cobertura (`doe`, `cibm`, `cat`, `gbm`, `bifea`, `ccs`) refletem estrutura genuinamente ausente nas
leis (muitas LOBs remetem subdivisões operacionais a decreto/RI), não lacuna de pesquisa.

Para ampliar esta camada no futuro, editar `scripts/lob_enrichment.py` e reexecutar
`python scripts/build_minuta_comparison.py` (e `python scripts/_check_lob_merge.py`).
