import { useState } from "react";
import { toast } from "sonner";

interface PDFExportOptions {
  filename?: string;
  title?: string;
  subtitle?: string;
}

/**
 * Hook para exportação de cargos como PDF via rota do servidor (/api/pdf/positions).
 * Gera o PDF no backend com pdfkit — suporta todos os dados sem limitações de browser.
 *
 * Para a página ComparativoCargos, passe:
 *   elementId = "positions" (não usado, apenas para compatibilidade)
 *   options.category = "chefe-co" | "chefe-dat"
 *   options.siglas = ["RO", "MG", ...] (opcional)
 *
 * Para a página Comparativo (estados), a exportação usa window.print() como fallback.
 */
export function usePDFExport() {
  const [isExporting, setIsExporting] = useState(false);

  /**
   * Exporta os cargos por categoria via rota do servidor.
   * @param _elementId - ignorado (mantido para compatibilidade de API)
   * @param options - opções de exportação
   * @param options.category - categoria do cargo ("chefe-co" | "chefe-dat")
   * @param options.siglas - lista de siglas de estados para filtrar (opcional)
   */
  const exportPositionsPDF = async (
    category: string,
    siglas: string[] = [],
    options: PDFExportOptions = {}
  ) => {
    setIsExporting(true);
    toast.loading("Gerando PDF...", { id: "pdf-export" });

    try {
      const params = new URLSearchParams({ category });
      if (siglas.length > 0) {
        params.set("siglas", siglas.join(","));
      }

      const response = await fetch(`/api/pdf/positions?${params.toString()}`);

      if (!response.ok) {
        const err = await response.json().catch(() => ({ error: "Erro desconhecido" }));
        throw new Error(err.error || `HTTP ${response.status}`);
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      // Criar link temporário para download
      const a = document.createElement("a");
      a.href = url;
      a.download = options.filename || `comparativo-cargos-${category}.pdf`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);

      toast.success("PDF gerado com sucesso!", { id: "pdf-export", duration: 4000 });
    } catch (err) {
      console.error("[PDF] Erro ao gerar PDF:", err);
      toast.error(
        err instanceof Error ? err.message : "Erro ao gerar PDF. Tente novamente.",
        { id: "pdf-export" }
      );
    } finally {
      setIsExporting(false);
    }
  };

  /**
   * Exporta conteúdo genérico via window.print() (fallback para páginas sem rota dedicada).
   * @param elementId - ID do elemento a ser impresso
   * @param options - opções de exportação
   */
  const exportToPDF = (_elementId: string, options: PDFExportOptions = {}) => {
    // Para ComparativoCargos, redirecionar para exportPositionsPDF se possível
    // Esta função é mantida para compatibilidade com a página Comparativo
    setIsExporting(true);
    toast.loading("Preparando impressão...", { id: "pdf-export" });

    setTimeout(() => {
      try {
        window.print();
        toast.success("Caixa de diálogo de impressão aberta. Salve como PDF.", {
          id: "pdf-export",
          duration: 5000,
        });
      } catch {
        toast.error("Não foi possível abrir a impressão.", { id: "pdf-export" });
      } finally {
        setIsExporting(false);
      }
    }, 300);
  };

  return { exportToPDF, exportPositionsPDF, isExporting };
}
