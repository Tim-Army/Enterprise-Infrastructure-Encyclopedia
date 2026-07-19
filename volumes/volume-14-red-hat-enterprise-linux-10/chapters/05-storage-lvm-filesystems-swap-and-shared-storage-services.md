# Chapter 05: Storage, LVM, Filesystems, Swap, and Shared-Storage Services

## Learning Objectives

- Partition disks using GPT and manage block devices with `parted` and
  `lsblk`.
- Build and extend a Logical Volume Management (LVM) stack from
  physical volumes through logical volumes.
- Create, mount, and persist XFS and ext4 filesystems, including
  UUID-based and automounted mounts.
- Configure and manage swap space, and explain when Stratis or VDO is
  a better fit than classic LVM.
- Share and consume storage across the network using NFS and Samba.
- Diagnose common storage failures, from a failed mount to a full
  filesystem to a degraded LVM volume group.

## Theory and Architecture

RHEL 10 storage is organized as a layered stack, and every layer above
raw block devices is a deliberate abstraction that trades some
simplicity for flexibility an enterprise environment needs: the
ability to grow a filesystem without downtime, to snapshot a volume
before a risky change, and to present storage consistently across
physical disks, virtual disks, and network-attached storage.

### The storage stack

```text
Physical/virtual disk  ->  Partition (GPT)  ->  LVM (PV -> VG -> LV)  ->  Filesystem (XFS/ext4)  ->  Mount point
```

A filesystem does not have to sit on an LVM logical volume — a
partition can be formatted and mounted directly — but LVM is the
default, recommended layer for anything that may need to grow, be
snapshotted, or be migrated to different physical storage without
unmounting.

### Partitioning

RHEL 10 uses **GPT (GUID Partition Table)** by default rather than the
legacy MBR scheme, supporting more than four primary partitions and
disks larger than 2 TiB. `parted` is the standard interactive and
scriptable partitioning tool; `gdisk` remains available for GPT-specific
low-level work. Block devices are named predictably
(`/dev/sda`, `/dev/nvme0n1`) and partitions are numbered suffixes
(`/dev/sda1`, `/dev/nvme0n1p1`); `lsblk` and `blkid` are the two
fastest ways to see the current device/partition/filesystem
relationship and each filesystem's UUID.

### LVM: physical volumes, volume groups, logical volumes

LVM interposes three abstractions between raw partitions and a usable
filesystem:

1. **Physical Volume (PV)** — a partition or whole disk initialized for
   LVM use (`pvcreate`), contributing its space to a volume group.
2. **Volume Group (VG)** — a pool of storage aggregated from one or
   more PVs (`vgcreate`); a VG's total capacity is the sum of its
   member PVs, and adding a PV to a VG (`vgextend`) grows that pool
   without touching existing logical volumes.
3. **Logical Volume (LV)** — a virtual block device carved out of a
   VG's free space (`lvcreate`), which is what actually gets formatted
   with a filesystem and mounted.

This indirection is what allows `lvextend` to grow a logical volume
live (immediately followed by growing the filesystem on top of it with
`xfs_growfs` or `resize2fs`) without unmounting, and what allows an
LVM **snapshot** — a point-in-time, copy-on-write view of an LV — to
back up or roll back a volume's state without a separate backup
appliance for the simplest cases.

### Filesystem choice: XFS and ext4

RHEL 10's default filesystem is **XFS**, a high-performance,
64-bit journaling filesystem well suited to large files and high
I/O concurrency; it does not support shrinking (an XFS filesystem can
only grow, never shrink in place — a fixed constraint worth
architecting around before provisioning). **ext4** remains fully
supported and is sometimes preferred for smaller volumes, compatibility
with tooling that expects ext-family semantics, or scenarios requiring
in-place shrink. Every filesystem is best referenced by its **UUID**
(from `blkid`) in `/etc/fstab` rather than its device path, because
device naming (`/dev/sdb1` vs `/dev/sdc1`) is not guaranteed stable
across reboots on systems with multiple disks, especially after a
hardware or virtual-disk-controller change.

### Swap

Swap space extends usable memory by paging inactive pages to disk
under memory pressure; on RHEL 10 it can be a dedicated partition or,
more commonly in virtualized and cloud deployments, an LVM logical
volume or a swap file. `swappiness` (a kernel tunable,
`/proc/sys/vm/swappiness`) controls how aggressively the kernel
prefers swapping over reclaiming page cache — low-latency,
memory-abundant server workloads typically lower it from the default.

### Stratis and VDO

Two additional storage technologies extend the classic LVM/filesystem
model for specific needs:

- **Stratis** is a local storage management solution
  (`stratisd` + `stratis` CLI) that layers thin provisioning,
  filesystem creation, and future snapshot/pool management behind a
  single simplified interface, aimed at reducing the number of manual
  LVM and filesystem steps for common configurations.
- **VDO (Virtual Data Optimizer)** provides inline deduplication and
  compression beneath a filesystem or LVM layer, most valuable for
  storage-dense workloads with highly redundant or compressible data
  (backup targets, VM image repositories) where the CPU cost of
  inline reduction is worth the capacity savings.

Both integrate with, rather than replace, the LVM concepts above.

### Shared-storage services: NFS and Samba

Not all storage needs are local. **NFS (Network File System)** shares
a server-side directory (`/etc/exports`) for Linux/Unix clients to
mount over the network, authenticated and authorized primarily by
client IP/network and UID/GID mapping rather than a login prompt.
**Samba** implements the SMB/CIFS protocol, the standard for sharing
storage with Windows clients and for cross-platform environments,
authenticated with its own user database or integration with a
directory service. **autofs** mounts either type of network share
on demand when a path is accessed and unmounts it after a period of
inactivity, avoiding the reliability and boot-order problems of a
network filesystem hard-mounted at boot via `/etc/fstab`.

## Design Considerations

- **Partition/LVM sizing headroom.** Size volume groups with growth
  headroom in mind — leaving unallocated space in a VG (rather than
  allocating 100% to LVs immediately) makes future `lvextend`
  operations trivial; retrofitting growth onto a fully allocated VG
  requires adding new physical storage first.
- **XFS's no-shrink constraint.** Because XFS cannot shrink in place,
  provisioning an oversized XFS volume "to be safe" is a one-way
  decision; either provision conservatively and grow later, or accept
  ext4 for volumes genuinely likely to need a size reduction.
- **Swap sizing philosophy.** Modern server guidance favors modest
  swap (enough to absorb transient pressure and support hibernation
  where relevant) over the older rule-of-thumb of swap equal to or
  double RAM; excessive swap on a memory-constrained host often
  masks a capacity problem rather than solving it, at the cost of
  severe performance degradation once swapping becomes sustained.
- **Stratis/VDO vs. plain LVM+filesystem.** Choose Stratis when
  operational simplicity for local storage matters more than
  fine-grained manual control; choose VDO specifically when the
  workload's data reduction ratio justifies its CPU overhead — neither
  is a default choice over LVM+XFS for a typical general-purpose
  volume.
- **NFS vs. Samba vs. block storage (iSCSI, covered in [Volume VI](../../volume-06-enterprise-storage-data-protection/README.md)).**
  NFS is the natural choice for Linux-to-Linux file sharing; Samba is
  required wherever Windows clients or SMB-only tooling is in the mix;
  neither is a substitute for shared block storage when an application
  specifically requires POSIX-local block semantics (a database data
  directory, for example) rather than a network filesystem.
- **autofs vs. persistent fstab mounts for network shares.** A
  network mount needed continuously by a service should still be a
  managed `.mount` unit or fstab entry with appropriate
  `_netdev`/timeout options; autofs is the better fit for
  intermittently accessed, user-facing paths (home directories, shared
  project space) where holding the mount open indefinitely wastes
  server-side resources.

## Implementation and Automation

### 1. Partitioning a disk with parted

```bash
# Inspect current block devices
lsblk
blkid

# Create a GPT label and a single primary partition using the full disk
parted /dev/sdb --script mklabel gpt
parted /dev/sdb --script mkpart primary 0% 100%
parted /dev/sdb --script print

# Inform the kernel of the new partition table without a reboot
partprobe /dev/sdb
```

### 2. Building the LVM stack

```bash
# Initialize the partition as a physical volume
pvcreate /dev/sdb1
pvs

# Create a volume group
vgcreate vg_data /dev/sdb1
vgs

# Create a logical volume, leaving headroom in the VG
lvcreate -n lv_appdata -L 20G vg_data
lvs

# Extend the logical volume and grow the filesystem on top of it live
lvextend -L +10G /dev/vg_data/lv_appdata
xfs_growfs /dev/vg_data/lv_appdata      # for XFS
# resize2fs /dev/vg_data/lv_appdata     # for ext4

# Create and roll back to an LVM snapshot
lvcreate -s -n lv_appdata_snap -L 5G /dev/vg_data/lv_appdata
lvconvert --merge /dev/vg_data/lv_appdata_snap
```

### 3. Filesystem creation and persistent mounting

```bash
# Format with XFS (default) or ext4
mkfs.xfs /dev/vg_data/lv_appdata
# mkfs.ext4 /dev/vg_data/lv_appdata

# Create a mount point and mount temporarily to verify
mkdir -p /appdata
mount /dev/vg_data/lv_appdata /appdata

# Determine the UUID for a stable fstab entry
blkid /dev/vg_data/lv_appdata

# Persist the mount by UUID
cat >> /etc/fstab <<'EOF'
UUID=<filesystem-uuid>  /appdata  xfs  defaults  0 0
EOF

# Validate fstab before rebooting on it
mount -a
findmnt /appdata
```

### 4. Swap configuration

```bash
# Create a dedicated swap logical volume
lvcreate -n lv_swap -L 4G vg_data
mkswap /dev/vg_data/lv_swap
swapon /dev/vg_data/lv_swap

# Persist in fstab
echo "/dev/vg_data/lv_swap  swap  swap  defaults  0 0" >> /etc/fstab

# Inspect and tune swappiness
cat /proc/sys/vm/swappiness
sysctl vm.swappiness=10
echo "vm.swappiness=10" > /etc/sysctl.d/99-swappiness.conf
```

### 5. Stratis and VDO basics

```bash
# Stratis: create a pool and a filesystem in one short workflow
dnf install -y stratisd stratis-cli
systemctl enable --now stratisd
stratis pool create pool1 /dev/sdc
stratis filesystem create pool1 fs1
lsblk

# VDO: create a deduplicated/compressed volume beneath a filesystem
dnf install -y vdo kmod-kvdo
vdo create --name=vdo1 --device=/dev/sdd --vdoLogicalSize=100G
mkfs.xfs /dev/mapper/vdo1
```

### 6. NFS server and client

```bash
# Server: install, export, and open the firewall
dnf install -y nfs-utils
mkdir -p /srv/nfs/projects
echo "/srv/nfs/projects  10.10.10.0/24(rw,sync,no_root_squash)" >> /etc/exports
systemctl enable --now nfs-server
exportfs -rav
firewall-cmd --add-service=nfs --permanent
firewall-cmd --reload

# Client: discover exports, then mount
showmount -e nfs-server.example.com
mkdir -p /mnt/projects
mount -t nfs nfs-server.example.com:/srv/nfs/projects /mnt/projects

# Persist the client mount
echo "nfs-server.example.com:/srv/nfs/projects  /mnt/projects  nfs  defaults,_netdev  0 0" >> /etc/fstab
```

### 7. Samba share

```bash
dnf install -y samba
mkdir -p /srv/samba/shared
chmod 2770 /srv/samba/shared

cat >> /etc/samba/smb.conf <<'EOF'
[shared]
   path = /srv/samba/shared
   valid users = @smbusers
   read only = no
EOF

smbpasswd -a jsmith
systemctl enable --now smb nmb
firewall-cmd --add-service=samba --permanent
firewall-cmd --reload
```

### 8. autofs for on-demand mounting

```bash
dnf install -y autofs
echo "/mnt/auto  /etc/auto.projects" >> /etc/auto.master
echo "projects  -fstype=nfs,rw  nfs-server.example.com:/srv/nfs/projects" >> /etc/auto.projects
systemctl enable --now autofs
```

## Validation and Troubleshooting

- **Confirm the storage stack end to end.** `lsblk -f` shows the full
  device-to-mountpoint chain including filesystem type and UUID in
  one view; `pvs`, `vgs`, `lvs` (or `vgdisplay`, `lvdisplay` for more
  detail) confirm each LVM layer independently when something is
  wrong at a specific level.
- **Diagnose a failed mount.** `mount -a` after editing `/etc/fstab`
  surfaces syntax and device errors immediately, before a reboot turns
  a typo into a boot-time emergency-mode incident; `findmnt <path>`
  confirms what is actually mounted where, and `journalctl -b` shows
  mount failures logged during boot.
- **Diagnose a full or nearly full filesystem.** `df -hT` shows
  filesystem-level usage; `du -h --max-depth=1 <path> | sort -rh`
  finds the largest consumers quickly. For XFS, remember that
  `df` free space cannot be reclaimed by shrinking — the fix is
  extending the LV (if VG space is available) or reducing consumed
  data.
- **Diagnose a degraded or inconsistent LVM state.**
  `pvs`/`vgs`/`lvs -o +devices` shows which physical devices back each
  logical volume; a missing PV shows as `PV unknown device` in `pvs`
  output, at which point `vgreduce --removemissing` is a last-resort
  recovery step only after confirming the device is truly gone and
  not merely renamed.
- **Diagnose a filesystem needing repair.** `xfs_repair` (only on an
  **unmounted** XFS filesystem) or `fsck.ext4` (similarly unmounted)
  should be run after an unclean shutdown if the filesystem fails to
  mount cleanly; never run a repair tool on a mounted filesystem.
- **Diagnose an NFS mount that hangs or fails.** `showmount -e
  <server>` confirms the export is visible and the network path is
  open; `rpcinfo -p <server>` confirms the required RPC services are
  registered; a client hang (rather than a fast failure) usually
  means the network path is blocked (firewall) rather than the NFS
  service being down outright — NFS's default behavior is to retry
  indefinitely for a hard-mounted share.
- **Diagnose a Samba access denial.** `testparm` validates
  `smb.conf` syntax; `smbclient -L localhost -U <user>` tests
  authentication and share visibility locally before troubleshooting
  from a remote Windows client; confirm the account exists in the
  Samba password database (`pdbedit -L`), which is separate from the
  Linux system account password.
- **Common failure: forgetting `_netdev` on network filesystem fstab
  entries.** Without `_netdev` (or using autofs instead), a boot can
  hang or fail waiting for a network mount that is not yet reachable
  because networking has not finished initializing.

## Security and Best Practices

- Reference filesystems in `/etc/fstab` by UUID, not device path, so a
  device-enumeration change never silently mounts the wrong filesystem
  at a critical path.
- Scope NFS exports to specific client networks (never `*` in
  production) and avoid `no_root_squash` unless a specific, understood
  requirement demands it — squashing root prevents a client's root
  user from acting as root on the exported filesystem.
- Require authenticated Samba access (`valid users =`, backed by
  `smbpasswd` or directory integration) rather than any form of
  anonymous/guest share access for anything beyond a genuinely public
  read-only share.
- Set restrictive permissions and ownership at both the filesystem
  level and the sharing-protocol level (NFS export options, Samba
  `valid users`/`write list`) — a share is only as restrictive as the
  more permissive of the two layers.
- Encrypt data at rest for volumes holding sensitive data using LUKS
  (covered in depth in [Chapter 06](06-selinux-permissions-cryptography-and-system-hardening.md)) beneath the LVM/filesystem layer,
  not as an afterthought applied only to specific files.
- Monitor filesystem and volume group free space proactively
  (threshold-based alerting, not manual checks) — an XFS filesystem
  that fills completely can cause application-level failures that are
  disproportionately disruptive to diagnose compared to the simplicity
  of the underlying cause.
- Test LVM snapshot and Stratis/VDO recovery procedures before relying
  on them operationally; a snapshot or reduction technology that has
  never been exercised is not a verified recovery capability.

## References and Knowledge Checks

**References**

- `parted(8)`, `lsblk(8)`, `blkid(8)` man pages.
- `pvcreate(8)`, `vgcreate(8)`, `lvcreate(8)`, `lvextend(8)` man pages.
- `xfs_growfs(8)`, `xfs_repair(8)`, `mkfs.ext4(8)`, `fsck(8)` man
  pages.
- `exports(5)`, `nfs(5)`, `smb.conf(5)` man pages.
- Red Hat Enterprise Linux 10 Managing Storage Devices guide — LVM,
  Stratis, and VDO chapters, Red Hat Customer Portal.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — RHEL 10
  baseline referenced throughout this chapter.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  RHCSA (EX200) blueprint mapping for this volume.

**Knowledge checks**

1. Why does adding a physical volume to a volume group not, by
   itself, change the size of any existing logical volume?
2. Why must `/etc/fstab` entries reference filesystems by UUID rather
   than device path in production environments?
3. What operational constraint does XFS have that ext4 does not, and
   how does that constraint change volume-sizing strategy?
4. Why does an NFS export's `no_root_squash` option carry security
   risk, and what is the default behavior it overrides?

## Hands-On Lab

**Objective:** Build a complete LVM-backed filesystem from an
unpartitioned disk, extend it live, configure swap on the same volume
group, and export the filesystem over NFS to a second host.

**Prerequisites**

- A RHEL 10 host or VM with root/sudo access and at least one spare,
  unpartitioned virtual disk (`/dev/sdb` in this lab) of 10 GB or
  larger.
- A second RHEL 10 host or VM on the same network to act as an NFS
  client (a single host can simulate both roles using `localhost` if a
  second host is unavailable).

**Steps**

1. Partition the spare disk and build the LVM stack:

   ```bash
   sudo parted /dev/sdb --script mklabel gpt
   sudo parted /dev/sdb --script mkpart primary 0% 100%
   sudo partprobe /dev/sdb
   sudo pvcreate /dev/sdb1
   sudo vgcreate vg_lab /dev/sdb1
   sudo lvcreate -n lv_share -L 4G vg_lab
   ```

2. Format, mount, and persist the filesystem:

   ```bash
   sudo mkfs.xfs /dev/vg_lab/lv_share
   sudo mkdir -p /srv/nfs/lab-share
   sudo mount /dev/vg_lab/lv_share /srv/nfs/lab-share
   UUID=$(sudo blkid -s UUID -o value /dev/vg_lab/lv_share)
   echo "UUID=${UUID}  /srv/nfs/lab-share  xfs  defaults  0 0" | sudo tee -a /etc/fstab
   sudo mount -a
   findmnt /srv/nfs/lab-share
   ```

   **Expected result:** `findmnt` shows `/srv/nfs/lab-share` mounted
   from `/dev/mapper/vg_lab-lv_share` with filesystem type `xfs`.

3. Extend the logical volume live and grow the filesystem:

   ```bash
   sudo lvextend -L +2G /dev/vg_lab/lv_share
   sudo xfs_growfs /srv/nfs/lab-share
   df -hT /srv/nfs/lab-share
   ```

   **Expected result:** the filesystem now reports approximately 6 GB
   total size without an unmount.

4. Add a swap logical volume in the same volume group:

   ```bash
   sudo lvcreate -n lv_swap -L 1G vg_lab
   sudo mkswap /dev/vg_lab/lv_swap
   sudo swapon /dev/vg_lab/lv_swap
   echo "/dev/vg_lab/lv_swap  swap  swap  defaults  0 0" | sudo tee -a /etc/fstab
   swapon --show
   ```

5. Export the filesystem over NFS and confirm from the client host:

   ```bash
   sudo dnf install -y nfs-utils
   echo "/srv/nfs/lab-share  10.10.10.0/24(rw,sync,no_root_squash)" | sudo tee -a /etc/exports
   sudo systemctl enable --now nfs-server
   sudo exportfs -rav
   sudo firewall-cmd --add-service=nfs --permanent
   sudo firewall-cmd --reload

   # From the client host:
   showmount -e <lab-server-ip>
   sudo mkdir -p /mnt/lab-share
   sudo mount -t nfs <lab-server-ip>:/srv/nfs/lab-share /mnt/lab-share
   echo "hello from client" | sudo tee /mnt/lab-share/test.txt
   ```

   **Expected result:** `test.txt` appears in `/srv/nfs/lab-share` on
   the server, confirming a working two-way NFS mount.

6. **Negative test:** attempt to mount the export from a source
   outside the permitted network and confirm it is refused:

   ```bash
   # Temporarily narrow the export to a network the client is NOT on
   sudo sed -i 's#10.10.10.0/24#192.0.2.0/24#' /etc/exports
   sudo exportfs -rav
   # From the client host (which is not on 192.0.2.0/24):
   sudo umount /mnt/lab-share
   sudo mount -t nfs <lab-server-ip>:/srv/nfs/lab-share /mnt/lab-share
   ```

   **Expected result:** the mount attempt fails with a permission or
   access error, confirming the export's client restriction is
   enforced.

7. **Cleanup:**

   ```bash
   # Client
   sudo umount -f /mnt/lab-share 2>/dev/null
   sudo rmdir /mnt/lab-share

   # Server
   sudo sed -i '/lab-share/d' /etc/exports
   sudo exportfs -rav
   sudo firewall-cmd --remove-service=nfs --permanent
   sudo firewall-cmd --reload
   sudo swapoff /dev/vg_lab/lv_swap
   sudo umount /srv/nfs/lab-share
   sudo sed -i '/vg_lab/d' /etc/fstab
   sudo lvremove -f /dev/vg_lab/lv_swap /dev/vg_lab/lv_share
   sudo vgremove vg_lab
   sudo pvremove /dev/sdb1
   sudo rmdir /srv/nfs/lab-share
   ```

## Summary and Completion Checklist

RHEL 10 storage layers partitions, LVM, and a filesystem into a stack
that supports live growth, snapshots, and consistent naming through
UUIDs — with XFS as the default filesystem and ext4 available where
its different constraints (including in-place shrink) are needed.
Stratis and VDO extend that model for simplified local pools and
inline data reduction, respectively, without replacing the underlying
LVM concepts. NFS and Samba extend the same storage outward across the
network, each with its own authentication and authorization model that
must be secured independently of filesystem permissions.

- [ ] Can partition a disk with GPT and build a full LVM stack from
      physical volume to mounted filesystem.
- [ ] Can extend a logical volume and its filesystem live, and create
      an LVM snapshot.
- [ ] Can configure swap and explain current swap-sizing guidance.
- [ ] Can explain when Stratis or VDO is a better fit than plain
      LVM and a filesystem.
- [ ] Can configure and secure an NFS export and a Samba share.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
