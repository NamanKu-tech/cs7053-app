import { useEffect, useState } from "react"
import { useParams, useNavigate, useSearchParams } from "react-router-dom"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { getPathTopics, getPathOverview } from "../api/paths"
import TopicRow from "../components/TopicRow"
import MockPractice from "../components/MockPractice"

const PATH_TABS = ["Overview", "Mock Practice"]

const SLIDE_MAP = {
  "q1-risk-analysis": [
    { file: "01-processes.pdf", title: "01 – Security Processes" },
  ],
  "q2-tls-protocols": [
    { file: "07-protocols.pdf",   title: "07 – Security Protocols" },
    { file: "08-tls-problems.pdf", title: "08 – TLS Problems" },
    { file: "09-tls13.pdf",       title: "09 – TLS 1.3" },
    { file: "05-pqc.pdf",         title: "05 – Post-Quantum Crypto" },
  ],
  "q3-system-design": [
    { file: "02-concepts.pdf",  title: "02 – Core Concepts" },
    { file: "03-passwords.pdf", title: "03 – Passwords" },
    { file: "04-crypto.pdf",    title: "04 – Cryptography" },
    { file: "06-hpke.pdf",      title: "06 – HPKE" },
  ],
  "q4-dns-dnssec": [
    { file: "10-dns.pdf",    title: "10 – DNS Security" },
    { file: "11-legal.pdf",  title: "11 – Legal & Privacy" },
  ],
}

function ExamQuestion({ q, defaultOpen }) {
  const [open, setOpen] = useState(defaultOpen || false)
  const [showAnswer, setShowAnswer] = useState(false)

  return (
    <div className="border border-gray-800 rounded-lg overflow-hidden">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-gray-900 transition-colors"
      >
        <div className="flex items-center gap-3">
          <span className="text-xs font-mono bg-gray-800 text-gray-400 px-2 py-0.5 rounded">{q.exam_slot}</span>
          <span className="text-sm text-gray-300 line-clamp-1">{q.question_text}</span>
        </div>
        <div className="flex items-center gap-2 shrink-0 ml-4">
          <span className="text-xs text-gray-600">{q.marks}m</span>
          <span className="text-gray-600 text-xs">{open ? "▲" : "▼"}</span>
        </div>
      </button>
      {open && (
        <div className="px-4 pb-4 border-t border-gray-800 bg-gray-950">
          <p className="text-sm text-gray-200 mt-3 leading-relaxed">{q.question_text}</p>
          <button
            onClick={() => setShowAnswer(a => !a)}
            className="mt-3 text-xs text-blue-400 hover:text-blue-300 underline"
          >
            {showAnswer ? "Hide sample answer" : "Show sample answer"}
          </button>
          {showAnswer && (
            <div className="mt-2 text-sm text-gray-400 leading-relaxed border-l-2 border-gray-700 pl-3 whitespace-pre-wrap">
              {q.sample_answer}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function ExamSection({ overview, slug }) {
  const [overviewOpen, setOverviewOpen] = useState(false)
  const [selectedYear, setSelectedYear] = useState(null)

  const years = [...new Set(overview.exam_questions.map(q => q.year))].sort((a, b) => b - a)

  useEffect(() => {
    if (years.length > 0 && selectedYear === null) setSelectedYear(years[0])
  }, [years.length])

  const filtered = selectedYear
    ? overview.exam_questions.filter(q => q.year === selectedYear)
    : overview.exam_questions

  return (
    <div className="mb-8">
      {overview.overview && (
        <div className="mb-4 border border-gray-800 rounded-xl overflow-hidden">
          <button
            onClick={() => setOverviewOpen(o => !o)}
            className="w-full flex items-center justify-between px-5 py-3.5 text-left hover:bg-gray-900 transition-colors"
          >
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-white">How to approach this question</span>
              <span className="text-xs text-gray-500">— strategy, template, common traps</span>
            </div>
            <span className="text-gray-500 text-xs">{overviewOpen ? "▲" : "▼"}</span>
          </button>
          {overviewOpen && (
            <div className="border-t border-gray-800 px-5 py-4 bg-gray-950 prose prose-invert prose-sm max-w-none overflow-auto max-h-[70vh]">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{overview.overview}</ReactMarkdown>
            </div>
          )}
        </div>
      )}

      {SLIDE_MAP[slug]?.length > 0 && (
        <div className="mb-4 p-3 rounded-lg border border-gray-800 bg-gray-900/40">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-2">Lecture Slides</p>
          <div className="flex flex-wrap gap-2">
            {SLIDE_MAP[slug].map(s => (
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

      <div className="flex items-center justify-between mb-3">
        <h2 className="text-sm font-semibold text-gray-300">Past Exam Questions</h2>
        <div className="flex gap-1 flex-wrap justify-end">
          {years.map(y => (
            <button
              key={y}
              onClick={() => setSelectedYear(y === selectedYear ? null : y)}
              className={`px-2.5 py-1 text-xs rounded-md font-medium transition-colors
                ${selectedYear === y
                  ? "bg-blue-600 text-white"
                  : "bg-gray-800 text-gray-400 hover:text-gray-200"
                }`}
            >
              {y}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-2">
        {filtered.map(q => (
          <ExamQuestion key={q.id} q={q} defaultOpen={filtered.length === 1} />
        ))}
        {filtered.length === 0 && (
          <p className="text-sm text-gray-600 text-center py-6">No questions for this year.</p>
        )}
      </div>
    </div>
  )
}

export default function Path() {
  const { slug } = useParams()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const [tab, setTab] = useState(searchParams.get("tab") === "mock" ? "Mock Practice" : "Overview")
  const [topics, setTopics] = useState([])
  const [overview, setOverview] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    Promise.all([getPathTopics(slug), getPathOverview(slug)])
      .then(([t, ov]) => { setTopics(t); setOverview(ov) })
      .finally(() => setLoading(false))
  }, [slug])

  function handleToggle(topicSlug, completed) {
    setTopics(ts => ts.map(t => t.slug === topicSlug ? { ...t, completed } : t))
  }

  const completed = topics.filter(t => t.completed).length
  const pct = topics.length > 0 ? Math.round((completed / topics.length) * 100) : 0

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center gap-4">
        <button onClick={() => navigate("/dashboard")} className="text-gray-400 hover:text-white text-sm">← Dashboard</button>
        <span className="text-gray-600">/</span>
        <span className="text-sm text-gray-300 capitalize">{slug.replace(/-/g, " ")}</span>
        <div className="ml-auto flex items-center gap-3">
          <span className="text-sm text-gray-400">{completed}/{topics.length}</span>
          <div className="w-24 bg-gray-800 rounded-full h-1.5">
            <div className="h-1.5 rounded-full bg-blue-500 transition-all" style={{ width: `${pct}%` }} />
          </div>
        </div>
      </nav>
      <div className="max-w-2xl mx-auto px-6 py-6">
        <div className="flex gap-1 mb-6 border-b border-gray-800">
          {PATH_TABS.map(t => (
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
              <div className={tab === "Overview" ? "" : "hidden"}>
                {overview && <ExamSection overview={overview} slug={slug} />}
                <h2 className="text-sm font-semibold text-gray-300 mb-3">Topics</h2>
                <div className="space-y-1">
                  {topics.map(t => <TopicRow key={t.slug} topic={t} onToggle={handleToggle} />)}
                </div>
              </div>
              <div className={tab === "Mock Practice" ? "" : "hidden"}>
                <MockPractice questions={overview?.exam_questions ?? []} />
              </div>
            </>
        }
      </div>
    </div>
  )
}
