import { useState } from 'react'
import JanelaSeparada from './JanelaSeparada.jsx'
import RegistroDecisaoForm from './RegistroDecisaoForm.jsx'

const AVISO_BLOQUEIO = 'O navegador bloqueou a janela separada. Libere pop-ups para este '
  + 'site se quiser preencher a decisão ao lado da tela de Decisões.'

// Escolhe a moldura do formulário: janela separada do navegador (para consultar a
// Questão e os excertos das candidatas enquanto se redige) e, se o pop-up for
// bloqueado, o overlay de sempre com um aviso — nunca um caminho morto.
export default function RegistroDecisaoModal(props) {
  const [bloqueada, setBloqueada] = useState(false)

  if (bloqueada) {
    return (
      <div className="decm-overlay" role="dialog" aria-modal="true">
        <RegistroDecisaoForm key={props.decisao.id} {...props} aviso={AVISO_BLOQUEIO} />
      </div>
    )
  }
  return (
    <JanelaSeparada
      titulo={`Registrar decisão — ${props.decisao.titulo}`}
      nome="registro-decisao"
      onFechar={props.onClose}
      onBloqueada={() => setBloqueada(true)}
    >
      <RegistroDecisaoForm key={props.decisao.id} {...props} />
    </JanelaSeparada>
  )
}
