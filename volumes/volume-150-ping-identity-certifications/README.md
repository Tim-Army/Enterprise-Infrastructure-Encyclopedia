# Volume CL — Ping Identity Certification Tracks

> The Ping Identity Certified Professional program — verified 5 August 2026 on `training.pingidentity.com/certification`.
> The program is **product-specific**: proctored exams at the **Certified Professional** level (with **Advanced
> Administrator** and **Expert** tiers above), each tied to a product — **PingFederate** (federation, PFP-001),
> **PingAccess** (access management, PAP-001), **PingDirectory** (PDP-001), **PingOne** (cloud SSO+MFA, POP-001),
> **PingOne DaVinci** (orchestration, PODV-001), **PingOne Advanced Identity Cloud** (PAICP-001), **PingOne Identity
> Governance** (IGAP-001), and **PingAM** (PT-AM-CPE). Ping **publishes** the mechanics: each exam is remotely
> **proctored**, multiple choice, roughly **70 questions in 90 minutes**, priced **~$395** (€365/£310), with pass
> marks that **vary by product** (64% PingFederate/PingAccess, 67% PingDirectory, 68% DaVinci, 70% Advanced Identity
> Cloud/Governance, 75% PingOne), and a voucher valid for a single attempt. The portfolio reflects the **2023 Ping +
> ForgeRock merger** — Ping-origin plus rebranded ForgeRock-origin products. Every lab runs free in Python; PingOne
> offers free trials.

## Overview

Ping Identity is a leader in **identity and access management (IAM)** — authenticating users, authorizing access, and
federating identity across applications, for both **workforce** and **customer** (CIAM) identity. Where
[Okta (LXXVI)](../volume-076-okta-certifications/README.md) is the cloud-first IDaaS generalist and
[SailPoint (CXXXII)](../volume-132-sailpoint-certifications/README.md) owns governance, **Ping's depth is federation
and access management** — the enterprise **PingFederate** server and a broad portfolio across SSO, MFA, directory,
orchestration, and governance, widened by the ForgeRock merger.

Chapter 02 covers **IAM fundamentals** — authentication vs authorization, SSO, federation, and CIAM. Chapter 03 covers
**PingFederate** — SAML, OIDC, OAuth, and the signed assertion. Chapter 04 covers **PingAccess and PingAM** —
centralized, policy-based access. Chapter 05 covers **PingOne** — cloud IDaaS and elasticity. Chapter 06 covers
**MFA, passwordless, and PingOne Protect** — adaptive, risk-based authentication. Chapter 07 covers **PingOne
DaVinci** — no-code identity orchestration. Chapter 08 covers **PingDirectory and PingOne Identity Governance** — the
directory and the "should". Chapter 09 closes on choosing a path.

A theme runs through it: **identity is the control plane** — in a perimeter-less world, who you are and what you can
access is the security boundary, and Ping owns its federation-and-access backbone.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Ping Identity Certification Program](chapters/01-the-ping-identity-certification-program.md) | 1.1–1.2 |
| 02 | [Identity and Access Management Fundamentals](chapters/02-identity-and-access-management-fundamentals.md) | 2.1–2.2 |
| 03 | [Federation — PingFederate](chapters/03-federation-pingfederate.md) | 3.1–3.2 |
| 04 | [Access Management — PingAccess and PingAM](chapters/04-access-management-pingaccess-and-pingam.md) | 4.1 |
| 05 | [Cloud Identity — PingOne](chapters/05-cloud-identity-pingone.md) | 5.1 |
| 06 | [MFA, Passwordless, and Threat Protection](chapters/06-mfa-passwordless-and-threat-protection.md) | 6.1–6.2 |
| 07 | [Identity Orchestration — PingOne DaVinci](chapters/07-identity-orchestration-pingone-davinci.md) | 7.1 |
| 08 | [Directory and Governance](chapters/08-directory-and-governance.md) | 8.1 |
| 09 | [Choosing Your Ping Path](chapters/09-choosing-your-ping-path.md) | 9.1–9.2 |

## The product-specific certifications

| Exam (Certified Professional) | Code | Area | Pass |
| --- | --- | --- | --- |
| **PingFederate** | PFP-001 | Federation / SSO | 64% |
| **PingAccess** | PAP-001 | Access management | 64% |
| **PingDirectory** | PDP-001 | Directory | 67% |
| **PingOne** | POP-001 | Cloud SSO + MFA | 75% |
| **PingOne DaVinci** | PODV-001 | Orchestration | 68% |
| **PingOne Advanced Identity Cloud** | PAICP-001 | IAM SaaS (ex-ForgeRock) | 70% |
| **PingOne Identity Governance** | IGAP-001 | Governance | 70% |
| **PingAM** | PT-AM-CPE | Access management (ex-ForgeRock) | — |

Plus **Advanced Administrator** and **Expert** tiers above for some products.

## What you will be able to do

- Read the product-specific program and certify for the products you operate.
- Distinguish authentication from authorization, and explain SSO and federation.
- Configure PingFederate federation (SAML/OIDC/OAuth) and trust the signed assertion, with least-privilege scopes.
- Enforce centralized, policy-based access with PingAccess/PingAM.
- Weigh cloud IDaaS (PingOne) against on-prem, and administer a tenant.
- Apply MFA, passwordless, and adaptive risk-based authentication with PingOne Protect.
- Design no-code identity journeys in PingOne DaVinci.
- Run the directory at scale and govern access with certification and lifecycle.

## Prerequisites

- Familiarity with web authentication and enterprise applications helps.
- A Linux or macOS host with `python3`. **PingOne** offers free trials for hands-on practice.

## See also

- [Volume LXXVI — Okta](../volume-076-okta-certifications/README.md), [Volume CXXXII — SailPoint](../volume-132-sailpoint-certifications/README.md) — the IDaaS and governance pillars of enterprise identity.
- [Volume CXLVII — Wiz](../volume-147-wiz-certifications/README.md) — cloud entitlements (CIEM), the same effective-permission discipline in the cloud.
- [Volume CXLVI — Jamf](../volume-146-jamf-certifications/README.md) — Jamf Connect brings cloud identity to the Mac login, on federation Ping provides.
