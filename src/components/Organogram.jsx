import { useState } from 'react'
import { ChevronRight, Minus, Info } from 'lucide-react'

function OrgNode({ node, level = 0, defaultExpanded = false, onSelect, selectedId }) {
  const [open, setOpen] = useState(level < 2 ? defaultExpanded : false)
  const hasChildren = node.children && node.children.length > 0
  const isSelected = selectedId === node.id

  function handleHeaderClick(e) {
    e.stopPropagation()
    if (hasChildren) setOpen(v => !v)
  }

  function handleInfoClick(e) {
    e.stopPropagation()
    if (onSelect) onSelect(node)
  }

  return (
    <div className={`org-node org-level-${Math.min(level, 3)}`}>
      <div
        className="org-node-header"
        style={{
          paddingLeft: level === 0 ? 12 : 8,
          background: isSelected ? 'rgba(183,28,28,0.15)' : undefined,
          border: isSelected ? '1px solid var(--cbm-red-800)' : '1px solid transparent',
          cursor: 'pointer',
        }}
        onClick={handleHeaderClick}
      >
        {hasChildren ? (
          <ChevronRight
            className={`org-node-toggle ${open ? 'open' : ''}`}
            size={16}
          />
        ) : (
          <Minus className="org-node-toggle leaf" size={14} />
        )}

        <span className="org-node-dot" />

        <span className="org-node-label" style={{ flex: 1 }}>{node.name}</span>

        {node.abbreviation && (
          <span className="org-node-abbr">{node.abbreviation}</span>
        )}

        {node.rank && (
          <span className="org-node-rank" style={{
            fontSize: '11px', color: 'var(--cbm-gold-400)', fontWeight: 600,
            flexShrink: 0, paddingRight: 4, marginLeft: 4,
          }}>
            {node.rank}
          </span>
        )}

        {/* Botão de info — abre o detalhe */}
        {onSelect && (
          <button
            onClick={handleInfoClick}
            title="Ver detalhes deste órgão"
            style={{
              background: isSelected ? 'var(--cbm-red-800)' : 'transparent',
              border: isSelected ? 'none' : '1px solid transparent',
              borderRadius: 5, padding: '2px 4px', cursor: 'pointer',
              color: isSelected ? '#fff' : 'var(--cbm-gray-400)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              flexShrink: 0, marginLeft: 4,
              transition: 'all 0.15s',
            }}
            onMouseEnter={e => {
              if (!isSelected) {
                e.currentTarget.style.background = 'var(--cbm-gray-700)'
                e.currentTarget.style.color = 'var(--text-primary)'
              }
            }}
            onMouseLeave={e => {
              if (!isSelected) {
                e.currentTarget.style.background = 'transparent'
                e.currentTarget.style.color = 'var(--cbm-gray-400)'
              }
            }}
          >
            <Info size={13} />
          </button>
        )}
      </div>

      {node.description && open && (
        <div style={{
          marginLeft: level === 0 ? 54 : 50,
          marginBottom: 6,
          fontSize: '12px',
          color: 'var(--text-muted)',
          lineHeight: '1.55',
          padding: '4px 8px',
          borderLeft: '2px solid var(--cbm-red-900)',
          paddingLeft: 10,
        }}>
          {node.description}
        </div>
      )}

      {hasChildren && (
        <div className="org-children" style={{ display: open ? 'block' : 'none' }}>
          {node.children.map((child, idx) => (
            <OrgNode
              key={child.id || idx}
              node={child}
              level={level + 1}
              defaultExpanded={defaultExpanded}
              onSelect={onSelect}
              selectedId={selectedId}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export default function Organogram({ data, title = 'Organograma', onSelectOrgan, selectedOrganId }) {
  const [allExpanded, setAllExpanded] = useState(false)
  const [key, setKey] = useState(0)

  function handleExpand() {
    setAllExpanded(true)
    setKey(k => k + 1)
  }

  function handleCollapse() {
    setAllExpanded(false)
    setKey(k => k + 1)
  }

  if (!data || data.length === 0) {
    return (
      <div className="empty-state" style={{ padding: '40px 20px' }}>
        <span className="empty-state-icon" style={{ fontSize: 32 }}>🏛</span>
        <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
          Estrutura organizacional não mapeada para este documento.
        </p>
      </div>
    )
  }

  return (
    <div>
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        marginBottom: 16, gap: 12,
      }}>
        <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>
          {onSelectOrgan
            ? 'Clique no ícone ⓘ para ver detalhes completos do órgão'
            : 'Clique nos nós para expandir/colapsar'}
        </span>
        <div style={{ display: 'flex', gap: 8 }}>
          <button className="btn btn-ghost btn-sm" onClick={handleExpand}>
            Expandir Tudo
          </button>
          <button className="btn btn-ghost btn-sm" onClick={handleCollapse}>
            Colapsar Tudo
          </button>
        </div>
      </div>

      <div
        className="organogram-container"
        style={{
          background: 'var(--bg-surface)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid var(--border-subtle)',
        }}
      >
        <div className="org-tree" key={key}>
          {data.map((node, idx) => (
            <OrgNode
              key={node.id || idx}
              node={node}
              level={0}
              defaultExpanded={allExpanded}
              onSelect={onSelectOrgan}
              selectedId={selectedOrganId}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
