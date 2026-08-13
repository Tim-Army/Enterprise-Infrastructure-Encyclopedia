# Chapter 09: Certification Prep, Currency, and Career

## Learning Objectives

- Plan preparation with the Datadog Learning Center.
- Register for an exam and manage the retake policy.
- Sequence the certifications into a career path.
- Keep certifications current with the evolving platform.
- Complete a walkthrough for each prep-and-career topic.

## Theory and Architecture

Earning Datadog certifications follows a consistent path. Preparation is **free** through the **Datadog
Learning Center** — self-paced courses, hands-on labs, and **practice exams** aligned to each
certification's domains — plus a **14-day trial** to practice on a live account. Register through the
Learning Center; each exam is **$100** with **90 multiple-choice questions**, and you may retake it up to
**three times within a 180-day** window from your first attempt. Because Datadog **relaunched** the
program on a new platform, confirm the current lineup and any pilot certifications (Database Monitoring,
Cloud SIEM) on datadoghq.com. A Datadog-skilled career ladders from **Datadog Fundamentals** (monitoring
foundation) into **APM** (application performance), **Log Management** (logging), **Database Monitoring**,
and **Cloud SIEM** (security) roles across SRE, DevOps, and observability engineering. This chapter closes
the volume with prep, currency, and career walkthroughs.

## Design Considerations

Prepare with the **free Learning Center** courses and the **practice exam**, on a live **trial** account
(this volume's labs). Start with **Datadog Fundamentals** and add role certifications. Plan your **three
attempts** within the 180-day window. Keep skills **current** as Datadog ships features and refreshes
exams — the platform evolves quickly.

## Implementation and Automation

The labs plan a preparation path, model the exam/retake policy, and map the certifications to a career —
the progression the program supports.

## Validation and Troubleshooting

Confirm prep, currency, and career:

```text
Prep: Datadog Learning Center (free courses + labs + practice exam) on a 14-day trial
Register: via Learning Center; $100; 90 MC; 3 attempts / 180 days from first attempt
Start: Datadog Fundamentals -> APM / Log Management / Database Monitoring / Cloud SIEM
Currency: platform relaunched + evolving -> re-check lineup and refresh skills on datadoghq.com
```

Common pitfalls: skipping the **practice exam** and hands-on trial; and burning the **three attempts**
without preparing between them.

## Security and Best Practices

Practice on your own trial account, protect API/app keys, and apply the security practices throughout
this volume. The Cloud SIEM path is defensive security operations. All work is authorized.

## Hands-On Lab

Prep-and-career walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 9.1 — Plan a preparation path

**Objective:** Sequence free resources to an exam.

```python
python3 - <<'PY'
plan = [
  "1. Start a 14-day Datadog trial (live account)",
  "2. Datadog Learning Center course for the target certification",
  "3. Hands-on labs (this volume's Agent/API/pipeline labs)",
  "4. Take the practice exam; review weak domains",
  "5. Register and sit the exam ($100; 90 questions)",
]
for step in plan: print(step)
PY
```

**Expected result:** a free-first preparation path ending at the exam.

**Negative test:** study slides only with no live account; the exams assume **hands-on** — use the trial
and labs.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — Model the exam and retake policy

**Objective:** Plan attempts within the window.

```python
python3 - <<'PY'
policy = {"cost": "$100", "questions": 90, "type": "multiple choice",
          "attempts": "3 within 180 days from first attempt"}
for k, v in policy.items(): print(f"{k:10}: {v}")
print("Plan: prepare between attempts; don't burn all three in a week")
PY
```

**Expected result:** the exam format and the three-attempts-per-180-days rule — plan attempts
deliberately.

**Negative test:** retake immediately without studying and exhaust attempts; **prepare** between tries.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.3 — Map a Datadog career

**Objective:** Sequence the certifications.

```python
python3 - <<'PY'
ladder = {
  "Datadog Fundamentals":      "monitoring foundation (Agent/metrics/dashboards/monitors)",
  "APM & Distributed Tracing": "application performance / SRE",
  "Log Management":            "logging / observability engineer",
  "Database Monitoring":       "database reliability",
  "Cloud SIEM":                "security operations (defensive)",
}
for cert, arc in ladder.items(): print(f"{cert:26}: {arc}")
print("Currency: program relaunched + evolving -> refresh on datadoghq.com")
PY
```

**Expected result:** the certifications mapped to career arcs across observability and security.

**Negative test:** stop at a lapsed credential as the platform changes; keep skills **current**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Datadog certification prep is free through the Datadog Learning Center — courses, labs, and a practice
exam on a 14-day trial — with exams at $100/90 questions and three attempts per 180 days. Starting at
Datadog Fundamentals and branching into APM, Log Management, Database Monitoring, and Cloud SIEM ladders a
career across SRE, observability, and security, kept current as the relaunched platform evolves.

- [ ] I can plan a preparation path with the Learning Center.
- [ ] I can model the exam and retake policy.
- [ ] I can sequence the certifications into a career.
- [ ] I can keep certifications current with the platform.
- [ ] I completed Labs 9.1–9.3 including each negative test.
