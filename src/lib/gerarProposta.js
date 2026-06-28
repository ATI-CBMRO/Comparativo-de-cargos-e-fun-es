// Chama o endpoint seguro que fala com o Gemini. O frontend nunca vê a chave.
export async function gerarProposta({ textoAtual, sugestoesRelevantes }) {
  const resp = await fetch('/api/gerar-proposta', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ textoAtual, sugestoes: sugestoesRelevantes }),
  })
  const json = await resp.json().catch(() => ({}))
  if (!resp.ok) throw new Error(json.error || 'Falha ao gerar proposta.')
  return json.proposta
}
