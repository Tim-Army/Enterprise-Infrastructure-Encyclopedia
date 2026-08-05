# Volume CXLIV — SAP Certification Tracks

> The SAP certification program — verified 4 August 2026 on sap.com and learning.sap.com. The defining
> current fact is a **transformation**: through Q1 2026 SAP is moving all certifications from
> multiple-choice to **practical, performance-based exams** — system-based tasks or roleplay scenarios,
> timeboxed around real project work, **open-book with AI-supported tools allowed**, and **not
> live-proctored** ("most exams available by mid-January 2026, all transitioned by end-March"). The
> reasoning is the AI-era one: when AI handles recall, the exam tests **application**, not memorization —
> "prove what you can do, not just what you know." Three levels structure the vast catalog: **Associate**
> (fundamental, supervised — the bulk, `C_` codes), **Specialist** (a focused add-on), and **Professional**
> (advanced, requiring *proven project experience* — e.g. 24 months of ERP work in the past 36). SAP
> publishes **prices** (USD 276 two-attempt bundle including 10 practice-system hours; a Learning Hub
> subscription with four attempts); per-exam duration and passing score vary by the new format and are not
> uniformly published. Every lab runs free in Python — SAP itself is enterprise software, so the labs model
> the decisions and disciplines the practical exams now test.

## Overview

SAP is the dominant enterprise-software vendor, and its certification program is correspondingly vast —
hundreds of certifications across finance, HR, procurement, development, and platform. The organizing
truth is **specialize, don't generalize**: you certify in a *solution area* at a *level*, never "in SAP."

Chapter 02 covers **S/4HANA and the RISE context** — the HANA in-memory data model, the three cloud
editions, and RISE/GROW. Chapter 03 covers **SAP Activate**, the certified implementation methodology,
and fit-to-standard. Chapter 04 covers **BTP and ABAP Cloud** — the clean-core principle and side-by-side
extension. Chapter 05 covers **SuccessFactors and the line-of-business suites**, including the partner-only
provisioning caveat. Chapter 06 covers **analytics, data, and Business AI** — Joule assistants versus
agents. Chapter 07 is **the practical-exam transition**, the volume's centerpiece. Chapter 08 covers
**security, compliance, and authorizations** — segregation of duties — defensively. Chapter 09 closes on
choosing a path.

A theme runs through it: **every customization is a liability, and the whole modern SAP program —
fit-to-standard, clean core, practical exams — is organized around that fact.**

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The SAP Certification Program](chapters/01-the-sap-certification-program.md) | 1.1–1.2 |
| 02 | [S/4HANA and the RISE Context](chapters/02-s4hana-and-the-rise-context.md) | 2.1–2.3 |
| 03 | [SAP Activate and Project Methodology](chapters/03-sap-activate-and-project-methodology.md) | 3.1–3.3 |
| 04 | [BTP and ABAP Cloud Development](chapters/04-btp-and-abap-cloud-development.md) | 4.1–4.3 |
| 05 | [SuccessFactors and the Line-of-Business Suites](chapters/05-successfactors-and-the-line-of-business-suites.md) | 5.1–5.3 |
| 06 | [Analytics, Data, and Business AI](chapters/06-analytics-data-and-business-ai.md) | 6.1–6.3 |
| 07 | [The Practical Exam Transition](chapters/07-the-practical-exam-transition.md) | 7.1–7.3 |
| 08 | [Security, Compliance, and Authorizations](chapters/08-security-compliance-and-authorizations.md) | 8.1–8.3 |
| 09 | [Choosing a Path, Currency, and Career](chapters/09-choosing-a-path-currency-career.md) | 9.1–9.2 |

## The program at a glance

| Level | Certifies | Prefix |
| --- | --- | --- |
| **Associate** | Fundamental consultant knowledge, applied under supervision (the bulk) | **C_** |
| **Specialist** | A focused role or integration component, added to an Associate | varies |
| **Professional** | Advanced — requires **proven, recent project experience** | **P_**, some **E_** |

**Purchasing:** attempt bundles (one / two / six) or a Learning Hub subscription — the **two-attempt bundle
is USD 276 and includes 10 hours of hands-on practice-system access**, because the practical exam is
prepared for by *doing*, not memorizing.

## What you will be able to do

- Read a certification as area + module + level, and choose a path in that order.
- Explain S/4HANA's data-model simplification and why conversion is a project.
- Apply fit-to-standard and clean-core, treating every customization as a permanent liability.
- Navigate the LoB suites, including the partner-only provisioning constraint.
- Distinguish Joule assistants from agents, and positioning certs from developer certs.
- Prepare for a practical, open-book, AI-allowed exam — hands-on hours, not question dumps.
- Reason about segregation of duties and design roles that pass audit.

## Prerequisites

- Familiarity with enterprise business processes (finance, HR, or procurement) helps but is not required.
- A Linux or macOS host with `python3`. SAP practice systems come with the certification purchase; the
  labs here model the decisions at no cost.

## See also

- [Volume CXXIII — IBM](../volume-123-ibm-certifications/README.md), [Volume XLVII — Oracle](../volume-047-oracle-certifications/README.md) — the other vast specialize-don't-generalize enterprise catalogs.
- [Volume LXXX — ServiceNow](../volume-080-servicenow-certifications/README.md), [Volume LXXXIII — Salesforce](../volume-083-salesforce-certifications/README.md) — business-platform programs with the same module/level structure.
- [Volume CXXXV — Confluent](../volume-135-confluent-certifications/README.md) — the integration discipline SAP's BTP chapter shares.
- [Volume XXXVIII — Microsoft Beyond Azure](../volume-038-microsoft-certifications-beyond-azure/README.md), [Volume CXXXVI — GitLab](../volume-136-gitlab-certifications/README.md) — the AI-era certification wave SAP is now part of.
