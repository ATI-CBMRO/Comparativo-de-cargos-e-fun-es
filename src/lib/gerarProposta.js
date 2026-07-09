import { auth } from './firebase.js'

// Chama o endpoint seguro que fala com o Gemini. O frontend nunca vê a chave.
// O endpoint exige login de administrador — enviamos o ID token do usuário atual.
export async function gerarProposta({ textoAtual, sugestoesRelevantes }) {
  if (!auth.currentUser) {
    throw new Error('Você precisa estar autenticado para gerar uma proposta.')
  }
  const token = await auth.currentUser.getIdToken()
  const resp = await fetch('/api/gerar-proposta', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ textoAtual, sugestoes: sugestoesRelevantes }),
  })
  const json = await resp.json().catch(() => ({}))
  if (!resp.ok) throw new Error(json.error || 'Falha ao gerar proposta.')
  return json.proposta
}
