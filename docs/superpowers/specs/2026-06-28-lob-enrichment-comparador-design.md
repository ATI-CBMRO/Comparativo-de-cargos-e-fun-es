# Enriquecimento LOB×LOB do /comparar — curadoria verbatim das LOBs (design)

## Contexto

A página `/comparar` ("Subsídio à Minuta", `src/pages/MinutaComparator.jsx`) compara,
órgão a órgão, o CBMRO contra cada estado em **3 colunas** (já existentes na tela):

1. **CBMRO** — a LOB do CBMRO (referência), de `organs_detail/ro.json`.
2. **LOB do estado** — `state.lobOrgans` / `state.lobProvenance`: só a Lei de Organização
   Básica do estado.
3. **Legislação compilada (LOB + RI)** — `state.organs` / `state.provenance`: a estrutura
   enriquecida com as demais fontes (Regimento Interno, NGA etc.).

Hoje a coluna 2 é preenchida por **auto-match por palavra-chave** contra
`organs_detail/<id>.json` filtrado a `source=='lob'` (`attach_lob_organs` em
`scripts/build_minuta_comparison.py`). Para os órgãos que são **estruturas básicas
presentes em todos os CBMs** (Comando Geral, Diretoria de Pessoal, Ensino, Finanças,
Saúde, Logística, Defesa Civil etc.), essa coluna é **vazia ou rasa** em muitos estados,
porque a curadoria do `organs_detail` priorizou os órgãos operacionais e porque muitas
LOBs descrevem esses órgãos apenas por uma **finalidade/caput** (uma frase), que a Frente 2
(critério estrito: só incisos enumerados verbatim) **descartava**.

Medição (estado atual): `dp` aparece em 18/27 estados (ausente em DF, ES, GO, MT, PA, SP,
RS, CE, MG, AP, SE), e raso (1–2 itens) em vários presentes; `depdec` ausente em 17 estados.

## Objetivo

Levantar o **máximo de informação das LOBs** de **todos os 27 estados** para **todos os 26
órgãos da LOB**, transcrito **verbatim**, enriquecendo as colunas 2 e 3 do `/comparar`:

- **Coluna 2 (LOB pura)** passa a trazer, por estado, a **finalidade verbatim** (caput de uma
  frase) e/ou os **incisos** que a LOB enumera para cada órgão, com citação da fonte
  (`cf. CBMxx, LOB (Lei …), Art. N`), marcada "Curado".
- **Coluna 3 (LOB + RI)** passa a ser a **união**: a finalidade da LOB (camada nova) **+** as
  competências de RI já curadas na Frente 2 (`ENRICHMENT_ORGAN`) **+** o auto-match,
  cada item rotulado por fonte.

### Mudança de critério (vs Frente 2)

A Frente 2 (em `docs/ENRIQUECIMENTO_MINUTA.md`) só admitia competência **enumerada e
verbatim**, descartando caput definicional/finalidade. Esta camada **relaxa** o critério
**apenas para a coluna LOB**: admite a **finalidade/caput verbatim** (1 frase) como conteúdo
válido, além dos incisos. Permanece proibido **parafrasear, condensar ou inventar** — só
transcrição fiel da LOB, com correção de OCR óbvio (ex.: "as as" → "as"). Itens de RI **não**
entram nesta camada (são da Frente 2).

## Escopo

- **Órgãos:** todos os 26 órgãos da LOB do CBMRO (`ORGAN_ORDER` em
  `scripts/build_minuta_structure.py`). A Guarnição (`guarnicao`) não tem equivalente de LOB
  estadual e fica fora desta camada (segue como está).
- **Estados:** todos os 27 (exceto RO, que é a referência), para cada órgão que a LOB do
  estado descreva. Estados cuja LOB não mencione um dado órgão simplesmente não geram entrada
  para aquele par (documentado, não é falha).

## Arquitetura

### Camada de dados nova

Arquivo novo `scripts/lob_enrichment.py`, espelhando o padrão de `minuta_enrichment.py`:

```python
# LOB_ENRICHMENT[(organ_key, state_id)] = entrada verbatim da LOB daquele estado.
LOB_ENRICHMENT = {
    ("dp", "sc"): {
        "finalidade": "<caput verbatim, 1 frase — ou '' se a LOB só enumera incisos>",
        "competencias": ["<inciso verbatim>", "<inciso verbatim>"],  # [] se só houver finalidade
        "source": "cf. CBMSC, LOB (Lei nº 1.058/2024), Art. N",
        "organName": "Diretoria de Pessoal",   # nome do órgão como aparece na LOB do estado
        "abbr": "DP",                            # sigla na LOB do estado (ou "")
    },
    # ...
}

def lob_enrich_for(organ_key: str, state_id: str):
    """Entrada da LOB para (órgão, estado) ou None."""
    return LOB_ENRICHMENT.get((organ_key, state_id))
```

### Mudanças em `scripts/build_minuta_comparison.py`

Três pontos, todos aditivos em relação às camadas existentes (Frente 2 / DPO-COT intactas):

1. **Helper** `lob_organ_from_entry(entry)` → objeto de órgão no formato da matriz
   (compatível com `extract_organ`):
   ```python
   def lob_organ_from_entry(entry):
       items = ([entry["finalidade"]] if entry.get("finalidade") else []) \
               + list(entry.get("competencias") or [])
       return {
           "name": entry.get("organName", ""), "abbreviation": entry.get("abbr", ""),
           "subordinadoA": "", "atribuicoes": items, "desdobramentos": [], "cargos": [],
       }
   ```

2. **Coluna 2** (`attach_lob_organs`): quando há `lob_enrich_for(organ_key, sid)`, o
   `lobOrgans` é montado a partir da entrada curada e `lobProvenance='curado'`; senão mantém
   o auto-match atual (comportamento inalterado).

3. **Coluna 3 + presença do estado** (`build()`): o conjunto de estados de um órgão passa a
   ser a **união** `curated (RI/DPO-COT) ∪ auto ∪ lob_curated`. Um novo
   `lob_curated_states_for(organ_key, meta)` produz registros para estados que têm entrada
   LOB, com `organs=[lob_organ_from_entry(entry)]`, `provenance='curado'`,
   `sourceLabel=entry["source"]`. No merge por estado:
   - se o estado já existe (via RI/auto), **anexa** o órgão da LOB à lista `organs` (col 3 vira
     LOB + RI) e, se ainda não houver, define `sourceLabel`;
   - se o estado só existe via LOB, entra novo (col 3 = só LOB).
   Dedup por texto evita repetir um item idêntico que apareça em LOB e RI.

   > Consequência intencional: a coluna 3 deixa de excluir a camada LOB (revoga o comentário
   > atual em `build_minuta_comparison.py:189-190`), passando a ser "LOB + RI" como pedido.

`database/organs_detail/*.json` e `database/comparativo_dpo_cot.json` **nunca são tocados**.
`ENRICHMENT_ORGAN` (Frente 2) **não é alterado** — só somado.

### Frontend

Nenhuma mudança estrutural obrigatória: `MinutaComparator.jsx` já renderiza as 3 colunas
(`PairTable` com `oc-pair-table-3`) e a coluna 2 já mostra `lobProvenance`. Ajuste textual
opcional: o parágrafo de ajuda e o cabeçalho da coluna 3 podem passar de "Compilada/todas as
fontes" para "LOB + RI", para casar com a nova semântica. Sem mudança de lógica.

## Workflow de curadoria — orientado a ESTADO

Diferente da Frente 2 (orientada a órgão), aqui a leitura é **por estado**: cada LOB descreve
vários órgãos, então o subagente lê a LOB de um estado **uma vez** e extrai todos os órgãos
que ela define, mapeando cada um ao `organ_key` do RO (nomes variam entre estados; usar o
mapa canônico de `STATE_META`/`ORGAN_ORDER` e sinônimos — ex.: "Diretoria de Gestão de
Pessoas" → `dp`, "Academia de Bombeiro" → `deei`). Estados que não tenham um órgão
simplesmente não geram entrada para ele.

Decomposição em **~5 lotes de 5–6 estados**. Cada lote:
1. Subagente de pesquisa (somente leitura nas LOBs em `database/markdown/*Organiza*Básica*.md`
   — e o doc único quando o estado só tem LOB) extrai, por estado e por órgão: finalidade
   verbatim + incisos verbatim + citação (Lei + Art.).
2. Controller integra as entradas em `scripts/lob_enrichment.py` (aditivo).
3. Regenera `comparativo_minuta.json`; verifica colunas 2 e 3; roda testes; revisão spec +
   qualidade (mesmo rito da Frente 2).

A **Task 0** (modelo de dados + merge no build) vem **antes** dos lotes e é validada com
**1–2 estados de amostra** end-to-end (conferir as 3 colunas na tela) antes da curadoria em
massa.

## Critério de aceite

- Todo item é **verbatim** da LOB (finalidade e/ou incisos), com citação `cf. CBMxx, LOB
  (Lei …), Art. N`. Nada parafraseado/inventado.
- Itens de RI não entram na camada LOB.
- Coluna 2 passa a "Curado" onde há entrada LOB; coluna 3 = LOB + RI (união rotulada).
- `organs_detail/*.json`, `comparativo_dpo_cot.json` e `ENRICHMENT_ORGAN` intocados.
- Build reproduzível; suíte JS (`node --test src/lib/minutaArticles.test.js`) verde.

## Casos de borda (aceitáveis)

- Estado cuja LOB remete a estrutura a decreto/RI (ex.: AP LC 180/2026) e não descreve o
  órgão: sem entrada LOB para aquele par — documentado.
- Órgão do RO sem equivalente na LOB de um estado: idem.
- LOB que só traz finalidade (sem incisos): entra só a finalidade (é o ganho principal).

## Fora de escopo

- Página **Detalhe do Estado** / `organs_detail` (Path A foi descartado): não muda.
- Wizard `/minuta` e `/minuta-diagramas`: não dependem desta camada.
- Reescrever a curadoria de RI da Frente 2: preservada e apenas somada.

## Testes

- Suíte JS existente (`src/lib/minutaArticles.test.js`) — deve seguir verde.
- Verificação manual de reprodutibilidade do build Python (sem suíte no pipeline de dados).
- Diff dirigido confirmando natureza aditiva (nenhuma linha removida de camadas pré-existentes;
  `organs_detail`/`dpo_cot` fora do diff).
- Após Task 0, validação visual das 3 colunas em http://localhost:5173 com 1–2 estados de
  amostra.

## Documentação

Nova seção em `docs/ENRIQUECIMENTO_MINUTA.md` ("Camada LOB — `/comparar`, 2026-06-28")
registrando o critério relaxado (finalidade admitida), o escopo (26 órgãos × 27 estados) e,
por lote, as LOBs aproveitadas e os pares sem equivalente (com motivo). `CLAUDE.md` atualizado
para descrever a camada `lob_enrichment.py` e a semântica "LOB + RI" da coluna 3.
