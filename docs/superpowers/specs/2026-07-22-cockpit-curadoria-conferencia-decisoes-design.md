# Cockpit de Curadoria — Conferência linear + Decisões — Design

**Data:** 2026-07-22 · **Validado por:** Wândrio (brainstorm + protótipo aprovado nesta data)
**Protótipo de referência:** `scratchpad/proto-conferencia.html` (3 abas, dados reais do cenário atual)

## Objetivo

Dar ao CBMRO uma tela única para **conferir a minuta dispositivo por dispositivo contra as
referências dos outros estados** e **tomar as decisões de curadoria dentro do sistema**, com
o material de apoio do Obsidian trazido para dentro. Substitui o vaivém entre telas soltas
(Comparar/Revisão) e o cofre Obsidian.

Atende duas necessidades declaradas do Wândrio:
- **B — conferência manual:** percorrer a minuta em ordem e verificar se a curadoria foi
  aplicada corretamente, olhando o que cada estado diz.
- **A — decisão no sistema:** registrar as decisões pendentes com o material que hoje só
  existe no Obsidian, e o sistema guiar o que fazer com cada decisão.

## Três blocos (= três abas do protótipo aprovado)

### A · Conferência do Regimento (por órgão) · B · Conferência do Regulamento (por tema)

Rolagem **linear**, dispositivo a dispositivo, na ordem do documento. Cada dispositivo é um
cartão com duas colunas:
- **Esquerda — "Minuta do CBMRO":** o texto do dispositivo (o `proposedText`/artigo da
  minuta), com o rótulo (Art. Nº / seção) e a fonte.
- **Direita — "Como outros estados tratam":** chips por estado; ao selecionar, mostra o
  texto do estado com etiqueta de qualidade: **`exata`** (texto verbatim) ou **`auto`**
  (correspondência automática por palavra-chave).

Controles por dispositivo: **✓ Confere** / **⚠ Divergente** / **✎ Anotar decisão**. Barra de
progresso "Conferidos X de N". Layout de 2 colunas confirmado pelo Wândrio.

**Enriquecimento verbatim do Regimento atual (achado do protótipo):** as referências dos
outros estados NÃO dependem do cenário do RO — a lei de Alagoas é a mesma. Por isso o
Regimento atual reaproveita o **Bloco D verbatim já curado para a minuta futura**, casando
órgão a órgão. 8 casam por chave idêntica (`cg, condeg, assessorias, corregedoria, dp, deei,
cat, dlog`); os 13 restantes casam por um **de-para a validar pelo Wândrio** (proposta):

| Atual | → Futura (Bloco D) | Atual | → Futura |
|---|---|---|---|
| ajudancia | ag | dcs | ccs |
| gabinete | gab-cg | dinf | cinf |
| cepdec | depdec | cob1 | cot |
| dint | cint | cob2 | crbm |
| cpof | dpof | coa | boa |
| gbs | bbs | | |

`emg` e `comissoes` ficam **sem equivalente Bloco D** (seguem com correspondência automática,
rotulada). Onde não há verbatim nem automática, o cartão diz isso — nunca esconde a lacuna.

### C · Decisões / Pendências

Lista os pontos que precisam da decisão do Comando, de **duas origens**:
1. **Curadoria (Obsidian):** as 36 notas de decisão já levantadas (9 do Regimento + 27 do
   Regulamento). Etiqueta roxa "curadoria (Obsidian)".
2. **Conferência:** o que o Wândrio marcar como **⚠ Divergente** nas abas A/B vira uma
   pendência aqui. Etiqueta laranja "marcada como divergente na conferência".

Cada decisão traz TODO o material da nota do Obsidian (validado no protótipo v3):
- **A questão** por extenso.
- **Cada caminho possível:** título do estado + **texto verbatim** (com incisos) + fonte
  (`cf. …`) + **nota de OCR** quando houver (reproduzida, em itálico) + **Leitura**
  (interpretação curada). Seleção por rádio (um caminho = a base adotada).
- **Comparação** ("o que pesa na decisão").
- **Deliberar em conjunto com:** decisões ligadas (as que a nota marca como conjuntas).
- **Sua decisão e o porquê** (texto livre) + **✓ Registrar decisão**.

## O que "Registrar decisão" faz (mecânica central)

Cada decisão carrega um **tipo** (curado na origem, a partir do próprio texto da nota, que já
distingue "divergência de estrutura" × "de redação"):

**Sempre, nos dois tipos:**
1. **Grava a decisão** no Firebase (mesma base dos comentários/textos finais): caminho
   escolhido, justificativa, autor (e-mail), data. Registro permanente e auditável — o
   "livro de decisões" da minuta.
2. **Marca o dispositivo como decidido** (some das pendências; aparece "decidido ✓" na
   conferência e na Revisão).

**Decisão de REDAÇÃO** (escolher o texto de um dispositivo):
3. Escreve o texto escolhido como **texto final** daquele dispositivo, reusando o mecanismo
   existente `finalTexts` (coleção Firestore, `src/lib/reviewData.js`, consumida em
   `Revisao.jsx` como sobreposição: `finalsForDoc.get(id) ?? proposedText`). Efeito
   imediato: a minuta mostra e **exporta no .docx** esse texto. Seguro contra regeração —
   é camada por cima, chaveada por `dispositivoId` estável.

**Decisão ESTRUTURAL** (fundir órgãos, mudar subordinação, mudar nível hierárquico):
3. NÃO reescreve um campo de texto (mudaria a árvore de órgãos, que é dado gerado). Em vez
   disso, gera uma **"ficha de aplicação"**: instrução precisa do que mudar na fonte de
   dados (`organs_detail/ro.json`/gerador) para uma **regeração controlada** (com
   conferência antes/depois). Registrada junto da decisão; aplicada por curadoria, não por
   clique. Motivo: aplicar estrutura automaticamente no clique corromperia a minuta.

## Dados e pipeline

- **Referências da conferência:** Regulamento e Regimento futura → campo `alternatives` já
  existente. Regimento atual → **novo enriquecimento** que injeta o Bloco D da futura via o
  de-para acima (gerador dedicado, isolado — nunca importa enriquecimento que vaze outros
  estados no texto do RO, conforme a armadilha do CLAUDE.md). Fallback: `comparativo_minuta`
  automático (já gerado).
- **Decisões:** **novo pipeline** que lê as notas do Obsidian
  (`Regimento Interno — Curadoria/`, `Regulamento — Curadoria/`) e produz um JSON estruturado
  (`database/decisoes_curadoria.json`) que o sistema consome: por decisão, `{questao,
  candidatas[{titulo, textoVerbatim[], fonte, ocr, leitura}], comparacao[], ligadas[], tipo:
  redacao|estrutural, alvoDispositivoId}`. Reconciliação obrigatória: cada trecho verbatim
  parseado deve bater caractere a caractere com a nota (e a nota já bate com o JSON da
  minuta). Anomalia se sinaliza.
- **Isolamento por cenário:** decisões e textos finais chaveados por `dispositivoId` estável,
  com o marcador de cenário já existente (`atual:`/`reg:atual:`/sem marcador), reusando
  `reviewGroup.js`. Sem colisão entre cenários.

## Fases de implementação (cada uma entrega software usável)

- **Fase 1 — Conferência linear (leitura):** a tela A/B, referências dos dois lados, o
  enriquecimento verbatim do Regimento atual (de-para validado), entrada no menu. Sem
  decisões ainda. Prova: percorrer a minuta e ver as referências.
- **Fase 2 — Decisões do Obsidian no sistema:** o pipeline notas→JSON + a aba C em modo
  leitura (mostra todo o material). Prova: as 36 decisões visíveis e fiéis à nota.
- **Fase 3 — Registrar e aplicar:** a mecânica de "Registrar decisão" (Firebase + `finalText`
  para redação + ficha de aplicação para estrutural) + o "Divergente" da conferência virando
  pendência. Prova: registrar uma decisão de redação e vê-la no .docx; registrar uma
  estrutural e receber a ficha.

## Fora de escopo (YAGNI)

- Aplicação automática de decisão estrutural no clique (deliberadamente manual, via ficha).
- Edição livre do texto da minuta fora do fluxo de decisão (a Revisão já cobre comentários).
- Novo backend: reusa Firebase existente.

## Testes e prova

- Lógica pura testada: o parser das notas do Obsidian (`node --test`/pytest), o de-para do
  Regimento, a classificação redação×estrutural, a resolução de `dispositivoId`.
- Reconciliação verbatim: amostragem trecho-da-aba × nota-do-Obsidian × JSON da minuta.
- Prova visual (Playwright, com login real do Wândrio): as 3 abas nos dois cenários; uma
  decisão de redação registrada refletindo no .docx; preservação das telas já validadas
  (Revisão, Subsídio) intocadas.

## Riscos

- **De-para do Regimento (13 órgãos):** proposta, precisa de validação humana antes de
  entrar. Onde incerto (`emg`, `comissoes`), fica automático rotulado.
- **Congelar `minuta_structure` durante a rodada de decisões** (premissa já existente do
  módulo de Revisão, por causa do `dispositivoId` estável).
- **Fidelidade verbatim no parse das notas:** defeitos de OCR devem ser preservados, não
  limpos — mesma regra dura da curadoria.
