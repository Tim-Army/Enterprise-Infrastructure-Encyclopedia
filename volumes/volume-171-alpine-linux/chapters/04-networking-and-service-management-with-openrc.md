# Chapter 04: Networking and Service Management with OpenRC

## Learning Objectives

- Configure a static address and a persistent DNS resolver on Alpine.
- Explain OpenRC's run levels and manage services with `rc-service` and
  `rc-update`.
- Distinguish a service's init script (`/etc/init.d`) from its configuration
  (`/etc/conf.d`).
- Run a command at every boot with the `local.d` mechanism.
- Make network and boot-time changes survive a reboot.

## Theory and Architecture

### Networking

Alpine configures interfaces through the classic **`/etc/network/interfaces`** file,
driven by `ifupdown-ng` (the modern replacement for `ifupdown`). A static
management interface looks like:

```text
auto eth0
iface eth0 inet static
    address 10.30.99.50/24
    gateway 10.30.99.1
```

DNS is separate: the resolver lives in **`/etc/resolv.conf`**. On a static
interface you can have `ifupdown-ng` write it for you by adding
`dns-nameservers`/`dns-search` lines to the interface stanza; on a DHCP interface
the lease supplies it. The cloud-image case from Chapter 02 — an address but no
resolver — happens when neither path runs, and the durable fix is to put the
resolver where it will persist rather than editing the live file each boot.

`ip` (from BusyBox or the full `iproute2` package) shows and changes runtime state;
`rc-service networking restart` reapplies the file.

### OpenRC

OpenRC is Alpine's service manager. It runs **init scripts** from `/etc/init.d`,
organized into **run levels**:

| Run level | Purpose |
| --- | --- |
| **sysinit** | Earliest bring-up (devfs, mdev) |
| **boot** | One-time boot tasks (hostname, filesystems, networking) |
| **default** | Normal multi-user services (sshd, your daemons) |
| **shutdown** | Teardown on halt/reboot |

Two commands cover day-to-day work:

- **`rc-service <name> <action>`** — act on a service *now* (`start`, `stop`,
  `restart`, `status`).
- **`rc-update add|del <name> [runlevel]`** — enable or disable a service *at boot*
  by adding it to (or removing it from) a run level (default is `default`).

A service's **behavior** is its init script in `/etc/init.d/<name>`; its
**configuration** is a separate file in `/etc/conf.d/<name>` (environment-style
variables the init script sources). Editing the wrong one is a common mistake:
tuning a daemon means editing `/etc/conf.d/<name>`, not the init script.

### The `local.d` boot hook

Not everything is a packaged service. OpenRC ships a **`local`** service that runs
every executable `*.start` script in **`/etc/local.d/`** at boot (and `*.stop`
scripts at shutdown). It is the simplest durable "run this at boot" mechanism — no
init script to write — and this volume uses it twice: to make a resolver persistent
and (Chapter 05) to launch the TFTP daemon when a packaged service is
inconvenient. `local` must itself be enabled once: `rc-update add local`.

## Design Considerations

- **Static addressing for anything that serves.** Give servers and appliances a
  static address in `/etc/network/interfaces`; convert lab DHCP nodes to static
  before they carry a service so the address cannot move.
- **Persist the resolver, do not re-edit it.** Put DNS where it survives — a
  `dns-nameservers` line on the interface, or a `local.d` script — rather than
  editing `/etc/resolv.conf` after every boot.
- **Enable services at the right run level.** Almost all daemons belong in
  `default`; reserve `boot` for one-time setup.
- **Prefer a packaged service; fall back to `local.d`.** When a package ships a
  clean init script, use it. When the packaged service's configuration is awkward
  or missing, `local.d` is the pragmatic, durable alternative.

## Implementation and Automation

Configure a static interface and apply it:

```sh
cat > /etc/network/interfaces <<'EOF'
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
    address 10.30.99.50/24
    gateway 10.30.99.1
EOF
rc-service networking restart
ip -brief address show eth0
```

Make DNS persistent with a `local.d` script (works regardless of interface driver):

```sh
cat > /etc/local.d/resolv.start <<'EOF'
#!/bin/sh
printf 'nameserver 96.45.45.45\nnameserver 96.45.46.46\n' > /etc/resolv.conf
EOF
chmod +x /etc/local.d/resolv.start
rc-update add local            # enable the local.d hook at boot
rc-service local start         # run it now
cat /etc/resolv.conf
```

Manage a service and enable it at boot:

```sh
apk add openssh
rc-service sshd start
rc-update add sshd default     # start at boot in the default run level
rc-status default              # confirm it is listed
```

## Validation and Troubleshooting

```sh
ip -brief address; ip route            # runtime addressing and default route
cat /etc/resolv.conf                   # resolver present
rc-status -a                           # services by run level
rc-update show                         # what is enabled at each run level
rc-service <name> status               # one service's state
```

Common issues:

- **The IP is right but name resolution fails.** Empty/wrong `/etc/resolv.conf`;
  persist a resolver (above). This is the recurring Alpine cloud gotcha.
- **A service runs now but not after reboot.** You started it with `rc-service`
  but never `rc-update add`ed it; enable it at boot.
- **A `local.d` script does nothing at boot.** Either it is not executable, or the
  `local` service was never enabled — `chmod +x` it and `rc-update add local`.
- **Editing `/etc/init.d/<name>` had no effect on the daemon's settings.** Daemon
  settings live in `/etc/conf.d/<name>`; edit that instead.

## Security and Best Practices

- Give management interfaces a **static** address so access does not depend on a
  DHCP lease.
- For `sshd`, install a key and disable password authentication; keep the service
  in `default` and nothing extra enabled.
- Keep the enabled-service list minimal — `rc-update show` should be short on an
  appliance; every enabled daemon is attack surface.
- Make `local.d` scripts idempotent (safe to run twice) since they run on every
  boot.

## References and Knowledge Checks

- Alpine wiki — [Configure Networking](https://wiki.alpinelinux.org/wiki/Configure_Networking)
  and [OpenRC](https://wiki.alpinelinux.org/wiki/OpenRC).
- Alpine wiki — [Local startup scripts (local.d)](https://wiki.alpinelinux.org/wiki/Local_Backup)
  and the `local` service.

**Knowledge checks:**

1. Which file configures interfaces, and which file holds the resolver?
2. What is the difference between `rc-service` and `rc-update add`?
3. How do you run an arbitrary command at every boot without writing an init
   script?

## Hands-On Lab

**Objective:** Configure persistent static networking and DNS, manage a service
with OpenRC, and add a boot-time `local.d` hook.

**Shared prerequisites** — an Alpine host (Chapter 02) you can reboot. **Cost:**
none.

### Lab 4.1 — Static addressing and persistent DNS

**Objective:** Convert the host to a static address with a resolver that survives
reboot.

1. Write `/etc/network/interfaces` and restart networking (Implementation above).
2. Add the `resolv.start` `local.d` script and enable `local`.
3. Reboot and verify persistence:

```sh
reboot
# after reboot:
ip -brief address show eth0            # 10.30.99.50/24
cat /etc/resolv.conf                   # nameservers present
ping -c1 dl-cdn.alpinelinux.org
```

**Expected result:** the static address and the resolver are both present after a
reboot — no manual fix-up needed.

**Negative test:** set the resolver by editing `/etc/resolv.conf` directly (no
`local.d`) and reboot a cloud image; it is empty again — a live-file edit does not
persist.

**Rollback:** keep the configuration (later chapters rely on it).

### Lab 4.2 — Manage a service with OpenRC

**Objective:** Start a service now and enable it at boot.

```sh
apk add openssh
rc-service sshd start
rc-service sshd status
rc-update add sshd default
rc-update show | grep sshd
```

**Expected result:** `sshd` running now and listed in the `default` run level, so
it starts on every boot.

**Negative test:** `rc-service sshd start` but skip `rc-update add`, then reboot;
`sshd` is not running — starting is not enabling.

**Rollback:** leave `sshd` enabled, or `rc-update del sshd && rc-service sshd stop`.

### Lab 4.3 — A boot-time `local.d` hook

**Objective:** Run a command at every boot and prove it fired.

```sh
cat > /etc/local.d/hello.start <<'EOF'
#!/bin/sh
echo "local.d ran at $(date -u)" >> /var/log/local-hook.log
EOF
chmod +x /etc/local.d/hello.start
rc-update add local
rc-service local start
cat /var/log/local-hook.log
reboot
# after reboot:
cat /var/log/local-hook.log            # a second, later timestamp
```

**Expected result:** the log gains a new timestamped line at each boot — the
`local.d` mechanism runs reliably, which is the foundation for Chapter 05's TFTP
launch.

**Negative test:** forget `chmod +x`; the script is ignored at boot — `local.d`
runs only executable `*.start` files.

**Rollback:** `rm /etc/local.d/hello.start /var/log/local-hook.log`.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Alpine configures interfaces in `/etc/network/interfaces` and the resolver in
`/etc/resolv.conf`; the durable fix for the cloud-image "address but no DNS" case is
to persist the resolver (an interface `dns-nameservers` line or a `local.d` script),
not to re-edit the live file. OpenRC runs services from `/etc/init.d` across run
levels — `rc-service` acts now, `rc-update add` enables at boot, and daemon settings
live in `/etc/conf.d`. The `local` service runs executable `local.d/*.start` scripts
at every boot, the simplest durable boot hook and the mechanism Chapter 05 uses.

- [ ] Can configure a persistent static address and resolver.
- [ ] Can start a service now and enable it at boot with OpenRC.
- [ ] Can tell an init script from its `/etc/conf.d` configuration.
- [ ] Can run a command at every boot with `local.d`.
- [ ] Completed Labs 4.1–4.3 including each negative test.
