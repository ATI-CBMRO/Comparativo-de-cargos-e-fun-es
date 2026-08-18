import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useVisitante } from '../lib/visitante.jsx'

export default function CadastroVisitante() {
  const { entrar, erro } = useVisitante()
  const [nome, setNome] = useState('')
  const [email, setEmail] = useState('')
  const [instituicao, setInstituicao] = useState('')
  const [enviando, setEnviando] = useState(false)

  const submeter = async (e) => {
    e.preventDefault()
    setEnviando(true)
    const ok = await entrar({ nome, email, instituicao })
    // Deu certo: o VisitanteProvider troca a tela sozinho. Deu errado: `erro` aparece
    // abaixo e o botão volta a ficar clicável.
    if (!ok) setEnviando(false)
  }

  return (
    <div className="login-wrap">
      <form className="login-card login-card--wide" onSubmit={submeter}>
        <h2 className="login-title">Acervo Legal — consulta pública</h2>
        <p className="login-sub">
          Legislação comparada dos 27 Corpos de Bombeiros Militares. Informe seus dados para consultar.
        </p>

        {erro && <div className="form-error">{erro}</div>}

        <label className="login-label">Nome completo
          <input className="login-input" type="text" value={nome}
            onChange={e => setNome(e.target.value)} autoComplete="name" maxLength={200} required />
        </label>
        <label className="login-label">E-mail
          <input className="login-input" type="email" value={email}
            onChange={e => setEmail(e.target.value)} autoComplete="email" maxLength={200} required />
        </label>
        <label className="login-label">Instituição ou órgão
          <input className="login-input" type="text" value={instituicao}
            onChange={e => setInstituicao(e.target.value)} maxLength={200} required
            placeholder="Ex.: CBMPA, Prefeitura de Porto Velho, autônomo" />
        </label>

        <button className="login-btn" type="submit" disabled={enviando}>
          {enviando ? 'Entrando…' : 'Consultar o acervo'}
        </button>

        <p className="pub-lgpd">
          Estes dados ficam registrados como controle de acesso ao acervo e são vistos
          apenas pelo administrador do portal. Não há envio de mensagens.
        </p>

        <div className="login-foot">
          <span className="login-foot-txt">É membro do grupo de trabalho?</span>
          <Link className="login-link" to="/login">Entrar</Link>
        </div>
      </form>
    </div>
  )
}
