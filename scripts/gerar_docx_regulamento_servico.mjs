// Gera o .docx da Minuta do Regulamento de Serviço como o participante com escopo a vê
// (mesma geração da tela do admin — src/lib/consultaDocx.js). Com a exportação de textos
// finais (scripts/exportar_firestore.mjs), aplica os fechados.
//
//   node scripts/gerar_docx_regulamento_servico.mjs [--finals .firestore-export/fs_finalTexts.json] [--out pasta]
import path from 'node:path'
import { filtrarEstruturaPorEscopo } from '../src/lib/escopoServico.js'
import { docxMinutaConsulta } from '../src/lib/consultaDocx.js'
import { ROOT, lerJson, lerBrasao, carregarFinais, salvarDocumento } from './lib_docx_minuta.mjs'

const args = process.argv.slice(2)
const arg = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null }
const outDir = arg('--out') ?? path.join(ROOT, 'docs', 'sei', '2026-09-11-regulamento-servico')
const finals = carregarFinais(arg('--finals'))

const completa = lerJson('database/atual/regulamento_structure.json')
const recorte = filtrarEstruturaPorEscopo(completa, 'servico')
const { doc, artigos, aplicados } = docxMinutaConsulta({ completa, recorte, finals, brasao: lerBrasao() })
const arquivo = await salvarDocumento(doc, path.join(outDir, 'Minuta_Regulamento_de_Servico_CBMRO_versao_em_consulta.docx'))
console.log(`OK: ${arquivo}`)
console.log(`artigos: ${artigos} · textos finais aplicados: ${aplicados}${finals ? '' : ' (sem exportação de finalTexts)'}`)
