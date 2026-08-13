# Chapter 02: RHCSA — Users, Storage, and Boot (EX200)

## Learning Objectives

- Cover the RHCSA objective areas for local users/groups/permissions, storage, and boot/systemd.
- Drill the tasks the way the performance exam presents them.
- Build verification into every task.

## The exam in brief

**RHCSA (EX200)** is 100% performance-based, ~2.5–3 hours, RHEL 10, valid 3 years, prerequisite for RHCE. Its objective areas span tools, operating running systems, local storage, filesystems, deployment/maintenance, users/groups, and security (SELinux/firewalld). This chapter covers users/permissions, storage, and boot; [Chapter 03](03-rhcsa-services-networking-selinux-containers.md) covers services, networking, SELinux, and containers.

## Hands-On Lab

A RHEL-family VM (RHEL 10 / AlmaLinux 10 / Rocky 10) with a spare disk or loop device. **Cost:** none.

### Lab 2.1 — Users, groups, permissions

**Objective (task):** "Create a group and two users, one with a non-default shell and an expiry; set a shared directory the group can collaborate in."

```bash
sudo groupadd engineering
sudo useradd -G engineering alice
sudo useradd -G engineering -s /sbin/nologin -e 2027-12-31 svcacct
sudo mkdir -p /srv/eng && sudo chgrp engineering /srv/eng && sudo chmod 2770 /srv/eng
id alice; ls -ld /srv/eng; sudo chage -l svcacct | grep -i expire
```

**Expected result:** `alice` in `engineering`, `svcacct` non-login with a 2027 expiry, and `/srv/eng` mode `2770` (setgid so new files inherit the group) — users, group membership, account policies, and the **setgid collaborative directory** are RHCSA staples.

**Negative test:** Drop the setgid bit (`chmod 0770`) and create a file as alice — it lands in alice's primary group, breaking collaboration; the `2` in `2770` is why the exam asks for it.

**Rollback:** `sudo userdel -r alice; sudo userdel -r svcacct; sudo groupdel engineering; sudo rm -rf /srv/eng`.

### Lab 2.2 — LVM: create, extend, and mount persistently

**Objective (task):** "Create a volume group and a 512 MB logical volume with XFS, mount it at /data persistently, then grow it to 768 MB online."

```bash
LOOP=$(sudo losetup -f --show <(: ) 2>/dev/null) || { dd if=/dev/zero of=/root/pv.img bs=1M count=1024 status=none; LOOP=$(sudo losetup -f --show /root/pv.img); }
sudo pvcreate $LOOP && sudo vgcreate vgdata $LOOP
sudo lvcreate -L 512M -n lvdata vgdata && sudo mkfs.xfs -q /dev/vgdata/lvdata
sudo mkdir -p /data && echo "/dev/vgdata/lvdata /data xfs defaults 0 2" | sudo tee -a /etc/fstab
sudo mount -a && df -h /data | tail -1
sudo lvextend -L 768M /dev/vgdata/lvdata && sudo xfs_growfs /data
df -h /data | tail -1
```

**Expected result:** The LV mounted at `/data` at 512 MB, then grown to 768 MB with `df` reflecting the online resize — LVM create/extend, XFS, fstab persistence with **`mount -a` verification**, and the XFS-specific `xfs_growfs` (XFS grows only, never shrinks) are all exam-mandatory.

**Negative test:** `lvreduce` an XFS volume — XFS cannot shrink; attempting it (or forgetting `xfs_growfs` after `lvextend`) is the classic storage-task failure. Also: an fstab typo caught by `mount -a` now beats an unbootable system on the exam.

**Rollback:** Remove the fstab line, `sudo umount /data`, `sudo vgremove -f vgdata`, `sudo losetup -d $LOOP`, `rm -f /root/pv.img`.

### Lab 2.3 — Swap and Stratis/VDO awareness

**Objective (task):** "Add a swap volume and enable it persistently."

```bash
sudo lvcreate -L 128M -n lvswap vgdata 2>/dev/null && sudo mkswap /dev/vgdata/lvswap
echo "/dev/vgdata/lvswap none swap defaults 0 0" | sudo tee -a /etc/fstab
sudo swapon -a && swapon --show | grep lvswap
```

**Expected result:** The swap volume formatted, added to fstab, and active in `swapon --show` — swap management is a discrete RHCSA objective; the fstab `swap`/`none` fields differ from a filesystem mount, a detail the exam checks.

**Negative test:** `swapon` a volume you forgot to `mkswap` — "read swap header failed"; the format step is separate from enabling.

**Rollback:** `sudo swapoff /dev/vgdata/lvswap`, remove the fstab line, `sudo lvremove -f /dev/vgdata/lvswap`.

### Lab 2.4 — Boot targets and recovery

**Objective (task):** "Set the default boot target to multi-user and know how to reset a lost root password."

```bash
sudo systemctl set-default multi-user.target
systemctl get-default
# root password recovery (concept — done at the GRUB prompt on the exam):
cat <<'EOF'
1) interrupt GRUB, append: rd.break  to the kernel line
2) mount -o remount,rw /sysroot ; chroot /sysroot
3) passwd root ; touch /.autorelabel   (SELinux relabel!) ; exit; reboot
EOF
```

**Expected result:** The default target set to `multi-user.target` and the root-recovery sequence recited — including the **`touch /.autorelabel`** step that RHCSA candidates forget, leaving SELinux to lock the system on next boot. Boot targets, `rd.break` recovery, and GRUB are core objectives.

**Negative test:** Reset the root password via `rd.break` but skip `.autorelabel` — SELinux denies login on reboot; the relabel is what makes the recovery actually work.

**Rollback:** Leave the target at `multi-user` (exam default) or restore as your lab prefers.

### Lab 2.5 — Tuning and scheduled tasks

**Objective (task):** "Apply a tuning profile and schedule a recurring job."

```bash
sudo tuned-adm active 2>/dev/null || sudo dnf install -y tuned >/dev/null
sudo tuned-adm profile virtual-guest && sudo tuned-adm active
echo '0 2 * * * root /usr/bin/dnf -y upgrade --security' | sudo tee /etc/cron.d/sec-updates
sudo systemctl enable --now crond 2>/dev/null; ls -l /etc/cron.d/sec-updates
```

**Expected result:** A tuned profile applied and a cron.d job installed — `tuned-adm` profile management and cron/systemd-timer scheduling are RHCSA objectives; the `/etc/cron.d` format includes the **user field** (`root`), unlike a user crontab.

**Negative test:** Put a user-crontab line (no user field) into `/etc/cron.d` — cron rejects it; the two formats differ by exactly that field.

**Rollback:** `sudo rm /etc/cron.d/sec-updates`.

## Summary and Completion Checklist

- [ ] Users/groups/permissions with setgid collaboration drilled.
- [ ] LVM create/extend + XFS grow + swap, all fstab-persistent and `mount -a`-verified.
- [ ] Boot target set and root-recovery (with `.autorelabel`) understood.
- [ ] Tuning profiles and scheduled jobs applied.
