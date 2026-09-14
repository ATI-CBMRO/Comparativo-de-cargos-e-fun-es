// Tela do administrador: pacote da consulta da Minuta do Regulamento de Serviço, gerado no
// navegador (spec 2026-09-14). Quatro .docx: a minuta em consulta, o relatório de
// interações para o SEI, o quadro de análise (pareceres registrados no portal) e a minuta
// reestruturada em Parte Geral/Especial. Lê o que o admin já enxerga (suggestions,
// finalTexts, members); nada é gravado.
import { useEffect, useMemo, useState } from 'react'
import { Packer } from 'docx'
import { Download, Users, MessageSquare, CheckSquare, FileText } from 'lucide-react'
import { useAuth } from '../lib/auth.jsx'
import { fetchJson } from '../lib/dataCache.js'
import { scenarioDbUrl } from '../lib/scenario.js'
import { subscribeSuggestions, subscribeFinalTexts } from '../lib/reviewData.js'
import { subscribeMembers } from '../lib/membersData.js'
import { filtrarEstruturaPorEscopo } from '../lib/escopoServico.js'
import { indexarRecorte, selecionarInteracoes, resumoParticipacao } from '../lib/consultaRelatorios.js'
import {
  docxMinutaConsulta, docxRelatorioInteracoes, docxQuadroAnalise, docxMinutaReestruturada,
} from '../lib/consultaDocx.js'
import { LoadingState, ErrorState } from '../components/Status.jsx'
import AvisoSincronizacao from '../components/AvisoSincronizacao.jsx'

async function carregarBrasao() {
  try {
    const resp = await fetch('/BrasaoCBMRO2D-COMPLETO.png')
    return resp.ok ? await resp.arrayBuffer() : null
  } catch { return null }
}

function baixar(blob, nome) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = nome
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

function Indicador({ icon: Icon, label, value, desc, accent = '' }) {
  return (
    <div className={`stat-card ${accent}`}>
      <div className="stat-card-top">
        <div className="stat-card-icon" style={{ background: 'rgba(200,16,46,0.08)' }}><Icon size={18} color="var(--cbm-red-700)" /></div>
        <span className="stat-label">{label}</span>
      </div>
      <span className="stat-value">{value}</span>
      <span className="stat-desc">{desc}</span>
    </div>
  )
}

export default function ConsultaRegulamentoServico() {
  const { user } = useAuth()
  const [completa, setCompleta] = useState(null)
  const [erro, setErro] = useState(null)
  const [sugestoes, setSugestoes] = useState([])
  const [finals, setFinals] = useState(new Map())
  const [membros, setMembros] = useState([])
  const [syncErro, setSyncErro] = useState(false)
  const [gerando, setGerando] = useState(null)
  const [aviso, setAviso] = useState(null)

  // A consulta é SEMPRE sobre o cenário atual (a rota /regulamento/servico trava nele).
  useEffect(() => {
    fetchJson(scenarioDbUrl('atual', 'regulamento_structure.json'))
      .then(setCompleta)
      .catch(() => setErro('Não foi possível carregar a minuta do Regulamento (cenário atual).'))
  }, [])
  useEffect(() => subscribeSuggestions(
    (v) => { setSugestoes(v); setSyncErro(false) },
    (e) => { console.error('Erro nas sugestões:', e); setSyncErro(true) },
  ), [])
  useEffect(() => subscribeFinalTexts(
    setFinals,
    (e) => { console.error('Erro nos textos finais:', e); setSyncErro(true) },
  ), [])
  useEffect(() => subscribeMembers(
    setMembros,
    (e) => { console.error('Erro nos membros:', e); setSyncErro(true) },
  ), [])

  const recorte = useMemo(() => (completa ? filtrarEstruturaPorEscopo(completa, 'servico') : null), [completa])
  const indice = useMemo(() => (recorte ? indexarRecorte(recorte) : null), [recorte])
  const interacoes = useMemo(
    () => (indice ? selecionarInteracoes({ sugestoes, membros, indice, finals }) : []),
    [indice, sugestoes, membros, finals],
  )
  const resumo = useMemo(() => resumoParticipacao(membros, interacoes), [membros, interacoes])
  const totalArtigos = useMemo(() => (recorte ? recorte.chapters.reduce((n, c) => n + c.articles.length, 0) : 0), [recorte])
  const finaisNoRecorte = useMemo(() => {
    let n = 0
    finals.forEach((f, id) => { if (f.status === 'fechado' && indice?.has(String(id).split('#')[0])) n += 1 })
    return n
  }, [finals, indice])

  async function gerar(qual) {
    setGerando(qual)
    setAviso(null)
    try {
      const brasao = await carregarBrasao()
      const data = new Date().toISOString().slice(0, 10)
      let out
      if (qual === 'minuta') {
        out = docxMinutaConsulta({ completa, recorte, finals, brasao })
        baixar(await Packer.toBlob(out.doc), `Minuta_Regulamento_de_Servico_em_consulta_${data}.docx`)
      } else if (qual === 'relatorio') {
        out = docxRelatorioInteracoes({ interacoes, membros, totalArtigos, brasao })
        baixar(await Packer.toBlob(out.doc), `Relatorio_Interacoes_Consulta_Regulamento_de_Servico_${data}.docx`)
      } else if (qual === 'quadro') {
        out = docxQuadroAnalise({ interacoes, membros, brasao })
        baixar(await Packer.toBlob(out.doc), `Quadro_Analise_Aplicacao_Regulamento_de_Servico_${data}.docx`)
      } else {
        out = docxMinutaReestruturada({ recorte, finals, brasao })
        baixar(await Packer.toBlob(out.doc), `Minuta_Regulamento_de_Servico_reestruturada_${data}.docx`)
      }
      if (out.aplicados != null) setAviso(`Gerado: ${out.artigos} artigos, ${out.aplicados} com texto final aplicado.`)
      else setAviso(`Gerado com ${interacoes.length} interações.`)
    } catch (e) {
      console.error(e)
      setAviso(`Não foi possível gerar o documento: ${e.message}`)
    } finally {
      setGerando(null)
    }
  }

  if (erro) return <ErrorState title="Erro ao carregar" hint={erro} />
  if (!completa) return <LoadingState label="Carregando a minuta em consulta…" />

  const semParecer = resumo.pareceres.pendente
  const botoes = [
    { k: 'minuta', titulo: '1. Minuta em consulta', desc: `Os ${recorte.chapters.length} capítulos e ${totalArtigos} artigos exatamente como o participante os vê, com os textos finais fechados aplicados.` },
    { k: 'relatorio', titulo: '2. Relatório das interações (SEI)', desc: 'Quem sugeriu (nome, nome de guerra, unidade), dispositivo, trecho e texto integral de cada sugestão; resumos por participante e por capítulo.' },
    { k: 'quadro', titulo: '3. Quadro de análise e aplicação', desc: `Sugestões por artigo com o parecer registrado no portal (relevante / descartada) e a situação do texto final. ${semParecer ? `${semParecer} sugestão(ões) ainda sem parecer.` : 'Todas as sugestões têm parecer.'}` },
    { k: 'reestruturada', titulo: '4. Minuta reestruturada (Parte Geral e Parte Especial)', desc: 'Os mesmos artigos reordenados na estrutura sugerida pelo Cel. Luiz Eduardo, com a correspondência de numeração e as notas de ajuste a deliberar.' },
  ]

  return (
    <>
      <div className="page-header">
        <div className="page-header-left">
          <h2 className="page-title">Consulta — Regulamento de Serviço</h2>
          <p className="page-subtitle">
            Pacote da consulta aos militares com acesso restrito ao Regulamento de Serviço, gerado aqui mesmo a partir
            do que está no portal. Os pareceres saem dos botões ✅/⛔ e o texto final do campo "Redação final" de cada
            balão na tela de revisão.
          </p>
        </div>
      </div>
      <div className="page-body">
        <AvisoSincronizacao visivel={syncErro} />
        <div className="grid-4" style={{ marginBottom: 20 }}>
          <Indicador icon={Users} label="Consultados" value={resumo.cadastradosEscopo} desc={`${resumo.contribuintes} registraram sugestão`} accent="red" />
          <Indicador icon={MessageSquare} label="Sugestões" value={resumo.total} desc={`${resumo.dosConsultados} dos consultados · ${resumo.daEquipe} da equipe`} accent="gold" />
          <Indicador icon={CheckSquare} label="Com parecer" value={resumo.pareceres.relevante + resumo.pareceres.descartada} desc={`${resumo.pareceres.relevante} relevantes · ${resumo.pareceres.descartada} descartadas`} accent="green" />
          <Indicador icon={FileText} label="Textos finais" value={finaisNoRecorte} desc={`dispositivos fechados no recorte de ${totalArtigos} artigos`} />
        </div>
        {aviso && <div className="form-error" style={{ marginBottom: 12, background: 'rgba(22,163,74,0.08)', color: '#15803d', borderColor: 'rgba(22,163,74,0.25)' }}>{aviso}</div>}
        <div className="grid-2">
          {botoes.map(b => (
            <div key={b.k} className="card">
              <div className="card-header"><span className="card-title">{b.titulo}</span></div>
              <p style={{ color: 'var(--text-secondary)', fontSize: 13, marginBottom: 14, lineHeight: 1.5 }}>{b.desc}</p>
              <button
                type="button" className="btn btn-primary" disabled={gerando != null || !user}
                onClick={() => gerar(b.k)}
              >
                <Download size={16} />{gerando === b.k ? 'Gerando…' : 'Baixar .docx'}
              </button>
            </div>
          ))}
        </div>
      </div>
    </>
  )
}
