import { createContext, useContext, useEffect, useState } from 'react'
import {
  signInWithEmailAndPassword, signOut, onAuthStateChanged,
  sendPasswordResetEmail,
} from 'firebase/auth'
import { doc, getDoc } from 'firebase/firestore'
import { auth, db } from './firebase.js'

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
      // Autorização = existir members/{uid} com ativo == true.
      const snap = await getDoc(doc(db, 'members', fbUser.uid))
      if (!snap.exists() || snap.data().ativo !== true) {
        setUser(null); setNaoAutorizado(true)
        await signOut(auth)
        setLoading(false)
        return
      }
      const m = snap.data()
      setUser({
        uid: fbUser.uid,
        email: fbUser.email,
        nome: m.nome ?? fbUser.email,
        role: m.role === 'admin' ? 'admin' : 'participante',
      })
      setNaoAutorizado(false)
      setLoading(false)
    })
    return unsub
  }, [])

  const entrar = async (email, senha) => {
    await signInWithEmailAndPassword(auth, email.trim(), senha)
  }
  const sair = () => signOut(auth)
  const recuperarSenha = (email) => sendPasswordResetEmail(auth, email.trim())

  return (
    <AuthContext.Provider value={{ user, loading, naoAutorizado, entrar, sair, recuperarSenha }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (ctx === null) throw new Error('useAuth precisa estar dentro de <AuthProvider>')
  return ctx
}
