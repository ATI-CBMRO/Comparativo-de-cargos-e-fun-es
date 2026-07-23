"""Auditoria de integridade das citações verbatim (criada na auditoria de 2026-07-23).

Verifica cada excerpt (caput+dispositivos+source) dos 4 JSONs de estrutura
(minuta/regulamento × futura/atual) contra o markdown do DOCUMENTO reivindicado
pela citação — pega tanto paráfrase quanto a classe "documento errado" (AR-02:
texto verbatim, mas capturado da LOB/RI/Regulamento errado do MESMO estado, que
verificar_verbatim.py não detecta). Classifica:
  OK              — verbatim no documento certo, artigo existe
  OK_COM_RUIDO    — verbatim a menos de ruído de conversão (nº de página embutido,
                    cabeçalho corrente, ligadura tipográfica) — minors conhecidos
  DOC_ERRADO      — verbatim, mas em OUTRO documento do mesmo estado (bug PA/dpo)
  ART_INEXISTENTE — artigo citado não existe no documento reivindicado
  NAO_VERBATIM    — texto não achado verbatim em documento nenhum do estado
  SEM_FONTE       — estado sem markdown correspondente ao documento citado

Exceções conhecidas (whitelist EXCECOES abaixo, cada uma com justificativa) não
derrubam o exit code. Uso:  python3 scripts/auditoria_citacoes.py  (exit 1 se
houver achado fora da whitelist).
"""
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (trecho do id do dispositivo, trecho do source) -> justificativa
EXCECOES = [
    ('', 'CBMPR, Lei nº 22.206/2024, Art. 35',
     'caput reconstruído por intervalo de linhas (_PR_LOB_LINE_OVERRIDES do extrator: '
     'defeito sistemático do PDF do PR) — verificado manualmente, não casável por substring'),
    ('', 'CBMRS, RI (Portaria nº 001/2025), Art. 6',
     'fake_art_res do CONFIG["rs"] rebaixa deliberadamente "Art."→"art." na citação '
     'interna ao Decreto 53.897/2018 (falso cabeçalho de artigo)'),
    ('', 'CBMBA, Norma Operacional nº 01/2021, Art. 35',
     'ANEXO A (tabela) linearizado pelo PDF em ordem diferente da captura — '
     'PENDÊNCIA de curadoria registrada em .claude/PENDENCIAS.md (2026-07-23)'),
    ('', 'DOB nº 08 (Serviço de Salvamento Aquático e Mergulho, 2022), seção 9',
     'elisão do título "REFERÊNCIAS" no meio do bloco (classe de elisão sem "[...]" '
     'já registrada como minor)'),
]
MD = ROOT / 'database' / 'markdown'

LIG = {'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
def deslig(s):
    for k, v in LIG.items():
        s = s.replace(k, v)
    return s

RE_LINHA_RUIDO = re.compile(
    r'^\s*(#|\*|Art\.?\s*\d+\s*\.?\s*$|\d+\s*$|https?://|\d{2}/\d{2}/\d{4},?\s*\d{2}:\d{2})'
    r'|^\s*P[áa]g\.?\s*\d*\s*$'
    r'|^\s*(Art\.?\s*\d+\s*[.ºo]?\s*)+$'
    r'|CORPO DE BOMBEIROS MILITAR DE ALAGOAS|BOLETIM GERAL OSTENSIVO|MACEI[ÓO]'
    r'|NORMA\s*OPERACIONAL|RESIOBOM|leisestaduais\.com\.br')

def fonte_super(raw):
    return '\n'.join(ln for ln in raw.splitlines() if not RE_LINHA_RUIDO.search(ln))

def norm_ws(t):
    t = t.replace('­', '')
    t = re.sub(r'-\s*\n\s*', '', t)
    return re.sub(r'\s+', ' ', t).strip()

def apertar(s):
    return re.sub(r'[\s\-–—­]', '', s)

# ---- registro de documentos por estado ----
ABBR2NAME = {
 'AC':'Acre','AL':'Alagoas','AP':'Amapá','AM':'Amazonas','BA':'Bahia','CE':'Ceará',
 'DF':'Distrito Federal','ES':'Espírito Santo','GO':'Goiás','MA':'Maranhão',
 'MT':'Mato Grosso','MS':'Mato Grosso do Sul','MG':'Minas Gerais','PA':'Pará',
 'PB':'Paraíba','PR':'Paraná','PE':'Pernambuco','PI':'Piauí','RJ':'Rio de Janeiro',
 'RN':'Rio Grande do Norte','RS':'Rio Grande do Sul','RO':'Rondônia','RR':'Roraíma',
 'SC':'Santa Catarina','SP':'São Paulo','SE':'Sergipe','TO':'Tocantins'}

def sem_digitos(s):
    return re.sub(r'\d+', '', s)

sys.path.insert(0, str(ROOT / 'scripts'))
def fonte_limpa(path):
    """Reusa a limpeza do próprio pipeline (RE_NOISE/RE_TITLE_CAPS)."""
    try:
        from extrair_ri_alternativas import clean_lines_generic
        return '\n'.join(clean_lines_generic(path.name))
    except Exception:
        return path.read_text(encoding='utf-8', errors='replace')

_doc_cache = {}
def load_doc(path):
    if path not in _doc_cache:
        raw = deslig(path.read_text(encoding='utf-8', errors='replace'))
        limpo = deslig(fonte_limpa(path))
        sup = fonte_super(raw)
        _doc_cache[path] = {
            'raw': raw,
            'estrito': [norm_ws(raw), apertar(raw), norm_ws(limpo), apertar(limpo)],
            'ruido': [sem_digitos(apertar(raw)), sem_digitos(apertar(limpo)),
                      sem_digitos(apertar(sup))],
        }
    return _doc_cache[path]

def state_docs(abbr):
    name = ABBR2NAME[abbr]
    return sorted(MD.glob(f'{name} - *.md'))

def strip_acc(s):
    return unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()

LAWNUM = re.compile(r'(\d[\d.]*)\s*/\s*(\d{4})')

def claimed_docs(abbr, source, doc_label):
    """Resolve o(s) markdown(s) que a citação reivindica."""
    docs = state_docs(abbr)
    hint = f'{source or ""} {doc_label or ""}'
    hl = strip_acc(hint)
    # 1) por número de lei/norma citado no hint, presente no conteúdo (cabeçalho) ou nome do arquivo
    nums = LAWNUM.findall(hint)
    if nums:
        matched = []
        for p in docs:
            fn = strip_acc(p.name)
            head = strip_acc(load_doc(p)['raw'][:3000])
            for n, y in nums:
                pat = re.escape(n) + r'\s*[/\-]\s*' + y
                if re.search(pat, fn.replace('-', '/')) or re.search(pat, head):
                    matched.append(p); break
        if matched:
            return matched
    # 2) por tipo
    def by(*keys):
        return [p for p in docs if any(k in strip_acc(p.name) for k in keys)]
    if 'nga' in hl or 'normas gerais' in hl:
        return by('normas gerais')
    if 'norma operacional' in hl:
        r = by('norma operacional')
        if r: return r
        # ex.: BA — o arquivo "Regulamento de Serviço" É a Norma Operacional 01/2021
        r = [p for p in docs if 'NORMA OPERACIONAL' in load_doc(p)['raw'][:4000]]
        if r: return r
    if 'diretriz operacional' in hl or re.search(r'\bdob', hl):
        m = re.search(r'dob\s*n?[oº.]*\s*0?(\d+)|diretriz operacional n?o?\s*0?(\d+)', hl)
        if m:
            n = m.group(1) or m.group(2)
            return by(f'diretriz operacional 0{n}', f'diretriz operacional {n}')
        return by('diretriz operacional')
    if 'norma operacional' in hl or re.search(r'\bno[\s\-]?\d', hl):
        m = re.search(r'norma operacional n?o?\s*0?(\d+)|\bno[\s\-]?0?(\d+)', hl)
        if m:
            n = m.group(1) or m.group(2)
            return by(f'norma operacional 0{n}', f'norma operacional {n}')
        return by('norma operacional')
    if 'risd' in hl:
        return by('regulamento interno', 'regimento de servico', 'regulamento de servico')
    if re.search(r'\bri\b', hl) or 'regimento interno' in hl or 'minuta de ri' in hl:
        r = by('regimento interno')
        if r: return r
        # MT: "RI" renomeado para Regulamento Geral (rename puro)
        return by('regulamento geral')
    if 'regulamento' in hl:
        return by('regulamento')
    if 'organizacao basica' in hl or re.search(r'\blob\b', hl) or re.search(r'\blei\b', hl) or re.search(r'\blc\b', hl):
        return by('organizacao basica', 'lei de organizacao')
    if 'risg' in hl or 'exercito' in hl:
        return [MD / 'RISG.md']
    return docs  # sem pista: aceita qualquer doc do estado (reporta como fraco)

ART = re.compile(r'art\.?\s*(\d+)', re.I)

def art_exists(path, n):
    raw = load_doc(path)['raw']
    digitos = r'\s*'.join(str(n))  # tolera OCR que parte dígitos: "Art. 1 9."
    return re.search(rf'[Aa]rt\.?\s*{digitos}\s*[.ºoO°º\-–—\s]', raw) is not None

def verbatim_in(text, path):
    """-> 'estrito' | 'ruido' | None"""
    d = load_doc(path)
    tl = deslig(text)
    if norm_ws(tl) in d['estrito'][0] or apertar(tl) in d['estrito'][1] \
       or norm_ws(tl) in d['estrito'][2] or apertar(tl) in d['estrito'][3]:
        return 'estrito'
    alvo = sem_digitos(apertar(deslig(text)))
    if alvo and any(alvo in f for f in d['ruido']):
        return 'ruido'
    return None

def check_excerpt(abbr, source, doc_label, texts):
    """-> (status, detalhe)"""
    if abbr == 'EB':
        claimed = [MD / 'RISG.md']
    else:
        claimed = claimed_docs(abbr, source, doc_label)
    claimed = [p for p in claimed if p.exists()]
    if not claimed:
        return 'SEM_FONTE', f'nenhum markdown p/ hint "{doc_label} | {source}"'
    texts = [t for t in texts if t and t.strip()]
    bad = None
    for p in claimed:
        levels = {t: verbatim_in(t, p) for t in texts}
        missing = [t for t, lv in levels.items() if lv is None]
        if not missing:
            m = ART.search(source or '')
            if m and not art_exists(p, m.group(1)):
                return 'ART_INEXISTENTE', f'Art. {m.group(1)} não achado em {p.name}'
            if any(lv == 'ruido' for lv in levels.values()):
                n = sum(1 for lv in levels.values() if lv == 'ruido')
                return 'OK_COM_RUIDO', f'{p.name} ({n} trecho(s) com ruído de página embutido)'
            return 'OK', p.name
        bad = missing
    others = [p for p in (state_docs(abbr) if abbr != 'EB' else []) if p not in claimed]
    for p in others:
        if all(verbatim_in(t, p) for t in texts):
            return 'DOC_ERRADO', f'texto achado em {p.name}, não em {[c.name for c in claimed]}'
    frag = norm_ws(bad[0])[:90] if bad else ''
    return 'NAO_VERBATIM', f'{len(bad)}/{len(texts)} trechos não achados; ex.: "{frag}" (reivindicado: {[c.name for c in claimed]})'

def walk_alt_nodes(obj):
    if isinstance(obj, dict):
        if 'alternatives' in obj and isinstance(obj['alternatives'], dict):
            yield obj
        for v in obj.values():
            yield from walk_alt_nodes(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_alt_nodes(v)

def audit_file(rel):
    path = ROOT / rel
    if not path.exists():
        print(f'!! {rel} não existe'); return []
    data = json.load(open(path))
    rows = []
    for node in walk_alt_nodes(data):
        nid = node.get('id') or node.get('editId') or node.get('title', '?')
        for key, alt in node['alternatives'].items():
            abbr = (alt.get('abbr') or key.split('_')[0]).split('_')[0].upper()
            if strip_acc(alt.get('name', '')) in ('exercito brasileiro',):
                abbr = 'EB'
            for ex in alt.get('excerpts', []):
                texts = [ex.get('caput', '')] + list(ex.get('dispositivos', []))
                status, det = check_excerpt(abbr, ex.get('source', ''), alt.get('docLabel', ''), texts)
                rows.append((rel, nid, key, ex.get('source', ''), status, det))
    return rows

def main():
    files = ['database/minuta_structure.json', 'database/regulamento_structure.json',
             'database/atual/minuta_structure.json', 'database/atual/regulamento_structure.json']
    all_rows = []
    for f in files:
        all_rows += audit_file(f)
    from collections import Counter
    c = Counter(r[4] for r in all_rows)
    print('TOTAL excerpts verificados:', len(all_rows))
    for k, v in c.most_common():
        print(f'  {k}: {v}')
    print()
    def whitelisted(r):
        return any(nid_part in str(r[1]) and src_part in str(r[3])
                   for nid_part, src_part, _ in EXCECOES)
    falhas = 0
    for r in all_rows:
        if r[4] in ('OK', 'OK_COM_RUIDO'):
            continue
        marca = 'EXCEÇÃO (whitelist)' if whitelisted(r) else 'FALHA'
        if marca == 'FALHA':
            falhas += 1
        print(marca, '|', ' | '.join(str(x) for x in r))
    print(f'\n{falhas} falha(s) fora da whitelist.')
    return 1 if falhas else 0

if __name__ == '__main__':
    sys.exit(main())
