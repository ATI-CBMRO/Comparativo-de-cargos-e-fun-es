import { cn } from "@/lib/utils";

type DetailLevel = "detalhado" | "moderado" | "basico";

const config: Record<DetailLevel, { label: string; className: string; dot: string }> = {
  detalhado: {
    label: "Detalhado",
    className: "badge-detalhado",
    dot: "bg-[oklch(0.45_0.18_145)]",
  },
  moderado: {
    label: "Moderado",
    className: "badge-moderado",
    dot: "bg-[oklch(0.60_0.18_75)]",
  },
  basico: {
    label: "Básico",
    className: "badge-basico",
    dot: "bg-[oklch(0.55_0.15_25)]",
  },
};

interface DetailLevelBadgeProps {
  level: DetailLevel;
  size?: "sm" | "md";
  className?: string;
}

export default function DetailLevelBadge({
  level,
  size = "md",
  className,
}: DetailLevelBadgeProps) {
  const { label, className: levelClass, dot } = config[level];

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full font-medium",
        size === "sm" ? "px-2 py-0.5 text-xs" : "px-2.5 py-1 text-xs",
        levelClass,
        className
      )}
    >
      <span className={cn("w-1.5 h-1.5 rounded-full flex-shrink-0", dot)} />
      {label}
    </span>
  );
}
