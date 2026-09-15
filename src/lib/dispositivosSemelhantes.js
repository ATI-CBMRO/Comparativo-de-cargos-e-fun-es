// Análise de DISPOSITIVOS COM TEXTO SEMELHANTE na minuta (pedido de 2026-09-15): compara
// caput, incisos, parágrafos e alíneas de todos os artigos e agrupa os parecidos para
// deliberação (qual permanece, qual é suprimido, ou se ficam os dois). Lógica pura.
//
// Medida: similaridade de Jaccard sobre o conjunto de palavras significativas (≥ 3 letras,
// sem acento, minúsculas, sem marcadores e pontuação). Unidades curtas (< MIN_TOKENS
// palavras — "Diretor", "Adjunto", "Seção Administrativa") são ignoradas: repetem-se por
// natureza nas listas de estrutura. Grupos formados por união (A~B, B~C → {A,B,C}).
import { articleLabel, romanize } from './minutaArticles.js'

export const LIMIAR = 0.6
export const MIN_TOKENS = 6

const STOP = new Set(['que', 'com', 'para', 'por', 'dos', 'das', 'nos', 'nas', 'aos', 'uma', 'seu', 'sua',
  'seus', 'suas', 'nao', 'como', 'mais', 'ser', 'sem', 'sob', 'entre', 'este', 'esta', 'esse', 'essa',
  'pelo', 'pela', 'pelos', 'pelas', 'lhe', 'lhes', 'ainda', 'quando', 'onde', 'bem', 'ate'])

export function tokens(texto) {
  return String(texto ?? '')
    .normalize('NFD').replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/^\s*(§\s*\d+[ºo°.]?|paragrafo unico\.?|[a-z]\)|[ivxlcdm]+\s*[-–.)]|\d+[.)])\s*/i, '')
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length >= 3 && !STOP.has(w))
}

export function jaccard(a, b) {
  const A = new Set(a)
  const B = new Set(b)
  if (!A.size || !B.size) return 0
  let inter = 0
  for (const w of A) if (B.has(w)) inter += 1
  return inter / (A.size + B.size - inter)
}

// Unidades de um bloco de artigo montado (montarReestruturada → blocos[].art): caput + cada
// inciso/parágrafo/alínea, com rótulo legível.
export function unidadesDoArtigo(numero, art, capitulo = '') {
  const rotulo = articleLabel(numero)
  const out = [{ artigo: numero, rotulo: `${rotulo}, caput`, texto: art.caput, capitulo, caputArtigo: art.caput }]
  let romano = 0
  art.incisos.forEach((inc) => {
    let parte
    if (inc.alinea) parte = `alínea ${inc.text.trim().slice(0, 2)}`
    else if (inc.ownMarker) parte = inc.text.trim().split(/\s+/).slice(0, 2).join(' ').replace(/\.$/, '')
    else { romano += 1; parte = `inciso ${romanize(romano)}` }
    out.push({ artigo: numero, rotulo: `${rotulo}, ${parte}`, texto: inc.text, capitulo, caputArtigo: art.caput })
  })
  return out
}

// Incisos de artigos "Compete ao X:" com sujeitos DIFERENTES (ex.: Comandante de Grupamento ×
// Comandante de Subgrupamento) repetem-se por desenho: a mesma atribuição em cada escalão.
function competenciasParalelas(itens) {
  if (itens.some(u => /caput$/.test(u.rotulo))) return false
  const caputs = new Set(itens.map(u => String(u.caputArtigo ?? '').trim()))
  return caputs.size > 1 && [...caputs].every(c => /^compete\b/i.test(c))
}
const sujeitoDe = (caput) => String(caput).replace(/^compete\s+(ao?|à|aos|às)\s+/i, '').replace(/[:.]\s*$/, '')

// unidades: [{artigo, rotulo, texto, capitulo}] → grupos [{itens, similaridade, identicos, recomendacao}]
// `incluirParalelas` (padrao false, determinacao de 2026-09-15): competencias paralelas de
// funcoes distintas repetem-se por desenho e ficam FORA do quadro; contam em `descartados`.
export function agruparSemelhantes(unidades, { limiar = LIMIAR, minTokens = MIN_TOKENS, incluirParalelas = false } = {}) {
  const us = unidades.map((u, i) => ({ ...u, i, toks: tokens(u.texto) })).filter(u => u.toks.length >= minTokens)
  const pai = new Map(us.map(u => [u.i, u.i]))
  const find = (x) => { while (pai.get(x) !== x) { pai.set(x, pai.get(pai.get(x))); x = pai.get(x) } return x }
  const pares = []
  for (let a = 0; a < us.length; a += 1) {
    for (let b = a + 1; b < us.length; b += 1) {
      const s = jaccard(us[a].toks, us[b].toks)
      if (s >= limiar) {
        pares.push([us[a].i, us[b].i, s])
        pai.set(find(us[a].i), find(us[b].i))
      }
    }
  }
  const emPar = new Set(pares.flatMap(([x, y]) => [x, y]))
  const grupos = new Map()
  for (const u of us) {
    if (!emPar.has(u.i)) continue
    const r = find(u.i)
    if (!grupos.has(r)) grupos.set(r, [])
    grupos.get(r).push(u)
  }
  const out = []
  for (const itens of grupos.values()) {
    const ids = new Set(itens.map(u => u.i))
    const sims = pares.filter(([x, y]) => ids.has(x) && ids.has(y)).map(p => p[2])
    const similaridade = Math.max(...sims)
    const norm = itens.map(u => u.toks.join(' '))
    const identicos = new Set(norm).size < norm.length
    const mesmoArtigo = new Set(itens.map(u => u.artigo)).size === 1
    const paralelas = competenciasParalelas(itens)
    let recomendacao
    if (paralelas) {
      const sujeitos = [...new Set(itens.map(u => sujeitoDe(u.caputArtigo)))].join(' × ')
      recomendacao = `Competências paralelas de funções distintas (${sujeitos}) — em regra mantêm-se as duas, uma em cada escalão; suprimir só se a atribuição couber a uma única função.`
    } else if (identicos) recomendacao = mesmoArtigo ? 'Texto repetido dentro do mesmo artigo — suprimir a repetição.' : 'Texto idêntico em artigos distintos — manter um e suprimir o outro.'
    else if (similaridade >= 0.8) recomendacao = 'Quase idênticos — fundir num só dispositivo ou manter apenas um.'
    else recomendacao = 'Semelhantes — avaliar se tratam da mesma matéria (fundir) ou de hipóteses distintas (manter ambos).'
    itens.sort((a, b) => a.artigo - b.artigo || a.i - b.i)
    out.push({ itens: itens.map(({ i, toks, ...u }) => u), similaridade, identicos, mesmoArtigo, paralelas, recomendacao })
  }
  out.sort((a, b) => (Number(b.identicos) - Number(a.identicos)) || (b.similaridade - a.similaridade) || (a.itens[0].artigo - b.itens[0].artigo))
  const paralelosDescartados = out.filter(g => g.paralelas).length
  const resultado = incluirParalelas ? out : out.filter(g => !g.paralelas)
  resultado.paralelosDescartados = paralelosDescartados
  return resultado
}

// Atalho: a partir dos blocos de montarReestruturada().
export function semelhantesDaMinuta(blocos, opts) {
  const unidades = []
  let capitulo = ''
  for (const b of blocos) {
    if (b.tipo === 'capitulo') capitulo = `${b.rotulo} — ${b.texto}`
    if (b.tipo === 'artigo') unidades.push(...unidadesDoArtigo(b.numero, b.art, capitulo))
  }
  const grupos = agruparSemelhantes(unidades, opts)
  return { grupos, unidades: unidades.length, paralelosDescartados: grupos.paralelosDescartados }
}

export const rotuloSimilaridade = (s) => `${Math.round(s * 100)}%`
