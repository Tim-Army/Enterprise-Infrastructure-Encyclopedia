# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and the two tracks it is written on (a real Akamai Guardicore Centra deployment and agent, or the native enforcement equivalent).
- Read the topology, address plan, and resource budget for the five-VM estate.
- Assemble the bill of materials before starting.
- Explain why the OT segment deliberately has no host adapter, and how Guardicore treats a device that can run no agent.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself microsegmentation lab. You will construct a five–virtual-machine enterprise in miniature on a single Windows 11 host, deliberately break it to prove that a flat network lets an attacker move sideways, and then apply **Akamai Guardicore Segmentation** to contain that movement.

Guardicore (formerly Guardicore Centra; acquired by **Akamai** in 2021) is a host-agent segmentation platform with two traits that shape this lab:

- Its **Reveal** map is drawn from flow telemetry that includes **process and user context**, not just IP and port — so a rule can say "only the `postgres` process, run by the `postgres` user, may serve 5432," which is a stronger statement than an address-and-port ACL.
- Its policy is a list of ordered **allow / block / alert** rules that you can run in an **alert-only** posture before you enforce, so you validate a rule by watching what it *would* do first.

The estate you build is intentionally heterogeneous — modern Linux servers, a Windows server, and an unpatchable "programmable logic controller" that cannot accept a security agent — because that mix is the reason segmentation platforms exist.

### An honest scope note — please read this before you start

Akamai Guardicore Segmentation is commercial software. Two consequences shape this lab:

1. **There is no single-laptop community edition.** The control plane (**Centra**: a Management server plus Aggregators and Collectors) and the agents are licensed and are paired to a management server you have been granted. Nothing on the public internet substitutes for it.
2. **The agent is registered against your management server.** You obtain the agent installer and its management address from the Centra console.

Therefore every exercise in Chapters 06–08 is written on **two tracks**:

- **Track 1 — Real Guardicore.** The actual Centra console navigation (Reveal, labels, policy), the agent registration, and the real verification points, for readers whose employer, partner account, or an Akamai evaluation has granted a Centra environment. Environment-specific values appear as placeholders such as `<centra-mgmt-fqdn>`.
- **Track 2 — Native equivalent.** A faithful reproduction you can run today with no Centra at all, driving the *same enforcement primitives the agent drives*: `nftables`/`iptables` on Linux and the Windows Filtering Platform on Windows, and reconstructing the process-aware flow map from `conntrack` and `ss -p`.

Track 2 is not a mock-up. The Guardicore agent does not invent a packet filter; it programs the native OS firewall. Writing the nftables rule yourself produces the artifact Centra's policy engine would have distributed. The management plane, the process-aware Reveal map, the label engine, and the alert-then-enforce lifecycle are what you are buying; the enforcement primitive is the one you can practice on for free.

Exercises that genuinely cannot be reproduced without the product — the Reveal map's process attribution, osquery-based Insight, and the threat-detection/deception features — are marked **Design Exercise** and are written analysis with a model answer.

### Conventions

| Convention | Meaning |
|:---|:---|
| `PS C:\>` | Run on the **Windows 11 host**, in an **elevated** PowerShell |
| `PS C:\Users\Administrator>` | Run inside the **gc-win01** guest VM, elevated |
| `user@gc-gw:~$` | Run inside the named Linux guest as a normal user |
| `#` prefix in a Linux block | Command requires `sudo` / root |
| `<angle brackets>` | A value you must substitute from your own environment |
| **Design Exercise** | No environment required and none simulated; written analysis with model answer |
| **Track 1** / **Track 2** | Real Guardicore path / native-equivalent path |

Every exercise follows the same five-part shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Rollback**. Do not skip the negative tests — proving that a thing is *blocked* is the entire product.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation and Workstation install | 45–90 min |
| B | Virtual network construction | 20 min |
| C | Building the five VMs | 3–4 hours (mostly unattended installs) |
| D | Baseline application and the flat-network attack | 45 min |
| E | Agents, Reveal, labels, and policy | 3–4 hours |
| F | The agentless OT device and Guardicore detection | 90 min |
| G | Operations, troubleshooting, teardown | 45 min |

Budget two comfortable days, or four evenings. Part C is the long pole and is largely waiting.

## Lab Overview

### Learning objectives

By the end of this lab you will be able to:

1. Describe the Centra architecture (Management, Aggregators, Collectors) and what the agent programs on Linux (`iptables`/`nftables`) and Windows (Windows Filtering Platform).
2. Satisfy the real agent prerequisites: administrative rights, resolution of and connectivity to the management server, a supported firewall backend, and a single controller of the native firewall.
3. Apply Guardicore's flexible **key/value labels** and write policy against labeled groups, not addresses.
4. Read the **Reveal** map, including its process-and-user context, and use it to discover flows before writing a rule.
5. Author ordered **allow / block / alert** policy, validate it in **alert-only** posture, then enforce it.
6. Ring-fence a two-tier application and tighten it to per-service, per-process rules.
7. Protect a device that **cannot run an agent** by enforcing on its managed neighbor, and reason about Guardicore's detection and deception coverage for OT.
8. Diagnose common failure modes and execute a break-glass rollback.

### Topology

Three isolated Layer 2 segments, joined by a single multi-homed Linux router that also becomes the managed enforcement point for the OT cell.

![Lab topology: the Windows 11 host, three VMware virtual networks (VMnet8 NAT "IT/Corporate", VMnet2 host-only "Data Center", VMnet3 host-only "OT Cell"), the five virtual machines, and the legitimate versus lateral-movement flows. gc-gw is the sole path between segments and the managed enforcement point protecting the agentless PLC.](../../../diagrams/volume-095-akamai-guardicore-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The five-VM IT/OT estate this lab builds: Guardicore agents on the router and the Data Center servers, the agentless PLC protected by policy on its managed neighbor (gc-gw), the two legitimate east-west flows allowed, and the compromised-HMI-to-database lateral movement denied.*

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
                  |  gc-gw     | .10            |
                  |  Ubuntu    |                |
                  |  22.04     |                |
                  |  agent +   |                |
                  |  router +  | .254           |
                  | ENFORCEMENT+----------------+=======================
                  |   POINT    |   VMnet2  Host-only - "Data Center"
                  |  for OT     |   10.10.20.0/24     (no DHCP)
                  |            |        |         |          |
                  |            |   +----+---+ +---+----+ +---+-----+
                  |            |   |gc-app01| |gc-db01 | |gc-win01 |
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
   Reachable ONLY through gc-gw = the managed enforcement point.
                        |
                  +-----+------+
                  |  gc-ot01   | .50
                  |  "PLC"     |
                  |  Modbus    |
                  |  TCP :502  |
                  |  AGENTLESS |
                  +------------+
```

The design choices are deliberate and each teaches something:

- **VMnet3 has no host virtual adapter.** The only way a packet reaches the PLC is through `gc-gw`. That property lets a managed neighbor enforce policy on behalf of a device that can run no agent.
- **VMnet2 has a host virtual adapter (10.10.20.1).** This is your out-of-band management path; it survives every policy you write. Lab 9.2 uses it as break-glass.
- `gc-gw` **is the default gateway for the Data Center segment.** All east-west and cross-segment traffic traverses it, so you can observe and enforce at a choke point.

### Address plan

| Host | Role | VMnet8 — IT/NAT | VMnet2 — Data Center | VMnet3 — OT Cell |
|:---|:---|:---|:---|:---|
| Windows 11 host | Admin console; "IT laptop" | 192.168.170.1 | 10.10.20.1 | *(none — by design)* |
| VMware NAT service | NAT gateway | 192.168.170.2 | — | — |
| **gc-gw** | Router; agent; OT enforcement point | 192.168.170.10 | 10.10.20.254 | 10.10.30.254 |
| **gc-app01** | Web/app tier, nginx :80; agent | — | 10.10.20.11 | — |
| **gc-db01** | PostgreSQL :5432; agent | — | 10.10.20.12 | — |
| **gc-win01** | Windows workload; SCADA/HMI; agent | — | 10.10.20.21 | — |
| **gc-ot01** | "PLC", Modbus TCP :502, agentless | — | — | 10.10.30.50 |

DNS for all guests: `192.168.170.2`. The agent must resolve and reach its management server, so DNS is the first thing to get right.

### Resource budget

| VM       | Guest OS                   | vCPU  | RAM         | Disk        | Runs during |
|:---------|:---------------------------|:------|:------------|:------------|:------------|
| gc-gw    | Ubuntu Server 22.04.5 LTS  | 1     | 1024 MB     | 20 GB       | All parts   |
| gc-app01 | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| gc-db01  | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| gc-win01 | Windows Server 2022 (Eval) | 2     | 4096 MB     | 60 GB       | E, F, G     |
| gc-ot01  | Ubuntu Server 22.04.5 LTS  | 1     | 768 MB      | 10 GB       | D, F, G     |
|          | **Peak concurrent**        | **6** | **~8.9 GB** | **~130 GB** |             |

**Host minimum:** 4 physical cores, 16 GB RAM, 250 GB free SSD. **Comfortable:** 8 cores, 32 GB RAM, 400 GB free NVMe. A real Centra management server is not run on this host; use an Akamai-provided environment for Track 1, or run Track 2.

### Bill of materials

| Item | Where | Size | Notes |
|:---|:---|:---|:---|
| VMware Workstation Pro 17.6.3 for Windows | Broadcom Support Portal | ~600 MB | **Free**, no license key. |
| Ubuntu Server 22.04.5 LTS ISO | `releases.ubuntu.com/jammy/` | ~2.0 GB | `ubuntu-22.04.5-live-server-amd64.iso` |
| Windows Server 2022 Evaluation ISO | Microsoft Evaluation Center | ~5.0 GB | 180-day evaluation |
| Guardicore agent + Centra access | Akamai (evaluation or partner) | — | **Track 1 only.** Track 2 needs none of this. |

Both Workstation 17.6.3 and its successor **26H1** (14 May 2026) work identically here; both are free and need no license key since 11 November 2024.

## Summary and Completion Checklist

- [ ] Topology, address plan, and resource budget understood.
- [ ] The Centra architecture and what the agent programs on Linux/Windows understood.
- [ ] Bill of materials downloaded.
- [ ] Track chosen: real Guardicore Centra (Track 1) or native equivalent (Track 2).
