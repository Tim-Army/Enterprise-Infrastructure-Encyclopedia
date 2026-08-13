# Chapter 07: Exam Preparation

## Learning Objectives

- Plan preparation across the four PSDGP content areas.
- Pace the 100-question, 90-minute proctored exam.
- Practice scenario-style reasoning that maps deliverables to drivers and law.
- Build a personal readiness checklist.
- Complete a walkthrough for each preparation sub-topic.

## Theory and Architecture

The PSDGP exam is **100 questions in 90 minutes**, timed and proctored at a third-party
center. It is a **governance and policy** exam, not a technical one: expect scenario questions
that ask which **deliverable**, **role**, or **legal obligation** applies to a public-sector
situation. Preparation is therefore about reasoning across the four content areas together —
given a scenario (a FOIA request, a data-sharing proposal, a quality failure), identify the
driver, the deliverable, the role, and the law. The R2C/Buchanan & Edwards three-day course is
the primary study path; this volume's Chapters 02–06 map to the blueprint.

## Design Considerations

Study by **scenario**, not by flashcard. Drill the mappings: driver → deliverable → role → law.
Pace at **~0.9 minutes per question**; flag and return rather than stalling. Use the
prerequisite check (Chapter 01) early so eligibility never blocks scheduling.

## Implementation and Automation

The labs build a blueprint-coverage tracker, an exam pacing plan, and a scenario drill.

## Validation and Troubleshooting

Confirm exam mechanics:

```text
100 questions / 90 minutes / proctored / third-party center / no membership required.
Style: scenario mapping across Mission Drivers, Deliverables, Roles, Legal & Regulatory.
Pace: ~0.9 min/question; flag-and-return.
```

Common pitfalls: preparing for a **technical** exam; and running out of time by not pacing.

## Security and Best Practices

Keep preparation grounded in the **authoritative content areas** (ther2c.com) and real
public-sector law — not third-party dumps. Practice the privacy-vs-openness and
retention-vs-deletion tensions, which recur in scenarios.

## Hands-On Lab

Exam-prep walkthroughs. **Shared prerequisites for Labs 7.1–7.3** — a shell with `python3`.
**Cost:** none.

### Lab 7.1 — Blueprint-coverage tracker

**Objective:** Track readiness across the four areas.

```python
python3 - <<'PY'
coverage={"Mission Drivers":0.9,"Deliverables":0.8,"Roles & Responsibilities":0.85,
          "Legal & Regulatory":0.7}
weak=[a for a,c in coverage.items() if c<0.8]
for a,c in coverage.items(): print(f"{a:26} {int(c*100)}%")
print("focus next:",weak or "none")
PY
```

**Expected result:** a per-area readiness score flagging the **weakest area** (Legal &
Regulatory) — where to study next.

**Negative test:** study only your strongest area; the exam spans **all four** — target the
weakest.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.2 — Exam pacing plan

**Objective:** Budget time across 100 questions.

```python
python3 - <<'PY'
q,minutes=100,90
per=minutes/q
checkpoints={25:round(25*per),50:round(50*per),75:round(75*per),100:minutes}
print(f"pace: {per:.2f} min/question")
for at,elapsed in checkpoints.items(): print(f"by Q{at}: ~{elapsed} min elapsed")
PY
```

**Expected result:** checkpoints (~22/45/67/90 min) — a pacing plan that finishes on time.

**Negative test:** spend five minutes on one hard question; at **0.9 min/question** that costs
five others — flag and return.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 7.3 — Scenario drill

**Objective:** Map a scenario across all four areas.

```python
python3 - <<'PY'
scenario="A citizen files a FOIA request for a dataset containing SSNs."
answer={"driver":"Transparency & accountability","deliverable":"Catalog + redaction workflow",
        "role":"Records/FOIA Officer + Privacy Officer","law":"FOIA (disclose) vs Privacy Act (protect PII)"}
print("Scenario:",scenario)
for k,v in answer.items(): print(f"  {k:11}: {v}")
PY
```

**Expected result:** a four-part mapping (driver/deliverable/role/law) with the **FOIA-vs-
Privacy** tension resolved by redaction — the reasoning the exam rewards.

**Negative test:** answer "just release it"; PII triggers the **Privacy Act** — redact before
disclosing.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The PSDGP exam is a 100-question, 90-minute proctored, scenario-based governance exam. Prepare
by drilling the driver → deliverable → role → law mapping across all four content areas, pace at
~0.9 minutes per question with flag-and-return, and target your weakest area.

- [ ] I can describe the exam format and style.
- [ ] I can track blueprint coverage and find my weak area.
- [ ] I can pace 100 questions in 90 minutes.
- [ ] I can map a scenario across all four content areas.
- [ ] I completed Labs 7.1–7.3 including each negative test.
