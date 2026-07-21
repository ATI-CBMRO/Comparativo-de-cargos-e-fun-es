# Herdar as 2 Partes nas telas Subsídio/Revisão do Regulamento — Design

**Data:** 2026-07-21
**Autor:** Wândrio + Claude
**Status:** spec para revisão (pré-implementação)
**Contexto:** pendência sinalizada desde o spec da Fase 1 (§5.4 — "fora da Fase 1"). O Wizard e
o `.docx` do Regulamento já mostram Parte I/Parte II desde a Fase 1; esta spec estende a mesma
divisão às demais telas que consomem `regulamento_structure.json`.

## 1. Escopo real (achado da exploração)

Das 3 telas citadas na pendência original, só **2 são acionáveis agora**:

| Tela | Estado atual | Ação |
|---|---|---|
| `RegulamentoComparator.jsx` (aba "Regulamento" do Subsídio, `/regulamento/subsidio`) | Funcional, lê `regulamento_structure.json`, agrupa capítulos por `ch.group` (taxonomia temática pré-existente: Fundamentos, Competências, Serviços, etc.) | Nest o agrupamento por `group` DENTRO de Parte I/Parte II |
| `Revisao.jsx` (modo `docId==='reg'`, `/regulamento/revisao`) | Funcional, lê `regulamento_structure.json` diretamente, renderiza faixa "CAPÍTULO N" antes de cada capítulo | Inserir a mesma faixa de Parte usada no Wizard |
| `RegDiagramas.jsx` (`/regulamento/diagramas`) | **"Em breve"** — bloqueada por falta de `commandChart` do Regulamento, que ainda não foi gerado | **Fora de escopo.** Não é sobre herdar Partes — é sobre gerar um dado que não existe. Fica registrado como pendência própria, não forçado aqui. |

## 2. Objetivo
Os usuários que comparam o Regulamento com outros estados (Subsídio) ou comentam a minuta
(Revisão) veem a mesma divisão Geral × Serviço que já existe no Wizard e no `.docx`, sem
duplicar lógica — reusando o helper `src/lib/regulamentoPartes.js` já criado na Fase 1
(`PARTE_HEADERS`, `parteByChapterTitle`).

**Não-objetivos:**
- Não gerar `commandChart` do Regulamento (RegDiagramas fica como está).
- Não mudar a taxonomia de `group` existente no Comparator — Parte é uma camada ACIMA dela,
  não substitui.
- Não tocar no Regimento Interno (`MinutaWizard`, `MinutaRIComparator`, `Revisao` em modo `ri`).

## 3. Arquitetura

### 3.1 `RegulamentoComparator.jsx`
- `groupChapters(chapters)` passa a agrupar em 2 NÍVEIS: primeiro por `parte` (via
  `parteByChapterTitle`-like lógica, mas direto pelo campo `ch.parte` já presente no JSON — mais
  simples que usar o helper baseado em `chapterTitle`), depois por `ch.group` dentro de cada
  Parte. Estrutura resultante: `[{ parte: 'geral', label: 'PARTE I — GERAL', groups: [{name,
  chapters}, ...] }, { parte: 'servico', label: 'PARTE II — DO SERVIÇO', groups: [...] }]`.
- Sidebar de navegação e o corpo do comparador ganham um cabeçalho de Parte acima dos grupos
  temáticos — mesmo padrão visual (cor `--cbm-red-700`) do Wizard.

### 3.2 `Revisao.jsx` (modo `reg`)
- Importa `PARTE_HEADERS`, `parteByChapterTitle` de `../lib/regulamentoPartes.js` (já existe).
- No render de artigos (onde hoje insere a faixa "CAPÍTULO N" antes de `art.chapterTitle`),
  insere a MESMA lógica de faixa de Parte usada no Wizard (calcula `parteDe` uma vez via
  `useMemo`, rastreia `ultimaParte`, emite o cabeçalho de Parte só na primeira mudança).
- Modo `ri` (Regimento Interno) não tem campo `parte` — `parteByChapterTitle` retorna `{}`,
  logo a lógica vira no-op automaticamente (mesma garantia já provada na Fase 1 para o `.docx`).

## 4. Testes
- Nenhum teste Python muda (dado já existe desde a Fase 1).
- `node --test` continua verde — nenhuma mudança em `regulamentoPartes.js` (reuso puro).
- Prova visual: screenshot do Subsídio mostrando Parte I/Parte II na navegação e do modo
  Revisão do Regulamento mostrando a faixa de Parte; confirmar que a Revisão do RI continua
  idêntica (prova de não-regressão).

## 5. Riscos
- `RegulamentoComparator` tem uma UI de navegação mais elaborada (busca, seleção de
  estado/comparação) — a alteração deve ser aditiva (só agrupamento visual), sem tocar na
  lógica de seleção/comparação existente.
