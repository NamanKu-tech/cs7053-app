import { useState } from "react"
import { useNavigate } from "react-router-dom"

const RFCS = [
  // ── Tier 1: Must know ───────────────────────────────────────────────────────
  {
    id: 8446, tier: 1, category: "TLS",
    title: "TLS 1.3",
    what: "The complete TLS 1.3 spec. 1-RTT handshake, mandatory forward secrecy, AEAD-only, encrypted extensions. Appendices C/D/E cover implementation, backward compat, and security analysis.",
    mnemonic: "8-4-4-6 → say it until it's muscle memory. This is the #1 cited RFC in the course. Every Q2 answer needs it.",
  },
  {
    id: 6973, tier: 1, category: "Privacy",
    title: "Privacy Considerations for Internet Protocols",
    what: "Defines the 7 privacy threat categories used directly in Q1c: Surveillance, Stored Data Exposure, Aggregation, Correlation, Secondary Use, Exclusion, Identification.",
    mnemonic: "6973 = '69' (intimate/private) + 73. The 7 threats: SACISSE — Surveillance, Aggregation, Correlation, Identification, Stored data, Secondary use, Exclusion.",
  },
  {
    id: 7258, tier: 1, category: "Privacy",
    title: "Pervasive Monitoring is an Attack",
    what: "Farrell co-authored. Declares mass passive surveillance a protocol-level attack class. Changed IETF policy: all new RFCs must consider pervasive monitoring.",
    mnemonic: "7258 = Snowden (2013). 7+2+5+8=22 → two-two → Farrell co-authored with two co-authors. 'Snooping = attack' in 4 words.",
  },
  {
    id: 1035, tier: 1, category: "DNS",
    title: "DNS — Implementation and Specification",
    what: "The DNS wire format: query/response structure, resource record types (A, AAAA, MX, NS, CNAME, PTR, TXT, SOA), UDP/TCP port 53, message compression.",
    mnemonic: "1035 follows 1034. Think: 1034 = WHAT is DNS, 1035 = HOW DNS works on the wire. 1-0-3-5 = 'one-oh-three-five, DNS is alive'.",
  },
  {
    id: 1034, tier: 1, category: "DNS",
    title: "DNS — Concepts and Facilities",
    what: "DNS architecture: namespace hierarchy, zones, authoritative vs recursive resolvers, iterative resolution algorithm, TTL caching, the delegation model.",
    mnemonic: "1034 = the first DNS RFC. Low number = foundational. 'One-oh-three-four, DNS at the core'. Pair with 1035.",
  },
  {
    id: 4034, tier: 1, category: "DNS",
    title: "DNSSEC Resource Records",
    what: "Defines DNSKEY (public keys), RRSIG (signatures over RRsets), DS (delegation signer — hash of child KSK in parent), NSEC (authenticated denial). The exam reference for DNSSEC record structure.",
    mnemonic: "4034 = middle of the DNSSEC triple: 4033 (intro) → 4034 (records) → 4035 (protocol). '4034 = four records: DNSKEY, RRSIG, DS, NSEC'.",
  },
  {
    id: 5869, tier: 1, category: "Crypto",
    title: "HKDF — HMAC-based Key Derivation Function",
    what: "Defines HKDF-Extract (mix entropy into a PRK) and HKDF-Expand (stretch PRK into key material). Used throughout TLS 1.3 key schedule, Signal, Noise Protocol.",
    mnemonic: "5869 = H-K-D-F. Count letters: H=8th, K=11th, D=4th, F=6th → 8-11-4-6 ≈ 8446 (TLS 1.3). HKDF lives inside TLS 1.3.",
  },
  {
    id: 7208, tier: 1, category: "Email",
    title: "SPF — Sender Policy Framework",
    what: "TXT record listing IPs authorised to send email for a domain. Receiving MTA checks envelope MAIL FROM against SPF record. `-all` = reject if not listed. Breaks on forwarding.",
    mnemonic: "7208 = SPF. S=19, P=16, F=6 → nope. Try: '7208 = Seven-Two-Oh-Eight = SPF is the first email auth layer'. SPF came first historically.",
  },
  {
    id: 6376, tier: 1, category: "Email",
    title: "DKIM — DomainKeys Identified Mail",
    what: "Mail server signs selected headers + body with a private key. Public key in DNS at `selector._domainkey.domain`. Survives forwarding (unlike SPF). Doesn't specify what to do on failure.",
    mnemonic: "6376 = DKIM. 63 = ASCII '?', 76 = 'L' → DKIM signs the Letter content. Or: 6+3+7+6=22 = DKIM has 2 components: signing + DNS key.",
  },
  {
    id: 7489, tier: 1, category: "Email",
    title: "DMARC — Domain-based Message Auth, Reporting and Conformance",
    what: "Policy on SPF/DKIM failure: none/quarantine/reject. Alignment: From: header must match SPF/DKIM domain. Aggregate reports (rua=) for monitoring. Ties SPF + DKIM together with a policy.",
    mnemonic: "7489 = DMARC. 7+4=11, 8+9=17 → DMARC is the 3rd layer (SPF→DKIM→DMARC). 'D=Decides what happens when SPF or DKIM fails'.",
  },
  {
    id: 7858, tier: 1, category: "DNS",
    title: "DNS over TLS (DoT)",
    what: "Encrypts DNS queries using TLS on port 853. Distinguishable by port — easy for enterprises to monitor/block. Supported by Android Private DNS, Unbound, Knot Resolver.",
    mnemonic: "7858 = DoT. 7+8=15, 5+8=13 → port 853 (8-5-3). DoT runs on port 853. '7858 → 853 → DoT'. DNS over **T**LS = **T**CP port 853.",
  },
  {
    id: 8484, tier: 1, category: "DNS",
    title: "DNS over HTTPS (DoH)",
    what: "DNS inside HTTPS POST/GET on port 443. Indistinguishable from web traffic — hard to block. Browser-native (Firefox, Chrome). Centralises DNS in large providers. Breaks enterprise filtering.",
    mnemonic: "8484 = DoH. 84-84 = repeating pair → DoH uses the same port (443) as HTTPS, blending in. '8484 = DNS hiding in HTTPS'.",
  },
  {
    id: 9162, tier: 1, category: "TLS",
    title: "Certificate Transparency 2.0",
    what: "Append-only public logs of all issued TLS certificates. CAs submit certs → logs return SCTs. Browsers require SCTs. Allows domain owners to detect unauthorised certificates.",
    mnemonic: "9162 = CT. 9+1=10, 6+2=8 → 10 and 8 → transparency. Or: '9162 = nine-one-six-two = CT logs are the 911 for rogue certificates'.",
  },

  // ── Tier 2: Important ────────────────────────────────────────────────────────
  {
    id: 5246, tier: 2, category: "TLS",
    title: "TLS 1.2",
    what: "Predecessor to TLS 1.3. Key differences: 2-RTT handshake, optional forward secrecy (static RSA allowed), MAC-then-encrypt, negotiable cipher suites including weak ones.",
    mnemonic: "5246 = TLS 1.2. '52' = poker deck (52 cards = complexity of TLS 1.2). Lower than 8446 → older spec. Know it to contrast with TLS 1.3.",
  },
  {
    id: 7457, tier: 2, category: "TLS",
    title: "Summary of Known TLS/DTLS Attacks",
    what: "Catalogue of every major TLS attack: BEAST, CRIME, TIME, BREACH, Lucky13, POODLE, DROWN, Logjam, FREAK, Heartbleed. Each with root cause and mitigation. Use as Q2 revision list.",
    mnemonic: "7457 = attack list. 7+4+5+7=23 → 23 known attack variants. '7457 = Seven-Four-Five-Seven = BEAST CRIME POODLE DROWN (4 famous attacks)'.",
  },
  {
    id: 5116, tier: 2, category: "Crypto",
    title: "An Interface and Algorithms for Authenticated Encryption (AEAD)",
    what: "Defines the standard AEAD interface: encrypt-then-MAC, 16-byte authentication tag, nonce requirements. TLS 1.3 mandates AEAD — this is the spec behind that decision.",
    mnemonic: "5116 = AEAD. The **16** in 5116 = the 16-byte authentication tag that AEADs produce. '5-1-16 = five-one-sixteen = the sixteen-byte tag'.",
  },
  {
    id: 8439, tier: 2, category: "Crypto",
    title: "ChaCha20 and Poly1305 for IETF Protocols",
    what: "Stream cipher (ChaCha20) + MAC (Poly1305) = ChaCha20-Poly1305 AEAD. Used in TLS 1.3, WireGuard, SSH. Preferred on devices without AES hardware acceleration (mobile, IoT).",
    mnemonic: "8439 = ChaCha20-Poly1305. '8439 = eighty-four-thirty-nine = 20+19=39, Poly1305 ends in 05'. Or: 8+4=12 = ChaCha has 12 rounds per block.",
  },
  {
    id: 4033, tier: 2, category: "DNS",
    title: "DNSSEC Introduction and Requirements",
    what: "Overview of DNSSEC: why plain DNS is unauthenticated, the chain of trust model, trust anchor concept, what DNSSEC does (integrity + auth) and does NOT do (privacy).",
    mnemonic: "4033 = DNSSEC overview. The DNSSEC triple starts here: 4033 (WHY) → 4034 (RECORDS) → 4035 (HOW). '4033 = four-oh-three-three = first of the DNSSEC trio'.",
  },
  {
    id: 4035, tier: 2, category: "DNS",
    title: "DNSSEC Protocol Modifications",
    what: "The validation algorithm: trust anchor → DS → DNSKEY → RRSIG verification. The AD flag (Authentic Data). SERVFAIL on validation failure. How resolvers walk the chain.",
    mnemonic: "4035 = DNSSEC validation. Third of the 4033/4034/4035 trio. '4035 = four-oh-three-five = the five-step validation chain'.",
  },
  {
    id: 5155, tier: 2, category: "DNS",
    title: "NSEC3 — Hashed Authenticated Denial of Existence",
    what: "Improvement over NSEC: hashes domain names in the denial-of-existence chain, preventing zone walking (enumerating all domain names in a zone by following NSEC records).",
    mnemonic: "5155 = NSEC3. The '3' in NSEC3 = 3rd record type in DNSSEC. 5155: '51 = hashed, 55 = denial × denial = authenticated denial'.",
  },
  {
    id: 2104, tier: 2, category: "Crypto",
    title: "HMAC: Keyed-Hashing for Message Authentication",
    what: "HMAC construction: H((K⊕opad) || H((K⊕ipad) || message)). Two keys (inner/outer pad), any hash function. Security proof. Foundation of HKDF and TLS 1.3 key schedule.",
    mnemonic: "2104 = HMAC. 21 = two pads (ipad + opad), 04 = XOR (⊕ symbol looks like 0 with a +). 'Two-one-oh-four = two pads, one hash, four letters: HMAC'.",
  },
  {
    id: 3552, tier: 2, category: "General",
    title: "Guidelines for Writing RFC Security Considerations",
    what: "The mandatory security analysis template every RFC must pass. Defines attacker model: passive eavesdropper, active MITM, replay, insider. Asset categories: confidentiality, integrity, availability.",
    mnemonic: "3552 = Security Considerations. 35 = 3 attacker types (passive, active, insider), 52 = 52 considerations. 'Three-five-five-two = security checklist'.",
  },
  {
    id: 6698, tier: 2, category: "DNS",
    title: "DANE — DNS-based Authentication of Named Entities",
    what: "TLSA DNS records to pin a TLS certificate/key using DNSSEC as the trust anchor instead of WebPKI CAs. Prevents rogue CA misissuance. Widely used for SMTP, limited HTTPS browser support.",
    mnemonic: "6698 = DANE. 66 = double trust (DNSSEC + certificate), 98 = year WebPKI trust model was established. 'DANE replaces CA trust with DNS trust'.",
  },
  {
    id: 8555, tier: 2, category: "TLS",
    title: "ACME — Automatic Certificate Management Environment",
    what: "Protocol behind Let's Encrypt. Domain validation (HTTP-01, DNS-01 challenges), automated issuance and renewal. How TLS certificates can be free and auto-renewed.",
    mnemonic: "8555 = ACME. 8+5+5+5=23 → ACME automates the 23-step manual certificate process. '8555 = Automatic Certificate Machine, Every day'.",
  },
  {
    id: 6520, tier: 2, category: "TLS",
    title: "TLS/DTLS Heartbeat Extension",
    what: "Keep-alive mechanism: send a payload, receive it echoed back. The Heartbleed bug (CVE-2014-0160) was in OpenSSL's implementation — it trusted the user-supplied length without bounds-checking.",
    mnemonic: "6520 = Heartbeat = Heartbleed. 65 = the age your heart gives out, 20 = 2014 (Heartbleed year, close enough). '6520 = the RFC with the heart that bled'.",
  },
  {
    id: 5280, tier: 2, category: "TLS",
    title: "X.509 PKI Certificate and CRL Profile",
    what: "The X.509 certificate format: Subject, Subject Alternative Name (SAN), validity period, key usage, extended key usage, AIA, OCSP endpoints. Foundation for all HTTPS certificates.",
    mnemonic: "5280 = X.509. 52 = 52 fields in a cert (roughly), 80 = v80 of PKI. Or: '5-2-8-0 = five to eighty = the certificate validity span in days/years'.",
  },
  {
    id: 9180, tier: 2, category: "Crypto",
    title: "HPKE — Hybrid Public Key Encryption",
    what: "Modern ECIES-style construction: KEM (key encapsulation) + KDF + AEAD. Used in TLS Encrypted Client Hello, MLS (group messaging), ODoH. Replaces ad-hoc hybrid encryption.",
    mnemonic: "9180 = HPKE. 9+1=10, 8+0=8 → hybrid of 10 and 8 = 18 = HPKE is the 18th century of crypto (combining old PKE with modern AEAD). '9180 = Hybrid PKE'.",
  },

  // ── Tier 3: Useful ──────────────────────────────────────────────────────────
  {
    id: 7919, tier: 3, category: "TLS",
    title: "Negotiated Finite Field DH Ephemeral Parameters (FFDHE)",
    what: "Standardises safe FFDHE groups (ffdhe2048, ffdhe3072 etc.) to prevent weak DH parameter attacks (Logjam). TLS 1.3 uses X25519 ECDHE by default, but FFDHE groups are supported.",
    mnemonic: "7919 = FFDHE. 79 = prime (7919 itself is a prime number — a safe DH modulus). '7919 is literally a prime, fitting for a DH parameters RFC'.",
  },
  {
    id: 8017, tier: 3, category: "Crypto",
    title: "PKCS#1 v2.2 — RSA Cryptography Standard",
    what: "Defines RSA-OAEP (correct encryption padding) and RSA-PSS (signature padding). Contrasts with v1.5 padding which is vulnerable to Bleichenbacher oracle attacks. Use OAEP, never v1.5 for encryption.",
    mnemonic: "8017 = RSA spec. 80 = RSA is 80s crypto, 17 = 2017 updated. 'Eight-oh-one-seven = the spec that says use OAEP not v1.5'.",
  },
  {
    id: 5746, tier: 3, category: "TLS",
    title: "TLS Renegotiation Indication Extension",
    what: "Fix for the 2009 TLS renegotiation injection attack. Clients/servers must include the renegotiation_info extension to bind the new handshake to the previous one. Backward incompatible.",
    mnemonic: "5746 = renegotiation fix. '57 = 2009 vulnerability year (sort of), 46 = TLS 1.3 (8446) came later and removed renegotiation entirely'.",
  },
  {
    id: 6749, tier: 3, category: "Auth",
    title: "OAuth 2.0 Authorization Framework",
    what: "Delegation framework: resource owner grants limited access to a client via an authorisation server. Separates authentication (who you are) from authorisation (what you can do).",
    mnemonic: "6749 = OAuth 2.0. 67 = authorisation is at layer 6-7 (application layer). 49 = 4 grant types (auth code, implicit, client creds, resource owner). '6749 = OAuth's four grant types'.",
  },
  {
    id: 7519, tier: 3, category: "Auth",
    title: "JWT — JSON Web Token",
    what: "Compact token format: header.payload.signature. Claims: iss, sub, aud, exp, iat. Exam pitfalls: alg:none attack, weak HMAC secret, missing audience verification.",
    mnemonic: "7519 = JWT. 75 = 75% of auth systems use JWTs, 19 = 2019 (roughly when JWT became standard). 'Seven-five-one-nine = JWT has three parts: 7+5=12, 1+9=10, 12+10=22 chars in header typically'.",
  },
  {
    id: 4120, tier: 3, category: "Auth",
    title: "Kerberos Network Authentication Service V5",
    what: "TGT/TGS ticket flow. AS-REQ → AS-REP (TGT) → TGS-REQ → TGS-REP (service ticket). KDC is the trust centre. Symmetric keys only. Used in Active Directory.",
    mnemonic: "4120 = Kerberos. 4 = the 4-step ticket exchange, 1 = one KDC trust centre, 20 = 20 years it's been in Windows AD. '4-1-2-0 = four messages, one KDC, two tickets, zero public key'.",
  },
  {
    id: 8461, tier: 3, category: "Email",
    title: "MTA-STS — SMTP MTA Strict Transport Security",
    what: "Policy file at `.well-known/mta-sts.txt` enforcing TLS for inbound SMTP. Alternative to DANE that doesn't require DNSSEC. Analogous to HSTS for email servers.",
    mnemonic: "8461 = MTA-STS. 84 = 1984 (SMTP is old), 61 = TLS enforced (STARTTLS became standard ~2001+61=2062, not great). Better: '8461 = MTA-STS is HSTS for email'.",
  },
  {
    id: 9230, tier: 3, category: "DNS",
    title: "Oblivious DNS over HTTPS (ODoH)",
    what: "Proxy between client and DoH resolver. Proxy sees client IP but not query. Resolver sees query but not client IP. Neither party has the full picture. Maximum DNS privacy.",
    mnemonic: "9230 = ODoH. 92 = 2 parties (proxy + resolver), 30 = 30% more overhead than DoH. '9230 = Oblivious: the resolver is oblivious to who's asking'.",
  },
  {
    id: 7958, tier: 3, category: "DNS",
    title: "DNSSEC Trust Anchor Publication for the Root Zone",
    what: "How the root KSK is published and distributed. RFC 5011 automated rollover. Root KSK rollover 2018: first ever, ~750k resolvers hadn't updated their trust anchor.",
    mnemonic: "7958 = Root KSK publication. 7+9+5+8=29 → 2019 (roughly when resolvers finished updating). '7958 = where to find the root's public key'.",
  },
  {
    id: 5011, tier: 3, category: "DNS",
    title: "Automated Updates of DNSSEC Trust Anchors",
    what: "How resolvers automatically track root KSK rollovers without manual intervention. Add-hold-down and remove-hold-down timers prevent premature trust anchor transitions.",
    mnemonic: "5011 = trust anchor auto-update. 50 = 50-day hold-down timer (roughly), 11 = the RFC number is 5011 → '50-11: fifty days, one-one'. '5011 = automated KSK rollover'.",
  },
  {
    id: 2181, tier: 3, category: "DNS",
    title: "Clarifications to the DNS Specification",
    what: "Fixes ambiguities in RFC 1034/1035: TTL semantics (all records in an RRset must have same TTL), CNAME restrictions, authoritative vs non-authoritative distinction, case insensitivity.",
    mnemonic: "2181 = DNS clarifications. 21+81=102 ≈ 102 clarifications. '2181 = 2 + 181 = the second major DNS RFC after the originals'.",
  },
  {
    id: 8890, tier: 3, category: "Privacy",
    title: "The Internet is for End Users",
    what: "Farrell co-authored. Argues that when protocol designer interests conflict, end users must come first — above operators, above regulators. Philosophical basis for privacy-first design.",
    mnemonic: "8890 = End Users. 88 = infinity (∞) rotated = endless user base, 90 = 1990s when the internet became public. 'The internet (8890) is for everyone'.",
  },
  {
    id: 5424, tier: 3, category: "General",
    title: "Syslog Protocol",
    what: "Standard structured log format. Severity 0 (Emergency) to 7 (Debug). Facility codes (0=kernel, 1=user, 3=mail...). Structured data fields for machine-parseable logs.",
    mnemonic: "5424 = Syslog. 54 = 54 facility+severity combinations (8 severities × ~24 facilities ≈ close). 24 = 24/7 logging. '5424 = logs running 24/7'.",
  },
]

const CATEGORIES = ["All", "TLS", "DNS", "Crypto", "Privacy", "Email", "Auth", "General"]

const CATEGORY_COLORS = {
  TLS:     "bg-blue-900/40 text-blue-300 border-blue-800",
  DNS:     "bg-purple-900/40 text-purple-300 border-purple-800",
  Crypto:  "bg-yellow-900/40 text-yellow-300 border-yellow-800",
  Privacy: "bg-green-900/40 text-green-300 border-green-800",
  Email:   "bg-orange-900/40 text-orange-300 border-orange-800",
  Auth:    "bg-red-900/40 text-red-300 border-red-800",
  General: "bg-gray-800 text-gray-300 border-gray-700",
}

const TIER_LABEL = { 1: "Must Know", 2: "Important", 3: "Useful" }
const TIER_COLOR = {
  1: "text-red-400 bg-red-950/40 border-red-900",
  2: "text-amber-400 bg-amber-950/40 border-amber-900",
  3: "text-gray-400 bg-gray-900 border-gray-800",
}

export default function RFCs() {
  const navigate = useNavigate()
  const [search, setSearch] = useState("")
  const [cat, setCat] = useState("All")
  const [openId, setOpenId] = useState(null)

  const filtered = RFCS.filter(r => {
    const matchCat = cat === "All" || r.category === cat
    const q = search.toLowerCase()
    const matchSearch = !q || String(r.id).includes(q) || r.title.toLowerCase().includes(q) || r.what.toLowerCase().includes(q)
    return matchCat && matchSearch
  })

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center gap-4">
        <button onClick={() => navigate("/dashboard")} className="text-gray-400 hover:text-white text-sm">← Dashboard</button>
        <span className="text-gray-600">/</span>
        <span className="text-sm text-gray-300">RFC Reference</span>
      </nav>

      <div className="max-w-3xl mx-auto px-6 py-6">
        <div className="mb-6">
          <h1 className="text-xl font-bold text-white mb-1">RFC Reference</h1>
          <p className="text-sm text-gray-500">{RFCS.filter(r => r.tier === 1).length} must-know · {RFCS.filter(r => r.tier === 2).length} important · {RFCS.filter(r => r.tier === 3).length} useful</p>
        </div>

        <input
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="Search by RFC number, name, or keyword..."
          className="w-full bg-gray-900 border border-gray-800 text-gray-200 text-sm rounded-lg px-4 py-2.5 mb-4 focus:outline-none focus:border-blue-500"
        />

        <div className="flex gap-1.5 flex-wrap mb-6">
          {CATEGORIES.map(c => (
            <button key={c} onClick={() => setCat(c)}
              className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors
                ${cat === c ? "bg-blue-600 text-white" : "bg-gray-800 text-gray-400 hover:text-gray-200"}`}>
              {c}
            </button>
          ))}
        </div>

        <div className="space-y-2">
          {filtered.map(r => (
            <div key={r.id} className="border border-gray-800 rounded-xl overflow-hidden">
              <button
                onClick={() => setOpenId(openId === r.id ? null : r.id)}
                className="w-full flex items-center gap-4 px-4 py-3 text-left hover:bg-gray-900 transition-colors"
              >
                <span className="font-mono text-lg font-bold text-white w-16 shrink-0">{r.id}</span>
                <span className="text-sm text-gray-200 flex-1 text-left">{r.title}</span>
                <div className="flex items-center gap-2 shrink-0">
                  <span className={`text-[10px] font-semibold px-2 py-0.5 rounded border ${CATEGORY_COLORS[r.category]}`}>{r.category}</span>
                  <span className={`text-[10px] font-semibold px-2 py-0.5 rounded border ${TIER_COLOR[r.tier]}`}>{TIER_LABEL[r.tier]}</span>
                  <span className="text-gray-600 text-xs">{openId === r.id ? "▲" : "▼"}</span>
                </div>
              </button>

              {openId === r.id && (
                <div className="border-t border-gray-800 bg-gray-950 px-4 py-4 space-y-3">
                  <p className="text-sm text-gray-300 leading-relaxed">{r.what}</p>
                  <div className="bg-blue-950/30 border border-blue-900/50 rounded-lg px-3 py-2.5">
                    <p className="text-xs text-blue-400 font-semibold uppercase tracking-wider mb-1">Mnemonic</p>
                    <p className="text-sm text-blue-200 leading-relaxed">{r.mnemonic}</p>
                  </div>
                  <a
                    href={`https://datatracker.ietf.org/doc/html/rfc${r.id}`}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 text-xs text-gray-400 hover:text-gray-200 transition-colors"
                  >
                    📄 datatracker.ietf.org/doc/html/rfc{r.id}
                  </a>
                </div>
              )}
            </div>
          ))}
          {filtered.length === 0 && (
            <p className="text-gray-500 text-sm text-center py-12">No RFCs match your search.</p>
          )}
        </div>
      </div>
    </div>
  )
}
