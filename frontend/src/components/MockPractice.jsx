import { useState, useEffect, useRef } from "react"
import { gradeAnswer, getAttempt, getHistory } from "../api/mock"

const SLIDE_MAP = {
  Q1: [
    { file: "01-processes.pdf",  title: "01 – Security Processes" },
  ],
  Q2: [
    { file: "07-protocols.pdf",  title: "07 – Security Protocols" },
    { file: "08-tls-problems.pdf", title: "08 – TLS Problems" },
    { file: "09-tls13.pdf",      title: "09 – TLS 1.3" },
    { file: "05-pqc.pdf",        title: "05 – Post-Quantum Crypto" },
  ],
  Q3: [
    { file: "02-concepts.pdf",   title: "02 – Core Concepts" },
    { file: "03-passwords.pdf",  title: "03 – Passwords" },
    { file: "04-crypto.pdf",     title: "04 – Cryptography" },
    { file: "06-hpke.pdf",       title: "06 – HPKE" },
  ],
  Q4: [
    { file: "10-dns.pdf",        title: "10 – DNS Security" },
    { file: "11-legal.pdf",      title: "11 – Legal & Privacy" },
  ],
}

function scoreColor(score) {
  if (score === null || score === undefined) return "text-gray-400"
  if (score >= 7) return "text-green-400"
  if (score >= 5) return "text-amber-400"
  return "text-red-400"
}

const TABS = ["Attempt", "Scores"]

export default function MockPractice({ questions, initialQuestion }) {
  const [selected, setSelected] = useState(initialQuestion || questions[0] || null)
  const [answer, setAnswer] = useState("")
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const [tab, setTab] = useState("Attempt")
  const pollRef = useRef(null)

  useEffect(() => { if (initialQuestion) setSelected(initialQuestion) }, [initialQuestion])

  useEffect(() => {
    if (!selected) return
    getHistory(selected.id).then(setHistory)
    setResult(null)
    setAnswer("")
    setSubmitted(false)
  }, [selected?.id])

  async function handleSubmit() {
    if (!selected || !answer.trim() || submitted) return
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

  function handleNewAttempt() {
    setAnswer("")
    setResult(null)
    setSubmitted(false)
  }

  if (questions.length === 0) return (
    <p className="text-gray-500 text-sm py-8 text-center">No questions available for practice yet.</p>
  )

  const attemptNumber = history.length + (submitted || result ? 0 : 1)

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <label className="text-xs text-gray-400 font-semibold uppercase tracking-wider block mb-2">Select Question</label>
        <select
          value={selected?.id || ""}
          onChange={e => setSelected(questions.find(q => q.id === parseInt(e.target.value)))}
          className="bg-gray-900 border border-gray-700 text-gray-200 text-sm rounded-lg px-3 py-2 w-full focus:outline-none focus:border-blue-500"
        >
          {questions.map(q => (
            <option key={q.id} value={q.id}>{q.year} · {q.exam_slot} · {q.marks} marks</option>
          ))}
        </select>
      </div>

      {selected && (
        <div className="space-y-3">
          <div className="bg-gray-900 rounded-lg p-4 border border-gray-800">
            <p className="text-xs text-gray-400 font-semibold uppercase tracking-wider mb-2">Question ({selected.marks} marks)</p>
            <p className="text-sm text-gray-200 leading-relaxed">{selected.question_text}</p>
          </div>
          {SLIDE_MAP[selected.exam_slot?.slice(0, 2)] && (
            <div className="bg-gray-900/50 rounded-lg p-3 border border-gray-800">
              <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Relevant Lecture Slides</p>
              <div className="flex flex-wrap gap-2">
                {SLIDE_MAP[selected.exam_slot?.slice(0, 2)].map(s => (
                  <a
                    key={s.file}
                    href={`/pdfs/${encodeURIComponent(s.file)}`}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-1.5 text-xs text-blue-400 hover:text-blue-300 bg-gray-800 hover:bg-gray-700 px-2.5 py-1.5 rounded-lg transition-colors"
                  >
                    📄 {s.title}
                  </a>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <div className="flex gap-1 border-b border-gray-800">
        {TABS.map(t => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px
              ${tab === t ? "border-blue-500 text-white" : "border-transparent text-gray-400 hover:text-gray-200"}`}>
            {t}
            {t === "Scores" && history.length > 0 && (
              <span className="ml-1.5 text-xs bg-gray-700 text-gray-300 px-1.5 py-0.5 rounded-full">{history.length}</span>
            )}
          </button>
        ))}
      </div>

      {tab === "Attempt" && (
        <div className="space-y-4">
          {result ? (
            <div className="space-y-4">
              <div className="bg-gray-900 rounded-lg p-4 border border-gray-700">
                {result.score !== null
                  ? <>
                      <div className="flex items-center gap-3 mb-3">
                        <span className={`text-2xl font-bold ${scoreColor(result.score)}`}>{result.score}/10</span>
                        <span className="text-xs text-gray-400">attempt {history.length}</span>
                      </div>
                      <p className="text-sm text-gray-300 leading-relaxed">{result.feedback}</p>
                    </>
                  : <p className="text-sm text-yellow-400">{result.feedback}</p>
                }
              </div>
              <button
                onClick={handleNewAttempt}
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg text-sm font-medium transition-colors"
              >
                Try Attempt {history.length + 1}
              </button>
            </div>
          ) : submitted ? (
            <div className="rounded-lg border border-amber-800/40 bg-amber-950/20 px-4 py-5 text-center space-y-1">
              <p className="text-sm text-amber-300 font-medium">Answer submitted</p>
              <p className="text-xs text-gray-400">Grading can take up to 10 minutes. You can navigate away — your result will appear here when ready.</p>
            </div>
          ) : (
            <>
              <div>
                <label className="text-xs text-gray-400 font-semibold uppercase tracking-wider block mb-2">
                  Your Answer {history.length > 0 && `· Attempt ${history.length + 1}`}
                </label>
                <textarea
                  value={answer}
                  onChange={e => setAnswer(e.target.value)}
                  placeholder="Write your exam answer here..."
                  className="w-full bg-gray-900 text-gray-200 text-sm rounded-lg p-4 border border-gray-800 focus:outline-none focus:border-blue-500 resize-none h-48 font-mono"
                />
              </div>
              <button
                onClick={handleSubmit}
                disabled={loading || !answer.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-6 py-2.5 rounded-lg text-sm font-medium transition-colors"
              >
                {loading ? "Submitting..." : "Submit for Grading"}
              </button>
            </>
          )}
        </div>
      )}

      {tab === "Scores" && (
        <div>
          {history.length === 0
            ? <p className="text-gray-500 text-sm text-center py-8">No attempts yet.</p>
            : <div className="space-y-2">
                {history.map((a, i) => (
                  <div key={a.id} className="bg-gray-900 rounded-lg p-4 border border-gray-800">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs text-gray-500">Attempt {i + 1} · {new Date(a.attempted_at).toLocaleDateString()}</span>
                      <span className={`text-lg font-bold ${scoreColor(a.score)}`}>
                        {a.score !== null ? `${a.score}/10` : "Pending"}
                      </span>
                    </div>
                    {a.feedback && <p className="text-xs text-gray-400 leading-relaxed">{a.feedback}</p>}
                  </div>
                ))}
              </div>
          }
        </div>
      )}
    </div>
  )
}
