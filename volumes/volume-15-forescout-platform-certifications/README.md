# Volume XV — Forescout Platform and Certifications

> Agentless device visibility, classification, compliance, and control on
> the Forescout Platform, from first appliance deployment through
> API-driven automation and OT/ICS-specific sensor design — mapped to the
> FSCA, FSCP, FSCE, FSCA: OT/ICS, and FSCE: OT/ICS certification tracks.

## Overview

Volume XV covers the Forescout Platform as both an enterprise network
access control (NAC) and asset visibility system and as a certification
track in its own right. It has no strict prerequisite volume within this
encyclopedia, though readers unfamiliar with general network engineering
concepts (Volume II) or enterprise cybersecurity fundamentals (Volume X)
will find those volumes useful background.

The volume is organized in three parts:

- **Chapters 01–04** build the enterprise visibility and administration
  foundation: platform architecture and deployment planning, the Console
  and plugin/property model, classification and clarification, and the
  compliance and control policies that turn visibility into governance —
  followed by the host management, RBAC, and reporting practices that
  keep a deployment operable day to day.
- **Chapters 05–07** move to advanced enterprise capability: eyeExtend
  integrations and eyeSegment segmentation modeling, deep troubleshooting
  and resilience design, and the Web API and automation governance that
  close with a full capstone scenario synthesizing the enterprise track.
- **Chapters 08–09** cover the Forescout OT/ICS product line (eyeInspect):
  passive sensor architecture aligned to the Purdue model, industrial
  protocol visibility, and expert-level multi-site deployment, asset
  curation, and OT-appropriate threat detection and control staging.

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

1. [Platform Architecture, Installation, and Deployment Planning](chapters/01-platform-architecture-installation-and-deployment-planning.md) — appliance, Enterprise Manager, and Console architecture; capability-module licensing; discovery mechanisms; and deployment planning and installation sequencing.
2. [Console, Plugins, Properties, and Asset Classification](chapters/02-console-plugins-properties-and-asset-classification.md) — the Console's functional areas, the plugin architecture, built-in versus custom properties, and the classification engine and confidence model.
3. [Clarification, Compliance, and Control Policies](chapters/03-clarification-compliance-and-control-policies.md) — the shared rule/condition/action policy model, clarification policies, compliance policies with grace periods, and staged control-action enforcement.
4. [Host Management, Administration, Inventory, and Reporting](chapters/04-host-management-administration-inventory-and-reporting.md) — inventory groups and tags, Console RBAC, platform administration (health, licensing, backup, updates), and dashboard/report design.
5. [Advanced Policy, Integrations, and Business Outcomes](chapters/05-advanced-policy-integrations-and-business-outcomes.md) — the eyeExtend integration model, SIEM/SOAR/ITSM/vulnerability-management/EDR integration patterns, eyeSegment segmentation modeling, and cross-policy orchestration.
6. [Advanced Troubleshooting, Performance, and Resilience](chapters/06-advanced-troubleshooting-performance-and-resilience.md) — a layered diagnostic model, appliance-level diagnostics, performance tuning drivers, and Enterprise Manager/appliance high availability and disaster recovery.
7. [Expert Automation, API Governance, and Capstone](chapters/07-expert-automation-api-governance-and-capstone.md) — the Forescout Web API, API governance controls, automation patterns, and a multi-site capstone scenario synthesizing Chapters 1–6.
8. [OT/ICS Associate Architecture, Sensors, and Asset Visibility](chapters/08-ot-ics-associate-architecture-sensors-and-asset-visibility.md) — why OT/ICS visibility is a distinct discipline, the Purdue model and eyeInspect sensor placement, and industrial protocol visibility via passive deep packet inspection.
9. [OT/ICS Expert Design, Deployment, Curation, and Troubleshooting](chapters/09-ot-ics-expert-design-deployment-curation-and-troubleshooting.md) — multi-site sensor topology design, asset curation, OT threat detection, and the conservative staged path to OT control capability.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Certification alignment

This volume aligns to the Forescout Technologies certification and
training paths recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md): FSCA,
FSCP, FSCE, FSCA: OT/ICS, and FSCE: OT/ICS. Chapters 1–4 map most
directly to FSCA-level foundational domains, Chapters 5–7 to FSCP/FSCE
enterprise domains, and Chapters 8–9 to the OT/ICS-specific FSCA and FSCE
tracks. This volume describes blueprint domains and points to the
official Forescout training catalog; it does not reproduce proprietary
exam questions or licensed courseware. Always confirm the current
blueprint against Forescout's official certification page before using
this volume for exam preparation.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): Forescout
eyeSight/eyeControl Console 8.5.x, dated 2026-07. Console menu paths and
workflow details can shift between releases; where an exact current UI
path is uncertain, chapters describe the workflow conceptually and note
that it may vary by release rather than asserting a precise, unverifiable
menu path. Update `SOFTWARE_VERSIONS.md`, not individual chapters, when
the baseline changes.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-15-forescout-platform-certifications

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-15-forescout-platform-certifications/chapters/01-platform-architecture-installation-and-deployment-planning.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
