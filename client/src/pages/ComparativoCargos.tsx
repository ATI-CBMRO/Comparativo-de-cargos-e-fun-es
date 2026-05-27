import { useState, useMemo } from "react";
import { trpc } from "@/lib/trpc";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Users,
  Building2,
  ChevronDown,
  ChevronUp,
  Filter,
  Info,
  GitBranch,
  ClipboardList,
  ArrowUpDown,
  X,
} from "lucide-react";

// ─── Helpers ─────────────────────────────────────────────────────────────────

const CATEGORY_LABELS: Record<string, { label: string; description: string; icon: "co" | "dat" }> = {
  "chefe-co": {
    label: "Chefe do Comando Operacional",
    description: "Titular do órgão de comando operacional (Comandante Operacional, Diretor de Planejamento Operacional, Diretor de Operações, etc.)",
    icon: "co",
  },
  "adjunto-co": {
    label: "Adjunto / Subcomandante Operacional",
    description: "Segundo na hierarquia do comando operacional (Adjunto, Subcomandante, Assistente, etc.)",
    icon: "co",
  },
  "chefe-depto-co": {
    label: "Chefe de Departamento/Centro (CO)",
    description: "Chefe de departamento ou centro subordinado ao Comando Operacional",
    icon: "co",
  },
  "chefe-secao-co": {
    label: "Chefe de Seção (CO)",
    description: "Chefe de seção ou divisão subordinada ao Comando Operacional",
    icon: "co",
  },
  "chefe-dat": {
    label: "Chefe da Diretoria de Atividades Técnicas",
    description: "Titular do órgão técnico (Diretor de Atividades Técnicas, Chefe do CAT, Coordenador de Atividades Técnicas, etc.)",
    icon: "dat",
  },
  "adjunto-dat": {
    label: "Adjunto / Subchefe da DAT",
    description: "Segundo na hierarquia da diretoria técnica (Adjunto, Subchefe, Vice-Diretor, etc.)",
    icon: "dat",
  },
  "chefe-depto-dat": {
    label: "Chefe de Departamento/Divisão (DAT)",
    description: "Chefe de departamento ou divisão subordinado à Diretoria Técnica",
    icon: "dat",
  },
  "chefe-secao-dat": {
    label: "Chefe de Seção/Núcleo (DAT)",
    description: "Chefe de seção, núcleo ou gerência subordinado à Diretoria Técnica",
    icon: "dat",
  },
};

const CATEGORY_GROUPS = [
  {
    group: "Comando Operacional",
    color: "blue",
    categories: ["chefe-co", "adjunto-co", "chefe-depto-co", "chefe-secao-co"],
  },
  {
    group: "Diretoria de Atividades Técnicas",
    color: "red",
    categories: ["chefe-dat", "adjunto-dat", "chefe-depto-dat", "chefe-secao-dat"],
  },
];

const REGION_STATES: Record<string, string[]> = {
  Norte: ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
  Nordeste: ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
  "Centro-Oeste": ["DF", "GO", "MT", "MS"],
  Sudeste: ["ES", "MG", "RJ", "SP"],
  Sul: ["PR", "RS", "SC"],
};

function OrgTypeBadge({ type }: { type: "co" | "dat" }) {
  if (type === "co") {
    return (
      <Badge className="bg-blue-100 text-blue-800 border-blue-200 text-xs font-medium">
        Cmd. Operacional
      </Badge>
    );
  }
  return (
    <Badge className="bg-red-100 text-red-800 border-red-200 text-xs font-medium">
      Dir. Atividades Técnicas
    </Badge>
  );
}

function AttributionList({ text }: { text: string | null | undefined }) {
  if (!text) return <p className="text-muted-foreground text-sm italic">Não especificado</p>;
  const items = text.split(";").map((s) => s.trim()).filter(Boolean);
  if (items.length === 0) return <p className="text-muted-foreground text-sm italic">Não especificado</p>;
  return (
    <ul className="space-y-1">
      {items.map((item, i) => (
        <li key={i} className="flex gap-2 text-sm text-foreground">
          <span className="mt-1.5 h-1.5 w-1.5 rounded-full bg-primary flex-shrink-0" />
          <span>{item}</span>
        </li>
      ))}
    </ul>
  );
}

function SubordinatesList({ text }: { text: string | null | undefined }) {
  if (!text) return <span className="text-muted-foreground text-sm italic">—</span>;
  const items = text.split(";").map((s) => s.trim()).filter(Boolean);
  return (
    <div className="flex flex-wrap gap-1">
      {items.map((item, i) => (
        <Badge key={i} variant="outline" className="text-xs">
          {item}
        </Badge>
      ))}
    </div>
  );
}

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

function PositionCard({
  entry,
  expanded,
  onToggle,
}: {
  entry: PositionEntry;
  expanded: boolean;
  onToggle: () => void;
}) {
  const { position, operationalCommand, technicalDirectorate, state } = entry;
  const orgType = operationalCommand ? "co" : "dat";
  const orgName = operationalCommand
    ? (operationalCommand.acronym ?? operationalCommand.nomenclature)
    : (technicalDirectorate?.acronym ?? technicalDirectorate?.nomenclature ?? "—");

  return (
    <Card className="border border-border shadow-sm hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 flex-wrap mb-1">
              <span className="text-lg font-bold text-foreground">
                {state?.sigla ?? "—"}
              </span>
              <OrgTypeBadge type={orgType} />
            </div>
            <CardTitle className="text-base font-semibold text-foreground leading-tight">
              {position.title}
            </CardTitle>
            {position.acronym && (
              <p className="text-xs text-muted-foreground mt-0.5">({position.acronym})</p>
            )}
          </div>
        </div>

        <div className="mt-2 space-y-1">
          {state && (
            <p className="text-xs text-muted-foreground truncate">{state.corporationName}</p>
          )}
          <p className="text-xs text-muted-foreground">
            <span className="font-medium">Órgão:</span> {orgName}
          </p>
          {position.rank && (
            <p className="text-xs text-muted-foreground">
              <span className="font-medium">Posto/Graduação:</span> {position.rank}
            </p>
          )}
          {position.subordinateTo && (
            <div className="flex items-center gap-1 text-xs text-muted-foreground">
              <ArrowUpDown className="h-3 w-3 flex-shrink-0" />
              <span>
                <span className="font-medium">Subordinado a:</span> {position.subordinateTo}
              </span>
            </div>
          )}
        </div>
      </CardHeader>

      <Separator />

      <CardContent className="pt-3 pb-3">
        <Button
          variant="ghost"
          size="sm"
          className="w-full flex items-center justify-between text-sm font-medium text-primary hover:text-primary"
          onClick={onToggle}
        >
          <span className="flex items-center gap-1.5">
            <ClipboardList className="h-4 w-4" />
            {expanded ? "Ocultar atribuições" : "Ver atribuições"}
          </span>
          {expanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        </Button>

        {expanded && (
          <div className="mt-3 space-y-3">
            {position.subordinates && (
              <div>
                <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1.5 flex items-center gap-1">
                  <GitBranch className="h-3 w-3" /> Subordinados / Desdobramentos
                </p>
                <SubordinatesList text={position.subordinates} />
              </div>
            )}
            <div>
              <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1.5 flex items-center gap-1">
                <ClipboardList className="h-3 w-3" /> Atribuições
              </p>
              <AttributionList text={position.attributions} />
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

// ─── Main Page ────────────────────────────────────────────────────────────────

export default function ComparativoCargos() {
  const [selectedCategory, setSelectedCategory] = useState<string>("");
  const [selectedSiglas, setSelectedSiglas] = useState<string[]>([]);
  const [expandedIds, setExpandedIds] = useState<Set<number>>(new Set());
  const [expandAll, setExpandAll] = useState(false);

  const { data: allStates } = trpc.data.allStates.useQuery();

  const { data: results, isLoading } = trpc.data.comparePositions.useQuery(
    { category: selectedCategory, siglas: selectedSiglas.length > 0 ? selectedSiglas : undefined },
    { enabled: !!selectedCategory }
  );

  const toggleState = (sigla: string) => {
    setSelectedSiglas((prev) =>
      prev.includes(sigla) ? prev.filter((s) => s !== sigla) : [...prev, sigla]
    );
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

  const categoryInfo = selectedCategory ? CATEGORY_LABELS[selectedCategory] : null;

  const availableSiglas = useMemo(() => {
    return allStates?.map((s: { sigla: string }) => s.sigla).sort() ?? [];
  }, [allStates]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
          <Users className="h-6 w-6 text-primary" />
          Comparativo por Cargo
        </h1>
        <p className="text-muted-foreground mt-1">
          Selecione um tipo de cargo para comparar nomenclaturas, subordinações e atribuições entre os estados.
        </p>
      </div>

      {/* Filtros */}
      <Card className="border border-border">
        <CardHeader className="pb-3">
          <CardTitle className="text-base flex items-center gap-2">
            <Filter className="h-4 w-4 text-primary" />
            Filtros de Comparação
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Seleção de categoria */}
          <div>
            <label className="text-sm font-medium text-foreground mb-1.5 block">
              Tipo de Cargo / Função
            </label>
            <div className="space-y-3">
              {CATEGORY_GROUPS.map((group) => (
                <div key={group.group}>
                  <p className={`text-xs font-semibold uppercase tracking-wide mb-2 ${group.color === "blue" ? "text-blue-700" : "text-red-700"}`}>
                    {group.group}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {group.categories.map((cat) => {
                      const info = CATEGORY_LABELS[cat];
                      const isSelected = selectedCategory === cat;
                      return (
                        <button
                          key={cat}
                          onClick={() => {
                            setSelectedCategory(cat);
                            setExpandedIds(new Set());
                            setExpandAll(false);
                          }}
                          className={`px-3 py-1.5 rounded-full text-sm font-medium border transition-all ${
                            isSelected
                              ? group.color === "blue"
                                ? "bg-blue-600 text-white border-blue-600 shadow-sm"
                                : "bg-red-600 text-white border-red-600 shadow-sm"
                              : "bg-background text-foreground border-border hover:border-primary hover:text-primary"
                          }`}
                        >
                          {info.label}
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Filtro por estado */}
          <div>
            <label className="text-sm font-medium text-foreground mb-1.5 block">
              Filtrar por Estado{" "}
              <span className="text-muted-foreground font-normal">(opcional — sem seleção exibe todos)</span>
            </label>
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
                <X className="h-3 w-3 mr-1" /> Limpar seleção de estados
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Descrição da categoria selecionada */}
      {categoryInfo && (
        <div className="flex items-start gap-2 rounded-lg border border-blue-200 bg-blue-50 px-4 py-3">
          <Info className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
          <div>
            <p className="text-sm font-semibold text-blue-800">{categoryInfo.label}</p>
            <p className="text-sm text-blue-700 mt-0.5">{categoryInfo.description}</p>
          </div>
        </div>
      )}

      {/* Resultados */}
      {!selectedCategory && (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <Users className="h-12 w-12 text-muted-foreground/40 mb-3" />
          <p className="text-muted-foreground font-medium">Selecione um tipo de cargo acima para iniciar a comparação</p>
          <p className="text-sm text-muted-foreground/70 mt-1">
            Os resultados serão exibidos lado a lado para facilitar a comparação entre estados
          </p>
        </div>
      )}

      {selectedCategory && isLoading && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <Skeleton key={i} className="h-48 rounded-lg" />
          ))}
        </div>
      )}

      {selectedCategory && !isLoading && results && (
        <div className="space-y-4">
          {/* Barra de ações */}
          <div className="flex items-center justify-between">
            <p className="text-sm text-muted-foreground">
              <span className="font-semibold text-foreground">{results.length}</span>{" "}
              {results.length === 1 ? "estado encontrado" : "estados encontrados"}
              {selectedSiglas.length > 0 && ` (filtrado por: ${selectedSiglas.join(", ")})`}
            </p>
            {results.length > 0 && (
              <Button variant="outline" size="sm" onClick={handleExpandAll} className="text-xs">
                {expandAll ? (
                  <>
                    <ChevronUp className="h-3 w-3 mr-1" /> Recolher todos
                  </>
                ) : (
                  <>
                    <ChevronDown className="h-3 w-3 mr-1" /> Expandir todos
                  </>
                )}
              </Button>
            )}
          </div>

          {results.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center border border-dashed border-border rounded-lg">
              <Building2 className="h-10 w-10 text-muted-foreground/40 mb-3" />
              <p className="text-muted-foreground font-medium">Nenhum resultado encontrado</p>
              <p className="text-sm text-muted-foreground/70 mt-1">
                Tente ajustar os filtros de estado ou selecionar outra categoria de cargo
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {results.map((entry) => (
                <PositionCard
                  key={entry.position.id}
                  entry={entry as PositionEntry}
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
