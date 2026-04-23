import { useState } from "react"

export default function QuestionList({ questions, onSelectForPractice }) {
  const [expanded, setExpanded] = useState(null)

  if (questions.length === 0) return (
    <p className="text-gray-500 text-sm py-8 text-center">No past questions for this topic yet.</p>
  )

  return (
    <div className="space-y-3">
      {questions.map(q => (
        <div key={q.id} className="bg-gray-900 rounded-lg border border-gray-800">
          <button
            className="w-full flex items-center justify-between px-4 py-3 hover:bg-gray-800 rounded-lg transition-colors text-left"
            onClick={() => setExpanded(expanded === q.id ? null : q.id)}>
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono bg-gray-800 px-2 py-0.5 rounded text-blue-400">{q.exam_slot}</span>
              <span className="text-xs text-gray-500">{q.year}</span>
              <span className="text-xs text-gray-500">{q.marks} marks</span>
            </div>
            <svg className={`w-4 h-4 text-gray-500 transition-transform ${expanded === q.id ? "rotate-180" : ""}`}
              fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          {expanded === q.id && (
            <div className="px-4 pb-4 space-y-4 border-t border-gray-800 pt-3">
              <div>
                <p className="text-xs text-gray-400 font-semibold uppercase tracking-wider mb-1">Question</p>
                <p className="text-sm text-gray-200 leading-relaxed">{q.question_text}</p>
              </div>
              <div>
                <p className="text-xs text-gray-400 font-semibold uppercase tracking-wider mb-1">Sample Answer</p>
                <p className="text-sm text-gray-400 leading-relaxed">{q.sample_answer}</p>
              </div>
              <button onClick={() => onSelectForPractice(q)}
                className="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-md transition-colors">
                Practice this →
              </button>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
