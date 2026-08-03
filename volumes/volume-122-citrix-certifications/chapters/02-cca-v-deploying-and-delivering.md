# Chapter 02: CCA-V — Deploying and Delivering Virtual Apps and Desktops

## Learning Objectives

- Map the CCA-V exam's first three modules: deploying CVAD, providing resources, and providing access.
- Understand the CVAD architecture: Delivery Controller, VDA, StoreFront, Studio, Director, Cloud Connector.
- Complete a walkthrough lab per module.

## The exam in brief

**Certification:** Citrix Certified Associate — Virtualization (CCA-V). **Exam:** *Citrix Virtual Apps and Desktops Administration* (replaces the retired 1Y0-204). ~60–65 questions, 90 minutes, ~65% passing, English, no prerequisites. **Recommended course:** CVAD-201 *Citrix Virtual Apps and Desktops Administration (2402 LTSR)*; on-demand equivalents on Pluralsight (CVAD Academy). The exam has nine modules; this chapter covers modules 1–3 and [Chapter 03](03-cca-v-security-monitoring-operations.md) covers modules 4–9.

## Module 1 — Deploying Citrix Virtual Apps and Desktops

The moving parts every CCA-V question assumes:

| Component | Role |
|:---|:---|
| **Delivery Controller** | Brokers sessions, manages the site (on-premises) |
| **Cloud Connector** | The controller's counterpart when the control plane is Citrix Cloud |
| **VDA (Virtual Delivery Agent)** | On every machine that delivers apps/desktops; registers with the controller |
| **StoreFront / Workspace** | The store users authenticate to and launch from |
| **Studio (Web Studio)** | Admin console: machine catalogs, delivery groups, policies |
| **Director** | Help-desk/monitoring console |
| **Site database** | SQL Server; site, config, and monitoring data |

Deployment order: database → controller(s) → Studio → VDA image → StoreFront → test launch. **Machine catalogs** (the pool of machines, MCS- or PVS-provisioned) feed **delivery groups** (what users are entitled to).

## Module 2 — Providing resources to end users

Published **applications**, **desktops** (pooled/static, server/desktop OS), and app **properties** (visibility, icons, categories, file-type association). Provisioning: **MCS** (Machine Creation Services — differencing disks from a master image) versus **PVS** (Provisioning — streamed vDisk).

## Module 3 — Providing access

StoreFront stores, Workspace app deployment, ICA/HDX launch flow (the `.ica` file → HDX session to the VDA), and beacons for internal/external detection.

## Hands-On Lab

Walkthroughs assume a lab CVAD site (trial or 2402 LTSR eval) with the **Remote PowerShell SDK** or on-premises PowerShell snap-ins loaded. **Cost:** trial/eval; none for the SDK.

### Lab 2.1 — Read the site like the exam does

**Objective:** Enumerate the deployment: site, controllers, and VDA registration state.

```powershell
Add-PSSnapin Citrix*
Get-BrokerSite | Select-Object Name, LicenseServerName
Get-BrokerController | Select-Object DNSName, State
Get-BrokerMachine | Select-Object MachineName, RegistrationState, DesktopGroupName
```

**Expected result:** The site name and license server; each Delivery Controller `Active`; each VDA machine `Registered` with its delivery group. `Unregistered` machines are the classic module-1 troubleshooting scenario — a VDA that cannot reach a controller delivers nothing.

**Negative test:** Stop the VDA service on a lab machine (`Stop-Service BrokerAgent`); `Get-BrokerMachine` shows it `Unregistered` and launches fail until it re-registers.

**Cleanup:** `Start-Service BrokerAgent` on the lab machine.

### Lab 2.2 — Catalog and delivery group

**Objective:** Trace resources from catalog to entitlement, the module-2 core.

```powershell
Get-BrokerCatalog | Select-Object Name, AllocationType, ProvisioningType, UnassignedCount
Get-BrokerDesktopGroup | Select-Object Name, DeliveryType, TotalDesktops, Enabled
Get-BrokerApplication | Select-Object ApplicationName, Enabled, AllAssociatedDesktopGroupUids
```

**Expected result:** Catalogs showing `MCS` (or `PVS`) provisioning and allocation type; delivery groups tying machines to users; published applications tied to their groups. The chain **catalog → delivery group → published app/desktop** is the mental model half the exam's scenarios test.

**Negative test:** Disable a delivery group (`Set-BrokerDesktopGroup -Name LabGroup -Enabled $false`); its resources vanish from StoreFront on next refresh — entitlement is the delivery group, not the catalog.

**Cleanup:** Re-enable the group.

### Lab 2.3 — Follow a launch

**Objective:** See the module-3 access flow end to end.

```powershell
# From a client, after a StoreFront/Workspace launch:
Get-BrokerSession | Select-Object UserName, DesktopGroupName, MachineName, Protocol, SessionState
```

**Expected result:** The session brokered onto a registered VDA, `Protocol HDX`, `SessionState Active` — store authentication, enumeration, `.ica` retrieval, and HDX connection all worked. Director shows the same session in its console view.

**Negative test:** Launch with the VDA's port 1494/2598 blocked; the store enumerates the icon (broker reachable) but the HDX connection fails — enumeration and session traffic are separate paths, a distinction the exam probes.

**Cleanup:** Log the test session off.

## Summary and Completion Checklist

- [ ] CVAD architecture and deployment order internalized.
- [ ] Catalog → delivery group → published resource chain drilled.
- [ ] Launch flow traced end to end with the broker PowerShell.
