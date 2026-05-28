import { useState, useMemo } from "react";
import { trpc } from "@/lib/trpc";
import { usePDFExport } from "@/hooks/usePDFExport";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Users,
  ChevronDown,
  ChevronUp,
  GitBranch,
  ClipboardList,
  ArrowUpDown,
  X,
  Shield,
  FlameKindling,
  FileDown,
  Loader2,
} from "lucide-react";

// ─── Tipos ────────────────────────────────────────────────────────────────────

type FilterType = "chefe-co" | "chefe-dat";

type PositionEntry = {
  position: {
    id: number;
    title: string;
    acronym: string | null;
    rank: string | null;
    subordinateTo: string | null;
    subordinates: string | null;
    attributions: string | null;
    positionCategory: string | null;
  };
  operationalCommand: { nomenclature: string; acronym: string | null } | null;
  technicalDirectorate: { nomenclature: string; acronym: string | null } | null;
  state: { id: number; name: string; sigla: string; corporationName: string } | null;
};

// ─── Helpers ─────────────────────────────────────────────────────────────────

const REGION_STATES: Record<string, string[]> = {
  Norte: ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
  Nordeste: ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
  "Centro-Oeste": ["DF", "GO", "MT", "MS"],
  Sudeste: ["ES", "MG", "RJ", "SP"],
  Sul: ["PR", "RS", "SC"],
};

function parseListContent(text: string): string[] {
  try {
    const parsed = JSON.parse(text);
    if (Array.isArray(parsed)) return parsed.map((s: unknown) => String(s).trim()).filter(Boolean);
  } catch { /* not JSON */ }
  return text.split(";").map((s) => s.trim()).filter(Boolean);
}

function AttributionList({ text }: { text: string | null | undefined }) {
  if (!text) return <p className="text-muted-foreground text-sm italic">Não especificado na legislação</p>;
  const items = parseListContent(text);
  if (items.length === 0) return <p className="text-muted-foreground text-sm italic">Não especificado na legislação</p>;
  return (
    <ul className="space-y-1.5">
      {items.map((item, i) => (
        <li key={i} className="flex gap-2 text-sm text-foreground leading-snug">
          <span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-primary flex-shrink-0" />
          <span>{item}</span>
        </li>
      ))}
    </ul>
  );
}

function SubdivisionsList({ text }: { text: string | null | undefined }) {
  if (!text) return <span className="text-muted-foreground text-sm italic">—</span>;
  const items = parseListContent(text);
  if (items.length === 0) return <span className="text-muted-foreground text-sm italic">—</span>;
  return (
    <div className="flex flex-wrap gap-1.5">
      {items.map((item, i) => (
        <Badge key={i} variant="outline" className="text-xs font-normal">
          {item}
        </Badge>
      ))}
    </div>
  );
}

function PositionCard({
  entry,
  filterType,
  expanded,
  onToggle,
}: {
  entry: PositionEntry;
  filterType: FilterType;
  expanded: boolean;
  onToggle: () => void;
}) {
  const { position, operationalCommand, technicalDirectorate, state } = entry;
  const isOp = filterType === "chefe-co";

  const orgName = isOp
    ? (operationalCommand?.nomenclature ?? "—")
    : (technicalDirectorate?.nomenclature ?? "—");

  const orgAcronym = isOp
    ? operationalCommand?.acronym
    : technicalDirectorate?.acronym;

  const accentColor = isOp
    ? "border-l-blue-600 bg-blue-50/30"
    : "border-l-red-600 bg-red-50/30";

  const badgeClass = isOp
    ? "bg-blue-100 text-blue-800 border-blue-200"
    : "bg-red-100 text-red-800 border-red-200";

  return (
    <Card className={`border border-border border-l-4 ${accentColor} shadow-sm hover:shadow-md transition-shadow`}>
      <CardHeader className="pb-2 pt-4 px-4">
        {/* Estado */}
        <div className="flex items-start justify-between gap-2 mb-2">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-black text-foreground tracking-tight">{state?.sigla ?? "—"}</span>
            <div>
              <p className="text-xs font-medium text-foreground leading-tight">{state?.name}</p>
              <p className="text-xs text-muted-foreground leading-tight truncate max-w-[180px]">{state?.corporationName}</p>
            </div>
          </div>
        </div>

        {/* Cargo */}
        <div className="space-y-1">
          <p className="text-sm font-bold text-foreground leading-tight">{position.title}</p>
          {position.acronym && (
            <Badge className={`text-xs font-semibold ${badgeClass}`}>{position.acronym}</Badge>
          )}
        </div>

        {/* Órgão */}
        <div className="mt-2 pt-2 border-t border-border/60 space-y-1">
          <p className="text-xs text-muted-foreground">
            <span className="font-semibold text-foreground">Órgão:</span>{" "}
            {orgName}{orgAcronym ? ` (${orgAcronym})` : ""}
          </p>
          {position.rank && (
            <p className="text-xs text-muted-foreground">
              <span className="font-semibold text-foreground">Posto/Graduação:</span> {position.rank}
            </p>
          )}
          {position.subordinateTo && (
            <div className="flex items-start gap-1 text-xs text-muted-foreground">
              <ArrowUpDown className="h-3 w-3 mt-0.5 flex-shrink-0 text-primary" />
              <span>
                <span className="font-semibold text-foreground">Subordinado a:</span>{" "}
                {position.subordinateTo}
              </span>
            </div>
          )}
        </div>
      </CardHeader>

      <Separator />

      <CardContent className="px-4 pt-3 pb-3">
        {/* Subdivisões sempre visíveis */}
        {position.subordinates && (
          <div className="mb-3">
            <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1.5 flex items-center gap-1">
              <GitBranch className="h-3 w-3" /> Subdivisões / Desdobramentos
            </p>
            <SubdivisionsList text={position.subordinates} />
          </div>
        )}

        {/* Toggle atribuições */}
        <Button
          variant="ghost"
          size="sm"
          className="w-full flex items-center justify-between text-xs font-medium text-primary hover:text-primary h-7 px-0"
          onClick={onToggle}
        >
          <span className="flex items-center gap-1.5">
            <ClipboardList className="h-3.5 w-3.5" />
            {expanded ? "Ocultar atribuições" : "Ver atribuições completas"}
          </span>
          {expanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
        </Button>

        {expanded && (
          <div className="mt-2 pt-2 border-t border-border/40">
            <AttributionList text={position.attributions} />
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// ─── Página Principal ─────────────────────────────────────────────────────────

export default function ComparativoCargos() {
  const [activeFilter, setActiveFilter] = useState<FilterType | null>(null);
  const [selectedSiglas, setSelectedSiglas] = useState<string[]>([]);
  const [expandedIds, setExpandedIds] = useState<Set<number>>(new Set());
  const [expandAll, setExpandAll] = useState(false);

  const { data: allStates } = trpc.data.allStates.useQuery();

  const { data: results, isLoading } = trpc.data.comparePositions.useQuery(
    {
      category: activeFilter ?? "chefe-co",
      siglas: selectedSiglas.length > 0 ? selectedSiglas : undefined,
    },
    { enabled: !!activeFilter }
  );

  const toggleState = (sigla: string) => {
    setSelectedSiglas((prev) =>
      prev.includes(sigla) ? prev.filter((s) => s !== sigla) : [...prev, sigla]
    );
  };

  const handleFilter = (f: FilterType) => {
    setActiveFilter(f);
    setExpandedIds(new Set());
    setExpandAll(false);
  };

  const toggleExpanded = (id: number) => {
    setExpandedIds((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const handleExpandAll = () => {
    if (!results) return;
    if (expandAll) {
      setExpandedIds(new Set());
      setExpandAll(false);
    } else {
      setExpandedIds(new Set(results.map((r) => r.position.id)));
      setExpandAll(true);
    }
  };

  const availableSiglas = useMemo(
    () => allStates?.map((s: { sigla: string }) => s.sigla).sort() ?? [],
    [allStates]
  );

  const { exportPositionsPDF, isExporting } = usePDFExport();

  const handleExportPDF = () => {
    if (!activeFilter) return;
    exportPositionsPDF(
      activeFilter,
      selectedSiglas,
      {
        filename: `comparativo-cargos-${activeFilter}.pdf`,
      }
    );
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
          <Users className="h-6 w-6 text-primary" />
          Comparativo de Cargos e Funções
        </h1>
        <p className="text-muted-foreground mt-1">
          Compare o titular do órgão operacional ou técnico entre os estados, com suas subordinações,
          desdobramentos e atribuições conforme a legislação de cada Corpo de Bombeiros.
        </p>
      </div>

      {/* Dois filtros fixos */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {/* Filtro 1 — Chefe do Órgão Operacional */}
        <button
          onClick={() => handleFilter("chefe-co")}
          className={`relative rounded-xl border-2 p-5 text-left transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-primary ${
            activeFilter === "chefe-co"
              ? "border-blue-600 bg-blue-50 shadow-md"
              : "border-border bg-card hover:border-blue-300 hover:bg-blue-50/40"
          }`}
        >
          <div className="flex items-start gap-3">
            <div className={`rounded-lg p-2 ${activeFilter === "chefe-co" ? "bg-blue-600" : "bg-blue-100"}`}>
              <Shield className={`h-5 w-5 ${activeFilter === "chefe-co" ? "text-white" : "text-blue-600"}`} />
            </div>
            <div>
              <p className={`font-bold text-base leading-tight ${activeFilter === "chefe-co" ? "text-blue-800" : "text-foreground"}`}>
                Chefe do Órgão Operacional
              </p>
              <p className="text-xs text-muted-foreground mt-1 leading-snug">
                Comandante Operacional, Diretor de Planejamento Operacional, Coordenador Operacional, etc.
              </p>
            </div>
          </div>
          {activeFilter === "chefe-co" && (
            <span className="absolute top-3 right-3 h-2.5 w-2.5 rounded-full bg-blue-600 animate-pulse" />
          )}
        </button>

        {/* Filtro 2 — Chefe do Órgão Técnico */}
        <button
          onClick={() => handleFilter("chefe-dat")}
          className={`relative rounded-xl border-2 p-5 text-left transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-primary ${
            activeFilter === "chefe-dat"
              ? "border-red-600 bg-red-50 shadow-md"
              : "border-border bg-card hover:border-red-300 hover:bg-red-50/40"
          }`}
        >
          <div className="flex items-start gap-3">
            <div className={`rounded-lg p-2 ${activeFilter === "chefe-dat" ? "bg-red-600" : "bg-red-100"}`}>
              <FlameKindling className={`h-5 w-5 ${activeFilter === "chefe-dat" ? "text-white" : "text-red-600"}`} />
            </div>
            <div>
              <p className={`font-bold text-base leading-tight ${activeFilter === "chefe-dat" ? "text-red-800" : "text-foreground"}`}>
                Chefe do Órgão Técnico
              </p>
              <p className="text-xs text-muted-foreground mt-1 leading-snug">
                Diretor de Atividades Técnicas, Coordenador de Atividades Técnicas, Comandante de Operações Técnicas, etc.
              </p>
            </div>
          </div>
          {activeFilter === "chefe-dat" && (
            <span className="absolute top-3 right-3 h-2.5 w-2.5 rounded-full bg-red-600 animate-pulse" />
          )}
        </button>
      </div>

      {/* Filtro por estado (opcional) */}
      {activeFilter && (
        <div className="rounded-lg border border-border bg-card p-4">
          <p className="text-sm font-medium text-foreground mb-3">
            Filtrar por Estado{" "}
            <span className="text-muted-foreground font-normal text-xs">(opcional — sem seleção exibe todos os estados)</span>
          </p>
          <div className="space-y-2">
            {Object.entries(REGION_STATES).map(([region, siglas]) => {
              const available = siglas.filter((s) => availableSiglas.includes(s));
              if (available.length === 0) return null;
              return (
                <div key={region} className="flex items-start gap-2">
                  <span className="text-xs text-muted-foreground w-28 pt-1 flex-shrink-0">{region}</span>
                  <div className="flex flex-wrap gap-1.5">
                    {available.map((sigla) => (
                      <button
                        key={sigla}
                        onClick={() => toggleState(sigla)}
                        className={`px-2 py-0.5 rounded text-xs font-mono font-bold border transition-all ${
                          selectedSiglas.includes(sigla)
                            ? "bg-primary text-primary-foreground border-primary"
                            : "bg-background text-foreground border-border hover:border-primary hover:text-primary"
                        }`}
                      >
                        {sigla}
                      </button>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
          {selectedSiglas.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              className="mt-2 h-7 text-xs text-muted-foreground"
              onClick={() => setSelectedSiglas([])}
            >
              <X className="h-3 w-3 mr-1" /> Limpar seleção
            </Button>
          )}
        </div>
      )}

      {/* Estado vazio — nenhum filtro selecionado */}
      {!activeFilter && (
        <div className="flex flex-col items-center justify-center py-20 text-center border border-dashed border-border rounded-xl bg-muted/20">
          <Users className="h-14 w-14 text-muted-foreground/30 mb-4" />
          <p className="text-muted-foreground font-semibold text-lg">Selecione um tipo de cargo acima</p>
          <p className="text-sm text-muted-foreground/70 mt-1 max-w-sm">
            Escolha entre "Chefe do Órgão Operacional" ou "Chefe do Órgão Técnico" para visualizar
            a comparação entre todos os estados
          </p>
        </div>
      )}

      {/* Loading */}
      {activeFilter && isLoading && (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Skeleton key={i} className="h-56 rounded-xl" />
          ))}
        </div>
      )}

      {/* Resultados */}
      {activeFilter && !isLoading && results && (
        <div className="space-y-4">
          {/* Barra de ações */}
          <div className="flex items-center justify-between gap-2 flex-wrap">
            <p className="text-sm text-muted-foreground">
              <span className="font-semibold text-foreground">{results.length}</span>{" "}
              {results.length === 1 ? "estado encontrado" : "estados encontrados"}
              {selectedSiglas.length > 0 && (
                <span className="ml-1 text-xs">(filtrado: {selectedSiglas.join(", ")})</span>
              )}
            </p>
            <div className="flex items-center gap-2">
              {results.length > 0 && (
                <Button variant="outline" size="sm" onClick={handleExpandAll} className="text-xs h-8">
                  {expandAll ? (
                    <><ChevronUp className="h-3 w-3 mr-1" /> Recolher atribuições</>
                  ) : (
                    <><ChevronDown className="h-3 w-3 mr-1" /> Expandir atribuições</>
                  )}
                </Button>
              )}
              {results.length > 0 && (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleExportPDF}
                  disabled={isExporting}
                  className="text-xs h-8 gap-1.5"
                >
                  {isExporting ? (
                    <><Loader2 className="h-3 w-3 animate-spin" /> Gerando PDF...</>
                  ) : (
                    <><FileDown className="h-3 w-3" /> Exportar PDF</>
                  )}
                </Button>
              )}
            </div>
          </div>

          {results.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center border border-dashed border-border rounded-xl">
              <Users className="h-10 w-10 text-muted-foreground/30 mb-3" />
              <p className="text-muted-foreground font-medium">Nenhum resultado encontrado</p>
              <p className="text-sm text-muted-foreground/60 mt-1">Tente ajustar os filtros de estado</p>
            </div>
          ) : (
            <div id="comparativo-cargos-content" className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {results.map((entry) => (
                <PositionCard
                  key={entry.position.id}
                  entry={entry as PositionEntry}
                  filterType={activeFilter}
                  expanded={expandedIds.has(entry.position.id)}
                  onToggle={() => toggleExpanded(entry.position.id)}
                />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
