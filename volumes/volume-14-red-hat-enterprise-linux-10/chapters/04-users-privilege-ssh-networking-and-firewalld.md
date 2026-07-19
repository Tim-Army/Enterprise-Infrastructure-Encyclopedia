# Chapter 04: Users, Privilege, SSH, Networking, and firewalld

![Lab topology for this chapter: a scoped operator account authenticates via SSH key with no password prompt, and sudo -l confirms exactly two permitted systemctl commands, not full root. SSH on a second interface is restricted by a firewalld rich rule to one client subnet, with the plain ssh service removed from that zone's service list. As a negative test, five repeated wrong-password login attempts are sent against the account; faillock records the failures and, once the configured threshold is exceeded, temporarily locks the account. Resetting the lockout restores normal access.](../../../diagrams/volume-14-red-hat-enterprise-linux-10/chapter-04-scoped-sudo-ssh-lockout-topology.svg)

*Figure 4-1. Topology used throughout this chapter's Hands-On Lab: a scoped operator account with delegated sudo and source-restricted SSH, tested against a brute-force lockout.*

## Learning Objectives

- Create and manage local users and groups, including password aging
  and account lockout policy.
- Delegate administrative privilege safely using `sudo` and understand
  where PAM enforces authentication and account policy.
- Configure and harden SSH for both password and key-based
  authentication.
- Configure host networking with `nmcli` and `nmtui`, including static
  addressing, bonding, and DNS resolution.
- Manage `firewalld` zones, services, ports, and rich rules to control
  inbound and outbound traffic.
- Diagnose common identity, connectivity, and firewall failures using
  the correct tool for each layer.

## Theory and Architecture

Identity, remote access, and network reachability are the three layers
an administrator must get right before any service on a RHEL 10 host
can be considered production-ready. Each layer has its own
authoritative data store and its own tooling, but they compose: a
user's ability to reach a host over SSH depends on the network being
configured correctly, the firewall permitting the connection, `sshd`
being configured to accept it, and the account's password and PAM
policy allowing authentication to succeed.

### Local identity: users, groups, and the shadow suite

RHEL 10 stores local account data in four files, collectively known as
the shadow password suite:

| File | Contents |
| --- | --- |
| `/etc/passwd` | Username, UID, primary GID, GECOS field, home directory, login shell |
| `/etc/shadow` | Hashed password, password aging fields, account expiration (root-readable only) |
| `/etc/group` | Group names, GIDs, and supplementary member lists |
| `/etc/gshadow` | Group password hashes and administrators (rarely used directly) |

`useradd` and `groupadd` write to these files using defaults drawn from
`/etc/login.defs` (UID/GID ranges, password aging defaults) and
`/etc/default/useradd` (default shell, home directory skeleton from
`/etc/skel`). UID ranges matter operationally: system accounts
(services, daemons) occupy a low range below `SYS_UID_MIN`/`UID_MIN`
(typically below 1000), while interactive human accounts start at
`UID_MIN`. Every account belongs to exactly one **primary group** and
may belong to any number of **supplementary groups**, which is how
RHEL grants access to shared resources (for example, membership in
`wheel` for sudo, or a service-specific group for shared file access)
without editing per-file permissions for every user.

### Privilege delegation: sudo and PAM

RHEL 10 does not expect interactive root logins for routine
administration; instead, `sudo` grants scoped, logged privilege
escalation from an unprivileged account. The `/etc/sudoers` file
(never edited directly — always through `visudo`, which validates
syntax before saving) and drop-in files under `/etc/sudoers.d/` define
who may run what as whom. The `wheel` group is the conventional
RHEL grant point: membership plus a sudoers rule for `%wheel` is the
standard "this account can administer this host" pattern.

Underneath both local login and `sudo`, **PAM (Pluggable
Authentication Modules)** is the actual policy engine. Each
PAM-aware service (`login`, `sshd`, `sudo`, `su`) has a stack defined
under `/etc/pam.d/`, and modules like `pam_faillock` (account lockout
after repeated failures) and `pam_pwquality` (password complexity)
plug into that stack without the calling application needing any
awareness of the policy being enforced. This separation is why
password complexity and lockout behavior can be changed system-wide by
editing PAM configuration once, rather than reconfiguring every
service that authenticates users.

### SSH architecture

`sshd` is the standard remote administration path for RHEL 10 and, in
most fleets, the only network-facing login mechanism enabled at all.
Authentication can use a password (validated through PAM, same as a
local login) or a public/private key pair: the server holds the
public key in the target account's `~/.ssh/authorized_keys`, and a
successful connection proves possession of the matching private key
without the private key or the password ever crossing the network.
Host keys (server-side, generated once per host, `/etc/ssh/ssh_host_*`)
let a client detect a changed or spoofed server; the client-side
`known_hosts` warning on a changed host key is a security control, not
a nuisance to suppress.

### NetworkManager

RHEL 10 manages all network interfaces through **NetworkManager**,
exposed via the `nmcli` command-line tool, the `nmtui` text UI, and
Cockpit's networking module ([Chapter 01](01-installation-subscriptions-repositories-and-cockpit.md)) — all three ultimately create
and modify the same **connection profiles**, stored as keyfiles under
`/etc/NetworkManager/system-connections/`. A connection profile binds
settings (IPv4/IPv6 addressing, DNS, routes) to a device or a matching
criterion, and a device activates at most one connection profile at a
time. This model supports more than simple static/DHCP addressing:
bonding and teaming aggregate multiple physical interfaces for
throughput or redundancy, and VLAN sub-interfaces tag traffic for
network segmentation, all as connection profiles layered on top of
physical device profiles.

### firewalld architecture

`firewalld` is RHEL 10's dynamic firewall management layer, using
`nftables` as its underlying packet-filtering backend (the successor
to the deprecated `iptables` backend from earlier RHEL releases).
Its core abstraction is the **zone**: a named set of rules
(services, ports, rich rules, and trust level) applied to one or more
network interfaces or source addresses. A host's interfaces are each
assigned to exactly one zone at a time, and the zone determines what
traffic is permitted by default — `public` (the default zone, "reject
what is not explicitly allowed"), `trusted` (allow everything, useful
for an isolated management network), `drop`, `internal`, `dmz`, and
others, each shipping a different default policy. Changes made without
`--permanent` apply immediately to the runtime configuration but are
lost on reload or reboot; changes made with `--permanent` persist but
require `firewall-cmd --reload` (or a service restart) to take
runtime effect — administrators frequently apply both flags together
during change windows to get an immediate, persistent result in one
step.

## Design Considerations

- **UID/GID range planning.** In environments mixing local and
  directory-service (LDAP/IdM/Active Directory) accounts, reserve
  local UID/GID ranges deliberately so they never collide with a
  directory-assigned range; a collision produces confusing,
  intermittent permission behavior that is difficult to diagnose after
  the fact.
- **sudo scope, not blanket wheel membership.** Granting broad `wheel`
  membership is simple but over-permissions every member for every
  command; role-scoped `sudoers.d` rules (a specific command set for a
  specific group) reduce blast radius from a compromised or misused
  account, at the cost of more rules to maintain.
- **Password authentication vs. key-only SSH.** Key-only SSH access
  eliminates password-guessing and credential-stuffing risk entirely
  for that path, but requires a working key-distribution and
  key-rotation process; environments without one yet should still
  disable root password login immediately while building toward
  key-only access fleet-wide.
- **Static addressing vs. DHCP with reservations.** Servers generally
  warrant static addressing or a DHCP reservation tied to the
  interface's MAC address so IP addresses remain predictable for
  firewall rules, monitoring, and DNS; pure dynamic DHCP is
  appropriate for less critical or highly ephemeral hosts.
- **Default-deny firewall posture.** Standardize on the `public` zone
  (or a custom equally restrictive zone) as the default and add
  services/ports explicitly, rather than starting from `trusted` and
  trying to remove access later — it is much easier to audit "what is
  allowed" than to audit "what was never removed."
- **Rich rules vs. zones for exceptions.** A one-off, source-scoped
  exception (a single monitoring host allowed to reach a management
  port) is a good fit for a firewalld rich rule; a broad category of
  hosts needing a different overall policy is better modeled as a
  separate zone assigned to the relevant interface or source range.

## Implementation and Automation

### 1. User and group management

```bash
# Create a user with a specific UID, primary group, and shell
useradd -u 2001 -g devops -G wheel -s /bin/bash -m jsmith

# Set or change a password (interactive)
passwd jsmith

# Modify an existing account: add a supplementary group
usermod -aG developers jsmith

# Lock and unlock an account without deleting it
usermod -L jsmith
usermod -U jsmith

# Delete a user and their home directory
userdel -r jsmith

# Create a group
groupadd devops

# Password aging: force change every 90 days, warn 7 days prior
chage -M 90 -W 7 jsmith
chage -l jsmith
```

### 2. Delegating privilege with sudo

```bash
# Always edit sudoers through visudo (syntax-checked before save)
visudo

# Grant the wheel group full sudo access (typical default, already present)
# %wheel  ALL=(ALL)       ALL

# Scoped delegation: allow a specific group to manage only httpd, via a drop-in
cat > /etc/sudoers.d/webteam-httpd <<'EOF'
%webteam ALL=(root) /usr/bin/systemctl restart httpd, /usr/bin/systemctl status httpd
EOF
visudo -cf /etc/sudoers.d/webteam-httpd

# Confirm what a user is permitted to run
sudo -l -U jsmith
```

### 3. PAM account lockout policy

```bash
# Inspect the current authselect profile
authselect current

# Enable faillock (account lockout after repeated failures) via authselect
authselect enable-feature with-faillock
authselect apply-changes

# Review and manually clear a lockout
faillock --user jsmith
faillock --user jsmith --reset
```

### 4. SSH configuration and key-based authentication

```bash
# Generate an ed25519 keypair on the client
ssh-keygen -t ed25519 -C "jsmith@workstation"

# Copy the public key to a remote account's authorized_keys
ssh-copy-id jsmith@server01.example.com

# Harden sshd_config (server side)
sed -i \
  -e 's/^#\?PermitRootLogin.*/PermitRootLogin no/' \
  -e 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' \
  -e 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/' \
  /etc/ssh/sshd_config

# Validate configuration syntax before restarting
sshd -t

sudo systemctl restart sshd
```

### 5. Networking with nmcli

```bash
# Show all connection profiles and device status
nmcli connection show
nmcli device status

# Create a static IPv4 connection profile on ens192
nmcli connection add type ethernet ifname ens192 con-name ens192-static \
  ipv4.method manual ipv4.addresses 192.0.2.10/24 \
  ipv4.gateway 192.0.2.1 ipv4.dns "192.0.2.53 192.0.2.54"

nmcli connection up ens192-static

# Set the hostname
hostnamectl set-hostname server01.example.com

# Create an active-backup bond across two interfaces
nmcli connection add type bond con-name bond0 ifname bond0 \
  bond.options "mode=active-backup,miimon=100"
nmcli connection add type ethernet ifname ens224 master bond0
nmcli connection add type ethernet ifname ens225 master bond0
nmcli connection up bond0

# Text UI, useful over a console/serial connection
nmtui
```

### 6. firewalld zones, services, and rich rules

```bash
# Show the default zone and all active zone-to-interface bindings
firewall-cmd --get-default-zone
firewall-cmd --get-active-zones

# List everything currently allowed in the default zone
firewall-cmd --list-all

# Allow the SSH and HTTPS services persistently, then apply
firewall-cmd --add-service=ssh --permanent
firewall-cmd --add-service=https --permanent
firewall-cmd --reload

# Allow a specific TCP port not covered by a named service
firewall-cmd --add-port=8443/tcp --permanent
firewall-cmd --reload

# Restrict a management port to a single source subnet with a rich rule
firewall-cmd --add-rich-rule='rule family="ipv4" source address="10.10.10.0/24" port protocol="tcp" port="9090" accept' --permanent
firewall-cmd --reload

# Assign an interface to a non-default zone
firewall-cmd --zone=internal --change-interface=ens224 --permanent
firewall-cmd --reload
```

## Validation and Troubleshooting

- **Confirm account and group state.** `id jsmith` shows resolved
  UID/GID and every group membership in one command; `getent passwd
  jsmith` confirms name-service resolution (local or directory-based)
  rather than only checking `/etc/passwd` directly.
- **Diagnose a sudo denial.** `sudo -l` for the affected user shows
  exactly what that account is permitted to run; a syntax error in a
  `sudoers.d` file is caught at edit time by `visudo -cf`, but a rule
  that is syntactically valid and simply does not match the attempted
  command is the more common real-world cause — compare the rule text
  to the exact command and arguments attempted.
- **Diagnose an account lockout.** `faillock --user <name>` shows the
  failure count and timestamps; a legitimate user locked out after a
  password rotation is a routine `faillock --user <name> --reset`
  after confirming the new password is correct.
- **Diagnose SSH authentication failures.** Run `sshd -T` on the
  server to see the fully resolved effective configuration (catches
  drop-in file overrides), and check `journalctl -u sshd` for the
  specific rejection reason (`Authentication refused: bad ownership or
  modes for directory /home/jsmith` is a common one — `sshd` refuses
  to trust `authorized_keys` if the home directory or `.ssh` directory
  is group- or world-writable).
- **Diagnose a network connection that will not come up.**
  `nmcli connection show <name>` and `nmcli device show <device>`
  report the active state and last error;
  `journalctl -u NetworkManager` shows activation failures in detail,
  and `ip addr` / `ip route` confirm what was actually applied versus
  what the profile intends.
- **Diagnose a blocked connection through firewalld.**
  `firewall-cmd --list-all --zone=<zone>` confirms what is actually
  allowed on the zone bound to the relevant interface (not
  necessarily the default zone); `ss -tlnp` confirms the service is
  actually listening before blaming the firewall at all — a connection
  refused error is often a stopped service, not a firewall rule.
- **Common failure: runtime-only firewall changes lost on reload.** A
  `firewall-cmd` command issued without `--permanent` works
  immediately but disappears on the next `--reload` or reboot; always
  decide deliberately whether a change is a temporary test
  (`--timeout=` is useful here) or a permanent policy change.

## Security and Best Practices

- Disable direct root SSH login (`PermitRootLogin no`) and require
  `sudo` for privileged actions, so every privileged action is
  individually attributable and logged.
- Move to key-only SSH authentication
  (`PasswordAuthentication no`) as soon as key distribution is in
  place, and protect private keys with a passphrase plus an
  `ssh-agent`, never storing an unencrypted private key on a shared or
  multi-user system.
- Scope `sudoers` rules to specific commands per role rather than
  granting `ALL=(ALL) ALL` to every administrator; use `sudoers.d`
  drop-in files so role changes do not require editing the monolithic
  `sudoers` file.
- Enforce `pam_faillock` account lockout and `pam_pwquality` complexity
  requirements through `authselect`, and monitor `faillock` events as
  a brute-force indicator, not just an inconvenience to reset.
- Keep the default firewalld zone deny-by-default and add only the
  services and ports a host's role actually requires; remove a rule
  when the service it supported is decommissioned, rather than letting
  firewall policy accumulate indefinitely.
- Scope sensitive management ports (Cockpit, database admin ports,
  monitoring agents) to a management-network source using rich rules
  or a dedicated zone rather than the host's general-purpose interface
  zone.
- Rotate and audit SSH keys the same way credentials are rotated
  elsewhere; a stale `authorized_keys` entry for a departed
  administrator is a persistent, easily overlooked access path.

## References and Knowledge Checks

**References**

- [`useradd(8)`, `usermod(8)`, `chage(1)`, `sudoers(5)`, `visudo(8)` man
  pages.](https://man7.org/linux/man-pages/man8/useradd.8.html)
- [`pam.d(5)`, `pam_faillock(8)`, `authselect(8)` man pages.](https://man7.org/linux/man-pages/man5/pam.d.5.html)
- [`sshd_config(5)`, `ssh-keygen(1)` man pages.](https://man7.org/linux/man-pages/man5/sshd_config.5.html)
- [`nmcli(1)`, NetworkManager documentation, Red Hat Customer Portal.](https://networkmanager.dev/docs/)
- [`firewalld.zones(5)`, `firewall-cmd(1)` man pages.](https://firewalld.org/documentation/)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — RHEL 10
  baseline referenced throughout this chapter.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  RHCSA (EX200) blueprint mapping for this volume.

**Knowledge checks**

1. What is the practical difference between a primary group and a
   supplementary group, and how does `wheel` membership typically
   interact with `sudoers`?
2. Why does `sshd` refuse key-based authentication when a user's home
   directory is group-writable, even if `authorized_keys` itself has
   correct permissions?
3. What is the difference between a runtime-only and a `--permanent`
   `firewall-cmd` change, and what command makes a permanent change
   take effect immediately without a reboot?
4. When would a firewalld rich rule be preferable to creating a new
   zone, and vice versa?

## Hands-On Lab

**Objective:** Provision a scoped administrative account, harden SSH
access to it, configure a static network profile, and restrict a
service to a specific source network with firewalld.

**Prerequisites**

- A RHEL 10 host or VM with root or sudo access and at least two
  network interfaces (a second virtual NIC is sufficient in a lab
  hypervisor).
- A separate SSH client machine able to reach the lab host.

**Steps**

1. Create a scoped operator account and grant it delegated sudo for a
   single service:

   ```bash
   sudo groupadd webteam
   sudo useradd -m -G webteam -s /bin/bash operator1
   sudo passwd operator1

   sudo tee /etc/sudoers.d/webteam-httpd <<'EOF'
   %webteam ALL=(root) /usr/bin/systemctl restart httpd, /usr/bin/systemctl status httpd
   EOF
   sudo visudo -cf /etc/sudoers.d/webteam-httpd
   ```

   **Expected result:** `visudo -cf` reports the file's syntax is
   correct.

2. Generate a key pair on the client and install it for the new
   account:

   ```bash
   ssh-keygen -t ed25519 -f ~/.ssh/lab_operator1 -N ""
   ssh-copy-id -i ~/.ssh/lab_operator1.pub operator1@<lab-host-ip>
   ```

3. Confirm key-based login works, then confirm the scoped sudo grant:

   ```bash
   ssh -i ~/.ssh/lab_operator1 operator1@<lab-host-ip> \
     "sudo systemctl status httpd; sudo -l"
   ```

   **Expected result:** the account authenticates without a password
   prompt, and `sudo -l` lists only the two permitted `systemctl`
   commands.

4. Configure a static IP on the lab host's second interface:

   ```bash
   sudo nmcli connection add type ethernet ifname ens224 con-name lab-static \
     ipv4.method manual ipv4.addresses 192.0.2.50/24 ipv4.gateway 192.0.2.1
   sudo nmcli connection up lab-static
   nmcli device status
   ```

   **Expected result:** `ens224` shows `connected` with the
   `lab-static` profile active.

5. Restrict SSH access on that interface's zone to your client's
   subnet only, then verify the running policy:

   ```bash
   sudo firewall-cmd --zone=public --add-rich-rule='rule family="ipv4" source address="192.0.2.0/24" service name="ssh" accept' --permanent
   sudo firewall-cmd --zone=public --remove-service=ssh --permanent
   sudo firewall-cmd --reload
   sudo firewall-cmd --list-all
   ```

   **Expected result:** the `ssh` service no longer appears in the
   plain `services:` list, but the rich rule scoping SSH to
   `192.0.2.0/24` is present.

6. **Negative test:** confirm the account lockout policy actually
   locks after repeated bad passwords:

   ```bash
   for i in 1 2 3 4 5; do
     sshpass -p "wrong-password" ssh -o PreferredAuthentications=password \
       -o PubkeyAuthentication=no operator1@<lab-host-ip> exit 2>/dev/null
   done
   sudo faillock --user operator1
   ```

   **Expected result:** `faillock` shows multiple recorded failures
   and, once the configured threshold is exceeded, the account is
   temporarily locked (if `sshpass` is unavailable, this step can be
   performed manually with repeated interactive password attempts).

7. Reset the lockout and confirm normal access is restored:

   ```bash
   sudo faillock --user operator1 --reset
   ```

8. **Cleanup:**

   ```bash
   sudo firewall-cmd --zone=public --remove-rich-rule='rule family="ipv4" source address="192.0.2.0/24" service name="ssh" accept' --permanent
   sudo firewall-cmd --zone=public --add-service=ssh --permanent
   sudo firewall-cmd --reload
   sudo nmcli connection delete lab-static
   sudo userdel -r operator1
   sudo groupdel webteam
   sudo rm -f /etc/sudoers.d/webteam-httpd
   rm -f ~/.ssh/lab_operator1 ~/.ssh/lab_operator1.pub
   ```

## Summary and Completion Checklist

Identity (the shadow password suite), privilege delegation (`sudo`
backed by PAM), remote access (`sshd` with key-based authentication),
host networking (NetworkManager connection profiles), and packet
filtering (`firewalld` zones and rich rules) form the layered access
path to every RHEL 10 host. Each layer has independent tooling and
independent failure modes, and a disciplined administrator diagnoses
from the bottom up — network reachability, then firewall policy, then
`sshd` configuration, then account and privilege state — rather than
guessing across layers.

- [ ] Can create and manage local users and groups, including password
      aging and account lockout.
- [ ] Can delegate scoped privilege with `sudo` and `sudoers.d`, backed
      by an understanding of PAM's role.
- [ ] Can configure and harden `sshd` for key-based authentication.
- [ ] Can configure static and bonded network profiles with `nmcli`.
- [ ] Can manage `firewalld` zones, services, ports, and rich rules.
- [ ] Completed the hands-on lab, including the negative test and
      cleanup.
