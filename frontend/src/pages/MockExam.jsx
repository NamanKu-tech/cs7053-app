import { useEffect, useState, useRef } from "react"
import { useNavigate } from "react-router-dom"
import { getExamCards, gradeExam } from "../api/mock"

const DIFF = {
  easy:   { border: "border-green-800",  badge: "bg-green-900 text-green-300",  label: "Easy" },
  medium: { border: "border-amber-800",  badge: "bg-amber-900 text-amber-300",  label: "Medium" },
  hard:   { border: "border-red-800",    badge: "bg-red-900 text-red-300",      label: "Hard" },
}

function formatTime(s) {
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const sec = s % 60
  return `${h}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}`
}

function scoreColor(score) {
  if (score === null || score === undefined) return "text-gray-400"
  if (score >= 7) return "text-green-400"
  if (score >= 5) return "text-amber-400"
  return "text-red-400"
}

// flatten all parts across all groups into a list for grading
function allParts(card) {
  return card.groups.flatMap(g => g.parts)
}

export default function MockExam() {
  const navigate = useNavigate()
  const [cards, setCards] = useState([])
  const [loading, setLoading] = useState(true)
  const [view, setView] = useState("cards")
  const [selectedCard, setSelectedCard] = useState(null)
  const [answers, setAnswers] = useState({})   // partId → text
  const [timeLeft, setTimeLeft] = useState(7200)
  const [grading, setGrading] = useState(false)
  const [results, setResults] = useState([])   // [{exam_question_id, score, feedback, part}]
  const timerRef = useRef(null)
  const submitRef = useRef(null)

  useEffect(() => {
    getExamCards().then(setCards).finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (view !== "exam") return
    timerRef.current = setInterval(() => {
      setTimeLeft(t => {
        if (t <= 1) { clearInterval(timerRef.current); submitRef.current?.(); return 0 }
        return t - 1
      })
    }, 1000)
    return () => clearInterval(timerRef.current)
  }, [view])

  function startExam(card) {
    setSelectedCard(card)
    setAnswers({})
    setResults([])
    setTimeLeft(7200)
    setView("exam")
  }

  async function handleSubmit() {
    clearInterval(timerRef.current)
    setGrading(true)
    try {
      const parts = allParts(selectedCard)
      const items = parts.map(p => ({ exam_question_id: p.id, answer_text: answers[p.id] || "" }))
      const data = await gradeExam(items)
      const mapped = data.results.map(r => ({
        ...r,
        part: parts.find(p => p.id === r.exam_question_id),
      }))
      setResults(mapped)
      setView("results")
    } finally {
      setGrading(false)
    }
  }

  submitRef.current = handleSubmit

  if (loading) return (
    <div className="min-h-screen bg-gray-950 text-gray-500 flex items-center justify-center">Loading…</div>
  )

  if (grading) return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center gap-4">
      <div className="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
      <p className="text-gray-300 font-medium">Grading your exam with Gemini...</p>
      <p className="text-gray-500 text-sm">This can take a minute or two. Please don't close the tab.</p>
    </div>
  )

  // ── CARDS VIEW ───────────────────────────────────────────────────────────────
  if (view === "cards") {
    return (
      <div className="min-h-screen bg-gray-950 text-white">
        <nav className="border-b border-gray-800 px-6 py-4 flex items-center gap-4">
          <button onClick={() => navigate("/dashboard")} className="text-gray-400 hover:text-white text-sm">← Dashboard</button>
          <span className="text-gray-400 text-sm font-medium">Mock Exams</span>
        </nav>
        <div className="max-w-4xl mx-auto px-6 py-8">
          <p className="text-gray-500 text-sm mb-6">
            10 timed exams · Q1–Q4 with all sub-parts · 2 hours · AI graded on submission
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {cards.map(card => {
              const d = DIFF[card.difficulty] || DIFF.medium
              const totalMarks = card.groups.flatMap(g => g.parts).reduce((s, p) => s + p.marks, 0)
              return (
                <div key={card.id} className={`border ${d.border} rounded-xl p-5 flex flex-col gap-4 bg-gray-900/20`}>
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-white text-sm">{card.title}</span>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${d.badge}`}>{d.label}</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    {card.groups.map(g => (
                      <div key={g.slot} className="bg-gray-900 rounded-lg px-3 py-2">
                        <p className="text-xs text-gray-400 font-semibold">{g.slot} · {g.year}</p>
                        <p className="text-xs text-gray-600 mt-0.5">
                          {g.parts.map(p => p.exam_slot.slice(-1).toUpperCase()).join(" / ")} ·{" "}
                          {g.parts.reduce((s, p) => s + p.marks, 0)} marks
                        </p>
                      </div>
                    ))}
                  </div>
                  <div className="flex items-center justify-between text-xs text-gray-600">
                    <span>{totalMarks} total marks</span>
                    <span>2 hr time limit</span>
                  </div>
                  <button
                    onClick={() => startExam(card)}
                    className="bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium transition-colors"
                  >
                    Start Exam
                  </button>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    )
  }

  // ── EXAM VIEW ────────────────────────────────────────────────────────────────
  if (view === "exam") {
    const parts = allParts(selectedCard)
    const answeredCount = parts.filter(p => (answers[p.id] || "").trim()).length
    const totalMarks = parts.reduce((s, p) => s + p.marks, 0)
    const isLow = timeLeft < 600

    return (
      <div className="min-h-screen bg-gray-950 text-white">
        <nav className="sticky top-0 z-10 border-b border-gray-800 px-6 py-4 flex items-center justify-between bg-gray-950">
          <div className="flex items-center gap-3">
            <span className="font-semibold text-sm">{selectedCard.title}</span>
            <span className="text-xs text-gray-600">{totalMarks} marks · {answeredCount}/{parts.length} answered</span>
          </div>
          <div className="flex items-center gap-4">
            <span className={`font-mono text-sm tabular-nums ${isLow ? "text-red-400" : "text-gray-300"}`}>
              {formatTime(timeLeft)}
            </span>
            <button
              onClick={handleSubmit}
              disabled={grading}
              className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-5 py-2 rounded-lg text-sm font-medium transition-colors"
            >
              {grading ? "Grading... please wait" : "Submit Exam"}
            </button>
          </div>
        </nav>

        <div className="max-w-3xl mx-auto px-6 py-8 space-y-10">
          {selectedCard.groups.map((g, gi) => (
            <div key={g.slot}>
              <div className="flex items-center gap-3 mb-4">
                <h2 className="text-base font-semibold text-white">Question {gi + 1} ({g.slot})</h2>
                <span className="text-xs text-gray-500">{g.year} paper</span>
                <span className="text-xs text-gray-600 ml-auto">
                  {g.parts.reduce((s, p) => s + p.marks, 0)} marks total
                </span>
              </div>
              <div className="space-y-6">
                {g.parts.map((p, pi) => (
                  <div key={p.id} className="border border-gray-800 rounded-xl p-5">
                    <div className="flex items-center gap-3 mb-3">
                      <span className="text-xs font-mono bg-gray-800 text-gray-400 px-2 py-0.5 rounded">
                        {p.exam_slot}
                      </span>
                      <span className="text-xs text-gray-500">{p.marks} marks</span>
                    </div>
                    <p className="text-sm text-gray-200 leading-relaxed mb-4">{p.question_text}</p>
                    <textarea
                      value={answers[p.id] || ""}
                      onChange={e => setAnswers(a => ({ ...a, [p.id]: e.target.value }))}
                      placeholder="Write your answer here…"
                      className="w-full bg-gray-900 text-gray-200 text-sm rounded-lg p-4 border border-gray-700 focus:outline-none focus:border-blue-500 resize-none h-36 font-mono"
                    />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  // ── RESULTS VIEW ─────────────────────────────────────────────────────────────
  const totalScore = results.reduce((s, r) => s + (r.score ?? 0), 0)
  const maxScore = results.length * 10
  const pct = maxScore > 0 ? Math.round((totalScore / maxScore) * 100) : 0

  // group results back by Q slot
  const resultsBySlot = selectedCard.groups.map(g => ({
    slot: g.slot,
    year: g.year,
    parts: g.parts.map(p => results.find(r => r.exam_question_id === p.id)).filter(Boolean),
  }))

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center gap-4">
        <span className="text-gray-400 text-sm font-medium">Results — {selectedCard.title}</span>
      </nav>
      <div className="max-w-3xl mx-auto px-6 py-8">
        <div className="mb-10 text-center">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Overall Score</p>
          <span className={`text-6xl font-bold ${scoreColor(totalScore / (results.length || 1))}`}>
            {totalScore}/{maxScore}
          </span>
          <p className="text-gray-400 text-sm mt-2">{pct}% confidence · {selectedCard.title}</p>
        </div>

        <div className="space-y-8">
          {resultsBySlot.map((g, gi) => (
            <div key={g.slot}>
              <h3 className="text-sm font-semibold text-gray-300 mb-3">
                Question {gi + 1} ({g.slot}) · {g.year}
              </h3>
              <div className="space-y-4">
                {g.parts.map(r => (
                  <div key={r.exam_question_id} className="border border-gray-800 rounded-xl p-5">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-mono bg-gray-800 text-gray-400 px-2 py-0.5 rounded">
                        {r.part?.exam_slot}
                      </span>
                      <span className={`text-lg font-bold ${scoreColor(r.score)}`}>
                        {r.score !== null && r.score !== undefined ? `${r.score}/10` : "N/A"}
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 mb-2 line-clamp-1">{r.part?.question_text}</p>
                    <p className="text-sm text-gray-300 leading-relaxed">{r.feedback}</p>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-8 flex gap-3">
          <button
            onClick={() => setView("cards")}
            className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition-colors"
          >
            Try Another Exam
          </button>
          <button
            onClick={() => navigate("/dashboard")}
            className="border border-gray-700 hover:border-gray-500 text-gray-400 hover:text-white px-5 py-2.5 rounded-lg text-sm font-medium transition-colors"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  )
}
