import { gerarPropostaCore } from './_gerarProposta.js'

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Método não permitido' })
    return
  }
  try {
    const { textoAtual, sugestoes } = req.body ?? {}
    const proposta = await gerarPropostaCore({
      textoAtual, sugestoes, apiKey: process.env.GEMINI_API_KEY,
    })
    res.status(200).json({ proposta })
  } catch (e) {
    res.status(500).json({ error: String(e?.message || e) })
  }
}
