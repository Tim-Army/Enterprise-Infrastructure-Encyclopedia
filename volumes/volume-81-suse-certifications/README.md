# Volume LXXXI — SUSE Certification Tracks

> The whole SUSE certification program in one volume — the SCA/SCDS/SCE levels across SUSE Linux
> Enterprise Server, SUSE Manager, Rancher/Kubernetes (RKE2/K3s), Longhorn, and NeuVector — with
> hands-on labs (zypper, Snapper rollback, Pacemaker HA, Salt, kubectl/Helm), verified against
> suse.com.

## Overview

Volume LXXXI maps the **SUSE** certification program — the credentials for administering and
engineering SUSE's enterprise open-source portfolio: **SUSE Linux Enterprise Server (SLES)** and the
cloud-native stack of **Rancher** (with the **RKE2** and **K3s** Kubernetes distributions),
**Longhorn** (storage), **NeuVector** (container security), and **SUSE Manager** (fleet management).
The program has three levels — **SUSE Certified Administrator (SCA)**, **SUSE Certified Deployment
Specialist (SCDS)**, and **SUSE Certified Engineer (SCE)** — each tied to a product, delivered via
**Questionmark**. It sits in the encyclopedia's Cloud & platform cluster and beside the other Linux
volumes (RHEL 10 XIV, Ubuntu XXI) and cloud-native volumes (CNCF/Kubernetes XLI, Containers VIII).

This is a **certification-tracks** volume, like the other vendor volumes (XXXIX–LXXX): it maps the
program — the levels and products — and teaches each with a hands-on walkthrough. Every level and
product area was **verified against suse.com on 29 July 2026**.

Chapters follow the portfolio:

- **Chapter 01** frames the program — the SCA/SCDS/SCE levels, the products, and the Questionmark model.
- **Chapters 02–04** take **SLES administration** (the SCA): install/software; storage/filesystem; networking/security/monitoring.
- **Chapter 05** takes the **SCE** advanced SLES (HA, AutoYaST, transactional-update).
- **Chapter 06** takes **SUSE Manager** (patch and config at scale).
- **Chapter 07** takes **Rancher and Kubernetes** (RKE2/K3s).
- **Chapter 08** takes **Longhorn storage and NeuVector security**.
- **Chapter 09** covers certification prep, currency, and career.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

> **Scope.** SUSE administration is authorized systems work. The NeuVector container-security content
> is **defensive** — securing and monitoring authorized clusters, never an attack.

## Chapters

1. [The SUSE Certification Program](chapters/01-the-suse-certification-program.md) — SCA/SCDS/SCE, products, Questionmark.
2. [SLES Administration — Install and Software](chapters/02-sles-administration-install-and-software.md) — zypper, YaST, systemd.
3. [SLES Storage and Filesystem](chapters/03-sles-storage-and-filesystem.md) — Btrfs/Snapper, LVM, rollback.
4. [SLES Networking, Security, and Monitoring](chapters/04-sles-networking-security-and-monitoring.md) — firewalld, AppArmor, journalctl.
5. [SCE — Advanced SLES](chapters/05-sce-advanced-sles.md) — Pacemaker HA, AutoYaST, transactional-update.
6. [SUSE Manager — Patch and Config at Scale](chapters/06-suse-manager-patch-and-config-at-scale.md) — content lifecycle, Salt.
7. [Rancher and Kubernetes](chapters/07-rancher-and-kubernetes.md) — RKE2/K3s, kubectl, Helm, RBAC.
8. [Longhorn Storage and NeuVector Security](chapters/08-longhorn-storage-and-neuvector-security.md) — persistent volumes, defensive runtime protection.
9. [Certification Prep, Currency, and Career](chapters/09-certification-prep-currency-and-career.md) — Questionmark prep, version currency.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume *is* the certification map for SUSE, recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md) and the Master Appendices
course-catalog appendix. Every chapter carries one hands-on walkthrough lab per level/product domain,
verified against suse.com on 29 July 2026.
