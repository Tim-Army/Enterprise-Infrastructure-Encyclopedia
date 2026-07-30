# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and the two tracks it is written on (a real Illumio PCE and VEN, or the native enforcement equivalent).
- Read the topology, address plan, and resource budget for the five-VM estate.
- Assemble the bill of materials before starting.
- Explain why the OT segment deliberately has no host adapter, and why Illumio protects the device on it without an agent.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself microsegmentation lab. You will construct a five–virtual-machine enterprise in miniature on a single Windows 11 host, deliberately break it to prove that a flat network lets an attacker move sideways, and then apply **Illumio** segmentation to contain that movement.

The estate you build is intentionally heterogeneous, because that heterogeneity is the whole reason a platform like Illumio exists. You will end up with modern Linux servers, a Windows server, and an unpatchable "programmable logic controller" that cannot accept a security agent — the exact mix that forces an architect to enforce policy in more than one place: with an agent on the hosts that can take one, and from a managed neighbor for the host that cannot.

Illumio's model is worth stating on page one, because it shapes every later chapter:

- The **PCE (Policy Compute Engine)** is the brain and console. It holds your labels and policy and compiles that policy into per-workload rules.
- The **VEN (Virtual Enforcement Node)** is the agent on each workload. It does *not* carry its own packet filter; it programs the **native OS firewall** — `iptables`/`nftables` on Linux and the **Windows Filtering Platform (WFP)** on Windows — exactly as the workload's own firewall would be programmed by hand.
- Policy is written against **labels** (Role, Application, Environment, Location), never against IP addresses, so it survives re-addressing and cloning.

### An honest scope note — please read this before you start

Illumio is commercial software. Two consequences shape this lab, and it is better that you know them on page one than discover them at exercise fourteen:

1. **There is no single-laptop community PCE.** Illumio's control plane ships either as **Illumio Cloud** (SaaS) or as a **self-managed on-premises PCE** (an RPM/OVA cluster). The on-prem PCE expects a dedicated node with multiple cores and 8 GB or more of RAM, and both editions require a license. Nothing on the public internet is a free stand-in for it.
2. **The VEN is generated and paired against a PCE you have been granted.** You obtain the VEN package and a **pairing key** from the PCE's pairing profile. Without a PCE there is no pairing key.

Therefore every exercise in Chapters 06–08 is written on **two tracks**:

- **Track 1 — Real Illumio.** The exact console navigation, the real `illumio-ven-ctl` commands, and the real verification points. Follow this if your employer, partner account, or an Illumio trial has given you a PCE tenant. Where a value is tenant-specific it appears as a placeholder such as `<pce-fqdn>:8443` and the guide says where in the console to find it.
- **Track 2 — Native equivalent.** A faithful reproduction you can run today with no PCE at all, driving the *same enforcement primitives the VEN drives*: `nftables`/`iptables` on Linux and the Windows Filtering Platform on Windows.

Track 2 is not a cartoon of the product. The Illumio VEN does not invent a packet filter; it programs the native OS firewall. When you write an nftables rule that permits `il-app01 → il-db01` on TCP 5432 and drops everything else, you are hand-writing the artifact that the PCE's policy compiler would have generated for you. The management plane, the Illumination traffic map, the label model, and the draft-then-provision policy lifecycle are what you are buying; the enforcement primitive is the one you can practice on for free. Knowing exactly what lands on the host makes you far better at operating the product, and much faster at troubleshooting it, than someone who has only ever clicked the console.

Exercises that genuinely cannot be reproduced without the product — the Illumination map's flow correlation, the policy compiler, SecureConnect (VEN-to-VEN IPsec) — are marked **Design Exercise** and are structured as written analysis with a model answer, not as pretend clicking.

### Conventions

| Convention | Meaning |
|:---|:---|
| `PS C:\>` | Run on the **Windows 11 host**, in an **elevated** PowerShell |
| `PS C:\Users\Administrator>` | Run inside the **il-win01** guest VM, elevated |
| `user@il-gw:~$` | Run inside the named Linux guest as a normal user |
| `#` prefix in a Linux block | Command requires `sudo` / root |
| `<angle brackets>` | A value you must substitute from your own environment |
| **Design Exercise** | No tenant required and none simulated; written analysis with model answer |
| **Track 1** / **Track 2** | Real Illumio path / native-equivalent path |

Every exercise follows the same five-part shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Cleanup**. Do not skip the negative tests. In segmentation work, proving that a thing is *blocked* is the entire product; proving that a thing is allowed only proves you have a network.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation and Workstation install | 45–90 min |
| B | Virtual network construction | 20 min |
| C | Building the five VMs | 3–4 hours (mostly unattended installs) |
| D | Baseline application and the flat-network attack | 45 min |
| E | VEN onboarding, Illumination, labels, and policy | 3–4 hours |
| F | Protecting the agentless OT device from a managed neighbor | 90 min |
| G | Operations, troubleshooting, teardown | 45 min |

Budget two comfortable days, or four evenings. Part C is the long pole and is largely waiting.

## Lab Overview

### Learning objectives

By the end of this lab you will be able to:

1. Explain the split between the **PCE** (policy and visibility) and the **VEN** (enforcement on the workload), and describe precisely what the VEN does to a Linux host (`iptables`/`nftables`) and to a Windows host (Windows Filtering Platform).
2. Satisfy the real VEN prerequisites: administrative rights, DNS resolution of the PCE FQDN, outbound TCP to the PCE on 8443/8444, a supported kernel/firewall backend, and the removal of any competing controller of the native firewall.
3. Apply Illumio's **label model** (Role, Application, Environment, Location) and write policy against labels rather than addresses.
4. Move a workload through the **enforcement states** — Idle, **Visibility Only**, **Selective Enforcement**, **Full Enforcement** — and use Visibility Only as the safety net it is designed to be.
5. Use **Illumination** (the traffic map) to discover real flows before writing a single rule.
6. Author **rulesets** and **rules** that permit a two-tier application and deny lateral reach into it, validate them in draft, then **provision** them.
7. Protect a device that **cannot run a VEN** by making its managed neighbor the enforcement point and applying an **enforcement boundary**, then default-deny everything else.
8. Diagnose the common failure modes and execute a break-glass rollback.

### Topology

Three isolated Layer 2 segments, joined by a single multi-homed Linux router that also becomes the managed enforcement point for the OT cell.

![Lab topology: the Windows 11 host, three VMware virtual networks (VMnet8 NAT "IT/Corporate", VMnet2 host-only "Data Center", VMnet3 host-only "OT Cell"), the five virtual machines, and the legitimate versus lateral-movement flows. il-gw is the sole path between segments and the managed enforcement point protecting the agentless PLC.](../../../diagrams/volume-094-illumio-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The five-VM IT/OT estate this lab builds: VENs on the Data Center servers and the router, the agentless PLC protected by an enforcement boundary on its managed neighbor (il-gw), the two legitimate east-west flows allowed, and the compromised-HMI-to-database lateral movement denied.*

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
                  |  il-gw     | .10            |
                  |  Ubuntu    |                |
                  |  22.04     |                |
                  |  VEN +     |                |
                  |  router +  | .254           |
                  | ENFORCEMENT+----------------+=======================
                  |   POINT    |   VMnet2  Host-only - "Data Center"
                  |  for OT     |   10.10.20.0/24     (no DHCP)
                  |            |        |         |          |
                  |            |   +----+---+ +---+----+ +---+-----+
                  |            |   |il-app01| |il-db01 | |il-win01 |
                  |            |   |  .11   | |  .12   | |  .21    |
                  |            |   | nginx  | |postgres| | Win2022 |
                  |            |   |  :80   | | :5432  | |SCADA/HMI|
                  |            |   |  VEN   | |  VEN   | |  VEN    |
                  |            |   +--------+ +--------+ +---------+
                  |            | .254
                  +-----+------+
  ================================================
   VMnet3  Host-only - "OT Cell"  10.10.30.0/24
   NO host adapter. NO DHCP. Fully isolated.
   Reachable ONLY through il-gw = the managed enforcement point.
                        |
                  +-----+------+
                  |  il-ot01   | .50
                  |  "PLC"     |
                  |  Modbus    |
                  |  TCP :502  |
                  |  AGENTLESS |
                  +------------+
```

The design choices here are deliberate and each teaches something:

- **VMnet3 has no host virtual adapter.** The Windows host has no Layer 2 presence in the OT cell. The only way a packet reaches the PLC is through `il-gw`. That physical property is what lets a managed neighbor enforce policy *on behalf of* a device that can run no agent: because all of the PLC's traffic transits `il-gw`, a rule on `il-gw` polices the PLC completely.
- **VMnet2 does have a host virtual adapter (10.10.20.1).** This is your out-of-band management path. It deliberately survives every policy you write. Real segmentation deployments always retain a management channel, and the discipline of *knowing* which path is your break-glass — rather than discovering it under pressure — is worth practising. Lab 9.2 uses it.
- `il-gw` **is the default gateway for the Data Center segment as well.** All east-west traffic between segments and all egress traverses it, so you can observe flows at a choke point and, later, enforce there. This mirrors how most organizations start: flow data at the router, long before agents.

### Address plan

Commit this table to a sticky note. Almost every troubleshooting session in this lab ends at it.

| Host | Role | VMnet8 — IT/NAT | VMnet2 — Data Center | VMnet3 — OT Cell |
|:---|:---|:---|:---|:---|
| Windows 11 host | Admin console; "IT laptop" | 192.168.170.1 | 10.10.20.1 | *(none — by design)* |
| VMware NAT service | NAT gateway | 192.168.170.2 | — | — |
| **il-gw** | Router; VEN; OT enforcement point | 192.168.170.10 | 10.10.20.254 | 10.10.30.254 |
| **il-app01** | Web/app tier, nginx :80; VEN | — | 10.10.20.11 | — |
| **il-db01** | PostgreSQL :5432; VEN | — | 10.10.20.12 | — |
| **il-win01** | Windows workload; SCADA/HMI; VEN | — | 10.10.20.21 | — |
| **il-ot01** | "PLC", Modbus TCP :502, agentless | — | — | 10.10.30.50 |

DNS for all guests: `192.168.170.2` (the VMware NAT service forwards to your host's resolvers). This matters more than it looks — the VEN must resolve the PCE FQDN or it will never pair, and DNS is the single most common cause of a stuck VEN.

### Resource budget

| VM       | Guest OS                   | vCPU  | RAM         | Disk        | Runs during |
|:---------|:---------------------------|:------|:------------|:------------|:------------|
| il-gw    | Ubuntu Server 22.04.5 LTS  | 1     | 1024 MB     | 20 GB       | All parts   |
| il-app01 | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| il-db01  | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| il-win01 | Windows Server 2022 (Eval) | 2     | 4096 MB     | 60 GB       | E, F, G     |
| il-ot01  | Ubuntu Server 22.04.5 LTS  | 1     | 768 MB      | 10 GB       | D, F, G     |
|          | **Peak concurrent**        | **6** | **~8.9 GB** | **~130 GB** |             |

**Host minimum:** 4 physical cores, 16 GB RAM, 250 GB free SSD. **Host comfortable:** 8 cores, 32 GB RAM, 400 GB free NVMe.

On a 16 GB host, do not run all five at once during Part C; build and shut down each VM in turn. From Part D onward, all five running together fits inside 16 GB with roughly 6 GB left for Windows 11 — tight but workable. If you also intend to run a real on-premises PCE (Track 1), it needs its own dedicated node and will not share this host comfortably; use Illumio Cloud (SaaS) for Track 1 instead, or run Track 2.

### Bill of materials

Download everything before you begin. Total download is roughly 8 GB.

| Item | Where | Size | Notes |
|:---|:---|:---|:---|
| VMware Workstation Pro 17.6.3 for Windows | Broadcom Support Portal | ~600 MB | **Free**, no license key, for commercial, educational, and personal use. Requires a free Broadcom account. |
| Ubuntu Server 22.04.5 LTS ISO | `releases.ubuntu.com/jammy/` | ~2.0 GB | File: `ubuntu-22.04.5-live-server-amd64.iso` |
| Windows Server 2022 Evaluation ISO | Microsoft Evaluation Center | ~5.0 GB | 180-day evaluation |
| PuTTY or Windows Terminal + OpenSSH | Built into Windows 11 | — | `ssh` is present by default on Windows 11 |
| Illumio VEN + PCE access | Illumio (SaaS trial or partner tenant) | — | **Track 1 only.** Obtain the VEN package and pairing key from **Infrastructure → Ventura/Pairing Profiles** in the PCE. Track 2 needs none of this. |

**A note on Workstation versions.** This guide targets **Workstation Pro 17.6.3**, the final 17.x release. Broadcom shipped the successor, **VMware Workstation Pro 26H1** (build 25388281), on **14 May 2026**; everything in this lab works identically on it — the Virtual Network Editor, the NAT service, host-only networks, and snapshots are unchanged in every respect this lab touches. Both are free. Since **11 November 2024**, VMware Workstation Pro has required no license key for commercial, educational, or personal use.

## Summary and Completion Checklist

- [ ] Topology, address plan, and resource budget understood.
- [ ] The PCE-versus-VEN split, and what the VEN programs on Linux and Windows, understood.
- [ ] Bill of materials downloaded and checksummed.
- [ ] Track chosen: real Illumio PCE (Track 1) or native equivalent (Track 2).
