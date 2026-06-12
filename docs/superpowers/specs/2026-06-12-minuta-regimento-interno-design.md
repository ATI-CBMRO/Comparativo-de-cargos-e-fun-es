# Design: Geração de Minuta de Regimento Interno (DPO e COT)

**Data:** 2026-06-12  
**Escopo:** Portal de Legislação CBM — nova funcionalidade de exportação de minuta em `.docx`

---

## Visão Geral

Wizard de 3 etapas no portal que gera uma minuta de Regimento Interno editável para a DPO ou o COT do CBMRO. O sistema propõe automaticamente um texto mesclado a partir dos regimentos dos 26 outros CBMs; o usuário revisa e edita seção a seção, depois baixa o `.docx` pronto para edição jurídica no Word/LibreOffice.

**Usuário-alvo:** Oficial do CBMRO que precisa de um rascunho para levar ao jurídico, ou redator jurídico que quer base comparativa já consolidada.

---

## Arquitetura

### Fluxo de dados

```
comparativo_dpo_cot.json
        ↓
build_minuta_structure.py   (novo script Python)
        ↓
database/minuta_structure.json   (gerado, servido pelo Vite plugin existente)
        ↓
MinutaWizard.jsx   (fetch + wizard + geração docx client-side)
        ↓
Minuta_RI_DPO_CBMRO.docx  /  Minuta_RI_COT_CBMRO.docx   (download)
```

Nenhuma mudança na infraestrutura Vite: `serveDatabase` (dev) e `copyDatabaseOnBuild` (produção) já servem/copiam tudo em `database/` automaticamente.

---

## Script Python — `scripts/build_minuta_structure.py`

**Entrada:** `database/comparativo_dpo_cot.json`  
**Saída:** `database/minuta_structure.json`

### Seções fixas (5 por órgão)

Derivadas da estrutura mais comum nos estados que têm LOB + Regimento Interno (AL, AM, DF, GO, MT, PR, PA, RS, SE):

| id | Título |
|----|--------|
| `subordinacao` | Denominação e Subordinação |
| `finalidade` | Finalidade |
| `competencias` | Competências |
| `organizacao` | Organização Interna |
| `cargos_atribuicoes` | Atribuições dos Cargos |

### Lógica de mesclagem

- CBMRO (`is_reference: true`) entra como base sempre que tiver dados para a seção.
- Para cada seção, coleta textos de todos os estados que possuem o campo preenchido.
- **Texto em prosa:** usa o trecho mais extenso como base.
- **Listas de atribuições/competências:** deduplica por normalização (strip, lowercase, remoção de numeração) e concatena itens únicos em lista numerada.
- Campo `sources` registra os ids dos estados que contribuíram para o `proposedText`.

### Estrutura do JSON gerado

```json
{
  "dpo": {
    "label": "Diretoria de Planejamento Operacional",
    "sections": [
      {
        "id": "subordinacao",
        "title": "Denominação e Subordinação",
        "proposedText": "...",
        "sources": ["ro", "am", "pa"]
      },
      ...
    ]
  },
  "cot": {
    "label": "Comando de Operações Técnicas",
    "sections": [ ... ]
  }
}
```

---

## Frontend — `src/pages/MinutaWizard.jsx`

Nova rota `/minuta` adicionada ao array `NAV` em `App.jsx`.

### Etapa 1 — Escolha do órgão

Dois cartões clicáveis: DPO e COT. Clicar avança para a etapa 2 e carrega as seções do órgão escolhido.

### Etapa 2 — Revisão seção a seção

- Stepper visual no topo (ex.: "Seção 3 de 5").
- Título da seção em destaque.
- Chips "Baseado em: RO, AM, PA" indicando as fontes.
- `<textarea>` pré-preenchida com `proposedText`, editável livremente.
- Botões Anterior / Próxima para navegar entre seções.
- Estado das edições em `useState`: `{ [sectionId]: textoEditado }`, inicializado com os `proposedText` do JSON.

### Etapa 3 — Download

- Resumo colapsável das seções editadas (somente leitura).
- Botão primário **"Baixar .docx"** — dispara geração client-side e download.
- Botão secundário **"Voltar e editar"** — retorna à etapa 2 na última seção.

### Arquivo único

```
src/pages/MinutaWizard.jsx
```

Sem subcomponentes adicionais — complexidade não justifica separação.

---

## Geração do `.docx`

**Biblioteca:** `docx` (npm) — geração client-side, sem servidor.  
**Nome do arquivo:** `Minuta_RI_DPO_CBMRO.docx` ou `Minuta_RI_COT_CBMRO.docx`.

### Estrutura do documento

| Elemento | Detalhe |
|----------|---------|
| Cabeçalho | Brasão CBMRO carregado via `fetch('/BrasaoCBMRO2D-COMPLETO.png')` e convertido para base64 no momento da geração; título institucional, subtítulo com nome do órgão, data de geração |
| Corpo | 5 capítulos (um por seção); cada capítulo: `Heading 1` + parágrafo normal + quebra de página antes (exceto cap. 1) |
| Rodapé | "Documento gerado pelo Portal de Legislação CBM — CBMRO · [data]" |
| Estilo | Times New Roman 12pt, espaçamento 1,5, margens ABNT (sup/esq 3 cm, inf/dir 2 cm) |

---

## Dependências novas

| Pacote | Uso |
|--------|-----|
| `docx` (npm) | Geração do `.docx` client-side |

Script Python não requer dependências novas (usa apenas `json` e `re` da stdlib).

---

## Comando de build

Adicionar ao `CLAUDE.md`:

```bash
python scripts/build_minuta_structure.py  # comparativo_dpo_cot.json -> database/minuta_structure.json
```

Rodar após `build_dpo_cot_comparison.py` (depende do `comparativo_dpo_cot.json`).

---

## Fora do escopo

- Edição colaborativa ou persistência das edições no servidor.
- Geração de DPO e COT num único documento.
- Preview ao vivo do documento durante edição.
- Integração com Track Changes do Word.
