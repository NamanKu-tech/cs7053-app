import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import client from "../api/client"

export default function Cheatsheet() {
  const [content, setContent] = useState("")
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    client.get("/cheatsheet").then(r => setContent(r.data.content)).finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center justify-between sticky top-0 bg-gray-950 z-10">
        <button onClick={() => navigate("/dashboard")} className="text-gray-400 hover:text-white text-sm">← Dashboard</button>
        <span className="font-bold text-lg">Exam Cheat Sheet</span>
        <span />
      </nav>

      <div className="max-w-4xl mx-auto px-6 py-10">
        {loading
          ? <div className="text-gray-500 text-center py-20">Loading...</div>
          : (
            <div className="prose prose-invert prose-sm max-w-none
              prose-headings:text-white prose-headings:font-semibold
              prose-h1:text-2xl prose-h1:border-b prose-h1:border-gray-700 prose-h1:pb-3 prose-h1:mb-6
              prose-h2:text-xl prose-h2:text-blue-300 prose-h2:mt-10 prose-h2:mb-4
              prose-h3:text-base prose-h3:text-gray-200 prose-h3:mt-6 prose-h3:mb-2
              prose-p:text-gray-300 prose-p:leading-relaxed
              prose-a:text-blue-400 prose-a:no-underline hover:prose-a:underline
              prose-strong:text-white
              prose-code:text-green-300 prose-code:bg-gray-800 prose-code:px-1 prose-code:rounded prose-code:text-xs
              prose-pre:bg-gray-900 prose-pre:border prose-pre:border-gray-700 prose-pre:rounded-xl prose-pre:text-xs
              prose-blockquote:border-blue-600 prose-blockquote:text-gray-400
              prose-table:text-sm prose-thead:bg-gray-800
              prose-th:text-gray-200 prose-th:px-3 prose-th:py-2
              prose-td:text-gray-300 prose-td:px-3 prose-td:py-2 prose-td:border-gray-700
              prose-tr:border-gray-700
              prose-li:text-gray-300 prose-li:marker:text-gray-500
              prose-hr:border-gray-700">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
            </div>
          )
        }
      </div>
    </div>
  )
}
