import { useEffect, useMemo, useState } from 'react'
import {
  Building2, ShieldAlert, Info, Award, AlertCircle,
  FileDown, FileText
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

/* ── helpers mantidos para o PrintReport ── */
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

/* ── Linhas da tabela matricial (campos como linhas, estados como colunas) ── */
const MATRIX_ROWS = [
  {
    key: 'organ',
    label: 'Órgão / Sigla',
    render: o => <OrganNameCell organ={o} />,
  },
  {
    key: 'subord',
    label: 'Subordinação',
    render: o => o.subordinadoA
      ? <span className="oc-sub">{renderFriendlyText(o.subordinadoA)}</span>
      : <span className="cc-empty">—</span>,
  },
  {
    key: 'cargos',
    label: 'Cargo / Função',
    render: o => {
      const names = (o.cargos || []).map(c => c.cargo).filter(Boolean)
      return names.length
        ? <ul className="cc-list">{names.map((n, i) => <li key={i}>{renderFriendlyText(n)}</li>)}</ul>
        : <span className="cc-empty">—</span>
    },
  },
  {
    key: 'req',
    label: 'Requisito / Posto',
    render: o => {
      const reqs = [...new Set((o.cargos || []).map(c => c.requisito).filter(Boolean))]
      return reqs.length
        ? <ul className="cc-list">{reqs.map((r, i) => <li key={i}>{renderFriendlyText(r)}</li>)}</ul>
        : <span className="cc-empty">—</span>
    },
  },
  {
    key: 'atrib',
    label: 'Atribuições',
    render: o => <List items={organAtribuicoes(o)} />,
  },
  {
    key: 'desd',
    label: 'Desdobramentos',
    render: o => {
      const items = o.desdobramentos || []
      return items.length ? <List items={items} /> : <span className="cc-empty">—</span>
    },
  },
]

/* ── Tabela matricial: campos em linhas, estados em colunas ── */
function MatrixTable({ referenceState, otherStates, group }) {
  const refOrgans = (referenceState?.[group]) || []
  const isCot = group === 'cot'

  const cols = otherStates.map(st => ({
    state: st,
    organs: st[group] || [],
    note: st.notes?.[group],
    span: Math.max((st[group] || []).length, 1),
  }))

  const hasSubCols = cols.some(c => c.organs.length > 1) || refOrgans.length > 1

  return (
    <div className="cargo-compare-wrapper oc-scroll">
      <table className="cargo-compare-table oc-matrix-table">
        <colgroup>
          <col style={{ width: 148 }} />
          {refOrgans.length === 0
            ? <col style={{ minWidth: 240 }} />
            : refOrgans.map((_, i) => <col key={i} style={{ minWidth: 240 }} />)
          }
          {cols.flatMap(c =>
            Array.from({ length: c.span }, (_, i) => (
              <col key={`${c.state.id}-${i}`} style={{ minWidth: 196 }} />
            ))
          )}
        </colgroup>

        <thead>
          {/* Linha 1: Campo | CBMRO | estados */}
          <tr>
            <th className="cc-col-label cc-corner" rowSpan={hasSubCols ? 2 : 1}>
              Campo
            </th>
            <th
              className="cc-col-ro cc-corner"
              colSpan={Math.max(refOrgans.length, 1)}
              rowSpan={refOrgans.length <= 1 && hasSubCols ? 2 : 1}
            >
              <div className="cc-corp-head">
                <span className="cc-corp-abbr ref">{referenceState?.abbreviation}</span>
                <div>
                  <div className="cc-corp-name">{referenceState?.name}</div>
                  <div className="cc-corp-cbm">
                    {referenceState?.cbm} · Referência
                    {isCot && (
                      <span className="oc-cot-note" title="No CBMRO, o COT é subordinado à DPO — estrutura única entre os 27 CBMs.">
                        <Info size={10} />
                        COT ⊂ DPO
                        <span className="oc-cot-tooltip">
                          No CBMRO, o COT é subordinado à DPO — estrutura única entre os 27 CBMs.
                        </span>
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </th>
            {cols.map(c => (
              <th
                key={c.state.id}
                colSpan={c.span}
                rowSpan={c.organs.length <= 1 && hasSubCols ? 2 : 1}
              >
                <div className="cc-corp-head">
                  <span className="cc-corp-abbr">{c.state.abbreviation}</span>
                  <div>
                    <div className="cc-corp-name">{c.state.name}</div>
                    <div className="cc-corp-cbm">{c.state.cbm}</div>
                  </div>
                </div>
              </th>
            ))}
          </tr>

          {/* Linha 2: sub-cabeçalhos de órgão (só quando algum estado tem 2+ órgãos) */}
          {hasSubCols && (
            <tr>
              {refOrgans.length > 1 && refOrgans.map((o, i) => (
                <th key={i} className="cc-col-ro oc-sub-header">
                  {o.abbreviation || o.name}
                </th>
              ))}
              {cols.map(c =>
                c.organs.length > 1
                  ? c.organs.map((o, i) => (
                      <th key={i} className="oc-sub-header">
                        {o.abbreviation || o.name}
                      </th>
                    ))
                  : null
              )}
            </tr>
          )}
        </thead>

        <tbody>
          {MATRIX_ROWS.map((row, rowIdx) => (
            <tr key={row.key}>
              <td className="cc-col-label">{row.label}</td>
              {/* Células CBMRO (sticky) */}
              {refOrgans.length === 0
                ? <td className="cc-col-ro cc-ref-cell"><span className="cc-empty">—</span></td>
                : refOrgans.map((o, i) => (
                    <td key={i} className="cc-col-ro cc-ref-cell">{row.render(o)}</td>
                  ))
              }
              {/* Células dos estados */}
              {cols.map(c => {
                if (c.organs.length === 0) {
                  if (rowIdx === 0) {
                    return (
                      <td key={c.state.id} className="cc-notfound" rowSpan={MATRIX_ROWS.length}>
                        <span style={{ display: 'flex', gap: 5, alignItems: 'flex-start', fontSize: 11.5 }}>
                          <AlertCircle size={13} style={{ flexShrink: 0, marginTop: 2 }} />
                          {c.note || 'Órgão equivalente não discriminado na legislação deste estado.'}
                        </span>
                      </td>
                    )
                  }
                  return null
                }
                return c.organs.map((o, i) => (
                  <td key={i}>{row.render(o)}</td>
                ))
              })}
            </tr>
          ))}
        </tbody>
      </table>
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

  if (error) {
    return (
      <div className=”empty-state” style={{ marginTop: 24 }}>
        <Building2 size={40} className=”empty-state-icon” />
        <h3>Comparativo não encontrado</h3>
        <p>Execute <code>python scripts/build_dpo_cot_comparison.py</code> para gerar os dados.</p>
      </div>
    )
  }
  if (!data) return <div className=”empty-state”><div className=”spinner” /></div>

  const GROUP_ICON = { dpo: Building2, cot: ShieldAlert }

  return (
    <div>
      {/* ===== UI de tela (oculta na impressão) ===== */}
      <div className=”no-print”>
        <div className=”card” style={{ marginBottom: 18 }}>
          <div className=”card-header”>
            <span className=”card-title” style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <Award size={18} color=”var(--cbm-red-700)” />
              Órgãos Operacionais — Referência CBMRO (Minuta de LOB)
            </span>
          </div>
          <p style={{ fontSize: 13, color: 'var(--text-secondary)', lineHeight: 1.6, margin: 0 }}>
            Comparação dos órgãos equivalentes à <strong>DPO</strong> (Diretoria de Planejamento
            Operacional) e ao <strong>COT</strong> (Comando de Operações Técnicas) da minuta de LOB
            do CBMRO, nos 27 CBMs. Casamento <strong>por função</strong> — a nomenclatura varia
            (COB, CAT etc.) — texto transcrito <strong>verbatim</strong>. Use{' '}
            <strong>&ldquo;Exportar PDF&rdquo;</strong> para o relatório completo.
          </p>
        </div>

        <div className=”tabs” style={{ marginBottom: 16 }}>
          {data.groups.map(g => {
            const Icon = GROUP_ICON[g.key] || Building2
            return (
              <button
                key={g.key}
                className={`tab ${group === g.key ? 'active' : ''}`}
                onClick={() => setGroup(g.key)}
              >
                <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <Icon size={14} /> {g.ref_abbr} — {g.title}
                </span>
              </button>
            )
          })}
        </div>

        {groupMeta && (
          <div className=”oc-group-desc” style={{ marginBottom: 16 }}>
            <Info size={14} style={{ flexShrink: 0, marginTop: 2 }} color=”var(--accent-blue)” />
            <span>
              <strong>{groupMeta.ref_abbr} — {groupMeta.ref_name}:</strong> {groupMeta.description}
            </span>
          </div>
        )}

        <div className=”oc-toolbar”>
          <span className=”oc-toolbar-info”>
            <FileText size={15} color=”var(--text-muted)” />
            {otherStates.length} estados comparados · referência CBMRO
          </span>
          <button className=”btn btn-primary” onClick={() => window.print()}>
            <FileDown size={16} />
            Exportar PDF — {groupMeta?.ref_abbr}
          </button>
        </div>

        <MatrixTable
          referenceState={referenceState}
          otherStates={otherStates}
          group={group}
        />

        <p style={{ fontSize: 11.5, color: 'var(--text-muted)', marginTop: 12, lineHeight: 1.5 }}>
          Fonte: legislação de organização básica / regimento de cada CBM. Estados com mais de uma
          coluna têm a função distribuída em múltiplos órgãos (ex.: capital e interior). Gerado por{' '}
          <code>scripts/build_dpo_cot_comparison.py</code>.
        </p>
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
