import { trpc } from "@/lib/trpc";
import { Link } from "wouter";
import {
  BarChart3,
  BookOpen,
  ChevronRight,
  Flame,
  GitCompare,
  List,
  MapPin,
  Shield,
} from "lucide-react";
import DetailLevelBadge from "@/components/DetailLevelBadge";

const regionColors: Record<string, string> = {
  Norte: "bg-[oklch(0.92_0.08_200)] text-[oklch(0.30_0.15_200)]",
  Nordeste: "bg-[oklch(0.95_0.08_75)] text-[oklch(0.40_0.15_75)]",
  "Centro-Oeste": "bg-[oklch(0.92_0.08_145)] text-[oklch(0.30_0.15_145)]",
  Sudeste: "bg-[oklch(0.92_0.08_255)] text-[oklch(0.30_0.12_255)]",
  Sul: "bg-[oklch(0.95_0.06_25)] text-[oklch(0.42_0.15_25)]",
};

export default function Home() {
  const { data: stats, isLoading } = trpc.dashboard.stats.useQuery();
  const { data: states } = trpc.states.list.useQuery();

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-8">
      {/* Hero */}
      <div className="relative overflow-hidden rounded-2xl text-white p-8" style={{background: "oklch(0.20 0.12 264)"}}>
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 right-0 w-96 h-96 rounded-full -translate-y-1/2 translate-x-1/3" style={{background: "oklch(0.44 0.22 22)"}} />
          <div className="absolute bottom-0 left-0 w-64 h-64 rounded-full translate-y-1/2 -translate-x-1/4" style={{background: "oklch(0.44 0.22 22)"}} />
        </div>
        <div className="relative z-10 flex flex-col md:flex-row md:items-center gap-6">
          <div className="flex-shrink-0 w-16 h-16 rounded-2xl flex items-center justify-center shadow-lg" style={{background: "oklch(0.44 0.22 22)"}}>
            <Flame className="w-9 h-9 text-white" />
          </div>
          <div className="flex-1">
            <h1 className="font-display text-2xl md:text-3xl font-bold mb-2">
              Portal de Legislação dos Corpos de Bombeiros Militares
            </h1>
            <p className="text-sm md:text-base max-w-2xl" style={{color: "oklch(0.80 0.04 264)"}}>
              Levantamento comparativo das estruturas organizacionais de Comandos Operacionais
              e Diretorias de Atividades Técnicas de 19 estados brasileiros, com base em
              Leis de Organização Básica, Regimentos Internos e Normas Gerais de Ação.
            </p>
          </div>
          <div className="flex gap-3">
            <Link
              href="/estados"
              className="flex items-center gap-2 text-white px-4 py-2.5 rounded-lg text-sm font-medium transition-colors" style={{background: "oklch(0.44 0.22 22)"}} onMouseEnter={e => (e.currentTarget as HTMLAnchorElement).style.background='oklch(0.36 0.22 22)'} onMouseLeave={e => (e.currentTarget as HTMLAnchorElement).style.background='oklch(0.44 0.22 22)'}
            >
              <List className="w-4 h-4" />
              Ver Estados
            </Link>
            <Link
              href="/comparativo"
              className="flex items-center gap-2 bg-white/10 hover:bg-white/20 text-white px-4 py-2.5 rounded-lg text-sm font-medium transition-colors"
            >
              <GitCompare className="w-4 h-4" />
              Comparar
            </Link>
          </div>
        </div>
      </div>

      {/* Stats cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl p-5 shadow-sm stat-card-blue">
          <div className="flex items-center justify-between mb-3">
            <MapPin className="w-5 h-5" style={{color: "oklch(0.28 0.14 264)"}} />
            <span className="text-xs text-muted-foreground">Total</span>
          </div>
          <p className="text-3xl font-display font-bold" style={{color: "oklch(0.28 0.14 264)"}}>
            {isLoading ? "—" : stats?.totalStates}
          </p>
          <p className="text-sm text-muted-foreground mt-1">Estados analisados</p>
        </div>

        <div className="bg-white rounded-xl p-5 shadow-sm stat-card-red">
          <div className="flex items-center justify-between mb-3">
            <Shield className="w-5 h-5" style={{color: "oklch(0.44 0.22 22)"}} />
            <span className="text-xs text-muted-foreground">Cmd. Operacional</span>
          </div>
          <p className="text-3xl font-display font-bold" style={{color: "oklch(0.44 0.22 22)"}}>
            {isLoading ? "—" : (stats?.operationalCommands?.detalhado ?? 0)}
          </p>
          <p className="text-sm text-muted-foreground mt-1">Com detalhamento completo</p>
        </div>

        <div className="bg-white rounded-xl p-5 shadow-sm stat-card-green">
          <div className="flex items-center justify-between mb-3">
            <BookOpen className="w-5 h-5 text-[oklch(0.45_0.18_145)]" />
            <span className="text-xs text-muted-foreground">Dir. Técnica</span>
          </div>
          <p className="text-3xl font-display font-bold text-[oklch(0.45_0.18_145)]">
            {isLoading ? "—" : (stats?.technicalDirectorates?.detalhado ?? 0)}
          </p>
          <p className="text-sm text-muted-foreground mt-1">Com detalhamento completo</p>
        </div>

        <div className="bg-white rounded-xl p-5 shadow-sm stat-card-gold">
          <div className="flex items-center justify-between mb-3">
            <BarChart3 className="w-5 h-5 text-[oklch(0.60_0.18_75)]" />
            <span className="text-xs text-muted-foreground">Regiões</span>
          </div>
          <p className="text-3xl font-display font-bold text-[oklch(0.60_0.18_75)]">
            {stats?.byRegion?.filter((r) => r.count > 0).length ?? "—"}
          </p>
          <p className="text-sm text-muted-foreground mt-1">Regiões representadas</p>
        </div>
      </div>

      {/* Detail level breakdown */}
      {stats && (
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-1 h-5 rounded" style={{background: "oklch(0.44 0.22 22)"}} />
              <h2 className="font-display font-semibold text-foreground">Comando Operacional</h2>
            </div>
            <div className="space-y-3">
              {[
                { level: "detalhado" as const, count: stats.operationalCommands?.detalhado ?? 0 },
                { level: "moderado" as const, count: stats.operationalCommands?.moderado ?? 0 },
                { level: "basico" as const, count: stats.operationalCommands?.basico ?? 0 },
              ].map(({ level, count }) => (
                <div key={level} className="flex items-center gap-3">
                  <DetailLevelBadge level={level} size="sm" className="w-24 justify-center" />
                  <div className="flex-1 bg-muted rounded-full h-2">
                    <div
                      className="h-2 rounded-full transition-all duration-500"
                      style={{
                        width: `${(count / (stats.totalStates || 1)) * 100}%`,
                        background:
                          level === "detalhado"
                            ? "oklch(0.45 0.18 145)"
                            : level === "moderado"
                            ? "oklch(0.60 0.18 75)"
                            : "oklch(0.55 0.15 25)",
                      }}
                    />
                  </div>
                  <span className="text-sm font-medium text-foreground w-6 text-right">{count}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-1 h-5 rounded" style={{background: "oklch(0.28 0.14 264)"}} />
              <h2 className="font-display font-semibold text-foreground">Diretoria de Atividades Técnicas</h2>
            </div>
            <div className="space-y-3">
              {[
                { level: "detalhado" as const, count: stats.technicalDirectorates?.detalhado ?? 0 },
                { level: "moderado" as const, count: stats.technicalDirectorates?.moderado ?? 0 },
                { level: "basico" as const, count: stats.technicalDirectorates?.basico ?? 0 },
              ].map(({ level, count }) => (
                <div key={level} className="flex items-center gap-3">
                  <DetailLevelBadge level={level} size="sm" className="w-24 justify-center" />
                  <div className="flex-1 bg-muted rounded-full h-2">
                    <div
                      className="h-2 rounded-full transition-all duration-500"
                      style={{
                        width: `${(count / (stats.totalStates || 1)) * 100}%`,
                        background:
                          level === "detalhado"
                            ? "oklch(0.45 0.18 145)"
                            : level === "moderado"
                            ? "oklch(0.60 0.18 75)"
                            : "oklch(0.55 0.15 25)",
                      }}
                    />
                  </div>
                  <span className="text-sm font-medium text-foreground w-6 text-right">{count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* States quick access */}
      {states && (
        <div className="bg-white rounded-xl p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <div className="w-1 h-5 rounded" style={{background: "oklch(0.44 0.22 22)"}} />
              <h2 className="font-display font-semibold text-foreground">Estados Analisados</h2>
            </div>
            <Link
              href="/estados"
              className="flex items-center gap-1 text-sm font-medium hover:underline" style={{color: "oklch(0.44 0.22 22)"}} 
            >
              Ver todos <ChevronRight className="w-4 h-4" />
            </Link>
          </div>
          <div className="flex flex-wrap gap-2">
            {states.map((state) => (
              <Link
                key={state.sigla}
                href={`/estado/${state.sigla}`}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-muted hover:bg-accent hover:text-accent-foreground transition-colors text-sm font-medium text-foreground"
              >
                <span
                  className={`text-xs px-1.5 py-0.5 rounded font-bold ${
                    regionColors[state.region] ?? "bg-muted text-muted-foreground"
                  }`}
                >
                  {state.sigla}
                </span>
                {state.name}
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Quick actions */}
      <div className="grid sm:grid-cols-2 gap-4">
        <Link
          href="/estados"
          className="group flex items-center gap-4 bg-white rounded-xl p-5 shadow-sm hover:shadow-md transition-all border border-transparent" style={{borderColor: 'transparent'}} onMouseEnter={e => (e.currentTarget as HTMLAnchorElement).style.borderColor='oklch(0.44 0.22 22 / 0.2)'} onMouseLeave={e => (e.currentTarget as HTMLAnchorElement).style.borderColor='transparent'}
        >
          <div className="w-12 h-12 rounded-xl flex items-center justify-center transition-colors" style={{background: "oklch(0.94 0.04 22)"}}>
            <List className="w-6 h-6 transition-colors" style={{color: "oklch(0.44 0.22 22)"}} />
          </div>
          <div>
            <p className="font-display font-semibold text-foreground">Consultar Estados</p>
            <p className="text-sm text-muted-foreground">Filtre e pesquise por estado, órgão ou nível</p>
          </div>
          <ChevronRight className="w-5 h-5 text-muted-foreground ml-auto transition-colors" />
        </Link>

        <Link
          href="/comparativo"
          className="group flex items-center gap-4 bg-white rounded-xl p-5 shadow-sm hover:shadow-md transition-all border border-transparent" style={{borderColor: 'transparent'}} onMouseEnter={e => (e.currentTarget as HTMLAnchorElement).style.borderColor='oklch(0.28 0.14 264 / 0.2)'} onMouseLeave={e => (e.currentTarget as HTMLAnchorElement).style.borderColor='transparent'}
        >
          <div className="w-12 h-12 rounded-xl flex items-center justify-center transition-colors" style={{background: "oklch(0.92 0.06 264)"}}>
            <GitCompare className="w-6 h-6 transition-colors" style={{color: "oklch(0.28 0.14 264)"}} />
          </div>
          <div>
            <p className="font-display font-semibold text-foreground">Comparar Estados</p>
            <p className="text-sm text-muted-foreground">Visualize lado a lado as estruturas de diferentes estados</p>
          </div>
          <ChevronRight className="w-5 h-5 text-muted-foreground ml-auto transition-colors" />
        </Link>
      </div>
    </div>
  );
}
