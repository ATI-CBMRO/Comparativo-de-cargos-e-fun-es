import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../lib/auth.jsx'

const MENSAGENS = {
  'auth/invalid-credential': 'E-mail ou senha incorretos.',
  'auth/invalid-email': 'E-mail inválido.',
  'auth/missing-password': 'Digite a senha.',
  'auth/too-many-requests': 'Muitas tentativas. Aguarde alguns minutos e tente de novo.',
}

export default function Login() {
  const { entrar, recuperarSenha, naoAutorizado, user } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [erro, setErro] = useState('')
  const [aviso, setAviso] = useState('')
  const [enviando, setEnviando] = useState(false)

  // Só avança quando o usuário for de fato confirmado (evita a corrida do 1º login).
  useEffect(() => {
    if (user) navigate('/revisao', { replace: true })
  }, [user, navigate])

  // Logou no Firebase mas não é membro autorizado: para o "Entrando…".
  useEffect(() => {
    if (naoAutorizado) setEnviando(false)
  }, [naoAutorizado])

  const submeter = async (e) => {
    e.preventDefault()
    setErro(''); setAviso(''); setEnviando(true)
    try {
      await entrar(email, senha)
      // A navegação acontece no useEffect acima, quando `user` for confirmado.
    } catch (err) {
      setErro(MENSAGENS[err.code] ?? 'Não foi possível entrar. Tente novamente.')
      setEnviando(false)
    }
  }

  const esqueci = async () => {
    setErro(''); setAviso('')
    if (!email.trim()) { setErro('Digite seu e-mail acima para receber o link de redefinição.'); return }
    try {
      await recuperarSenha(email)
      setAviso('Enviamos um link de redefinição de senha para o seu e-mail.')
    } catch {
      setErro('Não foi possível enviar o e-mail de redefinição.')
    }
  }

  return (
    <div className="login-wrap">
      <form className="login-card" onSubmit={submeter}>
        <h2 className="login-title">Revisão da Minuta</h2>
        <p className="login-sub">Acesso restrito a convidados</p>

        {naoAutorizado && (
          <div className="login-erro">Seu acesso ainda não foi liberado pelo administrador.</div>
        )}
        {erro && <div className="login-erro">{erro}</div>}
        {aviso && <div className="login-aviso">{aviso}</div>}

        <label className="login-label">E-mail
          <input className="login-input" type="email" value={email}
            onChange={e => setEmail(e.target.value)} autoComplete="email" required />
        </label>
        <label className="login-label">Senha
          <input className="login-input" type="password" value={senha}
            onChange={e => setSenha(e.target.value)} autoComplete="current-password" required />
        </label>

        <button className="login-btn" type="submit" disabled={enviando}>
          {enviando ? 'Entrando…' : 'Entrar'}
        </button>
        <button className="login-link" type="button" onClick={esqueci}>Esqueci minha senha</button>
      </form>
    </div>
  )
}
