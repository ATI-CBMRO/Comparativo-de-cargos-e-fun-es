// Acervo Legal — bloco de cobertura com 3 visões (subabas):
//  • "Tabela": matriz agrupada por documentação (Com Regimento Interno / Com
//    Regulamento de Serviço / Somente LOB). Cada célula lista os documentos como
//    etiquetas com o número da lei; clicar abre o PDF num popup. A coluna
//    Regulamento de Serviço recebe acento azul (barra/ícone), mantendo o padrão
//    neutro da tabela.
//  • "Por documento": três colunas (LOB / RI / Regulamento) com os estados que
//    possuem cada tipo.
//  • "Documentos por estado": relação detalhada, com busca e botão de PDF.
// Clicar no nome de uma coluna filtra os estados que possuem aquele documento.
// Componente puro — recebe as linhas agregadas (buildCoverageRows) e um callback
// de navegação. Ver docs/superpowers/specs/2026-07-09-acervo-tabela-cobertura-design.md.
import { Fragment, useEffect, useState } from 'react'
import { FileText, Search, X, ExternalLink } from 'lucide-react'

const COLUMNS = [
  { key: 'lob', label: 'LOB', seal: false },
  { key: 'regimento', label: 'Regimento Interno', seal: true },
  { key: 'regulamento', label: 'Regulamento de Serviço', seal: true },
]
const SHORT = { lob: 'LOB', regimento: 'RI', regulamento: 'Reg.', outros: 'Doc.' }
const TYPE_SHORT = {
  'Lei de Organização Básica': 'LOB',
  'Regimento Interno': 'RI',
  'Regimento de Serviços': 'Reg.',
  'Regulamento Geral': 'Reg.',
  'Normas Gerais de Ação': 'NGA',
  'Quadro Demonstrativo de Cargos': 'QDC',
  'Quadro de Organização e Distribuição': 'QOD',
}

// Grupos por cobertura, em prioridade: um estado entra no primeiro que casar.
const GROUPS = [
  { id: 'ri', title: 'Com Regimento Interno', match: r => r.columns.regimento.present },
  { id: 'rg', title: 'Com Regulamento de Serviço', match: r => r.columns.regulamento.present },
  { id: 'lob', title: 'Somente LOB', match: r => !r.columns.regimento.present && !r.columns.regulamento.present },
]

function groupRows(rows) {
  const used = new Set()
  return GROUPS.map(g => {
    const items = rows.filter(r => !used.has(r.stateId) && g.match(r))
    items.forEach(r => used.add(r.stateId))
    return { ...g, items }
  }).filter(g => g.items.length > 0)
}

// Etiqueta de um documento na tabela. Barra colorida = status (verde conferido /
// âmbar só por nome / vermelho para a LOB); Regulamento usa acento azul.
function Tag({ doc, colKey, seal, onOpen }) {
  const s = seal ? (doc.verified ? 'ok' : 'warn') : 'yes'
  const cls = `acervo-tag col-${colKey} st-${s}${doc.pdf ? '' : ' np'}`
  const inner = (
    <>
      <span className="acervo-tag-bar" />
      <FileText size={13} className="acervo-tag-ico" />
      <span className="acervo-tag-num">{doc.label}</span>
      {doc.pdf && <span className="acervo-tag-go">abrir ›</span>}
    </>
  )
  if (!doc.pdf) return <span className={cls} title="Sem PDF no acervo">{inner}</span>
  return (
    <button type="button" className={cls} onClick={() => onOpen(doc)} title={`Abrir o PDF — ${doc.label}`}>
      {inner}
    </button>
  )
}

function TableCell({ cell, colKey, seal, onOpen }) {
  if (!cell.present) return <span className="acervo-cov-dash">—</span>
  return (
    <div className="acervo-tags">
      {cell.docs.map((d, i) => <Tag key={i} doc={d} colKey={colKey} seal={seal} onOpen={onOpen} />)}
    </div>
  )
}

function MatrixView({ groups, filterCol, onToggle, onSelectState, onOpenPdf }) {
  return (
    <div className="acervo-cov-wrap">
      <table className="acervo-cov-table">
        <colgroup>
          <col className="acervo-col-st" />
          {COLUMNS.map(c => <col key={c.key} className="acervo-col-doc" />)}
        </colgroup>
        <thead>
          <tr>
            <th scope="col">Estado</th>
            {COLUMNS.map(c => (
              <th key={c.key} scope="col" className={`acervo-cov-colh ${filterCol === c.key ? 'is-active' : ''}`}>
                <button type="button" onClick={() => onToggle(c.key)} title={`Filtrar estados com ${c.label}`}>
                  {c.label}
                </button>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {groups.map(g => (
            <Fragment key={g.id}>
              <tr className="acervo-cov-grouphd">
                <td colSpan={COLUMNS.length + 1}>{g.title} · {g.items.length}</td>
              </tr>
              {g.items.map(r => (
                <tr key={r.stateId}>
                  <th scope="row">
                    <button type="button" className="acervo-cov-state" onClick={() => onSelectState(r.stateId)} title={`Abrir a página de ${r.stateName}`}>
                      <span className="acervo-cov-abbr">{r.abbreviation}</span>
                      <span className="acervo-cov-name">{r.stateName}</span>
                    </button>
                  </th>
                  {COLUMNS.map(c => (
                    <td key={c.key} className={`acervo-cov-cell ${filterCol === c.key ? 'is-active' : ''}`}>
                      <TableCell cell={r.columns[c.key]} colKey={c.key} seal={c.seal} onOpen={onOpenPdf} />
                    </td>
                  ))}
                </tr>
              ))}
            </Fragment>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function DocumentView({ rows, filterCol, onToggle, onSelectState }) {
  return (
    <div className="acervo-cov-doccols">
      {COLUMNS.map(c => {
        const have = rows.filter(r => r.columns[c.key].present)
        return (
          <div key={c.key} className={`acervo-cov-doccol ${filterCol === c.key ? 'is-active' : ''}`}>
            <button type="button" className="acervo-cov-doccol-hd" onClick={() => onToggle(c.key)}>
              <b>{c.label}</b>
              <span className="acervo-cov-doccol-n">{have.length} estados</span>
            </button>
            <div className="acervo-cov-doccol-body">
              {have.length === 0 ? (
                <span className="acervo-cov-empty">Nenhum estado no acervo.</span>
              ) : have.map(r => {
                const ok = r.columns[c.key].verified === true
                return (
                  <button key={r.stateId} type="button" className="acervo-cov-stitem" onClick={() => onSelectState(r.stateId)} title={`Abrir a página de ${r.stateName}`}>
                    <span className="acervo-cov-abbr">{r.abbreviation}</span>
                    <span className="acervo-cov-name">{r.stateName}</span>
                    {c.seal && <span className={`acervo-cov-mk is-${ok ? 'ok' : 'warn'}`}>{ok ? '✓' : '⚠'}</span>}
                  </button>
                )
              })}
            </div>
          </div>
        )
      })}
    </div>
  )
}

// Relação detalhada (antes ficava abaixo da tabela). Busca por estado, sigla,
// tipo ou número da lei; um card por estado com seus documentos e botão de PDF.
function DetailView({ rows, onSelectState, onOpenPdf }) {
  const [query, setQuery] = useState('')
  const q = query.trim().toLowerCase()

  const cards = rows.map(r => ({ ...r, docs: r.documents || [] })).map(card => ({
    ...card,
    docs: !q ? card.docs : card.docs.filter(d =>
      card.stateName.toLowerCase().includes(q)
      || card.abbreviation?.toLowerCase().includes(q)
      || card.cbmAbbr?.toLowerCase().includes(q)
      || card.cbmName?.toLowerCase().includes(q)
      || d.type?.toLowerCase().includes(q)
      || d.label?.toLowerCase().includes(q)
      || d.lawText?.toLowerCase().includes(q)
    ),
    matchState: !q
      || card.stateName.toLowerCase().includes(q)
      || card.abbreviation?.toLowerCase().includes(q)
      || card.cbmAbbr?.toLowerCase().includes(q)
      || card.cbmName?.toLowerCase().includes(q),
  })).filter(card => card.docs.length > 0 || card.matchState)

  const total = cards.reduce((acc, c) => acc + c.docs.length, 0)

  return (
    <div className="acervo-detail">
      <div className="acervo-detail-search">
        <Search size={16} className="acervo-detail-search-ico" />
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Buscar por estado, sigla, tipo de documento ou número da lei..."
        />
      </div>
      <p className="acervo-detail-count">{total} documento{total !== 1 ? 's' : ''} em {cards.length} estado{cards.length !== 1 ? 's' : ''}.</p>
      {cards.length === 0 ? (
        <div className="acervo-cov-empty" style={{ padding: 24 }}>Nenhuma legislação encontrada. Tente ajustar a busca.</div>
      ) : (
        <div className="acervo-detail-grid">
          {cards.map(card => (
            <div key={card.stateId} className="acervo-detail-card">
              <button type="button" className="acervo-detail-hd" onClick={() => onSelectState(card.stateId)} title={`Abrir a página de ${card.stateName}`}>
                <span className="acervo-cov-abbr">{card.abbreviation}</span>
                <span className="acervo-detail-hd-meta">
                  <b>{card.stateName}</b>
                  {card.cbmAbbr && <small>{card.cbmAbbr}{card.cbmName ? ` · ${card.cbmName}` : ''}</small>}
                </span>
              </button>
              <div className="acervo-detail-bd">
                {card.docs.length === 0 ? (
                  <div className="acervo-detail-row"><span className="acervo-cov-empty">Nenhum documento neste filtro.</span></div>
                ) : card.docs.map((d, i) => (
                  <div key={i} className="acervo-detail-row">
                    <span className={`acervo-detail-tag col-${d.bucket}`}>{TYPE_SHORT[d.type] || SHORT[d.bucket]}</span>
                    <div className="acervo-detail-info">
                      <div className="acervo-detail-title">{d.type}{d.lawText && <span className="acervo-detail-law"> · {d.lawText}</span>}</div>
                      <div className="acervo-detail-sub">
                        {d.year ? `${d.year}` : ''}{d.year && d.charCount ? ' · ' : ''}{d.charCount ? `${Math.round(d.charCount / 1000)}k car.` : ''}
                        {d.bucket !== 'lob' && (d.verified ? ' · ✓ conferido' : ' · ⚠ só por nome')}
                      </div>
                    </div>
                    {d.pdf
                      ? <button type="button" className="acervo-detail-pdf" onClick={() => onOpenPdf(d)}><ExternalLink size={13} /> PDF</button>
                      : <span className="acervo-detail-nopdf">sem PDF</span>}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function PdfModal({ doc, onClose }) {
  useEffect(() => {
    const onKey = e => { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [onClose])
  return (
    <div className="acervo-pdf-ov" onClick={e => { if (e.target === e.currentTarget) onClose() }}>
      <div className="acervo-pdf-modal" role="dialog" aria-modal="true" aria-label={`PDF — ${doc.label}`}>
        <div className="acervo-pdf-hd">
          <div className="acervo-pdf-title">
            <b>{doc.type} — {doc.label}</b>
            {doc.lawText && <small>{doc.lawText}</small>}
          </div>
          <a className="acervo-pdf-ext" href={doc.pdf} target="_blank" rel="noreferrer" title="Abrir em nova aba"><ExternalLink size={15} /></a>
          <button type="button" className="acervo-pdf-x" onClick={onClose} aria-label="Fechar"><X size={17} /></button>
        </div>
        <iframe className="acervo-pdf-frame" src={doc.pdf} title={`PDF ${doc.label}`} />
      </div>
    </div>
  )
}

export default function AcervoCoverageTable({ rows, onSelectState }) {
  const [view, setView] = useState('tabela')
  const [filterCol, setFilterCol] = useState(null)
  const [pdfDoc, setPdfDoc] = useState(null)
  if (!rows || rows.length === 0) return null

  const toggleFilter = key => setFilterCol(prev => (prev === key ? null : key))
  const visible = filterCol ? rows.filter(r => r.columns[filterCol].present) : rows
  const groups = groupRows(visible)

  const TABS = [
    { id: 'tabela', label: 'Tabela' },
    { id: 'pordoc', label: 'Por documento' },
    { id: 'docs', label: 'Documentos por estado' },
  ]

  return (
    <section className="acervo-cov">
      <div className="acervo-cov-head">
        <div className="acervo-cov-title">Cobertura por estado</div>
        <div className="acervo-cov-tabs" role="tablist" aria-label="Modo de visualização">
          {TABS.map(t => (
            <button key={t.id} type="button" role="tab" aria-selected={view === t.id}
              className={view === t.id ? 'is-on' : ''} onClick={() => setView(t.id)}>
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {view !== 'docs' && (
        <div className="acervo-cov-hint">
          Clique no nome de uma coluna para filtrar os estados que possuem o documento.
          {filterCol && (
            <button type="button" className="acervo-cov-clear" onClick={() => setFilterCol(null)}>
              ✕ limpar filtro ({COLUMNS.find(c => c.key === filterCol).label})
            </button>
          )}
        </div>
      )}

      {view === 'tabela' && (
        <MatrixView groups={groups} filterCol={filterCol} onToggle={toggleFilter} onSelectState={onSelectState} onOpenPdf={setPdfDoc} />
      )}
      {view === 'pordoc' && (
        <DocumentView rows={rows} filterCol={filterCol} onToggle={toggleFilter} onSelectState={onSelectState} />
      )}
      {view === 'docs' && (
        <DetailView rows={rows} onSelectState={onSelectState} onOpenPdf={setPdfDoc} />
      )}

      {view !== 'docs' && (
        <p className="acervo-cov-legend">
          <span className="acervo-cov-mk is-ok">✓</span> conferido por conteúdo ·{' '}
          <span className="acervo-cov-mk is-warn">⚠</span> só por nome de arquivo ·{' '}
          <span className="acervo-cov-dash">—</span> não possui
        </p>
      )}

      {pdfDoc && <PdfModal doc={pdfDoc} onClose={() => setPdfDoc(null)} />}
    </section>
  )
}
