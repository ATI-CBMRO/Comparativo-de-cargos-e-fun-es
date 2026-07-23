import { useEffect, useMemo, useState } from 'react'
import { ListChecks, Check, AlertTriangle } from 'lucide-react'
import { useScenario } from '../context/ScenarioContext.jsx'
import { useAuth } from '../lib/auth.jsx'
import { scenarioDbUrl } from '../lib/scenario.js'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'
import { renderFriendlyText } from '../lib/comparatorRender.jsx'
import { buildConferencia } from '../lib/conferencia.js'
import { confKey, mergeStatus } from '../lib/conferenciaStatus.js'
import { subscribeConferencia, saveConferenciaStatus } from '../lib/conferenciaData.js'
import { articleLabel, romanize } from '../lib/minutaArticles.js'
import { AlternativesPanel } from '../components/AlternativesPanel.jsx'
import AvisoSincronizacao from '../components/AvisoSincronizacao.jsx'

const ARQ = { ri: 'minuta_structure.json', reg: 'regulamento_structure.json' }
const TITULO = { ri: 'Regimento Interno', reg: 'Regulamento Geral' }

export default function ConferenciaLinear({ trilha = 'ri' }) {
  const { cenario } = useScenario()
  const { user } = useAuth()
  const [data, setData] = useState(null)
  const [error, setError] = useState(false)
  const [statusLocal, setStatusLocal] = useState(new Map()) // chave estável -> 'ok'|'div' (fallback sem login)
  const [remoto, setRemoto] = useState(null)
  const [ufSel, setUfSel] = useState({}) // chapterId -> uf selecionada

  useEffect(() => {
    setData(null); setError(false)
    fetchJson(scenarioDbUrl(cenario, ARQ[trilha])).then(setData).catch(() => setError(true))
  }, [cenario, trilha])

  const [syncErro, setSyncErro] = useState(false)
  useEffect(() => {
    if (!user) { setRemoto(null); return undefined }
    return subscribeConferencia(
      (v) => { setRemoto(v); setSyncErro(false) },
      (e) => { console.error('Erro na assinatura da conferência:', e); setSyncErro(true) },
    )
  }, [user])

  const lista = useMemo(() => (data ? buildConferencia(data) : []), [data])
  const statusMap = useMemo(() => mergeStatus(statusLocal, remoto), [statusLocal, remoto])
  const feitos = useMemo(
    () => lista.filter(item => statusMap.get(confKey(item.dispositivo))).length,
    [statusMap, lista],
  )

  const marcar = (item) => (v) => {
    const key = confKey(item.dispositivo)
    setStatusLocal(m => { const n = new Map(m); if (v == null) n.delete(key); else n.set(key, v); return n })
    if (user) saveConferenciaStatus(key, v, { nome: user.nome ?? user.email }).catch(e => {
      console.error('Erro ao salvar conferência:', e)
      window.alert('Não foi possível salvar essa conferência agora. Tente novamente.')
    })
  }

  if (error) {
    return (
      <ErrorState
        icon={ListChecks}
        title="Estrutura não encontrada"
        hint={<>Execute o script que gera <code>database/{ARQ[trilha]}</code>.</>}
      />
    )
  }
  if (!data) return <LoadingState label="" />

  return (
    <div className="conf">
      <div className="section-bar no-print">
        <div className="section-bar-label">Conferência — {TITULO[trilha]}</div>
        <span className="section-bar-badge">
          <ListChecks size={13} color="var(--cbm-red-700)" />
          {feitos} / {lista.length} conferidos
        </span>
        {!user && <span className="wiz-finais-aviso">Entre para salvar a conferência.</span>}
      </div>

      <div className="page-body">
        <AvisoSincronizacao visivel={syncErro} />
        <div className="conf-progress">
          <div className="conf-progress-bar" style={{ width: `${lista.length ? (feitos / lista.length) * 100 : 0}%` }} />
        </div>

        {lista.length === 0 ? (
          <div className="card" style={{ padding: 24, textAlign: 'center', color: 'var(--text-muted)' }}>
            Nenhum dispositivo encontrado.
          </div>
        ) : (
          lista.map((item, i) => (
            <ConferenciaItem
              key={item.dispositivo.number ?? i}
              item={item}
              idx={i}
              status={statusMap.get(confKey(item.dispositivo))}
              onStatus={marcar(item)}
              ufSel={ufSel}
              setUfSel={setUfSel}
            />
          ))
        )}
      </div>
    </div>
  )
}

function ConferenciaItem({ item, idx, status, onStatus, ufSel, setUfSel }) {
  const { dispositivo, chapterTitle, chapterId, alternatives } = item

  return (
    <div className={`card conf-item${status === 'ok' ? ' conf-item-ok' : status === 'div' ? ' conf-item-div' : ''}`} style={{ marginBottom: 14, padding: 16 }}>
      {chapterTitle && <div className="rg-heading">{chapterTitle}</div>}
      <div className="rg-columns" style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
        <div className="rg-col" style={{ flex: 1, minWidth: 0 }}>
          <div className="rg-article">
            <p className="rg-caput">
              <strong>{articleLabel(dispositivo.number)}</strong> {renderFriendlyText(dispositivo.caput)}
            </p>
            {dispositivo.incisos?.length > 0 && (
              <ul className="cc-list rg-incisos">
                {dispositivo.incisos.map((inc, i) => (
                  <li key={i}>{inc.ownMarker ? '' : `${romanize(i + 1)} - `}{renderFriendlyText(inc.text)}</li>
                ))}
              </ul>
            )}
          </div>
          <div className="conf-controls no-print">
            <button
              type="button"
              className={`btn btn-ghost${status === 'ok' ? ' active' : ''}`}
              onClick={() => onStatus(status === 'ok' ? null : 'ok')}
            >
              <Check size={15} /> Confere
            </button>
            <button
              type="button"
              className={`btn btn-ghost${status === 'div' ? ' active' : ''}`}
              onClick={() => onStatus(status === 'div' ? null : 'div')}
            >
              <AlertTriangle size={15} /> Divergente
            </button>
          </div>
        </div>

        <div className="rg-col no-print" style={{ flex: 1, minWidth: 0 }}>
          <AlternativesPanel
            alternatives={alternatives}
            selectedUf={ufSel[chapterId]}
            onSelectUf={(uf) => setUfSel(u => ({ ...u, [chapterId]: uf }))}
          />
        </div>
      </div>
    </div>
  )
}
