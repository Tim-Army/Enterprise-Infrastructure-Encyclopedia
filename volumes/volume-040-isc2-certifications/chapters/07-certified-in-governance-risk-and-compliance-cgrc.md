# Chapter 07: Certified in Governance, Risk and Compliance (CGRC)

## Learning Objectives

- Explain what CGRC certifies and its history as the former CAP credential.
- List the seven CGRC domains and their exam weights.
- Describe how CGRC maps to the NIST Risk Management Framework and the authorization (ATO) process.
- Apply GRC thinking: categorization, control selection, assessment, and continuous monitoring.
- Complete a per-domain walkthrough for each CGRC domain.

## Theory and Architecture

**Certified in Governance, Risk and Compliance (CGRC)** — formerly the
**Certified Authorization Professional (CAP)** — is ISC2's credential for the
people who **authorize systems to operate**: the security-control assessors,
system owners, and authorization staff who run the **Risk Management Framework
(RMF)** and grant or deny an **Authorization to Operate (ATO)**. It is the most
**process- and documentation-oriented** ISC2 credential, heavily aligned to
**NIST SP 800-37 (RMF)**, **SP 800-53 (controls)**, and privacy frameworks. It
requires **two years** of experience.

The exam is **125 items in 3 hours**, pass mark **700/1000**. The outline
effective **15 June 2024** weights the domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Security and Privacy Governance, Risk Management, and Compliance Program | 16% |
| 2 | Scope of the System | 10% |
| 3 | Selection and Approval of Framework, Security, and Privacy Controls | 14% |
| 4 | Implementation of Security and Privacy Controls | 17% |
| 5 | Assessment/Audit of Security and Privacy Controls | 16% |
| 6 | System Compliance | 14% |
| 7 | Compliance Maintenance | 13% |

The seven domains trace the **RMF lifecycle** end to end — from establishing the
governance program, through scoping and control selection, to implementation,
assessment, authorization, and ongoing maintenance.

## Design Considerations

CGRC is for **government, defense, and regulated-industry** roles where a system
cannot go live without a formal, risk-based authorization. It pairs naturally
with **ISSEP** (engineering to the RMF) and **CISSP Domain 1** (risk and
governance). If your work involves **System Security Plans (SSPs)**, **control
assessments**, **POA&Ms** (Plans of Action and Milestones), or **continuous
monitoring**, CGRC formalizes it. The credential rewards **process fluency** —
knowing *which RMF step produces which artifact* — more than deep technical
tooling.

## Implementation and Automation

The labs below model the **artifacts and decisions** of the RMF: a
categorization by impact (Domain 2), a control-baseline selection (Domain 3), a
control-implementation record (Domain 4), an assessment finding and POA&M
(Domain 5), an authorization decision (Domain 6), and a continuous-monitoring
cadence (Domain 7) — the documentation trail a CGRC holder owns.

## Validation and Troubleshooting

Confirm the CGRC blueprint before studying:

```text
isc2.org > Certifications > CGRC > Exam Outline:
  - seven domains and weights (16/10/14/17/16/14/13, eff 15 Jun 2024)
  - 125 items, 3 hours, 700/1000
  - two years of experience; formerly named CAP
```

Common pitfalls: studying old **CAP** material without checking the 2024 CGRC
outline (which added **privacy** throughout); treating **categorization** (FIPS
199 impact levels) casually — it drives the entire control baseline; and
confusing **assessment** (testing controls) with **authorization** (accepting
residual risk).

## Security and Best Practices

Ground CGRC in the **NIST RMF**: categorize honestly (over- or under-
categorizing distorts every downstream control), select the correct **SP 800-53
baseline** and tailor it, document in the **SSP**, assess with evidence, track
gaps in a **POA&M**, and never let authorization become a one-time event —
**continuous monitoring** is the final and ongoing domain. Renew with CPE and
AMF.

## References and Knowledge Checks

- isc2.org: *CGRC* page and Exam Outline; NIST SP 800-37 (RMF), SP 800-53, SP 800-53A, FIPS 199.

**Knowledge checks**

1. What was CGRC previously called, and what was added in the 2024 refresh?
2. How do the seven CGRC domains map onto the RMF lifecycle?
3. What is the difference between assessing a control and authorizing a system?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CGRC domain**.

**Shared prerequisites** — a Linux shell with `python3`. **Cost:** none.

### Lab 7.1 — CGRC: Governance, Risk Management, and Compliance Program (16%)

**Objective:** Establish a control-to-authority governance mapping.

```bash
python3 - <<'PY'
program = {"policy":"board-approved infosec policy",
           "framework":"NIST RMF + 800-53",
           "roles":"System Owner, ISSO, Assessor, Authorizing Official",
           "cadence":"annual review + continuous monitoring"}
for k,v in program.items(): print(f"{k:10}: {v}")
PY
```

**Expected result:** the pillars of a GRC program — policy, framework, roles,
cadence — the governance foundation CGRC Domain 1 establishes.

**Negative test:** run controls with no named Authorizing Official; without
accountable authority, risk acceptance is undefined.

**Cleanup:** none.

### Lab 7.2 — CGRC: Scope of the System (10%)

**Objective:** Categorize a system's impact (FIPS 199 high-water mark).

```bash
python3 - <<'PY'
cia = {"confidentiality":"Moderate","integrity":"High","availability":"Low"}
order = {"Low":1,"Moderate":2,"High":3}
hwm = max(cia.values(), key=lambda v: order[v])
print("CIA impact:", cia)
print(f"System categorization (high-water mark) = {hwm}")
PY
```

**Expected result:** a system categorized **High** (the maximum across C/I/A) —
the FIPS 199 categorization that scopes the whole authorization, CGRC Domain 2.

**Negative test:** average the three impact levels; categorization takes the
**high-water mark**, not the mean.

**Cleanup:** none.

### Lab 7.3 — CGRC: Selection and Approval of Controls (14%)

**Objective:** Select the control baseline that matches the categorization.

```bash
python3 - <<'PY'
baseline = {"Low":"SP 800-53 Low baseline","Moderate":"Moderate baseline",
            "High":"High baseline"}
cat = "High"
print(f"Categorization {cat} -> select {baseline[cat]}, then TAILOR (add/remove/parameterize).")
PY
```

**Expected result:** the High categorization selecting the **High baseline**,
then tailoring — the control-selection step of CGRC Domain 3.

**Negative test:** apply every control in the catalog; baselines are tailored to
the categorization — more controls is not automatically better.

**Cleanup:** none.

### Lab 7.4 — CGRC: Implementation of Controls (17%)

**Objective:** Record a control implementation in an SSP-style entry.

```bash
python3 - <<'PY'
ssp_entry = {"control":"AC-2 Account Management",
             "status":"Implemented",
             "how":"central IdP provisions/deprovisions; quarterly access review",
             "responsible":"IAM team"}
for k,v in ssp_entry.items(): print(f"{k:12}: {v}")
PY
```

**Expected result:** a System Security Plan entry documenting *how* a control is
implemented and *who* owns it — the artifact CGRC Domain 4 (the heaviest)
produces.

**Negative test:** mark a control "Implemented" with no description of how;
assessors need the implementation detail to test it.

**Cleanup:** none.

### Lab 7.5 — CGRC: Assessment/Audit of Controls (16%)

**Objective:** Turn an assessment finding into a POA&M item.

```bash
python3 - <<'PY'
finding = {"control":"AU-6 log review","result":"Other Than Satisfied",
           "weakness":"no documented weekly review","risk":"Moderate"}
poam = {"item":finding["control"],"milestone":"implement weekly review + evidence",
        "due":"90 days","risk":finding["risk"]}
print("Finding:", finding); print("POA&M:", poam)
PY
```

**Expected result:** an assessment finding converted into a tracked POA&M with a
milestone and due date — the assessment-to-remediation workflow of CGRC Domain 5.

**Negative test:** close a finding without a POA&M or evidence; unremediated
weaknesses must be tracked to closure.

**Cleanup:** none.

### Lab 7.6 — CGRC: System Compliance (14%)

**Objective:** Make the authorization (ATO) decision from residual risk.

```bash
python3 - <<'PY'
open_poams = [("Low",3),("Moderate",1),("High",0)]  # (risk, count)
high = dict(open_poams)["High"]
decision = "ATO granted (residual risk acceptable)" if high==0 else \
           "Denied / ATO with conditions (High risks open)"
print("Open POA&Ms:", dict(open_poams))
print("Authorizing Official decision ->", decision)
PY
```

**Expected result:** with no open High-risk items, an **ATO granted** decision —
the risk-acceptance authorization at the core of CGRC Domain 6.

**Negative test:** grant an unconditional ATO with open High-risk findings; the
Authorizing Official must accept, mitigate, or condition that risk explicitly.

**Cleanup:** none.

### Lab 7.7 — CGRC: Compliance Maintenance (13%)

**Objective:** Define a continuous-monitoring cadence (ongoing authorization).

```bash
python3 - <<'PY'
conmon = {"vulnerability scans":"weekly","control reassessment":"1/3 of controls per year",
          "POA&M review":"monthly","reauthorization":"event-driven or 3-year"}
for k,v in conmon.items(): print(f"{k:22}: {v}")
PY
```

**Expected result:** a continuous-monitoring schedule keeping authorization
current — CGRC Domain 7, which makes authorization ongoing rather than a
point-in-time event.

**Negative test:** authorize once and never revisit; RMF requires continuous
monitoring — configuration drift and new threats erode the original ATO.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CGRC (formerly CAP) is ISC2's governance, risk, and compliance credential for
authorizing systems to operate: seven domains weighted 16/10/14/17/16/14/13
tracing the NIST RMF lifecycle from categorization through continuous
monitoring. It is the process-and-documentation credential for government and
regulated roles, pairing naturally with ISSEP and CISSP Domain 1.

- [ ] I can list the seven CGRC domains and their weights.
- [ ] I can categorize a system and select/tailor its control baseline.
- [ ] I can write an SSP entry, a POA&M, and an ATO decision.
- [ ] I can define a continuous-monitoring cadence.
- [ ] I completed Labs 7.1–7.7 including each negative test.
