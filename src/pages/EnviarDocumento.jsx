import { useState } from 'react'
import { UploadCloud } from 'lucide-react'
import { useVisitante } from '../lib/visitante.jsx'
import { TIPOS_DOCUMENTO, validarEnvio } from '../lib/uploadDocumento.js'
import { enviarDocumento } from '../lib/uploadsData.js'

// Envio de documentos pelo visitante (spec 2026-08-18): um campo único, compartilhado por
// todos os CBMs — a curadoria de cada arquivo é feita depois pelo administrador, fora do
// app. A tela não sabe nada de Storage: quem cuida disso é uploadsData.js.
export default function EnviarDocumento() {
  const { visitante } = useVisitante()
  const [estado, setEstado] = useState('')
  const [tipoDocumento, setTipoDocumento] = useState('')
  const [observacao, setObservacao] = useState('')
  const [arquivo, setArquivo] = useState(null)
  const [erro, setErro] = useState('')
  const [enviado, setEnviado] = useState(false)
  const [enviando, setEnviando] = useState(false)

  const submeter = async (e) => {
    e.preventDefault()
    setErro(''); setEnviado(false)

    const v = validarEnvio({ estado, tipoDocumento, observacao, arquivo })
    if (!v.ok) { setErro(v.erro); return }

    setEnviando(true)
    try {
      await enviarDocumento({
        uid: visitante.uid,
        nomeVisitante: visitante.nome,
        emailVisitante: visitante.email ?? '',
        ...v.dados,
        arquivo,
      })
      // Limpa para permitir outro envio na mesma visita — quem tem um documento costuma
      // ter dois.
      setEstado(''); setTipoDocumento(''); setObservacao(''); setArquivo(null)
      e.target.reset()
      setEnviado(true)
    } catch (err) {
      console.error('Falha ao enviar documento:', err)
      setErro(
        err?.code === 'storage/unauthorized'
          ? 'O envio de arquivos ainda não foi liberado no servidor. Avise o administrador do portal.'
          : 'Não foi possível enviar o documento agora. Tente novamente.',
      )
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div className="pub-envio">
      <h2 className="pub-envio-titulo">Enviar documento ao acervo</h2>
      <p className="pub-envio-sub">
        Falta a legislação do seu estado aqui? Envie o PDF e ele entra na fila de análise da
        equipe do CBMRO. Um documento por envio.
      </p>

      <form className="pub-envio-form" onSubmit={submeter}>
        {erro && <div className="form-error">{erro}</div>}
        {enviado && (
          <div className="pub-envio-ok">
            Recebido, obrigado! O documento entra na fila de análise. Pode enviar outro, se quiser.
          </div>
        )}

        <label className="login-label">Estado / CBM de origem
          <input className="login-input" type="text" value={estado}
            onChange={ev => setEstado(ev.target.value)} maxLength={120} required
            placeholder="Ex.: CBMPA, CBMSC, CBMDF" />
        </label>

        <label className="login-label">Tipo de documento
          <select className="login-input" value={tipoDocumento}
            onChange={ev => setTipoDocumento(ev.target.value)} required>
            <option value="">Escolha…</option>
            {TIPOS_DOCUMENTO.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
        </label>

        <label className="login-label">Observação (opcional)
          <textarea className="login-input pub-envio-obs" value={observacao}
            onChange={ev => setObservacao(ev.target.value)} maxLength={1000} rows={3}
            placeholder="Ex.: publicado no Diário Oficial de 03/2025; substitui a lei anterior" />
        </label>

        <label className="login-label">Arquivo (PDF, até 20 MB)
          <input className="login-input" type="file" accept="application/pdf"
            onChange={ev => setArquivo(ev.target.files?.[0] ?? null)} required />
        </label>

        <button className="login-btn" type="submit" disabled={enviando}>
          <UploadCloud size={16} /> {enviando ? 'Enviando…' : 'Enviar documento'}
        </button>

        <p className="pub-lgpd">
          Seu nome, e-mail e instituição acompanham o envio, para o administrador saber a
          origem do documento. O arquivo é analisado antes de qualquer publicação no acervo.
        </p>
      </form>
    </div>
  )
}
