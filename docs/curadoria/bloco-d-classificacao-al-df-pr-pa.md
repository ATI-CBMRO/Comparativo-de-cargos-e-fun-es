# Bloco D — classificação dos trechos já extraídos (AL/DF/PR/PA) por órgão do RO

> Fable, 2026-07-08. **Tarefas 1 e 3 do pacote** `bloco-d-pacote-trabalho-fable.md`.
> Material-fonte: os trechos verbatim já extraídos em `scripts/minuta_enrichment.py`
> (`ENRICHMENT_ORGAN` e `ENRICHMENT`), julgados contra a finalidade de cada órgão da
> minuta (`database/minuta_structure.json`). Régua idêntica à do Regulamento
> (`panorama-cobertura.md`): **● exata** (mesmo assunto e alcance) · **◐ parcial**
> (parte do tema/alcance diferente) · **○ temática** (assunto vizinho, inspiração) ·
> **— ausente**.
>
> Este documento alimenta o futuro campo `alternatives` de `minuta_structure.json`
> (tela de comparação lado a lado da minuta do RI). Código NÃO foi alterado.

## Nota de método (leia antes de usar)

1. O nível é atribuído **por fonte citada** (trecho × órgão do RO), não pelo órgão
   como um todo. Um órgão pode ter uma fonte ● e outra ◐.
2. Só entram aqui as fontes dos **4 estados RI-válidos já extraídos** (AL, DF, PR,
   PA). As fontes de MT/SC/BA/PE/CE/SP/ES/GO que convivem no mesmo dict ficam FORA
   do comparador de RI (continuam válidas na minuta como enriquecimento, mas não são
   "Regimento Interno" — ver correção MT/SE de 2026-07-08).
3. **Natureza da fonte**: nem tudo dos 4 estados é RI em sentido estrito — PR usa a
   Lei nº 22.206/2024 (LOB) e a Portaria nº 227/2023; PA usa também a Lei nº
   11.060/2025. O nível de correspondência não muda por isso, mas a UI deve exibir o
   rótulo fiel (já está correto nos `source`).
4. O RI do PA é **minuta de Decreto em tramitação (2026)** — citar como tal (regra
   já registrada no `panorama-cobertura.md`).

## Tarefa 1 — os 20 órgãos já cobertos por AL/DF/PR/PA

| Órgão RO | Fonte (trecho já em `ENRICHMENT_ORGAN`) | Nível | Justificativa |
|---|---|---|---|
| **dpo** | CBMPA, Lei nº 11.060/2025, Art. 16 (Comando de Operações) | ◐ | O COP paraense é comando operacional pleno (direção e controle da execução); a DPO/RO é diretoria de planejamento e supervisão. Os 2 incisos são genéricos e aproveitáveis, mas o alcance do órgão difere. |
| **dpo** | CBMDF, RI (Portaria nº 24/2020), Art. 454 (COMOP) | ◐ | O núcleo (planejamento estratégico setorial, coordenação do emprego, doutrina) casa com a DPO; mas o COMOP também EXECUTA (movimenta pessoal, executa atividades operacionais) — alcance maior. Usar os incisos de planejamento/coordenação. |
| **cot** | CBMDF, RI (Portaria nº 24/2020), Art. 54 (DESEG) | ● | SCIP completo: normatização, análise de projetos, vistoria, fiscalização, perícia, credenciamento, hidrantes — espelho da finalidade do COT/RO. |
| **bbm** | CBMPR, Lei nº 22.206/2024, Art. 35, I | ● | Missões do Batalhão idênticas às do BBM/RO (poder de polícia SCIP, combate a incêndio, busca/salvamento/APH, defesa civil). |
| **cibm** | CBMPR, Lei nº 22.206/2024, Art. 35, II | ● | Mesma definição do RO: atribuições do Batalhão em circunscrição de menores dimensões. |
| **bbs** | CBMPR, Lei nº 22.206/2024, Art. 35, III (GOST) | ◐ | Socorro tático/busca e salvamento casam, mas o GOST inclui emergências ambientais (no RO é matéria do BIFEA) e forças-tarefa; natureza de "grupo tático", não batalhão. |
| **boa** | CBMPR, Lei nº 22.206/2024, Art. 35, IV (UOA) | ● | Missões aéreas idênticas (busca/resgate urbano-rural, matas/águas, defesa civil, apoio a órgãos). |
| **cg** | CBMPA, RI, Art. 6 (Comando-Geral) | ◐ | O PA define o "Comando-Geral" como órgão de ASSESSORAMENTO ao Comandante-Geral (3 incisos); o CG/RO é o órgão máximo executivo. Matéria vizinha da administração superior. |
| **cg** | CBMDF, RI (Portaria nº 24/2020), Art. 58 (EMG) | ◐ | Competências de estado-maior (planejamento estratégico, diretrizes, orçamento) — matéria da administração superior do CG/RO, mas órgão distinto e com incisos amarrados a estruturas do DF (PARF, DEALF, Alto Comando). Podar na adaptação. |
| **depdec** | CBMAL, RI, Art. 13 (CEDEC) | ● | Órgão central estadual de defesa civil: coordenação do sistema estadual, planos, mobilização, homologação de SE/ECP — o papel do DEPDEC no SIEPDEC. Nota: terminologia pré-PNPDEC/2012 ("defesa civil", SINDEC) — atualizar nomenclatura na adaptação, conteúdo aderente. |
| **condeg** | CBMAL, RI, Art. 11 (Conselho de Políticas Estratégicas) | ◐ | Parte dos incisos é de estudo/parecer/assessoramento (casa com o CONDEG consultivo); mas o artigo mistura competências executivas (administrar pessoal, dirigir trabalhos) que extrapolam órgão deliberativo-consultivo. Filtrar incisos. |
| **dp** | CBMDF, RI (Portaria nº 24/2020), Art. 127 (DIGEP) | ● | Gestão de pessoal completa: movimentação, inatividade, folha, promoções, cadastro, ingresso — espelho da DP/RO. |
| **dp** | CBMPR, Lei nº 22.206/2024, Art. 28 (Diretoria de Pessoal) | ● | Mesmo órgão e alcance, redação sintética (classificação, movimentação, inativos, folha, saúde ocupacional como assessoria). |
| **deei** | CBMDF, RI (Portaria nº 24/2020), Art. 227 (DIREN) | ● | Formação, aperfeiçoamento, cursos, certificação, doutrina, avaliação de ensino — espelho da DEEI/RO. |
| **dpof** | CBMDF, RI (Portaria nº 24/2020), Art. 187 (DIOFI) | ◐ | Execução orçamentária, financeira e contábil — núcleo casa; NÃO cobre a vertente "planejamento" da DPOF (no DF isso é do EMG, cf. Art. 58). |
| **dpof** | CBMPA, RI, Art. 170 (Diretoria de Finanças) | ● | Orçamento + finanças + contábil + fiscal + assessoria de planejamento (LOA/PPA) — é o espelho mais completo da DPOF/RO. |
| **dpof** | CBMAL, RI, Art. 52 (Diretoria de Finanças) | ◐ | Finanças, tesouraria, contabilidade e auditoria; orçamento aparece só como apoio — alcance menor que a DPOF. |
| **dsap** | CBMDF, RI (Portaria nº 24/2020), Art. 154 (DISAU) | ● | Saúde + assistência (médico-hospitalar, odontológica, psicossocial, perícias, fundo de saúde) — cobre as duas pernas da DSAP/RO. |
| **dlog** | CBMPR, Lei nº 22.206/2024, Art. 29 (DALF) | ◐ | O órgão do PR acumula logística E finanças (sobreposição com a DPOF/RO). Usar apenas os incisos de logística/suprimento/patrimônio. |
| **dlog** | CBMDF, RI (Portaria nº 24/2020), Art. 218 (DIMAT) | ● | Gestão de bens, contratações, manutenção, intendência, patrimônio, frota. Nota: não cobre "comunicação" (que a LOB do RO põe na DLOG) — complementar com RS (a DTIC de lá tem Seção de Comunicações). |
| **dlog** | CBMPA, RI, Art. 163 (DAL) | ● | Sistema logístico completo: suprimento, estoque, frota, obras/infraestrutura, patrimônio, sustentabilidade — espelho da DLOG/RO. |
| **cint** | CBMDF, RI (Portaria nº 24/2020), Art. 304 (CEINT) | ● | Inteligência e contrainteligência completas (produção/difusão, investigação social, sigilo, doutrina). |
| **cint** | CBMPA, RI, Art. 140 (CEINT) | ● | Sintético (3 incisos), mas mesmo assunto e alcance: planejar/coordenar/executar inteligência + SISBIN. |
| **cint** | CBMAL, RI, Art. 25 (AICI) | ● | Conteúdo aderente; vocabulário datado (doutrina de "informações/contra-informações", 2001) — atualizar termos na adaptação. |
| **ccs** | CBMDF, RI (Portaria nº 24/2020), Art. 291 (CECOM) | ● | Comunicação social completa: campanhas, solenidades, imagem, imprensa, tradições. |
| **ccs** | CBMAL, RI, Art. 26 (ARPCS) | ◐ | Mistura relações-públicas/cerimonial com incisos genéricos de assessoria pessoal ao Cmt-G ("praticar todos os atos..."); aproveitável com poda. |
| **cinf** | CBMDF, RI (Portaria nº 24/2020), Art. 241 (DITIC) | ● | TIC completa: PDTI, segurança da informação, sistemas, redes, manutenção — espelho da CINF/RO. |
| **gab-cg** | CBMDF, RI (Portaria nº 24/2020), Art. 6 | ● | Assistência/assessoramento direto ao Cmt-G, documentação, agenda — exatamente a finalidade do GAB-CG/RO. |
| **gab-cg** | CBMPA, RI, Art. 107 | ● | ⚠️ Os 6 incisos do PA são **IDÊNTICOS, palavra por palavra, aos do DF Art. 6** (a minuta paraense reproduziu o RI do DF). Na tela de comparação vão aparecer como duplicata — exibir com nota ou deduplicar na curadoria fina. |
| **ag** | CBMDF, RI (Portaria nº 24/2020), Art. 110 | ● | Protocolo-geral, correio, arquivo, Boletim Geral, administração do QCG, apoio a solenidades — espelho da AG/RO ("apoio aos órgãos instalados no QCG"). |
| **ag** | CBMPA, RI, Art. 119 | ● | Mesmo núcleo (protocolo, QCG, Boletim Geral Eletrônico, apoio logístico a eventos, segurança do QCG). |
| **corregedoria** | CBMDF, RI (Portaria nº 24/2020), Art. 96 | ● | Atividade correcional plena: sindicâncias, IPM, PAD, conselhos de justificação/disciplina, custódia. |
| **corregedoria** | CBMAL, RI, Art. 29 | ○ | O artigo alagoano trata de **assistência judiciária ao militar e à família** (orientar processados, habilitar pensão), não do poder correcional. Assunto vizinho — rever se permanece no capítulo da Corregedoria da minuta. |
| **corregedoria** | CBMPR, Portaria nº 227/2023, Art. 3º | ● | Correições, polícia judiciária militar, apuração, mandados — atividade correcional plena. Nota: fonte é portaria específica da Corregedoria, não a coletânea "RI" do PR. |

### Classificação do enriquecimento POR CARGO (`ENRICHMENT`, CBMAL)

Também alimenta o comparador (dispositivo por dispositivo), então classifiquei:

| Órgão/cargo RO | Fonte | Nível | Justificativa |
|---|---|---|---|
| crbm / Comandante | CBMAL, RI, Art. 107 (Comandante Operacional de Bombeiro) | ● | O COB alagoano é o escalão regional de AL (cf. AL Art. 105: "mais alto escalão do Sistema Operacional", com planejamento/coordenação/fiscalização das unidades subordinadas) — competências típicas de comando regional. |
| crbm / Adjunto | CBMAL, RI, Art. 115 (Subcomandante de UOp) | ◐ | Função equivalente (substituir, fiscalizar, disciplina), mas descrita no nível de UNIDADE, aplicada por analogia ao escalão regional. |
| bbm / Comandante | CBMAL, RI, Art. 114 (Comandante de Grupamento) | ● | "Grupamento" em AL ≈ Batalhão; atribuições de comandante de unidade operacional ordinária. |
| cibm · bbs · bifea · boa / Comandante | CBMAL, RI, Art. 114 | ◐ | Mesmo texto do BBM aplicado por analogia a unidades de porte (companhia independente) ou especialidade (salvamento, florestal, aéreo) distintos. |
| guarnicao / Cmt de Guarnição e Condutor | CBMSE, RISD, Arts. 14–15 | (fora do conjunto RI) | SE não é mais estado RI-válido; o material segue sendo o melhor existente para o capítulo (ver Lacunas, item 1). |

## Tarefa 3 — Lacunas: busca dirigida dos 7 órgãos nos 5 RIs (AL, DF, PR, PA, RS)

Busca por palavra-chave (florestal, ambiental, guarnição, especializad, vistoria,
"grupo de bombeiro", assessoria, regional) nos 5 markdowns + leitura pontual dos
artigos encontrados. Resultado: **5 dos 7 ganharam fonte RI-válida** (4 achados
novos + crbm resolvido pelo RS); **2 permanecem sem fonte plena** (gbm só ◐,
guarnicao só ○).

### Achados novos (candidatos a extração futura — o texto AINDA NÃO está no enrichment)

| Órgão RO | Fonte encontrada | Nível | O que é |
|---|---|---|---|
| **bifea** | CBMDF, RI (Portaria nº 24/2020), Art. 530 (GPRAM — Grupamento de Proteção Ambiental) | ● | Executa prevenção e combate a **incêndios florestais**, atendimento a emergências com produtos perigosos e proteção ao meio ambiente; doutrina e capacitação das unidades de multiemprego. Única fonte orgânica de "florestal+ambiental" nos 5 RIs. (Arts. 531 ss. detalham as seções.) |
| **cat** | CBMRS, RI (Portaria nº 001/2025), Arts. 16, 39 e 55 (BESCI) | ● | Batalhão Especial de Segurança Contra Incêndio: órgão de EXECUÇÃO estadual de análise de planos (PPCI), vistoria e fiscalização, subordinado ao departamento técnico — espelho do CAT/RO subordinado ao COT. Ver `de-para-ri-rs.md`. |
| **cat** | CBMDF, RI (Portaria nº 24/2020), Arts. 251 (DIVIS) e 263 ss. (DIEAP) | ◐ | O DF divide a execução técnica em duas diretorias (Vistorias · Estudos e Análise de Projetos); cada uma cobre metade do alcance do CAT — juntas cobrem o órgão. |
| **doe** | CBMDF, RI (Portaria nº 24/2020), Arts. 488–489 (COESP — Comando Especializado) | ● | Prepara, coordena, controla e fiscaliza as unidades ESPECIALIZADAS (GBS, GAEPH, GPRAM, GPCIV, GAVOP, GPCIU) e a doutrina operacional — o papel da DOE/RO sobre BBS/BIFEA/BOA. |
| **doe** | CBMPA, RI, Arts. 49–51 (COP) | ○ | O COP subordina os grupamentos especializados do PA (GMAF, GBS, GSE, GOA), mas é comando operacional GERAL — já classificado como fonte ◐ do dpo; para a DOE é só inspiração. |
| **assessorias** | CBMPA, RI, Art. 69 (Assessorias Técnicas) | ● | Competências das assessorias técnicas: análises especializadas, pareceres, avaliação de riscos, conformidade normativa, assistência aos órgãos — espelho da finalidade das Assessorias/RO. |
| **assessorias** | CBMRS, RI (Portaria nº 001/2025), Arts. 31, II–VI, 37 §1º e 47 §§2º–6º | ◐ | Assessorias do GCG (Controle Interno, Jurídica/Convênios, Comunicação, Inteligência, Planejamento Estratégico): conteúdo rico, mas são frações do Gabinete, não órgãos autônomos. Ver `de-para-ri-rs.md`. |

### Resolvido pela leitura do RS (Tarefa 2)

| Órgão RO | Fonte | Nível |
|---|---|---|
| **crbm** | CBMRS, RI (Portaria nº 001/2025), Arts. 14, 38 e 54 | ● — fonte primária do capítulo (estrutura com 6 divisões + competências + comandante regional). Detalhe no `de-para-ri-rs.md`. |

### Lacunas confirmadas (esperadas, não bloqueantes)

1. **guarnicao — SEM fonte plena em RI.** Nenhum dos 5 RIs define a guarnição como
   fração operacional com competências próprias. O que existe: RS Arts. 70–71
   (escalas de serviço, citam a função "Comandante de Guarnição de Serviço") e Art.
   94 (efetivo mínimo das guarnições via Câmaras Técnicas) — nível **○**; DF só
   menções incidentais ("guarnição de pronto atendimento", tempo-resposta).
   **Motivo**: é matéria de regulamento de serviço diário (RISD), não de RI de
   organização — mesmo padrão já visto com uniformes/cerimonial no Regulamento.
   A fonte já usada no capítulo (CBMSE, RISD, Arts. 14–15) permanece a melhor
   disponível; no comparador de RI o órgão fica **pendente** com esta nota.
2. **gbm — só correspondência parcial.** O RS tem "Grupo de Bombeiro Militar"
   nominal e estruturado (Arts. 15 §4º: mínimo 10 BM; 43 §2º, IV: competências; 57
   §4º: comandante) — nível **◐**, porque lá o GBM é fração orgânica de Pelotão,
   enquanto no RO é unidade criada por CONVÊNIO com prefeituras em municípios sem
   serviço regular. O RS Art. 72 (municípios conveniados com Civis Auxiliares de
   Bombeiro) é o análogo de interiorização — **○**. ⚠️ Homonímia: em AL e PA,
   "Grupamento BM (GBM)" é unidade tipo BATALHÃO — não usar essas fontes para o
   gbm/RO sem nota.
3. **bifea nos demais estados**: AL, PR e RS não têm unidade florestal/ambiental
   (zero ocorrências orgânicas); PA só menciona incêndio florestal na competência
   geral da corporação. Fica DF (Art. 530) como fonte única.

## Resumo por órgão (melhor fonte RI-válida disponível, pós Tarefas 1–3)

- **● exata (23):** ag, assessorias, bbm, bbs (RS), bifea (DF 530), boa, cat (RS
  BESCI), ccs, cibm, cinf, cint, condeg (RS Art. 29), corregedoria, cot, crbm (RS),
  deei, depdec, dlog, doe (DF COESP), dp, dpof (PA 170), dsap, gab-cg
- **◐ parcial (3):** cg, dpo, gbm
- **○ temática/pendente (1):** guarnicao
