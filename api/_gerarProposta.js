// Lógica compartilhada (sem framework) para gerar a proposta via Gemini.
// Usada pela função serverless (Vercel) e pelo middleware de dev (Vite).
const DEFAULT_MODEL = 'gemini-2.0-flash'

export function buildPrompt(textoAtual, sugestoes) {
  const lista = (sugestoes ?? [])
    .map((s, i) => `${i + 1}. ${String(s).trim()}`)
    .join('\n')
  return [
    'Você é um redator legislativo experiente. Reescreva o dispositivo legal abaixo,',
    'incorporando as sugestões pertinentes e preservando a técnica e o estilo legislativo.',
    'Responda APENAS com o texto final do dispositivo, sem comentários, títulos ou aspas.',
    '',
    'TEXTO ATUAL DO DISPOSITIVO:',
    String(textoAtual ?? '').trim(),
    '',
    'SUGESTÕES RELEVANTES A CONSIDERAR:',
    lista || '(nenhuma)',
  ].join('\n')
}

export function parseGeminiResposta(json) {
  const txt = json?.candidates?.[0]?.content?.parts?.[0]?.text
  if (!txt || !String(txt).trim()) {
    throw new Error('Resposta da IA vazia ou em formato inesperado.')
  }
  return String(txt).trim()
}

export async function gerarPropostaCore({ textoAtual, sugestoes, apiKey, model = DEFAULT_MODEL }) {
  if (!apiKey) throw new Error('Chave do Gemini ausente no servidor (GEMINI_API_KEY).')
  const prompt = buildPrompt(textoAtual, sugestoes)
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }),
  })
  if (!resp.ok) {
    const detalhe = await resp.text().catch(() => '')
    throw new Error(`Gemini respondeu ${resp.status}: ${detalhe.slice(0, 200)}`)
  }
  return parseGeminiResposta(await resp.json())
}
