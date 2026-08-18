import { useEffect, useMemo, useState } from 'react'
import { useAuth } from '../lib/auth.jsx'
import { contaStatus, situacaoMembro, normalizeEmail } from '../lib/membersStats.js'
import {
  subscribeMembers, setMemberRole, setMemberEscopo, setMemberAtivo, removeMember,
  recusarSolicitacao,
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
  pendente: { cls: 'b-pend', txt: '🟠 Pendente' },
  bloqueado: { cls: 'b-bloq', txt: '🔴 Bloqueado' },
}

export default function Acessos() {
  const { user } = useAuth()
  const [members, setMembers] = useState([])
  const [erro, setErro] = useState(null)

  useEffect(() => subscribeMembers(
    setMembers,
    (e) => { console.error('Erro ao carregar membros:', e); setErro('Não foi possível carregar a lista de acessos.') },
  ), [])

  const stats = useMemo(() => contaStatus(members), [members])
  const pendentes = useMemo(() => members.filter(m => situacaoMembro(m) === 'pendente'), [members])

  const alternarPapel = async (m) => {
    try { await setMemberRole(m.email, m.role === 'admin' ? 'participante' : 'admin') }
    catch (err) { console.error(err); setErro('Não foi possível alterar o papel da pessoa.') }
  }
  const alternarEscopo = async (m) => {
    try { await setMemberEscopo(m.email, m.escopo === 'servico' ? '' : 'servico') }
    catch (err) { console.error(err); setErro('Não foi possível alterar o alcance da pessoa.') }
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
  const aprovar = async (m) => {
    try { await setMemberAtivo(m.email, true) }
    catch (err) { console.error(err); setErro('Não foi possível aprovar o pedido.') }
  }
  const recusar = async (m) => {
    if (!window.confirm(`Recusar o pedido de ${m.nome}?`)) return
    try { await recusarSolicitacao(m.email) }
    catch (err) { console.error(err); setErro('Não foi possível recusar o pedido.') }
  }

  return (
    <div className="acc-wrap">
      <h2 className="acc-title">Acessos</h2>
      <p className="acc-sub">Aprove pedidos de acesso, controle papéis e acompanhe quem entrou e quando.</p>

      {erro && <div className="form-error" style={{ marginBottom: 12 }}>{erro}</div>}

      <div className="acc-cards">
        <div className="acc-stat"><div className="acc-n">{stats.total}</div><div className="acc-l">Pessoas no total</div></div>
        <div className="acc-stat"><div className="acc-n"><span className="acc-dot" style={{ background: 'var(--accent-green)' }} />{stats.cadastrados}</div><div className="acc-l">Cadastradas</div></div>
        <div className="acc-stat"><div className="acc-n"><span className="acc-dot" style={{ background: '#b45500' }} />{stats.pendentes}</div><div className="acc-l">Pedidos pendentes</div></div>
        <div className="acc-stat"><div className="acc-n"><span className="acc-dot" style={{ background: 'var(--cbm-red-700)' }} />{stats.bloqueados}</div><div className="acc-l">Bloqueadas</div></div>
      </div>

      {pendentes.length > 0 && (
        <>
          <div className="acc-bar">
            <strong>Solicitações pendentes</strong>
          </div>
          <div className="acc-panel" style={{ marginBottom: 18 }}>
            <table className="acc-table">
              <thead>
                <tr><th>Pessoa</th><th>Cidade / Comando / Unidade</th><th style={{ textAlign: 'right' }}>Ações</th></tr>
              </thead>
              <tbody>
                {pendentes.map(m => (
                  <tr key={m.email}>
                    <td>
                      <div className="acc-nome">{m.nome}{m.nomeGuerra ? ` (${m.nomeGuerra})` : ''}</div>
                      <div className="acc-mail">{m.email}</div>
                    </td>
                    <td>{m.cidade} — {m.comando} — {m.unidade}</td>
                    <td>
                      <div className="acc-acts">
                        <button type="button" className="acc-ic" onClick={() => aprovar(m)}>aprovar</button>
                        <button type="button" className="acc-ic danger" onClick={() => recusar(m)}>recusar</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      <div className="acc-bar">
        <strong>Pessoas</strong>
      </div>
      <div className="acc-panel">
        <table className="acc-table">
          <thead>
            <tr><th>Pessoa</th><th>Papel</th><th>Alcance</th><th>Status</th><th>Último login</th><th style={{ textAlign: 'right' }}>Ações</th></tr>
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
                  <td className="acc-mail">{m.role === 'admin' ? '—' : (m.escopo === 'servico' ? 'Só Regulamento de Serviço' : 'Portal completo')}</td>
                  <td><span className={`acc-badge ${badge.cls}`}>{badge.txt}</span></td>
                  <td className={login ? 'acc-quando' : 'acc-nunca'}>{login ?? 'nunca entrou'}</td>
                  <td>
                    {ehEu ? (
                      <div className="acc-acts"><span className="acc-eu">você</span></div>
                    ) : (
                      <div className="acc-acts">
                        <button type="button" className="acc-ic" onClick={() => alternarPapel(m)}>papel</button>
                        {m.role !== 'admin' && (
                          <button type="button" className="acc-ic" onClick={() => alternarEscopo(m)}>
                            {m.escopo === 'servico' ? 'liberar portal' : 'restringir a serviço'}
                          </button>
                        )}
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
