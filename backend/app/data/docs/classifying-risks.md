<!-- MODE:EASY -->
# Classifying Risks — Simple Version

Once you have your list of bad things that could happen, you need to sort them. Not all bad things are equally scary.

Imagine you run a lemonade stand:
- A **bee sting** is bad but unlikely and you'd recover fast → LOW impact, LOW likelihood
- **Running out of lemons** is pretty likely on a hot day and stops the whole business → HIGH likelihood, MEDIUM impact
- **The whole stand catching fire** is terrible but very unlikely → HIGH impact, LOW likelihood

You give every risk two scores:
- **How bad is it?** (Impact: High / Medium / Low)
- **How likely is it?** (Likelihood: High / Medium / Low)

Then you combine them using a simple grid:

| | Low Impact | Medium Impact | High Impact |
|---|---|---|---|
| **High Likelihood** | Medium priority | High priority | 🔴 TOP priority |
| **Medium Likelihood** | Low | Medium | High |
| **Low Likelihood** | Ignore | Low | Medium |

Top priority = fix it first. Ignore = don't waste time on it now.

**The key rule:** Always justify your scores. Just saying "HIGH" without a reason scores zero. Say *why* it's high.

<!-- MODE:TECHNICAL -->
# Classifying Risks: Impact × Likelihood

## The Two-Dimensional Model

Every risk gets two independent scores:

| Dimension | Question | Scale |
|---|---|---|
| **Impact** | How bad if this threat is realised? | High / Medium / Low |
| **Likelihood** | How probable is this threat in practice? | High / Medium / Low |

## 3×3 Priority Matrix

| | Low Impact | Medium Impact | High Impact |
|---|---|---|---|
| **High Likelihood** | Medium | High | **Top** |
| **Medium Likelihood** | Low | Medium | High |
| **Low Likelihood** | Ignore | Low | Medium |

## What Makes Impact HIGH?

- GDPR breach → regulatory fine (up to 4% of global turnover)
- Reputational damage → customer churn, press coverage
- Safety consequence → physical harm
- Critical national infrastructure outage

## What Makes Likelihood HIGH?

- Known CVEs in the software stack
- Commodity attacks (credential stuffing, SQLi) — automated, cheap
- Already-motivated attacker (political actor in election scenario)
- Very large attack surface / publicly exposed endpoints

## Exam Pattern: Q1(b) — 3 Risks

**Template per risk (~4–5 marks each):**

**Risk N: [Descriptive name]**
- **What:** One sentence describing the threat and the vulnerability it exploits
- **Impact:** HIGH/MEDIUM/LOW — justify in one sentence
- **Likelihood:** HIGH/MEDIUM/LOW — justify in one sentence
- **Countermeasure:** Specific, actionable mitigation

## Worked Example (2025 Q1b — ISP LLM chatbot)

**Risk 1: Customer PII leaking to LLM provider**
- Impact: HIGH — GDPR breach, regulatory fine, reputational damage
- Likelihood: HIGH — LLM APIs log prompts by default
- Countermeasure: Data minimisation (strip PII before API call); review provider DPA; consider self-hosted LLM

**Risk 2: LLM hallucinating incorrect responses**
- Impact: HIGH — financial liability if customer acts on wrong info
- Likelihood: MEDIUM — inherent LLM property, worse on edge cases
- Countermeasure: Human-in-the-loop for high-stakes; AI-generated disclosure; easy escalation path

**Risk 3: Prompt injection**
- Impact: HIGH — attacker extracts other customers' data, bypasses guardrails
- Likelihood: MEDIUM-HIGH — OWASP LLM Top-10, actively exploited
- Countermeasure: Input sanitisation; privilege separation (LLM cannot write to DB); red-team testing

## Farrell's Marking Traps

- Generic countermeasures ("use firewalls") = 0 marks
- Unlabelled impact/likelihood = partial marks
- Repeating Q1(a) content here = marks deducted
- Repeating risks between Q1(b) and Q1(c) = penalised in official solutions

<!-- MODE:HINGLISH -->
# Risks Classify Karna — Hinglish mein

## Do sawaal, har risk ke liye

Har ek risk ke liye sirf do cheezein poochhni hain:

1. **"Agar yeh ho gaya, kitna nuksan hoga?"** → Impact: High / Medium / Low
2. **"Yeh hone ki kitni zyada chance hai?"** → Likelihood: High / Medium / Low

Bas itna hi. Dono scores deke ek priority nikalo.

## Priority grid yaad karo

Sabse important case: **High Impact + High Likelihood = Top Priority** — pehle isko fix karo.

Sabse ignore karne wala: **Low Impact + Low Likelihood** — time waste mat karo isme.

## Justification dena zaroori hai

Sirf "HIGH" likhna kafi nahi. Examiner ko reason chahiye.

❌ Galat: "Impact: HIGH"

✅ Sahi: "Impact: HIGH — GDPR breach hone par company ko 4% global turnover ka fine lag sakta hai aur reputation damage hoga"

## Q1(b) ka format

Teen risks likhne hote hain. Har ek mein:
- Kya risk hai (ek line)
- Impact: HIGH/MEDIUM/LOW + reason
- Likelihood: HIGH/MEDIUM/LOW + reason  
- Countermeasure: specific solution (vague nahi — "security improve karo" = 0 marks)

## Common mistakes

"Firewalls use karo" — yeh 0 marks wala answer hai. Specific bolo: *"Input sanitisation karo, LLM ko database write access mat do, red-team testing karo."*

Q1(a) ki cheezein yahaan mat likhna — woh process tha, yeh risks hain. Dono alag questions hain.
