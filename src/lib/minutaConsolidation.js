// A partir das sugestões ACEITAS, produz `edits` (editId -> texto multilinha de
// incisos crus) para alimentar buildArticles e gerar a minuta consolidada.
// Aplica, por seção: remover (descarta o inciso), editar (troca o texto) e incluir
// (anexa novo inciso ao fim). Seções totalmente novas (incluir-secao) ficam fora do
// protótipo de geração (registradas como sugestão, não inseridas no .docx).

// Indexa os textos CRUS (não normalizados) de cada folha "incisos" da estrutura.
function indexRawItems(structure) {
  const idx = {}
  const addLeaf = leaf => {
    if (leaf && leaf.kind === 'incisos') idx[leaf.editId] = (leaf.items ?? []).map(it => it.text ?? '')
  }
  for (const ch of structure.chapters) {
    if (ch.kind === 'organ') (ch.sections ?? []).forEach(addLeaf)
    else if (ch.kind === 'articles') (ch.articles ?? []).forEach(addLeaf)
  }
  return idx
}

export function applyDecisionsToEdits(structure, suggestions) {
  const raw = indexRawItems(structure)
  const byEdit = {}
  for (const s of suggestions) {
    if (s.status !== 'aceita') continue
    ;(byEdit[s.targetId] ||= []).push(s)
  }

  const edits = {}
  for (const [editId, list] of Object.entries(byEdit)) {
    const base = raw[editId]
    if (!base) continue // sem incisos crus (prose ou seção nova) — fora do protótipo
    const items = base.map((text, index) => ({ text, index, removed: false }))
    const appended = []
    for (const s of list) {
      if (s.type === 'remover' && s.incisoIndex != null) {
        const t = items.find(i => i.index === s.incisoIndex)
        if (t) t.removed = true
      } else if (s.type === 'editar' && s.incisoIndex != null) {
        const t = items.find(i => i.index === s.incisoIndex)
        if (t && (s.proposedText ?? '').trim()) t.text = s.proposedText.trim()
      } else if (s.type === 'incluir' && (s.proposedText ?? '').trim()) {
        appended.push(s.proposedText.trim())
      }
    }
    const finalTexts = items.filter(i => !i.removed).map(i => i.text).concat(appended)
    edits[editId] = finalTexts.join('\n')
  }
  return edits
}
