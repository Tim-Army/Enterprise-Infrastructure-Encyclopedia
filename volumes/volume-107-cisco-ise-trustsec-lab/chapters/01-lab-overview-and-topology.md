# Chapter 01: Lab Overview and Topology

![Lab topology: Cisco ISE as the policy engine defining SGTs and the SGACL egress matrix, an IOS-XE enforcer that downloads the matrix over RADIUS and learns IP-SGT bindings over SXP, and four tagged endpoints — web (WEB=10), db (DB=20, :5432), hmi (HMI=30), plc (PLC=40, :502). The matrix permits WEB-to-DB:5432 and HMI-to-PLC:502 and denies the HMI-to-DB lateral flow.](../../../diagrams/volume-107-cisco-ise-trustsec-lab/chapter-01-lab-topology.svg)

*Figure 1-1. TrustSec segments by group tag, not IP: ISE holds the policy, the IOS-XE enforcer applies the SGACL matrix on egress, and the operator's lateral path to the database is denied by the matrix default while the two legitimate flows stay open.*

## Learning Objectives

- State what this lab builds and how Cisco TrustSec segments a network by **group tag**, not by IP.
- Read the four moving parts: **SGT**, **SGACL**, the **egress policy matrix**, and **SXP**.
- Understand the two tracks — a real Cisco ISE + IOS-XE fabric, and a native Linux model that teaches the same idea with no Cisco kit.
- Read the lab topology and the security-group tag plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab built on **Cisco TrustSec** — the fabric-based approach in which every packet carries a **Security Group Tag (SGT)** describing *what the sender is* (web server, database, operator), and the network enforces a matrix of **Security Group ACLs (SGACLs)** that say which tag may talk to which. The policy brain is **Cisco Identity Services Engine (ISE)**; the enforcers are the switches and routers. Because the policy is written in terms of groups, it is independent of IP addressing and VLANs — the defining property that separates fabric microsegmentation from traditional ACLs.

TrustSec is a commercial, largely hardware-assisted technology, so this volume is **two-track**, exactly like the other build-it-yourself labs in this series:

- **Track 1 — the real thing.** Cisco ISE (90-day evaluation VM) as the policy engine and an IOS-XE device (a Catalyst 9000v in Cisco Modeling Labs, or a physical Catalyst 9300) as the enforcement point. You author real SGTs and SGACLs, push them with SXP, and read `show cts role-based` counters.
- **Track 2 — the native model.** A single Linux host with **nftables** that reproduces the *semantics* — an IP-to-SGT binding table (what SXP distributes) and a tag-to-tag rule matrix (what an SGACL is) — so the tag-based-segmentation muscle memory is available to anyone with two VMs and no Cisco hardware.

Do Track 2 to understand the model cheaply; do Track 1 to operate the product. The chapters run both side by side.

### The four moving parts

| Part | What it is | Where it lives |
|:---|:---|:---|
| **SGT** | A 16-bit tag naming the sender's group (e.g. WEB=10, DB=20) | Assigned by ISE; carried in the packet (inline) or in a binding table |
| **SGACL** | An ACL keyed on *(source SGT, destination SGT)* rather than IP | Authored in ISE, downloaded to the enforcer |
| **Egress policy matrix** | The grid of SGACLs — rows are source SGTs, columns destination SGTs | ISE → Work Centers → TrustSec → Policy |
| **SXP** | SGT Exchange Protocol — distributes IP-to-SGT bindings to devices that cannot tag inline | Between ISE/NADs |

Two ideas carry the whole volume:

- **Enforce on the destination (egress).** TrustSec enforces where traffic *leaves* the fabric toward the destination group, so the enforcer needs the destination SGT locally plus the source SGT from the packet or a binding.
- **Group, not address.** `WEB → DB permit 5432` keeps working when servers scale, move VLANs, or re-address. That is the same lesson every volume in this series teaches, expressed in Cisco's fabric.

### Topology

```text
                 +-------------------+
                 |  Cisco ISE (VM)   |  policy: SGTs, SGACL matrix, SXP
                 |  10.10.0.10       |
                 +----+----------+---+
                      | RADIUS    | SXP (IP-SGT bindings)
                      |           |
                 +----+-----------+----+
                 | IOS-XE enforcer NAD |  cts role-based enforcement
                 | (Cat9000v / Cat9300)|  downloads SGACLs, tags/enforces
                 +--+-----+------+-----+
        WEB=10 __/     |      |      \__ PLC=40
             +-----+ DB=20  HMI=30  +-----+
             | web |  +----+ +-----+| plc |
             +-----+  | db | | hmi |+-----+
                      +----+ +-----+
   legit:  WEB->DB tcp/5432 ,  HMI->PLC tcp/502
   denied: HMI->DB (lateral) ,  everything else east-west
```

### The security-group tag plan

| Endpoint | Role | SGT name | SGT value |
|:---|:---|:---|:---|
| web | Application front end | `WEB` | 10 |
| db | PostgreSQL database | `DB` | 20 |
| hmi | Operator workstation | `HMI` | 30 |
| plc | OT controller (Modbus) | `PLC` | 40 |
| — | Unclassified | `Unknown` | 0 |

### Time and effort

| Chapters | Content | Track 1 | Track 2 |
|:---|:---|:---|:---|
| 02–04 | Bring-up, endpoints, SGT assignment | 2–3 h (ISE boot is slow) | 45 min |
| 05–07 | Flat network, SGACL matrix, enforcement | 2 h | 1 h |
| 08–09 | Inline tagging, scale, ops, teardown | 1 h | 30 min |

ISE takes 30–45 minutes to boot the first time; plan around it.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Steps on real Cisco ISE + IOS-XE |
| **Track 2** | Steps on the native Linux/nftables model |
| `ise/#`, `nad#` | ISE admin CLI / IOS-XE privileged prompt (shown for orientation; you type the command after it) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Rollback**.

## Summary and Completion Checklist

- [ ] The SGT / SGACL / matrix / SXP model understood.
- [ ] Egress enforcement and group-not-address internalized.
- [ ] Track chosen (or both).
- [ ] Topology and SGT plan read.
