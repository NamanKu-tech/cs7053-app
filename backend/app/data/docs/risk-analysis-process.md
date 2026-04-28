<!-- MODE:EASY -->
# Risk Analysis Process — Simple Version

Imagine you're babysitting and you need to make sure nothing bad happens.

**Step 1:** Figure out what you're protecting. The baby? The house? Grandma's vase? These are your *assets*.

**Step 2:** Think of everything that could go wrong. Baby falls. House catches fire. Dog eats the vase. These are your *risks*.

**Step 3:** For each bad thing, ask two questions: "How bad would it be?" and "How likely is it?" Give each a score: High, Medium, or Low.

**Step 4:** Sort your list — worst and most likely stuff goes to the top.

**Step 5:** Fix the top problem first. Maybe you put a gate at the stairs.

**Step 6:** Now re-check your list. Does the gate also fix anything else? Do this again.

**Step 7:** Keep going until you run out of time or money.

That's it. In an exam, the question always says "describe the PROCESS" — so they want you to describe these steps, not the actual risks. Don't describe the risks — that's a different question!

**The magic word: ITERATE.** You don't do it once. You loop.

<!-- MODE:TECHNICAL -->
# Risk Analysis Process

## The 7-Step Process (Q1a every year since 2014)

1. **Identify assets** — data, services, infrastructure, people, reputation, legal compliance
2. **Identify risks and vulnerabilities** — what can go wrong; which weakness it exploits
3. **Classify: impact × likelihood** — High/Medium/Low for each dimension independently
4. **Rank** — high-impact + high-likelihood first; assign a partial order
5. **Design mitigation for top risk** — specific, concrete countermeasure
6. **Re-run the analysis** — one mitigation may lower likelihood/impact of other risks, or introduce new ones
7. **Iterate until effort exhausted** — record all decisions throughout

## Official Examiner Quote (from solutions 2022–2025)

> "The student should describe a process of identifying assets and risks, classifying them in terms of impact and probability of occurrence, e.g. with High/Medium/Low scores for each, and assigning an overall (partial) order to the list. Normally, one then iterates, designing a mitigation for the most important item on the list, and then re-doing the analysis as necessary."

## Scenario-Specific Bonus (5 marks)

| Scenario | What to add |
|---|---|
| LLM/AI | Safety-checking processes not established; seek external LLM security expertise |
| BYOD | Interview end users to establish actual device/OS range before classifying |
| Healthcare | Interview clinical staff, not just IT; include regulatory assets |
| IoT | Include physical security and default-credential risks |
| Political | Seek external advice on disinformation/manipulation risks |

## Farrell Penalises

- Describing specific risks (that's Q1b) instead of the process
- No mention of iteration / re-running
- Generic answers with no scenario adaptation
- Forgetting reputation as an asset


## Relevant RFCs

- **RFC 3552** — *Guidelines for Writing RFC Security Considerations* — how to think about threats and mitigations systematically; the framework behind structured risk analysis
- **RFC 6973** — *Privacy Considerations for Internet Protocols* — defines the privacy threat taxonomy (surveillance, aggregation, correlation, secondary use, disclosure, exclusion) used directly in Q1c answers
- **RFC 7258** — *Pervasive Monitoring is an Attack* — Farrell co-authored; establishes that passive mass surveillance is a legitimate attack class to mitigate

<!-- MODE:HINGLISH -->
# Risk Analysis Process — Hinglish mein

Yeh Q1(a) ka backbone hai. Har saal aata hai, 2014 se 2025 tak — ek baar bhi miss nahi hua.

## Process kya hai?

Soch lo tum ek naya startup join kiye ho aur boss ne bola "ek risk analysis karo." Toh tum kya karoge?

**Pehla kaam:** Dhundo kya protect karna hai — data, servers, reputation, GDPR compliance. Inhe *assets* kehte hain. **Reputation ko bhoolna mat** — har official solution mein yeh specifically mention hota hai.

**Doosra kaam:** Socho kya galat ho sakta hai. Hacker data chura sakta hai? Server crash ho sakta hai? Yeh risks hain.

**Teesra kaam:** Har risk ke liye do questions poochho: *"Kitna bura hoga?"* aur *"Kitni baar hoga?"* — High/Medium/Low mein score karo.

**Chauthaa kaam:** List ko sort karo — sabse dangerous upar.

**Paanchwa kaam:** Sabse top wale risk ka solution nikalo. Specific solution, vague nahi — "firewalls lagao" nahi chalega.

**Chhathaa kaam:** Solution lagane ke baad **dobara poori list check karo.** Ek solution doosre risks ko bhi affect kar sakta hai.

**Saatwa kaam:** Tab tak karo jab tak time/paisa khatam na ho. Sab kuch record karo.

## Exam mein kya likhna hai?

**Yad rakho:** Q1(a) process ke baare mein poochha jaata hai, specific risks ke baare mein nahi. Agar tum risks likhne lage toh marks kaatenge. Process = yeh 7 steps + iteration ka concept.

**Magic word:** ITERATE — ek baar karke chhod mat do. Loop chalao.
