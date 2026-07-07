"""Garimpo automático de candidatos por tema, para acelerar a curadoria dos
regulamentos estaduais (Bloco B1-M, passo 1 — "os textos não casam perfeitamente
entre estados").

Este script NÃO decide nada: só reduz o volume de texto que precisa ser lido com
atenção (pelo modelo mais capaz ou pelo Wândrio) para montar o de-para tema -> artigos
de cada estado (passo 2). Ranqueia trechos candidatos por palavra-chave (expandida
pelo glossário de sinônimos) + similaridade barata de sequência — sem dependências
externas, só stdlib.

Uso:
    python3 scripts/sugerir_equivalencias.py <uf>   (ex.: mt, rn, se)

Gera docs/curadoria/candidatos-<uf>.md
"""
import re
import sys
import unicodedata
from pathlib import Path
from difflib import SequenceMatcher

sys.path.insert(0, str(Path(__file__).resolve().parent))
from equivalencias_terminologicas import expand_terms  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_DIR = ROOT / 'database' / 'markdown'
OUT_DIR = ROOT / 'docs' / 'curadoria'

# Inventário dos regulamentos/regimentos disponíveis no acervo (arquivo .md por UF).
# Mesmo inventário que scripts/regulamento_enrichment.py (Bloco B1) vai usar — cresce
# conforme o Wândrio conseguir novos PDFs de regulamento.
REGULAMENTO_DOCS = {
    'al': 'Alagoas - Regimento Interno.md',
    'df': 'Distrito Federal - Regimento Interno.md',
    'go': 'Goiás - Regimento dos Serviços Interno e Operacional.md',
    'mt': 'Mato Grosso - Regimento Interno.md',
    'pa': 'Pará - Regimento Interno.md',
    'pr': 'Paraná - Regimento Interno.md',
    'rn': 'Rio Grande do Norte - Regulamento Geral (Decreto 31.139-2021).md',
    'rs': 'Rio Grande do Sul - Regimento Interno.md',
    'se': 'Sergipe - Regimento Interno.md',
}

# Taxonomia de temas (mesma do futuro scripts/regulamento_enrichment.py) — cada tema
# tem palavras-chave-semente que orientam o garimpo (expandidas pelo glossário).
THEMES = [
    ('disposicoes-preliminares', 'Disposições Preliminares',
     ['disposições preliminares', 'finalidade', 'âmbito de aplicação']),
    ('organizacao-geral', 'Organização Geral',
     ['estrutura orgânica', 'organização básica', 'organograma']),
    ('competencias-direcao', 'Competências de Direção',
     ['comandante-geral', 'subcomandante-geral', 'competência', 'atribuições do comando']),
    ('competencias-apoio-assessoramento', 'Competências de Apoio e Assessoramento',
     ['assessoria', 'assessoramento', 'apoio administrativo']),
    ('competencias-execucao', 'Competências de Execução',
     ['execução operacional', 'unidades operacionais', 'comando de área']),
    ('servico-operacional', 'Serviço Operacional',
     ['serviço operacional', 'escala de serviço', 'guarnição de serviço', 'regime de serviço']),
    ('servico-interno-dia', 'Serviço Interno / de Dia',
     ['serviço de dia', 'serviço de permanência', 'oficial de dia', 'fiscal de dia']),
    ('atribuicoes-funcoes', 'Atribuições de Funções',
     ['atribuições do comandante', 'atribuições do subcomandante', 'atribuições do chefe']),
    ('disciplina-correicao', 'Disciplina e Correição',
     ['disciplina', 'corregedoria', 'transgressão disciplinar', 'conselho de disciplina']),
    ('uniformes-apresentacao', 'Uniformes e Apresentação',
     ['uniforme', 'apresentação pessoal', 'traje']),
    ('cerimonial-honras', 'Cerimonial e Honras',
     ['cerimonial militar', 'honras militares', 'continência']),
    ('disposicoes-finais', 'Disposições Finais',
     ['disposições finais', 'disposições gerais', 'casos omissos']),
]


def normalize(text):
    text = unicodedata.normalize('NFKD', text.lower())
    return ''.join(c for c in text if not unicodedata.combining(c))


def split_articles(text):
    """Quebra o markdown em blocos por 'Art. Nº' (ou 'Artigo Nº'), do início de cada
    artigo até o próximo — mantém cabeçalho + corpo juntos."""
    pattern = re.compile(r'(?=^\s*Art(?:igo)?\.?\s*\d+)', re.IGNORECASE | re.MULTILINE)
    parts = pattern.split(text)
    return [p.strip() for p in parts if p.strip()]


def expand_keywords(keywords):
    expanded = set()
    for kw in keywords:
        expanded |= expand_terms(kw)
    return expanded


def score_article(article_norm, keywords_norm):
    """Score barato: +2 por palavra-chave (ou sinônimo) encontrada literalmente, mais
    a razão de similaridade de sequência com as keywords juntas — pega trechos que
    usam vocabulário parecido mesmo sem a palavra-chave exata."""
    score = 0.0
    for kw in keywords_norm:
        if kw in article_norm:
            score += 2.0
    joined_kw = ' '.join(keywords_norm)
    score += SequenceMatcher(None, article_norm[:400], joined_kw).ratio()
    return score


def sugerir(uf, top_n=8):
    uf = uf.lower()
    filename = REGULAMENTO_DOCS.get(uf)
    if not filename:
        raise SystemExit(f"UF '{uf}' não está em REGULAMENTO_DOCS. Disponíveis: {sorted(REGULAMENTO_DOCS)}")
    md_path = MARKDOWN_DIR / filename
    if not md_path.exists():
        raise SystemExit(f"Markdown não encontrado: {md_path}")

    text = md_path.read_text(encoding='utf-8', errors='replace')
    articles = split_articles(text)
    articles_norm = [normalize(a) for a in articles]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f'candidatos-{uf}.md'
    lines = [
        f'# Candidatos de equivalência — {filename}',
        '',
        '> Gerado automaticamente por `scripts/sugerir_equivalencias.py`. NÃO decide',
        '> nada — é um garimpo por palavra-chave para reduzir o volume de leitura antes',
        '> do de-para (feito por leitura humana/modelo capaz, Bloco B1-M passo 2).',
        '> Sempre conferir contra o texto integral antes de transcrever verbatim.',
        '',
    ]
    for theme_key, theme_title, keywords in THEMES:
        expanded = expand_keywords(keywords)
        scored = []
        for art, art_norm in zip(articles, articles_norm):
            s = score_article(art_norm, expanded)
            if s > 0:
                scored.append((s, art))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:top_n]
        lines.append(f'## {theme_title} (`{theme_key}`)')
        lines.append('')
        if not top:
            lines.append('_Nenhum candidato encontrado por palavra-chave._')
            lines.append('')
            continue
        for score, art in top:
            heading = art.splitlines()[0][:120]
            lines.append(f'- **score {score:.1f}** — {heading}')
        lines.append('')

    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Gerado: {out_path} ({len(articles)} artigos varridos)')
    return out_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('Uso: python3 scripts/sugerir_equivalencias.py <uf>  (ex.: mt, rn, se)')
    sugerir(sys.argv[1])
