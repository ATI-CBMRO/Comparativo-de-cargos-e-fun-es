import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from regulamento_enrichment import THEME_KEYS, REGULAMENTO_DOCS

ROOT = Path(__file__).resolve().parent.parent
d = json.load(open(ROOT / 'database' / 'regulamento_structure.json', encoding='utf-8'))

assert d['title'].startswith('Minuta de Regulamento Geral')
assert len(d['chapters']) == len(THEME_KEYS)

# 2 Partes (spec 2026-07-21): todo capítulo tem parte válida e a ordem é Parte I → Parte II.
for c in d['chapters']:
    assert c.get('parte') in ('geral', 'servico'), f"capítulo sem parte: {c['themeKey']}"
ordem = [c['parte'] for c in d['chapters']]
assert ordem == sorted(ordem, key=lambda p: {'geral': 0, 'servico': 1}[p]), \
    f'capítulo geral depois de servico: {ordem}'
assert 'central-operacoes-193' in [c['themeKey'] for c in d['chapters']]

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
        if leaf.get('autoral'):
            # Redação própria (scripts/regulamento_reescrita.py): não é transcrição de
            # outro estado, então NÃO passa por verificar_verbatim.py — em troca é
            # obrigada a declarar o fundamento na lei de Rondônia que a sustenta.
            assert leaf.get('fundamento'), f'artigo autoral sem fundamento: {leaf["editId"]}'
            assert leaf['source'] == leaf['fundamento']
            assert ('Lei nº 2.204/2009' in leaf['fundamento']
                    or 'LOB' in leaf['fundamento']
                    or 'Decreto nº 21.425/2016' in leaf['fundamento']
                    or 'Lei estadual nº 3.924/2016' in leaf['fundamento']
                    or 'organograma oficial' in leaf['fundamento']
                    or 'NGA-CIOP-001/2026' in leaf['fundamento']), \
                f'fundamento não cita norma de RO: {leaf["fundamento"]}'
        else:
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
            assert ex['source'].startswith('cf. CBM') or ex['source'].startswith('cf. Exército Brasileiro'), \
                ex['source']

# Nenhum capítulo sem conteúdo primário — exceto os explicitamente pendentes (Fase 2).
PENDENTES_OK = set()  # Fase 2A preencheu central-operacoes-193; nenhum tema pode ficar vazio
vazios = [c['themeKey'] for c in d['chapters']
          if not c['articles'] and c['themeKey'] not in PENDENTES_OK]
assert not vazios, f'capítulos sem artigos: {vazios}'

_co = next(c for c in d['chapters'] if c['themeKey'] == 'central-operacoes-193')
assert _co['articles'], 'central-operacoes-193 sem artigos (Fase 2A deveria ter preenchido)'
assert _co['parte'] == 'servico', _co['parte']
assert _co['primary']['uf'] == 'ba', _co['primary']['uf']
assert 'to' in _co['alternatives'], 'faltou a alternativa TO em central-operacoes-193'

# O piso existe para pegar PERDA ACIDENTAL de artigo (regressão do extrator ou do
# enrichment). Em 2026-08-13/14 ele baixou de 413 para 416 (passando por 396 e 415) por
# decisão de curadoria, não por regressão — a aritmética, conferida artigo a artigo:
#     413 importados
#     -13 artigos removidos (órgão do MT inexistente em RO — REMOVER_ARTIGOS)
#     -19 artigos do capítulo de segurança contra incêndio (era o regimento da DSCIP/MT)
#     +15 artigos de redação própria da CAT/DAT/SAT (ARTIGOS_PROPRIOS)
#     = 396
#     -2 artigos de organizacao-geral (mt-art-4 e mt-art-5 — organograma do CBMMT)
#     +21 artigos de redação própria do organograma do CBMRO (ARTIGOS_PROPRIOS)
#     = 415
#     -3 artigos de central-operacoes-193 (ba-art-8/9/18 — CICOM da Bahia)
#     +4 artigos de redação própria (Supervisores/Atendentes/Despachadores da NGA-CIOP +
#        remissão), fundados na NGA-CIOP-001/2026
#     = 416
# Ver scripts/regulamento_reescrita.py para o motivo de cada remoção.
assert len(edit_ids) >= 416, f'regressão: {len(edit_ids)} artigos (esperado >= 416)'
autorais = [l for c in d['chapters'] for l in c['articles'] if l.get('autoral')]
assert len(autorais) == 40, \
    f'artigos autorais: {len(autorais)} (esperado 15 SCI + 21 org.-geral + 4 CIOP = 40)'
for tema in ('seguranca-contra-incendio', 'organizacao-geral', 'central-operacoes-193'):
    cap = [c for c in d['chapters'] if c['themeKey'] == tema][0]
    assert all(l.get('autoral') for l in cap['articles']), \
        f'capítulo {tema} deve ser 100% redação própria'
    assert cap['alternatives'], f'Bloco D do capítulo {tema} foi perdido'

for c in d['chapters']:
    assert c['primary']['uf'] != 'risg', f"RISG não pode ser fonte primária: {c['themeKey']}"

print(f"OK — scripts/test_regulamento_structure.py ({len(d['chapters'])} capítulos, "
      f"{len(edit_ids)} artigos, schema compatível com buildArticles)")
