import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  ChevronLeft, BookOpen, FileText,
  Building2, Scale, ListTree, Shield, Users, Info
} from 'lucide-react'
import Organogram from '../components/Organogram.jsx'
import OrgDetail from '../components/OrgDetail.jsx'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState } from '../components/Status.jsx'

const REGION_CSS = {
  Norte: 'norte', Nordeste: 'nordeste', 'Centro-Oeste': 'centroeste',
  Sudeste: 'sudeste', Sul: 'sul'
}

const DOC_TYPE_SHORT = {
  'Lei de Organização Básica': 'LOB',
  'Regimento Interno': 'Regimento',
  'Regimento de Serviços': 'Reg. Serviços',
  'Regulamento Geral': 'Regulamento',
  'Normas Gerais de Ação': 'NGA',
  'Quadro Demonstrativo de Cargos': 'QDC',
  'Quadro de Organização e Distribuição': 'QOD',
}

function InfoRow({ label, value }) {
  if (!value) return null
  return (
    <div style={{ display: 'flex', gap: 12, padding: '8px 0', borderBottom: '1px solid var(--border-subtle)' }}>
      <span style={{ fontSize: 12, color: 'var(--text-muted)', minWidth: 140, flexShrink: 0 }}>{label}</span>
      <span style={{ fontSize: 13, color: 'var(--text-primary)' }}>{value}</span>
    </div>
  )
}

function DocCard({ doc }) {
  const [hovered, setHovered] = useState(false)
  const short = DOC_TYPE_SHORT[doc.type] || doc.type
  const totalKb = doc.char_count ? Math.round(doc.char_count / 1000) : '?'
  
  const pdfUrl = doc.md_file && doc.has_pdf ? `/legislacao-pdf/${encodeURIComponent(doc.md_file.replace('.md', '.pdf'))}` : null

  return (
    <div
      style={{
        background: hovered ? 'var(--bg-card-hover)' : 'var(--bg-surface)',
        border: hovered ? '1px solid var(--cbm-red-400)' : '1px solid var(--border-card)',
        borderRadius: 'var(--radius-md)',
        padding: '14px 16px',
        display: 'flex', alignItems: 'flex-start', gap: 14,
        cursor: pdfUrl ? 'pointer' : 'default',
        transition: 'all 0.15s ease',
        transform: hovered ? 'translateY(-2px)' : 'none',
        boxShadow: hovered ? 'var(--shadow-md)' : 'var(--shadow-card)',
      }}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onClick={() => {
        if (pdfUrl) {
          window.open(pdfUrl, '_blank')
        }
      }}
      title={pdfUrl ? "Clique para abrir o arquivo PDF oficial da legislação" : ""}
    >
      <div style={{
        width: 40, height: 40, borderRadius: 'var(--radius-md)',
        background: doc.type === 'Lei de Organização Básica' ? 'rgba(183,28,28,0.2)' : 'rgba(255,179,0,0.12)',
        display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
      }}>
        <FileText size={18} color={doc.type === 'Lei de Organização Básica' ? 'var(--cbm-red-400)' : 'var(--cbm-gold-400)'} />
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)', marginBottom: 3, display: 'flex', alignItems: 'center', gap: 6 }}>
          {doc.type}
          {pdfUrl && (
            <span style={{ fontSize: 10, color: 'var(--text-muted)', fontWeight: 500 }}>
              (PDF ↗)
            </span>
          )}
        </div>
        {doc.laws?.length > 0 && (
          <div style={{ fontSize: 12, color: 'var(--cbm-gold-400)', marginBottom: 3, fontWeight: 600 }}>
            {doc.laws.map(l => `${l.tipo} nº ${l.numero}`).join(' · ')}
          </div>
        )}
        <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
          {doc.year ? `Ano: ${doc.year} · ` : ''}{totalKb}k caracteres extraídos
        </div>
        {doc.type !== 'Lei de Organização Básica' && (
          <div
            style={{ fontSize: 11, marginTop: 3, color: doc.typeVerified ? 'var(--success-text, #2e7d32)' : 'var(--text-muted)' }}
            title={doc.typeVerified
              ? 'O tipo deste documento foi conferido lendo o conteúdo de verdade, não só o nome do arquivo.'
              : 'Este tipo de documento ainda não foi conferido por conteúdo — a classificação é só pelo nome do arquivo, pode estar incorreta.'}
          >
            {doc.typeVerified ? '✓ tipo conferido por conteúdo' : '⚠ tipo só por nome de arquivo'}
          </div>
        )}
      </div>
      <span className={`badge ${doc.type === 'Lei de Organização Básica' ? 'badge-red' : 'badge-gold'}`} style={{ fontSize: 10, flexShrink: 0 }}>
        {short}
      </span>
    </div>
  )
}

export default function StateDetail() {
  const { stateId } = useParams()
  const navigate = useNavigate()
  const [state, setState] = useState(null)
  const [orgDetail, setOrgDetail] = useState(null)   // mapa id → detalhes ricos
  const [selectedOrgan, setSelectedOrgan] = useState(null)
  const [activeTab, setActiveTab] = useState('organograma')
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(false)

  useEffect(() => {
    fetchJson('/database/states_data.json')
      .then(data => {
        const found = data.states.find(s => s.id === stateId)
        setState(found || null)
        setLoading(false)
      })
      .catch((e) => {
        // Distingue "estado não existe" de "falha ao carregar a base" — antes os
        // dois caíam no mesmo "não encontrado" (auditoria 2026-07-23).
        console.error('Erro ao carregar states_data.json:', e)
        setLoadError(true)
        setLoading(false)
      })
  }, [stateId])

  // Tenta carregar dados de detalhe de órgãos para este estado (nem todo estado tem).
  useEffect(() => {
    fetchJson(`/database/organs_detail/${stateId}.json`, { optional: true })
      .then(data => {
        if (data?.organs) setOrgDetail(data.organs)
      })
      // Ausência esperada já volta null via optional:true — erro REAL não pode ser
      // engolido sem rastro (auditoria 2026-07-23).
      .catch((e) => console.error(`Erro ao carregar organs_detail/${stateId}.json:`, e))
  }, [stateId])

  function handleSelectOrgan(node) {
    if (!node) return
    // Resolve o detalhe: detailId carimbado no build > id > nome > sigla
    if (orgDetail) {
      const detail = (node.detailId && orgDetail[node.detailId])
        || orgDetail[node.id]
        || Object.values(orgDetail).find(o => o.name === node.name)
        || (node.abbreviation && Object.values(orgDetail).find(o => o.abbreviation === node.abbreviation))
      if (detail) {
        setSelectedOrgan(detail)
        return
      }
    }
    // Fallback: mostra os dados básicos do nó (sem cargos detalhados)
    setSelectedOrgan({
      id: node.id,
      name: node.name,
      abbreviation: node.abbreviation,
      category: node.category,
      description: node.description,
      legalRef: node.legalRef,
      atribuicoes: node.description ? [node.description] : [],
      desdobramentos: node.children?.map(c => c.name) || [],
      cargos: [],
    })
  }

  if (loading) return <LoadingState label="" />

  if (loadError) return (
    <div className="not-found" style={{ padding: 32 }}>
      <h3>Erro ao carregar a base de dados</h3>
      <p>Não foi possível carregar os dados dos estados (falha de conexão ou servidor). Recarregue a página.</p>
    </div>
  )
  if (!state) return (
    <div className="empty-state" style={{ marginTop: 80 }}>
      <Shield size={40} className="empty-state-icon" />
      <h3>Estado não encontrado</h3>
      <button className="btn btn-ghost" onClick={() => navigate('/estados')}>
        <ChevronLeft size={16} /> Voltar à lista
      </button>
    </div>
  )

  const TABS = [
    { id: 'organograma', label: 'Organograma', icon: ListTree },
    { id: 'documentos', label: 'Documentos', icon: FileText },
    { id: 'informacoes', label: 'Informações', icon: Info },
  ]

  const hasRichDetail = !!orgDetail && Object.keys(orgDetail).length > 0

  return (
    <>
      {/* Header */}
      <div className="hero-bar">
        <button className="back-btn" onClick={() => navigate('/estados')}>
          <ChevronLeft size={16} /> Voltar para a lista
        </button>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginTop: 12 }}>
          <div style={{
            width: 60, height: 60, background: 'var(--cbm-red-800)',
            borderRadius: 'var(--radius-lg)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontFamily: 'Outfit', fontWeight: 900, fontSize: 22, color: '#fff',
            flexShrink: 0, boxShadow: 'var(--shadow-red)',
          }}>
            {state.abbreviation}
          </div>
          <div>
            <h1 style={{ fontFamily: 'Outfit', fontSize: 24, fontWeight: 900, letterSpacing: '-0.4px' }}>
              {state.name}
            </h1>
            <p style={{ color: 'var(--cbm-gray-300)', fontSize: 14, marginTop: 2 }}>
              {state.cbm_name} · <strong style={{ color: 'var(--cbm-red-400)' }}>{state.cbm_abbreviation}</strong>
            </p>
            <div style={{ display: 'flex', gap: 8, marginTop: 8, flexWrap: 'wrap' }}>
              <span className={`region-chip region-${REGION_CSS[state.region] || 'norte'}`}>
                {state.region}
              </span>
              <span className="badge badge-gray" style={{ fontSize: 10 }}>
                {state.stats?.total_documents} documento{state.stats?.total_documents !== 1 ? 's' : ''}
              </span>
              {state.stats?.has_regimento && <span className="badge badge-gold" style={{ fontSize: 10 }}>Regimento Interno</span>}
              {state.stats?.has_nga && <span className="badge badge-gold" style={{ fontSize: 10 }}>NGA</span>}
              {state.stats?.curated && <span className="badge badge-green" style={{ fontSize: 10 }}>Organograma Curado</span>}
              {hasRichDetail && <span className="badge badge-gold" style={{ fontSize: 10 }}>Detalhamento Completo</span>}
            </div>
          </div>
        </div>
      </div>

      {/* Main layout — quando painel de detalhe está aberto, margem direita */}
      <div className="page-body" style={{ marginRight: selectedOrgan ? 540 : 0, transition: 'margin-right 0.3s ease' }}>
        {/* Tabs */}
        <div className="tabs" style={{ marginBottom: 20 }}>
          {TABS.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              className={`tab ${activeTab === id ? 'active' : ''}`}
              onClick={() => setActiveTab(id)}
            >
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <Icon size={14} /> {label}
              </span>
            </button>
          ))}
        </div>

        {/* ── TAB: Organograma ── */}
        {activeTab === 'organograma' && (
          <div>
            <div style={{ marginBottom: 16 }}>
              <h2 style={{ fontFamily: 'Outfit', fontSize: 17, fontWeight: 700, marginBottom: 4 }}>
                Estrutura Organizacional — {state.cbm_abbreviation}
              </h2>
              {state.stats?.curated ? (
                <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
                  Estrutura curada manualmente com base fiel nos documentos legais.
                  {state.legal_basis && <> · Base legal: <span style={{ color: 'var(--cbm-gold-400)' }}>{state.legal_basis}</span></>}
                </p>
              ) : (
                <p style={{ fontSize: 13, color: 'var(--cbm-gold-500)' }}>
                  Estrutura extraída automaticamente por análise textual. Pode conter imprecisões.
                </p>
              )}
              {hasRichDetail && (
                <div style={{
                  display: 'flex', alignItems: 'center', gap: 8,
                  marginTop: 8, padding: '8px 12px',
                  background: 'rgba(255,179,0,0.07)', borderRadius: 'var(--radius-md)',
                  border: '1px solid rgba(255,179,0,0.18)', fontSize: 12, color: 'var(--cbm-gold-300)',
                }}>
                  <Info size={13} />
                  Clique no botão <Info size={11} style={{ display: 'inline' }} /> ao lado de cada órgão para ver subordinação completa, desdobramentos, atribuições e cargos extraídos fielmente da legislação.
                </div>
              )}
            </div>

            {state.organs?.length > 0 ? (
              <Organogram
                data={state.organs}
                onSelectOrgan={handleSelectOrgan}
                selectedOrganId={selectedOrgan?.id}
              />
            ) : (
              <div className="empty-state">
                <Building2 size={40} className="empty-state-icon" />
                <h3>Estrutura não mapeada</h3>
                <p>Os órgãos deste estado ainda não foram extraídos ou mapeados.</p>
              </div>
            )}
          </div>
        )}

        {/* ── TAB: Documentos ── */}
        {activeTab === 'documentos' && (
          <div>
            <h2 style={{ fontFamily: 'Outfit', fontSize: 17, fontWeight: 700, marginBottom: 16 }}>
              Documentos Legais — {state.stats?.total_documents} arquivo{state.stats?.total_documents !== 1 ? 's' : ''}
            </h2>

            {state.stats?.has_regimento && (
              <div className="article-block" style={{ marginBottom: 16 }}>
                <span style={{ color: 'var(--cbm-gold-400)', fontWeight: 700 }}>Nota sobre unificação:</span>{' '}
                <span style={{ fontSize: 13 }}>
                  Este estado possui LOB e Regimento Interno. O organograma consolida ambos: a LOB define a estrutura jurídica formal e o Regimento detalha as subdivisões, atribuições e cargos de cada órgão.
                </span>
              </div>
            )}

            {state.stats?.has_nga && (
              <div className="article-block" style={{ marginBottom: 16, borderLeftColor: 'var(--cbm-gold-500)' }}>
                <span style={{ color: 'var(--cbm-gold-400)', fontWeight: 700 }}>Nota sobre NGA:</span>{' '}
                <span style={{ fontSize: 13 }}>
                  As Normas Gerais de Ação (NGA) funcionam como o Regimento Interno deste estado e foram unificadas com a LOB no organograma.
                </span>
              </div>
            )}

            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {state.documents?.map((doc, idx) => (
                <DocCard key={idx} doc={doc} />
              ))}
            </div>

            {state.chapters_summary?.length > 0 && (
              <div style={{ marginTop: 24 }}>
                <div className="section-heading">
                  <BookOpen size={14} />
                  Sumário de Capítulos
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                  {state.chapters_summary.map((ch, i) => (
                    <div key={i} style={{
                      display: 'flex', gap: 12, padding: '8px 12px',
                      background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)',
                      fontSize: 13,
                    }}>
                      <span style={{ color: 'var(--cbm-red-400)', fontWeight: 700, minWidth: 80 }}>
                        Cap. {ch.number}
                      </span>
                      <span style={{ color: 'var(--text-secondary)' }}>{ch.title}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ── TAB: Informações ── */}
        {activeTab === 'informacoes' && (
          <div>
            <h2 style={{ fontFamily: 'Outfit', fontSize: 17, fontWeight: 700, marginBottom: 16 }}>
              Informações Institucionais
            </h2>
            <div className="card" style={{ marginBottom: 16 }}>
              <div className="card-header">
                <span className="card-title">Identificação</span>
                <Shield size={18} color="var(--text-muted)" />
              </div>
              <InfoRow label="Estado" value={state.name} />
              <InfoRow label="Sigla do Estado" value={state.abbreviation} />
              <InfoRow label="Região" value={state.region} />
              <InfoRow label="Denominação Completa" value={state.cbm_name} />
              <InfoRow label="Sigla da Corporação" value={state.cbm_abbreviation} />
            </div>
            <div className="card" style={{ marginBottom: 16 }}>
              <div className="card-header">
                <span className="card-title">Base Legal</span>
                <Scale size={18} color="var(--text-muted)" />
              </div>
              <InfoRow label="Legislação" value={state.legal_basis} />
            </div>
            <div className="card">
              <div className="card-header">
                <span className="card-title">Dados Técnicos</span>
                <Users size={18} color="var(--text-muted)" />
              </div>
              <InfoRow label="Documentos mapeados" value={`${state.stats?.total_documents}`} />
              <InfoRow label="Possui Regimento Interno" value={state.stats?.has_regimento ? 'Sim' : 'Não'} />
              <InfoRow label="Possui NGA" value={state.stats?.has_nga ? 'Sim' : 'Não'} />
              <InfoRow label="Órgãos mapeados" value={`${state.stats?.organs_mapped || 0}`} />
              <InfoRow label="Organograma curado" value={state.stats?.curated ? 'Sim — verificado manualmente' : 'Não — extração automática'} />
              <InfoRow label="Detalhamento completo" value={hasRichDetail ? `Sim — ${Object.keys(orgDetail).length} órgãos com cargos e atribuições` : 'Não disponível'} />
              <InfoRow label="Volume documental" value={`${((state.stats?.total_chars || 0) / 1000).toFixed(1)}k caracteres`} />
            </div>
          </div>
        )}
      </div>

      {/* Overlay + Painel de detalhes do órgão */}
      {selectedOrgan && (
        <>
          <div
            className="detail-backdrop"
            onClick={() => setSelectedOrgan(null)}
          />
          <OrgDetail
            organ={selectedOrgan}
            onClose={() => setSelectedOrgan(null)}
          />
        </>
      )}
    </>
  )
}
