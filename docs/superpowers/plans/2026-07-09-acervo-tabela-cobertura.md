# Tabela de Cobertura do Acervo Legal — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adicionar uma tabela-resumo (27 estados × colunas LOB / Regimento Interno / Regulamento de Serviço) no topo da página Acervo Legal, com selo de verificação por célula, sem tocar na lista detalhada atual.

**Architecture:** Lógica pura de agregação isolada em `src/lib/acervoCoverage.js` (testável com node --test), componente de apresentação puro em `src/components/AcervoCoverageTable.jsx` (recebe tudo por props), e integração mínima em `src/pages/Legislations.jsx` que injeta os dados e a navegação. CSS novo em `src/index.css` sob prefixo `.acervo-cov-*`.

**Tech Stack:** React 18 (function components + hooks), Vite, `node --test` (test runner nativo do Node, sem framework externo), lucide-react (ícones).

## Global Constraints

- **Fonte de dados:** `database/states_data.json`, carregado via `fetchJson` de `src/lib/dataCache.js`. Cada estado tem `id`, `name`, `abbreviation`, e `documents[]` com `{ type, typeVerified, has_pdf, ... }`.
- **Coluna "Regulamento de Serviço"** funde dois `type` reais: `'Regulamento Geral'` e `'Regimento de Serviços'`. Rótulo exibido: exatamente `Regulamento de Serviço`.
- **Coluna LOB** (`type === 'Lei de Organização Básica'`) mostra apenas presença — **nunca** selo ✓/⚠ (coerência com a lista atual, onde LOB não tem selo).
- **Selo ✓/⚠** só nas colunas Regimento Interno e Regulamento de Serviço: `✓` verde (`var(--success-text)`) quando TODOS os documentos daquele tipo têm `typeVerified === true`; `⚠` (`var(--text-muted)`) quando ALGUM tem `typeVerified` falso/ausente.
- **Célula ausente:** travessão `—` na cor `var(--text-muted)`.
- **Múltiplos documentos do mesmo tipo:** um selo + sufixo `+N` (N = total de documentos daquele tipo naquele estado).
- **Clique em célula preenchida OU no nome do estado:** navega para `/estados/:id`.
- **A tabela mostra sempre os 27 estados** e NÃO é filtrada pela busca de texto da página (a busca continua governando só a lista detalhada abaixo).
- **Sem cores hardcoded novas** — reutilizar variáveis CSS existentes (`--success-text`, `--text-muted`, `--border-card`, `--bg-surface`, `--text-primary`, `--radius-md`).
- **Test runner:** `npm test` roda `node --test "src/lib/**/*.test.js" "api/**/*.test.js"`. Testes de lib usam `import { test } from 'node:test'` e `import assert from 'node:assert/strict'`.
- **Documentos fora das 3 colunas** (NGA, QDC, QOD) ficam de fora da tabela; continuam só na lista detalhada.

---

### Task 1: Lógica pura de agregação (`acervoCoverage.js`)

Cria a função que transforma `data.states` em linhas prontas para a tabela. Todo o raciocínio (fusão de tipos, regra do selo, contagem, ordenação) mora aqui e é testado isoladamente, sem React.

**Files:**
- Create: `src/lib/acervoCoverage.js`
- Test: `src/lib/acervoCoverage.test.js`

**Interfaces:**
- Consumes: array `states` no formato de `database/states_data.json` (`{ id, name, abbreviation, documents: [{ type, typeVerified }] }`).
- Produces:
  - `export const REGULAMENTO_SERVICO_TYPES = ['Regulamento Geral', 'Regimento de Serviços']`
  - `export function buildCoverageRows(states) => Array<Row>` onde
    `Row = { stateId: string, stateName: string, abbreviation: string, columns: { lob: Cell, regimento: Cell, regulamento: Cell } }`
    e `Cell = { count: number, present: boolean, verified: boolean | null }`.
    Regra de `verified`: `null` para a coluna `lob` sempre, e `null` quando `present === false`; caso contrário `true` se todos os docs daquele tipo têm `typeVerified === true`, senão `false`. Linhas ordenadas por `stateName` com `localeCompare(…, 'pt-BR')`.

- [ ] **Step 1: Write the failing test**

Criar `src/lib/acervoCoverage.test.js`:

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { buildCoverageRows, REGULAMENTO_SERVICO_TYPES } from './acervoCoverage.js'

const doc = (type, typeVerified) => ({ type, typeVerified })

const STATES = [
  {
    id: 'se', name: 'Sergipe', abbreviation: 'SE',
    documents: [
      doc('Lei de Organização Básica', undefined),
      doc('Lei de Organização Básica', undefined),
      doc('Regimento de Serviços', true),
    ],
  },
  {
    id: 'al', name: 'Alagoas', abbreviation: 'AL',
    documents: [
      doc('Lei de Organização Básica', undefined),
      doc('Regimento Interno', false),
    ],
  },
  {
    id: 'mt', name: 'Mato Grosso', abbreviation: 'MT',
    documents: [
      doc('Lei de Organização Básica', undefined),
      doc('Regulamento Geral', true),
    ],
  },
  {
    id: 'ro', name: 'Rondônia', abbreviation: 'RO',
    documents: [doc('Lei de Organização Básica', undefined)],
  },
]

test('funde Regulamento Geral e Regimento de Serviços na coluna regulamento', () => {
  assert.deepEqual(REGULAMENTO_SERVICO_TYPES, ['Regulamento Geral', 'Regimento de Serviços'])
  const rows = buildCoverageRows(STATES)
  const mt = rows.find(r => r.stateId === 'mt')
  const se = rows.find(r => r.stateId === 'se')
  assert.equal(mt.columns.regulamento.present, true)   // Regulamento Geral
  assert.equal(se.columns.regulamento.present, true)   // Regimento de Serviços
})

test('LOB conta múltiplos documentos e nunca tem selo (verified null)', () => {
  const se = buildCoverageRows(STATES).find(r => r.stateId === 'se')
  assert.equal(se.columns.lob.count, 2)
  assert.equal(se.columns.lob.present, true)
  assert.equal(se.columns.lob.verified, null)
})

test('coluna ausente: present false e verified null', () => {
  const ro = buildCoverageRows(STATES).find(r => r.stateId === 'ro')
  assert.equal(ro.columns.regimento.present, false)
  assert.equal(ro.columns.regimento.count, 0)
  assert.equal(ro.columns.regimento.verified, null)
})

test('regulamento todo verificado => verified true', () => {
  const mt = buildCoverageRows(STATES).find(r => r.stateId === 'mt')
  assert.equal(mt.columns.regulamento.verified, true)
})

test('documento com typeVerified falso => verified false', () => {
  const al = buildCoverageRows(STATES).find(r => r.stateId === 'al')
  assert.equal(al.columns.regimento.present, true)
  assert.equal(al.columns.regimento.verified, false)
})

test('linhas ordenadas por nome (pt-BR)', () => {
  const names = buildCoverageRows(STATES).map(r => r.stateName)
  assert.deepEqual(names, ['Alagoas', 'Mato Grosso', 'Rondônia', 'Sergipe'])
})

test('states nulo/vazio não quebra', () => {
  assert.deepEqual(buildCoverageRows(undefined), [])
  assert.deepEqual(buildCoverageRows([]), [])
})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npx node --test src/lib/acervoCoverage.test.js`
Expected: FAIL — `Cannot find module './acervoCoverage.js'` (arquivo ainda não existe).

- [ ] **Step 3: Write minimal implementation**

Criar `src/lib/acervoCoverage.js`:

```js
// Lógica pura do Acervo Legal: agrega os documentos de cada estado nas 3
// colunas da tabela de cobertura (LOB / Regimento Interno / Regulamento de
// Serviço). Sem React. A coluna "Regulamento de Serviço" funde dois tipos
// reais do acervo (Regulamento Geral e Regimento de Serviços).

export const REGULAMENTO_SERVICO_TYPES = ['Regulamento Geral', 'Regimento de Serviços']

const LOB_TYPE = 'Lei de Organização Básica'
const REGIMENTO_TYPE = 'Regimento Interno'

// Monta uma célula a partir dos documentos de um tipo. `withSeal` = false para a
// LOB (nunca exibe selo), então verified fica sempre null.
function buildCell(docs, withSeal) {
  const present = docs.length > 0
  let verified = null
  if (present && withSeal) {
    verified = docs.every(d => d.typeVerified === true)
  }
  return { count: docs.length, present, verified }
}

// data.states -> uma linha por estado, ordenada por nome (pt-BR).
export function buildCoverageRows(states) {
  if (!Array.isArray(states)) return []
  const rows = states.map(s => {
    const docs = s.documents || []
    const lobDocs = docs.filter(d => d.type === LOB_TYPE)
    const riDocs = docs.filter(d => d.type === REGIMENTO_TYPE)
    const regDocs = docs.filter(d => REGULAMENTO_SERVICO_TYPES.includes(d.type))
    return {
      stateId: s.id,
      stateName: s.name,
      abbreviation: s.abbreviation,
      columns: {
        lob: buildCell(lobDocs, false),
        regimento: buildCell(riDocs, true),
        regulamento: buildCell(regDocs, true),
      },
    }
  })
  return rows.sort((a, b) => a.stateName.localeCompare(b.stateName, 'pt-BR'))
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npx node --test src/lib/acervoCoverage.test.js`
Expected: PASS — `# pass 7`, `# fail 0`.

- [ ] **Step 5: Confirm full suite still green**

Run: `npm test`
Expected: todos passam (89 anteriores + 7 novos = 96), `# fail 0`.

- [ ] **Step 6: Commit**

```bash
git add src/lib/acervoCoverage.js src/lib/acervoCoverage.test.js
git commit -m "feat(acervo): lógica pura de cobertura estado × tipo de documento"
```

---

### Task 2: Componente de apresentação (`AcervoCoverageTable.jsx`)

Componente puro que renderiza a tabela a partir das linhas já prontas. Não busca dados, não conhece rotas — recebe `rows` e `onSelectState` por props.

**Files:**
- Create: `src/components/AcervoCoverageTable.jsx`

**Interfaces:**
- Consumes: `buildCoverageRows` de `src/lib/acervoCoverage.js` (via o container na Task 3; o componente em si recebe o resultado por prop).
- Produces: `export default function AcervoCoverageTable({ rows, onSelectState })`. `rows` = saída de `buildCoverageRows`. `onSelectState` = `(stateId: string) => void`, chamado ao clicar no nome do estado ou numa célula preenchida.

- [ ] **Step 1: Write the component**

Criar `src/components/AcervoCoverageTable.jsx`:

```jsx
// Tabela-resumo do Acervo: uma linha por estado, colunas LOB / Regimento
// Interno / Regulamento de Serviço. Componente puro — recebe as linhas já
// agregadas (buildCoverageRows) e um callback de navegação. Ver design
// docs/superpowers/specs/2026-07-09-acervo-tabela-cobertura-design.md.

const COLUMNS = [
  { key: 'lob', label: 'LOB', seal: false },
  { key: 'regimento', label: 'Regimento Interno', seal: true },
  { key: 'regulamento', label: 'Regulamento de Serviço', seal: true },
]

// Conteúdo de uma célula de tipo. Ausente => travessão. Presente => selo
// (✓/⚠ só nas colunas com seal) + sufixo +N quando há mais de um documento.
function CellContent({ cell, seal }) {
  if (!cell.present) {
    return <span className="acervo-cov-dash" aria-label="não possui">—</span>
  }
  const suffix = cell.count > 1 ? <span className="acervo-cov-count">+{cell.count}</span> : null
  if (!seal) {
    // Coluna LOB: só presença.
    return <span className="acervo-cov-has">possui{suffix}</span>
  }
  const ok = cell.verified === true
  return (
    <span
      className={`acervo-cov-seal ${ok ? 'is-ok' : 'is-warn'}`}
      title={ok
        ? 'Tipo conferido lendo o conteúdo do documento, não só o nome do arquivo.'
        : 'Tipo ainda não conferido por conteúdo — classificação só pelo nome do arquivo, pode estar incorreta.'}
    >
      {ok ? '✓' : '⚠'}{suffix}
    </span>
  )
}

export default function AcervoCoverageTable({ rows, onSelectState }) {
  if (!rows || rows.length === 0) return null
  return (
    <section className="acervo-cov">
      <div className="acervo-cov-title">Cobertura por estado</div>
      <div className="acervo-cov-wrap">
        <table className="acervo-cov-table">
          <thead>
            <tr>
              <th scope="col">Estado</th>
              {COLUMNS.map(c => <th key={c.key} scope="col">{c.label}</th>)}
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
              <tr key={r.stateId}>
                <th scope="row">
                  <button
                    type="button"
                    className="acervo-cov-state"
                    onClick={() => onSelectState(r.stateId)}
                    title={`Abrir a página de ${r.stateName}`}
                  >
                    <span className="acervo-cov-abbr">{r.abbreviation}</span>
                    <span className="acervo-cov-name">{r.stateName}</span>
                  </button>
                </th>
                {COLUMNS.map(c => {
                  const cell = r.columns[c.key]
                  return (
                    <td key={c.key} className="acervo-cov-cell">
                      {cell.present ? (
                        <button
                          type="button"
                          className="acervo-cov-cellbtn"
                          onClick={() => onSelectState(r.stateId)}
                          title={`Abrir a página de ${r.stateName}`}
                        >
                          <CellContent cell={cell} seal={c.seal} />
                        </button>
                      ) : (
                        <CellContent cell={cell} seal={c.seal} />
                      )}
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="acervo-cov-legend">
        <span className="acervo-cov-seal is-ok">✓</span> tipo conferido por conteúdo ·{' '}
        <span className="acervo-cov-seal is-warn">⚠</span> só por nome de arquivo ·{' '}
        <span className="acervo-cov-dash">—</span> não possui
      </p>
    </section>
  )
}
```

- [ ] **Step 2: Verify it builds (no test yet — presentational)**

Run: `npm run build`
Expected: build de produção limpo, sem erro de import/JSX. (O componente ainda não é usado por nenhuma rota; só garantimos que compila.)

- [ ] **Step 3: Commit**

```bash
git add src/components/AcervoCoverageTable.jsx
git commit -m "feat(acervo): componente de apresentação da tabela de cobertura"
```

---

### Task 3: Integração na página + CSS

Liga o componente à página Acervo Legal (injeta dados e navegação) e adiciona o CSS. Depois desta task a tabela aparece de verdade no topo da página.

**Files:**
- Modify: `src/pages/Legislations.jsx`
- Modify: `src/index.css`

**Interfaces:**
- Consumes: `buildCoverageRows` de `src/lib/acervoCoverage.js`; `AcervoCoverageTable` (default) de `src/components/AcervoCoverageTable.jsx`.
- Produces: nada consumido por outras tasks (é a folha da árvore).

- [ ] **Step 1: Import the new modules in Legislations.jsx**

Em `src/pages/Legislations.jsx`, logo abaixo da linha `import { fetchJson } from '../lib/dataCache.js'`, adicionar:

```jsx
import { buildCoverageRows } from '../lib/acervoCoverage.js'
import AcervoCoverageTable from '../components/AcervoCoverageTable.jsx'
```

- [ ] **Step 2: Compute the rows with useMemo**

Em `src/pages/Legislations.jsx`, logo após o bloco `const allDocs = useMemo(...)` (que termina em `}, [data])`), adicionar:

```jsx
  // Linhas da tabela de cobertura (sempre os 27 estados; NÃO é filtrada pela
  // busca — ver design). Independente de `allDocs`/`filtered`.
  const coverageRows = useMemo(() => buildCoverageRows(data?.states), [data])
```

- [ ] **Step 3: Render the table at the top of page-body**

Em `src/pages/Legislations.jsx`, dentro de `<div className="page-body">`, ANTES do `{/* Busca */}` (a `<div className="search-input-wrap" ...>`), inserir:

```jsx
        <AcervoCoverageTable
          rows={coverageRows}
          onSelectState={id => navigate(`/estados/${id}`)}
        />

```

- [ ] **Step 4: Add the CSS block**

No fim de `src/index.css`, adicionar:

```css
/* ===== Tabela de cobertura do Acervo (estado × tipo de documento) ===== */
.acervo-cov { margin-bottom: 28px; }
.acervo-cov-title {
  font-size: 12px; font-weight: 700; letter-spacing: 0.04em;
  text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px;
}
.acervo-cov-wrap { overflow-x: auto; border: 1px solid var(--border-card); border-radius: var(--radius-md); }
.acervo-cov-table { border-collapse: collapse; width: 100%; min-width: 560px; background: var(--bg-surface); }
.acervo-cov-table th, .acervo-cov-table td {
  border-bottom: 1px solid var(--border-card); padding: 8px 12px; text-align: left; font-size: 13px;
}
.acervo-cov-table thead th {
  font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.03em;
  color: var(--text-muted); background: var(--bg-surface); position: sticky; top: 0;
}
.acervo-cov-table tbody tr:last-child th,
.acervo-cov-table tbody tr:last-child td { border-bottom: none; }
.acervo-cov-state {
  display: flex; align-items: baseline; gap: 8px; background: none; border: none;
  cursor: pointer; padding: 0; text-align: left; color: var(--text-primary); width: 100%;
}
.acervo-cov-state:hover .acervo-cov-name { text-decoration: underline; }
.acervo-cov-abbr { font-weight: 700; font-size: 12px; color: var(--text-muted); min-width: 26px; }
.acervo-cov-name { font-weight: 600; }
.acervo-cov-cell { text-align: center; }
.acervo-cov-cellbtn { background: none; border: none; cursor: pointer; padding: 2px 6px; font: inherit; }
.acervo-cov-dash { color: var(--text-muted); }
.acervo-cov-has { font-size: 12px; color: var(--text-primary); }
.acervo-cov-count { font-size: 10px; color: var(--text-muted); margin-left: 2px; vertical-align: super; }
.acervo-cov-seal { font-size: 14px; font-weight: 700; }
.acervo-cov-seal.is-ok { color: var(--success-text); }
.acervo-cov-seal.is-warn { color: var(--text-muted); }
.acervo-cov-legend { font-size: 11px; color: var(--text-muted); margin-top: 8px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
```

- [ ] **Step 5: Verify build is clean**

Run: `npm run build`
Expected: build de produção limpo, sem erros.

- [ ] **Step 6: Verify the full test suite still passes**

Run: `npm test`
Expected: `# fail 0` (nada quebrou; a integração não tem teste unitário — é verificada visualmente no Step 7).

- [ ] **Step 7: Visual verification (manual, via preview local)**

Subir o dev server (`npm run dev`, porta 5173), logar, navegar até **Acervo Legal**, e confirmar:
- A tabela "Cobertura por estado" aparece no TOPO, acima da busca.
- 27 linhas (uma por estado), ordem alfabética.
- Coluna LOB: todas mostram "possui"; SE/AC/CE/PE/PI/SP mostram "possui +2".
- Coluna Regimento Interno: selo só em AL, DF, PR, PA, RS; resto travessão "—".
- Coluna Regulamento de Serviço: selo só em GO, MT, RN, SE; resto travessão "—".
- Selo é ✓ verde quando conferido por conteúdo, ⚠ cinza quando só por nome.
- Clicar no nome de um estado OU numa célula preenchida abre `/estados/:id`.
- A lista detalhada continua embaixo, com a busca funcionando só nela.
- Reduzir a largura da janela (viewport mobile ~375px): a tabela desliza horizontalmente, o resto da página não estoura.

- [ ] **Step 8: Commit**

```bash
git add src/pages/Legislations.jsx src/index.css
git commit -m "feat(acervo): tabela de cobertura no topo da página Acervo Legal"
```

---

### Task 4: Documentação (CLAUDE.md)

Registrar a nova tela para futuras sessões/colegas.

**Files:**
- Modify: `CLAUDE.md`

**Interfaces:** nenhuma (só docs).

- [ ] **Step 1: Add a short section to CLAUDE.md**

Em `CLAUDE.md`, adicionar um parágrafo curto na seção que descreve as páginas/telas do portal (ou criar uma linha na descrição do Acervo Legal), com este conteúdo:

```markdown
### Tabela de cobertura no Acervo Legal (jul/2026)
A página Acervo Legal (`src/pages/Legislations.jsx`) mostra, no topo, uma
tabela-resumo `estado × tipo` (LOB / Regimento Interno / Regulamento de
Serviço) — lógica pura em `src/lib/acervoCoverage.js` (testada), apresentação
em `src/components/AcervoCoverageTable.jsx`. A coluna "Regulamento de Serviço"
funde os tipos `Regulamento Geral` e `Regimento de Serviços`. O selo ✓/⚠ por
célula reusa o campo `typeVerified` dos dados (✓ = conferido por conteúdo, ⚠ =
só por nome de arquivo). A tabela NÃO é filtrada pela busca da página (é
panorama fixo dos 27); a busca continua governando só a lista detalhada abaixo.
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: registra a tabela de cobertura do Acervo Legal"
```

---

## Verificação fim a fim (após todas as tasks)

1. `npm test` → `# fail 0` (96 testes: 89 antigos + 7 novos de acervoCoverage).
2. `npm run build` → limpo.
3. Preview local: Acervo Legal com a tabela no topo, 27 linhas, selos corretos (AL/DF/PR/PA/RS no Regimento Interno; GO/MT/RN/SE no Regulamento de Serviço), "+2" nas 6 LOBs duplicadas, navegação por clique, lista detalhada intacta abaixo, rolagem horizontal no mobile.
4. Nenhum hex novo hardcoded: `grep -n "#[0-9a-fA-F]\{3,6\}" src/components/AcervoCoverageTable.jsx` → vazio.
