import {
  collection, addDoc, deleteDoc, doc, updateDoc, setDoc,
  onSnapshot, query, orderBy, serverTimestamp,
  arrayUnion, arrayRemove,
} from 'firebase/firestore'
import { db } from './firebase.js'

const COL = 'suggestions'
const COL_FINAL = 'finalTexts'
const DOC_CONFIG = doc(db, 'config', 'revisao')

export function subscribeSuggestions(onChange, onError) {
  const q = query(collection(db, COL), orderBy('criadoEm', 'asc'))
  return onSnapshot(q,
    (snap) => {
      const list = snap.docs.map(d => ({ id: d.id, ...d.data() }))
      onChange(list)
    },
    (err) => { if (onError) onError(err) },
  )
}

// As rules limitam os snapshots a 1000 chars (A8.7); dispositivos longos (há incisos
// de 1792 chars no Regulamento e textos de até 7737 no RI) são truncados — o snapshot
// é só contexto, o dispositivoId continua apontando para o texto íntegro.
const SNAPSHOT_MAX = 1000

export async function addSuggestion({ dispositivoId, dispositivoLabelSnapshot, trechoSnapshot, texto, autor }) {
  await addDoc(collection(db, COL), {
    dispositivoId,
    dispositivoLabelSnapshot: String(dispositivoLabelSnapshot ?? '').slice(0, SNAPSHOT_MAX),
    trechoSnapshot: String(trechoSnapshot ?? '').slice(0, SNAPSHOT_MAX),
    texto: texto.trim(),
    autorUid: autor.uid,
    autorNome: autor.nome,
    curtidoPor: [],
    criadoEm: serverTimestamp(),
  })
}

export async function toggleLike(suggestion, uid) {
  const jaCurtiu = (suggestion.curtidoPor ?? []).includes(uid)
  await updateDoc(doc(db, COL, suggestion.id), {
    curtidoPor: jaCurtiu ? arrayRemove(uid) : arrayUnion(uid),
  })
}

export async function deleteSuggestion(id) {
  await deleteDoc(doc(db, COL, id))
}

export async function setAdminStatus(suggestionId, status) {
  await updateDoc(doc(db, COL, suggestionId), { adminStatus: status })
}

export function subscribeFinalTexts(onChange, onError) {
  return onSnapshot(collection(db, COL_FINAL),
    (snap) => {
      const map = new Map()
      snap.docs.forEach(d => map.set(d.id, d.data()))
      onChange(map)
    },
    (err) => { if (onError) onError(err) },
  )
}

export async function saveFinalText(dispositivoId, { texto, status, autor }) {
  await setDoc(doc(db, COL_FINAL, dispositivoId), {
    texto: texto.trim(),
    status,
    atualizadoPor: autor.nome,
    atualizadoEm: serverTimestamp(),
  }, { merge: true })
}

// Ausência do doc == regulamentoAberto:false (fail-closed) — nunca abrir por omissão.
export function subscribeRevisaoConfig(onChange, onError) {
  return onSnapshot(DOC_CONFIG,
    (snap) => onChange(snap.exists() ? snap.data() : { regulamentoAberto: false }),
    (err) => { if (onError) onError(err) },
  )
}

export async function setRegulamentoAberto(aberto) {
  await setDoc(DOC_CONFIG, { regulamentoAberto: aberto }, { merge: true })
}
