# Volume XXXVI — Windows Server 2025 and Active Directory

> Installing, administering, securing, and automating Windows Server 2025
> and Active Directory Domain Services — from a single domain controller
> to a hybrid, clustered, PowerShell-driven estate joined to Microsoft
> Entra ID and Azure Arc.

## Overview

Volume XXXVI covers **Windows Server 2025** as an enterprise infrastructure
platform and **Active Directory Domain Services (AD DS)** as the identity
foundation most Windows estates are still built on. It is the Windows
counterpart to the Linux platform volumes —
[Volume XIV — Red Hat Enterprise Linux 10](../volume-014-red-hat-enterprise-linux-10/README.md)
and
[Volume XXI — Ubuntu Server and Cloud 26.04 LTS](../volume-021-ubuntu-server-cloud-26-04-lts/README.md) —
and assumes the general systems-administration foundation from
[Volume IV — Enterprise Systems Administration](../volume-004-enterprise-systems-administration/README.md).

The volume treats Windows Server the way a modern administrator actually
runs it: **PowerShell first**, Server Core and Windows Admin Center over
the full desktop where practical, and every on-premises role considered
alongside its **hybrid** extension into Microsoft Entra ID, Azure Arc,
Azure File Sync, and Azure Update Manager. That hybrid framing is not
decoration — it is exactly what the current **Windows Server Hybrid
Administrator** certification (exams **AZ-800** and **AZ-801**) measures,
and the on-premises depth maps to the newer **Windows Server
Administrator** credential.

Chapters build cumulatively:

- **Chapters 01–02** establish the platform: editions and installation,
  Server Core, Windows Admin Center, servicing, and the PowerShell,
  remoting, and Desired State Configuration fluency every later chapter
  relies on.
- **Chapters 03–05** build the identity core: AD DS forests, domains,
  domain controllers and replication; the object model and delegation;
  and Group Policy.
- **Chapters 06–07** cover the network and storage services a server
  estate exists to provide: DNS, DHCP, and IPAM; and Storage Spaces,
  ReFS, deduplication, SMB, and DFS.
- **Chapters 08–09** move to virtualization and availability: Hyper-V and
  Windows containers, then Failover Clustering, Hyper-V Replica, and
  backup for high availability and disaster recovery.
- **Chapters 10–11** close with security and hybrid operations:
  certificate services, gMSA, LAPS, Credential Guard, and Defender; then
  Azure Arc, Entra Connect, Azure File Sync, Storage Migration Service,
  Azure Update Manager, and a capstone that ties the estate together.

Every chapter follows the standard structure — learning objectives,
theory and architecture, design considerations, implementation and
automation, validation and troubleshooting, security and best practices,
references and knowledge checks, a hands-on lab, and a summary and
completion checklist — defined in
[templates/chapter.md](../../templates/chapter.md) and enforced by
[EDITORIAL_STANDARDS.md](../../EDITORIAL_STANDARDS.md).

## Chapters

1. [Windows Server 2025 — Editions, Installation, Server Core, and Windows Admin Center](chapters/01-windows-server-2025-editions-installation-server-core-and-windows-admin-center.md) — the 2025 release and editions, installation options, Server Core versus Desktop Experience, servicing channels, and managing servers with Windows Admin Center.
2. [PowerShell, Remoting, and Desired State Configuration](chapters/02-powershell-remoting-and-desired-state-configuration.md) — cmdlets, objects and the pipeline, PowerShell 7 alongside 5.1, remoting and JEA, modules, and configuration as code with DSC.
3. [Active Directory Domain Services — Forests, Domains, Domain Controllers, and Replication](chapters/03-active-directory-domain-services-forests-domains-domain-controllers-and-replication.md) — the AD DS logical and physical model, installing and promoting domain controllers, FSMO roles, sites, and multi-master replication.
4. [AD DS Objects and Administration — Users, Groups, OUs, Delegation, and Trusts](chapters/04-ad-ds-objects-users-groups-ous-delegation-and-trusts.md) — users, groups and scopes, organizational units, delegated administration, fine-grained password policies, RODCs, and trusts.
5. [Group Policy — Processing, Preferences, Filtering, and the Central Store](chapters/05-group-policy-processing-preferences-filtering-and-the-central-store.md) — GPO structure and processing order, security filtering and WMI filters, preferences, the ADMX central store, and troubleshooting with `gpresult`.
6. [DNS, DHCP, and IP Address Management](chapters/06-dns-dhcp-and-ip-address-management.md) — AD-integrated DNS zones and records, conditional forwarders and DNSSEC, DHCP scopes, failover and policies, and IPAM.
7. [Storage and File Services — Storage Spaces Direct, ReFS, Deduplication, SMB, and DFS](chapters/07-storage-and-file-services-storage-spaces-direct-refs-deduplication-smb-and-dfs.md) — disks and volumes, Storage Spaces and Storage Spaces Direct, ReFS and deduplication, SMB shares and permissions, and DFS Namespaces and Replication.
8. [Hyper-V Virtualization and Windows Containers](chapters/08-hyper-v-virtualization-and-windows-containers.md) — the hypervisor, virtual machines and generations, virtual switches, storage, checkpoints and live migration, and Windows/Hyper-V-isolated containers.
9. [High Availability and Disaster Recovery — Failover Clustering, Hyper-V Replica, and Backup](chapters/09-high-availability-and-disaster-recovery-failover-clustering-hyper-v-replica-and-backup.md) — Failover Clustering, quorum, Cluster Shared Volumes, clustered roles, Hyper-V Replica, and Windows Server Backup.
10. [Security and Identity Hardening — AD CS, gMSA, LAPS, Credential Guard, and Defender](chapters/10-security-and-identity-hardening-ad-cs-gmsa-laps-credential-guard-and-defender.md) — Active Directory Certificate Services, group managed service accounts, Windows LAPS, Credential Guard and protected users, tiering, and Microsoft Defender.
11. [Hybrid Operations and Migration — Azure Arc, Entra Connect, Azure File Sync, Update Manager, and Capstone](chapters/11-hybrid-operations-and-migration-azure-arc-entra-connect-azure-file-sync-update-manager-and-capstone.md) — Azure Arc-enabled servers, Entra Connect and hybrid identity, Azure File Sync, Storage Migration Service, Azure Update Manager, and a provisioning-to-operations capstone.

## Volume resources

- [Index](INDEX.md) — alphabetized topical index across all eleven chapters.
- [Glossary](GLOSSARY.md) — definitions for terms introduced in this volume.

## Certification alignment

This volume maps to Microsoft's **Windows Server** role-based certifications,
as recorded in
[CERTIFICATION_BLUEPRINTS.md](../../CERTIFICATION_BLUEPRINTS.md). It is a
product volume, not a certification-tracks volume — the certification
program beyond Azure is covered in Volume XXXVIII, and Azure itself in
[Volume XXXIII](../volume-033-microsoft-azure-certifications/README.md).

| Certification | Exams | Primarily covered by |
| --- | --- | --- |
| **Windows Server Hybrid Administrator Associate** | AZ-800, AZ-801 | Every chapter; hybrid emphasis in 06–11 |
| **Windows Server Administrator Associate** (beta; on-premises) | *published on Microsoft Learn* | Chapters 01–10 |

**AZ-800 — Administering Windows Server Hybrid Core Infrastructure** maps to
Chapters 03–08 (AD DS, Group Policy, networking, storage, and virtual
machines on-premises and in a hybrid environment). **AZ-801 — Configuring
Windows Server Hybrid Advanced Services** maps to Chapters 09–11 plus
Chapter 10 (security, high availability, disaster recovery, migration, and
monitoring). Confirm the current exam names, numbers, and status on
Microsoft Learn before scheduling — Microsoft retires and renames exams
frequently, and the on-premises Windows Server Administrator credential was
in beta at the time of writing.

## Lab coverage

Every chapter carries a Hands-On Lab of topic-level walkthroughs, one per
major administrative task, mapped to the AZ-800/AZ-801 skills. Each step is
a runnable **PowerShell** command (with Windows Admin Center or GUI noted
where it is the practical path), and each lab states an objective,
prerequisites, expected results with representative output, a negative
test, and cleanup. Each lab ends with a **`**Lab verified by:** *pending*`**
sign-off until a human runs it.

Labs assume a small lab domain — for example `corp.contoso.lab` — built on
the Windows Server 2025 **Evaluation** edition (180-day), which is free to
download and rearm. The reasoning and the PowerShell can be followed
without a live domain, but the sign-off is reserved for an actual run.

## Software and platform baseline

Chapters target **Windows Server 2025** (Standard and Datacenter),
**Windows Admin Center**, **PowerShell 5.1 and PowerShell 7**, **RSAT** for
management from a workstation, and the current **Hyper-V**, **Failover
Clustering**, **AD DS**, **AD CS**, **DNS/DHCP/IPAM**, and **Storage
Spaces** roles and features. Hybrid chapters reference **Microsoft Entra
ID**, **Microsoft Entra Connect**, **Azure Arc**, **Azure File Sync**, and
**Azure Update Manager**. Windows Server is serviced continuously; confirm
current cmdlet syntax, role names, and portal paths against Microsoft
Learn before production use.

## Building and validating this volume

From the repository root, after completing [SETUP.md](../../SETUP.md):

```bash
scripts/bash/validate.sh
```

```bash
scripts/bash/build-book.sh --format all --volume volume-036-windows-server-2025-active-directory
```

See the root [README.md](../../README.md#validation) for the complete
validation and multi-format build reference.
