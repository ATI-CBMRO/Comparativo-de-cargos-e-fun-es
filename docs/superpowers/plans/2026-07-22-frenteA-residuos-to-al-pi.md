# Frente A — Resíduos TO/AL/PI — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) ou superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Incorporar à base do Regulamento o corpo principal de Tocantins e os 4 DOBs de Alagoas (como alternativas), esclarecer a NO-02 e destravar a LOB do Piauí por OCR — com verificação verbatim e vault sincronizado.

**Architecture:** Reuso dos mecanismos existentes de `scripts/extrair_regulamentos.py`: `extract_line_slices()` (corte por linha absoluta — técnica do ES, resolve a colisão de numeração do TO) e um novo modo de corte POR SEÇÃO NUMERADA para os DOBs. Saída = novos arquivos `regulamento_enrichment_*.py` GERADOS + registro no mestre `regulamento_enrichment.py` → `build_regulamento_structure.py` regenera o JSON. OCR do PI via `ocrmypdf` em venv isolado.

**Tech Stack:** Python 3 (`.venv-pipeline/bin/python`), pypdf/ocrmypdf, `node --test` (suíte intocada deve passar).

## Global Constraints

- Spec: `docs/superpowers/specs/2026-07-22-regulamento-residuos-to-al-pi-design.md`.
- Verbatim absoluto: `verificar_verbatim.py` DEVE passar para todo excerto novo; defeitos de fonte reproduzidos.
- Fontes novas SÓ como alternativas; fonte primária de NENHUM tema muda; os 413 artigos primários intocados (número e texto). `test_regulamento_structure.py` deve continuar garantindo isso.
- Nada de pip no Python do sistema: usar `.venv-pipeline/bin/python`; para OCR, instalar `ocrmypdf` DENTRO de `.venv-pipeline` (ou venv novo `.venv-ocr/` se conflitar).
- JSON gerado não se edita à mão; edita-se gerador e regenera.
- Após regenerar: `node --test` completo verde; gerador do cenário atual (`build_regulamento_structure_atual.py`) reexecutado para herdar.
- Classificação de conteúdo por LEITURA (nunca por nome de arquivo).

---

### Task A1: Corpo principal de Tocantins (corte por linha absoluta)

**Files:** Modify: `scripts/extrair_regulamentos.py` (CONFIG['to'] ou novo bloco), `scripts/regulamento_enrichment.py` (registro). Regenerar: `scripts/regulamento_enrichment_to.py`, `database/regulamento_structure.json`.

- [ ] Ler `database/markdown/` do TO (Diretriz Geral) e mapear as LINHAS do corpo principal (Art. 1-13, 16) vs. o início do Anexo 2 (já usado). Cuidado: o Anexo 2 já alimenta `atribuicoes-funcoes` e `central-operacoes-193` — os excertos existentes NÃO mudam.
- [ ] Configurar o corte por linha absoluta (mecanismo `extract_line_slices`, precedente do ES em CONFIG) para o corpo principal; mapear cada artigo ao tema certo por leitura (provável: servico-operacional / servico-interno-dia).
- [ ] Regenerar enrichment TO + `build_regulamento_structure.py`; rodar `verificar_verbatim.py` (novo material 100%), `test_regulamento_structure.py`, `node --test`; conferir por diff de JSON que NENHUM excerto pré-existente mudou e que artigos primários = 413.
- [ ] Reexecutar `build_regulamento_structure_atual.py`. Commit.

### Task A2: DOBs 05-08 de Alagoas (extração por seção numerada)

**Files:** Modify: `scripts/extrair_regulamentos.py` (novo modo `extract_sections` p/ documentos "N TÍTULO"), `scripts/regulamento_enrichment.py`. Create (gerado): `scripts/regulamento_enrichment_al_dobs.py`. Regenerar JSON.

- [ ] Ler os 4 markdowns dos DOBs 05-08; confirmar a estrutura de seção numerada; escrever o modo de corte por seção (unidade = seção numerada; excerpt: `caput` = título+primeiro parágrafo? NÃO — manter fidelidade: `caput` = a primeira linha da seção como está, `dispositivos` = demais linhas/itens; `source` = `cf. CBMAL, <norma>, seção N`).
- [ ] Classificar cada DOB/seção ao tema certo por leitura (chaves novas `al_dob05..al_dob08`, name "Alagoas", docLabel com o nome real da norma).
- [ ] `verificar_verbatim.py` adaptado se necessário para as seções (todo texto citado existe literalmente no markdown); regenerar tudo; suítes verdes; primários intocados; gerador do atual reexecutado. Commit.

### Task A3: NO-02 de Alagoas + OCR do Piauí

**Files:** possivelmente `database/markdown/Alagoas - Norma Operacional 02.md` (reconvertido), `database/markdown/Piauí - Organização Básica (…).md` (reconvertido pós-OCR). Nenhum código novo além de comandos.

- [ ] NO-02: abrir o PDF correspondente em `LEGISLAÇÃO CBMS/` (via pypdf, contar páginas/caracteres); se a conversão perdeu texto, reconverter com `convert_to_markdown.py`; se a norma é curta mesmo, registrar a conclusão no relatório (com contagem de páginas) e NÃO mexer.
- [ ] PI: instalar `ocrmypdf` em venv (preferir `.venv-pipeline`; se conflitar, `.venv-ocr/`, fora do git); rodar OCR no PDF do PI gerando PDF pesquisável em arquivo TEMPORÁRIO (scratchpad) — NÃO sobrescrever o original sem backup: copiar o original para o scratchpad antes; depois decidir: gravar o OCRizado ao lado (mesmo nome + sufixo) ou substituir SÓ se o Wândrio já autorizou — como não autorizou substituição, gravar como novo arquivo `Piauí - Organização Básica (Lei 5.949-2009 alt. Lei 7.772-2022) [OCR].pdf` e reconverter o markdown a partir dele (o `.md` de destino substitui o de 604 bytes).
- [ ] Reconciliar: `.md` do PI com tamanho plausível de LOB (>20KB) e texto legível (amostrar artigos); rodar `build_states_data.py` na ordem do pipeline (org detail antes se necessário — para PI, `build_organs_detail` + `build_states_data`) e `node --test`. Commit.

### Task A4: Sincronizar o vault (fontes/temas/decisões afetados)

**Files (vault):** Create `Fonte — DOB-05-AL.md` … `Fonte — DOB-08-AL.md`; Modify `Fonte — Diretriz-TO.md`, notas de Tema afetadas (cobertura + possíveis novas decisões), `_Índice — Curadoria do Regulamento.md` (lista de fontes).

- [ ] A partir do `regulamento_structure.json` REGENERADO, atualizar as notas de tema afetadas (novas linhas de cobertura para o corpo do TO e DOBs); se o material novo criar divergência REAL nova com regra existente, criar `Decisão — <tema> — <assunto>.md` no formato padrão (verbatim + cf. + Decisão CBMRO vazia); senão, registrar como reforço/lacuna fechada.
- [ ] Criar as 4 notas de fonte dos DOBs (formato padrão) e atualizar a do TO (agora cobre corpo principal + Anexo 2); atualizar a lista de fontes no Índice.
- [ ] Verificação: varredura de wikilinks da pasta (0 quebrados); amostragem verbatim de qualquer excerto novo citado; contagens reportadas. Commit (só docs/repo; vault fora do git).
