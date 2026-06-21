import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Flame, BookOpen, FileText, Map, GitCompare, MapPin,
  TrendingUp, Shield, ChevronRight, Award, ListTree
} from 'lucide-react'

const REGION_LABELS = {
  Norte: { css: 'norte', count: 0 },
  Nordeste: { css: 'nordeste', count: 0 },
  'Centro-Oeste': { css: 'centroeste', count: 0 },
  Sudeste: { css: 'sudeste', count: 0 },
  Sul: { css: 'sul', count: 0 },
}

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
    fetch('/database/states_data.json')
      .then(r => r.json())
      .then(d => { setData(d); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh', flexDirection: 'column', gap: 16 }}>
        <div className="spinner" />
        <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>Carregando base de dados...</p>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="empty-state" style={{ marginTop: 80 }}>
        <Flame size={48} className="empty-state-icon" />
        <h3>Base de dados não encontrada</h3>
        <p>Execute <code>python scripts/build_states_data.py</code> para gerar os dados estruturados.</p>
      </div>
    )
  }

  const { metadata, states } = data

  const byRegion = JSON.parse(JSON.stringify(REGION_LABELS))
  states.forEach(s => { if (byRegion[s.region]) byRegion[s.region].count++ })
  const maxRegion = Math.max(...Object.values(byRegion).map(r => r.count), 1)

  const withRegimento = states.filter(s => s.stats?.has_regimento).length
  const withNGA = states.filter(s => s.stats?.has_nga).length
  const curated = states.filter(s => s.stats?.curated).length
  const numRegions = Object.values(byRegion).filter(r => r.count > 0).length

  const topByDocs = [...states].sort(
    (a, b) => (b.stats?.total_chars || 0) - (a.stats?.total_chars || 0)
  ).slice(0, 5)

  return (
    <>
      {/* Barra de seção (breadcrumb + badge) */}
      <div className="section-bar">
        <div className="section-bar-label">
          Corpos de Bombeiros Militares — Estrutura Organizacional
        </div>
        <span className="section-bar-badge">
          <TrendingUp size={13} color="var(--cbm-red-700)" />
          {metadata.total_states} estados analisados
        </span>
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
            accent="gold" icon={Map} iconBg="rgba(245,166,35,0.14)" iconColor="var(--cbm-gold-500)"
            label="Regiões" value={numRegions} desc="Regiões representadas"
          />
        </div>

        <div className="grid-2" style={{ marginBottom: 24, gap: 20 }}>
          {/* Cobertura por Região */}
          <div className="card">
            <div className="card-header">
              <span className="card-title">Cobertura por Região</span>
              <Map size={18} color="var(--text-muted)" />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {Object.entries(byRegion).map(([region, info]) => (
                <div key={region} style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <span className={`region-chip region-${info.css}`} style={{ minWidth: 96 }}>{region}</span>
                  <div style={{ flex: 1, height: 7, background: 'var(--track)', borderRadius: 4, overflow: 'hidden' }}>
                    <div style={{ height: '100%', width: `${(info.count / maxRegion) * 100}%`, background: 'var(--cbm-red-700)', borderRadius: 4, transition: 'width 0.5s ease' }} />
                  </div>
                  <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--navy-900)', minWidth: 20, textAlign: 'right' }}>{info.count}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Tipos de Documento */}
          <div className="card">
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

        {/* Maior volume documental */}
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="card-header">
            <span className="card-title">Maior Volume Documental</span>
            <TrendingUp size={18} color="var(--text-muted)" />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {topByDocs.map((s, i) => {
              const chars = s.stats?.total_chars || 0
              const maxChars = topByDocs[0]?.stats?.total_chars || 1
              return (
                <div
                  key={s.id}
                  style={{ display: 'flex', alignItems: 'center', gap: 14, cursor: 'pointer', padding: '8px 4px', borderRadius: 'var(--radius-md)', transition: 'background 0.15s' }}
                  onClick={() => navigate(`/estados/${s.id}`)}
                  onMouseEnter={e => e.currentTarget.style.background = 'var(--gray-50)'}
                  onMouseLeave={e => e.currentTarget.style.background = ''}
                >
                  <span style={{ width: 22, height: 22, borderRadius: '50%', background: i === 0 ? 'var(--cbm-gold-400)' : 'var(--gray-200)', color: i === 0 ? '#fff' : 'var(--gray-600)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 11, fontWeight: 700, flexShrink: 0 }}>
                    {i + 1}
                  </span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                      <span style={{ fontWeight: 700, fontSize: 13, color: 'var(--text-primary)' }}>{s.name}</span>
                      <span className={`region-chip region-${REGION_LABELS[s.region]?.css || 'norte'}`}>{s.abbreviation}</span>
                    </div>
                    <div style={{ height: 6, background: 'var(--track)', borderRadius: 4, overflow: 'hidden' }}>
                      <div style={{ height: '100%', width: `${(chars / maxChars) * 100}%`, background: i === 0 ? 'var(--cbm-gold-400)' : 'var(--cbm-red-700)', borderRadius: 4 }} />
                    </div>
                  </div>
                  <span style={{ fontSize: 12, color: 'var(--text-muted)', whiteSpace: 'nowrap' }}>{(chars / 1000).toFixed(0)}k chars</span>
                  <ChevronRight size={16} color="var(--gray-400)" />
                </div>
              )
            })}
          </div>
        </div>

        {/* Acesso rápido por estado */}
        <div className="section-heading">
          <BookOpen size={14} />
          Acesso Rápido por Estado
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: 12 }}>
          {states.map(s => (
            <div key={s.id} className="state-card" onClick={() => navigate(`/estados/${s.id}`)}>
              <div className="state-card-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <div className="state-initials">{s.abbreviation}</div>
                  <div>
                    <div className="state-name">{s.name}</div>
                    <div className="state-cbm-name">{s.cbm_abbreviation}</div>
                  </div>
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span className={`region-chip region-${REGION_LABELS[s.region]?.css || 'norte'}`}>{s.region}</span>
                <div style={{ display: 'flex', gap: 4 }}>
                  <span className="badge badge-gray" style={{ fontSize: 10 }}>
                    {s.stats?.total_documents} doc{s.stats?.total_documents !== 1 ? 's' : ''}
                  </span>
                  {s.stats?.curated && <span className="badge badge-gold" style={{ fontSize: 10 }}>Curado</span>}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  )
}
