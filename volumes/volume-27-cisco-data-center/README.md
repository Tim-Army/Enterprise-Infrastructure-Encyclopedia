# Volume XXVII — Cisco Data Center

The data center is where the enterprise's applications actually live,
and Cisco's data center portfolio — Nexus switching, ACI, UCS compute,
storage networking, and now AI infrastructure — is its own discipline
with its own certification track. This volume teaches that discipline
end to end: the switching fabrics that move east-west traffic, the
policy model that replaced box-by-box configuration, the compute and
storage layers underneath, the automation that operates all of it, and
the AI-cluster requirements reshaping data center design.

## Overview

The volume is sequenced the way a data center is actually built and
operated. It opens with architecture and the platform landscape, builds
the network layer (NX-OS switching, vPC, VXLAN EVPN, then ACI's policy
model), adds compute (UCS) and storage networking (Fibre Channel, FCoE,
NVMe), then turns to how modern data centers are run: automation and
APIs, AI infrastructure, security and segmentation, and finally design
methodology, structured troubleshooting, and certification readiness.

Every chapter pairs theory with configuration against real platform
behavior, closes with a hands-on lab, and carries the standard
verification sign-off. The certification spine is the **CCNP Data
Center** track — the DCCOR core and its five concentration exams — with
the chapter mapping recorded in the certification alignment below.

## Chapters

1. [Data Center Architecture and the CCNP Data Center Track](chapters/01-data-center-architecture-and-the-ccnp-data-center-track.md)
2. [Nexus Switching, vPC, and VXLAN EVPN Fabrics](chapters/02-nexus-switching-vpc-and-vxlan-evpn-fabrics.md)
3. [ACI: Policy Model, Fabric Operations, and External Connectivity](chapters/03-aci-policy-model-fabric-and-external-connectivity.md)
4. [UCS Compute and Hyperconverged Platforms](chapters/04-ucs-compute-and-hyperconverged-platforms.md)
5. [Storage Networking: Fibre Channel, FCoE, and NVMe](chapters/05-storage-networking-fibre-channel-fcoe-and-nvme.md)
6. [Data Center Automation: NX-API, Models, and Tooling](chapters/06-data-center-automation-nx-api-models-and-tooling.md)
7. [Data Center AI Infrastructure](chapters/07-data-center-ai-infrastructure.md)
8. [Data Center Security and Segmentation](chapters/08-data-center-security-and-segmentation.md)
9. [Design, Troubleshooting, and Certification Readiness](chapters/09-design-troubleshooting-and-certification-readiness.md)

## Volume resources

- [Index](INDEX.md) — alphabetized topics with chapter pointers
- [Glossary](GLOSSARY.md) — data center terminology introduced in this
  volume

## Related volumes

- [Volume III — Cisco Enterprise Networking](../volume-03-cisco-enterprise-networking/README.md)
  supplies the routing, switching, and IOS XE foundations this volume
  assumes.
- [Volume VI — Enterprise Storage and Data Protection](../volume-06-enterprise-storage-data-protection/README.md)
  covers the storage systems whose traffic Chapter 05 transports.
- [Volume IX — Infrastructure Automation](../volume-09-infrastructure-automation/README.md)
  goes deeper on the automation tooling Chapter 06 applies to Nexus and
  ACI.
- [Volume XXV — Cisco Security](../volume-25-cisco-security/README.md)
  extends the security model where the data center meets the enterprise
  security stack.

## Certification alignment

This volume maps to the **CCNP Data Center** certification track, as
recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). CCNP
Data Center requires the `DCCOR` core exam plus **one** concentration
exam; this volume covers the core and all five concentrations. `DCCOR`
is also the qualifying exam for **CCIE Data Center**. Chapter content
describes blueprint domains and points to Cisco's official sources; it
does not reproduce proprietary exam questions or licensed courseware.

### The exams

| Exam | Title | Duration | Role in the track |
| --- | --- | --- | --- |
| **350-601 DCCOR** v1.2 | Implementing Cisco Data Center Core Technologies | 120 min | Core — required for CCNP Data Center and CCIE Data Center |
| **300-610 DCID** v1.2 | Designing Cisco Data Center Infrastructure | 90 min | Concentration |
| **300-615 DCIT** v1.2 | Troubleshooting Cisco Data Center Infrastructure | 90 min | Concentration |
| **300-620 DCACI** v1.2 | Implementing Cisco Application Centric Infrastructure | 90 min | Concentration |
| **300-635 DCAUTO** v1.1 | Automating Cisco Data Center Solutions | 90 min | Concentration |
| **300-640 DCAI** v1.0 | Implementing Cisco Data Center AI Infrastructure | 90 min | Concentration (specialist, GA 3 February 2026) |

All are delivered through Pearson VUE. Question counts, cut scores, and
pricing are set per exam and are not restated here; confirm them at
registration.

**Two portfolio movements to know about.** DCAI arrived on 3 February
2026 as the newest path to the certification — DCAI plus DCCOR earns
CCNP Data Center. In the same restructure, Cisco began rebranding
`300-635 DCAUTO` as `DCNAUTO` under the new CCNP Automation track;
the code is unchanged, but confirm its concentration status for the
Data Center track at registration if automation is your chosen
concentration.

### Domain weights, mapped to this volume

**350-601 DCCOR v1.2**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Network | 25% | 02, 03 |
| 2.0 Compute | 25% | 04 |
| 3.0 Storage Network | 20% | 05 |
| 4.0 Automation and Artificial Intelligence | 15% | 06, 07 |
| 5.0 Security | 15% | 08 |

**300-610 DCID v1.2**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Network Design | 35% | 02, 03, 09 |
| 2.0 Compute Design | 25% | 04, 09 |
| 3.0 Storage Network Design | 20% | 05, 09 |
| 4.0 Automation Design | 20% | 06, 09 |

**300-615 DCIT v1.2**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Network | 25% | 02, 03, 09 |
| 2.0 Compute Platforms | 25% | 04, 09 |
| 3.0 Storage Network | 15% | 05, 09 |
| 4.0 Automation | 15% | 06, 09 |
| 5.0 Management and Operations | 20% | 09 |

**300-620 DCACI v1.2**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 ACI Fabric Infrastructure | 20% | 03 |
| 2.0 ACI Packet Forwarding | 15% | 03 |
| 3.0 External Network Connectivity | 20% | 03 |
| 4.0 Integrations | 15% | 03, 04 |
| 5.0 ACI Management | 20% | 03, 08 |
| 6.0 ACI Anywhere | 10% | 03 |

**300-635 DCAUTO v1.1**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Network Programmability Foundation | 10% | 06 |
| 2.0 Controller Based Data Center Networking | 30% | 03, 06 |
| 3.0 Data Center Device-centric Networking | 30% | 02, 06 |
| 4.0 Data Center Compute | 30% | 04, 06 |

**300-640 DCAI v1.0**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 AI Fundamentals and Applications | 20% | 07 |
| 2.0 AI Infrastructure Components and Architecture | 30% | 07 |
| 3.0 AI Infrastructure Deployment and Data Management | 30% | 07 |
| 4.0 AI Infrastructure Operations and Troubleshooting | 20% | 07 |

### Study plan

**DCCOR — eight to ten weeks** at 8–10 hours per week, for a reader
with the Volume III routing and switching foundation:

| Week | Focus | Chapters |
| --- | --- | --- |
| 1 | Architecture: platform families, spine-leaf, management planes | 01 |
| 2–3 | **The first heavy block (25%).** NX-OS switching, vPC, overlays: VXLAN EVPN control and data planes, multi-site | 02 |
| 4 | ACI at core depth: policy model, fabric bring-up, contracts | 03 |
| 5–6 | **The second heavy block (25%).** UCS: service profiles, Intersight, firmware, hyperconverged | 04 |
| 7 | Storage networking: FC fabrics, zoning, FCoE, NVMe transport | 05 |
| 8 | Automation and AI: NX-API, model-driven telemetry, tooling, AI-domain basics | 06, 07 |
| 9 | Security: AAA, RBAC, segmentation, hardening across NX-OS, ACI, UCS | 08 |
| 10 | Full-blueprint review weighted to Network and Compute, timed practice | 09 |

Then take **one concentration** within a few months, three to five
weeks each, matched to your role: DCACI for ACI-operating shops (Chapter
03 in depth), DCID for design (35% of it is network design — drill
Chapter 02's topologies), DCIT for operations (its Management and
Operations domain is 20% — Chapter 09), DCAUTO/DCNAUTO for automation
engineers (Chapter 06), or DCAI where AI clusters are landing (Chapter
07).

### Study materials

| Role | Resource | Why |
| --- | --- | --- |
| Official blueprint | [Cisco Learning Network exam topics](https://learningnetwork.cisco.com/s/) | Authority on domains, weights, and version — outranks any third-party material where they disagree |
| Reference text | Cisco Press Official Cert Guide library for DCCOR | Blueprint-ordered; the closest thing to a canonical text |
| Official training | [Cisco U.](https://u.cisco.com/) | Guided paths for every exam in the track, including the only published DCAI training |
| Practice exams | Boson ExSim-Max where available | Closest simulation of Cisco question style, with reasoned explanations |
| Lab | Cisco Modeling Labs for NX-OS; the ACI Simulator and Cisco U. sandboxes for ACI and UCS | Nexus 9000v labs VXLAN EVPN well; ACI and UCS need the simulator and sandboxes — see Practicing |

## Practicing

NX-OS practice is straightforward: the Nexus 9000v image in Cisco
Modeling Labs carries every Chapter 02 topology, including VXLAN EVPN.
ACI practice needs the **ACI Simulator** (a downloadable appliance for
policy-model work — it simulates the fabric, so no data plane) or the
free **Cisco DevNet sandboxes**, which reserve real APIC instances. UCS
practice uses the **UCS Platform Emulator** and the Intersight free
tier. There is no home-lab substitute for AI-cluster hardware; Chapter
07's lab therefore drives design and validation artifacts rather than
GPUs.

## Software and platform baseline

Guidance in this volume is written against the dated baseline in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): NX-OS 10.x on
Nexus 9000, ACI 6.x, UCS Manager 4.x with Intersight as the ascendant
management plane. Where platform behavior differs across trains, the
chapter says so rather than assuming the newest.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format html --volume volume-27-cisco-data-center
```
