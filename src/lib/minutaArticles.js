// Lógica pura de articulação da minuta de regimento (sem React, sem docx).

export function articleLabel(n) {
  return n <= 9 ? `Art. ${n}º` : `Art. ${n}`
}

const ROMAN_MAP = [
  [1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
  [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'],
  [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I'],
]

export function romanize(n) {
  let out = ''
  let val = n
  for (const [v, sym] of ROMAN_MAP) {
    while (val >= v) { out += sym; val -= v }
  }
  return out
}

// Remove marcador de lista inicial ("1.", "1)", "I -", "- ", "a)") e pontuação
// final, minúscula a 1ª letra e aplica o sufixo conforme a posição no rol.
export function normalizeInciso(text, index, total) {
  let t = (text ?? '').trim()
  t = t.replace(/^(\d+[.)]|[ivxlcdm]+\s*[-–.)]|[a-z][).]|[-–•])\s*/i, '')
  t = t.replace(/[;.]\s*$/, '')
  if (t) t = t[0].toLowerCase() + t.slice(1)
  let suffix = ';'
  if (index === total - 1) suffix = '.'
  else if (index === total - 2) suffix = '; e'
  return t + suffix
}

// Articula a estrutura hierárquica: chapters[] (prose | incisos | organ).
// Numeração de artigos contínua; capítulos e seções em romano (seção reseta por capítulo).
// edits[editId] (string) sobrepõe o texto de um nó-folha; ao editar, a fonte vira null.
export function buildArticles(structure, edits = {}) {
  const articles = []
  let articleCounter = 0
  let chapterCounter = 0

  for (const chapter of structure.chapters) {
    let firstOfChapter = true
    let sectionCounter = 0

    const emitLeaf = (leaf, isSection) => {
      let firstOfSection = true

      const pushArticle = (caput, incisos) => {
        articleCounter += 1
        const art = {
          number: articleCounter, caput, incisos,
          chapterNumber: null, chapterTitle: null,
          sectionNumber: null, sectionTitle: null,
        }
        if (firstOfChapter) {
          chapterCounter += 1
          art.chapterNumber = chapterCounter
          art.chapterTitle = chapter.chapterTitle ?? null
          firstOfChapter = false
        }
        if (isSection && firstOfSection) {
          sectionCounter += 1
          art.sectionNumber = sectionCounter
          art.sectionTitle = leaf.sectionTitle ?? null
          firstOfSection = false
        }
        articles.push(art)
      }

      if (leaf.kind === 'prose') {
        const text = edits[leaf.editId] ?? leaf.proposedText ?? ''
        for (const line of text.split('\n')) {
          const c = line.trim()
          if (c) pushArticle(c, [])
        }
      } else if (leaf.kind === 'incisos') {
        const edited = edits[leaf.editId]
        let items
        if (edited != null) {
          items = edited.split('\n').map(l => l.trim()).filter(Boolean)
            .map(t => ({ text: t, source: null }))
        } else {
          items = (leaf.items ?? []).filter(it => (it.text ?? '').trim())
        }
        const incisos = items.map((it, i) => ({
          text: normalizeInciso(it.text, i, items.length),
          source: it.source ?? null,
        }))
        if (incisos.length || !isSection) {
          pushArticle(leaf.caput ?? '', incisos)
        }
      }
    }

    if (chapter.kind === 'organ') {
      for (const section of chapter.sections) emitLeaf(section, true)
    } else {
      emitLeaf(chapter, false)
    }
  }

  return articles
}
