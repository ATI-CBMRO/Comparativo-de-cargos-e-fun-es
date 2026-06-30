# Estrutura interna dos órgãos-folha no organograma da minuta (`/minuta-diagramas`)

**Data:** 2026-06-30
**Status:** Aprovado (design) — aguardando plano de implementação

## Problema

No organograma da minuta (`/minuta-diagramas`, `MinutaOrgChart.jsx`), apenas **DPO**
e **DOE** mostram expansão visual (botão −/+), porque COT/CRBM e BBS/BIFEA/BOA são
órgãos do `ORGAN_ORDER` da minuta apontando para eles via `subordinadoA`. Os demais
18 órgãos (DP, DEEI, DPOF, DSAP, DLOG, CINT, CCS, CINF, CONDEG, DEPDEC,
CORREGEDORIA, CAT, CIBM, GBM, GAB-CG, AG, ASSESSORIAS, e os batalhões/CRBM que já
são folhas terminais) aparecem como caixas planas, dando a impressão de que só
DPO/DOE têm estrutura — quando, na realidade, **todo órgão do `ro.json` já tem
`desdobramentos`** (Diretor, Adjunto, Coordenadorias, Seções etc.) descrevendo sua
composição interna pela LOB.

## Objetivo

Fazer os órgãos-folha (sem filhos de órgão) do `commandChart` exibirem sua estrutura
interna (`desdobramentos` do `ro.json`) como nós filhos expansíveis no organograma da
minuta, sem alterar o comportamento de DPO/DOE/COT/CRBM/BBM/BBS/BIFEA/BOA (que já têm
filhos de órgão reais).

## Não-objetivos

- Não alterar órgãos que já têm filhos de órgão no `commandChart` (DPO, DOE, COT,
  CRBM, BBM, BBS, BIFEA, BOA) — ficam exatamente como hoje.
- Não alterar o Mapa Mental (`MinutaMindMap.jsx`) nem o `/comparar`
  (`OrgTreeNode`/`buildOrganTree`) — nenhum dos dois usa `commandChart`.
- Não trazer os 11 órgãos novos do organograma real do RO (`ai, ae, al, ap, apge, af,
  aci, comissoes, conselhos, gab-scg, gab-emg`, adicionados em
  `docs/superpowers/specs/2026-06-30-organograma-ro-orgaos-administrativos-design.md`)
  para o `ORGAN_ORDER` da minuta — são órgãos do organograma real do RO, fora do
  escopo dos 26 órgãos da LOB cobertos pela minuta.
- Não criar um novo nível de profundidade dentro das Coordenadorias/Seções listadas
  num único `desdobramento` (ex.: a string completa de "Coordenadoria de Gestão de
  Pessoal Ativo — Coordenador, Adjunto, Seção Administrativa, Seção de Pessoal
  Ativo, ...") — cada `desdobramento` se torna **um** nó, com o texto truncado no
  primeiro separador " — "/" – ", sem desmembrar a lista interna em mais nós.

## Mudanças

### a) `scripts/build_minuta_structure.py` — `build_command_chart()`

Depois de montar a árvore de órgãos pela subordinação (loop existente que preenche
`nodes[p]["children"]`) e antes de tratar a Guarnição/raiz, percorrer todos os nós e,
**somente para os que ficaram sem filhos** (`not n["children"]`), buscar
`organs.get(k, {}).get("desdobramentos") or []` e anexar cada item como nó filho
estrutural:

```python
for k, n in nodes.items():
    if n["children"]:
        continue  # já tem filhos de órgão (DPO, DOE, COT, CRBM, BBM, BBS, BIFEA, BOA)
    desdobramentos = (organs.get(k) or {}).get("desdobramentos") or []
    for desd in desdobramentos:
        label = re.split(r"\s+[—–]\s+", desd, maxsplit=1)[0].strip()
        n["children"].append({
            "organKey": None, "sigla": "", "label": label,
            "structural": True, "isInternal": True,
            "chapterId": None, "children": [],
        })
```

- `isInternal: True` distingue esses nós dos estruturais já existentes na cadeia de
  frações do BBM (Cia BM / Pel BM), que continuam sem essa flag.
- O truncamento usa regex (`—` em dash ou `–` en dash, já usados no `ro.json`) para
  extrair só o nome da unidade, descartando a enumeração de cargos/seções internas
  que vem depois do separador.
- Roda **antes** do bloco que processa `guarnicao`/`bbm` (que já lida com `nodes["bbm"]`
  separadamente — `bbm` não fica "sem filhos" depois desse bloco rodar primeiro, então a
  ordem importa: o loop de `desdobramentos` deve rodar **antes** de popular a cadeia
  Cia BM → Pel BM → Guarnição, para não marcar `bbm` como folha indevidamente).

### b) `src/components/MinutaOrgChart.jsx`

Adicionar a classe `moc-box-internal` quando `node.isInternal`:

```jsx
const cls = `moc-box${node.synthetic ? ' moc-box-root' : ''}${node.isInternal ? ' moc-box-internal' : ''}${selected ? ' moc-box-sel' : ''}`
```

Nenhuma outra mudança — `clickable` já é `false` para nós sem `chapterId` (renderiza
`<div>`), e `showToggle`/`hasKids` já funcionam para qualquer nó com `children`.

### c) `src/index.css`

Nova regra `.moc-box-internal`: fonte menor, borda tracejada, fundo neutro — visualmente
mais leve que `.moc-box` padrão (que representa órgãos reais e abre painel ao clicar).

## Fluxo de dados

`ro.json` (`desdobramentos` por órgão) → `build_command_chart()` injeta nós
`isInternal` nos órgãos-folha do `commandChart` → `minuta_structure.json` →
`MinutaOrgChart.jsx` renderiza com estilo `.moc-box-internal` → toggle −/+ já
funciona (herdado do mecanismo existente); fechado por padrão.

## Riscos e verificação

### Risco — marcar `bbm` como folha antes da cadeia de frações ser anexada
Mitigado pela ordem: o loop de injeção de `desdobramentos` roda **antes** do bloco
`if guarnicao is not None and "bbm" in nodes`. Verificação: após o build, `bbm` deve
ter como filho a cadeia "Cia BM" (estrutural, sem `isInternal`), não os
`desdobramentos` truncados do próprio BBM.

### Risco — duplicar visualmente nós que já são órgãos
Não se aplica: a injeção só ocorre em nós **sem filhos de órgão**, então DPO/DOE/COT/
CRBM/BBM/BBS/BIFEA/BOA (que têm filhos reais) nunca recebem nós internos.

### Verificação funcional
1. Asserção Python sobre `minuta_structure.json`: para uma amostra de órgãos-folha
   (`dp`, `deei`, `dpof`, `dsap`, `dlog`, `cint`, `ccs`, `cinf`, `condeg`, `depdec`,
   `corregedoria`, `cat`, `cibm`, `gbm`, `gab-cg`, `ag`, `assessorias`), `children`
   não-vazio e cada filho com `isInternal: true`.
2. Para `dpo`/`doe`/`cot`/`crbm`/`bbm`/`bbs`/`bifea`/`boa`: nenhum filho com
   `isInternal: true` (children, se houver, são órgãos reais ou a cadeia BBM).
3. Visual: abrir `/minuta-diagramas`, expandir DP (antes flat) — deve aparecer
   "Diretor", "Adjunto", "Seção Administrativa", "Coordenadoria de Gestão de Pessoal
   Ativo" etc., com estilo mais leve que os órgãos. DPO/DOE seguem mostrando só seus
   órgãos-filhos (COT/CRBM, BBS/BIFEA/BOA), sem itens internos adicionados.
4. Impressão (`window.print()`): expandir tudo e confirmar que os nós internos
   aparecem na página impressa sem quebrar o layout.

## Testes

Não há suíte de testes de dados no projeto. Verificação via asserção Python
(ponto 1-2 acima) + inspeção visual (pontos 3-4).
