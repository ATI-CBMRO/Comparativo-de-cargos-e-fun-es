# Comparador "Subsídio à Minuta" — Design

**Data:** 2026-06-21
**Status:** Aprovado no brainstorming, aguardando revisão do spec

## Problema

Depois que os comparadores foram criados, a geração da **minuta de Regimento Interno**
evoluiu e ficou muito mais profunda: hoje cobre toda a cadeia operacional do CBMRO
(10 órgãos da LOB + capítulo da **Guarnição de Serviço Operacional**, descendo até as
atribuições do **Comandante de Guarnição**). Os comparadores não acompanharam essa
profundidade e ficaram desalinhados do objetivo real.

Hoje existem **dois** comparadores como abas do Dashboard:
- **Comparativo de Cargos** (`CargoComparator.jsx`): casa 1 cargo do RO contra os 26
  estados; filtros de região, similaridade e busca.
- **DPO × COT** (`OrgaosOperacionaisComparator.jsx`): compara apenas os órgãos DPO e COT,
  em matriz + modal fullscreen + exportação PDF.

Problemas: (a) só cobrem DPO/COT e cargos isolados — raso perante a minuta; (b) propósitos
sobrepostos em dois lugares; (c) filtros (região, similaridade) e disposição poluem a
leitura; (d) o de Cargos não abre em página própria.

## Objetivo

Uma **única ferramenta** que compare a legislação do CBMRO contra os demais estados,
organizada pela **mesma estrutura da minuta**, para **subsidiar a elaboração do Regimento
Interno** — navegar pela minuta e, em cada ponto, ver o que cada estado fez ali.

## Decisões (tomadas no brainstorming)

1. **Estrutura:** página única espelhando a minuta (não duas páginas separadas).
2. **Cobertura:** exibir **só onde há dado** — ocultar automaticamente colunas/níveis sem
   substância, para reduzir ruído.
3. **Layout da comparação:** **matriz** — campos nas linhas, estados nas colunas, RO sticky
   à esquerda (mesmo estilo do DPO×COT atual, que o usuário aprova).
4. **Fonte de dados:** **híbrido** — curado onde existe, complementado por extração
   automática, com marcação clara de proveniência.
5. **`Compare.jsx` (página "Comparativo" estado × estado):** **remover** (rota, página e
   item de sidebar). O objetivo é RO-cêntrico; comparar dois estados quaisquer agrega pouco.

## Arquitetura

### Navegação e IA

- A nova página fica na sidebar como **"Subsídio à Minuta"** → rota **`/comparar`** (mesma
  rota antes usada pelo `Compare.jsx`, agora reaproveitada).
- `src/pages/Compare.jsx` é removido; a rota `/comparar` passa a renderizar a nova página.
- As abas **"Comparativo de Cargos"** e **"DPO × COT"** saem do `Dashboard.jsx` — o
  Dashboard volta a ter só **"Visão Geral"** (remove o estado `activeTab` e os imports dos
  dois comparadores).
- Componentes aposentados: `CargoComparator.jsx` e `OrgaosOperacionaisComparator.jsx`
  (sua lógica útil — normalização/casamento de cargos, render verbatim, matriz, PDF — é
  reaproveitada na nova página).

### Espinha = a minuta

- Sidebar/sumário interno lista os **12 órgãos** na ordem de subordinação do RO:
  DPO, COT, DOE, CRBM, BBM, CIBM, GBM, BBS, BIFEA, BOA, **+ Guarnição de Serviço
  Operacional**.
- Clicar num órgão carrega o comparativo daquele órgão.
- Capítulos de prosa (Preliminares, Estrutura, Disposições Finais) ficam de fora — não são
  comparáveis estado a estado.

### Matriz por órgão

Para o órgão selecionado, tabela com:
- **Linhas (campos):** Órgão/Sigla, Subordinação, Cargo/Função, Requisito/Posto,
  Atribuições/Competências (verbatim), Desdobramentos.
- **Colunas:** RO (sticky, referência) + cada estado **que tem dado** para aquele órgão.
- Estados sem nenhum dado para o órgão **não geram coluna**.
- Cada coluna de estado traz um selo de **proveniência**: `Curado` (verbatim, atribuído) ou
  `Automático` (extração de `organs_detail`, pode ser raso/impreciso).

### Camada de dados — pipeline (híbrido)

Seguindo o padrão do projeto (frontend lê JSON gerado offline), um **novo script**
`scripts/build_minuta_comparison.py` produz **`database/comparativo_minuta.json`**, a fonte
única da página. O script combina três origens, na ordem de prioridade:

1. **DPO e COT → curado.** Reaproveita `database/comparativo_dpo_cot.json` (mapeamento
   curado de qual órgão de cada estado ≈ DPO/COT, com textos verbatim e notas). Proveniência
   `curado`.
2. **Competências curadas e Guarnição → curado.** Pivota o material de
   `scripts/minuta_enrichment.py` (`ENRICHMENT_ORGAN` por órgão e `GUARNICAO_CHAPTER` do
   CBMSE) por **estado de origem**, expondo os incisos verbatim atribuídos
   (ex.: "cf. CBMMT, RI, Art. 236", "cf. CBMSE, RISD, Art. 14"). Proveniência `curado`.
3. **Demais órgãos → automático.** Para os órgãos sem cobertura curada, casa o órgão da
   minuta contra os órgãos de cada `database/organs_detail/<estado>.json` por
   nome/sigla, reusando a normalização tolerante (sinônimos/tokens) hoje em
   `CargoComparator.jsx` (a ser portada para Python). Proveniência `automatico`.

**Coluna do RO (referência):** sempre da legislação **própria** do RO —
`database/organs_detail/ro.json` puro (estrutura, cargos com requisito + atribuições,
desdobramentos). Nunca usa o texto enriquecido da minuta (evita comparação circular).

**Guarnição:** o RO **não disciplina** (a minuta adotou o CBMSE/RISD). A coluna do RO exibe
a nota *"O CBMRO não disciplina a Guarnição de Serviço; a minuta propõe com base no
CBMSE/RISD"*, e a coluna do CBMSE traz as atribuições do **Comandante de Guarnição** e do
**Condutor/Operador de Viatura** verbatim.

#### Formato de `comparativo_minuta.json` (esboço)

```jsonc
{
  "generated_by": "scripts/build_minuta_comparison.py",
  "reference": { "id": "ro", "name": "Rondônia", "abbr": "RO", "cbm": "CBMRO" },
  "organs": [
    {
      "key": "cot",
      "title": "DO COMANDO DE OPERAÇÕES TÉCNICAS (COT)",
      "abbr": "COT",
      "reference": {            // coluna RO (de ro.json)
        "name": "...", "abbreviation": "COT", "subordinadoA": "...",
        "cargos": [ { "cargo": "...", "requisito": "...", "atribuicoes": ["..."] } ],
        "atribuicoes": ["..."], "desdobramentos": ["..."]
      },
      "states": [
        {
          "id": "mt", "name": "Mato Grosso", "abbr": "MT", "cbm": "CBMMT",
          "provenance": "curado",          // curado | automatico
          "sourceLabel": "cf. CBMMT, RI, Art. 198",   // quando curado
          "note": null,
          "name_organ": "...", "abbreviation": "...", "subordinadoA": "...",
          "cargos": [ ... ], "atribuicoes": ["..."], "desdobramentos": ["..."]
        }
      ]
    }
  ]
}
```

> ORDEM IMPORTA: `build_minuta_comparison.py` depende de `comparativo_dpo_cot.json`
> (rode `build_dpo_cot_comparison.py` antes), de `organs_detail/*.json`
> (`build_organs_detail.py`) e de `minuta_enrichment.py`.

### Controles (limpos)

- **Removidos:** filtro de **região** e filtro de **nível de similaridade**.
- **Mantidos:** busca textual simples de estado (filtra colunas) e a navegação por órgão.
- **Exportação PDF:** preservada (sem regressão) — exporta o órgão selecionado, no mesmo
  estilo institucional do PDF atual do DPO×COT.

## Componentes (frontend)

- `src/pages/MinutaComparator.jsx` (nova página): fetch de `comparativo_minuta.json`;
  sumário de órgãos (sidebar interna); matriz do órgão selecionado; busca de estado;
  exportação PDF.
- Reaproveitar helpers de render verbatim (`renderFriendlyText`, `List`, células de
  cargos/atribuições) — extrair para um módulo compartilhado se reduzir duplicação.
- `src/App.jsx`: rota `/comparar` aponta para a nova página; remove import/rota de
  `Compare.jsx`; item de sidebar passa a se chamar **"Subsídio à Minuta"**.
- `src/pages/Dashboard.jsx`: remove abas e imports dos comparadores.

## Fora de escopo (v1)

- Curadoria profunda dos 8 órgãos não-DPO/COT (BBM, CRBM, GBM…) — hoje ficam em
  `automatico` e podem ser rasos. Curar a fundo (como DPO/COT) é passo futuro.
- Navegação cargo a cargo dentro do órgão — as atribuições por cargo aparecem nas células
  da matriz; não há tela dedicada por cargo.
- Comparação estado × estado (capacidade do `Compare.jsx` removido).

## Critérios de sucesso

1. A página `/comparar` mostra os 12 órgãos da minuta e, para cada um, RO × estados com dado.
2. Guarnição exibe o Comandante de Guarnição (CBMSE) verbatim — a profundidade que faltava.
3. DPO/COT mantêm a qualidade curada atual; itens curados trazem a fonte; itens automáticos
   vêm marcados como tais.
4. Sem filtros de região/similaridade; disposição limpa; abre em página própria.
5. Dashboard só com "Visão Geral"; `Compare.jsx` removido; sem rotas/links quebrados.
