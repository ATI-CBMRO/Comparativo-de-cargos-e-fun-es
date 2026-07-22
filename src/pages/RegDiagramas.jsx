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
