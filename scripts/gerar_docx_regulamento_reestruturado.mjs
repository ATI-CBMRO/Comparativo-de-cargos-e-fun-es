// Minuta em PARTE GERAL + PARTE ESPECIAL, formato publicável (versão ATUAL, sem selos nem
// anexos, frases capitalizadas) — mesma geração da tela do admin (src/lib/consultaDocx.js).
// O quadro de dispositivos semelhantes foi eliminado por decisão de 15/09/2026 (a lógica
// segue em src/lib/dispositivosSemelhantes.js, sem uso na tela).
//
//   node scripts/gerar_docx_regulamento_reestruturado.mjs [--out pasta]
import path from 'node:path'
import fs from 'node:fs'
import { filtrarEstruturaPorEscopo } from '../src/lib/escopoServico.js'
import { docxMinutaReestruturada } from '../src/lib/consultaDocx.js'
import { ROOT, lerJson, lerBrasao, salvarDocumento } from './lib_docx_minuta.mjs'

const args = process.argv.slice(2)
const arg = (k) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : null }
const outDir = arg('--out') ?? path.join(ROOT, 'docs', 'sei', '2026-09-11-regulamento-servico')
const brasao = lerBrasao()

const atualCompleta = lerJson('database/atual/regulamento_structure.json')
const recorte = filtrarEstruturaPorEscopo(atualCompleta, 'servico')
const { doc, artigos, depara } = docxMinutaReestruturada({ recorte, brasao })
const arquivo = await salvarDocumento(doc, path.join(outDir, 'Minuta_Regulamento_de_Servico_CBMRO_parte_geral_e_especial.docx'))
fs.writeFileSync(path.join(outDir, 'depara_reestruturacao.json'), JSON.stringify(depara.map(d => [d.novo, d.antigo, d.origem, d.posicao]), null, 2), 'utf8')
console.log(`OK: ${arquivo}`)
console.log(`artigos: ${artigos}`)

