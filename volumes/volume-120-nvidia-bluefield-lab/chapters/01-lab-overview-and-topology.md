# Chapter 01: Lab Overview and Topology

![Lab topology: each protected workload sits behind its own NVIDIA BlueField DPU, which enforces segmentation at the NIC in a trust domain isolated from the host CPU. DPU-web permits only web-to-db:5432 and DPU-hmi permits only hmi-to-plc:502; every other flow is denied at the workload's own DPU, and a compromised host with root cannot see, disable, or alter the DPU policy.](../../../diagrams/volume-120-nvidia-bluefield-lab/chapter-01-lab-topology.svg)

*Figure 1-1. NVIDIA BlueField enforces segmentation per server at the NIC, in a trust domain the host CPU cannot reach: each workload's DPU permits only its sanctioned flow, and because the policy runs beside the workload but outside its trust boundary, the segmentation survives a fully-compromised host — the answer to the killable-agent weakness of host-based microsegmentation.*

## Learning Objectives

- State what this lab builds and how the NVIDIA BlueField **DPU enforces segmentation at each server's NIC**.
- Understand the defining property: enforcement in an **isolated trust domain** the host CPU cannot tamper with.
- Understand the two tracks — a design view of BlueField/DOCA, and a buildable out-of-band enforcement model.
- Read the lab topology and the policy plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab modeled on the **NVIDIA BlueField DPU** — a data processing unit on the server's network adapter that sits **between the host's workloads and the network** and enforces policy **in the DPU**, on its own Arm cores running its own OS via the **DOCA** framework. Two properties make it distinctive among the fabric/DPU volumes:

- **Per-server enforcement at the NIC.** Unlike a ToR-switch DPU (the previous volume) that firewalls a whole rack, BlueField enforces at **each host's own adapter**, so policy is applied to a workload's traffic before it reaches the wire, per server.
- **An isolated trust domain.** The DPU is a separate computer from the host — a **compromised host CPU cannot see, disable, or alter** the DPU's segmentation policy. Enforcement survives host compromise, which host-agent microsegmentation (an agent the attacker can kill) cannot guarantee.

The theme is **enforcement the host cannot tamper with**: the segmentation runs beside the workload but outside its trust boundary. BlueField enforcement lives in DPU hardware with no free emulator, so this volume is **design-leaning two-track**:

- **Track 1 — the real product (design level).** How segmentation/firewall policy is deployed to BlueField DPUs (DOCA, partner microseg running on the DPU) and managed, described accurately.
- **Track 2 — a buildable out-of-band model.** One Linux host where each workload is a namespace whose only path to the network is through a **separate DPU namespace** it has no access to; the DPU namespace holds the policy, so a "compromised" workload cannot disable its own segmentation — the isolated-trust-domain property made concrete.

### The moving parts

| Part | What it is | BlueField construct |
|:---|:---|:---|
| **DPU (per NIC)** | A separate processor on the server's adapter | BlueField DPU |
| **Isolated trust domain** | Policy the host CPU cannot tamper with | DPU control plane |
| **DOCA** | The DPU software framework | NVIDIA DOCA |
| **Distributed firewall** | Per-workload policy enforced at the NIC | DPU-offloaded segmentation |
| **Offload** | Enforcement at zero host-CPU cost | DPU hardware offload |

Two ideas carry the volume:

- **Enforce beside the workload, outside its trust boundary.** The DPU applies policy at the NIC, isolated from the host it protects.
- **Survives host compromise.** Because the attacker cannot reach the DPU, the segmentation holds even on a fully-owned host.

### Topology

```text
   Each server: workload  --[ BlueField DPU (isolated) ]-->  network
   +-----------+        +-----------------+
   | web (host)| =====> | DPU-web policy  | ====> db:5432 (allowed)
   +-----------+        +-----------------+  X--> hmi (denied)
   +-----------+        +-----------------+
   | hmi (host)| =====> | DPU-hmi policy  | ====> plc:502 (allowed)
   +-----------+        +-----------------+  X--> db  (denied)
   host compromise cannot alter the DPU policy (separate trust domain)
```

### The policy plan

| Workload | Address | DPU-enforced permit |
|:---|:---|:---|
| web | 10.140.0.10 | → db:5432 |
| db | 10.140.0.20 | (receives from web) |
| hmi | 10.140.0.30 | → plc:502 |
| plc | 10.140.0.40 | (receives from hmi) |

Only the two flows are permitted; each workload's DPU denies everything else, and the host cannot change its DPU's policy.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Design-level steps on BlueField / DOCA |
| **Track 2** | Buildable steps on the native out-of-band DPU model |
| `dpu>` | DPU/DOCA action (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Cleanup**.

## Summary and Completion Checklist

- [ ] Per-server DPU enforcement at the NIC understood.
- [ ] The isolated-trust-domain / survives-host-compromise property internalized.
- [ ] Track chosen (Track 2 is the buildable one).
- [ ] Topology and policy plan read.
