# Chapter 09: Certification Prep, Currency, and Career

## Learning Objectives

- Prepare for Salesforce exams with Trailhead.
- Practice hands-on in a free Developer Edition org.
- Maintain certifications across the three annual releases.
- Plan a career across the Salesforce tracks.
- Complete a walkthrough for exam prep and currency.

## Theory and Architecture

Salesforce exams are delivered **online-proctored** (via Kryterion/Webassessor) and combine
**conceptual knowledge** with **applied scenarios**, so preparation must build both. The signature
prep resource is **Trailhead** — Salesforce's free, gamified learning platform with **trails**,
**modules**, and hands-on **Trailhead Playgrounds** — plus **exam guides** (each certification's
official topic breakdown) and a **free Developer Edition org** for real practice. On **currency**:
Salesforce ships **three releases a year** (Spring, Summer, Winter), and certifications are **maintained
by completing free release modules on Trailhead** each cycle — skip them and a certification can
lapse. A Salesforce career is a **pyramid**: start with **Administrator**, branch into **App Builder**,
**Developer**, **Consultant**, or the **Architect** track (toward CTA), and ride the **Agentforce/AI**
wave — the ecosystem rewards stacking credentials. This closing chapter turns the volume into a durable
exam-prep, maintenance, and career plan.

## Design Considerations

Prepare with **Trailhead + exam guide + hands-on** (free Dev org/Playground). Map study to the
certification's **exam guide** weightings. **Maintain** certifications via the free release modules each
cycle. Stack credentials from **Administrator** toward your career direction. Keep learning with the
active **Trailblazer community**.

## Implementation and Automation

The labs plan Trailhead-based prep, verify a free org, and plan currency/career.

## Validation and Troubleshooting

Confirm the prep/currency model:

```text
Exams: online proctored (Kryterion/Webassessor), concepts + applied scenarios. Prepare: Trailhead (trails/modules/Playground) + official exam guide + free Developer Edition org.
Currency: 3 releases/yr; maintain certs via free Trailhead release modules each cycle. Career: pyramid from Administrator -> App Builder/Developer/Consultant/Architect (CTA) + Agentforce/AI.
```

Common pitfalls: studying with no **hands-on** org; and letting a certification **lapse** by skipping
release maintenance.

## Security and Best Practices

Prepare with **Trailhead + exam guide + hands-on**, **maintain** with free release modules, and stack
credentials toward your career. Practice on a **free Dev org**. All practice is authorized.

## Hands-On Lab

Prep and currency walkthroughs. **Shared prerequisites** — `python3`; a free Dev org optional. **Cost:**
none.

### Lab 9.1 — Plan Trailhead-based preparation

**Objective:** Cover concepts and practice.

```python
python3 - <<'PY'
prep={"Trailhead":"trails + modules for the target certification","Exam guide":"official topic weightings -> focus study",
      "Hands-on":"free Developer Edition org / Trailhead Playground: build the features","Superbadges":"applied, scenario-based practice"}
for k,v in prep.items(): print(f"{k:11}: {v}")
PY
```

**Expected result:** a Trailhead prep plan (trails, exam guide, hands-on, superbadges) — balanced
preparation.

**Negative test:** read modules without a **hands-on** org; exams test applied skill — build in a
Playground.

**Cleanup:** none.

### Lab 9.2 — Verify a free practice org

**Objective:** Practice at no cost.

```python
python3 - <<'PY'
free_prep={"org":"free Developer Edition (developer.salesforce.com) — never expires","playground":"Trailhead Playground for guided challenges",
          "cli":"Salesforce CLI (sf) for scratch orgs + deployment practice","cost":"$0"}
for k,v in free_prep.items(): print(f"{k:11}: {v}")
PY
```

**Expected result:** a **free** practice setup — accessible hands-on preparation.

**Negative test:** assume you need a paid org to practice; a **Developer Edition** org is free — use it.

**Cleanup:** none.

### Lab 9.3 — Plan currency and career

**Objective:** Stay current and plan a path.

```python
python3 - <<'PY'
routine={"Maintenance":"complete the free Trailhead release module each of the 3 yearly releases",
         "Track":"new certifications (Agentforce/AI) + exam-guide changes on Trailhead",
         "Practice":"keep a free Developer Edition org","Career":"Administrator -> App Builder/Developer/Consultant -> Architect (CTA) + Agentforce"}
for k,v in routine.items(): print(f"- {k}: {v}")
PY
```

**Expected result:** a currency-and-career routine — release maintenance, tracking, practice, and a
pyramid path.

**Negative test:** skip a **release maintenance** module; the certification lapses — complete it each
cycle.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Salesforce exams are Trailhead-prepared and test concepts plus applied skill, practiced in a free
Developer Edition org; certifications are maintained via free release modules across three annual
releases, so hands-on prep, release maintenance, and credential stacking from Administrator keep you
current.

- [ ] I can plan Trailhead-based preparation.
- [ ] I can verify a free practice org.
- [ ] I can plan release-based currency.
- [ ] I can plan a career across the tracks.
- [ ] I completed Labs 9.1–9.3 including each negative test.
