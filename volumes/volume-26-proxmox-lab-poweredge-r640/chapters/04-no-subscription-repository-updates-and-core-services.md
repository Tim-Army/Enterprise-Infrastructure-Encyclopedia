# Chapter 04: The No-Subscription Repository, Updates, and Core Services

## Learning Objectives

- Explain Proxmox's subscription model and what the "free version" actually
  is.
- Switch the node from the enterprise repository to the no-subscription
  repository.
- Bring Proxmox VE fully up to date safely.
- Point the node at the gateway (10.30.161.1) for DNS and NTP time.
- Confirm the node is current, resolving names, and keeping time.

## Theory and Architecture

### What "activate the free version" means

Proxmox VE is free and open-source; there is no paid "version" to unlock.
What the subscription model gates is the **enterprise update repository**, a
tested, stable update stream that requires a paid subscription key. A fresh
install points at that enterprise repository, which is why the web interface
shows a subscription warning and why updates fail until this is changed.

"Activating the free version" therefore means one specific thing: **switch
from the enterprise repository to the no-subscription repository.** The
no-subscription repository provides the same packages on a slightly less
conservative release cadence, needs no key, and is the correct choice for a
lab. This is a configuration change, not a license activation — an important
distinction, because there is no key to enter and nothing to purchase.

### The repositories involved

Proxmox VE's package sources on a fresh install include:

- **`pve-enterprise`** — the paid, subscription-gated repository. It must be
  disabled for a no-subscription setup, or updates error on it.
- **`pve-no-subscription`** — the free repository. It must be enabled.
- **The Debian base repositories** — Proxmox is built on Debian, so its base
  and security repositories are also in play and stay enabled.
- **`ceph` repositories** — relevant only if using Ceph storage, which this
  single-node build does not.

### Why DNS and NTP point at the gateway

This build routes the node's **DNS and NTP through the gateway,
10.30.161.1** — "the gateway for NTP, DNS, and any other services," as the
specification puts it. Correct time and name resolution are not optional
niceties:

- **Time** — certificate validation, cluster operations (if ever added), and
  correlated logging all depend on accurate time. A node whose clock drifts
  produces confusing, hard-to-correlate failures.
- **DNS** — the node resolves package mirrors, the gateway, and any hostnames
  it references through DNS. Pointing at the gateway keeps resolution
  consistent with the rest of the environment.

## Design Considerations

- **Disable the enterprise repository explicitly, do not just add the free
  one.** Leaving `pve-enterprise` enabled without a key makes every
  `apt update` throw an error on it. Disable it and enable
  `pve-no-subscription`.
- **Update once, fully, before building on the node.** A node updated to
  current before the network, storage, and VMs are configured avoids
  updating under load later. Do the full upgrade now.
- **Point DNS and NTP at the gateway deliberately.** The build specifies the
  gateway for these services; configuring them now means every later step
  runs with correct time and resolution.
- **Expect and dismiss the subscription nag correctly.** The web UI's
  subscription warning is informational on the no-subscription repository;
  it is not an error and does not need a workaround beyond knowing it is
  expected.

## Implementation and Automation

### 1. Switching to the no-subscription repository

On the Proxmox node (SSH as root, or the web UI's shell):

```bash
# Disable the enterprise repository.
# (On PVE 8/9 the enterprise repos live in these files.)
sed -i 's/^deb/#deb/' /etc/apt/sources.list.d/pve-enterprise.list
# If a Ceph enterprise repo exists and is unused, disable it too.
[ -f /etc/apt/sources.list.d/ceph.list ] && \
  sed -i 's/^deb/#deb/' /etc/apt/sources.list.d/ceph.list

# Enable the no-subscription repository.
cat > /etc/apt/sources.list.d/pve-no-subscription.list <<'EOF'
deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription
EOF
# (Match the Debian codename to your PVE release — e.g. the PVE 9 base.)

# Refresh package lists — this should now succeed with no enterprise error.
apt update
```

### 2. Updating to the latest version

```bash
# Full distribution upgrade to the current no-subscription packages.
apt full-upgrade -y

# Reboot if the kernel was updated, so the node runs the new kernel.
[ -n "$(ls /boot/vmlinuz-* 2>/dev/null | tail -1)" ] && systemctl reboot
```

After the reboot, confirm the running version:

```bash
pveversion            # the Proxmox VE version string
uname -r              # the running kernel
```

### 3. Pointing DNS and NTP at the gateway

```bash
# DNS: resolve through the gateway.
cat > /etc/resolv.conf <<'EOF'
nameserver 10.30.161.1
EOF
# (On a systemd-resolved or ifupdown-managed node, set this via the network
# configuration so it survives reboots — finalized with the management
# interface in Chapter 05.)

# Time: point the node's time sync at the gateway.
# Proxmox uses chrony (or systemd-timesyncd); set the gateway as the source.
sed -i '/^pool /d;/^server /d' /etc/chrony/chrony.conf 2>/dev/null
echo 'server 10.30.161.1 iburst' >> /etc/chrony/chrony.conf
systemctl restart chrony 2>/dev/null || systemctl restart systemd-timesyncd
```

### 4. Confirming current, resolving, and keeping time

```bash
# Up to date: no further upgrades pending.
apt update && apt list --upgradable

# DNS resolves through the gateway.
getent hosts download.proxmox.com

# Time is synchronized to the gateway.
chronyc sources 2>/dev/null || timedatectl status
```

## Validation and Troubleshooting

### The three things this chapter must leave true

| State | Check | Failure means |
| --- | --- | --- |
| No enterprise repo error | `apt update` runs clean | `pve-enterprise` still enabled without a key |
| Fully updated | `apt list --upgradable` empty | Upgrade not run, or a held package |
| DNS resolves | `getent hosts ...` returns an address | Resolver not pointed at the gateway |
| Time synced | `chronyc sources` shows the gateway | NTP source not set, or gateway not serving time |

### The enterprise-repository error

The most common post-install problem is `apt update` failing with a
401/authentication error on `enterprise.proxmox.com`. The cause is always
the same: the enterprise repository is still enabled without a subscription
key. Disabling it (commenting the `deb` line) resolves it; adding the
no-subscription repository alone does not, because the enterprise line still
errors.

### Time not syncing

If `chronyc sources` shows no reachable source, confirm the gateway
(10.30.161.1) actually serves NTP and is reachable from the node. A node
that cannot sync time will produce certificate and logging problems later
that are hard to trace back to the clock — which is why this is validated
now, not discovered later.

## Security and Best Practices

- **Keep the node updated on a cadence, not once.** This chapter brings it
  current; staying current is ongoing, and a lab node still carries known
  vulnerabilities if left unpatched.
- **Verify package sources.** The no-subscription repository is an official
  Proxmox source; do not add untrusted third-party repositories that could
  introduce unverified packages into the hypervisor.
- **Correct time is a security control.** Accurate time underpins
  certificate validation and log correlation; the gateway NTP source is part
  of the security posture, not just housekeeping.
- **Restrict outbound access from the management interface appropriately.**
  The node needs to reach the package mirrors and the gateway; it does not
  need broad internet access, and limiting it reduces exposure.

## References and Knowledge Checks

**References**

- [Proxmox VE package repositories documentation](https://pve.proxmox.com/wiki/Package_Repositories)
  — the authoritative source on the enterprise and no-subscription repos.
- [Volume XIV, Chapter 01](../../volume-14-red-hat-enterprise-linux-10/chapters/01-installation-subscriptions-repositories-and-cockpit.md)
  — subscription and repository management concepts, applied here to
  Proxmox's Debian base.
- [Chapter 05](05-network-architecture-management-nic-vlan-trunk-and-bridges.md)
  — where the DNS and management addressing set here is finalized on the
  interface configuration.

**Knowledge checks**

1. What does "activate the free version of Proxmox" actually mean, and why
   is there no key to enter?
2. Which repository must be disabled and which enabled, and what error
   appears if the first is left on?
3. Why does this build point DNS and NTP at the gateway, and what breaks if
   time is wrong?
4. What is the correct response to the web UI's subscription warning on a
   no-subscription node?
5. Why is updating fully now, before configuring network and VMs, better
   than updating later?

## Hands-On Lab

**Objective:** Switch the node to the no-subscription repository, bring it
fully up to date, and point DNS and NTP at the gateway.

**Prerequisites:** The installed Proxmox node from
[Chapter 03](03-installing-proxmox-ve.md), reachable on its management
address, with a path to the Proxmox package mirrors and the gateway.

**This lab is reproducible on any Proxmox node**, hardware or nested — the
repository and service configuration is not hardware-specific.

**Procedure**

1. Disable the `pve-enterprise` repository and enable `pve-no-subscription`.
   Run `apt update` and confirm it completes with no enterprise error.
2. Run `apt full-upgrade`, and reboot if the kernel updated.
3. Confirm the version with `pveversion` and `uname -r`.
4. Point the resolver at 10.30.161.1 and confirm `getent hosts
   download.proxmox.com` resolves.
5. Set the NTP source to 10.30.161.1 and confirm `chronyc sources` (or
   `timedatectl`) shows the node synchronized to the gateway.

**Negative test**

6. Re-enable the `pve-enterprise` repository, run `apt update`, and observe
   the authentication error on `enterprise.proxmox.com` — confirming that
   the enterprise repo, not a missing free repo, is what causes the common
   post-install update failure. Disable it again and confirm `apt update`
   is clean.

**Expected results**

- `apt update` runs clean with no enterprise error.
- The node is fully updated and running the current kernel.
- DNS resolves through the gateway and time is synchronized to it.

**Cleanup**

7. Leave the no-subscription repository and the gateway DNS/NTP settings in
   place — they are the node's steady state for the rest of the build.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

"Activating the free version" of Proxmox is not a license step — Proxmox VE
is already free — but a repository switch: disabling the subscription-gated
`pve-enterprise` repository and enabling `pve-no-subscription`, which is why
the fix for the ubiquitous post-install update error is disabling the
enterprise repo rather than adding anything. With the free repository in
place the node is brought fully current, and its DNS and NTP are pointed at
the gateway (10.30.161.1) so that name resolution and, critically, time are
correct before the network, storage, and VMs are built on top — because a
node with the wrong time produces certificate and logging failures that are
painful to trace later.

- [ ] `pve-enterprise` disabled, `pve-no-subscription` enabled.
- [ ] `apt update` runs clean and the node is fully upgraded.
- [ ] Running the current Proxmox VE version and kernel.
- [ ] DNS resolves through the gateway 10.30.161.1.
- [ ] Time synchronized to the gateway.
