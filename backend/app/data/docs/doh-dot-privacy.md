<!-- MODE:EASY -->
# DNS Privacy (DoH / DoT) — Simple Version

Remember how DNS is the internet's phone book? Every time you visit a website, your computer asks "what's the IP address for google.com?" — and that question travels in plain text across the internet. Anyone watching can see every site you visit.

**DoT (DNS over TLS)** wraps your DNS questions in an encrypted envelope. Same question, same answer — but nobody snooping on the network can read it. Like sending a letter in a sealed envelope instead of a postcard.

**DoH (DNS over HTTPS)** does the same thing but sends DNS inside regular HTTPS traffic. That means it looks exactly like normal web browsing — your ISP, employer, or school network can't easily block or filter it because it blends in with all other HTTPS traffic on port 443.

**Why does this matter?**

Without DNS privacy:
- Your ISP can see every website you visit (and sell that data)
- Your employer can monitor your browsing
- A coffee shop attacker can see what you're looking up in real time

With DoH/DoT: they see encrypted traffic, nothing useful.

**The catch:**

You're now trusting your DoH provider (Cloudflare, Google, etc.) instead of your ISP. They can see your queries. You've just moved who you trust, not eliminated trust entirely.

DNSSEC checks whether answers are correct. DoH/DoT checks whether the connection is private. They solve different problems and work together.

<!-- MODE:TECHNICAL -->
# DNS over HTTPS (DoH) and DNS over TLS (DoT)

## Why DNS Privacy Matters

Classic DNS: plaintext UDP port 53. Observable by: ISP, network admin, on-path adversary, exit node. DNSSEC provides integrity but NOT confidentiality — DNSSEC-signed queries are still visible.

**Threat model:**
- Passive surveillance (logging by ISP/network operator)
- Traffic analysis (query patterns reveal browsing behaviour)
- DNS-based content filtering / censorship evasion
- MITM rewriting (requires both integrity AND privacy)

## DoT (DNS over TLS) — RFC 7858

DNS over TLS port **853**. Standard TLS 1.3 handshake → DNS queries/responses inside encrypted channel.

```
Client → TCP:853 → TLS handshake → DNS query inside TLS → Response
```

**Properties:**
- Confidentiality: yes (TLS encryption)
- Integrity: yes (TLS MAC)
- Authentication: yes (TLS certificate validates resolver identity)
- Port: 853 (distinguishable from HTTPS — easy to block)
- Connection reuse: persistent TCP connection reduces latency overhead

**Deployment:** Cloudflare (1.1.1.1), Google (8.8.8.8), Quad9 (9.9.9.9) all support DoT.

## DoH (DNS over HTTPS) — RFC 8484

DNS queries inside HTTPS POST/GET requests. Port **443**.

```
POST https://cloudflare-dns.com/dns-query
Content-Type: application/dns-message

[binary DNS wire format]
```

**Properties:**
- Confidentiality: yes (TLS)
- Integrity: yes (TLS)
- Authentication: yes (TLS certificate)
- Port: 443 (indistinguishable from HTTPS — hard to block without DPI)
- Multiplexed over HTTP/2 → low overhead

**Censorship resistance:** Because DoH traffic looks identical to HTTPS, ISP/firewall can't block it without blocking all HTTPS → massive collateral damage. This is why authoritarian regimes hate DoH.

**Browser support:** Firefox, Chrome natively support DoH. Firefox enabled by default with Cloudflare as default DoH provider (controversial).

## DoT vs DoH Comparison

| Property | DoT (853) | DoH (443) |
|---|---|---|
| Port visibility | Visible (853 distinct) | Hidden (443 = HTTPS) |
| Firewall bypass | Easy to block | Hard to block |
| Network admin control | Retained | Lost |
| Standard DNS software | Easier integration | Requires HTTP stack |
| Browser integration | No (OS level) | Yes (built-in) |
| Latency | Lower (persistent TCP) | Slightly higher |

## ODoH (Oblivious DoH) — RFC 9230

DoH gives the resolver your IP + query. ODoH splits knowledge between two servers:
- **Proxy** knows your IP, not your query
- **Target resolver** knows your query, not your IP

```
Client → (encrypted query + IP) → Proxy → (encrypted query, no IP) → Target resolver
```

Neither server has full information. Even Cloudflare can't correlate your identity with your queries.

**Implementation:** Cloudflare operates both ODoH proxy and target. Apple uses ODoH for iCloud Private Relay DNS component.

## DNSSEC + DoH/DoT Relationship

| Problem | Solution |
|---|---|
| DNS answers tampered/forged | DNSSEC (integrity + authentication) |
| DNS queries visible on network | DoH/DoT (confidentiality) |
| Resolver compromise | DNSSEC (resolver can't forge signed answers) |
| Resolver learns your queries | ODoH (splits knowledge) |

These are orthogonal solutions. Best deployment: DoH/DoT + DNSSEC validation at the resolver.

## Deployment and Adoption

**Encrypted DNS adoption (2025):**
- ~50% of DNS traffic is now DoH/DoT (driven by browser defaults)
- Firefox: DoH default (Cloudflare) since 2019 in US, expanding globally
- Chrome: DoH upgrade if system resolver supports it (automatic upgrade)
- iOS/macOS: DoT/DoH via Network Extension; iCloud Private Relay uses ODoH
- Android: Private DNS = DoT since Android 9

**Operational tension:**
Enterprise networks use DNS for security monitoring (block malware C2 domains, filter content). DoH bypasses network-level DNS filtering → enterprise CISO problem. Split-horizon DNS also breaks. Solution: enterprise DoH resolvers (employees use corporate DoH endpoint instead of public one).


## Relevant RFCs

- **RFC 7858** — *DNS over TLS (DoT)* — port 853, TLS-encrypted DNS; authentication via PKIX or DANE; keeps DNS privacy from on-path observers
- **RFC 8484** — *DNS over HTTPS (DoH)* — DNS inside HTTPS POST/GET on port 443; indistinguishable from web traffic; breaks enterprise DNS filtering
- **RFC 9230** — *Oblivious DNS over HTTPS (ODoH)* — proxy between client and resolver; proxy sees IP not query, resolver sees query not IP; maximum unlinkability
- **RFC 8310** — *Usage Profiles for DNS over TLS / DTLS* — opportunistic vs strict authentication modes; how clients verify the resolver's identity

<!-- MODE:HINGLISH -->
# DoH / DoT — Hinglish mein

## Problem yaad karo pehle

Classic DNS: plaintext UDP port 53. ISP, network admin, Wi-Fi snoop — sab dekh sakte hain tum kaun si websites visit kar rahe ho. DNSSEC ne integrity fix ki — answers tamper-proof hue. Lekin DNSSEC ne PRIVACY fix nahi ki. Queries abhi bhi visible hain.

## DoT kya hai?

**DNS over TLS (RFC 7858):** DNS queries TLS ke andar wrap karo. Port 853 par connect karo. TLS handshake pehle, phir DNS queries encrypted tunnel mein.

Simple: postal envelope mein letter. Content hidden, but envelope itself visible — port 853 clearly DNS traffic hai, easily blocked.

## DoH kya hai?

**DNS over HTTPS (RFC 8484):** DNS queries HTTPS POST requests mein bhejo. Port 443 par.

Simple: HTTPS traffic mein DNS chhupa do. ISP dekh nahi sakta — sab HTTPS traffic same dikhta hai port 443 par.

**Key advantage over DoT:** Port 443 block karna = sab HTTPS block karna. ISP ya firewall easily nahi kar sakta. Censorship bypass ke liye effective.

**Browser support:** Firefox (default Cloudflare DoH), Chrome (automatic upgrade if resolver supports it). OS level se alag — browser khud karta hai.

## DoT vs DoH practically

**DoT:** Network admin still dekh sakta hai ki port 853 use ho raha hai = DNS traffic. Corporate networks mein DNS filtering maintain ho sakti hai. Lower latency (persistent connection).

**DoH:** Network admin ko pata nahi ki HTTPS mein DNS chhupa hai. Corporate DNS filtering bypass ho jaati hai. Isliye enterprise admins DoH se pareshaan hain.

## ODoH — bonus

**Oblivious DoH:** Privacy problem with DoH: Cloudflare still tumhara IP + query dono jaanta hai. ODoH: proxy ko IP pata, resolver ko query pata — dono ko poori info nahi milti. Apple Private Relay isme use karta hai.

## DNSSEC vs DoH/DoT — exam mein yeh likhna

**DNSSEC:** "Answer tamper nahi hua" prove karta hai. Privacy nahi deta.

**DoH/DoT:** Query encrypt karta hai. Answer ki authenticity prove nahi karta.

**Dono chahiye ideal deployment mein:** DoH/DoT for privacy + DNSSEC for integrity.

Yeh distinction marks deta hai — explicitly likhna ki yeh different problems solve karte hain.

## Deployment stats (2025)

~50% DNS traffic encrypted (DoH/DoT). Firefox ne 2019 mein US mein default DoH kiya. Chrome automatic upgrade karta hai. Android 9+ mein "Private DNS" = DoT. ISPs aur enterprises resistance karte hain — monitoring aur filtering lose ho jaati hai.
