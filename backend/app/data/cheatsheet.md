# CS7053 Exam Cheat Sheet

> Exam format: 4 questions (Q1–Q4), 40 marks each, attempt **any 3**. Read Q1 first — it is nearly always the most straightforward.

---

## Q1 — Risk Analysis

### The Process (Q1a template, ~15 marks)

Answer these 7 steps in order. Missing **any** of the bold lines loses marks:

1. **Identify assets** — data, availability, reputation, staff, licences. **Always mention reputation as an asset.**
2. **Identify risks and vulnerabilities** — interview domain experts, not just IT. For medical: interview doctors. For LLMs: seek external LLM security expertise.
3. **Classify each risk** — Impact (High/Medium/Low) × Likelihood (High/Medium/Low) → overall risk priority.
4. **Prioritise** — highest combined score gets mitigated first.
5. **Design a mitigation** for the top-ranked risk.
6. **Re-run the analysis** — each mitigation changes probability of others. **This is what makes it iterative — say so explicitly.**
7. **Iterate** until effort budget exhausted or time runs out. **Record all decisions throughout**, even ones you decide NOT to mitigate.

**Key Farrell phrases to include:**
- "Seek outside expertise where internal knowledge is insufficient"
- "Reputation is an asset"
- "Re-run the analysis after each mitigation"
- "Record everything — including things not mitigated"

---

### Three Risks Template (Q1b, ~15 marks)

For each risk, use this structure:

> **Risk name:** [what could go wrong]
> **Impact:** HIGH/MEDIUM/LOW — [why: GDPR fine, service outage, reputational damage...]
> **Likelihood:** HIGH/MEDIUM/LOW — [why: exposed endpoint, weak passwords, phishing...]
> **Countermeasure:** [specific, not vague — AES-256-GCM not "use encryption"]

Pick risks that span categories:
- One **technical** (e.g. data breach, injection, XSS)
- One **process** (e.g. insider threat, credential mismanagement)
- One **external** (e.g. DDoS, supply chain, phishing)

---

### Privacy Threats — RFC 6973

RFC 6973 defines privacy threats *beyond* normal security threats:

| Threat | Meaning |
|--------|---------|
| **Correlation** | Linking records from different contexts |
| **Identification** | Linking data to a real person |
| **Secondary use** | Using data beyond original stated purpose |
| **Disclosure** | Exposing private data |
| **Exclusion** | Not allowing people to know what data is held about them |
| **Re-identification** | Combining supposedly anonymous data to reveal identity |

---

### GDPR Key Points

- **Data minimisation** — collect only what you need
- **Purpose limitation** — use data only for stated purpose
- **Consent** — must be freely given, informed, specific
- **Right to erasure** ("right to be forgotten")
- **DPA notification within 72 hours** of discovering a breach
- **Data Protection Impact Assessments (DPIAs)** for high-risk processing

---

### Privacy by Design (7 Principles)

1. Proactive not reactive — prevent, don't remediate
2. Privacy as the default setting
3. Privacy embedded into design
4. Full functionality — positive-sum, not zero-sum
5. End-to-end security — full lifecycle protection
6. Visibility and transparency
7. Respect for user privacy — keep it user-centric

---

### Security in the SDLC

Security requirements → threat modelling → code review → penetration testing → incident response planning

**Always include**: requirements at design stage, not bolted on after.

---

## Q2 — TLS and Protocols

### TLS 1.3 — RFC 8446 (exam favourite)

> Farrell says: spend time on TLSv1.3 for exam. ~90% of students choose TLS.

**Major changes from TLS 1.2:**
- AEAD everywhere (no more MAC-then-encrypt, no CBC, no compression)
- All key exchanges provide **forward secrecy** — RSA key transport removed
- 1-RTT handshake (was 2-RTT)
- More handshake messages encrypted (incl. Certificate)
- Ciphersuite refactored: only specifies record layer crypto, not key exchange
- ECC built in; no custom DH groups
- PKCS#1v1.5 → RSA PSS for protocol signatures
- 0-RTT "early data" mode added (dangerous)
- **Versioning muck**: pretends to be TLSv1.2 for middleboxes

---

### TLS 1.3 Full 1-RTT Handshake

```
Client                                               Server
Key  ^ ClientHello
Exch | + key_share*
     | + signature_algorithms*
     | + psk_key_exchange_modes*
     v + pre_shared_key*         -------->
                                            ServerHello  ^ Key
                                           + key_share*  | Exch
                                      + pre_shared_key*  v
                                  {EncryptedExtensions}  ^  Server
                                  {CertificateRequest*}  v  Params
                                         {Certificate*}  ^
                                   {CertificateVerify*}  | Auth
                                             {Finished}  v
                              <--------  [Application Data*]
     ^ {Certificate*}
Auth | {CertificateVerify*}
     v {Finished}                -------->
       [Application Data]        <------->  [Application Data]
```

`{}` = encrypted under handshake traffic key; `[]` = encrypted under application traffic key

---

### 0-RTT Early Data — The Sharp Implement

- Client sends application data **before server responds** (requires prior PSK/ticket)
- Used by browsers for HTTP GET in "first flight"
- **Problem: early data can be REPLAYED**
  - Attacker records 0-RTT message, replays to another load-balanced instance
  - Especially bad for DoT (DNS-over-TLS) with anycast recursives
- Early data NOT authenticated until server validates client Finished
- **Do NOT act on early data until after Finished is checked**
- HTTP GET is theoretically idempotent — but real-world servers don't always honour this

---

### TLS 1.3 Key Schedule (HKDF)

```
PSK ──→ HKDF-Extract = Early Secret
             │
             ├──→ client_early_traffic_secret
             │
        Derive-Secret(., "derived", "")
             │
(EC)DHE ──→ HKDF-Extract = Handshake Secret
             │
             ├──→ client_handshake_traffic_secret
             ├──→ server_handshake_traffic_secret
             │
        Derive-Secret(., "derived", "")
             │
     0 ──→  HKDF-Extract = Master Secret
             │
             ├──→ client_application_traffic_secret_0
             ├──→ server_application_traffic_secret_0
             ├──→ exporter_master_secret
             └──→ resumption_master_secret
```

`HKDF-Expand-Label(Secret, Label, Context, Length)` — HKDF defined in RFC 5869.

---

### TLS 1.3 Ciphersuites (record layer only)

| TLS 1.3 Suite | Notes |
|---------------|-------|
| `TLS_AES_128_GCM_SHA256` | Default, hardware-accelerated |
| `TLS_AES_256_GCM_SHA384` | Higher security margin |
| `TLS_CHACHA20_POLY1305_SHA256` | Best if no AES hardware |

Key exchange and auth are now in **extensions** (key_share, signature_algorithms), NOT the ciphersuite.

---

### TLS Attacks — Know These

| Attack | Year | Problem | Fix |
|--------|------|---------|-----|
| **BEAST** | 2011 | CBC IV = last ciphertext block; active content + MITM → cookie recovery | TLS 1.2+ |
| **CRIME** | 2012 | Compression reveals secret via size oracle | Turn off compression |
| **Lucky-13** | 2013 | CBC timing side-channel via HMAC-SHA1 input size | Use AEAD (TLS 1.2+) |
| **DROWN** | 2016 | SSLv2 re-enables Bleichenbacher; cross-protocol attack | Remove old SSLv2 code |
| **ROBOT** | 2017 | Bleichenbacher still present in real deployments | Don't support RSA key transport |
| **Heartbleed** | 2014 | TLS heartbeat (RFC 6520) buffer overread → server private key | Bounds check |
| **goto fail** | 2014 | Apple bug: TLS signature check always passed (duplicate goto) | Code review |
| **Marvin** | 2023 | Bleichenbacher via timing + statistical analysis; most RSA/TLS impls affected | Don't use RSA key transport |
| **Stuxnet/Flame** | ~2010 | Compromised code-signing keys + MD5 prefix-collision | Better PKI, drop MD5 |
| **Bleichenbacher** | 1998 | PKCS#1 padding oracle; basis for DROWN/ROBOT/Marvin | RFC 3218; use OAEP |
| **KeyTrap** | 2023 | DNSSEC: publish many bad sigs → DNS resolver DoS (CPU 100% for hours) | Patched in DNS servers |

---

### PKI

- **X.509** (RFC 5280): certificate format used everywhere
- **CA** signs certificates; **RA** handles registration
- **CRL** (Certificate Revocation List): periodic list of revoked certs
- **OCSP** (Online Certificate Status Protocol): real-time check; can be **stapled**
- **Certificate Transparency (CT)** (RFC 6962/9162): append-only public log — detects mis-issuance (not prevents)
- **ACME** (RFC 8555): automated cert management (Let's Encrypt uses this)
- **CAA RR** in DNS: tells CAs which CAs may issue for a domain
- **HSTS** (RFC 6797): browser must only use TLS for this site
- **Notable CA failures**: DigiNotar (2011, hacked, liquidated), Comodo RA hack (2011), Trustico (2018 — emailed 23k private keys)

---

### AEAD — Authenticated Encryption with Additional Data

- Combines confidentiality + integrity in a **single operation**
- Returns error OR plaintext — never partial decryption
- **CRITICAL: Never reuse nonce with same key** — especially AES-GCM behaves like a stream cipher on nonce reuse
- RFC 5116 defines the abstract AEAD interface

| Mode | Notes |
|------|-------|
| **AES-128-GCM** | Default for capable devices (hardware AES-NI) |
| **AES-256-GCM** | Higher margin; same structure |
| **ChaCha20-Poly1305** | Best without hardware AES; RFC 7539 |
| **AES-CCM** | WiFi, IoT (Zigbee) |

---

### Other Protocols (know one in detail)

**IPsec (RFC 4301):**
- Operates at IP layer; tunnel mode (VPN) or transport mode
- AH (deprecated) + **ESP** (RFC 4303) — encrypts payload + auth
- **IKEv2** (RFC 7296): key exchange and auth (NOT IKEv1 — too complex)
- SPI + dest IP = Security Association (SA); directional

**SSH (RFC 4251):**
- TOFU model for host keys ("trust on first use")
- Turn off password auth; use public key
- Architecture in RFC 4251, transport RFC 4253, user auth RFC 4252

**Kerberos (RFC 4120):**
- Symmetric key-based; KDC = AS + TGS
- Client gets TGT from AS, uses TGT to get Service Ticket from TGS
- Used in Windows ActiveDirectory; requires loose clock sync (~5 min skew)

**Wireguard:**
- Curve25519 keys, ChaCha20-Poly1305, UDP, ~4K LOC kernel
- No crypto agility by design; in Linux kernel since Jan 2020
- Static key pairs per interface; ephemeral keys in 1-RTT handshake
- DoS mitigation via cookie mechanism
- Optional PSK for post-quantum future-proofing

---

### Crypto Quick Reference

| Algorithm | Type | Status | RFC |
|-----------|------|--------|-----|
| AES-128/256 | Symmetric block cipher | RECOMMENDED | — |
| ChaCha20 | Symmetric stream cipher | RECOMMENDED | 7539 |
| SHA-256 | Hash | RECOMMENDED | 6234 |
| SHA-3/Keccak | Hash | OK | — |
| Curve25519/Ed25519 | ECC | RECOMMENDED | 7748, 8032 |
| RSA-2048+ | Asymmetric | OK for sigs, NOT key transport | — |
| ECDH/ECDSA (P-256) | ECC | OK (avoid non-deterministic ECDSA) | — |
| HKDF | KDF | Used in TLS 1.3 | 5869 |
| Argon2 | Password hash | RECOMMENDED winner of PHC | 9106 |
| PBKDF2 | Password hash | Acceptable | 8018 |
| **MD5** | Hash | **BROKEN — DO NOT USE** | — |
| **SHA-1** | Hash | **DEPRECATED — BROKEN** | — |
| **RC4** | Stream cipher | **VERY NOT RECOMMENDED** | — |
| **DES/3DES** | Block cipher | **NOT RECOMMENDED** | — |

**Key rule for exam**: Public key encrypts; private key decrypts. Private key signs; public key verifies. Getting these reversed = marks lost.

**Forward Secrecy**: Use ephemeral key exchange (ECDHE/DHE) so that compromise of long-term keys doesn't decrypt past sessions.

---

## Q3 — System Design / Authentication

### Authentication Factors

- **Something known**: password, PIN
- **Something possessed**: smart card, hardware token, phone (TOTP)
- **Something personal**: fingerprint, retina (biometrics — use with caution)
- Combinations are stronger (MFA)

**Note**: SMS-based 2FA is weak — SS7 protocol attacks allow interception.

---

### Password Security

**What sysadmins must do:**
- Store passwords as **salted** slow hashes (Argon2 > sha-512-crypt > bcrypt > PBKDF2)
- **Never store plaintext** or unsalted MD5/SHA-1
- Use **unique random salt** per password
- Enforce not-online-guessable strength; don't over-enforce "quality" rules (NIST recanted)
- Consider checking against HaveIBeenPwned k-anonymity API
- Prefer **password managers** and passkeys/FIDO2

**Argon2** (RFC 9106): winner of Password Hashing Competition
- Memory-hard, time-memory trade-off resistant
- Argon2id is the recommended variant

**Attack types:**
- **Dictionary attack**: guess from word list + variants
- **Rainbow tables**: time-memory trade-off (defeated by salting)
- **Brute force**: try all combinations (defeated by slow hash + length limits)

---

### FIDO2 / WebAuthn / Passkeys

- Public key credential stored on device/platform
- Challenge-response: server sends random challenge, client signs with private key
- Private key never leaves device
- Resistant to phishing (origin-bound)
- Replaces or supplements passwords

---

### Security Architecture Principles

| Principle | Meaning |
|-----------|---------|
| CIA triad | Confidentiality, Integrity, Availability |
| Least privilege | Each component has minimum necessary access |
| Defence in depth | Multiple layers; no single point of failure |
| Fail-safe defaults | Default deny, not default allow |
| Separation of duties | No single person/process has all access |
| Attack surface minimisation | Fewer entry points = harder to attack |

---

### Crypto Choices for System Design

- **Data at rest**: AES-256-GCM
- **Data in transit**: TLS 1.3 with ECDHE + AES-128-GCM or ChaCha20-Poly1305
- **Password hashing**: Argon2id
- **Token signing**: Ed25519 or RSA-PSS (not PKCS#1v1.5)
- **Key exchange**: X25519 (Curve25519) or P-256 ECDH
- **Hashing**: SHA-256; never MD5 or SHA-1
- **Never**: roll your own crypto

---

### Audit Logging

- Log authentication attempts (success and failure)
- Log privilege escalations
- Log data access to sensitive records
- Logs must be **tamper-evident** (append-only, offsite, signed)
- Don't log passwords — even in failure messages ("username: 123456" anti-pattern)

---

## Q4 — DNS, DNSSEC, Email Security

### DNS Resolution Flow

```
Browser → OS Stub Resolver → Recursive Resolver
         Recursive → Root Servers (.)
         Recursive → TLD Servers (.ie, .com)
         Recursive → Authoritative Server (tcd.ie)
         → Answer cached for TTL duration
```

**Key record types:**

| RR | Purpose |
|----|---------|
| A | IPv4 address |
| AAAA | IPv6 address |
| MX | Mail server for domain |
| NS | Authoritative nameservers |
| SOA | Start of Authority (zone admin) |
| TXT | Arbitrary text (SPF, DKIM, etc.) |
| CAA | Which CAs may issue certs for domain |
| CNAME | Alias to another name |
| DS | Delegation Signer (DNSSEC chain) |
| DNSKEY | Public key for zone signing |
| RRSIG | Signature over an RRset |
| NSEC/NSEC3 | Proof of non-existence |
| TLSA (DANE) | TLS certificate constraints in DNS |

---

### DNS Poisoning

- DNS queries default to **UDP port 53**
- Query ID is only 16 bits + source port = ~32 bits of guessable entropy
- **Anyone can answer first** — attacker races with legitimate answer
- Poisoned cache = attacker controls where users go for entire TTL
- Fix: DNSSEC (cryptographic signatures on answers)

---

### DNSSEC

**How it works:**
- Zone has two keys: **KSK** (Key Signing Key) and **ZSK** (Zone Signing Key)
- KSK signs the DNSKEY RRset
- ZSK signs all other RRsets (A, MX, etc.)
- Parent zone has a **DS** record = hash of child's KSK (creates chain of trust)
- Chain goes up to root `.` (root KSK is the ultimate trust anchor)

**DNSSEC record types:**
- `DNSKEY` — public signing key for zone
- `RRSIG` — signature over an RRset; includes expiry
- `DS` — delegation signer (lives in parent zone, points to child KSK)
- `NSEC`/`NSEC3` — authenticated denial of existence

**Root KSK ceremony**: quarterly IANA event; KSK held in HSMs by community members; scripted, streamed.

**Deployment problems:**
- Requires registrar to pass DS record to parent — often via crappy web form
- RRSIG expiry = new thing to manage (can break zones if forgotten)
- Only ~4.5% of .com domains signed (2026); .se ~60%; .ie ~0.45%
- Some middleboxes strip DNSSEC RRs
- CDS/CDNSKEY (RFC 8078): child publishes new DS in own zone; parent scans and picks up

---

### DNS Privacy

Plain DNS leaks your browsing to ISPs, recursive operators, and network observers.

| Solution | RFC | Notes |
|----------|-----|-------|
| **DoT** (DNS over TLS) | RFC 7858 | Port 853; stub↔recursive common |
| **DoH** (DNS over HTTPS) | RFC 8484 | Port 443; used in browsers (Firefox, Chrome) |
| **QNAME minimisation** | RFC 9156 | Only send minimal labels per upstream query |
| **Padding** | RFC 8467 | Pad queries to N×128, responses to N×468 octets |
| **Tor** | — | Hides client IP too |

---

### Email Security

**Email transport stack:**
- MUA → MTA (SMTP/587) → MTA (SMTP/25) → Mailbox

**Transport security:**
- SMTP/TLS: opportunistic — often still accepts bad/expired certs
- **MTA-STS** (RFC 8461): signals strict SMTP/TLS (like HSTS for email)
- **DANE** (RFC 7671): TLSA RR authenticated by DNSSEC

**Sender authentication (anti-spoofing/spam):**

| Standard | RFC | How it works |
|----------|-----|-------------|
| **SPF** | 7208 | Publish authorised sending IPs in DNS; receiving MTA checks source IP |
| **DKIM** | 6376 | Sending MTA signs outbound email with private key; receiving MTA verifies via public key in DNS |
| **DMARC** | 7489 | Publishing MTA defines policy (none/quarantine/reject) for how receivers handle SPF/DKIM failure; enables reporting |

**DMARC downsides:** breaks mailing lists (sender's domain in From: header fails DKIM after list server re-sends). IETF mailing lists work around this by rewriting From.

**End-to-end email:** S/MIME (CMS, RFC 8551) or PGP (RFC 9580) — not widely deployed; hop-by-hop TLS is the norm.

---

## Key RFCs to Know

| RFC | Topic |
|-----|-------|
| **8446** | TLS 1.3 |
| **6973** | Privacy threat taxonomy |
| **9106** | Argon2 password hashing |
| **5280** | X.509 PKI certificates |
| **8555** | ACME (Let's Encrypt) |
| **6962** | Certificate Transparency |
| **7858** | DNS over TLS (DoT) |
| **8484** | DNS over HTTPS (DoH) |
| **9156** | QNAME minimisation |
| **7208** | SPF |
| **6376** | DKIM |
| **7489** | DMARC |
| **8461** | MTA-STS |
| **4120** | Kerberos v5 |
| **7296** | IKEv2 |
| **4301** | IPsec Architecture |
| **4303** | ESP |
| **5869** | HKDF |
| **6797** | HSTS |
| **8659** | CAA DNS record |
| **7539** | ChaCha20-Poly1305 |
| **5116** | AEAD interface |
| **3218** | Bleichenbacher avoidance |
| **8078** | CDS/CDNSKEY (DNSSEC key rollover) |

---

## Common Marks Traps

- **Q1a**: listing risks instead of describing the process → zero for that part
- **Q1b**: vague countermeasures ("use encryption") → lose marks; be specific ("AES-256-GCM for data at rest")
- **Crypto keys**: mixing up public/private key roles → immediate loss of marks
- **TLS**: saying TLS 1.3 is only a minor update → wrong; it's a major overhaul
- **0-RTT**: saying it has no security downsides → wrong; replay attacks
- **DNSSEC**: saying it encrypts DNS queries → wrong; it authenticates but doesn't encrypt
- **DMARC**: claiming it solves spam → wrong; it addresses spoofing; spam is separate
- **Argon2**: calling it just "a hash function" → it's specifically a password-hashing function designed to be memory-hard
