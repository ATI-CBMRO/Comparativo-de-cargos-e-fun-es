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

## Expansão: Cargos e Funções
- [x] Schema: tabela `positions` com cargos/funções vinculados a operational_commands e technical_directorates
- [x] Migration SQL aplicada via webdev_execute_sql
- [x] Seed: popular banco com cargos e funções de todos os estados levantados (112 cargos/funções inseridos)
- [x] Backend: incluir cargos/funções nas queries de detalhes e comparativo
- [x] Frontend: exibir cargos/funções na página de detalhes por estado
- [x] Frontend: exibir cargos/funções na página de comparativo
- [x] Testes atualizados para cargos/funções (17 testes passando)
- [x] Checkpoint final com cargos/funções

## Filtro Comparativo por Cargo

- [x] Backend: endpoint `data.positionTypes` para listar tipos de cargos disponíveis
- [x] Backend: endpoint `data.comparePositions` para comparar um tipo de cargo entre todos os estados
- [x] Frontend: nova página `ComparativoCargos` com filtro por tipo de cargo e visualização comparativa
- [x] Frontend: integrar link na sidebar e em `App.tsx`
- [x] Testes para os novos endpoints (23 testes passando)
- [x] Checkpoint final

## Revisão de Dados - Estados com Detalhamento Básico

- [x] Reler documentos de AL (Regimento Interno) — dados já corretos no banco (detalhado)
- [x] Reler documentos de CE (Organização Básica) — dados já corretos no banco (moderado)
- [x] Reler documentos de MA (Organização Básica + Quadro de Organização) — dados já corretos no banco (detalhado)
- [x] Reler documentos de SE (Organização Básica + Regimento Interno) — dados já corretos no banco (moderado)
- [x] Verificar nível de detalhamento dos estados revisados no banco — nenhum estado com nível "básico" incorreto

## Exportação PDF

- [x] Instalar biblioteca de geração PDF (jsPDF + html2canvas)
- [x] Implementar hook usePDFExport reutilizável
- [x] Botão "Exportar PDF" na página ComparativoCargos (exporta os cards visíveis)
- [x] Botão "Exportar PDF" na página Comparativo (exporta a comparação lado a lado)
- [x] PDF formatado com cabeçalho institucional (título, subtítulo, data)
- [ ] Testes para verificar que os botões existem e são clicáveis
