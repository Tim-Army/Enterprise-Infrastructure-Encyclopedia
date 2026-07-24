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
concentration exam; this volume covers the core, SPRI, SPVI, and the
retired SPAUTO in depth; the new SPCNI cloud-infrastructure
concentration is mapped in the exam table below. `SPCOR` is also the qualifying exam for **CCIE Service
Provider**. Chapter content describes blueprint domains and points to
Cisco's official sources; it does not reproduce proprietary exam
questions or licensed courseware.

### The exams

| Exam | Title | Duration | Role in the track |
| --- | --- | --- | --- |
| **350-501 SPCOR** v1.1 | Implementing and Operating Cisco Service Provider Network Core Technologies | 120 min | Core — required for CCNP Service Provider and CCIE Service Provider |
| **300-510 SPRI** v1.1 | Implementing Cisco Service Provider Advanced Routing Solutions | 90 min | Concentration |
| **300-515 SPVI** v1.1 | Implementing Cisco Service Provider VPN Solutions | 90 min | Concentration |
| **300-540 SPCNI** v1.0 | Designing and Implementing Cisco Service Provider Cloud Network Infrastructure | 90 min | Concentration |
| **300-535 SPAUTO** v1.1 | Automating and Programming Cisco Service Provider Solutions | 90 min | **Retired 2026** under the Automation restructure — kept for the record |

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

**300-540 SPCNI v1.0** *(new for 2026 — no dedicated chapter yet;
study from Cisco's exam-topics page)*

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Virtualized Architecture | 25% | — |
| 2.0 Cloud Interconnect | 25% | — |
| 3.0 High Availability | 20% | — |
| 4.0 Security | 15% | — |
| 5.0 Service Assurance and Optimization | 15% | — |

**300-535 SPAUTO v1.1** *(retired 2026 — kept for the record)*

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Network Programmability Foundation | 10% | 09 |
| 2.0 Automation APIs and Protocols | 30% | 09 |
| 3.0 Network Device Programmability | 30% | 09 |
| 4.0 Automation and Orchestration Platforms | 30% | 09 |

### Topic-level lab coverage

Every exam topic across **all current Cisco Service Provider certifications** —
the SPCOR core, the SPRI/SPVI/SPCNI concentrations, and CCIE Service Provider —
is covered by a hands-on **walkthrough** lab; the retired **SPAUTO 300-535**
automation blueprint is covered as well (kept for the record, and the subject of
Chapter 09 with the SPCOR automation domain). Topics were harvested from Cisco's
official exam-topics PDFs (`learningcontent.cisco.com`) in July 2026 — SPCOR/SPRI/
SPVI v1.1, SPCNI v1.0, SPAUTO v1.1. Labs use the IOS XR CLI, MPLS/Segment Routing,
L3VPN/L2VPN/EVPN, NETCONF/RESTCONF/gNMI, YANG tooling, and NSO/Crosswork. Each
carries `**Lab verified by:** *pending*` until a human runs it. **123 numbered
labs** in total, mapped one lab per exam topic (the core and concentrations are
distributed across chapters by domain):

**350-501 SPCOR v1.1**

| Exam topic | Lab |
| --- | --- |
| 1.1 Describe service provider architectures | Lab 1.1 |
| 1.2 Describe Cisco network software architecture | Lab 1.2 |
| 1.3 Describe service provider virtualization | Lab 1.3 |
| 1.4 Describe QoS architecture | Lab 8.1 |
| 1.5 Configure and verify control plan security | Lab 8.3 |
| 1.6 Describe management plane security | Lab 8.4 |
| 1.7 Implement data plane security | Lab 8.5 |
| 2.1 Implement IS-IS (IPv4 and IPv6) | Lab 2.1 |
| 2.2 Implement OSPF (v2 and v3) | Lab 2.2 |
| 2.3 Describe BGP path selection algorithm. | Lab 3.1 |
| 2.4 Implement BGP (v4 and v6 for IBGP and EBGP) | Lab 3.2 |
| 2.5 Implement routing policy language and route maps (BGP, OSPF, IS-IS) | Lab 3.3 |
| 2.6 Troubleshoot routing protocols | Lab 3.4 |
| 2.7 Describe IPv6 transition (NAT44, NAT64, CGNAT, MAP-T and DS Lite) | Lab 8.6 |
| 2.8 Implement high availability | Lab 5.1 |
| 3.1 Implement MPLS | Lab 4.1 |
| 3.2 Describe traffic engineering | Lab 5.2 |
| 3.3 Describe segment routing | Lab 4.2 |
| 4.1 Describe VPN services | Lab 6.1 |
| 4.2 Configure L2VPN and Carrier Ethernet | Lab 7.1 |
| 4.3 Configure L3VPN | Lab 6.2 |
| 4.4 Implement multicast services | Lab 8.7 |
| 4.5 Implement QoS services | Lab 8.2 |
| 5.1 Describe the programmable APIs used to include Cisco devices in network … | Lab 9.1 |
| 5.2 Interpret an external script to configure a Cisco device using a REST … | Lab 9.2 |
| 5.3 Describe the role of Network Services Orchestration (NSO) | Lab 9.3 |
| 5.4 Describe the high-level principles and benefits of a data modeling … | Lab 9.4 |
| 5.5 Describe configuration management tools, such as Ansible and Terraform | Lab 9.5 |
| 5.6 Describe Secure ZTP | Lab 9.6 |
| 5.7 Configure dial-in/out, TCP, TLS and mTLS certificates using gRPC and … | Lab 9.7 |
| 5.8 Configure and verify NetFlow/IPFIX | Lab 9.8 |
| 5.9 Configure and verify NETCONF and RESTCONF | Lab 9.9 |
| 5.10 Configure and verify SNMP (v2c/v3) | Lab 9.10 |

**300-510 SPRI v1.1**

| Exam topic | Lab |
| --- | --- |
| 1.1 Compare OSPF and IS-IS routing protocols | Lab 2.3 |
| 1.2 Troubleshoot OSPF multiarea operations (IPv4 and IPv6) | Lab 2.4 |
| 1.3 Troubleshoot IS-IS multilevel operations (IPv4 and IPv6) | Lab 2.5 |
| 1.4 Describe the BGP scalability and performance | Lab 3.5 |
| 1.5 Troubleshoot BGP | Lab 3.6 |
| 1.6 Describe IPv6 tunneling mechanisms | Lab 2.6 |
| 1.7 Implement fast convergence | Lab 5.3 |
| 2.1 Compare multicast concepts | Lab 8.8 |
| 2.2 Describe multicast concepts | Lab 8.9 |
| 2.3 Implement PIM-SM operations | Lab 8.10 |
| 2.4 Troubleshoot multicast routing | Lab 8.11 |
| 3.1 Compare routing policy language and route maps | Lab 3.7 |
| 3.2 Describe conditional matching | Lab 3.8 |
| 3.3 Troubleshoot route manipulation for IGPs | Lab 3.9 |
| 3.4 Troubleshoot route manipulation for BGP | Lab 3.10 |
| 4.1 Troubleshoot MPLS | Lab 4.3 |
| 4.2 Implement segment routing | Lab 4.4 |
| 4.3 Implement segment routing traffic engineering | Lab 5.4 |
| 4.4 Implement segment routing v6 (SRv6) | Lab 4.5 |

**300-515 SPVI v1.1**

| Exam topic | Lab |
| --- | --- |
| 1.1 Compare VPN architecture | Lab 6.3 |
| 1.2 Troubleshoot underlay | Lab 6.4 |
| 1.3 Describe Layer 2 service architecture | Lab 7.2 |
| 1.4 Describe the L3VPN control plane operation | Lab 6.5 |
| 1.5 Describe the L3VPN data plane operation | Lab 6.6 |
| 2.1 Troubleshoot L2VPN Services | Lab 7.3 |
| 2.2 Describe EVPN concepts | Lab 7.4 |
| 2.3 Implement Ethernet Operations, Administration, and Maintenance (E-OAM) | Lab 7.5 |
| 2.4 Implementing EVPN | Lab 7.6 |
| 3.1 Describe routing requirements | Lab 6.7 |
| 3.2 Troubleshoot Intra-AS L3VPNs | Lab 6.8 |
| 3.3 Implement multicast VPN | Lab 6.9 |
| 3.4 Implement extranet/shared services | Lab 6.10 |
| 3.5 Describe Inter-AS L3VPNs | Lab 6.11 |
| 3.6 Describe CSC concepts | Lab 6.12 |
| 4.1 Describe routing requirements | Lab 6.13 |
| 4.2 Troubleshoot IPv6 VPN provider edge | Lab 6.14 |

**300-540 SPCNI v1.0**

| Exam topic | Lab |
| --- | --- |
| 1.1 Describe IaaS constraints such as VLAN scale and segmentation | Lab 1.4 |
| 1.2 Determine the cloud service model (such as IaaS, PaaS, SaaS, and FaaS) … | Lab 1.5 |
| 1.3 Describe container orchestration and virtual machines | Lab 1.6 |
| 1.4 Implement virtualization functions | Lab 1.7 |
| 1.5 Deploy NFV using automation and orchestration | Lab 1.8 |
| 2.1 Describe carrier-neutral facilities | Lab 7.7 |
| 2.2 Evaluate WAN infrastructure connectivity | Lab 7.8 |
| 2.3 Troubleshoot DCI solutions | Lab 7.9 |
| 3.1 Implement technologies for high availability | Lab 5.5 |
| 3.2 Implement multi-homing | Lab 5.6 |
| 3.3 Implement EVLAG | Lab 5.7 |
| 3.4 Implement a virtual private cloud | Lab 5.8 |
| 3.5 Implement ECMP from NFVI to physical infrastructure such as BGP … | Lab 5.9 |
| 3.6 Recommend design models for high availability such as DNS, routing, and … | Lab 5.10 |
| 4.1 Implement infrastructure security | Lab 8.12 |
| 4.2 Describe DoS mitigation techniques | Lab 8.13 |
| 4.3 Describe NFVI security | Lab 8.14 |
| 4.4 Describe cloud security solutions such as DNS security, zero-day … | Lab 8.15 |
| 5.1 Describe network assurance | Lab 9.11 |
| 5.2 Describe cloud infrastructure and performance monitoring | Lab 9.12 |
| 5.3 Diagnose NFVI errors and events | Lab 9.13 |
| 5.4 Describe VNF optimization | Lab 9.14 |

**300-535 SPAUTO v1.1 (retired)**

| Exam topic | Lab |
| --- | --- |
| 1.1 Utilize common version control operations with Git (add, clone, push, … | Lab 9.15 |
| 1.2 Describe characteristics of API styles (REST and RPC) | Lab 9.16 |
| 1.3 Describe the challenges encountered and patterns used when consuming … | Lab 9.17 |
| 1.4 Interpret Python scripts containing data types, functions, classes, … | Lab 9.18 |
| 1.5 Describe the benefits of Python virtual environments | Lab 9.19 |
| 1.6 Explain the benefits of using network configuration tools such as … | Lab 9.20 |
| 2.1 Describe the characteristics and use of YANG Data Models (OpenConfig, … | Lab 9.21 |
| 2.2 Describe common HTTP authentication mechanisms (basic, token, and oauth) | Lab 9.22 |
| 2.3 Compare common data types (JSON, XML, YAML, plain text, gRPC, and … | Lab 9.23 |
| 2.4 Interpret the JSON instance based on a YANG model | Lab 9.24 |
| 2.5 Interpret the XML instance based on a YANG model | Lab 9.25 |
| 2.6 Interpret a YANG module tree generated by pyang | Lab 9.26 |
| 2.7 Implement configuration and operation management using RESTCONF protocol | Lab 9.27 |
| 2.8 Implement configuration and operation management using NETCONF protocol | Lab 9.28 |
| 2.9 Compare the NETCONF datastores | Lab 9.29 |
| 3.1 Deploy device configuration and validate operational state using … | Lab 9.30 |
| 3.2 Construct a Python script using NETCONF with YDK, including YANG Suite | Lab 9.31 |
| 3.3 Deploy device configuration and validate operational state using NetMiko | Lab 9.32 |
| 3.4 Deploy device configuration and validate operational state using … | Lab 9.33 |
| 3.5 Compare gNMI with NETCONF and gRPC | Lab 9.34 |
| 3.6 Construct a Python script using RESTCONF, including YANG Suite | Lab 9.35 |
| 3.7 Construct XPath notation for a given node or instance of a node | Lab 9.36 |
| 3.8 Diagnose model-driven dial-in/-out telemetry streams with gRPC for a … | Lab 9.37 |
| 4.1 Describe ETSI NFV | Lab 9.38 |
| 4.2 Describe NSO architecture | Lab 9.39 |
| 4.3 Describe Cisco Crosswork Network Controller and applications | Lab 9.40 |
| 4.4 Construct a Python script to configure a device using NSO RESTCONF API | Lab 9.41 |
| 4.5 Describe the management and automation of Cisco ESC components | Lab 9.42 |
| 4.6 Implement SR-PCE (formerly XTC), including topology information … | Lab 9.43 |
| 4.7 Describe Cisco WAE | Lab 9.44 |
| 4.8 Construct a service template using NSO | Lab 9.45 |
| 4.9 Deploy a service package using NSO | Lab 9.46 |

### CCIE Service Provider coverage

The CCIE Service Provider **qualifying exam is 350-501 SPCOR**, covered above.
The 8-hour hands-on lab applies the same technologies at expert depth; its focus
areas map to this volume:

| CCIE Service Provider focus area | Chapters / labs |
| --- | --- |
| Core IGP (IS-IS/OSPF) and BGP | Chapters 02, 03 |
| MPLS, Segment Routing, and SRv6 | Chapter 04 |
| Traffic engineering and fast restoration | Chapter 05 |
| L3VPN services (incl. inter-AS, CSC, 6VPE) | Chapter 06 |
| L2VPN and EVPN services | Chapter 07 |
| QoS, multicast, security, and the edge | Chapter 08 |
| Automation, telemetry, and assurance | Chapter 09 |

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
combined), and **SPCNI** for the cloud-infrastructure designer (new
for 2026 — no dedicated chapter here; study from Cisco's SPCNI v1.0
exam topics). **SPAUTO** was retired by Cisco in 2026; Chapter 09
still carries its automation material for SPCOR's Automation and
Assurance domain.

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
