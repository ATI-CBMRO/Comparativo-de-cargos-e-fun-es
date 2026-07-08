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

// Dispositivos como "Parágrafo único." e "§ 1º" são unidades legislativas completas
// (não incisos numerados) — carregam o próprio marcador verbatim da fonte e nunca
// devem ganhar numeral romano artificial nem perder a maiúscula/pontuação original.
export function hasOwnMarker(text) {
  return /^\s*(§\s*\d|Par[áa]grafo\s+[úu]nico)/i.test(text ?? '')
}

// Remove marcador de lista inicial ("1.", "1)", "I -", "- ", "a)") e pontuação
// final, minúscula a 1ª letra e aplica o sufixo conforme a posição no rol.
// Dispositivos com marcador próprio (ver hasOwnMarker) são devolvidos como vieram —
// já são uma frase completa, não uma cláusula que continua o caput.
export function normalizeInciso(text, index, total) {
  let t = (text ?? '').trim()
  if (hasOwnMarker(t)) return t
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
// isExcluded(editId, index) remove incisos específicos (curadoria); a numeração ignora os removidos.
// Cada artigo carrega editId; cada inciso carrega { text, source, editId, index (original) }.
export function buildArticles(structure, edits = {}, isExcluded = () => false) {
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
          number: articleCounter, caput, incisos, editId: leaf.editId,
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
        let incisos
        if (edited != null) {
          const raw = edited.split('\n').map(l => l.trim()).filter(Boolean)
          incisos = raw.map((t, i) => ({
            text: normalizeInciso(t, i, raw.length),
            ownMarker: hasOwnMarker(t),
            source: null, editId: leaf.editId, index: i,
          }))
        } else {
          // preserva o índice ORIGINAL em leaf.items para a chave de exclusão
          const kept = []
          ;(leaf.items ?? []).forEach((it, i) => {
            if (!(it.text ?? '').trim()) return
            if (isExcluded(leaf.editId, i)) return
            kept.push({ it, i })
          })
          incisos = kept.map((k, pos) => ({
            text: normalizeInciso(k.it.text, pos, kept.length),
            ownMarker: hasOwnMarker(k.it.text),
            source: k.it.source ?? null, editId: leaf.editId, index: k.i,
          }))
        }
        if (incisos.length || !isSection) {
          pushArticle(leaf.caput ?? '', incisos)
        }
      }
    }

    if (chapter.kind === 'organ') {
      for (const section of chapter.sections) emitLeaf(section, true)
    } else if (chapter.kind === 'articles') {
      for (const leaf of chapter.articles) emitLeaf(leaf, false)
    } else {
      emitLeaf(chapter, false)
    }
  }

  return articles
}
