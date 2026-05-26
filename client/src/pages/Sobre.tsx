import { BookOpen, FileText, Flame, Info, MapPin, Shield } from "lucide-react";

const DOCUMENTS = [
  { state: "Alagoas", docs: "Regimento Interno do CBMAL; Quadro Demonstrativo de Cargos e Funções" },
  { state: "Ceará", docs: "Lei de Organização Básica do CBMCE" },
  { state: "Distrito Federal", docs: "Regimento Interno do CBMDF" },
  { state: "Espírito Santo", docs: "Normas Gerais de Ação do CBMES" },
  { state: "Maranhão", docs: "Lei de Organização Básica do CBMMA; Quadro de Organização e Distribuição" },
  { state: "Mato Grosso", docs: "Lei de Organização Básica do CBMMT" },
  { state: "Mato Grosso do Sul", docs: "Lei de Organização Básica do CBMMS" },
  { state: "Minas Gerais", docs: "Lei de Organização Básica do CBMMG" },
  { state: "Pará", docs: "Lei de Organização Básica do CBMPA; Regimento Interno do CBMPA" },
  { state: "Paraíba", docs: "Lei de Organização Básica do CBMPB" },
  { state: "Paraná", docs: "Lei de Organização Básica do CBMPR" },
  { state: "Pernambuco", docs: "Lei de Organização Básica do CBMPE" },
  { state: "Piauí", docs: "Lei de Organização Básica do CBMPI" },
  { state: "Rio de Janeiro", docs: "Lei de Organização Básica do CBMERJ" },
  { state: "Rio Grande do Sul", docs: "Lei de Organização Básica do CBMRS; Regimento Interno do CBMRS" },
  { state: "Rondônia", docs: "Minuta de Lei de Organização Básica do CBMRO" },
  { state: "Santa Catarina", docs: "Lei de Organização Básica do CBMSC" },
  { state: "Sergipe", docs: "Lei de Organização Básica do CBMSE; Regimento Interno do CBMSE" },
  { state: "Tocantins", docs: "Lei de Organização Básica do CBMTO" },
];

export default function Sobre() {
  return (
    <div className="p-6 max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div className="bg-[oklch(0.22_0.10_255)] rounded-2xl p-8 text-white relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 right-0 w-64 h-64 bg-[oklch(0.48_0.22_25)] rounded-full -translate-y-1/2 translate-x-1/4" />
        </div>
        <div className="relative z-10 flex items-start gap-4">
          <div className="w-14 h-14 rounded-xl bg-[oklch(0.48_0.22_25)] flex items-center justify-center flex-shrink-0">
            <Flame className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="font-display font-bold text-2xl mb-2">Sobre o Portal</h1>
            <p className="text-[oklch(0.80_0.03_255)] text-sm leading-relaxed max-w-2xl">
              Portal de consulta e comparação das estruturas organizacionais dos Corpos de Bombeiros
              Militares estaduais brasileiros, com foco no Comando Operacional e na Diretoria de
              Atividades Técnicas (ou nomenclaturas equivalentes).
            </p>
          </div>
        </div>
      </div>

      {/* Objective */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-5 rounded bg-[oklch(0.48_0.22_25)]" />
          <h2 className="font-display font-semibold text-foreground">Objetivo</h2>
        </div>
        <p className="text-sm text-foreground leading-relaxed">
          Este portal foi desenvolvido para apoiar o trabalho de assessoria técnica institucional
          do Corpo de Bombeiros Militar de Rondônia (CBMRO), consolidando em um único ambiente
          consultável as informações sobre a estrutura organizacional dos corpos de bombeiros
          estaduais, com ênfase em dois órgãos fundamentais:
        </p>
        <div className="grid sm:grid-cols-2 gap-4 mt-4">
          <div className="p-4 rounded-lg bg-[oklch(0.97_0.02_25)] border border-[oklch(0.90_0.05_25)]">
            <div className="flex items-center gap-2 mb-2">
              <Shield className="w-5 h-5 text-[oklch(0.48_0.22_25)]" />
              <h3 className="font-semibold text-sm text-[oklch(0.48_0.22_25)]">Comando Operacional</h3>
            </div>
            <p className="text-xs text-muted-foreground leading-relaxed">
              Órgão responsável pelo planejamento, coordenação e controle das atividades
              operacionais de bombeiros — combate a incêndio, busca, salvamento, resgate e APH.
              Pode receber nomenclaturas como Diretoria Operacional, Coordenadoria Operacional,
              Comando de Operações, entre outras.
            </p>
          </div>
          <div className="p-4 rounded-lg bg-[oklch(0.97_0.02_255)] border border-[oklch(0.88_0.05_255)]">
            <div className="flex items-center gap-2 mb-2">
              <BookOpen className="w-5 h-5 text-[oklch(0.28_0.12_255)]" />
              <h3 className="font-semibold text-sm text-[oklch(0.28_0.12_255)]">Diretoria de Atividades Técnicas</h3>
            </div>
            <p className="text-xs text-muted-foreground leading-relaxed">
              Órgão responsável pela análise de projetos de segurança contra incêndio, vistorias,
              normatização, investigação de incêndios e fiscalização de edificações. Pode ser
              denominado Diretoria de Serviços Técnicos, Centro de Atividades Técnicas,
              Departamento de Segurança Contra Incêndio, entre outros.
            </p>
          </div>
        </div>
      </div>

      {/* Methodology */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-5 rounded bg-[oklch(0.28_0.12_255)]" />
          <h2 className="font-display font-semibold text-foreground">Metodologia</h2>
        </div>
        <p className="text-sm text-foreground leading-relaxed mb-3">
          O levantamento foi realizado a partir da análise direta dos documentos legislativos
          oficiais de cada estado, classificando o nível de detalhamento das informações encontradas
          em três categorias:
        </p>
        <div className="space-y-3">
          {[
            {
              level: "Detalhado",
              color: "oklch(0.45 0.18 145)",
              bg: "oklch(0.92 0.08 145)",
              desc: "O documento define claramente a estrutura do órgão, seus desdobramentos (seções, divisões, departamentos), os cargos previstos e as atribuições específicas de cada um.",
            },
            {
              level: "Moderado",
              color: "oklch(0.60 0.18 75)",
              bg: "oklch(0.95 0.08 75)",
              desc: "O documento menciona o órgão com sua nomenclatura e competências gerais, com algum detalhamento de estrutura, mas sem especificar todos os desdobramentos ou atribuições individuais.",
            },
            {
              level: "Básico",
              color: "oklch(0.55 0.15 25)",
              bg: "oklch(0.95 0.06 25)",
              desc: "O documento apenas menciona o órgão na estrutura organizacional, sem detalhar sua composição interna, cargos ou atribuições específicas.",
            },
          ].map(({ level, color, bg, desc }) => (
            <div
              key={level}
              className="flex items-start gap-3 p-3 rounded-lg"
              style={{ background: bg }}
            >
              <span
                className="text-xs font-bold px-2 py-0.5 rounded-full text-white flex-shrink-0 mt-0.5"
                style={{ background: color }}
              >
                {level}
              </span>
              <p className="text-xs text-foreground leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Sources */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-1 h-5 rounded bg-[oklch(0.48_0.22_25)]" />
          <h2 className="font-display font-semibold text-foreground">Fontes Consultadas</h2>
        </div>
        <p className="text-sm text-muted-foreground mb-4">
          Foram analisados documentos legislativos de 19 estados brasileiros:
        </p>
        <div className="space-y-2">
          {DOCUMENTS.map(({ state, docs }) => (
            <div key={state} className="flex items-start gap-3 py-2 border-b border-border last:border-0">
              <div className="flex items-center gap-1.5 flex-shrink-0 w-36">
                <MapPin className="w-3.5 h-3.5 text-[oklch(0.48_0.22_25)]" />
                <span className="text-sm font-semibold text-foreground">{state}</span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {docs.split(";").map((doc, i) => (
                  <span
                    key={i}
                    className="flex items-center gap-1 text-xs text-muted-foreground bg-muted px-2 py-0.5 rounded"
                  >
                    <FileText className="w-3 h-3" />
                    {doc.trim()}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer note */}
      <div className="flex items-start gap-3 p-4 rounded-xl bg-[oklch(0.95_0.03_255)] border border-[oklch(0.88_0.05_255)]">
        <Info className="w-5 h-5 text-[oklch(0.28_0.12_255)] flex-shrink-0 mt-0.5" />
        <p className="text-xs text-muted-foreground leading-relaxed">
          As informações contidas neste portal são baseadas nos documentos legislativos analisados
          e têm caráter informativo e comparativo. Para fins oficiais, consulte sempre a legislação
          vigente de cada estado. Este portal foi desenvolvido para uso interno do Corpo de Bombeiros
          Militar de Rondônia.
        </p>
      </div>
    </div>
  );
}
