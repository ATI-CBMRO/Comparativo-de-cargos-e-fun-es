// Deriva, do minuta_structure.json articulado, a lista de capítulos com seus
// artigos/incisos endereçáveis para a UI de revisão. Reusa buildArticles para
// herdar numeração e normalização — não reimplementa nada disso.
import { buildArticles } from './minutaArticles.js'

// chapterId = prefixo do editId antes da primeira "/" (ex.: "organ:cg/competencia"
// -> "organ:cg"; "estrutura/direcao" -> "estrutura"; "preliminares" -> "preliminares").
export function chapterIdOf(editId) {
  return String(editId).split('/')[0]
}

// Chave única de um "item" deliberável: inciso = "<editId>#<index>"; seção/prose = editId.
export function itemKeyOf(editId, incisoIndex) {
  return incisoIndex == null ? editId : `${editId}#${incisoIndex}`
}

// -> [{ chapterId, chapterTitle, chapterNumber,
//        articles: [{ editId, number, caput, sectionTitle, sectionNumber,
//                     incisos: [{ index, text, source }] }] }]
export function buildTargets(structure) {
  const arts = buildArticles(structure)
  const chapters = []
  let current = null
  for (const a of arts) {
    if (a.chapterNumber) {
      current = {
        chapterId: chapterIdOf(a.editId),
        chapterTitle: a.chapterTitle,
        chapterNumber: a.chapterNumber,
        articles: [],
      }
      chapters.push(current)
    }
    current.articles.push({
      editId: a.editId,
      number: a.number,
      caput: a.caput,
      sectionTitle: a.sectionTitle,
      sectionNumber: a.sectionNumber,
      incisos: a.incisos.map(inc => ({ index: inc.index, text: inc.text, source: inc.source })),
    })
  }
  return chapters
}
