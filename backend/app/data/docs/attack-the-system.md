<!-- MODE:EASY -->
# Being the Attacker — Simple Version

Q3's final sub-part almost always says: "Now describe how you would attack the system you just designed."

This feels weird — you spent the whole answer building defences, and now you have to tear them down. But it's actually the most fun part, and Farrell rewards specific, honest answers.

**The key insight:** The attacker doesn't need to break your best defences. They look for the easiest path.

**Common attack paths to mention:**

🔑 **Phish an admin** — Send a fake email that looks like an internal IT request. Admin clicks link, enters credentials on a fake login page. Attacker now has admin access. Bypasses all your technical defences.

🔓 **Exploit a forgotten test endpoint** — Developers often leave debug pages, API endpoints, or admin interfaces enabled in production. Attacker scans for these. No authentication required.

👤 **Malicious insider** — An employee with legitimate access abuses it. A database admin exports all customer records to a personal drive. They have the access — no hacking needed.

⚡ **DoS the hot-path** — Find the most expensive operation in your system (maybe a complex database query or a file upload). Flood it. Even if you have rate limiting, they may find a parameter that bypasses it.

🧩 **Supply-chain** — Don't attack the target directly. Compromise a library or tool the target uses. The target then installs the attack themselves. (XZ backdoor, SolarWinds)

**Why Farrell wants this:**
Real security thinking means knowing how your defences fail, not just what they protect against. An answer that says "attackers would find it very hard" gets zero. An answer that describes a specific path gets marks.

<!-- MODE:TECHNICAL -->
# Being the Attacker (Q3c wildcard)

## What Farrell Is Testing

The wildcard sub-part tests whether you've actually thought about your design from an adversary's perspective, not just built a castle without thinking about siege warfare.

**High-mark answers:** Name specific attack paths that exploit the architecture you just described. Reference real techniques or incidents.

**Zero-mark answers:** "The system would be difficult to attack." "Attackers would need sophisticated tools." Generic responses.

## Attack Path Taxonomy

### 1. Social Engineering / Phishing
**Target:** Privileged users (admins, developers, auditors)
**Technique:** Spear-phishing email with credential-harvesting page; MFA bypass via real-time MITM proxy (Evilginx2); SIM swap for SMS MFA
**Mitigation missed:** Even FIDO2 resists phishing; SMS MFA doesn't
**Named example:** RSA SecurID breach 2011 — phishing → seed files stolen → hardware tokens compromised

### 2. Insider Threat
**Target:** Legitimate users with authorised access
**Technique:** Exfiltrate data over time using normal queries; use sysadmin access outside working hours; plant persistent access for post-employment
**Mitigation missed:** Anomaly detection in SIEM; user behaviour analytics; data-loss prevention on export
**Realistic scenario:** DBA queries customer records beyond normal pattern → SIEM alert → investigation

### 3. Exposed Debug/Test Endpoints
**Technique:** Scan for common paths (`/admin`, `/debug`, `/metrics`, `/.env`, `/_debug_toolbar`); spider for undocumented endpoints
**Discovery:** Shodan, Google dorks, GitHub code search for repo leaks
**Named example:** Many breaches via exposed `.env` files with DB credentials in S3 buckets

### 4. Supply Chain Compromise
**Target:** Build pipeline, dependencies, or infrastructure tooling
**Technique:** Compromise widely-used open-source library (typosquatting, maintainer account takeover, long-con like XZ); inject malicious package into CI
**Named examples:** SolarWinds (2020), XZ backdoor (2024), Codecov (2021), event-stream npm (2018)

### 5. Exploit Forgotten Services
**Technique:** Old API version still running; dev environment accessible; legacy admin interface; S3 bucket public by misconfiguration
**Tool:** Shodan, Censys, `nmap` for unexpected open ports
**Prevention:** Asset inventory; port scanning your own perimeter; decommission old endpoints

### 6. DoS the Bottleneck
**Technique:** Identify expensive operations (complex search queries, file parsing, crypto operations). Flood with requests that trigger maximum CPU/DB load. Even authenticated endpoints can be DoS'd if the rate limiting is per-IP only.
**Example:** HTTPS POST with large XML → parser bomb; complex LDAP query → AD DoS

### 7. Session Token Theft
**Technique:** XSS → steal session cookie. Man-in-the-browser via browser extension malware. Malicious redirect on shared WiFi. HTTP-only + Secure cookie flags mitigate most paths.

## Building a Q3(c) Answer

Structure: pick 3 attack paths, for each state:
1. What you target (which component, which user)
2. The specific technique
3. What access you gain
4. Which of your own defences it bypasses or exploits a gap in


## Relevant RFCs

- **RFC 3552** — *Guidelines for Writing RFC Security Considerations* — attacker model taxonomy: passive eavesdropper, active MITM, off-path attacker, compromised endpoint
- **RFC 7457** — *Summary of Known TLS/DTLS Attacks* — useful reference when constructing attacks against TLS-secured systems
- **RFC 6973** — *Privacy Threat Model* — attacker goals beyond confidentiality: re-identification, aggregation, correlation across sessions

<!-- MODE:HINGLISH -->
# Attacker Mindset — Hinglish mein

## Q3(c) ka pattern

Almost har Q3 mein ek sub-part hota hai: "Ab batao agar tum attacker hote toh is system ko kaise attack karte?"

Yeh thoda weird lagta hai — pehle system design kiya, ab khud attack karo. Lekin yahi marks deta hai.

**Sahi approach:** Honest raho. Apni hi design ki weaknesses dhundho. Generic nahi — specific attack path bolo.

## Top 5 attack paths

**1. Admin ko phish karo**
Technical defences bypass karne ki zaroorat hi nahi. Ek convincing email bhejo "IT security alert: please verify your account." Admin link click karta hai, creds enter karta hai fake page par. Game over.

Real mitigation: FIDO2 (phishing-resistant MFA). SMS OTP yahan kaam nahi karta.

**2. Insider threat**
Ek DBA ya admin ke paas already access hai. Office hours ke baad customer records export kar sakta hai. Koi "hacking" nahi — normal access ka abuse.

Detection: SIEM mein user behaviour analytics. Normal query patterns se deviation = alert.

**3. Debug endpoints scan karo**
Developers aksar `/admin`, `/.env`, `/debug` wali pages production mein chhod dete hain. Shodan aur nmap se dhundho. No auth required.

Equifax breach mein bhi ek expired certificate ki wajah se ek portal invisible tha monitors ke liye.

**4. Supply chain attack**
Target ko directly attack karna zarooori nahi. Unki koi library ya tool compromise karo. Target khud install kar lega. XZ backdoor (2024) — 2 saal ka patience, phir SSH compromise.

**5. DoS the expensive endpoint**
System mein sabse heavy operation dhundho — complex search, file upload, crypto. Isko flood karo. Rate limiting often sirf public unauthenticated endpoints par hota hai; authenticated bulk operations miss ho jaate hain.

## Exam ke liye

Q3(c) mein 3 attacks: ek social engineering (phishing), ek insider, ek technical (forgotten endpoint ya supply chain). Har ek mein specific technique bolo aur kaunsa defence miss kiya ya bypass hua.
