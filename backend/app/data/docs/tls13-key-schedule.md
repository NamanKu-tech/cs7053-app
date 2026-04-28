<!-- MODE:EASY -->
# TLS 1.3 Key Schedule — Simple Version

After the handshake, TLS has a shared secret. But you don't use that secret directly for encryption — you use it to *make* several different keys, each for a different job.

Think of it like a master key that opens a key cabinet, inside which are separate keys for:
- The front door (encrypting handshake messages)
- The living room (encrypting your data going to the server)
- The bedroom (encrypting data coming back from the server)
- A spare (for resumption next time)

The process of making all these keys from the original secret is called the **key schedule**.

Why separate keys for each direction? So that if someone finds one key, they only get one direction of traffic — not everything.

Why use HKDF (the "key mixing" function) instead of just using the secret directly? HKDF is designed to produce keys that look completely random even if the input had weaknesses. It's like putting ingredients through a very good blender so the output tastes uniform no matter what went in.

**The three important secrets (in order):**
1. **Early secret** — used if there's 0-RTT data
2. **Handshake secret** — encrypts the rest of the handshake (certificate, Finished messages)
3. **Master secret** — produces the final application traffic keys

That's it. You don't need to know the maths — just know the three secrets exist and what they protect.

<!-- MODE:TECHNICAL -->
# TLS 1.3 Key Schedule (HKDF)

## Overview

TLS 1.3 uses HKDF (HMAC-based Key Derivation Function, RFC 5869) to derive all keys from two inputs: the ECDHE shared secret and the handshake transcript hash.

## Key Schedule Diagram

```
0 (empty)
    |
HKDF-Extract(salt=0, IKM=0)
    |
  early_secret
    |-- client_early_traffic_secret  →  client 0-RTT write key
    |-- early_exporter_master_secret
    |
HKDF-Extract(salt=Derive(early_secret), IKM=ECDHE_shared_secret)
    |
  handshake_secret
    |-- client_handshake_traffic_secret  →  client handshake write key
    |-- server_handshake_traffic_secret  →  server handshake write key
    |
HKDF-Extract(salt=Derive(handshake_secret), IKM=0)
    |
  master_secret
    |-- client_application_traffic_secret_0  →  client app write key
    |-- server_application_traffic_secret_0  →  server app write key
    |-- exporter_master_secret
    |-- resumption_master_secret  →  PSK for next session
```

## HKDF: Extract + Expand

**HKDF-Extract(salt, IKM)** → pseudorandom key (PRK)
Combines salt (previous secret) and input key material into a fixed-length PRK.

**HKDF-Expand-Label(PRK, label, context, length)** → derived key
Takes PRK + a label string + transcript hash → produces a specific-length key.

The `label` string (e.g., `"tls13 c hs traffic"`) is what makes each derived key unique and domain-separated.

## Why Separate Client/Server Keys?

Asymmetric encryption — client encrypts with its write key, server reads with the corresponding read key. If an attacker compromises one direction's key, the other direction remains confidential.

## Why Bind to Transcript Hash?

Every key derivation includes the transcript hash (hash of all handshake messages so far). This means the keys are **session-specific** and **order-dependent** — a replay or modification of any message produces different keys and causes Finished MAC verification failure.

## Key Compromise Impact

| What is compromised | What attacker can do |
|---|---|
| ECDHE private key (ephemeral) | Nothing for past sessions (no long-term key) |
| Handshake traffic key | Decrypt cert/Finished for that session |
| Application traffic key | Decrypt that session's data only |
| Resumption PSK | All sessions using that PSK |
| Server certificate private key | Impersonate server (future sessions); cannot decrypt past (FS) |


## Relevant RFCs

- **RFC 8446** — *TLS 1.3* — Section 7 defines the full key schedule; every label, every HKDF-Expand-Label call is specified here
- **RFC 5869** — *HKDF — HMAC-based Key Derivation Function* — defines HKDF-Extract and HKDF-Expand that TLS 1.3 uses throughout; includes the security proof
- **RFC 2104** — *HMAC: Keyed-Hashing for Message Authentication* — the MAC construction underlying HKDF; understanding this is needed to follow the key schedule derivation
- **RFC 8448** — *TLS 1.3 Example Handshake Traces* — includes worked examples of key schedule outputs for specific inputs; use to check your understanding

<!-- MODE:HINGLISH -->
# TLS 1.3 Key Schedule — Hinglish mein

## Problem kya hai?

ECDHE handshake ke baad dono sides ke paas ek shared secret hai. Lekin is secret ko directly encryption ke liye use nahi karte. Kyun? Ek key sab jagah use karo toh risk zyada hota hai.

## Solution: HKDF se multiple keys banao

HKDF = ek function jo ek secret input lekar kai alag keys banata hai. Har key ka ek alag kaam.

**Teen stages hain:**

**Stage 1 — Early Secret:**
0-RTT data ke liye. Agar client pehle se server se connected hai aur PSK hai toh yeh use hota hai.

**Stage 2 — Handshake Secret:**
ECDHE shared secret aata hai. Yahan se do keys bantein hain:
- Client handshake write key (client → server encryption, handshake mein)
- Server handshake write key (server → client encryption, handshake mein)

Yahi keys Certificate, CertificateVerify, aur Finished messages ko encrypt karte hain.

**Stage 3 — Master Secret:**
Yahan se application traffic keys bantein hain:
- Client app write key (tumhara browser → server, real data)
- Server app write key (server → tumhara browser, real data)
- Resumption key (next session ke liye PSK)

## Transcript hash kyun?

Har key mein handshake transcript ka hash milaya jaata hai. Matlab: agar kisi ne handshake ka koi message badal diya toh keys alag niklenge aur Finished message verify nahi hoga. Attack detect ho jaayega.

## Exam ke liye key point

Early → Handshake → Master — yeh teen secrets yaad karo. Aur yeh bolo ki application traffic ke liye client aur server ke alag-alag keys hote hain (asymmetric) taaki ek direction compromise hone par doosra safe rahe.
