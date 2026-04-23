import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { getPrebuiltNote, getUserNote, getMaterials, getTopicProgress, setTopicProgress } from "../api/topics"
import NoteEditor from "../components/NoteEditor"
import MaterialsRoadmap from "../components/MaterialsRoadmap"
import { TOPIC_MEDIA } from "../config/topicMedia"

const TABS = ["Notes", "Materials", "Video", "Podcast"]

export default function Topic() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const [tab, setTab] = useState("Notes")
  const [prebuilt, setPrebuilt] = useState("")
  const [userNote, setUserNote] = useState("")
  const [materials, setMaterials] = useState([])
  const [materialsProgress, setMaterialsProgress] = useState(0)
  const [completed, setCompleted] = useState(false)
  const [toggling, setToggling] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    Promise.all([getPrebuiltNote(slug), getUserNote(slug), getMaterials(slug), getTopicProgress(slug)])
      .then(([pb, un, mat, prog]) => {
        setPrebuilt(pb.content)
        setUserNote(un.content)
        setMaterials(mat.materials)
        setMaterialsProgress(mat.progress)
        setCompleted(prog.completed)
      })
      .finally(() => setLoading(false))
  }, [slug])

  async function handleToggleComplete() {
    setToggling(true)
    try {
      const res = await setTopicProgress(slug, !completed)
      setCompleted(res.completed)
    } finally {
      setToggling(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center gap-4">
        <button onClick={() => navigate(-1)} className="text-gray-400 hover:text-white text-sm">← Back</button>
        <span className="text-gray-600">/</span>
        <span className="text-sm text-gray-300 capitalize">{slug.replace(/-/g, " ")}</span>
        <button
          onClick={handleToggleComplete}
          disabled={toggling || loading}
          className={`ml-auto text-sm font-medium px-4 py-1.5 rounded-lg border transition-colors disabled:opacity-50
            ${completed
              ? "bg-green-900/40 border-green-700 text-green-400 hover:bg-green-900/60"
              : "border-gray-700 text-gray-400 hover:border-gray-500 hover:text-white"
            }`}
        >
          {completed ? "✓ Completed" : "Mark as Complete"}
        </button>
      </nav>
      <div className="max-w-6xl mx-auto px-6 py-6">
        <div className="flex gap-1 mb-6 border-b border-gray-800">
          {TABS.map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px
                ${tab === t ? "border-blue-500 text-white" : "border-transparent text-gray-400 hover:text-gray-200"}`}>
              {t}
            </button>
          ))}
        </div>
        {loading
          ? <div className="text-gray-500 text-center py-20">Loading...</div>
          : <>
              <div className={tab === "Notes" ? "" : "hidden"}>
                <NoteEditor slug={slug} prebuiltContent={prebuilt} userNoteContent={userNote} />
              </div>
              <div className={tab === "Materials" ? "" : "hidden"}>
                <MaterialsRoadmap slug={slug} initialMaterials={materials} initialProgress={materialsProgress} />
              </div>
              <div className={tab === "Video" ? "" : "hidden"}>
                {TOPIC_MEDIA[slug]?.videoUrl
                  ? (
                    TOPIC_MEDIA[slug].videoUrl.includes("youtube") || TOPIC_MEDIA[slug].videoUrl.includes("youtu.be")
                      ? (
                        <div className="relative w-full rounded-xl overflow-hidden border border-gray-800" style={{ paddingBottom: "56.25%" }}>
                          <iframe
                            src={TOPIC_MEDIA[slug].videoUrl}
                            title={`${slug} video`}
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                            allowFullScreen
                            className="absolute inset-0 w-full h-full"
                          />
                        </div>
                      )
                      : (
                        <div className="rounded-xl overflow-hidden border border-gray-800 bg-black">
                          <video
                            controls
                            className="w-full"
                            src={TOPIC_MEDIA[slug].videoUrl}
                          >
                            Your browser does not support the video element.
                          </video>
                        </div>
                      )
                  )
                  : (
                    <div className="flex flex-col items-center justify-center py-24 text-gray-600">
                      <span className="text-4xl mb-3">▶</span>
                      <p className="text-sm">No video added yet.</p>
                    </div>
                  )
                }
              </div>
              <div className={tab === "Podcast" ? "" : "hidden"}>
                {TOPIC_MEDIA[slug]?.audioUrl
                  ? (
                    <div className="rounded-xl border border-gray-800 bg-gray-900 p-6">
                      <p className="text-xs text-gray-500 uppercase tracking-wider mb-3">Audio / Podcast</p>
                      <audio controls className="w-full" src={TOPIC_MEDIA[slug].audioUrl}>
                        Your browser does not support the audio element.
                      </audio>
                    </div>
                  )
                  : (
                    <div className="flex flex-col items-center justify-center py-24 text-gray-600">
                      <span className="text-4xl mb-3">🎙</span>
                      <p className="text-sm">No podcast added yet.</p>
                    </div>
                  )
                }
              </div>
            </>
        }
      </div>
    </div>
  )
}
