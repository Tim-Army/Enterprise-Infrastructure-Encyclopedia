# Chapter 05: Web Security — OSWA and OSWE

## Learning Objectives

- Explain the web-security credentials: OSWA (WEB-200) and OSWE (WEB-300).
- Distinguish black-box web assessment (OSWA) from white-box code review (OSWE).
- Practice web-vulnerability methodology against your own lab, paired with defenses.
- Understand each vulnerability class well enough to fix it.
- Complete per-topic walkthroughs for the OSWA and OSWE topic areas.

## Theory and Architecture

Two credentials cover web application security at increasing depth:

- **OSWA (OffSec Web Assessor, WEB-200)** — **black-box** web assessment:
  enumerating web apps and finding and exploiting common vulnerability classes —
  **injection** (SQL, command), **cross-site scripting (XSS)**, and
  **authentication/session** flaws — the way an external tester would.
- **OSWE (OffSec Web Expert, WEB-300)** — **white-box** application security:
  reading **source code** to find deep vulnerabilities (authentication bypasses,
  injection, insecure deserialization) and **chaining** them to remote code
  execution. It is one of the three **OSCE³** credentials and does **not** expire.

OSWA finds vulnerabilities from the outside; OSWE understands and chains them from
the inside — both taught here so you can **fix** them.

## Design Considerations

Take **OSWA** to build a solid black-box methodology (map the app, test every
input, understand each class), then **OSWE** to develop the **code-reading** skill
that finds what scanners miss and to learn **exploit chaining**. For both, the
durable skill is understanding **root cause** — parameterization, output encoding,
safe deserialization, correct authentication — which is exactly what a developer
needs. Practice only against **your own** deliberately vulnerable apps or
authorized labs.

## Implementation and Automation

The labs below use a **local, authorized** app (a Python demo or your own
vulnerable VM) to make each class concrete, and each pairs the flaw with its
**secure-coding fix**. They stay at demonstration and defense — the point is
recognizing and remediating the class.

## Validation and Troubleshooting

Confirm the courses on offsec.com:

```text
offsec.com/courses:
  - WEB-200 -> OSWA (black-box: injection, XSS, auth) 
  - WEB-300 -> OSWE (white-box source review, chaining to RCE) — no expiry, part of OSCE3
```

Common pitfalls: relying on **automated scanners** alone (they miss logic and
chained flaws); and testing web apps you do not own — use your own or authorized
targets.

## Security and Best Practices

Fix at the **root cause**: parameterized queries (SQLi), context-aware **output
encoding** (XSS), input validation and safe APIs (command injection), robust
**authentication/session** management, and **safe deserialization**. Adopt OWASP
**ASVS** and the **Top 10** as the checklist. Every offensive technique here maps
to one of these controls.

## References and Knowledge Checks

- offsec.com: *WEB-200 (OSWA)* and *WEB-300 (OSWE)* course pages; OWASP Top 10 and ASVS.

**Knowledge checks**

1. What distinguishes OSWA (black-box) from OSWE (white-box)?
2. What is the root-cause fix for SQL injection and for XSS?
3. Why is code-reading (OSWE) able to find what scanners miss?

## Hands-On Lab

Per-topic walkthroughs — **against your own local app only; each pairs the flaw
with its fix.**

**Shared prerequisites** — a shell with `python3` (and `sqlite3`); a local
authorized web app or the inline demos below. **Cost:** none.

### OSWA — Black-box Web Assessment

### Lab 5.1 — OSWA: web enumeration and mapping

**Objective:** Map an app's surface (endpoints, methods, parameters).

```bash
python3 -m http.server 8081 --directory /tmp >/tmp/w.log 2>&1 &
sleep 1
curl -s -I http://127.0.0.1:8081/ | head -3
curl -s http://127.0.0.1:8081/ | head -3
kill %1 2>/dev/null
```

**Expected result:** headers and content from your **own** local server — the
mapping step that precedes any web test. **Defense:** minimize exposed endpoints
and information in headers.

**Negative test:** test inputs before mapping the app; enumerate the full surface
first — untested endpoints hide flaws.

**Cleanup:** `pkill -f 'http.server 8081' 2>/dev/null || true`

### Lab 5.2 — OSWA: SQL injection (demonstrate and fix)

**Objective:** Show injection against a vulnerable query and the parameterized fix.

```bash
python3 - <<'PY'
import sqlite3
db=sqlite3.connect(":memory:"); db.execute("CREATE TABLE u(name TEXT, role TEXT)")
db.execute("INSERT INTO u VALUES('admin','admin')")
evil = "x' OR '1'='1"
# VULNERABLE (string-built) vs SAFE (parameterized):
bad = f"SELECT * FROM u WHERE name='{evil}'"
print("vulnerable query returns:", db.execute(bad).fetchall(), "<- auth bypass!")
print("parameterized returns   :", db.execute("SELECT * FROM u WHERE name=?", (evil,)).fetchall())
PY
```

**Expected result:** the string-built query returns the admin row (injection
bypass) while the parameterized query returns nothing — the flaw and its fix.
**Defense:** always parameterize.

**Negative test:** "sanitize" by escaping quotes manually; parameterization is the
correct, complete fix — do not hand-roll escaping.

**Cleanup:** none.

### Lab 5.3 — OSWA: cross-site scripting (demonstrate and fix)

**Objective:** Show unescaped output and the encoding fix.

```bash
python3 - <<'PY'
import html
untrusted = "<script>alert(1)</script>"
print("reflected unsafely:", untrusted, "<- executes in a browser")
print("output-encoded    :", html.escape(untrusted), "<- rendered as text")
PY
```

**Expected result:** the raw string (which would execute) versus the encoded
`&lt;script&gt;…` (inert) — XSS and its fix. **Defense:** context-aware output
encoding and a Content-Security-Policy.

**Negative test:** filter the word "script"; blacklist filtering is bypassable —
**encode on output** instead.

**Cleanup:** none.

### Lab 5.4 — OSWA: authentication and session testing

**Objective:** Reason about auth/session weaknesses and controls.

```bash
python3 - <<'PY'
checks = {"Credential stuffing":"MFA + rate limiting + breached-password checks",
          "Weak session id":"long random ids, HttpOnly+Secure+SameSite cookies",
          "No lockout":"progressive lockout/backoff",
          "IDOR":"authorize every object access server-side"}
for flaw,fix in checks.items(): print(f"{flaw:20} -> {fix}")
PY
```

**Expected result:** common auth/session flaws mapped to controls — the OSWA
auth-testing area, oriented to fixes. **Defense:** each listed control.

**Negative test:** trust client-side checks; **authorization must be enforced
server-side** for every request.

**Cleanup:** none.

### OSWE — White-box Web Expert

### Lab 5.5 — OSWE: source-code review methodology

**Objective:** Trace untrusted input to a dangerous sink in code.

```bash
cat > app.py <<'PY'
def handler(req):
    name = req["name"]                 # SOURCE: untrusted input
    return db.query("SELECT * FROM u WHERE name='" + name + "'")  # SINK: injection
PY
grep -nE 'req\[|query\(|exec|eval|system|deserialize|pickle' app.py
echo "OSWE method: trace SOURCE (input) -> SINK (dangerous call); flag unsafe flows."
```

**Expected result:** the source (`req["name"]`) and the injection sink flagged by
grep — the code-reading method OSWE teaches. **Defense:** parameterize the sink.

**Negative test:** review only for style; **data-flow from source to sink** is
what reveals real vulnerabilities.

**Cleanup:** `rm -f app.py`

### Lab 5.6 — OSWE: authentication bypass (logic review)

**Objective:** Spot an authentication-logic flaw in code.

```bash
python3 - <<'PY'
def is_admin(user):
    # FLAW: type juggling / loose compare lets "0"==0 or ""==False slip through
    return user.get("role") == "admin" or user.get("is_admin")  # truthy non-bool bug
# Fix: explicit, strict checks and server-side session role, never client-supplied.
print("Review finding: authorization derived from client-supplied fields -> bypass risk.")
PY
```

**Expected result:** a flagged auth-bypass pattern (authorization from
client-controlled/loose fields) — the logic review OSWE rewards. **Defense:**
strict, server-side authorization.

**Negative test:** trust a client-supplied `is_admin`; derive roles from a
**server-side session**, never the request.

**Cleanup:** none.

### Lab 5.7 — OSWE: insecure deserialization and chaining (concept)

**Objective:** Understand deserialization risk and exploit chaining.

```bash
python3 - <<'PY'
print("Insecure deserialization: untrusted data -> object -> gadget chain -> RCE.")
print("Chaining (OSWE): auth bypass -> file write -> deserialization -> RCE, combined into one exploit.")
print("Defense: never deserialize untrusted input; use safe formats (JSON) + schema validation.")
PY
```

**Expected result:** the deserialization-to-RCE concept and how OSWE **chains**
primitives — the expert-level skill. **Defense:** avoid native deserialization of
untrusted data; validate against a schema.

**Negative test:** deserialize untrusted input with a native (pickle-style)
loader; use a **safe format** and validate — native deserialization is dangerous.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OSWA (WEB-200) and OSWE (WEB-300) cover web security from black-box assessment to
white-box code review: OSWA finds injection, XSS, and auth flaws from the outside;
OSWE reads source to find and **chain** deep vulnerabilities to RCE (an OSCE³
credential, no expiry). Every class here is paired with its root-cause fix and
practiced only against your own or authorized apps.

- [ ] I can distinguish OSWA (black-box) from OSWE (white-box).
- [ ] I can demonstrate SQLi and XSS and state their fixes.
- [ ] I can trace source-to-sink and spot an auth-bypass in code.
- [ ] I can explain insecure deserialization and exploit chaining.
- [ ] I completed Labs 5.1–5.7 including each negative test.
