# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and the two tracks it is written on (a real Cisco Secure Workload deployment, or the native equivalent).
- Read the topology, address plan, and resource budget for the five-VM estate.
- Explain how Secure Workload's telemetry-driven, auto-discovered policy differs from hand-written rules.
- Explain why the OT segment deliberately has no host adapter.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself microsegmentation lab. You will construct a five–virtual-machine enterprise in miniature on a single Windows 11 host, deliberately break it to prove that a flat network lets an attacker move sideways, and then apply **Cisco Secure Workload** (formerly Tetration) to contain that movement.

Secure Workload is a host-agent platform with a distinctive workflow: it collects **comprehensive flow and process telemetry** from agents on every workload, uses it to **automatically discover the application's dependencies** — a step called **Application Dependency Mapping (ADM)** — and from that discovery **generates least-privilege policy** you review, analyze against real traffic, and then enforce. Three ideas shape this lab:

- **Telemetry first.** Agents report every flow and the process behind it. You do not guess the policy; you discover it from what the application actually does.
- **ADM and auto-generated policy.** Secure Workload clusters workloads into tiers from their flow patterns and proposes a least-privilege policy per cluster — the automation that makes segmentation tractable at scale.
- **Scopes and policy analysis.** Workloads live in a hierarchical **scope** tree, and a candidate policy can be **analyzed against historical flows** — a "what-if" that shows exactly what it would allow and deny — *before* it is enforced on the host firewall.

The estate you build is intentionally heterogeneous — Linux servers, a Windows server, and an unpatchable "programmable logic controller" — because that mix is the reason segmentation platforms exist.

### An honest scope note — please read this before you start

Cisco Secure Workload is commercial software. Two consequences shape this lab:

1. **There is no single-laptop community edition.** The control plane is a licensed on-premises cluster or SaaS tenant, and the enforcement agents are licensed. Nothing on the public internet is a free Secure Workload.
2. **The analytics are the product; the enforcement is the OS firewall.** Secure Workload's agents enforce by programming the **native host firewall** — `iptables` with `ipset` on Linux, the **Windows Filtering Platform** on Windows — which you can reproduce natively. The comprehensive telemetry, the ADM clustering, and the policy analysis are what you are buying.

Therefore every exercise in Chapters 06–08 is written on **two tracks**:

- **Track 1 — Real Secure Workload.** The cluster workflow — installing agents, collecting telemetry, running ADM, reviewing scopes and workspaces, analyzing policy, and enforcing — for readers with a deployment. Deployment-specific values appear as placeholders such as `<cluster-fqdn>`.
- **Track 2 — Native equivalent.** A faithful reproduction with no cluster. You collect comprehensive flow telemetry natively, perform ADM by clustering it into tiers, auto-generate a least-privilege policy, analyze it against the captured flows, and enforce it with `iptables`/`ipset` and the Windows Filtering Platform.

Track 2 is not a mock-up. ADM is, at bottom, "group workloads by who they talk to and generate rules from it" — something you can do from `conntrack` and flow logs. Doing it yourself makes the discovery concrete rather than magical.

Exercises that genuinely cannot be reproduced without the product — cluster-scale ADM, process forensics, and vulnerability correlation — are marked **Design Exercise** with a model answer.

### Conventions

| Convention | Meaning |
|:---|:---|
| `PS C:\>` | Run on the **Windows 11 host**, in an **elevated** PowerShell |
| `PS C:\Users\Administrator>` | Run inside the **cw-win01** guest VM, elevated |
| `user@cw-gw:~$` | Run inside the named Linux guest as a normal user |
| `#` prefix in a Linux block | Command requires `sudo` / root |
| `<angle brackets>` | A value you must substitute from your own environment |
| **Design Exercise** | No deployment required and none simulated; written analysis with model answer |
| **Track 1** / **Track 2** | Real Secure Workload path / native-equivalent path |

Every exercise follows the same five-part shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Cleanup**. Do not skip the negative tests — proving a thing is *blocked* is the entire product.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation and Workstation install | 45–90 min |
| B | Virtual network construction | 20 min |
| C | Building the five VMs | 3–4 hours (mostly unattended installs) |
| D | Baseline application and the flat-network attack | 45 min |
| E | Telemetry, ADM, and auto-generated policy | 3–4 hours |
| F | Policy analysis, enforcement, and the agentless OT device | 90 min |
| G | Operations, troubleshooting, teardown | 45 min |

Budget two comfortable days, or four evenings. Part C is the long pole and is largely waiting.

## Lab Overview

### Learning objectives

By the end of this lab you will be able to:

1. Explain the cluster-and-agent architecture and what the agent programs on Linux (`iptables`/`ipset`) and Windows (WFP).
2. Collect comprehensive flow telemetry and perform **Application Dependency Mapping** to discover tiers and dependencies.
3. Auto-generate a least-privilege policy from the discovery and organize workloads in a scope hierarchy.
4. **Analyze** a candidate policy against captured flows before enforcing it.
5. Enforce the policy on the host firewall and confirm the intended flows survive while the attack is blocked.
6. Protect a device that can run no agent by enforcing on its managed neighbor.
7. Diagnose common failure modes and execute a break-glass rollback.

### Topology

Three isolated Layer 2 segments, joined by a single multi-homed Linux router that also becomes the enforcement point for the OT cell.

![Lab topology: the Windows 11 host, three VMware virtual networks (VMnet8 NAT "IT/Corporate", VMnet2 host-only "Data Center", VMnet3 host-only "OT Cell"), the five virtual machines, and the legitimate versus lateral-movement flows. cw-gw is the sole path between segments and the enforcement point protecting the agentless PLC.](../../../diagrams/volume-100-cisco-secure-workload-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The five-VM IT/OT estate this lab builds: Secure Workload agents on the router and the Data Center servers collect telemetry and enforce on their host firewalls, the agentless PLC is protected by policy on its managed neighbor (cw-gw), the two legitimate east-west flows are allowed, and the compromised-HMI-to-database lateral movement is denied.*

A text-only rendering of the same topology follows for reference:

```text
                    +----------------------------------------------+
                    |   Windows 11 Education host                  |
                    |   VMware Workstation Pro 17.6.3              |
                    |   Roles: admin console + "IT laptop"         |
                    |          (the untrusted lateral-movement     |
                    |           source in Lab 5.3)                 |
                    +---+-----------------------+------------------+
                        | 192.168.170.1         | 10.10.20.1
                        | (host vNIC)           | (host vNIC)
  ======================+===============        |
   VMnet8  NAT - "IT / Corporate"               |
   192.168.170.0/24   NAT gw .2                 |
                        |                       |
                  +-----+------+                |
                  |  cw-gw     | .10            |
                  |  Ubuntu    |                |
                  |  22.04     |                |
                  | agent +    |                |
                  |  router +  | .254           |
                  | ENFORCEMENT+----------------+=======================
                  |   POINT    |   VMnet2  Host-only - "Data Center"
                  |  for OT     |   10.10.20.0/24     (no DHCP)
                  |            |        |         |          |
                  |            |   +----+---+ +---+----+ +---+-----+
                  |            |   |cw-app01| |cw-db01 | |cw-win01 |
                  |            |   |  .11   | |  .12   | |  .21    |
                  |            |   | nginx  | |postgres| | Win2022 |
                  |            |   |  :80   | | :5432  | |SCADA/HMI|
                  |            |   | agent  | | agent  | | agent   |
                  |            |   +--------+ +--------+ +---------+
                  |            | .254
                  +-----+------+
  ================================================
   VMnet3  Host-only - "OT Cell"  10.10.30.0/24
   NO host adapter. NO DHCP. Fully isolated.
   Reachable ONLY through cw-gw = the enforcement point.
                        |
                  +-----+------+
                  |  cw-ot01   | .50
                  |  "PLC"     |
                  |  Modbus    |
                  |  TCP :502  |
                  |  AGENTLESS |
                  +------------+
```

The design choices are deliberate:

- **VMnet3 has no host virtual adapter.** The only path to the PLC is through `cw-gw`, which lets a managed neighbor enforce for a device that can host no agent.
- **VMnet2 has a host virtual adapter (10.10.20.1).** This out-of-band management path survives every policy; Lab 9.2 uses it as break-glass.
- `cw-gw` **is the default gateway for the Data Center segment.** All east-west and cross-segment traffic traverses it, so the agent there sees transit flows for telemetry.

### Address plan

| Host | Role | VMnet8 — IT/NAT | VMnet2 — Data Center | VMnet3 — OT Cell |
|:---|:---|:---|:---|:---|
| Windows 11 host | Admin console; "IT laptop" | 192.168.170.1 | 10.10.20.1 | *(none — by design)* |
| VMware NAT service | NAT gateway | 192.168.170.2 | — | — |
| **cw-gw** | Router; agent; OT enforcement point | 192.168.170.10 | 10.10.20.254 | 10.10.30.254 |
| **cw-app01** | Web/app tier, nginx :80; agent | — | 10.10.20.11 | — |
| **cw-db01** | PostgreSQL :5432; agent | — | 10.10.20.12 | — |
| **cw-win01** | Windows workload; SCADA/HMI; agent | — | 10.10.20.21 | — |
| **cw-ot01** | "PLC", Modbus TCP :502, agentless | — | — | 10.10.30.50 |

DNS for all guests: `192.168.170.2`.

### Resource budget

| VM       | Guest OS                   | vCPU  | RAM         | Disk        | Runs during |
|:---------|:---------------------------|:------|:------------|:------------|:------------|
| cw-gw    | Ubuntu Server 22.04.5 LTS  | 1     | 1024 MB     | 20 GB       | All parts   |
| cw-app01 | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| cw-db01  | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| cw-win01 | Windows Server 2022 (Eval) | 2     | 4096 MB     | 60 GB       | E, F, G     |
| cw-ot01  | Ubuntu Server 22.04.5 LTS  | 1     | 768 MB      | 10 GB       | D, F, G     |
|          | **Peak concurrent**        | **6** | **~8.9 GB** | **~130 GB** |             |

**Host minimum:** 4 cores, 16 GB RAM, 250 GB free SSD. **Comfortable:** 8 cores, 32 GB RAM, 400 GB free NVMe. A real Secure Workload cluster is not run on this host; use a cluster/SaaS for Track 1, or run Track 2.

### Bill of materials

| Item | Where | Size | Notes |
|:---|:---|:---|:---|
| VMware Workstation Pro 17.6.3 for Windows | Broadcom Support Portal | ~600 MB | **Free**, no license key. |
| Ubuntu Server 22.04.5 LTS ISO | `releases.ubuntu.com/jammy/` | ~2.0 GB | `ubuntu-22.04.5-live-server-amd64.iso` |
| Windows Server 2022 Evaluation ISO | Microsoft Evaluation Center | ~5.0 GB | 180-day evaluation |
| Secure Workload cluster/SaaS + agents | Cisco | — | **Track 1 only.** Track 2 needs none of this. |

Both Workstation 17.6.3 and 26H1 (14 May 2026) work identically here; both are free and need no license key since 11 November 2024.

## Summary and Completion Checklist

- [ ] Topology, address plan, and resource budget understood.
- [ ] The telemetry → ADM → auto-policy → analyze → enforce workflow understood.
- [ ] Bill of materials downloaded.
- [ ] Track chosen: real Secure Workload (Track 1) or native equivalent (Track 2).
