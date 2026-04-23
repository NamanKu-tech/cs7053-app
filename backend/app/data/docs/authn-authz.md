<!-- MODE:EASY -->
# Authentication + Authorisation — Simple Version

**Authentication** = proving who you are.
**Authorisation** = deciding what you're allowed to do once we know who you are.

These are different things. Getting them mixed up is a common mistake.

Authentication is like showing your passport at the border. You prove your identity.
Authorisation is like having a visa for a specific country. Proving who you are doesn't mean you can go anywhere.

**Authentication factors (pick 2+ for MFA):**
- Something you **know** — password, PIN
- Something you **have** — phone (TOTP app), hardware key (YubiKey)
- Something you **are** — fingerprint, face

**MFA = Multi-Factor Authentication.** Combine two different factors. Even if someone steals your password, they can't log in without your phone.

**Modern password rules:**
- Never store passwords as plain text (obviously)
- Never use MD5 or SHA-1 to hash passwords (too fast — easy to crack)
- Use **bcrypt** or **Argon2** — they're designed to be slow on purpose so brute-forcing takes years
- Add a **salt** (random data) so two users with the same password have different hashes

**Authorisation models:**
- **RBAC** (Role-Based Access Control) — give people roles (admin, viewer, editor), assign permissions to roles
- **ABAC** (Attribute-Based Access Control) — more flexible, decisions based on attributes (time of day, location, data sensitivity)
- **Least privilege** — everyone gets the minimum they need

<!-- MODE:TECHNICAL -->
# Authentication + Authorisation (RBAC, FIDO2, OIDC)

## Authentication Spectrum

| Mechanism | Phishing resistant? | MFA factor | Typical use |
|---|---|---|---|
| Password only | No | Know | Legacy; never alone |
| TOTP (RFC 6238) | No | Have | Better than password alone |
| SMS OTP | No (SS7 attacks) | Have | Deprecated in high-security |
| FIDO2 / WebAuthn | **Yes** | Have + Are | Modern web, enterprise |
| PKI smartcard | **Yes** | Have | Government, financial |
| OIDC (OAuth2) | Depends on IdP | N/A | Federated login |
| mTLS (client cert) | **Yes** | Have | Service-to-service, API |

## Password Storage (exam must-know)

**MD5 / SHA-1 / SHA-256 for passwords = wrong.** All are fast hash functions. A GPU can compute 10+ billion SHA-256 hashes per second → 8-char passwords cracked in minutes.

**Correct approach:**
- **bcrypt** (cost factor ≥12) — adaptive; 12 rounds takes ~250ms per hash
- **Argon2id** — winner of Password Hashing Competition 2015; tunable memory + time
- **scrypt** — memory-hard
- **PBKDF2** — acceptable if iterations high enough (NIST recommends 600,000 for SHA-256)

**Salt:** Random per-user value concatenated before hashing. Same password → different hash → rainbow tables fail.

**Pepper:** Global secret added before hashing, stored separately from DB. If DB leaked, still need pepper to crack.

## FIDO2 / WebAuthn

Authenticator (YubiKey / platform): generates ECDSA key pair per origin. Private key never leaves authenticator. Registration: send public key to server. Authentication: server sends challenge; authenticator signs with private key; server verifies.

Phishing-resistant because private key is bound to the origin domain — cannot be tricked into authenticating to a lookalike domain.

## OIDC (OpenID Connect)

OAuth2 + identity layer. Server issues ID token (JWT) with user claims. Used by "Sign in with Google/GitHub." Federated identity — no need to manage passwords.

Claims in JWT: `sub` (user ID), `email`, `name`, `aud` (audience — your app ID), `exp` (expiry).

## Authorisation Models

**RBAC:** Users → Roles → Permissions. Simple, auditable. Roles: `admin`, `reader`, `editor`. Scale: fine for most systems.

**ABAC:** Policy engine evaluates attributes: user department, data classification, time, location. More flexible but complex. Used in healthcare (doctor can see own patients' records).

**Separation of duties:** Critical operations split across roles. Auditors can read but not write. Admins can write but cannot read PII. Requires collusion to abuse.

**Just-in-time (JIT) access:** Admin rights granted only for specific task, for limited time, logged. Reduces standing privilege.

<!-- MODE:HINGLISH -->
# Auth + Authz — Hinglish mein

## Pehle difference clear karo

**Authentication (AuthN):** Tum kaun ho? Prove karo. Passport dikhao.

**Authorisation (AuthZ):** Prove karne ke baad — kya karne ki permission hai? Sirf passport se kaafi nahi, visa bhi chahiye.

## Password storage — galat aur sahi

**Galat:**
- Plain text store karna — obviously nahi
- MD5 ya SHA-1 — too fast. GPU se seconds mein crack
- Plain SHA-256 — abhi bhi too fast

**Sahi:**
- **bcrypt** (cost factor ≥12) — intentionally slow, ~250ms per hash
- **Argon2id** — memory-hard, modern best choice
- **Salt** — har user ka alag random value add karo. Same password ka alag hash hoga. Rainbow tables fail.

## MFA kyun zaroori hai

Password akele kaafi nahi. Breaches mein passwords leak ho jaate hain — billions leaked on dark web. Agar MFA hai toh leaked password bhi kaam nahi karta.

**Best MFA:** FIDO2/WebAuthn (YubiKey ya phone ka biometric). Phishing-resistant — fake website par kaam nahi karta.

**Decent MFA:** TOTP app (Google Authenticator). Phishing possible lekin much better than no MFA.

**Avoid:** SMS OTP — SS7 attacks se intercept ho sakta hai.

## RBAC vs ABAC

**RBAC:** Role assign karo, role ko permissions. Simple. Admin → sab kuch. Reader → sirf read. Zyada tar systems ke liye kaafi hai.

**ABAC:** Policy engine context dekhta hai — time, location, data sensitivity, user department. Zyada flexible. Healthcare mein use hota hai (doctor apne patients ke records dekh sakta hai, doosron ke nahi).

## Exam pattern

Q3 mein har actor class ka alag auth mechanism likhna chahiye:
- Citizens/Users → OIDC ya FIDO2
- Staff → PKI smartcard + MFA
- Admins → MFA + jump-host + JIT access
- APIs → mTLS + bearer token
- Auditors → Read-only, alag authentication
