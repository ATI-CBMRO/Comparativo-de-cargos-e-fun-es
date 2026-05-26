import { useState, useMemo } from "react";
import { trpc } from "@/lib/trpc";
import DetailLevelBadge from "@/components/DetailLevelBadge";
import { Button } from "@/components/ui/button";
import {
  BookOpen,
  ChevronRight,
  FileText,
  GitCompare,
  Layers,
  Plus,
  Shield,
  Target,
  Trash2,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";

type DetailLevel = "detalhado" | "moderado" | "basico";

function SubdivisionList({ content }: { content: string | null | undefined }) {
  if (!content) return <p className="text-xs text-muted-foreground italic">Não especificado</p>;
  const items = content.split(";").map((s) => s.trim()).filter(Boolean);
  return (
    <ul className="space-y-1">
      {items.map((item, i) => (
        <li key={i} className="flex items-start gap-1.5 text-xs text-foreground">
          <ChevronRight className="w-3 h-3 text-muted-foreground flex-shrink-0 mt-0.5" />
          {item}
        </li>
      ))}
    </ul>
  );
}

function AttributionList({ content }: { content: string | null | undefined }) {
  if (!content) return <p className="text-xs text-muted-foreground italic">Não especificado</p>;
  const items = content.split(";").map((s) => s.trim()).filter(Boolean);
  return (
    <ul className="space-y-1">
      {items.map((item, i) => (
        <li key={i} className="flex items-start gap-1.5 text-xs text-foreground">
          <span className="w-1.5 h-1.5 rounded-full bg-muted-foreground flex-shrink-0 mt-1.5" />
          {item}
        </li>
      ))}
    </ul>
  );
}

export default function Comparativo() {
  const [selectedSiglas, setSelectedSiglas] = useState<string[]>([]);
  const [showStateSelector, setShowStateSelector] = useState(false);

  const { data: states } = trpc.states.list.useQuery();
  const { data: results, isLoading } = trpc.data.filtered.useQuery(
    { siglas: selectedSiglas, orgType: "all" },
    { enabled: selectedSiglas.length > 0 }
  );

  const addState = (sigla: string) => {
    if (!selectedSiglas.includes(sigla) && selectedSiglas.length < 5) {
      setSelectedSiglas((prev) => [...prev, sigla]);
    }
    setShowStateSelector(false);
  };

  const removeState = (sigla: string) => {
    setSelectedSiglas((prev) => prev.filter((s) => s !== sigla));
  };

  const availableStates = useMemo(
    () => (states ?? []).filter((s) => !selectedSiglas.includes(s.sigla)),
    [states, selectedSiglas]
  );

  const colWidth = selectedSiglas.length <= 2 ? "min-w-[320px]" : "min-w-[280px]";

  return (
    <div className="p-6 max-w-full mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="font-display text-2xl font-bold text-foreground">Comparativo entre Estados</h1>
        <p className="text-muted-foreground text-sm mt-1">
          Selecione até 5 estados para comparar lado a lado suas estruturas organizacionais.
        </p>
      </div>

      {/* State selector */}
      <div className="bg-white rounded-xl p-4 shadow-sm">
        <div className="flex items-center gap-3 flex-wrap">
          {selectedSiglas.map((sigla) => {
            const state = states?.find((s) => s.sigla === sigla);
            return (
              <div
                key={sigla}
                className="flex items-center gap-2 bg-[oklch(0.22_0.10_255)] text-white px-3 py-1.5 rounded-lg text-sm font-medium"
              >
                <span className="font-bold text-[oklch(0.75_0.15_75)]">{sigla}</span>
                <span className="text-[oklch(0.80_0.03_255)]">{state?.name}</span>
                <button
                  onClick={() => removeState(sigla)}
                  className="ml-1 hover:text-[oklch(0.48_0.22_25)] transition-colors"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>
            );
          })}

          {selectedSiglas.length < 5 && (
            <div className="relative">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowStateSelector(!showStateSelector)}
                className="gap-2 border-dashed"
              >
                <Plus className="w-4 h-4" />
                Adicionar estado
              </Button>
              {showStateSelector && (
                <div className="absolute top-full left-0 mt-1 z-50 bg-white border border-border rounded-xl shadow-lg p-2 w-64 max-h-72 overflow-y-auto">
                  {availableStates.length === 0 ? (
                    <p className="text-xs text-muted-foreground p-2">Todos os estados já selecionados.</p>
                  ) : (
                    availableStates.map((state) => (
                      <button
                        key={state.sigla}
                        onClick={() => addState(state.sigla)}
                        className="w-full flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-muted text-sm text-left transition-colors"
                      >
                        <span className="font-bold text-[oklch(0.28_0.12_255)] w-8">{state.sigla}</span>
                        <span className="text-foreground">{state.name}</span>
                      </button>
                    ))
                  )}
                </div>
              )}
            </div>
          )}

          {selectedSiglas.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSelectedSiglas([])}
              className="gap-2 text-muted-foreground ml-auto"
            >
              <Trash2 className="w-4 h-4" />
              Limpar seleção
            </Button>
          )}
        </div>
      </div>

      {/* Empty state */}
      {selectedSiglas.length === 0 && (
        <div className="bg-white rounded-xl p-16 shadow-sm text-center">
          <GitCompare className="w-16 h-16 text-muted-foreground mx-auto mb-4 opacity-30" />
          <p className="font-display font-semibold text-foreground mb-2">Nenhum estado selecionado</p>
          <p className="text-sm text-muted-foreground max-w-sm mx-auto">
            Adicione dois ou mais estados para visualizar a comparação lado a lado das estruturas organizacionais.
          </p>
        </div>
      )}

      {/* Comparison table */}
      {selectedSiglas.length > 0 && (
        <div className="overflow-x-auto">
          {isLoading ? (
            <div className="flex gap-4">
              {selectedSiglas.map((s) => (
                <div key={s} className="min-w-[300px] h-96 bg-muted rounded-xl animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="space-y-6">
              {/* ── Comando Operacional ── */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Shield className="w-5 h-5 text-[oklch(0.48_0.22_25)]" />
                  <h2 className="font-display font-bold text-foreground">Comando Operacional</h2>
                  <div className="flex-1 h-px bg-border" />
                </div>
                <div className="flex gap-4 overflow-x-auto pb-2">
                  {(results ?? []).map(({ state, operationalCommand }) => (
                    <div
                      key={state.sigla}
                      className={cn(
                        "flex-shrink-0 bg-white rounded-xl shadow-sm overflow-hidden",
                        colWidth
                      )}
                      style={{ borderTop: "4px solid oklch(0.48 0.22 25)" }}
                    >
                      {/* Column header */}
                      <div className="p-4 bg-[oklch(0.97_0.02_25)] border-b border-border">
                        <div className="flex items-center justify-between">
                          <span className="font-display font-bold text-[oklch(0.28_0.12_255)] text-lg">
                            {state.sigla}
                          </span>
                          {operationalCommand && (
                            <DetailLevelBadge level={operationalCommand.detailLevel} size="sm" />
                          )}
                        </div>
                        <p className="text-xs text-muted-foreground mt-0.5">{state.name}</p>
                      </div>

                      {operationalCommand ? (
                        <div className="p-4 space-y-4">
                          {/* Nomenclature */}
                          <div>
                            <p className="text-xs font-bold text-[oklch(0.48_0.22_25)] uppercase tracking-wide mb-1">
                              Nomenclatura
                            </p>
                            <p className="text-sm font-semibold text-foreground leading-snug">
                              {operationalCommand.nomenclature}
                            </p>
                            {operationalCommand.acronym && (
                              <p className="text-xs text-muted-foreground">({operationalCommand.acronym})</p>
                            )}
                          </div>

                          {/* Subdivisions */}
                          <div>
                            <div className="flex items-center gap-1.5 mb-1.5">
                              <Layers className="w-3.5 h-3.5 text-[oklch(0.48_0.22_25)]" />
                              <p className="text-xs font-bold text-[oklch(0.48_0.22_25)] uppercase tracking-wide">
                                Desdobramentos
                              </p>
                            </div>
                            <SubdivisionList content={operationalCommand.subdivisions} />
                          </div>

                          {/* Attributions */}
                          <div>
                            <div className="flex items-center gap-1.5 mb-1.5">
                              <Target className="w-3.5 h-3.5 text-[oklch(0.48_0.22_25)]" />
                              <p className="text-xs font-bold text-[oklch(0.48_0.22_25)] uppercase tracking-wide">
                                Atribuições
                              </p>
                            </div>
                            <AttributionList content={operationalCommand.attributions} />
                          </div>

                          {/* Legal basis */}
                          {operationalCommand.legalBasis && (
                            <div>
                              <div className="flex items-center gap-1.5 mb-1">
                                <FileText className="w-3.5 h-3.5 text-muted-foreground" />
                                <p className="text-xs font-bold text-muted-foreground uppercase tracking-wide">
                                  Base Legal
                                </p>
                              </div>
                              <p className="text-xs text-muted-foreground">{operationalCommand.legalBasis}</p>
                            </div>
                          )}
                        </div>
                      ) : (
                        <div className="p-6 text-center">
                          <Shield className="w-8 h-8 text-muted-foreground mx-auto mb-2 opacity-30" />
                          <p className="text-xs text-muted-foreground">Sem dados disponíveis</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              {/* ── Diretoria de Atividades Técnicas ── */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <BookOpen className="w-5 h-5 text-[oklch(0.28_0.12_255)]" />
                  <h2 className="font-display font-bold text-foreground">Diretoria de Atividades Técnicas</h2>
                  <div className="flex-1 h-px bg-border" />
                </div>
                <div className="flex gap-4 overflow-x-auto pb-2">
                  {(results ?? []).map(({ state, technicalDirectorate }) => (
                    <div
                      key={state.sigla}
                      className={cn(
                        "flex-shrink-0 bg-white rounded-xl shadow-sm overflow-hidden",
                        colWidth
                      )}
                      style={{ borderTop: "4px solid oklch(0.28 0.12 255)" }}
                    >
                      {/* Column header */}
                      <div className="p-4 bg-[oklch(0.97_0.02_255)] border-b border-border">
                        <div className="flex items-center justify-between">
                          <span className="font-display font-bold text-[oklch(0.28_0.12_255)] text-lg">
                            {state.sigla}
                          </span>
                          {technicalDirectorate && (
                            <DetailLevelBadge level={technicalDirectorate.detailLevel} size="sm" />
                          )}
                        </div>
                        <p className="text-xs text-muted-foreground mt-0.5">{state.name}</p>
                      </div>

                      {technicalDirectorate ? (
                        <div className="p-4 space-y-4">
                          {/* Nomenclature */}
                          <div>
                            <p className="text-xs font-bold text-[oklch(0.28_0.12_255)] uppercase tracking-wide mb-1">
                              Nomenclatura
                            </p>
                            <p className="text-sm font-semibold text-foreground leading-snug">
                              {technicalDirectorate.nomenclature}
                            </p>
                            {technicalDirectorate.acronym && (
                              <p className="text-xs text-muted-foreground">({technicalDirectorate.acronym})</p>
                            )}
                          </div>

                          {/* Subdivisions */}
                          <div>
                            <div className="flex items-center gap-1.5 mb-1.5">
                              <Layers className="w-3.5 h-3.5 text-[oklch(0.28_0.12_255)]" />
                              <p className="text-xs font-bold text-[oklch(0.28_0.12_255)] uppercase tracking-wide">
                                Desdobramentos
                              </p>
                            </div>
                            <SubdivisionList content={technicalDirectorate.subdivisions} />
                          </div>

                          {/* Attributions */}
                          <div>
                            <div className="flex items-center gap-1.5 mb-1.5">
                              <Target className="w-3.5 h-3.5 text-[oklch(0.28_0.12_255)]" />
                              <p className="text-xs font-bold text-[oklch(0.28_0.12_255)] uppercase tracking-wide">
                                Atribuições
                              </p>
                            </div>
                            <AttributionList content={technicalDirectorate.attributions} />
                          </div>

                          {/* Legal basis */}
                          {technicalDirectorate.legalBasis && (
                            <div>
                              <div className="flex items-center gap-1.5 mb-1">
                                <FileText className="w-3.5 h-3.5 text-muted-foreground" />
                                <p className="text-xs font-bold text-muted-foreground uppercase tracking-wide">
                                  Base Legal
                                </p>
                              </div>
                              <p className="text-xs text-muted-foreground">{technicalDirectorate.legalBasis}</p>
                            </div>
                          )}
                        </div>
                      ) : (
                        <div className="p-6 text-center">
                          <BookOpen className="w-8 h-8 text-muted-foreground mx-auto mb-2 opacity-30" />
                          <p className="text-xs text-muted-foreground">Sem dados disponíveis</p>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
