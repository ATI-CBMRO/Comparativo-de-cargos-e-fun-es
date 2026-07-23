"""
build_minuta_comparison_atual.py — Portal CBM (cenário LOB ATUAL, Lei nº 2.204/2009)

Gera database/atual/comparativo_minuta.json: os 21 órgãos do CBMRO vigente × demais
estados, SÓ com a camada 'automatico' (casamento por palavra-chave no organs_detail
compartilhado). Decisão de produto 2026-07-22: sem curadoria manual nesta fatia; a
tela rotula tudo como correspondência automática.

ISOLAMENTO (armadilha documentada no CLAUDE.md): este script NÃO importa
minuta_enrichment, lob_enrichment, build_minuta_structure nem build_minuta_comparison
— qualquer um deles traria conteúdo da LOB futura para o cenário atual.

Rodar: .venv-pipeline/bin/python scripts/build_minuta_comparison_atual.py
Valida: .venv-pipeline/bin/python scripts/test_minuta_comparison_atual.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from minuta_comparison_lib import norm, auto_match_organ_ids  # noqa: E402  (única importação permitida da lib)

BASE_DIR = Path(__file__).parent.parent
ATUAL_DIR = BASE_DIR / "database" / "atual"
DET_DIR = BASE_DIR / "database" / "organs_detail"          # acervo dos 27 (compartilhado)
RO_ATUAL_JSON = ATUAL_DIR / "organs_detail" / "ro.json"     # 21 órgãos vigentes
STRUCT_JSON = ATUAL_DIR / "minuta_structure.json"
STATES_JSON = BASE_DIR / "database" / "states_data.json"
OUT_JSON = ATUAL_DIR / "comparativo_minuta.json"

REF_ID = "ro"

# Palavras-chave POR ÓRGÃO DO ATUAL (chaves da Lei 2.204/2009 — a tabela da lib usa as
# chaves da futura e não serve aqui). include/exclude já normalizados (sem acento).
AUTO_MATCH_KEYWORDS_ATUAL = {
    "cg":           {"include": ["comando geral", "comando-geral"],
                     # "gabinete": mesmo AR-01 da lib — Gabinete do Comando-Geral não é
                     # o Comando-Geral (auditoria 2026-07-23).
                     "exclude": ["regional", "operacoes", "setorial", "secao", "gabinete"]},
    "emg":          {"include": ["estado maior", "estado-maior"], "exclude": ["regional"]},
    "corregedoria": {"include": ["corregedoria", "correicao"], "exclude": []},
    "ajudancia":    {"include": ["ajudancia", "ajudante-geral", "ajudante geral"], "exclude": []},
    "gabinete":     {"include": ["gabinete"],
                     "exclude": ["subcomando", "subcomandante", "chefia de gabinete"]},
    "cepdec":       {"include": ["defesa civil", "protecao e defesa"], "exclude": []},
    "condeg":       {"include": ["conselho"], "exclude": ["municipal", "regional", "ensino"]},
    "dint":         {"include": ["inteligencia"], "exclude": []},
    "cpof":         {"include": ["financas", "orcamento", "administracao financeira"],
                     "exclude": ["planejamento operacional"]},
    "assessorias":  {"include": ["assessoria"],
                     "exclude": ["assessoria de comunicacao", "comunicacao social",
                                 "inteligencia", "defesa civil",
                                 "informatica", "telecomunicacoes"]},
    "comissoes":    {"include": ["comissao"], "exclude": ["promocao"]},
    "dp":           {"include": ["diretoria de pessoal", "departamento de pessoal",
                                 "gestao de pessoal", "gestao de pessoas", "recursos humanos"],
                     "exclude": ["assistencia ao pessoal", "saude"]},
    "deei":         {"include": ["ensino", "instrucao", "academia"], "exclude": ["defesa civil"]},
    "cat":          {"include": ["atividades tecnicas", "atividade tecnica"],
                     "exclude": ["operacoes tecnicas", "comando de operacoes"]},
    "dlog":         {"include": ["logistica", "apoio logistico", "material e patrimonio",
                                 "materiais e servicos", "suprimento"], "exclude": []},
    "dcs":          {"include": ["comunicacao social"], "exclude": []},
    "dinf":         {"include": ["informatica", "tecnologia da informacao"], "exclude": []},
    "cob1":         {"include": ["comando operacional", "comando de operacoes",
                                 "coordenadoria operacional"],
                     # "operacoes tecnicas" exclui o COT (segurança contra incêndio),
                     # que NÃO é o COB operacional/socorro — armadilha AR-01.
                     # "defesa civil"/"inteligencia": Comandos de Operações de Defesa
                     # Civil e de Inteligência (GO) não são o COB (auditoria 2026-07-23).
                     "exclude": ["aerea", "aereo", "aviacao", "atividades tecnicas",
                                 "operacoes tecnicas", "operacao tecnica",
                                 "defesa civil", "inteligencia"]},
    "cob2":         {"include": ["regional", "regiao de bombeiro"], "exclude": []},
    "coa":          {"include": ["aerea", "aereo", "aviacao", "operacoes aereas"], "exclude": []},
    "gbs":          {"include": ["busca", "salvamento"], "exclude": []},
}


def match_ids(organ_key, organs):
    # Reusa o matcher ÚNICO da lib com a tabela do atual — antes era uma cópia da
    # função e correções não propagavam entre cenários (auditoria 2026-07-23).
    return auto_match_organ_ids(organ_key, organs, AUTO_MATCH_KEYWORDS_ATUAL)


def extract_organ(organs, oid):
    o = organs.get(oid)
    if not o:
        return None
    return {
        "name": o.get("name", ""), "abbreviation": o.get("abbreviation", ""),
        "subordinadoA": o.get("subordinadoA", ""),
        "atribuicoes": list(o.get("atribuicoes", [])),
        "desdobramentos": list(o.get("desdobramentos", [])),
        "cargos": [{
            "cargo": c.get("cargo", ""), "requisito": c.get("requisito", ""),
            "subordinadoA": c.get("subordinadoA", ""),
            "atribuicoes": list(c.get("atribuicoes", [])),
            "desdobramentos": list(c.get("desdobramentos", [])),
        } for c in o.get("cargos", [])],
    }


def load_state_meta():
    data = json.loads(STATES_JSON.read_text(encoding="utf-8"))
    return {s["id"]: {
        "id": s["id"], "name": s.get("name", s["id"]),
        "abbr": s.get("abbreviation", s["id"].upper()),
        "cbm": s.get("cbm_abbreviation", ""), "region": s.get("region", ""),
    } for s in data.get("states", [])}


def depth_map(chart):
    """{organKey: profundidade} a partir do commandChart do atual (dict raiz)."""
    out = {}
    def walk(node, d):
        out[node.get("organKey")] = d
        for ch in node.get("children", []) or []:
            walk(ch, d + 1)
    walk(chart, 0)
    return out


def build():
    struct = json.loads(STRUCT_JSON.read_text(encoding="utf-8"))
    ro_organs = json.loads(RO_ATUAL_JSON.read_text(encoding="utf-8")).get("organs", {})
    meta = load_state_meta()
    depths = depth_map(struct.get("commandChart") or {})

    organs_out = []
    for ch in struct["chapters"]:
        key = ch["id"].split(":")[-1]
        reference = extract_organ(ro_organs, key)
        states = []
        for sid in sorted(meta):
            if sid == REF_ID:
                continue
            p = DET_DIR / f"{sid}.json"
            if not p.exists():
                continue
            all_organs = json.loads(p.read_text(encoding="utf-8")).get("organs", {})
            lobbed = {oid: o for oid, o in all_organs.items() if o.get("source") == "lob"}
            non_lob = {oid: o for oid, o in all_organs.items() if o.get("source") != "lob"}
            lob_pool = lobbed if lobbed else all_organs  # regra da futura, copiada (não importada)
            ri = [extract_organ(non_lob, oid) for oid in match_ids(key, non_lob)]
            ri = [m for m in ri if m]
            lob = [extract_organ(lob_pool, oid) for oid in match_ids(key, lob_pool)]
            lob = [m for m in lob if m]
            if not ri and not lob:
                continue
            states.append({
                **meta[sid],
                "provenance": "automatico", "sourceLabel": None, "note": None,
                "organs": ri, "riOrgans": ri,
                "riProvenance": "automatico" if ri else None, "riSourceLabel": None,
                "lobOrgans": lob, "lobProvenance": "automatico" if lob else None,
            })
        states.sort(key=lambda s: s["name"])
        organs_out.append({
            "key": key,
            "title": ch.get("chapterTitle", key.upper()),
            "abbr": (reference or {}).get("abbreviation") or key.upper(),
            "depth": depths.get(key, 1),
            "reference": reference, "referenceNote": None,
            "states": states,
        })
        print(f"  ✓ {key:12s}: {len(states):2d} estados (automatico)")

    rmeta = meta.get(REF_ID, {"name": "Rondônia", "abbr": "RO", "cbm": "CBMRO"})
    out = {
        "generated_by": "scripts/build_minuta_comparison_atual.py",
        "scenario": "atual",
        "reference": {"id": REF_ID, "name": rmeta["name"], "abbr": rmeta["abbr"], "cbm": rmeta["cbm"]},
        "organs": organs_out,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Gerado: {OUT_JSON} ({len(organs_out)} órgãos)")


if __name__ == "__main__":
    build()
