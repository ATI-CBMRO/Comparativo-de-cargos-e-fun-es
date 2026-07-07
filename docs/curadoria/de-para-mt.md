# De-para — Mato Grosso (Lote 1, estado-esqueleto)

> **B1-M passo 2** — mapeamento tema→artigos produzido pelo Fable em 2026-07-06, a partir
> da leitura estrutural integral do documento + varredura de termos + leitura dos
> trechos-fronteira. Candidatos automáticos usados como apoio: `candidatos-mt.md`.
>
> ✅ **VALIDADO PELO WÂNDRIO (passo 3, 2026-07-06) — decisões que SUPERAM as colunas
> "Recomendação" da tabela abaixo:**
> 1. **Transcrição INTEGRAL dos 266 artigos** (não o corte prioritário de ~90). As
>    colunas "Recomendação" da tabela valem apenas como guia de PRIORIDADE/ORDEM dos
>    lotes — nada fica de fora. A poda fina será feita depois, no wizard da minuta
>    (curadoria por inciso/fonte), como já acontece na Minuta RI.
> 2. **Temas novos APROVADOS**: `ensino-instrucao` e `seguranca-contra-incendio`
>    entram na taxonomia (14 temas).
> 3. **Renomear o arquivo de MT** ("Regimento Interno" → "Regulamento Geral") em rodada
>    futura de dados — fica na fila de melhorias; transcrição já usa a citação correta.
>
> ⚠️ **FASEAMENTO SUPERADO (2026-07-06, 3ª rodada):** a pedido do Wândrio ("as demais
> legislações também devem ser levadas em consideração"), a ordem de transcrição passou
> a ser TEMA A TEMA atravessando todos os 9 estados — ver
> `docs/curadoria/panorama-cobertura.md`. A transcrição INTEGRAL de MT permanece
> validada (todo artigo tem tema); apenas a ORDEM dos lotes abaixo deixa de valer.
>
> **Instruções para a transcrição (passo 4, Sonnet/Haiku):** transcrever POR LOTES na
> ordem do documento (1: Arts. 1º–14; 2: 15–59; 3: 60–159; 4: 160–217; 5: 218–266),
> gravando cada artigo no tema indicado pela tabela abaixo, com `match` conforme o
> nível mapeado e rótulo `cf. CBMMT, Regulamento Geral (Portaria nº 009/BM-8/2013),
> Art. NN`. Rodar `python3 scripts/verificar_verbatim.py` AO FIM DE CADA LOTE — nenhum
> lote avança com dispositivo que não seja literal. Art. 5º: transcrever também
> (decisão de integralidade), mas marcado `match:'parcial'` com nota "estrutura é a de
> MT; a da minuta de RO vem da LOB de RO".

## Identificação da fonte

| Campo | Valor |
|---|---|
| Documento | **Regulamento Geral do CBMMT** |
| Ato de aprovação | Portaria nº 009/BM-8/2013, publicada no BGE nº 755, de 14/11/2013 |
| Fundamento | Arts. 7º e 8º, V e VII, da **Lei Complementar nº 404/2010** (LOB do CBMMT) |
| Arquivo no acervo | `database/markdown/Mato Grosso - Regimento Interno.md` (282 KB, 266 artigos + 3 da Portaria) |
| Rótulo de fonte a usar na transcrição | `cf. CBMMT, Regulamento Geral (Portaria nº 009/BM-8/2013), Art. NN` |

⚠️ **Nota de qualidade de dados:** o NOME do arquivo diz "Regimento Interno", mas o
CONTEÚDO é o *Regulamento Geral* (o próprio Art. 2º da Portaria revoga "todos os
Regulamentos e Regimentos" anteriores). Como `parse_doc_type` classifica pelo nome do
arquivo, MT aparece como "Regimento Interno" no portal. **Decisão sugerida ao Wândrio:**
renomear o PDF/MD para "Mato Grosso - Regulamento Geral (Portaria 009-BM-8-2013)" numa
rodada futura de dados (muda referências `md_file`/`has_pdf` — reexecutar a pipeline), ou
conviver com o rótulo. A transcrição usará o rótulo correto de qualquer forma.

## Leitura geral (o que este documento É e o que NÃO é)

O Regulamento Geral do CBMMT é essencialmente um **regulamento de organização e
competências**: detalha órgão por órgão (do Comandante-Geral ao Pelotão) a constituição
e as competências de cada estrutura e função de chefia. É o esqueleto IDEAL para os
capítulos organizacionais da minuta de RO (a LOB de RO seguiu a de MT — os 7 níveis do
Art. 4º casam com a estrutura de `organs_detail/ro.json`).

O que ele **NÃO regula** (confirmado por varredura de termos, não só pelo garimpo):
serviço operacional (escalas/guarnições/plantão — zero ocorrências normativas),
uniformes (só menções incidentais), continência/cerimonial (só como competência da
Comunicação Social). Esses temas virão de SE (RISD) e RN (Regulamento Geral) — ver
tabela de ausências no fim.

## Mapa estrutural do documento (para orientar a transcrição)

| Divisão | Artigos | Conteúdo |
|---|---|---|
| Portaria de aprovação | 1º–3º (da Portaria) | aprovação, revogação, vigência |
| TÍTULO I, Cap. I — Destinação, Subordinação e Competência | 1º–3º | natureza, subordinação, competências do CBMMT |
| TÍTULO II, Cap. I — Estrutura Organizacional Básica | 4º–5º | 7 níveis + lista completa de órgãos |
| TÍTULO III, Cap. I — Nível de Direção Geral | 6º–8º | Comandante-Geral |
| Cap. II — Nível de Decisão Colegiada | 9º–10 | Conselho Superior de Bombeiros |
| Cap. III — Nível de Direção Superior | 11–14 (Seção I) · 15–33 (Seção II) | Cmt-Geral Adjunto + Estado-Maior Geral · Corregedoria Geral |
| Cap. IV — Nível de Assessoramento Superior | 34–59 | Assessorias (35–45), Ouvidoria (46–51), Inteligência (52–58), Comissões (59) |
| Cap. V — Nível de Direção Setorial / EMG | 60–217 | DAI + 10 coordenadorias BM/1–BM/10 (60–159) · DEIP/ensino (160–196) · DSCIP (197–217) |
| Cap. VI — Nível de Apoio | 218–233 | Gabinetes (220–227), COB (228–233) |
| Cap. VII — Nível de Execução | 234–263 | DOp (235–246), CRBM (247–252), UBM/BBM/Cia/Pel (253–263) |
| Finais | 264–266 | extensão às demais unidades, NGAs, casos omissos |

## DE-PARA: tema → artigos (com nível de correspondência)

Níveis: **exata** (mesmo assunto e alcance) · **parcial** (parte do tema/alcance
diferente) · **temática** (assunto vizinho, inspiração) · **ausente**.

| # | Tema | Artigos MT | Nível | Observações | Recomendação |
|---|---|---|---|---|---|
| 1 | `disposicoes-preliminares` | 1º, 2º, 3º | **exata** | Natureza (força auxiliar), subordinação (Governador; vínculo operacional à Sesp) e competências institucionais (11 incisos). Espelho perfeito para abrir a minuta de RO — adaptar referências à CE de MT. | **Transcrever integral** (3 artigos) |
| 2 | `organizacao-geral` | 4º, 5º | **exata** | Art. 4º define os 7 níveis; Art. 5º lista TODOS os órgãos hierarquizados. Na minuta de RO, o Art. 5º deve ser **substituído pela estrutura da LOB de RO** (ro.json) — transcrever o Art. 4º verbatim e usar o 5º só como MODELO DE FORMA (numeração aninhada). | **Transcrever Art. 4º; Art. 5º como modelo de forma** (não verbatim — estrutura é a de RO) |
| 3 | `competencias-direcao` | 6º–14 | **exata** | Cmt-Geral (6º–8º, competências em ~20 incisos), Conselho Superior (9º–10), Cmt-Geral Adjunto (11–12), EMG (13–14). Núcleo da direção. | **Transcrever integral** (9 artigos) |
| 4 | `competencias-apoio-assessoramento` | 34–59 · 218–233 | **exata** | Duas frentes: Assessoramento Superior (34–59) e Nível de Apoio (218–233). Padrão interno: caput do órgão → competências do órgão → competências do chefe → seções internas. Para a minuta, os artigos de **órgão** importam mais que os de subseção micro (protocolo, arquivo…). | **Transcrever caputs + competências de órgão** (34–38, 40–41, 43–44, 46–48, 52–54, 59, 218–220, 224, 228–229); cargo/subseção só sob demanda |
| 5 | `competencias-execucao` | 234–263 | **exata** | Definição (234), DOp (235–246), CRBM (247–252), UBM: Batalhões (253–261), Companhias (262), Pelotões (263). Casa com Execução Ordinária/Especializada da LOB de RO. BEA/GAvBM (estrutura no Art. 5º) não têm artigos próprios de competência — cobertos pelo 264. | **Transcrever** 234–238, 247–250, 253–255, 262–263; 239–246/251–252/256–261 (adjuntos e seções) sob demanda |
| 6 | `servico-operacional` | 228–233 · 258 | **temática** | COB (centro de operações; despacho/coordenação) e Seção de Operações do BBM tangenciam, mas NÃO há regime de escalas/guarnições operacionais. | **Não transcrever para este tema** — buscar em SE (RISD) e RN |
| 7 | `servico-interno-dia` | **158** | **parcial** | Achado fora do garimpo: a Companhia de Comando e Serviço (dentro da Ajudância Geral/QCG) organiza escalas, comanda a parada diária, mantém o livro do **Adjunto de Dia**, formatura de início/término de expediente e guarda do quartel. É a ÚNICA norma de serviço interno do documento. | **Transcrever Art. 158 (7 incisos)** com selo `parcial`; complementar com SE/RN |
| 8 | `atribuicoes-funcoes` | 62–63, 67, 111, 123, 137, 144, 153, 163–164, 170, 181–182, 190–191, 200–201, 221–222, 225, 230, 238–239, 250–251, 255–256, 262–263 | **exata** | Todo órgão tem artigos "Compete ao [Diretor/Coordenador/Comandante/Chefe]". Riquíssimo, mas transcrever TUDO duplicaria o documento. Priorizar as funções que existem na LOB de RO: Cmt-Geral (8º), Adjunto (12), Corregedor (19), Diretores (62, 163, 200, 238), Cmt Regional (250–251), Cmt BBM (255–256), Cmt Cia (262), Cmt Pel (263). | **Transcrever o conjunto prioritário** (~12 artigos); demais sob demanda |
| 9 | `disciplina-correicao` | 15–33 · 72–73 | **exata** (estrutura correcional) | Corregedoria completa: definição (15–16), constituição (17), Corregedor (18–20), corregedor auxiliar (21), seções (22–33, nível micro). + Seção de Justiça e Disciplina da BM/1 (72–73). ATENÇÃO: é estrutura/competência correcional — NÃO é código disciplinar (punições/transgressões ficam em lei própria). | **Transcrever 15–21**; 22–33 (subseções micro) descartar por granularidade; 72–73 transcrever |
| 10 | `uniformes-apresentacao` | — | **ausente** | Só menções incidentais (auxílio-uniforme; "correção de atitudes e uniformes" como dever de aluno/Cmt de Cia). | Buscar em RN; registrar ausência |
| 11 | `cerimonial-honras` | 110 (X–XI), 113, 116–118 | **temática** | Cerimonial aparece como competência da Comunicação Social (realizar/elaborar normas de cerimonial) e Corpo Musical (116–118). Não há normas de continência/honras em si. | **Não transcrever para este tema**; buscar em RN. Corpo Musical pode entrar em apoio (tema 4) se RO quiser |
| 12 | `disposicoes-finais` | 264–266 | **exata** | Extensão de competências às demais unidades (264), prazo para NGAs das unidades (265 — mecanismo interessante p/ RO), casos omissos (266). | **Transcrever integral** (3 artigos) |

## Propostas de AMPLIAÇÃO da taxonomia (temas novos — taxonomia é dado, cresce)

O regulamento de MT cobre fartamente duas matérias típicas de regulamento de CBM que a
taxonomia inicial de 12 temas não previu. Proponho criar:

| Tema novo | Artigos MT | Nível | Justificativa |
|---|---|---|---|
| `ensino-instrucao` | 160–196 | **exata** | DEIP completa: diretoria (160–165), coordenadorias (166–167), CEIB (168–178), CCF (179–187), Escola Dom Pedro II (188–196), incluindo direitos/deveres do Corpo de Alunos (177–178, 195–196). RO tem ensino na LOB; a minuta vai precisar deste capítulo. Transcrever: 160–163, 168–169, 179–180, 188–189 (+ 177–178 se RO quiser normas de aluno). |
| `seguranca-contra-incendio` | 197–217 | **exata** | DSCIP completa: análise de processos (206–208), fiscalização (209–211), legislação/pareceres (212–214), perícias (215), hidrantes (216), SSCIPs regionais (217). Atividade-fim técnica que RO certamente regulamentará. Transcrever: 197–199, 206, 209, 215–217. |

## Ausências de MT → onde buscar (guia p/ os próximos de-paras)

| Tema | 1ª fonte provável | Observação |
|---|---|---|
| `servico-operacional` (escalas, guarnições, regime) | **SE — RISD** (Regulamento Interno dos Serviços Diários) | é a especialidade do RISD; RN como 2ª fonte |
| `servico-interno-dia` (complemento) | **SE — RISD** e **RN** | MT dá só o Art. 158 |
| `uniformes-apresentacao` | **RN — Regulamento Geral** | conferir no de-para de RN |
| `cerimonial-honras` | **RN — Regulamento Geral** | conferir no de-para de RN |

## Resumo para validação (o que você precisa bater o olho)

1. **Prioridade de transcrição** (colunas "Recomendação"): concorda em transcrever
   caputs+competências de ÓRGÃO e deixar subseções micro (protocolo, arquivo, almoxarifado…)
   de fora da 1ª rodada? (~90 artigos transcritos dos 266; o resto fica endereçado no
   de-para para busca posterior.)
2. **Dois temas novos** (`ensino-instrucao`, `seguranca-contra-incendio`) — aprovar?
3. **Art. 5º como modelo de forma** (estrutura da minuta vem da LOB de RO, não de MT) — ok?
4. **Renomear o arquivo de MT** ("Regimento Interno" → "Regulamento Geral") em rodada
   futura de dados, ou conviver com o rótulo?
5. Alguma matéria que você queira ADICIONAR do regulamento de MT que não esteja mapeada?
