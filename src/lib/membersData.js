import {
  collection, doc, setDoc, updateDoc, deleteDoc,
  onSnapshot, query, orderBy, serverTimestamp,
} from 'firebase/firestore'
import { db } from './firebase.js'
import { normalizeEmail } from './membersStats.js'

const COL = 'members'

export function subscribeMembers(onChange, onError) {
  const q = query(collection(db, COL), orderBy('criadoEm', 'asc'))
  return onSnapshot(q,
    (snap) => onChange(snap.docs.map(d => ({ id: d.id, ...d.data() }))),
    (err) => { if (onError) onError(err) },
  )
}

export async function addMember({ email, nome, role }, criadoPor) {
  const id = normalizeEmail(email)
  await setDoc(doc(db, COL, id), {
    email: id,
    nome: (nome ?? '').trim() || id,
    role: role === 'admin' ? 'admin' : 'participante',
    ativo: true,
    status: 'convidado',
    uid: null,
    criadoEm: serverTimestamp(),
    criadoPor: criadoPor ?? null,
    ultimoLogin: null,
  })
}

export async function setMemberRole(email, role) {
  await updateDoc(doc(db, COL, normalizeEmail(email)), {
    role: role === 'admin' ? 'admin' : 'participante',
  })
}

export async function setMemberAtivo(email, ativo) {
  await updateDoc(doc(db, COL, normalizeEmail(email)), { ativo: !!ativo })
}

export async function removeMember(email) {
  await deleteDoc(doc(db, COL, normalizeEmail(email)))
}
