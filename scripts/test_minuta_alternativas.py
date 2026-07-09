"""Teste de schema do campo `alternatives` em minuta_structure.json (Bloco D —
comparador do Regimento Interno). Sem pytest: assert, rodar com python.

Valida a MESMA forma que scripts/ri_alternativas_enrichment.py gera e que
scripts/build_minuta_structure.py anexa a cada capítulo kind='organ':
  alternatives: {uf: {name, abbr, docLabel, excerpts: [{heading, caput,
  dispositivos, source, match}, ...]}, ...}
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ri_alternativas_enrichment import RI_ALTERNATIVES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
d = json.load(open(ROOT / 'database' / 'minuta_structure.json', encoding='utf-8'))

MATCH_VALUES = ('exata', 'parcial', 'tematica')

organ_chapters = [c for c in d['chapters'] if c.get('kind') == 'organ']
assert organ_chapters, 'nenhum capítulo kind=organ encontrado'

n_organs_com_alt = 0
n_excerpts_total = 0

for c in organ_chapters:
    organ_key = c['organKey']
    alt = c.get('alternatives')
    assert isinstance(alt, dict), f'{organ_key}: alternatives não é dict ({type(alt)})'

    if not alt:
        continue
    n_organs_com_alt += 1

    for uf, entry in alt.items():
        assert isinstance(uf, str) and uf, f'{organ_key}: chave de estado inválida {uf!r}'
        for campo in ('name', 'abbr', 'docLabel', 'excerpts'):
            assert campo in entry, f'{organ_key}/{uf}: falta campo {campo!r}'
        assert entry['name'].strip(), f'{organ_key}/{uf}: name vazio'
        assert entry['abbr'].strip(), f'{organ_key}/{uf}: abbr vazio'
        assert entry['abbr'] == entry['abbr'].upper(), f'{organ_key}/{uf}: abbr não está em maiúsculas ({entry["abbr"]!r})'
        assert entry['docLabel'].strip(), f'{organ_key}/{uf}: docLabel vazio'
        assert entry['excerpts'], f'{organ_key}/{uf}: excerpts vazio'

        for ex in entry['excerpts']:
            for campo in ('heading', 'caput', 'dispositivos', 'source', 'match'):
                assert campo in ex, f'{organ_key}/{uf}: excerpt sem campo {campo!r}: {ex}'
            assert ex['caput'].strip(), f'{organ_key}/{uf}: caput vazio — {ex["source"]}'
            assert isinstance(ex['dispositivos'], list), f'{organ_key}/{uf}: dispositivos não é lista'
            assert ex['source'].startswith('cf. CBM'), f'{organ_key}/{uf}: source sem prefixo "cf. CBM" ({ex["source"]!r})'
            assert ex['match'] in MATCH_VALUES, f'{organ_key}/{uf}: match inválido {ex["match"]!r}'
            n_excerpts_total += 1

# O gerador (RI_ALTERNATIVES) e o campo anexado devem contar a mesma coisa —
# garante que build_minuta_structure.py não perdeu nem inventou nenhum órgão.
organs_no_gerador = set(RI_ALTERNATIVES)
organs_no_json = {c['organKey'] for c in organ_chapters if c.get('alternatives')}
assert organs_no_gerador == organs_no_json, (
    f'divergência gerador x JSON: só no gerador={organs_no_gerador - organs_no_json}, '
    f'só no JSON={organs_no_json - organs_no_gerador}'
)

# Órgãos-âncora citados no pedido: devem ter alternatives não-vazio.
for organ_key in ('dp', 'crbm', 'cg'):
    chapter = next(c for c in organ_chapters if c['organKey'] == organ_key)
    assert chapter.get('alternatives'), f'{organ_key}: alternatives vazio (esperado não-vazio)'

print(
    f"OK — scripts/test_minuta_alternativas.py "
    f"({n_organs_com_alt} órgãos com alternatives, {n_excerpts_total} excertos, "
    f"schema compatível com o comparador do RI)"
)
