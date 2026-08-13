# Chapter 01: Lab Overview and Topology

![Lab topology: the Aruba CX 10000 top-of-rack switch embeds a Pensando DPU running a stateful firewall for east-west traffic at line rate, managed by PSM/Fabric Composer. A default-deny stateful policy permits web-to-db:5432 and hmi-to-plc:502; return traffic is permitted by connection state (no reverse rule), and hmi-to-db plus any unsolicited/invalid packet is dropped.](../../../diagrams/volume-119-hpe-aruba-cx10000-lab/chapter-01-lab-topology.svg)

*Figure 1-1. The Aruba CX 10000 firewalls east-west in the switch DPU with connection tracking: only the two flows are permitted, replies are carried by state rather than a reverse rule, and the lateral flow and unsolicited reverse-tuple packets are dropped — firewall-grade stateful policy at line rate, no hairpin.*

## Learning Objectives

- State what this lab builds and how the Aruba CX 10000 puts a **stateful firewall in the top-of-rack switch** via a DPU.
- Understand **stateful** segmentation (connection tracking) versus the stateless ACLs of earlier fabrics.
- Understand the two tracks — a design view of the CX 10000 and PSM, and a buildable stateful model.
- Read the lab topology and the policy plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab modeled on the **HPE Aruba CX 10000 distributed services switch**, which embeds an **AMD Pensando DPU** in the top-of-rack (ToR) switch. The DPU runs **stateful services** — a **stateful firewall**, microsegmentation, NAT, and per-flow telemetry — at line rate for east-west traffic, so every flow between servers in the rack is firewalled **in the switch**, with **connection tracking**, without hair-pinning to a separate firewall. Policy is managed centrally by the **Pensando Policy and Services Manager (PSM)** and **Aruba Fabric Composer**.

The distinguishing property is **stateful enforcement in the fabric**. The ASIC-based fabrics of the previous volumes (ACI, Arista MSS) enforce largely **stateless** group/contract ACLs; the CX 10000's DPU tracks **connection state** — so return traffic is permitted automatically, unsolicited or invalid packets are dropped, and you get firewall-grade behavior at switch scale (millions of connections). Because the enforcement lives in DPU hardware with no free emulator, this volume is **design-leaning two-track**:

- **Track 1 — the real product (design level).** How stateful segmentation policies, security policies, and telemetry are configured on the CX 10000 via PSM/Fabric Composer, described accurately.
- **Track 2 — a buildable stateful model.** One Linux host whose **nftables connection tracking** reproduces exactly the stateful behavior the DPU accelerates — default-deny, stateful permits, automatic return traffic, and dropped invalid flows — the concept made concrete (the DPU is what makes this run at line rate for a whole rack).

### The moving parts

| Part | What it is | CX 10000 construct |
|:---|:---|:---|
| **Distributed services switch** | ToR switch with an embedded DPU | Aruba CX 10000 |
| **Stateful firewall** | Connection-tracked east-west policy in the DPU | Pensando stateful services |
| **Security policy** | Default-deny with stateful permits | PSM policy |
| **Connection tracking** | Per-flow state; return traffic auto-permitted | DPU conntrack |
| **PSM / Fabric Composer** | Central policy + telemetry | Pensando PSM / Aruba FC |

Two ideas carry the volume:

- **Stateful, in the fabric.** The DPU firewalls east-west with connection tracking at the ToR — no hairpin, firewall-grade behavior.
- **State is the difference.** Return traffic is permitted by state, not by a mirror-image rule; invalid/unsolicited packets are dropped.

### Topology

```text
                         +---------------------------+
                         |  PSM / Aruba Fabric       |  stateful policy +
                         |  Composer                 |  per-flow telemetry
                         +-------------+-------------+
                                       | policy
              +------------ CX 10000 ToR (embedded DPU) ------------+
              |     stateful firewall east-west, line rate         |
              |  web .10   db .20 :5432   hmi .30   plc .40         |
              +----------------------------------------------------+
   stateful permit:  web -> db:5432 (return traffic auto-permitted)
   denied:  hmi -> db (no permit) , any unsolicited/invalid packet
```

### The policy plan

| Endpoint | Address | Stateful permit |
|:---|:---|:---|
| web | 10.130.1.10 | → db:5432 (NEW; return ESTABLISHED auto) |
| db | 10.130.2.20 | (receives from web; replies auto-permitted) |
| hmi | 10.130.3.30 | → plc:502 |
| plc | 10.130.4.40 | (receives from hmi) |

Only the two flows are permitted (default-deny); return traffic is permitted by **state**, and any unsolicited or invalid packet is dropped.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Design-level steps on the CX 10000 / PSM |
| **Track 2** | Buildable steps on the native stateful (conntrack) model |
| `psm>` | PSM / Fabric Composer action (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Rollback**.

## Summary and Completion Checklist

- [ ] DPU-offloaded stateful firewalling at the ToR understood.
- [ ] Stateful vs stateless enforcement internalized.
- [ ] Track chosen (Track 2 is the buildable one).
- [ ] Topology and policy plan read.
