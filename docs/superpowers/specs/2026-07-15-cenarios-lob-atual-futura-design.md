# Separação de cenários: LOB atual × LOB futura

**Data:** 2026-07-15
**Status:** Aprovado (blocos 1–5) — aguardando revisão do documento antes do plano

## Contexto e problema

Todo o portal foi construído sobre a **nova LOB do CBMRO** (em aprovação na Assembleia
Legislativa, previsão ~90 dias). Esse trabalho não se perde: regulamentará a documentação
quando a nova LOB entrar em vigor.

Existe, porém, uma **LOB atual já vigente** (Lei nº 2.204/2009, com alterações até a Lei nº
5.697/2023), para a qual faltam dois documentos essenciais: o **Regimento Interno** e o
**Regulamento (de Serviço)**. É preciso elaborar as minutas desses documentos para a LOB
vigente.

O sistema passa a suportar **dois cenários**:
- **LOB atual** (vigente) — foco de trabalho a partir de agora;
- **LOB futura** (em aprovação) — preservada como está, curadoria pausada.

Requisito duro: **um cenário nunca se mistura com o outro**. O acervo de legislação de
referência dos 27 estados serve **aos dois** cenários.

## Decisões tomadas (perguntas de brainstorming)

1. **Forma da separação:** chave (seletor) no topo — trocar o cenário troca todo o sistema;
   os dois nunca aparecem juntos.
2. **Documentos por cenário:** os dois cenários têm os **mesmos 2 documentos** — "Regimento
   Interno" e "Regulamento Geral" (rótulos idênticos nos dois; muda só a LOB de base).
3. **Fonte da estrutura da LOB atual:** o Wândrio forneceu o texto da LOB atual (Lei
   2.204/2009 consolidada). A estrutura de órgãos vigente será extraída dele na Fase 2.
4. **Organização dos dados:** pastas separadas por cenário (Opção A).
5. **Escopo:** pausar curadoria da LOB futura; trabalhar só na LOB atual, com separação clara.

## Arquitetura

### 1. Chave de cenário (contexto global)

- **Seletor no topo da barra lateral**, sempre visível, com selo/cor distinta por cenário
  (ex.: atual = navy; futura = vermelho CBMRO) para identificação imediata.
- Um **contexto React** (`ScenarioContext`/`useScenario`) expõe o cenário ativo (`'atual'` |
  `'futura'`) e a função de troca.
- Estado **persistido** (localStorage) e **refletido na URL**, de modo que abrir um link nunca
  traga o cenário errado. (Detalhe de implementação — prefixo de rota vs. query param — a
  definir no plano; premissa: o cenário é recuperável da URL.)
- O contexto alimenta menu, páginas e a montagem dos caminhos de `fetch`.

### 2. Menu

- As duas trilhas (**Regimento Interno** e **Regulamento Geral**) permanecem, com os mesmos
  rótulos. Trocar a chave troca a LOB de base por trás delas.
- O bloco "Geral" (Acervo Legal, Organograma, Manual, Acessos) é **compartilhado** entre
  cenários — o acervo dos 27 estados serve aos dois.

### 3. Dados (Opção A — gavetas por cenário)

Reorganização das pastas em `database/`:

- **Específicos de cenário** (movidos para subpasta por cenário):
  - `database/futura/` ← estado atual de: `minuta_structure.json`,
    `regulamento_structure.json`, `comparativo_minuta.json`, `comparativo_dpo_cot.json`.
  - `database/atual/` ← novo, começa vazio; recebe os arquivos equivalentes da LOB atual.
- **Compartilhados** (permanecem na raiz, servem aos dois): `states_data.json`,
  `organs_detail/`, `markdown/`, `documents_index.json`.
- O `fetch` das páginas passa a montar o caminho com o cenário ativo, ex.:
  `/database/${cenario}/minuta_structure.json`. Os caminhos compartilhados não mudam.
- **Pipeline Python:** os scripts que geram os arquivos específicos de cenário passam a
  escrever na subpasta do cenário; os plugins de servir/copiar do `vite.config.js`
  (`serveDatabase`, `copyDatabaseOnBuild`) continuam expondo `database/` inteira (subpastas
  incluídas) — sem mudança estrutural neles.

### 4. Revisão colaborativa (Firebase) — isolamento por cenário

- Hoje o endereço estável de cada dispositivo (`dispositivoId` = `editId#index`) usa prefixo
  `reg:` para separar RI de Regulamento. **Acrescenta-se o cenário ao endereço** (ex.:
  `atual:` / `futura:`), na mesma lógica, para que um comentário de um cenário nunca caia na
  minuta do outro.
- A liberação para não-admin (`config/revisao.regulamentoAberto`, fail-closed) passa a valer
  **por cenário**.
- A revisão da LOB atual nasce vazia (sem conteúdo de minuta ainda) — já isolada por
  construção; sem urgência.

## Fases de execução (PRs incrementais)

- **Fase 1 — Chave + gavetas (sem conteúdo novo).** Criar `ScenarioContext` + seletor no topo;
  mover dados atuais para `database/futura/`; criar `database/atual/` vazio; ajustar `fetch`,
  URL e scripts Python de saída. Ao fim: em "LOB futura" o sistema funciona **idêntico a hoje**
  (nada do validado se perde); "LOB atual" aparece vazio/"em construção". **Esta é a entrega
  desta rodada.**
- **Fase 2 — Estrutura da LOB atual.** A partir do texto da Lei 2.204/2009 consolidada,
  extrair a estrutura de órgãos **vigente** (separando dispositivos em vigor dos revogados) e
  gerar o esqueleto das minutas do cenário atual (mesmo pipeline da futura). Requer validação
  humana da estrutura vigente.
- **Fase 3+ — Curadoria do cenário atual.** Enriquecer dispositivo a dispositivo com o acervo
  dos estados (mesma metodologia verbatim já usada).

A curadoria da LOB futura fica **pausada e preservada** exatamente onde está.

## Fonte da LOB atual (insumo da Fase 2)

- **Lei nº 2.204, de 18/12/2009** — Lei Orgânica do CBMRO, texto consolidado com alterações
  até a **Lei nº 5.697/2023**. PDF fornecido pelo Wândrio (a versionar no repositório para a
  Fase 2).
- **Atenção (registrada agora):** o texto consolidado contém muitos dispositivos
  **revogados/alterados** (trechos riscados). A estrutura vigente exige leitura cuidadosa de
  qual redação está em vigor — trabalho da Fase 2, com validação do Wândrio, não desta rodada.

## Fora de escopo desta rodada

- Extração/curadoria de conteúdo da LOB atual (Fase 2+).
- Qualquer mudança na curadoria da LOB futura (apenas mover arquivos de pasta).
- Página de Organograma: permanece compartilhada; eventual visão específica por cenário não
  entra agora.
