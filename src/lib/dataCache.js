// Cache em memória para os fetches de dados (JSONs em database/), compartilhado entre
// páginas. Evita baixar o mesmo arquivo (ex.: states_data.json, ~760 KB) a cada navegação
// e deduplica corridas simultâneas — a mesma Promise é reusada enquanto ela estiver "em voo".
const cache = new Map()

// `optional: true`: um 404 não é erro — resolve para `null` (ex.: organs_detail/<uf>.json
// nem sempre existe). Falhas nunca ficam em cache — a próxima chamada tenta de novo.
export function fetchJson(url, { optional = false } = {}) {
  if (cache.has(url)) return cache.get(url)
  const promise = fetch(url)
    .then((r) => {
      if (r.status === 404 && optional) return null
      if (!r.ok) throw new Error(`HTTP ${r.status} ao carregar ${url}`)
      return r.json()
    })
    .catch((err) => {
      cache.delete(url)
      throw err
    })
  cache.set(url, promise)
  return promise
}

export function clearJsonCache(url) {
  if (url) cache.delete(url)
  else cache.clear()
}
