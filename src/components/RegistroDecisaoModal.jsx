import { useEffect, useMemo, useState } from 'react'
import { X } from 'lucide-react'
import { fetchJson } from '../lib/dataCache.js'
import { scenarioDbUrl } from '../lib/scenario.js'
import { buildConferencia } from '../lib/conferencia.js'
import { caputDispositivoId } from '../lib/dispositivoId.js'
import { registrarDecisao } from '../lib/decisionsData.js'
import { saveFinalText } from '../lib/reviewData.js'

const ARQ = { ri: 'minuta_structure.json', reg: 'regulamento_structure.json' }
const semCenario = (id) => String(id ?? '').replace(/^reg:atual:/, 'reg:').replace(/^atual:/, '')

export default function RegistroDecisaoModal({ decisao: d, trilha, cenario, autor, onClose, onSaved }) {
  const [tipo, setTipo] = useState('redacao')
  const [texto, setTexto] = useState('')
  const [fonte, setFonte] = useState('Redação própria')
  const [oQueMuda, setOQueMuda] = useState('')
  const [onde, setOnde] = useState('')
  const [alvo, setAlvo] = useState(null)          // { editId, label, caput }
  const [textoFinal, setTextoFinal] = useState('')
  const [struct, setStruct] = useState(null)
  const [erro, setErro] = useState(null)
  const [salvando, setSalvando] = useState(false)
  const [decisaoGravada, setDecisaoGravada] = useState(false) // p/ repetir só o finalText

  const [structErro, setStructErro] = useState(false)
  useEffect(() => {
    setStructErro(false)
    fetchJson(scenarioDbUrl(cenario, ARQ[trilha]))
      .then(setStruct)
      .catch((e) => {
        // Distingue falha de carregamento de "capítulo não existe no cenário" —
        // antes a mensagem mandava trocar de cenário mesmo em erro de rede
        // (auditoria 2026-07-23).
        console.error('Erro ao carregar estrutura p/ registro de decisão:', e)
        setStruct(null)
        setStructErro(true)
      })
  }, [cenario, trilha])

  const artigos = useMemo(() => {
    if (!struct) return []
    const lista = buildConferencia(struct).filter(it => semCenario(it.chapterId) === d.chapterId)
    const porEditId = new Map()
    lista.forEach(it => porEditId.set(it.dispositivo.editId, (porEditId.get(it.dispositivo.editId) ?? 0) + 1))
    return lista.map(it => ({
      editId: it.dispositivo.editId,
      number: it.dispositivo.number,
      caput: it.dispositivo.caput,
      elegivel: porEditId.get(it.dispositivo.editId) === 1,
    }))
  }, [struct, d.chapterId])

  const escolher = (a) => { setAlvo(a); setTextoFinal(a.caput) }

  const podeSalvar = texto.trim() && !salvando && (
    tipo === 'estrutural' ? (oQueMuda.trim() && onde.trim()) : (alvo && textoFinal.trim()))

  const gravarFinal = async () => {
    await saveFinalText(caputDispositivoId(alvo.editId), { texto: textoFinal, status: 'fechado', autor })
  }

  const salvar = async () => {
    setSalvando(true); setErro(null)
    try {
      if (!decisaoGravada) {
        await registrarDecisao(d.id, {
          tipo, decisao: texto.trim(), fonteEscolhida: fonte,
          alvoDispositivoId: tipo === 'redacao' ? caputDispositivoId(alvo.editId) : null,
          ficha: tipo === 'estrutural' ? { oQueMuda: oQueMuda.trim(), onde: onde.trim(), status: 'aguardando' } : null,
        }, autor)
        setDecisaoGravada(true)
      }
      if (tipo === 'redacao') await gravarFinal()
      onSaved()
    } catch (e) {
      setErro(decisaoGravada
        ? `Decisão registrada, mas o texto final falhou: ${e.message}`
        : `Falha ao registrar: ${e.message}`)
    } finally { setSalvando(false) }
  }

  return (
    <div className="decm-overlay" role="dialog" aria-modal="true">
      <div className="decm card">
        <div className="decm-head">
          <h3>Registrar decisão</h3>
          <button className="btn btn-ghost" onClick={onClose}><X size={16} /></button>
        </div>
        <p className="dec-questao">{d.titulo}</p>

        <div className="decm-field">
          <label>Tipo</label>
          <label><input type="radio" checked={tipo === 'redacao'} onChange={() => setTipo('redacao')} /> Redação (muda o texto de um artigo)</label>
          <label><input type="radio" checked={tipo === 'estrutural'} onChange={() => setTipo('estrutural')} /> Estrutural (muda a estrutura — gera ficha de aplicação)</label>
        </div>

        <div className="decm-field">
          <label>Decisão (o que ficou decidido e por quê)</label>
          <textarea rows={4} value={texto} onChange={e => setTexto(e.target.value)} />
        </div>

        <div className="decm-field">
          <label>Fonte escolhida</label>
          <select value={fonte} onChange={e => setFonte(e.target.value)}>
            {[...d.candidatas.map(c => c.fonte), 'Redação própria'].map(f => <option key={f} value={f}>{f}</option>)}
          </select>
        </div>

        {tipo === 'redacao' && (
          <div className="decm-field">
            <label>Artigo alvo (cenário ativo: {cenario})</label>
            {artigos.length === 0 && (
              <p className="rg-empty">{structErro
                ? 'Não foi possível carregar a estrutura do documento (falha de conexão). Feche e tente de novo.'
                : 'Este capítulo não existe no cenário ativo — troque o cenário para aplicar a redação.'}</p>
            )}
            <div className="decm-artigos">
              {artigos.map(a => (
                <label key={`${a.editId}#${a.number}`} className={a.elegivel ? '' : 'decm-inelegivel'}>
                  <input type="radio" disabled={!a.elegivel} checked={alvo?.editId === a.editId}
                    onChange={() => escolher(a)} />
                  {' '}Art. {a.number} — {String(a.caput).slice(0, 90)}
                  {!a.elegivel && <em> (indisponível: artigo desdobrado de texto corrido)</em>}
                </label>
              ))}
            </div>
            {alvo && (
              <>
                <label>Texto final do artigo</label>
                <textarea rows={4} value={textoFinal} onChange={e => setTextoFinal(e.target.value)} />
              </>
            )}
          </div>
        )}

        {tipo === 'estrutural' && (
          <div className="decm-field">
            <label>O que muda</label>
            <textarea rows={2} value={oQueMuda} onChange={e => setOQueMuda(e.target.value)} />
            <label>Onde (órgãos/temas/arquivos envolvidos)</label>
            <input type="text" value={onde} onChange={e => setOnde(e.target.value)} />
          </div>
        )}

        {erro && (
          <div className="decm-erro">
            {erro}
            {decisaoGravada && tipo === 'redacao' && (
              <button className="btn btn-ghost" onClick={salvar}>Repetir gravação do texto final</button>
            )}
          </div>
        )}

        <div className="decm-acoes">
          <button className="btn btn-ghost" onClick={onClose}>Cancelar</button>
          <button className="btn" disabled={!podeSalvar} onClick={salvar}>
            {salvando ? 'Salvando…' : 'Registrar decisão'}
          </button>
        </div>
      </div>
    </div>
  )
}
