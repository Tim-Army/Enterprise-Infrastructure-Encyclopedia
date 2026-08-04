# Chapter 01: The Rubrik Program and Cyber Resilience

![The Rubrik certification program: one active certification, RCSA (Rubrik Certified System Administrator), earned through Rubrik University via a free self-paced learning path or a paid hands-on Rubrik Security Cloud Administration bootcamp, with unlimited practice exams and a Credly badge (the older RCE is retired). All grounded in Rubrik Security Cloud — the Cyber Resilience Platform for Data and Identity: policy-driven data protection, immutable air-gapped backups, ransomware and cyber recovery with Data Threat Analytics, Data Security Posture Management, and identity resilience.](../../../diagrams/volume-130-rubrik-certifications/chapter-01-certification-program.svg)

*Figure 1-1. The Rubrik program: a focused certification (RCSA) on the Rubrik Security Cloud platform, plus topic workshops — all in service of cyber resilience: assume breach, protect immutably, recover fast.*

## Learning Objectives

- Describe the Rubrik certification program: RCSA (the active credential) and Rubrik University's free/paid paths.
- Understand cyber resilience and how Rubrik Security Cloud implements it.
- Know the platform's domains: data protection, immutability/air-gap, ransomware recovery, DSPM, and identity resilience.
- Set up a free study lab that models Rubrik's cyber-resilience concepts.

## What Rubrik certifies

**Rubrik** is a **Cyber Resilience Platform for Data and Identity**. Its premise is the modern security reality: **assume you will be breached** — by ransomware or an insider — and design so you can **recover fast and cleanly** anyway. The **Rubrik Security Cloud (RSC)** platform delivers immutable, air-gapped backups, ransomware/cyber recovery, data threat analytics, data security posture management (DSPM), and identity resilience.

The **Rubrik certification program** is deliberately focused: one active certification, **RCSA**, validates operational administration of the platform, with Rubrik University providing the learning paths.

## The certification and learning paths

Verified on training.rubrik.com (Rubrik University), 4 August 2026:

| Credential | What it validates | Preparation |
|:---|:---|:---|
| **RCSA — Rubrik Certified System Administrator** | Day-to-day operational administration of Rubrik Security Cloud (protecting data-center workloads) | **Free** self-paced eLearning path + **unlimited** practice exams; **or** a **paid** 4-day hands-on RSC Administration bootcamp (~60% labs) |
| ~~RCE — Rubrik Certified Engineer~~ | — | **Retired** (expired on Credly) |

Two study routes to RCSA: the **free learning path** (eLearning → practice exams with immediate feedback → final exam) or the **paid bootcamp** (instructor-led, hands-on labs; exam questions drawn from bootcamp content). Badges issue on **Credly**; **Rubrik Support credentials** are required to access Rubrik University. Beyond RCSA, Rubrik University offers topic **workshops** (Threat Detection & Incident Recovery, Protecting Cloud-Native Workloads, Protecting Database Workloads) — training, not separate certifications — which this volume folds into the relevant chapters.

## The Rubrik Security Cloud domains

| Domain | What it does |
|:---|:---|
| **Data protection** | Policy-driven (SLA Domains) protection of VMs, physical, NAS, databases, cloud, SaaS/M365 |
| **Immutability + air-gap** | Append-only, logically air-gapped backups ransomware cannot alter |
| **Ransomware / cyber recovery** | Anomaly detection, Data Threat Analytics, threat hunting/monitoring, orchestrated recovery |
| **DSPM** | Sensitive-data discovery, classification, and data-risk/access analytics |
| **Identity resilience** | Protect and recover identity systems (Active Directory / Entra ID) |

The through-line: **the backup is the last line of defense**, so it must be immutable and analyzable — you recover *known-clean* data fast, and you know *what* was exposed.

## Hands-On Lab

RCSA is a platform-administration certification; this volume **models** Rubrik's cyber-resilience concepts (immutability, anomaly detection, classification, recovery orchestration) with **free Python** — no Rubrik software or license required. **Cost:** none.

### Lab 1.1 — Map the program

**Objective:** Fix the certification and platform structure.

```bash
cat <<'EOF'
RCSA (active cert): Rubrik Certified System Administrator — operate Rubrik Security Cloud
  Free path:  self-paced eLearning + unlimited practice exams -> final exam
  Paid path:  4-day RSC Administration bootcamp (~60% hands-on labs)
  Badge: Credly | Access: Rubrik Support credentials required
RCE (Rubrik Certified Engineer): RETIRED
Platform (RSC): data protection · immutability/air-gap · ransomware recovery · DSPM · identity resilience
Cyber-resilience premise: ASSUME BREACH — protect immutably, recover fast and clean.
EOF
```

**Expected result:** The focused program — one active cert (RCSA), two study routes (free/paid), on the RSC platform. This structures the volume: [Chapter 02](02-rsc-architecture-data-protection.md) covers RSC/data protection (RCSA core), [03](03-immutability-and-air-gap.md) immutability, [04](04-ransomware-cyber-recovery.md) ransomware recovery, [05](05-dspm.md) DSPM, [06](06-recovery-orchestration.md) recovery, [07](07-workloads.md) workloads, [08](08-security-rbac-identity-resilience.md) security/identity.

**Negative test:** Studying for "RCE" — it's retired; RCSA is the active certification. Verify the current cert list on training.rubrik.com before scheduling.

**Cleanup:** None.

### Lab 1.2 — Stand up the study lab

**Objective:** Prepare the free primitives that model Rubrik's techniques.

```bash
python3 -c "import hashlib, re, json, datetime; print('stdlib available for immutability/anomaly/classification modeling')"
echo "lab ready: python models immutable/WORM backups, ransomware anomaly detection,"
echo "           data classification (DSPM), recovery orchestration, and RBAC — no Rubrik software"
```

**Expected result:** Python and its standard library present — this volume models immutability, anomaly detection, classification, recovery orchestration, and RBAC on one host, so the cyber-resilience concepts are concrete without the Rubrik platform.

**Negative test:** Expecting the labs to *be* Rubrik Security Cloud — they model the **concepts** RCSA tests; the real platform (production immutability, global data threat analytics, orchestrated mass recovery) carries the authoritative implementation this volume points to.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The focused program (RCSA active, RCE retired) and free/paid study routes understood.
- [ ] Cyber resilience (assume breach; protect immutably, recover fast) internalized.
- [ ] The RSC domains (protection, immutability, recovery, DSPM, identity) mapped.
- [ ] The free study lab stood up.
