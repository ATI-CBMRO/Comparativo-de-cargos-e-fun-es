import { useParams, Link } from "wouter";
import { trpc } from "@/lib/trpc";
import DetailLevelBadge from "@/components/DetailLevelBadge";
import {
  ArrowLeft,
  BookOpen,
  Building2,
  ChevronRight,
  FileText,
  Layers,
  Shield,
  Target,
} from "lucide-react";

function InfoSection({
  icon: Icon,
  title,
  content,
  color,
}: {
  icon: React.ElementType;
  title: string;
  content: string | null | undefined;
  color: string;
}) {
  if (!content) return null;
  const items = content.split(";").map((s) => s.trim()).filter(Boolean);

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2">
        <Icon className={`w-4 h-4 ${color}`} />
        <h4 className={`text-sm font-semibold ${color}`}>{title}</h4>
      </div>
      <ul className="space-y-1.5 pl-6">
        {items.map((item, i) => (
          <li key={i} className="flex items-start gap-2 text-sm text-foreground">
            <ChevronRight className="w-3.5 h-3.5 text-muted-foreground flex-shrink-0 mt-0.5" />
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function OrgCard({
  type,
  nomenclature,
  acronym,
  subdivisions,
  attributions,
  detailLevel,
  legalBasis,
  notes,
}: {
  type: "operational" | "technical";
  nomenclature: string;
  acronym?: string | null;
  subdivisions?: string | null;
  attributions?: string | null;
  detailLevel: "detalhado" | "moderado" | "basico";
  legalBasis?: string | null;
  notes?: string | null;
}) {
  const isOperational = type === "operational";
  const accentColor = isOperational ? "oklch(0.48 0.22 25)" : "oklch(0.28 0.12 255)";
  const bgColor = isOperational ? "oklch(0.97 0.02 25)" : "oklch(0.97 0.02 255)";
  const textColor = isOperational ? "text-[oklch(0.48_0.22_25)]" : "text-[oklch(0.28_0.12_255)]";
  const Icon = isOperational ? Shield : BookOpen;
  const typeLabel = isOperational ? "Comando Operacional" : "Diretoria de Atividades Técnicas";

  return (
    <div
      className="bg-white rounded-xl shadow-sm overflow-hidden"
      style={{ borderTop: `4px solid ${accentColor}` }}
    >
      <div className="p-5 border-b border-border" style={{ background: bgColor }}>
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-2">
            <Icon className={`w-5 h-5 ${textColor}`} />
            <span className={`text-xs font-bold uppercase tracking-wider ${textColor}`}>
              {typeLabel}
            </span>
          </div>
          <DetailLevelBadge level={detailLevel} />
        </div>
        <h3 className="font-display font-bold text-foreground text-lg mt-3 leading-snug">
          {nomenclature}
        </h3>
        {acronym && (
          <p className={`text-sm font-medium ${textColor} mt-1`}>Sigla: {acronym}</p>
        )}
      </div>

      <div className="p-5 space-y-5">
        <InfoSection
          icon={Layers}
          title="Desdobramentos (Seções / Divisões)"
          content={subdivisions}
          color={textColor}
        />
        <InfoSection
          icon={Target}
          title="Atribuições"
          content={attributions}
          color={textColor}
        />
        {legalBasis && (
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <FileText className={`w-4 h-4 ${textColor}`} />
              <h4 className={`text-sm font-semibold ${textColor}`}>Base Legal</h4>
            </div>
            <p className="text-sm text-muted-foreground pl-6">{legalBasis}</p>
          </div>
        )}
        {notes && (
          <div className="p-3 rounded-lg bg-muted">
            <p className="text-xs text-muted-foreground italic">{notes}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default function EstadoDetalhe() {
  const params = useParams<{ sigla: string }>();
  const sigla = params.sigla?.toUpperCase() ?? "";

  const { data, isLoading, error } = trpc.states.details.useQuery({ sigla });

  if (isLoading) {
    return (
      <div className="p-6 max-w-5xl mx-auto space-y-6">
        <div className="h-8 bg-muted rounded w-48 animate-pulse" />
        <div className="h-32 bg-muted rounded-xl animate-pulse" />
        <div className="grid md:grid-cols-2 gap-6">
          <div className="h-64 bg-muted rounded-xl animate-pulse" />
          <div className="h-64 bg-muted rounded-xl animate-pulse" />
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-6 max-w-5xl mx-auto text-center py-20">
        <p className="text-muted-foreground">Estado não encontrado.</p>
        <Link
          href="/estados"
          className="mt-4 inline-flex items-center gap-2 text-sm text-[oklch(0.48_0.22_25)] hover:underline"
        >
          <ArrowLeft className="w-4 h-4" /> Voltar para Estados
        </Link>
      </div>
    );
  }

  const { state, operationalCommand, technicalDirectorate } = data;

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-6">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Link href="/estados" className="hover:text-foreground transition-colors">
          Estados
        </Link>
        <ChevronRight className="w-4 h-4" />
        <span className="text-foreground font-medium">{state.name}</span>
      </div>

      {/* State header */}
      <div className="bg-[oklch(0.22_0.10_255)] rounded-2xl p-6 text-white relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 right-0 w-64 h-64 bg-[oklch(0.48_0.22_25)] rounded-full -translate-y-1/2 translate-x-1/4" />
        </div>
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-3">
            <span className="font-display font-bold text-4xl text-[oklch(0.75_0.15_75)]">
              {state.sigla}
            </span>
            <div>
              <h1 className="font-display font-bold text-2xl">{state.name}</h1>
              <p className="text-[oklch(0.70_0.05_255)] text-sm">{state.region}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Building2 className="w-4 h-4 text-[oklch(0.70_0.05_255)]" />
            <p className="text-[oklch(0.85_0.03_255)] text-sm">{state.corporationName}</p>
          </div>
          {state.legislationDocuments && (
            <div className="flex items-center gap-2 mt-2">
              <FileText className="w-4 h-4 text-[oklch(0.70_0.05_255)]" />
              <p className="text-[oklch(0.70_0.05_255)] text-xs">{state.legislationDocuments}</p>
            </div>
          )}
        </div>
      </div>

      {/* Org cards */}
      <div className="grid md:grid-cols-2 gap-6">
        {operationalCommand ? (
          <OrgCard
            type="operational"
            nomenclature={operationalCommand.nomenclature}
            acronym={operationalCommand.acronym}
            subdivisions={operationalCommand.subdivisions}
            attributions={operationalCommand.attributions}
            detailLevel={operationalCommand.detailLevel}
            legalBasis={operationalCommand.legalBasis}
            notes={operationalCommand.notes}
          />
        ) : (
          <div className="bg-white rounded-xl p-6 shadow-sm border-2 border-dashed border-border text-center">
            <Shield className="w-8 h-8 text-muted-foreground mx-auto mb-2 opacity-40" />
            <p className="text-sm text-muted-foreground">
              Dados de Comando Operacional não disponíveis.
            </p>
          </div>
        )}

        {technicalDirectorate ? (
          <OrgCard
            type="technical"
            nomenclature={technicalDirectorate.nomenclature}
            acronym={technicalDirectorate.acronym}
            subdivisions={technicalDirectorate.subdivisions}
            attributions={technicalDirectorate.attributions}
            detailLevel={technicalDirectorate.detailLevel}
            legalBasis={technicalDirectorate.legalBasis}
            notes={technicalDirectorate.notes}
          />
        ) : (
          <div className="bg-white rounded-xl p-6 shadow-sm border-2 border-dashed border-border text-center">
            <BookOpen className="w-8 h-8 text-muted-foreground mx-auto mb-2 opacity-40" />
            <p className="text-sm text-muted-foreground">
              Dados de Diretoria de Atividades Técnicas não disponíveis.
            </p>
          </div>
        )}
      </div>

      {/* Back link */}
      <Link
        href="/estados"
        className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Voltar para a listagem
      </Link>
    </div>
  );
}
