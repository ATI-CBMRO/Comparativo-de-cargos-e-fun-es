import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchJson } from '../lib/dataCache.js'
import { buildCoverageRows } from '../lib/acervoCoverage.js'
import AcervoCoverageTable from '../components/AcervoCoverageTable.jsx'

export default function Legislations() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    fetchJson('/database/states_data.json')
      .then(setData)
      .catch(() => setError('Não foi possível carregar a base de dados. Recarregue a página.'))
  }, [])

  const coverageRows = useMemo(() => buildCoverageRows(data?.states), [data])
  const totalDocs = useMemo(
    () => (data?.states || []).reduce((acc, s) => acc + (s.documents?.length || 0), 0),
    [data],
  )

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
          <h1 className="page-title">Acervo Legal</h1>
          <p className="page-subtitle">
            {totalDocs} legislações de {data.states.length} Corpos de Bombeiros Militares, organizadas por estado
          </p>
        </div>
      </div>

      <div className="page-body">
        <AcervoCoverageTable
          rows={coverageRows}
          onSelectState={id => navigate(`/estados/${id}`)}
        />
      </div>
    </>
  )
}
