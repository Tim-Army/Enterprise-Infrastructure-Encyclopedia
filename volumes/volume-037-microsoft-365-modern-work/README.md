# Volume XXXVII — Microsoft 365 and Modern Work

> Administering the Microsoft 365 cloud: Entra ID identity and access,
> Intune-managed endpoints and Autopilot, Exchange/SharePoint/Teams
> workloads, and Microsoft Purview compliance and Defender XDR protection —
> the modern-work stack for a hybrid workforce.

## Overview

Volume XXXVII covers **Microsoft 365** as an administered platform: the
identity, endpoint, collaboration, compliance, and security services that a
modern organization runs from the cloud. It is the second of the
encyclopedia's three Microsoft volumes, sitting alongside the on-premises
[Volume XXXVI — Windows Server 2025 and Active Directory](../volume-036-windows-server-2025-active-directory/README.md)
and the platform-neutral
[Volume XXXIII — Microsoft Azure Certification Tracks](../volume-033-microsoft-azure-certifications/README.md).
Where Volume XXXVI ends — Microsoft Entra Connect projecting on-premises
identity into the cloud — this volume begins.

The volume is organized the way a Microsoft 365 administrator actually
works: **identity first** (Entra ID, authentication, Conditional Access,
governance), then **endpoints** (Intune enrollment, compliance,
configuration, apps, Autopilot), then the **workloads** (Exchange Online,
SharePoint and OneDrive, Teams), and finally **protection** (Microsoft
Purview information protection and compliance, and Microsoft Defender XDR).
Copilot and agent administration — now a first-class part of the modern-work
surface — is treated where it belongs, in identity, endpoint, and security
governance.

Chapters build cumulatively:

- **Chapters 01–04** establish the platform and identity: the tenant, admin
  centers and roles; Entra ID users, groups, devices, and RBAC;
  authentication, MFA, passwordless, and Conditional Access; and identity
  governance and hybrid identity.
- **Chapters 05–07** cover endpoint management: Intune enrollment and device
  management; compliance and configuration profiles with endpoint security;
  and application deployment with Windows Autopilot.
- **Chapters 08–09** cover the collaboration workloads: Exchange Online mail
  flow and protection; and SharePoint, OneDrive, and Teams administration.
- **Chapters 10–11** close with governance and defense: Microsoft Purview
  information protection, DLP, retention, and compliance; and Microsoft
  Defender XDR, Secure Score, Copilot and agent governance, and a capstone.

Every chapter follows the standard structure — learning objectives, theory
and architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references and
knowledge checks, a hands-on lab, and a summary and completion checklist —
defined in [templates/chapter.md](../../templates/chapter.md) and enforced
by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).

## Chapters

1. [Microsoft 365 and the Modern Work Platform](chapters/01-microsoft-365-and-the-modern-work-platform.md) — tenants, subscriptions and licensing, the admin centers, admin roles and delegation, and service health.
2. [Microsoft Entra ID — Identities, Groups, Devices, and Roles](chapters/02-microsoft-entra-id-identities-groups-devices-and-roles.md) — users and groups, device identity and join types, administrative units, and role-based access control.
3. [Authentication and Access — MFA, Passwordless, and Conditional Access](chapters/03-authentication-and-access-mfa-passwordless-and-conditional-access.md) — authentication methods, MFA and passwordless, Conditional Access, and Entra ID Protection.
4. [Identity Governance and Hybrid Identity](chapters/04-identity-governance-and-hybrid-identity.md) — Privileged Identity Management, access reviews, entitlement management, and Entra Connect/cloud sync.
5. [Microsoft Intune — Enrollment and Device Management](chapters/05-microsoft-intune-enrollment-and-device-management.md) — Intune setup, platform enrollment, device inventory, and the management lifecycle.
6. [Compliance Policies, Configuration Profiles, and Endpoint Security](chapters/06-compliance-policies-configuration-profiles-and-endpoint-security.md) — device compliance, configuration and settings-catalog profiles, and endpoint security baselines.
7. [Application Management and Windows Autopilot](chapters/07-application-management-and-windows-autopilot.md) — app deployment and protection policies, and zero-touch provisioning with Windows Autopilot.
8. [Exchange Online — Recipients, Mail Flow, and Protection](chapters/08-exchange-online-recipients-mail-flow-and-protection.md) — mailboxes and recipients, mail flow and connectors, and Exchange Online Protection.
9. [SharePoint Online, OneDrive, and Microsoft Teams](chapters/09-sharepoint-online-onedrive-and-microsoft-teams.md) — sites and sharing, OneDrive, and Teams administration, policies, and voice.
10. [Microsoft Purview — Information Protection, DLP, Retention, and Compliance](chapters/10-microsoft-purview-information-protection-dlp-retention-and-compliance.md) — sensitivity labels, data loss prevention, retention and records, and compliance solutions.
11. [Microsoft Defender XDR, Secure Score, Copilot Governance, and Capstone](chapters/11-microsoft-defender-xdr-secure-score-copilot-governance-and-capstone.md) — Defender for Office 365, Endpoint, and Cloud Apps, Secure Score, Microsoft 365 Copilot and agent governance, and a capstone.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all eleven chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume maps to Microsoft's **Microsoft 365** and **Security** role-based
certifications, as recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). The broader
role-based program beyond Azure is catalogued in Volume XXXVIII; this is a
product/administration volume mapped to the exams below.

| Certification | Exam | Primarily covered by |
| --- | --- | --- |
| **Microsoft 365 Certified: Fundamentals** | MS-900 | Chapter 01 |
| **Microsoft 365 Certified: Administrator Expert** | MS-102 | Chapters 01–04, 08–11 |
| **Microsoft 365 Certified: Endpoint Administrator Associate** | MD-102 | Chapters 05–07 |
| **Microsoft 365 Certified: Teams Administrator Associate** | MS-700 | Chapter 09 |
| **Microsoft 365 Certified: Collaboration Communications Systems Engineer** | MS-721 | Chapter 09 |
| **Microsoft Certified: Identity and Access Administrator** | SC-300 | Chapters 02–04 |
| **Microsoft Certified: Information Security Administrator** | SC-401 | Chapter 10 |
| **Microsoft Certified: Security Operations Analyst** | SC-200 | Chapter 11 |

Exam codes were verified against Microsoft Learn on 26 July 2026. Microsoft
retires and renames exams frequently — for example **SC-401** replaced the
former Information Protection Administrator (SC-400), and **Cloud and AI
Security Engineer (SC-500)** is a newer identity/security credential —
so confirm the current exam names, numbers, and status on Microsoft Learn
before scheduling.

## Lab coverage

Every chapter carries a Hands-On Lab of topic-level walkthroughs, one per
major administrative task, mapped to the MS-102/MD-102/SC-300 skills. Because
Microsoft 365 is a cloud SaaS platform, labs pair **admin-center
walkthroughs** with **Microsoft Graph PowerShell** commands (the supported
automation surface) so each task can be performed clickpath-free and
repeatably. Each lab states an objective, prerequisites, expected results
with representative output, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off until a human runs it.

Labs assume a Microsoft 365 tenant — a free **Microsoft 365 Developer** or
trial tenant is sufficient for most steps. The reasoning and the Graph
PowerShell can be followed without one, but the sign-off is reserved for an
actual run.

## Software and platform baseline

Chapters target the current **Microsoft 365 admin center**, **Microsoft
Entra admin center**, **Microsoft Intune admin center**, **Exchange admin
center**, **SharePoint admin center**, **Teams admin center**, and the
**Microsoft Purview** and **Microsoft Defender** portals, plus the
**Microsoft Graph PowerShell SDK** and **Microsoft Graph** for automation.
Microsoft 365 is a continuously updated service; confirm current cmdlet
syntax, portal paths, and licensing against Microsoft Learn before
production use.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-037-microsoft-365-modern-work
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
