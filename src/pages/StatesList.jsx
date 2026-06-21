import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search, ChevronRight, BookOpen } from 'lucide-react'

export default function StatesList() {
  const [data, setData] = useState(null)
  const [query, setQuery] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetch('/database/states_data.json')
      .then(r => r.json())
      .then(setData)
  }, [])

  if (!data) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
      <div className="spinner" />
    </div>
  )

  const filtered = data.states.filter(s => (
    !query || s.name.toLowerCase().includes(query.toLowerCase())
    || s.cbm_abbreviation?.toLowerCase().includes(query.toLowerCase())
    || s.cbm_name?.toLowerCase().includes(query.toLowerCase())
  ))

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h1 className="page-title">Legislações Estaduais</h1>
          <p className="page-subtitle">{data.states.length} Corpos de Bombeiros Militares — {data.metadata.total_documents} documentos legais</p>
        </div>
      </div>

      <div className="page-body">
        {/* Busca */}
        <div className="search-input-wrap" style={{ marginBottom: 16 }}>
          <Search size={16} className="search-input-icon" />
          <input
            className="search-input"
            placeholder="Buscar estado ou sigla..."
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
        </div>

        <p style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 16 }}>
          Exibindo {filtered.length} de {data.states.length} corporações
        </p>

        {/* Grid de estados */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 14 }}>
          {filtered.map(s => (
            <div
              key={s.id}
              className="state-card"
              onClick={() => navigate(`/estados/${s.id}`)}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: 14 }}>
                <div className="state-initials" style={{ fontSize: 18 }}>{s.abbreviation}</div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div className="state-name">{s.name}</div>
                  <div className="state-cbm-name">{s.cbm_name}</div>
                  <div style={{ marginTop: 4 }}>
                    <span className="state-cbm-name" style={{ fontWeight: 700, color: 'var(--cbm-red-400)' }}>
                      {s.cbm_abbreviation}
                    </span>
                  </div>
                </div>
                <ChevronRight size={18} color="var(--cbm-gray-400)" style={{ flexShrink: 0, marginTop: 2 }} />
              </div>

              <div className="divider" style={{ margin: '10px 0' }} />

              <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                {s.documents?.map(doc => (
                  <span key={doc.md_file} className="badge badge-gray" style={{ fontSize: 10 }}>
                    {doc.type === 'Lei de Organização Básica' ? 'LOB' :
                     doc.type === 'Regimento Interno' ? 'Reg.' :
                     doc.type === 'Normas Gerais de Ação' ? 'NGA' :
                     doc.type === 'Quadro Demonstrativo de Cargos' ? 'QDC' :
                     doc.type === 'Quadro de Organização e Distribuição' ? 'QOD' : 'Doc.'}
                    {doc.year ? ` ${doc.year}` : ''}
                  </span>
                ))}

                {s.stats?.curated && (
                  <span className="badge badge-gold" style={{ fontSize: 10, marginLeft: 'auto' }}>
                    Organograma Curado
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>

        {filtered.length === 0 && (
          <div className="empty-state">
            <BookOpen size={40} className="empty-state-icon" />
            <h3>Nenhum resultado encontrado</h3>
            <p>Tente ajustar os filtros de busca.</p>
          </div>
        )}
      </div>
    </>
  )
}
