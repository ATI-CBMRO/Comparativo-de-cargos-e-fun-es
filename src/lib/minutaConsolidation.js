// A partir das RESOLUÇÕES aprovadas na deliberação (texto final por item), produz
// `edits` (editId -> incisos por linha) para gerar a minuta consolidada. Esta é a
// fonte de verdade da Fase 2: o texto final é o que o relator aprovou (partindo da
// sugestão aceita e possivelmente editado à mão). finalText vazio = inciso removido.

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

export function applyResolutionsToEdits(structure, resolutions) {
  const raw = indexRawItems(structure)
  const byEdit = {}
  for (const [key, res] of Object.entries(resolutions || {})) {
    if (!res || res.status !== 'decidido') continue
    const hash = key.indexOf('#')
    if (hash === -1) continue // resolução de seção/prose: fora do protótipo
    const editId = key.slice(0, hash)
    const idx = Number(key.slice(hash + 1))
    if (!Number.isInteger(idx)) continue
    ;(byEdit[editId] ||= {})[idx] = res.finalText ?? ''
  }
  const edits = {}
  for (const [editId, finals] of Object.entries(byEdit)) {
    const base = raw[editId]
    if (!base) continue
    const out = []
    base.forEach((text, index) => {
      if (index in finals) {
        const ft = (finals[index] ?? '').trim()
        if (ft) out.push(ft) // finalText vazio => remove o inciso
      } else {
        out.push(text)
      }
    })
    edits[editId] = out.join('\n')
  }
  return edits
}
