<!-- MODE:EASY -->
# DNS Architecture + Issues — Simple Version

DNS stands for Domain Name System. It's the internet's phone book.

When you type `www.google.com` into a browser, your computer doesn't know where Google's servers are. It only knows IP addresses (numbers like `142.250.80.36`). DNS translates names into numbers.

**How it works (simplified):**

1. You type `google.com`
2. Your computer asks its local DNS resolver (usually your router or ISP)
3. If the resolver doesn't know, it asks the root nameservers ("who handles .com?")
4. The root points to the .com nameservers ("ask these servers")
5. The .com nameservers say "google.com is handled by Google's nameservers"
6. Google's nameserver says "google.com → 142.250.80.36"
7. Your browser connects to that IP

**The three big problems with original DNS:**

**No integrity** — Anyone who can intercept DNS traffic can lie about what IP address a name points to. Send people to a fake bank website.

**No authentication** — There's no way to verify the answers came from the legitimate DNS server.

**No privacy** — Your DNS queries are sent in plaintext. Your ISP, your network provider, anyone on the path can see every website you look up.

DNSSEC fixes the first two but not the third. DoH/DoT fix the third.

<!-- MODE:TECHNICAL -->
# DNS Architecture + Issues

## DNS Resolution Flow

```
Stub resolver (your laptop)
  ↓  query: what is google.com?
Recursive resolver (ISP or 8.8.8.8)
  ↓  cache miss → iterative resolution
Root nameservers (13 clusters, anycast, .root-servers.net)
  ↓  "for .com, ask a.gtld-servers.net"
TLD nameservers (.com, .ie, .org)
  ↓  "for google.com, ask ns1.google.com"
Authoritative nameserver (ns1.google.com)
  ↓  "google.com A 142.250.80.36  TTL 300"
Recursive resolver caches response
  ↓  returns to stub resolver
```

## DNS Record Types

| Type | Purpose | Example |
|---|---|---|
| A | IPv4 address | google.com → 142.250.80.36 |
| AAAA | IPv6 address | google.com → 2a00:1450:4009:816::200e |
| MX | Mail server | google.com → aspmx.l.google.com |
| CNAME | Alias | www.google.com → google.com |
| TXT | Text records (SPF, DKIM, verification) | google.com → "v=spf1 ..." |
| NS | Nameserver delegation | google.com → ns1.google.com |
| HTTPS | HTTP endpoint + ALPN + ECH key config | Newer record type |

## Three Core Issues DNS Doesn't Address

**1. Cache poisoning / Spoofing (Kaminsky 2008)**
Attacker floods recursive resolver with forged responses before legitimate one arrives. Birthday attack on 16-bit transaction ID + source port randomisation. If forged response accepted, all users of that resolver directed to attacker's IP.

**2. Lack of origin authentication**
No mechanism in original DNS to verify response came from authoritative server. DNSSEC adds RRSIG (signed record sets) to address this.

**3. Query privacy**
All queries in plaintext over UDP port 53. ISP / network operator / on-path adversary sees every hostname queried. DNSSEC does NOT address this. Requires DoT/DoH/ODoH.

## Kaminsky Attack (2008)

Dan Kaminsky discovered that birthday-attack on 16-bit TXID (65,536 values) combined with query for random non-existent sub-domain makes poisoning viable in seconds on unpatched resolvers. Coordinated vendor disclosure and emergency patch. Required source-port randomisation + larger transaction ID space as mitigation. DNSSEC is the correct long-term fix.

## DNS Amplification DoS

DNS over UDP: small query → large response. Authoritative servers return large DNSSEC-signed responses (several KB). Attacker spoofs source IP (victim's IP) → amplifies traffic to victim. DNSSEC makes responses larger → worse amplification factor.

Mitigation: response rate limiting (RRL) on authoritative servers; BCP38 (ingress filtering to prevent source-IP spoofing).


## Relevant RFCs

- **RFC 1034** — *Domain Names: Concepts and Facilities* — the original 1987 DNS spec; defines the namespace hierarchy, zones, resolvers, and the iterative resolution algorithm
- **RFC 1035** — *Domain Names: Implementation and Specification* — companion to RFC 1034; wire format, resource record types (A, MX, NS, CNAME, PTR), UDP/TCP transport
- **RFC 2181** — *Clarifications to the DNS Specification* — fixes ambiguities in RFC 1034/1035; TTL semantics, CNAME restrictions, authoritative vs non-authoritative answers
- **RFC 2308** — *Negative Caching of DNS Queries* — how NXDOMAIN responses are cached; SOA minimum TTL as the negative cache TTL

<!-- MODE:HINGLISH -->
# DNS Basics — Hinglish mein

## DNS kya hai?

Internet ka phone book. Jab tum browser mein `google.com` type karte ho, computer ko actual IP address chahiye. DNS woh translation karta hai.

## Resolution flow (simple)

Tumhara laptop → Recursive resolver (ISP ya Google 8.8.8.8) → Root servers → .com TLD servers → Google ke nameservers → IP milta hai → Browser connect karta hai.

## Teen core problems

**1. Spoofing / Cache Poisoning:**
DNS mein koi signature nahi. Attacker fake DNS response bhej sakta hai — "google.com ka IP yeh hai (attacker ka server)." Recursive resolver maan leta hai. Kaminsky (2008) ne dikhaya ki 16-bit transaction ID birthday attack se seconds mein crack hota tha.

**2. No authentication:**
Koi prove nahi kar sakta ki answer legitimate DNS server se aaya. DNSSEC isko fix karta hai — signed records.

**3. No privacy:**
DNS queries plaintext hain, UDP port 53 par. ISP, network admin, Wi-Fi hotspot owner — sab dekh sakte hain tum kaun si websites visit kar rahe ho. DNSSEC yeh FIX NAHI KARTA.

Privacy ke liye: DoT (DNS over TLS), DoH (DNS over HTTPS), ODoH (Oblivious DoH).

## DNSSEC vs Privacy

**DNSSEC:** Integrity + authentication. "Yeh answer tamper nahi hua" prove karta hai.

**DNSSEC does NOT:** Query encrypt nahi karta. Observer dekh sakta hai tum kya query kar rahe ho.

Yeh distinction exam mein marks deta hai — "DNSSEC privacy nahi deta, DoH/DoT deta hai" explicitly likhna.

## DNS Amplification

Small query → large response (DNSSEC responses bigger hain). Attacker source IP spoof karta hai → victim par flood. RRL (Response Rate Limiting) fix karta hai. DNSSEC ne amplification worse banaya (bigger responses).
