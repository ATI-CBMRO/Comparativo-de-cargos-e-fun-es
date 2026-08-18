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
  const [pendente, setPendente] = useState(false)
  const [erroVerificacao, setErroVerificacao] = useState(null)

  useEffect(() => {
    const unsub = onAuthStateChanged(auth, async (fbUser) => {
      // Sessão ANÔNIMA é do visitante do acervo público (src/lib/visitante.jsx) e não
      // pertence a este provedor: ela não tem e-mail, então a checagem de members faria
      // doc(db,'members','') — caminho vazio — e o signOut abaixo derrubaria o visitante.
      // `user` continua significando "membro autorizado", e só isso.
      if (!fbUser || fbUser.isAnonymous) {
        setUser(null); setNaoAutorizado(false); setPendente(false); setLoading(false)
        return
      }
      try {
        // Autorização = existir members/{email} com ativo == true.
        const email = normalizeEmail(fbUser.email)
        const ref = doc(db, 'members', email)
        const snap = await getDoc(ref)
        if (!snap.exists() || snap.data().ativo !== true) {
          setUser(null)
          setNaoAutorizado(true)
          setPendente(snap.exists() && snap.data().status === 'pendente')
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
          // Escopo restringe o participante a um recorte do portal (ver
          // src/lib/escopoServico.js). Ausente/desconhecido = null = portal completo,
          // que é o caso de TODOS os cadastros existentes.
          escopo: m.escopo === 'servico' ? 'servico' : null,
        })
        setNaoAutorizado(false)
        setPendente(false)
        setErroVerificacao(null)
      } catch (e) {
        // Falha ao verificar o cadastro (ex.: rede): não trava a tela, mas AVISA —
        // antes o usuário só via a tela de login de novo, achando que perdeu o
        // acesso, quando foi falha transitória (auditoria 2026-07-23).
        console.error('Erro ao verificar acesso:', e)
        setUser(null); setNaoAutorizado(false); setPendente(false)
        setErroVerificacao('Não foi possível verificar seu acesso agora (falha de conexão). Tente entrar novamente.')
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
    const cred = await createUserWithEmailAndPassword(auth, normalizeEmail(email), senha)
    return cred.user
  }
  const sair = async () => {
    await signOut(auth)
    // Limpa só as chaves do protótipo de revisão (localStorage), nunca localStorage.clear() —
    // outras chaves da página não pertencem a este app.
    try { window.localStorage?.removeItem(PROTOTYPE_STORAGE_KEY) } catch { /* ambiente sem localStorage */ }
  }
  const recuperarSenha = (email) => sendPasswordResetEmail(auth, normalizeEmail(email))

  return (
    <AuthContext.Provider value={{ user, loading, naoAutorizado, pendente, erroVerificacao, entrar, cadastrar, sair, recuperarSenha }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (ctx === null) throw new Error('useAuth precisa estar dentro de <AuthProvider>')
  return ctx
}
