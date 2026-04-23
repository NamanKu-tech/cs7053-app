<!-- MODE:EASY -->
# Real Incidents — Simple Version

These are three real-world security disasters you must know for the exam. Farrell expects you to name them and explain why they happened.

**Equifax (2017) — "They forgot to update the software"**

Equifax is a company that holds credit records for hundreds of millions of people. Hackers found a known weakness in software called Apache Struts. The fix had been available for 2 months, but Equifax hadn't applied it. Hackers got in and stole 147 million people's data.

Lesson: *Patch your software. Check your dependencies for known bugs. Have a process.*

**Stuxnet (discovered 2010) — "A virus that physically broke machines"**

Stuxnet was a computer virus (almost certainly made by the USA and Israel) that targeted Iran's nuclear centrifuges. The clever part: it spread via USB drives, went through Windows computers, and when it found a specific type of industrial controller, it made the centrifuges spin too fast and break — while showing the operators fake "everything is fine" readings.

Lesson: *Air-gapped (offline) systems aren't fully safe. Supply chains can be attacked. Physical infrastructure can be harmed via software.*

**Mirai (2016) — "Millions of baby cameras broke the internet"**

Mirai was malware that scanned the internet for routers, cameras, and other small devices that still had their factory-default passwords (like "admin/admin"). It infected hundreds of thousands of devices and used them all to flood a company called Dyn with traffic — which took down Twitter, Netflix, Reddit, and others for hours.

Lesson: *Default credentials are a critical vulnerability. IoT devices need proper security. One botnet can take down major infrastructure.*

<!-- MODE:TECHNICAL -->
# Real Incidents (Equifax, Stuxnet, Mirai)

## Equifax (2017)

**Vulnerability:** Apache Struts CVE-2017-5638 (remote code execution via Content-Type header). Published March 2017.

**Breach:** May–July 2017. Exploited for 78 days before detection.

**Impact:** 147.9 million US consumers' PII (SSN, DOB, addresses, driver's licence, credit cards). £500k ICO fine (UK); ~$575M FTC settlement (US).

**Process failure:** Dependency scanning absent from CI/CD pipeline. Patch management process did not have mandatory timelines. Certificate expired on intrusion detection system — monitoring was blind.

**Exam use:** "Process failure, not technical novelty. A dependency scan in CI would have detected the CVE within hours of publication."

## Stuxnet (discovered June 2010)

**Attribution:** Almost certainly NSA + Unit 8200 (Israel) — "Olympic Games" operation.

**Target:** Natanz uranium enrichment facility, Iran. Targeted Siemens S7-315 and S7-417 PLCs controlling IR-1 centrifuges.

**Mechanism:** Four zero-days (unprecedented). Spread via USB (LNK exploit). Checked for specific Siemens STEP 7 software. Issued malicious commands to centrifuges (overspeed/understress cycles) while sending falsified sensor readings to operators.

**Impact:** ~1,000 centrifuges destroyed. 5-year setback estimated.

**Key facts:** First known malware to cause physical destruction. First known nation-state cyberweapon used in active conflict. Demonstrated air-gap bypass via USB supply chain.

**Exam use:** "Supply-chain attack bypassing air-gap; demonstrates that ICS/SCADA systems face nation-state-level threats requiring physical isolation plus software integrity."

## Mirai (September 2016)

**Author:** Three US college students (ultimately pleaded guilty). Source code released publicly — spawned many variants.

**Mechanism:** Scanned IPv4 space for telnet (port 23/2323). Tried 61 default username/password combinations (admin/admin, root/1234, etc.). Infected devices silently joined botnet. C2 issued DDoS commands.

**Attack:** 21 October 2016. Dyn DNS provider (managed DNS for Twitter, Netflix, Reddit, GitHub, PayPal) hit with ~1.2 Tbps UDP flood. Major outage across US east coast for ~11 hours.

**Scale:** ~600,000 infected IoT devices (cameras, DVRs, routers — mostly by Dahua, XiongMai).

**Exam use:** "Default credentials on IoT devices enabled ~600k-device botnet. Countermeasure: mandatory unique per-device credentials at manufacture; network segmentation; rate-limiting DNS responses."

## Bonus: XZ Backdoor (2024)

Social-engineering over 2 years; attacker "Jia Tan" gained commit access to XZ Utils (compression library). Inserted backdoor that activated specifically in systemd-linked OpenSSH on systemd-using Linux distros. Caught accidentally by Andres Freund noticing 500ms SSH slowness. CVSS 10.0. Narrowly avoided catastrophic compromise of SSH infrastructure globally.

**Exam use:** "Supply-chain via long-con social engineering. SBOM + signed dependency releases + code review of third-party commits would reduce exposure."

<!-- MODE:HINGLISH -->
# Real Incidents — Hinglish mein

Yeh teen incidents Farrell ke favourite examples hain. Inhe naam se jaano aur ek line mein explain karna aana chahiye.

## Equifax (2017) — "Patch nahi kiya toh 147 million log suffer kiye"

Apache Struts mein ek bug aaya March 2017 mein. Fix available tha. Equifax ne 2 mahine tak update nahi kiya. Hackers ghus gaye, 147 million Americans ka data chura liya — Social Security numbers, dates of birth, credit card numbers sab.

**Root cause:** Process failure. CI mein dependency scan nahi tha. Patch management ka koi timeline nahi tha. Upar se intrusion detection ka certificate expire tha — monitoring kaafi time se kaam nahi kar rahi thi.

**Exam line:** "Equifax breach process failure thi — Apache Struts CVE 2 mahine tak unpatched raha. Dependency scanning in CI is se roke rakhta."

## Stuxnet (2010) — "USB se nuclear plant todh diya"

US aur Israel ne milke ek wirus banaya jo Iran ke nuclear centrifuges ko physically damage kare. Wirus USB drive se phela (internet se connected nahi the machines fir bhi). Centrifuges ko galat speed pe chalaya jabki operators ko fake "sab theek hai" readings dikhata raha. ~1000 centrifuges barbad.

**Key point:** Air-gap (no internet) bhi safe nahi tha. Supply chain (USB) se ghusa. First time software ne physical damage kiya.

**Exam line:** "Stuxnet ne dikhaya ki ICS systems nation-state attacks se safe nahi hain chahe air-gapped hon. Supply chain integrity critical hai."

## Mirai (2016) — "Baby cameras ne Twitter tod diya"

Teen college students ne ek botnet banaya. Unka kaam? Internet scan karo, devices dhundho jo abhi bhi default passwords use kar rahe hain (admin/admin, root/1234). 600,000 devices infect kiye — cameras, routers, DVRs. Sab milke Dyn DNS company par attack kiya. Twitter, Netflix, Reddit ghanton ke liye band ho gaye.

**Root cause:** IoT devices factory default credentials ke saath ship kiye jaate the. Koi bhi change nahi karta.

**Exam line:** "Mirai ne default IoT credentials ka danger dikhaaya. Fix: manufacture time par unique per-device passwords mandatory karo."

## Bonus yaad rakho: XZ Backdoor (2024)

Ek attacker ne 2 saal mein slowly open-source project ka trust gain kiya aur SSH infrastructure mein backdoor daala. Ek engineer ne accidentally pakad liya. Agar nahi pakda jaata toh poori Linux SSH security compromise ho jaati.

**Exam line:** "Long-con supply chain attack. SBOM aur signed releases is tarah ke attacks detect karne mein help karte."
