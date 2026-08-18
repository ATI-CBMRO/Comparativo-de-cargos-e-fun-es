// Registro dos visitantes do acervo público (spec 2026-08-18). Coleção `visitantes`,
// documento identificado pelo uid da sessão ANÔNIMA — não há e-mail autenticado aqui, e
// por isso este registro nunca se confunde com `members`.
import {
  collection, doc, setDoc, updateDoc, onSnapshot, query, orderBy, serverTimestamp,
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

// Toque de "ainda ativo": chamado quando o visitante volta com o localStorage intacto
// (sessão reconhecida sem precisar preencher o formulário de novo). Grava só ultimoAcesso —
// sem isto a coluna "Último acesso" do admin (Acessos.jsx) ficaria congelada na data do
// cadastro para sempre, e a ordenação por recência (subscribeVisitantes) viraria ordenação
// por data de cadastro. Passa na regra do Firestore mesmo sem reenviar nome/email/instituicao:
// em update/merge, request.resource.data é o documento MESCLADO (campos antigos preservados),
// então uid/nome/email/instituicao continuam presentes e hasOnly não quebra.
export async function marcarRetorno(uid) {
  await updateDoc(doc(db, COL, uid), { ultimoAcesso: serverTimestamp() })
}

export function subscribeVisitantes(onChange, onError) {
  const q = query(collection(db, COL), orderBy('ultimoAcesso', 'desc'))
  return onSnapshot(q,
    (snap) => onChange(snap.docs.map(d => ({ id: d.id, ...d.data() }))),
    (err) => { if (onError) onError(err) },
  )
}
