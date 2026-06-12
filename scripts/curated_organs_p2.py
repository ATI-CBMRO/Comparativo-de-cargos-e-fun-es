# curated_organs_p2.py — Estados: GO, MT, PR, PA, RS, SE, MS, MA

def _n(id_, name, abbr=None, rank=None, desc=None, ref=None, children=None, cat=None):
    node = {"id": id_, "name": name, "children": children or []}
    if abbr:  node["abbreviation"] = abbr
    if rank:  node["rank"] = rank
    if desc:  node["description"] = desc
    if ref:   node["legalRef"] = ref
    if cat:   node["category"] = cat
    return node


CURATED_ORGANS_P2 = {

# ════════════════════════════════════════════════════════════
# GOIÁS — Lei nº 16.899/2010 + Regimento dos Serviços Interno e Operacional
# ════════════════════════════════════════════════════════════
"go": [
    _n("cg-go","Comando-Geral","CG","Coronel",
       ref="Lei nº 16.899/2010", cat="Direção Geral", children=[
        _n("scg-go","Subcomandante-Geral"),
        _n("emg-go","Estado-Maior Geral","EMG", children=[
            _n("bm1-go","1ª Seção EMG — Pessoal e Promoções","BM/1"),
            _n("bm2-go","2ª Seção EMG — Inteligência","BM/2"),
            _n("bm3-go","3ª Seção EMG — Operações e Eventos","BM/3"),
            _n("bm4-go","4ª Seção EMG — Planejamento e Orçamento","BM/4"),
            _n("bm5-go","5ª Seção EMG — Comunicação Social","BM/5"),
            _n("bm6-go","6ª Seção EMG — TI e Comunicações","BM/6"),
            _n("bm7-go","7ª Seção EMG — Gestão e Fiscalização de Recursos","BM/7"),
            _n("bm8-go","8ª Seção EMG — Ações Sociais, Corpo Musical e Guarda de Honra","BM/8"),
            _n("bm9-go","9ª Seção EMG — Estatística e Análise da Informação","BM/9"),
        ]),
        _n("gab-go","Gabinete do CG","GCG", children=[
            _n("gab-scg-go","Gabinete do SCG","GSCG"),
        ]),
        _n("sg-go","Secretaria-Geral","SG"),
        _n("ouv-go","Ouvidoria Adjunta","OA/CBMGO"),
    ]),
    _n("dir-set-go","Comandos de Direção Setorial", cat="Direção Setorial",
       ref="Regimento dos Serviços Interno e Operacional", children=[
        _n("ccd","Comando de Correições e Disciplina","CCD","Coronel"),
        _n("codec","Comando de Operações de Defesa Civil","CODEC","Coronel"),
        _n("caebm","Comando da Academia e Ensino Bombeiro Militar","CAEBM","Coronel"),
        _n("cal-go","Comando de Apoio Logístico","CAL","Coronel"),
        _n("cgf-go","Comando de Gestão e Finanças","CGF"),
        _n("cat-go","Comando de Atividades Técnicas","CAT","Coronel"),
        _n("cge-go","Comando de Gestão Estratégica","CGE","Coronel"),
        _n("cme-go","Comando de Missões Especiais","CME","Coronel"),
    ]),
    _n("apoio-go","Órgãos de Apoio", cat="Apoio", children=[
        _n("coa","Centro de Operações Aéreas","COA"),
        _n("cob-go","Centro Operacional de Bombeiros","COB"),
        _n("ceman-go","Centro de Manutenção","CEMAN"),
        _n("csau-go","Comando de Saúde","CSAU"),
        _n("cmbm","Corpo Musical Bombeiro Militar","CMBM"),
    ]),
    _n("exec-go","Órgãos de Execução Regional", cat="Execução", children=[
        _n("1crbm-go","1º CRBM — Goiânia (Capital)","1º CRBM"),
        _n("2crbm-go","2º CRBM — Rio Verde","2º CRBM"),
        _n("3crbm-go","3º CRBM — Anápolis","3º CRBM"),
        _n("4crbm-go","4º CRBM — Luziânia","4º CRBM"),
        _n("5crbm-go","5º CRBM — Aparecida de Goiânia","5º CRBM"),
        _n("6crbm-go","6º CRBM — Goiás","6º CRBM"),
        _n("7crbm-go","7º CRBM — Caldas Novas","7º CRBM"),
        _n("8crbm-go","8º CRBM — Uruaçu","8º CRBM"),
        _n("9crbm-go","9º CRBM — Formosa","9º CRBM"),
        _n("bbm-esp-go","Batalhões Especializados", children=[
            _n("bse-go","Batalhão de Salvamento em Emergência","BSE"),
            _n("bopar","1º BBM — Batalhão de Operações, Proteção Ambiental e Resposta a Desastres","BOPAR"),
            _n("beopp","21º BBM — Batalhão Especializado em Operações com Produtos Perigosos","BEOPP"),
        ]),
        _n("bbm-reg-go","Batalhões Regionais (3º ao 23º BBM)"),
        _n("cibm-go","26 Companhias Independentes BM","CIBM"),
        _n("pbm-go","Pelotões BM (3 unidades)","PBM"),
        _n("dbm-go","24 Destacamentos BM"),
    ]),
],

# ════════════════════════════════════════════════════════════
# MATO GROSSO — LC nº 775/2023 (alt. LC 806/2024) + Regimento Interno
# ════════════════════════════════════════════════════════════
"mt": [
    _n("cg-mt","Comando-Geral","CG","Coronel QOBM",
       ref="LC nº 775/2023", cat="Direção Geral", children=[
        _n("colegiados-mt","Conselhos Superiores", children=[
            _n("csup-mt","Conselho Superior de Bombeiros Militar"),
            _n("csepe","Conselho Superior de Ensino, Pesquisa e Extensão"),
        ]),
        _n("cgadj","Comandante-Geral Adjunto / Chefe do Estado-Maior-Geral","","Coronel QOBM"),
        _n("correg-mt","Corregedoria Geral", children=[
            _n("correg-adj-mt","Corregedoria Adjunta"),
            _n("corr-adm-mt","Seção Administrativa"),
            _n("corr-pjm-mt","Seção de Polícia Judiciária Militar"),
            _n("corr-pad","Seção de Procedimentos Administrativos Disciplinares"),
        ]),
        _n("ouv-mt","Ouvidoria Setorial", children=[
            _n("ouv-sec-mt","Seção Administrativa"),
        ]),
        _n("ctrl-mt","Controladoria Interna Setorial", children=[
            _n("ctrl-adm-mt","Seção Administrativa"),
            _n("ctrl-aud","Seção de Auditoria e Controle de Gestão"),
            _n("ctrl-op","Seção de Controle Operacional"),
        ]),
        _n("assess-mt","Assessorias Superiores", children=[
            _n("ass-jur-mt","Assessoria Jurídica"),
            _n("ass-aic","Assessoria de Articulação e Integração Comunitária"),
            _n("ass-aph","Assessoria de Atendimento Pré-Hospitalar"),
            _n("ass-dc","Assessoria de Proteção e Defesa Civil"),
            _n("ass-inter","Assessoria Interinstitucional"),
            _n("ass-parl-mt","Assessoria Parlamentar"),
            _n("ass-ri","Assessoria de Relações Internacionais"),
        ]),
        _n("gab-cg-mt","Gabinete do Comandante-Geral", children=[
            _n("gab-chefe-mt","Chefia de Gabinete"),
            _n("gab-sec-mt","Secretaria do Gabinete"),
            _n("ajord-mt","Ajudante-de-Ordens"),
        ]),
        _n("aci-mt","Agência Central de Inteligência", children=[
            _n("int-sec","Seção de Inteligência"),
            _n("int-ci","Seção de Contra Inteligência"),
            _n("int-op","Seção de Inteligência Operacional"),
        ]),
        _n("ccs-mt","Centro de Comunicação Social BM", children=[
            _n("ccs-rp","Seção de Relações Públicas e Cerimonial"),
            _n("ccs-imp","Seção de Assessoria de Imprensa"),
            _n("ccs-prod","Seção de Produção e Divulgação"),
        ]),
    ]),
    _n("dir-set-mt","Diretorias de Administração Sistêmica", cat="Direção Setorial",
       ref="LC nº 775/2023", children=[
        _n("dai","Diretoria de Administração Institucional","DAI", children=[
            _n("dai-fin","Seção de Finanças"),
            _n("dai-log","Seção Logística e Patrimônio"),
            _n("dai-tic","Seção de Tecnologia da Informação e Comunicação"),
            _n("dai-eng","Seção de Engenharia"),
            _n("csm-mt","Centro de Suprimento e Manutenção", children=[
                _n("csm-vtr","Seção de Suprimento e Manutenção de Viatura"),
                _n("csm-mot","Seção de Suprimento e Manutenção de Material Motomecanizado"),
                _n("csm-op","Seção de Suprimento e Manutenção de Material Operacional"),
            ]),
        ]),
        _n("dgp-mt","Diretoria de Gestão de Pessoas","DGP", children=[
            _n("dgp-rs","Seção de Recrutamento e Seleção"),
            _n("dgp-fp","Seção de Folha de Pagamento"),
            _n("dgp-cp","Seção de Desenvolvimento e Controle de Pessoal"),
            _n("dgp-av","Seção de Avaliação de Desempenho"),
            _n("dgp-tmp","Seção de Pessoal Temporário"),
            _n("cgsps","Centro de Gestão do Sistema de Proteção Social BM", children=[
                _n("cgsps-ben","Seção de Concessão de Benefícios"),
                _n("cgsps-man","Seção de Manutenção"),
                _n("cgsps-mon","Seção de Monitoramento"),
                _n("cgsps-cal","Seção de Cálculos"),
            ]),
        ]),
        _n("deip-mt","Diretoria de Ensino, Instrução e Pesquisa","DEIP", children=[
            _n("deip-fi","Seção de Formação Inicial e Continuada"),
            _n("deip-gc","Seção de Gestão do Conhecimento"),
            _n("esbm","Escola Superior Bombeiro Militar", children=[
                _n("abm-mt","Academia de Bombeiros Militar","ABM", children=[
                    _n("abm-ce","Conselho de Ensino e Disciplina"),
                    _n("abm-de","Divisão de Ensino"),
                    _n("abm-da","Divisão Administrativa"),
                    _n("abm-alunos","Divisão de Alunos"),
                ]),
                _n("cfap-mt","Núcleo de Ensino — Formação e Aperfeiçoamento de Praças"),
                _n("nfr","Núcleos de Formação Regional"),
            ]),
            _n("cdpi","Centro de Desenvolvimento, Pesquisa e Inovação", children=[
                _n("obs","Observatório de Segurança e Defesa Civil"),
                _n("pesq","Seção de Pesquisa e Tecnologia"),
                _n("lab","Seção de Laboratórios de Ensaios e Testes"),
            ]),
            _n("ccfm-mt","Centro de Capacitação Física Militar"),
            _n("mhcbm","Museu Histórico do Corpo de Bombeiros Militar"),
            _n("cfc-mt","Centro de Formação de Condutores"),
        ]),
        _n("dge-mt","Diretoria de Gestão Estratégica","DGE", children=[
            _n("dge-pl","Seção de Planejamento e Execução Orçamentária"),
            _n("dge-est","Seção de Estatística e Arrecadação"),
            _n("dge-conv","Seção de Convênios"),
            _n("edp-mt","Escritório Diretivo de Projetos do CBM"),
        ]),
        _n("ds-mt","Diretoria de Saúde","DS", children=[
            _n("ds-sm","Seção de Saúde do Pessoal Militar"),
            _n("ds-aph","Seção de Atendimento Pré-Hospitalar e Resgate"),
            _n("amb-mt","Ambulatório do CBM"),
            _n("cis-mt","Centro de Inspeção de Saúde"),
            _n("cab-mt","Centro de Assistência Biopsicossocial"),
        ]),
    ]),
    _n("apoio-cga-mt","Apoio ao Cmd.-Geral Adjunto", cat="Apoio", children=[
        _n("gab-cgadj","Gabinete do Cmd.-Geral Adjunto"),
        _n("ag-mt","Ajudância Geral", children=[
            _n("ag-cia","Companhia de Comando e Serviços"),
        ]),
        _n("corpo-mus-mt","Corpo Musical do CBM", children=[
            _n("banda-mt","Banda de Música"),
            _n("banda-reg","Bandas Regionais"),
            _n("banda-sinf","Banda Sinfônica"),
            _n("coral-mt","Coral"),
        ]),
    ]),
    _n("exec-mt","Nível de Execução", cat="Execução", children=[
        _n("dscip-mt","Diretoria de Segurança Contra Incêndio e Pânico","DSCIP", children=[
            _n("dscip-ap","Seção de Análise de Processos"),
            _n("dscip-fisc","Seção de Fiscalização"),
            _n("dscip-en","Seção de Estudos, Normas e Pareceres"),
            _n("dscip-per","Seção de Perícia de Incêndio"),
        ]),
        _n("dop-mt","Diretoria Operacional","DOp", children=[
            _n("dop-pto","Seção de Planejamento Tático e Operacional"),
            _n("dop-dout","Seção de Doutrina e Emprego Operacional"),
            _n("dop-hid","Seção de Hidrantes"),
            _n("dop-geo","Seção de Estatística e Georreferenciamento"),
            _n("bea","Batalhão de Emergências Ambientais","BEA", children=[
                _n("caepp","Cia. de Atendimento a Emergência com Produtos Perigosos","CAEPP"),
                _n("cpcif","Cia. de Prevenção e Combate a Incêndio Florestal","CPCIF"),
            ]),
            _n("gavbm","Grupo de Aviação de Bombeiros Militar","GAvBM"),
            _n("crbm-mt","Comandos Regionais BM","CRBM", children=[
                _n("bbm-mt","Batalhões BM","BBM"),
                _n("cibm-mt","Cias. Independentes BM","CIBM"),
                _n("pibm-mt","Pelotões Independentes BM","PIBM"),
                _n("nbm-mt","Núcleos BM","NBM"),
            ]),
        ]),
    ]),
],

# ════════════════════════════════════════════════════════════
# PARANÁ — Lei nº 22.206/2024 + Regimento Interno
# ════════════════════════════════════════════════════════════
"pr": [
    _n("cg-pr","Comando-Geral","CmdoG","Coronel Combatente",
       ref="Lei nº 22.206/2024", cat="Direção Geral", children=[
        _n("cmt-pr","Comandante-Geral","CG","Coronel Combatente"),
        _n("scmt-pr","Subcomandante-Geral","SCG","Coronel Combatente"),
        _n("em-pr","Estado-Maior","EM", children=[
            _n("bm1-pr","1ª Seção — Pessoal e Legislação","BM/1"),
            _n("bm2-pr","2ª Seção — Inteligência","BM/2"),
            _n("bm3-pr","3ª Seção — Operações e Estatística","BM/3"),
            _n("bm4-pr","4ª Seção — Logística","BM/4"),
        ]),
        _n("gab-pr","Gabinete do Comando-Geral","Gab.CmtG", children=[
            _n("ag-pr","Ajudância-Geral","AG"),
            _n("assest-pr","Assessoria Estratégica","Assest"),
            _n("assecom-pr","Assessoria de Comunicação Organizacional","Assecom"),
            _n("sec-cg-pr","Secretaria do Comando-Geral","Sec.CmdoG"),
        ]),
        _n("ci-pr","Consultoria Institucional","CI"),
        _n("correg-pr","Corregedoria-Geral","Coger","Coronel Combatente"),
        _n("comissoes-pr","Comissões", children=[
            _n("cpo-pr","Comissão de Promoções de Oficiais","CPO"),
            _n("cpp-pr","Comissão de Promoções de Praças","CPP"),
            _n("cm-pr","Comissão de Mérito","CM"),
        ]),
    ]),
    _n("dir-set-pr","Órgãos de Direção Setorial", cat="Direção Setorial", children=[
        _n("dp-pr","Diretoria de Pessoal","DP","Oficial Superior", children=[
            _n("crs-pr","Centro de Recrutamento e Seleção","CRS"),
            _n("cs-pr","Centro de Saúde","CS"),
            _n("cefid-pr","Centro de Educação Física e Desporto","CEFID"),
        ]),
        _n("dalf-pr","Diretoria de Apoio Logístico e Finanças","DALF","Oficial Superior", children=[
            _n("cpc-pr","Centro de Planejamento e Compras","CPC"),
            _n("cal-pr","Centro de Administração Logística","CAL"),
            _n("cof-pr","Centro de Orçamento e Finanças","COF"),
            _n("csm-pr","Centro de Suprimento e Manutenção","CSM"),
        ]),
        _n("dat-pr","Diretoria de Atividades Técnicas","DAT","Oficial Superior"),
        _n("esbm-pr","Escola Superior de Bombeiro Militar","ESBM","Oficial Superior"),
    ]),
    _n("exec-pr","Órgãos de Execução", cat="Execução", children=[
        _n("crbm-pr","Comandos Regionais BM","CRBM"),
        _n("bbm-pr","Batalhões de BM","BBM", children=[
            _n("cia-pr","Companhias BM","Cia.BM"),
            _n("pel-pr","Pelotões BM","Pel.BM"),
            _n("gp-pr","Grupos BM","Gp.BM"),
        ]),
        _n("gost","Grupo de Operações de Socorro Tático","GOST"),
        _n("uoa-pr","Unidades de Operações Aéreas","UOA"),
    ]),
],

# ════════════════════════════════════════════════════════════
# PARÁ — Lei nº 11.060/2025 + Regimento Interno
# ════════════════════════════════════════════════════════════
"pa": [
    _n("cg-pa","Comando-Geral","CG","Coronel QOBM",
       ref="Lei nº 11.060/2025", cat="Direção Geral", children=[
        _n("alto-cmd-pa","Alto Comando",
           desc="Órgão colegiado presidido pelo CG. Membros: Chefe do EMG, Coordenador-Adj. CEDEC, Corregedor-Geral, Cmd. Operacional, Chefes dos Departamentos-Gerais.", children=[
            _n("emg-pa","Estado-Maior Geral","EMG", children=[
                _n("emg-pa1","1ª Seção — Pessoal e Legislação","BM/1"),
                _n("emg-pa2","2ª Seção — Gestão do Conhecimento e Inovação","BM/2"),
                _n("emg-pa3","3ª Seção — Operações, Doutrina e Estatística","BM/3"),
                _n("emg-pa4","4ª Seção — Logística","BM/4"),
                _n("emg-pa5","5ª Seção — Gestão pela Qualidade","BM/5"),
                _n("emg-pa6","6ª Seção — Planejamento e Orçamento Institucional","BM/6"),
                _n("edp-pa","Escritório de Projetos e Convênios"),
            ]),
        ]),
        _n("cedec-pa","Coordenadoria Estadual de Proteção e Defesa Civil","CEDEC","Coronel QOBM", children=[
            _n("cedec-gr","Divisão de Gestão de Risco"),
            _n("cedec-gd","Divisão de Gerenciamento de Desastres"),
            _n("cedec-adm","Divisão Administrativa"),
            _n("cedec-of","Divisão Orçamentária e Financeira"),
            _n("cedec-ass","Assessoria de Articulação e Gestão"),
        ]),
        _n("correg-pa","Corregedoria-Geral","CORREG","Coronel QOBM", children=[
            _n("scorr-pa","Subcorregedor-Geral","","Tenente-Coronel"),
            _n("cd-ger","Comissão Disciplinar Geral"),
            _n("cd-rec","Comissão Disciplinar de Recurso"),
            _n("corr-int-pa","Seção de Inteligência Correcional e Operações"),
            _n("corr-gest","Seção de Gestão de Processos e Apoio Administrativo"),
        ]),
        _n("cmd-op-pa","Comando de Operações","","Coronel QOBM", children=[
            _n("cop-ps","Seção de Planejamento de Pessoal"),
            _n("cop-log","Seção de Planejamento Logístico"),
            _n("cop-op","Seção de Planejamento de Operações e Estatística"),
            _n("cop-ev","Seção de Planejamento de Eventos"),
        ]),
        _n("gab-pa","Gabinete do Comandante-Geral"),
        _n("ag-pa","Ajudância-Geral"),
        _n("ctrl-pa","Controladoria Interna"),
        _n("cj-pa","Consultoria Jurídica"),
        _n("ci-pa","Centro de Inteligência"),
    ]),
    _n("deptos-pa","Departamentos-Gerais de Direção Setorial", cat="Direção Setorial", children=[
        _n("dga","Departamento-Geral de Administração","DGA"),
        _n("dgp-pa","Departamento-Geral de Pessoal","DGP"),
        _n("dgcep","Departamento-Geral de Cultura, Educação e Pesquisa","DGCEP"),
        _n("dgsci","Departamento-Geral de Segurança contra Incêndios e Emergências","DGSCI"),
        _n("dal-pa","Diretoria de Apoio Logístico","DAL"),
        _n("df-pa","Diretoria de Finanças","DF"),
        _n("dca-pa","Diretoria de Contratações e Aquisições","DCA"),
        _n("dtic-pa","Diretoria de TIC","DTIC"),
        _n("ds-pa","Diretoria de Saúde"),
    ]),
    _n("dir-int-pa","Direção Intermediária", cat="Direção Regional", children=[
        _n("crb","Comandos Regionais de Bombeiros de Proteção e Emergência","CRB"),
    ]),
    _n("apoio-pa","Órgãos de Apoio", cat="Apoio", children=[
        _n("abm-pa","Academia Bombeiro Militar"),
        _n("cfae-pa","Centro de Formação, Aperfeiçoamento e Especialização"),
        _n("ccfd-pa","Centro de Capacitação Física e Desporto"),
        _n("csm-pa","Centro de Suprimento e Manutenção de Viaturas e Materiais"),
        _n("cp-pa","Centro de Patrimônio"),
        _n("cm-pa","Centro de Memória"),
        _n("cap-pa","Capelania"),
        _n("bm-pa","Banda de Música"),
    ]),
    _n("exec-pa","Órgãos de Execução", cat="Execução", children=[
        _n("gbm-pa","Grupamento Bombeiro Militar","GBM"),
        _n("sgbm-pa","Subgrupamento Bombeiro Militar"),
        _n("sbm-pa","Seção Bombeiro Militar"),
        _n("gmaf","Grupamento Marítimo e Fluvial","GMAF"),
        _n("gbs-pa","Grupamento de Busca e Salvamento","GBS"),
        _n("gse-pa","Grupamento de Socorro e Emergência","GSE"),
        _n("goa-pa","Grupamento de Operações Aéreas","GOA"),
        _n("nac","Núcleo de Ações com Cães","NAC"),
    ]),
],

# ════════════════════════════════════════════════════════════
# RIO GRANDE DO SUL — LC nº 14.920/2016 + Dec. nº 53.897/2018
# ════════════════════════════════════════════════════════════
"rs": [
    _n("cg-rs","Comando-Geral","Cmt-G","Coronel Combatente",
       ref="LC nº 14.920/2016; Dec. nº 53.897/2018", cat="Direção Geral", children=[
        _n("scmt-rs","Subcomandante-Geral","SCmt-G","Coronel Combatente"),
        _n("csup-rs","Conselho Superior","CSup",desc="Órgão consultivo."),
        _n("correg-rs","Corregedoria-Geral","Corr-G", children=[
            _n("dadm-correg","Divisão Administrativa","DAdm/Corr-G"),
            _n("djd","Divisão de Justiça e Disciplina","DJD/Corr-G"),
            _n("dcic","Divisão de Controle Interno Correcional","DCIC/Corr-G"),
            _n("dfe","Divisão de Feitos Especiais","DFE/Corr-G"),
            _n("ouv-rs","Ouvidoria","Ouv/Corr-G"),
        ]),
        _n("gcg-rs","Gabinete do Comandante-Geral","GCG", children=[
            _n("secexec-rs","Secretaria-Executiva do CG","SecExec/GCG"),
            _n("ci-rs","Assessoria de Controle Interno","CI/GCG"),
            _n("ajcc","Assessoria Jurídica, Convênios e Contratos","AJCC/GCG"),
            _n("acs-rs","Assessoria de Comunicação Social","ACS/GCG"),
            _n("aci-rs","Agência Central de Inteligência","ACI/GCG"),
            _n("aperi","Assessoria de Planejamento Estratégico e Relações Institucionais","APERI/GCG"),
        ]),
        _n("cam-rs","Comissão de Avaliação e Mérito","CAM", children=[
            _n("samo","Subcomissão de Avaliação e Mérito de Oficiais","SAMO/CAM"),
            _n("samp","Subcomissão de Avaliação e Mérito de Praças","SAMP/CAM"),
        ]),
    ]),
    _n("deptos-rs","Nível Departamental", cat="Direção Setorial",
       ref="Dec. nº 53.897/2018", children=[
        _n("da-rs","Departamento Administrativo","DA", children=[
            _n("dadm-rs","Divisão Administrativa","DAdm"),
            _n("dlp-rs","Divisão de Logística e Patrimônio","DLP"),
            _n("dof-rs","Divisão de Orçamento e Finanças","DOF"),
            _n("drh-rs","Divisão de Recursos Humanos","DRH"),
            _n("dtic-rs","Divisão de TIC","DTIC"),
        ]),
        _n("dspci","Departamento de Segurança, Prevenção e Proteção Contra Incêndio","DSPCI", children=[
            _n("dgn","Divisão de Gestão e Normatização","DGN"),
            _n("dpis","Divisão de Pesquisa e Investigação de Sinistros","DPIS"),
        ]),
        _n("abm-rs","Academia de Bombeiro Militar","ABM", children=[
            _n("dens-abm","Divisão de Ensino","DEns/ABM"),
            _n("opeta","Órgão de Pesquisa, Ensino, Treinamento e Avaliação","OPETA", children=[
                _n("esef","Escola de Educação Física","EsEF/OPETA"),
                _n("esscid","Escola Superior de Segurança Contra Incêndio e Desastres","ESSCID/OPETA"),
                _n("esbo","Escola de Bombeiro Militar","EsBo/OPETA"),
                _n("escab","Escola de Serviços Civis Auxiliares de Bombeiro","ESCAB/OPETA"),
            ]),
        ]),
        _n("aodc","Assessoria de Operações, Defesa Civil e Serviços Civis","AODC", children=[
            _n("dodc","Divisão de Operações e Defesa Civil","DODC/AODC"),
            _n("dscab","Divisão de Serviços Civis e Auxiliares de Bombeiro","DSCAB/AODC"),
            _n("dmo","Divisão de Monitoramento Operacional","DMO/AODC"),
            _n("doa-rs","Divisão de Operações Aéreas","DOA/AODC"),
        ]),
    ]),
    _n("exec-rs","Nível Operacional / Comandos Regionais", cat="Execução", children=[
        _n("1crbm-rs","1º CRBM — Porto Alegre","1ºCRBM", children=[
            _n("1bbm-rs","1º BBM — Porto Alegre"),
            _n("8bbm-rs","8º BBM — Canoas"),
            _n("9bbm-rs","9º BBM — Tramandaí"),
            _n("bbs-rs","Batalhão de Busca e Salvamento","BBS"),
        ]),
        _n("2crbm-rs","2º CRBM — Caxias do Sul","2ºCRBM", children=[
            _n("2bbm-rs","2º BBM — São Leopoldo"),
            _n("5bbm-rs","5º BBM — Caxias do Sul"),
            _n("7bbm-rs","7º BBM — Passo Fundo"),
        ]),
        _n("3crbm-rs","3º CRBM — Pelotas","3ºCRBM", children=[
            _n("3bbm-rs","3º BBM — Rio Grande"),
            _n("10bbm-rs","10º BBM — Santana do Livramento"),
            _n("13bbm-rs","13º BBM — Uruguaiana"),
        ]),
        _n("4crbm-rs","4º CRBM — Santa Maria","4ºCRBM", children=[
            _n("4bbm-rs","4º BBM — Santa Maria"),
            _n("6bbm-rs","6º BBM — Santa Cruz do Sul"),
            _n("11bbm-rs","11º BBM — Santo Ângelo"),
            _n("12bbm-rs","12º BBM — Ijuí"),
        ]),
        _n("besci","Batalhão Especial de Segurança contra Incêndio","BESCI","","Abrangência estadual"),
    ]),
],

# ════════════════════════════════════════════════════════════
# SERGIPE — Lei nº 8.979/2022 + Regimento Interno
# ════════════════════════════════════════════════════════════
"se": [
    _n("cg-se","Comando-Geral","CG","Coronel QOBM",
       ref="Lei nº 8.979/2022, Art. 5º–7º", cat="Direção Estratégica", children=[
        _n("cmt-se","Comandante-Geral","CG","Coronel QOBM (Comb., ativa, último posto; CFO+APO+CSBM, Art. 6º)"),
        _n("scmt-se","Subcomandante-Geral / Chefe do EMG","SCG","Coronel QOBM (Art. 8º)"),
        _n("emg-se","Estado-Maior-Geral","EMG", ref="Art. 10"),
        _n("gab-se","Gabinete", ref="Art. 11–14", children=[
            _n("chgab-se","Chefia de Gabinete","","Oficial Superior QOBM"),
            _n("ajord-se","Ajudância de Ordens"),
            _n("ajudancia-geral-se","Ajudância-Geral","AjG","Oficial Superior QOBM"),
        ]),
        _n("corregedoria-geral-se","Corregedoria-Geral","Corr-G","Coronel QOBM (Art. 15 p.u.)", ref="Art. 15"),
        _n("controladoria-interna-se","Controladoria Interna","CI", ref="Art. 16"),
        _n("ouvidoria-geral-se","Ouvidoria-Geral","Ouv-G", ref="Art. 17"),
        _n("assessorias-se","Assessorias", ref="Art. 18", desc="Assessoria Técnica de Engenharia e Arquitetura; de Inteligência; Técnica Institucional; de Comunicação; de TI; Parlamentar (Art. 18 §1º)."),
        _n("ac-se","Alto-Comando","AC", ref="Art. 20", desc="Órgão Colegiado Superior, presidido pelo Comandante-Geral (Art. 20)."),
    ]),
    _n("dir-geral-se","Órgãos de Direção-Geral", ref="Lei nº 8.979/2022, Art. 22–27", cat="Direção Geral", children=[
        _n("dlog-se","Diretoria de Logística","DLOG","Coronel QOBM (último posto)", ref="Art. 23"),
        _n("dfin-se","Diretoria de Finanças","DFIN","Coronel QOBM (último posto)", ref="Art. 24"),
        _n("dgp-se","Diretoria de Gestão de Pessoal","DGP","Coronel QOBM (último posto)", ref="Art. 25"),
        _n("dep-se","Diretoria de Ensino e Pesquisa","DEP","Coronel QOBM (último posto)", ref="Art. 26"),
        _n("dplan-se","Diretoria de Planejamento","DPLAN","Coronel QOBM (último posto)", ref="Art. 27"),
    ]),
    _n("dir-op-se","Órgãos de Direção Operacional", ref="Lei nº 8.979/2022, Art. 28–31", cat="Direção Operacional", children=[
        _n("dat-se","Diretoria de Atividades Técnicas","DAT","Coronel QOBM (último posto)", ref="Art. 29"),
        _n("dop-se","Diretoria Operacional","DOP","Coronel QOBM (último posto)", ref="Art. 30", children=[
            _n("crm-se","Comando Regional Metropolitano","CRM","Oficial Superior QOBM", ref="Art. 35 §2º I", children=[
                _n("1gbm-se","1º Grupamento Bombeiro Militar","1º GBM","Oficial Superior QOBM", ref="Art. 37 I", desc="Localizado em Aracaju."),
                _n("4gbm-se","4º Grupamento Bombeiro Militar","4º GBM","Oficial Superior QOBM", ref="Art. 37 IV", desc="Localizado em Nossa Senhora do Socorro (CRM/CRL)."),
                _n("8gbm-se","8º Grupamento Bombeiro Militar","8º GBM","Oficial Superior QOBM", ref="Art. 37 VIII", desc="Localizado na Barra dos Coqueiros."),
            ]),
            _n("cras-se","Comando Regional do Alto Sertão","CRAS","Oficial Superior QOBM", ref="Art. 35 §2º II", children=[
                _n("7gbm-se","7º Grupamento Bombeiro Militar","7º GBM","Oficial Superior QOBM", ref="Art. 37 VII", desc="Localizado em Nossa Senhora da Glória (CRAS/CRMS)."),
            ]),
            _n("crms-se","Comando Regional do Médio Sertão","CRMS","Oficial Superior QOBM", ref="Art. 35 §2º III"),
            _n("crcs-se","Comando Regional do Centro Sul","CRCS","Oficial Superior QOBM", ref="Art. 35 §2º IV", children=[
                _n("5gbm-se","5º Grupamento Bombeiro Militar","5º GBM","Oficial Superior QOBM", ref="Art. 37 V", desc="Localizado em Lagarto."),
            ]),
            _n("crs-se","Comando Regional do Sul","CRS","Oficial Superior QOBM", ref="Art. 35 §2º V", children=[
                _n("2gbm-se","2º Grupamento Bombeiro Militar","2º GBM","Oficial Superior QOBM", ref="Art. 37 II", desc="Localizado em Estância."),
            ]),
            _n("crl-se","Comando Regional do Leste","CRL","Oficial Superior QOBM", ref="Art. 35 §2º VI"),
            _n("cra-se","Comando Regional do Agreste","CRA","Oficial Superior QOBM", ref="Art. 35 §2º VII", children=[
                _n("3gbm-se","3º Grupamento Bombeiro Militar","3º GBM","Oficial Superior QOBM", ref="Art. 37 III", desc="Localizado em Itabaiana."),
            ]),
            _n("crbsf-se","Comando Regional do Baixo São Francisco","CRBSF","Oficial Superior QOBM", ref="Art. 35 §2º VIII", children=[
                _n("6gbm-se","6º Grupamento Bombeiro Militar","6º GBM","Oficial Superior QOBM", ref="Art. 37 VI", desc="Localizado em Propriá."),
            ]),
            _n("gbs-se","Grupamento de Busca e Salvamento","GBS","Oficial Superior QOBM", ref="Art. 39 I"),
            _n("goa-se","Grupamento de Operações Aéreas","GOA","Oficial Superior QOBM", ref="Art. 39 II"),
        ]),
    ]),
],

# ════════════════════════════════════════════════════════════
# MATO GROSSO DO SUL — LC nº 188/2014 (alt. LC 323/2023)
# ════════════════════════════════════════════════════════════
"ms": [
    _n("cg-ms","Comando Geral","CG","Coronel Combatente QOBM",
       ref="LC nº 188/2014", cat="Direção Geral", children=[
        _n("scmt-ms","Subcomandante-Geral","","Coronel Combatente QOBM"),
        _n("emg-ms","Estado-Maior-Geral","EMG","Coronel Combatente QOBM", children=[
            _n("bm1-ms","1ª Seção — Pessoal e Legislação","BM-1"),
            _n("bm2-ms","2ª Seção — Inteligência","BM-2"),
            _n("bm3-ms","3ª Seção — Instrução, Operações, Ensino, Estatística e Meio Ambiente","BM-3"),
            _n("bm4-ms","4ª Seção — Logística, Patrimônio e Informática","BM-4"),
            _n("bm5-ms","5ª Seção — Comunicação Social","BM-5"),
            _n("bm6-ms","6ª Seção — Planejamento Administrativo, Orçamentário e Financeiro","BM-6"),
            _n("bm7-ms","7ª Seção — Proteção Contra Incêndio, Pânico e Outros Riscos","BM-7"),
        ]),
        _n("correg-ms","Corregedoria","","Coronel Combatente QOBM", children=[
            _n("scorr-ms","Corregedor-Adjunto","","Penúltimo posto QOBM"),
            _n("gab-corr-ms","Gabinete do Corregedor"),
            _n("cart-ms","Cartório"),
            _n("sjd-ms","Seção de Justiça e Disciplina"),
            _n("cpd-ms","Conselho Permanente de Disciplina"),
            _n("ouv-ms","Ouvidoria"),
            _n("sint-ms","Seção de Inteligência"),
            _n("pdo-ms","Patrulha Disciplinar Ostensiva"),
        ]),
        _n("ag-ms","Ajudância Geral","AG","Coronel Combatente QOBM"),
        _n("gab-cg-ms","Gabinete do CG","GabCG","Penúltimo posto QOBM"),
        _n("cjur-ms","Coordenadoria Jurídica","CJur","Of. Superior — Bacharel em Direito"),
        _n("ass-ms","Assessorias Especiais","AssEsp"),
        _n("ass-parl-ms","Assessoria Parlamentar","AssP"),
    ]),
    _n("dir-set-ms","Diretorias (Direção Setorial)", cat="Direção Setorial",
       desc="Subordinadas ao Subcomandante-Geral.", children=[
        _n("dp-ms","Diretoria de Pessoal","DP"),
        _n("dal-ms","Diretoria de Apoio Logístico","DAL"),
        _n("df-ms","Diretoria de Finanças","DF"),
        _n("dat-ms","Diretoria de Atividades Técnicas","DAT"),
        _n("deipe","Diretoria de Ensino, Instrução, Pesquisa e Educação","DEIPE", children=[
            _n("abm-ms","Academia de Bombeiros Militar","ABM", children=[
                _n("esbom-ms","Escola Superior de Bombeiros","EsBom"),
                _n("cfae-ms","Centro de Formação, Aperfeiçoamento e Especialização","CFAE"),
                _n("cieb","Centro de Instrução Especializada","CIEB"),
            ]),
        ]),
        _n("ds-ms","Diretoria de Saúde","DS", children=[
            _n("poli-ms","Policlínica"),
            _n("craph","Centro de Resgate e Atendimento Pré-hospitalar","CRAPH"),
            _n("cab-ms","Centro de Atendimento Biopsicossocial","CAB"),
            _n("capel-ms","Capelania Militar","CapMil"),
        ]),
        _n("dtel-ms","Diretoria de Telemática e Estatística","DTel", children=[
            _n("cit-ms","Centro de Informática e Tecnologia","CIT"),
        ]),
        _n("dpa-ms","Diretoria de Proteção Ambiental","DPA"),
        _n("dintel-ms","Diretoria de Inteligência","DIntel"),
    ]),
    _n("gds-ms","Grandes Comandos", cat="Execução", children=[
        _n("cmb","Comando Metropolitano de Bombeiros","CMB","Último posto QOBM"),
        _n("cbdiv","Comando de Bombeiros de Divisas","CBDiv"),
        _n("cbfron","Comando de Bombeiros de Fronteiras","CBFron"),
        _n("cbesp","Comando de Bombeiros de Atividades Especializadas","CBEsp"),
        _n("cocb","Comando de Operações do CBM","COCB"),
    ]),
    _n("ap-scg-ms","Apoio ao Subcomando-Geral", cat="Apoio", children=[
        _n("gab-scg-ms","Gabinete do SCG","GabScG"),
        _n("goa-ms","Grupamento de Operações Aéreas","GOA"),
        _n("cpa-ms","Centro de Proteção Ambiental","CPA"),
        _n("csm-ms","Centro de Suprimento e Manutenção","CSM"),
    ]),
],

# ════════════════════════════════════════════════════════════
# MARANHÃO — Lei nº 10.230/2015 + Quadro de Organização e Distribuição
# ════════════════════════════════════════════════════════════
"ma": [
    _n("cg-ma","Comando-Geral", cat="Direção Geral",
       ref="Lei nº 10.230/2015", children=[
        _n("alto-cmd-ma","Alto-Comando",
           desc="Órgão consultivo. Presidente: CG. Membros natos: Cmd. Adj./Chefe EMG, Subchefe EMG, Coord. Est. CPDC. Membros efetivos: Diretores.", children=[
            _n("emg-ma","Estado-Maior-Geral","EMG", children=[
                _n("emg-chefe-ma","Chefe do EMG","","Coronel Combatente"),
                _n("emg-sub-ma","Subchefe do EMG","","Coronel Combatente"),
                _n("bm1-ma","1ª Seção — Pessoal e Legislação","BM/1","Tenente-Coronel"),
                _n("bm2-ma","2ª Seção — Legislação Técnica, Perícias e Prevenção","BM/2","Tenente-Coronel"),
                _n("bm3-ma","3ª Seção — Ensino, Instrução, Operações e Doutrina","BM/3","Tenente-Coronel"),
                _n("bm4-ma","4ª Seção — Modernização, Material e Orçamento","BM/4","Tenente-Coronel"),
                _n("bm5-ma","5ª Seção — Relações Públicas e Comunicação Social","BM/5","Tenente-Coronel"),
            ]),
        ]),
        _n("gab-ma","Gabinete do CG", children=[
            _n("ajord-ma","Ajudantes-de-Ordens"),
        ]),
        _n("ag-ma","Ajudância-Geral","","Tenente-Coronel", children=[
            _n("ag-adm-ma","Seção de Administração e Expediente"),
            _n("cia-gcs","Companhia de Guarda, Comando e Serviços"),
            _n("banda-ma","Banda de Música"),
        ]),
        _n("ctrl-ma","Controladoria", children=[
            _n("ctrl-pla-ma","Seção de Planejamento e Controle", children=[
                _n("ctrl-fis","Subseção de Escrituração Fiscal e Contábil"),
                _n("ctrl-ac","Subseção de Avaliação e Controle"),
            ]),
        ]),
        _n("ouv-ma","Ouvidoria"),
        _n("coord-medica-ma","Coordenadoria Médica de Saúde","CMS","Tenente-Coronel"),
        _n("coord-odonto-ma","Coordenadoria de Serviços Odontológicos","CSO","Tenente-Coronel"),
    ]),
    _n("dir-set-ma","Diretorias", cat="Direção Setorial", children=[
        _n("dp-ma","Diretoria de Pessoal","","Coronel Combatente", children=[
            _n("drh-ma","Departamento de Recursos Humanos", children=[
                _n("drh-sr-ma","Seção de Seleção e Recrutamento"),
                _n("drh-jd-ma","Seção de Justiça e Disciplina"),
            ]),
            _n("dapr","Departamento de Assistência Psicossocial e Religiosa"),
        ]),
        _n("df-ma","Diretoria de Finanças","","Coronel Combatente", children=[
            _n("df-rfc","Departamento de Recursos Financeiros e Contábeis", children=[
                _n("df-pag","Seção de Pagamento de Pessoal"),
                _n("df-emp","Seção de Empenho"),
            ]),
            _n("df-conv","Departamento de Contratos e Convênios"),
        ]),
        _n("dep-ma","Diretoria de Ensino e Pesquisa","","Coronel Combatente", children=[
            _n("dep-te","Seção Técnica de Ensino"),
            _n("dep-ce","Seção de Cursos e Estágios"),
            _n("abm-ma","Academia de Bombeiro Militar"),
            _n("col-ma","Colégios Militares"),
        ]),
        _n("dal-ma","Diretoria de Apoio Logístico","","Coronel Combatente", children=[
            _n("dal-comp","Seção de Compras"),
            _n("csm-ma","Centro de Suprimento e Manutenção", children=[
                _n("csm-mot-ma","Seção de Manutenção de Motomecanização"),
                _n("csm-com-ma","Seção de Manutenção de Comunicações"),
            ]),
        ]),
        _n("dat-ma","Diretoria de Atividades Técnicas","","Coronel Combatente", children=[
            _n("dat-ipi","Departamento de Investigação e Prevenção de Incêndio", children=[
                _n("dat-pp","Seção de Prevenção e Perícia"),
            ]),
            _n("dat-vp","Departamento de Vistorias e Pareceres", children=[
                _n("dat-ap","Seção de Análise de Projetos"),
                _n("dat-op","Seção de Operações"),
            ]),
        ]),
        _n("di-ma","Diretoria de Inteligência","","Coronel Combatente", children=[
            _n("di-ici","Departamento de Inteligência e Contra-Inteligência"),
        ]),
        _n("dpm-ma","Diretoria de Planejamento e Modernização","","Coronel Combatente", children=[
            _n("dpm-po","Departamento de Planejamento Orçamentário", children=[
                _n("dpm-ac","Seção de Avaliação e Controle de Metas"),
                _n("dpm-gp","Seção de Gestão de Projetos"),
            ]),
            _n("dpm-ti","Departamento de Tecnologia da Informação", children=[
                _n("dpm-st","Subseção de Suporte Técnico"),
                _n("dpm-sis","Subseção de Sistemas"),
            ]),
        ]),
    ]),
    _n("exec-ma","Órgãos de Execução", cat="Execução", children=[
        _n("cmd-op-ma","Comandos Operacionais do CBM"),
        _n("bbm-ma","Batalhões de Bombeiros Militar","BBM","Tenente-Coronel"),
        _n("bbe-ma","Batalhões de Bombeiros Especializados (COECB)","COECB","Tenente-Coronel", children=[
            _n("bbmar-ma","Batalhão de Bombeiros Marítimo","BBMar","Tenente-Coronel"),
            _n("bbem-ma","Batalhão de Bombeiros de Emergências Médicas","BBEM","Tenente-Coronel"),
            _n("bbs-ma","Batalhão de Busca e Salvamento","BBS","Tenente-Coronel"),
            _n("bba-ma","Batalhão de Bombeiros Ambiental","BBA","Tenente-Coronel"),
        ]),
        _n("cibm-ma","Companhias Independentes BM","","Major"),
        _n("cia-ma","Companhias de BM","","Capitão"),
        _n("pbm-ma","Postos de Bombeiro Militar","","1º/2º Tenente"),
    ]),
],

}  # fim CURATED_ORGANS_P2
