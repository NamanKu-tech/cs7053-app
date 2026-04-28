<!-- MODE:EASY -->
# Post-Quantum Cryptography in TLS — Simple Version

Normal computers use maths that quantum computers would solve easily. Most of the internet's security relies on two hard problems: factoring huge numbers (RSA) and solving discrete logarithms (Diffie-Hellman). A powerful enough quantum computer would break both in minutes.

**Shor's algorithm** is the quantum algorithm that breaks RSA and DH. We don't have a quantum computer powerful enough to run it yet, but we might in 10–30 years.

**Grover's algorithm** is another quantum algorithm that would halve the effective key length of symmetric encryption (AES). AES-256 would become as strong as AES-128 is today. Not broken, just weakened.

**The plan:**
- Switch from RSA/ECDH to "post-quantum" alternatives for key exchange
- NIST ran a competition and picked winners in 2024:
  - **Kyber (ML-KEM)** — new key exchange algorithm that quantum computers can't break
  - **Dilithium (ML-DSA)** — new signature algorithm

**What's already deployed:**
Chrome and Cloudflare already use **X25519Kyber768** — a *hybrid* of the old (X25519) and new (Kyber) algorithms. If either one is secure, the whole thing is secure. Belt-and-suspenders approach during transition.

**Why hybrid?**
Because we're not 100% sure Kyber doesn't have undiscovered weaknesses. So we keep ECDH alongside it. Worst case: we're no worse off than today.

**The problem with signatures:**
PQ signature schemes like Dilithium produce much larger signatures and keys. TLS certificates use signatures. Bigger certs = bigger handshakes = slower connections. This is why key exchange migrated first but signature migration is slower.

<!-- MODE:TECHNICAL -->
# Post-Quantum Cryptography (PQC) Migration in TLS

## Why PQC?

**Shor's algorithm** (quantum): factors RSA moduli and solves discrete logarithms in polynomial time. Breaks RSA, DH, ECDH, ECDSA.

**Grover's algorithm** (quantum): searches unsorted databases in O(√N) time. Halves effective symmetric key length. AES-128 → 64-bit security; AES-256 → 128-bit (still acceptable).

**Timeline:** No known quantum computer can run Shor against 2048-bit RSA today. Estimates: 10–20 years for "cryptographically relevant" quantum computer. **Store-Now-Decrypt-Later (SNDL)** means adversaries are recording traffic today to decrypt when quantum computers arrive.

## NIST PQC Selections (August 2024)

| Algorithm | Type | Based on | TLS use |
|---|---|---|---|
| ML-KEM (Kyber) | KEM | Module lattice | Key exchange |
| ML-DSA (Dilithium) | Signature | Module lattice | Certificate signing |
| SLH-DSA (SPHINCS+) | Signature | Hash-based | Certificate signing (backup) |
| FN-DSA (Falcon) | Signature | NTRU lattice | Certificate signing |

## Current Deployment: Hybrid X25519Kyber768

**Chrome 116+ and Cloudflare (2023–2024):** TLS key exchange uses `X25519Kyber768Draft00` — concatenate X25519 and Kyber768 key shares; combine shared secrets via KDF.

**Security property:** If *either* X25519 or Kyber is secure, the combined key is secure. Protects against: (a) Kyber having undiscovered weakness, (b) quantum computer breaking X25519.

**IANA codepoint:** `0x6399`

## Why Signature Migration Lags

| | ECDSA P-256 cert | ML-DSA cert | Dilithium3 |
|---|---|---|---|
| Public key size | 64 bytes | 1,952 bytes | 1,952 bytes |
| Signature size | ~72 bytes | 3,293 bytes | 3,293 bytes |
| Handshake impact | Minimal | +5–10KB per chain | Significant |

Larger certs increase TLS handshake size, causing TCP fragmentation, requiring EDNS0-style extensions, slowing TTFB. Root CA programs need to support PQ certs before deployment.

## Exam Answer Pattern

"For Q2's 'how would you future-proof TLS': deploy hybrid X25519+Kyber768 for key exchange (already standard in Chrome/Cloudflare); plan ML-DSA for certificate signatures once size constraints are resolved; upgrade symmetric to AES-256 (Grover halves key strength); document SNDL threat to justify urgency."


## Relevant RFCs

- **RFC 8446** — *TLS 1.3* — the extensibility mechanisms (NamedGroup, KeyShare) that PQC algorithms plug into without changing the handshake structure
- **RFC 9180** — *Hybrid Public Key Encryption (HPKE)* — the building block used in Encrypted Client Hello and proposed PQC hybrid constructions
- **draft-ietf-tls-hybrid-design** — *Hybrid Key Exchange in TLS 1.3* — IETF draft defining how to combine classical (X25519) + PQC (ML-KEM) key exchange in a single handshake
- **NIST FIPS 203** — *ML-KEM (Kyber)* — the standardised lattice-based KEM; the algorithm being added to TLS via the hybrid draft

<!-- MODE:HINGLISH -->
# PQC in TLS — Hinglish mein

## Problem simple mein

Aaj ka internet RSA aur ECDH par depend karta hai. Yeh dono is assumption par safe hain ki kuch maths problems bahut hard hain.

Quantum computers ke saath yeh assumption toot jaayegi. **Shor's algorithm** RSA aur ECDH dono ko polynomial time mein break kar sakta hai. Abhi hum ke paas itna powerful quantum computer nahi — lekin 10-20 saal mein ho sakta hai.

## SNDL — yaad karo

**Store-Now-Decrypt-Later.** Intelligence agencies abhi encrypted traffic record kar rahi hain. Jab quantum computer ready hoga, decrypt kar lenge. Yeh already ho raha hai.

Isliye migration urgent hai — wait karo toh purana traffic retroactively exposed hoga.

## NIST ne kya choose kiya (2024)

**ML-KEM (Kyber)** — key exchange ke liye. TLS mein yeh ECDH replace karega.

**ML-DSA (Dilithium)** — signatures ke liye. Certificates ke liye.

Dono lattice-based hain — quantum computers ke liye hard problems.

## Abhi kya deployed hai?

Chrome aur Cloudflare ne **X25519Kyber768** launch kiya — hybrid approach.

Hybrid = X25519 (purana ECDH) + Kyber768 (naya PQC) dono saath. Agar dono mein se koi ek secure hai toh connection secure hai. Safe transition strategy.

## Signatures kyun slow hain?

Kyber keys = chhoti. Dilithium signatures = bahut badi (3293 bytes vs ECDSA ke ~72 bytes). TLS handshake heavy ho jaata hai. Isliye key exchange ne pehle migrate kiya, signatures abhi bhi pending.

## Exam line

"Future-proof TLS ke liye: hybrid X25519+Kyber768 deploy karo (already Chrome/Cloudflare mein), AES-256 use karo (Grover protection), ML-DSA signatures plan karo jab size issue solve ho. SNDL threat justify karta hai ki yeh ab karna urgent hai."
