# Chapter 01: Lab Overview and Topology

![Lab topology: the APIC drives a Nexus 9000 fabric with an application-centric whitelist. Endpoints live in EPGs — web (EPG-Web), db (EPG-DB, :5432), hmi (EPG-Mgmt), plc (EPG-OT, :502). Contracts permit only Web-to-DB:5432 and Mgmt-to-OT:502; every other EPG pair, including Mgmt-to-DB, is denied by the whitelist default. uSeg micro-EPGs reclassify a compromised endpoint into a deny-all quarantine by attribute.](../../../diagrams/volume-117-cisco-aci-lab/chapter-01-lab-topology.svg)

*Figure 1-1. Cisco ACI segments by application group: traffic between EPGs is denied unless a contract permits it, so only the two contracted flows pass and the operator's uncontracted path to the database is denied by the whitelist default — with uSeg micro-EPGs for attribute-based quarantine and intra-EPG isolation for peers within a group.*

## Learning Objectives

- State what this lab builds and how Cisco ACI segments with **application-centric whitelist** policy.
- Understand **EPGs**, **contracts**, the default-deny between groups, and **uSeg (micro-EPGs)**.
- Understand the two tracks — a design/APIC view of a real ACI fabric, and a buildable EPG/contract model.
- Read the lab topology and the EPG/contract plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab modeled on **Cisco ACI (Application Centric Infrastructure)** — the Nexus 9000 spine-leaf fabric controlled by the **APIC**. ACI's model is **application-centric and whitelist by default**: endpoints are placed in **Endpoint Groups (EPGs)**, and traffic between two EPGs is **denied unless a contract permits it**. A **contract** names the allowed protocols/ports (its **filters**); one EPG **provides** the contract and another **consumes** it. For finer control, **uSeg EPGs (micro-EPGs)** classify endpoints into groups by *attribute* (IP, MAC, VM property) rather than by port, and **intra-EPG isolation** can deny traffic even between members of the same EPG. The policy is enforced in the fabric ASICs.

The theme is **whitelist between application groups**: nothing talks unless a contract says so, and the grouping is by application role, not subnet. ACI needs Nexus 9000 hardware and an APIC (the ACI Simulator models the control plane but does not forward data-plane traffic), so this volume is **two-track**:

- **Track 1 — the real product (design level).** How tenants, bridge domains, EPGs, contracts, filters, and uSeg EPGs are configured on the APIC (GUI/REST), described accurately; the data-plane result is what Track 2 makes concrete.
- **Track 2 — a buildable EPG/contract model.** One Linux host where EPGs are nftables groups, contracts are allow rules between them, the default between groups is deny, and uSeg reclassifies an endpoint by attribute — a working reproduction of application-centric whitelist segmentation.

### The moving parts

| Part | What it is | ACI construct |
|:---|:---|:---|
| **EPG** | A group of endpoints sharing policy | Endpoint Group |
| **Contract** | The permitted traffic between two EPGs | Contract (+ subject/filter) |
| **Provide / consume** | Which EPG offers vs uses a contract | Contract relationships |
| **Default between EPGs** | Deny unless a contract permits | Whitelist model |
| **uSeg EPG** | Attribute-based micro-segmentation group | Micro-EPG |

Two ideas carry the volume:

- **Whitelist by contract.** Between EPGs, deny is the default; a contract is an explicit exception naming the exact ports.
- **Group by application role, refine by attribute.** EPGs group by role; uSeg refines by attribute for micro-segmentation and intra-EPG isolation.

### Topology

```text
                         +---------------------------+
                         |  APIC (controller)        |  tenants, EPGs,
                         |  Nexus 9000 spine-leaf    |  contracts, uSeg
                         +-------------+-------------+
                                       | policy (fabric-enforced)
   EPG-Web            EPG-DB            EPG-Mgmt          EPG-OT
   +-----+  contract  +----+           +-----+  contract +-----+
   | web | =web-db=>  | db |           | hmi | =mgmt-ot=>| plc |
   +-----+   5432     +----+           +-----+   502     +-----+
   default between EPGs: DENY (no contract) — e.g. Mgmt -> DB blocked
   uSeg: reclassify a compromised endpoint into EPG-Quarantine (deny all)
```

### The EPG and contract plan

| Endpoint | EPG | Address | Contract |
|:---|:---|:---|:---|
| web | `EPG-Web` | 10.110.1.10 | consumes `web-db` |
| db | `EPG-DB` | 10.110.2.20 | provides `web-db` (tcp 5432) |
| hmi | `EPG-Mgmt` | 10.110.3.30 | consumes `mgmt-ot` |
| plc | `EPG-OT` | 10.110.4.40 | provides `mgmt-ot` (tcp 502) |

Only the two contracted flows are permitted; every other EPG pair (including `EPG-Mgmt → EPG-DB`) is denied by the whitelist default. (ACI additionally enforces between EPGs that share a bridge domain/subnet; this model maps each EPG to its own subnet for clarity, and the same contract logic applies.)

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Design-level steps on a real APIC / ACI Simulator |
| **Track 2** | Buildable steps on the native EPG/contract model |
| `apic>` | APIC GUI/REST action (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Cleanup**.

## Summary and Completion Checklist

- [ ] The EPG/contract whitelist model understood.
- [ ] Default-deny between EPGs and uSeg micro-segmentation internalized.
- [ ] Track chosen (Track 2 is the buildable one).
- [ ] Topology and EPG/contract plan read.
