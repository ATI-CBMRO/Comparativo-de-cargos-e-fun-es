import { Navigate } from 'react-router-dom'
import { useAuth } from '../lib/auth.jsx'

export default function ProtectedRoute({ children, requireAdmin = false }) {
  const { user, loading } = useAuth()
  if (loading) return <div style={{ padding: 32 }}>Carregando…</div>
  if (!user) return <Navigate to="/login" replace />
  if (requireAdmin && user.role !== 'admin') {
    return <div style={{ padding: 32 }}>Acesso restrito ao administrador.</div>
  }
  return children
}
