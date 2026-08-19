import { useEffect, useMemo, useState } from 'react'
import { useAuth } from '../lib/auth.jsx'
import { contaStatus, situacaoMembro, normalizeEmail } from '../lib/membersStats.js'
import {
  subscribeMembers, setMemberRole, setMemberEscopo, setMemberAtivo, removeMember,
  recusarSolicitacao,
} from '../lib/membersData.js'
import { subscribeVisitantes } from '../lib/visitantesData.js'
import { subscribeUploads, urlDeDownload, removerUpload } from '../lib/uploadsData.js'
import AvisoSincronizacao from '../components/AvisoSincronizacao.jsx'

function formatLogin(ts) {
  if (!ts || typeof ts.toDate !== 'function') return null
  return ts.toDate().toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit',
  })
}

function formatTamanho(bytes) {
  if (typeof bytes !== 'number' || bytes < 0) return '—'
  const mb = bytes / (1024 * 1024)
  return mb >= 1 ? `${mb.toFixed(1)} MB` : `${Math.max(1, Math.round(bytes / 1024))} KB`
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
  const [visitantes, setVisitantes] = useState([])
  const [erroVisitantes, setErroVisitantes] = useState(false)

  useEffect(() => subscribeMembers(
    setMembers,
    (e) => { console.error('Erro ao carregar membros:', e); setErro('Não foi possível carregar a lista de acessos.') },
  ), [])

  // Erro visível na tela, nunca só no console (AR-04): sem isto, uma queda do feed
  // deixaria a seção mostrando "nenhum visitante" — que é indistinguível de "ninguém
  // acessou ainda" e mente para o administrador.
  useEffect(() => subscribeVisitantes(
    (lista) => { setVisitantes(lista); setErroVisitantes(false) },
    (e) => { console.error('Erro ao carregar visitantes:', e); setErroVisitantes(true) },
  ), [])

  const [uploads, setUploads] = useState([])
  const [erroUploads, setErroUploads] = useState(false)

  // Erro visível na tela, nunca só no console (AR-04): sem isto, uma queda do feed deixaria
  // a seção mostrando "nenhum envio", que é indistinguível de "ninguém enviou nada" e mente
  // para o administrador — que poderia perder um documento enviado.
  useEffect(() => subscribeUploads(
    (lista) => { setUploads(lista); setErroUploads(false) },
    (e) => { console.error('Erro ao carregar envios:', e); setErroUploads(true) },
  ), [])

  const baixar = async (u) => {
    try {
      const url = await urlDeDownload(u.storagePath)
      window.open(url, '_blank', 'noopener')
    } catch (err) {
      console.error(err); setErro('Não foi possível abrir o arquivo enviado.')
    }
  }
  const removerEnvio = async (u) => {
    if (!window.confirm(`Remover o envio "${u.nomeArquivo}"? O arquivo é apagado junto e não há como desfazer.`)) return
    try { await removerUpload({ id: u.id, storagePath: u.storagePath }) }
    catch (err) { console.error(err); setErro('Não foi possível remover o envio.') }
  }

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

      <h3 className="acc-sec-title">Visitantes do acervo público ({visitantes.length})</h3>
      <p className="acc-sub">
        Quem consultou o acervo pela página pública, sem login. Registro de histórico — não há
        aprovação nem bloqueio: o acervo é público por decisão do comando.
      </p>

      <AvisoSincronizacao visivel={erroVisitantes}>
        Não foi possível carregar a lista de visitantes agora — o que aparece abaixo pode estar
        incompleto ou desatualizado.
      </AvisoSincronizacao>

      <div className="acc-panel">
        <table className="acc-table">
          <thead>
            <tr>
              <th>Visitante</th><th>Instituição</th><th>Primeiro acesso</th><th>Último acesso</th>
            </tr>
          </thead>
          <tbody>
            {visitantes.length === 0 && !erroVisitantes && (
              <tr><td colSpan={4} className="acc-mail">Nenhum visitante registrado até agora.</td></tr>
            )}
            {visitantes.map(v => (
              <tr key={v.id}>
                <td>
                  <div className="acc-nome">{v.nome}</div>
                  <div className="acc-mail">{v.email}</div>
                </td>
                <td className="acc-papel">{v.instituicao}</td>
                <td className={formatLogin(v.criadoEm) ? 'acc-quando' : 'acc-nunca'}>
                  {formatLogin(v.criadoEm) ?? '—'}
                </td>
                <td className={formatLogin(v.ultimoAcesso) ? 'acc-quando' : 'acc-nunca'}>
                  {formatLogin(v.ultimoAcesso) ?? '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h3 className="acc-sec-title">Documentos enviados por visitantes ({uploads.length})</h3>
      <p className="acc-sub">
        Legislações que militares de outros CBMs enviaram pela página pública. Baixe, avalie e
        — se aproveitar — ingira no acervo pelo processo de sempre. Remover apaga o arquivo junto.
      </p>

      <AvisoSincronizacao visivel={erroUploads}>
        Não foi possível carregar os envios agora — a lista abaixo pode estar incompleta ou
        desatualizada.
      </AvisoSincronizacao>

      <div className="acc-panel">
        <table className="acc-table">
          <thead>
            <tr>
              <th>Documento</th><th>Enviado por</th><th>Observação</th><th>Quando</th><th></th>
            </tr>
          </thead>
          <tbody>
            {uploads.length === 0 && !erroUploads && (
              <tr><td colSpan={5} className="acc-mail">Nenhum documento enviado até agora.</td></tr>
            )}
            {uploads.map(u => (
              <tr key={u.id}>
                <td>
                  <div className="acc-nome">{u.estado} · {u.tipoDocumento}</div>
                  <div className="acc-mail">{u.nomeArquivo} · {formatTamanho(u.tamanho)}</div>
                </td>
                <td>
                  <div className="acc-nome">{u.nomeVisitante}</div>
                  {/* E-mail pode faltar em envio de visitante cadastrado ANTES desta entrega
                      (o campo só passou a ser retido agora): cai para a lista de visitantes,
                      que o admin já tem carregada nesta mesma tela. */}
                  <div className="acc-mail">
                    {u.emailVisitante || visitantes.find(v => v.id === u.uid)?.email || '—'}
                  </div>
                </td>
                <td className="acc-papel">{u.observacao || '—'}</td>
                <td className={formatLogin(u.criadoEm) ? 'acc-quando' : 'acc-nunca'}>
                  {formatLogin(u.criadoEm) ?? '—'}
                </td>
                <td>
                  <div className="acc-acts">
                    <button type="button" className="acc-ic" onClick={() => baixar(u)}>baixar</button>
                    <button type="button" className="acc-ic danger" onClick={() => removerEnvio(u)}>remover</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
