// Relatório das interações (.docx + .md + .json) e Quadro de análise (.docx) da consulta da
// Minuta do Regulamento de Serviço — mesma geração da tela do admin (src/lib/consultaDocx.js).
//
// Entrada: exportação do Firestore (scripts/exportar_firestore.mjs):
//   .firestore-export/fs_suggestions.json, fs_members.json (e fs_finalTexts.json, opcional)
//
//   node scripts/gerar_sei_interacoes.mjs [--export pasta] [--out pasta] [--desde AAAA-MM-DD]
//
// Só os militares consultados (escopo "servico"). Os registros das contas de administração do
// portal são revisão interna, já incorporada à versão atual, e não saem como sugestão. Cada
// registro traz a coluna "Aplicação": o que a versão atual fez com o artigo comentado.
import fs from 'node:fs'
import path from 'node:path'
import { filtrarEstruturaPorEscopo } from '../src/lib/escopoServico.js'
import {
  indexarRecorte, selecionarInteracoes, resumoParticipacao, formatarDataHora, localizar,
  aplicacaoPorArtigo, ROTULO_APLICACAO,
} from '../src/lib/consultaRelatorios.js'
import { docxRelatorioInteracoes, docxQuadroAnalise } from '../src/lib/consultaDocx.js'
import { ROOT, lerJson, lerBrasao, carregarFinais, salvarDocumento } from './lib_docx_minuta.mjs'

const args = process.argv.slice(2)
const arg = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null }
const exportDir = arg('--export') ?? path.join(ROOT, '.firestore-export')
const outDir = arg('--out') ?? path.join(ROOT, 'docs', 'sei', '2026-09-11-regulamento-servico')
const desde = arg('--desde') ? new Date(arg('--desde')) : null

const lerExport = (nome, obrigatorio = true) => {
  const p = path.join(exportDir, nome)
  if (!fs.existsSync(p)) {
    if (obrigatorio) { console.error(`Falta ${p} — rode scripts/exportar_firestore.mjs antes.`); process.exit(2) }
    return []
  }
  return JSON.parse(fs.readFileSync(p, 'utf8'))
}
const sugestoes = lerExport('fs_suggestions.json')
const membros = lerExport('fs_members.json', false)
const finals = carregarFinais(path.join(exportDir, 'fs_finalTexts.json')) ?? new Map()

const completa = lerJson('database/atual/regulamento_structure_consulta.json')
const atualCompleta = lerJson('database/atual/regulamento_structure.json')
const recorte = filtrarEstruturaPorEscopo(completa, 'servico')
const indice = indexarRecorte(recorte)
const totalArtigos = recorte.chapters.reduce((n, c) => n + c.articles.length, 0)
const interacoes = selecionarInteracoes({ sugestoes, membros, indice, finals, desde, aplicacaoArtigos: aplicacaoPorArtigo(atualCompleta) })
const resumo = resumoParticipacao(membros, interacoes)
const foraDoRecorte = sugestoes.filter(s => String(s.dispositivoId ?? '').startsWith('reg:') && !localizar(indice, s.dispositivoId).noRecorte).length
const rotuloAplicacao = (r) => `${ROTULO_APLICACAO[r.aplicacao?.como] ?? ROTULO_APLICACAO.nenhuma}${r.aplicacao?.nota ? ` — ${r.aplicacao.nota}` : ''}`

fs.mkdirSync(outDir, { recursive: true })
fs.writeFileSync(path.join(outDir, 'interacoes_consulta.json'), JSON.stringify(interacoes.map(r => ({ ...r, data: r.data?.toISOString() ?? null })), null, 2), 'utf8')

const esc = (t) => String(t ?? '').replace(/\|/g, '\\|').replace(/\n/g, ' ')
const md = [`# Interações recebidas — consulta da Minuta do Regulamento de Serviço`, ``,
  `Gerado em ${formatarDataHora(new Date())} a partir da coleção \`suggestions\` do Firestore (${sugestoes.length} registros no total; ${interacoes.length} dos militares consultados sobre o recorte${desde ? `, a partir de ${arg('--desde')}` : ''}; ${foraDoRecorte} do Regulamento fora do recorte).`, ``,
  `Aplicação na versão atual da minuta: ${resumo.aplicadas} sugestões sobre artigos alterados, ${resumo.total - resumo.aplicadas} sobre artigos mantidos. Por tipo: ${Object.keys(ROTULO_APLICACAO).filter(k => resumo.aplicacoes[k]).map(k => `${ROTULO_APLICACAO[k]}: ${resumo.aplicacoes[k]}`).join('; ')}.`, ``,
  `| # | Data | Autor | Unidade | Alcance | Dispositivo | Endereço | Sugestão | Aplicação | Parecer |`, `|---|---|---|---|---|---|---|---|---|---|`]
for (const r of interacoes) {
  md.push(`| ${r.n} | ${formatarDataHora(r.data)} | ${r.autor.nome}${r.autor.nomeGuerra ? ` (${r.autor.nomeGuerra})` : ''} | ${r.autor.unidade} | ${r.autor.alcance} | ${r.dispositivo} | \`${r.dispositivoId}\` | ${esc(r.sugestao)} | ${esc(rotuloAplicacao(r))} | ${r.parecer} |`)
}
fs.writeFileSync(path.join(outDir, 'interacoes_consulta.md'), md.join('\n'), 'utf8')

const brasao = lerBrasao()
const rel = docxRelatorioInteracoes({ interacoes, membros, totalArtigos, brasao, desde })
await salvarDocumento(rel.doc, path.join(outDir, 'Relatorio_Interacoes_Consulta_Regulamento_de_Servico.docx'))
const quadro = docxQuadroAnalise({ interacoes, membros, brasao })
await salvarDocumento(quadro.doc, path.join(outDir, 'Quadro_Analise_Aplicacao_Regulamento_de_Servico.docx'))
console.log(`OK: ${outDir}`)
console.log(`sugestões: total ${sugestoes.length} · listadas ${interacoes.length} (militares consultados) · reg fora do recorte ${foraDoRecorte} · pareceres: ${resumo.pareceres.relevante} relevantes, ${resumo.pareceres.descartada} descartadas, ${resumo.pareceres.pendente} sem parecer`)
console.log(`aplicação: ${resumo.aplicadas} sobre artigos alterados, ${resumo.total - resumo.aplicadas} sobre artigos mantidos · ${JSON.stringify(resumo.aplicacoes)}`)
