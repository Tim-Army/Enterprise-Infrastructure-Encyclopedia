# Volume CXV — TXOne Networks Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab modeled on **TXOne Networks**, the OT-security vendor whose
> products *block* rather than merely observe. Where the passive monitors delegate enforcement, TXOne's
> **EdgeIPS/EdgeFire** sit **inline as a transparent bump-in-the-wire** — dropped in front of an OT cell
> **without changing any IP** — and enforce OT-aware policy, headlined by **virtual patching**: IPS
> signatures that shield an unpatchable device from a known exploit *without touching the device*. On the
> host, **StellarProtect** enforces **application lockdown** so only approved software runs. The lab stands
> up a genuinely vulnerable PLC, lands the exploit, inserts a transparent inline inspector, arms a virtual
> patch that blocks the exploit while the PLC stays unpatched, adds a trust list and command filter, and
> locks down the engineering host with a hash-based allowlist. Because TXOne is commercial, this volume is
> **two-track**: Track 1 describes EdgeIPS/EdgeFire/StellarProtect at design level; **Track 2 is a fully
> buildable inline model** (transparent redirect + signature inspector + application-lockdown launcher).
> Nine chapters, ~22 walkthrough labs.

## Overview

Volume CXV is a **hands-on lab volume** and the fourth of the OT-security tier. It is the **enforcement**
counterpart to the passive monitors: Claroty ([CXIII](../volume-113-claroty-xdome-lab/README.md)) and
Nozomi ([CXIV](../volume-114-nozomi-networks-lab/README.md)) see and decide but delegate blocking — TXOne
is the inline device that does the blocking, plus the endpoint layer they lack.

Its defining idea is **protecting the unpatchable**: OT equipment that cannot be fixed is shielded by a
transparent inline virtual patch and by locking down the hosts around it. The lab makes both concrete —
a real exploit against a vulnerable PLC, blocked inline without modifying the device, and a malware binary
denied execution on a locked-down engineering host — and draws the honest boundary: inline protection is a
placement problem (a bypass path defeats it) and virtual patching blocks the *known*, so it pairs with
behavioral detection for the unknown.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [Transparent Inline Deployment](chapters/03-transparent-inline-deployment.md) | 3.1–3.2 |
| 04 | [Virtual Patching](chapters/04-virtual-patching.md) | 4.1–4.2 |
| 05 | [Trust List and Command Filtering](chapters/05-trust-list-and-command-filtering.md) | 5.1–5.2 |
| 06 | [Endpoint Lockdown with StellarProtect](chapters/06-endpoint-lockdown.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Central Management, Scale, and the Boundary](chapters/08-central-management-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Insert a transparent inline inspector without changing any device's IP.
- Arm a virtual patch that blocks a known exploit while the device stays unpatched.
- Enforce a trust list and command filter inline.
- Lock an OT host to a hash-based application allowlist.
- Verify layered network + endpoint protection and state the placement boundary.

## Prerequisites

- **Track 1:** TXOne EdgeIPS/EdgeFire and StellarProtect (commercial; covered at design level).
- **Track 2:** one Ubuntu 22.04 host with `python3`, `nftables`, and `iproute2` (fully buildable, no TXOne software).

## See also

- [Volume CXIV — Nozomi Networks](../volume-114-nozomi-networks-lab/README.md) and [Volume CXIII — Claroty xDome](../volume-113-claroty-xdome-lab/README.md) — the passive monitors TXOne enforces for.
- [Volume CXII — Xage Security](../volume-112-xage-security-lab/README.md) — identity-brokered OT access.
- [Volume LXX — Trellix Certification Tracks](../volume-070-trellix-certifications/README.md) — endpoint protection lineage (application control).
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
