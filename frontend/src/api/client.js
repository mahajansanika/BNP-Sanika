import { getMockLadder } from './mockData'

const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false'
const BASE = '/api/v1'

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

export async function getLadder(approach, filters) {
  if (USE_MOCK) {
    await wait(300)
    return getMockLadder(approach, filters)
  }

  const query = new URLSearchParams(filters).toString()
  const res = await fetch(`${BASE}/ladder/${approach}?${query}`)
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.message ?? `Request failed (${res.status})`)
  }
  return res.json()
}