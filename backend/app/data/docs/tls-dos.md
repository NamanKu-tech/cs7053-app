<!-- MODE:EASY -->
# TLS DoS Vectors — Simple Version

DoS stands for Denial of Service — making a system so busy that real users can't use it.

TLS has a specific problem: the *server* does much more work than the *client* during a handshake. The client sends a small message; the server has to do expensive maths (cryptography) before responding.

This creates an asymmetry that attackers love:

Attacker sends 1,000 ClientHello messages (cheap — just a few bytes each). Server starts doing expensive DH computation for each one. Server gets overwhelmed. Real users can't connect.

**Mitigations:**

**HelloRetryRequest** — Server doesn't commit to doing expensive work until the client proves it can receive a response (proving it has a real IP address, not a spoofed one).

**Rate limiting** — Only allow X new TLS connections per IP per second.

**Session resumption** — Returning clients don't do the full handshake again. They use a ticket from the previous session. Much cheaper for the server.

**Over-provisioning + CDN** — Have enough capacity that a moderate flood doesn't matter. Put a CDN in front.

**Connection timeouts** — If a client starts a handshake and doesn't finish in 5 seconds, drop it.

The key insight: **the asymmetry is the attack surface.** Any mitigation that reduces the server's work-per-new-connection narrows that gap.

<!-- MODE:TECHNICAL -->
# TLS DoS Vectors + Mitigations

## The Asymmetry Problem

TLS handshake is computationally asymmetric:
- Client: sends a small ClientHello with a pre-computed ECDHE public key
- Server: must verify client's key_share, generate its own ECDHE key pair, sign the transcript, compute the handshake keys

An attacker with a botnet can flood servers with incomplete or repeated ClientHellos at minimal cost to itself.

## Attack Vectors

**Handshake flood:** Send thousands of ClientHello messages per second; never complete the handshake. Server allocates state + performs ECDHE for each.

**Large certificate chains:** Some TLS configurations include very long certificate chains. Server must send and client must verify multiple certs. DDoS amplification if server-initiated.

**0-RTT replay flood:** Record a valid 0-RTT first flight; replay it repeatedly. If server accepts early data without replay protection, each replay may trigger expensive processing.

**Renegotiation flood (TLS 1.2):** Client repeatedly requested renegotiation, forcing server to redo the handshake. TLS 1.3 removed renegotiation.

## Mitigations

| Mitigation | How it works |
|---|---|
| **HelloRetryRequest (TLS 1.3)** | Server sends HRR instead of ServerHello when it wants client to prove IP reachability. Cheap for server. Client must do another round trip before server commits resources. |
| **SYN cookies equivalent** | At TCP layer, validate TCP handshake before accepting TLS connection |
| **Rate limiting per IP** | Cap new TLS handshakes per source IP per second |
| **Session resumption (PSK)** | Returning clients skip full handshake; use pre-shared resumption ticket. Ticket decryption is AEAD — cheap. |
| **Connection timeout** | Drop half-open TLS connections after N seconds |
| **CDN / Anycast** | Distribute load globally; absorb volumetric floods at edge |
| **Certificate optimisation** | Use ECDSA certs (smaller than RSA); short chains; OCSP stapling reduces extra round trips |

## Large-Certificate-Chain DoS

RSA-4096 cert + 3-cert chain + OCSP response can be several KB per new connection. Under connection flood, bandwidth becomes the bottleneck before CPU.

Fix: ECDSA P-256 certificates (~3× smaller than RSA-2048); short chains (2 certs max); Let's Encrypt automation for cert rotation.

## 0-RTT Replay

Server mitigations: single-use tickets (mark ticket as used in shared cache); time-limited anti-replay window (bloom filter); only allow idempotent requests in early data (e.g., GET, not POST with side effects).

<!-- MODE:HINGLISH -->
# TLS DoS Attacks — Hinglish mein

## Problem kya hai?

TLS handshake mein server ka kaam client se zyada hota hai. Client ek chhoti si message bhejta hai. Server expensive cryptographic operations karta hai — ECDHE key generate karna, certificate sign karna, keys derive karna.

Yeh asymmetry = attack surface.

Attacker 10,000 ClientHello bhej sakta hai ek second mein (cheap). Server har ek ke liye expensive maths karta hai. Server crash.

## Top mitigations

**HelloRetryRequest:** Server pehle ek cheap HRR bhejta hai. Client ko prove karna hota hai ki woh real IP se hai. Tabhi server expensive kaam shuru karta hai. Rate limiting jaisa effect.

**Session Resumption:** Purane clients ko full handshake nahi karna padta. PSK ticket use karte hain. Server ke liye bahut cheaper.

**Rate limiting:** Ek IP se ek second mein max X connections. Flood automatically block.

**CDN / Anycast:** Traffic globally distribute karo. Ek server par sara load nahi.

**Connection timeout:** Agar client 5 seconds mein handshake complete nahi karta, drop karo. Half-open connections accumulate nahi hoti.

## 0-RTT replay

0-RTT mein first message replay ho sakta hai. Attacker recorded valid first flight dobara bhejta hai. Server ko dekh ke sab process karna padta hai.

Fix: single-use tickets, time-window anti-replay, sirf idempotent requests (GET, not POST) early data mein.

## Exam ke liye

Q2 sub-part "DoS mitigations" poochhe toh: HelloRetryRequest + session resumption + rate limiting + CDN. Asymmetry concept mention karo — client cheap, server expensive.
