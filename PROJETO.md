# Portal de Legislação dos Corpos de Bombeiros Militares

**Documentação Técnica e Funcional — versão 1.5.0**

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
11. [Histórico de Versões](#11-histórico-de-versões)

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

### 2.1 Instrumentos Normativos por Estado

> **Nota sobre os arquivos PDF:** Todos os 31 arquivos de legislação fornecidos como base de dados são **PDFs com texto digital extraível** (não são imagens escaneadas), com exceção do `Amazonas-OrganizaçãoBásica.pdf` (14 páginas de imagem escaneada, sem texto extraível — estado não incluído nos 19 do portal). Os demais arquivos foram gerados por Microsoft Word, Ghostscript, PDF24 ou impressão direta do navegador, e possuem de 3 a 854 páginas em formato A4.

Cada estado possui o campo **Base Legal** preenchido com o número completo, data e ementa do instrumento normativo de referência, extraído diretamente dos arquivos de legislação.

| Estado | Instrumento Normativo | Tipo |
|---|---|---|
| AL | Lei n.º 6.212, de 26/12/2000 (reg. pelo Decreto n.º 408/2001) | Lei Ordinária |
| CE | Lei n.º 13.438, de 07/01/2004 | Lei Ordinária |
| DF | Portaria n.º 24, de 25/11/2020 | Portaria (Regimento Interno) |
| ES | Lei Estadual n.º 9.220, de 17/06/2009 | Lei Ordinária |
| MA | Lei n.º 8.508, de 27/11/2006 | Lei Ordinária |
| MG | Lei Complementar n.º 54, de 13/12/1999 | Lei Complementar |
| MS | Lei Complementar n.º 188, de 03/04/2014 | Lei Complementar |
| MT | Lei Complementar n.º 775, de 27/09/2023 | Lei Complementar |
| PA | Lei n.º 11.060, de 01/07/2025 | Lei Ordinária |
| PB | Lei Complementar n.º 191, de 26/04/2024 | Lei Complementar |
| PE | Lei n.º 15.187, de 12/12/2013 | Lei Ordinária |
| PI | Lei n.º 7.772, de 04/04/2022 | Lei Ordinária |
| PR | Lei n.º 22.206, de 29/11/2024 | Lei Ordinária |
| RJ | Lei n.º 250, de 02/07/1979 | Lei Ordinária |
| RO | Minuta de Projeto de Lei n.º 0059262482 (abril/2025) — *em tramitação* | Minuta |
| RS | Decreto n.º 53.897, de 25/01/2018 (reg. LC n.º 14.920/2016) | Decreto |
| SC | Lei Complementar n.º 724, de 18/07/2018 | Lei Complementar |
| SE | Lei n.º 8.979, de 03/02/2022 | Lei Ordinária |
| TO | Lei Complementar n.º 131, de 30/09/2021 | Lei Complementar |

> **Atenção:** O estado de Rondônia (RO) está baseado em minuta de projeto de lei ainda não promulgada (abril/2025). Os dados devem ser atualizados quando a lei for sancionada.

---

## 3. Arquitetura do Sistema

O sistema opera como uma **aplicação monolítica Node.js** com dois servidores integrados: um servidor **Express** que serve a API REST e as rotas tRPC, e um servidor **Vite** que serve o frontend React em desenvolvimento. Em produção, o Vite compila o frontend e o Express serve os arquivos estáticos.

A comunicação entre frontend e backend ocorre exclusivamente via **tRPC**, garantindo tipagem de ponta a ponta sem necessidade de contratos manuais. As exceções são as rotas de exportação PDF (`GET /api/pdf/positions` e `GET /api/pdf/comparative`), implementadas como rotas Express convencionais por exigirem streaming de resposta binária.

```
Cliente (React 19 + Tailwind 4)
        │
        │  tRPC (JSON-RPC sobre HTTP)
        ▼
Servidor Express 4
        ├── /api/trpc/*     → Procedimentos tRPC (dados)
        ├── /api/pdf/*      → Rotas Express (exportação PDF)
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
| `acronym` | VARCHAR(50) | Sigla do órgão (ex: CO) |
| `subdivisions` | TEXT | Subdivisões/desdobramentos (JSON array) |
| `attributions` | TEXT | Atribuições do órgão (JSON array) |
| `detailLevel` | ENUM | Nível de detalhamento: `detalhado`, `moderado`, `basico` |
| `legalBasis` | VARCHAR(500) | Base legal completa (número, data e ementa) |
| `legalArticle` | VARCHAR(200) | Artigo(s) de referência na legislação |
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
| `acronym` | VARCHAR(50) | Sigla do cargo |
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

### 5.2 Rotas REST de Exportação PDF

| Método | Rota | Parâmetros | Descrição |
|---|---|---|---|
| `GET` | `/api/pdf/positions` | `category` (obrigatório), `siglas` (opcional, separado por vírgula) | Gera e baixa o PDF do comparativo de cargos |
| `GET` | `/api/pdf/comparative` | `siglas` (obrigatório, separado por vírgula, máx. 5) | Gera e baixa o PDF do comparativo de CO e DAT |

**Exemplos de uso:**

```
GET /api/pdf/positions?category=chefe-co
GET /api/pdf/positions?category=chefe-dat&siglas=RO,MT,MS,DF,MG
GET /api/pdf/comparative?siglas=RO,MT,MS
```

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

Página dedicada a cada estado com todas as informações disponíveis: dados do CO (nomenclatura, sigla, base legal completa, artigo de referência, desdobramentos, atribuições, cargos vinculados) e da DAT (mesma estrutura). Exibe os cargos e funções em cards expansíveis com posto/graduação, subordinação e atribuições.

### 6.4 Comparativo (`/comparativo`)

Permite selecionar de 1 a 5 estados e exibir uma tabela comparativa lado a lado com os dados do CO e da DAT de cada estado selecionado. O seletor de estados é organizado por região geográfica (Norte, Nordeste, Centro-Oeste, Sudeste, Sul). Inclui botão **"Exportar PDF"** que baixa o comparativo em formato PDF. Cada card exibe a seção **"Artigo Legal de Origem"** com o artigo de referência na legislação.

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
│       │   ├── AppLayout.tsx         ← Layout com cabeçalho institucional e sidebar
│       │   └── ui/                   ← Componentes shadcn/ui
│       ├── hooks/
│       │   └── usePDFExport.ts       ← Hook de exportação PDF (fetch + Blob download)
│       └── pages/
│           ├── Home.tsx              ← Dashboard com indicadores
│           ├── Estados.tsx           ← Listagem com filtros
│           ├── EstadoDetalhe.tsx     ← Detalhes por estado (com artigo legal)
│           ├── Comparativo.tsx       ← Comparativo lado a lado (seletor por região)
│           ├── ComparativoCargos.tsx ← Comparativo por cargo (chefe-co / chefe-dat)
│           └── Sobre.tsx             ← Sobre o portal
├── drizzle/
│   ├── schema.ts                     ← Definição das tabelas (Drizzle ORM)
│   └── relations.ts                  ← Relações entre tabelas
├── server/
│   ├── db.ts                         ← Helpers de consulta ao banco
│   ├── routers.ts                    ← Procedimentos tRPC
│   ├── pdfRouter.ts                  ← Rotas Express de exportação PDF (pdfkit)
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
2. Inserir o Comando Operacional na tabela `operational_commands` com `stateId` correspondente, preenchendo `legalBasis` com o número e data completos da lei/decreto.
3. Inserir a Diretoria de Atividades Técnicas na tabela `technical_directorates` com `stateId` correspondente.
4. Inserir os cargos na tabela `positions` vinculados ao `operationalCommandId` ou `technicalDirectorateId`, definindo `positionCategory` como `chefe-co` ou `chefe-dat` para o titular.

### Adicionar uma nova categoria de cargo

A coluna `positionCategory` em `positions` aceita qualquer string. Para criar uma nova categoria comparável (ex: `adj-co` para adjuntos do CO), basta inserir os registros com o valor desejado. A página **Cargos e Funções** precisará ser atualizada para incluir o novo filtro na interface.

### Atualizar a base legal de um estado

Quando uma lei for revogada ou substituída, atualizar o campo `legalBasis` nas tabelas `operational_commands` e `technical_directorates` do estado correspondente via SQL:

```sql
UPDATE operational_commands SET legalBasis = 'Lei n.º XXXXX, de DD/MM/AAAA — ...' WHERE stateId = (SELECT id FROM states WHERE sigla = 'XX');
UPDATE technical_directorates SET legalBasis = 'Lei n.º XXXXX, de DD/MM/AAAA — ...' WHERE stateId = (SELECT id FROM states WHERE sigla = 'XX');
```

### Proteger funcionalidades com autenticação

A infraestrutura de autenticação já está disponível. Para proteger um procedimento tRPC, substituir `publicProcedure` por `protectedProcedure` em `server/routers.ts`. Para criar funcionalidades exclusivas de administrador, usar o padrão `adminProcedure` com verificação de `ctx.user.role`.

---

## 11. Histórico de Versões

| Versão | Data | Principais Mudanças |
|---|---|---|
| 1.0.0 | maio/2026 | Versão inicial: 19 estados, CO e DAT, filtros, comparativo, detalhes por estado |
| 1.1.0 | maio/2026 | Expansão: tabela `positions` com cargos e funções; página Cargos e Funções |
| 1.2.0 | maio/2026 | Exportação PDF (pdfkit); comparativo PDF; layout dinâmico de colunas |
| 1.3.0 | maio/2026 | Redesign identidade visual CBMRO; cabeçalho institucional; fonte Josefin Sans |
| 1.4.0 | maio/2026 | Desdobramentos reais dos 19 estados; base legal completa (número e data); artigo de origem; seletor por região; correções de layout mobile; remoção do brasão duplicado |
| 1.5.0 | maio/2026 | Correção dos desdobramentos de AL (DST: seções conforme Art. 60–64 do Regimento Interno); varredura e validação dos PDFs de legislação (31 arquivos, todos com texto digital extraível, exceto Amazonas que é imagem escaneada); publicação no GitHub |

---

*Documentação gerada em maio de 2026 — Portal de Legislação dos Corpos de Bombeiros Militares — CBMRO*
