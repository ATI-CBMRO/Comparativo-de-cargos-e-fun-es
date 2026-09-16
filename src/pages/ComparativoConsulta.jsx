// Comparativo da consulta (admin): versão EM CONSULTA (lida pelos militares + correções) ×
// versão ATUAL (após as sugestões), artigo a artigo, lado a lado, com selo do tipo de
// mudança e download em .docx. Curadoria de 2026-09-14 (scripts/regulamento_curadoria_consulta.py).
import { useEffect, useMemo, useState } from 'react'
import { Packer } from 'docx'
import { Download } from 'lucide-react'
import { fetchJson } from '../lib/dataCache.js'
import { regulamentoDbUrl } from '../lib/scenario.js'
import { filtrarEstruturaPorEscopo } from '../lib/escopoServico.js'
import { articular } from '../lib/consultaRelatorios.js'
import { compararVersoes, resumoComparativo, ROTULO_TIPO, rotuloArtigo } from '../lib/comparativoConsulta.js'
import { docxComparativo } from '../lib/consultaDocx.js'
import { rotuloRomano } from '../lib/minutaArticles.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'

const BADGE = {
  igual: 'badge-gray', corrigido: 'badge-gray', alterado: 'badge-gold',
  reescrito: 'badge-gold', incluido: 'badge-green', suprimido: 'badge-red',
}

function Artigo({ art, num, vazio }) {
  if (!art) return <p style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>{vazio}</p>
  const a = articular(art)
  return (
    <div>
      <p style={{ margin: '0 0 6px' }}><strong>{rotuloArtigo(num)}</strong> {a.caput}</p>
      {a.incisos.map((inc, i) => (
        <p key={inc.index} style={{ margin: `0 0 4px ${inc.alinea ? 36 : 18}px` }}>{inc.ownMarker ? '' : <strong>{rotuloRomano(art.incisos, i)} - </strong>}{inc.text}</p>
      ))}
    </div>
  )
}

export default function ComparativoConsulta() {
  const [consulta, setConsulta] = useState(null)
  const [atual, setAtual] = useState(null)
  const [erro, setErro] = useState(null)
  const [filtro, setFiltro] = useState('mudancas') // 'mudancas' | 'tudo'
  const [gerando, setGerando] = useState(false)

  useEffect(() => {
    Promise.all([fetchJson(regulamentoDbUrl('atual', 'consulta')), fetchJson(regulamentoDbUrl('atual', 'atual'))])
      .then(([c, a]) => { setConsulta(c); setAtual(a) })
      .catch(() => setErro('Não foi possível carregar as duas versões do Regulamento (cenário atual).'))
  }, [])

  const comparacao = useMemo(() => {
    if (!consulta || !atual) return []
    return compararVersoes(filtrarEstruturaPorEscopo(consulta, 'servico'), filtrarEstruturaPorEscopo(atual, 'servico'))
  }, [consulta, atual])
  const resumo = useMemo(() => resumoComparativo(comparacao), [comparacao])

  async function baixar() {
    setGerando(true)
    try {
      let brasao = null
      try { const r = await fetch('/BrasaoCBMRO2D-COMPLETO.png'); if (r.ok) brasao = await r.arrayBuffer() } catch { /* sem brasão */ }
      const { doc } = docxComparativo({
        recorteConsulta: filtrarEstruturaPorEscopo(consulta, 'servico'),
        recorteAtual: filtrarEstruturaPorEscopo(atual, 'servico'),
        brasao,
      })
      const blob = await Packer.toBlob(doc)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `Comparativo_Consulta_Regulamento_de_Servico_${new Date().toISOString().slice(0, 10)}.docx`
      document.body.appendChild(a); a.click(); document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } finally { setGerando(false) }
  }

  if (erro) return <ErrorState title="Erro ao carregar" hint={erro} />
  if (!consulta || !atual) return <LoadingState label="Carregando as duas versões…" />

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Comparativo da consulta — Regulamento de Serviço</h2>
          <p className="page-subtitle">
            Esquerda: a minuta como foi disponibilizada aos militares (sem os dispositivos suprimidos pela curadoria). Direita: a versão atual, após a
            revisão de texto e as sugestões. Numeração de cada versão.
          </p>
          <p className="rev-progresso">
            {resumo.igual} sem alteração · {resumo.corrigido} com correção de texto · {resumo.alterado} com texto alterado ·{' '}
            {resumo.reescrito} reescritos · {resumo.incluido} novos · {resumo.suprimido} suprimidos · {resumo.propostas} proposta(s) pendente(s) de deliberação
          </p>
          <div className="rev-doc-switch" role="group" aria-label="Filtro">
            <button type="button" className={`oc-state-chip${filtro === 'mudancas' ? ' active' : ''}`} onClick={() => setFiltro('mudancas')}>Só o que mudou</button>
            <button type="button" className={`oc-state-chip${filtro === 'tudo' ? ' active' : ''}`} onClick={() => setFiltro('tudo')}>Todos os artigos</button>
            <button type="button" className="btn btn-primary btn-sm" style={{ marginLeft: 12 }} disabled={gerando} onClick={baixar}>
              <Download size={14} />{gerando ? 'Gerando…' : 'Baixar comparativo (.docx)'}
            </button>
          </div>
        </div>
      </div>
      <div className="page-body">
        {comparacao.map(cap => {
          const entradas = filtro === 'tudo' ? cap.entradas : cap.entradas.filter(e => e.tipo !== 'igual')
          if (!entradas.length) return null
          return (
            <section key={cap.capitulo} style={{ marginBottom: 28 }}>
              <p className="rev-chapter">{cap.capitulo}</p>
              {entradas.map((e, i) => (
                <div key={`${cap.capitulo}-${i}`} className="card" style={{ marginBottom: 12, borderLeft: e.proposta ? '4px solid var(--cbm-red-700)' : undefined }}>
                  <div className="card-header" style={{ marginBottom: 8, flexWrap: 'wrap', gap: 8 }}>
                    <span className="card-title" style={{ fontSize: 14 }}>
                      {rotuloArtigo(e.numAntes)} (consulta) → {rotuloArtigo(e.numDepois)} (atual)
                    </span>
                    <span>
                      <span className={`badge ${BADGE[e.tipo]}`}>{ROTULO_TIPO[e.tipo]}</span>
                      {e.proposta && <span className="badge badge-red" style={{ marginLeft: 6 }}>proposta pendente de deliberação</span>}
                    </span>
                  </div>
                  {(e.nota || e.motivo) && <p style={{ fontSize: 12, color: 'var(--text-muted)', margin: '0 0 10px' }}>{e.nota ?? e.motivo}</p>}
                  <div className="grid-2" style={{ fontSize: 13, lineHeight: 1.5 }}>
                    <div style={{ background: 'var(--gray-50)', padding: 10, borderRadius: 8 }}>
                      <Artigo art={e.antes} num={e.numAntes} vazio={e.tipo === 'incluido' ? 'Não existia na versão em consulta.' : 'Mesmo artigo da linha anterior.'} />
                    </div>
                    <div style={{ background: e.tipo === 'suprimido' ? 'rgba(200,16,46,0.05)' : 'rgba(22,163,74,0.05)', padding: 10, borderRadius: 8 }}>
                      <Artigo art={e.depois} num={e.numDepois} vazio="Suprimido na versão atual." />
                    </div>
                  </div>
                </div>
              ))}
            </section>
          )
        })}
      </div>
    </>
  )
}
