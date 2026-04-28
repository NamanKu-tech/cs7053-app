<!-- MODE:EASY -->
# Security Requirements — Simple Version

Before you design a system, you need a list of the rules it must follow to be secure. These are called security requirements.

Think of designing a bank. Before building it, you'd write rules like:
- Only authorised people can access the vault (authentication + authorisation)
- Every transaction must be recorded and can't be deleted (audit)
- Even if the power goes out, the system must keep running (availability)
- Customers' account details must be private (confidentiality)
- No one must be able to change a balance secretly (integrity)

In security, there's a famous acronym to remember the basics: **CIA+**

**C — Confidentiality:** Only authorised people see the data.
**I — Integrity:** Data can't be changed without authorisation.
**A — Availability:** The system works when people need it.
**+ Non-repudiation:** Once you do something, you can't deny you did it (think digital signatures on transactions).
**+ Authentication:** Prove who you are before accessing anything.
**+ Authorisation:** Just because you're authenticated doesn't mean you can do everything.

Q3 always asks you to list security requirements first, then design a system to meet them. Students who skip straight to the architecture lose the requirement marks.

Every Q3 scenario also has an "auditor" role — someone who needs to check what happened. Always include an audit requirement.

<!-- MODE:TECHNICAL -->
# Writing Security Requirements (CIA+)

## The Standard Set (use for any Q3 scenario)

| Requirement | What it means | Mechanism that satisfies it |
|---|---|---|
| **Confidentiality** | Data visible only to authorised parties | Encryption at rest (AES-256-GCM) + in transit (TLS 1.3) |
| **Integrity** | Data cannot be modified undetected | Digital signatures; hash chains; AEAD authentication tag |
| **Availability** | System accessible when needed | BCP/DR; load balancing; CDN; rate limiting against DoS |
| **Authentication** | Verify identity of each principal | PKI certificates; FIDO2/WebAuthn; OIDC; mTLS for services |
| **Authorisation** | Grant access based on verified identity | RBAC + ABAC; least-privilege; separation of duties |
| **Non-repudiation** | Actions cannot be denied | Digital signatures on transactions; append-only audit log |
| **Accountability** | Track who did what and when | Tamper-evident audit trail; identity-linked action logging |
| **Privacy** | Minimise data collection and use | Data minimisation; purpose limitation; anonymisation |
| **GDPR compliance** | Meet legal obligations | DPIA; 72h breach notification; right to erasure; DPA |

## Farrell's Q3 Pattern

Every Q3 has **multiple actor classes.** Enumerate them and assign auth mechanisms:

| Actor class | Typical mechanism |
|---|---|
| End users / citizens | OIDC (OAuth2 + OpenID Connect), FIDO2 passkeys |
| Staff / internal users | PKI smartcard, hardware OTP token, MFA |
| Admins | MFA + jump-host + just-in-time privilege (PAM) |
| External APIs / services | Bearer token + mTLS |
| Auditors | Read-only, separate authentication path, isolated log store |

**Key rule:** Admins must NOT access plaintext PII (separation of duties). Design architecture so that full cleartext requires collusion between multiple roles.

## Trust Boundaries

Identify and document every boundary where trust changes:
- User browser → web tier
- Web tier → application tier
- Application tier → database
- Admin plane → production plane
- External API → internal services

Each boundary needs explicit auth + encryption.

## GDPR as a Requirements Source

For any scenario involving EU residents or EU-established organisations:
- Art. 5: Lawful basis, minimisation, purpose limitation
- Art. 25: Privacy by design and by default
- Art. 35: DPIA if high-risk processing
- Art. 33: 72h breach notification to DPC/supervisory authority


## Relevant RFCs

- **RFC 2119** — *Key Words for use in RFCs (MUST, SHOULD, MAY)* — the vocabulary for writing security requirements; exam answers using MUST/SHOULD signal precision
- **RFC 3552** — *Guidelines for Writing RFC Security Considerations* — the template for enumerating security requirements in any protocol or system design
- **RFC 6973** — *Privacy Considerations for Internet Protocols* — companion checklist for privacy requirements alongside security requirements

<!-- MODE:HINGLISH -->
# Security Requirements — Hinglish mein

## Pehle requirements, phir architecture

Q3 mein sabse common mistake: students seedha architecture draw karne lagte hain. Pehle requirements likhni chahiye. Examiner pehle requirements ke marks deta hai.

## CIA+ — yaad karo ek baar

**C — Confidentiality:** Data sirf authorised logon ko dikhna chahiye. AES-256-GCM encryption + TLS 1.3.

**I — Integrity:** Data change nahi hona chahiye bina detect hue. Digital signatures, hash chains, AEAD tag.

**A — Availability:** System kaam karta rahe. Load balancing, CDN, DoS protection, DR plan.

**Authentication:** Pehle prove karo tum kaun ho. FIDO2, PKI smartcard, OIDC.

**Authorisation:** Prove karne ke baad bhi sab kuch access nahi — sirf jo tumhe allowed hai. RBAC + least privilege.

**Non-repudiation:** Jo kiya woh deny nahi kar sakte. Digital signatures + audit log.

**Privacy (GDPR):** Data minimisation, purpose limitation, right to erasure.

## Har Q3 mein auditor hota hai

Farrell har Q3 mein ek "auditor" role deta hai — koi jo check kare kya hua. Tumhe likhna chahiye:

- Auditor ke liye separate read-only access path
- Append-only audit log (delete nahi ho sakta)
- Log ko isolated server par bhejo taaki admin bhi tamper na kar sake
- Tamper-evident: hash-chained entries

## Actor classes aur unke auth mechanisms

Users → OIDC / FIDO2
Staff → PKI smartcard + MFA
Admins → MFA + jump-host + just-in-time access
APIs → mTLS + bearer token
Auditors → Read-only, alag auth, isolated

**Golden rule:** Admins ko plaintext PII access nahi hona chahiye. Separation of duties.
