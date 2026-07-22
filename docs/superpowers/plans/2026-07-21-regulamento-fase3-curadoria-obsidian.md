# Fase 3 — Curadoria no Obsidian (piloto) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Semear no vault Obsidian o repositório de curadoria do Regulamento: índice + 19 notas de fonte + o tema-piloto `servico-operacional` (nota de tema + notas de decisão onde há divergência real).

**Architecture:** Notas nascem do `database/regulamento_structure.json` (dados verificados; NUNCA reler PDFs). Semeadura única — depois as notas são do Wândrio. Fonte da verdade continua no repo; o vault orienta.

**Tech Stack:** Markdown do Obsidian (frontmatter YAML, wikilinks `[[...]]`), Python 3 (só para extrair/verificar dados do JSON — sem criar scripts no repo; usar heredocs).

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-21-regulamento-fase3-curadoria-obsidian-design.md`.
- Vault: `/Users/wandriobandeira/Documents/Obsidian Vault/`. Pasta nova:
  `Codebases/Comparativo-de-cargos-e-funcoes/Regulamento — Curadoria/` (criar).
- Dados: SOMENTE de `database/regulamento_structure.json` (e CLAUDE.md para contexto de fonte). Nenhum PDF.
- Todo excerto legal citado é VERBATIM do JSON, com a citação `cf. …` do campo `source`. Proibido parafrasear texto de lei.
- Notas em pt-BR, tom claro para não-dev; tabelas enxutas (apontar para o portal, não duplicar tudo).
- NENHUMA mudança de código no repo; nada commitado além de docs (o vault está fora do git).
- Wikilinks usam o nome EXATO do arquivo alvo sem `.md` (ex.: `[[Fonte — RISD-SE]]`).
- Nomes de arquivo definidos na Task 1/2/3 são contrato — não renomear depois.

---

### Task 1: Índice + 19 notas de Fonte

**Files:**
- Create (no vault, pasta `Regulamento — Curadoria/`):
  - `_Índice — Curadoria do Regulamento.md`
  - 19 notas `Fonte — <slug>.md` (lista exata no Step 1)

**Interfaces:**
- Produces: nomes de arquivo das fontes (contrato para Tasks 2-3): `Fonte — Regulamento-MT`, `Fonte — RISD-SE`, `Fonte — RI-AL`, `Fonte — NO-03-AL`, `Fonte — NO-04-AL`, `Fonte — NO-06-AL`, `Fonte — NO-07-AL`, `Fonte — NO-11-Canil-AL`, `Fonte — NO-01-BA`, `Fonte — RI-DF`, `Fonte — NGA-ES`, `Fonte — Regimento-GO`, `Fonte — Minuta-RI-PA`, `Fonte — Atribuicoes-PR`, `Fonte — RISG-Exercito`, `Fonte — Regulamento-RN`, `Fonte — INOp-RR`, `Fonte — RI-RS`, `Fonte — Diretriz-TO`.

- [ ] **Step 1: Extrair o mapa fonte→temas do JSON** (para preencher as notas com dados reais):

```bash
python3 - <<'EOF'
import json
d=json.load(open('/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/database/regulamento_structure.json'))
srcs={}
for ch in d['chapters']:
    p=ch.get('primary',{})
    srcs.setdefault(p.get('uf'),{'name':p.get('name'),'doc':p.get('docLabel'),'prim':set(),'alt':set()})['prim'].add(ch['themeKey'])
    for uf,alt in (ch.get('alternatives') or {}).items():
        srcs.setdefault(uf,{'name':alt.get('name'),'doc':alt.get('docLabel'),'prim':set(),'alt':set()})['alt'].add(ch['themeKey'])
for uf,v in sorted(srcs.items()):
    print(uf,'|',v['name'],'|',v['doc'],'| primária em:',sorted(v['prim']),'| alternativa em:',sorted(v['alt']))
EOF
```

Mapa slug↔chave do JSON: `mt`→Regulamento-MT, `se`→RISD-SE, `al`→RI-AL, `al_no03`→NO-03-AL, `al_no04`→NO-04-AL, `al_no06`→NO-06-AL, `al_no07`→NO-07-AL, `al_no11`→NO-11-Canil-AL, `ba`→NO-01-BA, `df`→RI-DF, `es`→NGA-ES, `go`→Regimento-GO, `pa`→Minuta-RI-PA, `pr`→Atribuicoes-PR, `risg`→RISG-Exercito, `rn`→Regulamento-RN, `rr`→INOp-RR, `rs`→RI-RS, `to`→Diretriz-TO.

- [ ] **Step 2: Criar as 19 notas de Fonte** com este template (preencher com a saída do Step 1; contexto adicional do CLAUDE.md do repo, seções "Regulamento Geral em 2 Partes" e "Curadoria"):

```markdown
---
tags: [cbmro, regulamento, curadoria, fonte]
type: fonte
uf: <uf>
jsonKey: <chave no JSON, ex. al_no03>
---

# Fonte — <slug>

**Documento:** <docLabel do JSON> · **Ente:** <name>
**O que é:** <1-2 frases: natureza do documento e o que cobre — sem inventar; se só o docLabel for conhecido, dizer isso>

## Papel na minuta do CBMRO
- Fonte **primária** dos temas: <lista de wikilinks [[Tema — <themeKey>]] ou "nenhum">
- Fonte **alternativa** nos temas: <lista de wikilinks ou "nenhum">

## Observações de curadoria
- <notas conhecidas: ex. RISG só entra como alternativa, nunca primária (testado); PA é MINUTA em tramitação; PR é portal oficial, não norma>
```

Regra: os wikilinks `[[Tema — <themeKey>]]` usam o themeKey literal (ex.: `[[Tema — servico-operacional]]`) — só o do piloto existirá por ora; os demais ficam como links pendentes (ok no Obsidian, viram cinza).

- [ ] **Step 3: Criar `_Índice — Curadoria do Regulamento.md`:**

```markdown
---
tags: [cbmro, regulamento, curadoria, indice]
type: indice
---

# Curadoria do Regulamento Geral — Índice

> Mesa de decisão da redação final da minuta. As notas ORIENTAM; a fonte da verdade dos
> dados é o repositório (`database/regulamento_structure.json`). Semeado em 2026-07-21 a
> partir do JSON verificado — depois disso, as notas são editadas à mão (nada regenera).

Legenda: 🟢 decidido · 🟡 em curadoria · ⚪ não iniciado

## PARTE I — GERAL (12 temas)
| Tema | Status |
|---|---|
| [[Tema — disposicoes-preliminares]] | ⚪ |
| [[Tema — organizacao-geral]] | ⚪ |
| [[Tema — competencias-direcao]] | ⚪ |
| [[Tema — competencias-apoio-assessoramento]] | ⚪ |
| [[Tema — competencias-execucao]] | ⚪ |
| [[Tema — pessoal-quadros]] | ⚪ |
| [[Tema — ensino-instrucao]] | ⚪ |
| [[Tema — cerimonial-honras]] | ⚪ |
| [[Tema — disciplina-correicao]] | ⚪ |
| [[Tema — uniformes-apresentacao]] | ⚪ |
| [[Tema — seguranca-contra-incendio]] | ⚪ |
| [[Tema — disposicoes-finais]] | ⚪ |

## PARTE II — DO SERVIÇO (4 temas)
| Tema | Status |
|---|---|
| [[Tema — servico-operacional]] | 🟡 (piloto) |
| [[Tema — servico-interno-dia]] | ⚪ |
| [[Tema — atribuicoes-funcoes]] | ⚪ |
| [[Tema — central-operacoes-193]] | ⚪ |

## Fontes
[[Fonte — Regulamento-MT]] · [[Fonte — RISD-SE]] · [[Fonte — RI-AL]] · [[Fonte — NO-03-AL]] · [[Fonte — NO-04-AL]] · [[Fonte — NO-06-AL]] · [[Fonte — NO-07-AL]] · [[Fonte — NO-11-Canil-AL]] · [[Fonte — NO-01-BA]] · [[Fonte — RI-DF]] · [[Fonte — NGA-ES]] · [[Fonte — Regimento-GO]] · [[Fonte — Minuta-RI-PA]] · [[Fonte — Atribuicoes-PR]] · [[Fonte — RISG-Exercito]] · [[Fonte — Regulamento-RN]] · [[Fonte — INOp-RR]] · [[Fonte — RI-RS]] · [[Fonte — Diretriz-TO]]

## Notas relacionadas
- [[Diário de Construção da Minuta — rumo à apresentação ao Comando]]
- [[Comparativo RISG × Regulamentos — Round 2 (verificado na fonte)]]
```

ATENÇÃO: antes de gravar a tabela, confira os 16 `themeKey` reais com:
`python3 -c "import json;print([c['themeKey'] for c in json.load(open('/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/database/regulamento_structure.json'))['chapters']])"`
— se algum nome da tabela acima divergir do JSON, o JSON vence (corrija a tabela, não invente).

- [ ] **Step 4: Verificar** — listar a pasta (20 arquivos: índice + 19 fontes); conferir que cada nota de fonte tem `jsonKey` válido e pelo menos 1 wikilink de tema; nenhum excerto legal foi citado nesta task (fontes não citam artigos).

### Task 2: Nota do Tema `servico-operacional`

**Files:**
- Create (no vault, mesma pasta): `Tema — servico-operacional.md`
- Create (scratch, NÃO no vault): análise auxiliar em arquivo temporário do implementador

**Interfaces:**
- Consumes: nomes `Fonte — <slug>` da Task 1.
- Produces: `Tema — servico-operacional.md` + LISTA DE DIVERGÊNCIAS (seção "Decisões a tomar" da nota) que a Task 3 transforma em notas de decisão. Cada item da lista: assunto curto + estados envolvidos + natureza da divergência.

- [ ] **Step 1: Extrair o material do tema** (primária SE: 70 artigos; alternativas go=12, ba=1, rr=11, to=3, al_no03=5, es=7, al_no11=5 excertos):

```bash
python3 - <<'EOF'
import json
d=json.load(open('/Users/wandriobandeira/Projetos de dev Sistemas/05. Comparativo-de-cargos-e-funcoes/database/regulamento_structure.json'))
ch=[c for c in d['chapters'] if c['themeKey']=='servico-operacional'][0]
out={'primary':ch['primary'],'articles':ch['articles'],'alternatives':ch.get('alternatives')}
open('/tmp/servico-operacional.json','w').write(json.dumps(out,ensure_ascii=False,indent=1))
print('ok', len(ch['articles']), 'artigos primários')
EOF
```

(Se o diretório scratch da sessão existir, gravar lá em vez de /tmp.)

- [ ] **Step 2: Ler e analisar o material** (ler o arquivo extraído; se longo, por partes). Produzir a análise: (a) grandes assuntos do tema (ex.: escala/carga horária, concepção do serviço operacional, prontidão, guarnições, canil/BREC, salvamento aquático — os assuntos REAIS saem da leitura, não desta lista de exemplo); (b) para cada assunto, quais fontes tratam e onde DIVERGEM de verdade (regras conflitantes, números diferentes, conceitos incompatíveis — divergência real, não redação diferente para a mesma regra).

- [ ] **Step 3: Escrever `Tema — servico-operacional.md`:**

```markdown
---
tags: [cbmro, regulamento, curadoria, tema]
type: tema
themeKey: servico-operacional
parte: servico
status: em-curadoria
---

# Tema — servico-operacional (Parte II — Do Serviço)

**Capítulo na minuta:** <chapterTitle do JSON> · **Primária:** [[Fonte — RISD-SE]] (70 artigos)
**Alternativas:** [[Fonte — Regimento-GO]] (12) · [[Fonte — INOp-RR]] (11) · [[Fonte — NGA-ES]] (7) · [[Fonte — NO-03-AL]] (5) · [[Fonte — NO-11-Canil-AL]] (5) · [[Fonte — Diretriz-TO]] (3) · [[Fonte — NO-01-BA]] (1)

## Cobertura por assunto
| Assunto | SE (primária) | Também tratam | Observação |
|---|---|---|---|
| <assunto 1> | Art. N-M | GO, RR | <1 linha> |
| ... | | | |

## Decisões a tomar (divergências reais)
- [[Decisão — servico-operacional — <assunto>]]: <estados envolvidos — natureza da divergência em 1 linha>
- ...

## Lacunas
- <matéria que nenhuma/só 1 fonte cobre, se houver>

## Ligações
[[_Índice — Curadoria do Regulamento]] · [[Diário de Construção da Minuta — rumo à apresentação ao Comando]]
```

Regras: a tabela de cobertura referencia artigos por número (`Art. N`), sem colar o texto integral (o portal já mostra); a nota deve responder em 1 tela quem cobre o quê, onde divergem, o que falta. Se um assunto NÃO tem divergência real, ele aparece na cobertura mas NÃO em "Decisões a tomar".

- [ ] **Step 4: Verificar** — cada linha de "Decisões a tomar" nomeia estados e a divergência; números de artigo citados existem no JSON (conferir por amostragem com python); wikilinks apontam para nomes exatos da Task 1.

### Task 3: Notas de Decisão do piloto

**Files:**
- Create (no vault): uma `Decisão — servico-operacional — <assunto>.md` por item listado em "Decisões a tomar" da Task 2 (quantidade vem da análise — pode ser 2, pode ser 8; zero itens = task vira no-op e reporta isso).

**Interfaces:**
- Consumes: lista "Decisões a tomar" de `Tema — servico-operacional.md` (nomes EXATOS das notas); excertos verbatim de `/tmp/servico-operacional.json` (ou scratch) da Task 2.
- Produces: notas de decisão prontas para o Wândrio preencher "## Decisão CBMRO".

- [ ] **Step 1: Para cada item da lista, criar a nota:**

```markdown
---
tags: [cbmro, regulamento, curadoria, decisao]
type: decisao
themeKey: servico-operacional
decidido: false
---

# Decisão — servico-operacional — <assunto>

**Questão:** <a pergunta a decidir, em 1-2 frases claras, linguagem de gestor>

## Redações candidatas
### <Estado 1> — <docLabel>
> <texto VERBATIM do JSON>

`cf. <campo source do excerto>`
**Leitura:** <1-2 linhas: o que essa redação implica na prática>

### <Estado 2> — <docLabel>
> <texto VERBATIM>

`cf. <source>`
**Leitura:** <...>

## Comparação
- <2-4 bullets: onde as candidatas conflitam; consequência prática de cada escolha para o CBMRO>

## Decisão CBMRO
_(a preencher pelo Wândrio — redação escolhida/adaptada e o porquê)_

## Ligações
[[Tema — servico-operacional]] · [[Fonte — <slug do estado 1>]] · [[Fonte — <slug do estado 2>]]
```

Regras: excertos SEMPRE verbatim (copiar do JSON extraído, sem "limpar" defeitos da fonte); "Leitura" e "Comparação" são análise sua, claramente separadas do texto legal; a seção "Decisão CBMRO" nasce vazia com o placeholder em itálico.

- [ ] **Step 2: Verificação verbatim por amostragem** — para 2 excertos de cada nota (ou todos, se poucos), conferir com python que o texto citado existe caractere a caractere no JSON:

```bash
python3 - <<'EOF'
import json,sys
d=json.load(open('/tmp/servico-operacional.json'))
trecho="<primeiras ~80 chars do excerto citado na nota>"
blob=json.dumps(d,ensure_ascii=False)
print('OK' if trecho in blob else 'FALHOU: excerto não é verbatim')
EOF
```

Toda amostra deve imprimir OK. FALHOU = corrigir a nota (nunca o JSON).

- [ ] **Step 3: Conferir simetria** — cada nota de decisão criada está listada no "Decisões a tomar" do tema, e vice-versa (mesmos nomes exatos).

### Task 4: Diário + fechamento

**Files:**
- Modify (vault): `Codebases/Comparativo-de-cargos-e-funcoes/Diário de Construção da Minuta — rumo à apresentação ao Comando.md`

**Interfaces:**
- Consumes: contagens finais das Tasks 1-3 (nº de fontes, nº de decisões criadas).

- [ ] **Step 1: Acrescentar linha à tabela "Linha do tempo"** do Diário (não reescrever nada existente):

```markdown
| 2026-07-21 | Fase 3 iniciada — curadoria no Obsidian: repositório conectado semeado (índice + 19 fontes + tema-piloto servico-operacional com N notas de decisão); vault vira a mesa de decisão da redação final, JSON segue fonte da verdade | spec `docs/superpowers/specs/2026-07-21-regulamento-fase3-curadoria-obsidian-design.md` |
```

(Substituir N pela contagem real da Task 3.)

- [ ] **Step 2: Acrescentar em "Material visual para a apresentação"** o item:

```markdown
- [ ] Print do grafo do Obsidian (Regulamento — Curadoria) mostrando as legislações conectadas.
```

- [ ] **Step 3: Verificação final da fase** — no vault: `ls` da pasta (20 + 1 tema + N decisões); abrir 1 nota de cada tipo e conferir wikilinks resolvendo (sem typo nos nomes); reportar contagens ao controlador.
