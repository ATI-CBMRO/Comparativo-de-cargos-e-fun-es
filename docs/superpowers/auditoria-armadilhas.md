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

## Diretriz geral para a auditoria (independe de classe)

- Verbatim: todo excerto exibido deve bater caractere a caractere com a fonte; defeitos de
  OCR preservados, não limpos.
- Contagens "ao centavo": todo número afirmado (órgãos, dispositivos, excertos) reconferido
  por comando.
- Isolamento de cenário: nenhum conteúdo da futura vaza no texto do RO do atual.
- Nada de buraco silencioso: onde falta dado, a tela/relatório diz — não esconde.
