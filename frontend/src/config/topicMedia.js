// Per-topic video and podcast configuration.
// videos    — array of { url, title }; url can be YouTube embed URL or relative path "/materials/file.mp4"
// audioUrl  — Relative path to audio file: "/materials/file.m4a"
// Leave videos as [] or audioUrl as null to hide that media section.

const MEDIA = import.meta.env.VITE_MEDIA_BASE ?? ""

export const TOPIC_MEDIA = {
  // ── Q1: Risk Analysis ────────────────────────────────────────────────────
  "risk-analysis-process":    { videos: [{ url: `${MEDIA}/materials/Mastering%20Risk%20Analysis.mp4`,        title: "Mastering Risk Analysis" }],        audioUrl: `${MEDIA}/materials/Episode%201.m4a` },
  "identifying-assets":       { videos: [{ url: `${MEDIA}/materials/Constructing%20the%20Attack%20Surface.mp4`, title: "Constructing the Attack Surface" }], audioUrl: `${MEDIA}/materials/Episode%202.m4a` },
  "classifying-risks":        { videos: [{ url: `${MEDIA}/materials/Classifying%20Risks.mp4`,                title: "Classifying Risks" }],                audioUrl: `${MEDIA}/materials/Episode%203.m4a` },
  "mitigations":              { videos: [{ url: `${MEDIA}/materials/Designing%20Mitigations.mp4`,            title: "Designing Mitigations" }],            audioUrl: `${MEDIA}/materials/Episode%204.m4a` },
  "privacy-threats":          { videos: [{ url: `${MEDIA}/materials/Internet%20Privacy%20Threats.mp4`,       title: "Internet Privacy Threats" }],         audioUrl: `${MEDIA}/materials/Episode%205.m4a` },
  "security-processes":       { videos: [{ url: `${MEDIA}/materials/Security%20and%20the%20SDLC.mp4`,        title: "Security and the SDLC" }],            audioUrl: `${MEDIA}/materials/Episode%206.m4a` },
  "real-incidents":           { videos: [{ url: `${MEDIA}/materials/Real%20Incidents.mp4`,                   title: "Real Incidents" }],                   audioUrl: `${MEDIA}/materials/Episode%207.m4a` },

  // ── Q2: TLS / Protocols ───────────────────────────────────────────────────
  "tls13-handshake":    { videos: [
                            { url: `${MEDIA}/materials/Unpacking%20TLS%201.mp4`,       title: "Unpacking TLS 1.3" },
                            { url: "https://www.youtube.com/embed/0TLDTodL7Lc",        title: "What is TLS/SSL?" },
                            { url: "https://www.youtube.com/embed/86cQJ0MMses",         title: "TLS Handshake" },
                            { url: "https://www.youtube.com/embed/s22eJ1eVLTU",         title: "What are Digital Signatures?" },
                          ], audioUrl: `${MEDIA}/materials/TLS_1.3.m4a` },
  "tls13-key-schedule": { videos: [{ url: `${MEDIA}/materials/Unlocking%20TLS%201.mp4`,                     title: "Unlocking TLS 1.3" }],              audioUrl: `${MEDIA}/materials/The%20TLS%201.m4a` },
  "tls13-record-layer": { videos: [{ url: `${MEDIA}/materials/TLS%20Video%201.mp4`,                          title: "TLS Record Layer" }],               audioUrl: `${MEDIA}/materials/TLS%201.m4a` },
  "forward-secrecy":    { videos: [
                            { url: `${MEDIA}/materials/Forward%20Secrecy%20in%20TLS.mp4`, title: "Forward Secrecy in TLS" },
                            { url: "https://www.youtube.com/embed/NmM9HA2MQGI",           title: "Diffie-Hellman" },
                          ], audioUrl: `${MEDIA}/materials/TLS%20Audio%201.m4a` },
  "tls-attacks":        { videos: [{ url: `${MEDIA}/materials/Attacks%20on%20TLS.mp4`,                      title: "Attacks on TLS" }],                 audioUrl: `${MEDIA}/materials/Anatomy%20of%20BEAST%20Crime%20Heartbleed%20DROWN.m4a` },
  "tls-dos":            { videos: [{ url: `${MEDIA}/materials/Defending_TLS__The_DoS_Threat.mp4`,           title: "Defending TLS: The DoS Threat" }],  audioUrl: `${MEDIA}/materials/Why_security_tools_break_your_encryption.m4a` },
  "pqc-tls":            { videos: [{ url: `${MEDIA}/materials/Securing%20TLS%20for%20Quantum%20Future.mp4`, title: "Securing TLS for Quantum Future" }], audioUrl: `${MEDIA}/materials/Securing%20TLS%20Against%20Quantum%20Computers.m4a` },
  "large-scale-tls":    { videos: [{ url: `${MEDIA}/materials/TLS%20at%20Scale%20The%20Real%20World.mp4`,   title: "TLS at Scale" }],                   audioUrl: null },

  // ── Q3: System Design ─────────────────────────────────────────────────────
  "security-requirements":    { videos: [], audioUrl: null },
  "architecture-patterns":    { videos: [], audioUrl: null },
  "authn-authz":              { videos: [{ url: "https://www.youtube.com/embed/qW361k3-BtU", title: "Taming Kerberos" }], audioUrl: null },
  "crypto-in-systems":        { videos: [
                            { url: "https://www.youtube.com/embed/O4xNJsjtN6E", title: "AES Explained" },
                            { url: "https://www.youtube.com/embed/vsXMMT2CqqE", title: "RSA" },
                            { url: "https://www.youtube.com/embed/GSIDS_lvRv4", title: "Public Key Cryptography" },
                            { url: "https://www.youtube.com/embed/wlSG3pEiQdc", title: "HMAC" },
                            { url: "https://www.youtube.com/embed/s22eJ1eVLTU", title: "What are Digital Signatures?" },
                            { url: "https://www.youtube.com/embed/DMtFhACPnTY", title: "SHA" },
                          ], audioUrl: null },
  "audit-logging":            { videos: [], audioUrl: null },
  "attack-the-system":        { videos: [], audioUrl: null },

  // ── Q4: DNS / DNSSEC ──────────────────────────────────────────────────────
  "dns-basics":               { videos: [], audioUrl: null },
  "dnssec-records":           { videos: [], audioUrl: null },
  "dnssec-key-hierarchy":     { videos: [], audioUrl: null },
  "dnssec-validation":        { videos: [], audioUrl: null },
  "doh-dot-privacy":          { videos: [], audioUrl: null },
  "email-security":           { videos: [], audioUrl: null },
}
