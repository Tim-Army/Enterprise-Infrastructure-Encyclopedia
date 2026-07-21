# Volume XIV — Red Hat Enterprise Linux 10

> Installing, administering, securing, automating, and operating Red Hat
> Enterprise Linux 10 as an enterprise server platform, aligned to the
> RHCSA (EX200) certification blueprint.

## Overview

Volume XIV is a hands-on, command-line-first treatment of RHEL 10
administration, built for infrastructure engineers who need to install,
configure, secure, and automate RHEL servers in production. It assumes
the general engineering practices from Volume I (version control,
documentation-as-code, automation architecture) and the networking
foundations from Volume II, and applies them specifically to Red Hat's
enterprise Linux distribution.

The volume progresses from a fresh installation to an integrated,
automated, RHCSA-aligned capstone build:

- **Chapters 01–02** cover getting a RHEL 10 system installed,
  registered, and productive: installation methods, subscription and
  repository management, the Cockpit web console, core shell tooling,
  Bash scripting, and `dnf`/`rpm` software management.
- **Chapters 03–05** cover the operating system's runtime foundation:
  the boot sequence and `systemd`, process and log management,
  scheduled work, identity and privilege delegation, SSH, networking
  with NetworkManager, `firewalld`, and the full storage stack from
  partitioning through LVM, filesystems, swap, and shared-storage
  services (NFS/Samba).
- **Chapter 06** covers defense in depth at the OS layer: standard
  permissions and ACLs, SELinux mandatory access control, LUKS
  encryption, system-wide cryptographic policy, and automated
  compliance scanning with OpenSCAP.
- **Chapter 07** covers the common server services layered on top of
  that foundation: `chrony` time synchronization, BIND DNS, Apache
  HTTP Server with TLS, and MariaDB/PostgreSQL.
- **Chapter 08** covers the container and platform layer: Podman's
  daemonless, rootless architecture, Docker CLI compatibility,
  Quadlet systemd integration, and the Kubernetes/OpenShift concepts
  Podman workloads graduate into.
- **Chapter 09** closes the volume with Ansible and RHEL System Roles
  for automating everything covered in Chapters 03–08, culminating in
  an RHCSA-aligned capstone lab that integrates identity, storage,
  SELinux, firewalld, a web service, and scheduled work on a single
  host.

Every chapter follows the same structure — learning objectives, theory
and architecture, design considerations, implementation and
automation, validation and troubleshooting, security and best
practices, references and knowledge checks, a hands-on lab, and a
summary and completion checklist — defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md). Each hands-on
lab is a reproducible, disposable exercise with a stated objective,
prerequisites, numbered steps, expected results, a negative test, and
cleanup instructions.

## Chapters

1. [Installation, Subscriptions, Repositories, and Cockpit](chapters/01-installation-subscriptions-repositories-and-cockpit.md) — Anaconda, Kickstart, and Image Builder installation methods; Red Hat Subscription Management and Simple Content Access; `dnf` repository and module-stream management; installing and securing the Cockpit web console.
2. [Essential Tools, Shell Scripting, and Software Management](chapters/02-essential-tools-shell-scripting-and-software-management.md) — coreutils and the Unix pipeline model; `grep`/`sed`/`awk`/`find`; production-quality Bash scripting; `dnf` and `rpm` package management, history, and rollback.
3. [Boot, systemd, Processes, Logging, and Scheduled Work](chapters/03-boot-systemd-processes-logging-and-scheduled-work.md) — firmware through GRUB2, kernel, and `systemd` as PID 1; unit types and targets; cgroup-aware process control; the `journald` journal; `cron`, `at`, and systemd timers; boot-failure recovery.
4. [Users, Privilege, SSH, Networking, and firewalld](chapters/04-users-privilege-ssh-networking-and-firewalld.md) — local user/group management and password aging; `sudo` and PAM; SSH hardening and key-based authentication; NetworkManager (`nmcli`/`nmtui`); `firewalld` zones, services, and rich rules.
5. [Storage, LVM, Filesystems, Swap, and Shared-Storage Services](chapters/05-storage-lvm-filesystems-swap-and-shared-storage-services.md) — GPT partitioning; the full LVM stack (PV/VG/LV) with live extension and snapshots; XFS and ext4; swap configuration; Stratis and VDO; NFS and Samba sharing; `autofs`.
6. [SELinux, Permissions, Cryptography, and System Hardening](chapters/06-selinux-permissions-cryptography-and-system-hardening.md) — special permission bits and POSIX ACLs; SELinux type enforcement, contexts, booleans, and denial troubleshooting; LUKS disk encryption; system-wide cryptographic policy; OpenSCAP compliance scanning.
7. [DNS, NTP, Web, Database, and Common Server Services](chapters/07-dns-ntp-web-database-and-common-server-services.md) — `chrony` time synchronization; BIND as a caching resolver and authoritative server; Apache virtual hosts and TLS with `mod_ssl`; MariaDB and PostgreSQL installation and hardening.
8. [Podman, Docker Compatibility, Kubernetes, and OpenShift Foundations](chapters/08-podman-docker-compatibility-kubernetes-and-openshift-foundations.md) — Podman's daemonless, rootless, pod-native architecture; Containerfile builds; Docker CLI compatibility; Quadlet systemd integration; core Kubernetes objects; OpenShift Routes, Source-to-Image, Operators, and CRC.
9. [Ansible, System Roles, Operations, and RHCSA Capstone](chapters/09-ansible-system-roles-operations-and-rhcsa-capstone.md) — Ansible's agentless, idempotent architecture; playbooks, roles, templates, and handlers; RHEL System Roles; Ansible Automation Platform; an integrated, RHCSA-aligned capstone lab spanning identity, storage, SELinux, firewalld, services, and scheduled work.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Certification alignment

This volume is mapped to the **Red Hat Certified System Administrator
(RHCSA), exam EX200**, in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md).
Chapters name the blueprint domains a topic supports and point to Red
Hat's official training and certification resources; no proprietary
exam questions or licensed courseware are reproduced anywhere in this
volume. Always confirm the current RHCSA blueprint against Red Hat's
official certification page before using this volume for exam
preparation, since blueprints change independently of this
repository's release cycle.

### The exam is performance-based, and that changes everything

**EX200 is not a multiple-choice exam.** It is performance-based: you are
given a live Red Hat Enterprise Linux system and a set of tasks, and you
are scored on whether the system ends up in the required state. Nothing
is asked about a command; the command either worked or it did not.

The exam is currently based on **Red Hat Enterprise Linux 10**, matching
this volume's baseline. Red Hat states the prerequisites as either the
RH124 and RH134 courses, or the RH199 Rapid Track that combines them, or
comparable production experience. RHCSA is also a hard prerequisite for
both Red Hat Certified Engineer credentials, in Enterprise Linux and in
Ansible.

Three consequences follow, and they should shape preparation more than
any reading list:

- **Reading cannot prepare you.** Every other certification in this
  encyclopedia can be partly passed on recall. This one cannot. Time not
  spent at a shell is close to wasted.
- **Speed is part of the assessment.** Tasks are timed in aggregate.
  Knowing *how* to configure LVM is necessary but not sufficient if it
  takes forty minutes.
- **Practice on a system you can destroy.** The productive loop is break,
  fix, and rebuild — which is what the labs in Chapters 01–09 are already
  built around, and why each carries a cleanup step.

### Mapping this volume to Red Hat interactive labs

Red Hat publishes free browser-based [interactive
labs](https://www.redhat.com/en/interactive-labs/enterprise-linux) — over
fifty for RHEL alone — each a preconfigured environment with a stated
objective, most running ten to twenty minutes. They need a Red Hat
account, which is free, and no subscription.

| Chapter | Topic | Interactive lab |
| --- | --- | --- |
| 01 | Subscriptions and entitlement | *Subscription management basics*; *The remote host configuration tool – rhc* |
| 01 | Web console administration | *Update a Red Hat Enterprise Linux host with the web console* |
| 02 | Package management and streams | *Install software using package managers*; *Manage software from an application stream*; *Extra Packages for Enterprise Linux* |
| 02 | Shell fundamentals | *Helpful Linux commands*; *Unusual unixisms* |
| 02 | Building packages | *Build software into RPM packages* (50 mins) |
| 03 | Services and processes | *Service administration basics* |
| 03 | Performance observation | *Performance Co-Pilot*; *Performance observability in practice with bcc tools*; *Use the web console to monitor performance* |
| 04 | Users, groups, permissions | *Manage user basics*; *Use file permissions* |
| 04 | Networking and firewalls | *Networking basics*; *Configure firewalls with RHEL system roles* |
| 05 | Storage | *Configure system storage with Stratis* |
| 06 | SELinux and containers | *Secure containers with SELinux (Udica)* |
| 06 | Cryptographic policy | *Configure the system-wide cryptographic policy*; *Customize the system-wide cryptographic policy* |
| 06 | Compliance and hardening | *Use OpenSCAP for security compliance and vulnerability scanning*; *Approve applications using file access policy (fapolicyd)*; *Configure terminal session recording* |
| 07 | Databases and services | *Intro to Databases*; *Use system roles to install Microsoft SQL Server* |
| 08 | Containers | *Deploy containers using Podman container tools*; *Create and manage Podman pods*; *Configure a rootless Podman service*; *Build container images with RHEL container tools*; *Create images with container tools (Buildah)* |
| 09 | System roles and automation | *Build a standard operating environment with system roles* |
| 09 | Image building | *Build custom images with Red Hat Image Builder*; *Build machine images with the web console and image builder* |
| — | Unstructured practice | *Red Hat Enterprise Linux open lab* (50 mins) |

**The open lab is the one to return to.** *Red Hat Enterprise Linux open
lab* runs 50 minutes on **RHEL 10 specifically** — the same release EX200
now tests — and gives a system with no prescribed task list. That makes
it the closest free analogue to exam conditions: set yourself an
objective from the RHCSA blueprint and work it unaided. Every other lab
here is guided.

Three labs sit outside RHCSA scope but inside this volume's:
*Introduction to image mode for Red Hat Enterprise Linux* and *Day 2
operations with image mode* cover bootc, and *Red Hat Satellite Basics*
runs two hours on fleet content management.

### Ansible Automation Platform labs

Red Hat publishes a [second lab
collection](https://www.redhat.com/en/interactive-labs/ansible) for
Ansible Automation Platform, on the same free terms. These serve
[Chapter 09](chapters/09-ansible-system-roles-operations-and-rhcsa-capstone.md)
and, past it, the RHCE in Ansible (EX294) that RHCSA gates.

| Topic | Lab |
| --- | --- |
| Command-line entry point | *Get started with ansible-navigator* (30 mins) |
| Execution environments | *Get started with ansible-builder* (45 mins) |
| Controller interface | *Get Started with Automation Controller* (55 mins) |
| Content signing and supply chain | *Sign Ansible Content Collections with private automation hub* (30 mins) |
| Windows targets | *Getting Started with Windows Automation* (55 mins) |
| Event-driven automation | *Get started with Event-Driven Ansible and Ansible Rulebooks* (30 mins); *Event-Driven Ansible controller* (55 mins) |
| ITSM integration | *Get started with ServiceNow automation* (60 mins) |

**These labs reach beyond this volume.** Six *Network automation* labs
run against Cisco IOS XE devices — first playbook, facts, resource
modules, surveys, backup and restore, and infrastructure awareness —
which makes them a practical companion to
[Volume III, Chapter 08](../volume-03-cisco-enterprise-networking/chapters/08-ios-xe-programmability-and-network-automation.md)
on IOS XE programmability, and to
[Volume IX](../volume-09-infrastructure-automation/README.md) generally.
Six more *Hybrid cloud automation* labs cover infrastructure visibility,
cloud operations, and optimization against AWS and Azure, which pair with
[Volume XVII](../volume-17-aws-architecture-security/README.md).

That cross-coverage is worth knowing about: the Ansible lab collection is
the single free resource in this encyclopedia that serves four volumes at
once.

### Other Red Hat practice routes

| Route | Cost | Notes |
| --- | --- | --- |
| Interactive labs | Free, account required | The table above; short, guided, no local setup |
| Developer subscription | Free | Up to 16 nodes for your own lab — see [Chapter 01](chapters/01-installation-subscriptions-repositories-and-cockpit.md) |
| [Developer Sandbox](https://developers.redhat.com/developer-sandbox) | Free | Hosted OpenShift, relevant to [Chapter 08](chapters/08-podman-docker-compatibility-kubernetes-and-openshift-foundations.md) |
| [Red Hat Learning Subscription](https://www.redhat.com/en/services/training/learning-subscription) | Paid, no-cost trial available | RH124, RH134, RH199 and exam attempts bundled |
| RH199 Rapid Track | Paid | Combines RH124 and RH134 for candidates with existing experience |

For a reader with production Linux experience, the developer
subscription plus the interactive labs is a complete free path to
RHCSA-level competence. The Learning Subscription earns its cost mainly
when an exam attempt is bundled or an employer is paying.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): **RHEL 10** as of
2026-07, with Ansible core 2.17/ansible 10.x and Kubernetes 1.31.x
referenced where this volume's automation and container chapters touch
those tools. Update that file, not individual chapters, when the
baseline changes.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-14-red-hat-enterprise-linux-10

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-14-red-hat-enterprise-linux-10/chapters/09-ansible-system-roles-operations-and-rhcsa-capstone.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
