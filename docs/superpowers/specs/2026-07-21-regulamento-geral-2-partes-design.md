# Regulamento Geral do CBMRO em 2 Partes (Geral × Serviço) — Design

**Data:** 2026-07-21
**Autor:** Wândrio + Claude
**Status:** spec para revisão (pré-implementação)
**Notas de curadoria (vault):** `Comparativo RISG × Regulamentos — Round 1 (hipótese)` e
`Round 2 (verificado na fonte)` em `Codebases/Comparativo-de-cargos-e-funcoes/`.

## 1. Problema e objetivo

O portal já gera uma minuta do **Regulamento** do CBMRO de forma **temática** (15 temas /
410 artigos, curados de 9 estados, esqueleto MT). Falta ao documento uma organização que
separe, com clareza, a matéria **institucional/geral** da matéria **de serviço/operacional**
— separação que existe na tradição do RISG (Regulamento Interno e dos Serviços Gerais R-1 do
Exército) e nos regulamentos estaduais, mas hoje fica implícita.

**Objetivo:** transformar o Regulamento num **documento único chamado "Regulamento Geral do
CBMRO", dividido em duas Partes** — Parte I (Geral/institucional) e Parte II (de
Serviço/operacional) — **enriquecendo** (não refazendo) a base atual, com leitura integral
dos documentos-fonte e curadoria apoiada no Obsidian.

**Não-objetivos (YAGNI):**
- Não criar trilha/rota nova: evolui a trilha `/regulamento` existente.
- Não refazer os 410 artigos já validados: novidade entra **ao lado**. (não é regra, se necessário, pode ser feito com cautela)
- Não tocar no Regimento Interno (RI por órgão) nem no cenário LOB atual/futura além do
  necessário para o campo `parte`.
- Não incorporar matéria de caserna do Exército sem correspondência no CBM (ex.: dependências
  físicas do quartel — rancho, cavalariças).

## 2. Decisões já validadas pelo Wândrio (brainstorming 2026-07-21)

1. Forma final: **1 documento, 2 Partes** (Parte I — Geral; Parte II — de Serviço).
2. A leitura integral **enriquece** a base atual (mantém os 15 temas / 410 artigos validados).
3. O **RISG** é referência: dá a **forma/espinha** e cobre Parte I + serviço de **caserna**;
   o serviço de **emergência bombeiro** vem dos RISD estaduais e dos documentos novos.
4. Identidade: o documento é o **"Regulamento Geral"** com 2 Partes (não dois documentos
   separados; não é "só o RISD").
5. **+1 tema novo**: `central-operacoes-193` (Central de Operações / teledespacho). Os demais
   candidatos (gestão de escala/afastamentos, gestão documental, grade de acionamento) **não**
   viram tema próprio — dobram-se em temas existentes.
6. Os 3 temas anfíbios (disciplina-correição, uniformes-apresentação, segurança-contra-incêndio)
   ficam **na Parte I (Geral)**.
7. Curadoria usa o **Obsidian** como camada de conexões desde já.

## 3. Repartição dos 16 temas nas 2 Partes

**Parte I — Geral (12 temas):**
`disposicoes-preliminares`, `organizacao-geral`, `competencias-direcao`, `competencias-apoio`,
`competencias-execucao`, `pessoal-quadros`, `ensino-instrucao`, `cerimonial-honras`,
`disciplina-correicao`, `uniformes-apresentacao`, `seguranca-contra-incendio`,
`disposicoes-finais`.

**Parte II — de Serviço (4 temas):**
`servico-operacional`, `servico-interno-dia`, `atribuicoes-funcoes`, `central-operacoes-193` 🆕.

Regra de mapeamento (verificada na fonte): a fronteira Geral/Serviço corta **por
capítulo/matéria**, não por documento nem por Título. Um documento-fonte pode contribuir
para as duas Partes (ex.: RS-RI: Cap. I–V Geral, Cap. VI Serviço).

## 4. Esqueletos e fontes por Parte (verificados no round 2)

| Parte | Esqueleto (primária) | Reforços verbatim verificados |
|---|---|---|
| I — Geral | **MT** (Regulamento Geral CBMMT — mais granular; premissa RO↔MT) | BA (competências ultra-granulares + ativação/desativação de unidades), DF (quadros de pessoal + execução saúde/aviação), PA (execução especializada), RN (validador enxuto/moderno 2021), PR (raso) |
| II — Serviço | **SE-RISD + GO** (Regimento dos Serviços) | RS (Cap. VI: boletins, escalas, formaturas, cerimonial, uniformes), **BA/RR/TO** (Regulamentos/Normas de Serviço novos), **9 das 17 normas de AL**, ES cirúrgico (prontidão/SOS/CERD/vistorias) |

RISG: régua de forma para as duas Partes; fonte de serviço de **caserna** (guarda, sentinela,
escala, parada, revista). O serviço de **emergência** (incêndio/resgate/193) NÃO vem do RISG.

Classificação por arquivo das 17 normas de AL (conteúdo, não o tipo no acervo):
- **Serviço (Parte II):** DOB 05, 06, 07, 08; NO 03, 04, 06, 07, 11.
- **Geral (Parte I):** DOB 01, 03; NO 01, 02; DOB 04; NO 05, 08, 09.

## 5. Arquitetura da solução

### 5.1 Camada de dados (Python, offline)
- **Campo novo `parte`** em cada capítulo/tema do `regulamento_structure.json`
  (`"parte": "geral" | "servico"`), definido por um mapa `TEMA_PARTE` no
  `build_regulamento_structure.py`. Sem coleção nova, sem migração — mesma filosofia dos
  marcadores `reg:`/`atual:` já usados.
- **16º tema** `central-operacoes-193` adicionado à lista de temas (THEMES) e ao gerador.
- **Enriquecimento verbatim**: os `regulamento_enrichment_<uf>.py` ganham as novas fontes
  (BA, RR, TO, AL, e o que faltava de SE/GO/RS/ES). Extração determinística mantém o padrão
  `extrair_regulamentos.py` (corte por "Art. N") + verificação verbatim
  (`verificar_verbatim.py`). Fontes com ruído de layout (BA, TO) usam `strip_lines` no CONFIG.
- **Espelho no cenário atual**: `build_regulamento_structure_atual.py` continua re-carimbando
  os ids do arquivo da futura; herda o campo `parte` automaticamente.

### 5.2 Leitura integral → verbatim (execução por subagentes)
Cada documento-fonte é lido **na íntegra** por um subagente que extrai, por artigo:
`{ caput verbatim, tema, parte, fonte, match }`. O resultado alimenta os
`*_enrichment.py`. Isolamento: um documento por agente; nada de `ro.json` é tocado.
Todo caput deve existir literalmente na fonte (verificação verbatim).

### 5.3 Camada de curadoria (Obsidian)
- Cada **tema** e cada **artigo curado** vira nota no vault
  (`Codebases/Comparativo-de-cargos-e-funcoes/`), com backlinks entre os estados que tratam
  do mesmo assunto.
- `obsidian-second-brain` faz aflorar contradições (redações divergentes para a mesma
  matéria) e lacunas (tema com poucos estados). O vault é o **cérebro da curadoria**; o
  repositório guarda o resultado determinístico (JSON + `.docx`).
- Regra: o vault ORIENTA a curadoria; a fonte da verdade dos dados continua nos scripts/JSON.

### 5.4 Frontend (React)
- `RegulamentoWizard` renderiza **cabeçalhos "PARTE I — GERAL" e "PARTE II — DE SERVIÇO"**,
  agrupando os temas conforme o campo `parte`. Numeração de artigos contínua no documento
  inteiro (mantém `buildArticles`).
- O `.docx` client-side (lib `docx`) sai com as duas Partes e índice único.
- Subsídio (`/regulamento/subsidio`), Diagramas e Revisão herdam a divisão por Parte.
- **Preservação:** a divisão entra AO LADO; nenhuma tela/artigo já validado é substituído.
  O diff deve provar que os 410 artigos existentes permanecem.

## 6. Fluxo de dados (resumo)

```
PDFs (LEGISLAÇÃO CBMS/) → markdown → [subagentes: leitura integral → artigo/tema/parte verbatim]
  → regulamento_enrichment_<uf>.py → build_regulamento_structure.py (campo `parte` + 16º tema)
  → regulamento_structure.json → RegulamentoWizard (2 Partes) → .docx
        (em paralelo) curadoria/conexões no Obsidian (backlinks, contradições, lacunas)
```

## 7. Tratamento de erros e casos-limite
- **Verbatim quebrado**: se um caput não existe literalmente na fonte, o artigo é rejeitado
  (não entra) e reportado — nunca ajustado em silêncio.
- **Ruído de OCR/layout** (BA, TO): `strip_lines` no CONFIG antes do parse.
- **Matéria sem tema**: se a leitura achar matéria nova fora dos 16 temas, ela é SINALIZADA
  para decisão humana — não é forçada num tema errado.
- **Tema anfíbio por artigo**: se um artigo específico contraria o `parte` do seu tema, marca-se
  como exceção explícita (curadoria), não se move o tema inteiro.

## 8. Testes
- `test_regulamento_structure.py` estendido: todo capítulo tem `parte` válida; o 16º tema
  existe; contagem de artigos por Parte; os 410 artigos antigos permanecem.
- Verificação verbatim de todos os caputs das novas fontes.
- Preservação: snapshot dos artigos existentes antes/depois (diff = só acréscimos).

## 9. Escopo quantificado (lei)
- Temas: 15 → **16**.
- Partes: 1 sequência → **2 Partes** rotuladas.
- Fontes lidas na íntegra nesta rodada: RISG + SE, GO, RS, BA, RR, TO, AL(17), MT, RN, DF, PA, PR, ES.
- Artigos preservados: **410** (base atual), + novos verbatim das fontes acima.

## 10. Riscos
- **Volume de leitura** (milhares de páginas): mitigado por subagentes (1 doc/agente).
- **Parte II sub-coberta em emergência**: os RISD estaduais + docs novos são a única fonte;
  se insuficiente, sinalizar lacuna (não inventar).
- **Deriva de escopo**: manter YAGNI — só o 16º tema; demais matérias novas dobram-se em
  temas existentes ou viram pendência sinalizada.
