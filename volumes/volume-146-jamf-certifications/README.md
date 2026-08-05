# Volume CXLVI — Jamf Certification Tracks

> The Jamf certification program — verified 5 August 2026 on `trainingcatalog.jamf.com` and `jamf.com/training`.
> Jamf structures its credentials as **numbered courses**, each culminating in a certification exam, across
> **three product tracks**: **Jamf Pro** (Apple device management — the flagship: **100** self-paced →
> Certified Associate, **200** → Certified Tech, **300** → Certified Admin, **400** → Certified Expert),
> **Jamf School** (education — **140** → Associate, **240** → Tech), and **Jamf Protect** (Apple endpoint
> security — **170** → Associate, **270** → Tech, **370** → Admin). The numbering encodes both level (leading
> digit) and track (middle digit: `x0x` Pro, `x4x` School, `x7x` Protect). Distinctively, the **exam format
> escalates with the level** — Associate is multiple choice (knowledge), Tech adds practical tasks (can you do
> it), Admin uses graded scenarios (judgment), Expert is scenario-based (design). The **Jamf 100 specifics are
> public**: USD 100, 50 multiple-choice questions, and the Associate certification **does not expire**, while
> the 200–400 certifications carry a **three-year validity**. Per-exam passing scores and exact durations for
> the instructor-led 200–400 courses are portal-gated, and instructor-led pricing is arranged rather than
> listed — this volume points to the training portal for those rather than asserting them. Every lab runs free
> in Python; Jamf offers a **free trial** of Jamf Pro and the self-paced Jamf 100 course as the on-ramp.

## Overview

Jamf is the leader in **Apple enterprise management** — deploying, configuring, securing, and supporting Mac,
iPhone, iPad, and Apple TV at scale. Where [Microsoft Intune (XXXVII)](../volume-037-microsoft-365-modern-work/README.md)
is the cross-platform generalist, **Jamf is the Apple specialist**, going deeper on Apple's own management
framework than a generalist can — and that depth is what its certifications validate.

Chapter 02 covers **Apple management fundamentals** — the MDM framework Jamf implements (cooperative, not
coercive), supervision, zero-touch enrollment via Apple Business Manager, and declarative device management
(DDM). Chapter 03 covers **Smart Groups and scope** — criteria-based membership and the pre-flight discipline
that keeps a change off the wrong devices. Chapter 04 covers **configuration profiles and patch management** —
declarative settings versus imperative actions, and patch compliance as a live risk number. Chapter 05 covers
**scripts, Self Service, and app deployment** — the push-versus-offer line and VPP-via-ABM. Chapter 06 covers
**Jamf Connect** — cloud identity and password synchronization at the Mac login window. Chapter 07 covers
**Jamf Protect** — Apple-native endpoint security, defensively (telemetry, threat prevention, compliance).
Chapter 08 covers **Jamf School and compliance** — shared-device education workflows and the CIS macOS
benchmark. Chapter 09 closes on choosing a path, currency, and the Apple-in-enterprise career.

A theme runs through it: **Apple management is cooperative, not coercive** — Jamf can only do what Apple's
framework permits, and the admin who designs with that grain (Smart Groups, declarative state, zero-touch,
identity-anchored login) succeeds where one who expects Windows-style total control is surprised.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Jamf Certification Ladder](chapters/01-the-jamf-certification-ladder.md) | 1.1–1.2 |
| 02 | [Apple Management Fundamentals](chapters/02-apple-management-fundamentals.md) | 2.1–2.3 |
| 03 | [Jamf Pro — Smart Groups and Scope](chapters/03-jamf-pro-smart-groups-and-scope.md) | 3.1–3.3 |
| 04 | [Configuration Profiles and Patch Management](chapters/04-configuration-profiles-and-patch-management.md) | 4.1–4.3 |
| 05 | [Scripts, Self Service, and App Deployment](chapters/05-scripts-self-service-and-app-deployment.md) | 5.1–5.3 |
| 06 | [Jamf Connect — Identity](chapters/06-jamf-connect-identity.md) | 6.1–6.2 |
| 07 | [Jamf Protect — Endpoint Security](chapters/07-jamf-protect-endpoint-security.md) | 7.1–7.2 |
| 08 | [Jamf School and Compliance](chapters/08-jamf-school-and-compliance.md) | 8.1–8.2 |
| 09 | [Choosing Your Jamf Path](chapters/09-choosing-your-path.md) | 9.1–9.2 |

## The three tracks

| Track | Courses → certifications | For |
| --- | --- | --- |
| **Jamf Pro** (flagship) | 100 → Associate · 200 → Tech · 300 → Admin · 400 → Expert | Apple device management |
| **Jamf School** | 140 → Associate · 240 → Tech | Education (shared devices, classroom) |
| **Jamf Protect** | 170 → Associate · 270 → Tech · 370 → Admin | Apple endpoint security (defensive) |

The **numbering is the map**: leading digit = level (1/2/3/4), middle digit = track (`x0x` Pro, `x4x` School,
`x7x` Protect) — so `370` reads as Protect Admin.

## What you will be able to do

- Read the ladder by track and level, and match a track to your job (manage / educate / secure).
- Explain the Apple MDM framework Jamf implements — supervision, zero-touch enrollment, and DDM.
- Design Smart Groups as live, criteria-based membership, and pre-flight a scope before deploying to it.
- Distinguish configuration profiles (maintained settings) from policies (one-shot actions), and run patching as a live risk number.
- Draw the Self Service push-versus-offer line and pick the right app-deployment model (VPP via ABM, package).
- Anchor the Mac login to cloud identity with Jamf Connect, closing local-account password drift and the offboarding gap.
- Defend Apple endpoints with Jamf Protect — Apple-aware telemetry, threat prevention, and continuous CIS compliance.
- Manage education's shared-device model with Jamf School, and compose profiles, Smart Groups, and monitoring into a compliance posture.

## Prerequisites

- Familiarity with endpoint management concepts helps; prior Windows/Intune experience is useful *if you set aside its coercive assumptions*.
- A Linux or macOS host with `python3`. A **free Jamf Pro trial** and the self-paced **Jamf 100** course make the practice real at no cost.

## See also

- [Volume XXXVII — Microsoft 365 Modern Work](../volume-037-microsoft-365-modern-work/README.md) — Intune, the cross-platform generalist many shops run alongside Jamf for Apple depth.
- [Volume LXXVI — Okta](../volume-076-okta-certifications/README.md), [Volume CXXXII — SailPoint](../volume-132-sailpoint-certifications/README.md) — the identity-as-control-plane discipline behind Jamf Connect.
- [Volume XLV — Splunk](../volume-045-splunk-certifications/README.md) — the SIEM/SOC pipeline Jamf Protect telemetry feeds.
- [Volume XLI — CNCF Kubernetes](../volume-041-cncf-kubernetes-certifications/README.md), [Volume XLII — HashiCorp](../volume-042-hashicorp-certifications/README.md) — the declarative desired-state model DDM mirrors.
