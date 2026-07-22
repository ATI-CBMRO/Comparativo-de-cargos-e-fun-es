# Diagramas do Regulamento — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Destravar `/regulamento/diagramas` com árvore do documento (Regulamento → 2 Partes → 16 temas) + mapa mental, montadas na tela a partir do `regulamento_structure.json` existente.

**Architecture:** Lógica pura nova (`src/lib/regulamentoTree.js`) monta um nó raiz no formato que `MinutaOrgChart` já consome; `RegDiagramas.jsx` vira espelho de `MinutaDiagrams.jsx` reusando `MinutaOrgChart`, `MinutaMindMap` e um `MinutaDetailPanel` extraído para componente compartilhado. Zero mudança em geradores Python/JSON.

**Tech Stack:** React 18 + Vite, `node --test` para lógica pura, CSS existente (`.moc-*`, `.mmm-*`, `.md-*` em `src/index.css`).

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-21-regulamento-diagramas-design.md`.
- NÃO alterar: geradores Python, JSONs de `database/`, comportamento de `/minuta/diagramas` (RI), `MinutaOrgChart.jsx`, `MinutaMindMap.jsx`, rotas/menu (a rota `/regulamento/diagramas` já existe em `App.jsx`).
- Cenários: carregar dados via `scenarioDbUrl(cenario, 'regulamento_structure.json')` (`src/lib/scenario.js`) + `useScenario()` (`src/context/ScenarioContext.jsx`), como `MinutaDiagrams.jsx:91-100` faz.
- Idioma da UI: pt-BR. Comentários de código em pt-BR, no estilo dos arquivos vizinhos.
- Rodar `node --test` a cada tarefa; os 96 testes existentes devem seguir passando.
- MANDATORY para exploração: rodar `graphify query "<pergunta>"` antes de grep/leitura ampla de fontes.

---

### Task 1: Lógica pura `buildRegulamentoTree` (TDD)

**Files:**
- Create: `src/lib/regulamentoTree.js`
- Test: `src/lib/regulamentoTree.test.js`

**Interfaces:**
- Produces: `buildRegulamentoTree(chapters) -> node` onde `node = { sigla, label, chapterId, synthetic?, structural?, children }` — MESMO formato consumido por `MinutaOrgChart.jsx` (raiz `synthetic:true` fica sempre expandida e não clicável; nós de Parte também `synthetic:true`; temas clicáveis via `chapterId`).
- Consumes: `PARTE_HEADERS` de `src/lib/regulamentoPartes.js` (`{ geral: 'PARTE I — GERAL', servico: 'PARTE II — DO SERVIÇO' }`).

- [ ] **Step 1: Write the failing test** — criar `src/lib/regulamentoTree.test.js`:

```js
import test from 'node:test'
import assert from 'node:assert/strict'
import { buildRegulamentoTree } from './regulamentoTree.js'

const CHAPTERS = [
  { id: 'reg:disposicoes-preliminares', chapterTitle: 'DAS DISPOSIÇÕES PRELIMINARES', parte: 'geral', articles: [{ caput: 'Art. 1º ...' }, { caput: 'Art. 2º ...' }] },
  { id: 'reg:pessoal-quadros', chapterTitle: 'DO PESSOAL', parte: 'geral', articles: [{ caput: 'Art. 3º ...' }] },
  { id: 'reg:servico-operacional', chapterTitle: 'DO SERVIÇO OPERACIONAL', parte: 'servico', articles: [{ caput: 'Art. 4º ...' }] },
]

test('raiz sintética com as 2 Partes na ordem geral → servico', () => {
  const root = buildRegulamentoTree(CHAPTERS)
  assert.equal(root.synthetic, true)
  assert.equal(root.label, 'Regulamento Geral do CBMRO')
  assert.deepEqual(root.children.map(p => p.label), ['PARTE I — GERAL', 'PARTE II — DO SERVIÇO'])
  assert.ok(root.children.every(p => p.synthetic === true && !p.chapterId))
})

test('temas na ordem do documento, clicáveis, com contagem de artigos', () => {
  const [pI, pII] = buildRegulamentoTree(CHAPTERS).children
  assert.deepEqual(pI.children.map(t => t.chapterId), ['reg:disposicoes-preliminares', 'reg:pessoal-quadros'])
  assert.equal(pI.children[0].label, 'DAS DISPOSIÇÕES PRELIMINARES')
  assert.equal(pI.children[0].sigla, '2 art.')
  assert.equal(pI.children[1].sigla, '1 art.')
  assert.deepEqual(pII.children.map(t => t.chapterId), ['reg:servico-operacional'])
  assert.deepEqual(pI.children[0].children, [])
})

test('capítulo sem parte reconhecida cai em "Outros"; sem esse caso, "Outros" não existe', () => {
  const comOrfao = buildRegulamentoTree([...CHAPTERS, { id: 'reg:x', chapterTitle: 'X', articles: [] }])
  assert.deepEqual(comOrfao.children.map(p => p.label), ['PARTE I — GERAL', 'PARTE II — DO SERVIÇO', 'Outros'])
  assert.equal(comOrfao.children[2].children[0].sigla, '0 art.')
  assert.equal(buildRegulamentoTree(CHAPTERS).children.length, 2)
})

test('entrada vazia/nula devolve raiz sem filhos', () => {
  assert.deepEqual(buildRegulamentoTree([]).children, [])
  assert.deepEqual(buildRegulamentoTree(null).children, [])
})
```

- [ ] **Step 2: Run test to verify it fails** — `node --test src/lib/regulamentoTree.test.js` → FAIL (módulo inexistente).

- [ ] **Step 3: Write minimal implementation** — criar `src/lib/regulamentoTree.js`:

```js
// Árvore do DOCUMENTO do Regulamento (Regulamento → 2 Partes → temas) no formato de nó
// que MinutaOrgChart consome ({ sigla, label, chapterId, synthetic, children }).
// O Regulamento é temático — não há cadeia de comando; esta árvore mostra a estrutura
// do documento (spec 2026-07-21-regulamento-diagramas-design.md).
import { PARTE_HEADERS } from './regulamentoPartes.js'

const OUTROS = 'Outros' // defensivo: capítulo sem `parte` reconhecida (hoje não ocorre)

export function buildRegulamentoTree(chapters) {
  const ordem = [...Object.keys(PARTE_HEADERS), OUTROS]
  const porParte = new Map()
  for (const ch of chapters ?? []) {
    const key = PARTE_HEADERS[ch.parte] ? ch.parte : OUTROS
    if (!porParte.has(key)) porParte.set(key, [])
    porParte.get(key).push({
      sigla: `${(ch.articles ?? []).length} art.`,
      label: ch.chapterTitle,
      chapterId: ch.id,
      children: [],
    })
  }
  return {
    synthetic: true,
    sigla: '',
    label: 'Regulamento Geral do CBMRO',
    chapterId: null,
    children: ordem
      .filter(key => porParte.has(key))
      .map(key => ({
        synthetic: true,
        sigla: '',
        label: PARTE_HEADERS[key] ?? OUTROS,
        chapterId: null,
        children: porParte.get(key),
      })),
  }
}
```

- [ ] **Step 4: Run tests** — `node --test src/lib/regulamentoTree.test.js` → PASS (4/4); depois `node --test` completo → 96 + 4 passando.

- [ ] **Step 5: Commit**

```bash
git add src/lib/regulamentoTree.js src/lib/regulamentoTree.test.js
git commit -m "feat(regulamento): lógica pura da árvore do documento (2 Partes → temas)"
```

### Task 2: Extrair `MinutaDetailPanel` para componente compartilhado

**Files:**
- Create: `src/components/MinutaDetailPanel.jsx`
- Modify: `src/pages/MinutaDiagrams.jsx` (remover as definições locais, importar o componente)

**Interfaces:**
- Produces: default export `MinutaDetailPanel({ chapter, onClose })` — comportamento IDÊNTICO ao atual painel local de `MinutaDiagrams.jsx:35-65` (suporta `kind:'organ'` via `sections` e `kind:'articles'` via `articles`).
- Consumes: nada de outras tasks.

- [ ] **Step 1: Criar `src/components/MinutaDetailPanel.jsx`** movendo VERBATIM de `MinutaDiagrams.jsx` as funções `srcBadge` (linhas 9-21), `capitalizeFirst` (23-27), `panelSections` (29-33) e o componente `MinutaDetailPanel` (35-65), acrescentando no topo:

```jsx
// Painel lateral de detalhe de capítulo, compartilhado por MinutaDiagrams (RI) e
// RegDiagramas (Regulamento). Extraído verbatim de MinutaDiagrams.jsx (2026-07-21).
import { X } from 'lucide-react'
```

e trocando `function MinutaDetailPanel` por `export default function MinutaDetailPanel`.

- [ ] **Step 2: Atualizar `MinutaDiagrams.jsx`** — apagar as 4 definições movidas; remover `X` do import de `lucide-react` (se não sobrar outro uso); adicionar `import MinutaDetailPanel from '../components/MinutaDetailPanel.jsx'`. NENHUMA outra linha muda.

- [ ] **Step 3: Verificar** — `node --test` (todos passam) e `npm run build` (sem erro). `git diff src/pages/MinutaDiagrams.jsx` deve mostrar SÓ remoção das definições + import (prova de preservação do RI).

- [ ] **Step 4: Commit**

```bash
git add src/components/MinutaDetailPanel.jsx src/pages/MinutaDiagrams.jsx
git commit -m "refactor(diagramas): extrai MinutaDetailPanel para componente compartilhado"
```

### Task 3: Reescrever `RegDiagramas.jsx` (árvore + mapa mental)

**Files:**
- Modify: `src/pages/RegDiagramas.jsx` (substituição integral do "em breve")

**Interfaces:**
- Consumes: `buildRegulamentoTree(chapters)` (Task 1); `MinutaDetailPanel` (Task 2); `MinutaOrgChart`/`MinutaMindMap` (existentes); `PARTE_HEADERS` de `regulamentoPartes.js`; `fetchJson` de `dataCache.js`; `useScenario`/`scenarioDbUrl`.
- Produces: tela final; nada consumido por outras tasks.

- [ ] **Step 1: Substituir o conteúdo de `src/pages/RegDiagramas.jsx`** por:

```jsx
// Diagramas do Regulamento Geral — árvore do DOCUMENTO (2 Partes → 16 temas) e mapa
// mental. O Regulamento é temático (não tem cadeia de comando): a árvore mostra a
// estrutura do documento, montada NA TELA a partir do regulamento_structure.json
// (spec 2026-07-21-regulamento-diagramas-design.md). Espelha MinutaDiagrams.jsx.
import { useMemo, useState, useEffect } from 'react'
import { Printer, Network, LayoutGrid, ChevronsDownUp, ChevronsUpDown } from 'lucide-react'
import MinutaOrgChart from '../components/MinutaOrgChart.jsx'
import MinutaMindMap from '../components/MinutaMindMap.jsx'
import MinutaDetailPanel from '../components/MinutaDetailPanel.jsx'
import { buildRegulamentoTree } from '../lib/regulamentoTree.js'
import { PARTE_HEADERS } from '../lib/regulamentoPartes.js'
import { fetchJson } from '../lib/dataCache.js'
import { useScenario } from '../context/ScenarioContext.jsx'
import { scenarioDbUrl } from '../lib/scenario.js'

const VIEW_LABEL = { org: 'Árvore do documento', mind: 'Mapa mental — temas do Regulamento' }

// Faixa de Parte (mesmo visual das faixas da Revisão/Subsídio).
function ParteFaixa({ children }) {
  return (
    <div style={{
      textAlign: 'center', fontWeight: 800, fontSize: 15, letterSpacing: 1,
      color: 'var(--cbm-red-700)', borderTop: '2px solid var(--cbm-red-700)',
      borderBottom: '2px solid var(--cbm-red-700)', padding: '8px 0', margin: '20px 0 12px',
    }}>{children}</div>
  )
}

export default function RegDiagramas() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [view, setView] = useState('org')
  const [selected, setSelected] = useState(null)
  // Expansão da árvore: `expandAll` é o estado-base reaplicado ao remontar (treeKey++).
  const [expandAll, setExpandAll] = useState(false)
  const [treeKey, setTreeKey] = useState(0)

  function setTree(expand) { setExpandAll(expand); setTreeKey(k => k + 1) }

  // Imprime com a árvore inteira aberta (senão o PDF sairia recolhido).
  function handlePrint() {
    if (view === 'org' && !expandAll) {
      setTree(true)
      setTimeout(() => window.print(), 120)
    } else {
      window.print()
    }
  }

  const { cenario } = useScenario()

  useEffect(() => {
    setLoading(true)
    setError(null)
    fetchJson(scenarioDbUrl(cenario, 'regulamento_structure.json'))
      .then(setData)
      .catch(() => setError('Erro ao carregar regulamento_structure.json. Execute build_regulamento_structure.py.'))
      .finally(() => setLoading(false))
  }, [cenario])

  const tree = useMemo(() => data ? buildRegulamentoTree(data.chapters) : null, [data])
  // Cartões do mapa mental agrupados por Parte (faixas PARTE I / PARTE II).
  const partes = useMemo(() => {
    if (!data) return []
    return Object.keys(PARTE_HEADERS)
      .map(key => ({ key, label: PARTE_HEADERS[key], chapters: data.chapters.filter(ch => ch.parte === key) }))
      .filter(p => p.chapters.length)
  }, [data])

  const header = (
    <div className="page-header">
      <div className="page-header-left">
        <h2 className="page-title">Diagramas — Regulamento Geral</h2>
        <p className="page-subtitle">
          Árvore do documento (2 Partes e seus temas) e mapa mental da minuta do
          Regulamento Geral do CBMRO. O Regulamento é temático — os diagramas mostram
          a estrutura do documento, não uma cadeia de comando.
        </p>
      </div>
    </div>
  )

  if (loading) {
    return (<>{header}<div className="page-body" style={{ padding: 32 }}>
      <p style={{ color: 'var(--text-muted)' }}>Carregando dados…</p></div></>)
  }
  if (error || !data) {
    return (<>{header}<div className="page-body" style={{ padding: 32 }}>
      <p style={{ color: 'var(--cbm-red-700)' }}>{error || 'Sem dados.'}</p></div></>)
  }

  const selectedChapter = selected ? data.chapters.find(c => c.id === selected) : null

  return (
    <>
      {header}
      <div className="page-body">
        <div className="print-only-title" style={{ display: 'none' }}>Diagramas do Regulamento — {VIEW_LABEL[view]}</div>

        <div className="md-controls no-print">
          <div className="md-segmented">
            <button
              type="button"
              className={`md-seg${view === 'org' ? ' active' : ''}`}
              onClick={() => { setView('org'); setSelected(null); setTree(false) }}
            ><Network size={15} /> Árvore do documento</button>
            <button
              type="button"
              className={`md-seg${view === 'mind' ? ' active' : ''}`}
              onClick={() => { setView('mind'); setSelected(null) }}
            ><LayoutGrid size={15} /> Mapa mental</button>
          </div>
          {view === 'org' && (
            <div className="md-segmented">
              <button type="button" className="md-seg" onClick={() => setTree(true)} title="Expandir toda a árvore">
                <ChevronsUpDown size={15} /> Expandir tudo
              </button>
              <button type="button" className="md-seg" onClick={() => setTree(false)} title="Recolher até o 1º nível">
                <ChevronsDownUp size={15} /> Recolher tudo
              </button>
            </div>
          )}
          <button type="button" className="btn btn-ghost btn-sm" onClick={handlePrint}>
            <Printer size={15} style={{ verticalAlign: -2, marginRight: 4 }} /> Imprimir / PDF
          </button>
        </div>

        <div className="md-layout">
          <div className="md-diagram">
            {view === 'org' ? (
              <MinutaOrgChart key={treeKey} chart={tree} onSelect={setSelected} selectedId={selected} defaultExpanded={expandAll} />
            ) : (
              partes.map(p => (
                <div key={p.key}>
                  <ParteFaixa>{p.label}</ParteFaixa>
                  <MinutaMindMap chapters={p.chapters} onSelect={setSelected} selectedId={selected} />
                </div>
              ))
            )}
          </div>
          {selectedChapter && (
            <MinutaDetailPanel chapter={selectedChapter} onClose={() => setSelected(null)} />
          )}
        </div>
      </div>
    </>
  )
}
```

- [ ] **Step 2: Verificar** — `node --test` (todos passam) e `npm run build` (sem erro). Nota: nós de Parte são `synthetic:true` → `MinutaOrgChart` os mantém sempre expandidos e sem clique, comportamento desejado; "Recolher tudo" recolhe só os temas (que não têm filhos) — sem efeito prático, aceitável.

- [ ] **Step 3: Smoke manual** — `npm run dev`, abrir `http://localhost:5173/regulamento/diagramas`: árvore com 2 Partes/16 temas; clicar num tema abre painel com artigos; aba Mapa mental com faixas; trocar cenário p/ atual recarrega.

- [ ] **Step 4: Commit**

```bash
git add src/pages/RegDiagramas.jsx
git commit -m "feat(regulamento): destrava Diagramas — árvore do documento + mapa mental"
```
