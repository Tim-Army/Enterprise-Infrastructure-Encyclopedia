# Volume XXI — Ubuntu Server and Cloud 26.04 LTS

> Installing, administering, securing, and automating Ubuntu Server
> 26.04 LTS across bare metal, virtualized, and cloud environments,
> using Canonical's native tooling end to end.

## Overview

Volume XXI covers Ubuntu Server 26.04 LTS as a production
infrastructure platform, from first installation through fleet-scale
automation. It assumes the general Linux administration foundation
built in [Volume IV — Enterprise Systems
Administration](../volume-04-enterprise-systems-administration/README.md)
and applies it specifically to the Debian/Ubuntu family: APT instead of
`dnf`, Netplan instead of NetworkManager-first configuration, AppArmor
instead of SELinux, and Canonical's own automation stack (cloud-init,
MAAS, Juju, Landscape) alongside the vendor-neutral tools (Ansible,
Docker, Kubernetes) most fleets already run.

The volume parallels [Volume XIV — Red Hat Enterprise Linux
10](../volume-14-red-hat-enterprise-linux-10/README.md) in structure
and depth, covering the same administrative domains — installation,
shell and package management, boot and service management, identity
and networking, storage, hardening, core services, containers, and
fleet automation — through Ubuntu/Debian-family conventions rather than
Red Hat's.

Chapters build cumulatively:

- **Chapters 01–02** establish installation (interactive and
  unattended), Ubuntu Pro entitlements, the APT repository model, and
  command-line/scripting fluency including Snap package management.
- **Chapters 03–06** cover the operating system core an administrator
  must control before running any workload: boot and systemd, identity
  and network configuration, storage, and AppArmor-based hardening.
- **Chapters 07–08** move to workloads: the common network and
  application services a server exists to run, and the three container
  and orchestration paths Ubuntu Server offers, including practical
  OpenShift interoperability.
- **Chapter 09** closes the volume with Canonical's full automation
  stack — cloud-init, MAAS, Juju, Ansible, and Landscape — and a
  capstone lab combining them into one provisioning-to-operations
  workflow.

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

1. [Installation, Autoinstall, Ubuntu Pro, Repositories, and Landscape](chapters/01-installation-autoinstall-ubuntu-pro-repositories-and-landscape.md) — the Subiquity installer, unattended autoinstall as a cloud-init subset, Ubuntu Pro and ESM, the APT component/pocket model, and Landscape registration.
2. [Essential Tools, Shell Scripting, APT, and Snap Management](chapters/02-essential-tools-shell-scripting-apt-and-snap-management.md) — coreutils and text-processing fluency, production Bash scripting, the APT/dpkg relationship, and Snap channels and confinement.
3. [Boot, systemd, Processes, Logging, and Scheduled Work](chapters/03-boot-systemd-processes-logging-and-scheduled-work.md) — the GRUB/initramfs/systemd boot sequence, unit authoring, cgroups v2, journald/rsyslog logging, and systemd timers vs. cron.
4. [Identity, Privilege, SSH, Netplan, and Firewalling](chapters/04-identity-privilege-ssh-netplan-and-firewalling.md) — users, groups, and sudo; SSH hardening; declarative Netplan configuration; and `ufw`/`nftables` host firewalling.
5. [Storage, LVM, Filesystems, Swap, and Shared-Storage Services](chapters/05-storage-lvm-filesystems-swap-and-shared-storage-services.md) — partitioning and LVM, ext4/XFS/ZFS, zram-based swap, and NFS/Samba/iSCSI.
6. [AppArmor, Permissions, Cryptography, and System Hardening](chapters/06-apparmor-permissions-cryptography-and-system-hardening.md) — AppArmor profile authoring, ACLs and extended attributes, LUKS/TPM2 encryption, and CIS hardening with the Ubuntu Security Guide.
7. [DNS, NTP, DHCP, Web, Database, and Common Server Services](chapters/07-dns-ntp-dhcp-web-database-and-common-server-services.md) — BIND9 and systemd-resolved, chrony, Kea DHCP, Apache2/Nginx with Let's Encrypt, and MariaDB/PostgreSQL.
8. [Docker, LXD, Canonical Kubernetes, and OpenShift Interoperability](chapters/08-docker-lxd-canonical-kubernetes-and-openshift-interoperability.md) — Docker Engine, LXD system containers, Canonical Kubernetes, and building container images that run correctly under OpenShift's default security constraints.
9. [Cloud-init, MAAS, Juju, Ansible, Landscape, Operations, and Capstone](chapters/09-cloud-init-maas-juju-ansible-landscape-operations-and-capstone.md) — cloud-init internals, MAAS bare-metal provisioning, Juju charms and bundles, Ansible fleet management, Landscape operations, and a capstone lab integrating the full stack.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine
  chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Software and platform baseline

Chapters in this volume reference the dated baseline recorded in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): Ubuntu Server /
Cloud 26.04 LTS, plus the current Ansible core baseline used for the
fleet-automation examples in Chapters 02 and 09. Update that file, not
individual chapters, when the baseline changes.

## Building and validating this volume

From the repository root, after completing
[SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-21-ubuntu-server-cloud-26-04-lts

# Build a single chapter.
scripts/bash/build-book.sh --format all \
  --chapter volumes/volume-21-ubuntu-server-cloud-26-04-lts/chapters/01-installation-autoinstall-ubuntu-pro-repositories-and-landscape.md
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
