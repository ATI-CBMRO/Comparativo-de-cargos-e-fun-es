// Aplica os textos finais (finalTexts, status 'fechado') sobre os artigos JÁ montados
// por buildArticles. Usada pelos Wizards (tela) e pelo minutaDocx (.docx) — a mesma
// função nos dois lugares garante que o documento baixado é o que se vê.
import { caputDispositivoId, incisoDispositivoId } from './dispositivoId.js'

// Artigos que a curadoria da consulta já fechou (versão atual/futura curada, 2026-09):
// `corrigido`, `alterado`, `substitui` ou `incluido`. Os textos finais do Firestore são
// anteriores a esse fechamento e foram incorporados (ou superados) por ele — aplicá-los por
// cima devolveria texto velho (achado de 16/09/2026: se-art-24/25/26/29 voltavam ao texto de
// agosto no wizard e no .docx do Regulamento Geral). Vale para qualquer estrutura curada.
export function editIdsFechadosPelaCuradoria(structure) {
  const out = new Set()
  for (const cap of structure?.chapters ?? []) {
    const folhas = cap.kind === 'organ' ? (cap.sections ?? []) : (cap.articles ?? [cap])
    for (const leaf of folhas) {
      if (leaf?.editId && (leaf.corrigido || leaf.alterado || leaf.substitui || leaf.incluido)) out.add(leaf.editId)
    }
  }
  return out
}

export function applyFinalsToArticles(articles, finalsMap, { skipEditIds = new Set() } = {}) {
  if (!finalsMap || finalsMap.size === 0) return { articles, appliedCount: 0 }
  const artigosPorEditId = new Map()
  for (const a of articles) {
    artigosPorEditId.set(a.editId, (artigosPorEditId.get(a.editId) ?? 0) + 1)
  }
  let appliedCount = 0
  const out = articles.map(a => {
    if (skipEditIds.has(a.editId)) return a
    let art = a
    const capFinal = finalsMap.get(caputDispositivoId(a.editId))
    if (capFinal?.status === 'fechado' && artigosPorEditId.get(a.editId) === 1) {
      art = { ...art, caput: capFinal.texto, hasFinal: true }
      appliedCount += 1
    }
    let mudouInciso = false
    const incisos = (art.incisos ?? []).map(inc => {
      // inc.reindexed: o índice é posicional novo (seção editada) e NÃO endereça
      // mais o inciso original — aplicar o final aqui acertaria o inciso errado
      // (auditoria 2026-07-23, classe do `[pw, pr] = data.pessoas` do MyFOP).
      if (inc.reindexed) return inc
      const f = finalsMap.get(incisoDispositivoId(a.editId, inc.index))
      if (f?.status === 'fechado') { mudouInciso = true; appliedCount += 1; return { ...inc, text: f.texto, source: null } }
      return inc
    })
    if (mudouInciso) art = { ...art, incisos, hasFinal: true }
    return art
  })
  return { articles: out, appliedCount }
}
