<!-- MODE:EASY -->
# Designing Mitigations — Simple Version

A mitigation is something you do to stop a bad thing from happening, or to make it less bad.

Think of it like this: your house might flood (the risk). What can you do?
- Put sandbags at the door (prevent it)
- Get flood insurance (reduce the damage)
- Install a sump pump (detect and respond)

In security, mitigations follow the same three ideas:
**Prevent → Detect → Respond**

The golden rule for exams: **be specific.** The examiner wants a real answer, not waffle.

Bad answer: "Improve security." (0 marks — means nothing)

Good answer: "Use bcrypt with a random salt to hash passwords, so stolen hashes can't be reversed quickly." (full marks — specific mechanism + why it works)

**Pairing risks to mitigations:**
- Stolen passwords → bcrypt + MFA + rate-limiting login attempts
- Data leaking in transit → TLS 1.3 for all connections
- Unauthorised access → RBAC (role-based access control) + least privilege
- GDPR breach → data minimisation + delete data when no longer needed
- Supply chain attack → pin dependency versions + check signatures

**Remember:** One good mitigation per risk is enough. Don't list five vague ones. List one specific, named one.

<!-- MODE:TECHNICAL -->
# Designing Mitigations

## Mitigation Categories

| Category | What it does | Examples |
|---|---|---|
| **Preventive** | Stops the attack happening | MFA, input validation, TLS, encryption at rest |
| **Detective** | Spots the attack in progress | SIEM, IDS, audit logging, anomaly detection |
| **Corrective** | Limits damage after attack | Incident response plan, backups, revocation |

## Countermeasure Quality: Mark vs No-Mark

Generic = 0 marks. Specific mechanism + justification = full marks.

| Risk | Poor (0 marks) | Good (full marks) |
|---|---|---|
| Credential theft | "Use stronger passwords" | "bcrypt with cost factor ≥12 + per-user salt; HIBP breach-password check at registration; TOTP MFA" |
| Data in transit | "Encrypt traffic" | "TLS 1.3 only; disable TLS 1.2 and earlier; HSTS with preload; certificate pinning for mobile clients" |
| SQL injection | "Sanitise inputs" | "Parameterised queries (prepared statements) for all DB interactions; ORM with no raw SQL; WAF with SQLi rules" |
| PII leak to third party | "Review contracts" | "Data minimisation before API call; review provider DPA; contractual deletion obligations; consider self-hosted model" |
| Supply chain | "Audit dependencies" | "SBOM generation; pin versions; signed releases; Dependabot / Renovate; periodic `npm audit` / `pip-audit` in CI" |
| DoS | "Add capacity" | "Rate limiting per IP + per user; anycast CDN; auto-scaling; HelloRetryRequest for TLS; SYN cookies" |
| Insider threat | "Monitor staff" | "Separation of duties; just-in-time privilege; PAM solution; append-only audit log shipped to isolated store" |

## GDPR-Specific Mitigations (Q1 must-have)

- **Data minimisation** — collect only what you need; delete when purpose expires
- **Pseudonymisation** — replace identifiers with tokens; real data in separate store
- **72-hour breach notification** — have an incident response procedure ready
- **DPIA** — Data Protection Impact Assessment for high-risk processing
- **DPA review** — verify third-party processors have adequate data agreements

## Exam Strategy

For Q1(b), each risk needs exactly one concrete countermeasure. Name the mechanism, not the category. "Encryption" is a category. "AES-256-GCM at rest + TLS 1.3 in transit, keys in HSM" is a countermeasure.


## Relevant RFCs

- **RFC 3552** — *Security Considerations Guidelines* — Section 5 covers standard mitigation patterns: authentication, confidentiality, integrity, non-repudiation
- **RFC 6973** — *Privacy Threat Model* — Section 6 maps each privacy threat to concrete mitigations: data minimisation, anonymisation, consent, access controls
- **RFC 7258** — *Pervasive Monitoring is an Attack* — motivates mitigations at the protocol design level (e.g. encrypting by default) rather than just at deployment

<!-- MODE:HINGLISH -->
# Mitigations — Hinglish mein

## Mitigation matlab kya?

Simple: risk ko rokna ya uska damage kam karna. Har risk ke saath ek specific solution dena hota hai.

**Sabse important rule:** Vague mat bolo. Specific bolo.

## Three types yaad karo

**Preventive** — pehle se rok lo. Example: MFA lagao taaki account steal na ho sake.

**Detective** — pata karo ki attack ho raha hai. Example: SIEM se suspicious logins ka alert aaye.

**Corrective** — damage ho gaya toh handle karo. Example: backup se restore karo, incident response plan follow karo.

## Common risks aur unke sahi mitigations

**Password theft →** bcrypt with salt (MD5 ya SHA-1 nahi — woh bahut fast hain), upar se MFA.

**Data transit mein leak →** TLS 1.3 sirf. TLS 1.2 disable karo.

**SQL Injection →** Parameterised queries. Raw SQL mat likhna.

**Third party ko data leak →** Data minimisation — API call se pehle PII strip karo. Provider ka DPA check karo.

**Supply chain attack →** Dependency versions pin karo. Signed releases check karo. CI mein `pip-audit` / `npm audit` chalao.

## Exam mein zero marks wale answers

"Security improve karo" — 0 marks.
"Firewalls lagao" — 0 marks.
"Better policies" — 0 marks.

Kuch bhi vague likhoge toh Farrell marks kaatega. Har mitigation mein:
1. Kya mechanism use kar rahe ho (e.g., bcrypt, TLS 1.3, RBAC)
2. Kyun woh kaam karega (e.g., "bcrypt slow hai toh brute force impractical ho jaata hai")
