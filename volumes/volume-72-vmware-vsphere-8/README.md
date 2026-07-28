# Volume LXXII — VMware vSphere 8

> A product deep-dive of VMware vSphere 8 — ESXi 8 and the Distributed Services Engine (DPU
> offload), vCenter Server 8 with identity federation, vSAN 8 Express Storage Architecture, device
> groups and vGPU, vMotion unified data transport, image-based lifecycle, and Tanzu availability
> zones — emphasizing the changes from vSphere 7, with hands-on esxcli, PowerCLI, and govc labs,
> verified against Broadcom/VMware documentation.

## Overview

Volume LXXII is a **product deep-dive** of **VMware vSphere 8**, the successor to
[Volume LXXI (VMware vSphere 7)](../../volume-71-vmware-vsphere-7/README.md). It teaches the platform
from install through operation with hands-on labs, **emphasizing what changed** from vSphere 7. It
is distinct from [Volume V (VMware Virtualization)](../../volume-05-vmware-virtualization/README.md)
and sits in the encyclopedia's **virtualization** reading path alongside VxRail (XXIV) and the
Proxmox lab (XXVI).

vSphere 8 (GA October 2022) introduced the **vSphere Distributed Services Engine** (DPU/SmartNIC
offload of network/storage/security), the **vSAN 8 Express Storage Architecture** (NVMe-optimized),
**vMotion unified data transport**, **device groups**, new **VM hardware versions**, **Tanzu
workload availability zones**, and image-forward **vLCM** (the last release to support baselines).
All facts were **verified against Broadcom/VMware documentation on 28 July 2026**, including the
Broadcom subscription-licensing model (VMware vSphere Foundation / VMware Cloud Foundation).

Chapters follow the platform, highlighting the 7 → 8 differences:

- **Chapter 01** frames what's new and the **7 → 8 upgrade**.
- **Chapter 02** covers **ESXi 8** and the **Distributed Services Engine (DPU)**.
- **Chapter 03** covers **vCenter Server 8** (identity federation).
- **Chapters 04–06** cover **virtual machines** (device groups/vGPU), **networking** (DPU offload),
  and **storage** (**vSAN 8 ESA**).
- **Chapter 07** covers **resource management and availability** (vMotion unified data transport).
- **Chapter 08** covers **lifecycle, security, and Tanzu** (image-based vLCM, TPM, availability zones).
- **Chapter 09** covers automation, operations, and keeping current.

Every chapter follows the standard structure defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md), including per-topic hands-on labs and
knowledge checks.

## Chapters

1. [vSphere 8 — What's New and the Upgrade from 7](chapters/01-vsphere-8-whats-new-and-upgrade.md) — DPU/DSE, ESA, upgrade order.
2. [ESXi 8 and the Distributed Services Engine](chapters/02-esxi-8-and-distributed-services-engine.md) — install, DPU offload.
3. [vCenter Server 8](chapters/03-vcenter-server-8.md) — VCSA, identity federation, roles, API.
4. [Virtual Machines](chapters/04-virtual-machines.md) — hardware v20/21, device groups, vGPU.
5. [Networking and DPU Offload](chapters/05-networking-and-dpu-offload.md) — vDS 8, DPU-offloaded NSX.
6. [Storage and vSAN 8 Express Storage Architecture](chapters/06-storage-vsan-8-esa.md) — ESA vs OSA, SPBM, NVMe.
7. [Resource Management and Availability](chapters/07-resource-management-and-availability.md) — DRS, HA, vMotion unified data transport.
8. [Lifecycle, Security, and Tanzu](chapters/08-lifecycle-security-and-tanzu.md) — image-based vLCM, TPM, availability zones.
9. [Automation, Operations, and Keeping Current](chapters/09-automation-operations-and-keeping-current.md) — PowerCLI/govc/API, updates, VCF.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all nine chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Related volumes

vSphere 8 is a product volume, not a certification-tracks volume; it is not mapped to a single exam
blueprint. The complementary volumes are [VMware vSphere 7 (LXXI)](../../volume-71-vmware-vsphere-7/README.md),
[VMware Virtualization (V)](../../volume-05-vmware-virtualization/README.md), and, for automation,
[Python for Infrastructure (LVII)](../../volume-57-python-infrastructure-automation/README.md) and
[Ansible (LIX)](../../volume-59-ansible/README.md). The Broadcom/VMware certification catalog is in
the [Master Appendices](../volume-97-master-appendices/README.md).

## Lab coverage

There is **one walkthrough lab for every topic** — **38 labs** across the nine chapters. The
walkthroughs use real tooling — **esxcli** on the host, **PowerCLI**, the open-source **govc**, and
the **vSphere REST API** — runnable on ESXi/vCenter 8 (evaluation) or nested ESXi in a lab, with
DPU/vSAN-ESA topics explained where hardware isn't available. Each lab states an objective,
commands, expected results, a negative test, and cleanup, and ends with a
**`**Lab verified by:** *pending*`** sign-off.

## Software and platform baseline

This volume references **Broadcom/VMware vSphere 8 documentation** (techdocs.broadcom.com), **ESXi
8.0** and **vCenter Server 8.0 (VCSA)**, the **vSphere Distributed Services Engine (DPU)**, **vSAN 8
ESA**, **vSphere Lifecycle Manager**, and **vSphere with Tanzu**, with **esxcli/PowerCLI/govc/
pyvmomi** for automation. All facts were verified against Broadcom/VMware documentation on 28 July
2026; vSphere 8 is delivered under Broadcom's VVF/VCF subscription model, so confirm current builds
and licensing for new work.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-72-vmware-vsphere-8
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
