# Volume CLVII — Cohesity Certification Tracks

> The Cohesity Academy certification program — verified 5 August 2026 on
> `cohesity.com/academy/certification`. Cohesity is a leader in **AI-powered data security and management**.
> Cohesity Academy runs **proctored** certification exams across **three tiers** — **Associate** (Protection
> Associate — DataProtect **COH100**, and Multicloud; credential **CCPA**), **Professional** (Implementation
> Professional — SmartFiles **CCIP**; Protection Professional and two **NetBackup** certs, credential **CCPP**),
> and **Specialist** (Security Specialist **COH350**, credential **CCSS**). Exams are **$200**, **valid 2 years**,
> and grant a **digital badge**; the DataProtect associate exam is **90 minutes / 58% to pass**. Cohesity
> **merged with Veritas in December 2024**, adding NetBackup. Every lab runs **free** in Python. **Defensive
> throughout** — protecting, recovering, and securing data against loss and ransomware.

## Overview

Cohesity is a leader in **AI-powered data security and management** — backup and recovery, ransomware
resilience, and data management across on-premises and cloud, consolidated onto the **Cohesity Data Cloud**.
The modern thesis is that **backup is both the last line of defense against ransomware and a prime target of
it**, so data management and data security have converged. The **December 2024 Veritas merger** added the
widely-deployed **NetBackup** enterprise backup line, making Cohesity the largest data-protection vendor.

The closest peer this shelf covers is [Rubrik (CXXX)](../volume-130-rubrik-certifications/README.md); **Cohesity
versus Rubrik** is the defining modern-data-security comparison, with [Commvault (CXXXIII)](../volume-133-commvault-certifications/README.md)
the enterprise-backup peer.

Chapter 02 frames **modern data security and management** — backup as a security function. Chapters 03–08 cover
the platform: **DataProtect** (backup, recovery, replication, archival), **ransomware resilience** (immutable
snapshots, DataLock/WORM, air-gapping, anomaly detection), **SmartFiles** (software-defined file and object
services), **FortKnox** (SaaS cyber-vaulting), **AI-powered data security** (DataHawk detection/classification
and Gaia generative search), and **NetBackup and the Veritas portfolio** (plus multicloud data management).
Chapter 09 closes on choosing a path.

A theme runs through it: **ransomware makes recovery a security imperative** — immutable, air-gapped, monitored
backups turn ransomware from a catastrophe into a recoverable event.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Cohesity Academy Certification Program](chapters/01-the-cohesity-program.md) | 1.1–1.2 |
| 02 | [Modern Data Security and Management](chapters/02-modern-data-security-and-management.md) | 2.1 |
| 03 | [DataProtect — Backup, Recovery, and Archival](chapters/03-dataprotect.md) | 3.1 |
| 04 | [Ransomware Resilience](chapters/04-ransomware-resilience.md) | 4.1 |
| 05 | [SmartFiles — Software-Defined File and Object Services](chapters/05-smartfiles.md) | 5.1 |
| 06 | [FortKnox — SaaS Cyber-Vaulting](chapters/06-fortknox-cyber-vaulting.md) | 6.1 |
| 07 | [AI-Powered Data Security](chapters/07-ai-powered-data-security.md) | 7.1 |
| 08 | [NetBackup and the Veritas Portfolio](chapters/08-netbackup-and-veritas.md) | 8.1 |
| 09 | [Choosing Your Cohesity Path](chapters/09-choosing-your-cohesity-path.md) | 9.1–9.2 |

## The certifications

| Tier | Certifications | Credential |
| --- | --- | --- |
| **Associate** | Protection Associate — DataProtect (COH100) · Protection Associate — Multicloud | **CCPA** |
| **Professional** | Implementation Professional — SmartFiles (**CCIP**) · Protection Professional · Protection Professional — NetBackup · Protection Professional — NetBackup and NetBackup Appliances (**CCPP**) | CCIP / CCPP |
| **Specialist** | Security Specialist (COH350) | **CCSS** |

Mechanics (COH100 exemplar): **proctored**, **90 minutes**, **58% to pass**, **$200**, **2-year validity**, 14-day retake, digital badge.

## What you will be able to do

- Read the three-tier Academy program and state its exam mechanics.
- Explain why backup is both the last line of defense and a ransomware target — data management and security converged.
- Apply policy-based protection, replication, archival, and fast mass recovery (DataProtect).
- Apply ransomware resilience — immutable snapshots, DataLock/WORM, air-gapping, anomaly detection, clean recovery.
- Consolidate unstructured data onto security-aware software-defined file and object services (SmartFiles).
- Use SaaS cyber-vaulting (FortKnox) for an isolated, immutable, air-gapped last-resort copy and clean-room recovery.
- Apply AI to data security — threat detection, classification, clean-recovery selection, and generative search (DataHawk/Gaia).
- Place the NetBackup/Veritas portfolio and multicloud data management in the combined program.

## Prerequisites

- Familiarity with backup, storage, and data-center or cloud operations helps.
- A Linux or macOS host with `python3`. The **Cohesity certifications** are proctored exams via Cohesity Academy.

## See also

- [Volume CXXX — Rubrik](../volume-130-rubrik-certifications/README.md) — the direct data-security peer; Cohesity vs Rubrik is *the* comparison.
- [Volume CXXXIII — Commvault](../volume-133-commvault-certifications/README.md) — enterprise backup and recovery.
- [Volume L — CrowdStrike](../volume-050-crowdstrike-certifications/README.md) and [Volume CLI — SentinelOne](../volume-151-sentinelone-certifications/README.md) — endpoint threat detection; the prevention side (Cohesity is the recovery side) of ransomware defense.
- [Volume CXXXVIII — Everpure / Pure Storage](../volume-138-everpure-purestorage-certifications/README.md) — the primary storage backup protects.
