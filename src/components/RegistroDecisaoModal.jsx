import RegistroDecisaoForm from './RegistroDecisaoForm.jsx'

// Moldura do registro de decisão. Nesta task ainda é o overlay de sempre; a Task 2
// troca por janela separada, mantendo este overlay como fallback de pop-up bloqueado.
export default function RegistroDecisaoModal(props) {
  return (
    <div className="decm-overlay" role="dialog" aria-modal="true">
      <RegistroDecisaoForm {...props} />
    </div>
  )
}
