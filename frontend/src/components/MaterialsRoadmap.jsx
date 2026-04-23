import { useState } from "react"
import { toggleMaterial } from "../api/topics"

const API = import.meta.env.VITE_API_URL || ""

function materialUrl(m) {
  if (m.external_url) return m.external_url
  return `${API}/materials/${encodeURIComponent(m.file)}`
}

function materialLabel(m) {
  if (m.external_url && !m.file) return "Open RFC"
  return "Open PDF"
}

export default function MaterialsRoadmap({ slug, initialMaterials, initialProgress }) {
  const [materials, setMaterials] = useState(initialMaterials)
  const [progress, setProgress] = useState(initialProgress)

  async function handleToggle(materialId) {
    const { completed } = await toggleMaterial(slug, materialId)
    const updated = materials.map(m => m.id === materialId ? { ...m, completed } : m)
    setMaterials(updated)
    const done = updated.filter(m => m.completed).length
    setProgress(updated.length ? Math.round(done / updated.length * 100) : 0)
  }

  if (!materials.length) {
    return <p className="text-gray-500 text-sm py-8 text-center">No materials linked to this topic yet.</p>
  }

  return (
    <div className="space-y-6">
      {/* Progress bar */}
      <div>
        <div className="flex justify-between items-center mb-2">
          <span className="text-xs text-gray-400 uppercase tracking-wider">Reading Progress</span>
          <span className="text-sm font-semibold text-white">{progress}%</span>
        </div>
        <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-500"
            style={{
              width: `${progress}%`,
              background: progress === 100
                ? "linear-gradient(90deg, #10b981, #34d399)"
                : "linear-gradient(90deg, #3b82f6, #60a5fa)",
            }}
          />
        </div>
        <p className="text-xs text-gray-500 mt-1">
          {materials.filter(m => m.completed).length} of {materials.length} papers read
        </p>
      </div>

      {/* Materials list */}
      <ol className="relative border-l border-gray-800 ml-3 space-y-0">
        {materials.map((m, idx) => (
          <li key={m.id} className="ml-6 pb-8 last:pb-0">
            {/* Timeline dot */}
            <span className={`absolute -left-3 flex items-center justify-center w-6 h-6 rounded-full ring-4 ring-gray-950 transition-colors
              ${m.completed ? "bg-green-500" : "bg-gray-700"}`}>
              {m.completed
                ? <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 12 12"><path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2 6l3 3 5-5"/></svg>
                : <span className="text-xs text-gray-400 font-mono">{idx + 1}</span>
              }
            </span>

            <div className={`ml-2 p-4 rounded-xl border transition-colors
              ${m.completed ? "border-green-900/40 bg-green-950/20" : "border-gray-800 bg-gray-900/40"}`}>
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <h3 className={`text-sm font-medium leading-snug ${m.completed ? "text-green-300" : "text-white"}`}>
                    {m.title}
                  </h3>
                  {m.note && (
                    <p className="text-xs text-gray-400 mt-1 leading-relaxed">{m.note}</p>
                  )}
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  {(m.file || m.external_url) && (
                    <a
                      href={materialUrl(m)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-3 py-1.5 text-xs rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-300 hover:text-white transition-colors border border-gray-700 hover:border-gray-600"
                    >
                      {materialLabel(m)}
                    </a>
                  )}
                  <button
                    onClick={() => handleToggle(m.id)}
                    className={`px-3 py-1.5 text-xs rounded-lg border transition-colors
                      ${m.completed
                        ? "bg-green-900/40 border-green-800 text-green-300 hover:bg-green-900/60"
                        : "bg-gray-800 border-gray-700 text-gray-400 hover:text-white hover:border-gray-500"
                      }`}
                  >
                    {m.completed ? "Done ✓" : "Mark read"}
                  </button>
                </div>
              </div>
            </div>
          </li>
        ))}
      </ol>
    </div>
  )
}
