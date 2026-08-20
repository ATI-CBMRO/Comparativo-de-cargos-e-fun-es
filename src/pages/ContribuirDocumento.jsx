import { Mail } from 'lucide-react'

// Contribuição por e-mail (2026-08-20): substitui o upload direto pelo portal — o Storage
// do Firebase exigiria o plano Blaze, e a decisão foi manter a conta gratuita. Quem quiser
// enviar um documento manda por e-mail para a equipe do CBMRO; a inclusão no acervo segue
// manual de qualquer forma, então a mudança não afeta a curadoria em si.
const EMAIL_CONTRIBUICAO = 'institucional_bsb_cbmro@cloud.sesdec.ro.gov.br'

export default function ContribuirDocumento() {
  return (
    <div className="pub-envio">
      <h2 className="pub-envio-titulo">Contribuir com o acervo</h2>
      <p className="pub-envio-sub">
        Falta a legislação do seu estado aqui? Envie o PDF por e-mail para a equipe do CBMRO,
        informando o estado/CBM de origem e o tipo de documento (Lei de Organização Básica,
        Regimento Interno, Regulamento de Serviço ou outro). O documento passa por conferência
        antes de entrar no acervo.
      </p>
      <div className="pub-envio-card">
        {/* Botão curto + endereço em texto à parte: são 46 caracteres sem
            espaço onde quebrar, e dentro do botão eles estouravam a largura do
            card no celular. Fora dele, o endereço ainda pode ser selecionado e
            copiado por quem não usa o app de e-mail do aparelho. */}
        <a className="pub-envio-mail" href={`mailto:${EMAIL_CONTRIBUICAO}`}>
          <Mail size={16} aria-hidden="true" />
          Enviar e-mail
        </a>
        <p className="pub-envio-mail-addr">{EMAIL_CONTRIBUICAO}</p>
      </div>
    </div>
  )
}
