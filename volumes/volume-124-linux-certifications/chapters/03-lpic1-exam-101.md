# Chapter 03: LPIC-1 — Exam 101 (101-500)

## Learning Objectives

- Cover exam 101-500's four topics with a walkthrough lab each.
- Drill system architecture, package management, GNU commands, and filesystems.
- Work from the published v5.0 objectives.

## The exam in brief

**Exam:** 101-500 (objectives v5.0), the first of LPIC-1's two exams; Pearson VUE delivery. Four topics: **101 System Architecture**, **102 Linux Installation and Package Management**, **103 GNU and Unix Commands**, **104 Devices, Linux Filesystems, Filesystem Hierarchy Standard**. Per-objective weights on lpi.org set question emphasis — Topic 103 carries the heaviest total weight, and this chapter's labs weight accordingly.

## Hands-On Lab

Any Linux VM (Debian/Ubuntu shown; RPM equivalents noted — the exam tests both families). **Cost:** none.

### Lab 3.1 — System architecture (Topic 101)

**Objective:** Read boot, hardware, and runlevel/target state.

```bash
systemctl get-default
lsblk
lsmod | head -5
dmesg 2>/dev/null | head -3 || journalctl -k | head -3
```

**Expected result:** The default target (`graphical.target`/`multi-user.target` — the systemd descendants of runlevels 5/3), block devices, loaded kernel modules, and kernel ring messages — Topic 101's surface: how the system boots (BIOS/UEFI → bootloader → kernel → init/systemd) and how hardware appears.

**Negative test:** `systemctl set-default rescue.target` on a lab VM and reboot — the system lands in rescue mode; restore with `set-default multi-user.target`. Targets are the boot destination, not decoration.

**Rollback:** Restore the default target.

### Lab 3.2 — Package management, both families (Topic 102)

**Objective:** Install, query, and remove with dpkg/apt — and know the rpm/dnf mirror image.

```bash
sudo apt-get update -qq && sudo apt-get install -y tree
dpkg -l tree | tail -1
dpkg -L tree | head -4
sudo apt-get remove -y tree
# RPM family equivalents: dnf install tree ; rpm -qi tree ; rpm -ql tree ; dnf remove tree
```

**Expected result:** `tree` installed, listed (`ii  tree …`), its files enumerated, then removed — the query verbs are the exam's favorites: which package owns a file, what files a package ships, what version is installed. The exam tests **both** dpkg/apt and rpm/dnf; drill the family you don't use daily. Topic 102 also covers boot managers (GRUB 2 install/config) and shared libraries (`ldd`, `ld.so.conf`).

**Negative test:** `dpkg -L` on an uninstalled package — the error distinguishes "not installed" from "no such package," a real exam nuance.

**Rollback:** Done in the walkthrough.

### Lab 3.3 — GNU and Unix commands (Topic 103, heaviest)

**Objective:** Drill the pipeline, redirection, and process toolkit that dominates the exam.

```bash
printf "beta\nalpha\nbeta\ngamma\n" > words.txt
sort words.txt | uniq -c | sort -rn | head -2
grep -n "a.pha" words.txt
sed 's/beta/BETA/' words.txt | tr 'a-z' 'A-Z' | tee out.txt | wc -l
cut -c1-3 words.txt | paste -sd, -
sleep 300 & jobs; kill %1
find . -name "*.txt" -newer words.txt -o -name "out*" | head -2
```

**Expected result:** Frequency-sorted words (`2 beta` first), a regex match with line number, a sed/tr/tee/wc pipeline printing `4`, `bet,alp,bet,gam`, a background job started and killed, and `find` locating files by test — Topic 103 in one sitting: text processing (`sort/uniq/grep/sed/tr/cut/paste/wc`), redirection and `tee`, job control, signals, and `find`. This is the heaviest-weighted topic; fluency here is most of exam 101.

**Negative test:** `sort words.txt | uniq -c` *without* the pre-sort (`uniq` on unsorted input) — `beta` counts twice separately; `uniq` only collapses adjacent lines, the classic trap.

**Rollback:** `rm words.txt out.txt`.

### Lab 3.4 — Devices, filesystems, FHS (Topic 104)

**Objective:** Make, mount, and check a filesystem; place it in the hierarchy.

```bash
dd if=/dev/zero of=disk.img bs=1M count=64 status=none
mkfs.ext4 -q disk.img
sudo mkdir -p /mnt/lab && sudo mount -o loop disk.img /mnt/lab
df -h /mnt/lab | tail -1
sudo umount /mnt/lab && fsck.ext4 -fn disk.img | tail -1
ls -d /etc /var /usr /home /tmp
```

**Expected result:** A 64 MB ext4 filesystem created on a loop device, mounted, reported by `df`, unmounted, and passing `fsck` clean — plus the FHS directories that Topic 104 expects you to place by purpose (`/etc` config, `/var` variable data, `/usr` system software, `/home` users, `/tmp` scratch). Permissions, links (`ln -s`), and quotas round out the topic.

**Negative test:** `fsck` a **mounted** filesystem — the tool warns hard; checking mounted filesystems corrupts, which is why the exam asks.

**Rollback:** `rm disk.img; sudo rmdir /mnt/lab`.

## Summary and Completion Checklist

- [ ] All four 101-500 topics exercised, weighted toward Topic 103.
- [ ] Both package families drilled.
- [ ] Filesystem lifecycle (mkfs/mount/df/umount/fsck) and FHS placement done.
