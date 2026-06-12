"""
build_dpo_cot_comparison.py — Portal CBM

Gera database/comparativo_dpo_cot.json: tabela comparativa, lado a lado, dos
órgãos equivalentes à DPO (Diretoria de Planejamento Operacional) e ao COT
(Comando de Operações Técnicas) da minuta de LOB do CBMRO, em todos os 27 CBMs.

O CASAMENTO é por FUNÇÃO, não por nome (a nomenclatura varia entre os estados):
  - DPO  ≈ órgão de planejamento/direção/comando das atividades OPERACIONAIS
  - COT  ≈ órgão de ATIVIDADES TÉCNICAS / segurança contra incêndio e pânico

O mapeamento abaixo (id de órgão por estado) foi curado manualmente a partir da
leitura das legislações. Os TEXTOS são extraídos VERBATIM de
database/organs_detail/<id>.json — nada é inventado aqui. Onde a lei não
discrimina o órgão, a lista fica vazia e um "note" explica.

Rodar: python scripts/build_dpo_cot_comparison.py
"""

import json
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).parent.parent
DET_DIR = BASE_DIR / "database" / "organs_detail"
STATES_JSON = BASE_DIR / "database" / "states_data.json"
OUT_JSON = BASE_DIR / "database" / "comparativo_dpo_cot.json"

REF_ID = "ro"

# ── Mapeamento curado: órgão(s) equivalente(s) por estado ──
# DPO-equivalente: planejamento / comando operacional
DPO_MAP = {
    "ro": ["dpo"],
    "ac": ["cob-ac", "cob-interior-ac"],
    "al": ["cob-al"],
    "am": ["cobom-am", "cbc-am", "cbi-am"],
    "ap": ["comando-operacional-ap"],
    "ba": ["cobm"],
    "ce": ["coordenadoria-operacional-ce"],
    "df": ["comando-operacional-df"],
    "es": ["diretoria-operacoes-es"],
    "go": ["cob"],
    "ma": ["cmd-op-ma"],
    "mg": ["comandos-operacionais-mg"],
    "ms": ["cmb-ms"],
    "mt": ["diretoria-operacional-mt"],
    "pa": ["comando_operacoes"],
    "pb": ["crbm-pb"],
    "pe": ["com-pe", "coesp-pe", "cointer1-pe", "cointer2-pe"],
    "pi": ["cob-pi"],
    "pr": ["estado_maior"],
    "rj": ["cba", "cocb-rj"],
    "rn": ["cmdoop-rn"],
    "rr": ["cmd-op-rr"],
    "rs": ["aodc"],
    "sc": ["1rbm"],
    "se": ["dop-se"],
    "sp": ["estado-maior-cb"],
    "to": ["cobm-to"],
}

# COT-equivalente: atividades técnicas / segurança contra incêndio e pânico
COT_MAP = {
    "ro": ["cot"],
    "ac": ["datop-ac"],
    "al": ["dst-al"],
    "am": ["dst-am"],
    "ap": ["at-ap"],
    "ba": ["csci-ba"],
    "ce": ["coordenadoria-atividades-tecnicas-ce"],
    "df": [],
    "es": ["centro-atividades-tecnicas-es"],
    "go": ["cat"],
    "ma": ["dat-ma"],
    "mg": ["cat-mg"],
    "ms": ["diretoria-atividades-tecnicas-ms"],
    "mt": ["diretoria-seguranca-mt"],
    "pa": ["departamento_seguranca_incendio"],
    "pb": ["dat-pb"],
    "pe": ["cat-pe"],
    "pi": ["dsci-pi"],
    "pr": ["diretoria_atividades_tecnicas"],
    "rj": ["dst-rj"],
    "rn": ["dat-rn"],
    "rr": ["dpst-rr"],
    "rs": ["dspci"],
    "sc": ["dsci-sc"],
    "se": ["dat-se"],
    "sp": ["secao-servico-tecnico"],
    "to": ["cat-to"],
}

# Observações curadas sobre correspondências imperfeitas (verbatim/explicativas)
NOTES = {
    "ap": {
        "cot": "A LC nº 180/2026 remete a estrutura detalhada a decreto; "
               "não há órgão de atividades técnicas próprio — consta apenas a "
               "Assessoria Técnica (assessoramento genérico, Art. 6º §2º).",
    },
    "df": {
        "cot": "A Lei nº 8.255/1991 (e alterações) estrutura a Corporação por "
               "Departamentos; o detalhamento curado não discrimina órgão "
               "específico de atividades técnicas / segurança contra incêndio.",
    },
    "pr": {
        "dpo": "Não há diretoria operacional autônoma: o planejamento operacional "
               "reside na 3ª Seção (BM/3) do Estado-Maior; a execução fica nos "
               "Comandos Regionais (CRBM) e Batalhões (BBM).",
    },
    "sp": {
        "dpo": "Não há diretoria operacional autônoma (Lei nº 616/1974): o "
               "planejamento operacional reside na 3ª Seção (B/3) do Estado-Maior; "
               "a execução fica nos Grupamentos.",
    },
    "pe": {
        "cot": "Único caso, além do RO, em que o órgão técnico (CAT) é subordinado "
               "ao comando operacional (COEsp) — estrutura análoga a DPO→COT.",
    },
    "sc": {
        "dpo": "Direção operacional regionalizada: 1ª, 2ª e 3ª RBM têm atribuições "
               "idênticas (Art. 39 I–IX); apresenta-se a 1ª RBM como representativa.",
    },
}

# Cache para nomes/regiões dos estados
def load_state_meta():
    data = json.loads(STATES_JSON.read_text(encoding="utf-8"))
    meta = {}
    for s in data.get("states", []):
        meta[s["id"]] = {
            "name": s.get("name", s["id"]),
            "abbreviation": s.get("abbreviation", s["id"].upper()),
            "cbm": s.get("cbm_abbreviation", ""),
            "region": s.get("region", ""),
        }
    return meta


def extract_organ(detail_organs, oid):
    """Extrai os campos verbatim de um órgão do JSON de detalhamento."""
    o = detail_organs.get(oid)
    if not o:
        return None
    cargos = []
    for c in o.get("cargos", []):
        cargos.append({
            "cargo": c.get("cargo", ""),
            "requisito": c.get("requisito", ""),
            "subordinadoA": c.get("subordinadoA", ""),
            "atribuicoes": list(c.get("atribuicoes", [])),
            "desdobramentos": list(c.get("desdobramentos", [])),
        })
    return {
        "id": oid,
        "name": o.get("name", ""),
        "abbreviation": o.get("abbreviation", ""),
        "category": o.get("category", ""),
        "legalRef": o.get("legalRef", ""),
        "baseLegal": o.get("baseLegal", ""),
        "subordinadoA": o.get("subordinadoA", ""),
        "atribuicoes": list(o.get("atribuicoes", [])),
        "desdobramentos": list(o.get("desdobramentos", [])),
        "cargos": cargos,
    }


def build():
    meta = load_state_meta()
    states_out = []
    ids = list(DPO_MAP.keys())
    # RO primeiro, depois alfabético pelos demais
    ids = [REF_ID] + sorted(i for i in ids if i != REF_ID)

    for sid in ids:
        det_path = DET_DIR / f"{sid}.json"
        if not det_path.exists():
            print(f"  ! {sid}: organs_detail ausente — pulando")
            continue
        organs = json.loads(det_path.read_text(encoding="utf-8")).get("organs", {})

        dpo = [extract_organ(organs, oid) for oid in DPO_MAP.get(sid, [])]
        cot = [extract_organ(organs, oid) for oid in COT_MAP.get(sid, [])]
        dpo = [x for x in dpo if x]
        cot = [x for x in cot if x]

        m = meta.get(sid, {"name": sid, "abbreviation": sid.upper(), "cbm": "", "region": ""})
        states_out.append({
            "id": sid,
            "name": m["name"],
            "abbreviation": m["abbreviation"],
            "cbm": m["cbm"],
            "region": m["region"],
            "is_reference": sid == REF_ID,
            "dpo": dpo,
            "cot": cot,
            "notes": NOTES.get(sid, {}),
        })
        print(f"  ✓ {sid}: DPO={len(dpo)} órgão(s) · COT={len(cot)} órgão(s)")

    out = {
        "generated_by": "scripts/build_dpo_cot_comparison.py",
        "reference": REF_ID,
        "groups": [
            {
                "key": "dpo",
                "title": "Planejamento / Comando Operacional",
                "ref_abbr": "DPO",
                "ref_name": "Diretoria de Planejamento Operacional",
                "description": "Órgão responsável pelo planejamento, direção, "
                               "coordenação, supervisão, fiscalização e avaliação "
                               "das atividades operacionais da Corporação.",
            },
            {
                "key": "cot",
                "title": "Atividades Técnicas / Segurança Contra Incêndio e Pânico",
                "ref_abbr": "COT",
                "ref_name": "Comando de Operações Técnicas",
                "description": "Órgão responsável pelo controle e observância dos "
                               "requisitos técnicos contra incêndio e pânico — "
                               "análise de projetos, vistorias, fiscalização, "
                               "normatização e perícia.",
            },
        ],
        "states": states_out,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n→ {OUT_JSON.relative_to(BASE_DIR)} ({len(states_out)} estados)")


if __name__ == "__main__":
    print("=" * 60)
    print("Gerando comparativo DPO × COT (27 CBMs)")
    print("=" * 60)
    build()
