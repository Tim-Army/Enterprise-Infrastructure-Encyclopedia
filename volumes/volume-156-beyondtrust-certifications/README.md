# Volume CLVI — BeyondTrust Certification Tracks

> The BeyondTrust University (BTU) certification program — verified 5 August 2026 on
> `beyondtrust.com/services/beyondtrust-university/get-certified`. BeyondTrust is a leader in
> **Privileged Access Management (PAM)**. The credential is the **BeyondTrust Certified Administrator**,
> issued as **Credly** verified digital badges, **one per product**. Each is granted on completion of the
> **required Instructor-Led Training (ILT)** course *and* a passing score of **75% or higher** on a
> **40-question** exam (rotating pools, online via the BTU portal, **open note** but completed
> independently, **two attempts**). Certifications are **valid for 2 years** (renew by purchasing new
> training and passing again) and grant **up to 16 CPE hours** per course. Eight products are covered.
> Every lab runs **free** in Python. **Defensive throughout** — vaulting credentials, enforcing least
> privilege, brokering sessions, and monitoring privileged access.

## Overview

BeyondTrust is a leader in **Privileged Access Management (PAM)** — securing, controlling, and monitoring
**privileged access** (administrator, root, and service accounts), the single most common path in a breach.
Its product line spans credential vaulting, endpoint least privilege, remote access, directory bridging,
and cloud entitlements, and **BeyondTrust University** certifies administrators on each. The other PAM
leader this shelf covers is [CyberArk (LXXVII)](../volume-077-cyberark-certifications/README.md); **BeyondTrust
versus CyberArk** is the defining PAM comparison.

Chapter 02 frames **the PAM discipline** — why privileged access is the attack path, and the controls
(vaulting, least privilege, session management, JIT). Chapters 03–08 take each product in turn:
**Password Safe** (vaulting, rotation, sessions), **Endpoint Privilege Management** (endpoint least
privilege on Windows/Mac/Linux), **Privileged Remote Access** (VPN-less brokered access with credential
injection), **Remote Support** (secure remote support, the Bomgar heritage), **AD Bridge** (extending
Active Directory to Linux/Unix/Mac), and **Entitle** (cloud/SaaS just-in-time access). Chapter 09 closes
on choosing a path.

A theme runs through it: **eliminate standing privilege** — replace always-on admin rights and shared
static passwords with brokered, monitored, time-bounded, just-in-time access.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The BeyondTrust University Certification Program](chapters/01-the-beyondtrust-program.md) | 1.1–1.2 |
| 02 | [Privileged Access Management — The Discipline](chapters/02-privileged-access-management.md) | 2.1–2.2 |
| 03 | [Password Safe — Vaulting, Rotation, and Sessions](chapters/03-password-safe.md) | 3.1–3.2 |
| 04 | [Endpoint Privilege Management](chapters/04-endpoint-privilege-management.md) | 4.1 |
| 05 | [Privileged Remote Access](chapters/05-privileged-remote-access.md) | 5.1 |
| 06 | [Remote Support](chapters/06-remote-support.md) | 6.1 |
| 07 | [AD Bridge](chapters/07-ad-bridge.md) | 7.1 |
| 08 | [Entitle — Cloud and SaaS Just-in-Time Access](chapters/08-entitle.md) | 8.1 |
| 09 | [Choosing Your BeyondTrust/PAM Path](chapters/09-choosing-your-beyondtrust-path.md) | 9.1–9.2 |

## The certifications

All eight are **BeyondTrust Certified Administrator** credentials (Credly badges), one per product, same mechanics:

| Product | Secures |
| --- | --- |
| **Password Safe** | Credential vaulting, rotation, privileged session management |
| **Endpoint Privilege Management — Windows** | Endpoint least privilege (Windows) |
| **Endpoint Privilege Management — Mac** | Endpoint least privilege (macOS) |
| **Endpoint Privilege Management — Linux** | Endpoint least privilege (Linux) |
| **Privileged Remote Access** | VPN-less brokered privileged access, credential injection |
| **Remote Support** | Secure remote support (Bomgar heritage) |
| **AD Bridge** | Extending Active Directory to Linux/Unix/Mac |
| **Entitle** | Cloud/SaaS just-in-time access |

Mechanics (uniform): **ILT prerequisite**, **40 questions**, **75% to pass**, two attempts, **2-year validity**, up to **16 CPE**.

## What you will be able to do

- Read the per-product Certified Administrator program and state its uniform exam mechanics precisely.
- Explain PAM — why privileged access is the primary attack path, and the controls that break the chain.
- Apply least privilege and just-in-time access to eliminate standing privilege.
- Describe Password Safe vaulting, rotation, and privileged session management.
- Apply endpoint least privilege — remove local admin, elevate the app not the user, application control.
- Broker VPN-less privileged access with credential injection (Privileged Remote Access), especially for vendors.
- Deliver secure, consent-based, recorded remote support (Remote Support).
- Extend Active Directory identity and policy to Linux/Unix/Mac (AD Bridge).
- Grant cloud/SaaS access just-in-time with self-service requests and auto-expiry (Entitle).

## Prerequisites

- Familiarity with identity, authentication, and systems administration helps.
- A Linux or macOS host with `python3`. The **BeyondTrust certifications** require instructor-led training via BTU.

## See also

- [Volume LXXVII — CyberArk](../volume-077-cyberark-certifications/README.md) — the other PAM leader; BeyondTrust vs CyberArk is *the* PAM comparison.
- [Volume CXXXII — SailPoint](../volume-132-sailpoint-certifications/README.md) — identity governance (IGA), the *what should you have* pillar.
- [Volume CL — Ping Identity](../volume-150-ping-identity-certifications/README.md) and [Volume LXXVI — Okta](../volume-076-okta-certifications/README.md) — access management, SSO, MFA — *who* logs in.
- [Volume CLV — Sysdig](../volume-155-sysdig-certifications/README.md) and [Volume CXLVII — Wiz](../volume-147-wiz-certifications/README.md) — cloud entitlement (CIEM), adjacent to Entitle's JIT.
- [Volume CXLVI — Jamf](../volume-146-jamf-certifications/README.md) — Apple-in-the-enterprise management, complementary to EPM for Mac.
