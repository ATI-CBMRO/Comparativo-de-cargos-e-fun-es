# Conferência das 71 sugestões do Regulamento (Firestore) — pós-rodada 18/08/2026

**Data:** 2026-08-18
**Plano:** `docs/superpowers/plans/2026-08-18-regulamento-servico-correcoes-fase2.md` (Task 10)
**Fonte:** coleção `suggestions` do Firestore, filtradas por `dispositivoId` iniciando em
`reg:` (71 das 81 sugestões existentes — as demais 10 são do Regimento Interno, fora de
escopo). Todas de autoria do Ten. Tiago e do Wândrio (Wândrio também tem 1 sugestão de teste,
sinalizada abaixo).

## Método

Cada sugestão foi cruzada contra o estado do documento **depois** das Tasks 1-9 (+ o fix
extra desta conferência). Classificação em 4 categorias:

- **✅ RESOLVIDA** — o dispositivo que a sugestão aponta foi removido ou reescrito pela
  rodada; a sugestão não se aplica mais ao texto atual.
- **🔶 ENDEREÇADA (parcial)** — a matéria da sugestão passou a ser tratada em outro lugar do
  documento (ex.: remissão nova), mas o dispositivo original em si não foi editado.
- **🔧 CORRIGIDA NESTA CONFERÊNCIA** — a leitura da sugestão revelou um defeito objetivo que
  não estava mapeado nas Tasks 1-9; corrigido agora com o mesmo mecanismo já aprovado (commit
  `66a3a96`).
- **🔴 PENDENTE** — fora do escopo desta rodada (terminologia/CIOP/mídia/ATTS/Cap. V); precisa
  de leitura humana ou decisão do CONDEG. Não foi tocada.

## ✅ Resolvidas — 15 sugestões

O artigo `se-art-113` (imprensa) foi removido por inteiro pela Task 6 e substituído pela
remissão à Resolução 121/2022 — as 6 sugestões abaixo pediam exatamente isso:

| dispositivoId | Sugestão |
|---|---|
| `se-art-113#0` | "Suprimir." |
| `se-art-113#1` | "Suprimir." |
| `se-art-113#2` | "Suprimir." |
| `se-art-113#3` | "Suprimir." |
| `se-art-113#4` | "Suprimir." |
| `se-art-113#caput` | "Suprimir os incisos e citar o Manual de Relacionamento com a Mídia elaborado pela DCS." — **é literalmente o que a Task 6 fez.** |

`se-art-48`/`se-art-49` (regime de serviço do Despachante ao CIOP) removidos pela Task 5,
matéria já regulada pela NGA-CIOP-001/2026 — as 2 sugestões pediam isso:

| `se-art-48#caput` | "Compete ao Capítulo III a regulamentação do serviço do CIOP." |
| `se-art-49#caput` | "Compete ao Capítulo III a regulamentação do serviço do CIOP." |

Terminologia "Supervisor de Dia" corrigida pela Task 4 — as 6 sugestões apontavam exatamente
essa duplicidade:

| `se-art-4#1` | "Duplicidade com 'Superior de Dia'." — inciso suprimido |
| `se-art-32#caput` | "Duplicidade com 'Superior de Dia'." — virou Oficial de Dia |
| `se-art-33#caput` | "Duplicidade com 'Superior de Dia'." — virou Oficial de Dia |
| `se-art-34#caput` | "Duplicidade com 'Superior de Dia'." — virou Oficial de Dia |
| `se-art-35#caput` | "Duplicidade com 'Superior de Dia'." — virou Oficial de Dia |
| `se-art-38#caput` | "Duplicidade com 'Superior de Dia'." — virou Superior de Dia (área estadual) |

`se-art-114#5` — "Definição adequada da cadeia de comando. Supressão do Superior de Dia" — é
exatamente a reescrita da cadeia de escalonamento que a Task 4 fez (Cmt SGBM → Cmt GBM → Cmt
COB → Superior de Dia).

## 🔶 Endereçadas (parcial) — 8 sugestões

Todas em `se-art-116` (protocolo de atendimento a pacientes com transtorno mental via SAMU),
pedindo verificação do protocolo ATTS:

`se-art-116#0`, `#1`, `#2`, `#3`, `#4`, `#5`, `#6`, `#caput` — todas: "Verificação do
protocolo adotado para ATTS."

A Task 7 criou um artigo **novo e autônomo** de remissão ao ATTS em `servico-operacional`
(não dentro de `se-art-116`). A lacuna apontada (o documento não tinha nenhuma menção ao
ATTS) está fechada — mas o texto de `se-art-116` em si não foi alterado para citar o
protocolo diretamente. Se a intenção do Ten. Tiago for que o PRÓPRIO `se-art-116` remeta ao
artigo do ATTS (não só que o ATTS exista em algum lugar do documento), falta uma remissão
cruzada — registrado como pendência abaixo.

## 🔧 Corrigidas nesta conferência (achado novo) — 3 sugestões

| `se-art-26#caput` | "A quem compete a coordenação do serviço diário de Superior de Dia?" |
| `se-art-30#caput` | "Artigo em duplicidade com o Art. 10" |
| `se-art-37#caput` | "Duplicidade com 'Superior de Dia'." |

Os três artigos citavam "Seção de Recursos Humanos" como subunidade do Comando Operacional
de Bombeiros — o MESMO defeito já corrigido em `se-art-34` pela Task 4 (a LOB, Art. 35,
parágrafo único, III, chama essa seção de **Seção de Pessoal**). Escaparam do levantamento
original porque não citam "Supervisor de Dia" literalmente. Corrigido agora (commit
`66a3a96`, revisado e aprovado) com o mesmo mecanismo `SUBSTITUIR_TERMOS`.

**Atenção:** isso resolve só o defeito de NOMENCLATURA. As perguntas substantivas originais
de cada sugestão continuam abertas (ver Pendentes): `se-art-26` pergunta A QUEM compete a
coordenação (resposta de mérito, não de nome); `se-art-30` aponta duplicidade de conteúdo com
outro artigo (`se-art-10`, a conferir); `se-art-37` pode ser o mesmo caso de duplicidade que
`se-art-30` (os dois têm texto quase idêntico sobre permuta de serviço).

## 🔴 Pendentes — 45 sugestões

Fora do escopo desta rodada (terminologia/CIOP/mídia/ATTS/Cap. V). Agrupadas por natureza:

### Bloco `se-art-23` (8 sugestões) — estrutura do artigo
`se-art-23#0` a `#7`: "Corrigir o título do inciso I", "Subitem do inciso I/II" (x6). Parecem
apontar problemas de extração/numeração do artigo (inciso mal segmentado do PDF de origem).
Precisa reler o artigo inteiro contra a fonte antes de decidir — não é find-replace simples.

### Bloco `se-art-135` (5 sugestões) — Grupamento de Operações Aéreas / cobertura territorial
`#8` "inexistência do SAMU em todas as localidades", `#9` "inexistência de tal companhia",
`#10` "quem aciona o helicóptero do GOA? Oficial ou Superior de Dia? Protocolo pro
interior?", `#11` "nas localidades que possuem o referido órgão", `#12` "informação fora do
contexto 'Grande Porte'". Todas de mérito operacional — dependem de decisão do Ten. Tiago/
CONDEG sobre cobertura real do GOA e do SAMU no interior do Estado.

### Bloco `se-art-127` (3 sugestões) — Parte Especial / documentação
`#3` excluir cláusula de "acordo formal entre as partes", `#4` "inexistência do referido
documento", `#7` redação de "relatar os fatos, através de Parte Especial". Mérito
documental/processual.

### Bloco "duplicidade entre artigos" (5 sugestões)
`se-art-30` (dup. com Art. 10 — nota: nomenclatura já corrigida, duplicidade de conteúdo
segue aberta), `se-art-41`/`se-art-45` ("utilizar o próprio Regulamento de Serviço como base
legal" — sugerem trocar o fundamento citado), `se-art-46` (dup. com Art. 27), `se-art-47`
(dup. com Art. 28). Precisa ler os pares de artigos lado a lado para decidir qual fica.

### Bloco "a quem compete" (4 sugestões)
`se-art-25` (autorizar permuta), `se-art-27`, `se-art-29`, `se-art-26` (coordenação do
serviço — nomenclatura já corrigida, mérito segue aberto). Perguntas de atribuição/hierarquia
que exigem decisão, não achado textual.

### Bloco Oficial/Superior de Dia — mérito, não terminologia (4 sugestões)
`se-art-24#caput` ("alterar o cargo a quem o Superior de dia deverá reportar"), `se-art-24#0`
("chancelar a Parte Diária do Oficial de Dia?"), `se-art-24#1` ("quem altera o regime do
serviço?"), `se-art-132#caput` (propõe trocar "presença do Oficial de Dia" por "ciência ao
Superior de Dia" — mudança de REGRA, não de nome). A Task 4 corrigiu só a terminologia
(Supervisor→Oficial/Superior); estas 4 pedem mudança de conteúdo/competência.

### Bloco Wândrio — organização geral e disposições preliminares (7 sugestões)
`ro-art-2#7`, `ro-art-6#10`, `ro-art-6#15`, `ro-art-7#6`, `ro-art-8#7` (retirar conjunção "e"
duplicada / corrigir duplicidade de título — ortografia, mas em `organizacao-geral`, capítulo
que já foi 100% reescrito em 13/08 e está fora do escopo desta rodada), `mt-art-3#2` (incluir
"Proteção" no título do inciso), `mt-art-3#caput` (pergunta se as 25 competências do Art. 2º
da LOB deveriam ser importadas por inteiro — decisão de escopo, não erro).

### Diversos (9 sugestões)
`se-art-36#caput` ("duplicidade com Superior de Dia" — **não encontrei o termo no artigo
atual**; pode ser rótulo copiado por engano ao percorrer sequencialmente `se-art-32` a
`se-art-38`, ou apontar duplicidade de CONTEÚDO com outro artigo da mesma região, não de
termo — precisa esclarecimento do Ten. Tiago), `se-art-43#caput` (mover artigo de posição),
`se-art-44#caput` (erro de digitação em "excepcionais" — ortografia pura, mas fora do
recorte tocado), `se-art-50#caput` ("sem previsão legal, manter?"), `se-art-52#caput`
(verificar rotina da Junta Militar de Saúde), `se-art-112#caput` ("pode ser suprimido"),
`se-art-115#caput` (resíduo de extração no título), `se-art-117#caput` ("Comandante-Geral",
sentido pouco claro sem reler o artigo), `se-art-134#caput` (proposta de reserva operacional
para ocorrências de grande vulto).

### Sugestão de teste (1) — recomendo exclusão
`mt-art-1#caput`, autor "Wandrio teste", 2026-08-13: **"TEste de sugestao wandrio"**. Não é
conteúdo real — parece ter sido deixada de um teste do fluxo de sugestões. Recomendo ao
Wândrio excluir pelo próprio app (`/regulamento/servico`, balão de sugestões).

## Resumo

| Categoria | Qtde |
|---|---:|
| ✅ Resolvida | 15 |
| 🔶 Endereçada (parcial) | 8 |
| 🔧 Corrigida nesta conferência | 3 |
| 🔴 Pendente | 45 |
| **Total** | **71** |

## Recomendação

As 45 pendentes não são, em sua maioria, ortografia — são perguntas de mérito operacional
("a quem compete", "protocolo para o interior", "duplicidade de conteúdo entre artigos") que
pedem leitura humana e, em vários casos, decisão do CONDEG. Não foram tocadas nesta rodada
para não expandir o escopo já aprovado no spec (`2026-08-18-regulamento-servico-correcoes-
fase2-design.md`). Sugiro tratá-las como um novo item de backlog — "3ª rodada de curadoria do
Regulamento de Serviço: bloco se-art-23, se-art-127, se-art-135 e as perguntas de
competência" — registrado em `.claude/PENDENCIAS.md`.
