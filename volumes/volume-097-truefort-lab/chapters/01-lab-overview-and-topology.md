# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and the two tracks it is written on (a real TrueFort Platform deployment, or the native equivalent).
- Read the topology, address plan, and resource budget for the five-VM estate.
- Explain how TrueFort's application-centric, EDR-leveraged model differs from a per-host firewall agent.
- Explain why the OT segment deliberately has no host adapter.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself microsegmentation lab. You will construct a five–virtual-machine enterprise in miniature on a single Windows 11 host, deliberately break it to prove that a flat network lets an attacker move sideways, and then apply **TrueFort** to contain that movement.

TrueFort is an application-centric segmentation and workload-protection platform, with three traits that shape this lab:

- It is **EDR-leveraged**. TrueFort can ingest telemetry from an **endpoint detection and response** agent you already run — **CrowdStrike Falcon, SentinelOne, Microsoft Defender for Endpoint** — so that where EDR exists you add no new agent; it also offers its own lightweight agent. Either way the telemetry it reasons over is **process, network, and identity** behavior, not just packets.
- It is **application-centric**. It groups workloads by the application they serve and **baselines each application's normal behavior** — which processes talk to which, over which ports, run by which accounts.
- It watches **service accounts**. TrueFort's signature is detecting and stopping **service-account misuse** — a stolen service credential used from a host or process that has never legitimately used it — which is one of the most common lateral-movement techniques and one an address-and-port ACL cannot see.

The estate you build is intentionally heterogeneous — Linux servers, a Windows server, and an unpatchable "programmable logic controller" — because that mix is the reason segmentation platforms exist.

### An honest scope note — please read this before you start

TrueFort is commercial software. Two consequences shape this lab:

1. **There is no single-laptop community edition.** The platform is a console that ingests EDR (or its own agent's) telemetry and distributes policy; it is licensed. Nothing on the public internet substitutes for it.
2. **The behavioral and identity analytics are the product.** The enforcement it produces — allow/deny on the host firewall — you can reproduce natively, but the application baselining, the service-account analytics, and the real EDR integration are TrueFort's value.

Therefore every exercise in Chapters 06–08 is written on **two tracks**:

- **Track 1 — Real TrueFort.** The console workflow — connecting EDR telemetry or the TrueFort agent, reviewing the application behavior baseline, authoring policy, and watching service-account analytics — for readers with a deployment. Deployment-specific values appear as placeholders such as `<truefort-console-fqdn>`.
- **Track 2 — Native equivalent.** A faithful reproduction with no console. You enforce with the same native firewall (`nftables`/Windows Filtering Platform), and you reconstruct the behavioral and service-account signals TrueFort reasons over from native tooling: process-to-socket attribution (`ss -tnp`), audit records (`auditd`), and authentication logs.

Track 2 is not a mock-up. The application baseline is, at bottom, "which process, run by which user, connected where" — data you can gather from the OS. Building it yourself makes the platform's analytics concrete rather than magical.

Exercises that genuinely cannot be reproduced without the product — the real EDR integration, cross-fleet behavioral learning, and the identity analytics at scale — are marked **Design Exercise** with a model answer.

### Conventions

| Convention | Meaning |
|:---|:---|
| `PS C:\>` | Run on the **Windows 11 host**, in an **elevated** PowerShell |
| `PS C:\Users\Administrator>` | Run inside the **tf-win01** guest VM, elevated |
| `user@tf-gw:~$` | Run inside the named Linux guest as a normal user |
| `#` prefix in a Linux block | Command requires `sudo` / root |
| `<angle brackets>` | A value you must substitute from your own environment |
| **Design Exercise** | No deployment required and none simulated; written analysis with model answer |
| **Track 1** / **Track 2** | Real TrueFort path / native-equivalent path |

Every exercise follows the same five-part shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Rollback**. Do not skip the negative tests — proving a thing is *blocked* is the entire product.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation and Workstation install | 45–90 min |
| B | Virtual network construction | 20 min |
| C | Building the five VMs | 3–4 hours (mostly unattended installs) |
| D | Baseline application and the flat-network attack | 45 min |
| E | Telemetry, application baseline, and policy | 3–4 hours |
| F | Service-account misuse and the agentless OT device | 90 min |
| G | Operations, troubleshooting, teardown | 45 min |

Budget two comfortable days, or four evenings. Part C is the long pole and is largely waiting.

## Lab Overview

### Learning objectives

By the end of this lab you will be able to:

1. Explain how TrueFort reasons over process, network, and identity telemetry — from EDR or its own agent — and how enforcement lands on the native host firewall.
2. Build an **application behavior baseline** and use it to author least-privilege policy.
3. Ring-fence a two-tier application and validate it before enforcing.
4. Detect and block **service-account misuse** — a legitimate credential used from an illegitimate place.
5. Protect a device that can host no agent by enforcing on its managed neighbor.
6. Diagnose common failure modes and execute a break-glass rollback.

### Topology

Three isolated Layer 2 segments, joined by a single multi-homed Linux router that also becomes the enforcement point for the OT cell.

![Lab topology: the Windows 11 host, three VMware virtual networks (VMnet8 NAT "IT/Corporate", VMnet2 host-only "Data Center", VMnet3 host-only "OT Cell"), the five virtual machines, and the legitimate versus lateral-movement flows. tf-gw is the sole path between segments and the enforcement point protecting the agentless PLC.](../../../diagrams/volume-097-truefort-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The five-VM IT/OT estate this lab builds: TrueFort reasons over process and identity telemetry on the router and the Data Center servers and enforces on their native firewalls, the agentless PLC is protected by policy on its managed neighbor (tf-gw), the two legitimate east-west flows are allowed, and the compromised-HMI-to-database lateral movement — including stolen-service-account use — is denied.*

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
                  |  tf-gw     | .10            |
                  |  Ubuntu    |                |
                  |  22.04     |                |
                  | telemetry+ |                |
                  |  router +  | .254           |
                  | ENFORCEMENT+----------------+=======================
                  |   POINT    |   VMnet2  Host-only - "Data Center"
                  |  for OT     |   10.10.20.0/24     (no DHCP)
                  |            |        |         |          |
                  |            |   +----+---+ +---+----+ +---+-----+
                  |            |   |tf-app01| |tf-db01 | |tf-win01 |
                  |            |   |  .11   | |  .12   | |  .21    |
                  |            |   | nginx  | |postgres| | Win2022 |
                  |            |   |  :80   | | :5432  | |SCADA/HMI|
                  |            |   |appbase | |svc-acct| | telem   |
                  |            |   +--------+ +--------+ +---------+
                  |            | .254
                  +-----+------+
  ================================================
   VMnet3  Host-only - "OT Cell"  10.10.30.0/24
   NO host adapter. NO DHCP. Fully isolated.
   Reachable ONLY through tf-gw = the enforcement point.
                        |
                  +-----+------+
                  |  tf-ot01   | .50
                  |  "PLC"     |
                  |  Modbus    |
                  |  TCP :502  |
                  |  AGENTLESS |
                  +------------+
```

The design choices are deliberate:

- **VMnet3 has no host virtual adapter.** The only path to the PLC is through `tf-gw`, which lets a managed neighbor enforce for a device that can host no agent.
- **VMnet2 has a host virtual adapter (10.10.20.1).** This out-of-band management path survives every policy; Lab 9.2 uses it as break-glass.
- `tf-gw` **is the default gateway for the Data Center segment.** All east-west and cross-segment traffic traverses it.

### Address plan

| Host | Role | VMnet8 — IT/NAT | VMnet2 — Data Center | VMnet3 — OT Cell |
|:---|:---|:---|:---|:---|
| Windows 11 host | Admin console; "IT laptop" | 192.168.170.1 | 10.10.20.1 | *(none — by design)* |
| VMware NAT service | NAT gateway | 192.168.170.2 | — | — |
| **tf-gw** | Router; OT enforcement point | 192.168.170.10 | 10.10.20.254 | 10.10.30.254 |
| **tf-app01** | Web/app tier, nginx :80 | — | 10.10.20.11 | — |
| **tf-db01** | PostgreSQL :5432 | — | 10.10.20.12 | — |
| **tf-win01** | Windows workload; SCADA/HMI | — | 10.10.20.21 | — |
| **tf-ot01** | "PLC", Modbus TCP :502, agentless | — | — | 10.10.30.50 |

DNS for all guests: `192.168.170.2`.

### Resource budget

| VM       | Guest OS                   | vCPU  | RAM         | Disk        | Runs during |
|:---------|:---------------------------|:------|:------------|:------------|:------------|
| tf-gw    | Ubuntu Server 22.04.5 LTS  | 1     | 1024 MB     | 20 GB       | All parts   |
| tf-app01 | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| tf-db01  | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| tf-win01 | Windows Server 2022 (Eval) | 2     | 4096 MB     | 60 GB       | E, F, G     |
| tf-ot01  | Ubuntu Server 22.04.5 LTS  | 1     | 768 MB      | 10 GB       | D, F, G     |
|          | **Peak concurrent**        | **6** | **~8.9 GB** | **~130 GB** |             |

**Host minimum:** 4 cores, 16 GB RAM, 250 GB free SSD. **Comfortable:** 8 cores, 32 GB RAM, 400 GB free NVMe.

### Bill of materials

| Item | Where | Size | Notes |
|:---|:---|:---|:---|
| VMware Workstation Pro 17.6.3 for Windows | Broadcom Support Portal | ~600 MB | **Free**, no license key. |
| Ubuntu Server 22.04.5 LTS ISO | `releases.ubuntu.com/jammy/` | ~2.0 GB | `ubuntu-22.04.5-live-server-amd64.iso` |
| Windows Server 2022 Evaluation ISO | Microsoft Evaluation Center | ~5.0 GB | 180-day evaluation |
| TrueFort Platform access | TrueFort (evaluation or partner) | — | **Track 1 only.** Track 2 needs none of this. |

Both Workstation 17.6.3 and 26H1 (14 May 2026) work identically here; both are free and need no license key since 11 November 2024.

## Summary and Completion Checklist

- [ ] Topology, address plan, and resource budget understood.
- [ ] The application-centric, EDR-leveraged model — and its focus on service accounts — understood.
- [ ] Bill of materials downloaded.
- [ ] Track chosen: real TrueFort Platform (Track 1) or native equivalent (Track 2).
