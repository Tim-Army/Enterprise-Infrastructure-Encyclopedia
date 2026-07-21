# Volume XVIII — Gigamon Network Visibility

> Deep-dive coverage of the Gigamon GigaVUE visibility fabric: traffic
> acquisition, physical and virtual visibility nodes, centralized fabric
> management, Flow Mapping and tool delivery, GigaSMART traffic
> intelligence, inline bypass and decryption, hybrid cloud automation, and
> day-2 operations.

## Overview

Volume XVIII builds on the network engineering foundations established in
Volume II and applies them to a specific, widely deployed category of
enterprise infrastructure: the dedicated visibility fabric that sits
between the production network and the security and monitoring tool
ecosystem. Where a production network is engineered to move traffic
efficiently from source to destination, a visibility fabric exists for a
different purpose — acquiring a copy (or, for inline security functions,
the traffic itself) once per tap point, and then filtering, transforming,
and delivering it to every tool that needs it, without adding load or
risk to the production network it observes.

The volume is organized to mirror how a Gigamon fabric is actually built,
in dependency order:

- **Chapter 01** establishes the architectural vocabulary — acquisition,
  fabric, and delivery — and the TAP-versus-SPAN and aggregation/
  replication concepts every later chapter assumes.
- **Chapters 02–03** cover first deployment of physical GigaVUE nodes
  (TA Series and HC Series) and virtual/cloud acquisition (GigaVUE V
  Series, the Universal Cloud Tap, and Kubernetes-aware tapping).
- **Chapter 04** covers GigaVUE-FM, the centralized fabric manager, and
  the governance controls (RBAC, directory integration, audit logging)
  that make it a production-grade control plane.
- **Chapters 05–06** cover the two mechanisms that decide what happens to
  acquired traffic: Flow Mapping (ports, maps, GigaStream, tagging) and
  GigaSMART (slicing, masking, deduplication, decryption, application
  metadata).
- **Chapter 07** covers inline deployment — the highest-risk, highest-value
  deployment mode — and the bypass, heartbeat, and decryption mechanisms
  that keep it production-safe.
- **Chapter 08** covers hybrid cloud automation: the GigaVUE-FM REST API,
  Terraform and Ansible integration patterns, and ecosystem integrations
  with SIEM and ITSM platforms.
- **Chapter 09** closes with day-2 operations, a structured
  troubleshooting methodology, the Gigamon Certified Professional
  certification path, and a capstone lab integrating every prior
  chapter's mechanisms into one end-to-end deployment.

Every chapter follows the same structure — learning objectives, theory
and architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md). Each hands-on lab
is a reproducible, disposable exercise with a stated objective,
prerequisites, numbered steps, expected results, a negative test, and
cleanup instructions.

## Chapters

1. [Visibility Architecture, Traffic Acquisition, and Tool Delivery](chapters/01-visibility-architecture-traffic-acquisition-and-tool-delivery.md) — the acquisition/fabric/delivery model, TAP versus SPAN, and N:1 aggregation/1:N replication.
2. [GigaVUE Appliance First Deployment and Fabric Foundations](chapters/02-gigavue-appliance-first-deployment-and-fabric-foundations.md) — TA Series and HC Series platforms, GigaVUE-OS CLI, port addressing, and clustering.
3. [GigaVUE Virtual Nodes and Virtual Traffic Acquisition](chapters/03-gigavue-virtual-nodes-and-virtual-traffic-acquisition.md) — GigaVUE V Series, the Universal Cloud Tap, G-vTAP agents, and Kubernetes-aware acquisition across VMware, AWS, Azure, and private cloud.
4. [GigaVUE-FM Installation, Onboarding, Security, and Governance](chapters/04-gigavue-fm-installation-onboarding-security-and-governance.md) — fabric manager deployment, node onboarding, RBAC, directory integration, licensing, and backup/restore.
5. [Ports, Flow Mapping, Traffic Policy, and Tool Delivery](chapters/05-ports-flow-mapping-traffic-policy-and-tool-delivery.md) — map types, rule priority, first-level/second-level map chaining, GigaStream, and source tagging.
6. [GigaSMART Traffic Intelligence and Packet Transformation](chapters/06-gigasmart-traffic-intelligence-and-packet-transformation.md) — packet slicing, masking, deduplication, header stripping, SSL/TLS decryption, and Application Metadata Intelligence.
7. [Inline Bypass, TLS Decryption, and Production Safety](chapters/07-inline-bypass-tls-decryption-and-production-safety.md) — inline network and tool groups, heartbeat, fail-open/fail-closed, maintenance mode, and Precryption.
8. [Hybrid Cloud Visibility, Automation, APIs, and Integrations](chapters/08-hybrid-cloud-visibility-automation-apis-and-integrations.md) — the GigaVUE-FM REST API, Terraform and Ansible patterns, elastic V Series scaling, and SIEM/ITSM integration.
9. [Operations, Troubleshooting, Training, and Enterprise Capstone](chapters/09-operations-troubleshooting-training-and-enterprise-capstone.md) — day-2 operations, a structured troubleshooting methodology, the Gigamon Certified Professional path, and an integrated capstone lab.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Certification alignment

This volume maps to the **Gigamon Certified Professional (GCP)**
certification, described in more depth in
[Chapter 09](chapters/09-operations-troubleshooting-training-and-enterprise-capstone.md).
Chapters describe the competencies the program validates and point to
Gigamon's official education services; no proprietary exam questions or
licensed courseware are reproduced. Confirm current details against
Gigamon Education Services before planning a study timeline.

### The exam

| Term | Detail |
| --- | --- |
| Format | Multiple choice, scenario-based |
| Passing score | 70% |
| Delivery | Remote proctored — anywhere with connectivity, webcam, and microphone |
| Cost | $250 US per attempt; vouchers available |
| Result | Pass or fail within 48 hours |
| Retakes | Permitted, but each needs a new voucher |
| Validity | **Two years**, then a renewal test focused on what has changed |

**The one weighting Gigamon publishes is unusual and useful.** The test
splits **35% general security, networking, and cloud knowledge** against
**65% Gigamon-specific implementation and configuration**. That ratio is
worth taking seriously in both directions: a third of the exam is not
about Gigamon at all, so a candidate who only knows the product will
struggle, while an experienced network engineer already holds much of
that third and should spend accordingly.

Gigamon states the prerequisite as extensive network security experience
plus product-specific knowledge — the latter normally acquired through
the **GCP Boot Camp**, a five-day instructor-led course with hands-on
labs, offered for a fee through Gigamon Education Services and its
Premium Training Partner network. The certification test is sold
separately and can be taken at the end of day five.

Note that the published certification datasheet carries a 2022 copyright.
It remains the current published document, but treat the figures above as
needing confirmation at registration rather than as freshly restated.

### Practicing without a production fabric

Gigamon has no free interactive lab catalog of the kind Red Hat or VMware
publish, and the hands-on labs that exist sit inside the paid boot camp.
Three routes give genuine console time without one:

| Route | Cost | What it gives you |
| --- | --- | --- |
| [GigaVUE-FM Test Drive](https://www.gigamon.com/lp/fm-test-drive.html) | Free | A hosted GigaVUE-FM with a step-by-step guide covering flow mapping, TLS/SSL decryption, and Application Intelligence — the closest free analogue to a lab |
| AWS Test Drive | Free | A launched environment with emailed access, time-boxed to about three hours per session |
| Trial licensing | Free, own infrastructure | GigaVUE-FM ships a 30-day trial bundle, plus a one-time 60-day 1TB SecureVUE Plus volume-based license from installation |
| [Live demos](https://www.gigamon.com/lp/free-trial.html) | Free | Expert-led sessions for data-center and hybrid-cloud visibility — watching, not driving |

The Test Drive maps most directly onto
[Chapter 04](chapters/04-gigavue-fm-installation-onboarding-security-and-governance.md)
(GigaVUE-FM),
[Chapter 05](chapters/05-ports-flow-mapping-traffic-policy-and-tool-delivery.md)
(flow mapping and tool delivery),
[Chapter 06](chapters/06-gigasmart-traffic-intelligence-and-packet-transformation.md)
(GigaSMART and Application Intelligence), and
[Chapter 07](chapters/07-inline-bypass-tls-decryption-and-production-safety.md)
(TLS decryption).

**The time limits are the constraint to plan around.** Three hours is
enough to follow a guided path, not enough to break something and rebuild
it — which is the loop that actually builds competence. For sustained
practice, the trial licenses on your own virtual infrastructure are the
better route: 30 and 60 days is long enough to deploy a fabric, map
traffic through it, and take it apart deliberately.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): **Gigamon GigaVUE-FM
6.x** (2026-07), with GigaVUE-OS on physical and virtual nodes aligned to
the same release train. GigaVUE-FM and GigaVUE-OS menu paths, CLI keyword
syntax, and REST API structures shown throughout this volume are
representative of the workflow and can vary between releases; validate
against the official documentation for the specific version deployed
before applying configuration to a production fabric.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-18-gigamon-network-visibility

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-18-gigamon-network-visibility/chapters/01-visibility-architecture-traffic-acquisition-and-tool-delivery.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
