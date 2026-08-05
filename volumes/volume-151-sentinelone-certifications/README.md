# Volume CLI — SentinelOne Certification Tracks

> The SentinelOne University program — verified 5 August 2026 on `sentinelone.com/global-services/university` and
> `university.sentinelone.com`. The program is **role-based** and issues **Credly** digital badges: **SIREN**
> (SentinelOne Incident Response Engineer — the flagship, ~**45 hours** of training before an online exam of
> multiple-choice and **scenario-based simulations**), **THP** (Threat Hunting Professional), **Administrator
> Levels 1–3** (policy → API automation), **CTP** (Certified Technical Professional, partners), and **CSP**
> (Certified Sales Professional). Exam **passing scores, durations, and validity are not published** — they sit
> behind SentinelOne University, so this volume asserts the program structure and the SIREN training expectation
> and points at the portal for the rest. Every lab runs free in Python; SentinelOne offers free trials of
> Singularity. **Defensive throughout** — this volume is about detecting, responding to, and recovering from
> threats.

## Overview

SentinelOne is a leader in **autonomous endpoint and extended security** — the **Singularity Platform** uses
**behavioral AI** running *on the agent* to detect and **autonomously respond** to threats at machine speed.
Where [CrowdStrike (L)](../volume-050-crowdstrike-certifications/README.md) pioneered cloud-delivered EDR,
SentinelOne's distinctive pitch is **autonomy on the agent** — the endpoint detects, correlates, responds, and
**rolls back** damage, even offline.

Chapter 02 covers **autonomous endpoint protection** — behavioral AI versus signatures and machine-speed
response. Chapter 03 covers **Storyline** — autonomous correlation of events into one attack narrative. Chapter
04 covers **detection and response** — the IR workflow and threat hunting. Chapter 05 covers **rollback and
remediation** — recovering ransomware-encrypted files. Chapter 06 covers **Singularity XDR and the Data Lake** —
cross-surface correlation and the AI SIEM. Chapter 07 covers **Purple AI and the AI SOC** — generative-AI
security operations. Chapter 08 covers **deployment, policy, and administration**. Chapter 09 closes on choosing
a path.

A theme runs through it: **the agent is autonomous, the human supervises** — machine-speed prevention,
correlation, and recovery free analysts to do judgment, hunting, and oversight.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The SentinelOne University Program](chapters/01-the-sentinelone-university-program.md) | 1.1–1.2 |
| 02 | [Autonomous Endpoint Protection](chapters/02-autonomous-endpoint-protection.md) | 2.1–2.2 |
| 03 | [Storyline — Autonomous Correlation](chapters/03-storyline-autonomous-correlation.md) | 3.1–3.2 |
| 04 | [Detection and Response — EDR Workflows](chapters/04-detection-and-response-edr-workflows.md) | 4.1–4.2 |
| 05 | [Rollback and Remediation](chapters/05-rollback-and-remediation.md) | 5.1–5.2 |
| 06 | [Singularity XDR and the Data Lake](chapters/06-singularity-xdr-and-the-data-lake.md) | 6.1 |
| 07 | [Purple AI and the AI SOC](chapters/07-purple-ai-and-the-ai-soc.md) | 7.1–7.2 |
| 08 | [Deployment, Policy, and Administration](chapters/08-deployment-policy-and-administration.md) | 8.1 |
| 09 | [Choosing Your SentinelOne Path](chapters/09-choosing-your-sentinelone-path.md) | 9.1–9.2 |

## The certifications

| Certification | For | Notes |
| --- | --- | --- |
| **SIREN** (Incident Response Engineer) | IR analysts, threat hunters, SOC | ~45h training; MC + simulations; the anchor |
| **THP** (Threat Hunting Professional) | Advanced analysts | Attack analysis, anomaly, SIEM/SOAR |
| **Administrator (Levels 1–3)** | Administrators | Policy → API automation |
| **CTP** / **CSP** | Partners / channel | Technical / sales |

## What you will be able to do

- Read the role-based program and certify for your seat (SIREN/THP for defenders, Administrator for operators).
- Explain behavioral-AI detection and why autonomous on-agent response beats machine-speed attacks.
- Investigate a Storyline — the correlated attack narrative — instead of stitching individual alerts.
- Walk the IR workflow (triage, scope, contain, remediate) and hunt proactively.
- Remediate completely and roll back ransomware-encrypted files without reimaging.
- Correlate across surfaces with XDR, and query the Data Lake / AI SIEM.
- Operate an AI-augmented SOC with Purple AI, validating rather than trusting.
- Deploy and tune policy (detect-first, then protect) balancing security against disruption.

## Prerequisites

- Familiarity with endpoint security and SOC concepts helps; prior EDR (e.g. CrowdStrike) experience transfers.
- A Linux or macOS host with `python3`. SentinelOne offers **free trials** of Singularity for hands-on practice.

## See also

- [Volume L — CrowdStrike](../volume-050-crowdstrike-certifications/README.md) — the EDR/XDR peer; concepts transfer.
- [Volume XLV — Splunk](../volume-045-splunk-certifications/README.md) — the SIEM/detection-engineering discipline the AI SIEM competes with.
- [Volume CXLVII — Wiz](../volume-147-wiz-certifications/README.md) — cloud security posture; Singularity Cloud overlaps, and cloud + endpoint is XDR.
- [Volume XLIII — OffSec](../volume-043-offensive-security-certifications/README.md) — understanding offense to hunt and defend better.
