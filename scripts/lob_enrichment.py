"""
lob_enrichment.py — Portal CBM

Camada CURADA da LOB para o comparativo /comparar (coluna "LOB do estado" e
parte "LOB" da coluna compilada). Para cada (organ_key, estado), a finalidade
e/ou os incisos VERBATIM que a Lei de Organização Básica do estado dá ao órgão,
com citação da fonte. Diferente de minuta_enrichment.ENRICHMENT_ORGAN (que é RI):
aqui é só LOB, e admite a finalidade/caput (1 frase) além de incisos.

Consumido por build_minuta_comparison.py. NÃO altera organs_detail nem ENRICHMENT_ORGAN.
"""

# LOB_ENRICHMENT[(organ_key, state_id)] -> entrada verbatim da LOB.
LOB_ENRICHMENT = {
    ("dp", "sc"): {
        "finalidade": (
            "A Diretoria de Pessoal, órgão de direção setorial, incumbe-se de planejar, "
            "coordenar, fiscalizar, controlar e executar a política de pessoal da Instituição"
        ),
        "competencias": [
            "controlar todas as atividades relacionadas com a vida funcional do pessoal "
            "militar e civil da Corporação, mantendo registros individuais",
            "promover a seleção para o ingresso no CBMSC e para admissão de pessoal civil, "
            "bem como o serviço de identificação",
            "executar as atividades relativas ao pagamento, alterações e demais encargos "
            "relativos ao pessoal ativo, inativo, pensionista e civil",
            "executar as atividades pertinentes à documentação do pessoal do CBMSC",
            "desenvolver os planos e baixar as ordens decorrentes das diretrizes da política "
            "de pessoal da Corporação",
            "propor a movimentação de Oficiais ao Comandante-Geral, e a de Praças ao "
            "Subcomandante-Geral",
            "preparar os atos de movimentação, classificação e nomeação de Oficiais",
            "preparar os atos de movimentação, classificação e designação de Praças e Civis",
            "manter ligação através do Comandante-Geral com os órgãos do Exército Brasileiro, "
            "relacionados com o controle do pessoal bombeiro militar",
            "estudar e instruir os processos administrativos e submetê-los à consideração do "
            "Chefe do Estado-Maior Geral em que lhe extrapolarem à competência",
            "manter o controle do pessoal agregado, excluído e licenciado",
            "atualizar a cada promoção os Almanaques de Oficiais, Subtenentes, Sargentos, "
            "Cabos e Soldados",
            "elaborar a documentação da Comissão de Promoção de Oficiais e Comissão de "
            "Promoção de Praças",
            "elaborar os processos de concessão de medalhas",
            "coordenar e controlar a execução do plano de férias da Corporação",
            "coletar dados e realizar inspeção de caráter setorial, visando à elaboração de "
            "estudos e propostas de medidas a serem submetidas ao Chefe do Estado-Maior Geral, "
            "para a melhoria e aperfeiçoamento do sistema de administração de pessoal",
            "elaborar estatísticas e relatórios das atividades da Diretoria",
            "manter e operacionalizar o funcionamento das comissões permanentes e de mérito",
            "planejar, orientar, coordenar, controlar e fiscalizar as atividades de saúde "
            "ocupacional, segurança do trabalho, assistência médica, odontológica e psicológica "
            "do pessoal do CBMSC e de seus dependentes",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 34",
        "organName": "Diretoria de Pessoal", "abbr": "DP",
    },
    ("cg", "sc"): {
        "finalidade": "",
        "competencias": [
            "concessão de medalha, condecoração e comenda",
            "movimentação de Oficial",
            "desenvolvimento funcional das Praças pela progressão por antiguidade e por merecimento",
            "assinatura de convênios com municípios, relativos à prestação de serviços de "
            "bombeiro militar e outras atividades consideradas por LEI de competência do CBMSC",
            "agregação e reversão de Praças e Oficiais do CBMSC",
            "exclusão do serviço ativo das Praças",
            "convocação e dispensa de Oficial da Reserva Remunerada do CBMSC para compor "
            "Conselho Especial de Justiça ou Conselho de Justificação, ambos encarregados de "
            "inquérito policial-militar, ou para outros procedimentos administrativos na falta "
            "de oficial da ativa em situação hierárquica compatível com a do oficial envolvido",
            "assinatura de termos de cooperação técnica e convênios com órgãos cujo objeto "
            "seja de interesse da Corporação",
            "designação e respectiva dispensa dos servidores inativos ao Corpo Temporário de "
            "Inativos da Segurança Pública (CTISP), após autorização do Grupo Gestor de Governo (GGG)",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 14",
        "organName": "Comando-Geral", "abbr": "CmdoG",
    },
    ("dp", "go"): {
        "finalidade": "",
        "competencias": [
            "planejar, controlar e executar as atividades relacionadas com pessoal",
            "promover as atividades inerentes ao pagamento de militares, civis e fornecedores",
            "praticar atos inerentes à execução financeira e contábil",
            "elaborar normas internas sobre gestão de pessoal e financeira",
            "planejar e fiscalizar as atividades relacionadas a segurança e medicina do trabalho",
            "elaborar boletins gerais",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 26",
        "organName": "Comando de Gestão e Finanças", "abbr": "",
    },
    ("cg", "go"): {
        "finalidade": (
            "O órgão de direção geral, representado pelo Comando Geral, é encarregado do "
            "planejamento e organização geral da Corporação, visando ao emprego estratégico "
            "de pessoal e material no âmbito da Instituição, cabendo-lhe ainda a fiscalização "
            "e o controle dos órgãos de direção setorial, de apoio e execução"
        ),
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 9",
        "organName": "Comando Geral", "abbr": "",
    },

    # =====================================================================
    # Lote 1 — AC, AL, AM, AP, BA (camada LOB /comparar, 2026-06-28)
    # =====================================================================

    # --- Acre (CBMAC) — Lei nº 2.009/2008 (alt. Lei nº 4.428/2024) ---
    # LOB enxuta/estrutural: descreve poucos órgãos por finalidade; Art. 22 (red.
    # Lei 3.105/2015) remete competências/atribuições dos demais órgãos a instruções
    # normativas do comandante-geral. (cg) usa a atribuição do comandante-geral (cargo).
    ("cg", "ac"): {
        "finalidade": (
            "Compete ao comandante-geral da corporação, dentre outras atribuições, "
            "planejar, coordenar, fiscalizar, controlar e orientar todas as atividades do "
            "CBMAC e centralizar o planejamento administrativo e a programação orçamentária, "
            "podendo delegar estas últimas"
        ),
        "competencias": [],
        "source": "cf. CBMAC, LOB (Lei nº 2.009/2008), Art. 6º",
        "organName": "Comando Geral", "abbr": "",
    },
    ("assessorias", "ac"): {
        "finalidade": (
            "As assessorias do comando geral destinam-se a apoiar o comandante-geral da "
            "corporação em assuntos especializados, podendo ser preenchidas por pessoal civil"
        ),
        "competencias": [],
        "source": "cf. CBMAC, LOB (Lei nº 2.009/2008), Art. 10",
        "organName": "Assessorias do Comando Geral", "abbr": "",
    },
    ("ag", "ac"): {
        "finalidade": (
            "À ajudância geral compete, dentre outras atribuições, a administração, a "
            "segurança e os serviços gerais, dando suporte e apoio em efetivo aos órgãos "
            "sediados no quartel do comando geral"
        ),
        "competencias": [],
        "source": "cf. CBMAC, LOB (Lei nº 2.009/2008), Art. 11",
        "organName": "Ajudância Geral", "abbr": "",
    },
    ("corregedoria", "ac"): {
        "finalidade": (
            "A corregedoria do CBMAC é o órgão responsável pelo sistema administrativo "
            "disciplinar do CBMAC e dos procedimentos de polícia judiciária militar e todos "
            "os seus atos serão validados pelo subcomandante da corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAC, LOB (Lei nº 2.009/2008), Art. 8º",
        "organName": "Corregedoria do CBMAC", "abbr": "",
    },

    # --- Alagoas (CBMAL) — Lei nº 7.444/2012 ---
    ("cg", "al"): {
        "finalidade": (
            "O Comando Geral da Corporação compete ao Comandante Geral do Corpo de Bombeiros "
            "Militar do Estado de Alagoas, responsável pelo comando e a administração da "
            "instituição, bem como a coordenação geral das ações de Defesa Civil no Estado de "
            "Alagoas"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 6º",
        "organName": "Comando Geral", "abbr": "",
    },
    ("gab-cg", "al"): {
        "finalidade": (
            "Ao Gabinete do Comandante Geral compete as funções de assistência e "
            "assessoramento direto ao Comandante Geral na prática de atos de gestão e nos "
            "assuntos que escapem às atribuições normais e específicas dos demais órgãos de "
            "direção"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 9º",
        "organName": "Gabinete do Comando Geral", "abbr": "",
    },
    ("condeg", "al"): {
        "finalidade": (
            "O Conselho de Políticas Estratégicas é um colegiado encarregado de assessorar ao "
            "Comandante Geral na formulação e avaliação de políticas estratégicas e na fixação "
            "de diretrizes de gerenciamento administrativo e de emprego do Corpo de Bombeiros "
            "Militar para o cumprimento de suas missões"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 11",
        "organName": "Conselho de Políticas Estratégicas", "abbr": "",
    },
    ("depdec", "al"): {
        "finalidade": (
            "A Coordenadoria Estadual de Defesa Civil é órgão de coordenação central do "
            "Sistema Estadual de Defesa Civil, competindo-lhe o estudo, o planejamento, a "
            "orientação técnica, a coordenação, a supervisão, a execução, o controle e a "
            "avaliação das ações de defesa civil no Estado de Alagoas, observando o disposto "
            "na Lei nº 6.171, de 31 de julho de 2000"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 12",
        "organName": "Coordenadoria Estadual de Defesa Civil", "abbr": "",
    },
    ("corregedoria", "al"): {
        "finalidade": (
            "A Corregedoria Geral do Corpo de Bombeiros Militar é o órgão de direção "
            "encarregado da orientação, fiscalização e correção dos procedimentos relativos à "
            "apuração das transgressões disciplinares e das infrações penais militares dos "
            "Bombeiros Militares, promovendo-lhes, ainda, a responsabilidade funcional e "
            "disciplinar"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 13",
        "organName": "Corregedoria Geral", "abbr": "",
    },
    ("dp", "al"): {
        "finalidade": (
            "A Diretoria de Recursos Humanos é o órgão central do sistema de recursos humanos "
            "do Corpo de Bombeiros Militar, competindo-lhe o estudo, o planejamento, a "
            "orientação normativa, a coordenação, a supervisão, o controle e a execução das "
            "atividades relativas à gestão de pessoal e desenvolvimento de recursos humanos da "
            "Corporação, de acordo com as diretrizes da Secretaria de Estado da Gestão "
            "Pública - SEGESP"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 15",
        "organName": "Diretoria de Recursos Humanos", "abbr": "DRH",
    },
    ("dlog", "al"): {
        "finalidade": (
            "A Diretoria de Material e Patrimônio é o órgão central do sistema logístico do "
            "Corpo de Bombeiros Militar, competindo-lhe o estudo, o planejamento, a orientação "
            "normativa, a coordenação, a supervisão, o controle e a execução das atividades "
            "relativas à gestão do material e patrimônio da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 16",
        "organName": "Diretoria de Material e Patrimônio", "abbr": "",
    },
    ("dpof", "al"): {
        "finalidade": (
            "A Diretoria de Finanças é o órgão central do sistema de administração financeira "
            "do Corpo de Bombeiros Militar, competindo-lhe o estudo, o planejamento, a "
            "orientação normativa, a coordenação, a supervisão, o controle e a execução das "
            "atividades relativas à gestão financeira, ao planejamento e execução "
            "orçamentária, à contabilidade e auditoria"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 17",
        "organName": "Diretoria de Finanças", "abbr": "",
    },
    ("cot", "al"): {
        "finalidade": (
            "A Diretoria de Atividades Técnicas é o órgão central do sistema de engenharia e "
            "segurança do Corpo de Bombeiros Militar, competindo-lhe o estudo, a análise, o "
            "planejamento, a orientação técnica, a execução, o controle e a fiscalização das "
            "atividades relativas à segurança contra incêndio e pânico e ao cumprimento das "
            "disposições legais sobre o assunto, no âmbito do Estado de Alagoas"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 18",
        "organName": "Diretoria de Atividades Técnicas", "abbr": "",
    },
    ("dpo", "al"): {
        "finalidade": (
            "A Diretoria de Planejamento e Orçamento é o órgão central do sistema de "
            "Planejamento Estratégico e Orçamentário do Corpo de Bombeiros Militar, "
            "competindo-lhe a coordenação do planejamento, a orientação técnica, o "
            "monitoramento, o controle e a fiscalização das atividades relativas ao "
            "planejamento estratégico, bem como a elaboração e execução do orçamento da "
            "Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 19",
        "organName": "Diretoria de Planejamento e Orçamento", "abbr": "",
    },
    ("deei", "al"): {
        "finalidade": (
            "A Diretoria de Ensino é o órgão de apoio do sistema de ensino da Corporação, "
            "incumbindo-lhe, o estudo, o planejamento, a supervisão e o controle das "
            "atividades de ensino e capacitação profissional da Instituição"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 20",
        "organName": "Diretoria de Ensino", "abbr": "",
    },
    ("ag", "al"): {
        "finalidade": (
            "A Secretaria Geral é o órgão de direção encarregado da administração do Quartel "
            "do Comando Geral, considerado como Organização Bombeiro Militar, bem como do "
            "expediente, da execução dos trabalhos de secretaria, incluindo a correspondência, "
            "correio, redação e impressão do boletim diário, do protocolo e arquivo geral e "
            "biblioteca, do apoio em pessoal aos órgãos que compõem o Comando Geral, dos "
            "serviços gerais, da banda de música e da segurança do Quartel do Comando Geral"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 21",
        "organName": "Secretaria Geral", "abbr": "",
    },
    ("cinf", "al"): {
        "finalidade": (
            "O Centro de Tecnologia em Informática e Informação é o órgão que gerencia e "
            "administra os recursos tecnológicos e computacionais de geração e uso da "
            "informação como também todo o parque de informática do Corpo de Bombeiros "
            "Militar, subordinado ao Subcomandante Geral, encarregado de desenvolver e manter "
            "sistemas informatizados, para as áreas administrativa, operacional, internet e "
            "intranet da Corporação, dar suporte tecnológico e apoio ao usuário, provendo "
            "informações de planejamento e avaliação da gestão pública"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 25",
        "organName": "Centro de Tecnologia de Informática e Informação", "abbr": "",
    },
    ("dsap", "al"): {
        "finalidade": (
            "O Centro de Assistência é o órgão de apoio do sistema de recursos humanos, "
            "subordinado ao Subcomandante Geral, incumbido do suporte ao sistema de "
            "atendimento pré-hospitalar, do estudo, planejamento, a supervisão, a execução e o "
            "controle das atividades de assistência médica, odontológica, farmacêutica, "
            "sanitária, religiosa e de assistência social aos Bombeiros Militares e seus "
            "dependentes, na forma da legislação em vigor"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 26",
        "organName": "Centro de Assistência", "abbr": "",
    },
    ("crbm", "al"): {
        "finalidade": (
            "Comando Operacional de Bombeiros é a denominação genérica dada a Organização "
            "Bombeiro-Militar de mais alto escalão do sistema operacional, subordinado ao "
            "Subcomandante Geral, que tem a seu cargo o planejamento estratégico, a "
            "coordenação e o emprego das Unidades Operacionais da Corporação que lhe forem "
            "subordinadas, com a finalidade de executar as missões de prevenção e extinção de "
            "incêndios, de resgate, busca e salvamento, de atendimento aos traumas e "
            "emergências pré-hospitalares e de defesa civil, além de outras, em uma "
            "determinada área operacional"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 30",
        "organName": "Comando Operacional de Bombeiros", "abbr": "",
    },
    ("gbm", "al"): {
        "finalidade": (
            "Os Grupamentos de Bombeiros Militar, subordinados aos Comandos Operacionais de "
            "Área, têm a seu cargo, dentro de sua área de atuação operacional, as missões de "
            "prevenção e extinção de incêndios, busca e salvamento, atendimento "
            "pré-hospitalar, emergências com produtos perigosos, bem como disporão de uma "
            "Seção de Atividades Técnicas para a execução dos trabalhos de análise de "
            "projetos, vistorias e pareceres técnicos em edificações e locais de risco, além "
            "de contar com uma Seção de Defesa Civil"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 34",
        "organName": "Grupamento de Bombeiros Militar", "abbr": "GBM",
    },
    ("bbs", "al"): {
        "finalidade": (
            "O Grupamento de Busca e Salvamento tem a seu cargo, dentro de uma determinada "
            "área de atuação operacional, as missões de busca, salvamento em altura e "
            "terrestre, resgate e outras voltadas para as missões de salvamento terrestre"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 38",
        "organName": "Grupamento de Busca e Salvamento", "abbr": "GBS",
    },
    ("bifea", "al"): {
        "finalidade": (
            "O Grupamento de Proteção Ambiental tem a seu cargo, dentro de uma determinada "
            "área de atuação operacional, as missões de prevenção, combate a incêndios "
            "florestais, preservação de áreas ambientais, seus recursos hídricos, salvamento "
            "de animais silvestres, dentre outras voltadas para a proteção e preservação da "
            "fauna e da flora"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 39",
        "organName": "Grupamento de Proteção Ambiental", "abbr": "GPA",
    },
    ("boa", "al"): {
        "finalidade": (
            "O Grupamento de Operações Aéreas tem a seu cargo, dentro de uma determinada área "
            "de atuação operacional, as missões, por meio aéreo, de socorro de urgência, "
            "extricação de presos em ferragens, combate a incêndios florestais, salvamentos e "
            "resgate, dentre outras atividades aéreas correlatas, além de dispor de uma "
            "assessoria de segurança de voo"
        ),
        "competencias": [],
        "source": "cf. CBMAL, LOB (Lei nº 7.444/2012), Art. 40",
        "organName": "Grupamento de Operações Aéreas", "abbr": "GOA",
    },

    # --- Amazonas (CBMAM) — Lei nº 2.538/1999 ---
    ("cg", "am"): {
        "finalidade": (
            "O Comandante Geral do Corpo de Bombeiros Militar do Estado do Amazonas é "
            "responsável pelo comando, administração e emprego da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 9º",
        "organName": "Comando Geral", "abbr": "",
    },
    ("gab-cg", "am"): {
        "finalidade": (
            "O Gabinete do Comando-Geral tem a seu cargo as funções de assistência e "
            "assessoramento direto ao Comandante Geral nos assuntos que refogem às atribuições "
            "normais e específicas dos demais órgãos de direção"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 16",
        "organName": "Gabinete do Comando-Geral", "abbr": "",
    },
    ("depdec", "am"): {
        "finalidade": (
            "A Coordenadoria Estadual de Defesa Civil (CEDEC) órgão de direção geral, "
            "centraliza o Sistema Estadual de Defesa Civil e tem por finalidade estabelecer "
            "normas e o exercício das atividades de integrar, planejar, organizar, coordenar e "
            "supervisionar a execução das medidas preventivas de socorro, de assistência e de "
            "recuperação, considerando os efeitos produzidos por fatos adversos de qualquer "
            "natureza e nas situações de emergência ou estado de calamidade pública"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 14",
        "organName": "Coordenadoria Estadual de Defesa Civil", "abbr": "CEDEC",
    },
    ("condeg", "am"): {
        "finalidade": (
            "O Conselho Superior de Políticas Estratégicas (CSPE), constituído pelo Comandante "
            "Geral, Subcomandante Geral, Comandantes de Bombeiros da Capital e do Interior e "
            "Diretores Setoriais, reunir-se-á, eventualmente, por convocação do Comandante "
            "Geral, ou em datas por ele prefixadas e, terá suas atribuições definidas no "
            "Regimento Interno da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 15",
        "organName": "Conselho Superior de Políticas Estratégicas", "abbr": "CSPE",
    },
    ("ag", "am"): {
        "finalidade": (
            "A Ajudância Geral (AG) é o órgão responsável pelas funções administrativas do "
            "Comando Geral"
        ),
        "competencias": [
            "trabalhos de secretaria, inclusive correspondências, correios, protocolo geral, "
            "arquivo geral e boletim geral",
            "serviço de embarque da Corporação",
            "apoio de pessoal auxiliar (militar e civil) aos órgãos do Comando Geral",
            "serviços gerais",
            "segurança do Quartel do Comando Geral",
        ],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 18",
        "organName": "Ajudância Geral", "abbr": "AG",
    },
    ("dp", "am"): {
        "finalidade": (
            "A Diretoria de Recursos Humanos (DRH) é o órgão de direção setorial responsável "
            "pelo planejamento, controle e fiscalização das atividades relacionadas com "
            "políticas de pessoal, da admissão, da capacitação técnica, da assistência "
            "psicológica, social, jurídica e religiosa, pela remuneração do pessoal e pela "
            "prevenção de acidentes no trabalho"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 21",
        "organName": "Diretoria de Recursos Humanos", "abbr": "DRH",
    },
    ("dpof", "am"): {
        "finalidade": (
            "A Diretoria de Finanças (DF) é o órgão de direção setorial responsável pelas "
            "atividades específicas da gestão orçamentária e financeira, supervisão destas "
            "junto aos demais órgãos da Corporação, controle de repasse de recursos "
            "orçamentários e captação de recursos financeiros, de acordo com o planejamento "
            "estabelecido"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 23",
        "organName": "Diretoria de Finanças", "abbr": "DF",
    },
    ("dlog", "am"): {
        "finalidade": (
            "A Diretoria de Logística (DL) é o órgão de direção setorial responsável pelo "
            "planejamento, coordenação, fiscalização e controle das atividades de suprimento e "
            "material da Corporação, além da elaboração de convênios e atividades de saúde"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 25",
        "organName": "Diretoria de Logística", "abbr": "DL",
    },
    ("deei", "am"): {
        "finalidade": (
            "A Diretoria de Ensino, Instrução, Pesquisa e Operações (DEIPO) é o órgão de "
            "direção setorial responsável pela coordenação, fiscalização, controle das "
            "atividades de ensino, instrução, pesquisa e pelo planejamento operacional da "
            "Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 27",
        "organName": "Diretoria de Ensino, Instrução, Pesquisa e Operações", "abbr": "DEIPO",
    },
    ("cot", "am"): {
        "finalidade": (
            "A Diretoria de Serviços Técnicos (DST) é o órgão de direção setorial incumbido de "
            "estudar, analisar, planejar, exigir, fiscalizar as atividades atinentes à "
            "prevenção e segurança contra incêndios e pânico, além de proceder testes, exames "
            "de plantas, perícias de incêndio e explosão, a realizar vistorias e emitir "
            "pareceres e supervisionar a instalação de hidrantes na rede pública"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 29",
        "organName": "Diretoria de Serviços Técnicos", "abbr": "DST",
    },
    ("cinf", "am"): {
        "finalidade": (
            "O Centro de Informática (CInf), órgão de apoio, subordinado diretamente à "
            "Diretoria de Ensino, Instrução, Pesquisa e Operações (DEIPO), destina-se a "
            "realizar programas e sistemas para a otimização das áreas administrativas e "
            "operacionais da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 37",
        "organName": "Centro de Informática", "abbr": "CInf",
    },
    ("crbm", "am"): {
        "finalidade": (
            "O Comando de Bombeiros da Capital (CBC) e o Comando de Bombeiros do Interior "
            "(CBI), órgãos de execução, subordinados ao Subcomandante Geral, destinam-se ao "
            "planejamento estratégico, à coordenação, à fiscalização e ao emprego das Unidades "
            "e Sub-unidades que lhe forem subordinadas, com a finalidade de executar "
            "atividades de prevenção, combate a incêndio, busca e salvamento, atendimento de "
            "socorros de emergência e defesa civil, além de outras atividades previstas em lei"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 45",
        "organName": "Comando de Bombeiros da Capital e do Interior", "abbr": "CBC/CBI",
    },
    ("bbm", "am"): {
        "finalidade": (
            "O Batalhão de Incêndio (BI), unidade operacional, órgão de execução, subordinado "
            "ao Comando de Bombeiros da Capital (CBC) ou Comando de Bombeiros do Interior "
            "(CBI), destina-se à coordenação, ao controle, à fiscalização e à execução de "
            "atividade operacional e administrativa em sua área de atuação"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 48",
        "organName": "Batalhão de Incêndio", "abbr": "BI",
    },
    ("bifea", "am"): {
        "finalidade": (
            "O Batalhão de Incêndio Florestal e Meio Ambiente (BIF/MA), unidade operacional, "
            "órgão de execução, subordinado ao Comando Operacional do Interior, destina-se à "
            "prevenção e combate a incêndio florestal e queimadas e socorro ao meio ambiente, "
            "em conformidade com a lei"
        ),
        "competencias": [],
        "source": "cf. CBMAM, LOB (Lei nº 2.538/1999), Art. 52",
        "organName": "Batalhão de Incêndio Florestal e Meio Ambiente", "abbr": "BIF/MA",
    },

    # --- Amapá (CBMAP) — Lei Complementar nº 180/2026 ---
    # LOB nova e enxuta: Art. 6º remete a estrutura/atribuições de cada órgão a decreto
    # ("definidas por ato do Governador"). Só descreve órgãos por CATEGORIA (§§ do Art. 6º);
    # as Diretorias/Centros não têm finalidade individual. (cg) usa a finalidade da
    # direção-geral; (corregedoria) usa a finalidade dos órgãos de correição (§5º).
    ("cg", "ap"): {
        "finalidade": (
            "os órgãos de direção-geral, responsáveis pela direção superior, planejamento "
            "estratégico e administração geral da Instituição, compostos pelo Gabinete do "
            "Comandante-Geral, Gabinete do Subcomandante-Geral, Comitê de Desenvolvimento "
            "Organizacional, Comando Operacional e Fundo de Reequipamento do Corpo de Bombeiros"
        ),
        "competencias": [],
        "source": "cf. CBMAP, LOB (LC nº 180/2026), Art. 6º, § 1º, I",
        "organName": "Órgãos de Direção-Geral", "abbr": "",
    },
    ("corregedoria", "ap"): {
        "finalidade": (
            "Os órgãos de correição, com atuação desconcentrada, destinam-se a exercer as "
            "funções de Corregedoria-Geral, mediante regulamentação de procedimentos internos, "
            "para a prevenção, fiscalização e apuração dos desvios de conduta em atos "
            "disciplinares e penais militares, a promoção da qualidade e eficiência do serviço "
            "de segurança pública e a instrumentalização da Justiça Militar, bem como a "
            "acompanhar o cumprimento de quaisquer medidas cautelares restritivas de direitos "
            "e mandados de prisão judicialmente deferidos em desfavor de militares dentro da "
            "instituição, sem suprimir a responsabilidade do poder hierárquico e disciplinar "
            "de outras autoridades"
        ),
        "competencias": [],
        "source": "cf. CBMAP, LOB (LC nº 180/2026), Art. 6º, § 5º",
        "organName": "Órgãos de Correição (Corregedoria-Geral)", "abbr": "",
    },

    # --- Bahia (CBMBA) — Lei nº 14.572/2023 ---
    # LOB moderna que dá finalidade ("tem por finalidade") a quase todos os órgãos; Art. 7º
    # §2º remete a estrutura interna e competências de detalhe a Regimento (Decreto).
    ("cg", "ba"): {
        "finalidade": (
            "O Comando-Geral é o órgão diretivo superior e estratégico que tem por finalidade "
            "planejar, dirigir, executar, avaliar, deliberar e controlar as atividades do CBMBA"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 11",
        "organName": "Comando-Geral", "abbr": "",
    },
    ("gab-cg", "ba"): {
        "finalidade": (
            "O Gabinete do Comando Geral, integrante do Comando-Geral, tem por finalidade "
            "prestar assistência ao Comandante-Geral em suas atribuições técnicas e "
            "administrativas e nas relações de interesse do CBMBA com órgãos e instituições "
            "dos Poderes Executivo, Legislativo e Judiciário, em âmbito Federal, Estadual e "
            "Municipal, do Ministério Público, dos Tribunais de Contas e de Organismos "
            "Internacionais"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 12",
        "organName": "Gabinete do Comando Geral", "abbr": "",
    },
    ("condeg", "ba"): {
        "finalidade": (
            "O Conselho do Corpo de Bombeiros Militar, órgão consultivo e propositivo, "
            "convocado e presidido pelo Comandante-Geral, é constituído pelos Coronéis da "
            "ativa, quando no exercício dos cargos privativos do posto de coronel previstos no "
            "quadro de organização do CBMBA, tendo como finalidade a análise e discussão sobre "
            "assuntos de relevante interesse da Corporação, ressalvada a competência do Alto "
            "Comando"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 10",
        "organName": "Conselho do Corpo de Bombeiros Militar", "abbr": "",
    },
    ("dpo", "ba"): {
        "finalidade": (
            "O Comando de Operações de Bombeiros Militar tem por finalidade assessorar o "
            "Comandante-Geral e o Subcomandante-Geral, planejar, coordenar, executar, avaliar "
            "e controlar as atividades operacionais de bombeiros militares, de proteção e "
            "defesa civil, executadas pelos Comandos Regionais e pelas Unidades Operacionais, "
            "no que concerne à proteção das pessoas e dos bens públicos e privados"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 16",
        "organName": "Comando de Operações de Bombeiros Militar", "abbr": "COBM",
    },
    ("boa", "ba"): {
        "finalidade": (
            "O Centro de Gestão do Vetor Aéreo, integrante do Comando de Operações de "
            "Bombeiros Militar, tem por finalidade a gestão e execução do apoio do vetor aéreo "
            "às atividades de bombeiros militares e defesa civil"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 17",
        "organName": "Centro de Gestão do Vetor Aéreo", "abbr": "",
    },
    ("cot", "ba"): {
        "finalidade": (
            "O Comando de Segurança Contra Incêndio tem por finalidade planejar, avaliar e "
            "efetuar pesquisas, perícias de incêndios, vistorias, análises de projetos de "
            "proteção contra incêndios e pânico na sua área específica de atuação, emitindo os "
            "respectivos laudos, pareceres e autos de vistorias técnicas"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 18",
        "organName": "Comando de Segurança Contra Incêndio", "abbr": "",
    },
    ("cint", "ba"): {
        "finalidade": (
            "A Coordenadoria de Inteligência tem por finalidade planejar, coordenar, executar, "
            "fiscalizar, controlar, articular, supervisionar e gerenciar as atividades de "
            "inteligência bombeiro militar, no âmbito do Sistema de Inteligência do Corpo de "
            "Bombeiros Militar - SINBOM, dentro do território baiano, e assessorar o Alto "
            "Comando da Corporação nos assuntos de cunho estratégico, tático e operacional que "
            "lhes forem confiados, além de se inter-relacionar com os demais órgãos estaduais "
            "de inteligência e do Sistema Brasileiro de Inteligência - SISBIN"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 19",
        "organName": "Coordenadoria de Inteligência", "abbr": "",
    },
    ("corregedoria", "ba"): {
        "finalidade": (
            "A Corregedoria do Corpo de Bombeiros Militar da Bahia tem por finalidade assistir "
            "o Comandante-Geral e o Subcomandante-Geral do Corpo de Bombeiros Militar da Bahia "
            "no desempenho de suas atribuições constitucionais, políticas e administrativas, "
            "realizar a atividade correcional, zelando pela justiça e disciplina dos "
            "integrantes da Corporação e gerenciar as atividades dos segmentos de correição "
            "descentralizados do CBMBA"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 20",
        "organName": "Corregedoria do Corpo de Bombeiros Militar da Bahia", "abbr": "",
    },
    ("dpof", "ba"): {
        "finalidade": (
            "O Departamento de Planejamento tem por finalidade elaborar o planejamento das "
            "políticas públicas e estratégias institucionais, orientar e executar a "
            "programação orçamentária, consolidar os planos, programas e projetos e realizar o "
            "acompanhamento e a avaliação das ações governamentais, no âmbito do CBMBA"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 21",
        "organName": "Departamento de Planejamento", "abbr": "",
    },
    ("dp", "ba"): {
        "finalidade": (
            "O Departamento de Pessoal tem por finalidade planejar, organizar, coordenar e "
            "controlar as atividades de pessoal do CBMBA"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 22",
        "organName": "Departamento de Pessoal", "abbr": "",
    },
    ("dlog", "ba"): {
        "finalidade": (
            "O Departamento de Apoio Logístico tem por finalidade planejar, coordenar, "
            "controlar e executar as atividades de logística e de patrimônio do CBMBA"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 23",
        "organName": "Departamento de Apoio Logístico", "abbr": "",
    },
    ("cinf", "ba"): {
        "finalidade": (
            "O Departamento de Modernização e Tecnologia tem por finalidade planejar, "
            "coordenar, executar e controlar as atividades de tecnologia da informação e "
            "telecomunicações, promovendo a elevação da qualidade dos serviços e das "
            "atividades do CBMBA, em estreita articulação com os órgãos estaduais de "
            "tecnologia da informação e telecomunicações, e, por intermédio de convênios, com "
            "as demais esferas de governo"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 25",
        "organName": "Departamento de Modernização e Tecnologia", "abbr": "",
    },
    ("deei", "ba"): {
        "finalidade": (
            "O Instituto Militar de Ensino Superior de Bombeiros - IMESB, instituição de "
            "ensino superior do CBMBA, tem por finalidade planejar, organizar, dirigir, "
            "controlar, avaliar e fiscalizar as atividades de ensino, instrução, extensão e "
            "pesquisa do CBMBA, emitindo diretrizes educacionais para as organizações "
            "tecnicamente subordinadas"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 28",
        "organName": "Instituto Militar de Ensino Superior de Bombeiros", "abbr": "IMESB",
    },
    ("dsap", "ba"): {
        "finalidade": (
            "A Coordenadoria de Saúde tem por finalidade planejar, coordenar, controlar e "
            "executar as atividades de promoção, prevenção, tratamentos médico, psicológico e "
            "odontológico, reabilitação e recuperação dos agravos à saúde dos integrantes do "
            "CBMBA e dos seus dependentes"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 32",
        "organName": "Coordenadoria de Saúde", "abbr": "",
    },
    ("crbm", "ba"): {
        "finalidade": (
            "Os Comandos Regionais de Bombeiros Militar, subordinados ao COBM, têm por "
            "finalidade planejar, coordenar, controlar, executar e avaliar as atividades "
            "operacionais de bombeiros militares de proteção e defesa civil nas regiões sob "
            "sua responsabilidade, bem como supervisionar as atividades realizadas pelas "
            "unidades operacionais respectivas, no que concerne à eficiência nas missões de "
            "bombeiro militar"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 33",
        "organName": "Comandos Regionais de Bombeiros Militar", "abbr": "",
    },
    ("bbm", "ba"): {
        "finalidade": (
            "Os Batalhões de Bombeiros Militar subordinados aos seus respectivos Comandos "
            "Regionais têm por finalidade a execução das missões de bombeiro militar, e terão "
            "atuação em todo o Estado da Bahia ou em região definida em regulamento"
        ),
        "competencias": [],
        "source": "cf. CBMBA, LOB (Lei nº 14.572/2023), Art. 34",
        "organName": "Batalhões de Bombeiros Militar", "abbr": "",
    },

    # =====================================================================
    # Lote 2 — CE, DF, ES, MA, MG + completa GO (camada LOB /comparar, 2026-06-28)
    # =====================================================================

    # --- Ceará (CBMCE) — Lei nº 13.438/2004 ---
    # LOB por "competência": dá finalidade (caput) e, em vários órgãos, incisos. (cg) usa a
    # atribuição do Comandante Geral (cargo); a LOB não dá finalidade ao Comando como órgão.
    ("cg", "ce"): {
        "finalidade": (
            "O Comandante Geral, responsável pelo comando e administração da Corporação, é "
            "cargo privativo de Oficial da ativa, do quadro de Oficiais Combatentes do Corpo "
            "de Bombeiros, dentre os Oficiais no Posto de Coronel, nomeado pelo Governador do "
            "Estado"
        ),
        "competencias": [],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 8º",
        "organName": "Comandante Geral", "abbr": "",
    },
    ("condeg", "ce"): {
        "finalidade": (
            "O Conselho Consultivo é o Órgão Colegiado de natureza consultiva com a finalidade "
            "de assessorar o Comandante Geral em assuntos de alta relevância no cumprimento de "
            "suas missões"
        ),
        "competencias": [],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 6º",
        "organName": "Conselho Consultivo", "abbr": "",
    },
    ("ag", "ce"): {
        "finalidade": (
            "A Secretaria Executiva tem por finalidade coordenar e supervisionar as atividades "
            "do Gabinete, bem como acompanhar os trabalhos das Comissões e Assessorias, "
            "competindo-lhe"
        ),
        "competencias": [
            "assessorar o Comandante Geral nos assuntos de controle interno, identificação e "
            "avaliação dos pontos críticos que possam ameaçar a comunidade cearense",
            "produzir informações estratégicas com vistas ao preparo e emprego do Corpo de "
            "Bombeiros Militar",
            "dar suporte ao Comando Geral nos assuntos de relações públicas envolvendo o "
            "público interno e externo",
            "coordenar e supervisionar assuntos relacionados com a imprensa em geral",
            "assessorar o Comando Geral na doutrina e legislação da Corporação",
            "coordenar as atividades relacionadas com a elaboração de leis, regulamentos e "
            "instruções normativas da Corporação",
            "desempenhar as funções de apoio administrativo, comando de serviços, expediente e "
            "trabalho de secretaria do Comando Geral, incluindo correspondência, protocolo "
            "geral e boletim diário",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 12",
        "organName": "Secretaria Executiva", "abbr": "",
    },
    ("assessorias", "ce"): {
        "finalidade": (
            "A Assessoria Jurídica é o órgão incumbido de assessorar o Comandante Geral nos "
            "diversos aspectos jurídicos da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 13",
        "organName": "Assessoria Jurídica", "abbr": "",
    },
    ("cat", "ce"): {
        "finalidade": (
            "A Coordenadoria de Atividades Técnicas é o Órgão de Execução Programática "
            "responsável pelo controle da observância dos requisitos técnicos contra incêndios "
            "e de projetos de edificações antes ou depois de sua liberação ao uso, "
            "competindo-lhe"
        ),
        "competencias": [
            "gerenciar o sistema de informações no que diz respeito à análise, cadastro e "
            "controle de dados",
            "desenvolver pesquisa científica e avaliar o desempenho operacional da Corporação",
            "analisar projetos de edificações, vistorias e pareceres técnicos",
            "controlar, manter e manobrar hidrantes",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 17",
        "organName": "Coordenadoria de Atividades Técnicas", "abbr": "",
    },
    ("dpo", "ce"): {
        "finalidade": "A Coordenadoria Operacional é responsável pela execução das operações bombeirísticas",
        "competencias": [],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 18",
        "organName": "Coordenadoria Operacional", "abbr": "",
    },
    ("crbm", "ce"): {
        "finalidade": (
            "O Núcleo de Bombeiro Metropolitano é responsável pela execução das operações de "
            "bombeiro militar na região metropolitana, competindo-lhe ainda o comando, controle "
            "e fiscalização das missões que lhe são atribuídas pelo Comandante Geral da "
            "Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 19",
        "organName": "Núcleo de Bombeiro Metropolitano (e do Interior)", "abbr": "",
    },
    ("depdec", "ce"): {
        "finalidade": (
            "O Núcleo de Defesa Civil do Corpo de Bombeiros é responsável, na fase de socorro, "
            "pelo planejamento, fiscalização, controle e execução e atividades de Defesa Civil, "
            "competindo-lhe"
        ),
        "competencias": [
            "realizar a integração com a Secretaria da Ação Social e a Comunidade a fim de "
            "avaliar as situações de risco e aspectos preventivos",
            "planejar as atividades operacionais de Defesa Civil em parceria com a Secretaria "
            "da Ação Social",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 21",
        "organName": "Núcleo de Defesa Civil", "abbr": "",
    },
    ("bbs", "ce"): {
        "finalidade": (
            "O Núcleo de Busca e Salvamento é a unidade operacional responsável pelo serviço "
            "de busca, salvamento e proteção"
        ),
        "competencias": [],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 22",
        "organName": "Núcleo de Busca e Salvamento", "abbr": "",
    },
    ("dlog", "ce"): {
        "finalidade": (
            "A Célula de Logística é o órgão incumbido da administração e do suprimento de "
            "material de todas as classes, sendo responsável também pela manutenção do "
            "patrimônio móvel e imóvel, manutenção de transportes e equipamentos pesados, "
            "competindo-lhe"
        ),
        "competencias": [
            "gerir a conservação, reforma, ampliação e construção do patrimônio móvel e imóvel "
            "da Corporação",
            "fiscalizar, acompanhar, solicitar e distribuir o material necessário a todas as "
            "unidades da Corporação",
            "supervisionar a manutenção de toda a frota operacional e administrativa da "
            "Corporação",
            "gerenciar as atividades de arquivo, protocolo e controle de pessoal",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 26",
        "organName": "Célula de Logística", "abbr": "",
    },
    ("dpof", "ce"): {
        "finalidade": (
            "O Núcleo Financeiro é responsável pelas atividades financeiras e de contabilidade "
            "da Corporação, competindo-lhe"
        ),
        "competencias": [
            "gerenciar as contas da Corporação, utilizando instrumentos adequados de "
            "acompanhamento e execução orçamentária, objetivando controle financeiro",
            "assegurar o cumprimento dos compromissos decorrentes da execução orçamentária "
            "financeira",
            "intermediar contatos para liberação de recursos e para implantação das alterações "
            "orçamentárias, bem como, pelos pagamentos de contas e do pessoal do Corpo de "
            "Bombeiros",
            "controlar toda captação de recursos da Corporação, e atribuições de planejar, "
            "lançar, acompanhar, fiscalizar, coordenar e controlar as receitas das taxas de "
            "serviços",
            "gerenciar o acompanhamento e planejamento orçamentário e financeiro",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 27",
        "organName": "Núcleo Financeiro", "abbr": "",
    },
    ("dp", "ce"): {
        "finalidade": (
            "A Célula de Gestão e Formação de Pessoas é incumbida do planejamento, controle, "
            "ensino, execução, capacitação e fiscalização das atividades relacionadas ao "
            "pessoal do Corpo de Bombeiros, competindo-lhe"
        ),
        "competencias": [
            "coordenar as atividades de recrutamento, seleção, acompanhamento, controle do "
            "pessoal ativo, inativo e servidores civis, bem como acompanhar as promoções, "
            "classificação e movimentação do pessoal",
            "acompanhar o trabalho do pessoal nos serviços de assistência religiosa e "
            "psicosocial",
            "planejar assuntos pertinentes à instrução e às operações do Corpo de Bombeiros",
            "consolidar projetos, através da coleta de informações, pesquisas e experiências "
            "operacionais, marketing de serviços e recursos humanos",
            "propor as implantações e modificações administrativas, para todos os níveis da "
            "Corporação, de acordo com os preceitos de qualidade total, reengenharia, "
            "racionalização de meios e espaço, no sentido de modernizar, aumentar a "
            "produtividade e a qualidade administrativa operacional",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 28",
        "organName": "Célula de Gestão e Formação de Pessoas", "abbr": "",
    },
    ("deei", "ce"): {
        "finalidade": (
            "O Colégio Militar do Corpo de Bombeiros – CMCB, é responsável pelo sistema de "
            "ensino da Corporação, desempenhando-as pelas seguintes atribuições"
        ),
        "competencias": [
            "orientar a formação integral dos alunos",
            "realizar o enquadramento militar compatível com a idade e a condição de aluno, em "
            "consonância com a Orientação Educacional do Colégio",
            "supervisionar, coordenar e controlar as atividades do Corpo Discente",
            "planejar, programar, executar, controlar, supervisionar e orientar os serviços "
            "administrativos do Colégio",
            "direcionar os objetivos para os métodos e aprendizagem aplicada pelo corpo docente "
            "e acompanhamento do processo ensino-aprendizagem",
            "planejar os assuntos relativos à comunicação social",
            "acompanhar os trabalhos educativos desenvolvidos e os projetos técnicos para o "
            "aprimoramento educacional",
        ],
        "source": "cf. CBMCE, LOB (Lei nº 13.438/2004), Art. 30",
        "organName": "Colégio Militar do Corpo de Bombeiros", "abbr": "CMCB",
    },

    # --- Goiás (CBMGO) — Lei nº 18.305/2013 (completa o Lote inicial; cg/go e dp/go já existem) ---
    # LOB por competências enumeradas (incisos); a finalidade dos Comandos Regionais vem do
    # Art. 21 e seus incisos do Art. 22.
    ("crbm", "go"): {
        "finalidade": (
            "Os órgãos de direção regional, representados pelos Comandos Regionais, são "
            "organizados para a consecução de atividades de gestão operacional, cabendo-lhes a "
            "otimização na aplicação dos recursos operacionais disponíveis nas respectivas "
            "atribuições, conforme diretrizes e ordens definidas pelo órgão de direção geral"
        ),
        "competencias": [
            "exercer a gestão operacional nas respectivas regiões",
            "planejar, controlar e fiscalizar as atividades operacionais desenvolvidas pelas "
            "respectivas unidades de execução, bem como exercer outras missões correlatas",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 21-22",
        "organName": "Comandos Regionais", "abbr": "",
    },
    ("corregedoria", "go"): {
        "finalidade": "",
        "competencias": [
            "assegurar a disciplina funcional, os princípios hierárquicos estruturais "
            "fundamentais e a apuração das infrações penais militares e transgressões "
            "disciplinares",
            "exercer diretamente ou por meio das Organizações Bombeiro Militares as funções de "
            "Polícia Judiciária Militar e de Polícia Administrativa, observada a legislação "
            "vigente",
            "acompanhar a apuração de ilícitos penais e transgressões disciplinares",
            "promover execução, controle, coordenação, orientação e fiscalização de atividade "
            "pertinente à disciplina e execução judiciária",
            "controlar a instauração de inquéritos policiais, sindicâncias, conselhos de "
            "justificação, conselhos de disciplina, autos de prisão em flagrante, inquéritos "
            "técnicos e outros procedimentos administrativos",
            "exercer fiscalização ostensiva quanto ao desempenho funcional, operacional e "
            "administrativo dos integrantes da Corporação",
            "exercer as atividades de ouvidoria no âmbito da Corporação",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 24",
        "organName": "Comando de Correições e Disciplina", "abbr": "",
    },
    ("dlog", "go"): {
        "finalidade": "",
        "competencias": [
            "planejar e controlar as atividades relacionadas às necessidades de suprimento e "
            "manutenção da Corporação, bem como o controle patrimonial, de acordo com premissas "
            "definidas pelo Comando Geral",
            "elaborar normas internas sobre especificações e solicitações de materiais e "
            "serviços, bem como aquisição, recebimento, armazenamento, distribuição, "
            "manutenção, fiscalização e controle dos materiais, equipamentos, viaturas e "
            "instalações no âmbito da Corporação e submeter à apreciação do Comando Geral para "
            "aprovação",
            "executar atos pertinentes a licitações e contratos, excetuando-se aqueles de "
            "competência exclusiva do ordenador de despesas, quando tratar-se de recursos do "
            "Fundo Especial de Reaparelhamento e Modernização do Corpo de Bombeiros Militar do "
            "Estado de Goiás – FUNEBOM–, bem como acompanhar processos até o cumprimento "
            "integral das obrigações contratuais",
            "realizar gestão junto aos órgãos competentes visando celeridade no andamento "
            "processual de licitações e contratos",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 25",
        "organName": "Comando de Apoio Logístico", "abbr": "",
    },
    ("depdec", "go"): {
        "finalidade": "",
        "competencias": [
            "elaborar planos de gestão operacional nos assuntos relacionados a defesa civil",
            "coordenar as atividades de planejamento, contingência, socorro e reconstrução "
            "relacionadas a defesa civil",
            "realizar ações de prevenção contra incêndio e pânico e de defesa civil por meio "
            "dos órgãos de execução",
            "planejar, controlar e fiscalizar as atividades relacionadas à análise de projetos "
            "e inspeções nas edificações e áreas de risco",
            "elaborar projetos e coordenar programas relacionados à política estadual de Defesa "
            "Civil, além de outras definidas em regulamento",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 27",
        "organName": "Comando de Operações de Defesa Civil", "abbr": "",
    },
    ("deei", "go"): {
        "finalidade": "",
        "competencias": [
            "elaborar o planejamento institucional inerente a formação, especialização, "
            "aperfeiçoamento, habilitação e aprimoramento técnico-profissional dos bombeiros "
            "militares, bem como o controle e fiscalização das atividades correlatas",
            "elaborar normas e manuais operacionais relacionados à doutrina institucional de "
            "ensino",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 28",
        "organName": "Comando de Ensino Bombeiro Militar", "abbr": "",
    },
    ("cint", "go"): {
        "finalidade": "",
        "competencias": [
            "produzir conhecimentos e informações que subsidiem ações para prevenir, "
            "neutralizar, coibir e reprimir atos de qualquer natureza que venham prejudicar a "
            "Corporação no cumprimento de suas atribuições legais, tendo como fundamentos "
            "básicos a defesa do Estado Democrático de Direito e a dignidade da pessoa humana",
            "exercer atividades de inteligência de interesse institucional com o intuito de "
            "subsidiar tomadas de decisão do Comandante-Geral e do Subcomandante-Geral, com "
            "vistas ao aprimoramento dos serviços prestados pela Instituição",
            "identificar, monitorar e avaliar ameaças reais ou potenciais à segurança e "
            "manutenção das atividades do Corpo de Bombeiros Militar",
            "realizar investigações sociais relativas à seleção de candidatos ao ingresso nas "
            "fileiras da Corporação",
            "produzir conhecimentos e informações que subsidiem tomadas de decisão e ações "
            "relacionadas ao exercício das atribuições previstas nesta Lei",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 29",
        "organName": "Comando de Operações de Inteligência", "abbr": "",
    },
    ("dsap", "go"): {
        "finalidade": "",
        "competencias": [
            "planejar, coordenar, orientar, controlar e avaliar as atividades realizadas pelos "
            "serviços médico e odontológico",
            "executar as ações relacionadas à saúde física e mental dos militares da Corporação",
            "apoiar a execução de atividades preventivas e operacionais realizadas diretamente "
            "pela Corporação ou em que ela esteja envolvida",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 32",
        "organName": "Comando de Saúde", "abbr": "",
    },
    ("boa", "go"): {
        "finalidade": (
            "O Centro de Operações Aéreas é responsável pela execução de operações aéreas "
            "relacionadas à missão constitucional da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 34, § 2º",
        "organName": "Centro de Operações Aéreas", "abbr": "",
    },
    ("gab-cg", "go"): {
        "finalidade": (
            "À Chefia de Gabinete compete o exercício das funções de assistência e "
            "assessoramento direto ao Comandante-Geral e ao Subcomandante-Geral, inerentes ao "
            "controle, coordenação e fiscalização das atividades administrativas desenvolvidas "
            "por militares e civis no âmbito dos Gabinetes do Comandante-Geral e do "
            "Subcomandante-Geral, da Ajudância de Ordens, da Assessoria Jurídica e da "
            "Secretaria-Geral"
        ),
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 15",
        "organName": "Chefia de Gabinete", "abbr": "",
    },
    ("assessorias", "go"): {
        "finalidade": (
            "À Assessoria Jurídica compete assessorar o Comando Geral em matérias de natureza "
            "jurídica já pacificadas no âmbito da Procuradoria-Geral do Estado"
        ),
        "competencias": [
            "analisar normas, diretrizes, portarias, determinações, informações e demais "
            "documentos emanados do Comando Geral",
            "orientar o Comando Geral quanto ao exato cumprimento de decisões e sentenças "
            "judiciais, de acordo com as orientações emanadas da Procuradoria-Geral do Estado",
            "coligir elementos de fato e de direito para preparar as informações que devem ser "
            "prestadas à Procuradoria-Geral do Estado, para a defesa dos interesses do Estado "
            "de Goiás em ações judiciais",
        ],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 17",
        "organName": "Assessoria Jurídica", "abbr": "",
    },
    ("ag", "go"): {
        "finalidade": (
            "À Secretaria-Geral competem a recepção, o protocolo, a elaboração e o controle de "
            "toda a documentação pertinente ao Comando Geral"
        ),
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 20",
        "organName": "Secretaria-Geral", "abbr": "",
    },
    ("bbm", "go"): {
        "finalidade": (
            "Batalhão Bombeiro Militar, cujo comando é prerrogativa de Oficial Superior do "
            "Quadro de Oficiais de Comando - QOC, é unidade operacional responsável pela "
            "execução de atividades-fim das respectivas áreas de atuação, conforme diretrizes e "
            "ordens emanadas dos órgãos de direção geral, regional e setorial"
        ),
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 34, § 5º, I",
        "organName": "Batalhão Bombeiro Militar", "abbr": "",
    },
    ("cibm", "go"): {
        "finalidade": (
            "Companhia Independente Bombeiro Militar, cujo comando é prerrogativa de Oficial "
            "Superior do QOC, é unidade operacional responsável pela execução de atividades-fim "
            "das respectivas áreas de atuação, conforme diretrizes e ordens emanadas dos órgãos "
            "de direção geral, regional e setorial"
        ),
        "competencias": [],
        "source": "cf. CBMGO, LOB (Lei nº 18.305/2013), Art. 34, § 5º, II",
        "organName": "Companhia Independente Bombeiro Militar", "abbr": "",
    },

    # --- Distrito Federal (CBMDF) — Lei nº 8.255/1991 ---
    # LOB por finalidade/atribuição; (cg) usa a atribuição do Comandante-Geral (cargo).
    ("cg", "df"): {
        "finalidade": (
            "O Comandante-Geral do Corpo de Bombeiros Militar do Distrito Federal é o "
            "responsável pela administração, comando e emprego da corporação"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 9º",
        "organName": "Comandante-Geral", "abbr": "",
    },
    ("condeg", "df"): {
        "finalidade": (
            "O Alto Comando, órgão consultivo do Comandante-Geral, é constituído dos seguintes "
            "membros: Comandante-Geral, na qualidade de Presidente; Subcomandante-Geral, na "
            "qualidade de Vice-Presidente; Chefe do Estado-Maior-Geral; Controlador; Chefe de "
            "Gabinete do Comandante-Geral; Chefes de Departamento; Diretores; "
            "Comandante-Operacional; Ajudante-Geral; os Ex-Comandantes-Gerais e "
            "Ex-Subcomandantes-Gerais da Corporação, enquanto não passarem para a inatividade"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 8º-A",
        "organName": "Alto Comando", "abbr": "",
    },
    ("corregedoria", "df"): {
        "finalidade": (
            "A Controladoria é o órgão de assessoramento direto e imediato ao Comandante-Geral "
            "quanto aos assuntos e providências relacionados com a defesa do patrimônio "
            "público, auditoria, correição, ouvidoria, orientação e fiscalização, e averiguação "
            "e análise das atividades de administração orçamentária, financeira, patrimonial e "
            "de gestão de pessoas"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 22",
        "organName": "Controladoria", "abbr": "",
    },
    ("ag", "df"): {
        "finalidade": (
            "A Ajudância Geral, subordinada diretamente ao Comandante-Geral, é o órgão de "
            "direção encarregado de auxiliar nas funções de administração do Quartel do Comando "
            "Geral, considerado como Organização de Bombeiro Militar"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 21",
        "organName": "Ajudância Geral", "abbr": "",
    },
    ("gab-cg", "df"): {
        "finalidade": (
            "O Gabinete do Comandante-Geral tem a seu cargo as funções de assistência e "
            "assessoramento direto ao Comandante-Geral, nos assuntos que escapem às atribuições "
            "normais e específicas dos demais órgãos de direção e destina-se a dar "
            "flexibilidade à estrutura do Comando Geral da Corporação, particularmente em "
            "assuntos técnicos especializados"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 23",
        "organName": "Gabinete do Comandante-Geral", "abbr": "",
    },
    ("deei", "df"): {
        "finalidade": (
            "A Academia de Bombeiro Militar (ABM) é o órgão de apoio do sistema de ensino, "
            "subordinado à Diretoria de Ensino e Instrução, incumbida da formação, do "
            "aperfeiçoamento, do treinamento e da instrução especializada dos oficiais e dos "
            "cadetes do Corpo de Bombeiros Militar do Distrito Federal e, eventualmente, de "
            "oficiais e de alunos de outras corporações"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 25",
        "organName": "Academia de Bombeiro Militar", "abbr": "ABM",
    },
    ("dsap", "df"): {
        "finalidade": (
            "As Policlínicas são órgãos de apoio ao sistema de saúde, incumbidas da assistência "
            "médica, odontológica, farmacêutica e sanitária à família bombeiro-militar, "
            "conforme dispuser a lei"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 26",
        "organName": "Policlínicas", "abbr": "",
    },
    ("dpo", "df"): {
        "finalidade": (
            "Comando Operacional é a denominação genérica dada a Organização Bombeiro-Militar "
            "de mais alto escalão, dotada de Estado-Maior próprio e subordinada ao "
            "Comandante-Geral, que tem a seu cargo o planejamento estratégico, a coordenação e "
            "o emprego das unidades e subunidades que lhes forem subordinadas, com a finalidade "
            "de executar atividades de prevenção, guarda e segurança, combate a incêndio, busca "
            "e salvamento, atendimento pré-hospitalar e defesa civil, além de outras, em uma "
            "determinada área operacional"
        ),
        "competencias": [],
        "source": "cf. CBMDF, LOB (Lei nº 8.255/1991), Art. 28, § 1º",
        "organName": "Comando Operacional", "abbr": "",
    },

    # --- Espírito Santo (CBMES) — Lei Complementar nº 101/1997 (texto consolidado) ---
    # LOB que dá finalidade/competência (caput e §§ acrescidos por LC 705/2013 — texto de Lei,
    # não NGA) a vários órgãos. (cg) usa a atribuição do Comandante-Geral.
    ("cg", "es"): {
        "finalidade": (
            "O Comandante-Geral é o responsável pelo comando, administração e emprego da "
            "Corporação. Será um Oficial da Ativa do último posto do Quadro de Oficiais "
            "Combatentes BM"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 10",
        "organName": "Comandante-Geral", "abbr": "",
    },
    ("depdec", "es"): {
        "finalidade": (
            "À Coordenadoria Estadual de Proteção e Defesa Civil, órgão central do Sistema "
            "Estadual de Defesa Civil, compete, além de outras atribuições que lhe forem "
            "conferidas por lei, articular e coordenar as ações de proteção e defesa civil no "
            "Estado, compreendendo a prevenção e a preparação para desastres, a assistência e "
            "socorro às vítimas das calamidades, o restabelecimento de serviços essenciais e a "
            "reconstrução de comunidades"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 9º, § 1º",
        "organName": "Coordenadoria Estadual de Proteção e Defesa Civil", "abbr": "",
    },
    ("corregedoria", "es"): {
        "finalidade": (
            "A Corregedoria é responsável por planejar, coordenar, instaurar, executar, "
            "fiscalizar e controlar os trabalhos dos processos e procedimentos administrativos "
            "de qualquer natureza, das atividades de investigação, bem como das apurações das "
            "infrações penais militares, referentes aos atos e fatos envolvendo a participação "
            "de militares estaduais da Corporação, competindo-lhe também a auditagem nos "
            "processos administrativos e operacionais da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 9º, § 2º",
        "organName": "Corregedoria", "abbr": "",
    },
    ("cot", "es"): {
        "finalidade": (
            "A Diretoria de Atividades Técnicas (DAT), órgão subordinado diretamente ao Comando "
            "Geral do Corpo de Bombeiros, tem como competência: estudar, analisar, planejar, "
            "normatizar, exigir e fiscalizar o cumprimento das disposições legais, assim como "
            "todos os serviços de segurança contra incêndio e pânico, dirigindo também todas as "
            "atividades que envolvem as perícias de incêndio e explosão em locais de sinistro "
            "no Estado do Espírito Santo"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 13, § 2º",
        "organName": "Diretoria de Atividades Técnicas", "abbr": "DAT",
    },
    ("dpo", "es"): {
        "finalidade": (
            "A Diretoria de Operações (DOp), órgão subordinado diretamente ao Comando Geral do "
            "Corpo de Bombeiros, tem como competência: disciplinar, coordenar e controlar todas "
            "as atividades envolvendo as missões constitucionais do CBMES especificamente no "
            "que se refere a combate a incêndios e busca e salvamento, bem como apurar dados a "
            "fim de fundamentar estatísticas para um melhor emprego e uso de técnicas e táticas "
            "adequadas nas ações referentes aos procedimentos operacionais"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 13, § 3º",
        "organName": "Diretoria de Operações", "abbr": "DOp",
    },
    ("dlog", "es"): {
        "finalidade": (
            "A Diretoria de Apoio Logístico (DAL), órgão subordinado diretamente ao Comando "
            "Geral do Corpo de Bombeiros, tem como competência: planejar, supervisionar, "
            "coordenar, controlar, fiscalizar e executar as ações da aquisição, do "
            "armazenamento e da manutenção dos materiais, dos equipamentos, dos armamentos, das "
            "munições, das viaturas, dos bens móveis e imóveis, obras e instalações "
            "patrimoniais, convênios e contratos administrativos e de telecomunicações"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 13, § 4º",
        "organName": "Diretoria de Apoio Logístico", "abbr": "DAL",
    },
    ("dpof", "es"): {
        "finalidade": (
            "A Diretoria de Finanças (DF), órgão subordinado diretamente ao Comando Geral do "
            "Corpo de Bombeiros, tem como competência: planejar, supervisionar, coordenar, "
            "controlar, fiscalizar e executar a administração financeira e patrimonial da "
            "Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 13, § 5º",
        "organName": "Diretoria de Finanças", "abbr": "DF",
    },
    ("ag", "es"): {
        "finalidade": (
            "A Ajudância-Geral tem como competência o desenvolvimento das atividades "
            "administrativas do Comando Geral e suas principais atribuições são: secretaria do "
            "Comando Geral, incluindo correspondência, protocolo geral, arquivo geral e serviço "
            "de embarque da corporação"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 14",
        "organName": "Ajudância-Geral", "abbr": "",
    },
    ("assessorias", "es"): {
        "finalidade": (
            "As assessorias, constituídas eventualmente para determinados estudos que escapem "
            "às atribuições normais e específicas dos órgãos de direção, destinam-se a dar "
            "flexibilidade a estrutura do Comando da Corporação, particularmente em assuntos "
            "especializados"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 16",
        "organName": "Assessorias", "abbr": "",
    },
    ("deei", "es"): {
        "finalidade": (
            "O Centro de Ensino e Instrução de Bombeiros (CEIB), é o órgão responsável pela "
            "formação, aperfeiçoamento e especialização de bombeiros, bem como, ao "
            "desenvolvimento de estudos e pesquisas"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 17, § 1º",
        "organName": "Centro de Ensino e Instrução de Bombeiros", "abbr": "CEIB",
    },
    ("dsap", "es"): {
        "finalidade": (
            "O Centro de Serviço Social (CSS), é o órgão de apoio de pessoal, destinando-se, a "
            "prestação de serviços assistenciais"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 17, § 2º",
        "organName": "Centro de Serviço Social", "abbr": "CSS",
    },
    ("cat", "es"): {
        "finalidade": (
            "O Centro de Atividades Técnicas (CAT), órgão subordinado diretamente ao Comando do "
            "Corpo de Bombeiros, tem como competência: estudar, analisar, planejar, normatizar, "
            "exigir e fiscalizar o cumprimento das disposições legais, assim como todos os "
            "serviços de segurança contra incêndio e pânico, bem como realizar perícias de "
            "incêndio e explosões em locais de sinistro no Estado do Espírito Santo"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 19",
        "organName": "Centro de Atividades Técnicas", "abbr": "CAT",
    },
    ("bbm", "es"): {
        "finalidade": (
            "O Batalhão de Bombeiros Militares, órgão subordinado diretamente ao Comando do "
            "Corpo de Bombeiros, tem como competência: a prevenção e o combate a incêndios, "
            "busca e salvamento, realizar socorros de urgências, controlar o tráfego de "
            "embarcações próximo às praias, rios e lagos e ações de defesa civil"
        ),
        "competencias": [],
        "source": "cf. CBMES, LOB (LC nº 101/1997), Art. 20",
        "organName": "Batalhão de Bombeiros Militares", "abbr": "BBM",
    },

    # --- Maranhão (CBMMA) — Lei nº 10.230/2015 ---
    # LOB que dá finalidade/competência aos órgãos (caput dos artigos e §§ do Art. 13).
    # (cg) usa a atribuição do Comandante-Geral.
    ("cg", "ma"): {
        "finalidade": "A administração e o comando da Corporação são de competência do Comandante-Geral",
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 6º",
        "organName": "Comandante-Geral", "abbr": "",
    },
    ("condeg", "ma"): {
        "finalidade": "O Alto-Comando tem por finalidade opinar, propor e estudar sobre",
        "competencias": [
            "políticas de gestão e estratégia da Corporação",
            "gestão de planos e programas oriundos do plano diretor da Corporação",
            "outras matérias que sejam propostas pelo Comandante-Geral",
        ],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 9º",
        "organName": "Alto-Comando", "abbr": "",
    },
    ("dp", "ma"): {
        "finalidade": (
            "À Diretoria de Pessoal compete o planejamento, coordenação, execução, controle e "
            "fiscalização relacionados a pessoal, além da assistência social e religiosa ao "
            "bombeiro militar"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 1º",
        "organName": "Diretoria de Pessoal", "abbr": "",
    },
    ("dpof", "ma"): {
        "finalidade": (
            "À Diretoria de Finanças compete o funcionamento do sistema de administração "
            "financeira, programação, orçamento e contabilidade"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 2º",
        "organName": "Diretoria de Finanças", "abbr": "",
    },
    ("deei", "ma"): {
        "finalidade": (
            "À Diretoria de Ensino e Pesquisa compete o planejamento, coordenação, controle e "
            "fiscalização das atividades de formação, aperfeiçoamento e especialização nos "
            "diferentes níveis de ensino, do adestramento e da instrução"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 3º",
        "organName": "Diretoria de Ensino e Pesquisa", "abbr": "",
    },
    ("dlog", "ma"): {
        "finalidade": (
            "À Diretoria de Apoio Logístico compete o planejamento, aquisição, coordenação, "
            "fiscalização e controle de suprimento, material, equipamentos e viaturas, bem "
            "como, das atividades de manutenção de material e das instalações físicas"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 4º",
        "organName": "Diretoria de Apoio Logístico", "abbr": "",
    },
    ("cat", "ma"): {
        "finalidade": (
            "À Diretoria de Atividades Técnicas compete o planejamento, fiscalização e controle "
            "das atividades de prevenção em locais de grande concentração humana, vistorias e "
            "pareceres técnicos, apoio operacional e auxílio dos serviços e missões específicas "
            "no âmbito estadual"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 5º",
        "organName": "Diretoria de Atividades Técnicas", "abbr": "",
    },
    ("cint", "ma"): {
        "finalidade": (
            "A Diretoria de Inteligência compete o assessoramento direto ao Comandante-Geral "
            "nos assuntos pertinentes à informação, à inteligência e à contra-inteligência"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 6º",
        "organName": "Diretoria de Inteligência", "abbr": "",
    },
    ("cinf", "ma"): {
        "finalidade": (
            "À Diretoria de Planejamento e Modernização compete o planejamento orçamentário, a "
            "gestão de projetos, elaboração de planos de modernização da Institucional e a "
            "implementação de sistemas de tecnologia da informação"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 13, § 7º",
        "organName": "Diretoria de Planejamento e Modernização", "abbr": "",
    },
    ("ag", "ma"): {
        "finalidade": (
            "A Ajudância-Geral, subordinada ao Comandante Adjunto, em nível de Centro, compete "
            "a publicação dos atos administrativos e auxiliar nas funções de administração e "
            "conservação das instalações físicas do Quartel do Comando Geral"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 14",
        "organName": "Ajudância-Geral", "abbr": "",
    },
    ("gab-cg", "ma"): {
        "finalidade": (
            "O Gabinete do Comandante-Geral, subordinado diretamente ao Comandante-Geral, em "
            "nível de Centro, tem a seu cargo as funções de assistência geral e assessoramento "
            "nos assuntos que não sejam às atribuições normais e específicas dos demais órgãos "
            "de direção e destina-se a dar flexibilidade à estrutura do Comando Geral da "
            "corporação"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 17",
        "organName": "Gabinete do Comandante-Geral", "abbr": "",
    },
    ("assessorias", "ma"): {
        "finalidade": (
            "As Assessorias compete dar suporte à estrutura do Comando da Corporação, "
            "particularmente em assuntos de natureza técnica ou especializada, podendo ser "
            "constituídas por bombeiros militar ou por civis, de acordo legislação específica"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 19",
        "organName": "Assessorias", "abbr": "",
    },
    ("dsap", "ma"): {
        "finalidade": (
            "A Coordenadoria Médica de Saúde, órgão subordinado ao Comandante Adjunto, compete "
            "a assistência médica, farmacêutica e sanitária da família bombeiro militar"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 22",
        "organName": "Coordenadoria Médica de Saúde", "abbr": "",
    },
    ("crbm", "ma"): {
        "finalidade": (
            "Aos Comandos Operacionais, denominação genérica dada às organizações bombeiros "
            "militar operacionais de mais alto escalão, subordinados ao Comandante Adjunto, "
            "compete à aplicação da disciplina, o planejamento estratégico, a coordenação e o "
            "emprego de unidade e subunidade operacionais, com a finalidade de executar as "
            "atividades de prevenção, guarda e segurança, combate a incêndio, busca e "
            "salvamento, atendimento pré-hospitalar e proteção e defesa civil, engenharia de "
            "segurança contra incêndio e pânico, além de outras conexas"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 29",
        "organName": "Comandos Operacionais", "abbr": "",
    },
    ("bbm", "ma"): {
        "finalidade": (
            "Ao Batalhão de Bombeiros Militar e ao Batalhão de Bombeiros Militar Especializado "
            "compete o planejamento estratégico, coordenação e o emprego de unidade e "
            "subunidade operacionais, com a finalidade de executar as atividades de prevenção, "
            "guarda e segurança, combate a incêndio, busca e salvamento, atendimento "
            "pré-hospitalar e proteção e defesa civil, engenharia de segurança contra incêndio "
            "e pânico, além de outras conexas"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 28, § 4º",
        "organName": "Batalhão de Bombeiros Militar", "abbr": "BBM",
    },
    ("bbs", "ma"): {
        "finalidade": (
            "Ao Batalhão de Bombeiros de Busca e Salvamento compete as missões de resgate, "
            "busca, salvamento terrestre e em altura e as demais que lhes sejam conexas"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 28, § 7º",
        "organName": "Batalhão de Bombeiros de Busca e Salvamento", "abbr": "BBS",
    },
    ("bifea", "ma"): {
        "finalidade": (
            "Ao Batalhão de Bombeiros Ambiental compete as missões de prevenção e combate a "
            "incêndios florestais, as relacionadas ao meio-ambiente e as demais que lhes sejam "
            "conexas"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 28, § 8º",
        "organName": "Batalhão de Bombeiros Ambiental", "abbr": "BBA",
    },
    ("cibm", "ma"): {
        "finalidade": (
            "A Companhia Independente de Bombeiros Militar e a Companhia Independente "
            "Especializada de Bombeiros Militar compete o planejamento estratégico, coordenação "
            "e o emprego de unidade e subunidade operacionais, em área de menor abrangência que "
            "um Batalhão de Bombeiros Militar, com a finalidade de executar as atividades de "
            "prevenção, guarda e segurança, combate a incêndio, busca e salvamento, atendimento "
            "pré-hospitalar e defesa civil, engenharia de segurança contra incêndio e pânico, "
            "além de outras conexas"
        ),
        "competencias": [],
        "source": "cf. CBMMA, LOB (Lei nº 10.230/2015), Art. 28, § 9º",
        "organName": "Companhia Independente de Bombeiros Militar", "abbr": "CIBM",
    },

    # --- Minas Gerais (CBMMG) — Lei Complementar nº 54/1999 ---
    # LOB que dá finalidade/competência (caput e incisos) a parte dos órgãos. As Diretorias
    # (Art. 17-19) só são mencionadas, sem finalidade individual → sem entrada (dp/dpof).
    ("cg", "mg"): {
        "finalidade": "O Comandante-Geral é responsável pelo comando e pela administração geral da Corporação",
        "competencias": [],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 12, § 1º",
        "organName": "Comandante-Geral", "abbr": "",
    },
    ("cat", "mg"): {
        "finalidade": (
            "Compete ao Centro de Atividades Técnicas - CAT -, unidade subordinada diretamente "
            "ao Comando-Geral do Corpo de Bombeiros Militar"
        ),
        "competencias": [
            "pesquisar, analisar, planejar, normatizar, exigir e fiscalizar o cumprimento das "
            "disposições legais próprias dos serviços de segurança contra incêndio e pânico",
            "realizar perícias de incêndio e explosão em locais de sinistro",
            "atuar como segunda instância na análise de projetos de prevenção no Estado",
        ],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 24",
        "organName": "Centro de Atividades Técnicas", "abbr": "CAT",
    },
    ("dlog", "mg"): {
        "finalidade": (
            "O Centro de Suprimento e Manutenção - CSM -, unidade responsável pelo suprimento "
            "logístico da corporação, vincula-se à diretoria de Apoio Logístico, cabendo-lhe as "
            "atividades de recebimento, estocagem, distribuição de materiais, manutenção de "
            "viaturas e equipamentos especializados e intendência"
        ),
        "competencias": [],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 23",
        "organName": "Centro de Suprimento e Manutenção", "abbr": "CSM",
    },
    ("deei", "mg"): {
        "finalidade": (
            "A Academia de Bombeiros Militar – ABM – é unidade responsável pela formação, pelo "
            "aperfeiçoamento e pela especialização de Bombeiros"
        ),
        "competencias": [],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 22",
        "organName": "Academia de Bombeiros Militar", "abbr": "ABM",
    },
    ("ag", "mg"): {
        "finalidade": (
            "A Ajudância-Geral, unidade responsável pelas funções administrativas do "
            "Comando-Geral, é subordinada diretamente a esse Comando, cabendo-lhe"
        ),
        "competencias": [
            "o trabalho de secretaria, correspondência, correio, protocolo geral, arquivo "
            "geral, boletim geral e outros",
            "o apoio ao quartel do Comando-Geral no que se refere a pessoal e material, "
            "administração financeira e contábil, almoxarifado e aprovisionamento",
            "a segurança do quartel do Comando-Geral",
        ],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 25",
        "organName": "Ajudância-Geral", "abbr": "",
    },
    ("crbm", "mg"): {
        "finalidade": (
            "Os Comandos Operacionais de Bombeiros, Unidades de Direção Intermediária, são "
            "responsáveis perante o Comando-Geral pela coordenação das atividades operacionais "
            "de competência do Corpo de Bombeiros Militar, em sua respectiva área de atuação, "
            "de acordo com as diretrizes e ordens emanadas do Comando-Geral"
        ),
        "competencias": [],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 20, § 1º",
        "organName": "Comandos Operacionais de Bombeiros", "abbr": "",
    },
    ("bbm", "mg"): {
        "finalidade": (
            "Compete ao Batalhão e à Companhia Independente de Bombeiros Militar, unidades "
            "subordinadas diretamente ao Comando Operacional de Bombeiros, realizar ações de "
            "prevenção e combate a incêndio, busca e salvamento, socorros de urgência e defesa "
            "civil"
        ),
        "competencias": [],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 27",
        "organName": "Batalhão de Bombeiros Militar", "abbr": "BBM",
    },
    ("cibm", "mg"): {
        "finalidade": (
            "Compete ao Batalhão e à Companhia Independente de Bombeiros Militar, unidades "
            "subordinadas diretamente ao Comando Operacional de Bombeiros, realizar ações de "
            "prevenção e combate a incêndio, busca e salvamento, socorros de urgência e defesa "
            "civil"
        ),
        "competencias": [],
        "source": "cf. CBMMG, LOB (LC nº 54/1999), Art. 27",
        "organName": "Companhia Independente de Bombeiros Militar", "abbr": "CIA IND BM",
    },

    # =====================================================================
    # Lote 3 — MS, MT, PA, PB, PE (camada LOB /comparar, 2026-06-28)
    # =====================================================================

    # --- Mato Grosso do Sul (CBMMS) — Lei Complementar nº 188/2014 ---
    # LOB moderna que dá finalidade ("é órgão de Direção Setorial do sistema...",
    # "competindo-lhe", "é o órgão de Apoio...") a quase todos os órgãos. (cg) usa a
    # atribuição do Comandante-Geral (a LOB não dá finalidade ao Comando como órgão).
    ("cg", "ms"): {
        "finalidade": (
            "O Comandante-Geral do CBMMS é o responsável superior pelo comando, "
            "administração e emprego da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 8º",
        "organName": "Comando Geral", "abbr": "",
    },
    ("corregedoria", "ms"): {
        "finalidade": (
            "A Corregedoria é órgão de Direção Geral, subordinado ao Comandante-Geral, "
            "responsável pela preservação da disciplina, hierarquia e da ética "
            "Bombeiro-Militar, competindo-lhe, também, normatizar, coordenar, controlar, "
            "fiscalizar e proceder a apuração de fatos que envolvam responsabilidade Penal "
            "Militar, Administrativa e Disciplinar dos membros da Corporação, bem como o "
            "exercer e supervisionar as atribuições relativas ao Poder Disciplinar e de "
            "Polícia Judiciária Militar, podendo, ainda exercer atribuições de inteligência"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 15",
        "organName": "Corregedoria", "abbr": "",
    },
    ("dp", "ms"): {
        "finalidade": (
            "A Diretoria de Pessoal é órgão de Direção Setorial do sistema de recursos "
            "humanos do CBMMS, competindo-lhe o estudo, planejamento, orientação normativa, "
            "coordenação, supervisão, controle e execução das atividades relativas à gestão "
            "de pessoal e desenvolvimento de recursos humanos da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 17",
        "organName": "Diretoria de Pessoal", "abbr": "DP",
    },
    ("dlog", "ms"): {
        "finalidade": (
            "A Diretoria de Apoio Logístico é órgão de Direção Setorial do sistema "
            "logístico do CBMMS, competindo-lhe o estudo, planejamento, orientação "
            "normativa, coordenação, supervisão, controle e execução das atividades "
            "relativas à gestão do material, patrimônio e informática da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 18",
        "organName": "Diretoria de Apoio Logístico", "abbr": "DAL",
    },
    ("dpof", "ms"): {
        "finalidade": (
            "A Diretoria de Finanças é órgão de Direção Setorial do sistema de administração "
            "financeira do CBMMS, competindo-lhe o estudo, planejamento, orientação "
            "normativa, coordenação, supervisão, controle e execução das atividades relativas "
            "à gestão financeira, ao planejamento e execução orçamentária, à contabilidade e "
            "auditoria"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 19",
        "organName": "Diretoria de Finanças", "abbr": "DF",
    },
    ("cot", "ms"): {
        "finalidade": (
            "A Diretoria de Atividades Técnicas é órgão de Direção Setorial do sistema de "
            "prevenção do CBMMS, competindo-lhe a normatização, o estudo, a análise, o "
            "planejamento das atividades preventivas, a orientação técnica, o controle e a "
            "fiscalização dos órgãos de execução da Corporação empenhados nas atividades "
            "relativas à aplicação das normas de segurança contra incêndio, pânico e outros "
            "riscos, e ao cumprimento das disposições legais sobre o assunto no âmbito do "
            "Estado de Mato Grosso do Sul"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 20",
        "organName": "Diretoria de Atividades Técnicas", "abbr": "DAT",
    },
    ("deei", "ms"): {
        "finalidade": (
            "A Diretoria de Ensino, Instrução, Pesquisa e Educação (DEIPE) é o órgão de "
            "Direção Setorial do CBMMS, responsável pela administração do Ensino, Instrução, "
            "Pesquisa e da Educação Bombeiro-Militar, com competência de planejar, coordenar, "
            "fiscalizar, controlar e promover a pesquisa, o ensino em todas as suas "
            "modalidades, a instrução e o treinamento operacional relativo às atividades do "
            "Corpo de Bombeiros Militar"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 21",
        "organName": "Diretoria de Ensino, Instrução, Pesquisa e Educação", "abbr": "DEIPE",
    },
    ("dsap", "ms"): {
        "finalidade": (
            "A Diretoria de Saúde é órgão de Direção Setorial do Sistema de Saúde do CBMMS, "
            "com competência para gerir, planejar, coordenar, fiscalizar, controlar e "
            "manutenir as atividades de atendimento de emergência e urgência pré-hospitalar, "
            "assistência social, religiosa, psicológica e de saúde em geral, destinados aos "
            "bombeiros militares"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 22",
        "organName": "Diretoria de Saúde", "abbr": "DS",
    },
    ("cinf", "ms"): {
        "finalidade": (
            "À Diretoria de Telemática e Estatística é o órgão de Direção Setorial do CBMMS "
            "com competência para implementar, coordenar, controlar e fiscalizar os sistemas "
            "de tecnologia da informação e de comunicações, assim como promover sua "
            "manutenção e desenvolver estudos estatísticos do CBMMS"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 23",
        "organName": "Diretoria de Telemática e Estatística", "abbr": "DTel",
    },
    ("bifea", "ms"): {
        "finalidade": (
            "A Diretoria de Proteção Ambiental (DPA) é o órgão de Direção Setorial do CBMMS, "
            "responsável pelo planejamento, execução, orientação normativa, supervisão e pelo "
            "controle das atividades inerentes ao serviço de proteção ambiental no âmbito do "
            "CBMMS"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 23-A",
        "organName": "Diretoria de Proteção Ambiental", "abbr": "DPA",
    },
    ("cint", "ms"): {
        "finalidade": (
            "A Diretoria de Inteligência (DIntel) é o órgão de Direção Setorial do CBMMS, "
            "responsável pelas políticas referentes ao sistema de gestão de Inteligência, "
            "voltado à atividade-fim da Instituição, com competência para planejar, coordenar, "
            "controlar e fiscalizar as atividades de inteligência e o gerenciamento, "
            "fiscalização e controle de material bélico"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 23-B",
        "organName": "Diretoria de Inteligência", "abbr": "DIntel",
    },
    ("crbm", "ms"): {
        "finalidade": (
            "O Comando Metropolitano de Bombeiros (CMB) é o órgão de Direção Setorial "
            "subordinado diretamente ao Subcomandante-Geral, responsável pelo planejamento, "
            "coordenação, fiscalização, controle, assessoramento e acompanhamento direto de "
            "todas as atividades operacionais e de prevenção desenvolvidas na capital e "
            "regiões a ela subordinadas"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 24",
        "organName": "Comando Metropolitano de Bombeiros", "abbr": "CMB",
    },
    ("ag", "ms"): {
        "finalidade": (
            "A Ajudância Geral é o órgão de Apoio ao Comando Geral, encarregado da "
            "administração e do expediente do Quartel do Comando Geral, considerada como "
            "Organização Bombeiro Militar (OBM), competindo-lhe ainda a execução dos trabalhos "
            "de secretaria, incluindo a correspondência, correio, redação e impressão do "
            "boletim diário, do protocolo e arquivo geral, do apoio em pessoal aos órgãos que "
            "compõem o Comando Geral, dos serviços gerais e da segurança do Quartel do Comando "
            "Geral"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 27",
        "organName": "Ajudância Geral", "abbr": "AG",
    },
    ("gab-cg", "ms"): {
        "finalidade": (
            "Ao Gabinete do Comandante-Geral competem as funções de receber organizar e "
            "distribuir toda a agenda administrativa e política do Comandante-Geral nos "
            "assuntos que extrapolem as atribuições normais e específicas dos demais órgãos da "
            "corporação"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 28",
        "organName": "Gabinete do Comandante-Geral", "abbr": "GabCG",
    },
    ("assessorias", "ms"): {
        "finalidade": (
            "As Assessorias especiais (AssEsp) são órgãos de apoio ligados diretamente ao "
            "Comandante-Geral do CBMMS e serão constituídas para determinados estudos que "
            "extrapolem as atribuições normais, específicas e peculiares dos órgãos de Direção "
            "e Estado-Maior, e se destinam a dar flexibilidade à estrutura do Comando da "
            "Corporação, particularmente em assuntos especializados, na forma da legislação "
            "pertinente"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 31",
        "organName": "Assessorias Especiais", "abbr": "AssEsp",
    },
    ("boa", "ms"): {
        "finalidade": (
            "O Grupamento de Operações Aéreas (GOA) é o órgão de apoio do Subcomando Geral, "
            "responsável pelo planejamento e execução das operações aéreas em apoio às "
            "atividades meio e fim da Corporação, transporte de autoridades, apoio aéreo a "
            "outros órgãos por meio de normas e procedimentos aplicáveis a tais operações, bem "
            "como, a formação de tripulações e manutenção das aeronaves em todo o território do "
            "Estado ou fora dele"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 36",
        "organName": "Grupamento de Operações Aéreas", "abbr": "GOA",
    },
    ("gbm", "ms"): {
        "finalidade": (
            "O GBM é a maior Unidade Operacional (UOp) do CBMMS, com nível de Batalhão, "
            "subordina-se ao CMB, ao CBDiv ou ao CBFron, conforme sua localização, "
            "competindo-lhe executar a atividade fim da corporação"
        ),
        "competencias": [],
        "source": "cf. CBMMS, LOB (LC nº 188/2014), Art. 46",
        "organName": "Grupamento de Bombeiros Militar", "abbr": "GBM",
    },

    # --- Mato Grosso (CBMMT) — Lei Complementar nº 775/2023 (consolidada até LC 806/2024) ---
    # LOB que dá finalidade/caput ("é responsável por...", "presta assessoramento...",
    # "tem por competência...") a cada Diretoria/órgão. (cg) usa a competência do
    # Comandante-Geral; o detalhamento de competências por cargo é remetido a regulamento
    # (Art. 74), mas o caput de cada órgão é VERBATIM da LOB.
    ("cg", "mt"): {
        "finalidade": (
            "A administração, o comando e o emprego da instituição são de competência e "
            "responsabilidade do Comandante-Geral, através de diretrizes e ordens a todos os "
            "níveis corporativos"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 12",
        "organName": "Comandante-Geral", "abbr": "",
    },
    ("condeg", "mt"): {
        "finalidade": (
            "O Conselho Superior de Bombeiros Militar é o colegiado superior da instituição, "
            "de caráter consultivo, que no processo decisório compartilha da gestão "
            "estratégica do Corpo de Bombeiros Militar, subsidiando as decisões do "
            "Comandante-Geral sobre assuntos de extrema relevância"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 14",
        "organName": "Conselho Superior de Bombeiros Militar", "abbr": "",
    },
    ("corregedoria", "mt"): {
        "finalidade": (
            "A Corregedoria Geral do Corpo de Bombeiros Militar é responsável pela "
            "sistematização e controle das atividades de correição funcional e setorial, de "
            "caráter disciplinar, administrativo ou de polícia judiciária militar, vinculada "
            "diretamente ao Comandante-Geral da Instituição"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 20",
        "organName": "Corregedoria Geral", "abbr": "",
    },
    ("assessorias", "mt"): {
        "finalidade": (
            "A Assessoria Jurídica presta assessoramento direto ao Comandante-Geral e "
            "Comandante-Geral Adjunto nas questões jurídicas e de legislação compreendidas na "
            "administração geral da instituição ou outras que lhe forem designadas"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 25",
        "organName": "Assessoria Jurídica", "abbr": "",
    },
    ("depdec", "mt"): {
        "finalidade": (
            "A Assessoria Especial de Proteção e Defesa Civil presta assessoramento direto ao "
            "Comandante-Geral nas questões referentes à promoção e integração à Política "
            "Nacional de Proteção e Defesa Civil e do Sistema Estadual de Proteção e Defesa "
            "Civil"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 28",
        "organName": "Assessoria de Proteção e Defesa Civil", "abbr": "",
    },
    ("dlog", "mt"): {
        "finalidade": (
            "A Diretoria de Administração Institucional é responsável por realizar "
            "planejamento, orientação, controle, coordenação, fiscalização e a execução das "
            "atividades relacionadas com a gestão administrativa, logística, orçamentária e "
            "financeira no âmbito da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 33",
        "organName": "Diretoria de Administração Institucional", "abbr": "",
    },
    ("dp", "mt"): {
        "finalidade": (
            "A Diretoria de Gestão de Pessoas é responsável pelo planejamento, coordenação, "
            "supervisão, fiscalização e execução das atividades relacionadas com as políticas "
            "de controle de pessoal, folha de pagamento, avaliação e promoção de pessoal, "
            "cadastro de pessoal, recrutamento e seleção, assistência à saúde, assistência "
            "psicossocial, segurança no trabalho, execução, coordenação, controle e orientação "
            "de publicação de atos administrativos no Boletim Geral Eletrônico e Restrito, e "
            "outras ações correlatas de interesse da instituição"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 34",
        "organName": "Diretoria de Gestão de Pessoas", "abbr": "",
    },
    ("deei", "mt"): {
        "finalidade": (
            "A Diretoria de Ensino, Instrução e Pesquisa é responsável pela administração do "
            "Sistema de Educação Bombeiro Militar, incumbindo-lhe o planejamento, a "
            "organização, a coordenação, a fiscalização e o controle das atividades de "
            "formação, graduação, pós-graduação, aperfeiçoamento, habilitação e treinamento do "
            "Bombeiro Militar, além da preservação, fomento e difusão da cultura institucional"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 35",
        "organName": "Diretoria de Ensino, Instrução e Pesquisa", "abbr": "",
    },
    ("dpof", "mt"): {
        "finalidade": (
            "A Diretoria de Gestão Estratégica é responsável pela formulação e acompanhamento "
            "das políticas de médio e longo prazo, do planejamento estratégico institucional "
            "e indicadores de desempenho, promovendo o empreendedorismo, a integração das "
            "áreas de planejamento, orçamento e gestão, a captação de recursos e "
            "desenvolvimento organizacional"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 36",
        "organName": "Diretoria de Gestão Estratégica", "abbr": "",
    },
    ("dsap", "mt"): {
        "finalidade": (
            "A Diretoria de Saúde é responsável pelo planejamento, execução, coordenação, "
            "supervisão, fiscalização e avaliação das atividades relacionadas com as políticas "
            "de saúde na corporação, socorros de urgências e emergências pré-hospitalares e "
            "resgate, inspeção de saúde, inquérito sanitário de origem, bem como fomentar e "
            "implementar políticas de melhoria da qualidade de vida e assistência psicossocial "
            "na Corporação, atuando de forma integrada ao Sistema Único de Saúde"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 37",
        "organName": "Diretoria de Saúde", "abbr": "",
    },
    ("gab-cg", "mt"): {
        "finalidade": (
            "O Gabinete do Comandante-Geral presta assessoramento e assistência diretamente "
            "ao Comandante-Geral do Corpo de Bombeiros Militar"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 38",
        "organName": "Gabinete do Comandante-Geral", "abbr": "",
    },
    ("cint", "mt"): {
        "finalidade": (
            "A Agência Central de Inteligência, vinculada diretamente ao Comandante-Geral da "
            "Instituição, integrante do sistema estadual de inteligência, é responsável pela "
            "sistematização, planejamento, coordenação, execução, controle e fiscalização das "
            "políticas de inteligência e informações no âmbito do Corpo de Bombeiros Militar, "
            "com a finalidade de proporcionar ao Comandante-Geral as informações setoriais e "
            "conjunturais necessárias ao processo de tomada de decisões em todos os níveis"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 39",
        "organName": "Agência Central de Inteligência", "abbr": "",
    },
    ("ccs", "mt"): {
        "finalidade": (
            "O Centro de Comunicação Social presta assessoramento direto ao Comandante-Geral "
            "e Comandante-Geral Adjunto, sendo responsável pela política de comunicação "
            "social, marketing e cerimonial da Instituição, visando preservar e fortalecer a "
            "imagem corporativa junto ao público interno e externo, além da coordenação das "
            "atividades do Corpo Musical e do Museu Histórico"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 40",
        "organName": "Centro de Comunicação Social Bombeiro Militar", "abbr": "",
    },
    ("ag", "mt"): {
        "finalidade": (
            "A Ajudância Geral, vinculada diretamente ao Comandante-Geral Adjunto, constitui "
            "uma unidade administrativa, responsável pelo apoio administrativo e de serviços "
            "às atividades do Quartel do Comando Geral do Corpo de Bombeiros Militar e seus "
            "setores descentralizados"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 42",
        "organName": "Ajudância Geral", "abbr": "",
    },
    ("cot", "mt"): {
        "finalidade": (
            "A Diretoria de Segurança Contra Incêndio e Pânico, subordinada diretamente ao "
            "Comandante-Geral Adjunto, é responsável pelo planejamento, execução, coordenação "
            "e controle de todas as atividades concernentes à segurança contra incêndio e "
            "pânico das instalações, edificações e locais de risco, em conformidade com a "
            "legislação peculiar"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 57",
        "organName": "Diretoria de Segurança Contra Incêndio e Pânico", "abbr": "",
    },
    ("dpo", "mt"): {
        "finalidade": (
            "A Diretoria Operacional, subordinada diretamente ao Comandante-Geral Adjunto, é "
            "responsável pela supervisão, coordenação e planejamento das políticas relacionadas "
            "com a atividade operacional da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 58",
        "organName": "Diretoria Operacional", "abbr": "",
    },
    ("crbm", "mt"): {
        "finalidade": (
            "As Unidades classificadas como Comandos Regionais de Bombeiros Militar - CRBM "
            "subordinam-se diretamente à Diretoria Operacional e são responsáveis pela "
            "supervisão, coordenação e planejamento do emprego operacional das UBM a eles "
            "subordinadas"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 59",
        "organName": "Comando Regional de Bombeiros Militar", "abbr": "CRBM",
    },
    ("bbm", "mt"): {
        "finalidade": (
            "As UBM classificadas como Batalhão de Bombeiros Militar (BBM), Companhia "
            "Independente de Bombeiros Militar (CIBM), Pelotão Independente de Bombeiros "
            "Militar (PIBM) e Núcleo de Bombeiros Militar (NBM) são unidades de execução "
            "subordinadas a um Comando Regional de Bombeiros Militar - CRBM"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 60",
        "organName": "Batalhão de Bombeiros Militar", "abbr": "BBM",
    },
    ("bifea", "mt"): {
        "finalidade": (
            "O Batalhão de Emergências Ambientais, unidade especializada, subordinada "
            "diretamente à Diretoria Operacional, é responsável pelo planejamento, "
            "organização, direção, coordenação e execução de atividades de prevenção e combate "
            "a incêndios florestais e emergências com produtos perigosos, atuando em reforço "
            "ou apoio as demais UBM"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 61",
        "organName": "Batalhão de Emergências Ambientais", "abbr": "BEA",
    },
    ("boa", "mt"): {
        "finalidade": (
            "O Grupo de Aviação de Bombeiros Militar, unidade especializada, subordinada "
            "diretamente a Diretoria Operacional, é responsável pelo planejamento, "
            "organização, direção, coordenação e execução de atividade que envolva o emprego "
            "da aviação Bombeiro Militar, atuando em reforço ou apoio as demais UBM"
        ),
        "competencias": [],
        "source": "cf. CBMMT, LOB (LC nº 775/2023), Art. 62",
        "organName": "Grupo de Aviação de Bombeiros Militar", "abbr": "",
    },

    # --- Pará (CBMPA) — Lei nº 11.060/2025 ---
    # LOB nova e detalhada, com caput definindo a finalidade de quase todos os órgãos
    # ("é o órgão de direção-geral responsável por...", "compete...", "À Diretoria ...
    # compete..."). O detalhamento de atribuições é remetido a regulamento (Art. 67), mas o
    # caput de cada órgão é VERBATIM da Lei. (cg) usa a competência do Comandante-Geral.
    # Texto restaurado da extração OCR (que rebaixou maiúsculas de nomes próprios).
    ("cg", "pa"): {
        "finalidade": (
            "Compete ao Comandante-Geral o comando, a gestão, o emprego, a supervisão e a "
            "coordenação geral das atividades da corporação, assessorado pelos órgãos de "
            "direção, apoio e de execução"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 8º",
        "organName": "Comandante-Geral", "abbr": "",
    },
    ("condeg", "pa"): {
        "finalidade": (
            "O Alto Comando do Corpo de Bombeiros Militar do Pará (CBMPA) é o órgão colegiado "
            "de direção-geral, com atribuições deliberativas e consultivas"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 9º",
        "organName": "Alto Comando", "abbr": "",
    },
    ("depdec", "pa"): {
        "finalidade": (
            "A Coordenadoria Estadual de Proteção e Defesa Civil do Pará (CEDEC), órgão de "
            "direção-geral, é o órgão central e coordenador do Sistema Estadual de Proteção e "
            "Defesa Civil (SEPDEC) tem a missão de contribuir para proteção da vida, "
            "patrimônio e meio ambiente, atendendo a população no território paraense, em "
            "situação de emergência ou calamidade pública, desencadeadas por fatores anormais "
            "e adversos, bem como limitar riscos e perdas para a comunidade, com a finalidade "
            "de preservar e restabelecer a normalidade da vida comunitária"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 13",
        "organName": "Coordenadoria Estadual de Proteção e Defesa Civil do Pará", "abbr": "CEDEC",
    },
    ("corregedoria", "pa"): {
        "finalidade": (
            "A Corregedoria-Geral (CORREG), diretamente vinculada ao Comandante-Geral, é o "
            "órgão correcional do Corpo de Bombeiros Militar do Pará (CBMPA) responsável pelo "
            "assessoramento disciplinar, pela orientação, prevenção e fiscalização das "
            "atividades funcionais e da conduta profissional, visando o aprimoramento da "
            "ética, da disciplina e da hierarquia entre os integrantes da corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 15",
        "organName": "Corregedoria-Geral", "abbr": "CORREG",
    },
    ("dpo", "pa"): {
        "finalidade": (
            "O Comando de Operações é o órgão de direção-geral responsável pela direção e pelo "
            "controle dos órgãos de direção intermediária e setorial, de apoio e de execução "
            "da atividade-fim da corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 16",
        "organName": "Comando de Operações", "abbr": "",
    },
    ("dp", "pa"): {
        "finalidade": (
            "O Departamento-Geral de Pessoal (DGP) é responsável pela direção e pelo controle "
            "das atividades de pessoal da corporação relacionadas ao ingresso, à "
            "identificação, à classificação e à movimentação, aos cadastros e às avaliações, "
            "ao recadastramento, às promoções, aos direitos, aos deveres e aos incentivos, à "
            "assistência psicológica, social e religiosa, ao acompanhamento e ao controle de "
            "veteranos e pensionistas, bem como de saúde"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 19",
        "organName": "Departamento-Geral de Pessoal", "abbr": "DGP",
    },
    ("deei", "pa"): {
        "finalidade": (
            "O Departamento-Geral de Cultura, Educação e Pesquisa (DGCEP) é responsável pela "
            "gestão do sistema de ensino bombeiro militar, das atividades de pesquisa, "
            "relacionados à formação, à capacitação, ao aperfeiçoamento, à especialização, à "
            "extensão e qualificação dos oficiais e praças, bem como pela promoção da cultura"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 20",
        "organName": "Departamento-Geral de Cultura, Educação e Pesquisa", "abbr": "DGCEP",
    },
    ("cot", "pa"): {
        "finalidade": (
            "O Departamento-Geral de Segurança contra Incêndios e Emergências (DGSCI) é "
            "responsável por estabelecer diretrizes gerais de segurança contra incêndios e "
            "emergências, de modo a proteger a vida e a reduzir danos ao meio ambiente e ao "
            "patrimônio"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 21",
        "organName": "Departamento-Geral de Segurança contra Incêndios e Emergências", "abbr": "DGSCI",
    },
    ("gab-cg", "pa"): {
        "finalidade": (
            "O Gabinete do Comandante-Geral é um órgão de direção-geral responsável por "
            "prestar assessoria direta, permanente e pessoal ao Comandante-Geral"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 24",
        "organName": "Gabinete do Comandante-Geral", "abbr": "",
    },
    ("ag", "pa"): {
        "finalidade": (
            "A Ajudância-Geral é o órgão de direção-geral que tem a seu cargo as funções de "
            "secretaria e apoio administrativo ao Comando-Geral, coordenação dos serviços "
            "gerais, manutenção e segurança do quartel do Comando-Geral"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 25",
        "organName": "Ajudância-Geral", "abbr": "",
    },
    ("assessorias", "pa"): {
        "finalidade": (
            "A Consultoria Jurídica (CONJUR) é órgão de direção-geral, diretamente subordinada "
            "ao Comandante-Geral, tendo por finalidade a prestação de assessoramento jurídico, "
            "competindo-lhe o estudo de questões de direito compreendidas na política de "
            "administração geral da instituição, examinar aspectos de legalidade dos atos e "
            "normas que lhe forem submetidos à análise e demais atribuições que venham a ser "
            "previstas em regulamento"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 27",
        "organName": "Consultoria Jurídica", "abbr": "CONJUR",
    },
    ("cint", "pa"): {
        "finalidade": (
            "O Centro de Inteligência (CEINT) é órgão de direção-geral, subordinado ao "
            "Comandante-Geral, responsável por planejar, coordenar, executar, fiscalizar, "
            "controlar, articular, supervisionar e gerenciar as atividades de inteligência "
            "bombeiro militar, no âmbito do Corpo de Bombeiros Militar do Pará (CBMPA), dentro "
            "do território paraense, e assessorar o Comandante-Geral da corporação nos "
            "assuntos de cunho estratégico, tático e operacional que lhe forem confiados"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 28",
        "organName": "Centro de Inteligência", "abbr": "CEINT",
    },
    ("crbm", "pa"): {
        "finalidade": (
            "Aos comandos operacionais intermediários de bombeiros, subordinados ao Comando de "
            "Operações, cabe a direção, o controle e o planejamento das atividades "
            "operacionais das suas Unidades Bombeiro Militar (UBMs) subordinadas, no âmbito de "
            "suas respectivas responsabilidades e circunscrições"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 30",
        "organName": "Comandos Operacionais Intermediários de Bombeiros", "abbr": "",
    },
    ("dlog", "pa"): {
        "finalidade": (
            "À Diretoria de Apoio Logístico (DAL), subordinada ao Departamento-Geral de "
            "Administração (DGA), compete planejar, coordenar, fiscalizar e controlar as "
            "necessidades de apoio, suprimento, manutenção, patrimônio e obras"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 33",
        "organName": "Diretoria de Apoio Logístico", "abbr": "DAL",
    },
    ("dpof", "pa"): {
        "finalidade": (
            "À Diretoria de Finanças (DF), subordinada ao Departamento-Geral de Administração "
            "(DGA), compete realizar as atividades financeiras dos órgãos da corporação e a "
            "distribuição de recursos orçamentários e, de acordo com o planejamento "
            "estabelecido"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 34",
        "organName": "Diretoria de Finanças", "abbr": "DF",
    },
    ("cinf", "pa"): {
        "finalidade": (
            "À Diretoria de Tecnologia da Informação e Comunicação (DTIC), subordinada ao "
            "Departamento-Geral de Administração (DGA), compete realizar o planejamento, a "
            "gestão e a execução das ações referentes à tecnologia da informação e "
            "comunicação, nos termos da legislação vigente"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 36",
        "organName": "Diretoria de Tecnologia da Informação e Comunicação", "abbr": "DTIC",
    },
    ("dsap", "pa"): {
        "finalidade": (
            "À Diretoria de Saúde (DS), subordinada ao Departamento-Geral de Pessoal (DGP), "
            "compete o planejamento, a gestão e a execução das ações de assistência "
            "relacionadas à saúde e atenção biopsicossocial do bombeiro militar, seus "
            "dependentes legais, bem como dos animais do Corpo de Bombeiros Militar do Pará "
            "(CBMPA)"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 37",
        "organName": "Diretoria de Saúde", "abbr": "DS",
    },
    ("gbm", "pa"): {
        "finalidade": (
            "Os grupamentos e subgrupamentos bombeiro Militar são órgãos de execução do Corpo "
            "de Bombeiros Militar do Pará (CBMPA), subordinados aos Comandos Regionais de "
            "Bombeiros de Proteção e Emergência Ambiental (CRB) correspondentes, de acordo com "
            "a sua circunscrição"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 50",
        "organName": "Grupamentos e Subgrupamentos Bombeiro Militar", "abbr": "GBM",
    },
    ("bbs", "pa"): {
        "finalidade": (
            "O Grupamento de Busca e Salvamento (GBS) é órgão de execução do Corpo de "
            "Bombeiros Militar do Pará (CBMPA), subordinado ao Comando de Missões Especiais "
            "Bombeiro Militar (CME-BM), tendo como atribuições as ações de busca, salvamento e "
            "resgate, além de outras específicas de Bombeiros Militar, em todo o território do "
            "estado do Pará"
        ),
        "competencias": [],
        "source": "cf. CBMPA, LOB (Lei nº 11.060/2025), Art. 54",
        "organName": "Grupamento de Busca e Salvamento", "abbr": "GBS",
    },

    # --- Paraíba (CBMPB) — Lei Complementar nº 191/2024 ---
    # LOB que dá finalidade ("tem por finalidade", "é responsável por...", "é a unidade
    # gestora...") a cada Diretoria/órgão. Detalhe (competências e estrutura) remetido ao
    # Regulamento Geral - RGBM (Art. 15, XX). (cg) usa a atribuição do Comandante Geral; o
    # planejamento estratégico/operacional cabe ao Estado Maior Geral (mapeado em dpo).
    # PB não tem CEDEC nem Comunicação Social/Inteligência como órgãos próprios (são
    # coordenadorias do EMG) — sem entrada (registrado no doc).
    ("cg", "pb"): {
        "finalidade": (
            "O Comandante Geral – CMTG – é o responsável pelo comando, gestão, emprego, "
            "supervisão e coordenação geral das atividades da Corporação, e seu cargo ocupado, "
            "privativamente, por coronel da ativa do QOEM do CBMPB"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 15",
        "organName": "Comando Geral", "abbr": "CG",
    },
    ("condeg", "pb"): {
        "finalidade": (
            "O Alto Comando – AC – tem a função de exercer o aconselhamento estratégico do "
            "Comando Geral, sendo presidido pelo Comandante Geral e tendo como membros: o "
            "Subcomandante Geral, o Chefe do EMG, o Corregedor Geral, o Controlador Geral, os "
            "Diretores Setoriais, e os Comandantes Regionais da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 27",
        "organName": "Alto Comando", "abbr": "AC",
    },
    ("dpo", "pb"): {
        "finalidade": (
            "O Estado Maior Geral – EMG – é o órgão de assessoramento estratégico do Gabinete "
            "do Comando Geral, responsável pela assessoria perante o Comando Geral no "
            "planejamento e na gestão estratégica para o desenvolvimento e cumprimento das "
            "missões institucionais"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 28",
        "organName": "Estado Maior Geral", "abbr": "EMG",
    },
    ("corregedoria", "pb"): {
        "finalidade": (
            "A Corregedoria do Corpo de Bombeiros Militar – CORREG – órgão auxiliar do Sistema "
            "Geral de Disciplina da Secretaria de Estado da Segurança e Defesa Social "
            "(SGC/SESDS), é o órgão de direção estratégica com a finalidade de apurar as "
            "infrações penais militares, apurando, acompanhando, fiscalizando e aplicando a "
            "correição no regime ético-disciplinar nos serviços da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 30",
        "organName": "Corregedoria do Corpo de Bombeiros Militar", "abbr": "CORREG",
    },
    ("crbm", "pb"): {
        "finalidade": (
            "Os Comandos Regionais de Bombeiro Militar – CRBM – são unidades gestoras, em "
            "nível estratégico, organizadas de forma sistêmica e responsáveis pela gestão "
            "estratégica regionalizada nas Regiões Integradas de Segurança Pública, através do "
            "controle, planejamento e supervisão das atividades operacionais realizadas pelas "
            "OBM subordinadas"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 32",
        "organName": "Comandos Regionais de Bombeiro Militar", "abbr": "CRBM",
    },
    ("dlog", "pb"): {
        "finalidade": (
            "A Diretoria de Apoio Logístico – DAL – tem por finalidade a gestão do sistema "
            "logístico, responsável pelo planejamento, coordenação, fiscalização e controle "
            "das atividades de aquisição, suprimento e manutenção de materiais, viaturas e "
            "equipamentos"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 34",
        "organName": "Diretoria de Apoio Logístico", "abbr": "DAL",
    },
    ("cot", "pb"): {
        "finalidade": (
            "A Diretoria de Atividades Técnicas – DAT – é a unidade gestora, em nível "
            "setorial, organizado de forma sistêmica e responsável pelo estudo, análise, "
            "planejamento, orientação técnica, normatização, controle e fiscalização das "
            "atividades relativas à segurança contra incêndio e controle de pânico, ao "
            "cumprimento das disposições legais sobre o assunto e investigação de incêndios e "
            "explosões"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 35",
        "organName": "Diretoria de Atividades Técnicas", "abbr": "DAT",
    },
    ("deei", "pb"): {
        "finalidade": (
            "A Diretoria de Educação e Pesquisa – DEP – é responsável pela gestão do sistema "
            "de educação militar da Corporação, por meio do planejamento, supervisão, "
            "coordenação, fiscalização, controle e execução das atividades de ensino, "
            "treinamento e pesquisa científica, relacionadas à qualificação profissional de "
            "recursos humanos para o exercício das funções atribuídas aos integrantes do CBMPB"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 37",
        "organName": "Diretoria de Educação e Pesquisa", "abbr": "DEP",
    },
    ("dpof", "pb"): {
        "finalidade": (
            "A Diretoria de Finanças – DF – tem como finalidade a gestão do sistema de "
            "planejamento e administração financeira, orçamentária, contábil, bem como a "
            "gestão de Fundos e Convênios"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 40",
        "organName": "Diretoria de Finanças", "abbr": "DF",
    },
    ("dp", "pb"): {
        "finalidade": (
            "A Diretoria de Gestão de Pessoas – DGP – tem como finalidade o planejamento, "
            "recrutamento, seleção, acompanhamento, execução, controle e fiscalização das "
            "atividades relacionadas com os recursos humanos da Corporação, sejam militares de "
            "carreira ou temporários, bem como os servidores civis"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 41",
        "organName": "Diretoria de Gestão de Pessoas", "abbr": "DGP",
    },
    ("dsap", "pb"): {
        "finalidade": (
            "A Diretoria de Saúde – DS – é o órgão integrante do Sistema de Proteção Social "
            "dos Militares da Corporação, com competência para planejar, coordenar, fiscalizar, "
            "controlar e executar todas as atividades de saúde, assistência biopsicossocial e "
            "veterinária, além do trato das questões referentes ao estado sanitário do pessoal "
            "da Corporação e seus dependentes"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 42",
        "organName": "Diretoria de Saúde", "abbr": "DS",
    },
    ("cinf", "pb"): {
        "finalidade": (
            "A Diretoria de Tecnologia da Informação – DTI – tem por finalidade desenvolver "
            "sistemas e aplicativos computacionais, a prospecção e absorção de novas "
            "tecnologias, administração da rede de informática e dos bancos de dados, o "
            "suporte técnico de software e equipamentos, o atendimento especializado aos "
            "usuários e a governança de tecnologia da informação e inovação"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 43",
        "organName": "Diretoria de Tecnologia da Informação", "abbr": "DTI",
    },
    ("assessorias", "pb"): {
        "finalidade": (
            "A Assessoria de Relações Institucionais - ARI – tem a finalidade de assessorar o "
            "Comando Geral em assuntos legislativos relacionados com a atividade fim da "
            "Corporação e atividades de Defesa Social e Defesa Civil, além de, representar a "
            "Corporação junto aos Poderes Legislativos Federal, Estadual e Municipais"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 21",
        "organName": "Assessoria de Relações Institucionais", "abbr": "ARI",
    },
    ("gab-cg", "pb"): {
        "finalidade": (
            "Ao Gabinete do Comandante Geral do Corpo de Bombeiros Militar compete a direção e "
            "administração geral do Corpo de Bombeiros Militar do Estado da Paraíba – CBMPB no "
            "cumprimento dos seus objetivos, sendo o Comandante Geral a autoridade máxima da "
            "Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 14",
        "organName": "Gabinete do Comandante Geral", "abbr": "GCMTG",
    },
    ("ag", "pb"): {
        "finalidade": (
            "O Quartel do Comando Geral “Coronel Geraldo Cabral de Vasconcelos” – QCG – é o "
            "Centro Administrativo da Corporação, responsável pela manutenção do funcionamento "
            "dos órgãos de direção estratégica e setorial, além do reforço operacional aos "
            "órgãos de execução"
        ),
        "competencias": [],
        "source": "cf. CBMPB, LOB (LC nº 191/2024), Art. 26",
        "organName": "Quartel do Comando Geral", "abbr": "QCG",
    },

    # --- Pernambuco (CBMPE) — Lei nº 15.187/2013 ---
    # LOB que dá finalidade ("incumbe-se de...", "é responsável por...", "tem a seu cargo...",
    # "é o órgão que...") a quase todos os órgãos. (cg) usa a atribuição do Comandante Geral.
    # As Diretorias Integradas (DIM/DIEsp/DInter) são os órgãos de direção operacional; usa-se
    # a DIM (metropolitana) para crbm e a DIEsp para cot (atividades técnicas). DPlaG e DF
    # mapeariam ambas a dpof: usada DF (Finanças). PE não tem órgão aéreo nem florestal/ambiental
    # próprio — sem entrada (registrado no doc).
    ("cg", "pe"): {
        "finalidade": (
            "O Comandante Geral do CBMPE, nomeado pelo Governador do Estado, é o responsável "
            "pelo comando, administração e emprego da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 10",
        "organName": "Comandante Geral", "abbr": "CG",
    },
    ("condeg", "pe"): {
        "finalidade": (
            "O Conselho de Políticas e Estratégias (CPE) é o órgão responsável pela formulação "
            "da doutrina geral de emprego da Corporação, de forma a viabilizar as políticas, "
            "estratégias, diretrizes e ordens estabelecidas pelo Comandante Geral e que "
            "acionam todos os demais órgãos no cumprimento de suas missões"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 12",
        "organName": "Conselho de Políticas e Estratégias", "abbr": "CPE",
    },
    ("dp", "pe"): {
        "finalidade": "A Diretoria de Gestão de Pessoal (DGP) incumbe-se:",
        "competencias": [
            "do planejamento, da normatização, do controle e da fiscalização das atividades "
            "relacionadas com a gestão de pessoal",
            "das atividades de formação, especialização e aperfeiçoamento",
            "da prestação de assistência social aos integrantes do CBMPE e seus dependentes",
        ],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 15",
        "organName": "Diretoria de Gestão de Pessoal", "abbr": "DGP",
    },
    ("dlog", "pe"): {
        "finalidade": "A Diretoria de Logística (DLog) incumbe-se:",
        "competencias": [
            "do planejamento, da normatização, da fiscalização e do controle das atividades "
            "relativas à gestão da aquisição e da contratação para fornecimento de bens e "
            "prestação de serviços",
            "da gestão da frota de viaturas e embarcações",
            "da gestão do patrimônio e do material bélico da Corporação",
            "das atividades de manutenção de materiais e equipamentos",
            "das atividades específicas de planejamento e gestão na área de serviços de "
            "engenharia, arquitetura e obras",
        ],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 17",
        "organName": "Diretoria de Logística", "abbr": "DLog",
    },
    ("dpof", "pe"): {
        "finalidade": (
            "A Diretoria de Finanças (DF) incumbe-se do planejamento, da normatização, da "
            "execução e do controle financeiro do CBMPE"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 19",
        "organName": "Diretoria de Finanças", "abbr": "DF",
    },
    ("crbm", "pe"): {
        "finalidade": (
            "A Diretoria Integrada Metropolitana (DIM) incumbe-se, na área territorial de "
            "Recife e sua Região Metropolitana, do planejamento e supervisão das ordens, "
            "doutrina e emprego das atividades operacionais de prevenção e combate a incêndio, "
            "atendimento pré-hospitalar e salvamento, além do controle operacional dos "
            "atendimentos emergenciais e do gerenciamento das ações de respostas aos desastres"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 23",
        "organName": "Diretoria Integrada Metropolitana", "abbr": "DIM",
    },
    ("cot", "pe"): {
        "finalidade": (
            "A Diretoria Integrada Especializada (DIEsp) incumbe-se na área territorial do "
            "Estado de Pernambuco, do planejamento e supervisão das ordens, doutrina e emprego "
            "das atividades técnicas, notadamente as vistorias, análises de projetos, "
            "cadastramento e credenciamento de empresas, e a execução das normas que "
            "disciplinam a segurança das pessoas e de seus bens contra incêndio e pânico"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 25",
        "organName": "Diretoria Integrada Especializada", "abbr": "DIEsp",
    },
    ("gab-cg", "pe"): {
        "finalidade": (
            "O Gabinete do Comandante Geral (GCG) tem a seu cargo as funções de assistência e "
            "assessoramento direto ao Comandante Geral, bem como a articulação junto aos órgãos "
            "legislativos, na esfera federal, estadual e municipal, em assuntos de interesse do "
            "CBMPE"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 43",
        "organName": "Gabinete do Comandante Geral", "abbr": "GCG",
    },
    ("assessorias", "pe"): {
        "finalidade": (
            "A Assessoria Jurídica (AJ) é o órgão que presta assessoramento jurídico ao "
            "Comando Geral e desempenho das atividades jurídicas previstas em legislação "
            "vigente"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 45",
        "organName": "Assessoria Jurídica", "abbr": "AJ",
    },
    ("ccs", "pe"): {
        "finalidade": (
            "O Centro e Comunicação Social (CCS) incumbe-se da assessoria ao Comando Geral nos "
            "assuntos civis, compreendendo relações públicas, relações com a imprensa, "
            "marketing institucional e cerimonial interno da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 47",
        "organName": "Centro de Comunicação Social", "abbr": "CCS",
    },
    ("cinf", "pe"): {
        "finalidade": (
            "O Centro de Tecnologia da Informação e Comunicações (CTIC) incumbe-se do "
            "assessoramento ao Comando Geral e gestão na área de tecnologia da informação e "
            "comunicações da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 49",
        "organName": "Centro de Tecnologia da Informação e Comunicação", "abbr": "CTIC",
    },
    ("cint", "pe"): {
        "finalidade": (
            "O Centro de Inteligência, órgão integrante do Centro Integrado de Inteligência da "
            "Secretaria de Defesa Social (CIIDS), é responsável pelo assessoramento ao Comando "
            "Geral relativo às ações de inteligência nas áreas de atuação do CBMPE e da defesa "
            "civil"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 53",
        "organName": "Centro de Inteligência", "abbr": "CI",
    },
    ("ag", "pe"): {
        "finalidade": (
            "A Ajudância Geral (AJG) incumbe-se da administração, manutenção, segurança das "
            "instalações do quartel do Comando Geral, bem como a gestão das publicações e "
            "arquivo geral da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 58",
        "organName": "Ajudância Geral", "abbr": "AjG",
    },
    ("corregedoria", "pe"): {
        "finalidade": (
            "O Centro de Justiça e Disciplina (CJD) incumbe-se do assessoramento ao "
            "Subcomandante Geral nos assuntos pertinentes à execução e acompanhamento de "
            "processos administrativos disciplinares, sindicâncias e Inquéritos Policiais "
            "Militares"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 60",
        "organName": "Centro de Justiça e Disciplina", "abbr": "CJD",
    },
    ("deei", "pe"): {
        "finalidade": (
            "O Campus de Ensino Metropolitano II (CEMet II), órgão integrante do Sistema de "
            "Ensino de Defesa Social, compondo a Academia Integrada de Defesa Social (ACIDES), "
            "é responsável pela formação e aperfeiçoamento de Praças e especialização de "
            "Oficiais e Praças da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 67",
        "organName": "Campus de Ensino Metropolitano II", "abbr": "CEMet II",
    },
    ("dsap", "pe"): {
        "finalidade": (
            "O Centro de Assistência Social (CAS) incumbe-se das atividades de assistência e "
            "promoção social, psicológica, jurídica e religiosa ao público interno do CBMPE"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 73",
        "organName": "Centro de Assistência Social", "abbr": "CAS",
    },
    ("gbm", "pe"): {
        "finalidade": (
            "Grupamento de Bombeiros (GB) responsável pelas missões de prevenção e combate a "
            "incêndios, busca e resgate de pessoas e bens, atendimento emergencial "
            "pré-hospitalar, além das atividades de prevenção aquática, de proteção ambiental "
            "na Zona da Mata, no Agreste e no Sertão do Estado"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 83, V",
        "organName": "Grupamento de Bombeiros", "abbr": "GB",
    },
    ("bbs", "pe"): {
        "finalidade": (
            "Grupamento de Bombeiros de Salvamento (GBS) responsável pelas missões de busca e "
            "resgate de pessoas e bens em ambiente fluvial, terrestre e aéreo e operações "
            "insulares, além da proteção ambiental na área territorial de Recife e sua Região "
            "Metropolitana"
        ),
        "competencias": [],
        "source": "cf. CBMPE, LOB (Lei nº 15.187/2013), Art. 83, IV",
        "organName": "Grupamento de Bombeiros de Salvamento", "abbr": "GBS",
    },

    # ===================================================================
    # Lote 4 — PI, PR, RJ, RN, RR
    # ===================================================================

    # --- Piauí (PI) — Lei nº 5.949/2009, alt. pela Lei nº 7.772/2022 (texto
    # consolidado, com artigos "(NR)"). LOB com caput de finalidade por órgão
    # ("é órgão de direção setorial...", "incumbe-se de..."); Art. 48 remete o
    # detalhamento de atribuições ao RACBMEPI (Regulamento, via Decreto).
    ("condeg", "pi"): {
        "finalidade": (
            "O Alto Comando da Corporação é o órgão colegiado e deliberativo composto pelos "
            "Coronéis da ativa da corporação, a ser convocado pelo Comandante-Geral ou seu "
            "substituto para colaborar com o processo decisório nos assuntos de relevância "
            "para o desenvolvimento e cumprimento das atribuições da corporação e elaborar "
            "políticas institucionais"
        ),
        "competencias": [],
        "source": "cf. CBMPI, LOB (Lei nº 5.949/2009 alt. Lei nº 7.772/2022), Art. 16",
        "organName": "Alto Comando da Corporação", "abbr": "",
    },
    ("dp", "pi"): {
        "finalidade": (
            "A Diretoria de Gestão de Pessoas, órgão de direção setorial do sistema de "
            "pessoal, incumbe-se do planejamento, da coordenação, da execução, do controle, e "
            "da fiscalização das atividades relacionadas à pessoal"
        ),
        "competencias": [],
        "source": "cf. CBMPI, LOB (Lei nº 5.949/2009 alt. Lei nº 7.772/2022), Art. 18",
        "organName": "Diretoria de Gestão de Pessoas", "abbr": "",
    },
    ("dpof", "pi"): {
        "finalidade": (
            "A Diretoria Administrativa e Financeira, o órgão de direção setorial responsável "
            "pelo funcionamento do sistema de administração financeira, programação, "
            "orçamento, contabilidade, incumbindo ainda o estudo, o planejamento, a "
            "orientação normativa, a coordenação, supervisão, o controle e a execução das "
            "atividades relativas à gestão do material e patrimônio da corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPI, LOB (Lei nº 5.949/2009 alt. Lei nº 7.772/2022), Art. 19",
        "organName": "Diretoria Administrativa e Financeira", "abbr": "",
    },
    ("deei", "pi"): {
        "finalidade": (
            "A Diretoria de Ensino, Instrução e Pesquisa, o órgão de direção setorial do "
            "sistema de ensino e instrução, incumbe-se do planejamento, da coordenação, do "
            "controle e da fiscalização de todas as atividades de formação, aperfeiçoamento e "
            "especialização, nos diferentes níveis do ensino, do adestramento e da instrução"
        ),
        "competencias": [],
        "source": "cf. CBMPI, LOB (Lei nº 5.949/2009 alt. Lei nº 7.772/2022), Art. 20",
        "organName": "Diretoria de Ensino, Instrução e Pesquisa", "abbr": "",
    },
    ("cot", "pi"): {
        "finalidade": (
            "A Diretoria de Segurança Contra Incêndio, unidade administrativa responsável "
            "pelo planejamento, análise, controle e fiscalização das atividades atinentes à "
            "segurança contra incêndio e pânico no âmbito do Estado do Piauí"
        ),
        "competencias": [],
        "source": "cf. CBMPI, LOB (Lei nº 5.949/2009 alt. Lei nº 7.772/2022), Art. 21",
        "organName": "Diretoria de Segurança Contra Incêndio", "abbr": "",
    },
    ("depdec", "pi"): {
        "finalidade": (
            "O Núcleo de Defesa Civil é órgão de assessoramento do Comando Operacional de "
            "Bombeiros responsável pelo planejamento e execução de atividades de defesa civil "
            "na área de competência do Corpo de Bombeiros"
        ),
        "competencias": [],
        "source": "cf. CBMPI, LOB (Lei nº 5.949/2009 alt. Lei nº 7.772/2022), Art. 26",
        "organName": "Núcleo de Defesa Civil", "abbr": "",
    },
    ("ag", "pi"): {
        "finalidade": (
            "A Ajudância Geral, subordinada diretamente ao Comandante Geral, compete a "
            "publicação dos atos administrativos, recepção de correspondências, assim como "
            "auxiliar nas funções de administração, conservação e segurança das instalações "
            "do Quartel do Comando Geral (QCG), considerado como Organização de Bombeiro "
            "Militar"
        ),
        "competencias": [],
        "source": "cf. CBMPI, LOB (Lei nº 5.949/2009 alt. Lei nº 7.772/2022), Art. 27",
        "organName": "Ajudância Geral", "abbr": "",
    },
    ("dsap", "pi"): {
        "finalidade": (
            "O Núcleo de Saúde é responsável pelo planejamento, orientação, coordenação, "
            "controle e execução de programas de medicina preventiva, saúde comunitária e "
            "controle médico-sanitário de pessoal, execução das atividades de assistência "
            "médica, odontológica, bem como pelas perícias médicas e homologar os pareceres "
            "da junta Médica de Saúde (JMS) no âmbito da corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPI, LOB (Lei nº 5.949/2009 alt. Lei nº 7.772/2022), Art. 32-C",
        "organName": "Núcleo de Saúde", "abbr": "",
    },
    ("dpo", "pi"): {
        "finalidade": (
            "O Comando Operacional de Bombeiros é órgão de execução do mais alto escalão do "
            "sistema operacional subordinado ao órgão de direção geral, tendo a seu cargo o "
            "planejamento estratégico e a fiscalização do emprego dos Comandos Regionais de "
            "Bombeiros"
        ),
        "competencias": [],
        "source": "cf. CBMPI, LOB (Lei nº 5.949/2009 alt. Lei nº 7.772/2022), Art. 34",
        "organName": "Comando Operacional de Bombeiros", "abbr": "COB",
    },
    ("crbm", "pi"): {
        "finalidade": (
            "Os Comandos Regionais de Bombeiros Militar são órgãos de execução subordinados "
            "diretamente ao Comandante Operacional de Bombeiros, devem efetuar o planejamento "
            "operacional, a supervisão, a coordenação, prevenção, o controle, a fiscalização e "
            "a execução das atividades de bombeiro no âmbito de suas respectivas "
            "responsabilidades e circunscrições"
        ),
        "competencias": [],
        "source": "cf. CBMPI, LOB (Lei nº 5.949/2009 alt. Lei nº 7.772/2022), Art. 36",
        "organName": "Comandos Regionais de Bombeiros Militar", "abbr": "",
    },
    ("gbm", "pi"): {
        "finalidade": (
            "Os Grupamentos de Bombeiros Militar têm a seu cargo, dentro de uma determinada "
            "área operacional, as missões de prevenção e extinção de incêndios, busca, "
            "salvamento, atendimento pré-hospitalar e auxílio nas atividades de defesa civil"
        ),
        "competencias": [],
        "source": "cf. CBMPI, LOB (Lei nº 5.949/2009 alt. Lei nº 7.772/2022), Art. 37",
        "organName": "Grupamentos de Bombeiros Militar", "abbr": "",
    },
    ("bbs", "pi"): {
        "finalidade": (
            "O Grupamento de Bombeiro Militar Marítimo tem a seu cargo a realização de "
            "operações aquáticas com a finalidade de executar serviços de prevenção em "
            "eventos náuticos, a busca, salvamentos de pessoas e bens, combate a incêndio em "
            "embarcações e instalações portuárias, bem como a preservação ambiental limitada "
            "às orlas fluviais e lacustre inscritas nos limites geográficos dos municípios de "
            "Ilha Grande de Santa Isabel, Parnaíba, Luís Correia e Cajueiro da Praia, assim "
            "como de toda a costa marítima piauiense"
        ),
        "competencias": [],
        "source": "cf. CBMPI, LOB (Lei nº 5.949/2009 alt. Lei nº 7.772/2022), Art. 38",
        "organName": "Grupamento de Bombeiro Militar Marítimo", "abbr": "",
    },

    # --- Paraná (PR) — Lei nº 22.206/2024, LOB moderna e detalhada (incisos
    # enumerados em quase todos os órgãos de direção). Números de artigo
    # confirmados contra o site oficial do CBMPR (bombeiros.pr.gov.br), dado
    # que a extração em markdown intercala blocos de "Art. N." soltos ao fim
    # de página (rodapé do PDF), não imediatamente antes de cada parágrafo.
    ("cg", "pr"): {
        "finalidade": (
            "O Comandante-Geral, responsável superior pelo comando e pela administração "
            "geral do Corpo de Bombeiros Militar do Paraná - CBMPR, será nomeado pelo "
            "Governador do Estado, dentre os Coronéis Combatentes da ativa da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 12",
        "organName": "Comandante-Geral", "abbr": "CG",
    },
    ("gab-cg", "pr"): {
        "finalidade": (
            "O Gabinete do Comando-Geral será chefiado por um Oficial Superior Combatente da "
            "ativa da Corporação, de livre escolha do Comandante-Geral, competindo-lhe"
        ),
        "competencias": [
            "a assistência direta ao Comandante-Geral no trato e apreciação de assuntos "
            "institucionais",
            "a recepção, o estudo e a triagem dos expedientes encaminhados ao Comandante-Geral",
            "a transmissão e o controle da execução das ordens emanadas pelo Comandante-Geral",
            "a coordenação dos serviços de Ajudância de Ordens do Comandante-Geral",
            "a execução e o controle das atividades relacionadas com a administração "
            "financeira, contabilidade, material e aprovisionamento do Comando-Geral",
        ],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 15",
        "organName": "Gabinete do Comando-Geral", "abbr": "Gab.CmtG",
    },
    ("ag", "pr"): {
        "finalidade": (
            "a Ajudância-Geral, subordinada ao Chefe de Gabinete, exercerá o apoio "
            "administrativo ao Comando-Geral, competindo-lhe"
        ),
        "competencias": [
            "a organização, a direção e a supervisão do pessoal auxiliar de todos os órgãos "
            "do Comando-Geral e do efetivo da Banda de Música do Corpo de Bombeiros Militar "
            "do Paraná - CBMPR",
            "a coordenação dos trabalhos de protocolo geral da Corporação",
            "o controle da entrada e retirada de processos e documentos do arquivo geral",
            "a elaboração dos boletins-gerais",
            "o desenvolvimento das demais tarefas relacionadas com a segurança do "
            "aquartelamento e dos serviços gerais do Comando-Geral",
            "a promoção das atividades necessárias para a manutenção e desenvolvimento do "
            "centro histórico",
        ],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 16",
        "organName": "Ajudância-Geral", "abbr": "AG",
    },
    ("ccs", "pr"): {
        "finalidade": (
            "a Assessoria de Comunicação Organizacional é órgão que presta assessoramento ao "
            "Comando-Geral, competindo-lhe as atividades de"
        ),
        "competencias": [
            "comunicação social, campanhas de educação preventiva e assessoria de imprensa",
            "organização de solenidades na sede do Corpo de Bombeiros Militar do Paraná - "
            "CBMPR, orientando e fiscalizando a execução de eventos nas demais unidades",
        ],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 18",
        "organName": "Assessoria de Comunicação Organizacional", "abbr": "Assecom",
    },
    ("assessorias", "pr"): {
        "finalidade": (
            "A Consultoria Institucional é o órgão que presta assessoramento direto ao "
            "Comandante-Geral e ao Subcomandante-Geral, competindo-lhe"
        ),
        "competencias": [
            "o estudo de questões de direito compreendidas na política de administração "
            "geral da Corporação, exames de aspectos de legalidade dos atos e normas que "
            "forem submetidos à sua apreciação e demais atribuições que venham a ser "
            "previstas em regulamentos",
            "a orientação quanto ao exato cumprimento de decisões e sentenças judiciais, de "
            "acordo com as orientações emanadas pela Procuradoria-Geral do Estado - PGE",
            "a compilação de elementos de fato e de direito para preparar as informações que "
            "devem ser prestadas à Procuradoria-Geral do Estado - PGE para a defesa dos "
            "interesses do Estado em ações judiciais",
            "a análise das minutas e convênios que forem submetidos à sua apreciação, "
            "verificando se preenchem os requisitos legais necessários à sua celebração",
        ],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 20",
        "organName": "Consultoria Institucional", "abbr": "CI",
    },
    ("corregedoria", "pr"): {
        "finalidade": (
            "A Corregedoria-Geral do Corpo de Bombeiros Militar do Paraná - CBMPR é o órgão "
            "técnico, subordinado ao Comandante-Geral, com atuação em todo o Estado, com a "
            "finalidade de"
        ),
        "competencias": [
            "assegurar a correta aplicação da lei",
            "padronizar os procedimentos de Polícia Judiciária Militar e de processos e "
            "procedimentos administrativos",
            "realizar correições, fiscalizações e garantir a preservação dos princípios da "
            "hierarquia e disciplina na Corporação",
        ],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 23",
        "organName": "Corregedoria-Geral", "abbr": "Coger",
    },
    ("dp", "pr"): {
        "finalidade": (
            "A Diretoria de Pessoal é o órgão de direção setorial do sistema de pessoal, "
            "responsável por"
        ),
        "competencias": [
            "desenvolvimento, coordenação, fiscalização, orientação, acompanhamento e "
            "controle das atividades relacionadas com a classificação e movimentação de "
            "pessoal",
            "mobilização, inativos, cadastro e avaliação, direitos, deveres, incentivos, "
            "gerenciamento e inspeção da folha de pagamento",
            "identificação, pessoal civil, serviço auxiliar temporário e recrutamento",
            "acompanhamento e controle das atividades técnico-administrativas relativas aos "
            "serviços de saúde física e mental, assistência social e psicológica",
            "assessoramento nos assuntos referentes a pessoal",
        ],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 28",
        "organName": "Diretoria de Pessoal", "abbr": "DP",
    },
    ("dlog", "pr"): {
        "finalidade": (
            "A Diretoria de Apoio Logístico e Finanças é o órgão de direção setorial "
            "responsável por"
        ),
        "competencias": [
            "coordenação, controle e execução das atividades de logística",
            "suprimento, manutenção e controle patrimonial da Corporação",
            "planejamento, acompanhamento e execução orçamentária e financeira",
            "atividades de controladoria e auditoria de recursos descentralizados",
        ],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 29",
        "organName": "Diretoria de Apoio Logístico e Finanças", "abbr": "DALF",
    },
    ("cot", "pr"): {
        "finalidade": (
            "A Diretoria de Atividades Técnicas é o órgão de direção setorial responsável "
            "pela coordenação, controle e assessoramento em assuntos relacionados"
        ),
        "competencias": [
            "à prevenção e combate a incêndios e desastres em edificações, estabelecimentos, "
            "áreas de risco e eventos temporários, atuando por meio do gerenciamento "
            "normativo, estudos e pesquisa de incêndios",
            "à tecnologia da informação e comunicação, com ações de gestão e desenvolvimento "
            "de sistemas informatizados, infraestrutura, segurança, projetos, inovações e "
            "governança",
        ],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 30",
        "organName": "Diretoria de Atividades Técnicas", "abbr": "DAT",
    },
    ("deei", "pr"): {
        "finalidade": (
            "A Escola Superior de Bombeiro Militar é o órgão de direção setorial de ensino e "
            "instrução no âmbito do Corpo de Bombeiros Militar do Paraná - CBMPR, responsável "
            "pelo planejamento, coordenação, fiscalização, execução e controle das atividades "
            "de ensino desenvolvidas pela Corporação, podendo atuar em parceria com outras "
            "instituições"
        ),
        "competencias": [],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 31",
        "organName": "Escola Superior de Bombeiro Militar", "abbr": "ESBM",
    },
    ("crbm", "pr"): {
        "finalidade": (
            "Os órgãos de execução são operacional e administrativamente subordinados aos "
            "Comandos Regionais de Bombeiro Militar, que são responsáveis, perante o "
            "Subcomandante-Geral, pelo cumprimento das missões bombeiro-militar em suas "
            "respectivas circunscrições territoriais"
        ),
        "competencias": [],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 35",
        "organName": "Comando Regional de Bombeiro Militar", "abbr": "CRBM",
    },
    ("bbm", "pr"): {
        "finalidade": (
            "Batalhão de Bombeiro Militar - BBM: unidade operacional que, utilizando dos "
            "recursos humanos e materiais postos à sua disposição, será incumbida da missão de"
        ),
        "competencias": [
            "coordenar e executar as atividades de defesa civil",
            "exercer o poder de polícia administrativa referente à prevenção a incêndios e "
            "desastres",
            "combater incêndios e desastres",
            "prevenir acidentes na orla marítima e fluvial",
            "realizar buscas, salvamentos, socorros públicos e atendimento pré-hospitalar",
            "outras atribuições definidas em lei",
        ],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 38, I",
        "organName": "Batalhão de Bombeiro Militar", "abbr": "BBM",
    },
    ("cibm", "pr"): {
        "finalidade": (
            "Companhia Independente de Bombeiro Militar - Cia. Ind. BM: unidade operacional "
            "encarregada das mesmas atribuições do Batalhão de Bombeiro Militar - BBM em "
            "áreas de menores dimensões que, por suas condições peculiares, não estejam "
            "incluídas na circunscrição daquele"
        ),
        "competencias": [],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 38, II",
        "organName": "Companhia Independente de Bombeiro Militar", "abbr": "Cia. Ind. BM",
    },
    ("bifea", "pr"): {
        "finalidade": (
            "Grupo de Operações de Socorro Tático - GOST: equivalente a uma Companhia "
            "Independente de Bombeiro Militar - Cia. Ind. BM, subordinado diretamente ao "
            "Comandante-Geral, em apoio especializado às Unidades Operacionais, que é "
            "incumbido de"
        ),
        "competencias": [
            "executar a missão especializada de socorro tático em todas as atividades de "
            "bombeiro-militar",
            "realizar ações de atendimento às emergências ambientais e a sinistros "
            "decorrentes de desastres naturais e antropogênicos e ações de defesa civil",
            "organizar forças-tarefas",
            "desempenhar atividades de busca e salvamento, inclusive com a utilização de cães",
            "organizar e manter o canil central e coordenar os canis setoriais",
        ],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 38, III",
        "organName": "Grupo de Operações de Socorro Tático", "abbr": "GOST",
    },
    ("boa", "pr"): {
        "finalidade": (
            "Unidade de Operações Aéreas - UOA: subordinada diretamente ao "
            "Subcomandante-Geral, é encarregada de, com a utilização de aeronaves"
        ),
        "competencias": [
            "atender e apoiar ações de busca, resgate e salvamento a vítimas de acidentes "
            "e/ou traumas em áreas urbanas, rurais e rodovias",
            "atender e apoiar ações de busca e resgate de vítimas em matas, florestas, "
            "montanhas, rios, lagos e mar",
            "atuar em missões de apoio à defesa civil",
            "apoiar órgãos federais, estaduais e municipais que necessitem do emprego de "
            "aeronaves",
            "desempenhar outras missões de preservação da ordem pública",
        ],
        "source": "cf. CBMPR, LOB (Lei nº 22.206/2024), Art. 38, IV",
        "organName": "Unidade de Operações Aéreas", "abbr": "UOA",
    },

    # --- Rio de Janeiro (RJ) — Lei nº 250/1979, LOB antiga e fundacional do
    # CBERJ; finalidade-caput por órgão ("é o Órgão de Direção Setorial do
    # sistema..."), sem incisos enumerados na maior parte dos órgãos.
    ("cg", "rj"): {
        "finalidade": "O Comandante-Geral é responsável pelo Comando e pela Administração da Corporação",
        "competencias": [],
        "source": "cf. CBERJ, LOB (Lei nº 250/1979), Art. 9º",
        "organName": "Comandante-Geral", "abbr": "",
    },
    ("dp", "rj"): {
        "finalidade": (
            "A Diretoria de Pessoal é o Órgão de Direção Setorial do Sistema de Pessoal, "
            "incumbido do planejamento, execução, controle e fiscalização das atividades "
            "relacionadas com a classificação e movimentação de pessoal da ativa, cadastro e "
            "avaliação, direitos, deveres e incentivos, pessoal inativo e pensionistas, "
            "pessoal civil, seleção e ingresso e assistência social e religiosa"
        ),
        "competencias": [],
        "source": "cf. CBERJ, LOB (Lei nº 250/1979), Art. 19",
        "organName": "Diretoria de Pessoal", "abbr": "",
    },
    ("deei", "rj"): {
        "finalidade": (
            "A Diretoria de Ensino é o Órgão de Direção Setorial do sistema de Ensino, "
            "incumbido de planejamento, coordenação, fiscalização e controle das atividades "
            "de formação, aperfeiçoamento e especialização de oficiais e praças BM do Corpo e, "
            "eventualmente, de civis ou oficiais e praças de outras Corporações"
        ),
        "competencias": [],
        "source": "cf. CBERJ, LOB (Lei nº 250/1979), Art. 22",
        "organName": "Diretoria de Ensino", "abbr": "",
    },
    ("dpof", "rj"): {
        "finalidade": (
            "A Diretoria de Finanças é o Órgão de Direção Setorial do sistema Financeiro, "
            "incumbido de realizar as atividades específicas e assessorar o Comandante-Geral "
            "na supervisão das atividades financeiras dos Órgãos da Corporação e na "
            "distribuição de recursos orçamentários, de acordo com o planejamento estabelecido"
        ),
        "competencias": [],
        "source": "cf. CBERJ, LOB (Lei nº 250/1979), Art. 24",
        "organName": "Diretoria de Finanças", "abbr": "",
    },
    ("dlog", "rj"): {
        "finalidade": (
            "A Diretoria de Apoio Logístico é o Órgão de Direção Setorial do Sistema "
            "Logístico, incumbido do planejamento, coordenação, fiscalização e controle das "
            "necessidades de apoio de saúde, de suprimento e de manutenção; realizará essas "
            "mesmas atividades no que se refere a obras"
        ),
        "competencias": [],
        "source": "cf. CBERJ, LOB (Lei nº 250/1979), Art. 26",
        "organName": "Diretoria de Apoio Logístico", "abbr": "",
    },
    ("cot", "rj"): {
        "finalidade": (
            "A Diretoria de Serviços Técnicos é o Órgão de Direção Setorial do Sistema de "
            "Engenharia de Segurança, incumbido de estudar, analisar, planejar, exigir e "
            "fiscalizar as atividades atinentes à segurança contra incêndio e pânico, proceder "
            "a exame de plantas e a perícias; realizar testes de incombustibilidade; realizar "
            "vistorias e emitir pareceres com autoridade para notificar, multar e interditar, "
            "na forma da legislação específica"
        ),
        "competencias": [],
        "source": "cf. CBERJ, LOB (Lei nº 250/1979), Art. 28",
        "organName": "Diretoria de Serviços Técnicos", "abbr": "",
    },
    ("ag", "rj"): {
        "finalidade": (
            "A Ajudância-Geral tem a seu cargo as funções administrativas do Comando-Geral, "
            "considerada como uma Organização de Bombeiros-Militares (OBM), bem como algumas "
            "atividades de pessoal para a Corporação como um todo"
        ),
        "competencias": [],
        "source": "cf. CBERJ, LOB (Lei nº 250/1979), Art. 30",
        "organName": "Ajudância-Geral", "abbr": "",
    },
    ("assessorias", "rj"): {
        "finalidade": (
            "As Assessorias destinam-se a dar flexibilidade à estrutura do Comando-Geral da "
            "Corporação, particularmente em assuntos especializados que escapem às "
            "atribuições normais e específicas dos órgãos de direção"
        ),
        "competencias": [],
        "source": "cf. CBERJ, LOB (Lei nº 250/1979), Art. 33",
        "organName": "Assessorias", "abbr": "",
    },
    ("crbm", "rj"): {
        "finalidade": (
            "Os Comandos de Bombeiros da Área, diretamente subordinados ao Comando-Geral, são "
            "responsáveis pelo planejamento, supervisão e execução das missões específicas de "
            "bombeiro-militar, na respectiva área, de acordo com as diretrizes e ordens do "
            "Comando-Geral"
        ),
        "competencias": [],
        "source": "cf. CBERJ, LOB (Lei nº 250/1979), Art. 44, §1º",
        "organName": "Comando de Bombeiros de Área", "abbr": "CBA",
    },
    ("bbm", "rj"): {
        "finalidade": (
            "Unidade de Extinção de Incêndio Terrestre é a que tem a seu cargo, dentro da área "
            "do Estado do Rio de Janeiro, as missões de prevenção e combate a incêndios"
        ),
        "competencias": [],
        "source": "cf. CBERJ, LOB (Lei nº 250/1979), Art. 47, §1º",
        "organName": "Unidade de Extinção de Incêndio Terrestre", "abbr": "",
    },
    ("bbs", "rj"): {
        "finalidade": (
            "Unidades de Busca e Salvamento é a que tem a seu cargo, dentro da área do Estado "
            "do Rio de Janeiro, as missões de busca e salvamento, tanto terrestre, como "
            "aquática"
        ),
        "competencias": [],
        "source": "cf. CBERJ, LOB (Lei nº 250/1979), Art. 47, §2º",
        "organName": "Unidade de Busca e Salvamento", "abbr": "",
    },

    # --- Rio Grande do Norte (RN) — LC nº 230/2002 (alt. até LC 791/2025).
    # LOB sucinta: trata sobretudo de efetivo/quadros/transição da PM; só há
    # um órgão colegiado de direção descrito por finalidade própria (o
    # Conselho Superior, Art. 9º); não há Diretorias, EMG, nem demais órgãos
    # de execução com finalidade-caput na lei (estrutura é deixada a decreto,
    # Art. 20).
    ("condeg", "rn"): {
        "finalidade": (
            "O Conselho Superior do Corpo de Bombeiros Militar, órgão de deliberação "
            "coletiva, assessora o Comandante Geral na formulação e avaliação de políticas e "
            "estratégias e na fixação de diretrizes de gerenciamento administrativo e "
            "operacional do Corpo de Bombeiros Militar, além exercer a seguintes atribuições "
            "institucionais"
        ),
        "competencias": [
            "aprovar a proposta orçamentária do Corpo de Bombeiros Militar",
            "aprovar o relatório geral e anual do Corpo de Bombeiros Militar",
            "deliberar sobre qualquer matéria de interesse do Corpo de Bombeiros Militar, que "
            "lhe seja submetida por quaisquer de seus membros",
            "dirimir quaisquer dúvidas ou omissões atinentes à competência dos órgãos que "
            "integram o Corpo de Bombeiros Militar",
            "analisar regras, critérios e princípios para a realização de concurso público "
            "para ingresso nas carreiras de Oficiais e Praças da Instituição, propostas pelo "
            "Comandante Geral, observado o disposto em lei",
            "estabelecer o padrão dos símbolos do Corpo de Bombeiros Militar",
            "deliberar sobre os processos de promoção de Oficiais e Praças da Corporação",
            "gerenciar e estabelecer as diretrizes do Fundo de Reaparelhamento do Corpo de "
            "Bombeiros Militar (FUNREBOM)",
            "elaborar o seu regimento interno",
        ],
        "source": "cf. CBMRN, LOB (LC nº 230/2002), Art. 9º",
        "organName": "Conselho Superior do Corpo de Bombeiros Militar", "abbr": "",
    },

    # --- Roraíma (RR) — LC nº 52/2001 (consolidada até LC 791/2025... na
    # verdade até a LC 275/2018, conforme alterações registradas no
    # cabeçalho). LOB rica e detalhada, com estrutura em níveis (direção
    # superior, setorial, execução); usado o texto CONSOLIDADO (versão mais
    # recente de cada artigo alterado, não a redação original revogada).
    ("ag", "rr"): {
        "finalidade": (
            "A Ajudância Geral, subordinada diretamente ao Subcomandante Geral, considerada "
            "como OBM de suporte, tem a seu cargo as funções administrativas do Quartel do "
            "Comando Geral, inclusive, as de controle de todo o seu pessoal"
        ),
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001), Art. 21",
        "organName": "Ajudância Geral", "abbr": "",
    },
    ("corregedoria", "rr"): {
        "finalidade": (
            "A Corregedoria Geral, subordinada diretamente ao Comandante Geral, é o órgão de "
            "disciplina, orientação e fiscalização das atividades funcionais e da conduta dos "
            "servidores da instituição, competindo-lhe, dentre outras atribuições, a apuração "
            "de responsabilidade criminal, administrativa e disciplinar"
        ),
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001), Art. 20",
        "organName": "Corregedoria Geral", "abbr": "",
    },
    ("depdec", "rr"): {
        "finalidade": (
            "A Coordenadoria Estadual de Proteção e Defesa Civil – CEPDEC, é o órgão de "
            "direção geral, que centraliza o sistema Estadual de Proteção e Defesa Civil de "
            "Roraima e tem por finalidade estabelecer normas e o exercício das atividades de "
            "integrar, planejar, organizar, coordenar e supervisionar as execuções das "
            "medidas preventivas, de socorro, de assistência e de recuperação, considerando "
            "os efeitos produzidos por fatores adversos de qualquer natureza e origens nas "
            "situações de emergência ou estado de calamidade pública"
        ),
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001, red. LC nº 257/2017), Art. 24",
        "organName": "Coordenadoria Estadual de Proteção e Defesa Civil", "abbr": "CEPDEC",
    },
    ("cint", "rr"): {
        "finalidade": (
            "A Diretoria de Inteligência - DINT, subordinada diretamente ao Comandante Geral, "
            "é o órgão encarregado do exercício sistemático de ações especializadas voltadas "
            "para a obtenção, produção de dados, conhecimentos e salvaguarda destes visando "
            "assessorar o Comandante Geral no planejamento, acompanhamento e execução de "
            "políticas e atos decisórios, bem como na identificação, avaliação e neutralização "
            "de atividades de inteligência promovidas por serviços de inteligências de outros "
            "Órgãos"
        ),
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001, red. LC nº 257/2017), Art. 25-A",
        "organName": "Diretoria de Inteligência", "abbr": "DINT",
    },
    ("dp", "rr"): {
        "finalidade": "A Diretoria de Pessoal e Legislação tem a seguinte estrutura",
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001), Art. 29",
        "organName": "Diretoria de Pessoal e Legislação", "abbr": "DPL",
    },
    ("cinf", "rr"): {
        "finalidade": (
            "O Centro de Informática - CINFOR, órgão de apoio subordinado diretamente à "
            "Diretoria de Informática e Estatística - DIE, é dirigido por um comandante e "
            "destina-se a realizar programas e sistemas para otimização das áreas "
            "administrativas e operacionais da corporação"
        ),
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001, red. LC nº 257/2017), Art. 45",
        "organName": "Centro de Informática", "abbr": "CINFOR",
    },
    ("deei", "rr"): {
        "finalidade": "A Diretoria de Ensino, Instrução e Pesquisa tem a seguinte estrutura",
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001, red. LC nº 257/2017), Art. 31",
        "organName": "Diretoria de Ensino, Instrução e Pesquisa", "abbr": "DEIP",
    },
    ("dlog", "rr"): {
        "finalidade": "A Diretoria de Logística tem a seguinte estrutura",
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001, red. LC nº 265/2018), Art. 32",
        "organName": "Diretoria de Logística", "abbr": "DLOG",
    },
    ("cot", "rr"): {
        "finalidade": "Diretoria de Prevenção e Serviços Técnicos – DPST – tem a seguinte estrutura",
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001), Art. 33",
        "organName": "Diretoria de Prevenção e Serviços Técnicos", "abbr": "DPST",
    },
    ("ccs", "rr"): {
        "finalidade": "A Diretoria de Assuntos Civis e Relações Públicas tem a seguinte estrutura",
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001), Art. 34",
        "organName": "Diretoria de Assuntos Civis e Relações Públicas", "abbr": "DACRP",
    },
    ("dpof", "rr"): {
        "finalidade": "A Diretoria de Gestão Orçamentária e Financeira tem a seguinte estrutura",
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001), Art. 35",
        "organName": "Diretoria de Gestão Orçamentária e Financeira", "abbr": "DGOF",
    },
    ("dsap", "rr"): {
        "finalidade": (
            "O Centro de Saúde – CESAU, é um órgão de apoio de saúde e de assistência social, "
            "subordinado diretamente ao Ajudante Geral. É dirigido por um comandante e "
            "destina-se à prestação de serviços de saúde e assistência social"
        ),
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001), Art. 47",
        "organName": "Centro de Saúde", "abbr": "CESAU",
    },
    ("doe", "rr"): {
        "finalidade": (
            "O Comando Operacional da Capital e do Interior, subordinados diretamente ao "
            "Subcomandante Geral"
        ),
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001, red. LC nº 257/2017), Art. 37",
        "organName": "Comando Operacional", "abbr": "",
    },
    ("cat", "rr"): {
        "finalidade": (
            "O Centro de Investigação e Prevenção de Incêndios, órgão de apoio, subordinado "
            "diretamente à Diretoria de Prevenção e Serviços Técnicos - DPST, é dirigido por "
            "um comandante e destina-se a realizar serviços de prevenção, investigação, "
            "perícias de incêndios e explosões e a emitir conclusões e laudos técnicos "
            "periciais sobre suas atividades"
        ),
        "competencias": [],
        "source": "cf. CBMRR, LOB (LC nº 52/2001), Art. 46",
        "organName": "Centro de Investigação e Prevenção de Incêndios", "abbr": "CIPI",
    },

    # =====================================================================
    # Lote 5 — RS, SE, SP, TO (+ SC completo) (camada LOB /comparar, 2026-06-28)
    # =====================================================================

    # --- Rio Grande do Sul (CBMRS) — Decreto nº 53.897/2018 (regulamenta a LC nº 14.920/2016) ---
    # Decreto regulamentador enxuto (4 páginas): dá finalidade por artigo a cada órgão de
    # direção/apoio, mas remete a estrutura interna e as competências de detalhe das Divisões e
    # dos OBM ao Regimento Interno do CBMRS (não disponível no corpus). Sem incisos enumerados.
    ("cg", "rs"): {
        "finalidade": (
            "Ao Comando-Geral, órgão de direção-geral do CBMRS, compete a administração da "
            "Instituição, que será exercida diretamente pelo Comandante-Geral"
        ),
        "competencias": [],
        "source": "cf. CBMRS, LOB (Dec. nº 53.897/2018, regulamenta a LC nº 14.920/2016), Art. 4º",
        "organName": "Comando-Geral", "abbr": "",
    },
    ("gab-cg", "rs"): {
        "finalidade": (
            "Ao Gabinete do Comando-Geral compete a assistência e o assessoramento direto ao "
            "Comandante-Geral e ao Subcomandante-Geral"
        ),
        "competencias": [],
        "source": "cf. CBMRS, LOB (Dec. nº 53.897/2018, regulamenta a LC nº 14.920/2016), Art. 6º",
        "organName": "Gabinete do Comando-Geral", "abbr": "",
    },
    ("condeg", "rs"): {
        "finalidade": (
            "O Conselho Superior é constituído pelos Coronéis da ativa em exercício na "
            "Corporação, competindo-lhe, em assessoramento direto ao Comandante-Geral, o "
            "acompanhamento e a manifestação em assuntos relevantes da Instituição, com vista "
            "ao fornecimento de subsídios para a tomada de decisão"
        ),
        "competencias": [],
        "source": "cf. CBMRS, LOB (Dec. nº 53.897/2018, regulamenta a LC nº 14.920/2016), Art. 8º",
        "organName": "Conselho Superior", "abbr": "",
    },
    ("corregedoria", "rs"): {
        "finalidade": (
            "A Corregedoria-Geral, órgão de disciplina, de orientação e de fiscalização das "
            "atividades funcionais e da conduta dos militares e dos servidores civis da "
            "Instituição, subordina-se diretamente ao Comandante-Geral"
        ),
        "competencias": [],
        "source": "cf. CBMRS, LOB (Dec. nº 53.897/2018, regulamenta a LC nº 14.920/2016), Art. 9º",
        "organName": "Corregedoria-Geral", "abbr": "",
    },
    ("dlog", "rs"): {
        "finalidade": (
            "O Departamento Administrativo é o responsável pelo planejamento, controle, "
            "fiscalização, auditoria e execução das atividades relacionadas a recursos "
            "humanos, orçamento e finanças, logística e patrimônio e tecnologia da informação "
            "e comunicações"
        ),
        "competencias": [],
        "source": "cf. CBMRS, LOB (Dec. nº 53.897/2018, regulamenta a LC nº 14.920/2016), Art. 12",
        "organName": "Departamento Administrativo", "abbr": "",
    },
    ("cot", "rs"): {
        "finalidade": (
            "O Departamento de Segurança, Prevenção e Proteção Contra Incêndios é o órgão de "
            "planejamento, controle e fiscalização das atividades relacionadas à segurança "
            "contra incêndios e à investigação de sinistros em âmbito estadual"
        ),
        "competencias": [],
        "source": "cf. CBMRS, LOB (Dec. nº 53.897/2018, regulamenta a LC nº 14.920/2016), Art. 13",
        "organName": "Departamento de Segurança, Prevenção e Proteção Contra Incêndios", "abbr": "",
    },
    ("deei", "rs"): {
        "finalidade": (
            "A Academia de Bombeiro Militar é o órgão responsável pelo planejamento, controle "
            "e fiscalização das atividades relacionadas ao ensino, à saúde física do efetivo e "
            "à pesquisa científica da Instituição, bem como pela capacitação continuada dos "
            "servidores e dos profissionais civis que exerçam atividade auxiliar de bombeiro "
            "em âmbito estadual"
        ),
        "competencias": [],
        "source": "cf. CBMRS, LOB (Dec. nº 53.897/2018, regulamenta a LC nº 14.920/2016), Art. 14",
        "organName": "Academia de Bombeiro Militar", "abbr": "",
    },
    ("crbm", "rs"): {
        "finalidade": (
            "Os Comandos Regionais de Bombeiro Militar, escalões intermediários de comando, "
            "com nível de Órgãos de Apoio, são os responsáveis, em suas respectivas "
            "circunscrições territoriais, pelas atividades administrativo-operacionais dos "
            "Órgãos de Bombeiro Militar – OBM, que lhe são subordinados"
        ),
        "competencias": [],
        "source": "cf. CBMRS, LOB (Dec. nº 53.897/2018, regulamenta a LC nº 14.920/2016), Art. 15",
        "organName": "Comandos Regionais de Bombeiro Militar", "abbr": "",
    },
    ("bbm", "rs"): {
        "finalidade": (
            "Aos OBM de Segurança, de Proteção, de Prevenção e de Combate a Incêndios compete "
            "a execução das atividades de bombeiros e de defesa civil, no âmbito de seu "
            "espaço de responsabilidade territorial, respondendo perante o Comando Regional "
            "de Bombeiros pela realização de suas atividades na correspondente circunscrição"
        ),
        "competencias": [],
        "source": "cf. CBMRS, LOB (Dec. nº 53.897/2018, regulamenta a LC nº 14.920/2016), Art. 18",
        "organName": "Batalhão de Bombeiro Militar", "abbr": "BBM",
    },

    # --- Sergipe (CBMSE) — Lei nº 8.979/2022 ---
    # LOB que dá finalidade aos órgãos de direção estratégica/colegiada/geral/operacional, sem
    # incisos enumerados por órgão (incisos do Art. 2º são missões da Corporação, não de órgão
    # específico). A estrutura interna e competências de detalhe são remetidas ao Regimento
    # Interno do CBMSE (Art. 4º, parágrafo único).
    ("cg", "se"): {
        "finalidade": (
            "O Comando-Geral é órgão de Direção Estratégica do CBMSE, sendo responsável pela "
            "administração superior (comando), gestão, planejamento e condução estratégica da "
            "Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 5º",
        "organName": "Comando-Geral", "abbr": "",
    },
    ("condeg", "se"): {
        "finalidade": (
            "O Alto-Comando do CBMSE é o Órgão Colegiado Superior da instituição, de caráter "
            "consultivo, necessário ao processo decisório compartilhado da gestão estratégica "
            "do Corpo de Bombeiros Militar, a partir da provocação do Comandante-Geral"
        ),
        "competencias": [
            "propor políticas de segurança pública, em particular na parcela constitucional "
            "que cabe ao Corpo de Bombeiros Militar, e apresentar soluções para o "
            "aperfeiçoamento do sistema",
            "apresentar propostas e mudanças sobre matérias de cunho estratégico que promovam "
            "o aperfeiçoamento da instituição",
            "submeter matérias de relevância, relativas à Corporação, à superior decisão "
            "governamental",
            "apresentar propostas que alterem a estrutura organizacional da instituição e "
            "outros assuntos do interesse da Corporação",
        ],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 20",
        "organName": "Alto-Comando", "abbr": "",
    },
    ("gab-cg", "se"): {
        "finalidade": (
            "À Chefia de Gabinete compete o exercício das funções de assistência e "
            "assessoramento direto ao Comandante-Geral e ao Subcomandante-Geral, inerentes ao "
            "controle, coordenação e fiscalização das atividades administrativas desenvolvidas "
            "por militares e civis no âmbito dos Gabinetes do Comandante-Geral e do "
            "Subcomandante-Geral, da Ajudância de Ordens"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 12",
        "organName": "Gabinete (Chefia de Gabinete)", "abbr": "",
    },
    ("ag", "se"): {
        "finalidade": (
            "À Ajudância-Geral compete a administração do Quartel do Comando-Geral, "
            "considerado como Organização Bombeiro Militar, bem como do expediente, da "
            "execução dos trabalhos de secretaria, incluindo a correspondência, correio, "
            "redação do boletim diário, do protocolo e arquivo geral e biblioteca, do apoio "
            "em pessoal aos órgãos que compõem o Comando-Geral, dos serviços gerais, do "
            "Centro de Memória e da segurança do Quartel do Comando-Geral"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 14",
        "organName": "Ajudância-Geral", "abbr": "",
    },
    ("corregedoria", "se"): {
        "finalidade": (
            "A Corregedoria-Geral do Corpo de Bombeiros Militar é o órgão responsável pela "
            "sistematização e controle das atividades de correição funcional, de caráter "
            "disciplinar, administrativo ou de polícia judiciária militar"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 15",
        "organName": "Corregedoria-Geral", "abbr": "",
    },
    ("assessorias", "se"): {
        "finalidade": "As Assessorias são órgãos de assessoramento direto do Comando-Geral em assuntos específicos da Corporação",
        "competencias": [
            "Assessoria Técnica de Engenharia e Arquitetura",
            "Assessoria de Inteligência",
            "Assessoria Técnica Institucional",
            "Assessoria de Comunicação",
            "Assessoria de Tecnologia da Informação",
            "Assessoria Parlamentar",
        ],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 18",
        "organName": "Assessorias", "abbr": "",
    },
    ("dlog", "se"): {
        "finalidade": (
            "A Diretoria de Logística - DLOG é responsável pela gestão, planejamento, "
            "coordenação, execução, fiscalização e controle das atividades relacionadas à "
            "logística e patrimônio do CBMSE"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 23",
        "organName": "Diretoria de Logística", "abbr": "DLOG",
    },
    ("dpof", "se"): {
        "finalidade": (
            "A Diretoria Financeira - DFIN é responsável pela gestão, planejamento, "
            "coordenação, execução, fiscalização e controle das atividades do sistema de "
            "administração financeira e contábil do CBMSE"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 24",
        "organName": "Diretoria Financeira", "abbr": "DFIN",
    },
    ("dp", "se"): {
        "finalidade": (
            "A Diretoria de Gestão de Pessoal - DGP é responsável pela gestão, planejamento, "
            "coordenação, execução, fiscalização e controle das atividades relativas à gestão "
            "de pessoal e desenvolvimento de recursos humanos do CBMSE"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 25",
        "organName": "Diretoria de Gestão de Pessoal", "abbr": "DGP",
    },
    ("deei", "se"): {
        "finalidade": (
            "A Diretoria de Ensino e Pesquisa - DEP é responsável pela gestão, planejamento, "
            "coordenação, execução, fiscalização e controle das atividades referentes ao "
            "ensino, fomentando a pesquisa e viabilizando a instrução continuada dos quadros "
            "no âmbito do CBMSE"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 26",
        "organName": "Diretoria de Ensino e Pesquisa", "abbr": "DEP",
    },
    ("dpo", "se"): {
        "finalidade": (
            "A Diretoria de Planejamento - DPLAN é responsável pela gestão, planejamento das "
            "políticas públicas e estratégias institucionais, orientação e execução da "
            "programação orçamentária, consolidação dos planos, programas e projetos e "
            "acompanhamento e avaliação das ações governamentais, no âmbito do CBMSE"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 27",
        "organName": "Diretoria de Planejamento", "abbr": "DPLAN",
    },
    ("cot", "se"): {
        "finalidade": (
            "A Diretoria de Atividades Técnicas - DAT é responsável pela gestão, planejamento, "
            "coordenação, execução, fiscalização e controle de todas as atividades "
            "concernentes à segurança contra incêndio e pânico das instalações, edificações e "
            "locais de risco, no âmbito do Estado de Sergipe"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 29",
        "organName": "Diretoria de Atividades Técnicas", "abbr": "DAT",
    },
    ("doe", "se"): {
        "finalidade": (
            "A Diretoria Operacional - DOP é responsável pela gestão, planejamento, "
            "coordenação, execução, fiscalização e controle das atividades operacionais e na "
            "execução das atividades de proteção e defesa civil, sendo responsável pela "
            "coordenação e emprego dos Comandos Regionais e Unidades Operacionais, que lhes "
            "são subordinadas"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 30",
        "organName": "Diretoria Operacional", "abbr": "DOP",
    },
    ("crbm", "se"): {
        "finalidade": (
            "Os Comandos Regionais Bombeiro Militar - CRBM subordinam-se à DOP e são órgãos de "
            "supervisão, coordenação e planejamento operacional das unidades subordinadas"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 35",
        "organName": "Comandos Regionais Bombeiro Militar", "abbr": "CRBM",
    },
    ("gbm", "se"): {
        "finalidade": (
            "As Unidades, também denominadas de Grupamentos, realizam a execução das "
            "atividades operacionais e de apoio da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 36",
        "organName": "Grupamento Bombeiro Militar", "abbr": "GBM",
    },
    ("bbs", "se"): {
        "finalidade": "São Grupamentos Especializados do CBMSE o Grupamento de Busca e Salvamento - GBS e o Grupamento de Operações Aéreas - GOA",
        "competencias": [],
        "source": "cf. CBMSE, LOB (Lei nº 8.979/2022), Art. 39",
        "organName": "Grupamento de Busca e Salvamento", "abbr": "GBS",
    },

    # --- São Paulo (CBPMESP) — Lei nº 616/1974 (LOB da Polícia Militar; Corpo de Bombeiros é a
    # Seção II, Arts. 38 a 43, integrado à PM) ---
    # LOB é da Polícia Militar do Estado de São Paulo como um todo; o Corpo de Bombeiros é
    # subordinado ao Comando Geral da PM como órgão de execução (Art. 9º). (cg) usa o Comando do
    # Corpo de Bombeiros (Art. 39), órgão equivalente ao Comando-Geral do CBMRO dentro da PM-SP.
    # Os demais órgãos de direção/apoio (Estado Maior, Diretorias, Ajudância) são da PM como um
    # todo, não exclusivos do Corpo de Bombeiros; mantidos como camada de referência por serem o
    # nível hierárquico equivalente na estrutura da Corporação à qual o CB está integrado.
    ("cg", "sp"): {
        "finalidade": (
            "O Comando do Corpo de Bombeiros da Polícia Militar é o órgão responsável perante "
            "o Comando Geral, pelo planejamento, comando, execução, coordenação, fiscalização "
            "e controle de todas as atividades de prevenção, extinção de incêndios e de buscas "
            "e salvamentos, bem como das atividades técnicas a elas relacionadas no território "
            "estadual"
        ),
        "competencias": [],
        "source": "cf. CBPMESP, LOB (Lei nº 616/1974), Art. 39",
        "organName": "Comando do Corpo de Bombeiros", "abbr": "CB",
    },
    ("dp", "sp"): {
        "finalidade": (
            "A Diretoria de Pessoal (DP) é o órgão de direção setorial do sistema de "
            "administração de pessoal, incumbindo-lhe o planejamento, execução, controle e "
            "fiscalização das atividades relacionadas com alistamento, assistência social, "
            "classificação e movimentação do pessoal, promoções, inativos e pensionistas "
            "cadastro e avaliação, direitos, deveres e incentivos e pessoal civil"
        ),
        "competencias": [],
        "source": "cf. CBPMESP, LOB (Lei nº 616/1974), Art. 16",
        "organName": "Diretoria de Pessoal", "abbr": "DP",
    },
    ("dpof", "sp"): {
        "finalidade": (
            "A Diretoria de Finanças (DF) é o órgão de direção setorial do sistema de "
            "administração financeira atuando, também, como órgão de apoio na supervisão do "
            "Comandante Geral sobre as atividades financeiras de todo e qualquer órgão da "
            "Corporação e na distribuição de recursos orçamentários e extraordinários aos "
            "responsáveis pelas despesas, de acordo com o planejamento estabelecido"
        ),
        "competencias": [],
        "source": "cf. CBPMESP, LOB (Lei nº 616/1974), Art. 14",
        "organName": "Diretoria de Finanças", "abbr": "DF",
    },
    ("dlog", "sp"): {
        "finalidade": (
            "A Diretoria de Apoio Logístico (DAL) é o órgão de direção setorial do sistema de "
            "administração de logística, incumbindo-lhe o planejamento, coordenação, "
            "fiscalização e controle das atividades de suprimento e manutenção de material à "
            "Corporação, inclusive a de saúde"
        ),
        "competencias": [],
        "source": "cf. CBPMESP, LOB (Lei nº 616/1974), Art. 15",
        "organName": "Diretoria de Apoio Logístico", "abbr": "DAL",
    },
    ("deei", "sp"): {
        "finalidade": (
            "À Diretoria de Ensino (DE), órgão de direção setorial do sistema de administração "
            "de ensino, incumbe o planejamento, coordenação, fiscalização e controle das "
            "atividades de formação, aperfeiçoamento e especialização de oficiais e praças"
        ),
        "competencias": [],
        "source": "cf. CBPMESP, LOB (Lei nº 616/1974), Art. 17",
        "organName": "Diretoria de Ensino", "abbr": "DE",
    },
    ("dsap", "sp"): {
        "finalidade": (
            "À Diretoria de Saúde (DS) órgão de direção setorial do sistema de administração "
            "de saúde, incumbe o planejamento, execução, controle e fiscalização de todas as "
            "atividades relacionadas à saúde do pessoal da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBPMESP, LOB (Lei nº 616/1974), Art. 18",
        "organName": "Diretoria de Saúde", "abbr": "DS",
    },
    ("ag", "sp"): {
        "finalidade": (
            "A Ajudância Geral (AG) tem a seu cargo as funções de apoio administrativo de "
            "atividades do Comando Geral, e de apoio em serviços e segurança do Quartel do "
            "mesmo Comando"
        ),
        "competencias": [],
        "source": "cf. CBPMESP, LOB (Lei nº 616/1974), Art. 19",
        "organName": "Ajudância Geral", "abbr": "AG",
    },
    ("bbm", "sp"): {
        "finalidade": (
            "Grupamentos de Incêndio (GI): unidades diretamente subordinadas ao Comando do "
            "Corpo de Bombeiros, incumbidas de missão de extinção de incêndios, podendo "
            "integrar missões de busca e salvamento"
        ),
        "competencias": [],
        "source": "cf. CBPMESP, LOB (Lei nº 616/1974), Art. 41, I",
        "organName": "Grupamento de Incêndio", "abbr": "GI",
    },
    ("bbs", "sp"): {
        "finalidade": (
            "Grupamentos de Busca e Salvamento (GBS): unidades diretamente subordinadas ao "
            "Comando de Corpo de Bombeiros, incumbidas da missão de busca e salvamento, de "
            "modo especial, em razão da extensão da missão"
        ),
        "competencias": [],
        "source": "cf. CBPMESP, LOB (Lei nº 616/1974), Art. 41, III",
        "organName": "Grupamento de Busca e Salvamento", "abbr": "GBS",
    },

    # --- Tocantins (CBMTO) — Lei Complementar nº 131/2021 ---
    # LOB moderna por "Unidades Administrativas" (Direção Superior/Setorial/Assessoramento
    # Geral/Apoio/Execução); dá finalidade/competência por artigo, em sua maioria sem incisos
    # (exceto Comando de Correição e Disciplina, Art. 12, e Assessoria de Inteligência, Art. 19).
    ("cg", "to"): {
        "finalidade": (
            "O Comandante-Geral, Secretário de Estado, nomeado por ato do Chefe do Poder "
            "Executivo, é responsável pelo comando, administração e emprego da Corporação e "
            "do Comando de Ações de Defesa Civil, assessorado pelas demais unidades "
            "administrativas, que lhe são subordinadas"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 7º",
        "organName": "Comandante-Geral", "abbr": "CG",
    },
    ("gab-cg", "to"): {
        "finalidade": "O Gabinete do Comandante-Geral tem atribuição de transmissão e controle da execução das ordens emanadas do Comandante-Geral",
        "competencias": [
            "organização da correspondência e despacho da documentação do Gabinete",
            "ajudância de ordens",
            "secretariado geral do Comandante-Geral e do Chefe do Estado-Maior",
            "publicação do Boletim Geral",
        ],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 19, VI",
        "organName": "Gabinete do Comandante-Geral", "abbr": "",
    },
    ("corregedoria", "to"): {
        "finalidade": "O Comando de Correição e Disciplina é encarregado de garantir a preservação dos princípios da hierarquia e disciplina da Corporação",
        "competencias": [
            "controlar, orientar e padronizar processos administrativos disciplinares e "
            "Inquéritos Policiais Militares",
            "apurar transgressões disciplinares e infrações penais de natureza militar "
            "envolvendo seus membros",
            "acompanhar pessoal submetido a processo penal e processo penal militar",
        ],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 12",
        "organName": "Comando de Correição e Disciplina", "abbr": "",
    },
    ("depdec", "to"): {
        "finalidade": (
            "O Comando de Ações de Defesa Civil é responsável pelo planejamento e coordenação "
            "das ações de prevenção, preparação e resposta no âmbito da defesa civil"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 13",
        "organName": "Comando de Ações de Defesa Civil", "abbr": "",
    },
    ("dp", "to"): {
        "finalidade": (
            "O Comando de Gestão de Pessoas é encarregado do planejamento e dos assuntos "
            "estratégicos referentes à gestão profissional, à legislação, ao pessoal, à saúde "
            "e ao ensino na Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 14",
        "organName": "Comando de Gestão de Pessoas", "abbr": "",
    },
    ("dpof", "to"): {
        "finalidade": (
            "O Comando de Gestão de Recursos Financeiros e Patrimoniais é responsável pelo "
            "planejamento dos assuntos referentes ao orçamento, finanças, logística e "
            "infraestrutura da Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 15",
        "organName": "Comando de Gestão de Recursos Financeiros e Patrimoniais", "abbr": "",
    },
    ("cot", "to"): {
        "finalidade": (
            "O Comando de Atividades Técnicas é encarregado de planejar, controlar e "
            "fiscalizar as atividades atinentes à segurança contra incêndio e emergência no "
            "Estado"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 16",
        "organName": "Comando de Atividades Técnicas", "abbr": "",
    },
    ("dpo", "to"): {
        "finalidade": (
            "O Comando Operacional Bombeiro Militar é responsável pelo planejamento dos "
            "assuntos relativos à articulação operacional, à administração e ao controle das "
            "operações bombeiro militares e pelos estudos, estatísticas, doutrinas, pesquisas "
            "e padronização de procedimentos relacionados às atividades operacionais da "
            "Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 17",
        "organName": "Comando Operacional Bombeiro Militar", "abbr": "",
    },
    ("cint", "to"): {
        "finalidade": "A Assessoria de Inteligência é encarregada dos assuntos relativos à inteligência e contrainteligência",
        "competencias": [
            "a guarda e manutenção de documentos e arquivos sigilosos",
            "o controle de armamento dos integrantes da Corporação",
            "a confecção do boletim reservado da Corporação",
            "o secretariado da Comissão de Promoções de Oficiais - CPO e Comissão de Promoção "
            "de Praças – CPP",
        ],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 19, I",
        "organName": "Assessoria de Inteligência", "abbr": "",
    },
    ("assessorias", "to"): {
        "finalidade": "A Assessoria Jurídica tem atribuições de consultoria, análise e emissão de pareceres jurídicos nos processos e assuntos de interesse da Corporação",
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 19, II",
        "organName": "Assessoria Jurídica", "abbr": "",
    },
    ("ccs", "to"): {
        "finalidade": (
            "A Assessoria de Comunicação Social é encarregada das atividades de comunicação "
            "social, publicidade, relacionamento com a mídia, cerimonial, eventos e marketing "
            "institucional"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 19, III",
        "organName": "Assessoria de Comunicação Social", "abbr": "",
    },
    ("cinf", "to"): {
        "finalidade": (
            "A Assessoria de Telecomunicações e Informática é responsável pela coordenação e "
            "execução das matérias relativas à informática, telecomunicações e tecnologia da "
            "informação"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 19, V",
        "organName": "Assessoria de Telecomunicações e Informática", "abbr": "",
    },
    ("dsap", "to"): {
        "finalidade": (
            "A Diretoria de Saúde e Assistência Social, subordinada ao Comando de Gestão de "
            "Pessoas, responsável pela coordenação, execução e acompanhamento dos assuntos "
            "relativos aos serviços de saúde e à promoção social dos bombeiros militares, seus "
            "dependentes e pensionistas"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 18, V",
        "organName": "Diretoria de Saúde e Assistência Social", "abbr": "",
    },
    ("deei", "to"): {
        "finalidade": (
            "Diretoria de Ensino e Pesquisa, subordinada ao Comando de Gestão de Pessoas, "
            "encarregada de assuntos relativos à coordenação e execução do ensino, instrução e "
            "pesquisa, inerentes às atividades de bombeiro militar"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 18, II",
        "organName": "Diretoria de Ensino e Pesquisa", "abbr": "DEP",
    },
    ("dlog", "to"): {
        "finalidade": (
            "Diretoria de Logística e Patrimônio, subordinada ao Comando de Gestão de "
            "Recursos Financeiros e Patrimoniais, responsável pelos assuntos relativos à "
            "aquisição de material e serviços, logística geral, e ao controle e fiscalização "
            "do patrimônio e estoque"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 18, III",
        "organName": "Diretoria de Logística e Patrimônio", "abbr": "",
    },
    ("ag", "to"): {
        "finalidade": (
            "Ajudância Geral, subordinada ao Comandante-Geral, encarregada dos assuntos "
            "administrativos de segurança e manutenção das instalações físicas do Quartel do "
            "Comando Geral, considerado como Organização Bombeiro Militar - OBM e de apoio às "
            "unidades do Comando-Geral com pessoal auxiliar"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 21, I",
        "organName": "Ajudância Geral", "abbr": "",
    },
    ("bbm", "to"): {
        "finalidade": (
            "As Unidades Administrativas de Execução, subordinadas ao Comando Operacional, "
            "são constituídas por Unidades Bombeiro Militares - UBM, encarregadas de executar "
            "as atividades-fim da Corporação em determinada área, conforme Plano de "
            "Articulação do CBMTO, podendo ser divididas em subunidades"
        ),
        "competencias": [],
        "source": "cf. CBMTO, LOB (LC nº 131/2021), Art. 24",
        "organName": "Unidade Bombeiro Militar", "abbr": "UBM",
    },

    # --- Santa Catarina (CBMSC) — Decreto nº 1.328/2021 (completa as entradas dp/sc e cg/sc já
    # existentes na amostra inicial) ---
    # Decreto regulamenta a LC nº 724/2018; dá finalidade e incisos detalhados (estrutura
    # "DOS ÓRGÃOS DE DIREÇÃO/APOIO/EXECUÇÃO" no Título III). Sem equivalente RO para Conselho
    # Estratégico (mapeado em condeg), Agência Central de Inteligência (cint) e Coordenadorias
    # Operacionais (sem chave própria, descartada — grupo de trabalho consultivo genérico).
    ("corregedoria", "sc"): {
        "finalidade": "São atribuições da Corregedoria-Geral:",
        "competencias": [
            "promover o acompanhamento das apurações de transgressões disciplinares e ilícitos "
            "penais atribuídos a bombeiros militares, realizadas pelos órgãos de direção, de "
            "apoio, e de execução do CBMSC, avocando-as quando necessário",
            "promover integração com os órgãos do Poder Judiciário, Ministério Público, "
            "Defensoria Pública e corregedorias de outros órgãos, nos temas relacionados a "
            "suas atribuições",
            "baixar normas técnicas em conjunto com Estado-Maior Geral, relativas às "
            "atividades de sua competência e controlar a sua aplicação",
            "gerenciar o sistema de corregedoria do CBMSC",
            "manter cópia digitalizada dos procedimentos disciplinares e penais que forem "
            "instaurados no CBMSC",
            "efetuar investigações, levantamentos externos ou diligências em conjunto com a "
            "Agência Central de Inteligência, para proveito das apurações das infrações "
            "penais militares e transgressões disciplinares e sua autoria, imputada a "
            "bombeiros militares",
            "elaborar estatísticas relativas às suas atividades",
            "remeter, com exclusividade, à Justiça Militar, os Inquéritos Policiais Militares, "
            "Sindicâncias e outros processos que tenham relação com a apuração no âmbito "
            "criminal, concernentes a atos praticados por integrantes do CBMSC",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 33",
        "organName": "Corregedoria-Geral", "abbr": "",
    },
    ("condeg", "sc"): {
        "finalidade": (
            "O Conselho Estratégico é um órgão de direção geral do Comando-Geral do CBMSC, "
            "tendo as seguintes atribuições"
        ),
        "competencias": [
            "prestar assistência ao Comando-Geral no desempenho das atividades relacionadas "
            "com a execução do planejamento estratégico da Corporação, auxiliando no processo "
            "de tomada de decisão",
            "colaborar na elaboração de planos e ordens do Comando-Geral relacionados com "
            "pessoal, informações, instrução, operações, ensino, assuntos administrativos, "
            "assuntos civis, planejamento administrativo, programação e orçamento",
            "desenvolver outras atividades de interesse ou determinadas pelo Comando-Geral da "
            "Corporação",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 30",
        "organName": "Conselho Estratégico", "abbr": "",
    },
    ("ag", "sc"): {
        "finalidade": (
            "A Ajudância-Geral é o órgão de direção que exerce as funções de assistência e "
            "assessoramento direto ao Comandante-Geral na prática de atos de gestão e nos "
            "assuntos que extrapolem às atribuições normais e específicas dos demais órgãos de "
            "direção"
        ),
        "competencias": [
            "desenvolver os trabalhos de secretaria e de documentações inerentes ao "
            "Comandante-Geral",
            "administrar e executar a atividade de protocolo geral da Corporação e propor a "
            "normatização do serviço para os demais órgãos",
            "receber e registrar a correspondência oficial, petições, processos, documentos e "
            "quaisquer expedientes endereçados ao Comando-Geral",
            "promover o controle dos atos administrativos assinados pelo Comandante-Geral",
            "administrar o arquivo geral da Corporação e propor a normatização do serviço para "
            "os demais órgãos",
            "planejar, organizar e dirigir os serviços de segurança interna e externa do "
            "Quartel do Comando-Geral",
            "administrar o serviço geral do Quartel do Comando-Geral",
            "publicar e distribuir o Boletim do CBMSC",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 27, § 1º",
        "organName": "Ajudância-Geral", "abbr": "",
    },
    ("assessorias", "sc"): {
        "finalidade": (
            "A Assessoria Jurídica, chefiada por oficial superior da ativa com formação em "
            "Direito, tem por finalidade prestar assistência jurídica ao Comandante-Geral, "
            "cabendo-lhe"
        ),
        "competencias": [
            "programar, organizar, orientar, coordenar, executar e controlar as atividades "
            "relacionadas com os serviços jurídicos, no âmbito do CBMSC, vinculando-se "
            "tecnicamente à Consultoria Jurídica da SSP e à Procuradoria-Geral do Estado (PGE)",
            "examinar a legalidade dos atos administrativos que lhe forem submetidos à "
            "apreciação pelo Comandante-Geral, Subcomandante-Geral e Chefe do Estado-Maior "
            "Geral",
            "participar do processo legislativo de elaboração de anteprojetos de LEI e "
            "DECRETO relacionados às atividades do CBMSC",
            "coordenar a elaboração de informações em mandados de segurança e habeas corpus "
            "do Comandante-Geral, do Subcomandante-Geral e do Chefe do Estado-Maior Geral, "
            "sendo as informações inerentes às demais autoridades coatoras a cargo de suas "
            "assessorias ou corregedorias setoriais",
            "requisitar de quaisquer órgãos ou entidades da Corporação, documentos ou "
            "informações necessários ao exame de matéria jurídica a ele submetida, devendo os "
            "consultados atender no prazo estipulado pela Assessoria Jurídica",
            "apreciar editais de concurso e processos seletivos de pessoal",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 32",
        "organName": "Assessoria Jurídica", "abbr": "",
    },
    ("ccs", "sc"): {
        "finalidade": (
            "O Centro de Comunicação Social do CBMSC é responsável por assessorar diretamente "
            "o Comandante-Geral, promovendo a construção e manutenção da opinião pública "
            "relacionada à Corporação, de modo a coordenar, controlar, e orientar em nível "
            "estratégico, todas as ações de marketing institucional, a fim de preservar e "
            "fortalecer a imagem do CBMSC, empregando todos os meios disponíveis em prol da "
            "credibilidade, confiança e prestígio institucionais, tendo as seguintes "
            "atribuições"
        ),
        "competencias": [
            "planejar, desenvolver, coordenar e executar as atividades de comunicação social "
            "do CBMSC",
            "assessorar o Comandante-Geral nos aspectos relacionados à imprensa, divulgação "
            "institucional e conscientização social",
            "desenvolver e propor políticas de relacionamento da Corporação com órgãos e "
            "entidades públicas e privadas, com profissionais da Corporação e com a população",
            "divulgar as atividades desenvolvidas pelo CBMSC por meio dos diversos veículos de "
            "comunicação social",
            "manter o Comandante-Geral informado sobre fatos de interesse do CBMSC, quando "
            "veiculados pela imprensa",
            "regular, planejar, coordenar e executar o cerimonial militar e o cerimonial das "
            "atividades sociais de interesse do Comando-Geral frequentes e aqueles "
            "extraordinários determinados pelo Comandante-Geral",
            "promover a imagem institucional e mercadológica do CBMSC nos ambientes sociais e "
            "de segurança pública",
            "possibilitar a elaboração de respostas coordenadas, articuladas, adequadas e "
            "oportunas, aos questionamentos da sociedade e do cidadão, sobre assuntos de "
            "interesse da Instituição",
            "coordenar as ações dos elementos subordinados em seus relacionamentos com outros "
            "órgãos de comunicação, que exijam, pela natureza da pauta, articulação interna e "
            "participação coordenada",
            "assessorar e supervisionar o conteúdo de comunicação social no âmbito da "
            "Corporação",
            "administrar os canais de comunicação oficiais da Corporação e monitorar os "
            "canais de comunicação em nível dos elementos subordinados",
            "acompanhar, analisar e informar o Comando-Geral a repercussão na sociedade das "
            "mídias utilizadas pela Corporação",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 28",
        "organName": "Centro de Comunicação Social", "abbr": "",
    },
    ("deei", "sc"): {
        "finalidade": (
            "A Diretoria de Instrução e Ensino, órgão de direção setorial do CBMSC, é "
            "responsável pela inovação, planejamento, coordenação, acompanhamento, "
            "fiscalização, controle e avaliação das seguintes atividades: formação, "
            "aperfeiçoamento, especialização, capacitação, treinamento, instrução, pesquisa, "
            "extensão e projetos de interesse institucional, com intuito de promover a "
            "excelência e a evolução sustentada nos processos de ensino, de aprendizagem e de "
            "gestão do conhecimento na educação corporativa do CBMSC"
        ),
        "competencias": [],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 35",
        "organName": "Diretoria de Instrução e Ensino", "abbr": "",
    },
    ("dsap", "sc"): {
        "finalidade": (
            "A Diretoria de Urgência e Emergência, órgão de direção setorial, incumbe-se de "
            "fomentar, estudar, analisar, planejar, pesquisar, normatizar, controlar, prestar "
            "assessoramento técnico e executar projetos estratégicos de atendimento "
            "pré-hospitalar e integração com o sistema de saúde"
        ),
        "competencias": [],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 36",
        "organName": "Diretoria de Urgência e Emergência", "abbr": "",
    },
    ("dlog", "sc"): {
        "finalidade": (
            "A Diretoria de Logística e Finanças, órgão de direção setorial, responsável pelo "
            "planejamento, coordenação, fiscalização, controle das atividades de logística, "
            "de patrimônio, de tecnologia da informação e de serviços de comunicação da "
            "Corporação"
        ),
        "competencias": [],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 37",
        "organName": "Diretoria de Logística e Finanças", "abbr": "",
    },
    ("cot", "sc"): {
        "finalidade": (
            "A Diretoria de Segurança Contra Incêndio, órgão de direção setorial, é "
            "responsável por inovar, planejar, coordenar, fiscalizar, acompanhar e controlar "
            "as atividades relacionadas com"
        ),
        "competencias": [
            "a normatização em segurança contra incêndio, pânico e desastre",
            "a análise de projetos e vistorias",
            "o exercício do Poder de Polícia Administrativa",
            "a investigação de incêndio e explosão",
            "a pesquisa e desenvolvimento em segurança contra incêndio, pânico e desastre",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 38",
        "organName": "Diretoria de Segurança Contra Incêndio", "abbr": "",
    },
    ("crbm", "sc"): {
        "finalidade": (
            "Os Comandos Regionais, órgãos de direção operacional, responsáveis por "
            "fiscalizar, planejar, controlar, supervisionar e coordenar as atividades das "
            "unidades operacionais subordinadas, bem como pela gestão da própria sede, têm as "
            "seguintes atribuições"
        ),
        "competencias": [
            "inspecionar periodicamente as Organizações Bombeiro Militar subordinadas",
            "coordenar, controlar, fiscalizar e apoiar as ações operacionais que ultrapassem a "
            "circunscrição ou a esfera de competência do comando da unidade operacional "
            "subordinada",
            "supervisionar a gestão de convênios, fundos municipais e instrumentos congêneres "
            "no âmbito da circunscrição",
            "orientar e acompanhar o desempenho administrativo e operacional dos elementos "
            "subordinados por meio de ações de comando e de ferramentas sistêmicas, visando o "
            "aprimoramento de resultados, em consonância com o Plano Estratégico do CBMSC",
            "fiscalizar, na circunscrição da RBM, a gestão das Centrais de Emergências e "
            "congêneres",
            "emitir ordens administrativas e operacionais visando regular as ações de "
            "coordenação, controle e fiscalização sobre os órgãos de execução de sua "
            "circunscrição",
            "instaurar inquéritos, sindicâncias e outros procedimentos administrativos "
            "pertinentes à manutenção da disciplina no âmbito dos Comandos Regionais",
            "definir o emprego de Força-Tarefa, de acordo com as diretrizes do Comando-Geral "
            "do CBMSC, no âmbito de sua respectiva circunscrição",
            "autorizar deslocamentos dos seus subordinados a serviço e dentro do território "
            "estadual",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 39",
        "organName": "Comandos Regionais (RBM)", "abbr": "",
    },
    ("cint", "sc"): {
        "finalidade": (
            "A Agência Central de Inteligência, órgão de apoio do CBMSC, tem por "
            "responsabilidade planejar, coordenar, executar, fiscalizar, controlar, articular, "
            "supervisionar e gerenciar as atividades de inteligência e tem as seguintes "
            "atribuições"
        ),
        "competencias": [
            "supervisionar e coordenar, em todo o território do Estado, a atividade de "
            "inteligência",
            "definir bases para o estabelecimento da doutrina da atividade de inteligência",
            "elaborar os planos de inteligência e de busca",
            "produzir conhecimentos necessários às decisões do Comandante-Geral, bem como aos "
            "estudos e planejamentos em nível de Estado-Maior Geral",
            "promover e coordenar o intercâmbio de informações entre as Agências Setoriais de "
            "Inteligência do CBMSC",
            "estabelecer o relacionamento e ligações com os órgãos federais e estaduais de "
            "inteligência, assegurando o intercâmbio de conhecimentos",
            "coordenar operações de inteligência em todo território do Estado",
            "promover a formação de uma correta mentalidade de inteligência",
            "organizar e manter em dia os arquivos sigilosos, bem como controlar o fluxo de "
            "documentos sigilosos do CBMSC",
            "elaborar e controlar a expedição dos boletins reservados do Comando-Geral",
            "outras atribuições correlatas ou que vierem a ser cometidas à Agência Central de "
            "Inteligência",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 42",
        "organName": "Agência Central de Inteligência", "abbr": "",
    },
    ("bbm", "sc"): {
        "finalidade": (
            "Os BBMs, órgãos de execução, subordinados às RBMs, são responsáveis por planejar, "
            "orientar, coordenar, executar, acompanhar, controlar e supervisionar as "
            "atividades inerentes às missões do CBMSC, em sua circunscrição, têm como "
            "atribuições"
        ),
        "competencias": [
            "realizar os serviços de segurança, prevenção, proteção e combate a incêndios",
            "realizar os serviços de busca e salvamento de pessoas e bens, por meio de "
            "resgates aéreo, aquático e terrestre",
            "realizar o atendimento pré-hospitalar, respeitadas as competências de outros "
            "órgãos",
            "executar a prevenção balneária por guarda-vidas e a prevenção de acidentes e "
            "incêndios na orla marítima e fluvial",
            "analisar previamente os projetos preventivos, acompanhar e fiscalizar sua "
            "execução e impor sanções administrativas estabelecidas em LEI em segurança "
            "contra incêndio e pânico em imóveis e áreas de risco e de armazenagem, "
            "manipulação e transporte de produtos perigosos",
            "credenciar e fiscalizar o funcionamento dos serviços civis auxiliares de "
            "bombeiros",
            "desenvolver atividades relacionadas à educação pública, com foco na criação de "
            "uma cultura preventiva e reativa na comunidade, abrangendo o rol de atendimentos "
            "prestados pela Corporação e em conformidade com a política de capacitação do "
            "público externo",
            "realizar investigação de incêndio e explosão de áreas sinistradas no limite de "
            "sua competência",
            "atuar de forma integrada com os órgãos de defesa civil",
            "outras atividades regularmente previstas, bem como outras necessárias para a "
            "consecução das atividades da Corporação",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 51",
        "organName": "Batalhão Bombeiro Militar", "abbr": "BBM",
    },
    ("boa", "sc"): {
        "finalidade": (
            "O Batalhão Bombeiro Militar de Operações Aéreas, órgão de execução do CBMSC, "
            "responsável por planejar, orientar, coordenar, executar, acompanhar, controlar e "
            "supervisionar as atividades aéreas, tem as seguintes atribuições"
        ),
        "competencias": [
            "realizar atividades de resgate e transporte aeromédico especializado, combate a "
            "incêndios, busca e salvamento, atendimento pré-hospitalar, prevenção, proteção ao "
            "meio ambiente, defesa civil, e apoio aos demais Órgãos do Estado, Municípios e "
            "União com a utilização de suas aeronaves",
            "assessorar o Comando do CBMSC para os assuntos referentes à utilização, "
            "aquisição, implementação e emprego de aeronaves em todo o território catarinense",
            "atuar na capacitação e aperfeiçoamento técnico de sua tripulação",
            "propor doutrinas e normatizações afetas à área de aviação e segurança "
            "operacional no CBMSC",
            "executar cooperação técnica, no âmbito da aviação de segurança pública, com "
            "órgãos correlatos, firmada pelo Comando-Geral do CBMSC",
            "atuar de forma integrada com a Coordenação Aeroespacial do Grupo de Resposta "
            "Aérea de Urgência do GRAU/SAMU-Santa Catarina, na capacitação e aperfeiçoamento "
            "técnico-científico dos enfermeiros e médicos de voo",
            "desenvolver e promover o serviço de resgate e transporte aeromédico especializado "
            "em todo território de Santa Catarina",
        ],
        "source": "cf. CBMSC, LOB (Dec. nº 1.328/2021), Art. 52",
        "organName": "Batalhão Bombeiro Militar de Operações Aéreas", "abbr": "",
    },
}


def lob_enrich_for(organ_key: str, state_id: str):
    """Entrada curada da LOB para (órgão, estado), ou None."""
    return LOB_ENRICHMENT.get((organ_key, state_id))
