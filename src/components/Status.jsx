// Componentes compartilhados de estado de tela (carregando / erro / vazio), sobre as
// classes já existentes em src/index.css (.empty-state, .spinner) — usados no lugar dos
// blocos ad hoc espalhados pelas páginas, para loading/erro terem a mesma cara em todo lugar.
import { Flame } from 'lucide-react'

export function LoadingState({ label = 'Carregando…' }) {
  return (
    <div
      role="status" aria-live="polite"
      style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 12, minHeight: '50vh' }}
    >
      <div className="spinner" />
      {label && <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>{label}</p>}
    </div>
  )
}

export function ErrorState({ icon: Icon = Flame, title = 'Erro ao carregar', hint }) {
  return (
    <div className="empty-state" role="alert" style={{ marginTop: 80 }}>
      <Icon size={40} className="empty-state-icon" />
      <h3>{title}</h3>
      {hint && <p>{hint}</p>}
    </div>
  )
}

export function EmptyState({ icon: Icon = Flame, title, text }) {
  return (
    <div className="empty-state" style={{ marginTop: 80 }}>
      <Icon size={40} className="empty-state-icon" />
      {title && <h3>{title}</h3>}
      {text && <p>{text}</p>}
    </div>
  )
}
