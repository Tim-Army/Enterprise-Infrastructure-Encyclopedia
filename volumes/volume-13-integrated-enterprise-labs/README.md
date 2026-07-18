# Volume XIII — Integrated Enterprise Labs

> A capstone lab volume that integrates Volumes I–XII into a single,
> continuous reference environment and exercises it end to end across
> identity, networking, virtualization, cloud, automation, security,
> observability, and resilience.

## Overview

Volume XIII has no new subject matter of its own. Every chapter's core
content is its Hands-On Lab, and every lab builds against one shared,
versioned reference environment — the **Meridian Industrial Group** lab
introduced in Chapter 01 — rather than a fresh, disposable environment per
chapter. Theory sections are deliberately brief scene-setting that ties
back to the volume where a concept was taught in depth; this volume's job
is to make the reader build, break, and fix things across domain
boundaries, not to re-teach any one domain.

Per [ROADMAP.md](../../ROADMAP.md), Volume XIII depends on Volumes I–XII
in full. The table below shows which prior volume each chapter draws on
most directly; most chapters draw on several.

| Chapter | Primary prior-volume dependencies |
| --- | --- |
| 01 — Lab Engineering, Safety, Reproducibility, and Evidence | Volume I (Chapters 02–03, 08), Volume XII (Chapter 01) |
| 02 — Integrated Identity, DNS, Time, and Core Services Lab | Volume II (Chapter 05), Volume IV (Chapters 02–04), Volume X (Chapter 02) |
| 03 — Campus, WAN, Wireless, and Network Services Lab | Volume II (Chapters 03–04, 06–07), Volume III (Chapters 02–05) |
| 04 — Virtualization, Storage, and Data Protection Lab | Volume V (Chapters 02–04, 06–07), Volume VI (Chapters 05–07) |
| 05 — Hybrid Cloud, Kubernetes, and Platform Services Lab | Volume VII (Chapters 02–04, 07), Volume VIII (Chapters 02, 04, 08) |
| 06 — Infrastructure as Code and Automated Delivery Lab | Volume I (Chapter 03), Volume IX (Chapters 02–03, 05–06, 08) |
| 07 — Zero Trust, Detection, and Incident Response Lab | Volume III (Chapter 07), Volume X (Chapters 02, 04, 06–07) |
| 08 — Observability, Operations, and Major-Incident Lab | Volume XI (Chapters 02–03, 05–07) |
| 09 — Enterprise Resilience and Lifecycle Capstone | Volume I (Chapter 08), Volume XII (Chapters 02–07, 09) |

## Chapters

1. [Lab Engineering, Safety, Reproducibility, and Evidence](chapters/01-lab-engineering-safety-reproducibility-and-evidence.md) — the shared reference lab's addressing, naming, and domain plan, a reusable evidence-capture pipeline, and tested snapshot/rollback discipline that every later chapter depends on.
2. [Integrated Identity, DNS, Time, and Core Services Lab](chapters/02-integrated-identity-dns-time-and-core-services-lab.md) — a replicated Active Directory forest, AD-integrated DNS, a single-rooted time hierarchy, DHCP failover, and a domain-joined Linux client, validated against a single domain controller failure.
3. [Campus, WAN, Wireless, and Network Services Lab](chapters/03-campus-wan-wireless-and-network-services-lab.md) — a resilient HSRP core pair, an HQ–BR1 WAN link with OSPF and IPsec, a branch RODC, and controller-based wireless, validated against a core-switch failure.
4. [Virtualization, Storage, and Data Protection Lab](chapters/04-virtualization-storage-and-data-protection-lab.md) — a two-node vSAN cluster with HA/DRS, migration of the volume's existing VMs into managed inventory, a scripted backup workflow, and vSphere Replication to a BR1 DR target.
5. [Hybrid Cloud, Kubernetes, and Platform Services Lab](chapters/05-hybrid-cloud-kubernetes-and-platform-services-lab.md) — a real `CLOUD1` landing zone connected to HQ by VPN, one Kubernetes cluster spanning on-premises and cloud workers, and platform services validated against a hybrid-link failure.
6. [Infrastructure as Code and Automated Delivery Lab](chapters/06-infrastructure-as-code-and-automated-delivery-lab.md) — Terraform and Ansible bringing Chapters 02–05's manual builds under management, a pipeline with plan/apply identity separation, centralized secrets, and a working policy gate.
7. [Zero Trust, Detection, and Incident Response Lab](chapters/07-zero-trust-detection-and-incident-response-lab.md) — 802.1X and default-deny microsegmentation, a SIEM with a baseline-tuned detection rule, and a full detect-contain-eradicate-recover cycle against a simulated intrusion.
8. [Observability, Operations, and Major-Incident Lab](chapters/08-observability-operations-and-major-incident-lab.md) — full-stack metrics, tracing, and alerting; an SLO and multi-window burn-rate alert for the volume's sample application; and a complete major-incident cycle with a telemetry-driven postmortem.
9. [Enterprise Resilience and Lifecycle Capstone](chapters/09-enterprise-resilience-and-lifecycle-capstone.md) — a business impact analysis, a full HQ site-failure chaos exercise, disaster-recovery failover and failback, and a complete, sanitized decommissioning of every system the volume built.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.
- [Master index](../../INDEX.md) and [master glossary](../../GLOSSARY.md)
  — cross-volume references, including back into Volumes I–XII.

## Software and platform baseline

This volume's labs span nearly every platform baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): Cisco IOS XE 17.x for
the campus and WAN build in Chapter 03, VMware vSphere 9.x for Chapter 04,
Kubernetes 1.31.x and current-GA AWS services for Chapter 05, Terraform
1.9.x and Ansible core 2.17/ansible 10.x for Chapter 06, and the same
baseline throughout for the operating systems introduced in earlier
chapters. Update that file, not individual chapters, when the baseline
changes.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-13-integrated-enterprise-labs

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-13-integrated-enterprise-labs/chapters/09-enterprise-resilience-and-lifecycle-capstone.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
