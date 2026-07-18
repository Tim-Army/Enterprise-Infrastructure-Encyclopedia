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
