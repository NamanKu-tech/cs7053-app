import { useState, useEffect, useCallback, useRef } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { saveUserNote, getCommunityNotes, uploadNoteImage, getNoteVisibility } from "../api/topics"

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
  if (idx === -1) return content
  const start = idx + marker.length
  const rest = content.slice(start)
  const nextIdx = rest.search(/<!-- MODE:[A-Z]+ -->/)
  return (nextIdx === -1 ? rest : rest.slice(0, nextIdx)).trim()
}

function MarkdownWithImages({ content }) {
  return (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      components={{
        img: ({ src, alt }) => (
          <img
            src={src}
            alt={alt}
            className="max-w-full rounded-lg border border-gray-700 my-2"
          />
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  )
}

const NOTE_TABS = ["Write", "Community"]

export default function NoteEditor({ slug, prebuiltContent, userNoteContent }) {
  const [mode, setMode] = useState("TECHNICAL")
  const [content, setContent] = useState(userNoteContent || "")
  const [saved, setSaved] = useState(true)
  const [isPublic, setIsPublic] = useState(false)
  const [noteTab, setNoteTab] = useState("Write")
  const [community, setCommunity] = useState([])
  const [communityLoading, setCommunityLoading] = useState(false)
  const [uploading, setUploading] = useState(false)
  const fileInputRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => { setContent(userNoteContent || "") }, [userNoteContent])

  useEffect(() => {
    getNoteVisibility(slug).then(r => setIsPublic(r.is_public)).catch(() => {})
  }, [slug])

  useEffect(() => {
    if (noteTab !== "Community") return
    setCommunityLoading(true)
    getCommunityNotes(slug).then(setCommunity).finally(() => setCommunityLoading(false))
  }, [noteTab, slug])

  const save = useCallback(async () => {
    await saveUserNote(slug, content, isPublic)
    setSaved(true)
  }, [slug, content, isPublic])

  async function handleTogglePublic() {
    const next = !isPublic
    setIsPublic(next)
    await saveUserNote(slug, content, next)
    setSaved(true)
  }

  async function handleImageUpload(e) {
    const file = e.target.files?.[0]
    if (!file) return
    setUploading(true)
    try {
      const { url } = await uploadNoteImage(slug, file)
      const ta = textareaRef.current
      if (ta) {
        const before = content.slice(0, ta.selectionStart)
        const after = content.slice(ta.selectionEnd)
        const inserted = `${before}\n![](${url})\n${after}`
        setContent(inserted)
        setSaved(false)
      }
    } finally {
      setUploading(false)
      e.target.value = ""
    }
  }

  const modeContent = parseMode(prebuiltContent || "", mode)
  const hasMultipleModes = prebuiltContent?.includes("<!-- MODE:")

  return (
    <div className="grid grid-cols-2 gap-6">
      {/* Left — prebuilt notes */}
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
          <MarkdownWithImages content={modeContent} />
        </div>
      </div>

      {/* Right — your notes + community */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <div className="flex gap-1 border-b border-gray-800 w-full">
            {NOTE_TABS.map(t => (
              <button key={t} onClick={() => setNoteTab(t)}
                className={`px-3 py-1.5 text-xs font-medium border-b-2 transition-colors -mb-px
                  ${noteTab === t ? "border-blue-500 text-white" : "border-transparent text-gray-400 hover:text-gray-200"}`}>
                {t}
                {t === "Community" && community.length > 0 && (
                  <span className="ml-1 text-xs bg-gray-700 text-gray-300 px-1.5 py-0.5 rounded-full">{community.length}</span>
                )}
              </button>
            ))}
            {noteTab === "Write" && (
              <div className="ml-auto flex items-center gap-2 pb-1">
                <span className={`text-xs ${saved ? "text-gray-600" : "text-amber-400"}`}>
                  {saved ? "Saved" : "Unsaved"}
                </span>
                <button
                  onClick={save}
                  disabled={saved}
                  className={`px-3 py-1 text-xs rounded-md font-medium transition-all
                    ${saved ? "bg-gray-800 text-gray-600 cursor-default" : "bg-blue-600 hover:bg-blue-500 text-white"}`}
                >
                  Save
                </button>
              </div>
            )}
          </div>
        </div>

        {noteTab === "Write" && (
          <div>
            <div className="flex items-center gap-2 mb-2">
              <input ref={fileInputRef} type="file" accept="image/*" className="hidden" onChange={handleImageUpload} />
              <button
                onClick={() => fileInputRef.current?.click()}
                disabled={uploading}
                className="flex items-center gap-1 px-2.5 py-1 text-xs bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-md transition-colors disabled:opacity-50"
              >
                {uploading ? "Uploading..." : "📎 Add Image"}
              </button>
              <button
                onClick={handleTogglePublic}
                className={`flex items-center gap-1.5 px-2.5 py-1 text-xs rounded-md transition-colors font-medium
                  ${isPublic ? "bg-green-700 text-white" : "bg-gray-800 text-gray-400 hover:text-gray-200"}`}
              >
                {isPublic ? "🌐 Public" : "🔒 Private"}
              </button>
            </div>
            <textarea
              ref={textareaRef}
              value={content}
              onChange={e => { setContent(e.target.value); setSaved(false) }}
              placeholder="Add your own notes here (markdown + images supported)..."
              className="w-full bg-gray-900 text-gray-200 text-sm rounded-lg p-4 border border-gray-800 focus:outline-none focus:border-blue-500 resize-none h-[58vh] font-mono"
            />
          </div>
        )}

        {noteTab === "Community" && (
          <div className="overflow-auto max-h-[65vh] space-y-4">
            {communityLoading
              ? <p className="text-gray-500 text-sm text-center py-8">Loading...</p>
              : community.length === 0
                ? <p className="text-gray-500 text-sm text-center py-8">No public notes from others yet.</p>
                : community.map((n, i) => (
                    <div key={i} className="bg-gray-900 rounded-lg border border-gray-800 p-4">
                      <p className="text-xs text-blue-400 font-semibold mb-2">@{n.author}</p>
                      <div className="prose prose-invert prose-sm max-w-none">
                        <MarkdownWithImages content={n.content} />
                      </div>
                    </div>
                  ))
            }
          </div>
        )}
      </div>
    </div>
  )
}
