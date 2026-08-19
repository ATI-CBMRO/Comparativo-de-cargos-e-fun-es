// Sessão do visitante do acervo público. Independente do AuthProvider: nenhum dado passa
// de um para o outro. No React a aninhagem de provedores é inevitável, mas a
// INDEPENDÊNCIA é real — este módulo não importa auth.jsx, e auth.jsx ignora sessões
// anônimas (ver a guarda `fbUser.isAnonymous` lá).
import { createContext, useContext, useEffect, useState } from 'react'
import { signInAnonymously, onAuthStateChanged } from 'firebase/auth'
import { auth } from './firebase.js'
import { registrarVisitante, marcarRetorno } from './visitantesData.js'
import {
  normalizarVisitante, lerVisitanteLocal, gravarVisitanteLocal, limparVisitanteLocal,
} from './visitante.js'

const VisitanteContext = createContext(null)

export function VisitanteProvider({ children }) {
  const [visitante, setVisitante] = useState(null)
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')

  // Só considera visitante conhecido quando o localStorage E a sessão anônima do Firebase
  // concordam. Caso real que isto resolve: a pessoa entrou como visitante, depois logou
  // como membro (o login SUBSTITUI a sessão anônima) e saiu — o localStorage ficaria
  // apontando para um uid que não existe mais, e a gravação seria recusada pela regra
  // `request.auth.uid == uid`. Melhor pedir o cadastro de novo do que falhar depois.
  useEffect(() => {
    const unsub = onAuthStateChanged(auth, (fbUser) => {
      const local = lerVisitanteLocal(globalThis.localStorage)
      if (fbUser?.isAnonymous && local && local.uid === fbUser.uid) {
        setVisitante(local)
        marcarRetorno(fbUser.uid).catch((e) => console.error('Não foi possível atualizar o último acesso:', e))
      } else {
        if (local) limparVisitanteLocal(globalThis.localStorage)
        setVisitante(null)
      }
      setCarregando(false)
    }, (e) => {
      console.error('Erro ao verificar sessão do visitante:', e)
      setCarregando(false)
      setErro('Não foi possível verificar seu acesso agora. Recarregue a página.')
    })
    return unsub
  }, [])

  // Devolve true quando entrou. Erro fica em `erro` — e a tela MOSTRA (nunca só console).
  const entrar = async (campos) => {
    setErro('')
    const v = normalizarVisitante(campos)
    if (!v.ok) { setErro(v.erro); return false }
    try {
      // Já existe sessão anônima? Então este cadastro é REPETIÇÃO (a pessoa limpou o
      // localStorage) e `criadoEm` não pode ser reescrito — senão o "primeiro acesso" da
      // lista do admin viraria a data de hoje, todas as vezes. signInAnonymously reaproveita
      // a sessão existente em vez de criar outra, então precisamos olhar ANTES de chamar.
      const jaTinhaSessao = Boolean(auth.currentUser?.isAnonymous)
      const cred = await signInAnonymously(auth)
      const uid = cred.user.uid
      await registrarVisitante({ uid, ...v.dados, primeiraVez: !jaTinhaSessao })
      gravarVisitanteLocal(globalThis.localStorage, { uid, nome: v.dados.nome, email: v.dados.email })
      setVisitante({ uid, nome: v.dados.nome, email: v.dados.email })
      return true
    } catch (e) {
      console.error('Falha ao registrar visitante:', e)
      setErro(
        e?.code === 'auth/operation-not-allowed'
          ? 'O acesso público ainda não foi habilitado no servidor. Avise o administrador do portal.'
          : 'Não foi possível concluir o cadastro agora. Tente novamente.',
      )
      return false
    }
  }

  return (
    <VisitanteContext.Provider value={{ visitante, carregando, erro, entrar }}>
      {children}
    </VisitanteContext.Provider>
  )
}

export function useVisitante() {
  const ctx = useContext(VisitanteContext)
  if (ctx === null) throw new Error('useVisitante precisa estar dentro de <VisitanteProvider>')
  return ctx
}
