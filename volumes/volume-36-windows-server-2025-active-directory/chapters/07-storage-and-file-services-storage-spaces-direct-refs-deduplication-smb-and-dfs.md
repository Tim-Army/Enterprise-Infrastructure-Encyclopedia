# Chapter 07: Storage and File Services — Storage Spaces Direct, ReFS, Deduplication, SMB, and DFS

## Learning Objectives

- Manage disks, volumes, and file systems (NTFS and ReFS) with PowerShell.
- Build resilient virtual disks with Storage Spaces and Storage Spaces Direct.
- Apply Data Deduplication and choose the right usage type.
- Share files over SMB with correct share and NTFS permissions and SMB hardening.
- Provide a unified namespace and replication with DFS Namespaces and DFS Replication.

## Theory and Architecture

Windows storage stacks from physical disk up. **Disks** carry **partitions**
formatted with a **file system**: **NTFS**, the mature default with quotas,
EFS, and fine-grained ACLs; and **ReFS**, the Resilient File System designed
for large volumes, integrity streams (checksums with automatic repair when
paired with Storage Spaces resiliency), block cloning, and fast VM
operations — the preferred file system for Hyper-V and backup targets.

**Storage Spaces** virtualizes disks: physical disks join a **storage pool**,
and **virtual disks (storage spaces)** are carved out with a **resiliency**
type — **simple** (striped, no protection), **mirror** (two- or three-way,
fast and resilient), or **parity** (space-efficient, better for archival).
**Storage Spaces Direct (S2D)**, a Datacenter feature, pools the **local**
disks of a cluster of servers into a single software-defined storage fabric
with no shared SAS — the basis of hyperconverged Windows and Azure Stack HCI.

**Data Deduplication** reclaims space by storing unique chunks once; its
**usage type** (General Purpose File Server, Hyper-V, Backup) tunes chunking
and scheduling for the workload. **SMB** is the file-sharing protocol;
access is governed by the **intersection** of **share permissions** and
**NTFS permissions** (the most restrictive wins), and SMB 3.x adds
encryption, signing, and multichannel. **DFS Namespaces** present many
physical shares as one logical path (`\\corp\files\hr`), and **DFS
Replication (DFSR)** keeps multiple copies of a folder synchronized using
remote differential compression.

## Design Considerations

Choose the file system by workload: **ReFS** for Hyper-V storage, backup
repositories, and very large volumes where integrity and block cloning
matter; **NTFS** where you need quotas, EFS, compression, or maximum
application compatibility. Choose **resiliency** by need: **three-way
mirror** for performance and strong protection, **parity** or
**mirror-accelerated parity** for capacity-oriented archival. Reserve
**S2D** for Datacenter clusters that are correctly sized (matched drives,
supported hardware, ≥2 nodes) — it is powerful but unforgiving of unbalanced
hardware.

Permission strategy should be **AGDLP** (Chapter 04): assign NTFS
permissions to **Domain Local** groups, keep **share** permissions simple
(often "Authenticated Users – Full" at the share layer and control access at
NTFS), and let the restrictive intersection do the work. Enable **SMB
encryption** for shares carrying sensitive data and **require signing** to
resist tampering. Plan **DFS Namespaces** as the user-facing paths so
back-end servers can move without changing drive mappings, and use **DFSR**
for branch replication or read-only content — but never to replicate an
actively multi-writer database or the same file edited in two sites at once.

## Implementation and Automation

Pool disks and create a resilient volume:

```powershell
$disks = Get-PhysicalDisk -CanPool $true
New-StoragePool -FriendlyName "Pool1" -StorageSubSystemFriendlyName (Get-StorageSubSystem).FriendlyName -PhysicalDisks $disks
New-VirtualDisk -StoragePoolFriendlyName "Pool1" -FriendlyName "Data" `
  -ResiliencySettingName Mirror -Size 500GB -ProvisioningType Thin
Get-VirtualDisk "Data" | Get-Disk | Initialize-Disk -PassThru |
  New-Partition -AssignDriveLetter -UseMaximumSize |
  Format-Volume -FileSystem ReFS -NewFileSystemLabel "Data"
```

Enable deduplication and share a folder with NTFS-controlled access:

```powershell
Install-WindowsFeature FS-Data-Deduplication
Enable-DedupVolume -Volume "E:" -UsageType Default
New-Item E:\Shares\HR -ItemType Directory
New-SmbShare -Name "HR" -Path "E:\Shares\HR" -FullAccess "Authenticated Users" -EncryptData $true
$acl = Get-Acl E:\Shares\HR
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule("CORP\DL-HR-RW","Modify","ContainerInherit,ObjectInherit","None","Allow")
$acl.AddAccessRule($rule); Set-Acl E:\Shares\HR $acl
```

Build a DFS namespace and add folder targets:

```powershell
Install-WindowsFeature FS-DFS-Namespace, FS-DFS-Replication -IncludeManagementTools
New-DfsnRoot -TargetPath "\\FS01\files" -Type DomainV2 -Path "\\corp.contoso.lab\files"
New-DfsnFolder -Path "\\corp.contoso.lab\files\hr" -TargetPath "\\FS01\HR"
New-DfsnFolderTarget -Path "\\corp.contoso.lab\files\hr" -TargetPath "\\FS02\HR"
```

## Validation and Troubleshooting

Confirm pool health, dedup savings, shares, and effective access:

```powershell
Get-VirtualDisk | Select-Object FriendlyName, ResiliencySettingName, HealthStatus, OperationalStatus
Get-DedupStatus -Volume "E:" | Select-Object Volume, SavedSpace, OptimizedFilesCount
Get-SmbShare; Get-SmbShareAccess -Name "HR"
Get-Acl E:\Shares\HR | Format-List
```

`HealthStatus : Healthy` and `OperationalStatus : OK` mean the space is fine;
`Degraded` means a disk failed but resiliency is holding — replace the disk
and let it repair. Common issues: a user denied because the **share** layer
is more restrictive than NTFS (or vice versa — remember the intersection);
dedup not saving space because the volume holds already-compressed data or
the optimization job has not run; DFSR **backlog** or **conflicts** when the
same file is edited in two sites (check `Get-DfsrBacklog` and the
ConflictAndDeleted folder); and SMB access failing because SMB1 is
(correctly) disabled while a legacy client still needs it — fix the client,
do not re-enable SMB1.

## Security and Best Practices

Disable **SMB1** everywhere (it is off by default on 2025) and require
**SMB signing**; enable **SMB encryption** for sensitive shares and consider
**SMB over QUIC** (Azure Edition) for internet-reachable file access without
a VPN. Apply **least privilege** with AGDLP NTFS permissions and audit
access to sensitive folders. Enable **ReFS integrity streams** on
resilient storage so bit rot is detected and repaired. Use **File Server
Resource Manager (FSRM)** for quotas and file-screening. Protect DFSR and
SYSVOL health, and keep **Volume Shadow Copies** (Previous Versions) enabled
so users can self-restore. Store backups on a **separate, ReFS** repository,
ideally immutable, to survive ransomware (Chapter 09).

## References and Knowledge Checks

- Microsoft Learn: *Storage Spaces*; *Storage Spaces Direct*; *ReFS*; *Data Deduplication*; *SMB*; *DFS Namespaces and Replication*.
- Microsoft Learn: AZ-800 — *Manage storage and file services*.

**Knowledge checks**

1. When is ReFS the right file system, and when is NTFS?
2. How is effective access computed from share and NTFS permissions?
3. What workload should never be synchronized with DFS Replication, and why?

## Hands-On Lab

Topic-level walkthroughs for AZ-800's storage and file-services skills.

**Shared prerequisites for Labs 7.1–7.4** — a Windows Server 2025 host with
at least two spare data disks, and Administrator rights. **Cost:** none.

### Lab 7.1 — Pool disks into a resilient ReFS volume (Topic: Storage Spaces)

**Objective:** Create a mirror space and format it ReFS.

```powershell
$disks = Get-PhysicalDisk -CanPool $true
New-StoragePool -FriendlyName "Pool1" -StorageSubSystemFriendlyName (Get-StorageSubSystem).FriendlyName -PhysicalDisks $disks
New-VirtualDisk -StoragePoolFriendlyName "Pool1" -FriendlyName "Data" -ResiliencySettingName Mirror -UseMaximumSize
Get-VirtualDisk "Data" | Get-Disk | Initialize-Disk -PassThru |
  New-Partition -AssignDriveLetter -UseMaximumSize | Format-Volume -FileSystem ReFS -Confirm:$false
Get-VirtualDisk "Data" | Select-Object HealthStatus, ResiliencySettingName
```

**Expected result:** a `Mirror` virtual disk with `HealthStatus : Healthy`,
formatted ReFS — mirror resiliency plus ReFS integrity streams detect and
repair corruption.

**Negative test:** try to create a mirror with only one physical disk; it
fails — mirror needs at least two disks.

**Cleanup:** `Remove-VirtualDisk "Data" -Confirm:$false; Remove-StoragePool "Pool1" -Confirm:$false`.

### Lab 7.2 — Enable deduplication (Topic: Data Deduplication)

**Objective:** Turn on dedup and confirm the job.

```powershell
Install-WindowsFeature FS-Data-Deduplication
Enable-DedupVolume -Volume "E:" -UsageType Default
Start-DedupJob -Volume "E:" -Type Optimization -Memory 50
Get-DedupStatus -Volume "E:" | Select-Object Volume, OptimizedFilesCount, SavedSpace
```

**Expected result:** dedup is enabled and, after the optimization job,
`SavedSpace` grows for a volume with redundant data — the usage type tunes
chunking for the workload.

**Negative test:** enable dedup on the system volume `C:`; it is blocked —
dedup is not supported on the boot/system volume.

**Cleanup:** `Disable-DedupVolume -Volume "E:"`.

### Lab 7.3 — Share a folder with AGDLP NTFS permissions (Topic: SMB file shares)

**Objective:** Create a share whose access is controlled by NTFS.

```powershell
New-Item E:\Shares\HR -ItemType Directory -Force
New-SmbShare -Name "HR" -Path "E:\Shares\HR" -FullAccess "Authenticated Users" -EncryptData $true
icacls E:\Shares\HR /grant "CORP\DL-HR-RW:(OI)(CI)M" /inheritance:r /grant "CORP\Domain Admins:(OI)(CI)F"
Get-SmbShareAccess HR; icacls E:\Shares\HR
```

**Expected result:** the share is encrypted and access resolves to the
NTFS `DL-HR-RW` (Modify) group — the restrictive intersection of share and
NTFS permissions governs access.

**Negative test:** set the **share** permission to Read for a user who has
NTFS Modify; effective access is Read — the more restrictive layer wins.

**Cleanup:** `Remove-SmbShare HR -Force; Remove-Item E:\Shares\HR -Recurse -Force`.

### Lab 7.4 — Build a DFS namespace (Topic: DFS Namespaces)

**Objective:** Present a share under a domain namespace.

```powershell
Install-WindowsFeature FS-DFS-Namespace -IncludeManagementTools
New-SmbShare -Name "files" -Path "E:\Shares" -FullAccess "Authenticated Users" -ErrorAction SilentlyContinue
New-DfsnRoot -TargetPath "\\$env:COMPUTERNAME\files" -Type DomainV2 -Path "\\corp.contoso.lab\files"
New-DfsnFolder -Path "\\corp.contoso.lab\files\hr" -TargetPath "\\$env:COMPUTERNAME\HR"
Get-DfsnFolderTarget -Path "\\corp.contoso.lab\files\hr"
```

**Expected result:** `\\corp.contoso.lab\files\hr` resolves to the physical
share — the namespace decouples the user-facing path from the server, so the
back end can move without remapping drives.

**Negative test:** point a folder target at a share that does not exist;
clients get a path-not-found on access — targets must reference real shares.

**Cleanup:** `Remove-DfsnFolder "\\corp.contoso.lab\files\hr" -Force; Remove-DfsnRoot "\\corp.contoso.lab\files" -Force`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Windows storage layers disks into pools and resilient virtual disks (Storage
Spaces, S2D), formatted NTFS or ReFS by workload, with deduplication for
space. SMB shares access through the restrictive intersection of share and
NTFS permissions, hardened with signing and encryption. DFS Namespaces give
a stable logical path and DFSR replicates content where it is safe to do so.

- [ ] I can build a resilient Storage Space and format it appropriately.
- [ ] I can enable deduplication with the right usage type.
- [ ] I can share files with AGDLP NTFS permissions and SMB hardening.
- [ ] I can deploy a DFS namespace and reason about DFSR safety.
- [ ] I completed Labs 7.1–7.4 including each negative test.
