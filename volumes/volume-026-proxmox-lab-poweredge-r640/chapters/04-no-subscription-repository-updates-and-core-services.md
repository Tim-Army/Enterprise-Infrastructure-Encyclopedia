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

**A note on the file format.** PVE 9 is built on Debian 13 (**trixie**) and
uses APT's **deb822 `.sources`** format: each repository is a key/value stanza
(`Types:`, `URIs:`, `Suites:`, `Components:`, `Signed-By:`) in a
`/etc/apt/sources.list.d/*.sources` file, and you **disable** one by adding
**`Enabled: false`** to its stanza. This replaces the older one-line
`deb http://… bookworm …` entries in `.list` files that PVE 8 (Debian
bookworm) used, where disabling meant commenting the line out. On a fresh PVE 9
install only the `.sources` files exist; a node upgraded in place from PVE 8
can carry the old `.list` files until `apt modernize-sources` converts them.
Everything below therefore edits `.sources` stanzas, not `.list` lines.

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
  `apt update` throw an error on it. On PVE 9 disable it by setting
  `Enabled: false` in its `.sources` stanza, and enable `pve-no-subscription`.
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
# PVE 9 is built on Debian 13 (trixie) and uses APT's deb822 ".sources"
# format: key/value stanzas in /etc/apt/sources.list.d/*.sources. Disabling a
# repo means setting "Enabled: false" in its stanza — the deb822 equivalent of
# commenting out the old one-line "deb" entry that PVE 8 (Debian bookworm) used.

# Disable the enterprise repos: pve-enterprise, and the Ceph enterprise repo a
# fresh install also drops. Set "Enabled: false" in place, which preserves each
# repo's release (the shipped Ceph line is e.g. ceph-squid or ceph-tentacle):
for repo in pve-enterprise ceph; do
  src="/etc/apt/sources.list.d/${repo}.sources"
  [ -f "$src" ] || continue
  if grep -q '^Enabled:' "$src"; then
    sed -i 's/^Enabled:.*/Enabled: false/' "$src"
  else
    printf 'Enabled: false\n' >> "$src"
  fi
done

# Enable the no-subscription repository (deb822; no "Enabled:" line means
# enabled). Suites is "trixie" — Debian 13, the base for the whole PVE 9 line:
cat > /etc/apt/sources.list.d/pve-no-subscription.sources <<'EOF'
Types: deb
URIs: http://download.proxmox.com/debian/pve
Suites: trixie
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
EOF

# A fresh PVE 9 install is already deb822. A node upgraded in place from PVE 8
# may still carry old one-line ".list" files; `apt modernize-sources` converts
# them to deb822. Remove any stale enterprise ".list" so it can't re-add the error:
rm -f /etc/apt/sources.list.d/pve-enterprise.list /etc/apt/sources.list.d/ceph.list 2>/dev/null

# Refresh package lists — now clean, hitting download.proxmox.com with no 401.
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
key. Disabling it resolves it — on PVE 9 that means setting `Enabled: false`
in `pve-enterprise.sources` (on PVE 8, commenting the `deb` line in
`pve-enterprise.list`); adding the no-subscription repository alone does not,
because the enterprise stanza still errors. A fresh PVE 9 install drops the
same enterprise stanza for Ceph in `ceph.sources`, which 401s the same way —
disable it too unless you are adding a matching no-subscription Ceph repo.

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
- [Volume XIV, Chapter 01](../../volume-014-red-hat-enterprise-linux-10/chapters/01-installation-subscriptions-repositories-and-cockpit.md)
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

This chapter carries a topic-level walkthrough lab for **each post-install configuration step** —
the no-subscription repository, updates, and the core Proxmox services. Every step is a runnable
command on the node. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 4.1–4.4** — a freshly installed Proxmox VE node (Chapter 03) with
root SSH, and internet access. **Cost:** none (the no-subscription repo is free).

### Lab 4.1 — Switch to the no-subscription repository (Topic: Repositories)

**Objective:** Point APT at the free community repo.

```bash
# PVE 9 uses the deb822 ".sources" format. Disable the enterprise repo by
# setting "Enabled: false" in its stanza, then write the no-subscription
# ".sources" (auto-filling the Debian codename — "trixie" on PVE 9):
src=/etc/apt/sources.list.d/pve-enterprise.sources
[ -f "$src" ] && { grep -q '^Enabled:' "$src" \
  && sed -i 's/^Enabled:.*/Enabled: false/' "$src" \
  || printf 'Enabled: false\n' >> "$src"; }
cat > /etc/apt/sources.list.d/pve-no-subscription.sources <<EOF
Types: deb
URIs: http://download.proxmox.com/debian/pve
Suites: $(. /etc/os-release; echo "$VERSION_CODENAME")
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
EOF
apt update
```

**Expected result:** `apt update` succeeds against the `pve-no-subscription` repo instead of erroring
on the enterprise repo — a Proxmox node without a subscription must use the no-subscription
repository to receive package updates; the enterprise repo returns 401 without a key. On PVE 9 the
`.sources` stanza with `Enabled: false` is the deb822 equivalent of commenting out the old
`.list` line.

**Negative test:** leave only the enterprise repo enabled with no subscription; `apt update` fails
with a 401 and the node never updates — the no-subscription repo is what a free/lab node updates
from.

**Rollback:** none (keep the repo configured).

### Lab 4.2 — Update and upgrade (Topic: Updates)

**Objective:** Bring the node current.

```bash
apt update && apt -y full-upgrade
pveversion -v | grep -E "pve-manager|proxmox-kernel|pve-kernel|qemu"
```

**Expected result:** the node upgrades to the current no-subscription package set (kernel, pve-
manager, QEMU) — keeping Proxmox current picks up security and stability fixes; `full-upgrade` (not
just `upgrade`) is used because PVE upgrades sometimes need to install/remove dependent packages.

**Negative test:** use `apt upgrade` alone across a PVE point release that changes dependencies;
some packages are held back and the node ends in a partial state — `full-upgrade` handles the
dependency changes Proxmox releases require.

**Rollback:** reboot if a new kernel was installed (`reboot`) during a maintenance window.

### Lab 4.3 — Core services (Topic: Services)

**Objective:** Confirm the Proxmox control-plane services are healthy.

```bash
systemctl status pve-cluster pvedaemon pveproxy pvestatd --no-pager | grep -E "●|Active" | head
pvesh get /cluster/resources --output-format json 2>/dev/null | python3 -c "import json,sys; print('resources visible:', len(json.load(sys.stdin)))"
```

**Expected result:** `pve-cluster` (the config filesystem `/etc/pve`), `pvedaemon`/`pveproxy` (API/
UI), and `pvestatd` (stats) are all active, and the API returns cluster resources — these services
are Proxmox's control plane; `/etc/pve` is a special FUSE filesystem backed by `pve-cluster`, so if
it is down, configuration cannot be read or written.

**Negative test:** edit files under `/etc/pve` when `pve-cluster` is stopped; writes fail because
that path is the pmxcfs FUSE mount, not a normal directory — the service must be running for config
to work.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 4.4 — Remove the subscription nag (Topic: UI configuration)

**Objective:** Suppress the no-subscription login popup (lab convenience).

```bash
# The community-documented one-liner patches the JS that shows the subscription warning:
sed -i "s/data.status !== 'Active'/false/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js 2>/dev/null
systemctl restart pveproxy
# (Re-applies after a pve-manager upgrade; not required for function.)
```

**Expected result:** the "No valid subscription" popup no longer appears at login on this lab node —
the nag is cosmetic (the node works fully without a subscription); patching it is a lab convenience,
and it reappears after upgrades that replace the JS file.

**Negative test:** treat the subscription popup as a functional block; it is not — the node updates
and runs VMs fine on the no-subscription repo, so the popup is informational only.

**Rollback:** none (the patch is reverted by the next `proxmox-widget-toolkit` upgrade anyway).

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
