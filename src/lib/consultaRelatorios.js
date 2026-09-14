// Lógica PURA do pacote da consulta do Regulamento de Serviço (spec 2026-09-14): índice do
// recorte em consulta, localização de um dispositivoId no texto, autoria (sugestão ×
// cadastro), aplicação de textos finais e o quadro de análise por artigo. Sem React, sem
// Firebase, sem docx — usada pelo app (tela do admin) e pelos scripts Node de docs/sei/.
import { normalizeInciso, hasOwnMarker, romanize, articleLabel } from './minutaArticles.js'
import { temaDoCapitulo } from './escopoServico.js'
import { parseDispositivoId } from './dispositivoId.js'

export const SUPRIMIDO = '(dispositivo suprimido — decisão registrada no portal)'

// Converte um nó `kind:'incisos'` da estrutura em { caput, incisos[] } como o portal exibe
// (normalizeInciso/hasOwnMarker), preservando o índice ORIGINAL de cada item — é ele que
// forma o endereço estável editId#index dos comentários.
export function articular(leaf) {
  const kept = []
  ;(leaf.items ?? []).forEach((it, i) => { if ((it.text ?? '').trim()) kept.push({ it, i }) })
  const incisos = kept.map((k, pos) => ({
    text: normalizeInciso(k.it.text, pos, kept.length),
    ownMarker: hasOwnMarker(k.it.text),
    index: k.i,
  }))
  return { caput: leaf.caput ?? '', incisos, editId: leaf.editId, id: leaf.id }
}

// Interpreta um documento de finalTexts. Achado da exportação de 11/09/2026: 53 dos 94
// "fechados" têm texto VAZIO (o admin clicou "Salvar e fechar" sem redigir) e 13 são só
// "Excluir". Aqui: vazio = conferido, texto original mantido; "Excluir" = suprimido.
export function textoFinalDe(f) {
  if (f?.status !== 'fechado') return null
  const t = String(f.texto ?? '').trim()
  if (!t) return { vazio: true }
  if (/^excluir\.?$/i.test(t)) return { suprimido: true }
  return { texto: t }
}

// finals: Map<dispositivoId, {status, texto}> (ids já DEcodificados, com '/').
export function aplicarFinais(art, finals) {
  if (!finals || finals.size === 0) return art
  let out = art
  const cap = textoFinalDe(finals.get(`${art.editId}#caput`))
  if (cap?.texto) out = { ...out, caput: cap.texto, temFinal: true }
  else if (cap?.suprimido) out = { ...out, caput: SUPRIMIDO, incisos: [], temFinal: true, suprimido: true }
  else if (cap?.vazio) out = { ...out, conferido: true }
  let mudou = false
  const incisos = out.incisos.map(inc => {
    const f = textoFinalDe(finals.get(`${art.editId}#${inc.index}`))
    if (f?.texto) { mudou = true; return { ...inc, text: f.texto } }
    if (f?.suprimido) { mudou = true; return { ...inc, text: SUPRIMIDO, ownMarker: true } }
    return inc
  })
  if (mudou) out = { ...out, incisos, temFinal: true }
  return out
}

// Map<editId, { numero, capitulo, tema, id, caput, incisos: Map<indexOriginal, {roman, text}> }>
// na numeração CONTÍNUA do recorte (a que o participante vê).
export function indexarRecorte(recorte) {
  const indice = new Map()
  let n = 0
  for (const cap of recorte?.chapters ?? []) {
    for (const leaf of cap.articles ?? []) {
      n += 1
      const art = articular(leaf)
      const incisos = new Map()
      art.incisos.forEach((inc, pos) => incisos.set(inc.index, { roman: inc.ownMarker ? null : romanize(pos + 1), text: inc.text }))
      indice.set(leaf.editId, { numero: n, capitulo: cap.chapterTitle, tema: temaDoCapitulo(cap.id), id: leaf.id, caput: art.caput, incisos })
    }
  }
  return indice
}

export function localizar(indice, dispositivoId) {
  const { editId, parte } = parseDispositivoId(String(dispositivoId ?? ''))
  const art = indice.get(editId)
  if (!art) return { noRecorte: false, rotulo: '(dispositivo fora do recorte em consulta)', editId, parte, texto: '' }
  if (parte === 'caput') return { noRecorte: true, art, rotulo: `${articleLabel(art.numero)}, caput`, editId, parte, texto: art.caput }
  const inc = art.incisos.get(parte)
  if (!inc) return { noRecorte: true, art, rotulo: `${articleLabel(art.numero)}, item ${parte} (não localizado)`, editId, parte, texto: '' }
  return {
    noRecorte: true, art, editId, parte, texto: inc.text,
    rotulo: inc.roman ? `${articleLabel(art.numero)}, inciso ${inc.roman}` : `${articleLabel(art.numero)}, parágrafo`,
  }
}

// Firestore Timestamp (toDate), ISO string, Date ou null → Date|null.
export function paraData(v) {
  if (!v) return null
  if (v instanceof Date) return v
  if (typeof v.toDate === 'function') return v.toDate()
  const d = new Date(v)
  return Number.isNaN(d.getTime()) ? null : d
}

export function formatarDataHora(v) {
  const d = paraData(v)
  return d ? d.toLocaleString('pt-BR', { timeZone: 'America/Porto_Velho', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : ''
}

export function rotuloAlcance(m) {
  if (!m) return '(não cadastrado)'
  return m.escopo === 'servico' ? 'Só Regulamento de Serviço' : 'Portal completo'
}

// Autor de uma sugestão a partir do cadastro (por uid; fallback por nome). E-mail fica de
// fora de propósito: os documentos vão ao SEI.
export function autorDe(s, membros) {
  const m = (membros ?? []).find(x => x.uid && x.uid === s.autorUid)
    ?? (membros ?? []).find(x => String(x.nome ?? '').trim().toLowerCase() === String(s.autorNome ?? '').trim().toLowerCase())
    ?? null
  return {
    nome: m?.nome ?? s.autorNome ?? '(sem nome)',
    nomeGuerra: m?.nomeGuerra ?? '',
    unidade: m ? [m.unidade, m.comando, m.cidade].filter(Boolean).join(' — ') : '',
    alcance: rotuloAlcance(m),
    role: m?.role ?? '',
    consultado: m?.escopo === 'servico',
  }
}

const ordemParte = (p) => (p === 'caput' ? -1 : Number(p))

// Sugestões do Regulamento (cenário atual) que caem no recorte, com autor, localização e
// texto final, ordenadas por artigo → caput → incisos → data. `desde` (Date) é opcional.
// `somenteConsultados` (padrão true, determinação do Ten. Tiago em 2026-09-14): o relatório
// para o SEI traz só as manifestações dos militares consultados (escopo "servico"); os
// registros internos da equipe de curadoria (Tiago/Wândrio, contas sem escopo) ficam de fora.
export function selecionarInteracoes({ sugestoes, membros, indice, finals, desde = null, somenteConsultados = true }) {
  const out = []
  for (const s of sugestoes ?? []) {
    if (!String(s.dispositivoId ?? '').startsWith('reg:atual:')) continue
    const loc = localizar(indice, s.dispositivoId)
    if (!loc.noRecorte) continue
    const data = paraData(s.criadoEm)
    if (desde && (!data || data < desde)) continue
    const autor = autorDe(s, membros)
    if (somenteConsultados && !autor.consultado) continue
    const fin = textoFinalDe(finals?.get(s.dispositivoId))
    out.push({
      firestoreId: s.id,
      data,
      autor,
      dispositivo: loc.rotulo,
      dispositivoId: s.dispositivoId,
      numeroArtigo: loc.art.numero,
      parte: loc.parte,
      capitulo: loc.art.capitulo,
      tema: loc.art.tema,
      idFonte: loc.art.id,
      caputArtigo: loc.art.caput,
      rotuloNaEpoca: s.dispositivoLabelSnapshot ?? '',
      trecho: loc.texto || s.trechoSnapshot || '',
      sugestao: s.texto ?? '',
      curtidas: (s.curtidoPor ?? []).length,
      parecer: s.adminStatus ?? 'pendente',      // 'pendente' | 'relevante' | 'descartada'
      textoFinal: fin?.texto ?? null,
      finalVazio: Boolean(fin?.vazio),
      suprimido: Boolean(fin?.suprimido),
    })
  }
  out.sort((a, b) => (a.numeroArtigo - b.numeroArtigo)
    || (ordemParte(a.parte) - ordemParte(b.parte))
    || ((a.data?.getTime() ?? 0) - (b.data?.getTime() ?? 0)))
  return out.map((r, i) => ({ ...r, n: i + 1 }))
}

export function resumoParticipacao(membros, interacoes) {
  const consultados = (membros ?? []).filter(m => m.escopo === 'servico')
  const porAutor = new Map()
  for (const r of interacoes) {
    const e = porAutor.get(r.autor.nome) ?? { autor: r.autor, qtd: 0 }
    e.qtd += 1
    porAutor.set(r.autor.nome, e)
  }
  const porCapitulo = new Map()
  for (const r of interacoes) porCapitulo.set(r.capitulo, (porCapitulo.get(r.capitulo) ?? 0) + 1)
  const contribuintes = consultados.filter(m => [...porAutor.values()].some(e => e.autor.nome === m.nome))
  return {
    cadastradosEscopo: consultados.length,
    contribuintes: contribuintes.length,
    total: interacoes.length,
    dosConsultados: interacoes.filter(r => r.autor.consultado).length,
    daEquipe: interacoes.filter(r => !r.autor.consultado).length,
    porAutor: [...porAutor.values()].sort((a, b) => b.qtd - a.qtd),
    porCapitulo: [...porCapitulo.entries()].map(([capitulo, qtd]) => ({ capitulo, qtd })),
    pareceres: {
      relevante: interacoes.filter(r => r.parecer === 'relevante').length,
      descartada: interacoes.filter(r => r.parecer === 'descartada').length,
      pendente: interacoes.filter(r => r.parecer !== 'relevante' && r.parecer !== 'descartada').length,
    },
  }
}

export const ROTULO_PARECER = { relevante: 'Acolhida (relevante)', descartada: 'Descartada', pendente: 'Sem parecer' }

// Quadro de análise: um bloco por artigo do recorte que recebeu sugestão, com as sugestões,
// o parecer de cada uma e a situação do texto final do dispositivo.
export function quadroAnalise(interacoes) {
  const porArtigo = new Map()
  for (const r of interacoes) {
    const e = porArtigo.get(r.numeroArtigo) ?? {
      numeroArtigo: r.numeroArtigo, rotulo: articleLabel(r.numeroArtigo), capitulo: r.capitulo,
      idFonte: r.idFonte, caput: r.caputArtigo, itens: [],
    }
    e.itens.push(r)
    porArtigo.set(r.numeroArtigo, e)
  }
  return [...porArtigo.values()].sort((a, b) => a.numeroArtigo - b.numeroArtigo).map(e => ({
    ...e,
    situacaoFinal: e.itens.some(i => i.suprimido) ? 'suprimido'
      : e.itens.some(i => i.textoFinal) ? 'redigido'
        : e.itens.some(i => i.finalVazio) ? 'conferido' : 'aberto',
  }))
}

export const ROTULO_SITUACAO = {
  suprimido: 'Dispositivo suprimido', redigido: 'Texto final redigido',
  conferido: 'Conferido, sem alteração', aberto: 'Em aberto',
}

// Map<dispositivoId decodificado, doc> a partir da lista/Map de finalTexts. Aceita o Map
// que o app já monta (subscribeFinalTexts, ids decodificados) ou a lista exportada em JSON
// (ids com '|').
export function mapaFinais(fonte) {
  if (!fonte) return new Map()
  if (fonte instanceof Map) return fonte
  const map = new Map()
  for (const d of fonte) map.set(String(d.id).replaceAll('|', '/'), d)
  return map
}
