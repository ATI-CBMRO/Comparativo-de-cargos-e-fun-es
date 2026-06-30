import { useState, useEffect } from 'react'
import { Routes, Route, NavLink, useLocation } from 'react-router-dom'
import {
  Flame, LayoutDashboard, BookOpen, GitCompare,
  Search, Library, ScrollText, Menu, X, Network, LogOut,
  MessageSquare, ShieldCheck, MessagesSquare, Gavel
} from 'lucide-react'
import Dashboard from './pages/Dashboard.jsx'
import StatesList from './pages/StatesList.jsx'
import StateDetail from './pages/StateDetail.jsx'
import MinutaComparator from './pages/MinutaComparator.jsx'
import SearchPage from './pages/Search.jsx'
import Legislations from './pages/Legislations.jsx'
import MinutaWizard from './pages/MinutaWizard.jsx'
import MinutaDiagrams from './pages/MinutaDiagrams.jsx'
import MinutaRevisao from './pages/MinutaRevisao.jsx'
import MinutaDeliberacao from './pages/MinutaDeliberacao.jsx'
import Login from './pages/Login.jsx'
import Cadastro from './pages/Cadastro.jsx'
import Revisao from './pages/Revisao.jsx'
import Acessos from './pages/Acessos.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import { useAuth } from './lib/auth.jsx'

const NAV = [
  { to: '/', icon: LayoutDashboard, label: 'Início', end: true },
  { to: '/estados', icon: BookOpen, label: 'Estados' },
  { to: '/comparar', icon: GitCompare, label: 'Subsídio à Minuta' },
  { to: '/minuta', icon: ScrollText, label: 'Minuta RI' },
  { to: '/minuta-diagramas', icon: Network, label: 'Diagramas da Minuta' },
  { to: '/minuta/revisao', icon: MessagesSquare, label: 'Revisão CONDEG' },
  { to: '/minuta/deliberacao', icon: Gavel, label: 'Deliberação CONDEG' },
  { to: '/legislacoes', icon: Library, label: 'Acervo Legal' },
  { to: '/busca', icon: Search, label: 'Busca Textual' },
]

function Header({ navOpen, onToggleNav }) {
  return (
    <header className="app-header">
      <button
        type="button"
        className="app-header-burger"
        onClick={onToggleNav}
        aria-label={navOpen ? 'Fechar navegação' : 'Abrir navegação'}
        aria-expanded={navOpen}
        aria-controls="sidebar-nav"
      >
        {navOpen ? <X size={22} /> : <Menu size={22} />}
      </button>
      <img
        className="app-header-emblem"
        src="/BrasaoCBMRO2D-COMPLETO.png"
        onError={e => { if (!e.currentTarget.dataset.fb) { e.currentTarget.dataset.fb = '1'; e.currentTarget.src = '/brasao-cbmro.svg' } }}
        alt="Brasão do Corpo de Bombeiros Militar de Rondônia"
      />
      <div className="app-header-text">
        <h1 className="app-header-title">
          Portal de Legislação dos Corpos de Bombeiros Militares
        </h1>
        <div className="app-header-rule" />
        <div className="app-header-sub">
          Corpo de Bombeiros Militar de Rondônia · CBMRO
        </div>
      </div>
      <HeaderUserBox />
    </header>
  )
}

function HeaderUserBox() {
  const { user, sair } = useAuth()
  if (!user) return null
  return (
    <div className="app-header-user">
      <span className="app-header-user-name">{user.nome}</span>
      <button type="button" className="app-header-user-exit" onClick={sair} title="Sair">
        <LogOut size={16} /> Sair
      </button>
    </div>
  )
}

function Sidebar({ open, collapsed, onNavigate, onToggleCollapse }) {
  const { user } = useAuth()
  return (
    <aside id="sidebar-nav" className={`sidebar${open ? ' open' : ''}`}>
      <button
        type="button"
        className="sidebar-logo"
        onClick={onToggleCollapse}
        aria-expanded={!collapsed}
        title={collapsed ? 'Expandir navegação' : 'Recolher navegação'}
      >
        <div className="sidebar-logo-icon">
          <Flame size={20} color="#fff" strokeWidth={2.5} />
        </div>
        <div className="sidebar-logo-text">
          <strong>Portal CBM</strong>
          <span>Legislação Comparada</span>
        </div>
      </button>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Navegação</div>
        {NAV.map(({ to, icon: Icon, label, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            onClick={onNavigate}
            title={label}
            className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
          >
            <Icon className="nav-icon" size={18} />
            <span className="nav-item-label">{label}</span>
          </NavLink>
        ))}

        {user && (
          <NavLink to="/revisao" onClick={onNavigate} title="Revisão"
            className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}>
            <MessageSquare className="nav-icon" size={18} />
            <span className="nav-item-label">Revisão</span>
          </NavLink>
        )}
        {user?.role === 'admin' && (
          <NavLink to="/acessos" onClick={onNavigate} title="Acessos"
            className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}>
            <ShieldCheck className="nav-icon" size={18} />
            <span className="nav-item-label">Acessos</span>
          </NavLink>
        )}
      </nav>

      <div className="sidebar-footer">
        <p className="sidebar-footer-text">
          Dados das legislações oficiais<br />
          <span style={{ color: '#4a5680' }}>Atualizado em junho/2026</span>
        </p>
      </div>
    </aside>
  )
}

export default function App() {
  const [navOpen, setNavOpen] = useState(false)      // gaveta mobile (≤900px)
  const [collapsed, setCollapsed] = useState(false)  // trilha de ícones (desktop)
  const location = useLocation()

  // Fecha a navegação ao mudar de rota (ex.: clique num item no mobile).
  useEffect(() => { setNavOpen(false) }, [location.pathname])

  // Clicar numa aba: navega, fecha a gaveta mobile e recolhe a barra no desktop.
  const handleNavigate = () => { setNavOpen(false); setCollapsed(true) }

  return (
    <div className={`app-shell${collapsed ? ' nav-collapsed' : ''}`}>
      <Header navOpen={navOpen} onToggleNav={() => setNavOpen(o => !o)} />
      <Sidebar
        open={navOpen}
        collapsed={collapsed}
        onNavigate={handleNavigate}
        onToggleCollapse={() => setCollapsed(c => !c)}
      />
      <div
        className={`sidebar-backdrop${navOpen ? ' show' : ''}`}
        onClick={() => setNavOpen(false)}
        aria-hidden="true"
      />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/estados" element={<StatesList />} />
          <Route path="/estados/:stateId" element={<StateDetail />} />
          <Route path="/legislacoes" element={<Legislations />} />
          <Route path="/comparar" element={<MinutaComparator />} />
          <Route path="/busca" element={<SearchPage />} />
          <Route path="/minuta" element={<MinutaWizard />} />
          <Route path="/minuta-diagramas" element={<MinutaDiagrams />} />
          <Route path="/minuta/revisao" element={<MinutaRevisao />} />
          <Route path="/minuta/deliberacao" element={<MinutaDeliberacao />} />
          <Route path="/login" element={<Login />} />
          <Route path="/cadastro" element={<Cadastro />} />
          <Route path="/revisao" element={<ProtectedRoute><Revisao /></ProtectedRoute>} />
          <Route path="/acessos" element={<ProtectedRoute requireAdmin><Acessos /></ProtectedRoute>} />
        </Routes>
      </main>
    </div>
  )
}
