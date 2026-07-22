// Árvore do DOCUMENTO do Regulamento (Regulamento → 2 Partes → temas) no formato de nó
// que MinutaOrgChart consome ({ sigla, label, chapterId, synthetic, children }).
// O Regulamento é temático — não há cadeia de comando; esta árvore mostra a estrutura
// do documento (spec 2026-07-21-regulamento-diagramas-design.md).
import { PARTE_HEADERS } from './regulamentoPartes.js'

const OUTROS = 'Outros' // defensivo: capítulo sem `parte` reconhecida (hoje não ocorre)

export function buildRegulamentoTree(chapters) {
  const ordem = [...Object.keys(PARTE_HEADERS), OUTROS]
  const porParte = new Map()
  for (const ch of chapters ?? []) {
    const key = PARTE_HEADERS[ch.parte] ? ch.parte : OUTROS
    if (!porParte.has(key)) porParte.set(key, [])
    porParte.get(key).push({
      sigla: `${(ch.articles ?? []).length} art.`,
      label: ch.chapterTitle,
      chapterId: ch.id,
      children: [],
    })
  }
  return {
    synthetic: true,
    sigla: '',
    label: 'Regulamento Geral do CBMRO',
    chapterId: null,
    children: ordem
      .filter(key => porParte.has(key))
      .map(key => ({
        synthetic: true,
        sigla: '',
        label: PARTE_HEADERS[key] ?? OUTROS,
        chapterId: null,
        children: porParte.get(key),
      })),
  }
}
