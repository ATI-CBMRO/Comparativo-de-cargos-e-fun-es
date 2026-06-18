# Minuta de Regimento Interno — articulação hierárquica do topo operacional à menor fração

**Data:** 2026-06-18
**Status:** Aprovado para planejamento
**Substitui (amplia):** `2026-06-18-minuta-articulada-design.md`

## Problema

A geração atual da minuta do Regimento Interno do CBMRO
(`scripts/build_minuta_structure.py`) cobre apenas **2 órgãos** — DPO e COT —
com 6 capítulos cada. Ela descarta toda a cadeia de execução operacional
(CRBM, BBM, Companhia, CIBM, GBM, DOE e unidades especializadas), que **já
existe** no `organs_detail/ro.json` com hierarquia de subordinação e cargos.

O usuário quer que a minuta detalhe a estrutura operacional **do topo à menor
fração**, espelhando o modelo do Regimento Interno do CBMAL, que enumera
competências verbatim descendo até Comandante/Subcomandante de Grupamento e
Subunidades (Arts. 113–116).

## Decisões (definidas com o usuário)

1. **Escopo:** cadeia operacional completa — DPO e COT + todos os subordinados
   operacionais (Coordenadorias, CRBM→BBM→Companhia, CIBM, GBM, DOE→BBS/BIFEA/BOA).
2. **Fonte das atribuições:** RO verbatim onde existir + enriquecimento com
   competências de outras legislações, **cada item rotulado com a fonte**
   (ex.: "cf. CBMAL, RI, Art. 115, III").
3. **Estrutura:** Abordagem A — regulamento hierárquico único espelhando um RI
   real (Título → Capítulos por órgão → Seções por função).
4. **Enriquecimento nesta entrega:** seed completo a partir do **CBMAL** para a
   cadeia de comando operacional; módulo estruturado para crescer (PR/PA/MT/ES) depois.

## Arquitetura de dados

Separação limpa de fontes — o `ro.json` **não** é poluído com texto de outros
estados (ele continua sendo a referência canônica do Comparador de Cargos):

| Fonte | Papel | Mudança |
|---|---|---|
| `database/organs_detail/ro.json` | Estrutura da cadeia operacional + competências RO verbatim (já completo). | Sem mudança de conteúdo. |
| **NOVO** `scripts/minuta_enrichment.py` | Enriquecimento curado por função: `{ organKey/function → [{text, source}] }`. Seed CBMAL. | Criar. |
| `database/comparativo_dpo_cot.json` | Agregação genérica existente p/ competências de DPO/COT. | Mantido. |

**Fluxo:**
```
ro.json + minuta_enrichment.py + comparativo_dpo_cot.json
   → build_minuta_structure.py
   → database/minuta_structure.json  (hierárquico)
   → MinutaWizard.jsx + exportação .docx
```

## Árvore operacional (ordem por subordinação, derivada do ro.json)

```
Subcomandante-Geral
├─ DPO ─ Coordenadorias (Operações · Doutrina/Pesquisa · Estudos Estratégicos)
│        ├─ CRBM ─ BBM ─ Companhia
│        │         └─ CIBM
│        └─ COT ─ CATs (→ Seções) · Coord. de Projetos de Arq./Eng.
├─ DOE ─ BBS · BIFEA · BOA
└─ GBM (Grupo — menor fração)
```

Subordinações relevantes confirmadas no `ro.json`:
`cot.subordinadoA = DPO`, `doe.subordinadoA = Subcomandante-Geral`,
`crbm.subordinadoA = DPO`, `bbm.subordinadoA = CRBM`, `cibm.subordinadoA = CRBM`,
`bbs/bifea/boa.subordinadoA = DOE`.

## Estrutura do documento gerado

```
TÍTULO ÚNICO — DO REGIMENTO INTERNO DA ESTRUTURA OPERACIONAL DO CBMRO
  CAP. I    — Das Disposições Preliminares        (global, prosa)
  CAP. II   — Da Estrutura Organizacional          (organograma → artigo + incisos)
  CAP. III  — Da Diretoria de Planejamento Operacional (DPO)
       Seção I   — Da Finalidade
       Seção II  — Da Competência                  (incisos)
       Seção III — Da Organização Interna          (incisos)
       Seção IV+ — Das Atribuições do <cargo>      (uma seção por função, incisos)
  CAP. IV   — Do Comando de Operações Técnicas (COT)        … mesmas seções
  CAP. V    — Da Diretoria Operacional Especializada (DOE)
  CAP. VI   — Dos Comandos Regionais de Bombeiro Militar (CRBM)
  CAP. VII  — Do Batalhão de Bombeiros Militar (BBM)
  CAP. VIII — Da Companhia Independente de Bombeiros Militar (CIBM)
  CAP. IX   — Do Grupo de Bombeiros Militar (GBM)
  CAP. X    — Das Unidades Operacionais Especializadas (BBS, BIFEA, BOA)
  CAP. XI   — Das Disposições Finais               (global)
```

- Numeração de artigos **contínua** atravessando todos os capítulos.
- Capítulos em romano (I, II, …); seções em romano próprias por capítulo.
- "Da Estrutura Organizacional" lista o organograma operacional como incisos.

## Modelo do `minuta_structure.json` (hierárquico)

```jsonc
{
  "generated_by": "...",
  "title": "TÍTULO ÚNICO — ...",
  "chapters": [
    { "id": "preliminares", "kind": "prose", "chapterTitle": "...", "proposedText": "..." },
    { "id": "estrutura",    "kind": "incisos", "caput": "...", "proposedText": "...", "sources": [...] },
    {
      "id": "organ:dpo", "kind": "organ", "chapterTitle": "DA DIRETORIA ...",
      "organKey": "dpo", "label": "...", "abbr": "DPO",
      "sections": [
        { "id": "finalidade",  "kind": "prose",   "sectionTitle": "Da Finalidade", "proposedText": "..." },
        { "id": "competencia", "kind": "incisos",  "sectionTitle": "Da Competência", "caput": "...",
          "items": [ { "text": "...", "source": "ro" }, { "text": "...", "source": "cf. CBMAL, Art. 115, III" } ] },
        { "id": "organizacao", "kind": "incisos",  "sectionTitle": "Da Organização Interna", "items": [...] },
        { "id": "cargo:diretor", "kind": "incisos", "sectionTitle": "Das Atribuições do Diretor", "caput": "Ao Diretor compete:", "items": [...] }
      ]
    }
  ]
}
```

Itens passam a ser `{text, source}` (não mais string pura) para carregar a
citação de fonte e permitir o badge no wizard. `source: "ro"` = verbatim RO.

## Enriquecimento rotulado

- `scripts/minuta_enrichment.py` expõe um dicionário curado mapeando função →
  lista de `{text, source}`, extraído verbatim do RI do CBMAL para a cadeia de
  comando: Comandante Regional, Comandante/Subcomandante de Batalhão-Grupamento,
  Comandante de Companhia, Chefes de Seção, Ajudante-Secretário.
- O build mescla RO (base) + enriquecimento, **deduplica** por texto normalizado
  (mesma `normalize()` atual) e ordena RO-primeiro.
- Citação inline na fonte de cada item (campo `source`); no wizard vira badge;
  no `.docx` vira nota/sufixo discreto.

## Frontend

- **`src/lib/minutaArticles.js`**: estender a articulação para a hierarquia
  Título → Capítulo → Seção (hoje só Capítulo). Suportar `items` `{text,source}`.
  Numeração de artigos contínua; seções romanas por capítulo.
- **`src/lib/minutaArticles.test.js`**: novos casos — numeração contínua
  atravessando capítulos; seções por função; sufixos de inciso "; e" / "."
  preservados; dedup de enriquecimento; presença da citação de fonte.
- **`src/pages/MinutaWizard.jsx`**: navegação pela árvore de órgãos (accordion/
  sidebar), prévia ao vivo do articulado completo, edição por seção, badge de
  fonte nos itens enriquecidos.
- **Exportação `.docx`**: refletir Título/Capítulo/Seção, incisos e citações.

## Pipeline / ordem de execução

`build_organs_detail.py` → `build_states_data.py` → `build_dpo_cot_comparison.py`
→ **`build_minuta_structure.py`** (reescrito). O enriquecimento é importado pelo
último script; não altera as etapas anteriores.

## Testes e verificação

- Unit puro (`minutaArticles.test.js`) cobrindo a articulação hierárquica.
- Verificação manual: `npm run dev` (localhost:5173), navegar o wizard, conferir
  prévia e gerar `.docx`.
- Conferir que o Comparador de Cargos continua intacto (ro.json não mudou).

## Fora de escopo (YAGNI)

- Enriquecimento de PR/PA/MT/ES (entrega futura; módulo já preparado).
- Órgãos não-operacionais (Pessoal, Logística, Saúde etc.).
- Alteração do conteúdo do `ro.json`.
