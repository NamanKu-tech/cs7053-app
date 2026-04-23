<!-- MODE:EASY -->
# Security Processes + SDLC — Simple Version

SDLC stands for Software Development Lifecycle — it's just the steps you go through when building software: plan → design → build → test → release → maintain.

The problem is that most teams only think about security at the *end* — right before release. By then, fixing problems is expensive and the bad habits are already baked in.

**The better way: put security checks at every stage.**

Imagine you're building a house:
- **Planning stage:** Think about where robbers might get in before you draw the blueprints. Don't add locks as an afterthought.
- **Building stage:** While laying bricks, check that walls are solid — don't wait until the house is finished to discover a wall is hollow.
- **Before moving in:** Get a professional to try to break in (penetration test).
- **After moving in:** Check locks regularly; change them when someone moves out.

That's exactly how secure software development should work.

**Key security gates in order:**
1. **Threat modelling** at design — ask "how could an attacker abuse this?"
2. **SAST** (automated code scanning) — finds bugs before the code runs
3. **Dependency scanning** — checks if any libraries you're using have known vulnerabilities
4. **Pen test** — a real human tries to hack it before launch
5. **Ongoing monitoring** — watch for attacks after launch; re-assess regularly

**The Equifax lesson:** They had a known vulnerability (Apache Struts CVE) for 2 months before the breach. A dependency scan in their CI pipeline would have caught it instantly. Process failure, not technical failure.

<!-- MODE:TECHNICAL -->
# Security Processes + SDLC

## SDLC Security Gates (what Farrell wants you to name)

| Phase | Security Activity | What it catches |
|---|---|---|
| **Requirements** | Security requirements definition; threat model scope | Missing requirements; wrong trust boundaries |
| **Design** | Threat modelling (STRIDE / attack trees) | Design-level flaws before any code is written |
| **Development** | SAST (static analysis: Semgrep, SonarQube, CodeQL) | Injection, memory errors, hardcoded secrets |
| **Build / CI** | Dependency scanning (Dependabot, Renovate, pip-audit, npm audit); SBOM generation | Known CVEs in third-party libraries |
| **Test** | DAST (dynamic analysis: OWASP ZAP, Burp); security regression tests | Runtime vulns, auth bypass, XSS, CSRF |
| **Pre-release** | Penetration test (manual, external) | Logic flaws, chained vulnerabilities |
| **Post-release** | Security monitoring (SIEM, IDS); bug bounty; periodic re-assessment | Zero-days, novel attack paths, configuration drift |

## Re-assessment Cadence

- **Quarterly review** of risk register
- **Re-assess on major change** (new feature, new integration, new regulation)
- **Re-assess after incident** — a breach changes the threat model

## Threat Modelling: STRIDE

| Letter | Threat | Example |
|---|---|---|
| S | Spoofing | Attacker impersonates admin user |
| T | Tampering | Attacker modifies stored data |
| R | Repudiation | User denies placing an order |
| I | Information Disclosure | PII visible in error messages |
| D | Denial of Service | Flood of requests crashes API |
| E | Elevation of Privilege | Regular user accesses admin endpoint |

## Key Incidents as Process Failure Examples

**Equifax 2017** — Apache Struts CVE published March 2017; Equifax breached May 2017. Two months and no dependency scan in CI. 147 million records leaked. Process failure.

**XZ backdoor 2024** — Long-con supply chain. Malicious contributor over 2 years earned commit access; inserted backdoor in compression library used by OpenSSH. Caught by one engineer noticing SSH slowness. Illustrates why SBOM + signed releases + code review of dependency commits matters.

## What Farrell Wants in Q1(c) / Q3 Process Sub-parts

Describe: threat model at design → automated scanning in CI → pen test pre-launch → quarterly re-assessment + re-assess on change. Name at least one tool per phase. Reference a real incident to justify the process.

<!-- MODE:HINGLISH -->
# Security Processes + SDLC — Hinglish mein

## SDLC kya hota hai?

Software Development Lifecycle = software banane ke steps. Problem yeh hai ki zyada teams security ko last mein sochti hain — "pehle build karo, baad mein secure karenge." Yeh galat approach hai.

## Sahi approach: har step mein security

**Design phase mein:** Threat modelling karo. Poochho: "agar main attacker hota toh kaise attack karta?" STRIDE framework use karo — Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege.

**Development mein:** SAST tools chalao (Semgrep, SonarQube). Yeh automatically code mein bugs dhundh lete hain — injection vulnerabilities, hardcoded passwords, etc.

**CI/CD pipeline mein:** Dependency scanning — Dependabot ya pip-audit. Known CVEs automatically detect ho jaate hain.

**Release se pehle:** Penetration test — real human try kare hack karne ki.

**Release ke baad:** SIEM se monitoring, bug bounty program, quarterly risk register review.

## Equifax wala sabak

March 2017: Apache Struts mein CVE published hua.
May 2017: Equifax breach hua — 147 million records chori.

Sirf 2 mahine! Agar unke CI mein ek dependency scan hota toh pata chal jaata. Technical failure nahi thi — **process failure thi.**

## Exam ke liye

Q1(c) ya Q3 mein process poochha jaaye toh yeh bolo:

1. Design mein threat model
2. CI mein SAST + dependency scan (naam lo: Dependabot, pip-audit)
3. Release se pehle pen test
4. Quarterly re-assessment + major change par re-assess
5. Real incident mention karo (Equifax, XZ backdoor)
