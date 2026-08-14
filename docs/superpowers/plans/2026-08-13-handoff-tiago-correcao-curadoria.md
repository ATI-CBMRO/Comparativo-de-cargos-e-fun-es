# Handoff — correção da curadoria à luz da LOB vigente

**Para:** Ten. Tiago · **De:** Wândrio (via Claude) · **Data:** 2026-08-13
**Branch com o trabalho já feito:** `fix/curadoria-lob-atual` (4 commits, ainda **não** mesclada)
**Relatório completo:** `docs/superpowers/specs/2026-08-13-revisao-curadoria-lob-atual.md`

---

## 1. Contexto em 30 segundos

A curadoria do Regulamento montou a minuta importando texto de outros estados (MT, SE, BA, RN, RS)
e "adaptando" para RO. **A adaptação só troca nome de estado — nunca estrutura organizacional.**

Resultado: nos capítulos que dizem quem faz o quê, a minuta descreve o CBM do Mato Grosso, de
Sergipe e da Bahia com o nome do CBMRO. **32 nomes de órgão citados não existem em nenhuma das
duas LOBs de Rondônia.**

O problema atinge **os dois cenários** (atual e futura), porque `database/atual/regulamento_structure.json`
é cópia byte-a-byte da futura com os ids re-carimbados (ver `build_regulamento_structure_atual.py`).

---

## 2. O que JÁ está feito nesta branch (não refazer)

Quatro commits, todos corrigindo **causa-raiz** em `scripts/regulamento_enrichment.py` — nunca o
JSON gerado à mão. Rode `python3 scripts/build_regulamento_structure.py && python3 scripts/build_regulamento_structure_atual.py`
para reproduzir.

| Commit | O que resolveu | Medição |
|---|---|---|
| `c40e850` | `ADAPTATIONS` cobria 9 estados e **não cobria a Bahia** — fonte primária de `central-operacoes-193`, que saía com zero adaptações | "CBMBA" 3→0 por cenário |
| `f715fac` | A tabela casa texto **literal**; variantes com separador escapavam | "CBM-MT" 6→0 por cenário |
| `2ff7ae7` | Rodapé do PDF do RISD/CBMSE embutido **no meio das frases**; a adaptação trocava CBMSE→CBMRO ali dentro e a minuta passava a **afirmar a existência de um "Boletim Geral nº 060/2022" do CBMRO** | 13 dispositivos→0; frases recompostas |
| `2ff7ae7` | "PMSE" mandava acionar a PM **de Sergipe** | 1→0 |
| `bdd7e39` | Relatório da análise | — |

**Verificação que passou:** `verificar_verbatim.py` OK (1166 excerpts) · `test_regulamento_structure.py`
OK (16 capítulos, 413 artigos) · `npm test` 154/154 · 413 artigos preservados · `original_caput` mantido.

> **Detalhe importante de método:** a limpeza do rodapé roda no **build** (`limpar_ruido_de_pagina()`),
> **não** na transcrição. O rodapé está mesmo no markdown de origem e `verificar_verbatim.py` compara
> a transcrição com ele — tirar da transcrição quebraria a conferência. Mantenha esse desenho.

**Backup dos JSONs antes da primeira regeneração:**
`~/Backups/regulamentacao-lob/2026-08-13-antes-correcao-curadoria/` (na máquina do Wândrio)

---

## 3. Primeira decisão, antes de escrever código

**Pergunta que trava tudo:** o Regulamento sai por **Portaria do Comandante-Geral** ou por
**Decreto do Governador**?

A Lei 2.204/2009, **Art. 59**, reserva ao Governador, por Decreto, criar, extinguir e **dar nome** a
órgão. O **Art. 48**, que nas redações antiga/2012/2014 delegava ao regulamento definir "estrutura
básica e denominações" das unidades, foi **reescrito pela Lei 4.303/2018** — essa delegação **não
existe mais**. Sobrou o **Art. 49, par. único**, que delega só os *critérios* de dimensionamento de
OBM, por portaria.

Se for Portaria, os capítulos que criam ou renomeiam órgão são inválidos na origem, e a tarefa
muda de "corrigir nomes" para "remover matéria e remeter a Decreto". **Não comece pelo texto sem
essa resposta.**

---

## 4. Tarefas de implementação, em ordem

### T1 — Resíduos mecânicos restantes (baixo risco, faça primeiro)

Todos em `scripts/regulamento_enrichment.py` (tabela `ADAPTATIONS`) + rebuild. Cada um precisa da
resposta certa antes de virar regra:

| Resíduo | Ocorrências | Precisa saber |
|---|---|---|
| `Secretaria de Estado de Segurança Pública` | 3 | Em RO é **SESDEC** (LOB Art. 1º, par. único). Esta é segura, pode aplicar |
| `ADEMA` | 1 | Órgão ambiental de Sergipe → qual o de RO |
| `e-doc` | 1 | Sistema do CBMSE → qual o sistema de processo eletrônico do CBMRO |
| `Art. 82 da Constituição Estadual` | 1 | É o artigo da Constituição **do MT**; achar o correspondente na CE/RO |
| `CICOM` | 12 | **Não aplique ainda** — ver T2 |

**Teste de aceite de T1:** rodar a varredura abaixo e ver zero para os itens aplicados.

```bash
python3 - <<'EOF'
import json, re
d = json.load(open('database/atual/regulamento_structure.json'))
def textos():
    for ch in d['chapters']:
        for a in ch.get('articles', []):
            yield a.get('caput') or ''
            for x in (a.get('items') or []):
                yield (x.get('text') if isinstance(x, dict) else str(x)) or ''
for nome, pat in {
    'CBM outro estado': r'\bCBM[\s.\-–—/]*(?:MT|SE|BA|RN|RS|AL|GO|PA|PR|DF)\b',
    'PM outro estado':  r'\bPM[\s.\-–—/]*(?:MT|SE|BA|RN|RS|AL|GO|PA|PR|DF)\b',
    'rodape/RISD':      r'BGO\s*N[ºo°]\s*060|\bRISD\b',
    'ADEMA':            r'\bADEMA\b',
    'e-doc':            r'\be-doc\b',
    'CICOM':            r'\bCICOM\b',
    'Secretaria SP MT': r'Secretaria de Estado de Seguran[çc]a P[úu]blica',
}.items():
    rx = re.compile(pat, re.I)
    print(f'{nome:20} {sum(len(rx.findall(t)) for t in textos()):3}x')
EOF
```

### T2 — Central de operações / capítulo 193 (`central-operacoes-193`, 3 art / 65 incisos)

**Fato que muda tudo:** o **COCB** (Centro de Operações e Comunicações de Bombeiros) foi
**revogado** pelo **Art. 51, pela Lei 4.303/2018**. A LOB vigente **não tem nenhuma central de
operações** — o Art. 35 (Comando Operacional) não a recriou.

A minuta usa **quatro nomes** para a mesma coisa: `CICOM` (Bahia, 12x), `Centro de Operações`
(usado nos arts. de fonte SE), `CIOSP` e `Centro de Operações de Bombeiros` (MT, art. 155).

Além do CICOM, o capítulo tem resíduos baianos que **não citam o nome do estado** (por isso a
varredura automática não pega): `SSP` (é a secretaria da Bahia; em RO é SESDEC), `Coordenadores de
Área`, `Coordenadoria de Saúde` (RO não tem órgão de saúde — Art. 62 revogado pela Lei 2.244/2010),
`Grupo de Despacho/GD`, `SGTO`, `Supervisor de Operações`, `Adjunto ao Oficial de Dia`, e remissão a
`ANEXO A desta Portaria` (anexo da norma baiana, inexistente aqui).

**Bloqueado por:** decidir a denominação oficial e se o CBMRO opera central própria ou dentro do CIOSP.

### T3 — Segurança contra incêndio (`seguranca-contra-incendio`, 19 art / 184 incisos)

É o **regimento interno da DSCIP do Mato Grosso**. Em RO a matéria é da **Coordenadoria de
Atividades Técnicas** — **LOB Art. 18**, com estrutura taxativa no §1º:

> I Coordenador · II Adjunto · III Seção Administrativa · IV Seção de Estudos Técnicos ·
> V Seção de Planejamento, Fiscalização e Suporte Técnico · VI Diretorias de Atividades Técnicas
> (a Diretor · b Adjunto · c Seção Administrativa · d Seção de Vistoria · e Seção de Análise de
> Projetos · f Seção de Investigação e Prevenção de Incêndio · g Seção de Hidrantes ·
> h Seção de Atividades Técnicas)

**Nenhuma** das 17 unidades listadas no art. 166 da minuta coincide. Recomendação do levantamento:
**reescrever o capítulo sobre a CAT**, não remendar ponto a ponto.

Dois pontos de hierarquia de norma neste capítulo:
- **"multar"** aparece em 4 dispositivos — a palavra **não existe na LOB**. Sanção pecuniária exige
  lei. Só manter se houver lei estadual de SCI em RO que a preveja (e citá-la no dispositivo).
- **Art. 18, §2º** (Lei 4.488/2019) é o mecanismo legal de vinculação das Seções de Atividades
  Técnicas a Grupamentos/Subgrupamentos — e é **facultativo, por ato do Comandante-Geral**. O art.
  182 da minuta afirma vinculação automática, o que contraria a lei.

### T4 — Atribuições das funções (`atribuicoes-funcoes`, 29 art / 345 incisos)

**25 dos 29 artigos com incompatibilidade.** É o Título III do Regulamento Geral do CBMMT.

Mapeamento MT → LOB de RO (Lei 2.204/2009) levantado na análise:

| Na minuta (MT) | Na LOB vigente de RO |
|---|---|
| Diretoria de Administração Institucional | Chefe do Estado-Maior-Geral (Art. 12-A) |
| Coordenador de Gestão de Pessoas | Coordenadoria de **Pessoal** (Art. 14); "Gestão de Pessoas" é **Diretoria** dentro dela |
| Coordenador de Comunicação Social | **Diretoria** de Comunicação Social (Art. 22) |
| Coordenadoria de Legislação e Doutrinas | Assessoria Especial / Assessoria Legislativa (Art. 29, §1º, I e II) |
| Coordenadoria de Finanças | Coordenadoria de Planejamento, Orçamento e Finanças (Art. 16) |
| Coordenador da Ajudância Geral | **Ajudante-Geral** (Art. 25) |
| **Comandante-Geral Adjunto** | **Subcomandante-Geral** (Art. 12) — *não existe "adjunto" em RO* |
| DEIP (Ensino, Instrução e Pesquisa) | Coordenadoria de Educação, Ensino e Instrução (Art. 15) |
| CEIB | Centro de Treinamento, Ensino e Instrução (Art. 15, V, "d") |
| Centro de Capacitação Física | **não existe** (0 ocorrências na LOB) |
| Escola Dom Pedro II | Unidades de Colégio BM (Art. 15, IV, "f") — *conferir se há colégio ativado* |
| DSCIP | Coordenadoria de Atividades Técnicas (Art. 18) |
| Diretoria Operacional | **Comando Operacional de Bombeiro Militar** (Arts. 34 e 35) |
| Comando Regional | **não existe** — extinto com a redação de 2018 |
| **Batalhão** | **não existe** (0 ocorrências) → Grupamento (Art. 47, I) |
| **CiaBM** | → Seção de Bombeiros (Art. 47, V) |
| **Pelotão** | **não existe na redação vigente** → Grupo de Bombeiros (Art. 47, VI) |
| Comandante Adjunto | **Subcomandante** (Art. 47, §1º, I, "b") |
| UBM | **OBM** (31 ocorrências a trocar no documento inteiro) |

**Cuidado (Art. 19 da LOB):** cargo de **Coordenador** é privativo de **Oficial do último posto**.
Cada "Coordenadoria" que o texto criar implica um cargo de Coronel — a correção não é só de nome, é
de desenho de efetivo.

### T5 — Serviço operacional e serviço de dia (fonte SE, 128 artigos)

- `Diretoria/Diretor de Operações` → **Comando/Comandante Operacional de Bombeiro Militar**
  (**20 ocorrências**, o defeito mais disseminado)
- `Seção de Recursos Humanos da DO` → **Seção de Pessoal** do Comando Operacional (Art. 35, III)
- **Escalas desenhadas para estado compacto:** Superior de Dia em sobreaviso **proibido de sair da
  área da residência** e ao mesmo tempo **responsável por todo o território estadual** (arts. 9 e
  16); Supervisor de Dia obrigado a comparecer a toda ocorrência com duas ou mais Unidades (art.
  58). Inexequível em Rondônia — regionalizar por Grupamento.
- **Funções órfãs e nomes concorrentes:** "Comandante de Área" (listado e nunca regulado),
  "Cmt do SOS", "Chefe da Prontidão", "Comandante de Operações" — uniformizar contra o rol do art. 7
- **Doutrina de comando contraditória:** art. 57 manda comandar por **antiguidade**, art. 41 manda
  seguir o **Sistema de Comando de Incidentes**. Escolher uma
- **5 regras conflitantes de "casos omissos"** — manter só a do art. 185 (Comandante-Geral)

### T6 — Fundamento legal (afeta o documento inteiro)

- **Nenhum dos 185 artigos menciona a Lei nº 2.204/2009.** Não há artigo de fundamento, cláusula de
  vigência nem cláusula revogatória
- **Art. 3 da minuta lista 11 competências; o Art. 2º da LOB tem 25.** O texto importado **suprime**
  competências legais (atendimento pré-hospitalar, guarda-vidas, socorro a embarcações, perícia
  técnica, vistorias, embargo/interdição, polícia judiciária militar, entre outras) e condiciona a
  convênio uma fiscalização que a lei dá como poder próprio (Art. 2º, VII, "c")
- Nomenclatura de defesa civil desatualizada: usar **SIEPDEC/CEPDEC** (Art. 17, red. Lei 5.697/2023)

### T7 — Regimento Interno do cenário FUTURO

`database/minuta_structure.json` tem **21 siglas de outros estados** no texto proposto:
CBMDF 10x, CBMMT 7x, CBM-MT 2x, CBMPA 2x (nos órgãos `cg`, `dp`, `deei`, `dsap`, `dlog`, `ccs`, `ag`,
`corregedoria`). **O RI do cenário atual está limpo (0).** Não afeta a reunião de 14/08.

---

## 5. Como validar qualquer alteração

```bash
python3 scripts/build_regulamento_structure.py
python3 scripts/build_regulamento_structure_atual.py
python3 scripts/verificar_verbatim.py        # transcrição fiel à fonte
python3 scripts/test_regulamento_structure.py # schema + contagem
npm test                                      # 154 testes
```

Sempre confira o **diff semântico** antes de commitar — regenerar o JSON inteiro esconde mudança
não intencional no `git diff`. Compare artigo a artigo (caput + incisos) contra a versão anterior e
confirme que só mudou o que você quis.

**Invariantes:** 413 artigos · 16 capítulos · `original_caput` preservado sempre que `adapted=True`
(é o que o comparador exibe ao lado do texto proposto).

---

## 6. Observação sobre o ambiente da reunião

O acesso setorizado (perfil `escopo: "servico"`, rota `/regulamento/servico`) já está em produção
desde 12/08 — ver `docs/superpowers/plans/2026-08-13-regulamento-servico-escopo.md`.

Os comentários são ancorados no **`editId` do dispositivo**, não no número do artigo. Então tudo que
for marcado na reunião **sobrevive** à renumeração e à reescrita dos capítulos previstas acima.
Nada do que a comissão marcar se perde quando essas correções forem aplicadas.
