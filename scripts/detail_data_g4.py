# detail_data_g4.py — Paraná, Paraíba, Pará, Pernambuco, Piauí

DATA = {

"pr": {
  "legal_source": "Lei nº 22.206, de 29 de novembro de 2024",
  "organs": {
    "comandante_geral": {
      "name": "Comandante-Geral", "abbreviation": "CG", "category": "Direção Geral",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 10",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 10 (Comandante-Geral)"],
      "atribuicoes": ["Responsável superior pelo comando e pela administração geral do CBMPR", "Precedência hierárquica e funcional sobre todos os Oficiais e Praças, exceto a precedência funcional em relação ao Coordenador Estadual da Defesa Civil"],
      "desdobramentos": ["Subcomandante-Geral", "Estado-Maior", "Gabinete do Comando-Geral", "Consultoria Institucional", "Corregedoria-Geral", "Comissões"],
      "cargos": [{"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel Combatente da ativa", "desdobramentos": [], "atribuicoes": ["Comando e administração geral do CBMPR"]}]
    },
    "subcomandante_geral": {
      "name": "Subcomandante-Geral", "abbreviation": "SCG", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 13",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 13 (Subcomandante-Geral)"],
      "atribuicoes": ["Substituto imediato do Comandante-Geral nos seus impedimentos, afastamentos temporários e/ou vacância", "Exerce a função de coordenador operacional da Corporação"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel Combatente da ativa", "desdobramentos": [], "atribuicoes": ["Substituição do Comandante-Geral e coordenação operacional"]}]
    },
    "estado_maior": {
      "name": "Estado-Maior", "abbreviation": "EM", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 14",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 14 (Estado-Maior)"],
      "atribuicoes": ["Órgão de direção geral responsável pelo planejamento estratégico da Corporação", "Elaboração de diretrizes e ordens do Comando-Geral no acionamento dos órgãos de direção setorial e de execução"],
      "desdobramentos": ["1ª Seção (BM/1): Pessoal e legislação", "2ª Seção (BM/2): Inteligência", "3ª Seção (BM/3): Planejamento, operações e estatística", "4ª Seção (BM/4): Logística"],
      "cargos": [{"cargo": "Chefe do Estado-Maior", "subordinadoA": "Comandante-Geral", "requisito": "Coronel Combatente da ativa", "desdobramentos": [], "atribuicoes": ["Precedência hierárquica e funcional sobre os demais, exceto CG e SCG", "Substituto eventual do Subcomandante-Geral"]}]
    },
    "gabinete_cg": {
      "name": "Gabinete do Comando-Geral", "abbreviation": "Gab.CmtG", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 9, § 1º, I, d",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 9 (Estrutura)"],
      "atribuicoes": ["Apoio e assessoramento ao Comando-Geral"],
      "desdobramentos": ["Ajudância-Geral (AG)", "Assessoria Estratégica (Assest)", "Assessoria de Comunicação Organizacional (Assecom)", "Secretaria do Comando-Geral (Sec.CmdoG)"],
      "cargos": []
    },
    "ajudancia_geral": {
      "name": "Ajudância-Geral", "abbreviation": "AG", "category": "Apoio",
      "subordinadoA": "Chefe de Gabinete", "legalRef": "Art. 16",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 16 (Ajudância-Geral)"],
      "atribuicoes": ["Organização, direção e supervisão do pessoal auxiliar de todos os órgãos do Comando-Geral", "Direção e supervisão do efetivo da Banda de Música do CBMPR", "Coordenação dos trabalhos de protocolo geral", "Elaboração dos boletins-gerais", "Manutenção e desenvolvimento do centro histórico"],
      "desdobramentos": [], "cargos": []
    },
    "assessoria_estrategica": {
      "name": "Assessoria Estratégica", "abbreviation": "Assest", "category": "Apoio",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 17",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 17 (Assessoria Estratégica)"],
      "atribuicoes": ["Planejamento, implementação e monitoramento de projetos e ações institucionais", "Gestão, monitoramento e controle da captação de recursos", "Assessoramento nos assuntos de defesa civil", "Coordenação do Serviço Integrado de Atendimento ao Trauma em Emergência (SIATE)"],
      "desdobramentos": [], "cargos": []
    },
    "assessoria_comunicacao": {
      "name": "Assessoria de Comunicação Organizacional", "abbreviation": "Assecom", "category": "Apoio",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 18",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 18 (Assecom)"],
      "atribuicoes": ["Comunicação social, campanhas de educação preventiva e assessoria de imprensa", "Organização de solenidades na sede do CBMPR"],
      "desdobramentos": [], "cargos": []
    },
    "consultoria_institucional": {
      "name": "Consultoria Institucional", "abbreviation": "CI", "category": "Apoio",
      "subordinadoA": "Comandante-Geral e Subcomandante-Geral", "legalRef": "Art. 20",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 20 (Consultoria Institucional)"],
      "atribuicoes": ["Estudo de questões de direito da política de administração geral da Corporação", "Exames de aspectos de legalidade dos atos e normas", "Orientação quanto ao cumprimento de decisões e sentenças judiciais", "Análise de minutas de convênios"],
      "desdobramentos": [], "cargos": []
    },
    "comissoes": {
      "name": "Comissões", "abbreviation": "CPO/CPP/CM", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 21",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 21 (Comissões)"],
      "atribuicoes": ["Caráter permanente ou temporário conforme necessidade"],
      "desdobramentos": ["Comissão de Promoções de Oficiais (CPO)", "Comissão de Promoções de Praças (CPP)", "Comissão de Mérito (CM)"],
      "cargos": []
    },
    "corregedoria_geral": {
      "name": "Corregedoria-Geral", "abbreviation": "Coger", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 23",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Arts. 23-26 (Corregedoria-Geral)"],
      "atribuicoes": ["Assegurar a correta aplicação da lei", "Padronizar os procedimentos de Polícia Judiciária Militar e processos administrativos", "Realizar correições, fiscalizações e preservar hierarquia e disciplina", "Apuração de crimes militares, fatos administrativos e faltas disciplinares", "Cumprir mandados de prisão e alvarás de soltura de integrantes da Corporação"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Corregedor-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel Combatente da ativa", "desdobramentos": [], "atribuicoes": ["Chefia da Corregedoria-Geral"]}]
    },
    "diretoria_pessoal": {
      "name": "Diretoria de Pessoal", "abbreviation": "DP", "category": "Direção Setorial",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 28",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 28 (Diretoria de Pessoal)"],
      "atribuicoes": ["Desenvolvimento, coordenação, fiscalização e controle das atividades de classificação e movimentação de pessoal", "Inativos, cadastro, avaliação, folha de pagamento, identificação e recrutamento", "Serviços de saúde física e mental, assistência social e psicológica"],
      "desdobramentos": ["Centro de Recrutamento e Seleção (CRS)", "Centro de Saúde (CS)", "Centro de Educação Física e Desporto (CEFID)"],
      "cargos": [{"cargo": "Diretor de Pessoal", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Direção da Diretoria"]}]
    },
    "diretoria_apoio_logistico": {
      "name": "Diretoria de Apoio Logístico e Finanças", "abbreviation": "DALF", "category": "Direção Setorial",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 29",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 29 (DALF)"],
      "atribuicoes": ["Coordenação, controle e execução das atividades de logística, suprimento, manutenção e controle patrimonial", "Planejamento, acompanhamento e execução orçamentária e financeira", "Controladoria e auditoria de recursos descentralizados"],
      "desdobramentos": ["Centro de Planejamento e Compras (CPC)", "Centro de Administração Logística (CAL)", "Centro de Orçamento e Finanças (COF)", "Centro de Suprimento e Manutenção (CSM)"],
      "cargos": [{"cargo": "Diretor de Apoio Logístico e Finanças", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Direção da Diretoria"]}]
    },
    "diretoria_atividades_tecnicas": {
      "name": "Diretoria de Atividades Técnicas", "abbreviation": "DAT", "category": "Direção Setorial",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 30",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 30 (DAT)"],
      "atribuicoes": ["Coordenação, controle e assessoramento sobre prevenção e combate a incêndios e desastres em edificações, estabelecimentos, áreas de risco e eventos", "Gerenciamento normativo, estudos e pesquisa de incêndios", "Tecnologia da informação e comunicação"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor de Atividades Técnicas", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Direção da Diretoria"]}]
    },
    "escola_superior": {
      "name": "Escola Superior de Bombeiro Militar", "abbreviation": "ESBM", "category": "Direção Setorial",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 31",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 31 (ESBM)"],
      "atribuicoes": ["Planejamento, coordenação, fiscalização, execução e controle das atividades de ensino", "Atuação em parceria com outras instituições"],
      "desdobramentos": [],
      "cargos": [{"cargo": "Diretor da ESBM", "subordinadoA": "Comandante-Geral", "requisito": "Oficial Superior", "desdobramentos": [], "atribuicoes": ["Direção da Escola Superior"]}]
    },
    "comando_regional": {
      "name": "Comando Regional de Bombeiro Militar", "abbreviation": "CRBM", "category": "Execução",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 35",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 35 (CRBM)"],
      "atribuicoes": ["Escalões intermediários de comando", "Desenvolver ações operacionais estratégicas", "Propor a distribuição do efetivo", "Auxílio, fiscalização e gestão logística das unidades subordinadas"],
      "desdobramentos": ["Batalhões de Bombeiro Militar (BBM)", "Companhias Independentes de Bombeiro Militar (Cia. Ind. BM)"],
      "cargos": []
    },
    "batalhao": {
      "name": "Batalhão de Bombeiro Militar", "abbreviation": "BBM", "category": "Execução",
      "subordinadoA": "Comando Regional", "legalRef": "Art. 38, I",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 38, I (BBM)"],
      "atribuicoes": ["Coordenar e executar as atividades de defesa civil", "Exercer o poder de polícia administrativa de prevenção a incêndios e desastres", "Combater incêndios e desastres", "Realizar buscas, salvamentos, socorros públicos e atendimento pré-hospitalar"],
      "desdobramentos": ["Companhias de Bombeiro Militar (Cia. BM)", "Pelotões de Bombeiro Militar (Pel. BM)", "Grupos de Bombeiro Militar (Gp. BM)"],
      "cargos": []
    },
    "companhia_independente": {
      "name": "Companhia Independente de Bombeiro Militar", "abbreviation": "Cia. Ind. BM", "category": "Execução",
      "subordinadoA": "Comando Regional", "legalRef": "Art. 38, II",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 38, II (Cia. Ind. BM)"],
      "atribuicoes": ["Mesmas atribuições do Batalhão de Bombeiro Militar em áreas de menores dimensões não incluídas na circunscrição daquele"],
      "desdobramentos": ["Pelotões de Bombeiro Militar (Pel. BM)", "Grupos de Bombeiro Militar (Gp. BM)"],
      "cargos": []
    },
    "gost": {
      "name": "Grupo de Operações de Socorro Tático", "abbreviation": "GOST", "category": "Execução",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 38, III",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 38, III (GOST)"],
      "atribuicoes": ["Executar a missão especializada de socorro tático", "Ações de atendimento às emergências ambientais e a sinistros decorrentes de desastres", "Atividades de busca e salvamento, inclusive com cães", "Organizar e manter o canil central"],
      "desdobramentos": [], "cargos": []
    },
    "uoa": {
      "name": "Unidade de Operações Aéreas", "abbreviation": "UOA", "category": "Execução",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 38, IV",
      "baseLegal": "Lei nº 22.206, de 29 de novembro de 2024",
      "artigosDeOrigem": ["Art. 38, IV (UOA)"],
      "atribuicoes": ["Atender e apoiar ações de busca, resgate e salvamento em áreas urbanas, rurais, rodovias, matas, florestas, montanhas, rios, lagos e mar", "Atuar em missões de apoio à defesa civil", "Apoiar órgãos que necessitem do emprego de aeronaves"],
      "desdobramentos": [], "cargos": []
    }
  }
},

"pb": {
  "legal_source": "Lei Complementar nº 191, de 26 de abril de 2024",
  "organs": {
    "cg-pb": {
      "name": "Comando Geral", "abbreviation": "CG", "category": "Direção Estratégica",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 14; Art. 15 §3º LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 14 (Gabinete do Comando Geral)", "Art. 15 §3º (Atribuições do CMTG)"],
      "atribuicoes": [
        "Ao Gabinete do Comandante Geral do Corpo de Bombeiros Militar compete a direção e administração geral do Corpo de Bombeiros Militar do Estado da Paraíba – CBMPB no cumprimento dos seus objetivos, sendo o Comandante Geral a autoridade máxima da Corporação. (Art. 14)",
        "I – aprovar as diretrizes e planos gerais de emprego operacional no Estado;",
        "II – aprovar as diretrizes gerais de ensino, instrução e pesquisa;",
        "III – aprovar o orçamento anual da Corporação;",
        "IV – aprovar o plano de aplicação dos recursos orçamentários;",
        "V – aprovar os regimentos internos dos órgãos da Corporação;",
        "VI – aprovar normas técnicas relativas à segurança contra incêndio e controle de pânico;",
        "VII – aprovar normas técnicas com vistas à normatização e fiscalização operacional e de ensino das brigadas de incêndio, bombeiros civis e de bombeiros voluntários, além da padronização de seus vestuários, no Estado da Paraíba;",
        "VIII – assessorar o Governador do Estado em assuntos inerentes à Corporação;",
        "IX – assessorar o Secretário de Estado da Segurança e Defesa Social em assuntos que digam respeito às ações e operações bombeiro militares, de defesa civil e de mobilização previstas na Constituição Federal;",
        "X – atender, dentro das possibilidades de seu efetivo, às requisições expedidas por autoridades civis e militares, consoante a legislação em vigor;",
        "XI – autorizar o pessoal militar e civil da Corporação a se afastarem do Estado;",
        "XII – celebrar convênios e contratos de interesse da Corporação com entidades de direito público ou privado, nos termos da lei;",
        "XIII – conceder licenças ou afastamentos de qualquer natureza, bem como, aprovar o plano anual de férias da Corporação;",
        "XIV – cumprir as obrigações previstas na legislação relativa à convocação e mobilização;",
        "XV – decidir originariamente ou em grau de recurso, todos os assuntos pertinentes ao pessoal do Corpo de Bombeiros Militar, nos limites de sua competência;",
        "XVI – declarar aspirantes-a-oficial e promover praças às graduações subsequentes;",
        "XVII – delegar atribuições de sua competência, respeitados os limites legais;",
        "XVIII – designar e dispensar bombeiros militares e funcionários civis da Corporação de funções administrativas ou operacionais previstas na estrutura organizacional, exceto os cargos de provimento em comissão;",
        "XIX – elaborar o plano de comando, de acordo com as diretrizes e programas do Governo;",
        "XX – encaminhar ao Governador do Estado, para aprovação e publicação em Diário Oficial do Estado – DOE, a minuta do Regulamento Geral Bombeiro Militar – RGBM, contendo as competências e estrutura pormenorizadas dos órgãos da Corporação;",
        "XXI – encaminhar ao Governador do Estado, para aprovação e publicação em Diário Oficial do Estado - DOE, a minuta do Regulamento Interno dos Serviços Gerais e Operacionais – RISCO, regulando todos os serviços internos e operacionais da Corporação;",
        "XXII – encaminhar ao Governador do Estado para aprovação e publicação em DOE, a minuta do Regulamento de Uniforme Bombeiro Militar – RUBM, regulando todos os uniformes e trajes da Corporação e a apresentação pessoal dos bombeiros militares;",
        "XXIII – encaminhar ao Governador do Estado para aprovação e publicação em DOE, a minuta do Regulamento de Movimentação de Oficiais e Praças do Corpo de Bombeiro Militar – REMOP, regulando as movimentações de oficiais e praças no âmbito da Corporação;",
        "XXIV – encaminhar, ao Governador do Estado, a solicitação de afastamento do País de bombeiros militares e servidores civis da Corporação, quando em serviço;",
        "XXV – encaminhar ao órgão competente o projeto de orçamento anual da Corporação e participar, no que couber, do planejamento do plano plurianual do Estado;",
        "XXVI – exercer a competência disciplinar e a polícia judiciária militar que lhe são afetas;",
        "XXVII – expedir os atos administrativos necessários à gestão Institucional;",
        "XXVIII – incluir, nomear, licenciar e excluir Praças e Praças Especiais, obedecidos os requisitos legais;",
        "XXIX – manter intercâmbio com as demais Instituições Militares, de Segurança Pública e Defesa Civil;",
        "XXX – movimentar oficiais e praças e afastá-los de suas funções, respeitadas disposições legais;",
        "XXXI – nomear comissões e grupos de trabalhos, estabelecendo suas incumbências;",
        "XXXII – ordenar o emprego de verbas orçamentárias, de crédito abertos ou de outros recursos em favor do Corpo de Bombeiros Militar da Paraíba;",
        "XXXIII – pôr bombeiros militares à disposição de órgãos vinculados ou não, agregar e reverter praças da Corporação;",
        "XXXIV – propor ao Governador do Estado a nomeação e exoneração dos cargos de provimento em comissão de oficiais bombeiros militares para o exercício das funções de comando, direção e assessoramento;",
        "XXXV – representar a Corporação junto aos Órgãos e Poderes constituídos;",
        "XXXVI – solucionar os casos omissos na legislação específica."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Comandante Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel da ativa do QOEM do CBMPB; honras, prerrogativas, direitos e obrigações de Secretário de Estado (Art. 15 §2º)", "desdobramentos": [], "atribuicoes": ["O Comandante Geral – CMTG – é o responsável pelo comando, gestão, emprego, supervisão e coordenação geral das atividades da Corporação. (Art. 15)"]}]
    },
    "gcg-pb": {
      "name": "Gabinete do Comando Geral", "abbreviation": "GCG", "category": "Direção Estratégica",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 13; Art. 18 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 13 (Composição do CG)", "Art. 18 (Chefia do GCG)"],
      "atribuicoes": [
        "A Chefia de Gabinete do Comando Geral – CGCG compete assistir diretamente o Gabinete do Comando Geral – GCG – e o Assistente do Comando Geral é o Chefe do GCG, realizando a assistência direta ao Comandante Geral e ao Subcomandante Geral. (Art. 18)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Assistente do Comando Geral / Chefe do GCG", "subordinadoA": "Comandante Geral", "requisito": "Tenente-Coronel da ativa do CBMPB (Art. 18)", "desdobramentos": [], "atribuicoes": ["Assistência direta ao Comandante Geral e ao Subcomandante Geral (Art. 18)."]}]
    },
    "gscmdg": {
      "name": "Gabinete do Subcomandante Geral", "abbreviation": "GSCMDG", "category": "Direção Estratégica",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 16; Art. 17 §3º LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 16 (Gabinete do SCG)", "Art. 17 §3º (Atribuições do SCMTG)"],
      "atribuicoes": [
        "Ao Gabinete do Subcomandante Geral do Corpo de Bombeiros Militar, compete assistir diretamente o Gabinete do Comandante Geral do Corpo de Bombeiros Militar no cumprimento dos seus objetivos, sendo o Subcomandante Geral do Corpo de Bombeiros Militar o substituto legal do Comandante Geral do Corpo de Bombeiros Militar. (Art. 16)",
        "I – assessorar o CMTG na coordenação do funcionamento da Corporação;",
        "II – estabelecer o expediente da Corporação;",
        "III – exercer a competência disciplinar e a polícia judiciária militar que lhe são afetas;",
        "IV – substituir o CMTG nos eventuais impedimentos;",
        "V – supervisionar a garantia da hierarquia e disciplina da Corporação;",
        "VI – supervisionar os trabalhos dos órgãos de direção setorial;",
        "VII – supervisionar os trabalhos dos órgãos de execução, em nível estratégico."
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Subcomandante Geral", "subordinadoA": "Comandante Geral", "requisito": "Coronel da ativa do QOEM do CBMPB; honras, prerrogativas, direitos e obrigações de Secretário Executivo de Estado (Art. 17 §2º)", "desdobramentos": [], "atribuicoes": ["O Subcomandante Geral – SCMTG – é o responsável pela garantia da hierarquia e disciplina, principal assessor do Comandante Geral. (Art. 17)"]}]
    },
    "scg-pb": {
      "name": "Secretaria do Comando Geral", "abbreviation": "SCG", "category": "Direção Estratégica",
      "subordinadoA": "Gabinete do Comando Geral", "legalRef": "Art. 19 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 19 (Secretaria do Comando Geral)"],
      "atribuicoes": [
        "A Secretaria do Comando Geral – SCG – compete ao secretariado do GCG, bem como a edição, controle, publicação e arquivo do Boletim Geral do Corpo de Bombeiros Militar – Bol. BM – e dos Boletins Reservados – Bol. BM/R – da Corporação. (Art. 19)",
        "§2º São atribuições do Secretário da SCG todos os trabalhos de secretariado, elaboração dos atos administrativos e da edição, controle, publicação e arquivo do Bol. BM e do Bol. BM/R."
      ],
      "desdobramentos": ["Ajudância de Ordem (AjO)"],
      "cargos": [{"cargo": "Secretário da SCG", "subordinadoA": "Gabinete do Comando Geral", "requisito": "Major da ativa da Corporação (Art. 19 §3º)", "desdobramentos": [], "atribuicoes": ["Secretariado do GCG; edição, controle, publicação e arquivo do Bol. BM e Bol. BM/R (Art. 19 §2º)."]}]
    },
    "ouv-pb": {
      "name": "Ouvidoria do Corpo de Bombeiros Militar", "abbreviation": "OUV", "category": "Direção Estratégica",
      "subordinadoA": "Gabinete do Comando Geral", "legalRef": "Art. 20 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 20 (Ouvidoria)"],
      "atribuicoes": [
        "A Ouvidoria do Corpo de Bombeiros Militar – OUV – tem por finalidade receber e registrar denúncias, reclamações e representações de atos desabonadores praticados por integrantes da Corporação ou críticas à prestação de serviço institucional, bem como, de encaminhar e acompanhar a solução delas, funcionando em estreita articulação com a Ouvidoria Geral do Estado – OGE. (Art. 20)"
      ],
      "desdobramentos": ["Ouvidoria Central", "Ouvidorias Setoriais"],
      "cargos": [{"cargo": "Ouvidor", "subordinadoA": "Gabinete do Comando Geral", "requisito": "Oficial QOEM", "desdobramentos": [], "atribuicoes": ["Receber e registrar denúncias, reclamações e representações; encaminhar e acompanhar sua solução (Art. 20)."]}]
    },
    "ari-pb": {
      "name": "Assessoria de Relações Institucionais", "abbreviation": "ARI", "category": "Direção Estratégica",
      "subordinadoA": "Gabinete do Comando Geral", "legalRef": "Art. 21 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 21 (Assessoria de Relações Institucionais)"],
      "atribuicoes": [
        "A Assessoria de Relações Institucionais - ARI – tem a finalidade de assessorar o Comando Geral em assuntos legislativos relacionados com a atividade fim da Corporação e atividades de Defesa Social e Defesa Civil, além de, representar a Corporação junto aos Poderes Legislativos Federal, Estadual e Municipais. (Art. 21)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Assessor de Relações Institucionais", "subordinadoA": "Gabinete do Comando Geral", "requisito": "Bombeiro militar designado pelo Comandante Geral para cargo de Assessor Parlamentar (Art. 21 pú)", "desdobramentos": [], "atribuicoes": ["Assessoramento em assuntos legislativos; representação junto aos Poderes Legislativos (Art. 21)."]}]
    },
    "ccg-pb": {
      "name": "Centro de Contratações Gerais", "abbreviation": "CCG", "category": "Direção Estratégica",
      "subordinadoA": "Gabinete do Comando Geral", "legalRef": "Art. 22 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 22 (Centro de Contratações Gerais)"],
      "atribuicoes": [
        "O Centro de Contratações Gerais do Corpo de Bombeiros Militar – CCG tem a finalidade de assessorar o Comando Geral em assuntos relacionados com as Leis de Licitações e Contratos Administrativos, bem como tomar decisões, acompanhar o trâmite das licitações, dar impulso aos procedimentos licitatórios, auxiliar comissão temporária de contratação e executar quaisquer outras atividades necessárias ao bom andamento dos certames até a homologação. (Art. 22)"
      ],
      "desdobramentos": ["Subcentro de Contratações Bens e Serviços (CCBS)", "Subcentro de Contratações de Obras e Serviço de Engenharia (CCOSE)"],
      "cargos": [{"cargo": "Chefe do CCG", "subordinadoA": "Gabinete do Comando Geral", "requisito": "Oficial QOEM", "desdobramentos": [], "atribuicoes": ["Assessoramento em licitações e contratos; acompanhamento dos certames (Art. 22)."]}]
    },
    "qcg-pb": {
      "name": "Quartel do Comando Geral", "abbreviation": "QCG", "category": "Direção Estratégica",
      "subordinadoA": "Gabinete do Comando Geral", "legalRef": "Art. 26 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 26 (Quartel do Comando Geral)"],
      "atribuicoes": [
        "O Quartel do Comando Geral 'Coronel Geraldo Cabral de Vasconcelos' – QCG – é o Centro Administrativo da Corporação, responsável pela manutenção do funcionamento dos órgãos de direção estratégica e setorial, além do reforço operacional aos órgãos de execução. (Art. 26)",
        "§4º O QCG é o centro administrativo da Corporação responsável pelo suprimento das necessidades de finanças, logística e pessoal dos órgãos de direção estratégica e setorial."
      ],
      "desdobramentos": ["Companhia de Comando e Serviço (CCSv/QCG)", "Guarda Bombeiro Militar da Reserva (GBMR)"],
      "cargos": [{"cargo": "Comandante do QCG", "subordinadoA": "Gabinete do Comando Geral", "requisito": "Tenente-Coronel da ativa da Corporação (cargo em comissão, nomeado pelo Governador do Estado — Art. 26 §2º)", "desdobramentos": [], "atribuicoes": ["Suprimento das necessidades de finanças, logística e pessoal dos órgãos de direção estratégica e setorial (Art. 26 §4º)."]}]
    },
    "ac-pb": {
      "name": "Alto Comando", "abbreviation": "AC", "category": "Direção Estratégica",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 27 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 27 (Alto Comando)"],
      "atribuicoes": [
        "O Alto Comando – AC – tem a função de exercer o aconselhamento estratégico do Comando Geral, sendo presidido pelo Comandante Geral e tendo como membros: o Subcomandante Geral, o Chefe do EMG, o Corregedor Geral, o Controlador Geral, os Diretores Setoriais, e os Comandantes Regionais da Corporação. (Art. 27)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Presidente do Alto Comando", "subordinadoA": "—", "requisito": "Comandante Geral (presidente nato)", "desdobramentos": [], "atribuicoes": ["Presidência do colegiado de aconselhamento estratégico (Art. 27)."]}]
    },
    "emg-pb": {
      "name": "Estado Maior Geral", "abbreviation": "EMG", "category": "Direção Estratégica",
      "subordinadoA": "Comandante Geral", "legalRef": "Art. 28; Art. 28 §4º LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 28 (Estado Maior Geral)", "Art. 28 §4º (Atribuições do Chefe do EMG)"],
      "atribuicoes": [
        "O Estado Maior Geral – EMG – é o órgão de assessoramento estratégico do Gabinete do Comando Geral, responsável pela assessoria perante o Comando Geral no planejamento e na gestão estratégica para o desenvolvimento e cumprimento das missões institucionais. (Art. 28 caput)",
        "I – acompanhar o desenvolvimento das políticas estabelecidas pelo Comandante Geral, a fim de mantê-lo informado dos objetivos alcançados e de sua evolução;",
        "II – assessorar o Comandante Geral no planejamento da Gestão Institucional;",
        "III – elaborar o Planejamento Estratégico da Corporação;",
        "IV – elaborar o Plano de Contratações Anual da Corporação em alinhamento com o Planejamento Estratégico;",
        "V – elaborar e aprovar as políticas setoriais da Corporação;",
        "VI – elaborar diretrizes, planos e ordens a serem baixados pelo Comandante Geral;",
        "VII – elaborar seu regimento interno e encaminhar para aprovação;",
        "VIII – realizar estudos e planejamentos, coordenar e fiscalizar todas as atividades da Corporação para assegurar o mais eficiente emprego;",
        "IX – supervisionar a execução dos planos e das ordens baixadas pelo Comandante-Geral e tomar as providências necessárias à consecução dos objetivos da Corporação."
      ],
      "desdobramentos": ["1ª EMG: Assessoria de Estudos Legislativos", "2ª EMG: Assessoria de Inteligência", "3ª EMG: Operações, Doutrina e Estatística", "4ª EMG: Mobilização, Avaliação de Riscos e Resposta a Desastres", "5ª EMG: Comunicação Social e Marketing", "6ª EMG: Planejamento Logístico, Elaboração e Gestão de Projetos", "7ª EMG: Gestão Estratégica e Gestão da Qualidade", "8ª EMG: Integração Comunitária, Programas e Projetos Sociais"],
      "cargos": [{"cargo": "Chefe do Estado Maior Geral", "subordinadoA": "Comandante Geral", "requisito": "Coronel da ativa da Corporação (cargo em comissão, nomeado pelo Governador do Estado — Art. 28 §2º)", "desdobramentos": [], "atribuicoes": ["I a IX – atribuições previstas no Art. 28 §4º da LC nº 191/2024."]}]
    },
    "ci-pb": {
      "name": "Controladoria Interna", "abbreviation": "CI", "category": "Direção Estratégica",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 29 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 29 (Controladoria Interna)"],
      "atribuicoes": [
        "A Controladoria Interna – CI – é responsável pelo controle, auditoria, fiscalização, monitoramento e orientação das atividades dos processos desenvolvidos e contratos firmados pela Corporação. (Art. 29 caput)",
        "§2º Cabe a Controladoria Interna - CI a gestão, fiscalização e análise dos processos de prestações de contas, atos de inclusão de pessoal, processos de inatividade de militares, licitações, contratos e convênios, controle de gastos, gestão de riscos e de controle preventivo das contratações, agindo de ofício, tendo, no exercício de suas funções, acesso irrestrito aos órgãos da Corporação e aos atos administrativos de seus membros."
      ],
      "desdobramentos": ["Seção de Auditoria e Fiscalização (CI/1)", "Seção de Gestão de Contratos (CI/2)", "Seção de Controle de Gastos (CI/3)", "Seção de Controle Patrimonial (CI/4)"],
      "cargos": [{"cargo": "Controlador Interno", "subordinadoA": "Comando Geral", "requisito": "Coronel da ativa da Corporação (cargo em comissão, nomeado pelo Governador do Estado — Art. 29 §3º)", "desdobramentos": [], "atribuicoes": ["Controle, auditoria, fiscalização, monitoramento e orientação das atividades dos processos desenvolvidos e contratos firmados (Art. 29)."]}]
    },
    "correg-pb": {
      "name": "Corregedoria do Corpo de Bombeiros Militar", "abbreviation": "CORREG", "category": "Direção Estratégica",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 30 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 30 (Corregedoria)"],
      "atribuicoes": [
        "A Corregedoria do Corpo de Bombeiros Militar – CORREG – é o órgão de direção estratégica com a finalidade de apurar as infrações penais militares, apurando, acompanhando, fiscalizando e aplicando a correição no regime ético-disciplinar nos serviços da Corporação, e terá sua organização e competências disciplinadas em legislação específica. (Art. 30)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Corregedor", "subordinadoA": "Comando Geral", "requisito": "Coronel da ativa da Corporação (cargo em comissão, nomeado pelo Governador do Estado — Art. 30 §1º)", "desdobramentos": [], "atribuicoes": ["Apuração de infrações penais militares; correição no regime ético-disciplinar (Art. 30)."]}]
    },
    "crbm-pb": {
      "name": "Comandos Regionais de Bombeiro Militar", "abbreviation": "CRBM", "category": "Direção Estratégica",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 32 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 32 (Comandos Regionais de Bombeiro Militar)"],
      "atribuicoes": [
        "Os Comandos Regionais de Bombeiro Militar – CRBM – são unidades gestoras, em nível estratégico, organizadas de forma sistêmica e responsáveis pela gestão estratégica regionalizada nas Regiões Integradas de Segurança Pública, através do controle, planejamento e supervisão das atividades operacionais realizadas pelas OBM subordinadas. (Art. 32)",
        "§6º O CRBM tem jurisdição na REISP onde está instalado, podendo apoiar operacionalmente municípios de responsabilidade de outro CRBM, articulando-se com as unidades locais.",
        "§7º Subordinam-se ao CRBM, administrativamente e operacionalmente, os Batalhões de Bombeiro Militar – BBM – e as Companhias Independentes de Bombeiro Militar – CIBM – instaladas na circunscrição da REISP que o respectivo comando é responsável.",
        "§8º O Centro Regional de Intendência – CRI - tem a competência de controle do almoxarifado, e de realizar a descarga ou descarte de materiais, assim como o controle e manutenção de viaturas e equipamentos no âmbito da regional."
      ],
      "desdobramentos": ["Estado Maior Regional (EM/R): B/1 a B/6", "Centro Regional de Intendência (CRI)"],
      "cargos": [{"cargo": "Comandante Regional de Bombeiro Militar", "subordinadoA": "Comando Geral", "requisito": "Coronel da ativa da Corporação (cargo em comissão, nomeado pelo Governador do Estado — Art. 32 §4º)", "desdobramentos": [], "atribuicoes": ["Gestão estratégica regionalizada; controle, planejamento e supervisão das atividades operacionais das OBM subordinadas (Art. 32)."]}]
    },
    "dal-pb": {
      "name": "Diretoria de Apoio Logístico", "abbreviation": "DAL", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 34 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 34 (Diretoria de Apoio Logístico)"],
      "atribuicoes": [
        "A Diretoria de Apoio Logístico – DAL – tem por finalidade a gestão do sistema logístico, responsável pelo planejamento, coordenação, fiscalização e controle das atividades de aquisição, suprimento e manutenção de materiais, viaturas e equipamentos. (Art. 34)",
        "§2º O Centro de Suprimento Logístico – CSL é o órgão de apoio logístico responsável pelo recebimento, controle, armazenamento, distribuição e suprimento de material de intendência, materiais permanentes, materiais de consumo e material bélico.",
        "§3º O Centro de Arquitetura, Engenharia e Obras – CAEO é o órgão de apoio logístico responsável pelos planos e projetos de arquitetura e engenharia dos prédios da Corporação, controle do patrimônio imóvel, fiscalização das obras de conservação predial e construção de novos aquartelamentos.",
        "§4º O Centro de Controle e Manutenção de Viaturas – CMAV é o órgão de apoio logístico responsável pelo recebimento, controle e manutenção de viaturas da Corporação."
      ],
      "desdobramentos": ["Centro de Suprimento Logístico (CSL)", "Centro de Arquitetura, Engenharia e Obras (CAEO)", "Centro de Controle e Manutenção de Viaturas (CMAV)"],
      "cargos": [{"cargo": "Diretor de Apoio Logístico", "subordinadoA": "Subcomandante Geral", "requisito": "Coronel da ativa da Corporação (cargo em comissão, nomeado pelo Governador do Estado — Art. 33 §3º)", "desdobramentos": [], "atribuicoes": ["Gestão do sistema logístico; planejamento, coordenação, fiscalização e controle das atividades de aquisição, suprimento e manutenção (Art. 34)."]}]
    },
    "dat-pb": {
      "name": "Diretoria de Atividades Técnicas", "abbreviation": "DAT", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 35 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 35 (Diretoria de Atividades Técnicas)"],
      "atribuicoes": [
        "A Diretoria de Atividades Técnicas – DAT – é a unidade gestora, em nível setorial, organizado de forma sistêmica e responsável pelo estudo, análise, planejamento, orientação técnica, normatização, controle e fiscalização das atividades relativas à segurança contra incêndio e controle de pânico, ao cumprimento das disposições legais sobre o assunto e investigação de incêndios e explosões. (Art. 35)"
      ],
      "desdobramentos": ["Conselho Técnico Normativo (CTN)", "Conselho Técnico Deliberativo (CTD)", "Comissão Interna de Análise Técnica (CIAT)", "Seção de Legislação de Prevenção contra Incêndio (DAT/1)", "Seção de Segurança contra Incêndio (DAT/2)"],
      "cargos": [{"cargo": "Diretor de Atividades Técnicas", "subordinadoA": "Subcomandante Geral", "requisito": "Coronel da ativa da Corporação (cargo em comissão, nomeado pelo Governador do Estado — Art. 33 §3º)", "desdobramentos": [], "atribuicoes": ["Estudo, análise, planejamento, normatização, controle e fiscalização das atividades de SCI/CP e investigação de incêndios (Art. 35)."]}]
    },
    "dep-pb": {
      "name": "Diretoria de Educação e Pesquisa", "abbreviation": "DEP", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 37 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 37 (Diretoria de Educação e Pesquisa)"],
      "atribuicoes": [
        "A Diretoria de Educação e Pesquisa – DEP – é responsável pela gestão do sistema de educação militar da Corporação, por meio do planejamento, supervisão, coordenação, fiscalização, controle e execução das atividades de ensino, treinamento e pesquisa científica, relacionadas à qualificação profissional de recursos humanos para o exercício das funções atribuídas aos integrantes do CBMPB, bem como de outras instituições civis ou militares, mediante convênio. (Art. 37)",
        "§3º A ABMAP é a instituição de ensino superior – IES, pluricurricular, especializada na formação tecnológica e profissional de bombeiros militares, com base na conjugação de conhecimentos técnicos e tecnológicos com as suas práticas pedagógicas, nos termos do sistema de ensino militar e das diretrizes e bases da educação nacional.",
        "§4º O CFAO é responsável pela pesquisa científica, execução e coordenação do planejamento pedagógico dos cursos de formação, habilitação e aperfeiçoamento de oficiais, através dos cursos de graduação e pós-graduação stricto-sensu ou lato-sensu.",
        "§5º O CFAP é responsável pela formação, habilitação e aperfeiçoamento de praças, através dos cursos de educação tecnológica de graduação e pós-graduação, bem como, dos cursos de educação técnica de nível médio."
      ],
      "desdobramentos": ["Academia de Bombeiro Militar 'Aristarcho Pessoa Cavalcanti de Albuquerque' (ABMAP)", "Centro de Formação, Habilitação e Aperfeiçoamento de Oficiais (CFAO)", "Centro de Formação, Habilitação e Aperfeiçoamento de Praças (CFAP)", "Centro de Pesquisa e Extensão (CPEx)", "Centro de Treinamento Operacional (CTOP)", "Colégios Militares", "Corpo Musical"],
      "cargos": [{"cargo": "Diretor de Educação e Pesquisa", "subordinadoA": "Subcomandante Geral", "requisito": "Coronel da ativa da Corporação (cargo em comissão, nomeado pelo Governador do Estado — Art. 33 §3º)", "desdobramentos": [], "atribuicoes": ["Gestão do sistema de educação militar; planejamento, supervisão, coordenação e execução do ensino, treinamento e pesquisa científica (Art. 37)."]}]
    },
    "df-pb": {
      "name": "Diretoria de Finanças", "abbreviation": "DF", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 40 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 40 (Diretoria de Finanças)"],
      "atribuicoes": [
        "A Diretoria de Finanças – DF – tem como finalidade a gestão do sistema de planejamento e administração financeira, orçamentária, contábil, bem como a gestão de Fundos e Convênios. (Art. 40)"
      ],
      "desdobramentos": ["Seção de Administração Financeira (DF/1)", "Seção de Orçamento (DF/2)", "Seção de Contabilidade (DF/3)", "Seção de Auditoria e Controle (DF/4)", "Seção de Captação de Recursos (DF/5)"],
      "cargos": [{"cargo": "Diretor de Finanças", "subordinadoA": "Subcomandante Geral", "requisito": "Coronel da ativa da Corporação (cargo em comissão, nomeado pelo Governador do Estado — Art. 33 §3º)", "desdobramentos": [], "atribuicoes": ["Gestão do sistema de planejamento e administração financeira, orçamentária, contábil e de Fundos e Convênios (Art. 40)."]}]
    },
    "dgp-pb": {
      "name": "Diretoria de Gestão de Pessoas", "abbreviation": "DGP", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 41 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 41 (Diretoria de Gestão de Pessoas)"],
      "atribuicoes": [
        "A Diretoria de Gestão de Pessoas – DGP – tem como finalidade o planejamento, recrutamento, seleção, acompanhamento, execução, controle e fiscalização das atividades relacionadas com os recursos humanos da Corporação, sejam militares de carreira ou temporários, bem como os servidores civis. (Art. 41)"
      ],
      "desdobramentos": ["Centro de Recrutamento e Seleção de Pessoal (CRESEP)", "Seções DGP/1 a DGP/8"],
      "cargos": [{"cargo": "Diretor de Gestão de Pessoas", "subordinadoA": "Subcomandante Geral", "requisito": "Coronel da ativa da Corporação (cargo em comissão, nomeado pelo Governador do Estado — Art. 33 §3º)", "desdobramentos": [], "atribuicoes": ["Planejamento, recrutamento, seleção, acompanhamento, execução, controle e fiscalização das atividades de recursos humanos (Art. 41)."]}]
    },
    "ds-pb": {
      "name": "Diretoria de Saúde", "abbreviation": "DS", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 42 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 42 (Diretoria de Saúde)"],
      "atribuicoes": [
        "A Diretoria de Saúde – DS – é o órgão integrante do Sistema de Proteção Social dos Militares da Corporação, com competência para planejar, coordenar, fiscalizar, controlar e executar todas as atividades de saúde, assistência biopsicossocial e veterinária, além do trato das questões referentes ao estado sanitário do pessoal da Corporação e seus dependentes. (Art. 42)"
      ],
      "desdobramentos": ["Centro de Perícia Médica de Saúde Militar (CPMSM)", "Centro de Saúde Biopsicossocial (CSBIO)", "Centro de Capacitação Física Militar (CCFM)", "Policlínicas de Saúde Biopsicossociais (PSBIO)", "Clínica Veterinária (CVET)"],
      "cargos": [{"cargo": "Diretor de Saúde", "subordinadoA": "Subcomandante Geral", "requisito": "Coronel da ativa da Corporação (cargo em comissão, nomeado pelo Governador do Estado — Art. 33 §3º)", "desdobramentos": [], "atribuicoes": ["Planejamento, coordenação, fiscalização, controle e execução das atividades de saúde, assistência biopsicossocial e veterinária (Art. 42)."]}]
    },
    "dti-pb": {
      "name": "Diretoria de Tecnologia da Informação", "abbreviation": "DTI", "category": "Direção Setorial",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Art. 43 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 43 (Diretoria de Tecnologia da Informação)"],
      "atribuicoes": [
        "A Diretoria de Tecnologia da Informação – DTI – tem por finalidade desenvolver sistemas e aplicativos computacionais, a prospecção e absorção de novas tecnologias, administração da rede de informática e dos bancos de dados, o suporte técnico de software e equipamentos, o atendimento especializado aos usuários e a governança de tecnologia da informação e inovação. (Art. 43)"
      ],
      "desdobramentos": ["Seções DTI/1 a DTI/8"],
      "cargos": [{"cargo": "Diretor de Tecnologia da Informação", "subordinadoA": "Subcomandante Geral", "requisito": "Coronel da ativa da Corporação (cargo em comissão, nomeado pelo Governador do Estado — Art. 33 §3º)", "desdobramentos": [], "atribuicoes": ["Desenvolvimento de sistemas, TI, suporte técnico e governança de tecnologia da informação e inovação (Art. 43)."]}]
    },
    "exec-pb": {
      "name": "Unidades Operacionais", "abbreviation": "UOP", "category": "Execução",
      "subordinadoA": "Comandos Regionais de Bombeiro Militar", "legalRef": "Art. 44 LC 191/2024",
      "baseLegal": "Lei Complementar nº 191, de 26 de abril de 2024",
      "artigosDeOrigem": ["Art. 44 (Órgãos de Execução)"],
      "atribuicoes": [
        "I – análise de projetos arquitetônicos e de medidas de segurança contra incêndio e controle de pânico;",
        "II – busca, resgate e salvamento;",
        "III – execução e coordenação das atividades defesa civil;",
        "IV – fiscalização das medidas de segurança contra incêndio e controle de pânico, através de vistorias técnicas solicitadas, inopinadas ou por denúncias;",
        "V – investigação de incêndios e explosões;",
        "VI – prevenção, combate e extinção de incêndios;",
        "VII – prevenção balneária, salvamento aquático e mergulho autônomo de resgate;",
        "VIII – operações aéreas e resgate aeromédico;",
        "IX – socorro de urgência e atendimento pré-hospitalar."
      ],
      "desdobramentos": ["Batalhões de Bombeiro Militar (BBM)", "Companhias de Bombeiro Militar (CiaBM)", "Companhias Independentes (CIBM)", "Centros de Atividades Técnicas (CAT)", "Grupamento Especializado em Operações de Risco (GEOR)", "Grupamento de Operações Aéreas (GOA)"],
      "cargos": [{"cargo": "Comandante de Unidade Operacional", "subordinadoA": "Comandante Regional de Bombeiro Militar", "requisito": "Tenente-Coronel da ativa da Corporação (Comandante de BBM — Art. 51 §6º)", "desdobramentos": [], "atribuicoes": ["I a IX – missões previstas no Art. 44 da LC nº 191/2024."]}]
    }
  }
},

"pa": {
  "legal_source": "Lei nº 11.060, de 1º de julho de 2025",
  "organs": {
    "comandante_geral": {
      "name": "Comandante-Geral", "abbreviation": "CG", "category": "Direção Geral",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 7",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025",
      "artigosDeOrigem": ["Art. 7 (Comandante-Geral)"],
      "atribuicoes": ["O comando, a gestão, o emprego, a supervisão e a coordenação geral das atividades da corporação", "A presidência do Alto Comando", "A presidência da Comissão de Promoção de Oficiais", "A presidência do Conselho do Mérito Bombeiro Militar", "Celebrar convênios e contratos de interesse da Corporação", "Promover praças e declarar aspirantes-a-oficial"],
      "desdobramentos": ["Alto Comando", "Estado-Maior Geral", "Coordenadoria Estadual de Proteção e Defesa Civil", "Corregedoria-Geral", "Comando de Operações", "Departamentos-Gerais"],
      "cargos": [{"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Oficial da ativa, último posto do QOBM, possuidor do curso superior de bombeiros; equiparado a Secretário de Estado", "desdobramentos": [], "atribuicoes": ["Comando geral da Corporação"]}]
    },
    "chefe_estado_maior_geral": {
      "name": "Chefe do Estado-Maior Geral", "abbreviation": "Chefe EMG", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 12",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025",
      "artigosDeOrigem": ["Art. 12 (Chefe do EMG)"],
      "atribuicoes": ["Dirigir, coordenar e controlar as atividades da sua área e dos órgãos subordinados", "Executar o planejamento aprovado pelo comandante-geral", "Assessorar o comandante-geral na coordenação e supervisão geral", "Substitui o Comandante-Geral nos seus impedimentos ou ausências"],
      "desdobramentos": ["1ª Seção (BM/1): Pessoal e Legislação", "2ª Seção (BM/2): Gestão do Conhecimento, Cultura e Inovação", "3ª Seção (BM/3): Operações, Doutrina e Estatística", "4ª Seção (BM/4): Logística", "5ª Seção (BM/5): Gestão pela Qualidade", "6ª Seção (BM/6): Planejamento e Orçamento Institucional", "Escritório de Projetos e Convênios"],
      "cargos": [{"cargo": "Chefe do Estado-Maior Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial da ativa, último posto do QOBM; equiparado a secretário-adjunto de estado", "desdobramentos": [], "atribuicoes": ["Direção do EMG e substituição do Comandante-Geral"]}]
    },
    "alto_comando": {
      "name": "Alto Comando", "abbreviation": "AC", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 9",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025",
      "artigosDeOrigem": ["Art. 9 (Alto Comando)"],
      "atribuicoes": ["Órgão colegiado de direção-geral, com atribuições deliberativas e consultivas"],
      "desdobramentos": ["Presidente: Comandante-Geral", "Membros natos: Chefe do EMG, Coordenador-Adjunto Estadual de Proteção e Defesa Civil, Corregedor-Geral, Comandante Operacional, Chefes dos Departamentos-Gerais", "Membros efetivos: 3 oficiais do último posto designados pelo Comandante-Geral"],
      "cargos": []
    },
    "cedec": {
      "name": "Coordenadoria Estadual de Proteção e Defesa Civil", "abbreviation": "CEDEC", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral (Coordenador Estadual)", "legalRef": "Art. 13",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025",
      "artigosDeOrigem": ["Art. 13 (CEDEC)"],
      "atribuicoes": ["Integrar, planejar, organizar, coordenar e supervisionar a execução das medidas preventivas, de socorro, assistenciais e de recuperação", "Elaborar o Plano Estadual de Proteção e Defesa Civil", "Celebrar e executar convênios com a União e com os municípios"],
      "desdobramentos": ["Coordenador Estadual (Comandante-Geral)", "Coordenador-Adjunto Estadual", "Divisão de Gestão de Risco", "Divisão de Gerenciamento de Desastres", "Divisão Administrativa", "Divisão Orçamentária e Financeira", "Assessoria de Articulação e Gestão"],
      "cargos": []
    },
    "corregedoria_geral": {
      "name": "Corregedoria-Geral", "abbreviation": "CORREG", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 15",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025",
      "artigosDeOrigem": ["Art. 15 (Corregedoria-Geral)"],
      "atribuicoes": ["Assessoramento disciplinar", "Orientação, prevenção e fiscalização das atividades funcionais e da conduta profissional", "Aprimoramento da ética, da disciplina e da hierarquia"],
      "desdobramentos": ["Corregedor-Geral (último posto QOBM, preferencialmente bacharel em direito)", "Subcorregedor-Geral (Tenente-Coronel)", "Comissão Disciplinar Geral", "Comissão Disciplinar de Recurso", "Seção de Inteligência Correcional e Operações", "Seção de Gestão de Processos e Apoio Administrativo"],
      "cargos": []
    },
    "comando_operacoes": {
      "name": "Comando de Operações", "abbreviation": "Comando Ops", "category": "Direção Geral",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 16",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025",
      "artigosDeOrigem": ["Art. 16 (Comando de Operações)"],
      "atribuicoes": ["Direção e controle dos órgãos de direção intermediária e setorial", "Direção e controle de apoio e de execução da atividade-fim da corporação"],
      "desdobramentos": ["Comandante Operacional (último posto QOBM)", "Assistente (Tenente-Coronel)", "Seção de Planejamento de Pessoal", "Seção de Planejamento Logístico", "Seção de Planejamento de Operações e Estatística", "Seção de Planejamento de Eventos"],
      "cargos": []
    },
    "departamento_administracao": {
      "name": "Departamento-Geral de Administração", "abbreviation": "DGA", "category": "Direção Setorial",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 18",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025",
      "artigosDeOrigem": ["Art. 18 (DGA)"],
      "atribuicoes": ["Direção e controle dos órgãos de direção setorial de apoio logístico, contratações e aquisições, finanças e tecnologia da informação e comunicação"],
      "desdobramentos": ["Diretoria de Apoio Logístico (DAL)", "Diretoria de Finanças (DF)", "Diretoria de Contratações e Aquisições (DCA)", "Diretoria de Tecnologia da Informação e Comunicação (DTIC)"],
      "cargos": [{"cargo": "Chefe do DGA", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do último posto do QOBM", "desdobramentos": [], "atribuicoes": ["Direção do Departamento-Geral"]}]
    },
    "departamento_pessoal": {
      "name": "Departamento-Geral de Pessoal", "abbreviation": "DGP", "category": "Direção Setorial",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 19",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025",
      "artigosDeOrigem": ["Art. 19 (DGP)"],
      "atribuicoes": ["Direção e controle das atividades de pessoal: ingresso, identificação, classificação e movimentação", "Cadastros, avaliações, promoções, direitos e deveres", "Assistência psicológica, social e religiosa", "Acompanhamento de veteranos, pensionistas e saúde"],
      "desdobramentos": ["Seção de Controle de Pessoal", "Seção de Pagamento de Pessoal", "Seção de Recrutamento, Seleção e Inclusão", "Seção de Identificação"],
      "cargos": []
    },
    "departamento_cultura": {
      "name": "Departamento-Geral de Cultura, Educação e Pesquisa", "abbreviation": "DGCEP", "category": "Direção Setorial",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 20",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025",
      "artigosDeOrigem": ["Art. 20 (DGCEP)"],
      "atribuicoes": ["Gestão do sistema de ensino bombeiro militar e das atividades de pesquisa", "Formação, capacitação, aperfeiçoamento, especialização e qualificação dos oficiais e praças", "Promoção da cultura"],
      "desdobramentos": ["Seção de Planejamento de Ensino e Pesquisa", "Academia Bombeiro Militar", "Centros de Formação"],
      "cargos": []
    },
    "departamento_seguranca_incendio": {
      "name": "Departamento-Geral de Segurança contra Incêndios e Emergências", "abbreviation": "DGSCI", "category": "Direção Setorial",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 21",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025",
      "artigosDeOrigem": ["Art. 21 (DGSCI)"],
      "atribuicoes": ["Estabelecer diretrizes gerais de segurança contra incêndios e emergências", "Proteger a vida e reduzir danos ao meio ambiente e ao patrimônio"],
      "desdobramentos": ["Seção de Fiscalização e Vistoria Técnica", "Seção de Análise de Projetos", "Seção de Perícia de Incêndio", "Seção de Credenciamento de Empresas e Profissionais"],
      "cargos": []
    },
    "comando_regional_bombeiros": {
      "name": "Comando Regional de Bombeiros de Proteção e Emergência Ambiental", "abbreviation": "CRB", "category": "Direção Regional",
      "subordinadoA": "Comando de Operações", "legalRef": "Art. 30",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025",
      "artigosDeOrigem": ["Art. 30 (CRB)"],
      "atribuicoes": ["Direção, controle e planejamento das atividades operacionais das Unidades Bombeiro Militar (UBMs) subordinadas"],
      "desdobramentos": ["Comandante (último posto QOBM)", "Subcomandante (Tenente-Coronel)", "Seção de Administração", "Seção de Planejamento, Instrução e Operações", "Núcleo de Corregedoria"],
      "cargos": []
    },
    "exec_pa": {
      "name": "Unidades de Execução", "abbreviation": "UBM", "category": "Execução",
      "subordinadoA": "Comandos Regionais de Bombeiros", "legalRef": "Lei nº 11.060/2025",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025",
      "artigosDeOrigem": ["Lei nº 11.060/2025 (Unidades de Execução)"],
      "atribuicoes": ["Execução das atividades-fim de bombeiro militar (multiemprego e especializadas)"],
      "desdobramentos": ["Grupamento Bombeiro Militar", "Subgrupamento Bombeiro Militar", "Seção Bombeiro Militar", "Grupamento Marítimo e Fluvial (GMAF)", "Grupamento de Busca e Salvamento (GBS)", "Grupamento de Socorro e Emergência (GSE)", "Grupamento de Operações Aéreas (GOA)", "Núcleo de Ações com Cães (NAC)"],
      "cargos": []
    },

    "cg-pa-lob": {
      "name": "Comandante-Geral", "abbreviation": "CG", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Governador do Estado", "legalRef": "Art. 6º, 7º, 8º",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 6º (Órgãos de Direção-Geral)", "Art. 7º (Comandante-Geral)", "Art. 8º (Competência)"],
      "atribuicoes": [
        "O comandante-geral é equiparado aos secretários de estado, fazendo jus às prerrogativas e honras do cargo de secretário de estado, sendo nomeado pelo Chefe do Poder Executivo Estadual dentre os oficiais da ativa da corporação, do último posto do Quadro de Oficiais Bombeiro Militar combatente (QOBM), não convocado da reserva, possuidor do curso superior de bombeiros, nos termos da legislação vigente (Art. 7º).",
        "Compete ao comandante-geral: o comando, a gestão, o emprego, a supervisão e a coordenação geral das atividades da corporação, assessorado pelos órgãos de direção, apoio e de execução (I); a presidência do Alto Comando do CBMPA, da Comissão de Promoção de Oficiais e do Conselho do Mérito Bombeiro Militar (II); encaminhar ao órgão competente o projeto de orçamento anual e participar, no que couber, da elaboração do Plano Plurianual (III); celebrar convênios e contratos de interesse do CBMPA com entidades de direito público ou privado (IV); nomear e exonerar bombeiros militares no exercício das funções de direção, comando e assessoramento (V); autorizar bombeiros militares e servidores civis a se afastarem do estado (VI); ordenar o emprego de verbas orçamentárias ou de créditos abertos em favor do CBMPA (VII); expedir os atos necessários para a administração do CBMPA (VIII); incorporar praças e praças especiais (IX); promover praças e declarar aspirantes-a-oficial (X); conceder férias, licenças ou afastamentos de qualquer natureza (XI); instaurar e solucionar procedimentos e processos administrativos, disciplinares ou não, aplicando as penalidades previstas na legislação vigente (XII); criar, desenvolver e gerenciar programas de prevenção e proteção nas atividades bombeiro militar (XIII); certificar o atendimento do direito ao porte de arma de seus militares (XIV); e encaminhar ao Chefe do Poder Executivo a lista de promoção dos oficiais (XV) (Art. 8º, I a XV)."
      ],
      "desdobramentos": ["Alto Comando", "Estado-Maior Geral", "Coordenadoria Estadual de Proteção e Defesa Civil do Pará (CEDEC)", "Corregedoria-Geral", "Comando de Operações", "Departamentos-Gerais", "Comissões", "Gabinete do Comandante-Geral", "Ajudância-Geral", "Controladoria Interna", "Consultoria Jurídica (CONJUR)", "Centro de Inteligência (CEINT)"],
      "cargos": []
    },
    "ac-pa-lob": {
      "name": "Alto Comando", "abbreviation": "AC", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 9º, 10",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 9º (Alto Comando)", "Art. 10 (Atribuições)"],
      "atribuicoes": [
        "O Alto Comando do CBMPA é o órgão colegiado de direção-geral, com atribuições deliberativas e consultivas (Art. 9º).",
        "São atribuições do Alto Comando, no âmbito da corporação: em caráter consultivo, manifestar-se sobre o orçamento anual do CBMPA e outros assuntos de interesse do CBMPA (I, a e b); em caráter deliberativo, manifestar-se sobre a elaboração de reforma ou projeto de lei que envolva o CBMPA, a expedição de atos normativos provenientes de suas deliberações, as propostas referentes ao aumento do efetivo e criação e extinção de cargos, os conflitos de atribuições entre os órgãos de direção, de apoio e de execução, e a proposta referente à remuneração (II, a a e) (Art. 10, I e II)."
      ],
      "desdobramentos": ["Presidente: Comandante-Geral", "Membros natos: Chefe do Estado-Maior Geral, Coordenador-Adjunto Estadual de Proteção e Defesa Civil, Corregedor-Geral, Comandante Operacional, Chefe do Departamento-Geral de Administração, Chefe do Departamento-Geral de Pessoal, Chefe do Departamento-Geral de Cultura, Educação e Pesquisa, Chefe do Departamento-Geral de Segurança contra Incêndios e Emergências", "Membros efetivos: 3 oficiais do último posto designados pelo Comandante-Geral"],
      "cargos": []
    },
    "emg-pa-lob": {
      "name": "Estado-Maior Geral", "abbreviation": "EMG", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 11, 12",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 11 (Estado-Maior Geral)", "Art. 12 (Chefe do EMG)"],
      "atribuicoes": [
        "O Estado-Maior Geral é o órgão de direção-geral responsável, perante o comandante-geral, pela elaboração da política bombeiro militar, pelo planejamento estratégico, pela orientação do preparo e do emprego da corporação, pela organização, pela direção e pelo controle das atividades da corporação, elaborando diretrizes e ordens de comando em consonância com a missão institucional e a política de segurança pública do estado (Art. 11).",
        "Compete ao Chefe do Estado-Maior Geral: substituir o Comandante-Geral nos seus impedimentos ou ausências, respondendo pelo comando-geral da corporação (I); dirigir, coordenar e controlar as atividades da sua área de atuação e dos órgãos subordinados (II); executar o planejamento aprovado pelo comandante-geral no tocante à competência dos órgãos subordinados (III); assessorar o comandante-geral na coordenação e supervisão geral das atividades da corporação por meio do controle das atividades dos órgãos de direção setorial (IV); assegurar a atuação convergente e dinâmica dos órgãos de direção, apoio e execução (V); supervisionar a execução das diretrizes, planos e ordens (VI); realizar inspeções periódicas (VII); e desempenhar outras atribuições delegadas pelo comandante-geral (VIII) (Art. 12, I a VIII)."
      ],
      "desdobramentos": ["Chefe do Estado-Maior Geral", "Subchefe do Estado-Maior Geral", "1ª Seção (BM/1): Política e Planejamento de Pessoal e Legislação", "2ª Seção (BM/2): Política e Planejamento de Gestão do Conhecimento, Cultura e Inovação", "3ª Seção (BM/3): Política e Planejamento de Operações, Doutrina e Estatística", "4ª Seção (BM/4): Política e Planejamento de Logística", "5ª Seção (BM/5): Gestão pela Qualidade", "6ª Seção (BM/6): Planejamento e Orçamento Institucional", "Escritório de Projetos e Convênios", "Ajudância de Ordens", "Secretaria"],
      "cargos": []
    },
    "cedec-pa-lob": {
      "name": "Coordenadoria Estadual de Proteção e Defesa Civil do Pará", "abbreviation": "CEDEC", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral (Coordenador Estadual)", "legalRef": "Art. 13, 14",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 13 (CEDEC)", "Art. 14 (Constituição)"],
      "atribuicoes": [
        "A Coordenadoria Estadual de Proteção e Defesa Civil do Pará (CEDEC), órgão de direção-geral, é o órgão central e coordenador do Sistema Estadual de Proteção e Defesa Civil (SEPDEC), tem a missão de contribuir para proteção da vida, patrimônio e meio ambiente, atendendo a população no território paraense, em situação de emergência ou calamidade pública, desencadeadas por fatores anormais e adversos, bem como limitar riscos e perdas para a comunidade, com a finalidade de preservar e restabelecer a normalidade da vida comunitária, competindo-lhe: integrar, planejar, organizar, coordenar e supervisionar a execução das medidas preventivas de socorro assistenciais e de recuperação (I); preservar a moral da população e o restabelecimento da normalidade da vida comunitária em todo o território do estado do Pará (II); elaborar o Plano Estadual de Proteção e Defesa Civil, e suas diretrizes (III); celebrar e executar convênios com a União e com os municípios do estado (IV); desenvolver programas, projetos e atividades de defesa civil nas fases de normalidade ou anormalidade, voltados para prevenção, preparação e resposta (V); fazer mobilização entre os órgãos governamentais e não governamentais (VI); e fomentar a proteção e defesa civil nos municípios do estado (VII) (Art. 13, I a VII)."
      ],
      "desdobramentos": ["Coordenador Estadual de Proteção e Defesa Civil (Comandante-Geral)", "Coordenador-Adjunto Estadual de Proteção e Defesa Civil", "Divisão de Gestão de Risco", "Divisão de Gerenciamento de Desastres", "Divisão Administrativa", "Divisão Orçamentária e Financeira", "Assessoria de Articulação e Gestão", "Secretaria"],
      "cargos": []
    },
    "correg-pa-lob": {
      "name": "Corregedoria-Geral", "abbreviation": "CORREG", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 15",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 15 (Corregedoria-Geral)"],
      "atribuicoes": [
        "A Corregedoria-Geral (CORREG), diretamente vinculada ao comandante-geral, é o órgão correcional do CBMPA responsável pelo assessoramento disciplinar, pela orientação, prevenção e fiscalização das atividades funcionais e da conduta profissional, visando o aprimoramento da ética, da disciplina e da hierarquia entre os integrantes da corporação (Art. 15)."
      ],
      "desdobramentos": ["Corregedor-Geral", "Subcorregedor-Geral", "Comissão Disciplinar Geral", "Comissão Disciplinar de Recurso", "Seção de Inteligência Correcional e Operações", "Seção de Gestão de Processos e Apoio Administrativo", "Secretaria"],
      "cargos": []
    },
    "co-pa-lob": {
      "name": "Comando de Operações", "abbreviation": "Comando Ops", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 16",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 16 (Comando de Operações)"],
      "atribuicoes": [
        "O Comando de Operações é o órgão de direção-geral responsável pela direção e pelo controle dos órgãos de direção intermediária e setorial, de apoio e de execução da atividade-fim da corporação (Art. 16)."
      ],
      "desdobramentos": ["Comandante Operacional", "Assistente", "Seção de Planejamento de Pessoal", "Seção de Planejamento Logístico", "Seção de Planejamento de Operações e Estatística", "Seção de Planejamento de Eventos", "Secretaria"],
      "cargos": []
    },
    "dga-pa-lob": {
      "name": "Departamento-Geral de Administração", "abbreviation": "DGA", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 17, 18",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 17 (Departamentos-Gerais)", "Art. 18 (DGA)"],
      "atribuicoes": [
        "O Departamento-Geral de Administração (DGA) é responsável pela direção e pelo controle dos órgãos de direção setorial de apoio logístico, de contratações e aquisições, de finanças e de tecnologia da informação e comunicação, que realizam a atividade-meio da corporação (Art. 18)."
      ],
      "desdobramentos": ["Chefe do DGA", "Assistente", "Secretaria", "Assessorias Técnicas", "Diretoria de Apoio Logístico (DAL)", "Diretoria de Finanças (DF)", "Diretoria de Contratações e Aquisições (DCA)", "Diretoria de Tecnologia da Informação e Comunicação (DTIC)"],
      "cargos": []
    },
    "dgp-pa-lob": {
      "name": "Departamento-Geral de Pessoal", "abbreviation": "DGP", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 17, 19",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 17 (Departamentos-Gerais)", "Art. 19 (DGP)"],
      "atribuicoes": [
        "O Departamento-Geral de Pessoal (DGP) é responsável pela direção e pelo controle das atividades de pessoal da corporação relacionadas ao ingresso, à identificação, à classificação e à movimentação, aos cadastros e às avaliações, ao recadastramento, às promoções, aos direitos, aos deveres e aos incentivos, à assistência psicológica, social e religiosa, ao acompanhamento e ao controle de veteranos e pensionistas, bem como de saúde (Art. 19)."
      ],
      "desdobramentos": ["Chefe do DGP", "Subchefe do DGP", "Seção de Controle de Pessoal", "Seção de Pagamento de Pessoal", "Seção de Recrutamento, Seleção e Inclusão", "Seção de Identificação", "Secretaria", "Diretoria de Saúde (DS)", "Capelania"],
      "cargos": []
    },
    "dgcep-pa-lob": {
      "name": "Departamento-Geral de Cultura, Educação e Pesquisa", "abbreviation": "DGCEP", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 17, 20",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 17 (Departamentos-Gerais)", "Art. 20 (DGCEP)"],
      "atribuicoes": [
        "O Departamento-Geral de Cultura, Educação e Pesquisa (DGCEP) é responsável pela gestão do sistema de ensino bombeiro militar, das atividades de pesquisa, relacionados à formação, à capacitação, ao aperfeiçoamento, à especialização, à extensão e qualificação dos oficiais e praças, bem como pela promoção da cultura (Art. 20)."
      ],
      "desdobramentos": ["Chefe do DGCEP", "Assistente", "Seção de Planejamento de Ensino e Pesquisa", "Secretaria", "Academia Bombeiro Militar (ABM)", "Centro de Formação, Aperfeiçoamento e Especialização (CFAE)", "Centro de Capacitação Física e Desporto (CCFD)", "Centro de Memória", "Colégios Militares"],
      "cargos": []
    },
    "dgsci-pa-lob": {
      "name": "Departamento-Geral de Segurança contra Incêndios e Emergências", "abbreviation": "DGSCI", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 17, 21",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 17 (Departamentos-Gerais)", "Art. 21 (DGSCI)"],
      "atribuicoes": [
        "O Departamento-Geral de Segurança contra Incêndios e Emergências (DGSCI) é responsável por estabelecer diretrizes gerais de segurança contra incêndios e emergências, de modo a proteger a vida e a reduzir danos ao meio ambiente e ao patrimônio (Art. 21)."
      ],
      "desdobramentos": ["Chefe do DGSCI", "Subchefe do DGSCI", "Seção de Fiscalização e Vistoria Técnica", "Seção de Análise de Projetos", "Seção de Perícia de Incêndio", "Seção de Credenciamento de Empresas e Profissionais", "Secretaria"],
      "cargos": []
    },
    "com-pa-lob": {
      "name": "Comissões (CPO e CPP)", "abbreviation": "COM", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral / Chefe do Estado-Maior Geral", "legalRef": "Art. 22, 23",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 22 (Comissão de Promoção de Oficiais)", "Art. 23 (Comissão de Promoção de Praças)"],
      "atribuicoes": [
        "A Comissão de Promoção de Oficiais (CPO) é o órgão de assessoramento permanente do comandante-geral nos assuntos relativos às carreiras dos oficiais da corporação, competindo-lhe o controle, a avaliação e o processamento das promoções (Art. 22).",
        "A Comissão de Promoção de Praças (CPP) é o órgão de assessoramento permanente do chefe do Estado-Maior Geral nos assuntos referentes às carreiras de praças da corporação, competindo-lhe o controle, a avaliação e o processamento das promoções (Art. 23)."
      ],
      "desdobramentos": ["Comissão de Promoção de Oficiais (CPO): Presidente Comandante-Geral, membros natos e efetivos", "Comissão de Promoção de Praças (CPP): Presidente Chefe do EMG, membro nato e efetivos"],
      "cargos": []
    },
    "gab-pa-lob": {
      "name": "Gabinete do Comandante-Geral", "abbreviation": "GAB", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 24",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 24 (Gabinete do Comandante-Geral)"],
      "atribuicoes": [
        "O Gabinete do Comandante-Geral é um órgão de direção-geral responsável por prestar assessoria direta, permanente e pessoal ao comandante-geral (Art. 24)."
      ],
      "desdobramentos": ["Chefia", "Assistência", "Assessoria de Comunicação Social", "Assessoria de Assuntos Institucionais", "Secretaria", "Ajudância de Ordens"],
      "cargos": []
    },
    "ag-pa-lob": {
      "name": "Ajudância-Geral", "abbreviation": "AG", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 25",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 25 (Ajudância-Geral)"],
      "atribuicoes": [
        "A Ajudância-Geral é o órgão de direção-geral que tem a seu cargo as funções de secretaria e apoio administrativo ao comando-geral, coordenação dos serviços gerais, manutenção e segurança do quartel do comando-geral (Art. 25)."
      ],
      "desdobramentos": ["Ajudante-Geral", "Fiscal Administrativo do Comando-Geral", "Seção Administrativa", "Secretaria e Protocolo-Geral", "Banda de Música"],
      "cargos": []
    },
    "ci-pa-lob": {
      "name": "Controladoria Interna", "abbreviation": "CI", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 26",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 26 (Controladoria Interna)"],
      "atribuicoes": [
        "A Controladoria Interna (CI), órgão de direção-geral, subordinada ao Comandante-Geral, é responsável por adotar as providências relacionadas com a defesa do patrimônio público, auditoria, orientação, fiscalização, averiguação e análise das atividades de administração orçamentária, financeira, patrimonial e de gestão de pessoas no âmbito da corporação, sem prejuízo das demais atribuições definidas em lei (Art. 26)."
      ],
      "desdobramentos": ["Controlador", "Seção de Auditorias", "Seção de Análise de Conformidade Normativa", "Seção Contábil, Orçamentária e Financeira", "Secretaria"],
      "cargos": []
    },
    "conjur-pa-lob": {
      "name": "Consultoria Jurídica", "abbreviation": "CONJUR", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 27",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 27 (Consultoria Jurídica)"],
      "atribuicoes": [
        "A Consultoria Jurídica (CONJUR) é órgão de direção-geral, diretamente subordinada ao Comandante-Geral, tendo por finalidade a prestação de assessoramento jurídico, competindo-lhe o estudo de questões de direito compreendidas na política de administração geral da instituição, examinar aspectos de legalidade dos atos e normas que lhe forem submetidos à análise e demais atribuições que venham a ser previstas em regulamento (Art. 27)."
      ],
      "desdobramentos": ["Chefe da Consultoria Jurídica (CONJUR)", "Membros da Consultoria Jurídica (CONJUR)", "Secretaria"],
      "cargos": []
    },
    "ceint-pa-lob": {
      "name": "Centro de Inteligência", "abbreviation": "CEINT", "category": "Direção Geral", "source": "lob",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 28",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 28 (Centro de Inteligência)"],
      "atribuicoes": [
        "O Centro de Inteligência (CEINT) é órgão de direção-geral, subordinado ao comandante-geral, responsável por planejar, coordenar, executar, fiscalizar, controlar, articular, supervisionar e gerenciar as atividades de inteligência bombeiro militar, no âmbito do CBMPA, dentro do território paraense, e assessorar o comandante-geral da corporação nos assuntos de cunho estratégico, tático e operacional que lhe forem confiados, além de se interrelacionar com os demais órgãos estaduais de inteligência e do Sistema Brasileiro de Inteligência (SISBIN) (Art. 28)."
      ],
      "desdobramentos": ["Chefia", "Seção de Inteligência", "Seção de Segurança Orgânica", "Secretaria"],
      "cargos": []
    },
    "crb-pa-lob": {
      "name": "Comandos Operacionais Intermediários de Bombeiros (CRB e CME-BM)", "abbreviation": "CRB/CME-BM", "category": "Direção Intermediária", "source": "lob",
      "subordinadoA": "Comando de Operações", "legalRef": "Art. 29, 30, 31",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 29 (Direção Intermediária e Setorial)", "Art. 30 (Comandos Operacionais Intermediários)", "Art. 31 (Estrutura)"],
      "atribuicoes": [
        "Aos Comandos Operacionais Intermediários de Bombeiros, subordinados ao Comando de Operações, cabe a direção, o controle e o planejamento das atividades operacionais das suas Unidades Bombeiro Militar (UBMs) subordinadas, no âmbito de suas respectivas responsabilidades e circunscrições, sendo assim definidos: Comando Regional de Bombeiros de Proteção e Emergência Ambiental (CRB) (I); e Comando de Missões Especiais Bombeiro Militar (CME-BM) (II) (Art. 30, I e II)."
      ],
      "desdobramentos": ["Comandante", "Subcomandante", "Seção de Administração", "Seção de Planejamento, Instrução e Operações", "Núcleo de Corregedoria"],
      "cargos": []
    },
    "dir-pa-lob": {
      "name": "Diretorias (DAL, DF, DCA, DTIC, DS)", "abbreviation": "DIR", "category": "Direção Setorial", "source": "lob",
      "subordinadoA": "Departamentos-Gerais", "legalRef": "Art. 32 a 37",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 32 (Diretorias)", "Art. 33 (DAL)", "Art. 34 (DF)", "Art. 35 (DCA)", "Art. 36 (DTIC)", "Art. 37 (DS)"],
      "atribuicoes": [
        "As diretorias constituem os órgãos de direção setorial, subordinadas aos departamentos-gerais, para as atividades administrativas de apoio logístico, finanças, contratações e aquisições, tecnologia da informação e comunicação, e saúde, compreendendo: Diretoria de Apoio Logístico (DAL) (I); Diretoria de Finanças (DF) (II); Diretoria de Contratações e Aquisições (DCA) (III); Diretoria de Tecnologia da Informação e Comunicação (DTIC) (IV); e Diretoria de Saúde (DS) (V) (Art. 32, I a V).",
        "À Diretoria de Apoio Logístico (DAL), subordinada ao Departamento-Geral de Administração (DGA), compete planejar, coordenar, fiscalizar e controlar as necessidades de apoio, suprimento, manutenção, patrimônio e obras (Art. 33).",
        "À Diretoria de Finanças (DF), subordinada ao Departamento-Geral de Administração (DGA), compete realizar as atividades financeiras dos órgãos da corporação e a distribuição de recursos orçamentários, de acordo com o planejamento estabelecido (Art. 34).",
        "À Diretoria de Contratações e Aquisições (DCA), subordinada ao Departamento-Geral de Administração (DGA), compete realizar os procedimentos licitatórios da corporação, além da formalização e administração dos contratos e convênios da corporação (Art. 35).",
        "À Diretoria de Tecnologia da Informação e Comunicação (DTIC), subordinada ao Departamento-Geral de Administração (DGA), compete realizar o planejamento, a gestão e a execução das ações referentes à tecnologia da informação e comunicação (Art. 36).",
        "À Diretoria de Saúde (DS), subordinada ao Departamento-Geral de Pessoal (DGP), compete o planejamento, a gestão e a execução das ações de assistência relacionadas à saúde e atenção biopsicossocial do bombeiro militar, seus dependentes legais, bem como dos animais do CBMPA (Art. 37)."
      ],
      "desdobramentos": ["Diretoria de Apoio Logístico (DAL)", "Diretoria de Finanças (DF)", "Diretoria de Contratações e Aquisições (DCA)", "Diretoria de Tecnologia da Informação e Comunicação (DTIC)", "Diretoria de Saúde (DS)"],
      "cargos": []
    },
    "apoio-pa-lob": {
      "name": "Órgãos de Apoio", "abbreviation": "APOIO", "category": "Apoio", "source": "lob",
      "subordinadoA": "Departamentos-Gerais / Diretoria de Apoio Logístico / Ajudância-Geral", "legalRef": "Art. 38 a 46",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 38 (Órgãos de Apoio)", "Art. 39 a 46 (Cada órgão)"],
      "atribuicoes": [
        "Os órgãos de apoio compreendem: Academia Bombeiro Militar (I); Centro de Formação, Aperfeiçoamento e Especialização (II); Centro de Capacitação Física e Desporto (III); Centro de Suprimento e Manutenção de Viaturas e Material Operacional (IV); Centro de Patrimônio (V); Centro de Memória (VI); Capelania (VII); Banda de Música (VIII); e Colégio Militar (IX) (Art. 38, I a IX).",
        "A Academia Bombeiro Militar 'Cap BM Antônio Veríssimo Ivo de Abreu' (ABM) é órgão de apoio subordinado ao Departamento-Geral de Cultura, Educação e Pesquisa (DGCEP), responsável pela realização dos cursos de formação, adaptação e habilitação de Oficiais, bem como pelas pós-graduações dos Oficiais e pelo desenvolvimento de altos estudos e pesquisas científicas de segurança pública (Art. 39).",
        "O Centro de Formação, Aperfeiçoamento e Especialização 'Maj BM Henrique Rubim' (CFAE) é órgão de apoio subordinado ao DGCEP, responsável pela realização dos cursos de formação, adaptação e aperfeiçoamento de Praças e especialização de bombeiros militares (Art. 40).",
        "O Centro de Capacitação Física e Desporto (CCFD) é órgão de apoio subordinado ao DGCEP, responsável pelas ações relacionadas à qualidade de vida e desporto na corporação, ligadas ao treinamento físico militar, avaliação física, treinamento desportivo e áreas correlatas à capacitação ao exercício da profissão bombeiro militar (Art. 41).",
        "O Centro de Suprimento, Manutenção de Viaturas e Material Operacional (CSMV/MOP) é órgão de apoio subordinado à Diretoria de Apoio Logístico (DAL), incumbido da obtenção, da estocagem e da distribuição dos suprimentos específicos e da execução, da manutenção do armamento e do material especializado, incumbindo-lhe ainda o suprimento e a manutenção das viaturas e de todo o equipamento da corporação (Art. 42).",
        "O Centro de Patrimônio é unidade de apoio subordinada à DAL, responsável pelo patrimônio por meio do controle dos bens móveis, imóveis e semoventes, materiais e equipamentos operacionais pertencentes à corporação (Art. 43).",
        "O Centro de Memória é órgão de apoio subordinado ao DGCEP, responsável por conservar, investigar, comunicar, interpretar, promover e expor conjuntos, concertos e coleções de valor histórico, artístico, científico, técnico ou de qualquer outra natureza cultural (Art. 44).",
        "A Capelania, órgão de apoio subordinado ao Departamento-Geral de Pessoal (DGP), é responsável pela assistência ecumênica dos militares da corporação e seus dependentes (Art. 45).",
        "A Banda de Música, órgão de apoio subordinado à Ajudância-Geral, destina-se a realizar concertos, formaturas, eventos e outras solenidades de interesse da corporação (Art. 46)."
      ],
      "desdobramentos": ["Academia Bombeiro Militar (ABM)", "Centro de Formação, Aperfeiçoamento e Especialização (CFAE)", "Centro de Capacitação Física e Desporto (CCFD)", "Centro de Suprimento e Manutenção de Viaturas e Material Operacional (CSMV/MOP)", "Centro de Patrimônio", "Centro de Memória", "Capelania", "Banda de Música", "Colégio Militar"],
      "cargos": []
    },
    "exec-pa-lob": {
      "name": "Órgãos de Execução (Unidades Bombeiro Militar)", "abbreviation": "UBM", "category": "Execução", "source": "lob",
      "subordinadoA": "Órgãos de Direção Intermediária", "legalRef": "Art. 47 a 56",
      "baseLegal": "Lei nº 11.060, de 1º de julho de 2025 (Lei de Organização Básica)",
      "artigosDeOrigem": ["Art. 47 (UBMs)", "Art. 48 (Multiemprego)", "Art. 49 (Especializadas)", "Art. 50 a 56 (Cada Unidade)"],
      "atribuicoes": [
        "As Unidades Bombeiro Militar (UBMs), subordinadas aos órgãos de direção intermediária, são órgãos de execução e constituem as unidades operacionais da corporação, classificadas em unidades de multiemprego e unidades especializadas (Art. 47).",
        "As Unidades Bombeiro Militar de multiemprego são compostas por: Grupamento Bombeiro Militar (GBM) (I); Subgrupamento Bombeiro Militar (SGBM) (II); Seção Bombeiro Militar (SBM) (III); Posto Avançado Bombeiro Militar (PABM) (IV); e Posto de Bombeiro Militar (PBM) (V) (Art. 48, I a V).",
        "As Unidades Bombeiro Militar especializadas são compostas por: Grupamento Marítimo e Fluvial (GMAF) (I); Grupamento de Busca e Salvamento (GBS) (II); Grupamento de Socorro e Emergência (GSE) (III); Grupamento de Operações Aéreas (GOA) (IV); e Núcleo de Ações com Cães (NAC) (V) (Art. 49, I a V).",
        "Os Grupamentos e Subgrupamentos Bombeiro Militar são órgãos de execução do CBMPA, subordinados aos Comandos Regionais de Bombeiros de Proteção e Emergência Ambiental (CRB) correspondentes, de acordo com a sua circunscrição (Art. 50).",
        "A Seção Bombeiro Militar (SBM) é a unidade destinada a atender serviços específicos objetos de convênio com empresas públicas ou privadas; não executa atividades referentes à segurança contra incêndios e emergências (Art. 51).",
        "Os Postos Avançados Bombeiro Militar (PABMs) são as menores unidades independentes de execução operacional e estrutura física da corporação, subordinados aos comandos regionais correspondentes, de acordo com a sua circunscrição (Art. 52).",
        "O Grupamento Marítimo e Fluvial (GMAF) é órgão de execução do CBMPA, subordinado ao Comando de Missões Especiais Bombeiro Militar (CME-BM), tendo como atribuições as ações de prevenção de acidentes e incêndios marítimos e fluviais em todo estado, além de busca, resgate e salvamento aquático (Art. 53).",
        "O Grupamento de Busca e Salvamento (GBS) é órgão de execução do CBMPA, subordinado ao CME-BM, tendo como atribuições as ações de busca, salvamento e resgate, além de outras específicas de bombeiros militar, em todo o território do estado do Pará (Art. 54).",
        "O Grupamento de Socorro e Emergência (GSE) é órgão de execução do CBMPA, subordinado ao CME-BM, tendo como atribuições as ações de emergências médicas voltadas ao atendimento pré-hospitalar e socorro de urgência, em todo o território do Estado (Art. 55).",
        "O Núcleo de Ações com Cães (NAC) é órgão de execução do CBMPA, subordinado ao CME-BM, tendo como atribuições as ações relativas à busca, resgate e salvamento com cães (Art. 56)."
      ],
      "desdobramentos": ["Grupamento Bombeiro Militar (GBM)", "Subgrupamento Bombeiro Militar (SGBM)", "Seção Bombeiro Militar (SBM)", "Posto Avançado Bombeiro Militar (PABM)", "Posto de Bombeiro Militar (PBM)", "Grupamento Marítimo e Fluvial (GMAF)", "Grupamento de Busca e Salvamento (GBS)", "Grupamento de Socorro e Emergência (GSE)", "Grupamento de Operações Aéreas (GOA)", "Núcleo de Ações com Cães (NAC)"],
      "cargos": []
    }
  }
},

"pe": {
  "legal_source": "Lei nº 15.187, de 12 de dezembro de 2013",
  "organs": {
    "cg-pe": {
      "name": "Comando Geral", "abbreviation": "CG", "category": "Direção Geral",
      "subordinadoA": "Secretário de Defesa Social", "legalRef": "Art. 10",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 10 (Comandante Geral)"],
      "atribuicoes": ["O Comandante Geral do CBMPE é o responsável pelo comando, administração e emprego da Corporação (Art. 10)"],
      "desdobramentos": ["Comandante Geral (CG)", "Subcomandante Geral (SCG)", "Conselho de Políticas e Estratégias (CPE)"],
      "cargos": [{"cargo": "Comandante Geral", "subordinadoA": "Secretário de Defesa Social", "requisito": "Oficial do Quadro de Combatentes (QOC) da ativa e do último posto, nomeado pelo Governador do Estado (Art. 10 §1º)", "desdobramentos": [], "atribuicoes": ["Responsável pelo comando, administração e emprego da Corporação (Art. 10)"]}]
    },
    "scg-pe": {
      "name": "Subcomandante Geral", "abbreviation": "SCG", "category": "Direção Geral",
      "subordinadoA": "Comandante Geral", "legalRef": "Arts. 11, 93",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 11 (Subcomandante Geral)", "Art. 93 (Atribuições)"],
      "atribuicoes": [
        "I - responder pelo expediente do Comando Geral, em impedimentos eventuais do Comandante Geral;",
        "II - exercer interinamente o cargo de Comandante Geral da Corporação em: a) impedimento temporário por mais de 30 dias; b) afastamento do território nacional; e c) impedimento definitivo até nomeação do novo Comandante Geral;",
        "III - zelar pela conduta civil e profissional do pessoal do CBMPE;",
        "IV - apresentar propostas e emitir pareceres sobre os assuntos administrativos e operacionais que devem ser apreciados pelo Comandante Geral;",
        "V - secundar o Comandante Geral na fiscalização das atividades do CBMPE;",
        "VI - propor ao Comandante Geral as alterações necessárias à melhoria da eficiência dos serviços prestados pela Corporação;",
        "VII - supervisionar, dirigir e coordenar os trabalhos do Comando Geral da Corporação, harmonizando e fiscalizando as atividades de todos os órgãos de direção, órgãos de apoio e órgãos de execução;",
        "VIII - zelar pelo fiel cumprimento das decisões do Comandante Geral, dando pleno conhecimento aos órgãos da Corporação e verificando seu fiel cumprimento; e",
        "IX - exercer outros encargos que lhe sejam atribuídos pela legislação vigente. (Art. 93 I–IX)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Subcomandante Geral", "subordinadoA": "Comandante Geral", "requisito": "Oficial combatente da ativa do último posto, nomeado pelo Governador por indicação do Comandante Geral (Art. 11)", "desdobramentos": [], "atribuicoes": ["Substituto imediato do Comandante Geral nas suas ausências e impedimentos (Art. 11)"]}]
    },
    "cpe-pe": {
      "name": "Conselho de Políticas e Estratégias", "abbreviation": "CPE", "category": "Direção Geral",
      "subordinadoA": "Comandante Geral", "legalRef": "Arts. 12–13",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 12 (CPE)", "Art. 13 (Composição)"],
      "atribuicoes": ["O CPE é o órgão responsável pela formulação da doutrina geral de emprego da Corporação, de forma a viabilizar as políticas, estratégias, diretrizes e ordens estabelecidas pelo Comandante Geral e que acionam todos os demais órgãos no cumprimento de suas missões (Art. 12)"],
      "desdobramentos": ["Presidente: Comandante Geral", "Subcomandante Geral", "Membros: Diretores setoriais e diretores executivos", "Secretaria: Gabinete do Comandante Geral (Art. 13 §1º)"],
      "cargos": [{"cargo": "Presidente do CPE", "subordinadoA": "—", "requisito": "Comandante Geral (Art. 13 I)", "desdobramentos": [], "atribuicoes": ["Presidir o Conselho de Políticas e Estratégias (Art. 13)"]}]
    },
    "dgp-pe": {
      "name": "Diretoria de Gestão de Pessoal", "abbreviation": "DGP", "category": "Direção Setorial",
      "subordinadoA": "Comandante Geral", "legalRef": "Arts. 15, 95",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 15 (DGP)", "Art. 95 (Atribuições comuns dos Diretores)"],
      "atribuicoes": [
        "A DGP incumbe-se: I - do planejamento, da normatização, do controle e da fiscalização das atividades relacionadas com a gestão de pessoal; II - das atividades de formação, especialização e aperfeiçoamento; e III - da prestação de assistência social aos integrantes do CBMPE e seus dependentes. (Art. 15 I–III)",
        "I - prestar assessoramento ao Comandante Geral em assuntos de sua competência;",
        "II - coordenar e gerenciar tecnicamente os programas e projetos executivos sob sua responsabilidade;",
        "III - contribuir para a manutenção da unidade de ação da Corporação, em conjunto com os demais órgãos integrantes de sua estrutura;",
        "IV - sugerir a adoção ou implantação de normas, medidas e procedimentos que visem o aperfeiçoamento da estrutura e do desempenho das atividades;",
        "V - coordenar a atuação dos órgãos e unidades subordinados, centralizando a demanda de serviços a eles destinada;",
        "VI - praticar os atos administrativos de rotina na sua órbita de competência;",
        "VII - preparar e discutir a proposta orçamentária da Diretoria ou Comando;",
        "VIII - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob sua supervisão, sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal;",
        "IX - encaminhar, anualmente, ao Subcomandante Geral da Corporação, relatório das atividades técnicas, administrativas e operacionais, conforme o caso, ou quando da transmissão de função;",
        "X - emitir pareceres em questões técnicas na sua esfera de atribuições;",
        "XI - desempenhar outras atribuições e tarefas compatíveis com a função e as que forem determinadas pelo Comando Geral da Corporação; e",
        "XII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 95 I–XII)"
      ],
      "desdobramentos": ["Divisão de Controle de Pessoal (DCP)", "Divisão de Formação, Especialização e Aperfeiçoamento (DFEA)", "Divisão de Inativos e Pensionistas (DIP)", "Divisão de Planejamento e Desenvolvimento (DPD)"],
      "cargos": [{"cargo": "Diretor de Gestão de Pessoal", "subordinadoA": "Comandante Geral", "requisito": "Oficial do CBMPE (Art. 94)", "desdobramentos": [], "atribuicoes": ["Responsável direto perante o Comandante Geral pelo funcionamento do sistema de gestão de pessoal (Art. 94)"]}]
    },
    "dlog-pe": {
      "name": "Diretoria de Logística", "abbreviation": "DLog", "category": "Direção Setorial",
      "subordinadoA": "Comandante Geral", "legalRef": "Arts. 17, 95",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 17 (DLog)", "Art. 95 (Atribuições comuns dos Diretores)"],
      "atribuicoes": [
        "A DLog incumbe-se: I - do planejamento, da normatização, da fiscalização e do controle das atividades relativas à gestão da aquisição e da contratação para fornecimento de bens e prestação de serviços; II - da gestão da frota de viaturas e embarcações; III - da gestão do patrimônio e do material bélico da Corporação; IV - das atividades de manutenção de materiais e equipamentos; V - das atividades específicas de planejamento e gestão na área de serviços de engenharia, arquitetura e obras. (Art. 17 I–V)",
        "I - prestar assessoramento ao Comandante Geral em assuntos de sua competência;",
        "II - coordenar e gerenciar tecnicamente os programas e projetos executivos sob sua responsabilidade;",
        "III - contribuir para a manutenção da unidade de ação da Corporação, em conjunto com os demais órgãos integrantes de sua estrutura;",
        "IV - sugerir a adoção ou implantação de normas, medidas e procedimentos que visem o aperfeiçoamento da estrutura e do desempenho das atividades;",
        "V - coordenar a atuação dos órgãos e unidades subordinados, centralizando a demanda de serviços a eles destinada;",
        "VI - praticar os atos administrativos de rotina na sua órbita de competência;",
        "VII - preparar e discutir a proposta orçamentária da Diretoria ou Comando;",
        "VIII - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob sua supervisão, sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal;",
        "IX - encaminhar, anualmente, ao Subcomandante Geral da Corporação, relatório das atividades técnicas, administrativas e operacionais, conforme o caso, ou quando da transmissão de função;",
        "X - emitir pareceres em questões técnicas na sua esfera de atribuições;",
        "XI - desempenhar outras atribuições e tarefas compatíveis com a função e as que forem determinadas pelo Comando Geral da Corporação; e",
        "XII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 95 I–XII)"
      ],
      "desdobramentos": ["Divisão de Planejamento Logístico (DPL)", "Divisão de Controle de Contratos (DCC)", "Divisão de Controle de Patrimônio (DCP)", "Divisão de Controle de Transporte (DCT)", "Divisão de Compras e Serviços (DCS)"],
      "cargos": [{"cargo": "Diretor de Logística", "subordinadoA": "Comandante Geral", "requisito": "Oficial do CBMPE (Art. 94)", "desdobramentos": [], "atribuicoes": ["Responsável direto perante o Comandante Geral pelo funcionamento do sistema de logística (Art. 94)"]}]
    },
    "df-pe": {
      "name": "Diretoria de Finanças", "abbreviation": "DF", "category": "Direção Setorial",
      "subordinadoA": "Comandante Geral", "legalRef": "Arts. 19, 95",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 19 (DF)", "Art. 95 (Atribuições comuns dos Diretores)"],
      "atribuicoes": [
        "A DF incumbe-se do planejamento, da normatização, da execução e do controle financeiro do CBMPE (Art. 19)",
        "I - prestar assessoramento ao Comandante Geral em assuntos de sua competência;",
        "II - coordenar e gerenciar tecnicamente os programas e projetos executivos sob sua responsabilidade;",
        "III - contribuir para a manutenção da unidade de ação da Corporação, em conjunto com os demais órgãos integrantes de sua estrutura;",
        "IV - sugerir a adoção ou implantação de normas, medidas e procedimentos que visem o aperfeiçoamento da estrutura e do desempenho das atividades;",
        "V - coordenar a atuação dos órgãos e unidades subordinados, centralizando a demanda de serviços a eles destinada;",
        "VI - praticar os atos administrativos de rotina na sua órbita de competência;",
        "VII - preparar e discutir a proposta orçamentária da Diretoria ou Comando;",
        "VIII - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob sua supervisão, sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal;",
        "IX - encaminhar, anualmente, ao Subcomandante Geral da Corporação, relatório das atividades técnicas, administrativas e operacionais, conforme o caso, ou quando da transmissão de função;",
        "X - emitir pareceres em questões técnicas na sua esfera de atribuições;",
        "XI - desempenhar outras atribuições e tarefas compatíveis com a função e as que forem determinadas pelo Comando Geral da Corporação; e",
        "XII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 95 I–XII)"
      ],
      "desdobramentos": ["Divisão de Controle Orçamentário e Financeiro (DCOF)", "Divisão Administrativa e Financeira (DAF)"],
      "cargos": [{"cargo": "Diretor de Finanças", "subordinadoA": "Comandante Geral", "requisito": "Oficial do CBMPE (Art. 94)", "desdobramentos": [], "atribuicoes": ["Responsável direto perante o Comandante Geral pelo funcionamento do sistema financeiro (Art. 94)"]}]
    },
    "dplag-pe": {
      "name": "Diretoria de Planejamento e Gestão", "abbreviation": "DPlaG", "category": "Direção Setorial",
      "subordinadoA": "Comandante Geral", "legalRef": "Arts. 21, 95",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 21 (DPlaG)", "Art. 95 (Atribuições comuns dos Diretores)"],
      "atribuicoes": [
        "A DPlaG incumbe-se: I - da elaboração e gestão do planejamento institucional; II - da proposição de normas, medidas e procedimentos que visem o aperfeiçoamento da gestão interna do CBMPE; III - do planejamento e monitoramento da execução do orçamento anual e do plano estratégico da Corporação; IV - da propositura e gestão de projetos e convênios com outros órgãos; e V - da gestão das atividades que envolvem o sistema de arrecadação dos tributos específicos destinados ao CBMPE. (Art. 21 I–V)",
        "I - prestar assessoramento ao Comandante Geral em assuntos de sua competência;",
        "II - coordenar e gerenciar tecnicamente os programas e projetos executivos sob sua responsabilidade;",
        "III - contribuir para a manutenção da unidade de ação da Corporação, em conjunto com os demais órgãos integrantes de sua estrutura;",
        "IV - sugerir a adoção ou implantação de normas, medidas e procedimentos que visem o aperfeiçoamento da estrutura e do desempenho das atividades;",
        "V - coordenar a atuação dos órgãos e unidades subordinados, centralizando a demanda de serviços a eles destinada;",
        "VI - praticar os atos administrativos de rotina na sua órbita de competência;",
        "VII - preparar e discutir a proposta orçamentária da Diretoria ou Comando;",
        "VIII - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob sua supervisão, sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal;",
        "IX - encaminhar, anualmente, ao Subcomandante Geral da Corporação, relatório das atividades técnicas, administrativas e operacionais, conforme o caso, ou quando da transmissão de função;",
        "X - emitir pareceres em questões técnicas na sua esfera de atribuições;",
        "XI - desempenhar outras atribuições e tarefas compatíveis com a função e as que forem determinadas pelo Comando Geral da Corporação; e",
        "XII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 95 I–XII)"
      ],
      "desdobramentos": ["Divisão de Planejamento e Gestão (DPG)", "Divisão de Projetos (DProj)", "Divisão de Convênios (DConv)", "Divisão de Arrecadação Tributária (DTA)"],
      "cargos": [{"cargo": "Diretor de Planejamento e Gestão", "subordinadoA": "Comandante Geral", "requisito": "Oficial do CBMPE (Art. 94)", "desdobramentos": [], "atribuicoes": ["Responsável direto perante o Comandante Geral pelo funcionamento do sistema de planejamento (Art. 94)"]}]
    },
    "dim-pe": {
      "name": "Diretoria Integrada Metropolitana", "abbreviation": "DIM", "category": "Direção Setorial",
      "subordinadoA": "Comandante Geral", "legalRef": "Arts. 23, 95",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 23 (DIM)", "Art. 95 (Atribuições comuns dos Diretores)"],
      "atribuicoes": [
        "A DIM incumbe-se, na área territorial de Recife e sua Região Metropolitana, do planejamento e supervisão das ordens, doutrina e emprego das atividades operacionais de prevenção e combate a incêndio, atendimento pré-hospitalar e salvamento, além do controle operacional dos atendimentos emergenciais e do gerenciamento das ações de respostas aos desastres (Art. 23)",
        "I - prestar assessoramento ao Comandante Geral em assuntos de sua competência;",
        "II - coordenar e gerenciar tecnicamente os programas e projetos executivos sob sua responsabilidade;",
        "III - contribuir para a manutenção da unidade de ação da Corporação, em conjunto com os demais órgãos integrantes de sua estrutura;",
        "IV - sugerir a adoção ou implantação de normas, medidas e procedimentos que visem o aperfeiçoamento da estrutura e do desempenho das atividades;",
        "V - coordenar a atuação dos órgãos e unidades subordinados, centralizando a demanda de serviços a eles destinada;",
        "VI - praticar os atos administrativos de rotina na sua órbita de competência;",
        "VII - preparar e discutir a proposta orçamentária da Diretoria ou Comando;",
        "VIII - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob sua supervisão, sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal;",
        "IX - encaminhar, anualmente, ao Subcomandante Geral da Corporação, relatório das atividades técnicas, administrativas e operacionais, conforme o caso, ou quando da transmissão de função;",
        "X - emitir pareceres em questões técnicas na sua esfera de atribuições;",
        "XI - desempenhar outras atribuições e tarefas compatíveis com a função e as que forem determinadas pelo Comando Geral da Corporação; e",
        "XII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 95 I–XII)"
      ],
      "desdobramentos": ["Comando Operacional Metropolitano (COM)", "Centro de Controle Operacional (CCO)", "Centro de Resposta a Desastres (CRD)"],
      "cargos": [{"cargo": "Diretor Integrado Metropolitano", "subordinadoA": "Comandante Geral", "requisito": "Oficial do CBMPE (Art. 94)", "desdobramentos": [], "atribuicoes": ["Responsável pelo planejamento e supervisão das atividades operacionais na RMR (Art. 23)"]}]
    },
    "diesp-pe": {
      "name": "Diretoria Integrada Especializada", "abbreviation": "DIEsp", "category": "Direção Setorial",
      "subordinadoA": "Comandante Geral", "legalRef": "Arts. 25, 95",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 25 (DIEsp)", "Art. 95 (Atribuições comuns dos Diretores)"],
      "atribuicoes": [
        "A DIEsp incumbe-se na área territorial do Estado de Pernambuco, do planejamento e supervisão das ordens, doutrina e emprego das atividades técnicas, notadamente as vistorias, análises de projetos, cadastramento e credenciamento de empresas, e a execução das normas que disciplinam a segurança das pessoas e de seus bens contra incêndio e pânico, na forma prevista na legislação específica (Art. 25)",
        "I - prestar assessoramento ao Comandante Geral em assuntos de sua competência;",
        "II - coordenar e gerenciar tecnicamente os programas e projetos executivos sob sua responsabilidade;",
        "III - contribuir para a manutenção da unidade de ação da Corporação, em conjunto com os demais órgãos integrantes de sua estrutura;",
        "IV - sugerir a adoção ou implantação de normas, medidas e procedimentos que visem o aperfeiçoamento da estrutura e do desempenho das atividades;",
        "V - coordenar a atuação dos órgãos e unidades subordinados, centralizando a demanda de serviços a eles destinada;",
        "VI - praticar os atos administrativos de rotina na sua órbita de competência;",
        "VII - preparar e discutir a proposta orçamentária da Diretoria ou Comando;",
        "VIII - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob sua supervisão, sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal;",
        "IX - encaminhar, anualmente, ao Subcomandante Geral da Corporação, relatório das atividades técnicas, administrativas e operacionais, conforme o caso, ou quando da transmissão de função;",
        "X - emitir pareceres em questões técnicas na sua esfera de atribuições;",
        "XI - desempenhar outras atribuições e tarefas compatíveis com a função e as que forem determinadas pelo Comando Geral da Corporação; e",
        "XII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 95 I–XII)"
      ],
      "desdobramentos": ["Comando Operacional Especializado (COEsp)"],
      "cargos": [{"cargo": "Diretor Integrado Especializado", "subordinadoA": "Comandante Geral", "requisito": "Oficial do CBMPE (Art. 94)", "desdobramentos": [], "atribuicoes": ["Responsável pelo planejamento e supervisão das atividades técnicas no Estado (Art. 25)"]}]
    },
    "dinter1-pe": {
      "name": "Diretoria Integrada do Interior/1", "abbreviation": "DInter/1", "category": "Direção Setorial",
      "subordinadoA": "Comandante Geral", "legalRef": "Arts. 27, 95",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 27 (DInter/1)", "Art. 95 (Atribuições comuns dos Diretores)"],
      "atribuicoes": [
        "A DInter/1 incumbe-se, na área territorial da Zona da Mata e Agreste do Estado, do planejamento e supervisão das ordens, doutrina e emprego das atividades operacionais de prevenção e combate a incêndio, atendimento pré-hospitalar e salvamento (Art. 27)",
        "I - prestar assessoramento ao Comandante Geral em assuntos de sua competência;",
        "II - coordenar e gerenciar tecnicamente os programas e projetos executivos sob sua responsabilidade;",
        "III - contribuir para a manutenção da unidade de ação da Corporação, em conjunto com os demais órgãos integrantes de sua estrutura;",
        "IV - sugerir a adoção ou implantação de normas, medidas e procedimentos que visem o aperfeiçoamento da estrutura e do desempenho das atividades;",
        "V - coordenar a atuação dos órgãos e unidades subordinados, centralizando a demanda de serviços a eles destinada;",
        "VI - praticar os atos administrativos de rotina na sua órbita de competência;",
        "VII - preparar e discutir a proposta orçamentária da Diretoria ou Comando;",
        "VIII - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob sua supervisão, sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal;",
        "IX - encaminhar, anualmente, ao Subcomandante Geral da Corporação, relatório das atividades técnicas, administrativas e operacionais, conforme o caso, ou quando da transmissão de função;",
        "X - emitir pareceres em questões técnicas na sua esfera de atribuições;",
        "XI - desempenhar outras atribuições e tarefas compatíveis com a função e as que forem determinadas pelo Comando Geral da Corporação; e",
        "XII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 95 I–XII)"
      ],
      "desdobramentos": ["Comando Operacional do Interior/1 (COInter/1)"],
      "cargos": [{"cargo": "Diretor Integrado do Interior/1", "subordinadoA": "Comandante Geral", "requisito": "Oficial do CBMPE (Art. 94)", "desdobramentos": [], "atribuicoes": ["Responsável pelo planejamento e supervisão das atividades operacionais na Zona da Mata e Agreste (Art. 27)"]}]
    },
    "dinter2-pe": {
      "name": "Diretoria Integrada do Interior/2", "abbreviation": "DInter/2", "category": "Direção Setorial",
      "subordinadoA": "Comandante Geral", "legalRef": "Arts. 29, 95",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 29 (DInter/2)", "Art. 95 (Atribuições comuns dos Diretores)"],
      "atribuicoes": [
        "A DInter/2 incumbe-se, na área territorial do Sertão do Estado, do planejamento e supervisão das ordens, doutrina e emprego das atividades operacionais de prevenção e combate a incêndio, atendimento pré-hospitalar e salvamento (Art. 29)",
        "I - prestar assessoramento ao Comandante Geral em assuntos de sua competência;",
        "II - coordenar e gerenciar tecnicamente os programas e projetos executivos sob sua responsabilidade;",
        "III - contribuir para a manutenção da unidade de ação da Corporação, em conjunto com os demais órgãos integrantes de sua estrutura;",
        "IV - sugerir a adoção ou implantação de normas, medidas e procedimentos que visem o aperfeiçoamento da estrutura e do desempenho das atividades;",
        "V - coordenar a atuação dos órgãos e unidades subordinados, centralizando a demanda de serviços a eles destinada;",
        "VI - praticar os atos administrativos de rotina na sua órbita de competência;",
        "VII - preparar e discutir a proposta orçamentária da Diretoria ou Comando;",
        "VIII - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob sua supervisão, sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal;",
        "IX - encaminhar, anualmente, ao Subcomandante Geral da Corporação, relatório das atividades técnicas, administrativas e operacionais, conforme o caso, ou quando da transmissão de função;",
        "X - emitir pareceres em questões técnicas na sua esfera de atribuições;",
        "XI - desempenhar outras atribuições e tarefas compatíveis com a função e as que forem determinadas pelo Comando Geral da Corporação; e",
        "XII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 95 I–XII)"
      ],
      "desdobramentos": ["Comando Operacional do Interior/2 (COInter/2)"],
      "cargos": [{"cargo": "Diretor Integrado do Interior/2", "subordinadoA": "Comandante Geral", "requisito": "Oficial do CBMPE (Art. 94)", "desdobramentos": [], "atribuicoes": ["Responsável pelo planejamento e supervisão das atividades operacionais no Sertão (Art. 29)"]}]
    },
    "gcg-pe": {
      "name": "Gabinete do Comandante Geral", "abbreviation": "GCG", "category": "Apoio",
      "subordinadoA": "Comandante Geral", "legalRef": "Arts. 43, 96",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 43 (GCG)", "Art. 96 (Atribuições comuns dos Chefes de Apoio)"],
      "atribuicoes": [
        "O GCG tem a seu cargo as funções de assistência e assessoramento direto ao Comandante Geral, bem como a articulação junto aos órgãos legislativos, na esfera federal, estadual e municipal, em assuntos de interesse do CBMPE; desempenha ainda a secretaria do CPE (Arts. 43, 13 §1º)",
        "I - exercer com dedicação e zelo a administração do respectivo órgão, buscando sempre alcançar uma melhoria do nível de prestação de serviços;",
        "II - exercer as atribuições que lhes forem cometidas por lei, regulamento ou qualquer outro documento normativo vigente na Corporação;",
        "III - baixar determinações, ordens ou diretrizes, no âmbito do respectivo órgão, visando à execução dos serviços que lhes são afetos;",
        "IV - propor soluções, ao titular do escalão imediatamente superior para quaisquer dificuldades surgidas no desempenho das atividades de seu órgão;",
        "V - apresentar relatórios ao escalão superior, na periodicidade que for estabelecida em regulamentos, regimentos, diretrizes, normas ou instrução;",
        "VI - aprovar pareceres, estudos e laudos elaborados no âmbito do referido órgão, relacionados com assuntos de interesse da Corporação;",
        "VII - supervisionar a administração dos recursos postos à disposição do órgão, estabelecendo prioridades e fiscalizando a plena obediência às disposições legais e regulamentares vigentes referentes à administração financeira e orçamentária;",
        "VIII - exercer outras atividades, encargos ou missões que lhe sejam atribuídos por disposições normativas vigentes ou pelo escalão superior;",
        "IX - dirigir, controlar, supervisionar e avaliar a atuação dos órgãos subordinados, centralizando a demanda de serviços a eles destinados, buscando facilitar o cumprimento dos objetivos setoriais; e",
        "X - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 96 I–X)"
      ],
      "desdobramentos": ["Divisão de Apoio (DAp)"],
      "cargos": [{"cargo": "Chefe do Gabinete do Comandante Geral", "subordinadoA": "Comandante Geral", "requisito": "Oficial do CBMPE (Art. 44)", "desdobramentos": [], "atribuicoes": ["Assistência e assessoramento direto ao Comandante Geral (Art. 43)"]}]
    },
    "aj-pe": {
      "name": "Assessoria Jurídica", "abbreviation": "AJ", "category": "Apoio",
      "subordinadoA": "Comandante Geral", "legalRef": "Arts. 45, 96",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 45 (AJ)", "Art. 96 (Atribuições comuns dos Chefes de Apoio)"],
      "atribuicoes": [
        "A AJ é o órgão que presta assessoramento jurídico ao Comando Geral e desempenho das atividades jurídicas previstas em legislação vigente (Art. 45)",
        "I - exercer com dedicação e zelo a administração do respectivo órgão, buscando sempre alcançar uma melhoria do nível de prestação de serviços;",
        "II - exercer as atribuições que lhes forem cometidas por lei, regulamento ou qualquer outro documento normativo vigente na Corporação;",
        "III - baixar determinações, ordens ou diretrizes, no âmbito do respectivo órgão, visando à execução dos serviços que lhes são afetos;",
        "IV - propor soluções, ao titular do escalão imediatamente superior para quaisquer dificuldades surgidas no desempenho das atividades de seu órgão;",
        "V - apresentar relatórios ao escalão superior, na periodicidade que for estabelecida em regulamentos, regimentos, diretrizes, normas ou instrução;",
        "VI - aprovar pareceres, estudos e laudos elaborados no âmbito do referido órgão, relacionados com assuntos de interesse da Corporação;",
        "VII - supervisionar a administração dos recursos postos à disposição do órgão, estabelecendo prioridades e fiscalizando a plena obediência às disposições legais e regulamentares vigentes referentes à administração financeira e orçamentária;",
        "VIII - exercer outras atividades, encargos ou missões que lhe sejam atribuídos por disposições normativas vigentes ou pelo escalão superior;",
        "IX - dirigir, controlar, supervisionar e avaliar a atuação dos órgãos subordinados, centralizando a demanda de serviços a eles destinados, buscando facilitar o cumprimento dos objetivos setoriais; e",
        "X - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 96 I–X)"
      ],
      "desdobramentos": ["Seção de Legislação e Pareceres (SLP)"],
      "cargos": [{"cargo": "Assessor Jurídico", "subordinadoA": "Comandante Geral", "requisito": "Oficial do CBMPE (Art. 46)", "desdobramentos": [], "atribuicoes": ["Assessoramento jurídico ao Comando Geral (Art. 45)"]}]
    },
    "ajg-pe": {
      "name": "Ajudância Geral", "abbreviation": "AJG", "category": "Apoio",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Arts. 58, 96",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 58 (AJG)", "Art. 96 (Atribuições comuns dos Chefes de Apoio)"],
      "atribuicoes": [
        "A AJG incumbe-se da administração, manutenção, segurança das instalações do quartel do Comando Geral, bem como a gestão das publicações e arquivo geral da Corporação (Art. 58)",
        "I - exercer com dedicação e zelo a administração do respectivo órgão, buscando sempre alcançar uma melhoria do nível de prestação de serviços;",
        "II - exercer as atribuições que lhes forem cometidas por lei, regulamento ou qualquer outro documento normativo vigente na Corporação;",
        "III - baixar determinações, ordens ou diretrizes, no âmbito do respectivo órgão, visando à execução dos serviços que lhes são afetos;",
        "IV - propor soluções, ao titular do escalão imediatamente superior para quaisquer dificuldades surgidas no desempenho das atividades de seu órgão;",
        "V - apresentar relatórios ao escalão superior, na periodicidade que for estabelecida em regulamentos, regimentos, diretrizes, normas ou instrução;",
        "VI - aprovar pareceres, estudos e laudos elaborados no âmbito do referido órgão, relacionados com assuntos de interesse da Corporação;",
        "VII - supervisionar a administração dos recursos postos à disposição do órgão, estabelecendo prioridades e fiscalizando a plena obediência às disposições legais e regulamentares vigentes referentes à administração financeira e orçamentária;",
        "VIII - exercer outras atividades, encargos ou missões que lhe sejam atribuídos por disposições normativas vigentes ou pelo escalão superior;",
        "IX - dirigir, controlar, supervisionar e avaliar a atuação dos órgãos subordinados, centralizando a demanda de serviços a eles destinados, buscando facilitar o cumprimento dos objetivos setoriais; e",
        "X - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 96 I–X)"
      ],
      "desdobramentos": ["Divisão de Publicação e Apoio (DPA)", "Divisão Administrativa (DA)"],
      "cargos": [{"cargo": "Chefe da Ajudância Geral", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial do CBMPE (Art. 59)", "desdobramentos": [], "atribuicoes": ["Administração, manutenção e segurança do quartel do CG; gestão das publicações e arquivo geral (Art. 58)"]}]
    },
    "cjd-pe": {
      "name": "Centro de Justiça e Disciplina", "abbreviation": "CJD", "category": "Apoio",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Arts. 60, 96",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 60 (CJD)", "Art. 96 (Atribuições comuns dos Chefes de Apoio)"],
      "atribuicoes": [
        "O CJD incumbe-se do assessoramento ao Subcomandante Geral nos assuntos pertinentes à execução e acompanhamento de processos administrativos disciplinares, sindicâncias e Inquéritos Policiais Militares (Art. 60)",
        "I - exercer com dedicação e zelo a administração do respectivo órgão, buscando sempre alcançar uma melhoria do nível de prestação de serviços;",
        "II - exercer as atribuições que lhes forem cometidas por lei, regulamento ou qualquer outro documento normativo vigente na Corporação;",
        "III - baixar determinações, ordens ou diretrizes, no âmbito do respectivo órgão, visando à execução dos serviços que lhes são afetos;",
        "IV - propor soluções, ao titular do escalão imediatamente superior para quaisquer dificuldades surgidas no desempenho das atividades de seu órgão;",
        "V - apresentar relatórios ao escalão superior, na periodicidade que for estabelecida em regulamentos, regimentos, diretrizes, normas ou instrução;",
        "VI - aprovar pareceres, estudos e laudos elaborados no âmbito do referido órgão, relacionados com assuntos de interesse da Corporação;",
        "VII - supervisionar a administração dos recursos postos à disposição do órgão, estabelecendo prioridades e fiscalizando a plena obediência às disposições legais e regulamentares vigentes referentes à administração financeira e orçamentária;",
        "VIII - exercer outras atividades, encargos ou missões que lhe sejam atribuídos por disposições normativas vigentes ou pelo escalão superior;",
        "IX - dirigir, controlar, supervisionar e avaliar a atuação dos órgãos subordinados, centralizando a demanda de serviços a eles destinados, buscando facilitar o cumprimento dos objetivos setoriais; e",
        "X - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 96 I–X)"
      ],
      "desdobramentos": ["Seções de Polícia Judiciária (SPJ)"],
      "cargos": [{"cargo": "Chefe do CJD", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial do CBMPE (Art. 61)", "desdobramentos": [], "atribuicoes": ["Assessoramento ao Subcomandante Geral em processos administrativos disciplinares, sindicâncias e IPM (Art. 60)"]}]
    },
    "cci-pe": {
      "name": "Centro de Controladoria Institucional", "abbreviation": "CCI", "category": "Apoio",
      "subordinadoA": "Subcomandante Geral", "legalRef": "Arts. 64, 96",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 64 (CCI)", "Art. 96 (Atribuições comuns dos Chefes de Apoio)"],
      "atribuicoes": [
        "O CCI incumbe-se do assessoramento ao Subcomandante Geral nos assuntos pertinentes aos atos de gestão do CBMPE, efetuando a orientação, acompanhamento e avaliação dos processos administrativos específicos desempenhados pelas OME, assegurando a regularidade e o fiel cumprimento dos princípios e normas estabelecidos pela Administração Pública (Art. 64)",
        "I - exercer com dedicação e zelo a administração do respectivo órgão, buscando sempre alcançar uma melhoria do nível de prestação de serviços;",
        "II - exercer as atribuições que lhes forem cometidas por lei, regulamento ou qualquer outro documento normativo vigente na Corporação;",
        "III - baixar determinações, ordens ou diretrizes, no âmbito do respectivo órgão, visando à execução dos serviços que lhes são afetos;",
        "IV - propor soluções, ao titular do escalão imediatamente superior para quaisquer dificuldades surgidas no desempenho das atividades de seu órgão;",
        "V - apresentar relatórios ao escalão superior, na periodicidade que for estabelecida em regulamentos, regimentos, diretrizes, normas ou instrução;",
        "VI - aprovar pareceres, estudos e laudos elaborados no âmbito do referido órgão, relacionados com assuntos de interesse da Corporação;",
        "VII - supervisionar a administração dos recursos postos à disposição do órgão, estabelecendo prioridades e fiscalizando a plena obediência às disposições legais e regulamentares vigentes referentes à administração financeira e orçamentária;",
        "VIII - exercer outras atividades, encargos ou missões que lhe sejam atribuídos por disposições normativas vigentes ou pelo escalão superior;",
        "IX - dirigir, controlar, supervisionar e avaliar a atuação dos órgãos subordinados, centralizando a demanda de serviços a eles destinados, buscando facilitar o cumprimento dos objetivos setoriais; e",
        "X - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 96 I–X)"
      ],
      "desdobramentos": ["1ª e 2ª Seções de Auditoria (SA)"],
      "cargos": [{"cargo": "Chefe do CCI", "subordinadoA": "Subcomandante Geral", "requisito": "Oficial do CBMPE (Art. 65)", "desdobramentos": [], "atribuicoes": ["Assessoramento ao Subcomandante Geral nos atos de gestão; orientação e avaliação dos processos das OME (Art. 64)"]}]
    },
    "com-pe": {
      "name": "Comando Operacional Metropolitano", "abbreviation": "COM", "category": "Direção Executiva",
      "subordinadoA": "Diretoria Integrada Metropolitana", "legalRef": "Arts. 33, 95",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 33 (COM)", "Art. 95 (Atribuições comuns dos Diretores)"],
      "atribuicoes": [
        "O COM incumbe-se da direção executiva na área territorial de Recife e sua Região Metropolitana, das atividades operacionais de combate a incêndio, salvamento e atendimento pré-hospitalar (Art. 33)",
        "I - prestar assessoramento ao Comandante Geral em assuntos de sua competência;",
        "II - coordenar e gerenciar tecnicamente os programas e projetos executivos sob sua responsabilidade;",
        "III - contribuir para a manutenção da unidade de ação da Corporação, em conjunto com os demais órgãos integrantes de sua estrutura;",
        "IV - sugerir a adoção ou implantação de normas, medidas e procedimentos que visem o aperfeiçoamento da estrutura e do desempenho das atividades;",
        "V - coordenar a atuação dos órgãos e unidades subordinados, centralizando a demanda de serviços a eles destinada;",
        "VI - praticar os atos administrativos de rotina na sua órbita de competência;",
        "VII - preparar e discutir a proposta orçamentária da Diretoria ou Comando;",
        "VIII - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob sua supervisão, sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal;",
        "IX - encaminhar, anualmente, ao Subcomandante Geral da Corporação, relatório das atividades técnicas, administrativas e operacionais, conforme o caso, ou quando da transmissão de função;",
        "X - emitir pareceres em questões técnicas na sua esfera de atribuições;",
        "XI - desempenhar outras atribuições e tarefas compatíveis com a função e as que forem determinadas pelo Comando Geral da Corporação; e",
        "XII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 95 I–XII)"
      ],
      "desdobramentos": ["Grupamento de Bombeiros de Incêndio (GBI)", "Grupamento de Atendimento Pré-Hospitalar (GBAPH)", "Grupamento de Bombeiros Marítimo (GBMar)", "Grupamento de Bombeiros de Salvamento (GBS)"],
      "cargos": [{"cargo": "Comandante Operacional Metropolitano", "subordinadoA": "DIM", "requisito": "Oficial do CBMPE (Art. 94)", "desdobramentos": [], "atribuicoes": ["Direção executiva das atividades operacionais na RMR (Art. 33)"]}]
    },
    "coesp-pe": {
      "name": "Comando Operacional Especializado", "abbreviation": "COEsp", "category": "Direção Executiva",
      "subordinadoA": "Diretoria Integrada Especializada", "legalRef": "Arts. 35, 95",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 35 (COEsp)", "Art. 95 (Atribuições comuns dos Diretores)"],
      "atribuicoes": [
        "O COEsp incumbe-se da direção executiva das atividades técnicas na área territorial do Estado (Art. 35)",
        "I - prestar assessoramento ao Comandante Geral em assuntos de sua competência;",
        "II - coordenar e gerenciar tecnicamente os programas e projetos executivos sob sua responsabilidade;",
        "III - contribuir para a manutenção da unidade de ação da Corporação, em conjunto com os demais órgãos integrantes de sua estrutura;",
        "IV - sugerir a adoção ou implantação de normas, medidas e procedimentos que visem o aperfeiçoamento da estrutura e do desempenho das atividades;",
        "V - coordenar a atuação dos órgãos e unidades subordinados, centralizando a demanda de serviços a eles destinada;",
        "VI - praticar os atos administrativos de rotina na sua órbita de competência;",
        "VII - preparar e discutir a proposta orçamentária da Diretoria ou Comando;",
        "VIII - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob sua supervisão, sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal;",
        "IX - encaminhar, anualmente, ao Subcomandante Geral da Corporação, relatório das atividades técnicas, administrativas e operacionais, conforme o caso, ou quando da transmissão de função;",
        "X - emitir pareceres em questões técnicas na sua esfera de atribuições;",
        "XI - desempenhar outras atribuições e tarefas compatíveis com a função e as que forem determinadas pelo Comando Geral da Corporação; e",
        "XII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 95 I–XII)"
      ],
      "desdobramentos": ["CAT/RMR", "CAT/Zona da Mata (CAT/ZM)", "CAT/Agreste", "CAT/Sertão I", "CAT/Sertão II"],
      "cargos": [{"cargo": "Comandante Operacional Especializado", "subordinadoA": "DIEsp", "requisito": "Oficial do CBMPE (Art. 94)", "desdobramentos": [], "atribuicoes": ["Direção executiva das atividades técnicas no Estado (Art. 35)"]}]
    },
    "cointer1-pe": {
      "name": "Comando Operacional do Interior/1", "abbreviation": "COInter/1", "category": "Direção Executiva",
      "subordinadoA": "Diretoria Integrada do Interior/1", "legalRef": "Arts. 37, 95",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 37 (COInter/1)", "Art. 95 (Atribuições comuns dos Diretores)"],
      "atribuicoes": [
        "O COInter/1 incumbe-se, na área territorial da Zona da Mata e Agreste, das atividades operacionais de combate a incêndio, salvamento e atendimento pré-hospitalar (Art. 37)",
        "I - prestar assessoramento ao Comandante Geral em assuntos de sua competência;",
        "II - coordenar e gerenciar tecnicamente os programas e projetos executivos sob sua responsabilidade;",
        "III - contribuir para a manutenção da unidade de ação da Corporação, em conjunto com os demais órgãos integrantes de sua estrutura;",
        "IV - sugerir a adoção ou implantação de normas, medidas e procedimentos que visem o aperfeiçoamento da estrutura e do desempenho das atividades;",
        "V - coordenar a atuação dos órgãos e unidades subordinados, centralizando a demanda de serviços a eles destinada;",
        "VI - praticar os atos administrativos de rotina na sua órbita de competência;",
        "VII - preparar e discutir a proposta orçamentária da Diretoria ou Comando;",
        "VIII - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob sua supervisão, sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal;",
        "IX - encaminhar, anualmente, ao Subcomandante Geral da Corporação, relatório das atividades técnicas, administrativas e operacionais, conforme o caso, ou quando da transmissão de função;",
        "X - emitir pareceres em questões técnicas na sua esfera de atribuições;",
        "XI - desempenhar outras atribuições e tarefas compatíveis com a função e as que forem determinadas pelo Comando Geral da Corporação; e",
        "XII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 95 I–XII)"
      ],
      "desdobramentos": ["1º Grupamento de Bombeiros (1ºGB)", "2º Grupamento de Bombeiros (2ºGB)", "6º Grupamento de Bombeiros (6ºGB)", "7º Grupamento de Bombeiros (7ºGB)"],
      "cargos": [{"cargo": "Comandante Operacional do Interior/1", "subordinadoA": "DInter/1", "requisito": "Oficial do CBMPE (Art. 94)", "desdobramentos": [], "atribuicoes": ["Direção executiva das atividades operacionais na Zona da Mata e Agreste (Art. 37)"]}]
    },
    "cointer2-pe": {
      "name": "Comando Operacional do Interior/2", "abbreviation": "COInter/2", "category": "Direção Executiva",
      "subordinadoA": "Diretoria Integrada do Interior/2", "legalRef": "Arts. 39, 95",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 39 (COInter/2)", "Art. 95 (Atribuições comuns dos Diretores)"],
      "atribuicoes": [
        "O COInter/2 incumbe-se, na área territorial do sertão, das atividades operacionais de combate a incêndio, salvamento e atendimento pré-hospitalar (Art. 39)",
        "I - prestar assessoramento ao Comandante Geral em assuntos de sua competência;",
        "II - coordenar e gerenciar tecnicamente os programas e projetos executivos sob sua responsabilidade;",
        "III - contribuir para a manutenção da unidade de ação da Corporação, em conjunto com os demais órgãos integrantes de sua estrutura;",
        "IV - sugerir a adoção ou implantação de normas, medidas e procedimentos que visem o aperfeiçoamento da estrutura e do desempenho das atividades;",
        "V - coordenar a atuação dos órgãos e unidades subordinados, centralizando a demanda de serviços a eles destinada;",
        "VI - praticar os atos administrativos de rotina na sua órbita de competência;",
        "VII - preparar e discutir a proposta orçamentária da Diretoria ou Comando;",
        "VIII - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob sua supervisão, sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal;",
        "IX - encaminhar, anualmente, ao Subcomandante Geral da Corporação, relatório das atividades técnicas, administrativas e operacionais, conforme o caso, ou quando da transmissão de função;",
        "X - emitir pareceres em questões técnicas na sua esfera de atribuições;",
        "XI - desempenhar outras atribuições e tarefas compatíveis com a função e as que forem determinadas pelo Comando Geral da Corporação; e",
        "XII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente. (Art. 95 I–XII)"
      ],
      "desdobramentos": ["3º Grupamento de Bombeiros (3ºGB)", "4º Grupamento de Bombeiros (4ºGB)", "5º Grupamento de Bombeiros (5ºGB)"],
      "cargos": [{"cargo": "Comandante Operacional do Interior/2", "subordinadoA": "DInter/2", "requisito": "Oficial do CBMPE (Art. 94)", "desdobramentos": [], "atribuicoes": ["Direção executiva das atividades operacionais no Sertão (Art. 39)"]}]
    },
    "cco-pe": {
      "name": "Centro de Controle Operacional", "abbreviation": "CCO", "category": "Execução",
      "subordinadoA": "Diretoria Integrada Metropolitana", "legalRef": "Arts. 85, 97",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 85 (CCO)", "Art. 97 (Atribuições comuns dos Comandantes de Execução)"],
      "atribuicoes": [
        "O CCO incumbe-se do recebimento e encaminhamento das solicitações de socorro e controle do atendimento emergencial realizado (Art. 85)",
        "I - administrar as atividades relativas à Unidade;",
        "II - cumprir e fazer cumprir, em sua área de ação, as diretrizes, planos, normas e ordens emanadas do escalão superior;",
        "III - planejar, comandar e fiscalizar as ações operacionais da unidade;",
        "IV - solicitar apoio ou reforço ao comando superior, quando necessário;",
        "V - comunicar imediatamente ao escalão superior qualquer fato ou situação em sua área de atuação, solicitando-lhe intervenção, se não for de sua competência providenciar a respeito;",
        "VI - informar ao comando a que estiver subordinado as principais ocorrências operacionais atendidas pela unidade;",
        "VII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente;",
        "VIII - zelar pela unidade e uniformidade da instrução e administração entre os órgãos subordinados;",
        "IX - planejar e operar as suas comunicações, de acordo com as normas vigentes;",
        "X - elaborar os documentos necessários à avaliação das atividades operacionais da Unidade, conforme normas estabelecidas pelo escalão superior;",
        "XI - comandar diretamente as ações que, pela gravidade, vulto, importância e complexidade assim o exigirem;",
        "XII - preparar e discutir a proposta orçamentária da unidade;",
        "XIII - encaminhar, mensalmente, ao comando do escalão superior, relatório das atividades técnicas, administrativas e operacionais executadas pela unidade;",
        "XIV - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob seu comando, adotando e sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal; e",
        "XV - exercer outros encargos que lhe forem atribuídos pelos escalões superiores. (Art. 97 I–XV)"
      ],
      "desdobramentos": ["Divisão de Operações (DOp)", "Seção de Radiocomunicação (SR)"],
      "cargos": [{"cargo": "Comandante do CCO", "subordinadoA": "DIM", "requisito": "Oficial do CBMPE (Art. 86)", "desdobramentos": [], "atribuicoes": ["Recebimento e encaminhamento das solicitações de socorro; controle do atendimento emergencial (Art. 85)"]}]
    },
    "crd-pe": {
      "name": "Centro de Resposta a Desastres", "abbreviation": "CRD", "category": "Execução",
      "subordinadoA": "Diretoria Integrada Metropolitana", "legalRef": "Arts. 87, 97",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 87 (CRD)", "Art. 97 (Atribuições comuns dos Comandantes de Execução)"],
      "atribuicoes": [
        "O CRD incumbe-se da articulação com o sistema de defesa civil, bem como pela coleta, processamento e atualização das informações estratégicas necessárias ao gerenciamento adequado das emergências, além dos estudos e monitoramento de ameaças de desastres (Art. 87)",
        "I - administrar as atividades relativas à Unidade;",
        "II - cumprir e fazer cumprir, em sua área de ação, as diretrizes, planos, normas e ordens emanadas do escalão superior;",
        "III - planejar, comandar e fiscalizar as ações operacionais da unidade;",
        "IV - solicitar apoio ou reforço ao comando superior, quando necessário;",
        "V - comunicar imediatamente ao escalão superior qualquer fato ou situação em sua área de atuação, solicitando-lhe intervenção, se não for de sua competência providenciar a respeito;",
        "VI - informar ao comando a que estiver subordinado as principais ocorrências operacionais atendidas pela unidade;",
        "VII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente;",
        "VIII - zelar pela unidade e uniformidade da instrução e administração entre os órgãos subordinados;",
        "IX - planejar e operar as suas comunicações, de acordo com as normas vigentes;",
        "X - elaborar os documentos necessários à avaliação das atividades operacionais da Unidade, conforme normas estabelecidas pelo escalão superior;",
        "XI - comandar diretamente as ações que, pela gravidade, vulto, importância e complexidade assim o exigirem;",
        "XII - preparar e discutir a proposta orçamentária da unidade;",
        "XIII - encaminhar, mensalmente, ao comando do escalão superior, relatório das atividades técnicas, administrativas e operacionais executadas pela unidade;",
        "XIV - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob seu comando, adotando e sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal; e",
        "XV - exercer outros encargos que lhe forem atribuídos pelos escalões superiores. (Art. 97 I–XV)"
      ],
      "desdobramentos": ["Divisão de Articulação e Planificação (DAP)", "Divisão de Monitoramento e Resposta (DMR)"],
      "cargos": [{"cargo": "Comandante do CRD", "subordinadoA": "DIM", "requisito": "Oficial do CBMPE (Art. 88)", "desdobramentos": [], "atribuicoes": ["Articulação com defesa civil; coleta e processamento de informações estratégicas; monitoramento de ameaças (Art. 87)"]}]
    },
    "cat-pe": {
      "name": "Centros de Atividades Técnicas", "abbreviation": "CAT", "category": "Execução",
      "subordinadoA": "Comando Operacional Especializado", "legalRef": "Arts. 89, 97",
      "baseLegal": "Lei nº 15.187, de 12 de dezembro de 2013",
      "artigosDeOrigem": ["Art. 89 (CATs)", "Art. 97 (Atribuições comuns dos Comandantes de Execução)"],
      "atribuicoes": [
        "Os CATs incumbem-se da execução das normas que disciplinam a segurança das pessoas e de seus bens contra incêndio e pânico, notadamente as vistorias, análises de projetos, cadastramento e credenciamento de empresas, nas áreas territoriais sob sua responsabilidade (Art. 89)",
        "I - administrar as atividades relativas à Unidade;",
        "II - cumprir e fazer cumprir, em sua área de ação, as diretrizes, planos, normas e ordens emanadas do escalão superior;",
        "III - planejar, comandar e fiscalizar as ações operacionais da unidade;",
        "IV - solicitar apoio ou reforço ao comando superior, quando necessário;",
        "V - comunicar imediatamente ao escalão superior qualquer fato ou situação em sua área de atuação, solicitando-lhe intervenção, se não for de sua competência providenciar a respeito;",
        "VI - informar ao comando a que estiver subordinado as principais ocorrências operacionais atendidas pela unidade;",
        "VII - fazer publicar no Boletim Interno (BI) da unidade todas as ordens, as ordens das autoridades superiores e fatos que sejam do interesse da unidade, em conformidade a legislação vigente;",
        "VIII - zelar pela unidade e uniformidade da instrução e administração entre os órgãos subordinados;",
        "IX - planejar e operar as suas comunicações, de acordo com as normas vigentes;",
        "X - elaborar os documentos necessários à avaliação das atividades operacionais da Unidade, conforme normas estabelecidas pelo escalão superior;",
        "XI - comandar diretamente as ações que, pela gravidade, vulto, importância e complexidade assim o exigirem;",
        "XII - preparar e discutir a proposta orçamentária da unidade;",
        "XIII - encaminhar, mensalmente, ao comando do escalão superior, relatório das atividades técnicas, administrativas e operacionais executadas pela unidade;",
        "XIV - controlar e avaliar o desempenho dos recursos humanos lotados nos órgãos sob seu comando, adotando e sugerindo medidas relacionadas à execução de programas de treinamento e desenvolvimento de pessoal; e",
        "XV - exercer outros encargos que lhe forem atribuídos pelos escalões superiores. (Art. 97 I–XV)"
      ],
      "desdobramentos": ["CAT/RMR (Recife e RMR)", "CAT/ZM (Zona da Mata Norte e Sul)", "CAT/Agreste (Agreste Setentrional, Central e Meridional)", "CAT/Sertão I (Pajeú, Moxotó, Itaparica)", "CAT/Sertão II (Sertão Central, Araripe, São Francisco)"],
      "cargos": [{"cargo": "Comandante do CAT", "subordinadoA": "COEsp", "requisito": "Oficial do CBMPE (Art. 90)", "desdobramentos": [], "atribuicoes": ["Execução das normas de segurança contra incêndio e pânico; vistorias, análises de projetos, cadastramento e credenciamento (Art. 89)"]}]
    },
  }
},

"pi": {
  "legal_source": "Lei nº 5.949, de 17 de dezembro de 2009 (alterada pela Lei nº 7.772, de 04 de abril de 2022)",
  "organs": {
    "cg-pi": {
      "name": "Comando Geral", "abbreviation": "CG", "category": "Direção Geral",
      "subordinadoA": "Governador do Estado", "legalRef": "Arts. 7, 13",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 7 (Órgãos de Direção Geral)", "Art. 13 (cargo de Comandante-Geral)"],
      "atribuicoes": [
        "O cargo de Comandante-Geral do Corpo de Bombeiros Militar do Estado do Piauí é privativo de oficial do último posto da Corporação, integrante do Quadro de Oficiais Bombeiros Militar Combatentes a ser nomeado pelo Governador do Estado. (Art. 13, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Comandante-Geral", "Subcomandante-Geral", "Alto Comando"],
      "cargos": [{"cargo": "Comandante-Geral", "subordinadoA": "Governador do Estado", "requisito": "Coronel do Quadro de Oficiais Bombeiros Militar Combatentes (Art. 13, 7.772)", "desdobramentos": [], "atribuicoes": ["Privativo de oficial do último posto da Corporação, integrante do QOBMC, a ser nomeado pelo Governador do Estado (Art. 13, 7.772)"]}]
    },
    "scg-pi": {
      "name": "Subcomandante-Geral", "abbreviation": "SCG", "category": "Direção Geral",
      "subordinadoA": "Comando Geral", "legalRef": "Arts. 14, 15",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 14 (atribuições do SCG)", "Art. 15 (cargo de SCG)"],
      "atribuicoes": [
        "O Subcomandante-Geral do Corpo de Bombeiro Militar do Estado do Piauí, acumula a função de Chefe do Estado-Maior-Geral, sendo o substituto imediato do Comandante-Geral, cumprindo-lhe substituí-lo em suas faltas ou impedimentos e desempenhar outras atribuições previstas em leis ou regulamentos, ou mediante expressa delegação do Comandante-Geral. (Art. 14, Lei nº 7.772/2022)"
      ],
      "desdobramentos": [],
      "cargos": [{"cargo": "Subcomandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Coronel do Quadro de Oficiais Bombeiros Militar Combatentes — seu substituto em faltas ou impedimentos é o coronel mais antigo do mesmo quadro (Art. 15, 7.772)", "desdobramentos": [], "atribuicoes": ["Acumula a função de Chefe do Estado-Maior-Geral; substituto imediato do CG (Art. 14, 7.772)"]}]
    },
    "alto-comando-pi": {
      "name": "Alto Comando", "abbreviation": "AC", "category": "Direção Geral",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 16",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 16 (Alto Comando)", "Art. 16 §2° I–VIII (pautas deliberativas)"],
      "atribuicoes": [
        "I - emprego de pessoal;",
        "II - ensino e instrução;",
        "III - controle interno;",
        "IV - disciplina;",
        "V - legislação;",
        "VI - projetos e convênios;",
        "VII - processos de promoções em grau de recurso;",
        "VIII - outros assuntos de interesse da Corporação. (Art. 16 §2° I–VIII, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Presidente: Comandante-Geral", "Vice-presidente: Subcomandante-Geral", "Diretor de Gestão de Pessoas", "Diretor de Ensino, Instrução e Pesquisa", "Diretor Administrativo e Financeiro", "Comandante Operacional de Bombeiros", "Secretaria"],
      "cargos": [{"cargo": "Presidente do Alto Comando", "subordinadoA": "—", "requisito": "Comandante-Geral (Art. 16 I, 7.772)", "desdobramentos": [], "atribuicoes": ["Convoca o Alto Comando para decidir em forma de colegiado sobre as pautas do Art. 16 §2° (7.772)"]}]
    },
    "emg-pi": {
      "name": "Estado-Maior-Geral", "abbreviation": "EMG", "category": "Assessoramento",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 28-A",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 28-A (EMG — acrescido pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "O Estado-Maior-Geral, encarregado da elaboração das diretrizes e ordens do comando, tem por missão o estudo, o planejamento, a coordenação, a programação orçamentária e financeira e o controle de todas as atividades da Corporação, por intermédio dos órgãos de direção setorial, de apoio e de execução, no exercício de suas competências, em conformidade com as decisões e diretrizes do Comandante-Geral do Corpo de Bombeiros Militar do Estado do Piaui. (Art. 28-A, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Chefe do Estado-Maior-Geral (Ch EMG)", "Subchefe do Estado-Maior-Geral (Sub Ch EMG)", "Secretaria", "1ª Seção — SEPLO", "2ª Seção — SEICI", "3ª Seção — SECPT", "4ª Seção — SEGEL", "5ª Seção — SERPACS"],
      "cargos": [{"cargo": "Chefe do Estado-Maior-Geral", "subordinadoA": "Subcomandante-Geral", "requisito": "Acumulado pelo Subcomandante-Geral (Art. 14, 7.772)", "desdobramentos": [], "atribuicoes": ["Chefia do EMG acumulada pelo SCG (Art. 14, 7.772)"]}]
    },
    "gcg-pi": {
      "name": "Gabinete do Comandante-Geral", "abbreviation": "GAB.CBMT", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 23",
      "baseLegal": "Lei nº 5.949, de 17 de dezembro de 2009",
      "artigosDeOrigem": ["Art. 23 (Gabinete do Comando Geral)"],
      "atribuicoes": [
        "Ao Gabinete do Comando Geral compete acompanhar os trabalhos das assessorias e comissões de caráter temporário, assessorar o Comandante Geral nos assuntos de controle interno, produzir informações estratégicas com vistas ao preparo e emprego do Corpo de Bombeiros Militar e desempenhar as funções de apoio administrativo, serviços gerais e os trabalhos de secretaria do comando geral. (Art. 23, Lei nº 5.949/2009)"
      ],
      "desdobramentos": ["Chefe", "Comissão de Promoções de Oficiais", "Ajudante de Ordens", "Ouvidoria", "Assessoria Técnica III", "Assessoria Técnica II", "Assistência de Serviços II", "Seção de Arquivo"],
      "cargos": [{"cargo": "Chefe do Gabinete do Comandante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do CBMEPI — o Chefe de Gabinete do CG é o Secretário do Alto Comando (Art. 16 §1°, 7.772)", "desdobramentos": [], "atribuicoes": ["Assessora o CG nos assuntos de controle interno e produz informações estratégicas (Art. 23, 5.949)"]}]
    },
    "gab-scg-pi": {
      "name": "Gabinete do Subcomandante-Geral", "abbreviation": "GAB.SUBCMT", "category": "Assessoramento",
      "subordinadoA": "Subcomandante-Geral", "legalRef": "Art. 24",
      "baseLegal": "Lei nº 5.949, de 17 de dezembro de 2009",
      "artigosDeOrigem": ["Art. 24 (Gabinete do Subcomando-Geral)"],
      "atribuicoes": [
        "Ao Gabinete do Subcomando-Geral compete assessorar o Subcomandante Geral nos assuntos relativos à justiça e disciplina bem como supervisionar os serviços diários desenvolvidos pela Corporação. (Art. 24, Lei nº 5.949/2009)"
      ],
      "desdobramentos": ["Chefe", "Comissão de Promoções de Praças", "Ajudante de Ordens", "Assessor Técnico II", "Assessor Técnico I", "Assistência de Serviços I"],
      "cargos": [{"cargo": "Chefe do Gabinete do Subcomandante-Geral", "subordinadoA": "Subcomandante-Geral", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Assessora o SCG nos assuntos de justiça e disciplina e supervisiona os serviços diários da Corporação (Art. 24, 5.949)"]}]
    },
    "nee-pi": {
      "name": "Núcleo de Estudos Estratégicos", "abbreviation": "NEE", "category": "Assessoramento",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 25",
      "baseLegal": "Lei nº 5.949, de 17 de dezembro de 2009",
      "artigosDeOrigem": ["Art. 25 (NEE)"],
      "atribuicoes": [
        "O Núcleo de Estudos Estratégicos é o órgão encarregado da realização de estudos em todas as áreas de atuação da Corporação, com vistas à permanente construção de um sistema de segurança pública na área de bombeiros e de defesa civil capaz de responder às demandas da sociedade. (Art. 25, Lei nº 5.949/2009)"
      ],
      "desdobramentos": ["Chefe", "Adjunto", "Coordenação de Projetos", "Seção de Estatística", "Seção de Estudos Prospectivos"],
      "cargos": [{"cargo": "Chefe do Núcleo de Estudos Estratégicos", "subordinadoA": "Comando Geral", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Realização de estudos estratégicos em todas as áreas de atuação da Corporação (Art. 25, 5.949)"]}]
    },
    "ndc-pi": {
      "name": "Núcleo de Defesa Civil", "abbreviation": "NDC", "category": "Assessoramento",
      "subordinadoA": "Comando Operacional de Bombeiros", "legalRef": "Art. 26",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 26 (NDC — nova redação pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "O Núcleo de Defesa Civil é órgão de assessoramento do Comando Operacional de Bombeiros responsável pelo planejamento e execução de atividades de defesa civil na área de competência do Corpo de Bombeiros. (Art. 26, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Chefe", "Seção de Defesa Civil da Capital", "Seção de Defesa Civil do Interior"],
      "cargos": [{"cargo": "Chefe do Núcleo de Defesa Civil", "subordinadoA": "Comandante Operacional de Bombeiros", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Planejamento e execução de atividades de defesa civil na área de competência do CBM (Art. 26, 7.772)"]}]
    },
    "ajg-pi": {
      "name": "Ajudância Geral", "abbreviation": "AJG", "category": "Assessoramento",
      "subordinadoA": "Comandante-Geral", "legalRef": "Art. 27",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 27 (AJG — nova redação pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "A Ajudância Geral, subordinada diretamente ao Comandante Geral, compete a publicação dos atos administrativos, recepção de correspondências, assim como auxiliar nas funções de administração, conservação e segurança das instalações do Quartel do Comando Geral (QCG), considerado como Organização de Bombeiros Militar. (Art. 27, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Ajudante-Geral", "Secretaria Administrativa", "Seção de Comando, Serviços e Segurança (SCS)", "Seção de Arquivo"],
      "cargos": [{"cargo": "Ajudante-Geral", "subordinadoA": "Comandante-Geral", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Publicação dos atos administrativos, recepção de correspondências e funções de administração, conservação e segurança do QCG (Art. 27, 7.772)"]}]
    },
    "nci-pi": {
      "name": "Núcleo de Controle Interno", "abbreviation": "NCI", "category": "Assessoramento",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 28",
      "baseLegal": "Lei nº 5.949, de 17 de dezembro de 2009",
      "artigosDeOrigem": ["Art. 28 (NCI)"],
      "atribuicoes": [
        "Ao Núcleo de Controle Interno compete acompanhar a implementação, pelos órgãos e suas unidades administrativas, das recomendações da Procuradoria Geral do Estado, da Controladoria-Geral do Estado e do Tribunal de Contas do Estado. (Art. 28, Lei nº 5.949/2009)"
      ],
      "desdobramentos": ["Chefe", "Coordenador", "Auxiliares"],
      "cargos": [{"cargo": "Chefe do Núcleo de Controle Interno", "subordinadoA": "Comando Geral", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Acompanha implementação das recomendações da PGE, CGE e TCE (Art. 28, 5.949)"]}]
    },
    "dgp-pi": {
      "name": "Diretoria de Gestão de Pessoas", "abbreviation": "DGP", "category": "Direção Setorial",
      "subordinadoA": "Comando Geral", "legalRef": "Arts. 17, 18",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 17 (competência geral das Diretorias)", "Art. 18 (DGP)"],
      "atribuicoes": [
        "A Diretoria de Gestão de Pessoas, órgão de direção setorial do sistema de pessoal, incumbe-se do planejamento, da coordenação, da execução, do controle, e da fiscalização das atividades relacionadas à pessoal. (Art. 18, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Seção de Folha e Cadastro (DGP-1)", "Seção de Promoções e Movimentações (DGP-2)", "Seção de Identificação e Ingresso (DGP-3)", "Seção de Inativos e Pensionistas (DGP-4)", "Seção de Atos (DGP-5)", "Seção de Justiça e Disciplina (DGP-6)", "Núcleo de Voluntários da Reserva Remunerada"],
      "cargos": [{"cargo": "Diretor de Gestão de Pessoas", "subordinadoA": "Comando Geral", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Direção do sistema de pessoal (Art. 18, 7.772)"]}]
    },
    "daf-pi": {
      "name": "Diretoria Administrativa e Financeira", "abbreviation": "DAF", "category": "Direção Setorial",
      "subordinadoA": "Comando Geral", "legalRef": "Arts. 17, 19",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 17 (competência geral das Diretorias)", "Art. 19 (DAF)"],
      "atribuicoes": [
        "A Diretoria Administrativa e Financeira, o órgão de direção setorial responsável pelo funcionamento do sistema de administração financeira, programação, orçamento, contabilidade, incumbindo ainda o estudo, o planejamento, a orientação normativa, a coordenação, supervisão, o controle e a execução das atividades relativas à gestão do material e patrimônio da corporação. (Art. 19, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Seção Administrativa Financeira (DAF-1)", "Seção de Orçamento, Compras e Contabilidade (DAF-2)", "Seção de Cadastro, Controle e Alienação do Patrimônio (DAF-3)", "Seção de Administração de Frota (DAF-4)", "Seção de Controle de Armas e Munições (DAF-5)"],
      "cargos": [{"cargo": "Diretor Administrativo e Financeiro", "subordinadoA": "Comando Geral", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Direção do sistema de administração financeira e gestão do material e patrimônio (Art. 19, 7.772)"]}]
    },
    "deip-pi": {
      "name": "Diretoria de Ensino, Instrução e Pesquisa", "abbreviation": "DEIP", "category": "Direção Setorial",
      "subordinadoA": "Comando Geral", "legalRef": "Arts. 17, 20",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 17 (competência geral das Diretorias)", "Art. 20 (DEIP)"],
      "atribuicoes": [
        "A Diretoria de Ensino, Instrução e Pesquisa, o órgão de direção setorial do sistema de ensino e instrução, incumbe-se do planejamento, da coordenação, do controle e da fiscalização de todas as atividades de formação, aperfeiçoamento e especialização, nos diferentes níveis do ensino, do adestramento e da instrução. (Art. 20, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Seção Técnica de Ensino (DEIP-1)", "Seção de Curso e Estágios (DEIP-2)", "Seção de Pesquisa e Doutrina (DEIP-3)", "Banda de Música"],
      "cargos": [{"cargo": "Diretor de Ensino, Instrução e Pesquisa", "subordinadoA": "Comando Geral", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Direção do sistema de ensino e instrução (Art. 20, 7.772)"]}]
    },
    "dsci-pi": {
      "name": "Diretoria de Segurança Contra Incêndio", "abbreviation": "DSCI", "category": "Direção Setorial",
      "subordinadoA": "Comando Geral", "legalRef": "Arts. 17, 21",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 17 (competência geral das Diretorias)", "Art. 21 (DSCI)"],
      "atribuicoes": [
        "A Diretoria de Segurança Contra Incêndio, unidade administrativa responsável pelo planejamento, análise, controle e fiscalização das atividades atinentes à segurança contra incêndio e pânico no âmbito do Estado do Piauí. (Art. 21, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Seção de Análise de Projetos (DSCI-1)", "Seção de Vistorias e Pareceres (DSCI-2)", "Seção de Fiscalização (DSCI-3)", "Seção de Apoio Técnico (DSCI-4)", "Seção de Estatística e Arquivo (DSCI-5)"],
      "cargos": [{"cargo": "Diretor de Segurança Contra Incêndio", "subordinadoA": "Comando Geral", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Planejamento, análise, controle e fiscalização das atividades de segurança contra incêndio e pânico (Art. 21, 7.772)"]}]
    },
    "ceman-pi": {
      "name": "Centro de Manutenção", "abbreviation": "CEMAN", "category": "Apoio",
      "subordinadoA": "Diretoria Administrativa e Financeira", "legalRef": "Art. 29",
      "baseLegal": "Lei nº 5.949, de 17 de dezembro de 2009",
      "artigosDeOrigem": ["Art. 29 (CEMAN)"],
      "atribuicoes": [
        "O Centro de Manutenção é órgão encarregado da manutenção das instalações dos quartéis, viaturas e manutenção de equipamentos de telecomunicações e operacionais da Corporação. (Art. 29, Lei nº 5.949/2009)"
      ],
      "desdobramentos": ["Chefe", "Seção de Manutenção", "Seção de Equipamentos Operacionais", "Seção de Equipamentos de Telecomunicações"],
      "cargos": [{"cargo": "Chefe do Centro de Manutenção", "subordinadoA": "Diretoria Administrativa e Financeira", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Manutenção das instalações dos quartéis, viaturas e equipamentos (Art. 29, 5.949)"]}]
    },
    "csm-pi": {
      "name": "Centro de Suprimento de Material", "abbreviation": "CSM", "category": "Apoio",
      "subordinadoA": "Diretoria Administrativa e Financeira", "legalRef": "Art. 30",
      "baseLegal": "Lei nº 5.949, de 17 de dezembro de 2009",
      "artigosDeOrigem": ["Art. 30 (CSM)"],
      "atribuicoes": [
        "O Centro de Suprimento de Material é órgão encarregado de atender as necessidades básicas de subsistência da Corporação. (Art. 30, Lei nº 5.949/2009)"
      ],
      "desdobramentos": ["Chefe", "Seção de Controle e Distribuição", "Almoxarifado"],
      "cargos": [{"cargo": "Chefe do Centro de Suprimento de Material", "subordinadoA": "Diretoria Administrativa e Financeira", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Atende as necessidades básicas de subsistência da Corporação (Art. 30, 5.949)"]}]
    },
    "cto-pi": {
      "name": "Centro de Treinamento Operacional", "abbreviation": "CTO", "category": "Apoio",
      "subordinadoA": "Diretoria de Ensino, Instrução e Pesquisa", "legalRef": "Art. 31",
      "baseLegal": "Lei nº 5.949, de 17 de dezembro de 2009",
      "artigosDeOrigem": ["Art. 31 (CTO)"],
      "atribuicoes": [
        "O Centro de Treinamento Operacional é órgão encarregado da realização de treinamentos técnicos operacionais de combate a incêndio, salvamento aquático e salvamento em altura da Corporação. (Art. 31, Lei nº 5.949/2009)"
      ],
      "desdobramentos": ["Chefe", "Adjunto", "Seção de Incêndio", "Seção de Salvamento Aquático e Mergulho", "Seção de Salvamento em Altura", "Seção de Salvamento Terrestre", "Pelotões Operacionais", "Pelotão Administrativo"],
      "cargos": [{"cargo": "Chefe do Centro de Treinamento Operacional", "subordinadoA": "Diretoria de Ensino, Instrução e Pesquisa", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Treinamentos técnicos operacionais de combate a incêndio, salvamento aquático e em altura (Art. 31, 5.949)"]}]
    },
    "cafd-pi": {
      "name": "Centro de Atividades Físicas e Desportos", "abbreviation": "CAFD", "category": "Apoio",
      "subordinadoA": "Diretoria de Ensino, Instrução e Pesquisa", "legalRef": "Art. 32-A",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 32-A (CAFD — acrescido pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "O Centro de Atividades Físicas e Desportos é um órgão de apoio da Diretoria de Ensino, Instrução e Pesquisa, competindo-lhe desenvolver programas específicos de condicionamento físico e desportos da corporação. (Art. 32-A, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Chefe", "Subchefe", "Seção de Avaliação e Reabilitação Física", "Seção de Condicionamento Físico", "Academia"],
      "cargos": [{"cargo": "Chefe do CAFD", "subordinadoA": "Diretoria de Ensino, Instrução e Pesquisa", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Desenvolver programas de condicionamento físico e desportos da corporação (Art. 32-A, 7.772)"]}]
    },
    "ceib-pi": {
      "name": "Centro de Ensino e Instrução de Bombeiros", "abbreviation": "CEIB", "category": "Apoio",
      "subordinadoA": "Diretoria de Ensino, Instrução e Pesquisa", "legalRef": "Art. 32-B",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 32-B (CEIB — acrescido pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "O Centro de Ensino e Instrução de Bombeiros é o órgão de apoio da Diretoria de Ensino, Instrução e Pesquisa, incumbido da formação, habilitação, aperfeiçoamento, especialização, treinamento e da instrução especializada dos bombeiros militar do Corpo de Bombeiros Militar do Estado do Piauí e, eventualmente, de bombeiros de outras corporações. (Art. 32-B, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Comandante", "Subcomandante", "Seção de Administração", "Seção Pedagógica", "Comando do Corpo de Alunos"],
      "cargos": [{"cargo": "Comandante do CEIB", "subordinadoA": "Diretoria de Ensino, Instrução e Pesquisa", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Formação, habilitação, aperfeiçoamento e instrução especializada dos BM (Art. 32-B, 7.772)"]}]
    },
    "coc-pi": {
      "name": "Centro de Operações e Comunicações", "abbreviation": "COC", "category": "Apoio",
      "subordinadoA": "Comando Operacional de Bombeiros", "legalRef": "Art. 32",
      "baseLegal": "Lei nº 5.949, de 17 de dezembro de 2009",
      "artigosDeOrigem": ["Art. 32 (COC)"],
      "atribuicoes": [
        "O Centro de Operações e Comunicações é o órgão responsável pela execução dos serviços de comunicação das ações operacionais. (Art. 32, Lei nº 5.949/2009)"
      ],
      "desdobramentos": ["Chefe", "Seção de Operações", "Seção de Comunicações", "Seção de Apoio"],
      "cargos": [{"cargo": "Chefe do Centro de Operações e Comunicações", "subordinadoA": "Comando Operacional de Bombeiros", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Execução dos serviços de comunicação das ações operacionais (Art. 32, 5.949)"]}]
    },
    "ns-pi": {
      "name": "Núcleo de Saúde", "abbreviation": "NS", "category": "Apoio",
      "subordinadoA": "Diretoria de Gestão de Pessoas", "legalRef": "Art. 32-C",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 32-C (Núcleo de Saúde — acrescido pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "O Núcleo de Saúde é responsável pelo planejamento, orientação, coordenação, controle e execução de programas de medicina preventiva, saúde comunitária e controle médico-sanitário de pessoal, execução das atividades de assistência médica, odontológica, bem como pelas perícias médicas e homologar os pareceres da junta Médica de Saúde (JMS) no âmbito da corporação. (Art. 32-C, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Chefe", "Perícias Médicas (PM)", "Junta Médica de Saúde (JMS)", "Seção Médica e Odontológica", "Seção de Psicologia", "Seção de Enfermagem", "Seção de Apoio Administrativo"],
      "cargos": [{"cargo": "Chefe do Núcleo de Saúde", "subordinadoA": "Diretoria de Gestão de Pessoas", "requisito": "Oficial Superior do Quadro de Oficiais Bombeiros Militar de Saúde da Corporação (Art. 32-C §2°, 7.772)", "desdobramentos": [], "atribuicoes": ["Planejamento e execução de programas de medicina preventiva, saúde comunitária, assistência médica e perícias (Art. 32-C, 7.772)"]}]
    },
    "cob-pi": {
      "name": "Comando Operacional de Bombeiros", "abbreviation": "COB", "category": "Execução",
      "subordinadoA": "Comando Geral", "legalRef": "Art. 34",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 34 (COB — nova redação pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "O Comando Operacional de Bombeiros é órgão de execução do mais alto escalão do sistema operacional subordinado ao órgão de direção geral, tendo a seu cargo o planejamento estratégico e a fiscalização do emprego dos Comandos Regionais de Bombeiros. (Art. 34, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Comandante Operacional de Bombeiros", "Subcomandante Operacional de Bombeiros", "Seção Administrativa", "Seção de Operações e Comunicações", "Seção de Controle e Fiscalização de Hidrantes", "Seção de Planejamento, Estatística e Avaliação Operacional", "Núcleo de Investigação e Prevenção de Incêndios", "Comandos Regionais de Bombeiros Militar"],
      "cargos": [
        {"cargo": "Comandante Operacional de Bombeiros", "subordinadoA": "Comandante-Geral", "requisito": "Coronel do Quadro de Oficiais Bombeiros Militar Combatentes (Art. 34 §2°, 7.772)", "desdobramentos": [], "atribuicoes": ["Planejamento estratégico e fiscalização do emprego dos CRBMs (Art. 34, 7.772)"]},
        {"cargo": "Subcomandante Operacional de Bombeiros", "subordinadoA": "Comandante Operacional de Bombeiros", "requisito": "Tenente-Coronel do Quadro de Oficiais Bombeiros Militar Combatentes (Art. 34 §2°, 7.772)", "desdobramentos": [], "atribuicoes": ["Substituto do Comandante Operacional de Bombeiros (Art. 34 §2°, 7.772)"]}
      ]
    },
    "nipi-pi": {
      "name": "Núcleo de Investigação e Prevenção de Incêndios", "abbreviation": "NIPI", "category": "Execução",
      "subordinadoA": "Comando Operacional de Bombeiros", "legalRef": "Art. 35",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 35 (NIPI — nova redação pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "O Núcleo de Investigação e Prevenção de Incêndios destina-se a realizar as análises laboratoriais relacionadas a investigação de incêndios e de explosões, emitir conclusões técnicas sobre atividades preventivas. (Art. 35, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Chefe", "Subchefe", "Seção de Perícias", "Seção de Pesquisas", "Laboratório"],
      "cargos": [{"cargo": "Chefe do NIPI", "subordinadoA": "Comando Operacional de Bombeiros", "requisito": "Oficial do CBMEPI", "desdobramentos": [], "atribuicoes": ["Análises laboratoriais de investigação de incêndios/explosões e conclusões técnicas preventivas (Art. 35, 7.772)"]}]
    },
    "crbm-i-pi": {
      "name": "Comando Regional de Bombeiros Militar do Meio-Norte", "abbreviation": "CRBM-I", "category": "Execução",
      "subordinadoA": "Comando Operacional de Bombeiros", "legalRef": "Art. 36",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 36 (CRBMs — nova redação pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "Os Comandos Regionais de Bombeiros Militar são órgãos de execução subordinados diretamente ao Comandante Operacional de Bombeiros, devem efetuar o planejamento operacional, a supervisão, a coordenação, prevenção, o controle, a fiscalização e a execução das atividades de bombeiro no âmbito de suas respectivas responsabilidades e circunscrições. (Art. 36, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Comandante", "Subcomandante", "Seção Administrativa", "Seção de Planejamento e Avaliação Operacional", "Seção de Comunicações e Logística", "Seção de Estatística", "Grupamentos de Bombeiros Militar", "Grupamento de Bombeiros Militar Marítimo"],
      "cargos": [{"cargo": "Comandante do CRBM-I", "subordinadoA": "Comandante Operacional de Bombeiros", "requisito": "Oficial do penúltimo posto do Quadro de Oficiais Bombeiros Militar Combatentes — Tenente-Coronel (Art. 36 §2°, 7.772)", "desdobramentos": [], "atribuicoes": ["Planejamento operacional, supervisão, coordenação e execução das atividades de bombeiro na macrorregião do Meio-Norte (Art. 36, 7.772)"]}]
    },
    "crbm-ii-pi": {
      "name": "Comando Regional de Bombeiros Militar do Litoral", "abbreviation": "CRBM-II", "category": "Execução",
      "subordinadoA": "Comando Operacional de Bombeiros", "legalRef": "Art. 36",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 36 (CRBMs — nova redação pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "Os Comandos Regionais de Bombeiros Militar são órgãos de execução subordinados diretamente ao Comandante Operacional de Bombeiros, devem efetuar o planejamento operacional, a supervisão, a coordenação, prevenção, o controle, a fiscalização e a execução das atividades de bombeiro no âmbito de suas respectivas responsabilidades e circunscrições. (Art. 36, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Comandante", "Subcomandante", "Seção Administrativa", "Seção de Planejamento e Avaliação Operacional", "Seção de Comunicações e Logística", "Seção de Estatística", "Grupamentos de Bombeiros Militar"],
      "cargos": [{"cargo": "Comandante do CRBM-II", "subordinadoA": "Comandante Operacional de Bombeiros", "requisito": "Oficial do penúltimo posto do Quadro de Oficiais Bombeiros Militar Combatentes — Tenente-Coronel (Art. 36 §2°, 7.772)", "desdobramentos": [], "atribuicoes": ["Planejamento operacional, supervisão, coordenação e execução das atividades de bombeiro na macrorregião do Litoral (Art. 36, 7.772)"]}]
    },
    "crbm-iii-pi": {
      "name": "Comando Regional de Bombeiros Militar do Semiárido", "abbreviation": "CRBM-III", "category": "Execução",
      "subordinadoA": "Comando Operacional de Bombeiros", "legalRef": "Art. 36",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 36 (CRBMs — nova redação pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "Os Comandos Regionais de Bombeiros Militar são órgãos de execução subordinados diretamente ao Comandante Operacional de Bombeiros, devem efetuar o planejamento operacional, a supervisão, a coordenação, prevenção, o controle, a fiscalização e a execução das atividades de bombeiro no âmbito de suas respectivas responsabilidades e circunscrições. (Art. 36, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Comandante", "Subcomandante", "Seção Administrativa", "Seção de Planejamento e Avaliação Operacional", "Seção de Comunicações e Logística", "Seção de Estatística", "Grupamentos de Bombeiros Militar"],
      "cargos": [{"cargo": "Comandante do CRBM-III", "subordinadoA": "Comandante Operacional de Bombeiros", "requisito": "Oficial do penúltimo posto do Quadro de Oficiais Bombeiros Militar Combatentes — Tenente-Coronel (Art. 36 §2°, 7.772)", "desdobramentos": [], "atribuicoes": ["Planejamento operacional, supervisão, coordenação e execução das atividades de bombeiro na macrorregião do Semiárido (Art. 36, 7.772)"]}]
    },
    "crbm-iv-pi": {
      "name": "Comando Regional de Bombeiros Militar do Cerrados", "abbreviation": "CRBM-IV", "category": "Execução",
      "subordinadoA": "Comando Operacional de Bombeiros", "legalRef": "Art. 36",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 36 (CRBMs — nova redação pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "Os Comandos Regionais de Bombeiros Militar são órgãos de execução subordinados diretamente ao Comandante Operacional de Bombeiros, devem efetuar o planejamento operacional, a supervisão, a coordenação, prevenção, o controle, a fiscalização e a execução das atividades de bombeiro no âmbito de suas respectivas responsabilidades e circunscrições. (Art. 36, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Comandante", "Subcomandante", "Seção Administrativa", "Seção de Planejamento e Avaliação Operacional", "Seção de Comunicações e Logística", "Seção de Estatística", "Grupamentos de Bombeiros Militar"],
      "cargos": [{"cargo": "Comandante do CRBM-IV", "subordinadoA": "Comandante Operacional de Bombeiros", "requisito": "Oficial do penúltimo posto do Quadro de Oficiais Bombeiros Militar Combatentes — Tenente-Coronel (Art. 36 §2°, 7.772)", "desdobramentos": [], "atribuicoes": ["Planejamento operacional, supervisão, coordenação e execução das atividades de bombeiro na macrorregião dos Cerrados (Art. 36, 7.772)"]}]
    },
    "gbm-pi": {
      "name": "Grupamento de Bombeiros Militar", "abbreviation": "GBM", "category": "Execução",
      "subordinadoA": "Comando Regional de Bombeiros Militar", "legalRef": "Art. 37",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 37 (GBM — nova redação pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "Os Grupamentos de Bombeiros Militar têm a seu cargo, dentro de uma determinada área operacional, as missões de prevenção e extinção de incêndios, busca, salvamento, atendimento pré-hospitalar e auxílio nas atividades de defesa civil. (Art. 37, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Comandante", "Subcomandante", "Administrativa", "Seção de Planejamento Operacional", "Seção de Logística", "Seção de Estatística", "Seção de Serviços Técnicos", "Subgrupamentos de Bombeiros Militar"],
      "cargos": [{"cargo": "Comandante do GBM", "subordinadoA": "Comando Regional de Bombeiros Militar", "requisito": "Oficial Superior do Quadro de Oficiais Bombeiros Militar Combatentes — excepcionalmente por Oficiais Superiores de outros quadros (Art. 37 §2°, 7.772)", "desdobramentos": [], "atribuicoes": ["Prevenção e extinção de incêndios, busca, salvamento, APH e defesa civil na área operacional (Art. 37, 7.772)"]}]
    },
    "gbmar-pi": {
      "name": "Grupamento de Bombeiros Militar Marítimo", "abbreviation": "GBMar", "category": "Execução",
      "subordinadoA": "Comando Regional de Bombeiros Militar do Litoral", "legalRef": "Art. 38",
      "baseLegal": "Lei nº 7.772, de 04 de abril de 2022",
      "artigosDeOrigem": ["Art. 38 (GBMar — nova redação pela Lei nº 7.772/2022)"],
      "atribuicoes": [
        "O Grupamento de Bombeiros Militar Marítimo tem a seu cargo a realização de operações aquáticas com a finalidade de executar serviços de prevenção em eventos náuticos, a busca, salvamentos de pessoas e bens, combate a incêndio em embarcações e instalações portuárias, bem como a preservação ambiental limitada às orlas fluviais e lacustre inscritas nos limites geográficos dos municípios de Ilha Grande de Santa Isabel, Parnaíba, Luís Correia e Cajueiro da Praia, assim como de toda a costa marítima piauiense. (Art. 38, Lei nº 7.772/2022)"
      ],
      "desdobramentos": ["Comandante", "Subcomandante", "Seção Administrativa", "Seção de Planejamento Operacional e Estatística", "Seção de Logística e Comunicações", "Seção de Capacitação Técnico-Profissional", "Subgrupamentos de Bombeiros Militar Marítimo (SGBMar)"],
      "cargos": [{"cargo": "Comandante do GBMar", "subordinadoA": "Comando Regional de Bombeiros Militar do Litoral", "requisito": "Major do Quadro de Oficiais Bombeiros Militar Combatentes (Art. 38 §único, 7.772)", "desdobramentos": [], "atribuicoes": ["Operações aquáticas, prevenção em eventos náuticos, busca/salvamento, combate a incêndio em embarcações e preservação ambiental na costa piauiense (Art. 38, 7.772)"]}]
    }
  }
},

}
