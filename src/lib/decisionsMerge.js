// Funde as decisões do JSON (pipeline da Fase 2) com os registros do Firebase.
// Precedência: registro no sistema > decidida no vault > pendente.
// O registro é procurado sob a chave DO CENÁRIO ativo (decisionDocId) — um registro
// feito no atual não pode marcar a decisão como decidida na futura, e vice-versa.
import { decisionDocId } from './decisoes.js'

export function mergeDecisoes(decisoesJson, fbMap, cenario) {
  return (decisoesJson ?? []).map(d => {
    const registro = fbMap?.get(decisionDocId(d.id, cenario)) ?? null
    if (registro) return { ...d, statusDecisao: 'sistema', registro }
    if (d.decidido) return { ...d, statusDecisao: 'vault', registro: null }
    return { ...d, statusDecisao: 'pendente', registro: null }
  })
}

export function pendenciasDeAplicacao(merged) {
  return merged.filter(d =>
    d.registro?.tipo === 'estrutural' && d.registro?.ficha?.status === 'aguardando')
}
