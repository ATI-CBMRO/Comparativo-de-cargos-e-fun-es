import type { Express, Request, Response } from "express";
import PDFDocument from "pdfkit";
import { getPositionsByCategory, getFilteredData, getPositionsByOperationalCommand, getPositionsByTechnicalDirectorate } from "./db";

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

// ─── Geração do PDF Comparativo ─────────────────────────────────────────────
// Estima a altura necessária para renderizar um org no PDF
function estimateOrgHeight(
  org: { nomenclature: string; acronym: string | null; subdivisions: string | null; attributions: string | null; legalBasis: string | null } | null,
  positionsList: { title: string; rank: string | null }[],
  colW: number
): number {
  if (!org) return 44;
  let h = 36; // card header
  if (org.subdivisions) {
    const subs = org.subdivisions.split(";").filter(Boolean);
    if (subs.length > 0) {
      h += 14;
      for (const sub of subs.slice(0, 4)) {
        h += Math.ceil(sub.length / (colW / 4.5)) * 9 + 1;
      }
      if (subs.length > 4) h += 9;
      h += 4;
    }
  }
  if (org.attributions) {
    const attrs = org.attributions.split(";").filter(Boolean);
    if (attrs.length > 0) {
      h += 14;
      for (const attr of attrs.slice(0, 3)) {
        h += Math.ceil(attr.length / (colW / 4.5)) * 9 + 1;
      }
      if (attrs.length > 3) h += 9;
      h += 4;
    }
  }
  if (positionsList.length > 0) {
    h += 14;
    for (const pos of positionsList.slice(0, 5)) {
      h += 9;
      if (pos.rank) h += 8;
    }
    if (positionsList.length > 5) h += 9;
  }
  if (org.legalBasis) h += 13;
  return h + 10;
}

async function generateComparativePDF(
  siglas: string[],
  res: Response
) {
  const entries = await getFilteredData({ siglas });

  if (entries.length === 0) {
    res.status(404).json({ error: "Nenhum estado encontrado para os filtros informados." });
    return;
  }

  // Buscar posições de cada estado
  const enriched = await Promise.all(
    entries.map(async (entry) => {
      const ocPositions = entry.operationalCommand
        ? await getPositionsByOperationalCommand(entry.operationalCommand.id)
        : [];
      const tdPositions = entry.technicalDirectorate
        ? await getPositionsByTechnicalDirectorate(entry.technicalDirectorate.id)
        : [];
      return { ...entry, ocPositions, tdPositions };
    })
  );

  const dateStr = new Date().toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  const stateLabel = siglas.length > 0 ? siglas.join(", ") : "Todos os estados";

  const doc = new PDFDocument({
    size: "A4",
    layout: "landscape",
    margin: 0,
    autoFirstPage: false,
    info: {
      Title: `Comparativo entre Estados — ${stateLabel}`,
      Author: "Portal de Legislação dos CBM",
      Subject: "Corpos de Bombeiros Militares — Estrutura Organizacional",
    },
  });

  res.setHeader("Content-Type", "application/pdf");
  res.setHeader(
    "Content-Disposition",
    `attachment; filename="comparativo-estados-${siglas.join("-")}.pdf"`
  );
  doc.pipe(res);

  // A4 landscape: 841.89 x 595.28 pts
  const PAGE_W = 841.89;
  const PAGE_H = 595.28;
  const MARGIN = 24;
  const CONTENT_W = PAGE_W - MARGIN * 2;
  const numCols = enriched.length;
  const COL_W = (CONTENT_W - (numCols - 1) * 8) / numCols;
  const BOTTOM_LIMIT = PAGE_H - 28;

  let pageNum = 0;

  function drawRect(x: number, y: number, w: number, h: number, color: string, radius = 0) {
    doc.save().roundedRect(x, y, w, h, radius).fill(color).restore();
  }

  function drawHeader() {
    pageNum++;
    doc.addPage({ size: "A4", layout: "landscape", margin: 0 });
    drawRect(0, 0, PAGE_W, 56, NAVY);
    doc
      .font("Helvetica-Bold")
      .fontSize(10)
      .fillColor(WHITE)
      .text("Portal de Legislação dos Corpos de Bombeiros Militares", MARGIN, 10, {
        width: CONTENT_W - 120,
      });
    doc
      .font("Helvetica")
      .fontSize(8)
      .fillColor("#94a3b8")
      .text(`Comparativo entre estados: ${stateLabel}`, MARGIN, 24, { width: CONTENT_W - 120 });
    doc
      .font("Helvetica")
      .fontSize(7.5)
      .fillColor("#94a3b8")
      .text(`Gerado em: ${dateStr}`, PAGE_W - MARGIN - 120, 10, { width: 120, align: "right" })
      .text(`Página ${pageNum}`, PAGE_W - MARGIN - 120, 22, { width: 120, align: "right" });
    drawRect(0, 56, PAGE_W, 3, RED);
  }

  function drawFooter() {
    drawRect(0, PAGE_H - 20, PAGE_W, 20, LIGHT_GRAY);
    doc
      .font("Helvetica")
      .fontSize(7)
      .fillColor(MID_GRAY)
      .text(
        "Portal de Legislação dos Corpos de Bombeiros Militares — Uso Institucional",
        MARGIN,
        PAGE_H - 13,
        { width: CONTENT_W, align: "center" }
      );
  }

  function getColX(i: number) {
    return MARGIN + i * (COL_W + 8);
  }

  // ─── Seção helper ────────────────────────────────────────────────────────
  // Helper para escrever texto apenas se Y estiver dentro do limite da página
  function safeText(
    text: string,
    x: number,
    y: number,
    options: { width?: number; align?: string; lineBreak?: boolean } = {}
  ): void {
    if (y < BOTTOM_LIMIT) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      doc.text(text, x, y, options as any);
    }
  }

  function drawSection(
    label: string,
    color: string,
    startY: number,
    stateEntries: typeof enriched
  ): number {
    let maxBottom = startY;

    for (let i = 0; i < stateEntries.length; i++) {
      const entry = stateEntries[i];
      const cx = getColX(i);
      let y = startY;

      const isOC = label === "Comando Operacional";
      const org = isOC ? entry.operationalCommand : entry.technicalDirectorate;
      const positionsList = isOC ? entry.ocPositions : entry.tdPositions;

      if (!org) {
        // Sem dados
        if (y + 40 < BOTTOM_LIMIT) {
          drawRect(cx, y, COL_W, 40, LIGHT_GRAY, 4);
          doc
            .font("Helvetica")
            .fontSize(7.5)
            .fillColor(MID_GRAY)
            .text("Sem dados disponíveis", cx + 8, y + 14, { width: COL_W - 16 });
        }
        maxBottom = Math.max(maxBottom, y + 40);
        continue;
      }

      // Card header
      if (y + 28 < BOTTOM_LIMIT) {
        drawRect(cx, y, COL_W, 28, LIGHT_GRAY, 4);
        doc
          .font("Helvetica-Bold")
          .fontSize(9)
          .fillColor(NAVY)
          .text(org.nomenclature, cx + 8, y + 5, { width: COL_W - 16 });
        if (org.acronym) {
          doc
            .font("Helvetica")
            .fontSize(7)
            .fillColor(MID_GRAY)
            .text(`(${org.acronym})`, cx + 8, y + 17, { width: COL_W - 16 });
        }
      }
      y += 32;

      // Subdivisões
      if (org.subdivisions) {
        const subs = org.subdivisions.split(";").map((s: string) => s.trim()).filter(Boolean);
        if (subs.length > 0 && y < BOTTOM_LIMIT) {
          doc.font("Helvetica-Bold").fontSize(6.5).fillColor(RED);
          safeText("DESDOBRAMENTOS", cx + 8, y, { width: COL_W - 16 });
          y += 10;
          for (const sub of subs.slice(0, 4)) {
            if (y >= BOTTOM_LIMIT) break;
            doc.font("Helvetica").fontSize(6.5).fillColor(DARK);
            safeText(`• ${sub}`, cx + 10, y, { width: COL_W - 18 });
            y += doc.heightOfString(`• ${sub}`, { width: COL_W - 18 }) + 1;
          }
          if (subs.length > 4 && y < BOTTOM_LIMIT) {
            doc.font("Helvetica").fontSize(6).fillColor(MID_GRAY);
            safeText(`+${subs.length - 4} mais...`, cx + 10, y, { width: COL_W - 18 });
            y += 9;
          }
          y += 4;
        }
      }

      // Atribuições
      if (org.attributions) {
        const attrs = org.attributions.split(";").map((s: string) => s.trim()).filter(Boolean);
        if (attrs.length > 0 && y < BOTTOM_LIMIT) {
          doc.font("Helvetica-Bold").fontSize(6.5).fillColor(RED);
          safeText("ATRIBUIÇÕES", cx + 8, y, { width: COL_W - 16 });
          y += 10;
          for (const attr of attrs.slice(0, 3)) {
            if (y >= BOTTOM_LIMIT) break;
            doc.font("Helvetica").fontSize(6.5).fillColor(DARK);
            safeText(`• ${attr}`, cx + 10, y, { width: COL_W - 18 });
            y += doc.heightOfString(`• ${attr}`, { width: COL_W - 18 }) + 1;
          }
          if (attrs.length > 3 && y < BOTTOM_LIMIT) {
            doc.font("Helvetica").fontSize(6).fillColor(MID_GRAY);
            safeText(`+${attrs.length - 3} mais...`, cx + 10, y, { width: COL_W - 18 });
            y += 9;
          }
          y += 4;
        }
      }

      // Cargos
      if (positionsList.length > 0 && y < BOTTOM_LIMIT) {
        doc.font("Helvetica-Bold").fontSize(6.5).fillColor(RED);
        safeText(`CARGOS (${positionsList.length})`, cx + 8, y, { width: COL_W - 16 });
        y += 10;
        for (const pos of positionsList.slice(0, 5)) {
          if (y >= BOTTOM_LIMIT) break;
          doc.font("Helvetica-Bold").fontSize(6.5).fillColor(DARK);
          safeText(pos.title, cx + 8, y, { width: COL_W - 16 });
          y += 9;
          if (pos.rank && y < BOTTOM_LIMIT) {
            doc.font("Helvetica").fontSize(6).fillColor(MID_GRAY);
            safeText(pos.rank, cx + 10, y, { width: COL_W - 18 });
            y += 8;
          }
        }
        if (positionsList.length > 5 && y < BOTTOM_LIMIT) {
          doc.font("Helvetica").fontSize(6).fillColor(MID_GRAY);
          safeText(`+${positionsList.length - 5} cargos...`, cx + 10, y, { width: COL_W - 18 });
          y += 9;
        }
      }

      // Base legal
      if (org.legalBasis && y + 13 < BOTTOM_LIMIT) {
        y += 4;
        doc.font("Helvetica").fontSize(6).fillColor(MID_GRAY);
        safeText(`Base legal: ${org.legalBasis}`, cx + 8, y, { width: COL_W - 16 });
        y += 9;
      }

      maxBottom = Math.max(maxBottom, y + 6);
    }

    return maxBottom;
  }

  // ─── Página 1: Cabeçalho de estados + CO ────────────────────────────────
  drawHeader();
  drawFooter();

  let curY = 68;

  // Cabeçalhos dos estados
  for (let i = 0; i < enriched.length; i++) {
    const entry = enriched[i];
    const cx = getColX(i);
    drawRect(cx, curY, COL_W, 36, NAVY, 6);
    doc
      .font("Helvetica-Bold")
      .fontSize(14)
      .fillColor(WHITE)
      .text(entry.state.sigla, cx + 8, curY + 6, { width: 30 });
    doc
      .font("Helvetica")
      .fontSize(8)
      .fillColor("#94a3b8")
      .text(entry.state.name, cx + 42, curY + 6, { width: COL_W - 50 });
    if (entry.state.region) {
      doc
        .font("Helvetica")
        .fontSize(7)
        .fillColor("#64748b")
        .text(entry.state.region, cx + 42, curY + 18, { width: COL_W - 50 });
    }
  }
  curY += 44;

  // Título da seção CO
  drawRect(MARGIN, curY, CONTENT_W, 18, RED, 3);
  doc
    .font("Helvetica-Bold")
    .fontSize(8)
    .fillColor(WHITE)
    .text("COMANDO OPERACIONAL", MARGIN + 8, curY + 5, { width: CONTENT_W - 16 });
  curY += 22;

  const afterCO = drawSection("Comando Operacional", RED, curY, enriched);
  curY = afterCO + 10;

  // Verificar se DAT cabe na mesma página
  if (curY + 60 > BOTTOM_LIMIT) {
    doc.addPage({ size: "A4", layout: "landscape", margin: 0 });
    drawHeader();
    drawFooter();
    curY = 68;
  }

  // Título da seção DAT
  drawRect(MARGIN, curY, CONTENT_W, 18, "#1e3a5f", 3);
  doc
    .font("Helvetica-Bold")
    .fontSize(8)
    .fillColor(WHITE)
    .text("DIRETORIA DE ATIVIDADES TÉCNICAS", MARGIN + 8, curY + 5, { width: CONTENT_W - 16 });
  curY += 22;

  drawSection("Diretoria de Atividades Técnicas", "#1e3a5f", curY, enriched);

  doc.flushPages();
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

  app.get("/api/pdf/comparative", async (req: Request, res: Response) => {
    try {
      const siglasParam = (req.query.siglas as string) || "";
      const siglas = siglasParam
        ? siglasParam
            .split(",")
            .map((s) => s.trim())
            .filter(Boolean)
        : [];
      await generateComparativePDF(siglas, res);
    } catch (err) {
      console.error("[PDF] Error generating comparative PDF:", err);
      if (!res.headersSent) {
        res.status(500).json({ error: "Erro ao gerar PDF comparativo." });
      }
    }
  });
}
