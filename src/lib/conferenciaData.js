// Persistência do Confere/Divergente (coleção 'conferencia'), por membro logado.
import { collection, doc, onSnapshot, setDoc, deleteDoc, serverTimestamp } from 'firebase/firestore'
import { db } from './firebase.js'
import { encodeFirestoreId, decodeFirestoreId } from './dispositivoId.js'

const COL = 'conferencia'

export function subscribeConferencia(onChange, onError) {
  return onSnapshot(collection(db, COL),
    (snap) => {
      const map = new Map()
      snap.docs.forEach(d => map.set(decodeFirestoreId(d.id), d.data()))
      onChange(map)
    },
    (err) => { if (onError) onError(err) },
  )
}

export async function saveConferenciaStatus(key, status, autor) {
  const ref = doc(db, COL, encodeFirestoreId(key))
  if (status == null) { await deleteDoc(ref); return }
  await setDoc(ref, { status, por: autor.nome, em: serverTimestamp() })
}
