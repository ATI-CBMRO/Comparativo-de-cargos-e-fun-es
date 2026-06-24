# Diagramas da Minuta — Design

**Data:** 2026-06-23
**Status:** Aprovado (design); pendente de plano de implementação

## Objetivo

Nova página no portal apresentando, de forma visual, **dois diagramas** da Minuta de
Regimento Interno operacional do CBMRO:

1. **Organograma** — a cadeia de comando operacional (quem se subordina a quem).
2. **Mapa mental** — a estrutura do documento (os 15 capítulos da minuta e suas seções).

Ambos clicáveis, abrindo um painel de detalhe com o conteúdo do capítulo correspondente,
e com exportação para impressão/PDF.

## Decisões (do brainstorming)

| Tema | Decisão |
|------|---------|
| O que os diagramas representam | Organograma = cadeia de comando; Mapa mental = estrutura do documento |
| Local | Novo item no menu lateral (rota própria) |
| Visual do organograma | Caixas e linhas (org chart clássico), em SVG/CSS à mão, **sem lib nova** |
| Visual do mapa mental | Cartões por capítulo, em grade |
| Profundidade do organograma | Os 12 órgãos da minuta, posicionados pela subordinação |
| Interação | Caixas/cartões clicáveis → painel de detalhe |
| Exportação | Imprimir/PDF via `window.print()` + `@media print` |
| Fonte de dados | Gerada no pipeline Python (não derivada no cliente) |

## Arquitetura

### 1. Navegação e rota

Em [App.jsx](../../../src/App.jsx):
- Novo item no array `NAV`, logo após "Minuta RI":
  `{ to: '/minuta-diagramas', icon: Network, label: 'Diagramas da Minuta' }`
  (ícone `Network` do `lucide-react`).
- Nova `<Route path="/minuta-diagramas" element={<MinutaDiagrams />} />`.

### 2. Camada de dados (pipeline)

Estender [build_minuta_structure.py](../../../scripts/build_minuta_structure.py) para gravar,
no `database/minuta_structure.json`, um novo campo de topo `commandChart`: a árvore dos 12
órgãos da minuta, derivada do `ro.json`.

**Algoritmo de montagem da árvore:**
1. Conjunto dos 12 `organKey` da minuta (dpo, doe, cot, crbm, bbm, cibm, cat, bbs, bifea,
   boa, gbm, guarnicao) com `sigla`/`label`/`chapterId` vindos dos próprios capítulos
   `kind == 'organ'` do `minuta_structure`.
2. Para cada órgão, ler `subordinadoA` no `ro.json` (as chaves de `organs` casam 1:1 com os
   `organKey`, exceto `guarnicao`, que não existe no `ro.json`).
3. Resolver o pai: procurar, na string `subordinadoA`, a **sigla** de outro órgão do
   conjunto. Casos:
   - `dpo`, `doe` → `subordinadoA` = "Subcomandante-Geral" (nenhuma sigla do conjunto) → filhos da raiz.
   - `cot`, `crbm` → DPO. `cat` → COT. `bbm`, `cibm` → CRBM. `bbs`, `bifea`, `boa` → DOE.
4. **Colocações padrão explícitas** (confirmadas com o usuário) para os dois nós que não
   casam pela subordinação textual:
   - `gbm` (`subordinadoA` = "Pelotão…", fora do conjunto) → filho de **BBM** (fração elementar).
   - `guarnicao` (sem entrada no `ro.json`; nó novo do RISD-CBMSE) → filho de **GBM** (menor fração).
5. Raiz sintética `{ label: "Subcomandante-Geral", synthetic: true, children: [dpo, doe] }`.

**Árvore resultante:**
```
Subcomandante-Geral (sintético)
├── DPO
│   ├── COT
│   │   └── CAT
│   └── CRBM
│       ├── BBM
│       │   └── GBM
│       │        └── Guarnição de Serviço Operacional
│       └── CIBM
└── DOE
    ├── BBS
    ├── BIFEA
    └── BOA
```

**Formato do nó** (nested):
```json
{ "organKey": "dpo", "sigla": "DPO", "label": "Diretoria de Planejamento Operacional",
  "chapterId": "organ:dpo", "children": [ ... ] }
```
A raiz usa `{ "label": "Subcomandante-Geral", "synthetic": true, "children": [ ... ] }`.

O `chapterId` (ex.: `organ:dpo`) liga cada caixa ao capítulo correspondente no array
`chapters`, alimentando o painel de detalhe.

### 3. Frontend

Nova página `src/pages/MinutaDiagrams.jsx`:
- `fetch('/database/minuta_structure.json')` com estados de loading/erro (padrão do
  `MinutaWizard`). Se faltar `commandChart` (JSON antigo), mensagem
  "Execute build_minuta_structure.py".
- **Controle segmentado** no topo: `[ Organograma ] [ Mapa mental ]` — mostra um diagrama
  por vez na tela — mais botão **Imprimir / PDF** (`window.print()`).
- Estado: `view` ('org' | 'mind'), `selected` (chapterId | null).

Componentes:
- **`src/components/MinutaOrgChart.jsx`** — recebe `commandChart` e `onSelect(chapterId)`.
  Org chart caixas-e-linhas, montado com flex aninhado + conectores via pseudo-elementos
  CSS (técnica clássica de árvore CSS, sem biblioteca). Container com scroll horizontal
  quando a árvore ficar larga. Cada caixa é um `<button>` (exceto a raiz sintética, que não
  tem capítulo) → `onSelect(node.chapterId)`. Caixa do `selected` recebe destaque.
- **`src/components/MinutaMindMap.jsx`** — recebe `chapters` e `onSelect(chapterId)`. Grade
  de cartões, um por capítulo (15 no total, incluindo `prose`/`articles`/`organ`). Cada
  cartão mostra o título do capítulo e lista suas seções (quando `kind == 'organ'`) ou um
  resumo (para `prose`/`articles`). Cartão clicável → `onSelect(chapterId)`.
- **`MinutaDetailPanel`** (definido no arquivo da página) — dado o `chapterId` selecionado,
  localiza o capítulo no array `chapters` e mostra: título, e para cada seção o
  `sectionTitle` + os itens (competências), reaproveitando o badge de fonte (RO/CBMxx) do
  padrão do `MinutaWizard` (`srcBadge`). Para capítulos `prose`/`articles`, mostra o
  texto/itens disponíveis. Botão de fechar.

### 4. Estilo e impressão

CSS no único [index.css](../../../src/index.css), seguindo a identidade CBMRO:
- Caixas do organograma: fundo claro com borda, título navy `#121d3d`, sigla destacada;
  raiz sintética em vermelho `#c8102e`. Conectores em cinza sutil.
- Cartões do mapa mental: cartão branco com borda, cabeçalho navy, seções listadas.
- Bloco `@media print`: oculta header/sidebar/controle segmentado/painel e ajusta o
  **diagrama atualmente visível** para caber em **Paisagem** (fonte reduzida), no mesmo
  padrão já usado no Subsídio à Minuta (`MinutaComparator`).

### 5. Estados de carga/erro

Idênticos ao `MinutaWizard`: cabeçalho de página + mensagem de "Carregando…" ou erro
vermelho. Erro específico se `commandChart` ausente.

### 6. Testes e documentação

- A lógica de montagem da árvore é pura, do lado Python; verificável rodando
  `build_minuta_structure.py` e inspecionando o `commandChart` no JSON gerado. Sem suíte de
  testes JS nova (a parte React é apresentacional).
- Atualizar a descrição de `build_minuta_structure.py` em [CLAUDE.md](../../../CLAUDE.md)
  para registrar o novo campo `commandChart` e a página `/minuta-diagramas`.

## Fora de escopo (YAGNI)

- Sem biblioteca de diagramas (react-flow etc.).
- Sem zoom/pan; apenas scroll horizontal quando necessário.
- Sem subdivisões internas além dos 12 órgãos no organograma.
- Sem exportação para PNG/SVG (apenas impressão/PDF).
- Mapa mental em cartões (não radial).
