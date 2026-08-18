// Prefixo de rota do acervo. Padrão '' = portal do membro (rotas de sempre); o visitante
// público monta as mesmas telas com base '/acervo-publico'. Existe para que Legislations,
// StateDetail e Search sejam REUSADAS sem fork e sem nenhum `if (visitante)` dentro delas.
import { createContext, useContext, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import { rotaEstado, rotaListaEstados } from '../lib/visitante.js'

const AcervoBaseContext = createContext('')

export function AcervoBaseProvider({ base, children }) {
  return <AcervoBaseContext.Provider value={base ?? ''}>{children}</AcervoBaseContext.Provider>
}

export function useAcervoNav() {
  const base = useContext(AcervoBaseContext)
  const navigate = useNavigate()
  return useMemo(() => ({
    irParaEstado: (id) => navigate(rotaEstado(base, id)),
    voltarParaEstados: () => navigate(rotaListaEstados(base)),
  }), [base, navigate])
}
