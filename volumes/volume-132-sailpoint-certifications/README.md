# Volume CXXXII — SailPoint Certification Tracks

> The certification map for **SailPoint**, the identity security vendor whose products answer the
> governance question *who has access to what, should they, and can you prove it?* — verified on
> **Identity University** (university.sailpoint.com), 4 August 2026. SailPoint's program is distinctive
> for running **two parallel tracks**: three **Knowledge Credentials** (Identity Security **Leader**,
> **Professional**, **Expert**) that are training-gated, online, adaptive, free for your first attempts,
> and carry badges that **never expire**; and four proctored, role-based **Professional Certifications**
> — **Certified Identity Security Administrator** and **Certified Identity Security Engineer** on
> **Identity Security Cloud**, plus **Certified IdentityIQ Associate** and **Certified IdentityIQ
> Engineer** on on-premises **IdentityIQ** — which cost $300–$400, include **two attempts** with
> **364 days** to schedule, and renew on a **two-year Recertification Program** launched in February
> 2026. Seven exams; **12,000+** certified professionals. The volume teaches the underlying discipline —
> **Identity Governance and Administration (IGA)** — and models all of it free in Python: identity
> correlation, role mining, joiner-mover-leaver provisioning, separation-of-duties policy, certification
> campaigns, and transforms. No SailPoint license required.

## Overview

Volume CXXXII is a **certification-tracks volume** organized by SailPoint's own exam domains, which are
strikingly consistent across the four Professional Certifications: sources and identity data (02), access
modeling (03), identity lifecycle management and provisioning (04), governance and compliance (05),
platform and virtual appliances (06), and rules/transforms/workflows/APIs (07) — the last being the
material that separates the **Engineer** exam from the **Administrator** exam. Chapter 08 covers the
on-premises **IdentityIQ** track on its own terms (installation, build and deploy, Lifecycle Manager,
custom development, debugging), and Chapter 09 closes on path selection, recertification, and career.

Its distinctive contribution to the encyclopedia is **governance**: where [Okta
LXXVI](../volume-076-okta-certifications/README.md) covers access management and authentication and
[CyberArk LXXVII](../volume-077-cyberark-certifications/README.md) covers privileged access, this volume
covers the discipline that decides what access is *appropriate* and produces the audit evidence to prove
it.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The SailPoint Program and Identity Security](chapters/01-the-sailpoint-program-and-identity-security.md) | 1.1–1.2 |
| 02 | [The Identity Data Model and Sources](chapters/02-identity-data-model-and-sources.md) | 2.1–2.3 |
| 03 | [Access Modeling — Roles, Entitlements, and Access Profiles](chapters/03-access-modeling.md) | 3.1–3.3 |
| 04 | [Identity Lifecycle Management and Provisioning](chapters/04-lifecycle-management-and-provisioning.md) | 4.1–4.3 |
| 05 | [Governance and Compliance — Certifications, Policies, and Audit](chapters/05-governance-and-compliance.md) | 5.1–5.3 |
| 06 | [Platform, Virtual Appliances, and Connectivity](chapters/06-platform-virtual-appliances-connectivity.md) | 6.1–6.3 |
| 07 | [Rules, Transforms, Workflows, and APIs](chapters/07-rules-transforms-workflows-apis.md) | 7.1–7.3 |
| 08 | [IdentityIQ On-Premises](chapters/08-identityiq-on-premises.md) | 8.1–8.3 |
| 09 | [Choosing a Path, Recertification, Currency, and Career](chapters/09-choosing-recertification-currency-career.md) | 9.1–9.2 |

## What you will be able to do

- Map SailPoint's two tracks and all seven exams, and choose the right one for your product and role.
- Build an identity data model: aggregate, correlate, and find orphan and uncorrelated accounts.
- Design an access model (entitlements → access profiles → roles), mine roles, and avoid role explosion.
- Automate joiner-mover-leaver provisioning that revokes as reliably as it grants.
- Run certification campaigns, evaluate separation-of-duties policy, and produce audit evidence.
- Reason about virtual appliances, connectivity, transforms, rules, workflows, and APIs.

## Prerequisites

- Directory and identity fundamentals (Active Directory/LDAP, groups, accounts); [Volume X](../volume-010-enterprise-cybersecurity/README.md) for the defensive program.
- A Linux or macOS host with `python3` — every lab runs on the standard library, with no SailPoint software.

## See also

- [Volume LXXVI — Okta](../volume-076-okta-certifications/README.md) and [Volume LXXVII — CyberArk](../volume-077-cyberark-certifications/README.md) — the access-management and privileged-access halves of identity.
- [Volume XL — ISC2](../volume-040-isc2-certifications/README.md) — CISSP's identity-and-access-management domain at concept level.
- [Volume X — Enterprise Cybersecurity](../volume-010-enterprise-cybersecurity/README.md) — the broader security program.
- [Master Appendices — SailPoint appendix](../volume-997-master-appendices/chapters/66-appendix-sailpoint-certifications-and-course-access.md) — certifications, training paths, and access.
