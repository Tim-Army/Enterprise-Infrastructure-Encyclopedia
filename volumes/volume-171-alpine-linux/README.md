# Volume CLXXI — Alpine Linux

> A product deep-dive of **Alpine Linux** — the small, security-oriented, musl-libc/BusyBox
> distribution behind most container base images — taught from install through operation with
> hands-on `apk`, OpenRC, and networking labs, including a full walkthrough for **standing up an
> Alpine host** and for **building a Linux TFTP server** on it, verified against the official Alpine
> wiki and a live Proxmox lab.

## Overview

Volume CLXXI is a **product deep-dive** of **Alpine Linux** — a Linux distribution built on **musl
libc** and **BusyBox** rather than the GNU userland, packaged with the **`apk`** package manager and
init-managed by **OpenRC**. Where a general-purpose server distribution optimizes for
completeness, Alpine optimizes for **size, simplicity, and attack surface**: a minimal install is a
few megabytes, the base image most container ecosystems build on. That same minimalism makes Alpine
the natural choice for the small, single-purpose appliances a homelab and an enterprise edge both
need — a DHCP relay, a jump host, a metrics exporter, or the **TFTP server** this volume builds to
stage firmware images.

This volume sits in the encyclopedia's **operating systems** reading path alongside
[Red Hat Enterprise Linux 10 (XIV)](../volume-014-red-hat-enterprise-linux-10/README.md) and
[Ubuntu Server and Cloud 26.04 LTS (XXI)](../volume-021-ubuntu-server-cloud-26-04-lts/README.md).
It is deliberately complementary to them: RHEL and Ubuntu teach the glibc/systemd server platform
most enterprises standardize on, while Alpine teaches the musl/OpenRC minimal platform those same
enterprises reach for whenever the job is a container image or a purpose-built appliance. Reading
one after the other is the fastest way to internalize *why* the two families differ — dynamic
linker, init system, package manager, and service model all change together.

Chapters follow the platform lifecycle:

- **Chapter 01** frames Alpine's architecture and design philosophy — musl vs. glibc, BusyBox, the
  `apk` model, OpenRC, and where Alpine is and is not the right tool.
- **Chapter 02** installs and provisions Alpine — the install modes (diskless, data, sys), the
  `setup-alpine` script, and cloud-init images on a hypervisor. **(Setup lab.)**
- **Chapter 03** covers **`apk`** package management — repositories, the `world` file, the cache,
  edge, and pinning.
- **Chapter 04** covers networking and service management with **OpenRC** — interfaces, DNS, run
  levels, and boot-time persistence with `local.d`.
- **Chapter 05** builds a **Linux TFTP server** on Alpine end to end — `tftp-hpa`/`in.tftpd`, the
  serving directory, firewalling, and client verification. **(TFTP-server lab.)**
- **Chapter 06** uses Alpine as a **container and appliance base** — the `alpine` image, multi-stage
  builds, and the musl gotchas that surprise people.
- **Chapter 07** operates Alpine over time — updates and release upgrades, growing a root
  filesystem, hardening, backups, and keeping current.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

## Chapters

1. [Alpine Linux Architecture, Philosophy, and Where It Fits](chapters/01-alpine-linux-architecture-philosophy-and-where-it-fits.md) — musl/BusyBox, `apk`, OpenRC, security posture, and when to choose Alpine.
2. [Installing and Provisioning Alpine Linux](chapters/02-installing-and-provisioning-alpine-linux.md) — install modes, `setup-alpine`, disk layout, and cloud-init images on a hypervisor.
3. [Package Management with apk and Repositories](chapters/03-package-management-with-apk-and-repositories.md) — `apk` verbs, main/community/edge, the `world` file, caching, and pinning.
4. [Networking and Service Management with OpenRC](chapters/04-networking-and-service-management-with-openrc.md) — `/etc/network/interfaces`, `resolv.conf`, run levels, `rc-service`/`rc-update`, and `local.d`.
5. [Building a Linux TFTP Server on Alpine](chapters/05-building-a-linux-tftp-server-on-alpine.md) — `tftp-hpa`/`in.tftpd`, the serving directory, permissions, firewall, and client verification.
6. [Alpine as a Container and Appliance Base](chapters/06-alpine-as-a-container-and-appliance-base.md) — the `alpine` image, multi-stage builds, image-size discipline, and musl vs. glibc.
7. [Operating Alpine: Updates, Storage Growth, Hardening, and Keeping Current](chapters/07-operating-alpine-updates-storage-growth-hardening-and-keeping-current.md) — release upgrades, `resize2fs`, `doas`, backups, and staying current.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all seven chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Related volumes

Alpine Linux is a product volume, not a certification-tracks volume; it is not mapped to a single
exam blueprint. The complementary volumes are
[Red Hat Enterprise Linux 10 (XIV)](../volume-014-red-hat-enterprise-linux-10/README.md) and
[Ubuntu Server and Cloud 26.04 LTS (XXI)](../volume-021-ubuntu-server-cloud-26-04-lts/README.md)
for the glibc/systemd server families, [Containers and Platform Engineering (VIII)](../volume-008-containers-platform-engineering/README.md)
for the container ecosystem Alpine base images serve, and
[Proxmox Lab on PowerEdge R640 (XXVI)](../volume-026-proxmox-lab-poweredge-r640/README.md) for the
hypervisor these labs run on. The TFTP server built in Chapter 05 is the firmware-staging host used
by [Volume XIX (Fortinet Network Security), Lab 4.8](../volume-019-fortinet-network-security/chapters/04-fortigate-first-deployment-licensing-management-and-hardening.md).

## Lab coverage

There is **one walkthrough lab for every chapter topic** — the two the reader is most likely to
have come here for are **Chapter 02** (install and provision an Alpine host) and **Chapter 05**
(build a Linux TFTP server). The walkthroughs use real tooling — `setup-alpine`, `apk`, `rc-service`
/`rc-update`, `in.tftpd`, and `resize2fs` — runnable on a small VM (this volume's were validated on
Proxmox VE). Each lab states an objective, prerequisites, numbered steps with expected output, a
negative test, and cleanup, and ends with a `**Lab verified by:** *pending*` sign-off.

## Software and platform baseline

This volume references the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): **Alpine Linux 3.24** (2026-08), with
**BusyBox 1.37.x**, **`apk-tools` 3.x**, and **OpenRC**. Update that file, not individual chapters,
when the baseline changes. Alpine's stable releases are supported for two years; confirm the current
stable release and its end-of-support date on the official
[Alpine releases page](https://alpinelinux.org/releases/) before deploying.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-171-alpine-linux
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
