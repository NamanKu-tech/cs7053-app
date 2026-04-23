// ─── NotebookLM Media ───────────────────────────────────────────────────────
// Replace null with your actual URLs once you have them from NotebookLM.

// YouTube embed URL, e.g. "https://www.youtube.com/embed/dQw4w9WgXcQ"
export const VIDEO_EMBED_URL = null

// NotebookLM audio overview — set to the direct .mp3/wav URL if you export it,
// OR a Spotify/Apple Podcasts embed src if you publish it there.
export const PODCAST_AUDIO_URL = null

// ─── Reference PDFs ─────────────────────────────────────────────────────────
// Files are served from /public/pdfs/ (Vite static assets).
export const REFERENCE_PDFS = [
  { id: "00", file: "00-quick-intro.pdf",           title: "00 – Quick Intro",             topic: "Overview" },
  { id: "01", file: "01-processes.pdf",              title: "01 – Security Processes",       topic: "Q1 — Risk Analysis" },
  { id: "02", file: "02-concepts.pdf",               title: "02 – Core Concepts",            topic: "Fundamentals" },
  { id: "03", file: "03-passwords.pdf",              title: "03 – Passwords",                topic: "Authentication" },
  { id: "04", file: "04-crypto.pdf",                 title: "04 – Cryptography",             topic: "Crypto" },
  { id: "05", file: "05-pqc.pdf",                    title: "05 – Post-Quantum Crypto",      topic: "Crypto" },
  { id: "06", file: "06-hpke.pdf",                   title: "06 – HPKE",                    topic: "Crypto" },
  { id: "07", file: "07-protocols.pdf",              title: "07 – Security Protocols",       topic: "Protocols" },
  { id: "08", file: "08-tls-problems.pdf",           title: "08 – TLS Problems",             topic: "Protocols" },
  { id: "09", file: "09-tls13.pdf",                  title: "09 – TLS 1.3",                 topic: "Protocols" },
  { id: "10", file: "10-dns.pdf",                    title: "10 – DNS Security",             topic: "DNS" },
  { id: "11", file: "11-legal.pdf",                  title: "11 – Legal & Privacy",          topic: "Legal / Privacy" },
  { id: "12", file: "12-censor.pdf",                 title: "12 – Censorship",               topic: "Censorship" },
  { id: "12s", file: "12-censor-short.pdf",          title: "12 – Censorship (short)",       topic: "Censorship" },
  { id: "priv", file: "Privacy Modern Concerns Slides.pdf", title: "Privacy – Modern Concerns", topic: "Legal / Privacy" },
]
