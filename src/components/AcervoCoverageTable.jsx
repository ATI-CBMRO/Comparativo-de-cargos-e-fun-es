// Tabela-resumo do Acervo: uma linha por estado, colunas LOB / Regimento
// Interno / Regulamento de Serviço. Componente puro — recebe as linhas já
// agregadas (buildCoverageRows) e um callback de navegação. Ver design
// docs/superpowers/specs/2026-07-09-acervo-tabela-cobertura-design.md.

const COLUMNS = [
  { key: 'lob', label: 'LOB', seal: false },
  { key: 'regimento', label: 'Regimento Interno', seal: true },
  { key: 'regulamento', label: 'Regulamento de Serviço', seal: true },
]

// Conteúdo de uma célula de tipo. Ausente => travessão. Presente => selo
// (✓/⚠ só nas colunas com seal) + sufixo +N quando há mais de um documento.
function CellContent({ cell, seal }) {
  if (!cell.present) {
    return <span className="acervo-cov-dash" aria-label="não possui">—</span>
  }
  const suffix = cell.count > 1 ? <span className="acervo-cov-count">+{cell.count}</span> : null
  if (!seal) {
    // Coluna LOB: só presença.
    return <span className="acervo-cov-has">possui{suffix}</span>
  }
  const ok = cell.verified === true
  return (
    <span
      className={`acervo-cov-seal ${ok ? 'is-ok' : 'is-warn'}`}
      title={ok
        ? 'Tipo conferido lendo o conteúdo do documento, não só o nome do arquivo.'
        : 'Tipo ainda não conferido por conteúdo — classificação só pelo nome do arquivo, pode estar incorreta.'}
    >
      {ok ? '✓' : '⚠'}{suffix}
    </span>
  )
}

export default function AcervoCoverageTable({ rows, onSelectState }) {
  if (!rows || rows.length === 0) return null
  return (
    <section className="acervo-cov">
      <div className="acervo-cov-title">Cobertura por estado</div>
      <div className="acervo-cov-wrap">
        <table className="acervo-cov-table">
          <thead>
            <tr>
              <th scope="col">Estado</th>
              {COLUMNS.map(c => <th key={c.key} scope="col">{c.label}</th>)}
            </tr>
          </thead>
          <tbody>
            {rows.map(r => (
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
                {COLUMNS.map(c => {
                  const cell = r.columns[c.key]
                  return (
                    <td key={c.key} className="acervo-cov-cell">
                      {cell.present ? (
                        <button
                          type="button"
                          className="acervo-cov-cellbtn"
                          onClick={() => onSelectState(r.stateId)}
                          title={`Abrir a página de ${r.stateName}`}
                        >
                          <CellContent cell={cell} seal={c.seal} />
                        </button>
                      ) : (
                        <CellContent cell={cell} seal={c.seal} />
                      )}
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="acervo-cov-legend">
        <span className="acervo-cov-seal is-ok">✓</span> tipo conferido por conteúdo ·{' '}
        <span className="acervo-cov-seal is-warn">⚠</span> só por nome de arquivo ·{' '}
        <span className="acervo-cov-dash">—</span> não possui
      </p>
    </section>
  )
}
