import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import { getPaths } from "../api/paths"
import PathCard from "../components/PathCard"

export default function Dashboard() {
  const [paths, setPaths] = useState([])
  const [loading, setLoading] = useState(true)
  const { logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => { getPaths().then(setPaths).finally(() => setLoading(false)) }, [])

  const totalTopics = paths.reduce((s, p) => s + p.total_topics, 0)
  const completedTopics = paths.reduce((s, p) => s + p.completed_topics, 0)
  const overallPct = totalTopics > 0 ? Math.round((completedTopics / totalTopics) * 100) : 0

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <span className="font-bold text-lg">CS7053 Prep</span>
        <div className="flex gap-4">
          <button onClick={() => navigate("/mock")} className="text-gray-400 hover:text-white text-sm">Mock Exams</button>
          <button onClick={() => navigate("/cheatsheet")} className="text-gray-400 hover:text-white text-sm">Cheat Sheet</button>
          <button onClick={() => navigate("/resources")} className="text-gray-400 hover:text-white text-sm">Resources</button>
          <button onClick={() => navigate("/graph")} className="text-gray-400 hover:text-white text-sm">Roadmap</button>
          <button onClick={logout} className="text-gray-400 hover:text-white text-sm">Logout</button>
        </div>
      </nav>
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h2 className="text-gray-400 text-sm mb-2">Overall progress</h2>
          <div className="flex items-center gap-4">
            <div className="flex-1 bg-gray-800 rounded-full h-2">
              <div className="h-2 rounded-full bg-blue-500 transition-all" style={{ width: `${overallPct}%` }} />
            </div>
            <span className="text-sm text-gray-300 shrink-0">{completedTopics}/{totalTopics} topics · {overallPct}%</span>
          </div>
        </div>
        {loading
          ? <div className="text-gray-500 text-center py-20">Loading...</div>
          : <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">{paths.map(p => <PathCard key={p.slug} path={p} />)}</div>
        }
      </div>
    </div>
  )
}
