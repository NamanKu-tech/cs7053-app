import { useNavigate } from "react-router-dom"
import { toggleProgress } from "../api/paths"

export default function TopicRow({ topic, onToggle }) {
  const navigate = useNavigate()

  async function handleCheck(e) {
    e.stopPropagation()
    await toggleProgress(topic.slug, !topic.completed)
    onToggle(topic.slug, !topic.completed)
  }

  return (
    <div onClick={() => navigate(`/topic/${topic.slug}`)}
      className="flex items-center gap-4 px-4 py-3 rounded-lg hover:bg-gray-800 cursor-pointer group transition-colors">
      <button
        onClick={handleCheck}
        className={`w-5 h-5 rounded border-2 flex items-center justify-center shrink-0 transition-colors
          ${topic.completed ? "bg-green-500 border-green-500" : "border-gray-600 group-hover:border-gray-400"}`}
        aria-label={topic.completed ? "Mark incomplete" : "Mark complete"}>
        {topic.completed && (
          <svg className="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
          </svg>
        )}
      </button>
      <span className={`text-sm ${topic.completed ? "text-gray-500 line-through" : "text-gray-200"}`}>
        {topic.title}
      </span>
    </div>
  )
}
