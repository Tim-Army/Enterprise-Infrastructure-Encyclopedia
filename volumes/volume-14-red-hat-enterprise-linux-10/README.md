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
