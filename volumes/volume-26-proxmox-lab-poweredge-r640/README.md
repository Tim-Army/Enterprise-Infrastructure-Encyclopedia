# Volume XXVI — Proxmox Virtualization Lab on Dell PowerEdge R640

> An end-to-end, hands-on build of a single-node virtualization lab on a
> Dell PowerEdge R640: iDRAC out-of-band setup, a BOSS boot mirror and a
> RAID 5 data array, Proxmox VE installation and update, a VLAN-trunked
> network with a management NIC, an ISO library, and a fleet of ten
> virtual machines on tagged VLANs.

## Overview

Volume XXVI is different in character from the reference volumes that
precede it. Where they teach a technology, this volume **builds one
specific thing**, start to finish: it takes a bare Dell PowerEdge R640 and
turns it into a working Proxmox virtualization lab hosting ten virtual
machines across two VLANs. It is an *integration* volume — the
counterpart, for a real build, to
[Volume XIII — Integrated Enterprise Labs](../volume-13-integrated-enterprise-labs/README.md).

It draws on, and assumes, several earlier volumes rather than repeating
them:

- **[Volume XXIII — Dell iDRAC 9 and 10 Administration](../volume-23-dell-idrac-9-10-administration/README.md)**
  for the out-of-band management, BOSS, and RAID configuration this build
  begins with.
- **[Volume XXII — Dell OpenManage Enterprise](../volume-22-dell-openmanage-enterprise/README.md)**
  for the Proxmox-on-PowerEdge context — this volume installs a different
  workload (Proxmox rather than the OME appliance) on the same class of
  hardware.
- **[Volume II — Network Engineering Foundations](../volume-02-network-engineering-foundations/README.md)**
  for the VLANs, trunking, and addressing the network chapter applies.
- **[Volume XIV — Red Hat Enterprise Linux 10](../volume-14-red-hat-enterprise-linux-10/README.md)**
  and
  **[Volume XXI — Ubuntu Server and Cloud 26.04 LTS](../volume-21-ubuntu-server-cloud-26-04-lts/README.md)**
  for the guest operating systems this lab hosts.

The volume follows the build in the order it is actually performed —
hardware and firmware first, then the operating platform, then the network,
then the workloads:

- **Chapters 01–02** bring the hardware up: iDRAC out-of-band access, then
  the storage — a BOSS boot mirror and a six-drive RAID 5 array named
  `river` for virtual machine data.
- **Chapters 03–04** install Proxmox VE onto the boot mirror, switch it to
  the free no-subscription update path, bring it fully current, and point
  it at the gateway for DNS and time.
- **Chapters 05–06** build the network — a dedicated management NIC and a
  VLAN-trunked NIC feeding a VLAN-aware bridge — and the storage layout in
  Proxmox: the `river` datastore for VMs and an ISO repository on it.
- **Chapters 07–08** assemble the ISO library and deploy the ten virtual
  machines, each on its assigned VLAN with its fixed address and hostname.
- **Chapter 09** validates the whole build end to end, troubleshoots the
  failures this kind of build most commonly produces, and closes with
  day-2 operational practice.

Every chapter follows the same structure — learning objectives, theory and
architecture, design considerations, implementation and automation,
validation and troubleshooting, security and best practices, references and
knowledge checks, a hands-on lab, a lab-verification sign-off, and a summary
and completion checklist — defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).

**This volume documents a concrete environment.** The addresses, VLANs, and
hostnames below are specific and real, not placeholders — the labs are
written to be executed exactly as stated on the hardware described. A reader
building a different environment substitutes their own values; the
procedures and reasoning transfer unchanged.

## The environment this volume builds

The target is a single Dell PowerEdge R640. The complete specification the
chapters implement:

### Out-of-band and host management

| Interface | Address | Gateway | Notes |
| --- | --- | --- | --- |
| iDRAC | 10.30.161.25/24 | 10.30.161.1 | Dedicated iDRAC port; out-of-band ([Chapter 01](chapters/01-idrac-out-of-band-access-and-first-configuration.md)) |
| Proxmox management | 10.30.161.10/24 | 10.30.161.1 | Host OS management, dedicated NIC port 0 ([Chapter 05](chapters/05-network-architecture-management-nic-vlan-trunk-and-bridges.md)) |

### Storage

| Volume | Composition | Purpose |
| --- | --- | --- |
| BOSS | 2 × 256 GB SSD, RAID 1 mirror | Proxmox VE boot ([Chapter 02](chapters/02-storage-boss-boot-mirror-and-the-river-raid-5-array.md)) |
| `river` | Front six drives, RAID 5 | Virtual machine storage and the ISO repository ([Chapters 02](chapters/02-storage-boss-boot-mirror-and-the-river-raid-5-array.md), [06](chapters/06-proxmox-storage-the-river-datastore-and-iso-repository.md)) |

### Network

- **Management** — dedicated NIC, **port 0**, host management on
  10.30.161.10/24.
- **Server/VM traffic** — dedicated NIC, **port 1**, configured as an
  **802.1Q trunk**. Allowed VLANs: **3, 6, 10, 200, 202**. All virtual
  machines attach to this NIC through a VLAN-aware bridge.
- DNS, NTP, and other services resolve through the gateway 10.30.161.1.

### Virtual machines

Each VM is deployed from the ISO library on `river`, on its assigned VLAN:

| VM | Hostname | IP | Gateway | VLAN |
| --- | --- | --- | --- | --- |
| Ubuntu Desktop | `ubuntu1` | 10.30.12.100/24 | 10.30.12.1 | 6 |
| Ubuntu Server | `ubuntu-server1` | 10.30.10.100/24 | 10.30.10.1 | 3 |
| EVE-ng | `eve-ng` | 10.30.10.85/24 | 10.30.10.1 | 3 |
| GNS3 | `gns3` | 10.30.10.86/24 | 10.30.10.1 | 3 |
| Cisco CML | `cml` | 10.30.10.87/24 | 10.30.10.1 | 3 |
| Red Hat Desktop | `rhel-desktop1` | 10.30.12.101/24 | 10.30.12.1 | 6 |
| Red Hat Server | `rhel-server1` | 10.30.10.88/24 | 10.30.10.1 | 3 |
| Windows 11 | `win11-1` | 10.30.12.102/24 | 10.30.12.1 | 6 |
| Windows Server | `win-server1` | 10.30.10.89/24 | 10.30.10.1 | 3 |
| NetBox | `netbox` | 10.30.10.62/24 | 10.30.10.1 | 3 |

The VLAN scheme is: **VLAN 6 → 10.30.12.0/24** (desktop workloads) and
**VLAN 3 → 10.30.10.0/24** (server workloads). VLANs 10, 200, and 202 are
carried on the trunk for future use but host no VM in this build.

**NetBox is deployed differently from the other machines.** NetBox
Community Edition is a Django web application, not a bootable
operating-system image — there is no NetBox ISO. It runs on **its own new
Ubuntu Server guest** (built from the Ubuntu Server image already in the
library, with NetBox installed on top), so the Ubuntu Server image serves
two machines much as the single RHEL image serves both Red Hat machines.
See [Chapter 07](chapters/07-building-the-iso-library.md) and
[Chapter 08](chapters/08-deploying-the-virtual-machines.md).

### Corrections applied to the original specification

Two conflicts in the source specification were resolved before this volume
was written, and are recorded here so the build is internally consistent:

- **The server trunk now allows VLAN 3.** The server VMs are tagged VLAN 3,
  but the originally stated trunk allow-list (6, 10, 200, 202) omitted it,
  which would have blocked all server-VLAN traffic. VLAN 3 has been added
  to the allowed list.
- **Windows Server uses 10.30.10.89, not .88.** The original specification
  assigned 10.30.10.88 to both Red Hat Server and Windows Server. Red Hat
  Server keeps .88; Windows Server moves to the next free address, .89.

EVE-ng was not given a VLAN in the source specification; it sits on the
10.30.10.0/24 server subnet and is therefore placed on **VLAN 3** with the
other server-subnet machines.

## Chapters

1. [iDRAC Out-of-Band Access and First Configuration](chapters/01-idrac-out-of-band-access-and-first-configuration.md)
2. [Storage: The BOSS Boot Mirror and the `river` RAID 5 Array](chapters/02-storage-boss-boot-mirror-and-the-river-raid-5-array.md)
3. [Installing Proxmox VE](chapters/03-installing-proxmox-ve.md)
4. [The No-Subscription Repository, Updates, and Core Services](chapters/04-no-subscription-repository-updates-and-core-services.md)
5. [Network Architecture: Management NIC, VLAN Trunk, and Bridges](chapters/05-network-architecture-management-nic-vlan-trunk-and-bridges.md)
6. [Proxmox Storage: The `river` Datastore and ISO Repository](chapters/06-proxmox-storage-the-river-datastore-and-iso-repository.md)
7. [Building the ISO Library](chapters/07-building-the-iso-library.md)
8. [Deploying the Virtual Machines](chapters/08-deploying-the-virtual-machines.md)
9. [Validation, Troubleshooting, and Operations](chapters/09-validation-troubleshooting-and-operations.md)

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across this volume.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this
  volume.

## Related volumes

- **Volume XXIII — Dell iDRAC 9 and 10 Administration** — the out-of-band,
  BOSS, and RAID foundations this build starts from.
- **Volume XXII — Dell OpenManage Enterprise** — Proxmox-on-PowerEdge
  context and the OME appliance as an alternative workload.
- **Volume II — Network Engineering Foundations** — VLANs, trunking, and
  addressing.
- **Volume XIII — Integrated Enterprise Labs** — the integration-volume
  pattern this one follows for a specific build.
- **Volumes XIV and XXI** — the Red Hat and Ubuntu guest operating systems.

## Prerequisites and practicing

**This volume assumes real hardware.** It is written against a physical
Dell PowerEdge R640 with a BOSS card, six front drives, two network
interfaces, and an iDRAC — the equipment the build requires. Unlike the
reference volumes, there is no free or virtual substitute for the hardware
phases (Chapters 01–02): iDRAC, BOSS, and PERC RAID are properties of the
server. A reader without the hardware can still follow the reasoning and
the Proxmox, network, and VM phases (Chapters 03–09) translate to any
Proxmox host, but the storage and out-of-band chapters are hardware-bound
by nature.

Proxmox VE itself is **free and open-source** — the "free version" this
volume activates is simply the no-subscription update repository, which
needs no license ([Chapter 04](chapters/04-no-subscription-repository-updates-and-core-services.md)).

**Guest operating system licensing is honestly mixed**, and
[Chapter 07](chapters/07-building-the-iso-library.md) states it per image:

- **Ubuntu Desktop and Server, EVE-ng, GNS3** — freely downloadable.
- **Red Hat Enterprise Linux** — needs a Red Hat account; the **free Red
  Hat Developer subscription** covers lab use up to a set number of
  systems, which is the route this volume uses.
- **Cisco CML** — **commercial and license-gated**; there is no free
  download, and this volume documents the deployment without redistributing
  the licensed image.
- **Windows 11 and Windows Server** — deployed from Microsoft's
  time-limited **evaluation** ISOs.

## Software and platform baseline

Chapters reference the dated baseline in
[SOFTWARE_VERSIONS.md](../../SOFTWARE_VERSIONS.md): Proxmox VE 9.x on the
R640. Guest OS versions track their own volumes' baselines. Update that
file, not individual chapters, when the baseline changes.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
# Validate structure, links, and Markdown/spelling conventions.
scripts/bash/validate.sh

# Build this volume as a standalone edition.
scripts/bash/build-book.sh --format all \
  --volume volume-26-proxmox-lab-poweredge-r640
```
