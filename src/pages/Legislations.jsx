import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, Filter, FileText, Library, ChevronRight, ExternalLink } from 'lucide-react'

const REGIONS = ['Todos', 'Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']

const DOC_TYPE_SHORT = {
  'Lei de Organização Básica': 'LOB',
  'Regimento Interno': 'Regimento',
  'Normas Gerais de Ação': 'NGA',
  'Quadro Demonstrativo de Cargos': 'QDC',
  'Quadro de Organização e Distribuição': 'QOD',
}

const REGION_CSS = {
  Norte: 'norte', Nordeste: 'nordeste', 'Centro-Oeste': 'centroeste',
  Sudeste: 'sudeste', Sul: 'sul'
}

export default function Legislations() {
  const [data, setData] = useState(null)
  const [query, setQuery] = useState('')
  const [regionFilter, setRegionFilter] = useState('Todos')
  const [typeFilter, setTypeFilter] = useState('Todos')
  const navigate = useNavigate()

  useEffect(() => {
    fetch('/database/states_data.json')
      .then(r => r.json())
      .then(setData)
  }, [])

  // Achata todos os documentos de todos os estados em uma única lista
  const allDocs = useMemo(() => {
    if (!data) return []
    const docs = []
    for (const s of data.states) {
      for (const doc of (s.documents || [])) {
        docs.push({
          ...doc,
          stateId: s.id,
          stateName: s.name,
          abbreviation: s.abbreviation,
          cbm_name: s.cbm_name,
          cbm_abbreviation: s.cbm_abbreviation,
          region: s.region,
        })
      }
    }
    return docs.sort((a, b) => a.stateName.localeCompare(b.stateName, 'pt-BR'))
  }, [data])

  const docTypes = useMemo(() => {
    const set = new Set(allDocs.map(d => d.type))
    return ['Todos', ...Array.from(set).sort((a, b) => a.localeCompare(b, 'pt-BR'))]
  }, [allDocs])

  if (!data) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
      <div className="spinner" />
    </div>
  )

  const q = query.trim().toLowerCase()
  const filtered = allDocs.filter(d => {
    const matchQuery = !q
      || d.stateName.toLowerCase().includes(q)
      || d.cbm_abbreviation?.toLowerCase().includes(q)
      || d.cbm_name?.toLowerCase().includes(q)
      || d.type?.toLowerCase().includes(q)
      || d.laws?.some(l => `${l.tipo} ${l.numero}`.toLowerCase().includes(q))
    const matchRegion = regionFilter === 'Todos' || d.region === regionFilter
    const matchType = typeFilter === 'Todos' || d.type === typeFilter
    return matchQuery && matchRegion && matchType
  })

  const totalChars = filtered.reduce((acc, d) => acc + (d.char_count || 0), 0)

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h1 className="page-title">Acervo Legal</h1>
          <p className="page-subtitle">
            {allDocs.length} legislações de {data.states.length} Corpos de Bombeiros Militares em um único índice
          </p>
        </div>
      </div>

      <div className="page-body">
        {/* Filtros */}
        <div style={{ display: 'flex', gap: 12, marginBottom: 16, flexWrap: 'wrap', alignItems: 'center' }}>
          <div className="search-input-wrap" style={{ flex: 1, minWidth: 240 }}>
            <Search size={16} className="search-input-icon" />
            <input
              className="search-input"
              placeholder="Buscar por estado, sigla, tipo de documento ou número da lei..."
              value={query}
              onChange={e => setQuery(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {REGIONS.map(r => (
              <button
                key={r}
                className={`btn btn-sm ${regionFilter === r ? 'btn-primary' : 'btn-ghost'}`}
                onClick={() => setRegionFilter(r)}
              >
                {r}
              </button>
            ))}
          </div>
        </div>

        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 16, alignItems: 'center' }}>
          <Filter size={16} color="var(--text-muted)" style={{ alignSelf: 'center' }} />
          {docTypes.map(t => (
            <button
              key={t}
              className={`btn btn-sm ${typeFilter === t ? 'btn-outline-red' : 'btn-ghost'}`}
              onClick={() => setTypeFilter(t)}
            >
              {t === 'Todos' ? 'Todos os tipos' : (DOC_TYPE_SHORT[t] || t)}
            </button>
          ))}
        </div>

        <p style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 16 }}>
          Exibindo {filtered.length} de {allDocs.length} legislações · {(totalChars / 1000).toFixed(0)}k caracteres
        </p>

        {/* Tabela de legislações */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          {filtered.map((d, idx) => {
            const short = DOC_TYPE_SHORT[d.type] || d.type
            const isLob = d.type === 'Lei de Organização Básica'
            const pdfUrl = d.md_file
              ? `/legislacao-pdf/${encodeURIComponent(d.md_file.replace('.md', '.pdf'))}`
              : null
            return (
              <div
                key={`${d.stateId}-${idx}`}
                className="leg-row"
                style={{
                  display: 'flex', alignItems: 'center', gap: 14,
                  background: 'var(--bg-surface)', border: '1px solid var(--border-card)',
                  borderRadius: 'var(--radius-md)', padding: '12px 16px',
                }}
              >
                <div style={{
                  width: 40, height: 40, borderRadius: 'var(--radius-md)', flexShrink: 0,
                  background: isLob ? 'rgba(183,28,28,0.2)' : 'rgba(255,179,0,0.12)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                }}>
                  <FileText size={18} color={isLob ? 'var(--cbm-red-400)' : 'var(--cbm-gold-400)'} />
                </div>

                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                    {d.type}
                    {d.laws?.length > 0 && (
                      <span style={{ fontSize: 12, color: 'var(--cbm-gold-400)', fontWeight: 600 }}>
                        {d.laws.map(l => `${l.tipo} nº ${l.numero}`).join(' · ')}
                      </span>
                    )}
                  </div>
                  <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 2 }}>
                    <strong style={{ color: 'var(--cbm-red-400)' }}>{d.cbm_abbreviation}</strong>
                    {' · '}{d.cbm_name}
                    {d.year ? ` · ${d.year}` : ''}
                    {d.char_count ? ` · ${Math.round(d.char_count / 1000)}k car.` : ''}
                  </div>
                </div>

                <span className={`region-chip region-${REGION_CSS[d.region] || 'norte'}`} style={{ flexShrink: 0 }}>
                  {d.region}
                </span>
                <span className={`badge ${isLob ? 'badge-red' : 'badge-gold'}`} style={{ fontSize: 10, flexShrink: 0 }}>
                  {short}
                </span>

                {pdfUrl && (
                  <button
                    className="btn btn-sm btn-ghost"
                    style={{ flexShrink: 0 }}
                    onClick={() => window.open(pdfUrl, '_blank')}
                    title="Abrir o PDF oficial da legislação"
                  >
                    <ExternalLink size={14} /> PDF
                  </button>
                )}
                <button
                  className="btn btn-sm btn-ghost"
                  style={{ flexShrink: 0 }}
                  onClick={() => navigate(`/estados/${d.stateId}`)}
                  title="Abrir a página do estado"
                >
                  Estado <ChevronRight size={14} />
                </button>
              </div>
            )
          })}
        </div>

        {filtered.length === 0 && (
          <div className="empty-state">
            <Library size={40} className="empty-state-icon" />
            <h3>Nenhuma legislação encontrada</h3>
            <p>Tente ajustar os filtros de busca.</p>
          </div>
        )}
      </div>
    </>
  )
}
