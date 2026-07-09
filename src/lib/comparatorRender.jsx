/* Helpers de render compartilhados pela matriz de comparação (verbatim). */
import { highlightSegments } from './highlightSegments.js'

export function renderFriendlyText(text) {
  if (!text) return <span className="cc-empty">—</span>
  return (
    <span>
      {highlightSegments(text).map((seg, i) => (seg.bold ? <strong key={i}>{seg.text}</strong> : <span key={i}>{seg.text}</span>))}
    </span>
  )
}

export function List({ items }) {
  if (!items || items.length === 0) return <span className="cc-empty">—</span>
  return <ul className="cc-list">{items.map((it, i) => <li key={i}>{renderFriendlyText(it)}</li>)}</ul>
}

function organAtribuicoes(organ) {
  if (organ.atribuicoes && organ.atribuicoes.length) return organ.atribuicoes
  const out = []
  for (const c of organ.cargos || []) for (const a of c.atribuicoes || []) out.push(a)
  return out
}

export const MATRIX_ROWS = [
  { key: 'organ', label: 'Órgão / Sigla', render: o => (
      <div>
        <div className="oc-organ-name">{renderFriendlyText(o.name || '—')}</div>
        {o.abbreviation && <div className="oc-organ-sub"><span className="oc-organ-abbr">{o.abbreviation}</span></div>}
      </div>
    ) },
  { key: 'subord', label: 'Subordinação', render: o => o.subordinadoA
      ? <span className="oc-sub">{renderFriendlyText(o.subordinadoA)}</span>
      : <span className="cc-empty">—</span> },
  { key: 'cargos', label: 'Cargo / Função', render: o => {
      const names = (o.cargos || []).map(c => c.cargo).filter(Boolean)
      return names.length
        ? <ul className="cc-list">{names.map((n, i) => <li key={i}>{renderFriendlyText(n)}</li>)}</ul>
        : <span className="cc-empty">—</span>
    } },
  { key: 'req', label: 'Requisito / Posto', render: o => {
      const reqs = [...new Set((o.cargos || []).map(c => c.requisito).filter(Boolean))]
      return reqs.length
        ? <ul className="cc-list">{reqs.map((r, i) => <li key={i}>{renderFriendlyText(r)}</li>)}</ul>
        : <span className="cc-empty">—</span>
    } },
  { key: 'atrib', label: 'Atribuições / Competências', render: o => <List items={organAtribuicoes(o)} /> },
  { key: 'desd', label: 'Desdobramentos', render: o => <List items={o.desdobramentos} /> },
]
