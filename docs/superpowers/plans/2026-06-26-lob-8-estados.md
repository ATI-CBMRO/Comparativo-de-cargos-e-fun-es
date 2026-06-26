# Curar a LOB dos 8 estados com LOB+RI fundidos — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Curar a Lei de Organização Básica (LOB) de 8 estados (AM, DF, GO, MT, PA, PR, RS, SE) como uma camada nova de entradas `source:"lob"` em `organs_detail`, sem tocar na curadoria mesclada existente, para viabilizar a futura 3ª coluna "LOB do estado" no comparativo (Sub-projeto B, fora deste plano).

**Architecture:** Reusa o padrão já executado e mergeado para AL/ES (Sub-projeto 1). Para cada estado, adicionam-se entradas de órgão com ids `<sigla>-<uf>-lob` e campo `source:"lob"` no `detail_data_g*.py` correspondente, extraídas do markdown de LOB daquele estado, mais o cargo do Comandante-Geral no `detail_cargos_g*.py`. O `build_organs_detail.py` já repassa o campo `source` para o JSON sem mudança de código (confirmado no Sub-projeto 1). Nenhuma lógica de pipeline ou frontend muda neste plano.

**Tech Stack:** Python 3.14, dicts em `scripts/detail_data_g*.py` / `detail_cargos_g*.py`, pipeline `build_organs_detail.py` → `build_states_data.py`. Sem suíte de testes; verificação por asserções Python ad-hoc sobre os dicts e o JSON gerado.

---

## Receita de curadoria (compartilhada por todas as tarefas de estado)

Cada tarefa de estado segue esta receita. Leia-a inteira antes de começar.

**Fonte:** o markdown de LOB do estado, em `database/markdown/<arquivo>.md` (caminho exato em
cada tarefa). Esse arquivo tem o texto da lei; os artigos que enumeram a estrutura começam
com algo como *"Os órgãos de direção … são: I - …; II - …"* e cada órgão tem um artigo com
sua finalidade/competência.

**Exemplar de formato (FONTE DE VERDADE do shape):** os blocos `*-al-lob` em
`scripts/detail_data_g1.py` e a entrada `cg-al-lob` em `scripts/detail_cargos_g1.py` (já
commitados, do Sub-projeto 1). Abra-os e copie EXATAMENTE a forma. Um órgão tem este shape:

```python
    "<sigla>-<uf>-lob": {
      "name": "<nome do órgão>", "abbreviation": "<sigla>", "category": "<Direção Geral|Direção Setorial|Apoio|Execução|Especial>", "source": "lob",
      "subordinadoA": "<a quem se subordina>", "legalRef": "<Art. N>",
      "baseLegal": "<lei do estado> (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. N (…)"],
      "atribuicoes": [
        "<finalidade/competência do órgão, VERBATIM ou transcrição fiel do texto da LOB>"
      ],
      "desdobramentos": ["<subdivisões nomeadas no texto>"],
      "cargos": []
    },
```

**Regras de conteúdo:**
- **Ids:** `<sigla>-<uf>-lob` (ex.: `cg-am-lob`, `em-df-lob`, `dat-go-lob`). Todos terminam
  em `-lob`. NÃO podem colidir com ids existentes do estado (que não têm o sufixo `-lob`).
- **`source: "lob"`** em toda entrada nova (órgão). Obrigatório — é o que o Sub-projeto B
  filtra.
- **`baseLegal`** cita a lei correta do estado (string exata em cada tarefa), sufixada por
  `(Lei de Organização Básica)`.
- **`atribuicoes`:** transcrição FIEL do texto da LOB (finalidade/competência do órgão).
  Onde a lei enumera por inciso, transcreva verbatim com o inciso entre parênteses; onde é
  prosa, transcreva a prosa fielmente. NÃO inventar listas (convenção do projeto, CLAUDE.md).
- **`desdobramentos`:** as subdivisões nomeadas no texto (seções, subunidades). Lista de
  strings; pode ser `[]` se a LOB não detalhar.
- **Profundidade:** cobrir os órgãos de **direção** (geral e setorial), **apoio** e
  **execução** nomeados na enumeração estrutural da LOB. Não descer a cada seção interna.
- **Cargo do Comandante-Geral:** no `detail_cargos_g*.py`, sob a chave do estado, adicionar
  uma entrada com a chave de órgão `cg-<uf>-lob` (ou o id que você deu ao Comando/Comandante
  Geral), contendo 1 cargo "Comandante-Geral"/"Comandante Geral" com `atribuicoes` verbatim
  se a LOB as enumerar, ou transcrição fiel da prosa caso contrário.

**Localização da edição (data):** dentro de `scripts/detail_data_g<N>.py`, encontre o bloco
`"<uf>": { … "organs": { … } }`. Insira os novos órgãos ANTES do `}` que fecha o dict
`"organs"` do estado (acrescentando vírgula após o `}` do último órgão existente). Para achar
o ponto exato, abra o arquivo e localize o último órgão do estado e o fechamento `  }` +
`},` do bloco do estado.

**Localização da edição (cargos):** em `scripts/detail_cargos_g<N>.py`, dentro do bloco
`"<uf>": { … }`, adicione a chave `"cg-<uf>-lob": [ {…} ]` antes do `}` que fecha o estado.

**Verificação por estado (rode após editar, ajustando `<uf>` e `<N>`):**

```bash
cd "c:\Users\tiago\OneDrive\Documentos\Comparativo de legislações CBM"
python -c "
import sys; sys.path.insert(0, 'scripts')
from detail_data_g<N> import DATA
from detail_cargos_g<N> import CARGOS
ids = list(DATA['<uf>']['organs'].keys())
lob = [i for i in ids if i.endswith('-lob')]
assert len(ids) == len(set(ids)), 'ids duplicados!'
assert len(lob) >= 5, f'esperado >=5 orgaos -lob, achei {len(lob)}'
assert all(DATA['<uf>']['organs'][i].get('source')=='lob' for i in lob), 'orgao -lob sem source'
old = [i for i in ids if not i.endswith('-lob')]
assert all(DATA['<uf>']['organs'][i].get('source') != 'lob' for i in old), 'orgao antigo marcado lob'
cg = [k for k in CARGOS['<uf>'] if k.endswith('-lob')]
assert cg, 'cargo do Comandante-Geral -lob ausente'
print('OK', '<uf>', '|', len(lob), 'orgaos lob |', len(old), 'antigos preservados | cargos-lob:', cg)
"
```

Expected: `OK <uf> | <N> orgaos lob | <M> antigos preservados | cargos-lob: [...]` sem erro.
(O mínimo `>=5` é conservador; a maioria dos estados terá mais. Se um estado tiver genuinamente
menos de 5 órgãos na LOB, reporte DONE_WITH_CONCERNS em vez de forçar.)

**Não faça:** não rode `build_organs_detail.py` nem `build_states_data.py` (é a Task 9). Não
toque em outros estados. Não toque nas entradas existentes (sem `-lob`). Há 8 arquivos
markdown pré-existentes modificados no working tree (Acre, Ceará etc.) — não os toque.

---

### Task 1: Amazonas (AM)

**Files:** Modify `scripts/detail_data_g1.py` (bloco `"am"`), `scripts/detail_cargos_g1.py` (bloco `"am"`)

- [ ] **Step 1:** Ler `database/markdown/Amazonas - Organização Básica.md` (Lei nº 2.538/1999). Estrutura-chave (Art. 8 órgãos de direção geral): **Comando Geral, Coordenadoria Estadual de Defesa Civil (CEDEC), Conselho Superior de Políticas Estratégicas (CSPE), Gabinete, Ajudância Geral (AG), Comissões**; mais órgãos de **direção setorial** (Diretorias), **apoio** e **execução** nomeados adiante no texto. Curar cada um seguindo a Receita.
- [ ] **Step 2:** Inserir os órgãos `*-am-lob` em `scripts/detail_data_g1.py` (bloco `"am"` → `"organs"`), `baseLegal = "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)"`.
- [ ] **Step 3:** Inserir o cargo `cg-am-lob` (Comandante Geral) em `scripts/detail_cargos_g1.py` (bloco `"am"`), atribuições verbatim/fiéis ao texto.
- [ ] **Step 4:** Verificar com o bloco da Receita (`<uf>=am`, `<N>=1`). Expected: `OK am | …`.
- [ ] **Step 5:** Commit:
```bash
git add scripts/detail_data_g1.py scripts/detail_cargos_g1.py
git commit -m "data(am): cura estrutura da LOB (Lei nº 2.538/1999) como camada source:lob"
```

---

### Task 2: Distrito Federal (DF)

**Files:** Modify `scripts/detail_data_g2.py` (bloco `"df"`), `scripts/detail_cargos_g2.py` (bloco `"df"`)

- [ ] **Step 1:** Ler `database/markdown/Distrito Federal - Organização Básica.md` (Lei nº 8.255/1991, com alterações). Estrutura-chave: órgãos de **direção** (Comando-Geral, **Estado-Maior-Geral**, Diretorias/direção setorial), **apoio** (Art. 24: **Academia de Bombeiros Militar, Policlínicas, Centros, Colégio Militar Dom Pedro II**), **execução** (Art. 28: **Comando Operacional, Unidades** …). Curar seguindo a Receita.
- [ ] **Step 2:** Inserir os órgãos `*-df-lob` em `scripts/detail_data_g2.py` (bloco `"df"`), `baseLegal = "Lei nº 8.255, de 20 de novembro de 1991 (Lei de Organização Básica)"`.
- [ ] **Step 3:** Inserir o cargo `cg-df-lob` (Comandante-Geral) em `scripts/detail_cargos_g2.py` (bloco `"df"`).
- [ ] **Step 4:** Verificar (`<uf>=df`, `<N>=2`). Expected: `OK df | …`.
- [ ] **Step 5:** Commit:
```bash
git add scripts/detail_data_g2.py scripts/detail_cargos_g2.py
git commit -m "data(df): cura estrutura da LOB (Lei nº 8.255/1991) como camada source:lob"
```

---

### Task 3: Goiás (GO)

**Files:** Modify `scripts/detail_data_g3.py` (bloco `"go"`), `scripts/detail_cargos_g3.py` (bloco `"go"`)

- [ ] **Step 1:** Ler `database/markdown/Goiás - Organização Básica (Lei 18.305-2013).md`. Estrutura-chave (Art. 4): **órgãos de direção, de apoio e de execução**; curar os órgãos nomeados em cada categoria (Comando-Geral/Estado-Maior, Diretorias, Comandos/Grupamentos regionais etc.). Usar APENAS o markdown da Lei 18.305/2013 (não o de Quadro de Organização). Seguir a Receita.
- [ ] **Step 2:** Inserir os órgãos `*-go-lob` em `scripts/detail_data_g3.py` (bloco `"go"`), `baseLegal = "Lei nº 18.305, de 30 de dezembro de 2013 (Lei de Organização Básica)"`.
- [ ] **Step 3:** Inserir o cargo `cg-go-lob` em `scripts/detail_cargos_g3.py` (bloco `"go"`).
- [ ] **Step 4:** Verificar (`<uf>=go`, `<N>=3`). Expected: `OK go | …`.
- [ ] **Step 5:** Commit:
```bash
git add scripts/detail_data_g3.py scripts/detail_cargos_g3.py
git commit -m "data(go): cura estrutura da LOB (Lei nº 18.305/2013) como camada source:lob"
```

---

### Task 4: Mato Grosso (MT)

**Files:** Modify `scripts/detail_data_g3.py` (bloco `"mt"`), `scripts/detail_cargos_g3.py` (bloco `"mt"`)

- [ ] **Step 1:** Ler `database/markdown/Mato Grosso - Organização Básica.md` (LC nº 775/2023). **ATENÇÃO:** usar o arquivo "Mato Grosso - …", NÃO "Mato Grosso do Sul - …" (são estados diferentes). Curar os órgãos de direção/apoio/execução da LOB seguindo a Receita.
- [ ] **Step 2:** Inserir os órgãos `*-mt-lob` em `scripts/detail_data_g3.py` (bloco `"mt"`), `baseLegal = "Lei Complementar nº 775, de 2023 (Lei de Organização Básica)"`.
- [ ] **Step 3:** Inserir o cargo `cg-mt-lob` em `scripts/detail_cargos_g3.py` (bloco `"mt"`).
- [ ] **Step 4:** Verificar (`<uf>=mt`, `<N>=3`). Expected: `OK mt | …`.
- [ ] **Step 5:** Commit:
```bash
git add scripts/detail_data_g3.py scripts/detail_cargos_g3.py
git commit -m "data(mt): cura estrutura da LOB (LC nº 775/2023) como camada source:lob"
```

---

### Task 5: Pará (PA)

**Files:** Modify `scripts/detail_data_g4.py` (bloco `"pa"`), `scripts/detail_cargos_g4.py` (bloco `"pa"`)

- [ ] **Step 1:** Ler `database/markdown/Pará - Organização Básica.md` (Lei nº 11.060/2025; markdown grande, ~136k chars). Localizar os artigos que enumeram a estrutura (órgãos de direção/apoio/execução) e curar cada órgão nomeado seguindo a Receita.
- [ ] **Step 2:** Inserir os órgãos `*-pa-lob` em `scripts/detail_data_g4.py` (bloco `"pa"`), `baseLegal = "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)"`.
- [ ] **Step 3:** Inserir o cargo `cg-pa-lob` em `scripts/detail_cargos_g4.py` (bloco `"pa"`).
- [ ] **Step 4:** Verificar (`<uf>=pa`, `<N>=4`). Expected: `OK pa | …`.
- [ ] **Step 5:** Commit:
```bash
git add scripts/detail_data_g4.py scripts/detail_cargos_g4.py
git commit -m "data(pa): cura estrutura da LOB (Lei nº 11.060/2025) como camada source:lob"
```

---

### Task 6: Paraná (PR)

**Files:** Modify `scripts/detail_data_g4.py` (bloco `"pr"`), `scripts/detail_cargos_g4.py` (bloco `"pr"`)

- [ ] **Step 1:** Ler `database/markdown/Paraná - Organização Básica.md` (Lei nº 22.206/2020). Curar os órgãos de direção (Comando-Geral, Estado-Maior, Diretorias), apoio e execução nomeados na LOB seguindo a Receita.
- [ ] **Step 2:** Inserir os órgãos `*-pr-lob` em `scripts/detail_data_g4.py` (bloco `"pr"`), `baseLegal = "Lei nº 22.206, de 29 de novembro de 2020 (Lei de Organização Básica)"`.
- [ ] **Step 3:** Inserir o cargo `cg-pr-lob` em `scripts/detail_cargos_g4.py` (bloco `"pr"`).
- [ ] **Step 4:** Verificar (`<uf>=pr`, `<N>=4`). Expected: `OK pr | …`.
- [ ] **Step 5:** Commit:
```bash
git add scripts/detail_data_g4.py scripts/detail_cargos_g4.py
git commit -m "data(pr): cura estrutura da LOB (Lei nº 22.206/2020) como camada source:lob"
```

---

### Task 7: Rio Grande do Sul (RS)

**Files:** Modify `scripts/detail_data_g5.py` (bloco `"rs"`), `scripts/detail_cargos_g5.py` (bloco `"rs"`)

- [ ] **Step 1:** Ler `database/markdown/Rio Grande do Sul - Organização Básica.md`. **Nuance:** o texto é o **Decreto que regulamenta a LC nº 14.920/2016** (a LOB); a estrutura de órgãos está nele. Curar os órgãos seguindo a Receita; o `baseLegal` deve refletir essa origem.
- [ ] **Step 2:** Inserir os órgãos `*-rs-lob` em `scripts/detail_data_g5.py` (bloco `"rs"`), `baseLegal = "Decreto regulamentador da Lei Complementar nº 14.920, de 1º de agosto de 2016 (Lei de Organização Básica)"`.
- [ ] **Step 3:** Inserir o cargo `cg-rs-lob` (Comandante-Geral) em `scripts/detail_cargos_g5.py` (bloco `"rs"`).
- [ ] **Step 4:** Verificar (`<uf>=rs`, `<N>=5`). Expected: `OK rs | …`.
- [ ] **Step 5:** Commit:
```bash
git add scripts/detail_data_g5.py scripts/detail_cargos_g5.py
git commit -m "data(rs): cura estrutura da LOB (Decreto da LC nº 14.920/2016) como camada source:lob"
```

---

### Task 8: Sergipe (SE)

**Files:** Modify `scripts/detail_data_g5.py` (bloco `"se"`), `scripts/detail_cargos_g5.py` (bloco `"se"`)

- [ ] **Step 1:** Ler `database/markdown/Sergipe - Organização Básica (Lei 8.979-2022).md` (usar este, da Lei 8.979/2022 — NÃO o markdown "Sergipe - Organização Básica.md" antigo nem o RI). Curar os órgãos de direção/apoio/execução da LOB seguindo a Receita.
- [ ] **Step 2:** Inserir os órgãos `*-se-lob` em `scripts/detail_data_g5.py` (bloco `"se"`), `baseLegal = "Lei nº 8.979, de 03 de fevereiro de 2022 (Lei de Organização Básica)"`.
- [ ] **Step 3:** Inserir o cargo `cg-se-lob` em `scripts/detail_cargos_g5.py` (bloco `"se"`).
- [ ] **Step 4:** Verificar (`<uf>=se`, `<N>=5`). Expected: `OK se | …`.
- [ ] **Step 5:** Commit:
```bash
git add scripts/detail_data_g5.py scripts/detail_cargos_g5.py
git commit -m "data(se): cura estrutura da LOB (Lei nº 8.979/2022) como camada source:lob"
```

---

### Task 9: Rebuild da pipeline e verificação consolidada

**Files:** Generated: `database/organs_detail/{am,df,go,mt,pa,pr,rs,se}.json`, `database/states_data.json`

- [ ] **Step 1:** Rodar `build_organs_detail.py`:
```bash
cd "c:\Users\tiago\OneDrive\Documentos\Comparativo de legislações CBM"
python scripts/build_organs_detail.py 2>&1 | grep -E "am\.json|df\.json|go\.json|mt\.json|pa\.json|pr\.json|rs\.json|se\.json|Concluído"
```
Expected: uma linha `✓ <uf>.json — <N> órgãos detalhados` para cada um dos 8.

- [ ] **Step 2:** Verificar `source:"lob"` em cada JSON gerado e preservação das entradas antigas:
```bash
python -c "
import json
exp_old = {'am':19,'df':11,'go':15,'mt':11,'pa':12,'pr':19,'rs':10,'se':26}
for sid in ['am','df','go','mt','pa','pr','rs','se']:
    d = json.load(open(f'database/organs_detail/{sid}.json', encoding='utf-8'))
    organs = d['organs']
    lob = [k for k,v in organs.items() if v.get('source')=='lob']
    old = [k for k,v in organs.items() if v.get('source')!='lob']
    assert len(lob) >= 5, f'{sid}: so {len(lob)} lob'
    assert len(old) == exp_old[sid], f'{sid}: antigos {len(old)} != {exp_old[sid]} (entradas antigas alteradas!)'
    assert len(set(organs)) == len(organs), f'{sid}: ids duplicados'
    print(f'{sid}: {len(lob)} lob + {len(old)} antigos = {len(organs)} OK')
print('TODOS OK')
"
```
Expected: uma linha por estado + `TODOS OK`. Se `exp_old` divergir, alguma entrada antiga foi alterada — investigar antes de prosseguir.

- [ ] **Step 3:** Rodar `build_states_data.py` (regenera o JSON consumido pelo frontend):
```bash
python scripts/build_states_data.py 2>&1 | tail -2
```
Expected: `Estados: 27 | Documentos: 47 | …` e `Concluído.`

- [ ] **Step 4:** Confirmar que o diff de `states_data.json` não vazou para estados fora dos 8 (efeito dos 8 markdown pré-existentes modificados). Se aparecer `char_count` de estados não-alvo, isolar como no Sub-projeto 1:
```bash
git diff --stat database/states_data.json database/organs_detail/
```
Expected: apenas os 8 `organs_detail/<uf>.json` alvo + `states_data.json`. Se `states_data.json`
trouxer mudança de `char_count` de estados fora dos 8, repetir o procedimento do Sub-projeto 1:
`git stash push -- database/markdown/*.md`, `python scripts/build_states_data.py`, commitar, `git stash pop`.

- [ ] **Step 5:** Conferência visual (servidor em http://localhost:5173; iniciar com `npm run dev -- --port 5173 --strictPort` se preciso). Abrir 2–3 dos estados curados, ex.: http://localhost:5173/estados/df e http://localhost:5173/estados/se. Expected: organograma curado atual intacto (árvore visual vem de `curated_organs*.py`, não tocada), sem erros no console. Os órgãos `-lob` NÃO aparecem na árvore visual (esperado).

- [ ] **Step 6:** Commit dos artefatos gerados:
```bash
git add database/organs_detail/am.json database/organs_detail/df.json database/organs_detail/go.json database/organs_detail/mt.json database/organs_detail/pa.json database/organs_detail/pr.json database/organs_detail/rs.json database/organs_detail/se.json database/states_data.json
git commit -m "data(8 estados): regenera organs_detail e states_data com a curadoria LOB"
```

---

## Self-Review (preenchido na escrita do plano)

**Cobertura do spec:**
- Curar a LOB dos 8 estados mistos com ids `-lob` + `source:"lob"` → Tasks 1–8 (um por estado). ✓
- Fontes/markdown/g-file por estado → tabela do spec refletida em cada task (markdown path, g-file, baseLegal). ✓
- Cargo do Comandante-Geral por estado → Step 3 de cada task. ✓
- Não tocar entradas mescladas; ids sem colisão → asserções da Receita + Task 9 Step 2 (compara contagem de antigos com `exp_old`). ✓
- Rebuild + verificação + visual → Task 9. ✓
- Fora de escopo (comparativo, frontend, curated_organs) → explicitado na Receita e no spec; nenhuma task os toca. ✓

**Placeholder scan:** sem "TBD"/"implementar depois". O conteúdo verbatim de cada órgão não é
pré-escrito porque, por natureza, é extraído do markdown citado em cada task — a instrução é
completa e exemplificada (exemplar `*-al-lob` commitado) e verificável (asserções por estado).

**Consistência:** ids `<sigla>-<uf>-lob` e campo `source:"lob"` idênticos em todas as tasks e
no exemplar AL/ES; `exp_old` na Task 9 vem das contagens reais medidas (am 19, df 11, go 15,
mt 11, pa 12, pr 19, rs 10, se 26); `<N>` do g-file casa com a tabela do spec.
