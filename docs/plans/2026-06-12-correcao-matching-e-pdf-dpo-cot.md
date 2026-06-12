# Correção de Matching e PDF DPO×COT — Plano de Implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Corrigir dois bugs críticos: (1) falsos positivos no algoritmo de matching de cargos no Comparativo de Cargos; (2) PDF do DPO×COT que não exibe dados de Cargo/Função, Requisito/Posto e Subordinação.

**Architecture:** Dois patches cirúrgicos e independentes — nenhum envolve geração de dados Python nem novos arquivos. Bug 1 altera o conjunto de stopwords em `CargoComparator.jsx`. Bug 2 reescreve o componente `PrintReport` em `OrgaosOperacionaisComparator.jsx` para consumir os dados curados diretamente (eliminando o segundo nível de matching por nome de cargo que falha).

**Tech Stack:** React 18, Vite, JavaScript (sem TypeScript, sem suíte de testes). Verificação manual via `npm run dev` (http://localhost:5173).

---

## Diagnóstico Raiz

### Bug 1 — Comparativo de Cargos: matching falso-positivo

**Causa:** `tokenSet()` em `CargoComparator.jsx` trata palavras estruturais de cargo (`diretor`, `comando`, `coordenador`…) como tokens discriminativos. "Diretor de Planejamento Operacional" e "Diretor de Finanças" compartilham o token `diretor` → cobertura = 1/2 = 50%, que atinge o limiar mínimo → match parcial fraudulento.

**Correção:** Adicionar palavras estruturais de cargo ao conjunto `STOP`. Após a correção, `tokenSet("Diretor de Planejamento Operacional")` = `{planejamento, operacional}` e `tokenSet("Diretor de Finanças")` = `{financas}` → zero tokens compartilhados → nenhum match.

### Bug 2 — PDF DPO×COT: colunas Cargo/Função, Requisito, Subordinação em branco

**Causa:** `PrintReport` itera sobre cargos de referência do CBMRO e usa `bestCargoMatch()` para encontrar o cargo equivalente em cada estado por similaridade de nome. Como a nomenclatura varia muito, o matching falha na maioria dos estados → exibe "Não localizado". O erro é conceitual: o `comparativo_dpo_cot.json` já mapeou os órgãos curados por estado — não é necessário um segundo nível de matching por cargo.

**Correção:** Reescrever `PrintReport` para exibir os cargos diretamente dos órgãos curados, sem nenhum matching adicional. Estrutura do PDF muda de "centrada no cargo de referência" para "centrada no estado".

---

## Arquivos Modificados

| Arquivo | Tipo | Mudança |
|---|---|---|
| `src/components/CargoComparator.jsx` | Modificar | Expandir `STOP` com palavras estruturais de cargo |
| `src/components/OrgaosOperacionaisComparator.jsx` | Modificar | Reescrever `PrintReport`; remover `bestCargoMatch` e `flattenStateCargos` (mortos após a correção) |

---

## Task 1: Expandir STOP words em CargoComparator.jsx

**Files:**
- Modify: `src/components/CargoComparator.jsx:10`

- [ ] **Passo 1: Substituir o conjunto STOP na linha 10**

  Localizar o bloco atual (linha 10):
  ```javascript
  const STOP = new Set(['de', 'do', 'da', 'dos', 'das', 'e', 'o', 'a', 'ao', 'geral'])
  ```

  Substituir por:
  ```javascript
  const STOP = new Set([
    // artigos, preposições e partículas
    'de', 'do', 'da', 'dos', 'das', 'e', 'o', 'a', 'ao', 'geral',
    // títulos estruturais de cargo — presentes em quase todo nome, não distinguem função
    'diretor', 'diretoria', 'diretora',
    'comando', 'comandante', 'subcomandante',
    'coordenador', 'coordenadoria', 'coordenadora',
    'chefe', 'adjunto', 'adjunta',
    'secao',       // seção → norm → secao
    'nucleo',      // núcleo → norm → nucleo
    'assessor', 'assessoria',
    'gerente', 'gerencia',   // gerência → norm → gerencia
    'supervisor', 'supervisao',
  ])
  ```

  > Nota: as palavras já estão na forma normalizada (sem acentos), pois `tokenSet()` chama `norm()` antes de tokenizar — `norm('seção')` → `'secao'`, `norm('núcleo')` → `'nucleo'`, etc.

- [ ] **Passo 2: Verificar no servidor de desenvolvimento**

  Rodar:
  ```bash
  npm run dev
  ```

  No Dashboard → aba "Comparativo de Cargos":
  1. Aguardar carregamento completo (barra de progresso 100%)
  2. Selecionar o cargo "Diretor de Planejamento Operacional" no select de referência
  3. Verificar que o estado **AL (CBMAL)** exibe badge "Não Localizado" (antes exibia "Parcial 67%")
  4. Verificar que o estado **AC (CBMAC)** exibe badge "Não Localizado" (antes exibia "Parcial 67%")
  5. Selecionar o cargo "Subcomandante-Geral" e verificar que o estado **MS** ainda encontra match caso o nome seja próximo (regressão esperada mínima — aceitar se o match for semanticamente correto)

  Se AL e AC deixaram de ter match falso, a correção está funcionando.

- [ ] **Passo 3: Commit**

  ```bash
  git add src/components/CargoComparator.jsx
  git commit -m "fix: adiciona títulos estruturais ao STOP para eliminar false-positive no matching de cargos"
  ```

---

## Task 2: Reescrever PrintReport em OrgaosOperacionaisComparator.jsx

**Files:**
- Modify: `src/components/OrgaosOperacionaisComparator.jsx:303-390` (função `PrintReport` + funções auxiliares `bestCargoMatch` e `flattenStateCargos`)

- [ ] **Passo 1: Remover funções auxiliares mortas**

  Localizar e remover as funções `bestCargoMatch` (linhas 38–55) e `flattenStateCargos` (linhas 56–62), que só eram usadas em `PrintReport` e deixarão de ser necessárias após a reescrita.

  Após a remoção, o início do arquivo deve ir de `function norm(s)` diretamente para `/** Formata texto verbatim... */`.

- [ ] **Passo 2: Reescrever a função PrintReport**

  Localizar a função `PrintReport` completa (linhas 304–390) e substituí-la pela versão abaixo, que exibe os dados curados diretamente por estado:

  ```jsx
  /* ── Relatório PDF — centrado no estado, dados curados diretos ── */
  function PrintReport({ referenceState, otherStates, group, groupMeta }) {
    if (!referenceState) return null
    const refOrgans = referenceState[group] || []
    const printDate = new Date().toLocaleDateString('pt-BR', {
      day: '2-digit', month: 'long', year: 'numeric',
    })

    return (
      <div className="oc-print">
        {/* Cabeçalho institucional */}
        <div className="oc-print-header">
          <img
            className="oc-print-emblem"
            src="/BrasaoCBMRO2D-COMPLETO.png"
            onError={e => {
              if (!e.currentTarget.dataset.fb) {
                e.currentTarget.dataset.fb = '1'
                e.currentTarget.src = '/brasao-cbmro.svg'
              }
            }}
            alt="Brasão CBMRO"
          />
          <div>
            <div className="oc-print-title">
              Relatório Comparativo — {groupMeta?.ref_abbr} ({groupMeta?.ref_name})
            </div>
            <div className="oc-print-sub">
              Corpos de Bombeiros Militares · Referência: minuta de LOB do CBMRO ·
              Portal de Legislação
            </div>
          </div>
          <div className="oc-print-meta">
            <span>Emitido em</span>
            <strong>{printDate}</strong>
          </div>
        </div>

        <p className="oc-print-intro">
          Comparativo do órgão equivalente à <strong>{groupMeta?.ref_abbr}</strong>{' '}
          ({groupMeta?.ref_name}) nos 27 Corpos de Bombeiros Militares. Para cada estado,
          são exibidos os cargos/funções, requisitos de posto e subordinação conforme a
          legislação curada. "Órgão não discriminado" indica ausência de mapeamento na
          legislação do estado.
        </p>

        {/* ── Referência CBMRO ── */}
        <section className="oc-print-cargo">
          <h3 className="oc-print-cargo-title">
            Referência — CBMRO · {groupMeta?.ref_abbr}
          </h3>
          {refOrgans.length === 0 ? (
            <p>Órgão de referência não discriminado.</p>
          ) : (
            refOrgans.map((organ, i) => (
              <div key={i} style={{ marginBottom: 12 }}>
                <div>
                  <strong>Órgão:</strong> {organ.name}
                  {organ.abbreviation ? ` (${organ.abbreviation})` : ''}
                  {organ.legalRef ? ` · ${organ.legalRef}` : ''}
                </div>
                {organ.subordinadoA && (
                  <div><strong>Subordinação:</strong> {organ.subordinadoA}</div>
                )}
                <PrintCargosTable cargos={organ.cargos} />
                <PrintDesdobramentos items={organ.desdobramentos} />
              </div>
            ))
          )}
        </section>

        {/* ── Um estado por seção ── */}
        {otherStates.map(st => {
          const organs = st[group] || []
          const note = st.notes?.[group]
          return (
            <section className="oc-print-cargo" key={st.id}>
              <h3 className="oc-print-cargo-title">
                {st.abbreviation} · {st.cbm} — {st.name}
              </h3>

              {organs.length === 0 ? (
                <p style={{ fontStyle: 'italic', color: '#666' }}>
                  {note || 'Órgão equivalente não discriminado na legislação deste estado.'}
                </p>
              ) : (
                organs.map((organ, j) => (
                  <div key={j} style={{ marginBottom: 12 }}>
                    <div>
                      <strong>Órgão:</strong> {organ.name}
                      {organ.abbreviation ? ` (${organ.abbreviation})` : ''}
                      {organ.legalRef ? ` · ${organ.legalRef}` : ''}
                    </div>
                    {organ.subordinadoA && (
                      <div><strong>Subordinação:</strong> {organ.subordinadoA}</div>
                    )}
                    <PrintCargosTable cargos={organ.cargos} />
                    <PrintDesdobramentos items={organ.desdobramentos} />
                    {note && (
                      <p style={{ fontSize: 10, color: '#555', marginTop: 4 }}>
                        Nota: {note}
                      </p>
                    )}
                  </div>
                ))
              )}
            </section>
          )
        })}
      </div>
    )
  }
  ```

- [ ] **Passo 3: Adicionar os dois subcomponentes auxiliares do PrintReport**

  Inserir imediatamente ANTES da função `PrintReport` (após o bloco `SBS_FIELDS`):

  ```jsx
  /* ── Subcomponentes exclusivos do relatório impresso ── */
  function PrintCargosTable({ cargos }) {
    if (!cargos || cargos.length === 0) {
      return <p style={{ fontSize: 10, color: '#888', fontStyle: 'italic' }}>Cargos não discriminados.</p>
    }
    return (
      <table className="oc-print-table" style={{ marginTop: 6 }}>
        <thead>
          <tr>
            <th style={{ width: '30%' }}>Cargo / Função</th>
            <th style={{ width: '25%' }}>Requisito / Posto</th>
            <th style={{ width: '25%' }}>Subordinação</th>
            <th style={{ width: '20%' }}>Atribuições (resumo)</th>
          </tr>
        </thead>
        <tbody>
          {cargos.map((c, i) => (
            <tr key={i}>
              <td>{c.cargo || '—'}</td>
              <td>{c.requisito || '—'}</td>
              <td>{c.subordinadoA || '—'}</td>
              <td>
                {c.atribuicoes && c.atribuicoes.length > 0
                  ? c.atribuicoes.join(' ')
                  : '—'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    )
  }

  function PrintDesdobramentos({ items }) {
    if (!items || items.length === 0) return null
    return (
      <div style={{ marginTop: 4, fontSize: 10 }}>
        <strong>Desdobramentos:</strong>{' '}
        <span style={{ color: '#444' }}>{items.join(' · ')}</span>
      </div>
    )
  }
  ```

- [ ] **Passo 4: Verificar no servidor de desenvolvimento**

  Com `npm run dev` rodando, ir ao Dashboard → aba "DPO × COT":

  1. Selecionar "DPO" e clicar em "Exportar PDF — relatório por cargo (DPO)"
  2. No diálogo de impressão do browser, verificar o preview do PDF
  3. Confirmar que cada estado tem uma seção com:
     - Nome do órgão equivalente
     - Tabela com cargos, requisitos e subordinação preenchidos (não mais "Não localizado")
     - Desdobramentos listados onde houver
  4. Verificar estados sem órgão mapeado (ex.: DF no COT) — devem exibir a nota explicativa em itálico
  5. Repetir verificação para a aba "COT"

- [ ] **Passo 5: Commit**

  ```bash
  git add src/components/OrgaosOperacionaisComparator.jsx
  git commit -m "fix: reescreve PrintReport para exibir dados curados diretos e eliminar matching por cargo no PDF DPO×COT"
  ```

---

## Self-Review

### Cobertura do spec

| Problema | Task que resolve |
|---|---|
| Matching falso: "Diretor de Finanças" ≈ "Diretor de Planejamento Operacional" | Task 1 — STOP words |
| PDF sem Cargo/Função Correspondente, Requisito, Subordinação | Task 2 — PrintReport |

### Riscos

- **Task 1 — regressão no matching legítimo:** Ao adicionar `diretor`/`coordenador`/etc. ao STOP, cargos que antes casavam por compartilhar só o título estrutural passam a "Não Localizado". Isso é o comportamento **correto** — eram matches inválidos. Cargos que compartilham termos funcionais (`planejamento`, `operacional`, `financas`, `logistica`) continuam casando normalmente.

- **Task 2 — quebra de layout no PDF:** Os subcomponentes `PrintCargosTable` e `PrintDesdobramentos` usam classes `oc-print-table` e estilos inline para impressão. Verificar no preview de impressão se o layout está dentro das margens.

### Sem impacto em

- Pipeline Python (nenhum script é alterado)
- Dados JSON (`states_data.json`, `comparativo_dpo_cot.json`, `organs_detail/*.json`)
- Outras páginas (`StateDetail`, `Compare`, `Search`, `Legislations`, `StatesList`)
- Visualização em tela do DPO×COT (tabela e modo lado a lado — inalterados)
