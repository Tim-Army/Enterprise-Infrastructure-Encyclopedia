# Volume XCVI — Zero Networks Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab on a single Windows 11 host: five virtual machines
> across three isolated VMware segments — a three-legged Linux router, an nginx application tier, a
> PostgreSQL database, a Windows SCADA/HMI station, and an agentless "PLC" speaking Modbus TCP 502 —
> built, deliberately broken to reproduce lateral movement across a flat network, then contained
> with **Zero Networks Segment**: the **agentless** model (the platform remotely programs each
> host's *own* firewall — no agent installed), the **learn → least-privilege → enforce** lifecycle
> (monitor traffic, auto-derive allow rules, then default-deny), and the signature control —
> **just-in-time MFA for privileged ports**, so RDP/SSH/WinRM/SMB are closed by default and opened
> per-source, per-session only after an authenticated, time-boxed grant. **31 walkthrough labs**
> across nine chapters, each on two tracks — a real Zero Networks deployment, or the native
> `nftables`/Windows Filtering Platform rules the platform itself writes, including a `timeout`-based
> just-in-time SSH grant that auto-revokes.

## Overview

Volume XCVI is a **hands-on lab volume**. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 05](../volume-087-microsegmentation-options/chapters/05-zero-networks.md)
summarizes Zero Networks, this volume is the **build**: 31 walkthrough labs that construct the
estate, break it, and segment it.

Zero Networks' distinguishing traits shape the product chapters and make the native track unusually
faithful. Because the platform is **agentless** — it enforces by remotely programming the native
host firewall rather than installing anything — Track 2 programs the very same firewall by hand. What
Track 1 adds is the automation: the ~30-day traffic **learning** that derives least-privilege rules,
and the **just-in-time MFA** that keeps administrative ports closed until an authenticated grant opens
them. The difference between the tracks is the automation and identity, not the enforcement engine.

### An honest scope note

Zero Networks Segment is **commercial software**. There is no single-laptop community edition, and
the platform uses a privileged service account to reach each host's firewall management interface.
Every exercise in Chapters 06–08 is therefore written on **two tracks**:

- **Track 1 — Real Zero Networks.** The console workflow — monitoring, reviewing learned rules,
  enabling protection, and configuring MFA for privileged ports — for readers with a deployment.
- **Track 2 — Native equivalent.** The same `nftables`/Windows Filtering Platform rules the platform
  writes, plus a `timeout`-based just-in-time grant that reproduces a time-boxed MFA session.

Exercises that genuinely cannot be reproduced without the product — automatic rule learning at scale
and the real MFA identity flow — are marked **Design Exercise** with a model answer.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.4 |
| 03 | [Building the Virtual Networks](chapters/03-virtual-networks.md) | 3.1–3.4 |
| 04 | [Building the Virtual Machines](chapters/04-building-the-virtual-machines.md) | 4.1–4.6 |
| 05 | [The Flat Network and Lateral Movement](chapters/05-flat-network-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [The Agentless Model and the Learning Phase](chapters/06-agentless-model-and-learning.md) | 6.1–6.4 |
| 07 | [Enforcement and Just-in-Time MFA](chapters/07-enforcement-and-jit-mfa.md) | 7.1–7.4 |
| 08 | [Protecting the Agentless PLC](chapters/08-protecting-the-agentless-plc.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Explain how an agentless platform enforces by remotely programming the native host firewall.
- Reproduce the learn → least-privilege → enforce lifecycle and review learned rules before enforcing.
- Build just-in-time MFA for privileged ports so RDP/SSH are closed until a time-boxed grant opens them.
- Protect an un-manageable device from its managed neighbor and the router path.
- Troubleshoot management-reach, expired grants, and unexpected blocks — and roll back with the JIT caveat in mind.

## Prerequisites

- A Windows 11 host: 4+ cores, 16 GB RAM (32 GB comfortable), 250 GB free SSD.
- VMware Workstation Pro 17.6.3 or 26H1 (free), Ubuntu Server 22.04.5 LTS, Windows Server 2022 Evaluation.
- Optional for Track 1: access to a Zero Networks Segment deployment.

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume XCIII — ColorTokens Xshield](../volume-093-colortokens-xshield-lab/README.md), [Volume XCIV — Illumio](../volume-094-illumio-lab/README.md), and [Volume XCV — Akamai Guardicore](../volume-095-akamai-guardicore-lab/README.md) — the same estate contained with other platforms.
