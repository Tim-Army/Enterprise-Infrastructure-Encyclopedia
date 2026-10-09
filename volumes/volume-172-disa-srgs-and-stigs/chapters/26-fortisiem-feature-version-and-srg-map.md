# Chapter 26: FortiSIEM Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiSIEM release that introduced a given feature.
- Map each FortiSIEM feature to the Central Log Server (CLS) SRG
  requirement, the Network Device Management (NDM) SRG requirement, or the
  General Purpose Operating System (GPOS) SRG requirement it helps satisfy.
- Explain why the host operating system of a FortiSIEM node is assessed
  against the GPOS SRG, and why the map cites only a few of its rules.
- Find the GUI pane, script, or command that configures each feature to
  meet its requirement.
- Use the map to scope an SRG-based assessment of FortiSIEM, which has no
  STIG of its own.
- Record the requirements that FortiSIEM cannot meet exactly, with their
  mitigations.

## Theory and Architecture

FortiSIEM is Fortinet's security information and event management (SIEM)
product. It collects events from network devices, servers, applications,
and cloud services (by syslog, SNMP traps, NetFlow, Windows and Linux
agents, and API event pulling), parses and normalizes them, stores them,
and correlates them in real time with rules that raise incidents. It also
discovers the devices it collects from into its Configuration Management
Database (CMDB), monitors their performance and configuration, scores the
risk of hosts and users, and offers search, reports, dashboards, cases,
notifications, and remediation.

A FortiSIEM deployment is built from a few node types:

- **Supervisor.** The node that runs the GUI, the App Server, the CMDB
  (a PostgreSQL database), and the rule, query, and report masters. A
  small deployment is a single *all-in-one* Supervisor; from 7.3.0,
  several Supervisors form an automated high availability cluster.
- **Workers.** Nodes that add event processing, storage, and query
  capacity to the Supervisor. In ClickHouse deployments, Workers act as
  ClickHouse Keeper, data, and query nodes.
- **Collectors.** Nodes placed near the devices. A Collector receives and
  pulls events, parses them, and uploads them over HTTPS to the Workers;
  it registers with the Supervisor with the `phProvisionCollector`
  command.
- **Agents.** Windows and Linux agents (renamed *Host Collectors* in 7.6.0)
  that send host logs, file integrity data, and osquery results to a
  Collector.
- **Event database.** ClickHouse (recommended), EventDB on local disk or
  NFS, or Elasticsearch, with archive storage on NFS, S3, or a ClickHouse
  cold tier.

The Supervisor, Worker, and Collector images run on **Rocky Linux**:
Rocky Linux 8 through the 7.4 train (updated to 8.8 in 7.0.1, 8.9 in
7.1.1, and 8.10 in 7.2.0), and Rocky Linux 9 from 7.5.0 (9.7 in 7.5.0 and
9.8 in 7.6.0), according to the release notes. Fortinet keeps its own Rocky Linux repositories, so the operating
system can be patched without a FortiSIEM upgrade. For environments that
require FIPS-validated cryptographic modules, FortiSIEM can instead be
installed as an application on Red Hat Enterprise Linux: RHEL 8.10 for
FIPS 140-2 modules (from 7.3.0) and RHEL 9.6 for FIPS 140-3 modules (the
7.6.0 guide).

FortiSIEM has **no DISA STIG** (Chapter 10), so it is assessed against
SRGs, as described in Chapter 03. Chapter 10 assigns it the **Central Log
Server SRG**, the **NDM SRG** for the appliance interface, and the
**operating system STIG or GPOS SRG** for the underlying host. Like
FortiAnalyzer in Chapter 12, FortiSIEM is a central log server first: it
is where the enclave's devices send their audit records, and where those
records are protected, analyzed, and turned into alerts. For every
FortiSIEM feature the chapter gives **which release introduced it**,
**which requirement it relates to**, and **which GUI pane or command
configures it to meet that requirement**.

Most of FortiSIEM is configured in the browser GUI. Its configuration uses
a few ideas again and again:

- **The Admin tab.** *Admin > Setup* holds storage, Collectors,
  credentials, discovery, event pulling, monitoring, and agents; *Admin >
  Settings* holds the system settings (UI, email, cluster, trusted hosts,
  API tokens, image server), the analytics settings (incident
  notification, FortiAI), the event pipeline (dropping, forwarding,
  tagging), the database settings (retention, event integrity), roles, and
  external authentication; *Admin > Health* and *Admin > User Activity*
  show the state of the nodes, Collectors, and users.
- **Users live in the CMDB.** *CMDB > Users* holds the GUI accounts and
  their FortiSIEM attributes: role, local or external authentication, User
  Unlock, Idle Timeout, and Password Reset.
- **Rules raise incidents, policies act on them.** *Resources > Rules*
  holds the correlation rules, *Resources > Reports* the reports
  (including the FortiSIEM Audit reports), and *Admin > Settings >
  General > Automation Policy* decides who is notified and which
  remediation runs
  when an incident triggers.
- **The nodes have a shell.** Installation and a few hardening tasks run on
  the Linux shell of each node: the `configFSM.sh` installer (time zone,
  node type, FIPS, network), `phProvisionCollector`, the
  `config-ssl-cert.sh` certificate script, entries in
  `/opt/phoenix/config/phoenix_config.txt`, and standard Rocky Linux
  commands such as `yum upgrade -y` and `firewall-cmd --reload`.

### Where the version data comes from

Fortinet publishes no Feature Matrix and no New Features Guide for
FortiSIEM. Each release, however, has **Release Notes** whose first page,
"What's New in *release*", lists the new features and key enhancements of
that release, and the **7.6.0 User Guide** repeats the "What's New"
pages of every 7.x release. docs.fortinet.com lists seven
FortiSIEM 7.x trains with 35 releases: **7.0.0 to 7.0.4**, **7.1.0 to
7.1.9**, **7.2.0 to 7.2.7**, **7.3.0 to 7.3.5**, **7.4.0 to 7.4.2**,
**7.5.0 and 7.5.1**, and **7.6.0**. The release notes are the best source:
they are the only document that lists the changes of every release. The
version column was built from the "What's New" page of all 35 releases,
using these rules:

- Each heading under *New Features*, *Features*, *Key Enhancements*, or
  *Enhancements* is one entry, with sub-headings folded into their parent
  (in 7.3.0, whose *Enhancements* section groups its headings under
  sub-sections, each heading of the next level is an entry). The feature
  sections that some pages place at the top level also count: device
  support, external log source integration, rules and reports changes,
  REST API enhancements, the 7.3.1 general enhancement, the 7.1.9 Linux
  Agent update, and the 7.3.0 RHEL 8.10 installation.
- The operating system and component update notice of a release (*System
  Update*, *OS Update*, *Rocky Linux Update*, *PostGreSQL Update*,
  whatever its heading level) is one entry for that release. A notice
  repeated on a later page of the same train (the PostgreSQL 13.14 notice
  on the 7.2.1 page) is counted once.
- Bug fixes, known issues, implementation notes, and upgrade notes are not
  entries. The pages of 7.1.2, 7.1.3, 7.2.1, and 7.2.3 list only fixes, so
  those releases have no entries.
- The "Linux Copy-Fail" and "Linux Dirty-Frag" notices at the top of the
  7.3.0 to 7.5.1 pages announce operating system fixes on the FortiSIEM
  repositories for every release from 6.4.1; they are not features of
  those releases and are not entries.
- The trains were maintained in parallel, so the same feature is sometimes
  listed in more than one train (high availability across data centers in
  7.4.1 and 7.5.0, for example). Each listing is its own entry, and the map
  merges related entries into one row with one version per train.

That gives 169 entries: 23 in 7.0 (18 in 7.0.0, 2 in 7.0.1, and 1
each in 7.0.2, 7.0.3, and 7.0.4), 36 in 7.1 (18 in 7.1.0, 6 each in 7.1.1
and 7.1.4, 2 in 7.1.9, and 1 each in 7.1.5 to 7.1.8), 21 in 7.2 (13 in
7.2.0, 4 in 7.2.2, and 1 each in 7.2.4 to 7.2.7), 28 in 7.3 (21 in 7.3.0,
2 each in 7.3.1 and 7.3.3, and 1 each in 7.3.2, 7.3.4, and 7.3.5), 22 in
7.4 (19 in 7.4.0, 2 in 7.4.1, and 1 in 7.4.2), 29 in 7.5 (17 in 7.5.0 and
12 in 7.5.1), and 10 in 7.6.0. Each entry title was taken from its heading
and shortened where needed.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: event
  collection and parsing, the event pipeline, storage, retention, archive,
  integrity, backups, search, reports, rules, notifications, health,
  users and their attributes, roles, trusted hosts, external
  authentication, the login banner, FIPS mode, certificates, and the
  Rocky Linux platform. Each one is described in the **FortiSIEM 7.0.0
  User Guide** (or, for the platform rows, the **FortiSIEM 7.6.0 Hardening
  Guide**, which applies to 7.x and 6.x), so it existed in the oldest 7.x
  release and is not in the "What's New" lists. One core row has a
  different version entry, explained below.
- **New features** are the 169 entries of the "What's New" pages,
  merged into 90 rows. The categories were assigned for this chapter,
  and the titles were shortened from the release notes text.

| Version entry | Meaning |
| --- | --- |
| `7.0.0 or earlier` | A core feature described in the FortiSIEM 7.0.0 User Guide (or the Hardening Guide), present in the oldest 7.x release |
| `7.3.0 and later` | Introduced in 7.3.0 (listed on its "What's New" page); later releases and trains include it |
| `7.4.1+; 7.5.0+` | Listed in each of those releases; the first release listed in each train is shown |
| `7.6 (release not stated)` | Documented in the 7.6.0 User Guide but not in the 7.0.0 User Guide, and on no "What's New" page (the Lockout Users setting for inactive users) |

Four cautions apply. First, Fortinet revises the guides in place: the
7.0.0 User Guide used here is dated 07/02/2026, so a core row records a
capability of the 7.0 train, but a detail of it may have arrived in a
later patch. Second, the 7.0.0 and 7.0.1 release notes say that those
releases cannot be installed with the FIPS option, while the Hardening
Guide describes FIPS mode for 7.x and 6.x; check the release notes of your
release before you rely on FIPS mode. Third, many features depend on the
event database (several are ClickHouse only), the license (UEBA, the
Automation Service, GB-per-day licensing), the deployment type
(Enterprise or Service Provider), or an outside service (OpenAI or Azure
OpenAI for FortiAI). Fourth, a row records a FortiSIEM capability, but its
pane was checked against the 7.6.0 User Guide, and 7.5.0 moved the
navigation from the top of the GUI to the side, so a pane may be placed
differently on an older release. The 7.6.0 "What's New" page lists a
*Features* section in its contents but has none, so 7.6.0 has only key
enhancements.

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **CLS** | Central Log Server SRG | V3R5, benchmark date 30 Sep 2026 | The primary SRG: log aggregation, storage, protection, integrity, analysis, alerting, reporting, retention, backup, and off-loading, plus FortiSIEM's own accounts, authentication, sessions, cryptography, and updates |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The appliance's management interface, for the few items the CLS SRG does not cover: the authentication server, the account of last resort, cryptography for remote maintenance, SNMP, NTP authentication, configuration backups, sending logs onward, and unnecessary services |
| **GPOS** | General Purpose Operating System SRG | V3R4, benchmark date 30 Sep 2026 | The Rocky Linux (or RHEL) host of each node, for the operating system rules that FortiSIEM's own documents and settings touch |

The **CLS SRG** is the primary SRG, as it is for FortiAnalyzer in Chapter
12, and it was parsed from the same file. The **NDM SRG** fills the gaps
for the management interface. Neither SRG is about the operating system
under FortiSIEM.

**Why the GPOS SRG.** A FortiSIEM node is a Linux server, not a sealed
firmware appliance: administrators log in to its shell, and the operating
system is patched with `yum`. The October 2026 library has STIGs for Red
Hat Enterprise Linux 9 and 10, Oracle Linux 8 and 9, AlmaLinux OS 9, and
Amazon Linux 2023, but **no STIG for Rocky Linux**, and no RHEL 8 STIG in
the import used for this volume. So the host of a standard FortiSIEM node
is assessed against the **GPOS SRG**, the SRG that the Linux STIGs are
built from. Where FortiSIEM is installed on RHEL 9.6 for FIPS 140-3
modules, the **RHEL 9 STIG** (V2R10) applies to the host instead.

**The map cites only the GPOS rules that FortiSIEM touches:** the host
firewall, SSH, unused interfaces, disk encryption, FIPS mode, operating
system updates and supported versions, and time synchronization. The rest
of the GPOS SRG (or the OS STIG) **still applies in full to every
Supervisor, Worker, and Collector host**: accounts and passwords for the
shell, the logon banner, audit rules, file permissions, kernel settings,
and so on (GPOS `SRG-OS-000480-GPOS-00227`). Assess each host against the
whole SRG, and check every change against Fortinet's support position
first, because FortiSIEM installs and upgrades its own packages and
expects some settings (the RHEL installation guide, for example, turns
SELinux off).

The requirement IDs are the **rule version IDs** from the XCCDF files,
and the severity is the rule's severity (high = CAT I, medium = CAT II,
low = CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiSIEM meets a
  requirement. Correlation rules implement the CLS requirement to notify
  the SA and ISSO when an attack is detected (CLS
  `SRG-APP-000516-AU-000350`), for example.
- **Must be configured to meet a requirement.** The feature is in scope
  of a requirement and has to be set up correctly. Event forwarding must
  use TCP over SSL to off-load records reliably and confidentially (CLS
  `SRG-APP-000516-AU-000340`, CLS `SRG-APP-000439-AU-004310`), for
  example.
- **No direct requirement.** The feature is operational, such as a
  dashboard, a machine learning model, a device integration, or a GUI
  change. It has no requirement of its own, but if it is not needed it
  falls under the CLS requirement to disable non-essential capabilities
  (CLS `SRG-APP-000141-AU-000090`). 54 rows are of this kind.

The mapping is a starting point for an assessment, not a ruling. Confirm
it with your assessor, especially the use of the GPOS SRG for the host and
the split between the CLS and NDM requirements.

### Where the commands come from

FortiSIEM has **no CLI Reference**: it is configured in the GUI, with
scripts and Linux commands on the nodes. The command column was therefore
built from these documents, all for **FortiSIEM 7.6.0**, the newest
release: the **User Guide** (dated 10/09/2026) for every GUI pane and the
documented scripts and `phoenix_config.txt` entries, and the **Hardening
Guide**, **ESX Installation Guide**, **OS Update Procedure**, **Configuring
CA Certificates**, **Disk Encryption for FortiSIEM Virtual Machine**,
**Upgrade Guide**, and **High Availability and Disaster Recovery
Procedures - ClickHouse** for the shell commands, together with the
release notes pages. The check was automatic: each GUI pane had to appear
in the User Guide or the release notes, and each command had to appear in
the documents verbatim up to its first placeholder, with every other
literal word of it also found there. All 24 commands and 83 GUI panes
passed. Read the column this way:

- **GUI:** entries name the FortiSIEM GUI pane; the text in parentheses
  names the fields to set.
- Commands run on the Linux shell of the node, as root. Statements are
  separated by `;` to fit in a table cell; enter each one on its own line.
  Values in `<ANGLE_BRACKETS>` are placeholders for your own values. A
  `name=value` entry in backticks is a line in
  `/opt/phoenix/config/phoenix_config.txt` (or the file named next to it).
- For **"No direct requirement"** rows, the entry shown is where the
  feature is turned off or left unconfigured when it is unused. A dash
  (**—**) means there is nothing to change: the feature is a platform
  change, a GUI change, a content or device update, or a capability that
  does nothing until it is configured.

Some requirements cannot be met exactly with FortiSIEM settings. Record
them on the checklist as open findings with mitigations, or meet them
another way:

- **Local passwords.** FortiSIEM requires 8 to 64 characters with a
  letter, a number, and a special character for local GUI and SSH
  passwords, and has no setting to raise that to 15 characters, require
  upper and lower case, require eight changed characters, or check a list
  of compromised passwords (CLS `SRG-APP-000164-AU-002480`, CLS
  `SRG-APP-000166-AU-002490`, CLS `SRG-APP-000170-AU-002530`, CLS
  `SRG-APP-000845-AU-000320`); the guides do not say how local passwords
  are stored (CLS `SRG-APP-000171-AU-002540`). Authenticate users through
  LDAPS or LDAPTLS, RADIUS, or SAML, whose directory enforces the policy,
  keep the local admin account as the account of last resort (NDM
  `SRG-APP-000148-NDM-000346`), and give local passwords 15 or more
  characters by procedure.
- **Lockout.** A GUI user is locked after **five** consecutive failed
  logons, with no setting for three or for a 15-minute window (CLS
  `SRG-APP-000065-AU-000240`). *User Unlock: Unlock by Administrator* does
  keep the account locked until an administrator releases it (CLS
  `SRG-APP-000345-AU-000400`). Set it for every user, and let the
  directory enforce the three-attempt limit for external users.
- **Login banner.** The *Login Banner* is displayed **after** logon, not
  before (CLS `SRG-APP-000068-AU-000035`, CLS `SRG-APP-000069-AU-000420`),
  and the shell banner is an operating system setting (GPOS
  `SRG-OS-000023-GPOS-00006`). Enable the Login Banner with the DoD
  notice, configure the SSH banner on each host, reach the GUI through a
  gateway that displays the banner before logon, and record the finding.
- **CAC.** The guides document no common access card (PKI) logon to the
  GUI (CLS `SRG-APP-000391-AU-002290`); multifactor authentication comes
  from Duo or from a SAML identity provider (CLS
  `SRG-APP-000149-AU-002280`). Use SAML with an identity provider that
  enforces CAC.
- **FIPS-validated modules.** FIPS mode (`configFSM.sh`) restricts
  FortiSIEM to FIPS-compliant algorithms and runs self-tests, but on Rocky
  Linux the modules themselves are not shown to be validated; Fortinet
  documents FIPS 140-2 validated modules only for installation on RHEL
  8.10 (7.3.0 and later) and FIPS 140-3 validated modules on RHEL 9.6 (CLS
  `SRG-APP-000514-AU-002890`, GPOS `SRG-OS-000478-GPOS-00223`). Where
  validated modules are required, install on RHEL. The RHEL installation
  turns SELinux off, while the RHEL 9 STIG requires it (RHEL-09-431010,
  CAT I, and RHEL-09-431015), so record that as a finding with Fortinet's
  support position.
- **Storage alerts.** The guides document no alert when event storage
  reaches 75 percent (CLS `SRG-APP-000359-AU-000120`). Space-based
  retention moves or purges the oldest events when a tier has less than
  10 percent free, and CMDB disk management prunes incidents when the CMDB
  disk runs low. Watch *Disk Percentage* in *Admin > Health > Cloud
  Health*, size storage and retention together, archive to separate
  storage, and alert on disk use by procedure or with a rule.
- **Time.** The installation guides set NTP on the hypervisor host (for
  ESX, the host's Time Configuration) and document no NTP authentication
  (NDM `SRG-APP-000395-NDM-000347`, CLS `SRG-APP-000920-AU-000410`).
  Synchronize every host to internal, DoD-approved time sources, as the
  operating system requirements expect (GPOS `SRG-OS-000355-GPOS-00143`),
  and check the time on hardware appliances by procedure.
- **SNMP traps.** Incident SNMP trap notification is configured with a
  community string only (NDM `SRG-APP-000395-NDM-000310`). Use email,
  HTTPS, or webhook notifications instead, and leave SNMP traps unset.
- **Internal certificate checks.** Certificate verification for the SSL
  sockets between the backend processes and the App Server is disabled by
  default, and Collectors verify the Supervisor's certificate only when
  `http_client_verify_peer=yes` is set (CLS `SRG-APP-000516-AU-000410`,
  CLS `SRG-APP-000427-AU-000040`). Install CA-signed certificates from a
  DoD-approved CA, run `config-ssl-cert.sh` with verification in both
  directions, and set peer verification before registering Collectors.
- **Event integrity.** EventDB records a checksum for each event file, but
  ClickHouse event integrity is off by default, the guide does not name
  the checksum algorithm, and Elasticsearch has no integrity function (CLS
  `SRG-APP-000080-AU-000010`, CLS `SRG-APP-000610-AU-000050`). Use
  ClickHouse or EventDB, turn ClickHouse event integrity on, validate on a
  schedule, and off-load records to a second system.
- **Software verification.** FortiSIEM checks the hash of Collector and
  agent images (*Hash Check*, which can be disabled), and the upgrade
  guide tells you to compare the hash of each downloaded image with the
  support site; the guides describe no digital signature check for
  Supervisor and Worker upgrades or operating system packages (CLS
  `SRG-APP-000810-AU-000250`, GPOS `SRG-OS-000366-GPOS-00153`). Keep Hash
  Check enabled, verify every image hash before an upgrade, and confirm
  that the host checks package signatures.
- **Inactive accounts.** The *Lockout Users* setting (inactive days) is
  documented in the 7.6.0 User Guide but not in the 7.0.0 guide (CLS
  `SRG-APP-000163-AU-002470`). On releases without it, disable inactive
  accounts in the directory or by a documented account review.
- **FortiAI and the MCP service.** FortiAI sends questions, logs, and
  incident details (anonymized for log and incident analysis) to OpenAI or
  Azure OpenAI, an outside service. Leave it unconfigured unless the
  authorizing official approves it, and treat the agentic features and the
  MCP service the same way (CLS `SRG-APP-000141-AU-000090`).
- **No STIG.** Without a STIG there is no DoD baseline for FortiSIEM
  itself; use this map, the Hardening Guide, and the GPOS SRG for the
  host as the baseline, and record the settings that differ from it.

## Design Considerations

- **Pick the release first, then the features.** If your design depends on
  a feature introduced in a certain release (automated Supervisor HA and
  the RHEL 8.10 FIPS installation in 7.3.0, RADIUS for GUI logons in
  7.4.0, API tokens and Rocky Linux 9 in 7.5.0, secure ClickHouse
  communication in 7.6.0), that sets the minimum release, and it must be a
  vendor-supported release (CLS `SRG-APP-001035-AU-000430`).
- **Choose ClickHouse.** Several requirements depend on ClickHouse-only
  features (event integrity, scheduled and advanced search rules, storage
  regions, the MCP service), and Elasticsearch has no event integrity
  function.
- **Keep the planes apart.** Put the Supervisor and Workers on an isolated,
  firewalled segment; allow GUI logons only from *Trusted Hosts* on the
  management network; open only the ports each node type needs; and keep
  SSH for the administrators who install and upgrade the nodes (NDM
  `SRG-APP-000880-NDM-000290`).
- **Plan storage, retention, and off-loading together.** Size online
  storage for the retention the SA and ISSM set, archive to NFS or S3
  storage that is not on the Supervisor or Workers, back up the CMDB, SVN,
  and event data weekly or more often to another system (CLS
  `SRG-APP-000125-AU-000300`), and forward events in real time over TCP
  over SSL to a second log server or the enclave aggregation server (CLS
  `SRG-APP-000086-AU-000390`).
- **Authenticate users elsewhere.** Use LDAPS or LDAPTLS with *Check
  Certificate*, RADIUS, or SAML with a CAC-enforcing identity provider,
  map directory groups to least-privilege roles, and keep one local admin
  account for emergencies.
- **Treat the hosts as servers.** Each Supervisor, Worker, and Collector
  host has its own operating system assessment against the GPOS SRG (or
  the RHEL 9 STIG), its own patch schedule from the FortiSIEM OS
  repositories, and its own disk encryption decision.
- **Turn off what is not used.** FortiAI and the MCP service, SNMP trap
  notification, the Automation Service, federated search, unused threat
  feeds and integrations, unused agents, and open ports such as SNMP trap
  UDP 162 all need a reason to stay on.

## Implementation and Automation

### The FortiSIEM feature map

The SRG column uses the abbreviations defined in *Where the SRG data
comes from*: **CLS** is the Central Log Server SRG, **NDM** the Network
Device Management SRG, and **GPOS** the General Purpose Operating System
SRG. The requirement titles are listed in the next table. The command
column follows the conventions in *Where the commands come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/26-fortisiem-feature-version-and-srg-map-feature-map.csv) (153 rows).

| Category | Feature | Introduced (FortiSIEM) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Event collection | Event collection by the Supervisor, Workers, and Collectors (syslog, SNMP traps, NetFlow, agents, and API event pulling) | 7.0.0 or earlier | CLS `SRG-APP-000086-AU-000020`; CLS `SRG-APP-000516-AU-000330`; CLS `SRG-APP-000089-AU-000400` | GUI: Admin > Setup > Pull Events (onboard every device and host in the SSP scope, and check it in CMDB > Devices) |
| Core: Event collection | Device discovery and access credentials | 7.0.0 or earlier | CLS `SRG-APP-000086-AU-000020` | GUI: Admin > Setup > Discovery; GUI: Admin > Setup > Credentials |
| Core: Event collection | Collector registration to the Supervisor over HTTPS (phProvisionCollector) | 7.0.0 or earlier | CLS `SRG-APP-000439-AU-004310`; CLS `SRG-APP-000516-AU-000410` | `phProvisionCollector --add <USER> '<PASSWORD>' <SUPERVISOR_FQDN> <ORGANIZATION> <COLLECTOR_NAME>` (register with the Supervisor FQDN; from 7.3.0, omit the password and enter it at the prompt) |
| Core: Event collection | CyberArk password vault for device credentials | 7.0.0 or earlier | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Admin > Setup > Credentials (Password config: CyberArk, when a vault is used) |
| Core: Event parsing | Parsers and event types (normalized attributes; reporting device and source host retained) | 7.0.0 or earlier | CLS `SRG-APP-000089-AU-000400`; CLS `SRG-APP-000516-AU-000330`; CLS `SRG-APP-000080-AU-000010` | GUI: Admin > Device Support > Parsers |
| Core: Event parsing | Event severity of each event type | 7.0.0 or earlier | CLS `SRG-APP-000516-AU-000380` | GUI: Admin > Device Support > Event Types (set the severity the organization assigns to each event type) |
| Core: Event parsing | Event receive time stamps (Event Receive Time recorded by FortiSIEM) | 7.0.0 or earlier | CLS `SRG-APP-000374-AU-000290`; CLS `SRG-APP-000086-AU-000030`; CLS `SRG-APP-000116-AU-000270` | (see the time synchronization row) |
| Core: Event pipeline | Event dropping rules | 7.0.0 or earlier | CLS `SRG-APP-000090-AU-000070`; CLS `SRG-APP-000800-AU-000230` | GUI: Admin > Settings > Event Pipeline > Dropping (only ISSM-approved roles may add or change rules) |
| Core: Event pipeline | Event forwarding to other systems (syslog over UDP, TCP, or TCP over SSL; NetFlow; Kafka) | 7.0.0 or earlier | CLS `SRG-APP-000358-AU-000100`; CLS `SRG-APP-000515-AU-000110`; CLS `SRG-APP-000086-AU-000390`; CLS `SRG-APP-000516-AU-000340`; CLS `SRG-APP-000439-AU-004310`; NDM `SRG-APP-000516-NDM-000350` | GUI: Admin > Settings > Event Pipeline > Forwarding tab (Protocol: TCP over SSL to the enclave aggregation server or second log server) |
| Core: Event pipeline | Multiline syslog and event organization mapping | 7.0.0 or earlier | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Core: Storage | Online event storage (ClickHouse, EventDB on local disk or NFS, Elasticsearch) | 7.0.0 or earlier | CLS `SRG-APP-000359-AU-000120`; CLS `SRG-APP-000118-AU-000100` | GUI: Admin > Setup > Storage (size the storage with the sizing guide for the required retention) |
| Core: Storage | Event retention policies (time-based, plus space-based moves and purges between tiers) | 7.0.0 or earlier | CLS `SRG-APP-000095-AU-000050`; CLS `SRG-APP-000516-AU-000060` | GUI: Admin > Settings > Database > Retention Policy (retention by criticality and event type, as set by the SA and ISSM) |
| Core: Storage | Archive storage (ClickHouse cold tier or S3, EventDB on NFS, copied in real time) | 7.0.0 or earlier | CLS `SRG-APP-000358-AU-000100`; CLS `SRG-APP-000515-AU-000110`; CLS `SRG-APP-000125-AU-000300` | GUI: Admin > Setup > Storage (Archive on NFS or S3 storage separate from the Supervisor and Workers) |
| Core: Storage | Event log integrity for EventDB (checksum per event file, Validate, Validate All, export) | 7.0.0 or earlier | CLS `SRG-APP-000080-AU-000010`; CLS `SRG-APP-000119-AU-000110`; CLS `SRG-APP-000795-AU-000220` | GUI: Admin > Settings > Database > Event Integrity (Validate All on a schedule and export the results) |
| Core: Storage | Backups of the CMDB (twice daily to /data/archive/cmdb), EventDB, SVN, and ClickHouse | 7.0.0 or earlier | CLS `SRG-APP-000125-AU-000300`; NDM `SRG-APP-000516-NDM-000340` | `rsync -a --progress /data/eventdb <BACKUP_DIR>`; `cp -r /svn <BACKUP_DIR>` (copy /data/archive/cmdb/phoenixdb* to another system; for ClickHouse, a daily clickhouse-backup cron job to an SFTP server or S3) |
| Core: Analytics | Real-time and historical search with filters, grouping, and sorting | 7.0.0 or earlier | CLS `SRG-APP-000115-AU-000160`; CLS `SRG-APP-000363-AU-000180`; CLS `SRG-APP-000362-AU-000170`; CLS `SRG-APP-000790-AU-000210`; CLS `SRG-APP-000745-AU-000120`; CLS `SRG-APP-000750-AU-000130`; CLS `SRG-APP-000780-AU-000190` | GUI: Analytics > Search |
| Core: Analytics | Reports, report bundles, and scheduled reports | 7.0.0 or earlier | CLS `SRG-APP-000366-AU-000220`; CLS `SRG-APP-000770-AU-000170`; CLS `SRG-APP-000365-AU-000210`; CLS `SRG-APP-000775-AU-000180` | GUI: Resources > Reports |
| Core: Analytics | FortiSIEM audit reports and audit events (GUI and SSH logons, lockouts, users, roles, rules, reports, CMDB, notifications, remediation, archive and purge) | 7.0.0 or earlier | CLS `SRG-APP-000026-AU-000580`; CLS `SRG-APP-000027-AU-000590`; CLS `SRG-APP-000503-AU-000280`; CLS `SRG-APP-000095-AU-000680`; CLS `SRG-APP-000100-AU-000730` | GUI: Resources > Reports (FortiSIEM Audit folder; schedule the reports for the ISSO) |
| Core: Rules and incidents | Real-time correlation rules and incidents (rule engine, MITRE ATT&CK mapping) | 7.0.0 or earlier | CLS `SRG-APP-000111-AU-000150`; CLS `SRG-APP-000516-AU-000350`; CLS `SRG-APP-000516-AU-000370` | GUI: Resources > Rules (activate the rules for attacks and account actions on the covered devices) |
| Core: Rules and incidents | Watch lists and lookup tables | 7.0.0 or earlier | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Core: Rules and incidents | Incident notification and automation policies (email, SMS, HTTP, SNMP trap, remediation) | 7.0.0 or earlier | CLS `SRG-APP-000516-AU-000350`; CLS `SRG-APP-000360-AU-000130`; CLS `SRG-APP-000292-AU-000420`; CLS `SRG-APP-000291-AU-000200` | GUI: Admin > Settings > General > Automation Policy (notify the SA and ISSO for attack, account, and log-collection incidents) |
| Core: Rules and incidents | Email server settings (TLS, S/MIME) | 7.0.0 or earlier | CLS `SRG-APP-000439-AU-004310` | GUI: Admin > Settings > System > Email (Secure Connection (TLS)) |
| Core: Rules and incidents | Incident SNMP trap notification (community string) | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310`; CLS `SRG-APP-000141-AU-000090` | GUI: Admin > Settings > Analytics > Incident Notification (leave Incident SNMP Traps unset unless required) |
| Core: Rules and incidents | Cases and external ticketing integrations (ServiceNow, Jira, ConnectWise, Salesforce) | 7.0.0 or earlier | CLS `SRG-APP-000516-AU-000360` | GUI: Admin > Settings > General > External Integration |
| Core: Rules and incidents | Remediation scripts and FortiSOAR playbooks | 7.0.0 or earlier | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Resources > Automation > Remediations |
| Core: Health | Log collection status (CMDB Event Status by log delay, Collector Health, Cloud Health) | 7.0.0 or earlier | CLS `SRG-APP-000360-AU-000130` | GUI: Admin > Health > Collector Health; GUI: Admin > Health > Cloud Health |
| Core: Health | Automated CMDB disk space management (prune thresholds, PH_AUDIT_CMDB_DISK_PRUNE events and system rules) | 7.0.0 or earlier | CLS `SRG-APP-000359-AU-000120` | (cmdb_disk_space_low_threshold and cmdb_disk_space_high_threshold in phoenix_config.txt; keep the two FortiSIEM: CMDB Disk space low rules active) |
| Core: Admin accounts | Local GUI users (CMDB > Users, FortiSIEM Role, Local mode) | 7.0.0 or earlier | CLS `SRG-APP-000148-AU-002270`; CLS `SRG-APP-000815-AU-000260` | GUI: CMDB > Users (one account for each person; no shared accounts) |
| Core: Admin accounts | Default GUI admin and SSH accounts (password change forced at installation) | 7.0.0 or earlier | NDM `SRG-APP-000148-NDM-000346`; CLS `SRG-APP-000164-AU-002480` | (keep the GUI admin account as the account of last resort, with a 15-character password) |
| Core: Admin accounts | Local password rules (8 to 64 characters with a letter, a number, and a special character) | 7.0.0 or earlier | CLS `SRG-APP-000164-AU-002480`; CLS `SRG-APP-000166-AU-002490`; CLS `SRG-APP-000170-AU-002530`; CLS `SRG-APP-000845-AU-000320`; CLS `SRG-APP-000171-AU-002540` | GUI: Admin > Settings > General > External Authentication (no setting raises the rules: authenticate users through the directory) |
| Core: Admin accounts | Password Reset (password expiration in days) | 7.0.0 or earlier | CLS `SRG-APP-000174-AU-002570` | GUI: CMDB > Users (FortiSIEM Attributes tab: Password Reset 180 days or less) |
| Core: Admin accounts | User Unlock after five failed logons (Unlock by Administrator or Delay next login) | 7.0.0 or earlier | CLS `SRG-APP-000065-AU-000240`; CLS `SRG-APP-000345-AU-000400` | GUI: CMDB > Users (FortiSIEM Attributes tab: User Unlock: Unlock by Administrator) |
| Core: Admin accounts | Idle Timeout (per user, 15 minutes by default) | 7.0.0 or earlier | CLS `SRG-APP-000295-AU-000190` | GUI: CMDB > Users (FortiSIEM Attributes tab: Idle Timeout set to the organization-defined value) |
| Core: Admin accounts | User Activity (logged-in and locked users; Log Out, Log Out and Lock Out, Unlock) | 7.0.0 or earlier | CLS `SRG-APP-000296-AU-000560`; CLS `SRG-APP-000345-AU-000400` | GUI: Admin > User Activity |
| Core: Admin accounts | Lockout Users (lock users after a number of inactive days) | 7.6 (release not stated) | CLS `SRG-APP-000163-AU-002470` | GUI: Admin > Settings > System > UI (Lockout Users: 35 days) |
| Core: Access control | Roles (GUI access, data visibility, obfuscation, and workflow permissions) | 7.0.0 or earlier | CLS `SRG-APP-000033-AU-001610`; CLS `SRG-APP-000090-AU-000070`; CLS `SRG-APP-000121-AU-000130`; CLS `SRG-APP-000118-AU-000100`; CLS `SRG-APP-000120-AU-000120` | GUI: Admin > Settings > Role > Role Management |
| Core: Access control | AD group to role mapping for externally authenticated users | 7.0.0 or earlier | CLS `SRG-APP-000033-AU-001610` | GUI: Admin > Settings > Role > AD Group Role |
| Core: Access control | Approval workflows (rule activation, report scheduling, deobfuscation, remediation) | 7.0.0 or earlier | CLS `SRG-APP-000800-AU-000230`; CLS `SRG-APP-000090-AU-000070` | GUI: Admin > Settings > Role > Role Management (approver roles for rule and report changes) |
| Core: Access control | Trusted Hosts (GUI logon only from listed addresses) | 7.0.0 or earlier | CLS `SRG-APP-000516-AU-000410`; NDM `SRG-APP-000880-NDM-000290` | GUI: Admin > Settings > System > Trusted Hosts (management network, Collectors, and Host Collectors only) |
| Core: Access control | Organizations (multi-tenancy in Service Provider deployments) | 7.0.0 or earlier | CLS `SRG-APP-000033-AU-001610` | GUI: Admin > Setup > Organizations |
| Core: Remote authentication | External authentication over LDAP, LDAPS, or LDAPTLS (Check Certificate) | 7.0.0 or earlier | CLS `SRG-APP-000148-AU-002270`; NDM `SRG-APP-000516-NDM-000336`; CLS `SRG-APP-000175-AU-002630`; CLS `SRG-APP-000427-AU-000040` | GUI: Admin > Settings > General > External Authentication (Protocol LDAPS or LDAPTLS with Check Certificate) |
| Core: Remote authentication | SAML single sign-on (Azure AD, Okta, FortiAuthenticator) with SAML role mapping | 7.0.0 or earlier | CLS `SRG-APP-000149-AU-002280`; CLS `SRG-APP-000391-AU-002290`; NDM `SRG-APP-000516-NDM-000336` | GUI: Admin > Settings > General > External Authentication; GUI: Admin > Settings > Role > SAML Role (an identity provider that enforces CAC) |
| Core: Remote authentication | Duo two-factor authentication for GUI users | 7.0.0 or earlier | CLS `SRG-APP-000149-AU-002280`; CLS `SRG-APP-000825-AU-000280` | GUI: Admin > Settings > General > External Authentication (Protocol: Duo; Second Factor on each local user) |
| Core: Session | Login Banner (shown after logon, with last logon time and account changes) | 7.0.0 or earlier | CLS `SRG-APP-000068-AU-000035`; CLS `SRG-APP-000069-AU-000420` | GUI: Admin > Settings > System > UI (Login Banner: Enabled, with the Standard Mandatory DoD Notice) |
| Core: Cryptography | FIPS mode (FIPS-compliant algorithms only, with self-tests at startup) | 7.0.0 or earlier | CLS `SRG-APP-000514-AU-002890`; CLS `SRG-APP-000179-AU-002670`; CLS `SRG-APP-000610-AU-000050`; NDM `SRG-APP-000412-NDM-000331`; GPOS `SRG-OS-000478-GPOS-00223` | `configFSM.sh` (FIPS option: install_with_fips at installation, or enable_fips later) |
| Core: Cryptography | TLS 1.2 and TLS 1.3 only, with secure cipher suites, for external communication | 7.0.0 or earlier | CLS `SRG-APP-000439-AU-004310`; NDM `SRG-APP-000412-NDM-000331` | — |
| Core: Cryptography | CA-signed certificates for the GUI and Collector HTTPS, with peer verification | 7.0.0 or earlier | CLS `SRG-APP-000427-AU-000040`; CLS `SRG-APP-000910-AU-000390`; CLS `SRG-APP-000175-AU-002630`; CLS `SRG-APP-000516-AU-000410` | `http_client_verify_peer=yes` (in phoenix_config.txt on each Collector and collector_config_template.txt on the Supervisor; SSLCertificateFile in /etc/httpd/conf.d/ssl.conf) |
| Core: Cryptography | Certificate verification for the SSL sockets between backend processes and the App Server (off by default) | 7.0.0 or earlier | CLS `SRG-APP-000516-AU-000410`; CLS `SRG-APP-000910-AU-000390` | `config-ssl-cert.sh -v 3 -c <CERT_FILE> -k <KEY_FILE> -a <CA_FILE> -r` |
| Core: Data protection | Disk encryption of the /cmdb, /svn, and /data disks | 7.0.0 or earlier | CLS `SRG-APP-000118-AU-000100`; GPOS `SRG-OS-000185-GPOS-00079`; GPOS `SRG-OS-000405-GPOS-00184` | `dnf install cryptsetup -y`; `cryptsetup luksFormat <DISK>` (per the Disk Encryption guide) |
| Core: Platform | Rocky Linux operating system, updated from the FortiSIEM OS repositories without a FortiSIEM upgrade | 7.0.0 or earlier | GPOS `SRG-OS-000439-GPOS-00195`; GPOS `SRG-OS-000830-GPOS-00300`; GPOS `SRG-OS-000366-GPOS-00153`; CLS `SRG-APP-000456-AU-000270` | `cat /etc/redhat-release`; `yum upgrade -y`; `needs-restarting -r` |
| Core: Platform | FortiSIEM upgrades and Collector image hash check | 7.0.0 or earlier | CLS `SRG-APP-000456-AU-000270`; CLS `SRG-APP-001035-AU-000430`; CLS `SRG-APP-000810-AU-000250` | GUI: Admin > Settings > System > Image Server (keep Hash Check enabled; compare the hash of each downloaded image with the support site) |
| Core: Platform | Host firewall (firewalld) with only the ports FortiSIEM needs | 7.0.0 or earlier | GPOS `SRG-OS-000480-GPOS-00232`; GPOS `SRG-OS-000096-GPOS-00050`; NDM `SRG-APP-000142-NDM-000245` | `firewall-cmd --reload` (close the ports the deployment does not use, such as SNMP Trap UDP 162) |
| Core: Platform | SSH access to the nodes (default port 22) | 7.0.0 or earlier | GPOS `SRG-OS-000033-GPOS-00014`; GPOS `SRG-OS-000297-GPOS-00115`; NDM `SRG-APP-000412-NDM-000331` | `systemctl status sshd` (SSH only for the administrators who install, upgrade, and troubleshoot; FIPS mode for the SSH ciphers) |
| Core: Platform | Unused interfaces on hardware appliances | 7.0.0 or earlier | GPOS `SRG-OS-000095-GPOS-00049` | `sudo ifconfig <INTERFACE> down` |
| Core: Platform | Time synchronization (NTP on the hypervisor host) | 7.0.0 or earlier | CLS `SRG-APP-000920-AU-000410`; CLS `SRG-APP-000086-AU-000030`; CLS `SRG-APP-000116-AU-000270`; GPOS `SRG-OS-000355-GPOS-00143`; NDM `SRG-APP-000395-NDM-000347` | (on ESX: host Configure > System > Time Configuration with internal NTP servers) |
| Core: Platform | Time zone set at installation; UTC date format in the GUI | 7.0.0 or earlier | CLS `SRG-APP-000374-AU-000290` | `configFSM.sh` (1 Set Timezone) |
| Core: High availability | Supervisor and Worker clusters, disaster recovery, and replication health | 7.0.0 or earlier | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Admin > Health > Replication Health |
| Core: Threat intelligence | FortiGuard IOC service and malware IP, domain, URL, and hash feeds | 7.0.0 or earlier | CLS `SRG-APP-000516-AU-000350` | GUI: Resources > Malware IPs |
| Core: Monitoring | Performance and availability monitoring, synthetic transactions, and configuration change monitoring | 7.0.0 or earlier | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Admin > Setup > Monitor Performance |
| Core: Monitoring | Business services, dashboards, and maintenance calendars | 7.0.0 or earlier | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Core: Monitoring | UEBA, identity and location, and risk scoring | 7.0.0 or earlier | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Core: Content | Content updates (parsers, rules, reports) from Fortinet | 7.0.0 or earlier | CLS `SRG-APP-000456-AU-000270` | GUI: Admin > Content Update |
| Core: Integration | Public REST API (user credentials over HTTPS) | 7.0.0 or earlier | CLS `SRG-APP-000148-AU-002270`; CLS `SRG-APP-000439-AU-004310` | (from 7.5.0, use API tokens; see that row) |
| Reports | Visual Report Designer (WYSIWYG report design editor) | 7.0.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Resources > Reports |
| Analytics | Query functions: aggregation, time window, string, conversion, extraction, and evaluation (ClickHouse and Elasticsearch) | 7.0.0 and later | CLS `SRG-APP-000750-AU-000130`; CLS `SRG-APP-000745-AU-000120` | GUI: Analytics > Search |
| Machine learning | Machine Learning Workbench (local or AWS jobs) and Gaussian and Gaussian mixture anomaly models | 7.0.0+; 7.1.0+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Analytics > Machine Learning |
| Incidents | Incident Investigation Workspace (link graph of incidents and entities) | 7.0.0 and later | CLS `SRG-APP-000365-AU-000210`; CLS `SRG-APP-000775-AU-000180` | GUI: Incidents > Investigation |
| Machine learning | Built-in models: login anomaly detection and incident resolution recommendation (the recommendation cannot be disabled) | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Storage | ClickHouse Event Integrity (per-shard and per-partition checksums; off by default) | 7.0.0 and later | CLS `SRG-APP-000080-AU-000010`; CLS `SRG-APP-000119-AU-000110`; CLS `SRG-APP-000795-AU-000220` | GUI: Admin > Settings > Database > Event Integrity (Event Integrity: On) |
| Discovery | Fortinet Security Fabric discovery and FortiClient EMS discovery (endpoints and vulnerabilities) | 7.0.0 and later | CLS `SRG-APP-000086-AU-000020` | GUI: Admin > Setup > Discovery |
| Remediation | FortiEMS endpoint tagging through the remediation framework | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Agents | Windows Agent 5.0.0 and Linux Agent 7.0.0: discovery and performance monitoring by the agent | 7.0.0 and later | CLS `SRG-APP-000086-AU-000020` | GUI: Admin > Setup > Windows Agent; GUI: Admin > Setup > Linux Agent |
| UEBA and risk | Entity risk view and host and user risk scoring (incident rarity) | 7.0.0+; 7.2.0+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Threat intelligence | External threat intelligence: Python feed framework and integration health, STIX/TAXII 2.1, and 34 more sources | 7.0.0+; 7.1.0+; 7.2.0+ | CLS `SRG-APP-000516-AU-000350` | GUI: Resources > Malware IPs |
| Storage | Elasticsearch 8.5.3 support | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Remediation | FortiGate VDOM-based mitigation scripts | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Rules | Rule enhancements (compare attributes within an event, expressions on the right-hand side) | 7.0.0 and later | CLS `SRG-APP-000111-AU-000150` | GUI: Resources > Rules |
| Admin accounts | GUI inactivity timeout enforced from the user's Idle Timeout (except on dashboards) | 7.0.0 and later | CLS `SRG-APP-000295-AU-000190` | GUI: CMDB > Users (FortiSIEM Attributes tab: Idle Timeout) |
| Platform | Miscellaneous: cloud service CMDB entries with no-log alerts, SMTP over SSL on ports 587 and 465, default FortiSIEM Users group | 7.0.0 and later | CLS `SRG-APP-000360-AU-000130`; CLS `SRG-APP-000439-AU-004310` | GUI: Admin > Settings > System > Email (Secure Connection (TLS)) |
| Platform | Rocky Linux 8 OS patches and component updates (PostgreSQL) shipped in the release | 7.0.1+; 7.1.0+; 7.2.0+; 7.3.0+; 7.4.0+ | GPOS `SRG-OS-000439-GPOS-00195`; CLS `SRG-APP-000456-AU-000270`; GPOS `SRG-OS-000830-GPOS-00300` | `yum upgrade -y` (between releases, from the FortiSIEM OS repositories) |
| Incidents | Optimized incident trigger event lookup (latest 100 events over 30 days) | 7.0.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Storage | ClickHouse storage reduction (ZSTD compression) | 7.0.2+; 7.1.0+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| FortiAI | Fortinet Advisor, renamed FortiAI in 7.2.0: OpenAI-powered SOC queries, incident analysis, and report building (data anonymized before sending) | 7.1.0+; 7.2.0+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Admin > Settings > Analytics > ML / AI (FortiAI tab: leave the ChatGPT Key empty unless approved) |
| Rules | Scheduled rules for ClickHouse, with FOLLOWED_BY and NOT_FOLLOWED_BY | 7.1.0+; 7.3.0+ | CLS `SRG-APP-000111-AU-000150`; CLS `SRG-APP-000516-AU-000350` | GUI: Resources > Rules |
| Agents | Windows certificate monitoring by the agent | 7.1.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Agents | Osquery through the Windows Agent (7.1.0) and the Linux Agent (7.5.0) | 7.1.0+; 7.5.0+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Resources > Osquery |
| UEBA and risk | User aliases in risk calculation | 7.1.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| GUI | GUI enhancements (incident slide-ins, threat analysis tab, markdown notes, related incidents, CMDB global view, filters) | 7.1.0+; 7.2.0+; 7.3.0+; 7.4.0+; 7.5.1+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Rules | Dynamic watch list using user-to-IP lookup | 7.1.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Event collection | Kafka event collection: several Collectors per topic, SASL/SSL encryption configured in the GUI | 7.1.0 and later | CLS `SRG-APP-000439-AU-004310` | (SASL/SSL for every Kafka integration) |
| Platform | Choice of network interface for the Windows Agent and at installation | 7.1.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Integration | Public REST API: archive query, IP/host/user context, and CMDB query APIs | 7.1.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Content | Built-in rule, report, parser, and dashboard content updates (data source fields, SIGMA rules, ITDR rule group) | 7.1.0+; 7.2.0+; 7.4.0+; 7.5.1+; 7.6.0+ | CLS `SRG-APP-000516-AU-000350` | GUI: Resources > Rules |
| Device support | New and enhanced device and log source support (including generic webhooks and FortiPAM in 7.2.0) | 7.1.0+; 7.2.0+; 7.4.0+; 7.5.0+; 7.6.0+ | CLS `SRG-APP-000086-AU-000020` | GUI: Admin > Setup > Pull Events |
| Platform | Redis memory usage optimization | 7.1.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Device support | Trend Vision One XDR support | 7.1.1 and later | CLS `SRG-APP-000086-AU-000020` | — |
| Integration | Public REST API throttling (concurrent requests per source IP and globally) | 7.1.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | `global_max_concurrent_public_api_requests=50` (in phoenix_config.txt) |
| Storage | ClickHouse archive to Google Cloud Storage (GCP deployments) | 7.1.4 and later | CLS `SRG-APP-000358-AU-000100`; CLS `SRG-APP-000125-AU-000300` | GUI: Admin > Setup > Storage |
| Agents | Windows Agent updates: native XML log format (7.1.4); no .NET Framework, osquery 5.14.1 (7.4.0) | 7.1.4+; 7.4.0+ | CLS `SRG-APP-000089-AU-000400` | — |
| Storage | ClickHouse data movement algorithm change between tiers | 7.1.4 and later | CLS `SRG-APP-000095-AU-000050` | — |
| Incidents | Incident actions on all incident pages | 7.1.4 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Storage | Script to rebuild pre-7.1.1 ClickHouse IP indexes | 7.1.4 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | `/opt/phoenix/phscripts/clickhouse/rebuild_ip_bloom_filter.sh -r <INDEX_ID>` |
| Agents | Linux Agent: new code signing certificate (7.1.9); AlmaLinux and Amazon Linux 2023 support (7.5.1) | 7.1.9+; 7.5.1+ | CLS `SRG-APP-000810-AU-000250` | — |
| Cases | Automated case management (analyst teams, case management and assignment policies, SLAs) | 7.2.0 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Admin > Settings > General > Case Management |
| High availability | Collector high availability (VRRP or load balancer) | 7.2.0 and later | CLS `SRG-APP-000360-AU-000130` | GUI: Admin > Settings > System > Cluster Config |
| Analytics | Search field analytics and up to 1 million non-aggregated search results (ClickHouse) | 7.2.0 and later | CLS `SRG-APP-000790-AU-000210`; CLS `SRG-APP-000745-AU-000120` | GUI: Analytics > Search |
| Rules | Custom SIGMA rule import (URL, file, or YAML) | 7.2.0 and later | CLS `SRG-APP-000516-AU-000350`; CLS `SRG-APP-000800-AU-000230` | GUI: Resources > Rules |
| Hardware and cloud | FortiSIEM 500G appliance as a ClickHouse Keeper | 7.2.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Licensing | Raw event size based licensing (GB per day) | 7.2.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Event collection | Script to export IBM QRadar logs to FortiSIEM | 7.2.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Dashboards | Dashboard query caching (ClickHouse) | 7.2.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| High availability | Automated Supervisor high availability (three or more nodes; manual HA with two nodes from 7.3.1) | 7.3.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Admin > License > Nodes |
| Analytics | Advanced Search with ClickHouse SQL queries, and scheduled rules built from it | 7.3.0+; 7.4.0+ | CLS `SRG-APP-000790-AU-000210`; CLS `SRG-APP-000111-AU-000150`; CLS `SRG-APP-000780-AU-000190` | GUI: Analytics > Advanced Search |
| Cryptography | Installation on RHEL 8.10 for FIPS 140-2 validated crypto modules | 7.3.0 and later | CLS `SRG-APP-000514-AU-002890`; GPOS `SRG-OS-000478-GPOS-00223` | (install FortiSIEM as an application on RHEL 8.10 where validated modules are required) |
| Platform | Collector OS updates through the Supervisor during upgrade | 7.3.0 and later | GPOS `SRG-OS-000439-GPOS-00195` | — |
| Platform | Simplified offline upgrade from a mounted OS repository | 7.3.0 and later | CLS `SRG-APP-000456-AU-000270` | — |
| Platform | Choice of disk sizes for opt, cmdb, and svn at installation | 7.3.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Storage | NFS storage for ClickHouse warm and cold tiers | 7.3.0 and later | CLS `SRG-APP-000359-AU-000120` | GUI: Admin > Settings > Database > ClickHouse Config |
| Event collection | Prompt for the Collector registration password | 7.3.0 and later | CLS `SRG-APP-000439-AU-004310` | `phProvisionCollector --add <USER> <SUPERVISOR_FQDN> <ORGANIZATION> <COLLECTOR_NAME>` |
| Platform | Separate open firewall ports for Supervisor, Workers, and Collectors | 7.3.0 and later | GPOS `SRG-OS-000096-GPOS-00050`; NDM `SRG-APP-000142-NDM-000245` | — |
| High availability | Rate-limited rsync between Supervisor sites | 7.3.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Notifications | Incident notifications by webhook (Microsoft Teams in 7.3.0; WhatsApp, Slack, Telegram, and custom in 7.5.0) | 7.3.0+; 7.5.0+ | CLS `SRG-APP-000516-AU-000350` | GUI: Admin > Settings > Analytics > Incident Notification |
| Notifications | Enhanced default incident email template | 7.3.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| FortiAI | FortiAI features: semantic search, SQL fixes and generation, GPT-4o agent, incident categorization, result analysis, and Azure OpenAI | 7.3.0+; 7.4.0+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Admin > Settings > Analytics > ML / AI (FortiAI tab: leave the ChatGPT Key empty unless approved) |
| Health | CMDB search on event pulling, performance monitoring, and agent status | 7.3.0 and later | CLS `SRG-APP-000360-AU-000130` | GUI: CMDB > Devices |
| Reports | PDF export for wide tables, and saved report results | 7.3.0+; 7.5.0+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Health | Slide-in panes for Admin > Health | 7.3.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Integration | REST API: case, entity reputation, risk score, and asynchronous triggering event APIs | 7.3.3+; 7.4.0+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Dashboards | New dashboard framework, global FortiSIEM dashboard, and revised built-in dashboards | 7.4.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Automation | Automation Service: native playbooks run on Collector agents (separate license) | 7.4.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Resources > Automation > Playbooks |
| Incidents | Incident tags associated with rules | 7.4.0 and later | CLS `SRG-APP-000516-AU-000380` | GUI: Admin > Settings > Analytics > Rule Tags |
| Platform | Automated cluster upgrade of Supervisors and Workers (fsm_cluster_upgrade.py) | 7.4.0+; 7.6.0+ | CLS `SRG-APP-000456-AU-000270` | `python fsm_cluster_upgrade.py` |
| Remote authentication | RADIUS for GUI external authentication; inter-node ports TCP 7900-7950 and 27900-27950 restricted to Supervisor and Worker nodes; audit logs for Org rule activation | 7.4.0 and later | NDM `SRG-APP-000516-NDM-000336`; CLS `SRG-APP-000148-AU-002270`; CLS `SRG-APP-000800-AU-000230` | GUI: Admin > Settings > General > External Authentication |
| Storage | ClickHouse partition order detection and shard storage gap rules | 7.4.0 and later | CLS `SRG-APP-000359-AU-000120` | `/opt/phoenix/bin/clickhouse-rebalance-partitions` |
| High availability | High availability across data centers (disaster recovery discontinued in 7.5.0) | 7.4.1+; 7.5.0+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Analytics | Federated search of external datastores (AWS Security Lake, S3, FortiEDR, databases) | 7.5.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Resources > External Datasets |
| Event pipeline | Event tagging by policy or file, applied on the Collectors | 7.5.0 and later | CLS `SRG-APP-000089-AU-000400` | GUI: Admin > Settings > Event Pipeline > Event Tagging (add attributes; never overwrite the original ones) |
| Storage | ClickHouse storage regions (events kept in regional shards) | 7.5.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| FortiAI | Agentic FortiAI chat and incident and case investigation, with read-only access and security restrictions | 7.5.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Admin > Settings > Analytics > ML / AI (FortiAI tab: leave the ChatGPT Key empty unless approved) |
| Integration | API tokens for the public REST API (OAuth refresh token grant in 7.5.0; client credentials grant in 7.5.1) | 7.5.0 and later | CLS `SRG-APP-000148-AU-002270`; CLS `SRG-APP-000033-AU-001610` | GUI: Admin > Settings > System > API Token (least-privilege tokens; revoke unused tokens) |
| Agents | Headless Windows Agent (configured locally, no Supervisor registration) | 7.5.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Platform | Rocky Linux 9 (9.7 in 7.5.0, 9.8 in 7.6.0) with GlassFish, JDK, PostgreSQL, ClickHouse, and Redis upgrades | 7.5.0+; 7.6.0+ | GPOS `SRG-OS-000439-GPOS-00195`; GPOS `SRG-OS-000830-GPOS-00300`; CLS `SRG-APP-000456-AU-000270`; CLS `SRG-APP-001035-AU-000430` | `cat /etc/redhat-release`; `yum upgrade -y` |
| GUI | GUI user experience: navigation moved to the side | 7.5.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Platform | App Server performance improvements (API tokens rather than sessions) | 7.5.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Cryptography | Client certificate based mutual authentication between Supervisor and Worker processes | 7.5.0 and later | CLS `SRG-APP-000516-AU-000410` | — |
| Agents | Pre-built Linux and Windows Agent monitoring templates | 7.5.0 and later | CLS `SRG-APP-000086-AU-000020` | GUI: Admin > Setup > Windows Agent; GUI: Admin > Setup > Linux Agent |
| Integration | MCP service for customer AI agents (read-only CMDB and event access by API token; ClickHouse only) | 7.5.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | GUI: Admin > Settings > System > API Token (issue no MCP tokens unless approved) |
| Integration | Public REST API updates (OAuth token, v2 event query, structured event query; deprecated and removed APIs) | 7.5.1+; 7.6.0+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Cryptography | Secure ClickHouse communication over SSL (default on new installations; script after upgrade) | 7.6.0 and later | CLS `SRG-APP-000439-AU-004310`; CLS `SRG-APP-000118-AU-000100` | `/opt/phoenix/phscripts/clickhouse/migrate_clickhouse_keeper_cluster_to_ssl_config.sh` |
| Event collection | Improved Collector event handling (PCRE2 with JIT-compiled regular expressions) | 7.6.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Hardware and cloud | Hardware appliances reach FortiGuard again (certificates from BIOS for IOC download, image hash verification, content updates) | 7.6.0 and later | CLS `SRG-APP-000810-AU-000250` | — |
| GUI | GUI rewritten in Angular 21; Windows and Linux Agents renamed Host Collectors | 7.6.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| High availability | Supervisor HA etcd improvements (location, compaction, defragmentation) | 7.6.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current releases:

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/26-fortisiem-feature-version-and-srg-map-requirements.csv) (101 rows).

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| CLS | `SRG-APP-000026-AU-000580` | CAT II | The Central Log Server must automatically audit account creation. |
| CLS | `SRG-APP-000027-AU-000590` | CAT II | The Central Log Server must automatically audit account modification. |
| CLS | `SRG-APP-000033-AU-001610` | CAT I | The Central Log Server must be configured to enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies. |
| CLS | `SRG-APP-000065-AU-000240` | CAT II | The Central Log Server must enforce the limit of three consecutive invalid logon attempts by a user during a 15 minute time period. |
| CLS | `SRG-APP-000068-AU-000035` | CAT III | The Central Log Server must display the Standard Mandatory DoW Notice and Consent Banner before granting access to the Central Log Server. |
| CLS | `SRG-APP-000069-AU-000420` | CAT III | The Central Log Server must retain the Standard Mandatory DoW Notice and Consent Banner on the screen until users acknowledge the usage conditions and take explicit actions to log on for further access. |
| CLS | `SRG-APP-000080-AU-000010` | CAT II | The Central Log Server must be configured to protect the data sent from hosts and devices from being altered in a way that may prevent the attribution of an action to an individual (or process acting on behalf of an individual). |
| CLS | `SRG-APP-000086-AU-000020` | CAT III | The Central Log Server must be configured to aggregate log records from organization-defined devices and hosts within its scope of coverage. |
| CLS | `SRG-APP-000086-AU-000030` | CAT III | Time stamps recorded on the log records in the Central Log Server must be configured to synchronize to within one second of the host server or, if NTP is configured directly in the log server, the NTP time source must be the same as the host and devices within its scope of coverage. |
| CLS | `SRG-APP-000086-AU-000390` | CAT II | Where multiple log servers are installed in the enclave, each log server must be configured to aggregate log records to a central aggregation server or other consolidated events repository. |
| CLS | `SRG-APP-000089-AU-000400` | CAT II | The Central Log Server must be configured to retain the DoW-defined attributes of the log records sent by the devices and hosts. |
| CLS | `SRG-APP-000090-AU-000070` | CAT III | The Central Log Server must be configured to allow only the Information System Security Manager (ISSM) (or individuals or roles appointed by the ISSM) to select which auditable events are to be retained. |
| CLS | `SRG-APP-000095-AU-000050` | CAT III | The System Administrator (SA) and Information System Security Manager (ISSM) must configure the retention of the log records based on criticality level, event type, and/or retention period, at a minimum. |
| CLS | `SRG-APP-000095-AU-000680` | CAT III | The Central Log Server must produce audit records containing information to establish what type of events occurred. |
| CLS | `SRG-APP-000100-AU-000730` | CAT III | The Central Log Server must generate audit records containing information that establishes the identity of any individual or process associated with the event. |
| CLS | `SRG-APP-000111-AU-000150` | CAT III | The Central Log Server must be configured to perform analysis of log records across multiple devices and hosts in the enclave that can be reviewed by authorized individuals. |
| CLS | `SRG-APP-000115-AU-000160` | CAT III | The Central Log Server must be configured to perform on-demand filtering of the log records for events of interest based on organization-defined criteria. |
| CLS | `SRG-APP-000116-AU-000270` | CAT III | The Central Log Server must be configured to use internal system clocks to generate time stamps for log records. |
| CLS | `SRG-APP-000118-AU-000100` | CAT II | The Central Log Server must protect audit information from any type of unauthorized read access. |
| CLS | `SRG-APP-000119-AU-000110` | CAT II | The Central Log Server must protect audit information from unauthorized modification. |
| CLS | `SRG-APP-000120-AU-000120` | CAT II | The Central Log Server must protect audit information from unauthorized deletion. |
| CLS | `SRG-APP-000121-AU-000130` | CAT II | The Central Log Server must protect audit tools from unauthorized access. |
| CLS | `SRG-APP-000125-AU-000300` | CAT III | The Central Log Server must be configured to back up the log records repository at least every seven days onto a different system or system component other than the system or component being audited. |
| CLS | `SRG-APP-000141-AU-000090` | CAT II | The Central Log Server must be configured to disable non-essential capabilities. |
| CLS | `SRG-APP-000148-AU-002270` | CAT I | The Central Log Server must be configured to uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| CLS | `SRG-APP-000149-AU-002280` | CAT II | The Central Log Server must use multifactor authentication for network access to privileged user accounts. |
| CLS | `SRG-APP-000163-AU-002470` | CAT II | The Central Log Server must disable accounts (individuals, groups, roles, and devices) after 35 days of inactivity. |
| CLS | `SRG-APP-000164-AU-002480` | CAT II | The Central Log Server must be configured to enforce a minimum 15-character password length. |
| CLS | `SRG-APP-000166-AU-002490` | CAT III | The Central Log Server must be configured to enforce password complexity by requiring that at least one uppercase character be used. |
| CLS | `SRG-APP-000170-AU-002530` | CAT III | The Central Log Server must be configured to require the change of at least eight of the total number of characters when passwords are changed. |
| CLS | `SRG-APP-000171-AU-002540` | CAT I | For accounts using password authentication, the Central Log Server must be configured to store only cryptographic representations of passwords. |
| CLS | `SRG-APP-000174-AU-002570` | CAT III | The Central Log Server must be configured to enforce a 180-day maximum password lifetime restriction. |
| CLS | `SRG-APP-000175-AU-002630` | CAT I | The Central Log Server, when utilizing PKI-based authentication, must validate certificates by constructing a certification path (which includes status information) to an accepted trust anchor. |
| CLS | `SRG-APP-000179-AU-002670` | CAT I | The Central Log Server must use FIPS-validated SHA-1 or higher hash function to protect the integrity of keyed-hash message authentication code (HMAC), Key Derivation Functions (KDFs), Random Bit Generation, hash-only applications, and digital signature verification (legacy use only). |
| CLS | `SRG-APP-000291-AU-000200` | CAT III | The Central Log Server must notify system administrators and ISSO when accounts are created. |
| CLS | `SRG-APP-000292-AU-000420` | CAT III | For devices and hosts within its scope of coverage, the Central Log Server must be configured to notify the system administrator (SA) and information system security officer (ISSO) when account modification events are received. |
| CLS | `SRG-APP-000295-AU-000190` | CAT II | The Central Log Server must automatically terminate a user session after organization-defined conditions or trigger events requiring session disconnect. |
| CLS | `SRG-APP-000296-AU-000560` | CAT II | The Central Log Server must provide a logout capability for user initiated communication session. |
| CLS | `SRG-APP-000345-AU-000400` | CAT II | The Central Log Server must automatically lock the account until the locked account is released by an administrator when three unsuccessful login attempts in 15 minutes are exceeded. |
| CLS | `SRG-APP-000358-AU-000100` | CAT II | The Central Log Server must be configured to off-load log records onto a different system or media than the system being audited. |
| CLS | `SRG-APP-000359-AU-000120` | CAT III | The Central Log Server must be configured to send an immediate alert to the System Administrator (SA) and Information System Security Officer (ISSO) (at a minimum) when allocated log record storage volume reaches 75 percent of the repository maximum log record storage capacity. |
| CLS | `SRG-APP-000360-AU-000130` | CAT III | For the host and devices within its scope of coverage, the Central Log Server must be configured to send a real-time alert to the System Administrator (SA) and Information System Security Officer (ISSO) (at a minimum) of all audit failure events, such as loss of communications with hosts and devices, or if log records are no longer being received. |
| CLS | `SRG-APP-000362-AU-000170` | CAT III | The Central Log Server must be configured to perform on-demand sorting of log records for events of interest based on the content of organization-defined audit fields within log records. |
| CLS | `SRG-APP-000363-AU-000180` | CAT III | The Central Log Server must be configured to perform on-demand searches of log records for events of interest based on the content of organization-defined audit fields within log records. |
| CLS | `SRG-APP-000365-AU-000210` | CAT III | The Central Log Server must be configured to perform audit reduction that supports after-the-fact investigations of security incidents. |
| CLS | `SRG-APP-000366-AU-000220` | CAT III | The Central Log Server must be configured to generate on-demand audit review and analysis reports. |
| CLS | `SRG-APP-000374-AU-000290` | CAT III | Upon receipt of the log record from hosts and devices, the Central Log Server must be configured to record time stamps of the time of receipt that can be mapped to Coordinated Universal Time (UTC). |
| CLS | `SRG-APP-000391-AU-002290` | CAT II | The Central Log Server must be configured to accept the DoW common access card (CAC) credential to support identity management and personal authentication. |
| CLS | `SRG-APP-000427-AU-000040` | CAT II | The Central Log Server must only allow the use of DoW Public Key Infrastructure (PKI)-established certificate authorities for verification of the establishment of protected sessions. |
| CLS | `SRG-APP-000439-AU-004310` | CAT I | The Central Log Server must be configured to protect the confidentiality and integrity of transmitted information. |
| CLS | `SRG-APP-000456-AU-000270` | CAT I | The Central Log Server must install security-relevant software updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| CLS | `SRG-APP-000503-AU-000280` | CAT II | The Central Log Server must generate audit records when successful/unsuccessful logon attempts occur. |
| CLS | `SRG-APP-000514-AU-002890` | CAT I | The Central Log Server must implement NIST FIPS-validated cryptography for the following: to provision digital signatures; to generate cryptographic hashes; and/or to protect unclassified information requiring confidentiality and cryptographic protection. |
| CLS | `SRG-APP-000515-AU-000110` | CAT III | The Central Log Server must be configured to off-load interconnected systems in real time and off-load standalone systems weekly, at a minimum. |
| CLS | `SRG-APP-000516-AU-000060` | CAT III | The Central Log Server must be configured so changes made to the level and type of log records stored in the centralized repository must take effect immediately without the need to reboot or restart the application. |
| CLS | `SRG-APP-000516-AU-000330` | CAT II | The Central Log Server must be configured to retain the identity of the original source host or device where the event occurred as part of the log record. |
| CLS | `SRG-APP-000516-AU-000340` | CAT II | The Central Log Server that aggregates log records from hosts and devices must be configured to use TCP for transmission. |
| CLS | `SRG-APP-000516-AU-000350` | CAT II | The Central Log Server must be configured to notify the System Administrator (SA) and Information System Security Officer (ISSO), at a minimum, when an attack is detected on multiple devices and hosts within its scope of coverage. |
| CLS | `SRG-APP-000516-AU-000360` | CAT II | The Central Log Server must be configured to automatically create trouble tickets for organization-defined threats and events of interest as they are detected in real time (within seconds). |
| CLS | `SRG-APP-000516-AU-000370` | CAT II | For devices and hosts within the scope of coverage, the Central Log Server must be configured to automatically aggregate events that indicate account actions. |
| CLS | `SRG-APP-000516-AU-000380` | CAT II | The Central Log Server must be configured with the organization-defined severity or criticality levels of each event that is being sent from individual devices or hosts. |
| CLS | `SRG-APP-000516-AU-000410` | CAT II | Analysis, viewing, and indexing functions, services, and applications used as part of the Central Log Server must be configured to comply with DoW-trusted path and access requirements. |
| CLS | `SRG-APP-000610-AU-000050` | CAT I | The Central Log Server must use FIPS-validated SHA-2 or higher hash function for digital signature generation and verification (non-legacy use). |
| CLS | `SRG-APP-000745-AU-000120` | CAT II | The Central Log Server must implement the capability to centrally review and analyze audit records from multiple components within the system. |
| CLS | `SRG-APP-000750-AU-000130` | CAT II | The Central Log Server must implement an audit reduction capability that supports on-demand audit review and analysis. |
| CLS | `SRG-APP-000770-AU-000170` | CAT II | The Central Log Server must implement a report generation capability that supports on-demand reporting requirements. |
| CLS | `SRG-APP-000775-AU-000180` | CAT II | The Central Log Server must implement a report generation capability that supports after-the-fact investigations of incidents. |
| CLS | `SRG-APP-000780-AU-000190` | CAT II | The Central Log Server must implement an audit reduction capability that does not alter original content or time ordering of audit records. |
| CLS | `SRG-APP-000790-AU-000210` | CAT II | The Central Log Server must implement the capability to process, sort, and search audit records for events of interest based on organization-defined audit fields within audit records. |
| CLS | `SRG-APP-000795-AU-000220` | CAT II | The Central Log Server must alert organization-defined personnel or roles upon detection of unauthorized access, modification, or deletion of audit information. |
| CLS | `SRG-APP-000800-AU-000230` | CAT II | The Central Log Server must implement the capability for organization-defined individuals or roles to change the auditing to be performed on organization-defined system components based on organization-defined selectable event criteria within organization-defined time thresholds. |
| CLS | `SRG-APP-000810-AU-000250` | CAT II | The Central Log Server must prevent the installation of organization-defined software and firmware components without verification that the component has been digitally signed using a certificate that is recognized and approved by the organization. |
| CLS | `SRG-APP-000815-AU-000260` | CAT II | The Central Log Server must require users to be individually authenticated before granting access to the shared accounts or resources. |
| CLS | `SRG-APP-000825-AU-000280` | CAT II | The Central Log Server must implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that the device meets organization-defined strength of mechanism requirements. |
| CLS | `SRG-APP-000845-AU-000320` | CAT II | The Central Log Server must for password-based authentication, verify when users create or update passwords, that the passwords are not found on the list of commonly-used, expected, or compromised passwords in IA-5 (1) (a). |
| CLS | `SRG-APP-000910-AU-000390` | CAT II | The Central Log Server must include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| CLS | `SRG-APP-000920-AU-000410` | CAT II | The Central Log Server must synchronize system clocks within and between systems or system components. |
| CLS | `SRG-APP-001035-AU-000430` | CAT I | The Central Log Server must be a version supported by the vendor. |
| NDM | `SRG-APP-000142-NDM-000245` | CAT I | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services |
| NDM | `SRG-APP-000148-NDM-000346` | CAT II | The network device must be configured with only one local account to be used as the account of last resort in the event the authentication server is unavailable. |
| NDM | `SRG-APP-000395-NDM-000310` | CAT II | The network device must be configured to authenticate SNMP messages using a FIPS-validated Keyed-Hash Message Authentication Code (HMAC). |
| NDM | `SRG-APP-000395-NDM-000347` | CAT II | The network device must authenticate Network Time Protocol sources using authentication that is cryptographically based. |
| NDM | `SRG-APP-000412-NDM-000331` | CAT I | The network device must be configured to implement cryptographic mechanisms using a FIPS 140-2 approved algorithm to protect the confidentiality of remote maintenance sessions |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000880-NDM-000290` | CAT II | The network device must be configured to protect nonlocal maintenance sessions by separating the maintenance session from other network sessions with the system by logically separated communications paths. |
| GPOS | `SRG-OS-000023-GPOS-00006` | CAT II | The operating system must display the Standard Mandatory DoW Notice and Consent Banner before granting local or remote access to the system. |
| GPOS | `SRG-OS-000033-GPOS-00014` | CAT I | The operating system must implement DoW-approved encryption to protect the confidentiality of remote access sessions. |
| GPOS | `SRG-OS-000095-GPOS-00049` | CAT II | The operating system must be configured to disable non-essential capabilities. |
| GPOS | `SRG-OS-000096-GPOS-00050` | CAT II | The operating system must be configured to prohibit or restrict the use of functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. |
| GPOS | `SRG-OS-000185-GPOS-00079` | CAT II | The operating system must protect the confidentiality and integrity of all information at rest. |
| GPOS | `SRG-OS-000297-GPOS-00115` | CAT II | The operating system must control remote access methods. |
| GPOS | `SRG-OS-000355-GPOS-00143` | CAT II | The operating system must, for networked systems, compare internal information system clocks at least every 24 hours with an authoritative time source. |
| GPOS | `SRG-OS-000366-GPOS-00153` | CAT I | The operating system must prevent the installation of patches, service packs, device drivers, or operating system components without verification they have been digitally signed using a certificate that is recognized and approved by the organization. |
| GPOS | `SRG-OS-000405-GPOS-00184` | CAT I | The operating system must implement cryptographic mechanisms to prevent unauthorized disclosure of all information at rest on all operating system components. |
| GPOS | `SRG-OS-000439-GPOS-00195` | CAT I | The operating system must install security-relevant software updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| GPOS | `SRG-OS-000478-GPOS-00223` | CAT I | The operating system must implement NIST FIPS-validated cryptography for the following: to provision digital signatures, to generate cryptographic hashes, and to protect unclassified information requiring confidentiality and cryptographic protection in accordance with applicable federal laws, Executive Orders, directives, policies, regulations, and standards. |
| GPOS | `SRG-OS-000480-GPOS-00227` | CAT II | The operating system must be configured in accordance with the security configuration settings based on DoW security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. |
| GPOS | `SRG-OS-000480-GPOS-00232` | CAT II | The operating system must enable an application firewall, if available. |
| GPOS | `SRG-OS-000830-GPOS-00300` | CAT I | The operating system must be a version supported by the vendor. |

### Collecting evidence

On each node, run `cat /etc/redhat-release` and keep the output with the
checklist, together with the FortiSIEM version of every node from *Admin >
Health > Cloud Health* and *Admin > Health > Collector Health*, and the
operating system assessment of each host. Add screenshots or exports of
the panes the map cites, above all *CMDB > Users* (the FortiSIEM
Attributes of each user), *Admin > Settings > Role > Role Management*,
*Admin > Settings > General > External Authentication*, *Admin >
Settings > System > UI* (Login Banner and Lockout Users), *Admin > Settings >
System > Trusted Hosts*, *Admin > Settings > Event Pipeline > Forwarding
tab*, *Admin > Setup > Storage*, *Admin > Settings > Database > Retention
Policy*, *Admin > Settings > Database > Event Integrity* (with the
exported validation results), *Admin > Settings > General > Automation
Policy*, and *Admin > Settings > System > Image Server*. Run the reports
in the FortiSIEM Audit folder of *Resources > Reports* for the assessment
period, list the active rules in *Resources > Rules*, and keep the backup
schedule and the location of the CMDB, SVN, and event backups.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiSIEM.** Check the version
  column against the release of every node, and check whether the feature
  depends on the event database (ClickHouse only), the license, or the
  deployment type.
- **A setting is not where the map says.** 7.5.0 moved the navigation to
  the side of the GUI and 7.6.0 rewrote the GUI; look for the setting under
  the same *Admin*, *CMDB*, or *Resources* path, and check the User Guide
  of your release.
- **Collectors stop registering or uploading after hardening.** Add the
  Collectors and Host Collectors to *Trusted Hosts*, check that the
  certificates match the FQDNs the Collectors use (and that
  `http_client_verify_peer=yes` is set on both sides), and check the
  firewall ports of each node type.
- **A FIPS node cannot talk to another node or device.** A FIPS-compliant
  node communicates only with FIPS-compliant nodes, and older devices that
  do not support FIPS algorithms break; check every node's mode before
  enabling it.
- **Events disappear before the retention period ends.** Space-based
  retention purges the oldest events when a tier is nearly full,
  regardless of the retention policies; add storage or archive capacity.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (account reviews, hash checks, time checks), by another system
  (the directory, the identity provider, the second log server), or by the
  host operating system. Record how each requirement is met, not just
  which feature covers it.

## Security and Best Practices

- Keep FortiSIEM on a vendor-supported release and patch the Rocky Linux
  hosts from the FortiSIEM OS repositories within 30 days.
- Change the default GUI and SSH passwords at installation, authenticate
  users through LDAPS, RADIUS, or SAML with CAC, give every user a
  least-privilege role, *Unlock by Administrator*, a short *Idle Timeout*,
  and a *Password Reset* of 180 days or less, and set *Lockout Users* to 35
  days.
- Enable the Login Banner, restrict GUI logons with *Trusted Hosts*, and
  restrict SSH to administrators.
- Use FIPS mode, or RHEL with validated modules where required; install
  CA-signed certificates and enable certificate verification for
  Collectors and the internal SSL sockets.
- Protect the event data: ClickHouse event integrity on, encrypted
  /cmdb, /svn, and /data disks, archives and backups on separate systems,
  and real-time forwarding over TCP over SSL.
- Activate the rules for attacks, account actions, and log-collection
  failures, and route their incidents to the SA and ISSO.
- Review this map each time Fortinet publishes a FortiSIEM release or DISA
  updates the CLS SRG, the NDM SRG, or the GPOS SRG.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiSIEM Release Notes*, page "What's New in *release*",
  releases 7.0.0 to 7.0.4, 7.1.0 to 7.1.9, 7.2.0 to 7.2.7, 7.3.0 to 7.3.5,
  7.4.0 to 7.4.2, 7.5.0, 7.5.1, and 7.6.0 (docs.fortinet.com, FortiSIEM
  documentation).
- Fortinet, *FortiSIEM 7.6.0 User Guide* and *FortiSIEM 7.0.0 User Guide*
  (for the core features).
- Fortinet, *FortiSIEM 7.6.0 Hardening Guide*, *ESX Installation Guide*,
  *OS Update Procedure*, *Configuring CA Certificates*, *Disk Encryption
  for FortiSIEM Virtual Machine*, *Upgrade Guide*, *High Availability and
  Disaster Recovery Procedures - ClickHouse*, and *Installing on RHEL 9.6
  for FIPS 140-3 Crypto Module Support*.
- DISA Central Log Server SRG V3R5, Network Device Management SRG V5R5,
  and General Purpose Operating System SRG V3R4, from the October 2026
  STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map), and
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the other Central Log Server SRG chapter and the
  model for this one).

**Knowledge checks:**

1. Why is the Central Log Server SRG the primary SRG for FortiSIEM, and
   what do the NDM and GPOS SRGs add?
2. Why is the host of a FortiSIEM node assessed against the GPOS SRG
   rather than an operating system STIG, and when does the RHEL 9 STIG
   apply instead?
3. Where does the version data come from, and which parts of the "What's
   New" pages are not counted as features?
4. Which features off-load and protect the log records, and which
   requirements do they support?
5. Which settings on a FortiSIEM user meet the lockout, idle timeout, and
   password lifetime requirements, and where do they fall short?
6. Which requirements can FortiSIEM not meet exactly, and how do you
   handle them?

## Summary and Completion Checklist

FortiSIEM has no STIG, so it is assessed against the Central Log Server
SRG as its primary SRG, the NDM SRG for its management interface, and the
GPOS SRG for the Rocky Linux host of each node. This chapter maps
153 features to the FortiSIEM release that introduced them, to
101 requirements (78 CLS, 9 NDM, and 14 GPOS), and
to the GUI pane or command that configures them: 63 core platform
features, and 90 features from the FortiSIEM 7.0.0 through 7.6.0
release notes. Operational features with no direct requirement fall under
the requirement to disable non-essential capabilities when unused, and the
full GPOS SRG still applies to every host.

- [ ] Can explain why FortiSIEM is assessed against the CLS, NDM, and GPOS
  SRGs.
- [ ] Can find the release that introduced a FortiSIEM feature.
- [ ] Can map a FortiSIEM feature to its CLS, NDM, or GPOS requirement.
- [ ] Can find the GUI pane or command that meets the requirement.
- [ ] Can collect FortiSIEM's evidence and record the requirements it
  cannot meet exactly.
