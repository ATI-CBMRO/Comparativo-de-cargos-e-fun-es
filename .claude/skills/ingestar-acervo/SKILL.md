---
name: ingestar-acervo
description: "Use ao adicionar ou atualizar documentos de legislação no Acervo Legal do portal CBM (novos PDFs em 'LEGISLAÇÃO CBMS/', atualizar acervo, reclassificar tipo de documento). Leva o documento à camada 1 (acervo) e carimba seu destino nas minutas (RI/Regulamento). NÃO faz curadoria verbatim das camadas 2/3."
---

# Ingestão de documento ao Acervo Legal (camada 1)

Processo padrão para receber, curar e adicionar novos documentos legais ao acervo do
portal. Leva cada documento até aparecer na tabela de cobertura, com tipo classificado e
verificado, e registra seu destino downstream (minuta de RI, minuta de Regulamento ou
referência) sem executar a curadoria cara das camadas 2/3.

Crie um todo por passo e execute na ordem. Os passos 1 e 3 usam o helper de triagem:
`python scripts/triagem_acervo.py "<pasta>"` (a partir da pasta desta skill), que é
READ-ONLY (não renomeia, move, nem edita nada).

## Passo 0 — Congelar o batch
A pasta de staging dentro de `LEGISLAÇÃO CBMS/` sincroniza ao vivo pelo OneDrive (nome e
conteúdo podem mudar durante o trabalho). Liste os PDFs com tamanho, copie para um local
estável fora do staging e confirme o conjunto ANTES de processar. Nunca assuma o conjunto.

## Passo 1 — Normalizar nomenclatura
Rode o helper de triagem sobre a pasta congelada. Para cada arquivo, garanta o nome
`<Estado por extenso> - <Descrição>.pdf`, com o prefixo (texto antes de " - ") batendo
EXATAMENTE uma chave de `STATE_META` em `scripts/build_states_data.py` (acentos e caixa
incluídos) — é assim que o build deriva o estado. Corrija acento/caixa se o helper acusar
divergência. Mova o arquivo normalizado para a RAIZ de `LEGISLAÇÃO CBMS/` (o
`convert_to_markdown.py` só varre o topo, não subpastas).

## Passo 2 — Converter
`python scripts/convert_to_markdown.py` (na raiz do repo).

## Passo 3 — Gate de qualidade da extração
Leia o score do helper. Se `RUIM` (PDF escaneado sem OCR ou fonte por glifos `/U00XX`):
PARE e decida — buscar fonte com OCR, ou registrar "no acervo, extração pendente de OCR"
com `typeVerified` falso. Não prossiga no automático para documentos `RUIM`.

## Passo 4 — Classificar por CONTEÚDO
Leia ementa/primeiros artigos e escolha o tipo canônico entre: `Lei de Organização
Básica`, `Regimento Interno`, `Regimento de Serviços`, `Regulamento Geral`, `Normas Gerais
de Ação`, `Quadro Demonstrativo de Cargos`, `Quadro de Organização e Distribuição`.
Compare com `parse_doc_type(nome)`:
- Coincide → adicione o `.md` a `CONTENT_VERIFIED_FILES` (selo ✓).
- Diverge → adicione/ajuste `CONTENT_TYPE_OVERRIDES[<arquivo.md>] = <tipo correto>` e
  marque verificado.
- Arquivo renomeado → REMOVA a chave de override antiga e crie a nova; apague o `.md`
  antigo em `database/markdown/`.

## Passo 5 — Rebuild completo (ordem importa)
```
python scripts/convert_to_markdown.py
python scripts/build_organs_detail.py
python scripts/build_states_data.py
python scripts/build_dpo_cot_comparison.py
python scripts/build_minuta_comparison.py
python scripts/build_minuta_structure.py
python scripts/build_regulamento_structure.py
```

## Passo 6 — Verificar (evidência antes de afirmar)
Diff de `database/states_data.json`: o documento aparece no estado + tipo certos,
`typeVerified` correto, contadores e célula da tabela de cobertura atualizados. Rode
`npm test` (lógica de `acervoCoverage` etc.). Opcional: `npm run dev` e conferir a página
Acervo em http://localhost:5173/legislacoes.

## Passo 7 — Handoff para camadas 2/3
Registre em `.claude/PENDENCIAS.md`, por documento, se é candidato à camada de comparação
e/ou à minuta, e QUAL minuta, pelo mapa:

| Tipo | Alimenta | Script downstream |
|---|---|---|
| Regimento Interno (organizacional) | Minuta de RI | ri_alternativas_enrichment.py, minuta_enrichment.py |
| Regulamento Geral ou Regimento de Serviços | Minuta de Regulamento | regulamento_enrichment_<uf>.py |
| Lei de Organização Básica | camada LOB | lob_enrichment.py |
| Quadro / Normas Gerais de Ação | referência (não alimenta minuta) | — |
| RI de diretoria ou extração RUIM | só acervo, sinalizado | — |

## Passo 8 — Limpeza + registro
Remova os arquivos processados do staging, atualize a contagem do acervo no CLAUDE.md se
mudou e proponha commit (só commite se o usuário pedir).
