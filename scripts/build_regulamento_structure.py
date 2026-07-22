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

        articles = []
        for ex in primarios:
            caput_original = sem_prefixo_art(ex.get('caput'))
            caput_adaptado, mudou_caput = adapt_text(caput_original)
            items = []
            houve_adapt = mudou_caput
            for disp in ex.get('dispositivos', []):
                texto, mudou = adapt_text(disp)
                houve_adapt = houve_adapt or mudou
                items.append({'text': texto, 'source': ex['source']})
            n = art_num(ex.get('source'))
            leaf = {
                'id': f'{primary_uf}-art-{n}',
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
            articles.append(leaf)

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
