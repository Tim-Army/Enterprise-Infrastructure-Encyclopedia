# Volume XXXVI Glossary

Definitions for terms used in **Volume XXXVI — Windows Server 2025 and
Active Directory**, alphabetized. See also the [volume index](INDEX.md) and
the [master glossary](../../GLOSSARY.md) for cross-volume terminology.

**AD CS (Active Directory Certificate Services)** — Windows public-key
infrastructure; an enterprise CA issues certificates from templates for
authentication, encryption, and signing. Misconfigured templates are a known
privilege-escalation path. Used in Chapter 10.

**AGDLP** — Accounts into Global groups, Global groups into Domain Local
groups, Permissions assigned to the Domain Local group. The canonical
Active Directory group-nesting strategy that separates role membership from
resource permissioning. Used in Chapters 04 and 07.

**Azure Arc** — A service that projects on-premises or other-cloud servers
into Azure as managed resources, unlocking Azure Policy, Monitor, Defender
for Cloud, Update Manager, and hotpatch enrollment. Used in Chapter 11.

**Azure File Sync** — Turns a Windows file server into a cache of an Azure
file share, keeping hot data local and tiering cold data to the cloud. Used
in Chapter 11.

**Cluster Shared Volume (CSV)** — A volume that all failover-cluster nodes
can access simultaneously, enabling clustered Hyper-V and Scale-Out File
Server. Used in Chapter 09.

**Credential Guard** — A virtualization-based-security feature that isolates
secrets (NTLM hashes, Kerberos tickets) from the OS so credential-theft tools
cannot scrape them. Used in Chapter 10.

**DSC (Desired State Configuration)** — PowerShell's declarative
configuration engine; a configuration document names resources and their
desired state, which the Local Configuration Manager enforces and corrects.
Used in Chapter 02.

**DFS (Distributed File System)** — DFS Namespaces present many shares as one
logical path; DFS Replication (DFSR) synchronizes folder copies with remote
differential compression. Used in Chapter 07.

**Entra Connect** — The tool that synchronizes on-premises Active Directory
identities to Microsoft Entra ID, with password hash sync, pass-through
authentication, or federation sign-in options. Used in Chapter 11.

**FSMO (Flexible Single Master Operations)** — The five roles held by a
single DC each: Schema Master and Domain Naming Master (forest-wide), and
RID Master, PDC Emulator, and Infrastructure Master (per-domain). Used in
Chapter 03.

**Global catalog** — A partial, read-only, forest-wide copy of every object,
enabling forest-wide logon and search without contacting every domain. Used
in Chapter 03.

**gMSA (group managed service account)** — A service account whose long,
random password Active Directory generates and rotates automatically;
authorized hosts retrieve it, so no human knows it. Used in Chapter 10.

**Hotpatching** — Applying most monthly security updates to running
processes without a reboot; supported on Azure Edition and enrolled on
premises through Azure Arc. Used in Chapters 01 and 11.

**Hyper-V Replica** — Asynchronous VM replication to a second host or site
for disaster recovery, with configurable recovery-point intervals and test
failover. Used in Chapter 09.

**JEA (Just Enough Administration)** — A constrained PowerShell remoting
endpoint that exposes only named cmdlets and parameters under a temporary
virtual account, for least-privilege delegated administration. Used in
Chapter 02.

**LSDOU** — The Group Policy processing order: Local, then Site, then Domain,
then each Organizational Unit from the top down; later wins unless a higher
link is Enforced. Used in Chapter 05.

**Windows LAPS** — Local Administrator Password Solution; randomizes each
machine's local admin password on a schedule and stores it encrypted in
Active Directory or Microsoft Entra ID. Used in Chapter 10.

**OSE (Operating System Environment)** — A licensing unit roughly equal to
one OS instance (physical or virtual); Standard grants two per licensed
host, Datacenter unlimited. Used in Chapter 01.

**Quorum** — The majority-of-votes mechanism (nodes plus an optional disk,
file-share, or cloud witness) that lets a failover cluster decide it has
authority and avoid split-brain. Used in Chapter 09.

**ReFS (Resilient File System)** — A file system for large volumes with
integrity streams (checksums with automatic repair on resilient storage),
block cloning, and fast VM operations; preferred for Hyper-V and backup
targets. Used in Chapters 07 and 08.

**RODC (read-only domain controller)** — A DC holding a read-only directory
copy that caches only permitted credentials, safe for physically insecure
sites. Used in Chapter 04.

**Server Core** — A Windows Server installation option with no desktop shell,
managed by PowerShell and remote tools; the default for its smaller footprint
and attack surface. Used in Chapter 01.

**Storage Spaces Direct (S2D)** — A Datacenter feature that pools the local
disks of a server cluster into software-defined shared storage with no shared
SAS; the basis of hyperconverged Windows and Azure Stack HCI. Used in
Chapter 07.

**Virtual switch** — A Hyper-V software switch of type external (bound to a
physical NIC), internal (host and VMs), or private (VMs only), connecting
virtual machines to networks. Used in Chapter 08.
