<!-- MODE:EASY -->
# Email Security — Simple Version

Email was invented in the 1970s with zero security. Anyone could send an email claiming to be anyone. I could send you an email "from" your bank, your boss, or the President — and your email client would show it as genuine.

Three technologies were invented to fix this. They all live in DNS, which is why they come up in this course.

**SPF (Sender Policy Framework)** — "Only these servers are allowed to send email for my domain"

Imagine a restaurant publishing a list: "Only our vans with these licence plates are authorised to deliver food in our name." If a random van shows up claiming to be us, it's fraud.

SPF is that list, published in DNS. When you get an email from `@tcd.ie`, the receiving server looks up TCD's SPF record and checks: "Did this email actually come from a server TCD authorised?" If not, it's probably spam or phishing.

**DKIM (DomainKeys Identified Mail)** — "I cryptographically signed this email"

SPF checks where the email came from. DKIM checks whether the content was signed by the real sender.

It's like a wax seal on an envelope — proves the letter came from someone with the right seal and hasn't been opened.

**DMARC** — "Here's what to do if SPF or DKIM fails"

SPF and DKIM alone don't tell receivers what to do with suspicious emails. DMARC says: "If our SPF/DKIM checks fail, reject the email / send it to spam / just report it to us."

Together, these three stop most email spoofing and phishing.

<!-- MODE:TECHNICAL -->
# Email Security: SPF, DKIM, DMARC

## Why Email Authentication Matters

Original SMTP (RFC 821, 1982): no authentication. Any server can claim any `MAIL FROM:` address. Phishing, spoofing, BEC (business email compromise) attacks all exploit this. DNS-based email authentication adds sender verification without modifying SMTP.

## SPF (Sender Policy Framework) — RFC 7208

DNS TXT record listing authorized sending IP ranges/hosts for a domain.

```
tcd.ie. TXT "v=spf1 ip4:134.226.0.0/16 include:spf.protection.outlook.com -all"
```

**Mechanism:**
- Receiving MTA extracts `MAIL FROM` (envelope sender) domain
- Queries DNS for TXT record: `tcd.ie TXT`
- Checks if sending IP is in the authorized list
- Result: `pass`, `fail`, `softfail`, `neutral`, `none`, `temperror`, `permerror`

**Qualifiers:**
- `-all` = reject if not listed (hard fail)
- `~all` = softfail (mark as suspicious, typically accepted)
- `?all` = neutral (no policy)
- `+all` = allow everything (useless, don't do this)

**SPF limitation:** Checks envelope sender (`MAIL FROM`), not the `From:` header user sees. Forwarded mail breaks SPF — the forwarding server's IP isn't in the original domain's SPF record.

## DKIM (DomainKeys Identified Mail) — RFC 6376

Cryptographic signature over email headers + body, published public key in DNS.

**Signing (sender side):**
1. Select headers to sign (From, Subject, Date, etc.) + body hash
2. Sign with RSA/Ed25519 private key
3. Add `DKIM-Signature:` header to outgoing email

```
DKIM-Signature: v=1; a=rsa-sha256; d=tcd.ie; s=selector1;
  h=from:to:subject:date; bh=[body_hash]; b=[signature]
```

**Verification (receiver side):**
1. Extract `d=` (domain) and `s=` (selector) from DKIM-Signature
2. Query DNS: `selector1._domainkey.tcd.ie TXT` → public key
3. Verify signature over specified headers + body hash

**Key storage in DNS:**
```
selector1._domainkey.tcd.ie. TXT "v=DKIM1; k=rsa; p=[base64_public_key]"
```

**DKIM advantage over SPF:** Survives email forwarding — signature travels with the message. Signs specific headers including `From:` (what user sees). Provides message integrity.

**DKIM limitation:** Doesn't specify what to do on failure. Doesn't prevent replay (attacker can replay a valid DKIM-signed email).

## DMARC (Domain-based Message Authentication, Reporting & Conformance) — RFC 7489

Policy layer on top of SPF and DKIM. Specifies: what to do on failure, plus reporting.

```
_dmarc.tcd.ie. TXT "v=DMARC1; p=reject; sp=quarantine; rua=mailto:dmarc@tcd.ie; pct=100"
```

**Policy values:**
- `p=none` — monitor only, take no action (used during rollout)
- `p=quarantine` — deliver to spam/junk folder
- `p=reject` — reject the message entirely

**DMARC alignment requirement:** Checks that the `From:` domain (what user sees) aligns with either:
- SPF: envelope sender domain matches `From:` domain (SPF alignment)
- DKIM: `d=` domain in DKIM-Signature matches `From:` domain (DKIM alignment)

This closes the gap where SPF/DKIM might pass for a relay domain but the `From:` header still shows a spoofed domain.

**Reporting:** `rua=` (aggregate reports) and `ruf=` (forensic reports) tell domain owners where their email is coming from — useful for discovering unauthorized senders.

## Deployment Flow

```
1. Publish SPF TXT record for your domain
2. Set up DKIM signing on outbound mail server; publish public key in DNS
3. Start with DMARC p=none (monitoring) → check rua reports
4. Identify legitimate mail streams (marketing, CRM, etc.)
5. Move to p=quarantine → p=reject once confident
```

## Interaction with DNSSEC

SPF + DKIM + DMARC records live in DNS as TXT records. If DNS is not DNSSEC-signed, an attacker who poisons the DNS cache can:
- Delete the SPF record → SPF returns `none` (no policy)
- Replace DKIM public key → DKIM verification fails or passes for attacker's key

**DNSSEC protects the integrity of these email authentication records.** DNSSEC + DMARC p=reject = strong email authentication stack.

## Attack Scenarios and Mitigations

| Attack | How it works | Mitigation |
|---|---|---|
| Email spoofing | Forge `From:` header | DMARC p=reject |
| SPF bypass via forwarding | Forwarder's IP not in SPF | DKIM alignment (survives forwarding) |
| DKIM replay | Resend valid signed email | Message-ID + timestamp checks |
| DNS cache poisoning of SPF/DKIM | Replace records with attacker's | DNSSEC |
| BEC via lookalike domain | `tcd-ie.com` instead of `tcd.ie` | Lookalike domain monitoring |

## Exam Pattern

Q3 system design often asks: "How would you secure email for your system?" Answer: SPF + DKIM + DMARC (with p=reject), DNSSEC on the DNS zone, TLS for SMTP transport (STARTTLS or SMTP over TLS). Mention reporting (`rua=`) for operational visibility.


## Relevant RFCs

- **RFC 7208** — *Sender Policy Framework (SPF)* — TXT record listing authorised sending IPs; `v=spf1 include:... -all`; checks envelope MAIL FROM not From: header
- **RFC 6376** — *DomainKeys Identified Mail (DKIM)* — sender signs selected headers + body with private key; public key in DNS; survives forwarding unlike SPF
- **RFC 7489** — *DMARC: Domain-based Message Authentication, Reporting and Conformance* — policy on SPF/DKIM failure (none/quarantine/reject); alignment between From: and SPF/DKIM domain
- **RFC 6698** — *DANE: DNS-based Authentication of Named Entities* — TLSA records to pin expected certificate for SMTP; requires DNSSEC; prevents rogue CA misissuance for mail servers
- **RFC 8461** — *SMTP MTA Strict Transport Security (MTA-STS)* — policy file enforcing TLS for SMTP; alternative to DANE that doesn't require DNSSEC

<!-- MODE:HINGLISH -->
# Email Security — Hinglish mein

## Problem kya hai?

Email 1970s mein banaya gaya tha — zero security. Koi bhi `From:` header mein kuch bhi likh sakta hai. "From: ceo@yourbank.com" — SMTP aankh moondh ke accept kar leta hai. Phishing aur spoofing isi wajah se itne common hain.

Teen DNS-based fixes hain: **SPF, DKIM, DMARC**.

## SPF — authorized senders ki list

**Sender Policy Framework (RFC 7208)**

Domain ke DNS mein ek TXT record publish karo: "Sirf yeh IP addresses/servers mere naam se email bhej sakte hain."

```
tcd.ie TXT "v=spf1 ip4:134.226.0.0/16 include:spf.protection.outlook.com -all"
```

Receiving server check karta hai: "Yeh email jo IP se aayi, kya woh tcd.ie ke SPF record mein listed hai?"

**`-all`** = hard fail (reject if not listed)
**`~all`** = soft fail (suspicious mark karo)

**SPF ki limitation:** Envelope sender (`MAIL FROM`) check karta hai, user ko dikhne wala `From:` header nahi. Email forwarding mein SPF break ho sakti hai — forwarding server ka IP original domain ke SPF mein nahi hota.

## DKIM — cryptographic signature

**DomainKeys Identified Mail (RFC 6376)**

Sender email par signature lagata hai (private key se). Public key DNS mein publish hoti hai.

```
selector1._domainkey.tcd.ie TXT "v=DKIM1; k=rsa; p=[public_key]"
```

Receiving server: DNS se public key fetch karo → email ka signature verify karo.

**DKIM ka advantage:** Email forward ho toh bhi signature remain karta hai (SPF ke unlike). `From:` header sign karta hai — jo user dekh raha hai woh verify hota hai.

**DKIM ki limitation:** Failure par kya karna chahiye yeh nahi batata. Replay attack possible — valid signed email ko attacker resend kar sakta hai.

## DMARC — policy layer

**Domain-based Message Authentication, Reporting & Conformance (RFC 7489)**

SPF aur DKIM ke upar ek policy: "Agar fail ho, toh kya karo?"

```
_dmarc.tcd.ie TXT "v=DMARC1; p=reject; rua=mailto:dmarc@tcd.ie"
```

**`p=none`** — sirf monitor karo (rollout phase mein use karo)
**`p=quarantine`** — spam folder mein bhejo
**`p=reject`** — reject kar do

**Alignment check:** DMARC check karta hai ki user-visible `From:` domain SPF ya DKIM domain se match karta hai. Sirf relay domain ke liye SPF pass karna enough nahi — `From:` header bhi match karna chahiye.

**Reporting:** `rua=` aggregate reports bhejta hai — domain owner ko pata chalta hai unki email kahaan kahaan se ja rahi hai. Unauthorized senders discover karo.

## Deployment order

1. SPF record publish karo
2. DKIM signing set up karo outbound mail par
3. DMARC `p=none` se shuru karo (monitoring)
4. Reports check karo — legitimate mail streams identify karo
5. `p=quarantine` → phir `p=reject`

## DNSSEC connection

SPF + DKIM + DMARC sab DNS TXT records hain. Agar DNS DNSSEC se protect nahi hai:
- Attacker SPF record delete kar sakta hai (no policy → attackers free)
- DKIM public key replace kar sakta hai

**DNSSEC in-band mein email authentication records bhi protect karta hai.**

Exam mein: "DNSSEC + DMARC p=reject = strong email authentication stack."

## Exam ke liye

Q3 mein "email secure karo" aa sakta hai. Answer: SPF + DKIM + DMARC (p=reject), DNSSEC on the zone, TLS for SMTP transport. Reporting mention karo (`rua=`) operational visibility ke liye.

Teen records, teen names, teen purposes yaad karo:
- SPF → authorized sender IPs list
- DKIM → cryptographic signature on message
- DMARC → policy on failure + reporting
