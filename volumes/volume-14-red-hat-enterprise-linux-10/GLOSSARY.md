# Volume XIV Glossary

Definitions for terms introduced in **Volume XIV — Red Hat Enterprise
Linux 10**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**ACL (Access Control List)** — A POSIX extension to standard Unix
permissions allowing multiple named users or groups to have
independent read/write/execute grants on a single file or directory,
managed with `setfacl` and `getfacl`. Introduced in Chapter 06.

**Anaconda** — RHEL's graphical and text-mode system installer, which
walks through language, storage, network, and software selection and
writes the result directly to disk. Introduced in Chapter 01.

**Ansible Automation Platform (AAP)** — Red Hat's governed control
plane for Ansible automation, adding credential management,
role-based access control, job scheduling, an audit trail, and
containerized execution environments on top of core Ansible. Introduced
in Chapter 09.

**Ansible Vault** — An Ansible feature for encrypting sensitive
variable data (passwords, keys) within a playbook or inventory so
secrets are never stored in plain text in version control. Introduced
in Chapter 09.

**AppStream** — The RHEL repository holding application-layer
packages and module streams, layered on top of BaseOS. Introduced in
Chapter 01.

**authselect** — The RHEL utility that manages the active
authentication profile (PAM and `nsswitch.conf` configuration),
including enabling features such as `pam_faillock`. Introduced in
Chapter 04.

**autofs** — A service that mounts a filesystem (commonly NFS) on
demand when a path is accessed and unmounts it after a period of
inactivity, avoiding the reliability issues of a hard-mounted network
share. Introduced in Chapter 05.

**BaseOS** — The RHEL repository containing the core, always-enabled
operating system packages: kernel, glibc, systemd, and core utilities.
Introduced in Chapter 01.

**BIND (named)** — The DNS server daemon used to run a caching
recursive resolver or an authoritative zone server on RHEL. Introduced
in Chapter 07.

**Boot Loader Specification (BLS)** — The boot-entry format RHEL 10
uses under `/boot/loader/entries/`, generated from `/etc/default/grub`
rather than hand-edited directly. Introduced in Chapter 03.

**cgroup (control group)** — A kernel mechanism that groups a process
tree for resource accounting and limiting; every systemd unit runs in
its own cgroup, enabling per-service CPU, memory, and I/O controls.
Introduced in Chapter 03.

**chrony (chronyd)** — RHEL's default NTP client/server
implementation, preferred over legacy `ntpd` for faster convergence
after network interruption. Introduced in Chapter 07.

**Cockpit** — A browser-based, socket-activated system administration
console authenticating through PAM and calling the same underlying
tools (`systemd`, NetworkManager, `storaged`, Podman) as the command
line. Introduced in Chapter 01.

**Containerfile** — A declarative build recipe (Docker's `Dockerfile`
format, used identically by Podman) describing how to assemble a
container image in layers. Introduced in Chapter 08.

**CRC (CodeReady Containers)** — A tool that runs a minimal,
single-node OpenShift cluster inside a local VM for development and
learning. Introduced in Chapter 08.

**dnf (DNF5)** — RHEL 10's package manager, built on `libdnf5`, that
resolves dependencies and records reversible transactions in `dnf
history` on top of the underlying RPM database. Introduced in Chapter
02.

**dracut** — The tool that builds the initramfs (initial RAM
filesystem) containing the drivers and utilities needed to locate and
mount the real root filesystem during boot. Introduced in Chapter 03.

**faillock** — The PAM module and companion command (`pam_faillock`)
that locks a local account after a configured number of consecutive
failed authentication attempts. Introduced in Chapter 04.

**firewalld** — RHEL's dynamic firewall management service, using
`nftables` as its packet-filtering backend and organizing rules into
named zones. Introduced in Chapter 04.

**GRUB2** — The GRand Unified Bootloader used by RHEL 10, reading
generated configuration from `/boot/grub2/grub.cfg` or the UEFI
equivalent. Introduced in Chapter 03.

**Handler (Ansible)** — A task that runs only when notified by another
task that reported a change, the standard Ansible pattern for
conditionally restarting a service after its configuration changes.
Introduced in Chapter 09.

**Idempotency** — The property, enforced structurally by Ansible
modules and by design in well-written Bash scripts, that running an
operation multiple times produces the same end state as running it
once. Introduced in Chapter 02 and formalized for automation in
Chapter 09.

**Image Builder (osbuild-composer)** — RHEL's blueprint-driven,
declarative image-building tool that produces a ready-to-boot image
(QCOW2, AMI, VMDK, or OSTree/`bootc` container image) without running
an interactive installer. Introduced in Chapter 01.

**journald (systemd-journald)** — The systemd component collecting
structured, indexed log data from the kernel, boot, and every managed
service, queried with `journalctl`. Introduced in Chapter 03.

**Kickstart** — A declarative file (`ks.cfg`) that Anaconda consumes
to perform an unattended, repeatable installation, the backbone of
fleet-scale RHEL provisioning. Introduced in Chapter 01.

**LUKS (Linux Unified Key Setup)** — The standard Linux full-disk/
full-partition encryption format, protecting data at rest beneath the
LVM and filesystem layers. Introduced in Chapter 06.

**LVM (Logical Volume Management)** — A storage abstraction layering
physical volumes, volume groups, and logical volumes between raw
partitions and a filesystem, enabling live resizing and snapshots.
Introduced in Chapter 05.

**MariaDB** — A MySQL-compatible relational database server, offered
as an AppStream module stream on RHEL 10. Introduced in Chapter 07.

**Module stream** — A selectable major-version lifecycle of an
AppStream package (for example, `postgresql:16`), letting an
administrator pin a specific application version independent of the
base OS release cadence. Introduced in Chapter 01.

**NetworkManager** — RHEL's network configuration service, managing
connection profiles for every interface and exposed through `nmcli`,
`nmtui`, and Cockpit. Introduced in Chapter 04.

**NFS (Network File System)** — A protocol for sharing a server-side
directory with Linux/Unix clients over the network, authorized
primarily by client network and UID/GID mapping. Introduced in Chapter
05.

**OpenSCAP (oscap)** — A tool that evaluates a system against a
machine-readable SCAP security profile (CIS, STIG) and can generate
automated remediation. Introduced in Chapter 06.

**OpenShift Route** — An OpenShift resource that exposes a Kubernetes
Service externally with integrated TLS handling, built on top of
Kubernetes Ingress concepts. Introduced in Chapter 08.

**Operator (Kubernetes/OpenShift)** — A packaged, Kubernetes-native
application that extends the Kubernetes API with custom resources
encoding its own day-2 operational knowledge (upgrades, backup,
scaling). Introduced in Chapter 08.

**PAM (Pluggable Authentication Modules)** — The policy engine
underlying every RHEL authentication path (login, `sudo`, `sshd`),
letting authentication and account policy be changed once, centrally,
rather than per application. Introduced in Chapter 04.

**Podman** — RHEL's default, daemonless, rootless-capable container
engine, executing each container as a direct process tree rather than
a child of a central daemon. Introduced in Chapter 08.

**Quadlet** — RHEL 10's supported mechanism for declaring Podman
containers, pods, networks, and volumes as systemd units, generated
automatically from `.container`/`.pod`/`.network`/`.volume` files.
Introduced in Chapter 08.

**Red Hat Insights** — A telemetry and analysis service fed by
`insights-client` that provides fleet-wide visibility into known CVEs,
misconfigurations, and compliance drift for registered systems.
Introduced in Chapter 01.

**Red Hat Subscription Management (RHSM)** — Red Hat's entitlement
system, exposed through `subscription-manager`, that authorizes a
system to pull content from Red Hat's CDN or a Satellite/Capsule
server. Introduced in Chapter 01.

**RHEL System Roles** — A collection of pre-built, Red Hat–supported
Ansible roles covering common administrative domains (`timesync`,
`network`, `storage`, `selinux`, `firewall`, and others). Introduced in
Chapter 09.

**Rootless container** — A container run as an unprivileged host user,
using Linux user namespaces to remap container-internal UID 0 to an
unprivileged host UID, narrowing the impact of a container escape.
Introduced in Chapter 08.

**SELinux context** — The `user:role:type:level` label carried by
every process and file under SELinux, with the **type** field driving
almost all targeted-policy decisions. Introduced in Chapter 06.

**SELinux (Security-Enhanced Linux)** — A kernel-enforced mandatory
access control (MAC) system that confines processes by type
independent of the Unix user running them and independent of
discretionary file permissions. Introduced in Chapter 06.

**Simple Content Access (SCA)** — The default Red Hat entitlement
model in which any registered system under an account can consume any
entitled content without attaching to an individual subscription pool.
Introduced in Chapter 01.

**Source-to-Image (S2I)** — An OpenShift build mechanism that produces
a container image directly from application source code and a
language-specific builder image, without requiring a hand-authored
Containerfile. Introduced in Chapter 08.

**Stratis** — A local storage management solution
(`stratisd`/`stratis`) that layers thin provisioning and filesystem
creation behind a simplified interface on top of the same underlying
storage concepts as LVM. Introduced in Chapter 05.

**Systemd target** — A systemd unit that groups other units as
dependencies to represent a synchronization point (for example,
`multi-user.target`), the systemd replacement for SysV runlevels.
Introduced in Chapter 03.

**Systemd timer** — A `.timer` unit that triggers a matching
`.service` unit on a calendar or relative schedule, the
Red Hat–recommended mechanism for new scheduled work over plain
`cron`. Introduced in Chapter 03.

**Systemd unit** — Any resource systemd supervises — a service,
socket, target, mount, timer, path, or device — declared in a `.ini`-
style unit file merged across three precedence layers under
`/usr`, `/etc`, and `/run`. Introduced in Chapter 03.

**UBI (Universal Base Image)** — Red Hat's minimal, freely
redistributable container base image family, the recommended starting
point for building custom container images. Introduced in Chapter 08.

**update-crypto-policies** — The RHEL command that sets a single,
system-wide cryptographic policy level (`DEFAULT`, `FUTURE`, `LEGACY`,
`FIPS`) governing every policy-aware application's allowed TLS, SSH,
and Kerberos algorithms. Introduced in Chapter 06.

**VDO (Virtual Data Optimizer)** — A storage layer providing inline
deduplication and compression beneath a filesystem or LVM layer, aimed
at storage-dense, highly redundant workloads. Introduced in Chapter
05.

**XFS** — RHEL's default filesystem: a high-performance, 64-bit
journaling filesystem that can grow live but cannot shrink in place.
Introduced in Chapter 05.
