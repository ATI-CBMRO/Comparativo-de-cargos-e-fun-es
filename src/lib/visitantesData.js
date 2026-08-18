// Registro dos visitantes do acervo público (spec 2026-08-18). Coleção `visitantes`,
// documento identificado pelo uid da sessão ANÔNIMA — não há e-mail autenticado aqui, e
// por isso este registro nunca se confunde com `members`.
import {
  collection, doc, setDoc, onSnapshot, query, orderBy, serverTimestamp,
} from 'firebase/firestore'
import { db } from './firebase.js'

const COL = 'visitantes'

// merge:true de propósito: se a pessoa limpar o localStorage e preencher de novo com a
// MESMA sessão anônima viva, isto ATUALIZA o registro (ultimoAcesso) em vez de duplicar.
// `criadoEm` só é escrito quando ainda não existe, preservando o primeiro acesso.
export async function registrarVisitante({ uid, nome, email, instituicao, primeiraVez = true }) {
  await setDoc(doc(db, COL, uid), {
    uid, nome, email, instituicao,
    ...(primeiraVez ? { criadoEm: serverTimestamp() } : {}),
    ultimoAcesso: serverTimestamp(),
  }, { merge: true })
}

export function subscribeVisitantes(onChange, onError) {
  const q = query(collection(db, COL), orderBy('ultimoAcesso', 'desc'))
  return onSnapshot(q,
    (snap) => onChange(snap.docs.map(d => ({ id: d.id, ...d.data() }))),
    (err) => { if (onError) onError(err) },
  )
}
