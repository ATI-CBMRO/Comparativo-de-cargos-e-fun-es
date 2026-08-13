# Regulamento de Serviço — ambiente setorizado por escopo do participante

**Data:** 2026-08-13
**Origem:** o Subcomandante-Geral decidiu entregar primeiro o **Regulamento de Serviço**
(serviço operacional, coordenado pelos COB; serviço técnico, coordenado pela CAT) e só
depois o Regulamento Geral completo. Reunião de apresentação e coleta de manifestações
com os responsáveis em 2026-08-13 (tarde).

**Problema:** hoje qualquer participante que faz login enxerga o portal inteiro — Acervo
dos 27 estados, Organograma, as duas trilhas (Regimento Interno e Regulamento Geral, 6
telas cada) e o seletor de cenário LOB atual × futura. Para uma reunião de análise de
conteúdo isso dispersa, e — pior — o cenário padrão é `futura`, de modo que uma
manifestação feita sem trocar o seletor é gravada no cenário errado, em silêncio.

---

## Decisões tomadas (com o Wândrio, 2026-08-13)

| Questão | Decisão |
|---|---|
| Perímetro do documento | Parte II (4 temas) + `seguranca-contra-incendio` + Preliminares + Finais = **7 capítulos, 185 artigos** |
| Cenário | **LOB atual** (Lei 2.204/2009) — é a lei vigente; o regulamento precisa poder ser assinado hoje |
| O que o participante faz | **Só lê e comenta** artigo a artigo (tela de Revisão). Sem Conferência, sem Subsídio |
| Abordagem | **Recorte por perfil dentro do sistema atual** (não criar documento novo) |
| Deploy | Direto no `master`, **em caráter excepcional autorizado pelo Wândrio** por causa do prazo; o Ten. Tiago é avisado depois (regra 4 do crachá) |

### Por que "serviço técnico da CAT" puxa um capítulo da Parte I

O Regulamento já está dividido em 2 Partes (spec `2026-07-21-regulamento-geral-2-partes-design.md`):
Parte I Geral (12 temas) e Parte II de Serviço (4 temas). O serviço **operacional** dos COB
cai redondo na Parte II. O serviço **técnico** da CAT é a matéria de
`DA SEGURANÇA CONTRA INCÊNDIO E PÂNICO` (19 artigos), que está na **Parte I**.

Ou seja: o recorte pedido pelo Subcomandante **não coincide** com a divisão de Partes já
existente. Por isso o escopo é uma lista explícita de capítulos, e **não** um filtro por
`parte === 'servico'`. Filtrar por `parte` deixaria a CAT sem matéria na pauta.

### Por que NÃO criar um documento "Regulamento de Serviço" separado

Foi considerado e descartado para esta etapa: exigiria estrutura JSON própria, gerador
próprio, rotas próprias, e **separaria os comentários do documento-mãe**. Custo em dias, e
retrabalho de consolidação depois. A geração de um `.docx` autônomo do Regulamento de
Serviço continua possível a partir deste mesmo recorte, quando a redação amadurecer.

---

## Análise de conteúdo transversal (requisito explícito: "sem lacunas")

Varredura automatizada dos 185 artigos do recorte no
`database/atual/regulamento_structure.json`, procurando matéria que dependa do que fica
de fora:

| Matéria fora do recorte invocada pelo texto do recorte | Trechos | Concentração |
|---|---:|---|
| Competências de órgão / cadeia de comando | 104 | `atribuicoes-funcoes` (82) |
| Ensino e instrução | 31 | `atribuicoes-funcoes` (26) |
| Pessoal e quadros | 14 | espalhado |
| Uniformes e apresentação | 6 | `servico-interno-dia` (3) |
| Disciplina e correição | 4 | `atribuicoes-funcoes` (3) |
| **Remissão explícita a "Art. N"** | **1** | referência ao Exército/Constituição, não interna |

**Conclusão 1 — cortar não quebra remissão.** A minuta praticamente não usa remissão
numérica interna (1 ocorrência em 185 artigos, e externa). A renumeração provocada pelo
recorte é, portanto, segura.

**Conclusão 2 — a lacuna é conceitual, não textual, e está concentrada em um capítulo.**
`DAS ATRIBUIÇÕES DAS FUNÇÕES` (29 artigos) descreve o que cada função faz, mas *quem é*
cada órgão está nos capítulos de Competências (158 artigos), fora do recorte.

**Tratamento adotado:** declarar o recorte no topo do documento (nota de escopo), em vez
de inchar a pauta com 228 artigos de Parte I. Lacuna declarada é escopo; lacuna silenciosa
é defeito.

---

## Fundamento técnico que torna o recorte seguro

Cada comentário é ancorado no **`editId` do dispositivo**, não no número do artigo
(`caputDispositivoId(art.editId)` / `incisoDispositivoId(inc.editId, inc.index)` —
`Revisao.jsx`, `src/lib/dispositivoId.js`). O `editId` é atributo do nó da estrutura e
**não depende de quantos capítulos foram articulados**.

Consequência: filtrar `structure.chapters` altera apenas `art.number` (a numeração exibida),
**nunca** a identidade dos comentários. Tudo o que for dito na reunião de hoje reaparece
grudado no dispositivo certo quando o Regulamento completo for aberto. Zero retrabalho.

**Risco residual aceito:** `dispositivoLabelSnapshot` grava o rótulo no momento do
comentário (ex.: "Art. 12º" na numeração do recorte). No documento completo esse mesmo
dispositivo terá outro número, então o rótulo histórico ficará defasado. É cosmético — o
vínculo real é o `editId` — e a alternativa (recalcular rótulos) reintroduziria o
endereçamento posicional que já causou o AR-03. **Não corrigir.**

Não há risco AR-03: o recorte remove capítulos inteiros, nunca reordena incisos dentro de
uma folha, de modo que os índices `#index` permanecem estáveis.

---

## Desenho

### 1. `src/lib/escopoServico.js` (lógica pura, testada)

Fonte única do recorte — nenhuma outra tela repete a lista.

- `TEMAS_SERVICO`: os 7 `themeKey` do recorte, **na ordem de leitura do documento**
  (ver abaixo). Esta lista é a ordem, não só o filtro.
- `filtrarEstruturaPorEscopo(structure, escopo)`: devolve a estrutura com `chapters`
  filtrados **e reordenados segundo `TEMAS_SERVICO`**. Com `escopo` nulo ou desconhecido,
  devolve a estrutura **intacta** (no-op) — quem não tem escopo não é afetado.
- Casamento por **sufixo do id** (`id.split(':').pop()`), porque o id carrega o marcador de
  cenário: `reg:servico-operacional` na futura, `reg:atual:servico-operacional` no atual.
  Casar pelo id inteiro quebraria em um dos cenários.

**Ordem de leitura — e por que NÃO preservar a ordem do arquivo.** No JSON, a Parte I vem
inteira antes da Parte II: `disposicoes-finais` está na posição 12 e os temas de serviço só
começam na 13. Filtrar preservando a ordem original **colocaria "DAS DISPOSIÇÕES FINAIS" no
meio do documento**, antes do serviço operacional — defeito grosseiro num documento que vai
ser lido em reunião. Por isso o recorte reordena explicitamente:

| # | Capítulo | Artigos | Racional |
|---|---|---:|---|
| 1 | Das Disposições Preliminares | 3 | abertura |
| 2 | Do Serviço Operacional | 70 | matéria dos COB |
| 3 | Da Central de Operações e do Teledespacho | 3 | matéria dos COB, junto do socorro |
| 4 | Do Serviço Interno e de Dia | 58 | serviço de escala |
| 5 | Das Atribuições das Funções | 29 | quem faz o quê no serviço |
| 6 | Da Segurança Contra Incêndio e Pânico | 19 | matéria da CAT (serviço técnico) |
| 7 | Das Disposições Finais | 3 | fechamento |

Agrupa a matéria dos COB no início, o serviço técnico da CAT em bloco próprio, e mantém
Preliminares e Finais nas pontas. **Esta ordem é decisão de produto revisável** — trocar
significa reordenar `TEMAS_SERVICO` e nada mais, sem tocar em dado nem em comentário.

### 2. Escopo no cadastro do participante

Campo `escopo` no documento `members/{email}`, propagado por `src/lib/auth.jsx` para
`user.escopo` (mesmo lugar onde `role` já é normalizado). Ausente ⇒ `null` ⇒ comportamento
de hoje, sem alteração para nenhum usuário existente.

Para a reunião de hoje o campo é gravado **direto no console do Firestore** nos poucos
participantes — construir tela de gestão de escopo em `Acessos.jsx` fica para depois da
reunião. Decisão consciente de prazo, registrada aqui para não virar dívida esquecida.

### 3. Menu enxuto

Em `App.jsx`, quando `user.escopo === 'servico'` a barra lateral mostra **apenas**:
*Manual de uso* e *Regulamento de Serviço* (`/regulamento/servico`). Some o
`ScenarioSwitcher`, somem as duas trilhas, some o Acervo, some o Organograma.

Isto é **simplificação de interface, não controle de segurança**: o participante que
digitar `/minuta` na barra de endereço ainda alcança a rota. Segurança de dado continua
sendo o `firestore.rules`, que não muda nesta entrega. Não vender isto como restrição de
acesso.

### 3b. Suprimir as faixas "PARTE I / PARTE II" no modo escopo

`Revisao.jsx` desenha uma faixa vermelha sempre que o capítulo muda de `parte`
(`PARTE_HEADERS` + `parteByChapterTitle`, `src/lib/regulamentoPartes.js`). Na ordem de
leitura acima, as partes se alternam — `geral` → `servico` → `geral` — e a tela imprimiria
**"PARTE I → PARTE II → PARTE I"**, sugerindo ao grupo que o documento volta atrás.

No modo escopo o documento **não é dividido em Partes**: é um documento único de serviço.
As faixas ficam suprimidas (`parteDe` vazio ⇒ o código já vira no-op, sem `if` novo). As
faixas continuam intactas no Regulamento Geral completo, que não é tocado.

### 3c. Restrições de interação (acrescentado pelo Wândrio em 2026-08-13)

Depois da 1ª revisão da spec, o Wândrio determinou: **quem não é administrador só
interage na Revisão.** A regra aterrissa em **dois níveis diferentes**, de propósito.

**Nível 1 — por ESCOPO (só os convidados da reunião).** Para `escopo === 'servico'`, além
do menu reduzido, as **rotas** ficam fechadas: digitar `/minuta`, `/regulamento/conferencia`,
`/regulamento/decisoes`, `/legislacoes` etc. na barra de endereço devolve o participante ao
documento dele. Endereços liberados: `/regulamento/servico`, `/manual`, `/login`,
`/cadastro` e a raiz `/`.

Por que só para o escopo, e não para todo não-admin: a **Conferência é colaborativa de
propósito** — qualquer membro confere ou desmarca, sem dono (decisão registrada no CLAUDE.md
e endurecida no `firestore.rules` em 25-26/07/2026). Fechá-la para todo não-admin
desfaria essa decisão e tiraria da comissão atual uma ferramenta em uso. O Wândrio optou
por preservá-la e restringir apenas os convidados desta reunião.

**Nível 2 — por PAPEL (todo não-admin).** Os dois Wizards (`MinutaWizard.jsx` e
`RegulamentoWizard.jsx`) ficam **somente leitura** para quem não é administrador. Isto não
desfaz decisão anterior: a edição dos Wizards nunca teve controle de papel.

Os 4 pontos de edição, idênticos nos dois arquivos:

| Ponto | `MinutaWizard.jsx` | `RegulamentoWizard.jsx` |
|---|---|---|
| Botão "editar" (abre o textarea) | 298 | 306 |
| `textarea` + "Concluir edição" | 267, 276 | 275, 284 |
| Caixa de seleção do inciso (exclui da minuta) | 312-313 | 320-321 |
| `RemovedBlock` — restaurar inciso removido | 322, 484 | 330, 513 |
| Seleção de fontes de enriquecimento | 406-407 | 416-417 |

**A edição do Wizard hoje NÃO é gravada em lugar nenhum** — `edits` e `excluded` são estado
local do React, que morre ao fechar a aba. O motivo de desabilitar não é proteger o dado, e
sim impedir que um participante altere o texto na tela e **baixe um `.docx` com a alteração
dele**, colocando uma versão paralela em circulação depois da reunião.

**O que estas restrições NÃO são.** Menu e rota são camada de interface. O
`firestore.rules` **não muda nesta entrega** e continua autorizando qualquer membro ativo a
gravar em `conferencia`. Um participante determinado ainda conseguiria gravar por fora da
tela. Publicar regra nova exige o console do Firebase no perfil Chrome Institucional — é
ação do Wândrio, não minha, e fica registrada como pendência.

### 4. Rota `/regulamento/servico`

Renderiza `Revisao` com `initialDoc='reg'` e o escopo de serviço aplicado. Reaproveita a
tela existente — nenhuma tela nova.

### 5. Cenário travado

Para quem tem escopo, o cenário é forçado a `atual` no mount da rota e o `ScenarioSwitcher`
não é exibido. Elimina a falha silenciosa de comentar na LOB futura por engano.

### 6. Nota de escopo no topo do documento

Bloco fixo antes do primeiro artigo, visível só no modo escopo:

> **Minuta do Regulamento de Serviço — 1ª etapa.** Reúne o serviço operacional (COB), o
> serviço técnico de segurança contra incêndio e pânico (CAT), o serviço interno e de dia,
> as atribuições das funções e a Central de Operações — 185 artigos, sobre a Lei nº
> 2.204/2009 (LOB vigente).
> Ficam para a 2ª etapa, no Regulamento Geral: competências dos órgãos de direção, apoio e
> execução, disciplina e correição, ensino e instrução, uniformes, cerimonial e honras,
> pessoal e quadros — 228 artigos.
> A numeração é provisória e será refeita na consolidação final.

### 7. Destravar `config/revisao.regulamentoAberto`

A chave é *fail-closed*: fechada, o participante vê "Regulamento em preparação"
(`Revisao.jsx:164`). Precisa ser ligada pelo botão de administrador na própria tela de
Revisão do Regulamento **antes** da reunião.

---

## Fluxo do participante

1. Recebe o link do portal e o convite por e-mail (já cadastrado em `members` com
   `ativo: true` e `escopo: 'servico'`).
2. `/cadastro` → cria a própria senha. `/login` nas próximas vezes.
3. Cai em `/regulamento/servico`: menu com dois itens, documento de 185 artigos, nota de
   escopo no topo.
4. Clica no balão à direita de qualquer artigo ou inciso → escreve a manifestação.
5. O comentário grava em `suggestions` com autor (nome/uid), data, o `editId` do
   dispositivo, o rótulo e o trecho no momento do comentário. As manifestações de todos
   ficam visíveis, com curtida.

## Verificação antes de declarar pronto

- `node --test` verde, incluindo os testes novos de `escopoServico.js`.
- Login real com uma conta de teste **com** escopo: screenshot mostrando menu de 2 itens,
  185 artigos, nota de escopo, sem seletor de cenário.
- Ordem dos capítulos conferida na tela contra a tabela desta spec (Finais por último,
  Preliminares primeiro) e **nenhuma faixa "PARTE I / PARTE II"** visível.
- Login real com uma conta **sem** escopo: screenshot provando que o portal continua
  idêntico ao de hoje (nenhuma regressão para quem já usa).
- Um comentário enviado ponta a ponta e conferido no Firestore, com o `editId` correto e o
  marcador `reg:atual:` do cenário.
- `grep` por outros lugares que articulam o Regulamento (Wizard, docx, Conferência,
  Subsídio) confirmando que **não** foram tocados.

## Fora de escopo desta entrega

- Tela de gestão de escopo em `Acessos.jsx` (o campo é gravado no console por ora).
- Documento `.docx` autônomo do Regulamento de Serviço.
- Qualquer alteração de redação da minuta — esta entrega é o **ambiente**, não o conteúdo.
- **`firestore.rules` — inalterado**, e por isso a restrição da Conferência é de tela, não
  de banco (ver 3c). Endurecer a regra é ação do Wândrio no console institucional; fica
  registrado em `.claude/PENDENCIAS.md`.
