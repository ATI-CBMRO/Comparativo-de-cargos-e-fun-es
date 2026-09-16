// Gera o Blob .docx da minuta a partir da estrutura articulada. Extraído de
// MinutaWizard para reuso pela Fase 2 (deliberação). Mantém a formatação original.
import {
  Document, Packer, Paragraph, TextRun, Footer, AlignmentType, ImageRun,
} from 'docx'
import { buildArticles, articleLabel, romanize, rotuloRomano } from './minutaArticles.js'
import { PARTE_HEADERS, parteByChapterTitle } from './regulamentoPartes.js'
import { applyFinalsToArticles } from './minutaFinals.js'
import { RECUO_PRIMEIRA_LINHA, ESPACAMENTO, MARGENS } from './docxFormato.js'

export async function buildMinutaBlob({ structure, edits = {}, isExcluded = () => false, subtitle, finals = null, skipEditIds }) {
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
  const withFinals = finals
    ? applyFinalsToArticles(articles, finals, { skipEditIds: skipEditIds ?? new Set(Object.keys(edits)) }).articles
    : articles
  let chapterSeen = false
  withFinals.forEach(art => {
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
    // Manual de Redação: recuo de primeira linha igual em todos os dispositivos, espaçamento simples, 6 pt após.
    children.push(new Paragraph({
      alignment: AlignmentType.JUSTIFIED,
      spacing: { ...ESPACAMENTO },
      indent: { firstLine: RECUO_PRIMEIRA_LINHA },
      children: [
        new TextRun({ text: `${articleLabel(art.number)} `, bold: true, font: 'Times New Roman', size: 24 }),
        new TextRun({ text: art.caput, font: 'Times New Roman', size: 24 }),
      ],
    }))
    art.incisos.forEach((inc, i) => {
      // Parágrafos (§/Parágrafo único) e alíneas ("a) …") saem verbatim; alíneas recuadas.
      const runs = [new TextRun({ text: inc.ownMarker ? inc.text : `${rotuloRomano(art.incisos, i)} - ${inc.text}`, font: 'Times New Roman', size: 24 })]
      if (inc.source && inc.source !== 'ro') {
        runs.push(new TextRun({ text: ` (${inc.source})`, font: 'Times New Roman', size: 20, italics: true, color: '888888' }))
      }
      children.push(new Paragraph({
        alignment: AlignmentType.JUSTIFIED, spacing: { ...ESPACAMENTO },
        indent: { firstLine: RECUO_PRIMEIRA_LINHA }, children: runs,
      }))
    })
  })

  const doc = new Document({
    sections: [{
      properties: { page: { margin: { ...MARGENS } } },
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
