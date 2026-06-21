"""
generate_text_pdfs.py — Portal CBM
Gera PDFs formatados a partir do texto verbatim já curado em database/markdown/
para legislações sem PDF de origem digitalizado disponível (PE, SE, SP).
Cada PDF leva uma nota de rodapé deixando claro que é um documento gerado a
partir do texto oficial consolidado, não a reprodução digitalizada da
publicação original. Não roda como parte do pipeline padrão — é pontual.
"""

import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

BASE_DIR = Path(__file__).parent.parent
MD_DIR = BASE_DIR / "database" / "markdown"
PDF_DIR = BASE_DIR / "LEGISLAÇÃO CBMS"

styles = getSampleStyleSheet()
body_style = ParagraphStyle("Body", parent=styles["Normal"], fontName="Times-Roman",
                             fontSize=11, leading=15, alignment=TA_JUSTIFY, spaceAfter=6)
title_style = ParagraphStyle("Title2", parent=styles["Normal"], fontName="Times-Bold",
                              fontSize=13, leading=17, alignment=TA_CENTER, spaceAfter=10)
footer_style = ParagraphStyle("Footer", parent=styles["Normal"], fontName="Times-Italic",
                               fontSize=8, leading=11, alignment=TA_JUSTIFY, textColor="#555555")


def clean_lines(raw_lines):
    """Remove linhas vazias/whitespace-only."""
    lines = [l.strip() for l in raw_lines]
    lines = [l for l in lines if l]
    return lines


PARA_BREAK_RE = re.compile(
    r"(?=(?:Art\.\s*\d|Parágrafo único|§\s*\d|T[ÍI]TULO\s|CAP[ÍI]TULO\s|SEÇÃO\s|"
    r"Palácio\s|Aracaju,|Recife,|São Paulo,))"
)


def reflow_paragraphs(lines):
    """Junta linhas quebradas no meio da frase (herdadas do HTML de origem) em
    parágrafos completos, abrindo um novo parágrafo só nos marcadores legais
    (Art., §, TÍTULO, CAPÍTULO, incisos romanos) ou na assinatura final."""
    joined = " ".join(lines)
    joined = re.sub(r"\s+", " ", joined).strip()
    parts = [p.strip() for p in PARA_BREAK_RE.split(joined) if p.strip()]
    return parts


def build_pdf(out_path: Path, heading_lines: list[str], body_lines: list[str], source_note: str):
    doc = SimpleDocTemplate(str(out_path), pagesize=A4,
                             topMargin=2.2 * cm, bottomMargin=2.2 * cm,
                             leftMargin=2.5 * cm, rightMargin=2.5 * cm)
    flow = []
    for h in heading_lines:
        flow.append(Paragraph(h, title_style))
    flow.append(Spacer(1, 8))
    for p in body_lines:
        flow.append(Paragraph(p, body_style))
    flow.append(Spacer(1, 16))
    flow.append(Paragraph(
        "Documento gerado a partir do texto oficial consolidado da legislação pelo "
        "Portal de Legislação dos Corpos de Bombeiros Militares — não é a reprodução "
        "digitalizada da publicação original. " + source_note,
        footer_style
    ))
    doc.build(flow)
    print(f"Gerado: {out_path.name}")


def pe():
    text = (MD_DIR / "Pernambuco - Organização Básica (Lei 15.187-2013).md").read_text(encoding="utf-8")
    lines = text.splitlines()
    start = next(i for i, l in enumerate(lines) if l.strip() == "LEI Nº 15.187, DE")
    end = next(i for i, l in enumerate(lines) if "não substitui o publicado" in l)
    body = clean_lines(lines[start:end])
    # Linhas 0-1: número/data da lei; linha 2 em diante: ementa + corpo
    heading = [" ".join(body[0:2])]
    rest = reflow_paragraphs(body[2:])
    heading.append(rest[0])  # ementa ("Dispõe sobre...")
    rest = rest[1:]
    build_pdf(
        PDF_DIR / "Pernambuco - Organização Básica (Lei 15.187-2013).pdf",
        heading, rest,
        "Fonte: Alepe Legis — Portal da Legislação Estadual de Pernambuco (legis.alepe.pe.gov.br)."
    )


def se():
    text = (MD_DIR / "Sergipe - Organização Básica (Lei 8.979-2022).md").read_text(encoding="utf-8")
    lines = text.splitlines()
    start = next(i for i, l in enumerate(lines) if "Secretaria-Geral da Mesa Diretora" in l) + 1
    start = next(i for i in range(start, len(lines)) if "LEI Nº 8.979" in lines[i])
    body = clean_lines(lines[start:])
    heading = [" ".join(body[0:2])]
    rest = reflow_paragraphs(body[2:])
    heading.append(rest[0])
    rest = rest[1:]
    build_pdf(
        PDF_DIR / "Sergipe - Organização Básica (Lei 8.979-2022).pdf",
        heading, rest,
        "Fonte: Alese Legis — Assembleia Legislativa do Estado de Sergipe (aleselegis.al.se.leg.br)."
    )


def sp():
    text = (MD_DIR / "São Paulo - Organização Básica (Lei 616-1974).md").read_text(encoding="utf-8")
    lines = text.splitlines()
    start = next(i for i, l in enumerate(lines) if l.strip() == "LEI Nº 616, DE 17 DE DEZEMBRO DE 1974")
    body = clean_lines(lines[start:])
    heading = [body[0], body[1]]
    rest = reflow_paragraphs(body[2:])
    heading.append(rest[0])
    rest = rest[1:]
    build_pdf(
        PDF_DIR / "São Paulo - Organização Básica (Lei 616-1974).pdf",
        heading, rest,
        "Fonte: Assembleia Legislativa do Estado de São Paulo (al.sp.gov.br)."
    )


if __name__ == "__main__":
    pe()
    se()
    sp()
