# Chapter 01: Lab Overview and Topology

![Lab topology: CloudVision manages an Arista EOS fabric enforcing group policy at line rate. Endpoints are in security groups — web (SG-Web), db (SG-DB, :5432), hmi (SG-Mgmt), plc (SG-OT, :502). MSS-Group permits only SG-Web-to-SG-DB:5432 and SG-Mgmt-to-SG-OT:502, denying the rest; MSS macro redirects the SG-Web-to-SG-DB flow through a firewall for inspection.](../../../diagrams/volume-118-arista-mss-group-lab/chapter-01-lab-topology.svg)

*Figure 1-1. Arista segments by group in the fabric: MSS-Group permits only the two group flows at line rate and denies the operator's lateral path by default, while MSS macro-segmentation redirects the web-to-db flow through an inserted firewall for inspection without re-cabling — micro for the many, macro for the few.*

## Learning Objectives

- State what this lab builds and how Arista segments with **group-based policy enforced in the switch**.
- Distinguish **MSS-Group** (micro-segmentation by group) from **MSS** (macro-segmentation via firewall redirect).
- Understand the two tracks — an EOS/CloudVision design view, and a buildable group-policy model.
- Read the lab topology and the group/policy plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab modeled on **Arista's Macro-Segmentation Service (MSS)** and **MSS-Group**, implemented on **EOS** switches and managed by **CloudVision**. Arista's approach enforces **group-based policy in the switching silicon at line rate**: endpoints are assigned to **security groups**, and a policy states which group may talk to which (with L4 rules), enforced in the fabric with no hairpin. There are two flavors:

- **MSS-Group** — **micro-segmentation**: group-to-group policy enforced directly in the switch ASIC, default-deny between groups.
- **MSS (macro-segmentation)** — **service insertion**: rather than permit or drop inter-group traffic outright, the fabric **redirects** it through an inserted **firewall** for deeper inspection, then returns it — segmentation that leverages an existing firewall without re-cabling.

The theme is **group policy in the fabric, plus optional firewall redirect**: segment at line rate by group, and steer the flows that need inspection through a firewall. Arista EOS runs as **cEOS/vEOS** for labs, but MSS-Group's line-rate enforcement lives in hardware, so this volume is **two-track**:

- **Track 1 — the real product (design level).** How security groups, MSS-Group policy, and MSS firewall-redirect are configured in EOS and CloudVision, described accurately.
- **Track 2 — a buildable group-policy model.** One Linux host where security groups are nftables sets, group policy is allow rules with a default deny, and macro-segmentation redirects an inter-group flow through an inspection point — a working reproduction of group-based fabric segmentation.

### The moving parts

| Part | What it is | Arista construct |
|:---|:---|:---|
| **Security group** | A group of endpoints sharing policy | MSS security group |
| **Group policy** | Which group may reach which, with L4 rules | MSS-Group policy |
| **Line-rate enforcement** | Policy applied in the switch ASIC, no hairpin | EOS hardware |
| **Firewall redirect** | Steer inter-group traffic through a firewall | MSS macro-segmentation |
| **CloudVision** | Central management/telemetry | Arista CloudVision |

Two ideas carry the volume:

- **Group policy at line rate.** Segment by group directly in the fabric, with no performance penalty and no traffic hairpin to a firewall.
- **Redirect when you need inspection.** MSS macro inserts a firewall into the path for the flows that warrant it, without re-architecting.

### Topology

```text
                         +---------------------------+
                         |  CloudVision              |  security groups +
                         |  Arista EOS fabric        |  group policy (MSS)
                         +-------------+-------------+
                                       | policy (line-rate in ASIC)
   SG-Web            SG-DB             SG-Mgmt          SG-OT
   +-----+  policy   +----+            +-----+  policy  +-----+
   | web | =5432==>  | db |            | hmi | =502===> | plc |
   +-----+           +----+            +-----+          +-----+
   default between groups: DENY
   MSS macro: redirect SG-Web -> SG-DB through a firewall for inspection
```

### The group and policy plan

| Endpoint | Security group | Address | Policy |
|:---|:---|:---|:---|
| web | `SG-Web` | 10.120.1.10 | → SG-DB:5432 (via firewall redirect) |
| db | `SG-DB` | 10.120.2.20 | (receives from SG-Web) |
| hmi | `SG-Mgmt` | 10.120.3.30 | → SG-OT:502 |
| plc | `SG-OT` | 10.120.4.40 | (receives from SG-Mgmt) |

Only the two group flows are permitted; every other group pair is denied. The `SG-Web → SG-DB` flow is additionally redirected through a firewall to demonstrate MSS macro-segmentation.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Design-level steps on EOS / CloudVision |
| **Track 2** | Buildable steps on the native group-policy model |
| `eos#` | EOS CLI (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Cleanup**.

## Summary and Completion Checklist

- [ ] Group-based line-rate policy understood.
- [ ] MSS-Group (micro) vs MSS (macro firewall-redirect) distinguished.
- [ ] Track chosen (Track 2 is the buildable one).
- [ ] Topology and group/policy plan read.
