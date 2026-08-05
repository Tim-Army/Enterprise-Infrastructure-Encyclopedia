# Chapter 01: The SAP Certification Program

![The SAP certification program in transition. As of 2026 SAP is moving all certifications from multiple-choice to practical, performance-based exams — system-based tasks or roleplay scenarios, timeboxed around real project expectations, open-book with AI-supported tools allowed, and not live-proctored; most exams available by mid-January 2026 and all transitioned by end-March. Three levels structure the catalog: Associate, the fundamental consultant qualification and the bulk of the program; Specialist, added to an Associate for a specific role or integration component; and Professional, the advanced level requiring proven project experience such as 24 months of ERP involvement in the past 36. Exam codes carry prefixes — C for Associate, E and P for higher levels. Certification is bought as attempt bundles: one, two, or six attempts, or an SAP Learning Hub subscription with four attempts; the two-attempt option is 276 US dollars and includes ten hours of hands-on practice systems. Solution areas span S/4HANA, SuccessFactors, the Business Technology Platform, Ariba, Concur, Analytics, Enterprise Architecture, and the Business AI Platform with Joule. The reimagined program validates what a candidate can do rather than what they can recall, because AI now handles recall.](../../../diagrams/volume-144-sap-certifications/chapter-01-certification-program.svg)

*Figure 1-1. A large enterprise-software certification program remaking itself around practical exams for the AI era.*

## Learning Objectives

- Describe the SAP certification program: levels, exam-code prefixes, and solution areas.
- Explain the 2026 transition to practical, performance-based exams and why it is happening.
- Read the purchasing model — attempt bundles and the Learning Hub subscription — accurately.
- Recognize what SAP publishes (levels, prices, format rules) and what varies per exam.

## What SAP is, and why the program is large

SAP is the dominant enterprise-software vendor — the ERP and business-application backbone of a large share of the world's big companies. Its certification program is correspondingly vast: hundreds of certifications spanning finance, HR, procurement, supply chain, analytics, application development, and platform administration, because SAP is not one product but a portfolio a career can specialize inside.

That scale is the first thing to understand about the program: **nobody "gets SAP certified" in general.** You certify in a *solution area* at a *level*, and the meaningful question is always "certified in what, at which level?" — the same specialize-don't-generalize truth this encyclopedia met at [IBM (CXXIII)](../../volume-123-ibm-certifications/README.md) and [Oracle (XLVII)](../../volume-047-oracle-certifications/README.md), at even larger scale.

## The 2026 story: certification reimagined for the AI era

The single most important current fact about SAP certification is that it is **changing format in 2026**, and the change is genuine rather than cosmetic:

> **SAP is transitioning all certifications from multiple-choice to practical, performance-based exams** — "most exams available by mid-January 2026, all practical exams transitioned by end-March."

The new exam format, in SAP's own terms:

| Property | What it means |
|:---|:---|
| **System-based tasks or roleplay scenarios** | You do the work in a real SAP environment, or handle a scenario, rather than answer questions about it |
| **Timeboxed challenges around real project expectations** | Structured like the job, under time pressure |
| **Open-book — resources and AI tools allowed** | You may use documentation *and AI assistants* during the exam |
| **No live proctoring** | Self-managed, modern exam experience |

The reasoning SAP gives is the interesting part, and it is worth taking seriously: **in a world where AI handles recall, memorizing facts is no longer the skill worth certifying.** The old multiple-choice exam tested whether you *knew* the transaction code; the AI assistant now knows it. So the exam moves to testing whether you can *apply* knowledge to deliver an outcome — with the AI assistant sitting right there, exactly as it will in the real job. Prove what you can do, not what you can recall.

This is a bet other vendors will be forced to make, and SAP is among the first at this scale to make it openly. The volume treats it as the defining feature, and Chapter 08 is devoted to preparing for a practical, open-book, AI-allowed exam — a genuinely different study problem.

**Two transition details that matter:**

- **Practical format is required for first-time takers only.** Already-certified professionals face no immediate re-certification; they continue their renewal cycle and take the standard "stay-certified assessment" at expiration.
- **Scoring:** task results are reviewed automatically or by AI; **video submissions are scored by experts within 20 business days.** Certified professionals still receive a **Credly badge** showing type and level.

## The three levels

| Level | What it certifies | Prefix (typical) |
|:---|:---|:---|
| **Associate** | Fundamental consultant knowledge — apply skills "under the guidance of an experienced consultant." The bulk of the catalog. | **C_** |
| **Specialist** | Added *on top of* an Associate — a specific role or integration component (e.g. S/4HANA Conversion and System Upgrade) | varies |
| **Professional** | Advanced — requires **proven project experience** and deeper business-process and solution understanding (e.g. RISE with SAP Methodology requires "a minimum of 24 months of active ERP project involvement within the past 36 months") | **P_**, some **E_** |

The Associate/Professional distinction is the one to internalize: Associate is knowledge-and-application under supervision; **Professional demands demonstrated, recent, real project experience** — it is not a harder test of the same material but a different claim about what you have actually done. That experience requirement is why Professional cannot be crammed.

## Exam codes and solution areas

SAP certifications carry **exam codes** with a letter prefix and a solution mnemonic — `C_THR81` (SuccessFactors Employee Central), `C_CPI` (Integration Developer), `C_ABAPD` (ABAP Cloud Backend Developer), `C_AIG` (Generative AI Developer), `P_`-prefixed Professional exams. The reinvented program tends to show **base codes** rather than the version-suffixed forms (`C_TS4CO_2023`) older references used — a currency trap when reading study material.

The solution areas the catalog spans (facets: Role, Product Category, Product, Language):

- **S/4HANA** — the ERP core (Cloud Public and Private Edition; Finance, Controlling, Sales, Sourcing & Procurement, Project Systems, Conversion/Upgrade)
- **SuccessFactors** — HXM (Employee Central, Performance & Goals, Succession, Recruiting)
- **Business Technology Platform (BTP)** — Administrator, Integration (CPI), ABAP Cloud development, **Generative AI Developer**, Business Data Cloud
- **Ariba / Business Network, Concur, Analytics (SAC/Datasphere), Enterprise Architecture (LeanIX), WalkMe, and the Business AI Platform + Joule**

## The purchasing model

Unlike several vendors in Batch F, **SAP publishes prices** — and the model is *attempt bundles and subscriptions*, not per-exam fees:

| Option | Includes |
|:---|:---|
| **Exam, one attempt** | A single attempt |
| **Exam, two attempts** | **USD 276.00/year** — two attempts (two areas, or a retry) **plus 10 hours of hands-on practice systems** |
| **Exam, six attempts** | Six attempts |
| **SAP Learning Hub subscription** | "All you need to get and stay certified," including **four exam attempts** |

The two-attempt bundle's **10 hours of practice-system access** is worth noting: on a practical exam, hands-on practice in a real SAP environment is the preparation, so SAP now bundles the practice environment with the attempts. That is the purchasing model adapting to the format change.

## Hands-On Lab

The labs in this volume model SAP certification concepts in Python at no cost — SAP itself is enterprise software you cannot spin up freely, so the labs model the *decisions and disciplines*, and Chapter 08 addresses practical-exam preparation directly.

### Lab 1.1 — Level, prefix, and what each claims

**Objective:** Read a certification's level and understand the claim it makes.

```bash
python3 - <<'EOF'
CERTS = [
  # code,       name,                                   level,          experience_required
  ("C_THR81",  "SuccessFactors Employee Central",       "Associate",    "none — entry, supervised"),
  ("C_CPI",    "Integration Developer",                 "Associate",    "none — mentored role"),
  ("C_ABAPD",  "ABAP Cloud Backend Developer",          "Associate",    "none — beta practical exam"),
  ("C_AIG",    "Generative AI Developer",               "Associate",    "none"),
  ("E_ACTAI",  "SAP Activate Agile Project Management",  "higher",       "project management skills"),
  ("P_...",    "Professional (e.g. Enterprise Arch.)",   "Professional", "PROVEN project experience"),
  ("C_RISME",  "RISE with SAP Methodology",             "experience",   "24 months ERP in past 36"),
]
print(f"{'code':10}{'level':>14}   certification / experience claim")
for code, name, level, exp in CERTS:
    print(f"{code:10}{level:>14}   {name}")
    print(f"{'':10}{'':>14}   -> requires: {exp}")
print("\nThe claim escalates with level:")
print("  ASSOCIATE (C_): 'I know this and can apply it UNDER SUPERVISION' — no")
print("     experience gate, entry qualification. Most of the catalog.")
print("  PROFESSIONAL (P_): 'I have DONE this on real projects' — a gated, recent-")
print("     experience claim. C_RISME's 24-months-in-36 is the pattern.")
print("\nReading a code: the PREFIX signals the claim, the mnemonic signals the area.")
print("Never read 'SAP certified' without asking WHICH cert — the program is")
print("hundreds of specialties, and the level changes what the badge even means.")
EOF
```

**Expected result:** Codes read as level-plus-area, with the Associate/Professional split framed as a supervision-versus-experience claim. The reading skill is the lesson — a bare "SAP certified" is nearly meaningless in a program this large, and the prefix plus experience gate is what the credential actually asserts.

**Negative test:** Treating a Professional certification as "the advanced version of the Associate exam." It is an experience-gated claim; 24 months of real project work is not a study task.

**Cleanup:** None.

### Lab 1.2 — The purchasing model and the practice hours

**Objective:** Choose an attempt bundle honestly.

```bash
python3 - <<'EOF'
OPTIONS = [
  # option,                        attempts, extras,                          price_usd
  ("Exam, one attempt",                 1,   "-",                              None),
  ("Exam, two attempts",                2,   "10 hrs hands-on practice systems", 276),
  ("Exam, six attempts",                6,   "-",                              None),
  ("SAP Learning Hub subscription",     4,   "full learning content + stay-certified", None),
]
print(f"{'option':32}{'attempts':>9}   extras / price")
for opt, att, extras, price in OPTIONS:
    p = f"USD {price}" if price else "priced separately"
    print(f"{opt:32}{att:>9}   {extras}  ({p})")
print("\nThe model is ATTEMPT BUNDLES, not per-exam fees — and one detail matters most:")
print("the two-attempt bundle includes 10 HOURS OF PRACTICE SYSTEM ACCESS.")
print("\nWhy that is not a throw-in: the exam is now PRACTICAL. You are doing tasks")
print("in a real SAP system. Practice IN a real SAP system is the preparation —")
print("so SAP now sells the practice environment WITH the attempts. On the old")
print("multiple-choice exam, practice-system hours would have been irrelevant.")
print("The purchasing model changed BECAUSE the exam format changed.")
print("\nChoosing: one attempt if you are experienced and ready; two (with the")
print("practice hours) for most first-timers on a practical exam; the Learning Hub")
print("subscription if you are certifying in several areas or need the full content.")
EOF
```

**Expected result:** The bundles laid out with the two-attempt option's 10 practice hours highlighted, and the insight that the purchasing model changed *because* the exam went practical. That causal link is the chapter's throughline — every feature of the reimagined program traces back to the format change, and the practice-system bundling is the clearest example.

**Negative test:** Buying a one-attempt exam for a first practical exam with no practice-system time. The format is unfamiliar and hands-on; the practice hours are where you learn the exam is not like the old one.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The program understood as hundreds of specialties across solution areas, not one credential.
- [ ] The 2026 practical-exam transition understood, including its AI-era reasoning.
- [ ] Associate, Specialist, and Professional levels distinguished by their claims.
- [ ] The attempt-bundle purchasing model read, with practice-system hours tied to the format change.
