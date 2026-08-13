# Chapter 01: The Cohesity Academy Certification Program

![The Cohesity Academy certification program and the Data Cloud platform beneath it. Cohesity Academy offers proctored certification exams across three tiers. The Associate level includes Protection Associate for DataProtect, exam COH100, and Protection Associate for Multicloud, both carrying the Cohesity Certified Protection Associate credential. The Professional level includes Implementation Professional for SmartFiles, Protection Professional, and two NetBackup-focused Protection Professional certifications from the Veritas heritage. The Specialist level is the Security Specialist, exam COH350. Exams are proctored, cost two hundred dollars, are valid for two years, are delivered in English, and grant a digital badge on completion. The DataProtect associate exam is ninety minutes with a fifty-eight percent passing score and can be retaken once every fourteen days. The platform beneath is the Cohesity Data Cloud, an AI-powered data security and management platform spanning backup and recovery with DataProtect, file and object services with SmartFiles, SaaS cyber-vaulting with FortKnox, and AI-powered threat detection and search with DataHawk and Gaia. Cohesity merged with Veritas in December 2024, adding NetBackup.](../../../diagrams/volume-157-cohesity-certifications/chapter-01-program.svg)

*Figure 1-1. The three-tier Academy certifications and the AI-powered Data Cloud platform they validate.*

## Learning Objectives

- Describe the Cohesity Academy program — three tiers of proctored certifications.
- Place the seven certifications and their credentials (CCPA, CCIP, CCPP, CCSS).
- State the exam mechanics (proctored, $200, two-year validity, digital badge).
- Recognize Cohesity's position in AI-powered data security and management.

> **Defensive framing.** This volume is about *data resilience* — protecting, recovering, and securing data against loss and ransomware. Cohesity's backup, immutable snapshots, cyber-vaulting, and threat detection are the tools that keep an organization's data safe and recoverable. Nothing here is about attacking systems.

## What Cohesity is

Cohesity is a leader in **AI-powered data security and management** — backup and recovery, ransomware resilience, and data management across on-premises and cloud. Its platform, the **Cohesity Data Cloud**, consolidates the historically fragmented world of backup, files, and archival onto one system, and adds **AI** for threat detection and search. In **December 2024, Cohesity merged with Veritas**, combining Cohesity's modern platform with Veritas's enterprise **NetBackup** — making the combined company the largest data-protection vendor and adding NetBackup to the certification portfolio.

The closest peer this shelf covers is [Rubrik (CXXX)](../../volume-130-rubrik-certifications/README.md); **Cohesity versus Rubrik** is the defining modern-data-security comparison, and [Commvault (CXXXIII)](../../volume-133-commvault-certifications/README.md) is the enterprise-backup peer.

## The program

**Cohesity Academy** runs the certification program — **proctored exams** across **three tiers**, awarding **digital badges**. Cohesity recommends about **three months of practical experience** before attempting an exam:

| Tier | Certifications | Credential |
|:---|:---|:---|
| **Associate** | Protection Associate — DataProtect (COH100) · Protection Associate — Multicloud | **CCPA** |
| **Professional** | Implementation Professional — SmartFiles (**CCIP**) · Protection Professional · Protection Professional — NetBackup · Protection Professional — NetBackup and NetBackup Appliances (**CCPP**) | CCIP / CCPP |
| **Specialist** | Security Specialist (COH350) | **CCSS** |

The tiers follow the usual arc — **Associate** (know and administer), **Professional** (implement and operate), **Specialist** (the security depth). The **NetBackup** certifications come from the **Veritas** merger, extending the program to the enterprise-backup installed base. The lab models the program.

## Exam mechanics

Mechanics are consistent and — for the **DataProtect Associate (COH100)** — precisely published:

| Element | Value (COH100 exemplar) |
|:---|:---|
| **Delivery** | **Proctored**, register for a day/time |
| **Duration** | **90 minutes** |
| **Passing score** | **58%** |
| **Fee** | **$200 USD** |
| **Validity** | **2 years** |
| **Retake** | Once every **14 days** |
| **Language** | English |
| **Prerequisite** | None |
| **Credential** | **Digital badge** on completion |

The exams are proctored (unlike the badges-and-training models elsewhere on the shelf), reflecting that Cohesity validates **hands-on platform competence** for real data-protection job roles. The lab models the rule set.

## Cohesity in data security

Cohesity sits at the intersection of **data management** and **security** — the modern thesis being that **backup is both the last line of defense against ransomware and a prime target of it**, so data protection *is* a security discipline. This volume covers the platform the certifications validate: [DataProtect](03-dataprotect.md), [ransomware resilience](04-ransomware-resilience.md), [SmartFiles](05-smartfiles.md), [FortKnox cyber-vaulting](06-fortknox-cyber-vaulting.md), [AI-powered security](07-ai-powered-data-security.md), and the [NetBackup/Veritas portfolio](08-netbackup-and-veritas.md). The lab situates it.

## Hands-On Lab

Python models the program. **Cost:** none.

### Lab 1.1 — Map the Academy certification tiers

**Objective:** Represent the three tiers and their credentials.

```bash
python3 - <<'EOF'
PROGRAM = {
  "Associate (CCPA)": [
    ("Protection Associate — DataProtect", "COH100"),
    ("Protection Associate — Multicloud", "—"),
  ],
  "Professional (CCIP / CCPP)": [
    ("Implementation Professional — SmartFiles", "CCIP"),
    ("Protection Professional", "CCPP"),
    ("Protection Professional — NetBackup", "CCPP (Veritas)"),
    ("Protection Professional — NetBackup and NetBackup Appliances", "CCPP (Veritas)"),
  ],
  "Specialist (CCSS)": [
    ("Security Specialist", "COH350"),
  ],
}
print("Cohesity Academy — three-tier certification program:\n")
total = 0
for tier, certs in PROGRAM.items():
    print(f"   {tier}")
    for name, code in certs:
        print(f"      - {name}  [{code}]")
        total += 1
    print()
print(f"   {total} certifications across 3 tiers\n")
print("The arc: ASSOCIATE (know + administer) -> PROFESSIONAL (implement + operate) ->")
print("SPECIALIST (security depth). The NETBACKUP certs come from the VERITAS merger")
print("(Dec 2024), extending the program to the enterprise-backup installed base. All")
print("PROCTORED, $200, valid 2 years, digital badge on pass — validating hands-on")
print("competence on the Cohesity Data Cloud for real data-protection job roles.")
EOF
```

**Expected result:** The seven certifications across Associate (CCPA), Professional (CCIP/CCPP, including two Veritas NetBackup credentials), and Specialist (CCSS) tiers. The program lesson is that Cohesity Academy runs a proctored, tiered program validating hands-on Data Cloud competence, with the NetBackup certifications reflecting the December 2024 Veritas merger.

**Negative test:** Assuming Cohesity certs are free online badges like some vendors. They are proctored, $200 exams validating hands-on platform skill — a different, competence-oriented model.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — The exam rule set

**Objective:** Reason about the proctored, two-year, retake design (COH100).

```bash
python3 - <<'EOF'
EXAM = {
  "number": "COH100 — Protection Associate, DataProtect",
  "duration_min": 90, "pass_pct": 58, "fee_usd": 200,
  "validity_years": 2, "retake_days": 14, "language": "English",
  "prereq": "none", "credential": "digital badge", "proctored": True,
}
print("COH100 (DataProtect Associate) — exam rule set:\n")
for k, v in EXAM.items():
    print(f"   {k:14}: {v}")
print()
print("Reading the design:")
print("  PROCTORED + hands-on domains (admin/monitor the Data Cloud; reporting, replication,")
print("     archival, file/object services) = validates DOING, not recall.")
print("  58% PASS = a real but attainable bar for an associate credential.")
print("  14-DAY RETAKE = a genuine cooldown to re-study, not an infinite-attempts grind.")
print("  2-YEAR VALIDITY = the platform evolves (AI features, cloud, the Veritas/NetBackup")
print("     portfolio), so the credential is refreshed rather than permanent.")
print("  ~3 MONTHS practical experience recommended -> aimed at people who OPERATE Cohesity.")
EOF
```

**Expected result:** The COH100 rule set — 90 minutes, 58% to pass, $200, two-year validity, 14-day retake, proctored, digital badge. The lesson is that the proctored format, hands-on domains, real passing bar, retake cooldown, and two-year validity together make the credential a refreshed validation of operating the Data Cloud, aimed at people with practical experience.

**Negative test:** Treating the exam as trivia to memorize. The domains require administering and monitoring the Data Cloud platform (reporting, replication, archival, file/object services); the proctored format and ~3-months-experience recommendation target hands-on operators.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The program understood — Cohesity Academy, three tiers, proctored exams, digital badges.
- [ ] The seven certifications and credentials (CCPA, CCIP, CCPP, CCSS) placed, including Veritas NetBackup.
- [ ] The exam mechanics known — proctored, $200, 90 min / 58% (COH100), two-year validity.
- [ ] Cohesity recognized as an AI-powered data-security leader, the peer of Rubrik (CXXX).
