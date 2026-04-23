<!-- MODE:EASY -->
# TLS Record Layer + AEAD — Simple Version

The record layer is the part of TLS that actually wraps your data before sending it. Think of it like an envelope factory — every piece of data gets sealed in a special envelope before it goes over the internet.

The old way (TLS 1.2 with CBC): First seal the envelope, then put a wax seal on the outside. Problem: the wax seal was checked *before* opening the envelope. Attackers could poke the envelope in clever ways to figure out what was inside without ever breaking the wax. This is called a **padding oracle attack** (Lucky13, POODLE).

The new way (TLS 1.3 with AEAD): Everything is done in one operation. Seal and verify at the same time. There's no separate "check the wax seal" step. Poking the envelope tells you nothing.

**AEAD** stands for "Authenticated Encryption with Associated Data." It means:
- The data is **encrypted** (confidential — no one can read it)
- The data is **authenticated** (integrity — no one can change it without being caught)
- Both happen at the same time in the same operation

TLS 1.3 uses:
- **AES-128-GCM** or **AES-256-GCM** — fast, hardware-accelerated on most CPUs
- **ChaCha20-Poly1305** — fast in software, great for phones and low-power devices

This one change (AEAD-only) is why TLS 1.3 killed BEAST, Lucky13, and POODLE in one shot.

<!-- MODE:TECHNICAL -->
# TLS 1.3 Record Layer + AEAD

## Record Layer Structure

Each TLS record:
```
struct {
    ContentType type;          // 1 byte  (application_data = 23)
    ProtocolVersion legacy;    // 2 bytes (always 0x0303 for compat)
    uint16 length;             // 2 bytes (max 2^14 + 256 bytes)
    opaque encrypted_record[length];  // AEAD ciphertext + tag
} TLSCiphertext;
```

The actual content type is hidden inside the encrypted payload (inner content type). The outer header always shows `application_data` — even for handshake records after ServerHello — preventing traffic analysis of record types.

## AEAD Operation (AES-128-GCM example)

```
Input:  plaintext || inner_content_type
AAD:    TLSCiphertext header (5 bytes — type, version, length)
Nonce:  record_iv XOR sequence_number  (sequence number is implicit)
Output: ciphertext || 16-byte authentication tag
```

**Encrypt:** AES-GCM encrypts plaintext; simultaneously computes a 128-bit GMAC tag over AAD + ciphertext.

**Decrypt:** Verify tag first; if valid, decrypt. Tag failure → immediately discard, send `bad_record_mac` alert.

Tag verification is **constant-time** — no timing oracle. This killed Lucky13.

## Why MAC-then-Encrypt Was Wrong

TLS 1.2 CBC mode: `encrypt(plaintext || MAC)` → attacker can query padding validity → timing oracle → byte-by-byte decryption without the key (Lucky13, BEAST, POODLE).

TLS 1.3 AEAD: `AEAD_encrypt(plaintext)` → no padding; tag covers everything; tag failure is indistinguishable from wrong key → no oracle.

## Removed from TLS 1.3 and Why

| Removed | Reason |
|---|---|
| CBC cipher suites | Padding oracle family (Lucky13, BEAST, POODLE) |
| RC4 | Biases in keystream; broken since 2013 |
| MD5 / SHA-1 in PRF | Collision vulnerabilities |
| Compression | CRIME/BREACH side-channel |
| Export cipher suites | FREAK, Logjam downgrade attacks |
| RSA key transport | No forward secrecy |

## Cipher Suites in TLS 1.3 (only 5 allowed)

- `TLS_AES_128_GCM_SHA256`
- `TLS_AES_256_GCM_SHA384`
- `TLS_CHACHA20_POLY1305_SHA256`
- `TLS_AES_128_CCM_SHA256`
- `TLS_AES_128_CCM_8_SHA256`

<!-- MODE:HINGLISH -->
# TLS Record Layer + AEAD — Hinglish mein

## Record layer kya karta hai?

Jab bhi data TLS ke through jaata hai, record layer usse wrap karta hai — encrypt bhi karta hai aur integrity bhi ensure karta hai. Ek hi operation mein dono kaam.

## AEAD kya hai aur kyun better hai?

**Old TLS 1.2 ka tarika (MAC-then-Encrypt):**
Pehle data encrypt karo. Phir upar se MAC (integrity check) lagao. Problem: MAC ko check karte waqt attackers clever tricks se pata kar sakte the ki plaintext mein kya tha, bina key ke. Yahi Lucky13, BEAST, POODLE attacks the.

**TLS 1.3 ka tarika (AEAD):**
Encrypt karo aur authenticate karo ek hi saath, ek hi function mein. Koi separate MAC nahi. Koi padding nahi. Attack surface zero.

**AEAD = Authenticated Encryption with Associated Data**
- Data encrypted (confidential)
- Data authenticated (integrity — koi badal nahi sakta)
- Dono ek hi step mein

## TLS 1.3 mein kya allowed hai?

Sirf AEAD cipher suites:
- **AES-128-GCM** ya **AES-256-GCM** — hardware mein bahut fast (modern CPUs mein AES instructions hote hain)
- **ChaCha20-Poly1305** — software mein fast, mobile devices ke liye perfect

## Kya kya hata diya aur kyun

**CBC** — Lucky13, BEAST, POODLE (padding oracle)
**RC4** — biased keystream, broken
**Compression** — CRIME/BREACH (length side-channel)
**RSA key transport** — no forward secrecy
**Export ciphers** — FREAK, Logjam (downgrade to weak crypto)

## Exam line

"TLS 1.3 sirf AEAD cipher suites allow karta hai — AES-GCM ya ChaCha20-Poly1305. CBC hata diya gaya jo Lucky13 aur POODLE attacks ko kill karta hai. Koi padding oracle possible nahi."
