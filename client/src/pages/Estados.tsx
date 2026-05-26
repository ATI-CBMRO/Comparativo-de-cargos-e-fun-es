import { useState, useMemo } from "react";
import { Link } from "wouter";
import { trpc } from "@/lib/trpc";
import DetailLevelBadge from "@/components/DetailLevelBadge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  ChevronRight,
  Filter,
  Search,
  Shield,
  BookOpen,
  X,
  MapPin,
} from "lucide-react";
import { cn } from "@/lib/utils";

type DetailLevel = "detalhado" | "moderado" | "basico";
type OrgType = "all" | "operational" | "technical";

const REGIONS = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"] as const;
const DETAIL_LEVELS: DetailLevel[] = ["detalhado", "moderado", "basico"];

export default function Estados() {
  const [search, setSearch] = useState("");
  const [selectedRegions, setSelectedRegions] = useState<string[]>([]);
  const [selectedDetailLevels, setSelectedDetailLevels] = useState<DetailLevel[]>([]);
  const [selectedSiglas, setSelectedSiglas] = useState<string[]>([]);
  const [orgType, setOrgType] = useState<OrgType>("all");
  const [showFilters, setShowFilters] = useState(false);

  const { data: states } = trpc.states.list.useQuery();
  const { data: results, isLoading } = trpc.data.filtered.useQuery({
    detailLevel: selectedDetailLevels.length > 0 ? selectedDetailLevels : undefined,
    siglas: selectedSiglas.length > 0 ? selectedSiglas : undefined,
    orgType,
    search: search.trim() || undefined,
  });

  const filteredResults = useMemo(() => {
    if (!results) return [];
    if (selectedRegions.length === 0) return results;
    return results.filter((r) => selectedRegions.includes(r.state.region));
  }, [results, selectedRegions]);

  const toggleRegion = (region: string) => {
    setSelectedRegions((prev) =>
      prev.includes(region) ? prev.filter((r) => r !== region) : [...prev, region]
    );
  };

  const toggleDetailLevel = (level: DetailLevel) => {
    setSelectedDetailLevels((prev) =>
      prev.includes(level) ? prev.filter((l) => l !== level) : [...prev, level]
    );
  };

  const toggleSigla = (sigla: string) => {
    setSelectedSiglas((prev) =>
      prev.includes(sigla) ? prev.filter((s) => s !== sigla) : [...prev, sigla]
    );
  };

  const clearFilters = () => {
    setSearch("");
    setSelectedRegions([]);
    setSelectedDetailLevels([]);
    setSelectedSiglas([]);
    setOrgType("all");
  };

  const hasFilters =
    search ||
    selectedRegions.length > 0 ||
    selectedDetailLevels.length > 0 ||
    selectedSiglas.length > 0 ||
    orgType !== "all";

  return (
    <div className="p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="font-display text-2xl font-bold text-foreground">Estados Analisados</h1>
        <p className="text-muted-foreground text-sm mt-1">
          {filteredResults.length} estado{filteredResults.length !== 1 ? "s" : ""} encontrado
          {filteredResults.length !== 1 ? "s" : ""}
        </p>
      </div>

      {/* Search and filter bar */}
      <div className="bg-white rounded-xl p-4 shadow-sm space-y-4">
        <div className="flex gap-3">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Buscar por nomenclatura, atribuição ou desdobramento..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9"
            />
          </div>
          <Button
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
            className={cn("gap-2", showFilters && "bg-muted")}
          >
            <Filter className="w-4 h-4" />
            Filtros
            {hasFilters && (
              <span className="w-2 h-2 rounded-full bg-[oklch(0.48_0.22_25)]" />
            )}
          </Button>
          {hasFilters && (
            <Button variant="ghost" onClick={clearFilters} className="gap-2 text-muted-foreground">
              <X className="w-4 h-4" />
              Limpar
            </Button>
          )}
        </div>

        {showFilters && (
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 pt-2 border-t border-border">
            {/* Org type filter */}
            <div>
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                Tipo de Órgão
              </p>
              <div className="flex flex-col gap-1.5">
                {[
                  { value: "all" as OrgType, label: "Ambos" },
                  { value: "operational" as OrgType, label: "Comando Operacional" },
                  { value: "technical" as OrgType, label: "Diretoria Técnica" },
                ].map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => setOrgType(opt.value)}
                    className={cn(
                      "text-left px-3 py-1.5 rounded-lg text-sm transition-colors",
                      orgType === opt.value
                        ? "bg-[oklch(0.28_0.12_255)] text-white"
                        : "hover:bg-muted text-foreground"
                    )}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Detail level filter */}
            <div>
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                Nível de Detalhamento
              </p>
              <div className="flex flex-col gap-1.5">
                {DETAIL_LEVELS.map((level) => (
                  <button
                    key={level}
                    onClick={() => toggleDetailLevel(level)}
                    className={cn(
                      "flex items-center gap-2 text-left px-3 py-1.5 rounded-lg text-sm transition-colors",
                      selectedDetailLevels.includes(level)
                        ? "bg-muted ring-1 ring-border"
                        : "hover:bg-muted"
                    )}
                  >
                    <DetailLevelBadge level={level} size="sm" />
                    {selectedDetailLevels.includes(level) && (
                      <X className="w-3 h-3 ml-auto text-muted-foreground" />
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Region filter */}
            <div>
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                Região
              </p>
              <div className="flex flex-col gap-1.5">
                {REGIONS.map((region) => (
                  <button
                    key={region}
                    onClick={() => toggleRegion(region)}
                    className={cn(
                      "flex items-center gap-2 text-left px-3 py-1.5 rounded-lg text-sm transition-colors",
                      selectedRegions.includes(region)
                        ? "bg-[oklch(0.92_0.08_255)] text-[oklch(0.28_0.12_255)] ring-1 ring-[oklch(0.28_0.12_255)]/30"
                        : "hover:bg-muted text-foreground"
                    )}
                  >
                    <MapPin className="w-3.5 h-3.5" />
                    {region}
                  </button>
                ))}
              </div>
            </div>

            {/* State filter */}
            <div>
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-2">
                Estados
              </p>
              <div className="flex flex-col gap-1 max-h-44 overflow-y-auto pr-1">
                {(states ?? []).map((state) => (
                  <button
                    key={state.sigla}
                    onClick={() => toggleSigla(state.sigla)}
                    className={cn(
                      "flex items-center gap-2 text-left px-2 py-1 rounded-lg text-xs transition-colors",
                      selectedSiglas.includes(state.sigla)
                        ? "bg-[oklch(0.92_0.08_25)] text-[oklch(0.40_0.18_25)] ring-1 ring-[oklch(0.48_0.22_25)]/30"
                        : "hover:bg-muted text-foreground"
                    )}
                  >
                    <span className="font-bold w-7 text-[oklch(0.28_0.12_255)]">{state.sigla}</span>
                    <span className="truncate">{state.name}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Results */}
      {isLoading ? (
        <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="bg-white rounded-xl p-5 shadow-sm animate-pulse">
              <div className="h-5 bg-muted rounded w-1/2 mb-3" />
              <div className="h-4 bg-muted rounded w-3/4 mb-2" />
              <div className="h-4 bg-muted rounded w-2/3" />
            </div>
          ))}
        </div>
      ) : filteredResults.length === 0 ? (
        <div className="bg-white rounded-xl p-12 shadow-sm text-center">
          <Search className="w-12 h-12 text-muted-foreground mx-auto mb-4 opacity-50" />
          <p className="font-display font-semibold text-foreground mb-2">Nenhum resultado encontrado</p>
          <p className="text-sm text-muted-foreground">
            Tente ajustar os filtros ou a busca textual.
          </p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-4">
          {filteredResults.map(({ state, operationalCommand, technicalDirectorate }) => (
            <Link
              key={state.sigla}
              href={`/estado/${state.sigla}`}
              className="block bg-white rounded-xl p-5 shadow-sm card-hover cursor-pointer"
            >
              {/* State header */}
              <div className="flex items-start justify-between mb-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-display font-bold text-lg text-[oklch(0.28_0.12_255)]">
                      {state.sigla}
                    </span>
                    <span className="text-xs text-muted-foreground bg-muted px-2 py-0.5 rounded-full">
                      {state.region}
                    </span>
                  </div>
                  <p className="font-semibold text-foreground text-sm">{state.name}</p>
                </div>
                <ChevronRight className="w-5 h-5 text-muted-foreground flex-shrink-0 mt-1" />
              </div>

              {/* Operational Command */}
              {(orgType === "all" || orgType === "operational") && operationalCommand && (
                <div className="mb-3 p-3 rounded-lg bg-[oklch(0.97_0.02_25)]">
                  <div className="flex items-center gap-1.5 mb-1.5">
                    <Shield className="w-3.5 h-3.5 text-[oklch(0.48_0.22_25)]" />
                    <span className="text-xs font-semibold text-[oklch(0.48_0.22_25)] uppercase tracking-wide">
                      Cmd. Operacional
                    </span>
                    <DetailLevelBadge level={operationalCommand.detailLevel} size="sm" className="ml-auto" />
                  </div>
                  <p className="text-xs text-foreground font-medium leading-snug">
                    {operationalCommand.nomenclature}
                  </p>
                  {operationalCommand.acronym && (
                    <p className="text-xs text-muted-foreground mt-0.5">
                      ({operationalCommand.acronym})
                    </p>
                  )}
                </div>
              )}

              {/* Technical Directorate */}
              {(orgType === "all" || orgType === "technical") && technicalDirectorate && (
                <div className="p-3 rounded-lg bg-[oklch(0.97_0.02_255)]">
                  <div className="flex items-center gap-1.5 mb-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-[oklch(0.28_0.12_255)]" />
                    <span className="text-xs font-semibold text-[oklch(0.28_0.12_255)] uppercase tracking-wide">
                      Dir. Técnica
                    </span>
                    <DetailLevelBadge level={technicalDirectorate.detailLevel} size="sm" className="ml-auto" />
                  </div>
                  <p className="text-xs text-foreground font-medium leading-snug">
                    {technicalDirectorate.nomenclature}
                  </p>
                  {technicalDirectorate.acronym && (
                    <p className="text-xs text-muted-foreground mt-0.5">
                      ({technicalDirectorate.acronym})
                    </p>
                  )}
                </div>
              )}

              {orgType === "operational" && !operationalCommand && (
                <p className="text-xs text-muted-foreground italic">
                  Sem dados de Comando Operacional para os filtros selecionados.
                </p>
              )}
              {orgType === "technical" && !technicalDirectorate && (
                <p className="text-xs text-muted-foreground italic">
                  Sem dados de Diretoria Técnica para os filtros selecionados.
                </p>
              )}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
