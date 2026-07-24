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
| **300-635 DCNAUTO** v2.0 | Automating Cisco Data Center Networking Solutions | 90 min | Concentration — formerly DCAUTO |
| **300-640 DCAI** v1.0 | Implementing Cisco Data Center AI Infrastructure | 90 min | Concentration (specialist, GA 3 February 2026) |

All are delivered through Pearson VUE. Question counts, cut scores, and
pricing are set per exam and are not restated here; confirm them at
registration.

**Two portfolio movements to know about.** DCAI arrived on 3 February
2026 as the newest path to the certification — DCAI plus DCCOR earns
CCNP Data Center. In the same restructure, Cisco rebranded
`300-635 DCAUTO` as `DCNAUTO` with a v2.0 refresh; the code is
unchanged, and Cisco's current lineup lists DCNAUTO as a Data Center
concentration (re-verified 22 July 2026).

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

**300-635 DCNAUTO v2.0** *(formerly DCAUTO v1.1)*

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Network Automation Foundation | 15% | 06 |
| 2.0 Infrastructure as Code | 25% | 06 |
| 3.0 Network Element Programmability | 25% | 03, 06 |
| 4.0 Operations | 25% | 06 |
| 5.0 AI in Automation | 15% | 06, 07 |

**300-640 DCAI v1.0**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 AI Fundamentals and Applications | 20% | 07 |
| 2.0 AI Infrastructure Components and Architecture | 30% | 07 |
| 3.0 AI Infrastructure Deployment and Data Management | 30% | 07 |
| 4.0 AI Infrastructure Operations and Troubleshooting | 20% | 07 |

### Topic-level lab coverage

Every exam topic across **all current Cisco Data Center certifications** — the
DCCOR core, the DCID/DCIT/DCACI/DCNAUTO/DCAI concentrations, and CCIE Data
Center — is covered by a hands-on **walkthrough** lab or a Design Exercise;
the retired **DCSAN 300-625** storage blueprint is covered as well. Topics were
harvested from Cisco's official exam-topics PDFs (`learningcontent.cisco.com`)
in July 2026 — DCCOR/DCID/DCIT/DCACI v1.2, DCNAUTO v2.0, DCAI v1.0, DCSAN v1.0.
Labs use the NX-OS, MDS/FC, APIC (`moquery`/REST), UCS/Intersight, and Nexus
Dashboard/NDFC CLIs and APIs, plus Python/Ansible/Terraform; each carries
`**Lab verified by:** *pending*` until a human runs it. **129 numbered labs**
in total.

**350-601 DCCOR v1.2** maps by domain: Domain 1 (Network) → Chapter 02 Labs
2.1–2.11; Domain 2 (Compute) → Chapter 04 Labs 4.1–4.6; Domain 3 (Storage
Network) → Chapter 05 Labs 5.1–5.4; Domain 4 (Automation and AI) → Chapter 06
Labs 6.1–6.2 and Chapter 07 Lab 7.1; Domain 5 (Security) → Chapter 08 Labs
8.1–8.3.

The implementation and troubleshooting concentrations map one lab per exam
topic; **DCID 300-610 v1.2** (design) is covered by the **Chapter 09 Design
Exercise** reasoning a full data center design from requirements:

**300-620 DCACI v1.2 → Chapter 3** — all six domains

| Exam topic | Lab |
| --- | --- |
| 1.1 Describe ACI architecture | Lab 3.1 |
| 1.2 Describe ACI Object Model | Lab 3.2 |
| 1.3 Utilize faults, events, audit log, and health score | Lab 3.3 |
| 1.4 Describe ACI fabric discovery | Lab 3.4 |
| 1.5 Implement ACI policies | Lab 3.5 |
| 1.6 Implement ACI logical constructs | Lab 3.6 |
| 2.1 Describe endpoint learning | Lab 3.7 |
| 2.2 Implement bridge domain configuration settings such as unicast routing, … | Lab 3.8 |
| 3.1 Implement Layer 2 connectivity (STP/MCP basics and EPG port bindings) | Lab 3.9 |
| 3.2 Implement Layer 3 out (excludes transit routing and VRF route leaking) | Lab 3.10 |
| 4.1 Implement virtual networking integration | Lab 3.11 |
| 4.2 Describe resolution and deployment immediacy in VMM | Lab 3.12 |
| 4.3 Implement service graph | Lab 3.13 |
| 5.1 Implement out-of-band and in-band management | Lab 3.14 |
| 5.2 Utilize traditional and AI-assisted monitoring tools | Lab 3.15 |
| 5.3 Implement configuration backup (snapshot/config import export) | Lab 3.16 |
| 5.4 Implement AAA and RBAC | Lab 3.17 |
| 5.5 Configure an upgrade | Lab 3.18 |
| 6.1 Describe Multi-Pod | Lab 3.19 |
| 6.2 Describe Multi-Site | Lab 3.20 |
| 6.3 Describe Remote Leaf | Lab 3.21 |

**300-625 DCSAN v1.0 → Chapter 5** — Fibre Channel, VSANs, zoning, IVR, DCNM, MDS troubleshooting

| Exam topic | Lab |
| --- | --- |
| 1.1 Describe installation and initial setup (NX-OS, DCNM, POAP) | Lab 5.5 |
| 1.2 Describe secure boot | Lab 5.6 |
| 2.1 Implement Fibre Channel port channels | Lab 5.7 |
| 2.2 Implement Fibre Channel protocol services (Name Service, Cisco Fabric … | Lab 5.8 |
| 2.3 Implement FCoE (FIP, PFC, ETS, DCBX/LLDP) | Lab 5.9 |
| 2.4 Implement VSANs | Lab 5.10 |
| 2.5 Implement NPV and NPIV | Lab 5.11 |
| 2.6 Implement device aliases and zoning | Lab 5.12 |
| 2.7 Configure inter-VSAN routing | Lab 5.13 |
| 2.8 Implement VSAN extensions | Lab 5.14 |
| 3.1 Configure DCNM (DCNM-SAN client, licensing, Device Manager) | Lab 5.15 |
| 3.2 Configure RBAC | Lab 5.16 |
| 3.3 Configure Fibre Channel fabric security | Lab 5.17 |
| 3.4 Describe slow-drain analysis | Lab 5.18 |
| 3.5 Implement SAN telemetry streaming | Lab 5.19 |
| 4.1 Troubleshoot Fibre Channel domains and duplicate domain ID | Lab 5.20 |
| 4.2 Troubleshoot zoning and zone merge failure | Lab 5.21 |
| 4.3 Troubleshoot boot and upgrade issues | Lab 5.22 |

**300-635 DCNAUTO v2.0 → Chapter 6** — YANG, IaC, programmability, operations, AI in automation

| Exam topic | Lab |
| --- | --- |
| 1.1 Describe OpenConfig, IETF, and native YANG models | Lab 6.3 |
| 1.2 Describe ACI-based network-centric mode including objects such as EPG, … | Lab 6.4 |
| 1.3 Describe DPUs in data center network switches | Lab 6.5 |
| 1.4 Describe NETCONF, gNMI, gRPC, and gNOI | Lab 6.6 |
| 1.5 Construct a gRPC payload based on a YANG module using tools such as YANG … | Lab 6.7 |
| 2.1 Describe infrastructure as code (IaC) and GitOps | Lab 6.8 |
| 2.2 Construct network configuration templates with Jinja2 using features such … | Lab 6.9 |
| 2.3 Construct an Ansible playbook with controller and device collections | Lab 6.10 |
| 2.4 Construct a Terraform plan with controller and device providers | Lab 6.11 |
| 2.5 Troubleshoot network automation solutions based on Ansible and Terraform | Lab 6.12 |
| 3.1 Construct a network automation solution with Python using ncclient to … | Lab 6.13 |
| 3.2 Construct a device-level network automation solution for Day-0 provisioning … | Lab 6.14 |
| 3.3 Implement on-box programmability and automation with NX-OS using | Lab 6.15 |
| 3.4 Describe the use of templates and policies in Nexus Dashboard | Lab 6.16 |
| 3.5 Construct network configuration templates with Nexus Dashboard | Lab 6.17 |
| 3.6 Describe capabilities and features of NX-API | Lab 6.18 |
| 4.1 Describe use of network topology simulation related to data center … | Lab 6.19 |
| 4.2 Implement change validation for a network automation solution using pyATS … | Lab 6.20 |
| 4.3 Describe architectural components of model-driven telemetry | Lab 6.21 |
| 4.4 Configure a subscription for model-driven telemetry on NX-OS devices (gNMI … | Lab 6.22 |
| 4.5 Integrate a network automation solution with a network source of truth | Lab 6.23 |
| 4.6 Construct a Python script that retrieves network health data from NX-OS … | Lab 6.24 |
| 4.7 Troubleshoot packet flows for containerized workloads on Linux hosts … | Lab 6.25 |
| 5.1 Describe AI-assisted code development for network automation | Lab 6.26 |
| 5.2 Describe the security risks in a given AI-based network automation solution | Lab 6.27 |
| 5.3 Describe the integration of network devices, controllers, and management … | Lab 6.28 |

**300-640 DCAI v1.0 → Chapter 7** — AI fundamentals, architecture, deployment, operations

| Exam topic | Lab |
| --- | --- |
| 1.1 Describe AI/ML workload types | Lab 7.2 |
| 1.2 Describe the AI lifecycle | Lab 7.3 |
| 1.3 Describe AI use cases | Lab 7.4 |
| 1.4 Describe the types of AI infrastructure | Lab 7.5 |
| 1.5 Describe the components used for AI environments | Lab 7.6 |
| 1.6 Describe Cisco AI solutions | Lab 7.7 |
| 2.1 Evaluate network deployment based on AI workload requirements such as … | Lab 7.8 |
| 2.2 Evaluate compute deployment based on AI workload requirements such as CPU … | Lab 7.9 |
| 2.3 Evaluate storage deployment based on AI workload requirements such as … | Lab 7.10 |
| 2.4 Evaluate power, efficiency, and sustainability based on AI workload … | Lab 7.11 |
| 2.5 Evaluate hybrid AI deployment with cloud integration such as secure … | Lab 7.12 |
| 3.1 Configure high-performance networks to support AI workloads using Cisco … | Lab 7.13 |
| 3.2 Configure high-performance compute and storage to support AI workloads … | Lab 7.14 |
| 3.3 Deploy AI-ready fabrics using Cisco orchestration tools | Lab 7.15 |
| 4.1 Implement benchmarks to evaluate AI infrastructure performance | Lab 7.16 |
| 4.2 Implement monitoring of AI data center infrastructures using Cisco … | Lab 7.17 |
| 4.3 Monitor AI infrastructure using system messages and management tools to … | Lab 7.18 |
| 4.4 Troubleshoot AI infrastructure using system messages and management tools | Lab 7.19 |

**300-615 DCIT v1.2 → Chapter 9** — all five troubleshooting domains

| Exam topic | Lab |
| --- | --- |
| 1.1 Troubleshoot routing protocols | Lab 9.1 |
| 1.2 Troubleshoot switching protocols, such as RSTP+, LACP, and vPC | Lab 9.2 |
| 1.3 Troubleshoot overlay protocols, such as VXLAN EVPN | Lab 9.3 |
| 1.4 Troubleshoot Application Centric Infrastructure | Lab 9.4 |
| 2.1 Troubleshoot Cisco Unified Computing System rack servers | Lab 9.5 |
| 2.2 Troubleshoot Cisco Unified Computing System blade chassis | Lab 9.6 |
| 2.3 Troubleshoot packet flow from server to the fabric | Lab 9.7 |
| 2.4 Troubleshoot hardware interoperability | Lab 9.8 |
| 2.5 Troubleshoot firmware upgrades, packages, and interoperability | Lab 9.9 |
| 3.1 Troubleshoot Fibre Channel physical infrastructure | Lab 9.10 |
| 3.2 Troubleshoot Fibre Channel services | Lab 9.11 |
| 4.1 Troubleshoot automation and scripting tools | Lab 9.12 |
| 4.2 Troubleshoot programmability and orchestration | Lab 9.13 |
| 5.1 Troubleshoot firmware upgrades, packages, and interoperability | Lab 9.14 |
| 5.2 Troubleshoot integration of centralized management such as Nexus Dashboard … | Lab 9.15 |
| 5.3 Troubleshooting network security | Lab 9.16 |
| 5.4 Troubleshoot ACI security domains and role mapping | Lab 9.17 |
| 5.5 Troubleshoot data center compute security | Lab 9.18 |
| 5.6 Troubleshoot storage security | Lab 9.19 |

### CCIE Data Center coverage

The CCIE Data Center **qualifying exam is 350-601 DCCOR**, covered above. The
8-hour hands-on lab (3-hour Design + 5-hour Deploy/Operate/Optimize) applies
the same technologies at expert depth; its focus areas map to this volume:

| CCIE Data Center focus area | Chapters / labs |
| --- | --- |
| Fabric infrastructure (NX-OS, vPC, VXLAN EVPN) | Chapter 02 |
| ACI (policy, forwarding, external, integrations) | Chapter 03 |
| Compute (UCS, Intersight, hyperconverged) | Chapter 04 |
| Storage networking (FC, FCoE, NVMe) | Chapter 05 |
| Automation and programmability | Chapter 06 |
| AI infrastructure (RoCEv2 fabrics, GPU compute) | Chapter 07 |
| Security and segmentation | Chapter 08 |
| Design and troubleshooting under time | Chapter 09 |

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
Operations domain is 20% — Chapter 09), DCNAUTO for automation
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

### CCIE lab readiness

**CCIE Data Center v3.1** sits above the CCNP track, reached by first
passing the `DCCOR 350-601` core. It is an **eight-hour, hands-on
practical exam** in the standard CCIE two-module shape — a **3-hour
Design** module (scenario-based, no device access) and a **5-hour
Deploy, Operate, and Optimize** module — covering the full data center
lifecycle: NX-OS and VXLAN EVPN fabrics, ACI, UCS compute, storage
networking, and automation, with programmability expected throughout.
Cisco is adding a **new AI module** to its CCIE practical exams —
fitting for a track that already gained the DCAI specialist; confirm the
current format at registration.

**What the lab adds over this volume.** These chapters build data
center knowledge and configuration skill at professional depth; the lab
tests **speed, cross-domain integration, and troubleshooting under
time** — building a VXLAN EVPN fabric, an ACI tenant, and UCS service
profiles that interoperate, quickly and correctly, then fixing
deliberately broken scenarios across network, compute, and storage at
once.

**How to prepare.** Rehearse full topologies against the clock in the
lab environments Chapter 01 and the Practicing section describe — Nexus
9000v in Cisco Modeling Labs, the ACI Simulator or DevNet sandboxes for
ACI, and the UCS Platform Emulator for compute — a complete build end to
end, then the same estate broken for you to repair. Pair each chapter's
Hands-On Lab with a timed rebuild, drill the Design module using the
method in [Volume XXX](../volume-30-cisco-ccde-network-design/README.md),
and use Cisco's official CCIE Data Center practice labs before exam day.
Confirm the current lab blueprint and format on the Cisco Learning
Network before scheduling — CCIE lab topics are separate from the
written exam topics and change independently.

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
