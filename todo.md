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
- [x] Testes para verificar que os botões existem e são clicáveis (validado via TypeScript sem erros + 23 testes passando)

## Correção da Exportação PDF

- [x] Corrigir erro de exportação PDF (html2canvas não suporta oklch) — migrado para geração no servidor com pdfkit
- [x] Rota GET /api/pdf/positions?category=&siglas= implementada com layout em 2 colunas e cabeçalho institucional
- [x] Hook usePDFExport atualizado para usar fetch + download via Blob URL
- [x] Testado com sucesso no browser — toast "PDF gerado com sucesso!" exibido corretamente

## Documentação do Projeto

- [x] Documentação técnica e funcional completa em PROJETO.md (v1.3.0)

## Layout Dinâmico e PDF Comparativo

- [x] Rota GET /api/pdf/comparative?siglas= implementada com layout em N colunas (1-5 estados)
- [x] Corrigir overflow de páginas no PDF comparativo (pdfkit auto-paginava ao ultrapassar PAGE_H) — resolvido com safeText() que limita Y ao BOTTOM_LIMIT
- [x] Layout dinâmico da página Comparativo — substituir flex-wrap por CSS Grid com número de colunas dinâmico baseado nos estados selecionados
- [x] PDF comparativo com 5 estados gera 1 página A4 landscape com todas as informações

## Redesign - Identidade Visual CBMRO

- [x] Atualizar paleta de cores no index.css (vermelho #E4001A, azul #1a3a8f, fundo #f2f2f7)
- [x] Adicionar fonte Josefin Sans ao index.html
- [x] Criar cabeçalho institucional da Assessoria Institucional do CBMRO (gradiente vermelho, divisor azul)
- [x] Atualizar sidebar/navegação com as novas cores (azul escuro CBMRO + fonte Josefin Sans)
- [x] Atualizar sub-header com gradiente vermelho→azul e fonte Josefin Sans
- [x] Atualizar componentes (cards, botões, badges) com a nova identidade visual — aplicado via tokens CSS globais (primary, secondary, sidebar)

## Revisão de Desdobramentos e Melhorias de UX

- [x] Revisar e corrigir desdobramentos de RO conforme legislação (minuta de lei – DPO/COT)
- [x] Revisar e corrigir desdobramentos de PE conforme legislação (DIM/DIEsp)
- [x] Revisar e corrigir desdobramentos de MT conforme legislação (DOP/DSCIP)
- [x] Adicionar agrupamento por região (Norte, Nordeste, Centro-Oeste, Sudeste, Sul) na tela de Comparativo
- [x] Adicionar campo `legalArticle` (artigo de origem) nos registros de desdobramentos no banco
- [x] Exibir tooltip/modal com artigo legal de origem em cada item de desdobramento

## Base Legal Completa e Ajustes de Layout

- [x] Extrair número e data completos das leis/decretos dos 19 estados nos arquivos de legislação
- [x] Atualizar campo `legalBasis` (CO e DAT) com número, data e ementa de cada instrumento normativo
- [x] Remover brasão duplicado do lado direito do cabeçalho institucional
- [x] Corrigir renderização dos desdobramentos — parse de JSON array em todos os componentes de lista
- [x] Corrigir layout mobile: sub-header com texto completo visível e sidebar não sobrepõe conteúdo
- [x] Seletor de estados no Comparativo agrupado por região geográfica (Norte/Nordeste/Centro-Oeste/Sudeste/Sul)
- [x] Seção "Artigo Legal de Origem" exibida nos cards de CO e DAT nas telas de Comparativo e EstadoDetalhe

## Correção de Dados - Alagoas e Varredura de PDFs

- [x] Corrigir desdobramentos da DST de AL conforme Art. 60–64 do Regimento Interno (5 seções: Estudos e Projetos, Testes/Vistorias/Pareceres, Perícias e Pesquisas, Hidrantes, Expediente e Arquivo)
- [x] Varredura dos 31 arquivos PDF de legislação: todos com texto digital extraível, exceto Amazonas (imagem escaneada)
- [x] Documentação atualizada para v1.5.0 com nota sobre formato dos PDFs
- [x] Publicação no GitHub
