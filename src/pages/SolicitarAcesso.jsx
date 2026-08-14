// src/pages/SolicitarAcesso.jsx
import { useMemo, useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../lib/auth.jsx'
import { solicitarAcesso } from '../lib/membersData.js'
import { cidadesDisponiveis, comandosPorCidade, unidadesPorCidadeEComando } from '../lib/unidadesCbmro.js'

const MENSAGENS = {
  'auth/email-already-in-use': 'Este e-mail já tem cadastro. Use a tela de login.',
  'auth/invalid-email': 'E-mail inválido.',
  'auth/weak-password': 'A senha precisa ter ao menos 6 caracteres.',
}

export default function SolicitarAcesso() {
  const { cadastrar, pendente } = useAuth()
  const [nomeCompleto, setNomeCompleto] = useState('')
  const [nomeGuerra, setNomeGuerra] = useState('')
  const [cidade, setCidade] = useState('')
  const [comando, setComando] = useState('')
  const [unidade, setUnidade] = useState('')
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [confirma, setConfirma] = useState('')
  const [erro, setErro] = useState('')
  const [enviando, setEnviando] = useState(false)

  const cidades = useMemo(() => cidadesDisponiveis(), [])
  const comandos = useMemo(() => (cidade ? comandosPorCidade(cidade) : []), [cidade])
  const unidades = useMemo(
    () => (cidade && comando ? unidadesPorCidadeEComando(cidade, comando) : []),
    [cidade, comando],
  )

  // Pedido gravado: o AuthProvider detecta ativo:false/status:'pendente' e desloga
  // sozinho — este efeito só tira o "Enviando…"; a confirmação é o `if (pendente)` abaixo.
  useEffect(() => { if (pendente) setEnviando(false) }, [pendente])

  const mudarCidade = (novaCidade) => {
    setCidade(novaCidade); setComando(''); setUnidade('')
  }
  const mudarComando = (novoComando) => {
    setComando(novoComando); setUnidade('')
  }

  const submeter = async (e) => {
    e.preventDefault()
    setErro('')
    if (!nomeCompleto.trim() || !nomeGuerra.trim()) { setErro('Preencha nome completo e nome de guerra.'); return }
    if (!cidade || !comando || !unidade) { setErro('Escolha cidade, comando e unidade.'); return }
    if (senha.length < 6) { setErro('A senha precisa ter ao menos 6 caracteres.'); return }
    if (senha !== confirma) { setErro('As senhas não conferem.'); return }
    setEnviando(true)
    try {
      const fbUser = await cadastrar(email, senha)
      await solicitarAcesso({ email, nome: nomeCompleto, nomeGuerra, cidade, comando, unidade, uid: fbUser.uid })
    } catch (err) {
      setErro(MENSAGENS[err.code] ?? 'Não foi possível enviar o pedido. Tente novamente.')
      setEnviando(false)
    }
  }

  if (pendente) {
    return (
      <div className="login-wrap">
        <div className="login-card login-card--wide">
          <h2 className="login-title">Pedido enviado</h2>
          <p className="login-sub">Seu pedido de acesso foi enviado para análise. Você será avisado quando for aprovado.</p>
          <Link className="login-link" to="/login">Voltar para o login</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="login-wrap">
      <form className="login-card login-card--wide" onSubmit={submeter}>
        <h2 className="login-title">Solicitar acesso</h2>
        <p className="login-sub">Preencha seus dados para pedir acesso à Revisão da Minuta</p>

        {erro && <div className="form-error">{erro}</div>}

        <label className="login-label">Nome completo
          <input className="login-input" value={nomeCompleto}
            onChange={e => setNomeCompleto(e.target.value)} required />
        </label>
        <label className="login-label">Nome de guerra
          <input className="login-input" value={nomeGuerra}
            onChange={e => setNomeGuerra(e.target.value)} required />
        </label>
        <label className="login-label">Cidade
          <select className="login-input" value={cidade}
            onChange={e => mudarCidade(e.target.value)} required>
            <option value="">Selecione...</option>
            {cidades.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </label>
        <label className="login-label">Comando
          <select className="login-input" value={comando}
            onChange={e => mudarComando(e.target.value)} required disabled={!cidade}>
            <option value="">{cidade ? 'Selecione...' : 'Escolha a cidade primeiro'}</option>
            {comandos.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </label>
        <label className="login-label">Unidade
          <select className="login-input" value={unidade}
            onChange={e => setUnidade(e.target.value)} required disabled={!comando}>
            <option value="">{comando ? 'Selecione...' : 'Escolha o comando primeiro'}</option>
            {unidades.map(u => <option key={u} value={u}>{u}</option>)}
          </select>
        </label>
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
          {enviando ? 'Enviando…' : 'Enviar pedido de acesso'}
        </button>
        <Link className="login-link" to="/login">Já tenho acesso — entrar</Link>
      </form>
    </div>
  )
}
