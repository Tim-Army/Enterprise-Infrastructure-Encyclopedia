# Chapter 03: Boot, systemd, Processes, Logging, and Scheduled Work

## Learning Objectives

- Trace the RHEL 10 boot sequence from firmware through GRUB2, the
  kernel, and initramfs to `systemd` as PID 1.
- Manage systemd units, targets, and dependencies, including custom
  service creation and resource control via cgroups.
- Inspect and control running processes using priority, signals, and
  systemd's cgroup-aware process accounting.
- Query and manage the systemd journal, including persistent storage
  and integration with `rsyslog` and log rotation.
- Schedule recurring and one-time work with `cron`, `at`, and systemd
  timer units, and choose correctly between them.
- Recover a system that fails to boot using rescue mode, emergency
  mode, and kernel command-line editing.

## Theory and Architecture

Every RHEL 10 system follows the same layered boot sequence regardless
of whether it runs on bare metal, a hypervisor, or a cloud instance:
firmware locates and hands off to a boot loader, the boot loader loads
a kernel and an initial RAM filesystem, and the kernel ultimately
executes `systemd` as process ID 1, which then brings the rest of
userspace online in dependency order. Understanding each stage — and
where to intervene when one fails — is a precondition for the
process, logging, and scheduling material later in this chapter,
because `systemd` is not just an init system; it is the same
dependency graph and control plane that owns services, sockets, mounts,
timers, and device units.

### Firmware, GRUB2, and the kernel

1. **Firmware (UEFI or legacy BIOS).** UEFI is the standard on RHEL 10
   deployments; it reads boot entries from the EFI System Partition
   (ESP, typically mounted at `/boot/efi`) rather than a Master Boot
   Record. Secure Boot, when enabled, validates the boot loader's
   signature before handing off control.
2. **GRUB2.** The GRand Unified Bootloader reads its configuration from
   `/boot/grub2/grub.cfg` (BIOS) or `/boot/efi/EFI/redhat/grub.cfg`
   (UEFI) — a generated file that administrators should not hand-edit.
   Instead, persistent changes go into `/etc/default/grub` and
   per-entry files under `/boot/loader/entries/` (Boot Loader
   Specification, or BLS, format used by RHEL 10), regenerated with
   `grub2-mkconfig` or managed live with `grubby`.
3. **Kernel and initramfs.** GRUB2 loads the selected kernel
   (`/boot/vmlinuz-<version>`) and its matching initial RAM filesystem
   (`/boot/initramfs-<version>.img`), built by `dracut`. The initramfs
   contains just enough of a root filesystem — kernel modules, LVM and
   multipath tooling, network drivers for network-rooted systems — to
   locate and mount the real root filesystem before control passes to
   it.
4. **systemd as PID 1.** Once the real root is mounted, the kernel
   executes `/usr/lib/systemd/systemd` as PID 1. From this point
   forward, every other process on the system is a descendant of
   `systemd`, and every service, mount, socket, device, and scheduled
   job is represented as a **unit** in its dependency graph.

### systemd targets replace runlevels

RHEL 10 has no SysV runlevels; **targets** are the systemd equivalent,
implemented as unit files that group other units together as
dependencies. The targets an administrator interacts with most are:

| Target | Approximate SysV equivalent | Purpose |
| --- | --- | --- |
| `poweroff.target` | Runlevel 0 | Shut the system down |
| `rescue.target` | Runlevel 1 | Single-user mode: root shell, minimal services, local filesystems mounted |
| `multi-user.target` | Runlevel 3 | Full multi-user, networked, non-graphical |
| `graphical.target` | Runlevel 5 | Multi-user plus a display manager |
| `reboot.target` | Runlevel 6 | Reboot the system |
| `emergency.target` | (none) | Minimal shell with almost nothing mounted or started; used for the most severe recovery cases |

A target is "reached" when every unit it pulls in as a dependency
(`Wants=`, `Requires=`) has started successfully; `systemctl
get-default` and `systemctl set-default` read and write the default
boot target, and `systemctl isolate <target>` switches the running
system to a different target immediately, stopping any unit not
required by the new target.

### Unit types and the unit file model

A systemd **unit** is any resource systemd supervises. The unit type is
determined by its file suffix:

| Unit type | Suffix | Manages |
| --- | --- | --- |
| Service | `.service` | A long-running or one-shot process |
| Socket | `.socket` | A network or IPC socket, optionally activating a service on first connection |
| Target | `.target` | A synchronization point / group of other units |
| Mount | `.mount` | A filesystem mount point |
| Timer | `.timer` | A scheduled trigger for another unit |
| Path | `.path` | A filesystem-change trigger (inotify-based) |
| Device | `.device` | A kernel-exposed device node |

Unit files live in three layers that systemd merges by precedence:
`/usr/lib/systemd/system/` (packaged, do not edit), `/etc/systemd/system/`
(administrator overrides and custom units, highest precedence), and
`/run/systemd/system/` (runtime-generated, transient). A `.service`
unit's structure is declarative:

```ini
[Unit]
Description=Human-readable description
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/my-daemon
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

`Type=` tells systemd how to determine the service has finished
starting: `simple` (default, the process itself is the service),
`forking` (the process forks and the parent exits), `oneshot` (runs to
completion, useful for setup tasks), and `notify` (the process signals
readiness via `sd_notify`). The `[Install]` section is only consulted
by `systemctl enable`/`disable`, which is why editing `ExecStart=` on
an already-enabled unit does not require re-enabling it, but adding a
`[Install]` section to a brand-new unit does.

### Process model and cgroups

Every process systemd starts is placed into its own control group
(cgroup), nested under the unit's slice (`system.slice`,
`user.slice`). This is what allows `systemctl status` to show the
exact process tree of a service, what allows `systemd-cgtop` to show
resource consumption per unit rather than per raw PID, and what allows
resource limits (`CPUQuota=`, `MemoryMax=`, `IOWeight=`) to be applied
to an entire service's process tree rather than a single PID — a
process spawned by a misbehaving service cannot silently escape its
resource controls by forking.

### The journal and structured logging

`systemd-journald` collects log data from the kernel, early boot,
standard output/error of every service, and `syslog()` calls, storing
it in a binary, indexed, structured format queried with `journalctl`.
Journal entries carry structured fields (`_SYSTEMD_UNIT`, `_PID`,
`_UID`, `PRIORITY`) that make filtering precise without regular
expressions. By default the journal may be volatile (`/run/log/journal`,
cleared at reboot) or persistent (`/var/log/journal`, survives reboot)
depending on `Storage=` in `/etc/systemd/journald.conf` and whether
that directory exists; RHEL 10's default install typically ships with
persistent logging enabled. `rsyslog` remains installed alongside
`journald` for environments needing traditional flat-file logs, remote
syslog forwarding, or a format other tooling expects — the two are
complementary, not competing, with `rsyslog` commonly configured to
read from the journal.

### Scheduling models: cron, at, and systemd timers

RHEL 10 supports three overlapping ways to run work on a schedule, and
choosing correctly matters operationally:

- **`cron`** (via `cronie`) runs recurring jobs from per-user crontabs
  (`crontab -e`) or system-wide files under `/etc/cron.d/` and the
  `/etc/cron.{hourly,daily,weekly,monthly}` directories (driven by
  `anacron`, which catches up missed runs on systems that are not
  always powered on).
- **`at`** runs a single, one-time job at a specified future time,
  queued and executed by `atd`.
- **systemd timer units** (`.timer`) trigger a matching `.service` unit
  on a calendar schedule (`OnCalendar=`) or relative to boot/activation
  (`OnBootSec=`, `OnUnitActiveSec=`). Timers integrate with the same
  dependency graph, logging, and resource controls as every other
  systemd unit, and are the Red Hat–recommended mechanism for new
  scheduled work on RHEL 10 — `cron` remains fully supported for
  compatibility and simple per-user schedules.

## Design Considerations

- **Target selection for headless servers.** Production servers should
  boot to `multi-user.target`, not `graphical.target`; a display
  manager and desktop stack on a server is unnecessary attack surface
  and unnecessary resource consumption. Reserve `graphical.target` for
  workstation-class or vendor-appliance builds that genuinely need a
  local console GUI.
- **Custom units vs. ad hoc cron/rc.local-style scripts.** A service
  that must survive a crash, respect dependency ordering (start only
  after a database is reachable), or be observable through the same
  tooling as every other daemon belongs in a proper systemd unit, not
  a background script launched from a login profile or a legacy
  `rc.local`.
- **Timers vs. cron for new automation.** Prefer systemd timers for new
  scheduled work: they get journal-integrated logging, `systemctl`
  status visibility, `OnFailure=` handling, and resource controls that
  plain cron jobs do not. Keep cron for environments standardizing on
  portable, per-user schedules across non-RHEL systems, or where staff
  are already deeply invested in cron tooling.
- **Persistent vs. volatile journal storage.** Persistent journal
  storage (`/var/log/journal`) is required for post-incident forensics
  across a reboot and for centralized log shipping continuity; size it
  deliberately with `SystemMaxUse=` in `journald.conf` rather than
  letting it consume unbounded disk.
- **Resource isolation by cgroup, not by convention.** On a
  multi-tenant or multi-service host, set `CPUQuota=` and
  `MemoryMax=` on services deliberately rather than relying on "this
  box has enough RAM" — cgroup limits turn a noisy-neighbor incident
  into a contained, observable failure of one unit instead of an
  OOM event affecting the whole host.
- **Boot-time recovery planning.** Document and rehearse the rescue
  and emergency mode recovery procedure before it is needed under
  incident pressure; an administrator who has never used `rd.break`
  outside of a drill will lose meaningful time re-deriving it during a
  real outage.

## Implementation and Automation

### 1. Inspecting the boot sequence

```bash
# Boot loader entries (BLS format)
ls /boot/loader/entries/
cat /boot/loader/entries/*.conf

# Kernel command line for the currently running kernel
cat /proc/cmdline

# List installed kernels and the default boot entry
grubby --info=ALL
grubby --default-kernel

# Regenerate GRUB2 configuration after editing /etc/default/grub
grub2-mkconfig -o /boot/grub2/grub.cfg          # BIOS
grub2-mkconfig -o /boot/efi/EFI/redhat/grub.cfg # UEFI

# Add a kernel argument persistently to every boot entry
grubby --update-kernel=ALL --args="net.ifnames=0"

# Analyze boot performance
systemd-analyze
systemd-analyze blame
systemd-analyze critical-chain
```

### 2. Managing targets

```bash
# Show the current and default target
systemctl get-default

# Set the default boot target to multi-user (headless server)
systemctl set-default multi-user.target

# Switch the running system to rescue mode immediately
systemctl isolate rescue.target

# List all currently active targets
systemctl list-units --type=target
```

### 3. Creating and managing a custom systemd service

```bash
cat > /etc/systemd/system/report-generator.service <<'EOF'
[Unit]
Description=Generate a nightly infrastructure report
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/generate-report.sh
User=report-svc
Group=report-svc

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd's unit cache after creating or editing a unit file
systemctl daemon-reload

# Enable and start it, verify status
systemctl enable --now report-generator.service
systemctl status report-generator.service

# Mask a unit to prevent it from starting even via a dependency
systemctl mask bluetooth.service
```

### 4. Process inspection and control

```bash
# Full process tree with systemd cgroup context
systemctl status
ps -ef --forest

# Live resource view, both classic and cgroup-aware
top
systemd-cgtop

# Show a unit's exact process tree (cgroup membership)
systemctl status httpd.service

# Adjust scheduling priority of a running process
renice -n 5 -p 4821

# Send a graceful termination, then a forced kill if needed
kill -TERM 4821
kill -KILL 4821
pkill -f generate-report.sh

# Apply a live resource limit to a running unit's cgroup
systemctl set-property httpd.service CPUQuota=50% MemoryMax=512M
```

### 5. Querying the journal

```bash
# Follow the live journal (like tail -f across all sources)
journalctl -f

# Logs for a specific unit
journalctl -u sshd.service

# Logs since the last boot, or a specific prior boot
journalctl -b
journalctl -b -1

# Logs in a time window, at warning severity or higher
journalctl --since "2026-07-18 08:00" --until "2026-07-18 09:00" -p warning

# Enable persistent journal storage explicitly
mkdir -p /var/log/journal
systemd-tmpfiles --create --prefix /var/log/journal
systemctl restart systemd-journald

# Cap journal disk usage
sed -i 's/^#SystemMaxUse=.*/SystemMaxUse=1G/' /etc/systemd/journald.conf
systemctl restart systemd-journald
```

### 6. Scheduling work: cron, at, and systemd timers

```bash
# Per-user crontab (interactive editor)
crontab -e
# Example line: run every day at 02:15
# 15 2 * * * /usr/local/bin/generate-report.sh

# System-wide cron drop-in
cat > /etc/cron.d/report-generator <<'EOF'
15 2 * * * report-svc /usr/local/bin/generate-report.sh
EOF

# One-time scheduled job
echo "/usr/local/bin/generate-report.sh" | at 23:30

# systemd timer: pairs with report-generator.service above
cat > /etc/systemd/system/report-generator.timer <<'EOF'
[Unit]
Description=Run report-generator.service nightly

[Timer]
OnCalendar=*-*-* 02:15:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable --now report-generator.timer
systemctl list-timers report-generator.timer
```

`Persistent=true` tells systemd to run the job immediately after boot
if the scheduled time was missed while the system was powered off —
the timer equivalent of `anacron`'s catch-up behavior for cron.

## Validation and Troubleshooting

- **Confirm a unit's actual state, not just whether it is running.**
  `systemctl status <unit>` shows active/inactive/failed state, the
  last several log lines, and the cgroup process tree in one view;
  `systemctl is-enabled <unit>` and `systemctl is-active <unit>`
  return script-friendly single-word output for automation checks.
- **Diagnose a service that fails immediately after starting.**
  `journalctl -u <unit> -b` shows exactly what the process printed
  before exiting; `systemctl status <unit>` shows the exit code and
  signal. A `Type=simple` service that exits immediately after
  `ExecStart` usually indicates the binary itself failed, not a
  systemd configuration problem — reproduce by running the
  `ExecStart=` command manually as the configured `User=`.
- **Diagnose slow boots.** `systemd-analyze blame` ranks units by
  time-to-start, and `systemd-analyze critical-chain` shows the
  dependency chain actually responsible for the total boot time —
  the two answer different questions and should be checked together.
- **Diagnose a system that will not boot.** Add `rd.break` (or
  `systemd.unit=rescue.target` / `systemd.unit=emergency.target` for
  a less severe interruption) to the kernel command line at the GRUB2
  menu (press `e` to edit the boot entry) to reach a shell before the
  real root is mounted read-write, useful for repairing an `/etc/fstab`
  error or a corrupted initramfs. Remount root read-write
  (`mount -o remount,rw /sysroot`) before making any change from this
  shell.
- **Diagnose a job that "never runs" under cron.** Confirm `crond` is
  active (`systemctl status crond`), check `/var/log/cron` or
  `journalctl -u crond`, and remember that cron jobs run with a
  minimal environment (`PATH`, `HOME` are not the interactive shell's)
  — scripts invoked by cron should use absolute paths and not assume
  interactive shell environment variables.
- **Diagnose a systemd timer that fired but did nothing.**
  `systemctl list-timers` shows next/last trigger times; if the timer
  fired but the paired service shows `inactive`/`failed`, check
  `journalctl -u <service-name>.service`, not the timer's own log
  output, since the timer unit only records the trigger event itself.
- **Common failure: forgetting `daemon-reload`.** Editing a unit file
  directly and running `systemctl restart` without first running
  `systemctl daemon-reload` restarts the service using the
  previously cached unit definition, silently ignoring the edit.

## Security and Best Practices

- Run custom services as a dedicated, unprivileged `User=`/`Group=`
  rather than root whenever the workload does not require root
  privileges; combine with `NoNewPrivileges=true`,
  `ProtectSystem=strict`, and `PrivateTmp=true` in the `[Service]`
  section for meaningful sandboxing with minimal effort.
- Set `Restart=on-failure` with a bounded `StartLimitIntervalSec=`/
  `StartLimitBurst=` on services that should self-heal, so a crash
  loop is capped rather than consuming resources indefinitely.
- Protect the GRUB2 boot menu with a password
  (`grub2-setpassword`) on systems where physical or console access is
  not fully trusted, since unrestricted kernel command-line editing is
  a direct path to a root shell via `rd.break`.
- Set conservative resource limits (`CPUQuota=`, `MemoryMax=`,
  `TasksMax=`) on any service that accepts external input or runs
  third-party code, to contain a runaway or compromised process.
- Ship persistent journal storage on any host that matters
  operationally or for compliance, and forward the journal or
  `rsyslog` output to a centralized log collector; a compromised host's
  local logs cannot be trusted after the fact.
- Avoid `/etc/rc.local` and ad hoc `@reboot` cron entries for anything
  that should be observable and restart-safe — a proper unit file with
  `[Install]` and dependency ordering is the supported, auditable
  mechanism.
- Review `systemctl list-unit-files --state=enabled` periodically on
  hardened builds to confirm no unexpected service was enabled by a
  package installation, and `mask` services that must never start
  rather than merely disabling them.

## References and Knowledge Checks

**References**

- [`bootup(7)`, `systemd.unit(5)`, `systemd.service(5)`,
  `systemd.timer(5)` man pages.](https://man7.org/linux/man-pages/man7/bootup.7.html)
- [`journalctl(1)`, `journald.conf(5)` man pages.](https://man7.org/linux/man-pages/man1/journalctl.1.html)
- [`crontab(5)`, `crontab(1)`, `at(1)` man pages.](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [Red Hat Enterprise Linux 10 System Administrator's Guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10) — Managing
  Systemd, Configuring Basic System Settings.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — RHEL 10
  baseline referenced throughout this chapter.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  RHCSA (EX200) blueprint mapping for this volume.

**Knowledge checks**

1. What distinguishes `Type=simple` from `Type=oneshot` in a systemd
   service unit, and when would `Type=forking` still be appropriate?
2. Why does editing an existing unit file require `systemctl
   daemon-reload` before the change takes effect?
3. When would a systemd timer be the better choice over a `cron`
   entry, and what does `Persistent=true` add to a timer that plain
   `cron` does not provide by default (without `anacron`)?
4. What kernel command-line parameter reaches an early shell before
   the real root filesystem is mounted, and why is it useful for
   fixing a bad `/etc/fstab` entry?

## Hands-On Lab

**Objective:** Build a custom systemd service and a companion timer,
observe them through the journal and process tools, and practice
recovering from a deliberately broken boot-time dependency.

**Prerequisites**

- A RHEL 10 host or VM with root or sudo access.
- Console access (not only SSH) for the boot-recovery portion of the
  lab, since a broken `fstab` can prevent SSH from coming up.

**Steps**

1. Create a small script and its target unit:

   ```bash
   sudo tee /usr/local/bin/heartbeat.sh <<'EOF'
   #!/usr/bin/env bash
   echo "heartbeat at $(date -Is)"
   EOF
   sudo chmod +x /usr/local/bin/heartbeat.sh

   sudo tee /etc/systemd/system/heartbeat.service <<'EOF'
   [Unit]
   Description=Heartbeat logger

   [Service]
   Type=oneshot
   ExecStart=/usr/local/bin/heartbeat.sh
   EOF

   sudo tee /etc/systemd/system/heartbeat.timer <<'EOF'
   [Unit]
   Description=Run heartbeat.service every minute

   [Timer]
   OnBootSec=1min
   OnUnitActiveSec=1min
   Persistent=true

   [Install]
   WantedBy=timers.target
   EOF
   ```

2. Load and enable the timer:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now heartbeat.timer
   systemctl list-timers heartbeat.timer
   ```

   **Expected result:** the timer appears in `list-timers` with a
   populated `NEXT` and `LEFT` column.

3. Wait at least one minute, then confirm the service ran and check
   its journal output:

   ```bash
   sleep 65
   systemctl status heartbeat.service
   journalctl -u heartbeat.service --since "5 minutes ago"
   ```

   **Expected result:** at least one `heartbeat at ...` line appears in
   the journal, and `systemctl status` shows the last run as
   `inactive (dead)` with exit code `0` (expected for a `oneshot`
   between runs).

4. Observe resource accounting for the unit while it is not running
   versus a long-lived process:

   ```bash
   systemd-cgtop -n 1
   ```

5. **Negative test:** intentionally reference a nonexistent script from
   a new unit and observe the failure signature:

   ```bash
   sudo tee /etc/systemd/system/broken-demo.service <<'EOF'
   [Unit]
   Description=Intentionally broken demo unit

   [Service]
   Type=simple
   ExecStart=/usr/local/bin/does-not-exist.sh
   EOF

   sudo systemctl daemon-reload
   sudo systemctl start broken-demo.service
   systemctl status broken-demo.service
   journalctl -u broken-demo.service -n 10
   ```

   **Expected result:** `systemctl status` reports `failed` with a
   status such as `203/EXEC`, and the journal shows systemd could not
   execute the configured `ExecStart=` path — demonstrating how a
   missing-binary failure is surfaced distinctly from an
   application-level crash.

6. Practice targeted log filtering by priority and time:

   ```bash
   journalctl -p err --since "10 minutes ago"
   ```

7. **Cleanup:**

   ```bash
   sudo systemctl disable --now heartbeat.timer
   sudo rm -f /etc/systemd/system/heartbeat.timer \
              /etc/systemd/system/heartbeat.service \
              /etc/systemd/system/broken-demo.service \
              /usr/local/bin/heartbeat.sh
   sudo systemctl daemon-reload
   sudo systemctl reset-failed
   ```

## Summary and Completion Checklist

RHEL 10 boots through a consistent firmware-to-GRUB2-to-kernel-to-
systemd sequence, and systemd's unit-and-target model governs every
service, mount, socket, and scheduled job as one dependency graph
rather than a collection of unrelated init scripts. Process control
inherits cgroup structure from that same model, giving per-service
resource accounting and limits. The journal centralizes structured
logging with precise filtering, and systemd timers extend the same
dependency and observability benefits to scheduled work, complementing
— not fully replacing — `cron` and `at`.

- [ ] Can trace the RHEL 10 boot sequence and explain each stage's
      role, from firmware through `systemd` as PID 1.
- [ ] Can create, enable, and troubleshoot a custom systemd service
      unit, including reading its journal output.
- [ ] Can inspect and control processes using cgroup-aware tools and
      apply live resource limits to a unit.
- [ ] Can query the journal by unit, time range, and priority, and
      configure persistent storage.
- [ ] Can create a systemd timer and explain when it is preferable to
      `cron`.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
