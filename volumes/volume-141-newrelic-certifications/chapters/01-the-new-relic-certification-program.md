# Chapter 01: The New Relic Certification Program

![The New Relic certification program: four certifications in a single ladder. The New Relic Verified Foundation, NVF, is free, forty-five minutes, multiple choice, online and unproctored, for candidates with zero to six months of experience. The Certified APM Practitioner Associate, APA, costs one hundred twenty-five dollars, runs fifty minutes, and is online proctored, for candidates with six or more months of experience. Two Professional certifications cost one hundred seventy-five dollars each and run sixty minutes, online proctored, for candidates with two or more years of experience: the Certified Performance Engineer Professional, PEP, covering platform capabilities, backend application performance, client-side performance, and infrastructure and cloud performance; and the Certified Reliability Engineer Professional, REP, covering alerts and incident management, service level management, infrastructure and cloud integration and networking, and automation with New Relic APIs and Terraform. All exams are offered in English, Spanish, Portuguese, and Japanese. Paid exams register through Webassessor; the free NVF is taken on learn.newrelic.com itself. Beneath the ladder sits the platform: MELT telemetry into NRDB, queried with NRQL, with entities, tags, and workloads for organization, and NerdGraph and Terraform for automation.](../../../diagrams/volume-141-newrelic-certifications/chapter-01-certification-program.svg)

*Figure 1-1. Four certifications, one ladder — and the platform beneath them.*

## Learning Objectives

- Describe all four New Relic certifications and their published mechanics.
- Choose an entry point based on experience rather than ambition.
- Know which exam facts New Relic publishes openly and which sit behind a sign-in.
- Set up a free study environment for the labs in this volume.

## What New Relic is

New Relic is one of the original application performance monitoring vendors, grown into a full observability platform. Its architecture is the **single-store** model: agents and integrations send telemetry — metrics, events, logs, traces, the **MELT** four — into **NRDB**, New Relic's telemetry database, and everything above it queries that one store with one language, **NRQL**.

That puts it in a specific position among the platforms this encyclopedia covers: like [Datadog (XC)](../../volume-090-datadog-certifications/README.md) and unlike [Grafana (CXXXIX)](../../volume-139-grafana-observability/README.md), New Relic owns its data; like [Dynatrace (CXL)](../../volume-140-dynatrace-certifications/README.md) it leans on agent auto-instrumentation, but with **NRQL exposed everywhere** — dashboards, alerts, and service levels are all queries, which makes the query language the platform's real center of gravity. Chapter 03 treats it accordingly.

## The program: four certifications, one ladder

New Relic's certification program is small and public. The entire catalog:

| | **NVF** | **APA** | **PEP** | **REP** |
|:---|:---|:---|:---|:---|
| Full name | New Relic Verified Foundation | Certified APM Practitioner – Associate | Certified Performance Engineer – Professional | Certified Reliability Engineer – Professional |
| Level | Foundation | Associate | Professional | Professional |
| Cost | **Free** | $125 USD | $175 USD | $175 USD |
| Duration | 45 min | 50 min | 60 min | 60 min |
| Format | Multiple choice | Multiple choice | Multiple choice | Multiple choice |
| Delivery | Online, **unproctored** | Online proctored | Online proctored | Online proctored |
| Languages | EN, ES, PT, JA | EN, ES, PT, JA | EN, ES, PT, JA | EN, ES, PT, JA |
| Recommended experience | 0–6 months | 6+ months | 2+ years | 2+ years |

Three structural observations:

1. **The on-ramp is genuinely free and unproctored.** The NVF has no prerequisites and no fee — New Relic's blog describes the Foundation tier as unproctored "allowing participants to complete them with greater flexibility," with proctoring reserved for Associate and Professional. That is a deliberate funnel design: zero friction at the bottom, verification where the credential carries weight.
2. **The two Professional certifications are siblings, not a sequence.** PEP is the *performance* track — backend, client-side, infrastructure performance. REP is the *reliability* track — alerting, service levels, automation. Same level, same price, different jobs. Chapter 09 helps you pick.
3. **There is no Expert tier.** The ladder tops out at Professional. Anyone selling "New Relic Expert certification" prep is selling something New Relic does not offer.

Paid exams are registered and delivered through **Webassessor** (`webassessor.com/newrelic`); the NVF is taken on `learn.newrelic.com` itself. All four exams publish their **section-level topics** on public pages — those topic lists are the blueprints this volume is organized around, and they are quoted in the relevant chapters.

## What is public and what is not

New Relic's disclosure posture is the opposite of the one documented in [Volume CXL](../../volume-140-dynatrace-certifications/README.md). Where Dynatrace University gates everything behind a sign-in, New Relic puts level, cost, duration, format, proctoring, languages, experience guidance, and per-section exam topics on public pages, with free prep courses and a downloadable program guide beside them.

Two things are *not* on the public pages, and the same discipline applies as everywhere else in this encyclopedia:

> **Question count and passing score live in the per-exam Exam Guides, which sit behind a free sign-in. No validity or expiration policy is stated on any public page.** This volume asserts none of these. Get them from the Exam Guide for your exam, and treat any third-party source stating them as unverified.

The honest summary: New Relic publishes roughly everything a candidate needs to *decide*, and keeps the details a candidate needs to *sit the exam* one free registration away. That is a much better deal than most vendors offer, and it still leaves numbers you should refuse to take from a search result.

## Hands-On Lab

The labs in this volume model New Relic concepts in Python at zero cost. New Relic also offers a free account tier — genuinely useful for practice, since every exam topic list assumes you have driven the platform.

### Lab 1.1 — The program at a glance

**Objective:** Encode the published mechanics and test your entry point.

```bash
python3 - <<'EOF'
CERTS = {
  "NVF": {"level":"Foundation","cost":0,"minutes":45,"proctored":False,"exp_months":(0,6)},
  "APA": {"level":"Associate","cost":125,"minutes":50,"proctored":True,"exp_months":(6,24)},
  "PEP": {"level":"Professional","cost":175,"minutes":60,"proctored":True,"exp_months":(24,999)},
  "REP": {"level":"Professional","cost":175,"minutes":60,"proctored":True,"exp_months":(24,999)},
}
print(f"{'cert':6}{'level':14}{'cost':>7}{'mins':>6}{'proctored':>11}   recommended experience")
for c, d in CERTS.items():
    lo, hi = d["exp_months"]
    exp = f"{lo}+ months" if hi == 999 and lo < 24 else (f"{lo//12}+ years" if lo >= 24 else f"{lo}-{hi} months")
    print(f"{c:6}{d['level']:14}{'FREE' if d['cost']==0 else '$'+str(d['cost']):>7}"
          f"{d['minutes']:>6}{'yes' if d['proctored'] else 'NO':>11}   {exp}")

my_months = 14   # <- your experience with New Relic, in months
eligible = [c for c, d in CERTS.items() if d["exp_months"][0] <= my_months]
print(f"\nAt {my_months} months of experience, the recommendation bands point at: {', '.join(eligible)}")
print("Professional certs recommend 2+ years — 'recommend' is not 'require', but the")
print("bands exist because the exams are written against that much platform exposure.")
print("\nTotal cost of the full ladder, NVF through one Professional: "
      f"${CERTS['APA']['cost'] + CERTS['PEP']['cost']} — the Foundation tier is free.")
print("There is NO Expert tier. The ladder tops out at Professional.")
EOF
```

**Expected result:** A table matching the published program exactly, with a 14-month candidate pointed at NVF and APA. The closing lines carry the two facts worth retaining: the whole ladder costs $300 because the entry tier is free, and the ladder has no Expert rung for anyone to sell you.

**Negative test:** Booking a Professional exam at six months of experience because the fee is affordable. The experience bands describe what the exam assumes, not what the checkout page enforces.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Record what is published and what is not

**Objective:** Build the study plan on verified ground.

```bash
cat > my-newrelic-plan.md <<'EOF'
PUBLISHED ON PUBLIC PAGES (verified 4 Aug 2026, learn.newrelic.com):
  catalog     NVF (free) -> APA ($125) -> PEP / REP ($175 each)
  mechanics   duration, format (multiple choice), proctoring, languages (EN/ES/PT/JA)
  topics      per-section exam topics for ALL FOUR exams  <- the blueprint
  prep        free prep courses, learning paths, exam readiness kit, program guide
  delivery    Webassessor for paid exams; NVF taken on learn.newrelic.com

BEHIND FREE SIGN-IN (Exam Guide PDFs):
  [ ] question count      [ ] passing score

NOT FOUND ON ANY PUBLIC PAGE:
  [ ] validity / expiration period      [ ] retake policy
  -> do not accept these from third parties; check the Exam Guide and FAQ

MY TARGET:  ______        WHY:  ____________________
PRACTICE:   free New Relic account; every exam assumes real platform time
EOF
cat my-newrelic-plan.md && rm my-newrelic-plan.md
```

**Expected result:** A plan with three tiers of confidence — public, sign-in-gated, and unknown — rather than one undifferentiated list of "facts." The habit this builds is the one that has paid off across this whole shelf of volumes: track *where* each claim comes from, because exam details are exactly what braindump sites invent most confidently.

**Negative test:** Copying a question count from a practice-exam site. New Relic put it behind a sign-in; a third party quoting it either registered (and is republishing gated material) or guessed.

**Rollback:** The plan file is removed at the end of the script; keep a copy if you want it.

## Summary and Completion Checklist

- [ ] All four certifications and their published mechanics described.
- [ ] NVF understood as free, unproctored, and prerequisite-free by design.
- [ ] PEP and REP recognized as sibling tracks, not a sequence — and no Expert tier exists.
- [ ] Question count, passing score, and validity identified as not publicly published.
- [ ] MELT, NRDB, and NRQL placed at the center of the platform.
