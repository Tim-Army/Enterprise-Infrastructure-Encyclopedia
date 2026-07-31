# Chapter 01: Lab Overview and Topology

![Lab topology: all four workloads (web, db :5432, hmi, plc :502) on one subnet 10.50.1.0/24. NSX Manager distributes tag-based group rules to every VM's vNIC, where the DFW enforces. It permits Web-to-Database:5432 and Operators-to-OT:502 with a zero-trust Drop default, denying the hmi-to-db lateral flow at db's own vNIC even though the two are same-subnet peers with no gateway between them.](../../../diagrams/volume-111-vmware-nsx-dfw-lab/chapter-01-lab-topology.svg)

*Figure 1-1. NSX enforces the distributed firewall at each vNIC: the operator's lateral path to the database is denied at the database's own interface, filtering same-subnet east-west traffic that a centralized firewall never sees — the defining microsegmentation advantage.*

## Learning Objectives

- State what this lab builds and how the NSX **Distributed Firewall (DFW)** enforces at every vNIC.
- Understand why distributed enforcement filters **same-subnet** traffic no gateway would see.
- Understand the two tracks — a real NSX Manager + ESXi, and a native per-workload nftables model.
- Read the lab topology, the tag plan, and the group plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab on the **VMware NSX Distributed Firewall (DFW)** — the model that runs firewall enforcement **in the hypervisor kernel at every virtual machine's vNIC**. Because the rule is applied at the workload's own virtual interface, DFW filters traffic **before it ever reaches the wire** — including traffic between two VMs on the **same subnet and the same host**, which a centralized gateway or ISFW never sees. This is the property that makes NSX the archetypal microsegmentation platform, and it is the deliberate contrast with the previous four fabric/firewall volumes, whose honest boundary was exactly that same-subnet east-west traffic.

Policy is written against **NSX groups** whose membership is **dynamic** — driven by **security tags**, VM name, or OS — so a rule reads "Web may reach Database" and every tagged VM is covered automatically. NSX is commercial, so this volume is **two-track**:

- **Track 1 — the real thing.** An **NSX Manager** and an **ESXi** transport node (evaluation), with real security tags, groups, a DFW rulebase, and a zero-trust default rule, driven through the NSX UI and the Policy API.
- **Track 2 — the native model.** One Linux host where each workload is a namespace enforcing **its own** nftables ruleset — a faithful model of *distributed* enforcement at the vNIC, including same-subnet filtering with no gateway in the path.

### The moving parts

| Part | What it is | NSX construct |
|:---|:---|:---|
| **Security tag** | A label applied to a VM | Inventory tag |
| **Group** | A dynamic set of VMs by tag/name/OS | NSX group with membership criteria |
| **Service** | The port/protocol a rule matches | NSX service |
| **DFW rule** | Source group, destination group, service, action, **Applied To** | Distributed firewall policy/rule |
| **Default rule** | The final catch-all, set to Drop for zero-trust | DFW default layer-3 rule |

Two ideas carry the volume:

- **Enforce at the vNIC, not at a chokepoint.** DFW filters east-west at each workload, so there is no hairpin to a firewall and no blind spot for same-subnet traffic.
- **Group by tag; membership is dynamic.** A rule against the `Database` group covers any VM tagged `role=db` — new VMs included automatically. The series' lesson, in NSX form.

### Topology — one subnet, on purpose

```text
   One L2 segment 10.50.1.0/24  (all four VMs, distributed enforcement at each vNIC)
   +----------------------------------------------------------------+
   |  [vNIC-DFW] web 10.50.1.10     [vNIC-DFW] db 10.50.1.20 :5432   |
   |       tag role=web                 tag role=db                  |
   |            \___ 5432 allow ___/                                 |
   |  [vNIC-DFW] hmi 10.50.1.30     [vNIC-DFW] plc 10.50.1.40 :502   |
   |       tag role=hmi                 tag role=plc                 |
   |            \___ 502 allow ___/     X  hmi->db denied            |
   +----------------------------------------------------------------+
   Every arrow is filtered at the destination vNIC — no gateway between peers.
```

Putting all four workloads on **one subnet** is deliberate: it demonstrates that DFW denies `hmi → db` even though the two VMs are on the same segment with no router between them — the case the centralized models in Volumes CVII–CX could not cover.

### The tag and group plan

| Endpoint | Address | Security tag | Group |
|:---|:---|:---|:---|
| web | 10.50.1.10 | `role=web` | `Web` |
| db | 10.50.1.20 | `role=db` | `Database` |
| hmi | 10.50.1.30 | `role=hmi` | `Operators` |
| plc | 10.50.1.40 | `role=plc` | `OT` |

The DFW permits `Web → Database` (PostgreSQL) and `Operators → OT` (Modbus); the default rule drops everything else, including `Operators → Database`.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Steps on real NSX Manager + ESXi (UI / Policy API) |
| **Track 2** | Steps on the native per-namespace nftables model |
| `nsx>` | NSX Policy API call (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Cleanup**.

## Summary and Completion Checklist

- [ ] The distributed, at-the-vNIC enforcement model understood.
- [ ] Why same-subnet traffic is filtered (and why that matters) internalized.
- [ ] Track chosen (or both).
- [ ] Topology, tag plan, and group plan read.
