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
  else if (index === total - 2 && total > 2) suffix = '; e'
  return t + suffix
}

export function buildArticles(organData, edits = {}) {
  const articles = []
  let articleCounter = 0
  let chapterCounter = 0

  for (const section of organData.sections) {
    const text = edits[section.id] ?? section.proposedText ?? ''
    const lines = text.split('\n')
    let firstOfSection = true

    const push = (caput, incisos) => {
      articleCounter += 1
      let chapterTitle = null
      let chapterNumber = null
      if (firstOfSection && section.chapterTitle) {
        chapterCounter += 1
        chapterTitle = section.chapterTitle
        chapterNumber = chapterCounter
      }
      firstOfSection = false
      articles.push({ number: articleCounter, chapterNumber, chapterTitle, caput, incisos })
    }

    if (section.kind === 'prose') {
      for (const line of lines) {
        const c = line.trim()
        if (c) push(c, [])
      }
    } else if (section.kind === 'incisos') {
      const raw = lines.map(l => l.trim()).filter(Boolean)
      const incisos = raw.map((t, i) => normalizeInciso(t, i, raw.length))
      push(section.caput ?? '', incisos)
    } else if (section.kind === 'cargos') {
      let current = null
      const flush = () => {
        if (current) {
          const incisos = current.raw.map((t, i) => normalizeInciso(t, i, current.raw.length))
          push(current.caput, incisos)
          current = null
        }
      }
      for (const line of lines) {
        const c = line.trim()
        if (!c) continue
        if (c.endsWith(':')) {
          flush()
          current = { caput: `Ao ${c.slice(0, -1).trim()} compete:`, raw: [] }
        } else if (current) {
          current.raw.push(c)
        }
      }
      flush()
    }
  }

  return articles
}
