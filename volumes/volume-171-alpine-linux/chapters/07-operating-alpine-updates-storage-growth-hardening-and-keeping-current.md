# Chapter 07: Operating Alpine — Updates, Storage Growth, Hardening, and Keeping Current

## Learning Objectives

- Apply security updates within a release and upgrade to a new stable release.
- Grow a root filesystem after enlarging a virtual disk — including Alpine's
  whole-disk (no-partition) cloud-image layout.
- Harden a host with `doas`, minimal services, and restricted SSH.
- Schedule updates and track Alpine's security database to stay current.

## Theory and Architecture

Alpine's release model is a set of **stable branches** (`v3.24`, `v3.25`, …), each
supported for **two years**, plus the rolling **edge** development branch. Two kinds
of update follow from that:

- **Within a release** — routine security and bugfix updates. `apk update && apk
  upgrade` moves every world package to the newest version in the pinned branch.
- **Across releases** — moving from one stable branch to the next. You repoint
  `/etc/apk/repositories` at the new version and run `apk upgrade --available`
  (which reconciles packages across the branch switch), then reboot. Do this
  deliberately, one branch at a time, with a backup or snapshot first.

**Storage** is the other operational surprise. Cloud images ship a small root
filesystem, and Alpine does not auto-grow it. When you enlarge the virtual disk at
the hypervisor, you must extend the filesystem yourself. Alpine's generic cloud
image commonly formats the **whole disk** as ext4 with **no partition table**
(`/dev/sda` is the filesystem), so it grows with a single `resize2fs /dev/sda` — no
partition to extend first. A partitioned install instead needs `growpart /dev/sda 1`
before `resize2fs /dev/sda1`. Checking `lsblk` tells you which case you are in.

For **privilege escalation**, Alpine favors **`doas`** (OpenBSD's small `sudo`
alternative) over `sudo`. Its configuration is a few lines in `/etc/doas.conf`.

## Design Considerations

- **Patch on a cadence and automate it.** Alpine has no `unattended-upgrades`
  daemon; drive `apk upgrade` from cron (`/etc/periodic/*`) or a scheduler, and
  reboot when the kernel changes.
- **Upgrade releases before support ends.** The two-year window lapses quietly; plan
  the jump to the next branch rather than drifting off support.
- **Size disks with growth in mind, then grow the filesystem.** Enlarge the virtual
  disk at the hypervisor, then extend ext4 — the two steps are separate.
- **Prefer `doas` and least privilege.** A small `doas.conf` scoped to a `wheel`
  group is easier to reason about than a large `sudoers`.
- **Back up according to install mode.** `sys` installs rely on config backups and
  VM snapshots; diskless nodes persist with `lbu commit`.

## Implementation and Automation

Routine updates and a scheduled job:

```sh
apk update && apk upgrade
# schedule daily: drop a script into the busybox-cron periodic dir
cat > /etc/periodic/daily/apk-upgrade <<'EOF'
#!/bin/sh
apk update && apk upgrade
EOF
chmod +x /etc/periodic/daily/apk-upgrade
rc-update add crond && rc-service crond start
```

Upgrade to the next stable release (example `v3.24` → `v3.25`):

```sh
sed -i 's/v3\.24/v3.25/g' /etc/apk/repositories
apk update
apk upgrade --available
reboot
cat /etc/alpine-release            # after reboot: the new release
```

Grow the root filesystem after enlarging the disk (whole-disk ext4, the cloud case):

```sh
df -h /                            # before: small (e.g., 3.9G)
lsblk                              # sda is the filesystem, no partitions
resize2fs /dev/sda                 # grow ext4 to fill the disk
df -h /                            # after: the full disk (e.g., 98G)
```

If the install is partitioned instead:

```sh
apk add cloud-utils-growpart e2fsprogs-extra
growpart /dev/sda 1
resize2fs /dev/sda1
```

Set up `doas`:

```sh
apk add doas
echo 'permit persist :wheel' > /etc/doas.conf
adduser labadmin wheel             # add your admin user to wheel
doas -u root id                    # test escalation as labadmin
```

## Validation and Troubleshooting

```sh
cat /etc/alpine-release            # current release
apk version -l '<'                 # packages older than the repo (want none)
df -h /                            # filesystem uses the full disk
rc-update show                     # enabled services — keep it short
doas id                            # doas works for the wheel user
```

Common issues:

- **`resize2fs` says the filesystem is already the right size but `df` disagrees.**
  You resized the wrong device — on a whole-disk layout target `/dev/sda`, on a
  partitioned one grow the partition first, then `/dev/sda1`.
- **A release upgrade left packages behind.** Use `apk upgrade --available` (not a
  plain `apk upgrade`) after switching branches so `apk` reconciles version moves.
- **`doas: command not found` or "not permitted".** Install `doas`, write
  `/etc/doas.conf`, and ensure the user is in `wheel`.
- **Cron never runs the update.** `crond` is not enabled; `rc-update add crond &&
  rc-service crond start`, and make the periodic script executable.

## Security and Best Practices

- **Restrict SSH:** disable root login and password authentication in
  `/etc/ssh/sshd_config` (`PermitRootLogin no`, `PasswordAuthentication no`) and
  rely on keys plus a `doas`-enabled `wheel` user.
- **Keep the enabled-service list minimal** — `rc-update show` should be short; every
  daemon is attack surface.
- **Track Alpine's security database (`secdb`).** Run `apk version -l '<'` and watch
  advisories for the packages you ship or serve.
- **Verify integrity** with `apk audit` (detects modified packaged files) as a
  drift/tamper check.
- **Snapshot before release upgrades** so a failed branch move is a one-command
  rollback.

## References and Knowledge Checks

- Alpine wiki — [Upgrading Alpine](https://wiki.alpinelinux.org/wiki/Upgrading_Alpine)
  and [doas](https://wiki.alpinelinux.org/wiki/Doas).
- Alpine [releases and support dates](https://alpinelinux.org/releases/) and the
  [security database](https://secdb.alpinelinux.org/).

**Knowledge checks:**

1. What is the difference between an in-release update and a release upgrade, and
   which flag reconciles packages across a branch switch?
2. How do you know whether to run `resize2fs /dev/sda` or grow a partition first?
3. Why does Alpine favor `doas`, and what does `permit persist :wheel` mean?

## Hands-On Lab

**Objective:** Patch a host, grow its root filesystem, and harden it with `doas` and
scheduled updates.

**Shared prerequisites** — an Alpine VM you can enlarge at the hypervisor and reboot
(Chapter 02). **Cost:** none.

### Lab 7.1 — Patch and schedule updates

**Objective:** Bring the host current and automate it.

```sh
apk update && apk upgrade
apk version -l '<'                 # want no output (nothing behind)
cat > /etc/periodic/daily/apk-upgrade <<'EOF'
#!/bin/sh
apk update && apk upgrade
EOF
chmod +x /etc/periodic/daily/apk-upgrade
rc-update add crond && rc-service crond start
run-parts --test /etc/periodic/daily   # lists the job that will run
```

**Expected result:** an up-to-date package set and a daily upgrade job that `crond`
will run.

**Negative test:** leave `crond` disabled; the periodic script never runs and the
host silently ages — enable `crond`.

**Rollback:** keep the schedule, or remove the script and disable `crond`.

### Lab 7.2 — Grow the root filesystem

**Objective:** Extend ext4 to fill an enlarged disk.

1. On the hypervisor, enlarge the disk (Proxmox: `qm resize 140 scsi0 100G`).
2. On the guest:

```sh
df -h /                            # small before
lsblk                              # whole-disk sda (no partitions) on cloud images
resize2fs /dev/sda                 # or growpart + resize2fs /dev/sda1 if partitioned
df -h /                            # now the full disk
```

**Expected result:** `/` grows from the small shipped size to the full disk —
enough to hold the firmware images the Chapter 05 server serves.

**Negative test:** run `resize2fs /dev/sda1` on a whole-disk (no-partition) layout;
it errors because there is no such device — target `/dev/sda`.

**Rollback:** none (the larger filesystem is wanted).

### Lab 7.3 — Harden with `doas` and restricted SSH

**Objective:** Replace root SSH with a `wheel` user and `doas`.

```sh
apk add doas
echo 'permit persist :wheel' > /etc/doas.conf
adduser labadmin wheel
# in /etc/ssh/sshd_config: PermitRootLogin no ; PasswordAuthentication no
rc-service sshd restart
doas -u root id                    # as labadmin: escalation works
```

**Expected result:** `labadmin` escalates with `doas`, and root SSH/password login
is disabled — least-privilege administration.

**Negative test:** try to `doas` as a user not in `wheel`; it is denied — the policy
is scoped to the `wheel` group.

**Rollback:** keep the hardened configuration.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Operating Alpine is a small, explicit set of habits: `apk upgrade` on a cron cadence
within a release, a deliberate `apk upgrade --available` across releases before
support lapses, and `resize2fs` to grow a filesystem after enlarging a disk — on a
cloud image's whole-disk ext4 that is a single `resize2fs /dev/sda`. Harden with
`doas` scoped to `wheel`, restricted SSH, and a short enabled-service list, and track
Alpine's security database so the box stays current. That is the full lifecycle of
the appliance this volume built.

- [ ] Can patch within a release and upgrade to the next stable release.
- [ ] Can grow a whole-disk and a partitioned root filesystem.
- [ ] Can configure `doas` and restrict SSH.
- [ ] Can schedule updates and track Alpine security advisories.
- [ ] Completed Labs 7.1–7.3 including each negative test.
