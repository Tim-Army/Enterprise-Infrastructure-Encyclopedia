# Chapter 01: Lab Overview and Topology

![Lab topology: five devices on one flat VLAN 10.100.1.0/24, each collapsed into a network of one whose only neighbor is the Airgap enforcement point — no direct L2 path between any two devices. The enforcement point denies east-west by default, permits only web-to-db:5432, and offers a ransomware kill switch; an infected victim is isolated and cannot spread.](../../../diagrams/volume-116-zscaler-airgap-lab/chapter-01-lab-topology.svg)

*Figure 1-1. Airgap makes every device a network of one: on a single VLAN with no agents and no IP changes, all east-west is brokered by the enforcement point, only the sanctioned web-to-db flow is permitted, and an infected host has no lateral path — with a kill switch to sever everything on demand.*

## Learning Objectives

- State what this lab builds and how Airgap (now Zscaler) segments **agentlessly** by controlling the network layer.
- Understand the **network-of-one** model, the **ransomware kill switch**, and cloud-delivered access via the Zero Trust Exchange.
- Understand the two tracks — a design view of the Zscaler/Airgap product, and a buildable agentless-isolation model.
- Read the lab topology and the isolation plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab modeled on **Airgap Networks** (acquired by **Zscaler**), whose approach is unlike any earlier volume: it segments **without agents and without changing VLANs** by taking control of the **network layer itself**. Airgap makes every device its own microsegment — a **network of one** — by controlling **ARP/DHCP** so that no device can see or reach any other device directly at Layer 2. All east-west traffic is forced through an **enforcement point** that applies zero-trust policy, so two machines on the *same subnet* cannot talk unless policy allows it. Because there is no lateral path by default, ransomware cannot spread — and a single **kill switch** can sever all east-west instantly during an incident. Zscaler pairs this with the **Zero Trust Exchange** for cloud-delivered, identity-based **access** (ZTNA) from users to applications.

The theme is **agentless isolation as the default**: you do not install anything on the endpoints or re-architect the network; you insert a control that makes every device an island and brokers every conversation. Zscaler/Airgap is a commercial platform, so this volume is **two-track**:

- **Track 1 — the real product (design level).** How the Airgap enforcement point controls ARP/DHCP to isolate devices, how policy and the kill switch are managed, and how the Zero Trust Exchange delivers access, described accurately.
- **Track 2 — a buildable agentless-isolation model.** One Linux host where each device is reconfigured into a **network of one** (a `/32` island whose only route is the enforcer), and the enforcer applies default-deny east-west policy plus a kill switch — a working reproduction of agentless microsegmentation.

### The moving parts

| Part | What it is | Airgap/Zscaler construct |
|:---|:---|:---|
| **Network of one** | Each device isolated so it has no direct L2 peers | Airgap host isolation |
| **Enforcement point** | The broker all east-west traffic must pass | Airgap gateway |
| **Zero-trust policy** | Default-deny east-west; allow only sanctioned flows | Airgap policy |
| **Ransomware kill switch** | Instantly sever all east-west | Airgap kill switch |
| **Zero Trust Exchange** | Cloud-delivered identity-based access (ZTNA) | Zscaler ZTE |

Two ideas carry the volume:

- **No lateral path by default.** Isolation is the baseline; connectivity is the exception, granted by policy.
- **Agentless and VLAN-preserving.** Nothing is installed on endpoints and no subnets change — the control is at the network layer.

### Topology

```text
   Flat VLAN 10.100.1.0/24 — but every device is a "network of one"
   +----------------------------------------------------------------+
   |  web .10    db .20 :5432    hmi .30    plc .40    victim .50    |
   |    \          |               |          |          /           |
   |     \_________|_____ enforcement point (.1) _______/            |
   |         all east-west brokered here; no direct L2 path          |
   +----------------------------------------------------------------+
   default:  no device can reach any other (isolated)
   allowed:  web -> db:5432  (only sanctioned flow)
   incident: kill switch severs ALL east-west instantly
```

Even though every device shares one VLAN, none can reach another directly — all traffic is brokered by the enforcement point, which permits only sanctioned flows.

### The isolation and policy plan

| Device | Address | Default reach | Sanctioned flow |
|:---|:---|:---|:---|
| web | 10.100.1.10 | none (isolated) | → db:5432 |
| db | 10.100.1.20 | none (isolated) | (receives from web) |
| hmi | 10.100.1.30 | none (isolated) | (out-of-band mgmt only) |
| plc | 10.100.1.40 | none (isolated) | (receives nothing east-west) |
| victim | 10.100.1.50 | none (isolated) | none — ransomware cannot spread |

The only permitted east-west flow is `web → db:5432`; every other pair is isolated by default, so a compromised `victim` has nowhere to go.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Design-level steps on real Zscaler/Airgap |
| **Track 2** | Buildable steps on the native agentless-isolation model |
| `airgap>` | Airgap/Zscaler action (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Rollback**.

## Summary and Completion Checklist

- [ ] Agentless network-of-one isolation understood.
- [ ] The kill switch and Zero Trust Exchange roles internalized.
- [ ] Track chosen (Track 2 is the buildable one).
- [ ] Topology and isolation plan read.
