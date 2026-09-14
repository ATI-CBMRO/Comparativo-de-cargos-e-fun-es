// Helpers Node (fora do navegador) para os scripts de docs/sei/. A geração dos quatro .docx
// do pacote da consulta vive em src/lib/consultaDocx.js (compartilhada com a tela do admin);
// aqui ficam só leitura de arquivos, brasão em disco, empacotamento e o conversor de
// Markdown (md_para_docx.mjs).
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import {
  Document, Packer, Paragraph, TextRun, Footer, AlignmentType, PageBreak,
  Table, TableRow, TableCell, WidthType, ImageRun, PageNumber,
} from 'docx'
import { articleLabel, romanize } from '../src/lib/minutaArticles.js'
import { mapaFinais } from '../src/lib/consultaRelatorios.js'

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const FONT = 'Times New Roman'

export function lerJson(rel) {
  return JSON.parse(fs.readFileSync(path.join(ROOT, rel), 'utf8'))
}

export function lerBrasao() {
  const p = path.join(ROOT, 'public', 'BrasaoCBMRO2D-COMPLETO.png')
  return fs.existsSync(p) ? fs.readFileSync(p) : null
}

// Lê a exportação fs_finalTexts.json (scripts/exportar_firestore.mjs) → Map por dispositivoId.
export function carregarFinais(arquivo) {
  if (!arquivo || !fs.existsSync(arquivo)) return null
  return mapaFinais(JSON.parse(fs.readFileSync(arquivo, 'utf8')))
}

export async function salvarDocumento(doc, arquivo) {
  const buf = await Packer.toBuffer(doc)
  fs.mkdirSync(path.dirname(arquivo), { recursive: true })
  fs.writeFileSync(arquivo, buf)
  return arquivo
}

export function dataExtensoPtBr(d = new Date()) {
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })
}

export function run(text, opts = {}) {
  return new TextRun({ text, font: FONT, size: 24, ...opts })
}

export function pCentro(text, { bold = true, size = 26, before = 240, after = 120, italics = false, pageBreakBefore = false } = {}) {
  return new Paragraph({ alignment: AlignmentType.CENTER, pageBreakBefore, spacing: { before, after }, children: [run(text, { bold, size, italics })] })
}

export function pJustificado(text, { italics = false, size = 24, after = 120, firstLine = 708, bold = false } = {}) {
  return new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { line: 360, after }, indent: firstLine ? { firstLine } : undefined, children: [run(text, { italics, size, bold })] })
}

export function cabecalhoInstitucional(subtitulo, linhaExtra) {
  const children = []
  const brasao = lerBrasao()
  if (brasao) {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, children: [new ImageRun({ data: brasao, transformation: { width: 65, height: 65 }, type: 'png' })] }))
  }
  children.push(
    pCentro('CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA', { size: 28, before: 120, after: 0 }),
    pCentro(subtitulo, { bold: false, size: 24, before: 0, after: 0 }),
  )
  if (linhaExtra) children.push(pCentro(linhaExtra, { bold: false, size: 22, italics: true, before: 0, after: 0 }))
  children.push(pCentro(dataExtensoPtBr(), { bold: false, size: 22, italics: true, before: 0, after: 480 }))
  return children
}

export function tabela(linhas, larguras) {
  const cell = (texto, { bold = false, shade } = {}) => new TableCell({
    shading: shade ? { fill: shade } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: String(texto ?? '').split('\n').map(l => new Paragraph({ spacing: { after: 0 }, children: [run(l, { size: 20, bold })] })),
  })
  const rows = linhas.map((l, i) => new TableRow({ tableHeader: i === 0, children: l.map(t => cell(t, { bold: i === 0, shade: i === 0 ? 'E8E8E8' : undefined })) }))
  return new Table({ rows, width: { size: 100, type: WidthType.PERCENTAGE }, columnWidths: larguras })
}

export async function salvarDocx(children, arquivo, rodape) {
  const doc = new Document({
    styles: { default: { document: { run: { font: FONT, size: 24 } } } },
    sections: [{
      properties: { page: { margin: { top: 1701, right: 1134, bottom: 1134, left: 1701 } } },
      footers: { default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [run(`${rodape} · pág. `, { size: 18, italics: true }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18, italics: true })],
      })] }) },
      children,
    }],
  })
  return salvarDocumento(doc, arquivo)
}

export { articleLabel, romanize, PageBreak, Paragraph, AlignmentType }
