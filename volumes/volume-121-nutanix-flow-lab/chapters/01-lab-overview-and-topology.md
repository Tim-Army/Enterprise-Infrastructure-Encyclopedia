# Chapter 01: Lab Overview and Topology

![Lab topology: four VMs on one AHV virtual switch, microsegmented by Nutanix Flow Network Security. Prism Central holds category-driven policy — an application policy permits web-to-db:5432 and hmi-to-plc:502, an isolation policy separates Environment:corp from Environment:ot, and a quarantine policy can cut off a compromised VM entirely. Enforcement is applied by every AHV host at the virtual switch, with no agent inside any guest.](../../../diagrams/volume-121-nutanix-flow-lab/chapter-01-lab-topology.svg)

*Figure 1-1. Nutanix Flow Network Security enforces category-driven policy at the AHV virtual switch: policies name categories, never addresses, and are written in monitor mode first — flows are visualized before anything is dropped — then applied. The guest holds no rules and runs no agent, so there is nothing inside the VM for an attacker to kill.*

## Learning Objectives

- State what this lab builds and how **Nutanix Flow Network Security** microsegments AHV VMs at the virtual switch.
- Understand **categories** — policy names key:value labels, never IP addresses.
- Understand the three policy types — **application**, **isolation**, and **quarantine** — and their precedence.
- Understand the **monitor-then-apply** workflow and the two tracks.
- Read the lab topology and the policy plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab modeled on **Nutanix Flow Network Security (FNS)** — the platform-native microsegmentation for the **AHV** hypervisor, managed in **Prism Central**. Three properties define the model:

- **Hypervisor-tier, agentless enforcement.** Policy is enforced by every AHV host **at the virtual switch**, on the VM's traffic as it enters the fabric. No agent runs inside any guest — there is nothing in the VM for an attacker with root to disable.
- **Categories drive policy.** VMs are labeled with **categories** (key:value pairs such as `AppTier: web` or `Environment: corp`), and policies reference categories, never addresses. Re-categorizing a VM changes its effective policy instantly, with no rule edits.
- **Monitor, then apply.** A policy is first saved in **monitor mode** — Prism Central visualizes every flow the policy would have allowed or blocked, without dropping anything — and only then **applied**. Observe-then-enforce is built into the product's workflow.

FNS provides three policy types, in strict precedence order: **quarantine** (cut a VM off entirely) beats **isolation** (two categories may never talk) beats **application** (whitelist the flows into and out of an application's tiers). This volume builds all three. Because FNS requires a Nutanix AHV cluster, the volume is **two-track**:

- **Track 1 — the real product (design level).** How categories, security policies, monitor mode, and quarantine are configured in Prism Central on an AHV cluster, described accurately.
- **Track 2 — a buildable native model.** One Linux host where the AHV virtual switch is a bridge, the VMs are namespaces, and the host's **nftables `bridge` family** enforces category-driven policy on bridged traffic — categories as named sets, monitor mode as a count-only chain, and the guests holding **no rules at all**, exactly the agentless property.

### The moving parts

| Part | What it is | FNS construct |
|:---|:---|:---|
| **Category** | key:value label on a VM | `AppTier: web`, `Environment: corp` |
| **Application policy** | Whitelist of flows for an app's tiers | Application security policy |
| **Isolation policy** | Two categories may never communicate | Isolation environment policy |
| **Quarantine policy** | Cut a VM off (strict or forensic) | Quarantine policy |
| **Monitor mode** | Visualize flows before enforcing | Policy in monitor state |
| **Prism Central** | Central policy and visibility plane | Prism Central (Flow enabled) |

Two ideas carry the volume:

- **The category is the policy language.** Rules name labels; membership decides behavior. Scale and change are handled by categorizing, not by editing rules.
- **Enforce beneath the guest.** The AHV host applies policy at the virtual switch — agentless, invisible to the workload, and outside the guest's trust boundary.

### Topology

```text
                 +---------------------------+
                 |  Prism Central (Flow)     |  categories + policies
                 |  monitor -> apply         |  flow visualization
                 +-------------+-------------+
                               | policy to every AHV host
        +---------- AHV virtual switch (enforced) -----------+
        |  web .10     db .20 :5432    hmi .30    plc .40    |
        +----------------------------------------------------+
   application:  web -> db:5432 allow , hmi -> plc:502 allow
   isolation:    Environment:corp  <-X->  Environment:ot
   quarantine:   (when invoked) VM loses all connectivity
```

### The policy plan

| VM | Address | Categories | Sanctioned flow |
|:---|:---|:---|:---|
| web | 10.150.0.10 | `AppTier: web`, `Environment: corp` | → db:5432 |
| db | 10.150.0.20 | `AppTier: db`, `Environment: corp` | (receives from web) |
| hmi | 10.150.0.30 | `AppTier: hmi`, `Environment: ot` | → plc:502 |
| plc | 10.150.0.40 | `AppTier: plc`, `Environment: ot` | (receives from hmi) |

Only the two application flows are permitted; the isolation policy additionally forbids all corp↔ot traffic, and a quarantine policy can remove a compromised VM from the network in one action.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Design-level steps in Prism Central on an AHV cluster |
| **Track 2** | Buildable steps on the native bridge/nftables model |
| `pc>` | Prism Central action (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Cleanup**.

## Summary and Completion Checklist

- [ ] Hypervisor-tier, agentless enforcement at the AHV virtual switch understood.
- [ ] Categories as the policy language internalized.
- [ ] The three policy types and their precedence (quarantine > isolation > application) understood.
- [ ] Monitor-then-apply workflow understood.
- [ ] Topology and policy plan read.
