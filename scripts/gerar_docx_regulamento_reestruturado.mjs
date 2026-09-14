// Minuta REESTRUTURADA (Parte Geral + Parte Especial) — mesma geração da tela do admin
// (src/lib/consultaDocx.js); a estrutura vive em src/lib/regulamentoReestruturado.js.
//
//   node scripts/gerar_docx_regulamento_reestruturado.mjs [--finals fs_finalTexts.json] [--out pasta]
import path from 'node:path'
import fs from 'node:fs'
import { filtrarEstruturaPorEscopo } from '../src/lib/escopoServico.js'
import { montarReestruturada } from '../src/lib/regulamentoReestruturado.js'
import { docxMinutaReestruturada } from '../src/lib/consultaDocx.js'
import { ROOT, lerJson, lerBrasao, carregarFinais, salvarDocumento } from './lib_docx_minuta.mjs'

const args = process.argv.slice(2)
const arg = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null }
const outDir = arg('--out') ?? path.join(ROOT, 'docs', 'sei', '2026-09-11-regulamento-servico')
const finals = carregarFinais(arg('--finals'))

const completa = lerJson('database/atual/regulamento_structure_consulta.json')
const recorte = filtrarEstruturaPorEscopo(completa, 'servico')
const { doc, artigos, aplicados } = docxMinutaReestruturada({ recorte, finals, brasao: lerBrasao() })
const arquivo = await salvarDocumento(doc, path.join(outDir, 'Minuta_Regulamento_de_Servico_CBMRO_reestruturada_parte_geral_e_especial.docx'))
fs.writeFileSync(path.join(outDir, 'depara_reestruturacao.json'), JSON.stringify(montarReestruturada(recorte).depara.map(d => [d.novo, d.antigo, d.origem, d.posicao]), null, 2), 'utf8')
console.log(`OK: ${arquivo}`)
console.log(`artigos: ${artigos} · textos finais aplicados: ${aplicados}${finals ? '' : ' (sem exportação de finalTexts)'}`)
