# Volume CXLV — Atlassian Certification Tracks

> The Atlassian credential program — verified 4 August 2026 on `community.atlassian.com/learning/certifications`
> (Atlassian University moved here; `university.atlassian.com` now redirects). The program restructured into
> **three tiers plus designations**: **ACH** (Atlassian Certificate Holder — **free**, foundational, for app
> users), **ACA** (Atlassian Certified Associate — for professionals who *use* the apps), and **ACP**
> (Atlassian Certified Professional — role-based, for solution *administrators*). **Designations** stack
> multiple related credentials into a meta-credential. The program is aggressively **cloud-first**: Atlassian
> Server reached end of support in **February 2024**, and the catalog now leads with the "for Cloud"
> variants while Data Center certifications persist for on-premise holdouts. Preparation is largely **free** —
> on-demand training, exam-prep courses, and a free Cloud tier — with per-exam mechanics (question count,
> duration, passing score, price, validity) behind the credential portal, which this volume points to rather
> than asserting. Every lab runs free in Python; Atlassian Cloud's free tier makes the administration
> practice real.

## Overview

Atlassian owns the **plan-and-coordinate** layer of the software toolchain — **Jira** (work tracking),
**Confluence** (knowledge), **Jira Service Management** (ITSM) — where [GitLab (CXXXVI)](../volume-136-gitlab-certifications/README.md)
and [GitHub (LXXXIX)](../volume-089-github-certifications/README.md) own the code. Its certifications are
about administering that toolset well.

Chapter 02 covers **Jira administration** — company-managed versus team-managed projects, and the scheme
model whose shared configuration is both Jira's power and its blast-radius danger. Chapter 03 covers
**workflows, JQL, and automation**. Chapter 04 covers **Confluence administration** — spaces, the
narrow-never-widen permission model, and knowledge rot. Chapter 05 covers **cloud organization admin and
Atlassian Guard** — domain verification and SCIM. Chapter 06 covers **Jira Service Management**. Chapter 07
covers **agile at scale and the Marketplace**, including app-governance risk. Chapter 08 covers **migration
and Data Center**. Chapter 09 closes on choosing a path.

A theme runs through it: **shared configuration and third-party apps are power that becomes liability
without governance** — schemes, spaces, automation rules, and Marketplace apps all decay into sprawl unless
someone tends them.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Atlassian Credential Program](chapters/01-the-atlassian-credential-program.md) | 1.1–1.2 |
| 02 | [Jira Administration — Projects and Schemes](chapters/02-jira-administration-projects-and-schemes.md) | 2.1–2.3 |
| 03 | [Workflows, JQL, and Automation](chapters/03-workflows-jql-and-automation.md) | 3.1–3.3 |
| 04 | [Confluence Administration](chapters/04-confluence-administration.md) | 4.1–4.3 |
| 05 | [Cloud Organization Admin and Access](chapters/05-cloud-organization-admin-and-access.md) | 5.1–5.3 |
| 06 | [Jira Service Management and ITSM](chapters/06-jira-service-management-and-itsm.md) | 6.1–6.3 |
| 07 | [Agile at Scale and the Marketplace](chapters/07-agile-at-scale-and-marketplace.md) | 7.1–7.3 |
| 08 | [Migration and Data Center](chapters/08-migration-and-data-center.md) | 8.1–8.3 |
| 09 | [Choosing a Path, Currency, and Career](chapters/09-choosing-a-path-currency-career.md) | 9.1–9.2 |

## The three tiers

| Tier | Full name | For | Cost |
| --- | --- | --- | --- |
| **ACH** | Atlassian Certificate Holder | App users — foundational knowledge | **Free** |
| **ACA** | Atlassian Certified Associate | Professionals who *use* the apps | Paid |
| **ACP** | Atlassian Certified Professional | Solution *administrators* — role-based | Paid |

Plus **Designations** — meta-credentials for earning multiple credentials in a related path.

## What you will be able to do

- Read the three tiers as a responsibility ladder and certify at the tier matching your role.
- Choose company-managed versus team-managed projects, and edit shared schemes with blast-radius awareness.
- Design workflows people follow, write indexed-first JQL, and govern automation against loops.
- Administer Confluence permissions correctly (narrow, never widen) and fight knowledge rot.
- Secure the org with Atlassian Guard — domain verification and SCIM offboarding.
- Configure JSM with correct SLA pause handling, and size agent teams with deflection.
- Govern Marketplace apps by usage, vendor health, and data access.
- Plan a Data-Center-to-Cloud migration as a staged project, cleaning up first.

## Prerequisites

- Familiarity with software teams' planning and documentation workflows helps.
- A Linux or macOS host with `python3`. A **free Atlassian Cloud tier** (up to 10 users) makes the ACP
  administration practice real at no cost.

## See also

- [Volume CXXXVI — GitLab](../volume-136-gitlab-certifications/README.md), [Volume LXXXIX — GitHub](../volume-089-github-certifications/README.md) — the build layer Atlassian's plan layer sits above.
- [Volume LXXX — ServiceNow](../volume-080-servicenow-certifications/README.md) — the dedicated ITSM platform JSM competes with.
- [Volume LXXVI — Okta](../volume-076-okta-certifications/README.md), [Volume CXXXII — SailPoint](../volume-132-sailpoint-certifications/README.md) — the identity-lifecycle discipline behind Atlassian Guard's SCIM.
- [Volume CXLIV — SAP](../volume-144-sap-certifications/README.md), [Volume LXXXIII — Salesforce](../volume-083-salesforce-certifications/README.md) — the other module/role business-platform programs.
