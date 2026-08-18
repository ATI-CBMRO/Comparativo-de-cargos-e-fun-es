// Subsídio do Regulamento Geral — mesmo padrão de abas do RI (documento + LOB).
// Hoje só a comparação do Regulamento existe; a aba LOB entra como "em breve".
import SubsidioTabs from '../components/SubsidioTabs.jsx'
import RegulamentoComparator from './RegulamentoComparator.jsx'

export default function RegSubsidio({ escopo } = {}) {
  return (
    <SubsidioTabs
      trilha={escopo === 'servico' ? 'Regulamento de Serviço' : 'Regulamento Geral'}
      tabs={[
        { id: 'reg', label: 'Regulamento', render: () => <RegulamentoComparator escopo={escopo} /> },
        {
          id: 'lob', label: 'LOB', soon: true,
          soonNote: 'O subsídio a partir das Leis de Organização Básica seguirá o mesmo padrão do Regimento Interno.',
        },
      ]}
    />
  )
}
