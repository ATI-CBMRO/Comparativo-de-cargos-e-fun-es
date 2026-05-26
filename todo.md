# Portal de Legislação dos Corpos de Bombeiros Militares - TODO

## Banco de Dados e Backend
- [x] Schema: tabela `states` com dados dos estados
- [x] Schema: tabela `operational_commands` com dados do Comando Operacional
- [x] Schema: tabela `technical_directorates` com dados da Diretoria de Atividades Técnicas
- [x] Gerar migration SQL e aplicar via webdev_execute_sql
- [x] Seed: popular banco com todos os estados levantados
- [x] tRPC router: listar todos os estados
- [x] tRPC router: buscar por estado(s) com filtros
- [x] tRPC router: filtro por tipo de órgão
- [x] tRPC router: filtro por nível de detalhamento
- [x] tRPC router: busca textual por nomenclatura ou atribuição
- [x] tRPC router: detalhes completos por estado

## Frontend - Layout e Navegação
- [x] Tema institucional: azul e vermelho (bombeiros)
- [x] DashboardLayout com sidebar de navegação
- [x] Página Home/Dashboard com indicadores gerais
- [x] Rota /estados - listagem com filtros
- [x] Rota /comparativo - comparação lado a lado
- [x] Rota /estado/:sigla - detalhes completos do estado

## Frontend - Funcionalidades
- [x] Filtro por estado (seleção múltipla/individual)
- [x] Filtro por tipo de órgão (CO, DAT, ambos)
- [x] Filtro por nível de detalhamento (detalhado, moderado, básico)
- [x] Campo de busca textual
- [x] Tabela comparativa lado a lado
- [x] Cards com badges/tags de nível de detalhamento
- [x] Página de detalhes expandida por estado
- [x] Indicadores visuais (badges) de nível de detalhamento

## Testes e Qualidade
- [x] Vitest: testes dos routers principais (11 testes passando)
- [x] Checkpoint final
