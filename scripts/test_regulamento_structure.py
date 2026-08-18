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
                    or 'NGA-CIOP-001/2026' in leaf['fundamento']
                    or 'Resolução nº 121/2022/CBM-CP' in leaf['fundamento']), \
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
# enrichment). Em 2026-08-13/14/18 ele passou de 413 para 408 (por 396, 415, 416 e 411)
# por decisão de curadoria, não por regressão — a aritmética, conferida artigo a artigo:
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
#     -8 artigos com resíduo de CIOP fora do capítulo próprio (mt-art-228, mt-art-229,
#        mt-art-230, mt-art-231, mt-art-232, mt-art-233, se-art-48, se-art-49 — matéria
#        da NGA-CIOP-001/2026, que o Regulamento remete em vez de duplicar — ver
#        regulamento_reescrita.py)
#     = 408
#     -1 artigo de servico-operacional (se-art-113 — regras próprias de entrevista
#        importadas de Sergipe, matéria da Resolução nº 121/2022/CBM-CP)
#     +1 artigo de redação própria (prestação de informações à imprensa), fundado na
#        Resolução nº 121/2022/CBM-CP
#     = 408
#     +1 artigo de redação própria (atendimento a tentativas de suicídio — remissão
#        genérica ao protocolo ATTS), fundado na LOB (Art. 2º, IV e VII, e Art. 15)
#     = 409
#     -10 artigos de atribuicoes-funcoes (mt-art-200/201/238/239/250/251/255/256/262/263 —
#        funções do COB e da "Diretoria de Segurança Contra Incêndio" do MT, cargo que não
#        existe com esse nome na estrutura real da CAT)
#     +19 artigos de redação própria (10 funções do Comando Operacional de Bombeiros + 9 da
#        Coordenadoria de Atividades Técnicas), fundados na LOB (Art. 18, Art. 34, Art. 35
#        e Art. 47) e no organograma oficial do CBMRO (Task 8, 2026-08-18)
#     = 418
# Ver scripts/regulamento_reescrita.py para o motivo de cada remoção.
assert len(edit_ids) >= 418, f'regressão: {len(edit_ids)} artigos (esperado >= 418)'
autorais = [l for c in d['chapters'] for l in c['articles'] if l.get('autoral')]
assert len(autorais) == 61, \
    f'artigos autorais: {len(autorais)} (esperado 15 SCI + 21 org.-geral + 4 CIOP + 1 ' \
    f'mídia + 1 ATTS + 10 COB + 9 CAT = 61)'
for tema in ('seguranca-contra-incendio', 'organizacao-geral', 'central-operacoes-193'):
    cap = [c for c in d['chapters'] if c['themeKey'] == tema][0]
    assert all(l.get('autoral') for l in cap['articles']), \
        f'capítulo {tema} deve ser 100% redação própria'
    assert cap['alternatives'], f'Bloco D do capítulo {tema} foi perdido'

for c in d['chapters']:
    assert c['primary']['uf'] != 'risg', f"RISG não pode ser fonte primária: {c['themeKey']}"

# Capítulo misto (2026-08-18): todo artigo precisa de tag de órgão, senão some do recorte
# do participante em silêncio — o filtro de escopo é fail-closed (src/lib/escopoServico.js).
_af = next(c for c in d['chapters'] if c['themeKey'] == 'atribuicoes-funcoes')
_sem_tag = [a['editId'] for a in _af['articles'] if not a.get('orgao')]
assert not _sem_tag, f'artigos sem tag de órgão no capítulo misto: {_sem_tag}'
_no_escopo = [a for a in _af['articles'] if a.get('orgao') in ('cob', 'cat')]
assert _no_escopo, 'nenhum artigo de COB/CAT — o recorte ficaria com o capítulo vazio'
assert all(a.get('autoral') for a in _no_escopo), \
    'artigo de COB/CAT no capítulo misto precisa ser redação própria sobre a LOB de RO'

print(f"OK — scripts/test_regulamento_structure.py ({len(d['chapters'])} capítulos, "
      f"{len(edit_ids)} artigos, schema compatível com buildArticles)")
