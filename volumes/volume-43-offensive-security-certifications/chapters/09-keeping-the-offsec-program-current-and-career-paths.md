# Chapter 09: Keeping the OffSec Program Current and Career Paths

## Learning Objectives

- Explain the OffSec "+" renewal model and which credentials expire.
- Track program change — the OSCP+ transition, new credentials, and course-code updates.
- Plan an OffSec career path across offense, defense, and AI.
- Relate OffSec credentials to the encyclopedia's security volumes.
- Verify program currency from the authoritative source.

## Theory and Architecture

OffSec now runs a **two-track renewal model**:

- **Renewable ("+") credentials** — **OSCP+**, the **OSCC** (CyberCore) variants,
  **OSTH**, **OSIR**, and **OSAI+** are valid **three years** and renewed through
  the **OffSec CPE program**, a recertification exam, or by passing another
  qualifying OffSec exam.
- **Non-expiring credentials** — the classic **OSCP** (lifetime), the 300-level
  **OSEP/OSWE/OSED**, and the top-tier **OSEE** do **not** expire.

This is a significant, recent change: passing **PEN-200** now grants both the
lifetime **OSCP** and the renewable **OSCP+**, and OffSec has added whole new
tracks (**CyberCore/OSCC**, **AI-300/OSAI**) since older program maps were
written.

## Design Considerations

Plan a path by **direction and depth**. A common route is **Foundational (OSCC,
KLCP) → OSCP+ → specialize**: red-teamers continue to **OSEP/OSWP** and the
**OSCE³** set (OSEP + OSWE + OSED); web specialists take **OSWA → OSWE**; exploit
developers take **OSED → OSEE**; blue-teamers take **OSDA/OSIR/OSTH**; and anyone
working with AI adds **OSAI**. Track which credentials **renew** so they do not
lapse, and treat the **report-writing** skill as career-long — it is what turns
findings into value.

## Implementation and Automation

Verify currency from **offsec.com** — the course catalog carries the current
codes and credentials:

```bash
curl -sSL "https://www.offsec.com/courses/" \
  | grep -oiE '(PEN|WEB|EXP|SOC|IR|TH|SEC|AI|SJD)-[0-9]{3}' | sort -u
```

## Validation and Troubleshooting

Confirm program facts before committing:

```text
offsec.com/courses:
  - current course codes and the credentials they earn
  - which credentials use the "+" three-year renewal vs never expire
  - exam format (practical hours + report) per course
Watch for new tracks (AI-300/OSAI and CyberCore/OSCC are recent additions).
```

Common pitfalls: assuming **OSCP never expires** (the lifetime OSCP still exists,
but **OSCP+** is the renewable one now emphasized); missing new courses
(**AI-300**, **SEC-100/SJD-100**); and letting a **"+"** credential lapse.

## Security and Best Practices

Keep renewable credentials current via **OffSec CPE** or re-exam. Keep practicing
in **authorized labs** with current tooling, and — the throughline of this whole
volume — apply offensive knowledge **ethically and defensively**, always within
authorization. Map your path to the roles you want (red team, blue team, exploit
dev, AI security) rather than collecting credentials for their own sake.

## References and Knowledge Checks

- offsec.com: the course-and-certification catalog, per-course exam guides, the CPE/renewal policy, and the code of conduct.

**Knowledge checks**

1. Which OffSec credentials renew under the "+" model, and which never expire?
2. What recent tracks and changes must you verify against an old program map?
3. What is a sensible path from foundational to expert or to defense?

## Hands-On Lab

Exam-preparation walkthroughs for tracking program change and planning a path.

**Shared prerequisites for Labs 9.1–9.2** — a shell with `curl` and `python3`.
**Cost:** none.

### Lab 9.1 — Verify the current catalog (Topic: Verify currency)

**Objective:** Read the current courses and credentials from the source.

```bash
curl -sSL "https://www.offsec.com/courses/" \
  | grep -oiE '(PEN|WEB|EXP|SOC|IR|TH|SEC|AI|SJD)-[0-9]{3}' | sort -u
```

**Expected result:** the current course codes including **AI-300** (OSAI) and
**SEC-100/SJD-100** (OSCC) — confirming the new tracks an old map would miss.

**Negative test:** trust a pre-2025 OffSec chart; it omits AI-300 and CyberCore
and predates the OSCP+ change — confirm on offsec.com.

**Cleanup:** none.

### Lab 9.2 — Plan a renewal (Topic: Maintain the credential)

**Objective:** Model the "+" three-year renewal for a renewable credential.

```bash
python3 - <<'PY'
from datetime import date
earned = date(2026, 7, 26)                 # OSCP+
expires = earned.replace(year=earned.year + 3)
print(f"OSCP+ earned {earned} -> expires {expires}")
print("Renew by: OffSec CPE program, a recert exam, OR another qualifying OffSec exam.")
print("Note: the lifetime OSCP earned alongside it does NOT expire.")
PY
```

**Expected result:** a three-year expiry and the renewal options, plus the note
that the paired lifetime OSCP does not expire — the "+" model in practice.

**Negative test:** assume every OffSec credential is lifetime; **OSCP+/OSCC/OSTH/
OSIR/OSAI+** renew every three years — track them.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OffSec now runs a two-track renewal model: OSCP+, the OSCC variants, OSTH, OSIR,
and OSAI+ renew every three years (OffSec CPE, re-exam, or another qualifying
exam), while OSCP (lifetime), OSEP/OSWE/OSED, and OSEE do not expire. The program
has grown with new AI (AI-300/OSAI) and foundational (CyberCore/OSCC) tracks.
Plan a path by role — offense, defense, exploit dev, or AI — and always practice
ethically within authorization.

- [ ] I can list which credentials renew and which never expire.
- [ ] I can name the recent tracks (OSAI, OSCC) and the OSCP+ change.
- [ ] I can plan a path from foundational to expert or to defense.
- [ ] I can verify the current catalog on offsec.com.
- [ ] I completed Labs 9.1–9.2 including each negative test.
