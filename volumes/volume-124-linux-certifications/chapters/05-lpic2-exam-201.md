# Chapter 05: LPIC-2 — Exam 201 (201-450)

## Learning Objectives

- Cover exam 201-450's seven topics with a walkthrough lab each.
- Drill capacity planning, kernel work, startup, filesystems, storage, networking, and maintenance.
- Work from the published v4.5 objectives.

## The exam in brief

**Exam:** 201-450 (objectives v4.5), the first of LPIC-2's two exams; requires an **active LPIC-1**. Seven topics: **200 Capacity Planning**, **201 Linux Kernel**, **202 System Startup**, **203 Filesystem and Devices**, **204 Advanced Storage Device Administration**, **205 Networking Configuration**, **206 System Maintenance**.

## Hands-On Lab

A Linux VM you can afford to break. **Cost:** none.

### Lab 5.1 — Capacity planning (Topic 200)

**Objective:** Measure before predicting.

```bash
vmstat 1 3 | tail -2
iostat 2>/dev/null | head -6 || echo "install sysstat for iostat/sar"
free -h | head -2
uptime
```

**Expected result:** CPU/memory/IO snapshots (`vmstat` columns: r=runnable, wa=IO wait), device throughput, memory with buffers/cache distinguished from used, and load averages — Topic 200 is reading these (plus `sar` trends, `top/htop`) and predicting growth from them.

**Negative test:** Reading high "used" memory in `free` as exhaustion while cache holds most of it — available, not used, is the number; the exam tests exactly this misread.

**Cleanup:** None.

### Lab 5.2 — Linux kernel (Topic 201)

**Objective:** Query, load, and parameterize kernel components.

```bash
uname -r
ls /lib/modules/$(uname -r)/kernel/ | head -4
sudo modprobe dummy numdummies=1 2>/dev/null && ip -brief link | grep dummy || echo "dummy module unavailable"
modinfo dummy 2>/dev/null | head -4
sudo sysctl vm.swappiness
sudo modprobe -r dummy 2>/dev/null
```

**Expected result:** The running kernel version, its module tree, the `dummy` module loaded with a parameter and its interface visible, `modinfo` metadata, and a `sysctl` value read — Topic 201's practice: modules (`modprobe/lsmod/modinfo`), parameters, `/proc` and `sysctl`, and awareness of building/patching kernels and initramfs.

**Negative test:** `modprobe` a nonexistent module — the error distinguishes missing module from bad parameters; both appear in exam scenarios.

**Cleanup:** Done in the walkthrough.

### Lab 5.3 — System startup (Topic 202)

**Objective:** Trace and influence the boot path.

```bash
systemctl list-dependencies multi-user.target --no-pager | head -8
systemd-analyze 2>/dev/null | head -1
ls /boot | head -5
grep -m1 GRUB_CMDLINE_LINUX /etc/default/grub 2>/dev/null || true
```

**Expected result:** The target dependency tree, boot-time analysis, the kernel/initramfs files in `/boot`, and the GRUB command line — Topic 202: GRUB 2 configuration and recovery, systemd units/targets, and rescuing a system that won't boot (single-user/rescue targets, `init=/bin/sh`).

**Negative test:** Edit `/etc/default/grub` without running `update-grub`/`grub2-mkconfig` — the change never takes effect; the two-step is the exam's favorite startup gotcha.

**Cleanup:** None (read-only).

### Lab 5.4 — Filesystem and devices (Topic 203)

**Objective:** Operate beyond mkfs: tune, label, and auto-mount.

```bash
dd if=/dev/zero of=fs.img bs=1M count=64 status=none && mkfs.ext4 -q fs.img
tune2fs -L LABFS fs.img && blkid fs.img
echo "fstab entry: LABEL=LABFS /mnt/lab ext4 defaults,noatime 0 2"
sudo mount -o loop fs.img /mnt 2>/dev/null && mount | grep fs.img; sudo umount /mnt 2>/dev/null
```

**Expected result:** A labeled filesystem, `blkid` showing LABEL and UUID, and the fstab grammar (device-by-label, mount point, type, options, dump, fsck order) — Topic 203: creating/tuning filesystems (`tune2fs`), UUID/label mounting, `/etc/fstab`, automount, and udev device naming.

**Negative test:** An fstab entry with a wrong UUID boots into emergency mode — why label/UUID hygiene is a boot-reliability issue, not cosmetics.

**Cleanup:** `rm fs.img`.

### Lab 5.5 — Advanced storage (Topic 204)

**Objective:** Build software RAID and LVM from loop devices.

```bash
for i in 1 2; do dd if=/dev/zero of=pv$i.img bs=1M count=64 status=none; done
L1=$(sudo losetup -f --show pv1.img); L2=$(sudo losetup -f --show pv2.img)
sudo mdadm --create /dev/md99 --level=1 --raid-devices=2 $L1 $L2 --run 2>/dev/null && cat /proc/mdstat | head -3
sudo mdadm --stop /dev/md99; sudo pvcreate $L1 $L2 && sudo vgcreate labvg $L1 $L2 && sudo lvcreate -L 32M -n lablv labvg
sudo lvs labvg
sudo vgremove -f labvg; sudo losetup -d $L1 $L2
```

**Expected result:** A RAID-1 array assembling in `/proc/mdstat`, then the same disks re-used as an LVM stack (`pvcreate → vgcreate → lvcreate`) with `lvs` showing the LV — Topic 204's two pillars, mdadm RAID and LVM (plus resizing and iSCSI awareness), built harmlessly on loop devices.

**Negative test:** `lvcreate` larger than the VG — "insufficient free space"; capacity flows PV→VG→LV, and the error proves the hierarchy.

**Cleanup:** `rm pv1.img pv2.img`.

### Lab 5.6 — Networking configuration (Topic 205)

**Objective:** Configure beyond the client basics of LPIC-1.

```bash
sudo ip link add lab0 type dummy && sudo ip addr add 192.0.2.10/24 dev lab0 && sudo ip link set lab0 up
ip -brief addr show lab0
sudo ip route add 198.51.100.0/24 via 192.0.2.1 dev lab0 && ip route | grep 198.51
sudo tcpdump -i lab0 -c 1 -w /dev/null 2>&1 | tail -1 &
sleep 1; sudo ip link del lab0
```

**Expected result:** A dummy interface addressed and up, a static route through it, and tcpdump attaching — Topic 205: persistent interface configuration, routing, VLANs/bridges awareness, troubleshooting with `ip`/`ss`/`tcpdump`, and wireless basics.

**Negative test:** Add the route before the interface has an address — "network unreachable"; ordering (link up, address, then route) is the operational sequence the exam tests.

**Cleanup:** Done in the walkthrough.

### Lab 5.7 — System maintenance (Topic 206)

**Objective:** Build from source and back up — the maintenance pair.

```bash
printf 'int main(){return 0;}' > tiny.c && gcc tiny.c -o tiny && ./tiny && echo "built+ran OK"
tar czf backup.tgz tiny.c tiny && tar tzf backup.tgz
rsync -a --dry-run ./ /tmp/labmirror/ | head -3
echo "notify: wall/shutdown messages; /etc/issue, motd"
```

**Expected result:** A program compiled from source (`make`-style flow: configure/make/install), a tar backup created and listed, and an rsync mirror previewed — Topic 206: building from source, backup strategies (tar, rsync, dd; full vs incremental), and notifying users of maintenance.

**Negative test:** Restore with `tar xzf` into the wrong directory — files land relative to CWD; tar's relative-path behavior is a classic restore surprise.

**Cleanup:** `rm tiny.c tiny backup.tgz`.

## Summary and Completion Checklist

- [ ] All seven 201-450 topics exercised.
- [ ] RAID + LVM built on loop devices; kernel module and sysctl work done.
- [ ] Boot-path, fstab, and backup/build maintenance drilled.
