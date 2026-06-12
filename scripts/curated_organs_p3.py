# curated_organs_p3.py — Estados: BA, CE, AP, MG, RJ, RN, PI, PE, PB, TO, ES, SC, SP

def _n(id_, name, abbr=None, rank=None, desc=None, ref=None, children=None, cat=None):
    node = {"id": id_, "name": name, "children": children or []}
    if abbr:  node["abbreviation"] = abbr
    if rank:  node["rank"] = rank
    if desc:  node["description"] = desc
    if ref:   node["legalRef"] = ref
    if cat:   node["category"] = cat
    return node


CURATED_ORGANS_P3 = {

# ════════════════════════════════════════════════════════════
# RORAIMA — Lei Complementar nº 52/2001 (alt. até LC nº 275/2018)
# ════════════════════════════════════════════════════════════
"rr": [
    _n("cg-rr","Comando Geral","CG","Coronel QOCBM",
       "Órgão máximo executivo do CBMRR, incumbido da administração da instituição.",
       "LC nº 52/2001, Art. 11", cat="Administração Superior", children=[
        _n("cmt-rr","Comandante Geral","","Coronel QOCBM"),
        _n("scmt-rr","Subcomandante Geral / Chefe do EMG","","Coronel QOCBM"),
        _n("gab-rr","Gabinete", children=[
            _n("chgab-rr","Chefia de Gabinete"),
            _n("sec-rr","Secretaria"),
            _n("aci-rr","Assessoria de Comunicação e Imprensa","ACI"),
            _n("cj-rr","Comissão de Justiça","CJ"),
            _n("ajord-rr","Ajudância de Ordens"),
        ]),
        _n("correg-rr","Corregedoria Geral", children=[
            _n("correg-chefia","Chefia da Corregedoria"),
            _n("correg-adm","Seção Administrativa"),
            _n("correg-cart","Cartório"),
            _n("correg-inv","Seção de Investigação"),
            _n("correg-ouv","Ouvidoria"),
        ]),
        _n("cam-rr","Comissão de Avaliação e Mérito","CAM"),
        _n("ag-rr","Ajudância Geral", children=[
            _n("ag-secg","Secretaria Geral"),
            _n("ag-adm","Seção Administrativa"),
            _n("ag-prot","Seção de Protocolo e Distribuição"),
            _n("ag-transp","Seção de Transporte e Embarque"),
            _n("ag-ccs","Companhia de Comando e Serviços"),
            _n("ag-cesau","Centro de Saúde"),
        ]),
        _n("ccult-rr","Centro Cultural", children=[
            _n("cc-adm","Seção Administrativa"),
            _n("cc-museu","Museu do Corpo de Bombeiro Militar"),
            _n("cc-banda","Banda de Música"),
        ]),
        _n("cepdec-rr","Coordenadoria Estadual de Proteção e Defesa Civil","CEPDEC", children=[
            _n("cepdec-prev","Divisão de Prevenção, Mitigação e Preparação"),
            _n("cepdec-resp","Divisão de Resposta ao Desastre"),
            _n("cepdec-rec","Divisão de Recuperação de Cenário de Desastre"),
            _n("cepdec-adm","Divisão Administrativa"),
        ]),
        _n("comissoes-rr","Comissões"),
        _n("dint-rr","Diretoria de Inteligência","DINT", children=[
            _n("dint-sub","Subdiretoria de Inteligência"),
            _n("dint-ci","Subdiretoria de Contra Inteligência e Segurança Institucional"),
            _n("dint-op","Subdiretoria de Operações de Inteligência"),
            _n("dint-arma","Subdiretoria de Registro e Porte de Arma de Fogo"),
            _n("dint-exp","Subdiretoria de Expediente"),
        ]),
        _n("emg-rr","Estado Maior Geral Bombeiro Militar","EMG",
           desc="OBM de Atuação Colegiada, define políticas, diretrizes e ordens em nível estratégico.",
           ref="LC nº 52/2001, Art. 26-27", children=[
            _n("dpl-rr","Diretoria de Pessoal e Legislação","DPL"),
            _n("die-rr","Diretoria de Informática e Estatísticas","DIE"),
            _n("deip-rr","Diretoria de Ensino, Instrução e Pesquisa","DEIP"),
            _n("dlog-rr","Diretoria de Logística","DLOG"),
            _n("dpst-rr","Diretoria de Prevenção e Serviços Técnicos","DPST"),
            _n("dacrp-rr","Diretoria de Assuntos Civis e Relações Públicas","DACRP"),
            _n("dgof-rr","Diretoria de Gestão Orçamentária e Financeira","DGOF"),
            _n("dci-rr","Diretoria de Controle Interno","DCI"),
        ]),
    ]),
    _n("setorial-rr","Órgãos do Nível de Administração Setorial", cat="Administração Setorial",
       desc="Traduzem as políticas e diretrizes do Comando Geral e do EMG em objetivos e metas.",
       ref="LC nº 52/2001, Art. 36", children=[
        _n("cmd-op-rr","Comando Operacional (Capital e Interior)","",
           desc="Subordinado ao Subcomandante Geral.", children=[
            _n("cmd-op-cap","Comando Operacional da Capital", children=[
                _n("emo-cap","Estado Maior Operacional da Capital"),
            ]),
            _n("cmd-op-int","Comando Operacional do Interior", children=[
                _n("emo-int","Estado Maior Operacional do Interior"),
            ]),
        ]),
        _n("ceib-rr","Centro de Ensino e Instrução de Bombeiros","CEIB"),
        _n("csm-rr","Centro de Suprimento e Material","CSM"),
        _n("ceman-rr","Centro de Manutenção","CEMAN"),
        _n("cinfor-rr","Centro de Informática","CINFOR"),
        _n("cipi-rr","Centro de Investigação e Prevenção de Incêndios","CIPI"),
        _n("cesau-rr","Centro de Saúde","CESAU"),
        _n("cest-rr","Centro de Estatísticas","CEST"),
        _n("cecer-rr","Centro de Cerimonial","CECER"),
        _n("cvap-rr","Centro de Vistoria e Análise de Projeto","CVAP"),
    ]),
    _n("execucao-rr","Órgãos do Nível de Execução", cat="Execução",
       desc="Realizam as atividades e tarefas dos sistemas e a execução dos planos operacionais.",
       ref="LC nº 52/2001, Art. 48", children=[
        _n("exec-op-rr","Órgãos de Execução Operacional", children=[
            _n("bbm-rr","Batalhão de Bombeiros"),
            _n("cibm-rr","Companhia Independente de Bombeiros"),
            _n("cia-rr","Companhia de Bombeiros"),
            _n("ccs-rr","Companhia de Comando e Serviço"),
            _n("pel-rr","Pelotão de Bombeiros"),
            _n("dest-rr","Destacamento de Bombeiros"),
        ]),
        _n("exec-prev-rr","Órgãos de Execução Prevencional", children=[
            _n("sub-hid-rr","Subdiretoria de Hidrantes"),
            _n("cipi-exec-rr","Centro de Investigação e Prevenção de Incêndios","CIPI"),
            _n("cvap-exec-rr","Centro de Vistoria e Análise de Projetos","CVAP"),
        ]),
        _n("exec-estr-rr","Órgãos de Execução Estratégica", children=[
            _n("ceib-exec","Centro de Ensino e Instrução de Bombeiros","CEIB"),
            _n("cesau-exec","Centro de Saúde","CESAU"),
            _n("cinfor-exec","Centro de Informática","CINFOR"),
            _n("cecer-exec","Centro de Cerimonial","CECER"),
            _n("cest-exec","Centro de Estatísticas","CEST"),
        ]),
        _n("exec-log-rr","Órgãos de Execução Logística", children=[
            _n("csm-exec","Centro de Suprimento e Material","CSM"),
            _n("ceman-exec","Centro de Manutenção","CEMAN"),
        ]),
    ]),
],

# ════════════════════════════════════════════════════════════
# BAHIA — Lei nº 14.572/2023
# ════════════════════════════════════════════════════════════
"ba": [
    _n("cg-ba","Comando Geral","CG","Coronel",
       ref="Lei nº 14.572/2023", cat="Direção Geral", children=[
        _n("alto-cmd-ba","Alto Comando","","Coronel"),
        _n("conselho-ba","Conselho do Corpo de Bombeiros Militar"),
        _n("scmt-ba","Subcomando-Geral","","Coronel", children=[
            _n("gab-scmt-ba","Gabinete do Subcomando-Geral"),
            _n("cge-ba","Centro de Gestão Estratégica","CGE"),
        ]),
        _n("gab-ba","Gabinete do Comando Geral"),
        _n("correg-ba","Corregedoria do CBM","",desc="Órgão de assessoramento disciplinar."),
        _n("cobm","Comando de Operações de Bombeiros Militar","COBM", children=[
            _n("cvga","Centro de Gestão do Vetor Aéreo"),
        ]),
        _n("csci-ba","Comando de Segurança Contra Incêndio"),
        _n("coord-int-ba","Coordenadoria de Inteligência"),
    ]),
    _n("dir-set-ba","Direção Administrativa e Logística", cat="Direção Setorial", children=[
        _n("deplan","Departamento de Planejamento"),
        _n("dpes-ba","Departamento de Pessoal"),
        _n("dal-ba","Departamento de Apoio Logístico", children=[
            _n("cea","Centro de Engenharia e Arquitetura"),
        ]),
        _n("dmt-ba","Departamento de Modernização e Tecnologia"),
        _n("daf-ba","Departamento de Auditoria e Finanças"),
        _n("cgf-ba","Coordenadoria de Gestão de Frota"),
    ]),
    _n("apoio-ba","Administração Setorial e Ensino", cat="Apoio", children=[
        _n("imesb","Instituto Militar de Ensino Superior de Bombeiros","IMESB"),
        _n("coord-sau-ba","Coordenadoria de Saúde"),
        _n("abm-ba","Academia de Bombeiros Militar"),
        _n("cfap-ba","Coordenadoria de Formação e Aperfeiçoamento de Praças"),
        _n("cto-ba","Coordenadoria de Treinamento Operacional"),
    ]),
    _n("exec-ba","Órgãos de Execução", cat="Execução", children=[
        _n("1crbm-ba","1º Comando Regional de Bombeiros Militar"),
        _n("2crbm-ba","2º Comando Regional de Bombeiros Militar"),
        _n("3crbm-ba","3º Comando Regional de Bombeiros Militar"),
        _n("4crbm-ba","4º Comando Regional de Bombeiros Militar"),
        _n("bbm-ba","Batalhões de Bombeiros Militar","BBM"),
    ]),
],

# ════════════════════════════════════════════════════════════
# CEARÁ — Lei nº 13.438/2004
# ════════════════════════════════════════════════════════════
"ce": [
    _n("cg-ce","Comando Geral","CG","Coronel",
       ref="Lei nº 13.438/2004", cat="Direção Geral", children=[
        _n("cmt-ce","Comandante Geral","","Coronel"),
        _n("cadj-ce","Comandante Adjunto","","Coronel"),
        _n("cc-ce","Conselho Consultivo"),
        _n("sec-exec-ce","Secretaria Executiva"),
        _n("ass-jur-ce","Assessoria Jurídica"),
    ]),
    _n("exec-prog-ce","Órgãos de Execução Programática", cat="Execução", children=[
        _n("cat-ce","Coordenadoria de Atividades Técnicas"),
        _n("cop-ce","Coordenadoria Operacional", children=[
            _n("nbm-metro","Núcleo de Bombeiro Metropolitano", children=[
                _n("1gbm-ce","1º Grupamento de Bombeiro"),
                _n("2gbm-ce","2º Grupamento de Bombeiro"),
                _n("3gbm-ce","3º Grupamento de Bombeiro"),
            ]),
            _n("nbm-int","Núcleo de Bombeiro do Interior", children=[
                _n("4gbm-ce","4º Grupamento de Bombeiro"),
                _n("5gbm-ce","5º Grupamento de Bombeiro"),
            ]),
            _n("ndc-ce","Núcleo de Defesa Civil"),
            _n("nbs-ce","Núcleo de Busca e Salvamento"),
            _n("nre-ce","Núcleo de Resgate e Emergência Pré-hospitalar"),
        ]),
    ]),
    _n("exec-inst-ce","Órgãos de Execução Instrumental", cat="Apoio", children=[
        _n("cg-coord-ce","Coordenadoria Geral", children=[
            _n("log-ce","Célula de Logística", children=[
                _n("nfin-ce","Núcleo Financeiro"),
            ]),
            _n("gfp-ce","Célula de Gestão e Formação de Pessoas", children=[
                _n("abm-ce","Academia de Bombeiro Militar"),
                _n("col-ce","Colégio Militar"),
            ]),
        ]),
    ]),
],

# ════════════════════════════════════════════════════════════
# AMAPÁ — LC nº 180/2026
# ════════════════════════════════════════════════════════════
"ap": [
    _n("cg-ap","Comando-Geral", cat="Direção Geral",
       ref="LC nº 180/2026", children=[
        _n("cmt-ap","Comandante-Geral"),
        _n("scmt-ap","Subcomandante-Geral"),
        _n("dir-ger-ap","Órgãos de Direção-Geral", children=[
            _n("gab-cg-ap","Gabinete do Comandante-Geral"),
            _n("gab-scg-ap","Gabinete do Subcomandante-Geral"),
            _n("cdo-ap","Comitê de Desenvolvimento Organizacional"),
            _n("cmd-op-ap","Comando Operacional"),
            _n("frcbm-ap","Fundo de Reequipamento do CBM"),
        ]),
        _n("dir-set-ap","Órgãos de Direção Setorial", children=[
            _n("dir-int-ap","Diretoria de Inteligência"),
            _n("dir-rh-ap","Diretoria de Recursos Humanos"),
            _n("dir-pd-ap","Diretoria de Pesquisa e Desenvolvimento"),
            _n("dir-of-ap","Diretoria de Gestão Orçamentária e Financeira"),
            _n("dir-amb-ap","Diretoria Ambiental"),
        ]),
    ]),
    _n("assess-ap","Órgãos de Assessoramento", cat="Assessoramento", children=[
        _n("aci-ap","Assessoria de Controle Interno"),
        _n("ass-jur-ap","Assessoria Jurídica"),
        _n("ass-tec-ap","Assessoria Técnica"),
        _n("comissoes-ap","Comissões"),
    ]),
    _n("apoio-ap","Órgãos de Apoio", cat="Apoio", children=[
        _n("abm-ap","Academia Bombeiro Militar"),
        _n("coord-ap","Coordenadorias"),
    ]),
    _n("correg-ap","Corregedoria-Geral", cat="Correição"),
    _n("exec-ap","Órgãos de Execução", cat="Execução", children=[
        _n("gbm-ap","Grupamentos de Bombeiro Militar"),
        _n("gbm-esp-ap","Grupamentos Especializados"),
    ]),
],

# ════════════════════════════════════════════════════════════
# MINAS GERAIS — LC nº 54/1999
# ════════════════════════════════════════════════════════════
"mg": [
    _n("cg-mg","Comando-Geral","CG","Coronel",
       ref="LC nº 54/1999", cat="Direção Geral", children=[
        _n("gab-mg","Gabinete do Comandante-Geral"),
        _n("emg-mg","Estado-Maior do CBM", children=[
            _n("emg-chefe-mg","Chefia do Estado-Maior"),
            _n("emg-sub-mg","Subchefia do Estado-Maior"),
            _n("emg-secoes-mg","Seções do EM (I a VII)"),
        ]),
        _n("audit-mg","Auditoria",desc="Subordinada diretamente ao Comandante-Geral."),
    ]),
    _n("dir-set-mg","Diretorias", cat="Direção Setorial", children=[
        _n("drh-mg","Diretoria de Recursos Humanos"),
        _n("dal-mg","Diretoria de Apoio Logístico"),
        _n("dcf-mg","Diretoria de Contabilidade e Finanças"),
    ]),
    _n("apoio-mg","Órgãos de Apoio", cat="Apoio", children=[
        _n("abm-mg","Academia de Bombeiros Militar","ABM"),
        _n("csm-mg","Centro de Suprimento e Manutenção","CSM"),
        _n("cat-mg","Centro de Atividades Técnicas","CAT"),
        _n("ag-mg","Ajudância-Geral"),
    ]),
    _n("exec-mg","Órgãos de Execução", cat="Execução", children=[
        _n("com-op-mg","Comandos Operacionais de Bombeiros (6 — por RISP)"),
        _n("bbm-mg","Batalhão de Bombeiros Militar","BBM"),
        _n("ciabm-mg","Cia. Independente de Bombeiros Militar","CIA IND BM"),
        _n("ciabm2-mg","Cia. de Bombeiros Militar","CIA BM"),
        _n("pelbm-mg","Pelotão de Bombeiros Militar","PEL BM"),
    ]),
    _n("ceb-mg","Comando Especializado de Bombeiros","CEB",
       ref="Resolução nº 898/2020", cat="Execução Especializada", children=[
        _n("boa-mg","Batalhão de Operações Aéreas","BOA"),
        _n("bemad-mg","Batalhão de Emergências Ambientais e Resposta a Desastres","BEMAD"),
    ]),
],

# ════════════════════════════════════════════════════════════
# RIO DE JANEIRO — Lei nº 250/1979
# ════════════════════════════════════════════════════════════
"rj": [
    _n("cg-rj","Comando-Geral","CmtG","Coronel ou Tenente-Coronel",
       ref="Lei nº 250/1979", cat="Direção Geral", children=[
        _n("emg-rj","Estado-Maior-Geral","EMG", children=[
            _n("emg-chefe-rj","Chefe (acumula função de Subcomandante)"),
            _n("emg-sub-rj","Subchefe"),
            _n("emg-secoes-rj","7 Seções (BM/1 a BM/7)"),
        ]),
        _n("ag-rj","Ajudância-Geral","AjG"),
    ]),
    _n("dir-set-rj","Diretorias de Direção Setorial", cat="Direção Setorial", children=[
        _n("dp-rj","Diretoria de Pessoal","DP"),
        _n("de-rj","Diretoria de Ensino","DE"),
        _n("df-rj","Diretoria de Finanças","DF"),
        _n("dal-rj","Diretoria de Apoio Logístico","DAL"),
        _n("dst-rj","Diretoria de Serviços Técnicos","DST"),
    ]),
    _n("apoio-rj","Órgãos de Apoio", cat="Apoio", children=[
        _n("css-rj","Centro de Serviço Social","CSS"),
        _n("csbm","Curso Superior de Bombeiro-Militar","CSBM"),
        _n("esfao","Escola de Formação e Aperfeiçoamento de Oficiais","EsFAO"),
        _n("cfap-rj","Centro de Formação e Aperfeiçoamento de Praças","CFAP"),
        _n("pagc","Pagadoria Central","PagC"),
        _n("csm-mop","Centro de Suprimento e Manutenção — Mat. Operacional","CSM/MOp"),
        _n("csm-mmoto","Centro de Suprimento e Manutenção — Mat. Motorizado","CSM/MMoto"),
        _n("csm-int","Centro de Suprimento e Manutenção — Intendência","CSM/Int"),
        _n("csm-o","Centro de Suprimento e Manutenção — Obras","CSM/O"),
        _n("csm-mtel","Centro de Suprimento e Manutenção — Telecomunicações","CSM/MTel"),
        _n("hcb","Hospitais do Corpo de Bombeiros","HCB"),
        _n("polcb","Policlínicas do Corpo de Bombeiros","PolCB"),
    ]),
    _n("exec-rj","Órgãos de Execução", cat="Execução", children=[
        _n("cba","Comando de Bombeiros de Área","CBA"),
        _n("cocb-rj","Centro de Operações do CBM","COCB"),
        _n("gi","Grupamento de Incêndio","GI"),
        _n("gbs-rj","Grupamento de Busca e Salvamento","GBS"),
        _n("gmar","Grupamento Marítimo","Gmar"),
    ]),
],

# ════════════════════════════════════════════════════════════
# RIO GRANDE DO NORTE — Decreto nº 31.139/2021 (Regulamento Geral)
# ════════════════════════════════════════════════════════════
"rn": [
    _n("cmt-rn","Comandante-Geral","CG","Coronel BM (QOCBM)",
       desc="Responsável pelo comando, coordenação, supervisão e orientação da Corporação (Decreto 31.139/2021, Art. 12).",
       ref="Decreto 31.139/2021, Art. 13", cat="Direção Superior", children=[
        _n("scmt-rn","Subcomandante-Geral","SCG","Coronel BM (QOCBM)",
           desc="Auxiliar direto do Comandante Geral, substituto nos impedimentos eventuais (Art. 15).",
           ref="Decreto 31.139/2021, Art. 15"),
        _n("csup-rn","Conselho Superior","CS",
           desc="Órgão de deliberação coletiva que assessora o Comandante Geral (Art. 17, I-IX).",
           ref="Decreto 31.139/2021, Art. 17", cat="Deliberação Coletiva"),
    ]),
    _n("assess-rn","Órgãos de Assessoramento","Assess",
       desc="Prestam serviços afetos às áreas de consultoria e de assessoramento técnico (Art. 10).",
       ref="Decreto 31.139/2021, Art. 10", cat="Assessoramento", children=[
        _n("gab-rn","Gabinete do Comando Geral","Gab.CG",
           desc="Órgão de apoio administrativo e de representação social do Comando Geral (Art. 19).",
           ref="Decreto 31.139/2021, Art. 19"),
        _n("aj-rn","Assessoria Jurídica","AJ",
           desc="Presta assessoramento jurídico direto ao Comandante Geral (Art. 20).",
           ref="Decreto 31.139/2021, Art. 20"),
        _n("aa-rn","Assessoria Administrativa","AA",
           desc="Órgão de assessoramento administrativo, diretamente subordinado ao Comandante Geral (Art. 21).",
           ref="Decreto 31.139/2021, Art. 21"),
        _n("ajg-rn","Ajudância Geral","AjG",
           desc="Encarregada do expediente, secretaria geral, protocolo e segurança do Quartel-General (Art. 22).",
           ref="Decreto 31.139/2021, Art. 22"),
        _n("cped-rn","Comissão Permanente de Ética e Disciplina","CPED",
           desc="Presidida pelo Subcomandante Geral; analisa o nível disciplinar da tropa (Art. 23).",
           ref="Decreto 31.139/2021, Art. 23"),
        _n("uci-rn","Unidade de Controle Interno","UCI",
           desc="Analisa processos de aquisição, contratos e despesas de pessoal no âmbito do CBMRN (Art. 24).",
           ref="Decreto 31.139/2021, Art. 24"),
        _n("cpo-rn","Comissão de Promoção de Oficiais","CPO",
           desc="Órgão de processamento das promoções dos Oficiais do CBMRN (Art. 25).",
           ref="Decreto 31.139/2021, Art. 25"),
        _n("cpp-rn","Comissão de Promoção de Praças","CPP",
           desc="Órgão consultivo e deliberativo para as promoções das Praças do CBMRN (Art. 26).",
           ref="Decreto 31.139/2021, Art. 26"),
        _n("appc-rn","Assessoria de Projetos, Processos e Convênios","APPC",
           desc="Gestão, elaboração e acompanhamento de convênios e projetos com órgãos públicos e privados (Art. 27).",
           ref="Decreto 31.139/2021, Art. 27"),
        _n("cpe-rn","Comissão de Planejamento Estratégico","CPE",
           desc="Assessoramento do Comandante Geral para implantação e controle do plano estratégico (Art. 28).",
           ref="Decreto 31.139/2021, Art. 28"),
        _n("aspar-rn","Assessoria Parlamentar","ASPAR",
           desc="Acompanha assuntos de interesse institucional junto ao Poder Legislativo Federal e Estadual (Art. 29).",
           ref="Decreto 31.139/2021, Art. 29"),
        _n("assint-rn","Assessoria de Inteligência","ASSINT",
           desc="Produce informações estratégicas e assessora o Comandante Geral em controle interno (Art. 30).",
           ref="Decreto 31.139/2021, Art. 30"),
        _n("assecom-rn","Assessoria de Comunicação Social","ASSECOM",
           desc="Assessora o Comandante Geral na divulgação da imagem e ações da Corporação (Art. 31).",
           ref="Decreto 31.139/2021, Art. 31"),
    ]),
    _n("cmdoop-rn","Comando Operacional Bombeiro Militar","CmdoOpBM","Coronel/TC BM",
       desc="Responsável pelo planejamento, coordenação, fiscalização e execução das atividades operacionais (Art. 32).",
       ref="Decreto 31.139/2021, Art. 32", cat="Execução", children=[
        _n("emop-rn","Estado-Maior Operacional","EM Op",
           desc="Estrutura de assessoramento e supervisão das atividades operacionais em todo o Estado (Art. 33).",
           ref="Decreto 31.139/2021, Art. 33"),
        _n("cocbm-rn","Centro de Operações do CBMRN","COCBM",
           desc="Coordena atendimento e despachos de ocorrências e as telecomunicações operacionais (Art. 33 §7).",
           ref="Decreto 31.139/2021, Art. 33 §7"),
        _n("codec-rn","Comissão de Defesa Civil","CODEC",
           desc="Coordenação de ações preventivas e de socorro emergencial de defesa civil (Art. 33 §8).",
           ref="Decreto 31.139/2021, Art. 33 §8"),
        _n("gbm1-rn","1º Grupamento de Bombeiros Militar","1º GBM","Major/TC BM",
           desc="Unidade operacional responsável por incêndio, busca e resgate na capital e região metropolitana (Art. 32 §9).",
           ref="Decreto 31.139/2021, Art. 32 §9"),
        _n("gbm2-rn","2º Grupamento de Bombeiros Militar","2º GBM","Major/TC BM",
           desc="Unidade operacional responsável por incêndio, busca, resgate e APH nos municípios do interior (Art. 32 §10).",
           ref="Decreto 31.139/2021, Art. 32 §10"),
        _n("gbmar-rn","Grupamento de Bombeiros Marítimo","GBMAR",
           desc="Unidade operacional responsável pelo salvamento aquático e fiscalização de atividades aquáticas (Art. 32 §11).",
           ref="Decreto 31.139/2021, Art. 32 §11"),
        _n("sibm-aph-rn","Subgrupamento Independente de APH","SIBM-APH",
           desc="Unidade responsável pelo atendimento pré-hospitalar de urgência na capital (Art. 32 §12).",
           ref="Decreto 31.139/2021, Art. 32 §12"),
        _n("sibm1-rn","1º Subgrupamento Independente de Bombeiros Militar","1º SIBM",
           desc="Unidade operacional no interior do Estado — incêndio, resgate e APH (Art. 32 §13).",
           ref="Decreto 31.139/2021, Art. 32 §13"),
        _n("sibm2-rn","2º Subgrupamento Independente de Bombeiros Militar","2º SIBM",
           desc="Unidade operacional no interior do Estado — incêndio, resgate e APH (Art. 32 §14).",
           ref="Decreto 31.139/2021, Art. 32 §14"),
    ]),
    _n("dlof-rn","Diretoria de Logística, Orçamento e Finanças","DLOF","Coronel/TC BM (QOCBM)",
       desc="Responsável pela gestão das finanças e logística da corporação (Art. 34).",
       ref="Decreto 31.139/2021, Art. 34", cat="Execução", children=[
        _n("sec-exec-dlof-rn","Secretaria Executiva (DLOF)","Sec.Exec.",
           ref="Decreto 31.139/2021, Art. 35"),
        _n("cpl-rn","Comissão Permanente de Licitação","CPL",
           ref="Decreto 31.139/2021, Art. 36"),
        _n("clog-rn","Centro de Logística","CLOG",
           ref="Decreto 31.139/2021, Art. 37"),
        _n("ctic-rn","Centro de Tecnologia da Informação e Comunicações","CTIC",
           ref="Decreto 31.139/2021, Art. 38"),
        _n("cafo-rn","Centro de Administração Financeira e Orçamentária","CAFO",
           ref="Decreto 31.139/2021, Art. 39"),
    ]),
    _n("dgpei-rn","Diretoria de Gestão de Pessoas, Ensino e Instrução","DGPEI","Coronel/TC BM (QOCBM)",
       desc="Responsável pelo gerenciamento de pessoas, ensino e instrução da Corporação (Art. 40).",
       ref="Decreto 31.139/2021, Art. 40", cat="Execução", children=[
        _n("crh-rn","Centro de Recursos Humanos","CRH",
           ref="Decreto 31.139/2021, Art. 41"),
        _n("csfa-rn","Centro Superior de Formação e Aperfeiçoamento","CSFA",
           ref="Decreto 31.139/2021, Art. 42"),
        _n("sv-saude-rn","Serviço de Saúde","SvSaúde",
           ref="Decreto 31.139/2021, Art. 43"),
    ]),
    _n("dat-rn","Diretoria de Atividades Técnicas","DAT","Coronel/TC BM (QOCBM)",
       desc="Desenvolve atividades de prevenção contra incêndio e controle de pânico (Art. 44).",
       ref="Decreto 31.139/2021, Art. 44", cat="Execução", children=[
        _n("carip-rn","Centro de Análise de Risco de Incêndio e Pânico","CARIP",
           ref="Decreto 31.139/2021, Art. 44 §3"),
        _n("cata-rn","Centro de Apoio Técnico Administrativo","CATA",
           ref="Decreto 31.139/2021, Art. 44 §4"),
        _n("cv-rn","Centro de Vistorias","CV",
           ref="Decreto 31.139/2021, Art. 44 §6"),
        _n("cf-rn","Centro de Fiscalização","CF",
           ref="Decreto 31.139/2021, Art. 44 §7"),
        _n("cat1-rn","1º Centro de Atividades Técnicas — Mossoró","1º CAT",
           ref="Decreto 31.139/2021, Art. 44 §8"),
        _n("cat2-rn","2º Centro de Atividades Técnicas — Caicó","2º CAT",
           ref="Decreto 31.139/2021, Art. 44 §9"),
    ]),
],

# ════════════════════════════════════════════════════════════
# PIAUÍ — Lei nº 7.772/2022 (altera Lei nº 5.949/2009)
# ════════════════════════════════════════════════════════════
"pi": [
    _n("cg-pi","Comando Geral","CG","Coronel",
       ref="Lei nº 5.949/2009 alt. 7.772/2022", cat="Direção Geral", children=[
        _n("scg-pi","Subcomandante-Geral","SCG"),
        _n("alto-comando-pi","Alto Comando","AC"),
        _n("emg-pi","Estado-Maior-Geral","EMG"),
        _n("gcg-pi","Gabinete do Comandante-Geral","GAB.CBMT"),
        _n("gab-scg-pi","Gabinete do Subcomandante-Geral","GAB.SUBCMT"),
        _n("nee-pi","Núcleo de Estudos Estratégicos","NEE"),
        _n("ndc-pi","Núcleo de Defesa Civil","NDC"),
        _n("ajg-pi","Ajudância Geral","AJG"),
        _n("nci-pi","Núcleo de Controle Interno","NCI"),
        _n("comissoes-pi","Comissões e Assessorias"),
    ]),
    _n("dir-set-pi","Diretorias Setoriais", cat="Direção Setorial", children=[
        _n("dgp-pi","Diretoria de Gestão de Pessoas","DGP"),
        _n("dsci-pi","Diretoria de Segurança Contra Incêndio","DSCI"),
        _n("deip-pi","Diretoria de Ensino, Instrução e Pesquisa","DEIP"),
        _n("daf-pi","Diretoria Administrativa e Financeira","DAF"),
    ]),
    _n("apoio-pi","Órgãos de Apoio", cat="Apoio", children=[
        _n("ceman-pi","Centro de Manutenção","CEMAN"),
        _n("csm-pi","Centro de Suprimento de Material","CSM"),
        _n("cto-pi","Centro de Treinamento Operacional","CTO"),
        _n("cafd-pi","Centro de Atividades Físicas e Desportos","CAFD"),
        _n("ceib-pi","Centro de Ensino e Instrução de Bombeiros","CEIB"),
        _n("coc-pi","Centro de Operações e Comunicações","COC"),
        _n("ns-pi","Núcleo de Saúde","NS"),
    ]),
    _n("exec-pi","Órgãos de Execução", cat="Execução", children=[
        _n("cob-pi","Comando Operacional de Bombeiros","COB", children=[
            _n("nipi-pi","Núcleo de Investigação e Prevenção de Incêndios","NIPI"),
            _n("crbm-i-pi","CRBM-I — Meio-Norte","CRBM-I"),
            _n("crbm-ii-pi","CRBM-II — Litoral","CRBM-II"),
            _n("crbm-iii-pi","CRBM-III — Semiárido","CRBM-III"),
            _n("crbm-iv-pi","CRBM-IV — Cerrados","CRBM-IV"),
            _n("gbm-pi","Grupamento de Bombeiros Militar","GBM"),
            _n("gbmar-pi","Grupamento de Bombeiros Militar Marítimo","GBMar"),
            _n("sgbm-pi","Subgrupamento de Bombeiros Militar","SGBM"),
        ]),
    ]),
],

# ════════════════════════════════════════════════════════════
# PERNAMBUCO — Lei nº 15.187/2013
# ════════════════════════════════════════════════════════════
"pe": [
    _n("cg-pe","Comando Geral","CG","Coronel",
       ref="Lei nº 15.187/2013", cat="Direção Geral", children=[
        _n("cmt-pe","Comandante Geral","CG"),
        _n("scmt-pe","Subcomandante Geral","SCG"),
        _n("cpe-pe","Conselho de Políticas e Estratégias","CPE"),
        _n("gcg-pe","Gabinete do Comandante Geral","GCG"),
        _n("aj-pe","Assessoria Jurídica","AJ"),
        _n("ccs-pe","Centro de Comunicação Social","CCS"),
        _n("ctic-pe","Centro de Tecnologia da Informação e Comunicação","CTIC"),
        _n("cpo-pe","Comissão de Promoção de Oficiais","CPO"),
        _n("ci-pe","Centro de Inteligência","CI"),
        _n("gsg-pe","Gabinete do Subcomandante Geral","GSG"),
        _n("ajg-pe","Ajudância Geral","AJG"),
        _n("cjd-pe","Centro de Justiça e Disciplina","CJD"),
        _n("cpp-pe","Comissão de Promoção de Praças","CPP"),
        _n("cci-pe","Centro de Controladoria Institucional","CCI"),
    ]),
    _n("dir-set-pe","Diretorias Setoriais", cat="Direção Setorial", children=[
        _n("dgp-pe","Diretoria de Gestão de Pessoal","DGP", children=[
            _n("cemet2-pe","Campus de Ensino Metropolitano II","CEMET II"),
            _n("cppa-pe","Centro de Pagamento de Pessoal Ativo","CPPA"),
            _n("cefd-pe","Centro de Educação Física e Desportos","CEFD"),
            _n("cas-pe","Centro de Assistência Social","CAS"),
        ]),
        _n("dlog-pe","Diretoria de Logística","DLog", children=[
            _n("cman-pe","Centro de Manutenção","CMan"),
            _n("cint-pe","Centro de Intendência","CInt"),
            _n("ceao-pe","Centro de Engenharia, Arquitetura e Obras","CEAO"),
        ]),
        _n("df-pe","Diretoria de Finanças","DF"),
        _n("dplag-pe","Diretoria de Planejamento e Gestão","DPlaG"),
        _n("dim-pe","Diretoria Integrada Metropolitana","DIM", children=[
            _n("com-pe","Comando Operacional Metropolitano","COM", children=[
                _n("gbi-pe","Grupamento de Bombeiros de Incêndio","GBI"),
                _n("gbaph-pe","Grupamento de Atendimento Pré-Hospitalar","GBAPH"),
                _n("gbmar-pe","Grupamento de Bombeiros Marítimo","GBMar"),
                _n("gbs-pe","Grupamento de Bombeiros de Salvamento","GBS"),
            ]),
            _n("cco-pe","Centro de Controle Operacional","CCO"),
            _n("crd-pe","Centro de Resposta a Desastres","CRD"),
        ]),
        _n("diesp-pe","Diretoria Integrada Especializada","DIEsp", children=[
            _n("coesp-pe","Comando Operacional Especializado","COEsp", children=[
                _n("cat-rmr","CAT/RMR","CAT/RMR"),
                _n("cat-zm","CAT/Zona da Mata","CAT/ZM"),
                _n("cat-agreste","CAT/Agreste","CAT/Agr"),
                _n("cat-sertao1","CAT/Sertão I","CAT/S1"),
                _n("cat-sertao2","CAT/Sertão II","CAT/S2"),
            ]),
        ]),
        _n("dinter1-pe","Diretoria Integrada do Interior/1","DInter/1", children=[
            _n("cointer1-pe","Comando Operacional do Interior/1","COInter/1", children=[
                _n("1gb-pe","1º Grupamento de Bombeiros","1ºGB"),
                _n("2gb-pe","2º Grupamento de Bombeiros","2ºGB"),
                _n("6gb-pe","6º Grupamento de Bombeiros","6ºGB"),
                _n("7gb-pe","7º Grupamento de Bombeiros","7ºGB"),
            ]),
        ]),
        _n("dinter2-pe","Diretoria Integrada do Interior/2","DInter/2", children=[
            _n("cointer2-pe","Comando Operacional do Interior/2","COInter/2", children=[
                _n("3gb-pe","3º Grupamento de Bombeiros","3ºGB"),
                _n("4gb-pe","4º Grupamento de Bombeiros","4ºGB"),
                _n("5gb-pe","5º Grupamento de Bombeiros","5ºGB"),
            ]),
        ]),
    ]),
],

# ════════════════════════════════════════════════════════════
# PARAÍBA — LC nº 191/2024
# ════════════════════════════════════════════════════════════
"pb": [
    _n("cg-pb","Comando Geral","CG","Coronel",
       ref="LC nº 191/2024", cat="Direção Geral", children=[
        _n("gcg-pb","Gabinete do Comando Geral","GCG", children=[
            _n("gcmtg","Gabinete do Comandante Geral","GCMTG"),
            _n("gscmdg","Gabinete do Subcomandante Geral","GSCMDG"),
            _n("scg-pb","Secretaria do Comando Geral","SCG", children=[
                _n("ajord-pb","Ajudância de Ordem","AjO"),
            ]),
            _n("ouv-pb","Ouvidoria do CBM","OUV"),
            _n("ari-pb","Assessoria de Relações Institucionais","ARI"),
            _n("ccg-pb","Centro de Contratações Gerais","CCG", children=[
                _n("ccbs","Subcentro de Contratações de Bens e Serviços","CCBS"),
                _n("ccose","Subcentro de Contratações de Obras e Serviços de Engenharia","CCOSE"),
            ]),
            _n("comissoes-pb","Comissões", children=[
                _n("cpo-pb","Comissão de Promoção de Oficiais","CPO"),
                _n("cpp-pb","Comissão de Promoção de Praças","CPP"),
                _n("cam-pb","Comissão de Avaliação de Mérito","CAM"),
                _n("cpad","Comissão Permanente de Avaliação de Documentos","CPAD"),
                _n("cpsb","Comissão Permanente de Segurança Cibernética","CPSB"),
            ]),
            _n("qcg-pb","Quartel do Comando Geral","QCG", children=[
                _n("ccsvqcg","Companhia de Comando e Serviço","CCSv/QCG"),
                _n("gbmr","Guarda de BM da Reserva","GBMR"),
            ]),
        ]),
        _n("ac-pb","Alto Comando","AC",desc="Conselho de Assuntos Estratégicos."),
        _n("emg-pb","Estado Maior Geral","EMG", children=[
            _n("emg1-pb","1ª Coord. — Assessoria de Estudos Legislativos","1ª EMG"),
            _n("emg2-pb","2ª Coord. — Assessoria de Inteligência","2ª EMG"),
            _n("emg3-pb","3ª Coord. — Operações, Doutrina e Estatística","3ª EMG"),
            _n("emg4-pb","4ª Coord. — Mobilização, Riscos e Resposta a Desastres","4ª EMG"),
            _n("emg5-pb","5ª Coord. — Comunicação Social e Marketing","5ª EMG"),
            _n("emg6-pb","6ª Coord. — Planejamento Logístico e Gestão de Projetos","6ª EMG"),
            _n("emg7-pb","7ª Coord. — Gestão Estratégica e Qualidade","7ª EMG"),
            _n("emg8-pb","8ª Coord. — Integração Comunitária e Projetos Sociais","8ª EMG"),
        ]),
        _n("ci-pb","Controladoria Interna","CI", children=[
            _n("ci1-pb","Seção de Auditoria e Fiscalização","CI/1"),
            _n("ci2-pb","Seção de Gestão de Contratos","CI/2"),
            _n("ci3-pb","Seção de Controle de Gastos","CI/3"),
            _n("ci4-pb","Seção de Controle Patrimonial","CI/4"),
        ]),
        _n("correg-pb","Corregedoria","CORREG"),
        _n("crbm-pb","Comandos Regionais BM","CRBM", children=[
            _n("emr-pb","Estado Maior Regional","EM/R", children=[
                _n("b1-pb","Seção de Gestão de Pessoas e Secretaria","B/1"),
                _n("b2-pb","Seção de Inteligência","B/2"),
                _n("b3-pb","Seção de Articulação Operacional","B/3"),
                _n("b4-pb","Seção de Articulação Logística e Mobilização","B/4"),
                _n("b5-pb","Seção de Comunicação Social e Marketing","B/5"),
                _n("b6-pb","Seção de Compras e Finanças","B/6"),
            ]),
            _n("cri","Centro Regional de Intendência","CRI"),
        ]),
    ]),
    _n("dir-set-pb","Diretorias de Direção Setorial", cat="Direção Setorial", children=[
        _n("dal-pb","Diretoria de Apoio Logístico","DAL", children=[
            _n("csl","Centro de Suprimento Logístico","CSL"),
            _n("caeo","Centro de Arquitetura, Engenharia e Obras","CAEO"),
            _n("cmav","Centro de Controle e Manutenção de Viaturas","CMAV"),
        ]),
        _n("dat-pb","Diretoria de Atividades Técnicas","DAT", children=[
            _n("ctn-pb","Conselho Técnico Normativo","CTN"),
            _n("ctd-pb","Conselho Técnico Deliberativo","CTD"),
        ]),
        _n("dep-pb","Diretoria de Educação e Pesquisa","DEP", children=[
            _n("abmap","Academia de Bombeiro Militar","ABMAP", children=[
                _n("cfao-pb","Centro de Formação, Habilitação e Aperfeiçoamento de Oficiais","CFAO"),
                _n("cfap-pb","Centro de Formação, Habilitação e Aperfeiçoamento de Praças","CFAP"),
                _n("cpex-pb","Centro de Pesquisa e Extensão","CPEx"),
                _n("ctop-pb","Centro de Treinamento Operacional","CTOP"),
            ]),
            _n("col-mil-pb","Colégios Militares"),
            _n("corpo-mus-pb","Corpo Musical"),
        ]),
        _n("df-pb","Diretoria de Finanças","DF", children=[
            _n("df1-pb","Seção de Administração Financeira","DF/1"),
            _n("df2-pb","Seção de Orçamento","DF/2"),
            _n("df3-pb","Seção de Contabilidade","DF/3"),
            _n("df4-pb","Seção de Auditoria e Controle","DF/4"),
            _n("df5-pb","Seção de Captação de Recursos","DF/5"),
        ]),
        _n("dgp-pb","Diretoria de Gestão de Pessoas","DGP", children=[
            _n("cresep","Centro de Recrutamento e Seleção de Pessoal","CRESEP"),
            _n("dgp1-pb","Seção de Análise de Legislação","DGP/1"),
            _n("dgp2-pb","Seção de Cadastro, Avaliação e Identificação","DGP/2"),
            _n("dgp3-pb","Seção de Acompanhamento, Movimentação e Promoções","DGP/3"),
            _n("dgp4-pb","Seção de Justiça e Disciplina","DGP/4"),
            _n("dgp5-pb","Seção de Inativos e Pensionistas","DGP/5"),
            _n("dgp8-pb","Seção de Folha de Pagamento e Implantação","DGP/8"),
        ]),
        _n("ds-pb","Diretoria de Saúde","DS", children=[
            _n("cpmsm","Centro de Perícia Médica de Saúde Militar","CPMSM"),
            _n("csbio","Centro de Saúde Biopsicossocial","CSBIO"),
            _n("ccfm-pb","Centro de Capacitação Física Militar","CCFM"),
            _n("psbio","Policlínicas de Saúde Biopsicossociais","PSBIO"),
            _n("cvet","Clínica Veterinária","CVET"),
        ]),
        _n("dti-pb","Diretoria de Tecnologia da Informação","DTI", children=[
            _n("dti1-pb","Seção de Administração e Gerência de Redes","DTI/1"),
            _n("dti2-pb","Seção de Bancos e Armazenamento de Dados","DTI/2"),
            _n("dti6-pb","Seção de Desenvolvimento de Sistemas Corporativos","DTI/6"),
            _n("dti7-pb","Seção de Suporte","DTI/7"),
        ]),
    ]),
    _n("exec-pb","Órgãos de Execução", cat="Execução", children=[
        _n("cat-pb","Centros de Atividades Técnicas","CAT"),
        _n("bbm-pb","Batalhões de Bombeiro Militar","BBM", children=[
            _n("emu-pb","Estado Maior de Unidade","EM/U"),
            _n("cia-bbm-pb","Companhias de BM","Cia BM"),
        ]),
        _n("cibm-pb","Companhias Independentes de BM","CIBM"),
        _n("geor","Grupamento Especializado em Operações de Risco","GEOR", children=[
            _n("geor-inc","Núcleo de Doutrina e Operações de Incêndio"),
            _n("geor-domar","Núcleo DOMAR — Mergulho Autônomo de Resgate"),
            _n("geor-brs","Núcleo Busca, Resgate e Salvamento","DOBRS"),
            _n("geor-cani","Núcleo de Busca, Resgate e Salvamento com Cães","DOC"),
        ]),
        _n("goa-pb","Grupamento de Operações Aéreas","GOA", children=[
            _n("goa1-pb","Seção de Gestão de Pessoas","GOA/1"),
            _n("goa2-pb","Seção de Segurança de Voo","GOA/2"),
            _n("goa3-pb","Seção de Operações","GOA/3"),
            _n("goa7-pb","Seção de Manutenção e Controle Técnico","GOA/7"),
        ]),
    ]),
],

# ════════════════════════════════════════════════════════════
# TOCANTINS — LC nº 131/2021
# ════════════════════════════════════════════════════════════
"to": [
    _n("cg-to","Comando-Geral","CG","Coronel",
       ref="LC nº 131/2021", cat="Direção Geral", children=[
        _n("cmt-to","Comandante-Geral"),
        _n("chem","Chefe do Estado Maior / Subcomandante-Geral","CHEM"),
        _n("subchem","Subchefe do Estado Maior","SUBCHEM"),
        _n("em-to","Estado Maior", children=[
            _n("ccd-to","Comando de Correição e Disciplina"),
            _n("cadc-to","Comando de Ações de Defesa Civil"),
            _n("cgp-to","Comando de Gestão de Pessoas"),
            _n("cgrf-to","Comando de Gestão de Recursos Financeiros e Patrimoniais"),
            _n("cat-to","Comando de Atividades Técnicas"),
            _n("cobm-to","Comando Operacional Bombeiro Militar"),
        ]),
        _n("gab-to","Gabinete do CG"),
        _n("comissoes-to","Comissões", children=[
            _n("cpo-to","CPO — Comissão de Promoção de Oficiais"),
            _n("cpp-to","CPP — Comissão de Promoção de Praças"),
            _n("cpm-to","CPM — Comissão de Promoção de Méritos"),
        ]),
    ]),
    _n("assess-to","Órgãos de Assessoramento", cat="Assessoramento", children=[
        _n("ai-to","Assessoria de Inteligência"),
        _n("aj-to","Assessoria Jurídica"),
        _n("acs-to","Assessoria de Comunicação Social"),
        _n("age-to","Assessoria de Gestão Estratégica"),
        _n("ati-to","Assessoria de Telecomunicações e Informática"),
        _n("ap-to","Assessoria Parlamentar"),
    ]),
    _n("dir-set-to","Diretorias", cat="Direção Setorial", children=[
        _n("dagp-to","Diretoria de Administração e Gestão de Pessoas"),
        _n("dep-to","Diretoria de Ensino e Pesquisa"),
        _n("dlp-to","Diretoria de Logística e Patrimônio"),
        _n("dof-to","Diretoria de Orçamento e Finanças"),
        _n("dsas-to","Diretoria de Saúde e Assistência Social"),
        _n("dst-to","Diretoria de Serviços Técnicos"),
    ]),
    _n("apoio-to","Órgãos de Apoio", cat="Apoio", children=[
        _n("ag-to","Ajudância Geral"),
        _n("acad-to","Academia de Formação de Bombeiros"),
        _n("col-to","Colégios Militares do CBM-TO"),
    ]),
    _n("exec-to","Órgãos de Execução", cat="Execução", children=[
        _n("ubm-to","Unidades Bombeiro Militares","UBM"),
        _n("bat-to","Batalhões"),
        _n("ci-to","Companhias Independentes"),
        _n("cia-to","Companhias Destacadas"),
        _n("pel-to","Pelotões"),
        _n("grp-to","Grupos"),
    ]),
],

# ════════════════════════════════════════════════════════════
# ESPÍRITO SANTO — NGA (Normas Gerais de Ação) 2022
# ════════════════════════════════════════════════════════════
"es": [
    _n("cg-es","Comando-Geral","CG",
       desc="Administração superior do CBMES.",
       ref="NGA — Normas Gerais de Ação 2022", cat="Direção Geral", children=[
        _n("gab-es","Gabinete do Comando-Geral","GCG", children=[
            _n("acmdo","Assistência ao Comando","ACMDO", children=[
                _n("aesp-es","Assessoria Especial","AEsp"),
            ]),
            _n("ascom","Assessoria de Comunicação","ASCOM", children=[
                _n("ascom-sec","Setor de Secretaria"),
                _n("ascom-cav","Setor de Comunicação e Arte Visual"),
                _n("ascom-pav","Setor de Produção Áudio Visual"),
                _n("ascom-pm","Setor de Publicação e Marketing Social"),
            ]),
            _n("aest","Assessoria Estratégica","AEST", children=[
                _n("deppi","Departamento de Projetos Institucionais","DepPI"),
                _n("depgc","Departamento de Gestão do Conhecimento","DepGC"),
                _n("gic","Gerência de Inteligência Corporativa","GIC"),
            ]),
            _n("ai-es","Assessoria de Inteligência","AI"),
            _n("ueci","Unidade Executora de Controle Interno","UECI"),
            _n("ag-es","Ajudância-Geral","Aj-Geral"),
        ]),
        _n("coorddc-es","Coordenadoria Estadual de Proteção e Defesa Civil"),
        _n("correg-es","Corregedoria"),
        _n("cat-es","Centro de Atividades Técnicas"),
    ]),
    _n("dir-set-es","Órgãos de Direção Setorial", cat="Direção Setorial", children=[
        _n("dgp-es","Diretoria de Gestão de Pessoas","DGP", children=[
            _n("crh","Centro de Recursos Humanos","CRH", children=[
                _n("grh","Gerência de Recursos Humanos","GRH"),
            ]),
            _n("sef-es","Seção de Educação Física","SEF"),
            _n("css-es","Centro de Serviço Social","CSS"),
            _n("ceib","Centro de Ensino e Instrução de Bombeiros","CEIB"),
        ]),
        _n("dop-es","Diretoria de Operações","DOP", children=[
            _n("div-op-es","Divisão de Operações"),
            _n("div-dout","Divisão de Doutrinas"),
        ]),
        _n("dal-es","Diretoria de Apoio Logístico","DAL", children=[
            _n("depof","Departamento de Orçamento e Finanças","DepOF"),
            _n("csp-es","Centro de Suprimento e Processamento","CSP"),
            _n("depmtr","Departamento de Manutenção, Transporte e Radiocomunicação","DepMTR", children=[
                _n("gti-es","Gerência de Tecnologia da Informação","GTI"),
            ]),
        ]),
    ]),
    _n("exec-es","Órgãos de Execução", cat="Execução", children=[
        _n("1bbm-es","1º Batalhão de Bombeiros Militar","1º BBM"),
        _n("2bbm-es","2º Batalhão de Bombeiros Militar","2º BBM"),
        _n("3bbm-es","3º Batalhão de Bombeiros Militar","3º BBM"),
        _n("4bbm-es","4º Batalhão de Bombeiros Militar","4º BBM"),
        _n("5bbm-es","5º Batalhão de Bombeiros Militar","5º BBM"),
        _n("6bbm-es","6º Batalhão de Bombeiros Militar","6º BBM"),
        _n("cias-ind-es","Companhias Independentes (1ª a 5ª CIA IND)"),
        _n("cerd","Centro Especializado de Resposta a Desastres","CERD"),
    ]),
],

# ════════════════════════════════════════════════════════════
# SANTA CATARINA — LC nº 724/2018 + Dec. nº 1.328/2021
# ════════════════════════════════════════════════════════════
"sc": [
    _n("cg-sc","Comando-Geral","CG","Coronel",
       ref="LC nº 724/2018; Dec. nº 1.328/2021", cat="Direção Geral", children=[
        _n("scmt-sc","Subcomando-Geral", children=[
            _n("cmop-sc","Centro de Monitoramento Operacional e Gestão de Crises"),
        ]),
        _n("emg-sc","Estado-Maior Geral", children=[
            _n("emg-sec-sc","Seção de Pessoal, Legislação e Cultura"),
            _n("emg-op-sc","Seção de Operações, Doutrina, Estatística, Ensino e Instrução"),
            _n("emg-log-sc","Seção de Logística e Patrimônio"),
            _n("emg-orc-sc","Seção de Planejamento Orçamentário"),
            _n("emg-proj-sc","Seção de Planejamento de Projetos"),
        ]),
        _n("gab-sc","Gabinete do Comando-Geral", children=[
            _n("ag-sc","Ajudância-Geral", children=[
                _n("ajord-sc","Ajudante de Ordens do CG"),
                _n("sec-g-sc","Secretaria-Geral"),
                _n("proto-sc","Protocolo-Geral"),
                _n("arq-sc","Arquivo-Geral"),
            ]),
            _n("ouv-sc","Ouvidoria-Geral"),
            _n("ccs-sc","Centro de Comunicação Social"),
            _n("ctrl-sc","Controladoria Interna"),
        ]),
        _n("ce-sc","Conselho Estratégico"),
        _n("ass-jur-sc","Assessoria Jurídica"),
    ]),
    _n("correg-sc","Corregedoria-Geral", cat="Correição", children=[
        _n("div-ef","Divisão de Eficiência Processual"),
        _n("div-sd","Divisão de Supervisão Disciplinar"),
    ]),
    _n("dir-set-sc","Diretorias", cat="Direção Setorial", children=[
        _n("dp-sc","Diretoria de Pessoal", children=[
            _n("drh-sc","Divisão de Recursos Humanos"),
            _n("dsel-sc","Divisão de Seleção, Inclusão e Estudo de Pessoal"),
            _n("dsao-sc","Divisão de Saúde Ocupacional e Promoção Social"),
            _n("def-sc","Divisão de Educação Física"),
            _n("dst-sc-dp","Divisão de Segurança do Trabalho"),
        ]),
        _n("die-sc","Diretoria de Instrução e Ensino", children=[
            _n("deb-sc","Divisão de Ensino Básico e Complementar"),
            _n("dca-sc","Divisão de Controle e Avaliação de Ensino"),
            _n("ded-sc","Divisão de Educação a Distância"),
            _n("cefc-sc","Centro de Educação e Formação de Condutores"),
        ]),
        _n("due-sc","Diretoria de Urgência e Emergência", children=[
            _n("dnp-sc","Divisão de Normatização e Protocolos"),
            _n("dep-ue-sc","Divisão de Educação Permanente"),
            _n("dao-sc","Divisão de Apoio Operacional"),
        ]),
        _n("dlf-sc","Diretoria de Logística e Finanças", children=[
            _n("dfin-sc","Divisão de Finanças"),
            _n("dlog-sc","Divisão de Logística"),
            _n("dtic-sc","Divisão de TIC"),
        ]),
        _n("dsci-sc","Diretoria de Segurança Contra Incêndio", children=[
            _n("dnorm-sc","Divisão de Normatização"),
            _n("dinv-sc","Divisão de Investigação de Incêndio e Explosão"),
            _n("dpesq-sc","Divisão de Pesquisa e Inovação"),
            _n("deng-sc","Divisão de Engenharia Contra Incêndio"),
            _n("dfisc-sc","Divisão de Fiscalização, Auditoria e Coordenação"),
        ]),
    ]),
    _n("apoio-sc","Órgãos de Apoio", cat="Apoio", children=[
        _n("cebm","Centro de Ensino Bombeiro Militar","CEBM", children=[
            _n("abm-sc","Academia de Bombeiro Militar"),
            _n("cfap-sc","Centro de Formação e Aperfeiçoamento de Praças"),
            _n("ces-sc","Centro de Estudos Superiores"),
        ]),
        _n("aci-sc","Agência Central de Inteligência", children=[
            _n("aci-int-sc","Seção de Inteligência e Contrainteligência"),
            _n("aci-op-sc","Seção de Inteligência Operacional e Prospectiva"),
        ]),
        _n("assess-esp-sc","Assessorias Especiais", children=[
            _n("aeis","Assessoria Especial de Integração de Serviços Auxiliares"),
            _n("aeai","Assessoria Especial de Assuntos Institucionais"),
            _n("aei-sc","Assessoria Especial de Inovação"),
        ]),
    ]),
    _n("exec-sc","Regiões e Batalhões BM", cat="Execução", children=[
        _n("1rbm","1ª Região BM","1ª RBM",desc="1º, 3º, 4º, 7º, 8º, 10º, 13º BBM"),
        _n("2rbm","2ª Região BM","2ª RBM",desc="2º, 5º, 9º, 15º BBM"),
        _n("3rbm","3ª Região BM","3ª RBM",desc="6º, 11º, 12º, 14º BBM"),
        _n("bbm-sc","Batalhões BM (1º a 15º + especializados)", children=[
            _n("bbm-aer-sc","BBM de Operações Aéreas"),
            _n("bbm-cs-sc","BBM de Comando e Serviços"),
            _n("bbm-ah-sc","BBM de Ajuda Humanitária"),
        ]),
    ]),
],

# ════════════════════════════════════════════════════════════
# SÃO PAULO — Dec. nº 65.096/2020 (subordinado à Polícia Militar)
# ════════════════════════════════════════════════════════════
"sp": [
    _n("ccb-sp","Comando do Corpo de Bombeiros","CCB","Coronel PM",
       desc="Órgão responsável perante o Comando Geral pelo planejamento, comando, execução, coordenação, fiscalização e controle das atividades de prevenção, extinção de incêndios e buscas e salvamentos no território estadual.",
       ref="Lei nº 616/1974, Arts. 38 a 40", cat="Direção Geral",
       children=[
        _n("emcb-sp","Estado Maior do Corpo de Bombeiros","EM/CB",
           ref="Lei nº 616/1974, Art. 40, II e §2º", cat="Assessoramento", children=[
            _n("b6-sp","Seção de Serviço Técnico (B/6)","B/6",
               desc="Incumbida das medidas técnicas de prevenção contra incêndios: exame de plantas, perícias, testes de incombustibilidade, vistorias, pareceres e rede de hidrantes públicos.",
               ref="Lei nº 616/1974, Art. 40, §2º, 7", cat="Seção do Estado Maior"),
        ]),
        _n("secr-sp","Secretaria do Corpo de Bombeiros","Sec",
           ref="Lei nº 616/1974, Art. 40, III e §3º", cat="Apoio"),
        _n("seccmd-sp","Seção de Comando","SC",
           ref="Lei nº 616/1974, Art. 40, IV e §4º", cat="Apoio"),
        _n("cccb-sp","Centro de Comunicações do Corpo de Bombeiros","CC/CB",
           ref="Lei nº 616/1974, Art. 40, V", cat="Apoio"),
    ]),
    _n("uniop-sp","Unidades Operacionais", cat="Execução",
       desc="Unidades de execução das missões de incêndio e de busca e salvamento (Lei nº 616/1974, Art. 41). A distribuição territorial vigente é organizada nos Comandos Metropolitano e do Interior (Decreto nº 65.096/2020).",
       ref="Lei nº 616/1974, Art. 41; Art. 42", children=[
        _n("cbm-sp","Comando de Bombeiros Metropolitano","CBM",
           ref="Decreto nº 65.096/2020, Art. 25, I", cat="Execução"),
        _n("cbi-sp","Comando de Bombeiros do Interior","CBI",
           ref="Decreto nº 65.096/2020, Art. 25, II", cat="Execução"),
        _n("gi-sp","Grupamentos de Incêndio","GI",
           desc="Unidades incumbidas da extinção de incêndios, podendo integrar missões de busca e salvamento.",
           ref="Lei nº 616/1974, Art. 41, I; Art. 42", cat="Execução", children=[
            _n("sgi-sp","Sub-Grupamentos de Incêndio","S/GI",
               ref="Lei nº 616/1974, Art. 41, II; Art. 42", cat="Execução"),
        ]),
        _n("gbs-sp","Grupamentos de Busca e Salvamento","GBS",
           desc="Unidades incumbidas da missão de busca e salvamento, em razão da extensão da missão.",
           ref="Lei nº 616/1974, Art. 41, III; Art. 42", cat="Execução"),
    ]),
    _n("apoio-sp","Órgãos de Apoio", cat="Apoio",
       desc="Órgãos de apoio do Corpo de Bombeiros (Lei nº 616/1974, Art. 43, redação da Lei nº 663/1975).",
       ref="Lei nº 616/1974, Art. 43", children=[
        _n("ciad-sp","Centro de Instruções e Adestramento","CIAd",
           ref="Lei nº 616/1974, Art. 43, I", cat="Apoio"),
        _n("csmmop-sp","Centro de Suprimento e Manutenção do Material Operacional","CSM/MOp",
           ref="Lei nº 616/1974, Art. 43, II", cat="Apoio"),
    ]),
],

}  # fim CURATED_ORGANS_P3
