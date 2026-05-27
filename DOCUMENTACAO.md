# Portal de Legislação dos Corpos de Bombeiros Militares

**Documentação Técnica e de Uso**
Versão 1.0 — Maio de 2026
Elaborado por: Assessoria Técnica Institucional — CBMRO

---

## Sumário

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Objetivos e Escopo](#2-objetivos-e-escopo)
3. [Arquitetura do Sistema](#3-arquitetura-do-sistema)
4. [Banco de Dados](#4-banco-de-dados)
5. [Backend — API tRPC](#5-backend--api-trpc)
6. [Frontend — Interface do Usuário](#6-frontend--interface-do-usuário)
7. [Guia de Uso do Portal](#7-guia-de-uso-do-portal)
8. [Dados Cadastrados](#8-dados-cadastrados)
9. [Critérios de Classificação](#9-critérios-de-classificação)
10. [Manutenção e Atualização de Dados](#10-manutenção-e-atualização-de-dados)
11. [Testes Automatizados](#11-testes-automatizados)
12. [Fontes Documentais](#12-fontes-documentais)

---

## 1. Visão Geral do Projeto

O **Portal de Legislação dos Corpos de Bombeiros Militares** é uma aplicação web institucional desenvolvida para a Assessoria Técnica Institucional do Corpo de Bombeiros Militar de Rondônia (CBMRO). Seu propósito central é consolidar, organizar e disponibilizar de forma consultável e comparativa as informações sobre as estruturas organizacionais dos Corpos de Bombeiros Militares estaduais brasileiros, com foco específico em dois órgãos-chave: o **Comando Operacional** (ou nomenclatura equivalente) e a **Diretoria de Atividades Técnicas** (ou nomenclatura equivalente).

O portal foi construído sobre uma base de dados extraída diretamente das legislações estaduais — Leis de Organização Básica, Regimentos Internos e Normas Gerais de Ação — de 19 estados brasileiros, cobrindo todas as cinco regiões do país. Cada registro reflete fielmente o texto legal de origem, sem inferências ou complementações externas.

A aplicação adota identidade visual institucional nas cores azul-marinho e vermelho, referenciando a tradição dos Corpos de Bombeiros Militares, e foi projetada para uso por gestores, assessores técnicos e pesquisadores que necessitem de subsídios comparativos para o desenvolvimento ou aprimoramento de legislações estaduais.

---

## 2. Objetivos e Escopo

O portal foi concebido para atender a três necessidades principais da assessoria técnica institucional:

**Consulta individualizada** — Permite ao usuário acessar, de forma estruturada e expandida, todas as informações disponíveis sobre a estrutura organizacional de qualquer estado cadastrado, incluindo nomenclatura do órgão, desdobramentos internos, cargos e funções com suas respectivas subordinações hierárquicas e atribuições legais.

**Comparação entre estados** — Oferece uma visualização lado a lado de até cinco estados simultaneamente, permitindo identificar convergências e divergências nas estruturas organizacionais, nomenclaturas e atribuições, o que é especialmente útil no processo de elaboração ou revisão de legislações estaduais.

**Pesquisa textual e filtragem** — Disponibiliza filtros combinados por estado, região geográfica, tipo de órgão (Comando Operacional, Diretoria de Atividades Técnicas ou ambos) e nível de detalhamento legislativo, além de busca textual livre que percorre nomenclaturas, desdobramentos e atribuições.

O escopo do projeto abrange os 19 estados para os quais foram obtidos documentos legislativos com detalhamento suficiente para análise. Estados cujas legislações não apresentavam informações estruturadas sobre os dois órgãos-alvo foram excluídos do banco de dados.

---

## 3. Arquitetura do Sistema

O portal é uma aplicação web full-stack de página única (SPA), composta por três camadas principais que se comunicam de forma tipada de ponta a ponta.

### 3.1 Visão Geral da Stack

| Camada | Tecnologia | Versão |
|---|---|---|
| Frontend | React + Vite | React 19, Vite 7 |
| Estilização | Tailwind CSS | v4 |
| Componentes UI | shadcn/ui + Radix UI | — |
| Roteamento | Wouter | v3 |
| Comunicação cliente-servidor | tRPC | v11 |
| Gerenciamento de estado assíncrono | TanStack Query | v5 |
| Backend | Express.js | v4 |
| ORM | Drizzle ORM | v0.44 |
| Banco de dados | TiDB (MySQL-compatível) | — |
| Linguagem | TypeScript | v5.9 |
| Testes | Vitest | v2 |
| Gerenciador de pacotes | pnpm | v10 |

### 3.2 Fluxo de Dados

O frontend React consome dados exclusivamente por meio de hooks tRPC (`trpc.*.useQuery`), que se comunicam com o servidor Express via HTTP sob o prefixo `/api/trpc`. O servidor processa as requisições nos routers tRPC, delega as consultas ao banco de dados por meio das funções definidas em `server/db.ts` (que utilizam Drizzle ORM), e retorna os resultados tipados diretamente ao cliente. A serialização é feita com SuperJSON, garantindo que tipos como `Date` sejam preservados corretamente entre servidor e cliente.

### 3.3 Estrutura de Diretórios

```
bombeiros-legislacao-portal/
├── client/
│   ├── src/
│   │   ├── components/         # Componentes reutilizáveis (AppLayout, badges, etc.)
│   │   │   └── ui/             # Componentes shadcn/ui
│   │   ├── pages/              # Páginas da aplicação
│   │   │   ├── Home.tsx        # Dashboard inicial com indicadores
│   │   │   ├── Estados.tsx     # Listagem com filtros
│   │   │   ├── EstadoDetalhe.tsx # Detalhe expandido por estado
│   │   │   ├── Comparativo.tsx # Comparação lado a lado
│   │   │   └── Sobre.tsx       # Metodologia e fontes
│   │   ├── App.tsx             # Roteamento e layout global
│   │   └── index.css           # Tema institucional e tokens de cor
├── server/
│   ├── db.ts                   # Queries e helpers do banco de dados
│   ├── routers.ts              # Endpoints tRPC
│   ├── portal.test.ts          # Testes automatizados
│   └── _core/                  # Infraestrutura (OAuth, contexto, etc.)
├── drizzle/
│   └── schema.ts               # Definição das tabelas
├── scripts/
│   └── seed-positions-v2.mjs   # Script de carga de cargos e funções
└── DOCUMENTACAO.md             # Este arquivo
```

---

## 4. Banco de Dados

O banco de dados é composto por cinco tabelas relacionais. O diagrama de relacionamento segue abaixo.

```
users
  └── (autenticação OAuth — não relacionada ao domínio principal)

states (1)
  ├── operational_commands (N=1 por estado)
  │     └── positions (N por comando)
  └── technical_directorates (N=1 por estado)
        └── positions (N por diretoria)
```

### 4.1 Tabela `states` — Estados

Armazena os dados cadastrais de cada estado analisado.

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INT (PK) | Identificador único auto-incremental |
| `name` | VARCHAR(100) | Nome completo do estado |
| `sigla` | VARCHAR(2) | Sigla do estado (único) |
| `region` | ENUM | Região geográfica (Norte, Nordeste, Centro-Oeste, Sudeste, Sul) |
| `corporationName` | VARCHAR(200) | Nome oficial do Corpo de Bombeiros |
| `legislationDocuments` | TEXT | Documentos legislativos analisados |
| `createdAt` | TIMESTAMP | Data de criação do registro |
| `updatedAt` | TIMESTAMP | Data da última atualização |

### 4.2 Tabela `operational_commands` — Comandos Operacionais

Armazena as informações sobre o Comando Operacional (ou nomenclatura equivalente) de cada estado.

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INT (PK) | Identificador único |
| `stateId` | INT (FK → states) | Referência ao estado |
| `nomenclature` | VARCHAR(300) | Nomenclatura oficial do órgão |
| `acronym` | VARCHAR(50) | Sigla do órgão |
| `subdivisions` | TEXT | Desdobramentos internos (separados por `;`) |
| `attributions` | TEXT | Atribuições do órgão |
| `detailLevel` | ENUM | Nível de detalhamento: `detalhado`, `moderado`, `basico` |
| `legalBasis` | VARCHAR(300) | Base legal (lei, decreto, portaria) |
| `notes` | TEXT | Observações complementares |

### 4.3 Tabela `technical_directorates` — Diretorias de Atividades Técnicas

Estrutura idêntica à tabela `operational_commands`, aplicada ao órgão de atividades técnicas de cada estado.

### 4.4 Tabela `positions` — Cargos e Funções

Armazena os cargos e funções individuais de cada órgão, com suas respectivas subordinações e atribuições. Cada registro pertence a um Comando Operacional **ou** a uma Diretoria de Atividades Técnicas (um dos dois campos de chave estrangeira será `NULL`).

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INT (PK) | Identificador único |
| `operationalCommandId` | INT (FK, nullable) | Referência ao Comando Operacional |
| `technicalDirectorateId` | INT (FK, nullable) | Referência à Diretoria Técnica |
| `title` | VARCHAR(200) | Título do cargo ou função |
| `acronym` | VARCHAR(50) | Sigla do cargo |
| `rank` | VARCHAR(100) | Posto ou graduação exigido |
| `subordinateTo` | VARCHAR(200) | A quem o cargo é subordinado |
| `subordinates` | TEXT | Órgãos/seções subordinados (separados por `;`) |
| `attributions` | TEXT | Atribuições legais do cargo |
| `sortOrder` | INT | Ordem de exibição hierárquica |

### 4.5 Tabela `users` — Usuários

Tabela de autenticação gerenciada pelo sistema OAuth da plataforma Manus. Não armazena dados do domínio legislativo.

---

## 5. Backend — API tRPC

Todos os endpoints da API são procedimentos tRPC públicos (não requerem autenticação), definidos em `server/routers.ts`. A comunicação ocorre sob o prefixo `/api/trpc`.

### 5.1 Endpoints Disponíveis

#### `states.list`
Retorna a lista completa de todos os estados cadastrados, ordenados alfabeticamente por nome. Não aceita parâmetros de entrada.

**Resposta:** Array de objetos `State` com todos os campos da tabela `states`.

#### `states.details`
Retorna o detalhamento completo de um estado específico, incluindo o Comando Operacional, a Diretoria de Atividades Técnicas e todos os cargos e funções de cada órgão.

**Entrada:** `{ sigla: string }` — sigla do estado com exatamente 2 caracteres.

**Resposta:** Objeto com `state`, `operationalCommand`, `technicalDirectorate`, `ocPositions` (array de cargos do Comando Operacional) e `tdPositions` (array de cargos da Diretoria Técnica).

#### `dashboard.stats`
Retorna os indicadores estatísticos exibidos na página inicial do portal.

**Resposta:** Objeto com `totalStates`, `operationalCommands` (contagem por nível de detalhamento), `technicalDirectorates` (contagem por nível) e `byRegion` (distribuição por região geográfica).

#### `data.filtered`
Endpoint principal de consulta com suporte a múltiplos filtros combinados.

**Entrada:**
```typescript
{
  siglas?: string[]        // Filtro por siglas de estados
  detailLevel?: ("detalhado" | "moderado" | "basico")[]
  orgType?: "all" | "operational" | "technical"
  search?: string          // Busca textual em nomenclatura, atribuições e desdobramentos
}
```

**Resposta:** Array de objetos com `state`, `operationalCommand` e `technicalDirectorate`. Quando `orgType` é `"operational"`, o campo `technicalDirectorate` é retornado como `null`, e vice-versa.

#### `data.comparative`
Endpoint especializado para a página de comparativo, que retorna os dados completos de múltiplos estados incluindo todos os cargos e funções.

**Entrada:** `{ siglas: string[] }` — entre 1 e 5 siglas de estados.

**Resposta:** Array de objetos com `state`, `operationalCommand`, `technicalDirectorate`, `ocPositions` e `tdPositions`. As posições são carregadas em duas queries paralelas (`Promise.all`) para otimização de desempenho.

### 5.2 Helpers de Banco de Dados (`server/db.ts`)

As funções de acesso ao banco são organizadas por domínio:

| Função | Descrição |
|---|---|
| `getAllStates()` | Retorna todos os estados ordenados por nome |
| `getStateBySigna(sigla)` | Busca um estado pela sigla |
| `getFilteredData(params)` | Query principal com filtros combinados |
| `getStateDetails(sigla)` | Detalhe completo com posições |
| `getDashboardStats()` | Indicadores do dashboard |
| `getPositionsByOperationalCommand(id)` | Cargos de um Comando Operacional |
| `getPositionsByTechnicalDirectorate(id)` | Cargos de uma Diretoria Técnica |
| `getPositionsByOperationalCommandIds(ids[])` | Cargos de múltiplos Comandos (para comparativo) |
| `getPositionsByTechnicalDirectorateIds(ids[])` | Cargos de múltiplas Diretorias (para comparativo) |

---

## 6. Frontend — Interface do Usuário

### 6.1 Roteamento

A aplicação utiliza o roteador Wouter, com as seguintes rotas registradas em `client/src/App.tsx`:

| Rota | Componente | Descrição |
|---|---|---|
| `/` | `Home` | Dashboard inicial com indicadores e acesso rápido |
| `/estados` | `Estados` | Listagem com filtros e busca |
| `/estado/:sigla` | `EstadoDetalhe` | Detalhe expandido por estado |
| `/comparativo` | `Comparativo` | Comparação lado a lado entre estados |
| `/sobre` | `Sobre` | Metodologia, fontes e critérios |

### 6.2 Layout e Navegação

Todas as páginas são envolvidas pelo componente `AppLayout`, que implementa a navegação lateral (sidebar) com suporte a recolhimento e menu mobile. A sidebar exibe os quatro itens de navegação principais com ícones e destaque visual na rota ativa. O cabeçalho superior exibe o título institucional e um badge fixo com o total de estados analisados.

O tema visual segue a identidade institucional dos Corpos de Bombeiros Militares, com as seguintes cores principais definidas como tokens CSS em `client/src/index.css`:

| Token | Cor | Uso |
|---|---|---|
| `--fire-red` | `#CC2222` | Destaque, badges "detalhado", botões primários |
| `--navy-blue` | `#1A2744` | Sidebar, cabeçalho, fundo escuro |
| `--gold` | `#C8A84B` | Badges "moderado", acentos dourados |
| `--slate-blue` | `#3B5998` | Links, badges "básico" |

A tipografia utiliza `Inter` para texto corrido e `Oswald` para títulos institucionais, ambas carregadas via Google Fonts.

### 6.3 Página Inicial (`Home`)

Apresenta quatro cards de métricas (total de estados, comandos operacionais detalhados, diretorias técnicas detalhadas e regiões representadas), dois painéis de distribuição por nível de detalhamento com barras percentuais visuais, e uma grade de acesso rápido a todos os estados cadastrados com links diretos para a página de detalhe.

### 6.4 Página de Estados (`Estados`)

É a interface principal de consulta. O painel de filtros lateral permite combinar:

- **Busca textual:** pesquisa simultânea em nomenclatura, desdobramentos e atribuições de ambos os órgãos.
- **Seleção de estados:** checkboxes individuais para cada um dos 19 estados.
- **Filtro por região:** Norte, Nordeste, Centro-Oeste, Sudeste e Sul.
- **Tipo de órgão:** Todos, apenas Comando Operacional ou apenas Diretoria de Atividades Técnicas.
- **Nível de detalhamento:** Detalhado, Moderado e/ou Básico.

Os resultados são exibidos em cards por estado, cada um mostrando os dois órgãos com nomenclatura, sigla, desdobramentos resumidos, atribuições e badge de nível de detalhamento. Um link "Ver detalhes" direciona para a página de detalhe do estado.

### 6.5 Página de Detalhes por Estado (`EstadoDetalhe`)

Exibe o perfil completo de um estado, organizado em duas colunas: Comando Operacional (à esquerda) e Diretoria de Atividades Técnicas (à direita). Para cada órgão, são apresentados:

- Nomenclatura oficial e sigla
- Desdobramentos internos (seções, departamentos, coordenadorias)
- Atribuições legais completas
- **Cargos e Funções:** cards expansíveis individuais para cada cargo, exibindo título, sigla, posto/graduação, subordinação hierárquica, subordinados/desdobramentos e atribuições completas
- Base legal (lei, decreto ou portaria de origem)
- Notas e observações complementares

### 6.6 Página de Comparativo (`Comparativo`)

Permite selecionar entre 1 e 5 estados para visualização simultânea em colunas paralelas. Para cada estado selecionado, são exibidas duas seções: Comando Operacional e Diretoria de Atividades Técnicas, cada uma com nomenclatura, sigla, desdobramentos, atribuições e a lista completa de cargos e funções com expansão individual. A seleção de estados é feita por botões de adição incremental, com remoção individual por ícone de fechamento em cada coluna.

### 6.7 Página Sobre o Portal (`Sobre`)

Apresenta o objetivo do portal, a metodologia de análise legislativa, os critérios de classificação por nível de detalhamento e a lista completa dos 19 estados com os respectivos documentos analisados.

---

## 7. Guia de Uso do Portal

### 7.1 Consultar um Estado Específico

Para acessar as informações completas de um estado, o usuário pode navegar até a página **Estados** e clicar em "Ver detalhes" no card do estado desejado, ou utilizar os atalhos de acesso rápido disponíveis na página inicial. A URL segue o padrão `/estado/RO` (substituindo `RO` pela sigla do estado desejado).

### 7.2 Comparar Dois ou Mais Estados

Na página **Comparativo**, clique no botão "Adicionar estado" e selecione os estados desejados na lista suspensa. É possível adicionar até cinco estados simultaneamente. Para remover um estado da comparação, clique no ícone de fechamento no topo da coluna correspondente. Os dados são carregados automaticamente após cada seleção.

### 7.3 Realizar Busca Textual

Na página **Estados**, utilize o campo de busca no topo do painel de filtros. A busca é aplicada simultaneamente sobre as nomenclaturas dos órgãos, seus desdobramentos e suas atribuições. Por exemplo, buscar "análise de projetos" retornará todos os estados cujos órgãos mencionem essa expressão em qualquer um desses campos.

### 7.4 Filtrar por Nível de Detalhamento

O filtro de nível de detalhamento permite selecionar múltiplas opções simultaneamente. Os três níveis disponíveis são:

- **Detalhado:** a legislação define explicitamente a estrutura do órgão, seus desdobramentos, os cargos e funções com subordinações e atribuições específicas.
- **Moderado:** a legislação menciona o órgão com algumas atribuições e desdobramentos, mas sem detalhamento completo de cargos e funções.
- **Básico:** a legislação apenas menciona o órgão ou lista suas atribuições gerais, sem estruturação interna.

---

## 8. Dados Cadastrados

O portal contém dados de **19 estados brasileiros**, distribuídos pelas cinco regiões do país.

### 8.1 Estados por Região

| Região | Estados |
|---|---|
| **Norte** | Pará (PA), Rondônia (RO), Tocantins (TO) |
| **Nordeste** | Alagoas (AL), Ceará (CE), Maranhão (MA), Paraíba (PB), Pernambuco (PE), Piauí (PI), Sergipe (SE) |
| **Centro-Oeste** | Distrito Federal (DF), Mato Grosso (MT), Mato Grosso do Sul (MS) |
| **Sudeste** | Espírito Santo (ES), Minas Gerais (MG), Rio de Janeiro (RJ) |
| **Sul** | Paraná (PR), Rio Grande do Sul (RS), Santa Catarina (SC) |

### 8.2 Nomenclaturas dos Órgãos por Estado

A tabela a seguir consolida as nomenclaturas utilizadas por cada estado para os dois órgãos analisados.

| Estado | Comando Operacional | Diretoria de Atividades Técnicas |
|---|---|---|
| AL | Comando Operacional de Bombeiros (COB) | Diretoria de Serviços Técnicos (DST) |
| CE | Coordenadoria Operacional (COROP) | Coordenadoria de Atividades Técnicas (CAT) |
| DF | Comando Operacional (COMOP) | Departamento de Segurança Contra Incêndio e Pânico (DESEG) |
| ES | Diretoria de Operações (DOp) | Centro de Atividades Técnicas (CAT) |
| MA | Comando Operacional do Corpo de Bombeiros (COCB) | Diretoria de Atividades Técnicas (DAT) |
| MT | Diretoria Operacional (DOP) | Diretoria de Segurança Contra Incêndio e Pânico (DSCI) |
| MS | Grande Comando Metropolitano (CMB) | Diretoria de Atividades Técnicas (DAT) |
| MG | Comando Operacional de Bombeiros (COp) | Centro de Atividades Técnicas (CAT) |
| PA | Comando de Operações | Departamento-Geral de Segurança contra Incêndios e Emergências (DGSCI) |
| PB | Comando Regional de Bombeiro Militar (CRBM) | Diretoria de Atividades Técnicas (DAT) |
| PE | Comando Operacional | Diretoria de Atividades Técnicas (DAT) |
| PI | Comando Operacional de Bombeiros (COB) | Diretoria de Segurança Contra Incêndio (DSCI) |
| PR | Comando Regional Bombeiro Militar (CRBM) | Diretoria de Atividades Técnicas (DAT) |
| RJ | Comando Operacional | Diretoria de Serviços Técnicos (DST) |
| RO | Diretoria de Planejamento Operacional (DPO) | Comando de Operações Técnicas (COT) |
| RS | Comando Operacional | Diretoria de Atividades Técnicas (DAT) |
| SC | Comando Operacional | Diretoria de Segurança Contra Incêndio e Pânico (DSCI) |
| SE | Diretoria Operacional (DOP) | Diretoria de Atividades Técnicas (DAT) |
| TO | Comando Operacional Bombeiro Militar (COBM) | Comando de Atividades Técnicas (CAT) |

### 8.3 Cargos e Funções Cadastrados

O banco de dados contém **70 registros de cargos e funções**, distribuídos entre os estados com legislação detalhada. Cada registro inclui título, sigla, posto/graduação exigido, subordinação hierárquica, subordinados/desdobramentos e atribuições legais completas, extraídas diretamente do texto das legislações.

---

## 9. Critérios de Classificação

### 9.1 Nível Detalhado

A legislação define explicitamente:
- A estrutura interna do órgão com seus desdobramentos (seções, departamentos, coordenadorias);
- Os cargos e funções com denominação específica;
- A cadeia de subordinação hierárquica;
- As atribuições individuais de cada cargo ou função.

**Estados com Comando Operacional detalhado:** AL, CE, DF, ES, MA, MG, PA, PB, PI, RO, SE, TO.

**Estados com Diretoria de Atividades Técnicas detalhada:** AL, CE, DF, ES, MA, MT, MS, MG, PA, PB, PI, PR, RO, SE, TO.

### 9.2 Nível Moderado

A legislação menciona o órgão, lista suas principais atribuições e indica alguns desdobramentos, mas não detalha os cargos e funções individualmente ou não apresenta a cadeia de subordinação completa.

### 9.3 Nível Básico

A legislação apenas menciona a existência do órgão ou lista atribuições gerais sem estruturação interna. Inclui casos em que o documento analisado é um Quadro de Organização e Distribuição de Efetivo (QOD) sem texto normativo.

---

## 10. Manutenção e Atualização de Dados

### 10.1 Atualizar Informações de um Estado

Para corrigir ou atualizar os dados de um estado existente, utilize o painel de banco de dados da plataforma (aba **Database** no painel de gerenciamento) ou execute SQL diretamente. O exemplo abaixo atualiza as atribuições do Comando Operacional de Rondônia:

```sql
UPDATE operational_commands
SET attributions = 'Nova atribuição conforme lei atualizada',
    legalBasis = 'Lei Complementar nº XX/XXXX'
WHERE stateId = (SELECT id FROM states WHERE sigla = 'RO');
```

### 10.2 Adicionar Novos Cargos e Funções

Para inserir um novo cargo vinculado a um Comando Operacional ou Diretoria Técnica, identifique primeiro o ID do órgão correspondente e utilize o script `scripts/seed-positions-v2.mjs` como referência para o formato dos dados. O campo `sortOrder` define a posição hierárquica na exibição (valores menores aparecem primeiro).

### 10.3 Adicionar um Novo Estado

Para incluir um estado ainda não cadastrado, siga a sequência:

1. Inserir o estado na tabela `states` com todos os campos obrigatórios.
2. Inserir o Comando Operacional na tabela `operational_commands` com o `stateId` correto.
3. Inserir a Diretoria de Atividades Técnicas na tabela `technical_directorates`.
4. Inserir os cargos e funções na tabela `positions`, vinculando ao `operationalCommandId` ou `technicalDirectorateId` correspondente.

### 10.4 Migração de Schema

Caso seja necessário alterar a estrutura das tabelas (adicionar colunas, modificar tipos), o processo correto é:

1. Editar o arquivo `drizzle/schema.ts` com as alterações desejadas.
2. Executar `pnpm drizzle-kit generate` para gerar o SQL de migração.
3. Aplicar o SQL gerado via painel de banco de dados ou ferramenta de administração.

---

## 11. Testes Automatizados

O projeto mantém uma suíte de testes automatizados em `server/portal.test.ts`, executada com Vitest. Os testes cobrem todos os endpoints tRPC públicos do portal utilizando mocks do banco de dados, garantindo que a lógica de negócio funcione corretamente de forma isolada.

Para executar os testes:

```bash
pnpm test
```

### 11.1 Cobertura dos Testes

| Endpoint | Casos Testados |
|---|---|
| `states.list` | Retorno de lista de estados |
| `states.details` | Detalhe com posições; estado inexistente retorna null |
| `dashboard.stats` | Contagem por nível e por região |
| `data.filtered` | Sem filtros; filtro por sigla; filtro por nível; filtro por tipo de órgão; busca textual |
| `data.comparative` | Comparativo com cargos; validação de limite máximo de 5 estados |
| `auth.logout` | Limpeza de cookie de sessão |

A suíte conta com **17 testes**, todos passando na versão atual.

---

## 12. Fontes Documentais

Os dados cadastrados no portal foram extraídos diretamente dos seguintes documentos legislativos, obtidos junto às corporações estaduais ou em bases públicas de legislação:

| Estado | Documento(s) Analisado(s) |
|---|---|
| AL | Regimento Interno do CBMAL; Quadro Demonstrativo de Cargos e Funções |
| CE | Lei de Organização Básica do CBMCE |
| DF | Regimento Interno do CBMDF |
| ES | Normas Gerais de Ação — CBMES (2023) |
| MA | Lei de Organização Básica do CBMMA; Quadro de Organização e Distribuição |
| MT | Lei de Organização Básica do CBMMT |
| MS | Lei Complementar nº 188/2014 — Organização Básica do CBMMS |
| MG | Lei Complementar nº 54/1999 — Organização Básica do CBMMG |
| PA | Lei de Organização Básica do CBMPA (2025); Regimento Interno |
| PB | Lei de Organização Básica do CBMPB |
| PE | Lei de Organização Básica do CBMPE |
| PI | Lei de Organização Básica do CBMPI |
| PR | Lei Ordinária nº 22.206/2024 — Organização Básica do CBMPR |
| RJ | Lei de Organização Básica do CBMRJ |
| RO | Minuta de Projeto de Lei de Organização Básica do CBMRO |
| RS | Lei de Organização Básica do CBMRS; Regimento Interno |
| SC | Lei de Organização Básica do CBMSC |
| SE | Lei de Organização Básica do CBMSE; Regimento Interno |
| TO | Lei de Organização Básica do CBMTO |

> **Nota de uso:** As informações disponibilizadas neste portal têm caráter informativo e comparativo. Para fins legais, regulatórios ou administrativos, recomenda-se sempre consultar o texto integral e atualizado da legislação vigente de cada estado.

---

*Documentação elaborada pela Assessoria Técnica Institucional do Corpo de Bombeiros Militar de Rondônia — CBMRO, com suporte da plataforma Manus AI. Versão 1.0 — Maio de 2026.*
