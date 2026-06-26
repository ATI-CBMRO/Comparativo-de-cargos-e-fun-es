# 3ª coluna "LOB do estado" no comparativo — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adicionar uma 3ª coluna "LOB do estado" ao comparativo `/comparar`, ao lado da coluna atual (renomeada "Legislação compilada"), sourced do `organs_detail` filtrado a LOB, sem alterar a coluna compilada.

**Architecture:** `build_minuta_comparison.py` ganha um conjunto paralelo `lobOrgans` por estado (casado no `organs_detail` filtrado a `source:lob`), além do `organs` compilado atual (intacto). O frontend `PairTable` passa de 3 para 4 colunas. Nenhuma camada curada é tocada.

**Tech Stack:** Python (pipeline offline), React/JSX (`MinutaComparator.jsx`), CSS único (`src/index.css`). Sem framework de testes Python; há `node --test` para JS (não afetado).

---

### Task 1: Dados — `lobOrgans` no `build_minuta_comparison.py`

**Files:**
- Modify: `scripts/minuta_comparison_lib.py` (estende `AUTO_MATCH_KEYWORDS`)
- Modify: `scripts/build_minuta_comparison.py` (helpers `lob_organs`, `attach_lob_organs`; chamada em `build()`)
- Generated: `database/comparativo_minuta.json`

- [ ] **Step 1: Estender `AUTO_MATCH_KEYWORDS` com `dpo` e `cot`**

Em `scripts/minuta_comparison_lib.py`, no dict `AUTO_MATCH_KEYWORDS`, adicionar duas entradas (logo após a linha `AUTO_MATCH_KEYWORDS = {`):

```python
AUTO_MATCH_KEYWORDS = {
    "dpo":   {"include": ["planejamento"],                     "exclude": []},
    "cot":   {"include": ["operacoes", "operacional"],
              "exclude": ["aerea", "aereo", "aviacao", "atividades tecnicas"]},
    "doe":   {"include": ["especializ"],                       "exclude": []},
```

(As demais entradas — doe, crbm, bbm, … — permanecem inalteradas; apenas dpo e cot foram acrescentados no topo.)

- [ ] **Step 2: Adicionar os helpers `lob_organs` e `attach_lob_organs`**

Em `scripts/build_minuta_comparison.py`, logo após a função `auto_states_for(...)` (antes de `def sort_states`), inserir:

```python
def lob_organs(organs):
    """Subconjunto LOB do organs_detail de um estado: se houver algum órgão com
    source=='lob' (estados com legislação mista, já tagueados), retorna só esses;
    senão retorna todos (estados de doc único de LOB, cuja curadoria já é LOB)."""
    lobbed = {oid: o for oid, o in organs.items() if o.get("source") == "lob"}
    return lobbed if lobbed else organs


def attach_lob_organs(organ_key, state_records):
    """Para cada estado já presente no comparativo, anexa:
      - lobOrgans: órgãos da LOB casados (organs_detail filtrado a LOB + auto-match);
      - lobProvenance: 'curado' se algum órgão casado tem source=='lob', senão 'automatico'.
    Não altera a coluna compilada (rec['organs'])."""
    for rec in state_records:
        sid = rec["id"]
        if sid == REF_ID:
            continue
        organs = load_organs(sid)
        lobbed = lob_organs(organs)
        ids = auto_match_organ_ids(organ_key, lobbed)
        matched = [extract_organ(lobbed, oid) for oid in ids]
        rec["lobOrgans"] = [m for m in matched if m]
        rec["lobProvenance"] = (
            "curado" if any(lobbed.get(oid, {}).get("source") == "lob" for oid in ids)
            else "automatico"
        )
```

- [ ] **Step 3: Chamar `attach_lob_organs` em `build()`**

Em `scripts/build_minuta_comparison.py`, dentro de `build()`, localizar:

```python
        states = sort_states(list(curated.values()) + list(auto.values()))
```

e inserir LOGO ABAIXO dessa linha:

```python
        attach_lob_organs(organ_key, states)
```

- [ ] **Step 4: Regenerar e verificar o JSON**

```bash
cd "c:\Users\tiago\OneDrive\Documentos\Comparativo de legislações CBM"
python scripts/build_minuta_comparison.py 2>&1 | tail -3
python -c "
import json
d = json.load(open('database/comparativo_minuta.json', encoding='utf-8'))
# todo estado em todo órgão deve ter lobOrgans (lista) e lobProvenance
bad = []
for o in d['organs']:
    for s in o['states']:
        if 'lobOrgans' not in s or 'lobProvenance' not in s:
            bad.append((o['key'], s['id']))
assert not bad, f'faltando lobOrgans: {bad[:5]}'
# estados tagueados puxam LOB: ex. MT no organo dpo deve casar algo (planejamento) ou cot
def has_lob(uf):
    n = 0
    for o in d['organs']:
        for s in o['states']:
            if s['id']==uf:
                n += len(s.get('lobOrgans',[]))
    return n
for uf in ('mt','al','se','ba'):
    print(uf, 'total lobOrgans casados:', has_lob(uf))
print('OK — todos os estados têm lobOrgans/lobProvenance')
"
```
Expected: linhas com contagens por estado (mt/al/se com >0 em vários órgãos) e `OK — …`, sem AssertionError.

- [ ] **Step 5: Commit**

```bash
git add scripts/minuta_comparison_lib.py scripts/build_minuta_comparison.py database/comparativo_minuta.json
git commit -m "feat(comparar): produz lobOrgans por estado (camada LOB) no build do comparativo"
```

---

### Task 2: Frontend — 4ª coluna no `PairTable`

**Files:**
- Modify: `src/pages/MinutaComparator.jsx` (`StateCell`, `PairTable`, texto introdutório)

- [ ] **Step 1: Refatorar `StateCell` para receber a lista de órgãos diretamente**

Em `src/pages/MinutaComparator.jsx`, substituir a função `StateCell` atual:

```jsx
/* Pilha de órgãos de um estado dentro de uma célula (alguns estados têm 2+) */
function StateCell({ state, row }) {
  if (!state || (state.organs || []).length === 0) return <span className="cc-empty">—</span>
  return (
    <>
      {state.organs.map((o, i) => (
        <div key={i} style={i > 0 ? { marginTop: 8, paddingTop: 8, borderTop: '1px dashed var(--border-subtle)' } : undefined}>
          {row.render(o)}
        </div>
      ))}
      {row.key === 'organ' && state.note && (
        <div style={{ marginTop: 6, fontSize: 10.5, color: 'var(--text-muted)', fontStyle: 'italic' }}>{state.note}</div>
      )}
    </>
  )
}
```

por (agora recebe `organs` e `note` diretamente, para servir às duas colunas do estado):

```jsx
/* Pilha de órgãos de um estado dentro de uma célula (alguns estados têm 2+).
   Recebe a lista de órgãos diretamente (serve à coluna LOB e à coluna compilada). */
function StateCell({ organs, note, row }) {
  if (!organs || organs.length === 0) return <span className="cc-empty">—</span>
  return (
    <>
      {organs.map((o, i) => (
        <div key={i} style={i > 0 ? { marginTop: 8, paddingTop: 8, borderTop: '1px dashed var(--border-subtle)' } : undefined}>
          {row.render(o)}
        </div>
      ))}
      {row.key === 'organ' && note && (
        <div style={{ marginTop: 6, fontSize: 10.5, color: 'var(--text-muted)', fontStyle: 'italic' }}>{note}</div>
      )}
    </>
  )
}
```

- [ ] **Step 2: Adicionar o helper de cabeçalho de coluna do estado**

Em `src/pages/MinutaComparator.jsx`, logo ANTES da função `PairTable`, inserir:

```jsx
/* Cabeçalho de uma das duas colunas do estado (LOB ou Compilada). */
function StateColHead({ state, kind }) {
  if (!state) return <span className="cc-empty">Selecione um estado</span>
  const isLob = kind === 'lob'
  const provenance = isLob ? state.lobProvenance : state.provenance
  return (
    <div className="cc-corp-head">
      <span className="cc-corp-abbr">{state.abbr}</span>
      <div>
        <div className="cc-corp-name">{state.name}</div>
        <div className="cc-corp-cbm" style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
          <span className="oc-col-kind">{isLob ? 'LOB' : 'Compilada'}</span>
          {provenance && <ProvBadge provenance={provenance} />}
        </div>
      </div>
    </div>
  )
}
```

- [ ] **Step 3: Reescrever `PairTable` para 4 colunas**

Em `src/pages/MinutaComparator.jsx`, substituir TODA a função `PairTable` (de `function PairTable({ organ, state }) {` até o seu `}` de fechamento) por:

```jsx
/* Tabela: Campo | CBMRO | LOB do estado | Legislação compilada */
function PairTable({ organ, state }) {
  const refOrgans = organ.reference ? [organ.reference] : []
  return (
    <div className="oc-pair-wrapper" style={{ border: '1px solid var(--border-card)', borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
      <table className="oc-pair-table oc-pair-table-3">
        <colgroup>
          <col className="oc-pair-col-label" />
          <col className="oc-pair-col-ro" />
          <col className="oc-pair-col-lob" />
          <col className="oc-pair-col-st" />
        </colgroup>
        <thead>
          <tr>
            <th className="oc-pair-th-label">Campo</th>
            <th className="oc-pair-th-ro">
              <div className="cc-corp-head">
                <span className="cc-corp-abbr ref">RO</span>
                <div>
                  <div className="cc-corp-name">Rondônia</div>
                  <div className="cc-corp-cbm">CBMRO · Referência (LOB)</div>
                </div>
              </div>
            </th>
            <th className="oc-pair-th-lob"><StateColHead state={state} kind="lob" /></th>
            <th className="oc-pair-th-st"><StateColHead state={state} kind="comp" /></th>
          </tr>
        </thead>
        <tbody>
          {MATRIX_ROWS.map((row, rowIdx) => (
            <tr key={row.key}>
              <td className="oc-pair-td-label">{row.label}</td>
              {refOrgans.length === 0
                ? (rowIdx === 0
                    ? <td className="oc-pair-td-ro" rowSpan={MATRIX_ROWS.length} style={{ verticalAlign: 'top' }}>
                        <span style={{ display: 'flex', gap: 5, alignItems: 'flex-start', fontStyle: 'italic', color: 'var(--text-muted)' }}>
                          <AlertCircle size={13} style={{ flexShrink: 0, marginTop: 2 }} />
                          {organ.referenceNote || 'O CBMRO não discrimina este órgão.'}
                        </span>
                      </td>
                    : null)
                : <td className="oc-pair-td-ro">{row.render(refOrgans[0])}</td>
              }
              <td className="oc-pair-td-lob"><StateCell organs={state?.lobOrgans} row={row} /></td>
              <td className="oc-pair-td-st"><StateCell organs={state?.organs} note={state?.note} row={row} /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

- [ ] **Step 4: Atualizar o texto introdutório da página**

Em `src/pages/MinutaComparator.jsx`, localizar o parágrafo introdutório dentro do primeiro `card no-print` (começa com `Compare a legislação do`). Substituir o seu conteúdo por:

```jsx
            Compare, órgão a órgão, a minuta da <strong>LOB do CBMRO</strong> com o estado
            selecionado em <strong>duas visões lado a lado</strong>: a <strong>LOB do estado</strong>
            (só a Lei de Organização Básica) e a <strong>legislação compilada</strong> (todas as
            fontes curadas — LOB, Regimento, NGA etc.). Escolha o órgão à esquerda e clique na
            <strong> sigla de um estado</strong> para trocar a comparação. Colunas marcadas
            <strong> Curado</strong> trazem texto verbatim atribuído à fonte; <strong>Auto</strong>
            vêm de extração automática e podem ser rasas.
```

- [ ] **Step 5: Verificar build do frontend (sem erro de sintaxe)**

```bash
cd "c:\Users\tiago\OneDrive\Documentos\Comparativo de legislações CBM"
npx vite build 2>&1 | tail -5
```
Expected: `✓ built in …` sem erros de transform/sintaxe. (Se preferir não buildar, basta garantir que o dev server em :5173 recompila sem erro no console.)

- [ ] **Step 6: Commit**

```bash
git add src/pages/MinutaComparator.jsx
git commit -m "feat(comparar): PairTable com 3 colunas (RO · LOB do estado · compilada)"
```

---

### Task 3: Estilo — 4 colunas no `src/index.css`

**Files:**
- Modify: `src/index.css` (larguras do `colgroup`, coluna LOB, min-width, print, mobile)

- [ ] **Step 1: Larguras das colunas (modo 3-conteúdo) e estilo da coluna LOB**

Em `src/index.css`, localizar o bloco de larguras:

```css
.oc-pair-col-label { width: 170px; }
.oc-pair-col-ro    { width: calc((100% - 170px) / 2); }
.oc-pair-col-st    { width: calc((100% - 170px) / 2); }
```

e substituir por:

```css
.oc-pair-col-label { width: 170px; }
.oc-pair-col-ro    { width: calc((100% - 170px) / 2); }
.oc-pair-col-st    { width: calc((100% - 170px) / 2); }
/* Modo 3 colunas de conteúdo (RO · LOB · compilada): divide o restante em 3 */
.oc-pair-table-3 { min-width: 880px; }
.oc-pair-table-3 .oc-pair-col-ro,
.oc-pair-table-3 .oc-pair-col-lob,
.oc-pair-table-3 .oc-pair-col-st { width: calc((100% - 170px) / 3); }
```

- [ ] **Step 2: Cabeçalho e célula da coluna LOB + rótulo de tipo**

Em `src/index.css`, logo após o bloco `.oc-pair-th-st { … }`, inserir:

```css
.oc-pair-th-lob {
  background: #eef4ec; border-left: 2px solid var(--accent-green, #16a34a);
}
```

e logo após o bloco `.oc-pair-td-st { … }`, inserir:

```css
.oc-pair-td-lob {
  background: #f7fbf6 !important;
  border-left: 2px solid rgba(22,163,74,0.25);
}
.oc-col-kind {
  font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em;
  color: var(--text-muted); border: 1px solid var(--border-card); border-radius: 4px;
  padding: 0 5px;
}
```

- [ ] **Step 3: Impressão (4 colunas em Paisagem)**

Em `src/index.css`, localizar no bloco `@media print`:

```css
  .oc-pair-table { font-size: 9pt; }
  .oc-pair-table td, .oc-pair-table th { padding: 8px 10px; }
```

e substituir por:

```css
  .oc-pair-table { font-size: 9pt; }
  .oc-pair-table-3 { font-size: 8pt; }
  .oc-pair-table td, .oc-pair-table th { padding: 8px 10px; }
  .oc-pair-table-3 td, .oc-pair-table-3 th { padding: 6px 7px; }
```

- [ ] **Step 4: Mobile (≤900px) — coluna LOB acompanha o scroll**

Em `src/index.css`, localizar no bloco `@media (max-width: 900px)`:

```css
  .oc-pair-table { min-width: 520px; }
  .oc-pair-col-label { width: 116px; }
  .oc-pair-col-ro,
  .oc-pair-col-st { width: calc((100% - 116px) / 2); }
```

e substituir por:

```css
  .oc-pair-table { min-width: 520px; }
  .oc-pair-table-3 { min-width: 760px; }
  .oc-pair-col-label { width: 116px; }
  .oc-pair-col-ro,
  .oc-pair-col-st { width: calc((100% - 116px) / 2); }
  .oc-pair-table-3 .oc-pair-col-ro,
  .oc-pair-table-3 .oc-pair-col-lob,
  .oc-pair-table-3 .oc-pair-col-st { width: calc((100% - 116px) / 3); }
```

- [ ] **Step 5: Commit**

```bash
git add src/index.css
git commit -m "style(comparar): larguras e estilo da 3ª coluna LOB (incl. print/mobile)"
```

---

### Task 4: Verificação visual e fechamento

**Files:** nenhum (verificação); o `comparativo_minuta.json` já foi commitado na Task 1.

- [ ] **Step 1: Garantir dev server em :5173**

```bash
cd "c:\Users\tiago\OneDrive\Documentos\Comparativo de legislações CBM"
(netstat -ano | grep -E ":5173\b" >/dev/null && echo UP) || (npm run dev -- --port 5173 --strictPort >/tmp/dev.log 2>&1 & sleep 4; echo STARTED)
```

- [ ] **Step 2: Conferência visual (Playwright headless) — 3 colunas, estados misto e puro**

Criar `scratchpad/check_3col.js` (na pasta de scratchpad da sessão) com um script Playwright que: abre `http://localhost:5173/comparar`, espera `.oc-pair-table-3`, seleciona o chip `MT` (estado misto) e tira screenshot; seleciona `BA` (estado puro) e tira screenshot; coleta erros de console. Rodar com `node` (instalar `playwright@1.48.0` no scratchpad se necessário — chromium já está baixado). Conferir nos screenshots:
  - 4 colunas visíveis: Campo · CBMRO · LOB do estado · Legislação compilada.
  - MT: coluna LOB mostra órgãos `source:lob` (ex.: Diretoria Operacional/DOp); compilada mostra a curadoria atual; ambas distintas.
  - BA: LOB ≈ compilada (estado puro).
  - Órgão sem casamento LOB mostra "—" na coluna LOB sem quebrar a compilada.
  - `console --errors` vazio.

Expected: screenshots confirmam as 4 colunas e nenhum erro de console.

- [ ] **Step 3: Limpeza dos artefatos de verificação**

Remover `scratchpad/check_3col.js`, screenshots e `node_modules` de teste do scratchpad.

- [ ] **Step 4: Rodar a suíte JS (não deve quebrar)**

```bash
cd "c:\Users\tiago\OneDrive\Documentos\Comparativo de legislações CBM"
node --test 2>&1 | grep -E "tests |pass |fail "
```
Expected: `pass 14 / fail 0`.

---

## Self-Review (preenchido na escrita do plano)

**Cobertura do spec:**
- `states[].lobOrgans` + `lobProvenance`, coluna compilada intacta → Task 1. ✓
- `lob_organs()` filtro (source:lob senão tudo) → Task 1 Step 2. ✓
- Estender `AUTO_MATCH_KEYWORDS` com dpo/cot → Task 1 Step 1. ✓
- 4 colunas no `PairTable`, `StateCell` servindo às duas colunas, cabeçalho LOB/Compilada com ProvBadge → Task 2. ✓
- Texto introdutório de 3 vias → Task 2 Step 4. ✓
- CSS larguras /3, coluna LOB, min-width, print, mobile → Task 3. ✓
- Verificação (json + visual misto/puro + "—" + console + node test) → Tasks 1 Step 4, 4. ✓
- Fora de escopo (curado/enrichment/Guarnição, RO, chips, sidebar) → nenhuma task os toca. ✓

**Placeholder scan:** sem "TBD"/"depois"; todo passo de código mostra o código real. A Task 4 Step 2 descreve o script Playwright em prosa (não código literal) por ser verificação visual ad-hoc no scratchpad — segue o mesmo padrão já usado nos sub-projetos anteriores.

**Consistência de tipos/nomes:** `lobOrgans`/`lobProvenance` usados igualmente em Task 1 (geração) e Task 2 (consumo: `state.lobOrgans`, `state.lobProvenance`). `StateCell` recebe `{organs, note, row}` em todas as chamadas. Classe `.oc-pair-table-3` e `.oc-pair-col-lob`/`.oc-pair-th-lob`/`.oc-pair-td-lob`/`.oc-col-kind` consistentes entre Task 2 (JSX) e Task 3 (CSS).
