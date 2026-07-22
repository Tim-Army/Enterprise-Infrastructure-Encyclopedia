# Volume XXVIII — Cisco Collaboration

Collaboration is the enterprise's most user-visible infrastructure:
when calling, meetings, messaging, or the contact center degrade,
everyone knows within minutes. This volume teaches Cisco's
collaboration stack as a discipline — SIP signaling and media, Unified
CM call control, dial plans, gateways and border elements, the
applications layer, Webex cloud and hybrid services, the Expressway
edge, and the contact center — with the operational rigor voice
engineers learned decades ago and cloud services still require.

## Overview

The volume follows a call's life and an estate's evolution. It opens
with architecture and deployment models, grounds SIP signaling and
media negotiation, then builds on-premises call control: Unified CM
foundations, then dial plans, features, and mobility. Gateways and the
Cisco Unified Border Element connect the estate to the PSTN and ITSPs;
the applications chapter adds SSO, messaging and presence, and
voicemail; cloud and edge brings Webex, Expressway, and Mobile and
Remote Access; media resources and QoS keep quality measurable; and
the closing chapter covers the Webex Contact Center, automation APIs,
and certification readiness.

The certification spine is the **CCNP Collaboration** track — the
CLCOR core and its concentrations, including the new cloud
contact-center exam — with every domain mapped in the certification
alignment below.

## Chapters

1. [Collaboration Architecture and the CCNP Collaboration Track](chapters/01-collaboration-architecture-and-the-ccnp-collaboration-track.md)
2. [Signaling and Media: SIP, Codecs, and Endpoints](chapters/02-signaling-and-media-sip-codecs-and-endpoints.md)
3. [Unified CM On-Premises Call Control Foundations](chapters/03-unified-cm-on-premises-call-control-foundations.md)
4. [Dial Plans, Call Control Features, and Mobility](chapters/04-dial-plans-call-control-features-and-mobility.md)
5. [Voice Gateways and the Cisco Unified Border Element](chapters/05-voice-gateways-and-the-cisco-unified-border-element.md)
6. [Collaboration Applications: SSO, Messaging, and Voicemail](chapters/06-collaboration-applications-sso-messaging-and-voicemail.md)
7. [Cloud and Edge: Webex, Expressway, and Mobile and Remote Access](chapters/07-cloud-and-edge-webex-expressway-and-mobile-and-remote-access.md)
8. [Media Resources, Conferencing, and QoS](chapters/08-media-resources-conferencing-and-qos.md)
9. [Contact Center, Automation, and Certification Readiness](chapters/09-contact-center-automation-and-certification-readiness.md)

## Volume resources

- [Index](INDEX.md) — alphabetized topics with chapter pointers
- [Glossary](GLOSSARY.md) — collaboration terminology introduced in
  this volume

## Related volumes

- [Volume II — Network Engineering Foundations](../volume-02-network-engineering-foundations/README.md)
  supplies the IP, DNS, and DHCP behavior every registration and call
  leg depends on.
- [Volume III — Cisco Enterprise Networking](../volume-03-cisco-enterprise-networking/README.md)
  carries the QoS architecture this volume's Chapter 08 applies to
  voice and video.
- [Volume IX — Infrastructure Automation](../volume-09-infrastructure-automation/README.md)
  deepens the API and tooling practices Chapter 09 applies to
  collaboration platforms.

## Certification alignment

This volume maps to the **CCNP Collaboration** certification track, as
recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). CCNP
Collaboration requires the `CLCOR` core exam plus **one** concentration
exam; this volume covers the core and all five concentrations. `CLCOR`
is also the qualifying exam for **CCIE Collaboration**. Chapter content
describes blueprint domains and points to Cisco's official sources; it
does not reproduce proprietary exam questions or licensed courseware.

### The exams

| Exam | Title | Duration | Role in the track |
| --- | --- | --- | --- |
| **350-801 CLCOR** v2.0 | Implementing and Operating Cisco Collaboration Core Technologies | 120 min | Core — required for CCNP Collaboration and CCIE Collaboration |
| **300-810 CLICA** v1.2 | Implementing Cisco Collaboration Applications | 90 min | Concentration |
| **300-815 CLACCM** v1.2 | Implementing Cisco Advanced Call Control and Mobility Services | 90 min | Concentration |
| **300-820 CLCEI** v1.2 | Implementing Cisco Collaboration Cloud and Edge Solutions | 90 min | Concentration |
| **300-830 CLCCE** v1.0 | Implementing Cisco Collaboration Cloud Customer Experience | 90 min | Concentration (new, GA 3 February 2026) |
| **300-835 CLAUTO** v1.1 | Automating and Programming Cisco Collaboration Solutions | 90 min | Concentration — **end-of-life announced** by Cisco under the Automation restructure; confirm availability before scheduling |

All are delivered through Pearson VUE. Question counts, cut scores,
and pricing are set per exam and are not restated here; confirm them
at registration.

### Domain weights, mapped to this volume

**350-801 CLCOR v2.0**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Infrastructure and Design | 15% | 01 |
| 2.0 Protocols and Endpoints | 10% | 02 |
| 3.0 On-Premises Call Control | 30% | 03, 04 |
| 4.0 Voice Gateways and Session Border Controllers | 10% | 05 |
| 5.0 Cloud and Hybrid Services | 25% | 07 |
| 6.0 Media and QoS | 10% | 08 |

**300-810 CLICA v1.2**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Single Sign-On (SSO) for Collaboration Applications | 15% | 06 |
| 2.0 Cisco Unified IM and Presence and Cloud Messaging | 30% | 06 |
| 3.0 Cisco Unity Connection | 30% | 06 |
| 4.0 Application Clients | 25% | 06 |

**300-815 CLACCM v1.2**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Signaling and Media Protocols | 20% | 02 |
| 2.0 Gateway Technologies | 10% | 05 |
| 3.0 Cisco Unified Border Element | 15% | 05 |
| 4.0 Call Control and Dial Planning | 25% | 04 |
| 5.0 Cisco Unified CM Call Control Features | 20% | 04 |
| 6.0 Mobility | 10% | 04 |

**300-820 CLCEI v1.2**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Key Concepts | 25% | 07 |
| 2.0 Initial Expressway Configurations | 25% | 07 |
| 3.0 Mobile and Remote Access | 25% | 07 |
| 4.0 Cisco WebEx Technologies | 25% | 07 |

**300-830 CLCCE v1.0**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Telephony and Call Routing | 30% | 09 |
| 2.0 Tenant Configuration and Reporting | 30% | 09 |
| 3.0 Digital Channels | 15% | 09 |
| 4.0 Advanced Features and AI | 25% | 09 |

**300-835 CLAUTO v1.1** *(EOL announced — see above)*

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Network Programmability Foundation | 10% | 09 |
| 2.0 Unified Communication | 25% | 09 |
| 3.0 Cloud Collaboration | 25% | 09 |
| 4.0 Collaboration Endpoints | 20% | 09 |
| 5.0 Meetings | 20% | 09 |

### Study plan

**CLCOR — eight to ten weeks** at 8–10 hours per week, assuming the
Volume II networking foundation:

| Week | Focus | Chapters |
| --- | --- | --- |
| 1 | Architecture, deployment models, licensing, high availability design | 01 |
| 2 | SIP signaling in depth: transactions, SDP offer/answer, codecs, DTMF | 02 |
| 3–5 | **The heavy block (30%).** Unified CM: registration, users and devices, then dial plans, partitions and calling search spaces, features, SRST | 03, 04 |
| 6 | Gateways and CUBE: PSTN interconnect, ITSP trunking, media handling | 05 |
| 7–8 | **The second block (25%).** Cloud and hybrid: Webex, Expressway pairs, MRA, hybrid services | 07 |
| 9 | Media resources, conferencing, and QoS end to end | 08 |
| 10 | Full-blueprint review weighted to call control and cloud, timed practice | 09 |

Then one concentration within a few months, three to five weeks each,
by role: **CLACCM** for dial-plan-heavy estates (Chapter 04 plus 02
and 05 in depth), **CLICA** for the applications layer (Chapter 06),
**CLCEI** for edge and Webex integration (Chapter 07), **CLCCE** where
Webex Contact Center is landing (Chapter 09) — and treat **CLAUTO** as
schedulable only after confirming Cisco still offers it, given the
announced end-of-life.

### Study materials

| Role | Resource | Why |
| --- | --- | --- |
| Official blueprint | [Cisco Learning Network exam topics](https://learningnetwork.cisco.com/s/) | Authority on domains, weights, and versions — outranks any third-party source |
| Reference text | Cisco Press Official Cert Guide for CLCOR | Blueprint-ordered and thorough |
| Official training | [Cisco U.](https://u.cisco.com/) | Guided paths for the track, including the only published CLCCE preparation |
| Practice exams | Boson ExSim-Max where available | Closest simulation of Cisco question style |
| Lab | CUCM/IM&P/Unity Connection VMs on ESXi or Proxmox; Webex free tier; Expressway trial OVAs | Collaboration labs are appliance VMs — see Practicing |

## Practicing

Cisco distributes Unified CM, IM and Presence, Unity Connection, and
Expressway as virtual appliances; a lab host with 32–64 GB of RAM
(the [Volume XXVI](../volume-26-proxmox-lab-poweredge-r640/README.md)
Proxmox build is ample) runs a complete on-premises estate. Webex and
Webex Contact Center practice uses free-tier and sandbox tenants —
Cisco DevNet's collaboration sandboxes reserve full environments,
including CUCM instances, without local hardware. Softphone endpoints
(Webex App, Jabber) remove the need for physical phones, though one
hardware endpoint teaches registration realities no softphone does.

## Software and platform baseline

Guidance in this volume is written against the dated baseline in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): Unified CM and its
companion applications on the 15.x train, Expressway current, and
Webex as a continuously delivered cloud service — where cloud behavior
drifts from what is printed here, the service's documentation wins.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format html --volume volume-28-cisco-collaboration
```
