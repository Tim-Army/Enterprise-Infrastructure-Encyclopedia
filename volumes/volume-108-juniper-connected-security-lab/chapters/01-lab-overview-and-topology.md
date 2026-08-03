# Chapter 01: Lab Overview and Topology

![Lab topology: a vSRX firewall segmenting a four-zone estate — web (zone APP), db (zone DB, :5432), hmi (zone MGMT), plc (zone OT, :502). Security policies permit APP-to-DB:5432 and MGMT-to-OT:502; the SRX default inter-zone deny drops the MGMT-to-DB lateral flow. A dynamic address group can quarantine a host by membership.](../../../diagrams/volume-108-juniper-connected-security-lab/chapter-01-lab-topology.svg)

*Figure 1-1. Juniper Connected Security segments with a stateful firewall: zones and policies permit only the two legitimate flows, the default inter-zone deny stops the operator's lateral path to the database, and a dynamic address group adds reactive containment.*

## Learning Objectives

- State what this lab builds and how Juniper Connected Security segments with **SRX zones and policies** plus **dynamic enforcement**.
- Distinguish this stateful-firewall model from the tag-fabric model of the previous volume.
- Understand the two tracks — a real vSRX, and a native Linux/nftables zone model.
- Read the lab topology and the zone plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab on **Juniper Connected Security** — Juniper's model in which the **SRX Series firewall** is the enforcement point, traffic is organized into **security zones**, and **security policies** decide which zone (and which address group and application) may talk to which. "Connected Security" is the larger idea that policy is driven centrally (by **Security Director** and **Policy Enforcer**) and can react to threat intelligence — for example, quarantining an infected host by adding it to a **dynamic address group** that a policy denies. This lab builds the enforcement core you can operate by hand.

Where the previous volume ([Volume CVII](../../volume-107-cisco-ise-trustsec-lab/README.md)) segmented by carrying a **group tag** in the fabric, this volume segments with a **stateful firewall**: zones and policies with address and application granularity, plus dynamic groups for reactive containment. The two are complementary models of the same goal, and worth contrasting directly.

SRX/Junos is commercial, so this volume is **two-track**:

- **Track 1 — the real thing.** A **vSRX 3.0** evaluation VM enforcing real Junos security zones, policies, address books, and dynamic address groups; optionally driven by Security Director.
- **Track 2 — the native model.** One Linux host with **nftables** whose zones (named sets of interfaces/addresses) and zone-to-zone rules reproduce the SRX policy model with no Juniper software.

### The moving parts

| Part | What it is | Junos construct |
|:---|:---|:---|
| **Security zone** | A named grouping of interfaces/segments | `security zones security-zone <name>` |
| **Address book** | Named addresses and address sets used in policies | `security address-book` |
| **Security policy** | An ordered rule: from-zone/to-zone, source/dest/application, permit/deny | `security policies from-zone A to-zone B` |
| **Application** | The service (port/protocol) a policy matches | `applications` / junos-defaults |
| **Dynamic address group** | A group whose members are fed dynamically (feeds/quarantine) | `security dynamic-address` |

Two ideas carry the volume:

- **Default-deny between zones.** SRX denies inter-zone traffic unless a policy permits it — the posture microsegmentation wants, out of the box.
- **Group and application, not just IP.** Policies match address *sets* and *applications*, and dynamic groups let identity change without editing rules — the same lesson the series teaches, in Junos form.

### Topology

```text
                       +---------------------+
                       |  vSRX (firewall)    |  zones + policies + dyn-address
                       |  Security Director  |  (optional central mgmt)
                       +--+----+-----+----+--+
             zone APP __/    |     |     \__ zone OT
              +-----+  zone DB   zone MGMT  +-----+
              | web |   +----+    +-----+   | plc |
              +-----+   | db |    | hmi |   +-----+
                        +----+    +-----+
   legit:  APP->DB tcp/5432 ,  MGMT->OT tcp/502
   denied: MGMT->DB (lateral) ,  all other inter-zone
```

### The zone plan

| Endpoint | Zone | Address | Legit reach |
|:---|:---|:---|:---|
| web | `APP` | 10.20.1.10 | → DB:5432 |
| db | `DB` | 10.20.2.10 | (receives from APP) |
| hmi | `MGMT` | 10.20.3.10 | → OT:502 |
| plc | `OT` | 10.20.4.10 | (receives from MGMT) |

The `MGMT → DB` flow is the lateral movement to deny; every other inter-zone flow is denied by default.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Steps on real vSRX / Junos |
| **Track 2** | Steps on the native Linux/nftables zone model |
| `srx#`, `[edit]` | Junos operational / configuration mode (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Cleanup**.

## Summary and Completion Checklist

- [ ] The zone/policy/address-book/dynamic-group model understood.
- [ ] The contrast with tag-fabric segmentation clear.
- [ ] Track chosen (or both).
- [ ] Topology and zone plan read.
