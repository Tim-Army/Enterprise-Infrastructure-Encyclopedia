# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and the two tracks it is written on (a real Elisity Cloud deployment, or the native equivalent).
- Read the four-segment topology, address plan, and resource budget.
- Explain how Elisity's identity-based, network-enforced model differs from a per-host agent — and why the database sits on its own segment in this lab.
- Explain why the OT segment deliberately has no host adapter.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself microsegmentation lab. You will construct a five–virtual-machine enterprise in miniature on a single Windows 11 host, deliberately break it to prove that a flat network lets an attacker move sideways, and then apply **Elisity** to contain that movement.

Elisity is different from the host-agent platforms in this series in two important ways:

- It is **identity-based and network-enforced**. Elisity classifies every user, device, and workload in an **IdentityGraph** built by ingesting from identity and context sources you already run — Active Directory, Entra ID (Azure AD), vCenter, ServiceNow, Infoblox, EDR, and CMDBs — and it writes policy against those **identities and attributes**, never against IP addresses.
- It **uses the network you already have**. Elisity enforces on the **existing access switches** through a cloud control plane (**Elisity Cloud**) and a lightweight connector (**Virtual Edge**) — **no agents on endpoints and no new hardware**. The switch, which already sees the traffic, becomes the enforcement point.

The estate you build is intentionally heterogeneous — Linux servers, a Windows server, and an unpatchable "programmable logic controller" — because that mix is the reason segmentation platforms exist.

### An honest scope note — please read this before you start

Elisity is commercial software, and its enforcement point is a **managed access switch**. Two consequences shape this lab:

1. **There is no single-laptop community edition, and no managed physical switch in a VM lab.** Elisity Cloud, the Virtual Edge connector, and switch integration are licensed and assume real switching infrastructure.
2. **So this lab models the switch with a router.** The `el-gw` Linux router is the single network device every cross-segment flow crosses; it stands in for the Elisity-managed access switch as the **network enforcement point**. To make that stand-in *complete* for the asset that matters most, the **database sits on its own segment behind `el-gw`** — so every access to the crown jewel is policed at the enforcement point, exactly as an access switch would police it. (A real switch also sees intra-VLAN traffic; the router does not, which is why the tested flows are arranged to cross it.)

Therefore every exercise in Chapters 06–08 is written on **two tracks**:

- **Track 1 — Real Elisity.** The Elisity Cloud workflow — connecting identity sources, reviewing the IdentityGraph, building identity-based policy groups and policy, and enforcing through the Virtual Edge on your switches — for readers with a deployment. Deployment-specific values appear as placeholders such as `<elisity-tenant>`.
- **Track 2 — Native equivalent.** A faithful reproduction with no cloud tenant. You build an **IdentityGraph** by hand from the same kinds of sources (an inventory/CMDB file, hostnames, an identity-attribute map), derive identity-based policy groups, and enforce the resulting ACLs on `el-gw` — the network enforcement point.

Track 2 is not a mock-up of the idea. Elisity's core insight is *classify by identity, then enforce on the network*; building the classification yourself and compiling it into switch-style ACLs is exactly that, minus the cloud automation and the live source integrations.

Exercises that genuinely cannot be reproduced without the product — live IdentityGraph ingestion, the Virtual Edge, and switch programming at scale — are marked **Design Exercise** with a model answer.

### Conventions

| Convention | Meaning |
|:---|:---|
| `PS C:\>` | Run on the **Windows 11 host**, in an **elevated** PowerShell |
| `PS C:\Users\Administrator>` | Run inside the **el-win01** guest VM, elevated |
| `user@el-gw:~$` | Run inside the named Linux guest as a normal user |
| `#` prefix in a Linux block | Command requires `sudo` / root |
| `<angle brackets>` | A value you must substitute from your own environment |
| **Design Exercise** | No deployment required and none simulated; written analysis with model answer |
| **Track 1** / **Track 2** | Real Elisity path / native-equivalent path |

Every exercise follows the same five-part shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Cleanup**. Do not skip the negative tests — proving a thing is *blocked* is the entire product.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation and Workstation install | 45–90 min |
| B | Virtual network construction (four segments) | 25 min |
| C | Building the five VMs | 3–4 hours (mostly unattended installs) |
| D | Baseline application and the flat-network attack | 45 min |
| E | IdentityGraph, policy groups, and enforcement | 3–4 hours |
| F | Policy for the agentless OT device | 90 min |
| G | Operations, troubleshooting, teardown | 45 min |

Budget two comfortable days, or four evenings. Part C is the long pole and is largely waiting.

## Lab Overview

### Learning objectives

By the end of this lab you will be able to:

1. Explain how Elisity classifies assets in an IdentityGraph from existing sources and enforces on the network, with no endpoint agents.
2. Build an IdentityGraph by hand and derive identity-based **policy groups** from it.
3. Author identity-based policy and enforce it at the network choke point.
4. Ring-fence a database that sits behind the enforcement point, and validate before enforcing.
5. Protect a device that can host no agent using the same network enforcement point.
6. Diagnose common failure modes and execute a break-glass rollback.

### Topology

Four segments, joined by a single multi-homed Linux router that stands in for the Elisity-managed access switch and enforces all cross-segment policy.

![Lab topology: the Windows 11 host, four VMware virtual networks (VMnet8 NAT "IT/Corporate", VMnet2 host-only "Data Center", VMnet4 host-only "Database", VMnet3 host-only "OT Cell"), the five virtual machines, and the legitimate versus lateral-movement flows. el-gw is the sole path between segments and the network enforcement point standing in for the Elisity-managed access switch.](../../../diagrams/volume-098-elisity-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The five-VM estate this lab builds: el-gw is the network enforcement point (the access-switch stand-in) that all cross-segment traffic crosses. The database sits on its own segment behind el-gw, the agentless PLC on the isolated OT segment. The two legitimate east-west flows are allowed; the compromised-HMI-to-database lateral movement is denied by identity-based policy.*

A text-only rendering of the same topology follows for reference:

```text
                    +----------------------------------------------+
                    |   Windows 11 Education host                  |
                    |   VMware Workstation Pro 17.6.3              |
                    |   Roles: admin console + "IT laptop"         |
                    |          (the untrusted lateral-movement     |
                    |           source in Lab 5.3)             |
                    +---+-------------+-------------+--------------+
                        | .170.1      | 10.10.20.1  | 10.10.40.1
  ======================+=======      |             | (host vNICs)
   VMnet8 NAT "IT"              |      |             |
   192.168.170.0/24            |      |             |
                        |      |      |             |
                  +-----+------+      |             |
                  |  el-gw     |.10   |             |
                  |  Ubuntu    |      |             |
                  |  4-legged  |      |             |
                  |  router =  |.254 (DC)           |
                  | NETWORK    +------+=============+========
                  | ENFORCEMENT|   VMnet2 "Data Center"
                  |  POINT     |   10.10.20.0/24 (no DHCP)
                  | (Elisity   |        |            |
                  |  access-   |   +----+---+   +----+----+
                  |  switch    |   |el-app01|   |el-win01 |
                  |  stand-in) |   |  .11   |   |  .21    |
                  |            |   | nginx  |   | Win2022 |
                  |            |   |  :80   |   |SCADA/HMI|
                  |            |   +--------+   +---------+
                  |            |.254 (DB)
                  |            +------+=====================
                  |            |   VMnet4 "Database" 10.10.40.0/24
                  |            |        |     (no DHCP; crown jewel isolated)
                  |            |   +----+----+
                  |            |   | el-db01 |
                  |            |   |  .40    |
                  |            |   |postgres |
                  |            |   |  :5432  |
                  |            |   +---------+
                  |            |.254 (OT)
                  +-----+------+
  ================================================
   VMnet3 "OT Cell" 10.10.30.0/24 (isolated, no host adapter)
                        |
                  +-----+------+
                  |  el-ot01   |.50
                  |  "PLC"     |
                  |  Modbus    |
                  |  TCP :502  |
                  |  AGENTLESS |
                  +------------+
```

The design choices are deliberate:

- **The database is on its own segment (VMnet4) behind `el-gw`.** Every access to it — legitimate or not — crosses the enforcement point, so `el-gw` polices it completely, the way an access switch would. This is the key modeling choice that makes network enforcement honest in a router-only lab.
- **VMnet3 (OT) has no host virtual adapter.** The only path to the PLC is through `el-gw`.
- **VMnet2 and VMnet4 have host adapters (10.10.20.1, 10.10.40.1).** These out-of-band management paths survive every policy; Lab 9.2 uses them as break-glass. The tested attack flows originate on the DC segment and cross `el-gw`, not these management adapters.

### Address plan

| Host | Role | VMnet8 IT/NAT | VMnet2 DC | VMnet4 DB | VMnet3 OT |
|:---|:---|:---|:---|:---|:---|
| Windows 11 host | Admin; "IT laptop" | 192.168.170.1 | 10.10.20.1 | 10.10.40.1 | *(none)* |
| VMware NAT | NAT gateway | 192.168.170.2 | — | — | — |
| **el-gw** | Router; network enforcement point | 192.168.170.10 | 10.10.20.254 | 10.10.40.254 | 10.10.30.254 |
| **el-app01** | Web/app tier, nginx :80 | — | 10.10.20.11 | — | — |
| **el-win01** | Windows workload; SCADA/HMI | — | 10.10.20.21 | — | — |
| **el-db01** | PostgreSQL :5432 (isolated) | — | — | 10.10.40.40 | — |
| **el-ot01** | "PLC", Modbus TCP :502, agentless | — | — | — | 10.10.30.50 |

DNS for all guests: `192.168.170.2`.

### Resource budget

| VM       | Guest OS                   | vCPU  | RAM         | Disk        | Runs during |
|:---------|:---------------------------|:------|:------------|:------------|:------------|
| el-gw    | Ubuntu Server 22.04.5 LTS  | 1     | 1024 MB     | 20 GB       | All parts   |
| el-app01 | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| el-db01  | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| el-win01 | Windows Server 2022 (Eval) | 2     | 4096 MB     | 60 GB       | E, F, G     |
| el-ot01  | Ubuntu Server 22.04.5 LTS  | 1     | 768 MB      | 10 GB       | D, F, G     |
|          | **Peak concurrent**        | **6** | **~8.9 GB** | **~130 GB** |             |

**Host minimum:** 4 cores, 16 GB RAM, 250 GB free SSD. **Comfortable:** 8 cores, 32 GB RAM, 400 GB free NVMe.

### Bill of materials

| Item | Where | Size | Notes |
|:---|:---|:---|:---|
| VMware Workstation Pro 17.6.3 for Windows | Broadcom Support Portal | ~600 MB | **Free**, no license key. |
| Ubuntu Server 22.04.5 LTS ISO | `releases.ubuntu.com/jammy/` | ~2.0 GB | `ubuntu-22.04.5-live-server-amd64.iso` |
| Windows Server 2022 Evaluation ISO | Microsoft Evaluation Center | ~5.0 GB | 180-day evaluation |
| Elisity Cloud access | Elisity (evaluation or partner) | — | **Track 1 only.** Track 2 needs none of this. |

Both Workstation 17.6.3 and 26H1 (14 May 2026) work identically here; both are free and need no license key since 11 November 2024.

## Summary and Completion Checklist

- [ ] Four-segment topology, address plan, and resource budget understood.
- [ ] The identity-based, network-enforced model — and why the database is isolated behind el-gw — understood.
- [ ] Bill of materials downloaded.
- [ ] Track chosen: real Elisity Cloud (Track 1) or native equivalent (Track 2).
