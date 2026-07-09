// Endereço ESTÁVEL de um dispositivo da minuta para ancorar comentários.
// Não use o rótulo "Art. 7º" (a numeração muda quando o texto é editado).
// Use o editId estável da seção + o índice original do inciso (mesmos que
// buildArticles expõe em cada inciso: { editId, index }).

export function incisoDispositivoId(editId, index) {
  return `${editId}#${index}`
}

export function caputDispositivoId(editId) {
  return `${editId}#caput`
}

export function parseDispositivoId(id) {
  const i = id.lastIndexOf('#')
  if (i === -1) return { editId: id, parte: null }
  const editId = id.slice(0, i)
  const tail = id.slice(i + 1)
  if (tail === 'caput') return { editId, parte: 'caput' }
  const n = Number(tail)
  return { editId, parte: Number.isInteger(n) ? n : null }
}
