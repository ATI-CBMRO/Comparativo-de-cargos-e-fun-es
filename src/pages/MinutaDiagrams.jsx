import { useState, useEffect } from 'react'
import { Printer, Network, LayoutGrid, ChevronsDownUp, ChevronsUpDown } from 'lucide-react'
import MinutaOrgChart from '../components/MinutaOrgChart.jsx'
import MinutaMindMap from '../components/MinutaMindMap.jsx'
import MinutaDetailPanel from '../components/MinutaDetailPanel.jsx'
import { fetchJson } from '../lib/dataCache.js'
import { useScenario } from '../context/ScenarioContext.jsx'
import { scenarioDbUrl } from '../lib/scenario.js'

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
