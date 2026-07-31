# Volume C — Cisco Secure Workload Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab on a single Windows 11 host: five virtual machines
> across three isolated VMware segments — a three-legged Linux router, an nginx application tier, a
> PostgreSQL database, a Windows SCADA/HMI station, and an agentless "PLC" speaking Modbus TCP 502 —
> built, deliberately broken to reproduce lateral movement across a flat network, then contained
> with **Cisco Secure Workload** (formerly Tetration): comprehensive **flow telemetry**, **Application
> Dependency Mapping (ADM)** that discovers the app's tiers and dependencies and **auto-generates** a
> least-privilege policy, hierarchical **scopes**, **policy analysis** that replays real traffic
> against a candidate policy before it ever blocks, and enforcement on the native host firewall.
> **30 walkthrough labs** across nine chapters, each on two tracks — a real Secure Workload cluster
> and agents, or the native equivalent: telemetry from `conntrack`, ADM by clustering it into tiers,
> auto-generated policy, a native "what-if" analysis, and enforcement with `iptables`/`ipset` and the
> Windows Filtering Platform.

## Overview

Volume C is a **hands-on lab volume**. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 04](../volume-087-microsegmentation-options/chapters/04-workload-agent-based-platforms.md)
summarizes host-agent platforms including Cisco Secure Workload, this volume is the **build**: 30
walkthrough labs that construct the estate, break it, and segment it.

Secure Workload's distinguishing workflow shapes the product chapters: you do not hand-write policy,
you **discover** it. Comprehensive telemetry feeds **Application Dependency Mapping**, which clusters
workloads into tiers and **generates** the least-privilege policy; you then **analyze** that policy
against real flows — a "what-if" that shows exactly what it will allow and deny — before enforcing it
on the host firewall. The native track makes each step concrete: flows from `conntrack`, ADM by hand,
a native policy-analysis script, and enforcement with `ipset`.

### An honest scope note

Cisco Secure Workload is **commercial software**; the control plane is a licensed on-premises cluster
or SaaS tenant, and the agents are licensed. Every exercise in Chapters 06–08 is therefore written on
**two tracks**:

- **Track 1 — Real Secure Workload.** The cluster workflow — agents, telemetry, ADM, scopes,
  workspaces, policy analysis, and enforcement — for readers with a deployment.
- **Track 2 — Native equivalent.** Telemetry from `conntrack`, ADM by clustering it into tiers,
  auto-generated policy, a native "what-if" analysis, and enforcement with `iptables`/`ipset` and WFP.

Exercises that genuinely cannot be reproduced without the product — cluster-scale ADM, process
forensics, and vulnerability correlation — are marked **Design Exercise** with a model answer.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.4 |
| 03 | [Building the Virtual Networks](chapters/03-virtual-networks.md) | 3.1–3.4 |
| 04 | [Building the Virtual Machines](chapters/04-building-the-virtual-machines.md) | 4.1–4.6 |
| 05 | [The Flat Network and Lateral Movement](chapters/05-flat-network-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [Telemetry, ADM, and Auto-Generated Policy](chapters/06-telemetry-adm-and-auto-policy.md) | 6.1–6.3 |
| 07 | [Policy Analysis and Enforcement](chapters/07-policy-analysis-and-enforcement.md) | 7.1–7.4 |
| 08 | [Protecting the Agentless PLC](chapters/08-protecting-the-agentless-plc.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Describe the cluster-and-agent architecture and what the agent programs on Linux (`iptables`/`ipset`) and Windows (WFP).
- Collect comprehensive telemetry and perform Application Dependency Mapping to discover tiers and dependencies.
- Auto-generate a least-privilege policy and analyze it against real flows before enforcing.
- Enforce with `ipset`-backed rules and protect an agentless device from its managed neighbor.
- Troubleshoot telemetry, discovery, and ipset-membership issues, and roll back under pressure.

## Prerequisites

- A Windows 11 host: 4+ cores, 16 GB RAM (32 GB comfortable), 250 GB free SSD.
- VMware Workstation Pro 17.6.3 or 26H1 (free), Ubuntu Server 22.04.5 LTS, Windows Server 2022 Evaluation.
- Optional for Track 1: access to a Cisco Secure Workload cluster or SaaS tenant and agents.

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume XXV — Cisco Security](../volume-025-cisco-security/README.md) for the broader Cisco security context.
- [Volume XCIII — ColorTokens](../volume-093-colortokens-xshield-lab/README.md) through [Volume XCIX — Tempered Airwall](../volume-099-tempered-airwall-lab/README.md) — the same estate contained with other platforms.
