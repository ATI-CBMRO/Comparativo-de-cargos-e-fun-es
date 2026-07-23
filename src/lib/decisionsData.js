// CRUD da coleção 'decisions' (decisões CBMRO registradas pelo sistema).
// Chave = id da decisão (nome da nota no vault, sem extensão). Encoding na fronteira
// por consistência (ids de decisão não têm '/', mas a regra é uniforme).
import {
  collection, doc, onSnapshot, setDoc, updateDoc, deleteDoc, serverTimestamp,
} from 'firebase/firestore'
import { db } from './firebase.js'
import { encodeFirestoreId, decodeFirestoreId } from './dispositivoId.js'

const COL = 'decisions'

export function subscribeDecisions(onChange, onError) {
  return onSnapshot(collection(db, COL),
    (snap) => {
      const map = new Map()
      snap.docs.forEach(d => map.set(decodeFirestoreId(d.id), d.data()))
      onChange(map)
    },
    (err) => { if (onError) onError(err) },
  )
}

// dados: { tipo, decisao, fonteEscolhida, alvoDispositivoId | null, ficha | null }
export async function registrarDecisao(id, dados, autor) {
  await setDoc(doc(db, COL, encodeFirestoreId(id)), {
    ...dados,
    registradoPor: autor.nome,
    registradoEm: serverTimestamp(),
  })
}

export async function marcarFichaAplicada(id) {
  await updateDoc(doc(db, COL, encodeFirestoreId(id)), { 'ficha.status': 'aplicada' })
}

export async function desfazerDecisao(id) {
  await deleteDoc(doc(db, COL, encodeFirestoreId(id)))
}
