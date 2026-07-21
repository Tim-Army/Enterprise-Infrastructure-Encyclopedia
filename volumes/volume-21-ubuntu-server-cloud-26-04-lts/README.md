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

## Certification alignment

Canonical's certification offering is **Canonical Academy**, whose
**SysAdmin** qualification is the track this volume relates to. It is
recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md).
Chapters describe the competencies the exams assess and point to
Canonical's published exam guide; no proprietary assessment content is
reproduced. Confirm current details against Canonical Academy before
planning a study timeline.

### The qualification is four exams, not one

The SysAdmin qualification requires a passing score on **all four** of
the following. They can be taken individually, in any order, and the
badge and certificate are issued through Credly once all four are
complete.

| Exam | Duration | Published domain weights |
| --- | --- | --- |
| Using Linux Terminal | 75 min | Navigating Files and Filesystems 34%; Managing System Resources 33%; Securing Filesystem Access 33% |
| Using Ubuntu Desktop | 90 min | Managing Applications 28%; Configuring Networking Capabilities 25%; Securing Desktop Systems 22%; Installing Ubuntu Desktop 10%; Engaging with the Open Source Community 10% |
| Using Ubuntu Server | 90 min | Deploying Ubuntu Server 27%; Managing Processes 26%; Securing Server Access 24%; Configuring Servers and Services 23% |
| Using DevOps Principles | 90–120 min (estimated) | Understanding Deployment Technologies 34%; Using Tools for Automation and System Updating 32%; Monitoring and Troubleshooting Systems (weight not published) |

**The format is partly hands-on.** Each exam is hybrid — multiple choice,
scenario-based, *and* performance-based, with candidates working in a
virtual system to perform administrative tasks while instructions sit
alongside the environment. Canonical is explicit that this is a
qualification validating occupational competence rather than a
certificate of course completion. Only Red Hat's EX200 goes further in
this direction among the certifications in this encyclopedia.

Canonical publishes a passing score of **70** for the 2024 edition of
*Using Linux Terminal*, and notes that cut scores are set per exam and
may change between editions.

### Two version and scope gaps to plan around

**The exams lag this volume by an LTS cycle.** Canonical states that
exams are based on the LTS running on the test nodes, that the 2024
exams are all built on **24.04 (Noble Numbat)**, and that they will not
change until the 2026 exams arrive for the **26.04** cycle. This volume
is written against 26.04. The gap is mostly immaterial for fundamentals —
filesystem navigation and process management do not change between LTS
releases — but anything this volume covers *because* it is new in 26.04
is by definition not yet examinable. Check which edition you are sitting.

**This volume does not cover Ubuntu Desktop.** *Using Ubuntu Desktop* is
one of the four required exams, and it is out of scope here: this is a
server and cloud volume throughout. A reader pursuing the full SysAdmin
qualification needs separate desktop preparation for roughly a quarter of
the track — installation, application management, and desktop security.

### Mapping the exams to this volume

| Exam | Chapters |
| --- | --- |
| Using Linux Terminal | [02](chapters/02-essential-tools-shell-scripting-apt-and-snap-management.md) (shell and text processing), [03](chapters/03-boot-systemd-processes-logging-and-scheduled-work.md) (logs, scheduled work), [04](chapters/04-identity-privilege-ssh-netplan-and-firewalling.md) (users, SSH keys, sudo), [05](chapters/05-storage-lvm-filesystems-swap-and-shared-storage-services.md) (partitions and filesystems), [06](chapters/06-apparmor-permissions-cryptography-and-system-hardening.md) (ownership and access) |
| Using Ubuntu Server | [01](chapters/01-installation-autoinstall-ubuntu-pro-repositories-and-landscape.md) (deployment and autoinstall), [03](chapters/03-boot-systemd-processes-logging-and-scheduled-work.md) (process management), [04](chapters/04-identity-privilege-ssh-netplan-and-firewalling.md) (server access), [07](chapters/07-dns-ntp-dhcp-web-database-and-common-server-services.md) (services) |
| Using DevOps Principles | [08](chapters/08-docker-lxd-canonical-kubernetes-and-openshift-interoperability.md) (containers and Kubernetes), [09](chapters/09-cloud-init-maas-juju-ansible-landscape-operations-and-capstone.md) (cloud-init, MAAS, Juju, Ansible, Landscape) |
| Using Ubuntu Desktop | Not covered — see the scope gap above |

### A complete training plan for all four exams

Roughly **fourteen weeks at 8–10 hours per week** for the full SysAdmin
qualification, assuming general Linux familiarity. An experienced
administrator can compress the first block considerably; someone new to
Linux should expect closer to twenty.

The order below is deliberate. *Using Linux Terminal* first, because
every other exam assumes it. *Ubuntu Server* second, because it is this
volume's center of gravity. *DevOps Principles* third, because it builds
on server administration. *Ubuntu Desktop* last and separately, because
it is the one exam this volume does not serve.

**Block 1 — Using Linux Terminal (weeks 1–3, 75-minute exam)**

| Week | Domain and weight | Chapters | Focus |
| --- | --- | --- | --- |
| 1 | Navigating Files and Filesystems (34%) | 02 | Terminal navigation, file manipulation, regular expressions, pipes and redirection |
| 2 | Managing System Resources (33%) | 03, 05 | Log locations and rotation, `fdisk`/`fsck`/`parted`, crontab format, reading logs while troubleshooting |
| 3 | Securing Filesystem Access (33%) | 04, 06 | SSH keys, password complexity and expiry, sudo policy, user and group management, ownership and permissions |

The three domains are near-equal, so split time evenly. Sit this exam
before starting Block 2 — it is the cheapest of the four to pass and
confirms your practice environment works.

**Block 2 — Using Ubuntu Server (weeks 4–7, 90-minute exam)**

| Week | Domain and weight | Chapters | Focus |
| --- | --- | --- | --- |
| 4 | Deploying Ubuntu Server (27%) | 01 | Subiquity, autoinstall, Ubuntu Pro entitlements, APT components and pockets |
| 5 | Managing Processes (26%) | 03 | systemd units and targets, cgroups, journald, timers versus cron |
| 6 | Securing Server Access (24%) | 04, 06 | SSH hardening, Netplan, `ufw`/`nftables`, AppArmor profiles |
| 7 | Configuring Servers and Services (23%) | 07 | BIND9 and systemd-resolved, chrony, Kea DHCP, web and database services |

Weights here are flat — 23% to 27% — so no domain dominates. Deployment
edges ahead, which rewards actually installing servers repeatedly rather
than reading about the installer.

**Block 3 — Using DevOps Principles (weeks 8–11, 90–120-minute exam)**

| Week | Domain and weight | Chapters | Focus |
| --- | --- | --- | --- |
| 8 | Understanding Deployment Technologies (34%) | 08 | Docker Engine, LXD system containers, Canonical Kubernetes |
| 9 | Understanding Deployment Technologies, continued | 08, 09 | Juju charms and bundles, MAAS bare-metal provisioning |
| 10 | Tools for Automation and System Updating (32%) | 09, 01, 02 | cloud-init, Ansible, Landscape, unattended upgrades, APT and Snap update paths |
| 11 | Monitoring and Troubleshooting Systems | 03, 09 | Log analysis, service failure diagnosis, fleet health |

The third domain's weight is not published; the other two account for
66%, so treat the remainder as substantial rather than incidental.

**Block 4 — Using Ubuntu Desktop (weeks 12–14, 90-minute exam)**

This volume does not cover Desktop, so this block runs on separate
material — install Ubuntu Desktop in a virtual machine and work through
Canonical's own documentation and tutorials.

| Week | Domain and weight | Focus |
| --- | --- | --- |
| 12 | Managing Applications (28%) and Installing Ubuntu Desktop (10%) | Installation, `apt` and Snap on the desktop, application sources and updates |
| 13 | Configuring Networking Capabilities (25%) | Desktop network configuration, wireless, VPN clients, sharing |
| 14 | Securing Desktop Systems (22%) and Engaging with the Open Source Community (10%) | Desktop hardening and user security; Launchpad, bug reporting, licensing, contribution norms |

**Do not skip the community domain.** *Engaging with the Open Source
Community* is 10% — as heavily weighted as installation — and it is
unlike anything else in the qualification or in this encyclopedia. It
covers how the Ubuntu project actually works: reporting bugs usefully,
Launchpad, licenses, and the norms of contributing. It cannot be inferred
from technical skill, and it is the domain most likely to surprise an
experienced administrator.

**Readiness signals.** Because the exams are partly performance-based,
the useful check is not a practice score but a timed rebuild: provision a
server unattended, harden it, stand up a service, and verify it — inside
the exam's time budget, unaided. If that is comfortable, sit the exam.

### Practicing

Ubuntu shares Wireshark's advantage: the platform is free, so lab access
is not the constraint. Any hypervisor, cloud instance, or spare machine
runs the real thing, and Ubuntu Server installs in minutes with no
license, trial window, or entitlement.

That makes the performance-based half of these exams unusually cheap to
prepare for. Build a virtual machine, work the tasks in each chapter's
lab, then destroy and rebuild it — the same break-and-rebuild loop the
Red Hat volume recommends, with none of the subscription friction.

For the DevOps exam specifically, the tooling in
[Chapter 09](chapters/09-cloud-init-maas-juju-ansible-landscape-operations-and-capstone.md)
— cloud-init, MAAS, Juju, Landscape — is all freely available for
evaluation, though MAAS in particular wants more than one machine to be
worth exercising properly.

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
