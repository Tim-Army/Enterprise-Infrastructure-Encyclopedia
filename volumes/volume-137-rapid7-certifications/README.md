# Volume CXXXVII — Rapid7 Certification Tracks

> The certification map for **Rapid7**, whose Insight platform spans vulnerability management,
> SIEM/detection, application security, and automation — verified on the **Rapid7 Academy**, 4 August
> 2026. Four certification exams at **$215** each: **InsightVM (Rapid7 Vulnerability Management)
> Certified Administrator**, **InsightIDR (Rapid7 SIEM) Certified Specialist**, **InsightAppSec (Rapid7
> Application Security) Certified Specialist**, and **InsightConnect (Rapid7 Automation) Certified
> Specialist**. Enrollment runs through a **purchase order** and a **promo code** from the registration
> email rather than card checkout, and virtual instructor-led courses **include one exam attempt**.
> **InsightCloudSec and Metasploit have training but no certification exam.** Academy courses carry
> **16–24 CPE credits** toward ISC2 and ISACA renewals. The volume follows Rapid7's own **Vulnerability
> Management Lifecycle** — Discovery → Analyze → Communicate → Remediate — then covers the detection
> half, and models everything free in Python: scan coverage and blind spots, the credentialed-scan
> uplift, context-aware prioritization against raw CVSS, SLA aging, log attribution and silent parsing
> failure, deception trip-wires, precision and recall, and SOAR playbook gating. **Defensive
> throughout** — no Rapid7 license required.

## Overview

Volume CXXXVII is a **certification-tracks volume** organized by discipline rather than by product
screen. Chapter 02 covers the Insight platform's components and the agent-versus-scan coverage decision.
Chapters 03–05 walk Rapid7's published vulnerability-management lifecycle: discovery and assessment
(including why an uncredentialed program mostly measures its own blindness), analysis and prioritization
(why raw CVSS sends you to the wrong work), and communication and remediation (SLA aging, owned
remediation projects, verified closure, expiring exceptions). Chapters 06–07 cover the InsightIDR half —
log collection, attribution, the silent parsing failure, and **deception technology**, whose
near-zero-false-positive property makes it structurally different from behavioral detection. Chapter 08
covers InsightConnect (SOAR) and InsightAppSec (DAST), tying automation decisions to measured detection
precision. Chapter 09 closes on exam choice and the enrollment path.

Its place in the encyclopedia completes the **vulnerability-management trio** with
[Tenable LXXVIII](../volume-078-tenable-certifications/README.md) and
[Qualys LXXIX](../volume-079-qualys-certifications/README.md), and contributes to the detection shelf
alongside [Splunk XLV](../volume-045-splunk-certifications/README.md) and
[Elastic LXXXVI](../volume-086-elastic-certifications/README.md).

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Rapid7 Program and the Insight Platform](chapters/01-the-rapid7-program-and-insight-platform.md) | 1.1–1.2 |
| 02 | [Insight Platform Architecture](chapters/02-insight-platform-architecture.md) | 2.1–2.3 |
| 03 | [Vulnerability Discovery and Assessment](chapters/03-vulnerability-discovery-and-assessment.md) | 3.1–3.3 |
| 04 | [Analyze and Prioritize](chapters/04-analyze-and-prioritize.md) | 4.1–4.3 |
| 05 | [Communicate and Remediate](chapters/05-communicate-and-remediate.md) | 5.1–5.3 |
| 06 | [Log Collection and the Detection Pipeline](chapters/06-log-collection-and-the-detection-pipeline.md) | 6.1–6.3 |
| 07 | [Detections, Alerts, and Deception Technology](chapters/07-detections-alerts-and-deception.md) | 7.1–7.3 |
| 08 | [InsightConnect (SOAR) and InsightAppSec](chapters/08-insightconnect-and-insightappsec.md) | 8.1–8.3 |
| 09 | [Choosing an Exam, Currency, and Career](chapters/09-choosing-an-exam-currency-career.md) | 9.1–9.2 |

## What you will be able to do

- Map the four exams and plan around the purchase-order enrollment path.
- Combine agent and scan coverage, and find the blind spots each leaves.
- Quantify the credentialed-scan uplift and report coverage alongside findings.
- Prioritize with exploitability, exposure, and asset criticality instead of raw CVSS.
- Track SLA aging rather than open counts, and verify remediation by rescan.
- Attribute log events to people and machines, and detect silent parsing failure.
- Deploy deception that catches attackers with near-zero false positives.
- Measure detection precision and recall, and use precision to decide what may be automated.

## Prerequisites

- Security operations fundamentals; [Volume X](../volume-010-enterprise-cybersecurity/README.md) for the broader program.
- A Linux or macOS host with `python3` — every lab runs on the standard library, with no Rapid7 software.

## See also

- [Volume LXXVIII — Tenable](../volume-078-tenable-certifications/README.md) and [Volume LXXIX — Qualys](../volume-079-qualys-certifications/README.md) — the other two vulnerability-management programs; the discipline transfers completely.
- [Volume XLV — Splunk](../volume-045-splunk-certifications/README.md), [Volume LXXXVI — Elastic](../volume-086-elastic-certifications/README.md) — SIEM peers; [Volume L — CrowdStrike](../volume-050-crowdstrike-certifications/README.md) — endpoint.
- [Volume X — Enterprise Cybersecurity](../volume-010-enterprise-cybersecurity/README.md), [Volume XL — ISC2](../volume-040-isc2-certifications/README.md) — the program context and the CPE destination.
- [Master Appendices — Rapid7 appendix](../volume-997-master-appendices/chapters/71-appendix-rapid7-certifications-and-course-access.md) — exams, Academy content, and access.
