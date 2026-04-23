<!-- MODE:EASY -->
# Named TLS Attacks — Simple Version

These are famous attacks on TLS that you must be able to name and explain in one sentence. Think of them as a hall of fame of things that went wrong.

**BEAST (2011)** — Found a way to predict what was inside an encrypted message by watching what changed. Affected TLS 1.0's CBC mode. Fixed by upgrading to TLS 1.1+ or using AEAD.

**CRIME / BREACH (2012–13)** — If you compress data before encrypting it, and an attacker can inject some text, they can guess the rest by watching whether the compressed size goes up or down. Like playing hot/cold to find a word. TLS 1.3 removed compression.

**Lucky13 (2013)** — CBC decryption took slightly longer when padding was wrong. An attacker could time the response and figure out the plaintext one byte at a time. Fixed by AEAD-only in TLS 1.3.

**POODLE (2014)** — Even if your server supports TLS, attackers could force a downgrade to the ancient SSLv3, which had a padding oracle. TLS 1.3 has no downgrade path.

**Heartbleed (2014)** — A bug in OpenSSL let attackers ask the server to send back more memory than they should. Like asking for a 1-word echo and getting 64KB of memory back, which might contain private keys. Patch immediately. Servers need to rotate all certificates.

**FREAK / Logjam (2015)** — Old "export-grade" crypto from the 1990s (required by US law back then) was still accepted by servers. Attackers forced the connection to use this weak crypto, then broke it in hours. Fixed by never accepting export cipher suites.

**DROWN (2016)** — SSLv2 was still enabled on some servers. Attackers used SSLv2's known weaknesses to decrypt TLS connections that used the same RSA key. Fix: disable SSLv2 entirely.

**ROBOT (2017)** — Bleichenbacher's 1998 padding oracle attack came back. Several major vendors still had RSA PKCS#1 v1.5 implementations that leaked information through error responses.

**Raccoon (2020)** — Subtle timing attack against finite-field DH. Fix: use ECDHE (X25519) instead.

**TLStorm (2022)** — Memory corruption bugs in TLS parser used in APC UPS devices. Shows that even good protocols fail if the implementation is buggy.

<!-- MODE:TECHNICAL -->
# Named TLS Attacks

## Quick Reference Card (memorise for exam)

| Attack | Year | Target | Mechanism | TLS 1.3 fix |
|---|---|---|---|---|
| BEAST | 2011 | TLS 1.0 CBC | Predictable IV → chosen-plaintext XOR | AEAD-only (no CBC) |
| CRIME | 2012 | TLS compression | Compression ratio side-channel | No compression |
| BREACH | 2013 | HTTP compression | Same but at HTTP layer | Not fully fixed by TLS |
| Lucky13 | 2013 | CBC MAC-then-encrypt | MAC verification timing oracle | AEAD-only |
| POODLE | 2014 | SSLv3 CBC | Padding oracle on downgrade | No SSLv3/downgrade |
| Heartbleed | 2014 | OpenSSL heartbeat | OOB read — returns up to 64KB server memory | Unrelated to protocol |
| goto fail | 2014 | Apple SecureTransport | Missing `{}`; always-true signature check | Code review |
| FREAK | 2015 | Export RSA | Downgrade to 512-bit RSA | No export suites |
| Logjam | 2015 | Export DHE | Downgrade to 512-bit DH; precompute DL | No export suites; ECDHE |
| SLOTH | 2016 | MD5 in TLS 1.2 PRF | Transcript collision → impersonation | SHA-256 only |
| DROWN | 2016 | SSLv2 shared RSA key | Cross-protocol oracle → decrypt TLS | Disable SSLv2; no shared keys |
| ROBOT | 2017 | PKCS#1 v1.5 RSA | Bleichenbacher padding oracle resurfaced | No RSA key transport |
| Raccoon | 2020 | Finite-field DHE | Timing of leading-zero handling | ECDHE; no FF-DHE |
| TLStorm | 2022 | APC UPS TLS parser | Memory corruption in embedded TLS impl | Implementation fix |

## Deep Dives for Sub-parts

### Bleichenbacher / ROBOT
Server response differs for correctly vs incorrectly padded PKCS#1 v1.5 RSA. Attacker sends ~2²⁰ crafted ciphertexts, observing error responses to recover pre-master secret.

TLS 1.3 removes RSA key transport entirely → attack impossible.

### Lucky13
TLS 1.2 CBC: HMAC computation time depended on padding length. Attacker measured response time to determine padding byte values → byte-by-byte plaintext recovery.

Fix (in TLS 1.3): AEAD produces a fixed-time authentication tag. No padding. No MAC-then-encrypt.

### Heartbleed (CVE-2014-0160)
OpenSSL heartbeat extension: client says "echo back N bytes." No bounds check — server returns N bytes from heap, potentially including private key material, session tickets, passwords. ~17% of HTTPS servers affected at disclosure.

Not a protocol flaw — implementation bug. Still requires certificate rotation even after patching (key may already be leaked).

### DROWN
SSLv2 allows export cipher suites and has a different padding format. Attacker uses SSLv2 oracle to decrypt TLS RSA-key-transport sessions sharing the same certificate private key. 33% of HTTPS servers vulnerable at 2016 disclosure.

<!-- MODE:HINGLISH -->
# Named TLS Attacks — Hinglish mein

Yeh attacks exam mein naam se poochhe jaate hain. Har ek ko ek line mein explain karna aana chahiye.

## Attack flashcards — rapid fire

**BEAST (2011):** CBC mode mein IV predictable tha. Attacker chosen-plaintext attack se decrypt kar sakta tha. Fix: AEAD.

**CRIME/BREACH (2012-13):** Compression + encryption saath hoti thi. Compression ratio se plaintext guess kar sakte the. Fix: compression hata do.

**Lucky13 (2013):** CBC MAC check slow hota tha jab padding galat hoti. Timing se plaintext byte by byte nikaal sakte the. Fix: AEAD (constant-time).

**POODLE (2014):** Attacker connection ko SSLv3 par downgrade karta tha (jo broken tha). SSLv3 mein padding oracle tha. Fix: SSLv3 disable.

**Heartbleed (2014):** OpenSSL mein bug tha. Client "64KB echo karo" bolta tha, server memory leak ho jaati thi — jisme private keys bhi ho sakti thi. Fix: patch + saare certificates rotate karo.

**FREAK / Logjam (2015):** 1990s ke zamane ke "export grade" weak crypto (512-bit RSA/DH) abhi bhi accept ho rahe the. Attacker downgrade karta tha fir break karta tha. Fix: weak cipher suites disable.

**DROWN (2016):** SSLv2 abhi bhi enable tha kuch servers par. SSLv2 ka oracle use karke TLS traffic decrypt ho sakti thi agar same RSA key share ho. Fix: SSLv2 disable karo.

**ROBOT (2017):** Bleichenbacher ka 1998 wala attack wapas aaya. PKCS#1 v1.5 RSA padding oracle. Fix: RSA key transport hata do (TLS 1.3 ne hata diya).

**Raccoon (2020):** DH timing attack. Fix: ECDHE use karo.

**TLStorm (2022):** APC UPS devices mein TLS parser mein memory corruption. Good protocol, buggy implementation.

## Exam strategy

Q2 sub-part mein "side-channel attacks" poochhen toh: Lucky13 + Bleichenbacher/ROBOT + Raccoon. "Implementation bugs" poochhen toh: Heartbleed + goto fail + TLStorm. "Downgrade attacks" poochhen toh: POODLE + FREAK + Logjam + DROWN.
