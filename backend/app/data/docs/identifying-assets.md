<!-- MODE:EASY -->
# Identifying Assets — Simple Version

Before you protect anything, you need to know *what* you're protecting.

Think of it like packing for a holiday. You don't just throw random stuff in a bag — you think about what matters: passport (most important!), laptop, clothes, money. If your passport gets stolen, the holiday is ruined. If you lose a sock, who cares?

**Assets** are the "important things" in a security system.

There are a few types:

🗂️ **Data** — customer names, passwords, medical records, credit cards. If this leaks, people get hurt.

⚙️ **Services** — the website, the app, the payment system. If it goes down, the business stops.

🏢 **Infrastructure** — servers, networks, cloud accounts. The physical/digital stuff everything runs on.

👤 **People** — employees with special access, customers whose data you hold.

⭐ **Reputation** — this one catches everyone out. Even if you fix a breach quickly, the news story kills your business. **Always include reputation.**

📜 **Legal compliance** — being GDPR-compliant is itself an asset. Losing it means fines.

**Exam trick:** The question says "identify assets including reputation" in every official answer since 2018. If you forget reputation, you lose marks. Every. Single. Time.

<!-- MODE:TECHNICAL -->
# Identifying Assets

## What Is an Asset?

Anything valuable that must be protected. Risk analysis starts here — you cannot classify risks until you know what you are protecting.

## Asset Categories

| Category | Examples |
|---|---|
| **Data** | Customer PII, financial records, source code, credentials, encryption keys |
| **Services** | APIs, web apps, databases, payment processing, uptime SLAs |
| **Infrastructure** | Servers, cloud accounts, CI/CD pipelines, network devices |
| **People** | Privileged employees, data subjects (GDPR), third-party contractors |
| **Reputation** | Brand trust, press coverage risk, customer churn after breach |
| **Legal/Compliance** | GDPR compliance status, contractual SLAs, regulatory licences |

## The Farrell Rule: Reputation Is Always an Asset

Every official solution since 2018 includes the phrase *"identify assets (including reputation)."* Omitting it costs marks.

**Why?** A technical breach fixed in hours can still destroy a company via reputational damage. Reputation is also the hardest asset to recover.

## How to Identify Assets in Any Scenario

1. What data does the system hold?
2. What services does it provide?
3. What legal obligations does it carry?
4. Who are the stakeholders (org, customers, regulators)?
5. What would cause headlines if it went wrong? → that is your reputation asset

## Worked Example: ISP LLM Chatbot (2025)

| Asset | Why it matters |
|---|---|
| Customer PII | GDPR obligations; leakage = fine + reputational damage |
| ISP corporate data (tariffs, plans) | Trade secrets; leakage to LLM provider = competitive harm |
| Chatbot availability | Customer support depends on it |
| Accuracy of responses | ISP liable for commitments chatbot makes |
| Reputation as trusted ISP | Breach erodes trust; customers switch |
| GDPR compliance status | Losing it means enforcement action |

## Common Exam Mistakes

- Only listing technical assets (servers, DBs) and ignoring intangibles
- **Not including reputation** — costs marks every time
- Confusing assets with risks ("data breach" is a risk; "customer data" is the asset)


## Relevant RFCs

- **RFC 3552** — *Guidelines for Writing RFC Security Considerations* — Section 3 defines asset categories: data confidentiality, data integrity, availability, accountability
- **RFC 7258** — *Pervasive Monitoring is an Attack* — frames metadata and traffic analysis as assets worth protecting, beyond just payload content
- **RFC 6973** — *Privacy Considerations for Internet Protocols* — Section 3 defines privacy-relevant assets: identity, location, associations, communication content

<!-- MODE:HINGLISH -->
# Assets Identify Karna — Hinglish mein

## Pehle samjho: Asset kya hota hai?

Asset = wo cheez jo protect karni hai. Jaise tum ghar mein lock kya lagate ho? Paise, jewellery, documents — wo sab assets hain.

Security mein bhi same logic. Pehle list banao kya protect karna hai, tabhi risks identify kar sakte ho.

## Asset types yaad karo

**Data assets:** Customer ke naam, addresses, credit card details, passwords, medical records. GDPR ke under yeh sabse important hain.

**Service assets:** Website, app, payment gateway — agar yeh down ho gaya toh business ruk jaata hai.

**Infrastructure:** Servers, cloud accounts, CI/CD pipelines. Physical aur digital dono.

**People:** Jo employees ke paas special access hai — woh bhi asset hain (aur risk bhi).

**Reputation:** ⚠️ **Yahi sabse zyada bhoolte hain log.** Ek chhoti si breach bhi agar news mein aa gayi toh company ka naam kharab ho jaata hai. Farrell ke har solution mein "including reputation" explicitly likha hota hai.

**Legal compliance:** GDPR-compliant rehna khud ek asset hai. Agar compliance jaati hai toh fine aata hai.

## Exam shortcut

Jab bhi scenario milta hai — ek simple question poochho apne aap se:

*"Agar yeh system hack ho jaaye, kya kya impact hoga?"*

Jo bhi impact hoga — woh asset hai jo compromise hua.

## Yaad rakhne wali cheez

Reputation bhoologe → marks katenge. Simple.

Aur assets aur risks ko confuse mat karo. "Data breach" — yeh risk hai. "Customer data" — yeh asset hai.
