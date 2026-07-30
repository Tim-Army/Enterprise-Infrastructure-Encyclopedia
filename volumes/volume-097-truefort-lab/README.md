# Volume XCVII — TrueFort Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab on a single Windows 11 host: five virtual machines
> across three isolated VMware segments — a three-legged Linux router, an nginx application tier, a
> PostgreSQL database, a Windows SCADA/HMI station, and an agentless "PLC" speaking Modbus TCP 502 —
> built, deliberately broken to reproduce lateral movement (including reuse of a **stolen service
> account**) across a flat network, then contained with **TrueFort**: the **EDR-leveraged** model
> (reuse existing CrowdStrike/SentinelOne/Defender telemetry instead of adding an agent), an
> **application behavior baseline** built from process, network, and identity data, least-privilege
> policy enforced on the native firewall, and the signature control — **service-account binding**, so
> a valid credential works only from its sanctioned host *and process identity*. **31 walkthrough
> labs** across nine chapters, each on two tracks — a real TrueFort Platform deployment, or the
> native `nftables`/Windows Filtering Platform enforcement plus the behavioral and identity signals
> reconstructed from `ss -tnp`, `auditd`, PostgreSQL `log_connections`, and an `nftables` `skuid`
> owner match.

## Overview

Volume XCVII is a **hands-on lab volume**. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 06](../volume-087-microsegmentation-options/chapters/06-truefort.md)
summarizes TrueFort, this volume is the **build**: 31 walkthrough labs that construct the estate,
break it, and segment it.

TrueFort's distinguishing traits shape the product chapters. It is **application-centric** and
**EDR-leveraged** — reasoning over process, network, and identity telemetry from an EDR you already
run — and its signature is following **identity**: it binds a service account to the process and host
that legitimately use it, so a stolen credential presented from anywhere else is denied and alerted.
The native track makes that concrete with an `nftables` socket-owner match, the OS-level analogue of
"only the sanctioned process may use this path."

### An honest scope note

TrueFort is **commercial software**. There is no single-laptop community edition; the platform
ingests EDR (or its own agent's) telemetry and distributes policy. Every exercise in Chapters 06–08
is therefore written on **two tracks**:

- **Track 1 — Real TrueFort.** The console workflow — connecting telemetry, reviewing the application
  baseline, authoring policy, and watching service-account analytics — for readers with a deployment.
- **Track 2 — Native equivalent.** The same native firewall enforcement, plus the behavioral and
  identity signals reconstructed from `ss -tnp`, `auditd`, PostgreSQL logs, and a `skuid` owner match.

Exercises that genuinely cannot be reproduced without the product — the real EDR integration and
cross-fleet behavioral learning — are marked **Design Exercise** with a model answer.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.4 |
| 03 | [Building the Virtual Networks](chapters/03-virtual-networks.md) | 3.1–3.4 |
| 04 | [Building the Virtual Machines](chapters/04-building-the-virtual-machines.md) | 4.1–4.6 |
| 05 | [The Flat Network and Lateral Movement](chapters/05-flat-network-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [Telemetry, the Application Baseline, and Policy](chapters/06-telemetry-baseline-and-policy.md) | 6.1–6.4 |
| 07 | [Enforcement and Service-Account Binding](chapters/07-enforcement-and-service-accounts.md) | 7.1–7.4 |
| 08 | [Protecting the Agentless PLC](chapters/08-protecting-the-agentless-plc.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Explain how TrueFort reasons over process/network/identity telemetry and enforces on the native firewall.
- Build an application behavior baseline and author least-privilege policy from it.
- Bind a service account to its sanctioned host and process identity, defeating stolen-credential reuse.
- Protect an agentless device from its managed neighbor and the router path.
- Troubleshoot telemetry gaps, identity blocks, and unexpected denies — and roll back under pressure.

## Prerequisites

- A Windows 11 host: 4+ cores, 16 GB RAM (32 GB comfortable), 250 GB free SSD.
- VMware Workstation Pro 17.6.3 or 26H1 (free), Ubuntu Server 22.04.5 LTS, Windows Server 2022 Evaluation.
- Optional for Track 1: access to a TrueFort Platform deployment (and, ideally, an EDR to integrate).

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume XCIII — ColorTokens Xshield](../volume-093-colortokens-xshield-lab/README.md), [Volume XCIV — Illumio](../volume-094-illumio-lab/README.md), [Volume XCV — Akamai Guardicore](../volume-095-akamai-guardicore-lab/README.md), and [Volume XCVI — Zero Networks](../volume-096-zero-networks-lab/README.md) — the same estate contained with other platforms.
