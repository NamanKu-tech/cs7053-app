import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { GoogleLogin } from "@react-oauth/google"
import { useAuth } from "../context/AuthContext"

export default function Login() {
  const { googleLogin, isAuthed } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState("")

  useEffect(() => {
    if (isAuthed) navigate("/dashboard")
  }, [isAuthed, navigate])

  async function handleSuccess(response) {
    setError("")
    try {
      await googleLogin(response.credential)
      navigate("/dashboard")
    } catch (err) {
      const status = err.response?.status
      if (status === 403) setError("Please sign in with your @tcd.ie account.")
      else setError("Login failed. Try again.")
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center">
      <div className="bg-gray-900 rounded-xl p-8 w-full max-w-sm border border-gray-800 flex flex-col items-center gap-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-white mb-1">CS7053 Prep</h1>
          <p className="text-gray-400 text-sm">Security &amp; Privacy exam prep</p>
        </div>
        <p className="text-xs text-gray-500">Sign in with your @tcd.ie Google account</p>
        <GoogleLogin
          onSuccess={handleSuccess}
          onError={() => setError("Google login failed. Try again.")}
          theme="filled_black"
          shape="rectangular"
          size="large"
          text="signin_with"
        />
        {error && <p className="text-red-400 text-sm text-center">{error}</p>}
      </div>
    </div>
  )
}
