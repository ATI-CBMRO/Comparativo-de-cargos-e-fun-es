import { useAuth } from '../lib/auth.jsx'

export default function Revisao() {
  const { user } = useAuth()
  return (
    <div style={{ padding: 32 }}>
      <h2 style={{ color: '#121d3d' }}>Revisão da Minuta</h2>
      <p>Olá, {user?.nome}. Seu papel: <strong>{user?.role}</strong>.</p>
      <p style={{ color: '#5a667f' }}>
        Esta área receberá o documento com os comentários por inciso na Etapa 2.
      </p>
    </div>
  )
}
