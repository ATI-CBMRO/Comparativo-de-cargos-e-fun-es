// Gera o Blob .docx da minuta a partir da estrutura articulada. Extraído de
// MinutaWizard para reuso pela Fase 2 (deliberação). Mantém a formatação original.
import {
  Document, Packer, Paragraph, TextRun, Footer, AlignmentType, ImageRun,
} from 'docx'
import { buildArticles, articleLabel, romanize } from './minutaArticles.js'
import { PARTE_HEADERS, parteByChapterTitle } from './regulamentoPartes.js'

export async function buildMinutaBlob({ structure, edits = {}, isExcluded = () => false, subtitle }) {
  const dateStr = new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })

  let imageData = null
  try {
    const resp = await fetch('/BrasaoCBMRO2D-COMPLETO.png')
    if (resp.ok) imageData = await resp.arrayBuffer()
  } catch (_) { /* segue sem imagem */ }

  const children = []
  if (imageData) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new ImageRun({ data: imageData, transformation: { width: 65, height: 65 }, type: 'png' })],
    }))
  }
  children.push(
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 120 },
      children: [new TextRun({ text: 'CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA', bold: true, size: 28, font: 'Times New Roman' })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: subtitle, size: 24, font: 'Times New Roman' })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 480 },
      children: [new TextRun({ text: dateStr, size: 22, font: 'Times New Roman', italics: true })],
    }),
  )

  const parteDe = parteByChapterTitle(structure)
  let ultimaParte = null
  const articles = buildArticles(structure, edits, isExcluded)
  let chapterSeen = false
  articles.forEach(art => {
    if (art.chapterTitle) {
      const parte = parteDe[art.chapterTitle]
      const novaParte = Boolean(parte) && parte !== ultimaParte
      if (novaParte) {
        children.push(new Paragraph({
          alignment: AlignmentType.CENTER, pageBreakBefore: chapterSeen,
          spacing: { before: 240, after: 240 },
          children: [new TextRun({ text: PARTE_HEADERS[parte], bold: true, font: 'Times New Roman', size: 30 })],
        }))
        ultimaParte = parte
      }
      children.push(
        new Paragraph({
          alignment: AlignmentType.CENTER, pageBreakBefore: chapterSeen && !novaParte,
          spacing: { before: 240, after: 0 },
          children: [new TextRun({ text: `CAPÍTULO ${romanize(art.chapterNumber)}`, bold: true, font: 'Times New Roman', size: 26 })],
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER, spacing: { after: 120 },
          children: [new TextRun({ text: art.chapterTitle, bold: true, font: 'Times New Roman', size: 26 })],
        }),
      )
      chapterSeen = true
    }
    if (art.sectionTitle) {
      children.push(new Paragraph({
        alignment: AlignmentType.CENTER, spacing: { before: 120, after: 80 },
        children: [new TextRun({ text: `Seção ${romanize(art.sectionNumber)} — ${art.sectionTitle}`, bold: true, italics: true, font: 'Times New Roman', size: 24 })],
      }))
    }
    children.push(new Paragraph({
      alignment: AlignmentType.JUSTIFIED,
      spacing: { line: 360, after: art.incisos.length ? 60 : 120 },
      indent: art.incisos.length ? undefined : { firstLine: 708 },
      children: [
        new TextRun({ text: `${articleLabel(art.number)} `, bold: true, font: 'Times New Roman', size: 24 }),
        new TextRun({ text: art.caput, font: 'Times New Roman', size: 24 }),
      ],
    }))
    art.incisos.forEach((inc, i) => {
      const runs = [new TextRun({ text: `${romanize(i + 1)} - ${inc.text}`, font: 'Times New Roman', size: 24 })]
      if (inc.source && inc.source !== 'ro') {
        runs.push(new TextRun({ text: ` (${inc.source})`, font: 'Times New Roman', size: 20, italics: true, color: '888888' }))
      }
      children.push(new Paragraph({
        alignment: AlignmentType.JUSTIFIED, spacing: { line: 360, after: 60 },
        indent: { left: 708, hanging: 340 }, children: runs,
      }))
    })
  })

  const doc = new Document({
    sections: [{
      properties: { page: { margin: { top: 1701, right: 1134, bottom: 1134, left: 1701 } } },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            children: [new TextRun({ text: `Documento gerado pelo Portal de Legislação CBM — CBMRO · ${dateStr}`, size: 18, font: 'Times New Roman', italics: true })],
          })],
        }),
      },
      children,
    }],
  })

  return await Packer.toBlob(doc)
}
