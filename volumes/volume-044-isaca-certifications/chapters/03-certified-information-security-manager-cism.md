# Chapter 03: Certified Information Security Manager (CISM)

## Learning Objectives

- Explain what CISM certifies and how it differs from CISA and CISSP.
- List the four CISM domains and their exam weights.
- Apply security-management thinking: governance, risk, program, and incidents.
- Relate CISM to business objectives and executive communication.
- Complete a per-domain walkthrough for each CISM domain.

## Theory and Architecture

The **Certified Information Security Manager (CISM)** certifies the **management**
of an information security program — governing it, managing its risks, building
and running it, and handling incidents. Where **CISA** audits and **CISSP** spans
the broad technical body of knowledge, **CISM** is squarely about **leading**
security as a business function. The exam is **150 questions** across four
weighted domains:

| # | Domain | Weight |
|---|--------|--------|
| 1 | Information Security Governance | 17% |
| 2 | Information Security Risk Management | 20% |
| 3 | Information Security Program | 33% |
| 4 | Incident Management | 30% |

**Program (33%)** and **Incident Management (30%)** dominate — building/running
the program and responding to incidents are the core of the manager's job.

## Design Considerations

CISM is a **management** exam: the best answer aligns security with **business
objectives**, manages **risk** to an acceptable level, and communicates to
**executives** in business terms. Study Domain 3 (Program) and Domain 4 (Incident
Management) most heavily. CISM pairs with **CRISC** (risk depth), **CGEIT**
(governance depth), and the ISC2 **CISSP/ISSMP** management view.

## Implementation and Automation

The labs below model the manager's artifacts: a security strategy tied to
business goals (D1), a risk-treatment decision (D2), a program metric/roadmap
(D3), and an incident-management plan with severity and communication (D4).

## Validation and Troubleshooting

Confirm the CISM blueprint before studying:

```text
isaca.org > Credentialing > CISM > Exam Content Outline:
  - four domains and weights (17/20/33/30), 150 questions
  - five years of infosec management experience (waivers available)
```

Common pitfalls: choosing the most **technical** answer instead of the
**management** one; under-weighting **Program** and **Incident Management**; and
confusing CISM (manage the program) with CISA (audit it) or CRISC (quantify and
treat risk).

## Security and Best Practices

Tie every control and initiative to a **business objective** and a **risk
decision**; report to leadership with **metrics** (KRIs/KPIs) and cost/benefit;
maintain an **incident-management plan** rehearsed before it is needed; and align
to recognized frameworks. Renew via CPE and the annual maintenance fee.

## References and Knowledge Checks

- isaca.org: *CISM* Exam Content Outline and review manual.

**Knowledge checks**

1. Which two CISM domains dominate the exam?
2. Why is the "best" CISM answer usually a management decision?
3. How does CISM differ from CISA and CRISC?

## Hands-On Lab

Per-topic walkthroughs — **one lab for every weighted CISM domain**.

**Shared prerequisites** — a Linux shell with `python3`. **Cost:** none.

### Lab 3.1 — CISM D1: Information Security Governance (17%)

**Objective:** Align a security strategy with business goals.

```bash
python3 - <<'PY'
goals = {"Expand to EU market":"GDPR-ready privacy + data residency",
         "Launch mobile app":"secure SDLC + app security program",
         "Reduce fraud":"fraud analytics + stronger authentication"}
for goal,sec in goals.items(): print(f"Business goal: {goal:22} -> security strategy: {sec}")
PY
```

**Expected result:** business goals each driving a security-strategy element —
the governance alignment CISM Domain 1 expects.

**Negative test:** build a security strategy with no link to business goals;
governance ties security to **enterprise objectives**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.2 — CISM D2: Information Security Risk Management (20%)

**Objective:** Make a risk-treatment decision from exposure and cost.

```bash
python3 - <<'PY'
def treat(ale, cost):
    if cost < ale*0.5: return "MITIGATE"
    if ale < 10000: return "ACCEPT"
    return "TRANSFER or AVOID"
for name,ale,cost in [("Ransomware",120000,25000),("Minor defacement",4000,30000)]:
    print(f"{name:18} ALE ${ale:,} cost ${cost:,} -> {treat(ale,cost)}")
PY
```

**Expected result:** ransomware → MITIGATE, minor defacement → ACCEPT — the
risk-treatment decisions a security manager owns (Domain 2).

**Negative test:** mitigate every risk regardless of cost; treatment is an
**economic** decision balanced against exposure.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.3 — CISM D3: Information Security Program (33%)

**Objective:** Define program metrics and a maturity roadmap.

```bash
python3 - <<'PY'
metrics = {"% critical patches <7 days":"92% (target 95%)",
           "MFA coverage":"78% (target 100%)",
           "Phishing failure rate":"6% (target <3%)"}
for m,v in metrics.items(): print(f"{m:32}: {v}")
print("Roadmap: close MFA gap -> raise patch SLA -> reduce phishing via training.")
PY
```

**Expected result:** program KPIs with targets and a roadmap — the program
management that is CISM's largest domain (Domain 3).

**Negative test:** run a program with no metrics; you cannot manage or report what
you do not measure — define KPIs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 3.4 — CISM D4: Incident Management (30%)

**Objective:** Classify an incident and set the response/communication.

```bash
python3 - <<'PY'
def sev(impact, spread):
    s = impact*spread
    band = "SEV1" if s>=12 else "SEV2" if s>=6 else "SEV3"
    comms = {"SEV1":"exec + legal + comms now","SEV2":"management update","SEV3":"team log"}
    return band, comms[band]
for name,i,sp in [("Ransomware on file server",4,4),("Single phished mailbox",3,2)]:
    b,c = sev(i,sp); print(f"{name:28} -> {b}, comms: {c}")
PY
```

**Expected result:** severity classification and matching communication — the
incident-management decision-making of Domain 4.

**Negative test:** treat every incident as SEV1; over-escalation causes fatigue —
classify by impact and spread, then communicate accordingly.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CISM certifies the management of an information security program: four domains
weighted 17/20/33/30, dominated by program management and incident management. Its
throughline is aligning security with business objectives, managing risk, and
communicating to executives — the manager's counterpart to CISA's audit view and
CISSP's technical breadth.

- [ ] I can list the four CISM domains and their weights.
- [ ] I can align a security strategy to business goals.
- [ ] I can make a risk-treatment decision and define program KPIs.
- [ ] I can classify an incident and set its communication.
- [ ] I completed Labs 3.1–3.4 including each negative test.
