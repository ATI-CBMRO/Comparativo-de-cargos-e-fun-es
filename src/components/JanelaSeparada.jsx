import { useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'

// Uma janela aberta por window.open nasce com <head> vazio — sem clonar as folhas de
// estilo, o conteúdo sai sem CSS nenhum. Cobre o dev (Vite injeta <style>) e a produção
// (<link rel="stylesheet">). É um retrato do momento da abertura: estilos injetados
// depois (HMR no dev) só aparecem ao reabrir a janela.
function clonarEstilos(origem, destino) {
  origem.querySelectorAll('style, link[rel="stylesheet"]')
    .forEach(no => destino.head.appendChild(no.cloneNode(true)))
}

// Renderiza `children` numa janela separada do navegador, mantendo-os na MESMA árvore
// React da janela principal (createPortal) — é isso que preserva login, cenário,
// Firestore e o estado do formulário sem nenhuma sincronização entre janelas.
export default function JanelaSeparada({
  titulo, nome = 'janela-portal', largura = 560, altura = 780,
  onFechar, onBloqueada, children,
}) {
  const [corpo, setCorpo] = useState(null)
  const janelaRef = useRef(null)
  // Callbacks em ref: mudam de identidade a cada render do pai e não podem
  // reabrir a janela.
  const onFecharRef = useRef(onFechar)
  const onBloqueadaRef = useRef(onBloqueada)
  useEffect(() => { onFecharRef.current = onFechar }, [onFechar])
  useEffect(() => { onBloqueadaRef.current = onBloqueada }, [onBloqueada])

  useEffect(() => {
    const janela = window.open('', nome, `width=${largura},height=${altura}`)
    if (!janela) { onBloqueadaRef.current?.(); return undefined }
    janelaRef.current = janela

    // Reabrir com o mesmo nome devolve a janela JÁ existente, que pode trazer o
    // conteúdo anterior — limpar antes de portalizar.
    janela.document.body.innerHTML = ''
    clonarEstilos(document, janela.document)
    janela.document.body.className = 'janela-sep-body'
    setCorpo(janela.document.body)

    // Avisa o pai uma única vez, venha o fechamento do evento ou do polling.
    let avisado = false
    const avisarFechamento = () => {
      if (avisado) return
      avisado = true
      onFecharRef.current?.()
    }
    janela.addEventListener('beforeunload', avisarFechamento)
    // Rede de segurança: nem todo navegador dispara beforeunload em janela
    // about:blank aberta por script.
    const vigia = setInterval(() => {
      if (janela.closed) { clearInterval(vigia); avisarFechamento() }
    }, 500)
    // Janela principal fechada/recarregada não pode deixar a filha órfã.
    const fecharFilha = () => janela.close()
    window.addEventListener('beforeunload', fecharFilha)

    return () => {
      clearInterval(vigia)
      janela.removeEventListener('beforeunload', avisarFechamento)
      window.removeEventListener('beforeunload', fecharFilha)
      janela.close()
    }
  }, [nome, largura, altura])

  // Trocar de decisão não reabre a janela: só atualiza o título e a traz para frente.
  useEffect(() => {
    const janela = janelaRef.current
    if (janela && !janela.closed) {
      janela.document.title = titulo
      janela.focus()
    }
  }, [titulo])

  if (!corpo) return null
  return createPortal(children, corpo)
}
