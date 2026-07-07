"""Verifica que cada dispositivo transcrito em REGULAMENTO_ENRICHMENT existe
LITERALMENTE no markdown de origem do estado (normalizando só espaços/hífens/quebras
de linha — nunca acento ou caixa) — pega na hora qualquer paráfrase acidental
introduzida na transcrição (Bloco B1-M, passo 4), antes de entrar na minuta do
Regulamento.

Entra no `npm run test:py`. Enquanto scripts/regulamento_enrichment.py não existir
(a curadoria do Bloco B1 ainda não começou), o script não falha — só avisa e sai OK,
para não quebrar o `test:py` antes da curadoria começar.

Uso:
    python3 scripts/verificar_verbatim.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_DIR = ROOT / 'database' / 'markdown'
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from regulamento_enrichment import REGULAMENTO_ENRICHMENT, REGULAMENTO_DOCS
except ImportError:
    REGULAMENTO_ENRICHMENT = None
    REGULAMENTO_DOCS = None


def normalize_whitespace(text):
    """Normaliza só espaços/hífens/quebras de linha — a verificação é verbatim
    (literal), então NUNCA mexe em acento ou caixa."""
    text = text.replace('­', '')       # hífen de quebra de linha do PDF
    text = re.sub(r'-\s*\n\s*', '', text)     # palavra hifenizada partida em 2 linhas
    text = re.sub(r'\s+', ' ', text)          # colapsa espaços/quebras de linha
    return text.strip()


def _apertar(s):
    """Só letras/dígitos/pontuação essencial: remove espaços e hifens/travessões —
    tolera artefatos de PDF ("ór gão") e hifenização de quebra de linha
    ("Comandante-\\nGeral" vs "Comandante-Geral"); as LETRAS continuam verbatim."""
    return re.sub(r'[\s\-–—­]', '', s)


def _fonte_limpa(state_id, raw):
    """Reusa o PRÓPRIO pipeline do extrator (inline_split, falsos cabeçalhos, filtros
    de ruído/títulos) para montar a fonte limpa — paridade garantida com a transcrição."""
    try:
        import extrair_regulamentos as ex
    except ImportError:
        return raw
    cfg = ex.CONFIG.get(state_id)
    if cfg is None:
        return raw
    lines = ex.load_for(cfg)
    keep = [ln for ln in lines
            if not (ex.RE_NOISE.match(ln) or (ln.strip() and ex.RE_TITLE_CAPS.match(ln.strip())))]
    return '\n'.join(keep)


def carrega_markdown(state_id, _cache={}):
    if state_id in _cache:
        return _cache[state_id]
    doc = REGULAMENTO_DOCS[state_id]
    # Aceita tanto o formato antigo (string) quanto o novo ({label, md}).
    filename = doc['md'] if isinstance(doc, dict) else doc
    path = MARKDOWN_DIR / filename
    raw = path.read_text(encoding='utf-8', errors='replace')
    limpo = _fonte_limpa(state_id, raw)
    # Pares (norm, apertado) para a fonte crua e para a fonte limpa.
    _cache[state_id] = tuple(
        v for base in (raw, limpo)
        for v in (normalize_whitespace(base), _apertar(base))
    )
    return _cache[state_id]


def esta_verbatim(trecho, fontes):
    alvo = normalize_whitespace(trecho)
    alvo_apertado = _apertar(trecho)
    for i, fonte in enumerate(fontes):
        chave = alvo_apertado if i % 2 else alvo
        if chave in fonte:
            return True
    return False


def verificar():
    if REGULAMENTO_ENRICHMENT is None:
        print('scripts/regulamento_enrichment.py ainda não existe (curadoria do Bloco B1 '
              'não começou) — nada para verificar.')
        return 0

    erros = []
    for (theme_key, state_id), excerpts in REGULAMENTO_ENRICHMENT.items():
        fonte_pair = carrega_markdown(state_id)
        for excerpt in excerpts:
            for dispositivo in excerpt.get('dispositivos', []):
                if dispositivo.strip() and not esta_verbatim(dispositivo, fonte_pair):
                    erros.append(f'[{state_id}/{theme_key}] dispositivo NÃO encontrado verbatim: "{normalize_whitespace(dispositivo)[:80]}..."')
            caput = excerpt.get('caput')
            if caput and caput.strip() and not esta_verbatim(caput, fonte_pair):
                erros.append(f'[{state_id}/{theme_key}] caput NÃO encontrado verbatim: "{normalize_whitespace(caput)[:80]}..."')

    if erros:
        print(f'{len(erros)} dispositivo(s) NÃO batem com o texto de origem:')
        for e in erros:
            print(' -', e)
        return 1

    total = sum(len(v) for v in REGULAMENTO_ENRICHMENT.values())
    print(f'OK — {total} excerpt(s) verificados, todos verbatim.')
    return 0


if __name__ == '__main__':
    sys.exit(verificar())
