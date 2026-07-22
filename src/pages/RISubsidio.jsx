// Subsídio do Regimento Interno. Duas abas: "Regimento Interno" (visão unificada
// — Opção A) e "LOB". A SELEÇÃO (órgão + estado) é compartilhada entre as abas:
// o órgão vive como chapterId; a aba LOB o traduz para organKey. Assim, escolher
// um órgão/estado numa aba mantém o contexto na outra.
import { useState } from 'react'
import { organKeyOfChapter } from '../lib/riComparison.js'
import { useScenario } from '../context/ScenarioContext'
import RISubsidioComparativo from './RISubsidioComparativo.jsx'
import MinutaComparator from './MinutaComparator.jsx'

const TABS = [
  { id: 'ri', label: 'Regimento Interno' },
  { id: 'lob', label: 'LOB' },
]

export default function RISubsidio() {
  const { cenario } = useScenario()
  const [tab, setTab] = useState('ri')
  const [chapterId, setChapterId] = useState(null)
  const [stateAbbr, setStateAbbr] = useState(null)

  const organKey = organKeyOfChapter(chapterId)

  return (
    <div className="subsidio">
      <div className="subsidio-bar">
        <span className="subsidio-eyebrow">Subsídio · Regimento Interno</span>
        <div className="subsidio-tabs" role="tablist">
          {TABS.map(t => (
            <button key={t.id} type="button" role="tab" aria-selected={tab === t.id}
              className={`subsidio-tab${tab === t.id ? ' is-on' : ''}`} onClick={() => setTab(t.id)}>
              {t.label}
            </button>
          ))}
        </div>
      </div>

      {tab === 'ri' ? (
        <RISubsidioComparativo
          chapterId={chapterId} setChapterId={setChapterId}
          stateAbbr={stateAbbr} setStateAbbr={setStateAbbr}
        />
      ) : (
        <MinutaComparator
          controlledOrganKey={organKey}
          onOrganKey={k => setChapterId(k ? `${cenario === 'atual' ? 'atual:' : ''}organ:${k}` : chapterId)}
          controlledStateAbbr={stateAbbr}
          onStateAbbr={setStateAbbr}
        />
      )}
    </div>
  )
}
