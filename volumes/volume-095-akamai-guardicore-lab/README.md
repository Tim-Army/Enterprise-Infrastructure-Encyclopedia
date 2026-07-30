# Volume XCV — Akamai Guardicore Segmentation Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab on a single Windows 11 host: five virtual machines
> across three isolated VMware segments — a three-legged Linux router, an nginx application tier, a
> PostgreSQL database, a Windows SCADA/HMI station, and an agentless "PLC" speaking Modbus TCP 502 —
> built, deliberately broken to reproduce lateral movement across a flat network, then contained
> with **Akamai Guardicore Segmentation**: the **Centra** architecture (Management, Aggregators,
> Collectors), agents that report flows with **process and user context**, the **Reveal** map,
> flexible **key/value labels**, ordered **allow / block / alert** policy validated in an
> **alert-only** posture before enforcement, process-scoped rules, and Guardicore's
> detection/deception fit for a single-flow OT segment. **32 walkthrough labs** across nine
> chapters, each on two tracks — a real Guardicore Centra environment and agent, or the native
> `nftables`/Windows Filtering Platform primitives the agent programs, with process attribution
> reconstructed from `conntrack` and `ss -tnp`.

## Overview

Volume XCV is a **hands-on lab volume**. Where
[Volume LXXXVII (Microsegmentation Options)](../volume-087-microsegmentation-options/README.md)
compares vendors and
[its Chapter 04](../volume-087-microsegmentation-options/chapters/04-workload-agent-based-platforms.md)
summarizes host-agent platforms including Akamai Guardicore, this volume is the **build**: 32
walkthrough labs that construct the estate, break it, and segment it.

The estate is deliberately heterogeneous — Linux servers, a Windows server, and an unpatchable PLC —
because that mix is the reason a platform like Guardicore exists. Guardicore's distinguishing traits
shape the product chapters: flow telemetry that carries **process and user context** (so a rule can
name the software, not just the host), and an **alert-then-enforce** lifecycle that lets you validate
every rule by watching what it *would* do first.

### An honest scope note

Akamai Guardicore Segmentation is **commercial software**. There is no single-laptop community
edition of the Centra control plane, and the agent is registered against a management server you have
been granted. Every exercise in Chapters 06–08 is therefore written on **two tracks**:

- **Track 1 — Real Guardicore.** The actual Centra console navigation (Reveal, labels, policy), agent
  registration, and verification points, for readers with access to a Centra environment.
  Environment-specific values appear as placeholders such as `<centra-mgmt-fqdn>`.
- **Track 2 — Native equivalent.** A faithful path that runs today with no Centra, driving the *same
  enforcement primitives the agent drives* — `nftables`/`iptables` and the Windows Filtering
  Platform — and reconstructing the process-aware flow view from `conntrack` and `ss -tnp`.

Exercises that genuinely cannot be reproduced without the product — Reveal's process attribution,
osquery-based Insight, and threat detection/deception — are marked **Design Exercise** with a model
answer.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Host Preparation](chapters/02-host-preparation.md) | 2.1–2.4 |
| 03 | [Building the Virtual Networks](chapters/03-virtual-networks.md) | 3.1–3.4 |
| 04 | [Building the Virtual Machines](chapters/04-building-the-virtual-machines.md) | 4.1–4.6 |
| 05 | [The Flat Network and Lateral Movement](chapters/05-flat-network-and-lateral-movement.md) | 5.1–5.3 |
| 06 | [Reveal, Agents, and Labels](chapters/06-reveal-agents-and-labels.md) | 6.1–6.4 |
| 07 | [Policy — Allow, Block, Alert, then Enforce](chapters/07-policy-alert-then-enforce.md) | 7.1–7.4 |
| 08 | [The Agentless PLC and Guardicore Detection](chapters/08-agentless-ot-and-detection.md) | 8.1–8.4 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Describe the Centra architecture and what the agent programs on Linux and Windows.
- Read the Reveal map with process and user context, and use it before writing a rule.
- Apply key/value labels and write ordered allow/block/alert policy validated in alert-only first.
- Reason about process-scoped rules that narrow trust to the software that earned it.
- Protect an agentless device via managed-neighbor and path enforcement, with a high-fidelity OT tripwire.
- Troubleshoot a stuck agent, an unpublished policy, and an unexpected block — and roll back under pressure.

## Prerequisites

- A Windows 11 host: 4+ cores, 16 GB RAM (32 GB comfortable), 250 GB free SSD.
- VMware Workstation Pro 17.6.3 or 26H1 (free), Ubuntu Server 22.04.5 LTS, Windows Server 2022 Evaluation.
- Optional for Track 1: access to an Akamai Guardicore Centra environment and agent.

## See also

- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
- [Volume XCIII — ColorTokens Xshield](../volume-093-colortokens-xshield-lab/README.md) and [Volume XCIV — Illumio](../volume-094-illumio-lab/README.md) — the same estate contained with other host-agent platforms.
