# Volume XXI Glossary

Definitions for terms introduced in **Volume XXI — Ubuntu Server and
Cloud 26.04 LTS**, alphabetized. See also the [volume index](INDEX.md)
for pointers back to the chapter section each term is drawn from, and
the [master glossary](../../GLOSSARY.md) for cross-volume terminology.

**ACL (Access Control List)** — A POSIX extension to standard Unix
permissions allowing per-user and per-group grants beyond owner/group/
other, set and read with `setfacl`/`getfacl`. Introduced in Chapter 06.

**AppArmor** — Ubuntu's default mandatory access control (MAC)
framework, confining applications through plain-text, path-based
profiles rather than SELinux's label-based model. Introduced in
Chapter 06.

**Autoinstall** — Canonical's unattended installation mechanism for
Ubuntu Server, expressed as a cloud-init `autoinstall:` user-data block
consumed by the Subiquity installer. Introduced in Chapter 01.

**Bundle (Juju)** — A YAML document describing a complete set of
applications and their relations, deployed together in a single
operation. Introduced in Chapter 09.

**Charm** — Reusable, versioned Juju operator code that packages an
application's installation and full lifecycle operations (upgrade,
backup, scaling) as callable actions. Introduced in Chapter 09.

**chrony** — The default NTP client/server implementation on Ubuntu
Server, replacing the legacy `ntpd`, with faster convergence and better
handling of intermittent connectivity. Introduced in Chapter 07.

**Cloud-init** — The cross-distribution tool that initializes a Linux
instance's identity, network, storage, and software configuration on
first boot, driven by datasource-supplied user-data, meta-data, and
vendor-data. Introduced in Chapter 01 and treated in depth in
Chapter 09.

**Commissioning (MAAS)** — The MAAS lifecycle stage in which a newly
enlisted physical machine is booted into an ephemeral environment to
inventory its hardware before it can be allocated and deployed.
Introduced in Chapter 09.

**Confinement (Snap)** — The isolation level (`strict`, `classic`, or
`devmode`) under which a Snap package's AppArmor/seccomp sandboxing
operates. Introduced in Chapter 02.

**Curtin** — The installation engine Subiquity uses to partition disks
and lay down the target filesystem during both interactive and
autoinstall installations. Introduced in Chapter 01.

**deb822** — The current default APT source-list format
(`.sources` files), supporting multiple suites and components per
stanza, distinct from the legacy one-line-per-entry `sources.list`
syntax. Introduced in Chapter 01.

**dpkg** — The low-level Debian package tool that installs, removes,
and queries individual `.deb` files against the local package database,
with no dependency resolution or repository awareness of its own.
Introduced in Chapter 02.

**ESM (Expanded Security Maintenance)** — An Ubuntu Pro entitlement
extending security patching beyond the standard LTS window, split into
ESM-Infra (`main`/`restricted`) and ESM-Apps (`universe`/
`multiverse`). Introduced in Chapter 01.

**GRUB2** — The bootloader Ubuntu Server uses by default, generating
`/boot/grub/grub.cfg` from `/etc/default/grub` and presenting the
kernel/initramfs selection at boot. Introduced in Chapter 03.

**Incus** — The community-governed fork of LXD created after a 2023
governance dispute; LXD itself remains actively developed and supported
by Canonical. Introduced in Chapter 08.

**initramfs** — A minimal, kernel-loaded root filesystem, built by
`initramfs-tools`, containing just enough drivers and tooling to locate
and mount the real root filesystem at boot. Introduced in Chapter 03.

**Juju** — Canonical's application modeling and deployment tool,
representing applications, their relations, and their lifecycle
operations as declarative objects rather than imperative scripts.
Introduced in Chapter 09.

**Kea** — ISC's actively maintained DHCP server, using JSON
configuration and a REST control-agent API, and Ubuntu's supported
replacement for the deprecated `isc-dhcp-server`. Introduced in
Chapter 07.

**Landscape** — Canonical's systems management platform for Ubuntu
fleets, providing inventory, patch management, and compliance reporting
through a lightweight `landscape-client` agent on each managed host.
Introduced in Chapter 01.

**LTS (Long Term Support)** — An Ubuntu release cadence (every two
years) receiving five years of free standard maintenance, extendable
to ten (or twelve, with the Legacy add-on) years through Ubuntu Pro.
Introduced in Chapter 01.

**LUKS (Linux Unified Key Setup)** — The standard Linux full-disk and
per-volume encryption format, managed through `cryptsetup`, optionally
paired with TPM2-bound automatic unlock. Introduced in Chapter 06.

**LVM (Logical Volume Management)** — A storage abstraction layer
(Physical Volume, Volume Group, Logical Volume) inserted between raw
partitions and filesystems, enabling online growth and snapshots.
Introduced in Chapter 05.

**LXD** — Canonical's container and virtual-machine manager, running
full-OS system containers (or KVM-backed VMs) through a unified
`lxc`/`lxd` command surface, distinct from Docker's single-process
application containers. Introduced in Chapter 08.

**MAAS (Metal as a Service)** — Canonical's bare-metal provisioning
platform, turning physical servers into API-provisionable resources
through a region-controller/rack-controller architecture. Introduced
in Chapter 09.

**Netplan** — Ubuntu's declarative network configuration abstraction,
rendering administrator-authored YAML into either a `systemd-networkd`
or `NetworkManager` backend configuration. Introduced in Chapter 04.

**`netplan try`** — A Netplan apply mode that activates a new network
configuration with an automatic rollback timer if the administrator
does not confirm the change, protecting against a remote session losing
connectivity. Introduced in Chapter 04.

**nftables** — The kernel packet-filtering framework underlying
Ubuntu's firewall stack, which `ufw` generates rules for as its
approachable front end. Introduced in Chapter 04.

**PAM (Pluggable Authentication Modules)** — The modular framework
mediating every authentication event on Ubuntu — login, `sudo`, `su`,
SSH password auth — through a configurable module stack in
`/etc/pam.d/`. Introduced in Chapter 04.

**Persistent journal** — systemd-journald log storage written to
`/var/log/journal` (surviving reboots), activated automatically once
that directory exists; otherwise the journal is volatile
(`/run/log/journal`) and cleared on reboot. Introduced in Chapter 03.

**PPA (Personal Package Archive)** — A third-party, non-Canonical-
supported APT repository hosted on Launchpad, added with
`add-apt-repository`. Introduced in Chapter 01.

**Relation (Juju)** — A declared integration between two Juju charms
that the charms themselves implement, automatically exchanging
configuration and credentials without manual wiring. Introduced in
Chapter 09.

**Security Context Constraints (SCC)** — OpenShift's admission-control
mechanism restricting what a pod's containers may do, whose default
"restricted" policy assigns containers an arbitrary non-root UID unless
explicitly granted otherwise. Introduced in Chapter 08.

**Snap** — Canonical's containerized, transactional package format,
bundling an application with its runtime into a read-only squashfs
image with automatic background updates and atomic rollback.
Introduced in Chapter 02.

**Subiquity** — The Python/Curtin-based installer Ubuntu Server uses
for both interactive and autoinstall-driven installation, replacing
the older Debian-installer-derived text installer. Introduced in
Chapter 01.

**systemd-cryptenroll** — The systemd tool that binds a LUKS volume's
unlock to a TPM2 module (or other hardware token), enabling automatic
unlock gated on verified boot-chain integrity. Introduced in
Chapter 06.

**systemd-resolved** — The client-side DNS resolution stub present on
every Ubuntu host by default, managing `/etc/resolv.conf` and
per-interface DNS assignment, distinct from running an authoritative
DNS server. Introduced in Chapter 07.

**systemd timer** — A `.timer` unit that activates a matching
`.service` unit on a schedule, supporting `Persistent=true` catch-up
after downtime and full systemd logging/dependency integration that
cron lacks natively. Introduced in Chapter 03.

**Ubuntu Pro** — Canonical's subscription layer atop the free Ubuntu
base, unlocking ESM, Livepatch, FIPS-validated crypto, and the Ubuntu
Security Guide. Introduced in Chapter 01.

**Ubuntu Security Guide (USG)** — Canonical's automated CIS/DISA-STIG
hardening and compliance tool, delivered through Ubuntu Pro, supporting
separate non-destructive `audit` and configuration-applying `fix`
operations. Introduced in Chapter 06.

**ufw (Uncomplicated Firewall)** — Ubuntu's policy-oriented front end
to `nftables`, translating simple rules (`ufw allow 22/tcp`) and named
application profiles into the underlying kernel ruleset. Introduced in
Chapter 04.

**Unattended-upgrades** — The APT-integrated package that applies
security updates automatically on a defined schedule, configurable by
origin pattern. Introduced in Chapter 02.

**User-data / meta-data / vendor-data** — The three cloud-init
configuration inputs: administrator-authored configuration
(user-data), platform-supplied instance identity (meta-data), and
platform- or image-builder-supplied configuration layered beneath
user-data (vendor-data). Introduced in Chapter 09.

**Zram** — A compressed block device in RAM used as swap, the default
swap mechanism on current Ubuntu Server cloud images, trading CPU for
faster effective swap I/O than disk-backed swap. Introduced in
Chapter 05.

**ZFS** — A combined filesystem and volume manager natively supported
on Ubuntu (including as an installer-selectable root filesystem),
providing checksummed data integrity, snapshots, and pool management
without a separate LVM layer. Introduced in Chapter 05.
