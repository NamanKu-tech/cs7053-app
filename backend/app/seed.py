import os
from app.database import SessionLocal
from app.models import Path, Topic, Note, Question, ExamQuestion, TopicMaterial
from app.exam_parser import parse_all as _parse_exam_questions

PATHS = [
    {
        "slug": "q1-risk-analysis",
        "title": "Q1 — Risk Analysis",
        "description": "Risk analysis process, assets, threats, mitigations. Appears as Q1 every year 2014–2025.",
        "exam_slot": "Q1",
        "overview": """# How to Answer Q1 — Risk Analysis

## The Pattern (Every Year)

Q1 is the most predictable question in the paper. The scenario changes (chatbot, mobile app, website) but the answer structure is identical every year.

**Q1a (15 marks): Describe the risk analysis process.**
**Q1b (15 marks): Describe 3 specific risks with impact, likelihood, and countermeasures.**
**Q1c (10 marks): Privacy threats / SDLC / GDPR — varies by year.**

---

## Q1a Template — The Process

Always cover these steps in order:

1. **Identify assets** — not just data, include reputation, availability, staff trust. Farrell always rewards "reputation" as an asset.
2. **Identify risks and vulnerabilities** — interview domain experts, not just IT staff. For medical systems: interview doctors. For statistical systems: interview statisticians.
3. **Classify each risk** — Impact (High/Medium/Low) × Likelihood (High/Medium/Low) → overall risk score/priority.
4. **Prioritise** — rank risks by score. Highest risk gets mitigated first.
5. **Design mitigations** — one at a time, then re-run the analysis because one mitigation changes the probability of others.
6. **Iterate** — repeat until effort budget is exhausted.
7. **Record everything** — document all decisions, even ones you decide not to mitigate.

**Key Farrell lines:**
- "Seek outside expertise where internal knowledge is insufficient" — always mention this.
- "Reputation is an asset" — always mention this.
- "Re-run the analysis after each mitigation" — this is what makes it iterative, say it explicitly.

---

## Q1b Template — Three Risks

For each risk, structure it as:

> **Risk name:** [what could go wrong]
> **Impact:** HIGH/MEDIUM/LOW — [why]
> **Likelihood:** HIGH/MEDIUM/LOW — [why]
> **Countermeasure:** [specific technical or process control]

Pick risks that span categories: one technical (e.g. data breach), one process (e.g. insider threat), one external (e.g. DoS or supply chain). Avoid listing three very similar risks.

---

## Q1c — Privacy / GDPR / SDLC

If asked about privacy threats (RFC 6973): surveillance, stored data exposure, aggregation, correlation, secondary use, exclusion, identification.

If asked about SDLC: security requirements at design → threat modelling → code review → pen test → incident response plan.

If asked about GDPR: data minimisation, purpose limitation, consent, right to erasure, DPA notification within 72 hours.

---

## Marks Traps

- Do NOT just list risks without process for Q1a — that gets zero.
- Do NOT give vague countermeasures ("use encryption") — be specific ("AES-256-GCM for data at rest, TLS 1.3 for data in transit").
- Do NOT forget to say the analysis is iterative and you re-run after each mitigation.
""",
        "topics": [
            {"slug": "risk-analysis-process", "title": "Risk Analysis Process", "order": 1, "depends_on": []},
            {"slug": "identifying-assets", "title": "Identifying Assets", "order": 2, "depends_on": ["risk-analysis-process"]},
            {"slug": "classifying-risks", "title": "Classifying Risks: Impact × Likelihood", "order": 3, "depends_on": ["identifying-assets"]},
            {"slug": "mitigations", "title": "Designing Mitigations", "order": 4, "depends_on": ["classifying-risks"]},
            {"slug": "privacy-threats", "title": "Privacy Threats (RFC 6973)", "order": 5, "depends_on": ["risk-analysis-process"]},
            {"slug": "security-processes", "title": "Security Processes + SDLC", "order": 6, "depends_on": ["mitigations"]},
            {"slug": "real-incidents", "title": "Real Incidents (Equifax, Stuxnet, Mirai)", "order": 7, "depends_on": ["security-processes"]},
        ],
        "exam_questions": [
            {
                "year": 2025, "exam_slot": "Q1a", "marks": 15,
                "question_text": "An Irish ISP is planning to deploy an upgraded customer support chatbot using a new LLM. Chatbot training uses ISP staff and contractors. The LLM provider's online API is required. Describe the process you would use to carry out a risk analysis for this system.",
                "sample_answer": "Identify assets (customer data, staff data, ISP reputation, service availability). Identify risks and vulnerabilities — interview staff, contractors, legal team, and seek external LLM security expertise. Classify each risk by impact and likelihood (High/Medium/Low). Assign overall priority. Design a mitigation for the highest-ranked risk, then re-run the analysis since one mitigation may affect the probability of other risks. Iterate until effort is exhausted. Record all decisions. For LLM systems, note safety-checking processes are not yet well-established; seek outside expertise.",
            },
            {
                "year": 2025, "exam_slot": "Q1b", "marks": 15,
                "question_text": "Describe three significant risks affecting the ISP LLM chatbot system, including their potential impact and likelihood, and outline countermeasures.",
                "sample_answer": "1. Customer PII leaking to LLM provider via prompts (Impact: HIGH — GDPR breach, fines; Likelihood: HIGH — inevitable with naive deployment). Countermeasure: data minimisation, anonymise inputs, review provider DPA. 2. LLM hallucinating incorrect advice (Impact: HIGH — liability, customer harm; Likelihood: MEDIUM). Countermeasure: human-in-the-loop review for sensitive queries, AI disclosure notices. 3. Prompt injection attacks (Impact: HIGH — data exfiltration, reputational damage; Likelihood: MEDIUM). Countermeasure: input sanitisation, privilege separation, regular red-team testing.",
            },
            {
                "year": 2024, "exam_slot": "Q1a", "marks": 15,
                "question_text": "A commercial Irish news organisation is planning a new election news website with a new CMS, user comments with moderation, and a paid subscription paywall. You are the employee tasked with carrying out a risk analysis. Describe the process you would use.",
                "sample_answer": "Identify assets (subscriber data, editorial reputation, ad revenue, availability during election). Identify risks — interview editorial staff (not just IT) for political manipulation risks. Classify by impact and likelihood. Prioritise. Design mitigations iteratively, re-running the analysis after each. Seek external expertise on political interference and election law. Record all decisions. Terminate when effort budget is exhausted.",
            },
            {
                "year": 2024, "exam_slot": "Q1b", "marks": 15,
                "question_text": "Describe three significant risks for the news organisation's election website, with impact, likelihood, and countermeasures.",
                "sample_answer": "1. Comment section weaponised for disinformation (Impact: HIGH — reputational, legal; Likelihood: HIGH). Countermeasure: pre-moderation during election, rate limiting, IP reputation checks. 2. CMS credentials stolen via phishing (Impact: HIGH — editorial control lost; Likelihood: MEDIUM). Countermeasure: FIDO2 MFA for all editorial staff, privileged access workstations. 3. Paywall bypass exposing subscriber data (Impact: MEDIUM — revenue loss, GDPR; Likelihood: MEDIUM). Countermeasure: server-side paywall enforcement, regular penetration testing.",
            },
            {
                "year": 2023, "exam_slot": "Q1a", "marks": 15,
                "question_text": "The CSO are considering replacing paper-based CPI price collection with a mobile phone app on collectors' own devices (BYOD). Describe the process you would use to carry out a risk analysis.",
                "sample_answer": "Identify assets (CPI data integrity, CSO reputation, collector privacy). Identify risks — interview CSO statistical staff (not just IT) to find statistical integrity risks unique to CPI. Classify by impact and likelihood. Rank. Design mitigations iteratively. For BYOD, survey the range of existing collector devices and OS versions. Seek external expertise for BYOD MDM policy. Record all decisions. Iterate until effort exhausted.",
            },
            {
                "year": 2023, "exam_slot": "Q1b", "marks": 15,
                "question_text": "Describe three significant risks for the CSO BYOD CPI app, with impact, likelihood, and countermeasures.",
                "sample_answer": "1. Collector's device compromised, CPI data exfiltrated or altered (Impact: HIGH — data integrity, public trust; Likelihood: MEDIUM). Countermeasure: app-level encryption, certificate pinning, MDM remote wipe. 2. Lost/stolen device exposes price data (Impact: MEDIUM — commercially sensitive; Likelihood: HIGH — collectors work in public). Countermeasure: device encryption enforced, remote wipe capability, data minimisation on device. 3. Insider threat — collector manipulates submitted prices (Impact: HIGH — CPI integrity; Likelihood: LOW). Countermeasure: digital signatures on each submission, anomaly detection on submitted data.",
            },
            {
                "year": 2022, "exam_slot": "Q1a", "marks": 15,
                "question_text": "The HSE is deploying a national COVID contact tracing app that records close contacts via Bluetooth and notifies users of exposure. Carry out a risk analysis process description for this system.",
                "sample_answer": "Identify assets (user location privacy, notification integrity, HSE reputation, app availability). Identify risks — interview public health experts as well as IT. Classify by impact and likelihood. Note that privacy perception risks require external public policy expertise beyond IT. Design mitigations iteratively, re-running after each step. Use decentralised architecture (DP-3T) to reduce server-side privacy risks. Record all decisions. Terminate when effort budget exhausted.",
            },
            {
                "year": 2022, "exam_slot": "Q1b", "marks": 15,
                "question_text": "Describe three significant risks for the HSE contact tracing app, with impact, likelihood, and countermeasures.",
                "sample_answer": "1. False positive notifications causing unnecessary quarantine (Impact: HIGH — public trust, economic harm; Likelihood: MEDIUM — Bluetooth range imprecision). Countermeasure: calibrate distance thresholds, allow user appeal. 2. App used to track individuals (Impact: HIGH — GDPR, public trust; Likelihood: MEDIUM). Countermeasure: decentralised design, no central location storage, privacy impact assessment. 3. Bluetooth replay attack inflating exposure reports (Impact: HIGH — system credibility; Likelihood: LOW). Countermeasure: rolling proximity identifiers, timestamp validation.",
            },
            {
                "year": 2021, "exam_slot": "Q1a", "marks": 15,
                "question_text": "A hospital network is deploying remote patient monitoring devices that send vital signs to a central dashboard viewable by on-call staff. Describe the risk analysis process you would apply.",
                "sample_answer": "Identify assets (patient safety, clinical data, availability of monitoring, hospital reputation). Identify risks — interview clinical staff, not just IT, to discover patient safety risks. Classify by impact and likelihood; availability has HIGH impact (patient safety implications). Design mitigations iteratively. Availability and integrity take priority over confidentiality for patient monitoring. Seek external expertise for medical device security standards (IEC 62443). Record all decisions.",
            },
            {
                "year": 2021, "exam_slot": "Q1b", "marks": 15,
                "question_text": "Describe three significant risks for the remote patient monitoring system, with impact, likelihood, and countermeasures.",
                "sample_answer": "1. Device firmware hijacked, vital signs falsified (Impact: HIGH — patient safety; Likelihood: LOW). Countermeasure: signed firmware updates, attestation on boot, network segmentation. 2. Monitoring dashboard unavailable during incident (Impact: HIGH — patient safety; Likelihood: MEDIUM). Countermeasure: redundant infrastructure, offline fallback display at bedside. 3. Patient data exfiltrated via compromised device (Impact: HIGH — GDPR, clinical confidentiality; Likelihood: MEDIUM). Countermeasure: TLS 1.3 with mutual authentication, data minimisation on device.",
            },
            {
                "year": 2020, "exam_slot": "Q1a", "marks": 15,
                "question_text": "The Department of Housing is planning an online rental deposit protection scheme, where tenants and landlords register deposits. Personal and financial data is held. Describe the risk analysis process.",
                "sample_answer": "Identify assets (deposit funds, personal data of tenants/landlords, scheme reputation, availability during peak periods). Identify risks — interview housing law experts and financial regulators as well as IT. Classify by impact and likelihood. Financial and GDPR risks dominate. Design mitigations iteratively. Seek external expertise on financial fraud patterns. Record all decisions. Terminate when effort exhausted.",
            },
            {
                "year": 2020, "exam_slot": "Q1b", "marks": 15,
                "question_text": "Describe three significant risks for the rental deposit scheme, with impact, likelihood, and countermeasures.",
                "sample_answer": "1. Fraudulent deposit claims (Impact: HIGH — financial loss, legal; Likelihood: HIGH — valuable target). Countermeasure: strong identity verification (passport + liveness), transaction audit trail. 2. GDPR breach of tenant/landlord personal data (Impact: HIGH — regulatory, reputational; Likelihood: MEDIUM). Countermeasure: data minimisation, encryption at rest, regular penetration testing. 3. System unavailable at end-of-tenancy peak (Impact: HIGH — financial deadlines, legal disputes; Likelihood: MEDIUM). Countermeasure: autoscaling, load testing, SLA with cloud provider.",
            },
            {
                "year": 2019, "exam_slot": "Q1a", "marks": 15,
                "question_text": "An Irish university is migrating all student records, email, and learning management systems to a US-based cloud provider. Describe the risk analysis process.",
                "sample_answer": "Identify assets (student data, academic records, email, LMS availability, university reputation). Identify risks — interview academic and administrative staff, not just IT. Classify by impact and likelihood. Data sovereignty (GDPR, US CLOUD Act) requires legal expertise beyond IT. Design mitigations iteratively. Seek outside legal expertise on data transfer mechanisms (SCCs, adequacy decisions). Record all decisions.",
            },
            {
                "year": 2019, "exam_slot": "Q1b", "marks": 15,
                "question_text": "Describe three significant risks for the university cloud migration, with impact, likelihood, and countermeasures.",
                "sample_answer": "1. US authorities accessing EU student data under CLOUD Act (Impact: HIGH — GDPR breach, legal; Likelihood: MEDIUM). Countermeasure: SCCs with provider, data residency in EU region, legal review. 2. Single cloud provider outage disrupts exams (Impact: HIGH — academic harm; Likelihood: LOW). Countermeasure: multi-cloud or hybrid for exam-critical systems. 3. Mass credential compromise via phishing targeting student accounts (Impact: HIGH — data breach; Likelihood: HIGH). Countermeasure: enforce MFA on all accounts, security awareness training.",
            },
            {
                "year": 2018, "exam_slot": "Q1a", "marks": 15,
                "question_text": "The Department of Social Protection is planning a national biometric identity card system storing fingerprint and facial data. Describe the risk analysis process.",
                "sample_answer": "Identify assets (biometric data, national identity infrastructure, citizen trust, availability). Biometric data is irreplaceable — compromise is permanent. Identify risks — interview civil liberties experts and legal counsel as well as IT. Classify by impact (biometric breach = HIGH permanently). Design mitigations iteratively, noting biometric data requires higher protection than passwords. Seek outside expertise on biometric standards (ISO/IEC 19795). Record all decisions.",
            },
            {
                "year": 2018, "exam_slot": "Q1b", "marks": 15,
                "question_text": "Describe three significant risks for the national biometric ID system, with impact, likelihood, and countermeasures.",
                "sample_answer": "1. Central biometric database breached — fingerprints stolen (Impact: CRITICAL — permanent, irreplaceable; Likelihood: MEDIUM). Countermeasure: store only derived templates not raw biometrics, split storage across HSMs, air-gap central store. 2. Fake biometric enrolment (Impact: HIGH — identity fraud; Likelihood: MEDIUM). Countermeasure: supervised in-person enrolment, liveness detection, document verification. 3. System used for mass surveillance beyond stated purpose (Impact: HIGH — civil liberties, GDPR; Likelihood: LOW-MEDIUM). Countermeasure: purpose limitation in law, independent oversight body, audit log of all queries.",
            },
            {
                "year": 2017, "exam_slot": "Q1a", "marks": 15,
                "question_text": "ESB is planning to roll out 2 million smart electricity meters with two-way communication for remote readings and demand management. Describe the risk analysis process.",
                "sample_answer": "Identify assets (electricity supply integrity, usage data privacy, meter firmware, ESB reputation). Identify risks — interview smart grid engineers and privacy experts as well as IT security staff. Classify by impact; electricity supply disruption has HIGH safety and economic impact. Design mitigations iteratively. Usage data is sensitive (reveals occupancy patterns) — seek external privacy expertise. Seek outside expertise on ICS/SCADA security. Record all decisions.",
            },
            {
                "year": 2017, "exam_slot": "Q1b", "marks": 15,
                "question_text": "Describe three significant risks for the ESB smart meter rollout, with impact, likelihood, and countermeasures.",
                "sample_answer": "1. Malicious firmware update disables meters at scale (Impact: HIGH — power disruption, safety; Likelihood: LOW). Countermeasure: signed firmware, staged rollout, cryptographic attestation, kill-switch requires multi-party authorisation. 2. Usage data reveals occupancy enabling burglary (Impact: HIGH — physical safety, privacy; Likelihood: MEDIUM). Countermeasure: aggregate data, limit access to raw readings, GDPR compliance. 3. Command injection via communications protocol manipulates tariffs (Impact: HIGH — financial; Likelihood: MEDIUM). Countermeasure: mutual TLS authentication, message signing, rate limiting on commands.",
            },
            {
                "year": 2016, "exam_slot": "Q1a", "marks": 15,
                "question_text": "A major Irish bank is launching a mobile banking app for iOS and Android supporting payments up to €10,000. Describe the risk analysis process.",
                "sample_answer": "Identify assets (customer funds, transaction data, bank reputation, app availability). Identify risks — interview fraud investigators and compliance as well as IT. Classify by impact and likelihood; financial fraud risks are HIGH impact. Design mitigations iteratively; re-run after each mitigation. Seek outside expertise on mobile banking fraud patterns and PSD2/EBA guidelines. Record all decisions.",
            },
            {
                "year": 2016, "exam_slot": "Q1b", "marks": 15,
                "question_text": "Describe three significant risks for the bank mobile app, with impact, likelihood, and countermeasures.",
                "sample_answer": "1. Malware on customer device intercepts credentials (Impact: HIGH — fraud, liability; Likelihood: HIGH). Countermeasure: FIDO2/biometric auth, anomaly detection on transactions. 2. App reverse-engineered, backend API abused (Impact: HIGH — fraud; Likelihood: MEDIUM). Countermeasure: certificate pinning, server-side authorisation, API rate limiting. 3. SIM swap attack bypasses SMS OTP (Impact: HIGH — account takeover; Likelihood: MEDIUM). Countermeasure: migrate from SMS OTP to FIDO2 hardware tokens or app-based TOTP.",
            },
            {
                "year": 2025, "exam_slot": "Q1c", "marks": 10,
                "question_text": "Describe the privacy threats relevant to the ISP LLM chatbot system, using the RFC 6973 privacy threat taxonomy.",
                "sample_answer": "RFC 6973 threats applicable to the LLM chatbot: (1) Surveillance — ISP staff monitoring chatbot conversations reveals customer behaviour and intent. (2) Stored data exposure — training data and conversation logs stored long-term; breach exposes sensitive personal and financial information. (3) Secondary use — conversation data used to train future LLMs beyond the original support purpose without user consent. (4) Aggregation — combining individual support queries builds detailed customer profiles. (5) Identification — seemingly anonymous queries can be re-identified via account context provided by the ISP. (6) Exclusion — users may not know their conversations are being logged or used for training. Mitigations: data minimisation, explicit consent for training use, retention limits, privacy notice update.",
            },
            {
                "year": 2024, "exam_slot": "Q1c", "marks": 10,
                "question_text": "Describe how security should be integrated into the software development lifecycle (SDLC) for the news organisation's election website.",
                "sample_answer": "Security must be integrated at every SDLC phase, not added at the end. Requirements phase: define security requirements (CIA+, GDPR, election-integrity requirements). Design phase: threat modelling (STRIDE) — identify attack surfaces (comment system, CMS, paywall). Development: secure coding standards, dependency scanning (SCA), pre-commit hooks for secret detection. Testing: SAST (static analysis), DAST (dynamic scanning against staging), penetration test before launch. Deployment: infrastructure-as-code security checks, secrets management (no credentials in repo), WAF configuration. Operations: security monitoring and alerting (SIEM), incident response plan, vulnerability disclosure policy. Maintenance: patch management process, regular re-pen-test. Key principle: security issues are cheapest to fix at design phase — exponentially more expensive post-deployment.",
            },
            {
                "year": 2023, "exam_slot": "Q1c", "marks": 10,
                "question_text": "Describe the GDPR obligations relevant to the CSO BYOD CPI mobile app, and how they should be addressed.",
                "sample_answer": "GDPR obligations: (1) Lawful basis — CSO must establish lawful basis for processing collector location/device data (likely public task, Art. 6(1)(e)). (2) Data minimisation — only collect data necessary for CPI collection; do not access other device data. (3) Purpose limitation — data collected for CPI cannot be repurposed. (4) Retention limits — delete collector data after retention period; define explicitly. (5) Security — appropriate technical measures (encryption, access controls) for data on personal devices. (6) Data subjects rights — collectors can request access to their data; right to erasure after employment. (7) DPIA — BYOD involving personal devices processing official data likely triggers Data Protection Impact Assessment. (8) DPA notification — if data breach occurs, notify DPC within 72 hours. Address by: DPIA before deployment, updated employment contracts, privacy notice, MDM policy, data retention schedule.",
            },
            {
                "year": 2022, "exam_slot": "Q1c", "marks": 10,
                "question_text": "Describe the privacy threats specific to a contact tracing app and how a privacy-by-design approach addresses them.",
                "sample_answer": "Privacy threats: (1) Surveillance — centralised server tracking user contacts and movements. (2) Identification — contact graph reveals relationships and locations. (3) Aggregation — combining exposure notifications with timing reveals movement patterns. (4) Correlation — matching app IDs across multiple observations re-identifies pseudonymous users. Privacy-by-design responses: Decentralised architecture (DP-3T/GAEN) — contact identifiers generated locally, compared locally; no central contact graph. Rolling proximity identifiers — device broadcasts rotating random IDs (changed every 10–20 min) preventing tracking across time. No location data — proximity only via Bluetooth signal strength; GPS not used. Minimisation — only positive cases upload keys; negative contacts never uploaded. Purpose limitation — app cannot be used for purposes other than exposure notification, enforced technically. Open source — independent audit of privacy claims.",
            },
            {
                "year": 2021, "exam_slot": "Q1c", "marks": 10,
                "question_text": "Describe the security processes a hospital should have in place to manage the ongoing security of the remote patient monitoring system.",
                "sample_answer": "Ongoing security processes: (1) Vulnerability management — subscribe to ICS/medical device CVE feeds; patch devices within defined SLA (critical: 24h, high: 7 days). (2) Penetration testing — annual external pen test of monitoring infrastructure; quarterly internal. (3) Security monitoring — SIEM with rules for anomalous device behaviour, off-hours access, unusual data volumes. (4) Incident response plan — defined playbook for monitoring system compromise; includes clinical fallback (paper-based monitoring). (5) Access review — quarterly review of who has access to monitoring dashboard; remove leavers immediately. (6) Vendor management — monitoring device vendors must provide security roadmaps and patch support; end-of-life devices replaced. (7) Staff training — annual security awareness for clinical and IT staff. (8) Configuration management — maintain inventory of all devices; flag unauthorised devices. All processes documented and audited annually.",
            },
            {
                "year": 2020, "exam_slot": "Q1c", "marks": 10,
                "question_text": "Describe the privacy threats facing tenants and landlords using the rental deposit scheme, using appropriate threat categories.",
                "sample_answer": "Privacy threats: (1) Stored data exposure — personal and financial data (bank details, PPSN, address) held long-term; breach exposes sensitive data of both parties. (2) Aggregation — combining deposit history, addresses, and financial data across transactions builds detailed housing profiles. (3) Identification — pseudonymised records re-identifiable via address and financial data combination. (4) Surveillance — government can see all rental relationships and movement patterns of population. (5) Secondary use — rental data used for tax enforcement or social welfare checks beyond deposit protection purpose. (6) Exclusion — parties may not know what data is held or how to access/correct it. Mitigations per GDPR: lawful basis (legal obligation for deposit protection only), data minimisation (no data beyond what's needed), purpose limitation enforced technically (separate data stores per use), privacy notice clearly stating all uses, Subject Access Request process, automatic deletion when deposit discharged.",
            },
            {
                "year": 2019, "exam_slot": "Q1c", "marks": 10,
                "question_text": "Describe how a university should handle a data breach discovered during the cloud migration. What are the legal and operational obligations?",
                "sample_answer": "Legal obligations: GDPR Art. 33 — notify Data Protection Commissioner within 72 hours of becoming aware of a breach likely to result in risk to individuals' rights. Art. 34 — if high risk to individuals (e.g. student health or financial data), notify affected individuals without undue delay. Operational steps: (1) Contain — isolate affected systems; revoke compromised credentials immediately. (2) Assess — determine what data was exposed, how many individuals, how it occurred. (3) Document — record breach details, impact assessment, remediation steps. (4) Notify DPC — within 72h with: nature of breach, categories and approximate number of individuals, likely consequences, measures taken. (5) Notify individuals — if high risk; clear language, specific risk. (6) Remediate — fix root cause; patch systems; update access controls. (7) Post-incident review — what failed, process improvement. Appoint Data Protection Officer if not already in place (required for universities processing large-scale student data).",
            },
            {
                "year": 2018, "exam_slot": "Q1c", "marks": 10,
                "question_text": "Describe the privacy threats posed by a national biometric ID system, and what legal and technical safeguards should be in place.",
                "sample_answer": "Privacy threats: (1) Identification — biometrics permanently link physical person to database record; no pseudonymisation possible. (2) Surveillance — biometric checkpoints enable mass tracking of citizen movements. (3) Aggregation — combining biometric ID with travel, financial, health records creates comprehensive life profiles. (4) Secondary use — biometric database originally for ID used for policing, immigration enforcement, etc. (5) Exclusion — citizens cannot know how their biometric data is used or shared. (6) Non-revocability — unlike passwords, compromised biometrics cannot be changed. Safeguards: legal — purpose limitation in primary legislation; independent oversight body; ban on real-time biometric surveillance; Subject Access Rights. Technical — derive templates from biometrics (cannot reconstruct original); store templates in encrypted HSMs; audit log of every query; strict access controls with MFA. International — Interpol/EU data sharing agreements must specify purpose limitation. Privacy Impact Assessment mandatory before deployment.",
            },
            {
                "year": 2017, "exam_slot": "Q1c", "marks": 10,
                "question_text": "Describe the security processes ESB should use to ensure the ongoing security of the smart meter infrastructure after rollout.",
                "sample_answer": "Ongoing processes: (1) Firmware update management — signed firmware updates; staged rollout (1% → 10% → 100%); rollback capability; update signing keys in HSM. (2) Security monitoring — anomaly detection on meter readings (sudden spikes/drops may indicate tampering); alert on unusual command traffic. (3) Incident response — playbook for mass meter compromise; ability to isolate affected meters without cutting power to unaffected customers. (4) Penetration testing — annual test of communications infrastructure and backend systems. (5) Key management — regular rotation of meter authentication keys; revocation process for compromised meters. (6) Vendor security management — meter manufacturer must provide vulnerability disclosure and patch support for device lifetime (15+ years). (7) Regulatory compliance — GDPR for usage data; NIS Directive for critical infrastructure. (8) Red team exercises — simulate nation-state attack on grid management systems.",
            },
            {
                "year": 2016, "exam_slot": "Q1c", "marks": 10,
                "question_text": "Describe the privacy threats facing customers of the bank's mobile app, and the measures the bank should take to address them.",
                "sample_answer": "Privacy threats: (1) Stored data exposure — transaction history, balance, payees stored on device and server; breach reveals financial behaviour. (2) Surveillance — app usage patterns reveal spending habits, location at time of transactions, lifestyle. (3) Aggregation — combining transaction data with other data sources (location, merchant categories) enables detailed financial profiling. (4) Identification — account numbers and transaction details uniquely identify individuals. (5) Secondary use — transaction analytics used for marketing beyond banking service. (6) Exclusion — customers may not know what data is collected or retained. Measures: privacy notice clearly explaining all data uses; consent for analytics beyond service delivery; data minimisation — do not log unnecessary device data; encryption at rest and in transit; short session timeouts; secure deletion of cached data on logout; right to erasure for closed accounts (within legal retention requirements); DPA as processor if using third-party analytics.",
            },
        ],
    },
    {
        "slug": "q2-tls-protocols",
        "title": "Q2 — TLS / Protocols",
        "description": "TLS 1.3 handshake, key schedule, AEAD record layer, named attacks, PQC migration.",
        "exam_slot": "Q2",
        "overview": """# How to Answer Q2 — TLS / Protocols

## The Pattern

Q2 is almost always about TLS 1.3. Since 2020 it has been TLS 1.3 exclusively. Earlier years covered TLS 1.2 and SSL weaknesses. The question is usually split into two halves.

**Q2a (~25 marks): Describe TLS 1.3 in detail — handshake, key schedule, record layer.**
**Q2b (~25 marks): Describe a named attack, OR PQC migration, OR forward secrecy, OR testing.**

---

## Q2a Template — TLS 1.3 Full Answer

Cover in this order:

### 1. Handshake (1-RTT)
- ClientHello: supported versions, cipher suites, key_share (X25519 or P-256), SNI, session ticket
- ServerHello: selected version=1.3, cipher, key_share
- Server immediately sends: EncryptedExtensions, Certificate, CertificateVerify (sig over transcript hash), Finished (HMAC)
- Client sends: Finished (HMAC)
- Everything after ServerHello is encrypted

### 2. Key Schedule (HKDF)
- HKDF-Extract → HKDF-Expand pattern
- early_secret → handshake_secret → master_secret
- Separate keys: client_handshake_traffic, server_handshake_traffic, client_application_traffic, server_application_traffic
- Each key derived from transcript hash at that point

### 3. Record Layer (AEAD only)
- No CBC, no RC4, no MAC-then-encrypt
- Only: AES-128-GCM, AES-256-GCM, ChaCha20-Poly1305
- Record format: type, version (fixed), length, AEAD ciphertext+tag
- Sequence number used as nonce component

### 4. Optional — 0-RTT
- PSK from previous session, early data in ClientHello
- Replay risk — server must be idempotent for 0-RTT data or use anti-replay

---

## Named Attacks to Know

| Attack | TLS version | What it exploits | Fix |
|--------|-------------|------------------|-----|
| BEAST | TLS 1.0 CBC | IV predictability in CBC | Upgrade to 1.1+ / AES-GCM |
| POODLE | SSL 3.0 | CBC padding oracle | Disable SSL 3.0 |
| CRIME/BREACH | TLS compression | Compression leaks secret length | Disable compression |
| Heartbleed | OpenSSL | Buffer over-read in heartbeat extension | Patch; revoke+reissue certs |
| ROBOT | RSA PKCS#1 v1.5 | Bleichenbacher oracle on key exchange | Use ECDHE, remove RSA key exchange |
| DROWN | SSLv2 cross-protocol | SSLv2 oracle decrypts RSA | Disable SSLv2 everywhere |
| RC4 weakness | All versions using RC4 | Biases in RC4 keystream | Remove RC4 from cipher suites |

---

## Testing TLS Implementations

- RFC 8448 test vectors (known-answer tests for key schedule)
- tlsfuzzer — fuzzes TLS state machine
- BoringSSL / NSS interoperability testing
- Fuzz the handshake parser with AFL/libFuzzer
- Static analysis (memory safety bugs — Heartbleed class)
- Differential testing across implementations

---

## PQC in TLS (for recent years)

- X25519Kyber768 hybrid key exchange in ClientHello key_share
- ECDSA/RSA signatures still classical (signatures not yet PQC)
- Chrome/Firefox ship experimental support
- Hybrid because Kyber not yet proven in production

---

## Marks Traps

- Do NOT say "TLS uses asymmetric encryption to encrypt data" — it uses AEAD symmetric with derived keys.
- Do NOT say "HTTPS = encrypted HTTP" without mentioning TLS and the handshake.
- Name specific cipher suites: TLS_AES_128_GCM_SHA256, not just "AES".
- Mention forward secrecy explicitly: ephemeral key exchange means compromise of server's long-term key doesn't expose past sessions.
""",
        "topics": [
            {"slug": "tls13-handshake", "title": "TLS 1.3 Handshake (1-RTT + 0-RTT)", "order": 1, "depends_on": []},
            {"slug": "tls13-key-schedule", "title": "TLS 1.3 Key Schedule (HKDF)", "order": 2, "depends_on": ["tls13-handshake"]},
            {"slug": "tls13-record-layer", "title": "Record Layer + AEAD", "order": 3, "depends_on": ["tls13-key-schedule"]},
            {"slug": "forward-secrecy", "title": "Forward Secrecy + Key Compromise Impact", "order": 4, "depends_on": ["tls13-handshake"]},
            {"slug": "tls-attacks", "title": "Named TLS Attacks (BEAST → TLStorm)", "order": 5, "depends_on": ["tls13-record-layer"]},
            {"slug": "tls-dos", "title": "DoS Vectors + Mitigations", "order": 6, "depends_on": ["tls13-handshake"]},
            {"slug": "pqc-tls", "title": "PQC Migration in TLS (Hybrid X25519+Kyber)", "order": 7, "depends_on": ["tls13-key-schedule"]},
            {"slug": "large-scale-tls", "title": "Large-Scale TLS (CA trust, OCSP, LE)", "order": 8, "depends_on": ["tls13-handshake"]},
        ],
        "exam_questions": [
            {
                "year": 2025, "exam_slot": "Q2a", "marks": 25,
                "question_text": "For TLS 1.3, describe the key management and application data protection aspects of the protocol in detail. Describe how a library developer might test their implementation.",
                "sample_answer": "TLS 1.3 Handshake (1-RTT): ClientHello sends supported versions, cipher suites, key_share (X25519), SNI. ServerHello replies with version=1.3, cipher, key_share. Server sends EncryptedExtensions, Certificate, CertificateVerify (sig over transcript), Finished (HMAC). Client sends Finished. Key schedule: HKDF derives early_secret → handshake_secret → master_secret, producing separate client/server handshake and application traffic keys. Record layer: AEAD only (AES-128-GCM, ChaCha20-Poly1305). No MAC-then-encrypt. Forward secrecy by default via ephemeral key exchange. 0-RTT with PSK possible but replay risk. Testing: RFC 8448 test vectors, tlsfuzzer, interop against BoringSSL/NSS, AFL fuzz on handshake parser.",
            },
            {
                "year": 2024, "exam_slot": "Q2a", "marks": 25,
                "question_text": "Describe the TLS 1.3 handshake in detail, including the key schedule and what messages are encrypted. Compare with TLS 1.2.",
                "sample_answer": "TLS 1.3: ClientHello includes key_share (no separate key exchange phase). ServerHello ends plaintext phase. All subsequent messages (EncryptedExtensions, Certificate, CertificateVerify, Finished) are encrypted using handshake keys derived via HKDF. Client Finished completes handshake. Key schedule: HKDF(early_secret, ECDHE) → handshake_secret → master_secret. TLS 1.2 differences: separate ServerKeyExchange message; RSA key exchange still possible (not forward-secret); MAC-then-encrypt in CBC mode; negotiated PRF; Certificate and CertificateRequest sent in plaintext. TLS 1.3 removes RSA key exchange, export ciphers, static DH, CBC+HMAC, renegotiation. Mandatory forward secrecy.",
            },
            {
                "year": 2024, "exam_slot": "Q2b", "marks": 25,
                "question_text": "Describe the Heartbleed vulnerability: how it works, how it was discovered, its impact, and how it could have been prevented.",
                "sample_answer": "Heartbleed (CVE-2014-0160) was a bounds-checking bug in OpenSSL's TLS heartbeat extension (RFC 6520). The heartbeat message allows a peer to send a payload and receive it echoed back. OpenSSL trusted the length field in the request without checking it against actual payload length. An attacker sent a 1-byte payload with length=65535, causing OpenSSL to read 65534 bytes of heap memory beyond the payload — potentially exposing private keys, session tokens, plaintext. Discovered by Google and Codenomicon independently. Impact: ~17% of HTTPS servers affected; required patching, certificate revocation, key regeneration. Prevention: memory-safe language (Rust), bounds checking, separate heap allocation for heartbeat responses, fuzzing the heartbeat handler.",
            },
            {
                "year": 2023, "exam_slot": "Q2a", "marks": 25,
                "question_text": "Describe the TLS 1.3 record layer in detail. Why was the record layer redesigned from TLS 1.2? What attacks does the new design prevent?",
                "sample_answer": "TLS 1.3 record layer uses only AEAD ciphers (AES-128-GCM, AES-256-GCM, ChaCha20-Poly1305). Structure: ContentType, legacy_version=0x0303, length, encrypted_record. The actual ContentType is hidden inside the encrypted payload (prevents traffic analysis of message types). Nonce: XOR of IV with sequence number. TLS 1.2 problems: CBC with HMAC allowed MAC-then-encrypt padding oracle attacks (BEAST: predictable IV in CBC; POODLE: SSL 3.0 padding oracle). RC4 had keystream biases. Compression enabled CRIME (length oracle). AEAD simultaneously provides confidentiality + integrity + authentication in one pass with no separate MAC. Padding oracle attacks impossible without CBC. Compression removed entirely.",
            },
            {
                "year": 2023, "exam_slot": "Q2b", "marks": 25,
                "question_text": "What is forward secrecy? Why does TLS 1.3 provide it by default while TLS 1.2 did not? Describe the impact of private key compromise with and without forward secrecy.",
                "sample_answer": "Forward secrecy: compromise of a long-term private key does not compromise past session keys. TLS 1.3 achieves this by mandating ephemeral key exchange (X25519 or P-256 ECDHE). Each session generates a fresh key pair; after the session the private key is deleted. The server's certificate private key is only used to authenticate (sign the transcript); it never encrypts session keys. TLS 1.2 allowed RSA key exchange: ClientKeyExchange contains a pre-master secret encrypted with the server's RSA public key. If the server's RSA private key is later compromised, an attacker with a recorded transcript can decrypt it. With FS: recorded traffic is useless without per-session ephemeral keys. Without FS: retroactive decryption is possible. TLS 1.3 removed static RSA and static DH key exchange entirely.",
            },
            {
                "year": 2022, "exam_slot": "Q2a", "marks": 25,
                "question_text": "Describe the TLS 1.3 key schedule in detail. What keys are derived and when are they used?",
                "sample_answer": "HKDF (RFC 5869) is used throughout. Steps: (1) early_secret = HKDF-Extract(0, PSK or 0) — used for 0-RTT early traffic keys. (2) HKDF-Extract(early_secret, ECDHE output) → handshake_secret. (3) client_handshake_traffic_secret, server_handshake_traffic_secret derived using HKDF-Expand-Label with transcript hash up to ServerHello. These encrypt Certificate, CertificateVerify, Finished messages. (4) HKDF-Extract(handshake_secret, 0) → master_secret. (5) client_application_traffic_secret_0, server_application_traffic_secret_0 derived with full transcript. (6) Separate exporter_master_secret for TLS exporters. (7) resumption_master_secret for PSK session tickets. Keys are directional (client/server), different for each direction, rotatable with KeyUpdate message.",
            },
            {
                "year": 2022, "exam_slot": "Q2b", "marks": 25,
                "question_text": "Describe Certificate Transparency (CT) and its role in TLS. What problem does it solve and what are its limitations?",
                "sample_answer": "CT (RFC 9162) is a public append-only log of all TLS certificates issued by CAs. CAs submit certificates to logs; logs return a Signed Certificate Timestamp (SCT). Browsers require SCTs in TLS handshake or OCSP staple to accept certificates. Problem solved: rogue or compromised CAs issuing fraudulent certificates (e.g. DigiNotar 2011, Google/Symantec disputes). CT allows domain owners to monitor logs for unauthorised certificates. Limitations: doesn't prevent misissuance, only makes it detectable; log operators could collude; monitoring requires automation; CT doesn't cover private/internal CAs; SCTs can be included in cert, TLS extension, or OCSP — inconsistent deployment. Complements CAA DNS records (specify which CAs may issue for domain).",
            },
            {
                "year": 2021, "exam_slot": "Q2a", "marks": 25,
                "question_text": "Describe the BEAST attack on TLS 1.0 and the POODLE attack on SSL 3.0. What do they have in common and how were they mitigated?",
                "sample_answer": "BEAST (2011): TLS 1.0 CBC used the previous record's ciphertext as the IV for the next record (chained IV). An attacker with a chosen-plaintext oracle (e.g. malicious JS) and network capture could predict the IV and make guesses about plaintext. POODLE (2014): SSL 3.0 CBC padding is not authenticated — the padding bytes are ignored after decryption. Attacker can manipulate padding bytes and use MITM to determine whether padding is valid, leaking 1 byte per 256 requests. Common: both exploit CBC mode's sensitivity to predictability and the separation of MAC from encryption (MAC-then-encrypt). Mitigations: BEAST — upgrade to TLS 1.1+, or use RC4 (short-term only, RC4 also broken). POODLE — disable SSL 3.0 entirely (TLS_FALLBACK_SCSV prevents downgrade). Long-term: TLS 1.3 removes CBC+MAC entirely, uses only AEAD.",
            },
            {
                "year": 2021, "exam_slot": "Q2b", "marks": 25,
                "question_text": "Describe DoS vulnerabilities in TLS and how they can be mitigated, both in TLS 1.2 and TLS 1.3.",
                "sample_answer": "TLS handshake is asymmetric in cost: client sends cheap ClientHello; server must perform expensive key exchange (ECDH) and certificate operations. TLS 1.2 renegotiation: client can request unlimited renegotiations, each costing a full handshake — amplification attack on server CPU. TLS 1.3 removes renegotiation (uses KeyUpdate instead). Mitigations: (1) Stateless cookies — server sends HelloRetryRequest with a cookie; client must echo it, proving reachability (proof-of-work). (2) Session resumption / PSK — avoids full crypto for returning clients. (3) Rate limiting per IP on handshake rate. (4) TLS termination at load balancer offloads crypto cost. (5) Hardware acceleration (AES-NI, dedicated TLS offload cards). (6) Client puzzles for expensive endpoints. TLS 1.3 session tickets reduce server-side state requirements.",
            },
            {
                "year": 2020, "exam_slot": "Q2a", "marks": 25,
                "question_text": "Describe how post-quantum cryptography (PQC) affects TLS. What changes are needed and why?",
                "sample_answer": "Current TLS key exchange (X25519, P-256) and signatures (ECDSA, RSA) are broken by Shor's algorithm on a cryptographically relevant quantum computer. TLS 1.3 changes needed: (1) Key exchange: replace ECDHE with Kyber (NIST ML-KEM) — a lattice-based KEM. Hybrid approach: X25519Kyber768 in key_share provides classical+PQC security simultaneously. (2) Signatures: ML-DSA (Dilithium) or SLH-DSA (SPHINCS+) to replace ECDSA/RSA in CertificateVerify. Challenges: Kyber public keys/ciphertexts are larger (1KB+) vs X25519 (32 bytes) — affects handshake size and MTU fragmentation. Post-quantum signatures are much larger (Dilithium ~2.4KB). Harvest-now-decrypt-later threat: adversaries record TLS traffic now to decrypt after quantum computing matures — so key exchange must be upgraded urgently even before signatures.",
            },
            {
                "year": 2019, "exam_slot": "Q2a", "marks": 25,
                "question_text": "Describe the ROBOT attack and the class of vulnerability it represents. How does TLS 1.3 eliminate this class of attack?",
                "sample_answer": "ROBOT (Return Of Bleichenbacher's Oracle Threat, 2017) is a revival of Bleichenbacher's 1998 attack on RSA PKCS#1 v1.5 padding. In TLS 1.2 RSA key exchange, the client encrypts the pre-master secret with the server's RSA public key. PKCS#1 v1.5 padding validation produces different error messages (or timing differences) depending on whether padding is valid. An adaptive chosen-ciphertext attacker can send crafted ciphertexts and observe server responses to gradually recover the pre-master secret using ~millions of queries. ROBOT found 27 of the top 100 HTTPS sites vulnerable in 2017. TLS 1.3 eliminates this by removing RSA key exchange entirely — only ephemeral ECDHE is allowed, so there is no server-decrypted value an oracle can leak.",
            },
            {
                "year": 2019, "exam_slot": "Q2b", "marks": 25,
                "question_text": "Describe OCSP stapling and Certificate Revocation Lists (CRLs). What are their limitations and what has replaced them at scale?",
                "sample_answer": "CRLs: CAs publish signed lists of revoked certificate serial numbers. Clients download and check. Problems: CRLs grow large; clients cache stale CRLs; revocation check adds latency; many clients soft-fail (accept cert if CRL unavailable). OCSP (Online Certificate Status Protocol): real-time per-certificate revocation query to CA's OCSP responder. Problems: privacy (CA learns which sites you visit); OCSP responder availability becomes a dependency; still soft-fail by default. OCSP Stapling: server fetches and caches OCSP response, staples it to TLS handshake (CertificateStatus message). Eliminates client-CA round trip and privacy leak. Must-Staple: certificate extension requiring stapled OCSP — hard-fail if missing. At scale: Chrome moved to CRLSets (compressed, pushed via browser update); Let's Encrypt short-lived certs (90-day) make revocation less critical — expiry is the revocation.",
            },
            {
                "year": 2018, "exam_slot": "Q2a", "marks": 25,
                "question_text": "Describe STARTTLS. What security properties does it provide and what attacks are possible against it?",
                "sample_answer": "STARTTLS is an opportunistic TLS upgrade mechanism for protocols that start in plaintext (SMTP, IMAP, XMPP). Client connects on plain port (25, 143), server advertises STARTTLS capability, client sends STARTTLS command, both negotiate TLS. Security properties: encrypts data in transit; prevents passive eavesdropping; authenticates server with certificate. Attacks: (1) STARTTLS stripping — active attacker removes STARTTLS from server capability advertisement; client falls back to plaintext. Most SMTP clients opportunistically downgrade. (2) Invalid certificate acceptance — SMTP commonly ignores certificate errors in opportunistic mode. (3) SMTP smuggling — interplay between STARTTLS and SMTP command parsing. Mitigations: DANE/TLSA records in DNS (requires DNSSEC) to pin expected certificate; MTA-STS policy file to enforce TLS; SMTP STS (RFC 8461) for enforced TLS between mail servers.",
            },
            {
                "year": 2017, "exam_slot": "Q2a", "marks": 25,
                "question_text": "Describe the role of Certificate Authorities in TLS. What trust model do they implement and what are its weaknesses?",
                "sample_answer": "CAs are third parties trusted by browsers/OS to certify that a public key belongs to a domain. WebPKI trust model: browsers ship a trust store of ~150 root CAs; any root CA can issue for any domain (no name constraints by default). Weaknesses: (1) Any root CA compromise allows MITM on any site — DigiNotar (2011) issued fraudulent google.com cert; CA revoked but damage done. (2) Intermediate CA compromise extends attack scope. (3) Nation-state CAs in browser trust stores. (4) DV certificates only verify domain control (not identity). Mitigations: Certificate Transparency (audit logs); CAA DNS records (restrict which CAs can issue for a domain); HPKP (deprecated — too risky); shorter certificate lifetimes (Let's Encrypt 90 days, now moving to 47 days).",
            },
            {
                "year": 2016, "exam_slot": "Q2a", "marks": 25,
                "question_text": "Describe the Diffie-Hellman key exchange and explain how it is used in TLS. What are the weaknesses of static DH and why does TLS 1.3 mandate ephemeral DH?",
                "sample_answer": "DH key exchange: Alice and Bob agree on public parameters (g, p). Alice sends g^a mod p, Bob sends g^b mod p. Both compute shared secret g^(ab) mod p. An eavesdropper cannot compute g^(ab) without solving the discrete logarithm. In TLS 1.2: static DH — server's DH public value is in its certificate (long-term). Same public value used in every session. If private key compromised (or if DLP solved for that key), all past sessions decryptable. Ephemeral DH (DHE): fresh keypair per session; session key deleted after use → forward secrecy. TLS 1.3: only ECDHE allowed in key_share (X25519, P-256). Static RSA and static DH removed entirely. Logjam attack (2015): 512-bit export DH parameters vulnerable to DLP via NFS; servers using common primes vulnerable to pre-computation attack. TLS 1.3 removes export grades and requires minimum 2048-bit FFDHE or P-256/X25519 ECDHE.",
            },
        ],
    },
    {
        "slug": "q3-system-design",
        "title": "Q3 — System Design",
        "description": "Design national/federated systems with security requirements, auth, crypto, audit.",
        "exam_slot": "Q3",
        "overview": """# How to Answer Q3 — System Design

## The Pattern

Q3 is a design question: you're given a national or institutional system to design securely. The sub-parts follow a consistent structure across all years.

**Q3a (~10 marks): List security requirements for the system.**
**Q3b (~20 marks): Describe a secure architecture meeting those requirements.**
**Q3c (~10 marks): Describe how you would attack the system you designed.**

---

## Q3a Template — Security Requirements

Use the CIA+ framework as your backbone:

- **Confidentiality**: only authorised parties can read data
- **Integrity**: data cannot be modified without detection
- **Availability**: system is accessible when needed
- **Authentication**: parties must prove identity before access
- **Authorisation**: authenticated parties can only do what they're permitted
- **Non-repudiation**: actions cannot be denied after the fact
- **Audit**: all significant actions are logged permanently
- **Privacy**: personal data handled per GDPR/data minimisation

Make requirements specific to the scenario. "The system must ensure only authorised prescribers can issue prescriptions" beats "the system must be confidential."

---

## Q3b Template — Secure Architecture

Structure your architecture answer as:

### 1. Authentication + Authorisation
- Who authenticates: patients, GPs, pharmacists, admins — each needs different auth
- MFA: FIDO2 hardware keys for admin, TOTP for professionals, citizen-facing: FIDO2 via passkeys
- RBAC: prescriber role (issue), dispenser role (mark dispensed), admin role (audit only)
- OIDC/OAuth2 for federated identity across organisations
- Session management: short-lived JWTs, server-side revocation

### 2. Crypto
- TLS 1.3 everywhere (no fallback)
- Data at rest: AES-256-GCM
- Signing: Ed25519 for prescriptions/records
- Key management: HSM for signing keys; key rotation policy
- No passwords stored in plaintext (bcrypt/Argon2)

### 3. Network
- WAF, DDoS mitigation upstream
- Network segmentation: DB not directly reachable from internet
- Bastion host / VPN for admin access

### 4. Audit + Logging
- Append-only audit log (hash-chained like a blockchain)
- Log: who, what, when, from where, on what data
- Logs shipped to separate SIEM immediately
- DBA cannot delete audit logs — separate log server with different credentials

### 5. Data
- Encrypt PII at rest
- Data minimisation: only store what's needed
- Pseudonymisation where full identity not needed

---

## Q3c Template — Attack the System

Pick 3 attack vectors. Each: (a) what you target, (b) specific technique, (c) what you gain, (d) which defence it bypasses.

**Best attacks to use:**
1. **Phishing an admin**: spear-phish → credential harvest → bypass all technical controls. Say: "SMS OTP doesn't help — use FIDO2 which is phishing-resistant."
2. **Insider threat**: DBA or sysadmin with legitimate access. Exports data at off-hours. Missed by access controls — caught only by UEBA in SIEM.
3. **Debug endpoint**: scan for `/admin`, `/.env`, `/actuator` — often left in production. No auth required.
4. **Supply chain**: compromise a library/dependency used in the system. Reference XZ backdoor (2024) or SolarWinds (2020).

---

## Marks Traps

- Do NOT say "use a firewall" and nothing else — say what it's blocking and how.
- Do NOT just list HTTPS — mention TLS 1.3 and why (AEAD, forward secrecy).
- Do NOT forget the attack section (Q3c) — Farrell rewards honest self-critique.
- Do NOT forget audit logs — this is always worth marks.
""",
        "topics": [
            {"slug": "security-requirements", "title": "Writing Security Requirements (CIA+)", "order": 1, "depends_on": []},
            {"slug": "architecture-patterns", "title": "Secure Architecture Patterns", "order": 2, "depends_on": ["security-requirements"]},
            {"slug": "authn-authz", "title": "Authentication + Authorisation (RBAC, FIDO2, OIDC)", "order": 3, "depends_on": ["architecture-patterns"]},
            {"slug": "crypto-in-systems", "title": "Crypto in System Design (HSM, key rotation)", "order": 4, "depends_on": ["authn-authz"]},
            {"slug": "audit-logging", "title": "Audit + Logging (append-only, hash-chained)", "order": 5, "depends_on": ["crypto-in-systems"]},
            {"slug": "attack-the-system", "title": "Being the Attacker (insider, supply chain, DoS)", "order": 6, "depends_on": ["architecture-patterns"]},
        ],
        "exam_questions": [
            {
                "year": 2025, "exam_slot": "Q3a", "marks": 10,
                "question_text": "A national e-health prescription system will allow GPs to issue digital prescriptions, pharmacists to dispense, and patients to view their prescription history. List the security requirements for this system.",
                "sample_answer": "Confidentiality: prescriptions visible only to the prescribing GP, patient, and dispensing pharmacist. Integrity: prescriptions must not be alterable after issuance (cryptographic signing). Availability: system must be available 24/7 (patient safety). Authentication: GPs and pharmacists must use strong MFA (FIDO2); patients must authenticate with eIDAS-compatible identity. Authorisation: RBAC — GPs can issue, pharmacists can mark dispensed, patients can view only their own. Audit: all prescription events logged permanently and tamper-evident. Non-repudiation: GP's digital signature on each prescription. Privacy: GDPR compliance, data minimisation, encrypted PII at rest.",
            },
            {
                "year": 2025, "exam_slot": "Q3b", "marks": 20,
                "question_text": "Describe a secure architecture for the national e-health prescription system, justifying your design choices.",
                "sample_answer": "Auth: FIDO2 hardware tokens for GPs/pharmacists via OIDC federated to HSE identity provider. Patients authenticate via MyGovID (eIDAS). RBAC: prescriber, dispenser, patient roles with least privilege. Prescriptions: GP signs prescription with Ed25519 key stored in HSM; signature stored alongside prescription. TLS 1.3 everywhere. DB: encrypted at rest (AES-256-GCM), keys in HSM. Audit: append-only hash-chained log shipped to separate SIEM — DBA cannot modify. Network: WAF, DDoS mitigation, DB on isolated subnet. API gateway validates JWT claims before forwarding. Pharmacist redemption: two-factor (pharmacist auth + patient eID scan) prevents forgery.",
            },
            {
                "year": 2025, "exam_slot": "Q3c", "marks": 10,
                "question_text": "Describe how you would attack the e-health prescription system you designed.",
                "sample_answer": "1. Phish a GP: spear-phishing email appearing to be HSE IT support requests FIDO2 device re-registration. GP visits attacker-controlled page, attacker uses real-time MITM (Evilginx2) to relay credentials. SMS MFA would fall here; FIDO2 resists phishing but registration flow could be targeted. 2. Insider: pharmacy staff member with dispenser role marks prescriptions as dispensed without physically dispensing — fraud. Detection requires anomaly detection on dispensing rates in SIEM. 3. Supply chain: compromise a dependency in the prescription signing library. Valid-looking prescriptions issued by attacker's key. Mitigate via SBOM and dependency pinning, but hard to prevent a patient maintainer attack (XZ-style).",
            },
            {
                "year": 2024, "exam_slot": "Q3a", "marks": 10,
                "question_text": "A university is deploying a federated identity system allowing staff and students to use a single login across all university services (email, LMS, library, VPN). List the security requirements.",
                "sample_answer": "Confidentiality: credentials and session tokens must not be exposed to relying party services. Integrity: identity assertions must not be forgeable. Authentication: phishing-resistant MFA for all accounts; step-up authentication for sensitive services (VPN, finance). Authorisation: service-specific attribute-based access (staff vs student vs admin). Availability: IdP must be highly available — its failure breaks all services. Audit: log all authentications, service accesses, and privilege changes. Account lifecycle: immediate deactivation on staff departure. Privacy: services receive minimal attributes (no oversharing of personal data).",
            },
            {
                "year": 2024, "exam_slot": "Q3b", "marks": 20,
                "question_text": "Describe a secure architecture for the university federated identity system.",
                "sample_answer": "Deploy OIDC/OAuth2 with a university IdP (Keycloak or Azure AD). SAML federation for legacy services. MFA: FIDO2 passkeys for staff, TOTP for students initially with FIDO2 upgrade path. Step-up auth policy: VPN and finance require FIDO2. Claims: IdP issues minimal claims per service (student number for LMS, not full profile). Session: short-lived access tokens (15 min), refresh tokens server-side revocable. SCIM provisioning: student/staff changes in HR system propagate to IdP automatically. Audit: all login events, token issuances, and anomalies shipped to SIEM. Redundancy: active-active IdP clusters in two datacentres. Consent: students consent to attribute release per service.",
            },
            {
                "year": 2024, "exam_slot": "Q3c", "marks": 10,
                "question_text": "Describe how you would attack the federated identity system.",
                "sample_answer": "1. Phish the IdP admin: the IdP is the single point of control. Compromise of an IdP admin account allows creation of persistent backdoor accounts, modification of attribute claims, or disabling MFA enforcement globally. SMS OTP doesn't resist real-time MITM phishing. 2. OAuth2 redirect_uri manipulation: if a relying party registers a wildcard redirect_uri, attacker can steal authorisation codes via open redirect on the RP domain. Grants access to the victim's account on that service. 3. Offline password cracking against legacy LDAP backend: if IdP federates to an on-premise LDAP and LDAP uses NTLM or weak hash, extract hashes via a compromised internal machine and crack offline using GPU rigs.",
            },
            {
                "year": 2023, "exam_slot": "Q3a", "marks": 10,
                "question_text": "The Irish government plans a digital identity wallet allowing citizens to store verifiable credentials (driving licence, passport, medical card) on their phone. List security requirements.",
                "sample_answer": "Confidentiality: credentials stored encrypted on device, not on central server. Integrity: credentials must be cryptographically signed by issuing authority and unalterable. Authentication: biometric unlock required to access wallet; device binding prevents credential theft. Authorisation: citizen controls which attributes they share and with whom (selective disclosure). Availability: offline presentation must work (no internet required at verification point). Audit: citizen can see log of all presentations. Non-repudiation: verifier receives signed presentation. Privacy: zero-knowledge or selective disclosure to minimise data shared (e.g. prove age without revealing birthdate).",
            },
            {
                "year": 2023, "exam_slot": "Q3b", "marks": 20,
                "question_text": "Describe a secure architecture for the digital identity wallet.",
                "sample_answer": "Credentials: SD-JWT (Selective Disclosure JWT) or ISO mDL (mobile driving licence) format. Issuer signs with Ed25519; public key published in issuer registry (CT-style log). Wallet app: credentials stored in device secure enclave encrypted with key derived from biometric. Presentation: wallet creates verifier-specific presentation (VP) signed with holder key. Selective disclosure: only requested attributes included. Verifier checks issuer signature + holder binding + revocation status (OCSP or status list). No central server in normal flow — fully offline for presentation. Revocation: status list approach (bit vector, no per-lookup privacy leak). Key recovery: issuer can re-issue to new device after identity re-verification; no key escrow. PKCE and device attestation for wallet issuance flow.",
            },
            {
                "year": 2023, "exam_slot": "Q3c", "marks": 10,
                "question_text": "Describe how you would attack the digital identity wallet system.",
                "sample_answer": "1. Malicious verifier: verifier app requests more attributes than needed and correlates presentations across services to build a profile of citizen behaviour. Selective disclosure limits this but correlation via holder binding key is possible. Mitigation: per-verifier ephemeral keys (complicated). 2. Compromise issuer signing key: if the driving licence issuing authority's Ed25519 private key is stolen, attacker can issue unlimited fraudulent credentials indistinguishable from genuine ones. HSM and ceremony required for issuance keys. 3. Malware on citizen device: if malware pre-dates biometric prompt, it can intercept the unlocked credential store. Device attestation (Android Strongbox, iOS Secure Enclave) mitigates but not all devices support it.",
            },
            {
                "year": 2022, "exam_slot": "Q3a", "marks": 10,
                "question_text": "The EU is deploying a cross-border COVID vaccine certificate system. Citizens of 27 member states can verify each other's certificates at borders and venues. List security requirements.",
                "sample_answer": "Integrity: certificates must be unforgeable and signed by the issuing member state. Authentication: each member state authenticates its issuing authority. Availability: verification must work offline (no internet at all checkpoints). Privacy: minimum data (name, DOB, vaccine type, date) — no central tracking of movements. Interoperability: all 27 member states can verify any certificate from any other. Revocation: compromised or fraudulent certificates must be revocable. Non-repudiation: issuer's digital signature binds the certificate to the issuing authority. Audit: issuance events logged at national level.",
            },
            {
                "year": 2022, "exam_slot": "Q3b", "marks": 20,
                "question_text": "Describe the EU Digital COVID Certificate architecture (or an equivalent design).",
                "sample_answer": "EU DCC architecture: CBOR-encoded payload (name, DOB, vaccine info, issuer, expiry) signed with ECDSA (P-256). Each member state has a Document Signing Certificate (DSC) issued by national CSCA. CSCA public keys published to EU Digital COVID Certificate Gateway (DCCG) — a centralised key registry. Verifier app downloads trusted key list from DCCG, caches it locally for offline use. Presentation: QR code contains signed CBOR (COSE format). Verification: scan QR → decode CBOR → find issuer country → look up DSC from local cache → verify ECDSA signature. Revocation: member state publishes revocation list to DCCG; verifier apps sync regularly. Privacy: no central tracking — no online check at verification time. Works offline after key list cached.",
            },
            {
                "year": 2022, "exam_slot": "Q3c", "marks": 10,
                "question_text": "Describe how you would attack the EU Digital COVID Certificate system.",
                "sample_answer": "1. Compromise a member state DSC private key: issue unlimited fraudulent certificates for that country. High impact — all 27 member states trust that DSC. Mitigation: short DSC validity (1 year), HSM for DSC private key, ceremony for issuance. 2. Phish an issuing authority employee: gain access to the certificate issuance system, issue fraudulent certificates for real-looking identities. Hard to detect without anomaly detection on issuance rates. 3. QR code screen sharing: a valid certificate's QR code shared digitally is indistinguishable from the original at a venue using only basic signature checking. Mitigation: require biometric match at high-security checkpoints, or short-lived certificates forcing re-issuance.",
            },
            {
                "year": 2021, "exam_slot": "Q3a", "marks": 10,
                "question_text": "A national patient portal allows citizens to view their health records, book GP appointments, and request prescription repeats. List the security requirements.",
                "sample_answer": "Confidentiality: health records visible only to the patient and their healthcare providers. Authentication: strong MFA for citizens; FIDO2 for healthcare providers. Authorisation: patient can view own records; GP can view/add to records of their patients only. Availability: appointment booking must be highly available. Audit: access to health records logged permanently. Integrity: records must not be altered without creating an audit trail. Privacy: GDPR, data minimisation, right of access (subject access request must be supported). Non-repudiation: healthcare provider's additions to records are signed.",
            },
            {
                "year": 2021, "exam_slot": "Q3b", "marks": 20,
                "question_text": "Describe a secure architecture for the national patient portal.",
                "sample_answer": "Auth: citizens authenticate via MyGovID (eIDAS level High) with FIDO2. GPs/nurses via HIQA-issued FIDO2 tokens federated via OIDC to HSE IdP. RBAC: patient, GP, specialist, admin roles with least privilege — GP sees only their patient list. TLS 1.3 everywhere. Records: stored encrypted at rest (AES-256-GCM), decryption keys in HSM per patient. Audit: append-only hash-chained log of every record access, shipped to separate SIEM immediately. Consent: patients must consent to specialist access; consent tracked in audit log. API gateway: validates JWT claims, rate limits per user. WAF upstream. DB isolated on private subnet — no direct internet access.",
            },
            {
                "year": 2021, "exam_slot": "Q3c", "marks": 10,
                "question_text": "Describe how you would attack the national patient portal.",
                "sample_answer": "1. Target a GP: GPs use the system daily and have broad access to their patient list. Spear-phish with a fake 'HSE IT security update' email. If GP uses TOTP (not FIDO2), attacker uses Evilginx2 real-time MITM to capture TOTP and session cookie simultaneously. 2. Insider: a hospital receptionist with GP role through misconfigured RBAC queries records of celebrities or politicians. No technical control prevents this if role assignment is wrong. Detect via SIEM anomaly detection on query patterns outside normal patient list. 3. IDOR on appointment API: booking API may use sequential appointment IDs — attacker iterates IDs to access other patients' appointment details. Prevent with proper authorisation checks (not just authentication) on every record access.",
            },
            {
                "year": 2020, "exam_slot": "Q3a", "marks": 10,
                "question_text": "A national digital voting system is proposed for Irish general elections. List the security requirements. Do you think such a system could be made secure?",
                "sample_answer": "Confidentiality: ballot content anonymous and unlinkable to voter. Integrity: each vote counted exactly once, unmodifiable after cast. Authentication: voter must be uniquely identified and not vote twice. Availability: system must work on election day at national scale. Verifiability: voter can verify their vote was counted (end-to-end verifiable). Audit: independent auditors can verify total without revealing individual votes. Non-repudiation: each submitted ballot is irrefutably received. Whether it can be made secure: academic cryptographic e-voting (homomorphic tallying, mix-nets, zero-knowledge proofs) can satisfy these properties mathematically; however, the voter device (home computer) is out of your control — malware could alter votes. Physical paper ballots provide coercion-resistance that digital systems cannot. Most computer security experts oppose online voting for national elections for this reason.",
            },
            {
                "year": 2019, "exam_slot": "Q3a", "marks": 10,
                "question_text": "Revenue is deploying a new online tax filing system replacing paper returns. Taxpayers file, Revenue processes, and refunds are issued via bank transfer. List security requirements.",
                "sample_answer": "Authentication: taxpayers must authenticate with strong identity (PPSN + FIDO2 or equivalent). Integrity: submitted returns must not be alterable after submission. Non-repudiation: taxpayer's digital signature on each return. Confidentiality: tax data visible only to the taxpayer and authorised Revenue officers. Authorisation: Revenue officers access only cases assigned to them; senior officers have audit/override access. Availability: high availability during tax filing deadlines. Audit: all accesses and modifications to tax records logged permanently. Privacy: GDPR compliance, data retained only as long as legally required.",
            },
            {
                "year": 2018, "exam_slot": "Q3a", "marks": 10,
                "question_text": "The Department of Social Protection is deploying a new welfare payments system integrated with banks, employers, and local authorities. List the security requirements.",
                "sample_answer": "Confidentiality: welfare entitlement data accessible only to the claimant and authorised DSP staff. Integrity: payment amounts and bank details must not be alterable without full audit trail. Authentication: claimants via MyGovID; DSP staff via FIDO2 hardware tokens. Authorisation: RBAC — processing officers see own caseload; supervisors have override; auditors have read-only access. Non-repudiation: all payment approvals signed by approving officer. Availability: payment processing must meet statutory deadlines. Audit: complete tamper-evident log of all payment decisions. Privacy: GDPR, data minimisation, no sharing with employers beyond legal entitlement.",
            },
            {
                "year": 2017, "exam_slot": "Q3a", "marks": 10,
                "question_text": "The HSE is deploying a cross-hospital electronic health record system allowing any hospital to access a patient's records in an emergency. List security requirements.",
                "sample_answer": "Confidentiality: records accessible only to treating clinicians and patient. Integrity: medical records must be tamper-evident; audit trail for all modifications. Emergency access: break-glass access for emergency clinicians, fully logged and reviewed. Authentication: clinicians authenticate with FIDO2 hardware tokens. Authorisation: RBAC — treating clinician, specialist, GP, patient roles. Availability: must be available 24/7, including in disaster scenarios. Consent: patient consent required for non-emergency access; emergency access bypasses consent but notifies patient. Audit: every access logged with justification.",
            },
            {
                "year": 2016, "exam_slot": "Q3a", "marks": 10,
                "question_text": "A national student data platform will hold academic records, exam results, and progression data for all Irish students from primary to third level. List security requirements.",
                "sample_answer": "Confidentiality: records accessible only to the student, parent/guardian (for minors), and authorised educational institutions. Integrity: academic records must not be alterable without full audit trail. Authentication: students/parents via national identity; educators via institution-issued credentials. Authorisation: primary school records not accessible to third-level employers; graduated access based on record type and relationship. Availability: accessible during academic administration periods. Audit: all accesses and modifications logged permanently. Privacy: GDPR (children's data requires higher protection), data minimisation, right to erasure on reaching adulthood for non-statutory records.",
            },
        ],
    },
    {
        "slug": "q4-dns-dnssec",
        "title": "Q4 — DNS / DNSSEC",
        "description": "DNSSEC architecture, key hierarchy (KSK/ZSK), DoH/DoT privacy, email security.",
        "exam_slot": "Q4",
        "overview": """# How to Answer Q4 — DNS / DNSSEC

## The Pattern

Q4 is almost always about DNSSEC and DNS privacy/security extensions. Since ~2018 the question has been very consistent.

**Q4a (~20 marks): DNSSEC architecture, key hierarchy, chain of trust, records.**
**Q4b (~20 marks): DoH/DoT/ODoH privacy, email security (SPF/DKIM/DMARC), or DANE.**

---

## Q4a Template — DNSSEC Architecture

Always cover:

### 1. The Four Record Types
- **DNSKEY**: zone's public keys. Two per zone: KSK (flag 257) and ZSK (flag 256).
- **RRSIG**: digital signature over an RRset. ZSK signs A/MX/TXT; KSK signs DNSKEY.
- **DS (Delegation Signer)**: published in *parent* zone. SHA-256 hash of child's KSK. This is the chain link.
- **NSEC3**: authenticated denial of existence. Hashes names (prevents zone walking). Can still be dictionary-attacked offline.

### 2. KSK vs ZSK
| | KSK (flag 257) | ZSK (flag 256) |
|--|--|--|
| Signs | DNSKEY RRset only | All other RRsets (A, MX, etc.) |
| Lifetime | Long (1–5 years) | Short (1–3 months) |
| Storage | HSM, offline ceremony | Automated rotation |
| Parent involvement | Yes (DS record update) | No |

### 3. Chain of Trust (draw this diagram)
```
Root (trust anchor hard-coded in resolver)
  DS(.ie) in root zone
    .ie DNSKEY (KSK + ZSK)
      DS(tcd.ie) in .ie zone
        tcd.ie DNSKEY (KSK + ZSK)
          RRSIG on tcd.ie A record (signed by ZSK)
```

### 4. Trust Anchor
The root KSK public key is hard-coded in resolver software. This is the foundation. Root KSK rollover in 2018 was the first ever — multi-party ceremony, ~750k resolvers at risk.

### 5. Validation Result Flags
- `ad` (Authenticated Data): chain validated successfully
- `SERVFAIL`: validation failed — something mismatched
- `cd` (Checking Disabled): client asked resolver to skip validation

---

## Q4b Template — DNS Privacy (DoH/DoT)

**Critical distinction for marks:** DNSSEC ≠ privacy. DNSSEC provides integrity. Queries are still visible.

| | DoT | DoH |
|--|--|--|
| Port | 853 (visible) | 443 (hidden in HTTPS) |
| Firewall bypass | Easy to block | Hard to block |
| Corporate filtering | Retained | Lost |
| Browser support | No | Yes (Firefox, Chrome) |

**ODoH**: proxy sees IP, resolver sees query — neither has both.

---

## Email Security Template (SPF + DKIM + DMARC)

- **SPF**: TXT record listing authorised sending IPs for domain. Checks envelope sender. Breaks on forwarding.
- **DKIM**: private key signs email headers + body. Public key in DNS TXT at `selector._domainkey.domain`. Survives forwarding. Doesn't specify failure policy.
- **DMARC**: policy layer. `p=reject` tells receivers to reject if SPF+DKIM both fail. Requires alignment between `From:` header and SPF/DKIM domain. Aggregate reports (`rua=`) for monitoring.

**Deployment order**: SPF → DKIM → DMARC p=none (monitor) → p=quarantine → p=reject

**DNSSEC connection**: SPF/DKIM/DMARC records are DNS TXT records. Without DNSSEC, attacker can poison these records. DNSSEC protects email authentication infrastructure.

---

## DANE Bonus (mention for extra marks)

DANE uses DNSSEC to publish TLS certificate fingerprints:
```
_443._tcp.tcd.ie. TLSA 3 1 1 [SHA-256 of cert public key]
```
Allows domain owners to pin their cert without relying on WebPKI CAs. Requires DNSSEC to be trustworthy.

---

## Marks Traps

- Do NOT confuse DNSSEC and DNS privacy — Farrell asks this every year.
- Do NOT forget to mention the trust anchor (root KSK hard-coded in resolver software).
- Do NOT say NSEC prevents zone walking — NSEC3 hashes names to prevent it; NSEC (original) leaks all names.
- Always draw/describe the chain from root → TLD → zone → record.
""",
        "topics": [
            {"slug": "dns-basics", "title": "DNS Architecture + Issues", "order": 1, "depends_on": []},
            {"slug": "dnssec-records", "title": "DNSSEC Records (DNSKEY, RRSIG, DS, NSEC3)", "order": 2, "depends_on": ["dns-basics"]},
            {"slug": "dnssec-key-hierarchy", "title": "Key Hierarchy (KSK/ZSK, Chain of Trust)", "order": 3, "depends_on": ["dnssec-records"]},
            {"slug": "dnssec-validation", "title": "Validation Flow + Trust Anchors", "order": 4, "depends_on": ["dnssec-key-hierarchy"]},
            {"slug": "doh-dot-privacy", "title": "DoH / DoT / ODoH — Privacy for DNS", "order": 5, "depends_on": ["dns-basics"]},
            {"slug": "email-security", "title": "Email Security: DKIM + SPF + DMARC", "order": 6, "depends_on": ["dns-basics"]},
        ],
        "exam_questions": [
            {
                "year": 2025, "exam_slot": "Q4a", "marks": 20,
                "question_text": "Describe the DNSSEC architecture and key hierarchy in detail.",
                "sample_answer": "Chain of trust: root (IANA) → TLD (.ie) → zone (tcd.ie) → records. Two keys per zone: KSK (flag 257) signs DNSKEY RRset only, long-lived (1–5 years), hash in parent DS record; ZSK (flag 256) signs all other RRsets, short-lived (1–3 months), automated rotation. Records: DNSKEY (public keys), RRSIG (signature over RRset, by ZSK), DS (parent zone's hash of child KSK), NSEC3 (authenticated denial, hashes names to prevent zone walking). Trust anchor: root KSK hard-coded in resolver software (RFC 7958). Root KSK rolled 2018 in multi-party ceremony. Validation: start from root trust anchor → DS → child DNSKEY → RRSIG on record. `ad` flag means validated; SERVFAIL means validation failure.",
            },
            {
                "year": 2025, "exam_slot": "Q4b", "marks": 20,
                "question_text": "DNSSEC does not protect DNS privacy. Describe the mechanisms that do, their trade-offs, and the privacy issues DNSSEC leaves unaddressed.",
                "sample_answer": "DNSSEC provides integrity + authentication but DNS queries remain plaintext on the wire. Privacy mechanisms: DoT (RFC 7858, port 853) — TLS-encrypted DNS, distinguishable by port. DoH (RFC 8484, port 443) — DNS inside HTTPS, indistinguishable from web traffic, hard to block, breaks enterprise DNS filtering. ODoH (RFC 9230) — proxy separates IP from query, neither party has both. ECH (TLS Encrypted Client Hello) — encrypts SNI using HPKE, hides which website you're connecting to. DNSSEC leaves unaddressed: query origin privacy, ISP traffic analysis, resolver seeing all queries. Trade-off: DoH centralises trust in a few large resolver providers (Cloudflare, Google).",
            },
            {
                "year": 2024, "exam_slot": "Q4a", "marks": 20,
                "question_text": "Describe the DNSSEC validation process step-by-step, including how the chain of trust is established and what happens when validation fails.",
                "sample_answer": "Validation process: (1) Resolver receives A record response for tcd.ie with RRSIG. (2) Fetches tcd.ie DNSKEY RRset. (3) Verifies RRSIG on A record using tcd.ie ZSK. (4) Verifies RRSIG on DNSKEY using tcd.ie KSK. (5) Fetches DS record for tcd.ie from .ie zone. (6) Checks: SHA-256(tcd.ie KSK) == DS value. (7) Repeats up the chain: .ie DNSKEY, .ie DS from root. (8) Verifies root DNSKEY using hard-coded trust anchor. If validation fails at any step: resolver returns SERVFAIL. Client gets 'website not found' even though website exists. `ad` flag in response means chain validated. `cd` flag means client asked resolver to skip checking (not recommended).",
            },
            {
                "year": 2024, "exam_slot": "Q4b", "marks": 20,
                "question_text": "Describe DANE and how it uses DNSSEC to improve TLS certificate validation. What problem does it solve compared to WebPKI?",
                "sample_answer": "DANE (DNS-based Authentication of Named Entities, RFC 6698) uses DNSSEC to publish TLS certificate fingerprints in TLSA DNS records. Example: `_443._tcp.tcd.ie. TLSA 3 1 1 [SHA-256 of cert public key]`. TLSA record fields: usage (3=domain-issued cert), selector (1=public key), matching type (1=SHA-256). Problem solved: WebPKI relies on ~150 trusted CAs — any one can issue a certificate for any domain. DigiNotar 2011 issued fraudulent google.com certificate. DANE allows the domain owner to pin exactly which certificate/key is valid, using DNSSEC as the trust anchor instead of a CA. If DNSSEC is validated, the TLSA record is trustworthy. Limitation: requires DNSSEC on the domain and a resolver that does DNSSEC validation; browser support is limited (mostly email/SMTP, not HTTPS).",
            },
            {
                "year": 2023, "exam_slot": "Q4a", "marks": 20,
                "question_text": "Describe the DNS cache poisoning attack (Kaminsky 2008) and how DNSSEC prevents it.",
                "sample_answer": "Kaminsky attack (2008): DNS uses 16-bit transaction ID (65,536 values) + UDP source port for response matching. Attacker queries resolver for random.tcd.ie (non-existent), causing resolver to query tcd.ie nameserver. While waiting, attacker floods resolver with forged responses claiming to be tcd.ie nameserver, each with a different transaction ID. Birthday attack: with source port randomisation as a multiplier (65k ports × 65k TXIDs = ~4 billion values), success probability is low per second but feasible within seconds on fast link. If forged response accepted, resolver caches attacker's IP for tcd.ie → all users of that resolver redirected. DNSSEC prevention: signed records — forged response fails RRSIG validation against tcd.ie's DNSKEY. Attacker cannot forge a valid signature without the private key. DNSSEC is the cryptographic fix; source port + TXID randomisation is a temporary mitigation.",
            },
            {
                "year": 2023, "exam_slot": "Q4b", "marks": 20,
                "question_text": "Describe the email authentication system (SPF, DKIM, DMARC) and how it interacts with DNSSEC.",
                "sample_answer": "SPF (RFC 7208): TXT record listing authorised sending IP ranges for domain. Receiving MTA checks if sending IP is in SPF record. `-all` means reject if not listed. Limitation: checks envelope sender (MAIL FROM), not From: header. Breaks on forwarding. DKIM (RFC 6376): sender's mail server signs selected headers + body with private key. Public key in DNS: `selector._domainkey.domain TXT`. Receiver verifies signature. Survives forwarding. Doesn't specify failure action. DMARC (RFC 7489): `_dmarc.domain TXT v=DMARC1; p=reject; rua=...`. Policy on SPF/DKIM failure: none/quarantine/reject. Alignment: From: header domain must align with SPF/DKIM domain. Aggregate reports (rua=) for monitoring. DNSSEC interaction: SPF/DKIM/DMARC records are DNS TXT records. Without DNSSEC, attacker can poison SPF record (removing it → no policy) or replace DKIM public key. DNSSEC protects the integrity of all email authentication DNS records.",
            },
            {
                "year": 2022, "exam_slot": "Q4a", "marks": 20,
                "question_text": "Describe the DNSSEC key rollover process for both ZSK and KSK. Why are they different? What went wrong with the 2018 root KSK rollover?",
                "sample_answer": "ZSK rollover (automated, no parent needed): Pre-publish method — publish new ZSK in DNSKEY RRset, wait for TTL expiry so all caches have both keys, then sign all records with new ZSK, retire old ZSK after TTL. Double-signature: sign with both keys simultaneously during overlap. No parent involvement because DS record contains KSK hash only. KSK rollover (requires parent cooperation): publish new KSK → inform parent to add new DS record → wait for both DS records to propagate → start signing DNSKEY with new KSK → retire old KSK → request parent to remove old DS. Root KSK rollover 2018: first ever root KSK rollover in DNSSEC history. IANA ceremony with physical key custodians, air-gapped HSM, multi-party authorisation. ~750,000 resolvers had not been updated with the new trust anchor (RFC 7958 automated update failed for them). ICANN ran safety checks and delayed from 2017. Risk: those resolvers would have returned SERVFAIL for all DNSSEC-signed domains. Ultimately successful after delay.",
            },
            {
                "year": 2022, "exam_slot": "Q4b", "marks": 20,
                "question_text": "Describe the DNS amplification DDoS attack. What role does DNSSEC play? How is it mitigated?",
                "sample_answer": "DNS amplification: DNS over UDP allows small query → large response. Attacker spoofs source IP (victim's IP). Small ANY or DNSKEY query (40–60 bytes) → large DNSSEC response (3–4 KB). Amplification factor 50–100×. Attacker sends queries from millions of spoofed IPs using open resolvers → victim flooded. DNSSEC role: DNSSEC responses are significantly larger than plain DNS (includes DNSKEY, RRSIG, NSEC3 records) → worse amplification factor. Mitigations: (1) Response Rate Limiting (RRL) on authoritative servers — limits responses per IP per second. (2) BCP38 (RFC 2827) — ingress filtering prevents IP spoofing at ISP level. (3) EDNS0 Client Subnet limits response size. (4) Authoritative servers should not answer from open recursive resolvers. (5) Minimise DNSSEC response sizes where possible (smaller key types: ECDSA P-256 vs RSA-2048).",
            },
            {
                "year": 2021, "exam_slot": "Q4a", "marks": 20,
                "question_text": "Describe the NSEC and NSEC3 record types. What problem do they solve and what attacks remain possible?",
                "sample_answer": "NSEC (Next Secure): provides authenticated denial of existence. If you query for a name that doesn't exist, the resolver returns a NSEC record proving there's no name between X and Y in canonical order. Signed by ZSK. NSEC problem: zone walking — follow NSEC chain to enumerate all names in a zone. Reveals all domain names, emails, internal hostnames. NSEC3: hashes owner names using iterated SHA-1 with a salt before including in NSEC3 record. Returns the hashed range rather than actual names. Prevents zone walking — attacker can't reconstruct names from hashes. Remaining attack: offline dictionary attack — attacker guesses common names (mail, www, vpn, admin), hashes them with the known salt, and compares against NSEC3 records. Common names found in seconds on a GPU. Mitigation: opt-out NSEC3 (only sign delegated zones), high iteration count (deprecated due to DoS risk), or use NSEC3 with long random labels.",
            },
            {
                "year": 2021, "exam_slot": "Q4b", "marks": 20,
                "question_text": "Compare DoT, DoH, and ODoH for DNS privacy. What are the deployment and operational challenges of each?",
                "sample_answer": "DoT (RFC 7858, port 853): encrypts DNS with TLS. Port 853 is distinguishable — easy to block. Enterprise DNS filtering retained. Low overhead (persistent TCP connection). Supported by Android Private DNS, Unbound. DoH (RFC 8484, port 443): DNS inside HTTPS POST. Looks like web traffic — hard to block without DPI. Breaks enterprise DNS-based filtering and parental controls. Browser-native (Firefox, Chrome). Centralises DNS in large providers. ODoH (RFC 9230): proxy between client and DoH target — proxy sees IP but not query; target sees query but not IP. Neither party has full picture. Maximum privacy against resolver. Deployment: requires both proxy and resolver infrastructure (Cloudflare operates both). Operational challenges: DoT/DoH — enterprise visibility lost; need to deploy enterprise DoH resolver for policy enforcement. All: DNS privacy doesn't help if TLS SNI leaks the destination hostname (ECH addresses this). All give privacy from ISP but not from chosen resolver.",
            },
            {
                "year": 2020, "exam_slot": "Q4a", "marks": 20,
                "question_text": "Describe the original DNS protocol, its security weaknesses, and how DNSSEC addresses them.",
                "sample_answer": "DNS (RFC 1035, 1987): UDP port 53, hierarchical namespace, iterative resolution. Resolver queries root → TLD → authoritative nameserver. Responses cached by TTL. Security weaknesses: (1) No integrity — responses not signed; anyone on path can inject forged responses. (2) No authentication — no way to verify response came from authoritative server. (3) 16-bit transaction ID — easily guessable, birthday attack viable (Kaminsky 2008). (4) No privacy — queries in plaintext, visible to ISP and on-path observers. DNSSEC addresses (1) and (2): RRSIG records provide cryptographic signatures over all RRsets. DS records create a chain of trust from root to zone. Trust anchor (root KSK) in resolver software is the foundation. DNSSEC does NOT address (3) — though TXID birthday attack is less relevant once signatures are checked. DNSSEC does NOT address (4) — queries still plaintext. DNS privacy requires DoT/DoH.",
            },
            {
                "year": 2019, "exam_slot": "Q4a", "marks": 20,
                "question_text": "Describe the DNSSEC root KSK rollover process. Why was it significant and what risks were involved?",
                "sample_answer": "Root KSK rollover (October 2018): first ever change to the DNS root KSK since DNSSEC deployment. Significance: the root KSK is the trust anchor for all DNSSEC validation globally. Every validating resolver has it hard-coded or auto-updated via RFC 7958. Process: IANA key ceremony — multi-party, air-gapped HSM, physical key share custodians from around the world, live-streamed. New KSK (20326) published alongside old (19036) in root DNSKEY RRset. DS records for old and new both available during transition. Validators update trust anchor via RFC 5011 automated rollover or manual update. Risks: approximately 750,000 resolvers worldwide had not updated their trust anchor. If rollover completed with those resolvers still on old KSK, all DNSSEC-signed domains would SERVFAIL for those resolvers. ICANN ran global measurement and delayed the rollover by one year (from 2017). After delay, resolvers updated sufficiently. Rollover completed successfully on 11 October 2018.",
            },
            {
                "year": 2019, "exam_slot": "Q4b", "marks": 20,
                "question_text": "Describe how DNS is used for email security (MX records, SPF, DKIM, DMARC). What attacks do these defences protect against?",
                "sample_answer": "MX records: publish mail server hostnames for a domain. Sending server looks up MX to find delivery target. SPF: TXT record listing authorised sending IP ranges. Prevents IP-based spoofing of envelope sender. Limitation: breaks on forwarding; doesn't protect From: header. DKIM: RSA/Ed25519 signature on email headers+body. Public key in `selector._domainkey.domain` TXT. Survives forwarding. DMARC: policy for SPF/DKIM failure. `p=reject` causes receiving server to reject non-aligning emails. Alignment: From: header must match SPF/DKIM domain. Attacks protected: email spoofing (attacker sends from forged@yourdomain.com) — DMARC p=reject blocks this. Business Email Compromise — attacker pretending to be CEO/CFO. Phishing from lookalike domains partially mitigated. Remaining gap: DMARC doesn't prevent lookalike domains (tcd-ie.com vs tcd.ie) — requires monitoring and brand protection services.",
            },
            {
                "year": 2018, "exam_slot": "Q4a", "marks": 20,
                "question_text": "Describe the DNSSEC records (DNSKEY, RRSIG, DS, NSEC/NSEC3) and explain their roles in the chain of trust.",
                "sample_answer": "DNSKEY: published in zone apex. Contains public key. Two per zone: KSK (flag 257) — signs DNSKEY RRset; ZSK (flag 256) — signs all other RRsets. Algorithm field specifies crypto (13=ECDSA P-256, 8=RSA/SHA-256, 15=Ed25519). RRSIG: signature over an RRset. Fields: covered type, algorithm, labels, original TTL, expiry, inception, key tag, signer name, signature. ZSK produces RRSIG for A/MX/TXT etc; KSK produces RRSIG for DNSKEY. DS (Delegation Signer): published in parent zone. SHA-256 hash of child's KSK. Links parent's trust to child's DNSKEY. DS signed by parent's ZSK. NSEC/NSEC3: authenticated denial of existence. NSEC lists next owner name — enables zone walking. NSEC3 hashes names — prevents zone walking but vulnerable to offline dictionary attack. Chain of trust: resolver trusts root KSK (hard-coded) → root's DS for .ie → .ie DNSKEY → .ie's DS for tcd.ie → tcd.ie DNSKEY → RRSIG on target record.",
            },
            {
                "year": 2017, "exam_slot": "Q4a", "marks": 20,
                "question_text": "Describe the problem of DNS cache poisoning and the solutions available, including DNSSEC and source port randomisation.",
                "sample_answer": "DNS cache poisoning: attacker tricks recursive resolver into caching a forged DNS record, redirecting users to attacker's IP. Classic attack: predict 16-bit TXID, send forged response before legitimate one arrives. Kaminsky (2008): query random non-existent subdomain, flood forged responses. Birthday attack on TXID + UDP source port. Source port randomisation mitigation: randomise UDP source port for outgoing queries, adding ~16 bits of entropy (65k ports × 65k TXIDs ≈ 4 billion combinations). Significantly harder but not impossible. Still vulnerable to off-path attackers with fast link. DNSSEC as cryptographic fix: signed RRsets make forged responses detectable even if accepted by resolver. `SERVFAIL` if signature doesn't validate. Attacker cannot forge valid signature without private key. DNSSEC validates the response content regardless of how it arrived. Both mitigations are complementary: port randomisation reduces poisoning success rate; DNSSEC makes poisoned responses detectable.",
            },
            {
                "year": 2016, "exam_slot": "Q4a", "marks": 20,
                "question_text": "Describe the DNS resolution process and the three core security problems it has. For each problem, describe the solution.",
                "sample_answer": "DNS resolution: stub resolver → recursive resolver (ISP/8.8.8.8) → root nameservers → TLD nameservers → authoritative nameserver → answer cached by TTL and returned. Three problems: (1) No integrity / spoofing: responses not signed; attacker can inject forged records. Solution: DNSSEC — RRSIG signatures over all RRsets, chain of trust from root. (2) No authentication: no way to verify response from legitimate server. Solution: DNSSEC — DS records create authenticated delegation chain from root trust anchor. (3) No privacy: queries are plaintext UDP/TCP. ISP, employer, on-path attacker can see every hostname queried. Solution: DNS over TLS (DoT, port 853) or DNS over HTTPS (DoH, port 443) encrypts queries between stub and recursive resolver. DNSSEC does NOT solve privacy — that requires DoT/DoH.",
            },
        ],
    },
]

QUESTIONS = [
    {
        "topic_slug": "risk-analysis-process",
        "year": 2025, "exam_slot": "Q1a", "marks": 15,
        "question_text": "An Irish ISP is planning to deploy an upgraded customer support chatbot using a new LLM. Chatbot training uses ISP staff and contractors. The LLM provider's online API is required. Describe the process you would use to carry out a risk analysis for this system.",
        "sample_answer": "Identify assets (including reputation). Identify risks and vulnerabilities. Classify each risk by impact and likelihood using High/Medium/Low scores. Assign an overall priority order. Design a mitigation for the highest-ranked risk, then re-run the analysis since one mitigation may affect the probability of other risks. Iterate until effort is exhausted. Record everything throughout. For LLM systems, note that safety-checking processes are not yet well-established and external expertise should be sought.",
    },
    {
        "topic_slug": "risk-analysis-process",
        "year": 2024, "exam_slot": "Q1a", "marks": 15,
        "question_text": "A commercial Irish news organisation is planning a new election news website with a new CMS, user comments with moderation, and a paid subscription paywall. You are the employee tasked with carrying out a risk analysis. Describe the process you would use.",
        "sample_answer": "Identify assets (including reputation and subscriber data). Identify risks and vulnerabilities. Classify each risk by impact and likelihood using High/Medium/Low. Assign an overall priority order. Iteratively design mitigations for the highest-ranked risks, re-running the analysis after each mitigation. Terminate when effort is exhausted. For this scenario, seek external advice on political manipulation risks and paywall perception risks beyond internal IT knowledge.",
    },
    {
        "topic_slug": "risk-analysis-process",
        "year": 2023, "exam_slot": "Q1a", "marks": 15,
        "question_text": "The CSO are considering replacing paper-based CPI price collection with a mobile phone app on collectors' own devices. Describe the process you would use to carry out a risk analysis.",
        "sample_answer": "Identify assets (CPI data integrity, CSO reputation). Identify risks and vulnerabilities — interview CSO statistical staff (not just IT) to find statistical integrity risks. Classify by impact and likelihood. Rank risks. Design mitigations iteratively, re-running after each. For BYOD, interview collectors to establish the range of existing devices and OS versions. Terminate when effort is exhausted. Record all decisions.",
    },
    {
        "topic_slug": "classifying-risks",
        "year": 2025, "exam_slot": "Q1b", "marks": 15,
        "question_text": "Describe three significant risks affecting the ISP LLM chatbot system, including their potential impact and likelihood of occurrence, and outline countermeasures.",
        "sample_answer": "1. Customer/corporate data leaking to LLM provider via prompts (Impact: HIGH — GDPR breach; Likelihood: HIGH). Countermeasure: data minimisation, review provider DPA. 2. LLM hallucinating incorrect responses (Impact: HIGH — liability; Likelihood: MEDIUM). Countermeasure: human-in-the-loop review, AI disclosure. 3. Prompt injection attacks (Impact: HIGH — data exposure; Likelihood: MEDIUM-HIGH). Countermeasure: input sanitisation, privilege separation, red-team testing.",
    },
    {
        "topic_slug": "tls13-handshake",
        "year": 2025, "exam_slot": "Q2a", "marks": 25,
        "question_text": "For TLS 1.3, describe the key management and application data protection aspects of the protocol in detail. Describe how a library developer might test their implementation.",
        "sample_answer": "TLS 1.3 Handshake (1-RTT): ClientHello sends supported versions, cipher suites, key_share (X25519), SNI. ServerHello replies with version=1.3, cipher, key_share. Server sends EncryptedExtensions, Certificate, CertificateVerify (sig over transcript), Finished (HMAC). Client sends Finished. Key schedule: HKDF derives early_secret → handshake_secret → master_secret, producing separate client/server handshake and application traffic keys. Record layer: AEAD only (AES-128-GCM, ChaCha20-Poly1305). No MAC-then-encrypt. Forward secrecy by default. 0-RTT with PSK possible but replay risk. Testing: unit tests for crypto primitives, interop tests against BoringSSL/NSS, fuzz testing handshake state machine, tlsfuzzer, RFC 8448 test vectors.",
    },
    {
        "topic_slug": "dnssec-key-hierarchy",
        "year": 2025, "exam_slot": "Q4a", "marks": 20,
        "question_text": "Describe the DNSSEC architecture and key hierarchy in detail.",
        "sample_answer": "Chain of trust: IANA root → TLD (.ie) → zone (tcd.ie) → records. Each zone has KSK (Key Signing Key — long-lived, hash in parent DS record) and ZSK (Zone Signing Key — shorter-lived, signs RRSets). Records: DNSKEY (public keys), RRSIG (signature over RRSet), DS (parent's hash of child KSK), NSEC3 (authenticated denial of existence, hashes names to prevent zone walking). Validation: resolver starts at root trust anchor → fetches DS → validates child DNSKEY → validates RRSIGs. Root KSK rolled via multi-party ceremony (2018). Key rollover uses pre-publish or double-signature.",
    },
    {
        "topic_slug": "doh-dot-privacy",
        "year": 2025, "exam_slot": "Q4b", "marks": 20,
        "question_text": "DNSSEC does not protect DNS privacy. Describe the mechanisms that do, their trade-offs, and the privacy issues DNSSEC leaves unaddressed.",
        "sample_answer": "DNSSEC provides integrity but DNS queries remain plaintext. Privacy mechanisms: (1) DNS-over-TLS (DoT, port 853) — encrypts queries, distinguishable by port. (2) DNS-over-HTTPS (DoH, port 443) — indistinguishable from web traffic, harder to block, but centralises trust in resolver providers. (3) Oblivious DoH — proxy between client and resolver, no single party sees both client IP and query. (4) ECH (Encrypted Client Hello) — encrypts SNI in TLS ClientHello using HPKE. DNSSEC leaves unaddressed: query origin privacy, traffic analysis from query timing/volume, resolver learning browsing patterns.",
    },
]


def _rfc(num, title, note):
    return {"title": f"RFC {num} — {title}", "external_url": f"https://datatracker.ietf.org/doc/html/rfc{num}", "note": note}


TOPIC_MATERIALS = {
    # Q1 — Risk Analysis
    "risk-analysis-process": [
        {"file": "attack-surface-1-s2.0-S0950584918301514-main.pdf", "title": "Attack Surface Survey", "note": "Formalises the attack-surface concept used in risk scoping"},
        {"file": "rapid7-survey.pdf", "title": "Rapid7 Threat Survey", "note": "Attack statistics for risk prioritisation"},
        {"file": "pci_dss_v3-2.pdf", "title": "PCI-DSS v3.2", "note": "Compliance-driven process example; structured risk management"},
        _rfc(6973, "Privacy Threat Model", "Correlation, identification, secondary use, disclosure, exclusion — used directly in Q1 privacy sub-parts"),
        _rfc(7258, "Pervasive Monitoring is an Attack", "Farrell co-authored; sets tone for why privacy matters in security design"),
    ],
    "identifying-assets": [
        {"file": "attack-surface-1-s2.0-S0950584918301514-main.pdf", "title": "Attack Surface Survey", "note": "Framework for enumerating what's attackable"},
        {"file": "Greenbone_Security_Report_Unprotected_Patient_Data_a_Review.pdf", "title": "Greenbone — Unprotected Patient Data", "note": "Healthcare assets exposed — good asset-scoping case study"},
        {"file": "rapid7-survey.pdf", "title": "Rapid7 Threat Survey", "note": "Real-world asset exposure statistics"},
    ],
    "classifying-risks": [
        {"file": "rapid7-survey.pdf", "title": "Rapid7 Threat Survey", "note": "Impact/likelihood data for risk classification"},
        {"file": "pci_dss_v3-2.pdf", "title": "PCI-DSS v3.2", "note": "Structured classification methodology"},
        {"file": "attack-surface-1-s2.0-S0950584918301514-main.pdf", "title": "Attack Surface Survey", "note": "Partial-order ranking of attack surface components"},
    ],
    "mitigations": [
        {"file": "Equifax-Report.pdf", "title": "Equifax Breach Post-Mortem", "note": "Canonical Q1 case study — patch management failure as mitigation gap"},
        {"file": "stuxnet-Cyber-Reports-2017-04.pdf", "title": "Stuxnet Report", "note": "Supply-chain mitigation lessons"},
        {"file": "mirai-7132482937526820422.pdf", "title": "Mirai Botnet Analysis", "note": "Default-credential mitigation — IoT risk"},
        {"file": "BlueBorne Technical White Paper.pdf", "title": "BlueBorne (Bluetooth RCE)", "note": "OS patching velocity as mitigation strategy"},
    ],
    "privacy-threats": [
        {"file": "us-ftc-140527databrokerreport.pdf", "title": "FTC Data Broker Report", "note": "Data broker practices — RFC 6973 privacy threats in practice"},
        {"file": "trackers.1712.06850.pdf", "title": "Web Trackers Analysis", "note": "Third-party tracking threats to end users"},
        {"file": "india-censorship-1912.08590.pdf", "title": "India Censorship Study", "note": "DNS-based surveillance as privacy threat"},
        {"file": "The Perpetual Line-Up - Center on Privacy and Technology at Georgetown Law.pdf", "title": "The Perpetual Line-Up", "note": "Facial recognition privacy policy analysis"},
        _rfc(6973, "Privacy Threat Model", "Defines correlation, identification, secondary use, disclosure, exclusion — the taxonomy used in Q1c answers"),
        _rfc(8890, "The Internet is for End Users", "Farrell co-authored; philosophical grounding for privacy-first design"),
    ],
    "security-processes": [
        {"file": "pci_dss_v3-2.pdf", "title": "PCI-DSS v3.2", "note": "Structured SDLC with compliance checkpoints"},
        {"file": "linux-root-vuln.pdf", "title": "Linux Root Vulnerability Case Study", "note": "Privilege escalation — process gaps in patch management"},
        {"file": "2020-01-14-out-of-control-final-version.pdf", "title": "Out of Control (sudo vuln 2020)", "note": "sudo privilege escalation — SDLC failure"},
        {"file": "patch-1712.09665.pdf", "title": "Patch Deployment Analysis", "note": "How fast patches get applied in practice"},
    ],
    "real-incidents": [
        {"file": "Equifax-Report.pdf", "title": "Equifax Breach Post-Mortem", "note": "Patch management failure — Apache Struts CVE"},
        {"file": "w32_stuxnet_dossier.pdf", "title": "Stuxnet Dossier (Symantec)", "note": "Technical deep-dive: supply-chain + ICS targeting"},
        {"file": "mirai-7132482937526820422.pdf", "title": "Mirai Botnet Analysis", "note": "Default-credential IoT disaster"},
        {"file": "Eurograbber_White_Paper.pdf", "title": "Eurograbber Whitepaper", "note": "Mobile-banking Zeus variant"},
        {"file": "stagefright.pdf", "title": "Stagefright (Android MMS RCE)", "note": "Patching velocity failure"},
        {"file": "ai-oops-2508.06394v1.pdf", "title": "AI Security Oops (2025)", "note": "LLM/AI security failures — Q1 2025/2026 relevance"},
    ],

    # Q2 — TLS Protocols
    "tls13-handshake": [
        {"file": "tls13-awacs.pdf", "title": "TLS 1.3 AWACS Analysis", "note": "Deep formal analysis of TLS 1.3 design — primary reference"},
        {"file": "google_infrastructure_whitepaper_fa.pdf", "title": "Google Infrastructure Whitepaper", "note": "ALTS: large-scale authenticated transport for context"},
        {"file": "ssl_jun21.pdf", "title": "SSL/TLS June 2021 Overview", "note": "TLS ecosystem snapshot and deployment stats"},
        _rfc(8446, "TLS 1.3", "THE spec — read Appendices C, D, E; 160 pages but essential for Q2"),
        _rfc(7301, "ALPN — Application Layer Protocol Negotiation", "How TLS clients/servers agree on h2/h3/http1.1 within handshake"),
    ],
    "tls13-key-schedule": [
        {"file": "tls13-awacs.pdf", "title": "TLS 1.3 AWACS Analysis", "note": "HKDF key schedule derivation analysis"},
        {"file": "djb.pdf", "title": "DJB — Curve25519", "note": "X25519 rationale — default key exchange in TLS 1.3"},
        {"file": "gcm.pdf", "title": "GCM (AEAD) Paper", "note": "AES-GCM reference — the AEAD used after key schedule"},
        _rfc(5869, "HKDF — HMAC-based Key Derivation Function", "Defines HKDF-Extract and HKDF-Expand used throughout TLS 1.3 key schedule"),
        _rfc(2104, "HMAC", "MAC construction underlying HKDF; collision resistance proof"),
    ],
    "tls13-record-layer": [
        {"file": "gcm.pdf", "title": "GCM (AEAD) Paper", "note": "AES-GCM reference — why AEAD is correct"},
        {"file": "AE_comparison_ipics04.pdf", "title": "AE Modes Comparison", "note": "MAC-then-encrypt vs encrypt-then-MAC — why TLS 1.3 is right"},
        {"file": "TLStiming.pdf", "title": "TLS Timing Attacks", "note": "Lucky13 — CBC padding oracle that AEAD eliminates"},
        _rfc(5116, "AEAD Interface", "Defines the abstract interface for AEADs; 16-octet tag standard used in TLS 1.3"),
        _rfc(8446, "TLS 1.3", "Record layer section — max 2^14 octet records, fake version headers for middlebox compat"),
    ],
    "forward-secrecy": [
        {"file": "imperfect-forward-secrecy-ccs15.pdf", "title": "Logjam / Imperfect Forward Secrecy", "note": "Export-grade DH downgrade — breaks forward secrecy"},
        {"file": "bleichenbacher-pkcs.pdf", "title": "Bleichenbacher PKCS#1 v1.5", "note": "Original padding oracle — RSA key-exchange attack"},
        {"file": "robot-1189.pdf", "title": "ROBOT Attack (2017)", "note": "Bleichenbacher returns — why static RSA key exchange is dead"},
        _rfc(3218, "Preventing the Million Message Attack (Bleichenbacher)", "Documents why PKCS#1 v1.5 RSA must never be used for key transport"),
        _rfc(8017, "PKCS#1 v2.2 / RSA-OAEP", "OAEP padding — the correct RSA encryption padding that avoids Bleichenbacher"),
    ],
    "tls-attacks": [
        {"file": "robot-1189.pdf", "title": "ROBOT Attack", "note": "Bleichenbacher oracle in F5/Citrix"},
        {"file": "Drown_Attack.pdf", "title": "DROWN Attack", "note": "SSLv2 cross-protocol oracle"},
        {"file": "TLStiming.pdf", "title": "TLS Timing Attacks", "note": "Lucky13 / CBC timing side-channel"},
        {"file": "Armis-TLStorm.pdf", "title": "Armis TLStorm (2022)", "note": "APC UPS TLS parser bugs — named attack"},
        {"file": "tls-mitm-boxes.pdf", "title": "TLS MITM Boxes", "note": "Corporate SSL inspection breaking security"},
        {"file": "DualECTLS.pdf", "title": "Dual-EC in TLS", "note": "Backdoored PRNG in Juniper — nation-state attack"},
        _rfc(7457, "Summary of Known TLS/DTLS Attacks", "Comprehensive attack catalogue up to 2015 — good Q2 revision list"),
        _rfc(5746, "TLS Renegotiation Indication Extension", "Fix for the 2009 renegotiation protocol flaw — backward incompatible"),
        _rfc(6520, "TLS/DTLS Heartbeat Extension", "The spec that contained Heartbleed — good example of implementation flaw"),
        _rfc(6101, "SSL 3.0 (Historical)", "SSLv2/3 that DROWN exploits; basis for understanding cross-protocol attacks"),
    ],
    "tls-dos": [
        {"file": "Armis-TLStorm.pdf", "title": "Armis TLStorm (2022)", "note": "TLS parser crash → DoS in embedded devices"},
        {"file": "TLStiming.pdf", "title": "TLS Timing Attacks", "note": "Computational DoS via timing side-channels"},
        {"file": "non-browser-ssl-shmat_ccs12.pdf", "title": "Non-Browser SSL is Broken", "note": "Accept-all-certs leaves apps open to MITM/DoS"},
        _rfc(8446, "TLS 1.3 — Anti-DoS Mechanisms", "Cookie extension for DTLS DoS; HelloRetryRequest flow"),
    ],
    "pqc-tls": [
        {"file": "2204.10920.pdf", "title": "PQC in TLS / Migration", "note": "Hybrid KEM (X25519+Kyber) in TLS — primary reference"},
        {"file": "2001.07421.pdf", "title": "PQC Survey / Transition Context", "note": "Overview of post-quantum migration landscape"},
        {"file": "mls-study.pdf", "title": "MLS (Messaging Layer Security)", "note": "HPKE as building block — PQC in group messaging"},
        {"file": "e2ee-2022-449.pdf", "title": "E2EE Design 2022", "note": "PQC-safe E2EE architecture"},
        _rfc(9180, "HPKE — Hybrid Public Key Encryption", "Used in TLS ECH and MLS; defines KEM+KDF+AEAD composition"),
        _rfc(8391, "XMSS — Stateful Hash-Based Signatures", "Quantum-resistant signatures; limited uses (2^10–2^20)"),
        _rfc(8554, "LMS — Leighton-Micali Signatures", "Second stateful hash-based sig scheme; same caveats as XMSS"),
    ],
    "large-scale-tls": [
        {"file": "crlite_oakland17.pdf", "title": "CRLite — Web PKI Revocation at Scale", "note": "Bloom-filter revocation — scalable certificate status"},
        {"file": "interception-ndss17.pdf", "title": "TLS Interception (NDSS 2017)", "note": "Measuring corporate MITM at scale"},
        {"file": "ssl_jun21.pdf", "title": "SSL/TLS June 2021 Overview", "note": "CA trust, OCSP, Let's Encrypt deployment stats"},
        {"file": "kohnfelder-07113748-MIT.pdf", "title": "Kohnfelder 1978 — PKI Certificates", "note": "Origin of the public key certificate concept"},
        _rfc(5280, "X.509 PKI and Certificate Profile", "WebPKI uses this; defines certificate structure, CRLs, path validation"),
        _rfc(6962, "Certificate Transparency (CT)", "Append-only logs of all issued certs — detects rogue CA issuance"),
        _rfc(8555, "ACME — Automatic Certificate Management", "Let's Encrypt protocol; DV cert issuance automation"),
        _rfc(6797, "HSTS — HTTP Strict Transport Security", "Prevents protocol downgrade; first connection still vulnerable"),
        _rfc(7469, "Public Key Pinning (HPKP)", "Deprecated cert pinning — too easy to lock yourself out; use CT instead"),
        _rfc(8659, "DNS CAA Resource Record", "CA can only issue cert if listed in CAA RR; partial fix for CA screw-ups"),
    ],

    # Q3 — System Design
    "security-requirements": [
        {"file": "attack-surface-1-s2.0-S0950584918301514-main.pdf", "title": "Attack Surface Survey", "note": "Formalising security requirements from attack surface"},
        {"file": "pci_dss_v3-2.pdf", "title": "PCI-DSS v3.2", "note": "Compliance as structured security requirements"},
        {"file": "Greenbone_Security_Report_Unprotected_Patient_Data_a_Review.pdf", "title": "Greenbone — Unprotected Patient Data", "note": "What requirements were missing in exposed systems"},
        _rfc(6973, "Privacy Threat Model", "Use this taxonomy when writing privacy requirements for Q3"),
    ],
    "architecture-patterns": [
        {"file": "google_infrastructure_whitepaper_fa.pdf", "title": "Google Infrastructure Whitepaper", "note": "Large-scale secure architecture — BeyondCorp / ALTS"},
        {"file": "raluca-cryptdb.pdf", "title": "CryptDB — Encrypted Databases", "note": "Encrypt-at-rest architecture pattern"},
        {"file": "websso-final.pdf", "title": "Web SSO Security Analysis", "note": "OAuth/SSO architecture patterns and vulnerabilities"},
        _rfc(5280, "X.509 PKI and Certificate Profile", "Foundation for any architecture involving TLS or certificate-based auth"),
        _rfc(6962, "Certificate Transparency", "Append-only audit log architecture pattern — relevant to Q3 audit requirements"),
        _rfc(8555, "ACME", "Automated cert lifecycle — zero-touch certificate management pattern"),
    ],
    "authn-authz": [
        {"file": "2012-jbonneau-phd_thesis.pdf", "title": "Bonneau PhD — Passwords", "note": "Statistics and entropy framing for auth design"},
        {"file": "WP_Consumer_Password_Worst_Practices.pdf", "title": "Consumer Password Worst Practices", "note": "Auth failure anecdotes for Q3 design discussion"},
        {"file": "johnny-fired.pdf", "title": "Why Johnny Was Fired (Usability)", "note": "Usability / auth failure — design implications"},
        {"file": "coniks-1004.pdf", "title": "CONIKS — Key Transparency", "note": "Auditable key directories for auth systems"},
        {"file": "WhatsAppEncryption.pdf", "title": "WhatsApp Encryption", "note": "Signal / Double-Ratchet — E2EE auth in practice"},
        _rfc(9106, "Argon2 Password Hashing", "PHC winner; memory-hard, time-memory-tradeoff-resistant — use for password storage"),
        _rfc(8018, "PBKDF2 (Password-Based Key Derivation)", "Older but widely deployed; bcrypt/scrypt/Argon2 all better for passwords"),
        _rfc(4120, "Kerberos v5", "Ticket-based SSO; used in Windows Active Directory; know the TGT/service-ticket flow"),
    ],
    "crypto-in-systems": [
        {"file": "gcm.pdf", "title": "GCM (AEAD) Paper", "note": "Choosing the right AEAD for system crypto"},
        {"file": "djb.pdf", "title": "DJB — Curve25519", "note": "Why X25519/Ed25519 are the right choices"},
        {"file": "lightweight-crypto-survey.pdf", "title": "Lightweight Crypto Survey", "note": "IoT / HSM crypto selection"},
        {"file": "raluca-cryptdb.pdf", "title": "CryptDB", "note": "Key rotation + encrypted DB architecture"},
        _rfc(7539, "ChaCha20-Poly1305", "DJB's stream cipher + MAC AEAD — preferred when no AES-NI hardware"),
        _rfc(5116, "AEAD Interface", "Abstract AEAD interface; 16-byte tag minimum; use this as the design boundary"),
        _rfc(8032, "EdDSA — Ed25519 and Ed448", "Deterministic signatures; safer than ECDSA (no nonce reuse risk)"),
        _rfc(7638, "JSON Web Key (Curve Definitions)", "X25519 and P-256 key representations"),
        _rfc(9180, "HPKE", "Encrypt-to-public-key with formal analysis; use instead of ad-hoc ECIES"),
    ],
    "audit-logging": [
        {"file": "patch-1712.09665.pdf", "title": "Patch Deployment Analysis", "note": "Audit trails enabling patch velocity measurement"},
        {"file": "pci_dss_v3-2.pdf", "title": "PCI-DSS v3.2", "note": "Logging requirements from compliance perspective"},
        _rfc(6962, "Certificate Transparency", "Append-only, Merkle-tree-backed log — architectural model for tamper-evident audit logs"),
    ],
    "attack-the-system": [
        {"file": "w32_stuxnet_dossier.pdf", "title": "Stuxnet Dossier", "note": "Supply-chain attack anatomy — attacker mindset"},
        {"file": "nsa-buying-fe33e1ba-full.pdf", "title": "NSA Buying Capabilities", "note": "Nation-state offensive capability procurement"},
        {"file": "The_Bvp47_a_top-tier_backdoor_of_us_nsa_equation_group.en.pdf", "title": "BVP47 — NSA Equation Group Backdoor", "note": "Nation-state implant reverse engineered"},
        {"file": "Eurograbber_White_Paper.pdf", "title": "Eurograbber", "note": "Targeted financial attack: insider + mobile compromise"},
        {"file": "fake-twitter-russians-17.001.02.pdf", "title": "Fake Twitter — Russian Influence Ops", "note": "Disinformation as system attack vector"},
    ],

    # Q4 — DNS & DNSSEC
    "dns-basics": [
        {"file": "June3_DNSSEC.pdf", "title": "June3 DNSSEC Lecture", "note": "Primary reference — comprehensive DNS + DNSSEC overview"},
        {"file": "dnspolicy-10.1002@poi3.195.pdf", "title": "DNS Policy (ICANN)", "note": "Governance and policy context for DNS architecture"},
        {"file": "dontlookup_ccs25_fullpaper.pdf", "title": "Don't Look Up (CCS 2025)", "note": "Recent DNS attack research — Q4 answer colour"},
        _rfc(9460, "SVCB and HTTPS Resource Records", "New RR types for TLS connection params; saves RTTs; HTTPS RR replaces A+TLS handshake"),
    ],
    "dnssec-records": [
        {"file": "June3_DNSSEC.pdf", "title": "June3 DNSSEC Lecture", "note": "DNSKEY, RRSIG, DS, NSEC3 record types explained"},
        _rfc(4033, "DNSSEC Introduction and Requirements", "Overview of the DNSSEC system — read this first"),
        _rfc(4034, "Resource Records for DNSSEC", "Defines DNSKEY, RRSIG, NSEC, DS record formats"),
        _rfc(4035, "Protocol Modifications for DNSSEC", "How resolvers validate; DO bit; AD flag"),
    ],
    "dnssec-key-hierarchy": [
        {"file": "June3_DNSSEC.pdf", "title": "June3 DNSSEC Lecture", "note": "KSK/ZSK separation, chain of trust, DS at parent"},
        _rfc(8078, "Managing DS Records from Child via CDS/CDNSKEY", "Automates DS publication at parent — helps with KSK rotation which is why DNSSEC deployment is hard"),
        _rfc(6979, "Deterministic ECDSA", "Prevents nonce reuse that would expose DNSSEC signing keys"),
    ],
    "dnssec-validation": [
        {"file": "June3_DNSSEC.pdf", "title": "June3 DNSSEC Lecture", "note": "Validation flow, trust anchors, NSEC denial-of-existence"},
        {"file": "dontlookup_ccs25_fullpaper.pdf", "title": "Don't Look Up (CCS 2025)", "note": "Attacks on validation — adds nuance to Q4a"},
        _rfc(4035, "DNSSEC Protocol Modifications", "Validation algorithm, trust anchor management, AD flag semantics"),
        _rfc(4034, "DNSSEC Resource Records", "NSEC and NSEC3 for authenticated denial-of-existence"),
    ],
    "doh-dot-privacy": [
        {"file": "india-censorship-1912.08590.pdf", "title": "India Censorship Study", "note": "DNS poisoning / SNI blocking at national scale"},
        {"file": "outages_censorship.pdf", "title": "Internet Outages & Censorship", "note": "BGP hijack + DNS shutdown measurement"},
        {"file": "robust-website-fingerprinting.pdf", "title": "Robust Website Fingerprinting", "note": "Traffic analysis even with DoH — displacement problem"},
        {"file": "dnspolicy-10.1002@poi3.195.pdf", "title": "DNS Policy (ICANN)", "note": "Policy implications of DoH centralisation"},
        _rfc(7858, "DNS over TLS (DoT)", "Port 853; encrypts DNS between stub and recursive; distinguishable by port"),
        _rfc(8484, "DNS over HTTPS (DoH)", "Port 443; indistinguishable from web traffic; centralises trust in browser's TRR"),
        _rfc(7830, "EDNS(0) Padding Option", "Adds padding to DNS messages to prevent length-based leakage"),
        _rfc(8467, "Padding Policies for DNS over TLS", "Queries: pad to N×128 octets; responses: N×468 octets"),
        _rfc(9076, "DNS Privacy Considerations", "Documents what DNS reveals: qname, IP, timing — all identifying"),
        _rfc(9156, "QNAME Minimisation", "Send only necessary labels to each authoritative — reduces privacy exposure"),
        _rfc(9539, "Opportunistic ADoT (Authoritative DNS over TLS)", "Recursive-to-authoritative encryption without authentication"),
    ],
    "email-security": [
        {"file": "June3_DNSSEC.pdf", "title": "June3 DNSSEC Lecture", "note": "DKIM/SPF/DMARC rely on DNS — lecture covers overlap"},
        {"file": "efail-attack-paper.pdf", "title": "EFAIL (PGP/S-MIME oracle)", "note": "Email E2EE vulnerability — what DMARC doesn't protect"},
        {"file": "coniks-1004.pdf", "title": "CONIKS — Key Transparency", "note": "Auditable key directories for email identity"},
        _rfc(6376, "DKIM — DomainKeys Identified Mail", "Signs email headers+body with sender domain's private key; public key in DNS TXT"),
        _rfc(7208, "SPF — Sender Policy Framework", "DNS TXT lists authorised sending IPs for a domain; prevents envelope-from spoofing"),
        _rfc(7489, "DMARC — Domain-based Message Authentication", "Policy over DKIM+SPF; p=reject/quarantine; RUA reporting"),
        _rfc(8617, "ARC — Authenticated Received Chain", "Preserves DKIM/SPF authentication info through forwarding/mailing lists"),
        _rfc(8461, "MTA-STS — Mail Transfer Agent Strict Transport Security", "Forces TLS for inbound SMTP delivery; analogous to HSTS for email"),
        _rfc(9580, "OpenPGP (new)", "Updated OpenPGP standard — web-of-trust model, not X.509 hierarchy"),
    ],
}


def seed(db=None):
    own_session = db is None
    if own_session:
        db = SessionLocal()
    try:
        if db.query(Path).count() > 0:
            print("Already seeded, skipping.")
            return

        slug_to_topic_id: dict[str, int] = {}

        # Load real exam questions from parsed PDF text files
        parsed_exam_qs: dict[str, list] = {}
        for eq in _parse_exam_questions():
            parsed_exam_qs.setdefault(eq["path_slug"], []).append(eq)

        for path_data in PATHS:
            path = Path(
                slug=path_data["slug"],
                title=path_data["title"],
                description=path_data["description"],
                exam_slot=path_data["exam_slot"],
                overview=path_data.get("overview"),
            )
            db.add(path)
            db.flush()

            for t in path_data["topics"]:
                topic = Topic(
                    slug=t["slug"],
                    title=t["title"],
                    order=t["order"],
                    depends_on=t["depends_on"],
                    path_id=path.id,
                )
                db.add(topic)
                db.flush()
                slug_to_topic_id[t["slug"]] = topic.id

                note_path = f"app/data/docs/{t['slug']}.md"
                if os.path.exists(note_path):
                    with open(note_path) as f:
                        content = f.read()
                    db.add(Note(topic_id=topic.id, content=content, is_prebuilt=True))

                for idx, m in enumerate(TOPIC_MATERIALS.get(t["slug"], [])):
                    db.add(TopicMaterial(
                        topic_id=topic.id,
                        title=m["title"],
                        file=m.get("file"),
                        external_url=m.get("external_url"),
                        note=m.get("note"),
                        order=idx,
                    ))

            for eq in parsed_exam_qs.get(path_data["slug"], []):
                db.add(ExamQuestion(
                    path_id=path.id,
                    year=eq["year"],
                    exam_slot=eq["exam_slot"],
                    marks=eq["marks"],
                    question_text=eq["question_text"],
                    sample_answer=eq["sample_answer"],
                ))

        for q in QUESTIONS:
            topic_id = slug_to_topic_id.get(q["topic_slug"])
            if topic_id:
                db.add(Question(
                    topic_id=topic_id,
                    year=q["year"],
                    exam_slot=q["exam_slot"],
                    marks=q["marks"],
                    question_text=q["question_text"],
                    sample_answer=q["sample_answer"],
                ))

        db.commit()
        print("Seeded successfully.")
    finally:
        if own_session:
            db.close()


if __name__ == "__main__":
    from app.database import engine, Base
    import app.models  # noqa: register models
    Base.metadata.create_all(bind=engine)
    seed()
