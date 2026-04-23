import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { REFERENCE_PDFS } from "../config/resources"
import { MATERIAL_GROUPS } from "../config/materials"

const LECTURE_TOPIC_COLORS = {
  "Overview":           "bg-gray-700 text-gray-200",
  "Q1 — Risk Analysis": "bg-blue-900 text-blue-200",
  "Fundamentals":       "bg-indigo-900 text-indigo-200",
  "Authentication":     "bg-yellow-900 text-yellow-200",
  "Crypto":             "bg-emerald-900 text-emerald-200",
  "Protocols":          "bg-purple-900 text-purple-200",
  "DNS":                "bg-cyan-900 text-cyan-200",
  "Legal / Privacy":    "bg-rose-900 text-rose-200",
  "Censorship":         "bg-orange-900 text-orange-200",
}

const GROUP_COLORS = {
  blue:    "border-blue-700 bg-blue-950/40",
  emerald: "border-emerald-700 bg-emerald-950/40",
  purple:  "border-purple-700 bg-purple-950/40",
  cyan:    "border-cyan-700 bg-cyan-950/40",
  indigo:  "border-indigo-700 bg-indigo-950/40",
  yellow:  "border-yellow-700 bg-yellow-950/40",
  rose:    "border-rose-700 bg-rose-950/40",
  orange:  "border-orange-700 bg-orange-950/40",
  teal:    "border-teal-700 bg-teal-950/40",
  gray:    "border-gray-700 bg-gray-900/40",
}

const GROUP_BADGE = {
  blue:    "bg-blue-900 text-blue-200",
  emerald: "bg-emerald-900 text-emerald-200",
  purple:  "bg-purple-900 text-purple-200",
  cyan:    "bg-cyan-900 text-cyan-200",
  indigo:  "bg-indigo-900 text-indigo-200",
  yellow:  "bg-yellow-900 text-yellow-200",
  rose:    "bg-rose-900 text-rose-200",
  orange:  "bg-orange-900 text-orange-200",
  teal:    "bg-teal-900 text-teal-200",
  gray:    "bg-gray-700 text-gray-200",
}


function MaterialGroup({ group }) {
  const [open, setOpen] = useState(false)
  const borderCls = GROUP_COLORS[group.color] ?? GROUP_COLORS.gray
  const badgeCls  = GROUP_BADGE[group.color]  ?? GROUP_BADGE.gray
  const baseUrl   = import.meta.env.VITE_API_URL ?? "http://localhost:8000"

  return (
    <div className={`rounded-xl border ${borderCls}`}>
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between px-4 py-3 text-left"
      >
        <div className="flex items-center gap-3">
          <span className={`text-xs px-2 py-0.5 rounded-full font-medium shrink-0 ${badgeCls}`}>
            {group.items.length} papers
          </span>
          <span className="text-sm font-medium text-gray-100">{group.label}</span>
        </div>
        <span className="text-gray-500 text-lg">{open ? "−" : "+"}</span>
      </button>
      {open && (
        <div className="border-t border-gray-800 px-4 py-3 grid grid-cols-1 gap-2">
          {group.items.map(item => (
            <a
              key={item.file}
              href={`${baseUrl}/materials/${encodeURIComponent(item.file)}`}
              target="_blank"
              rel="noreferrer"
              className="flex items-start gap-3 rounded-lg px-3 py-2 hover:bg-white/5 transition-colors group"
            >
              <span className="text-lg mt-0.5 shrink-0">📄</span>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-200 group-hover:text-white">{item.title}</p>
                {item.note && <p className="text-xs text-gray-500 mt-0.5">{item.note}</p>}
              </div>
              <span className="text-xs text-gray-600 group-hover:text-gray-400 shrink-0 mt-1">Open →</span>
            </a>
          ))}
        </div>
      )}
    </div>
  )
}

export default function Resources() {
  const navigate = useNavigate()

  const grouped = REFERENCE_PDFS.reduce((acc, pdf) => {
    if (!acc[pdf.topic]) acc[pdf.topic] = []
    acc[pdf.topic].push(pdf)
    return acc
  }, {})

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <button onClick={() => navigate("/dashboard")} className="text-gray-400 hover:text-white text-sm">← Dashboard</button>
        <span className="font-bold text-lg">Resources</span>
        <span />
      </nav>

      <div className="max-w-5xl mx-auto px-6 py-10 space-y-14">

        {/* ── Lecture Slides ── */}
        <section>
          <h2 className="text-xl font-semibold mb-1">2026 Lecture Slides</h2>
          <p className="text-gray-400 text-sm mb-6">All current lecture PDFs — open in browser or download.</p>
          <div className="space-y-8">
            {Object.entries(grouped).map(([topic, pdfs]) => {
              const cls = LECTURE_TOPIC_COLORS[topic] ?? "bg-gray-700 text-gray-200"
              return (
                <div key={topic}>
                  <div className="flex items-center gap-3 mb-3">
                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${cls}`}>{topic}</span>
                    <div className="flex-1 h-px bg-gray-800" />
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {pdfs.map(pdf => (
                      <a
                        key={pdf.id}
                        href={`/pdfs/${encodeURIComponent(pdf.file)}`}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center gap-3 rounded-lg border border-gray-800 bg-gray-900 px-4 py-3 hover:border-gray-600 hover:bg-gray-800 transition-colors group"
                      >
                        <span className="text-2xl">📄</span>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-100 truncate group-hover:text-white">{pdf.title}</p>
                          <p className="text-xs text-gray-500">{pdf.file}</p>
                        </div>
                        <span className="text-xs text-gray-600 group-hover:text-gray-400 shrink-0">Open →</span>
                      </a>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        </section>

        {/* ── Reference Materials ── */}
        <section>
          <h2 className="text-xl font-semibold mb-1">Reference Materials</h2>
          <p className="text-gray-400 text-sm mb-6">
            {MATERIAL_GROUPS.reduce((n, g) => n + g.items.length, 0)} papers from the{" "}
            <code className="text-gray-300 text-xs bg-gray-800 px-1 rounded">materials/</code> corpus, grouped by exam relevance.
            Click a group to expand.
          </p>
          <div className="space-y-3">
            {MATERIAL_GROUPS.map(g => <MaterialGroup key={g.id} group={g} />)}
          </div>
        </section>

      </div>
    </div>
  )
}
