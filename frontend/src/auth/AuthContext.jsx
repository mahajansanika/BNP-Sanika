import { createContext, useContext, useState } from 'react'
import { login as apiLogin } from '../api/client'
import { clearSession, loadSession, saveSession } from './token'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [session, setSession] = useState(loadSession)

  async function login(username, password) {
    const res = await apiLogin(username, password)
    const next = { token: res.access_token, user: res.user }
    saveSession(next)
    setSession(next)
  }

  function logout() {
    clearSession()
    setSession(null)
  }

  const value = {
    user: session?.user ?? null,
    isLoggedIn: Boolean(session),
    login,
    logout,
  }
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}