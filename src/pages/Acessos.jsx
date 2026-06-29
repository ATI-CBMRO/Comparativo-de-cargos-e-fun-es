import { useEffect, useMemo, useState } from 'react'
import { useAuth } from '../lib/auth.jsx'
import { contaStatus, situacaoMembro, normalizeEmail } from '../lib/membersStats.js'
import {
  subscribeMembers, addMember, setMemberRole, setMemberAtivo, removeMember,
} from '../lib/membersData.js'

function formatLogin(ts) {
  if (!ts || typeof ts.toDate !== 'function') return null
  return ts.toDate().toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
  })
}

const BADGE = {
  cadastrado: { cls: 'b-cad', txt: '🟢 Cadastrado' },
  convidado: { cls: 'b-conv', txt: '🟡 Convidado' },
  bloqueado: { cls: 'b-bloq', txt: '🔴 Bloqueado' },
}

export default function Acessos() {
  const { user } = useAuth()
  const [members, setMembers] = useState([])
  const [erro, setErro] = useState(null)
  const [abrindo, setAbrindo] = useState(false)
  const [email, setEmail] = useState('')
  const [nome, setNome] = useState('')
  const [role, setRole] = useState('participante')

  useEffect(() => subscribeMembers(
    setMembers,
    (e) => { console.error('Erro ao carregar membros:', e); setErro('Não foi possível carregar a lista de acessos.') },
  ), [])

  const stats = useMemo(() => contaStatus(members), [members])

  const convidar = async (e) => {
    e.preventDefault()
    if (!email.trim()) return
    try {
      await addMember({ email, nome, role }, user.email)
      setEmail(''); setNome(''); setRole('participante'); setAbrindo(false)
    } catch (err) {
      console.error(err); setErro('Não foi possível adicionar a pessoa.')
    }
  }

  const alternarPapel = async (m) => {
    try { await setMemberRole(m.email, m.role === 'admin' ? 'participante' : 'admin') }
    catch (err) { console.error(err); setErro('Não foi possível alterar o papel da pessoa.') }
  }
  const alternarAtivo = async (m) => {
    try { await setMemberAtivo(m.email, !m.ativo) }
    catch (err) { console.error(err); setErro('Não foi possível alterar o acesso da pessoa.') }
  }
  const remover = async (m) => {
    if (!window.confirm(`Remover ${m.email}? As sugestões já enviadas permanecem.`)) return
    try { await removeMember(m.email) }
    catch (err) { console.error(err); setErro('Não foi possível remover a pessoa.') }
  }

  return (
    <div className="acc-wrap">
      <h2 className="acc-title">Acessos</h2>
      <p className="acc-sub">Convide pessoas pelo e-mail, controle papéis e acompanhe quem se cadastrou e quando entrou.</p>

      {erro && <div className="login-erro" style={{ marginBottom: 12 }}>{erro}</div>}

      <div className="acc-cards">
        <div className="acc-stat"><div className="acc-n">{stats.total}</div><div className="acc-l">Pessoas no total</div></div>
        <div className="acc-stat"><div className="acc-n"><span className="acc-dot" style={{ background: '#2aa05a' }} />{stats.cadastrados}</div><div className="acc-l">Cadastradas</div></div>
        <div className="acc-stat"><div className="acc-n"><span className="acc-dot" style={{ background: '#e0a106' }} />{stats.convidados}</div><div className="acc-l">Convidadas (sem entrar)</div></div>
        <div className="acc-stat"><div className="acc-n"><span className="acc-dot" style={{ background: '#c8102e' }} />{stats.bloqueados}</div><div className="acc-l">Bloqueadas</div></div>
      </div>

      <div className="acc-bar">
        <strong>Pessoas</strong>
        <button type="button" className="acc-add" onClick={() => setAbrindo(o => !o)}>＋ Convidar pessoa</button>
      </div>

      {abrindo && (
        <form className="acc-addform" onSubmit={convidar}>
          <div className="acc-fld" style={{ flex: 2, minWidth: 220 }}>
            <label>E-mail</label>
            <input value={email} onChange={e => setEmail(e.target.value)} type="email" placeholder="pessoa@exemplo.com" required />
          </div>
          <div className="acc-fld" style={{ flex: 2, minWidth: 180 }}>
            <label>Nome</label>
            <input value={nome} onChange={e => setNome(e.target.value)} placeholder="Posto e nome" />
          </div>
          <div className="acc-fld">
            <label>Papel</label>
            <select value={role} onChange={e => setRole(e.target.value)}>
              <option value="participante">Participante</option>
              <option value="admin">Administrador</option>
            </select>
          </div>
          <button type="submit" className="acc-add">Adicionar à lista</button>
        </form>
      )}

      <div className="acc-panel">
        <table className="acc-table">
          <thead>
            <tr><th>Pessoa</th><th>Papel</th><th>Status</th><th>Último login</th><th style={{ textAlign: 'right' }}>Ações</th></tr>
          </thead>
          <tbody>
            {members.map(m => {
              const sit = situacaoMembro(m)
              const badge = BADGE[sit]
              const login = formatLogin(m.ultimoLogin)
              const ehEu = normalizeEmail(m.email) === normalizeEmail(user.email)
              return (
                <tr key={m.email} style={sit === 'bloqueado' ? { opacity: .65 } : undefined}>
                  <td>
                    <div className="acc-nome">{m.nome}{m.role === 'admin' ? ' (administrador)' : ''}</div>
                    <div className="acc-mail">{m.email}</div>
                  </td>
                  <td><span className={`acc-papel${m.role === 'admin' ? ' adm' : ''}`}>{m.role === 'admin' ? 'Administrador' : 'Participante'}</span></td>
                  <td><span className={`acc-badge ${badge.cls}`}>{badge.txt}</span></td>
                  <td className={login ? 'acc-quando' : 'acc-nunca'}>{login ?? 'nunca entrou'}</td>
                  <td>
                    {ehEu ? (
                      <div className="acc-acts"><span className="acc-eu">você</span></div>
                    ) : (
                      <div className="acc-acts">
                        <button type="button" className="acc-ic" onClick={() => alternarPapel(m)}>papel</button>
                        <button type="button" className="acc-ic" onClick={() => alternarAtivo(m)}>{m.ativo ? 'bloquear' : 'liberar'}</button>
                        <button type="button" className="acc-ic danger" onClick={() => remover(m)}>remover</button>
                      </div>
                    )}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
