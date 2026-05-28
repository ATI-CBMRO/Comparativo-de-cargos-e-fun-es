import { useState, useMemo, useRef, useEffect } from "react";
import { trpc } from "@/lib/trpc";
import { usePDFExport } from "@/hooks/usePDFExport";
import DetailLevelBadge from "@/components/DetailLevelBadge";
import { Button } from "@/components/ui/button";
import {
  BookOpen,
  ChevronDown,
  ChevronRight,
  ChevronUp,
  FileDown,
  FileText,
  GitCompare,
  Layers,
  Loader2,
  Plus,
  Shield,
  Target,
  Trash2,
  User,
  Users,
  X,
} from "lucide-react";
import { cn } from "@/lib/utils";

type Position = {
  id: number;
  title: string;
  acronym: string | null;
  rank: string | null;
  subordinateTo: string | null;
  subordinates: string | null;
  attributions: string | null;
  sortOrder: number | null;
};

function SubdivisionList({ content }: { content: string | null | undefined }) {
  if (!content) return <p className="text-xs text-muted-foreground italic">Não especificado</p>;
  let items: string[];
  try {
    const parsed = JSON.parse(content);
    items = Array.isArray(parsed)
      ? parsed.map((s: unknown) => String(s).trim()).filter(Boolean)
      : content.split(";").map((s) => s.trim()).filter(Boolean);
  } catch {
    items = content.split(";").map((s) => s.trim()).filter(Boolean);
  }
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
  let items: string[];
  try {
    const parsed = JSON.parse(content);
    items = Array.isArray(parsed)
      ? parsed.map((s: unknown) => String(s).trim()).filter(Boolean)
      : content.split(";").map((s) => s.trim()).filter(Boolean);
  } catch {
    items = content.split(";").map((s) => s.trim()).filter(Boolean);
  }
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

function PositionCard({ position, accentColor }: { position: Position; accentColor: string }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <div
      className="border border-border rounded-lg overflow-hidden"
      style={{ borderLeftColor: accentColor, borderLeftWidth: 3 }}
    >
      <button
        className="w-full flex items-center justify-between px-3 py-2 bg-muted/40 hover:bg-muted/70 transition-colors text-left"
        onClick={() => setExpanded((v) => !v)}
      >
        <div className="flex items-center gap-2 min-w-0">
          <User className="w-3.5 h-3.5 flex-shrink-0" style={{ color: accentColor }} />
          <div className="min-w-0">
            <p className="text-xs font-semibold text-foreground truncate">
              {position.title}
              {position.acronym && (
                <span className="ml-1 text-muted-foreground font-normal">({position.acronym})</span>
              )}
            </p>
            {position.rank && (
              <p className="text-[10px] text-muted-foreground">{position.rank}</p>
            )}
          </div>
        </div>
        {expanded ? (
          <ChevronUp className="w-3.5 h-3.5 text-muted-foreground flex-shrink-0" />
        ) : (
          <ChevronDown className="w-3.5 h-3.5 text-muted-foreground flex-shrink-0" />
        )}
      </button>

      {expanded && (
        <div className="px-3 py-2 space-y-2 bg-white">
          {position.subordinateTo && (
            <div>
              <p className="text-[10px] font-bold uppercase tracking-wide text-muted-foreground mb-0.5">
                Subordinado a
              </p>
              <p className="text-xs text-foreground">{position.subordinateTo}</p>
            </div>
          )}
          {position.subordinates && (
            <div>
              <p className="text-[10px] font-bold uppercase tracking-wide text-muted-foreground mb-0.5">
                Subordinados / Desdobramentos
              </p>
              <SubdivisionList content={position.subordinates} />
            </div>
          )}
          {position.attributions && (
            <div>
              <p className="text-[10px] font-bold uppercase tracking-wide text-muted-foreground mb-0.5">
                Atribuições
              </p>
              <AttributionList content={position.attributions} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function PositionsList({
  positions,
  accentColor,
  emptyLabel,
}: {
  positions: Position[];
  accentColor: string;
  emptyLabel: string;
}) {
  if (positions.length === 0) {
    return <p className="text-xs text-muted-foreground italic">{emptyLabel}</p>;
  }
  return (
    <div className="space-y-1.5">
      {positions.map((pos) => (
        <PositionCard key={pos.id} position={pos} accentColor={accentColor} />
      ))}
    </div>
  );
}

const REGION_STATES: Record<string, string[]> = {
  Norte: ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
  Nordeste: ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
  "Centro-Oeste": ["DF", "GO", "MT", "MS"],
  Sudeste: ["ES", "MG", "RJ", "SP"],
  Sul: ["PR", "RS", "SC"],
};

export default function Comparativo() {
  const [selectedSiglas, setSelectedSiglas] = useState<string[]>([]);
  const [showStateSelector, setShowStateSelector] = useState(false);
  const selectorRef = useRef<HTMLDivElement>(null);

  const { data: states } = trpc.states.list.useQuery();
  const { data: results, isLoading } = trpc.data.comparative.useQuery(
    { siglas: selectedSiglas },
    { enabled: selectedSiglas.length > 0 }
  );

  // Fechar dropdown ao clicar fora
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (selectorRef.current && !selectorRef.current.contains(e.target as Node)) {
        setShowStateSelector(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  const addState = (sigla: string) => {
    if (!selectedSiglas.includes(sigla) && selectedSiglas.length < 5) {
      setSelectedSiglas((prev) => [...prev, sigla]);
    }
    setShowStateSelector(false);
  };

  const removeState = (sigla: string) => {
    setSelectedSiglas((prev) => prev.filter((s) => s !== sigla));
  };

  // Siglas disponíveis no banco (apenas os 19 estados com dados)
  const availableSiglas = useMemo(
    () => (states ?? []).map((s) => s.sigla),
    [states]
  );

  const availableStates = useMemo(
    () => (states ?? []).filter((s) => !selectedSiglas.includes(s.sigla)),
    [states, selectedSiglas]
  );

  // Escala dinâmica: grid com número de colunas fixo baseado na quantidade de estados
  const colCount = selectedSiglas.length || 1;
  // Mapeamento de quantidade de estados para colunas do grid
  const gridCols: Record<number, string> = {
    1: "grid-cols-1",
    2: "grid-cols-2",
    3: "grid-cols-3",
    4: "grid-cols-4",
    5: "grid-cols-5",
  };
  const gridClass = gridCols[colCount] ?? "grid-cols-5";
  const OC_COLOR = "oklch(0.48 0.22 25)";
  const TD_COLOR = "oklch(0.28 0.12 255)";

  const { exportComparativePDF, isExporting } = usePDFExport();

  const handleExportPDF = () => {
    exportComparativePDF(selectedSiglas, {
      filename: `comparativo-estados-${selectedSiglas.join("-")}-${Date.now()}.pdf`,
    });
  };

  return (
    <div className="p-6 max-w-full mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="font-display text-2xl font-bold text-foreground">Comparativo entre Estados</h1>
        <p className="text-muted-foreground text-sm mt-1">
          Selecione até 5 estados para comparar lado a lado suas estruturas organizacionais, incluindo cargos, funções, subordinações e atribuições.
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
            <div className="relative" ref={selectorRef}>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowStateSelector(!showStateSelector)}
                className="gap-2 border-dashed"
              >
                <Plus className="w-4 h-4" />
                Adicionar estado
                <ChevronDown className="w-3 h-3" />
              </Button>
              {showStateSelector && (
                <div className="absolute top-full left-0 mt-1 z-50 bg-white border border-border rounded-xl shadow-lg p-3 w-72 max-h-80 overflow-y-auto">
                  {availableStates.length === 0 ? (
                    <p className="text-xs text-muted-foreground p-2">Todos os estados já selecionados.</p>
                  ) : (
                    <div className="space-y-3">
                      {Object.entries(REGION_STATES).map(([region, siglas]) => {
                        const regionAvailable = siglas.filter(
                          (s) => availableSiglas.includes(s) && !selectedSiglas.includes(s)
                        );
                        if (regionAvailable.length === 0) return null;
                        return (
                          <div key={region}>
                            <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-1.5 px-1">{region}</p>
                            <div className="space-y-0.5">
                              {regionAvailable.map((sigla) => {
                                const state = states?.find((s) => s.sigla === sigla);
                                return (
                                  <button
                                    key={sigla}
                                    onClick={() => addState(sigla)}
                                    className="w-full flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-muted text-sm text-left transition-colors"
                                  >
                                    <span className="font-bold text-[oklch(0.28_0.12_255)] w-8 font-mono text-xs">{sigla}</span>
                                    <span className="text-foreground text-xs">{state?.name ?? sigla}</span>
                                  </button>
                                );
                              })}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {selectedSiglas.length > 0 && (
            <div className="flex items-center gap-2 ml-auto">
              <Button
                variant="outline"
                size="sm"
                onClick={handleExportPDF}
                disabled={isExporting || isLoading || !results}
                className="gap-2"
              >
                {isExporting ? (
                  <><Loader2 className="w-4 h-4 animate-spin" /> Gerando PDF...</>
                ) : (
                  <><FileDown className="w-4 h-4" /> Exportar PDF</>
                )}
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSelectedSiglas([])}
                className="gap-2 text-muted-foreground"
              >
                <Trash2 className="w-4 h-4" />
                Limpar seleção
              </Button>
            </div>
          )}
        </div>
      </div>

      {/* Empty state */}
      {selectedSiglas.length === 0 && (
        <div className="bg-white rounded-xl p-16 shadow-sm text-center">
          <GitCompare className="w-16 h-16 text-muted-foreground mx-auto mb-4 opacity-30" />
          <p className="font-display font-semibold text-foreground mb-2">Nenhum estado selecionado</p>
          <p className="text-sm text-muted-foreground max-w-sm mx-auto">
            Adicione dois ou mais estados para visualizar a comparação lado a lado das estruturas organizacionais, incluindo cargos, funções e atribuições.
          </p>
        </div>
      )}

      {/* Comparison table */}
      {selectedSiglas.length > 0 && (
        <div>
          {isLoading ? (
            <div className={`grid ${gridClass} gap-4`}>
              {selectedSiglas.map((s) => (
                <div key={s} className="h-96 bg-muted rounded-xl animate-pulse" />
              ))}
            </div>
          ) : (
            <div id="comparativo-content" className="space-y-8">

              {/* ── Comando Operacional ── */}
              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Shield className="w-5 h-5" style={{ color: OC_COLOR }} />
                  <h2 className="font-display font-bold text-foreground">Comando Operacional</h2>
                  <div className="flex-1 h-px bg-border" />
                </div>
                <div className={`grid ${gridClass} gap-4`}>
                  {(results ?? []).map(({ state, operationalCommand, ocPositions }) => (
                    <div
                      key={state.sigla}
                      className="bg-white rounded-xl shadow-sm overflow-hidden"
                      style={{ borderTop: `4px solid ${OC_COLOR}` }}
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
                            <p className="text-xs font-bold uppercase tracking-wide mb-1" style={{ color: OC_COLOR }}>
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
                              <Layers className="w-3.5 h-3.5" style={{ color: OC_COLOR }} />
                              <p className="text-xs font-bold uppercase tracking-wide" style={{ color: OC_COLOR }}>
                                Desdobramentos
                              </p>
                            </div>
                            <SubdivisionList content={operationalCommand.subdivisions} />
                          </div>

                          {/* Attributions */}
                          <div>
                            <div className="flex items-center gap-1.5 mb-1.5">
                              <Target className="w-3.5 h-3.5" style={{ color: OC_COLOR }} />
                              <p className="text-xs font-bold uppercase tracking-wide" style={{ color: OC_COLOR }}>
                                Atribuições do Órgão
                              </p>
                            </div>
                            <AttributionList content={operationalCommand.attributions} />
                          </div>

                          {/* Positions */}
                          <div>
                            <div className="flex items-center gap-1.5 mb-2">
                              <Users className="w-3.5 h-3.5" style={{ color: OC_COLOR }} />
                              <p className="text-xs font-bold uppercase tracking-wide" style={{ color: OC_COLOR }}>
                                Cargos e Funções ({ocPositions?.length ?? 0})
                              </p>
                            </div>
                            <PositionsList
                              positions={ocPositions ?? []}
                              accentColor={OC_COLOR}
                              emptyLabel="Nenhum cargo/função detalhado na legislação"
                            />
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

                          {/* Artigo Legal de Origem */}
                          {(operationalCommand as any).legalArticle && (
                            <div className="rounded-lg border border-amber-200 bg-amber-50 p-3">
                              <div className="flex items-center gap-1.5 mb-1">
                                <BookOpen className="w-3.5 h-3.5 text-amber-600" />
                                <p className="text-xs font-bold text-amber-700 uppercase tracking-wide">
                                  Artigo Legal de Origem
                                </p>
                              </div>
                              <p className="text-xs text-amber-800 leading-relaxed">
                                {(operationalCommand as any).legalArticle}
                              </p>
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
                  <BookOpen className="w-5 h-5" style={{ color: TD_COLOR }} />
                  <h2 className="font-display font-bold text-foreground">Diretoria de Atividades Técnicas</h2>
                  <div className="flex-1 h-px bg-border" />
                </div>
                <div className={`grid ${gridClass} gap-4`}>
                  {(results ?? []).map(({ state, technicalDirectorate, tdPositions }) => (
                    <div
                      key={state.sigla}
                      className="bg-white rounded-xl shadow-sm overflow-hidden"
                      style={{ borderTop: `4px solid ${TD_COLOR}` }}
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
                            <p className="text-xs font-bold uppercase tracking-wide mb-1" style={{ color: TD_COLOR }}>
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
                              <Layers className="w-3.5 h-3.5" style={{ color: TD_COLOR }} />
                              <p className="text-xs font-bold uppercase tracking-wide" style={{ color: TD_COLOR }}>
                                Desdobramentos
                              </p>
                            </div>
                            <SubdivisionList content={technicalDirectorate.subdivisions} />
                          </div>

                          {/* Attributions */}
                          <div>
                            <div className="flex items-center gap-1.5 mb-1.5">
                              <Target className="w-3.5 h-3.5" style={{ color: TD_COLOR }} />
                              <p className="text-xs font-bold uppercase tracking-wide" style={{ color: TD_COLOR }}>
                                Atribuições do Órgão
                              </p>
                            </div>
                            <AttributionList content={technicalDirectorate.attributions} />
                          </div>

                          {/* Positions */}
                          <div>
                            <div className="flex items-center gap-1.5 mb-2">
                              <Users className="w-3.5 h-3.5" style={{ color: TD_COLOR }} />
                              <p className="text-xs font-bold uppercase tracking-wide" style={{ color: TD_COLOR }}>
                                Cargos e Funções ({tdPositions?.length ?? 0})
                              </p>
                            </div>
                            <PositionsList
                              positions={tdPositions ?? []}
                              accentColor={TD_COLOR}
                              emptyLabel="Nenhum cargo/função detalhado na legislação"
                            />
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

                          {/* Artigo Legal de Origem */}
                          {(technicalDirectorate as any).legalArticle && (
                            <div className="rounded-lg border border-amber-200 bg-amber-50 p-3">
                              <div className="flex items-center gap-1.5 mb-1">
                                <BookOpen className="w-3.5 h-3.5 text-amber-600" />
                                <p className="text-xs font-bold text-amber-700 uppercase tracking-wide">
                                  Artigo Legal de Origem
                                </p>
                              </div>
                              <p className="text-xs text-amber-800 leading-relaxed">
                                {(technicalDirectorate as any).legalArticle}
                              </p>
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
