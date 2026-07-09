# Comparativo de RI — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Adicionar uma página nova `/minuta/comparativo-ri` que compara, capítulo a capítulo, a minuta de RI do CBMRO com as competências do órgão equivalente nos Regimentos Internos de 9 estados.

**Architecture:** Uma página React de leitura, em 3 colunas (ChapterRail reusado · minuta CBMRO · estado-RI selecionado). Toda a lógica de indexação/seleção fica num módulo puro `src/lib/riComparison.js` testado com `node --test`; a página só orquestra fetch + render. Dados vêm de `minuta_structure.json` (via `buildTargets`) e `comparativo_minuta.json` já existentes — sem novo pipeline Python.

**Tech Stack:** React 18 + Vite, react-router-dom, lucide-react, `node:test`.

## Global Constraints

- Somente leitura: nenhuma edição, sugestão ou persistência.
- Sem novo script Python; sem regeneração de dados.
- Estados-RI (ordem fixa): `al, am, df, go, mt, pr, pa, rs, se`.
- Testes de lógica pura com `node --test` (padrão do projeto); componentes React não têm suíte de teste — verificam-se por `npm run build` + inspeção manual.
- Servidor de dev na porta 5173 (`npm run dev`).

---

### Task 1: Módulo puro `riComparison.js`

**Files:**
- Create: `src/lib/riComparison.js`
- Test: `src/lib/riComparison.test.js`

**Interfaces:**
- Consumes: nada de tarefas anteriores. Consome o formato de `comparativo_minuta.json`: `{ organs: [{ key, title, abbr, states: [{ id, name, abbr, provenance, sourceLabel, organs: [{ name, abbreviation, atribuicoes: [] }] }] }] }`, e `chapterId` no formato `"organ:<key>"` / `"estrutura"` / `"preliminares"` / `"finais"`.
- Produces:
  - `RI_STATE_IDS: string[]` — `['al','am','df','go','mt','pr','pa','rs','se']`
  - `indexComparativo(comparativo) -> { [key: string]: organEntry }`
  - `organKeyOfChapter(chapterId) -> string | null`
  - `stateHasData(stateEntry) -> boolean`
  - `statesWithData(organEntry, stateIds=RI_STATE_IDS) -> stateEntry[]`
  - `pickState(prevStateId, available) -> string | null` (`available` é `stateEntry[]`)

- [ ] **Step 1: Write the failing tests**

Create `src/lib/riComparison.test.js`:

```js
import { test } from 'node:test'
import assert from 'node:assert/strict'
import {
  RI_STATE_IDS, indexComparativo, organKeyOfChapter,
  stateHasData, statesWithData, pickState,
} from './riComparison.js'

const COMPARATIVO = {
  organs: [
    {
      key: 'cg', title: 'DO COMANDO GERAL (CG)', abbr: 'CG',
      states: [
        { id: 'al', abbr: 'AL', provenance: 'curado', sourceLabel: 'cf. CBMAL',
          organs: [{ name: 'Comando Geral', abbreviation: 'CG', atribuicoes: ['comandar'] }] },
        { id: 'ac', abbr: 'AC', provenance: 'curado', sourceLabel: 'cf. CBMAC',
          organs: [{ name: 'Comando Geral', abbreviation: 'CG', atribuicoes: ['comandar'] }] },
        { id: 'rs', abbr: 'RS', provenance: 'automático', sourceLabel: 'cf. CBMRS',
          organs: [{ name: 'CG', abbreviation: 'CG', atribuicoes: [] }] },
      ],
    },
    {
      key: 'dpo', title: 'DA DPO', abbr: 'DPO',
      states: [
        { id: 'mt', abbr: 'MT', provenance: 'curado', sourceLabel: 'cf. CBMMT',
          organs: [{ name: 'Departamento', abbreviation: 'DPO', atribuicoes: ['planejar'] }] },
      ],
    },
  ],
}

test('RI_STATE_IDS tem os 9 estados com RI na ordem fixa', () => {
  assert.deepEqual(RI_STATE_IDS, ['al', 'am', 'df', 'go', 'mt', 'pr', 'pa', 'rs', 'se'])
})

test('indexComparativo indexa por key, ignorando entradas sem key', () => {
  const idx = indexComparativo({ organs: [...COMPARATIVO.organs, { key: null, states: [] }] })
  assert.equal(idx.cg.title, 'DO COMANDO GERAL (CG)')
  assert.equal(idx.dpo.abbr, 'DPO')
  assert.equal(Object.keys(idx).length, 2)
})

test('indexComparativo tolera entrada vazia', () => {
  assert.deepEqual(indexComparativo(null), {})
  assert.deepEqual(indexComparativo({}), {})
})

test('organKeyOfChapter extrai a key só de capítulos de órgão', () => {
  assert.equal(organKeyOfChapter('organ:cg'), 'cg')
  assert.equal(organKeyOfChapter('organ:dpo'), 'dpo')
  assert.equal(organKeyOfChapter('estrutura'), null)
  assert.equal(organKeyOfChapter('preliminares'), null)
  assert.equal(organKeyOfChapter(null), null)
})

test('stateHasData exige ao menos uma atribuição não vazia', () => {
  assert.equal(stateHasData({ organs: [{ atribuicoes: ['x'] }] }), true)
  assert.equal(stateHasData({ organs: [{ atribuicoes: [] }] }), false)
  assert.equal(stateHasData({ organs: [] }), false)
  assert.equal(stateHasData(null), false)
})

test('statesWithData filtra por RI + dado e mantém a ordem de RI_STATE_IDS', () => {
  const idx = indexComparativo(COMPARATIVO)
  const withData = statesWithData(idx.cg)
  // 'ac' não é estado-RI; 'rs' é RI mas tem atribuições vazias -> só 'al'
  assert.deepEqual(withData.map(s => s.id), ['al'])
})

test('statesWithData retorna [] para organEntry ausente', () => {
  assert.deepEqual(statesWithData(null), [])
})

test('pickState mantém o estado anterior quando disponível', () => {
  const available = [{ id: 'al' }, { id: 'mt' }]
  assert.equal(pickState('mt', available), 'mt')
})

test('pickState cai no primeiro quando o anterior sumiu', () => {
  const available = [{ id: 'al' }, { id: 'mt' }]
  assert.equal(pickState('rs', available), 'al')
})

test('pickState retorna null quando não há disponíveis', () => {
  assert.equal(pickState('al', []), null)
  assert.equal(pickState(null, []), null)
})
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `node --test src/lib/riComparison.test.js`
Expected: FAIL — `Cannot find module './riComparison.js'` (ou erro de import).

- [ ] **Step 3: Write the implementation**

Create `src/lib/riComparison.js`:

```js
// Lógica pura do Comparativo de RI: indexa comparativo_minuta.json por órgão,
// mapeia capítulo->órgão e seleciona os estados com RI que têm dado. Sem React.

// Os 9 estados com LOB + Regimento Interno (ordem de exibição fixa).
export const RI_STATE_IDS = ['al', 'am', 'df', 'go', 'mt', 'pr', 'pa', 'rs', 'se']

const ORGAN_PREFIX = 'organ:'

// comparativo.organs[] -> { [key]: organEntry }. Ignora entradas sem key.
export function indexComparativo(comparativo) {
  const map = {}
  for (const o of comparativo?.organs ?? []) {
    if (o && o.key) map[o.key] = o
  }
  return map
}

// "organ:cg" -> "cg"; "estrutura"/"preliminares"/"finais" -> null.
export function organKeyOfChapter(chapterId) {
  const id = String(chapterId ?? '')
  return id.startsWith(ORGAN_PREFIX) ? id.slice(ORGAN_PREFIX.length) : null
}

// Verdadeiro se algum órgão do estado tem ao menos uma atribuição não vazia.
export function stateHasData(stateEntry) {
  return (stateEntry?.organs ?? []).some(o => (o?.atribuicoes ?? []).length > 0)
}

// Estados de RI_STATE_IDS (nessa ordem) que existem no órgão e têm dado.
export function statesWithData(organEntry, stateIds = RI_STATE_IDS) {
  if (!organEntry) return []
  const byId = {}
  for (const s of organEntry.states ?? []) byId[s.id] = s
  const out = []
  for (const id of stateIds) {
    const s = byId[id]
    if (s && stateHasData(s)) out.push(s)
  }
  return out
}

// Mantém prevStateId se ainda disponível; senão o primeiro; senão null.
export function pickState(prevStateId, available) {
  if (!available || available.length === 0) return null
  if (prevStateId && available.some(s => s.id === prevStateId)) return prevStateId
  return available[0].id
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `node --test src/lib/riComparison.test.js`
Expected: PASS — todos os testes verdes.

- [ ] **Step 5: Commit**

```bash
git add src/lib/riComparison.js src/lib/riComparison.test.js
git commit -m "feat(comparativo-ri): lógica pura de indexação e seleção de estados"
```

---

### Task 2: Página `RIComparator.jsx` + rota + menu + CSS

**Files:**
- Create: `src/pages/RIComparator.jsx`
- Modify: `src/App.jsx` (imports ~14-17, `NAV` 25-35, `Routes` 180-195)
- Modify: `src/index.css` (adicionar `.ri-state-col` no fim do arquivo e no bloco `@media (max-width: 900px)`)

**Interfaces:**
- Consumes (Task 1): `indexComparativo`, `organKeyOfChapter`, `statesWithData`, `pickState` de `src/lib/riComparison.js`.
- Consumes (existentes): `buildTargets(structure)` de `src/lib/minutaTargets.js` (retorna `[{ chapterId, chapterTitle, chapterNumber, articles: [{ editId, number, caput, sectionTitle, sectionNumber, incisos: [{ index, text }] }] }]`); `articleLabel(n)` e `romanize(n)` de `src/lib/minutaArticles.js`; `ChapterRail` de `src/components/ChapterRail.jsx` (props: `chapters, counts, selectedId, onSelect`).
- Produces: componente default `RIComparator` montado na rota `/minuta/comparativo-ri`.

- [ ] **Step 1: Criar a página `RIComparator.jsx`**

Create `src/pages/RIComparator.jsx`:

```jsx
import { useEffect, useMemo, useState } from 'react'
import { articleLabel, romanize } from '../lib/minutaArticles.js'
import { buildTargets } from '../lib/minutaTargets.js'
import { indexComparativo, organKeyOfChapter, statesWithData, pickState } from '../lib/riComparison.js'
import ChapterRail from '../components/ChapterRail.jsx'

const EMPTY_COUNTS = {}

export default function RIComparator() {
  const [chapters, setChapters] = useState(null)
  const [compByKey, setCompByKey] = useState({})
  const [selectedChapterId, setSelectedChapterId] = useState(null)
  const [selectedStateId, setSelectedStateId] = useState(null)
  const [error, setError] = useState(null)

  // Carga inicial: minuta articulada + comparativo, em paralelo.
  useEffect(() => {
    let alive = true
    ;(async () => {
      try {
        const [rs, rc] = await Promise.all([
          fetch('/database/minuta_structure.json'),
          fetch('/database/comparativo_minuta.json'),
        ])
        if (!rs.ok || !rc.ok) throw new Error('fetch')
        const [structure, comparativo] = [await rs.json(), await rc.json()]
        if (!alive) return
        const chs = buildTargets(structure)
        setChapters(chs)
        setCompByKey(indexComparativo(comparativo))
        // Primeiro capítulo de órgão como padrão (fallback: primeiro capítulo).
        const firstOrgan = chs.find(c => organKeyOfChapter(c.chapterId))
        setSelectedChapterId((firstOrgan ?? chs[0])?.chapterId ?? null)
      } catch {
        if (alive) setError('Erro ao carregar os dados. Execute build_minuta_structure.py e build_minuta_comparison.py.')
      }
    })()
    return () => { alive = false }
  }, [])

  const chapter = chapters?.find(c => c.chapterId === selectedChapterId) ?? null
  const organKey = chapter ? organKeyOfChapter(chapter.chapterId) : null
  const organEntry = organKey ? compByKey[organKey] : null
  const available = useMemo(() => statesWithData(organEntry), [organEntry])

  // Reconcilia o estado quando o capítulo (e portanto `available`) muda.
  useEffect(() => {
    setSelectedStateId(prev => pickState(prev, available))
  }, [available])

  const stateEntry = available.find(s => s.id === selectedStateId) ?? null

  if (error) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Comparativo de RI</h2></div></div>
        <div className="page-body" style={{ padding: 32 }}><p style={{ color: '#c8102e' }}>{error}</p></div>
      </>
    )
  }
  if (!chapters) {
    return (
      <>
        <div className="page-header"><div className="page-header-left"><h2 className="page-title">Comparativo de RI</h2></div></div>
        <div className="page-body" style={{ padding: 32 }}><p style={{ color: 'var(--text-muted)' }}>Carregando…</p></div>
      </>
    )
  }

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Comparativo de RI — Minuta CBMRO × demais estados</h2>
          <p className="page-subtitle">Selecione um capítulo e um estado para ver, lado a lado, o texto da minuta do CBMRO e as competências do órgão equivalente no Regimento Interno do estado.</p>
        </div>
      </div>
      <div className="page-body">
        <div className="rev-layout" style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
          <ChapterRail chapters={chapters} counts={EMPTY_COUNTS} selectedId={selectedChapterId} onSelect={setSelectedChapterId} />

          <div className="rev-doc" style={{ flex: 1.25, minWidth: 0 }}>
            {chapter && (
              <>
                <p className="rev-chapter" style={{ color: '#121d3d' }}>
                  CAPÍTULO {romanize(chapter.chapterNumber)} — {chapter.chapterTitle}
                </p>
                {chapter.articles.map(art => (
                  <div key={art.number} style={{ marginBottom: 10 }}>
                    {art.sectionTitle && (
                      <p className="rev-section">Seção {romanize(art.sectionNumber)} — {art.sectionTitle}</p>
                    )}
                    <p style={{ textAlign: 'justify', margin: '0 0 4px', textIndent: art.incisos.length ? 0 : '1.25em' }}>
                      <strong>{articleLabel(art.number)}</strong> {art.caput}
                    </p>
                    {art.incisos.map(inc => (
                      <p key={inc.index} style={{ textAlign: 'justify', margin: '2px 0 2px 1.25em' }}>
                        <strong>{romanize(inc.index + 1)} -</strong> {inc.text}
                      </p>
                    ))}
                  </div>
                ))}
              </>
            )}
          </div>

          <aside className="ri-state-col">
            <div style={{ fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', fontSize: 11, marginBottom: 8 }}>
              Regimento Interno equivalente
            </div>
            {!organKey ? (
              <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>Sem equivalente direto nos RIs analisados.</p>
            ) : available.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>Nenhum RI analisado trata deste órgão.</p>
            ) : (
              <>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 12 }}>
                  {available.map(s => {
                    const on = s.id === selectedStateId
                    return (
                      <button key={s.id} onClick={() => setSelectedStateId(s.id)} style={{
                        font: '700 11px Inter, sans-serif', padding: '4px 9px', borderRadius: 20, cursor: 'pointer',
                        border: on ? '1px solid #c8102e' : '1px solid var(--border-card)',
                        background: on ? '#c8102e' : '#fff', color: on ? '#fff' : '#444',
                      }}>{s.abbr}</button>
                    )
                  })}
                </div>
                {stateEntry ? (
                  <div>
                    {(stateEntry.organs ?? []).map((o, i) => (
                      <div key={i} style={{ marginBottom: 12 }}>
                        <p style={{ fontWeight: 700, fontSize: 13, color: '#121d3d', margin: '0 0 4px' }}>
                          {o.name}{o.abbreviation ? ` (${o.abbreviation})` : ''}
                        </p>
                        {(o.atribuicoes ?? []).map((a, j) => (
                          <p key={j} style={{ fontSize: 12.5, textAlign: 'justify', margin: '0 0 5px', color: '#333' }}>• {a}</p>
                        ))}
                      </div>
                    ))}
                    <div style={{ marginTop: 10, paddingTop: 8, borderTop: '1px solid var(--border-card)', fontSize: 11, color: 'var(--text-muted)' }}>
                      <span style={{
                        display: 'inline-block', padding: '1px 7px', borderRadius: 10, fontWeight: 700, fontSize: 10, marginRight: 6,
                        background: stateEntry.provenance === 'curado' ? '#e6f4ea' : '#fdeaea',
                        color: stateEntry.provenance === 'curado' ? '#1e7d40' : '#c8102e',
                      }}>{stateEntry.provenance === 'curado' ? 'curado (RI)' : 'automático (LOB)'}</span>
                      {stateEntry.sourceLabel}
                    </div>
                  </div>
                ) : (
                  <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>Nenhum dado disponível para este órgão neste RI.</p>
                )}
              </>
            )}
          </aside>
        </div>
      </div>
    </>
  )
}
```

- [ ] **Step 2: Adicionar `.ri-state-col` ao CSS**

No `src/index.css`, adicionar ao final do arquivo:

```css
/* Coluna do estado no Comparativo de RI: fixa e rolável no desktop. */
.ri-state-col {
  flex: 0 0 320px; align-self: flex-start; position: sticky; top: calc(var(--header-h) + 8px);
  max-height: calc(100vh - var(--header-h) - 24px); overflow: auto;
  border: 1px solid var(--border-card); border-radius: 8px; background: #fff; padding: 14px 16px;
}
```

E, dentro do bloco `@media (max-width: 900px)` existente (logo após a regra `.chapter-rail`, por volta da linha 1445), acrescentar:

```css
  .ri-state-col {
    flex: 1 1 auto !important; width: 100% !important; position: static !important;
    top: auto !important; max-height: none !important;
  }
```

- [ ] **Step 3: Registrar a rota e o item de menu no `App.jsx`**

Em `src/App.jsx`:

1. Adicionar `GitCompareArrows` à lista de ícones importados de `lucide-react` (linha 3-7). Fica:

```jsx
import {
  Flame, LayoutDashboard, BookOpen, GitCompare,
  Search, Library, ScrollText, Menu, X, Network, LogOut, LogIn,
  MessageSquare, ShieldCheck, MessagesSquare, Gavel, GitCompareArrows
} from 'lucide-react'
```

2. Importar a página (após a linha 17, `import MinutaDeliberacao ...`):

```jsx
import RIComparator from './pages/RIComparator.jsx'
```

3. Inserir o item no array `NAV`, logo após a linha `{ to: '/minuta/deliberacao', ... }`:

```jsx
  { to: '/minuta/comparativo-ri', icon: GitCompareArrows, label: 'Comparativo de RI' },
```

4. Registrar a rota, logo após `<Route path="/minuta/deliberacao" ... />` (linha 190):

```jsx
          <Route path="/minuta/comparativo-ri" element={<RIComparator />} />
```

- [ ] **Step 4: Verificar a compilação**

Run: `npm run build`
Expected: build conclui sem erros (Vite gera `dist/` sem falha de import/JSX).

- [ ] **Step 5: Verificação manual no dev server**

Run: `npm run dev -- --port 5173 --strictPort` (se ainda não estiver rodando) e abrir http://localhost:5173/minuta/comparativo-ri

Conferir:
- A página carrega com 3 colunas; "Comparativo de RI" aparece no menu lateral.
- Capítulo de órgão (ex.: DPO) mostra o texto da minuta à esquerda e as competências do estado à direita.
- As pills listam só estados-RI com dado; clicar troca a coluna direita.
- Trocar de capítulo mantém o estado quando ele tem dado; senão repõe no primeiro.
- Capítulos "Preliminares"/"Estrutura"/"Finais" mostram "Sem equivalente direto nos RIs analisados."
- Badge de proveniência + rótulo de fonte visíveis.

- [ ] **Step 6: Commit**

```bash
git add src/pages/RIComparator.jsx src/App.jsx src/index.css
git commit -m "feat(comparativo-ri): página /minuta/comparativo-ri com rota e menu"
```

---

## Self-Review

**1. Spec coverage:**
- Página separada + rota + menu → Task 2 (steps 1, 3). ✓
- 3 zonas (ChapterRail · CBMRO · estado) → Task 2 step 1. ✓
- Somente leitura, sem pipeline → nenhum script Python; Global Constraints. ✓
- Dois fetches paralelos + índice por organKey → Task 2 step 1 (`Promise.all`, `indexComparativo`). ✓
- Mapeamento capítulo→órgão, prose/articles sem organKey → `organKeyOfChapter` (Task 1) + aviso "Sem equivalente" (Task 2). ✓
- 9 estados-RI fixos + pills só com dado → `RI_STATE_IDS`/`statesWithData` (Task 1) + render de pills (Task 2). ✓
- Regras de seleção (mantém/repõe) → `pickState` (Task 1) + effect de reconciliação (Task 2). ✓
- Bordas: falha de fetch, capítulo sem órgão, órgão sem estado, estado sem dado → Task 2 step 1 (ramos condicionais). ✓
- Badge proveniência + sourceLabel → Task 2 step 1. ✓
- Testes de lógica pura → Task 1. ✓

**2. Placeholder scan:** Sem TBD/TODO; todo código é literal e completo.

**3. Type consistency:** `chapterId` string `"organ:<key>"`; `organKeyOfChapter` retorna a key ou null; `statesWithData` retorna `stateEntry[]` com `{ id, abbr, provenance, sourceLabel, organs }`; `pickState(prev, stateEntry[])` retorna id string ou null. Uso na página bate com as assinaturas da Task 1. `ChapterRail` recebe `counts={}` (EMPTY_COUNTS) — compatível com `counts[c.chapterId] ?? 0`.
