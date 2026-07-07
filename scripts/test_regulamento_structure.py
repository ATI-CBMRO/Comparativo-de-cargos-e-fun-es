import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from regulamento_enrichment import THEME_KEYS, REGULAMENTO_DOCS

ROOT = Path(__file__).resolve().parent.parent
d = json.load(open(ROOT / 'database' / 'regulamento_structure.json', encoding='utf-8'))

assert d['title'].startswith('Minuta de Regulamento Geral')
assert len(d['chapters']) == len(THEME_KEYS)

edit_ids = set()
for c in d['chapters']:
    assert c['kind'] == 'articles'
    assert c['themeKey'] in THEME_KEYS
    assert c['primary']['uf'] in REGULAMENTO_DOCS
    for leaf in c['articles']:
        assert leaf['kind'] == 'incisos'
        assert leaf['editId'].startswith('reg:'), leaf['editId']
        assert leaf['editId'] not in edit_ids, f'editId duplicado: {leaf["editId"]}'
        edit_ids.add(leaf['editId'])
        assert leaf['source'].startswith('cf. CBM'), leaf['source']
        assert leaf['match'] in ('exata', 'parcial', 'tematica')
        assert not leaf['caput'].startswith('Art.'), f'caput com prefixo Art.: {leaf["caput"][:60]}'
        for it in leaf['items']:
            assert it['text'].strip() and it['source']
        if leaf.get('adapted'):
            assert 'original_caput' in leaf
    for uf, alt in c['alternatives'].items():
        assert uf in REGULAMENTO_DOCS and uf != c['primary']['uf']
        assert alt['excerpts'], f'alternativa vazia: {c["themeKey"]}/{uf}'
        for ex in alt['excerpts']:
            assert ex['source'].startswith('cf. CBM')

# Nenhum capítulo pode ficar sem conteúdo primário (cobertura confirmada no panorama).
vazios = [c['themeKey'] for c in d['chapters'] if not c['articles']]
assert not vazios, f'capítulos sem artigos: {vazios}'

print(f"OK — scripts/test_regulamento_structure.py ({len(d['chapters'])} capítulos, "
      f"{len(edit_ids)} artigos, schema compatível com buildArticles)")
