# Comparativo de RI — Minuta CBMRO × RIs dos demais estados

**Data:** 2026-07-03
**Status:** Aprovado (design)

## Problema

Durante a revisão colaborativa da minuta de Regimento Interno (RI) do CBMRO
(`/minuta/revisao`), os coronéis do CONDEG carecem de um referencial externo:
não têm à mão como os demais estados regularam o mesmo órgão em seus próprios
Regimentos Internos. Precisamos de um comparativo capítulo a capítulo entre a
minuta do CBMRO e os RIs equivalentes de outros estados, para embasar as
sugestões de redação.

Nem todos os estados possuem RI. O comparativo deve, portanto, exibir apenas os
estados com dado curado de RI e sinalizar quando não há equivalente.

## Escopo

- **Página nova e separada** (`/minuta/comparativo-ri`), acessível pelo menu
  lateral, agrupada às demais páginas da minuta.
- **Somente leitura.** Não há edição, sugestão ou persistência — é uma tela de
  consulta/apoio à revisão.
- **Sem novo pipeline Python.** Reaproveita dados já gerados
  (`minuta_structure.json` e `comparativo_minuta.json`). Nenhum script novo,
  nenhuma regeneração.

### Fora de escopo
- Texto integral do capítulo do RI (extração de PDF). Exibimos as competências
  curadas do órgão, não o texto bruto do documento.
- Comparação simultânea de vários estados lado a lado. É uma comparação par a
  par: CBMRO fixo × um estado por vez.
- Qualquer alteração no fluxo de revisão/deliberação existente.

## Layout

Página de 3 zonas horizontais, espelhando o padrão visual de `/minuta/revisao`:

```
┌───────────────┬──────────────────────┬──────────────────────┐
│  ChapterRail  │   CBMRO (Minuta)     │  Estado selecionado  │
│  (210px)      │   capítulo atual     │  órgão equivalente   │
│  reusado      │   somente leitura    │                      │
│               │                      │  [AL][AM][DF][GO]... │
│  Cap. I       │  CAPÍTULO IV         │  ─────────────────   │
│  Cap. II      │  DO DPO              │  AL — Dir. Planej.   │
│  Cap. III     │                      │  I - planejar...     │
│  Cap. IV  ●   │  Art. 12. O DPO...   │  II - coordenar...   │
│  ...          │  I - planejar...     │                      │
│               │  II - organizar...   │  fonte: RI (curado)  │
└───────────────┴──────────────────────┴──────────────────────┘
```

- **Coluna 1 — ChapterRail** (`src/components/ChapterRail.jsx`, reusado sem
  alteração). Navega entre capítulos. Como não há contagem de sugestões nesta
  página, `counts` é passado como `{}` (badge sempre 0 — aceitável; a trilha
  serve só como índice de navegação).
- **Coluna 2 — CBMRO (Minuta).** Renderiza o capítulo selecionado da minuta em
  modo leitura: título do capítulo, e para cada artigo o título de seção (se
  houver), o caput em negrito e os incisos numerados em romano. Reusa a
  numeração de `buildArticles`/`articleLabel`/`romanize` (via `buildTargets`).
- **Coluna 3 — Estado selecionado.** No topo, pills dos estados com RI que têm
  dado para o capítulo atual. Abaixo, para o estado ativo: nome do órgão
  equivalente e suas atribuições (uma por parágrafo); se o estado tiver mais de
  um órgão mapeado (`stateEntry.organs[]` com múltiplos itens), cada um recebe
  um subtítulo. Rodapé com badge de proveniência (`curado` / `automático`) e o
  `sourceLabel`.

## Dados

Dois fetches na montagem, em paralelo:

1. `fetch('/database/minuta_structure.json')` → `buildTargets(structure)` →
   lista de capítulos (mesma função usada por `/minuta/revisao`, reusada sem
   modificação). Fornece a Coluna 2 e alimenta a ChapterRail.
2. `fetch('/database/comparativo_minuta.json')` → indexado em memória como
   `{ [organKey]: organEntry }` para lookup O(1). Fornece a Coluna 3.

### Mapeamento capítulo → dados do estado

```
chapter.organKey  →  compByKey[organKey]  →  organEntry.states[]
                                                    ↓  (filtra por state.id)
                                          stateEntry.organs[].atribuicoes[]
                                          stateEntry.provenance
                                          stateEntry.sourceLabel
```

- Capítulos com `kind: 'organ'` têm `organKey` (ex. `"dpo"`, `"cg"`) — são os
  27 capítulos comparáveis.
- Capítulos com `kind: 'prose'` ou `kind: 'articles'` (Disposições Preliminares,
  Estrutura Organizacional, Disposições Finais) **não** têm `organKey` — a
  Coluna 3 exibe aviso estático "Sem equivalente direto nos RIs analisados".

### Estados com RI

Lista fixa de 9 estados (os que possuem LOB + Regimento Interno, conforme
`CLAUDE.md`): `al, am, df, go, mt, pr, pa, rs, se`. Cobertura verificada no
`comparativo_minuta.json` (capítulos-órgão com atribuições não vazias): AL 21,
MT 21, PR 20, PA 20, GO 19, SE 18, DF 17, AM 16, RS 11 — de 27 capítulos-órgão.

### Regras de seleção de estado

- O seletor (pills) mostra apenas os estados com RI que **têm dado não vazio**
  para o capítulo atualmente selecionado. Estados sem dado para aquele capítulo
  não aparecem como pill.
- Ao entrar na página, seleciona-se o primeiro capítulo-órgão e o primeiro
  estado disponível para ele.
- Ao trocar de capítulo: se o estado atualmente selecionado tiver dado para o
  novo capítulo, mantém-se a seleção; caso contrário, salta para o primeiro
  estado disponível no novo capítulo.
- Se o capítulo não tiver `organKey` (prose/articles), a fileira de pills fica
  vazia e a Coluna 3 mostra o aviso de "sem equivalente".

## Componentes e arquivos

| Arquivo | Ação | Responsabilidade |
|---|---|---|
| `src/pages/RIComparator.jsx` | Criar | Página inteira: fetches, estado local, 3 colunas |
| `src/App.jsx` | Modificar | Rota `/minuta/comparativo-ri` + item no `NAV` |
| `src/index.css` | Modificar | Classe `.ri-state-col` (sticky + scroll), espelhando `.rev-doc` |

Sem componentes auxiliares novos: a Coluna 2 e a Coluna 3 são renderizadas
inline em `RIComparator.jsx`. `ChapterRail` é reusado.

### `App.jsx`
- Rota: `<Route path="/minuta/comparativo-ri" element={<RIComparator />} />`.
- Entrada no array `NAV`: ícone `GitCompareArrows` (lucide-react), rótulo
  "Comparativo de RI", posicionada junto às demais rotas `/minuta/*`.

## Tratamento de erros e estados de borda

- **Falha de fetch** (qualquer um dos dois JSON): exibe mensagem de erro no
  corpo da página, no mesmo padrão de `MinutaRevisao.jsx` ("Erro ao carregar…").
- **Capítulo sem `organKey`:** Coluna 3 exibe "Sem equivalente direto nos RIs
  analisados." (nenhuma pill).
- **Capítulo-órgão sem nenhum estado-RI com dado:** fileira de pills vazia;
  Coluna 3 exibe "Nenhum RI analisado trata deste órgão."
- **Estado selecionado sem dado** (não deve ocorrer, pois pills só listam
  estados com dado): guarda defensiva exibindo "Nenhum dado disponível para
  este órgão neste RI."
- **`stateEntry.organs[]` com atribuições vazias:** o estado é tratado como
  "sem dado" e não vira pill.

## Testes

A lógica de mapeamento e seleção é pura e testável isoladamente. Extrair para
funções puras (dentro de `RIComparator.jsx` ou um pequeno módulo
`src/lib/riComparison.js`) e cobrir com `node --test`:

- `indexComparativo(comparativo)` → `{ [organKey]: organEntry }`.
- `statesWithData(organEntry, riStateIds)` → lista ordenada de estados com
  atribuições não vazias para aquele órgão.
- `pickState(prevStateId, availableStates)` → mantém o estado anterior se
  disponível, senão o primeiro; `null` se lista vazia.

Casos: órgão com vários estados; órgão sem nenhum estado-RI; troca de capítulo
preservando/repondo o estado; capítulo sem `organKey`.

## Critérios de aceitação

1. `/minuta/comparativo-ri` existe, está no menu e carrega sem erro.
2. Selecionar um capítulo-órgão (ex.: DPO) mostra o texto da minuta do CBMRO à
   esquerda e, à direita, as competências do órgão equivalente do estado-RI
   selecionado.
3. Só aparecem como pills os estados-RI com dado para o capítulo atual.
4. Trocar de capítulo preserva o estado quando possível, senão repõe.
5. Capítulos sem equivalente (Preliminares, Estrutura, Finais) exibem o aviso
   apropriado.
6. Badge de proveniência (curado/automático) e `sourceLabel` visíveis na
   Coluna 3.
7. Nenhuma alteração de comportamento nas demais páginas.
