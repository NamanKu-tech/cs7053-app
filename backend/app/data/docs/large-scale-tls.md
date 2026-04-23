<!-- MODE:EASY -->
# Large-Scale TLS — Simple Version

TLS works great for one connection. But what happens when you're running a service used by millions of people? New problems appear that don't exist at small scale.

**Problem 1: Certificate revocation**
Certificates expire, but what if a private key gets stolen *before* it expires? You need to tell browsers "this certificate is now cancelled." The old way (CRL — a big list) is too slow and too big. The newer way (OCSP) requires your browser to call a third-party server every time it visits a website. TLS 1.3 encourages *OCSP stapling* — the website itself includes the "still valid" proof in the handshake, so browsers don't need an extra round trip.

**Problem 2: Too many certificates to manage**
Before Let's Encrypt, getting a TLS certificate cost $100+ and took days. Most small websites skipped HTTPS. Let's Encrypt made it free and automatic — now you renew every 90 days automatically. ~300 million certificates issued. The web got encrypted.

**Problem 3: Corporate MITM boxes**
Big companies put boxes on their network that intercept all TLS traffic (for antivirus, compliance). These boxes replace the real certificate with a company-issued one. Security researchers found these boxes often use weaker crypto than the original, and they break forward secrecy. Your IT department can read all your HTTPS traffic.

**Problem 4: Non-browser apps**
Most phone apps and desktop software that use TLS don't validate certificates properly. Studies found many apps accept any certificate — making TLS useless against anyone with a fake cert.

<!-- MODE:TECHNICAL -->
# Large-Scale TLS Deployment Issues

## Certificate Ecosystem Problems

**CA Compromise (DigiNotar 2011):** DigiNotar CA was breached; attackers issued fraudulent certs for google.com and others. Browsers had to emergency-distrust the entire CA. ~500,000 Iranian users' traffic intercepted.

**CT Logs (Certificate Transparency, RFC 6962):** All publicly-trusted CAs must submit certs to append-only public logs before issuance. Allows detection of mis-issued certs. Chrome requires 2+ SCTs (Signed Certificate Timestamps) from distinct logs.

## Revocation: A Broken Problem

| Mechanism | Problem |
|---|---|
| CRL | Too large (MB range for major CAs); cached for days; not checked for end-entity certs |
| OCSP | Privacy leak (CA learns every site you visit); single point of failure; added latency |
| OCSP Stapling | Server fetches OCSP response and includes it in handshake — good, but optional |
| OCSP Must-Staple | Certificate extension requiring staple — server misconfiguration breaks the site |
| CRLite | Mozilla: bloom-filter encoding of full CRL database pushed to browser — promising |
| Short-lived certs | Let's Encrypt 6-day certs (2024) — revocation becomes unnecessary if TTL < incident response time |

## Let's Encrypt + ACME

Automated Certificate Management Environment (RFC 8555). Domain validation via DNS-01 or HTTP-01 challenge. 90-day cert lifecycle; auto-renewal via certbot/acme.sh. ~400M active certs as of 2024.

Effect: HTTPS adoption jumped from ~30% to ~90%+ of web traffic between 2014–2024.

## Corporate TLS Inspection (MITM Boxes)

Interception-NDSS17 study: 10–15% of TLS connections inspected. Boxes often:
- Downgrade cipher suites (use TLS 1.0, RC4)
- Remove forward secrecy (use RSA key transport instead of DHE)
- Don't validate upstream cert properly (Fahl et al.: non-browser SSL is broken)

Attack surface: if the box is compromised, attacker sees all corporate traffic in plaintext.

## Non-Browser TLS (Fahl et al., CCS 2012)

Android apps studied: 41% accept all certificates; 16% accept all hostnames. Most using HttpClient with disabled verification. Apps transmitting passwords in "HTTPS" that provides zero protection against MITM.

## Session Tickets at Scale

Server-side session tickets are encrypted with a ticket encryption key (TEK). At scale (millions of servers), TEK must be shared across fleet. If TEK is compromised, all sessions using resumption lose forward secrecy. Rotate TEKs every few hours.

<!-- MODE:HINGLISH -->
# Large-Scale TLS — Hinglish mein

## Problem: Ek certificate kaise revoke karein?

Socho server ka private key chori ho gayi. Certificate valid hai 1 saal ke liye. Abhi browser ko kaise bataaoge ki yeh certificate cancel kar do?

**CRL (Certificate Revocation List):** Ek badi list jo daily update hoti hai. Problem: list MB mein hoti hai. Har connection par download nahi kar sakte.

**OCSP:** Browser har website visit par CA server se poochhta hai "certificate valid hai?" Problem: privacy leak (CA ko pata chal jaata hai tum kahan ja rahe ho) + extra latency.

**OCSP Stapling (best option):** Website khud apna "main valid hoon" proof handshake mein attach karta hai. Browser ko alag request nahi bhejni. TLS 1.3 mein recommend kiya jaata hai.

**Short-lived certs (newest):** Let's Encrypt ke 6-day certs — itne jaldi expire hote hain ki revocation ki zaroorat hi nahi.

## Let's Encrypt ne kya badla

Pehle TLS certificate: $100+ aur kaafi din ka wait. Isliye chhoti websites HTTP use karti thi (insecure).

2014 mein Let's Encrypt aaya — free, automatic, 90-day rotation. Ab HTTPS worldwide ~90% web traffic par hai.

## Corporate MITM boxes — scary stuff

Bade companies apne network mein ek box lagate hain jo sari TLS traffic intercept karta hai "security ke liye." Browser ek fake company certificate accept karta hai. IT department tumhari sari HTTPS traffic padh sakti hai.

Problem: yeh boxes often weak crypto use karte hain (TLS 1.0, RC4) aur forward secrecy remove kar dete hain. Agar box hack ho jaaye — attacker ko sab plaintext milta hai.

## Exam ke liye

Q2 sub-part "large-scale deployment issues" poochhe toh: Certificate Transparency (CT logs), OCSP stapling vs short-lived certs, Let's Encrypt automation, corporate MITM box risks, session ticket key rotation.
