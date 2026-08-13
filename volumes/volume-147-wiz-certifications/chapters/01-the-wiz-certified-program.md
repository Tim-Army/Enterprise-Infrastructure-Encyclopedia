# Chapter 01: The Wiz Certified Program

![The Wiz Certified program and the platform beneath it. The certification ladder runs from Wiz Certified Cloud User, an entry-level user credential, to Wiz Certified Cloud Fundamentals, which validates deployment and management of Wiz Cloud and is the prerequisite for future specialized exams, to Wiz Certified Defend Fundamentals, which validates cloud threat detection and response with Wiz Defend. Exams are proctored online or at an onsite test center and are open to Wiz customers, partners, and cloud security professionals. The Defend Fundamentals exam is public: sixty multiple-choice questions in one hundred fifty minutes, a two-year certification, and a shareable badge. Training is free through the CloudSec Academy. The platform beneath spans three pillars in a code-to-cloud-to-runtime story: Wiz Code for shift-left security of code, infrastructure as code, and secrets before deployment; Wiz Cloud for cloud-native application protection posture including CSPM, CWPP, CIEM, DSPM, and vulnerability management; and Wiz Defend for cloud detection and response of runtime threats. Underneath all of it is the Wiz Security Graph, which models cloud resources and their relationships so that attack paths, the toxic combinations of exposure, vulnerability, privilege, and sensitive data that form an exploitable route, can be prioritized over a flat list of issues.](../../../diagrams/volume-147-wiz-certifications/chapter-01-certified-program.svg)

*Figure 1-1. An expanding exam ladder over the code-to-cloud-to-runtime platform, all anchored on the Security Graph.*

## Learning Objectives

- Describe the Wiz Certified program — the exams, the prerequisite chain, and how they are delivered.
- Distinguish the three platform pillars: Wiz Code, Wiz Cloud, Wiz Defend.
- Understand what CNAPP is and why the Wiz Security Graph is the thing beneath everything.
- Recognize Wiz's position as the graph-based, agentless cloud-security platform.

## What Wiz is

Wiz is a **cloud security platform** — a **CNAPP** (Cloud-Native Application Protection Platform) that finds, prioritizes, and helps remediate risk across cloud environments, and (with Wiz Defend) detects and responds to threats at runtime. Its defining idea is the **Wiz Security Graph**: rather than emitting a flat list of thousands of findings, Wiz builds a graph of your cloud resources and their relationships, then surfaces the **attack paths** — the *combinations* of issues that form an actually-exploitable route to something that matters.

That is the whole pitch and the subject of its certifications: not "here are 10,000 misconfigurations," but "here are the three attack paths where a public workload with a critical vulnerability has a role that can reach your customer database." The certifications validate that you can operate the platform that thinks this way.

## The certification ladder

The **Wiz Certified** program launched in February 2025 and is an *expanding portfolio* of proctored exams — taken **online or at an onsite test center**, and open to Wiz customers, partners, and cloud security professionals alike. As of 2026 there are three:

| Exam | Validates | Notes |
|:---|:---|:---|
| **Wiz Certified Cloud User** | Using Wiz Cloud effectively as a day-to-day user | Entry point |
| **Wiz Certified Cloud Fundamentals** | Deploying and managing Wiz Cloud | The first exam (Feb 2025); **prerequisite for future specialized exams** |
| **Wiz Certified Defend Fundamentals** | Cloud threat detection and response with Wiz Defend | Live Nov 2025; for SOC/IR, IT, admins, developers |

**Cloud Fundamentals is the keystone**: Wiz explicitly designed it as the foundation and prerequisite for the specialized exams that follow, so most paths run *through* it. The ladder is young and growing — the structure to internalize is the **pillar-aligned, fundamentals-first** shape, not a fixed list.

## What is published

Wiz publishes the program, the delivery model, and the **Defend Fundamentals specifics**: **60 multiple-choice questions in 150 minutes**, a **two-year certification**, and a **shareable badge**. Wiz recommends the *Wiz for Threat Detection and Response* course plus **two months of hands-on time** in Wiz Defend before sitting it.

> **The published-versus-portal split:** Defend Fundamentals' mechanics are public and stated here. Exact question counts and durations for Cloud User and Cloud Fundamentals are not uniformly published; this volume asserts the Defend numbers and points at the Wiz Certified homepage for the rest. Training is **free** through the CloudSec Academy — this is a low-barrier program to *learn*, with proctored exams to *certify*.

## The three pillars

Every Wiz exam sits on the **code-to-cloud-to-runtime** platform:

| Pillar | Is | Covers |
|:---|:---|:---|
| **Wiz Code** | Shift-left / ASPM | Securing code, IaC, and secrets *before* deployment |
| **Wiz Cloud** | CNAPP posture | CSPM, CWPP, CIEM, DSPM, vulnerability management |
| **Wiz Defend** | Cloud detection & response (CDR) | Runtime threats, with code-to-cloud context |

The pillars share one substrate — the **Security Graph** — so a finding in code (Wiz Code), a posture issue in the cloud (Wiz Cloud), and a runtime detection (Wiz Defend) are all *the same graph*, letting Wiz trace a runtime alert back through the cloud posture to the line of code that introduced it. That unity is why the certifications teach the graph first (Chapter 2) and the pillars second.

## Hands-On Lab

The labs in this volume model cloud-security concepts in Python at no cost — Wiz is a SaaS platform, so the labs model the *decisions and disciplines* the certifications test (attack-path prioritization, effective-permission calculation, agentless coverage). Wiz offers a **free demo/trial** and the **CloudSec Academy** is free.

### Lab 1.1 — Read the ladder and the prerequisite chain

**Objective:** Place an exam by pillar, audience, and the prerequisite chain.

```bash
python3 - <<'EOF'
EXAMS = [
  # exam,               pillar,      audience,                     prereq,           mechanics
  ("Cloud User",        "Wiz Cloud", "day-to-day platform users",  None,             "portal-gated"),
  ("Cloud Fundamentals","Wiz Cloud", "deploy & manage Wiz Cloud",  None,             "portal-gated (the keystone)"),
  ("Defend Fundamentals","Wiz Defend","SOC/IR, IT, admins, devs",  "recommend Cloud Fundamentals first", "60Q / 150min / 2yr / badge"),
]
print(f"{'exam':22}{'pillar':12}{'prereq':38}mechanics")
for name, pillar, aud, prereq, mech in EXAMS:
    p = prereq if prereq else "-"
    print(f"{name:22}{pillar:12}{p:38}{mech}")
print("\nTwo things to read from this:")
print("  1. FUNDAMENTALS-FIRST: Cloud Fundamentals is the keystone Wiz designed as the")
print("     prerequisite for future SPECIALIZED exams. Most paths run through it.")
print("  2. PILLAR-ALIGNED: exams map to the platform pillars (Cloud, Defend, and Code")
print("     as it grows). Pick the pillar that matches your job, climb from Fundamentals.")
print("\nThe program is YOUNG and EXPANDING (launched Feb 2025) — internalize the SHAPE")
print("(fundamentals-first, pillar-aligned, proctored, 2-year currency), not a fixed list.")
print("Only Defend Fundamentals' mechanics are public (60Q/150min/2yr + shareable badge);")
print("the rest are portal-gated, so this volume asserts only what Wiz publishes.")
EOF
```

**Expected result:** The three exams placed by pillar and audience, with Cloud Fundamentals identified as the prerequisite keystone and only Defend Fundamentals carrying public mechanics. The fundamentals-first, pillar-aligned shape is the lesson — the program is young and expanding, so the structure matters more than a fixed exam list, and the volume asserts only Wiz's published facts.

**Negative test:** Assuming a fixed, complete exam catalog like a mature vendor's. Wiz Certified launched in 2025 and is explicitly expanding — treating today's three exams as the final list will date quickly; the durable knowledge is the shape.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Map a pillar to the job

**Objective:** Match the platform pillar (and its exam) to a role.

```bash
python3 - <<'EOF'
ROLES = [
  ("cloud security engineer / CSPM owner", "Wiz Cloud",  "posture: CSPM/CWPP/CIEM/DSPM, attack paths"),
  ("developer / platform / DevSecOps",     "Wiz Code",   "shift-left: code, IaC, secrets before deploy"),
  ("SOC analyst / incident responder",     "Wiz Defend", "runtime detection & response (Defend Fundamentals)"),
  ("cloud security architect (all three)", "all pillars","one Security Graph, code-to-cloud-to-runtime"),
]
print(f"{'role':40}{'pillar':14}focus")
for role, pillar, focus in ROLES:
    print(f"{role:40}{pillar:14}{focus}")
print("\nThe three pillars are three JOBS on ONE graph:")
print("  WIZ CODE   — the DEVELOPER/DevSecOps job: catch risk in code/IaC/secrets")
print("               BEFORE it ships (shift-left).")
print("  WIZ CLOUD  — the CLOUD-SECURITY job: posture across CSPM (config), CWPP")
print("               (workloads), CIEM (identity), DSPM (data), vuln mgmt — and the")
print("               ATTACK PATHS that connect them.")
print("  WIZ DEFEND — the SOC/IR job: detect and respond to RUNTIME threats, with the")
print("               code-to-cloud context the graph already holds.")
print("\nStart in the pillar that matches your work and climb from Fundamentals. The")
print("architect spans all three BECAUSE they're one graph — a runtime detection")
print("(Defend) traces back through cloud posture (Cloud) to the code that caused it")
print("(Code). That unity is Wiz's whole thesis, and why the graph comes first (Ch 2).")
EOF
```

**Expected result:** The three pillars mapped to the developer, cloud-security, and SOC jobs, unified by the single Security Graph. The pick-your-pillar guidance is the takeaway, with the architect spanning all three precisely because code, cloud, and runtime are one graph — a runtime detection traces back to the code that introduced it.

**Negative test:** Treating Wiz Code, Cloud, and Defend as three separate products to learn in isolation. They share one Security Graph; the value — and the exams' framing — is the code-to-cloud-to-runtime continuity, not three silos.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The Wiz Certified ladder read as fundamentals-first and pillar-aligned, with Cloud Fundamentals as the prerequisite keystone.
- [ ] The three pillars (Code, Cloud, Defend) matched to the developer, cloud-security, and SOC jobs.
- [ ] The Security Graph recognized as the single substrate beneath all three pillars.
- [ ] The published Defend Fundamentals mechanics (60Q / 150min / 2yr / badge) known; other exams identified as portal-gated.
