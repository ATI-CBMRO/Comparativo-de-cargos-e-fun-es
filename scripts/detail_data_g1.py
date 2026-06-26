# detail_data_g1.py — Alagoas, Amapá, Amazonas
# Extraído fielmente das legislações. (Acre está em database/organs_detail/ac.json)

DATA = {

"al": {
  "legal_source": "Lei nº 6.212, de 26 de dezembro de 2000, regulamentada pelo Decreto nº 408, de 08 de novembro de 2001 (Regimento Interno)",
  "organs": {
    "cg-al": {
      "name": "Comandante Geral", "abbreviation": "CG", "category": "Direção Geral",
      "subordinadoA": "Governador do Estado / Secretário de Defesa Social", "legalRef": "Art. 8º",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)", "Art. 8º (Atribuições)"],
      "atribuicoes": [
        "Assessorar o Governador do Estado nos assuntos relacionados com as atividades bombeiro militar",
        "Assessorar o Secretário de Defesa Social nos assuntos de Segurança Pública",
        "Dirigir as atividades técnicas, operacionais e administrativas da Corporação",
        "Fazer cumprir as leis, normas e regulamentos da Corporação",
        "Baixar portarias e ordens de serviços",
        "Aplicar penas disciplinares de sua alçada",
        "Autorizar despesas, nos limites de sua competência",
        "Submeter ao Governador do Estado e ao Secretário de Defesa Social os planos, estudos, programas",
        "Exercer a supervisão superior dos órgãos de direção, de apoio e de execução",
        "Desempenhar as funções de Coordenador Estadual de Defesa Civil"
      ],
      "desdobramentos": ["Subcomandante Geral", "Conselho de Políticas Estratégicas", "Gabinete do Comandante Geral", "Corregedoria Geral", "Diretorias", "Comando Operacional de Bombeiros"],
      "cargos": [
        {"cargo": "Comandante Geral", "subordinadoA": "Governador do Estado", "requisito": "Oficial de posto elevado", "desdobramentos": [], "atribuicoes": ["Comando da Corporação"]}
      ]
    },
    "scg-al": {
      "name": "Subcomandante Geral", "abbreviation": "SCG", "category": "Direção Geral",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 9º",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)", "Art. 9º (Atribuições)"],
      "atribuicoes": [
        "Responder pelo Comandante Geral em seus impedimentos eventuais",
        "Exercer o controle disciplinar dos integrantes da Corporação",
        "Apresentar propostas ou emitir pareceres sobre assuntos administrativos e operacionais",
        "Coordenar e elaborar o relatório anual de atividades",
        "Secundar o Comandante Geral na fiscalização das atividades",
        "Coordenar as atividades, tarefas e trabalhos do Conselho de Políticas Estratégicas"
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Subcomandante Geral", "subordinadoA": "Comandante Geral", "requisito": "Oficial de posto elevado", "desdobramentos": [], "atribuicoes": ["Substituição do Comandante Geral", "Assessoramento ao Comandante Geral"]}
      ]
    },
    "cpet-al": {
      "name": "Conselho de Políticas Estratégicas", "abbreviation": "CPE", "category": "Direção Geral",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 10 e 11",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)", "Art. 10 e 11 (Atribuições)"],
      "atribuicoes": [
        "Assessorar nos assuntos referentes ao planejamento, coordenação e fiscalização",
        "Propor medidas necessárias ao aperfeiçoamento das atividades técnicas especializadas",
        "Supervisionar, dirigir e coordenar os trabalhos da Corporação"
      ],
      "desdobramentos": ["Comandante Geral", "Subcomandante Geral", "Chefe de Gabinete do Comandante Geral", "Diretor de Recursos Humanos", "Diretor de Material e Patrimônio", "Diretor de Finanças", "Diretor de Serviços Técnicos", "Diretor da Policlínica", "Corregedor Geral", "Ajudante Geral", "Comandante Operacional de Bombeiros"],
      "cargos": []
    },
    "cedec-al": {
      "name": "Coordenadoria Estadual de Defesa Civil", "abbreviation": "CEDEC", "category": "Direção Geral",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 12 a 19",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)", "Art. 12-19 (Atribuições)"],
      "atribuicoes": [
        "Promover, coordenar e supervisionar, no âmbito estadual, as ações de defesa civil",
        "Mobilizar recursos humanos e materiais necessários às ações de defesa civil",
        "Incentivar a criação e a implementação de Coordenadorias Municipais de Defesa Civil",
        "Propor ao Governador a homologação de situação de emergência ou estado de calamidade pública",
        "Coordenar e controlar a distribuição de suprimentos às populações atingidas"
      ],
      "desdobramentos": ["Coordenador Estadual de Defesa Civil", "Assessoria Técnica", "Secretaria Executiva", "Seção de Planejamento, Avaliação e Controle", "Seção de Coordenação e Controle Operacional", "Seção de Cadastro e Controle de Recursos", "Seção Administrativa"],
      "cargos": [
        {"cargo": "Coordenador Estadual de Defesa Civil", "subordinadoA": "Governador do Estado", "requisito": "Oficial", "desdobramentos": [], "atribuicoes": ["Exercer a coordenação geral das ações de defesa civil", "Dirigir as atividades técnicas, administrativas e operacionais da CEDEC", "Propor homologação de situação de emergência ou estado de calamidade pública"]},
        {"cargo": "Secretário Executivo", "subordinadoA": "Coordenador Estadual de Defesa Civil", "requisito": "Tenente Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Planejamento, coordenação, controle e execução das atribuições da CEDEC"]}
      ]
    },
    "gabinete-al": {
      "name": "Gabinete do Comandante Geral", "abbreviation": "GAB", "category": "Apoio ao Comando-Geral",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 7º, I, e",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)"],
      "atribuicoes": ["Assistência ao Comandante Geral", "Assessoramento ao Comandante Geral"],
      "desdobramentos": ["Chefia do Gabinete", "Ajudância de Ordem do Comandante Geral", "Assessoria de Inteligência e Contra-Inteligência", "Assessoria de Relações Públicas e Comunicação Social", "Secretaria Administrativa"],
      "cargos": [
        {"cargo": "Chefe do Gabinete do Comando Geral", "subordinadoA": "Comandante Geral", "requisito": "Tenente Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Direção do Gabinete do Comando Geral"]},
        {"cargo": "Ajudante de Ordens do Comandante Geral", "subordinadoA": "Comandante Geral", "requisito": "Capitão QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Assessoramento do Comandante Geral"]},
        {"cargo": "Chefe da Assessoria de Inteligência e Contra-Inteligência", "subordinadoA": "Comandante Geral", "requisito": "Major QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Assessoramento em inteligência e contra-inteligência"]},
        {"cargo": "Chefe da Assessoria de Relações Públicas e Comunicação Social", "subordinadoA": "Comandante Geral", "requisito": "Tenente Coronel QOBM/COMB", "desdobramentos": ["Subseção de Imprensa e Marketing", "Subseção de Relações Públicas, Publicidade e Propaganda"], "atribuicoes": ["Direção das atividades de comunicação social"]}
      ]
    },
    "corregedoria-al": {
      "name": "Corregedoria Geral", "abbreviation": "COR", "category": "Direção Geral",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 7º, I, f",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)"],
      "atribuicoes": ["Fiscalização disciplinar", "Apuração de desvios de conduta"],
      "desdobramentos": ["Corregedor Geral", "Subcorregedor Geral", "Ouvidoria", "Seção de Polícia Disciplinar", "Seção de Polícia Judiciária Militar", "Seção de Apoio Administrativo", "Seção de Inteligência"],
      "cargos": [
        {"cargo": "Corregedor Geral", "subordinadoA": "Comandante Geral", "requisito": "Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Direção da Corregedoria"]},
        {"cargo": "Subcorregedor Geral", "subordinadoA": "Corregedor Geral", "requisito": "Tenente Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Substituição do Corregedor Geral"]},
        {"cargo": "Ouvidor Geral", "subordinadoA": "Corregedor Geral", "requisito": "Tenente Coronel QOBM/COMB", "desdobramentos": ["Sub-Ouvidor Geral", "Assistente da Ouvidoria"], "atribuicoes": ["Ouvidoria da Corporação"]}
      ]
    },
    "drh-al": {
      "name": "Diretoria de Recursos Humanos", "abbreviation": "DRH", "category": "Direção Setorial",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 7º, I, g",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)"],
      "atribuicoes": ["Planejamento de recursos humanos", "Controle de pessoal", "Fiscalização de atividades de pessoal"],
      "desdobramentos": ["Seção de Seleção e Ingresso de RH", "Seção de Cadastro, Avaliação, Controle e Movimentação", "Seção de Desenvolvimento de RH", "Seção de Promoções", "Seção de Pagamento de Pessoal", "Seção de Inativos e Pensionistas", "Seção de Identificação", "Seção de Expediente e Arquivo", "Seção de Legislação"],
      "cargos": [
        {"cargo": "Diretor de Recursos Humanos", "subordinadoA": "Comandante Geral", "requisito": "Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Direção das atividades de recursos humanos"]},
        {"cargo": "Chefe da Seção de Seleção e Ingresso de RH", "subordinadoA": "Diretor de Recursos Humanos", "requisito": "Tenente Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Seleção e ingresso de pessoal"]},
        {"cargo": "Chefe da Seção de Pagamento de Pessoal", "subordinadoA": "Diretor de Recursos Humanos", "requisito": "Major QOBM/ADM", "desdobramentos": [], "atribuicoes": ["Pagamento de pessoal"]}
      ]
    },
    "dmp-al": {
      "name": "Diretoria de Material e Patrimônio", "abbreviation": "DMP", "category": "Direção Setorial",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 7º, I, h",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)"],
      "atribuicoes": ["Controle de material", "Controle de patrimônio", "Planejamento logístico"],
      "desdobramentos": ["Seção de Aquisições e Gestão de Contratos e Convênios", "Seção de Apoio a CPL", "Seção de Administração da Frota", "Seção de Cadastro, Controle e Alienação", "Seção de Administração, Expediente e Arquivo", "Seção de Estatística da DMP"],
      "cargos": [
        {"cargo": "Diretor de Material e Patrimônio", "subordinadoA": "Comandante Geral", "requisito": "Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Direção das atividades de material e patrimônio"]}
      ]
    },
    "df-al": {
      "name": "Diretoria de Finanças", "abbreviation": "DF", "category": "Direção Setorial",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 7º, I, i",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)"],
      "atribuicoes": ["Planejamento financeiro", "Controle de finanças", "Fiscalização de recursos orçamentários"],
      "desdobramentos": ["Seção de Administração Financeira", "Seção de Contabilidade e Auditoria", "Seção de Expediente e Arquivo", "Tesouraria Geral"],
      "cargos": [
        {"cargo": "Diretor de Finanças", "subordinadoA": "Comandante Geral", "requisito": "Tenente Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Direção das atividades de finanças"]}
      ]
    },
    "dst-al": {
      "name": "Diretoria de Serviços Técnicos", "abbreviation": "DST", "category": "Direção Setorial",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 7º, I, j",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)"],
      "atribuicoes": ["Planejamento de serviços técnicos", "Controle técnico", "Supervisão de atividades técnicas"],
      "desdobramentos": ["Seção de Estudos e Análises de Projetos", "Seção de Testes, Vistorias e Pareceres", "Seção de Perícias e Pesquisas", "Seção de Hidrantes"],
      "cargos": [
        {"cargo": "Diretor de Serviços Técnicos", "subordinadoA": "Comandante Geral", "requisito": "Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Direção das atividades de serviços técnicos"]}
      ]
    },
    "policlinica-al": {
      "name": "Diretoria da Policlínica", "abbreviation": "POL", "category": "Direção Setorial",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 7º, I, l",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)"],
      "atribuicoes": ["Planejamento de saúde", "Controle de atividades de saúde", "Fiscalização de serviços médicos"],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Diretor da Policlínica", "subordinadoA": "Comandante Geral", "requisito": "Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Direção das atividades da Policlínica"]}
      ]
    },
    "ag-al": {
      "name": "Ajudância Geral", "abbreviation": "AG", "category": "Apoio",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 7º, I, m",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)"],
      "atribuicoes": ["Funções administrativas do Comando Geral", "Secretaria", "Protocolo", "Arquivo", "Serviços gerais"],
      "desdobramentos": ["Secretaria Geral", "Seção Administrativa", "Seção de Comando e Serviço", "Protocolo Geral", "Arquivo Geral", "Biblioteca Geral", "Banda de Música"],
      "cargos": [
        {"cargo": "Ajudante Geral", "subordinadoA": "Comandante Geral", "requisito": "Tenente Coronel ou Capitão QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Direção da Ajudância Geral"]}
      ]
    },
    "cob-al": {
      "name": "Comando Operacional de Bombeiros", "abbreviation": "COB", "category": "Execução",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 7º, III, a",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 7º (Estrutura Básica)"],
      "atribuicoes": ["Coordenação operacional", "Execução das atividades-fins da Corporação"],
      "desdobramentos": ["Comando Operacional de Bombeiros da Região Metropolitana de Maceió", "Comando Operacional de Bombeiros do Interior"],
      "cargos": [
        {"cargo": "Comandante Operacional de Bombeiros", "subordinadoA": "Subcomandante Geral", "requisito": "Tenente Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Comando operacional"]}
      ]
    },
    "ubm-al": {
      "name": "Unidades de Bombeiros Militar", "abbreviation": "UBM", "category": "Execução",
      "subordinadoA": "Comando Operacional de Bombeiros", "legalRef": "Art. 113; Art. 114 RI/CBMAL",
      "baseLegal": "Decreto nº 408, de 08 de novembro de 2001",
      "artigosDeOrigem": ["Art. 113 (Unidades Operacionais de Bombeiros)", "Art. 114 (Comandante de Grupamento de Bombeiros Militar)"],
      "atribuicoes": [
        "I - planejar, coordenar, fiscalizar, controlar e executar as ações operacionais em suas áreas de atuação;",
        "II - levantar e manter registros atualizados dos principais riscos existentes em sua área, desenvolvendo planos setoriais para prevenção e proteção;",
        "III - coordenar, controlar, fiscalizar e executar a instrução de manutenção e adestramento da tropa;",
        "IV - manter registro estatístico das ocorrências verificadas em sua área de atuação operacional;",
        "V - efetuar a manutenção e manter registro dos bens móveis e imóveis que estiverem sob sua guarda;",
        "VI - elaborar as Normas Gerais de Ação da UOp e remetê-las à aprovação do Comandante do COB;",
        "VII - fiscalizar o cumprimento da legislação pertinente às suas atividades operacionais."
      ],
      "desdobramentos": ["Grupamento de Bombeiros Militar (GBM)", "Grupamento de Salvamento Aquático (GSA)", "Grupamento de Socorro de Emergência (GSE)"],
      "cargos": [{"cargo": "Comandante de Grupamento de Bombeiros Militar", "subordinadoA": "Comando Operacional de Bombeiros", "requisito": "Oficial QOBM/COMB", "desdobramentos": [], "atribuicoes": [
        "I - dirigir, cumprir e fazer cumprir as atividades relacionadas à prevenção, combate a incêndios e salvamento em altura e terrestre na sua área de atuação;",
        "II - praticar os atos administrativos necessários ao perfeito funcionamento da UOp e de suas subunidades;",
        "III - manter a tropa permanentemente adestrada e pronta para o emprego;",
        "IV - comandar diretamente as atividades operacionais que envolvam mais de uma operação de socorro bombeiro militar na área de atuação dos Subgrupamentos;",
        "V - desenvolver o espírito de iniciativa e camaradagem de seus subordinados;",
        "VI - comunicar imediatamente à autoridade superior qualquer fato grave ocorrido em sua área de atuação, solicitando intervenção nos casos que exijam a participação de outros órgãos;",
        "VII - controlar e zelar pela conservação e manutenção dos bens móveis e imóveis sob sua responsabilidade;",
        "VIII - providenciar a manutenção dos bens patrimoniais sob sua guarda;",
        "IX - elaborar e submeter à aprovação do Comandante do COB das Normas Gerais de Ação dos órgãos do Grupamento;",
        "X - movimentar os oficiais e praças no âmbito dos respectivos Subgrupamentos;",
        "XI - controlar e fiscalizar a execução, no âmbito das respectivas Subunidades Operacionais, dos planos e ordens superiores;",
        "XII - elaborar e manter atualizado o quadro estatístico de ocorrências operacionais de suas Subunidades;",
        "XIII - executar atos administrativos que lhes competirem, como integrante do sistema de administração de pessoal e material;",
        "XIV - instaurar sindicância;",
        "XV - exercer outros encargos que lhes forem atribuídos pelo Comandante Geral ou previstos em leis e regulamentos vigentes."
      ]}]
    },

    "cg-al-lob": {
      "name": "Comando Geral", "abbreviation": "CG", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 6º a 9º",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 6º (Comando Geral)", "Art. 7º (Requisitos do Comandante)", "Art. 8º (Competências)", "Art. 9º (Gabinete)"],
      "atribuicoes": [
        "O Comando Geral da Corporação compete ao Comandante Geral do Corpo de Bombeiros Militar do Estado de Alagoas, responsável pelo comando e a administração da instituição, bem como a coordenação geral das ações de Defesa Civil no Estado de Alagoas."
      ],
      "desdobramentos": ["Gabinete do Comandante Geral", "Subcomando Geral", "Conselho de Políticas Estratégicas", "Coordenadoria Estadual de Defesa Civil", "Corregedoria Geral", "Diretorias", "Secretaria Geral", "Comissões"],
      "cargos": []
    },
    "scg-al-lob": {
      "name": "Subcomando Geral", "abbreviation": "SCG", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 10",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 10 (Subcomando Geral)"],
      "atribuicoes": [
        "O Subcomando Geral do Corpo de Bombeiros Militar de Alagoas compete ao Oficial designado pelo Governador do Estado, sendo responsável por auxiliar direta e imediatamente o Comandante Geral, cumprindo-lhe substituí-lo em suas faltas ou impedimentos, dentre outras atribuições previstas em lei ou regulamento ou mediante expressa delegação do Comandante Geral da Corporação."
      ],
      "desdobramentos": [],
      "cargos": []
    },
    "cpe-al-lob": {
      "name": "Conselho de Políticas Estratégicas", "abbreviation": "CPE", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 11",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 11 (Conselho de Políticas Estratégicas)"],
      "atribuicoes": [
        "O Conselho de Políticas Estratégicas é um colegiado encarregado de assessorar ao Comandante Geral na formulação e avaliação de políticas estratégicas e na fixação de diretrizes de gerenciamento administrativo e de emprego do Corpo de Bombeiros Militar para o cumprimento de suas missões."
      ],
      "desdobramentos": ["Comandante Geral (presidente)", "Subcomandante Geral", "Diretor de Recursos Humanos", "Comandantes Operacionais", "Diretor de Material e Patrimônio", "Diretor de Finanças", "Diretor de Planejamento e Orçamento", "Diretor de Ensino", "Diretor de Serviços Técnicos", "Secretário Executivo da Defesa Civil"],
      "cargos": []
    },
    "cedc-al-lob": {
      "name": "Coordenadoria Estadual de Defesa Civil", "abbreviation": "CEDEC", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 12",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 12 (Coordenadoria Estadual de Defesa Civil)"],
      "atribuicoes": [
        "A Coordenadoria Estadual de Defesa Civil é órgão de coordenação central do Sistema Estadual de Defesa Civil, competindo-lhe o estudo, o planejamento, a orientação técnica, a coordenação, a supervisão, a execução, o controle e a avaliação das ações de defesa civil no Estado de Alagoas, observando o disposto na Lei nº 6.171, de 31 de julho de 2000."
      ],
      "desdobramentos": ["Coordenador Estadual de Defesa Civil", "Secretaria Executiva de Defesa Civil", "Assessoria Técnica", "Seção de Administração", "Seção de Operações", "Seção de Vistorias e Análise", "Seção de Planejamento"],
      "cargos": []
    },
    "corg-al-lob": {
      "name": "Corregedoria Geral", "abbreviation": "CORREG", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 13",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 13 (Corregedoria Geral)"],
      "atribuicoes": [
        "A Corregedoria Geral do Corpo de Bombeiros Militar é o órgão de direção encarregado da orientação, fiscalização e correção dos procedimentos relativos à apuração das transgressões disciplinares e das infrações penais militares dos Bombeiros Militares, promovendo-lhes, ainda, a responsabilidade funcional e disciplinar."
      ],
      "desdobramentos": ["Corregedor Geral", "Subcorregedor Geral", "Ouvidoria", "Seção de Polícia Disciplinar", "Seção de Polícia Judiciária Militar", "Seção de Apoio Administrativo", "Seção de Inteligência"],
      "cargos": []
    },
    "drh-al-lob": {
      "name": "Diretoria de Recursos Humanos", "abbreviation": "DRH", "category": "Direção Setorial", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 15",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 15 (Diretoria de Recursos Humanos)"],
      "atribuicoes": [
        "A Diretoria de Recursos Humanos é o órgão central do sistema de recursos humanos do Corpo de Bombeiros Militar, competindo-lhe o estudo, o planejamento, a orientação normativa, a coordenação, a supervisão, o controle e a execução das atividades relativas à gestão de pessoal e desenvolvimento de recursos humanos da Corporação, de acordo com as diretrizes da Secretaria de Estado da Gestão Pública - SEGESP."
      ],
      "desdobramentos": ["Seção de Seleção e Ingresso de Recursos Humanos", "Seção de Cadastro, Avaliação, Controle e Movimentação", "Seção de Desenvolvimento de Recursos Humanos", "Seção de Promoções", "Seção de Pagamento de Pessoal", "Seção de Inativos e Pensionistas", "Seção de Identificação", "Seção de Expediente e Arquivo", "Seção de Legislação"],
      "cargos": []
    },
    "dmp-al-lob": {
      "name": "Diretoria de Material e Patrimônio", "abbreviation": "DMP", "category": "Direção Setorial", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 16",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 16 (Diretoria de Material e Patrimônio)"],
      "atribuicoes": [
        "A Diretoria de Material e Patrimônio é o órgão central do sistema logístico do Corpo de Bombeiros Militar, competindo-lhe o estudo, o planejamento, a orientação normativa, a coordenação, a supervisão, o controle e a execução das atividades relativas à gestão do material e patrimônio da Corporação."
      ],
      "desdobramentos": ["Seção de Cadastro, Controle e Alienação", "Seção de Aquisição, Contratos e Convênios", "Seção de Administração da Frota", "Seção de Apoio a Comissão de Licitação", "Seção de Expediente e Arquivo"],
      "cargos": []
    },
    "dfin-al-lob": {
      "name": "Diretoria de Finanças", "abbreviation": "DFIN", "category": "Direção Setorial", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 17",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 17 (Diretoria de Finanças)"],
      "atribuicoes": [
        "A Diretoria de Finanças é o órgão central do sistema de administração financeira do Corpo de Bombeiros Militar, competindo-lhe o estudo, o planejamento, a orientação normativa, a coordenação, a supervisão, o controle e a execução das atividades relativas à gestão financeira, ao planejamento e execução orçamentária, à contabilidade e auditoria."
      ],
      "desdobramentos": ["Seção de Administração Financeira", "Seção de Contabilidade e Auditoria", "Seção de Expediente e Arquivo", "Tesouraria Geral"],
      "cargos": []
    },
    "dat-al-lob": {
      "name": "Diretoria de Atividades Técnicas", "abbreviation": "DAT", "category": "Direção Setorial", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 18",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 18 (Diretoria de Atividades Técnicas)"],
      "atribuicoes": [
        "A Diretoria de Atividades Técnicas é o órgão central do sistema de engenharia e segurança do Corpo de Bombeiros Militar, competindo-lhe o estudo, a análise, o planejamento, a orientação técnica, a execução, o controle e a fiscalização das atividades relativas à segurança contra incêndio e pânico e ao cumprimento das disposições legais sobre o assunto, no âmbito do Estado de Alagoas."
      ],
      "desdobramentos": ["Seção de Estudos e Análise de Projetos", "Seção de Testes, Vistorias e Pareceres", "Seção de Perícias e Pesquisas", "Seção de Hidrantes", "Seção de Expediente e Arquivo"],
      "cargos": []
    },
    "dpo-al-lob": {
      "name": "Diretoria de Planejamento e Orçamento", "abbreviation": "DPO", "category": "Direção Setorial", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 19",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 19 (Diretoria de Planejamento e Orçamento)"],
      "atribuicoes": [
        "A Diretoria de Planejamento e Orçamento é o órgão central do sistema de Planejamento Estratégico e Orçamentário do Corpo de Bombeiros Militar, competindo-lhe a coordenação do planejamento, a orientação técnica, o monitoramento, o controle e a fiscalização das atividades relativas ao planejamento estratégico, bem como a elaboração e execução do orçamento da Corporação."
      ],
      "desdobramentos": ["Seção de Administração", "Seção de Informações", "Seção de Monitoramento da Estrutura Organizacional", "Seção de Planejamento, Execução, Controle e Fiscalização Orçamentária"],
      "cargos": []
    },
    "dens-al-lob": {
      "name": "Diretoria de Ensino", "abbreviation": "DENS", "category": "Direção Setorial", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 20",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 20 (Diretoria de Ensino)"],
      "atribuicoes": [
        "A Diretoria de Ensino é o órgão de apoio do sistema de ensino da Corporação, incumbindo-lhe o estudo, o planejamento, a supervisão e o controle das atividades de ensino e capacitação profissional da Instituição."
      ],
      "desdobramentos": ["Seção Técnica de Ensino", "Seção de Legislação de Ensino", "Seção de Convênios de Ensino", "Seção de Avaliação e Controle do Ensino", "Academia de Formação de Bombeiros Militares"],
      "cargos": []
    },
    "sg-al-lob": {
      "name": "Secretaria Geral", "abbreviation": "SG", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 21",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 21 (Secretaria Geral)"],
      "atribuicoes": [
        "A Secretaria Geral é o órgão de direção encarregado da administração do Quartel do Comando Geral, considerado como Organização Bombeiro Militar, bem como do expediente, da execução dos trabalhos de secretaria, incluindo a correspondência, correio, redação e impressão do boletim diário, do protocolo e arquivo geral e biblioteca, do apoio em pessoal aos órgãos que compõem o Comando Geral, dos serviços gerais, da banda de música e da segurança do Quartel do Comando Geral."
      ],
      "desdobramentos": ["Seção Administrativa", "Seção de Comando e Serviço", "Protocolo Geral", "Arquivo Geral e Biblioteca", "Banda de Música"],
      "cargos": []
    },
    "com-al-lob": {
      "name": "Comissões", "abbreviation": "COM", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 22",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 22 (Comissões)"],
      "atribuicoes": [
        "As Comissões são órgãos de assessoramento do Comandante Geral, constituídas para tratar de assuntos específicos de interesse da Corporação e se destinam a dar flexibilidade à estrutura do Comando Geral."
      ],
      "desdobramentos": ["Comissão de Promoção de Oficiais", "Comissão de Promoção de Praças", "Comissão Permanente de Licitação", "Comissões temporárias"],
      "cargos": []
    },
    "cman-al-lob": {
      "name": "Centro de Manutenção", "abbreviation": "CMAN", "category": "Apoio", "source": "lob",
      "subordinadoA": "Diretoria de Material e Patrimônio", "legalRef": "Art. 24",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 24 (Centro de Manutenção)"],
      "atribuicoes": [
        "O Centro de Manutenção é o órgão de apoio do sistema logístico, subordinado à Diretoria de Material e Patrimônio, incumbido das atividades de manutenção do material e do patrimônio da Corporação, inclusive das instalações, bem como do recebimento e da estocagem de todo material necessário a esse fim."
      ],
      "desdobramentos": ["Seção de Manutenção de Material Motomecanizado", "Seção de Manutenção de Material Operacional", "Seção de Manutenção de Obras", "Seção de Administração"],
      "cargos": []
    },
    "cti-al-lob": {
      "name": "Centro de Tecnologia em Informática e Informação", "abbreviation": "CTI", "category": "Apoio", "source": "lob",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 25",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 25 (Centro de Tecnologia em Informática e Informação)"],
      "atribuicoes": [
        "O Centro de Tecnologia em Informática e Informação é o órgão que gerencia e administra os recursos tecnológicos e computacionais de geração e uso da informação como também todo o parque de informática do Corpo de Bombeiros Militar, subordinado ao Subcomandante Geral, encarregado de desenvolver e manter sistemas informatizados, para as áreas administrativa, operacional, internet e intranet da Corporação, dar suporte tecnológico e apoio ao usuário, provendo informações de planejamento e avaliação da gestão pública."
      ],
      "desdobramentos": ["Seção de Gerenciamento de Redes e Infraestrutura", "Seção de Banco de Dados", "Seção de Desenvolvimento de Sistemas, Internet e Intranet", "Seção de Suporte e Apoio ao Usuário"],
      "cargos": []
    },
    "cass-al-lob": {
      "name": "Centro de Assistência", "abbreviation": "CASS", "category": "Apoio", "source": "lob",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 26",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 26 (Centro de Assistência)"],
      "atribuicoes": [
        "O Centro de Assistência é o órgão de apoio do sistema de recursos humanos, subordinado ao Subcomandante Geral, incumbido do suporte ao sistema de atendimento pré-hospitalar, do estudo, planejamento, a supervisão, a execução e o controle das atividades de assistência médica, odontológica, farmacêutica, sanitária, religiosa e de assistência social aos Bombeiros Militares e seus dependentes, na forma da legislação em vigor."
      ],
      "desdobramentos": ["Subchefia", "Junta de Inspeção de Saúde", "Serviço de Clínica Médica e Atendimento Ambulatorial", "Serviço Odontológico", "Serviço de Enfermaria", "Serviço de Farmácia", "Serviço de Capelania", "Serviço de Assistência Psicossocial", "Serviço de Administração"],
      "cargos": []
    },
    "almox-al-lob": {
      "name": "Almoxarifado Central", "abbreviation": "ALMOX", "category": "Apoio", "source": "lob",
      "subordinadoA": "Diretoria de Material e Patrimônio", "legalRef": "Art. 27",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 27 (Almoxarifado Central)"],
      "atribuicoes": [
        "O Almoxarifado Central é o órgão de apoio do sistema logístico, subordinado à Diretoria de Material e Patrimônio, incumbido do recebimento, da estocagem e da distribuição de suprimentos específicos e execução da manutenção do material de intendência."
      ],
      "desdobramentos": [],
      "cargos": []
    },
    "aprov-al-lob": {
      "name": "Aprovisionamento Central", "abbreviation": "APROV", "category": "Apoio", "source": "lob",
      "subordinadoA": "Diretoria de Material e Patrimônio", "legalRef": "Art. 28",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 28 (Aprovisionamento Central)"],
      "atribuicoes": [
        "O Aprovisionamento Central é o órgão de apoio do sistema logístico, subordinado à Diretoria de Material e Patrimônio, incumbido do recebimento, da estocagem e da distribuição de suprimentos e material de subsistência."
      ],
      "desdobramentos": [],
      "cargos": []
    },
    "cob-al-lob": {
      "name": "Comandos Operacionais de Bombeiros", "abbreviation": "COB", "category": "Execução", "source": "lob",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 29, 30",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 29 (Órgãos de Execução)", "Art. 30 (Comando Operacional de Bombeiros)"],
      "atribuicoes": [
        "Comando Operacional de Bombeiros é a denominação genérica dada a Organização Bombeiro-Militar de mais alto escalão do sistema operacional, subordinado ao Subcomandante Geral, que tem a seu cargo o planejamento estratégico, a coordenação e o emprego das Unidades Operacionais da Corporação que lhe forem subordinadas, com a finalidade de executar as missões de prevenção e extinção de incêndios, de resgate, busca e salvamento, de atendimento aos traumas e emergências pré-hospitalares e de defesa civil, além de outras, em uma determinada área operacional."
      ],
      "desdobramentos": ["Comando Operacional de Bombeiros da Região Metropolitana", "Comando Operacional de Bombeiros do Interior", "Comandos de Bombeiros de Áreas (Agreste, Sertão, Litoral Norte, Litoral Sul)", "Conselho de Comandantes", "Centro de Operações e Comunicações"],
      "cargos": []
    },
    "uop-al-lob": {
      "name": "Unidades Operacionais", "abbreviation": "UOP", "category": "Execução", "source": "lob",
      "subordinadoA": "Comando Operacional de Bombeiros / Comando de Bombeiros de Área", "legalRef": "Art. 31 a 41",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 31 (Unidades Operacionais)", "Art. 32 (Tipos)", "Art. 41 (Estrutura comum)"],
      "atribuicoes": [
        "Unidades Operacionais são as que têm a missão principal de emprego nas mais diversas operações Bombeiros Militares, dos tipos: Grupamento de Incêndio (GI), Grupamento de Bombeiros Militar (GBM), Grupamento de Salvamento Aquático (GSA), Grupamento de Socorro de Emergência (GSE), Grupamento de Busca e Salvamento (GBS), Grupamento de Proteção Ambiental (GPA) e Grupamento de Operações Aéreas (GOA)."
      ],
      "desdobramentos": ["Comando", "Subcomando", "Secretaria", "Seção de Administração", "Seção de Manutenção", "Almoxarifado", "Seção de Operações e Instrução", "Subunidades"],
      "cargos": []
    },
    "oesp-al-lob": {
      "name": "Órgão Especial (Seção Aérea e Bombeiros do Gabinete Militar)", "abbreviation": "OESP", "category": "Especial", "source": "lob",
      "subordinadoA": "Gabinete Militar do Governador", "legalRef": "Art. 42",
      "baseLegal": "Lei nº 7.444, de 28 de dezembro de 2012 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 42 (Órgão Especial)"],
      "atribuicoes": [
        "O Órgão Especial a que se refere este Capítulo compreende a Seção Aérea e Bombeiros do Gabinete Militar competindo-lhe o assessoramento, planejamento, coordenação, fiscalização, manutenção e controle das operações aéreas nas missões Bombeiro Militar, além do transporte aéreo do Governador e das autoridades por ele designadas."
      ],
      "desdobramentos": [],
      "cargos": []
    }
  }
},

"ap": {
  "legal_source": "Lei Complementar nº 180, de 06 de janeiro de 2026",
  "organs": {
    "cg-ap": {
      "name": "Comandante-Geral", "abbreviation": "CG", "category": "Direção Geral",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 3º e 4º",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 3º (Subordinação)", "Art. 4º (Estrutura Organizacional)"],
      "atribuicoes": ["Direção superior, planejamento estratégico e administração geral da Instituição (Art. 6º, §1º, I)", "Cargo considerado de nível equivalente ao de Secretário de Estado (Art. 3º)"],
      "desdobramentos": ["Subcomandante-Geral", "Órgãos de Direção-Geral", "Órgãos de Direção Setorial"],
      "cargos": [
        {"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel do Quadro de Oficiais do Estado-Maior da ativa, nomeado pelo Governador; cargo de nível equivalente ao de Secretário de Estado (Art. 3º)", "desdobramentos": [], "atribuicoes": ["Comando superior e administração geral do Corpo de Bombeiros Militar do Estado do Amapá (Art. 3º)"]}
      ]
    },
    "scg-ap": {
      "name": "Subcomandante-Geral", "abbreviation": "SCG", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 4º",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 4º (Estrutura Organizacional)"],
      "atribuicoes": ["O Subcomandante-Geral substituirá o Comandante-Geral em seus impedimentos, ausências ou afastamentos, ocasião em que será formalmente nomeado pelo Governador do Estado como Comandante-Geral em substituição (Art. 3º, §1º)"],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel do Quadro de Oficiais do Estado-Maior da ativa, indicado pelo Comandante-Geral e nomeado pelo Governador do Estado (Art. 3º)", "desdobramentos": [], "atribuicoes": ["Substituição do Comandante-Geral em seus impedimentos, ausências ou afastamentos (Art. 3º, §1º)"]}
      ]
    },
    "gabinete-ap": {
      "name": "Gabinete do Comandante-Geral", "abbreviation": "GAB", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 6º, § 1º",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 6º (Organização e Estrutura)"],
      "atribuicoes": ["Órgão de direção-geral, responsável pela direção superior, planejamento estratégico e administração geral da Instituição (Art. 6º, §1º, I)"],
      "desdobramentos": ["Gabinete do Comandante-Geral", "Gabinete do Subcomandante-Geral"],
      "cargos": []
    },
    "cdoem-ap": {
      "name": "Comitê de Desenvolvimento Organizacional", "abbreviation": "CDO", "category": "Direção-Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 6º, § 1º, I",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 6º, §1º, I (órgãos de direção-geral)"],
      "atribuicoes": ["Órgão de direção-geral, responsável pela direção superior, planejamento estratégico e administração geral da Instituição (Art. 6º, §1º, I)"],
      "desdobramentos": [], "cargos": []
    },
    "comando-operacional-ap": {
      "name": "Comando Operacional", "abbreviation": "CmtOp", "category": "Direção-Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 6º, § 1º, I",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 6º, §1º, I (órgãos de direção-geral)"],
      "atribuicoes": ["Órgão de direção-geral, responsável pela direção superior, planejamento estratégico e administração geral da Instituição (Art. 6º, §1º, I)"],
      "desdobramentos": [], "cargos": []
    },
    "frcb-ap": {
      "name": "Fundo de Reequipamento do Corpo de Bombeiros", "abbreviation": "FRCB", "category": "Direção-Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 6º, § 1º, I",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 6º, §1º, I (órgãos de direção-geral)"],
      "atribuicoes": ["Integra os órgãos de direção-geral, responsáveis pela direção superior, planejamento estratégico e administração geral da Instituição (Art. 6º, §1º, I)"],
      "desdobramentos": [], "cargos": []
    },
    "diretorias-ap": {
      "name": "Diretorias (Órgãos de Direção Setorial)", "abbreviation": "DIR", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 6º, § 1º, II",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 6º, §1º, II (órgãos de direção setorial)"],
      "atribuicoes": ["Órgãos de direção setorial, responsáveis pela administração setorial das atividades de inteligência, recursos humanos, pesquisa e desenvolvimento, gestão orçamentária, financeira e ambiental, bem como pelo assessoramento técnico, planejamento, coordenação, execução, controle e fiscalização das atividades administrativas da Corporação e das políticas de desenvolvimento institucional (Art. 6º, §1º, II)"],
      "desdobramentos": ["Diretoria de Inteligência", "Diretoria de Recursos Humanos", "Diretoria de Pesquisa e Desenvolvimento", "Diretoria de Gestão Orçamentária e Financeira", "Diretoria Ambiental"],
      "cargos": []
    },
    "aci-ap": {
      "name": "Assessoria de Controle Interno", "abbreviation": "ACI", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 6º, § 2º",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 6º, §2º (órgãos de assessoramento)"],
      "atribuicoes": ["Órgão de assessoramento destinado a prestar assessoria, consultoria, recomendação e orientação técnica e política e a expedir nota técnica, para auxiliar as decisões dos órgãos de direção em assuntos especializados (Art. 6º, §2º)"],
      "desdobramentos": [], "cargos": []
    },
    "aj-ap": {
      "name": "Assessoria Jurídica", "abbreviation": "AJ", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 6º, § 2º",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 6º, §2º (órgãos de assessoramento)"],
      "atribuicoes": ["Órgão de assessoramento destinado a prestar assessoria, consultoria, recomendação e orientação técnica e política e a expedir nota técnica, para auxiliar as decisões dos órgãos de direção em assuntos especializados (Art. 6º, §2º)"],
      "desdobramentos": [], "cargos": []
    },
    "at-ap": {
      "name": "Assessoria Técnica", "abbreviation": "AT", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 6º, § 2º",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 6º, §2º (órgãos de assessoramento)"],
      "atribuicoes": ["Órgão de assessoramento destinado a prestar assessoria, consultoria, recomendação e orientação técnica e política e a expedir nota técnica, para auxiliar as decisões dos órgãos de direção em assuntos especializados (Art. 6º, §2º)"],
      "desdobramentos": [], "cargos": []
    },
    "centros-ap": {
      "name": "Centros (Órgãos de Apoio)", "abbreviation": "CEN", "category": "Apoio",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 6º, § 3º",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 6º, §3º (órgãos de apoio)"],
      "atribuicoes": ["Órgãos de apoio destinados, entre outras atribuições, ao atendimento das necessidades de recursos humanos, saúde, ensino, pesquisa e logística, responsáveis pela realização das atividades-meio da instituição (Art. 6º, §3º)"],
      "desdobramentos": ["Centros", "Academia Bombeiro Militar", "Coordenadorias"],
      "cargos": []
    },
    "gbm-ap": {
      "name": "Grupamentos de Bombeiro Militar", "abbreviation": "GBM", "category": "Execução",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 6º, § 4º",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 6º, §4º (órgãos de execução)"],
      "atribuicoes": ["Órgãos de execução destinados à realização das atividades-fim da instituição (Art. 6º, §4º)"],
      "desdobramentos": ["Grupamentos de Bombeiro Militar", "Grupamentos Especializados"],
      "cargos": []
    },
    "corregedoria-ap": {
      "name": "Corregedoria-Geral", "abbreviation": "COR", "category": "Correição",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 6º, § 5º",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 6º, §5º (órgãos de correição)"],
      "atribuicoes": ["Órgão de correição, com atuação desconcentrada, destinado a exercer as funções de Corregedoria-Geral, mediante regulamentação de procedimentos internos, para a prevenção, fiscalização e apuração dos desvios de conduta em atos disciplinares e penais militares, a promoção da qualidade e eficiência do serviço de segurança pública e a instrumentalização da Justiça Militar (Art. 6º, §5º)", "Acompanhar o cumprimento de medidas cautelares restritivas de direitos e mandados de prisão judicialmente deferidos em desfavor de militares dentro da instituição (Art. 6º, §5º)"],
      "desdobramentos": [], "cargos": []
    },
    "em-ap": {
      "name": "Escola Militar", "abbreviation": "EM", "category": "Órgão Vinculado",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 6º, § 6º",
      "baseLegal": "Lei Complementar nº 180, de 06 de janeiro de 2026",
      "artigosDeOrigem": ["Art. 6º, §6º (órgãos vinculados)"],
      "atribuicoes": ["Órgão vinculado, com regulamentação, organização e estruturação próprias, vinculado ao CBMAP, por meio do desenvolvimento de atividades inerentes à atividade militar e à Defesa Civil (Art. 6º, §6º)"],
      "desdobramentos": ["Projetos Sociais (entre outros previstos no decreto regulamentador)"], "cargos": []
    }
  }
},

"am": {
  "legal_source": "Lei nº 2.538, de 08 de junho de 1999 (e Lei Delegada nº 89, de 18 de maio de 2007; Lei nº 3.437/2009)",
  "organs": {
    "cg-am": {
      "name": "Comando Geral", "abbreviation": "CG", "category": "Direção Geral",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 8º, I; Art. 9º",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 8º (Órgãos de Direção Geral)", "Art. 9º (Comandante Geral)"],
      "atribuicoes": [
        "Responsável pelo comando, administração e emprego da Corporação",
        "Execução do planejamento",
        "Coordenação, fiscalização e acionamento dos órgãos de apoio e de execução"
      ],
      "desdobramentos": ["Subcomandante Geral", "Coordenadoria Estadual de Defesa Civil", "Conselho Superior de Políticas Estratégicas", "Gabinete do Comando-Geral", "Ajudância Geral", "Comissões"],
      "cargos": [
        {"cargo": "Comandante Geral", "subordinadoA": "Governador do Estado", "requisito": "Oficial superior combatente da ativa, possuidor do CSBM, do último posto (Coronel)", "desdobramentos": [], "atribuicoes": ["Comando, administração e emprego da Corporação", "Assessoramento por oficiais superiores na função de assistentes"]}
      ]
    },
    "scg-am": {
      "name": "Subcomandante Geral", "abbreviation": "SCG", "category": "Direção Geral",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 11 e 12",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 11 e 12 (Subcomandante Geral)"],
      "atribuicoes": [
        "Substituição automática do Comandante Geral nas suas faltas e impedimentos",
        "Principal assessor do Comandante Geral",
        "Direção, orientação, coordenação e fiscalização de todos os trabalhos internos"
      ],
      "desdobramentos": [],
      "cargos": [
        {"cargo": "Subcomandante Geral", "subordinadoA": "Comandante Geral (indicado) e Governador (nomeado)", "requisito": "Oficial superior combatente da ativa do último posto", "desdobramentos": [], "atribuicoes": ["Direção, orientação, coordenação e fiscalização de todos os trabalhos internos da Corporação"]}
      ]
    },
    "cedec-am": {
      "name": "Coordenadoria Estadual de Defesa Civil", "abbreviation": "CEDEC", "category": "Direção Geral",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 14",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 14 (CEDEC)"],
      "atribuicoes": ["Centralização do Sistema Estadual de Defesa Civil", "Integração, planejamento, organização, coordenação e supervisão", "Execução de medidas preventivas de socorro, assistência e recuperação"],
      "desdobramentos": ["Coordenador Estadual de Defesa Civil", "Assessoria Técnica", "Secretaria Executiva", "Subcomando Geral da Defesa Civil (SUBCOMADEC)", "Subcomando de Pronto Atendimento e Resgate (SUBPAR)"],
      "cargos": [{"cargo": "Coordenador Estadual de Defesa Civil", "subordinadoA": "Governador do Estado", "requisito": "Integrante da estrutura da CEDEC (Art. 14 §2º)", "desdobramentos": [], "atribuicoes": ["Coordenação das atividades de defesa civil previstas no Art. 14 da Lei nº 2.538/1999."]}]
    },
    "cspe-am": {
      "name": "Conselho Superior de Políticas Estratégicas", "abbreviation": "CSPE", "category": "Direção Geral",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 15",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 15 (CSPE)"],
      "atribuicoes": ["Assessoramento do Comandante Geral", "Formulação e avaliação de políticas estratégicas", "Fixação de diretrizes de gerenciamento administrativo"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Presidente do CSPE", "subordinadoA": "—", "requisito": "Comandante Geral (presidente nato — Art. 15)", "desdobramentos": [], "atribuicoes": ["Presidência do colegiado de assessoramento estratégico do Comando Geral (Art. 15)."]}]
    },
    "gabinete-am": {
      "name": "Gabinete do Comando-Geral", "abbreviation": "GAB", "category": "Apoio ao Comando-Geral",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 16 e 17",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 16 e 17 (Gabinete)"],
      "atribuicoes": ["Assistência e assessoramento direto ao Comandante Geral", "Controle e supervisão do expediente pessoal do Comandante Geral"],
      "desdobramentos": ["Chefe de Gabinete", "Secretário", "Assessor de Comunicações e Imprensa (ACI)", "Assessor Jurídico (AJ)", "Ajudante-de-Ordens"],
      "cargos": [
        {"cargo": "Chefe de Gabinete", "subordinadoA": "Comandante Geral", "requisito": "Tenente Coronel QOBM/COMB", "desdobramentos": [], "atribuicoes": ["Direção do Gabinete"]}
      ]
    },
    "ag-am": {
      "name": "Ajudância Geral", "abbreviation": "AG", "category": "Apoio",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 18",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 18 (Ajudância Geral)"],
      "atribuicoes": ["Funções administrativas do Comando Geral", "Trabalhos de secretaria", "Serviço de embarque da Corporação", "Segurança do Quartel do Comando Geral"],
      "desdobramentos": ["Secretaria Geral (AG-0)", "Seção Administrativa (AG-1)", "Seção de Protocolo e Distribuição (AG-2)", "Seção de Transporte e Embarque (AG-3)", "Seção de Comando e Serviço (AG-4)", "Banda de Música"],
      "cargos": [
        {"cargo": "Ajudante Geral", "subordinadoA": "Comandante Geral", "requisito": "Coronel QOBM", "desdobramentos": [], "atribuicoes": ["Direção da Ajudância Geral"]}
      ]
    },
    "drh-am": {
      "name": "Diretoria de Recursos Humanos", "abbreviation": "DRH", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 21 e 22",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 21 e 22 (DRH)"],
      "atribuicoes": ["Planejamento de recursos humanos", "Controle e fiscalização das atividades relacionadas com políticas de pessoal", "Capacitação técnica", "Assistência psicológica, social, jurídica e religiosa"],
      "desdobramentos": ["Seção de Controle de Pessoal Ativo, Inativo e Civil (DRH-1)", "Seção de Recrutamento, Seleção e Serviço Reservado (DRH-2)", "Seção de Cadastro, Identificação, Avaliação, Classificação, Movimentação e Promoções (DRH-3)", "Seção de Desenvolvimento Humano (DRH-4)", "Seção de Expediente e Mobilização (DRH-5)", "Seção de Pagadoria de Pessoal (DRH-6)", "Centro de Assistência Social e Religiosa (CASR)"],
      "cargos": [
        {"cargo": "Diretor de Recursos Humanos", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Direção das atividades de recursos humanos"]}
      ]
    },
    "df-am": {
      "name": "Diretoria de Finanças", "abbreviation": "DF", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 23 e 24",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 23 e 24 (DF)"],
      "atribuicoes": ["Atividades específicas da gestão orçamentária e financeira", "Controle de repasse de recursos orçamentários", "Captação de recursos financeiros"],
      "desdobramentos": ["Seção de Administração Financeira (DF-1)", "Seção de Contabilidade (DF-2)", "Seção de Auditoria (DF-3)", "Seção de Expediente (DF-4)"],
      "cargos": [
        {"cargo": "Diretor de Finanças", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Direção das atividades de finanças"]}
      ]
    },
    "dl-am": {
      "name": "Diretoria de Logística", "abbreviation": "DL", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 25 e 26",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 25 e 26 (DL)"],
      "atribuicoes": ["Planejamento, coordenação, fiscalização e controle das atividades de suprimento", "Controle das atividades de material da Corporação", "Elaboração de convênios"],
      "desdobramentos": ["Seção de Suprimento (DL-1)", "Seção de Manutenção (DL-2)", "Seção de Patrimônio e Expediente (DL-3)", "Centro de Suprimento e Manutenção de Materiais e Serviços (CSM/MS)"],
      "cargos": [
        {"cargo": "Diretor de Logística", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Direção das atividades de logística"]}
      ]
    },
    "deipo-am": {
      "name": "Diretoria de Ensino, Instrução, Pesquisa e Operações", "abbreviation": "DEIPO", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 27 e 28",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 27 e 28 (DEIPO)"],
      "atribuicoes": ["Coordenação, fiscalização, controle das atividades de ensino, instrução e pesquisa", "Planejamento operacional da Corporação"],
      "desdobramentos": ["Seção de Ensino, Instrução e Pesquisa (DEIPO-1)", "Seção de Projetos e Programas Especiais (DEIPO-2)", "Seção de Planejamento, Expediente e Meios Auxiliares (DEIPO-3)", "Escola de Bombeiros Militar (ESBOM)", "Centro de Informática (CInf)"],
      "cargos": [
        {"cargo": "Diretor de Ensino, Instrução, Pesquisa e Operações", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Direção das atividades de ensino, instrução, pesquisa e operações"]}
      ]
    },
    "dst-am": {
      "name": "Diretoria de Serviços Técnicos", "abbreviation": "DST", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 29 e 30",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 29 e 30 (DST)"],
      "atribuicoes": ["Estudo, análise, planejamento de atividades de prevenção", "Segurança contra incêndios e pânico", "Perícias de incêndio e explosão", "Realização de vistorias e emissão de pareceres"],
      "desdobramentos": ["Seção de Exames de Projetos (DST-1)", "Seção de Vistorias e Pareceres (DST-2)", "Seção de Hidrante, Expediente e Apoio (DST-3)", "Centro de Perícia de Incêndio (CPI)"],
      "cargos": [
        {"cargo": "Diretor de Serviços Técnicos", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Direção das atividades de serviços técnicos"]}
      ]
    },
    "casr-am": {
      "name": "Centro de Assistência Social e Religiosa", "abbreviation": "CASR", "category": "Apoio",
      "subordinadoA": "Diretoria de Recursos Humanos", "legalRef": "Art. 32 e 33",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 32 e 33 (CASR)"],
      "atribuicoes": ["Prestação de serviços assistenciais e religiosos aos componentes do Corpo de Bombeiros e seus dependentes"],
      "desdobramentos": ["Seção de Assistência (CASR-1)", "Seção de Orientação e Encaminhamento (CASR-2)", "Seção de Assistência Religiosa (CASR-3)"],
      "cargos": [
        {"cargo": "Chefe do CASR", "subordinadoA": "Diretor de Recursos Humanos", "requisito": "Oficial", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Assistência Social e Religiosa"]}
      ]
    },
    "csm-am": {
      "name": "Centro de Suprimento e Manutenção de Materiais e Serviços", "abbreviation": "CSM/MS", "category": "Apoio",
      "subordinadoA": "Diretoria de Logística", "legalRef": "Art. 34",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 34 (CSM/MS)"],
      "atribuicoes": ["Aquisição de suprimentos", "Execução de obras", "Transporte de pessoal e material", "Armamentos e munições"],
      "desdobramentos": ["Seção de Recebimento e Distribuição (CSM/MS-1)", "Seção de Oficinas (CSM/MS-2)", "Seção de Expediente, Obras e Serviços Gerais (CSM/MS-3)"],
      "cargos": [
        {"cargo": "Chefe do CSM/MS", "subordinadoA": "Diretor de Logística", "requisito": "Oficial", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Suprimento e Manutenção"]}
      ]
    },
    "esbom-am": {
      "name": "Escola de Bombeiros Militar", "abbreviation": "ESBOM", "category": "Apoio",
      "subordinadoA": "Diretoria de Ensino, Instrução, Pesquisa e Operações", "legalRef": "Art. 35 e 36",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 35 e 36 (ESBOM)"],
      "atribuicoes": ["Formação, aperfeiçoamento e especialização de bombeiros", "Desenvolvimento de estudos e pesquisas técnico-científicas"],
      "desdobramentos": ["Comando", "Secretaria", "Divisão de Ensino (DE)", "Divisão Administrativa (DA)", "Corpo de Alunos (CA)"],
      "cargos": [
        {"cargo": "Comandante da ESBOM", "subordinadoA": "Diretor de DEIPO", "requisito": "Oficial", "desdobramentos": [], "atribuicoes": ["Comando e direção da Escola"]}
      ]
    },
    "cinf-am": {
      "name": "Centro de Informática", "abbreviation": "CInf", "category": "Apoio",
      "subordinadoA": "Diretoria de Ensino, Instrução, Pesquisa e Operações", "legalRef": "Art. 37 e 38",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 37 e 38 (CInf)"],
      "atribuicoes": ["Otimização de áreas administrativas e operacionais", "Desenvolvimento de programas e sistemas"],
      "desdobramentos": ["Seção de Suporte (CInf-1)", "Seção de Desenvolvimento e Manutenção de Sistemas (CInf-2)", "Seção de Treinamento (CInf-3)"],
      "cargos": [
        {"cargo": "Chefe do CInf", "subordinadoA": "Diretor de DEIPO", "requisito": "Oficial", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Informática"]}
      ]
    },
    "cpi-am": {
      "name": "Centro de Perícia de Incêndio", "abbreviation": "CPI", "category": "Apoio",
      "subordinadoA": "Diretoria de Serviços Técnicos", "legalRef": "Art. 39 e 40",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 39 e 40 (CPI)"],
      "atribuicoes": ["Investigações de incêndios e explosões", "Coletas e análises laboratoriais", "Emissão de conclusões técnicas"],
      "desdobramentos": ["Seção de Investigação e Coleta (CPI-1)", "Seção de Análises Laboratoriais (CPI-2)", "Seção de Meios e Expedientes (CPI-3)"],
      "cargos": [
        {"cargo": "Chefe do CPI", "subordinadoA": "Diretor de Serviços Técnicos", "requisito": "Oficial", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Perícia de Incêndio"]}
      ]
    },
    "cobom-am": {
      "name": "Centro de Operações Bombeiro Militar", "abbreviation": "COBOM", "category": "Execução",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 43 e 44",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 43 e 44 (COBOM)"],
      "atribuicoes": ["Controle e coordenação de ações operacionais", "Serviços de comunicações"],
      "desdobramentos": ["Seção de Operações (COBOM-1)", "Seção de Comunicações (COBOM-2)", "Seção de Apoio (COBOM-3)"],
      "cargos": [
        {"cargo": "Chefe do COBOM", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial", "desdobramentos": [], "atribuicoes": ["Direção do Centro de Operações"]}
      ]
    },
    "cbc-am": {
      "name": "Comando de Bombeiros da Capital", "abbreviation": "CBC", "category": "Execução",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 45 e 46",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 45 e 46 (Comando de Bombeiros da Capital)"],
      "atribuicoes": ["Planejamento estratégico, coordenação, fiscalização e emprego das Unidades", "Execução de atividades de prevenção, combate a incêndio, busca e salvamento, socorros de emergência e defesa civil"],
      "desdobramentos": ["Comando", "Seção de Administração e Apoio (SAA)", "Seção de Planejamento Operacional (SPO)", "Batalhões de Incêndio (BI)", "Batalhão de Bombeiro Especial (BBE)", "Batalhão de Incêndio Florestal e Meio Ambiente (BIF/MA)", "Companhias de Incêndio (CI)", "Companhias de Incêndio Florestal e Meio Ambiente (CIF/MA)", "Pelotões de Incêndio (PEL/INC)"],
      "cargos": [
        {"cargo": "Comandante do CBC", "subordinadoA": "Subcomandante Geral", "requisito": "Tenente Coronel QOBM", "desdobramentos": [], "atribuicoes": ["Comando das operações na capital"]}
      ]
    },
    "cbi-am": {
      "name": "Comando de Bombeiros do Interior", "abbreviation": "CBI", "category": "Execução",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 45 e 46",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999",
      "artigosDeOrigem": ["Art. 45 e 46 (Comando de Bombeiros do Interior)"],
      "atribuicoes": ["Planejamento estratégico, coordenação, fiscalização e emprego das Unidades", "Execução de atividades de prevenção, combate a incêndio, busca e salvamento, socorros de emergência e defesa civil"],
      "desdobramentos": ["1ª Cia. Independente BM — Itacoatiara (1ª CIBM)", "2ª Cia. Independente BM — Manacapuru (2ª CIBM)", "3ª Cia. Independente BM — Parintins (3ª CIBM)", "1º Pelotão Independente BM — Tefé (1º PIBM)", "2º Pelotão Independente BM — Tabatinga (2º PIBM)"],
      "cargos": [
        {"cargo": "Comandante do CBI", "subordinadoA": "Subcomandante Geral", "requisito": "Tenente Coronel QOBM", "desdobramentos": [], "atribuicoes": ["Comando das operações no interior"]}
      ]
    },

    "cg-am-lob": {
      "name": "Comando Geral", "abbreviation": "CG", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 8º, I; Art. 9º e 10",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 8º (Órgãos de Direção Geral)", "Art. 9º (Comandante Geral)", "Art. 10 (Requisitos e nomeação)"],
      "atribuicoes": [
        "O Comandante Geral do Corpo de Bombeiros Militar do Estado do Amazonas é responsável pelo comando, administração e emprego da Corporação.",
        "O Comandante Geral do CBMAM, no âmbito do Estado do Amazonas, tem honras e prerrogativas de Secretário de Estado (Art. 9º, parágrafo único)."
      ],
      "desdobramentos": ["Subcomandante Geral", "Coordenadoria Estadual de Defesa Civil", "Conselho Superior de Políticas Estratégicas", "Gabinete", "Ajudância Geral (AG)", "Comissões"],
      "cargos": []
    },
    "scg-am-lob": {
      "name": "Subcomandante Geral", "abbreviation": "SCG", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante Geral (indicação) / Governador do Estado (nomeação)", "legalRef": "Art. 11 a 13",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 11 (Substituto automático)", "Art. 12 (Requisitos e nomeação)", "Art. 13 (Competências)"],
      "atribuicoes": [
        "O Subcomandante Geral é o substituto automático do Comandante Geral nas suas faltas e impedimentos (Art. 11).",
        "O Subcomandante Geral é o principal assessor do Comandante Geral, competindo-lhe dirigir, orientar, coordenar e fiscalizar todos os trabalhos internos da Corporação (Art. 13).",
        "O Subcomandante Geral do CBMAM, no âmbito do Estado do Amazonas, tem honras e prerrogativas de Subsecretário de Estado (Art. 13, parágrafo único)."
      ],
      "desdobramentos": [],
      "cargos": []
    },
    "cedec-am-lob": {
      "name": "Coordenadoria Estadual de Defesa Civil", "abbreviation": "CEDEC", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 8º, II; Art. 14",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 8º (Órgãos de Direção Geral)", "Art. 14 (CEDEC)"],
      "atribuicoes": [
        "A Coordenadoria Estadual de Defesa Civil (CEDEC), órgão de direção geral, centraliza o Sistema Estadual de Defesa Civil e tem por finalidade estabelecer normas e o exercício das atividades de integrar, planejar, organizar, coordenar e supervisionar a execução das medidas preventivas de socorro, de assistência e de recuperação, considerando os efeitos produzidos por fatos adversos de qualquer natureza e nas situações de emergência ou estado de calamidade pública (Art. 14).",
        "A Coordenadoria Estadual de Defesa Civil terá seu regimento, estrutura própria e dotação orçamentária específica para os fins a que se destina (Art. 14, § 2º)."
      ],
      "desdobramentos": [],
      "cargos": []
    },
    "cspe-am-lob": {
      "name": "Conselho Superior de Políticas Estratégicas", "abbreviation": "CSPE", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 8º, III; Art. 15",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 8º (Órgãos de Direção Geral)", "Art. 15 (CSPE)"],
      "atribuicoes": [
        "O Conselho Superior de Políticas Estratégicas (CSPE), constituído pelo Comandante Geral, Subcomandante Geral, Comandantes de Bombeiros da Capital e do Interior e Diretores Setoriais, reunir-se-á, eventualmente, por convocação do Comandante Geral, ou em datas por ele prefixadas, e terá suas atribuições definidas no Regimento Interno da Corporação (Art. 15)."
      ],
      "desdobramentos": ["Comandante Geral", "Subcomandante Geral", "Comandantes de Bombeiros da Capital e do Interior", "Diretores Setoriais"],
      "cargos": []
    },
    "gabinete-am-lob": {
      "name": "Gabinete do Comando-Geral", "abbreviation": "GAB", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 8º, IV; Art. 16 e 17",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 8º (Órgãos de Direção Geral)", "Art. 16 (Gabinete)", "Art. 17 (Funções de confiança)"],
      "atribuicoes": [
        "O Gabinete do Comando-Geral tem a seu cargo as funções de assistência e assessoramento direto ao Comandante Geral nos assuntos que refogem às atribuições normais e específicas dos demais órgãos de direção (Art. 16).",
        "Ao Gabinete do Comando-Geral cabe o controle e a supervisão do expediente pessoal do Comandante Geral (Art. 16, parágrafo único)."
      ],
      "desdobramentos": ["Chefe de Gabinete", "Secretário", "Assessor de Comunicações e Imprensa (ACI)", "Assessor Jurídico (AJ)", "Ajudante-de-Ordens"],
      "cargos": []
    },
    "ag-am-lob": {
      "name": "Ajudância Geral", "abbreviation": "AG", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 8º, V; Art. 18",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 8º (Órgãos de Direção Geral)", "Art. 18 (Ajudância Geral)"],
      "atribuicoes": [
        "A Ajudância Geral (AG) é o órgão responsável pelas funções administrativas do Comando Geral (Art. 18).",
        "São atribuições da Ajudância Geral: trabalhos de secretaria, inclusive correspondências, correios, protocolo geral, arquivo geral e boletim geral (a); serviço de embarque da Corporação (b); apoio de pessoal auxiliar (militar e civil) aos órgãos do Comando Geral (c); serviços gerais (d); e segurança do Quartel do Comando Geral (e) (Art. 18, § 1º)."
      ],
      "desdobramentos": ["Secretaria Geral", "Seção Administrativa (AG-1)", "Seção de Protocolo e Distribuição (AG-2)", "Seção de Transporte e Embarque (AG-3)", "Seção de Comando e Serviço (AG-4)", "Banda de Música"],
      "cargos": []
    },
    "comissoes-am-lob": {
      "name": "Comissões", "abbreviation": "COM", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 8º, VI; Art. 19",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 8º (Órgãos de Direção Geral)", "Art. 19 (Comissões)"],
      "atribuicoes": [
        "As Comissões, órgãos de assessoramento superior do Comando Geral, constituídas para dirimir assuntos específicos, serão de caráter permanente ou temporário (Art. 19).",
        "A Comissão de Promoção de Oficiais (CPO), presidida pelo Comandante-Geral, e a Comissão de Promoções de Praças (CPP), pelo Subcomandante Geral, terão caráter permanente (Art. 19, § 1º).",
        "Além das Comissões de que trata este artigo, poderão ser constituídas outras Comissões, de caráter temporário, destinadas a estudos específicos, a critério do Comandante-Geral (Art. 19, § 2º)."
      ],
      "desdobramentos": ["Comissão de Promoção de Oficiais (CPO)", "Comissão de Promoções de Praças (CPP)", "Comissões temporárias"],
      "cargos": []
    },
    "drh-am-lob": {
      "name": "Diretoria de Recursos Humanos", "abbreviation": "DRH", "category": "Direção Setorial", "source": "lob",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 20, I; Art. 21 e 22",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 20 (Órgãos de Direção Setorial)", "Art. 21 (DRH)", "Art. 22 (Organização)"],
      "atribuicoes": [
        "A Diretoria de Recursos Humanos (DRH) é o órgão de direção setorial responsável pelo planejamento, controle e fiscalização das atividades relacionadas com políticas de pessoal, da admissão, da capacitação técnica, da assistência psicológica, social, jurídica e religiosa, pela remuneração do pessoal e pela prevenção de acidentes no trabalho (Art. 21).",
        "Às Diretorias, sob a coordenação do Subcomandante Geral, competem, também, em suas áreas específicas: produzir informações (I); realizar estudos de situação (II); apresentar propostas e sugestões (III); elaborar planos e ordens para aprovação do Comandante-Geral (IV); e supervisionar, no âmbito de sua competência, a execução dos planos e ordens (V) (Art. 20, parágrafo único)."
      ],
      "desdobramentos": ["Seção de Controle de Pessoal Ativo, Inativo e Civil (DRH-1)", "Seção de Recrutamento, Seleção e Serviço Reservado (DRH-2)", "Seção de Cadastro, Identificação, Avaliação, Classificação, Movimentação e Promoções (DRH-3)", "Seção de Desenvolvimento Humano (DRH-4)", "Seção de Expediente e Mobilização (DRH-5)", "Seção de Pagadoria de Pessoal (DRH-6)", "Centro de Assistência Social e Religiosa (CASR)"],
      "cargos": []
    },
    "df-am-lob": {
      "name": "Diretoria de Finanças", "abbreviation": "DF", "category": "Direção Setorial", "source": "lob",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 20, II; Art. 23 e 24",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 20 (Órgãos de Direção Setorial)", "Art. 23 (DF)", "Art. 24 (Organização)"],
      "atribuicoes": [
        "A Diretoria de Finanças (DF) é o órgão de direção setorial responsável pelas atividades específicas da gestão orçamentária e financeira, supervisão destas junto aos demais órgãos da Corporação, controle de repasse de recursos orçamentários e captação de recursos financeiros, de acordo com o planejamento estabelecido (Art. 23).",
        "À Diretoria de Finanças (DF) compete o controle e a fiscalização da execução orçamentária e financeira da Corporação (Art. 23, parágrafo único)."
      ],
      "desdobramentos": ["Seção de Administração Financeira (DF-1)", "Seção de Contabilidade (DF-2)", "Seção de Auditoria (DF-3)", "Seção de Expediente (DF-4)"],
      "cargos": []
    },
    "dl-am-lob": {
      "name": "Diretoria de Logística", "abbreviation": "DL", "category": "Direção Setorial", "source": "lob",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 20, III; Art. 25 e 26",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 20 (Órgãos de Direção Setorial)", "Art. 25 (DL)", "Art. 26 (Organização)"],
      "atribuicoes": [
        "A Diretoria de Logística (DL) é o órgão de direção setorial responsável pelo planejamento, coordenação, fiscalização e controle das atividades de suprimento e material da Corporação, além da elaboração de convênios e atividades de saúde (Art. 25)."
      ],
      "desdobramentos": ["Seção de Suprimento (DL-1)", "Seção de Manutenção (DL-2)", "Seção de Patrimônio e Expediente (DL-3)", "Centro de Suprimento e Manutenção de Materiais e Serviços (CSM/MS)"],
      "cargos": []
    },
    "deipo-am-lob": {
      "name": "Diretoria de Ensino, Instrução, Pesquisa e Operações", "abbreviation": "DEIPO", "category": "Direção Setorial", "source": "lob",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 20, IV; Art. 27 e 28",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 20 (Órgãos de Direção Setorial)", "Art. 27 (DEIPO)", "Art. 28 (Organização)"],
      "atribuicoes": [
        "A Diretoria de Ensino, Instrução, Pesquisa e Operações (DEIPO) é o órgão de direção setorial responsável pela coordenação, fiscalização, controle das atividades de ensino, instrução, pesquisa e pelo planejamento operacional da Corporação (Art. 27)."
      ],
      "desdobramentos": ["Seção de Ensino, Instrução e Pesquisa (DEIPO-1)", "Seção de Projetos e Programas Especiais (DEIPO-2)", "Seção de Planejamento, Expediente e Meios Auxiliares (DEIPO-3)", "Escola de Bombeiros Militar (ESBOM)", "Centro de Informática (CInf)"],
      "cargos": []
    },
    "dst-am-lob": {
      "name": "Diretoria de Serviços Técnicos", "abbreviation": "DST", "category": "Direção Setorial", "source": "lob",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 20, V; Art. 29 e 30",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 20 (Órgãos de Direção Setorial)", "Art. 29 (DST)", "Art. 30 (Organização)"],
      "atribuicoes": [
        "A Diretoria de Serviços Técnicos (DST) é o órgão de direção setorial incumbido de estudar, analisar, planejar, exigir, fiscalizar as atividades atinentes à prevenção e segurança contra incêndios e pânico, além de proceder testes, exames de plantas, perícias de incêndio e explosão, a realizar vistorias e emitir pareceres e supervisionar a instalação de hidrantes na rede pública (Art. 29)."
      ],
      "desdobramentos": ["Seção de Exames de Projetos (DST-1)", "Seção de Vistorias e Pareceres (DST-2)", "Seção de Hidrante, Expediente e Apoio (DST-3)", "Centro de Perícia de Incêndio (CPI)"],
      "cargos": []
    },
    "casr-am-lob": {
      "name": "Centro de Assistência Social e Religiosa", "abbreviation": "CASR", "category": "Apoio", "source": "lob",
      "subordinadoA": "Diretoria de Recursos Humanos", "legalRef": "Art. 31, I, a; Art. 32 e 33",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 31 (Órgãos de Apoio)", "Art. 32 (CASR)", "Art. 33 (Organização)"],
      "atribuicoes": [
        "O Centro de Assistência Social e Religiosa (CASR), órgão de apoio de pessoal, subordinado diretamente à Diretoria de Recursos Humanos, destina-se à prestação de serviços assistenciais e religiosos aos componentes do Corpo de Bombeiros e seus dependentes (Art. 32)."
      ],
      "desdobramentos": ["Seção de Assistência (CASR-1)", "Seção de Orientação e Encaminhamento (CASR-2)", "Seção de Assistência Religiosa (CASR-3)"],
      "cargos": []
    },
    "csm-am-lob": {
      "name": "Centro de Suprimento e Manutenção de Materiais e Serviços", "abbreviation": "CSM/MS", "category": "Apoio", "source": "lob",
      "subordinadoA": "Diretoria de Logística", "legalRef": "Art. 31, II, a; Art. 34",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 31 (Órgãos de Apoio)", "Art. 34 (CSM/MS)"],
      "atribuicoes": [
        "O Centro de Suprimento e Manutenção de Materiais e Serviços (CSM/MS), órgão de apoio logístico, subordinado à Diretoria de Logística, destina-se à aquisição de suprimentos, execução de obras, manutenção e transporte de pessoal e material, em proveito de toda a Corporação, inclusive armamentos e munições (Art. 34)."
      ],
      "desdobramentos": ["Seção de Recebimento e Distribuição (CSM/MS-1)", "Seção de Oficinas (CSM/MS-2)", "Seção de Expediente, Obras e Serviços Gerais (CSM/MS-3)"],
      "cargos": []
    },
    "esbom-am-lob": {
      "name": "Escola de Bombeiros Militar", "abbreviation": "ESBOM", "category": "Apoio", "source": "lob",
      "subordinadoA": "Diretoria de Ensino, Instrução, Pesquisa e Operações", "legalRef": "Art. 31, III, a; Art. 35 e 36",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 31 (Órgãos de Apoio)", "Art. 35 (ESBOM)", "Art. 36 (Estrutura)"],
      "atribuicoes": [
        "A Escola de Bombeiros Militar (ESBOM), órgão de apoio de ensino subordinado à Diretoria de Ensino, Instrução, Pesquisa e Operações (DEIPO), destina-se à formação, aperfeiçoamento e especialização de bombeiros, bem como ao desenvolvimento de estudos e pesquisas técnico-científicas (Art. 35).",
        "Dependendo da disponibilidade de pessoal, material, instalações e recursos financeiros, estes serviços poderão, mediante convênio, ser estendidos a civis, oficiais e praças de outras corporações (Art. 35, parágrafo único)."
      ],
      "desdobramentos": ["Comando", "Secretaria", "Divisão de Ensino (DE)", "Divisão Administrativa (DA)", "Corpo de Alunos (CA)"],
      "cargos": []
    },
    "cinf-am-lob": {
      "name": "Centro de Informática", "abbreviation": "CInf", "category": "Apoio", "source": "lob",
      "subordinadoA": "Diretoria de Ensino, Instrução, Pesquisa e Operações", "legalRef": "Art. 31, III, b; Art. 37 e 38",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 31 (Órgãos de Apoio)", "Art. 37 (CInf)", "Art. 38 (Organização)"],
      "atribuicoes": [
        "O Centro de Informática (CInf), órgão de apoio, subordinado diretamente à Diretoria de Ensino, Instrução, Pesquisa e Operações (DEIPO), destina-se a realizar programas e sistemas para a otimização das áreas administrativas e operacionais da Corporação (Art. 37)."
      ],
      "desdobramentos": ["Seção de Suporte (CInf-1)", "Seção de Desenvolvimento e Manutenção de Sistemas (CInf-2)", "Seção de Treinamento (CInf-3)"],
      "cargos": []
    },
    "cpi-am-lob": {
      "name": "Centro de Perícia de Incêndio", "abbreviation": "CPI", "category": "Apoio", "source": "lob",
      "subordinadoA": "Diretoria de Serviços Técnicos", "legalRef": "Art. 31, IV, a; Art. 39 e 40",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 31 (Órgãos de Apoio)", "Art. 39 (CPI)", "Art. 40 (Organização)"],
      "atribuicoes": [
        "O Centro de Perícia de Incêndio (CPI), órgão de apoio, subordinado à Diretoria de Serviços Técnicos (DST), destina-se a realizar investigações, coletas e análises laboratoriais relacionadas com a perícia de incêndios e explosões e a emitir conclusões técnicas sobre suas atividades (Art. 39)."
      ],
      "desdobramentos": ["Seção de Investigação e Coleta (CPI-1)", "Seção de Análises Laboratoriais (CPI-2)", "Seção de Meios e Expedientes (CPI-3)"],
      "cargos": []
    },
    "cobom-am-lob": {
      "name": "Centro de Operações Bombeiro Militar", "abbreviation": "COBOM", "category": "Execução", "source": "lob",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 42, I; Art. 43 e 44",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 41 (Finalidade)", "Art. 42 (Órgãos de Execução)", "Art. 43 (COBOM)", "Art. 44 (Organização)"],
      "atribuicoes": [
        "O Centro de Operações Bombeiro Militar (COBOM), órgão de execução, subordinado ao Subcomandante Geral, destina-se ao controle, coordenação, serviços de comunicações e ações operacionais (Art. 43)."
      ],
      "desdobramentos": ["Seção de Operações (COBOM-1)", "Seção de Comunicações (COBOM-2)", "Seção de Apoio (COBOM-3)"],
      "cargos": []
    },
    "cbc-am-lob": {
      "name": "Comando de Bombeiros da Capital", "abbreviation": "CBC", "category": "Execução", "source": "lob",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 42, II; Art. 45 a 47",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 42 (Órgãos de Execução)", "Art. 45 (CBC e CBI)", "Art. 46 (Organização)", "Art. 47 (Unidades Operacionais)"],
      "atribuicoes": [
        "O Comando de Bombeiros da Capital (CBC) e o Comando de Bombeiros do Interior (CBI), órgãos de execução, subordinados ao Subcomandante Geral, destinam-se ao planejamento estratégico, à coordenação, à fiscalização e ao emprego das Unidades e Sub-unidades que lhe forem subordinadas, com a finalidade de executar atividades de prevenção, combate a incêndio, busca e salvamento, atendimento de socorros de emergência e defesa civil, além de outras atividades previstas em lei (Art. 45)."
      ],
      "desdobramentos": ["Comando", "Seção de Administração e Apoio (SAA)", "Seção de Planejamento Operacional (SPO)", "Batalhões de Incêndio (BI)", "Batalhão de Bombeiro Especial (BBE)", "Batalhão de Incêndio Florestal e Meio Ambiente (BIF/MA)", "Companhias de Incêndio (CI)", "Companhia de Bombeiro Especial (CBE)", "Companhias de Incêndio Florestal e Meio Ambiente (CIF/MA)", "Pelotões de Incêndio (PEL/INC)", "Pelotões de Incêndio Florestal e Meio Ambiente (PEL/MA)", "Pelotões de Bombeiros Especiais (PEL/BE)"],
      "cargos": []
    },
    "cbi-am-lob": {
      "name": "Comando de Bombeiros do Interior", "abbreviation": "CBI", "category": "Execução", "source": "lob",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 42, III; Art. 45 a 47",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 42 (Órgãos de Execução)", "Art. 45 (CBC e CBI)", "Art. 46 (Organização)", "Art. 47 (Unidades Operacionais)"],
      "atribuicoes": [
        "O Comando de Bombeiros da Capital (CBC) e o Comando de Bombeiros do Interior (CBI), órgãos de execução, subordinados ao Subcomandante Geral, destinam-se ao planejamento estratégico, à coordenação, à fiscalização e ao emprego das Unidades e Sub-unidades que lhe forem subordinadas, com a finalidade de executar atividades de prevenção, combate a incêndio, busca e salvamento, atendimento de socorros de emergência e defesa civil, além de outras atividades previstas em lei (Art. 45)."
      ],
      "desdobramentos": ["Comando", "Seção de Administração e Apoio (SAA)", "Seção de Planejamento Operacional (SPO)", "Batalhões de Incêndio (BI)", "Batalhão de Bombeiro Especial (BBE)", "Batalhão de Incêndio Florestal e Meio Ambiente (BIF/MA)", "Companhias de Incêndio (CI)", "Companhia de Bombeiro Especial (CBE)", "Companhias de Incêndio Florestal e Meio Ambiente (CIF/MA)", "Pelotões de Incêndio (PEL/INC)", "Pelotões de Incêndio Florestal e Meio Ambiente (PEL/MA)", "Pelotões de Bombeiros Especiais (PEL/BE)"],
      "cargos": []
    },
    "bbm-am-lob": {
      "name": "Batalhão de Bombeiros Militar", "abbreviation": "BBM", "category": "Execução", "source": "lob",
      "subordinadoA": "Comando de Bombeiros da Capital (CBC) / Comando de Bombeiros do Interior (CBI)", "legalRef": "Art. 42, IV; Art. 48 a 53",
      "baseLegal": "Lei nº 2.538, de 08 de junho de 1999 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 42 (Órgãos de Execução)", "Art. 48 e 49 (Batalhão de Incêndio)", "Art. 50 e 51 (Batalhão de Bombeiro Especial)", "Art. 52 e 53 (Batalhão de Incêndio Florestal e Meio Ambiente)"],
      "atribuicoes": [
        "O Batalhão de Incêndio (BI), unidade operacional, órgão de execução, subordinado ao Comando de Bombeiros da Capital (CBC) ou Comando de Bombeiros do Interior (CBI), destina-se à coordenação, ao controle, à fiscalização e à execução de atividade operacional e administrativa em sua área de atuação (Art. 48).",
        "O Batalhão de Bombeiro Especial (BBE), unidade operacional e órgão de execução, subordinado ao Comando de Bombeiros da Capital, destina-se à coordenação, ao controle, à fiscalização e à execução de atividades administrativas e operacionais de salvamento, busca, resgate e emergências médicas (Art. 50).",
        "O Batalhão de Incêndio Florestal e Meio Ambiente (BIF/MA), unidade operacional, órgão de execução, subordinado ao Comando Operacional do Interior, destina-se à prevenção e combate a incêndio florestal e queimadas e socorro ao meio ambiente, em conformidade com a lei (Art. 52)."
      ],
      "desdobramentos": ["Comando", "Seção Administrativa (SA)", "Seção Operacional (SO)", "Companhias de Incêndios (CI)", "Pelotões de Incêndios (PEL/INC)", "Companhias de Bombeiro Especial (CBE)", "Pelotões de Bombeiros Especiais (PEL/BE)", "Companhias de Incêndio Florestal e Meio Ambiente (CIF/MA)", "Pelotões de Incêndio Florestal e Meio Ambiente (PEL/IF/MA)"],
      "cargos": []
    }
  }
},

}
