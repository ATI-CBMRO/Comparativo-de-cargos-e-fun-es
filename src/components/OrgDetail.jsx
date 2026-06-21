import { X, ChevronRight, Scale, Users, ListTree, FileText, BookOpen, AlertCircle } from 'lucide-react'

function SectionHeading({ icon: Icon, label, color = 'var(--cbm-red-400)' }) {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 8,
      marginBottom: 10, marginTop: 18,
    }}>
      <Icon size={13} color={color} />
      <span style={{
        fontSize: 11, fontWeight: 700, textTransform: 'uppercase',
        letterSpacing: '1px', color,
      }}>{label}</span>
      <div style={{ flex: 1, height: 1, background: 'var(--border-subtle)' }} />
    </div>
  )
}

function CargoCard({ cargo, idx }) {
  return (
    <div style={{
      background: 'var(--bg-surface)',
      border: '1px solid var(--border-subtle)',
      borderLeft: '3px solid var(--cbm-red-800)',
      borderRadius: '0 var(--radius-md) var(--radius-md) 0',
      padding: '12px 14px',
      marginBottom: 8,
    }}>
      {/* Cargo title */}
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 10, marginBottom: 8 }}>
        <span style={{
          background: 'var(--cbm-red-900)', color: 'var(--cbm-red-300)',
          borderRadius: 4, padding: '2px 7px', fontSize: 10, fontWeight: 700,
          flexShrink: 0, marginTop: 2,
        }}>
          {String(idx + 1).padStart(2, '0')}
        </span>
        <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.4 }}>
          {cargo.cargo}
        </span>
      </div>

      {/* Subordinado a */}
      {cargo.subordinadoA && (
        <div style={{ display: 'flex', gap: 8, marginBottom: 6, fontSize: 12 }}>
          <span style={{ color: 'var(--cbm-gray-400)', minWidth: 90, flexShrink: 0 }}>
            SUBORDINADO A
          </span>
          <span style={{ color: 'var(--cbm-gold-400)', fontWeight: 600 }}>
            {cargo.subordinadoA}
          </span>
        </div>
      )}

      {/* Requisito */}
      {cargo.requisito && (
        <div style={{ display: 'flex', gap: 8, marginBottom: 6, fontSize: 12 }}>
          <span style={{ color: 'var(--cbm-gray-400)', minWidth: 90, flexShrink: 0 }}>
            REQUISITO
          </span>
          <span style={{ color: 'var(--cbm-gray-200)', fontStyle: 'italic' }}>
            {cargo.requisito}
          </span>
        </div>
      )}

      {/* Desdobramentos / Subordinados */}
      {cargo.desdobramentos?.length > 0 && (
        <div style={{ marginBottom: 8 }}>
          <div style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.8px', color: 'var(--cbm-gold-500)', marginBottom: 5 }}>
            SUBORDINADOS / DESDOBRAMENTOS
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            {cargo.desdobramentos.map((d, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: 6, fontSize: 12, color: 'var(--text-secondary)' }}>
                <ChevronRight size={12} color="var(--cbm-gray-500)" style={{ flexShrink: 0, marginTop: 2 }} />
                <span>{d}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Atribuições */}
      {cargo.atribuicoes?.length > 0 && (
        <div>
          <div style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.8px', color: 'var(--cbm-red-400)', marginBottom: 5 }}>
            ATRIBUIÇÕES
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            {cargo.atribuicoes.map((a, i) => (
              <div key={i} style={{ display: 'flex', gap: 8, fontSize: 12, color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                <span style={{ color: 'var(--cbm-red-500)', flexShrink: 0 }}>•</span>
                <span>{a}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default function OrgDetail({ organ, onClose }) {
  if (!organ) return null

  const hasDetail = organ.atribuicoes?.length || organ.desdobramentos?.length || organ.cargos?.length

  return (
    <div className="org-detail-panel" style={{
      position: 'fixed',
      top: 0, right: 0,
      width: 520,
      height: '100vh',
      background: 'var(--bg-modal)',
      borderLeft: '1px solid var(--border-card)',
      boxShadow: '-8px 0 40px rgba(16,32,64,0.22)',
      zIndex: 200,
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden',
    }}>
      {/* Header */}
      <div style={{
        background: 'linear-gradient(125deg, var(--navy-900) 0%, var(--navy-700) 100%)',
        borderBottom: '3px solid var(--cbm-red-700)',
        padding: '16px 20px',
        flexShrink: 0,
      }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
              {organ.abbreviation && (
                <span style={{
                  background: 'var(--cbm-red-800)', color: '#fff',
                  padding: '2px 8px', borderRadius: 5,
                  fontSize: 12, fontWeight: 800, flexShrink: 0,
                }}>
                  {organ.abbreviation}
                </span>
              )}
              {organ.category && (
                <span className="badge badge-gray" style={{ fontSize: 10 }}>
                  {organ.category}
                </span>
              )}
            </div>
            <h2 style={{
              fontFamily: 'Outfit', fontSize: 17, fontWeight: 800,
              color: '#fff', marginTop: 6, lineHeight: 1.3,
            }}>
              {organ.name}
            </h2>
            {organ.subordinadoA && (
              <p style={{ fontSize: 12, color: 'var(--cbm-gold-400)', marginTop: 4, fontWeight: 600 }}>
                Subordinado a: {organ.subordinadoA}
              </p>
            )}
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'rgba(255,255,255,0.08)', border: '1px solid rgba(255,255,255,0.12)',
              borderRadius: 8, padding: 6, cursor: 'pointer',
              color: 'var(--cbm-gray-300)', flexShrink: 0,
            }}
          >
            <X size={18} />
          </button>
        </div>
      </div>

      {/* Body */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px 20px' }}>

        {!hasDetail && (
          <div style={{
            display: 'flex', flexDirection: 'column', alignItems: 'center',
            gap: 12, padding: '40px 20px', textAlign: 'center',
          }}>
            <AlertCircle size={32} color="var(--cbm-gray-500)" />
            <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
              Detalhamento completo não disponível para este órgão neste estado.
              Consulte o documento legislativo fonte.
            </p>
            {organ.legalRef && (
              <span className="badge badge-gray" style={{ fontSize: 11 }}>
                {organ.legalRef}
              </span>
            )}
          </div>
        )}

        {/* NOMENCLATURA */}
        {organ.legalRef && (
          <>
            <SectionHeading icon={FileText} label="Nomenclatura" />
            <div style={{
              background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)',
              padding: '10px 14px', marginBottom: 4,
            }}>
              <div style={{ fontSize: 14, fontWeight: 700, color: 'var(--text-primary)' }}>
                {organ.name}
              </div>
              {organ.abbreviation && (
                <div style={{ fontSize: 12, color: 'var(--cbm-gray-300)', marginTop: 2 }}>
                  ({organ.abbreviation})
                </div>
              )}
            </div>
          </>
        )}

        {/* DESDOBRAMENTOS */}
        {organ.desdobramentos?.length > 0 && (
          <>
            <SectionHeading icon={ListTree} label="Desdobramentos" color="var(--cbm-gold-400)" />
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              {organ.desdobramentos.map((d, i) => (
                <div key={i} style={{
                  display: 'flex', alignItems: 'flex-start', gap: 8,
                  padding: '5px 0', borderBottom: '1px solid var(--border-subtle)',
                  fontSize: 13, color: 'var(--text-secondary)',
                }}>
                  <ChevronRight size={14} color="var(--cbm-gold-500)" style={{ flexShrink: 0, marginTop: 2 }} />
                  <span>{d}</span>
                </div>
              ))}
            </div>
          </>
        )}

        {/* ATRIBUIÇÕES DO ÓRGÃO */}
        {organ.atribuicoes?.length > 0 && (
          <>
            <SectionHeading icon={Scale} label="Atribuições do Órgão" color="var(--cbm-red-400)" />
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              {organ.atribuicoes.map((a, i) => (
                <div key={i} style={{
                  display: 'flex', gap: 10, fontSize: 13, color: 'var(--text-secondary)',
                  lineHeight: 1.7, padding: '4px 0',
                  borderBottom: '1px solid var(--border-subtle)',
                }}>
                  <span style={{ color: 'var(--cbm-red-500)', flexShrink: 0, marginTop: 2 }}>•</span>
                  <span>{a}</span>
                </div>
              ))}
            </div>
          </>
        )}

        {/* CARGOS E FUNÇÕES */}
        {organ.cargos?.length > 0 && (
          <>
            <SectionHeading
              icon={Users}
              label={`Cargos e Funções (${organ.cargos.length})`}
              color="var(--cbm-gold-400)"
            />
            <div>
              {organ.cargos.map((cargo, idx) => (
                <CargoCard key={idx} cargo={cargo} idx={idx} />
              ))}
            </div>
          </>
        )}

        {/* BASE LEGAL */}
        {organ.baseLegal && (
          <>
            <SectionHeading icon={BookOpen} label="Base Legal" color="var(--cbm-gray-300)" />
            <div style={{
              background: 'var(--bg-surface)', borderRadius: 'var(--radius-md)',
              padding: '10px 14px', fontSize: 12, color: 'var(--text-muted)',
              lineHeight: 1.6,
            }}>
              {organ.baseLegal}
            </div>
          </>
        )}

        {/* ARTIGO LEGAL DE ORIGEM */}
        {organ.artigosDeOrigem?.length > 0 && (
          <>
            <div style={{ marginTop: 14 }}>
              <div style={{
                background: 'rgba(183,28,28,0.08)', border: '1px solid var(--cbm-red-900)',
                borderRadius: 'var(--radius-md)', padding: '10px 14px',
              }}>
                <div style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.8px', color: 'var(--cbm-red-400)', marginBottom: 6 }}>
                  ARTIGO LEGAL DE ORIGEM
                </div>
                <div style={{ fontSize: 12, color: 'var(--cbm-red-300)' }}>
                  {organ.artigosDeOrigem.join('; ')}
                </div>
              </div>
            </div>
          </>
        )}

        <div style={{ height: 32 }} />
      </div>
    </div>
  )
}
