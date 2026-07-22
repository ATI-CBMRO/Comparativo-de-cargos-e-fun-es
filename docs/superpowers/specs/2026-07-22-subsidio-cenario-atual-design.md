# Subsídio no cenário LOB atual — Design

**Data:** 2026-07-22 · **Aprovado por:** Wândrio (brainstorm nesta data)
**Objetivo:** destravar `/minuta/subsidio` e `/regulamento/subsidio` no cenário **LOB
atual** (hoje mostram "Em construção" via `TrilhaRoute`), gerando o comparativo do
atual **sem vazar enriquecimento da LOB futura**.

## Decisões de produto (do brainstorm)

1. **Qualidade do comparativo RI do atual: automático rotulado.** Sem curadoria manual
   de de-para nesta fatia. O casamento é por palavra-chave (mesma mecânica da camada
   `automatico` da futura), e a tela exibe SEMPRE um selo/aviso visível:
   **"correspondência automática — sujeita a revisão"** quando o cenário é o atual.
   Curadoria fina fica para rodada futura, se o Wândrio sentir falta.
2. **Lado Regulamento é só ligação de dados:** `database/atual/regulamento_structure.json`
   já existe (herdado com `alternatives`); a tela passa a resolver o endereço pela chave
   de cenário. Nenhum gerador novo desse lado.
3. **Cenário futura intocado:** mesmas telas, mesmos dados, mesmo visual (prova por
   diff + screenshot lado a lado).
4. Onde o casamento automático não encontrar nada para um capítulo, a tela diz isso
   claramente (estado vazio), nunca esconde a lacuna.

## Arquitetura

### Gerador novo (isolado — padrão dos geradores do atual)

`scripts/build_minuta_comparison_atual.py` → `database/atual/comparativo_minuta.json`.

- **NÃO importa** `minuta_enrichment`, `lob_enrichment`, `build_minuta_structure`
  (ORGAN_ORDER da futura) nem `build_minuta_comparison` — a armadilha documentada no
  CLAUDE.md ("vaza CBMMT/PA/DF") fica estruturalmente impossível: isolamento por
  arquivo, não por `if`.
- Reusa apenas a lib neutra `scripts/minuta_comparison_lib.py` (`norm`) e utilitários
  de leitura próprios.
- **Referência (coluna RO):** os 21 órgãos de `database/atual/organs_detail/ro.json`
  (chaves: cg, emg, corregedoria, ajudancia, gabinete, cepdec, condeg, dint, cpof,
  assessorias, comissoes, dp, deei, cat, dlog, dcs, dinf, cob1, cob2, coa, gbs), na
  ORDEM dos capítulos de `database/atual/minuta_structure.json` (`atual:organ:<key>`).
- **Camada única `automatico`:** tabela própria `AUTO_MATCH_KEYWORDS_ATUAL` (21
  chaves do atual; a tabela da lib usa as chaves da futura e não serve aqui) +
  matcher local que reusa `norm`. Estados vêm de `database/organs_detail/<id>.json`
  (acervo compartilhado dos 27 — pode ler; é compartilhado por design). Estrutura de
  cada registro de estado espelha o formato do comparativo da futura
  (`provenance: "automatico"`, `organs: [...]`), inclusive a separação
  `organs`/`lobOrgans`/`riOrgans` que o `MinutaComparator` consome (mesmo shape, para
  a tela não precisar de caminho de código novo):
  - `lobOrgans`: casamento sobre o subconjunto LOB do organs_detail (mesma regra
    `source=='lob'` → só esses; senão todos — copiar a regra, não importar).
  - `riOrgans`: casamento sobre o subconjunto não-LOB.
  - `organs` (visão mesclada histórica): casamento sobre os não-LOB (paridade com a
    futura, que exclui `source:lob` da coluna compilada).
- **Sem camada `curado`, sem Guarnição** (o atual não tem capítulo de guarnição).
- Metadados de topo: `{ scenario: "atual", generatedFrom: "Lei nº 2.204/2009", ... }`.

### Telas (resolver endereço pela chave de cenário)

Mecanismo já existente: `scenarioDbUrl(cenario, '<arquivo>')` de `src/lib/scenario.js`.

- `MinutaComparator.jsx`: `fetchJson(scenarioDbUrl(cenario, 'comparativo_minuta.json'))`
  (linha ~175). No cenário atual, exibir o aviso fixo "correspondência automática —
  sujeita a revisão" no topo do painel de estados.
- `RISubsidioComparativo.jsx`: os dois fetches (linhas ~94-95) passam por
  `scenarioDbUrl`; mesmo aviso no cenário atual.
- `RegulamentoComparator.jsx`: fetch (linha ~43) por `scenarioDbUrl` (sem aviso — os
  dados do Regulamento são curados/herdados, não automáticos).
- `App.jsx`: remover o `TrilhaRoute` APENAS das rotas `/minuta/subsidio` e
  `/regulamento/subsidio` (linhas 283 e 288). As demais rotas gated (`/comparar`,
  `/minuta/comparar`, `/minuta/comparativo-ri`, `/regulamento/comparar`,
  `/minuta/deliberacao`) continuam gated — fora do escopo.
- `RISubsidio.jsx` / `RegSubsidio.jsx` (cascas): sem mudança de estrutura; a aba LOB
  do RISubsidio traduz chapterId→organKey por `organKeyOfChapter` — verificar que
  funciona com ids `atual:organ:<key>` (se o prefixo `atual:` quebrar a tradução,
  normalizar no ponto de tradução, sem tocar a futura).

### Compatibilidade RISubsidioComparativo (aba RI)

A aba RI usa `minuta_structure.json` (do cenário) + `comparativo_minuta.json` (do
cenário) casados por `organKey`/chapterId. O gerador do atual DEVE usar as mesmas
chaves de órgão dos capítulos do `atual/minuta_structure.json` (sem o prefixo
`atual:organ:` no campo de chave do comparativo — usar a chave nua `<key>`, espelhando
a futura, e deixar a tela resolver como já resolve hoje).

## Fora de escopo (YAGNI)

- Curadoria manual de equivalências do atual (rodada futura, sob demanda).
- Destravar as rotas de compat gated (`/comparar` etc.) no atual.
- Guarnição/RISD no atual.
- Firebase/Revisão (já isolado por `atual:`; nada muda).

## Testes e prova

- **Testes do gerador** (python, padrão dos irmãos): 21 capítulos na ordem do
  `atual/minuta_structure.json`; `scenario=="atual"`; **nenhum rótulo de fonte da
  futura** no JSON (proibido: qualquer `cf. CBMMT/CBMPA/CBMDF` — o comparativo do
  atual não tem camada curada); toda `provenance` == `automatico`.
- **Suíte JS:** `node --test` intocada (114) + teste novo apenas se surgir lógica pura
  nova em `src/lib` (ex.: normalização de organKey do atual).
- **Prova real (obrigatória):** screenshots das 2 telas no cenário atual (com o selo
  visível) E das mesmas telas no cenário futura idênticas ao estado anterior; diff da
  branch provando que os arquivos da futura em `database/` não mudaram.

## Riscos e mitigação

- **Vazamento futura→atual:** mitigado por isolamento de arquivo + teste automatizado
  de rótulos proibidos.
- **Casamento automático fraco em órgãos sem nome óbvio (cob1/cob2, comissoes):**
  aceito pela decisão de produto nº 1 (selo + estado vazio honesto).
- **`organKeyOfChapter` com prefixo `atual:`:** verificado na implementação; correção
  localizada no ponto de tradução se necessário.
