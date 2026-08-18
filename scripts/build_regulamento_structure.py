"""Gera database/regulamento_structure.json — a MINUTA do Regulamento Geral do CBMRO.

Mesmo formato de minuta_structure.json (chapters -> articles -> incisos), o que dá de
graça a numeração contínua (minutaArticles.js), o export .docx (minutaDocx.js), o wizard
e o módulo de revisão. Conteúdo: para cada um dos 15 temas, o texto PROPOSTO vem da
fonte primária do tema (PRIMARY_SOURCE — nunca "MT por padrão"), ADAPTADO para RO pela
tabela ADAPTATIONS (original preservado); os demais estados entram em `alternatives`
por tema, SEM adaptação (o comparador exibe o texto original de cada estado).

Ordem: python3 scripts/extrair_regulamentos.py  →  este script.
Valida: python3 scripts/test_regulamento_structure.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from regulamento_enrichment import (  # noqa: E402
    THEMES, THEME_KEYS, PRIMARY_SOURCE, REGULAMENTO_DOCS, REGULAMENTO_ENRICHMENT, adapt_text,
)
from regulamento_reescrita import (  # noqa: E402
    REMOVER_ARTIGOS, REMOVER_INCISOS, SUBSTITUI_INTEGRALMENTE, ARTIGOS_PROPRIOS,
    SUBSTITUIR_TERMOS, ORGAO_DO_ARTIGO,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'database' / 'regulamento_structure.json'

STATE_NAMES = {
    'al': 'Alagoas', 'df': 'Distrito Federal', 'go': 'Goiás', 'mt': 'Mato Grosso',
    'pa': 'Pará', 'pr': 'Paraná', 'rn': 'Rio Grande do Norte',
    'rs': 'Rio Grande do Sul', 'se': 'Sergipe',
    'ba': 'Bahia', 'rr': 'Roraima', 'to': 'Tocantins', 'to_corpo': 'Tocantins',
    'al_no03': 'Alagoas', 'al_no04': 'Alagoas', 'al_no06': 'Alagoas',
    'al_no07': 'Alagoas', 'al_no11': 'Alagoas',
    'al_dob05': 'Alagoas', 'al_dob06': 'Alagoas', 'al_dob07': 'Alagoas', 'al_dob08': 'Alagoas',
    'risg': 'Exército Brasileiro',
    'es': 'Espírito Santo',
}

# 2 Partes do Regulamento (spec 2026-07-21): Parte I — Geral | Parte II — do Serviço.
TEMA_PARTE = {
    'disposicoes-preliminares': 'geral', 'organizacao-geral': 'geral',
    'competencias-direcao': 'geral', 'competencias-apoio-assessoramento': 'geral',
    'competencias-execucao': 'geral', 'pessoal-quadros': 'geral',
    'ensino-instrucao': 'geral', 'cerimonial-honras': 'geral',
    'disciplina-correicao': 'geral', 'uniformes-apresentacao': 'geral',
    'seguranca-contra-incendio': 'geral', 'disposicoes-finais': 'geral',
    'servico-operacional': 'servico', 'servico-interno-dia': 'servico',
    'atribuicoes-funcoes': 'servico', 'central-operacoes-193': 'servico',
}

RE_ART_PREFIX = re.compile(r'^\s*Art\s*\.?\s*\d[\d\s]{0,3}\s*[ºo°]?\s*\.?\s*[-–—]?\s*')


def sem_prefixo_art(caput):
    """Tira o "Art. Nº" do início — a numeração da minuta é contínua e própria."""
    return RE_ART_PREFIX.sub('', caput or '').strip()


def art_num(source):
    m = re.search(r'Art\.\s*(\d+)', source or '')
    return int(m.group(1)) if m else 0


def build():
    chapters = []
    pendencias = []
    for theme_key, theme_title, group in THEMES:
        primary_uf = PRIMARY_SOURCE[theme_key]
        primarios = REGULAMENTO_ENRICHMENT.get((theme_key, primary_uf), [])
        primarios = sorted(primarios, key=lambda e: art_num(e.get('source')))

        # Camada de reescrita (scripts/regulamento_reescrita.py): dispositivos que citam
        # órgão inexistente em RO SAEM, e temas cujo texto importado descrevia outra
        # corporação são substituídos por redação própria fundada na lei de Rondônia.
        fora_art = REMOVER_ARTIGOS.get(theme_key, {})
        fora_inc = REMOVER_INCISOS.get(theme_key, {})
        if theme_key in SUBSTITUI_INTEGRALMENTE:
            primarios = []

        articles = []
        for ex in primarios:
            n = art_num(ex.get('source'))
            art_id = f'{primary_uf}-art-{n}'
            if art_id in fora_art:
                continue
            caput_original = sem_prefixo_art(ex.get('caput'))
            caput_adaptado, mudou_caput = adapt_text(caput_original)
            # Substituição de termo por artigo (ex.: "Supervisor de Dia", figura que não
            # existe no CBMRO — ver docs/curadoria/depara-supervisor-de-dia.md). Roda
            # DEPOIS da adaptação de termos (ADAPTATIONS) e não mexe em `caput_original`
            # (o texto original preservado em `original_caput` é o pré-ADAPTATIONS).
            termos = SUBSTITUIR_TERMOS.get(theme_key, {}).get(art_id, [])
            for de, para in termos:
                if de in caput_adaptado:
                    caput_adaptado = caput_adaptado.replace(de, para)
                    mudou_caput = True
            # Incisos que citam órgão inexistente saem — casados por TEXTO, contra o
            # dispositivo original, para não depender de índice posicional (AR-03).
            trechos = fora_inc.get(art_id, [])
            dispositivos = [x for x in ex.get('dispositivos', [])
                            if not any(t in x for t in trechos)]
            tirar = len(ex.get('dispositivos', [])) - len(dispositivos)
            items = []
            houve_adapt = mudou_caput
            for disp in dispositivos:
                texto, mudou = adapt_text(disp)
                for de, para in termos:
                    if de in texto:
                        texto = texto.replace(de, para)
                        mudou = True
                houve_adapt = houve_adapt or mudou
                items.append({'text': texto, 'source': ex['source']})
            leaf = {
                'id': art_id,
                'kind': 'incisos',
                'editId': f'reg:{theme_key}/{primary_uf}-art-{n}',
                'caput': caput_adaptado,
                'items': items,
                'source': ex['source'],
                'match': ex.get('match', 'exata'),
                'heading': ex.get('heading'),
            }
            if houve_adapt:
                leaf['adapted'] = True
                leaf['original_caput'] = caput_original
            if tirar:
                # AR-03: tirar inciso re-indexa os seguintes, então `editId#index` deixa de
                # endereçar o mesmo conteúdo. Mesma convenção do minutaArticles.js.
                leaf['reindexed'] = True
                leaf['incisos_removidos'] = tirar
            # Tag de órgão (Task 8, 2026-08-18): só o capítulo misto atribuicoes-funcoes
            # usa isto hoje — o filtro de escopo do Regulamento de Serviço
            # (src/lib/escopoServico.js) lê o campo `orgao` para decidir o que entra no
            # recorte. Artigo sem tag simplesmente não grava o campo (não None/vazio).
            orgao = ORGAO_DO_ARTIGO.get(theme_key, {}).get(art_id)
            if orgao:
                leaf['orgao'] = orgao
            articles.append(leaf)

        # Artigos de redação própria, fundados na lei de Rondônia.
        for i, art in enumerate(ARTIGOS_PROPRIOS.get(theme_key, []), start=1):
            art_id = f'ro-art-{i}'
            gerado = {
                'id': art_id,
                'kind': 'incisos',
                'editId': f'reg:{theme_key}/{art_id}',
                'caput': art['caput'],
                'items': [{'text': t, 'source': art['fundamento']} for t in art.get('dispositivos', [])],
                'source': art['fundamento'],
                'match': 'exata',
                'heading': art.get('heading'),
                'autoral': True,
                'fundamento': art['fundamento'],
            }
            if art.get('orgao'):
                gerado['orgao'] = art['orgao']
            articles.append(gerado)

        if not articles:
            pendencias.append(theme_key)

        # Alternativas por tema: os demais estados, texto ORIGINAL (sem adaptação).
        alternatives = {}
        for uf in REGULAMENTO_DOCS:
            if uf == primary_uf:
                continue
            excerpts = REGULAMENTO_ENRICHMENT.get((theme_key, uf))
            if not excerpts:
                continue
            alternatives[uf] = {
                'name': STATE_NAMES[uf],
                'abbr': uf.upper(),
                'docLabel': REGULAMENTO_DOCS[uf]['label'],
                'excerpts': sorted(excerpts, key=lambda e: art_num(e.get('source'))),
            }

        chapters.append({
            'id': f'reg:{theme_key}',
            'kind': 'articles',
            'chapterTitle': theme_title.upper(),
            'group': group,
            'themeKey': theme_key,
            'parte': TEMA_PARTE[theme_key],
            'primary': {
                'uf': primary_uf,
                'name': STATE_NAMES[primary_uf],
                'docLabel': REGULAMENTO_DOCS[primary_uf]['label'],
            },
            'status': 'pendente' if not articles else 'rascunho',
            'articles': articles,
            'alternatives': alternatives,
        })

    # Parte I (geral) antes da Parte II (servico); dentro de cada Parte, ordem dos THEMES.
    _ordem_parte = {'geral': 0, 'servico': 1}
    chapters.sort(key=lambda c: (_ordem_parte[c['parte']], THEME_KEYS.index(c['themeKey'])))

    structure = {
        'generated_by': 'scripts/build_regulamento_structure.py',
        'title': 'Minuta de Regulamento Geral do Corpo de Bombeiros Militar de Rondônia',
        'chapters': chapters,
    }
    OUT.write_text(json.dumps(structure, ensure_ascii=False, indent=1), encoding='utf-8')
    total_arts = sum(len(c['articles']) for c in chapters)
    total_alt = sum(len(alt['excerpts']) for c in chapters for alt in c['alternatives'].values())
    print(f'Gerado: {OUT}')
    print(f'Capítulos: {len(chapters)} | artigos propostos: {total_arts} | excerpts alternativos: {total_alt}')
    if pendencias:
        print(f'Capítulos pendentes (sem fonte primária): {pendencias}')


if __name__ == '__main__':
    build()
