import { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useAuth } from '../lib/auth.jsx'

const MENSAGENS = {
  'auth/email-already-in-use': 'Este e-mail já tem cadastro. Use a tela de login.',
  'auth/invalid-email': 'E-mail inválido.',
  'auth/weak-password': 'A senha precisa ter ao menos 6 caracteres.',
}

export default function Cadastro() {
  const { cadastrar, naoAutorizado } = useAuth()
  const [searchParams] = useSearchParams()
  // Link de convite (gerado em Acessos) já chega com o e-mail liberado — poupa
  // digitação e evita erro de digitação num e-mail que precisa bater exato.
  const [email, setEmail] = useState(() => searchParams.get('email') ?? '')
  const [senha, setSenha] = useState('')
  const [confirma, setConfirma] = useState('')
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)

  // Cadastrou e foi autorizado: a navegação pós-cadastro acontece no nível do App
  // (troca de LoggedOutRoutes para o portal autenticado assim que `user` é confirmado).
  // Conta criada, mas e-mail não está na lista de convidados: para o "Criando…".
  useEffect(() => { if (naoAutorizado) setEnviando(false) }, [naoAutorizado])

  const submeter = async (e) => {
    e.preventDefault()
    setErro('')
    if (senha.length < 6) { setErro('A senha precisa ter ao menos 6 caracteres.'); return }
    if (senha !== confirma) { setErro('As senhas não conferem.'); return }
    setEnviando(true)
    try {
      await cadastrar(email, senha)
      // Autorização/navegação acontecem via AuthProvider (useEffect acima / naoAutorizado).
    } catch (err) {
      setErro(MENSAGENS[err.code] ?? 'Não foi possível criar o cadastro. Tente novamente.')
      setEnviando(false)
    }
  }

  return (
    <div className="login-wrap">
      <form className="login-card" onSubmit={submeter}>
        <h2 className="login-title">Criar acesso</h2>
        <p className="login-sub">Use o e-mail que foi liberado pelo administrador</p>

        {naoAutorizado && (
          <div className="form-error">Este e-mail ainda não foi liberado pelo administrador.</div>
        )}
        {erro && <div className="form-error">{erro}</div>}

        <label className="login-label">E-mail
          <input className="login-input" type="email" value={email}
            onChange={e => setEmail(e.target.value)} autoComplete="email" required />
        </label>
        <label className="login-label">Senha
          <input className="login-input" type="password" value={senha}
            onChange={e => setSenha(e.target.value)} autoComplete="new-password" required />
        </label>
        <label className="login-label">Confirmar senha
          <input className="login-input" type="password" value={confirma}
            onChange={e => setConfirma(e.target.value)} autoComplete="new-password" required />
        </label>

        <button className="login-btn" type="submit" disabled={enviando}>
          {enviando ? 'Criando…' : 'Criar acesso'}
        </button>
        <Link className="login-link" to="/login">Já tenho acesso — entrar</Link>
      </form>
    </div>
  )
}
