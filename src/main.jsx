import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import { AuthProvider } from './lib/auth.jsx'
import { ScenarioProvider } from './context/ScenarioContext.jsx'
import { VisitanteProvider } from './lib/visitante.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <ScenarioProvider>
          <VisitanteProvider>
            <App />
          </VisitanteProvider>
        </ScenarioProvider>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
)
