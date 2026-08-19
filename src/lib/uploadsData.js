// Envios de documentos pelos visitantes do acervo público (spec 2026-08-18).
// O ARQUIVO vai para o Storage (uploads-visitantes/{uid}/...) e os METADADOS para a
// coleção `uploadsVisitantes` do Firestore. Os dois lados são apagados juntos —
// ver removerUpload.
import {
  collection, addDoc, deleteDoc, doc, onSnapshot, query, orderBy, serverTimestamp,
} from 'firebase/firestore'
import { ref, uploadBytes, getDownloadURL, deleteObject } from 'firebase/storage'
import { db, storage } from './firebase.js'
import { caminhoUpload, nomeArquivoSeguro } from './uploadDocumento.js'

const COL = 'uploadsVisitantes'

// Ordem importa: sobe o arquivo PRIMEIRO, grava o metadado DEPOIS. Se o metadado falhar,
// apaga o arquivo recém-enviado — senão fica um objeto órfão no Storage, consumindo cota,
// sem nenhum registro que aponte para ele (ninguém jamais saberia que existe).
// A ordem inversa (metadado primeiro) deixaria uma linha na caixa de entrada do admin
// cujo botão "Baixar" quebra — pior, porque é visível e confunde.
export async function enviarDocumento({
  uid, nomeVisitante, emailVisitante, estado, tipoDocumento, observacao, arquivo,
}) {
  const storagePath = caminhoUpload(uid, arquivo.name, Date.now())
  const objeto = ref(storage, storagePath)
  await uploadBytes(objeto, arquivo, { contentType: 'application/pdf' })

  try {
    await addDoc(collection(db, COL), {
      uid,
      nomeVisitante,
      emailVisitante,
      estado,
      tipoDocumento,
      observacao,
      storagePath,
      nomeArquivo: nomeArquivoSeguro(arquivo.name),
      tamanho: arquivo.size,
      criadoEm: serverTimestamp(),
    })
  } catch (e) {
    await deleteObject(objeto).catch(() => { /* melhor esforço: o erro que importa é o de baixo */ })
    throw e
  }
}

export function subscribeUploads(onChange, onError) {
  const q = query(collection(db, COL), orderBy('criadoEm', 'desc'))
  return onSnapshot(q,
    (snap) => onChange(snap.docs.map(d => ({ id: d.id, ...d.data() }))),
    (err) => { if (onError) onError(err) },
  )
}

// URL gerada sob demanda (no clique), não na renderização da lista: uma chamada de rede
// por linha só para desenhar a tabela seria desperdício, e a URL tem validade própria.
export function urlDeDownload(storagePath) {
  return getDownloadURL(ref(storage, storagePath))
}

// Apaga os DOIS lados. O arquivo primeiro: se o Storage falhar, o metadado continua lá e
// o admin pode tentar de novo. Se fosse o contrário e o Storage falhasse, o arquivo
// ficaria órfão, invisível e impossível de achar pela interface.
export async function removerUpload({ id, storagePath }) {
  await deleteObject(ref(storage, storagePath))
  await deleteDoc(doc(db, COL, id))
}
