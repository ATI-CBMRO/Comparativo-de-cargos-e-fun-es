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
    }
  }
},

}
