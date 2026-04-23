import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import { getPathTopics } from "../api/paths"

const ROADMAP = [
  { slug: "q2-tls-protocols",  label: "Q2 — TLS & Cryptography",  color: "#3b82f6" },
  { slug: "q1-risk-analysis",  label: "Q1 — Risk Analysis",        color: "#f59e0b" },
  { slug: "q4-dns-dnssec",     label: "Q4 — DNS & DNSSEC",         color: "#8b5cf6" },
  { slug: "q3-system-design",  label: "Q3 — System Design",        color: "#10b981" },
]

const MARKS_PER_PATH = 30
const TOTAL_MARKS = MARKS_PER_PATH * ROADMAP.length

export default function Graph() {
  const navigate = useNavigate()
  const [pathTopics, setPathTopics] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all(ROADMAP.map(p => getPathTopics(p.slug).then(t => [p.slug, t])))
      .then(results => setPathTopics(Object.fromEntries(results)))
      .finally(() => setLoading(false))
  }, [])

  const predictedMarks = ROADMAP.reduce((total, p) => {
    const topics = pathTopics[p.slug] || []
    if (!topics.length) return total
    const done = topics.filter(t => t.completed).length
    return total + Math.round((done / topics.length) * MARKS_PER_PATH)
  }, 0)
  const predictedPct = Math.round((predictedMarks / TOTAL_MARKS) * 100)

  const scoreColor = predictedPct >= 70 ? "#16a34a" : predictedPct >= 50 ? "#f59e0b" : "#3b82f6"

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center gap-4">
        <button onClick={() => navigate("/dashboard")} className="text-gray-400 hover:text-white text-sm">← Dashboard</button>
        <span className="text-gray-400 text-sm font-medium">Exam Roadmap</span>
      </nav>

      <div className="max-w-2xl mx-auto px-6 py-8">
        <div className="mb-8 flex items-start justify-between gap-6">
          <div>
            <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Predicted score</p>
            <div className="flex items-end gap-2">
              <span className="text-4xl font-bold" style={{ color: scoreColor }}>{predictedMarks}</span>
              <span className="text-gray-500 text-sm mb-1">/ {TOTAL_MARKS} marks · {predictedPct}%</span>
            </div>
            <div className="mt-3 w-56 bg-gray-800 rounded-full h-2">
              <div className="h-2 rounded-full transition-all duration-500"
                style={{ width: `${predictedPct}%`, background: scoreColor }} />
            </div>
          </div>
          <button
            onClick={() => navigate("/mock")}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg text-sm font-semibold transition-colors shrink-0 mt-1"
          >
            Test Your Knowledge
          </button>
        </div>

        {loading
          ? <div className="text-gray-500 text-center py-20">Loading...</div>
          : (
            <div className="space-y-3">
              {ROADMAP.map((p, idx) => {
                const topics = pathTopics[p.slug] || []
                const done = topics.filter(t => t.completed).length
                const pct = topics.length > 0 ? Math.round((done / topics.length) * 100) : 0

                return (
                  <div key={p.slug} className="rounded-xl overflow-hidden border border-gray-800">
                    <div className="px-5 py-4 flex items-center gap-4 bg-gray-900/40"
                      style={{ borderLeft: `3px solid ${p.color}` }}>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs text-gray-600">Priority {idx + 1}</span>
                          {idx === 0 && (
                            <span className="text-xs px-2 py-0.5 rounded-full bg-blue-950 text-blue-400 border border-blue-800">
                              Start here
                            </span>
                          )}
                        </div>
                        <h3 className="font-semibold text-white text-sm">{p.label}</h3>
                        <div className="flex items-center gap-2 mt-2">
                          <div className="w-32 bg-gray-800 rounded-full h-1">
                            <div className="h-1 rounded-full transition-all"
                              style={{ width: `${pct}%`, background: p.color }} />
                          </div>
                          <span className="text-xs text-gray-600">{done}/{topics.length} topics</span>
                        </div>
                      </div>
                      <button
                        onClick={() => navigate(`/path/${p.slug}?tab=mock`)}
                        className="text-xs text-gray-400 hover:text-white border border-gray-700 hover:border-gray-500 px-3 py-1.5 rounded-lg transition-colors shrink-0"
                      >
                        Practice
                      </button>
                    </div>

                    <div className="divide-y divide-gray-800/50">
                      {topics.map(t => (
                        <button
                          key={t.slug}
                          onClick={() => navigate(`/topic/${t.slug}`)}
                          className="w-full flex items-center gap-3 px-5 py-2.5 hover:bg-gray-900 transition-colors text-left group"
                        >
                          <span className={`shrink-0 w-4 h-4 rounded-full border flex items-center justify-center
                            ${t.completed
                              ? "bg-green-600 border-green-600 text-white text-xs"
                              : "border-gray-600 group-hover:border-gray-400"
                            }`}>
                            {t.completed && "✓"}
                          </span>
                          <span className={`text-sm transition-colors
                            ${t.completed ? "text-gray-600 line-through" : "text-gray-300 group-hover:text-white"}`}>
                            {t.title}
                          </span>
                        </button>
                      ))}
                    </div>
                  </div>
                )
              })}
            </div>
          )
        }
      </div>
    </div>
  )
}
