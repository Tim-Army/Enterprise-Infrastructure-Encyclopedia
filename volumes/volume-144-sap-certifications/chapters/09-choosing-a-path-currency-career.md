# Chapter 09: Choosing a Path, Currency, and Career

## Learning Objectives

- Choose an SAP certification path — solution area, module, and level.
- Prepare for practical, open-book, AI-allowed exams.
- Place SAP among the encyclopedia's enterprise and platform volumes.
- Stay current with a program mid-transformation.

## Choosing a path

An SAP certification path is three decisions, in order:

1. **Solution area** — the biggest fork. S/4HANA (ERP core), SuccessFactors (HR), BTP (development/platform), Ariba (procurement), Analytics, or the AI/data layer. This is choosing an industry within SAP, and it is largely a choice of what business function you want to work in.
2. **Module or role** — within the area: FI vs SD vs MM in S/4HANA; Employee Central vs Compensation in SuccessFactors; Administrator vs Developer vs Integration in BTP. This is the specialty that defines your day-to-day.
3. **Level** — Associate to start (knowledge + supervised application), Specialist to add a focused component, Professional once you have the **proven project experience** the level gates on.

| If you… | Start with | Then |
|:---|:---|:---|
| Want the ERP-core consultant path | An **S/4HANA module Associate** (FI/CO/SD/MM) | Add a Specialist; Professional after real projects |
| Want the HR/people path | **SuccessFactors Employee Central** | Specialize (Compensation, Recruiting) — mind the partner-provisioning caveat |
| Want the developer/platform path | **BTP** (ABAP Cloud Dev, Integration, or Administrator) | The clean-core and integration depth |
| Want the architect path | Positioning + **Enterprise Architect (Professional)** | Experience-gated; build the project history first |
| Want the AI path | **Generative AI Developer** or a positioning cert | Match to build-vs-articulate (Chapter 06) |

**The overriding rule:** there is no "SAP certification" — there is *this module, at this level, in this area*. Choose the business function first, because the module, the projects, and the roles all follow from it, and switching areas later means largely starting the specialty over.

## Preparing for the practical exam

Chapter 07 is the study plan, and it inverts the traditional SAP approach:

1. **Get hands-on time.** The exam is a task in a live system; the only real preparation is doing the work. The two-attempt bundle's **10 practice-system hours** exist for this; the Learning Hub subscription gives more.
2. **Practice open-book skills.** Learn to navigate the documentation *fast* and direct the AI assistant *well* — both are now assessed, neither was before.
3. **Stop memorizing.** Question dumps target the retired multiple-choice format. They are worse than useless — they prepare the wrong skill.
4. **Understand the why.** The practical exam tests judgment (fit-to-standard, SoD-aware role design, clean-core choices), not recall. Understanding *why* a process works is what lets you handle a scenario you have not seen.
5. **Budget the scoring window.** Video-scored components take up to **20 business days**; do not schedule an exam the week you need the badge.

> **What SAP publishes and what it does not:** the levels, the exam *format*, the transition timeline, the scoring windows, and the **prices** (USD 276 two-attempt; subscription tiers) are all public. Per-exam duration, question count, and passing score vary by the new practical format and are not uniformly published — get the specifics for your target certification from its own page, and never from a dumps site preparing you for an exam that no longer exists.

## Where SAP sits in the encyclopedia

SAP is the encyclopedia's first pure **enterprise-business-application** vendor, and its neighbors are the other giant, portfolio-spanning programs:

| Volume | Kinship |
|:---|:---|
| [**CXXIII IBM**](../../volume-123-ibm-certifications/README.md), [**XLVII Oracle**](../../volume-047-oracle-certifications/README.md) | The other vast, specialize-don't-generalize enterprise catalogs |
| [**LXXX ServiceNow**](../../volume-080-servicenow-certifications/README.md), [**LXXXIII Salesforce**](../../volume-083-salesforce-certifications/README.md) | Business-platform certification programs with the same module/role structure |
| [**CXXXV Confluent**](../../volume-135-confluent-certifications/README.md) | The integration discipline SAP's BTP chapter shares |
| The AI-cert wave ([**XXXVIII Microsoft**](../../volume-038-microsoft-certifications-beyond-azure/README.md), [**CXXXVI GitLab**](../../volume-136-gitlab-certifications/README.md)) | The assistant-vs-agent and AI-era certification design SAP is now part of |

The comparison worth carrying: **SAP and Salesforce/ServiceNow all structure certification as module-plus-level within a huge platform**, and all are being reshaped by AI. What makes SAP distinctive in 2026 is being **among the first at this scale to move the entire program to practical, open-book, AI-allowed exams** — a bet that, if it works, the others will follow. This volume treats that transition as the headline because it is the most consequential certification-design change on the whole shelf.

## Currency

- **The program is mid-transformation.** Practical exams rolled out Q1 2026; the format, the AI-tool rules, and the per-exam specifics are all still settling. Re-verify on `learning.sap.com` before planning — this is the most fast-moving program in the encyclopedia right now.
- **Exam codes shed version suffixes.** The reinvented program shows base codes (`C_ABAPD`) where older references used version-dated forms (`C_TS4CO_2023`) — a currency trap in old study material.
- **Next-version dates are published per exam** (many SuccessFactors exams noted "next version mid-December 2026") — check your target's version before booking.
- **Already-certified professionals are unaffected for now** — no immediate re-certification; standard renewal continues.
- **Verified 4 August 2026** from sap.com (certification options + pricing), learning.sap.com/certifications (catalog + exam codes), and learning.sap.com/get-certified/reimagining-certification (the practical-exam transition — format, timeline, scoring, rules). Per-exam duration/question count/passing score vary by the new format and are not asserted here.

## Hands-On Lab

### Lab 9.1 — Build your SAP path

**Objective:** Make the three decisions in order.

```bash
python3 - <<'EOF'
PROFILE = {
  "business function I want":   "finance",       # finance / HR / procurement / development / architecture
  "years of SAP project exp":   0,
  "prefer config or code":      "config",
}
AREA = {"finance":"S/4HANA (FI/CO)","HR":"SuccessFactors","procurement":"Ariba/MM",
        "development":"BTP","architecture":"Enterprise Architecture"}
area = AREA[PROFILE["business function I want"]]
print(f"1. SOLUTION AREA (from business function '{PROFILE['business function I want']}'): {area}")
module = {"S/4HANA (FI/CO)":"start with FI Associate, add CO",
          "SuccessFactors":"start with Employee Central",
          "BTP":"ABAP Cloud Dev or Integration or Administrator"}.get(area, "the area's foundational module")
print(f"2. MODULE/ROLE: {module}")
exp = PROFILE["years of SAP project exp"]
level = "Associate (no experience gate — start here)" if exp < 2 else "Associate now; Professional is within reach (2+ yrs experience)"
print(f"3. LEVEL: {level}")
print(f"\nYour path: {area} -> {module} -> {level}")
print("\nThe order is not negotiable: AREA first (it is choosing a business function),")
print("then MODULE (the day-to-day specialty), then LEVEL (gated by experience for")
print("Professional). Switching AREA later means restarting the specialty — so choose")
print("the business function you actually want to work in, not the one with the most")
print("certifications or the shiniest AI badge.")
print("\nAnd prepare for a PRACTICAL exam (Chapter 07): hands-on hours, not question dumps.")
EOF
```

**Expected result:** A three-decision path resolving area → module → level, gated on experience for Professional. The non-negotiable ordering is the lesson — solution area is a business-function choice that everything else follows from, and switching it later is expensive, so it deserves the most thought.

**Negative test:** Choosing a certification by which has the most job postings, ignoring the business function. You may certify into work you do not want to do, in an area you will then leave — restarting the specialty.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 9.2 — The practical-exam readiness check

**Objective:** Assess readiness for the new format honestly.

```bash
python3 - <<'EOF'
plan = """
TARGET: ______ Associate  (solution area + module)

READINESS FOR THE PRACTICAL FORMAT (Chapter 07) — the exam is a live-system task:
  [ ] hands-on hours logged in a real/practice SAP system: ___ (aim: 20+)
  [ ] can complete the module's core tasks WITHOUT a step-by-step guide
  [ ] can find answers in SAP Help docs FAST (open-book only helps if you're quick)
  [ ] comfortable directing the AI assistant (it is allowed — use it well)
  [ ] understand WHY the processes work, not just the click-path (scenarios test judgment)

DO NOT:
  [ ] rely on a question dump — it targets the RETIRED multiple-choice format
  [ ] schedule the exam the week you need the badge — video scoring takes 20 business days

PUBLISHED FACTS TO CONFIRM ON learning.sap.com FOR MY EXAM:
  [ ] the exam's CURRENT version + next-version date (codes shed version suffixes)
  [ ] whether it has a video-scored component (-> the 20-day window applies)
  [ ] price/attempt bundle (USD 276 two-attempt incl. 10 practice hours, or Learning Hub)

MINDSET: prove what you can DO. The exam mirrors the job — docs open, AI available,
under a clock, doing real tasks. Practice THOSE conditions, not flashcards.
"""
print(plan)
print("Every 'DO NOT' targets a habit from the OLD exam era. The single biggest")
print("preparation mistake in 2026 is studying for the exam SAP just retired.")
EOF
```

**Expected result:** A readiness checklist built entirely around the practical format — hands-on hours, doc speed, AI-direction, and judgment — with the retired-format habits explicitly flagged. The mindset line is the volume's closing note: the exam mirrors the job, so practicing the job's conditions is the preparation, and studying for the old format is 2026's most common mistake.

**Negative test:** Filling this out and then studying from a multiple-choice question bank anyway. The checklist and the dump prepare for different exams; only one of them still exists.

**Rollback:** Keep the plan.

## Summary and Completion Checklist

- [ ] An SAP path chosen as area → module → level, business function first.
- [ ] Practical-exam preparation built on hands-on hours, not memorization.
- [ ] The published facts (format, timeline, pricing, scoring window) separated from per-exam specifics.
- [ ] SAP placed among the enterprise-platform volumes and the AI-era certification wave.
- [ ] A faster re-verification cadence noted for a program mid-transformation.
