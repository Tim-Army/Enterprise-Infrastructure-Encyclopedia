# Volume CVIII — Juniper Connected Security Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab on **Juniper Connected Security** — the model where the **SRX
> Series firewall** is the enforcement point, traffic is organized into **security zones**, and **security
> policies** (from-zone/to-zone, address set, application) decide who may talk to whom, with **dynamic
> address groups** adding reactive containment driven by threat intelligence. The lab puts a four-tier
> estate (web/db/hmi/plc) into four zones, proves a permit-any lets the operator reach the database, then
> contains it with least-privilege policies that permit only APP→DB:5432 and MGMT→OT:502 and rely on the
> SRX default inter-zone deny — then quarantines a "compromised" host by group membership without editing
> a rule. Because SRX/Junos is commercial, this volume is **two-track**: Track 1 on a real **vSRX 3.0**
> evaluation VM, Track 2 a native **Linux/nftables** zone model on one host. Nine chapters, ~24 walkthrough
> labs; the stateful-firewall counterpart to the previous volume's tag-fabric approach.

## Overview

Volume CVIII is a **hands-on lab volume** and the second of the fabric/firewall tier. Where
[Volume CVII (Cisco ISE + TrustSec)](../volume-107-cisco-ise-trustsec-lab/README.md) segmented by carrying
a group tag in the fabric, this volume segments with a **stateful firewall**: zones, ordered policies with
address and application granularity, and dynamic groups for reactive containment. Reading the two together
is the clearest way to see the two dominant network-enforcement models side by side.

Its distinguishing ideas are **default-deny between zones** (an SRX denies inter-zone traffic unless a
policy permits it) and **membership-driven reaction** (Connected Security contains an infected host by
adding it to a dynamic address group a standing policy denies — no rule edit, no commit). The lab builds
both by hand, then reaches the honest boundary: a firewall segments only what transits it, so intra-zone
and bypassed traffic need zone design or host controls beneath the firewall.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [Zones and the Address Book](chapters/03-zones-and-address-book.md) | 3.1–3.2 |
| 04 | [The Flat Policy and Lateral Movement](chapters/04-flat-policy-and-lateral-movement.md) | 4.1–4.3 |
| 05 | [Security Policies](chapters/05-security-policies.md) | 5.1–5.2 |
| 06 | [Dynamic Address Groups and Connected Security](chapters/06-dynamic-address-groups.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Security Director, Policy Enforcer, and the Boundary](chapters/08-security-director-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Assign interfaces to security zones and build an address book of named objects.
- Author least-privilege zone-to-zone policies scoped by address and application.
- Rely on the SRX default inter-zone deny and remove a permit-any safely.
- Contain a host with a dynamic address group without editing policy.
- Read the session table, hit counts, and security log; identify the firewall's boundary.

## Prerequisites

- **Track 1:** a Juniper **vSRX 3.0** evaluation VM (KVM/ESXi/Workstation) and four endpoint VMs.
- **Track 2:** one Ubuntu 22.04 host with `nftables` and `iproute2` (no Juniper software required).

## See also

- [Volume CVII — Cisco ISE and TrustSec](../volume-107-cisco-ise-trustsec-lab/README.md) — the tag-fabric model to contrast with this stateful-firewall model.
- [Volume XXXI — Juniper Networks Certification Tracks](../volume-031-juniper-networks-certifications/README.md) — broader Junos and SRX coverage.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
