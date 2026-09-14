"""Valida as DUAS versões do Regulamento do cenário atual geradas por
build_regulamento_structure_atual.py com a curadoria da consulta
(scripts/regulamento_curadoria_consulta.py)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from regulamento_curadoria_consulta import (  # noqa: E402
    CORRECOES, SUPRIMIR, SUBSTITUIR, INCLUIR, TEXTOS_FINAIS_ATUAL,
)

ROOT = Path(__file__).resolve().parent.parent
consulta = json.load(open(ROOT / 'database' / 'atual' / 'regulamento_structure_consulta.json', encoding='utf-8'))
atual = json.load(open(ROOT / 'database' / 'atual' / 'regulamento_structure.json', encoding='utf-8'))

assert consulta['versao'] == 'consulta' and atual['versao'] == 'atual'
assert [c['id'] for c in consulta['chapters']] == [c['id'] for c in atual['chapters']]


def por_tema(s):
    return {c['id'].split(':')[-1]: c for c in s['chapters']}


C, A = por_tema(consulta), por_tema(atual)

# 1. A versão em consulta tem EXATAMENTE os ids que os militares leram (nenhum novo, nenhum
#    a menos) — só o texto corrigido. Sem isso os comentários (editId#index) ficariam órfãos.
for tema, cap in C.items():
    for a in cap['articles']:
        assert not a.get('substitui') and not a.get('incluido') and not a.get('alterado'), \
            f'versão em consulta com alteração indevida: {tema}/{a["id"]}'
        assert '-r' not in a['id'].split('art-')[-1] and '-c' not in a['id'].split('art-')[-1], a['id']

# 2. Correções aplicadas nas DUAS versões, e marcadas.
for tema, arts in CORRECOES.items():
    for aid, regras in arts.items():
        for s, rotulo in ((C, 'consulta'), (A, 'atual')):
            art = next((x for x in s[tema]['articles'] if x['id'] == aid), None)
            if art is None:  # na atual o artigo pode ter sido substituído/suprimido
                assert rotulo == 'atual', f'{tema}/{aid} sumiu da versão em consulta'
                continue
            assert art.get('corrigido'), f'{rotulo}: {tema}/{aid} sem marca corrigido'
            for velho, novo in regras.get('caput', []):
                assert velho not in art['caput'] or velho in novo, f'{rotulo}: {tema}/{aid} ainda tem {velho!r}'
                assert novo in art['caput'], f'{rotulo}: {tema}/{aid} não tem {novo!r}'
assert 'Art. 148 da Constituição Estadual' in next(a for a in C['disposicoes-preliminares']['articles'] if a['id'] == 'mt-art-1')['caput']
assert 'Art. 148 da Constituição Estadual' in next(a for a in A['disposicoes-preliminares']['articles'] if a['id'] == 'mt-art-1')['caput']

# 3. Supressões: saem da atual, ficam na consulta, registradas no capítulo.
for tema, ids in SUPRIMIR.items():
    ids_atual = {a['id'] for a in A[tema]['articles']}
    ids_cons = {a['id'] for a in C[tema]['articles']}
    for aid in ids:
        assert aid not in ids_atual, f'{tema}/{aid} deveria ter sido suprimido da atual'
        assert aid in ids_cons, f'{tema}/{aid} sumiu da versão em consulta'
    assert {s['id'] for s in A[tema].get('suprimidos', [])} == set(ids)

# 4. Substituições: o antigo sai, o novo entra NO MESMO LUGAR com `substitui`.
for tema, subs in SUBSTITUIR.items():
    ids_atual = [a['id'] for a in A[tema]['articles']]
    ids_cons = [a['id'] for a in C[tema]['articles']]
    for aid, specs in subs.items():
        assert aid not in ids_atual, f'{tema}/{aid} deveria ter sido substituído'
        novos = [a for a in A[tema]['articles'] if a.get('substitui') == aid]
        assert len(novos) == len(specs), f'{tema}/{aid}: {len(novos)} novos, esperava {len(specs)}'
        pos_cons = ids_cons.index(aid)
        anterior = ids_cons[pos_cons - 1] if pos_cons else None
        if anterior and anterior in ids_atual:
            assert ids_atual.index(novos[0]['id']) == ids_atual.index(anterior) + 1, \
                f'{tema}/{aid}: substituto fora de posição'
        for n in novos:
            assert n['autoral'] and n['fundamento'] and 'Lei nº 2.204/2009' in n['fundamento'], n['id']
            assert n['editId'].startswith(f'reg:atual:{tema}/'), n['editId']
            assert n['items'] and all(it['text'].strip() for it in n['items']), n['id']

# 5. Inclusões: entram só na atual, logo após o âncora (ou após o último substituto dele).
for tema, blocos in INCLUIR.items():
    ids_atual = [a['id'] for a in A[tema]['articles']]
    for b in blocos:
        novos = [a for a in A[tema]['articles'] if a['id'].startswith(f'{b["apos"]}-c')]
        assert len(novos) == len(b['artigos']), f'{tema}/{b["apos"]}: {len(novos)} incluídos'
        assert all(n.get('incluido') for n in novos)
        assert not any(a['id'].startswith(f'{b["apos"]}-c') for a in C[tema]['articles'])
        # ancora suprimida (se-art-38) não está na atual; os novos precisam existir mesmo assim
        if b['apos'] in ids_atual:
            assert ids_atual.index(novos[0]['id']) == ids_atual.index(b['apos']) + 1

# 6. Propostas de mérito marcadas.
propostas = [a for c in atual['chapters'] for a in c['articles'] if a.get('proposta')]
assert len(propostas) == 3, f'esperava 3 propostas pendentes de deliberação, achei {len(propostas)}'
assert all('PROPOSTA PENDENTE' in a['nota'] for a in propostas)

# 7. Textos finais só na atual.
for tema, arts in TEXTOS_FINAIS_ATUAL.items():
    for aid, f in arts.items():
        art_a = next(a for a in A[tema]['articles'] if a['id'] == aid)
        art_c = next(a for a in C[tema]['articles'] if a['id'] == aid)
        assert art_a.get('alterado') == 'texto final'
        if 'caput' in f:
            assert art_a['caput'] == f['caput'] and art_c['caput'] != f['caput'], f'{tema}/{aid}'

# 8. editIds únicos nas duas; recorte de serviço da atual: capítulo misto todo com orgao.
for s in (consulta, atual):
    vistos = set()
    for c in s['chapters']:
        for a in c['articles']:
            assert a['editId'] not in vistos, f'editId duplicado: {a["editId"]}'
            vistos.add(a['editId'])
for a in A['atribuicoes-funcoes']['articles']:
    if a.get('substitui') or a.get('incluido'):
        assert a.get('orgao') in ('cob', 'cat'), f'novo artigo sem orgao: {a["id"]}'

n_c = sum(len(c['articles']) for c in consulta['chapters'])
n_a = sum(len(c['articles']) for c in atual['chapters'])
print(f'OK — scripts/test_regulamento_curadoria_consulta.py (consulta {n_c} artigos, atual {n_a} artigos, '
      f'{len(propostas)} propostas pendentes, curadoria={atual["curadoria"]})')
