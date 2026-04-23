import { useState, useEffect, useRef } from "react"
import { gradeAnswer, getAttempt, getHistory } from "../api/mock"

function scoreColor(score) {
  if (score === null) return "text-gray-400"
  if (score >= 7) return "text-green-400"
  if (score >= 5) return "text-amber-400"
  return "text-red-400"
}

export default function MockPractice({ questions, initialQuestion }) {
  const [selected, setSelected] = useState(initialQuestion || questions[0] || null)
  const [answer, setAnswer] = useState("")
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const pollRef = useRef(null)

  useEffect(() => { if (initialQuestion) setSelected(initialQuestion) }, [initialQuestion])

  useEffect(() => {
    if (!selected) return
    getHistory(selected.id).then(setHistory)
    setResult(null)
    setAnswer("")
  }, [selected?.id])

  async function handleSubmit() {
    if (!selected || !answer.trim()) return
    setLoading(true)
    try {
      const res = await gradeAnswer(selected.id, answer)
      setSubmitted(true)
      setLoading(false)
      pollAttempt(res.attempt_id, 5000)
    } catch {
      setLoading(false)
    }
  }

  function pollAttempt(attempt_id, delay) {
    clearTimeout(pollRef.current)
    pollRef.current = setTimeout(async () => {
      try {
        const res = await getAttempt(attempt_id)
        if (res.status === "complete") {
          setResult(res)
          setSubmitted(false)
          getHistory(selected.id).then(setHistory)
        } else {
          pollAttempt(attempt_id, Math.min(delay * 2, 30000))
        }
      } catch {
        pollAttempt(attempt_id, Math.min(delay * 2, 30000))
      }
    }, delay)
  }

  useEffect(() => () => clearTimeout(pollRef.current), [])

  if (questions.length === 0) return (
    <p className="text-gray-500 text-sm py-8 text-center">No questions available for practice yet.</p>
  )

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <label className="text-xs text-gray-400 font-semibold uppercase tracking-wider block mb-2">Select Question</label>
        <select value={selected?.id || ""} onChange={e => setSelected(questions.find(q => q.id === parseInt(e.target.value)))}
          className="bg-gray-900 border border-gray-700 text-gray-200 text-sm rounded-lg px-3 py-2 w-full focus:outline-none focus:border-blue-500">
          {questions.map(q => (
            <option key={q.id} value={q.id}>{q.year} · {q.exam_slot} · {q.marks} marks</option>
          ))}
        </select>
      </div>

      {selected && (
        <div className="bg-gray-900 rounded-lg p-4 border border-gray-800">
          <p className="text-xs text-gray-400 font-semibold uppercase tracking-wider mb-2">Question ({selected.marks} marks)</p>
          <p className="text-sm text-gray-200 leading-relaxed">{selected.question_text}</p>
        </div>
      )}

      <div>
        <label className="text-xs text-gray-400 font-semibold uppercase tracking-wider block mb-2">Your Answer</label>
        <textarea value={answer} onChange={e => setAnswer(e.target.value)}
          placeholder="Write your exam answer here..."
          className="w-full bg-gray-900 text-gray-200 text-sm rounded-lg p-4 border border-gray-800 focus:outline-none focus:border-blue-500 resize-none h-48 font-mono" />
      </div>

      <button onClick={handleSubmit} disabled={loading || !answer.trim()}
        className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-6 py-2.5 rounded-lg text-sm font-medium transition-colors">
        {loading ? "Submitting..." : "Submit for Grading"}
      </button>

      {submitted && (
        <div className="rounded-lg border border-amber-800/40 bg-amber-950/20 px-4 py-5 text-center space-y-1">
          <p className="text-sm text-amber-300 font-medium">Answer submitted</p>
          <p className="text-xs text-gray-400">Grading can take up to 10 minutes. You can navigate away — your result will appear here when ready.</p>
        </div>
      )}

      {result && (
        <div className="bg-gray-900 rounded-lg p-4 border border-gray-700">
          {result.score !== null
            ? <>
                <div className="flex items-center gap-3 mb-3">
                  <span className={`text-2xl font-bold ${scoreColor(result.score)}`}>{result.score}/10</span>
                  <span className="text-xs text-gray-400">confidence score</span>
                </div>
                <p className="text-sm text-gray-300 leading-relaxed">{result.feedback}</p>
              </>
            : <p className="text-sm text-yellow-400">{result.feedback}</p>
          }
        </div>
      )}

      {history.length > 0 && (
        <div>
          <h4 className="text-xs text-gray-400 font-semibold uppercase tracking-wider mb-3">Past Attempts</h4>
          <div className="space-y-2">
            {history.map(a => (
              <div key={a.id} className="bg-gray-900 rounded-lg p-3 border border-gray-800 flex items-center justify-between">
                <span className="text-xs text-gray-500">{new Date(a.attempted_at).toLocaleDateString()}</span>
                <span className={`text-sm font-semibold ${scoreColor(a.score)}`}>
                  {a.score !== null ? `${a.score}/10` : "N/A"}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
