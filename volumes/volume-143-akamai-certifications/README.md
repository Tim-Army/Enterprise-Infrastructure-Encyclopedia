# Volume CXLIII — Akamai Certification Tracks

> The Akamai edge platform and its credential landscape — verified 4 August 2026 on akamai.com
> (Akamai University: Customer Enablement) and the Akamai Credly issuer catalog (**192 badges**). Akamai's
> credentials divide into four groups that a résumé must keep apart: **University course badges** (the
> course-is-the-credential model — Web Performance, Media Delivery, Web App & API Protection, Bot & Abuse,
> Automation & DevOps, and more, each a Credly badge for completed ILT/VILT training); the **certification
> tier** with real exams (the **Guardicore** ladder — GCSA, GCSA Advanced, GCSE, GCSE On-Premise, and
> partner GCSP; the **API Security – Architect**; the **Cloud Computing Foundations Certification**); a
> **partner track** (Certified Partner Solutions Architect × 12 products, Partner Foundations/Advanced);
> and the **Akamai Technical Academy** Coursera certificates for career entry. Badge metadata publishes
> level, a Paid/Free flag, and a time-to-earn band — and **no exam durations, question counts, or passing
> scores are public for any credential**, so this volume asserts none. Every lab runs free in Python;
> Guardicore uniquely has a matching hands-on build already in this encyclopedia ([Volume XCV](../volume-095-akamai-guardicore-lab/README.md)).

## Overview

Akamai runs one of the internet's largest edge platforms and sells three businesses on it — delivery &
performance, security, and cloud computing. The immediate contrast is with
[Cloudflare (CXLII)](../volume-142-cloudflare-certifications/README.md): where Cloudflare is one
configuration model on one network with a self-serve free tier, Akamai is an enterprise estate — richer
per-product, configured per product, learned per course, priced per conversation — and the credential
program mirrors that exactly.

Chapter 02 covers the **intelligent edge** — DNS mapping (not anycast), Edge DNS, GTM, and the
Property Manager staging model. Chapter 03 covers **web performance and media delivery**, with offload
as a byte-weighted number. Chapters 04–06 cover the **security portfolio** — App & API Protector, the
bot/abuse/fraud family, API Security, and the Zero Trust products — defensively. Chapter 07 is the
**Guardicore segmentation certifications**, Akamai's deepest ladder, paired with the existing Volume XCV
lab. Chapter 08 covers **Akamai Cloud and automation**. Chapter 09 closes on choosing a path.

A recurring audit runs through the volume: **the inventory you enforce against must be discovered from
reality, not copied from documentation** — forgotten DNS answers, shadow APIs, unmapped east-west flows,
and drifted configs are the same failure at four layers.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Akamai Credential Landscape](chapters/01-the-akamai-credential-landscape.md) | 1.1–1.2 |
| 02 | [The Intelligent Edge — DNS, GTM, and Delivery](chapters/02-the-intelligent-edge-dns-and-delivery.md) | 2.1–2.3 |
| 03 | [Web Performance and Media Delivery](chapters/03-web-performance-and-media-delivery.md) | 3.1–3.3 |
| 04 | [App & API Protector](chapters/04-app-and-api-protector.md) | 4.1–4.3 |
| 05 | [Bot, Abuse, and Fraud Protection](chapters/05-bot-abuse-and-fraud.md) | 5.1–5.3 |
| 06 | [API Security and Zero Trust](chapters/06-api-security-and-zero-trust.md) | 6.1–6.3 |
| 07 | [Guardicore Segmentation Certifications](chapters/07-guardicore-segmentation-certifications.md) | 7.1–7.3 |
| 08 | [Akamai Cloud and Automation](chapters/08-akamai-cloud-and-automation.md) | 8.1–8.3 |
| 09 | [Choosing a Path, Currency, and Career](chapters/09-choosing-a-path-currency-career.md) | 9.1–9.2 |

## The credential groups

| Group | Examples | Nature |
| --- | --- | --- |
| **University course badges** | Web Performance Foundations & Offload, Media Delivery, WAAP, Bot & Abuse, Automation & DevOps | Course completion → Credly badge |
| **Certification tier** | **GCSA / GCSA Advanced / GCSE / GCSE On-Prem / GCSP**, **API Security – Architect**, **Cloud Computing Foundations** | Exams (mechanics unpublished) |
| **Partner track** | Certified Partner: Solutions Architect ×12, Partner Foundations/Advanced ×4 | Partner-org credentials |
| **Career entry** | Technical Academy (Coursera): Network Engineering; Customer Consulting & Support | Professional certificates |

## What you will be able to do

- Sort the 192-badge catalog into the ~21 credentials a practitioner can actually pursue.
- Reason about DNS mapping, GTM failover timing, and staged property activation.
- Compute byte-weighted offload and run the RUM steering loop.
- Operate the WAF/bot/API-security stack defensively, on the evaluate-then-enforce ladder.
- Design label-based segmentation policy and quantify blast-radius containment.
- Place Akamai Cloud by data gravity and manage the estate as code.

## Prerequisites

- Working familiarity with DNS, HTTP, TLS, and web/security operations.
- A Linux or macOS host with `python3`. For Guardicore, pair this volume with the hands-on
  [Volume XCV](../volume-095-akamai-guardicore-lab/README.md).

## See also

- [Volume CXLII — Cloudflare](../volume-142-cloudflare-certifications/README.md) — the edge comparison in every enterprise evaluation.
- [Volume XCV — Akamai Guardicore Build-It-Yourself Lab](../volume-095-akamai-guardicore-lab/README.md) — the hands-on build behind Chapter 07.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md), [Volume XXXV — Zscaler](../volume-035-zscaler-zero-trust-exchange/README.md), [Volume CXXVII — Netskope](../volume-127-netskope-certifications/README.md) — the zero-trust shelf.
- [Volume XVII — AWS](../volume-017-aws-architecture-security/README.md), [Volume XXXIII — Azure](../volume-033-microsoft-azure-certifications/README.md) — the hyperscalers Akamai Cloud does not try to be.
