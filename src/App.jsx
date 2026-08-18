import { useState, useEffect } from 'react'
import { Routes, Route, Navigate, NavLink, useLocation } from 'react-router-dom'
import {
  Flame, LayoutDashboard, BookOpen, GitCompare,
  Search, Library, ScrollText, Menu, X, Network, LogOut,
  MessageSquare, ShieldCheck, BookMarked, Scale, GitCompareArrows, ChevronsLeft, GitBranch, ListChecks, ClipboardList
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
import RegulamentoWizard from './pages/RegulamentoWizard.jsx'
import RegulamentoComparator from './pages/RegulamentoComparator.jsx'
import MinutaRIComparator from './pages/MinutaRIComparator.jsx'
import RIComparator from './pages/RIComparator.jsx'
import RISubsidio from './pages/RISubsidio.jsx'
import RegSubsidio from './pages/RegSubsidio.jsx'
import RegDiagramas from './pages/RegDiagramas.jsx'
import ConferenciaLinear from './pages/ConferenciaLinear.jsx'
import DecisoesCuradoria from './pages/DecisoesCuradoria.jsx'
import Manual from './pages/Manual.jsx'
import Organograma from './pages/Organograma.jsx'
import Login from './pages/Login.jsx'
import SolicitarAcesso from './pages/SolicitarAcesso.jsx'
import Revisao from './pages/Revisao.jsx'
import Acessos from './pages/Acessos.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import ScenarioSwitcher from './components/ScenarioSwitcher.jsx'
import EmConstrucao from './components/EmConstrucao.jsx'
import { useAuth } from './lib/auth.jsx'
import { useScenario } from './context/ScenarioContext.jsx'
import { rotaLiberadaNoEscopo } from './lib/escopoServico.js'

// /minuta/revisao e /minuta/deliberacao (protótipo CONDEG em localStorage) saíram do
// menu — a Revisão da Minuta oficial (Firebase, item abaixo) assumiu o papel de produção.
// As rotas continuam acessíveis por URL direta; nada foi apagado (ver CLAUDE.md).
//
// Agrupado em 3 blocos (pedido do Wândrio): itens gerais, e as DUAS trilhas de minuta
// (Regimento Interno e Regulamento Geral) — cada uma com seu comparador + editor,
// para o menu deixar claro que são dois documentos distintos sendo elaborados.
//
// Duas telas de comparação do RI coexistem de propósito (fusão com o master,
// 2026-07-09): "Subsídio ao RI" reusa a MESMA matriz estrutural de
// "Subsídio à Minuta" (comparativo_minuta.json), só filtrada aos estados com RI —
// compara ESTRUTURA/competências. "Comparar Regimento Interno" compara o TEXTO
// verbatim de cada artigo, lado a lado, com selo de correspondência — é o
// equivalente do "Comparar Regulamento" pro RI. Nomes escolhidos pra deixar a
// diferença óbvia no menu.
// As DUAS trilhas de minuta seguem o MESMO pipeline (padrão único): Subsídio →
// Minuta → Diagramas → Revisão. A parte "Geral" fica só com o acervo/corpus,
// comum às duas. O Subsídio de cada trilha reúne os comparadores em abas
// (Estrutura / Texto / LOB). Ver plano seguindo-o-menu-*.md.
const NAV_GROUPS = [
  {
    section: null,
    items: [
      { to: '/legislacoes', icon: Library, label: 'Acervo Legal' },
      { to: '/organograma', icon: GitBranch, label: 'Organograma' },
      { to: '/manual', icon: BookOpen, label: 'Manual de uso' },
      { to: '/acessos', icon: ShieldCheck, label: 'Acessos', admin: true },
    ],
  },
  {
    section: 'Regimento Interno',
    items: [
      { to: '/minuta/subsidio', icon: GitCompare, label: 'Subsídio' },
      { to: '/minuta/conferencia', icon: ListChecks, label: 'Conferência' },
      { to: '/minuta/decisoes', icon: ClipboardList, label: 'Decisões' },
      { to: '/minuta', icon: ScrollText, label: 'Minuta do Regimento Interno', end: true },
      { to: '/minuta/diagramas', icon: Network, label: 'Diagramas' },
      { to: '/minuta/revisao', icon: MessageSquare, label: 'Revisão' },
    ],
  },
  {
    section: 'Regulamento Geral',
    items: [
      { to: '/regulamento/subsidio', icon: GitCompare, label: 'Subsídio' },
      { to: '/regulamento/conferencia', icon: ListChecks, label: 'Conferência' },
      { to: '/regulamento/decisoes', icon: ClipboardList, label: 'Decisões' },
      { to: '/regulamento', icon: BookMarked, label: 'Minuta do Regulamento Geral', end: true },
      { to: '/regulamento/diagramas', icon: Network, label: 'Diagramas' },
      { to: '/regulamento/revisao', icon: MessageSquare, label: 'Revisão' },
    ],
  },
]

// Menu do participante com escopo (spec 2026-08-13): só o que diz respeito a ele.
// ATENÇÃO: isto é simplificação de INTERFACE, não parede — quem digitar /minuta na
// barra de endereço ainda alcança a rota. Segurança de dado é do firestore.rules.
const NAV_ESCOPO = {
  servico: [
    { to: '/regulamento/servico', icon: BookMarked, label: 'Regulamento de Serviço', end: true },
    { to: '/regulamento/servico/subsidio', icon: GitCompare, label: 'Subsídio' },
    { to: '/manual', icon: BookOpen, label: 'Manual de uso' },
  ],
}

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
  // O cabeçalho só é renderizado com o usuário autenticado (ver App()); sem login,
  // o portal inteiro mostra apenas as telas de login/solicitar-acesso.
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
  const itensEscopo = NAV_ESCOPO[user?.escopo] ?? null
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

      {/* Participante com escopo não escolhe cenário: a rota já o trava em "atual". */}
      {!itensEscopo && <ScenarioSwitcher />}

      <nav className="sidebar-nav">
        <div className="nav-section-label">Navegação</div>
        {itensEscopo
          ? (
            <div className="nav-group">
              {itensEscopo.map(({ to, icon: Icon, label, end }) => (
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
            </div>
          )
          : NAV_GROUPS.map((group, gi) => (
          <div key={group.section ?? `g${gi}`} className="nav-group">
            {group.section && <div className="nav-section-label nav-section-label-sub">{group.section}</div>}
            {group.items
              .filter(it => !it.admin || user?.role === 'admin')
              .map(({ to, icon: Icon, label, end }) => (
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
          </div>
        ))}
        {/* "Acessos" (admin) e "Revisão" agora vivem dentro dos grupos — a
            Revisão em cada trilha, Acessos na parte Geral. */}
      </nav>

      <div className="sidebar-footer">
        <button
          type="button"
          className="sidebar-collapse-btn"
          onClick={onToggleCollapse}
          title={collapsed ? 'Expandir menu' : 'Recolher menu'}
          aria-label={collapsed ? 'Expandir menu' : 'Recolher menu'}
        >
          <ChevronsLeft className={`sidebar-collapse-ico${collapsed ? ' is-collapsed' : ''}`} size={18} />
          <span className="sidebar-collapse-label">Recolher menu</span>
        </button>
        <p className="sidebar-footer-text">
          Dados das legislações oficiais<br />
          <span style={{ color: 'var(--navy-500)' }}>Atualizado em junho/2026</span>
        </p>
      </div>
    </aside>
  )
}

function FullPageLoading() {
  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="spinner" />
    </div>
  )
}

// Usuário já autenticado que chega em /login ou /solicitar-acesso (link antigo, aba
// duplicada etc.): manda de volta ao destino original que ele tentou acessar antes do login
// (guardado em location.state.from pelo LoggedOutRoutes), ou para o Início.
// Páginas das trilhas (Regimento Interno / Regulamento Geral) só têm conteúdo na LOB
// futura por enquanto. No cenário "atual", mostram o placeholder — nada de dados se mistura.
function TrilhaRoute({ children }) {
  const { cenario } = useScenario()
  return cenario === 'atual' ? <EmConstrucao /> : children
}

function AlreadyLoggedInRedirect() {
  const location = useLocation()
  return <Navigate to={location.state?.from || '/'} replace />
}

// Rota do Regulamento de Serviço (recorte setorizado). Trava o cenário em "atual": a
// LOB vigente é a que este regulamento regulamenta, e comentário de um cenário NUNCA
// aparece no outro — deixar no padrão "futura" gravaria a manifestação no lugar errado,
// em silêncio.
function RegulamentoServicoRoute() {
  const { cenario, setCenario } = useScenario()
  useEffect(() => {
    if (cenario !== 'atual') setCenario('atual')
  }, [cenario, setCenario])
  return <Revisao initialDoc="reg" escopo="servico" />
}

// Subsídio (comparação com os demais estados) do mesmo recorte de Serviço — mesma trava
// de cenário do documento principal, mesmos 7 temas.
function RegulamentoServicoSubsidioRoute() {
  const { cenario, setCenario } = useScenario()
  useEffect(() => {
    if (cenario !== 'atual') setCenario('atual')
  }, [cenario, setCenario])
  return <RegSubsidio escopo="servico" />
}

// Quem tem escopo não cai no Acervo dos 27 estados: vai direto ao documento dele.
function InicioPorEscopo() {
  const { user } = useAuth()
  const destino = user?.escopo === 'servico' ? '/regulamento/servico' : '/legislacoes'
  return <Navigate to={destino} replace />
}

// Devolve o participante com escopo ao documento dele quando ele alcança uma rota fora do
// recorte (link antigo, endereço digitado, aba salva). Sem escopo, é no-op absoluto.
function GuardaDeEscopo({ children }) {
  const { user } = useAuth()
  const { pathname } = useLocation()
  if (user?.escopo && !rotaLiberadaNoEscopo(pathname, user.escopo)) {
    return <Navigate to="/regulamento/servico" replace />
  }
  return children
}

// Portal inteiro exige login: sem sessão válida, só /login e /solicitar-acesso respondem —
// qualquer outra URL redireciona para /login guardando o destino pedido, para retomá-lo
// assim que a pessoa autenticar. Não há mais cadastro manual por e-mail (Acessos só
// aprova/gerencia quem já pediu acesso pelo formulário público).
function LoggedOutRoutes() {
  const location = useLocation()
  const from = `${location.pathname}${location.search}`
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/solicitar-acesso" element={<SolicitarAcesso />} />
      <Route path="*" element={<Navigate to="/login" replace state={{ from }} />} />
    </Routes>
  )
}

export default function App() {
  const { user, loading } = useAuth()
  const [navOpen, setNavOpen] = useState(false)      // gaveta mobile (≤900px)
  const [collapsed, setCollapsed] = useState(false)  // trilha de ícones (desktop) — expandida por padrão
  const location = useLocation()

  // Fecha a navegação ao mudar de rota (ex.: clique num item no mobile).
  useEffect(() => { setNavOpen(false) }, [location.pathname])

  // Clicar numa aba: navega e fecha a gaveta mobile. NÃO recolhe a barra no
  // desktop — o recolhimento só acontece pelo botão de recolher.
  const handleNavigate = () => { setNavOpen(false) }

  // Evita "piscar" a tela de login enquanto o Firebase ainda resolve a sessão.
  if (loading) return <FullPageLoading />
  if (!user) return <LoggedOutRoutes />

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
        <GuardaDeEscopo>
        <Routes>
          {/* Início saiu do menu — a home passa a ser o Acervo (ou o Regulamento de
              Serviço, para quem tem escopo). */}
          <Route path="/" element={<InicioPorEscopo />} />
          <Route path="/legislacoes" element={<Legislations />} />
          <Route path="/manual" element={<Manual />} />
          <Route path="/organograma" element={<Organograma />} />
          {/* Estados saiu do menu; a rota de detalhe continua (aberta pelo Acervo). */}
          <Route path="/estados" element={<StatesList />} />
          <Route path="/estados/:stateId" element={<StateDetail />} />
          <Route path="/busca" element={<SearchPage />} />
          {/* Trilha Regimento Interno (pipeline padrão) */}
          <Route path="/minuta/subsidio" element={<RISubsidio />} />
          <Route path="/minuta/conferencia" element={<ConferenciaLinear trilha="ri" />} />
          <Route path="/minuta/decisoes" element={<DecisoesCuradoria trilha="ri" />} />
          <Route path="/minuta" element={<MinutaWizard />} />
          <Route path="/minuta/diagramas" element={<MinutaDiagrams />} />
          <Route path="/minuta/revisao" element={<ProtectedRoute><Revisao initialDoc="ri" /></ProtectedRoute>} />
          {/* Trilha Regulamento Geral (mesmo pipeline) */}
          <Route path="/regulamento/subsidio" element={<RegSubsidio />} />
          <Route path="/regulamento/conferencia" element={<ConferenciaLinear trilha="reg" />} />
          <Route path="/regulamento/decisoes" element={<DecisoesCuradoria trilha="reg" />} />
          <Route path="/regulamento" element={<RegulamentoWizard />} />
          <Route path="/regulamento/diagramas" element={<RegDiagramas />} />
          <Route path="/regulamento/revisao" element={<ProtectedRoute><Revisao initialDoc="reg" /></ProtectedRoute>} />
          <Route path="/regulamento/servico" element={<ProtectedRoute><RegulamentoServicoRoute /></ProtectedRoute>} />
          <Route path="/regulamento/servico/subsidio" element={<ProtectedRoute><RegulamentoServicoSubsidioRoute /></ProtectedRoute>} />
          {/* Rotas antigas mantidas por compatibilidade (fora do menu) */}
          <Route path="/comparar" element={<TrilhaRoute><MinutaComparator /></TrilhaRoute>} />
          <Route path="/minuta-diagramas" element={<MinutaDiagrams />} />
          <Route path="/minuta/deliberacao" element={<TrilhaRoute><MinutaDeliberacao /></TrilhaRoute>} />
          <Route path="/minuta/comparar" element={<TrilhaRoute><MinutaRIComparator /></TrilhaRoute>} />
          <Route path="/minuta/comparativo-ri" element={<TrilhaRoute><RIComparator /></TrilhaRoute>} />
          <Route path="/regulamento/comparar" element={<TrilhaRoute><RegulamentoComparator /></TrilhaRoute>} />
          <Route path="/login" element={<AlreadyLoggedInRedirect />} />
          {/* /cadastro não existe mais (fluxo manual removido) — link antigo cai aqui em
              vez de página em branco. */}
          <Route path="/cadastro" element={<AlreadyLoggedInRedirect />} />
          <Route path="/solicitar-acesso" element={<AlreadyLoggedInRedirect />} />
          <Route path="/revisao" element={<ProtectedRoute><Revisao /></ProtectedRoute>} />
          <Route path="/acessos" element={<ProtectedRoute requireAdmin><Acessos /></ProtectedRoute>} />
        </Routes>
        </GuardaDeEscopo>
      </main>
    </div>
  )
}
