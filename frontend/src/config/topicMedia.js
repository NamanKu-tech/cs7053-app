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
  "tls13-handshake":    { videoUrl: `${MEDIA}/materials/Unpacking%20TLS%201.mp4`,                     audioUrl: `${MEDIA}/materials/Why_Standard_Primes_and_Firewalls_Fail.m4a` },
  "tls13-key-schedule": { videoUrl: `${MEDIA}/materials/Unlocking%20TLS%201.mp4`,                     audioUrl: `${MEDIA}/materials/The%20TLS%201.m4a` },
  "tls13-record-layer": { videoUrl: `${MEDIA}/materials/TLS%20Video%201.mp4`,                          audioUrl: `${MEDIA}/materials/TLS%201.m4a` },
  "forward-secrecy":    { videoUrl: `${MEDIA}/materials/Forward%20Secrecy%20in%20TLS.mp4`,            audioUrl: `${MEDIA}/materials/TLS%20Audio%201.m4a` },
  "tls-attacks":        { videoUrl: `${MEDIA}/materials/Attacks%20on%20TLS.mp4`,                      audioUrl: `${MEDIA}/materials/Anatomy%20of%20BEAST%20Crime%20Heartbleed%20DROWN.m4a` },
  "tls-dos":            { videoUrl: `${MEDIA}/materials/Defending_TLS__The_DoS_Threat.mp4`,           audioUrl: `${MEDIA}/materials/Why_security_tools_break_your_encryption.m4a` },
  "pqc-tls":            { videoUrl: `${MEDIA}/materials/Securing%20TLS%20for%20Quantum%20Future.mp4`, audioUrl: `${MEDIA}/materials/Securing%20TLS%20Against%20Quantum%20Computers.m4a` },
  "large-scale-tls":    { videoUrl: `${MEDIA}/materials/TLS%20at%20Scale%20The%20Real%20World.mp4`,   audioUrl: null },

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
