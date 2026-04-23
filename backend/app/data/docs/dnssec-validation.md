<!-- MODE:EASY -->
# DNSSEC Validation — Simple Version

Validation is the process of checking whether DNS answers are genuine. Think of it as verifying a chain of signatures to make sure nothing was tampered with.

When your DNS resolver asks for `tcd.ie`'s IP address and gets a response, it needs to check: "Was this signed by tcd.ie's real DNS server? And can I trust tcd.ie's key? And how do I know I should trust whoever signed off on tcd.ie's key?"

It's like a chain of references:
- You want to hire someone. They give you a reference from their previous employer.
- You call the employer to check. The employer was referenced by a government registry.
- You check the registry. The registry is verified by the government itself.
- You trust the government. So you can trust the hire.

That chain works because each step checks the one below it. The root (IANA) is the government — the ultimate trusted authority. Your DNS software has the root's public key built in.

**What happens if validation fails?**

The resolver returns SERVFAIL — a server error. The user gets "website not found" even though the website exists. This is actually correct behaviour — it means something looked wrong.

**The practical problem:**

Most users' computers use a local resolver (ISP or router) that does the validation for them. The user doesn't get to see whether DNSSEC validated or not. This is called "trusting your resolver."

If you're on a cafe WiFi, your "resolver" might be a hostile box that intercepts your DNS and returns whatever it likes. For that case, you need DoH/DoT — which encrypts the DNS query to a resolver you've explicitly chosen and trust.

<!-- MODE:TECHNICAL -->
# DNSSEC Validation Flow + Trust Anchors

## Validation Process (recursive resolver)

```
1. Resolver receives answer for tcd.ie A record
2. Fetch tcd.ie DNSKEY records
3. Verify RRSIG on tcd.ie A record using tcd.ie ZSK from DNSKEY
4. Verify RRSIG on tcd.ie DNSKEY using tcd.ie KSK
5. Fetch DS record for tcd.ie from parent (.ie) zone
6. Check: SHA-256(tcd.ie KSK) == DS record value
7. Fetch .ie DNSKEY, verify with .ie KSK
8. Fetch DS record for .ie from root zone
9. Check: SHA-256(.ie KSK) == DS record value
10. Verify root DNSKEY RRSIG using root KSK (trust anchor)
11. Root KSK matches hard-coded trust anchor → chain validated ✓
```

## Trust Anchor

The root zone's KSK is embedded in resolver software (RFC 7958 format). Updated when root KSK rolls over.

Current root KSK: `19036` (retired 2018) and `20326` (current). Most resolvers have both during rollover window.

`dig +dnssec . DNSKEY` shows the root trust anchor.

## Validation Results

| Flag | Meaning |
|---|---|
| `ad` (Authenticated Data) | Resolver validated DNSSEC chain successfully |
| `SERVFAIL` | Validation failed — mismatch or missing signatures |
| `cd` (Checking Disabled) | Client told resolver to skip validation |

## Stub Resolver vs Recursive Resolver Validation

**Recursive resolver validates:** Most common. Client trusts its resolver (ISP's 8.8.8.8, Cloudflare 1.1.1.1). If resolver is compromised or misconfigured, client is vulnerable.

**Stub resolver validates:** Client runs its own validating resolver locally (e.g., Unbound). Receives `SERVFAIL` directly if DNSSEC fails. Maximum security, maximum complexity.

## Operational Challenges

**EDNS0 required:** DNSSEC responses are large. DNS over UDP has 512-byte limit. EDNS0 (Extension Mechanisms for DNS, RFC 6891) extends this. Some networks/firewalls block EDNS0 → TCP fallback → latency.

**Deployment statistics (2025):**
- ~6% of delegated zones are DNSSEC-signed
- ~50% of recursive resolvers validate DNSSEC (major resolvers: Cloudflare, Google, most ISPs)
- Stub resolvers: almost never validate directly

**Key management pain:** Zone operators need automation (BIND auto-sign, Knot DNS, OpenDNSSEC, PowerDNS) for reliable ZSK rotation. Manual rotation = operational errors = validation failure = outages.

## DNSSEC + DANE

DANE (DNS-based Authentication of Named Entities, RFC 6698) uses DNSSEC to publish TLS certificate fingerprints in DNS (TLSA records). Allows domain owners to pin their TLS cert via DNSSEC rather than relying on Web PKI CAs.

```
_443._tcp.tcd.ie. TLSA 3 1 1 [SHA-256 of cert public key]
```

DNSSEC must validate for DANE to be trustworthy.

<!-- MODE:HINGLISH -->
# DNSSEC Validation — Hinglish mein

## Validation kaise kaam karta hai?

Recursive resolver DNS answer milne ke baad verify karta hai. Process: chain follow karo root tak.

**Simple steps:**

1. tcd.ie ka A record mila + uska RRSIG
2. tcd.ie ki DNSKEY fetch karo, RRSIG verify karo
3. Parent (.ie) se DS record fetch karo — yeh tcd.ie ke KSK ka hash hai
4. Match karo: DS record == hash(tcd.ie KSK)? ✓
5. .ie ki DNSKEY fetch karo, verify karo
6. Root se .ie ka DS record fetch karo
7. Root KSK use karo verify karne ke liye
8. Root KSK resolver mein hard-coded hai — yahi trust anchor hai

## Validation results

**`ad` flag in response:** Successfully validated. DNSSEC chain intact.

**`SERVFAIL`:** Validation fail hua. Kuch mismatch mila ya signature missing. Client ko "not found" milega — yeh correct behaviour hai. Fake answer se better hai.

## Practical problem: trusting the resolver

Zyada tar log apna ISP ya router ka DNS use karte hain. Resolver validation karta hai, user khud nahi karta. Agar resolver compromised hai (cafe WiFi!) toh user ko pata nahi chalega.

Isliye DoH/DoT important hai — resolver par bhi trust establish karo.

## Deployment stats (approx 2025)

Sirf ~6% zones DNSSEC-signed hain. ~50% resolvers validate karte hain. Bahut slow adoption — zone operators ke liye management overhead hai (ZSK rotation automate karna padta hai).

## DANE — bonus mention karo

DNSSEC ke upar DANE lagao: TLS certificate ka fingerprint DNS mein TLSA record ke zariye publish karo. Web PKI CAs par depend karne ki zaroorat nahi. Agar DNSSEC validated hai, toh TLSA record trustworthy hai.

Q4 mein ek line mention karo DANE — extra marks mil sakte hain.
