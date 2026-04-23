<!-- MODE:EASY -->
# Audit + Logging — Simple Version

An audit log is a record of everything that happens in a system. Think of it like CCTV footage for your application — you might not watch it every day, but when something goes wrong, you can look back and see exactly what happened, who did it, and when.

**Why audit logs matter:**
- **Detect attacks:** If someone is trying lots of wrong passwords, the log shows it
- **Investigate incidents:** After a breach, "what did the attacker access?" is only answerable with good logs
- **Compliance:** GDPR and most regulations require you to be able to prove what happened to data
- **Non-repudiation:** A user can't deny placing an order if the log shows their authenticated action

**The golden rules for audit logs:**

1. **Append-only** — logs can only be added to, never deleted or changed. If an admin can delete logs, they can cover their tracks.

2. **Hash-chained** — each log entry includes a hash of the previous entry. If anyone tries to remove or change an old entry, all subsequent hashes break. Like a blockchain for your logs.

3. **Sent to an isolated store** — don't keep logs on the same server as the application. If the server is compromised, the attacker shouldn't be able to destroy the evidence.

4. **Include enough context** — log *who* did *what* to *which resource* at *what time* with *what result*.

**What NOT to log:**
- Passwords (obviously)
- Full credit card numbers
- Encryption keys
- Any PII you don't absolutely need in the log

<!-- MODE:TECHNICAL -->
# Audit + Logging (Append-only, Hash-chained)

## What to Log (at minimum)

Every security-relevant event:
- Authentication events: login success/failure, MFA challenge, session creation/expiry, password reset
- Authorisation decisions: access granted/denied, privilege escalation attempts
- Data access: which records accessed, by whom, at what time
- Data modification: create/update/delete with before/after values for sensitive fields
- Configuration changes: any change to security settings, user roles, firewall rules
- Admin actions: all privileged operations
- Errors: unexpected exceptions (potential exploitation attempts)

## Log Entry Format (structured)

```json
{
  "timestamp": "2026-04-23T14:32:01.234Z",
  "event_type": "data_access",
  "actor": { "user_id": "u-4729", "ip": "10.0.1.42", "session": "s-abc123" },
  "resource": { "type": "patient_record", "id": "p-9981" },
  "action": "read",
  "outcome": "success",
  "hash_prev": "sha256:abcdef...",
  "hash_self": "sha256:123456..."
}
```

## Hash Chaining

Each entry includes `SHA-256(previous_entry_bytes)`. Creating a tamper-evident chain:

```
entry_1 | hash(genesis)
entry_2 | hash(entry_1)
entry_3 | hash(entry_2)
...
```

Deleting or modifying `entry_2` breaks the chain: `hash(modified_entry_2) ≠ hash_prev` in `entry_3`. Auditors can verify the chain with a single pass.

## Architectural Requirements

**Separation:** Log store must be on a different system (ideally different network segment) from the application. Application has write-only access to logs. Admins cannot delete from application interface.

**WORM storage:** Write-Once-Read-Many. AWS S3 Object Lock, Azure Immutable Blob Storage, or physical tape archive for long-term retention.

**SIEM integration:** Logs streamed to Security Information and Event Management system (Splunk, Elastic SIEM, Chronicle). SIEM runs correlation rules: 10 failed logins + 1 success → alert.

## Retention and GDPR

Tension: GDPR right to erasure (Art. 17) vs audit log retention (security + legal requirement).

Resolution: pseudonymise audit logs after the erasure request. Replace `user_id = "john.smith@example.com"` with `user_id = "ERASED-2026-04-23"`. The *action* is retained; the *identity* is removed.

Legal basis for retention: Article 6(1)(c) — compliance with legal obligation; legitimate interest for security investigation (time-limited).

## What Not to Log

- Passwords, tokens, session cookies in full
- Full credit card numbers (PCI-DSS requirement)
- Encryption keys
- Excessive PII (minimisation — log user_id, not full name + address + DOB)

<!-- MODE:HINGLISH -->
# Audit Logging — Hinglish mein

## Audit log kya hai aur kyun chahiye?

Socho security camera — cheezein hoti rehti hain, log karta rehta hai. Kuch hua toh playback karo, dekho kya hua, kaun tha.

Security breach ke baad pehla sawaal: "attacker ne kya access kiya?" — audit log ke bina answer impossible.

GDPR ke under bhi: data se kya kiya gaya, yeh prove karna padta hai.

## Golden rules

**Append-only:** Delete nahi ho sakta. Agar admin logs delete kar sake toh woh apni galati chhupa sakta hai. Write-only access application ko, delete kisi ko nahi.

**Hash-chained:** Har entry mein pichle entry ka hash. Koi bhi entry modify karo → sab baad ke entries ka hash toot jaata hai. Tampering detect ho jaata hai.

**Alag server par:** App server aur log server alag. App compromise ho → attacker logs destroy nahi kar sakta.

**WORM storage** (best case): Write Once Read Many. AWS S3 Object Lock, Azure Immutable Blob. Ek baar write karo, kabhi delete nahi.

## Kya log karein?

- Login success + failure (with IP, timestamp, user_id)
- Access grants + denials
- Data read/write/delete (sensitive records ke liye)
- Configuration changes
- Admin actions (sab kuch)
- Errors aur exceptions

## Kya log mat karein?

- Passwords
- Full credit card numbers
- Encryption keys
- Zyada PII (naam, address, DOB sirf agar zaroori ho)

## GDPR + audit log tension

User ne "right to erasure" request kiya (Art. 17). Lekin audit log mein uski activity hai jo security ke liye rakhni hai.

Solution: **pseudonymise** the log — user_id ko replace karo ek random token se. Action record rehta hai, identity remove ho jaati hai. Dono requirements satisfy.

## Exam ke liye

Q3 mein audit logging mention karo: append-only, hash-chained, isolated store, SIEM integration. GDPR tension aur pseudonymisation fix bhi mention karo — marks milenge.
