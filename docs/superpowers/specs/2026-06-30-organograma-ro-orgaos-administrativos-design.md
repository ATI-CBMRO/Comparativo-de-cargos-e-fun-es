# Desdobramento dos órgãos administrativos do RO no organograma (`/estados/ro`)

**Data:** 2026-06-30
**Status:** Aprovado (design) — aguardando plano de implementação

## Problema

No organograma do RO (`/estados/ro`), ao clicar nos órgãos do lado
**administrativo** (Assessorias, Apoio, Correição) o usuário recebe
"Detalhamento completo não disponível", enquanto o lado **operacional**
(DPO, COT, diretorias, batalhões) abre painel rico. Isso dá a impressão de que
"só DPO e COT" estão desenvolvidos.

### Causa raiz

O painel (`OrgDetail.jsx`) renderiza genericamente qualquer órgão que tenha
`cargos`/`desdobramentos`/`atribuicoes`. O detalhe é resolvido pelo `detailId`
carimbado em cada nó da árvore por `enrich_tree_from_detail()`
(`scripts/build_states_data.py`), que casa o nó da árvore curada com um órgão de
`database/organs_detail/ro.json` por **id → sigla → nome → tokens**.

Mapeando os nós "reais" da árvore do RO contra o detalhe:

- **22 nós casam** e abrem painel (incl. DPO, COT e **todas as diretorias**).
- **Não casam (ficam mudos):**
  - **7 Assessorias** (ids `ai, ae, al, ap, apge, af, aci`) — o detalhe só tem
    um órgão **combinado** `assessorias`; "Assessoria Institucional" não casa
    com "Assessorias" (plural) nem por nome nem por tokens.
  - **Órgãos de Correição** (id de nó `correg`) — o detalhe existe como
    `corregedoria`, mas id/nome não casam.
  - **Comissões, Conselhos, Gabinete do Subcomando-Geral, Gabinete do EMG**
    (ids de nó `comissoes, conselhos, gab-scg, gab-emg`) — **não há** órgão de
    detalhe correspondente no `ro.json`.

A própria Minuta da LOB do RO (`database/markdown/Rondônia - Minuta de Lei de
Organização Básica.md`) **enumera verbatim** as competências de todos esses
órgãos (Arts. 7-10 e 30-38), então há fonte legítima para completá-los sem
recorrer a material de outros estados.

## Objetivo

Fazer **todos** os órgãos administrativos do RO abrirem painel de detalhe no
`/estados/ro`, com competências **verbatim da Minuta da LOB do RO**. Não tocar
o lado operacional (já funciona) nem importar estrutura de outros estados (isso
seria fabricação no organograma *real* do RO — distinto da `/minuta`, que é uma
proposta).

## Não-objetivos

- Não importar estrutura/competência de outros CBMs para o organograma do RO.
- Não alterar `/minuta`, nem a lógica do `/comparar` (apenas verificar
  não-regressão).
- Não alterar `OrgDetail.jsx` / `Organogram.jsx` (já renderizam genericamente).
- Não aprofundar internamente os órgãos além do que a LOB do RO descreve.

## Mudanças

### a) `database/organs_detail/ro.json` (escrito à mão; nenhum script o regenera)

Verificado: `build_organs_detail.py` e os `detail_data_g*.py`/`detail_cargos_g*.py`
**não** têm entrada "ro" — editar o JSON diretamente é seguro.

1. **Adicionar** 7 órgãos de assessoria individuais, com ids casando os nós da
   árvore (`ai, ae, al, ap, apge, af, aci`), `category: "Assessoramento"`,
   `subordinadoA: "Comandante-Geral"`, `artigosDeOrigem: ["Art. 7º", "Art. 30"]`.
   **Manter** o órgão combinado `assessorias` (hoje dormente no organograma, mas
   consumido por id exato pela coluna RO do `/comparar` —
   `build_reference("assessorias")` em `build_minuta_comparison.py:114-119`).
   Competência verbatim do **Art. 30 §1º** para os 7 individuais:
   - `ai` Assessoria Institucional, `ae` Especial, `al` Legislativa,
     `ap` Parlamentar, `apge` de Projetos e Gestão Estratégica,
     `aci` de Controle Interno → texto integral do inciso correspondente.
   - `af` Assessoria **Fundacional** → a LOB **não enumera** competência
     ("Assessoria Fundacional; e"). Fica só com o caput do Art. 30; `atribuicoes`
     vazio + nota "Sem competência detalhada na LOB". **Não inventar.**
2. **Adicionar** 4 órgãos de apoio inexistentes no detalhe, ids casando a árvore:
   - `comissoes` (Art. 32) — competência + composição (Presidente, Secretário,
     Membros); cita as comissões permanentes (Promoção de Oficiais, Promoção de
     Praças).
   - `conselhos` (Arts. 33-35) — Conselhos de Justificação e Disciplina, de Ética
     e Disciplina Militares e de Condecorações; competência verbatim, registrando
     que composição/atribuições são "fixadas em legislação específica".
   - `gab-scg` (Art. 36) — Gabinete do Subcomando-Geral; competência + composição
     (Chefia de Gabinete, Secretaria, Ajudância de Ordens).
   - `gab-emg` (Art. 38) — Gabinete do Estado-Maior Geral; competência +
     composição (Chefia de Gabinete, Secretaria, Ajudante de ordens).
3. Inalterados: `corregedoria` (Art. 10), `gab-cg` (Art. 31), `ag` (Art. 37).

### b) `scripts/curated_organs.py` (árvore do RO, bloco `"ro": [...]`)

- Trocar o id do nó de Correição de `correg` → `corregedoria` (linha ~89) para
  casar com o detalhe `corregedoria`. Nome exibido permanece "Órgãos de
  Correição".
- Os 7 nós de assessoria e os 4 de apoio **já têm os ids corretos**; casam por id
  assim que os órgãos existirem no `ro.json`. Nenhuma outra alteração na árvore.
- (Opcional, cosmético) aproximar os `desc` das categorias `assess`/`apoio`/`exec`
  do texto dos Arts. 7/8/9.

### Regeneração

Rodar **apenas** `python scripts/build_states_data.py` (lê `ro.json` + árvore
curada, re-carimba `detailId` e injeta desdobramentos como filhos `_reg`).
**Não** rodar `build_organs_detail.py` (regeneraria os demais estados a partir
dos g*.py e ignoraria o RO de qualquer forma).

## Fluxo de dados

LOB markdown (fonte) → editar `ro.json` (7 assessorias + 4 apoio) + id da
Correição em `curated_organs.py` → `build_states_data.py`
(`enrich_tree_from_detail` re-carimba `detailId` nos 7+4+1 nós) →
`states_data.json` → `StateDetail`/`Organogram`/`OrgDetail` abrem os painéis.

## Riscos e verificação

### Risco principal — não regredir o `/comparar` (mitigado por construção)
A coluna RO do `/comparar` é montada por `build_reference(organ_key, ro_organs)`
com **busca por id exato** (`ro_organs[organ_key]`,
`build_minuta_comparison.py:114-119`); o `auto_match` por palavra-chave **não**
roda para o RO (só estados não-curados, `build_minuta_comparison.py:205-214`). E
`build_dpo_cot_comparison.py` usa mapas explícitos `DPO_MAP`/`COT_MAP`, que nem
tocam `assessorias`.

Portanto, **mantendo** o órgão combinado `assessorias` (e apenas *adicionando* os
7 individuais + 4 de apoio, cujos ids não são organ_keys do comparador), a saída
do `/comparar` fica inalterada por construção.

**Critério de pronto (guarda de regressão):** snapshot de `comparativo_minuta.json`
e `comparativo_dpo_cot.json` antes; regenerar
`python scripts/build_dpo_cot_comparison.py` e
`python scripts/build_minuta_comparison.py` depois; **diff vazio** em ambos.

### Fidelidade ao texto
Só texto verbatim da LOB. Onde a lei remete a "legislação específica" (Conselhos)
ou não enumera (Assessoria Fundacional), registrar o caput e sinalizar a lacuna —
sem fabricar.

### Verificação funcional
1. Script Python de asserção sobre `states_data.json` (RO): os **12 nós-alvo**
   passam a ter `detailId` — `ai, ae, al, ap, apge, af, aci` (assessorias),
   `corregedoria` (Correição), `comissoes, conselhos, gab-scg, gab-emg` (apoio).
   Os nós de **categoria** (`assess, apoio, exec, ap-cg, ap-scg, ap-emg, ap-set`
   e os rótulos de execução) permanecem sem `detailId` por serem agrupadores —
   comportamento esperado, não falha.
2. Subir o dev server em http://localhost:5173, abrir `/estados/ro` e clicar
   cada órgão antes mudo (7 assessorias, Correição, Comissões, Conselhos,
   Gabinete SCG, Gabinete EMG), conferindo painel com texto da LOB.
3. Diff vazio nos comparativos do `/comparar` (risco principal acima).

## Testes

Não há suíte de testes de dados no projeto. A verificação é a do bloco acima
(asserção Python + inspeção visual + diff de regeneração).

## Texto verbatim de referência (fonte: Minuta LOB RO)

- **Art. 7º** (caput Assessoramento), **Art. 8º** (Apoio), **Art. 9º** (Execução),
  **Art. 10** (Correição/Corregedoria-Geral).
- **Art. 30 §1º, I-VII** — competências das 7 assessorias (VI Fundacional sem
  texto).
- **Art. 32** (Comissões), **Arts. 33-35** (Conselhos), **Art. 36** (Gabinete
  SCG), **Art. 38** (Gabinete EMG).
