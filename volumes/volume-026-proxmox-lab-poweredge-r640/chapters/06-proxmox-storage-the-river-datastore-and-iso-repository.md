# Chapter 06: Proxmox Storage — The `river` Datastore and ISO Repository

## Learning Objectives

- Add the `river` RAID 5 array to Proxmox as virtual-machine storage.
- Choose an appropriate storage type for VM disks on `river`.
- Create an ISO repository on `river` to hold installation media.
- Understand Proxmox content types and which storage holds what.
- Verify both the VM datastore and the ISO repository are usable.

## Theory and Architecture

### From a RAID array to Proxmox storage

The `river` RAID 5 array from
[Chapter 02](02-storage-boss-boot-mirror-and-the-river-raid-5-array.md)
exists at the hardware level, but Proxmox does not use it until it is added
as a **storage** in Proxmox's own configuration. This chapter makes `river`
serve two purposes:

- **Virtual-machine storage** — the disks of the ten VMs live here.
- **An ISO repository** — the installation media (`.iso` files) the VMs are
  built from live here too.

Both sit on the same physical array, but Proxmox treats them as different
*content types* on that storage, which is the concept to understand.

### Proxmox content types

A Proxmox storage declares which **content types** it holds. The ones that
matter here:

- **`images`** — virtual machine disk images. This is what makes `river`
  usable as VM storage.
- **`iso`** — ISO installation media. This is what makes the ISO repository.
- Others (`vztmpl`, `backup`, `snippets`) exist but are not the focus of
  this build.

A single storage can hold multiple content types, or you can define separate
storages on the same underlying array for clarity. This build treats
`river` as holding VM images, and establishes an ISO repository — either as
an additional content type on the same storage or as a directory storage
pointed at a path on `river`.

### Choosing the storage type for VM disks

Proxmox can present `river` to VMs in several ways, and the choice affects
features and performance:

- **LVM-Thin** — thin-provisioned logical volumes on the array; supports
  snapshots and efficient space use. A common, capable default for local VM
  storage on a single node.
- **Directory** — a filesystem on the array holding disk-image files
  (qcow2/raw); simplest, flexible, and the natural home for the ISO
  repository since ISOs are files.
- **ZFS** — powerful (snapshots, checksums) but layered on top of hardware
  RAID it adds complexity; on a hardware-RAID array like `river`, a simpler
  type is usually the better fit.

For VM disks on a hardware-RAID array, **LVM-Thin** is a strong choice
(snapshots, thin provisioning). For the **ISO repository**, a **directory**
content type is natural because ISOs are ordinary files. This build uses
`river` for VM images and a directory-backed ISO content type on the same
array.

## Design Considerations

- **Keep VM storage and the ISO repository on `river`, off the boot
  mirror.** The BOSS mirror holds only Proxmox; VM disks and ISOs belong on
  the capacity array. Pointing either at the boot device would fill the small
  mirror.
- **Pick a VM storage type that supports snapshots if you want them.**
  LVM-Thin and ZFS support snapshots; plain directory with raw images does
  not (qcow2 in a directory does). For a lab where rolling a VM back is
  useful, choose accordingly.
- **Give the ISO repository room for a large library.** This build stores
  nine ISOs, several of them multi-gigabyte (Windows, CML); ensure the
  content type has access to enough of `river`'s capacity.
- **Name storages clearly.** A storage named `river` (or `river-vm` and
  `river-iso`) is self-documenting; obscure names make later operations
  error-prone.

## Implementation and Automation

Storage is added through the web UI (Datacenter → Storage → Add) or the
`pvesm` command line.

### 1. Adding `river` as VM storage

If `river` is presented as an LVM volume group, add it as LVM-Thin:

```bash
# Create a thin pool on the river volume group (if not already), then add it.
# (Assumes river is an LVM VG on the RAID 5 array.)
pvesm add lvmthin river-vm --vgname river --thinpool riverdata \
  --content images
```

Or, to use a directory on a filesystem mounted from `river`:

```bash
# A filesystem mounted from the river array, holding VM images and ISOs.
mkdir -p /mnt/river
# (Mount the river filesystem at /mnt/river via /etc/fstab.)
pvesm add dir river --path /mnt/river --content images,iso
```

### 2. Creating the ISO repository

If VM storage is LVM-Thin (which cannot hold ISO files, being block
storage), the ISO repository is a **directory** content type on a filesystem
from `river`:

```bash
# A directory storage on river dedicated to ISO media.
mkdir -p /mnt/river/template/iso
pvesm add dir river-iso --path /mnt/river --content iso
```

Proxmox expects ISOs under `<path>/template/iso/`; the directory storage
exposes that path in the UI as the place to upload or store ISO files, which
[Chapter 07](07-building-the-iso-library.md) populates.

### 3. Verifying the storages

```bash
# Both storages should be active and enabled.
pvesm status

# The ISO storage should accept iso content; the VM storage, images.
pvesm list river-iso        # lists ISO content (empty until Chapter 07)
```

The web UI shows each storage under the node, with the ISO storage offering
an upload/import option and the VM storage available as a disk target when
creating a VM.

## Validation and Troubleshooting

### Confirming the storages are usable

| Check | Expectation | Failure means |
| --- | --- | --- |
| `pvesm status` | `river` VM storage and ISO storage active | Storage not added, or path/VG missing |
| VM storage holds `images` | Available as a disk target | Wrong content type declared |
| ISO storage holds `iso` | Offers ISO upload/import | ISO content type not set, or wrong path |
| Both on `river`, not BOSS | Capacity matches the RAID 5 array | Pointed at the boot mirror by mistake |

### The block-storage-cannot-hold-ISOs gotcha

A frequent confusion: LVM-Thin (and other block storage) holds VM *images*
but **cannot hold ISO files**, because ISOs are files and block storage has
no filesystem to put them in. If the ISO upload option does not appear, the
cause is usually trying to store ISOs on block storage. The fix is a
**directory** content type on a filesystem from `river` — which is why this
build establishes a directory storage for the ISO repository even when VM
disks use LVM-Thin.

### Pointing storage at the wrong array

If a storage shows far less capacity than expected, confirm it is backed by
`river` (the RAID 5 array) and not the small BOSS boot mirror. VM disks or a
growing ISO library on the boot mirror will fill it quickly and can destabilize
the node.

## Security and Best Practices

- **Keep the boot device free of VM data and ISOs.** The hypervisor's boot
  mirror stays small and dedicated; everything else lives on `river`.
- **Protect the ISO repository's integrity.** ISOs become running systems;
  storing only checksum-verified media (Chapter 07) keeps a compromised
  image from becoming a compromised VM.
- **Back up VM configurations and critical VM data off `river`.** RAID 5
  tolerates a drive, not a catastrophe; the availability-is-not-backup
  principle applies to the VM datastore as much as anywhere.
- **Restrict who can add or modify storage.** Storage definitions control
  where every VM's data lives; changing them is a privileged operation.

## References and Knowledge Checks

**References**

- [Proxmox VE storage documentation](https://pve.proxmox.com/wiki/Storage)
  — storage types, content types, and configuration.
- [Chapter 02](02-storage-boss-boot-mirror-and-the-river-raid-5-array.md)
  — the `river` RAID 5 array this chapter adds to Proxmox.
- [Volume VI, Chapter 01](../../volume-006-enterprise-storage-data-protection/chapters/01-enterprise-storage-architecture-and-service-design.md)
  — storage architecture and service design vocabulary.

**Knowledge checks**

1. What must happen before Proxmox can use the `river` RAID 5 array for VMs?
2. What are Proxmox content types, and which two matter for this build?
3. Why can LVM-Thin hold VM disks but not ISO files, and what storage type
   holds ISOs?
4. Where does Proxmox expect ISO files to live under a directory storage?
5. How would you notice a storage accidentally pointed at the BOSS mirror
   instead of `river`?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each storage-configuration step** — turning
the `river` RAID-5 array into a Proxmox datastore, setting content types, and an ISO repository.
Commands are runnable Proxmox storage CLI (`pvesm`). Each ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 6.1–6.4** — a Proxmox node with the `river` RAID-5 virtual disk
(Chapter 02) presented as a block device, and root SSH. **Cost:** none.

### Lab 6.1 — Create the `river` datastore (Topic: VM datastore)

**Objective:** Make the RAID-5 array a Proxmox storage for VM disks.

```bash
lsblk                                        # identify the 'river' block device (e.g. /dev/sdb)
# Create an LVM-thin pool on it (thin provisioning + snapshots on hardware RAID):
pvcreate /dev/sdb
vgcreate river /dev/sdb
lvcreate -l 95%FREE --thinpool riverpool river
pvesm add lvmthin river --vgname river --thinpool riverpool --content images,rootdir
pvesm status
```

**Expected result:** an LVM-thin storage named `river` for VM disks and containers appears in
`pvesm status` — on a hardware-RAID array, **LVM-thin** gives thin provisioning and snapshots
without stacking ZFS on the RAID controller; this is the datastore the ten VMs will use.

**Negative test:** put ZFS directly on the hardware-RAID `river` device for its features; ZFS cannot
see or manage the individual disks behind the PERC, losing its self-healing/scrub value — LVM-thin
is the appropriate layer on hardware RAID.

**Cleanup:** keep `river` (it is the build's VM datastore).

### Lab 6.2 — Storage content types (Topic: Content types)

**Objective:** Understand what each storage may hold.

```bash
pvesm status --content images        # storages that can hold VM disk images
cat /etc/pve/storage.cfg
```

**Expected result:** `storage.cfg` shows each storage's allowed **content** — `images` (VM disks),
`rootdir` (container filesystems), `iso` (install media), `vztmpl` (container templates), `backup`
(vzdump archives), `snippets` — a storage only accepts the content types it is configured for, so
`river` holds images/rootdir while ISOs go elsewhere.

**Negative test:** try to upload an ISO to a storage whose content is only `images`; Proxmox refuses
it — the content-type setting governs what a storage can store, so ISO media needs an `iso`-capable
storage (Lab 6.3).

**Cleanup:** none.

### Lab 6.3 — ISO repository storage (Topic: ISO repository)

**Objective:** Provide a place for install media.

```bash
# A directory storage on 'river' (or local) for ISOs and container templates:
mkdir -p /river/template/iso /river/template/cache
pvesm add dir riverfiles --path /river --content iso,vztmpl,backup
pvesm status --content iso
```

**Expected result:** a directory storage (`riverfiles`) that accepts `iso`, container templates, and
backups — the ISO repository (Chapter 07) needs an `iso`-content storage; a directory storage on the
`river` array keeps install media on the large array rather than the small boot mirror.

**Negative test:** store ISOs on the small BOSS boot mirror (`local`); it fills quickly and risks the
OS volume — put the ISO library on the large `river` array where there is room.

**Cleanup:** remove `riverfiles` only if reworking the storage layout.

### Lab 6.4 — Verify storage (Topic: Verification)

**Objective:** Confirm all storages are online with expected capacity.

```bash
pvesm status
pvesh get /nodes/pve01/storage --output-format json | python3 -c "import json,sys; [print(s['storage'], s['type'], s.get('content')) for s in json.load(sys.stdin)]"
```

**Expected result:** `local` (boot mirror, small), `river` (LVM-thin, large, images/rootdir), and
`riverfiles` (dir, iso/backup) all active with correct sizes — verifying the storage layout confirms
VM disks will land on the RAID-5 array and ISOs/backups have a home before you build VMs.

**Negative test:** deploy VMs before confirming `river` is active; if the LVM-thin pool failed to
create, VM disks fall back to the tiny boot mirror and fill it — verify storage is online and sized
first.

**Cleanup:** none (read-only).

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The `river` RAID 5 array becomes usable only once it is added to Proxmox as
storage, and this build gives it two roles through Proxmox's content-type
model: `images` for the ten VMs' disks and `iso` for the installation media
they are built from. Both sit on `river` and off the small BOSS boot mirror.
VM disks suit a snapshot-capable type such as LVM-Thin, while the ISO
repository must be a directory (filesystem) storage — because ISOs are
files and block storage cannot hold them, which is the most common storage
confusion in this phase. With the VM datastore and ISO repository confirmed
active on the capacity array, the build is ready to assemble its ISO library
and deploy the virtual machines.

- [ ] `river` added as VM storage with content type `images`.
- [ ] A directory-backed ISO repository on `river` with content type `iso`.
- [ ] `pvesm status` shows both active.
- [ ] Both confirmed backed by `river`, not the BOSS mirror.
- [ ] ISO storage offers upload/import for Chapter 07.
