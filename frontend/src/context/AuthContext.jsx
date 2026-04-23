import { createContext, useContext, useState, useCallback } from "react"
import client from "../api/client"

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"))

  const googleLogin = useCallback(async (credential) => {
    const res = await client.post("/auth/google", { credential })
    localStorage.setItem("token", res.data.access_token)
    setToken(res.data.access_token)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem("token")
    setToken(null)
  }, [])

  return (
    <AuthContext.Provider value={{ token, googleLogin, logout, isAuthed: !!token }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
