import { createContext, useContext, useState, useCallback } from "react"
import client from "../api/client"

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"))

  const login = useCallback(async (email, password) => {
    const res = await client.post("/auth/login", { email, password })
    localStorage.setItem("token", res.data.access_token)
    setToken(res.data.access_token)
  }, [])

  const register = useCallback(async (email, password) => {
    const res = await client.post("/auth/register", { email, password })
    localStorage.setItem("token", res.data.access_token)
    setToken(res.data.access_token)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem("token")
    setToken(null)
  }, [])

  return (
    <AuthContext.Provider value={{ token, login, register, logout, isAuthed: !!token }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
