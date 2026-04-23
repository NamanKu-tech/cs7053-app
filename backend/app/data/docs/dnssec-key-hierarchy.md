<!-- MODE:EASY -->
# DNSSEC Key Hierarchy — Simple Version

DNSSEC uses two types of keys in every zone, and the zones form a chain from the top of the internet all the way down to individual websites. Understanding this hierarchy is worth big marks in Q4.

**Why two keys per zone?**

Imagine you're a bank. You have a master vault key (very important, kept very safe, rarely used) and daily till keys (used constantly, rotated often).

- **KSK (Key Signing Key)** = master vault key. Important, rarely changed, stored offline in a ceremony. Its fingerprint (DS record) is published by the parent zone.
- **ZSK (Zone Signing Key)** = daily till key. Used to sign all the zone's DNS records. Changed frequently (every few months). If it's compromised, damage is limited.

Why separate? If you used one key for everything and it was compromised, you'd have to redo the whole chain of trust. With two keys, you can rotate the ZSK cheaply without touching the KSK.

**The hierarchy (top to bottom):**

```
Internet Root (IANA/ICANN)
    ↓  DS record
.ie TLD
    ↓  DS record
tcd.ie zone
    ↓  DS record
cs.tcd.ie zone
    ↓  RRSIG on actual record
cs7053.cs.tcd.ie  A  1.2.3.4
```

Each arrow represents: parent publishes DS record (fingerprint of child's KSK), child publishes DNSKEY and RRSIG records.

The root's public key (called the *trust anchor*) is hard-coded into DNS resolver software. That's the foundation everything else rests on.

<!-- MODE:TECHNICAL -->
# DNSSEC Key Hierarchy (KSK/ZSK, Chain of Trust)

## Two-Key Architecture per Zone

### KSK (Key Signing Key)
- Flags: `257` in DNSKEY record
- Signs: DNSKEY RRset only
- Published: its SHA-256 hash is the DS record in the parent zone
- Lifetime: long (1–5 years typical); rollover via elaborate ceremony
- Storage: often offline (HSM + physical ceremony); never online

### ZSK (Zone Signing Key)
- Flags: `256` in DNSKEY record
- Signs: all other RRsets in the zone (A, MX, CNAME, SOA, etc.)
- Lifetime: short (1–3 months typical); automated rollover
- Compromise impact: limited to that zone; rollover straightforward

**Why two keys?** ZSK rotates frequently — keeping KSK offline and stable means parent zone's DS record rarely changes (updating DS requires parent cooperation). ZSK compromise requires only zone-level rollover, not parent involvement.

## Chain of Trust Structure

```
Root zone
  DNSKEY: root KSK (trust anchor — hard-coded in resolvers, RFC 7958)
  DNSKEY: root ZSK
  RRSIG(DNSKEY) ← signed by root KSK
  DS(tld) ← hash of TLD's KSK, signed by root ZSK
        ↓
TLD zone (.ie, .com)
  DNSKEY: TLD KSK
  DNSKEY: TLD ZSK
  RRSIG(DNSKEY) ← signed by TLD KSK
  DS(child) ← hash of child KSK, signed by TLD ZSK
        ↓
Zone (tcd.ie)
  DNSKEY: zone KSK
  DNSKEY: zone ZSK
  RRSIG(DNSKEY) ← signed by zone KSK
  A/MX/TXT records
  RRSIG(A) ← signed by zone ZSK
```

## Root KSK Rollover (2018)

First root KSK rollover in DNSSEC history. IANA ceremony on 11 October 2018 (delayed from 2017). Multi-party ceremony with physical key custodians, air-gapped HSM, live-streamed. ~750,000 resolvers were not updated with new trust anchor → would have lost DNS resolution. ICANN ran safety checks and delayed once. Ultimately successful.

Teaches: **root KSK is single point of failure for global DNSSEC.** Key ceremony is the operational cost of this architecture.

## Key Rollover Methods

**ZSK rollover (automated):**
- Pre-publish method: publish new ZSK in DNSKEY RRset; wait for TTL expiry; start signing with new ZSK; retire old
- Double-signature method: sign with both old and new ZSK simultaneously for overlap period

**KSK rollover (requires parent cooperation):**
- Publish new KSK → inform parent to publish new DS → wait for both DS records in parent → start signing DNSKEY with new KSK → retire old → inform parent to remove old DS

## Validation Algorithm (resolver side)

1. Fetch target zone's DNSKEY records
2. Verify RRSIG on DNSKEY using KSK
3. Verify KSK against DS record from parent zone (fetched in previous step)
4. Verify parent's DS record RRSIG using parent's ZSK
5. Chain upward until root trust anchor
6. Verify target record's RRSIG using zone's ZSK

<!-- MODE:HINGLISH -->
# DNSSEC Key Hierarchy — Hinglish mein

## Q4 ka core answer yahi hai

Yeh question almost har saal aata hai — verbatim: "Describe the DNSSEC architecture and key management hierarchy."

## Two keys per zone kyun?

**KSK (Key Signing Key):** Bahut important. Rarely change hoti hai (1-5 saal). Offline stored (HSM + physical ceremony). Sirf DNSKEY RRset sign karti hai. Parent zone mein iska hash DS record ke roop mein hota hai.

**ZSK (Zone Signing Key):** Frequently change hoti hai (1-3 mahine). Saare actual records sign karti hai (A, MX, TXT, etc.). Agar compromise ho toh sirf zone-level rollover chahiye, parent ka involvement nahi.

**Logic:** Agar ek hi key hoti aur compromise hoti, poori chain update karni padti. Alag keys se ZSK cheaply rotate hoti hai bina parent ko involve kiye.

## Chain of trust — yaad karo diagram

```
Root (IANA)
  KSK → trust anchor (resolvers mein hard-coded)
  ZSK → DS records sign karta hai TLDs ke liye
    ↓
TLD (.ie)
  KSK → parent (root) ka DS record isme
  ZSK → child zones ke DS records sign karta hai
    ↓
Zone (tcd.ie)
  KSK → parent (.ie) ka DS record isme
  ZSK → A, MX, TXT records sign karta hai
    ↓
Actual DNS record
  RRSIG (ZSK ne sign kiya)
```

## Root KSK Rollover (2018)

Pehli baar root KSK change hua DNSSEC history mein. Physical ceremony, multiple custodians, air-gapped HSM. ~750,000 resolvers update nahi huye the — unhe DNS resolution lose ho jaata. ICANN ne delay kiya, finally successful raha. Teach: root KSK single point of failure hai global DNSSEC ke liye.

## Exam ke liye exact sentences

"Har zone mein do keys hote hain: KSK jo sirf DNSKEY RRset sign karta hai aur jiska hash parent ke DS record mein hota hai; aur ZSK jo baaki sab records sign karta hai aur frequently rotate hota hai. Chain of trust root ke hard-coded trust anchor se shuru hoti hai aur DS → DNSKEY → RRSIG ke zariye TLD → zone → record tak jaati hai."
