import { useState, useEffect, useCallback } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { saveUserNote } from "../api/topics"

const MODES = [
  { id: "EASY",      label: "Easy",      emoji: "🟢", desc: "Explain like I'm 5", color: "green" },
  { id: "TECHNICAL", label: "Technical", emoji: "🔵", desc: "Exam-ready depth",   color: "blue"  },
  { id: "HINGLISH",  label: "Hinglish",  emoji: "🟠", desc: "Hindi + English",    color: "orange"},
]

const MODE_STYLES = {
  green:  { active: "bg-green-600 text-white border-green-500",  inactive: "text-green-400 border-green-900 hover:border-green-700 hover:bg-green-900/30" },
  blue:   { active: "bg-blue-600 text-white border-blue-500",    inactive: "text-blue-400 border-blue-900 hover:border-blue-700 hover:bg-blue-900/30" },
  orange: { active: "bg-orange-600 text-white border-orange-500",inactive: "text-orange-400 border-orange-900 hover:border-orange-700 hover:bg-orange-900/30" },
}

function parseMode(content, mode) {
  const marker = `<!-- MODE:${mode} -->`
  const idx = content.indexOf(marker)
  if (idx === -1) return content  // fallback: show full content if no markers
  const start = idx + marker.length
  const rest = content.slice(start)
  // find the next mode marker
  const nextIdx = rest.search(/<!-- MODE:[A-Z]+ -->/)
  return (nextIdx === -1 ? rest : rest.slice(0, nextIdx)).trim()
}

export default function NoteEditor({ slug, prebuiltContent, userNoteContent }) {
  const [mode, setMode] = useState("TECHNICAL")
  const [content, setContent] = useState(userNoteContent || "")
  const [saved, setSaved] = useState(true)

  useEffect(() => { setContent(userNoteContent || "") }, [userNoteContent])

  const save = useCallback(async () => {
    await saveUserNote(slug, content)
    setSaved(true)
  }, [slug, content])

  const modeContent = parseMode(prebuiltContent || "", mode)
  const hasMultipleModes = prebuiltContent?.includes("<!-- MODE:")

  return (
    <div className="grid grid-cols-2 gap-6">
      <div>
        <div className="mb-4">
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Pre-built Notes</h3>
          {hasMultipleModes && (
            <div className="flex gap-2">
              {MODES.map(m => {
                const styles = MODE_STYLES[m.color]
                const isActive = mode === m.id
                return (
                  <button
                    key={m.id}
                    onClick={() => setMode(m.id)}
                    className={`flex-1 flex flex-col items-center gap-0.5 px-3 py-2.5 rounded-xl border text-sm font-semibold transition-all duration-150
                      ${isActive ? styles.active : styles.inactive}`}
                  >
                    <span className="text-base leading-none">{m.emoji}</span>
                    <span className="leading-none">{m.label}</span>
                    <span className={`text-[10px] font-normal leading-none mt-0.5 ${isActive ? "opacity-80" : "opacity-50"}`}>{m.desc}</span>
                  </button>
                )
              })}
            </div>
          )}
        </div>
        <div className="prose prose-invert prose-sm max-w-none bg-gray-900 rounded-lg p-4 overflow-auto max-h-[60vh]">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{modeContent}</ReactMarkdown>
        </div>
      </div>
      <div>
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Your Notes</h3>
          <div className="flex items-center gap-2">
            <span className={`text-xs ${saved ? "text-gray-600" : "text-amber-400"}`}>
              {saved ? "Saved" : "Unsaved changes"}
            </span>
            <button
              onClick={save}
              disabled={saved}
              className={`px-3 py-1 text-xs rounded-md font-medium transition-all duration-150
                ${saved
                  ? "bg-gray-800 text-gray-600 cursor-default"
                  : "bg-blue-600 hover:bg-blue-500 text-white cursor-pointer"
                }`}
            >
              Save
            </button>
          </div>
        </div>
        <textarea
          value={content}
          onChange={e => { setContent(e.target.value); setSaved(false) }}
          placeholder="Add your own notes here (markdown supported, saved automatically on blur)..."
          className="w-full bg-gray-900 text-gray-200 text-sm rounded-lg p-4 border border-gray-800 focus:outline-none focus:border-blue-500 resize-none h-[65vh] font-mono"
        />
      </div>
    </div>
  )
}
