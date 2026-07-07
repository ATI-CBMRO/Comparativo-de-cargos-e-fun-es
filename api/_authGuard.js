// Guarda de autenticação/autorização para o endpoint de IA (/api/gerar-proposta).
// Sem dependências novas: valida o ID token do Firebase por REST e checa se o dono do
// token é administrador ativo em `members/{email}`, usando o próprio token do usuário
// como Bearer (as firestore.rules já permitem o dono ler members/{email}).
const MAX_TEXTO_ATUAL = 4000
const MAX_SUGESTOES = 30
const MAX_SUGESTAO_LEN = 2000
const MAX_BODY_BYTES = 20 * 1024
const RATE_LIMIT_WINDOW_MS = 60 * 1000
const RATE_LIMIT_MAX = 8

function erro(status, mensagem) {
  const e = new Error(mensagem)
  e.status = status
  return e
}

function normalizeEmail(email) {
  return String(email ?? '').trim().toLowerCase()
}

export function validarPayload({ textoAtual, sugestoes, rawSize } = {}) {
  if (typeof rawSize === 'number' && rawSize > MAX_BODY_BYTES) {
    throw erro(413, `Corpo da requisição excede o limite de ${MAX_BODY_BYTES} bytes.`)
  }
  if (typeof textoAtual !== 'string' || textoAtual.length > MAX_TEXTO_ATUAL) {
    throw erro(400, `textoAtual deve ser uma string de até ${MAX_TEXTO_ATUAL} caracteres.`)
  }
  if (!Array.isArray(sugestoes) || sugestoes.length > MAX_SUGESTOES) {
    throw erro(400, `sugestoes deve ser um array de até ${MAX_SUGESTOES} itens.`)
  }
  for (const s of sugestoes) {
    if (typeof s !== 'string' || s.length > MAX_SUGESTAO_LEN) {
      throw erro(400, `Cada sugestão deve ser uma string de até ${MAX_SUGESTAO_LEN} caracteres.`)
    }
  }
}

export async function verificarIdToken(idToken, apiKey) {
  if (!idToken) throw erro(401, 'Token de autenticação ausente.')
  const url = `https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=${apiKey}`
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ idToken }),
  })
  if (!resp.ok) throw erro(401, 'Token de autenticação inválido ou expirado.')
  const json = await resp.json().catch(() => null)
  const email = json?.users?.[0]?.email
  if (!email) throw erro(401, 'Token de autenticação inválido ou expirado.')
  return normalizeEmail(email)
}

export async function verificarMembro(idToken, projectId, email) {
  const url = `https://firestore.googleapis.com/v1/projects/${projectId}/databases/(default)/documents/members/${encodeURIComponent(email)}`
  const resp = await fetch(url, { headers: { Authorization: `Bearer ${idToken}` } })
  if (!resp.ok) throw erro(403, 'Acesso restrito a administradores.')
  const doc = await resp.json().catch(() => null)
  const ativo = doc?.fields?.ativo?.booleanValue === true
  const role = doc?.fields?.role?.stringValue
  if (!ativo || role !== 'admin') {
    throw erro(403, 'Acesso restrito a administradores.')
  }
}

// Best-effort: janela deslizante em memória por instância serverless. Não é à prova de
// balas (cada instância fria tem seu próprio mapa), mas já impede o abuso trivial de cota.
const rateLimitState = new Map()

export function checarRateLimit(email, now = Date.now()) {
  const hist = (rateLimitState.get(email) || []).filter((t) => now - t < RATE_LIMIT_WINDOW_MS)
  if (hist.length >= RATE_LIMIT_MAX) {
    throw erro(429, 'Muitas requisições em pouco tempo. Aguarde um minuto e tente novamente.')
  }
  hist.push(now)
  rateLimitState.set(email, hist)
}

export async function guardarRequisicao({ authorization, body, rawSize, apiKey, projectId }) {
  validarPayload({ ...(body || {}), rawSize })
  const bearer = String(authorization || '').replace(/^Bearer\s+/i, '').trim()
  const email = await verificarIdToken(bearer, apiKey)
  await verificarMembro(bearer, projectId, email)
  checarRateLimit(email)
  return { email }
}
