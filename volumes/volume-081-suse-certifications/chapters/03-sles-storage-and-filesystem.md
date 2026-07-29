# Chapter 03: SLES Storage and Filesystem

## Learning Objectives

- Understand the Btrfs filesystem and Snapper snapshots.
- Perform system rollback with snapshots.
- Manage storage with LVM and partitions.
- Mount and manage filesystems.
- Complete a walkthrough for each storage/filesystem topic.

## Theory and Architecture

SLES's signature storage feature is **Btrfs with Snapper**. **Btrfs** is a copy-on-write filesystem;
SLES uses it for the root filesystem and integrates **Snapper**, which takes automatic **snapshots**
before and after system changes (a zypper install, a YaST config change). Because snapshots are
cheap copy-on-write states, an administrator can **roll back** the entire system to a pre-change
snapshot if an update breaks something — a powerful safety net unique to the SUSE experience. Beyond
Btrfs, SLES manages storage with the **Logical Volume Manager (LVM)** — physical volumes, volume
groups, and logical volumes that can be resized flexibly — plus standard partitioning and filesystems
(XFS for data volumes is common). The **Storage Management** and **Linux Filesystem** exam domains
cover mounting (`/etc/fstab`), filesystem types, LVM, and the Btrfs/Snapper workflow. This chapter
teaches each with a hands-on walkthrough (Snapper snapshots, LVM, and filesystem management).

## Design Considerations

Use **Btrfs + Snapper** on root for **rollback** safety; XFS/LVM for flexible data volumes. Take (or
rely on automatic) **snapshots** before risky changes. Manage capacity with **LVM** (resize without
downtime). Mount via **/etc/fstab** with correct options. Monitor filesystem usage.

## Implementation and Automation

The labs list Snapper snapshots, reason about rollback, and manage LVM.

## Validation and Troubleshooting

Confirm the storage model:

```text
Btrfs (copy-on-write root) + Snapper (auto snapshots before/after changes) -> system rollback safety net. LVM (PV/VG/LV, flexible resize). XFS common for data. Mount via /etc/fstab.
SCA domains: Linux Filesystem, Storage Management.
```

Common pitfalls: assuming an update is irreversible on SLES (**Snapper rollback** exists); and filling
the root filesystem with snapshots (manage retention).

## Security and Best Practices

Rely on **Btrfs/Snapper** rollback for safe updates, manage capacity with **LVM**, mount correctly via
**fstab**, and monitor usage/snapshot retention. All work is authorized administration.

## Hands-On Lab

Storage walkthroughs. **Shared prerequisites** — a SLES/openSUSE VM (Snapper/Btrfs) or read the
commands; `python3`. **Cost:** none.

### Lab 3.1 — List Snapper snapshots

**Objective:** See the rollback safety net.

```bash
snapper list 2>/dev/null | head || echo "snapper list: pre/post snapshots around each change (zypper/YaST)"
echo "SLES: Snapper auto-snapshots before + after system changes on Btrfs root"
```

**Expected result:** the **Snapper** pre/post snapshots — SLES's change safety net.

**Negative test:** assume a bad `zypper patch` can't be undone; **Snapper rollback** reverts it — use
it.

**Cleanup:** none (read-only).

### Lab 3.2 — Reason about a rollback

**Objective:** Recover from a bad change.

```python
python3 - <<'PY'
change={"action":"zypper patch broke a service","pre_snapshot":42,"post_snapshot":43}
print(f"snapshots: pre={change['pre_snapshot']} (good), post={change['post_snapshot']} (broken)")
print("recovery: 'snapper rollback 42' (or boot into snapshot 42) -> system restored to pre-change state")
PY
```

**Expected result:** rolling back to the **pre-change snapshot** to recover — Btrfs/Snapper rollback.

**Negative test:** rebuild the server from scratch after a bad update; **snapshot rollback** is minutes
— use it first.

**Cleanup:** none.

### Lab 3.3 — Manage storage with LVM

**Objective:** Flexible capacity.

```bash
# LVM layers: physical volume -> volume group -> logical volume
pvs 2>/dev/null | head || echo "pvs/vgs/lvs: physical volumes, volume groups, logical volumes"
echo "resize a logical volume + filesystem (lab): lvextend -L +5G /dev/vg0/data && xfs_growfs /data"
```

**Expected result:** the **LVM** layers and an online resize — flexible SLES storage.

**Negative test:** create fixed partitions with no LVM; growing them later is hard — use **LVM** for
flexibility.

**Cleanup:** none.

### Lab 3.4 — Mount a filesystem via fstab

**Objective:** Persistent mounts.

```bash
findmnt / 2>/dev/null | head || cat /etc/fstab 2>/dev/null | grep -v '^#' | head
echo "SLES: /etc/fstab defines persistent mounts (device/UUID, mountpoint, fs type, options)"
```

**Expected result:** the persistent mount configuration in **/etc/fstab** — filesystem management.

**Negative test:** `mount` a filesystem manually only; it's gone after reboot — add it to **fstab**.

**Cleanup:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SLES storage centers on Btrfs with Snapper for snapshot-based system rollback, LVM for flexible
capacity, and standard filesystem mounting via fstab — the Storage Management and Filesystem domains
with SUSE's signature safety net.

- [ ] I can list Snapper snapshots.
- [ ] I can reason about a rollback.
- [ ] I can manage storage with LVM.
- [ ] I can mount a filesystem via fstab.
- [ ] I completed Labs 3.1–3.4 including each negative test.
