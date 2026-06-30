# curated_organs.py — Estruturas organizacionais curadas manualmente
# Fonte: legislações oficiais de cada estado (LOB + Regimento/NGA quando disponível)

def _n(id_, name, abbr=None, rank=None, desc=None, ref=None, children=None, cat=None):
    """Cria um nó de órgão."""
    node = {"id": id_, "name": name, "children": children or []}
    if abbr:  node["abbreviation"] = abbr
    if rank:  node["rank"] = rank
    if desc:  node["description"] = desc
    if ref:   node["legalRef"] = ref
    if cat:   node["category"] = cat
    return node


CURATED_ORGANS = {

# ════════════════════════════════════════════════════════════
# RONDÔNIA — Minuta LOB 2025 (SEI 0004.013288/2024-28)
# ════════════════════════════════════════════════════════════
"ro": [
    _n("cg","Comando Geral","CG","Coronel QOEMBM",
       "Órgão máximo executivo do CBMRO, incumbido da administração superior.",
       "Art. 11-12 — Minuta LOB 2025", cat="Direção Geral", children=[
        _n("condeg","Conselho Deliberativo de Estratégia e Gestão","CONDEG",
           desc="Órgão de direção colegiada.", cat="Colegiado"),
        _n("dir-set","Órgãos de Direção Setorial", cat="Direção Setorial", children=[
            _n("dp","Diretoria de Pessoal","DP"),
            _n("deei","Diretoria de Ensino, Educação e Instrução","DEEI"),
            _n("dpof","Diretoria de Planejamento, Orçamento e Finanças","DPOF"),
            _n("dsap","Diretoria de Saúde e Assistência ao Pessoal","DSAP"),
            _n("dlog","Diretoria de Logística","DLOG"),
            _n("dpo","Diretoria de Planejamento Operacional","DPO"),
            _n("doe","Diretoria Operacional Especializada","DOE"),
            _n("cot","Comando de Operações Técnicas","COT"),
            _n("cint","Coordenadoria de Inteligência","CINT"),
            _n("ccs","Coordenadoria de Comunicação Social","CCS"),
            _n("cinf","Coordenadoria de Informática","CINF"),
        ]),
        _n("dir-reg","Órgãos de Direção Regional", cat="Direção Regional", children=[
            _n("crbm","Comandos Regionais de Bombeiro Militar","CRBM"),
        ]),
    ]),
    _n("assess","Órgãos de Assessoramento", cat="Assessoramento",
       desc="Prestam assessoria, consultoria e orientação técnica.",
       ref="Art. 7 — Minuta LOB 2025", children=[
        _n("ai","Assessoria Institucional"),
        _n("ae","Assessoria Especial"),
        _n("al","Assessoria Legislativa"),
        _n("ap","Assessoria Parlamentar"),
        _n("apge","Assessoria de Projetos e Gestão Estratégica"),
        _n("af","Assessoria Fundacional"),
        _n("aci","Assessoria de Controle Interno"),
    ]),
    _n("apoio","Órgãos de Apoio", cat="Apoio",
       desc="Realizam as atividades-meio da Corporação.",
       ref="Art. 8 — Minuta LOB 2025", children=[
        _n("ap-cg","Apoio ao Comando-Geral", children=[
            _n("gab-cg","Gabinete do Comando Geral"),
            _n("comissoes","Comissões"),
            _n("conselhos","Conselhos"),
        ]),
        _n("ap-scg","Apoio ao Subcomando-Geral", children=[
            _n("gab-scg","Gabinete do Subcomando-Geral"),
            _n("ajudancia","Ajudância-Geral"),
        ]),
        _n("ap-emg","Apoio ao Estado-Maior Geral", children=[
            _n("gab-emg","Gabinete do Estado-Maior Geral"),
            _n("ap-set","Órgãos de Apoio Setorial"),
        ]),
    ]),
    _n("exec","Órgãos de Execução", cat="Execução",
       desc="Incumbidos da tradução das políticas nas atividades-fim.",
       ref="Art. 9 — Minuta LOB 2025", children=[
        _n("exec-ord","Atuação Operacional Ordinária", children=[
            _n("bbm","Batalhão de Bombeiros Militar","BBM"),
            _n("cat","Coordenadoria de Atividades Técnicas","CAT"),
        ]),
        _n("exec-esp","Atuação Operacional Especializada Terrestre", children=[
            _n("bbs","Batalhão de Busca e Salvamento","BBS"),
            _n("bifea","Batalhão de Incêndio Florestal e Emergências Ambientais","BIFEA"),
        ]),
        _n("exec-aer","Atuação Operacional Especializada Aérea", children=[
            _n("boa","Batalhão de Operações Aéreas","BOA"),
        ]),
        _n("exec-mun","Atuação Operacional Conveniada Municipal", children=[
            _n("gbm","Grupo de Bombeiros Militar","GBM"),
        ]),
    ]),
    _n("corregedoria","Órgãos de Correição", cat="Correição",
       desc="Exercem as funções de Corregedoria-Geral.",
       ref="Art. 10 — Minuta LOB 2025"),
],

# ════════════════════════════════════════════════════════════
# ACRE — Lei nº 3.105/2015 (altera Lei nº 2.009/2008)
# ════════════════════════════════════════════════════════════
"ac": [
    _n("dir-ger","Órgãos de Direção Geral", cat="Direção Geral",
       ref="Lei nº 3.105/2015, Art. 4º, I", children=[
        _n("cmt-g","Comandante-Geral","","Coronel BM"),
        _n("scmt-g","Subcomandante-Geral","","Coronel BM"),
        _n("emg","Estado-Maior Geral","EMG"),
        _n("correg","Corregedoria do CBMAC"),
        _n("ajg-ac","Ajudância Geral","AjG","Tenente-Coronel BM"),
    ]),
    _n("dir-set","Órgãos de Direção Setorial", cat="Direção Setorial",
       ref="Lei nº 3.105/2015, Art. 4º, II", children=[
        _n("drh","Diretoria de Recursos Humanos","DRH","Oficial Superior"),
        _n("datop","Diretoria de Atividades Técnicas e Operacionais","DATOP","Oficial Superior"),
        _n("dlpf","Diretoria de Logística, Patrimônio e Finanças","DLPF","Oficial Superior"),
        _n("dei","Diretoria de Ensino e Instrução","DEI","Oficial Superior"),
        _n("dp","Diretoria de Planejamento","DP","Oficial Superior"),
        _n("ds","Diretoria de Saúde","DS","Oficial Superior"),
        _n("comissoes","Comissões"),
        _n("ass-jur","Assessoria Jurídica"),
        _n("ass-int","Assessoria de Inteligência"),
        _n("ass-com","Assessoria de Comunicação Social e Imprensa"),
        _n("ctrl-int","Controle Interno"),
    ]),
    _n("dir-exec","Órgãos de Direção Executiva", cat="Direção Executiva",
       ref="Lei nº 3.105/2015, Art. 4º, III", children=[
        _n("cmd-cap","Comando Operacional — Capital e Entorno","","Ten.-Coronel BM", children=[
            _n("1bepcif","1º BEPCIF","1º BEPCIF"),
            _n("2bepcif","2º BEPCIF","2º BEPCIF"),
            _n("3bepcif","3º BEPCIF","3º BEPCIF"),
            _n("1bbs","1º Batalhão de Busca e Salvamento","1º BBS"),
            _n("1ciaciaer","1ª Cia. de Combate a Incêndio em Aeródromos","1ª CIACIAER"),
        ]),
        _n("cmd-int","Comando Operacional — Interior","","Ten.-Coronel BM", children=[
            _n("4bepcif","4º BEPCIF/CZS"),
            _n("5bepcif","5º BEPCIF/EPT"),
            _n("6bepcif","6º BEPCIF/SM"),
            _n("7bepcif","7º BEPCIF/TK"),
        ]),
    ]),
],

# ════════════════════════════════════════════════════════════
# DISTRITO FEDERAL — Lei nº 8.255/1991 + Portaria nº 24/2020
# ════════════════════════════════════════════════════════════
"df": [
    _n("cg","Comando-Geral","CG","Coronel QOBM/Comb.",
       "Órgão supremo de direção e administração do CBMDF.",
       "Lei nº 8.255/1991; Portaria nº 24/2020 (Regimento Interno)", cat="Direção Geral", children=[
        _n("alto-cmd","Alto Comando",desc="Órgão consultivo presidido pelo Comandante-Geral.",children=[
            _n("scg","Subcomandante-Geral","","Coronel QOBM/Comb."),
            _n("emg-chefe","Chefe do Estado-Maior-Geral","","Coronel QOBM/Comb."),
            _n("ctrl","Controlador"),
            _n("chgab","Chefe de Gabinete do Comandante-Geral"),
        ]),
        _n("gabcg","Gabinete do Comandante-Geral","GABCG",
           desc="Funções de assistência e assessoramento direto ao Comandante-Geral.", children=[
            _n("segep","Seção de Gestão de Processos","SEGEP"),
            _n("ajord","Ajudância de Ordens do Comandante-Geral","AJORD"),
            _n("seaad","Seção de Apoio Administrativo","SEAAD"),
            _n("astad","Assessoria Técnico-Administrativa","ASTAD", children=[
                _n("segod","Seção de Governança de Dados","SEGOD"),
                _n("segov","Seção de Governança Corporativa","SEGOV"),
                _n("seger","Seção de Gestão de Riscos","SEGER"),
            ]),
            _n("aspar","Assessoria Parlamentar e Relações Institucionais","ASPAR", children=[
                _n("separ","Seção de Assuntos Parlamentares","SEPAR"),
                _n("seain","Seção de Assuntos Institucionais","SEAIN"),
                _n("secer","Seção de Cerimonial","SECER"),
                _n("secap","Seção de Captação de Recursos","SECAP"),
            ]),
            _n("asjur","Assessoria Jurídico-Legislativa","ASJUR", children=[
                _n("sepai","Seção de Pessoal e Assuntos Institucionais","SEPAI"),
                _n("sapli","Seção de Análise de Procedimentos Licitatórios","SAPLI"),
            ]),
            _n("ascop","Assessoria para Acordos de Cooperação","ASCOP"),
        ]),
        _n("emg","Estado-Maior-Geral","EMG",
           "Coronel QOBM/Comb.",
           "Responsável pelo planejamento estratégico e orientação do preparo e emprego da Corporação.", children=[
            _n("emg-sec","Secretaria do EMG"),
            _n("emg-secoes","Seções do EMG (máximo 10)"),
        ]),
        _n("controladoria","Controladoria",
           desc="Assessoramento sobre defesa do patrimônio, auditoria, correição e ouvidoria.", children=[
            _n("auditoria","Auditoria"),
            _n("ouvidoria","Ouvidoria"),
            _n("corregedoria","Corregedoria"),
            _n("nuc-cust","Núcleo de Custódia"),
        ]),
        _n("ajg","Ajudância Geral","AjG",
           desc="Auxilia na administração do Quartel do Comando Geral."),
    ]),
    _n("deptos","Departamentos (máx. 6) e Diretorias", cat="Direção Setorial",
       desc="Exercem competências por meio de diretorias e órgãos diretamente subordinados.",
       ref="Lei nº 8.255/1991 Art. 13; Portaria nº 24/2020", children=[
        _n("drh-dep","Departamento de Recursos Humanos", children=[
            _n("dgp","Diretoria de Gestão de Pessoal","DGP"),
            _n("dip","Diretoria de Inativos e Pensionistas","DIP"),
            _n("dsau","Diretoria de Saúde","DSaú"),
        ]),
        _n("dal-dep","Departamento de Administração Logística e Financeira", children=[
            _n("dof","Diretoria de Orçamento e Finanças","DOF"),
            _n("dca","Diretoria de Contratações e Aquisições","DCA"),
            _n("dms","Diretoria de Materiais e Serviços","DMS"),
        ]),
        _n("dep-ensino","Departamento de Ensino, Pesquisa, Ciência e Tecnologia", children=[
            _n("dens","Diretoria de Ensino","DEns"),
            _n("dpct","Diretoria de Pesquisa, Ciência e Tecnologia","DPCT"),
            _n("dtic","Diretoria de Tecnologia da Informação e Comunicação","DTIC"),
        ]),
        _n("dep-sci","Departamento de Segurança Contra Incêndio", children=[
            _n("dvis","Diretoria de Vistorias","DVis"),
            _n("deap","Diretoria de Estudos e Análise de Projetos","DEAP"),
            _n("dii","Diretoria de Investigação de Incêndio","DII"),
        ]),
    ]),
    _n("apoio","Órgãos de Apoio", cat="Apoio",
       ref="Lei nº 8.255/1991 Art. 24; Portaria nº 24/2020", children=[
        _n("abm","Academia de Bombeiro Militar","ABM",
           desc="Formação e aperfeiçoamento de oficiais e cadetes."),
        _n("poli-med","Policlínica Médica"),
        _n("poli-odont","Policlínica Odontológica"),
        _n("ccs","Centro de Comunicação Social"),
        _n("cint","Centro de Inteligência"),
        _n("cpmed","Centro de Perícias Médicas"),
        _n("cabm","Centro de Assistência Bombeiro Militar"),
        _n("ccf","Centro de Capacitação Física"),
        _n("cmev","Centro de Manutenção de Equipamentos e Viaturas"),
        _n("comp","Centro de Obras e Manutenção Predial"),
        _n("csm","Centro de Suprimento e Material"),
        _n("cepd","Centro de Estudos de Política, Estratégia e Doutrina"),
        _n("cfap","Centro de Formação e Aperfeiçoamento de Praças"),
        _n("cto","Centro de Treinamento Operacional"),
        _n("cmd-pii","Colégio Militar Dom Pedro II"),
    ]),
    _n("execucao","Órgãos de Execução", cat="Execução",
       ref="Lei nº 8.255/1991 Art. 28; Portaria nº 24/2020", children=[
        _n("cmd-op","Comando Operacional",
           desc="Organização de mais alto escalão de execução, com Estado-Maior próprio.", children=[
            _n("scmd-op","Subcomando Operacional"),
            _n("emop","Estado-Maior Operacional"),
            _n("cmds-area","Comandos de Área", children=[
                _n("gbm-area","Grupamentos de Bombeiro Militar","GBM"),
            ]),
        ]),
        _n("cmd-esp","Comando Especializado", children=[
            _n("gpciu","Grupamento de Prevenção e Combate a Incêndio Urbano","GPCIU"),
            _n("gbs","Grupamento de Busca e Salvamento","GBS"),
            _n("gaeph","Grupamento de Atendimento de Emergência Pré-Hospitalar","GAEPH"),
            _n("gpa","Grupamento de Proteção Ambiental","GPA"),
            _n("gpc","Grupamento de Proteção Civil","GPC"),
            _n("gao","Grupamento de Aviação Operacional","GAO"),
            _n("gbmm","Grupamento de Bombeiros Militar de Motomecanização","GBMM"),
        ]),
    ]),
],

# ════════════════════════════════════════════════════════════
# ALAGOAS — Lei nº 6.212/2000 + Regimento Interno (Dec. 408/2001)
# ════════════════════════════════════════════════════════════
"al": [
    _n("cg","Comando Geral", cat="Direção Geral",
       ref="Lei nº 6.212/2000", children=[
        _n("cmt","Comandante Geral","","Coronel QOBM/Comb."),
        _n("scmt","Subcomandante Geral","","Coronel QOBM/Comb."),
        _n("cpe","Conselho de Políticas Estratégicas",
           desc="Composto pelo CG, SCG, Chefe de Gabinete, Diretores, Corregedor, AjG e Cmd. Operacional."),
        _n("cedec","Coordenadoria Estadual de Defesa Civil","CEDEC", children=[
            _n("ass-tec-cedec","Assessoria Técnica"),
            _n("sec-exec-cedec","Secretaria Executiva", children=[
                _n("spl","Seção de Planejamento, Avaliação e Controle"),
                _n("scco","Seção de Coordenação e Controle Operacional"),
                _n("scc","Seção de Cadastro e Controle de Recursos"),
                _n("sa","Seção Administrativa"),
            ]),
        ]),
        _n("gab-cg","Gabinete do Comandante Geral", children=[
            _n("chgab","Chefia do Gabinete","","Tenente-Coronel QOBM/Comb."),
            _n("ajord","Ajudância de Ordem do CG","","Capitão QOBM/Comb."),
            _n("aic","Assessoria de Inteligência e Contra-Inteligência","","Major QOBM/Comb."),
            _n("arpc","Assessoria de Relações Públicas e Comunicação Social","","Ten.-Coronel", children=[
                _n("imp","Subseção de Imprensa e Marketing"),
                _n("rp","Subseção de Relações Públicas, Publicidade e Propaganda"),
            ]),
            _n("sec-adm","Secretaria Administrativa", children=[
                _n("ctrl-cg","Subseção de Controle Administrativo do CG","","Major"),
                _n("ctrl-scg","Subseção de Controle Administrativo do SCG","","Capitão"),
            ]),
        ]),
    ]),
    _n("dir-set","Órgãos de Direção Setorial", cat="Direção Setorial", children=[
        _n("drh","Diretoria de Recursos Humanos","DRH","Coronel QOBM/Comb.", children=[
            _n("drh-1","Seção de Seleção e Ingresso de RH","","Tenente-Coronel"),
            _n("drh-2","Seção de Cadastro, Avaliação, Controle e Movimentação","","Tenente-Coronel"),
            _n("drh-3","Seção de Desenvolvimento de RH","","Major"),
            _n("drh-4","Seção de Promoções","","Capitão"),
            _n("drh-5","Seção de Pagamento de Pessoal","","Major QOAdm"),
            _n("drh-6","Seção de Inativos e Pensionistas","","Major QOAdm"),
            _n("drh-7","Seção de Identificação","","Capitão"),
            _n("drh-8","Seção de Expediente e Arquivo","","1º Tenente QOAdm"),
            _n("drh-9","Seção de Legislação","","1º Tenente QOAdm"),
        ]),
        _n("correg","Corregedoria Geral", children=[
            _n("corr-g","Corregedor Geral","","Coronel"),
            _n("scorr","Subcorregedor Geral","","Tenente-Coronel"),
            _n("ouvidoria","Ouvidoria","","Tenente-Coronel"),
            _n("corr-pol","Seção de Polícia Disciplinar","","1º Tenente"),
            _n("corr-pjm","Seção de Polícia Judiciária Militar","","1º Tenente"),
            _n("corr-adm","Seção de Apoio Administrativo","","Capitão QOAdm"),
            _n("corr-int","Seção de Inteligência","","Major"),
        ]),
        _n("dmp","Diretoria de Material e Patrimônio","DMP","Coronel", children=[
            _n("dmp-1","Seção de Aquisições e Gestão de Contratos","","Tenente-Coronel", children=[
                _n("dmp-1a","Subseção de Gestão de Contratos e Convênios","","Major"),
                _n("dmp-1b","Subseção de Aquisições","","1º Tenente"),
            ]),
            _n("dmp-2","Seção de Apoio a CPL","","Capitão"),
            _n("dmp-3","Seção de Administração da Frota","","Major QOAdm"),
            _n("dmp-4","Seção de Cadastro, Controle e Alienação","","Major QOAdm"),
            _n("dmp-5","Seção de Administração, Expediente e Arquivo","","1º Tenente QOAdm"),
            _n("dmp-6","Seção de Estatística","","1º Tenente QOAdm"),
        ]),
        _n("df-al","Diretoria de Finanças","DF","Tenente-Coronel", children=[
            _n("df-1","Seção de Administração Financeira","","Major", children=[
                _n("df-1a","Subseção de Controle e Execução Orçamentária","","Capitão QOAdm"),
            ]),
            _n("df-2","Seção de Contabilidade e Auditoria","","Major QOAdm"),
            _n("df-3","Seção de Expediente e Arquivo","","2º Tenente QOAdm"),
            _n("df-4","Tesouraria Geral","","1º Tenente QOAdm"),
        ]),
        _n("dplan","Diretoria de Planejamento e Orçamento","DPLAN","Coronel", children=[
            _n("dplan-1","Seção de Informações","","Tenente-Coronel"),
            _n("dplan-2","Seção de Monitoramento da Estrutura Organizacional","","Tenente-Coronel"),
            _n("dplan-3","Seção de Planejamento e Execução Orçamentária","","Major"),
        ]),
        _n("dat-al","Diretoria de Atividades Técnicas","DAT","Coronel", children=[
            _n("dat-1","Seção de Estudos e Análises de Projetos","","Tenente-Coronel"),
            _n("dat-2","Seção de Testes, Vistorias e Pareceres","","Major"),
            _n("dat-3","Seção de Perícias e Pesquisas","","Major"),
            _n("dat-4","Seção de Hidrantes","","1º Tenente QOAdm"),
        ]),
        _n("dpol-al","Diretoria da Policlínica"),
    ]),
    _n("apoio-al","Órgãos de Apoio", cat="Apoio", children=[
        _n("cfae-al","Centro de Formação, Aperfeiçoamento e Especialização"),
        _n("cman-al","Centro de Manutenção"),
        _n("cast-al","Centro de Assistência"),
        _n("cti-al","Centro de Tecnologia, Informática e Informação"),
        _n("alm-al","Almoxarifado Central"),
        _n("apr-al","Aprovisionamento Central"),
    ]),
    _n("exec-al","Órgãos de Execução", cat="Execução", children=[
        _n("cobm-al","Comando Operacional de Bombeiros", children=[
            _n("cobm-cap","Cmd. Op. de Bombeiros — Região Metropolitana de Maceió"),
            _n("cobm-int","Cmd. Op. de Bombeiros do Interior"),
        ]),
        _n("gbm-al","Grupamento de Bombeiros Militar","GBM"),
        _n("gsa-al","Grupamento de Salvamento Aquático","GSA"),
        _n("gse-al","Grupamento de Socorro de Emergência","GSE"),
    ]),
],

# ════════════════════════════════════════════════════════════
# AMAZONAS — Lei nº 2.538/1999 + Lei nº 3.437/2009
# ════════════════════════════════════════════════════════════
"am": [
    _n("cg-am","Comando Geral", cat="Direção Geral",
       ref="Lei nº 2.538/1999", children=[
        _n("cmt-am","Comandante Geral","","Coronel QOBM/Comb."),
        _n("scmt-am","Subcomandante Geral","","Coronel QOBM/Comb."),
        _n("cedec-am","Coordenadoria Estadual de Defesa Civil","CEDEC"),
        _n("cspe","Conselho Superior de Políticas Estratégicas","CSPE"),
        _n("gab-am","Gabinete do Comando-Geral", children=[
            _n("chgab-am","Chefe de Gabinete"),
            _n("aci-am","Assessor de Comunicações e Imprensa","ACI"),
            _n("aj-am","Assessor Jurídico","AJ"),
            _n("ajord-am","Ajudante-de-Ordens"),
        ]),
        _n("ag-am","Ajudância Geral","AG", children=[
            _n("ag0","Secretaria Geral","AG-0"),
            _n("ag1","Seção Administrativa","AG-1"),
            _n("ag2","Seção de Protocolo e Distribuição","AG-2"),
            _n("ag3","Seção de Transporte e Embarque","AG-3"),
            _n("ag4","Seção de Comando e Serviço","AG-4"),
            _n("banda","Banda de Música"),
        ]),
        _n("comissoes-am","Comissões", children=[
            _n("cpo-am","Comissão de Promoção de Oficiais","CPO"),
            _n("cpp-am","Comissão de Promoção de Praças","CPP"),
        ]),
    ]),
    _n("dir-set-am","Órgãos de Direção Setorial", cat="Direção Setorial", children=[
        _n("drh-am","Diretoria de Recursos Humanos","DRH", children=[
            _n("drh-am1","Seção de Controle de Pessoal Ativo, Inativo e Civil","DRH-1"),
            _n("drh-am2","Seção de Recrutamento, Seleção e Serviço Reservado","DRH-2"),
            _n("drh-am3","Seção de Cadastro, Identificação, Avaliação e Promoções","DRH-3"),
            _n("drh-am4","Seção de Desenvolvimento Humano","DRH-4"),
            _n("drh-am5","Seção de Expediente e Mobilização","DRH-5"),
            _n("drh-am6","Seção de Pagadoria de Pessoal","DRH-6"),
        ]),
        _n("df-am","Diretoria de Finanças","DF", children=[
            _n("df-am1","Seção de Administração Financeira","DF-1"),
            _n("df-am2","Seção de Contabilidade","DF-2"),
            _n("df-am3","Seção de Auditoria","DF-3"),
            _n("df-am4","Seção de Expediente","DF-4"),
        ]),
        _n("dl-am","Diretoria de Logística","DL", children=[
            _n("dl-am1","Seção de Suprimento","DL-1"),
            _n("dl-am2","Seção de Manutenção","DL-2"),
            _n("dl-am3","Seção de Patrimônio e Expediente","DL-3"),
        ]),
        _n("deipo","Diretoria de Ensino, Instrução, Pesquisa e Operações","DEIPO", children=[
            _n("deipo1","Seção de Ensino, Instrução e Pesquisa","DEIPO-1"),
            _n("deipo2","Seção de Projetos e Programas Especiais","DEIPO-2"),
            _n("deipo3","Seção de Planejamento, Expediente e Meios Auxiliares","DEIPO-3"),
        ]),
        _n("dst-am","Diretoria de Serviços Técnicos","DST", children=[
            _n("dst1","Seção de Exames de Projetos","DST-1"),
            _n("dst2","Seção de Vistorias e Pareceres","DST-2"),
            _n("dst3","Seção de Hidrante, Expediente e Apoio","DST-3"),
        ]),
        _n("ds-am","Diretoria de Saúde","DS"),
    ]),
    _n("apoio-am","Órgãos de Apoio", cat="Apoio", children=[
        _n("esbom","Escola de Bombeiros Militar","ESBOM", children=[
            _n("de-esbom","Divisão de Ensino","DE"),
            _n("da-esbom","Divisão Administrativa","DA"),
            _n("ca-esbom","Corpo de Alunos","CA"),
        ]),
        _n("cinf-am","Centro de Informática","CInf", children=[
            _n("cinf1","Seção de Suporte","CInf-1"),
            _n("cinf2","Seção de Desenvolvimento e Manutenção de Sistemas","CInf-2"),
            _n("cinf3","Seção de Treinamento","CInf-3"),
        ]),
        _n("cpi-am","Centro de Perícia de Incêndio","CPI", children=[
            _n("cpi1","Seção de Investigação e Coleta","CPI-1"),
            _n("cpi2","Seção de Análises Laboratoriais","CPI-2"),
            _n("cpi3","Seção de Meios e Expedientes","CPI-3"),
        ]),
        _n("casr","Centro de Assistência Social e Religiosa","CASR", children=[
            _n("casr1","Seção de Assistência","CASR-1"),
            _n("casr2","Seção de Orientação e Encaminhamento","CASR-2"),
            _n("casr3","Seção de Assistência Religiosa","CASR-3"),
        ]),
        _n("csm-am","Centro de Suprimento e Manutenção","CSM/MS", children=[
            _n("csm1","Seção de Recebimento e Distribuição","CSM/MS-1"),
            _n("csm2","Seção de Oficinas","CSM/MS-2"),
            _n("csm3","Seção de Expediente, Obras e Serviços Gerais","CSM/MS-3"),
        ]),
    ]),
    _n("exec-am","Órgãos de Execução", cat="Execução", children=[
        _n("cobom","Centro de Operações Bombeiro Militar","COBOM", children=[
            _n("cobom1","Seção de Operações","COBOM-1"),
            _n("cobom2","Seção de Comunicações","COBOM-2"),
            _n("cobom3","Seção de Apoio","COBOM-3"),
        ]),
        _n("cbc","Comando de Bombeiros da Capital","CBC", children=[
            _n("bi","Batalhões de Incêndio","BI"),
            _n("bbe","Batalhão de Bombeiro Especial","BBE"),
            _n("bifma","Batalhão de Incêndio Florestal e Meio Ambiente","BIF/MA"),
        ]),
        _n("cbi","Comando de Bombeiros do Interior","CBI", children=[
            _n("1cibm","1ª Cia. Independente BM — Itacoatiara","1ª CIBM"),
            _n("2cibm","2ª Cia. Independente BM — Manacapuru","2ª CIBM"),
            _n("3cibm","3ª Cia. Independente BM — Parintins","3ª CIBM"),
            _n("1pibm","1º Pelotão Independente BM — Tefé","1º PIBM"),
            _n("2pibm","2º Pelotão Independente BM — Tabatinga","2º PIBM"),
        ]),
    ]),
],

}  # fim CURATED_ORGANS parte 1 — continuação em curated_organs_p2.py
