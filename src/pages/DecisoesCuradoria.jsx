import { useEffect, useMemo, useState } from 'react'
import { ClipboardList, Check, AlertTriangle, ChevronRight } from 'lucide-react'
import { fetchJson } from '../lib/dataCache.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'
import { renderFriendlyText } from '../lib/comparatorRender.jsx'
import { decisoesDaTrilha, filtrarDecisoes, contarDecisoes } from '../lib/decisoes.js'

const TITULO = { ri: 'Regimento Interno', reg: 'Regulamento Geral' }
const FILTROS = [
  { id: 'todas', label: 'Todas' },
  { id: 'pendentes', label: 'Pendentes' },
  { id: 'decididas', label: 'Decididas' },
]

export default function DecisoesCuradoria({ trilha = 'ri' }) {
  const [dados, setDados] = useState(null)
  const [error, setError] = useState(false)
  const [filtro, setFiltro] = useState('todas')

  useEffect(() => {
    setDados(null); setError(false)
    fetchJson('/database/decisoes_curadoria.json').then(setDados).catch(() => setError(true))
  }, [])

  const daTrilha = useMemo(() => decisoesDaTrilha(dados, trilha), [dados, trilha])
  const contagem = useMemo(() => contarDecisoes(daTrilha), [daTrilha])
  const lista = useMemo(() => filtrarDecisoes(daTrilha, filtro), [daTrilha, filtro])

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
        <div className="dec-filtros no-print">
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

        {lista.length === 0 ? (
          <div className="card" style={{ padding: 24, textAlign: 'center', color: 'var(--text-muted)' }}>
            Nenhuma decisão neste filtro.
          </div>
        ) : (
          lista.map(d => <DecisaoCard key={d.id} d={d} />)
        )}
      </div>
    </div>
  )
}

function DecisaoCard({ d }) {
  const [abertas, setAbertas] = useState({}) // índice da candidata -> aberta
  const [cmpAberta, setCmpAberta] = useState(false)
  const decidida = d.decidido

  return (
    <div className={`card dec-card${decidida ? ' dec-card-ok' : ''}`} style={{ marginBottom: 14, padding: 16 }}>
      <div className="dec-card-head">
        <h3 className="dec-titulo">{d.titulo}</h3>
        <span className={`dec-selo ${decidida ? 'dec-selo-ok' : 'dec-selo-pend'}`}>
          {decidida ? <><Check size={13} /> Decidida</> : <><AlertTriangle size={13} /> Pendente</>}
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

      {decidida && d.decisao && (
        <div className="dec-decisao">
          <div className="rg-heading">Decisão CBMRO</div>
          <p className="rg-caput">{d.decisao}</p>
        </div>
      )}
    </div>
  )
}
