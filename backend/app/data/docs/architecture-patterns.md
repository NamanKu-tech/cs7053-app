<!-- MODE:EASY -->
# Secure Architecture Patterns — Simple Version

Architecture is how you arrange the pieces of a system. Good security architecture makes attacks harder, limits damage when something does go wrong, and makes it obvious when someone is doing something suspicious.

**The key ideas:**

**Defence in depth** — Don't rely on one lock. Use many layers. If an attacker breaks through the front door, there should be another door inside, and another after that. Each layer buys time and limits damage.

**Least privilege** — Every part of the system gets only the access it absolutely needs. The web server doesn't need access to the database. The app only needs read access, not write. If an attacker compromises the web server, they can't get to the database directly.

**Separation of duties** — Important actions require more than one person/system. Admins can't both create accounts AND approve transactions. A developer can't push code AND deploy to production without review.

**Fail secure** — When something breaks, it should fail *safely*. If the authentication service crashes, the system should deny all access (not grant all access).

**Trust boundaries** — Draw a line between zones that trust each other differently. Users are outside. Internal services are inside. The boundary has a checkpoint (authentication + authorisation).

**A typical 3-tier web architecture:**
1. **Load balancer / CDN** (public-facing, absorbs DoS)
2. **Web/API tier** (behind firewall, handles requests)
3. **Database tier** (only accessible from app tier, never public)

Plus: separate admin path, separate audit path, separate monitoring.

<!-- MODE:TECHNICAL -->
# Secure Architecture Patterns

## Core Design Principles (name these in Q3)

| Principle | Application |
|---|---|
| **Defence in depth** | Multiple independent security controls; breach of one doesn't compromise all |
| **Least privilege** | Each component has minimum necessary permissions; no broad database grants |
| **Separation of duties** | Critical operations require multiple roles; prevents insider abuse |
| **Fail secure** | Default deny; fail closed (crash → reject requests, not accept) |
| **Complete mediation** | Every access request checked against policy; no cached bypass |
| **Economy of mechanism** | Simple designs have fewer bugs; complexity is the enemy of security |
| **Open design** | Security does not rely on obscurity; Kerckhoffs's principle |

## Standard Q3 Architecture Layout

```
Internet
   |
[CDN / DDoS scrubbing]
   |
[WAF + Load Balancer]   ← TLS termination here
   |
[Web / API tier]        ← stateless; horizontal scaling; no plaintext PII
   |
[Application tier]      ← business logic; auth decisions; audit events emitted
   |
[DB tier]               ← encrypted at rest; accessible only from app tier
   |
[Audit log store]       ← append-only; isolated; separate auth; hash-chained
                          (shipped to write-once storage / WORM)

Separate plane:
[Jump-host]  → [Admin interface]    ← MFA required; all access logged
[SIEM]       ← receives audit events from all tiers
[HSM]        ← holds signing keys; key encryption keys; never exports raw keys
```

## Trust Boundaries to Always Draw

1. Internet → DMZ (WAF/LB validates all input)
2. DMZ → App tier (mutual TLS for service-to-service)
3. App tier → DB (dedicated service account; parameterised queries; no SA or root)
4. Admin plane → Production (separate network segment; jump-host; MFA; JIT)
5. Audit store → everything else (write-only from prod; read-only for auditors from separate auth)

## HSM Usage (always mention in Q3)

Hardware Security Module: signs JWTs/certificates; encrypts DB keys; key never leaves hardware. Even compromised app server can't extract the signing key — it can only ask HSM to sign things.

FIPS 140-2 Level 3 / 4 for high-assurance (government, financial).

## Anonymisation for Statistics

Q3 often has a "statistics" or "analytics" requirement alongside PII. Use:
- **k-anonymity** — no record is distinguishable from k-1 others
- **Differential privacy** — add calibrated noise; mathematical guarantee
- **Aggregation only** — never release individual records; only counts/averages

<!-- MODE:HINGLISH -->
# Secure Architecture — Hinglish mein

## Ek system design karo — kahan se shuru karein?

Q3 mein system design ka jawab ek pattern follow karta hai:

1. Requirements (CIA+) — pehle yeh
2. Architecture diagram describe karo
3. Trust boundaries identify karo
4. Har actor ke liye auth mechanism

## Key patterns yaad karo

**Defence in depth:** Ek lock kaafi nahi. Multiple layers. Front door toota → andar aur doors hain. Time milta hai detect karne ka.

**Least privilege:** Har part ko sirf utna hi access jitna zaroori hai. Web server ko database direct access nahi chahiye. Application ko sirf read access agar wahi kaafi hai.

**Separation of duties:** Important kaam ek akele nahi kar sakta. Code review alag person, deployment alag person. Admin create kar sakta hai account, approve doosra karega.

**Fail secure:** System crash ho toh deny karo, grant mat karo. Default = reject.

## Standard 3-tier architecture

```
Internet
  ↓
CDN + WAF + Load Balancer  (DoS protection, TLS termination)
  ↓
Web/API tier  (stateless, no PII store)
  ↓
App tier  (business logic, auth, audit events)
  ↓
DB tier  (encrypted at rest, sirf app tier se accessible)

Alag:
Jump-host → Admin interface (MFA required)
SIEM ← sari tiers se audit events
HSM ← signing keys (kabhi bahar nahi nikalti)
```

## Trust boundaries

Har boundary par check hona chahiye. Internet se aane wali har request WAF se guzre. App se DB tak mTLS. Admin plane production se alag network segment mein.

## HSM — kyun important hai

Hardware Security Module mein keys hoti hain jo kabhi hardware se bahar nahi nikalti. App compromised ho bhi jaaye — signing key safe hai. Always mention karo Q3 mein.
