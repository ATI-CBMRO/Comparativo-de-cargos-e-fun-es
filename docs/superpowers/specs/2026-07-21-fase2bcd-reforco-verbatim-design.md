# Fase 2, Fatias B+C+D — Reforço verbatim do Regulamento — Design

**Data:** 2026-07-21
**Autor:** Wândrio + Claude
**Status:** spec para revisão (execução autorizada — "siga tudo")
**Contexto:** conclui a Fase 2 do projeto "Regulamento Geral em 2 Partes" (Fatia A já entregue
— 16º tema preenchido). Fatias B, C, D reforçam com verbatim novo os temas já existentes, sem
mudar a estrutura (2 Partes, 16 temas) definida na Fase 1.

## 1. Objetivo e escopo

Reusa o MESMO pipeline de curadoria da Fatia A (extrator por faixa de "Art. N" +
`verificar_verbatim.py`). Três fatias independentes, cada uma um commit próprio:

- **Fatia B** — reforça a **Parte II (Serviço)** com o restante de Bahia, todo o Roraima,
  o restante de Tocantins (Anexo 2), e 5 normas de Alagoas com corpo articulado utilizável.
- **Fatia C** — reforça 2 temas magros da **Parte I (Geral)** com o RISG do Exército:
  `cerimonial-honras` e `pessoal-quadros`.
- **Fatia D** — reforço cirúrgico de `servico-operacional` e `seguranca-contra-incendio` com
  3 trechos específicos do Espírito Santo (CAT, 1º BBM, CERD).

## 2. Decisões de escopo (curadoria — sinalizadas, não forçadas)

Nem toda fonte lida vira conteúdo nesta rodada. Registro explícito do que fica de fora e por quê:

| Fonte/trecho | Por que fica de fora AGORA |
|---|---|
| Tocantins — corpo principal (Art. 1-13, 16, antes do Anexo 2) | Colisão de numeração: o corpo principal tem "Art. 8" e o Anexo 2 também tem "Art. 8" — mapear ambos para o mesmo tema (`atribuicoes-funcoes`) geraria `editId` duplicado. Corrigir exigiria extração por linha absoluta (`line_slices`) com mapeamento fino artigo a artigo — mais arriscado sob "siga tudo"; fica de fora, sinalizado como pendência de curadoria fina. |
| Alagoas — DOB 05, 06, 07, 08 | Não têm corpo articulado por "Art. N" (são estruturados por seção numerada: "1 FINALIDADE", "2 APLICAÇÃO"...). O extrator atual só corta por "Art. N". Incompatível com o mecanismo determinístico sem um modo de extração novo — fica de fora, sinalizado. |
| RISG — `uniformes-apresentacao` | A leitura das faixas mais prováveis (Revista de Pessoal, Apresentações) não achou capítulo dedicado a uniforme. Sem achado forte, o tema segue com 1 artigo (SE) apenas — não forçar conteúdo fraco/tangencial. |
| RISG — Título VI, Cap. II (art. 328-333, símbolos do Exército) | Específicos do Exército (RUE, estandartes históricos) sem paralelo em CBM. |
| RISG — art. 386-390 (substituição entre oficiais-generais) | CBM estadual não tem cargo de oficial-general. |
| CERD (ES) — atribuições internas de cargos (Chefe do CERD, GERD, Seção de Logística) | Fora do recorte "cirúrgico" pedido (estrutura administrativa interna, não o conceito operacional de resposta a desastres). Só entram Art. 1-3 (finalidade/composição/atribuições gerais). |

## 3. Fatia B — reforço da Parte II

### 3.1 Bahia — 17 artigos novos (além dos 3 já usados na Fatia A)
Fonte: `Bahia - Regulamento de Serviço.md`. Faixas (mesmo `slice_between`/`strip_lines` já
configurados na Fatia A):

| Faixa | Tema | Heading |
|---|---|---|
| Art. 1 | disposicoes-preliminares | Portaria — objeto |
| Art. 2 | disposicoes-preliminares | Cap. I — Da Finalidade |
| Art. 3 | disposicoes-preliminares | Cap. II — Dos Objetivos |
| Art. 4 | servico-operacional | Cap. III — Objetivos Básicos do Serviço Operacional |
| Art. 5 | organizacao-geral | Cap. IV — Das Funções Operacionais |
| Art. 6-7, 10-17 | atribuicoes-funcoes | Cap. V — Atribuições (Superior de Dia a Integrantes da Guarnição) |
| Art. 19 | disciplina-correicao | Cap. VI — Das Medidas Disciplinares |
| Art. 20-25 | servico-interno-dia | Cap. VII — Da Passagem de Serviço |
| Art. 26-35 | disposicoes-finais | Disposições Finais (escala, EPI, instrução, vigência) |

### 3.2 Roraima — 97 artigos (documento inteiro)
Fonte: `Roraíma - Regulamento de Serviço.md` (INOp 01/2024). Abertura: heading "CONCEITUAÇÃO
BÁSICA" (após o Sumário — evita falso-match no índice). Fecho: "ANEXO ÚNICO". Faixas: ver
tabela completa levantada na leitura de fonte (Art. 1 a 97, cobrindo os 9 capítulos de funções
de dia — Superior, Coordenador, Oficial de Dia, Incêndio/Salvamento/EPH, Comunicação, Saúde,
Correições, Sobreaviso — mapeados majoritariamente a `atribuicoes-funcoes`,
`servico-interno-dia`, `pessoal-quadros` [escalas], `servico-operacional` e
`disciplina-correicao`/`disposicoes-finais` nas bordas).

### 3.3 Tocantins — resto do Anexo 2 (7 artigos, além dos 3 já usados)
Faixas dentro do bloco já delimitado por `slice_between=('ANEXO 2', None)`:
- Art. 1-2 → `disposicoes-preliminares`
- Art. 3-5 → `organizacao-geral`
- Art. 6 → `competencias-direcao`
- Art. 7 → `servico-interno-dia`
- Art. 8 → `atribuicoes-funcoes`
- Art. 9-11 → `servico-operacional`
- Art. 15 → `disposicoes-finais`

### 3.4 Alagoas — 5 documentos com corpo articulado (novo UF cada um)
Cada Norma Operacional de AL vira uma entrada de `CONFIG` própria (não é um "estado" novo — é
mais uma fonte de Alagoas; usar chaves como `al-no03`, `al-no04` etc., cada uma com seu próprio
`md`, já que são arquivos separados):

| Doc | Faixas | 
|---|---|
| NO 03 | Art. 1-5 → `servico-operacional`; Art. 5(2ª ocorrência)-6 → `disposicoes-finais` (nota: documento tem "Art. 5º" duplicado no original — extração usa a 2ª ocorrência para a faixa final) |
| NO 04 | Art. 1-2 → `servico-interno-dia`; Art. 3-4 → `disposicoes-finais` |
| NO 06 | Art. 1-3 → `servico-interno-dia`; Art. 4-5 → `disposicoes-finais` |
| NO 07 | Art. 1-2 → `servico-interno-dia`; Art. 3-4 → `disposicoes-finais` |
| NO 11 | Art. 1 → `disposicoes-preliminares`; Art. 2-8 → `servico-interno-dia`; Art. 9-10 → `atribuicoes-funcoes`; Art. 11-12 → `servico-interno-dia`; Art. 13-15 → `ensino-instrucao`; Art. 16-20 → `servico-operacional`; Art. 21-23 → `disposicoes-finais` |

## 4. Fatia C — RISG reforça Parte I (cerimonial-honras, pessoal-quadros)

### 4.1 Pré-requisito: trazer o RISG para o pipeline oficial
O RISG (`LEGISLAÇÃO CBMS/RISG.pdf`) ainda não foi convertido pelo `convert_to_markdown.py`
oficial (só existe um `.txt` ad-hoc em scratchpad, que não sobrevive entre sessões). Rodar o
conversor para gerar `database/markdown/RISG.md` de forma permanente e rastreável.

### 4.2 RISG como pseudo-fonte (não é um "estado" do CBM)
O RISG não é uma legislação estadual — é o regulamento do Exército Brasileiro. Para caber na
mesma arquitetura (`REGULAMENTO_DOCS`/`STATE_NAMES`, chaveados por "uf"), ele entra como uma
chave própria `risg`, rotulada honestamente: `STATE_NAMES['risg'] = 'Exército Brasileiro'`,
`REGULAMENTO_DOCS['risg'] = {'label': 'RISG — R-1 (Portaria SGEx nº 51/2003)', 'md': 'RISG.md'}`.
Ele SÓ entra como **alternativa** (nunca primária) nos dois temas — os primárias continuam
sendo RS (cerimonial) e RN (pessoal). Como alternativa, o texto aparece SEM adaptação
(convenção já usada no projeto: alternativas mostram o original de cada fonte) — o leitor vê
claramente que é o texto do Exército, rotulado como tal.

### 4.3 Faixas (numeração do RISG é ÚNICA e contínua, 1-477 — sem colisão)
- `cerimonial-honras`: Art. 321-327 (símbolos nacionais, exata), Art. 337-343 (festas
  nacionais, exata), Art. 344-348 (festas militares específicas do Exército, **parcial** —
  estrutura reaproveitável, conteúdo específico não), Art. 461-462 (honras militares, **parcial**
  — raso, remete a outro regulamento).
- `pessoal-quadros`: Art. 364-375 (cargo/função militar, exata), Art. 376-385 (substituições —
  normas gerais + guarnições, exata), Art. 391-410 (substituições entre oficiais e praças,
  exata), Art. 411-414 (qualificação das praças, exata).

## 5. Fatia D — ES reforça servico-operacional e seguranca-contra-incendio

Fonte: `Espírito Santo - Normas Gerais de Ação.md`. **Numeração de "Art. N" reinicia a cada
órgão/unidade** — não dá para usar `slice_between` + `ranges` simples (colidiria com dezenas de
outros "Art. 9", "Art. 16" etc. do resto do documento). Usa o modo `line_slices` do extrator
(faixas por LINHA ABSOLUTA do arquivo, já suportado por `extrair_regulamentos.py`), com 4
blocos, linhas confirmadas por grep direto na fonte:

| Bloco | Linhas (absolutas) | Tema | Conteúdo |
|---|---|---|---|
| CAT | 11053–11136 | seguranca-contra-incendio | Art. 16-17 — Gerência de Vistorias, Seção de Fiscalização |
| 1º BBM (prontidão/SOS) | 12424–12454 | servico-operacional | Art. 9-10 — definição de prontidão operacional + SOS |
| 1º BBM (chefia SOS) | 13573–13701 | servico-operacional | Art. 30-31 — Chefe da SOS, Fiscal do Salvamar |
| CERD | 32072–32246 | servico-operacional | Art. 1-3 — finalidade, composição, atribuições gerais |

Usa só o **1º BBM** como representante (os outros 5 batalhões repetem o mesmo texto-base com
nomes de área trocados — extrair um basta; extrair os 6 seria redundância, não reforço).

## 6. Arquitetura (igual às Fatias A/1 — nenhum mecanismo novo, exceto D)
- B e C: mesmo modo `extract_ranges` (faixa de Art. N dentro de um `slice_between`), já usado
  desde a Fase 1.
- D: mesmo modo `extract_line_slices` que já existe no extrator (usado hoje só implicitamente
  por outros CONFIGs atípicos) — primeira vez que usamos explicitamente para um documento
  "órgão-por-órgão" como o ES.
- Todas passam por `verificar_verbatim.py` antes do rebuild.
- `PRIMARY_SOURCE` não muda nesta rodada (B/C/D só adicionam `alternatives`, exceto onde a
  fonte primária de um tema ainda não existisse — não é o caso aqui).

## 7. Não-objetivos (YAGNI)
- Não mexer no 16º tema (`central-operacoes-193`) — já fechado na Fatia A.
- Não mudar a divisão 12 Geral / 4 Serviço.
- Não adaptar automaticamente o texto do RISG (fica cru, como alternativa rotulada).
- Não tentar resolver a colisão de Tocantins nem os 4 DOBs de Alagoas nesta rodada — ficam
  como pendência explícita.

## 8. Testes
- `test_regulamento_structure.py`: manter as invariantes existentes (16 capítulos, editIds
  únicos); adicionar checagem de que o total de artigos cresce de 413 para o número final
  (a confirmar após extração) e que `risg` aparece como alternativa em cerimonial-honras e
  pessoal-quadros, nunca como primária.
- `verificar_verbatim.py` verde para todo o conteúdo novo.
- `node --test` continua verde (nenhuma mudança JS nesta fase).

## 9. Riscos
- **Volume de Roraima** (97 artigos): maior lote de uma vez; mitigar validando a contagem
  exata pós-extração antes de prosseguir.
- **RISG como pseudo-estado**: pode confundir a UI do comparador (aparecer "Exército
  Brasileiro" ao lado dos 27 estados). Aceitável e transparente — rótulo explícito evita
  qualquer ambiguidade. Sinalizar ao Wândrio na entrega.
- **`line_slices` para ES**: primeira vez usado deliberadamente para um documento
  "órgão-por-órgão"; testar a extração isoladamente antes de aceitar.
