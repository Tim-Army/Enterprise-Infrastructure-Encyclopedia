# Volume IV — Enterprise Systems Administration

> Cross-platform Linux and Windows Server administration: the operating
> model, identity, compute, configuration, storage, security, and
> operational disciplines every enterprise systems administrator applies
> regardless of distribution or vendor.

## Overview

Volume IV establishes the cross-platform systems administration
foundation this encyclopedia builds distribution- and vendor-specific
depth on top of. It depends on Volume I (Enterprise Engineering
Foundations) for its automation, documentation, and lifecycle vocabulary,
and it is itself the named dependency for Volume XIV (Red Hat Enterprise
Linux 10), Volume XXI (Ubuntu Server and Cloud 26.04 LTS), Volume XXII
(Dell OpenManage Enterprise), and Volume XXIII (Dell iDRAC 9/10
Administration), per [ROADMAP.md](../../ROADMAP.md).

This volume is deliberately distribution-neutral and vendor-neutral where
Linux and Windows Server share common concepts: process and service
models, identity, configuration management, storage, security automation,
and monitoring. Deep, product-specific administration — RHEL subscription
management and `firewalld` policy authoring, Ubuntu's Snap/Netplan stack,
SAN/NAS array design, hardware out-of-band management — is covered in
their dedicated volumes rather than duplicated here.

The volume is organized in two halves:

- **Chapters 01–04** establish the operating model and platform basics: how
  enterprise administration teams are organized and governed, the shared
  architecture of enterprise Linux, the role-and-feature model of Windows
  Server, and the Active Directory identity fabric both platforms
  ultimately depend on.
- **Chapters 05–09** go deeper into the operational disciplines that span
  both platforms: compute and process/service management, configuration
  and patch management, storage and filesystems, security automation and
  compliance, and monitoring/troubleshooting through decommissioning.

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references
and knowledge checks, a hands-on lab, and a summary and completion
checklist — defined in [templates/chapter.md](../../templates/chapter.md)
and enforced by [EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).
Each hands-on lab is a reproducible, disposable exercise with a stated
objective, prerequisites, numbered steps, expected results, a negative
test, and cleanup instructions.

## Chapters

1. [Systems Administration Architecture and Operating Model](chapters/01-systems-administration-architecture-and-operating-model.md) — centralized, federated, and platform-team operating models; the management plane; ITIL-aligned process mapping; tiered support.
2. [Enterprise Linux Administration](chapters/02-enterprise-linux-administration.md) — the Filesystem Hierarchy Standard, `systemd` as PID 1, DAC/MAC privilege model, LVM, and kernel run-time tuning.
3. [Windows Server Administration](chapters/03-windows-server-administration.md) — the roles-and-features model, Server Core vs. Desktop Experience, the Service Control Manager, PowerShell Remoting, and the Event Log subsystem.
4. [Enterprise Identity and Directory Services](chapters/04-enterprise-identity-and-directory-services.md) — Active Directory Domain Services architecture, FSMO roles, Kerberos/LDAP, Group Policy, and Linux integration with SSSD/realmd.
5. [Compute, Process, and Service Management](chapters/05-compute-process-and-service-management.md) — process lifecycle and CPU scheduling, cgroups v2 and Job Objects, `systemd` dependency chains vs. the Windows SCM, and overlap-safe job scheduling.
6. [Configuration, Software, and Patch Management](chapters/06-configuration-software-and-patch-management.md) — push vs. pull configuration management (Ansible, DSC), golden images, staged patch rings, and drift detection.
7. [Storage, Filesystems, and Data Services](chapters/07-storage-filesystems-and-data-services.md) — filesystem selection (ext4/XFS/Btrfs/NTFS/ReFS), Windows Storage Spaces, NFS and SMB network file services, and quotas/ACLs.
8. [Systems Security, Automation, and Compliance](chapters/08-systems-security-automation-and-compliance.md) — CIS/DISA STIG baselines as code, OpenSCAP scanning, `auditd`/Advanced Audit Policy, and the scan-remediate-rescan loop.
9. [Monitoring, Troubleshooting, and Lifecycle Operations](chapters/09-monitoring-troubleshooting-and-lifecycle-operations.md) — platform-native performance tooling, a structured (USE-method) troubleshooting methodology, log centralization, and full-lifecycle decommissioning.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): Red Hat Enterprise
Linux 10 and Ubuntu Server/Cloud 26.04 LTS as the enterprise Linux
targets (with distribution-specific depth in Volume XIV and Volume XXI),
current Windows Server with PowerShell 7.4+, and Ansible core 2.17 /
`ansible` 10.x for the cross-platform configuration management examples.
Update that file, not individual chapters, when the baseline changes.

## Certification alignment

This volume maps to the entry-level **Cisco Certified Support Technician
(CCST) IT Support** certification, as recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). Chapter
content describes blueprint domains and points to Cisco's official
sources; it does not reproduce proprietary exam content. Always confirm
the current blueprint against Cisco Learning & Certifications before
using a chapter for exam preparation.

### CCST IT Support (100-140)

A **50-minute** entry-level exam covering help-desk and endpoint-support
job tasks. Cisco does not publish domain weights for the CCST exams; the
six domains map to this volume as:

| Domain | Chapters |
| --- | --- |
| 1.0 IT Support Job Tasks and Responsibilities | 01 |
| 2.0 Hardware Issues | 05, 07 |
| 3.0 Connectivity and Resource Access Issues | 04 |
| 4.0 Operating System and Application Issues | 02, 03, 06 |
| 5.0 Common Threats and Preventions | 08 |
| 6.0 Job Tools | 06, 09 |

Two to three weeks at 8–10 hours per week suits a reader with help-desk
exposure. This volume runs deeper than the exam in most domains — it is
written for administrators, not first-line support — so treat the exam
as a checkpoint on the way into the volume rather than the goal of it.
Basic network connectivity questions draw on
[Volume II](../volume-02-network-engineering-foundations/README.md).

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-04-enterprise-systems-administration

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-04-enterprise-systems-administration/chapters/05-compute-process-and-service-management.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
