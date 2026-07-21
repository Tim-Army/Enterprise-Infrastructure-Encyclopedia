# Chapter 02: Enterprise Linux Administration

![Lab flow for this chapter: a system account labsvc owns /var/lib/labsvc/data (mode 750) and runs labsvc-heartbeat.timer, which writes a timestamp every minute via a oneshot service; the volume group backing / is extended with an attached disk (pvcreate, vgextend, lvextend +2G, filesystem grow), increasing available space; a sudoers rule scopes the labops group to only restart or check the status of labsvc-heartbeat.timer. As a negative test, a user outside labops is refused when attempting to restart the timer via sudo; after being added to labops, the same command succeeds.](../../../diagrams/volume-04-enterprise-systems-administration/chapter-02-confined-service-account-flow.svg)

*Figure 2-1. Flow used throughout this chapter's Hands-On Lab: a confined service account, its systemd timer, an LVM storage extension, and a group-scoped sudo rule, all on a single lab VM.*

## Learning Objectives

- Describe the common architecture shared by enterprise Linux
  distributions: filesystem hierarchy, init system, package management,
  and privilege model.
- Administer users, groups, and file permissions, including access control
  lists (ACLs) and mandatory access control frameworks.
- Manage `systemd` units, targets, timers, and journal-based logging.
- Perform disk partitioning and Logical Volume Manager (LVM) operations.
- Apply kernel run-time tuning with `sysctl` and understand where those
  settings persist.
- Explain how this chapter's distribution-neutral coverage relates to the
  distribution-specific depth in [Volume XIV](../../volume-14-red-hat-enterprise-linux-10/README.md) (RHEL 10) and [Volume XXI](../../volume-21-ubuntu-server-cloud-26-04-lts/README.md)
  (Ubuntu Server 26.04 LTS).

## Theory and Architecture

Enterprise Linux administration rests on a small number of concepts that
are consistent across every major enterprise distribution — Red Hat
Enterprise Linux, its downstream/compatible rebuilds, SUSE Linux
Enterprise Server, and Debian-family distributions such as Ubuntu Server.
This chapter covers that shared foundation at a cross-platform,
distribution-neutral level. Package-manager syntax (`dnf` vs. `apt`),
default security modules (SELinux vs. AppArmor), and release-specific
tooling are noted where they diverge, but deep distribution-specific
administration — RHEL subscription management, `firewalld` policy
authoring, Ubuntu's Snap/Netplan stack — is covered in [Volume XIV](../../volume-14-red-hat-enterprise-linux-10/README.md) and
[Volume XXI](../../volume-21-ubuntu-server-cloud-26-04-lts/README.md).

### Filesystem Hierarchy Standard

Every enterprise Linux distribution implements the Filesystem Hierarchy
Standard (FHS), which defines the purpose of top-level directories:

| Path | Purpose |
| --- | --- |
| `/etc` | Host-specific configuration files |
| `/var` | Variable data: logs, spool, application state |
| `/usr` | Installed software and shared read-only data |
| `/opt` | Third-party/vendor-installed application packages |
| `/home` | User home directories |
| `/boot` | Kernel, initramfs, and bootloader configuration |
| `/proc`, `/sys` | Kernel-exposed virtual filesystems for process and device state |

Understanding the FHS matters operationally: `/var` growth (logs, package
caches) is the most common cause of enterprise Linux hosts running out of
disk space, which is why `/var` is frequently placed on its own logical
volume or partition ([Chapter 07](07-storage-filesystems-and-data-services.md)).

### The init system: systemd

Every enterprise Linux distribution in this encyclopedia's baseline
(RHEL 10, Ubuntu Server 26.04 LTS, SUSE Linux Enterprise Server) uses
`systemd` as PID 1. `systemd` organizes work into **units**:

- **Service units** (`.service`) — long-running or one-shot processes.
- **Target units** (`.target`) — grouping points analogous to legacy
  runlevels (`multi-user.target`, `graphical.target`).
- **Timer units** (`.timer`) — `systemd`'s native replacement for `cron`,
  covered later in this chapter and again in [Chapter 05](05-compute-process-and-service-management.md).
- **Mount and automount units** — filesystem mounts expressed as units so
  they participate in dependency ordering.
- **Socket units** — enable socket-activated service startup.

`systemd` also owns structured logging through `journald`, replacing (or
sitting alongside) traditional syslog.

### Privilege model: users, groups, and sudo

Linux enforces discretionary access control (DAC) through the classic
owner/group/other permission model, extended by POSIX ACLs for
finer-grained cases, and by mandatory access control (MAC) frameworks —
SELinux (RHEL family) or AppArmor (Debian/Ubuntu family, SUSE) — that
confine even a compromised root process to a policy-defined set of
allowed actions. Administrators should treat root privilege as something
granted per-command through `sudo`, logged and auditable, rather than as a
shared interactive login.

### Package management

Enterprise Linux systems draw software from signed repositories using one
of two package manager families:

| Family | Tool | Package format | Distributions |
| --- | --- | --- | --- |
| RPM | `dnf` (successor to `yum`) | `.rpm` | RHEL, SUSE (`zypper`) |
| Debian | `apt` | `.deb` | Ubuntu, Debian |

Both resolve dependencies, verify package signatures against imported GPG
keys, and support staged/offline repositories for air-gapped enterprise
environments. Patch and update strategy (WSUS-equivalent tooling,
maintenance windows, staged rollout) is covered in [Chapter 06](06-configuration-software-and-patch-management.md).

## Design Considerations

- **Distribution standardization.** Running multiple Linux distributions
  increases the automation and patching burden linearly with each added
  distribution family. Most enterprises standardize on one RPM-family and,
  at most, one Debian-family distribution, and justify any exception
  (a vendor appliance that only ships as a Debian image, for example).
- **SELinux/AppArmor enforcing vs. permissive.** Disabling MAC frameworks
  is a common but risky shortcut. Design for `enforcing`/`enforce` mode
  from initial build; retrofitting policy onto a fleet that has run
  permissive for years is far more expensive than starting correctly.
- **Partitioning strategy.** Decide up front which paths get dedicated
  logical volumes (`/var`, `/var/log`, `/home`, `/tmp`) so that log growth
  or a runaway user process cannot fill the root filesystem and crash the
  host. [Chapter 07](07-storage-filesystems-and-data-services.md) covers LVM and filesystem design in depth.
- **sudo policy granularity.** A single `%wheel ALL=(ALL) ALL` entry is
  simple but grants blanket root. Enterprise environments should scope
  `sudo` rules to the specific commands a role needs, and log every
  invocation centrally.
- **Kernel tuning scope.** `sysctl` changes should be justified,
  documented, and applied through configuration management
  (`/etc/sysctl.d/*.conf`), never as ad hoc `sysctl -w` commands that
  disappear on reboot and leave no audit trail.

## Implementation and Automation

### User and group management

```bash
# Create a service group and a system account with no interactive login,
# consistent with least-privilege service-account design.
sudo groupadd --system svc-appmon
sudo useradd --system --gid svc-appmon --shell /usr/sbin/nologin \
  --home-dir /var/lib/appmon --create-home svc-appmon

# Grant a human administrator scoped sudo rights via a drop-in file
# rather than editing /etc/sudoers directly.
sudo tee /etc/sudoers.d/10-appteam-restart <<'EOF'
%appteam ALL=(root) NOPASSWD: /usr/bin/systemctl restart appmon.service, \
                               /usr/bin/systemctl status appmon.service
EOF
sudo visudo -c
```

### File permissions and ACLs

```bash
# Standard owner/group/other permissions.
sudo chown svc-appmon:svc-appmon /var/lib/appmon
sudo chmod 750 /var/lib/appmon

# POSIX ACL: grant a second group read access without changing the
# primary owner/group, useful when two teams share a data directory.
sudo setfacl -m g:appteam:rx /var/lib/appmon
getfacl /var/lib/appmon
```

### systemd unit and timer management

```ini
# /etc/systemd/system/appmon-cleanup.service
[Unit]
Description=Purge appmon temp files older than 7 days

[Service]
Type=oneshot
ExecStart=/usr/bin/find /var/lib/appmon/tmp -mtime +7 -type f -delete
```

```ini
# /etc/systemd/system/appmon-cleanup.timer
[Unit]
Description=Daily appmon temp cleanup

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now appmon-cleanup.timer
systemctl list-timers appmon-cleanup.timer
```

### LVM operations

```bash
# Extend a logical volume backing /var/log after adding a new disk.
sudo pvcreate /dev/sdb
sudo vgextend vg_system /dev/sdb
sudo lvextend -L +10G /dev/vg_system/lv_varlog
sudo xfs_growfs /var/log      # XFS: online grow
# For ext4 instead: sudo resize2fs /dev/vg_system/lv_varlog
```

### Kernel run-time tuning

```bash
# Persisted sysctl change, applied through a drop-in file so it survives
# reboots and is visible to configuration-management diffing.
sudo tee /etc/sysctl.d/60-appmon-network.conf <<'EOF'
net.core.somaxconn = 4096
net.ipv4.tcp_fin_timeout = 15
EOF
sudo sysctl --system
```

### Centralized log inspection with journald

```bash
# Review the last boot's failures for a specific unit.
journalctl -u appmon.service -b -p err

# Forward journald to a remote syslog collector (deep dive: Chapter 09
# and Volume XI).
sudo tee -a /etc/systemd/journald.conf <<'EOF'
[Journal]
ForwardToSyslog=yes
EOF
sudo systemctl restart systemd-journald
```

## Validation and Troubleshooting

- Confirm a unit's actual runtime state, not just whether it is enabled:
  `systemctl status appmon.service` shows `active (running)` versus
  `enabled` (which only means it starts at boot).
- Confirm SELinux/AppArmor is enforcing: `getenforce` (SELinux) should
  return `Enforcing`; `aa-status` (AppArmor) should show profiles in
  `enforce` mode, not `complain`.
- Confirm disk pressure before it becomes an outage:
  `df -hT` for filesystem usage, `lvs` and `vgs` for volume group free
  space, and set monitoring thresholds ([Chapter 09](09-monitoring-troubleshooting-and-lifecycle-operations.md)) well before 100%.
- Confirm a `sysctl` change actually took effect and persisted:
  `sysctl net.core.somaxconn` should match the drop-in file, and the
  setting should survive a reboot.

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| Service fails to start after boot but starts manually | Unit ordering/dependency missing (`After=`, `Requires=`) | `systemctl list-dependencies appmon.service` |
| `Permission denied` despite correct owner/group | SELinux/AppArmor denial, not a DAC issue | `sudo ausearch -m avc -ts recent` (SELinux) or `journalctl -k \| grep -i apparmor` |
| `/var` fills unexpectedly | Runaway log or unrotated journal | `journalctl --disk-usage`; check `logrotate` configuration |
| `lvextend` succeeds but filesystem size unchanged | Filesystem not grown after the logical volume | Run `xfs_growfs` (XFS) or `resize2fs` (ext4) after `lvextend` |
| `sysctl -w` change disappears after reboot | Change was not persisted to `/etc/sysctl.d/` | Move the setting into a drop-in file and re-apply with `sysctl --system` |

## Security and Best Practices

- Run SELinux or AppArmor in enforcing mode in production; treat
  `permissive`/`complain` as a temporary diagnostic state, not a steady
  state.
- Disable direct root SSH login (`PermitRootLogin no` in `sshd_config`)
  and require named-user `sudo` for privileged actions, so every
  privileged action is attributable.
- Scope `sudo` rules to specific commands per role rather than granting
  blanket root, and log `sudo` invocations to a centralized collector.
- Use system accounts (`useradd --system`, `nologin` shell) for services;
  never run application daemons as an interactive human account or as
  root unless the daemon explicitly requires it and drops privilege after
  binding.
- Keep `/tmp`, `/var/tmp`, and any world-writable directory mounted with
  `nosuid,nodev` (and `noexec` where the application allows it).
- Apply CIS Benchmark or DISA STIG hardening baselines consistently
  through configuration management, not manual one-off hardening
  ([Chapter 08](08-systems-security-automation-and-compliance.md)).

## References and Knowledge Checks

**References**

- [`systemd.unit(5)`, `systemd.timer(5)`, and `journalctl(1)` man pages.](https://man7.org/linux/man-pages/man5/systemd.unit.5.html)
- Red Hat Enterprise Linux 10 documentation — System Administrator's Guide
  (see [Volume XIV](../../volume-14-red-hat-enterprise-linux-10/README.md) for the distribution-specific deep dive).
- Ubuntu Server 26.04 LTS documentation (see [Volume XXI](../../volume-21-ubuntu-server-cloud-26-04-lts/README.md) for the
  distribution-specific deep dive).
- [SELinux User's and Administrator's Guide (Red Hat); AppArmor
  documentation (Canonical/SUSE).](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/using_selinux/index)
- [Filesystem Hierarchy Standard (FHS) 3.0, Linux Foundation.](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)

**Knowledge Checks**

1. What is the difference between a unit being `enabled` and a unit being
   `active`?
2. Why should `sysctl` changes be applied through `/etc/sysctl.d/` rather
   than `sysctl -w` at the command line?
3. Describe a scenario where a DAC permission check passes but access is
   still denied. What subsystem is responsible?
4. Why is it common practice to place `/var/log` on its own logical
   volume?
5. What is the security benefit of a `nologin` shell on a service
   account?

## Hands-On Lab

**Objective:** Provision a service account, confine it with a scoped
`systemd` unit and `sudo` rule, extend its storage with LVM, and validate
enforcement — all on a single lab VM.

### Prerequisites

- One enterprise Linux VM (RHEL-family or Debian-family, 2 vCPU / 2 GB RAM)
  with an additional unpartitioned virtual disk attached as `/dev/sdb`
  (8 GB or larger) and LVM already in use for the root volume group
  (default in most distribution installers).
- `sudo` access.

### Procedure

1. Create the service account and group:

   ```bash
   sudo groupadd --system labsvc
   sudo useradd --system --gid labsvc --shell /usr/sbin/nologin \
     --home-dir /var/lib/labsvc --create-home labsvc
   ```

2. Create a data directory and set ownership:

   ```bash
   sudo mkdir -p /var/lib/labsvc/data
   sudo chown -R labsvc:labsvc /var/lib/labsvc
   sudo chmod 750 /var/lib/labsvc
   ```

3. Create a `systemd` service and timer that write a timestamp file every
   minute:

   ```bash
   sudo tee /etc/systemd/system/labsvc-heartbeat.service <<'EOF'
   [Unit]
   Description=Lab heartbeat writer

   [Service]
   Type=oneshot
   User=labsvc
   Group=labsvc
   ExecStart=/bin/sh -c 'date > /var/lib/labsvc/data/heartbeat.txt'
   EOF

   sudo tee /etc/systemd/system/labsvc-heartbeat.timer <<'EOF'
   [Unit]
   Description=Run labsvc heartbeat every minute

   [Timer]
   OnCalendar=*-*-* *:*:00
   Persistent=true

   [Install]
   WantedBy=timers.target
   EOF

   sudo systemctl daemon-reload
   sudo systemctl enable --now labsvc-heartbeat.timer
   ```

4. Wait at least 60 seconds, then confirm the timer fired:

   ```bash
   systemctl list-timers labsvc-heartbeat.timer
   cat /var/lib/labsvc/data/heartbeat.txt
   ```

   **Expected result:** `list-timers` shows a recent `LAST` run, and
   `heartbeat.txt` contains a current timestamp.

5. Extend storage for the growing data directory using the attached disk:

   ```bash
   sudo pvcreate /dev/sdb
   sudo vgextend "$(sudo vgs --noheadings -o vg_name | tr -d ' ' | head -1)" /dev/sdb
   sudo lvextend -L +2G "/dev/$(sudo lvs --noheadings -o vg_name,lv_name | awk '{print $1"/"$2}' | grep -i root)"
   sudo xfs_growfs / 2>/dev/null || sudo resize2fs "$(findmnt -n -o SOURCE /)"
   ```

   **Expected result:** `df -hT /` shows increased available space
   compared to before this step.

6. Grant a non-root administrative group scoped rights to manage only this
   timer:

   ```bash
   sudo groupadd labops || true
   sudo tee /etc/sudoers.d/20-labops-heartbeat <<'EOF'
   %labops ALL=(root) NOPASSWD: /usr/bin/systemctl restart labsvc-heartbeat.timer, \
                                 /usr/bin/systemctl status labsvc-heartbeat.timer
   EOF
   sudo visudo -c
   ```

   **Expected result:** `visudo -c` reports the file as syntactically
   valid.

### Negative Test

As a non-root, non-`labops` user (or by running `sudo -l` after removing
your own account from `labops`), attempt to restart the timer:
`sudo systemctl restart labsvc-heartbeat.timer`. The command should be
refused with a "not allowed" message, proving the `sudo` rule is scoped
to the `labops` group rather than globally permitted. Then add your test
user to `labops` (`sudo usermod -aG labops <user>`, then re-login) and
confirm the same command now succeeds.

### Cleanup

```bash
sudo systemctl disable --now labsvc-heartbeat.timer
sudo rm -f /etc/systemd/system/labsvc-heartbeat.service \
           /etc/systemd/system/labsvc-heartbeat.timer
sudo systemctl daemon-reload
sudo rm -f /etc/sudoers.d/20-labops-heartbeat
sudo userdel -r labsvc
sudo groupdel labops 2>/dev/null || true
```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Enterprise Linux administration is built on a small, consistent core
across every major distribution: the FHS, `systemd` as PID 1 with its
service/target/timer/journal model, a DAC-plus-MAC privilege model, LVM
for flexible storage growth, and package management through signed
repositories. This chapter's distribution-neutral treatment is the
foundation for the RHEL 10 and Ubuntu Server 26.04 LTS deep dives later in
this encyclopedia.

- [ ] Can create a scoped service account and confine it with `systemd`
      and `sudo`, rather than granting blanket root.
- [ ] Can extend a logical volume and grow its filesystem online.
- [ ] Can persist and validate a `sysctl` kernel tuning change.
- [ ] Can distinguish a DAC permission denial from a MAC (SELinux/
      AppArmor) denial and knows the diagnostic command for each.
- [ ] Completed the hands-on lab, including the negative `sudo` scope
      test.
