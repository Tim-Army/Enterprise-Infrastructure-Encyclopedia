# Chapter 02: ESXi 7 Installation and Host Configuration

## Learning Objectives

- Install ESXi 7 and complete initial configuration.
- Manage the host with the DCUI, Host Client, and esxcli.
- Configure management networking, NTP, and services.
- Configure host storage and scratch.
- Complete a walkthrough for each host-configuration topic.

## Theory and Architecture

**ESXi 7** installs directly on server hardware (or nested for labs) from an ISO, writing a small
hypervisor to a boot device. Initial configuration happens at the **DCUI** (Direct Console User
Interface — set the root password and a **management network**: a VMkernel adapter with an IP,
usually on `vmk0`). Day-to-day host management uses the **VMware Host Client** (the per-host HTML5
UI), **esxcli** (the comprehensive command-line namespace), and PowerCLI/API. Key host settings
include **NTP** (accurate time is critical for vCenter, certificates, and logs), **services** (SSH,
the shell — enabled only as needed), **syslog** (forwarding logs off-host), and **scratch/coredump**
locations. A host joins **vCenter** to become part of a cluster. Understanding host configuration —
especially **esxcli** — is the foundation for everything above it.

## Design Considerations

Standardize host configuration (ideally via **host profiles** or vLCM images, Chapter 8) so hosts
are identical. Keep **SSH/shell disabled** except during maintenance. Configure **NTP** and
**syslog** on every host. Put the **management network** on redundant NICs. Automate host config
with esxcli/PowerCLI rather than per-host clicking.

## Implementation and Automation

The labs configure the management network, NTP, services, and inspect the host with esxcli.

## Validation and Troubleshooting

Confirm the host model:

```text
Install: ISO -> boot device -> DCUI (root pw + management network vmk0).
Manage: DCUI + Host Client (HTML5) + esxcli + PowerCLI/API. Services: SSH/shell (as needed), syslog, NTP.
Join vCenter -> cluster. Standardize via host profiles / vLCM images.
```

Common pitfalls: **no NTP** (certificate/vCenter/log problems); and leaving **SSH enabled**
permanently (security exposure).

## Security and Best Practices

Enable **NTP** and **syslog** everywhere, keep **SSH/shell** off except for maintenance, use
**lockdown mode** where appropriate (Chapter 8), and standardize configuration. Redundant
management NICs. Automate for consistency. These are host-hardening basics.

## Hands-On Lab

Host-configuration walkthroughs. **Shared prerequisites** — an ESXi 7 host (physical or nested)
with shell access, in a lab. **Cost:** none.

### Lab 2.1 — Inspect the management network

**Objective:** Verify the VMkernel management adapter.

```bash
esxcli network ip interface ipv4 get
esxcli network ip interface list
```

**Expected result:** the **vmk0** management interface with its IPv4 address — the host's presence
on the network.

**Negative test:** assume management connectivity without checking **vmk0**; verify the VMkernel
adapter and IP.

**Cleanup:** none (read-only).

### Lab 2.2 — Configure NTP

**Objective:** Set accurate time.

```bash
esxcli system ntp set --server=pool.ntp.org --enabled=true
esxcli system ntp get
```

**Expected result:** **NTP** enabled and synchronized — accurate time for certificates, vCenter,
and logs.

**Negative test:** run a host with **no NTP**; time drift breaks certificate validation and vCenter
operations — enable NTP.

**Cleanup:** `esxcli system ntp set --enabled=false` (in a lab).

### Lab 2.3 — Manage a service (SSH)

**Objective:** Control host services safely.

```bash
esxcli network firewall ruleset list --ruleset-id=sshServer
# Enable only for maintenance, then disable:
vim-cmd hostsvc/enable_ssh; vim-cmd hostsvc/disable_ssh
esxcli system syslog config get
```

**Expected result:** SSH toggled for maintenance and **syslog** configuration shown — controlled
services.

**Negative test:** leave **SSH permanently enabled**; enable it only when needed — reduce the attack
surface.

**Cleanup:** ensure SSH is disabled after the lab.

### Lab 2.4 — Inspect host hardware and storage

**Objective:** Review host resources and datastores.

```bash
esxcli hardware cpu list | head
esxcli storage filesystem list
esxcli storage core device list | head
```

**Expected result:** the host's **CPU, filesystems (datastores), and storage devices** — the
resource inventory.

**Negative test:** provision VMs without checking **storage/scratch**; verify datastores and free
space first.

**Cleanup:** none (read-only).

### Lab 2.5 — Set the host to maintenance mode

**Objective:** Prepare a host for changes safely.

```bash
esxcli system maintenanceMode set --enable=true
esxcli system maintenanceMode get
esxcli system maintenanceMode set --enable=false
```

**Expected result:** the host entering and exiting **maintenance mode** — the safe state for
patching/changes (VMs evacuate via DRS/vMotion in a cluster).

**Negative test:** patch or reboot a host with running VMs and no maintenance mode; **enter
maintenance mode** first so VMs migrate off.

**Cleanup:** ensure the host is out of maintenance mode.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ESXi 7 installs from ISO and is configured via the DCUI, Host Client, and esxcli: management
networking, NTP, controlled services, syslog, and storage. Standardize configuration, keep SSH off
except for maintenance, sync time everywhere, and use maintenance mode for changes.

- [ ] I can inspect the management network with esxcli.
- [ ] I can configure NTP.
- [ ] I can manage host services safely.
- [ ] I can enter/exit maintenance mode.
- [ ] I completed Labs 2.1–2.5 including each negative test.
