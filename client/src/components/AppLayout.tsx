import { useState } from "react";
import { Link, useLocation } from "wouter";
import {
  BarChart3,
  BookOpen,
  ChevronLeft,
  ChevronRight,
  Flame,
  GitCompare,
  Home,
  List,
  Menu,
  Users,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/", icon: Home, label: "Início" },
  { href: "/estados", icon: List, label: "Estados" },
  { href: "/comparativo", icon: GitCompare, label: "Comparativo" },
  { href: "/comparativo-cargos", icon: Users, label: "Cargos e Funções" },
  { href: "/sobre", icon: BookOpen, label: "Sobre o Portal" },
];

interface AppLayoutProps {
  children: React.ReactNode;
}

export default function AppLayout({ children }: AppLayoutProps) {
  const [location] = useLocation();
  const [collapsed, setCollapsed] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-background">

      {/* ── Cabeçalho Institucional CBMRO ─────────────────────────────────── */}
      <header
        className="flex-shrink-0 w-full"
        style={{
          background: "linear-gradient(to right, #c8001a 0%, #e8301a 30%, #e8301a 70%, #c8001a 100%)",
          boxShadow: "0 3px 10px rgba(0,0,0,0.3)",
        }}
      >
        <div className="flex items-center justify-between px-4 py-2 gap-4">

          {/* Brasão esquerdo */}
          <img
            src="/manus-storage/brasao-cbmro-oficial_c63237f8.webp"
            alt="Brasão CBMRO"
            style={{
              height: "clamp(56px, 7.5vw, 88px)",
              width: "auto",
              filter: "drop-shadow(0 2px 6px rgba(0,0,0,0.5))",
              flexShrink: 0,
            }}
          />

          {/* Bloco central de texto */}
          <div className="flex flex-col items-center justify-center flex-1">
            <span
              style={{
                color: "#fff",
                fontFamily: "'Josefin Sans', 'Segoe UI', sans-serif",
                fontSize: "clamp(0.72rem, 2vw, 1.1rem)",
                fontWeight: 700,
                textTransform: "uppercase",
                letterSpacing: "2px",
                lineHeight: 1.2,
                textShadow: "1px 1px 4px rgba(0,0,0,0.4)",
                textAlign: "center",
                paddingBottom: "4px",
              }}
            >
              Assessoria Institucional do Corpo de Bombeiros Militar de Rondônia
            </span>

            {/* Divisor azul */}
            <div
              style={{
                width: "80%",
                height: "3px",
                background: "linear-gradient(to right, transparent, #1a3a8f, #3a6abf, #1a3a8f, transparent)",
                margin: "4px 0",
                borderRadius: "2px",
              }}
            />

            {/* Subtítulo */}
            <span
              style={{
                color: "#fff",
                fontFamily: "'Josefin Sans', 'Segoe UI', sans-serif",
                fontSize: "clamp(0.60rem, 1.3vw, 0.82rem)",
                fontWeight: 600,
                textTransform: "uppercase",
                letterSpacing: "2px",
                textShadow: "1px 1px 3px rgba(0,0,0,0.3)",
                textAlign: "center",
                paddingTop: "2px",
              }}
            >
              Corpo de Bombeiros Militar de Rondônia &nbsp;·&nbsp; CBMRO
            </span>
          </div>

        </div>
      </header>

      {/* ── Layout principal (sidebar + conteúdo) ─────────────────────────── */}
      <div className="flex flex-1 min-h-0 overflow-hidden">

        {/* Mobile overlay */}
        {mobileOpen && (
          <div
            className="fixed inset-0 z-40 bg-black/50 lg:hidden"
            onClick={() => setMobileOpen(false)}
          />
        )}

        {/* Sidebar */}
        <aside
          className={cn(
            "fixed top-0 bottom-0 left-0 z-50 flex flex-col transition-all duration-300 lg:relative lg:z-auto lg:top-auto lg:bottom-auto",
            collapsed ? "w-16" : "w-64",
            mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
          )}
          style={{ background: "oklch(0.20 0.12 264)" }}
        >
          {/* Logo area */}
          <div
            className="flex items-center gap-3 px-4 py-4 border-b"
            style={{ borderColor: "oklch(0.30 0.12 264)" }}
          >
            <div
              className="flex-shrink-0 w-9 h-9 rounded-lg flex items-center justify-center shadow-md"
              style={{ background: "oklch(0.44 0.22 22)" }}
            >
              <Flame className="w-5 h-5 text-white" />
            </div>
            {!collapsed && (
              <div className="overflow-hidden">
                <p
                  className="font-bold text-sm leading-tight text-white"
                  style={{ fontFamily: "'Josefin Sans', sans-serif", letterSpacing: "0.05em", textTransform: "uppercase" }}
                >
                  Portal CBM
                </p>
                <p className="text-xs leading-tight" style={{ color: "oklch(0.60 0.05 264)" }}>
                  Legislação Comparada
                </p>
              </div>
            )}
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-2 py-4 space-y-1 overflow-y-auto">
            {navItems.map((item) => {
              const isActive = location === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={cn(
                    "sidebar-nav-item",
                    isActive && "active",
                    collapsed && "justify-center px-2"
                  )}
                  title={collapsed ? item.label : undefined}
                  onClick={() => setMobileOpen(false)}
                >
                  <item.icon className="w-5 h-5 flex-shrink-0" />
                  {!collapsed && <span>{item.label}</span>}
                </Link>
              );
            })}
          </nav>

          {/* Collapse button */}
          <div
            className="px-2 py-3 border-t"
            style={{ borderColor: "oklch(0.30 0.12 264)" }}
          >
            <button
              onClick={() => setCollapsed(!collapsed)}
              className={cn(
                "w-full flex items-center gap-2 px-3 py-2 rounded-lg transition-colors text-sm",
                collapsed && "justify-center"
              )}
              style={{ color: "oklch(0.60 0.05 264)" }}
              onMouseEnter={e => {
                (e.currentTarget as HTMLButtonElement).style.background = "oklch(0.28 0.12 264)";
                (e.currentTarget as HTMLButtonElement).style.color = "#fff";
              }}
              onMouseLeave={e => {
                (e.currentTarget as HTMLButtonElement).style.background = "";
                (e.currentTarget as HTMLButtonElement).style.color = "oklch(0.60 0.05 264)";
              }}
            >
              {collapsed ? (
                <ChevronRight className="w-4 h-4" />
              ) : (
                <>
                  <ChevronLeft className="w-4 h-4" />
                  <span>Recolher</span>
                </>
              )}
            </button>
          </div>
        </aside>

        {/* Main content */}
        <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
          {/* Sub-header com título da seção */}
          <div
            className="flex-shrink-0 min-h-11 bg-white border-b flex items-center gap-4 px-4 lg:px-6 py-2"
            style={{ borderColor: "oklch(0.88 0.006 264)" }}
          >
            <button
              className="lg:hidden p-1.5 rounded-md text-muted-foreground hover:bg-muted flex-shrink-0"
              onClick={() => setMobileOpen(true)}
            >
              <Menu className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-2 flex-1 min-w-0">
              <div
                className="w-1 flex-shrink-0 self-stretch rounded-full"
                style={{ background: "linear-gradient(180deg, oklch(0.44 0.22 22), oklch(0.28 0.14 264))", minHeight: "1.25rem" }}
              />
              <h2
                className="font-semibold text-foreground text-sm leading-snug break-words"
                style={{ fontFamily: "'Josefin Sans', sans-serif", letterSpacing: "0.04em", textTransform: "uppercase" }}
              >
                Corpos de Bombeiros Militares — Estrutura Organizacional
              </h2>
            </div>

            <div className="flex items-center gap-2">
              <span
                className="hidden sm:flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full"
                style={{
                  background: "oklch(0.94 0.006 264)",
                  color: "oklch(0.52 0.02 264)",
                }}
              >
                <BarChart3 className="w-3 h-3" />
                19 estados analisados
              </span>
            </div>
          </div>

          {/* Page content */}
          <main className="flex-1 overflow-y-auto bg-background">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}
