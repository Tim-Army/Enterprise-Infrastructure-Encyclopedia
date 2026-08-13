# Chapter 01: The Veeam Certification Program

## Learning Objectives

- Describe the 2026 Veeam certification transition (VMCE → VMCE+, retired VMCA, coming VMCSE).
- Explain the required-training model and Veeam University Pro.
- Explain exam delivery (Pearson VUE), format, and Credly badges.
- Place VMCE+ and VMCSE on the ladder with the Veeam Data Platform.
- Complete a walkthrough for each program-orientation topic.

## Theory and Architecture

The **Veeam** certification program was rebuilt for 2026 around the **Veeam Data Platform** and **Veeam
Backup & Replication v13**. The long-standing **VMCE (Veeam Certified Engineer)** exam is being retired —
available only through **31 March 2026** — and the **VMCA (Veeam Certified Architect)** was **retired on
30 November 2025**. In their place:

- **VMCE+ (Veeam Certified Engineer Plus)** — the new flagship, **live now** and the first certification
  aligned to **v13**. It validates advanced expertise managing and optimizing enterprise data
  protection across the Veeam Data Platform. The exam is **100 multiple-choice questions in 150 minutes**
  (an extra 30 minutes if English is not your first language), delivered **proctored through Pearson
  VUE (Pearson Professional Assessments)**, with a **Credly** digital badge on passing.
- **VMCSE (Veeam Certified Security Expert)** — arriving **Q2 2026**, focused on cyber resilience. It
  **requires a valid VMCE+** plus the **Enterprise Data Security** training.

A distinctive feature is that **attending the required trainings is a hard prerequisite** to sit the
exam — you must complete them before scheduling. Those trainings are delivered through a **Veeam
University Pro** subscription (sold through the Veeam channel and Authorized Education Centers, not
directly). VMCE+ requires three courses — **Veeam Backup & Replication: Configure, Manage, and Recover**;
**Veeam Data Platform: Monitor, Manage, Analyze (Veeam ONE)**; and **Veeam Data Platform: Scale,
Automate, Secure (Veeam Recovery Orchestrator)** — about 55+ hours in total. This chapter orients you on
the program using a free **Veeam Backup & Replication Community Edition** server and its PowerShell
module so the credentials map to real operations.

## Design Considerations

If you hold **VMCE**, plan your move to **VMCE+** — the v13-aligned successor — before VMCE retires on
31 March 2026. Because training is a **hard requirement**, budget the Veeam University Pro subscription
and the ~55 hours of coursework before booking the exam. Sequence toward **VMCSE** only after VMCE+.
Study against **v13** and the **Veeam Data Platform** (not just Backup & Replication).

## Implementation and Automation

The labs connect to a Veeam backup server with PowerShell, read the product version and edition, and
map the certification ladder — the orientation a VMCE+ candidate needs before the deeper chapters.

## Validation and Troubleshooting

Confirm the program map:

```text
Retired:  VMCA (30 Nov 2025); VMCE exam ends 31 Mar 2026
Flagship: VMCE+ (live, v13-aligned) -> VMCSE (Q2 2026, requires VMCE+ + Enterprise Data Security)
Exam:     VMCE+ = 100 MCQ / 150 min (+30 for non-native EN); Pearson VUE proctored; Credly badge
Training: HARD requirement via Veeam University Pro (3 courses for VMCE+, ~55h)
Platform: Backup & Replication v13 + Veeam ONE + Recovery Orchestrator + Data Cloud
```

Common pitfalls: booking the **VMCE+** exam before completing the required **trainings** (they are a
hard prerequisite); and studying the retired **VMCE**/v12 material instead of **VMCE+**/v13.

## Security and Best Practices

Veeam certifications validate the ability to protect and recover **your own** data. Treat the lab
backup server as production-adjacent: use RBAC, protect credentials, and keep backups immutable
(Chapter 08). All work in this volume is authorized, defensive data protection.

## Hands-On Lab

Program-orientation walkthroughs. **Shared prerequisites** — a free **Veeam Backup & Replication
Community Edition** server reachable via the **Veeam PowerShell module** (`Connect-VBRServer`), and
`python3` for ladder planning. **Cost:** none (Community Edition is free).

### Lab 1.1 — Connect and read the product version

**Objective:** Confirm the Veeam Data Platform version the exams assume.

```powershell
PS> Connect-VBRServer -Server localhost
PS> Get-VBRServerSession | Select-Object Server, Build

Server     Build
------     -----
localhost  13.0.0.4967
```

**Expected result:** a connected session on Veeam Backup & Replication **v13** — the platform VMCE+
aligns to.

**Negative test:** study against v12/VMCE material; VMCE+ is **v13** — confirm the build and use v13
content.

**Rollback:**

```powershell
PS> Disconnect-VBRServer
```

### Lab 1.2 — Map the certification ladder

**Objective:** Reason about the 2026 credentials and their prerequisites.

```python
python3 - <<'PY'
ladder = {
  "VMCA (Architect)": "RETIRED 30 Nov 2025",
  "VMCE (Engineer)":  "legacy; exam ends 31 Mar 2026",
  "VMCE+ (Engineer Plus)": "LIVE, v13-aligned flagship; 3 trainings required",
  "VMCSE (Security Expert)": "Q2 2026; requires VMCE+ + Enterprise Data Security training",
}
for cert, status in ladder.items():
    print(f"{cert:24}: {status}")
print("Rule: VMCE holders -> move to VMCE+ before 31 Mar 2026; VMCSE builds on VMCE+")
PY
```

**Expected result:** the ladder with VMCA retired, VMCE ending, VMCE+ live, and VMCSE requiring VMCE+.

**Negative test:** plan to sit **VMCSE** without **VMCE+**; VMCE+ is a hard prerequisite — earn it first.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Confirm the edition and training path

**Objective:** Read the licensed edition and required trainings.

```powershell
PS> Get-VBRInstalledLicense | Select-Object Edition, Status

Edition    Status
-------    ------
Community  Valid
```

```python
python3 - <<'PY'
vmce_plus = [
  "Veeam Backup & Replication: Configure, Manage, and Recover",
  "Veeam Data Platform: Monitor, Manage, Analyze (Veeam ONE)",
  "Veeam Data Platform: Scale, Automate, Secure (Veeam Recovery Orchestrator)",
]
for i, course in enumerate(vmce_plus, 1):
    print(f"Training {i}: {course}")
print("All three (~55h, Veeam University Pro) are required before the VMCE+ exam")
PY
```

**Expected result:** the Community edition confirmed and the three required VMCE+ trainings listed.

**Negative test:** assume any single course qualifies you; **all three** trainings are required for
VMCE+ — complete the full path.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Veeam's 2026 program retired VMCA and is retiring VMCE (31 March 2026) in favor of the v13-aligned
**VMCE+** flagship and the coming **VMCSE** security expert. Both require attending Veeam University Pro
trainings before the Pearson VUE exam, and both validate protecting data across the Veeam Data Platform
(Backup & Replication, Veeam ONE, Recovery Orchestrator).

- [ ] I can describe the VMCE→VMCE+ transition and the retired VMCA.
- [ ] I can explain the required-training model and Veeam University Pro.
- [ ] I can explain the VMCE+ exam format and Credly badges.
- [ ] I completed Labs 1.1–1.3 including each negative test.
