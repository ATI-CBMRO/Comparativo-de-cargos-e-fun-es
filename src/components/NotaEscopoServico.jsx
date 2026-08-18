import { Info } from 'lucide-react'

// Nota de escopo do recorte setorizado (spec 2026-08-13). Declara na cara do documento
// o que ficou para a 2ª etapa: a análise transversal mostrou que a lacuna do recorte é
// CONCEITUAL (matéria pressuposta), não textual — a minuta tem 1 única remissão a
// "Art. N" em todo o recorte, e ela é externa. Lacuna declarada é escopo.
export default function NotaEscopoServico({
  artigosNoEscopo, artigosEmCapitulosFora, capitulosFora, artigosCortadosNoEscopo,
}) {
  return (
    <aside className="nota-escopo">
      <Info className="nota-escopo-ico" size={18} aria-hidden="true" />
      <div>
        <p className="nota-escopo-titulo">Minuta do Regulamento de Serviço — 1ª etapa</p>
        <p>
          Reúne o serviço operacional (COB), a Central de Operações e o teledespacho, o
          serviço interno e de dia, as atribuições das funções e o serviço técnico de
          segurança contra incêndio e pânico (CAT) — <strong>{artigosNoEscopo} artigos</strong>,
          sobre a Lei nº 2.204/2009, a Lei de Organização Básica vigente.
        </p>
        {capitulosFora.length > 0 && (
          <p>
            Ficam para a 2ª etapa, no Regulamento Geral completo,{' '}
            <strong>{artigosEmCapitulosFora} artigos</strong>: {capitulosFora.join('; ')}.
          </p>
        )}
        {artigosCortadosNoEscopo > 0 && (
          <p>
            No capítulo das Atribuições das Funções constam apenas as funções do Comando
            Operacional de Bombeiros e da Coordenadoria de Atividades Técnicas —{' '}
            <strong>{artigosCortadosNoEscopo} artigos</strong> das funções dos demais órgãos
            ficam para o Regulamento Geral completo.
          </p>
        )}
        <p className="nota-escopo-aviso">
          A numeração dos artigos é provisória e será refeita na consolidação final.
        </p>
      </div>
    </aside>
  )
}
