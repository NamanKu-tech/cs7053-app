<!-- MODE:EASY -->
# TLS 1.3 Handshake — Simple Version

TLS is the lock on the internet. When you see "https://" and the padlock icon, TLS is running. The *handshake* is the conversation that happens before any real data is sent — two computers agreeing on how to talk securely.

Think of it like meeting a stranger to exchange secret notes:

1. **You wave** (ClientHello) — "Hi, I can do these types of secret codes, here's my half of a key."
2. **They wave back** (ServerHello) — "Great, let's use *this* code. Here's my half of the key. Also here's my ID card to prove who I am."
3. **You verify their ID** — check their certificate is signed by someone you trust (like a government-issued ID)
4. **You both say "ready"** (Finished messages) — "I've verified everything. Let's talk."

That whole exchange takes just **one round trip** (you say something, they reply). That's why TLS 1.3 is fast.

The key you both computed is never sent over the internet — you each computed it from the same maths using your halves. An eavesdropper who recorded everything still can't figure out the key. This magic is called **Diffie-Hellman key exchange**.

After the handshake, everything is encrypted. Even someone watching the traffic sees only scrambled data.

<!-- MODE:TECHNICAL -->
# TLS 1.3 Handshake (1-RTT + 0-RTT)

## Full 1-RTT Handshake (RFC 8446)

```
Client                                           Server
------                                           ------
ClientHello
  + supported_versions (TLS 1.3)
  + key_share (X25519 public key)
  + cipher_suites (TLS_AES_128_GCM_SHA256 etc.)
  + SNI (server name)
  + early_data? (0-RTT flag)
                          ------>
                                           ServerHello
                                             + key_share (server X25519 public)
                                             + selected cipher_suite
                                           {EncryptedExtensions}
                                           {Certificate}
                                           {CertificateVerify}  ← sig over transcript
                                           {Finished}           ← HMAC of transcript
                          <------
{Finished}                ← client confirms transcript
                          ------>
[Application Data]        <=====>  [Application Data]
```

**Everything in `{}` is already encrypted** with handshake traffic keys derived from the shared ECDHE secret.

## Key Properties

- **1-RTT** — one round trip before application data flows (vs 2-RTT in TLS 1.2)
- **ECDHE only** — ephemeral keys always; no static RSA key transport (→ forward secrecy mandatory)
- **AEAD only** — AES-128-GCM, AES-256-GCM, ChaCha20-Poly1305; CBC and RC4 removed
- **No compression** — CRIME/BREACH killed compression
- **No renegotiation** — complexity source removed; use key_update instead
- **Encrypted extensions** — certificate and extensions are encrypted (unlike TLS 1.2)

## CertificateVerify — Why It Matters

The server signs the **entire handshake transcript** (hash of all messages so far), not just the certificate. This binds the cert to this specific session, preventing cross-protocol attacks.

## 0-RTT (Early Data)

Client reuses PSK (pre-shared key) from previous session. Sends early data in first flight.

**Risk:** No forward secrecy for early data. Replay attacks possible (attacker re-sends the first flight). Mitigate with: single-use tickets, server-side anti-replay (bloom filter), idempotent requests only.

## TLS 1.3 vs TLS 1.2 Key Differences

| | TLS 1.2 | TLS 1.3 |
|---|---|---|
| RTT | 2 | 1 (0 with PSK) |
| Key exchange | RSA or DHE | ECDHE only |
| Record layer | MAC-then-encrypt (CBC) or AEAD | AEAD only |
| Encryption of handshake | Partial | Most messages encrypted |
| Forward secrecy | Optional | Mandatory |

<!-- MODE:HINGLISH -->
# TLS 1.3 Handshake — Hinglish mein

## TLS kya hai?

Jab tum kisi website ko https:// se open karte ho, TLS chal raha hota hai. Yeh ek lock jaisa hai jo internet par tumhari aur website ki baat ko private rakhta hai.

Handshake = wo conversation jo real data bhejne se pehle hoti hai. Dono computers ek dusre se milte hain aur decide karte hain kaise baat karni hai.

## 1-RTT handshake — simple flow

**Step 1 — Client bolta hai (ClientHello):**
"Mujhe yeh cipher suites support karte hain. Yeh mera key_share hai (X25519 public key). Mujhe TLS 1.3 chahiye."

**Step 2 — Server reply karta hai:**
"Theek hai, yeh cipher use karte hain. Yeh mera key_share. Mera certificate lo — dekhlo main real hoon. Mera Finished message bhi lo."

Certificate verify hota hai trusted CA se (jaise government ID card ko trust karte hain).

**Step 3 — Client Finished bhejta hai:**
"Sab verify ho gaya. Shuru karte hain."

**Total = 1 round trip.** TLS 1.2 mein 2 trips lagte the. TLS 1.3 faster hai.

## Key points jo exam mein kaam aayenge

- Keys kabhi bhi directly internet par nahi bheji jaatein. Dono sides same maths se key compute karte hain. Eavesdropper traffic record kar le fir bhi key nahi nikaal sakta. Yeh **ECDHE** (Elliptic Curve Diffie-Hellman) hai.

- **Forward secrecy mandatory** — har session ke naye keys. Purani keys leak ho bhi jaayein toh purani traffic decrypt nahi hogi.

- **AEAD only** — AES-GCM ya ChaCha20. CBC hata diya gaya (Lucky13 attack ki wajah se).

- **Certificate signature handshake transcript par hai** — sirf certificate par nahi. Isse cross-protocol attacks nahi hote.

## 0-RTT — fast but risky

PSK (previous session key) use karke first message mein hi data bhejo. Fast hai but replay attack possible hai. Important data 0-RTT mein mat bhejo.
