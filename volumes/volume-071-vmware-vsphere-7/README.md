# Volume LXXI — VMware vSphere 7

> A product deep-dive of VMware vSphere 7 — ESXi 7, vCenter Server 7 (appliance-only), virtual
> machines, networking, storage and vSAN, DRS/HA/vMotion, vSphere Lifecycle Manager, security, and
> vSphere with Tanzu — with hands-on esxcli, PowerCLI, and govc labs, verified against Broadcom/
> VMware documentation.

## Overview

Volume LXXI is a **product deep-dive** of **VMware vSphere 7** — the ESXi 7 hypervisor and vCenter
Server 7 platform, taught from install through operation with hands-on labs. It is distinct from
[Volume V (VMware Virtualization)](../../volume-005-vmware-virtualization/README.md) (the broader
VMware volume) and from [Volume LXXII (VMware vSphere 8)](../../volume-072-vmware-vsphere-8/README.md)
(the next release), and sits in the encyclopedia's **virtualization** reading path alongside VxRail
(XXIV) and the Proxmox lab (XXVI).

vSphere 7 (GA April 2020) introduced appliance-only vCenter, image-based **vSphere Lifecycle
Manager**, a rewritten **DRS**, and **vSphere with Tanzu** (Kubernetes on vSphere). It reached
**end of general support on 2 April 2025**, so this volume covers the platform as it stands and
flags the **upgrade to vSphere 8**. All facts were **verified against Broadcom/VMware documentation
on 28 July 2026**, including the Broadcom subscription-licensing context.

Chapters follow the platform:

- **Chapter 01** frames the architecture and what vSphere 7 introduced.
- **Chapter 02** covers **ESXi 7** installation and host configuration.
- **Chapter 03** covers **vCenter Server 7** (VCSA, inventory, SSO, roles).
- **Chapters 04–06** cover **virtual machines**, **networking**, and **storage/vSAN**.
- **Chapter 07** covers **resource management and availability** (DRS/HA/vMotion).
- **Chapter 08** covers **lifecycle, security, and Tanzu**.
- **Chapter 09** covers automation, operations, and keeping current.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

## Chapters

1. [vSphere 7 Architecture and What's New](chapters/01-vsphere-7-architecture-and-whats-new.md) — ESXi/vCenter, vLCM, Tanzu, lifecycle.
2. [ESXi 7 Installation and Host Configuration](chapters/02-esxi-7-installation-and-host-configuration.md) — install, esxcli, networking, NTP.
3. [vCenter Server 7](chapters/03-vcenter-server-7.md) — VCSA, inventory, SSO, roles, API.
4. [Virtual Machines](chapters/04-virtual-machines.md) — hardware versions, Tools, templates, snapshots.
5. [vSphere Networking](chapters/05-vsphere-networking.md) — standard and distributed switches, VLANs, teaming.
6. [vSphere Storage](chapters/06-vsphere-storage.md) — VMFS/NFS, vSAN 7, SPBM, multipathing.
7. [Resource Management and Availability](chapters/07-resource-management-and-availability.md) — DRS, HA, vMotion, EVC.
8. [Lifecycle, Security, and Tanzu](chapters/08-lifecycle-security-and-tanzu.md) — vLCM, lockdown, host profiles, Tanzu.
9. [Automation, Operations, and Keeping Current](chapters/09-automation-operations-and-keeping-current.md) — PowerCLI/govc/API, backup, upgrade.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Related volumes

vSphere 7 is a product volume, not a certification-tracks volume; it is not mapped to a single exam
blueprint. The complementary volumes are [VMware Virtualization (V)](../../volume-005-vmware-virtualization/README.md),
[VMware vSphere 8 (LXXII)](../../volume-072-vmware-vsphere-8/README.md), and, for automation,
[Python for Infrastructure (LVII)](../../volume-057-python-infrastructure-automation/README.md) and
[Ansible (LIX)](../../volume-059-ansible/README.md). The Broadcom/VMware certification catalog is in
the [Master Appendices](../volume-997-master-appendices/README.md).

## Lab coverage

There is **one walkthrough lab for every topic** — **38 labs** across the nine chapters. The
walkthroughs use real tooling — **esxcli** on the host, **PowerCLI**, the open-source **govc**, and
the **vSphere REST API** — runnable on ESXi/vCenter 7 (evaluation) or nested ESXi in a lab. Each lab
states an objective, commands, expected results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **Broadcom/VMware vSphere documentation** (techdocs.broadcom.com), **ESXi
7.0** and **vCenter Server 7.0 (VCSA)**, **vSAN 7**, **vSphere Lifecycle Manager**, and **vSphere
with Tanzu**, with **esxcli/PowerCLI/govc/pyvmomi** for automation. All facts were verified against
Broadcom/VMware documentation on 28 July 2026; vSphere 7 is past general support (2 April 2025), so
confirm interoperability and plan the upgrade to vSphere 8 for new work.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-071-vmware-vsphere-7
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
