# Volume XXIX — Cisco Service Provider

Service provider networks carry everyone else's traffic. Their scale,
their multi-tenancy, and their strict service-level obligations make
them a discipline apart from the enterprise: IS-IS and BGP at internet
scale, MPLS and Segment Routing as the transport substrate, L2VPN and
L3VPN as the products sold to customers, and automation as the only
way to operate tens of thousands of devices. This volume teaches that
discipline on Cisco's SP platforms — IOS XR foremost — end to end.

## Overview

The volume follows how a provider network is built and monetized. It
opens with SP architecture and the IOS XR operating model, builds the
core routing (IS-IS, then BGP and its address families and scaling),
lays the MPLS and Segment Routing transport, adds traffic engineering
and fast restoration, then turns to the revenue layer: L3VPNs, L2VPNs
and EVPN, and multicast. QoS and the provider edge shape and police
customer traffic; security and assurance harden and observe the
network; and the closing chapter covers automation, model-driven
telemetry, and certification readiness.

The certification spine is the **CCNP Service Provider** track — the
SPCOR core and its concentrations — with every domain mapped in the
certification alignment below.

## Chapters

1. [Service Provider Architecture and the IOS XR Operating Model](chapters/01-service-provider-architecture-and-the-ios-xr-operating-model.md)
2. [Provider Core Routing: IS-IS and OSPF at Scale](chapters/02-provider-core-routing-is-is-and-ospf-at-scale.md)
3. [BGP for Service Providers: Design, Policy, and Scale](chapters/03-bgp-for-service-providers-design-policy-and-scale.md)
4. [MPLS and Segment Routing Transport](chapters/04-mpls-and-segment-routing-transport.md)
5. [Traffic Engineering and Fast Restoration](chapters/05-traffic-engineering-and-fast-restoration.md)
6. [L3VPN Services](chapters/06-l3vpn-services.md)
7. [L2VPN and EVPN Services](chapters/07-l2vpn-and-evpn-services.md)
8. [Provider QoS, Multicast, and the Edge](chapters/08-provider-qos-multicast-and-the-edge.md)
9. [Automation, Assurance, and Certification Readiness](chapters/09-automation-assurance-and-certification-readiness.md)

## Volume resources

- [Index](INDEX.md) — alphabetized topics with chapter pointers
- [Glossary](GLOSSARY.md) — service provider terminology introduced in
  this volume

## Related volumes

- [Volume III — Cisco Enterprise Networking](../volume-03-cisco-enterprise-networking/README.md)
  supplies the IGP and BGP foundations this volume scales up.
- [Volume XXVII — Cisco Data Center](../volume-27-cisco-data-center/README.md)
  shares the VXLAN EVPN and segment-routing ideas that recur here at
  provider scale.
- [Volume IX — Infrastructure Automation](../volume-09-infrastructure-automation/README.md)
  deepens the model-driven tooling Chapter 09 applies to IOS XR.

## Certification alignment

This volume maps to the **CCNP Service Provider** certification track,
as recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). CCNP
Service Provider requires the `SPCOR` core exam plus **one**
concentration exam; this volume covers the core and all three
concentrations. `SPCOR` is also the qualifying exam for **CCIE Service
Provider**. Chapter content describes blueprint domains and points to
Cisco's official sources; it does not reproduce proprietary exam
questions or licensed courseware.

### The exams

| Exam | Title | Duration | Role in the track |
| --- | --- | --- | --- |
| **350-501 SPCOR** v1.1 | Implementing and Operating Cisco Service Provider Network Core Technologies | 120 min | Core — required for CCNP Service Provider and CCIE Service Provider |
| **300-510 SPRI** v1.1 | Implementing Cisco Service Provider Advanced Routing Solutions | 90 min | Concentration |
| **300-515 SPVI** v1.1 | Implementing Cisco Service Provider VPN Solutions | 90 min | Concentration |
| **300-535 SPAUTO** v1.1 | Automating and Programming Cisco Service Provider Solutions | 90 min | Concentration — **end-of-life announced** by Cisco under the Automation restructure; confirm availability before scheduling |

All are delivered through Pearson VUE. Question counts, cut scores,
and pricing are set per exam and are not restated here; confirm them
at registration.

### Domain weights, mapped to this volume

**350-501 SPCOR v1.1**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Architecture | 15% | 01 |
| 2.0 Networking | 30% | 02, 03 |
| 3.0 MPLS and Segment Routing | 20% | 04, 05 |
| 4.0 Services | 20% | 06, 07, 08 |
| 5.0 Automation and Assurance | 15% | 09 |

**300-510 SPRI v1.1**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Unicast Routing | 35% | 02, 03 |
| 2.0 Multicast Routing | 15% | 08 |
| 3.0 Routing Policy and Manipulation | 25% | 03 |
| 4.0 MPLS and Segment Routing | 25% | 04, 05 |

**300-515 SPVI v1.1**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 VPN Architecture | 25% | 06, 07 |
| 2.0 Layer 2 VPNs | 30% | 07 |
| 3.0 Layer 3 VPNs | 35% | 06 |
| 4.0 IPv6 VPNs | 10% | 06 |

**300-535 SPAUTO v1.1** *(EOL announced — see above)*

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Network Programmability Foundation | 10% | 09 |
| 2.0 Automation APIs and Protocols | 30% | 09 |
| 3.0 Network Device Programmability | 30% | 09 |
| 4.0 Automation and Orchestration Platforms | 30% | 09 |

### Study plan

**SPCOR — eight to ten weeks** at 8–10 hours per week, for a reader
with the Volume III routing foundation:

| Week | Focus | Chapters |
| --- | --- | --- |
| 1 | SP architecture, IOS XR operating model, platforms and planes | 01 |
| 2–4 | **The heavy block (30%).** Core routing: IS-IS at scale, then BGP address families, route reflection, policy, and convergence | 02, 03 |
| 5 | MPLS label operations and Segment Routing (SR-MPLS, SRv6 concepts) | 04 |
| 6 | Traffic engineering, TI-LFA, and fast restoration | 05 |
| 7 | Services: L3VPN, then L2VPN/EVPN | 06, 07 |
| 8 | Provider QoS models, multicast, and the edge | 08 |
| 9 | Automation and assurance: model-driven config and telemetry | 09 |
| 10 | Full-blueprint review weighted to Networking, timed practice | — |

Then one concentration within a few months, three to five weeks each,
by role: **SPRI** for the routing specialist (Chapters 02–05 in
depth — its Unicast Routing domain alone is 35%), **SPVI** for the
services engineer (Chapters 06–07; its L3VPN and L2VPN domains are 65%
combined), and **SPAUTO** for automation — schedulable only after
confirming Cisco still offers it, given the announced end-of-life;
Chapter 09 carries its material.

### Study materials

| Role | Resource | Why |
| --- | --- | --- |
| Official blueprint | [Cisco Learning Network exam topics](https://learningnetwork.cisco.com/s/) | Authority on domains, weights, and versions — outranks any third-party source |
| Reference text | Cisco Press Official Cert Guide for SPCOR | Blueprint-ordered and thorough |
| Official training | [Cisco U.](https://u.cisco.com/) | Guided paths for the track |
| Practice exams | Boson ExSim-Max where available | Closest simulation of Cisco question style |
| Lab | Cisco Modeling Labs with IOS XRv 9000 nodes | XRv carries the whole blueprint short of hardware-specific forwarding — see Practicing |

### CCIE lab readiness

**CCIE Service Provider v5.1** sits above the CCNP track, reached by
first passing the `SPCOR 350-501` core. It is an **eight-hour, hands-on
practical exam** in the standard CCIE two-module shape — a **3-hour
Design** module (scenario-based, no device access) and a **5-hour
Deploy, Operate, and Optimize** module — covering the full provider
lifecycle: IS-IS and BGP at scale, MPLS and Segment Routing, traffic
engineering, L3VPN and L2VPN/EVPN, QoS, and multicast on IOS XR, with
programmability and model-driven operation expected throughout. Cisco is
adding a **new AI module** to its CCIE practical exams — confirm the
current format at registration.

**What the lab adds over this volume.** These chapters build
provider-technology knowledge and IOS XR configuration skill at
professional depth; the lab tests **speed, integration, and
troubleshooting under time** — building a provider core with services
layered on it (SR transport, TI-LFA protection, L3VPN and EVPN isolation
all working together), quickly, then diagnosing deliberately broken
scenarios where IP reachability and label reachability diverge, at pace.

**How to prepare.** Rehearse full topologies against the clock with IOS
XRv 9000 in Cisco Modeling Labs (or the DevNet IOS XR sandboxes): a
complete provider build — core IGP, BGP/RR, SR transport, TI-LFA, L3VPN,
EVPN — end to end, then the same network broken for you to repair using
the layer-by-layer method the chapters teach. Pair each chapter's
Hands-On Lab with a timed rebuild, drill the Design module using the
method in [Volume XXX](../volume-30-cisco-ccde-network-design/README.md),
and use Cisco's official CCIE Service Provider practice labs before exam
day. Confirm the current lab blueprint and format on the Cisco Learning
Network before scheduling — CCIE lab topics are separate from the
written exam topics and change independently.

## Practicing

The service provider blueprint is almost entirely testable in Cisco
Modeling Labs: the **IOS XRv 9000** image runs IS-IS, BGP, MPLS,
Segment Routing, L3VPN, L2VPN/EVPN, and the model-driven interfaces of
Chapter 09, and multi-node topologies model a provider core and its
PE/CE edges. Where hardware ASIC behavior matters — line-rate QoS,
scale numbers — the lab teaches the configuration and control plane
while the datasheet supplies the forwarding limits. DevNet's IOS XR
sandboxes provide the same environment hosted, including
programmability targets.

## Software and platform baseline

Guidance in this volume is written against the dated baseline in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): Cisco IOS XR 7.x on
ASR 9000 / NCS platforms, with SR-MPLS as the default transport and
SRv6 treated as the forward direction. Where a feature differs across
XR trains, the chapter says so rather than assuming the newest.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format html --volume volume-29-cisco-service-provider
```
