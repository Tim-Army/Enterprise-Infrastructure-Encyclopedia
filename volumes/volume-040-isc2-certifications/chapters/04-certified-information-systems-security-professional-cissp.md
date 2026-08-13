# Chapter 04: Certified Information Systems Security Professional (CISSP)

## Learning Objectives

- Explain why CISSP is the pivot credential of the ISC2 ladder and the security profession.
- List the eight CISSP domains and their 2024 exam weights.
- Describe the CAT exam mechanics, the five-year experience gate, and the Associate path.
- Apply CISSP-level thinking across risk, architecture, IAM, testing, operations, and software.
- Complete a per-domain walkthrough for each CISSP domain.

## Theory and Architecture

The **Certified Information Systems Security Professional (CISSP)** is ISC2's
flagship and the most widely required advanced security credential in the world.
It certifies that its holder can **design, engineer, and manage** an
organization's whole security program — not operate a single tool, but decide
policy, architecture, and controls across eight domains collectively known as
the **Common Body of Knowledge (CBK)**. CISSP requires **five years** of paid
experience across two or more domains (a one-year waiver for a relevant degree or
approved credential); those who pass without the experience become an
**Associate of ISC2** with up to six years to earn it.

The exam is **Computer Adaptive Testing (CAT)**: **100–150 items in up to 3
hours**, pass mark **700/1000**. The outline effective **15 April 2024** weights
the domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Security and Risk Management | 16% |
| 2 | Asset Security | 10% |
| 3 | Security Architecture and Engineering | 13% |
| 4 | Communication and Network Security | 13% |
| 5 | Identity and Access Management (IAM) | 13% |
| 6 | Security Assessment and Testing | 12% |
| 7 | Security Operations | 13% |
| 8 | Software Development Security | 10% |

The 2024 refresh nudged **Domain 1 up to 16%** and **Domain 8 down to 10%** —
governance and risk remain the single largest area.

## Design Considerations

CISSP is the **pivot point** of the ladder: below it, CC and SSCP validate
foundations and operations; above and beside it, the **ISSAP/ISSEP/ISSMP**
concentrations and the specialist **CCSP/CGRC/CSSLP** credentials all assume
CISSP-level breadth. Design a study plan around **Domain 1 (16%)** as the
backbone — risk management, governance, law, and ethics frame every other
domain — and treat CISSP as a **management-level** exam: the "best" answer is
usually the one a security *manager* would choose (address root cause, follow
policy, manage risk) rather than the most technical fix.

## Implementation and Automation

The eight domains span the whole discipline; the labs below ground each in a
concrete artifact — a risk calculation (D1), a data-classification scheme (D2),
a trusted-computing/crypto check (D3), TLS and segmentation (D4), an RBAC model
(D5), a vulnerability triage (D6), log and IR operations (D7), and a dependency/
supply-chain scan (D8) — the same techniques the specialist credentials deepen.

## Validation and Troubleshooting

Confirm the CISSP blueprint before studying:

```text
isc2.org > Certifications > CISSP > Exam Outline:
  - eight domains and weights (16/10/13/13/13/12/13/10, eff 15 Apr 2024)
  - CAT: 100-150 items, up to 3 hours, 700/1000
  - five years of experience across >=2 domains (Associate path otherwise)
```

Common pitfalls: studying the pre-2024 weights; picking the most **technical**
answer instead of the **managerial** one; underestimating **Domain 1**; and
assuming passing equals certification — **endorsement** and **experience** are
required, and the **AMF** and **CPE** keep it active.

## Security and Best Practices

Think like a risk manager: tie every control to a **risk**, a **policy**, and a
**business objective**; prefer **root-cause** remediation; and respect **law,
regulation, and ethics** (the ISC2 Code of Ethics is examinable and binding).
CISSP satisfies **DoD 8140/8570 IAT/IAM Level III and IASAE** baselines and is a
common baseline for security-leadership roles.

## References and Knowledge Checks

- isc2.org: *CISSP* page, Exam Outline, and Exam Refresh FAQ; *CISSP Official Study Guide (CBK)*; *ISC2 Code of Ethics*.

**Knowledge checks**

1. Which CISSP domain is largest, and what does it cover?
2. Why is the "best" CISSP answer often managerial rather than technical?
3. What is the difference between a CISSP and an Associate of ISC2?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CISSP domain**.

**Shared prerequisites** — a Linux shell with `python3`, `openssl`, `ss`, and
`journalctl`; internet access for one TLS lab. **Cost:** none.

### Lab 4.1 — CISSP D1: Security and Risk Management (16%)

**Objective:** Compute Annualized Loss Expectancy (ALE) to justify a control.

```bash
python3 - <<'PY'
AV=250000; EF=0.4; ARO=0.2          # asset value, exposure factor, annual rate
SLE=AV*EF; ALE=SLE*ARO
print(f"SLE = AV*EF = ${SLE:,.0f}")
print(f"ALE = SLE*ARO = ${ALE:,.0f} / yr")
print("Spend on a control is justified up to ~ALE (minus residual risk).")
PY
```

**Expected result:** SLE $100,000 and ALE $20,000/yr — the quantitative risk
figure that justifies control spend, core to Domain 1.

**Negative test:** buy a $50,000/yr control for a $20,000/yr risk without a
qualitative rationale; you are over-spending relative to ALE.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — CISSP D2: Asset Security (10%)

**Objective:** Apply a data-classification scheme to drive handling.

```bash
python3 - <<'PY'
classify = {"marketing_flyer.pdf":"Public","payroll.xlsx":"Confidential",
            "merger_memo.docx":"Restricted"}
handling = {"Public":"no controls","Confidential":"encrypt + access control",
            "Restricted":"encrypt + MFA + need-to-know + DLP"}
for f,c in classify.items():
    print(f"{f:20} -> {c:12} -> {handling[c]}")
PY
```

**Expected result:** each asset mapped to a classification and its required
handling — classification driving protection, the essence of Asset Security.

**Negative test:** protect everything at the highest level; that wastes budget
and desensitizes users — controls follow classification.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — CISSP D3: Security Architecture and Engineering (13%)

**Objective:** Demonstrate an engineering primitive — asymmetric key generation
and a digital signature (non-repudiation).

```bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out priv.pem 2>/dev/null
openssl pkey -in priv.pem -pubout -out pub.pem
echo "contract terms" > c.txt
openssl dgst -sha256 -sign priv.pem -out c.sig c.txt
openssl dgst -sha256 -verify pub.pem -signature c.sig c.txt
```

**Expected result:** `Verified OK` — a private key signs, the public key
verifies, giving integrity and **non-repudiation**, a Domain 3 building block.

**Negative test:** sign with the public key; only the *private* key signs — the
public key verifies. The roles are not interchangeable.

**Rollback:** `rm -f priv.pem pub.pem c.txt c.sig`

### Lab 4.4 — CISSP D4: Communication and Network Security (13%)

**Objective:** Verify a server negotiates a modern TLS version and cipher.

```bash
echo | openssl s_client -connect www.isc2.org:443 -tls1_2 2>/dev/null \
  | grep -E 'Protocol|Cipher' | head
```

**Expected result:** a negotiated `TLSv1.2` (or higher) protocol and a strong
cipher suite — validating secure-channel design in Domain 4.

**Negative test:** force `-ssl3` or `-tls1`; a hardened server refuses obsolete
protocols — that refusal is the control working.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.5 — CISSP D5: Identity and Access Management (13%)

**Objective:** Model role-based access control (RBAC) and test an access
decision.

```bash
python3 - <<'PY'
roles = {"analyst":{"read"}, "admin":{"read","write","delete"}}
def can(role, action): return action in roles.get(role, set())
for r,a in [("analyst","read"),("analyst","delete"),("admin","delete")]:
    print(f"{r:8} {a:7} -> {'ALLOW' if can(r,a) else 'DENY'}")
PY
```

**Expected result:** analyst/read ALLOW, analyst/delete DENY, admin/delete ALLOW
— an RBAC decision enforcing least privilege, central to Domain 5.

**Negative test:** grant permissions to users directly instead of via roles; it
does not scale and breaks least privilege — assign to roles.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.6 — CISSP D6: Security Assessment and Testing (12%)

**Objective:** Triage vulnerabilities by CVSS band for remediation order.

```bash
python3 - <<'PY'
findings = [("CVE-A",9.8),("CVE-B",5.4),("CVE-C",7.5),("CVE-D",3.1)]
band = lambda s: "Critical" if s>=9 else "High" if s>=7 else "Medium" if s>=4 else "Low"
for cve,score in sorted(findings, key=lambda x:-x[1]):
    print(f"{cve}  CVSS {score}  -> {band(score)}")
PY
```

**Expected result:** findings ordered 9.8 (Critical), 7.5 (High), 5.4 (Medium),
3.1 (Low) — risk-ranked test output driving remediation, the Domain 6 workflow.

**Negative test:** remediate in the order findings were discovered; fix by
**severity and exposure**, not discovery order.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.7 — CISSP D7: Security Operations (13%)

**Objective:** Detect a brute-force pattern in authentication logs.

```bash
journalctl _COMM=sshd --no-pager 2>/dev/null | grep -c "Failed password" \
  || echo "0 (no sshd log on this host)"
echo "Threshold example: >10 failures/5 min from one IP -> alert + block"
```

**Expected result:** a count of failed authentications and a detection threshold
— the monitoring-and-response loop of Domain 7.

**Negative test:** alert on every single failure; alert fatigue hides real
attacks — tune thresholds and correlate.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.8 — CISSP D8: Software Development Security (10%)

**Objective:** Show input validation preventing an injection class.

```bash
python3 - <<'PY'
import sqlite3
db=sqlite3.connect(":memory:"); db.execute("CREATE TABLE u(name TEXT)")
db.execute("INSERT INTO u VALUES('alice')")
evil = "x'; DROP TABLE u;--"
# Parameterized query treats input as DATA, not SQL:
rows = db.execute("SELECT * FROM u WHERE name=?", (evil,)).fetchall()
print("rows matched:", rows, "-> table intact:", 
      db.execute("SELECT count(*) FROM u").fetchone()[0], "row(s)")
PY
```

**Expected result:** no rows match and the table still has 1 row — a
parameterized query neutralizes SQL injection, the Domain 8 secure-coding
lesson.

**Negative test:** build the query with string concatenation (`"... name='"+evil+"'"`);
that executes the injected `DROP` — never concatenate untrusted input into SQL.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CISSP is the pivot of the ISC2 ladder and the security profession's flagship:
eight CBK domains weighted 16/10/13/13/13/12/13/10 (2024 refresh), a CAT exam,
and a five-year experience gate. It certifies program-level design and
management across risk, asset protection, architecture, network security, IAM,
testing, operations, and software — the breadth every ISC2 specialist credential
assumes.

- [ ] I can list the eight CISSP domains and their weights.
- [ ] I can compute SLE/ALE and classify assets for handling.
- [ ] I can sign/verify, model RBAC, and neutralize SQL injection.
- [ ] I can explain why CISSP answers are managerial and the Associate path.
- [ ] I completed Labs 4.1–4.8 including each negative test.
