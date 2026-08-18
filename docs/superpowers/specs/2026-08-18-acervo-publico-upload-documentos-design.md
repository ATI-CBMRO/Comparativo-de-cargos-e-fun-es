# Acervo público — upload de documentos pelo visitante + caixa de entrada do admin

**Data:** 2026-08-18
**Origem:** pedido do Ten. Tiago — a finalidade do perfil público (visitante sem login,
`docs/superpowers/specs/2026-08-18-acervo-publico-visitante-design.md`) não é só consulta:
é também dar a militares de **outros Corpos de Bombeiros Militares** um caminho para
**contribuir** com legislações que ainda não estão relacionadas no acervo. Um campo único de
envio, compartilhado por todos os visitantes (não um campo por CBM); a curadoria de cada
arquivo — decidir se e como ele entra no acervo — continua manual, feita pelo administrador.

## Requisitos fixados com o Ten. Tiago (2026-08-18)

| Decisão | Escolha |
|---|---|
| O que o admin faz com o arquivo, dentro do app | **Só uma caixa de entrada**: vê, baixa, remove. Nenhum fluxo de status (pendente/aprovado/rejeitado) — a inclusão no acervo em si continua pelo processo manual já existente (`/ingerir-legislacao`), fora do app |
| Metadados que o visitante preenche | **Estado/CBM (texto livre) + tipo de documento (LOB / Regimento Interno / Regulamento de Serviço / Outro) + observação opcional** |
| Tipo e tamanho de arquivo | **Só PDF, até 20 MB** |
| Limpeza da caixa de entrada | **Admin remove item a item**, depois de baixar/processar — apaga o metadado no Firestore e o arquivo no Storage junto, sem deixar lixo órfão |

## Por que Firebase Storage (não é escolha de produto, é a única opção sólida)

Guardar o PDF direto num documento do Firestore não é viável — documentos do Firestore têm
limite de **1 MB**, e o requisito é até 20 MB. O pacote `firebase` (v11.10.0) já é dependência
do projeto e inclui o SDK de Storage; nenhuma dependência nova, nenhuma conta nova. A
alternativa de apontar o visitante para um formulário externo (Google Forms, por exemplo)
evitaria construir isto no app, mas fragmentaria a experiência — o visitante sairia do portal
— e o Ten. Tiago já pediu explicitamente "um campo" dentro do sistema. Não é apresentada como
opção viva, só registrada aqui como a alternativa mais barata que existiria se a decisão um dia
for revista.

## 1. Fluxo

Visitante identificado (mesmo `useVisitante()` já construído — não pede cadastro de novo)
abre uma terceira aba dentro da casca pública, **"Enviar documento"**, ao lado de "Acervo
Legal" e "Busca". Preenche estado/CBM, tipo de documento, observação opcional, anexa um PDF.
Ao enviar: o arquivo vai para o Storage, um documento de metadados vai para o Firestore, e o
visitante vê uma confirmação simples. O admin vê tudo isso como uma seção nova em `/acessos`,
baixa o que quiser pelo link, e remove da lista quando já tiver processado — o processamento
em si (decidir se o documento entra no acervo, rodar o pipeline de ingestão) continua manual,
fora do escopo desta entrega.

## 2. Formulário de envio — `src/pages/EnviarDocumento.jsx`

Nova página, montada em `/acervo-publico/enviar`, dentro da mesma `AcervoPublico.jsx`
(reaproveita o `visitante` do contexto — sem re-cadastro). Campos:

- **Estado/CBM** — texto livre (ex. "CBMPA"), obrigatório.
- **Tipo de documento** — seletor com as mesmas categorias já usadas no Acervo Legal (LOB,
  Regimento Interno, Regulamento de Serviço, Outro), obrigatório.
- **Observação** — texto livre, opcional.
- **Arquivo** — `<input type="file" accept="application/pdf">`, obrigatório.

Validação no cliente antes de gastar banda: obrigatoriedade dos três campos + arquivo;
`file.type === 'application/pdf'`; `file.size <= 20 * 1024 * 1024`. Mensagem de erro
específica para cada caso (campo faltando / tipo errado / tamanho excedido), sempre visível
na tela, nunca só no console. Depois do envio bem-sucedido: mensagem de confirmação
("Recebido, obrigado — o documento entra na fila de análise") e o formulário limpa para
permitir novo envio na mesma visita.

## 3. Armazenamento

**Storage**, caminho `uploads-visitantes/{uid-do-visitante}/{timestamp}-{nome-do-arquivo}`
— prefixado pelo próprio uid, que é exatamente o que a regra de segurança do Storage vai
usar para autorizar a escrita (seção 4).

**Firestore**, coleção nova `uploadsVisitantes/{id}` (id automático):

| Campo | Tipo | Origem |
|---|---|---|
| `uid` | string | sessão anônima do visitante |
| `nomeVisitante` | string | `useVisitante()` |
| `emailVisitante` | string | `useVisitante()` — ver nota abaixo |
| `estado` | string | formulário |
| `tipoDocumento` | string | formulário |
| `observacao` | string | formulário (pode ser vazio) |
| `storagePath` | string | caminho gerado no upload |
| `nomeArquivo` | string | nome original do arquivo |
| `tamanho` | number | bytes |
| `criadoEm` | timestamp | `serverTimestamp()` |

**Nota — extensão necessária ao `VisitanteProvider` existente:** hoje `useVisitante()`
expõe só `{ uid, nome }` (`src/lib/visitante.jsx`, entrega anterior) — o e-mail é gravado no
Firestore durante o cadastro, mas não fica retido no estado/contexto do app, e a regra atual
de `visitantes/{uid}` só permite **leitura pelo admin** (`allow read, delete: if isAdmin()`),
não pelo próprio visitante. Ou seja, não dá para "ler de volta" o e-mail do Firestore no
momento do upload sem afrouxar essa regra — e a entrega anterior decidiu deliberadamente não
conceder essa leitura ("o visitante também não lê o próprio documento: não precisa, e a
regra não concede"). Esta entrega **estende** `normalizarVisitante`/`entrar()`/
`lerVisitanteLocal`/`gravarVisitanteLocal` (`src/lib/visitante.js` e `visitante.jsx`) para
também reter `email` no estado local — o mesmo dado que a pessoa acabou de digitar no
cadastro, sem leitura nova ao Firestore e sem tocar a regra de `visitantes/{uid}`.

## 4. Regras de segurança — duas frentes

**Firestore** (`firestore.rules`, bloco novo `match /uploadsVisitantes/{id}`, mesmo padrão
do bloco `visitantes` já existente): visitante só **cria** (nunca atualiza) um documento com
`uid == request.auth.uid`; campos obrigatórios validados (`estado`/`tipoDocumento` não
vazios, tamanhos máximos, `keys().hasOnly([...])`); só o admin **lê e apaga**.

**Storage** (`storage.rules` — **arquivo novo neste projeto**; hoje não existe nenhuma regra
de Storage porque nada usava Storage até aqui, então é mais uma publicação manual no console,
como já acontece com `firestore.rules`): visitante só escreve dentro da própria pasta
`uploads-visitantes/{uid}/...`, com `request.resource.size < 20 * 1024 * 1024` e
`request.resource.contentType == 'application/pdf'` reforçados na regra (não só no cliente
— um cliente adulterado não pode burlar o limite); só o admin lê. A regra do Storage
referencia o Firestore com `firestore.get(/databases/(default)/documents/members/$(...))`
para checar `role == 'admin'`, o mesmo dado que `isAdmin()` já usa do lado do Firestore —
suportado nativamente pelo Firebase (regras de Storage podem consultar Firestore).
**Ressalva:** este é o primeiro uso de Storage Rules neste projeto — a sintaxe exata de
`firestore.get()` a partir de uma regra de Storage precisa ser conferida contra a
documentação atual do Firebase durante a implementação; não há como testar isso sem um
projeto Firebase ao vivo (mesma limitação já registrada nas entregas anteriores).

## 5. Caixa de entrada do admin — `/acessos`

Nova seção, "Documentos enviados por visitantes", no mesmo estilo de tabela das seções que
já existem na página (`.acc-panel`/`.acc-table`): estado, tipo, quem enviou (nome + e-mail),
observação, tamanho, data, um link **Baixar** (URL de download do Storage,
`getDownloadURL`) e um botão **Remover**. Remover apaga os dois lados — o documento no
Firestore **e** o objeto no Storage — numa operação só, para não deixar arquivo órfão
consumindo cota sem metadado que aponte pra ele.

## 6. Erros e limites

Toda falha de rede/permissão no envio aparece como mensagem visível no formulário — nunca
só `console.error` (mesma disciplina AR-04 do resto do projeto,
`docs/superpowers/auditoria-armadilhas.md`). Sem limite de quantidade de envios por
visitante nesta entrega — risco aceito, mesma decisão já tomada para o cadastro (spec do
visitante, seção 7).

## 7. Fora de escopo (de propósito)

Processamento automático do PDF (OCR, classificação por conteúdo, entrada automática no
acervo) — continua manual, pelo pipeline `/ingerir-legislacao` já existente. Fluxo de
status dentro do app (pendente/aprovado/rejeitado/integrado). Notificação por e-mail ao
admin quando chega um envio novo. Limite de envios por pessoa ou por dia. Se algum desses
importar depois, é entrega própria.
