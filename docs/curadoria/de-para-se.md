# De-para — Sergipe (Lote 1)

> **B1-M passo 2** — mapeamento produzido pelo Fable em 2026-07-06 (leitura estrutural
> integral). Apoio: `candidatos-se.md`. **Aguarda validação do Wândrio (passo 3).**

## Identificação da fonte

| Campo | Valor |
|---|---|
| Documento | **RISD — Regulamento Interno dos Serviços Diários do CBMSE** |
| Versão | Atualizado em março de 2022 |
| Arquivo | `Sergipe - Regimento Interno.md` (150 artigos, 12 capítulos) |
| Rótulo de fonte | `cf. CBMSE, RISD (atual. 2022), Art. NN` |

É o documento-alma dos capítulos de SERVIÇO da minuta de RO (temas 6 e 7) — matéria que
MT e RN não regulam. Já era usado como fonte da "Guarnição" na minuta de RI
(`minuta_enrichment.py: GUARNICAO_CHAPTER`) — a curadoria nova NÃO deve duplicar o que
já está lá; reaproveitar/referenciar.

## Estrutura do documento

| Capítulo | Artigos | Conteúdo |
|---|---|---|
| I — Finalidade | 1º | dispor sobre o serviço operacional diário |
| II — Objetivos | 2º | objetivos do regulamento |
| III — Políticas operacionais | 3º | princípios do serviço operacional |
| IV — Funções operacionais | 4º | rol das funções do serviço diário |
| V — Atribuições | 5º–22 | por função: Superior de Dia (5–6), …, Auxiliares da Guarda (20), Socorristas (21), Permanência (22) |
| VI — Regime e Escalas de Serviço | 23–53 | carga horária adm./operacional, escalas, permutas, atestados, uniforme do serviço (53) |
| VII — Rotina Diária das Unidades | 54–111 | quadro de rotina (54), dia operacional (55…), permutas fora do prazo (112 é do VIII) |
| VIII — Situações Extraordinárias | 112–116 | prontidão, chamadas extraordinárias |
| IX — Viaturas Operacionais | 117–128 | classificação e regras de uso (proibições no 118) |
| X — Apoio Operacional | 129–135 | atendimento e apoio entre unidades |
| XI — Procedimentos nas Ocorrências | 136–147 | comando do socorro, área de emergência |
| XII — Disposições Gerais | 148–150 | deveres (148) e vedações (149) do BM nas operações; casos omissos (150) |

## DE-PARA: tema → artigos

| Tema | Artigos | Nível | Observações / recomendação |
|---|---|---|---|
| 6 servico-operacional | 1º–4º · 23–53 · 112–147 | **exata** | Núcleo: princípios (1–4), regime/escalas (23–53), extraordinárias (112–116), viaturas (117–128), apoio (129–135), ocorrências (136–147). Transcrever integral, na Rodada T2. |
| 7 servico-interno-dia | 54–111 | **exata** | Rotina diária completa das unidades (quadro de rotina no 54). Transcrever integral (é o coração do tema). |
| 8 atribuicoes-funcoes | 5º–22 | **exata** | Atribuições de TODAS as funções do serviço (Superior de Dia, Chefe de Guarnição, Socorrista, Permanência…). ⚠️ Conferir sobreposição com `GUARNICAO_CHAPTER` já curado em minuta_enrichment.py — reaproveitar, não duplicar. |
| 10 uniformes-apresentacao | 53 | **parcial** | Único artigo do acervo sobre uniforme (o do serviço). Transcrever com selo parcial — melhor que nada até chegarem PDFs específicos. |
| 12 disposicoes-finais | 148–150 | **exata** | Deveres/vedações nas operações + casos omissos. Transcrever integral (148–149 podem também ancorar um futuro capítulo de deveres operacionais). |
| 1 disposicoes-preliminares | 1º–2º | **parcial** | Finalidade/objetivos são DO REGULAMENTO DE SERVIÇO, não da corporação — usar só como referência de forma no comparador, selo parcial. |
| 2–5, 9, 13–15 (organização, direção, correição, ensino, SCIP, pessoal) | — | **ausente** | O RISD não trata — fontes: MT/RN/DF/PA/RS/AL. |

**Escopo recomendado:** transcrição INTEGRAL (150 artigos), com a checagem de
sobreposição com a curadoria de Guarnição já existente.
