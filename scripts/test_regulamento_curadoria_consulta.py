"""Valida as DUAS versões do Regulamento do cenário atual geradas por
build_regulamento_structure_atual.py com a curadoria da consulta
(scripts/regulamento_curadoria_consulta.py)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from regulamento_curadoria_consulta import (  # noqa: E402
    CORRECOES, CORRECOES_GLOBAIS, SUPRIMIR, SUPRIMIR_AMBAS, SUBSTITUIR, INCLUIR, TEXTOS_FINAIS_ATUAL,
)


def _com_globais(texto):
    """As CORRECOES específicas casam com o texto JÁ passado pelas CORRECOES_GLOBAIS."""
    for velho, novo in CORRECOES_GLOBAIS:
        texto = texto.replace(velho, novo)
    return texto

ROOT = Path(__file__).resolve().parent.parent
consulta = json.load(open(ROOT / 'database' / 'atual' / 'regulamento_structure_consulta.json', encoding='utf-8'))
atual = json.load(open(ROOT / 'database' / 'atual' / 'regulamento_structure.json', encoding='utf-8'))

assert consulta['versao'] == 'consulta' and atual['versao'] == 'atual'
assert [c['id'] for c in consulta['chapters']] == [c['id'] for c in atual['chapters']]


def por_tema(s):
    return {c['id'].split(':')[-1]: c for c in s['chapters']}


C, A = por_tema(consulta), por_tema(atual)

# 1. A versão em consulta é EXATAMENTE o que os militares leram: mesmos ids, texto intocado
#    (nem correção). Sem isso os comentários (editId#index) ficariam órfãos ou enganosos.
for tema, cap in C.items():
    for a in cap['articles']:
        assert not a.get('substitui') and not a.get('incluido') and not a.get('alterado') and not a.get('corrigido'), \
            f'versão em consulta com alteração indevida: {tema}/{a["id"]}'
        assert '-r' not in a['id'].split('art-')[-1] and '-c' not in a['id'].split('art-')[-1], a['id']

# 2. Correções aplicadas SÓ na atual, e marcadas; a consulta mantém o texto antigo.
for tema, arts in CORRECOES.items():
    for aid, regras in arts.items():
        art_c = next((x for x in C[tema]['articles'] if x['id'] == aid), None)
        if art_c is None:  # suprimido nas duas versões (16/09): a correção só vale antes da supressão
            assert aid in SUPRIMIR_AMBAS.get(tema, {}) or aid in SUPRIMIR.get(tema, {}), f'consulta: {tema}/{aid} sumiu sem estar em SUPRIMIR/SUPRIMIR_AMBAS'
            continue
        art = next((x for x in A[tema]['articles'] if x['id'] == aid), None)
        for velho, novo in regras.get('caput', []):
            assert velho in _com_globais(art_c['caput']), f'consulta: {tema}/{aid} deveria manter {velho!r}'
        if art is None:  # na atual o artigo pode ter sido substituído/suprimido
            continue
        assert art.get('corrigido'), f'atual: {tema}/{aid} sem marca corrigido'
        for velho, novo in regras.get('caput', []):
            assert velho not in art['caput'] or velho in novo, f'atual: {tema}/{aid} ainda tem {velho!r}'
            assert novo in art['caput'], f'atual: {tema}/{aid} não tem {novo!r}'
assert 'Art. 82 da Constituição Estadual' in next(a for a in C['disposicoes-preliminares']['articles'] if a['id'] == 'mt-art-1')['caput']
assert 'Art. 148 da Constituição Estadual' in next(a for a in A['disposicoes-preliminares']['articles'] if a['id'] == 'mt-art-1')['caput']

# 3. Supressões: saem das DUAS versões (determinação de 16/09), registradas no capítulo de ambas.
for tema, ids in SUPRIMIR.items():
    ids_atual = {a['id'] for a in A[tema]['articles']}
    ids_cons = {a['id'] for a in C[tema]['articles']}
    for aid in ids:
        assert aid not in ids_atual, f'{tema}/{aid} deveria ter sido suprimido da atual'
        assert aid not in ids_cons, f'{tema}/{aid} deveria ter sido suprimido também da versão em consulta'
    regs_a = {s['id'] for s in A[tema].get('suprimidos', [])}
    regs_c = {s['id'] for s in C[tema].get('suprimidos', [])}
    assert set(ids) <= regs_a and set(ids) <= regs_c and regs_a == regs_c, f'{tema}: registros de supressão divergem entre as versões'
    assert all(s.get('ambas') for s in A[tema].get('suprimidos', []) + C[tema].get('suprimidos', []))
# nenhum texto suprimido sobrevive em qualquer das versões
for _tema, _ids in SUPRIMIR.items():
    for _id in _ids:
        assert _id not in {a['id'] for a in C[_tema]['articles']}

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
assert len(propostas) == 0, f'não deveria restar proposta pendente de deliberação, achei {len(propostas)}'
assert all('PROPOSTA PENDENTE' in a['nota'] for a in propostas)

# 7. Textos finais e redações ajustadas só na atual; inciso suprimido vira texto vazio no
#    MESMO índice (os demais não se movem — AR-03) e fica registrado.
for tema, arts in TEXTOS_FINAIS_ATUAL.items():
    for aid, f in arts.items():
        art_a = next(a for a in A[tema]['articles'] if a['id'] == aid)
        art_c = next(a for a in C[tema]['articles'] if a['id'] == aid)
        assert art_a.get('alterado') == f.get('alterado', 'texto final'), f'{tema}/{aid}'
        if 'caput' in f:
            assert art_a['caput'] == f['caput'] and art_c['caput'] != f['caput'], f'{tema}/{aid}'
        for idx, texto in f.get('items', {}).items():
            if texto is None:   # inciso suprimido: vazio nas DUAS versões (revisão de 16/09), mesmo índice
                assert art_a['items'][idx]['text'] == '' and idx in art_a['incisos_suprimidos'], f'{tema}/{aid}#{idx}'
                assert art_c['items'][idx]['text'] == '' and idx in art_c['incisos_suprimidos'], f'{tema}/{aid}#{idx} deveria estar vazio também na consulta'
                continue
            assert art_c['items'][idx]['text'].strip(), f'{tema}/{aid}#{idx} vazio na consulta'
            if False:
                pass
            else:
                assert art_a['items'][idx]['text'] == texto, f'{tema}/{aid}#{idx}'
        assert len(art_a['items']) == len(art_c['items']) + len(f.get('acrescentar', [])), f'{tema}/{aid}: incisos re-indexados'
        for k, texto in enumerate(f.get('acrescentar', [])):
            assert art_a['items'][len(art_c['items']) + k]['text'] == texto

# 7b. Ajustes de redação e correções da curadoria de set/2026 (só na atual).
_se_c = {a['id']: a for a in C['servico-operacional']['articles']}
_se_a = {a['id']: a for a in A['servico-operacional']['articles']}
assert 'Grupamento de Operações Aéreas – GOA' in _se_a['se-art-135']['items'][10]['text']
assert 'GTA' in _se_c['se-art-135']['items'][10]['text'], 'a consulta mantém o texto lido'
assert 'atividades de defesa civil do Estado' in next(a for a in C['disposicoes-preliminares']['articles'] if a['id'] == 'mt-art-3')['items'][2]['text']
assert _se_a['ro-art-2-c1']['caput'].startswith('Os casos omissos serão resolvidos'), 'casos omissos movidos (se-art-43 fora das duas versões)'
assert A['servico-operacional']['articles'][-1]['id'] == 'ro-art-2-c1', 'casos omissos fecham o capítulo'
assert 'ciência ao Superior de Dia' in _se_a['se-art-132']['caput']
# deliberação 15/09 (grupo 3 do quadro de semelhantes): inciso VI sem o parágrafo grudado
assert _se_a['se-art-114']['items'][5]['text'].endswith('pelo Oficial de Dia/Comandante de Guarnição.') and 'omissos' not in _se_a['se-art-114']['items'][5]['text']
assert 'Parágrafo Único' in _se_c['se-art-114']['items'][5]['text'], 'a consulta mantém o texto lido'
# se-art-116 (pacientes com transtorno mental, incl. o parágrafo dos casos omissos) foi suprimido nas duas versões em 16/09
assert atual['curadoria']['deliberacoes'][0]['dispositivos'][0] == 'servico-operacional/se-art-114#5'
# resíduos de outros CBMs (15/09): nada de Sergipe/MT nos temas do recorte de serviço da atual
# (a Parte I do Regulamento Geral completo ainda é transplante de MT — pendência própria)
_TEMAS_RECORTE = {'disposicoes-preliminares', 'atribuicoes-funcoes', 'servico-operacional', 'central-operacoes-193',
                  'servico-interno-dia', 'seguranca-contra-incendio', 'disposicoes-finais'}
for c in atual['chapters']:
    if c['id'].split(':')[-1] not in _TEMAS_RECORTE:
        continue
    for a in c['articles']:
        texto = ' '.join([a.get('caput', '')] + [it['text'] for it in a.get('items', [])])
        for termo in ('CIOSP', 'SES/SSP', 'UM de Saúde', 'Comandante do SOS', 'Chefe da Prontidão', 'Central Integrada',
                      'Boletim Geral Ostensivo', 'Comandante do Socorro', 'Comandante de Operações', 'Unidade Operacional',
                      'deste regimento', 'Regulamento Geral', 'Diretoria de Pessoal, Ensino', 'Comandante de Socorro', 'Comandante de socorro',
                      'Cmt de Socorro', 'Adjunto ao Oficial', 'adjunto do oficial', 'Auxiliares do Comandante', 'auxiliares da guarnição',
                      'Guarda de Quartel', 'Auxiliar da Guarda', 'Comandante de Área', 'Reserva Técnica', 'Chefe da Prontidão'):
            assert termo not in texto, f'{c["id"]}/{a["id"]}: resíduo "{termo}"'
assert not any(a['id'] in ('se-art-95', 'se-art-99') for a in A['servico-interno-dia']['articles'])
assert _se_a['se-art-4']['items'][1]['text'] == '' and 1 in _se_a['se-art-4']['incisos_suprimidos']
assert _se_a['se-art-4']['items'][-1]['text'].startswith('Parágrafo único. O serviço de Oficial de Dia existe apenas no 1º Grupamento')
assert 'QCG' not in ' '.join(it['text'] for it in _se_a['se-art-38-c2']['items']) and '1º Grupamento' in _se_a['se-art-38-c1']['caput']
# 15/09: Parte I comum aos dois serviços — finalidade e objetivos generalizados; política do serviço técnico nova
assert 'o serviço operacional e o serviço técnico' in _se_a['se-art-1']['caput'] and _se_a['se-art-1'].get('alterado') == 'redação'
assert 'serviço operacional diário' in _se_c['se-art-1']['caput'], 'a consulta mantém a finalidade original'
assert len(_se_a['se-art-2-r1']['items']) == 10 and _se_a['se-art-2-r1']['items'][9]['text'].startswith('X - uniformizar')
assert _se_a['se-art-2-r1']['items'][7]['text'].endswith(';') and _se_a['se-art-2-r1']['items'][8]['text'].endswith('; e')
_sci_a = {a['id']: a for c in atual['chapters'] if c['id'].endswith('seguranca-contra-incendio') for a in c['articles']}
_sci_c = {a['id']: a for c in consulta['chapters'] if c['id'].endswith('seguranca-contra-incendio') for a in c['articles']}
assert 'ro-art-13-c1' in _sci_a and _sci_a['ro-art-13-c1']['caput'].startswith('Entende-se por política do serviço técnico')
assert 'ro-art-13-c1' not in _sci_c and not _sci_a['ro-art-13-c1'].get('proposta')
# 15/09: Superior de Dia com alcance estadual
assert 'todo o território estadual' in _se_a['se-art-31-c1']['caput'] and 'Capital' not in _se_a['se-art-31-c1']['caput']
assert not any('Capital' in it['text'] for it in _se_a['se-art-31-c2']['items'])
# se-art-31 (área de atuação) suprimido nas duas versões em 16/09 (duplicidade com se-art-31-c1)
assert 'se-art-43-c1' not in {a['id'] for a in A['servico-operacional']['articles']}, 'competências operacionais do Oficial de Dia suprimidas em 16/09'
# 16/09: supressões comuns às DUAS versões; alterações de texto só na atual
for _tema, _ids in {'servico-operacional': ['se-art-31', 'se-art-39', 'se-art-42', 'se-art-44', 'se-art-45', 'se-art-116', 'se-art-137', 'se-art-147'],
                    'servico-interno-dia': ['se-art-54', 'se-art-71', 'se-art-77', 'se-art-91'], 'disposicoes-finais': ['mt-art-265']}.items():
    for _id in _ids:
        assert _id not in {a['id'] for a in A[_tema]['articles']} and _id not in {a['id'] for a in C[_tema]['articles']}, f'{_tema}/{_id} deveria estar fora das duas versões'
        assert any(sp['id'] == _id and sp.get('ambas') for sp in C[_tema].get('suprimidos', [])), f'{_tema}/{_id} sem registro em suprimidos da consulta'
assert 'se-art-136' in {a['id'] for a in C['servico-operacional']['articles']} and 'se-art-136' in _se_a and 'Sistema de Comando de Incidentes' in _se_a['se-art-136']['caput']
assert 'Sistema de Comando de Incidentes' not in _se_c['se-art-136']['caput'], 'alteração de texto fica só na atual'
_sci6 = {v: {a['id']: a for a in X['seguranca-contra-incendio']['articles']}['ro-art-6'] for v, X in (('c', C), ('a', A))}
assert all(_sci6[v]['items'][0]['text'] == '' and 0 in _sci6[v]['incisos_suprimidos'] for v in 'ca'), 'parágrafo único das DAT suprimido nas duas versões'
_od = _se_a['se-art-38-c2']
assert _od['items'][18]['text'] == '' and 18 in _od['incisos_suprimidos'] and 'Sistema Eletrônico de Informações' in _od['items'][17]['text']
assert 'Comandante do COB I' in _se_a['se-art-25']['caput'] and 'Comandante do COB I' in _se_a['se-art-26']['caput'] and 'processo eletrônico' in _se_a['se-art-26']['items'][0]['text']
_dia_a = {a['id']: a for a in A['servico-interno-dia']['articles']}
assert _dia_a['se-art-61']['caput'].startswith('A passagem de serviço, presidida pelo Oficial de Dia no 1º Grupamento') and 'Comandante do SGBM' in _dia_a['se-art-62']['caput']
assert _dia_a['se-art-109']['caput'].startswith('Depois de publicada a escala em Boletim Interno') and 'EPI' in _dia_a['se-art-93']['items'][0]['text']
assert atual['curadoria']['suprimidos_ambas'] == 29 and consulta['curadoria']['suprimidos_ambas'] == 29 + sum(len(v) for v in SUPRIMIR.values())
for c in atual['chapters']:
    for a in c['articles']:
        texto = ' '.join([a.get('caput', '')] + [it['text'] for it in a.get('items', [])])
        assert 'Comandante Geral' not in texto, f'{c["id"]}/{a["id"]}: grafia "Comandante Geral" restante'

# 7c. Nenhuma menção nominal à equipe de curadoria no que ESTA curadoria produz (notas,
#     motivos e fundamentos dos artigos alterados/novos/suprimidos) — vai para tela e .docx.
import re  # noqa: E402
for c in atual['chapters']:
    for a in c['articles'] + c.get('suprimidos', []):
        if not (a.get('origem') == 'consulta-2026-08' or a.get('alterado') or a.get('corrigido') or a.get('motivo')):
            continue
        campos = ' '.join(str(a.get(k, '')) for k in ('nota', 'motivo', 'fundamento_alteracao'))
        assert not re.search(r'Tiago|W[aâ]ndrio', campos), f'{c["id"]}/{a["id"]}: menção nominal à equipe'
for s in (consulta, atual):
    por_art = s['curadoria']['atendimentos_artigos']
    assert por_art['reg:atual:servico-operacional/se-art-4']['como'] == 'incluido'
    ids_c = {a['editId'] for c in consulta['chapters'] for a in c['articles']}
    assert all(k in ids_c for k in por_art), 'atendimentos_artigos aponta para editId inexistente na consulta'
    assert 'atendimentos' not in s['curadoria']
    assert 'correcoes' not in consulta['curadoria']

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
_cont = {k: v for k, v in atual['curadoria'].items() if not k.startswith('atendimentos')}
print(f'OK — scripts/test_regulamento_curadoria_consulta.py (consulta {n_c} artigos, atual {n_a} artigos, '
      f'{len(propostas)} propostas pendentes, curadoria={_cont})')
