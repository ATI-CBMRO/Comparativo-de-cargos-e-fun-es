import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Flame, BookOpen, FileText, GitCompare, MapPin, ListTree
} from 'lucide-react'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'

function StatCard({ accent, icon: Icon, iconBg, iconColor, label, value, desc }) {
  return (
    <div className={`stat-card ${accent}`}>
      <div className="stat-card-top">
        <div className="stat-card-icon" style={{ background: iconBg }}>
          <Icon size={18} color={iconColor} />
        </div>
        <span className="stat-label">{label}</span>
      </div>
      <span className="stat-value">{value}</span>
      <span className="stat-desc">{desc}</span>
    </div>
  )
}

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    fetchJson('/database/states_data.json')
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) return <LoadingState label="Carregando base de dados..." />

  if (!data) {
    return (
      <ErrorState
        title="Base de dados não encontrada"
        hint={<>Execute <code>python scripts/build_states_data.py</code> para gerar os dados estruturados.</>}
      />
    )
  }

  const { metadata, states } = data

  const withRegimento = states.filter(s => s.stats?.has_regimento).length
  const withNGA = states.filter(s => s.stats?.has_nga).length
  const curated = states.filter(s => s.stats?.curated).length

  return (
    <>
      {/* Barra de seção */}
      <div className="section-bar">
        <div className="section-bar-label">
          Corpos de Bombeiros Militares — Estrutura Organizacional
        </div>
      </div>

      <div className="page-body">
        {/* Hero card navy */}
        <div className="hero-card" style={{ marginBottom: 24 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 22, position: 'relative', zIndex: 1, flexWrap: 'wrap' }}>
            <div style={{
              width: 64, height: 64, background: 'var(--cbm-red-700)', borderRadius: 'var(--radius-lg)',
              display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
              boxShadow: 'var(--shadow-red)'
            }}>
              <Flame size={30} color="#fff" />
            </div>
            <div style={{ flex: 1, minWidth: 280 }}>
              <h1 style={{ fontFamily: 'Outfit', fontSize: 28, fontWeight: 900, color: '#fff', letterSpacing: '-0.5px', lineHeight: 1.15 }}>
                Portal de Legislação dos Corpos de Bombeiros Militares
              </h1>
              <p style={{ color: '#aeb9d6', fontSize: 14, marginTop: 10, maxWidth: 640, lineHeight: 1.6 }}>
                Levantamento comparativo das estruturas organizacionais — comandos, diretorias,
                órgãos e cargos — de {metadata.total_states} Corpos de Bombeiros Militares,
                com base em Leis de Organização Básica, Regimentos Internos e Normas Gerais de Ação.
              </p>
              <div style={{ display: 'flex', gap: 12, marginTop: 18, flexWrap: 'wrap' }}>
                <button className="btn btn-primary" onClick={() => navigate('/estados')}>
                  <BookOpen size={16} /> Ver Estados
                </button>
                <button className="btn btn-ghost" onClick={() => navigate('/comparar')}>
                  <GitCompare size={16} /> Comparar
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Stat cards */}
        <div className="grid-4" style={{ marginBottom: 24 }}>
          <StatCard
            accent="" icon={MapPin} iconBg="rgba(37,99,235,0.10)" iconColor="var(--accent-blue)"
            label="Total" value={metadata.total_states} desc="Estados analisados"
          />
          <StatCard
            accent="red" icon={FileText} iconBg="rgba(200,16,46,0.10)" iconColor="var(--cbm-red-700)"
            label="Documentos" value={metadata.total_documents} desc="LOBs, Regimentos e NGAs"
          />
          <StatCard
            accent="green" icon={ListTree} iconBg="rgba(22,163,74,0.10)" iconColor="var(--accent-green)"
            label="Detalhamento" value={curated} desc="Organogramas curados"
          />
          <StatCard
            accent="gold" icon={BookOpen} iconBg="rgba(245,166,35,0.14)" iconColor="var(--cbm-gold-500)"
            label="Regimentos" value={withRegimento} desc="Estados com Regimento Interno"
          />
        </div>

        {/* Tipos de Documento */}
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="card-header">
            <span className="card-title">Tipos de Documento</span>
            <FileText size={18} color="var(--text-muted)" />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {[
              { label: 'Lei de Organização Básica', value: metadata.total_states, color: 'var(--cbm-red-700)' },
              { label: 'Regimento Interno', value: withRegimento, color: 'var(--cbm-gold-400)' },
              { label: 'Normas Gerais de Ação (NGA)', value: withNGA, color: 'var(--accent-orange)' },
              { label: 'Quadros / Outros', value: Math.max(0, metadata.total_documents - metadata.total_states - withRegimento - withNGA), color: 'var(--accent-blue)' },
            ].map(item => (
              <div key={item.label} style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <span style={{ width: 10, height: 10, borderRadius: '50%', background: item.color, flexShrink: 0 }} />
                <span style={{ flex: 1, fontSize: 13, color: 'var(--text-secondary)' }}>{item.label}</span>
                <span style={{ fontSize: 14, fontWeight: 700, color: 'var(--navy-900)', fontFamily: 'Outfit' }}>{item.value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}
