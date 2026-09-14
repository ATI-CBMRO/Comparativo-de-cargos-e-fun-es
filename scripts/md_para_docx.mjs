// Converte um Markdown simples (títulos #/##/###, parágrafos, listas "- ", tabelas "| a | b |",
// negrito **x**) em .docx com o cabeçalho institucional do CBMRO — para os relatórios de
// análise que vão ao SEI.
//
//   node scripts/md_para_docx.mjs entrada.md saida.docx "Subtítulo do cabeçalho"
import fs from 'node:fs'
import { Paragraph, TextRun, AlignmentType } from 'docx'
import { cabecalhoInstitucional, pCentro, salvarDocx, tabela } from './lib_docx_minuta.mjs'

const [entrada, saida, subtitulo = ''] = process.argv.slice(2)
if (!entrada || !saida) { console.error('uso: md_para_docx.mjs entrada.md saida.docx [subtitulo]'); process.exit(2) }

const FONT = 'Times New Roman'
function runs(texto, { size = 22, italics = false } = {}) {
  // **negrito** e `código` (código vira itálico)
  const out = []
  const re = /(\*\*[^*]+\*\*|`[^`]+`)/g
  let last = 0
  for (const m of texto.matchAll(re)) {
    if (m.index > last) out.push(new TextRun({ text: texto.slice(last, m.index), font: FONT, size, italics }))
    const t = m[0]
    if (t.startsWith('**')) out.push(new TextRun({ text: t.slice(2, -2), font: FONT, size, bold: true, italics }))
    else out.push(new TextRun({ text: t.slice(1, -1), font: FONT, size, italics: true }))
    last = m.index + t.length
  }
  if (last < texto.length) out.push(new TextRun({ text: texto.slice(last), font: FONT, size, italics }))
  return out
}

const linhas = fs.readFileSync(entrada, 'utf8').split(/\r?\n/)
const children = cabecalhoInstitucional(subtitulo || linhas.find(l => l.startsWith('# '))?.slice(2) || '')
let i = 0
let tituloPrincipalVisto = false
while (i < linhas.length) {
  const l = linhas[i]
  if (!l.trim()) { i += 1; continue }
  if (l.startsWith('# ')) {
    if (!tituloPrincipalVisto) { tituloPrincipalVisto = true; i += 1; continue } // já está no cabeçalho
    children.push(pCentro(l.slice(2), { size: 26, before: 240, after: 160 })); i += 1; continue
  }
  if (l.startsWith('## ')) {
    children.push(new Paragraph({ spacing: { before: 280, after: 120 }, children: [new TextRun({ text: l.slice(3), font: FONT, size: 24, bold: true })] })); i += 1; continue
  }
  if (l.startsWith('### ')) {
    children.push(new Paragraph({ spacing: { before: 200, after: 80 }, children: [new TextRun({ text: l.slice(4), font: FONT, size: 22, bold: true, italics: true })] })); i += 1; continue
  }
  if (l.startsWith('|')) {
    const rows = []
    while (i < linhas.length && linhas[i].startsWith('|')) {
      const cells = linhas[i].slice(1, -1).split('|').map(c => c.trim())
      if (!cells.every(c => /^:?-{2,}:?$/.test(c))) rows.push(cells)
      i += 1
    }
    const ncol = Math.max(...rows.map(r => r.length))
    const larguras = Array.from({ length: ncol }, () => Math.floor(9300 / ncol))
    children.push(tabela(rows.map(r => { while (r.length < ncol) r.push(''); return r.map(c => c.replace(/\*\*/g, '').replace(/`/g, '')) }), larguras))
    children.push(new Paragraph({ spacing: { after: 120 }, children: [] }))
    continue
  }
  if (/^\s*[-*] /.test(l)) {
    const nivel = Math.floor((l.match(/^\s*/)[0].length) / 2)
    children.push(new Paragraph({
      alignment: AlignmentType.JUSTIFIED, spacing: { after: 60, line: 300 },
      indent: { left: 360 + nivel * 360, hanging: 240 },
      children: [new TextRun({ text: '• ', font: FONT, size: 22 }), ...runs(l.replace(/^\s*[-*] /, ''))],
    })); i += 1; continue
  }
  if (/^\d+\. /.test(l)) {
    children.push(new Paragraph({
      alignment: AlignmentType.JUSTIFIED, spacing: { after: 60, line: 300 }, indent: { left: 360, hanging: 300 },
      children: runs(l),
    })); i += 1; continue
  }
  if (l.startsWith('> ')) {
    children.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 100, line: 300 }, indent: { left: 708 }, children: runs(l.slice(2), { italics: true }) })); i += 1; continue
  }
  // parágrafo (junta linhas consecutivas)
  let par = l
  while (i + 1 < linhas.length && linhas[i + 1].trim() && !/^(#|\||\s*[-*] |\d+\. |> )/.test(linhas[i + 1])) { i += 1; par += ' ' + linhas[i].trim() }
  children.push(new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 300 }, children: runs(par) }))
  i += 1
}
await salvarDocx(children, saida, `${subtitulo || 'Relatório'} · CBMRO`)
console.log('OK:', saida)
