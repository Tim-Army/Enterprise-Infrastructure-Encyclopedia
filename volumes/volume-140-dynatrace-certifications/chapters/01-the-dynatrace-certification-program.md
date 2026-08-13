# Chapter 01: The Dynatrace Certification Program

![The Dynatrace certification program and platform. The practitioner ladder runs from the Beginner course badge and the knowledge-only Essentials certificate, through the Associate certification and its Managed variant, to the Professional tier — Dynatrace Professional, Administration Professional, and Implementation Professional — and finally the Master certification, which carries live product usage exams. Four Intermediate-level Specialist certifications sit beside the ladder: Advanced Observability, DEM and Business Analytics, Advanced Security, and Advanced Automation, plus the Application Development Specialist for AppEngine. A separate and much larger partner and services track covers Partner Sales, Partner Sales Specialist, the free Partner Sales Engineer, ACE Services, three Services Delivery certifications, Partner Services Project Management, and the Endorsed Services Partner accreditation with SaaS Upgrade, CloudOps, and App Developer specializations. Underneath sits the platform: OneAgent and ActiveGate for collection, Grail as the observability data lakehouse queried with DQL and DPL, Davis AI for deterministic causation-based root cause, and the app layer of AppEngine, AutomationEngine workflows, and Site Reliability Guardian. Exam mechanics — cost, duration, question count, passing score, and validity — are not published publicly; Dynatrace University requires a sign-in.](../../../diagrams/volume-140-dynatrace-certifications/chapter-01-certification-program.svg)

*Figure 1-1. The Dynatrace credential catalog and the platform beneath it.*

## Learning Objectives

- Describe the Dynatrace certification ladder and distinguish practitioner credentials from partner, services, and internal ones.
- Read the program's own level labels correctly — and notice where they contradict the credential names.
- Understand which exam facts Dynatrace publishes and which it does not.
- Set up a free study environment for the labs in this volume.

## What Dynatrace is

Dynatrace is an observability and application-security platform whose defining bet is **automation over assembly**. Where a stack built on open components asks you to instrument, collect, store, and correlate deliberately, Dynatrace deploys a single agent that discovers what is running, builds a live dependency model, and applies causal AI to it.

Four pieces carry that bet:

| Component | Role |
|:---|:---|
| **OneAgent** | One installed agent that auto-instruments hosts, processes, containers, and applications |
| **ActiveGate** | A proxy/gateway component for routing, remote monitoring, and secure connectivity |
| **Grail** | "The Dynatrace data lakehouse designed explicitly for observability data" — logs, metrics, traces, and events in one store, organized in **buckets, tables, and views** |
| **Davis AI** | **Deterministic, causation-based analysis** that identifies root cause using topology and dependency context |

Grail's design point matters for the exams and for the job: it requires **"no up-front description of the input data's schema."** You query it with **DQL** (Dynatrace Query Language), with **DPL** (Dynatrace Pattern Language) for pattern matching.

Davis AI's framing is the platform's sharpest claim. Correlation-based tools tell you *what* changed together; Dynatrace's documentation positions Davis as explaining *why*, by correlating "code changes, deployments, configuration, and policy updates" against an actual dependency model rather than statistical coincidence. Chapter 06 tests how much of that distinction survives contact with reality — the answer is "most of it, provided the topology is right," and the failure mode is worth knowing.

## The credential catalog

Dynatrace publishes **34 badges** through Credly. That number is misleading in a specific way, so it is worth splitting up before anything else:

| Group | Count | Can a practitioner earn it? |
|:---|:---|:---|
| **Practitioner certifications** | ~11 | Yes — this is the ladder that matters |
| **Learning credentials** (Beginner, Essentials) | 2 | Yes, but they are course completions, not exams |
| **Partner / services** | ~15 | Only via a Dynatrace partner organization |
| **Internal Dynatrace programs** | ~4 | No — these are employee leadership programs |

A reader searching "Dynatrace certification" meets all 34 at once. Roughly a third are earnable by an ordinary practitioner.

### The practitioner ladder

| Tier | Credential | Dynatrace's own level label |
|:---|:---|:---|
| Entry | **Dynatrace Beginner** (course completion) | — |
| Entry | **Dynatrace Essentials** (knowledge certificate) | — |
| Core | **Dynatrace Associate** · **Associate for Managed** | **Intermediate** |
| Core | **Dynatrace Professional** | **Advanced** |
| Core | **Administration Professional** | **Advanced** |
| Core | **Implementation Professional** | **Advanced** |
| Top | **Dynatrace Master** | **Advanced** |

Two things in that table deserve to be said plainly.

**First: "Associate" is labeled Intermediate, not foundational.** Dynatrace's own badge metadata rates the Associate as Intermediate and everything above it as Advanced. The genuinely foundational rungs are Beginner and Essentials. If you read "Associate" as "the beginner exam," you have misread the ladder by one full step — the same trap Grafana's "introductory" 101 sets in [Volume CXXXIX](../../volume-139-grafana-observability/README.md).

**Second: Essentials does not test hands-on skill.** Its own description says the credential "does not measure hands[-on]" ability — it confirms you can recognize features and describe concepts. That is a useful thing to hold and a dangerous thing to mistake for competence.

### The Specialist certifications

Four **Intermediate**-level Specialists sit *beside* the ladder rather than above it, each covering one practice area:

| Specialist | Covers |
|:---|:---|
| **Advanced Observability** | OneAgent, ActiveGate, Grail, DQL/DPL, extensions, synthetics, permissions |
| **DEM and Business Analytics** | RUM (web and mobile), Session Replay, business events, data privacy, USQL |
| **Advanced Security** | Runtime vulnerabilities, attack detection and blocking, DevSecOps, threat hunting |
| **Advanced Automation** | Workflows, Site Reliability Guardian, SLOs, configuration-as-code, CI/CD |

A fifth, **Application Development Specialist**, covers AppEngine and building custom Dynatrace apps.

These are the most useful credentials for most working engineers, because they map to what people actually do. Chapters 03–08 follow their subject matter.

## What Dynatrace does not publish

Dynatrace University — where the certification catalog, exam registration, and preparation material live — **requires a sign-in**. The public marketing pages describe training formats but name no certifications and state no exam mechanics.

The consequence is specific and worth stating rather than papering over:

> **Cost, duration, question count, passing score, and validity period are not publicly published for Dynatrace certifications.** This volume does not assert them.

That is the same discipline applied to [Rapid7 (CXXXVII)](../../volume-137-rapid7-certifications/README.md) and [SolarWinds (CXXXIV)](../../volume-134-solarwinds-certifications/README.md). Where a vendor does not publish a number, inventing one — or repeating a number from a site selling practice exams — is worse than saying "check the University."

What *is* publicly verifiable, from Dynatrace's own badge metadata: the credential names, their level labels, whether each is paid or free, the rough time-to-earn bands, and the **skill lists**, which function as domain outlines. Those skill lists are the closest thing to a published blueprint, and this volume is built on them.

Two mechanics facts that are public and worth noting: the **Partner Sales Engineer** badge is marked **Free** (nearly everything else is Paid), and **Administration Professional** is the only credential with a time-to-earn of **Weeks** rather than Days — a signal that it expects accumulated operational practice, not a study weekend.

The **Master** credential's skill list includes **"Live Product Usage Exams,"** which is Dynatrace saying, in its own metadata, that the top credential is partly practical.

## Hands-On Lab

The labs in this volume model Dynatrace concepts in Python so they cost nothing. Where the real product is needed, Dynatrace offers a free trial; the concepts are what the exams test.

### Lab 1.1 — Map the catalog to what you can actually earn

**Objective:** Separate the 34 badges into the ones that apply to you.

```bash
python3 - <<'EOF'
CATALOG = [
  # (name, group, level, notes)
  ("Dynatrace Beginner",                    "learning",   "-",            "course completion"),
  ("Dynatrace Essentials",                  "learning",   "-",            "knowledge only, NOT hands-on"),
  ("Dynatrace Associate",                   "core",       "Intermediate", "6 domains"),
  ("Dynatrace Associate for Managed",       "core",       "Intermediate", "same 6, Managed"),
  ("Dynatrace Professional",                "core",       "Advanced",     "Associate 6 + Product Extensions"),
  ("Administration Professional",           "core",       "Advanced",     "time to earn: WEEKS"),
  ("Implementation Professional",           "core",       "Advanced",     "architect/plan/implement"),
  ("Dynatrace Master",                      "core",       "Advanced",     "LIVE PRODUCT USAGE EXAMS"),
  ("Advanced Observability Specialist",     "specialist", "Intermediate", "OneAgent/Grail/DQL"),
  ("DEM & Business Analytics Specialist",   "specialist", "Intermediate", "RUM/Session Replay"),
  ("Advanced Security Specialist",          "specialist", "Intermediate", "runtime vuln + attacks"),
  ("Advanced Automation Specialist",        "specialist", "Intermediate", "workflows/SRG/SLOs"),
  ("Application Development Specialist",    "specialist", "-",            "AppEngine"),
  ("Dynatrace Ambassador",                  "community",  "-",            "invited/elite"),
  ("Autonomous Cloud Endorsement",          "community",  "Advanced",     "from the ACL lab"),
  ("Partner Sales",                         "partner",    "-",            "partner org only"),
  ("Partner Sales Specialist",              "partner",    "-",            "partner org only"),
  ("Partner Sales Engineer",                "partner",    "Advanced",     "FREE"),
  ("ACE Services Certification",            "partner",    "-",            "partner org only"),
  ("Services Delivery - Observability",     "partner",    "-",            "partner org only"),
  ("Services Delivery - SaaS Upgrade",      "partner",    "-",            "partner org only"),
  ("Services Delivery - CloudOps",          "partner",    "-",            "partner org only"),
  ("Partner Services Project Mgmt",         "partner",    "-",            "partner org only"),
  ("Endorsed Services Partner (+3 spec.)",  "partner",    "Foundational", "type=EXPERIENCE, years"),
  ("Service Delivery Practitioner",         "partner",    "-",            "partner org only"),
  ("Service Delivery Management",           "partner",    "-",            "partner org only"),
  ("RD / RVP / Future Leaders Excellence",  "internal",   "-",            "Dynatrace employees"),
  ("Dynatrace Customer Success",            "internal",   "-",            "Dynatrace employees"),
]
from collections import Counter
groups = Counter(g for _, g, _, _ in CATALOG)
print("Dynatrace credential catalog, grouped:\n")
for g in ("learning","core","specialist","community","partner","internal"):
    rows = [c for c in CATALOG if c[1] == g]
    print(f"  {g.upper():11} {len(rows):>2} entries")
earnable = [c for c in CATALOG if c[1] in ("learning","core","specialist")]
print(f"\nEarnable by an ordinary practitioner: {len(earnable)} of {len(CATALOG)} listed rows")
print("(the real badge count is 34; several rows above collapse variants)\n")
print("The practitioner ladder, with Dynatrace's OWN level labels:")
for n, g, lvl, note in CATALOG:
    if g in ("learning","core"):
        flag = "  <-- note the label" if n == "Dynatrace Associate" else ""
        print(f"   {n:34} {lvl:13} {note}{flag}")
print("\n'Associate' is labeled INTERMEDIATE. Beginner and Essentials are the entry rungs.")
print("Reading 'Associate' as the beginner exam misreads the ladder by a full step.")
EOF
```

**Expected result:** Roughly half the catalog rows are partner or internal credentials you cannot earn as an individual practitioner, and the Associate carries an Intermediate label. The second point is the one that changes behavior: candidates routinely book the Associate as a first exam because the *name* implies entry level, when Dynatrace's own metadata places two rungs beneath it.

**Negative test:** Counting "34 Dynatrace certifications" as a menu of options — most of them require a partner organization or Dynatrace employment.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Build a study plan against what is actually published

**Objective:** Record the known facts and, just as importantly, the unknown ones.

```bash
cat > my-dynatrace-plan.md <<'EOF'
PUBLISHED (verifiable from Dynatrace's own badge metadata, 4 Aug 2026):
  ladder      Beginner / Essentials -> Associate -> Professional tier -> Master
  levels      Associate = INTERMEDIATE ; Professional/Admin/Impl/Master = ADVANCED
  specialists Advanced Observability | DEM & Business Analytics |
              Advanced Security | Advanced Automation | Application Development
  domains     published as per-badge SKILL LISTS (the closest thing to a blueprint)
  cost flag   nearly all Paid; Partner Sales Engineer is FREE
  time bands  most "Days"; Administration Professional is "WEEKS"
  Master      includes "Live Product Usage Exams" -> practical component

NOT PUBLISHED (do not trust any source that states these):
  [ ] exam fee            [ ] duration          [ ] number of questions
  [ ] passing score       [ ] validity period   [ ] retake policy
  -> Dynatrace University requires sign-in. CHECK THERE, and only there.

MY PLAN
  target:      ____________________  (Associate / a Specialist / Professional)
  why:         ____________________
  prep:        Dynatrace Essentials learning plan + free trial tenant
  reality:     the Associate is Intermediate — budget accordingly
EOF
cat my-dynatrace-plan.md
```

**Expected result:** A plan whose "not published" section is as prominent as its "published" one. That inversion is the point — the most common way to be wrong about this program is to absorb a confident number from a practice-exam site that has no more access to the University than you do.

**Negative test:** Filling in a fee or passing score from a search result. If Dynatrace has not published it, a third party did not learn it legitimately.

**Rollback:** Keep the plan.

## Summary and Completion Checklist

- [ ] The 34-badge catalog split into practitioner, partner, and internal groups.
- [ ] The Associate correctly read as **Intermediate**, with Beginner/Essentials beneath it.
- [ ] Essentials understood as knowledge-only.
- [ ] The unpublished exam mechanics identified as unpublished, not guessed.
- [ ] OneAgent, ActiveGate, Grail, and Davis AI placed in the architecture.
