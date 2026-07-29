import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { ClipboardList, Check, AlertTriangle, ChevronRight, BookOpen, Download } from 'lucide-react'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'
import { renderFriendlyText } from '../lib/comparatorRender.jsx'
import {
  decisoesDaTrilha, filtrarDecisoes, contarDecisoes, filtrarPorCenario, decisionDocId,
} from '../lib/decisoes.js'
import { useAuth } from '../lib/auth.jsx'
import { useScenario } from '../context/ScenarioContext.jsx'
import { subscribeDecisions, desfazerDecisao, marcarFichaAplicada } from '../lib/decisionsData.js'
import { mergeDecisoes, pendenciasDeAplicacao } from '../lib/decisionsMerge.js'
import { subscribeConferencia } from '../lib/conferenciaData.js'
import { divergentesDe } from '../lib/conferenciaStatus.js'
import RegistroDecisaoModal from '../components/RegistroDecisaoModal.jsx'
import AvisoSincronizacao from '../components/AvisoSincronizacao.jsx'

const TITULO = { ri: 'Regimento Interno', reg: 'Regulamento Geral' }
const FILTROS = [
  { id: 'todas', label: 'Todas' },
  { id: 'pendentes', label: 'Pendentes' },
  { id: 'decididas', label: 'Decididas' },
]

export default function DecisoesCuradoria({ trilha = 'ri' }) {
  const { user } = useAuth()
  const { cenario } = useScenario()
  const isAdmin = user?.role === 'admin'
  const [dados, setDados] = useState(null)
  const [error, setError] = useState(false)
  const [filtro, setFiltro] = useState('todas')
  const [fbDecisoes, setFbDecisoes] = useState(null)
  const [conf, setConf] = useState(null)
  const [registrando, setRegistrando] = useState(null)

  useEffect(() => {
    setDados(null); setError(false)
    fetchJson('/database/decisoes_curadoria.json').then(setDados).catch(() => setError(true))
  }, [])

  const [syncErro, setSyncErro] = useState(false)

  useEffect(() => {
    if (!user) { setFbDecisoes(null); return undefined }
    return subscribeDecisions(
      (v) => { setFbDecisoes(v); setSyncErro(false) },
      (e) => { console.error('Erro na assinatura de decisões:', e); setSyncErro(true) },
    )
  }, [user])

  useEffect(() => {
    if (!user) { setConf(null); return undefined }
    return subscribeConferencia(
      setConf,
      (e) => { console.error('Erro na assinatura da conferência:', e); setSyncErro(true) },
    )
  }, [user])

  const daTrilha = useMemo(() => decisoesDaTrilha(dados, trilha), [dados, trilha])
  // A curadoria existente do RI foi redigida sobre a LOB futura — não vale para o
  // cenário atual (ver filtrarPorCenario). O Regulamento, temático, vale nos 2.
  const doCenario = useMemo(() => filtrarPorCenario(daTrilha, cenario), [daTrilha, cenario])
  const merged = useMemo(
    () => mergeDecisoes(doCenario, fbDecisoes, cenario), [doCenario, fbDecisoes, cenario])
  const contagem = useMemo(() => contarDecisoes(merged), [merged])
  const lista = useMemo(() => filtrarDecisoes(merged, filtro), [merged, filtro])
  const pendencias = useMemo(() => pendenciasDeAplicacao(merged), [merged])
  const divergentes = useMemo(() => divergentesDe(conf, trilha, cenario), [conf, trilha, cenario])

  const exportar = () => {
    const registradas = mergeDecisoes(dados?.decisoes ?? [], fbDecisoes, cenario)
      .filter(d => d.statusDecisao === 'sistema')
    if (registradas.length === 0) { window.alert('Nenhuma decisão registrada no sistema para exportar.'); return }
    const payload = registradas.map(d => ({
      id: d.id, tipo: d.registro.tipo, decisao: d.registro.decisao,
      fonteEscolhida: d.registro.fonteEscolhida ?? null,
      alvoDispositivoId: d.registro.alvoDispositivoId ?? null,
      registradoPor: d.registro.registradoPor ?? null,
      registradoEm: d.registro.registradoEm?.toDate?.()?.toISOString() ?? null,
    }))
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' })
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = 'decisoes_export.json'
    a.click()
    URL.revokeObjectURL(a.href)
  }

  if (error) {
    return (
      <ErrorState
        icon={ClipboardList}
        title="Decisões não encontradas"
        hint={<>Execute <code>scripts/build_decisoes_curadoria.py</code>.</>}
      />
    )
  }
  if (!dados) return <LoadingState label="" />

  return (
    <div className="dec">
      <div className="section-bar no-print">
        <div className="section-bar-label">Decisões — {TITULO[trilha]}</div>
        <span className="section-bar-badge">
          <ClipboardList size={13} color="var(--cbm-red-700)" />
          {contagem.decididas} / {contagem.total} decididas
        </span>
      </div>

      <div className="page-body">
        <AvisoSincronizacao visivel={syncErro} />
        <div className="dec-filtros no-print" style={{ display: 'flex', justifyContent: 'space-between', gap: 8, flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {FILTROS.map(f => (
              <button
                key={f.id}
                className={`btn btn-ghost${filtro === f.id ? ' active' : ''}`}
                onClick={() => setFiltro(f.id)}
              >
                {f.label}
              </button>
            ))}
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <Link to="/manual#cockpit" className="btn btn-ghost"><BookOpen size={15} /> Como funciona</Link>
            {isAdmin && (
              <button className="btn btn-ghost" onClick={exportar}><Download size={15} /> Exportar decisões</button>
            )}
          </div>
        </div>

        {(pendencias.length > 0 || divergentes.length > 0) && (
          <div className="card dec-pendencias" style={{ padding: 16 }}>
            <div className="rg-heading">Pendências de aplicação</div>
            {pendencias.map(d => (
              <div key={d.id} className="dec-pendencia-item">
                <strong>{d.titulo}</strong> — {d.registro.ficha.oQueMuda} ({d.registro.ficha.onde})
                {isAdmin && (
                  <button className="btn btn-ghost" onClick={() => marcarFichaAplicada(decisionDocId(d.id, cenario)).catch(e => {
                    console.error('Erro ao marcar ficha como aplicada:', e)
                    window.alert('Não foi possível marcar como aplicada agora. Tente novamente.')
                  })}>
                    Marcar aplicada
                  </button>
                )}
              </div>
            ))}
            {divergentes.map(({ key }) => (
              <div key={key} className="dec-pendencia-item">Divergente — {key}</div>
            ))}
          </div>
        )}

        {lista.length === 0 ? (
          doCenario.length === 0 && daTrilha.length > 0 ? (
            <SemDecisoesNoCenario trilha={trilha} cenario={cenario} n={daTrilha.length} />
          ) : (
            <div className="card" style={{ padding: 24, textAlign: 'center', color: 'var(--text-muted)' }}>
              Nenhuma decisão neste filtro.
            </div>
          )
        ) : (
          lista.map(d => (
            <DecisaoCard
              key={d.id}
              d={d}
              isAdmin={isAdmin}
              emEdicao={registrando?.id === d.id}
              onRegistrar={() => setRegistrando(d)}
              onDesfazer={() => {
                if (window.confirm('Desfazer o registro? O texto final aplicado (se houver) permanece e pode ser revisto pela Revisão.')) {
                  desfazerDecisao(decisionDocId(d.id, cenario)).catch(e => {
                    console.error('Erro ao desfazer decisão:', e)
                    window.alert('Não foi possível desfazer o registro agora. Tente novamente.')
                  })
                }
              }}
            />
          ))
        )}
      </div>

      {registrando && (
        <RegistroDecisaoModal
          decisao={registrando}
          trilha={trilha}
          cenario={cenario}
          autor={{ nome: user?.nome ?? user?.email }}
          onClose={() => setRegistrando(null)}
          onSaved={() => setRegistrando(null)}
        />
      )}
    </div>
  )
}

// Estado vazio HONESTO: há decisões nesta trilha, mas nenhuma pertence ao cenário
// ativo. Diz o que existe e onde está, em vez de sumir com tudo em silêncio (a
// alternativa — reaproveitar por semelhança de nome de órgão — é a armadilha AR-01:
// as decisões do RI discutem órgãos da LOB futura que não existem na Lei 2.204/2009).
function SemDecisoesNoCenario({ trilha, cenario, n }) {
  const outro = cenario === 'atual' ? 'futura' : 'atual'
  return (
    <div className="card" style={{ padding: 24, color: 'var(--text-muted)' }}>
      <div className="rg-heading">Nenhuma decisão curada para a LOB {cenario}</div>
      <p style={{ marginTop: 8 }}>
        {trilha === 'ri'
          ? <>As {n} decisões existentes do Regimento Interno foram redigidas sobre a
              estrutura da <b>LOB {outro}</b> (órgãos como BBS, CRBM, DEPDEC, DOE e COT),
              que não têm equivalente na Lei nº 2.204/2009. A curadoria do RI para este
              cenário ainda não foi feita.</>
          : <>As {n} decisões existentes desta trilha pertencem ao cenário <b>{outro}</b>.</>}
      </p>
      <p style={{ marginTop: 8 }}>
        Troque o cenário no topo da barra lateral para consultá-las.
      </p>
    </div>
  )
}

function DecisaoCard({ d, isAdmin, emEdicao, onRegistrar, onDesfazer }) {
  const [abertas, setAbertas] = useState({}) // índice da candidata -> aberta
  const [cmpAberta, setCmpAberta] = useState(false)
  const status = d.statusDecisao ?? (d.decidido ? 'vault' : 'pendente')

  return (
    <div className={`card dec-card${status !== 'pendente' ? ' dec-card-ok' : ''}${emEdicao ? ' dec-card-editando' : ''}`} style={{ marginBottom: 14, padding: 16 }}>
      <div className="dec-card-head">
        <h3 className="dec-titulo">{d.titulo}</h3>
        <span className={`dec-selo ${status === 'sistema' ? 'dec-selo-sys' : status === 'vault' ? 'dec-selo-ok' : 'dec-selo-pend'}`}>
          {status === 'sistema' && <><Check size={13} /> Decidida no sistema</>}
          {status === 'vault' && <><Check size={13} /> Decidida no vault</>}
          {status === 'pendente' && <><AlertTriangle size={13} /> Pendente</>}
        </span>
      </div>
      <p className="dec-questao">{d.questao}</p>

      <div className="dec-candidatas">
        {d.candidatas.map((c, i) => (
          <div className="dec-candidata" key={i}>
            <button className="dec-cand-head" onClick={() => setAbertas(a => ({ ...a, [i]: !a[i] }))}>
              <ChevronRight size={14} className={`dec-chevron${abertas[i] ? ' aberta' : ''}`} />
              <span className="dec-cand-fonte">{c.fonte}</span>
              {c.citacao && <span className="rg-source">{c.citacao}</span>}
            </button>
            {abertas[i] && (
              <div className="dec-cand-corpo">
                {c.verbatim.map((linha, j) => (
                  <p className="rg-caput" key={j}>{renderFriendlyText(linha)}</p>
                ))}
                {c.ocr && <p className="dec-ocr">{c.ocr}</p>}
                {c.leitura && <p className="dec-leitura"><strong>Leitura:</strong> {c.leitura}</p>}
              </div>
            )}
          </div>
        ))}
      </div>

      {d.comparacao.length > 0 && (
        <div className="dec-comparacao">
          <button className="dec-cand-head" onClick={() => setCmpAberta(v => !v)}>
            <ChevronRight size={14} className={`dec-chevron${cmpAberta ? ' aberta' : ''}`} />
            <span className="dec-cand-fonte">Comparação</span>
          </button>
          {cmpAberta && (
            <ul className="dec-cmp-list">
              {d.comparacao.map((b, i) => <li key={i}>{b}</li>)}
            </ul>
          )}
        </div>
      )}

      {status === 'vault' && d.decisao && (
        <div className="dec-decisao">
          <div className="rg-heading">Decisão CBMRO</div>
          <p className="rg-caput">{d.decisao}</p>
        </div>
      )}

      {status === 'sistema' && d.registro && (
        <div className="dec-decisao">
          <div className="rg-heading">Decisão CBMRO</div>
          <p className="rg-caput">{d.registro.decisao}</p>
          <p className="dec-leitura">
            <strong>Fonte:</strong> {d.registro.fonteEscolhida} · <strong>Tipo:</strong> {d.registro.tipo}
          </p>
          {d.registro.tipo === 'estrutural' && d.registro.ficha && (
            <p className="dec-leitura">
              <strong>Ficha:</strong> {d.registro.ficha.oQueMuda} ({d.registro.ficha.onde}) — {d.registro.ficha.status}
            </p>
          )}
        </div>
      )}

      {isAdmin && (
        <div className="decm-acoes" style={{ marginTop: 12 }}>
          {status === 'sistema' ? (
            <button className="btn btn-ghost" onClick={onDesfazer}>Desfazer</button>
          ) : emEdicao ? (
            <button className="btn btn-ghost" disabled>Editando em outra janela</button>
          ) : (
            <button className="btn btn-ghost" onClick={onRegistrar}>Registrar decisão</button>
          )}
        </div>
      )}
    </div>
  )
}
