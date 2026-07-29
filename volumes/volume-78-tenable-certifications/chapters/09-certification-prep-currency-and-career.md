# Chapter 09: Certification Prep, Currency, and Career

## Learning Objectives

- Prepare for the two-part (written + practical) Tenable exams.
- Practice the hands-on skills the practical validates.
- Keep credentials current across the two-year cycle.
- Plan a career in vulnerability and exposure management.
- Complete a walkthrough for exam prep and currency.

## Theory and Architecture

Tenable certifications require passing **both** a written and a practical exam, so preparation must
cover **knowledge and hands-on skill**. The **written** exam (60 MCQ, 120 min, 80%) tests concepts —
scanning, prioritization (CVSS/VPR/AES), platform architecture, and workflows. The **practical** (up
to 30 tasks, 240 min, 80%) tests the ability to actually **plan, deploy, verify, and troubleshoot**
in the product; it permits access to the **pyTenable/developer API documentation**, so knowing where
to find things matters. Effective prep combines the **instructor-led course**, the **product
documentation** (docs.tenable.com), and **hands-on practice** in a real product instance (Nessus
Essentials and a trial/lab tenant). On **currency**: certifications are valid **two years** and
renewed by retaking both parts, and the platform evolves toward **Tenable One** exposure management,
so tracking tenable.com is ongoing. This closing chapter turns the volume into a durable exam-prep,
renewal, and career plan.

## Design Considerations

Study for **both** exam parts — don't neglect the practical. Get **hands-on** time in a real instance.
Know the **API docs** you may reference. Schedule **renewal** before the two-year expiry. Follow the
platform's move to **exposure management**. Match certifications to your **career** direction (VM →
Security Center → OT → exposure lead).

## Implementation and Automation

The labs plan exam prep, drill a practical skill, and plan currency/career.

## Validation and Troubleshooting

Confirm the prep/currency map:

```text
Exam: written (60 MCQ, 120 min, 80%) + practical (up to 30 tasks, 240 min, 80%, API docs allowed). Prepare: course + docs + hands-on.
Currency: valid 2 years, retake both to recertify. Platform trending to Tenable One exposure management. Track tenable.com.
```

Common pitfalls: studying only concepts and failing the **practical**; and letting a cert **lapse**
past two years.

## Security and Best Practices

Prepare for **both** exam parts with **hands-on** practice, know the **API docs**, renew before
expiry, and track the platform's exposure-management direction. Practice on **authorized** targets.
All work is defensive.

## Hands-On Lab

Prep and currency walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none.

### Lab 9.1 — Plan two-part exam preparation

**Objective:** Cover knowledge and skill.

```python
python3 - <<'PY'
prep={"Written":"course + docs: scanning, CVSS/VPR/AES, architecture, workflows",
      "Practical":"hands-on in Nessus Essentials + trial tenant: build scan, prioritize, report, troubleshoot",
      "API docs":"familiarize with pytenable.readthedocs.io / developer.tenable.com (allowed in practical)"}
for k,v in prep.items(): print(f"{k:9}: {v}")
PY
```

**Expected result:** a prep plan covering **both** exam parts and the API docs — balanced
preparation.

**Negative test:** cram MCQs only; the **practical** requires real product skill — practice
hands-on.

**Cleanup:** none.

### Lab 9.2 — Drill a practical skill

**Objective:** Rehearse an exam-style task.

```python
python3 - <<'PY'
task="Configure a credentialed weekly scan of 10.10.0.0/24, then export the top-10 by VPR"
steps=["create scan (Advanced template)","add authorized target + scan credentials",
       "schedule weekly","run + wait","sort findings by VPR desc","export top 10"]
for i,s in enumerate(steps,1): print(f"{i}. {s}")
print("Practical: perform end-to-end tasks under time pressure -> rehearse them")
PY
```

**Expected result:** an exam-style **practical task** broken into steps — hands-on rehearsal.

**Negative test:** read about scanning without ever building one; the **practical** is hands-on —
rehearse real tasks.

**Cleanup:** none.

### Lab 9.3 — Plan currency and career

**Objective:** Keep credentials and skills current.

```python
python3 - <<'PY'
routine={"Validity":"2 years — retake both parts to recertify",
         "Platform":"track Tenable One / exposure-management changes on tenable.com",
         "Practice":"keep a Nessus Essentials + trial for hands-on",
         "Career":"VM -> Security Center -> OT Exposure -> exposure-management lead"}
for k,v in routine.items(): print(f"- {k}: {v}")
PY
```

**Expected result:** a currency-and-career routine — renewal, platform tracking, practice, and a path.

**Negative test:** let a cert lapse past **two years**; it's no longer current — recertify ahead of
expiry.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Tenable certifications require both a written and a practical exam, so prep combines concepts and
hands-on skill; certifications renew on a two-year cycle as the platform moves toward exposure
management — so balanced prep, hands-on practice, and timely renewal keep you current.

- [ ] I can plan two-part exam preparation.
- [ ] I can drill a practical skill.
- [ ] I can plan two-year renewal.
- [ ] I can plan a career in exposure management.
- [ ] I completed Labs 9.1–9.3 including each negative test.
