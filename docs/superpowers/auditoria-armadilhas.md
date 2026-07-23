# Registro de armadilhas — checklist da auditoria final

> Propósito: catalogar CLASSES de falha detectadas durante o planejamento/execução do
> cockpit de curadoria (e correlatos), para que a **auditoria final** — rodada ao término
> da implementação — cace ativamente cada classe em TODO o trabalho produzido, não só onde
> já foi vista. Toda correção fecha com varredura de casos análogos (regra do CLAUDE.md
> global). Este arquivo é versionado e cresce a cada armadilha nova encontrada.

## Como a auditoria final usa este arquivo

Para cada classe abaixo, a auditoria deve: (1) reproduzir o método de detecção; (2) varrer
TODOS os pontos onde a classe pode ocorrer (não só o caso original); (3) reportar quantos
foram encontrados e corrigidos; (4) se achar uma classe nova, registrá-la aqui.

---

## AR-01 · Casamento semântico errado por semelhança de nome

**O que é:** associar dois itens (órgãos, temas, tipos de documento, fontes) só porque os
NOMES se parecem, sem conferir o CONTEÚDO — e os conteúdos serem coisas diferentes.

**Caso original (2026-07-22, planejamento Fase 1):** no de-para do Regimento atual→futura,
propus `cob1 → cot` porque ambos têm "Operações" no nome. Ao ler o conteúdo real:
- **COB (atual)** = Comando Operacional de Bombeiros — operação/socorro, atividade-fim,
  agrega Grupamentos (comando operacional regional).
- **COT (futura)** = Comando de Operações **Técnicas** — segurança contra incêndio e pânico,
  análise de edificações (engenharia de prevenção). Nada a ver com socorro.
- Correção: **COB I e COB II → CRBM** (Comandos Regionais); o COT já é coberto por `cat→cat`.

**Método de detecção:** para cada par mapeado, abrir a **finalidade/competência real** dos
dois lados e confirmar que a MATÉRIA é a mesma — nunca decidir pelo rótulo.

**Onde a auditoria deve varrer (não só o de-para do cob):**
- de-para de órgãos do Regimento atual↔futura (todos os 19 pares, não só cob).
- `AUTO_MATCH_KEYWORDS`/`AUTO_MATCH_KEYWORDS_ATUAL` (casamento por palavra-chave — mesma
  armadilha: "operações" casa COT e COB; "técnicas" casa CAT e COT; etc.).
- Classificação de tipo de documento por nome de arquivo (`parse_doc_type` e overrides).
- `PRIMARY_SOURCE`/temas do Regulamento (fonte primária de cada tema).
- Qualquer lugar onde um id/rótulo é usado como chave de associação.

**Instância #2 (achada pela auditoria da Fase 1, 2026-07-22):** `AUTO_MATCH_KEYWORDS_ATUAL["cob1"]`
em `build_minuta_comparison_atual.py` (tabela do Subsídio atual) casava o organ **cot**
(Comando de Operações **Técnicas** / segurança contra incêndio) porque o include "comando de
operacoes" pegava "Comando de Operações Técnicas" e o exclude só tinha "atividades tecnicas".
Corrigido: acrescentado "operacoes tecnicas"/"operacao tecnica" ao exclude do cob1 (cob2 não
tinha o problema — include por "regional"). Regenerado `comparativo_minuta.json` do atual;
`match_ids('cob1', {cot}) → []` confirmado.

**Status:** caso original (de-para) e instância #2 (keyword-match do Subsídio atual) CORRIGIDOS
em 2026-07-22. Varreduras restantes conferidas na auditoria da Fase 1 (fase1-final-review.md):
`DEPARA_BLOCO_D` 19/19 ok; `AUTO_MATCH_KEYWORDS` da futura sem colisão; `parse_doc_type`+overrides
0 suspeitos. **Reexecutar as 3 varreduras a cada nova fase.**

---

## AR-02 · Parâmetro aceito mas ignorado → fallback silencioso para a fonte errada

**O que é:** uma função aceita um parâmetro que deveria selecionar a FONTE (documento,
arquivo, cenário), mas o ignora para parte dos casos e cai num default — sem erro, sem
aviso. O resultado é plausível (mesmo estado, mesmo nº de artigo), só que do documento
ERRADO.

**Caso original (2026-07-23, auditoria Rodada 1):** `md_for(uf, doc)` em
`scripts/extrair_ri_alternativas.py` só honrava `doc` para `uf == 'pr'`; para os demais
devolvia sempre `MD_FILE[uf]` (o RI). A CITATION do `dpo` dizia `('pa', 'lob', [16])` —
e o extrator capturou o Art. 16 do **RI do Pará** em vez da **LOB (Lei 11.060/2025)**.
O bug ficou invisível porque o RI também tem um Art. 16 (verbatim de outro documento
passa em qualquer verificação que não confira o documento). Detectado pelo Wândrio a
olho (excerto não batia com a lei citada) e pela auditoria na varredura completa.

**Correção:** mapa explícito `LOB_MD` + `KeyError` alto quando a LOB do estado não está
mapeada — proibido cair no RI em silêncio. Regeneração verbatim (minúsculas do OCR do PA
preservadas — a correção manual da manhã tinha capitalizado o texto, commit cabf7fb).

**Método de detecção:** para cada citação `source`, resolver o DOCUMENTO reivindicado
(tipo + nº da lei) e verificar o texto verbatim CONTRA ELE — e, se falhar, procurar nos
demais documentos do estado: achado em outro = classe AR-02. Automatizado em
`scripts/auditoria_citacoes.py` (1605 excertos: 1569 estritos, 24 com ruído de página,
12 exceções documentadas em whitelist, 0 falhas).

**Onde varrer (além do caso original):**
- Toda função `*_for(x, y)`/resolvedor com branch por caso especial (`if uf == 'pr'`) —
  o que acontece com os valores fora do branch?
- `scenarioDbUrl`/gavetas de cenário (a MESMA forma: parâmetro que escolhe fonte).
- `.get(chave, default)` onde o default é uma fonte alternativa "parecida".

**Status:** caso original CORRIGIDO em 2026-07-23 (extrator + regeneração dos 4 JSONs);
varredura completa das citações roda em `scripts/auditoria_citacoes.py`.

---

## Diretriz geral para a auditoria (independe de classe)

- Verbatim: todo excerto exibido deve bater caractere a caractere com a fonte; defeitos de
  OCR preservados, não limpos.
- Contagens "ao centavo": todo número afirmado (órgãos, dispositivos, excertos) reconferido
  por comando.
- Isolamento de cenário: nenhum conteúdo da futura vaza no texto do RO do atual.
- Nada de buraco silencioso: onde falta dado, a tela/relatório diz — não esconde.
