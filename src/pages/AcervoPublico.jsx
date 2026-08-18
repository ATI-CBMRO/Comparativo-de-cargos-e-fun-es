// Casca do acervo público: cabeçalho próprio, navegação de dois itens e as MESMAS telas
// do acervo do portal, montadas sob o prefixo /acervo-publico (AcervoBaseProvider).
// Ela vive FORA do portal logado de propósito — a fronteira entre visitante e membro é o
// caminho da URL, não uma condição de login (spec, seção 1).
import { Routes, Route, NavLink, Navigate, Link } from 'react-router-dom'
import { Library, Search as SearchIcon, LogIn } from 'lucide-react'
import MarcaPortal from '../components/MarcaPortal.jsx'
import Legislations from './Legislations.jsx'
import StateDetail from './StateDetail.jsx'
import SearchPage from './Search.jsx'
import CadastroVisitante from './CadastroVisitante.jsx'
import { useVisitante } from '../lib/visitante.jsx'
import { AcervoBaseProvider } from '../context/AcervoBaseContext.jsx'
import { BASE_PUBLICA } from '../lib/visitante.js'

export default function AcervoPublico() {
  const { visitante, carregando } = useVisitante()

  if (carregando) return <div style={{ padding: 32 }}>Carregando…</div>
  if (!visitante) return <CadastroVisitante />

  return (
    <div className="pub-shell">
      <header className="app-header">
        <MarcaPortal />
        <div className="app-header-user">
          <span className="pub-selo">Consulta pública</span>
          <Link className="app-header-user-enter" to="/login" title="Entrar como membro">
            <LogIn size={16} /> Sou membro
          </Link>
        </div>
      </header>

      <nav className="pub-nav">
        <NavLink end to={BASE_PUBLICA} className={({ isActive }) => `pub-nav-item${isActive ? ' active' : ''}`}>
          <Library size={16} /> Acervo Legal
        </NavLink>
        <NavLink to={`${BASE_PUBLICA}/busca`} className={({ isActive }) => `pub-nav-item${isActive ? ' active' : ''}`}>
          <SearchIcon size={16} /> Busca
        </NavLink>
        <span className="pub-nav-quem">Olá, {visitante.nome}</span>
      </nav>

      <main className="pub-main">
        {/* Sem ScenarioSwitcher: o acervo é o mesmo nos cenários LOB atual e futura
            (states_data.json e organs_detail/ são compartilhados), então escolher
            cenário não mudaria nada nestas telas. */}
        <AcervoBaseProvider base={BASE_PUBLICA}>
          <Routes>
            <Route index element={<Legislations />} />
            <Route path="estados/:stateId" element={<StateDetail />} />
            <Route path="busca" element={<SearchPage />} />
            {/* Endereço fora do recorte dentro do prefixo: devolve ao acervo. */}
            <Route path="*" element={<Navigate to={BASE_PUBLICA} replace />} />
          </Routes>
        </AcervoBaseProvider>
      </main>
    </div>
  )
}
