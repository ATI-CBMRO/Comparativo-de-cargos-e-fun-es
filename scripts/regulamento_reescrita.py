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
    'organizacao-geral': {
        'mt-art-5': [
            'Coordenadoria de Articulação e Integração Comunitária',
            'Coordenadoria de Recrutamento',
            'Centro de Capacitação Física',
            'Coordenadoria de Atendimento Pré-Hospitalar',
            'Emergências Ambientais',
            # Bloco da DSCIP do MT: o capítulo de segurança contra incêndio foi reescrito
            # sobre a CAT, então a estrutura antiga não pode continuar no organograma.
            'Diretoria de Segurança Contra Incêndio e Pânico',
            'CCIP/1', 'CCIP/2', 'CCIP/3', 'CCIP/4', 'CCIP/5',
        ],
    },
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
    'ensino-instrucao': {
        'mt-art-162': ['Coordenadoria de Seleção', 'Centro de Capacitação Física'],
    },
}


# ── (b) Capítulo reescrito sobre a estrutura legal de Rondônia ───────────────────────
# Temas cujos artigos IMPORTADOS são integralmente descartados e substituídos pelos
# artigos autorais abaixo. O Bloco D (alternatives) do tema é preservado pelo builder:
# o comparador continua mostrando o texto dos outros estados lado a lado.
SUBSTITUI_INTEGRALMENTE = {'seguranca-contra-incendio'}

_LOB = 'CBMRO, Lei nº 2.204/2009'
_DEC = 'CBMRO, Decreto nº 21.425/2016'

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
}
