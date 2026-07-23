import { buildArticles } from './minutaArticles.js'
import { chapterIdOf } from './minutaTargets.js'

// Normaliza o marcador de cenário para casar dispositivo (editId) com capítulo (id).
const semCenario = (id) => String(id ?? '').replace(/^reg:atual:/, 'reg:').replace(/^atual:/, '')

// Lista linear de conferência: cada dispositivo da minuta (numeração contínua) com as
// alternativas (referências de outros estados) do seu capítulo/órgão anexadas.
export function buildConferencia(structure) {
  if (!structure?.chapters) return []
  const altPorCap = new Map(
    structure.chapters.map(c => [semCenario(c.id), c.alternatives ?? {}]),
  )
  return buildArticles(structure).map(dispositivo => {
    const chapterId = chapterIdOf(dispositivo.editId)
    const cap = structure.chapters.find(c => semCenario(c.id) === semCenario(chapterId))
    return {
      dispositivo,
      chapterId,
      chapterTitle: cap?.chapterTitle ?? null,
      alternatives: altPorCap.get(semCenario(chapterId)) ?? {},
    }
  })
}
