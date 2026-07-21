# Fase 2A — Preencher o 16º tema (Central de Operações 193) — Design

**Data:** 2026-07-21
**Autor:** Wândrio + Claude
**Status:** spec para revisão (pré-implementação)
**Contexto:** primeira fatia da Fase 2 do projeto "Regulamento Geral em 2 Partes"
(spec-mãe: `2026-07-21-regulamento-geral-2-partes-design.md`; Fase 1 concluída no PR #15).

## 1. Problema e objetivo

Na Fase 1, o 16º tema `central-operacoes-193` ("Da Central de Operações e do Teledespacho")
foi criado VAZIO — aparece na tela com o marcador `⏳` (pendente). Esta fatia o **preenche**
com texto verbatim das fontes que tratam da central de emergência 193, usando o pipeline de
curadoria já existente (`extrair_regulamentos.py` → `regulamento_enrichment_<uf>.py`).

**Objetivo:** o tema `central-operacoes-193` deixa de ser pendente e passa a exibir artigos
verbatim sobre teledespacho/atendimento, com a Bahia como fonte primária e Roraima/Tocantins
como alternativas.

**Não-objetivos (YAGNI):**
- NÃO curar o resto dos Regulamentos de Serviço de BA/RR/TO — isso é a Fatia B. Aqui entram
  SÓ os artigos de teledespacho/atendimento dessas fontes.
- NÃO criar a "grade de acionamento / mapa de força" como conteúdo (decisão de escopo: tema
  enxuto, só teledespacho).
- NÃO incluir a estrutura física do COB/CIODES como órgão (isso seria matéria da Parte I).
- NÃO tocar em nenhum tema já existente nem nos 410 artigos da Fase 1.

## 2. Decisões já validadas pelo Wândrio (brainstorming 2026-07-21)

1. Fatiar a Fase 2; começar pela Fatia A (preencher o 16º tema).
2. Escopo do tema: **só teledespacho/atendimento** (atendente 193, despachante, operador de
   rádio, supervisor/operador de teledespacho, regulação da ocorrência). Sem grade de
   acionamento, sem estrutura física da central.
3. Fonte primária: **Bahia — CICOM** (a mais rica e articulada em teledespacho: 48 menções,
   funções próprias de Supervisor e Operador de Teledespacho). Alternativas: RR (COCB), TO
   (SIOP/COCB).
4. Validação: **confiar na extração determinística + verificação verbatim** (sem gate manual
   de de-para antes da extração). A garantia de integridade é o `verificar_verbatim.py`: todo
   caput deve existir literalmente na fonte.

## 3. Arquitetura da solução

Reusa o pipeline de curadoria existente (nada de mecanismo novo):

### 3.1 Identificação dos artigos (leitura de fonte)
Um subagente lê os markdowns de BA, RR e TO
(`database/markdown/{Bahia,Roraíma,Tocantins} - Regulamento de Serviço.md`) e identifica os
NÚMEROS de artigo que tratam de teledespacho/atendimento 193 (funções e rotina da central).
Todos os três são articulados por "Art. N" (BA 35, RR 97, TO 32 artigos), então a extração
determinística por faixa funciona. Entrega: a lista de faixas `(início, fim, heading)` por UF.

### 3.2 CONFIG do extrator (`scripts/extrair_regulamentos.py`)
Adicionar três entradas ao dict `CONFIG`, no mesmo formato das existentes (`mt`/`se`/`go`):
```python
'ba': {
    'md': 'Bahia - Regulamento de Serviço.md',
    'src': 'cf. CBMBA, Norma Operacional nº 01/2021, Art. {n}',
    'slice_between': (<abertura>, <fecho>),   # definidos na leitura
    'strip_lines': [<regex de ruído de layout>],  # BA tem cabeçalho repetido
    'ranges': [ (<ini>, <fim>, 'central-operacoes-193', 'exata', '<heading>') ],
    'overrides': {},
},
# idem 'rr' (Roraíma - Regulamento de Serviço.md) e 'to' (Tocantins - Regulamento de Serviço.md)
```
As `ranges` cobrem SÓ os artigos de teledespacho. Artigos fora das faixas não são extraídos
(ficam para a Fatia B).

### 3.3 Registro das UFs (`scripts/regulamento_enrichment.py`)
- Adicionar `ba`/`rr`/`to` à lista de UFs que o mestre auto-importa (bloco ~linha 124).
- Adicionar `ba`/`rr`/`to` a `REGULAMENTO_DOCS` (label + md) e ao `STATE_NAMES` do builder.
- `PRIMARY_SOURCE['central-operacoes-193']`: mudar de `'to'` (provisório da Fase 1) → `'ba'`.

### 3.4 Extração e verificação
```
.venv-pipeline/bin/python scripts/extrair_regulamentos.py ba rr to   # gera os _enrichment_ba/rr/to.py
.venv-pipeline/bin/python scripts/verificar_verbatim.py               # todo caput existe literal na fonte
```

### 3.5 Rebuild
```
.venv-pipeline/bin/python scripts/build_regulamento_structure.py          # tema deixa de ser pendente
.venv-pipeline/bin/python scripts/build_regulamento_structure_atual.py    # espelho do atual herda
```

## 4. Tratamento de erros e casos-limite
- **Verbatim quebrado**: se `verificar_verbatim.py` acusar um caput que não existe literal na
  fonte, o artigo é corrigido (faixa/`strip_lines`) ou removido — nunca ajustado à mão no
  arquivo gerado (que traz aviso "NÃO editar à mão"). Reportar, não silenciar.
- **Ruído de layout (BA/TO)**: usar `strip_lines` no CONFIG, como já feito para SE.
- **Nenhum artigo de teledespacho numa fonte**: se RR ou TO não tiver artigo isolável de
  teledespacho (o 193 pode estar difuso dentro de "Oficial de Comunicação"), essa UF entra só
  com o(s) artigo(s) que existir(em), ou fica de fora do tema — sinalizar, não forçar.
- **Marcador de cenário atual**: o espelho `reg:atual:` é herdado pelo gerador do atual, que
  re-carimba os ids — sem ação manual.

## 5. Testes
- `scripts/test_regulamento_structure.py`:
  - Remover `central-operacoes-193` da allowlist `PENDENTES_OK`.
  - Passar a exigir: o capítulo `central-operacoes-193` tem `articles` não-vazio, `parte ==
    'servico'`, e `primary.uf == 'ba'`.
  - Manter a invariante de preservação (≥ 410 artigos; agora o total sobe com os novos).
- `verificar_verbatim.py` verde para os caputs novos.
- `node --test` continua verde (nenhuma mudança JS nesta fatia).

## 6. Escopo quantificado (lei)
- Tema preenchido: `central-operacoes-193` (era 0 artigos → passa a N>0, só teledespacho).
- Fontes novas parcialmente curadas: BA (primária), RR, TO (só as faixas de teledespacho).
- Artigos pré-existentes preservados: 410 (nenhum tocado).

## 7. Riscos
- **193 difuso na fonte**: em RR/TO o teledespacho pode não estar num artigo próprio, e sim
  dentro das atribuições do Oficial de Comunicação/Coordenador. Mitigação: a leitura de fonte
  (3.1) decide o que é isolável; o que não for, não entra (sinalizado).
- **Fonte primária fraca**: se a leitura mostrar que a BA, na verdade, trata teledespacho de
  forma menos articulada que o previsto, reavaliar a primária (RR/TO) — decisão de curadoria a
  sinalizar, não a esconder.
