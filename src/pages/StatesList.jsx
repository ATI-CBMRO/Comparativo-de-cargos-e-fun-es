import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChevronRight } from 'lucide-react'
import { fetchJson } from '../lib/dataCache.js'

export default function StatesList() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchJson('/database/states_data.json')
      .then(setData)
      .catch(() => setError('Não foi possível carregar a base de dados. Recarregue a página.'))
  }, [])

  if (error) return (
    <div className="empty-state" style={{ marginTop: 80 }}>
      <h3>Erro ao carregar</h3>
      <p>{error}</p>
    </div>
  )

  if (!data) return (
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
      <div className="spinner" />
    </div>
  )

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h1 className="page-title">Legislações Estaduais</h1>
          <p className="page-subtitle">{data.states.length} Corpos de Bombeiros Militares — {data.metadata.total_documents} documentos legais</p>
        </div>
      </div>

      <div className="page-body">
        {/* Grid de estados */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: 14 }}>
          {data.states.map(s => (
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
      </div>
    </>
  )
}
