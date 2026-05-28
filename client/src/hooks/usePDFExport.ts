import { useState } from "react";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { toast } from "sonner";

interface PDFExportOptions {
  filename?: string;
  title?: string;
  subtitle?: string;
}

export function usePDFExport() {
  const [isExporting, setIsExporting] = useState(false);

  const exportToPDF = async (
    elementId: string,
    options: PDFExportOptions = {}
  ) => {
    const {
      filename = "relatorio-cbm.pdf",
      title = "Portal de Legislação dos Corpos de Bombeiros Militares",
      subtitle = "",
    } = options;

    const element = document.getElementById(elementId);
    if (!element) {
      console.error(`Element with id "${elementId}" not found`);
      return;
    }

    setIsExporting(true);
    toast.loading("Gerando PDF...", { id: "pdf-export" });
    try {
      const canvas = await html2canvas(element, {
        scale: 2,
        useCORS: true,
        allowTaint: true,
        backgroundColor: "#ffffff",
        logging: false,
        windowWidth: element.scrollWidth,
        windowHeight: element.scrollHeight,
      });

      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF({
        orientation: canvas.width > canvas.height ? "landscape" : "portrait",
        unit: "mm",
        format: "a4",
      });

      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      const margin = 10;
      const headerHeight = 20;

      // Header institucional
      pdf.setFillColor(15, 23, 42); // azul escuro
      pdf.rect(0, 0, pageWidth, headerHeight, "F");

      pdf.setTextColor(255, 255, 255);
      pdf.setFontSize(11);
      pdf.setFont("helvetica", "bold");
      pdf.text(title, margin, 8);

      if (subtitle) {
        pdf.setFontSize(8);
        pdf.setFont("helvetica", "normal");
        pdf.text(subtitle, margin, 14);
      }

      // Data de geração
      const dateStr = new Date().toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
      pdf.setFontSize(7);
      pdf.setTextColor(200, 200, 200);
      pdf.text(`Gerado em: ${dateStr}`, pageWidth - margin, 14, {
        align: "right",
      });

      // Imagem do conteúdo
      const contentY = headerHeight + 4;
      const availableWidth = pageWidth - 2 * margin;
      const availableHeight = pageHeight - contentY - margin;

      const imgWidth = canvas.width;
      const imgHeight = canvas.height;
      const ratio = Math.min(
        availableWidth / imgWidth,
        availableHeight / imgHeight
      );

      const scaledWidth = imgWidth * ratio;
      const scaledHeight = imgHeight * ratio;

      // Se o conteúdo for maior que uma página, divide em múltiplas páginas
      if (scaledHeight <= availableHeight) {
        pdf.addImage(imgData, "PNG", margin, contentY, scaledWidth, scaledHeight);
      } else {
        // Múltiplas páginas
        const pxPerPage = (availableHeight / ratio);
        let yOffset = 0;
        let pageNum = 0;

        while (yOffset < imgHeight) {
          if (pageNum > 0) {
            pdf.addPage();
            // Repetir header
            pdf.setFillColor(15, 23, 42);
            pdf.rect(0, 0, pageWidth, headerHeight, "F");
            pdf.setTextColor(255, 255, 255);
            pdf.setFontSize(11);
            pdf.setFont("helvetica", "bold");
            pdf.text(title, margin, 8);
            if (subtitle) {
              pdf.setFontSize(8);
              pdf.setFont("helvetica", "normal");
              pdf.text(subtitle, margin, 14);
            }
          }

          const sliceHeight = Math.min(pxPerPage, imgHeight - yOffset);
          const sliceCanvas = document.createElement("canvas");
          sliceCanvas.width = imgWidth;
          sliceCanvas.height = sliceHeight;
          const ctx = sliceCanvas.getContext("2d")!;
          ctx.drawImage(canvas, 0, -yOffset);
          const sliceData = sliceCanvas.toDataURL("image/png");
          const sliceScaledHeight = sliceHeight * ratio;

          pdf.addImage(
            sliceData,
            "PNG",
            margin,
            contentY,
            scaledWidth,
            sliceScaledHeight
          );

          yOffset += pxPerPage;
          pageNum++;
        }
      }

      pdf.save(filename);
      toast.success("PDF gerado com sucesso!", { id: "pdf-export" });
    } catch (err) {
      console.error("Erro ao gerar PDF:", err);
      toast.error("Erro ao gerar PDF. Tente novamente.", { id: "pdf-export" });
    } finally {
      setIsExporting(false);
    }
  };

  return { exportToPDF, isExporting };
}
