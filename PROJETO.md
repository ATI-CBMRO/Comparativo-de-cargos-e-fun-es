# Portal de Legislação dos Corpos de Bombeiros Militares

**Documentação Técnica e Funcional — versão 1.3.0**

Desenvolvido por: Assessoria Técnica Institucional — CBMRO
Última atualização: maio de 2026

---

## Sumário

1. [Visão Geral](#1-visão-geral)
2. [Cobertura de Dados](#2-cobertura-de-dados)
3. [Arquitetura do Sistema](#3-arquitetura-do-sistema)
4. [Banco de Dados](#4-banco-de-dados)
5. [API Backend](#5-api-backend)
6. [Páginas e Funcionalidades](#6-páginas-e-funcionalidades)
7. [Exportação PDF](#7-exportação-pdf)
8. [Estrutura de Arquivos](#8-estrutura-de-arquivos)
9. [Testes Automatizados](#9-testes-automatizados)
10. [Guia de Expansão](#10-guia-de-expansão)

---

## 1. Visão Geral

O **Portal de Legislação dos Corpos de Bombeiros Militares** é uma aplicação web institucional desenvolvida para o Corpo de Bombeiros Militar de Rondônia (CBMRO) com o objetivo de centralizar e comparar as estruturas organizacionais dos Corpos de Bombeiros Militares brasileiros, com foco nos **Comandos Operacionais** e nas **Diretorias de Atividades Técnicas** de cada estado.

O portal permite que assessores técnicos e gestores institucionais realizem comparações entre nomenclaturas, siglas, postos/graduações, subordinações, desdobramentos e atribuições dos principais órgãos de direção setorial dos CBMs, com base em fontes legislativas primárias (Leis de Organização Básica, Regimentos Internos e Normas Gerais de Ação).

A aplicação foi construída sobre uma stack moderna: **React 19 + Tailwind 4 + Express 4 + tRPC 11**, com banco de dados MySQL/TiDB gerenciado pela plataforma Manus.

---

## 2. Cobertura de Dados

O portal cobre **19 estados brasileiros**, distribuídos pelas cinco regiões do país. Cada estado possui registro do **Comando Operacional (CO)** e da **Diretoria de Atividades Técnicas (DAT)**, com nível de detalhamento variável conforme a disponibilidade e especificidade das legislações consultadas.

| Região | Estados Cobertos |
|---|---|
| Norte | PA, RO, TO |
| Nordeste | AL, CE, MA, PB, PE, PI, SE |
| Centro-Oeste | DF, MT, MS |
| Sudeste | ES, MG, RJ |
| Sul | PR, RS, SC |

O nível de detalhamento de cada registro segue a seguinte classificação:

| Nível | Descrição |
|---|---|
| **Detalhado** | Nomenclatura, sigla, posto/graduação, subordinação, desdobramentos e atribuições completas |
| **Moderado** | Nomenclatura, sigla, posto/graduação e subordinação, com desdobramentos parciais |
| **Básico** | Apenas nomenclatura e competências gerais, sem cargos subordinados detalhados |

---

## 3. Arquitetura do Sistema

O sistema opera como uma **aplicação monolítica Node.js** com dois servidores integrados: um servidor **Express** que serve a API REST e as rotas tRPC, e um servidor **Vite** que serve o frontend React em desenvolvimento. Em produção, o Vite compila o frontend e o Express serve os arquivos estáticos.

A comunicação entre frontend e backend ocorre exclusivamente via **tRPC**, garantindo tipagem de ponta a ponta sem necessidade de contratos manuais. A única exceção é a rota de exportação PDF (`GET /api/pdf/positions`), implementada como rota Express convencional por exigir streaming de resposta binária.

```
Cliente (React 19 + Tailwind 4)
        │
        │  tRPC (JSON-RPC sobre HTTP)
        ▼
Servidor Express 4
        ├── /api/trpc/*     → Procedimentos tRPC (dados)
        ├── /api/pdf/*      → Rota Express (exportação PDF)
        ├── /api/oauth/*    → Autenticação Manus OAuth
        └── /manus-storage/ → Proxy de arquivos S3
        │
        ▼
Banco de Dados MySQL/TiDB (Manus)
```

A autenticação é gerenciada pelo **Manus OAuth**, com sessão via cookie JWT assinado. O portal é atualmente de acesso público (sem restrição de login para leitura), com a infraestrutura de autenticação disponível para futuras funcionalidades protegidas.

---

## 4. Banco de Dados

O banco de dados é composto por cinco tabelas principais. O schema completo está em `drizzle/schema.ts`.

### 4.1 Tabela `states`

Armazena os dados cadastrais de cada estado.

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INT PK | Identificador único |
| `name` | VARCHAR(100) | Nome completo do estado |
| `sigla` | VARCHAR(2) UNIQUE | Sigla do estado (ex: RO) |
| `region` | ENUM | Região geográfica |
| `corporationName` | VARCHAR(200) | Nome oficial do Corpo de Bombeiros |
| `legislationDocuments` | TEXT | Documentos legislativos consultados |

### 4.2 Tabela `operational_commands`

Armazena os dados do Comando Operacional (ou equivalente) de cada estado.

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INT PK | Identificador único |
| `stateId` | INT FK | Referência ao estado |
| `nomenclature` | VARCHAR(300) | Nome do órgão (ex: Comando Operacional) |
| `acronym` | VARCHAR(50) | Sigla do órgão (ex: COMOP) |
| `subdivisions` | TEXT | Subdivisões/desdobramentos (JSON array ou separado por `;`) |
| `attributions` | TEXT | Atribuições do órgão (JSON array ou separado por `;`) |
| `detailLevel` | ENUM | Nível de detalhamento: `detalhado`, `moderado`, `basico` |
| `legalBasis` | VARCHAR(300) | Base legal (lei, decreto, portaria) |
| `notes` | TEXT | Observações adicionais |

### 4.3 Tabela `technical_directorates`

Estrutura idêntica à `operational_commands`, referente à Diretoria de Atividades Técnicas (ou equivalente) de cada estado.

### 4.4 Tabela `positions`

Armazena os cargos e funções vinculados a cada Comando Operacional ou Diretoria de Atividades Técnicas. Cada registro representa um cargo específico (ex: Chefe do Órgão Operacional, Adjunto, Chefe de Seção).

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INT PK | Identificador único |
| `operationalCommandId` | INT FK (nullable) | Vínculo com o CO |
| `technicalDirectorateId` | INT FK (nullable) | Vínculo com a DAT |
| `title` | VARCHAR(200) | Denominação do cargo (ex: Comandante Operacional) |
| `acronym` | VARCHAR(50) | Sigla do cargo (ex: Cmt COMOP) |
| `rank` | VARCHAR(100) | Posto ou graduação exigido |
| `subordinateTo` | VARCHAR(200) | A quem o cargo é subordinado |
| `subordinates` | TEXT | Cargos/órgãos subordinados (JSON array ou `;`) |
| `attributions` | TEXT | Atribuições do cargo (JSON array ou `;`) |
| `positionCategory` | VARCHAR(100) | Categoria para comparativo: `chefe-co`, `chefe-dat`, `adj-co`, `adj-dat` |
| `sortOrder` | INT | Ordem de exibição |

### 4.5 Tabela `users`

Gerenciada automaticamente pelo Manus OAuth. Armazena usuários autenticados com campo `role` (`user` ou `admin`) para controle de acesso futuro.

---

## 5. API Backend

### 5.1 Procedimentos tRPC

Todos os procedimentos são públicos (`publicProcedure`) e acessíveis sem autenticação. O prefixo de URL é `/api/trpc`.

| Procedimento | Entrada | Descrição |
|---|---|---|
| `states.list` | — | Lista todos os estados com CO e DAT |
| `states.details` | `{ sigla: string }` | Detalhes completos de um estado, incluindo cargos |
| `dashboard.stats` | — | Estatísticas gerais (totais por nível de detalhamento) |
| `data.allStates` | — | Lista simplificada de estados (sigla, nome, região) |
| `data.filtered` | `{ siglas?, detailLevel?, orgType?, search? }` | Dados filtrados por estado, nível, tipo de órgão ou busca textual |
| `data.positionTypes` | — | Lista as categorias de cargos disponíveis no banco |
| `data.comparePositions` | `{ category: string, siglas?: string[] }` | Comparativo de cargos por categoria entre estados |
| `data.comparative` | `{ siglas: string[] }` | Comparação completa de CO e DAT entre 1 a 5 estados selecionados |
| `auth.me` | — | Retorna o usuário autenticado ou `null` |
| `auth.logout` | — | Encerra a sessão (limpa o cookie JWT) |

### 5.2 Rota REST de Exportação PDF

| Método | Rota | Parâmetros | Descrição |
|---|---|---|---|
| `GET` | `/api/pdf/positions` | `category` (obrigatório), `siglas` (opcional, separado por vírgula) | Gera e baixa o PDF do comparativo de cargos |

**Exemplos de uso:**

```
GET /api/pdf/positions?category=chefe-co
GET /api/pdf/positions?category=chefe-dat&siglas=RO,MT,MS,DF,MG
```

Os valores aceitos para `category` são: `chefe-co` (Chefe do Órgão Operacional) e `chefe-dat` (Chefe do Órgão Técnico).

---

## 6. Páginas e Funcionalidades

### 6.1 Dashboard (`/`)

Página inicial com indicadores gerais do portal: total de estados analisados, quantidade com detalhamento completo no CO e na DAT, regiões representadas, e distribuição por nível de detalhamento em barras de progresso. Exibe a lista de todos os estados com links diretos para os detalhes.

### 6.2 Estados (`/estados`)

Listagem completa dos 19 estados com filtros combinados:

- **Filtro por região** — Norte, Nordeste, Centro-Oeste, Sudeste, Sul
- **Filtro por nível de detalhamento** — Detalhado, Moderado, Básico (aplicável a CO e DAT separadamente)
- **Filtro por tipo de órgão** — Ambos, apenas CO, apenas DAT
- **Busca textual** — pesquisa por nomenclatura, sigla ou atribuição em todos os campos

### 6.3 Detalhes do Estado (`/estado/:sigla`)

Página dedicada a cada estado com todas as informações disponíveis: dados do CO (nomenclatura, sigla, base legal, desdobramentos, atribuições, cargos vinculados) e da DAT (mesma estrutura). Exibe os cargos e funções em cards expansíveis com posto/graduação, subordinação e atribuições.

### 6.4 Comparativo (`/comparativo`)

Permite selecionar de 1 a 5 estados e exibir uma tabela comparativa lado a lado com os dados do CO e da DAT de cada estado selecionado. Inclui botão **"Exportar PDF"** que baixa o comparativo em formato PDF.

### 6.5 Cargos e Funções (`/comparativo-cargos`)

Comparativo especializado no titular do órgão (Chefe do CO ou Chefe da DAT) entre todos os estados. Funcionalidades:

- **Dois filtros fixos** — "Chefe do Órgão Operacional" e "Chefe do Órgão Técnico"
- **Filtro por estado** — seleção múltipla organizada por região; sem seleção exibe todos os estados
- **Expansão de atribuições** — botão "Expandir atribuições" expande todos os cards simultaneamente
- **Exportar PDF** — gera PDF formatado com os cards visíveis (filtro e estados selecionados)

### 6.6 Sobre o Portal (`/sobre`)

Página informativa com a metodologia de levantamento, fontes legislativas utilizadas, limitações do estudo e informações de contato institucional.

---

## 7. Exportação PDF

A exportação PDF é gerada no **servidor** (Node.js) usando a biblioteca `pdfkit`, sem dependência de renderização no browser. Essa abordagem foi adotada porque bibliotecas de captura de tela como `html2canvas` não suportam o formato de cor `oklch` utilizado pelo Tailwind CSS 4.

O PDF gerado possui as seguintes características:

- **Formato A4** com margens de 28pt
- **Cabeçalho institucional** em azul-marinho com título, subtítulo (tipo de cargo) e data/hora de geração
- **Faixa vermelha** separando o cabeçalho do conteúdo
- **Layout em duas colunas** com cards individuais por estado
- **Card por estado** contendo: sigla e nome do estado, nome do CBM, cargo/função, sigla do cargo, posto/graduação, subordinação, subdivisões/desdobramentos e até 3 atribuições (com indicação de quantas foram omitidas)
- **Rodapé** com identificação institucional em todas as páginas
- **Paginação automática** com número de página no cabeçalho

O download é iniciado automaticamente pelo browser via `Blob URL` após a requisição ao servidor. O usuário recebe feedback visual via toast: "Gerando PDF..." durante o processamento e "PDF gerado com sucesso!" ao concluir.

---

## 8. Estrutura de Arquivos

```
bombeiros-legislacao-portal/
├── client/
│   ├── index.html                    ← HTML base (Google Fonts via <link>)
│   └── src/
│       ├── App.tsx                   ← Roteamento e layout global
│       ├── index.css                 ← Tema institucional (azul/vermelho, dark/light)
│       ├── components/
│       │   ├── AppLayout.tsx         ← Layout com sidebar de navegação
│       │   └── ui/                   ← Componentes shadcn/ui
│       ├── hooks/
│       │   └── usePDFExport.ts       ← Hook de exportação PDF (fetch + Blob download)
│       └── pages/
│           ├── Home.tsx              ← Dashboard com indicadores
│           ├── Estados.tsx           ← Listagem com filtros
│           ├── EstadoDetalhe.tsx     ← Detalhes por estado
│           ├── Comparativo.tsx       ← Comparativo lado a lado (até 5 estados)
│           ├── ComparativoCargos.tsx ← Comparativo por cargo (chefe-co / chefe-dat)
│           └── Sobre.tsx             ← Sobre o portal
├── drizzle/
│   ├── schema.ts                     ← Definição das tabelas (Drizzle ORM)
│   └── relations.ts                  ← Relações entre tabelas
├── server/
│   ├── db.ts                         ← Helpers de consulta ao banco
│   ├── routers.ts                    ← Procedimentos tRPC
│   ├── pdfRouter.ts                  ← Rota Express de exportação PDF (pdfkit)
│   ├── storage.ts                    ← Helpers de armazenamento S3
│   └── portal.test.ts                ← Testes automatizados (Vitest)
├── shared/
│   └── types.ts                      ← Tipos compartilhados frontend/backend
├── todo.md                           ← Histórico de funcionalidades implementadas
└── PROJETO.md                        ← Esta documentação
```

---

## 9. Testes Automatizados

O projeto possui **23 testes automatizados** implementados com **Vitest**, cobrindo os principais fluxos do backend. Os testes estão em `server/portal.test.ts` e `server/auth.logout.test.ts`.

Para executar os testes:

```bash
pnpm test
```

Os testes cobrem os seguintes cenários:

- Listagem de todos os estados (`states.list`)
- Busca de detalhes por sigla (`states.details`)
- Estatísticas do dashboard (`dashboard.stats`)
- Filtros por nível de detalhamento, tipo de órgão e busca textual (`data.filtered`)
- Listagem de categorias de cargos (`data.positionTypes`)
- Comparativo por categoria de cargo (`data.comparePositions`)
- Comparativo completo entre estados (`data.comparative`)
- Autenticação: logout e estado de sessão

---

## 10. Guia de Expansão

### Adicionar um novo estado

1. Inserir o estado na tabela `states` via SQL ou pela interface do banco de dados do portal.
2. Inserir o Comando Operacional na tabela `operational_commands` com `stateId` correspondente.
3. Inserir a Diretoria de Atividades Técnicas na tabela `technical_directorates` com `stateId` correspondente.
4. Inserir os cargos na tabela `positions` vinculados ao `operationalCommandId` ou `technicalDirectorateId`, definindo `positionCategory` como `chefe-co` ou `chefe-dat` para o titular.

### Adicionar uma nova categoria de cargo

A coluna `positionCategory` em `positions` aceita qualquer string. Para criar uma nova categoria comparável (ex: `adj-co` para adjuntos do CO), basta inserir os registros com o valor desejado. A página **Cargos e Funções** precisará ser atualizada para incluir o novo filtro na interface.

### Adicionar exportação PDF para o Comparativo

A rota `/api/pdf/positions` cobre apenas o comparativo por cargo. Para exportar a comparação lado a lado da página `/comparativo`, é necessário implementar uma nova rota `GET /api/pdf/comparative?siglas=RO,MT,...` em `server/pdfRouter.ts`, seguindo o mesmo padrão da rota existente.

### Proteger funcionalidades com autenticação

A infraestrutura de autenticação já está disponível. Para proteger um procedimento tRPC, substituir `publicProcedure` por `protectedProcedure` em `server/routers.ts`. Para criar funcionalidades exclusivas de administrador, usar o padrão `adminProcedure` com verificação de `ctx.user.role`.

---

*Documentação gerada em maio de 2026 — Portal de Legislação dos Corpos de Bombeiros Militares — CBMRO*
