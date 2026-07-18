# Volume IV Glossary

Definitions for terms introduced in **Volume IV — Enterprise Systems
Administration**, alphabetized. See also the [volume index](INDEX.md) for
pointers back to the chapter section each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**Active Directory Domain Services (AD DS)** — Microsoft's enterprise
directory service, organizing identity into forests, domains, and
organizational units, and providing the Kerberos/LDAP authentication and
directory-access backbone both Windows and integrated Linux hosts rely on.
Introduced in Chapter 04.

**Ansible Vault** — Ansible's built-in mechanism for encrypting secrets
(passwords, keys) within playbook source so they can be committed to
version control without exposing plaintext credentials. Introduced in
Chapter 06.

**`ansible-pull`** — A mode of running Ansible in which a target host
pulls a playbook from a Git source and applies it locally, typically on a
recurring timer, converting Ansible's normally push-oriented model into a
pull-style, self-reconciling pattern. Introduced in Chapter 06.

**`auditd`** — The Linux audit daemon, which loads rules watching specific
files, syscalls, or syscall arguments and writes tamper-evident records to
`/var/log/audit/audit.log`, queried with `ausearch` and `aureport`.
Introduced in Chapter 08.

**Bastion / jump host** — A hardened, heavily audited host that brokers
SSH or RDP access into a production network so administrator workstations
never connect directly to production hosts. Introduced in Chapter 01.

**Btrfs** — A copy-on-write Linux filesystem offering native snapshots
and block checksumming, the default filesystem on SUSE Linux Enterprise
Server. Introduced in Chapter 07.

**cgroups v2 (control groups)** — The Linux kernel's unified resource-
grouping hierarchy, with controllers (`cpu`, `memory`, `io`, `pids`,
`cpuset`) that `systemd` maps directly onto its own service/scope/slice
unit hierarchy to enforce resource limits. Introduced in Chapter 05.

**Change management** — The ITIL-aligned process controlling how planned
modifications to production infrastructure are proposed, assessed,
approved, and recorded. Introduced in Chapter 01.

**CIS Benchmark** — A consensus-developed hardening baseline published by
the Center for Internet Security, offered per platform in Level 1
(broadly safe) and Level 2 (stricter, more operational impact) profiles.
Introduced in Chapter 08.

**Compliance as code** — The practice of expressing a security baseline as
an automated scan-remediate-rescan loop (OpenSCAP profiles, configuration
management remediation) rather than a manually walked checklist.
Introduced in Chapter 08.

**Desired State Configuration (DSC)** — Windows PowerShell's declarative
configuration management framework, in which a Local Configuration
Manager (LCM) reconciles a host to a defined configuration, optionally on
a continuous basis (`ApplyAndAutoCorrect`). Introduced in Chapter 06.

**DISA STIG (Security Technical Implementation Guide)** — A hardening
baseline published by the U.S. Defense Information Systems Agency, with
findings categorized by severity (CAT I highest through CAT III lowest),
widely adopted beyond its originating government context. Introduced in
Chapter 08.

**Drift (configuration drift)** — The gap between a host's declared
desired state and its actual running state, caused by manual out-of-band
changes or partial automation failures. Introduced in Chapter 06.

**File Server Resource Manager (FSRM)** — A Windows Server role providing
quota management, file screening, and storage reporting for file shares,
supporting both hard (blocking) and soft (alerting-only) quota limits.
Introduced in Chapter 07.

**Filesystem Hierarchy Standard (FHS)** — The specification defining the
purpose of top-level Linux directories (`/etc`, `/var`, `/usr`, `/opt`,
and others), used operationally to decide which paths warrant dedicated
storage. Introduced in Chapter 02.

**`flock`** — A Linux utility that applies an advisory file lock around a
command, commonly used to prevent a scheduled job (`cron` entry) from
overlapping a still-running previous invocation. Introduced in Chapter 05.

**FSMO roles (Flexible Single Master Operations)** — Five forest- or
domain-scoped Active Directory operations (Schema Master, Domain Naming
Master, RID Master, PDC Emulator, Infrastructure Master) that cannot be
safely multi-mastered and are each held by exactly one domain controller
at a time. Introduced in Chapter 04.

**Golden image** — A validated, versioned base image — typically built
with a tool such as Packer — that new hosts provision from, rather than
each host installing its software stack from scratch. Introduced in
Chapter 06.

**Group Managed Service Account (gMSA)** — An Active Directory-managed
service account whose password Active Directory rotates automatically,
eliminating manually managed service account credentials for
domain-joined services. Introduced in Chapter 03; used in Chapter 04.

**Group Policy Object (GPO)** — A container of configuration settings
applied to computers or users based on domain, site, or organizational
unit membership, following Local-Site-Domain-OU (LSDOU) precedence.
Introduced in Chapter 04.

**Job Object (Windows)** — A Windows kernel object grouping processes so
they share CPU rate limits, memory limits, and a process-count limit, and
can be terminated as a unit; used internally by IIS application pools and
container runtimes. Introduced in Chapter 05.

**`journald`** — `systemd`'s structured logging subsystem, queried with
`journalctl` and optionally forwarded to syslog or a remote collector.
Introduced in Chapter 02.

**Kerberos** — The default network authentication protocol for Active
Directory and most enterprise identity systems, using a Key Distribution
Center to issue time-sensitive tickets so credentials are not repeatedly
sent over the network. Introduced in Chapter 04.

**LDAP (Lightweight Directory Access Protocol)** — The query and
read/write protocol for directory objects, exposed by Active Directory on
port 389 (plain) and 636 (LDAPS/TLS). Introduced in Chapter 04.

**Logical Volume Manager (LVM)** — The Linux subsystem that groups
physical volumes into volume groups and carves resizable logical volumes
from them, allowing storage to be extended without repartitioning the
underlying disk. Introduced in Chapter 02.

**Management plane** — The set of systems (bastion hosts, out-of-band
management, configuration management control plane, identity, monitoring)
administrators use to reach, configure, and observe the workload plane.
Introduced in Chapter 01.

**Multiple-instance policy** — A Windows Task Scheduler setting
(`IgnoreNew`, `Parallel`, `Queue`, `StopExisting`) that governs whether a
new trigger firing while a previous run is still active starts a second
instance. Introduced in Chapter 05.

**NFS (Network File System)** — The standard Linux-native network
filesystem protocol; this volume's baseline assumes stateful NFSv4.2 with
optional Kerberos-backed security (`sec=krb5`, `krb5i`, `krb5p`).
Introduced in Chapter 07.

**NUMA (Non-Uniform Memory Access)** — A multi-socket compute architecture
in which memory access latency depends on which CPU socket's local memory
is being accessed, relevant to sizing and pinning workloads on large
hosts. Introduced in Chapter 05.

**OpenSCAP** — A Linux implementation of the Security Content Automation
Protocol (SCAP), evaluating XCCDF checklist documents and OVAL system
checks against a named profile (such as `cis` or `stig`) to produce
machine-readable and human-readable compliance results. Introduced in
Chapter 08.

**Out-of-band (OOB) management** — Baseboard management controller access
(iDRAC, iLO, or equivalent) that provides console and power control
independent of the host operating system. Introduced in Chapter 01.

**Package version pinning** — Deliberately locking a package at its
current version (`dnf versionlock`, `apt-mark hold`) to prevent an
automatic upgrade, used sparingly and with an expiration plan. Introduced
in Chapter 06.

**Patch ring** — A staged patch-rollout structure (canary/pilot, broad,
remaining) separated by a minimum soak period, used to catch a bad update
before it reaches the full fleet. Introduced in Chapter 06.

**Platform-team operating model** — An administration structure in which
the central team exposes self-service provisioning and owns the
underlying platform, while consumers request compute rather than filing
tickets against a human queue. Introduced in Chapter 01.

**POSIX ACL** — A filesystem access control list extending the classic
Linux owner/group/other permission model to grant additional users or
groups fine-grained access without changing primary ownership. Introduced
in Chapter 02.

**PowerShell Remoting (WinRM)** — The Windows Remote Management
transport underlying `Invoke-Command`, `New-PSSession`, and Windows Admin
Center, running over HTTP (5985) or a hardened HTTPS listener (5986).
Introduced in Chapter 03.

**ReFS (Resilient File System)** — A Windows filesystem providing block
checksumming and metadata integrity, commonly paired with Storage Spaces
mirror or parity resiliency for large data volumes; not supported as a
boot volume. Introduced in Chapter 07.

**Resiliency type (Storage Spaces)** — The redundancy model — `Simple`
(no redundancy), `Mirror`, or `Parity` — declared when creating a Storage
Spaces virtual disk, conceptually parallel to RAID levels. Introduced in
Chapter 07.

**`sar` / sysstat** — The Linux system activity reporter and its
supporting package, which samples and retains system activity data (via a
`systemd` timer) so performance issues can be diagnosed retrospectively,
not only live. Introduced in Chapter 09.

**SCHED_FIFO / SCHED_RR** — Linux real-time scheduling classes that
preempt normal (CFS/EEVDF-scheduled) processes, appropriate only for
trusted, genuinely latency-critical workloads. Introduced in Chapter 05.

**SELinux / AppArmor** — Mandatory access control (MAC) frameworks that
confine even a compromised root process to a policy-defined set of
allowed actions, used respectively by RHEL-family and Debian-family/SUSE
distributions. Introduced in Chapter 02.

**Server Core** — A minimal Windows Server installation option omitting
the Windows Explorer shell and most GUI management consoles, reducing
patch and reboot footprint; the recommended enterprise default over
Desktop Experience. Introduced in Chapter 03.

**Service Control Manager (SCM)** — The Windows subsystem that manages
services: startup type, logon identity, dependency list, and recovery
policy — the direct Windows analog to a `systemd` service unit. Introduced
in Chapter 03.

**SMB (Server Message Block)** — The standard Windows-native network
filesystem protocol; this volume's baseline assumes SMB 3.1.1 with
mandatory signing and optional end-to-end encryption. Introduced in
Chapter 07.

**SSSD (System Security Services Daemon)** — The Linux service that
performs Kerberos/LDAP lookups against Active Directory (or another
identity provider) and exposes the results to NSS/PAM, typically
configured through `realmd`. Introduced in Chapter 04.

**Storage pool (Storage Spaces)** — A Windows abstraction grouping
physical disks so that virtual disks can be carved from the pooled
capacity with a declared resiliency type — the Windows Storage Spaces
analog to an LVM volume group. Introduced in Chapter 07.

**`systemd` slice** — A `systemd` unit type representing a node in the
cgroup hierarchy that groups related services for collective resource
accounting and limits, such as a `batch.slice` grouping background jobs.
Introduced in Chapter 05.

**Tiered administration model (Tier 0/1/2)** — Microsoft's model
separating credentials for domain-controller/PKI administration (Tier 0),
server administration (Tier 1), and workstation administration (Tier 2)
so that compromising a lower tier's credential cannot escalate to domain
compromise. Introduced in Chapter 04.

**USE method** — A troubleshooting lens (Utilization, Saturation, Errors)
applied per resource — CPU, memory, disk, network — to identify a
performance bottleneck from evidence rather than guesswork. Introduced in
Chapter 09.

**Windows Admin Center (WAC)** — A browser-based, gateway-deployed
management surface consolidating certificate, storage, networking,
Hyper-V, and update management for many servers, connecting to each
managed node over WinRM. Introduced in Chapter 03.

**Windows Event Forwarding (WEF)** — A native Windows mechanism in which
a designated collector pulls (or sources push) event log data over WinRM
per a defined subscription, without installing a third-party shipping
agent. Introduced in Chapter 09.

**WSUS (Windows Server Update Services)** — A Windows Server role that
downloads updates once from Microsoft and lets administrators approve
them into named computer groups (rings) before broader deployment.
Introduced in Chapter 06.

**XCCDF / OVAL** — The two SCAP component standards OpenSCAP evaluates:
XCCDF defines checklist structure and remediation, and OVAL defines the
actual system checks a rule performs. Introduced in Chapter 08.

**XFS** — A Linux filesystem optimized for large-file and parallel I/O
throughput, the default filesystem on Red Hat Enterprise Linux; supports
online growth but cannot be shrunk. Introduced in Chapter 07.
