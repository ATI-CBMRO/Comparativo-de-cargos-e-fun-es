import { Routes, Route, NavLink } from 'react-router-dom'
import {
  Flame, LayoutDashboard, BookOpen, GitCompare,
  Search, Shield, FileText, Award, Library, ScrollText
} from 'lucide-react'
import Dashboard from './pages/Dashboard.jsx'
import StatesList from './pages/StatesList.jsx'
import StateDetail from './pages/StateDetail.jsx'
import MinutaComparator from './pages/MinutaComparator.jsx'
import SearchPage from './pages/Search.jsx'
import Legislations from './pages/Legislations.jsx'
import MinutaWizard from './pages/MinutaWizard.jsx'

const NAV = [
  { to: '/', icon: LayoutDashboard, label: 'Início', end: true },
  { to: '/estados', icon: BookOpen, label: 'Estados' },
  { to: '/legislacoes', icon: Library, label: 'Acervo Legal' },
  { to: '/comparar', icon: GitCompare, label: 'Subsídio à Minuta' },
  { to: '/busca', icon: Search, label: 'Busca Textual' },
  { to: '/minuta', icon: ScrollText, label: 'Minuta RI' },
]

function Header() {
  return (
    <header className="app-header">
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
    </header>
  )
}

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">
          <Flame size={20} color="#fff" strokeWidth={2.5} />
        </div>
        <div className="sidebar-logo-text">
          <strong>Portal CBM</strong>
          <span>Legislação Comparada</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <div className="nav-section-label">Navegação</div>
        {NAV.map(({ to, icon: Icon, label, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
          >
            <Icon className="nav-icon" size={18} />
            {label}
          </NavLink>
        ))}

        <div className="nav-section-label" style={{ marginTop: 8 }}>Referência</div>
        <div className="nav-item" style={{ cursor: 'default', opacity: 0.7 }}>
          <Shield className="nav-icon" size={18} />
          27 CBMs mapeados
        </div>
        <div className="nav-item" style={{ cursor: 'default', opacity: 0.7 }}>
          <FileText className="nav-icon" size={18} />
          37 documentos legais
        </div>
        <div className="nav-item" style={{ cursor: 'default', opacity: 0.7 }}>
          <Award className="nav-icon" size={18} />
          Detalhamento por órgão
        </div>
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
  return (
    <div className="app-shell">
      <Header />
      <Sidebar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/estados" element={<StatesList />} />
          <Route path="/estados/:stateId" element={<StateDetail />} />
          <Route path="/legislacoes" element={<Legislations />} />
          <Route path="/comparar" element={<MinutaComparator />} />
          <Route path="/busca" element={<SearchPage />} />
          <Route path="/minuta" element={<MinutaWizard />} />
        </Routes>
      </main>
    </div>
  )
}
