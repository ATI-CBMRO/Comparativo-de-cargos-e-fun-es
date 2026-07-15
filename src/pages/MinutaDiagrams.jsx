import { useState, useEffect } from 'react'
import { Printer, X, Network, LayoutGrid, ChevronsDownUp, ChevronsUpDown } from 'lucide-react'
import MinutaOrgChart from '../components/MinutaOrgChart.jsx'
import MinutaMindMap from '../components/MinutaMindMap.jsx'
import { fetchJson } from '../lib/dataCache.js'
import { useScenario } from '../context/ScenarioContext.jsx'
import { scenarioDbUrl } from '../lib/scenario.js'

// Badge de fonte (RO não recebe badge); espelha o padrão do MinutaWizard.
// whiteSpace:nowrap + inline-block mantêm a citação inteira numa linha só
// (quebra como um bloco, em vez de partir "cf." do resto).
function srcBadge(source) {
  if (!source || source === 'ro') return null
  return (
    <span style={{
      marginLeft: 6, fontSize: 11, fontFamily: 'Inter, sans-serif', fontWeight: 600,
      color: '#fff', background: 'var(--cbm-red-700)', borderRadius: 4, padding: '1px 6px',
      whiteSpace: 'nowrap', display: 'inline-block', verticalAlign: 'baseline',
    }}>{source}</span>
  )
}

// Inicial maiúscula para exibição (itens verbatim começam em minúscula).
function capitalizeFirst(text) {
  const t = (text || '').trim()
  return t ? t.charAt(0).toUpperCase() + t.slice(1) : t
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
                  {items.map((it, j) => <li key={j}>{capitalizeFirst(it.text)}{srcBadge(it.source)}</li>)}
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
    fetchJson(scenarioDbUrl(cenario, 'minuta_structure.json'))
      .then(setData)
      .catch(() => setError('Erro ao carregar minuta_structure.json. Execute build_minuta_structure.py.'))
      .finally(() => setLoading(false))
  }, [cenario])

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
      <p style={{ color: 'var(--cbm-red-700)' }}>{error || 'Sem dados.'}</p></div></>)
  }
  if (!data.commandChart) {
    return (<>{header}<div className="page-body" style={{ padding: 32 }}>
      <p style={{ color: 'var(--cbm-red-700)' }}>
        Campo <code>commandChart</code> ausente no minuta_structure.json. Execute
        <code> python scripts/build_minuta_structure.py</code>.</p></div></>)
  }

  const selectedChapter = selected ? data.chapters.find(c => c.id === selected) : null

  return (
    <>
      {header}
      <div className="page-body">
        <div className="print-only-title" style={{ display: 'none' }}>Diagramas da Minuta — {VIEW_LABEL[view]}</div>

        <div className="md-controls no-print">
          <div className="md-segmented">
            <button
              type="button"
              className={`md-seg${view === 'org' ? ' active' : ''}`}
              onClick={() => { setView('org'); setSelected(null); setTree(false) }}
            ><Network size={15} /> Organograma</button>
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
              <MinutaOrgChart key={treeKey} chart={data.commandChart} onSelect={setSelected} selectedId={selected} defaultExpanded={expandAll} />
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
