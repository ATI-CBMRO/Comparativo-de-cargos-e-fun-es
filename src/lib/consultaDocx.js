// Geração dos QUATRO .docx do pacote da consulta do Regulamento de Serviço, com a lib `docx`
// (a mesma do Wizard). Cada função devolve um `Document`; quem chama empacota com
// Packer.toBlob (navegador) ou Packer.toBuffer (Node). Sem React, sem Firebase: recebe os
// dados já resolvidos pela lógica pura de consultaRelatorios.js / regulamentoReestruturado.js.
import {
  Document, Paragraph, TextRun, Footer, AlignmentType, PageBreak, ImageRun, PageNumber,
  Table, TableRow, TableCell, WidthType,
} from 'docx'
import { articleLabel, romanize, rotuloRomano } from './minutaArticles.js'
import { resumoForaDoEscopo } from './escopoServico.js'
import {
  articular, aplicarFinais, formatarDataHora, quadroAnalise, resumoParticipacao,
  ROTULO_PARECER, ROTULO_SITUACAO, ROTULO_APLICACAO,
} from './consultaRelatorios.js'

const rotuloAplicacao = (r) => ROTULO_APLICACAO[r.aplicacao?.como] ?? ROTULO_APLICACAO.nenhuma
const textoAplicacao = (r) => `${rotuloAplicacao(r)}${r.aplicacao?.nota ? ` — ${r.aplicacao.nota}` : ''}`
const tabelaAplicacoes = (resumo) => tabela(
  [['Aplicação dada pela curadoria', 'Sugestões'],
    ...Object.keys(ROTULO_APLICACAO).filter(k => resumo.aplicacoes[k]).map(k => [ROTULO_APLICACAO[k], String(resumo.aplicacoes[k])]),
    ['Total', String(resumo.total)]],
  [7000, 1300],
)
import { montarReestruturada } from './regulamentoReestruturado.js'
import { capitalizarFrases } from './formatacaoTexto.js'
import { compararVersoes, resumoComparativo, ROTULO_TIPO, rotuloArtigo } from './comparativoConsulta.js'

const FONT = 'Times New Roman'
const run = (text, o = {}) => new TextRun({ text, font: FONT, size: 24, ...o })

function pCentro(text, { bold = true, size = 26, before = 240, after = 120, italics = false, pageBreakBefore = false } = {}) {
  return new Paragraph({ alignment: AlignmentType.CENTER, pageBreakBefore, spacing: { before, after }, children: [run(text, { bold, size, italics })] })
}
function pJust(text, { italics = false, size = 24, after = 120, firstLine = 708, bold = false } = {}) {
  return new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { line: 360, after }, indent: firstLine ? { firstLine } : undefined, children: [run(text, { italics, size, bold })] })
}
const quebra = () => new Paragraph({ children: [new PageBreak()] })
const dataExtenso = () => new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })

function cabecalho(subtitulo, linhaExtra, brasao) {
  const children = []
  if (brasao) {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, children: [new ImageRun({ data: brasao, transformation: { width: 65, height: 65 }, type: 'png' })] }))
  }
  children.push(
    pCentro('CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA', { size: 28, before: 120, after: 0 }),
    pCentro(subtitulo, { bold: false, size: 24, before: 0, after: 0 }),
  )
  if (linhaExtra) children.push(pCentro(linhaExtra, { bold: false, size: 22, italics: true, before: 0, after: 0 }))
  children.push(pCentro(dataExtenso(), { bold: false, size: 22, italics: true, before: 0, after: 480 }))
  return children
}

function tabela(linhas, larguras) {
  const cell = (texto, { bold = false, shade } = {}) => new TableCell({
    shading: shade ? { fill: shade } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: String(texto ?? '').split('\n').map(l => new Paragraph({ spacing: { after: 0 }, children: [run(l, { size: 20, bold })] })),
  })
  const rows = linhas.map((l, i) => new TableRow({ tableHeader: i === 0, children: l.map(t => cell(t, { bold: i === 0, shade: i === 0 ? 'E8E8E8' : undefined })) }))
  return new Table({ rows, width: { size: 100, type: WidthType.PERCENTAGE }, columnWidths: larguras })
}

// `publicavel`: sem selos de curadoria e com a primeira letra de cada frase em maiúscula.
function paragrafosArtigo(numero, art, { publicavel = false } = {}) {
  const ps = []
  const fmt = (t) => (publicavel ? capitalizarFrases(t) : t)
  const capRuns = [run(`${articleLabel(numero)} `, { bold: true }), run(fmt(art.caput))]
  if (art.temFinal && !publicavel) capRuns.push(run(' [texto final aplicado]', { italics: true, size: 18, color: '888888' }))
  ps.push(new Paragraph({
    alignment: AlignmentType.JUSTIFIED, spacing: { line: 360, after: art.incisos.length ? 60 : 120 },
    indent: art.incisos.length ? undefined : { firstLine: 708 }, children: capRuns,
  }))
  art.incisos.forEach((inc, i) => {
    ps.push(new Paragraph({
      alignment: AlignmentType.JUSTIFIED, spacing: { line: 360, after: 60 },
      indent: { left: inc.alinea ? 1134 : 708, hanging: inc.ownMarker ? 0 : 340 },
      children: [run(inc.ownMarker ? fmt(inc.text) : `${rotuloRomano(art.incisos, i)} - ${fmt(inc.text)}`)],
    }))
  })
  return ps
}

function documento(children, rodape) {
  return new Document({
    styles: { default: { document: { run: { font: FONT, size: 24 } } } },
    sections: [{
      properties: { page: { margin: { top: 1701, right: 1134, bottom: 1134, left: 1701 } } },
      footers: { default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [run(`${rodape} · pág. `, { size: 18, italics: true }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18, italics: true })],
      })] }) },
      children,
    }],
  })
}

// 1. Minuta em consulta — o recorte exatamente como o participante vê, com finais aplicados.
export function docxMinutaConsulta({ completa, recorte, finals, brasao }) {
  const fora = resumoForaDoEscopo(completa, recorte, 'servico')
  const total = recorte.chapters.reduce((n, c) => n + c.articles.length, 0)
  const children = cabecalho(
    'Minuta do Regulamento de Serviço — 1ª etapa (recorte submetido à consulta dos militares)',
    'Versão em consulta no Portal de Legislação CBM · cenário: Lei nº 2.204/2009 (LOB vigente)', brasao,
  )
  children.push(pJust(
    `Este documento reproduz a minuta tal como publicada no portal para os militares com acesso restrito ao Regulamento de Serviço, sem as correções e alterações posteriores da curadoria (que estão na versão atual e no Comparativo): ${total} artigos, reunindo o serviço operacional (COB), a Central de Operações e o teledespacho, o serviço interno e de dia, as atribuições das funções (somente COB e CAT) e o serviço técnico de segurança contra incêndio e pânico (CAT). Ficam para o Regulamento Geral completo ${fora.artigosEmCapitulosFora} artigos de ${fora.capitulosFora.length} capítulos${fora.artigosCortadosNoEscopo ? ` e ${fora.artigosCortadosNoEscopo} artigos das funções dos demais órgãos` : ''}. A numeração é provisória. Textos finais fechados no portal estão aplicados e sinalizados; fechamentos sem texto mantêm o original.`,
    { italics: true, size: 22, after: 240 },
  ))
  let numero = 0
  let aplicados = 0
  recorte.chapters.forEach((cap, ci) => {
    children.push(pCentro(`CAPÍTULO ${romanize(ci + 1)}`, { pageBreakBefore: ci > 0, after: 0 }))
    children.push(pCentro(cap.chapterTitle, { before: 0 }))
    let ultimo = null
    const variaHeading = cap.articles.some(a => a.heading !== cap.articles[0]?.heading)
    for (const leaf of cap.articles) {
      if (variaHeading && leaf.heading && leaf.heading !== ultimo) children.push(pCentro(leaf.heading, { size: 22, before: 160, after: 80, italics: true }))
      ultimo = leaf.heading ?? ultimo
      const art = aplicarFinais(articular(leaf), finals)
      if (art.temFinal) aplicados += 1
      numero += 1
      children.push(...paragrafosArtigo(numero, art))
    }
  })
  return { doc: documento(children, 'Minuta do Regulamento de Serviço — CBMRO · Portal de Legislação CBM'), artigos: numero, aplicados }
}

// 2. Relatório das interações (para o SEI).
export function docxRelatorioInteracoes({ interacoes, membros, totalArtigos, brasao, desde = null }) {
  const resumo = resumoParticipacao(membros, interacoes)
  const children = cabecalho(
    'Relatório das interações recebidas na consulta da Minuta do Regulamento de Serviço',
    'Portal de Legislação CBM — acesso "Só Regulamento de Serviço" · cenário: Lei nº 2.204/2009', brasao,
  )
  children.push(pJust(
    `A minuta do Regulamento de Serviço (1ª etapa, ${totalArtigos} artigos) foi submetida à apreciação dos militares cadastrados no Portal de Legislação CBM com acesso restrito ao Regulamento de Serviço, que puderam registrar sugestões dispositivo a dispositivo. Este relatório consolida ${resumo.total} interações dos militares consultados${desde ? `, registradas a partir de ${desde.toLocaleDateString('pt-BR')}` : ''}. Cada registro identifica o autor, a unidade, o dispositivo comentado (numeração da versão em consulta), o trecho, o texto integral da sugestão, reproduzido como foi escrito, e o que a versão atual da minuta fez com o artigo comentado (reescrito, artigo novo incluído, texto alterado, suprimido ou sem alteração).`,
    { size: 22, after: 200 },
  ))
  children.push(pCentro('1. Participantes e quantidade de sugestões', { size: 24, before: 240, after: 120 }))
  children.push(pJust(`Militares cadastrados com acesso restrito: ${resumo.cadastradosEscopo}${resumo.contasEscopo > resumo.cadastradosEscopo ? ` (${resumo.contasEscopo} contas — o mesmo militar pode ter mais de um cadastro; os registros foram somados por pessoa)` : ''}; destes, ${resumo.contribuintes} registr${resumo.contribuintes === 1 ? 'ou' : 'aram'} sugestão.`, { size: 22, firstLine: 0 }))
  children.push(tabela(
    [['Autor', 'Nome de guerra', 'Unidade', 'Alcance no portal', 'Sugestões'],
      ...resumo.porAutor.map(e => [e.autor.nome, e.autor.nomeGuerra, e.autor.unidade, e.autor.alcance, String(e.qtd)])],
    [2600, 1500, 2800, 1500, 900],
  ))
  children.push(pCentro('2. Sugestões por capítulo da minuta', { size: 24, before: 240, after: 120 }))
  children.push(tabela([['Capítulo', 'Sugestões'], ...resumo.porCapitulo.map(c => [c.capitulo, String(c.qtd)])], [7000, 1300]))
  children.push(pCentro('3. Aplicação das sugestões na versão atual da minuta', { size: 24, before: 240, after: 120 }))
  children.push(pJust(`${resumo.aplicadas} das ${resumo.total} sugestões recaem sobre artigos alterados na versão atual da minuta; ${resumo.total - resumo.aplicadas} sobre artigos mantidos como estavam. O Comparativo (versão em consulta × versão atual) mostra cada alteração artigo a artigo; as propostas que mudam regra de mérito estão marcadas como pendentes de deliberação do CONDEG.`, { size: 22, firstLine: 0 }))
  children.push(tabelaAplicacoes(resumo))
  children.push(quebra())
  children.push(pCentro('4. Interações, dispositivo a dispositivo', { size: 24, before: 240, after: 120 }))
  let capAtual = null
  let artAtual = null
  for (const r of interacoes) {
    if (r.capitulo !== capAtual) { capAtual = r.capitulo; artAtual = null; children.push(pCentro(capAtual, { size: 22, before: 240, after: 80 })) }
    const cabecaArt = r.dispositivo.split(',')[0]
    if (cabecaArt !== artAtual) { artAtual = cabecaArt; children.push(pJust(`${cabecaArt} — ${r.caputArtigo}`, { size: 20, bold: true, firstLine: 0, after: 60 })) }
    const meta = [`nº ${r.n}`, formatarDataHora(r.data), r.curtidas ? `${r.curtidas} apoio(s)` : null, r.textoFinal ? 'texto final redigido' : r.suprimido ? 'dispositivo suprimido' : r.finalVazio ? 'conferido' : null].filter(Boolean).join(' · ')
    children.push(tabela([
      ['Registro', meta],
      ['Autor', `${r.autor.nome}${r.autor.nomeGuerra ? ` (${r.autor.nomeGuerra})` : ''}${r.autor.unidade ? ` — ${r.autor.unidade}` : ''}`],
      ['Dispositivo', `${r.dispositivo}${r.rotuloNaEpoca && !r.dispositivo.startsWith(r.rotuloNaEpoca.split(',')[0]) ? ` (na época: ${r.rotuloNaEpoca})` : ''} · ${r.dispositivoId}`],
      ['Trecho comentado', r.trecho],
      ['Sugestão', r.sugestao],
      ['Aplicação', textoAplicacao(r)],
    ], [1800, 7500]))
    children.push(new Paragraph({ spacing: { after: 120 }, children: [] }))
  }
  return { doc: documento(children, 'Interações da consulta — Minuta do Regulamento de Serviço · CBMRO'), resumo }
}

// 3. Quadro de análise e aplicação — por artigo, com o parecer registrado no portal.
export function docxQuadroAnalise({ interacoes, membros, brasao }) {
  const resumo = resumoParticipacao(membros, interacoes)
  const quadro = quadroAnalise(interacoes)
  const children = cabecalho(
    'Quadro de análise e aplicação das sugestões — Minuta do Regulamento de Serviço',
    'Pareceres e textos finais registrados no Portal de Legislação CBM', brasao,
  )
  children.push(pJust(
    `Este quadro consolida, artigo a artigo, as ${resumo.total} sugestões recebidas dos militares consultados sobre a minuta em consulta e o tratamento dado a cada uma: o que a versão atual da minuta fez com o artigo (${resumo.aplicadas} sugestões sobre artigos alterados, ${resumo.total - resumo.aplicadas} sobre artigos mantidos) e o parecer registrado no portal (${resumo.pareceres.relevante} acolhida(s) como relevante(s), ${resumo.pareceres.descartada} descartada(s) e ${resumo.pareceres.pendente} ainda sem parecer). Para cada artigo consta também a situação do texto final (redigido, conferido sem alteração, suprimido ou em aberto). O parecer é registrado pelo administrador no balão de cada sugestão (✅ relevante / ⛔ descartar) e o texto final no campo "Redação final".`,
    { size: 22, after: 200 },
  ))
  children.push(tabelaAplicacoes(resumo))
  children.push(new Paragraph({ spacing: { after: 120 }, children: [] }))
  children.push(tabela([
    ['Situação no portal', 'Quantidade'],
    ['Sugestões acolhidas (relevantes)', String(resumo.pareceres.relevante)],
    ['Sugestões descartadas', String(resumo.pareceres.descartada)],
    ['Sem parecer', String(resumo.pareceres.pendente)],
    ['Artigos com sugestão', String(quadro.length)],
    ['Artigos com texto final redigido', String(quadro.filter(q => q.situacaoFinal === 'redigido').length)],
    ['Artigos suprimidos', String(quadro.filter(q => q.situacaoFinal === 'suprimido').length)],
    ['Artigos conferidos sem alteração', String(quadro.filter(q => q.situacaoFinal === 'conferido').length)],
    ['Artigos em aberto', String(quadro.filter(q => q.situacaoFinal === 'aberto').length)],
  ], [6000, 2300]))
  children.push(quebra())
  let capAtual = null
  for (const q of quadro) {
    if (q.capitulo !== capAtual) { capAtual = q.capitulo; children.push(pCentro(capAtual, { size: 22, before: 240, after: 80 })) }
    children.push(pJust(`${q.rotulo} — ${q.caput}`, { size: 20, bold: true, firstLine: 0, after: 40 }))
    children.push(pJust(`Situação do texto final: ${ROTULO_SITUACAO[q.situacaoFinal]}${q.itens.find(i => i.textoFinal) ? ` — "${q.itens.find(i => i.textoFinal).textoFinal}"` : ''}`, { size: 20, italics: true, firstLine: 0, after: 60 }))
    children.push(tabela([
      ['Dispositivo', 'Autor', 'Sugestão', 'Aplicação', 'Parecer'],
      ...q.itens.map(i => [i.dispositivo.replace(`${q.rotulo}, `, ''), `${i.autor.nome}${i.autor.nomeGuerra ? ` (${i.autor.nomeGuerra})` : ''}`, i.sugestao, textoAplicacao(i), ROTULO_PARECER[i.parecer] ?? i.parecer]),
    ], [1300, 1600, 3000, 2400, 1000]))
    children.push(new Paragraph({ spacing: { after: 120 }, children: [] }))
  }
  return { doc: documento(children, 'Quadro de análise — Minuta do Regulamento de Serviço · CBMRO'), resumo, quadro }
}

// 5. Comparativo: versão em consulta × versão atual, artigo a artigo (curadoria 2026-09-14).
function textoArtigo(a) {
  if (!a) return ''
  const art = articular(a)
  return [art.caput, ...art.incisos.map((inc, i) => (inc.ownMarker ? `${inc.alinea ? '    ' : ''}${inc.text}` : `${rotuloRomano(art.incisos, i)} - ${inc.text}`))].join('\n')
}
export function docxComparativo({ recorteConsulta, recorteAtual, brasao }) {
  const comparacao = compararVersoes(recorteConsulta, recorteAtual)
  const r = resumoComparativo(comparacao)
  const children = cabecalho(
    'Comparativo — Minuta do Regulamento de Serviço: versão em consulta × versão atual',
    'Curadoria das sugestões recebidas na consulta aos militares (ago/2026)', brasao,
  )
  children.push(pJust(
    `A coluna da esquerda traz a minuta exatamente como foi disponibilizada aos militares; a da direita, a versão atual, produzida após a consulta (revisão de texto da curadoria e sugestões recebidas). Resumo: ${r.igual} artigos sem alteração, ${r.corrigido} com correção de texto (grafia, concordância, resíduos de extração, nomenclatura), ${r.alterado} com texto alterado, ${r.reescrito} reescritos, ${r.incluido} incluídos e ${r.suprimido} suprimidos; ${r.propostas} artigo(s) marcado(s) como proposta pendente de deliberação do CONDEG. Artigos sem alteração aparecem só pelo número, para o documento caber.`,
    { italics: true, size: 22, after: 240 },
  ))
  for (const cap of comparacao) {
    children.push(pCentro(cap.capitulo, { size: 24, before: 240, after: 120 }))
    const iguais = cap.entradas.filter(e => e.tipo === 'igual')
    if (iguais.length) children.push(pJust(`Sem alteração: ${iguais.map(e => `${rotuloArtigo(e.numAntes)}→${rotuloArtigo(e.numDepois)}`).join(', ')}.`, { size: 20, italics: true, firstLine: 0 }))
    for (const e of cap.entradas) {
      if (e.tipo === 'igual') continue
      const rotulo = `${ROTULO_TIPO[e.tipo]}${e.proposta ? ' · PROPOSTA PENDENTE DE DELIBERAÇÃO' : ''}`
      children.push(pJust(`${rotuloArtigo(e.numAntes)} (consulta) → ${rotuloArtigo(e.numDepois)} (atual) — ${rotulo}`, { size: 20, bold: true, firstLine: 0, after: 40 }))
      if (e.nota || e.motivo) children.push(pJust(e.nota ?? e.motivo, { size: 18, italics: true, firstLine: 0, after: 60 }))
      children.push(tabela([
        ['Versão em consulta', 'Versão atual'],
        [textoArtigo(e.antes) || (e.tipo === 'incluido' ? '(não existia)' : ''), textoArtigo(e.depois) || (e.tipo === 'suprimido' ? '(suprimido)' : '')],
      ], [4650, 4650]))
      children.push(new Paragraph({ spacing: { after: 120 }, children: [] }))
    }
  }
  return { doc: documento(children, 'Comparativo da consulta — Minuta do Regulamento de Serviço · CBMRO'), resumo: r }
}

// 4. Minuta reestruturada (Parte Geral + Parte Especial) — formato PUBLICÁVEL (2026-09-15):
// sem autoria da estrutura, sem texto introdutório, sem anexos, sem selos de curadoria, com a
// primeira letra de cada frase em maiúscula. Gerada a partir da versão ATUAL do recorte.
export function docxMinutaReestruturada({ recorte, finals = null, brasao }) {
  const r = montarReestruturada(recorte, finals)
  const children = cabecalho('Minuta do Regulamento de Serviço', null, brasao)
  for (const b of r.blocos) {
    if (b.tipo === 'parte') {
      children.push(pCentro(b.texto, { size: 30, before: 240, after: b.subtitulo ? 0 : 240, pageBreakBefore: b.quebraAntes }))
      if (b.subtitulo) children.push(pCentro(b.subtitulo, { bold: false, italics: true, size: 22, before: 0, after: 240 }))
    } else if (b.tipo === 'titulo') {
      children.push(pCentro(b.texto, { size: 28, before: 240, after: 200 }))
    } else if (b.tipo === 'capitulo') {
      children.push(pCentro(b.rotulo, { after: 0, before: 240 }))
      children.push(pCentro(b.texto, { before: 0 }))
    } else {
      children.push(...paragrafosArtigo(b.numero, b.art, { publicavel: true }))
    }
  }
  return { doc: documento(children, 'Minuta do Regulamento de Serviço — CBMRO'), artigos: r.totalArtigos, aplicados: r.aplicados, depara: r.depara }
}
