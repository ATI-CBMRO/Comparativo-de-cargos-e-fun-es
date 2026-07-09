# De-para RI — Rio Grande do Sul × os 27 ÓRGÃOS da minuta do RO (Bloco D, Tarefa 2)

> Fable, 2026-07-08. Fonte: **Regimento Interno do CBMRS, Anexo Único da Portaria
> CBMRS nº 001, de 03/01/2025** — 96 artigos, vigente e recente.
> Rótulo: `cf. CBMRS, RI (Portaria nº 001/2025), Art. NN`.
> Arquivo: `database/markdown/Rio Grande do Sul - Regimento Interno.md`.
>
> ⚠️ **Taxonomia diferente do `de-para-rs.md`**: aquele mapeia os 15 TEMAS do
> Regulamento; este mapeia os **27 órgãos** (`organKey` de `minuta_structure.json`)
> para o comparador do RI. O `de-para-rs.md` continua valendo para o Regulamento —
> este documento cumpre a nota que ficou pendente lá ("Cap. IV … dividir por órgão
> na transcrição").
> Régua: **● exata · ◐ parcial · ○ temática · — ausente** (mesma do panorama).

## Como o RS se organiza (chave para o fatiamento)

O CBMRS não tem diretorias setoriais autônomas como o RO. A estrutura é:
**Nível Institucional** (Cmt-G, SCmt-G, CSup, Corregedoria, GCG com 5 assessorias +
ACI, CAM — Arts. 3º, 7º–9º, 27–32, 46–48) → **Nível Departamental de Apoio** (4
órgãos-mãe: DA, DSPCI, ABM, AODC — Arts. 4º, 10–13, 33–37, 49–52) → **Apoio e
Execução** (4 CRBM + BESCI — Arts. 5º, 14, 16, 38–39, 54–55) → **Execução** (BBM,
BBS, CEBM, Cia/Pel/GBM — Arts. 6º, 15, 42–44, 57).

Consequência prática: **um órgão do RO quase sempre corresponde a uma DIVISÃO de um
órgão-mãe do RS** (ex.: DP/RO ↔ DRH do DA). Cada divisão tem 3 dispositivos
paralelos: estrutura (Arts. 7–16), competência do órgão (Arts. 30–39, por inciso)
e atribuição do dirigente (Arts. 46–57, por parágrafo) — transcrever os três juntos.

## DE-PARA: organKey → artigos do RS

| organKey | Órgão RO | Artigos RS (estrutura · competência · função) | Nível | Observações |
|---|---|---|---|---|
| `cg` | Comando Geral | 2º–3º (nível institucional) · **27 (Cmt-G) · 28 (SCmt-G)** · 17 §1º, 24 (planejamento e controle estratégicos) | ◐ | O RS não tem Estado-Maior: as competências do CG/RO ficam diluídas entre Cmt-G/SCmt-G e as assessorias do GCG (APERI faz o planejamento estratégico, Art. 31, VI). Arts. 27–28 são curtos, mas verbatim aproveitáveis. |
| `gab-cg` | Gabinete do Comandante-Geral | 8º (estrutura) · **31, caput e I (SecExec)** · 47, caput e §1º (Chefe de Gabinete) · 53 (Secretários-Executivos) | ● | Órgão homônimo e de mesma finalidade (assistência, assessoramento, transmissão e fiscalização das ordens do Cmt-G/SCmt-G). Os incisos II–VI do Art. 31 pertencem às Assessorias — fatiar (ver `assessorias`, `ccs`, `cint`). |
| `assessorias` | Assessorias | 8º, II–IV e VI (estrutura) · **31, II (Controle Interno), III (Jurídica/Convênios), VI (APERI)** · 37 §1º (conceito de Assessorias) · 47 §§2º–3º e 6º (chefes) | ◐ | Conteúdo aderente à finalidade do RO (estudos, pareceres, assessoramento técnico), mas no RS são frações do GCG, não órgãos autônomos. Fonte ● complementar: PA, RI, Art. 69 (ver `bloco-d-classificacao-al-df-pr-pa.md`). |
| `condeg` | Conselho Deliberativo de Estratégia e Gestão | **29 (Conselho Superior)** · apoio: 9º/32/48 (CAM) · 94 (Câmaras Técnicas) | ● | Art. 29 é curto porém exato: colegiado de assessoramento direto ao Cmt-G para "assuntos relevantes… subsídios para a tomada de decisão". CAM (○) e Câmaras Técnicas (○) são colegiados vizinhos — citar só como inspiração. |
| `corregedoria` | Corregedoria-Geral | 7º (estrutura: DJD, DCIC, DFE, **Ouvidoria**, Cartório) · **30 (competências, 6 incisos)** · 46 (Corregedor-Geral + chefias) · 62 (publicação disciplinar) | ● | Fonte rica e recente; diferencial: Ouvidoria e Cartório dentro da Corregedoria (o RO não prevê — candidato a contribuição da minuta). Incisos do Art. 30 têm preâmbulo repetitivo ("planejar, dirigir…") — podar na transcrição. |
| `cint` | Coordenadoria de Inteligência | 8º, V (ACI) · **31, V (competência ACI)** · 31 §2º · 47 §5º (Chefe ACI) · 38, VI (ARI regional) · 54 §2º (Chefe ARI) · 15 §1º, I (ALI nas unidades) | ● | Sistema de inteligência em 3 camadas (Central/Regional/Local) — modelo interessante para o RO, que só prevê a CINT central. Transcrever Art. 31, V como núcleo. |
| `ccs` | Coordenadoria de Comunicação Social | 8º, IV (ACS) · **31, IV (competência ACS)** · 47 §4º (Chefe ACS) · 38, V (DCS regional) · 54 §5º | ● | Matéria completa (imprensa, cerimonial militar, marketing, comunicação interna, prevenção primária); posição orgânica distinta (assessoria do GCG, não coordenadoria autônoma) — nota na transcrição. |
| `cinf` | Coordenadoria de Informática | 10, V (DTIC) · **34, V (competência DTIC)** · 49 §6º (Chefe DTIC) | ● | Fatiar do Departamento Administrativo. Bônus: a DTIC do RS inclui Seção de COMUNICAÇÕES — cobre a lacuna "comunicação" que a LOB do RO põe na DLOG (decidir na curadoria fina onde citar). |
| `dp` | Diretoria de Pessoal | 10, IV (DRH) · **34, IV (competência DRH)** · 49 §4º (Diretor de RH, rico) | ● | Fatiar do DA. Cobre inclusão, inativação, afastamentos, recrutamento/seleção, identificação, mobilização, assistência social. |
| `dpof` | Diretoria de Planejamento, Orçamento e Finanças | 10, III (DOF) · **34, III (competência DOF)** · 49 §3º (Diretor de Orçamento e Finanças) | ● | Fatiar do DA (controle/distribuição de recursos, vencimentos, execução orçamentária, prestação de contas). Vertente "planejamento institucional" do RO está na APERI (31, VI) — ◐, citar como complemento. |
| `dlog` | Diretoria de Logística | 10, II (DLP) · **34, II (competência DLP)** · 49 §2º (Diretor de Logística e Patrimônio) · 61 (publicações de logística) · 38, IV (DLPF regional) | ● | Fatiar do DA: materiais, patrimônio, frota/motomecanização, material bélico, compras/catalogação, conservação e obras. |
| `dsap` | Diretoria de Saúde e Assistência ao Pessoal | 92 (assistência médico-hospitalar) · 34, IV in fine (apoio ao Dpto. de Saúde da **Brigada Militar** e caráter assistencial; SAS/DRH) | ○ | **Ausência estrutural**: o CBMRS usa o sistema de saúde da Brigada Militar/IPE — não há diretoria de saúde própria no RI. Registrar ausência; fonte ● já existente: DF, RI, Art. 154. |
| `deei` | Diretoria de Educação, Ensino e Instrução | 12 (estrutura ABM: DEns, OPETA, escolas EsEF/ESSCID/EsBo/ESCAB) · **36 (competências ABM)** · 45 (órgãos de ensino e CTs) · 51 (Cmt da ABM + chefes) | ● | Fonte primária e extensa: política de ensino, currículos, EAD, avaliação, banco de instrutores, corpo de alunos. Casa também com o tema 13 do Regulamento. |
| `dpo` | Diretoria de Planejamento Operacional | 13 (estrutura AODC) · **37, caput, II e IV (DODC + DMO)** · 52, caput e §§2º/4º (Diretor AODC e chefes) · 17 §§3º–5º (planejamento operacional) | ◐ | A AODC mescla operações + defesa civil + serviços civis + operações aéreas. Para a DPO/RO, transcrever o núcleo de operações (DODC) e monitoramento/estatística (DMO — que opera com CCOB/COBOM, cf. 38, II). Fatiar os demais incisos para `depdec` e `boa`. |
| `doe` | Diretoria Operacional Especializada | 44 (Órgãos Especiais — competências) · 14 §5º (BBS como Órgão Especial) | ○ | O RS não tem diretoria especializada: as especialidades vivem no próprio BBS/CEBM. Art. 44 descreve EXECUÇÃO, não direção — só inspiração. Fonte ● encontrada: DF, RI, Arts. 488–489 (COESP). |
| `depdec` | Diretoria Estadual de Proteção e Defesa Civil | **37, caput e II (AODC/DODC — defesa civil)** · 52, caput (interlocução em ações de defesa civil) · 1º, IV (competência institucional) | ◐ | No RS a coordenação do SISTEMA estadual de PDC não é do CBMRS (fica fora do RI); o que há é a participação operacional em defesa civil. Fonte ● segue sendo AL, RI, Art. 13. |
| `cot` | Comando de Operações Técnicas | 11 (estrutura DSPCI: DGN, DPIS) · **35 (competências DSPCI)** · 50 (Diretor DSPCI + diretores de Gestão/Normatização e de Pesquisa/Investigação) · 42 (execução SCIP) | ● | Espelho do COT/RO: normatização, doutrina, licenciamento/fiscalização em nível estadual, investigação de sinistros. (O Art. 86 — Regulamento de Uniformes — NÃO entra aqui.) |
| `cat` | Coordenadoria de Atividades Técnicas | 16 (estrutura BESCI: análise de PPCI + vistoria/fiscalização) · **39 (competências BESCI)** · 55 (Cmt BESCI) · 42 §1º (DSCI/SSeg/SSCI — capilaridade) | ● | **Melhor fonte do acervo para o CAT**: órgão de execução técnica estadual subordinado ao DSPCI, com análise de planos, vistoria e fiscalização — estrutura-espelho do CAT/COT do RO. |
| `crbm` | Comandos Regionais de Bombeiro Militar | 5º (os 4 CRBM) · **14 (estrutura: DAdmC, ARI, DODC, DLPF, DCS, DSCI)** · **38 (competências das 6 divisões)** · 54 (Comandante Regional + chefes de divisão) · 66 (Boletim Interno) · 43 §1º | ● | **Fonte primária do capítulo** — era a lacuna nº 1 do briefing. O modelo de CRBM "espelho em miniatura" do nível central (com divisões de correição, inteligência, operações, logística, comunicação e SCIP) é o contraste mais útil para o RO. |
| `bbm` | Batalhão de Bombeiros Militar | 15, I e §§1º–3º (estrutura BBM: Cia/Pel/GBM + ALI, SAdmC, SODC, SSeg, CTs) · **43 §2º e incisos I/III/IV (competências)** · 57, caput e §§1º/3º (Cmt BBM, Cmt Cia, Cmt Pel) · 59 (RI próprio até Batalhão) | ● | Cadeia completa Batalhão→Companhia→Pelotão→Grupo com competências por fração — casa com a estrutura da LOB do RO. |
| `cibm` | Companhia Independente de Bombeiros Militar | 15, III e §2º (**CEBM** — Companhia Especial, comandada por Oficial Superior) · 43, II (competências CEBM) · 57 §2º (Cmt CEBM) | ◐ | O análogo mais próximo é a Companhia ESPECIAL (autônoma, Oficial Superior), mas a CEBM do RS é vocacionada a especialidade, não a circunscrição própria como a CIBM/RO. Fonte ● segue sendo PR, Lei 22.206/2024, Art. 35, II. |
| `bbs` | Batalhão de Busca e Salvamento | 15, II (estrutura CiaBS/PelBS/GBS) · 14 §§1º/5º (abrangência estadual; Órgão Especial) · **44 §1º e incisos (competências + rol de especialidades: mergulho, salvamento aquático/altura, estruturas colapsadas, cães, áreas deslizadas, produtos perigosos, APH)** · 57 (Cmt BBS) | ● | Órgão homônimo e de mesmo desenho (batalhão especializado estadual). O rol de especialidades do Art. 44 §1º é o melhor texto do acervo RI para o BBS/RO. |
| `bifea` | Batalhão de Incêndio Florestal e Emergências Ambientais | 44 §1º (produtos perigosos como especialidade do BBS) · 44 §2º (especialidades por convênio) | — /○ | **Ausente**: zero ocorrências de "florestal" no RI do RS; emergências ambientais aparecem só como especialidade difusa do BBS. Fonte ● encontrada: DF, RI, Art. 530 (GPRAM). |
| `boa` | Batalhão de Operações Aéreas | 13, V (DOA/AODC: Comando Aéreo + Seções de Operações/Manutenção/Segurança Operacional) · **37, V (competência DOA — regras ANAC)** · 52 §5º (Chefe DOA) | ◐ | Matéria equivalente, mas no RS operações aéreas são DIVISÃO da AODC, não batalhão. Fonte ● segue sendo PR, Lei 22.206/2024, Art. 35, IV. |
| `gbm` | Grupo de Bombeiros Militar | 15, I.3 e §4º (**GBM: fração mínima, ≥10 BM, comandada por Sargento**) · 43 §2º, IV (competências) · 57 §4º (Cmt de GBM) · 72 (municípios atendidos por Civis Auxiliares conveniados) | ◐ | Mesmo nome, natureza diferente: no RS o GBM é fração orgânica do Pelotão; no RO é unidade conveniada com prefeituras. O Art. 72 (convênio com municípios) é o análogo temático de interiorização — transcrever com selo ○. |
| `guarnicao` | Guarnição de Serviço Operacional | 70–71 (escalas de serviços internos/externos; função "Comandante de Guarnição de Serviço") · 85 (sobreaviso/prontidão) · 94 (efetivo mínimo das guarnições, via Câmaras Técnicas) | ○ | O RS delega a matéria aos RIs dos órgãos (Arts. 58–59, 70–71). Não define competências da guarnição — lacuna esperada; fonte permanece o RISD de SE (fora do conjunto RI). |
| `ag` | Ajudância-Geral | 31, I (SecExec do GCG) · 53 (Secretários-Executivos) · 60 (Boletim Geral) | ○ | O RS não tem Ajudância-Geral/QCG como órgão: as funções de secretaria/publicação ficam no GCG e nos Secretários-Executivos. Fontes ● seguem sendo DF Art. 110 e PA Art. 119. |

## Dispositivos transversais úteis ao comparador (não são de um órgão só)

| Artigos | Matéria | Uso sugerido |
|---|---|---|
| 40 | Prazo máximo de 6 anos nas funções de direção/chefia/comando | Contribuição de governança sem paralelo no RO — mostrar como "dispositivo extra" |
| 41 · 56 | Seções e Setores (desdobramentos) + chefes | Análogo genérico das seções internas dos órgãos do RO |
| 58–59 | Cada órgão (até Batalhão) elabora o próprio RI | Mecanismo-chave; já apontado no `de-para-rs.md` (análogo ao MT 265) |
| 60–69 | Sistema de Boletins (Geral, Interno, Reservado, de Avaliação) | Citar no capítulo do CG/AG conforme decisão de estrutura |
| 82–84 | Sistema normativo e correspondência | Disposições gerais |
| 87–88, 90–91, 95–96 | Implantação gradual, organograma descritivo, siglas, quadros, revisão | Disposições finais |

## Ausências do RS (registro para o comparador)

- **Saúde própria** (`dsap`) — usa a Brigada Militar/IPE (Art. 92).
- **Unidade florestal/ambiental** (`bifea`) — inexistente.
- **Diretoria especializada** (`doe`) — especialidades vivem no BBS.
- **Ajudância-Geral** (`ag`) — funções absorvidas pelo GCG.
- **Guarnição como fração normatizada** (`guarnicao`) — delegada aos RIs dos órgãos.

**Escopo sugerido de transcrição para o comparador**: Arts. 27–57 integrais (fatiados
por órgão conforme a tabela), + 5º/14/16 (estruturas de CRBM/BESCI), + 58–59 e 70–72
(selo ◐/○ conforme tabela). Os Arts. 73–81 (cerimonial) já estão endereçados no
Regulamento via `de-para-rs.md` — não duplicar aqui.
