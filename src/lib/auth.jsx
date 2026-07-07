import { createContext, useContext, useEffect, useState } from 'react'
import {
  signInWithEmailAndPassword, createUserWithEmailAndPassword,
  signOut, onAuthStateChanged, sendPasswordResetEmail,
} from 'firebase/auth'
import { doc, getDoc, updateDoc, serverTimestamp } from 'firebase/firestore'
import { auth, db } from './firebase.js'
import { normalizeEmail } from './membersStats.js'
import { PROTOTYPE_STORAGE_KEY } from './suggestionsStore.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [naoAutorizado, setNaoAutorizado] = useState(false)

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, async (fbUser) => {
      if (!fbUser) {
        setUser(null); setNaoAutorizado(false); setLoading(false)
        return
      }
      try {
        // Autorização = existir members/{email} com ativo == true.
        const email = normalizeEmail(fbUser.email)
        const ref = doc(db, 'members', email)
        const snap = await getDoc(ref)
        if (!snap.exists() || snap.data().ativo !== true) {
          setUser(null); setNaoAutorizado(true)
          await signOut(auth)
          return
        }
        const m = snap.data()
        // Marca presença: vincula o uid, confirma o cadastro e registra o login.
        try {
          await updateDoc(ref, {
            uid: fbUser.uid,
            status: 'cadastrado',
            ultimoLogin: serverTimestamp(),
          })
        } catch (e) {
          console.error('Não foi possível registrar o último login:', e)
        }
        setUser({
          uid: fbUser.uid,
          email,
          nome: m.nome ?? email,
          role: m.role === 'admin' ? 'admin' : 'participante',
        })
        setNaoAutorizado(false)
      } catch (e) {
        // Falha ao verificar o cadastro (ex.: rede): não trava a tela.
        console.error('Erro ao verificar acesso:', e)
        setUser(null); setNaoAutorizado(false)
      } finally {
        setLoading(false)
      }
    })
    return unsub
  }, [])

  const entrar = async (email, senha) => {
    await signInWithEmailAndPassword(auth, normalizeEmail(email), senha)
  }
  const cadastrar = async (email, senha) => {
    await createUserWithEmailAndPassword(auth, normalizeEmail(email), senha)
  }
  const sair = async () => {
    await signOut(auth)
    // Limpa só as chaves do protótipo de revisão (localStorage), nunca localStorage.clear() —
    // outras chaves da página não pertencem a este app.
    try { window.localStorage?.removeItem(PROTOTYPE_STORAGE_KEY) } catch { /* ambiente sem localStorage */ }
  }
  const recuperarSenha = (email) => sendPasswordResetEmail(auth, normalizeEmail(email))

  return (
    <AuthContext.Provider value={{ user, loading, naoAutorizado, entrar, cadastrar, sair, recuperarSenha }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (ctx === null) throw new Error('useAuth precisa estar dentro de <AuthProvider>')
  return ctx
}
