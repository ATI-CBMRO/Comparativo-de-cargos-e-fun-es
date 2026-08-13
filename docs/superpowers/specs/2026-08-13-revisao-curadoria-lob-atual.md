# Revisão da curadoria à luz da LOB vigente — Regimento e Regulamento

**Data:** 2026-08-13 · **Pedido:** Wândrio · **Cenário sob exame:** LOB ATUAL (Lei 2.204/2009)
**Motivo:** a curadoria assumiu que a LOB de RO teria sido feita sobre a LOB do Mato Grosso.
Isso vale para a LOB **futura** (em reforma), não se confirma para a **vigente**.

---

## 1. Resposta direta à premissa levantada

A preocupação estava certa no efeito e **incompleta na causa**. Vale registrar a diferença,
porque ela muda o tamanho do problema.

**Não é que a premissa "MT" contaminou o cenário atual.** É que a curadoria **nunca mapeou
estrutura organizacional** — ela só trocou **nome de estado**. A tabela `ADAPTATIONS`
(`scripts/regulamento_enrichment.py`) substitui "Mato Grosso"→"Rondônia", "CBMSE"→"CBMRO" e
similares. Ela não sabe que "Batalhão" não existe em RO, que "Diretoria de Segurança Contra
Incêndio e Pânico" é órgão do MT, ou que "CICOM" é o centro de comunicações da Bahia.

Consequência: o defeito atinge **os dois cenários**. No futuro ele fica disfarçado — a LOB em
reforma é ela própria inspirada no MT, então os nomes "encaixam". No atual ele fica escancarado.

Medição (nomes institucionais citados no recorte de Serviço, 185 artigos):

| Situação | Nomes distintos |
|---|---|
| Sem lastro em **nenhuma** das duas LOBs de RO | **32** |
| Ausentes da atual, presentes na futura (a hipótese original) | 6 |
| Presentes nas duas | 10 |
| Presentes só na atual | 5 |

Ou seja: os 6 nomes da hipótese original existem, mas são a menor parte. O grosso — 32 nomes —
não pertence a nenhuma realidade de Rondônia.

**Regimento Interno (RI):** está limpo no cenário atual — 0 vazamentos, e os órgãos que ele usa
(CAT, COB, CEPDEC, CONDEG, DINT, GBS) existem na lei vigente. O RI é construído **por órgão, a
partir de cada LOB**, e por isso não sofreu o problema. **O RI do cenário futuro tem 21 siglas de
outros estados** (CBMDF 10x, CBMMT 7x, CBM-MT 2x, CBMPA 2x) — pendência separada, não afeta a
reunião de 14/08.

---

## 2. O problema de fundo: a matéria do Regulamento não tem âncora na LOB vigente

Este é o achado mais importante e não é sobre texto — é sobre competência.

**A LOB vigente é totalmente silente sobre serviço.** Varredura no texto integral (2.925 linhas,
incluindo dispositivos revogados):

| Termo | Ocorrências na Lei 2.204/2009 |
|---|---|
| escala | 0 |
| guarnição | 0 |
| oficial de dia | 0 |
| sobreaviso | 0 |
| prontidão | 0 |
| plantão · turno · revezamento | 0 |

**E a delegação que autorizaria o Regulamento a tratar disso foi superada.** O Art. 48, nas
redações original, de 2012 e de 2014, dizia que "a estrutura básica dos Grupamentos,
Subgrupamentos, Pelotões (…) e suas denominações serão definidas no regulamento desta Lei". A Lei
4.303/2018 **reescreveu o Art. 48 inteiro**, que passou a tratar de OBM Especializadas. Restou
apenas o Art. 49, parágrafo único — e ele delega somente os **critérios** de dimensionamento de
OBM, por portaria.

O que a lei vigente reserva a cada instrumento:

- **Decreto do Governador** — estruturação, transformação, extinção, **denominação** e localização
  de órgãos (Art. 59); ativação de OBM (Art. 60); regulamentação da estrutura organizacional e
  distribuição de efetivo (Art. 64).
- **Portaria do Comandante-Geral** — critérios de criação/estrutura/subordinação das OBM
  operacionais (Art. 49, par. único); comissões (Art. 26).

**Por que isso decide tudo:** se o Regulamento sair por **Portaria**, os capítulos que criam ou
renomeiam órgão são inválidos na origem — não por erro de redação, mas por falta de competência.
Essa pergunta precisa ser respondida antes de qualquer discussão de mérito sobre o texto.

---

## 3. O que foi corrigido (3 commits, com prova)

Corrigi apenas o que é **defeito mecânico inequívoco** — identidade de estado e lixo de extração.
Não mexi em nada que dependa de decisão de mérito.

| # | Defeito | Causa-raiz | Efeito medido |
|---|---|---|---|
| `c40e850` | "CBMBA" na minuta de RO | `ADAPTATIONS` cobria 9 estados e **não cobria a Bahia** — que é fonte primária do capítulo 193, então ele saía com zero adaptações | 3 trechos/cenário → **0** |
| `f715fac` | "CBM-MT" sobrevivia | a tabela casa texto **literal**; toda variante com separador escapava ("CBM-MT", "CBM- MT") | 6 trechos/cenário → **0** |
| `2ff7ae7` | Rodapé de PDF fabricando ato normativo | extração do RISD/CBMSE embutiu o rodapé **no meio das frases**; a adaptação trocava "CBMSE"→"CBMRO" ali dentro e a minuta passava a **afirmar a existência de um "Boletim Geral nº 060, de 30/03/2022" do CBMRO** | 13 dispositivos → **0** |
| `2ff7ae7` | "PMSE" | mandava acionar a Polícia Militar **de Sergipe** numa ocorrência em Rondônia | 1 → **0** |

Exemplo do estrago do rodapé, antes e depois:

> **Antes:** "A permuta de escala do Supervisor de Dia, só será permitida mediante autorização por
> escrito `14/28 BGO Nº 060 Publicado em 30/03/2022 CBMRO/RISD – Regulamento Interno dos Serviços
> Diários.` do Diretor Operacional do CBMRO"
>
> **Depois:** "A permuta de escala do Supervisor de Dia, só será permitida mediante autorização por
> escrito do Diretor Operacional do CBMRO, após publicação em Boletim Geral Ostensivo."

**Método:** todas as correções foram feitas na **causa-raiz** (o script que gera), não no dado
gerado — assim não voltam no próximo rebuild. A limpeza do rodapé roda no **build**, e não na
transcrição, de propósito: o rodapé está mesmo no markdown de origem e
`scripts/verificar_verbatim.py` compara a transcrição com ele. Tirar da transcrição quebraria essa
conferência.

**Verificação após as correções:** `verificar_verbatim.py` OK (1166 excerpts, todos verbatim) ·
`test_regulamento_structure.py` OK (16 capítulos, 413 artigos) · `npm test` 154/154 ·
413 artigos preservados nos dois cenários · `original_caput` mantido, então o comparador continua
mostrando o texto de origem para conferência.

Backup dos JSONs antes da primeira regeneração:
`~/Backups/regulamentacao-lob/2026-08-13-antes-correcao-curadoria/`

---

## 4. O que NÃO corrigi, e por quê

Tudo abaixo exige decisão de mérito de quem conhece o CBMRO. Corrigir por conta própria seria
trocar o erro do Mato Grosso pelo meu palpite.

### 4.1 Resíduos ainda no texto (mecânicos, mas exigem a resposta certa)

| Resíduo | Onde | Qual é a resposta certa? |
|---|---|---|
| **CICOM** (12x) | capítulo 193 | Nome do centro de comunicações **da Bahia**. Em RO **não há órgão equivalente na lei**: o COCB foi **revogado** (Art. 51, pela Lei 4.303/2018) e o Art. 35 não o recriou. Qual é a central que opera o 193 hoje? |
| **Secretaria de Estado de Segurança Pública** (3x) | preliminares e competências | É a pasta do MT. Em RO é a **SESDEC** (Art. 1º, par. único) |
| **"Art. 82 da Constituição Estadual"** (1x) | `mt-art-1` | É o artigo da Constituição **do Mato Grosso**. Falta identificar o correspondente na Constituição de RO |
| **ADEMA** (1x) | `se-art-135` | Órgão ambiental **de Sergipe** |
| **sistema "e-doc"** (1x) | `se-art-111` | Sistema do CBMSE; qual o do CBMRO? |

### 4.2 O problema maior: capítulos que descrevem outra corporação

| Capítulo | Artigos | Diagnóstico |
|---|---|---|
| `atribuicoes-funcoes` | 29 art / 345 incisos | **25 dos 29 artigos com incompatibilidade.** É o Título III do Regulamento Geral do **CBMMT** — descreve DAI, DEIP, DSCIP, Diretoria Operacional, Comandos Regionais, Batalhões, Companhias, Pelotões, Escola Dom Pedro II, Centro de Capacitação Física, "Comandante-Geral Adjunto". **Nenhum existe na LOB de RO** |
| `seguranca-contra-incendio` | 19 art / 184 incisos | É o **regimento interno da DSCIP do Mato Grosso**. Em RO a matéria é da **Coordenadoria de Atividades Técnicas** (Art. 18), cuja estrutura é taxativa e **não coincide em nenhuma das 17 unidades** listadas |
| `central-operacoes-193` | 3 art / 65 incisos | Fonte Bahia, **zero adaptações**. Além do CICOM: SSP, Coordenadores de Área, Coordenadoria de Saúde, Grupo de Despacho, SGTO, remissão a "ANEXO A desta Portaria" (anexo baiano inexistente aqui) |
| `servico-operacional` + `servico-interno-dia` | 128 art | Fonte Sergipe. "Diretoria/Diretor de Operações" **20 vezes** (em RO é **Comando Operacional**, Art. 35). Escalas desenhadas para estado compacto: Superior de Dia em sobreaviso proibido de sair da área de residência **mas responsável por todo o território estadual** — inexequível em Rondônia |

Dois pontos de **hierarquia de normas**, além da estrutura:

- **"Multar"** aparece em 4 dispositivos. A palavra **não existe na LOB** — o Art. 2º prevê poder
  de polícia, embargo e interdição, não multa. Sanção pecuniária exige previsão em **lei**.
- **Art. 3 da minuta** reescreve as competências do CBMRO em 11 incisos; o **Art. 2º da LOB tem
  25**. O texto importado **suprime competências legais** (atendimento pré-hospitalar, guarda-vidas,
  perícia técnica, polícia judiciária militar, entre outras) e condiciona a convênio uma
  fiscalização que a lei dá como poder próprio.

### 4.3 Fundamento legal ausente

Em nenhum dos 185 artigos há menção à **Lei nº 2.204/2009**. Não há artigo de fundamento, não há
cláusula de vigência, não há cláusula revogatória. O documento não declara em que lei se apoia.

---

## 5. Recomendação para a reunião de 14/08

**Não apresentar o texto como "a minuta do CBMRO" para discussão artigo por artigo.** Nos capítulos
de estrutura ele descreve MT, SE e BA. Discutir mérito de dispositivo cuja premissa institucional
está errada gasta a reunião e produz decisão sobre o que não existe.

**Apresentar como o que ele é: material-base de outros estados, já organizado por tema.** É um bom
ponto de partida — 185 artigos de doutrina de serviço levantados e comparados. O que falta é o
mapeamento para a realidade de Rondônia, e esse mapeamento é justamente o que as pessoas na sala
sabem fazer.

**Ordem sugerida de trabalho na reunião:**

1. **Decidir o instrumento** (Portaria do Cmt-Geral × Decreto do Governador). Define o teto do que
   o Regulamento pode fazer. Sem isso, o resto é conversa no vazio.
2. **Fechar o mapa de órgãos** — para cada função importada, qual é o órgão correspondente na Lei
   2.204/2009. É trabalho de sala, com quem conhece a casa, e destrava tudo depois.
3. **Responder as três perguntas de fato** que travam capítulos inteiros:
   - Qual órgão opera o 193 hoje, e sob qual denominação? (o COCB foi revogado em 2018)
   - Existe lei estadual de segurança contra incêndio em RO? (é o que autoriza multa, alvará, taxa
     e credenciamento — sem ela, vários dispositivos caem)
   - Há Decreto ou Quadro de Organização detalhando a CAT? (se houver, o capítulo deve espelhá-lo,
     não competir com ele)
4. **Só então** discutir mérito de escala, guarnição e rotina — que é onde o material importado é
   genuinamente aproveitável.

**O que o ambiente do portal já entrega bem:** os comentários ficam ancorados no dispositivo, não
no número do artigo. Então tudo que for marcado amanhã sobrevive à renumeração e à reescrita dos
capítulos. A reunião pode ser usada para **marcar** sem medo de perder o trabalho.

---

## 6. Pendências abertas

- [ ] Definir instrumento de aprovação (Portaria × Decreto) — **bloqueia o resto**
- [ ] Mapear os 32 nomes de órgão sem lastro para os órgãos da Lei 2.204/2009
- [ ] Decidir a denominação da central de operações (CICOM → ?) e harmonizar os 4 nomes hoje em uso
      na minuta: "CICOM", "Centro de Operações", "CIOSP", "Centro de Operações de Bombeiros"
- [ ] Substituir "Secretaria de Estado de Segurança Pública" por SESDEC (3x)
- [ ] Identificar o artigo da Constituição de RO correspondente ao "Art. 82" do MT
- [ ] Inserir fundamento legal (Lei 2.204/2009), cláusula de vigência e cláusula revogatória
- [ ] Reconciliar o Art. 3 da minuta com os 25 incisos do Art. 2º da LOB
- [ ] Decidir sobre "multar" (só se houver lei estadual que o preveja)
- [ ] Regionalizar as escalas de Superior/Supervisor de Dia (hoje: estado inteiro)
- [ ] Limpar as 21 siglas de outros estados no **RI do cenário futuro** (não afeta 14/08)

---

### Método desta revisão

Varredura por script sobre os 4 documentos (Regulamento e RI × atual e futura) + leitura integral
dos 185 artigos do recorte de Serviço e da Lei 2.204/2009 com todas as alterações até a Lei
5.697/2023, capítulo por capítulo, cruzando cada órgão citado contra o texto da lei. Toda afirmação
deste documento tem dispositivo que a sustenta. Onde a lei é ambígua (ex.: Art. 59 delega usando
vocabulário que os Arts. 3º a 7º, revogados, definiam), isso está sinalizado como ambiguidade e não
resolvido por conta própria.
