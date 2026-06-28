# Frente 2 — Curadoria verbatim dos 15 órgãos novos no comparador

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preencher os 15 órgãos da LOB que hoje aparecem com "0 estados" no `/comparar`, curando competências verbatim de outras legislações estaduais, de forma puramente aditiva.

**Architecture:** Trabalho de dados em 3 arquivos (`scripts/minuta_enrichment.py`, `scripts/minuta_comparison_lib.py`, `docs/ENRIQUECIMENTO_MINUTA.md`), em 4 tarefas por bloco de categoria + 1 tarefa final de verificação. Cada tarefa: subagente de pesquisa (somente leitura nos `database/markdown/*.md`) → integração manual → regeneração dos JSON → verificação de não-regressão → commit. Nenhuma mudança em código de build/frontend; `database/organs_detail/ro.json` e `database/comparativo_dpo_cot.json` nunca são tocados.

**Tech Stack:** Python 3 (scripts de build, sem suíte de testes no pipeline de dados), Node `--test` (suíte JS existente em `src/lib/minutaArticles.test.js`), Git.

---

## Contexto compartilhado (ler antes de qualquer tarefa)

**Os 15 órgãos sem cobertura** (confirmado por `python scripts/build_minuta_comparison.py`):

| organ_key | Nome (em `ro.json`) | Bloco |
|---|---|---|
| `cg` | Comando Geral | 1 |
| `depdec` | Diretoria Estadual de Proteção e Defesa Civil | 1 |
| `condeg` | Conselho Deliberativo de Estratégia e Gestão | 1 |
| `dp` | Diretoria de Pessoal | 2 |
| `deei` | Diretoria de Educação, Ensino e Instrução | 2 |
| `dpof` | Diretoria de Planejamento, Orçamento e Finanças | 2 |
| `dsap` | Diretoria de Saúde e Assistência ao Pessoal | 2 |
| `dlog` | Diretoria de Logística | 2 |
| `cint` | Coordenadoria de Inteligência | 2 |
| `ccs` | Coordenadoria de Comunicação Social | 2 |
| `cinf` | Coordenadoria de Informática | 2 |
| `assessorias` | Assessorias | 3 |
| `gab-cg` | Gabinete do Comandante-Geral | 3 |
| `ag` | Ajudância-Geral | 3 |
| `corregedoria` | Corregedoria-Geral | 4 |

**Critério de inclusão (verbatim/enumerado).** Só entra competência **enumerada e
verbatim** — incisos limpos transcritos da fonte. Fica **fora**: texto condensado,
paráfrase, ou narrativo por subdivisão (parágrafos longos não decomponíveis em
incisos sem cortar/parafrasear). Esse é o mesmo critério já aplicado e documentado
em `docs/ENRIQUECIMENTO_MINUTA.md`.

**Natureza aditiva (regra invariável).** As chaves já curadas em `ENRICHMENT_ORGAN`
(`dpo`, `cot`, `crbm`, `bbm`, `cibm`, `bbs`, `boa`) e em `AUTO_MATCH_KEYWORDS`
(`dpo`, `cot`, `doe`, `crbm`, `bbm`, `cibm`, `gbm`, `bbs`, `bifea`, `boa`, `cat`)
**não podem ser alteradas**. `database/organs_detail/ro.json` e
`database/comparativo_dpo_cot.json` **não podem ser tocados**.

**Padrão de código em `scripts/minuta_enrichment.py`.** O arquivo usa o helper:

```python
def _tag(items, source):
    return [{"text": t, "source": source} for t in items]
```

Cada competência vira uma lista de strings nomeada `_XX_ORGAO` (XX = sigla do estado,
ORGAO = sigla do órgão na fonte), e o dict `ENRICHMENT_ORGAN` (linha ~314) recebe uma
chave nova por organ_key, exatamente no mesmo formato das existentes. Exemplo real
atual (não alterar — só imitar):

```python
ENRICHMENT_ORGAN = {
    "dpo":  _tag(_MT_DOP,   "cf. CBMMT, RI, Art. 236")
          + _tag(_PA_COP,   "cf. CBMPA, Lei nº 11.060/2025, Art. 16")
          ...
    "bbm":  _tag(_PR_BBM,  "cf. CBMPR, Lei nº 22.206/2024, Art. 35, I"),
}
```

**Padrão de código em `scripts/minuta_comparison_lib.py`.** O dict
`AUTO_MATCH_KEYWORDS` (linha ~27) mapeia `organ_key -> {"include": [...], "exclude": [...]}`,
com palavras-chave **já normalizadas** (sem acento, minúsculas — a função `norm()`
casa contra o nome do órgão). Exemplo real atual:

```python
AUTO_MATCH_KEYWORDS = {
    "dpo":   {"include": ["planejamento"],                     "exclude": []},
    "crbm":  {"include": ["regional", "regiao de bombeiro"],   "exclude": []},
}
```

**Fontes de pesquisa.** Os arquivos em `database/markdown/` (48 arquivos). Para cada
estado, há tipicamente uma "Organização Básica" (LOB) e às vezes um "Regimento
Interno"/"Regulamento"/"Normas Gerais de Ação". Estados já avaliados com seus achados
e descartes estão na tabela de `docs/ENRIQUECIMENTO_MINUTA.md` — mas aqueles
descartes foram avaliados para os órgãos operacionais/técnicos; **reavalie cada
estado do zero para os órgãos deste plano** (uma LOB pode não enumerar COT mas
enumerar Diretoria de Pessoal).

**Comandos de regeneração (rodar sempre nesta ordem):**

```bash
python scripts/build_minuta_structure.py
python scripts/build_minuta_comparison.py
```

**Suíte de testes JS (deve continuar passando):**

```bash
node --test src/lib/minutaArticles.test.js
```

---

## Prompt de pesquisa (reusar em cada Task, trocando só a lista de órgãos)

> Pesquisa SOMENTE LEITURA. Você varre os arquivos em `database/markdown/` (LOBs e
> Regimentos/Regulamentos dos estados brasileiros — exceto Rondônia/RO, que é a
> referência). Para CADA órgão da lista abaixo, procure em cada estado um órgão
> equivalente por função (os nomes variam: "Diretoria de Pessoal", "Diretoria de
> Gestão de Pessoas", "Departamento de Pessoal" → todos casam com `dp`). Reporte
> apenas competências **enumeradas e verbatim** (incisos/itens limpos, transcritos
> exatamente da fonte). DESCARTE texto condensado, paráfrase, caput meramente
> definicional, ou narrativo por subdivisão. Para cada achado, informe:
> `organ_key`, sigla do estado, citação exata da fonte (lei/decreto/RI + artigo +
> inciso se houver), e a lista de itens verbatim (cada item começando em letra
> minúscula, sem o número do inciso, terminando sem ponto final — seguindo o estilo
> das listas já existentes em `scripts/minuta_enrichment.py`). Para órgãos sem
> nenhuma fonte verbatim, reporte explicitamente "nenhum match" e o motivo de
> descarte por estado relevante. NÃO edite nenhum arquivo; apenas reporte.
>
> Órgãos desta rodada: <LISTA DO BLOCO>

---

### Task 1: Bloco 1 — Direção Geral/Colegiada (`cg`, `depdec`, `condeg`)

**Files:**
- Modify: `scripts/minuta_enrichment.py` (adicionar listas `_XX_*` antes do dict `ENRICHMENT_ORGAN` na ~linha 311; adicionar chaves `cg`/`depdec`/`condeg` ao dict na ~linha 314)
- Modify: `scripts/minuta_comparison_lib.py` (adicionar chaves `cg`/`depdec`/`condeg` ao `AUTO_MATCH_KEYWORDS` na ~linha 27)
- Modify: `docs/ENRIQUECIMENTO_MINUTA.md` (nova subseção do bloco)
- Regenera: `database/minuta_structure.json`, `database/comparativo_minuta.json`

- [ ] **Step 1: Pesquisa por subagente**

Dispatch um subagente de pesquisa com o "Prompt de pesquisa" acima, com
`<LISTA DO BLOCO>` = `cg` (Comando Geral / Comando-Geral), `depdec` (Diretoria/órgão
de Proteção e Defesa Civil), `condeg` (Conselho Deliberativo / Conselho Superior /
Conselho de Administração). Aguarde o relatório de achados + descartes.

Nota de domínio para o subagente: `cg` é o órgão de cúpula — muitas LOBs descrevem
as competências do **Comandante-Geral** (pessoa), não do Comando como unidade; só
aceite se a fonte enumerar competências (caso contrário, é cargo, fora do escopo
deste comparativo de órgão). `condeg` é frequentemente raro — é esperado poucos ou
nenhum match.

- [ ] **Step 2: Integrar competências verbatim em `minuta_enrichment.py`**

Para cada achado do relatório, adicione (logo antes da linha
`# Mapeamento organ_key -> competências verbatim`, ~linha 312) uma lista nomeada e,
no dict `ENRICHMENT_ORGAN`, a chave correspondente. Use EXATAMENTE este formato
(exemplo ilustrativo — substituir pelos itens reais do relatório; se um órgão não
tiver match, NÃO crie chave para ele):

```python
# ── CBMxx, <lei/RI>, Art. N — <órgão> (depdec) ──
_XX_DEPDEC = [
    "<item verbatim 1>",
    "<item verbatim 2>",
]
```

E no dict (mantendo as chaves existentes intactas, apenas acrescentando ao final
antes do `}`):

```python
    "depdec": _tag(_XX_DEPDEC, "cf. CBMxx, <lei/RI>, Art. N"),
```

Se um mesmo órgão tiver fontes de vários estados, encadeie com `+` como em `dpo`/`cot`.

- [ ] **Step 3: Estender `AUTO_MATCH_KEYWORDS` em `minuta_comparison_lib.py`**

Adicione ao dict (na ~linha 27), para cada um dos 3 órgãos do bloco, palavras-chave
normalizadas (minúsculas, sem acento). Valores iniciais sugeridos (ajustar conforme
os nomes reais vistos na pesquisa):

```python
    "cg":     {"include": ["comando geral", "comando-geral", "estado-maior"],
               "exclude": ["regional", "operacoes"]},
    "depdec": {"include": ["defesa civil", "protecao e defesa"], "exclude": []},
    "condeg": {"include": ["conselho"],                          "exclude": []},
```

- [ ] **Step 4: Documentar em `docs/ENRIQUECIMENTO_MINUTA.md`**

Adicione uma subseção (após a tabela "Legislações curadas (11)") com o título
`## Frente 2 — Bloco 1: Direção Geral/Colegiada (2026-06-28)`, listando em tabela as
fontes aproveitadas (Estado | Base legal | Órgão | Itens) e, em lista, os estados
avaliados e descartados com o motivo (ex.: "condeg — nenhuma LOB enumera competências
do conselho; só composição/atribuições do presidente").

- [ ] **Step 5: Regenerar os JSON**

Run:
```bash
python scripts/build_minuta_structure.py && python scripts/build_minuta_comparison.py
```
Expected: ambos rodam sem erro; a saída de `build_minuta_comparison.py` agora mostra
contagem > 0 para `cg`/`depdec`/`condeg` SE houve achados (ou segue 0 onde foi
descartado, o que é aceitável).

- [ ] **Step 6: Verificar não-regressão das chaves pré-existentes**

Run:
```bash
git diff scripts/minuta_enrichment.py scripts/minuta_comparison_lib.py | grep -E "^-" | grep -v "^---"
```
Expected: NENHUMA linha removida (saída vazia) — a mudança é puramente aditiva.
Confirme também que `ro.json` não aparece em `git status`:
```bash
git status --short database/organs_detail/ro.json database/comparativo_dpo_cot.json
```
Expected: saída vazia (arquivos intocados).

- [ ] **Step 7: Rodar a suíte JS**

Run:
```bash
node --test src/lib/minutaArticles.test.js
```
Expected: `# pass 14` (ou o total atual), `# fail 0`.

- [ ] **Step 8: Commit**

```bash
git add scripts/minuta_enrichment.py scripts/minuta_comparison_lib.py docs/ENRIQUECIMENTO_MINUTA.md database/minuta_structure.json database/comparativo_minuta.json
git commit -m "data(comparador): cura Bloco 1 (Direcao Geral/Colegiada) dos orgaos novos"
```

---

### Task 2: Bloco 2 — Direção Setorial (`dp`, `deei`, `dpof`, `dsap`, `dlog`, `cint`, `ccs`, `cinf`)

**Files:**
- Modify: `scripts/minuta_enrichment.py` (listas `_XX_*` + chaves no `ENRICHMENT_ORGAN`)
- Modify: `scripts/minuta_comparison_lib.py` (chaves no `AUTO_MATCH_KEYWORDS`)
- Modify: `docs/ENRIQUECIMENTO_MINUTA.md` (subseção do bloco)
- Regenera: `database/minuta_structure.json`, `database/comparativo_minuta.json`

- [ ] **Step 1: Pesquisa por subagente**

Dispatch um subagente com o "Prompt de pesquisa", `<LISTA DO BLOCO>` =
`dp` (Diretoria de Pessoal / Gestão de Pessoas), `deei` (Diretoria de Ensino /
Educação / Instrução), `dpof` (Diretoria de Finanças / Orçamento / Planejamento
administrativo), `dsap` (Diretoria de Saúde / Assistência), `dlog` (Diretoria de
Logística / Apoio Logístico / Material e Patrimônio), `cint` (Inteligência),
`ccs` (Comunicação Social), `cinf` (Informática / Tecnologia da Informação / TI).

Nota de domínio: estas diretorias administrativas são comuns em LOBs modernas, mas
muitas as descrevem por finalidade em uma frase (descartar). Procure especialmente
RIs e regulamentos que enumeram competências por inciso (ex.: o RI do CBMPR, CBMMT,
CBMDF já são fontes ricas para outros órgãos).

- [ ] **Step 2: Integrar competências verbatim em `minuta_enrichment.py`**

Mesmo padrão da Task 1, Step 2 — uma lista `_XX_DP`, `_XX_DEEI`, etc. por achado, e
uma chave por organ_key no dict `ENRICHMENT_ORGAN`. Exemplo de formato:

```python
# ── CBMxx, <lei/RI>, Art. N — Diretoria de Pessoal (dp) ──
_XX_DP = [
    "<item verbatim 1>",
    "<item verbatim 2>",
]
```

```python
    "dp":   _tag(_XX_DP,   "cf. CBMxx, <lei/RI>, Art. N"),
    "dlog": _tag(_XX_DLOG, "cf. CBMxx, <lei/RI>, Art. M"),
```

- [ ] **Step 3: Estender `AUTO_MATCH_KEYWORDS` em `minuta_comparison_lib.py`**

Valores iniciais sugeridos (ajustar aos nomes reais):

```python
    "dp":   {"include": ["pessoal", "gestao de pessoas", "recursos humanos"], "exclude": []},
    "deei": {"include": ["ensino", "instrucao", "educacao"],     "exclude": []},
    "dpof": {"include": ["financas", "orcamento"],
             "exclude": ["planejamento operacional"]},
    "dsap": {"include": ["saude", "assistencia ao pessoal"],     "exclude": []},
    "dlog": {"include": ["logistica", "apoio logistico", "material"], "exclude": []},
    "cint": {"include": ["inteligencia"],                        "exclude": []},
    "ccs":  {"include": ["comunicacao social"],                  "exclude": []},
    "cinf": {"include": ["informatica", "tecnologia da informacao"], "exclude": []},
```

- [ ] **Step 4: Documentar em `docs/ENRIQUECIMENTO_MINUTA.md`**

Subseção `## Frente 2 — Bloco 2: Direção Setorial (2026-06-28)`, tabela de fontes
aproveitadas + lista de descartes com motivo.

- [ ] **Step 5: Regenerar os JSON**

Run:
```bash
python scripts/build_minuta_structure.py && python scripts/build_minuta_comparison.py
```
Expected: ambos rodam sem erro; contagens > 0 onde houve achados.

- [ ] **Step 6: Verificar não-regressão**

Run:
```bash
git diff scripts/minuta_enrichment.py scripts/minuta_comparison_lib.py | grep -E "^-" | grep -v "^---"
git status --short database/organs_detail/ro.json database/comparativo_dpo_cot.json
```
Expected: ambas as saídas vazias.

- [ ] **Step 7: Rodar a suíte JS**

Run:
```bash
node --test src/lib/minutaArticles.test.js
```
Expected: `# fail 0`.

- [ ] **Step 8: Commit**

```bash
git add scripts/minuta_enrichment.py scripts/minuta_comparison_lib.py docs/ENRIQUECIMENTO_MINUTA.md database/minuta_structure.json database/comparativo_minuta.json
git commit -m "data(comparador): cura Bloco 2 (Direcao Setorial) dos orgaos novos"
```

---

### Task 3: Bloco 3 — Assessoramento/Apoio (`assessorias`, `gab-cg`, `ag`)

**Files:**
- Modify: `scripts/minuta_enrichment.py`
- Modify: `scripts/minuta_comparison_lib.py`
- Modify: `docs/ENRIQUECIMENTO_MINUTA.md`
- Regenera: `database/minuta_structure.json`, `database/comparativo_minuta.json`

- [ ] **Step 1: Pesquisa por subagente**

Dispatch com `<LISTA DO BLOCO>` = `assessorias` (Assessoria/Assessorias —
jurídica, parlamentar, técnica), `gab-cg` (Gabinete do Comandante-Geral),
`ag` (Ajudância-Geral / Ajudante-Geral / Secretaria-Geral).

Nota de domínio: estes são órgãos de apoio ao comando; raramente as LOBs os
enumeram (são citados por finalidade). Match esperado baixo; é aceitável reportar
"nenhum match" para qualquer um deles.

- [ ] **Step 2: Integrar competências verbatim em `minuta_enrichment.py`**

Mesmo padrão (Task 1, Step 2). Formato:

```python
# ── CBMxx, <lei/RI>, Art. N — <órgão> (gab-cg) ──
_XX_GABCG = [
    "<item verbatim 1>",
]
```

```python
    "gab-cg": _tag(_XX_GABCG, "cf. CBMxx, <lei/RI>, Art. N"),
```

Atenção: a chave `gab-cg` tem hífen — é uma string literal válida como chave de dict
Python (`"gab-cg"`); o nome da variável Python não pode ter hífen, por isso a lista
é `_XX_GABCG` (sem hífen).

- [ ] **Step 3: Estender `AUTO_MATCH_KEYWORDS`**

Valores iniciais sugeridos:

```python
    "assessorias": {"include": ["assessoria"],     "exclude": []},
    "gab-cg":      {"include": ["gabinete"],        "exclude": []},
    "ag":          {"include": ["ajudancia", "ajudante-geral"], "exclude": []},
```

- [ ] **Step 4: Documentar em `docs/ENRIQUECIMENTO_MINUTA.md`**

Subseção `## Frente 2 — Bloco 3: Assessoramento/Apoio (2026-06-28)`.

- [ ] **Step 5: Regenerar os JSON**

Run:
```bash
python scripts/build_minuta_structure.py && python scripts/build_minuta_comparison.py
```
Expected: rodam sem erro.

- [ ] **Step 6: Verificar não-regressão**

Run:
```bash
git diff scripts/minuta_enrichment.py scripts/minuta_comparison_lib.py | grep -E "^-" | grep -v "^---"
git status --short database/organs_detail/ro.json database/comparativo_dpo_cot.json
```
Expected: vazias.

- [ ] **Step 7: Rodar a suíte JS**

Run:
```bash
node --test src/lib/minutaArticles.test.js
```
Expected: `# fail 0`.

- [ ] **Step 8: Commit**

```bash
git add scripts/minuta_enrichment.py scripts/minuta_comparison_lib.py docs/ENRIQUECIMENTO_MINUTA.md database/minuta_structure.json database/comparativo_minuta.json
git commit -m "data(comparador): cura Bloco 3 (Assessoramento/Apoio) dos orgaos novos"
```

---

### Task 4: Bloco 4 — Correição (`corregedoria`)

**Files:**
- Modify: `scripts/minuta_enrichment.py`
- Modify: `scripts/minuta_comparison_lib.py`
- Modify: `docs/ENRIQUECIMENTO_MINUTA.md`
- Regenera: `database/minuta_structure.json`, `database/comparativo_minuta.json`

- [ ] **Step 1: Pesquisa por subagente**

Dispatch com `<LISTA DO BLOCO>` = `corregedoria` (Corregedoria / Corregedoria-Geral
/ Corregedoria do CBM). Corregedorias frequentemente têm competências enumeradas em
lei própria ou no RI — match plausível.

- [ ] **Step 2: Integrar competências verbatim em `minuta_enrichment.py`**

```python
# ── CBMxx, <lei/RI>, Art. N — Corregedoria-Geral (corregedoria) ──
_XX_CORREG = [
    "<item verbatim 1>",
]
```

```python
    "corregedoria": _tag(_XX_CORREG, "cf. CBMxx, <lei/RI>, Art. N"),
```

- [ ] **Step 3: Estender `AUTO_MATCH_KEYWORDS`**

```python
    "corregedoria": {"include": ["corregedoria", "correicao"], "exclude": []},
```

- [ ] **Step 4: Documentar em `docs/ENRIQUECIMENTO_MINUTA.md`**

Subseção `## Frente 2 — Bloco 4: Correição (2026-06-28)`.

- [ ] **Step 5: Regenerar os JSON**

Run:
```bash
python scripts/build_minuta_structure.py && python scripts/build_minuta_comparison.py
```
Expected: rodam sem erro.

- [ ] **Step 6: Verificar não-regressão**

Run:
```bash
git diff scripts/minuta_enrichment.py scripts/minuta_comparison_lib.py | grep -E "^-" | grep -v "^---"
git status --short database/organs_detail/ro.json database/comparativo_dpo_cot.json
```
Expected: vazias.

- [ ] **Step 7: Rodar a suíte JS**

Run:
```bash
node --test src/lib/minutaArticles.test.js
```
Expected: `# fail 0`.

- [ ] **Step 8: Commit**

```bash
git add scripts/minuta_enrichment.py scripts/minuta_comparison_lib.py docs/ENRIQUECIMENTO_MINUTA.md database/minuta_structure.json database/comparativo_minuta.json
git commit -m "data(comparador): cura Bloco 4 (Correicao) dos orgaos novos"
```

---

### Task 5: Verificação final e atualização de docs

**Files:**
- Modify (se necessário): `CLAUDE.md` (seção do `/comparar` — atualizar contagem de órgãos cobertos, se mudou)
- Verifica: `database/comparativo_minuta.json`, `database/minuta_structure.json`

- [ ] **Step 1: Conferir cobertura final dos 15 órgãos**

Run:
```bash
python scripts/build_minuta_comparison.py
```
Expected: a saída lista os 27 órgãos com suas contagens. Anote quantos dos 15
órgãos-alvo agora têm > 0 estados. Os que permanecerem em 0 devem ter motivo de
descarte registrado em `docs/ENRIQUECIMENTO_MINUTA.md` (verificar).

- [ ] **Step 2: Reprodutibilidade do build**

Run:
```bash
python scripts/build_minuta_structure.py && python scripts/build_minuta_comparison.py
git status --short database/minuta_structure.json database/comparativo_minuta.json
```
Expected: saída vazia (rodar de novo não muda os JSON já commitados — build
reproduzível).

- [ ] **Step 3: Confirmar invariantes globais do branch**

Run:
```bash
git diff master --stat -- database/organs_detail/ro.json database/comparativo_dpo_cot.json
```
Expected: saída vazia (nenhuma mudança nesses dois arquivos em todo o branch).

- [ ] **Step 4: Suíte JS final**

Run:
```bash
node --test src/lib/minutaArticles.test.js
```
Expected: `# fail 0`.

- [ ] **Step 5: Atualizar `CLAUDE.md` se a descrição do `/comparar` ficou desatualizada**

Localize na seção `/comparar` de `CLAUDE.md` a frase que descreve o escopo de órgãos
do comparador. Se ela citar um número de órgãos cobertos que mudou, atualize para
refletir que os 26 órgãos da LOB + Guarnição agora têm camada de dados (curada e/ou
automática), mencionando que parte permanece sem match por ausência de fonte verbatim
(documentado em `docs/ENRIQUECIMENTO_MINUTA.md`). Se a seção não cita número
específico, nenhuma edição é necessária.

- [ ] **Step 6: Commit (se houve mudança em CLAUDE.md)**

```bash
git add CLAUDE.md
git commit -m "docs: atualiza CLAUDE.md para a cobertura ampliada do comparador (Frente 2)"
```

Se nenhum arquivo mudou neste passo, pular o commit.

---

## Self-Review (executado pelo autor do plano)

**Spec coverage:**
- Objetivo (pesquisa profunda verbatim dos 15 órgãos) → Tasks 1–4.
- 4 blocos por categoria → Tasks 1 (Direção Geral/Colegiada), 2 (Direção Setorial),
  3 (Assessoramento/Apoio), 4 (Correição). ✓
- Integração aditiva em 3 arquivos → Steps 2–4 de cada task. ✓
- `ro.json`/`comparativo_dpo_cot.json` intocados → Step 6 de cada task + Task 5 Step 3. ✓
- Casos de borda (órgãos sem match) → notas de domínio em cada task + documentação de
  descarte em Step 4. ✓
- Testes/reprodutibilidade → Steps 5–7 de cada task + Task 5. ✓

**Placeholder scan:** Os `<...>` em blocos de código são marcadores explícitos para
conteúdo vindo do relatório de pesquisa (a curadoria é inerentemente dependente do
achado real — não há como pré-escrever os incisos verbatim de leis ainda não lidas).
Os valores de `AUTO_MATCH_KEYWORDS` são sugestões concretas e funcionais, ajustáveis.
Não há TODO/TBD/"implementar depois" genéricos.

**Type consistency:** `_tag(items, source)` → `[{"text", "source"}]` usado
consistentemente; chaves de dict são organ_keys exatas de `ORGAN_ORDER`
(`gab-cg` com hífen na string, `_XX_GABCG` sem hífen na variável — explicitado na
Task 3 Step 2); `include`/`exclude` batem com a assinatura de `AUTO_MATCH_KEYWORDS`.
