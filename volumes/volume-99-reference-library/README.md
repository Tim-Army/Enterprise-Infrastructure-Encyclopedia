# Volume XCIX — Reference Library

> A consolidated, series-wide reference volume: dense lookup tables,
> decision aids, and checklists pulled together from Volumes I through
> XXIII for the reader who needs an answer during real work, not a
> narrative introduction to a topic.

## Overview

Volume XCIX is not a teaching volume. Every other volume in this
encyclopedia introduces a domain, builds understanding of it, and ends
with a hands-on lab that exercises that understanding. Volume XCIX assumes
the reader already has that understanding from the relevant volume and
instead answers a narrower, more urgent question: "what is the port
number," "what does this error mean," "what is the exact syntax," "who do
I escalate to," or "what standard governs this." It is the volume a reader
keeps open in a second window while working, not the volume to read start to
finish before starting.

Because of that purpose, this volume deliberately inverts the usual
balance of its chapters: Theory and Architecture sections are brief, and
the bulk of each chapter is structured reference material — tables,
decision trees, templates, and checklists — designed to be scanned rather
than read in prose. Every chapter still follows the same nine-section
framework as the rest of the encyclopedia (see [Chapter
framework](../../README.md#chapter-framework)), including a hands-on lab,
so that Volume XCIX remains consistent with the series' structure and
validation tooling even though its content is reference-first.

The volume is organized in a rough dependency order, though most chapters
stand alone and can be consulted independently:

- **Chapter 01** establishes the cross-platform command quick-reference
  table and the four safe-administration gates every other chapter's
  guidance assumes.
- **Chapters 02–03** consolidate the foundational facts an engineer needs
  constant access to: ports/protocols/services and traffic flows, and
  addressing/naming/time/identity.
- **Chapters 04–05** consolidate the governance mechanics around change:
  configuration templates and baselines, and the validation/evidence/
  acceptance discipline that closes out a change.
- **Chapter 06** consolidates troubleshooting decision aids and
  escalation practice, drawing on the flow and change vocabulary from the
  prior chapters.
- **Chapters 07–08** consolidate security/risk/incident-response
  reference material and automation/API/integration reference material.
- **Chapter 09** closes the volume — and the encyclopedia — by
  consolidating the standards bodies, certification blueprints, and
  vendor documentation sources that every prior volume's technical claims
  ultimately rest on, and by defining how this reference volume itself
  stays current.

## Chapters

1. [Command Quick Reference and Safe Administration](chapters/01-command-quick-reference-and-safe-administration.md) — cross-platform command mapping (Linux, Windows, Cisco IOS XE, PAN-OS, FortiOS, VMware, AWS) and the four safe-administration gates.
2. [Ports, Protocols, Services, and Traffic Flows](chapters/02-ports-protocols-services-and-traffic-flows.md) — a consolidated port/protocol/service table, IANA port-range taxonomy, and the five-field traffic-flow statement template.
3. [Addressing, Subnetting, Naming, Time, and Identity Reference](chapters/03-addressing-subnetting-naming-time-and-identity-reference.md) — IPv4/IPv6 CIDR tables, RFC 1918 and special-use ranges, DNS/hostname conventions, NTP stratum design, and identity namespace formats (DN, UPN, SPN, ARN).
4. [Configuration Templates, Baselines, and Change Records](chapters/04-configuration-templates-baselines-and-change-records.md) — template placeholder conventions, example templates across platform families, a change-record format, and per-platform drift-detection methods.
5. [Validation, Evidence, Checklists, and Acceptance](chapters/05-validation-evidence-checklists-and-acceptance.md) — the validation-evidence-acceptance pipeline, evidence types by platform, an acceptance checklist template, and the pass/fail/waived disposition model.
6. [Troubleshooting Decision Aids and Escalation](chapters/06-troubleshooting-decision-aids-and-escalation.md) — text-based decision trees for connectivity, performance, and service-availability incidents, a severity/escalation matrix, and an incident timeline format.
7. [Security, Hardening, Incident Response, and Risk Reference](chapters/07-security-hardening-incident-response-and-risk-reference.md) — CIS Benchmark profile levels, the NIST SP 800-61 incident response lifecycle, CVSS severity bands, a likelihood-times-impact risk matrix, and a data classification reference.
8. [Automation, APIs, Data Formats, and Integration Reference](chapters/08-automation-apis-data-formats-and-integration-reference.md) — HTTP methods and status codes, JSON/YAML/XML comparison, an automation-tool comparison, API authentication patterns, and a webhook-integration checklist.
9. [Standards, Certifications, Vendor Documentation, and Reference Governance](chapters/09-standards-certifications-vendor-documentation-and-reference-governance.md) — standards-body and vendor-documentation reference tables, the certification blueprint cross-reference, and the reference-governance discipline that keeps this volume current.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.
- [Master index](../../INDEX.md) and [master glossary](../../GLOSSARY.md)
  — series-wide versions covering all 26 volumes.

## Software and platform baseline

Every version-specific reference in this volume (Cisco IOS XE, PAN-OS,
FortiOS, RHEL, Ubuntu, Kubernetes, Terraform, Ansible, AWS, and other
platform baselines) points to the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md). Update that file, not
individual chapters in this volume, when a baseline changes, and treat
that update as the trigger for reviewing this volume's reference tables
per Chapter 09's governance checklist.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-99-reference-library

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-99-reference-library/chapters/02-ports-protocols-services-and-traffic-flows.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
