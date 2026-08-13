# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and the two tracks it is written on (a real Zero Networks Segment deployment, or the native enforcement equivalent).
- Read the topology, address plan, and resource budget for the five-VM estate.
- Explain why Zero Networks is **agentless** and what that means for how policy actually lands on a host.
- Explain why the OT segment deliberately has no host adapter.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself microsegmentation lab. You will construct a five–virtual-machine enterprise in miniature on a single Windows 11 host, deliberately break it to prove that a flat network lets an attacker move sideways, and then apply **Zero Networks Segment** to contain that movement.

Zero Networks is a segmentation platform with three traits that shape this lab, and one of them makes the native track unusually faithful:

- It is **agentless**. It installs no agent on the protected hosts. Instead it uses a privileged service account to **remotely program each host's own firewall** — the **Windows Firewall** on Windows, `iptables`/`nftables` on Linux. The artifact that enforces policy is the native OS firewall you already own; Zero Networks is the automation that writes it.
- It **learns, then least-privileges**. For roughly **30 days** it watches traffic in a monitoring state, automatically proposes least-privilege allow rules from what it observed, and only then flips hosts to a default-deny posture.
- It applies **just-in-time MFA to privileged ports**. Administrative protocols — RDP, SSH, WinRM, SMB — are closed by default and opened, per host and per session, only after the requester passes **multi-factor authentication**. This is the platform's signature: segmentation of privileged access, not just of application traffic.

The estate you build is intentionally heterogeneous — Linux servers, a Windows server, and an unpatchable "programmable logic controller" — because that mix is the reason segmentation platforms exist.

### An honest scope note — please read this before you start

Zero Networks Segment is commercial software. Two consequences shape this lab:

1. **There is no single-laptop community edition.** The platform deploys as a management console plus connectors and uses a privileged service account to reach each host's firewall management interface. Nothing on the public internet substitutes for it.
2. **The learning-and-MFA workflow is the product.** The remote-firewall enforcement it produces you *can* reproduce natively — indeed you will, because it is the same native firewall — but the 30-day learning, automatic rule generation, and MFA gating are the platform's value.

Therefore every exercise in Chapters 06–08 is written on **two tracks**:

- **Track 1 — Real Zero Networks.** The actual console workflow — monitoring, reviewing learned rules, enabling protection, and configuring MFA for privileged ports — for readers whose employer or an evaluation has granted a deployment. Deployment-specific values appear as placeholders such as `<zn-console-fqdn>`.
- **Track 2 — Native equivalent.** A faithful reproduction with no console at all. Because Zero Networks programs the native firewall, you program the *same* `nftables`/Windows Filtering Platform rules by hand, and you simulate the learn-then-enforce lifecycle and the just-in-time MFA grant with a timed firewall rule.

Track 2 is unusually true to this product: for an agent-based platform, the native track approximates what the agent does; for Zero Networks, the native firewall **is** what the platform drives. The difference between the tracks is the automation and the MFA, not the enforcement primitive.

Exercises that genuinely cannot be reproduced without the product — the automatic rule learning at scale and the real MFA identity flow — are marked **Design Exercise** with a model answer.

### Conventions

| Convention | Meaning |
|:---|:---|
| `PS C:\>` | Run on the **Windows 11 host**, in an **elevated** PowerShell |
| `PS C:\Users\Administrator>` | Run inside the **zn-win01** guest VM, elevated |
| `user@zn-gw:~$` | Run inside the named Linux guest as a normal user |
| `#` prefix in a Linux block | Command requires `sudo` / root |
| `<angle brackets>` | A value you must substitute from your own environment |
| **Design Exercise** | No deployment required and none simulated; written analysis with model answer |
| **Track 1** / **Track 2** | Real Zero Networks path / native-equivalent path |

Every exercise follows the same five-part shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Rollback**. Do not skip the negative tests — proving a thing is *blocked* is the entire product.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation and Workstation install | 45–90 min |
| B | Virtual network construction | 20 min |
| C | Building the five VMs | 3–4 hours (mostly unattended installs) |
| D | Baseline application and the flat-network attack | 45 min |
| E | Monitoring, learned rules, and enforcement | 3–4 hours |
| F | Just-in-time MFA and the agentless OT device | 90 min |
| G | Operations, troubleshooting, teardown | 45 min |

Budget two comfortable days, or four evenings. Part C is the long pole and is largely waiting.

## Lab Overview

### Learning objectives

By the end of this lab you will be able to:

1. Explain how an agentless platform enforces policy by remotely programming the native host firewall, and verify the result on the OS.
2. Reproduce the **learn → least-privilege → enforce** lifecycle: monitor traffic, derive allow rules, then default-deny.
3. Ring-fence a two-tier application from learned rules and validate it before enforcing.
4. Configure **just-in-time MFA** for privileged ports so RDP/SSH are closed until an authenticated, time-boxed grant opens them.
5. Protect a device that can be neither agented nor remotely managed by enforcing on its managed neighbor.
6. Diagnose common failure modes and execute a break-glass rollback.

### Topology

Three isolated Layer 2 segments, joined by a single multi-homed Linux router that also becomes the enforcement point for the OT cell.

![Lab topology: the Windows 11 host, three VMware virtual networks (VMnet8 NAT "IT/Corporate", VMnet2 host-only "Data Center", VMnet3 host-only "OT Cell"), the five virtual machines, and the legitimate versus lateral-movement flows. zn-gw is the sole path between segments and the enforcement point protecting the agentless PLC.](../../../diagrams/volume-096-zero-networks-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The five-VM IT/OT estate this lab builds: Zero Networks remotely programs the native firewall on the router and the Data Center servers, the agentless PLC is protected by policy on its managed neighbor (zn-gw), the two legitimate east-west flows are allowed, and the compromised-HMI-to-database lateral movement is denied. Privileged ports (RDP/SSH) are closed until a just-in-time MFA grant opens them.*

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
                  |  zn-gw     | .10            |
                  |  Ubuntu    |                |
                  |  22.04     |                |
                  | native fw  |                |
                  |  router +  | .254           |
                  | ENFORCEMENT+----------------+=======================
                  |   POINT    |   VMnet2  Host-only - "Data Center"
                  |  for OT     |   10.10.20.0/24     (no DHCP)
                  |            |        |         |          |
                  |            |   +----+---+ +---+----+ +---+-----+
                  |            |   |zn-app01| |zn-db01 | |zn-win01 |
                  |            |   |  .11   | |  .12   | |  .21    |
                  |            |   | nginx  | |postgres| | Win2022 |
                  |            |   |  :80   | | :5432  | |SCADA/HMI|
                  |            |   |nativefw| |nativefw| |Win FW   |
                  |            |   +--------+ +--------+ +---------+
                  |            | .254
                  +-----+------+
  ================================================
   VMnet3  Host-only - "OT Cell"  10.10.30.0/24
   NO host adapter. NO DHCP. Fully isolated.
   Reachable ONLY through zn-gw = the enforcement point.
                        |
                  +-----+------+
                  |  zn-ot01   | .50
                  |  "PLC"     |
                  |  Modbus    |
                  |  TCP :502  |
                  |  AGENTLESS |
                  +------------+
```

The design choices are deliberate:

- **VMnet3 has no host virtual adapter.** The only path to the PLC is through `zn-gw`, which lets a managed neighbor enforce on behalf of a device that can be neither agented nor remotely managed.
- **VMnet2 has a host virtual adapter (10.10.20.1).** This out-of-band management path survives every policy; Lab 9.2 uses it as break-glass.
- `zn-gw` **is the default gateway for the Data Center segment.** All east-west and cross-segment traffic traverses it.

### Address plan

| Host | Role | VMnet8 — IT/NAT | VMnet2 — Data Center | VMnet3 — OT Cell |
|:---|:---|:---|:---|:---|
| Windows 11 host | Admin console; "IT laptop" | 192.168.170.1 | 10.10.20.1 | *(none — by design)* |
| VMware NAT service | NAT gateway | 192.168.170.2 | — | — |
| **zn-gw** | Router; OT enforcement point | 192.168.170.10 | 10.10.20.254 | 10.10.30.254 |
| **zn-app01** | Web/app tier, nginx :80 | — | 10.10.20.11 | — |
| **zn-db01** | PostgreSQL :5432 | — | 10.10.20.12 | — |
| **zn-win01** | Windows workload; SCADA/HMI | — | 10.10.20.21 | — |
| **zn-ot01** | "PLC", Modbus TCP :502, agentless | — | — | 10.10.30.50 |

DNS for all guests: `192.168.170.2`. In a real deployment, Zero Networks must reach each host's firewall management interface; here that path is the VMnet2 segment.

### Resource budget

| VM       | Guest OS                   | vCPU  | RAM         | Disk        | Runs during |
|:---------|:---------------------------|:------|:------------|:------------|:------------|
| zn-gw    | Ubuntu Server 22.04.5 LTS  | 1     | 1024 MB     | 20 GB       | All parts   |
| zn-app01 | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| zn-db01  | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| zn-win01 | Windows Server 2022 (Eval) | 2     | 4096 MB     | 60 GB       | E, F, G     |
| zn-ot01  | Ubuntu Server 22.04.5 LTS  | 1     | 768 MB      | 10 GB       | D, F, G     |
|          | **Peak concurrent**        | **6** | **~8.9 GB** | **~130 GB** |             |

**Host minimum:** 4 cores, 16 GB RAM, 250 GB free SSD. **Comfortable:** 8 cores, 32 GB RAM, 400 GB free NVMe.

### Bill of materials

| Item | Where | Size | Notes |
|:---|:---|:---|:---|
| VMware Workstation Pro 17.6.3 for Windows | Broadcom Support Portal | ~600 MB | **Free**, no license key. |
| Ubuntu Server 22.04.5 LTS ISO | `releases.ubuntu.com/jammy/` | ~2.0 GB | `ubuntu-22.04.5-live-server-amd64.iso` |
| Windows Server 2022 Evaluation ISO | Microsoft Evaluation Center | ~5.0 GB | 180-day evaluation |
| Zero Networks Segment access | Zero Networks (evaluation or partner) | — | **Track 1 only.** Track 2 needs none of this. |

Both Workstation 17.6.3 and 26H1 (14 May 2026) work identically here; both are free and need no license key since 11 November 2024.

## Summary and Completion Checklist

- [ ] Topology, address plan, and resource budget understood.
- [ ] The agentless model — remotely programmed native firewalls — understood.
- [ ] Bill of materials downloaded.
- [ ] Track chosen: real Zero Networks Segment (Track 1) or native equivalent (Track 2).
