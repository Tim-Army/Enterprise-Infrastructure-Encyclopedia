# Chapter 01: Lab Overview and Topology

![Lab topology: a FortiGate Internal Segmentation Firewall segmenting a four-zone estate — web (zone APP), db (zone DB, :5432), hmi (zone MGMT), plc (zone OT, :502). Policies permit APP-to-DB PGSQL and MGMT-to-OT MODBUS; the implicit deny drops the MGMT-to-DB lateral flow. The OT tier is isolated in its own VDOM, crossed only by a scoped inter-VDOM link.](../../../diagrams/volume-109-fortinet-isfw-vdom-lab/chapter-01-lab-topology.svg)

*Figure 1-1. Fortinet segments east-west with an internal firewall (ISFW): zone policies permit only the two legitimate flows and the implicit deny stops the operator's lateral path to the database, while VDOMs isolate the OT tier so IT-to-OT crosses only a tightly scoped inter-VDOM link.*

## Learning Objectives

- State what this lab builds and how a Fortinet **Internal Segmentation Firewall (ISFW)** segments east-west traffic.
- Understand **VDOMs** as hard partitions of one FortiGate into independent virtual firewalls.
- Understand the two tracks — a real FortiGate-VM, and a native Linux/nftables model.
- Read the lab topology, the zone plan, and the VDOM plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab on **Fortinet FortiGate**, using two of Fortinet's segmentation mechanisms:

- The **Internal Segmentation Firewall (ISFW)** — a FortiGate placed *inside* the network (not just at the perimeter) so that east-west traffic between internal segments must pass a full firewall policy, with FortiOS application and identity awareness.
- **Virtual Domains (VDOMs)** — partitions that split one FortiGate into several independent virtual firewalls, each with its own interfaces, policies, and routing. VDOMs give hard multi-tenant separation: traffic crosses between VDOMs only over an explicit inter-VDOM link governed by policy.

The lab segments a four-tier estate (web/db/hmi/plc) first with ISFW zone-to-zone firewall policies, then demonstrates hardening the separation with VDOMs. FortiOS is commercial, so this volume is **two-track**:

- **Track 1 — the real thing.** A **FortiGate-VM** evaluation running FortiOS: real interfaces, zones, address objects, firewall policies, and VDOMs.
- **Track 2 — the native model.** One Linux host with **nftables** whose zones and ordered policies reproduce the FortiOS model with no Fortinet software.

### The moving parts

| Part | What it is | FortiOS construct |
|:---|:---|:---|
| **Interface / zone** | A segment, or a named group of interfaces | `config system interface` / `config system zone` |
| **Address object** | A named host/subnet used in policy | `config firewall address` |
| **Service** | The port/protocol a policy matches | `config firewall service custom` / predefined |
| **Firewall policy** | Ordered rule: srcintf/dstintf, srcaddr/dstaddr, service, action | `config firewall policy` |
| **VDOM** | An independent virtual firewall inside one FortiGate | `config vdom` |

Two ideas carry the volume:

- **Implicit deny at the end.** A FortiGate applies an implicit deny after the last policy, so anything not explicitly permitted is dropped — default-deny east-west once ISFW is in the path.
- **Policy by object, not just address; VDOM for hard separation.** Policies reference named address objects and services; VDOMs isolate whole tenants. Both keep policy meaningful as the estate changes.

### Topology

```text
                    +-------------------------+
                    |  FortiGate (ISFW)       |  firewall policies (+ VDOMs)
                    |  FortiOS                |  implicit deny at the end
                    +--+-----+------+-----+---+
           zone APP _/    |      |      \_ zone OT
            +-----+  zone DB   zone MGMT   +-----+
            | web |  +----+     +-----+    | plc |
            +-----+  | db |     | hmi |    +-----+
                     +----+     +-----+
   legit:  APP->DB tcp/5432 ,  MGMT->OT tcp/502
   denied: MGMT->DB (lateral) ,  all other east-west
```

### The zone and VDOM plan

**Licensed FortiGate — four physical data ports:**

| Endpoint | Interface | Zone | VDOM (Ch 06) | Address |
|:---|:---|:---|:---|:---|
| web | port2 | `APP` | `IT` | 10.30.1.10 |
| db | port3 | `DB` | `IT` | 10.30.2.10 |
| hmi | port4 | `MGMT` | `IT` | 10.30.3.10 |
| plc | port5 | `OT` | `OT` | 10.30.4.10 |

**Evaluation FortiGate — four VLAN subinterfaces on one trunk port (`port2`):**

| Endpoint | Interface | VLAN | Zone | VDOM (Ch 06) | Address |
|:---|:---|:---|:---|:---|:---|
| web | v2001 | 2001 | `APP` | `IT` | 10.30.1.10 |
| db | v2002 | 2002 | `DB` | `IT` | 10.30.2.10 |
| hmi | v2003 | 2003 | `MGMT` | `IT` | 10.30.3.10 |
| plc | v2004 | 2004 | `OT` | `OT` | 10.30.4.10 |

The zones, VDOM split, and addresses are identical either way — only the interface each endpoint lands on changes. In Chapter 07 the OT tier moves to its own VDOM, so IT↔OT traffic must cross an explicit inter-VDOM link — the hardest separation FortiGate offers short of separate appliances.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Steps on real FortiGate-VM / FortiOS |
| **Track 2** | Steps on the native Linux/nftables model |
| `FGT #` | FortiOS CLI (orientation only; type the command shown) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Cleanup**.

## Summary and Completion Checklist

- [ ] The ISFW and VDOM concepts understood.
- [ ] Implicit-deny and policy-by-object internalized.
- [ ] Track chosen (or both).
- [ ] Topology, zone plan, and VDOM plan read.
