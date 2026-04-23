<!-- MODE:EASY -->
# Forward Secrecy — Simple Version

Imagine you and a friend pass notes in class. You write a new secret code for each note. After reading it, you both burn your copy of that code.

Now even if someone later finds *all your old notes*, they can't read them — the codes are gone.

That's forward secrecy. Every session gets its own temporary key that gets deleted after the session ends.

**The old way (no forward secrecy):**
Banks and websites used one big private key for years. Your browser would encrypt everything with that key. If a hacker stole that key years later, they could go back and decrypt all the old traffic they had saved.

**The new way (forward secrecy):**
Each connection generates a fresh, temporary key. The website never "knows" this key in a way they could save it. After the connection ends, the key is gone forever. Saved traffic is permanently unreadable.

**Why does this matter?**

The NSA (and probably others) recorded massive amounts of internet traffic for years, hoping to eventually get the private keys and decrypt it. With forward secrecy, that plan fails — the keys no longer exist.

**TLS 1.3 makes forward secrecy mandatory.** There's no option to turn it off. TLS 1.2 had it as optional, and many servers didn't use it.

**Key compromise scenarios:**
- Server's certificate private key stolen → attacker can *impersonate* the server in future connections, but cannot decrypt *past* traffic (forward secrecy protects it)
- Session key stolen → only that one session is affected

<!-- MODE:TECHNICAL -->
# Forward Secrecy + Key Compromise Impact

## Definition

**Perfect Forward Secrecy (PFS):** Compromise of long-term private keys does not compromise past session keys.

Achieved by using **ephemeral** Diffie-Hellman (DHE or ECDHE) for key agreement. Each session generates a fresh ephemeral key pair, discarded after the session.

## Why RSA Key Transport Lacked FS

TLS 1.2 RSA mode: client generates pre-master secret, encrypts it with server's certificate public key, sends it. Server decrypts with private key.

**Problem:** If the server's private key is compromised later (or was already compromised), an attacker who recorded past traffic can now decrypt all of it retroactively. The pre-master secret was always present in the recorded traffic, just encrypted.

## TLS 1.3 Solution

ECDHE only. Server's certificate private key is used only for the `CertificateVerify` signature — it never touches the key material. Key material flows exclusively through the ephemeral ECDHE exchange. The private key's compromise cannot expose session keys.

## Key Compromise Scenarios

| What is compromised | Impact | FS protects? |
|---|---|---|
| Server certificate private key | Impersonation (future sessions); cannot decrypt past traffic | Yes — past sessions safe |
| Ephemeral ECDHE private key | Only that session (key discarded immediately after) | N/A — already ephemeral |
| Session (application traffic) key | That session's plaintext only | — |
| PSK (resumption ticket) | All sessions using that PSK — both past and future | No — PSK compromise is retroactive |
| CA root key | Impersonation via forged certificates | Depends on revocation response |

## Logjam (2015) — FS Weakened by Export DH

DHE with 512-bit (export-grade) DH parameters is crackable in hours. Many servers accepted export DH even in "strong" mode due to misconfiguration. Attacker downgrades the handshake to export DHE, then precomputes the discrete log.

Fix: minimum 2048-bit DH parameters; prefer ECDHE (X25519) over finite-field DHE.

## Store-Now-Decrypt-Later (SNDL)

Nation-state adversaries record encrypted traffic now, expecting to decrypt it when quantum computers can break RSA/ECDH. Forward secrecy does not protect against this if the *session key* itself can be broken (it's AES-symmetric, so Grover's halves the key strength — AES-128 becomes 64-bit effective). Mitigation: upgrade to AES-256 + hybrid PQC key exchange.

<!-- MODE:HINGLISH -->
# Forward Secrecy — Hinglish mein

## Simple analogy

Soch lo tum aur friend ek secret code likhte ho har note ke liye, aur padhne ke baad code ko jalaa dete ho. Agar koi baad mein tumhare saare purane notes bhi steal kar le, toh bhi padh nahi sakta kyunki codes exist hi nahi karte.

Yahi forward secrecy hai.

## Problem with old TLS (no FS)

Purani TLS mein server ke paas ek long-term private key hoti thi. Browser us key se session key encrypt karke bhejta tha. Agar koi badmaash 5 saal baad bhi us private key ko chura le, toh woh 5 saal purani traffic bhi decrypt kar sakta tha jo usne record kar rakhi thi.

NSA aur duniya bhar ki intelligence agencies exactly yahi kar rahi thi — traffic record karo, baad mein decrypt karo jab key mile.

## TLS 1.3 ka solution

Har session ke liye **ephemeral ECDHE** keys generate hote hain. Session khatam hone ke baad keys delete. Certificate ki private key sirf signature ke liye use hoti hai — key material se kabhi nahi milti.

Ab chahe server ka certificate key koi chura le — purani traffic safe hai.

## Key compromise scenarios yaad karo

**Certificate private key compromised:** Server ko impersonate kar sakte ho future sessions mein. Lekin past traffic? Safe. (Forward secrecy ne protect kiya.)

**Ephemeral key compromised:** Sirf woh ek session. Key already delete ho chuki thi. Minimal damage.

**PSK (session resumption ticket) compromised:** Yahan FS kaam nahi karta. Woh PSK use karne wale saare sessions exposed.

## Exam ke liye

"TLS 1.3 mein forward secrecy mandatory hai — ECDHE only, RSA key transport nahi. Certificate key compromise sirf future impersonation enable karta hai, past sessions safe rehti hain."
