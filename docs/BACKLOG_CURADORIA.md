# Backlog de Curadoria — Portal CBM

> Gerado pela varredura de qualidade de 2026-06-07. Score composto 0–100:
> profundidade estrutural (nós + nº órgãos), cobertura de cargos (órgãos com `cargos[]`),
> e riqueza de atribuições (total + comprimento médio do texto).
> Reproduzir: ver o script de auditoria ad-hoc no histórico ou recalcular a partir de
> `database/states_data.json` + `database/organs_detail/*.json`.

## Progresso

- **2026-06-07** — Varredura de qualidade dos 27 estados; criado este backlog; corrigida
  doc desatualizada sobre `CURATED_ORGANS` (cobre os 27, profundidade varia). Confirmado:
  zero corrupção de encoding (o `�` é só renderização cp1252 do console).
- **2026-06-07** — **RR investigado e curado**: não era bug; lacuna de fonte. +9 cargos
  "Comandante" nos Centros (cobertura 6/31 → 15/31). Detalhes na seção RR abaixo.
- **2026-06-07** — **SP curado** (score 33 → 65): baixada e salva a fonte correta do CBMSP
  — Lei nº 616/1974 (atual. até Lei nº 735/1975) — em `database/markdown/São Paulo -
  Organização Básica (Lei 616-1974).md`. Reconstruídos detalhamento (3 → 13 órgãos) e
  árvore (7 → 54 nós) a partir dos Arts. 38 a 43, mantendo os comandos modernos do
  Decreto 65.096/2020 (CBM/CBI) com baseLegal rastreável. Todos os 13 órgãos com detailId
  ligado. Fidelidade total: cada atribuição cita artigo/inciso, sem invenção.
- **2026-06-07** — **AP curado** (score 48 → 57): atribuições alinhadas à finalidade
  VERBATIM de cada categoria (Art. 6º, §§1º–6º da LC 180/2026), adicionado o órgão
  "Comando Operacional" (direção-geral, que faltava), Escola Militar reclassificada como
  órgão vinculado, cargos de CG/Subcomandante enriquecidos com o Art. 3º. avgLen 32→133.
- **2026-06-07** — **RN investigado** (score 48, source-capped): a LC 230/2002 DELEGA a estrutura
  detalhada a decreto (não disponível naquela data). Tornado fiel ao máximo possível pela LC.
- **2026-06-09** — **RN curado verbatim** (score 48 → **100**, 🟢 T4): localizado e baixado o
  **Decreto nº 31.139, de 1º de dezembro de 2021** (Regulamento Geral do CBMRN) via Diário
  Oficial do RN (doc 749493, TLS bypass). Documento salvo em `database/markdown/`. Bloco
  reescrito: 5 → 28 órgãos verbatim; IDs alinhados à nova árvore curada (cmt-rn, scmt-rn,
  csup-rn, gab-rn, ajg-rn, uci-rn, cpp-rn, cped-rn, assint-rn, cmdoop-rn, emop-rn, cocbm-rn,
  codec-rn, gbm1-rn, gbm2-rn, gbmar-rn, sibm-aph-rn, dlof-rn, cafo-rn, dgpei-rn, crh-rn,
  csfa-rn, dat-rn, carip-rn, cf-rn, cat1-rn, cat2-rn + 1 adicional). Art. 13 I–XIX no CG (19
  itens); Art. 15 I–XIII no SCG (13 itens); Art. 17 I–IX no Conselho Superior; Art. 24 I–IX na
  UCI; Art. 39 I–XVI no CAFO (16 itens); Art. 40 I–VI na DGPEI; Art. 41 I–VIII no CRH; Art. 42
  I–V no CSFA; demais órgãos com caput verbatim. Todos 28/28 com cargos. nodes 7→85,
  totAtrib 22→175, avgLen 100→154.6.
- **2026-06-07** — **AC investigado** (mantido): falso alarme — não é verbatim, árvore já
  completa/fiel, lei curta e estrutural (source-capped). Sem ação.
- **2026-06-07** — **RS curado verbatim** (score 78 → 87 → **93**, 🟢 T4): (1) competência
  institucional do CBMRS verbatim (RI Art. 1º, I–X) no Comando-Geral; (2) definição verbatim
  (caput) de cada órgão a partir do Regimento — Corregedoria (Art. 30), Gabinete (Art. 31),
  Dep. Administrativo (Art. 34), DSPCI (Art. 35), ABM (Art. 36), AODC (Art. 37), CRBM (Art. 38),
  BESCI (Art. 39); (3) cargos titulares com requisito QOEM e atribuições verbatim (Comandante-Geral
  Art. 27, Subcomandante Art. 28, Corregedor-Geral Art. 46, Chefe de Gabinete Art. 47, Diretores
  Arts. 49/50, Comandantes Arts. 51/54/55, Diretor AODC Art. 52). wCarg 8→10/10, avgLen 56→124.
  NOTA: as competências granulares por subunidade ("Por meio da X, compete...") são boilerplate
  repetido — caput é o conteúdo distintivo; transcrito o essencial sem inchar.
- **2026-06-07** — **GO e SE investigados** (NÃO são candidatos a verbatim in-project): os
  "Regimentos" de GO ("dos Serviços Interno e Operacional") e SE ("Regimento Interno") são
  REGULAMENTOS DE SERVIÇO DIÁRIO (escalas, Superior/Supervisor de Dia, Oficial de Dia,
  guarnições), não definem atribuições de órgãos/comandos. GO ainda vem fragmentado (14
  chars/linha). A estrutura de ambos vem das LOBs, que NÃO estão no projeto (GO: dispersa na
  ampla Lei 21.792/2023; SE: LOB própria). Ambos já estão decentes (GO 82, SE 84) com
  atribuições parafraseadas curtas. Para verbatim, seria preciso BAIXAR as LOBs (estilo SP).
- **2026-06-07** — **GO curado verbatim via fetch** (score 82 → **97**, 🟢 T4): identificada a
  LOB CORRETA do CBMGO — **Lei nº 18.305/2013** (a 16.899/2010 é só efetivo; a 21.792/2023 é lei
  ampla de administração, sem estrutura do CBMGO) — baixada da Casa Civil/GO (legisla.casacivil)
  e salva em `database/markdown/Goiás - Organização Básica (Lei 18.305-2013).md`. Competência
  institucional (Art. 2º, I–VII) verbatim no EMG; 5 Comandos setoriais transcritos verbatim —
  CCD (Art. 24, 17 incisos), CAL (Art. 25), CGF (Art. 26), CODEC (Art. 27), CAEBM (Art. 28) —
  com requisito de comando (Coronel QOC + CSBM, Art. 23 §1º). Referências legais corrigidas
  (citavam erradamente a 21.792/2023). NOTA: CAT/CGE/CME/COA/COB/CSAU/CEMAN são Comandos
  pós-2013 (fonte não localizada) — mantidos como estavam.
- **2026-06-07** — **SE curado verbatim via fetch** (score 84 → **96**, 🟢 T4): LOB correta do
  CBMSE é a **Lei nº 8.979, de 03 de fevereiro de 2022** (baixada de aleselegis.al.se.leg.br,
  windows-1252), salva em `database/markdown/Sergipe - Organização Básica (Lei 8.979-2022).md`.
  Atribuições do Comandante-Geral (Art. 7º, I–XX) verbatim como 20 itens individuais; SCG
  (Art. 9º, I–VI) como 6 itens; caput verbatim para todos os outros 24 órgãos. Adicionados 10
  órgãos faltantes: 7 CRBMs (CRAS/CRMS/CRCS/CRS/CRL/CRA/CRBSF), 1 GBM agregado (8 GBMs Art. 37),
  GBS (Art. 39 I), GOA (Art. 39 II). Árvore curada atualizada (curated_organs_p2.py): 42→132 nós
  com hierarquia correta — DOP→CRBMs→GBMs. nOrg 16→26, wCarg 16/16→26/26, totAtrib 70→50,
  avgLen 56→169 chars.
- **CONCLUSÃO**: fetch de LOB externa (estilo SP/GO/SE) é o caminho de maior ganho. SE +11 pts,
  GO +15 pts. Mesmo método aplicável a outros.
- **2026-06-07** — **MG curado** (score 70 → **76**, 🟠 T2): LC 54/1999 curta e estrutural
  (source-capped). Todos 11 órgãos com cargos e requisitos corretos; CAT (Art. 24, I–III),
  Ajudância-Geral (Art. 25, I–III) e Estado-Maior (Art. 14, I–II) transcritos verbatim;
  csm-mg: 3 atribuições fabricadas removidas — lei só diz "suprimento logístico" (Art. 23).
- **2026-06-09** — **MG refinado** (score 76 → **92.6**, 🟢 T4): adicionados CEB (Resolução nº 898,
  de 2 abr 2020), BOA e BEMAD — 3 novos órgãos criados via resolução interna não prevista na LC 54/1999.
  Missão do CEB verbatim: "coordenar, em âmbito estadual, as atividades operacionais especializadas do
  CBMMG". BOA: 4 companhias em BH, Varginha, Montes Claros e Uberaba. BEMAD: CQBRN, CBS, Cia BRESC,
  CPA. Árvore: 41 → 54 nós. totAtrib: 18 → 47. nOrg: 11 → 14. Fontes: bombeiros.mg.gov.br/boa,
  bombeiros.mg.gov.br/bemad, notícia 5 anos CEB (oficial CBMMG).
- **2026-06-09** — **AC refinado** (score 72 → **97.8**, 🟢 T4): Lei nº 2.009/2008 (red. até Lei nº 4.428/2024)
  baixada de legis.ac.gov.br via PowerShell -SkipCertificateCheck (cbmac.ac.gov.br estava fora do ar).
  Reescrita completa de 16 órgãos com atribuições verbatim (Art. 5º–15º, Art. 24 I–XI); adicionada
  Ajudância Geral (Art. 11 e Art. 7º X) como 17º órgão; EMG corrigido com 2 cargos; todos os desdobramentos
  dos COBs (7 BEPCIFs + 1º BBS + 2 CIACIAERs) listados verbatim. avgLen: 35 → 166. totAtrib: 51 → 57.
  Fonte: legis.ac.gov.br/detalhar/3521 (texto compilado com todas as alterações).
- **2026-06-07** — **CE curado verbatim via fetch** (score 76 → **90**, 🟢 T4): LOB do CBMCE
  é a **Lei nº 13.438, de 07 de janeiro de 2004** (baixada de belt.al.ce.gov.br, UTF-8), salva
  em `database/markdown/Ceará - Organização Básica (Lei 13.438-2004).md`. Bloco reescrito de
  9 → 18 órgãos. Atribuições verbatim: SE (Art. 12, I–VII + §1º), AJur (Art. 14, I–IV), CAT
  (Art. 17, I–IV), NDC (Art. 21, I–II), CLog (Art. 26, I–IV), NF (Art. 27, I–V), CGFP (Art. 28,
  I–V), ABM (Art. 29, I–II), CMCB (Art. 30, I–VII). 9 novos órgãos operacionais (NBM, NBI, NDC,
  NBS, NREPH, CLog, NF, CGFP, CMCB). Todos 18 órgãos com cargos e requisitos da lei.
- **2026-06-07** — **PE curado verbatim via fetch** (score 77 → **100**, 🟢 T4): LOB do CBMPE
  é a **Lei nº 15.187, de 12 de dezembro de 2013** (baixada de legis.alepe.pe.gov.br, UTF-8),
  salva em `database/markdown/Pernambuco - Organização Básica (Lei 15.187-2013).md`. Bloco
  reescrito de 11 → 23 órgãos. Subcomandante-Geral: Art. 93 I–IX verbatim (9 itens). Todas
  as 8 Diretorias: atribuição específica + Art. 95 I–XII (12 itens comuns verbatim). Apoio
  (GCG, AJ, AJG, CJD, CCI): Art. 96 I–X (10 itens comuns verbatim). Execução (COM, COEsp,
  COInter/1, COInter/2, CCO, CRD, CATs): Art. 97 I–XV (15 itens comuns verbatim). Árvore
  expandida de 22 → 85 nós (exec stub explodida: COM→4 GBs, COEsp→5 CATs, COInter/1→4 GBs,
  COInter/2→3 GBs; 14 órgãos de apoio sob CG/SCG). Todos 23 órgãos com cargos.
- **PI** ✅ CURADO 2026-06-08 (score 77→90). Lei 5.949/2009 + 7.772/2022: 29 órgãos verbatim (estrutural/prosa, sem incisos por órgão exceto Alto Comando §2° I–VIII). Árvore expandida, todos 29 órgãos com cargos e requisitos.
- **MA** ✅ CURADO 2026-06-09 (score 80→93). Lei 10.230/2015: 26 órgãos verbatim. Art. 2 I–X no CG, Art. 9 I–III no Alto-Comando, Art. 13 caput+§§ nas 7 Diretorias, demais Arts. verbatim. Árvore: +BBMar/BBEM/BBS/BBA + CoordMédica/CoordOdonto.
- **RJ** ✅ CURADO 2026-06-09 (score 83→95). Lei 250/1979: 9→25 órgãos verbatim. Art. 2 I–VI no CG; Art. 30 pú split (6 itens) na AjG; todos os Apoio (CSS, CSBM, EsFAO/cursos, CFAP/cursos, PagC, 5 CSMs, HCB, PolCB) e Exec (CBA, COCB, GI, GBS, Gmar) com cargos.
- **BA** ✅ CURADO 2026-06-09 (score 85→**99**, 🟢 T4). Lei 14.572/2023: 18→29 órgãos verbatim. Art. 2 I–XX + §3º I–V + Art. 11 no CG (26 itens); Art. 49 I–XXVII nos cargos titulares (CG, SCG, COBM, CSCI, Corregedor, Diretores VI, IMESB VII, CRBMs VIII, ABM IX, Saúde X, Inteligência XI, CFAP XII, CTO XIII, Frota XIV, BBM XXVII, CGVA XXV, CEA XXX). Árvore: +alto-cmd-ba, +conselho-ba, scmt-ba expandido (+gab-scmt-ba, +cge-ba). cobm enriquecido com 4 CRBMs como desdobramentos; imesb com 3 subordinadas; bbm-ba com 20 BBMs + Companhias (Art. 55 XIV confirma 20 Comandantes de Batalhão). nodes 35→60.
- **SC** ✅ CURADO 2026-06-09 (score 75.8→**98.7**, 🟢 T4). Dec. 1.328/2021 (LC 724/2018): 13→23 órgãos verbatim. IDs corrigidos para casar com árvore curada (cg-sc, scmt-sc, gab-sc, ag-sc, correg-sc, dp-sc + novos ccs-sc, ce-sc, ass-jur-sc, aci-sc, aeis, aeai, aei-sc, bbm-sc). Art. 14 I–IX no CG; Art. 16 I–V no SCG; Art. 17 I–V no EMG; Art. 26 I–II no Gab; Art. 27 §1 I–VIII na AjG; Art. 30 I–III no CE; Art. 32 I–VI na AJ; Art. 28 I–XIII no CCS; Art. 33 I–VIII na Correg; Art. 34 I–XLIII na DP; Art. 35 I–XI na DIE; Art. 36 I–XIII na DUE; Art. 37 I–XXIX na DLF; Art. 38 I–V na DSCI; Art. 39 I–IX em cada RBM; Art. 40 I–X no CEBM; Art. 42 I–XI na ACI; Art. 44 I–XX na AEIS; Arts. 45–46 nas demais Assessorias; Art. 51 I–X nos BBMs. totAtrib 42→241, avgLen 30→127, wCarg 13→22.
- **TO** ✅ CURADO 2026-06-09 (score 87→**95.8**, 🟢 T4). LC 131/2021: 16→26 órgãos verbatim, IDs corrigidos para casar com árvore curada (cg-to, chem, subchem, em-to, ccd-to, cadc-to, cgp-to, cgrf-to, cat-to, cobm-to + novos gab-to, ai-to, aj-to, acs-to, age-to, ati-to, ap-to, dagp-to, dep-to, dlp-to, dof-to, dsas-to, dst-to, ag-to, acad-to, ubm-to). Art. 2 I–XI no CG (institucional); Art. 7 no CG; Art. 8 no CHEM; Art. 9 §3º no SUBCHEM; Art. 10–11 no EM; Art. 12 I–IV no CCorD; Arts. 13–17 nos demais Comandos de Seção; Art. 18 I–VI nas Diretorias; Art. 19 I–VI nas Assessorias (ai-to: a-e verbatim; gab-to: a-e verbatim); Art. 21 I/II/IV nos órgãos de Apoio; Arts. 23–24 na UBM. Todos 26/26 com cargos. totAtrib 34→54, avgLen 55→160, wCarg 15→26.
- **PB** ✅ CURADO 2026-06-09 (score 88→**100**, 🟢 T4). LC 191/2024: 15→21 órgãos verbatim, IDs corrigidos para casar com árvore curada (cg-pb, gcg-pb, gscmdg, scg-pb, ouv-pb, ari-pb, ccg-pb, qcg-pb, ac-pb, emg-pb, ci-pb, correg-pb, crbm-pb, dal-pb, dat-pb, dep-pb, df-pb, dgp-pb, ds-pb, dti-pb, exec-pb). Art. 15 §3º I–XXXVI (36 itens verbatim) no CG; Art. 17 §3º I–VII no SCG; Art. 28 §4º I–IX no EMG; Art. 44 I–IX na exec; caput verbatim nos demais 17 órgãos. Todos 21/21 com cargos. totAtrib 68→119, avgLen 53→153.
- **AL** ✅ CURADO 2026-06-09 (score 89→**94**, 🟢 T4). RI/CBMAL Dec. 408/2001: único órgão sem cargo (ubm-al) recebeu Art. 113 I–VII (7 itens verbatim de UOp) + cargo Comandante de Grupamento com Art. 114 I–XV verbatim. wCarg 13→14/14, totAtrib 91→111, avgLen 58→68.
- **AM** ✅ CURADO 2026-06-09 (score 89→**91.9**, 🟢 T4). Lei 2.538/1999: 2 órgãos sem cargo (cedec-am, cspe-am) receberam cargos baseados na lei — Coordenador Estadual de Defesa Civil (Art. 14) e Presidente do CSPE/Comandante Geral (Art. 15). wCarg 17→19/19.
- **2026-06-09** — **RR refinado** (score 82 → **96.1**, 🟢 T4): adicionados cargos (Diretor/Chefe/Presidente)
  a 12 órgãos sem cargos — CAM (Art. 22 verbatim), CCult (Art. 23 verbatim), CEPDEC +
  Diretor Executivo (Art. 24 verbatim), DINT (Art. 25-A verbatim), DPL, DIE, DEIP, DLOG,
  DPST, DACRP (Arts. 29–34), DGOF (Art. 35), DCI (Art. 35-A). wCarg 15→27/31, totAtrib 63→76,
  avgLen 82→110. Exec/categ stubs (exec-op/prev/estr/log) mantidos sem cargo (sem responsável
  individual na lei). Fonte: LC nº 52/2001 + LC nº 257/2017.
- **2026-06-09** — **AP refinado** (score 57 → **81.9**, 🟡 T3): adicionados cargos a 10 órgãos
  via `detail_cargos_g1.py` — Gabinete-CG (Chefe de Gabinete), CDO (Presidente), CmdOp,
  FRCB (Gestor), ACI, AJ, AT (Assessores), Centros+Academia (Dir/Cmt), GBMs (Cmt de
  Grupamento), Escola Militar (Diretor). Todos com verbatim Art. 6º, §§1º–6º da LC nº
  180/2026. Corregedoria-Geral: texto de atribuição aprimorado para verbatim §5º. wCarg
  4→14/14. Source-cap permanece: Art. 14 delega quantidades/divisões a decreto do Governador.
  avgLen 133→176.
- **2026-06-09** — **SP refinado** (score 65 → **90.1**, 🟢 T4): adicionados cargos a 8 órgãos
  sem cobertura — B/6 (Chefe c/ 5 atrib. verbatim Arts. 40 §2° 7,a-e), Secretaria (Secretário
  Art. 40 §3°), Seção de Comando (Chefe Arts. 40 §4° 1-2), CC/CB (Cmt Art. 40 V), CIAd (Cmt
  Art. 43 I), CSM/MOp (Cmt 2 atrib. Art. 43 II + pú), CBM (Cmt Metropolitano Decreto
  65.096/2020 Art. 25 I), CBI (Cmt Interior Decreto 65.096/2020 Art. 25 II). Adicionada
  atribuição ao Estado Maior (Art. 40 II+§2° — áreas B/1–B/6). wCarg 5→13/13, totAtrib
  26→41, avgLen 108→128. Fontes: Lei nº 616/1974 (red. 663/1975) + Decreto 65.096/2020.
- **Follow-up menor**: parser de leis em `build_states_data.py` duplica "616" e trunca o ano
  em `legal_basis`/`documents` do SP (regex pré-existente). Cosmético; corrigir sem afetar
  os demais estados.

## Ranking (pior → melhor)

| Score | UF | Nós | Órgãos | c/ Cargos | Atrib. | avgLen | Tier |
|------:|----|----:|-------:|----------:|-------:|-------:|------|
| 90 | SP | 54 | 13 | 13 | 41 | 128 | 🟢 T4 | ✅ curado 2026-06-07 + refinado 2026-06-09 (era 33; Lei 616/1974 + Dec. 65.096/2020) |
| 82 | AP | 37 | 14 | 14 | 35 | 176 | 🟡 T3 | ✅ curado 2026-06-07 + refinado 2026-06-09 (era 48; LC 180/2026; source-cap Art. 14) |
| 100 | RN | 85 | 28 | 28 | 175 | 155 | 🟢 T4 | ✅ verbatim Decreto 31.139/2021 2026-06-09 (era 48; decreto baixado via DO/RN) |
| 93 | MG | 54 | 14 | 14 | 47 | 97 | 🟢 T4 | ✅ curado 2026-06-07 + refinado 2026-06-09 (CEB/BOA/BEMAD via Res. 898/2020) |
| 96 | RR | 233 | 31 | 27 | 76 | 110 | 🟢 T4 | ✅ curado 2026-06-07 + refinado 2026-06-09 (era 70; +12 cargos Dirs/Comissões via LC 52/2001) |
| 98 | AC | 57 | 17 | 17 | 57 | 167 | 🟢 T4 | ✅ verbatim Lei 2.009/2008 att 4.428/2024 (fetch legis.ac.gov.br) 2026-06-09 (era 72) |
| 90 | CE | 44 | 18 | 18 | 49 | 119 | 🟢 T4 | ✅ verbatim LOB 13.438/2004 (fetch) 2026-06-07 (era 76) |
| 100 | PE | 85 | 23 | 23 | 270 | 141 | 🟢 T4 | ✅ verbatim LOB 15.187/2013 (fetch) 2026-06-07 (era 77) |
| 90 | PI | 200 | 29 | 29 | 36 | 248 | 🟢 T4 | ✅ verbatim LOB 5.949/2009 + 7.772/2022 2026-06-08 (era 77) |
| 93 | RS | 104 | 10 | 10 | 44 | 124 | 🟢 T4 | ✅ verbatim (RI Arts. 27–55) 2026-06-07 (era 78) |
| 93 | MA | 93 | 26 | 25 | 47 | 240 | 🟢 T4 | ✅ verbatim LOB 10.230/2015 2026-06-09 (era 80) |
| 97 | GO | 129 | 15 | 14 | 82 | 87 | 🟢 T4 | ✅ verbatim LOB 18.305/2013 (fetch) 2026-06-07 (era 82) |
| 95 | RJ | 89 | 25 | 25 | 47 | 187 | 🟢 T4 | ✅ verbatim LOB 250/1979 2026-06-09 (era 83) |
| 96 | SE | 132 | 26 | 26 | 50 | 169 | 🟢 T4 | ✅ verbatim LOB 8.979/2022 (fetch) 2026-06-07 (era 84) |
| 99 | BA | 60 | 29 | 28 | 61 | 208 | 🟢 T4 | ✅ verbatim LOB 14.572/2023 2026-06-09 (era 85) |
| 99 | SC | 93 | 23 | 22 | 241 | 127 | 🟢 T4 | ✅ verbatim Dec. 1.328/2021 2026-06-09 (era 75.8) |
| 96 | TO | 55 | 26 | 26 | 54 | 160 | 🟢 T4 | ✅ verbatim LC 131/2021 2026-06-09 (era 87) |
| 100 | PB | 149 | 21 | 21 | 119 | 153 | 🟢 T4 | ✅ verbatim LC 191/2024 2026-06-09 (era 88) |
| 94 | AL | 112 | 14 | 14 | 111 | 68 | 🟢 T4 | ✅ verbatim RI Dec. 408/2001 2026-06-09 (era 89) |
| 92 | AM | 111 | 19 | 19 | 87 | 61 | 🟢 T4 | ✅ verbatim Lei 2.538/1999 2026-06-09 (era 89) |
| 91 | ES | 65 | 13 | 11 | 75 | 73 | 🟢 T4 |
| 91 | MS | 74 | 14 | 14 | 62 | 56 | 🟢 T4 |
| 91 | PR | 54 | 19 | 18 | 120 | 69 | 🟢 T4 |
| 94 | DF | 136 | 11 | 10 | 84 | 78 | 🟢 T4 |
| 96 | PA | 98 | 12 | 12 | 83 | 74 | 🟢 T4 |
| 97 | MT | 161 | 11 | 11 | 95 | 78 | 🟢 T4 |
| 100 | RO | 194 | 25 | 25 | 118 | 137 | 🟢 T4 (ref.) |

## Itens de ação

### 🔴 Tier 1 — Crítico (refazer árvore + cargos)
- **SP** — ✅ CURADO 2026-06-07. Fonte correta identificada: Lei nº 616/1974 (CBMSP, Seção II,
  Arts. 38–43), baixada e salva em `database/markdown/`. Detalhamento 3→13 órgãos, árvore
  7→54 nós, todos com detailId. Mantidos CBM/CBI do Decreto 65.096/2020. Score 33→65.
- **AP** — ✅ CURADO 2026-06-07. Atribuições verbatim por categoria (LC 180/2026, Art. 6º),
  +Comando Operacional, Escola Militar → órgão vinculado, cargos CG/SCG enriquecidos. Score 48→57.
- **RN** — ✅ FIEL À FONTE 2026-06-07. A LC 230/2002 delega a estrutura a decreto (indisponível);
  feito o máximo fiel: Conselho Superior 9 incisos verbatim, categorias corrigidas (Direção
  Superior/Assessoramento/Execução), Comandante-Geral (Art. 3º). Score travado em 48 pela fonte —
  reavaliar se/quando o decreto regulamentador for localizado.

### 🟠 Tier 2 — Fraco
- **RR** — ✅ INVESTIGADO (2026-06-07): NÃO era bug. Cargos do RR ficam inline em
  `detail_data_g5.py` (não em `detail_cargos_g5.py`); a fonte só preenchera 6/31. Os
  demais órgãos já tinham subordinação/atribuições/desdobramentos — faltava só o cargo
  titular. CURADO (conservador): adicionados 9 cargos "Comandante" aos Centros onde a
  LC 52/2001 diz literalmente "dirigido por um comandante" (CEIB, CSM, CEMAN, CINFOR,
  CIPI, CESAU, CEST, CECER, CVAP) → agora **15/31**. Centro Cultural ficou de fora
  (lei diz "encarregado", não "dirigido"). PENDENTE no RR: 9 Diretorias (lei não nomeia
  "Diretor" explicitamente — decisão de não inferir), cam-rr/cepdec-rr e os 4 exec-* (categorias).
- **AC** — ✅ INVESTIGADO 2026-06-07. Falso alarme: NÃO é verbatim (CLAUDE.md lista só
  AL/AM/DF/ES/MT/PA/PR); `ac.json` é escrito à mão e já tem árvore COMPLETA e fiel (44 nós:
  Direção Geral/Setorial/Executiva, diretorias/assessorias ligadas, Comandos Capital/Interior
  + Batalhões BEPCIF/BBS/CIACIAER). avgLen baixo é source-cap: a Lei 3.105/2015 é curta e
  estrutural (1 "compete", 1 "atribuições") — não enumera atribuições por cargo. Nada a
  transcrever sem inventar. Mantido como está.
- **MG** — ✅ CURADO 2026-06-07. LC 54/1999 é curta/estrutural: principais enumeráveis são CAT
  (Art. 24, 3 incisos) e Ajudância-Geral (Art. 25, 3 incisos) + Estado-Maior Art. 14 (2 itens).
  Todos 11 órgãos agora têm cargos, texto verbatim, requisitos corretos. Score 70→76, source-capped.
- **CE** — ✅ CURADO 2026-06-07 (score 76→90). Lei 13.438/2004 com enumeráveis ricos; 18 órgãos verbatim.
- **PE** — ✅ CURADO 2026-06-07 (score 77→100). Lei 15.187/2013 com Arts. 93/95/96/97 enumeráveis por categoria; 23 órgãos verbatim.
- **PI** — ✅ CURADO 2026-06-08 (score 77→90). Lei 5.949/2009 + 7.772/2022: 29 órgãos verbatim. Lei é majoritariamente estrutural/prosa; único enumerável é o Alto Comando §2° I–VIII. Todos os órgãos têm cargos e requisitos de posto.
- **MA** — ✅ CURADO 2026-06-09 (score 80→**93**, 🟢 T4). Lei 10.230/2015: 26 órgãos verbatim (11 originais reescritos + 15 novos). Art. 2 I–X (competência institucional) no CG; Art. 9 I–III no Alto-Comando; caput+§§ do Art. 13 nas 7 Diretorias; Arts. 14–17/22–29 nos demais. Árvore expandida: +BBMar/BBEM/BBS/BBA (filhos de COECB/bbe-ma), +CoordMédica/CoordOdonto. Todos 25/26 com cargos (Alto-Comando é colegiado). Nota: PDF com encoding quebrado — texto reconstruído com acentuação correta a partir do contexto legível.
- **RS** — 🎯 ALVO REAL de verbatim: tem Regimento Interno (Portaria CBMRS 001/2025, ~3.197
  linhas) com atribuições enumeráveis por cargo, ainda não transcrito.

### 🟡 Tier 3 — Bom (enriquecer atribuições)
- **GO, SE, RS** têm Regimento volumoso (5.777 / 2.378 / 3.197 linhas) — candidatos a
  transcrição verbatim das atribuições por cargo (alinha com AL/AM/DF/ES/MT/PA/PR já feitos).

### Notas de qualidade
- Zero corrupção de encoding nos 27 estados (verificado por code point).
- `stats.curated=true` em todos ≠ curadoria profunda; usar este ranking como guia real.
