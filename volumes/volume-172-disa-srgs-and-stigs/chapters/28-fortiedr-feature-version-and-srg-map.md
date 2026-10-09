# Chapter 28: FortiEDR Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiEDR release, and where it matters the Central Manager or
  Core build, that introduced a given feature.
- Map each FortiEDR feature to the Network Device Management (NDM) SRG,
  Unified Endpoint Management (UEM) Server or Agent SRG, or Intrusion
  Detection and Prevention Systems (IDPS) SRG requirement it helps satisfy.
- Explain why the NDM SRG covers the Central Manager console, why the UEM
  SRGs cover the Collector's management channel, why the IDPS SRG covers
  the malicious code protection, and where the host operating system STIGs
  take over.
- Find the Central Manager pane or the documented command that configures
  each feature to meet its requirement.
- Use the map to scope an SRG-based assessment of FortiEDR, which has no
  STIG of its own.
- Record the requirements that FortiEDR cannot meet exactly, with their
  mitigations.

## Theory and Architecture

FortiEDR is Fortinet's endpoint detection and response (EDR) platform. It
detects and blocks malicious files, malicious outbound connections, and
ransomware behavior on endpoints, records endpoint activity for threat
hunting and forensics, and responds to incidents automatically. Its
distributed architecture has these parts, as the Administration Guide
describes them:

- **Collector.** The agent on each Windows, macOS, or Linux device (with
  separate mobile Collectors for Android and iOS from 7.0, and a node
  Collector for cloud workloads). It registers with the Aggregator over SSL,
  receives its configuration from the Aggregator, sends security events to
  the Aggregator and activity events to the Core, and by default analyzes
  activity locally (autonomous mode). Stopping the Collector service, and
  uninstalling the Collector, require the device registration password.
- **Core.** The Linux-based policy enforcer and decision maker, which
  analyzes the metadata that the Collectors send, and in its *Jumpbox* role
  connects to LDAP servers and integrated systems.
- **Aggregator.** A proxy for the Central Manager: Collectors and Cores
  register with it, report health and events through it, and receive the
  policies, rules, and exceptions defined in the Central Manager from it.
- **Central Manager.** The only component with a user interface: the web
  console in which administrators configure the system, handle incidents,
  run forensics and threat hunting, and monitor system health.
- **Threat Hunting Repository** (the activity event store) and the
  **FortiEDR Cloud Service (FCS)**, which reclassifies events with cloud
  analysis and drives automated exceptions and playbook actions.

FortiEDR is delivered in two ways. In **FortiEDR Cloud**, Fortinet hosts
the Central Manager, Aggregator, Core, and repository, and the customer
provisions the environment from FortiCloud and installs only the
Collectors. In an **on-premises deployment**, the customer installs the
Central Manager, Aggregator, Threat Hunting Repository, reputation server,
and Core as virtual machines from Fortinet ISO images, configures each with
the `fortiedr config` installer, and manages them with the `fortiedr`
command line (Appendix C of the Administration Guide; Appendix D adds
air-gapped environments from 7.2.3). The console and its settings are the
same in both, except for the settings that only exist on the server side.

FortiEDR has **no DISA STIG** (Chapter 10), so it is assessed against SRGs,
as described in Chapter 03. Chapter 10 assigns the **host operating system
STIG** to the agents and **NDM and application requirements** to the
management console. For every FortiEDR feature this chapter gives **which
FortiEDR release introduced it**, **which requirement it relates to**, and
**which pane or command configures it to meet that requirement**.

### Where the version data comes from

Fortinet publishes no Feature Matrix and no New Features Guide for
FortiEDR. The best available source is the **release notes**:
docs.fortinet.com lists FortiEDR documentation for the 4.1, 4.2, 5.0, 5.1,
5.2, 6.0, 6.2, 7.0, and 7.2 trains (no later train), with release notes for
**5.0.1, 5.0.2, 5.0.3, 5.1.0, 5.2.0, 5.2.1, 6.0, 6.2, 7.0, 7.2.0, 7.2.1,
and 7.2.3**. This chapter covers the 5.0 train, the oldest train of the
current 5.x, 6.x, and 7.x numbering, through 7.2.3; the 4.1 and 4.2
release notes are older PDF documents and were not used. The version
column was built with these rules:

- The online release notes from 5.0.3 have a *What's new* page. In the
  5.2.0, 6.0, 6.2, 7.0, and 7.2.3 release notes that page is split into a
  page per build (the *GA build*, then later *Central Manager - Build*
  and *Core - Build* pages), because Fortinet adds features to a train by
  new Central Manager or Core builds rather than by new release notes. Each
  feature heading of a *What's new* page or build page is one entry,
  with the release and, for a build page, the build.
- The 5.0.1 and 5.0.2 release notes are PDF documents with the same
  *Version Highlights* list. Those ten features are entered as 5.0.1. The
  5.0.3 *What's new* page repeats them and adds three Central Manager build
  features and one feature with no build (customized cross-platform
  eXtended incident response), which are entered as 5.0.3.
- The 7.0 *GA build* page lists nine features, each on its own page; each
  is one entry. Sub-topics of one heading (the two parts of the 7.2.1 *GUI
  enhancements* list, for example) are folded into their entry, but the
  three parts of the 6.0 GA *Threat Hunting enhancements* (macOS support,
  the Threat Intelligence Feed connector, and query conversion) are
  separate entries, because they are separate features.
- The trains overlap: a feature added by a late build of one train is
  sometimes listed again in another train (revoking a compromised
  registration password in 5.2.0 build 3192 and 6.0 build 6.0.1.0723, for
  example). Each listing is its own entry, and the map merges them into one
  row with the first release in each train.

That gives 127 entries: 14 in 5.0 (10 in 5.0.1 and 4 in 5.0.3), 8
in 5.1.0, 27 in 5.2 (19 in 5.2.0 and 8 in 5.2.1), 18 in 6.0, 27 in 6.2, 10
in 7.0, and 23 in 7.2 (7 in 7.2.0, 6 in 7.2.1, and 10 in 7.2.3). Each entry
title was taken from the release notes and shortened where needed.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: the
  Collector and its registration, the Aggregator and Core, the Central
  Manager console, its users, roles, two-factor, LDAP, and SAML
  authentication, the Audit Trail, system events, syslog and email export,
  installation, updates, the security policies, playbooks, exceptions and
  exclusions, communication control, integrations, and inventory. Each one
  is described in the **FortiEDR 5.0.0 Installation and Administration
  Guide**, so it existed at the start of the 5.0 train and is not in the
  *What's new* lists.
- **New features** are the 127 entries of the release notes,
  merged into 90 rows. The categories were assigned for this chapter.

| Version entry | Meaning |
| --- | --- |
| `5.0.0 or earlier` | A core feature described in the FortiEDR 5.0.0 Installation and Administration Guide |
| `5.1.0 and later` | Introduced in that release (listed on its *What's new* page or in the 5.0.1 *Version Highlights*); later releases include it |
| `5.2.0 GA and later` | Introduced in the GA build of that train |
| `5.2.0 (CM build 2387) and later` | Introduced by that Central Manager (CM) build of the train; the 5.0 and 5.2 release notes give short build numbers, the 6.x and 7.x release notes full ones such as `6.2 (CM 6.2.4.0026)` |
| `6.0 (Core 6.0.1.0646) and later` | Introduced by that Core build |
| `5.2.0 (CM build 3192)+; 6.0 (CM 6.0.1.0723)+` | Listed in each of those trains; the first release or build listed in each train is shown |

Four cautions apply. First, many features also need a minimum **Collector**
version, which is numbered separately from the Central Manager (host
firewall policies need Collector 6.1, the Collector Settings policy
Collector 6.2, for example); the release notes and the Administration
Guide say which, so check the Collector version as well as the console.
Second, several build features are enabled only through Fortinet Support
(the SSL connection between Collector and Core, exceptions for command
execution, the Degraded Collector system event, and the legacy Forensics
view). Third, a row records when Fortinet first listed a feature, which is
not always when it first existed: the 5.0.0 guide already has an
on-premises appendix, while the release notes list on-premises deployment
for 5.2.0 Central Manager build 2325. Fourth, a row records a capability,
but its pane and command were checked against the 7.2.3 Administration
Guide; earlier releases name some panes differently (*Administration >
Tools* became *Administration > Settings* in 7.0, *Event Viewer* became
*Incidents*, and *Security Settings* became *Profiles*).

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The Central Manager console's management plane: users, roles, authentication, password policy, sessions, the Audit Trail, syslog, certificates, time, software updates, and the `fortiedr` command line of on-premises components (assigned by Chapter 10) |
| **UEM-S** | Unified Endpoint Management Server SRG | V2R6, benchmark date 30 Sep 2026 | The Central Manager, Aggregator, and Core as the managers of the Collectors: the trusted channel to the agents, agent authentication, agent status queries, alerts about agent anomalies, and code signing of Collector updates |
| **UEM-A** | Unified Endpoint Management Agent SRG | V2R2, benchmark date 29 Jun 2026 | The Collector as a managed agent: enrollment, the server it registers with, preventing unenrollment, and sending endpoint activity to a server |
| **IDPS** | Intrusion Detection and Prevention Systems SRG | V3R4, benchmark date 28 Oct 2025 | The protection function: blocking and quarantining malicious code, alerts, protection updates, monitoring of endpoint connections, detection records, and integration with the monitoring architecture |

Chapter 10 names the host operating system STIG for the agents and NDM
and application requirements for the console. The other two SRGs were
chosen because each fits a part of FortiEDR that the NDM SRG does not
reach, and each is used only for that part:

- **NDM for the console.** The NDM SRG is the closest match for how the
  Central Manager is administered: it has the account, authentication,
  session, audit, and cryptography requirements that the console settings
  address, and its requirement to disable unnecessary functions
  (NDM `SRG-APP-000142-NDM-000245`) is used for every row with no direct
  requirement. The UEM Server SRG has requirements for the same
  administrative topics, but the map takes those from the NDM SRG only, so
  that each setting is assessed once.
- **UEM for the Collector channel.** The UEM SRGs, which Chapter 27 used
  for FortiClient and EMS, describe a server that enrolls agents, pushes
  configuration to them, and queries their state, and an agent that accepts
  that management. FortiEDR is not a unified endpoint management product:
  it does not deploy software or manage device settings, so most UEM
  requirements do not apply. The parts that do fit are the agent's
  enrollment (UEM-A `SRG-APP-000516-UEM-100010`), recording the server it
  enrolled with (UEM-A `SRG-APP-000516-UEM-100006`), preventing
  unenrollment, which the registration password does
  (UEM-A `SRG-APP-000516-UEM-100011`), sending endpoint activity to a
  server (UEM-A `SRG-APP-000358-UEM-100013`), and, on the server side, the
  trusted channel to the agents (UEM-S `SRG-APP-000191-UEM-000119`,
  UEM-S `SRG-APP-000395-UEM-000266`, UEM-S `SRG-APP-000439-UEM-000313`),
  agent authentication (UEM-S `SRG-APP-000580-UEM-000398`), agent status
  queries (UEM-S `SRG-APP-000472-UEM-000347`), alerts about anomalies
  (UEM-S `SRG-APP-000474-UEM-000349`), and code signing of agent updates
  (UEM-S `SRG-APP-000427-UEM-000299`).
- **IDPS for the protection function.** DISA has no SRG for endpoint
  protection or EDR products. The IDPS SRG, which Chapter 21 used for
  FortiSandbox, has the malicious code requirements that describe what the
  FortiEDR security policies do: blocking malicious code
  (IDPS `SRG-NET-000249-IDPS-00176`) or quarantining it
  (IDPS `SRG-NET-000249-IDPS-00221`), an immediate alert when it is
  detected (IDPS `SRG-NET-000249-IDPS-00222`), alerts to the ISSM and ISSO
  (IDPS `SRG-NET-000392-IDPS-00214`, IDPS `SRG-NET-000392-IDPS-00219`),
  automatic protection updates (IDPS `SRG-NET-000246-IDPS-00205`,
  IDPS `SRG-NET-000251-IDPS-00178`, IDPS `SRG-NET-000019-IDPS-00187`), and
  the content and off-loading of detection records. Its monitoring
  requirements (IDPS `SRG-NET-000390-IDPS-00212`,
  IDPS `SRG-NET-000391-IDPS-00213`, IDPS `SRG-NET-000018-IDPS-00018`, and
  IDPS `SRG-NET-000384-IDPS-00209`) fit the Exfiltration Prevention policy,
  communication control, and the host firewall, which watch and block
  connections at the endpoint rather than in the network. The IDPS
  requirements written for an inline network sensor (denial-of-service,
  ICMP, and injection attacks, fragmented packets, and blocking at the
  enclave boundary) are left out. The UEM SRGs were considered for this
  function and rejected: they have no malicious code requirements.

**The host operating systems.** None of these SRGs covers the operating
system of an endpoint, and the map does not cite operating system rules
row by row. As Chapter 10 says, each endpoint with a Collector is assessed
against **its own operating system STIG** (Windows 11, Windows Server,
macOS, RHEL, Ubuntu, and so on). Those STIGs carry the endpoint's own
requirements for antivirus or endpoint security software, firewalls, USB
control, and disk encryption, which FortiEDR's Execution Prevention policy,
host firewall, Device Control policy, and disk encryption management may
help meet; they are assessed there. In an on-premises deployment, the
Central Manager and Core are Ubuntu 22.04 virtual machines built from
Fortinet images (Core build 6.0.1.0646 moved the Core from CentOS, and
Central Manager build 6.2.1.0111 added migration to Ubuntu), so assess
each host against the **Ubuntu 22.04 LTS STIG** as far as Fortinet's image
allows, and record the deviations. The map has one row for this (NDM
`SRG-APP-000516-NDM-000317`, configuration according to DoD guidance,
including STIGs). In FortiEDR Cloud the back end is a Fortinet-hosted
service: confirm its authorization and impact level under the Cloud
Computing SRG (Chapter 08) before use, and assess the console settings
with this map.

The requirement IDs are the **rule version IDs** from the XCCDF files,
and the severity is the rule's severity (high = CAT I, medium = CAT II,
low = CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiEDR meets a
  requirement. The Execution Prevention policy implements the requirement
  to block malicious code (IDPS `SRG-NET-000249-IDPS-00176`), and the
  registration password prompt implements the requirement to prevent
  unenrollment (UEM-A `SRG-APP-000516-UEM-100011`), for example.
- **Must be configured to meet a requirement.** The feature is in scope
  of a requirement and has to be set up correctly. The password policy
  must require 15 characters (NDM `SRG-APP-000164-NDM-000252`), and each
  security policy must be in Protection mode, for example.
- **No direct requirement.** The feature is operational, such as a
  dashboard, a localization, a GUI change, a licensing change, or an
  analysis view. It has no requirement of its own, but if it is not needed
  it falls under the NDM requirement to disable unnecessary functions
  (NDM `SRG-APP-000142-NDM-000245`). 59 rows are of this kind.

The mapping is a starting point for an assessment, not a ruling. Confirm
it with your assessor, especially the use of the UEM and IDPS SRGs for a
product that is neither a UEM server nor a network IDPS.

### Where the commands come from

FortiEDR is configured in the Central Manager GUI, and it has no CLI
Reference. The command column was therefore built from the **FortiEDR
7.2.3 Administration Guide**, the newest release: its chapters for every
GUI pane and field, *Deploying FortiEDR Collectors* for the Collector
command lines, and *Appendix C* for the `fortiedr` command line of the
on-premises components (the *FortiEDR CLI commands* table). The check was
automatic: each GUI pane had to appear in the guide's text or be a heading
path of its outline (chapter, section, and subsection), each field label
in parentheses had to appear in the guide, each `fortiedr` command had to
be a basic action of the table or a component of its
`fortiedr {edr|aggregator|core|manager|activemq}` syntax followed by a
command in the table, and each other command had to appear in the guide
with its placeholders. All 83 GUI panes, 45 field labels, and 8 commands
passed. Read the column this way:

- **GUI:** entries name the console pane (*menu > page > section*); the
  text in parentheses names the fields to set, with the value where it
  matters. A third level that is a section of a page (such as
  *Administration > Settings > Audit Trail* or *Administration > Users >
  LDAP authentication*) is a section or tab of that page.
- Commands in backticks are entered on the endpoint (`msiexec` on
  Windows, `fortiedrconfig.sh` on Linux) or, for `fortiedr`, as root on an
  on-premises Central Manager, Aggregator, or Core. Values in
  `<ANGLE_BRACKETS>` are placeholders. Statements are separated by `;` to
  fit in a table cell; enter each one on its own line.
- For **"No direct requirement"** rows, the entry shown is where the
  feature is turned off or left unconfigured when it is unused. A dash
  (**—**) means there is nothing to change: the feature is a GUI change, a
  licensing or platform change, an analysis view, or a capability that does
  nothing until it is configured or licensed.

Some requirements cannot be met exactly with FortiEDR settings. Record
them on the checklist as open findings with mitigations, or meet them
another way:

- **Login banner.** The Administration Guide documents no logon banner
  for the Central Manager console (NDM `SRG-APP-000068-NDM-000215`). Log
  administrators on through SAML with an identity provider that shows the
  DoD notice and consent banner, and record the finding for the local
  logon page.
- **FIPS-validated cryptography.** The guides document no FIPS mode for
  the Central Manager, the back-end components, or the Collector, and cite
  no FIPS 140 validation (NDM `SRG-APP-000179-NDM-000265`, UEM-A
  `SRG-APP-000555-UEM-100014`, CAT I). Ask Fortinet for the validation
  status of the release you deploy, rely on validated modules of the host
  operating system where they apply, and record the finding.
- **Password policy.** The password policy sets a minimum length, but its
  complexity option requires three of the four character types rather than
  all four (NDM `SRG-APP-000166-NDM-000254`, NDM
  `SRG-APP-000167-NDM-000255`, NDM `SRG-APP-000168-NDM-000256`, NDM
  `SRG-APP-000169-NDM-000257`), and the guide documents no rule for the
  number of changed characters or for password storage (NDM
  `SRG-APP-000170-NDM-000329`, NDM `SRG-APP-000171-NDM-000258`, CAT I).
  Set the minimum length to 15, enable the complexity option, require all
  four types by procedure, and keep local accounts to the account of last
  resort.
- **Lockout.** Brute-force protection blocks a user after **five** failed
  logons in the console or REST API, and the user stays blocked until an
  administrator resets the password, while the requirement is three
  attempts (NDM `SRG-APP-000065-NDM-000214`). Enable brute-force
  protection, let the directory or identity provider enforce three
  attempts for LDAP and SAML users, and record the difference for local
  users.
- **Multifactor authentication.** Two-factor authentication uses
  FortiToken or an authenticator application, not DoD PKI (NDM
  `SRG-APP-000149-NDM-000247`, CAT I). Use SAML with an identity provider
  that enforces CAC for all administrators, and require 2FA for the local
  account of last resort.
- **Session timeout.** The idle session timeout is set in Hoster view
  (1 to 1440 minutes, 15 by default) and does not apply to the Dashboard
  tab (NDM `SRG-APP-000190-NDM-000267`, CAT I). Set it to 5 minutes, and
  for FortiEDR Cloud ask Fortinet Support where your environment does not
  show the setting.
- **Audit content.** The Audit Trail records user actions (policy,
  forensic, administrative, event, and inventory actions, and system health
  changes) with date, subsystem, user, and description, but the guide does
  not say that it records logons or failed logons, its time stamps carry no
  time zone, the console downloads at most 30 days at a time, and Personal
  Data Handling replaces a removed user's details in the Audit Trail with
  `GDPR_ANONYMIZE` (NDM `SRG-APP-000503-NDM-000320`, NDM
  `SRG-APP-000374-NDM-000299`, NDM `SRG-APP-000120-NDM-000237`). Send the
  audit trail to syslog, keep it in the central log server, restrict
  Personal Data Handling to Admin users, and check the records during the
  assessment.
- **Signed policies.** The UEM SRGs require the server to sign policies
  and the agent to accept only signed policies (UEM-S
  `SRG-APP-000427-UEM-000500`, CAT I, and UEM-A
  `SRG-APP-000427-UEM-100007`). The guide documents no signing: the
  Aggregator distributes configuration to Collectors and Cores, and the
  Collector registers with the Aggregator over SSL. Record the finding.
- **Agent channel and authentication.** All Collectors share one
  registration password, which is not the cryptographic bidirectional
  authentication the UEM Server SRG requires (UEM-S
  `SRG-APP-000580-UEM-000398`, UEM-S `SRG-APP-000395-UEM-000266`, CAT I),
  and the SSL connection between Collector and Core is enabled only through
  Fortinet Support (5.2.0 build 3092). Ask Fortinet Support to enable SSL
  for the Core channel, revoke the registration password when it may be
  compromised, generate new custom Collector installers after a revocation,
  and record the finding.
- **Time.** Date, time, and time zone are set at installation, and the
  guide documents no NTP or time-source setting for the on-premises
  components (NDM `SRG-APP-000920-NDM-000320`). Configure time
  synchronization on the Ubuntu host as the Ubuntu STIG requires, and for
  FortiEDR Cloud rely on Fortinet's service.
- **Backups.** The guide documents replication of Threat Hunting
  Repository data to an NFS server, but no backup of the Central Manager
  configuration (NDM `SRG-APP-000516-NDM-000340`). Back up the on-premises
  virtual machines with the hypervisor, export policy-related lists where
  the console allows (exclusion lists, application lists), and record the
  finding.
- **Software verification.** Back-end upgrades run installer files that
  Fortinet provides, and the guide describes no signature check before an
  upgrade (NDM `SRG-APP-000131-NDM-000243`). Check each file's hash with
  Fortinet before you run it. The Collector packages are code signed (the
  5.0 release notes mention the strong ciphers with which the Collector is
  signed), which supports UEM-S `SRG-APP-000427-UEM-000299`.
- **Cloud services.** FCS sends event data to Fortinet's cloud (from
  Central Manager build 6.2.4.0026 with user names, host names, addresses,
  and other fields obfuscated), and Collectors query the cloud reputation
  service. Use them only when the authorizing official approves, answer
  no at the FCS prompt of `fortiedr config` otherwise, and use the
  on-premises reputation server and the air-gapped deployment where
  required (NDM `SRG-APP-000142-NDM-000245`).
- **No STIG.** Without a STIG there is no DoD baseline for FortiEDR itself;
  use this map, the NDM, UEM, and IDPS SRGs, and the operating system STIGs
  as the baseline, and record the settings that differ from it.

## Design Considerations

- **Pick the releases first, then the features.** If your design depends
  on a feature introduced in a certain release or build (the password
  policy in 6.0, the idle session timeout in 5.2.0 build 2387, host
  firewall and disk encryption in 7.2.0, the AV Signature policy and
  air-gapped deployment in 7.2.3), that sets the minimum Central Manager
  release and, often, a minimum Collector version, and both must be
  vendor-supported (NDM `SRG-APP-001035-NDM-000340`).
- **Choose cloud or on-premises deliberately.** FortiEDR Cloud moves the
  back-end hosts, their operating system STIG, and their backups to
  Fortinet, but needs a Cloud Computing SRG decision; on-premises keeps
  everything in your boundary but adds the Ubuntu hosts, the `fortiedr`
  command line, and the backups to your assessment.
- **Put every endpoint in Protection mode.** FortiEDR ships with every
  security policy in Simulation mode. Assign each Collector group a policy
  set, move the Execution Prevention, Exfiltration Prevention, and
  Ransomware Prevention policies to Protection after the acquaintance
  period, and keep exceptions and exclusions narrow and reviewed.
- **Protect the registration password.** It installs, stops, and
  uninstalls Collectors; keep it out of users' hands, embed it in custom
  installers, and revoke it when it may be compromised.
- **Log administrators on through SAML with CAC.** Map identity provider
  groups to the Admin, Senior Analyst, Analyst, IT, and Read-Only roles,
  keep one local Admin as the account of last resort with 2FA, and grant
  REST API, custom script, and FortiEDR Connect permissions only to the
  users who need them.
- **Send events out.** Send security events, system events, and the
  audit trail to FortiAnalyzer or a SIEM over TCP with TLS, and email
  security and system events to the ISSO through distribution lists and
  playbooks.
- **Turn off what is not used.** Leave FortiEDR Connect, IoT discovery,
  the secure browser, and unused connectors off, and disable FCS and cloud
  reputation where they are not approved.

## Implementation and Automation

### The FortiEDR feature map

The SRG column uses the abbreviations defined in *Where the SRG data comes
from*: **NDM** is the Network Device Management SRG, **UEM-S** the UEM
Server SRG, **UEM-A** the UEM Agent SRG, and **IDPS** the Intrusion
Detection and Prevention Systems SRG. The requirement titles are listed in
the next table. The command column follows the conventions in *Where the
commands come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/28-fortiedr-feature-version-and-srg-map-feature-map.csv) (143 rows).

| Category | Feature | Introduced (FortiEDR) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Architecture | Collector on Windows, macOS, and Linux endpoints (the host operating system STIG applies to each endpoint) | 5.0.0 or earlier | UEM-A `SRG-APP-000516-UEM-100010`; UEM-A `SRG-APP-000516-UEM-100006` | `msiexec /i FortiEDRCollectorInstaller64.msi /qn AGG=<AGGREGATOR>:8081 PWD=<REGISTRATION_PASSWORD>`; `sudo /opt/FortiEDRCollector/scripts/fortiedrconfig.sh` |
| Core: Architecture | Custom Collector installer with the Aggregator address, organization, and group embedded | 5.0.0 or earlier | UEM-A `SRG-APP-000516-UEM-100010`; UEM-A `SRG-APP-000516-UEM-100006` | GUI: Administration > Deployment > Collector (Request Collector Installer, Aggregator Address) |
| Core: Architecture | Device registration password for Collectors, Aggregators, and Cores (also needed to uninstall a Collector) | 5.0.0 or earlier | UEM-A `SRG-APP-000516-UEM-100011`; UEM-S `SRG-APP-000580-UEM-000398` | GUI: Administration > Settings > Component Authentication (keep the password secret; endpoint users must not know it) |
| Core: Architecture | Aggregator and Core (cloud-hosted, or on-premises appliances), and the Collector communication channel | 5.0.0 or earlier | UEM-S `SRG-APP-000191-UEM-000119`; UEM-S `SRG-APP-000439-UEM-000313` | Use SSL between Collector and Core (see the 5.2.0 build 3092 row) |
| Core: Architecture | Network ports between Collectors, Aggregator, Core, Central Manager, and Threat Hunting Repository | 5.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245` | Open only the documented ports, narrowed to the component addresses |
| Core: Architecture | FortiEDR Cloud Service (FCS) classification and analysis | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `fortiedr config` (answer no at the Do you want to enable FCS? prompt if FCS is not approved) |
| Core: Architecture | Threat Hunting Repository (on-premises) | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Architecture | Multi-tenancy (organizations) and Hoster view | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Console | Central Manager console over HTTPS (port 443) | 5.0.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000172-NDM-000259` | Browse to https://<CENTRAL_MANAGER>/ only; restrict port 443 to the management network |
| Core: Console | Central Manager server certificate (PEM, CN matching the FQDN) | 5.0.0 or earlier | NDM `SRG-APP-000516-NDM-000344` | GUI: Administration > Deployment > Collector (Central Manager Certificate); `fortiedr manager load-ssl-certificate <USER> <PASSWORD> <CERTIFICATE_FILE> <PRIVATE_KEY_FILE> <PRIVATE_KEY_PASSWORD>` (certificate from a DoD-approved CA) |
| Core: Console | Trusted CA certificates of the Central Manager (MITM CA upload for Internet access) | 5.0.0 or earlier | NDM `SRG-APP-000910-NDM-000300` | Upload only approved CAs with the /maintenance/upload-certificate API |
| Core: Accounts | Local console users and predefined roles | 5.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287`; NDM `SRG-APP-000340-NDM-000288` | GUI: Administration > Users (Add User, Role) |
| Core: Accounts | First administrator defined at installation (account of last resort) | 5.0.0 or earlier | NDM `SRG-APP-000148-NDM-000346` | GUI: Administration > Users (keep one local Admin; log on everyone else through LDAP or SAML) |
| Core: Accounts | Rest API, Custom script, and FortiEDR Connect user permissions | 5.0.0 or earlier | NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000231-NDM-000271` | GUI: Administration > Users (Rest API, Custom script, FortiEDR Connect) |
| Core: Accounts | Resetting a user password and releasing a locked account | 5.0.0 or earlier | NDM `SRG-APP-000065-NDM-000214` | GUI: Administration > Users > Resetting a user password |
| Core: Authentication | Two-factor authentication for a user (FortiToken or an authenticator application) | 5.0.0 or earlier | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000156-NDM-000250` | GUI: Administration > Users > Two-factor authentication |
| Core: Authentication | LDAP authentication (Active Directory or OpenLDAP through a Jumpbox Core) | 5.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000172-NDM-000259` | GUI: Administration > Users > LDAP authentication (LDAP Enabled, Security Level: TLS, Role/Group mapping) |
| Core: Authentication | SAML authentication (FortiEDR as service provider with FortiAuthenticator, Okta, or another IdP) | 5.0.0 or earlier | NDM `SRG-APP-000149-NDM-000247`; NDM `SRG-APP-000516-NDM-000336` | GUI: Administration > Users > SAML authentication (use an IdP that enforces CAC) |
| Core: Audit | Audit Trail of user actions (CSV download, sent through syslog) | 5.0.0 or earlier | NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000027-NDM-000209`; NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000100-NDM-000230` | GUI: Administration > Settings > Audit Trail |
| Core: Audit | System events (component, Collector, license, and mode changes; FCS connectivity) | 5.0.0 or earlier | UEM-S `SRG-APP-000474-UEM-000349` | GUI: Administration > System events; GUI: Administration > Distribution lists |
| Core: Audit | Personal Data Handling (removal of a user's data, including from the Audit Trail) | 5.0.0 or earlier | NDM `SRG-APP-000120-NDM-000237` | GUI: Administration > Settings > Personal Data Handling (restrict to Admin users; record each removal) |
| Core: Logging | Syslog destinations for security events, system events, and the audit trail | 5.0.0 or earlier | NDM `SRG-APP-000516-NDM-000350`; NDM `SRG-APP-000515-NDM-000325`; IDPS `SRG-NET-000511-IDPS-00012`; IDPS `SRG-NET-000091-IDPS-00193` | GUI: Profiles > Export settings > Syslog (Protocol: TCP, TLS, Client Certificate) |
| Core: Logging | SMTP server and distribution lists (email for security and system events) | 5.0.0 or earlier | IDPS `SRG-NET-000249-IDPS-00222`; IDPS `SRG-NET-000392-IDPS-00214` | GUI: Profiles > Export settings > SMTP; GUI: Administration > Distribution lists |
| Core: Logging | Open Ticket (events sent to Jira, ServiceNow, or another tool by email) | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Profiles > Export settings > Open Ticket |
| Core: Platform | Central Manager, Aggregator, and Core installation and upgrade with Fortinet installer files | 5.0.0 or earlier | NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-000131-NDM-000243` | `fortiedr version` (install the installer files that Fortinet provides, after checking them) |
| Core: Platform | The fortiedr command line of the Central Manager, Aggregator, Core, and Repository | 5.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000378-NDM-000302` | `fortiedr status` (restrict root and SSH access to authorized administrators) |
| Core: Platform | Date, time, and time zone set by the installer | 5.0.0 or earlier | NDM `SRG-APP-000116-NDM-000234`; NDM `SRG-APP-000374-NDM-000299`; NDM `SRG-APP-000920-NDM-000320` | `fortiedr tzselect` (synchronize the host clock with an authoritative time source) |
| Core: Platform | Licensing page and license loading | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Administration > Licensing |
| Core: Platform | Collector version updates and automatic Collector updates | 5.0.0 or earlier | UEM-S `SRG-APP-000427-UEM-000299`; NDM `SRG-APP-000378-NDM-000302` | GUI: Administration > Deployment > Collector (Update Collectors) |
| Core: Platform | Content updates (policy rules and built-in exceptions, Content Updates add-on) | 5.0.0 or earlier | IDPS `SRG-NET-000246-IDPS-00205`; IDPS `SRG-NET-000251-IDPS-00178`; IDPS `SRG-NET-000019-IDPS-00187` | GUI: Administration > Licensing (Load Content) |
| Core: Platform | Exporting logs of Collectors, Cores, and Aggregators (diagnostics) | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Protection | Security policies assigned to Collector groups | 5.0.0 or earlier | IDPS `SRG-NET-000512-IDPS-00194` | GUI: Profiles > Security > Policies (assign every Collector group a policy set) |
| Core: Protection | Protection or Simulation mode of each policy | 5.0.0 or earlier | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Profiles > Security > Policies (Protection) |
| Core: Protection | Execution Prevention policy (malicious file detection and blocking, NGAV) | 5.0.0 or earlier | IDPS `SRG-NET-000249-IDPS-00176`; IDPS `SRG-NET-000249-IDPS-00221` | GUI: Profiles > Security > Policies (Execution Prevention) |
| Core: Protection | Exfiltration Prevention policy (malicious connection establishment) | 5.0.0 or earlier | IDPS `SRG-NET-000391-IDPS-00213`; IDPS `SRG-NET-000249-IDPS-00176` | GUI: Profiles > Security > Policies (Exfiltration Prevention) |
| Core: Protection | Ransomware Prevention policy | 5.0.0 or earlier | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Profiles > Security > Policies (Ransomware Prevention) |
| Core: Protection | Device Control policy (USB devices) | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Profiles > Security > Policies (Device Control) |
| Core: Protection | File Scan (scheduled and on-demand scans) | 5.0.0 or earlier | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Administration > Settings > File Scan (Perform scheduled scan) |
| Core: Protection | Exception Manager and Exclusion Manager | 5.0.0 or earlier | IDPS `SRG-NET-000512-IDPS-00194`; NDM `SRG-APP-000380-NDM-000304` | GUI: Profiles > Security > Exception Manager; GUI: Profiles > Security > Exclusion Manager (review exceptions and exclusions) |
| Core: Protection | Device isolation | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Protection | Enabling and disabling a Collector | 5.0.0 or earlier | NDM `SRG-APP-000340-NDM-000288` | GUI: Assets > Inventory > Enabling/disabling a Collector |
| Core: Response | Playbook policies (notifications, isolation, high-security group, remediation) | 5.0.0 or earlier | IDPS `SRG-NET-000249-IDPS-00222`; IDPS `SRG-NET-000392-IDPS-00219` | GUI: Profiles > Playbooks (Send Email Notification, Send Syslog Notification) |
| Core: Response | Remediating a device upon malware detection (delete file, terminate process, clean registry) | 5.0.0 or earlier | IDPS `SRG-NET-000249-IDPS-00221` | GUI: Incidents > Investigation View > Remediating a device upon malware detection |
| Core: Response | Event Viewer (security events, classification, handled status) | 5.0.0 or earlier | IDPS `SRG-NET-000113-IDPS-00013`; IDPS `SRG-NET-000113-IDPS-00082`; IDPS `SRG-NET-000074-IDPS-00059` | GUI: Incidents |
| Core: Response | Forensics (flow analyzer, stack view, compare view, memory retrieval) | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Communication control | Application communication control (reputation, vulnerability, allow or deny policies) | 5.0.0 or earlier | IDPS `SRG-NET-000384-IDPS-00209`; IDPS `SRG-NET-000391-IDPS-00213`; IDPS `SRG-NET-000018-IDPS-00018` | GUI: Communication control > Policies; GUI: Communication control > Applications |
| Core: Integrations | Connectors (firewall, NAC, sandbox, eXtended detection, custom) and Jumpbox Cores | 5.0.0 or earlier | IDPS `SRG-NET-000383-IDPS-00208` | GUI: Profiles > Integrations > Connectors |
| Core: Integrations | IP sets | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Inventory | Collector inventory, states, and versions | 5.0.0 or earlier | UEM-S `SRG-APP-000472-UEM-000347` | GUI: Assets > Inventory |
| Core: Inventory | Unmanaged devices | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Inventory | IoT device discovery | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Administration > Settings > IoT Device Discovery (Perform ongoing device discovery: off) |
| Core: Inventory | Dashboard and executive summary report | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Endpoint | End-user notifications (tray icon and pop-ups) | 5.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| XDR | FortiXDR extended detection, investigation, and response, with the event advanced analysis view of the automated FCS analysis | 5.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat hunting | Behavior-based threat hunting with MITRE techniques, collection profiles, and collection exclusions | 5.0.1 and later | UEM-A `SRG-APP-000358-UEM-100013` | GUI: Profiles > EDR > Collection Profiles; GUI: Profiles > EDR > Collection Exclusions |
| Threat hunting | Scheduled threat hunting queries, and incident response actions triggered by them | 5.0.1+; 5.2.1+ | IDPS `SRG-NET-000392-IDPS-00214` | GUI: Forensics > Threat Hunting |
| Protection | Web filtering powered by FortiGuard | 5.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Protection | Security event exception enhancements (user-based exceptions) | 5.0.1 and later | IDPS `SRG-NET-000512-IDPS-00194` | GUI: Profiles > Security > Exception Manager |
| Platform | Oracle Linux Collector support | 5.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Endpoint | Enhanced end-user notification (recent events, Collector version and state) | 5.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Administration > Settings > End Users Notifications (Show system tray icon with collector status) |
| Endpoint | Windows Security Center registration controlled from the console | 5.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Administration > Settings > Windows Security Center (Register collectors to Windows Security Center) |
| Console administration | REST API additions (threat hunting, enriched events, unmanaged devices, SAML SSO configuration) | 5.0.1 and later | NDM `SRG-APP-000340-NDM-000288` | GUI: Administration > Users (Rest API: off) (for every user who does not need the API) |
| Communication control | Communication Control free-text search covers process properties | 5.0.3 (CM build 827) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Forensics | Forensics > Events available to every role with Forensics permission, regardless of license type | 5.0.3 (CM build 834)+; 5.2.1+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Inventory | Disabling IoT scans (iot.disabled in application.properties on premises; Fortinet Support for cloud) | 5.0.3 (CM build 834)+; 5.2.0 (CM build 2162)+ | NDM `SRG-APP-000142-NDM-000245` | Set iot.disabled in application.properties |
| Integrations | Custom cross-platform eXtended incident response and pre-canned third-party integrations triggered by playbooks | 5.0.3+; 5.2.0 GA+ | IDPS `SRG-NET-000383-IDPS-00208` | GUI: Profiles > Integrations > Connectors; GUI: Profiles > Playbooks |
| Protection | Application Control: blocklist of applications per Collector group, by hash, name, path, or signer, predefined application groups, and the Application Name field | 5.1.0+; 5.2.0 GA+; 6.2 GA+ | IDPS `SRG-NET-000249-IDPS-00176`; IDPS `SRG-NET-000512-IDPS-00194` | GUI: Profiles > Security > Application Control |
| Threat hunting | Threat hunting for Linux and macOS | 5.1.0+; 6.0 GA+ | UEM-A `SRG-APP-000358-UEM-100013` | GUI: Profiles > EDR > Collection Profiles |
| Protection | Process exclusions and NGAV exclusions, and exporting and importing exclusion lists | 5.1.0+; 6.2 GA+ | IDPS `SRG-NET-000512-IDPS-00194`; NDM `SRG-APP-000380-NDM-000304` | GUI: Profiles > Security > Exclusion Manager (exclude only approved, signed processes and paths) |
| Protection | Keylogging activity detection | 5.1.0 and later | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Profiles > Security > Policies |
| Threat hunting | Enhanced data collection, the Collection Profiles and Collection Exclusions terms, and collection exclusions for macOS | 5.1.0+; 6.0 (CM 6.0.1.0723)+ | UEM-A `SRG-APP-000358-UEM-100013` | GUI: Profiles > EDR > Collection Exclusions |
| Platform | FortiEDR serial number on the Licensing page | 5.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Response | FortiEDR Connect (remote shell to Windows devices) | 5.2.0 GA and later | NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000408-NDM-000314` | GUI: Administration > Settings > FortiEDR Connect (leave remote shell off unless needed; grant it per user) |
| Threat hunting | Threat hunting data retention visibility | 5.2.0 GA and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Console administration | Japanese and Chinese localization of the console | 5.2.0 GA+; 7.2.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Syslog additions: remediation details, MITRE techniques, event data, deployment, stack hashes, and stack certificates | 5.2.0 GA+; 6.0 (CM 6.0.1.0940)+ | IDPS `SRG-NET-000074-IDPS-00059`; IDPS `SRG-NET-000091-IDPS-00193` | GUI: Profiles > Export settings > Syslog |
| Platform | On-premises deployment (Central Manager, Aggregator, Threat Hunting Repository, reputation server, and Core) | 5.2.0 (CM build 2325) and later | NDM `SRG-APP-000516-NDM-000317` | `fortiedr config` (assess each host against DoD guidance) |
| Logging | FortiAnalyzer syslog support | 5.2.0 (CM build 2387) and later | NDM `SRG-APP-000516-NDM-000350`; IDPS `SRG-NET-000511-IDPS-00012` | GUI: Profiles > Export settings > Syslog (Format: FAZ) |
| Logging | Client certificate for TLS syslog servers | 5.2.0 (CM build 2387) and later | NDM `SRG-APP-000516-NDM-000350`; NDM `SRG-APP-000516-NDM-000344` | GUI: Profiles > Export settings > Syslog (TLS, Client Certificate) |
| Console administration | Idle session timeout (1 to 1440 minutes, 15 by default; Hoster view) | 5.2.0 (CM build 2387) and later | NDM `SRG-APP-000190-NDM-000267` | GUI: Administration > Settings (Session Time Out: 5) |
| Console administration | REST API tokens valid only for the TCP session (60 seconds idle, 4 hours maximum) | 5.2.0 (CM build 2527) and later | NDM `SRG-APP-000190-NDM-000267` | — |
| Protection | Exceptions for specific command execution (enabled by Fortinet Support) | 5.2.0 (Core 5.2.2.2027) and later | IDPS `SRG-NET-000512-IDPS-00194` | GUI: Profiles > Security > Exception Manager |
| Threat hunting | Changing the default threat hunting collection profile | 5.2.0 (CM build 3092)+; 6.0 (CM 6.0.1.0723)+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Architecture | SSL connection between Collector and Core (enabled by Fortinet Support) | 5.2.0 (CM build 3092) and later | UEM-S `SRG-APP-000191-UEM-000119`; UEM-S `SRG-APP-000395-UEM-000266`; UEM-S `SRG-APP-000439-UEM-000313` | Ask Fortinet Support to enable SSL between Collector and Core |
| Architecture | Revoking a compromised registration password | 5.2.0 (CM build 3192)+; 6.0 (CM 6.0.1.0723)+ | UEM-A `SRG-APP-000516-UEM-100011`; UEM-S `SRG-APP-000580-UEM-000398` | GUI: Administration > Settings > Component Authentication (Advanced Password Management) |
| Inventory | Aggregators listed by their machine names | 5.2.0 (CM build 3192)+; 6.0 (CM 6.0.1.0723)+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Creating a syslog destination through the REST API (all fields and notifications enabled by default) | 5.2.0 (CM build 3192)+; 6.0 (CM 6.0.1.0723)+ | NDM `SRG-APP-000516-NDM-000350` | GUI: Profiles > Export settings > Syslog |
| Protection | Exceptions based on child processes | 5.2.0 (CM build 3192)+; 6.0 (CM 6.0.1.0723)+ | IDPS `SRG-NET-000512-IDPS-00194` | GUI: Profiles > Security > Exception Manager |
| Console administration | Admin, Senior Analyst, Analyst, IT, and Read-Only roles, also mapped to LDAP and SAML groups | 5.2.1 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287`; NDM `SRG-APP-000153-NDM-000249` | GUI: Administration > Users (Role) |
| XDR | eXtended detection sources: Google SCC, Amazon GuardDuty, FortiAnalyzer Cloud, FortiSIEM, FortiSIEM Cloud, FortiGate and VDOM filters, and custom external systems | 5.2.1+; 6.2 GA+; 7.0 GA+ | IDPS `SRG-NET-000383-IDPS-00208` | GUI: Profiles > Integrations > Connectors |
| Integrations | Zero Trust incident response with FortiClient EMS tags, including the predefined FortiEDR tags | 5.2.1+; 6.0 (CM 6.0.1.0723)+ | IDPS `SRG-NET-000383-IDPS-00208` | GUI: Profiles > Integrations > Connectors |
| Integrations | User access incident response (reset a user password, disable an Active Directory account) | 5.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Response | Time filter in the Event Viewer | 5.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Integrations | FortiGate connector with virtual domains, and FortiManager ADOM blocking in workspace mode | 5.2.1+; 6.2 (CM 6.2.4.0026)+ | IDPS `SRG-NET-000383-IDPS-00208` | GUI: Profiles > Integrations > Connectors |
| Response | Investigation View and its enhancements (stacks view, JSON export, response actions, filters) | 6.0 GA+; 6.2 GA+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Threat hunting | Threat Intelligence Feed integration (STIX/TAXII) and query conversion into Lucene | 6.0 GA and later | IDPS `SRG-NET-000383-IDPS-00208` | GUI: Profiles > Integrations > Connectors |
| Console administration | Password policy: minimum length, character types, brute-force protection, required 2FA, and closing open sessions | 6.0 GA and later | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000166-NDM-000254`; NDM `SRG-APP-000167-NDM-000255`; NDM `SRG-APP-000168-NDM-000256`; NDM `SRG-APP-000169-NDM-000257`; NDM `SRG-APP-000065-NDM-000214`; NDM `SRG-APP-000820-NDM-000170` | GUI: Administration > Users (Password Policy, Minimum password length: 15, Brute-force protection, Require 2FA, Close open sessions immediately) |
| Architecture | Organization-specific Aggregators | 6.0 (CM 6.0.1.0723) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Console administration | Getting started videos | 6.0 (CM 6.0.1.0940) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | System event when a Collector becomes Degraded (enabled by Fortinet Support) | 6.0 (CM 6.0.1.0940) and later | UEM-S `SRG-APP-000474-UEM-000349` | Ask Fortinet Support to enable the event |
| Architecture | Reputation service: Core and Windows Collector query it directly | 6.0 (Core 6.0.1.0637)+; 6.2 (CM 6.2.3.0036)+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Administration > Settings > Reputation Service |
| Platform | Core and on-premises components on Ubuntu 22.04 instead of CentOS, and migration | 6.0 (Core 6.0.1.0646)+; 6.2 (CM 6.2.1.0111)+ | NDM `SRG-APP-000516-NDM-000317` | Migrate to Ubuntu 22.04 and assess the host |
| Forensics | Forensics moved into the Investigation View, then the Forensics Viewer restored | 6.2 GA+; 7.2.1+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Response | FortiEDR Connect commands recorded in the Audit Trail | 6.2 GA and later | NDM `SRG-APP-000101-NDM-000231`; NDM `SRG-APP-000343-NDM-000289` | GUI: Administration > Settings > Audit Trail |
| Logging | CEF and LEEF syslog formats | 6.2 GA and later | IDPS `SRG-NET-000091-IDPS-00193` | GUI: Profiles > Export settings > Syslog (Format) |
| Console administration | Control of access to new license functionality in multi-tenant environments | 6.2 GA and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Console administration | Certificate field renamed Signature | 6.2 GA and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Protection | New applications not blocked by default, and the Enable Default application state option | 6.2 (CM 6.2.0.0451) and later | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Administration > Settings > Application Control Manager (Enable Default application state) |
| Platform | HTTPS for the Grafana connection (on-premises) | 6.2 (CM 6.2.1.0111) and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000516-NDM-000344` | Enable TLS on Grafana with your own certificate |
| Forensics | Legacy Forensics view (enabled by Fortinet Support) | 6.2 (CM 6.2.1.0111) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Endpoint | FortiClient notifications for FortiEndpoint deployments | 6.2 (CM 6.2.4.0026) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Administration > Settings > End Users Notifications (Enable FortiClient notifications) |
| Architecture | Jumpbox change disabled for Cores earlier than 6.0.1.652 | 6.2 (CM 6.2.4.0026) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Architecture | Obfuscation of user names, host names, addresses, and other data sent to FCS | 6.2 (CM 6.2.4.0026) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Console administration | Deployment URL and reputation service list in Administration > Tools | 6.2 (CM 6.2.5.0052) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | License consolidation for workstations and servers | 6.2 (CM 6.2.5.0052)+; 7.0 (CM 7.0.4.0050)+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Inventory | VDI devices shown as Disconnected (Expired) after 6 hours | 6.2 (CM 6.2.5.0052) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Protection | PUP Prevented rule in the Execution Prevention policy | 6.2 (CM 6.2.6.0097) and later | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Profiles > Security > Policies (Execution Prevention) |
| Console administration | Login blocked when the license has expired | 6.2 (CM 6.2.6.0097) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Protection | AV Engine 7.0 signatures selected through the Aggregator API | 6.2 (CM 6.2.6.0097) and later | IDPS `SRG-NET-000246-IDPS-00205` | — |
| Platform | Hardening enhancements | 6.2 (CM 6.2.6.0097) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Protection | Cloud workload protection with the node Collector (AWS, Azure, GCP) | 7.0 GA and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Protection | Mobile device protection (Android and iOS) and the Mobile Devices policy | 7.0 GA and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Console administration | Dashboard changes, and PDF reports generated from the dashboard | 7.0 GA+; 7.2.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Response | Incidents workflow (Event Viewer renamed Incidents), incident entities, and filtering of events older than 30 days | 7.0 GA+; 7.2.0+ | IDPS `SRG-NET-000113-IDPS-00013` | GUI: Incidents |
| Inventory | Security posture indicator (Device Security column) for Windows and macOS endpoints | 7.0 GA and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Integrations | External attack surface visibility with FortiRecon (NIST and ACI severity) | 7.0 GA and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Console administration | New look and feel and color schemes of the console | 7.0 GA+; 7.2.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Console administration | Administration > Tools renamed Administration > Settings | 7.0 GA and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Communication control | Host firewall policies on Collector groups | 7.2.0 and later | IDPS `SRG-NET-000390-IDPS-00212`; IDPS `SRG-NET-000391-IDPS-00213`; IDPS `SRG-NET-000018-IDPS-00018` | GUI: Communications Control > Host Firewall |
| Protection | Disk encryption management for Windows (BitLocker) and macOS (FileVault) endpoints | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Profiles > Disk Encryption |
| Communication control | Exporting Communication Control applications through the notification center | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Protection | Secure browser (disabled by default) | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Inventory | Collector filtering, including devices not seen for more than 30 days | 7.2.1 and later | UEM-S `SRG-APP-000472-UEM-000347` | GUI: Assets > Inventory |
| Console administration | Time zone per organization | 7.2.1 and later | NDM `SRG-APP-000374-NDM-000299` | GUI: Administration > Settings > Time Zone (Ignore data converter) |
| Console administration | Login without the organization name in multi-tenancy | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Console administration | GUI enhancements: user field validation (2FA, password, role), exceptions loaded only on supported Collectors, error reporting | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | On-premises deployment in air-gapped environments | 7.2.3 and later | NDM `SRG-APP-000516-NDM-000317` | — |
| Protection | AV Signature policy and manual content upload in the Update Center | 7.2.3 and later | IDPS `SRG-NET-000246-IDPS-00205`; IDPS `SRG-NET-000251-IDPS-00178`; IDPS `SRG-NET-000019-IDPS-00187` | GUI: Profiles > Security > Security Content Update; GUI: Administration > Deployment > Update Center |
| Protection | Collector Settings policy (behavior in operating modes, upgrade schedule) | 7.2.3 and later | IDPS `SRG-NET-000512-IDPS-00194` | GUI: Profiles > Security > Collector Settings |
| Response | Inconclusive events sent to FCS before they appear in Incidents | 7.2.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Protection | High-Sensitivity Mode of the File Encryptor rule (Ransomware Prevention) | 7.2.3 and later | IDPS `SRG-NET-000249-IDPS-00176` | GUI: Profiles > Security > Policies (Ransomware Prevention) |
| Inventory | System summary and reporting enhancements | 7.2.3 (CM 7.2.3.0302) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Console administration | UX improvements (loading indicator, notification counters, certificate settings navigation) | 7.2.3 (CM 7.2.3.0302) and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current releases:

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/28-fortiedr-feature-version-and-srg-map-requirements.csv) (80 rows).

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| NDM | `SRG-APP-000026-NDM-000208` | CAT II | The network device must automatically audit account creation. |
| NDM | `SRG-APP-000027-NDM-000209` | CAT II | The network device must automatically audit account modification. |
| NDM | `SRG-APP-000033-NDM-000212` | CAT I | The network device must be configured to assign appropriate user roles or access levels to authenticated users. |
| NDM | `SRG-APP-000065-NDM-000214` | CAT II | The network device must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must block any login attempt for 15 minutes. |
| NDM | `SRG-APP-000068-NDM-000215` | CAT II | The network device must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the device. |
| NDM | `SRG-APP-000095-NDM-000225` | CAT II | The network device must produce audit log records containing sufficient information to establish what type of event occurred. |
| NDM | `SRG-APP-000100-NDM-000230` | CAT II | The network device must generate audit records containing information that establishes the identity of any individual or process associated with the event. |
| NDM | `SRG-APP-000101-NDM-000231` | CAT II | The network device must generate audit records containing the full-text recording of privileged commands. |
| NDM | `SRG-APP-000116-NDM-000234` | CAT II | The network device must use internal system clocks to generate time stamps for audit records. |
| NDM | `SRG-APP-000120-NDM-000237` | CAT II | The network device must protect audit information from unauthorized deletion. |
| NDM | `SRG-APP-000131-NDM-000243` | CAT II | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| NDM | `SRG-APP-000142-NDM-000245` | CAT I | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services |
| NDM | `SRG-APP-000148-NDM-000346` | CAT II | The network device must be configured with only one local account to be used as the account of last resort in the event the authentication server is unavailable. |
| NDM | `SRG-APP-000149-NDM-000247` | CAT I | The network device must be configured to use DoD PKI as multi-factor authentication (MFA) for interactive logins. |
| NDM | `SRG-APP-000153-NDM-000249` | CAT II | The network device must be configured to authenticate each administrator prior to authorizing privileges based on assignment of group or role. |
| NDM | `SRG-APP-000156-NDM-000250` | CAT II | The network device must implement replay-resistant authentication mechanisms for network access to privileged accounts. |
| NDM | `SRG-APP-000164-NDM-000252` | CAT II | The network device must enforce a minimum 15-character password length. |
| NDM | `SRG-APP-000166-NDM-000254` | CAT II | The network device must enforce password complexity by requiring that at least one uppercase character be used. |
| NDM | `SRG-APP-000167-NDM-000255` | CAT II | The network device must enforce password complexity by requiring that at least one lowercase character be used. |
| NDM | `SRG-APP-000168-NDM-000256` | CAT II | The network device must enforce password complexity by requiring that at least one numeric character be used. |
| NDM | `SRG-APP-000169-NDM-000257` | CAT II | The network device must enforce password complexity by requiring that at least one special character be used. |
| NDM | `SRG-APP-000170-NDM-000329` | CAT II | The network device must require that when a password is changed, the characters are changed in at least eight of the positions within the password. |
| NDM | `SRG-APP-000171-NDM-000258` | CAT I | The network device must be configured to store passwords using an approved salted key derivation function, preferably using a keyed hash for password-based authentication. |
| NDM | `SRG-APP-000172-NDM-000259` | CAT I | The network device must transmit only encrypted representations of passwords. |
| NDM | `SRG-APP-000179-NDM-000265` | CAT I | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| NDM | `SRG-APP-000190-NDM-000267` | CAT I | The network device must terminate all network connections associated with a device management session at the end of the session, or the session must be terminated after five minutes of inactivity except to fulfill documented and validated mission requirements. |
| NDM | `SRG-APP-000231-NDM-000271` | CAT I | The network device must only allow authorized administrators to view or change the device configuration, system files, and other files stored either in the device or on removable media (such as a flash drive). |
| NDM | `SRG-APP-000329-NDM-000287` | CAT II | If the network device uses role-based access control, the network device must enforce organization-defined role-based access control policies over defined subjects and objects. |
| NDM | `SRG-APP-000340-NDM-000288` | CAT I | The network device must prevent non-privileged users from executing privileged functions to include disabling, circumventing, or altering implemented security safeguards/countermeasures. |
| NDM | `SRG-APP-000343-NDM-000289` | CAT II | The network device must audit the execution of privileged functions. |
| NDM | `SRG-APP-000374-NDM-000299` | CAT II | The network device must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). |
| NDM | `SRG-APP-000378-NDM-000302` | CAT II | The network device must prohibit installation of software without explicit privileged status. |
| NDM | `SRG-APP-000380-NDM-000304` | CAT II | The network device must enforce access restrictions associated with changes to device configuration. |
| NDM | `SRG-APP-000408-NDM-000314` | CAT II | Network devices performing maintenance functions must restrict use of these functions to authorized personnel only. |
| NDM | `SRG-APP-000412-NDM-000331` | CAT I | The network device must be configured to implement cryptographic mechanisms using a FIPS 140-2 approved algorithm to protect the confidentiality of remote maintenance sessions |
| NDM | `SRG-APP-000457-NDM-000352` | CAT II | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| NDM | `SRG-APP-000503-NDM-000320` | CAT II | The network device must generate audit records when successful/unsuccessful logon attempts occur. |
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000317` | CAT II | The network device must be configured in accordance with the security configuration settings based on DoD security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000344` | CAT II | The network device must obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000820-NDM-000170` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |
| UEM-S | `SRG-APP-000191-UEM-000119` | CAT II | The UEM server must be configured to invoke either host-OS functionality or server functionality to provide a trusted communication channel between itself and managed devices that provides assured identification of its endpoints and protection of the communicated data from modification and disclosure using [selection: -TLS, -HTTPS]. |
| UEM-S | `SRG-APP-000395-UEM-000266` | CAT I | Before establishing a connection to any endpoint device being managed, the UEM server must establish a trusted path between the server and endpoint that provides assured identification of the end point using a bidirectional authentication mechanism configured with a FIPS-validated Advanced Encryption Standard (AES) cipher block algorithm to authenticate with the device. |
| UEM-S | `SRG-APP-000427-UEM-000299` | CAT II | The UEM server must be configured to use X.509v3 certificates for code signing for system software updates. |
| UEM-S | `SRG-APP-000427-UEM-000500` | CAT I | The UEM server must provide digitally signed policies and policy updates to the UEM agent. |
| UEM-S | `SRG-APP-000439-UEM-000313` | CAT I | The UEM server must connect to [assignment: [list of applications]] and managed mobile devices with an authenticated and secure (encrypted) connection to protect the confidentiality and integrity of transmitted information. |
| UEM-S | `SRG-APP-000472-UEM-000347` | CAT II | The UEM server must be configured with the periodicity of the following commands to the agent of six hours or less: - query connectivity status; - query the current version of the managed device firmware/software; - query the current version of installed mobile applications; - read audit logs kept by the managed device. |
| UEM-S | `SRG-APP-000474-UEM-000349` | CAT II | The UEM server must alert the system administrator (SA) when anomalies in the operation of security functions are discovered. |
| UEM-S | `SRG-APP-000580-UEM-000398` | CAT II | The UEM server must authenticate endpoint devices (servers) before establishing a local, remote, and/or network connection using bidirectional authentication that is cryptographically based. |
| UEM-A | `SRG-APP-000358-UEM-100013` | CAT II | The UEM Agent must be configured to enable the following function: transfer managed endpoint device audit logs read by the UEM Agent to an UEM server or third-party audit management server. |
| UEM-A | `SRG-APP-000427-UEM-100007` | CAT II | The UEM Agent must only accept policies and policy updates that are digitally signed by a certificate that has been authorized for policy updates by the UEM Server. |
| UEM-A | `SRG-APP-000516-UEM-100006` | CAT II | The UEM Agent must record the reference identifier of the UEM Server during the enrollment process. |
| UEM-A | `SRG-APP-000516-UEM-100010` | CAT II | The UEM Agent must perform the following functions: -enroll in management -configure whether users can unenroll from management -configure periodicity of reachability events. |
| UEM-A | `SRG-APP-000516-UEM-100011` | CAT II | The UEM Agent must be configured to perform one of the following actions upon an attempt to unenroll the mobile device from management: -prevent the unenrollment from occurring -wipe the device to factory default settings -wipe the work profile with all associated applications and data. |
| UEM-A | `SRG-APP-000555-UEM-100014` | CAT I | All UEM Agent cryptography supporting DoW functionality must be FIPS 140-3 validated. |
| IDPS | `SRG-NET-000018-IDPS-00018` | CAT II | The IPS must enforce approved authorizations by restricting or blocking the flow of harmful or suspicious communications traffic within the network. |
| IDPS | `SRG-NET-000019-IDPS-00187` | CAT II | The IDPS must immediately use updates made to policy filters, rules, signatures, and anomaly analysis algorithms for traffic detection and prevention functions. |
| IDPS | `SRG-NET-000074-IDPS-00059` | CAT II | The IDPS must produce audit records containing sufficient information to establish what type of event occurred, including, at a minimum, event descriptions, policy filter, rule or signature invoked, port, protocol, and criticality level/alert code or description. |
| IDPS | `SRG-NET-000091-IDPS-00193` | CAT II | The IDPS must provide log information in a format that can be extracted and used by centralized analysis tools. |
| IDPS | `SRG-NET-000113-IDPS-00013` | CAT II | The IDPS must provide audit record generation capability for detection events based on implementation of policy filters, rules, signatures, and anomaly analysis. |
| IDPS | `SRG-NET-000113-IDPS-00082` | CAT II | The IDPS must provide audit record generation capability for events where communication traffic is blocked or restricted based on policy filters, rules, signatures, and anomaly analysis. |
| IDPS | `SRG-NET-000246-IDPS-00205` | CAT II | The IDPS must automatically update malicious code protection mechanisms as new releases are available in accordance with organizational configuration management procedures. |
| IDPS | `SRG-NET-000249-IDPS-00176` | CAT II | The IPS must block malicious code. |
| IDPS | `SRG-NET-000249-IDPS-00221` | CAT II | The IPS must quarantine or block malicious code. |
| IDPS | `SRG-NET-000249-IDPS-00222` | CAT II | The IDPS must send an immediate (within seconds) alert to, at a minimum, the system administrator when malicious code is detected. |
| IDPS | `SRG-NET-000251-IDPS-00178` | CAT II | The IDPS must automatically update malicious code protection mechanisms as new releases are available in accordance with organizational configuration management policy. |
| IDPS | `SRG-NET-000383-IDPS-00208` | CAT II | IDPS components, including sensors, event databases, and management consoles must integrate with a network-wide monitoring capability. |
| IDPS | `SRG-NET-000384-IDPS-00209` | CAT II | The IDPS must detect network services that have not been authorized or approved by the ISSO or ISSM, at a minimum. |
| IDPS | `SRG-NET-000390-IDPS-00212` | CAT II | The IDPS must continuously monitor inbound communications traffic for unusual/unauthorized activities or conditions. |
| IDPS | `SRG-NET-000391-IDPS-00213` | CAT II | The IDPS must continuously monitor outbound communications traffic for unusual/unauthorized activities or conditions. |
| IDPS | `SRG-NET-000392-IDPS-00214` | CAT II | The IDPS must send an alert to, at a minimum, the information system security manager (ISSM) and information system security officer (ISSO) when intrusion detection events are detected which indicate a compromise or potential for compromise. |
| IDPS | `SRG-NET-000392-IDPS-00219` | CAT II | The IDPS must generate an alert to, at a minimum, the ISSM and ISSO when new active propagation of malware infecting DoD systems or malicious code adversely affecting the operations and/or security of DoD systems is detected. |
| IDPS | `SRG-NET-000511-IDPS-00012` | CAT II | The IDPS must off-load log records to a centralized log server in real-time. |
| IDPS | `SRG-NET-000512-IDPS-00194` | CAT II | The IDPS must be configured in accordance with the security configuration settings based on DoD security policy and technology-specific security best practices. |

### Collecting evidence

Record the Central Manager version and the Collector versions in use
(*Administration > Deployment > System Components* and *Assets >
Inventory*, exported with each Collector's version, state, and group), and
on each on-premises component run `fortiedr version` and `fortiedr status`
and keep the output with the operating system assessment of the host. Add
screenshots or exports of the panes the map cites, above all
*Administration > Users* (users, roles, advanced permissions, and the
password policy), the LDAP and SAML authentication settings,
*Administration > Settings* (Session Time Out, Component Authentication,
FortiEDR Connect, and the other sections), *Profiles > Export settings*
(syslog destinations and their notifications), *Administration >
Distribution lists*, and *Profiles > Security > Policies* with the mode of
each policy and the Collector groups assigned to it. Generate an Audit
Trail for the assessment period, export the exception and exclusion lists,
and keep the playbook settings that send email and syslog notifications.

## Validation and Troubleshooting

- **A feature in the map is missing.** Check the version column against
  both the Central Manager and the Collector: many features need a minimum
  Collector version, some need a license add-on (Forensics, Threat
  Hunting, eXtended Detection, Vulnerability Management), and some build
  features are enabled only through Fortinet Support.
- **A setting is not where the map says.** The map uses the 7.2.3 pane
  names; earlier releases use *Administration > Tools*, *Event Viewer*, and
  *Security Settings*. Some settings exist only in Hoster view (Session
  Time Out, SMTP in multi-organization systems) or only for an organization
  (Component Authentication, End Users Notifications, File Scan).
- **Collectors do not register after hardening.** Check that the
  Aggregator address and port (8081) and the Core port (555) are open from
  the endpoints, that the registration password in the installer is
  current after a revocation, and that the Central Manager certificate
  matches its FQDN.
- **LDAP users cannot log on.** LDAP authentication needs a Core with the
  Jumpbox function that can reach the directory; check the security level
  and port, and the group DNs of the role mapping.
- **A policy blocks a legitimate application.** Define a narrow exception
  from the incident, or a process or path exclusion, instead of returning
  the policy to Simulation mode, and record it for review.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (account reviews, hash checks), by another system (the identity
  provider, the central log server), or by the host operating system.
  Record how each requirement is met, not just which feature covers it.

## Security and Best Practices

- Keep the Central Manager, back-end components, and Collectors on
  vendor-supported releases, and install security updates within 30 days
  (NDM `SRG-APP-000457-NDM-000352`), under change control.
- Log administrators on through SAML with CAC, give each the least
  privileged role, set the password policy to 15 characters with
  complexity, brute-force protection, and required 2FA, and set the idle
  session timeout to 5 minutes.
- Install a Central Manager certificate from a DoD-approved CA, keep the
  console on the management network, and upload only approved CA
  certificates to the Central Manager trust store.
- Run every security policy in Protection mode, keep content and AV
  signatures current through the Content Updates add-on or the AV
  Signature policy, and review exceptions and exclusions.
- Protect and, when needed, revoke the registration password, and ask
  Fortinet Support to enable SSL between Collector and Core.
- Send security events, system events, and the audit trail to a central
  log server over TLS, and alert the ISSO on malicious code detections.
- Review this map each time Fortinet publishes a FortiEDR release or
  Central Manager build, or DISA updates the NDM, UEM, or IDPS SRGs.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiEDR Release Notes*, page "What's new" and its build
  pages, releases 5.0.3, 5.1.0, 5.2.0, 5.2.1, 6.0, 6.2, 7.0, 7.2.0,
  7.2.1, and 7.2.3, and the *FortiEDR 5.0.1* and *5.0.2 Release Notes*
  (PDF) (docs.fortinet.com, FortiEDR documentation).
- Fortinet, *FortiEDR 5.0.0 Installation and Administration Guide* (for
  the core features), *FortiEDR 7.2.3 Administration Guide*, and *FortiEDR
  7.2 Syslog Message Reference*.
- DISA Network Device Management SRG V5R5, Unified Endpoint Management
  Server SRG V2R6, Unified Endpoint Management Agent SRG V2R2, and
  Intrusion Detection and Prevention Systems SRG V3R4, from the October
  2026 STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map),
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the model for this one),
  [Chapter 21](21-fortisandbox-feature-version-and-srg-map.md) (the
  FortiSandbox map, which uses the IDPS SRG), and
  [Chapter 27](27-forticlient-and-ems-feature-version-and-srg-map.md) (the
  FortiClient and EMS map, which uses the UEM SRGs).

**Knowledge checks:**

1. Which SRG covers the Central Manager console, and why are the UEM and
   IDPS SRGs used only for parts of FortiEDR?
2. Which STIG applies to an endpoint with a Collector, and which to an
   on-premises Central Manager?
3. Where does the version data come from, and why do some version entries
   name a Central Manager or Core build?
4. Which FortiEDR setting keeps a Collector from being stopped or
   uninstalled by a user, and what weakens it?
5. Which security policy settings must change before FortiEDR blocks
   malicious code, and how do you show it to an assessor?
6. Which requirements can FortiEDR not meet exactly, and how do you handle
   them?

## Summary and Completion Checklist

FortiEDR has no STIG, so it is assessed against the NDM SRG for the
Central Manager console, the UEM Server and Agent SRGs for the Collector's
management channel, and the IDPS SRG for its malicious code protection,
with the operating system STIGs for every endpoint and for the on-premises
hosts. This chapter maps 143 features to the FortiEDR release or
build that introduced them, to 80 requirements (47 NDM,
8 UEM-S, 6 UEM-A, and 19 IDPS), and to the pane or
command that configures them: 53 core platform features, and
90 features from the FortiEDR 5.0 through 7.2.3 release notes.
Operational features with no direct requirement fall under the requirement
to disable unnecessary functions when unused, and the operating system
STIGs still apply in full to every endpoint.

- [ ] Can explain why FortiEDR is assessed against the NDM, UEM, and IDPS
  SRGs, and where the operating system STIGs apply.
- [ ] Can find the FortiEDR release or build that introduced a feature.
- [ ] Can map a FortiEDR feature to its NDM, UEM, or IDPS requirement.
- [ ] Can find the pane or command that meets the requirement.
- [ ] Can collect the evidence and record the requirements that FortiEDR
  cannot meet exactly.
