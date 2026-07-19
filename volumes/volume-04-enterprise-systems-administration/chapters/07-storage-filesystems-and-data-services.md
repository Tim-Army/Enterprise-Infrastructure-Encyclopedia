# Chapter 07: Storage, Filesystems, and Data Services

## Learning Objectives

- Compare enterprise-relevant filesystems — ext4, XFS, and Btrfs on
  Linux; NTFS and ReFS on Windows — and select the appropriate one for a
  given workload.
- Extend the LVM coverage from [Chapter 02](02-enterprise-linux-administration.md) with Windows Storage Spaces as
  the conceptually parallel Windows volume-management layer.
- Deploy and consume network file services — NFS and SMB/CIFS — from both
  Linux and Windows hosts.
- Apply filesystem-level quotas and access controls to enforce fair use
  and delegated administration.
- Explain where this chapter's host-level storage coverage ends and the
  block/array-level storage design covered in [Volume VI](../../volume-06-enterprise-storage-data-protection/README.md) begins.
- Design a filesystem layout that isolates growth-prone paths from
  critical system partitions.

## Theory and Architecture

This chapter covers storage from the perspective of the operating system
consuming it: which filesystem to format a volume with, how to manage
volumes above the raw disk (extending [Chapter 02](02-enterprise-linux-administration.md)'s LVM coverage to
Windows), how to share and consume filesystems over the network, and how
to constrain consumption with quotas. Storage array architecture, SAN/NAS
protocol design (iSCSI, Fibre Channel, NVMe-oF), snapshots at the array
layer, and backup/replication strategy are covered in [Volume VI](../../volume-06-enterprise-storage-data-protection/README.md); this
chapter stops at the host's own filesystem and volume-management layer.

### Filesystem choice

| Filesystem | Platform | Strengths | Limitations |
| --- | --- | --- | --- |
| ext4 | Linux | Mature, low overhead, well understood failure modes | No native snapshots or checksumming; shrinking is possible but disruptive |
| XFS | Linux (RHEL default) | Strong large-file and parallel I/O throughput, online grow | Cannot shrink an XFS filesystem at all — only grow |
| Btrfs | Linux (SUSE default) | Copy-on-write snapshots, built-in checksumming, native multi-device support | More operational complexity; historically less mature under heavy random-write database workloads |
| NTFS | Windows (default) | Mature, rich ACL model, widely supported by every Windows-aware tool | No built-in checksumming of data blocks |
| ReFS | Windows (Server, data volumes) | Block checksumming and metadata integrity, integrates with Storage Spaces mirror/parity for automatic repair | Not supported as a boot volume; feature parity with NTFS is intentionally partial |

The practical default in this encyclopedia's baseline: XFS for RHEL 10
data volumes ([Volume XIV](../../volume-14-red-hat-enterprise-linux-10/README.md) covers RHEL-specific tuning), ext4 where
shrink-capable flexibility matters more than large-file throughput, NTFS
for Windows system and general data volumes, and ReFS for large
Windows data volumes — especially those backed by Storage Spaces — where
its self-healing integrates with mirror or parity resiliency.

### Windows Storage Spaces as the volume-management layer

[Chapter 02](02-enterprise-linux-administration.md) covered Linux Logical Volume Manager (LVM): physical volumes
(PVs) join a volume group (VG), from which logical volumes (LVs) are
carved and later grown. Windows Storage Spaces follows the same
three-layer shape under different names:

| LVM concept | Storage Spaces concept |
| --- | --- |
| Physical Volume (PV) | Physical Disk, added to a Storage Pool |
| Volume Group (VG) | Storage Pool |
| Logical Volume (LV) | Virtual Disk, formatted with a Volume |

A Virtual Disk in Storage Spaces additionally declares a **resiliency
type** at creation — `Simple` (striped, no redundancy — analogous to
RAID 0), `Mirror` (analogous to RAID 1/10), or `Parity` (analogous to
RAID 5/6) — a decision LVM leaves to a separate layer (`mdadm`/RAID
underneath the PV) rather than baking into the volume-management tool
itself.

### Network file services

- **NFS** (Network File System) is the standard Linux-native network
  filesystem. NFSv3 is stateless and uses separate mount/lock protocols on
  dynamic ports (requiring `rpcbind`); **NFSv4.2** — the version assumed
  in this baseline — is stateful, consolidates everything onto a single
  TCP port 2049, and supports Kerberos-based security (`sec=krb5`,
  `krb5i`, `krb5p`) instead of relying solely on host/UID trust.
- **SMB** (Server Message Block, still commonly called CIFS from its
  older dialect) is the standard Windows-native network filesystem. This
  baseline assumes **SMB 3.1.1**, which supports mandatory signing and
  end-to-end encryption. Linux hosts serve SMB shares with **Samba** and
  consume Windows SMB shares with the kernel `cifs` filesystem client;
  Windows hosts consume NFS exports with the optional "Client for NFS"
  feature.
- Choosing between them for a given workload: SMB is the natural choice
  when Windows clients are involved or when the enterprise's identity
  integration is AD/Kerberos-centric end to end; NFS remains the standard
  for Linux-to-Linux workloads, especially where POSIX semantics
  (advisory locking, permission bits) matter to the application.

### Quotas and access control

Filesystem quotas cap consumption per user, group, or (on XFS) per
**project** — an arbitrary directory-based grouping independent of Unix
ownership, useful for capping a shared application directory regardless
of which service account writes to it. Windows offers the equivalent
through **File Server Resource Manager (FSRM)** quotas, which can be
**hard** (block writes once the limit is hit) or **soft** (log/alert only).
[Chapter 02](02-enterprise-linux-administration.md) introduced POSIX ACLs for fine-grained Linux permissions; NTFS
ACLs serve the same purpose on Windows and are considerably richer by
default, since NTFS was designed around ACL-based access control from the
outset rather than adding it on top of a simpler owner/group/other model.

## Design Considerations

- **Match the filesystem to the workload's I/O pattern**, not to habit.
  A database workload with heavy random writes has different filesystem
  needs than a large sequential-write log archive; test the actual
  workload rather than defaulting to "whatever the last host used."
- **Isolate growth-prone paths, extending [Chapter 02](02-enterprise-linux-administration.md)'s FHS guidance.**
  `/var`, `/var/log`, `/home`, and equivalents (`D:\Data`, `D:\Logs` on
  Windows) belong on their own volume so unbounded growth cannot fill the
  volume the operating system itself depends on.
- **NFS vs. SMB is a client-mix and identity-integration decision**, not
  a performance-only one; mixed-client environments sometimes run both,
  exported from the same underlying data with careful attention to
  permission-model translation between POSIX and NTFS semantics.
- **Storage Spaces resiliency trade-off.** Mirror resiliency costs more
  usable capacity for better random-write performance and faster rebuild;
  parity resiliency is more capacity-efficient but rebuilds more slowly
  and costs more write performance — choose based on the workload's
  read/write ratio and rebuild-time tolerance, not capacity efficiency
  alone.
- **Know where OS-level storage design hands off to the array.** Multipath
  I/O, array-level snapshots, replication, and SAN zoning are [Volume VI](../../volume-06-enterprise-storage-data-protection/README.md)
  topics; this chapter's LVM/Storage Spaces layer sits on top of whatever
  block device the array (or a simple local disk) presents.
- **Design quota enforcement with a grace period**, not an abrupt hard
  stop, wherever the workload can tolerate it — a soft limit with
  alerting gives an administrator or user time to react before a hard
  limit blocks writes outright.

## Implementation and Automation

### Creating and mounting filesystems on Linux

```bash
# Format a new logical volume with XFS and mount it with sensible
# enterprise defaults (noatime avoids unnecessary metadata writes on
# every read).
sudo mkfs.xfs /dev/vg_data/lv_appdata
sudo mkdir -p /data/app
sudo mount -o noatime /dev/vg_data/lv_appdata /data/app

# Persist the mount, referencing the volume by its stable UUID rather
# than device path.
uuid=$(sudo blkid -s UUID -o value /dev/vg_data/lv_appdata)
echo "UUID=${uuid} /data/app xfs noatime 0 2" | sudo tee -a /etc/fstab
sudo mount -a
```

### Windows Storage Spaces

```powershell
# Build a mirrored storage pool from two data disks, then carve a
# resilient virtual disk and format it with ReFS — the Windows analog to
# the pvcreate/vgcreate/lvcreate sequence in Chapter 02.
$disks = Get-PhysicalDisk -CanPool $true

New-StoragePool -FriendlyName 'AppDataPool' `
    -StorageSubsystemFriendlyName '*Storage Spaces*' `
    -PhysicalDisks $disks

New-VirtualDisk -StoragePoolFriendlyName 'AppDataPool' `
    -FriendlyName 'AppDataDisk' -ResiliencySettingName Mirror `
    -UseMaximumSize

Get-VirtualDisk 'AppDataDisk' | Get-Disk | Initialize-Disk -PartitionStyle GPT -PassThru |
    New-Partition -DriveLetter D -UseMaximumSize |
    Format-Volume -FileSystem ReFS -NewFileSystemLabel 'AppData' -Confirm:$false
```

### NFS server and client

```bash
# Server: export a directory to a specific client subnet only, with
# Kerberos-backed privacy (sec=krb5p) rather than host/UID trust alone.
sudo dnf install -y nfs-utils   # Debian/Ubuntu: sudo apt install nfs-kernel-server

sudo mkdir -p /export/appdata
sudo tee -a /etc/exports <<'EOF'
/export/appdata 10.20.30.0/24(rw,sync,sec=krb5p,no_subtree_check)
EOF
sudo exportfs -ra
sudo systemctl enable --now nfs-server

# Client: mount using NFSv4.2 explicitly.
sudo mkdir -p /mnt/appdata
sudo mount -t nfs4 -o sec=krb5p nfs01.example.internal:/export/appdata /mnt/appdata
```

### SMB share creation and consumption

```powershell
# Windows SMB server side (extends the Chapter 03 file-server example
# with an access-controlled group rather than "Administrators" only).
New-SmbShare -Name 'AppData' -Path 'D:\AppData' `
    -FullAccess 'EXAMPLE\app-admins' -ChangeAccess 'EXAMPLE\app-writers'
Set-SmbShare -Name 'AppData' -EncryptData $true
```

```bash
# Linux client mounting a Windows SMB share with the kernel cifs client.
sudo dnf install -y cifs-utils   # Debian/Ubuntu: sudo apt install cifs-utils
sudo mkdir -p /mnt/appdata-smb
sudo mount -t cifs //winsrv-file01/AppData /mnt/appdata-smb \
  -o username=svc-appmount,domain=EXAMPLE,seal,vers=3.1.1,credentials=/etc/smb-appmount.cred
```

### Quota configuration

```bash
# XFS project quota: cap a shared directory at 50 GiB regardless of
# which UID writes into it — requires the pquota mount option.
sudo tee -a /etc/projects <<'EOF'
100:/data/app/shared
EOF
sudo tee -a /etc/projid <<'EOF'
sharedapp:100
EOF
sudo xfs_quota -x -c 'project -s sharedapp' /data/app
sudo xfs_quota -x -c 'limit -p bhard=50g sharedapp' /data/app
xfs_quota -x -c 'report -p' /data/app
```

```powershell
# FSRM soft quota with an email/log alert at 85% of a 100 GB limit —
# requires the File Server Resource Manager feature.
Install-WindowsFeature FS-Resource-Manager -IncludeManagementTools

New-FsrmQuota -Path 'D:\AppData' -Size 100GB -SoftLimit `
    -Threshold @(New-FsrmQuotaThreshold -Percentage 85 -Action `
        (New-FsrmAction -Type Email -MailTo 'storage-alerts@example.internal' `
            -Subject 'AppData quota at [Quota Threshold]%'))
```

## Validation and Troubleshooting

- Confirm filesystem and mount state: `df -hT`, `findmnt /data/app`,
  `xfs_info /data/app` (Linux); `Get-Volume`, `Get-StoragePool`,
  `Get-VirtualDisk | Select FriendlyName, HealthStatus` (Windows).
- Confirm an NFS export is visible and correctly restricted:
  `showmount -e nfs01.example.internal` from an authorized client should
  list the export; the same command from an unauthorized network should
  either be refused or show an empty list depending on firewall policy.
- Confirm SMB reachability before troubleshooting authentication:
  `Test-NetConnection -ComputerName winsrv-file01 -Port 445`; from Linux,
  `smbclient -L //winsrv-file01 -U svc-appmount`.
- Confirm quota enforcement: `xfs_quota -x -c 'report -p' /data/app` shows
  used vs. limit; `Get-FsrmQuota -Path D:\AppData` shows current usage
  against the configured threshold.

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| NFS mount hangs indefinitely | Server unreachable, NFS service down, or firewall blocking port 2049 | `showmount -e` from the client; `systemctl status nfs-server` on the server |
| NFS mount returns "stale file handle" | Export was reconfigured/removed while a client held it mounted | Unmount and remount (`umount -f`, then re-mount); confirm current `/etc/exports` matches expectation |
| SMB share inaccessible with "access denied" despite correct share permissions | NTFS ACL on the underlying folder is more restrictive than the share permission | Check `Get-Acl D:\AppData`; share and NTFS permissions are both enforced, and the more restrictive one wins |
| `lvextend`/Storage Spaces virtual disk grows but the filesystem does not | Filesystem not grown after the volume-management layer | `xfs_growfs` (XFS) / `resize2fs` (ext4); `Resize-Partition` then `Resize-FileSystem` on Windows |
| Quota limit reached unexpectedly early | Project/user quota misattributed, or a different UID/service account is writing than assumed | `xfs_quota -x -c 'report -p'`; confirm the writing account's UID against `/etc/projid` mapping |

## Security and Best Practices

- Prefer NFSv4.2 with `sec=krb5p` (Kerberos with full privacy/encryption)
  over host-based `AUTH_SYS` trust, which trusts any client claiming a
  given UID with no cryptographic verification.
- Require SMB signing and, for sensitive shares, SMB encryption
  (`Set-SmbShare -EncryptData $true`); confirm SMBv1 remains disabled
  fleet-wide, consistent with [Chapter 03](03-windows-server-administration.md).
- Grant NTFS and share permissions to specific groups scoped to the
  actual need (`app-admins`, `app-writers`), never `Everyone: Full
  Control`, mirroring the least-privilege ACL guidance in [Chapter 02](02-enterprise-linux-administration.md).
- Use quotas as a capacity-exhaustion control, not only a cost-management
  one — an unbounded shared directory is the network-storage equivalent
  of the unmonitored `/var` growth called out in [Chapter 02](02-enterprise-linux-administration.md).
- Encrypt data at rest where compliance requires it (LUKS on Linux,
  BitLocker on Windows); this chapter covers filesystem/volume mechanics
  only — encryption key management and compliance mapping are covered in
  [Volume VI](../../volume-06-enterprise-storage-data-protection/README.md) and [Volume X](../../volume-10-enterprise-cybersecurity/README.md).
- Audit share and export permission changes the same way any other
  security-relevant configuration change is audited ([Chapter 08](08-systems-security-automation-and-compliance.md)).

## References and Knowledge Checks

**References**

- `xfs(5)`, `mkfs.xfs(8)`, `exports(5)`, `nfs(5)` man pages.
- Microsoft Learn: "Storage Spaces overview," "ReFS overview," and "File
  Server Resource Manager overview."
- Microsoft Learn: "SMB security enhancements."
- Red Hat documentation: "Managing file systems" (XFS/ext4) and
  "Configuring an NFS server."

**Knowledge Checks**

1. Why can an XFS filesystem be grown online but never shrunk, and what
   does that imply for initial sizing?
2. Map LVM's physical volume, volume group, and logical volume concepts
   to their Windows Storage Spaces equivalents.
3. What security advantage does NFSv4 with `sec=krb5p` have over
   NFSv3's default host-based trust model?
4. If a user has full NTFS permissions on a folder but the SMB share
   permission only grants read access, what access do they actually get?
5. What is the difference between a hard quota and a soft quota, and
   when would an administrator choose the softer option?

## Hands-On Lab

**Objective:** Export an NFSv4 share restricted to a specific client
subnet, mount it from a second Linux VM, apply an XFS project quota to
the exported directory, and validate both the access restriction and the
quota.

### Prerequisites

- Two Linux VMs on the same private subnet: `nfs01` (server) and
  `nfsclient01` (client), both RHEL-family or Debian-family, 2 vCPU / 2 GB
  RAM each.
- `sudo` access on both VMs.
- `nfs01` has an XFS filesystem mounted at `/data` with the `pquota`
  mount option enabled (add `pquota` to the relevant `/etc/fstab` entry
  and remount, or format a scratch logical volume as XFS specifically for
  this lab if `/data` cannot be remounted).

### Procedure

1. On `nfs01`, install NFS server packages and create the export
   directory:

   ```bash
   sudo dnf install -y nfs-utils
   sudo mkdir -p /data/labexport
   sudo chmod 755 /data/labexport
   echo "lab file from nfs01" | sudo tee /data/labexport/hello.txt
   ```

2. Export the directory restricted to `nfsclient01`'s subnet only
   (adjust the CIDR to your lab network):

   ```bash
   sudo tee -a /etc/exports <<'EOF'
   /data/labexport 10.20.30.0/24(rw,sync,no_subtree_check)
   EOF
   sudo exportfs -ra
   sudo systemctl enable --now nfs-server
   ```

3. On `nfsclient01`, mount the export and confirm access:

   ```bash
   sudo dnf install -y nfs-utils
   sudo mkdir -p /mnt/labexport
   sudo mount -t nfs4 nfs01:/data/labexport /mnt/labexport
   cat /mnt/labexport/hello.txt
   ```

   **Expected result:** the command prints `lab file from nfs01`,
   confirming the mount succeeded and the export is readable.

4. On `nfs01`, apply an XFS project quota of 10 MiB to the exported
   directory:

   ```bash
   echo "200:/data/labexport" | sudo tee -a /etc/projects
   echo "labexport:200" | sudo tee -a /etc/projid
   sudo xfs_quota -x -c 'project -s labexport' /data
   sudo xfs_quota -x -c 'limit -p bhard=10m labexport' /data
   ```

5. From `nfsclient01`, exceed the quota and confirm enforcement:

   ```bash
   dd if=/dev/zero of=/mnt/labexport/fillfile bs=1M count=15 2>&1 | tail -3
   ```

   **Expected result:** the write fails partway with a "Disk quota
   exceeded" error once the 10 MiB project limit is reached, confirmed by
   `sudo xfs_quota -x -c 'report -p' /data` on `nfs01` showing usage at
   the hard limit.

### Negative Test

From a third host **outside** the `10.20.30.0/24` subnet permitted in
step 2 (or by temporarily changing `nfsclient01`'s IP outside that range
if a third host is unavailable), attempt:

```bash
showmount -e nfs01
sudo mount -t nfs4 nfs01:/data/labexport /mnt/labexport
```

**Expected result:** the mount is refused (permission denied or no
route, depending on firewall configuration), confirming the export's
subnet restriction is enforced by the NFS server, not merely documented
as an intended restriction.

### Cleanup

```bash
# On nfsclient01:
sudo umount /mnt/labexport
sudo rmdir /mnt/labexport

# On nfs01:
sudo sed -i '/labexport/d' /etc/exports /etc/projects /etc/projid
sudo exportfs -ra
sudo xfs_quota -x -c 'limit -p bhard=0 labexport' /data
sudo rm -rf /data/labexport
```

## Summary and Completion Checklist

This chapter extended the [Chapter 02](02-enterprise-linux-administration.md) LVM foundation to the full host
storage picture: filesystem selection across ext4, XFS, Btrfs, NTFS, and
ReFS; Windows Storage Spaces as the direct conceptual counterpart to LVM;
NFS and SMB as the two enterprise network file service protocols, each
with its own security model; and quotas and ACLs as the controls that
keep shared storage fairly allocated and appropriately restricted. Array-
level storage design picks up where this chapter's host-level coverage
ends, in [Volume VI](../../volume-06-enterprise-storage-data-protection/README.md).

- [ ] Can select an appropriate filesystem for a given workload and
      justify the choice against the comparison table in this chapter.
- [ ] Can map LVM concepts to Windows Storage Spaces concepts one for
      one.
- [ ] Can export/mount NFSv4 and create/consume an SMB share with
      access restricted to specific clients or groups.
- [ ] Can apply and verify an XFS project quota or an FSRM quota.
- [ ] Completed the hands-on lab, including the negative test proving
      the NFS export's subnet restriction is enforced at the server, not
      merely documented.
