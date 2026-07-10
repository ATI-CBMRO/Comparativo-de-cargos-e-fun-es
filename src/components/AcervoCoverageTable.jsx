// Tabela-resumo do Acervo (modelo "grupos por cobertura"). Uma linha por
// estado, colunas LOB / Regimento Interno / Regulamento de Serviço, agrupadas
// por quais documentos o estado possui. Componente puro — recebe as linhas já
// agregadas (buildCoverageRows) e um callback de navegação. Duas visões:
// "Matriz" (agrupada) e "Por documento" (estados em colunas por tipo). Clicar
// numa coluna filtra só os estados que possuem aquele documento. Ver design
// docs/superpowers/specs/2026-07-09-acervo-tabela-cobertura-design.md.
import { Fragment, useState } from 'react'

const COLUMNS = [
  { key: 'lob', label: 'LOB', seal: false },
  { key: 'regimento', label: 'Regimento Interno', seal: true },
  { key: 'regulamento', label: 'Regulamento de Serviço', seal: true },
]

// Grupos por cobertura, em prioridade: um estado entra no primeiro que casar.
const GROUPS = [
  { id: 'ri', title: 'Com Regimento Interno', match: r => r.columns.regimento.present },
  { id: 'rg', title: 'Com Regulamento de Serviço', match: r => r.columns.regulamento.present },
  { id: 'lob', title: 'Somente LOB', match: r => !r.columns.regimento.present && !r.columns.regulamento.present },
]

// Estado de uma célula: 'ok' | 'warn' (colunas com selo) | 'yes' (LOB) | 'no'.
function cellStatus(cell, seal) {
  if (!cell.present) return 'no'
  if (!seal) return 'yes'
  return cell.verified === true ? 'ok' : 'warn'
}

const CELL_LABEL = { ok: '✓ sim', warn: '⚠ sim', yes: 'sim', no: '—' }
const CELL_TITLE = {
  ok: 'Tipo conferido lendo o conteúdo do documento, não só o nome do arquivo.',
  warn: 'Tipo ainda não conferido por conteúdo — classificação só pelo nome do arquivo, pode estar incorreta.',
  yes: 'Documento presente no acervo.',
  no: 'Não possui no acervo.',
}

function Cell({ cell, seal }) {
  const s = cellStatus(cell, seal)
  const suffix = cell.count > 1 ? <sup className="acervo-cov-count">+{cell.count}</sup> : null
  return (
    <span className={`acervo-cov-pill is-${s}`} title={CELL_TITLE[s]} aria-label={CELL_LABEL[s]}>
      {CELL_LABEL[s]}{suffix}
    </span>
  )
}

// Distribui as linhas visíveis nos grupos (cada estado num só grupo).
function groupRows(rows) {
  const used = new Set()
  return GROUPS.map(g => {
    const items = rows.filter(r => !used.has(r.stateId) && g.match(r))
    items.forEach(r => used.add(r.stateId))
    return { ...g, items }
  }).filter(g => g.items.length > 0)
}

function MatrixView({ groups, filterCol, onToggle, onSelectState }) {
  return (
    <div className="acervo-cov-wrap">
      <table className="acervo-cov-table">
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
                    <button
                      type="button"
                      className="acervo-cov-state"
                      onClick={() => onSelectState(r.stateId)}
                      title={`Abrir a página de ${r.stateName}`}
                    >
                      <span className="acervo-cov-abbr">{r.abbreviation}</span>
                      <span className="acervo-cov-name">{r.stateName}</span>
                    </button>
                  </th>
                  {COLUMNS.map(c => (
                    <td key={c.key} className={`acervo-cov-cell ${filterCol === c.key ? 'is-active' : ''}`}>
                      <Cell cell={r.columns[c.key]} seal={c.seal} />
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
                const s = cellStatus(r.columns[c.key], c.seal)
                return (
                  <button
                    key={r.stateId}
                    type="button"
                    className="acervo-cov-stitem"
                    onClick={() => onSelectState(r.stateId)}
                    title={`Abrir a página de ${r.stateName}`}
                  >
                    <span className="acervo-cov-abbr">{r.abbreviation}</span>
                    <span className="acervo-cov-name">{r.stateName}</span>
                    {c.seal && <span className={`acervo-cov-mk is-${s}`}>{s === 'ok' ? '✓' : '⚠'}</span>}
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

export default function AcervoCoverageTable({ rows, onSelectState }) {
  const [view, setView] = useState('matriz')
  const [filterCol, setFilterCol] = useState(null)
  if (!rows || rows.length === 0) return null

  const toggleFilter = key => setFilterCol(prev => (prev === key ? null : key))
  const visible = filterCol ? rows.filter(r => r.columns[filterCol].present) : rows
  const groups = groupRows(visible)
  const countPresent = key => rows.filter(r => r.columns[key].present).length

  return (
    <section className="acervo-cov">
      <div className="acervo-cov-head">
        <div className="acervo-cov-title">Cobertura por estado</div>
        <div className="acervo-cov-tabs" role="tablist" aria-label="Modo de visualização">
          <button
            type="button" role="tab" aria-selected={view === 'matriz'}
            className={view === 'matriz' ? 'is-on' : ''} onClick={() => setView('matriz')}
          >Matriz</button>
          <button
            type="button" role="tab" aria-selected={view === 'doc'}
            className={view === 'doc' ? 'is-on' : ''} onClick={() => setView('doc')}
          >Por documento</button>
        </div>
      </div>

      <div className="acervo-cov-filters">
        <span className="acervo-cov-flabel">Filtrar:</span>
        {COLUMNS.map(c => (
          <button
            key={c.key} type="button"
            className={`acervo-cov-chip ${filterCol === c.key ? 'is-on' : ''}`}
            onClick={() => toggleFilter(c.key)}
            aria-pressed={filterCol === c.key}
          >
            {c.label}<span className="acervo-cov-chipn">{countPresent(c.key)}</span>
          </button>
        ))}
        {filterCol && (
          <button type="button" className="acervo-cov-chip is-clear" onClick={() => setFilterCol(null)}>
            ✕ Limpar
          </button>
        )}
      </div>

      {view === 'matriz'
        ? <MatrixView groups={groups} filterCol={filterCol} onToggle={toggleFilter} onSelectState={onSelectState} />
        : <DocumentView rows={rows} filterCol={filterCol} onToggle={toggleFilter} onSelectState={onSelectState} />}

      <p className="acervo-cov-legend">
        <span className="acervo-cov-pill is-ok">✓ sim</span> conferido por conteúdo ·{' '}
        <span className="acervo-cov-pill is-warn">⚠ sim</span> só por nome de arquivo ·{' '}
        <span className="acervo-cov-pill is-yes">sim</span> possui (LOB) ·{' '}
        <span className="acervo-cov-dash">—</span> não possui
      </p>
    </section>
  )
}
