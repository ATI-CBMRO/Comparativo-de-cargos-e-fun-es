"""
build_decisoes_curadoria.py — Portal CBM (cockpit de curadoria, Fase 2)

Lê as 36 notas de Decisão do vault Obsidian (fora do repo) e gera
database/decisoes_curadoria.json — material de LEITURA para a aba Decisões.
Só leitura: não decide nada, não toca a estrutura da minuta.

Arquivo ÚNICO para os 2 cenários, mas cada decisão declara em QUAIS ela vale (campo
`cenarios`) — o RI é por ÓRGÃO e portanto específico da LOB de cada cenário; o
Regulamento é temático e vale nos dois. Ver _cenarios() e o espelho em
src/lib/decisoes.js (cenariosDaDecisao).

Rodar: .venv-pipeline/bin/python scripts/build_decisoes_curadoria.py
Valida: cd scripts && ../.venv-pipeline/bin/python -m pytest test_decisoes_curadoria.py -q
"""
import json
import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUT_JSON = BASE_DIR / "database" / "decisoes_curadoria.json"

DEFAULT_VAULT = Path.home() / "Documents" / "Obsidian Vault" / "Codebases" / "Comparativo-de-cargos-e-funcoes"
VAULT_CURADORIA = Path(os.environ.get("VAULT_CURADORIA", str(DEFAULT_VAULT)))

SUBPASTAS = {
    "ri":  "Regimento Interno — Curadoria",
    "reg": "Regulamento — Curadoria",
}

FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _frontmatter(texto):
    m = FRONT_RE.match(texto)
    fm = {}
    if m:
        for linha in m.group(1).splitlines():
            if ":" in linha:
                k, v = linha.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm


def _secoes(corpo):
    """Divide o corpo (sem frontmatter) em {titulo_h2: texto} + o texto antes do 1º H2."""
    partes = re.split(r"^## +", corpo, flags=re.MULTILINE)
    intro = partes[0]
    secs = {}
    for p in partes[1:]:
        nome, _, resto = p.partition("\n")
        secs[nome.strip()] = resto
    return intro, secs


def _parse_candidatas(texto):
    """Cada '### Fonte' vira {fonte, verbatim[], citacao, ocr, leitura}."""
    out = []
    for bloco in re.split(r"^### +", texto, flags=re.MULTILINE)[1:]:
        fonte, _, corpo = bloco.partition("\n")
        verbatim, citacao, ocr, leitura = [], None, None, None
        for linha in corpo.splitlines():
            s = linha.rstrip()
            if s.startswith("> "):
                verbatim.append(s[2:])
            elif s.startswith("`cf.") and s.endswith("`"):
                citacao = s.strip("`")
            elif s.startswith("*(") and s.endswith(")*"):
                ocr = s[2:-2]
            elif s.startswith("**Leitura:**"):
                leitura = s[len("**Leitura:**"):].strip()
        out.append({
            "fonte": fonte.strip(), "verbatim": verbatim,
            "citacao": citacao, "ocr": ocr, "leitura": leitura,
        })
    return out


def _limpar_wikilinks(texto):
    return re.sub(r"\[\[([^\]]+)\]\]", r"\1", texto)


def _bullets(texto):
    return [_limpar_wikilinks(l[2:].strip()) for l in texto.splitlines() if l.startswith("- ")]


def _wikilinks(texto):
    return re.findall(r"\[\[([^\]]+)\]\]", texto)


def _questao_legado(secs):
    texto = secs.get("O problema") or secs.get("Contexto") or ""
    # primeiro parágrafo (até linha em branco ou até um heading '##'/'|' de tabela)
    linhas = []
    for linha in texto.splitlines():
        if not linha.strip():
            if linhas:
                break
            continue
        if linha.strip().startswith("|"):
            break
        linhas.append(linha.strip())
    return _limpar_wikilinks(" ".join(linhas))


HEADER_LEGADO_RE = re.compile(r"^\*\*(.+?)\*\*\s*(\(.*\))?\s*:?\s*$")
CF_RE = re.compile(r"cf\.\s*([^)`]+)")


def _parse_candidatas_legado(texto):
    """'## Excertos verbatim' do template antigo: cada linha em negrito seguida de
    blockquote(s) e, opcionalmente, uma nota OCR entre asteriscos-parênteses (podendo
    se estender por várias linhas)."""
    out = None
    candidatas = []
    coletando_ocr = None  # buffer de linhas quando uma nota OCR abre em uma linha e fecha em outra
    for linha in texto.splitlines():
        s = linha.rstrip()
        if coletando_ocr is not None:
            coletando_ocr.append(s.strip())
            if s.strip().endswith(")*"):
                bruto = " ".join(coletando_ocr)
                out["ocr"] = bruto[2:-2] if bruto.startswith("*(") else bruto.strip("*()")
                coletando_ocr = None
            continue
        m = HEADER_LEGADO_RE.match(s.strip())
        if m and s.strip().startswith("**"):
            if out is not None:
                candidatas.append(out)
            header_plano = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s.strip())
            header_plano = header_plano.replace("**", "").rstrip(":").strip()
            parentetico = (m.group(2) or "").strip()
            if parentetico.startswith("(") and parentetico.endswith(")"):
                parentetico = parentetico[1:-1]
            cf_match = re.search(r"cf\.\s*([^`]+)", parentetico) or CF_RE.search(s)
            out = {
                "fonte": header_plano,
                "verbatim": [],
                "citacao": ("cf. " + cf_match.group(1).strip()) if cf_match else None,
                "ocr": None,
                "leitura": None,
            }
        elif out is not None:
            if s.startswith("> "):
                out["verbatim"].append(s[2:].strip('"'))
            elif s.strip().startswith("*(") and s.strip().endswith(")*"):
                out["ocr"] = s.strip()[2:-2]
            elif s.strip().startswith("*(") and not s.strip().endswith(")*"):
                coletando_ocr = [s.strip()]
            elif s.startswith("**Leitura:**"):
                out["leitura"] = s[len("**Leitura:**"):].strip()
    if out is not None:
        candidatas.append(out)
    return candidatas


def _comparacao_legado(secs):
    if secs.get("Divergência"):
        texto = secs["Divergência"]
        paragrafos = [_limpar_wikilinks(" ".join(p.split())) for p in re.split(r"\n\s*\n", texto) if p.strip()]
        return paragrafos
    for nome, texto in secs.items():
        if texto.strip().startswith("|") or "\n|" in texto:
            linhas = [l.strip() for l in texto.splitlines() if l.strip().startswith("|")]
            linhas = [l for l in linhas if not re.match(r"^\|[\s\-\|]+\|$", l)]
            bullets = []
            for l in linhas[1:]:  # pula a linha de cabeçalho da tabela
                cols = [c.strip() for c in l.strip("|").split("|")]
                if len(cols) >= 3:
                    bullets.append(_limpar_wikilinks(f"{cols[0]}: {cols[1]} — {cols[2]}"))
            if bullets:
                return bullets
    return []


CENARIOS_VALIDOS = ("atual", "futura")


def _cenarios(fm, trilha):
    """Cenários em que a decisão vale, do frontmatter (`cenarios: atual, futura`).

    Sem o campo, cai no padrão da REGRA DE PRODUTO (CLAUDE.md): o Regimento Interno é
    organizado por ÓRGÃO — logo é específico da LOB — e toda a curadoria existente foi
    redigida sobre a LOB FUTURA; o Regulamento é TEMÁTICO (serviço/disciplina/ensino),
    não depende da LOB e vale nos dois. Espelha cenariosDaDecisao() de src/lib/decisoes.js.
    """
    bruto = fm.get("cenarios") or fm.get("cenario") or ""
    vals = [c.strip().strip('[]"\'') for c in bruto.split(",")]
    vals = [c for c in vals if c in CENARIOS_VALIDOS]
    if vals:
        return vals
    return list(CENARIOS_VALIDOS) if trilha == "reg" else ["futura"]


def parse_decisao(texto, arquivo, trilha):
    fm = _frontmatter(texto)
    key = fm.get("organKey") or fm.get("themeKey")
    if not key:
        raise ValueError(f"{arquivo}: sem organKey/themeKey no frontmatter")
    corpo = FRONT_RE.sub("", texto, count=1)
    intro, secs = _secoes(corpo)

    is_legado = "Redações candidatas" not in secs and "Excertos verbatim" in secs

    mtit = re.search(r"^# +(.*)$", intro, flags=re.MULTILINE)
    titulo = mtit.group(1).strip() if mtit else Path(arquivo).stem
    if is_legado:
        questao = _questao_legado(secs)
        if not questao:
            raise ValueError(f"{arquivo}: formato legado sem '## O problema' nem '## Contexto'")
    else:
        mq = re.search(r"\*\*Questão:\*\*\s*(.+?)(?:\n\n|\Z)", intro, flags=re.DOTALL)
        if not mq:
            raise ValueError(f"{arquivo}: sem **Questão:**")
        questao = _limpar_wikilinks(" ".join(mq.group(1).split()))

    dec_txt = (secs.get("Decisão CBMRO") or "").strip()
    is_placeholder = dec_txt.startswith("_(") or dec_txt.startswith("<!--") or not dec_txt
    decidido = fm.get("decidido", "false").lower() == "true"
    decisao = None if is_placeholder else dec_txt

    if is_legado:
        candidatas = _parse_candidatas_legado(secs.get("Excertos verbatim", ""))
        comparacao = _comparacao_legado(secs)
        ligadas = _wikilinks(corpo)
    else:
        candidatas = _parse_candidatas(secs.get("Redações candidatas", ""))
        comparacao = _bullets(secs.get("Comparação", ""))
        ligadas = _wikilinks(secs.get("Ligações", ""))

    return {
        "id": Path(arquivo).stem,
        "trilha": trilha,
        "cenarios": _cenarios(fm, trilha),
        "key": key,
        "chapterId": ("organ:" if trilha == "ri" else "reg:") + key,
        "titulo": titulo,
        "questao": questao,
        "candidatas": candidatas,
        "comparacao": comparacao,
        "ligadas": ligadas,
        "decidido": decidido,
        "decisao": decisao,
    }


def build():
    if not VAULT_CURADORIA.is_dir():
        sys.exit(f"ERRO: vault não encontrado em {VAULT_CURADORIA} (defina VAULT_CURADORIA).")
    decisoes, recon = [], {}
    for trilha, sub in SUBPASTAS.items():
        pasta = VAULT_CURADORIA / sub
        if not pasta.is_dir():
            sys.exit(f"ERRO: subpasta ausente: {pasta}")
        arquivos = sorted(pasta.glob("Decisão — *.md"))
        for p in arquivos:
            decisoes.append(parse_decisao(p.read_text(encoding="utf-8"), p.name, trilha))
        recon[trilha] = {"disco": len(arquivos), "parseadas": len(arquivos)}
        print(f"  ✓ {trilha}: {len(arquivos)} decisões")

    out = {
        "generated_by": "scripts/build_decisoes_curadoria.py",
        "reconciliacao": recon,
        "decisoes": decisoes,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Gerado: {OUT_JSON} ({len(decisoes)} decisões)")


if __name__ == "__main__":
    build()
