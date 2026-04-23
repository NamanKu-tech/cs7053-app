// Per-topic video and podcast configuration.
// videoUrl  — YouTube embed URL or relative path: "/materials/file.mp4"
// audioUrl  — Relative path to audio file: "/materials/file.m4a"
// Leave as null to hide the media section for that topic.

const MEDIA = import.meta.env.VITE_MEDIA_BASE ?? ""

export const TOPIC_MEDIA = {
  // ── Q1: Risk Analysis ────────────────────────────────────────────────────
  "risk-analysis-process":    { videoUrl: `${MEDIA}/materials/Mastering%20Risk%20Analysis.mp4`,        audioUrl: `${MEDIA}/materials/Episode%201.m4a` },
  "identifying-assets":       { videoUrl: `${MEDIA}/materials/Constructing%20the%20Attack%20Surface.mp4`, audioUrl: `${MEDIA}/materials/Episode%202.m4a` },
  "classifying-risks":        { videoUrl: `${MEDIA}/materials/Classifying%20Risks.mp4`,                audioUrl: `${MEDIA}/materials/Episode%203.m4a` },
  "mitigations":              { videoUrl: `${MEDIA}/materials/Designing%20Mitigations.mp4`,            audioUrl: `${MEDIA}/materials/Episode%204.m4a` },
  "privacy-threats":          { videoUrl: `${MEDIA}/materials/Internet%20Privacy%20Threats.mp4`,       audioUrl: `${MEDIA}/materials/Episode%205.m4a` },
  "security-processes":       { videoUrl: `${MEDIA}/materials/Security%20and%20the%20SDLC.mp4`,        audioUrl: `${MEDIA}/materials/Episode%206.m4a` },
  "real-incidents":           { videoUrl: `${MEDIA}/materials/Real%20Incidents.mp4`,                   audioUrl: `${MEDIA}/materials/Episode%207.m4a` },

  // ── Q2: TLS / Protocols ───────────────────────────────────────────────────
  "tls13-handshake":          { videoUrl: null, audioUrl: null },
  "tls13-key-schedule":       { videoUrl: null, audioUrl: null },
  "tls13-record-layer":       { videoUrl: null, audioUrl: null },
  "forward-secrecy":          { videoUrl: null, audioUrl: null },
  "tls-attacks":              { videoUrl: null, audioUrl: null },
  "tls-dos":                  { videoUrl: null, audioUrl: null },
  "pqc-tls":                  { videoUrl: null, audioUrl: null },
  "large-scale-tls":          { videoUrl: null, audioUrl: null },

  // ── Q3: System Design ─────────────────────────────────────────────────────
  "security-requirements":    { videoUrl: null, audioUrl: null },
  "architecture-patterns":    { videoUrl: null, audioUrl: null },
  "authn-authz":              { videoUrl: null, audioUrl: null },
  "crypto-in-systems":        { videoUrl: null, audioUrl: null },
  "audit-logging":            { videoUrl: null, audioUrl: null },
  "attack-the-system":        { videoUrl: null, audioUrl: null },

  // ── Q4: DNS / DNSSEC ──────────────────────────────────────────────────────
  "dns-basics":               { videoUrl: null, audioUrl: null },
  "dnssec-records":           { videoUrl: null, audioUrl: null },
  "dnssec-key-hierarchy":     { videoUrl: null, audioUrl: null },
  "dnssec-validation":        { videoUrl: null, audioUrl: null },
  "doh-dot-privacy":          { videoUrl: null, audioUrl: null },
  "email-security":           { videoUrl: null, audioUrl: null },
}
