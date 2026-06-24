// Organograma caixas-e-linhas (CSS puro) da cadeia de comando da minuta.
// `chart` é o nó raiz (commandChart); cada nó: { organKey, sigla, label, chapterId, children }.
// A raiz é sintética (synthetic:true, sem chapterId) e não é clicável.

function ChartNode({ node, onSelect, selectedId }) {
  const kids = node.children || []
  const clickable = !node.synthetic && node.chapterId
  const selected = clickable && node.chapterId === selectedId
  const cls = `moc-box${node.synthetic ? ' moc-box-root' : ''}${selected ? ' moc-box-sel' : ''}`

  const inner = (
    <>
      {node.sigla ? <span className="moc-sigla">{node.sigla}</span> : null}
      <span className="moc-label">{node.label}</span>
    </>
  )

  return (
    <li>
      {clickable ? (
        <button type="button" className={cls} onClick={() => onSelect(node.chapterId)}>
          {inner}
        </button>
      ) : (
        <div className={cls}>{inner}</div>
      )}
      {kids.length > 0 && (
        <ul>
          {kids.map(c => (
            <ChartNode key={c.organKey || c.label} node={c} onSelect={onSelect} selectedId={selectedId} />
          ))}
        </ul>
      )}
    </li>
  )
}

export default function MinutaOrgChart({ chart, onSelect, selectedId }) {
  if (!chart) return null
  return (
    <div className="moc-tree">
      <ul>
        <ChartNode node={chart} onSelect={onSelect} selectedId={selectedId} />
      </ul>
    </div>
  )
}
