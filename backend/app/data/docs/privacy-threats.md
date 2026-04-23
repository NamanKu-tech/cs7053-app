<!-- MODE:EASY -->
# Privacy Threats — Simple Version

Privacy is your right to control information about yourself. Privacy threats are ways that control gets taken away from you.

RFC 6973 is just a document that gives these threats official names. You don't need to memorise the RFC number — just know the threat types with one example each.

**Surveillance** — Someone is watching everything you do. Like if your boss read every email you send. Online: your ISP seeing every website you visit.

**Stored data compromise** — Your data was saved somewhere and got stolen. Like when a company gets hacked and your password leaks.

**Correlation** — Someone connects dots between different pieces of info to figure out something you didn't want them to know. Like: "This person buys pregnancy tests and baby clothes... they must be pregnant." Even if neither piece alone was secret.

**Identification** — Anonymous data gets linked back to you specifically. "We don't know who user #4729 is... oh wait, they live at this address and work here — it's definitely Sarah."

**Secondary use** — Your data was collected for one purpose but used for another. You signed up for a newsletter, but they sold your email to advertisers.

**Disclosure** — Private information gets revealed to people who shouldn't see it. Like a medical record being visible to your employer.

**Exclusion** — You're not told what data someone holds about you, or can't correct it. GDPR's Article 15 (right of access) and Article 17 (right to erasure) fight this.

**GDPR connection:** Most of these are addressed by data minimisation, purpose limitation, and the rights of data subjects.

<!-- MODE:TECHNICAL -->
# Privacy Threats (RFC 6973)

## The Seven Threat Categories

| Threat | Definition | Example |
|---|---|---|
| **Surveillance** | Monitoring communications/behaviour without consent | ISP logging DNS queries; employer monitoring employee traffic |
| **Stored data compromise** | Unauthorised access to stored personal data | Database breach exposing PII |
| **Correlation** | Linking multiple datasets to infer private information | Combining purchase history + location to infer health status |
| **Identification** | Linking anonymised data back to a specific individual | Re-identifying users from "anonymous" mobility datasets |
| **Secondary use** | Using data beyond its original collection purpose | Marketing use of data collected for service delivery |
| **Disclosure** | Revealing data to parties not authorised to receive it | Medical records accessed by employer |
| **Exclusion** | Preventing individuals from knowing/correcting data about them | No access to credit score; no right to erasure |

## GDPR Countermeasures per Threat

| RFC 6973 Threat | GDPR Mechanism |
|---|---|
| Surveillance | Data minimisation (Art. 5); DPIA for high-risk monitoring |
| Stored data compromise | Breach notification 72h (Art. 33); encryption at rest |
| Correlation | Purpose limitation (Art. 5); pseudonymisation |
| Identification | Anonymisation; k-anonymity for statistical releases |
| Secondary use | Purpose limitation; explicit consent for new use |
| Disclosure | Access controls; need-to-know; RBAC |
| Exclusion | Art. 15 right of access; Art. 17 right to erasure; Art. 16 rectification |

## Exam Application

These threats appear in Q1 scenarios as the *what* (what privacy harm could occur), while GDPR mechanisms are the *countermeasure*. In Q3, they structure your security requirements: "The system must prevent correlation attacks by pseudonymising user records before statistical export."

## Key GDPR Articles to Quote

- **Art. 5** — Data minimisation + purpose limitation
- **Art. 17** — Right to erasure ("right to be forgotten")
- **Art. 15** — Right of access
- **Art. 33** — 72-hour breach notification to supervisory authority
- **Art. 35** — DPIA required for high-risk processing
- **Art. 25** — Privacy by design and by default

<!-- MODE:HINGLISH -->
# Privacy Threats — Hinglish mein

## Privacy threats kya hote hain?

Simple: koi tumhare baare mein kuch jaanna chahta hai jo tum nahi chahte. RFC 6973 ne inhe proper names diye hain.

## 7 threats yaad karo — ek example ke saath

**Surveillance** — koi tumhe dekh raha hai. ISP jo har website ka record rakhta hai. Employer jo emails read karta hai.

**Stored data compromise** — tumhara data kahin save tha, kisi ne chura liya. Database breach.

**Correlation** — alag-alag harmless cheezein jodke kuch private pata karna. Pregnancy test + baby clothes purchase = pregnant? Dono cheezein alone innocent thi, lekin milake sensitive ho gayi.

**Identification** — "anonymous" data ko real person se joड़ना. Netflix ne kaha tha data anonymous hai, researchers ne user IDs nikaal liye sirf 2 ratings se.

**Secondary use** — data ek kaam ke liye liya, doosre mein use kiya. Newsletter ke liye email diya, advertisers ko bech diya.

**Disclosure** — galat logon ko data dikha diya. Medical record employer ne dekh liya.

**Exclusion** — tumhe pata hi nahi kya data collect hua, ya correct karne ka mauka nahi mila. GDPR ka Art. 15 (right of access) aur Art. 17 (right to erasure) yahi fix karta hai.

## Exam mein kaise use karein

Q1 mein privacy threat = risk. Uski countermeasure = GDPR mechanism.

Example: "Secondary use ka risk HIGH hai — user data ko insurance companies ko bech diya ja sakta hai. Countermeasure: purpose limitation (Art. 5) — data sirf original purpose ke liye use hoga, explicit consent ke bina nahi."
