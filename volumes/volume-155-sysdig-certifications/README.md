# Volume CLV — Sysdig Certification Tracks

> The Sysdig learning program — verified 5 August 2026 on `sysdig.com` and `enablement.sysdig.com`. Sysdig's program
> has **two strands**: its own **Credly digital badges** earned through the enablement portal — most notably the
> **Kraken Hunter** accreditation (a hands-on workshop of labs and presentations plus an exam, validating
> Sysdig-tooling skill for cloud and container security) and a **Partner Technical Accreditation** program — plus the
> open-source **Falco** training path, the Linux Foundation / CNCF course **LFS254 "Detecting Cloud Runtime Threats
> with Falco"** (~20 hours). This is a **badges-and-training** program stated plainly — hands-on and current, not a
> proctored vendor-exam gate. Every lab runs **free** in Python. **Defensive throughout** — detecting threats at
> runtime, prioritizing real vulnerabilities, and enforcing posture on cloud-native workloads.

## Overview

Sysdig is a leader in **cloud-native and container security**. Its platform, **Sysdig Secure**, is a **runtime-first
CNAPP** (Cloud-Native Application Protection Platform) that secures containers, Kubernetes, and cloud by watching what
is **actually running** — and Sysdig also *created* **Falco**, the open-source runtime security engine now stewarded by
the [CNCF (XLI)](../volume-041-cncf-kubernetes-certifications/README.md). Where the
[Wiz volume (CXLVII)](../volume-147-wiz-certifications/README.md) leads with *agentless posture* (what *could* be
wrong), **Sysdig leads with *runtime* — what *is* happening right now** on your workloads, via deep **eBPF**
instrumentation.

Chapter 02 covers **runtime-first cloud security** — why runtime is the differentiator. Chapter 03 covers **Falco**,
the open-source detection engine. Chapter 04 covers **eBPF and deep visibility** — how runtime data is captured.
Chapter 05 covers **cloud detection and response** — Falco-powered five-second detection and drift. Chapter 06 covers
**vulnerability management** prioritized by in-use runtime context. Chapter 07 covers **posture, permissions, and
compliance** — CSPM, CIEM, and benchmarks. Chapter 08 covers **the unified CNAPP and Sysdig Monitor** — one platform
on shared runtime data. Chapter 09 closes on choosing a path.

A theme runs through it: **runtime is the connective tissue** — one deep observation of what is actually running
sharpens detection, vulnerability prioritization, posture, and entitlements alike, and the same data powers
observability.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Sysdig Program](chapters/01-the-sysdig-program.md) | 1.1–1.2 |
| 02 | [Runtime-First Cloud Security](chapters/02-runtime-first-cloud-security.md) | 2.1 |
| 03 | [Falco — Open-Source Runtime Security](chapters/03-falco-open-source-runtime-security.md) | 3.1 |
| 04 | [eBPF and Deep Visibility](chapters/04-ebpf-and-deep-visibility.md) | 4.1 |
| 05 | [Cloud Detection and Response](chapters/05-cloud-detection-and-response.md) | 5.1 |
| 06 | [Vulnerability Management — Runtime Prioritization](chapters/06-vulnerability-management-runtime-prioritization.md) | 6.1 |
| 07 | [Posture, Permissions, and Compliance](chapters/07-posture-permissions-and-compliance.md) | 7.1 |
| 08 | [The Unified CNAPP and Sysdig Monitor](chapters/08-the-unified-cnapp-and-monitor.md) | 8.1 |
| 09 | [Choosing Your Sysdig/Falco Path](chapters/09-choosing-your-sysdig-path.md) | 9.1–9.2 |

## The program

| Strand | Is |
| --- | --- |
| **Kraken Hunter** (Credly) | Sysdig-tooling accreditation — workshop (hands-on labs) + exam |
| **Partner Technical Accreditation** | Partner-team badges per level |
| **Falco LFS254** (CNCF / Linux Foundation) | Open-source runtime-security course (~20 hours) |

Two strands reflecting Sysdig's dual identity: a **commercial platform** (Sysdig Secure) *and* the **steward of
open-source Falco**. A **badges-and-training** model, not a proctored exam gate.

## What you will be able to do

- Read the two-strand program and sequence a path — free open-source Falco (LFS254) then the Kraken Hunter accreditation.
- Explain runtime-first security — securing what is *actually running*, complementing agentless posture.
- Describe Falco as the open-source (CNCF) runtime detection engine and its detection-as-code rules.
- Explain eBPF as safe in-kernel instrumentation of system calls — the ground-truth data foundation.
- Apply cloud detection and response — five-second detection, drift detection, and forensics.
- Prioritize vulnerabilities by in-use runtime context rather than raw CVE counts.
- Apply CSPM, CIEM (right-sized from observed usage), and continuous compliance in the unified CNAPP.
- Recognize runtime as the connective tissue tying detection, vulnerabilities, posture, and entitlements together.

## Prerequisites

- Familiarity with containers, Kubernetes, and cloud fundamentals helps.
- A Linux or macOS host with `python3`. **Falco is free and open-source**; the Sysdig accreditations are badge-based.

## See also

- [Volume XLI — CNCF / Kubernetes](../volume-041-cncf-kubernetes-certifications/README.md) — the platform Sysdig secures; Falco is itself a CNCF project.
- [Volume CXLVII — Wiz](../volume-147-wiz-certifications/README.md) — agentless posture CNAPP; Sysdig's runtime-first complements it.
- [Volume CXLVIII — Snyk](../volume-148-snyk-certifications/README.md) — shift-left / AppSec, the prevention half of the lifecycle.
- [Volume CLI — SentinelOne](../volume-151-sentinelone-certifications/README.md) — runtime detection and response, the endpoint parallel.
- [Volume XLV — Splunk](../volume-045-splunk-certifications/README.md) — detection engineering and the SOC that consumes runtime alerts.
