# Frente A — Resíduos do Regulamento: TO corpo principal, DOBs de AL, NO-02, OCR do PI

**Data:** 2026-07-22 · **Status:** aprovado (brainstorming com o Wândrio)

## Objetivo

Fechar os 3 buracos sinalizados da base do Regulamento (e 1 do acervo) para que TODO o
material de referência esteja na base verificada — e, por consequência, no vault Obsidian.

## Escopo

1. **Tocantins — corpo principal** (Diretriz Geral, Art. 1-13 e 16): entra na base como
   reforço dos temas de serviço. Técnica: corte por LINHA ABSOLUTA do markdown (mesma
   técnica validada no ES quando a numeração se repete), isolando corpo principal do
   Anexo 2 (já usado). Sem tocar nos excertos existentes do Anexo 2.
2. **Alagoas — DOBs/Normas 05-08** (sem "Art. N"; estrutura "1 FINALIDADE / 2 APLICAÇÃO…"):
   novo modo de extração POR SEÇÃO NUMERADA. Citação `cf.` referencia a seção (ex.:
   `cf. CBMAL, DOB nº 05, seção 4`). Entram como novas pseudo-fontes `al_dob05..al_dob08`
   nos temas onde o conteúdo couber (classificação por leitura, não por nome).
3. **AL NO-02** (.md de 1,6KB): conferir contra o PDF; se a conversão falhou, reconverter;
   se a norma é curta mesmo, registrar e seguir.
4. **Piauí — LOB** (PDF escaneado, .md de 604 bytes): passar OCR (ex.: `ocrmypdf` em venv
   isolado ou tesseract) e reconverter para markdown legível. NÃO entra no Regulamento
   (é LOB — alimenta acervo/comparativos); o objetivo é o acervo deixar de ter estado cego.

## Regras (herdadas do projeto)

- Verbatim absoluto: extração determinística; `verificar_verbatim.py` deve passar para todo
  excerto novo; defeitos de fonte reproduzidos, nunca limpos.
- Fontes novas entram SÓ como alternativas — nenhuma troca de fonte primária; os 413
  artigos primários não mudam (nem numeração, nem texto).
- `build_regulamento_structure.py` regenerado; `test_regulamento_structure.py` e a suíte
  `node --test` seguem passando. O cenário atual herda via seu gerador (re-carimbo de ids).
- Vault: atualizar as notas de fonte/temas afetados + criar `Fonte — DOB-0X-AL.md` (4) e
  atualizar `Fonte — Diretriz-TO.md`; se o material novo criar divergência REAL nova,
  criar a nota de decisão correspondente (mesmo formato).
- Python: usar `.venv-pipeline/bin/python`; nada instalado no sistema sem venv.

## Aceite

- Corpo principal de TO e 4 DOBs de AL presentes em `regulamento_structure.json` como
  alternativas, verbatim verificado; PI com .md legível (>20KB típico de LOB); NO-02
  esclarecida; vault sincronizado; pendências e Diário atualizados.
