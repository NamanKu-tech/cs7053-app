import { useNavigate } from "react-router-dom"

const SLOT_COLORS = { Q1: "bg-amber-500", Q2: "bg-blue-500", Q3: "bg-emerald-500", Q4: "bg-violet-500" }
const SLOT_BAR = { Q1: "bg-amber-500", Q2: "bg-blue-500", Q3: "bg-emerald-500", Q4: "bg-violet-500" }

export default function PathCard({ path }) {
  const navigate = useNavigate()
  const pct = path.total_topics > 0 ? Math.round((path.completed_topics / path.total_topics) * 100) : 0

  return (
    <div onClick={() => navigate(`/path/${path.slug}`)}
      className="bg-gray-900 border border-gray-800 rounded-xl p-6 cursor-pointer hover:border-gray-600 transition-colors">
      <div className="flex items-center justify-between mb-3">
        <span className={`text-xs font-bold px-2 py-0.5 rounded text-white ${SLOT_COLORS[path.exam_slot]}`}>
          {path.exam_slot}
        </span>
        <span className="text-gray-400 text-sm">{path.completed_topics}/{path.total_topics}</span>
      </div>
      <h3 className="text-white font-semibold mb-1">{path.title}</h3>
      <p className="text-gray-500 text-xs mb-4 line-clamp-2">{path.description}</p>
      <div className="w-full bg-gray-800 rounded-full h-1.5">
        <div className={`h-1.5 rounded-full transition-all ${SLOT_BAR[path.exam_slot]}`} style={{ width: `${pct}%` }} />
      </div>
      <p className="text-gray-500 text-xs mt-1">{pct}% complete</p>
    </div>
  )
}
