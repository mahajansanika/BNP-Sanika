import { loadSession } from '../auth/token'
import { getMockLadder } from './mockData'

const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false'
const BASE = '/api/v1'

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))

async function request(path, options = {}) {
  const headers = { ...options.headers }
  const session = loadSession()
  if (session?.token) headers.Authorization = `Bearer ${session.token}`

  const res = await fetch(`${BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.message ?? `Request failed (${res.status})`)
  }
  return res.json()
}

export async function login(username, password) {
  if (USE_MOCK) {
    await wait(300)
    if (!username || !password) throw new Error('Enter a username and password')
    return { access_token: 'mock-token', user: { username, location: 'London' } }
  }
  return request('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
}

export async function getLadder(approach, filters) {
  if (USE_MOCK) {
    await wait(300)
    return getMockLadder(approach, filters)
  }
  const query = new URLSearchParams(filters).toString()
  return request(`/ladder/${approach}?${query}`)
}