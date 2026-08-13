# Chapter 01: Lab Overview and Topology

## Learning Objectives

- State what this lab builds and the two tracks it is written on (a real Airwall deployment, or a native encrypted overlay).
- Read the topology, address plan, and resource budget for the five-VM estate and its overlay.
- Explain the Host Identity Protocol (HIP) overlay model — cryptographic identity, encryption, cloaking, default-deny — and how WireGuard reproduces it.
- Explain why the OT segment deliberately has no host adapter.

## How to Use This Guide

### What this lab is

This is a self-contained, build-it-yourself microsegmentation lab. You will construct a five–virtual-machine enterprise in miniature on a single Windows 11 host, deliberately break it to prove that a flat network lets an attacker move sideways, and then apply **Tempered Airwall** to contain that movement.

Airwall (from Tempered Networks, acquired by **Johnson Controls** in June 2022) is unlike every other platform in this series: it does not filter the network you have — it builds a **new, encrypted overlay** on top of it and moves your protected devices onto it. Three ideas define the model:

- **Cryptographic identity (HIP).** Airwall is built on the **Host Identity Protocol**. Every protected thing — an **Airwall Agent** on a host, or an **Airwall Gateway** in front of devices that can run no agent — has a cryptographic identity, and devices are authorized by that identity, not by IP address.
- **Encryption and cloaking.** All overlay traffic is encrypted end to end, and protected devices are **cloaked**: they do not respond to anything on the underlay network, so they are invisible and unaddressable except through the overlay. The default is *dark* — nothing connects until you say so.
- **Trust policy in the Conductor.** The **Airwall Conductor** is the console where you define **overlay networks**: which identities may communicate. Microsegmentation is expressed as overlay membership, not as firewall rules.

The estate you build is intentionally heterogeneous — Linux servers, a Windows server, and an unpatchable "programmable logic controller" — because that mix is the reason segmentation platforms exist.

### An honest scope note — please read this before you start

Airwall is commercial software. Two consequences shape this lab:

1. **There is no single-laptop community edition.** The Conductor, Airwall Gateways, and Airwall Agents are licensed through Johnson Controls. Nothing on the public internet is a free Airwall.
2. **But the overlay model has a faithful open equivalent.** Airwall's HIP overlay — cryptographic peer identity, always-on encryption, default-deny, and cloaking — is reproduced almost one-for-one by **WireGuard**: peers are identified by a **public key** (cryptographic identity), all traffic is encrypted, only explicitly-configured peers can communicate (default-deny), and a WireGuard endpoint silently ignores unauthenticated packets (cloaking).

Therefore every exercise in Chapters 06–08 is written on **two tracks**:

- **Track 1 — Real Airwall.** The Conductor workflow — provisioning Airwall Agents and Gateways, licensing identities, and building overlay networks and trust — for readers with a deployment. Deployment-specific values appear as placeholders such as `<conductor-fqdn>`.
- **Track 2 — Native equivalent.** A real encrypted overlay built with **WireGuard**: cryptographic identities (keys), a hub on `aw-gw` that enforces the trust policy, **cloaking** of the underlay so devices talk only over the overlay, and an `aw-gw` **gateway** that carries the agentless PLC onto the overlay just as an Airwall Gateway does.

This is the one volume in the series whose native track is not host-firewall rules but a genuine **encrypted overlay** — because that is what Airwall actually is.

### Conventions

| Convention | Meaning |
|:---|:---|
| `PS C:\>` | Run on the **Windows 11 host**, in an **elevated** PowerShell |
| `PS C:\Users\Administrator>` | Run inside the **aw-win01** guest VM, elevated |
| `user@aw-gw:~$` | Run inside the named Linux guest as a normal user |
| `#` prefix in a Linux block | Command requires `sudo` / root |
| `<angle brackets>` | A value you must substitute from your own environment |
| **Design Exercise** | No deployment required and none simulated; written analysis with model answer |
| **Track 1** / **Track 2** | Real Airwall path / native-overlay path |

Every exercise follows the same five-part shape: **Objective**, **Walkthrough**, **Expected result**, **Negative test**, **Rollback**. Do not skip the negative tests — proving a thing is *blocked* is the entire product.

### Time and effort

| Part | Content | Approximate time |
|:---|:---|:---|
| A | Host preparation and Workstation install | 45–90 min |
| B | Virtual network construction | 20 min |
| C | Building the five VMs | 3–4 hours (mostly unattended installs) |
| D | Baseline application and the flat-network attack | 45 min |
| E | The HIP overlay: identities, connection, and cloaking | 3–4 hours |
| F | The Airwall Gateway and the agentless OT device | 90 min |
| G | Operations, troubleshooting, teardown | 45 min |

Budget two comfortable days, or four evenings. Part C is the long pole and is largely waiting.

## Lab Overview

### Learning objectives

By the end of this lab you will be able to:

1. Explain the HIP overlay model — cryptographic identity, encryption, cloaking, default-deny — and map each idea to its WireGuard equivalent.
2. Build an encrypted overlay, give each protected device a cryptographic identity, and connect them through a hub.
3. **Cloak** the underlay so protected devices communicate only over the encrypted overlay.
4. Express microsegmentation as overlay trust policy — which identities may talk — and enforce it.
5. Carry a device that can run no agent onto the overlay with a gateway, and protect it there.
6. Diagnose common failure modes and execute a break-glass rollback.

### Topology

Three underlay segments joined by a single multi-homed Linux router that plays the Airwall Gateway for the OT cell and the hub of the encrypted overlay.

![Lab topology: the Windows 11 host, three VMware underlay segments (VMnet8 NAT "IT/Corporate", VMnet2 host-only "Data Center", VMnet3 host-only "OT Cell"), the five virtual machines, and the encrypted overlay that carries all protected traffic. aw-gw is the overlay hub and the Airwall Gateway that cloaks the agentless PLC.](../../../diagrams/volume-099-tempered-airwall-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The five-VM estate this lab builds: the servers and HMI run an overlay agent (WireGuard); the agentless PLC is carried onto the overlay by the aw-gw gateway. After cloaking, protected devices are dark on the underlay and reach each other only through the encrypted overlay, where trust policy on aw-gw permits app→db and hmi→plc and denies the rest.*

A text-only rendering of the same topology follows for reference:

```text
                    +----------------------------------------------+
                    |   Windows 11 Education host                  |
                    |   VMware Workstation Pro 17.6.3              |
                    |   Roles: admin console + "IT laptop"         |
                    |          (the untrusted lateral-movement     |
                    |           source in Lab 5.3)             |
                    +---+-----------------------+------------------+
                        | 192.168.170.1         | 10.10.20.1
  ======================+===============        |
   VMnet8 NAT "IT" 192.168.170.0/24             |
                        |                       |
                  +-----+------+                |
                  |  aw-gw     | .10            |   ~~~ encrypted overlay ~~~
                  |  Ubuntu    |                |   10.99.0.0/24 (WireGuard)
                  |  router +  | .254           |   hub .254
                  | OVERLAY HUB+----------------+=======================
                  | + AIRWALL  |   VMnet2 "Data Center" 10.10.20.0/24
                  |  GATEWAY   |        |         |          |
                  | (for OT)   |   +----+---+ +---+----+ +---+-----+
                  |            |   |aw-app01| |aw-db01 | |aw-win01 |
                  |            |   | .11    | | .12    | | .21     |
                  |            |   | ovl .11| | ovl .12| | ovl .21 |
                  |            |   | nginx  | |postgres| |SCADA/HMI|
                  |            |   +--------+ +--------+ +---------+
                  |            | .254
                  +-----+------+
  ================================================
   VMnet3 "OT Cell" 10.10.30.0/24 (isolated, no host adapter)
   PLC carried onto the overlay by the aw-gw gateway
                        |
                  +-----+------+
                  |  aw-ot01   | .50
                  |  "PLC"     |
                  |  Modbus    |
                  |  TCP :502  |
                  |  AGENTLESS |
                  +------------+
```

The design choices are deliberate:

- **The overlay (10.99.0.0/24) is where protected devices actually talk.** After cloaking, the underlay addresses (10.10.20.x) stop being usable between protected devices; all their traffic rides the encrypted overlay through the `aw-gw` hub, which enforces trust policy.
- **VMnet3 (OT) has no host virtual adapter.** The PLC is reachable only through `aw-gw`, which carries it onto the overlay as an Airwall Gateway would.
- **VMnet2 has a host adapter (10.10.20.1).** This out-of-band underlay path is your break-glass; it deliberately stays outside the overlay.

### Address plan

| Host | Role | Underlay (VMnet) | Overlay (10.99.0.0/24) |
|:---|:---|:---|:---|
| Windows 11 host | Admin; "IT laptop" | 192.168.170.1 / 10.10.20.1 | *(not on overlay)* |
| **aw-gw** | Router; overlay hub; Airwall Gateway | .170.10 / 10.10.20.254 / 10.10.30.254 | 10.99.0.254 |
| **aw-app01** | Web/app tier, nginx :80 | 10.10.20.11 | 10.99.0.11 |
| **aw-db01** | PostgreSQL :5432 | 10.10.20.12 | 10.99.0.12 |
| **aw-win01** | Windows workload; SCADA/HMI | 10.10.20.21 | 10.99.0.21 |
| **aw-ot01** | "PLC", Modbus TCP :502, agentless | 10.10.30.50 | *(via aw-gw gateway)* |

DNS for all guests: `192.168.170.2`.

### Resource budget

| VM       | Guest OS                   | vCPU  | RAM         | Disk        | Runs during |
|:---------|:---------------------------|:------|:------------|:------------|:------------|
| aw-gw    | Ubuntu Server 22.04.5 LTS  | 1     | 1024 MB     | 20 GB       | All parts   |
| aw-app01 | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| aw-db01  | Ubuntu Server 22.04.5 LTS  | 1     | 1536 MB     | 20 GB       | D, E, G     |
| aw-win01 | Windows Server 2022 (Eval) | 2     | 4096 MB     | 60 GB       | E, F, G     |
| aw-ot01  | Ubuntu Server 22.04.5 LTS  | 1     | 768 MB      | 10 GB       | D, F, G     |
|          | **Peak concurrent**        | **6** | **~8.9 GB** | **~130 GB** |             |

**Host minimum:** 4 cores, 16 GB RAM, 250 GB free SSD. **Comfortable:** 8 cores, 32 GB RAM, 400 GB free NVMe.

### Bill of materials

| Item | Where | Size | Notes |
|:---|:---|:---|:---|
| VMware Workstation Pro 17.6.3 for Windows | Broadcom Support Portal | ~600 MB | **Free**, no license key. |
| Ubuntu Server 22.04.5 LTS ISO | `releases.ubuntu.com/jammy/` | ~2.0 GB | `ubuntu-22.04.5-live-server-amd64.iso` |
| Windows Server 2022 Evaluation ISO | Microsoft Evaluation Center | ~5.0 GB | 180-day evaluation |
| WireGuard | Ubuntu repo (`wireguard`), Windows installer | small | **Track 2** — the native overlay. Free and open source. |
| Airwall Conductor + Agents/Gateways | Johnson Controls | — | **Track 1 only.** |

Both Workstation 17.6.3 and 26H1 (14 May 2026) work identically here; both are free and need no license key since 11 November 2024.

## Summary and Completion Checklist

- [ ] Topology, address plan, overlay plan, and resource budget understood.
- [ ] The HIP overlay model — identity, encryption, cloaking, default-deny — mapped to WireGuard.
- [ ] Bill of materials downloaded.
- [ ] Track chosen: real Airwall (Track 1) or native WireGuard overlay (Track 2).
