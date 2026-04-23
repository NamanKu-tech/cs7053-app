<!-- MODE:EASY -->
# Crypto in System Design — Simple Version

When you're designing a real system, you need to make decisions about cryptography. You don't need to invent new crypto — just pick the right tools and use them correctly.

**The main questions:**

**1. What do I encrypt?**
- Data *in transit* (moving between systems) → TLS 1.3
- Data *at rest* (stored in databases, files, backups) → AES-256-GCM
- Data *in use* is the hardest (it's usually plaintext in memory while being processed)

**2. Where do I keep the keys?**
Never keep keys next to the data they encrypt. That's like locking your door and hiding the key under the doormat.

The best solution: a **Hardware Security Module (HSM)** — a special piece of hardware that stores keys and does cryptography, but never lets the raw key out. Even if an attacker owns your server, they can't extract the key from the HSM.

**3. What happens when I need to change keys?**
Keys should rotate regularly (e.g., every year). Rotate means: generate a new key, re-encrypt data with the new key, retire the old key.

**4. Digital signatures — why use them?**
If you need to prove that a document was created by a specific person and hasn't been changed, use digital signatures. Like a wax seal but mathematically impossible to fake.

**5. What NOT to do:**
- Don't roll your own crypto
- Don't use MD5 or SHA-1 for anything security-sensitive
- Don't hardcode keys in source code
- Don't use ECB mode for AES (it leaks patterns)

<!-- MODE:TECHNICAL -->
# Cryptography in System Design (HSM, key rotation)

## Encryption Choices by Use Case

| Use case | Algorithm | Notes |
|---|---|---|
| Data in transit | TLS 1.3 (AES-128-GCM or ChaCha20-Poly1305) | Never roll your own; use well-audited libraries |
| Data at rest | AES-256-GCM | Authenticated encryption; nonce must be unique per encryption |
| Password storage | Argon2id or bcrypt ≥12 rounds | Never SHA-256 direct |
| Digital signatures | ECDSA P-256 or Ed25519 | RSA-2048 minimum if RSA required; prefer elliptic curve |
| Key wrapping | AES-256-GCM or RSA-OAEP | Key encrypting key (KEK) pattern |
| Hashing | SHA-256 / SHA-3 | MD5 and SHA-1 deprecated |
| Symmetric key exchange | ECDHE (X25519) | Mandatory ephemeral in TLS 1.3 |

## Key Management Architecture

**Key Hierarchy:**
```
Root Key (Hardware Security Module — never leaves)
  ↓
Key Encrypting Key (KEK) — wraps data encryption keys
  ↓
Data Encryption Key (DEK) — encrypts actual data
```

**HSM (Hardware Security Module):**
- FIPS 140-2 Level 3+ for government/financial
- Keys generated inside HSM; never exported in plaintext
- All crypto operations performed inside hardware
- Tamper-evident / tamper-resistant: physical attack triggers key zeroisation
- Cloud HSMs: AWS KMS, GCP Cloud KMS, Azure Key Vault (backed by HSMs)

**Key Rotation:**
- Rotate DEKs periodically (quarterly or annually) and on suspected compromise
- Re-encrypt data under new key; old key kept for decryption of backups for retention period
- Rotation of signing keys: pre-publish new key before retiring old (DNSSEC-style)

## Nonce Management (Critical for AES-GCM)

AES-GCM requires unique 96-bit nonce per encryption under the same key. **Nonce reuse = catastrophic** — reveals XOR of plaintexts and compromises authentication key.

Approaches:
- Random 96-bit nonce (collision probability: ~1/2³² after 2³² operations — rotate key before that)
- Counter nonce (deterministic but requires state; never reuse after crash)
- Deterministic Nonce Misuse Resistant AEAD (AES-GCM-SIV) — nonce reuse doesn't catastrophically fail

## End-to-End Encryption (E2EE)

Server never sees plaintext. Keys generated/held by end users only. Examples: Signal (Double Ratchet), WhatsApp, iMessage.

**Trade-off:** Server cannot scan content (good for privacy; bad for abuse detection). Key recovery on device loss is hard.

## Common Implementation Mistakes

- **ECB mode:** each block encrypted independently → identical plaintext blocks produce identical ciphertext → pattern leakage (famous penguin image)
- **Hardcoded keys in source:** leaked via git history; rotate immediately if found
- **Using random() for crypto:** use `os.urandom()` / `crypto.getRandomValues()` / `SecureRandom`
- **Not validating AEAD tag:** decrypting before checking tag → padding oracle behaviour

<!-- MODE:HINGLISH -->
# Crypto in Systems — Hinglish mein

## Teen basic questions

**Kya encrypt karein?**
- Transit mein data → TLS 1.3
- Rest mein data (DB, files, backups) → AES-256-GCM
- Passwords → Argon2id ya bcrypt (hashing, encryption nahi)

**Keys kahaan rakhein?**
Data ke paas mat rakhna. Best option: **HSM** (Hardware Security Module) — ek special hardware jahan keys kabhi bahar nahi nikalti, even if server compromised ho jaaye.

**Keys kab change karein?**
Rotate karo. Quarterly ya yearly. Agar compromise suspected ho toh turant. New key se re-encrypt karo, purani key backup retention ke liye rakhlo.

## HSM kyun important hai

HSM = ek black box. Keys andar generate hoti hain, kabhi bahar nahi aatein. Tumhara app HSM se bolti hai "please yeh sign karo" — HSM sign karta hai aur result deta hai. Private key ka access kabhi nahi milta.

Cloud mein: AWS KMS, GCP Cloud KMS, Azure Key Vault — sab HSM-backed hain.

## AES-GCM ka important rule

Nonce (initialization vector) har baar unique honi chahiye. Ek hi key ke saath agar ek hi nonce dobara use karo → catastrophic failure. Plaintext leak, authentication break.

Fix: random 96-bit nonce (2³² operations se pehle key rotate karo) ya counter-based nonce.

## Galtiyan jo avoid karni hain

**ECB mode:** Identical blocks → identical ciphertext. Pattern leakage. AES-GCM use karo.

**Hardcoded keys:** Source code mein key mat daalo. Git history mein rahegi forever. Secrets manager use karo.

**Fast hash for passwords:** SHA-256 fast hai. Attacker 10 billion hashes/sec crack kar sakta hai. Bcrypt ya Argon2 use karo — intentionally slow hote hain.

## Exam ke liye

Q3 mein crypto choices always include: TLS 1.3 in transit, AES-256-GCM at rest, keys in HSM, key rotation policy, digital signatures for non-repudiation. Yeh mention karo aur marks pakke.
