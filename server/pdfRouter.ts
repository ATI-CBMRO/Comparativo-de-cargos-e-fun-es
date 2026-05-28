import type { Express, Request, Response } from "express";
import PDFDocument from "pdfkit";
import { getPositionsByCategory } from "./db";

// ─── Cores institucionais ─────────────────────────────────────────────────────
const NAVY = "#0f172a";
const RED = "#b91c1c";
const LIGHT_GRAY = "#f1f5f9";
const MID_GRAY = "#64748b";
const DARK = "#1e293b";
const WHITE = "#ffffff";
const BORDER = "#e2e8f0";

// ─── Helper: parse JSON array stored as string ────────────────────────────────
function parseJsonArray(val: string | null | undefined): string[] {
  if (!val) return [];
  try {
    const parsed = JSON.parse(val);
    return Array.isArray(parsed) ? parsed.map(String) : [];
  } catch {
    // Fallback: semicolon-separated
    return val
      .split(";")
      .map((s) => s.trim())
      .filter(Boolean);
  }
}

// ─── Geração do PDF ───────────────────────────────────────────────────────────
async function generatePositionsPDF(
  category: string,
  siglas: string[],
  res: Response
) {
  const allEntries = await getPositionsByCategory(category);

  // Filtrar por siglas se necessário
  const entries =
    siglas.length > 0
      ? allEntries.filter((e) => siglas.includes(e.state?.sigla ?? ""))
      : allEntries;

  if (entries.length === 0) {
    res.status(404).json({ error: "Nenhum dado encontrado para os filtros informados." });
    return;
  }

  const categoryLabel =
    category === "chefe-co"
      ? "Chefe do Órgão Operacional"
      : category === "chefe-dat"
      ? "Chefe do Órgão Técnico"
      : category;

  const dateStr = new Date().toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  const doc = new PDFDocument({
    size: "A4",
    margin: 0,
    info: {
      Title: `Comparativo de Cargos — ${categoryLabel}`,
      Author: "Portal de Legislação dos CBM",
      Subject: "Corpos de Bombeiros Militares — Estrutura Organizacional",
    },
  });

  res.setHeader("Content-Type", "application/pdf");
  res.setHeader(
    "Content-Disposition",
    `attachment; filename="comparativo-cargos-${category}.pdf"`
  );
  doc.pipe(res);

  const PAGE_W = doc.page.width;
  const PAGE_H = doc.page.height;
  const MARGIN = 28;
  const CONTENT_W = PAGE_W - MARGIN * 2;
  const COL_W = (CONTENT_W - 12) / 2;

  let pageNum = 0;

  function drawRect(
    x: number,
    y: number,
    w: number,
    h: number,
    color: string,
    radius = 0
  ) {
    doc.save().roundedRect(x, y, w, h, radius).fill(color).restore();
  }

  function drawHeader() {
    pageNum++;
    drawRect(0, 0, PAGE_W, 64, NAVY);
    doc
      .font("Helvetica-Bold")
      .fontSize(11)
      .fillColor(WHITE)
      .text("Portal de Legislação dos Corpos de Bombeiros Militares", MARGIN, 14, {
        width: CONTENT_W - 120,
      });
    doc
      .font("Helvetica")
      .fontSize(8.5)
      .fillColor("#94a3b8")
      .text(`Comparativo: ${categoryLabel}`, MARGIN, 30, { width: CONTENT_W - 120 });
    doc
      .font("Helvetica")
      .fontSize(8)
      .fillColor("#94a3b8")
      .text(`Gerado em: ${dateStr}`, PAGE_W - MARGIN - 120, 14, {
        width: 120,
        align: "right",
      })
      .text(`Página ${pageNum}`, PAGE_W - MARGIN - 120, 26, {
        width: 120,
        align: "right",
      });
    drawRect(0, 64, PAGE_W, 3, RED);
  }

  function drawFooter() {
    drawRect(0, PAGE_H - 24, PAGE_W, 24, LIGHT_GRAY);
    doc
      .font("Helvetica")
      .fontSize(7.5)
      .fillColor(MID_GRAY)
      .text(
        "Portal de Legislação dos Corpos de Bombeiros Militares — Uso Institucional",
        MARGIN,
        PAGE_H - 16,
        { width: CONTENT_W, align: "center" }
      );
  }

  // ─── Primeira página ────────────────────────────────────────────────────────
  drawHeader();
  drawFooter();

  let curY = 80;
  let col = 0; // 0 = esquerda, 1 = direita

  function getColX(c: number) {
    return MARGIN + c * (COL_W + 12);
  }

  for (const entry of entries) {
    const { position: pos, operationalCommand: oc, technicalDirectorate: td, state } = entry;

    const stateSigla = state?.sigla ?? "";
    const stateName = state?.name ?? "";
    const orgName = oc?.nomenclature ?? td?.nomenclature ?? "";
    const orgAcronym = oc?.acronym ?? td?.acronym ?? "";
    const positionName = pos.title;
    const positionAcronym = pos.acronym ?? "";
    const rankOrGrade = pos.rank ?? "";
    const subordinateTo = pos.subordinateTo ?? "";
    const subdivisions = parseJsonArray(pos.subordinates);
    const attributions = parseJsonArray(pos.attributions);

    // Estimar altura do card
    let cardH = 36; // faixa de cabeçalho (estado + org)
    cardH += 14; // nome do cargo
    if (positionAcronym) cardH += 18; // badge
    const fieldCount = [orgName, rankOrGrade, subordinateTo].filter(Boolean).length;
    cardH += fieldCount * 12;
    if (subdivisions.length > 0) {
      cardH += 14 + subdivisions.length * 11;
    }
    if (attributions.length > 0) {
      cardH += 14;
      const shown = attributions.slice(0, 3);
      for (const attr of shown) {
        const lines = Math.ceil(attr.length / 55);
        cardH += Math.max(1, lines) * 10;
      }
      if (attributions.length > 3) cardH += 10;
    }
    cardH += 10; // padding inferior

    const BOTTOM_LIMIT = PAGE_H - 36;

    // Se não cabe na coluna atual, tentar a outra ou nova página
    if (curY + cardH > BOTTOM_LIMIT) {
      if (col === 0) {
        // Tentar coluna direita — mas só se o card cabe a partir do topo atual
        // Se também não cabe, nova página
        if (curY + cardH > BOTTOM_LIMIT) {
          doc.addPage({ size: "A4", margin: 0 });
          drawHeader();
          drawFooter();
          curY = 80;
          col = 0;
        } else {
          col = 1;
        }
      } else {
        doc.addPage({ size: "A4", margin: 0 });
        drawHeader();
        drawFooter();
        curY = 80;
        col = 0;
      }
    }

    const cx = getColX(col);

    // ── Card background ──
    drawRect(cx, curY, COL_W, cardH, WHITE);
    doc
      .save()
      .roundedRect(cx, curY, COL_W, cardH, 6)
      .lineWidth(0.5)
      .strokeColor(BORDER)
      .stroke()
      .restore();

    // ── Faixa de cabeçalho do card ──
    drawRect(cx, curY, COL_W, 36, LIGHT_GRAY, 6);

    // Sigla e nome do estado
    doc
      .font("Helvetica-Bold")
      .fontSize(13)
      .fillColor(NAVY)
      .text(stateSigla, cx + 8, curY + 6, { width: 28 });
    doc
      .font("Helvetica-Bold")
      .fontSize(8.5)
      .fillColor(DARK)
      .text(stateName, cx + 36, curY + 6, { width: COL_W - 44 });
    doc
      .font("Helvetica")
      .fontSize(7)
      .fillColor(MID_GRAY)
      .text(orgName, cx + 36, curY + 18, { width: COL_W - 44 });

    let y = curY + 42;

    // ── Nome do cargo ──
    doc
      .font("Helvetica-Bold")
      .fontSize(9)
      .fillColor(DARK)
      .text(positionName, cx + 8, y, { width: COL_W - 16 });
    y += 14;

    // ── Badge da sigla ──
    if (positionAcronym) {
      const badgeW = Math.min(doc.widthOfString(positionAcronym) + 10, COL_W - 20);
      drawRect(cx + 8, y, badgeW, 14, LIGHT_GRAY, 3);
      doc
        .font("Helvetica")
        .fontSize(7)
        .fillColor(MID_GRAY)
        .text(positionAcronym, cx + 13, y + 3, { width: badgeW - 6 });
      y += 18;
    }

    // ── Campos ──
    const fields: [string, string][] = [
      ["Órgão", orgAcronym ? `${orgName} (${orgAcronym})` : orgName],
      ["Posto/Grad.", rankOrGrade],
      ["Subordinado a", subordinateTo],
    ].filter(([, v]) => !!v) as [string, string][];

    for (const [label, value] of fields) {
      doc
        .font("Helvetica-Bold")
        .fontSize(7)
        .fillColor(MID_GRAY)
        .text(`${label}: `, cx + 8, y, { continued: true, width: COL_W - 16 });
      doc
        .font("Helvetica")
        .fontSize(7)
        .fillColor(DARK)
        .text(value, { width: COL_W - 16 });
      y += 12;
    }

    // ── Subdivisões ──
    if (subdivisions.length > 0) {
      y += 2;
      doc
        .font("Helvetica-Bold")
        .fontSize(7)
        .fillColor(RED)
        .text("Subdivisões / Desdobramentos", cx + 8, y, { width: COL_W - 16 });
      y += 12;
      for (const sub of subdivisions) {
        doc
          .font("Helvetica")
          .fontSize(7)
          .fillColor(DARK)
          .text(`• ${sub}`, cx + 12, y, { width: COL_W - 20 });
        y += 11;
      }
    }

    // ── Atribuições (primeiras 3) ──
    if (attributions.length > 0) {
      y += 2;
      doc
        .font("Helvetica-Bold")
        .fontSize(7)
        .fillColor(RED)
        .text("Atribuições", cx + 8, y, { width: COL_W - 16 });
      y += 12;
      const shown = attributions.slice(0, 3);
      for (const attr of shown) {
        doc
          .font("Helvetica")
          .fontSize(7)
          .fillColor(DARK)
          .text(`• ${attr}`, cx + 12, y, { width: COL_W - 20 });
        y += doc.heightOfString(`• ${attr}`, { width: COL_W - 20 }) + 2;
      }
      if (attributions.length > 3) {
        doc
          .font("Helvetica")
          .fontSize(6.5)
          .fillColor(MID_GRAY)
          .text(`e mais ${attributions.length - 3} atribuição(ões)...`, cx + 12, y, {
            width: COL_W - 20,
          });
        y += 10;
      }
    }

    // Avançar posição
    if (col === 0) {
      // Coluna esquerda preenchida; coluna direita começa na mesma linha
      col = 1;
    } else {
      // Ambas as colunas preenchidas; avançar para próxima linha
      curY = curY + cardH + 10;
      col = 0;
    }
  }

  doc.end();
}

// ─── Rota Express ─────────────────────────────────────────────────────────────
export function registerPDFRoutes(app: Express) {
  app.get("/api/pdf/positions", async (req: Request, res: Response) => {
    try {
      const category = (req.query.category as string) || "chefe-co";
      const siglasParam = (req.query.siglas as string) || "";
      const siglas = siglasParam
        ? siglasParam
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean)
        : [];

      await generatePositionsPDF(category, siglas, res);
    } catch (err) {
      console.error("[PDF] Error generating PDF:", err);
      if (!res.headersSent) {
        res.status(500).json({ error: "Erro ao gerar PDF." });
      }
    }
  });
}
