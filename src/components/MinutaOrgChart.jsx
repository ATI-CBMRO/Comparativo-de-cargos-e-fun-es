// Organograma caixas-e-linhas (CSS puro) da cadeia de comando da minuta.
// `chart` é o nó raiz (commandChart); cada nó: { organKey, sigla, label, chapterId, children }.
// A raiz normalmente é um órgão real (ex.: Comando-Geral) e é clicável; só cai no caso
// sintético (synthetic:true, sem chapterId, não clicável) se houver 0 ou 2+ raízes
// desconexas na cadeia de comando — ver build_command_chart em build_minuta_structure.py.
//
// Árvore dinâmica: nós com filhos têm um botão −/+ (moc-toggle) que expande/recolhe
// a subárvore; o clique na CAIXA continua abrindo o painel de detalhe. A raiz (real ou
// sintética) fica sempre expandida via a prop `isRoot`; os demais nós iniciam conforme
// `defaultExpanded` (recolhidos por padrão → só os filhos diretos visíveis). Trocar
// `defaultExpanded` + remontar (via `key` na árvore) reaplica "expandir/recolher tudo".

import { useState } from 'react'

function ChartNode({ node, onSelect, selectedId, defaultExpanded, isRoot = false }) {
  const kids = node.children || []
  const hasKids = kids.length > 0
  const clickable = !node.synthetic && node.chapterId
  const selected = clickable && node.chapterId === selectedId
  const [open, setOpen] = useState(isRoot || node.synthetic ? true : defaultExpanded)
  const cls = `moc-box${node.synthetic ? ' moc-box-root' : ''}${selected ? ' moc-box-sel' : ''}`
  const showToggle = hasKids && !node.synthetic
  const name = node.sigla || node.label || 'nó'

  const inner = (
    <>
      {node.sigla ? <span className="moc-sigla">{node.sigla}</span> : null}
      <span className="moc-label">{node.label}</span>
    </>
  )

  return (
    <li>
      <div className="moc-node">
        {clickable ? (
          <button type="button" className={cls} onClick={() => onSelect(node.chapterId)}>
            {inner}
          </button>
        ) : (
          <div className={cls}>{inner}</div>
        )}
        {showToggle && (
          <button
            type="button"
            className={`moc-toggle${open ? ' open' : ''}`}
            onClick={() => setOpen(v => !v)}
            aria-expanded={open}
            aria-label={`${open ? 'Recolher' : 'Expandir'} ${name}`}
            title={open ? 'Recolher' : `Expandir (${kids.length})`}
          >
            {open ? '−' : '+'}
          </button>
        )}
      </div>
      {hasKids && open && (
        <ul>
          {kids.map(c => (
            <ChartNode
              key={c.organKey || c.label}
              node={c}
              onSelect={onSelect}
              selectedId={selectedId}
              defaultExpanded={defaultExpanded}
            />
          ))}
        </ul>
      )}
    </li>
  )
}

export default function MinutaOrgChart({ chart, onSelect, selectedId, defaultExpanded = false }) {
  if (!chart) return null
  return (
    <div className="moc-tree">
      <ul>
        <ChartNode
          node={chart}
          onSelect={onSelect}
          selectedId={selectedId}
          defaultExpanded={defaultExpanded}
          isRoot
        />
      </ul>
    </div>
  )
}
