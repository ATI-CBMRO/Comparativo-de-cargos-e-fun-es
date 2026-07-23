# Cockpit de curadoria — Fase 2: aba "Decisões" (leitura) — Design

**Data:** 2026-07-23
**Status:** aprovado (brainstorming com o Wândrio, 2026-07-23)
**Fase anterior:** Fase 1 — Conferência linear (`2026-07-22-cockpit-curadoria-conferencia-decisoes-design.md`), concluída e mesclada (PR #19).
**Fase seguinte:** Fase 3 — registrar/aplicar decisão (plano próprio, depois).

## Objetivo

Trazer as **36 Decisões CBMRO** (material de curadoria hoje só no vault Obsidian) para dentro
do portal, como uma **página de LEITURA**: o Wândrio lê, dispositivo temático a dispositivo,
a Questão + as redações candidatas verbatim das leis de outros estados + a comparação + a
decisão já tomada (quando houver), sem sair do sistema. É a base de conhecimento sobre a qual
a Fase 3 permitirá registrar/aplicar a decisão.

**Esta fase é SÓ leitura.** Registrar decisão pelo sistema, pular da decisão para o
dispositivo da minuta, e a distinção redação×estrutural ficam para a Fase 3.

## Contexto descoberto (2026-07-23)

As 36 notas existem no vault e **já trazem todo o material de curadoria**; o que está em
branco é o campo final `## Decisão CBMRO` na maioria delas. Localização:

```
~/Documents/Obsidian Vault/Codebases/Comparativo-de-cargos-e-funcoes/
  ├─ Regimento Interno — Curadoria/   → 9 notas "Decisão — ri — <organKey> — <slug>.md"
  └─ Regulamento — Curadoria/          → 27 notas "Decisão — <themeKey> — <slug>.md"
```

As duas famílias seguem **o mesmo esqueleto** (um parser só serve as duas):

```markdown
---
type: decisao
organKey: dlog        # OU  themeKey: servico-operacional
decidido: false
---
# Decisão — ...
**Questão:** <1 parágrafo>
## Redações candidatas
### <Fonte legível>
> <verbatim, 1+ linhas em blockquote>
`cf. <citação>`
*(nota opcional de ruído de OCR)*
**Leitura:** <comentário do curador>
### <outra Fonte> ...
## Comparação
- <bullet> ...
## Decisão CBMRO
_(a preencher pelo Wândrio — ...)_   # placeholder itálico quando não decidida
## Ligações
[[Órgão — dlog]] · [[Fonte — RI-PR]] · ...
```

Chave de junção: `organKey` → capítulo `organ:<key>`; `themeKey` → capítulo `reg:<key>`
(o `chapterId` é derivado no pipeline; usado só como metadado nesta fase, ativado na Fase 3).

## Decisões de produto (aprovadas)

1. **Onde mora:** página própria "Decisões" no menu, uma por trilha
   (`/minuta/decisoes` = Regimento; `/regulamento/decisoes` = Regulamento). Separa a leitura
   densa das decisões da conferência rápida dispositivo a dispositivo.
2. **Cenário:** as **mesmas 36** nos dois cenários (atual e futura). São referência de como
   outros estados resolveram cada ponto — não texto do RO. O JSON é **compartilhado** (lido da
   raiz `database/`, não da gaveta `database/atual/`), como `states_data.json`. Sem
   `TrilhaRoute` — a página funciona nos dois cenários, igual à Conferência.
3. **Densidade:** cartões **recolhidos**; o verbatim longo e a Leitura de cada candidata
   abrem ao clicar. Questão + fontes candidatas (título) sempre visíveis.

## Arquitetura

O mesmo padrão de todos os pipelines: script Python offline lê o vault (fora do repo) e gera
**um** JSON commitado; o frontend só consome o JSON. O vault não é servido ao navegador — esta
é a única via.

```
Vault (.md, 36 notas)  →  scripts/build_decisoes_curadoria.py  →  database/decisoes_curadoria.json  →  DecisoesCuradoria.jsx
```

### Componente 1 — `scripts/build_decisoes_curadoria.py`

Responsabilidade: localizar as notas, parsear, reconciliar contagens, gravar o JSON.

- **Caminho do vault:** constante `VAULT_CURADORIA` com o default descoberto
  (`~/Documents/Obsidian Vault/Codebases/Comparativo-de-cargos-e-funcoes`), sobreponível por
  variável de ambiente `VAULT_CURADORIA`. Se a pasta (ou uma das duas subpastas) não existir,
  **erro claro e saída não-zero** — nunca grava JSON vazio em silêncio.
- **Descoberta:** lê `Regimento Interno — Curadoria/Decisão — *.md` (trilha `ri`) e
  `Regulamento — Curadoria/Decisão — *.md` (trilha `reg`). Ignora `Fonte — *`, `Tema — *`,
  `Órgão — *`, `_Índice — *`.
- **Parser** (`parse_decisao(texto, arquivo, trilha) -> dict`), puro, testável:
  - frontmatter: `organKey`|`themeKey`, `decidido` (bool);
  - `titulo` (linha `# `), `questao` (parágrafo após `**Questão:**`);
  - `candidatas`: lista, uma por `### `, com `{ fonte, verbatim: [linhas], citacao, ocr, leitura }`
    (`verbatim` = linhas do(s) blockquote(s) sem o `> `; `citacao` = linha `` `cf. …` ``;
    `ocr` = texto da nota itálica `*(…OCR…)*` quando presente, senão `null`;
    `leitura` = texto após `**Leitura:**`);
  - `comparacao`: bullets da seção `## Comparação`;
  - `ligadas`: nomes dos wikilinks `[[…]]` da seção `## Ligações`;
  - `decidido` (do frontmatter) + `decisao`: texto sob `## Decisão CBMRO` **apenas se não for o
    placeholder itálico** `_(…)_`; caso contrário `null`;
  - `chapterId`: `organ:<organKey>` (ri) ou `reg:<themeKey>` (reg);
  - `id`: slug estável = nome do arquivo sem extensão.
- **Reconciliação:** imprime `notas em disco = N, parseadas = N` por trilha (falha se diferir);
  por nota, imprime nº de candidatas. Grava no JSON um bloco `reconciliacao` com as contagens.
- **Verbatim fiel:** blockquotes reproduzidos exatamente como na nota, defeitos de OCR
  preservados (a nota já os sinaliza no campo `ocr`).

**Formato de `database/decisoes_curadoria.json`:**

```json
{
  "generated_by": "scripts/build_decisoes_curadoria.py",
  "reconciliacao": { "ri": {"disco": 9, "parseadas": 9}, "reg": {"disco": 27, "parseadas": 27} },
  "decisoes": [
    {
      "id": "Decisão — ri — dlog — fusao-logistica-financas",
      "trilha": "ri",
      "key": "dlog",
      "chapterId": "organ:dlog",
      "titulo": "Decisão — ri — dlog — fusao-logistica-financas",
      "questao": "A minuta do RO trata Logística …",
      "candidatas": [
        {
          "fonte": "Paraná — Lei nº 22.206/2024 (fusão logística + finanças)",
          "verbatim": ["A Diretoria de Apoio Logístico e Finanças é o órgão …", "I - …"],
          "citacao": "cf. CBMPR, Lei nº 22.206/2024, Art. 29",
          "ocr": null,
          "leitura": "os 4 incisos do PR misturam …"
        }
      ],
      "comparacao": ["DF e PA convergem entre si …", "PR diverge …"],
      "ligadas": ["Órgão — dlog", "Órgão — dpof", "Fonte — RI-PR"],
      "decidido": false,
      "decisao": null
    }
  ]
}
```

### Componente 2 — `src/lib/decisoes.js` (lógica pura, testável)

- `filtrarDecisoes(decisoes, filtro)` — `filtro` ∈ `'todas'|'pendentes'|'decididas'`;
  pendentes = `!decidido`, decididas = `decidido`.
- `contarDecisoes(decisoes)` → `{ total, decididas, pendentes }`.
- `decisoesDaTrilha(dados, trilha)` → filtra `decisoes` por `trilha`.

### Componente 3 — `src/pages/DecisoesCuradoria.jsx` (prop `trilha: 'ri'|'reg'`)

- Carrega `database/decisoes_curadoria.json` (raiz, via `fetchJson('/database/decisoes_curadoria.json')`
  — **não** `scenarioDbUrl`, arquivo é compartilhado). Erro/loading via `Status.jsx`.
- Barra de seção "Decisões — {Regimento Interno|Regulamento Geral}", contador
  `decididas / total`, e filtro Todas / Pendentes / Decididas (estado local).
- Lista de cartões (`DecisaoCard`): título + Questão sempre visíveis; selo **Decidida ✓ /
  Pendente ⚠**; para cada candidata, cabeçalho (fonte + citação) clicável que expande o
  **verbatim** (estilizado com as classes `rg-*`/`renderFriendlyText` reusadas da Conferência)
  + nota de OCR + **Leitura**; seção Comparação recolhível; decisão exibida só se `decidido`.
  Estado de expansão local por cartão/candidata.
- Sem persistência (leitura pura). Sem dependência de cenário.

### Componente 4 — Rotas + menu (`src/App.jsx`)

- Import de `DecisoesCuradoria`; rotas `/minuta/decisoes` (`trilha="ri"`) e
  `/regulamento/decisoes` (`trilha="reg"`), **sem** `TrilhaRoute` (padrão da Conferência).
- Duas entradas em `NAV_GROUPS`: uma no bloco Regimento Interno, uma no Regulamento Geral,
  rótulo "Decisões", após "Conferência".

## Tratamento de erro

- Vault ausente/subpasta faltando → script falha com mensagem e saída não-zero.
- Contagem disco≠parseadas → script falha (não grava JSON parcial).
- Nota sem `organKey`/`themeKey` ou sem `## Questão` → script falha nomeando o arquivo
  (buraco não passa em silêncio).
- Frontend: JSON ausente → `ErrorState` com dica de rodar o script (padrão da Conferência).

## Testes

- `scripts/test_decisoes_curadoria.py` — `parse_decisao` contra fixture (uma nota `ri` com
  candidata+OCR e uma `reg`): valida título, questão, nº de candidatas, verbatim, `decidido`,
  `chapterId`, e que o placeholder itálico vira `decisao: null`.
- `src/lib/decisoes.test.js` — `filtrarDecisoes`/`contarDecisoes`/`decisoesDaTrilha`.

## Fora de escopo (Fase 3)

Registrar decisão pelo sistema (Firebase + overlay `finalText` para redação / ficha de
aplicação para estrutural); pular da decisão para o dispositivo (join por `chapterId`);
distinção redação×estrutural; "Divergente" da Conferência virar pendência.

## Varreduras AR-01 (auditoria — reexecutar nesta fase)

Antes de fechar a fase, rodar as 3 varreduras do `docs/superpowers/auditoria-armadilhas.md`.
Ponto de atenção específico desta fase: o `chapterId` derivado (`organ:<organKey>` /
`reg:<themeKey>`) é casamento por chave — conferir que cada `organKey`/`themeKey` das notas
existe de fato como capítulo na estrutura correspondente, sem casar por semelhança de nome.
