# Chapter 09: Choosing a Certification, Currency, and Career

## Learning Objectives

- Choose between the four certifications — especially between the sibling Professionals.
- Prepare from the published topic lists and free official courses.
- Place New Relic among the encyclopedia's other observability volumes.
- Stay current with a young program that is still growing.

## Choosing

| If you… | Take | Why |
|:---|:---|:---|
| Are new to New Relic (0–6 months) | **NVF** | Free, unproctored, no prerequisites — there is no reason not to |
| Work in APM daily (6+ months) | **APA** | The practitioner credential for the platform's core use case |
| Own performance — backend, frontend, infrastructure | **PEP** | The performance track |
| Own reliability — alerting, SLOs, automation | **REP** | The reliability track |

**PEP versus REP is a job-description question, not a difficulty question.** Same level, same price, same duration. Read the section lists side by side: PEP's spine is *performance* (backend, client-side, infrastructure); REP's is *operating reliably* (alerts, service levels, automation). If your week is spent making things fast, PEP describes it; if it is spent keeping promises and reducing noise, REP does. Engineers who genuinely do both usually feel which chapters of this volume were "their" chapters — 04–06 point to PEP, 07–08 to REP.

And take the NVF regardless of seniority if you are new to *this platform*: it is free, it calibrates you against the platform's vocabulary, and an unproctored 45-minute exam is the cheapest possible diagnostic of what you skimmed.

## Preparing

New Relic's publication posture makes preparation unusually straightforward:

1. **The section-level topic lists are public** for all four exams — they are quoted at the top of Chapters 02–08, and they are the blueprint.
2. **The official prep is free**: per-exam prep courses, certification learning paths, an exam readiness kit, and a downloadable program guide.
3. **Question count and passing score are in the per-exam Exam Guide**, behind a free sign-in. Read the guide for your exam; do not take those numbers from anywhere else.
4. **Practice on a free account.** Every topic list assumes platform time — "visualizing insights" and "advanced tuning" are things you have done, not read.

The exams are multiple choice, 45–60 minutes, in English, Spanish, Portuguese, or Japanese; the paid three are proctored through Webassessor. No validity or expiration policy appears on the public pages — check the current Exam Guide and FAQ rather than assuming either way.

## Where New Relic sits in the encyclopedia

This volume completes a four-platform observability set, and the axis positions matter more than any ranking:

| Volume | Model | Certification posture |
|:---|:---|:---|
| **CXLI New Relic** (this one) | Single store (NRDB), one language (NRQL) everywhere | **4 certs, small and fully public** — free on-ramp |
| [**CXL Dynatrace**](../../volume-140-dynatrace-certifications/README.md) | Single agent, causal AI, automation over assembly | 34 badges, mechanics unpublished, sign-in gated |
| [**XC Datadog**](../../volume-090-datadog-certifications/README.md) | SaaS, owns its data, breadth of integrations | Relaunched product-scoped certs, $100 each |
| [**CXXXIX Grafana**](../../volume-139-grafana-observability/README.md) | Queries data where it lives; you assemble the stack | Free badges, not certifications |

The New Relic-specific claims worth carrying out of this volume: **events as first-class telemetry** (per-occurrence questions stay answerable because attributes were kept), and **one query language as the entire configuration surface** — which cuts both ways, as Lab 3.3 showed. Against Dynatrace specifically, the certification-program contrast is almost comic: four public certifications versus thirty-four badges behind a sign-in. Neither posture says anything about the platforms' quality; both say a great deal about how easily you can verify a claim about them.

Deeper foundations: [Prometheus (LV)](../../volume-055-prometheus/README.md) and [OpenTelemetry (LIV)](../../volume-054-opentelemetry/README.md) — New Relic ingests OTel natively, so instrumentation skills transfer in. The SRE discipline REP examines is the vendor-neutral content of [Volume XI](../../volume-011-observability-enterprise-operations/README.md).

## Currency

- **The program is young and small.** Four certifications with room to grow — new certifications or an Expert tier would be unsurprising. Re-check `learn.newrelic.com/page/certifications` before planning; a program this size can change shape in one announcement.
- **The NVF registration moved once already** (onto learn.newrelic.com itself) — registration mechanics are the most perishable facts here.
- **Topic lists are versioned implicitly.** The section lists quoted in this volume are the verification-date snapshot; the platform ships continuously and the exams track it.
- **Verified 4 August 2026** from learn.newrelic.com (certifications overview + all four exam detail pages, public) and New Relic's program blog. Question count, passing score, validity, and retake policy were not on public pages and are not asserted anywhere in this volume.

## Hands-On Lab

### Lab 9.1 — PEP or REP, decided by your calendar

**Objective:** Let the work choose the track.

```bash
python3 - <<'EOF'
WEEK = {                              # hours/week, honestly
  "profiling and fixing slow endpoints":        7,
  "frontend performance / Core Web Vitals":     3,
  "capacity and infrastructure performance":    4,
  "alert tuning and noise reduction":           6,
  "SLO definition, attainment reviews":         5,
  "Terraform / NerdGraph fixture management":   4,
  "incident response and postmortems":         5,
}
PEP_ITEMS = ["profiling and fixing slow endpoints",
             "frontend performance / Core Web Vitals",
             "capacity and infrastructure performance"]
REP_ITEMS = ["alert tuning and noise reduction",
             "SLO definition, attainment reviews",
             "Terraform / NerdGraph fixture management",
             "incident response and postmortems"]
total = sum(WEEK.values())
pep = sum(WEEK[i] for i in PEP_ITEMS)
rep = sum(WEEK[i] for i in REP_ITEMS)
print(f"{'activity':44}{'h/wk':>6}   track")
for act, h in WEEK.items():
    t = "PEP" if act in PEP_ITEMS else "REP"
    print(f"{act:44}{h:>6}   {t}")
print(f"\nPEP-shaped hours: {pep}/{total} ({pep/total*100:.0f}%)")
print(f"REP-shaped hours: {rep}/{total} ({rep/total*100:.0f}%)")
lead = "REP" if rep > pep else "PEP"
print(f"\nThis calendar is {lead}-shaped. Book {lead} first — same level, same price,")
print("so the tiebreaker is which exam's questions you answer from experience")
print("rather than from the prep course. The other track remains available; the")
print("program is a pair of siblings, not a sequence, and nothing expires by")
print("taking them in either order.")
EOF
```

**Expected result:** A 20-of-34 REP-shaped week, with the recommendation following the hours rather than any notion of prestige. The sibling structure is what makes this low-stakes — choosing "wrong" costs nothing but ordering, which is exactly why the honest-calendar exercise beats deliberation.

**Negative test:** Choosing PEP because "performance sounds more technical." The exam will be answered from the prep course instead of from experience, which is the difference the experience bands describe.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — The preparation checklist

**Objective:** Assemble the plan entirely from official, free material.

```bash
python3 - <<'EOF'
plan = """
TARGET: REP  (Certified Reliability Engineer - Professional, $175, 60 min, proctored)

BLUEPRINT (public topic list, quoted in this volume's chapter headers):
  [ ] S1 Alerts & incident mgmt      -> ch07 + Lab 7.2's audit on YOUR account
  [ ] S2 Service level management    -> ch08 + boundary/prioritization labs
  [ ] S3 Infra, cloud, networking    -> ch06 + agent-tuning ledger on YOUR fleet
  [ ] S4 Automation (APIs/Terraform) -> ch08 Lab 8.3 + the real Terraform provider

OFFICIAL FREE PREP:
  [ ] REP Exam Prep Course           [ ] Certification Learning Path
  [ ] Exam readiness kit             [ ] Program guide (downloadable)

FROM THE EXAM GUIDE (free sign-in — the ONLY source for these):
  [ ] question count                 [ ] passing score
  [ ] current retake / validity policy

DO ON A REAL ACCOUNT BEFORE BOOKING:
  [ ] build a policy + NRQL condition + workflow, end to end
  [ ] define one SLI/SLO and watch attainment for two weeks
  [ ] apply one alert via the Terraform provider, then drift it and re-apply
"""
print(plan)
print("Every unchecked box is free. The only money in this plan is the $175 exam,")
print("and the two-week SLO item is the reason to book the date two weeks out.")
EOF
```

**Expected result:** A complete preparation plan whose only cost is the exam fee itself. The two-week SLO item is the deliberately inconvenient one — attainment is a number you understand by watching it move, and scheduling the exam around that fact is the plan working as intended.

**Negative test:** Substituting a third-party question bank for the sign-in-gated Exam Guide. The guide is free and authoritative; the bank is neither.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] An entry point chosen by experience band, with NVF taken regardless (it is free).
- [ ] PEP or REP selected by calendar shape, not by sound.
- [ ] Preparation assembled from public topic lists and free official courses.
- [ ] Exam Guide consulted for the gated numbers; third-party figures declined.
- [ ] New Relic placed on the single-store, one-language axis among its peers.
