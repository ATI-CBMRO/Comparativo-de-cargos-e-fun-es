import { useEffect, useMemo, useState } from 'react'
import {
  Building2, ShieldAlert, Info, Award, AlertCircle,
  ArrowLeftRight, X, Pin, FileDown, FileText
} from 'lucide-react'

/* ────────────────────────────────────────────────────────────
   Comparativo DPO × COT — órgão de planejamento operacional e
   órgão de atividades técnicas, nos 27 CBMs.
   Consome database/comparativo_dpo_cot.json (dados verbatim).

   - Card de referência (CBMRO) no topo (estrutura completa).
   - Tabela dos 26 estados; cada um abre o modo "lado a lado" (RO × estado).
   - Exportação de PDF: relatório estruturado POR CARGO/FUNÇÃO da minuta
     de LOB do CBMRO, com o comparativo nas demais legislações.
   ──────────────────────────────────────────────────────────── */

/** Formata texto verbatim aplicando negrito a postos e termos de subordinação. */
function renderFriendlyText(text) {
  if (!text) return <span className="cc-empty">—</span>
  let html = text
  const patterns = [
    { regex: /\b(Oficiais|Oficial superior|Oficiais superiores|Oficial da ativa|Oficiais da ativa|último posto|último Posto|Coronéis|Coronel|Tenente-Coronel|Majores|Major|Capitão|Tenente|Praças|QOEMBM|QCOBM|CCEMBM)\b/gi, replacement: '<strong>$1</strong>' },
    { regex: /\b(Governador do Estado|Governador|Secretário de Estado|Comandante-Geral|Subcomandante-Geral|Chefe do Estado-Maior|Chefe do EMG|Estado-Maior Geral|Subcomandante|Comandante|Diretor-Geral|Diretor|Diretora|Coordenador|Coordenadora)\b/gi, replacement: '<strong>$1</strong>' }
  ]
  patterns.forEach(p => { html = html.replace(p.regex, p.replacement) })
  return <span dangerouslySetInnerHTML={{ __html: html }} />
}

function List({ items }) {
  if (!items || items.length === 0) return <span className="cc-empty">—</span>
  return <ul className="cc-list">{items.map((it, i) => <li key={i}>{renderFriendlyText(it)}</li>)}</ul>
}

function organAtribuicoes(organ) {
  if (organ.atribuicoes && organ.atribuicoes.length) return organ.atribuicoes
  const fromCargos = []
  for (const c of organ.cargos || []) for (const a of c.atribuicoes || []) fromCargos.push(a)
  return fromCargos
}

function OrganNameCell({ organ }) {
  return (
    <div>
      <div className="oc-organ-name">{renderFriendlyText(organ.name)}</div>
      <div className="oc-organ-sub">
        {organ.abbreviation && <span className="oc-organ-abbr">{organ.abbreviation}</span>}
        {(organ.legalRef || organ.baseLegal) && (
          <span className="oc-organ-ref">{organ.legalRef || organ.baseLegal}</span>
        )}
      </div>
    </div>
  )
}

function CargosCell({ cargos }) {
  if (!cargos || cargos.length === 0) return <span className="cc-empty">—</span>
  return (
    <div className="oc-cargos">
      {cargos.map((c, i) => (
        <div key={i} className="oc-cargo">
          <span className="oc-cargo-name">{renderFriendlyText(c.cargo)}</span>
          {c.requisito && <span className="oc-cargo-req">{renderFriendlyText(c.requisito)}</span>}
          {c.subordinadoA && (
            <span className="oc-cargo-sub">
              Subordinação: <strong>{c.subordinadoA}</strong>
            </span>
          )}
        </div>
      ))}
    </div>
  )
}

function CbmCell({ st, note, onCompare }) {
  return (
    <div className="oc-cbm-cell">
      <div className="cc-corp-head">
        <span className={`cc-corp-abbr ${st.is_reference ? 'ref' : ''}`}>{st.abbreviation}</span>
        <div>
          <div className="cc-corp-name">{st.name}</div>
          <div className="cc-corp-cbm">{st.cbm}{st.is_reference ? ' · Referência' : ''}</div>
        </div>
      </div>
      {onCompare && (
        <button className="oc-compare-btn" onClick={() => onCompare(st)}>
          <ArrowLeftRight size={12} /> Comparar com RO
        </button>
      )}
      {note && (
        <div className="oc-note">
          <Info size={11} style={{ flexShrink: 0, marginTop: 1 }} />
          <span>{note}</span>
        </div>
      )}
    </div>
  )
}

/* ── Card de referência (CBMRO) — bloco normal no fluxo ── */
function ReferenceCard({ state, group, groupMeta }) {
  const organs = (state && state[group]) || []
  const GroupIcon = group === 'cot' ? ShieldAlert : Building2
  return (
    <div className="oc-ref-card">
      <div className="oc-ref-card-head">
        <span className="oc-ref-badge">{state.abbreviation}</span>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div className="oc-ref-card-title">
            <Pin size={13} /> Referência — {state.cbm} · {groupMeta?.ref_abbr}
          </div>
          <div className="oc-ref-card-sub">
            {state.name} · Minuta de LOB do CBMRO — estrutura completa do {groupMeta?.ref_abbr}
          </div>
        </div>
        <GroupIcon size={26} className="oc-ref-card-glyph" />
      </div>

      {organs.length === 0 ? (
        <div className="oc-ref-empty">Órgão de referência não localizado para este grupo.</div>
      ) : (
        <div className="oc-ref-body">
          {organs.map((organ, i) => (
            <div key={i} className="oc-ref-organ">
              <div className="oc-ref-organ-head">
                <OrganNameCell organ={organ} />
                {organ.subordinadoA && (
                  <span className="oc-ref-sub">
                    Subordinação: {renderFriendlyText(organ.subordinadoA)}
                  </span>
                )}
              </div>
              <div className="oc-ref-grid">
                <div className="oc-ref-col">
                  <div className="oc-ref-col-label">Cargos / Funções</div>
                  <CargosCell cargos={organ.cargos} />
                </div>
                <div className="oc-ref-col">
                  <div className="oc-ref-col-label">Atribuições (verbatim)</div>
                  <List items={organAtribuicoes(organ)} />
                  <div className="oc-ref-col-label" style={{ marginTop: 16 }}>Desdobramentos</div>
                  <List items={organ.desdobramentos} />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

/* ── Lado a lado: RO × estado, campo a campo ── */
function perOrgan(organs, fn) {
  if (!organs || organs.length === 0) return <span className="cc-empty">—</span>
  if (organs.length === 1) return fn(organs[0])
  return (
    <div className="oc-multi">
      {organs.map((o, i) => (
        <div key={i} className="oc-multi-item">
          <div className="oc-multi-tag">{o.abbreviation || o.name}</div>
          {fn(o)}
        </div>
      ))}
    </div>
  )
}

const SBS_FIELDS = [
  { label: 'Órgão equivalente', render: orgs => perOrgan(orgs, o => <OrganNameCell organ={o} />) },
  { label: 'Subordinação', render: orgs => perOrgan(orgs, o => o.subordinadoA ? <span className="oc-sub">{renderFriendlyText(o.subordinadoA)}</span> : <span className="cc-empty">—</span>) },
  { label: 'Cargo / Função', render: orgs => perOrgan(orgs, o => <CargosCell cargos={o.cargos} />) },
  { label: 'Atribuições (verbatim)', render: orgs => perOrgan(orgs, o => <List items={organAtribuicoes(o)} />) },
  { label: 'Desdobramentos', render: orgs => perOrgan(orgs, o => <List items={o.desdobramentos} />) },
]

function SideBySide({ referenceState, target, group, groupMeta, note, onClose }) {
  const refOrgans = referenceState[group] || []
  const tgtOrgans = target[group] || []
  return (
    <div>
      <div className="oc-sbs-toolbar">
        <button className="btn btn-ghost btn-sm" onClick={onClose}>
          <X size={14} /> Voltar à tabela
        </button>
        <span className="oc-sbs-title">
          <ArrowLeftRight size={15} color="var(--cbm-red-700)" />
          {groupMeta?.ref_abbr} — CBMRO <span className="oc-sbs-vs">×</span> {target.cbm || target.abbreviation}
        </span>
      </div>

      {note && (
        <div className="oc-note" style={{ margin: '0 0 12px' }}>
          <Info size={12} style={{ flexShrink: 0, marginTop: 1 }} />
          <span>{note}</span>
        </div>
      )}

      <div className="cargo-compare-wrapper oc-scroll">
        <table className="cargo-compare-table cc-table oc-sbs-table">
          <colgroup>
            <col style={{ width: 170 }} />
            <col style={{ width: '50%' }} />
            <col style={{ width: '50%' }} />
          </colgroup>
          <thead>
            <tr>
              <th className="cc-col-label cc-corner">Campo</th>
              <th className="cc-col-ro cc-corner">
                <div className="cc-corp-head">
                  <span className="cc-corp-abbr ref">{referenceState.abbreviation}</span>
                  <div>
                    <div className="cc-corp-name">{referenceState.name}</div>
                    <div className="cc-corp-cbm">{referenceState.cbm} · Referência</div>
                  </div>
                </div>
              </th>
              <th>
                <div className="cc-corp-head">
                  <span className="cc-corp-abbr">{target.abbreviation}</span>
                  <div>
                    <div className="cc-corp-name">{target.name}</div>
                    <div className="cc-corp-cbm">{target.cbm}</div>
                  </div>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            {tgtOrgans.length === 0 ? (
              <tr>
                <td className="cc-col-label">Situação</td>
                <td className="cc-col-ro cc-ref-cell">{SBS_FIELDS[0].render(refOrgans)}</td>
                <td className="cc-notfound">
                  <span style={{ display: 'flex', gap: 6, alignItems: 'flex-start' }}>
                    <AlertCircle size={13} style={{ flexShrink: 0, marginTop: 2 }} />
                    {note || 'Órgão equivalente não discriminado na legislação deste estado.'}
                  </span>
                </td>
              </tr>
            ) : (
              SBS_FIELDS.map(f => (
                <tr key={f.label}>
                  <td className="cc-col-label">{f.label}</td>
                  <td className="cc-col-ro cc-ref-cell">{f.render(refOrgans)}</td>
                  <td>{f.render(tgtOrgans)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

/* ── Relatório PDF — uma folha por estado (CBMRO × estado), 3 colunas ── */
function PrintReport({ referenceState, otherStates, group, groupMeta }) {
  if (!referenceState) return null
  const refOrgans = referenceState[group] || []
  const printDate = new Date().toLocaleDateString('pt-BR', {
    day: '2-digit', month: 'long', year: 'numeric',
  })

  return (
    <div className="oc-print">
      {/* ── Capa (folha própria) ── */}
      <div className="oc-print-cover">
        {/* Barra de cabeçalho — réplica do portal */}
        <div className="oc-cover-header-bar">
          <img
            className="oc-cover-emblem"
            src="/BrasaoCBMRO2D-COMPLETO.png"
            onError={e => {
              if (!e.currentTarget.dataset.fb) {
                e.currentTarget.dataset.fb = '1'
                e.currentTarget.src = '/brasao-cbmro.svg'
              }
            }}
            alt="Brasão CBMRO"
          />
          <div className="oc-cover-header-text">
            <div className="oc-cover-header-title">Portal CBM — Legislação Nacional</div>
            <div className="oc-cover-header-rule" />
            <div className="oc-cover-header-sub">Corpos de Bombeiros Militares</div>
          </div>
        </div>

        {/* Área central com o título */}
        <div className="oc-cover-body">
          <div className="oc-cover-label">Relatório Comparativo</div>
          <div className="oc-cover-main-title">{groupMeta?.ref_abbr}</div>
          <div className="oc-cover-subtitle">{groupMeta?.ref_name}</div>
          <div className="oc-cover-rule" />
          <p className="oc-cover-desc">
            Comparativo do órgão equivalente à <strong>{groupMeta?.ref_abbr}</strong> nos
            27 Corpos de Bombeiros Militares. Cada folha apresenta a comparação direta
            CBMRO × estado, com os campos dispostos em linhas e as duas legislações em
            colunas paralelas.
          </p>
          <div className="oc-cover-stats">
            <span>27 Corpos de Bombeiros Militares</span>
            <span className="oc-cover-stats-sep">·</span>
            <span>Referência: Minuta de LOB do CBMRO</span>
          </div>
        </div>

        {/* Rodapé com data */}
        <div className="oc-cover-footer">
          <span>Portal de Legislação CBM</span>
          <span>Emitido em <strong>{printDate}</strong></span>
        </div>
      </div>

      {/* Uma folha por estado */}
      {otherStates.map((st, idx) => {
        const stOrgans = st[group] || []
        const note = st.notes?.[group]
        const isLast = idx === otherStates.length - 1
        return (
          <section
            key={st.id}
            className="oc-print-page"
            style={!isLast ? { pageBreakAfter: 'always' } : undefined}
          >
            {/* Mini cabeçalho da folha */}
            <div className="oc-print-page-head">
              <span className="oc-print-group-tag">{groupMeta?.ref_abbr}</span>
              <span className="oc-print-page-title">
                CBMRO × {st.abbreviation} · {st.cbm}
              </span>
              <span className="oc-print-page-date">{printDate}</span>
            </div>

            {/* Tabela de comparação 3 colunas */}
            <table className="oc-print-sbs">
              <colgroup>
                <col style={{ width: '16%' }} />
                <col style={{ width: '42%' }} />
                <col style={{ width: '42%' }} />
              </colgroup>
              <thead>
                <tr>
                  <th className="oc-psbs-label-head">Campo</th>
                  <th className="oc-psbs-ro-head">
                    {referenceState.abbreviation} · {referenceState.cbm}
                    <span className="oc-psbs-ref-tag">Referência</span>
                  </th>
                  <th className="oc-psbs-state-head">
                    {st.abbreviation} · {st.cbm}
                    <br /><small>{st.name}</small>
                  </th>
                </tr>
              </thead>
              <tbody>
                {stOrgans.length === 0 ? (
                  <tr>
                    <td className="oc-psbs-label">Situação</td>
                    <td>{SBS_FIELDS[0].render(refOrgans)}</td>
                    <td className="oc-psbs-notfound">
                      {note || 'Órgão equivalente não discriminado na legislação deste estado.'}
                    </td>
                  </tr>
                ) : (
                  SBS_FIELDS.map(f => (
                    <tr key={f.label}>
                      <td className="oc-psbs-label">{f.label}</td>
                      <td>{f.render(refOrgans)}</td>
                      <td>{f.render(stOrgans)}</td>
                    </tr>
                  ))
                )}
                {note && stOrgans.length > 0 && (
                  <tr>
                    <td className="oc-psbs-label">Nota</td>
                    <td>—</td>
                    <td className="oc-psbs-note">{note}</td>
                  </tr>
                )}
              </tbody>
            </table>
          </section>
        )
      })}
    </div>
  )
}

export default function OrgaosOperacionaisComparator() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const [group, setGroup] = useState('dpo')
  const [compareId, setCompareId] = useState(null)

  useEffect(() => {
    fetch('/database/comparativo_dpo_cot.json')
      .then(r => (r.ok ? r.json() : Promise.reject()))
      .then(setData)
      .catch(() => setError(true))
  }, [])

  const groupMeta = useMemo(
    () => (data ? data.groups.find(g => g.key === group) : null),
    [data, group]
  )
  const referenceState = useMemo(
    () => (data ? data.states.find(s => s.is_reference) : null),
    [data]
  )
  const otherStates = useMemo(
    () => (data ? data.states.filter(s => !s.is_reference) : []),
    [data]
  )
  const compareTarget = useMemo(
    () => (data && compareId ? data.states.find(s => s.id === compareId) : null),
    [data, compareId]
  )

  if (error) {
    return (
      <div className="empty-state" style={{ marginTop: 24 }}>
        <Building2 size={40} className="empty-state-icon" />
        <h3>Comparativo não encontrado</h3>
        <p>Execute <code>python scripts/build_dpo_cot_comparison.py</code> para gerar os dados.</p>
      </div>
    )
  }
  if (!data) return <div className="empty-state"><div className="spinner" /></div>

  const GROUP_ICON = { dpo: Building2, cot: ShieldAlert }

  return (
    <div>
      {/* ===== UI de tela (oculta na impressão) ===== */}
      <div className="no-print">
        {/* Intro / contexto da referência */}
        <div className="card" style={{ marginBottom: 18 }}>
          <div className="card-header">
            <span className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <Award size={18} color="var(--cbm-red-700)" />
              Órgãos Operacionais — Referência CBMRO (Minuta de LOB)
            </span>
          </div>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.6, margin: 0 }}>
            Comparação dos órgãos equivalentes à <strong>DPO</strong> (Diretoria de Planejamento
            Operacional) e ao <strong>COT</strong> (Comando de Operações Técnicas) da minuta de Lei
            de Organização Básica do CBMRO, nos 27 CBMs. O casamento é <strong>por função</strong> —
            a nomenclatura varia (COB, CAT etc.) — e o texto é transcrito <strong>verbatim</strong>.
            Use <strong>“Comparar com RO”</strong> para o detalhe lado a lado de um estado, ou
            <strong> “Exportar PDF”</strong> para o relatório por cargo/função com todos os estados.
          </p>
        </div>

        {/* Alternância DPO / COT */}
        <div className="tabs" style={{ marginBottom: 16 }}>
          {data.groups.map(g => {
            const Icon = GROUP_ICON[g.key] || Building2
            return (
              <button
                key={g.key}
                className={`tab ${group === g.key ? 'active' : ''}`}
                onClick={() => { setGroup(g.key); setCompareId(null) }}
              >
                <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <Icon size={14} /> {g.ref_abbr} — {g.title}
                </span>
              </button>
            )
          })}
        </div>

        {/* Descrição do grupo ativo */}
        {groupMeta && (
          <div className="oc-group-desc" style={{ marginBottom: 16 }}>
            <Info size={14} style={{ flexShrink: 0, marginTop: 2 }} color="var(--accent-blue)" />
            <span>
              <strong>{groupMeta.ref_abbr} — {groupMeta.ref_name}:</strong> {groupMeta.description}
            </span>
          </div>
        )}

        {/* Card de referência (oculto no modo lado a lado) */}
        {referenceState && !compareTarget && (
          <ReferenceCard state={referenceState} group={group} groupMeta={groupMeta} />
        )}

        {compareTarget ? (
          <SideBySide
            referenceState={referenceState}
            target={compareTarget}
            group={group}
            groupMeta={groupMeta}
            note={compareTarget.notes?.[group]}
            onClose={() => setCompareId(null)}
          />
        ) : (
          <>
            {/* Barra de ações: exportar PDF de todos os estados */}
            <div className="oc-toolbar">
              <span className="oc-toolbar-info">
                <FileText size={15} color="var(--text-muted)" />
                {otherStates.length} estados comparados · referência CBMRO
              </span>
              <button className="btn btn-primary" onClick={() => window.print()}>
                <FileDown size={16} />
                Exportar PDF — relatório por cargo ({groupMeta?.ref_abbr})
              </button>
            </div>

            {/* Tabela dos 26 estados (5 colunas, cabe na tela) */}
            <div className="cargo-compare-wrapper oc-scroll">
              <table className="cargo-compare-table oc-table">
                <colgroup>
                  <col style={{ width: '15%' }} />
                  <col style={{ width: '21%' }} />
                  <col style={{ width: '20%' }} />
                  <col style={{ width: '26%' }} />
                  <col style={{ width: '18%' }} />
                </colgroup>
                <thead>
                  <tr>
                    <th className="oc-col-cbm cc-corner">CBM</th>
                    <th>Órgão equivalente</th>
                    <th>Cargo / Função</th>
                    <th>Atribuições (verbatim)</th>
                    <th>Desdobramentos</th>
                  </tr>
                </thead>
                <tbody>
                  {otherStates.map(st => {
                    const organs = st[group] || []
                    const note = st.notes?.[group]

                    if (organs.length === 0) {
                      return (
                        <tr key={st.id}>
                          <td className="oc-col-cbm">
                            <CbmCell st={st} onCompare={s => setCompareId(s.id)} />
                          </td>
                          <td colSpan={4} className="cc-notfound">
                            <span style={{ display: 'flex', gap: 6, alignItems: 'flex-start' }}>
                              <AlertCircle size={13} style={{ flexShrink: 0, marginTop: 2 }} />
                              {note || 'Órgão equivalente não discriminado na legislação deste estado.'}
                            </span>
                          </td>
                        </tr>
                      )
                    }

                    return organs.map((organ, j) => (
                      <tr key={`${st.id}-${j}`}>
                        {j === 0 && (
                          <td className="oc-col-cbm" rowSpan={organs.length}>
                            <CbmCell st={st} note={note} onCompare={s => setCompareId(s.id)} />
                          </td>
                        )}
                        <td>
                          <OrganNameCell organ={organ} />
                          {organ.subordinadoA && (
                            <div className="oc-organ-subord">
                              <span className="oc-organ-subord-label">Subordinação:</span>{' '}
                              {renderFriendlyText(organ.subordinadoA)}
                            </div>
                          )}
                        </td>
                        <td><CargosCell cargos={organ.cargos} /></td>
                        <td><List items={organAtribuicoes(organ)} /></td>
                        <td><List items={organ.desdobramentos} /></td>
                      </tr>
                    ))
                  })}
                </tbody>
              </table>
            </div>

            <p style={{ fontSize: 11.5, color: 'var(--text-muted)', marginTop: 12, lineHeight: 1.5 }}>
              Fonte: legislação de organização básica / regimento de cada CBM. Linhas com várias
              organizações indicam que a função se distribui por mais de um órgão (ex.: capital e
              interior). Gerado por <code>scripts/build_dpo_cot_comparison.py</code>.
            </p>
          </>
        )}
      </div>

      {/* ===== Relatório PDF (visível apenas na impressão) ===== */}
      <PrintReport
        referenceState={referenceState}
        otherStates={otherStates}
        group={group}
        groupMeta={groupMeta}
      />
    </div>
  )
}
