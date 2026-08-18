"""Camada de REESCRITA da minuta do Regulamento — o que a adaptação de termos não faz.

Até 2026-08-13 a minuta era inteiramente TEXTO IMPORTADO de outros estados, adaptado
pela tabela ADAPTATIONS (scripts/regulamento_enrichment.py), que só troca termo por
termo. Isso resolve "Batalhão"→"Grupamento", mas não resolve dois casos:

  (a) ÓRGÃO QUE NÃO EXISTE EM RONDÔNIA — renomear não adianta: o dispositivo descreve
      uma unidade que a Lei 2.204/2009 não tem (Centro de Capacitação Física, Núcleo
      Sistêmico, Coordenadoria de Articulação e Integração Comunitária, Coordenadoria de
      Atendimento Pré-Hospitalar, Coordenadoria de Recrutamento/Seleção, Grupamento de
      Emergências Ambientais, Coordenadoria de Saúde). O dispositivo tem de SAIR.

  (b) CAPÍTULO QUE DESCREVE OUTRA CORPORAÇÃO — o de segurança contra incêndio era, do
      primeiro ao último artigo, o regimento interno da DSCIP do Mato Grosso (CCIP 1 a
      CCIP 5, Tesouraria, Subseção de Protocolo, Subseção de Arrecadação e Estatística).
      Nenhuma dessas unidades existe aqui. Precisa ser REESCRITO sobre a estrutura legal
      de Rondônia — CAT → DAT → SAT.

Por que uma camada separada e não mais pares na tabela:
  - `scripts/verificar_verbatim.py` confere que todo texto IMPORTADO existe literalmente
    no markdown de origem. Ele percorre REGULAMENTO_ENRICHMENT; o que é escrito aqui não
    entra lá, então a conferência verbatim continua valendo para o que é transcrição e
    NÃO acusa falso erro no que é redação própria. As duas coisas seguem certas.
  - Artigo autoral carrega `autoral: True` e `fundamento` citando a norma de RONDÔNIA que
    o sustenta, para a tela e o .docx poderem rotular a origem.

Determinação do Ten. Tiago em 2026-08-13: "os três documentos são os documentos legais
existentes; tudo o que diverge deles deve ser ajustado" e "o dispositivo precisa sair".
Fontes: Lei nº 2.204/2009 (LOB consolidada até a Lei 5.697/2023), Decreto nº 21.425/2016
(regulamento de segurança contra incêndio e pânico, alt. Decreto 24.357/2019) e o
organograma oficial do CBMRO.

  (c) MATÉRIA QUE TEM NORMA PRÓPRIA DE RONDÔNIA MAIS AUTORITATIVA QUE O TEXTO IMPORTADO —
      o capítulo "Da Central de Operações e do Teledespacho" usava o Supervisor/Operador
      do Teledespacho (CICOM) da Bahia por falta de fonte melhor. Em 2026-08-14 o Ten.
      Tiago forneceu a minuta da NGA-CIOP-001/2026 (Norma Geral de Ação do Centro
      Integrado de Operações, SESDEC/CIOP — "Beta Consolidada, Revisão 4"), com as
      competências de Supervisores, Atendentes e Despachadores do CIOP de Rondônia. Essa
      NGA é, ela própria, um DOCUMENTO DE TRABALHO — sua Folha de Aprovação está com as
      assinaturas em branco e o texto se autodeclara "não substitui... o ato de aprovação
      da autoridade competente". Por isso o Regulamento REPRODUZ apenas as três funções
      pedidas (não replica o Volume II/III da NGA — tecnologia, continuidade operacional,
      eventos críticos etc.) e fecha com um artigo de REMISSÃO: as demais matérias que a
      NGA descreve permanecem reguladas por norma própria do órgão de competência da
      SESDEC, sem duplicá-las aqui. Determinação: "não é necessário adicionar o documento
      ao acervo legal" — a NGA fundamenta o artigo 74-76 sem entrar no acervo (ao
      contrário do Decreto 21.425/2016, que foi ingerido).
"""

# ── (a) Dispositivos que SAEM ────────────────────────────────────────────────────────
# Artigos inteiros: o órgão inexistente é o próprio sujeito do artigo.
REMOVER_ARTIGOS = {
    'competencias-direcao': {
        'mt-art-86': 'Coordenadoria de Articulação e Integração Comunitária — não existe na LOB de RO',
        'mt-art-87': 'competências do Coordenador de Articulação e Integração Comunitária — idem',
    },
    'competencias-execucao': {
        'mt-art-245': 'Coordenadoria de Atendimento Pré-Hospitalar (CAPH) — o APH é competência '
                      'legal (LOB Art. 2º, IV), mas não há órgão com esse nome; a atividade é do '
                      'Comando Operacional de Bombeiros',
    },
    'ensino-instrucao': {
        'mt-art-166': 'Coordenadoria de Recrutamento, Formação e Ensino (CEIP/1) — não existe; '
                      'recrutamento é da Coordenadoria de Pessoal (Art. 14) e o ensino da CEEI (Art. 15)',
        'mt-art-171': 'Centro de Capacitação Física (CCF) — não existe na LOB de RO',
        'mt-art-179': 'CCF — repetição literal do mt-art-171 na fonte',
        'mt-art-180': 'competências do CCF — idem',
        'mt-art-183': 'Seção Administrativa do CCF — subunidade de órgão inexistente',
        'mt-art-184': 'competências da Seção Administrativa do CCF — idem',
        'mt-art-185': 'Seção Técnica e de Desportos do CCF — idem',
        'mt-art-186': 'competências da Seção Técnica e de Desportos — 9 dos 21 incisos são do CCF',
    },
    'atribuicoes-funcoes': {
        'mt-art-181': 'Chefe do Centro de Capacitação Física — órgão inexistente',
        'mt-art-182': 'Chefe Adjunto do Centro de Capacitação Física — idem',
        'mt-art-230': 'competências do Chefe do Central Integrada de Operações (CIOP) — '
                      'Direção da CIOP, matéria já regulada pela NGA-CIOP-001/2026 (ver '
                      'cláusula de remissão em central-operacoes-193)',
        # Task 8 (2026-08-18): as funções do COB e da CAT foram reescritas sobre a LOB de
        # RO e o organograma oficial (ver ARTIGOS_PROPRIOS['atribuicoes-funcoes'] abaixo).
        # Manter, no MESMO capítulo, o texto velho de MT (outro cargo, outra corporação) e
        # o texto novo autoral seria conteúdo duplicado e contraditório — os 10 artigos de
        # MT que tratam de funções do COB (8) e da CAT (2) saem por inteiro, substituídos.
        'mt-art-238': 'Compete ao Comandante Operacional de Bombeiros (MT) — substituído '
                      'por reescrita autoral sobre a estrutura real do CBMRO',
        'mt-art-239': 'Diretor Adjunto Operacional (MT) — substituído por reescrita '
                      'autoral sobre a estrutura real do CBMRO',
        'mt-art-250': 'Comandantes Operacionais de Bombeiros, nível CRBM (MT) — '
                      'substituído por reescrita autoral sobre a estrutura real do CBMRO',
        'mt-art-251': 'Comandantes Operacionais de Bombeiros Adjuntos (MT) — substituído '
                      'por reescrita autoral sobre a estrutura real do CBMRO',
        'mt-art-255': 'Comandantes de Batalhões (MT) — substituído por reescrita autoral '
                      'sobre a estrutura real do CBMRO',
        'mt-art-256': 'Comandante Adjunto dos Batalhões (MT) — substituído por reescrita '
                      'autoral sobre a estrutura real do CBMRO',
        'mt-art-262': 'Comandantes dos Subgrupamentos de Bombeiros Militar (MT) — '
                      'substituído por reescrita autoral sobre a estrutura real do CBMRO',
        'mt-art-263': 'Comandantes de Pelotões Bombeiro Militar (MT) — substituído por '
                      'reescrita autoral sobre a estrutura real do CBMRO',
        'mt-art-200': 'Diretor de Segurança Contra Incêndio e Pânico (MT) — cargo que não '
                      'existe com esse nome na estrutura real da CAT; substituído por '
                      'reescrita autoral sobre a estrutura real do CBMRO',
        'mt-art-201': 'Diretor Adjunto de Segurança Contra Incêndio e Pânico (MT) — '
                      'substituído por reescrita autoral sobre a estrutura real do CBMRO',
    },
    # Resíduo de CIOP fora do capítulo próprio (Task 5, 2026-08-18): o capítulo
    # central-operacoes-193 já reescreve a matéria sobre a NGA-CIOP-001/2026; estes
    # artigos importados de MT têm a própria CIOP como sujeito (finalidade,
    # competências, direção) — duplicariam o que a cláusula de remissão daquele
    # capítulo já cobre. NÃO inclui mt-art-236 (competência do próprio Comando
    # Operacional de Bombeiros que só MENCIONA a CIOP como instrumento) nem os
    # artigos de servico-interno-dia (dever do comandante de guarnição de
    # comunicar-se com a CIOP) — nenhum dos dois regula a CIOP em si, então ficam.
    'competencias-apoio-assessoramento': {
        'mt-art-228': 'finalidade/atribuições da própria Central Integrada de Operações '
                      '(CIOP) — matéria da NGA-CIOP-001/2026, já regulada em '
                      'central-operacoes-193',
        'mt-art-229': 'competências da própria Central Integrada de Operações (CIOP) — idem',
        # Achado de revisão (2026-08-18): mt-art-231/232/233 são exatamente os 3 sub-ramos
        # internos da CIOP que já saíram de mt-art-219 (SAdm, SCOp, NOB) — mesmo heading
        # "Nível de Apoio (Gabinetes e COB)" de mt-art-228/229, mesmo critério de remoção
        # (organização/competência interna da CIOP, cláusula de remissão de
        # central-operacoes-193). O regex do levantamento não os pegou porque nenhum dos
        # três diz "CIOP"/"Central Integrada"/"Centro Integrado" — só a sigla ambígua "COB"
        # (aqui = Centro de Operações de Bombeiros/CIOP; não confundir com o "COB" de
        # Rondônia = Comando Operacional de Bombeiros, usado noutro heading do arquivo).
        'mt-art-231': 'competências da Seção Administrativa do COB - SAdm — subunidade '
                      'interna da CIOP (inclui, no inciso X, elaborar a NGA do COB/CIOP, '
                      'papel que a NGA-CIOP-001/2026 real de Rondônia já ocupa)',
        'mt-art-232': 'competências da Seção de Comunicações e Operações - SCOp — '
                      'subunidade interna da CIOP (triagem de chamados, despacho, '
                      'sistema 193)',
        'mt-art-233': 'competências do Núcleo de Operações de Bombeiros – NOB — '
                      'subunidade interna da CIOP',
    },
    'servico-operacional': {
        # O serviço de Despachante ao CIOP (regime de escala, regras internas) é
        # função/atribuição do próprio CIOP, regulada pela NGA-CIOP-001/2026 (Dos
        # Despachadores). A função em si sai da lista-mestra do se-art-4 (ver
        # REMOVER_INCISOS abaixo); estes dois artigos só existem para descrever o
        # regime desse serviço, então saem inteiros junto.
        'se-art-48': 'regime do serviço de Despachante ao Central Integrada de Operações '
                     '(CIOP) — função do Despachador, já regulada pela NGA-CIOP-001/2026',
        'se-art-49': 'regras internas do serviço de despachante ao Central Integrada de '
                     'Operações (CIOP) — idem',
        # Task 6 (2026-08-18): regras próprias de entrevista à imprensa importadas de
        # Sergipe — matéria que Rondônia já regula por norma própria (Resolução nº
        # 121/2022/CBM-CP). Ver ARTIGOS_PROPRIOS['servico-operacional'] abaixo.
        'se-art-113': 'regras próprias de entrevista importadas de Sergipe — matéria da '
                      'Resolução nº 121/2022/CBM-CP (Diretriz Geral de Comunicação Social), '
                      'para a qual o Regulamento agora remete',
    },
}

# Incisos avulsos: o artigo continua válido, o item é que cita o órgão inexistente.
#
# O casamento é por TEXTO, não por índice posicional. Índice quebraria em silêncio assim
# que outra remoção deslocasse a lista — foi exatamente o que aconteceu na primeira
# versão deste arquivo, e é a mesma classe da armadilha AR-03 do catálogo. O trecho
# procurado é comparado contra o dispositivo ORIGINAL (antes da adaptação de termos), por
# isso usa a grafia da FONTE: "Batalhão de Emergências Ambientais", não "Grupamento".
REMOVER_INCISOS = {
    # 'organizacao-geral' NÃO entra mais aqui: em 2026-08-13 os dois artigos importados
    # do tema (mt-art-4 e mt-art-5) foram descartados por inteiro — ver
    # SUBSTITUI_INTEGRALMENTE abaixo. Não é caso de tirar inciso: mt-art-5 tinha 47
    # incisos sobreviventes após a 2ª leva e QUASE TODOS estavam mal colocados na
    # hierarquia (ex.: Ajudância-Geral, Assessoria Legislativa e a Coordenadoria de
    # Planejamento/Orçamento/Finanças listadas como "BM/N" DENTRO do Estado-Maior-Geral,
    # quando a LOB as subordina diretamente ao Comandante-Geral ou ao Subcomandante — a
    # estrutura toda é a distribuição do CBMMT, não só os nomes).
    'competencias-direcao': {
        'mt-art-61': ['Articulação e Integração Comunitária'],
        'mt-art-96': ['Núcleo Sistêmico'],
        'mt-art-98': ['Núcleo Sistêmico'],
        'mt-art-100': ['Núcleo Sistêmico'],
        'mt-art-107': ['Núcleo Sistêmico'],
    },
    'competencias-execucao': {
        'mt-art-237': ['Coordenadoria de Atendimento Pré-Hospitalar'],
    },
    # Resíduo de CIOP fora do capítulo próprio (Task 5, 2026-08-18) — mesmo racional
    # do bloco em REMOVER_ARTIGOS: o mt-art-219 lista TODA a constituição dos órgãos
    # de apoio (Gabinetes + CIOP); só o ramo "2 -" (CIOP e sua estrutura interna:
    # Chefia, SAdm, SCOp, NOB) é matéria da própria CIOP, já regulada pela
    # NGA-CIOP-001/2026 ("organização" da CIOP, cláusula de remissão). O ramo "1 -"
    # (Gabinetes do Comandante-Geral e do Subcomandante) continua válido e fica.
    'competencias-apoio-assessoramento': {
        'mt-art-219': [
            '2 - Órgão de Apoio da Diretoria Operacional:',
            '2.1 – Centro de Operações de Bombeiros - COB:',
            '2.1.1 - Chefia do COB;',
            '2.1.1.1 - Seção Administrativa - SAdm;',
            '2.1.1.2 - Seção de Comunicações e Operações – SCOp;',
            '2.1.1.3 - Núcleos de Operações de Bombeiros – NOB.',
        ],
    },
    'ensino-instrucao': {
        'mt-art-162': ['Coordenadoria de Seleção', 'Centro de Capacitação Física'],
    },
    'servico-operacional': {
        # A figura do Supervisor de Dia não existe no CBMRO: a lista-mestra das funções do
        # serviço diário já traz Superior de Dia (inciso I) e Oficial de Dia (inciso V). Ver
        # de-para aprovado em docs/curadoria/depara-supervisor-de-dia.md. O Despachante ao
        # CIOP (Task 5, 2026-08-18) sai pelo mesmo motivo do se-art-48/49 (REMOVER_ARTIGOS):
        # é função do próprio CIOP, regulada pela NGA-CIOP-001/2026 (Dos Despachadores).
        'se-art-4': ['Supervisor de Dia', 'Despachante ao Centro de Operações'],
        # Os atendentes do CBMRO junto à CIOP são pessoal do próprio CIOP (Dos
        # Atendentes, NGA-CIOP-001/2026) — o dever de contatar a Polícia em longa
        # distância é atribuição do Atendente, não do comandante da guarnição; só o
        # inciso sai, o artigo (protocolo SAMU/CBMRO para pacientes com transtorno
        # mental) continua válido.
        'se-art-116': ['atendentes do CBMSE junto ao Centro de Operações'],
    },
}


# ── (b) Capítulo reescrito sobre a estrutura legal de Rondônia ───────────────────────
# Temas cujos artigos IMPORTADOS são integralmente descartados e substituídos pelos
# artigos autorais abaixo. O Bloco D (alternatives) do tema é preservado pelo builder:
# o comparador continua mostrando o texto dos outros estados lado a lado.
SUBSTITUI_INTEGRALMENTE = {'seguranca-contra-incendio', 'organizacao-geral', 'central-operacoes-193'}

_LOB = 'CBMRO, Lei nº 2.204/2009'
_DEC = 'CBMRO, Decreto nº 21.425/2016'
_NGA = 'NGA-CIOP-001/2026 (Norma Geral de Ação do Centro Integrado de Operações — ' \
       'SESDEC/CIOP, Beta Consolidada Revisão 4, documento de trabalho em validação ' \
       'institucional)'
_RES121 = 'CBMRO, Resolução nº 121/2022/CBM-CP (Diretriz Geral de Comunicação Social — ' \
          'D-05-BM), de 09 de dezembro de 2022'
# Princípio de substituição eventual do titular por seu Adjunto: a LOB não descreve a
# competência de nenhum "Adjunto" da estrutura, mas define esse mesmo papel para as duas
# posições de 2º escalão que ela detalha (Subcomandante-Geral e Chefe do Estado-Maior-
# Geral) — extensão do padrão da própria LOB para os demais Adjuntos, não analogia com
# outro estado (Task 8, 2026-08-18).
_SUBST_ADJUNTO = ('princípio de substituição eventual do titular extraído do Art. 12, '
                  '§ 2º (red. Lei n. 3.413/2014), e do Art. 12-A, § 2º (acrescido pela '
                  'Lei n. 3.413/2014)')

ARTIGOS_PROPRIOS = {
    'seguranca-contra-incendio': [
        {
            'heading': 'Cap. I — Do órgão responsável',
            'caput': 'A Coordenadoria de Atividades Técnicas – CAT é o órgão máximo responsável '
                     'pelo Sistema de Atividades Técnicas do Corpo de Bombeiros Militar do Estado '
                     'de Rondônia, competindo-lhe o controle e a observância dos requisitos '
                     'técnicos contra incêndio e pânico das edificações e áreas de risco no '
                     'Estado, bem como o planejamento, a normatização, a fiscalização, a análise '
                     'de projetos de edificações, a vistoria e a emissão de pareceres.',
            'dispositivos': [
                'Parágrafo único. O cargo de Coordenador de Atividades Técnicas é privativo de '
                'Oficial da ativa do último posto pertencente ao Quadro de Oficiais Combatentes '
                'do Estado de Rondônia.',
            ],
            'fundamento': 'LOB, Art. 18, caput, e Art. 19; Decreto nº 21.425/2016, Arts. 2º e 5º',
        },
        {
            'heading': 'Cap. I — Do órgão responsável',
            'caput': 'A Coordenadoria de Atividades Técnicas tem a seguinte estrutura:',
            'dispositivos': [
                'I - Coordenador;',
                'II - Adjunto;',
                'III - Seção Administrativa;',
                'IV - Seção de Estudos Técnicos;',
                'V - Seção de Planejamento, Fiscalização e Suporte Técnico;',
                'VI - Diretorias de Atividades Técnicas.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º (red. Lei nº 4.303/2018 e Lei nº 4.488/2019)',
        },
        {
            'heading': 'Cap. I — Do órgão responsável',
            'caput': 'Compete à Coordenadoria de Atividades Técnicas:',
            'dispositivos': [
                'I - estudar, planejar, analisar e elaborar as normas que disciplinam a segurança '
                'contra incêndio e pânico no Estado de Rondônia;',
                'II - regulamentar as medidas de segurança contra incêndio e pânico por intermédio '
                'de Instruções Técnicas, submetendo-as à homologação do Comandante-Geral;',
                'III - fiscalizar o cumprimento das normas de segurança contra incêndio e pânico e '
                'promover programas de educação pública sobre a matéria;',
                'IV - orientar e supervisionar tecnicamente as Diretorias de Atividades Técnicas '
                'nas suas respectivas áreas de abrangência;',
                'V - emitir respostas a consultas técnicas e pareceres técnicos referentes à '
                'segurança contra incêndio e pânico;',
                'VI - credenciar os integrantes do Sistema de Segurança Contra Incêndio e Pânico '
                'por intermédio de cursos ou estágios de capacitação e de treinamento, a fim de '
                'realizar as análises dos projetos e as vistorias das edificações e áreas de risco.',
            ],
            'fundamento': 'Decreto nº 21.425/2016, Arts. 2º, 5º, 7º e 8º',
        },
        {
            'heading': 'Cap. II — Das Seções da Coordenadoria',
            'caput': 'Compete à Seção de Estudos Técnicos:',
            'dispositivos': [
                'I - realizar os estudos técnicos que subsidiem a elaboração e a revisão das '
                'Instruções Técnicas do Corpo de Bombeiros Militar;',
                'II - analisar norma técnica ou literatura estrangeira apresentada pelo '
                'interessado, verificando sua aplicabilidade aos objetivos do Regulamento de '
                'Segurança Contra Incêndio e Pânico do Estado;',
                'III - instruir os casos que necessitem de soluções técnicas diversas das '
                'previstas em Instrução Técnica, submetendo-os à Comissão Técnica;',
                'IV - manter atualizado o acervo técnico e normativo da Coordenadoria.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, IV; Decreto nº 21.425/2016, Arts. 12 e 13',
        },
        {
            'heading': 'Cap. II — Das Seções da Coordenadoria',
            'caput': 'Compete à Seção de Planejamento, Fiscalização e Suporte Técnico:',
            'dispositivos': [
                'I - planejar e coordenar as ações de fiscalização das medidas de segurança contra '
                'incêndio e pânico nas edificações e áreas de risco;',
                'II - consolidar os dados das Diretorias de Atividades Técnicas e produzir os '
                'indicadores do Sistema de Atividades Técnicas;',
                'III - prestar suporte técnico às Diretorias e Seções de Atividades Técnicas na '
                'aplicação das Instruções Técnicas;',
                'IV - acompanhar a tramitação dos processos administrativos do Sistema de '
                'Segurança Contra Incêndio e Pânico, na forma de Instrução Técnica específica '
                'aprovada por Portaria.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, V; Decreto nº 21.425/2016, Art. 15',
        },
        {
            'heading': 'Cap. III — Das Diretorias de Atividades Técnicas',
            'caput': 'As Diretorias de Atividades Técnicas – DAT são os órgãos de execução do '
                     'Sistema de Atividades Técnicas, uma em cada Grupamento de Bombeiro Militar, '
                     'e obedecem, nas suas respectivas áreas de abrangência, às disposições legais '
                     'instituídas pela Coordenadoria de Atividades Técnicas.',
            'dispositivos': [
                'Parágrafo único. As Diretorias de Atividades Técnicas são as de Porto Velho, '
                'Ariquemes, Ji-Paraná, Cacoal, Rolim de Moura e Vilhena.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, VI; Decreto nº 21.425/2016, Art. 5º, § 1º; '
                          'organograma oficial do CBMRO',
        },
        {
            'heading': 'Cap. III — Das Diretorias de Atividades Técnicas',
            'caput': 'Cada Diretoria de Atividades Técnicas tem a seguinte estrutura:',
            'dispositivos': [
                'I - Diretor;',
                'II - Adjunto;',
                'III - Seção Administrativa;',
                'IV - Seção de Vistoria;',
                'V - Seção de Análise de Projetos;',
                'VI - Seção de Investigação e Prevenção de Incêndio;',
                'VII - Seção de Hidrantes;',
                'VIII - Seção de Atividades Técnicas.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, VI, alíneas "a" a "h" (red. Lei nº 4.488/2019)',
        },
        {
            'heading': 'Cap. IV — Das Seções das Diretorias',
            'caput': 'Compete à Seção de Vistoria:',
            'dispositivos': [
                'I - realizar as vistorias técnicas nas edificações e áreas de risco, verificando '
                'a execução das medidas de segurança contra incêndio e pânico previstas no projeto '
                'aprovado e nas Instruções Técnicas;',
                'II - expedir o Auto de Vistoria Contra Incêndio e Pânico – AVCIP e o Auto de '
                'Conformidade de Procedimento Simplificado – ACPS, este para as edificações '
                'classificadas como de risco baixo;',
                'III - realizar a vistoria de ofício, inopinada, ou mediante solicitação do '
                'proprietário, do responsável pelo uso, do responsável técnico ou da autoridade '
                'competente;',
                'IV - vistoriar obrigatoriamente as estruturas temporárias e os eventos '
                'temporários, exigindo a respectiva Anotação, Registro ou Termo de '
                'Responsabilidade Técnica;',
                'V - instruir o procedimento administrativo de cassação do AVCIP ou do ACPS quando '
                'constatada irregularidade posterior à emissão.',
            ],
            'fundamento': 'Decreto nº 21.425/2016, Arts. 7º, V, VI e VIII, e Art. 10, §§ 1º a 7º',
        },
        {
            'heading': 'Cap. IV — Das Seções das Diretorias',
            'caput': 'Compete à Seção de Análise de Projetos:',
            'dispositivos': [
                'I - analisar o Projeto de Proteção Contra Incêndio e Pânico – PPCIP, deferindo-o '
                'quando atendidas as exigências do Regulamento de Segurança Contra Incêndio e '
                'Pânico do Estado e das Instruções Técnicas;',
                'II - motivar o indeferimento do PPCIP com base na inobservância, pelo '
                'interessado, das disposições daquele Regulamento e das Instruções Técnicas;',
                'III - conferir se as medidas de segurança foram projetadas por profissional '
                'legalmente habilitado e registrado no respectivo Conselho Regional;',
                'IV - manter o resultado da análise à disposição do interessado na seção de '
                'atividades técnicas em que o processo se iniciou;',
                'V - assegurar ao interessado, mediante o pagamento da taxa, o direito a mais 2 '
                '(duas) reanálises do mesmo projeto.',
            ],
            'fundamento': 'Decreto nº 21.425/2016, Art. 7º, IV, e Art. 9º, §§ 1º a 7º',
        },
        {
            'heading': 'Cap. IV — Das Seções das Diretorias',
            'caput': 'Compete à Seção de Investigação e Prevenção de Incêndio:',
            'dispositivos': [
                'I - apurar as causas, o desenvolvimento e as consequências dos incêndios '
                'atendidos pelo CBMRO, mediante exame técnico das edificações, materiais e '
                'equipamentos, no local ou em laboratório especializado;',
                'II - produzir laudo técnico pericial das ocorrências de incêndio e explosão '
                'relacionadas com a competência da Corporação;',
                'III - subsidiar, com os resultados da investigação, o aprimoramento técnico das '
                'medidas de segurança contra incêndio e pânico e a revisão das Instruções '
                'Técnicas;',
                'IV - executar as ações de prevenção e de educação pública contra incêndio e '
                'pânico na área de abrangência da Diretoria.',
            ],
            'fundamento': 'LOB, Art. 2º, VIII e X, e Art. 18, § 1º, VI, "f"; '
                          'Decreto nº 21.425/2016, Art. 4º, XVII',
        },
        {
            'heading': 'Cap. IV — Das Seções das Diretorias',
            'caput': 'Compete à Seção de Hidrantes:',
            'dispositivos': [
                'I - elaborar estudos e projetos para a implantação e a manutenção da rede pública '
                'de hidrantes, em articulação com os órgãos e as empresas estaduais e municipais '
                'competentes;',
                'II - cadastrar, sinalizar e manter atualizado o registro dos hidrantes públicos '
                'existentes na área de abrangência da Diretoria;',
                'III - fiscalizar as condições de funcionamento e de acesso dos hidrantes '
                'públicos, comunicando as irregularidades à concessionária responsável;',
                'IV - subsidiar as guarnições com as informações de disponibilidade e vazão da '
                'rede de hidrantes.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, VI, "g"',
        },
        {
            'heading': 'Cap. V — Das Seções de Atividades Técnicas',
            'caput': 'As Seções de Atividades Técnicas – SAT executam, no âmbito do respectivo '
                     'Subgrupamento de Bombeiros Militar, as atividades de análise de projetos, '
                     'vistoria e fiscalização, sob orientação técnica da Diretoria de Atividades '
                     'Técnicas a que se vinculam.',
            'dispositivos': [
                'Parágrafo único. As Diretorias de Atividades Técnicas e as Seções de Atividades '
                'Técnicas PODERÃO ser vinculadas aos Grupamentos de Bombeiros Militar e aos '
                'Subgrupamentos de Bombeiros Militar, por ato administrativo do Comandante-Geral '
                'do CBMRO, de acordo com a necessidade do serviço e com a política de pessoal '
                'apresentada pelo órgão pertinente, com vistas a maior eficiência, emprego e '
                'atuação do efetivo.',
            ],
            'fundamento': 'LOB, Art. 18, § 2º (acrescido pela Lei nº 4.488/2019) — a vinculação é '
                          'FACULTATIVA e depende de ato do Comandante-Geral, não automática',
        },
        {
            'heading': 'Cap. VI — Do Sistema de Segurança Contra Incêndio e Pânico',
            'caput': 'O Sistema de Segurança Contra Incêndio e Pânico – SSCIP compreende o '
                     'conjunto de unidades do CBMRO que desenvolvem as atividades relacionadas à '
                     'prevenção e à proteção contra incêndio e pânico nas edificações e áreas de '
                     'risco, observado o cumprimento das exigências do Regulamento de Segurança '
                     'Contra Incêndio e Pânico do Estado e das Instruções Técnicas.',
            'dispositivos': [
                'I - habilitar seus oficiais e praças por meio de cursos de capacitação, '
                'especialização e treinamento, ministrados por profissionais legalmente '
                'habilitados;',
                'II - regulamentar as medidas de segurança contra incêndio e pânico;',
                'III - planejar ações e operações na área da segurança contra incêndio e pânico;',
                'IV - analisar projeto de proteção contra incêndio e pânico e realizar vistorias '
                'nas edificações e áreas de risco;',
                'V - fiscalizar o cumprimento do Regulamento e aplicar as sanções administrativas '
                'cabíveis;',
                'VI - cassar ou anular o AVCIP, o ACPS ou o ato de deferimento do processo, no '
                'caso de apuração de irregularidade;',
                'VII - elaborar as Instruções Técnicas sobre as medidas de segurança contra '
                'incêndio e pânico, cuja homologação, por Portaria, compete ao Comandante-Geral '
                'do CBMRO.',
            ],
            'fundamento': 'Decreto nº 21.425/2016, Arts. 6º e 7º e parágrafo único',
        },
        {
            'heading': 'Cap. VII — Das penalidades',
            'caput': 'Constatadas irregularidades em vistoria técnica ou fiscalização nas '
                     'edificações e áreas de risco, o Sistema de Segurança Contra Incêndio e '
                     'Pânico aplicará, na forma da Lei estadual nº 3.924, de 17 de outubro de '
                     '2016, e do Decreto nº 21.425, de 29 de novembro de 2016, as seguintes '
                     'penalidades:',
            'dispositivos': [
                'I - advertência escrita;',
                'II - multa;',
                'III - interdição parcial ou total;',
                'IV - embargo;',
                'V - apreensão de materiais e equipamentos;',
                'VI - cassação do AVCIP para habite-se ou funcionamento.',
                '§ 1º As sanções administrativas seguirão sequência lógica de aplicação, gradual e '
                'de caráter instrutivo antes do punitivo, salvo necessidade devidamente '
                'justificada.',
                '§ 2º A multa observará a gradação em Unidades Padrão Fiscal do Estado de '
                'Rondônia prevista na legislação de regência, e o seu produto será recolhido ao '
                'Fundo Estadual de Bombeiros – FUNESBOM.',
                '§ 3º O pagamento da multa não exime o infrator do cumprimento das exigências do '
                'Regulamento e das Instruções Técnicas, nem acarreta a cessação da interdição ou '
                'do embargo.',
            ],
            'fundamento': 'Decreto nº 21.425/2016, Arts. 34, 38 e 40, §§ 6º e 11 — a multa tem '
                          'base na Lei estadual nº 3.924/2016, e não na LOB',
        },
        {
            'heading': 'Cap. VIII — Das comissões e do direito de defesa',
            'caput': 'A Comissão Técnica – CT, formada por Oficiais e Praças Bombeiros Militares '
                     'qualificados no campo da segurança contra incêndio e pânico e presidida pelo '
                     'Oficial de maior posto, tem caráter temporário e destina-se a analisar e '
                     'emitir pareceres nos casos que exijam solução técnica ou apresentem dúvida '
                     'quanto às exigências previstas na legislação.',
            'dispositivos': [
                '§ 1º Caso o responsável pela edificação ou área de risco não concorde com as '
                'irregularidades apontadas ou com as penalidades aplicadas, poderá contestar, por '
                'escrito, no prazo de até 10 (dez) dias corridos, protocolando a contestação no '
                'órgão de Atividades Técnicas responsável pela autuação.',
                '§ 2º Até a decisão da contestação fica automaticamente suspenso o prazo '
                'estabelecido no Auto de Infração, reiniciando-se a contagem após a decisão.',
                '§ 3º A Comissão Técnica terá o prazo de até 30 (trinta) dias corridos para '
                'proferir a decisão, que será publicada no Diário Oficial do Estado.',
                '§ 4º A Comissão Técnica Especial – CTE, nomeada por Portaria do Comandante-Geral '
                'e presidida pelo Oficial responsável pelo Sistema de Atividades Técnicas, avalia '
                'a execução das normas e propõe as alterações necessárias ao Regulamento e às '
                'Instruções Técnicas.',
            ],
            'fundamento': 'Decreto nº 21.425/2016, Arts. 49 a 55',
        },
    ],

    # ── organizacao-geral (2026-08-13) ───────────────────────────────────────────────
    # Os dois artigos importados (mt-art-4 e mt-art-5) descreviam o organograma do
    # CBMMT: mt-art-4 usava os "7 níveis" (Direção Geral, Decisão Colegiada, Direção
    # Superior, Assessoramento Superior, Direção Setorial, Apoio, Execução) da redação
    # ORIGINAL de 2009 da LOB, superada; mt-art-5 listava 58 unidades em numeração
    # "1.1", "1.2"..., das quais 47 sobreviveram à 2ª leva de correção (nomes trocados),
    # mas a HIERARQUIA continuava a do MT — Ajudância-Geral, Assessoria Legislativa e a
    # Coordenadoria de Planejamento/Orçamento/Finanças apareciam como slot "BM/N" DENTRO
    # do Estado-Maior-Geral, quando a LOB as subordina diretamente ao Comandante-Geral ou
    # ao Subcomandante-Geral. Havia também órgão inventado (Secretaria das Comissões de
    # Promoções, Museu do CBM, Núcleo Bombeiro Militar — sem previsão na Lei 2.204/2009 em
    # nenhuma redação) e um bug de concordância que escapou da 2ª leva ("Batalhões", no
    # plural, não casava com a regra "Batalhão"→"Grupamento", que só cobria o singular).
    #
    # Reescrito como organograma narrativo, cruzado artigo a artigo com a redação
    # CONSOLIDADA (mais recente) de cada dispositivo da LOB e com o organograma oficial
    # fornecido pelo Ten. Tiago em 2026-08-13. A distribuição dos Grupamentos entre COB I/
    # COB II e a existência de 2 CIOP vêm do organograma; o detalhamento por MUNICÍPIO
    # (Subgrupamento a Subgrupamento) fica FORA — pertence ao Quadro de Organização (LOB
    # Art. 59, parágrafo único), não ao Regulamento por Portaria (ver decisão registrada
    # em PENDENCIAS.md: Portaria não cria/nomeia órgão, LOB Art. 59).
    'organizacao-geral': [
        {
            'heading': 'Cap. I — Dos níveis administrativos',
            'caput': 'O Corpo de Bombeiros Militar do Estado de Rondônia estrutura-se em três '
                     'níveis administrativos: Órgãos de Direção, Órgãos de Apoio e Órgãos de '
                     'Execução.',
            'dispositivos': [
                '§ 1º Os Órgãos de Direção constituem o Comando-Geral e destinam-se a efetuar a '
                'direção geral, o planejamento estratégico e a administração superior da '
                'Instituição, exercer as funções de corregedoria-geral e realizar a '
                'administração das atividades de recursos humanos, ensino, logística e gestão '
                'orçamentária e financeira, entre outras.',
                '§ 2º Os Órgãos de Apoio são os responsáveis pelo atendimento das necessidades '
                'da atividade-meio, de acordo com a legislação em vigor, os regulamentos e os '
                'demais documentos baixados pelo Comando-Geral.',
                '§ 3º Os Órgãos de Execução realizam a atividade-fim da Corporação, em '
                'obediência às determinações dos escalões superiores.',
            ],
            'fundamento': 'LOB, Art. 8º (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. II — Dos Órgãos de Direção',
            'caput': 'Os Órgãos de Direção compreendem o Comando Geral e o Estado-Maior-Geral '
                     'Bombeiro Militar, sendo o Comando Geral constituído por:',
            'dispositivos': [
                'I - Comandante-Geral;', 'II - Subcomandante-Geral;', 'III - Estado-Maior-Geral;',
                'IV - Corregedoria-Geral;', 'V - Gabinete do Comando;', 'VI - Ajudância-Geral;',
                'VII - Comissões;', 'VIII - Conselhos; e', 'IX - Assessorias.',
            ],
            'fundamento': 'LOB, Art. 9º e Art. 10 (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. II — Dos Órgãos de Direção',
            'caput': 'O Estado-Maior-Geral é dirigido por um Chefe, subordinado ao '
                     'Subcomandante-Geral, e tem a seguinte composição:',
            'dispositivos': [
                'I - Chefe;', 'II - Adjunto;', 'III - Seção Administrativa;',
                'IV - Coordenadorias e Diretorias:',
                'a) Coordenadoria de Pessoal;', 'b) Coordenadoria de Educação, Ensino e Instrução;',
                'c) Coordenadoria de Atividades Técnicas;', 'd) Diretoria de Logística;',
                'e) Diretoria de Comunicação Social; e', 'f) Diretoria de Informática.',
                '§ 1º O Chefe do Estado-Maior-Geral é o substituto eventual do '
                'Subcomandante-Geral em seus afastamentos e impedimentos.',
                '§ 2º Compete à Coordenadoria de Atividades Técnicas o disposto no capítulo '
                'próprio deste Regulamento, "Da Segurança Contra Incêndio e Pânico".',
            ],
            'fundamento': 'LOB, Art. 12-A, caput, § 2º e § 3º (red. Lei nº 4.488/2019)',
        },
        {
            'heading': 'Cap. III — Das Coordenadorias do Estado-Maior-Geral',
            'caput': 'A Coordenadoria de Pessoal é o órgão responsável pelo planejamento, '
                     'coordenação, fiscalização e controle das atividades relacionadas ao '
                     'recrutamento, à administração e à gestão de pessoal civil e militar do '
                     'CBMRO, tendo a seguinte estrutura:',
            'dispositivos': [
                'I - Coordenador;', 'II - Adjunto;', 'III - Seção Administrativa;',
                'IV - Diretoria de Gestão de Pessoas:',
                'a) Adjunto;', 'b) Seção de Pessoal Ativo;',
                'c) Seção de Pessoal Inativos e Pensionistas;',
                'd) Centro de Legislação, Controle e Análise de Processos;',
                'e) Seção de Promoção e Condecoração;', 'f) Seção de Movimentação e Pagamento; e',
                'g) Seção de Pessoal Civil.',
            ],
            'fundamento': 'LOB, Art. 14, caput e parágrafo único (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. III — Das Coordenadorias do Estado-Maior-Geral',
            'caput': 'A Coordenadoria de Educação, Ensino e Instrução é o órgão responsável por '
                     'todas as atividades de ensino, com competência para planejar, coordenar e '
                     'fiscalizar o ensino em todas as suas modalidades, a instrução e o '
                     'treinamento operacional do Corpo de Bombeiros Militar, tendo a seguinte '
                     'estrutura:',
            'dispositivos': [
                'I - Coordenador;', 'II - Adjunto;', 'III - Seção Administrativa;',
                'IV - Diretoria de Educação:',
                'a) Diretor;', 'b) Adjunto;', 'c) Seção Administrativa;', 'd) Seção de Educação;',
                'e) Seção de Atividades Sociais;', 'f) Unidades de Colégio Bombeiro Militar; e',
                'g) Centros de Educação Infantil Bombeiro Militar;',
                'V - Diretoria de Ensino e Instrução:',
                'a) Diretor;', 'b) Adjunto;', 'c) Seção Administrativa;',
                'd) Centro de Treinamento, Ensino e Instrução;',
                'e) Escola de Formação de Oficiais;', 'f) Escola de Formação de Praças; e',
                'g) Escola de Aperfeiçoamento e Especialização;',
                'VI - Diretoria de Projetos e Pesquisa:',
                'a) Diretor;', 'b) Adjunto;', 'c) Seção Administrativa;', 'd) Seção de Projetos; e',
                'e) Seção de Pesquisa.',
            ],
            'fundamento': 'LOB, Art. 15, caput e parágrafo único (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. IV — Dos órgãos subordinados diretamente ao Comandante-Geral',
            'caput': 'A Coordenadoria de Planejamento, Orçamento e Finanças, subordinada ao '
                     'Comandante-Geral, é responsável pelo planejamento, pelo apoio '
                     'administrativo, orçamentário e técnico-financeiro, bem como por executar, '
                     'acompanhar e controlar as atividades inerentes à sua responsabilidade, '
                     'tendo a seguinte estrutura:',
            'dispositivos': [
                'I - Coordenador;', 'II - Adjunto;', 'III - Seção Administrativa;',
                'IV - Diretoria de Orçamento e Finanças:',
                'a) Diretor;', 'b) Adjunto;', 'c) Seção Administrativa;', 'd) Seção de Orçamento;',
                'e) Seção de Contabilidade;', 'f) Seção de Finanças;', 'g) Seção de Compras; e',
                'h) Seção de Diárias;',
                'V - Diretoria de Planejamento:',
                'a) Diretor;', 'b) Adjunto;', 'c) Seção Administrativa; e', 'd) Seção de '
                'Planejamento;',
                'VI - Comissão Permanente de Licitações: Seção de Licitações.',
            ],
            'fundamento': 'LOB, Art. 16, caput e parágrafo único (red. Lei nº 4.488/2019)',
        },
        {
            'heading': 'Cap. IV — Dos órgãos subordinados diretamente ao Comandante-Geral',
            'caput': 'A Coordenadoria Estadual de Proteção e Defesa Civil – CEPDEC, que tem por '
                     'Coordenador-Geral o Comandante-Geral do CBMRO e por Coordenador '
                     'Estratégico-Operacional um Oficial do último posto do Quadro de '
                     'Combatentes, centraliza o Sistema Estadual de Proteção e Defesa Civil de '
                     'Rondônia – SIEPDEC, com a seguinte composição:',
            'dispositivos': [
                'I - Coordenador-Geral;', 'II - Coordenador Estratégico-Operacional;',
                'III - Adjunto;', 'IV - Seção Administrativa;', 'V - Secretaria Executiva;',
                'VI - Divisão de Apoio Administrativo e Financeiro;',
                'VII - Divisão de Operações Emergenciais; e',
                'VIII - Divisão de Minimização de Desastres.',
            ],
            'fundamento': 'LOB, Art. 17, caput e parágrafo único (red. Lei nº 5.697/2023)',
        },
        {
            'heading': 'Cap. IV — Dos órgãos subordinados diretamente ao Comandante-Geral',
            'caput': 'A Diretoria de Inteligência, subordinada ao Comandante-Geral, é '
                     'responsável por desenvolver, planejar, executar, coordenar, supervisionar '
                     'e controlar as Atividades de Inteligência, tendo a seguinte estrutura:',
            'dispositivos': [
                'I - Diretor;', 'II - Adjunto;', 'III - Seção Administrativa;',
                'IV - Sala de Situação;', 'V - Seção de Inteligência;',
                'VI - Seção de Contra-Inteligência;', 'VII - Seção de Operações de Inteligência;',
                'VIII - Seção de Documentos e Informática; e', 'IX - Seção de Controle de '
                'Armamento.',
            ],
            'fundamento': 'LOB, Art. 20, caput e parágrafo único (red. Lei nº 4.488/2019)',
        },
        {
            'heading': 'Cap. IV — Dos órgãos subordinados diretamente ao Comandante-Geral',
            'caput': 'A Diretoria de Logística, subordinada ao Chefe do Estado-Maior-Geral, é o '
                     'órgão responsável pela gestão logística da Corporação, tendo a seguinte '
                     'estrutura:',
            'dispositivos': [
                'I - Diretor;', 'II - Adjunto;', 'III - Seção Administrativa;',
                'IV - Centro de Controle de Material e Patrimônio: Seção de Controle de '
                'Material; Seção de Controle de Patrimônio;',
                'V - Centro de Suprimento e Material: Seção de Almoxarifado Geral; Seção de '
                'Aprovisionamento; e',
                'VI - Centro de Manutenção: Seção de Manutenção de Viaturas e Equipamentos '
                'Motorizados.',
            ],
            'fundamento': 'LOB, Art. 21, caput e parágrafo único (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. IV — Dos órgãos subordinados diretamente ao Comandante-Geral',
            'caput': 'A Diretoria de Comunicação Social é o órgão responsável pelo planejamento, '
                     'pela orientação, pela coordenação e pela supervisão das atividades de '
                     'comunicação social, tendo a seguinte estrutura:',
            'dispositivos': [
                'I - Diretor;', 'II - Adjunto;', 'III - Seção Administrativa;',
                'IV - Seção de Imprensa;', 'V - Seção de Relações Públicas; e',
                'VI - Seção de Comunicação Institucional.',
            ],
            'fundamento': 'LOB, Art. 22, caput e parágrafo único (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. IV — Dos órgãos subordinados diretamente ao Comandante-Geral',
            'caput': 'A Diretoria de Informática é o órgão responsável pelo planejamento, pela '
                     'orientação, pela coordenação e pela supervisão das atividades de '
                     'tecnologia da informação da Corporação, tendo a seguinte estrutura:',
            'dispositivos': [
                'I - Diretor;', 'II - Adjunto;', 'III - Seção Administrativa;',
                'IV - Centro de Capacitação;', 'V - Seção de Projetos e Desenvolvimento;',
                'VI - Seção de Suporte; e', 'VII - Seção de Redes.',
            ],
            'fundamento': 'LOB, Art. 23, caput e parágrafo único (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. V — Da Corregedoria-Geral, do Gabinete e da Ajudância-Geral',
            'caput': 'A Corregedoria-Geral, subordinada ao Subcomandante-Geral, é o órgão de '
                     'disciplina, orientação e fiscalização das atividades funcionais e da '
                     'conduta dos militares da Instituição, sendo o Corregedor-Geral Oficial da '
                     'ativa do último posto do Quadro de Oficiais Combatentes, e tem a seguinte '
                     'estrutura:',
            'dispositivos': [
                'I - Corregedor;', 'II - Adjunto;', 'III - Seção Administrativa;', 'IV - '
                'Cartório;', 'V - Núcleo de Inteligência; e', 'VI - Seção de Processo '
                'Administrativo.',
            ],
            'fundamento': 'LOB, Art. 13, caput e parágrafo único (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. V — Da Corregedoria-Geral, do Gabinete e da Ajudância-Geral',
            'caput': 'Ao Gabinete do Comandante-Geral compete a supervisão e a execução das '
                     'atividades administrativas de apoio e assessoramento direto, imediato e '
                     'pessoal do Comandante-Geral, tendo a seguinte estrutura:',
            'dispositivos': [
                'I - Chefia de Gabinete;', 'II - Secretaria;',
                'III - Assessoria de Comunicação e Imprensa; e', 'IV - Ajudância de Ordens.',
            ],
            'fundamento': 'LOB, Art. 24, caput e parágrafo único (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. V — Da Corregedoria-Geral, do Gabinete e da Ajudância-Geral',
            'caput': 'A Ajudância-Geral, subordinada ao Subcomandante-Geral, é o órgão '
                     'responsável pelo apoio aos órgãos instalados no Quartel do Comando-Geral, '
                     'pela manutenção e segurança das instalações e pelas funções '
                     'administrativas, inclusive de controle de todo o pessoal, tendo a seguinte '
                     'estrutura:',
            'dispositivos': [
                'I - Ajudante-Geral;', 'II - Adjunto;', 'III - Secretaria-Geral;',
                'IV - Companhia de Comando e Serviços;', 'V - Banda de Música; e',
                'VI - Centro de Assistência Social.',
            ],
            'fundamento': 'LOB, Art. 25, caput e parágrafo único (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. VI — Do Conselho Deliberativo de Estratégia e Gestão e das '
                       'Assessorias',
            'caput': 'O Conselho Deliberativo de Estratégia e Gestão – CONDEG é o órgão '
                     'responsável pelo estudo, pelo planejamento e pela assessoria consultiva ao '
                     'Comandante-Geral para a solução de questões institucionais e de segurança '
                     'pública da Corporação, composto por Oficiais da ativa do último posto.',
            'dispositivos': [
                '§ 1º Nas deliberações do CONDEG, os membros deverão fundamentar seus votos.',
                '§ 2º As deliberações do CONDEG serão apreciadas pelo Comandante-Geral, que '
                'poderá homologá-las total ou parcialmente ou avocar para si a decisão final, '
                'fundamentando a solução que adotar.',
            ],
            'fundamento': 'LOB, Art. 27 (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. VI — Do Conselho Deliberativo de Estratégia e Gestão e das '
                       'Assessorias',
            'caput': 'As Assessorias subordinam-se ao Comandante-Geral e são órgãos que prestam '
                     'assessoramento administrativo e técnico, responsáveis pela realização de '
                     'estudos e pareceres e pelo relacionamento com os Poderes e outros órgãos. '
                     'São assessorias permanentes:',
            'dispositivos': [
                'I - Assessoria Especial;', 'II - Assessoria Legislativa;',
                'III - Assessoria Parlamentar;', 'IV - Assessoria Previdenciária;',
                'V - Assessoria na Superintendência de Compras e Licitação – SUPEL;',
                'VI - Assessoria na Diretoria Executiva do Sistema de Pagamento – DESP; e',
                'VII - Assessoria Institucional.',
            ],
            'fundamento': 'LOB, Art. 29, caput e § 1º (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. VII — Dos Órgãos de Execução',
            'caput': 'São considerados Órgãos de Execução, incumbidos da tradução das políticas '
                     'e diretrizes do Comando-Geral e do Estado-Maior-Geral em objetivos e '
                     'metas, de coordenação, fiscalização e controle das atividades da '
                     'Corporação:',
            'dispositivos': [
                'I - Comando Operacional de Bombeiro Militar;',
                'II - Comando de Operações Aéreas de Bombeiro Militar; e',
                'III - Grupamento de Busca e Salvamento.',
            ],
            'fundamento': 'LOB, Art. 34, caput e parágrafo único (red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. VII — Dos Órgãos de Execução',
            'caput': 'O Comando Operacional de Bombeiros é o órgão responsável pela execução das '
                     'atividades-fins da Corporação e de Defesa Civil, subordinado '
                     'operacionalmente ao Subcomandante-Geral e administrativamente ao Chefe do '
                     'Estado-Maior-Geral, desdobrado em dois: o Comando Operacional de Bombeiros '
                     'I, com sede em Porto Velho, e o Comando Operacional de Bombeiros II, com '
                     'sede em Ji-Paraná.',
            'dispositivos': [
                '§ 1º Cada Comando Operacional de Bombeiros tem a seguinte estrutura: '
                'Comandante; Adjunto; Seção de Pessoal; Seção Administrativa; Seção de '
                'Informática; Seção de Correição; Seção de Planejamento Operacional e Controle '
                'de Resultados; Agência Regional de Inteligência; e Órgãos de Execução '
                'Operacional.',
                '§ 2º O apoio às atividades de operações do Comando Operacional de Bombeiros é '
                'prestado por uma Central Integrada de Operações – CIOP em cada sede, com as '
                'mesmas atribuições: a CIOP de Porto Velho atende, pelo número 193, as '
                'ocorrências da área do Comando Operacional de Bombeiros I, e a CIOP de '
                'Ji-Paraná, as ocorrências da área do Comando Operacional de Bombeiros II.',
            ],
            'fundamento': 'LOB, Art. 35, caput e parágrafo único (red. Lei nº 4.303/2018); '
                          'organograma oficial do CBMRO e confirmação do Ten. Tiago (2026-08-13)',
        },
        {
            'heading': 'Cap. VII — Dos Órgãos de Execução',
            'caput': 'O Comando de Operações Aéreas de Bombeiro Militar, subordinado '
                     'operacionalmente ao Subcomandante-Geral e administrativamente ao Chefe do '
                     'Estado-Maior-Geral, é o órgão responsável pela coordenação e pelo controle '
                     'das atividades-fins concernentes a operações aéreas da Corporação, '
                     'compreendendo o Grupamento de Operações Aéreas.',
            'dispositivos': [
                '§ 1º O Comando de Operações Aéreas tem a seguinte estrutura: Comandante; '
                'Adjunto; Seção de Pessoal; Seção Administrativa; Seção de Informática; Seção '
                'de Correição; Seção de Planejamento Operacional e Controle de Resultados; '
                'Agência Regional de Inteligência; e Órgãos de Execução Operacional.',
                '§ 2º O Grupamento de Operações Aéreas é estruturado em Esquadrões de Operações '
                'Aéreas, destacados ou não, cada um com Comando, Estado-Maior e Bateria.',
            ],
            'fundamento': 'LOB, Art. 39, caput e parágrafo único, e Art. 48, § 2º '
                          '(red. Lei nº 4.303/2018)',
        },
        {
            'heading': 'Cap. VII — Dos Órgãos de Execução',
            'caput': 'O Grupamento de Busca e Salvamento, subordinado diretamente ao Comando '
                     'Operacional de Bombeiros I, é a unidade que tem a seu cargo, dentro de sua '
                     'área de atuação operacional, as missões de resgate, busca e salvamento, '
                     'organizado em Subgrupamentos de Bombeiro Militar, destacados ou não, que '
                     'se estruturam em Seções de Busca e Salvamento.',
            'dispositivos': [],
            'fundamento': 'LOB, Art. 40 (red. Lei nº 4.488/2019) e Art. 48, § 1º '
                          '(red. Lei nº 4.303/2018); organograma oficial do CBMRO',
        },
        {
            'heading': 'Cap. VII — Dos Órgãos de Execução',
            'caput': 'As unidades operacionais terrestres do Corpo de Bombeiros Militar '
                     'classificam-se, em ordem decrescente de abrangência, em Grupamento de '
                     'Bombeiro Militar, Subgrupamento Independente de Bombeiros, Subgrupamento '
                     'de Bombeiro Militar, Seção de Comando e Serviço, Seção de Bombeiros, Grupo '
                     'de Bombeiros e Destacamento de Bombeiros, subordinadas diretamente ao '
                     'Comando Operacional de Bombeiros.',
            'dispositivos': [
                '§ 1º O CBMRO conta com 6 (seis) Grupamentos de Bombeiro Militar, organizados em '
                'Subgrupamentos de Bombeiros Militar, destacados ou não: o 1º, o 2º e o 5º '
                'Grupamento, subordinados ao Comando Operacional de Bombeiros I, e o 3º, o 4º e '
                'o 6º Grupamento, subordinados ao Comando Operacional de Bombeiros II.',
                '§ 2º A estrutura pormenorizada de cada Grupamento e de cada Subgrupamento — '
                'sede, área de circunscrição territorial e efetivo — constará do Quadro de '
                'Organização da Corporação.',
            ],
            'fundamento': 'LOB, Art. 47, caput e § 1º (red. Lei nº 4.303/2018), e Art. 59, '
                          'parágrafo único; organograma oficial do CBMRO',
        },
    ],

    # ── central-operacoes-193 (2026-08-14) ───────────────────────────────────────────
    # Os 3 artigos importados (ba-art-8, ba-art-9, ba-art-18) descreviam o Supervisor e o
    # Operador do Teledespacho do CICOM da Bahia — nome e estrutura de outra corporação,
    # com resíduos que citavam SSP, Coordenadoria de Saúde e ANEXO A inexistente aqui.
    # Substituídos pelas competências de Supervisores, Atendentes e Despachadores da
    # NGA-CIOP-001/2026 (norma própria de Rondônia, ainda em validação institucional — ver
    # nota no topo do arquivo), mais um artigo de remissão para as demais matérias que a
    # NGA regula (Direção, Coordenação de Plantão, Recepção Institucional, Apoio
    # Operacional, tecnologia, continuidade operacional, eventos críticos etc.), que NÃO
    # são reproduzidas aqui.
    'central-operacoes-193': [
        {
            'heading': 'NGA-CIOP-001/2026 — Dos Supervisores',
            'caput': 'Os Supervisores exercem a supervisão técnica e funcional das equipes e '
                     'das atividades da Central Integrada de Operações – CIOP sob sua '
                     'responsabilidade, apoiando o Coordenador de Plantão na manutenção da '
                     'qualidade, da regularidade e da eficiência dos serviços, competindo-lhes:',
            'dispositivos': [
                'I - supervisionar as equipes e os processos operacionais sob sua '
                'responsabilidade;',
                'II - orientar tecnicamente os atendentes, os despachadores, os integrantes '
                'da recepção institucional e os profissionais de apoio operacional, conforme '
                'a área de atuação;',
                'III - acompanhar os indicadores operacionais e comunicar ao Coordenador de '
                'Plantão os desvios que possam comprometer a qualidade ou a continuidade do '
                'serviço;',
                'IV - monitorar a qualidade, a consistência e a completude dos registros '
                'produzidos nos sistemas corporativos;',
                'V - comunicar imediatamente ao Coordenador de Plantão as intercorrências, as '
                'indisponibilidades, os riscos operacionais e as situações críticas '
                'identificadas;',
                'VI - apoiar a solução de ocorrências complexas, nos limites de sua '
                'competência, sem interferir nas atribuições legais dos órgãos participantes;',
                'VII - propor medidas de aperfeiçoamento dos fluxos, dos registros, das '
                'rotinas e dos procedimentos operacionais;',
                'VIII - fiscalizar o cumprimento dos protocolos, das orientações de serviço e '
                'das normas de segurança aplicáveis ao setor.',
                'Parágrafo único. Os Supervisores atuam sob coordenação do Coordenador de '
                'Plantão, mantendo comunicação permanente sobre a situação de suas equipes, a '
                'capacidade operacional, os riscos identificados e as providências adotadas; '
                'sua atuação limita-se à orientação e ao controle das atividades internas da '
                'CIOP, não abrangendo o exercício de atribuições privativas de outros órgãos '
                'ou autoridades.',
            ],
            'fundamento': f'{_NGA}, Arts. 23 a 25',
        },
        {
            'heading': 'NGA-CIOP-001/2026 — Dos Atendentes',
            'caput': 'Compete ao Atendente realizar o atendimento inicial das demandas '
                     'recebidas pelos canais oficiais da Central Integrada de Operações – '
                     'CIOP, coletando, qualificando e registrando as informações necessárias '
                     'ao adequado processamento da ocorrência, competindo-lhe ainda:',
            'dispositivos': [
                'I - atender o cidadão com urbanidade, imparcialidade, objetividade e '
                'linguagem compatível com a natureza da demanda;',
                'II - identificar, mediante coleta das informações essenciais, a natureza, o '
                'local, as pessoas envolvidas e o grau de prioridade aparente da ocorrência;',
                'III - registrar os dados de forma clara, completa, objetiva e tempestiva nos '
                'sistemas corporativos;',
                'IV - prestar as orientações iniciais previstas nos protocolos aplicáveis, sem '
                'emitir juízo técnico, jurídico ou médico fora de sua competência;',
                'V - encaminhar a ocorrência ao setor ou ao recurso competente, conforme os '
                'fluxos estabelecidos;',
                'VI - comunicar imediatamente ao Supervisor as inconsistências, as falhas de '
                'sistema, as demandas sensíveis ou as situações que possam comprometer o '
                'atendimento;',
                'VII - preservar o sigilo das informações obtidas em razão do serviço.',
            ],
            'fundamento': f'{_NGA}, Arts. 26 e 27',
        },
        {
            'heading': 'NGA-CIOP-001/2026 — Dos Despachadores',
            'caput': 'Compete ao Despachador realizar o gerenciamento operacional das '
                     'ocorrências registradas, promovendo o acionamento e o acompanhamento dos '
                     'recursos disponíveis, de acordo com os protocolos, a prioridade da '
                     'demanda e as competências dos órgãos envolvidos, competindo-lhe ainda:',
            'dispositivos': [
                'I - analisar tecnicamente as informações recebidas e complementar os '
                'registros quando necessário;',
                'II - acionar, despachar ou solicitar o emprego dos recursos operacionais '
                'compatíveis com a ocorrência, nos limites dos protocolos e das '
                'disponibilidades informadas pelos órgãos competentes;',
                'III - acompanhar a evolução das ocorrências em atendimento, mantendo '
                'atualizados os registros e as informações relevantes;',
                'IV - manter comunicação operacional com as equipes e os canais institucionais '
                'autorizados;',
                'V - informar imediatamente ao Supervisor ou ao Coordenador de Plantão as '
                'situações críticas, a indisponibilidade de recursos, os riscos de '
                'continuidade ou os fatos que exijam deliberação superior;',
                'VI - preservar a rastreabilidade dos acionamentos, das comunicações e das '
                'atualizações realizadas nos sistemas corporativos.',
            ],
            'fundamento': f'{_NGA}, Arts. 28 e 29',
        },
        {
            'heading': 'NGA-CIOP-001/2026 — Da remissão às demais matérias',
            'caput': 'As demais atribuições, competências, organização e finalidade da '
                     'Central Integrada de Operações – CIOP, inclusive quanto à Direção, à '
                     'Coordenação de Plantão, à Recepção Institucional, ao Apoio Operacional, '
                     'à tecnologia e à governança da informação, à segurança orgânica, à '
                     'continuidade operacional, à gestão de eventos críticos, ao '
                     'videomonitoramento, à proteção de dados e à capacitação e '
                     'responsabilização de seus integrantes, são reguladas por Norma Geral de '
                     'Ação própria, expedida pelo órgão de competência da Secretaria de Estado '
                     'da Segurança, Defesa e Cidadania – SESDEC.',
            'dispositivos': [],
            'fundamento': f'{_NGA}',
        },
    ],
    # ── servico-operacional (2026-08-18) ─────────────────────────────────────────────
    # O texto importado de Sergipe regulava entrevistas com regras próprias (quem concede,
    # o que é vedado, uniforme), matéria que em Rondônia já tem norma: a Resolução nº
    # 121/2022/CBM-CP aprova a Diretriz Geral de Comunicação Social (D-05-BM), fundada no
    # art. 11 da própria Lei 2.204/2009. O Regulamento remete a ela em vez de concorrer
    # com ela. O Manual de Relacionamento com a Mídia da DCS é citado como instrumento de
    # aplicação, NÃO como fundamento: não tem número de ato nem data de aprovação.
    'servico-operacional': [
        {
            'heading': 'Da prestação de informações à imprensa',
            'caput': 'A prestação de informações à imprensa e o relacionamento com os '
                     'meios de comunicação observarão a Diretriz Geral de Comunicação '
                     'Social do Corpo de Bombeiros Militar do Estado de Rondônia e as '
                     'orientações do Manual de Relacionamento com a Mídia editado pela '
                     'Diretoria de Comunicação Social, publicados no sítio oficial da '
                     'Corporação.',
            'dispositivos': [
                '§ 1º Compete à Diretoria de Comunicação Social coordenar o atendimento '
                'à imprensa, podendo a informação sobre ocorrência em curso ser prestada '
                'pelo militar que a comande, restrita aos aspectos técnicos do fato, '
                'vedada a manifestação de caráter pessoal.',
                '§ 2º As ocorrências de grande vulto ou de repercussão estadual terão o '
                'atendimento à imprensa articulado com a Diretoria de Comunicação Social '
                'e com o Superior de Dia.',
            ],
            'fundamento': f'{_RES121}; LOB, Art. 22',
        },
        # A remissão é DELIBERADAMENTE genérica (determinação do Ten. Tiago,
        # 2026-08-18): o material disponível do ATTS é slide de instrução do CHOABM,
        # sem portaria ou resolução que o adote no CBMRO. Transcrever as 4 fases
        # (Aproximação, Silêncio Inicial, Apresentação Pessoal, Início do Diálogo)
        # elevaria material didático a norma e congelaria doutrina de curso dentro do
        # Regulamento. Se surgir ato que adote o protocolo, este artigo passa a citá-lo,
        # no padrão da Resolução nº 121/2022/CBM-CP.
        {
            'heading': 'Do atendimento a tentativas de suicídio',
            'caput': 'O atendimento às ocorrências de tentativa de suicídio observará o '
                     'protocolo de Abordagem Técnica nas Tentativas de Suicídio e a '
                     'doutrina nacional correspondente, adotados pela Corporação em seus '
                     'cursos de formação, habilitação e aperfeiçoamento.',
            'dispositivos': [
                '§ 1º A abordagem será conduzida por militar habilitado no protocolo, '
                'privilegiando a técnica de aproximação e diálogo sobre a intervenção '
                'física, que se reserva às situações de risco iminente à vida.',
                '§ 2º Compete à Coordenadoria de Educação, Ensino e Instrução manter a '
                'capacitação do efetivo operacional no protocolo de que trata este artigo.',
            ],
            'fundamento': 'LOB, Art. 2º, IV e VII (socorro e salvamento), e Art. 15 '
                          '(Coordenadoria de Educação, Ensino e Instrução)',
        },
    ],

    # ── atribuicoes-funcoes (2026-08-18, Task 8) ─────────────────────────────────────
    # O capítulo trata de FUNÇÕES (a pessoa que ocupa o cargo — "Compete ao..."), nunca de
    # ÓRGÃOS (a unidade — "Compete à..."), matéria já coberta por organizacao-geral e por
    # seguranca-contra-incendio; por isso os Chefes de Seção aqui abaixo recebem
    # competência de CHEFIA (dirigir, distribuir, submeter ao superior), não a competência
    # técnica substantiva da Seção, já escrita naqueles dois capítulos.
    #
    # Cap. I cobre as 10 funções do Comando Operacional de Bombeiros, da estrutura do
    # Art. 35, parágrafo único (I a IX), somada ao Comandante/Comandante de Subgrupamento
    # do Art. 47. Cap. II cobre as 9 funções da Coordenadoria de Atividades Técnicas, da
    # estrutura do Art. 18, § 1º.
    #
    # Onde a LOB só ENUMERA o cargo sem descrever competência própria (todo Chefe de
    # Seção, todo Adjunto), a competência foi DERIVADA — nunca inventada por analogia com
    # outro estado: dos Chefes de Seção, pela finalidade da unidade já escrita em
    # organizacao-geral/seguranca-contra-incendio; dos Adjuntos, pelo princípio de
    # substituição eventual do titular que a própria LOB usa para o Subcomandante-Geral
    # (Art. 12, § 2º) e o Chefe do Estado-Maior-Geral (Art. 12-A, § 2º) — ver _SUBST_ADJUNTO
    # acima.
    #
    # Item 8 da CAT ("Chefes das Seções da Diretoria: Vistoria, Análise de Projetos,
    # Investigação e Prevenção de Incêndio, Hidrantes") virou UM artigo genérico cobrindo
    # as 4 Seções, em vez de 4 artigos repetindo a mesma competência de chefia — decisão de
    # redação da Task 8, documentada no `fundamento` do próprio artigo.
    'atribuicoes-funcoes': [
        # -- Cap. I — Comando Operacional de Bombeiros (10 funções, orgao: 'cob') --------
        {
            'heading': 'Cap. I — Das funções do Comando Operacional de Bombeiros',
            'orgao': 'cob',
            'caput': 'Compete ao Comandante Operacional de Bombeiros:',
            'dispositivos': [
                'I - comandar as atividades-fins da Corporação e de proteção e defesa civil '
                'na área de abrangência do respectivo Comando Operacional, traduzindo em '
                'objetivos e metas as políticas e diretrizes do Comando-Geral e do '
                'Estado-Maior-Geral;',
                'II - exercer o comando dos Grupamentos de Bombeiro Militar a ele '
                'subordinados e das demais unidades operacionais de sua área;',
                'III - coordenar o emprego dos meios operacionais disponíveis, determinando '
                'o deslocamento de recursos entre as unidades subordinadas conforme a '
                'natureza e a magnitude da ocorrência;',
                'IV - fiscalizar e controlar a execução das atividades operacionais na sua '
                'área, respondendo pelos resultados perante o Subcomandante-Geral;',
                'V - autorizar, por escrito, a permuta de escala do serviço de Oficial de '
                'Dia, com posterior publicação em Boletim Geral Ostensivo;',
                'VI - acionar o Superior de Dia nas ocorrências de grande vulto, na forma '
                'deste Regulamento;',
                'VII - propor ao Comando-Geral a criação, a extinção ou a alteração de '
                'unidades operacionais de sua área, para constar do Quadro de Organização '
                'da Corporação;',
                'VIII - submeter-se, no que respeita à administração, ao Chefe do '
                'Estado-Maior-Geral, e, no que respeita às operações, ao Subcomandante-Geral.',
            ],
            'fundamento': 'LOB, Art. 34, Art. 35 e Art. 47 (red. Lei nº 4.303/2018) e '
                          'Art. 59, parágrafo único; organograma oficial do CBMRO',
        },
        {
            'heading': 'Cap. I — Das funções do Comando Operacional de Bombeiros',
            'orgao': 'cob',
            'caput': 'Compete ao Adjunto do Comando Operacional de Bombeiros:',
            'dispositivos': [
                'I - auxiliar o Comandante Operacional de Bombeiros no planejamento, na '
                'coordenação e na fiscalização das atividades do Comando Operacional;',
                'II - substituir o Comandante Operacional de Bombeiros em seus impedimentos '
                'e afastamentos eventuais;',
                'III - exercer as demais atribuições que lhe forem delegadas pelo '
                'Comandante Operacional de Bombeiros.',
            ],
            'fundamento': 'LOB, Art. 35, parágrafo único, II (red. Lei nº 4.303/2018); '
                          f'{_SUBST_ADJUNTO}; organograma oficial do CBMRO',
        },
        {
            'heading': 'Cap. I — Das funções do Comando Operacional de Bombeiros',
            'orgao': 'cob',
            'caput': 'Compete ao Chefe da Seção de Pessoal:',
            'dispositivos': [
                'I - dirigir e distribuir os trabalhos da Seção de Pessoal, controlando a '
                'situação funcional, a lotação e a movimentação do efetivo do Comando '
                'Operacional de Bombeiros;',
                'II - determinar a instrução dos processos administrativos de pessoal de '
                'interesse do efetivo do Comando Operacional e das unidades a ele '
                'subordinadas;',
                'III - submeter ao Comandante Operacional de Bombeiros os assuntos de '
                'pessoal que excedam a competência da Seção.',
            ],
            'fundamento': 'LOB, Art. 35, parágrafo único, III (red. Lei nº 4.303/2018); '
                          'organograma oficial do CBMRO — competência derivada da '
                          'finalidade da Seção, sem duplicar a Coordenadoria de Pessoal do '
                          'Estado-Maior-Geral (Art. 14)',
        },
        {
            'heading': 'Cap. I — Das funções do Comando Operacional de Bombeiros',
            'orgao': 'cob',
            'caput': 'Compete ao Chefe da Seção Administrativa:',
            'dispositivos': [
                'I - dirigir e distribuir os trabalhos da Seção Administrativa, respondendo '
                'pelo expediente, pelo protocolo e pelo arquivo do Comando Operacional de '
                'Bombeiros;',
                'II - controlar o patrimônio e os materiais de consumo em uso nas '
                'instalações do Comando Operacional;',
                'III - submeter ao Comandante Operacional de Bombeiros os processos '
                'administrativos que excedam a competência da Seção.',
            ],
            'fundamento': 'LOB, Art. 35, parágrafo único, IV (red. Lei nº 4.303/2018); '
                          'organograma oficial do CBMRO — competência derivada da '
                          'finalidade da Seção',
        },
        {
            'heading': 'Cap. I — Das funções do Comando Operacional de Bombeiros',
            'orgao': 'cob',
            'caput': 'Compete ao Chefe da Seção de Informática:',
            'dispositivos': [
                'I - dirigir os trabalhos da Seção de Informática, prestando suporte '
                'técnico às unidades do Comando Operacional de Bombeiros;',
                'II - zelar pelo funcionamento dos sistemas corporativos, dos equipamentos '
                'e da rede de dados em uso no Comando Operacional;',
                'III - articular-se com a Diretoria de Informática do Estado-Maior-Geral '
                'nas matérias que exijam padronização ou suporte de nível superior.',
            ],
            'fundamento': 'LOB, Art. 35, parágrafo único, V (red. Lei nº 4.303/2018); '
                          'organograma oficial do CBMRO — competência derivada da '
                          'finalidade da Seção, sem duplicar a Diretoria de Informática do '
                          'Estado-Maior-Geral (Art. 23)',
        },
        {
            'heading': 'Cap. I — Das funções do Comando Operacional de Bombeiros',
            'orgao': 'cob',
            'caput': 'Compete ao Chefe da Seção de Correição:',
            'dispositivos': [
                'I - dirigir os trabalhos da Seção de Correição, instruindo, no âmbito do '
                'Comando Operacional de Bombeiros, os procedimentos disciplinares e '
                'correcionais que lhe forem determinados;',
                'II - acompanhar o cumprimento das normas disciplinares pelo efetivo das '
                'unidades subordinadas ao Comando Operacional;',
                'III - encaminhar à Corregedoria-Geral os casos que excedam a competência '
                'correcional do Comando Operacional de Bombeiros.',
            ],
            'fundamento': 'LOB, Art. 35, parágrafo único, VI (red. Lei nº 4.303/2018); '
                          'organograma oficial do CBMRO — competência derivada da '
                          'finalidade da Seção, sem duplicar a Corregedoria-Geral (Art. 13)',
        },
        {
            'heading': 'Cap. I — Das funções do Comando Operacional de Bombeiros',
            'orgao': 'cob',
            'caput': 'Compete ao Chefe da Seção de Planejamento Operacional e Controle de '
                     'Resultados:',
            'dispositivos': [
                'I - dirigir a elaboração do planejamento operacional do Comando '
                'Operacional de Bombeiros, desdobrando as diretrizes do Comando-Geral e do '
                'Estado-Maior-Geral;',
                'II - consolidar os indicadores e os resultados operacionais das unidades '
                'subordinadas ao Comando Operacional;',
                'III - subsidiar o Comandante Operacional de Bombeiros com informações '
                'para a tomada de decisão e a prestação de contas perante os escalões '
                'superiores.',
            ],
            'fundamento': 'LOB, Art. 35, parágrafo único, VII (red. Lei nº 4.303/2018); '
                          'organograma oficial do CBMRO — competência derivada da '
                          'finalidade da Seção',
        },
        {
            'heading': 'Cap. I — Das funções do Comando Operacional de Bombeiros',
            'orgao': 'cob',
            'caput': 'Compete ao Chefe da Agência Regional de Inteligência:',
            'dispositivos': [
                'I - dirigir a produção e a difusão do conhecimento de inteligência de '
                'interesse das atividades operacionais do Comando Operacional de '
                'Bombeiros;',
                'II - articular-se com a Diretoria de Inteligência do Comandante-Geral nas '
                'matérias que exijam padronização, sigilo ou tratamento em nível superior;',
                'III - subsidiar o Comandante Operacional de Bombeiros com informações '
                'relevantes à segurança das operações e do efetivo.',
            ],
            'fundamento': 'LOB, Art. 35, parágrafo único, VIII (red. Lei nº 4.303/2018); '
                          'organograma oficial do CBMRO — competência derivada da '
                          'finalidade da Agência, sem duplicar a Diretoria de Inteligência '
                          'do Comandante-Geral (Art. 20)',
        },
        {
            'heading': 'Cap. I — Das funções do Comando Operacional de Bombeiros',
            'orgao': 'cob',
            'caput': 'Compete ao Comandante de Grupamento de Bombeiro Militar:',
            'dispositivos': [
                'I - comandar as atividades operacionais e administrativas do Grupamento, '
                'subordinado ao Comandante Operacional de Bombeiros;',
                'II - exercer o comando dos Subgrupamentos, das Seções de Comando e '
                'Serviço, das Seções de Bombeiros, dos Grupos de Bombeiros e dos '
                'Destacamentos de Bombeiros subordinados ao Grupamento;',
                'III - fazer cumprir, na área de circunscrição do Grupamento, as '
                'diretrizes, os planos e as ordens do Comando Operacional de Bombeiros;',
                'IV - responder, perante o Comandante Operacional de Bombeiros, pelos '
                'resultados operacionais e administrativos do Grupamento.',
            ],
            'fundamento': 'LOB, Art. 47, caput, I, e § 1º (red. Lei nº 4.303/2018); '
                          'organograma oficial do CBMRO — competência de comando derivada '
                          'da subordinação hierárquica ao Comando Operacional de Bombeiros',
        },
        {
            'heading': 'Cap. I — Das funções do Comando Operacional de Bombeiros',
            'orgao': 'cob',
            'caput': 'Compete ao Comandante de Subgrupamento de Bombeiro Militar:',
            'dispositivos': [
                'I - comandar as atividades operacionais e administrativas do '
                'Subgrupamento, subordinado ao Comandante de Grupamento;',
                'II - exercer o comando das Seções de Bombeiros, dos Grupos de Bombeiros e '
                'dos Destacamentos de Bombeiros subordinados ao Subgrupamento;',
                'III - executar, na área de circunscrição do Subgrupamento, as diretrizes, '
                'os planos e as ordens do Grupamento e do Comando Operacional de '
                'Bombeiros;',
                'IV - responder, perante o Comandante de Grupamento, pelos resultados '
                'operacionais e administrativos do Subgrupamento.',
            ],
            'fundamento': 'LOB, Art. 47, caput, III, e § 1º, III (red. Lei nº 4.303/2018); '
                          'organograma oficial do CBMRO — competência de comando derivada '
                          'da subordinação hierárquica ao Grupamento',
        },

        # -- Cap. II — Coordenadoria de Atividades Técnicas (9 funções, orgao: 'cat') ----
        {
            'heading': 'Cap. II — Das funções da Coordenadoria de Atividades Técnicas',
            'orgao': 'cat',
            'caput': 'Compete ao Coordenador de Atividades Técnicas:',
            'dispositivos': [
                'I - dirigir, coordenar e fiscalizar as atividades da Coordenadoria de '
                'Atividades Técnicas e das Diretorias de Atividades Técnicas a ela '
                'subordinadas;',
                'II - submeter à homologação do Comandante-Geral as Instruções Técnicas '
                'elaboradas no âmbito da Coordenadoria;',
                'III - representar o Sistema de Atividades Técnicas perante os demais '
                'órgãos da Corporação e perante terceiros, nos assuntos de segurança '
                'contra incêndio e pânico;',
                'IV - presidir a Comissão Técnica Especial – CTE, nomeada por Portaria do '
                'Comandante-Geral, que avalia a execução das normas e propõe as '
                'alterações necessárias ao Regulamento de Segurança Contra Incêndio e '
                'Pânico do Estado e às Instruções Técnicas;',
                'V - responder, perante o Comandante-Geral, pelos resultados do Sistema de '
                'Atividades Técnicas.',
            ],
            'fundamento': 'LOB, Art. 18, caput e § 1º (red. Lei nº 4.303/2018 e Lei nº '
                          '4.488/2019); Decreto nº 21.425/2016, Art. 2º, Art. 5º, caput e '
                          '§ 1º, e Art. 55, caput',
        },
        {
            'heading': 'Cap. II — Das funções da Coordenadoria de Atividades Técnicas',
            'orgao': 'cat',
            'caput': 'Compete ao Adjunto da Coordenadoria de Atividades Técnicas:',
            'dispositivos': [
                'I - auxiliar o Coordenador de Atividades Técnicas no planejamento, na '
                'coordenação e na fiscalização das atividades da Coordenadoria;',
                'II - substituir o Coordenador de Atividades Técnicas em seus impedimentos '
                'e afastamentos eventuais;',
                'III - exercer as demais atribuições que lhe forem delegadas pelo '
                'Coordenador de Atividades Técnicas.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, II (red. Lei nº 4.303/2018); '
                          f'{_SUBST_ADJUNTO}; organograma oficial do CBMRO',
        },
        {
            'heading': 'Cap. II — Das funções da Coordenadoria de Atividades Técnicas',
            'orgao': 'cat',
            'caput': 'Compete ao Chefe da Seção Administrativa da Coordenadoria de '
                     'Atividades Técnicas:',
            'dispositivos': [
                'I - dirigir e distribuir os trabalhos da Seção Administrativa, respondendo '
                'pelo expediente, pelo protocolo e pelo arquivo da Coordenadoria de '
                'Atividades Técnicas;',
                'II - controlar o patrimônio e os materiais de consumo em uso nas '
                'instalações da Coordenadoria;',
                'III - submeter ao Coordenador de Atividades Técnicas os processos '
                'administrativos que excedam a competência da Seção.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, III (red. Lei nº 4.303/2018); organograma '
                          'oficial do CBMRO — competência derivada da finalidade da Seção',
        },
        {
            'heading': 'Cap. II — Das funções da Coordenadoria de Atividades Técnicas',
            'orgao': 'cat',
            'caput': 'Compete ao Chefe da Seção de Estudos Técnicos:',
            'dispositivos': [
                'I - dirigir e distribuir os trabalhos da Seção de Estudos Técnicos, '
                'supervisionando os estudos que subsidiam a elaboração e a revisão das '
                'Instruções Técnicas;',
                'II - subscrever, para encaminhamento ao Coordenador de Atividades '
                'Técnicas, os estudos e os pareceres técnicos produzidos pela Seção;',
                'III - zelar pelo cumprimento, pela Seção, das competências técnicas '
                'previstas no Cap. II — Das Seções da Coordenadoria, do capítulo Da '
                'Segurança Contra Incêndio e Pânico deste Regulamento.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, IV (red. Lei nº 4.303/2018); Decreto nº '
                          '21.425/2016, Art. 13 — competência de chefia da Seção, sem '
                          'duplicar a competência técnica já disciplinada em '
                          'seguranca-contra-incendio',
        },
        {
            'heading': 'Cap. II — Das funções da Coordenadoria de Atividades Técnicas',
            'orgao': 'cat',
            'caput': 'Compete ao Chefe da Seção de Planejamento, Fiscalização e Suporte '
                     'Técnico:',
            'dispositivos': [
                'I - dirigir e distribuir os trabalhos da Seção de Planejamento, '
                'Fiscalização e Suporte Técnico, coordenando as ações de fiscalização das '
                'Diretorias de Atividades Técnicas;',
                'II - acompanhar, no âmbito da Seção, o cumprimento das competências '
                'técnicas previstas no Cap. II — Das Seções da Coordenadoria, do capítulo '
                'Da Segurança Contra Incêndio e Pânico deste Regulamento;',
                'III - submeter ao Coordenador de Atividades Técnicas os processos '
                'administrativos que exijam decisão em nível superior ao da Seção.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, V (red. Lei nº 4.303/2018); organograma '
                          'oficial do CBMRO — competência de chefia da Seção, sem duplicar '
                          'a competência técnica já disciplinada em '
                          'seguranca-contra-incendio',
        },
        {
            'heading': 'Cap. II — Das funções da Coordenadoria de Atividades Técnicas',
            'orgao': 'cat',
            'caput': 'Compete ao Diretor de Atividades Técnicas:',
            'dispositivos': [
                'I - dirigir, coordenar e fiscalizar as atividades da Diretoria de '
                'Atividades Técnicas na sua área de abrangência, observadas as '
                'disposições instituídas pela Coordenadoria de Atividades Técnicas;',
                'II - responder, perante o Coordenador de Atividades Técnicas, pelos '
                'resultados do Sistema de Atividades Técnicas na sua área de abrangência;',
                'III - representar a Diretoria de Atividades Técnicas perante os demais '
                'órgãos do Grupamento de Bombeiro Militar e perante terceiros, nos '
                'assuntos de segurança contra incêndio e pânico.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, VI, "a" (red. Lei nº 4.488/2019); Decreto '
                          'nº 21.425/2016, Art. 5º, § 1º; organograma oficial do CBMRO',
        },
        {
            'heading': 'Cap. II — Das funções da Coordenadoria de Atividades Técnicas',
            'orgao': 'cat',
            'caput': 'Compete ao Adjunto da Diretoria de Atividades Técnicas:',
            'dispositivos': [
                'I - auxiliar o Diretor de Atividades Técnicas no planejamento, na '
                'coordenação e na fiscalização das atividades da Diretoria;',
                'II - substituir o Diretor de Atividades Técnicas em seus impedimentos e '
                'afastamentos eventuais;',
                'III - exercer as demais atribuições que lhe forem delegadas pelo Diretor '
                'de Atividades Técnicas.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, VI, "b" (red. Lei nº 4.488/2019); '
                          f'{_SUBST_ADJUNTO}; organograma oficial do CBMRO',
        },
        {
            'heading': 'Cap. II — Das funções da Coordenadoria de Atividades Técnicas',
            'orgao': 'cat',
            'caput': 'Compete ao Chefe de Seção da Diretoria de Atividades Técnicas — de '
                     'Vistoria, de Análise de Projetos, de Investigação e Prevenção de '
                     'Incêndio, ou de Hidrantes:',
            'dispositivos': [
                'I - dirigir e distribuir, na respectiva área técnica, os trabalhos da '
                'Seção, observadas as disposições do Regulamento de Segurança Contra '
                'Incêndio e Pânico do Estado e das Instruções Técnicas;',
                'II - subscrever, para encaminhamento ao Diretor de Atividades Técnicas, '
                'os autos, os pareceres e os demais documentos técnicos produzidos pela '
                'Seção;',
                'III - submeter ao Diretor de Atividades Técnicas os casos que exijam '
                'decisão em nível superior ao da Seção.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, VI, alíneas "d" a "g" (red. Lei nº '
                          '4.488/2019); Decreto nº 21.425/2016, Arts. 7º, 9º e 10 — '
                          'competência COMUM de chefia das quatro Seções da Diretoria '
                          '(Vistoria, Análise de Projetos, Investigação e Prevenção de '
                          'Incêndio, Hidrantes), sem duplicar a competência técnica de '
                          'cada Seção, já disciplinada em seguranca-contra-incendio; '
                          'artigo único cobrindo as quatro Seções por decisão de redação '
                          'da Task 8 (2026-08-18), em vez de repetir 4 vezes a mesma '
                          'competência de chefia',
        },
        {
            'heading': 'Cap. II — Das funções da Coordenadoria de Atividades Técnicas',
            'orgao': 'cat',
            'caput': 'Compete ao Chefe da Seção de Atividades Técnicas:',
            'dispositivos': [
                'I - dirigir, no âmbito do respectivo Subgrupamento de Bombeiro Militar, a '
                'Seção no cumprimento das competências técnicas previstas no Cap. V — Das '
                'Seções de Atividades Técnicas, do capítulo Da Segurança Contra Incêndio e '
                'Pânico deste Regulamento;',
                'II - observar, no exercício de suas atribuições, a orientação técnica da '
                'Diretoria de Atividades Técnicas a que a Seção se vincula;',
                'III - submeter à Diretoria de Atividades Técnicas os casos que exijam '
                'decisão em nível superior ao da Seção.',
            ],
            'fundamento': 'LOB, Art. 18, § 1º, VI, "h" (red. Lei nº 4.488/2019); '
                          'organograma oficial do CBMRO — competência de chefia da Seção, '
                          'sem duplicar a competência já disciplinada em '
                          'seguranca-contra-incendio, Cap. V',
        },
    ],
}

# ── (e) TAG DE ÓRGÃO NO CAPÍTULO DAS ATRIBUIÇÕES DAS FUNÇÕES ────────────────────────
# O capítulo é MISTO por decisão de escopo (Ten. Tiago, 2026-08-18): as funções de COB e
# CAT foram reescritas sobre a LOB de RO e entram no recorte do Regulamento de Serviço; as
# dos demais órgãos seguem sendo o transplante de MT e só aparecem no Regulamento Geral
# completo, até a curadoria da 2ª etapa. A tag é o que o filtro de escopo do frontend lê
# (src/lib/escopoServico.js) — artigo SEM tag não entra no recorte, de propósito.
#
# Os ids de COB/CAT do transplante de MT (mt-art-200/201/238/239/250/251/255/256/262/263)
# NÃO entram aqui: saíram por inteiro (REMOVER_ARTIGOS acima), substituídos pela redação
# autoral em ARTIGOS_PROPRIOS['atribuicoes-funcoes']. mt-art-230 (Chefe do CIOP) também
# não entra: já tinha sido removido antes desta tarefa (Task 5).
ORGAO_DO_ARTIGO = {
    'atribuicoes-funcoes': {
        'mt-art-62': 'emg', 'mt-art-63': 'emg', 'mt-art-67': 'dp',
        'mt-art-111': 'dcs', 'mt-art-123': 'cpof', 'mt-art-137': 'assessorias',
        'mt-art-144': 'cpof', 'mt-art-153': 'ajudancia',
        'mt-art-163': 'deei', 'mt-art-164': 'deei', 'mt-art-170': 'deei',
        'mt-art-190': 'deei', 'mt-art-191': 'deei',
        'mt-art-221': 'gabinete', 'mt-art-222': 'gabinete', 'mt-art-225': 'gabinete',
    },
}

# ── (d) SUBSTITUIÇÃO DE TERMO POR ARTIGO ─────────────────────────────────────────────
# Diferente da tabela ADAPTATIONS (regulamento_enrichment.py), que troca um termo em TODO
# o documento: aqui a mesma expressão vira coisas diferentes conforme o artigo, porque a
# fonte (RISD de Sergipe) tem TRÊS figuras de escala e o CBMRO tem duas. Ver o de-para
# aprovado em docs/curadoria/depara-supervisor-de-dia.md (aprovado pelo Ten. Tiago,
# 2026-08-18, sem alterações).
#
# O casamento é por TEXTO, não por índice — mesma razão de REMOVER_INCISOS (armadilha
# AR-03 do catálogo: índice posicional dessincroniza em silêncio quando a lista muda).
#
# `se-art-113` fica DE FORA de propósito: o de-para aprovado manda o artigo inteiro
# remeter à Resolução 121/2022 (matéria de mídia/imprensa) — isso é substituição
# integral, não substituição de termo. Resolvido pela Task 6 (2026-08-18) via
# REMOVER_ARTIGOS + ARTIGOS_PROPRIOS['servico-operacional'] acima — o artigo saiu por
# inteiro e "Supervisor de Dia" não aparece mais em nenhum dispositivo do documento.
SUBSTITUIR_TERMOS = {
    'servico-operacional': {
        'se-art-24': [('Supervisor de Dia', 'Oficial de Dia')],
        'se-art-32': [('Supervisor de Dia', 'Oficial de Dia')],
        'se-art-33': [('Supervisor de Dia', 'Oficial de Dia')],
        'se-art-34': [('Supervisor de Dia', 'Oficial de Dia'),
                      # O COB não tem "Seção de Recursos Humanos" — na LOB Art. 35,
                      # parágrafo único, é "Seção de Pessoal". Corrigido junto (de-para).
                      ('Seção de Recursos Humanos', 'Seção de Pessoal')],
        'se-art-35': [('Supervisor de Dia', 'Oficial de Dia')],
        'se-art-38': [('Supervisor de Dia', 'Superior de Dia'),
                      # Resíduo de extração: o título da seção seguinte ("Oficial de Dia")
                      # ficou grudado no fim do caput. Corrigido junto (de-para).
                      ('estadual. Oficial de Dia', 'estadual.')],
        # Mesmo defeito do se-art-34 (o COB não tem "Seção de Recursos Humanos" — na LOB
        # Art. 35, parágrafo único, III, é "Seção de Pessoal"), achado na conferência das
        # sugestões dos usuários no Firestore: estes 3 artigos não continham "Supervisor
        # de Dia" e por isso escaparam do levantamento original da Task 4.
        'se-art-26': [('Seção de Recursos Humanos', 'Seção de Pessoal')],
        'se-art-30': [('Seção de Recursos Humanos', 'Seção de Pessoal')],
        'se-art-37': [('Seção de Recursos Humanos', 'Seção de Pessoal')],
        # Cadeias de escalonamento (se-art-114 e se-art-116): o "Supervisor de Dia" é elo
        # intermediário numa cadeia que não existe no CBMRO. Substituída pela cadeia real
        # de acionamento (definição do Ten. Tiago, 2026-08-18): Comandante de Subgrupamento
        # → Comandante de Grupamento → Comandante Operacional de Bombeiros → Superior de
        # Dia (para ocorrência de grande vulto).
        'se-art-114': [
            ('Cmt do SOS em conjunto com o Supervisor de Dia, devendo se necessário, '
             'acionar o Superior de Dia e ou o Comando Operacional',
             'Comandante do socorro, que os submeterá, sucessivamente, ao Comandante do '
             'Subgrupamento, ao Comandante do Grupamento e ao Comandante Operacional de '
             'Bombeiros, acionando-se o Superior de Dia quando a ocorrência for de grande vulto'),
        ],
        # se-art-116 tem 3 ocorrências do termo (o resumo do de-para só cita o parágrafo
        # único). 2 dos 3 pares (inciso II e § 3º) são decisão pontual de um único agente,
        # sem escalonamento condicional no original — recebem o swap simples, mesmo padrão
        # de se-art-24/32/etc. Só o parágrafo único (casos omissos, com "devendo se
        # necessário, acionar" já no original) recebe a cadeia de escalonamento, mesmo
        # padrão de se-art-114.
        'se-art-116': [
            ('cabendo ao Supervisor a liberação da equipe para atendimento, após checagem '
             'dos dados junto ao SAMU da condição do paciente.',
             'cabendo ao Oficial de Dia a liberação da equipe para atendimento, após '
             'checagem dos dados junto ao SAMU da condição do paciente.'),
            ('deve informar ao Supervisor a situação e passar ao SAMU a obrigação de '
             'contenção e transporte.',
             'deve informar ao Oficial de Dia a situação e passar ao SAMU a obrigação de '
             'contenção e transporte.'),
            ('Cmt do SOS em conjunto com o Supervisor de Dia, devendo se necessário, '
             'acionar o Superior de Dia ou o Comandante da OB M e/ou o Comandante '
             'Operacional de Bombeiros',
             'Comandante do socorro, que os submeterá, sucessivamente, ao Comandante do '
             'Subgrupamento, ao Comandante do Grupamento e ao Comandante Operacional de '
             'Bombeiros, acionando-se o Superior de Dia quando a ocorrência for de grande vulto'),
        ],
        'se-art-132': [('Supervisor de Dia', 'Oficial de Dia')],
        'se-art-145': [('Supervisor de Dia', 'Oficial de Dia')],
    },
}
