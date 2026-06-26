# detail_cargos_g2.py — Cargos detalhados: BA, CE, DF, ES
# Chaveado por id de órgão existente em detail_data_g2.

CARGOS = {

# ── BAHIA (Lei nº 14.572/2023) ──
"ba": {
  "comando-geral-cbmba": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Oficial da ativa do último posto do QOBM", "desdobramentos": ["Gabinete do Comando-Geral", "Subcomando-Geral", "Comandos, Departamentos e Coordenadorias"], "atribuicoes": ["Promover a administração geral do CBMBA", "Exercer a representação política e institucional", "Autorizar a abertura de processos licitatórios e homologá-los", "Aprovar a programação e a proposta orçamentária anual", "Aplicar penas disciplinares; instaurar e decidir sindicâncias e processos administrativos disciplinares", "Expedir Instruções Técnicas e Portarias de segurança contra incêndio e pânico"]},
  ],
  "subcomando-geral": [
    {"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel da ativa do QOBM", "desdobramentos": ["Gabinete do Subcomando-Geral", "Centro de Gestão Estratégica"], "atribuicoes": ["Auxiliar o Comandante-Geral; dirigir, organizar, orientar, coordenar e controlar as atividades de bombeiro militar", "Substituir o Comandante-Geral em afastamentos, ausências e impedimentos", "Instaurar e decidir sindicâncias e processos disciplinares"]},
  ],
  "comando-operacoes": [
    {"cargo": "Comandante de Operações de Bombeiros Militar", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM", "desdobramentos": ["Centro de Gestão do Vetor Aéreo", "Comandos Regionais"], "atribuicoes": ["Planejar, organizar, supervisionar, coordenar e controlar as atividades operacionais", "Planejar, coordenar, executar, avaliar e controlar atividades de proteção e defesa civil"]},
  ],
  "comando-seguranca-incendio": [
    {"cargo": "Comandante de Segurança Contra Incêndio", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM (cargo privativo do posto)", "desdobramentos": [], "atribuicoes": ["Planejar, executar, controlar e fiscalizar as atividades de proteção contra incêndio", "Planejar, executar e controlar as ações de perícia de incêndio", "Promover ações de prevenção contra incêndio"]},
  ],
  "corregedoria": [
    {"cargo": "Corregedor-Chefe", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM (cargo privativo do posto)", "desdobramentos": [], "atribuicoes": ["Propor ao Comandante-Geral medidas de apuração de denúncias", "Encaminhar relatórios mensais de dados estatísticos das apurações", "Elaborar normas de orientação e padronização dos feitos investigatórios", "Assessorar o Comandante-Geral quanto à justiça e disciplina", "Instaurar e decidir sindicâncias e processos administrativos disciplinares"]},
  ],
  "coordenadoria-inteligencia": [
    {"cargo": "Coordenador de Inteligência", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Promover as atividades de inteligência no âmbito do CBMBA (SINBOM)", "Assessorar o Alto Comando em assuntos estratégicos, táticos e operacionais"]},
  ],
  "departamento-planejamento": [
    {"cargo": "Diretor do Departamento de Planejamento", "subordinadoA": "Comandante-Geral (via Subcomando-Geral)", "requisito": "Coronel QOBM", "desdobramentos": ["Subdivisões do Departamento"], "atribuicoes": ["Planejar, controlar e fiscalizar as atividades do Departamento", "Propor estudos e pesquisas para melhoria das competências", "Instaurar e decidir sindicâncias e processos administrativos disciplinares"]},
  ],
  "departamento-pessoal": [
    {"cargo": "Diretor do Departamento de Pessoal", "subordinadoA": "Comandante-Geral (via Subcomando-Geral)", "requisito": "Coronel QOBM", "desdobramentos": [], "atribuicoes": ["Planejar, organizar, coordenar e controlar as atividades de pessoal do CBMBA"]},
  ],
  "departamento-apoio-logistico": [
    {"cargo": "Diretor do Departamento de Apoio Logístico", "subordinadoA": "Comandante-Geral (via Subcomando-Geral)", "requisito": "Coronel QOBM", "desdobramentos": ["Centro de Engenharia e Arquitetura"], "atribuicoes": ["Planejar, coordenar, controlar e executar as atividades de logística e patrimônio"]},
  ],
  "departamento-modernizacao-tecnologia": [
    {"cargo": "Diretor do Departamento de Modernização e Tecnologia", "subordinadoA": "Comandante-Geral (via Subcomando-Geral)", "requisito": "Coronel QOBM", "desdobramentos": [], "atribuicoes": ["Planejar, coordenar, executar e controlar as atividades de TI e telecomunicações", "Promover a elevação da qualidade dos serviços e das atividades"]},
  ],
  "departamento-auditoria-financas": [
    {"cargo": "Diretor do Departamento de Auditoria e Finanças", "subordinadoA": "Comandante-Geral (via Subcomando-Geral)", "requisito": "Coronel QOBM", "desdobramentos": [], "atribuicoes": ["Análise e controle da gestão financeira dos órgãos do CBMBA", "Acompanhamento da execução orçamentária, financeira e contábil", "Realizar a atividade de auditoria"]},
  ],
  "imesb": [
    {"cargo": "Diretor do Instituto Militar de Ensino Superior de Bombeiros", "subordinadoA": "Comandante-Geral", "requisito": "Coronel QOBM (cargo privativo do posto)", "desdobramentos": ["Academia de Bombeiro Militar", "Coordenadoria de Formação e Aperfeiçoamento de Praças", "Coordenadoria de Treinamento Operacional"], "atribuicoes": ["Planejar, controlar e fiscalizar as atividades de ensino e pesquisa", "Elaborar diretrizes da política institucional de educação"]},
  ],
  "academia-bombeiros-militar": [
    {"cargo": "Diretor da Academia de Bombeiros Militar", "subordinadoA": "Instituto Militar de Ensino Superior de Bombeiros", "requisito": "Coronel QOBM", "desdobramentos": [], "atribuicoes": ["Planejar, controlar e fiscalizar as atividades da Academia", "Promover a formação e o aperfeiçoamento de Oficiais Bombeiros Militares"]},
  ],
  "coordenadoria-saude": [
    {"cargo": "Coordenador de Saúde", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Coordenar as ações de saúde implementadas na Corporação"]},
  ],
  "comandos-regionais": [
    {"cargo": "Comandante Regional de Bombeiros Militar", "subordinadoA": "Comando de Operações de Bombeiros Militar", "requisito": "Coronel QOBM (cargo privativo do posto)", "desdobramentos": ["Batalhões de Bombeiros Militar subordinados"], "atribuicoes": ["Cumprir as atividades de prevenção e combate a incêndios, busca, salvamento e defesa civil", "Coordenar, controlar e supervisionar as Unidades Operacionais"]},
  ],
  "batalhoes": [
    {"cargo": "Comandante de Batalhão", "subordinadoA": "Comandante Regional", "requisito": "", "desdobramentos": ["Companhias do Batalhão"], "atribuicoes": ["Comandar e executar missões de prevenção e combate a incêndio, busca, salvamento e defesa civil", "Observar as normas e diretrizes do Comando de Operações"]},
    {"cargo": "Comandante de Companhia", "subordinadoA": "Comandante de Batalhão", "requisito": "", "desdobramentos": [], "atribuicoes": ["Coordenar, supervisionar, controlar e executar as atividades de bombeiro militar"]},
  ],
},

# ── CEARÁ (Lei nº 13.438/2004) ──
"ce": {
  "comando-geral-ce": [
    {"cargo": "Comandante Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel do Quadro de Oficiais Combatentes (CFO, CAO e CSBM ou equivalente)", "desdobramentos": ["Conselho Consultivo", "Comandante Adjunto", "Secretaria Executiva", "Coordenadorias"], "atribuicoes": ["Responsável pelo comando e administração da Corporação", "Estabelecer Normas Técnicas de Segurança Contra Incêndio, Pânico e Produtos Perigosos", "Determinar afastamento de bombeiro militar incompatível com o cargo"]},
  ],
  "comandante-adjunto-ce": [
    {"cargo": "Comandante Adjunto", "subordinadoA": "Comandante Geral", "requisito": "Coronel do Quadro de Oficiais Combatentes (CFO, CAO e CSBM ou equivalente)", "desdobramentos": [], "atribuicoes": ["Substituir o Comandante Geral em seus impedimentos"]},
  ],
  "secretaria-executiva-ce": [
    {"cargo": "Secretário Executivo", "subordinadoA": "Comandante Geral", "requisito": "Oficial Superior do Quadro de Oficiais Combatentes", "desdobramentos": [], "atribuicoes": ["Assessorar o Comandante Geral nas áreas operacionais e administrativas", "Coordenar e supervisionar as atividades do Gabinete", "Produzir informações estratégicas; coordenar a imprensa", "Exercer as atribuições de ouvidoria"]},
  ],
  "assessoria-juridica-ce": [
    {"cargo": "Chefe da Assessoria Jurídica", "subordinadoA": "Comandante Geral", "requisito": "Advogado civil de provimento em comissão", "desdobramentos": [], "atribuicoes": ["Coordenar os aspectos jurídicos da Corporação", "Manter atualizada a legislação de interesse do CBMCE", "Coordenar e elaborar contratos, convênios e acordos"]},
  ],
  "coordenadoria-atividades-tecnicas-ce": [
    {"cargo": "Coordenador de Atividades Técnicas", "subordinadoA": "Comandante Geral", "requisito": "Oficial Superior do Quadro de Oficiais Combatentes", "desdobramentos": [], "atribuicoes": ["Controle dos requisitos técnicos contra incêndios e projetos de edificações", "Pesquisa científica e avaliação do desempenho operacional", "Analisar projetos, vistorias e pareceres técnicos; controlar hidrantes"]},
  ],
  "coordenadoria-operacional-ce": [
    {"cargo": "Coordenador Operacional", "subordinadoA": "Comandante Geral", "requisito": "Oficial Superior do Quadro de Oficiais Combatentes", "desdobramentos": ["Núcleo de Bombeiro Metropolitano", "Núcleo de Bombeiro do Interior", "Núcleo de Defesa Civil", "Núcleo de Busca e Salvamento", "Núcleo de Resgate e Emergência Pré-hospitalar"], "atribuicoes": ["Responsável pela execução das operações bombeirísticas"]},
  ],
  "coordenadoria-geral-ce": [
    {"cargo": "Coordenador Geral", "subordinadoA": "Comandante Geral", "requisito": "Coronel do Quadro de Oficiais Combatentes", "desdobramentos": ["Célula de Logística", "Núcleo Financeiro", "Célula de Gestão e Formação de Pessoas"], "atribuicoes": ["Fiscalização administrativa, financeira e controle interno da Corporação", "Substituto eventual do Comandante Adjunto"]},
    {"cargo": "Chefe da Célula de Logística", "subordinadoA": "Coordenador Geral", "requisito": "Oficial Superior do Quadro de Oficiais Combatentes", "desdobramentos": [], "atribuicoes": ["Gerir conservação, reforma, ampliação e construção do patrimônio", "Distribuir material às unidades; supervisionar a manutenção da frota"]},
    {"cargo": "Chefe do Núcleo Financeiro", "subordinadoA": "Coordenador Geral", "requisito": "Oficial Superior do Quadro de Oficiais Combatentes", "desdobramentos": [], "atribuicoes": ["Gerenciar as contas e o acompanhamento orçamentário", "Controlar a captação de recursos da Corporação"]},
    {"cargo": "Chefe da Célula de Gestão e Formação de Pessoas", "subordinadoA": "Coordenador Geral", "requisito": "Oficial Superior do Quadro de Oficiais Combatentes", "desdobramentos": ["Academia de Bombeiro Militar", "Colégio Militar"], "atribuicoes": ["Coordenar recrutamento, seleção, acompanhamento e controle de pessoal", "Acompanhar promoções, classificação e movimentação"]},
  ],
  "academia-bombeiro-militar-ce": [
    {"cargo": "Diretor da Academia de Bombeiro Militar", "subordinadoA": "Célula de Gestão e Formação de Pessoas", "requisito": "Oficial Superior do Quadro de Oficiais Combatentes", "desdobramentos": [], "atribuicoes": ["Gerir a formação, disciplina e hierarquia; orientação e supervisão do Corpo Discente", "Fiscalizar, avaliar e acompanhar os programas de ensino"]},
  ],
  "conselho-consultivo": [
    {"cargo": "Presidente do Conselho Consultivo", "subordinadoA": "(órgão colegiado)", "requisito": "Comandante Geral", "desdobramentos": [], "atribuicoes": ["Assessorar o Comandante Geral em assuntos de alta relevância", "Decidir, em colegiado, sobre pessoal e legislação, inteligência, instrução e operações e disciplina"]},
  ],
},

# ── DISTRITO FEDERAL (Lei nº 8.255/1991 + Portaria nº 24/2020) ──
"df": {
  "comando-geral-df": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Distrito Federal", "requisito": "Coronel da ativa do Quadro de Oficiais BM Combatentes", "desdobramentos": ["Subcomando-Geral", "Chefe do Estado-Maior-Geral", "Departamentos", "Controlador", "Chefe de Gabinete", "Comandante Operacional", "Ajudância-Geral"], "atribuicoes": [
       "Representar a Corporação perante órgãos e entidades públicas e privadas e a sociedade (Art. 3º, I)",
       "Planejar, organizar, dirigir, coordenar, controlar e fiscalizar as atividades da Corporação (II)",
       "Praticar atos administrativos necessários ao funcionamento da Corporação (III)",
       "Nomear membros de conselhos previstos em lei (IV)",
       "Estabelecer as políticas e diretrizes estratégicas da Corporação (V)",
       "Decidir sobre questões administrativas (VI)",
       "Aprovar os planos estratégicos da Corporação, inclusive o de aplicação de recursos financeiros e o de emprego (VII)",
       "Movimentar os Oficiais do Alto Comando (VIII)",
       "Determinar a instauração de inquérito técnico (IX)",
       "Declarar aspirantes-a-oficial, demitir oficiais e promover ou excluir praças, observado o que consta do Estatuto dos Bombeiros Militares do CBMDF (X)",
       "Assessorar o Secretário de Segurança Pública do Distrito Federal e, quando solicitado, os órgãos nacionais de segurança pública, defesa civil e meio ambiente, nos assuntos de competência da Corporação (Art. 3º)",
       "Delegar competências, observados os limites estabelecidos em lei ou regulamento (XI)",
       "Supervisionar a administração orçamentária, financeira, contábil e patrimonial (XII)",
       "Nomear militares da reserva remunerada, na forma prevista em legislação específica (XIII)",
       "Promover a incorporação dos candidatos aprovados nos concursos públicos para os diversos Quadros ou Qualificações existentes na Corporação (XIV)",
       "Celebrar contratos, convênios, termos de cooperação, parcerias e similares (XV)",
       "Propor ao Governador do DF a criação de grupamentos e subgrupamentos, considerados os aspectos demográficos, os riscos específicos e o fator tempo-resposta (XVI)",
       "Instalar o Gabinete de Gerência de Incidentes, órgão de caráter eventual presidido pelo Comandante Operacional e baseado no Sistema de Comando de Incidentes (XVII)",
       "Avocar, em caráter excepcional e por motivos relevantes devidamente justificados, competência atribuída a órgão subordinado (XVIII)",
       "Conceder férias regulamentares aos oficiais do último posto (XIX)",
       "Presidir o Alto Comando da Corporação (XX)",
       "Presidir a Comissão de Promoção de Oficiais – CPO (XXI)"
     ]},
  ],
  "subcomando-geral-df": [
    {"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel do Quadro de Oficiais BM Combatentes da ativa", "desdobramentos": ["Departamento de Recursos Humanos", "Departamento de Administração Logística e Financeira", "Departamento de Ensino, Pesquisa, Ciência e Tecnologia", "Departamento de Segurança contra Incêndio"], "atribuicoes": ["Coordenar, fiscalizar e controlar as rotinas administrativas", "Substituir o Comandante-Geral em seus impedimentos", "Supervisionar e coordenar as atividades dos departamentos", "Presidir a Comissão de Promoção de Praças"]},
  ],
  "estado-maior-geral-df": [
    {"cargo": "Chefe do Estado-Maior-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel da ativa do Quadro de Oficiais BM Combatentes", "desdobramentos": ["Secretaria", "Seções (máximo 10)"], "atribuicoes": ["Orientação, coordenação e fiscalização dos trabalhos do EMG", "Estudo, planejamento, programação orçamentária e financeira", "Controle de todas as atividades da Corporação via órgãos subordinados"]},
  ],
  "controladoria-df": [
    {"cargo": "Controlador", "subordinadoA": "Comandante-Geral", "requisito": "Oficial superior", "desdobramentos": ["Auditoria", "Ouvidoria", "Corregedoria", "Núcleo de Custódia"], "atribuicoes": ["Defesa do patrimônio público; auditoria, correição e ouvidoria", "Averiguação das atividades de administração orçamentária, financeira, patrimonial e de pessoas"]},
  ],
  "gabinete-comandante-geral-df": [
    {"cargo": "Chefe de Gabinete do Comandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial superior", "desdobramentos": ["Seção de Gestão de Processos (SEGEP)", "Ajudância de Ordens (AJORD)", "Assessoria Técnico-Administrativa (ASTAD)", "Assessoria Parlamentar (ASPAR)", "Assessoria Jurídico-Legislativa (ASJUR)"], "atribuicoes": ["Assistir o Comandante-Geral na tomada de decisões técnicas e administrativas", "Analisar atos, solicitações e processos administrativos", "Expedir Instrução Normativa; garantir execução do Plano Estratégico"]},
  ],
  "departamentos-df": [
    {"cargo": "Chefe do Departamento de Recursos Humanos", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial superior", "desdobramentos": ["Diretoria de Gestão de Pessoal", "Diretoria de Inativos e Pensionistas", "Diretoria de Saúde"], "atribuicoes": ["Planejar, orientar, coordenar e controlar assistência à saúde, social e religiosa, cadastro, efetivos, avaliação, promoções, seleção e ingresso", "Movimentar oficiais (exceto Alto Comando) e praças", "Homologar o Plano de Férias Anual"]},
    {"cargo": "Chefe do Departamento de Administração Logística e Financeira", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial superior", "desdobramentos": ["Diretoria de Orçamento e Finanças", "Diretoria de Contratações e Aquisições", "Diretoria de Materiais e Serviços"], "atribuicoes": ["Planejar, orientar, coordenar e controlar orçamento e finanças, aquisições e contratações, materiais, obras e serviços, manutenção e patrimônio", "Elaborar o Plano de Contratações Anual; exercer função de Gestor do PCA"]},
    {"cargo": "Chefe do Departamento de Ensino, Pesquisa, Ciência e Tecnologia", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial superior", "desdobramentos": ["Diretoria de Ensino", "Diretoria de Pesquisa, Ciência e Tecnologia", "Diretoria de Tecnologia da Informação e Comunicação"], "atribuicoes": ["Planejar, orientar, coordenar e controlar formação, aperfeiçoamento, especialização e altos estudos", "Aprovar Plano de Ensino e Plano Diretor de TI", "Modernização administrativa e operacional"]},
    {"cargo": "Chefe do Departamento de Segurança contra Incêndio", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial superior", "desdobramentos": ["Diretoria de Vistorias", "Diretoria de Estudos e Análise de Projetos", "Diretoria de Investigação de Incêndio"], "atribuicoes": ["Planejar, orientar e controlar as atividades de segurança contra incêndio e pânico"]},
  ],
  "diretoria-gestao-pessoal-df": [
    {"cargo": "Diretor de Gestão de Pessoal", "subordinadoA": "Chefe do Departamento de Recursos Humanos", "requisito": "", "desdobramentos": [], "atribuicoes": ["Executar políticas de cadastro do pessoal ativo, inativo e pensionistas, controle de efetivos, avaliação, promoções, direitos e deveres, seleção e ingresso"]},
  ],
  "diretoria-saude-df": [
    {"cargo": "Diretor de Saúde", "subordinadoA": "Chefe do Departamento de Recursos Humanos", "requisito": "", "desdobramentos": ["Policlínica Médica", "Policlínica Odontológica", "Centro de Perícias Médicas"], "atribuicoes": ["Executar políticas de assistência à saúde, social e religiosa; saúde preventiva e curativa"]},
  ],
  "comando-operacional-df": [
    {"cargo": "Comandante Operacional", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": ["Subcomando Operacional", "Comandos de Área", "Grupamentos de Bombeiro Militar", "Comando Especializado", "Estado-Maior Operacional"], "atribuicoes": ["Planejamento estratégico e coordenação do emprego das unidades", "Execução de prevenção, combate a incêndio, busca e salvamento, atendimento pré-hospitalar e defesa civil"]},
  ],
  "ajudancia-geral-df": [
    {"cargo": "Ajudante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": ["Seção de Serviços Internos", "Seção de Protocolo-Geral", "Secretaria do Comando-Geral"], "atribuicoes": ["Auxiliar nas funções de administração do Quartel do Comando Geral"]},
  ],
},

# ── ESPÍRITO SANTO (Normas Gerais de Ação) ──
"es": {
  "comando-geral-es": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Oficial superior", "desdobramentos": ["Gabinete do Comando-Geral", "Assistência ao Comando", "Assessoria de Comunicação", "Assessoria Estratégica", "Assessoria de Inteligência", "Unidade Executora de Controle Interno", "Ajudância-Geral"], "atribuicoes": [
       "As previstas na legislação pertinente à Administração Pública e aos militares estaduais (Art. 5º, I)",
       "Praticar os atos necessários ao perfeito funcionamento do serviço do Corpo de Bombeiros Militar do Espírito Santo, visando o exercício da sua competência constitucional (II)",
       "Constituir comissões (III)",
       "Decidir questões administrativas (IV)",
       "Estabelecer a política de recursos humanos e de execução de atividades afetas ao CBMES (V)",
       "Aprovar regimentos, normas gerais de ação, planos, diretrizes e outros dos órgãos subordinados (VI)",
       "Promover praça e declarar Aspirante-a-Oficial (VII)",
       "Encaminhar expediente ao Governador do Estado e propor promulgação de atos que interessem ao CBMES (VIII)",
       "Instaurar Inquérito Policial Militar e Técnico, bem como Sindicância (IX)",
       "Baixar Portarias necessárias à administração do CBMES (X)",
       "Aprovar Normas e Pareceres Técnicos de órgãos subordinados (XI)",
       "Delegar atribuições de sua competência (XII)",
       "Outras que advenham de lei (XIII)"
     ]},
  ],
  "assistencia-comando-es": [
    {"cargo": "Assistente do Comandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": ["Assessoria Especial"], "atribuicoes": [
       "Assessorar o Comandante-Geral quanto a questões compreendidas na política de administração geral da Corporação (Art. 20, I)",
       "Examinar os aspectos de legalidade dos atos e normas oriundos do Comando-Geral, bem como a direção, orientação, coordenação, controle e fiscalização das atividades (II)",
       "Elaborar pareceres em assuntos jurídicos e administrativos (III)",
       "Realizar interface do CBMES junto à Procuradoria Geral do Estado, à Secretaria de Estado de Governo, e aos demais órgãos e entidades demandados nos atos do Comandante-Geral (IV)",
       "Estudar e propor ao Comandante-Geral medidas que lhe escapam à competência (V)"
     ]},
    {"cargo": "Gerente de Assessoria", "subordinadoA": "Assistente do Comandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": [
       "Assessorar o Assistente do Comandante-Geral no que se refere aos despachos, decisões e encaminhamentos dos processos de interesse do CBMES (Art. 21, I)",
       "Manter o Assistente do Comandante-Geral informado quanto ao andamento dos processos da Corporação, especialmente nos casos em que houver a ocorrência de eventuais questões que possam acarretar em prejuízos ao CBMES (II)",
       "Manter contato com autoridades civis e militares em assuntos de interesse do CBMES (III)",
       "Promover estudos e sugerir ao Assistente do Comandante-Geral medidas que visem a melhoria no rendimento e nas atividades da Seção (IV)"
     ]},
  ],
  "assessoria-comunicacao-es": [
    {"cargo": "Assessor de Comunicação Social", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": ["Setor de Secretaria", "Setor de Comunicação e Arte Visual", "Setor de Produção Áudio Visual", "Setor de Publicação e Marketing Social", "Cerimonial"], "atribuicoes": ["Planejar, desenvolver e coordenar a comunicação interna e externa", "Coordenar as relações do CBMES com os meios de comunicação", "Organizar o cerimonial do Comandante-Geral"]},
    {"cargo": "Chefe da Assessoria de Comunicação", "subordinadoA": "Assessor de Comunicação Social", "requisito": "", "desdobramentos": [], "atribuicoes": ["Gerir a seção da Assessoria de Comunicação; propor estratégia de marketing", "Responsabilizar-se pelas informações aos órgãos de imprensa"]},
  ],
  "assessoria-estrategica-es": [
    {"cargo": "Assessor Estratégico", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": ["Gerência de Inteligência Corporativa", "Departamento de Projetos Institucionais", "Departamento de Gestão do Conhecimento"], "atribuicoes": ["Inteligência corporativa, gestão do conhecimento e projetos institucionais", "Planejamentos administrativo e estratégico"]},
    {"cargo": "Gerente de Inteligência Corporativa", "subordinadoA": "Assessor Estratégico", "requisito": "", "desdobramentos": [], "atribuicoes": ["Estudos e pesquisas para aprimoramento da GIC", "Aperfeiçoamento da doutrina de inteligência corporativa"]},
    {"cargo": "Chefe do Departamento de Projetos Institucionais", "subordinadoA": "Assessor Estratégico", "requisito": "", "desdobramentos": ["Seção de Gestão de Projetos", "Seção de Engenharia, Arquitetura e Obras"], "atribuicoes": ["Gerir as seções do DepPI; monitorar prazos dos projetos", "Conduzir projetos alinhados ao Planejamento Estratégico"]},
  ],
  "ajudancia-geral-es": [
    {"cargo": "Ajudante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": ["Seção de Serviços Internos", "Seção de Protocolo-Geral", "Secretaria do Comando-Geral", "Seção de Expediente"], "atribuicoes": ["Atividades administrativas do Comando-Geral; protocolo geral e cerimonial", "Conservação das áreas comuns do QCG; controle de entrada de pessoas e veículos"]},
    {"cargo": "Ajudante de Ordens", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Acompanhar o Comandante-Geral em eventos internos e externos", "Organizar as agendas e os deslocamentos"]},
  ],
  "diretoria-gestao-pessoas-es": [
    {"cargo": "Diretor de Gestão de Pessoas", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": ["Centro de Recursos Humanos", "Gerência de Recursos Humanos", "Seção de Educação Física", "Centro de Serviço Social", "Centro de Ensino e Instrução de Bombeiros"], "atribuicoes": ["Planejar, coordenar, controlar e executar atividades de gestão de pessoas"]},
    {"cargo": "Gerente de Recursos Humanos", "subordinadoA": "Diretor de Gestão de Pessoas", "requisito": "", "desdobramentos": [], "atribuicoes": ["Gerenciar as atividades de pessoal do Centro de Recursos Humanos"]},
  ],
  "diretoria-operacoes-es": [
    {"cargo": "Diretor de Operações", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": ["1º ao 6º Batalhão de Bombeiros Militar", "Companhias Independentes", "Centro Especializado de Resposta a Desastres"], "atribuicoes": ["Planejar, coordenar, controlar e executar as atividades operacionais"]},
    {"cargo": "Comandante de Batalhão", "subordinadoA": "Diretor de Operações", "requisito": "", "desdobramentos": ["Companhias subordinadas", "Seções de Comando"], "atribuicoes": ["Comandar e executar as operações de bombeiros militares na sua área de responsabilidade"]},
  ],
  "diretoria-apoio-logistico-es": [
    {"cargo": "Diretor de Apoio Logístico", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": ["Seção de Expediente e Material Bélico", "Departamento de Orçamento e Finanças", "Centro de Suprimento e Processamento", "Departamento de Manutenção, Transporte e Radiocomunicação", "Gerência de Tecnologia da Informação"], "atribuicoes": ["Planejar, coordenar, controlar e executar as atividades de apoio logístico"]},
  ],
  "corregedoria-es": [
    {"cargo": "Diretor de Correição", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Realizar a atividade correcional", "Zelar pela justiça e disciplina dos integrantes da Corporação"]},
  ],
  "centro-atividades-tecnicas-es": [
    {"cargo": "Diretor do Centro de Atividades Técnicas", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Planejar, executar, controlar e fiscalizar as atividades de proteção contra incêndio", "Realizar perícias de incêndio e vistorias"]},
  ],
  "coordenadoria-protecao-defesa-civil-es": [
    {"cargo": "Diretor da Coordenadoria Estadual de Proteção e Defesa Civil", "subordinadoA": "Comandante-Geral", "requisito": "", "desdobramentos": [], "atribuicoes": ["Planejar, coordenar, dirigir e regular os serviços de proteção e defesa civil"]},
  ],
  "cg-es-lob": [
    {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Oficial da ativa do último posto do Quadro de Oficiais Combatentes BM (Art. 10)",
     "desdobramentos": ["Estado-Maior", "Diretorias", "Ajudância-Geral", "Comissões", "Assessorias", "Coordenadoria Estadual de Proteção e Defesa Civil", "Corregedoria"],
     "atribuicoes": [
       "A administração, o comando e o emprego da Corporação são de competência e responsabilidade do Comandante-Geral do Corpo de Bombeiros, assessorado pelos órgãos de direção (Art. 4º).",
       "O Comandante-Geral tem precedência hierárquica e funcional sobre todos os Oficiais da Corporação (Art. 10, §4º)."
     ]},
  ],
},

}
