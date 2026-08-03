# Volume CXXI — Nutanix Flow Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab modeled on **Nutanix Flow Network Security (FNS)** — the
> platform-native microsegmentation for the **AHV** hypervisor, managed in **Prism Central**. Flow's model
> is **hypervisor-tier and agentless**: every AHV host enforces policy at the **virtual switch**, so no
> agent runs inside any guest; **categories** (key:value labels) are the entire policy language — rules
> name labels, never addresses; and every policy is written in **monitor mode** first (flows visualized,
> nothing dropped), then **applied**. The lab builds all three policy types in their precedence order —
> **application** (permit `web→db:5432` and `hmi→plc:502`, default-deny), **isolation**
> (`Environment: corp` ↔ `Environment: ot` may never talk), and **quarantine** (one category assignment
> cuts a compromised VM off entirely, beating every permit) — then proves the category-driven property by
> policy-enabling a new VM with zero rule edits, and drills the **Prism Central DR constraint** (categories
> and policies do not replicate between instances) with a backup/restore exercise. Because FNS requires a
> Nutanix cluster, this volume is **two-track**: Track 1 describes Prism Central; **Track 2 is a fully
> buildable model** — the virtual switch as a bridge, categories as nftables sets, enforcement in the
> host's `bridge` table with guests holding no rules at all. Nine chapters, ~23 walkthrough labs.

## Overview

Volume CXXI is a **hands-on lab volume** and the final volume of the microsegmentation lab program
(XCIII–CXXI). It closes the hypervisor tier alongside VMware NSX DFW
([CXI](../volume-111-vmware-nsx-dfw-lab/README.md)): both enforce beneath the guest at the virtual
switch, but Flow is defined by its **category-driven** policy language, its built-in
**monitor-then-apply** workflow, and its three-type policy model with strict precedence
(quarantine > isolation > application).

The lab reaches the honest boundary from both directions: enforcement is **AHV-only** (off-platform
workloads need the agent or fabric models of the earlier volumes), the virtual switch cannot see inside
a VM, and the platform's operational catch — **Flow policy does not replicate between Prism Central
instances** — is drilled as a backup/restore exercise rather than footnoted.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [The Flat Network and Lateral Movement](chapters/03-flat-network-and-lateral-movement.md) | 3.1–3.3 |
| 04 | [Categories and Monitor Mode](chapters/04-categories-and-monitor-mode.md) | 4.1–4.3 |
| 05 | [Applying the Application Policies](chapters/05-application-policies-apply.md) | 5.1–5.2 |
| 06 | [Isolation and Quarantine Policies](chapters/06-isolation-and-quarantine.md) | 6.1–6.3 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Prism Central, Scale, and the Boundary](chapters/08-prism-central-scale-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Categorize VMs and express security policy entirely in categories.
- Write a policy in monitor mode, read its flow telemetry, and apply it.
- Layer application, isolation, and quarantine policies and predict which layer decides each flow.
- Policy-enable a new VM by categorization alone — zero rule edits.
- Drill the Prism Central DR constraint with a policy export and restore.
- State the AHV-only, virtual-switch boundary of the model.

## Prerequisites

- **Track 1:** a Nutanix AHV cluster with Prism Central and Flow Network Security (Community Edition for study; per-node subscription in production) — design level.
- **Track 2:** one Ubuntu 22.04 host with `nftables` and `iproute2` (fully buildable, no Nutanix software).

## See also

- [Volume CXI — VMware NSX Distributed Firewall](../volume-111-vmware-nsx-dfw-lab/README.md) — the other hypervisor-tier model, for contrast with category-driven Flow.
- [Volume LI — Nutanix Certification Tracks](../volume-051-nutanix-certifications/README.md) — broader Nutanix platform and certification coverage.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab program pairs with.
