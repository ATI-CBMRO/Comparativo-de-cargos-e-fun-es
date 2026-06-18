# Design: Minuta de Regimento Interno Articulada (DPO/COT)

**Data:** 2026-06-18
**Escopo:** Evolução da feature de geração de minuta — passar de blocos de texto livre para um regimento articulado (Art. 1º, 2º…), com pré-visualização ao vivo e fontes por seção.

---

## Visão Geral

Hoje a minuta é gerada como 5 blocos de texto por órgão. Esta evolução transforma a saída em um **regimento interno articulado** segundo a técnica legislativa: Capítulos > Artigos numerados (Art. 1º, 2º…) > incisos (I, II, III) e parágrafos. O usuário continua editando por textarea (uma linha = um inciso/artigo), mas a numeração e a formatação legislativa são aplicadas automaticamente na renderização — vista em uma **pré-visualização ao vivo** e exportada idêntica no `.docx`.

Gera-se um documento por órgão (DPO e COT separados), como já ocorre.

---

## Decisões de design (do brainstorming)

- **Formato:** articulado de verdade (Art. 1º, 2º…), não blocos de texto.
- **Esqueleto:** 6 capítulos — Disposições Preliminares, Finalidade, Competência, Organização, Atribuições dos Cargos, Disposições Finais.
- **Cláusulas-padrão:** incluir Disposições Preliminares e Disposições Finais (NÃO incluir ementa/preâmbulo nem fecho/assinatura).
- **Edição:** mantém textarea (uma linha = um inciso); sem editor estruturado de itens.
- **Wizard:** adicionar pré-visualização ao vivo + fontes por seção (NÃO incluir localStorage nem export PDF).
- **Incisos:** normalização mecânica de caixa/pontuação na renderização (não reescreve o sentido).

---

## Arquitetura

### Fonte da verdade: `buildArticles`

Um módulo novo `src/lib/minutaArticles.js`, sem dependência de React nem de `docx`, exporta uma função pura:

```
buildArticles(organData, edits) -> Article[]
```

`Article`:
```js
{
  number: 3,                          // número sequencial do artigo no documento
  chapterTitle: "DA COMPETÊNCIA",     // string no 1º artigo do capítulo; null nos demais
  caput: "Compete à DPO:",            // texto do caput do artigo
  incisos: ["coordenação operacional", "execução das atividades-fins"]  // [] se não houver
}
```

A numeração de artigos é **contínua** em todo o documento e calculada aqui (um contador percorre os capítulos na ordem). Nenhum número é digitado pelo usuário.

### Dois renderizadores consomem o mesmo array

1. **Pré-visualização ao vivo** (HTML, em `MinutaWizard.jsx`) — re-renderiza a cada edição.
2. **Geração `.docx`** (parágrafos `docx`, em `MinutaWizard.jsx`) — no download.

O que aparece na prévia é exatamente o que sai no Word, pois ambos derivam do mesmo `buildArticles`.

### Funções auxiliares em `minutaArticles.js`

- `articleLabel(n)` → "Art. 1º"…"Art. 9º" (ordinal até 9), "Art. 10"… (cardinal de 10 em diante).
- `romanize(i)` → "I", "II", "III"… para incisos.
- `normalizeInciso(text, isLast, isPenult)` → 1ª letra minúscula; remove pontuação final existente; acrescenta ";" (ou "; e" no penúltimo, "." no último). Não altera o miolo.

---

## Esqueleto do documento e regras de articulação

Cada órgão produz 6 capítulos. Cada seção tem um `kind` que define a articulação:

| Cap. | `id` | Título (`chapterTitle`) | `kind` | Articulação |
|---|---|---|---|---|
| I | `preliminares` | DAS DISPOSIÇÕES PRELIMINARES | `prose` | Cada linha não-vazia → um artigo (caput em prosa). Pré-preenchido: artigo do objeto + artigo da base legal/subordinação |
| II | `finalidade` | DA FINALIDADE | `prose` | 1 artigo em prosa |
| III | `competencias` | DA COMPETÊNCIA | `incisos` | 1 artigo: caput fixo + cada linha → inciso |
| IV | `organizacao` | DA ORGANIZAÇÃO | `incisos` | 1 artigo: caput fixo + cada linha → inciso |
| V | `cargos_atribuicoes` | DAS ATRIBUIÇÕES DOS CARGOS | `cargos` | Cada linha terminada em ":" inicia um artigo "Ao {cargo} compete:"; linhas seguintes (indentadas ou não) → incisos do artigo corrente |
| VI | `disposicoes_finais` | DAS DISPOSIÇÕES FINAIS | `prose` | Cada linha não-vazia → um artigo. Pré-preenchido: casos omissos + vigência/revogação |

### Regras (no `buildArticles`)

- **`prose`:** cada linha não-vazia de `proposedText` vira um `Article` com `caput = linha`, `incisos = []`.
- **`incisos`:** um único `Article` cujo `caput` é o `section.caput` (template, ex.: "Compete à DPO:") e cujos `incisos` são as linhas não-vazias de `proposedText`, na ordem.
- **`cargos`:** percorre as linhas; linhas em branco são ignoradas; uma linha terminada em ":" abre novo `Article` (`caput` = "Ao {nome} compete:", derivado do texto antes do ":"); demais linhas não-vazias entram em `incisos` do artigo corrente. Linhas de inciso antes de qualquer "Cargo:" são descartadas (não há artigo aberto).
- **Normalização de incisos:** aplicada na renderização (não muda o `proposedText` editável). Penúltimo inciso recebe "; e"; último recebe "."; demais ";".
- **`chapterTitle`:** preenchido apenas no primeiro `Article` de cada capítulo; `null` nos seguintes (para um capítulo com vários artigos, ex.: preliminares, cargos, finais).
- **Concordância de gênero:** o caput usa o campo `artigoCaput` do órgão ("à DPO" / "ao COT"); sem heurística.

---

## Camada de dados: `build_minuta_structure.py`

O JSON gerado passa a ter, por órgão, os campos `abbr` e `artigoCaput`, e cada seção ganha `chapterTitle`, `kind`, `caput` e `sourceExcerpts`.

```json
{
  "generated_by": "scripts/build_minuta_structure.py",
  "dpo": {
    "label": "Diretoria de Planejamento Operacional",
    "abbr": "DPO",
    "artigoCaput": "à DPO",
    "sections": [
      {
        "id": "preliminares",
        "chapterTitle": "DAS DISPOSIÇÕES PRELIMINARES",
        "kind": "prose",
        "caput": null,
        "proposedText": "Este Regimento Interno disciplina a organização, as competências e o funcionamento da Diretoria de Planejamento Operacional (DPO) do Corpo de Bombeiros Militar do Estado de Rondônia.\nA Diretoria de Planejamento Operacional subordina-se ao Subcomandante-Geral, nos termos da Minuta de Projeto de Lei n.º 0059262482 (abril de 2025) — Organização Básica do CBMRO.",
        "sources": ["ro"],
        "sourceExcerpts": {}
      },
      {
        "id": "competencias",
        "chapterTitle": "DA COMPETÊNCIA",
        "kind": "incisos",
        "caput": "Compete à DPO:",
        "proposedText": "coordenação operacional\nexecução das atividades-fins da Corporação\n…",
        "sources": ["ro", "am", "pr"],
        "sourceExcerpts": {
          "ro": "Órgão responsável pelo planejamento…",
          "am": "Coordenação operacional\nExecução das atividades-fins\n…"
        }
      }
    ]
  },
  "cot": { "…": "mesma estrutura" }
}
```

### Mudanças no script

- **Dois capítulos novos** (`preliminares`, `disposicoes_finais`) com `proposedText` montado por template a partir dos dados do CBMRO:
  - Preliminares — Art. objeto: "Este Regimento Interno disciplina a organização, as competências e o funcionamento da {label} ({abbr}) do Corpo de Bombeiros Militar do Estado de Rondônia." Art. base legal: "A {label} subordina-se a {subordinadoA}, nos termos da {baseLegal}."
  - Disposições Finais — Art.: "Os casos omissos neste Regimento serão resolvidos pelo Comandante-Geral do CBMRO." Art.: "Este Regimento Interno entra em vigor na data de sua publicação, revogadas as disposições em contrário."
- **`kind`, `chapterTitle`, `caput`** por seção, conforme a tabela do esqueleto.
- **`caput` de competências/organização:** "Compete {artigoCaput}:" e "{artigoCaput===\"à DPO\" ? \"A DPO\" : \"O COT\"} tem a seguinte estrutura:" (texto pré-computado no script, que conhece o órgão).
- **`proposedText` de competências:** somente as linhas dos incisos (sem prefixo "1."). A lógica atual de limpeza (base CBMRO + genéricas filtradas) é mantida — apenas o prefixo numérico deixa de ser escrito.
- **`sourceExcerpts`:** para cada seção e cada estado em `sources`, o texto bruto extraído daquele estado (antes do merge). Para competências, a lista de atribuições do estado (uma por linha). Para preliminares/finais (templates), fica `{}`.
- A função `extract_*` existente é reaproveitada para popular `sourceExcerpts` por estado.
- Comando de build no `CLAUDE.md` permanece o mesmo.

---

## Wizard: `MinutaWizard.jsx`

Mantém o fluxo de 3 etapas (escolha → revisão → download) e a edição por textarea.

### Etapa 2 — revisão (duas colunas)

- **Coluna esquerda (edição):** título do capítulo, chips de fontes, textarea pré-preenchida com `proposedText` (estado em `edits[section.id]`, como hoje), navegação Anterior/Próxima.
- **Coluna direita (prévia ao vivo):** renderiza via `buildArticles` **apenas o capítulo atual** já articulado (Art. Nº, incisos numerados, normalização aplicada). Atualiza a cada tecla.
- **Responsivo:** em telas estreitas, a prévia vira painel colapsável abaixo da textarea.
- **Fontes por seção:** os chips de estados são clicáveis; ao clicar, expande abaixo o trecho de `sourceExcerpts[estado]` num bloco de leitura (somente leitura, para copiar ideias). Seções sem `sources` (preliminares/finais) não exibem chips.

### Etapa 3 — download

- O resumo passa a exibir a **prévia articulada completa** (todos os capítulos), reusando o renderizador de preview da Etapa 2.
- Botões "Voltar e editar" e "Baixar .docx" mantidos.

### Geração `.docx`

- `handleDownload` passa a iterar o array de `buildArticles(organData, edits)`:
  - Título do capítulo (quando presente): duas linhas centralizadas/negrito — "CAPÍTULO {N}" e "{chapterTitle}"; quebra de página antes (exceto o 1º).
  - Caput: "Art. Nº" em negrito + restante; justificado; recuo de 1ª linha ~1,25 cm (708 twips).
  - Incisos: "I - texto;" com hanging indent; justificado.
- Cabeçalho institucional (brasão, título, subtítulo do órgão, data) e rodapé: mantidos.
- Estilo Times New Roman 12pt, espaçamento 1,5, margens ABNT: mantidos.
- Nome do arquivo: mantido.

---

## Arquivos afetados

| Ação | Arquivo |
|---|---|
| Criar | `src/lib/minutaArticles.js` |
| Modificar | `scripts/build_minuta_structure.py` |
| Modificar | `src/pages/MinutaWizard.jsx` |
| Regerar | `database/minuta_structure.json` |

---

## Fora do escopo

- Editor estruturado de incisos (botões reordenar/excluir/adicionar) — mantém-se a textarea.
- Persistência de rascunho (localStorage).
- Exportação em PDF.
- Ementa, preâmbulo, fecho e assinatura.
- Geração de DPO e COT num único documento.
- Parágrafos (§) e alíneas como entidades editáveis distintas — o usuário pode digitá-los livremente na textarea, mas não há tratamento estrutural dedicado nesta fase.
