# Chapter 01: The UiPath Certified Professional Program

![The UiPath Certified Professional program and the platform beneath it. The program is role-based, aligned to real-world automation roles across two levels, Associate and Professional. Certifications include Agentic Automation Associate and Professional for collaborating with and governing AI agents, Automation Developer Associate and Professional for building automations, Specialized AI Professional for Document Understanding and Communications Mining, Automation Solution Architect Professional for enterprise architecture, Automation Business Analyst Professional for process discovery and requirements, and the testing track moving from the retiring Software Testing Engineer Professional to the new Test Cloud Architect Professional. The Automation Developer Associate exam is sixty multiple-choice and multi-select questions. Credentials issued since February 2026 are valid for three years. Preparation is free through UiPath Academy; exams are proctored and paid via vouchers; holding multiple certifications earns the Automation Catalysts badge. The legacy UiPath RPA Associate and Advanced RPA Developer certifications, retired in 2023, expire on October 15, 2026, and were relaunched as the Automation Developer Associate and Professional. The platform spans Studio for building automations, Orchestrator for deploying and managing robots, attended and unattended Robots for execution, and AI and discovery products including Document Understanding, Communications Mining, Process Mining, Task Mining, and Autopilot, all reflecting the industry shift from robotic process automation to agentic automation that combines AI agents, robots, and humans.](../../../diagrams/volume-149-uipath-certifications/chapter-01-certification-program.svg)

*Figure 1-1. Role-based Associate and Professional certifications over the automation platform, amid the RPA-to-agentic shift.*

## Learning Objectives

- Describe the UiPath Certified Professional program — role-based certifications across two levels.
- Distinguish the certification roles: developer, business analyst, architect, AI, testing, agentic.
- Understand the RPA-to-agentic-automation shift the program reflects.
- Recognize currency, legacy retirement, and the free UiPath Academy prep path.

## What UiPath is

UiPath is the leader in **business process automation** — the platform organizations use to automate repetitive, rule-based work by building software **robots** that operate applications the way a person would, and, increasingly, **AI agents** that reason and act. UiPath pioneered **RPA** (Robotic Process Automation) and has since expanded into **agentic automation** — the subject of [Chapter 2](02-from-rpa-to-agentic-automation.md). Its certifications validate the skills to build, deploy, and govern automation at enterprise scale, typically within a **Center of Excellence (CoE)**.

## The role-based program

The **UiPath Certified Professional** program is **role-based**: rather than one linear ladder, it offers certifications aligned to the real jobs on an automation team, each at an **Associate** or **Professional** level:

| Certification | Role | Level |
|:---|:---|:---|
| **Agentic Automation Associate** | Collaborating with AI agents (technical & non-technical) | Associate |
| **Agentic Automation Professional** | Designing, orchestrating, governing agentic automation | Professional |
| **Automation Developer Associate** | Building automations | Associate |
| **Automation Developer Professional** | Advanced building, best practices, scale | Professional |
| **Specialized AI Professional** | Document Understanding & Communications Mining | Professional |
| **Automation Solution Architect Professional** | Enterprise automation architecture | Professional |
| **Automation Business Analyst Professional** | Process discovery & requirements | Professional |
| **Test Cloud Architect Professional** *(new, May 2026)* | Cloud-based test architecture | Professional |

The **Automation Developer Associate** is the common entry point — its exam is **60 multiple-choice and multi-select questions**. The **agentic** certifications are the program's newest and fastest-growing area, reflecting where automation is heading.

## The RPA-to-agentic shift

The single most important context for the whole program is that UiPath — and the industry — has moved **from RPA to agentic automation**. Classic RPA automates *deterministic, rule-based* tasks (a robot that reads an invoice PDF and types it into an ERP). **Agentic automation** adds **AI agents** that *reason and decide* — handling the judgment and ambiguity that deterministic robots cannot — orchestrated together with robots and humans. This is why the certification program is **AI-forward** (agentic certs front and center, "AI-powered automation" in every description) and why the legacy pure-RPA certifications are being retired. [Chapter 2](02-from-rpa-to-agentic-automation.md) covers the shift in depth.

## Currency and legacy

Two dates matter:

- **Validity:** credentials issued **since February 2026 are valid for three years** from the achievement date.
- **Legacy retirement:** the old **UiRPA** (RPA Associate) and **UiARD** (Advanced RPA Developer) certifications, retired in 2023, **expire on 15 October 2026**. They were relaunched as the **Automation Developer Associate** and **Professional** — so a UiRPA holder's path forward is the current Developer Associate.

Preparation is **free through UiPath Academy** (comprehensive courses); exams are **proctored** and paid via **vouchers**. Holding **multiple** certifications earns the **Automation Catalysts** badge.

## Hands-On Lab

The labs in this volume model automation concepts in Python at no cost — UiPath is enterprise software, so the labs model the *decisions and disciplines* the certifications test (what to automate, attended vs unattended, queue throughput, straight-through processing). **UiPath Academy is free**, and a **Community Edition** of the product is free for learning.

### Lab 1.1 — Read the role-based program

**Objective:** Place a certification by role and level.

```bash
python3 - <<'EOF'
CERTS = [
  # cert,                              role,                  level,        note
  ("Agentic Automation Associate",     "work with AI agents", "Associate",  "technical + non-technical"),
  ("Agentic Automation Professional",  "govern agentic",      "Professional","design/orchestrate/govern"),
  ("Automation Developer Associate",   "build automations",   "Associate",  "entry point; 60 MC+multi-select"),
  ("Automation Developer Professional","build at scale",      "Professional","advanced + best practices"),
  ("Specialized AI Professional",      "IDP + comms mining",  "Professional","Document Understanding, Comms Mining"),
  ("Automation Solution Architect Pro","architecture",        "Professional","enterprise tech stacks"),
  ("Automation Business Analyst Pro",  "discovery + reqs",    "Professional","bridge business & technical"),
  ("Test Cloud Architect Pro",         "test architecture",   "Professional","NEW May 2026"),
]
print(f"{'certification':36}{'level':13}role")
for name, role, level, note in CERTS:
    print(f"{name:36}{level:13}{role}")
print("\nHow to read it — it's ROLE-BASED, not a single ladder:")
print("  - pick the CERT that matches your JOB (developer? architect? analyst?")
print("    agentic? testing?), then the LEVEL (Associate -> Professional).")
print("  - the Automation DEVELOPER ASSOCIATE is the common entry point (60 MC +")
print("    multi-select questions).")
print("  - the AGENTIC certs (Associate + Professional) are the newest, fastest-")
print("    growing area — where automation is heading (Chapter 2).")
print("\nThe program mirrors an automation TEAM in a Center of Excellence: developers")
print("build, analysts discover, architects design, testers validate, and everyone")
print("increasingly works WITH AI agents. Certify for the seat you're in.")
EOF
```

**Expected result:** The certifications placed by role (developer, analyst, architect, AI, testing, agentic) and level (Associate, Professional), with the Automation Developer Associate as the entry point and the agentic certs as the growth area. The role-based lesson is that this is not a single ladder but a map of automation-team seats — certify for your role, then climb Associate to Professional.

**Negative test:** Treating UiPath certification as one linear track from beginner to expert. It is role-based — a business analyst and a developer take different certifications, not different rungs of the same ladder.

**Cleanup:** None.

### Lab 1.2 — Currency and the legacy migration

**Objective:** Plan around the three-year validity and the October 2026 legacy expiry.

```bash
python3 - <<'EOF'
from datetime import date
LEGACY_EXPIRY = date(2026, 10, 15)
TODAY = date(2026, 8, 5)
days_left = (LEGACY_EXPIRY - TODAY).days

CREDS = [
  # cert,                          status,                       action
  ("UiRPA (RPA Associate)",        "retired 2023",               f"EXPIRES 15 Oct 2026 ({days_left}d) -> take Automation Developer Associate"),
  ("UiARD (Advanced RPA Dev)",     "retired 2023",               "EXPIRES 15 Oct 2026 -> take Automation Developer Professional"),
  ("Automation Developer Associate","current",                   "valid 3 years (since Feb 2026)"),
  ("Agentic Automation Professional","current",                  "valid 3 years"),
]
print(f"UiPath credential currency (today = {TODAY}):\n")
for cert, status, action in CREDS:
    print(f"   {cert:34} [{status}]")
    print(f"   {'':34}  -> {action}")
print(f"\nTWO currency facts:")
print(f"  1. LEGACY EXPIRY: UiRPA + UiARD (retired 2023) EXPIRE 15 Oct 2026 — {days_left} days")
print("     away. Holders must pass a CURRENT exam to stay in the program. The natural")
print("     migration: UiRPA -> Automation Developer Associate, UiARD -> Developer Pro.")
print("  2. 3-YEAR VALIDITY: current credentials (issued since Feb 2026) last 3 years,")
print("     then renew — because the platform and (especially) AI move fast.")
print("\nThe rename from 'RPA' to 'Automation Developer' isn't cosmetic: it marks the")
print("shift from pure robotic process automation to AI-powered/agentic automation.")
print("A UiRPA holder migrating isn't just renewing — they're re-skilling into the AI")
print("era. Prep is FREE via UiPath Academy, so the migration cost is time, not money.")
EOF
```

**Expected result:** The legacy UiRPA/UiARD credentials flagged as expiring 15 October 2026 with their migration to the current Automation Developer certifications, alongside the three-year validity of current credentials. The currency lesson is two-fold — legacy pure-RPA certs expire soon and migrate to the renamed AI-powered Developer certs, and current credentials renew every three years against a fast-moving platform.

**Negative test:** Assuming a retired UiRPA certification remains valid indefinitely. It expires 15 October 2026; staying in the program requires passing a current exam — the natural path being the Automation Developer Associate that replaced it.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The UiPath program understood as role-based, across Associate and Professional levels, not a single ladder.
- [ ] The certification roles (developer, analyst, architect, AI, testing, agentic) matched to automation-team seats.
- [ ] The RPA-to-agentic shift recognized as the context for the AI-forward program and the legacy retirements.
- [ ] Currency understood — three-year validity since Feb 2026, and the UiRPA/UiARD expiry (15 Oct 2026) with its migration path, prepped free via UiPath Academy.
