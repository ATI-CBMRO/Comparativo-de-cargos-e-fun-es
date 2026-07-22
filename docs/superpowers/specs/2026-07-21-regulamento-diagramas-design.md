# Diagramas do Regulamento Geral — árvore do documento + mapa mental

**Data:** 2026-07-21 · **Status:** aprovado (brainstorming com o Wândrio)

## Problema

`/regulamento/diagramas` (`RegDiagramas.jsx`) está "em breve" desde a criação da trilha do
Regulamento, prometendo um `commandChart` que nunca foi gerado. Descoberta do brainstorming:
**a promessa estava errada** — o Regulamento é TEMÁTICO (2 Partes → 16 temas → artigos), não
tem cadeia de comando. Um organograma de órgãos seria dado artificial.

## Decisões (com o Wândrio)

1. **Conteúdo**: árvore do DOCUMENTO (Regulamento → Parte I/II → 16 temas) + mapa mental em
   cartões. Nada de organograma forçado.
2. **Origem da árvore**: montada NA TELA a partir dos 16 capítulos do
   `regulamento_structure.json` (campo `parte` + ordem existente). Zero mudança nos geradores
   Python; cenários atual/futura herdam de graça.

## Desenho

- **`RegDiagramas.jsx`** vira espelho do `MinutaDiagrams.jsx`: abas "Árvore do documento" e
  "Mapa mental", painel lateral por tema (artigos), Imprimir/PDF, cenário via
  `useScenario()` + `scenarioDbUrl(cenario, 'regulamento_structure.json')`.
- **Árvore**: lógica pura nova em `src/lib/regulamentoTree.js` —
  `buildRegulamentoTree(chapters)` retorna nó raiz no MESMO formato consumido por
  `MinutaOrgChart` (`{ sigla, label, chapterId, children }`): raiz "Regulamento Geral" →
  2 nós de Parte (rótulos de `PARTE_HEADERS` em `regulamentoPartes.js`, `structural: true`,
  não clicáveis) → temas na ordem do array `chapters` (clicáveis, `chapterId: ch.id`,
  contagem de artigos no rótulo). Capítulo sem `parte` reconhecida cai num grupo "Outros"
  (defensivo; hoje não ocorre).
- **Mapa mental**: reuso direto de `MinutaMindMap` (já lista caputs de `kind:'articles'`),
  com faixas "PARTE I — GERAL"/"PARTE II — DO SERVIÇO" separando os cartões — mesmo padrão
  visual das faixas do Subsídio/Revisão.
- **Painel lateral**: mesmo `MinutaDetailPanel` (o de `MinutaDiagrams` é local ao arquivo —
  extrair para componente compartilhado OU duplicar mínimo; preferir extração se limpa,
  sem alterar o comportamento do RI).

## O que NÃO muda

Geradores Python, JSONs de dados, `MinutaDiagrams.jsx` (RI), `MinutaOrgChart`/`MinutaMindMap`
(a menos de prop opcional retro-compatível se necessária), menu/rotas (rota já existe).

## Testes e prova

- `src/lib/regulamentoTree.test.js` (`node --test`): 2 Partes na ordem certa, temas na ordem
  do documento, contagem de artigos, capítulo sem parte → "Outros", chapterId correto.
- Prova visual: login no portal (Playwright), screenshots das 2 abas nos 2 cenários
  (futura e atual) + confirmação de que `/minuta/diagramas` (RI) segue intocada.
