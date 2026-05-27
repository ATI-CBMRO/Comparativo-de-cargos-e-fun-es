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
    <div className="flex h-screen overflow-hidden bg-background">
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
          "fixed inset-y-0 left-0 z-50 flex flex-col transition-all duration-300 lg:relative lg:z-auto",
          "bg-[oklch(0.22_0.10_255)]",
          collapsed ? "w-16" : "w-64",
          mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        )}
      >
        {/* Logo area */}
        <div className="flex items-center gap-3 px-4 py-5 border-b border-[oklch(0.32_0.10_255)]">
          <div className="flex-shrink-0 w-9 h-9 rounded-lg bg-[oklch(0.48_0.22_25)] flex items-center justify-center shadow-md">
            <Flame className="w-5 h-5 text-white" />
          </div>
          {!collapsed && (
            <div className="overflow-hidden">
              <p className="text-white font-display font-bold text-sm leading-tight">
                Portal CBM
              </p>
              <p className="text-[oklch(0.60_0.05_255)] text-xs leading-tight">
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
        <div className="px-2 py-3 border-t border-[oklch(0.32_0.10_255)]">
          <button
            onClick={() => setCollapsed(!collapsed)}
            className={cn(
              "w-full flex items-center gap-2 px-3 py-2 rounded-lg text-[oklch(0.60_0.05_255)] hover:text-white hover:bg-[oklch(0.30_0.10_255)] transition-colors text-sm",
              collapsed && "justify-center"
            )}
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
        {/* Top header */}
        <header className="flex-shrink-0 h-14 bg-white border-b border-border flex items-center gap-4 px-4 lg:px-6">
          <button
            className="lg:hidden p-1.5 rounded-md hover:bg-muted text-muted-foreground"
            onClick={() => setMobileOpen(true)}
          >
            <Menu className="w-5 h-5" />
          </button>

          <div className="flex items-center gap-2 flex-1">
            <div className="section-divider w-1 h-6 rounded-full" />
            <h1 className="font-display font-semibold text-foreground text-base">
              Corpos de Bombeiros Militares — Estrutura Organizacional
            </h1>
          </div>

          <div className="flex items-center gap-2">
            <span className="hidden sm:flex items-center gap-1.5 text-xs text-muted-foreground bg-muted px-2.5 py-1 rounded-full">
              <BarChart3 className="w-3 h-3" />
              19 estados analisados
            </span>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto bg-background">
          {children}
        </main>
      </div>
    </div>
  );
}
