# Chapter 09: Certification Prep, Currency, and Career

## Learning Objectives

- Plan the VMCE+ path (required trainings, exam booking, currency).
- Plan the VMCSE path and its prerequisites.
- Migrate from VMCE to VMCE+ before retirement.
- Map a Veeam data-protection career.
- Complete a walkthrough for each prep-and-career topic.

## Theory and Architecture

Earning and keeping Veeam credentials in 2026 follows the new model. For **VMCE+**, complete the **three
required Veeam University Pro trainings** (Backup & Replication: Configure/Manage/Recover; Veeam ONE;
Veeam Recovery Orchestrator — about 55+ hours) **before** booking the **Pearson VUE** exam (100
questions, 150 minutes). For **VMCSE**, hold a valid **VMCE+** and complete the **Enterprise Data
Security** training, then sit the exam when it launches in **Q2 2026**. Holders of the legacy **VMCE**
should migrate to **VMCE+** before the VMCE exam retires on **31 March 2026** (VMCA already retired 30
November 2025). Certifications carry a validity period and are re-earned by passing the current version;
because Veeam ties exams to product versions (VMCE+ = **v13**), plan to re-certify as the platform
advances. A Veeam career ladders from backup administrator to data-protection engineer (VMCE+) to
security/resilience specialist (VMCSE) and architect. This chapter closes the volume with prep,
currency, and career walkthroughs.

## Design Considerations

Budget the **Veeam University Pro** subscription and ~55 hours of coursework before the VMCE+ exam —
training is a **hard requirement**. Sequence **VMCE+ → VMCSE** (VMCE+ is a hard prerequisite). If you
hold **VMCE**, migrate before **31 March 2026**. Track **product-version** alignment (v13) and
re-certify on cadence. Use the free **Community Edition** and hands-on labs to prepare.

## Implementation and Automation

The labs plan the VMCE+ and VMCSE paths, model the VMCE→VMCE+ migration deadline, and map a career — the
progression these credentials support.

## Validation and Troubleshooting

Confirm the prep-and-career plan:

```text
VMCE+: 3 required trainings (~55h, University Pro) BEFORE Pearson VUE exam (100Q/150min) -> Credly
VMCSE: valid VMCE+ + Enterprise Data Security training -> exam Q2 2026
Migrate: VMCE exam ends 31 Mar 2026 (VMCA retired 30 Nov 2025) -> move to VMCE+
Currency: exams tied to product version (VMCE+ = v13); re-certify as platform advances
Career: Backup Admin -> Data-Protection Engineer (VMCE+) -> Security Specialist (VMCSE) -> Architect
```

Common pitfalls: booking VMCE+ before finishing the **required trainings**; and letting a **VMCE**
lapse past 31 March 2026 without migrating to VMCE+.

## Security and Best Practices

Prepare on your own lab (Community Edition), keep backups immutable while you practice, and pursue the
VMCSE to deepen defensive resilience skills. All work is authorized, defensive data protection.

## Hands-On Lab

Prep-and-career walkthroughs. **Shared prerequisites** — `python3` for planning. **Cost:** none.

### Lab 9.1 — Plan the VMCE+ path

**Objective:** Sequence trainings and the exam.

```python
python3 - <<'PY'
steps = [
  "1. Subscribe to Veeam University Pro (via Veeam channel / Authorized Education Center)",
  "2. Complete: Backup & Replication: Configure, Manage, and Recover",
  "3. Complete: Veeam Data Platform: Monitor, Manage, Analyze (Veeam ONE)",
  "4. Complete: Veeam Data Platform: Scale, Automate, Secure (Recovery Orchestrator)",
  "5. Book the VMCE+ exam (Pearson VUE, 100Q / 150min) -> Credly badge",
]
for s in steps:
    print(s)
print("Training (~55h) is a HARD requirement before the exam")
PY
```

**Expected result:** the ordered VMCE+ path — three trainings, then the Pearson VUE exam.

**Negative test:** try to book the exam with no completed trainings; they are a hard prerequisite —
finish them first.

**Cleanup:** none.

### Lab 9.2 — Plan the VMCSE path and migrate from VMCE

**Objective:** Sequence VMCSE and beat the VMCE deadline.

```python
python3 - <<'PY'
from datetime import date
vmce_retires = date(2026, 3, 31)
today = date(2026, 7, 29)
status = "PAST DEADLINE — VMCE exam retired; go straight to VMCE+" if today > vmce_retires else \
         f"{(vmce_retires - today).days} days left to sit VMCE"
print(f"VMCE exam retirement: {vmce_retires} -> {status}")
print("VMCSE path: valid VMCE+  +  Enterprise Data Security training  ->  VMCSE exam (Q2 2026)")
PY
```

**Expected result:** the VMCSE prerequisites and a clear read that VMCE has retired — plan directly for
VMCE+.

**Negative test:** bank on sitting VMCE now; it retired 31 March 2026 — pursue **VMCE+** instead.

**Cleanup:** none.

### Lab 9.3 — Map a Veeam career

**Objective:** Plan progression.

```python
python3 - <<'PY'
ladder = [
  ("Backup Administrator",        "operate jobs, restores (Community/Foundation)"),
  ("Data-Protection Engineer",    "VMCE+ — full Data Platform, replication, SOBR, orchestration"),
  ("Security/Resilience Specialist","VMCSE — immutability, ZTDR, ransomware detection, SCA"),
  ("Data-Protection Architect",   "design enterprise resilience across sites and cloud"),
]
for role, focus in ladder:
    print(f"{role:30}: {focus}")
print("Currency: re-certify as the platform advances (VMCE+ = v13)")
PY
```

**Expected result:** a career ladder from administrator through VMCE+ and VMCSE to architect.

**Negative test:** stop at a lapsed credential on an old product version; re-certify on the current
version to stay current.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The 2026 Veeam path is VMCE+ (three required Veeam University Pro trainings, then a Pearson VUE exam)
rising to VMCSE (valid VMCE+ plus Enterprise Data Security training, Q2 2026), with VMCE holders
migrating before 31 March 2026 — kept current against the v13-aligned platform, laddering a
data-protection career from administrator to architect.

- [ ] I can plan the VMCE+ path and its required trainings.
- [ ] I can plan the VMCSE path and prerequisites.
- [ ] I can plan the VMCE→VMCE+ migration.
- [ ] I can map a Veeam data-protection career.
- [ ] I completed Labs 9.1–9.3 including each negative test.
