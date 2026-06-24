# Diagramas da Minuta — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Nova página "Diagramas da Minuta" (`/minuta-diagramas`) com um organograma (cadeia de comando dos 12 órgãos) e um mapa mental (cartões por capítulo) da Minuta de RI, ambos clicáveis para abrir um painel de detalhe, com impressão/PDF.

**Architecture:** O pipeline Python (`build_minuta_structure.py`) passa a emitir um campo `commandChart` (árvore dos 12 órgãos derivada de `ro.json`) dentro de `minuta_structure.json`. Uma nova página React lê esse único JSON, alterna entre dois componentes de diagrama (`MinutaOrgChart` caixas-e-linhas em CSS puro; `MinutaMindMap` grade de cartões) e mostra um painel de detalhe lendo o capítulo correspondente. Sem dependências novas.

**Tech Stack:** Python (pipeline), React 18 + react-router-dom, lucide-react, CSS único em `src/index.css`, `window.print()` + `@media print`.

---

## File Structure

- **Modify** `scripts/build_minuta_structure.py` — adiciona `build_command_chart()` e grava `commandChart` no JSON.
- **Create** `scripts/test_command_chart.py` — teste (assert) da forma da árvore.
- **Create** `src/components/MinutaOrgChart.jsx` — organograma caixas-e-linhas (CSS puro).
- **Create** `src/components/MinutaMindMap.jsx` — grade de cartões por capítulo.
- **Create** `src/pages/MinutaDiagrams.jsx` — página: toggle de visão, painel de detalhe, impressão.
- **Modify** `src/App.jsx` — import, item de `NAV`, `<Route>`.
- **Modify** `src/index.css` — estilos `.moc-*`, `.mmm-*`, `.md-*` e regras `@media print`.
- **Modify** `CLAUDE.md` — documenta `commandChart` e a página `/minuta-diagramas`.

---

## Task 1: Pipeline — campo `commandChart` no minuta_structure.json

**Files:**
- Modify: `scripts/build_minuta_structure.py`
- Test: `scripts/test_command_chart.py` (create)

- [ ] **Step 1: Write the failing test**

Create `scripts/test_command_chart.py`:

```python
"""Teste da forma da árvore commandChart (sem pytest: rodar com python)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_minuta_structure as B  # noqa: E402
from build_minuta_structure import build_command_chart  # noqa: E402

RO_JSON = Path(__file__).parent.parent / "database" / "organs_detail" / "ro.json"


def _chapters(organs):
    chapters = [B.build_preliminares_chapter(), B.build_estrutura_chapter(organs)]
    for k, title, _a in B.ORGAN_ORDER:
        o = organs.get(k)
        if o:
            chapters.append(B.build_organ_chapter(k, title, o))
    chapters.append(B.build_guarnicao_chapter())
    chapters.append(B.build_finais_chapter())
    return chapters


def kids(node):
    return {c["organKey"]: c for c in node["children"]}


def main():
    organs = json.loads(RO_JSON.read_text(encoding="utf-8"))["organs"]
    chart = build_command_chart(organs, _chapters(organs))

    assert chart.get("synthetic") is True
    assert chart["label"] == "Subcomandante-Geral"

    top = kids(chart)
    assert set(top) == {"dpo", "doe"}, list(top)
    dpo = kids(top["dpo"])
    assert set(dpo) == {"cot", "crbm"}, list(dpo)
    assert set(kids(dpo["cot"])) == {"cat"}
    crbm = kids(dpo["crbm"])
    assert set(crbm) == {"bbm", "cibm"}, list(crbm)
    bbm = kids(crbm["bbm"])
    assert set(bbm) == {"gbm"}
    assert set(kids(bbm["gbm"])) == {"guarnicao"}
    assert set(kids(top["doe"])) == {"bbs", "bifea", "boa"}, list(kids(top["doe"]))

    def walk(n):
        if not n.get("synthetic"):
            assert n["chapterId"].startswith("organ:"), n
            assert "sigla" in n and "label" in n, n
        for c in n["children"]:
            walk(c)
    walk(chart)

    print("OK: commandChart shape correct")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python scripts/test_command_chart.py`
Expected: FAIL com `ImportError: cannot import name 'build_command_chart'`.

- [ ] **Step 3: Add the `build_command_chart` function**

Em `scripts/build_minuta_structure.py`, adicione esta função logo antes de `def main():` (a `re` já está importada no topo do arquivo):

```python
# Colocações padrão para nós que não casam pela subordinação textual do ro.json:
#   gbm        -> subordinadoA = "Pelotão…" (fora do conjunto) -> fração elementar sob BBM
#   guarnicao  -> não existe no ro.json (nó novo do RISD-CBMSE) -> menor fração sob GBM
COMMAND_PARENT_OVERRIDE = {"gbm": "bbm", "guarnicao": "gbm"}


def build_command_chart(organs, chapters):
    """Árvore dos 12 órgãos (capítulos kind='organ') pela subordinação do ro.json.

    Pai = órgão do conjunto cuja SIGLA aparece em subordinadoA; senão, raiz.
    Retorna a raiz sintética 'Subcomandante-Geral'.
    """
    nodes = {}
    for c in chapters:
        if c.get("kind") != "organ":
            continue
        k = c["organKey"]
        nodes[k] = {
            "organKey": k,
            "sigla": c.get("abbr") or "",
            "label": c.get("label") or "",
            "chapterId": c["id"],
            "children": [],
        }

    siglas = {k: n["sigla"] for k, n in nodes.items() if n["sigla"]}

    def find_parent(k):
        if k in COMMAND_PARENT_OVERRIDE:
            return COMMAND_PARENT_OVERRIDE[k]
        sub = (organs.get(k) or {}).get("subordinadoA", "") or ""
        for other_k, sig in siglas.items():
            if other_k == k:
                continue
            if re.search(rf"\b{re.escape(sig)}\b", sub):
                return other_k
        return None  # raiz

    roots = []
    for k, n in nodes.items():
        p = find_parent(k)
        if p and p in nodes:
            nodes[p]["children"].append(n)
        else:
            roots.append(n)

    return {"label": "Subcomandante-Geral", "synthetic": True, "children": roots}
```

- [ ] **Step 4: Wire `commandChart` into the output**

Em `scripts/build_minuta_structure.py`, dentro de `main()`, altere o dict `output` para incluir o campo. Localize:

```python
    output = {
        "generated_by": "scripts/build_minuta_structure.py",
        "title": TITLE,
        "chapters": chapters,
    }
```

Substitua por:

```python
    output = {
        "generated_by": "scripts/build_minuta_structure.py",
        "title": TITLE,
        "chapters": chapters,
        "commandChart": build_command_chart(organs, chapters),
    }
```

- [ ] **Step 5: Run the test to verify it passes**

Run: `python scripts/test_command_chart.py`
Expected: `OK: commandChart shape correct`

- [ ] **Step 6: Regenerate the JSON and sanity-check**

Run: `python scripts/build_minuta_structure.py`
Expected: imprime `Gerado: …minuta_structure.json` e a contagem de capítulos.

Run: `python -c "import json; d=json.load(open('database/minuta_structure.json',encoding='utf-8')); print('commandChart' in d, d['commandChart']['label'], [c['organKey'] for c in d['commandChart']['children']])"`
Expected: `True Subcomandante-Geral ['dpo', 'doe']`

- [ ] **Step 7: Commit**

```bash
git add scripts/build_minuta_structure.py scripts/test_command_chart.py database/minuta_structure.json
git commit -m "feat(minuta): commandChart (árvore dos 12 órgãos) no minuta_structure.json

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: Componente `MinutaOrgChart.jsx`

**Files:**
- Create: `src/components/MinutaOrgChart.jsx`
- Modify: `src/index.css` (estilos `.moc-*`)

- [ ] **Step 1: Create the component**

Create `src/components/MinutaOrgChart.jsx`:

```jsx
// Organograma caixas-e-linhas (CSS puro) da cadeia de comando da minuta.
// `chart` é o nó raiz (commandChart); cada nó: { organKey, sigla, label, chapterId, children }.
// A raiz é sintética (synthetic:true, sem chapterId) e não é clicável.

function ChartNode({ node, onSelect, selectedId }) {
  const kids = node.children || []
  const clickable = !node.synthetic && node.chapterId
  const selected = clickable && node.chapterId === selectedId
  const cls = `moc-box${node.synthetic ? ' moc-box-root' : ''}${selected ? ' moc-box-sel' : ''}`

  const inner = (
    <>
      {node.sigla ? <span className="moc-sigla">{node.sigla}</span> : null}
      <span className="moc-label">{node.label}</span>
    </>
  )

  return (
    <li>
      {clickable ? (
        <button type="button" className={cls} onClick={() => onSelect(node.chapterId)}>
          {inner}
        </button>
      ) : (
        <div className={cls}>{inner}</div>
      )}
      {kids.length > 0 && (
        <ul>
          {kids.map(c => (
            <ChartNode key={c.organKey || c.label} node={c} onSelect={onSelect} selectedId={selectedId} />
          ))}
        </ul>
      )}
    </li>
  )
}

export default function MinutaOrgChart({ chart, onSelect, selectedId }) {
  if (!chart) return null
  return (
    <div className="moc-tree">
      <ul>
        <ChartNode node={chart} onSelect={onSelect} selectedId={selectedId} />
      </ul>
    </div>
  )
}
```

- [ ] **Step 2: Add the CSS**

Em `src/index.css`, ao final do arquivo (antes de qualquer bloco `@media print` final, ou logo após os estilos existentes do organograma), adicione:

```css
/* ── Organograma caixas-e-linhas (Diagramas da Minuta) ── */
.moc-tree { overflow-x: auto; padding: 8px 0 16px; }
.moc-tree > ul { display: flex; justify-content: center; min-width: max-content; }
.moc-tree ul { display: flex; justify-content: center; padding-top: 22px; position: relative; }
.moc-tree li { list-style: none; text-align: center; position: relative; padding: 22px 8px 0; }
.moc-tree li::before, .moc-tree li::after {
  content: ''; position: absolute; top: 0; right: 50%;
  border-top: 1.5px solid var(--border-card); width: 50%; height: 22px;
}
.moc-tree li::after { right: auto; left: 50%; border-left: 1.5px solid var(--border-card); }
.moc-tree li:only-child::before, .moc-tree li:only-child::after { display: none; }
.moc-tree li:only-child { padding-top: 0; }
.moc-tree li:first-child::before, .moc-tree li:last-child::after { border: 0 none; }
.moc-tree li:last-child::before { border-right: 1.5px solid var(--border-card); border-radius: 0 6px 0 0; }
.moc-tree li:first-child::after { border-radius: 6px 0 0 0; }
.moc-tree ul ul::before {
  content: ''; position: absolute; top: 0; left: 50%;
  border-left: 1.5px solid var(--border-card); width: 0; height: 22px;
}

.moc-box {
  display: inline-flex; flex-direction: column; align-items: center; gap: 2px;
  min-width: 96px; max-width: 158px; padding: 8px 12px;
  border: 1.5px solid var(--border-card); border-radius: 8px; background: #fff;
  font-family: inherit; cursor: pointer; color: #121d3d; line-height: 1.25;
  transition: border-color 0.15s, box-shadow 0.15s;
}
button.moc-box:hover { border-color: var(--cbm-red-400); }
.moc-box-root { background: #c8102e; border-color: #c8102e; color: #fff; cursor: default; }
.moc-box-root .moc-label { color: #fff; font-weight: 700; font-size: 12px; }
.moc-box-sel { border-color: #c8102e; box-shadow: 0 0 0 2px rgba(200, 16, 46, 0.25); }
.moc-sigla { font-weight: 800; font-size: 13px; }
.moc-label { font-size: 10.5px; color: var(--text-muted); }
```

- [ ] **Step 3: Verify it imports cleanly (build check)**

Run: `npm run build`
Expected: build conclui sem erros (o componente ainda não está roteado; este passo só garante que não há erro de sintaxe).

- [ ] **Step 4: Commit**

```bash
git add src/components/MinutaOrgChart.jsx src/index.css
git commit -m "feat(diagramas): componente MinutaOrgChart (org chart CSS puro)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: Componente `MinutaMindMap.jsx`

**Files:**
- Create: `src/components/MinutaMindMap.jsx`
- Modify: `src/index.css` (estilos `.mmm-*`)

- [ ] **Step 1: Create the component**

Create `src/components/MinutaMindMap.jsx`:

```jsx
// Mapa mental: grade de cartões, um por capítulo da minuta.
// `chapters` é data.chapters; cada cartão lista suas seções (organ) ou caputs (articles).

function chapterSubitems(ch) {
  if (ch.kind === 'organ') return (ch.sections || []).map(s => s.sectionTitle).filter(Boolean)
  if (ch.kind === 'articles') return (ch.articles || []).map(a => a.caput).filter(Boolean)
  return []
}

export default function MinutaMindMap({ chapters, onSelect, selectedId }) {
  if (!chapters || !chapters.length) return null
  return (
    <div className="mmm-grid">
      {chapters.map(ch => {
        const sub = chapterSubitems(ch)
        const selected = ch.id === selectedId
        return (
          <button
            key={ch.id}
            type="button"
            className={`mmm-card${selected ? ' mmm-card-sel' : ''}`}
            onClick={() => onSelect(ch.id)}
          >
            <div className="mmm-card-head">{ch.chapterTitle}</div>
            {sub.length ? (
              <ul className="mmm-card-list">
                {sub.map((t, i) => <li key={i}>{t}</li>)}
              </ul>
            ) : (
              <div className="mmm-empty">Texto corrido</div>
            )}
          </button>
        )
      })}
    </div>
  )
}
```

- [ ] **Step 2: Add the CSS**

Em `src/index.css`, logo após o bloco `.moc-*` da Task 2, adicione:

```css
/* ── Mapa mental: cartões por capítulo (Diagramas da Minuta) ── */
.mmm-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(244px, 1fr)); gap: 14px; }
.mmm-card {
  text-align: left; border: 1px solid var(--border-card); border-radius: 10px; background: #fff;
  padding: 0; overflow: hidden; cursor: pointer; font-family: inherit;
  display: flex; flex-direction: column; transition: border-color 0.15s, box-shadow 0.15s;
}
.mmm-card:hover { border-color: var(--cbm-red-400); }
.mmm-card-sel { border-color: #c8102e; box-shadow: 0 0 0 2px rgba(200, 16, 46, 0.2); }
.mmm-card-head { background: #121d3d; color: #fff; font-weight: 700; font-size: 12.5px; padding: 10px 12px; line-height: 1.3; }
.mmm-card-list { margin: 0; padding: 10px 12px 12px 26px; font-size: 12px; color: var(--text-secondary); }
.mmm-card-list li { margin-bottom: 3px; }
.mmm-empty { font-style: italic; color: var(--text-muted); padding: 10px 12px; font-size: 12px; }
```

- [ ] **Step 3: Verify build**

Run: `npm run build`
Expected: build conclui sem erros.

- [ ] **Step 4: Commit**

```bash
git add src/components/MinutaMindMap.jsx src/index.css
git commit -m "feat(diagramas): componente MinutaMindMap (cartões por capítulo)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: Página `MinutaDiagrams.jsx` + rota + navegação

**Files:**
- Create: `src/pages/MinutaDiagrams.jsx`
- Modify: `src/App.jsx`

- [ ] **Step 1: Create the page**

Create `src/pages/MinutaDiagrams.jsx`:

```jsx
import { useState, useEffect } from 'react'
import { Printer, X, Network, LayoutGrid } from 'lucide-react'
import MinutaOrgChart from '../components/MinutaOrgChart.jsx'
import MinutaMindMap from '../components/MinutaMindMap.jsx'

// Badge de fonte (RO não recebe badge); espelha o padrão do MinutaWizard.
function srcBadge(source) {
  if (!source || source === 'ro') return null
  return (
    <span style={{
      marginLeft: 6, fontSize: 11, fontFamily: 'Inter, sans-serif',
      color: '#fff', background: '#c8102e', borderRadius: 4, padding: '1px 6px',
    }}>{source}</span>
  )
}

function panelSections(ch) {
  if (ch.kind === 'organ') return ch.sections || []
  if (ch.kind === 'articles') return ch.articles || []
  return [{ sectionTitle: null, caput: null, items: [], proposedText: ch.proposedText }]
}

function MinutaDetailPanel({ chapter, onClose }) {
  const sections = panelSections(chapter)
  return (
    <aside className="md-panel no-print">
      <div className="md-panel-head">
        <span>{chapter.chapterTitle}</span>
        <button type="button" className="md-panel-close" onClick={onClose} aria-label="Fechar">
          <X size={16} />
        </button>
      </div>
      <div className="md-panel-body">
        {sections.map((s, i) => {
          const items = (s.items || []).filter(it => (it.text || '').trim())
          return (
            <div key={i} className="md-panel-sec">
              {s.sectionTitle && <h4>{s.sectionTitle}</h4>}
              {s.caput && <p className="md-caput">{s.caput}</p>}
              {items.length ? (
                <ul>
                  {items.map((it, j) => <li key={j}>{it.text}{srcBadge(it.source)}</li>)}
                </ul>
              ) : s.proposedText ? (
                <p className="md-prose">{s.proposedText}</p>
              ) : null}
            </div>
          )
        })}
      </div>
    </aside>
  )
}

const VIEW_LABEL = { org: 'Organograma — cadeia de comando', mind: 'Mapa mental — estrutura do documento' }

export default function MinutaDiagrams() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [view, setView] = useState('org')
  const [selected, setSelected] = useState(null)

  useEffect(() => {
    fetch('/database/minuta_structure.json')
      .then(r => { if (!r.ok) throw new Error(r.status); return r.json() })
      .then(setData)
      .catch(() => setError('Erro ao carregar minuta_structure.json. Execute build_minuta_structure.py.'))
      .finally(() => setLoading(false))
  }, [])

  const header = (
    <div className="page-header">
      <div className="page-header-left">
        <h2 className="page-title">Diagramas da Minuta</h2>
        <p className="page-subtitle">
          Organograma da cadeia de comando operacional e mapa mental da estrutura do
          documento da Minuta de Regimento Interno do CBMRO.
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
      <p style={{ color: '#c8102e' }}>{error || 'Sem dados.'}</p></div></>)
  }
  if (!data.commandChart) {
    return (<>{header}<div className="page-body" style={{ padding: 32 }}>
      <p style={{ color: '#c8102e' }}>
        Campo <code>commandChart</code> ausente no minuta_structure.json. Execute
        <code> python scripts/build_minuta_structure.py</code>.</p></div></>)
  }

  const selectedChapter = selected ? data.chapters.find(c => c.id === selected) : null

  return (
    <>
      {header}
      <div className="page-body">
        <div className="print-only-title">Diagramas da Minuta — {VIEW_LABEL[view]}</div>

        <div className="md-controls no-print">
          <div className="md-segmented">
            <button
              type="button"
              className={`md-seg${view === 'org' ? ' active' : ''}`}
              onClick={() => { setView('org'); setSelected(null) }}
            ><Network size={15} /> Organograma</button>
            <button
              type="button"
              className={`md-seg${view === 'mind' ? ' active' : ''}`}
              onClick={() => { setView('mind'); setSelected(null) }}
            ><LayoutGrid size={15} /> Mapa mental</button>
          </div>
          <button type="button" className="btn btn-ghost btn-sm" onClick={() => window.print()}>
            <Printer size={15} style={{ verticalAlign: -2, marginRight: 4 }} /> Imprimir / PDF
          </button>
        </div>

        <div className="md-layout">
          <div className="md-diagram">
            {view === 'org' ? (
              <MinutaOrgChart chart={data.commandChart} onSelect={setSelected} selectedId={selected} />
            ) : (
              <MinutaMindMap chapters={data.chapters} onSelect={setSelected} selectedId={selected} />
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

- [ ] **Step 2: Register import, NAV item and route in App.jsx**

Em `src/App.jsx`, no import de ícones do `lucide-react`, acrescente `Network`:

```jsx
import {
  Flame, LayoutDashboard, BookOpen, GitCompare,
  Search, Library, ScrollText, Menu, X, Network
} from 'lucide-react'
```

Acrescente o import da página (após o import de `MinutaWizard`):

```jsx
import MinutaDiagrams from './pages/MinutaDiagrams.jsx'
```

No array `NAV`, adicione o item logo após o de "Minuta RI":

```jsx
  { to: '/minuta', icon: ScrollText, label: 'Minuta RI' },
  { to: '/minuta-diagramas', icon: Network, label: 'Diagramas da Minuta' },
```

Na lista de `<Routes>`, adicione a rota após a de `/minuta`:

```jsx
          <Route path="/minuta" element={<MinutaWizard />} />
          <Route path="/minuta-diagramas" element={<MinutaDiagrams />} />
```

- [ ] **Step 3: Add page/panel CSS**

Em `src/index.css`, logo após o bloco `.mmm-*` da Task 3, adicione:

```css
/* ── Página Diagramas da Minuta: controles, layout e painel ── */
.md-controls { display: flex; flex-wrap: wrap; align-items: center; gap: 12px; margin-bottom: 16px; }
.md-segmented { display: inline-flex; border: 1px solid var(--border-card); border-radius: 8px; overflow: hidden; background: #fff; }
.md-seg {
  display: inline-flex; align-items: center; gap: 6px; padding: 7px 14px; border: none;
  background: #fff; color: var(--text-secondary); cursor: pointer; font-size: 13px; font-family: inherit;
}
.md-seg + .md-seg { border-left: 1px solid var(--border-card); }
.md-seg.active { background: #121d3d; color: #fff; }

.md-layout { display: flex; gap: 18px; align-items: flex-start; }
.md-diagram { flex: 1; min-width: 0; }
.md-panel {
  flex: 0 0 340px; position: sticky; top: 16px; max-height: 82vh; overflow: auto;
  border: 1px solid var(--border-card); border-radius: 10px; background: #fff;
}
.md-panel-head {
  display: flex; align-items: flex-start; justify-content: space-between; gap: 8px;
  background: #121d3d; color: #fff; font-weight: 700; font-size: 13px; padding: 12px 14px; line-height: 1.3;
}
.md-panel-close { border: none; background: transparent; color: #fff; cursor: pointer; padding: 0; flex-shrink: 0; }
.md-panel-body { padding: 12px 14px; font-size: 13px; color: var(--text-primary); }
.md-panel-sec { margin-bottom: 14px; }
.md-panel-sec h4 { margin: 0 0 4px; font-size: 12.5px; color: #c8102e; }
.md-caput { margin: 0 0 4px; font-weight: 600; }
.md-panel-sec ul { margin: 0; padding-left: 20px; }
.md-panel-sec li { margin-bottom: 4px; line-height: 1.5; }
.md-prose { margin: 0; line-height: 1.55; }

@media (max-width: 900px) {
  .md-layout { flex-direction: column; }
  .md-panel { flex: 1 1 auto; width: 100%; position: static; max-height: none; }
}
```

- [ ] **Step 4: Manual verification on the dev server**

Run: `npm run dev -- --port 5173 --strictPort`
Abra http://localhost:5173/minuta-diagramas e verifique:
- O item "Diagramas da Minuta" aparece no menu lateral e a rota carrega.
- Visão **Organograma**: a raiz vermelha "Subcomandante-Geral" no topo; DPO/DOE abaixo; COT→CAT, CRBM→(BBM, CIBM), BBM→GBM→Guarnição; DOE→(BBS, BIFEA, BOA). Linhas conectando as caixas.
- Clicar numa caixa (ex.: DPO) abre o painel com Finalidade/Competência e badges de fonte; o ✕ fecha.
- Alternar para **Mapa mental**: 15 cartões; clicar num cartão abre o mesmo painel.
- O toggle limpa a seleção ao trocar de visão.

- [ ] **Step 5: Commit**

```bash
git add src/pages/MinutaDiagrams.jsx src/App.jsx src/index.css
git commit -m "feat(diagramas): página Diagramas da Minuta (toggle, painel, rota, nav)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: Impressão / PDF (`@media print`)

**Files:**
- Modify: `src/index.css` (bloco `@media print`)

- [ ] **Step 1: Add print rules**

Em `src/index.css`, no FINAL do arquivo, adicione um novo bloco `@media print` (os seletores globais já ocultam `.sidebar`, `.app-header`, `.page-header`, `.btn`, `input`, `select` e `.no-print`; aqui só ajustamos o layout dos diagramas):

```css
/* ── Impressão: Diagramas da Minuta ── */
@media print {
  .md-layout { display: block !important; }
  .md-controls, .md-panel { display: none !important; }
  .moc-tree { overflow: visible !important; }
  .moc-box, .mmm-card { break-inside: avoid !important; page-break-inside: avoid !important; }
  .mmm-grid { grid-template-columns: repeat(2, 1fr) !important; }
  .mmm-card-head, .mmm-card-list { color: #1a1a1a !important; }
  .mmm-card-head { background: #e7ebf3 !important; }
}
```

- [ ] **Step 2: Manual verification of print**

Com o dev server rodando (`npm run dev -- --port 5173 --strictPort`), em http://localhost:5173/minuta-diagramas:
- Na visão Organograma, acione **Imprimir / PDF** (ou Ctrl+P). No diálogo, escolha **Paisagem**.
- Confirme na pré-visualização: título "Diagramas da Minuta — Organograma…" centralizado; menu/cabeçalho/controles/painel ocultos; só o organograma aparece, caixas inteiras (sem quebrar no meio).
- Repita na visão Mapa mental: cartões em 2 colunas, cabeçalhos legíveis.

- [ ] **Step 3: Commit**

```bash
git add src/index.css
git commit -m "feat(diagramas): impressão/PDF dos diagramas em paisagem

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: Documentação (CLAUDE.md)

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Update the build_minuta_structure.py command note**

Em `CLAUDE.md`, na seção "Comandos", localize a linha do `build_minuta_structure.py`:

```
python scripts/build_minuta_structure.py   # database/organs_detail/ro.json + minuta_enrichment.py -> database/minuta_structure.json (wizard /minuta)
```

Substitua por:

```
python scripts/build_minuta_structure.py   # database/organs_detail/ro.json + minuta_enrichment.py -> database/minuta_structure.json (wizard /minuta + commandChart p/ /minuta-diagramas)
```

- [ ] **Step 2: Add the route and page to the frontend docs**

Em `CLAUDE.md`, na seção "Frontend (React)", na linha que lista as rotas, acrescente a nova rota. Localize:

```
  `/busca` (Search), `/minuta` (MinutaWizard).
```

Substitua por:

```
  `/busca` (Search), `/minuta` (MinutaWizard), `/minuta-diagramas` (MinutaDiagrams).
```

E adicione, ao final da subseção do Wizard de Minuta (após o parágrafo sobre `MinutaWizard.jsx`), um novo parágrafo:

```
### Diagramas da Minuta (`/minuta-diagramas`)
Página que apresenta dois diagramas da minuta, lendo o mesmo `minuta_structure.json`:
- **Organograma** (`src/components/MinutaOrgChart.jsx`) — cadeia de comando dos 12 órgãos,
  caixas-e-linhas em CSS puro (sem lib), a partir do campo `commandChart` gerado por
  `build_minuta_structure.py` (árvore derivada de `subordinadoA` no `ro.json`; GBM sob BBM e
  Guarnição sob GBM por colocação padrão em `COMMAND_PARENT_OVERRIDE`).
- **Mapa mental** (`src/components/MinutaMindMap.jsx`) — grade de cartões, um por capítulo.
Ambos clicáveis: abrem um painel lateral com as seções/competências do capítulo. Exporta via
`window.print()` (`@media print`, Paisagem), ocultando navegação/controles/painel.
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: registra commandChart e página /minuta-diagramas no CLAUDE.md

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Self-Review Notes

- **Spec coverage:** rota+nav (Task 4) ✓; pipeline `commandChart` com colocações GBM→BBM, Guarnição→GBM (Task 1) ✓; org chart caixas-e-linhas sem lib (Task 2) ✓; mapa mental em cartões (Task 3) ✓; clique→painel de detalhe com badges de fonte (Task 4) ✓; impressão/PDF paisagem (Task 5) ✓; estados loading/erro + `commandChart` ausente (Task 4) ✓; docs (Task 6) ✓.
- **Type consistency:** nós do `commandChart` usam `{organKey, sigla, label, chapterId, children}` e raiz `{label, synthetic, children}` de forma idêntica no Python (Task 1), no `MinutaOrgChart` (Task 2) e no teste (Task 1). `chapterId` casa com `chapter.id` (`organ:<key>`) usado no lookup do painel (Task 4).
- **Sem placeholders:** todo passo de código traz o código completo.
