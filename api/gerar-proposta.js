import { gerarPropostaCore } from './_gerarProposta.js'
import { guardarRequisicao } from './_authGuard.js'

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Método não permitido' })
    return
  }
  try {
    const body = req.body ?? {}
    const rawSize = req.headers?.['content-length']
      ? Number(req.headers['content-length'])
      : Buffer.byteLength(JSON.stringify(body))
    await guardarRequisicao({
      authorization: req.headers?.authorization,
      body,
      rawSize,
      apiKey: process.env.VITE_FIREBASE_API_KEY,
      projectId: process.env.VITE_FIREBASE_PROJECT_ID,
    })
    const { textoAtual, sugestoes } = body
    const proposta = await gerarPropostaCore({
      textoAtual, sugestoes, apiKey: process.env.GEMINI_API_KEY,
    })
    res.status(200).json({ proposta })
  } catch (e) {
    res.status(e?.status || 500).json({ error: String(e?.message || e) })
  }
}
