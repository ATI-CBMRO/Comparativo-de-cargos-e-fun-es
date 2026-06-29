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
}


def lob_enrich_for(organ_key: str, state_id: str):
    """Entrada curada da LOB para (órgão, estado), ou None."""
    return LOB_ENRICHMENT.get((organ_key, state_id))
