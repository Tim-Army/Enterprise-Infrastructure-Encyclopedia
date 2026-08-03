# Volume CXX — NVIDIA BlueField Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab modeled on the **NVIDIA BlueField DPU** — a data processing
> unit on the server's network adapter that sits between the host's workloads and the network and enforces
> segmentation **in the DPU**, on its own Arm cores running the **DOCA** framework. Two properties set it
> apart: **per-server enforcement at the NIC** (each host's own adapter firewalls its workloads, not a
> shared switch), and — the defining one — enforcement in an **isolated trust domain the host CPU cannot
> tamper with**, so the segmentation **survives host compromise**, which a host agent an attacker can kill
> cannot guarantee. The lab puts each protected workload behind its own DPU, applies a default-deny policy
> permitting only its sanctioned flow, then attacks the policy from a fully-compromised workload (flushing
> and rewriting its own firewall rules) and shows it changes nothing because the policy lives in a
> namespace the workload cannot reach — the out-of-band property made concrete. Because BlueField
> enforcement is DPU hardware with no free emulator, this volume is **design-leaning two-track**: Track 1
> describes BlueField/DOCA; **Track 2 is a fully buildable out-of-band model** — each workload's only path
> to the network is a separate DPU namespace it has no access to. Nine chapters, ~22 walkthrough labs.

## Overview

Volume CXX is a **hands-on lab volume** and the fourth of the hardware-fabric/DPU tier — the second and
final DPU volume, paired with the CX 10000 ([CXIX](../volume-119-hpe-aruba-cx10000-lab/README.md)). Where
the CX 10000 puts a DPU in the top-of-rack switch to firewall a whole rack, BlueField puts a DPU on **each
server's NIC**, so enforcement is host-adjacent yet outside the host's trust boundary.

Its defining contribution is **tamper-resistant enforcement**: the policy runs beside the workload but on a
separate computer the attacker cannot reach, so it holds even on a fully-owned host — the strongest answer
to the "an attacker with root disables the agent" failure mode of host-based microsegmentation. The lab
makes that concrete by attacking the policy from inside a compromised workload and watching it survive, and
draws the honest boundary: enforcement is where the DPU is, and the management plane that programs it must
itself be secured.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [The Flat Network and Lateral Movement](chapters/03-flat-network-and-lateral-movement.md) | 3.1–3.3 |
| 04 | [DPU-Enforced Microsegmentation](chapters/04-dpu-enforced-microsegmentation.md) | 4.1–4.2 |
| 05 | [The Out-of-Band Advantage](chapters/05-out-of-band-advantage.md) | 5.1–5.2 |
| 06 | [Offload and Host CPU](chapters/06-offload-and-host-cpu.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Scale, Management, and the Boundary](chapters/08-scale-management-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Place each workload behind its own DPU namespace, isolated from the workload.
- Apply default-deny policy in the DPU permitting only the sanctioned flow.
- Prove a fully-compromised workload cannot disable its own DPU policy.
- Show enforcement runs in the DPU domain at zero host-CPU cost.
- State the per-DPU-server boundary and where BlueField fits among the enforcement models.

## Prerequisites

- **Track 1:** servers with NVIDIA BlueField DPUs and DOCA — hardware; covered at design level.
- **Track 2:** one Ubuntu 22.04 host with `nftables` and `iproute2` (fully buildable, no NVIDIA hardware).

## See also

- [Volume CXIX — HPE Aruba CX 10000](../volume-119-hpe-aruba-cx10000-lab/README.md) — the ToR-switch DPU model, paired with this per-server DPU one.
- [Volume XCIII — ColorTokens Xshield](../volume-093-colortokens-xshield-lab/README.md) and the host-agent labs (Volumes XCIV–C) — the on-host model whose tamper weakness DPU enforcement addresses.
- [Volume XLVI — NVIDIA Certification Tracks](../volume-046-nvidia-certifications/README.md) — broader NVIDIA/DOCA coverage.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
