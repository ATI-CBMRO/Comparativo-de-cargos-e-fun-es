"""Gera database/atual/regulamento_structure.json — MINUTA do Regulamento do CBMRO
para o cenário LOB ATUAL (vigente).

Decisão de produto (validada 2026-07-15): o Regulamento é TEMÁTICO (regula serviço,
disciplina, uniformes, ensino etc.), e esses temas NÃO dependem da Lei Orgânica — logo
o cenário atual usa os MESMOS 15 temas e o mesmo material verbatim dos 9 estados já
curados para a futura. A diferença é o ISOLAMENTO: os editIds recebem o marcador de
cenário 'reg:atual:' (em vez de 'reg:'), para que comentários, textos finais e curadoria
do atual nunca se misturem com os da futura. A distinção LOB-específica vive no RI (que é
por órgão); o Regulamento (serviço) é matéria comum, mantida em baldes separados por
cenário.

Lê a estrutura temática já gerada da futura (database/regulamento_structure.json) e
re-carimba os ids — sem chamar o builder da futura (que reescreveria o arquivo dela) e
sem tocar em nada da futura.

Pré-requisito: rodar antes `python scripts/build_regulamento_structure.py` (gera a futura).

Saída: database/atual/regulamento_structure.json
"""
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
FUTURA_JSON = BASE_DIR / "database" / "regulamento_structure.json"
OUT_JSON = BASE_DIR / "database" / "atual" / "regulamento_structure.json"

FUTURA_PREFIX = "reg:"
ATUAL_PREFIX = "reg:atual:"


def _restamp_editids(obj):
    """Percorre recursivamente e troca o prefixo de cenário em qualquer campo 'editId'
    (reg:... -> reg:atual:...) — isola os endereços de dispositivo do Regulamento futuro."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "editId" and isinstance(v, str) and v.startswith(FUTURA_PREFIX) \
                    and not v.startswith(ATUAL_PREFIX):
                obj[k] = ATUAL_PREFIX + v[len(FUTURA_PREFIX):]
            else:
                _restamp_editids(v)
    elif isinstance(obj, list):
        for it in obj:
            _restamp_editids(it)
    return obj


def main():
    if not FUTURA_JSON.exists():
        raise SystemExit(
            "database/regulamento_structure.json não existe — rode antes "
            "`python scripts/build_regulamento_structure.py`."
        )
    # Aviso de frescor (auditoria 2026-07-23): herdamos o JSON gerado da futura —
    # se ele estiver mais velho que o enrichment mestre, o atual propaga conteúdo
    # defasado em silêncio. Sinaliza, não bloqueia.
    enr = FUTURA_JSON.parent.parent / "scripts" / "regulamento_enrichment.py"
    if enr.exists() and enr.stat().st_mtime > FUTURA_JSON.stat().st_mtime:
        print("  AVISO: database/regulamento_structure.json (futura) é mais velho que "
              "scripts/regulamento_enrichment.py — rode antes "
              "`python scripts/build_regulamento_structure.py`.")
    structure = json.loads(FUTURA_JSON.read_text(encoding="utf-8"))  # temática da futura
    _restamp_editids(structure)

    structure["generated_by"] = "scripts/build_regulamento_structure_atual.py"
    structure["cenario"] = "atual"
    structure["title"] = (
        "DO REGULAMENTO DO CORPO DE BOMBEIROS MILITAR DO ESTADO DE RONDÔNIA (CBMRO) — LOB ATUAL"
    )

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(structure, ensure_ascii=False, indent=2), encoding="utf-8")

    n_art = sum(len(c.get("articles", [])) for c in structure["chapters"])
    print(f"Gerado: {OUT_JSON}")
    print(f"  {len(structure['chapters'])} temas · {n_art} artigos (isolados como reg:atual:)")


if __name__ == "__main__":
    main()
