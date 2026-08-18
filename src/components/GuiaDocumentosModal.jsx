import { useEffect, useState } from 'react'
import { X, Search } from 'lucide-react'
import { useAuth } from '../lib/auth.jsx'

const VISTO_KEY = 'guiaDocumentosVisto'

// Popup de orientação (spec 2026-08-18): explica a diferença entre LOB, Regimento
// Interno e Regulamento de Serviço a quem acessa o portal. Some para o administrador
// (que já conhece o sistema) e, para o participante, aparece uma vez só — a marca fica
// no localStorage por e-mail, não expira ao trocar de aba/rota.
//
// Paleta e layout replicam de propósito o protótipo "G" aprovado para a apresentação de
// 18/08 (pergaminho/vermelho-tijolo/azul/verde) — fidelidade pedida explicitamente pelo
// Wândrio, mesmo destoando da identidade visual do resto do portal (vermelho/navy/branco).
export default function GuiaDocumentosModal() {
  const { user } = useAuth()
  const [aberto, setAberto] = useState(false)

  useEffect(() => {
    if (!user || user.role === 'admin') return
    const visto = localStorage.getItem(`${VISTO_KEY}:${user.email}`)
    if (!visto) setAberto(true)
  }, [user])

  if (!aberto) return null

  function fechar() {
    localStorage.setItem(`${VISTO_KEY}:${user.email}`, '1')
    setAberto(false)
  }

  return (
    <div className="gdoc-overlay" role="dialog" aria-modal="true" aria-label="Diferença entre LOB, Regimento Interno e Regulamento de Serviço">
      <div className="gdoc-modal">
        <button type="button" className="gdoc-close" onClick={fechar} aria-label="Fechar">
          <X size={18} />
        </button>
        <div className="gdoc-head">
          <span className="gdoc-eyebrow">Ficha de cada documento</span>
          <h2>A pergunta que cada documento responde — em formato de ficha.</h2>
          <p>A mesma lógica de dossiê, com a pergunta em destaque, a explicação completa — e a ficha que está sob a lupa da comissão hoje.</p>
        </div>
        <div className="gdoc-cards">
          <div className="gdoc-card" data-k="lob">
            <div className="gdoc-tab" />
            <div className="gdoc-stamp">documento fundador</div>
            <div className="gdoc-card-head">
              <div className="gdoc-doc-eyebrow">Ficha 01</div>
              <h3>LOB — Lei de Organização Básica</h3>
            </div>
            <div className="gdoc-card-body">
              <div className="gdoc-q">"Quais órgãos existem, e a quem eles se subordinam?"</div>
              <p>É a lei estadual, aprovada pela Assembleia Legislativa e sancionada pelo Governador, que cria formalmente o Corpo de Bombeiros Militar e define sua espinha dorsal: quais órgãos existem — COB, CAT, GBM, DAT e os demais — e como eles se relacionam entre si. Sem ela, a estrutura simplesmente não existe juridicamente: é o documento fundador de toda a organização.</p>
              <div className="gdoc-field"><span>Nível de decisão</span>Poder Legislativo</div>
              <div className="gdoc-field"><span>Exemplo prático</span>Criar um Comando Regional novo; subordinar o GBM ao COB</div>
              <div className="gdoc-field"><span>Frequência de mudança</span>Rara — é reforma estrutural</div>
            </div>
          </div>

          <div className="gdoc-card" data-k="ri">
            <div className="gdoc-tab" />
            <div className="gdoc-stamp">competência dos órgãos</div>
            <div className="gdoc-card-head">
              <div className="gdoc-doc-eyebrow">Ficha 02</div>
              <h3>Regimento Interno</h3>
            </div>
            <div className="gdoc-card-body">
              <div className="gdoc-q">"De quem é a responsabilidade disso?"</div>
              <p>Uma vez que a LOB já criou os órgãos, o Regimento Interno detalha, órgão por órgão, quais são as competências e atribuições de cada um — explica o "quem faz o quê" dentro da estrutura já existente. Como ainda organiza um órgão da administração pública, continua sendo ato do Poder Executivo estadual: mais ágil do que uma lei, mas ainda não é decisão interna da própria corporação.</p>
              <div className="gdoc-field"><span>Nível de decisão</span>Poder Executivo estadual</div>
              <div className="gdoc-field"><span>Exemplo prático</span>Definir que a CAT responde pela segurança contra incêndio, o COB pelo socorro</div>
              <div className="gdoc-field"><span>Frequência de mudança</span>Ocasional — reorganização de competências</div>
            </div>
          </div>

          <div className="gdoc-card gdoc-current" data-k="reg">
            <span className="gdoc-badge"><Search size={15} /> Fase atual — estamos aqui</span>
            <svg className="gdoc-lens" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4"><circle cx="10" cy="10" r="7.5" /><path d="M15.5 15.5l6.5 6.5" /></svg>
            <div className="gdoc-tab" />
            <div className="gdoc-stamp">rotina operacional</div>
            <div className="gdoc-card-head">
              <div className="gdoc-doc-eyebrow">Ficha 03</div>
              <h3>Regulamento de Serviço</h3>
            </div>
            <div className="gdoc-card-body">
              <div className="gdoc-q">"Como se faz, na prática, o serviço do dia a dia?"</div>
              <p>É o documento que o bombeiro realmente usa no cotidiano: escalas e turnos, uniforme, disciplina, o protocolo de atendimento da Central de Operações 193, as atribuições de cada função dentro do serviço operacional. Não trata de estrutura nem de competência de órgão — trata de rotina. Por ser ato interno da própria instituição, aprovado pelo Comandante-Geral, é o nível de decisão mais ágil dos três.</p>
              <div className="gdoc-field"><span>Nível de decisão</span>Interno da corporação</div>
              <div className="gdoc-field"><span>Exemplo prático</span>Escala de serviço, protocolo da Central 193, uniforme operacional</div>
              <div className="gdoc-field"><span>Frequência de mudança</span>Frequente — ajuste conforme a operação exige</div>
            </div>
          </div>
        </div>
        <div className="gdoc-foot">
          <button type="button" className="gdoc-ok" onClick={fechar}>Entendi, continuar</button>
        </div>
      </div>
    </div>
  )
}
