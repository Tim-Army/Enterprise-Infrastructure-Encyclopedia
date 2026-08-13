# Chapter 11: Hybrid Operations and Migration — Azure Arc, Entra Connect, Azure File Sync, Update Manager, and Capstone

## Learning Objectives

- Project on-premises servers into Azure with Azure Arc for unified management.
- Extend Active Directory identity to the cloud with Microsoft Entra Connect.
- Tier and cache file data with Azure File Sync.
- Patch a hybrid estate with Azure Update Manager and enable hotpatching.
- Migrate servers and workloads, and complete a provisioning-to-operations capstone.

## Theory and Architecture

"Hybrid" is the normal state of a Windows estate: domain controllers and
file servers on-premises, identity and management extending into Azure and
Microsoft 365. Windows Server 2025 is built for it, and AZ-801's advanced
services are largely about the seam between on-premises and cloud.

**Azure Arc-enabled servers** install an agent that projects an
on-premises (or other-cloud) machine into Azure as a first-class resource.
Once Arc-enabled, a server can receive **Azure Policy**, **Azure Monitor**,
**Microsoft Defender for Cloud**, **Azure Update Manager**, extension-based
configuration, and even **hotpatching** enrollment — one control plane for
servers wherever they run.

**Microsoft Entra Connect** synchronizes on-premises AD identities to
**Microsoft Entra ID** (formerly Azure AD) so users have one identity for
on-premises and cloud apps. Sign-in options range from **password hash
synchronization** (simplest, most resilient) to **pass-through
authentication** and **federation** (AD FS). **Entra Connect cloud sync**
is the newer, lightweight agent-based alternative for many scenarios. This
is the bridge that makes the Microsoft 365 and Intune world of Volume XXXVII
possible.

**Azure File Sync** turns a Windows file server into a cache of an **Azure
file share**: hot data stays local while cold data is **tiered** to the
cloud, and multiple servers can sync the same namespace — cloud-backed file
services with local performance. **Azure Update Manager** patches Windows
(and Linux) across on-premises (via Arc) and Azure from one place, replacing
the on-premises-only WSUS model for many organizations. Migration tools —
**Storage Migration Service** (move file servers, including old SMB1
servers, with cutover), **Active Directory Migration Toolkit / ADMT**, and
**Azure Migrate** — move workloads forward without a rebuild.

## Design Considerations

Arc-enable **every** server you want to govern centrally — the agent is
lightweight and unlocks Policy, Monitor, Defender for Cloud, Update Manager,
and hotpatch. Choose the **Entra Connect sign-in method** by resilience and
requirements: **password hash sync** for most (cloud authentication survives
an on-premises outage), **pass-through** or **federation** only where policy
demands on-premises credential validation; prefer **cloud sync** for simple
topologies. Keep **one** authoritative sync and watch the sync scope so you
do not synchronize service or privileged accounts unnecessarily.

Use **Azure File Sync** where branch/HQ file servers benefit from cloud
tiering and centralized backup, sizing the **local cache** to the hot
working set. Move patching to **Azure Update Manager** for a single hybrid
view and schedule maintenance windows; adopt **hotpatching** (via Arc) where
reboot avoidance is valuable. Plan **migrations** with Storage Migration
Service for file servers and Azure Migrate for lift-and-shift, always with a
tested cutover and rollback. Throughout, apply the **security** posture of
Chapter 10 — Arc, Entra, and File Sync all use identities and keys that must
be protected.

## Implementation and Automation

Onboard a server to Azure Arc and check in:

```powershell
# Download and run the Connected Machine agent, then connect:
& "$env:ProgramFiles\AzureConnectedMachineAgent\azcmagent.exe" connect `
  --resource-group "rg-hybrid" --tenant-id "<tenant>" --location "eastus" --subscription-id "<sub>"
& "$env:ProgramFiles\AzureConnectedMachineAgent\azcmagent.exe" show
```

Deploy Azure File Sync on a server (after creating the Storage Sync Service
and sync group in Azure):

```powershell
Install-Module Az.StorageSync -Scope AllUsers
# Install the sync agent, register the server, then add a server endpoint with cloud tiering:
Register-AzStorageSyncServer -ResourceGroupName "rg-hybrid" -StorageSyncServiceName "sss-corp"
New-AzStorageSyncServerEndpoint -Name "E-Shares" -ServerLocalPath "E:\Shares" `
  -CloudTiering $true -VolumeFreeSpacePercent 20
```

Enroll and patch with Azure Update Manager (Arc-connected servers appear
automatically); trigger an assessment/update from the portal or CLI. For
identity, install **Entra Connect** and select **password hash sync** in the
wizard, then confirm synchronization:

```powershell
Import-Module ADSync
Get-ADSyncScheduler | Select-Object SyncCycleEnabled, NextSyncCyclePolicyType
Start-ADSyncSyncCycle -PolicyType Delta
```

## Validation and Troubleshooting

Confirm Arc connection, identity sync, and file-sync health:

```powershell
azcmagent show                                  # Agent Status: Connected
Get-ADSyncScheduler                             # sync enabled, next cycle
Get-AzStorageSyncServerEndpoint -Name "E-Shares" | Select-Object SyncStatus, LastSyncSuccessTimestamp
```

Arc `Agent Status : Connected` means the server is projected into Azure.
Common issues: Arc onboarding failing on **outbound HTTPS/443** to Azure
endpoints or a missing service principal role; **Entra Connect** not
synchronizing because of a **duplicate/soft-match** attribute conflict or a
filtered OU (check the synchronization service manager and Entra Connect
Health); **Azure File Sync** tiering not reclaiming space because the volume
free-space policy is already satisfied or files are pinned; and **Update
Manager** showing servers non-compliant because the Arc agent or update
extension is unhealthy. For migrations, Storage Migration Service **cutover**
failing usually traces to network, credentials, or SMB signing mismatches
between source and destination.

## Security and Best Practices

Protect the **hybrid seam**: Arc uses a managed identity — scope its RBAC
tightly; Entra Connect holds powerful sync rights — run it on a hardened,
Tier-0-class server and enable **Entra Connect Health** monitoring. Do
**not** synchronize privileged on-premises accounts to the cloud, and use
**Entra ID Protection** and Conditional Access (Volume XXXVII) on the synced
identities. Secure **Azure File Sync** storage accounts with private
endpoints and restricted keys. Patch continuously with **Update Manager**
and adopt **hotpatching** to cut reboot exposure. During **migration**,
preserve least privilege, validate data integrity after cutover, and keep
the source recoverable until the destination is proven. Treat Azure
resources with the same tiering discipline as on-premises Tier 0.

## References and Knowledge Checks

- Microsoft Learn: *Azure Arc-enabled servers*; *Microsoft Entra Connect*; *Azure File Sync*; *Azure Update Manager*; *Storage Migration Service*.
- Microsoft Learn: AZ-801 — *Migrate servers and workloads; monitor and troubleshoot Windows Server*.

**Knowledge checks**

1. What capabilities does Arc-enabling an on-premises server unlock?
2. Why is password hash synchronization often the most resilient Entra Connect sign-in method?
3. How does Azure File Sync keep local performance while reducing on-premises capacity?

## Hands-On Lab

Topic-level walkthroughs for AZ-801's hybrid and migration skills, closing
with a capstone. The Azure-connected steps assume a subscription; the
capstone can be completed on-premises only.

**Shared prerequisites for Labs 11.1–11.4** — the `corp.contoso.lab` domain,
outbound HTTPS to Azure, an Azure subscription (free tier is sufficient for
the Arc/File Sync steps), and Administrator rights. **Cost:** minimal
(Arc-enabled servers and small file shares fall in or near the free tier;
delete resources after).

### Lab 11.1 — Arc-enable a server (Topic: Hybrid management)

**Objective:** Project a server into Azure.

```powershell
& "$env:ProgramFiles\AzureConnectedMachineAgent\azcmagent.exe" connect `
  --resource-group "rg-hybrid" --location "eastus" --subscription-id "<sub>" --tenant-id "<tenant>"
& "$env:ProgramFiles\AzureConnectedMachineAgent\azcmagent.exe" show
```

**Expected result:** `Agent Status : Connected` and the server appears in the
Azure portal under Azure Arc — it can now receive Policy, Monitor, Defender
for Cloud, and Update Manager.

**Negative test:** run `connect` with outbound 443 to Azure blocked; it fails
with a connectivity error — Arc needs outbound HTTPS to Azure endpoints.

**Rollback:** `azcmagent disconnect` and delete the Azure resource.

### Lab 11.2 — Verify Entra Connect synchronization (Topic: Hybrid identity)

**Objective:** Confirm on-premises identities reach Entra ID.

```powershell
Import-Module ADSync
Get-ADSyncScheduler | Select-Object SyncCycleEnabled, NextSyncCyclePolicyType
Start-ADSyncSyncCycle -PolicyType Delta
```

**Expected result:** the scheduler is enabled and a delta sync runs; a test
user created on-premises appears in Entra ID within a cycle — password hash
sync gives one identity for cloud and on-premises.

**Negative test:** place a user in an OU excluded from the sync scope; it
never appears in Entra ID — sync scope (filtering) controls what is
projected.

**Rollback:** remove the test user; leave sync running.

### Lab 11.3 — Add an Azure File Sync server endpoint with tiering (Topic: Hybrid file services)

**Objective:** Back a local share with an Azure file share and tier cold data.

```powershell
Register-AzStorageSyncServer -ResourceGroupName "rg-hybrid" -StorageSyncServiceName "sss-corp"
New-AzStorageSyncServerEndpoint -Name "E-Shares" -ServerLocalPath "E:\Shares" `
  -CloudTiering $true -VolumeFreeSpacePercent 20
Get-AzStorageSyncServerEndpoint -Name "E-Shares" | Select-Object SyncStatus, CloudTiering
```

**Expected result:** the server endpoint syncs `E:\Shares` to the Azure file
share and tiers cold files when free space drops below 20% — hot data stays
local, cold data moves to the cloud.

**Negative test:** set `VolumeFreeSpacePercent` to `0`; nothing tiers because
the policy is never triggered — tiering is driven by the free-space policy.

**Rollback:** remove the server endpoint and Azure resources.

### Lab 11.4 — Capstone: provision-to-operations for a new application server (Topic: Integrate the volume)

**Objective:** Combine the volume's skills into one workflow.

```powershell
# 1. Provision (Ch01/02): deploy Server Core, name it, join the domain
Add-Computer -DomainName "corp.contoso.lab" -NewName "APP10" -Restart
# 2. Placement & policy (Ch04/05): OU + baseline GPO already target Servers OU
Move-ADObject (Get-ADComputer APP10).DistinguishedName -TargetPath "OU=Servers,DC=corp,DC=contoso,DC=lab"
# 3. Identity for the app (Ch10): a gMSA, no static secret
New-ADServiceAccount -Name "gmsa-app10" -DNSHostName "gmsa-app10.corp.contoso.lab" `
  -PrincipalsAllowedToRetrieveManagedPassword "GG-App-Servers"
# 4. Storage (Ch07): resilient ReFS data volume + share
# 5. Availability (Ch09): back up system state / add to a cluster if needed
# 6. Hybrid (Ch11): Arc-enable and enroll in Update Manager
azcmagent connect --resource-group "rg-hybrid" --location "eastus" --subscription-id "<sub>" --tenant-id "<tenant>"
```

**Expected result:** `APP10` is domain-joined in the Servers OU with the
baseline GPO applied, uses a gMSA for its service, stores data on resilient
ReFS, is backed up, and is Arc-managed and patched by Update Manager — the
whole volume in one server's lifecycle.

**Negative test:** skip the OU move; the baseline GPO never applies because
the computer sits in the default `Computers` container — placement drives
policy (Chapter 05).

**Rollback:** decommission `APP10` and remove its gMSA and Azure resources.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Hybrid operations connect the on-premises estate to Azure: Arc projects
servers into one control plane; Entra Connect extends identity to the cloud;
Azure File Sync tiers file data; Azure Update Manager and hotpatching keep
the estate current; and Storage Migration Service and Azure Migrate move
workloads forward. The capstone shows the whole volume — provisioning,
identity, policy, storage, availability, security, and hybrid management —
as one server's lifecycle.

- [ ] I can Arc-enable a server and explain what it unlocks.
- [ ] I can verify Entra Connect identity synchronization.
- [ ] I can deploy Azure File Sync with cloud tiering.
- [ ] I can patch a hybrid estate and plan a migration.
- [ ] I completed Labs 11.1–11.4, including the capstone and each negative test.
