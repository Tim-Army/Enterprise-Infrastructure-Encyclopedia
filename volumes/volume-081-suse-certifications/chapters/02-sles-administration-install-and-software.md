# Chapter 02: SLES Administration — Install and Software

## Learning Objectives

- Navigate SLES and the command line.
- Manage software with zypper and repositories.
- Configure the system with YaST.
- Manage services with systemd.
- Complete a walkthrough for each SLES foundation topic.

## Theory and Architecture

The **SCA in SUSE Linux Enterprise** starts with core administration. **SLES** is a systemd-based
enterprise Linux managed through the **command line**, the **YaST** configuration tool (SUSE's
signature admin UI/CLI, `yast2`), and standard Linux utilities. Software is managed with **zypper**,
SUSE's package manager: it installs and removes packages, applies **patches** (security/recommended
updates grouped as patches), manages **repositories** (`zypper lr`, `zypper ar`), and resolves
dependencies. Services and boot are handled by **systemd** — units, targets, `systemctl` (start/
enable/status), and `journalctl` for logs. Understanding **zypper software/patch management**, **YaST
configuration**, and **systemd service management** is the foundation of SLES administration and the
bulk of the SCA exam's Software Management and System Initialization domains. This chapter teaches each
with a hands-on walkthrough (real commands; run on SLES/openSUSE, or read the SUSE-specific commands on
another Linux).

## Design Considerations

Manage software with **zypper** and keep **repositories** and **patches** current. Use **YaST** for
guided configuration and **systemd** (`systemctl`/`journalctl`) for services and logs. Register systems
for updates (SCC/RMT). Prefer **patches** for security currency. Automate with scripts or SUSE Manager
at scale.

## Implementation and Automation

The labs manage software with zypper, patch, inspect repos, and manage a service.

## Validation and Troubleshooting

Confirm the SLES foundation:

```text
SLES = systemd enterprise Linux. Admin: CLI + YaST (yast2). Software: zypper (install/remove, patch, repos: zypper lr/ar/in/up/patch). Services/boot: systemd (systemctl, journalctl).
SCA domains here: Overview, Command Line, System Initialization, Software Management.
```

Common pitfalls: installing software by downloading RPMs manually (bypasses dependency/patch
management); and unregistered systems that can't get **patches**.

## Security and Best Practices

Use **zypper** for software and **patches**, keep **repositories** registered and current, configure
with **YaST**, and manage services/logs with **systemd**. Apply security patches promptly. All work is
authorized administration.

## Hands-On Lab

SLES foundation walkthroughs. **Shared prerequisites** — a SLES/openSUSE VM (or read the commands),
`python3`. **Cost:** none (openSUSE Leap is free).

### Lab 2.1 — Manage software with zypper

**Objective:** Install and query packages.

```bash
zypper lr                      # list repositories
zypper search --installed-only nginx 2>/dev/null || echo "zypper se: search packages"
zypper --non-interactive install tree 2>/dev/null || echo "zypper in <pkg>: install with dependency resolution"
zypper info tree 2>/dev/null | head || echo "zypper info: package details"
```

**Expected result:** repositories listed and a package installed via **zypper** with dependency
resolution — SLES software management.

**Negative test:** `rpm -i` a downloaded package ignoring dependencies; it may fail or break — use
**zypper** for resolution.

**Rollback:** `zypper --non-interactive remove tree` (in a lab).

### Lab 2.2 — Apply patches

**Objective:** Keep the system current.

```bash
zypper lp 2>/dev/null | head || echo "zypper lp: list available patches (security/recommended)"
# Apply patches (lab):
zypper --non-interactive patch 2>/dev/null || echo "zypper patch: applies grouped security/recommended updates"
```

**Expected result:** available **patches** listed/applied — SLES patch management (security currency).

**Negative test:** run `zypper update` and assume you're patched; **`zypper patch`** applies the
grouped security patches — use it for compliance.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — Configure with YaST

**Objective:** Use the SUSE admin tool.

```bash
# YaST is SUSE's guided config tool (ncurses or GUI):
yast2 --list 2>/dev/null | head || echo "yast2 modules: users, network, software, services, storage, firewall, ..."
echo "SLES: YaST (yast2) provides guided modules for most administration tasks"
```

**Expected result:** the **YaST** modules for guided configuration — SUSE's signature admin tool.

**Negative test:** hand-edit every config file without knowing the format; **YaST** validates and
guides — use it where appropriate.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Manage a service with systemd

**Objective:** Control services and read logs.

```bash
systemctl status sshd 2>/dev/null | head -5 || echo "systemctl status <unit>: service state"
systemctl is-enabled sshd 2>/dev/null || echo "systemctl enable/disable: boot behavior"
journalctl -u sshd -n 5 --no-pager 2>/dev/null || echo "journalctl -u <unit>: service logs"
```

**Expected result:** service **status**, boot behavior, and **logs** via systemd — SLES service
management.

**Negative test:** look for services in `/etc/init.d` (SysV); SLES uses **systemd** — use
`systemctl`/`journalctl`.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SLES administration foundations cover the command line, zypper software and patch management, YaST
configuration, and systemd service management — the core of the SCA in SUSE Linux Enterprise.

- [ ] I can manage software with zypper.
- [ ] I can apply patches.
- [ ] I can configure with YaST.
- [ ] I can manage a service with systemd.
- [ ] I completed Labs 2.1–2.4 including each negative test.
