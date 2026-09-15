// Formatação de texto para a minuta PUBLICÁVEL (pedido de 2026-09-15): primeira letra de
// cada frase em maiúscula. Lógica pura, sem React/docx.
//
// O portal exibe incisos em minúscula ("I - realizar…", normalizeInciso) — estilo de leitura
// do comparador. Para publicação a determinação é capitalizar o início de cada frase,
// inclusive incisos, alíneas e parágrafos, e após ponto final dentro do texto.

// Abreviaturas cujo ponto NÃO encerra frase (comparação sem acento, minúscula).
const ABREVIATURAS = new Set([
  'art', 'arts', 'inc', 'incs', 'n', 'no', 'num', 'cf', 'red', 'cmt', 'sgt', 'cel', 'ten', 'cap',
  'maj', 'asp', 'sd', 'cb', 'st', 'dr', 'dra', 'ex', 'obs', 'par', 'pag', 'p', 'pp', 'al', 'fl', 'fls',
  'tel', 'etc', 'ltda', 'sr', 'sra', 'srs', 'prof', 'gen', 'adm', 'depto', 'ed', 'ref', 'vol', 'sec',
])
const semAcento = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '')

// Maiúscula na primeira letra do texto (pulando marcadores como "§ 1º ", "a) ", "I - ") e
// após ponto/exclamação/interrogação seguido de espaço — exceto após abreviatura, número ou
// token de um só caractere (enumerações inline como "a. qual foi o fato").
export function capitalizarFrases(texto) {
  let t = String(texto ?? '')
  if (!t.trim()) return t
  // pula o marcador inicial (se houver) e capitaliza a 1ª letra que vier logo depois
  const marcador = t.match(/^\s*(?:§\s*\d+[ºo°.]?\s*|[a-z]\)\s*|[ivxlcdm]+\s*[-–.)]\s*|\d+[.)]\s*)/i)
  const inicio = marcador ? marcador[0].length : (t.length - t.trimStart().length)
  t = t.slice(0, inicio) + t.slice(inicio).replace(/^(\p{Ll})/u, ch => ch.toUpperCase())
  t = t.replace(/(\S+)([.!?])(\s+)(\p{Ll})/gu, (m, palavra, pont, esp, ch) => {
    const nucleo = semAcento(palavra.replace(/^[("'“‘]+/, '')).toLowerCase()
    if (pont === '.' && (ABREVIATURAS.has(nucleo) || nucleo.length <= 1 || /^\d{1,2}$/.test(nucleo))) return m
    return `${palavra}${pont}${esp}${ch.toUpperCase()}`
  })
  return t
}
