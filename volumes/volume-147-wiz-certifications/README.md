# Volume CXLVII — Wiz Certification Tracks

> The Wiz Certified program — verified 5 August 2026 on `wiz.io/wiz-certified` and the Wiz blog. Launched
> **February 2025**, it is an **expanding portfolio** of **proctored** exams (taken online or at an onsite test
> center) open to Wiz customers, partners, and cloud security professionals. Three exams exist as of 2026:
> **Wiz Certified Cloud User** (entry-level user), **Wiz Certified Cloud Fundamentals** (the first exam;
> validates deploying and managing Wiz Cloud and is the **prerequisite** for future specialized exams), and
> **Wiz Certified Defend Fundamentals** (cloud threat detection and response with Wiz Defend). The **Defend
> Fundamentals mechanics are public**: **60 multiple-choice questions in 150 minutes**, a **two-year**
> certification, and a **shareable badge**; Wiz recommends the *Wiz for Threat Detection and Response* course
> plus two months of hands-on time. Exact mechanics for Cloud User and Cloud Fundamentals are portal-gated —
> this volume asserts the Defend numbers and points at the Wiz Certified homepage for the rest. Training is
> **free** through the **CloudSec Academy**. Every lab runs free in Python; Wiz offers a free demo/trial.

## Overview

Wiz is a **CNAPP** (Cloud-Native Application Protection Platform) — it finds, prioritizes, and helps remediate
cloud risk, and (with Wiz Defend) detects and responds to threats at runtime. Its defining idea is the **Wiz
Security Graph**: rather than a flat list of thousands of findings, Wiz builds a graph of cloud resources and
their relationships and surfaces the **attack paths** — the *toxic combinations* of exposure, vulnerability,
privilege, and data access that form an actually-exploitable route. The certifications validate that you can
operate the platform that thinks this way.

Chapter 02 covers **CNAPP and the Security Graph** — the consolidation of CSPM/CWPP/CIEM/DSPM and agentless
scanning. Chapter 03 covers **attack paths and toxic combinations** — the signature Wiz concept: prioritize
the path, not the pile. Chapter 04 covers **agentless posture** — CSPM and in-context vulnerability
management. Chapter 05 covers **CIEM and DSPM** — effective permissions and sensitive-data exposure, the two
ends of the path. Chapter 06 covers **Wiz Code** — shift-left security of code, IaC, and secrets with
code-to-cloud tracing. Chapter 07 covers **Wiz Defend** — cloud detection and response, defensively. Chapter
08 covers **operationalizing Wiz** — Posture Issues, democratization, and guardrails. Chapter 09 closes on
choosing a path.

A theme runs through it: **risk lives in the relationships**, so a graph beats a list — the few findings on a
path to a crown jewel matter, and the many that are not can wait.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Wiz Certified Program](chapters/01-the-wiz-certified-program.md) | 1.1–1.2 |
| 02 | [CNAPP and the Wiz Security Graph](chapters/02-cnapp-and-the-security-graph.md) | 2.1–2.2 |
| 03 | [Attack Paths and Toxic Combinations](chapters/03-attack-paths-and-toxic-combinations.md) | 3.1–3.2 |
| 04 | [Agentless Posture — CSPM and Vulnerabilities](chapters/04-agentless-posture-and-vulnerabilities.md) | 4.1–4.2 |
| 05 | [CIEM and DSPM — Identity and Data](chapters/05-ciem-and-dspm-identity-and-data.md) | 5.1–5.2 |
| 06 | [Wiz Code — Shift-Left](chapters/06-wiz-code-shift-left.md) | 6.1–6.2 |
| 07 | [Wiz Defend — Detection and Response](chapters/07-wiz-defend-detection-and-response.md) | 7.1–7.2 |
| 08 | [Operationalizing Wiz](chapters/08-operationalizing-wiz.md) | 8.1–8.2 |
| 09 | [Choosing Your Wiz Path](chapters/09-choosing-your-wiz-path.md) | 9.1–9.2 |

## The exams

| Exam | Validates | Mechanics |
| --- | --- | --- |
| **Cloud User** | Using Wiz Cloud day-to-day | Portal-gated |
| **Cloud Fundamentals** | Deploying & managing Wiz Cloud (the **prerequisite keystone**) | Portal-gated |
| **Defend Fundamentals** | Cloud threat detection & response (Wiz Defend) | **60 Q / 150 min / 2-year / badge** |

The program is young and expanding — the **pillars** (Wiz Code, Wiz Cloud, Wiz Defend) are the stable map.

## What you will be able to do

- Read the exam ladder as fundamentals-first and pillar-aligned, and pick the pillar that matches your job.
- Explain CNAPP as the consolidation of CSPM/CWPP/CIEM/DSPM, unified by the Security Graph and agentless scanning.
- Prioritize by attack path and toxic combination, and find the chokepoint fix that severs a path.
- Rank misconfigurations and vulnerabilities by graph context rather than raw CVSS.
- Compute effective (chain-resolved) permissions and rank sensitive-data exposure.
- Shift left with Wiz Code, tracing a cloud finding to the IaC line that caused it and fixing at the source.
- Enrich a runtime detection with graph context and trace an incident code-to-cloud-to-runtime.
- Operationalize with Posture Issues and democratization so security scales with the org.

## Prerequisites

- Familiarity with at least one public cloud (AWS, Azure, or GCP) and basic IAM concepts helps.
- A Linux or macOS host with `python3`. A **free Wiz demo/trial** and the **CloudSec Academy** make the practice real at no cost.

## See also

- [Volume XVII — AWS Architecture & Security](../volume-017-aws-architecture-security/README.md), [Volume XXXIII — Microsoft Azure](../volume-033-microsoft-azure-certifications/README.md), [Volume XXXIV — Google Cloud](../volume-034-google-cloud-certifications/README.md) — the clouds Wiz secures.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the network side of attack-path reduction.
- [Volume L — CrowdStrike](../volume-050-crowdstrike-certifications/README.md), [Volume LXV — Palo Alto Networks](../volume-065-palo-alto-networks-certifications/README.md) — the competitive CNAPP/CDR landscape.
- [Volume XLV — Splunk](../volume-045-splunk-certifications/README.md) — the SIEM/SOC pipeline Wiz Defend telemetry feeds.
