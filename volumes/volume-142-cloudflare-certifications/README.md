# Volume CXLII — Cloudflare Certification Tracks

> The Cloudflare platform and its certification program — verified 4 August 2026 on
> `certifications.cloudflare.com`, the Connect 2026 University page, and Cloudflare's partner-program
> blog. The certification track is the **youngest on this shelf**: two Associate exams — the
> **Application Security Associate** and the **Zero Trust Associate** — delivered on **Cloudflare's own
> exam platform**, whose public portal still shows "Register Interest." At **Connect 2026** (October
> 19–21, San Francisco) a **$495 University Pass** adds a training day plus **one attempt at both
> exams, in-person proctored**. **Duration, question count, passing score, validity, and standalone
> pricing are not published; this volume asserts none of them.** A separate **partner accreditation
> track** (Accredited Sales Professional, Sales Engineer, Configuration Engineer, Services Architect,
> and a Workers Developer in development) is a different kind of credential, and this volume keeps the
> two firmly apart. Every lab runs free in Python — and Cloudflare's free tier covers nearly the whole
> practice syllabus, which no other vendor on this shelf matches.

## Overview

Cloudflare's architecture is one idea applied everywhere: a global **anycast edge network** that your
traffic reaches first, where caching, inspection, filtering, and compute happen before anything
touches your origin or leaves your users. The two exams map onto the two product families that run on
it — **Application Security** (Chapters 03–04) and **Cloudflare One / Zero Trust** (Chapters 05–06) —
with the substrate itself in Chapter 02 and the Workers developer platform in Chapter 07.

Chapter 02 covers **anycast, DNS, and caching**, including the gray-cloud origin-exposure audit.
Chapters 03–04 cover the **WAF, rate limiting, DDoS, Bot Management, and API Shield**, defensively,
on the log → challenge → block ladder. Chapters 05–06 cover **Access, Gateway, WARP, and Tunnel** —
per-application access, egress filtering, and the inversion that closes inbound ports entirely.
Chapter 08 covers **operating it all as code**, with drift detection on security configuration.
Chapter 09 closes on choosing between the exams and preparing for a program still in rollout.

A recurring audit pattern runs through the volume: **documentation versus reality.** Forgotten DNS
records, shadow API endpoints, unowned service tokens, and hand-drifted WAF rules are the same
failure at four layers, and the countermeasure is always an owner, a scope, and a schedule.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Cloudflare Certification Program](chapters/01-the-cloudflare-certification-program.md) | 1.1–1.2 |
| 02 | [The Edge Network, DNS, and Caching](chapters/02-the-edge-network-dns-and-caching.md) | 2.1–2.3 |
| 03 | [WAF, Rules, and Rate Limiting](chapters/03-waf-rules-and-rate-limiting.md) | 3.1–3.3 |
| 04 | [DDoS Protection, Bot Management, and API Shield](chapters/04-ddos-bots-and-api-shield.md) | 4.1–4.3 |
| 05 | [Zero Trust Access](chapters/05-zero-trust-access.md) | 5.1–5.3 |
| 06 | [Gateway, WARP, and Tunnel](chapters/06-gateway-warp-and-tunnel.md) | 6.1–6.3 |
| 07 | [Workers and the Developer Platform](chapters/07-workers-and-the-developer-platform.md) | 7.1–7.3 |
| 08 | [Operating Cloudflare — API, Terraform, and Logs](chapters/08-operating-cloudflare-api-terraform-and-logs.md) | 8.1–8.3 |
| 09 | [Choosing a Certification, Currency, and Career](chapters/09-choosing-a-certification-currency-career.md) | 9.1–9.2 |

## The credential catalog

| Credential | Type | Status at verification |
| --- | --- | --- |
| **Application Security Associate** | Certification (proctored exam) | Live portal page; "Register Interest" |
| **Zero Trust Associate** | Certification (proctored exam) | Named on the Connect 2026 University page |
| Accredited Sales Professional / Sales Engineer / Configuration Engineer / Services Architect | Partner accreditations (course tracks) | Active |
| Accredited Workers Developer | Partner accreditation | Announced as in development |

No Professional or Expert certification tier exists.

## What you will be able to do

- Read the program accurately: two Associate exams, a separate accreditation track, and which facts are published.
- Audit DNS for origin exposure, and size origins for cache-miss scenarios rather than steady state.
- Roll out WAF and bot enforcement on the log → challenge → block ladder with measured precision.
- Protect APIs with discovery-first schema validation, and find shadow endpoints from traffic.
- Bound blast radius with per-application Access policies, posture signals, and scoped service tokens.
- Close inbound ports with Tunnel, filter egress with Gateway, and govern TLS-inspection exceptions.
- Place compute next to its data, and choose edge storage per datum's consistency needs.
- Manage the whole estate as code with scheduled drift detection and monitored log pipelines.

## Prerequisites

- Working familiarity with DNS, HTTP, TLS, and general network security concepts.
- A Linux or macOS host with `python3`. A **free Cloudflare account plus a spare domain** turns
  Chapter 09's practice syllabus into the real thing at zero cost.

## See also

- [Volume XXXV — Zscaler Zero Trust Exchange](../volume-035-zscaler-zero-trust-exchange/README.md) and [Volume CXXVII — Netskope](../volume-127-netskope-certifications/README.md) — the rival SSE stacks.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the east-west half of zero trust; this volume's Access/Tunnel is the north-south half.
- [Volume CXL — Dynatrace](../volume-140-dynatrace-certifications/README.md) and [Volume CXLI — New Relic](../volume-141-newrelic-certifications/README.md) — the Batch F disclosure arc this volume completes.
- [Volume XLV — Splunk](../volume-045-splunk-certifications/README.md), [Volume LXXXVI — Elastic](../volume-086-elastic-certifications/README.md) — where Chapter 08's Logpush evidence should land.
