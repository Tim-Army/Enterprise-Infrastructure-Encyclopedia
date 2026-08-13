# Chapter 05: Web Application Security

## Learning Objectives

- Cover the web-application certifications (HTB CWES/CWEE; INE eWPT/eWPTX; TCM PWPA/PWPP/PWPE).
- Understand the OWASP Top 10 vulnerability classes — to write secure code and detect exploitation.
- Model each major vulnerability class and its fix.

## Understand the vulnerability to remove it

The web certs — HTB **CWES**/**CWEE**, INE **eWPT**/**eWPTX**, TCM **PWPA**/**PWPP**/**PWPE** — assess finding and demonstrating web vulnerabilities in authorized targets. The defensive translation is **secure coding and detection**: each vulnerability class maps to a coding pattern that prevents it and a signal that detects its exploitation. This chapter models the classes and their fixes (no operational exploitation).

| OWASP-class vulnerability | Root cause | Fix (secure coding) |
|:---|:---|:---|
| **Injection (SQLi)** | Untrusted input in a query | Parameterized queries / prepared statements |
| **XSS** | Untrusted input in HTML output | Context-aware output encoding + CSP |
| **Broken access control (IDOR)** | Authorization not enforced per object | Server-side authorization on every object access |
| **SSRF** | Server fetches an attacker-controlled URL | Allowlist destinations; block internal ranges |
| **Auth flaws** | Weak session/credential handling | MFA, secure session mgmt, rate limiting |
| **Insecure deserialization** | Trusting serialized input | Avoid native deserialization of untrusted data |

## Hands-On Lab

Python models vulnerability classes and their fixes. **Cost:** none.

### Lab 5.1 — SQL injection: the flaw and the fix

**Objective:** Show why string-built queries are exploitable and how parameterization removes the class.

```bash
python3 - <<'EOF'
import sqlite3
db = sqlite3.connect(":memory:"); db.execute("CREATE TABLE users(name, role)")
db.execute("INSERT INTO users VALUES ('alice','user'), ('admin','admin')")
user_input = "x' OR '1'='1"   # attacker-controlled

# VULNERABLE: input concatenated into the query -> the OR '1'='1' returns all rows
vuln = f"SELECT name FROM users WHERE name = '{user_input}'"
print("vulnerable query returns:", [r[0] for r in db.execute(vuln)])   # leaks all users

# SECURE: parameterized -> the input is data, never SQL; the injection is inert
rows = db.execute("SELECT name FROM users WHERE name = ?", (user_input,)).fetchall()
print("parameterized returns:  ", [r[0] for r in rows])                 # matches nothing
EOF
```

**Expected result:**

```text
vulnerable query returns: ['alice', 'admin']
parameterized returns:   []
```

The string-built query lets `' OR '1'='1` return every row (injection); the parameterized query treats the same input as **data**, so the injection is inert and matches nothing. Parameterization doesn't *mitigate* SQLi — it **removes the entire class**. The web certs teach the exploit; the defensive lesson is: never build queries by concatenation.

**Negative test:** "Sanitizing" by escaping quotes instead of parameterizing — brittle and bypassable (encoding tricks, second-order injection); parameterized queries are the correct, complete fix.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.2 — IDOR / broken access control

**Objective:** Model the most common serious web flaw — missing per-object authorization.

```bash
python3 - <<'EOF'
# IDOR: the app trusts an object ID from the request without checking the user OWNS it
orders = {101:"alice", 102:"bob", 103:"alice"}
def get_order(requesting_user, order_id, enforce_authz):
    owner = orders.get(order_id)
    if enforce_authz and owner != requesting_user:
        return f"DENY: {requesting_user} may not access order {order_id} (owned by {owner})"
    return f"return order {order_id} (owner {owner})"
print("VULNERABLE:", get_order("alice", 102, enforce_authz=False))   # alice reads bob's order
print("SECURE:    ", get_order("alice", 102, enforce_authz=True))
EOF
```

**Expected result:** Without server-side authorization, alice reads bob's order (IDOR); with it, she's denied. Broken access control is consistently the top web risk, and the fix is unglamorous but absolute: **enforce authorization on the server for every object access**, never trust that the client only requests its own IDs. The certs surface these flaws; secure design prevents them.

**Negative test:** Hiding other users' IDs in the UI but not enforcing authorization server-side — an attacker just changes the ID in the request; access control must be server-side, per object, every time.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.3 — Detecting web exploitation

**Objective:** Turn attack knowledge into detection signatures.

```bash
python3 - <<'EOF'
import re
# WAF/detection view: recognize exploitation attempts in requests (defensive)
signatures = {
  "SQLi":      r"('|\")\s*(or|and)\s+['\"0-9]", 
  "XSS":       r"<script|onerror\s*=|javascript:",
  "path traversal": r"\.\./|\.\.\\",
  "SSRF":      r"(169\.254\.169\.254|localhost|127\.0\.0\.1|metadata)",
}
requests = [
  "GET /product?id=5",
  "GET /product?id=5' OR '1'='1",
  "POST /comment body=<script>steal()</script>",
  "GET /fetch?url=http://169.254.169.254/latest/meta-data/",
]
for r in requests:
    hits = [name for name, pat in signatures.items() if re.search(pat, r, re.I)]
    print(f"{r[:48]:<50}-> {'ALERT: '+', '.join(hits) if hits else 'clean'}")
EOF
```

**Expected result:** The SQLi payload, the `<script>` XSS, and the SSRF to the cloud metadata endpoint all alert; the benign request is clean. Understanding how these attacks look on the wire (a CWES/eWPT skill) is what lets a defender **write the detection** — a WAF rule, a SIEM signature. Offensive knowledge directly produces defensive coverage.

**Negative test:** Signature-only detection is evadable (encoding, obfuscation) — so pair it with secure coding (Labs 5.1–5.2) that removes the vulnerability regardless; detection and prevention are complementary, not either/or.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] SQLi and its complete fix (parameterization) modeled.
- [ ] IDOR / broken access control and server-side authorization drilled.
- [ ] Web-exploitation detection signatures (turning attack knowledge into defense) built.
