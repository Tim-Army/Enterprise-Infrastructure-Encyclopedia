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
exam; this volume covers the core and every concentration blueprint —
the three current ones and the two Cisco retired in February 2026.
`CLCOR`
is also the qualifying exam for **CCIE Collaboration**. Chapter content
describes blueprint domains and points to Cisco's official sources; it
does not reproduce proprietary exam questions or licensed courseware.

### The exams

| Exam | Title | Duration | Role in the track |
| --- | --- | --- | --- |
| **350-801 CLCOR** v2.0 | Implementing and Operating Cisco Collaboration Core Technologies | 120 min | Core — required for CCNP Collaboration and CCIE Collaboration |
| **300-810 CLICA** v1.2 | Implementing Cisco Collaboration Applications | 90 min | **Retired February 2026** — kept for the record |
| **300-815 CLACC** v2.0 | Implementing Cisco Advanced Call Control On-Premises | 90 min | Concentration |
| **300-820 CLHCT** v2.0 | Implementing Cisco Collaboration Hybrid and Cloud Technologies | 90 min | Concentration |
| **300-830 CLCCE** v1.0 | Implementing Cisco Collaboration Cloud Customer Experience | 90 min | Concentration (new, GA 3 February 2026) |
| **300-835 CLAUTO** v1.1 | Automating and Programming Cisco Collaboration Solutions | 90 min | **Retired in the February 2026 restructure** — kept for the record |

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

**300-810 CLICA v1.2** *(retired February 2026 — kept for the record)*

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Single Sign-On (SSO) for Collaboration Applications | 15% | 06 |
| 2.0 Cisco Unified IM and Presence and Cloud Messaging | 30% | 06 |
| 3.0 Cisco Unity Connection | 30% | 06 |
| 4.0 Application Clients | 25% | 06 |

**300-815 CLACC v2.0** *(formerly CLACCM v1.2)*

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Signaling and Media Protocols | 10% | 02 |
| 2.0 Session Border Controller and Voice Gateway Technologies | 30% | 05 |
| 3.0 Advanced Call Control | 25% | 04 |
| 4.0 Supplemental Features and Security | 20% | 04 |
| 5.0 Remote Connectivity and Business to Business Solutions | 15% | 05, 07 |

**300-820 CLHCT v2.0** *(formerly CLCEI v1.2)*

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Suite and Devices Configuration | 25% | 07 |
| 2.0 Cloud Management | 10% | 07 |
| 3.0 Suite and Devices Management | 25% | 07 |
| 4.0 Suite and Device Administration | 10% | 07 |
| 5.0 Hybrid and Migration to the Cloud | 10% | 07 |
| 6.0 Security | 10% | 07 |
| 7.0 APIs and Programmability | 10% | 09 |

**300-830 CLCCE v1.0**

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Telephony and Call Routing | 30% | 09 |
| 2.0 Tenant Configuration and Reporting | 30% | 09 |
| 3.0 Digital Channels | 15% | 09 |
| 4.0 Advanced Features and AI | 25% | 09 |

**300-835 CLAUTO v1.1** *(retired in the February 2026 restructure — kept for the record)*

| Domain | Weight | Chapters |
| --- | --- | --- |
| 1.0 Network Programmability Foundation | 10% | 09 |
| 2.0 Unified Communication | 25% | 09 |
| 3.0 Cloud Collaboration | 25% | 09 |
| 4.0 Collaboration Endpoints | 20% | 09 |
| 5.0 Meetings | 20% | 09 |

### Topic-level lab coverage

Every exam topic across **all current Cisco Collaboration certifications** — the
CLCOR core, the CLACC/CLHCT/CLCCE concentrations, and CCIE Collaboration — is
covered by a hands-on **walkthrough** lab; the retired **CLICA 300-810** and
**CLAUTO 300-835** blueprints are covered as well (kept for the record, and the
subjects of Chapters 06 and 09). Topics were harvested from Cisco's official
exam-topics PDFs (`learningcontent.cisco.com`) in July 2026 — CLCOR/CLACC/CLHCT
v2.0, CLCCE v1.0, CLICA v1.2, CLAUTO v1.1. Labs use the Unified CM CLI/AXL, IOS
XE (CUBE/voice), Expressway, Webex Control Hub and REST APIs, Webex Contact
Center, and device xAPI; each carries `**Lab verified by:** *pending*` until a
human runs it. **141 numbered labs** in total.

**350-801 CLCOR v2.0** maps by domain: Domain 1 (Infrastructure and Design) and
Domain 2 (Protocols and Endpoints) → Chapter 02 Labs 2.1–2.8; Domain 3
(On-Premises Call Control) → Chapter 03 Labs 3.1–3.7; Domain 4 (Voice Gateways
and SBC) → Chapter 05 Labs 5.1–5.3; Domain 5 (Cloud and Hybrid Services) →
Chapter 07 Labs 7.1–7.10; Domain 6 (Media and QoS) → Chapter 08 Labs 8.1–8.4.

**300-815 CLACC v2.0** maps by domain: Domains 1 (Signaling and Media) and 2
(SBC and Voice Gateway) → Chapter 05 Labs 5.4–5.10; Domain 3 (Advanced Call
Control) and Domain 4 (Supplemental Features and Security) → Chapter 04 Labs
4.1–4.7; Domain 5 (Remote Connectivity and B2B) → Chapter 07 Labs 7.35–7.41.

The remaining concentrations map one lab per exam topic:

**300-820 CLHCT v2.0 → Chapter 07**

| Exam topic | Lab |
| --- | --- |
| 1.1 Configure SSO | Lab 7.11 |
| 1.2 Configure directory synchronization | Lab 7.12 |
| 1.3 Configure hybrid calendar service using cloud mail services | Lab 7.13 |
| 1.4 Configure local gateways | Lab 7.14 |
| 1.5 Configure site survivability | Lab 7.15 |
| 1.6 Configure Control Hub calling features such as hot desking or auto … | Lab 7.16 |
| 2.1 Troubleshoot cloud user management | Lab 7.17 |
| 2.2 Diagnose network issues such as bandwidth and QoS when using Webex Suite … | Lab 7.18 |
| 3.1 Troubleshoot Webex Calling | Lab 7.19 |
| 3.2 Troubleshoot call routing in Webex Calling | Lab 7.20 |
| 3.3 Troubleshoot cloud meetings | Lab 7.21 |
| 3.4 Troubleshoot cloud messages | Lab 7.22 |
| 3.5 Troubleshoot endpoint registration to the cloud | Lab 7.23 |
| 4.1 Describe the administration functions in Webex | Lab 7.24 |
| 4.2 Describe AI features in cloud collaboration solutions | Lab 7.25 |
| 4.3 Describe the Control Hub migration tool options from on-premises to cloud | Lab 7.26 |
| 5.1 Configure hybrid and migration from on-premises to cloud | Lab 7.27 |
| 5.2 Configure advance dial plans | Lab 7.28 |
| 6.1 Implement security such as administration, endpoints, meetings, and … | Lab 7.29 |
| 6.2 Describe the Webex cloud security realm architecture | Lab 7.30 |
| 6.3 Configure hybrid data security deployment model | Lab 7.31 |
| 7.1 Describe App Hub, Developer Portal, and Room OS Portal | Lab 7.32 |
| 7.2 Describe macros on devices | Lab 7.33 |
| 7.3 Construct Webex Messaging, Meeting, Calling, People, and Events APIs | Lab 7.34 |

**300-830 CLCCE v1.0 → Chapter 09**

| Exam topic | Lab |
| --- | --- |
| 1.1 Describe Webex Contact Center telephony architecture options | Lab 9.1 |
| 1.2 Configure Webex Contact Center telephony integration via: | Lab 9.2 |
| 1.3 Configure inbound and outdial telephony options for Webex Contact Center … | Lab 9.3 |
| 1.4 Configure components to route voice calls within Webex Contact Center | Lab 9.4 |
| 1.5 Troubleshoot voice channels | Lab 9.5 |
| 2.1 Describe network requirements for Webex Contact Center | Lab 9.6 |
| 2.2 Configure Webex Contact Center users | Lab 9.7 |
| 2.3 Configure the desktop experience such as desktop layouts and desktop … | Lab 9.8 |
| 2.4 Configure recording | Lab 9.9 |
| 2.5 Configure visualizations and dashboards for reports | Lab 9.10 |
| 3.1 Configure components to route digital contacts within Webex Contact Center | Lab 9.11 |
| 3.2 Troubleshoot digital channels such as chat, email, SMS, and social | Lab 9.12 |
| 4.1 Configure advanced voice flow design features such as call back, HTTP … | Lab 9.13 |
| 4.2 Configure advanced digital flow design features such as HTTP request, … | Lab 9.14 |
| 4.3 Describe prebuilt and custom connectors | Lab 9.15 |
| 4.4 Describe Webex Contact Center APIs | Lab 9.16 |
| 4.5 Describe AI assistant features such as summarization, topic analytics, … | Lab 9.17 |
| 4.6 Describe Webex AI agent | Lab 9.18 |

**300-810 CLICA v1.2 (retired) → Chapter 06**

| Exam topic | Lab |
| --- | --- |
| 1.1 Describe these types of SSO as they relate to Collaboration | Lab 6.1 |
| 1.2 Describe the SAML SSO login process flow in the context of Cisco … | Lab 6.2 |
| 1.3 Describe these components of SAML 2.0 and later | Lab 6.3 |
| 1.4 Describe SAML SSO configuration | Lab 6.4 |
| 1.5 Describe OAuth 2.0 | Lab 6.5 |
| 2.1 Configure Cisco Unified IM and Presence on-premises | Lab 6.6 |
| 2.2 Troubleshoot Cisco Unified IM and Presence on-premises | Lab 6.7 |
| 3.1 Configure these in Cisco Unity Connection | Lab 6.8 |
| 3.2 Troubleshoot these in Cisco Unity Connection | Lab 6.9 |
| 3.3 Implement toll fraud prevention | Lab 6.10 |
| 3.4 Troubleshoot Cisco Unity Connection integration options with Cisco UCM | Lab 6.11 |
| 3.5 Describe digital networking in multicluster deployments in Cisco Unity … | Lab 6.12 |
| 4.1 Configure DNS for service discovery | Lab 6.13 |
| 4.2 Troubleshoot service discovery | Lab 6.14 |
| 4.3 Troubleshoot Cisco Jabber and Webex App phone control | Lab 6.15 |
| 4.4 Troubleshoot Cisco Jabber and Webex App voicemail integration | Lab 6.16 |
| 4.5 Troubleshoot certificate validation | Lab 6.17 |
| 4.6 Describe the Cisco Unified Attendant Console Advanced integration | Lab 6.18 |
| 4.7 Troubleshoot Webex App functions | Lab 6.19 |

**300-835 CLAUTO v1.1 (retired) → Chapter 09**

| Exam topic | Lab |
| --- | --- |
| 1.1 Utilize common version control operations with Git (add, clone, push, … | Lab 9.19 |
| 1.2 Describe characteristics of API styles (REST, RPC, and SOAP) | Lab 9.20 |
| 1.3 Describe the challenges encountered and patterns used when consuming APIs … | Lab 9.21 |
| 1.4 Interpret Python scripts containing data types, functions, classes, … | Lab 9.22 |
| 1.5 Describe the benefits of Python virtual environments | Lab 9.23 |
| 1.6 Identify the roles of load balancer, firewall, DNS, and reverse proxy in … | Lab 9.24 |
| 2.1 Construct API calls to automate Cisco UCM user/phone moves, adds, … | Lab 9.25 |
| 2.2 Construct API calls to automate Cisco UCM dial plan and cluster config … | Lab 9.26 |
| 2.3 Describe the capabilities and use of the Cisco UCM CTI APIs TAPI/JTAPI | Lab 9.27 |
| 2.4 Describe the capabilities and use of the Cisco UCM Serviceability Perfmon … | Lab 9.28 |
| 2.5 Describe the capabilities and use of the IP Phone Services API | Lab 9.29 |
| 2.6 Describe the capabilities of Finesse REST APIs and Gadgets | Lab 9.30 |
| 3.1 Describe Webex REST API capabilities, use, application architectures, … | Lab 9.31 |
| 3.2 Implement administrative operations on Webex organizations, users, … | Lab 9.32 |
| 3.3 Construct a Python script to automate creation of Webex spaces and … | Lab 9.33 |
| 3.4 Construct a Python script to implement notification | Lab 9.34 |
| 3.5 Construct API calls to implement interactive bots (including buttons and … | Lab 9.35 |
| 3.6 Describe Webex bots, embedded apps, guest issuer apps, and integrations | Lab 9.36 |
| 3.7 Create a web application embedding Webex and messaging using Webex Widgets | Lab 9.37 |
| 3.8 Describe the capabilities and use for the various Webex Teams SDKs | Lab 9.38 |
| 4.1 Construct API calls to automate Cisco collaboration room devices direct … | Lab 9.39 |
| 4.2 Construct a script to monitor Cisco collaboration room device events … | Lab 9.40 |
| 4.3 Describe the capabilities, use, creation, and deployment of custom … | Lab 9.41 |
| 4.4 Describe the capabilities, use, creation, and deployment of Cisco … | Lab 9.42 |
| 5.1 Describe Webex Meetings REST API capabilities and use to manage meetings … | Lab 9.43 |
| 5.2 Construct REST API calls to implement meetings management for Webex … | Lab 9.44 |
| 5.3 Construct REST API calls to configure Cisco Meeting Server | Lab 9.45 |

### CCIE Collaboration coverage

The CCIE Collaboration **qualifying exam is 350-801 CLCOR**, covered above. The
8-hour hands-on lab applies the same technologies at expert depth; its focus
areas map to this volume:

| CCIE Collaboration focus area | Chapters / labs |
| --- | --- |
| Infrastructure, protocols, and endpoints | Chapters 02, 08 |
| On-premises call control and dial plans | Chapters 03, 04 |
| Voice gateways and CUBE (SBC) | Chapter 05 |
| Collaboration applications (IM&P, Unity, SSO) | Chapter 06 |
| Cloud, hybrid, Expressway, and MRA/B2B | Chapter 07 |
| Contact center and automation/programmability | Chapter 09 |

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
by role: **CLACC** for dial-plan-heavy estates (Chapter 04 plus 02
and 05 in depth), **CLHCT** for Webex and hybrid estates (Chapter 07),
**CLCCE** where Webex Contact Center is landing (Chapter 09). **CLICA**
and **CLAUTO** were retired by Cisco in February 2026; their material
(Chapters 06 and 09) still serves CLCOR's applications domain and
day-to-day operations.

### Study materials

| Role | Resource | Why |
| --- | --- | --- |
| Official blueprint | [Cisco Learning Network exam topics](https://learningnetwork.cisco.com/s/) | Authority on domains, weights, and versions — outranks any third-party source |
| Reference text | Cisco Press Official Cert Guide for CLCOR | Blueprint-ordered and thorough |
| Official training | [Cisco U.](https://u.cisco.com/) | Guided paths for the track, including the only published CLCCE preparation |
| Practice exams | Boson ExSim-Max where available | Closest simulation of Cisco question style |
| Lab | CUCM/IM&P/Unity Connection VMs on ESXi or Proxmox; Webex free tier; Expressway trial OVAs | Collaboration labs are appliance VMs — see Practicing |

### CCIE lab readiness

**CCIE Collaboration v3.1** sits above the CCNP track, reached by first
passing the `CLCOR 350-801` core. It is an **eight-hour, hands-on
practical exam** in the standard CCIE two-module shape — a **3-hour
Design** module (scenario-based, no device access) and a **5-hour
Deploy, Operate, and Optimize** module — covering the full collaboration
lifecycle: call control, protocols and endpoints, applications, the
edge, and media, with programmability expected throughout. Cisco is
adding a **new AI module** to its CCIE practical exams — confirm the
current format at registration.

**What the lab adds over this volume.** These chapters build
collaboration knowledge and configuration skill at professional depth;
the lab tests **speed, integration, and troubleshooting under time** —
standing up CUCM, IM&P, Unity Connection, CUBE, and Expressway so they
interoperate (registration, dial plan, MRA, voicemail all working end to
end), quickly, then diagnosing deliberately broken call flows across the
whole estate.

**How to prepare.** Build the complete collaboration estate as virtual
appliances (the Practicing section's CUCM/IM&P/Unity/Expressway VMs, or
DevNet's collaboration sandboxes) and rehearse it against the clock: a
full build with a working call, MRA sign-in, and voicemail end to end,
then the same estate broken for you to fix — reading SIP and diagnosing
by Call-ID as Chapter 02 teaches, at pace. Pair each chapter's Hands-On
Lab with a timed rebuild, drill the Design module using the method in
[Volume XXX](../volume-30-cisco-ccde-network-design/README.md), and use
Cisco's official CCIE Collaboration practice labs before exam day.
Confirm the current lab blueprint and format on the Cisco Learning
Network before scheduling — CCIE lab topics are separate from the
written exam topics and change independently.

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
