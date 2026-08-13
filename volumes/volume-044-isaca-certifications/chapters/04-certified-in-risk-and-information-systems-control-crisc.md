# Chapter 04: Certified in Risk and Information Systems Control (CRISC)

## Learning Objectives

- Explain what CRISC certifies and its focus on IT risk.
- List the four CRISC domains and their exam weights.
- Apply IT-risk practice: governance, assessment, response, and control monitoring.
- Relate CRISC to CISM and CGEIT in the governance stack.
- Complete a per-domain walkthrough for each CRISC domain.

## Theory and Architecture

The **Certified in Risk and Information Systems Control (CRISC)** certifies the
identification, assessment, response, and monitoring of **IT risk**, and the
design and operation of the **controls** that treat it. It is the risk-specialist
credential — deeper on quantifying and treating risk than CISM. Updated in **2025**,
the exam is **150 questions** across four weighted domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Governance | 26% |
| 2 | IT Risk Assessment | 22% |
| 3 | Risk Response and Reporting | 32% |
| 4 | Technology and Security | 20% |

**Risk Response and Reporting (32%)** leads — treating risk and reporting it to
stakeholders is the core deliverable.

## Design Considerations

CRISC rewards the ability to connect **enterprise risk** to **IT controls**: build
a risk register, assess likelihood and impact, choose a treatment (accept/
mitigate/transfer/avoid), and monitor **key risk indicators (KRIs)**. Study Domain
3 (Response and Reporting) most heavily, and ground everything in a recognized
**risk framework**. CRISC pairs with **CISM** (security management) and **CGEIT**
(governance), and with ISC2's governance material.

## Implementation and Automation

The labs below model the risk practitioner's artifacts: a governance/appetite
statement (D1), a risk assessment (D2), a risk-treatment and KRI report (D3), and
a control mapped to a risk (D4).

## Validation and Troubleshooting

Confirm the CRISC blueprint before studying:

```text
isaca.org > Credentialing > CRISC > Exam Content Outline:
  - four domains and weights (26/22/32/20), 150 questions, updated 2025
  - three years of IT risk management/control experience
```

Common pitfalls: studying a **pre-2025** outline; confusing a **KRI** (leading
risk indicator) with a **KPI** (performance); and reporting risk without a clear
**treatment decision** and owner.

## Security and Best Practices

Maintain a living **risk register** with owners and treatment plans; express risk
in terms leadership can act on (likelihood × impact, or quantified loss);
monitor **KRIs** against thresholds; and tie controls back to the risks they
treat. Align to **NIST RMF/ISO 31000/COBIT**. Renew via CPE.

## References and Knowledge Checks

- isaca.org: *CRISC* Exam Content Outline and review manual; ISO 31000; NIST RMF.

**Knowledge checks**

1. Which CRISC domain is largest, and what does it deliver?
2. What is the difference between a KRI and a KPI?
3. What are the four risk-treatment options?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CRISC domain**.

**Shared prerequisites** — a Linux shell with `python3`. **Cost:** none.

### Lab 4.1 — CRISC D1: Governance (26%)

**Objective:** Express risk appetite and tolerance.

```bash
python3 - <<'PY'
appetite = {"data breach":"LOW appetite -> strong controls, low tolerance",
            "project delay":"MODERATE appetite -> some risk acceptable for speed",
            "regulatory non-compliance":"ZERO appetite -> must comply"}
for risk,stance in appetite.items(): print(f"{risk:26} -> {stance}")
PY
```

**Expected result:** risks mapped to an appetite/tolerance stance — the governance
foundation (Domain 1) that frames every risk decision.

**Negative test:** treat all risks with one blanket appetite; appetite **varies**
by risk type — state it per category.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.2 — CRISC D2: IT Risk Assessment (22%)

**Objective:** Score risks by likelihood and impact into a register.

```bash
python3 - <<'PY'
def score(l,i):
    s=l*i; band="LOW" if s<=6 else "MEDIUM" if s<=14 else "HIGH"; return s,band
for name,l,i in [("Unpatched internet-facing RCE",5,5),("Lost laptop (encrypted)",3,2),
                 ("Insider data theft",2,5)]:
    s,b=score(l,i); print(f"{name:32} L{l}xI{i}={s:2} -> {b}")
PY
```

**Expected result:** a scored, banded risk register (25 HIGH, 6 LOW, 10 MEDIUM) —
the assessment of Domain 2.

**Negative test:** rank by likelihood alone; a rare but catastrophic risk still
ranks high — risk is likelihood × impact.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.3 — CRISC D3: Risk Response and Reporting (32%)

**Objective:** Choose treatments and report KRIs against thresholds.

```bash
python3 - <<'PY'
kris = {"Overdue high-risk findings":(7,5,"RED"),   # (actual, threshold, status)
        "Privileged accounts without MFA":(0,0,"GREEN"),
        "Vendors without risk assessment":(3,2,"AMBER")}
for kri,(a,t,s) in kris.items(): print(f"{kri:34} actual {a} / threshold {t} -> {s}")
print("Treatments: RED -> escalate + mitigate; AMBER -> plan; GREEN -> monitor.")
PY
```

**Expected result:** KRIs reported against thresholds with treatment actions — the
response-and-reporting deliverable that is CRISC's largest domain.

**Negative test:** report risk status with no thresholds; a **KRI** needs a
threshold to signal action — define them.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — CRISC D4: Technology and Security (20%)

**Objective:** Map a control to the risk it treats and rate residual risk.

```bash
python3 - <<'PY'
control = {"risk":"credential theft (inherent HIGH)",
           "control":"phishing-resistant MFA + monitoring",
           "residual":"LOW (control effective)"}
for k,v in control.items(): print(f"{k:9}: {v}")
PY
```

**Expected result:** a control mapped to its risk with residual risk rated — the
technology/security control linkage of Domain 4.

**Negative test:** deploy controls with no link to a risk; every control should
**treat** an identified risk and reduce residual risk measurably.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CRISC certifies IT-risk practice: four domains weighted 26/22/32/20 (2025 update),
led by risk response and reporting. It connects enterprise risk to IT controls —
appetite, assessment, treatment, KRIs, and control monitoring — pairing with CISM
and CGEIT in the governance stack.

- [ ] I can list the four CRISC domains and their weights.
- [ ] I can express risk appetite and score a risk register.
- [ ] I can choose treatments and report KRIs against thresholds.
- [ ] I can map a control to its risk and rate residual risk.
- [ ] I completed Labs 4.1–4.4 including each negative test.
