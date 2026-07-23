// Lógica pura da conferência persistente. A chave é estável enquanto a estrutura
// estiver congelada (mesma premissa do dispositivoId da Revisão).
import { docOfDispositivo, scenarioOfDispositivo } from './reviewGroup.js'

export function confKey(dispositivo) {
  return `${dispositivo.editId}#art${dispositivo.number}`
}

export function mergeStatus(localMap, remotoMap) {
  const m = new Map(localMap)
  remotoMap?.forEach((v, k) => { m.set(k, v.status) })
  return m
}

export function divergentesDe(remotoMap, docId, cenario) {
  const out = []
  remotoMap?.forEach((v, k) => {
    if (v.status !== 'div') return
    if (docOfDispositivo(k) !== docId) return
    if (scenarioOfDispositivo(k) !== cenario) return
    out.push({ key: k, status: v.status })
  })
  return out
}
