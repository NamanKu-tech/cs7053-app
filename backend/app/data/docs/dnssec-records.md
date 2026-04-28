<!-- MODE:EASY -->
# DNSSEC Records — Simple Version

DNSSEC adds digital signatures to DNS. Each DNS answer comes with a signature proving it's genuine and hasn't been tampered with.

To do this, DNSSEC introduces four new record types. Think of them as the paperwork that makes the signature system work.

**DNSKEY** — "Here are my public keys"
This is where a zone publishes the public keys it uses to sign things. Like a notary publishing their official seal so you can verify their stamps.

**RRSIG** — "Here is my signature on this answer"
Every DNS record that's signed has an RRSIG record alongside it. This is the actual digital signature. Your DNS resolver checks this signature against the DNSKEY to verify the answer is genuine.

**DS (Delegation Signer)** — "I trust this child zone's key"
When a parent zone (like .ie) vouches for a child zone (like tcd.ie), it publishes a DS record — a fingerprint of the child's public key. This is what creates the chain of trust from the root down to individual domains.

**NSEC / NSEC3** — "This name definitely doesn't exist"
In original DNS, if you ask for a name that doesn't exist, you just get "NXDOMAIN." An attacker could fake that response. NSEC/NSEC3 provides a signed proof of non-existence so you can't fake "this domain doesn't exist."

NSEC3 is the newer version that hashes the names, so you can't list all domains in a zone by walking through NSEC records (zone walking). Though it's still vulnerable to offline dictionary attacks.

<!-- MODE:TECHNICAL -->
# DNSSEC Records (DNSKEY, RRSIG, DS, NSEC3)

## The Four Record Types

### DNSKEY
Published in the zone itself. Contains the public key used to verify signatures.

```
tcd.ie. 3600 IN DNSKEY 257 3 13 [base64_public_key]
```

Flags field:
- `256` = ZSK (Zone Signing Key) — signs zone records
- `257` = KSK (Key Signing Key) — signs DNSKEY RRset; hash in parent DS record

Algorithm field: 13 = ECDSA P-256 with SHA-256 (recommended); 8 = RSA/SHA-256; 15 = Ed25519.

### RRSIG (Resource Record Signature)
Signatures over each RRset (group of records of the same type for the same name).

```
tcd.ie. A 3600 IN RRSIG A 13 2 3600 20260501000000 20260401000000 12345 tcd.ie. [base64_signature]
```

Fields: covered type, algorithm, labels, original TTL, signature expiry, signature inception, key tag, signer name, signature.

Validated by: resolver fetches DNSKEY, verifies RRSIG using covered RRset bytes.

### DS (Delegation Signer)
Published in the *parent* zone; contains a hash of the child zone's KSK.

```
tcd.ie. 3600 IN DS 12345 13 2 [SHA-256_hash_of_KSK]
```

Fields: key tag, algorithm, digest type (2=SHA-256), digest.

This is the link in the chain of trust: parent zone signs its DS record for the child, which is the child's KSK fingerprint.

### NSEC3 (Next Secure version 3)
Provides authenticated denial of existence. Proves "this name does not exist" without enumerating all names.

NSEC3 hashes owner names (using iterated SHA-1 with a salt) before including them. Prevents zone walking (enumerating all names by following NSEC pointers). Still vulnerable to offline dictionary attack — attacker can hash common names and compare.

**NSEC** (original): lists actual next owner name in canonical order → leaks all zone names. Only use in non-sensitive zones.

## Chain of Trust Validation (step by step)

```
1. Root zone: resolver trusts root KSK (hard-coded trust anchor in software)
2. Root zone: DS record for .ie signed by root ZSK → proves root trusts .ie's KSK
3. .ie zone: publishes DNSKEY (KSK + ZSK)
4. .ie zone: DS record for tcd.ie signed by .ie ZSK
5. tcd.ie zone: publishes DNSKEY; signs all records with ZSK; RRSIGs present
6. Resolver: validates chain root → .ie → tcd.ie → individual records
```

## Signature Algorithms Comparison

| Algorithm | Key size | Signature size | Performance | Status |
|---|---|---|---|---|
| RSA/SHA-256 (alg 8) | 1024–4096 bits | Large | Slower | Widely deployed |
| ECDSA P-256 (alg 13) | 256 bits | Small (~64 bytes) | Fast | Recommended |
| Ed25519 (alg 15) | 256 bits | Small (~64 bytes) | Fastest | Modern |


## Relevant RFCs

- **RFC 4033** — *DNS Security Introduction and Requirements* — overview of DNSSEC goals, threat model, and the chain of trust concept
- **RFC 4034** — *Resource Records for the DNS Security Extensions* — defines DNSKEY, RRSIG, DS, NSEC record formats and semantics; the primary reference for exam questions on record structure
- **RFC 4035** — *Protocol Modifications for the DNS Security Extensions* — how resolvers use DNSSEC records to validate responses; the validation algorithm
- **RFC 5155** — *DNS Security (NSEC3)* — NSEC3 hashed denial-of-existence records that prevent zone walking while still providing authenticated NXDOMAIN

<!-- MODE:HINGLISH -->
# DNSSEC Records — Hinglish mein

## Four new record types — ek ek karo

**DNSKEY:** Zone ka public key yahan publish hota hai. Jaise notary apni seal publish kare.

Do types:
- ZSK (Zone Signing Key) — zone ke records sign karta hai, frequently rotate
- KSK (Key Signing Key) — sirf DNSKEY RRset sign karta hai, parent zone mein DS record hota hai iska

**RRSIG:** Actual digital signature. Har signed RRset ke saath RRSIG hota hai. Resolver DNSKEY use karke verify karta hai.

**DS (Delegation Signer):** Parent zone mein child zone ke KSK ka hash. Yahi chain of trust banata hai. .ie zone mein tcd.ie ka DS record hai.

**NSEC3:** Authenticated denial of existence. "Yeh naam exist nahi karta" ka signed proof. Pehle NSEC tha jo actual names list karta tha (zone walking possible tha). NSEC3 names ko hash karta hai — zone walking prevent hota hai. Offline dictionary attack abhi bhi possible lekin harder.

## Chain of trust yaad karo

Root (hard-coded trust anchor) → .ie (root ke DS record se validate) → tcd.ie (.ie ke DS record se validate) → individual records (tcd.ie ke ZSK ke RRSIG se validate)

Root ki public key resolver mein already embedded hoti hai. Wahan se puri chain verify ho sakti hai.

## Exam ke liye

Yeh four record types + chain of trust = Q4 ka core answer. DNSKEY + RRSIG + DS + NSEC3 — naam, kaam, kahan hain. Chain of trust: root → TLD → zone → records.
