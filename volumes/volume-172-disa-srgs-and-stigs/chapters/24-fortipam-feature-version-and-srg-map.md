# Chapter 24: FortiPAM Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiPAM release that introduced a given feature.
- Map each FortiPAM feature to the Network Device Management (NDM) SRG
  requirement or the Application Security and Development (ASD) STIG rule
  it helps satisfy.
- Explain why most ASD STIG rules are developer obligations, and which
  ones a FortiPAM administrator can configure or verify.
- Find the FortiPAM GUI pane, or the documented CLI command, that
  configures each feature to meet its requirement.
- Use the map to scope an SRG-based assessment of FortiPAM, which has no
  STIG of its own.
- Record the requirements that FortiPAM cannot meet exactly, with their
  mitigations.

## Theory and Architecture

FortiPAM is Fortinet's privileged access management (PAM) product. It
keeps the credentials of privileged accounts (passwords, SSH keys,
certificates, and key-value pairs) in an encrypted vault as *secrets*;
launches sessions to the targets that use them (SSH, RDP, VNC, Telnet,
SFTP, SMB, databases, web sites, and OT applications) without showing the
credential to the user; proxies and records those sessions as video, with
the SSH commands logged; gates access with check-out, approval workflows,
and just-in-time privilege; and changes and verifies the stored passwords
on a schedule. It has **no DISA STIG** (Chapter 10), so it is assessed
against SRGs, as described in Chapter 03. Chapter 10 assigns it the **NDM
SRG** and **the Application Security and Development requirements that
apply to the application**. For every FortiPAM feature the chapter gives
**which FortiPAM release introduced it**, **which requirement it relates
to**, and **which GUI pane or command configures it to meet that
requirement**.

FortiPAM runs on hardware appliances and as a virtual machine on private
and public clouds, and its operating system is derived from FortiOS: the
CLI uses FortiOS-style `config`, `edit`, `set`, `next`, and `end`
statements, and the Administration Guide notes that `?` lists the options
at each level. Its configuration uses a few ideas again and again:

- **One user list, many roles.** Every account in *User Management > User
  List* is a local, API, JWT, or remote (LDAP, RADIUS, or SAML) user, with
  a role type (standard user, power user, administrator, and others) and a
  role from *User Management > Role* that gives None, Read, or Read/Write
  access to each page, plus switches such as CLI access, glass breaking,
  maintenance mode, and log viewing.
- **Secrets, folders, and policies.** A secret is created from a
  *template* (its fields and launchers), points to a *target*, and lives in
  a folder. The folder's *secret policy* sets session recording, proxy
  mode, tunnel encryption, check-out, approval, clipboard blocking, the SSH
  filter, and automatic password changing and verification for every
  secret in it.
- **Launchers.** Sessions start through native launchers on the user's
  endpoint (through FortiClient) or through web launchers in the browser.
  In proxy mode the session passes through FortiPAM, which records it.
- **System settings.** *System > Settings* holds the user password policy
  and login lockout, the GUI session timeout, concurrent log-on, the login
  disclaimer, the global minimum TLS version, time, email, and the storage
  and video settings; *Network > Interfaces* sets the GUI portal and the
  management access of each interface; logging is under *Log & Report*.

### Where the version data comes from

Fortinet publishes no Feature Matrix and no New Features Guide for
FortiPAM. Its **Release Notes**, however, have a "What's new" page for
every release, and the Administration Guide repeats the entries of its own
release in a "What's new in FortiPAM" chapter. docs.fortinet.com lists
eleven FortiPAM trains, **1.0** through **1.9** and **7.0** (the release
after 1.9.2 is numbered 7.0.0), with 31 releases: 1.0.0 to 1.0.3, 1.1.0 to
1.1.2, 1.2.0, 1.3.0 and 1.3.1, 1.4.0 to 1.4.3, 1.5.0 and 1.5.1, 1.6.0 to
1.6.2, 1.7.0 to 1.7.2, 1.8.0 to 1.8.4, 1.9.0 to 1.9.2, and 7.0.0. The
release notes are the best source: they are the only document that lists
the changes of every release, and each entry is a separate section. The
version column was built from the "What's new" pages of all 31 releases.

- The first release, **1.0.0**, has a "Supported features" page instead,
  which lists the capabilities of the first release. It is used for the
  core features, not as new-feature entries.
- Sixteen pages say that the release is a patch release with no new
  features: 1.0.2, 1.1.1, 1.3.1, 1.4.1, 1.4.2, 1.4.3, 1.5.1, 1.6.1, 1.6.2,
  1.7.1, 1.7.2, 1.8.1, 1.8.2, 1.8.3, 1.8.4, and 1.9.2.
- The 1.0.1 and 1.0.3 pages have one bulleted entry each. From 1.1.0 on,
  each entry is a heading that starts with the Fortinet bug IDs of the
  change ("842754, 899220- Simplified ZTNA GUI"); from 1.4.0 the entries
  are grouped under *Secret/Launch*, *User/Group*, *System/Log*, and
  *Others*.

That gives 281 entries: 2 in 1.0, 42 in 1.1, 28 in 1.2, 25 in
1.3, 38 in 1.4, 28 in 1.5, 21 in 1.6, 25 in 1.7, 28 in 1.8, 26 in 1.9, and
18 in 7.0. Each entry title was taken from its heading without the bug
IDs, and its description from the text up to the next entry.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: management
  access, roles and users, remote authentication, two-factor
  authentication, the password policy, logging, time, SNMP, certificates,
  HA, backups, firmware, the encrypted vault, and the PAM functions
  themselves (secrets, policies, recording, check-out, approval, and
  password rotation). Each one is in the 1.0.0 Supported features list or
  described in the **FortiPAM 1.0.0 Administration Guide** (February 2023),
  so it existed in the first release and is not in the release notes
  lists. Two core rows have a different version entry, explained below.
- **New features** are the 281 entries of the "What's new" pages,
  one row each. The categories were assigned for this chapter (the release
  notes categories are too broad to help), and the titles were shortened
  from the release notes text. Where the same topic appears in two
  releases (concurrent log-on in 1.2.0 and 1.4.0, the Web API password
  changer in 1.5.0 and 1.8.0, and auto provisioning of display names for
  SAML users in 1.8.0 and for LDAP users in 1.9.0), each release has its
  own row, because each entry describes a different change.

| Version entry | Meaning |
| --- | --- |
| `1.0.0` | A core feature in the FortiPAM 1.0.0 Supported features list or Administration Guide (the first release) |
| `1.4.0 and later` | Introduced in FortiPAM 1.4.0 (listed on its "What's new" page) |
| `1.1.0 or earlier` | Named in the 1.1.0 release notes as an existing setting that was renamed (Admin Session Timeout became User Session Timeout), but not described in the 1.0.0 Administration Guide |
| `7.0.0 or earlier` | In the 7.0.0 Administration Guide, but in no release notes page and not in the 1.0.0 Administration Guide (the Max Retry and Lockout Duration settings of the login lockout) |

Three cautions apply. First, every FortiPAM minor release (1.1, 1.2, and
so on) is its own train with only a few patch releases, and each one adds
features, so "and later" means every later release. Second, many features
depend on the platform (hardware RAID on the 1000G and 3000G, vTPM on KVM,
VMware, and GCP, disk encryption and vTPM not on OCI), on the license
(stackable seats, floating and concurrent logon licenses, FortiToken
Cloud), or on the client (FortiClient or the Fortinet Privileged Access
Agent browser extension, often a minimum version). Third, a core row
records a FortiPAM capability, but its pane was checked against the 7.0.0
Administration Guide and may be named or placed differently on an older
release (the GUI was reorganized in 1.1.0, 1.2.0, 1.4.0, and 1.7.0, and
the Web Launcher was renamed Web Browsing in 1.7.0).

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG or STIG | Release | Applies to |
| --- | --- | --- | --- |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The management plane: administrator accounts and roles, GUI and CLI access, the logon banner, lockout, idle timeout, cryptography for management, logging, time, SNMP, firmware, backups, and certificates |
| **ASD** | Application Security and Development STIG | V6R5, benchmark date 30 Sep 2026 | FortiPAM as an application that users log in to: session management, account management and auditing, authorization, authentication and passwords, credential and data protection, audit records, and transmission protection |

The **NDM SRG** covers FortiPAM's administration, as it does for the
other Fortinet appliances in this volume. The **ASD STIG** is the DISA
STIG for applications in general, built from the Application Security
Requirements Guide; Chapter 10 assigns its requirements to FortiPAM
because FortiPAM is, above all, an application that every privileged user
logs in to. ASD rules have STIG IDs of the form `APSC-DV-nnnnnn`. The map
cites them by that rule version, as the XCCDF gives it, and the
Requirement reference table gives the SRG ID that each one implements (the
XCCDF group title, such as `SRG-APP-000065` for the lockout rule).

The ASD STIG has 286 rules, and most of them are **developer
obligations**: input validation, protection from cross-site scripting,
SQL injection, and overflow attacks, session ID handling and cookie flags,
SOAP and SAML message construction, error handling, code review, threat
models, test plans, configuration management of the source code, and
secure design. For a commercial product, those are met (or not) by
Fortinet, and an assessor checks them through vendor evidence or a
vulnerability scan, not through settings; they are out of scope for a
configuration map. This chapter cites only the 101 ASD rules that a
FortiPAM administrator can actually **configure or verify**: idle
timeouts and concurrent sessions, lockout, the banner, account management
and its audit and notification, authorization, two-factor and PIV
authentication, the password policy, encryption of stored and transmitted
data, audit content, off-loading and protection, backups, signed updates,
and the use of supported releases. Where an ASD rule and an NDM
requirement cover the same setting, the map gives both: the NDM
requirement for FortiPAM's administrators and the ASD rule for every user
of the application.

The requirement IDs are the **rule version IDs** from the XCCDF files,
and the severity is the rule's severity (high = CAT I, medium = CAT II,
low = CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiPAM meets a
  requirement. SSH command logging on SSH secrets implements the full-text
  recording of privileged commands on targets (ASD `APSC-DV-001030`), for
  example.
- **Must be configured to meet a requirement.** The feature is in scope
  of a requirement and has to be set up correctly. The user password
  policy must be set to a minimum length of 15 (NDM
  `SRG-APP-000164-NDM-000252`, ASD `APSC-DV-001680`, CAT I), for example.
- **No direct requirement.** The feature is operational, such as a new
  launcher, a template, a GUI change, or a cloud platform. It has no
  requirement of its own, but if it is not needed it falls under the NDM
  requirement to prohibit unnecessary functions, ports, protocols, and
  services (NDM `SRG-APP-000142-NDM-000245`).

The mapping is a starting point for an assessment, not a ruling. Confirm
it with your assessor, especially the choice of ASD rules and the split
between the NDM SRG and the ASD STIG.

### Where the commands come from

Fortinet publishes **no CLI Reference for FortiPAM**: no train on
docs.fortinet.com has one. The **FortiPAM 7.0.0 Administration Guide**
(initial release 14 September 2026), the newest Administration Guide, is
the source for every command and pane. It configures almost everything in
the GUI, and prints CLI blocks only for settings that have no GUI or as
examples. The command column therefore names the **GUI pane** for most
rows and uses the CLI where the guide prints a block for the setting. The
check was automatic: every CLI block of the guide was collected (62
`config` paths), and each `config` path, nested table, `set` option, and
enumerated value in the map was checked against them; each `execute` and
`diagnose` command against the guide's command lines; and each GUI pane
against the guide's text (one pane, *Monitoring > User Monitor*, is named
only in the 1.2.0 release notes). Read the column this way:

- **GUI:** entries name the FortiPAM GUI pane; the text in parentheses
  names the fields to set.
- Commands run on the FortiPAM CLI, over SSH or in the GUI's CLI console.
  Statements are separated by `;` to fit in a table cell; on the CLI,
  enter each one on its own line. Values in `<ANGLE_BRACKETS>` are
  placeholders for your own values.
- For **"No direct requirement"** rows, the entry shown is where the
  feature is turned off when it is unused. A dash (**—**) means there is
  nothing to change: the feature is a platform, a template, a launcher, a
  GUI change, a behavior change, or a capability that is off unless
  configured.

Some requirements cannot be met exactly with FortiPAM settings. Record
them on the checklist as open findings with mitigations, or meet them
another way:

- **No CLI Reference.** Settings can be checked only in the GUI, through
  the REST API, or in a configuration backup. Use screenshots or exports
  of the panes the map cites as evidence.
- **No FIPS mode.** The 7.0.0 Administration Guide describes no FIPS or
  Common Criteria mode, so FIPS-validated cryptography for authentication
  and for remote management (NDM `SRG-APP-000179-NDM-000265`,
  NDM `SRG-APP-000412-NDM-000331`, CAT I) and FIPS-validated modules for
  protected information (ASD `APSC-DV-001860`, ASD `APSC-DV-002040`)
  cannot be shown with a setting. Set the minimum TLS version to TLSv1-2
  or TLSv1-3, set *SSH Algorithm Negotiation* to high-encryption, and
  check the NIST Cryptographic Module Validation Program for your release.
- **Post-login banner.** The *Login Disclaimer* (and `set
  post-login-banner enable`) shows the banner after the user
  authenticates, and the user must select Accept to continue or is logged
  out with Decline. The banner requirements say the banner is shown
  *before* access is granted (NDM `SRG-APP-000068-NDM-000215`,
  ASD `APSC-DV-000550`); the Accept step meets the acknowledgment
  (NDM `SRG-APP-000069-NDM-000216`, ASD `APSC-DV-000560`). Use the
  Standard Mandatory DoD Notice and Consent Banner as the disclaimer text,
  add it to the *Login Page* replacement message so that it is also shown
  before logon, and record how the banner is displayed. The guide does not
  document a banner for SSH logins.
- **Lockout window.** *Max Retry* (1 to 10) and *Lockout Duration*
  (seconds) lock an account after the set number of failed logins; the
  guide documents no 15-minute window for counting the failures
  (ASD `APSC-DV-000530`). Set Max Retry to 3 and Lockout Duration to 900
  seconds or longer.
- **Password rules.** The user password policy applies to local users. It
  sets the minimum length, the number of new characters, the four
  character types, reuse, and expiration, but no minimum password lifetime
  (ASD `APSC-DV-001760`) and no check against a list of commonly used or
  compromised passwords (NDM `SRG-APP-000845-NDM-000220`). Disabling
  *Allow password reuse* is stricter than the five-generation rule
  (ASD `APSC-DV-001780`). Prefer remote accounts, whose passwords the
  directory enforces. The guide does not say how local user passwords are
  stored (NDM `SRG-APP-000171-NDM-000258`, ASD `APSC-DV-001740`); the
  vault's secrets must be stored reversibly so that FortiPAM can use them,
  and are protected with AES-256 and private data encryption instead.
- **Idle timeout.** *GUI Session Timeout* is one global setting for every
  user (1 to 480 minutes idle), so set it to 10 minutes or less to meet
  both the administrator and the user rules (ASD `APSC-DV-000080`,
  ASD `APSC-DV-000070`), and disable *Override Idle Timeout* and *Never
  Timeout* in every role. The guide documents no idle timeout for SSH CLI
  sessions (NDM `SRG-APP-000190-NDM-000267`).
- **Account notifications.** No setting is documented that emails the SA
  and ISSO when an account is created, changed, disabled, enabled, or
  removed (ASD `APSC-DV-000380`, ASD `APSC-DV-000390`,
  ASD `APSC-DV-000400`, ASD `APSC-DV-000410`, ASD `APSC-DV-000430`).
  Automation stitches and automation triggers on event log IDs can send
  email; build and test one for each user event, or alert from the central
  log server.
- **Inactive and temporary accounts.** Automatic disabling after a number
  of inactive days applies only to auto-provisioned remote users
  (ASD `APSC-DV-000320`), and nothing removes temporary accounts after 72
  hours (ASD `APSC-DV-000300`). Disable inactive local users by procedure
  and in the directory, give temporary users a one-time login schedule,
  and prefer one-time invitations for external users.
- **DoD PKI.** Certificate authentication for FortiPAM login arrived in
  7.0.0, for local and remote LDAP users in the GUI; SSH and CLI logins
  keep using passwords, and the guide does not describe revocation
  checking for login certificates beyond importing CRLs. On 7.0.0, enable
  certificate authentication with the DoD CAs for administrators and
  users (NDM `SRG-APP-000149-NDM-000247`, ASD `APSC-DV-001560`); on older
  releases, use a SAML identity provider that enforces PKI, require
  FortiToken two-factor authentication, and record the finding.
- **Log transport and failures.** Syslog uses UDP or reliable TCP, and
  the guide documents no TLS for it; send logs over the management network
  or to FortiAnalyzer. In HA, logs and videos are kept only on the primary
  unit and are not synchronized. The GUI warns about log or video disk
  failures, but nothing alerts at 75 percent of log storage or when a
  syslog server stops receiving logs (ASD `APSC-DV-001090`,
  ASD `APSC-DV-001110`, NDM `SRG-APP-000360-NDM-000295`); alert on
  missing logs at the log server and watch *Log & Report > Disk Usage*.
- **FortiPAM's own CLI commands.** SSH command logging covers the
  sessions users launch to targets. The guide does not say that commands
  entered on FortiPAM's own CLI are logged in full text
  (NDM `SRG-APP-000101-NDM-000231`); restrict *Allow CLI Access* to a few
  administrators and check the system event log on your release.
- **Firmware signatures.** Mandatory dual-signature verification of
  firmware images arrived in 7.0.0 (NDM `SRG-APP-000131-NDM-000243`,
  ASD `APSC-DV-001430`). On older releases, download images only from
  Fortinet support over HTTPS and compare the checksum before every
  upgrade.
- **NTP and SNMP.** Custom NTP servers are configured in the CLI, but the
  guide prints neither the command nor NTP authentication
  (NDM `SRG-APP-000395-NDM-000347`). SNMP v3 offers MD5 and DES as well as
  SHA-2 and AES; choose SHA256 or stronger and AES or AES256
  (NDM `SRG-APP-000395-NDM-000310`).
- **Clear-text password view.** The login page of 1.9.0 and later lets
  the user display the password while typing it
  (NDM `SRG-APP-000178-NDM-000264`, ASD `APSC-DV-001850`). The password is
  hidden unless the user chooses to show it; record the behavior.
- **No STIG.** Without a STIG there is no DoD baseline to check against
  (NDM `SRG-APP-000516-NDM-000317`, ASD `APSC-DV-002970`); use this map
  and the vendor guidance as the baseline, and record the settings that
  differ from it.

## Design Considerations

- **Pick the release first, then the features.** If your design depends
  on a feature introduced in a certain release (additional authentication
  on secret access in 1.9.0, or certificate login, FIDO2 passkeys, SSH host
  key verification, dual-signed firmware, and periodic configuration
  checks in 7.0.0), that sets the minimum FortiPAM release, and it must be
  a vendor-supported release (NDM `SRG-APP-001035-NDM-000340`,
  ASD `APSC-DV-003240`).
- **FortiPAM holds the keys to everything.** It stores the credentials of
  the most privileged accounts in the enterprise, so protect it like a
  domain controller: enable private data encryption with a custom key (and
  TPM or vTPM where available), encrypt the log and video disks, put the
  GUI portal and SSH only on the management network, and allow logins only
  from trusted hosts.
- **Make every privileged session accountable.** Use folders whose secret
  policy enables session recording, proxy mode, tunnel encryption,
  check-out with password change at check-in, and approval for the most
  sensitive targets, and block self-approval. Rotate shared credentials
  automatically, so that a password a user saw stops working when they
  leave (ASD `APSC-DV-000290`).
- **Plan for FortiPAM being down.** Users cannot reach their targets
  while FortiPAM is unreachable. Run an active-passive HA cluster, back up
  the configuration automatically with encryption, and plan glass breaking
  and break-glass credentials for the targets, with alerts when glass
  breaking mode is used.
- **Use the directory and two factors.** Authenticate users against LDAP
  over LDAPS or STARTTLS, or a SAML identity provider that signs its
  assertions and responses, and require two-factor authentication (or, on
  7.0.0, certificates) for every user.
- **Log centrally and keep the videos.** Send system and secret logs to a
  central syslog server or FortiAnalyzer, move session videos to SFTP
  storage, and keep them for the retention period of your audit policy
  (ASD `APSC-DV-002900`).
- **Turn off what is not used.** SNMP v1 and v2c, SCIM, the explicit web
  proxy, FortiToken Mobile push, Telnet launchers, launchers and templates
  that nobody uses, the local NTP server, and debug logging all need a
  reason to stay on.

## Implementation and Automation

### The FortiPAM feature map

The SRG column uses the abbreviations defined in *Where the SRG data
comes from*. The requirement titles are listed in the next table. The
command column follows the conventions in *Where the commands come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/24-fortipam-feature-version-and-srg-map-feature-map.csv) (366 rows).

| Category | Feature | Introduced (FortiPAM) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Management access | Management access on each network interface (PING, SNMP, SCIM, and SSH, with a global SSH port) | 1.0.0 | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000880-NDM-000290`; ASD `APSC-DV-001510` | GUI: Network > Interfaces (Management Access: SSH only on the interface connected to the management network; PING, SNMP, and SCIM only where they are used) |
| Core: Management access | Management access from the CLI on an interface | 1.0.0 | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000408-NDM-000314` | `config system interface`; `edit <PORT>`; `set allowaccess ping ssh`; `next`; `end` |
| Core: Management access | GUI portal on an interface (external IP, service port, SSL certificate, and minimum SSL version) | 1.0.0 | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000516-NDM-000344`; ASD `APSC-DV-002440`; ASD `APSC-DV-001950` | GUI: Network > Interfaces (Service Access Setting, GUI Portal: a DoD-issued SSL certificate; Minimum SSL Version: TLSv1-2 or Follow system global setting) |
| Core: Management access | Global minimum SSL/TLS version | 1.0.0 | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000172-NDM-000259`; ASD `APSC-DV-002440`; ASD `APSC-DV-001750`; ASD `APSC-DV-001940`; ASD `APSC-DV-001950` | GUI: System > Settings (Security, Minimum SSL Version: TLSv1-2 or TLSv1-3) |
| Core: Management access | CLI console in the GUI and CLI over SSH | 1.0.0 | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000340-NDM-000288` | GUI: User Management > Role (Allow CLI Access and Allow CLI Diagnostic Commands only in the roles of administrators who need them) |
| Core: Management access | GUI session timeout (idle timeout or forced logout) | 1.1.0 or earlier | NDM `SRG-APP-000190-NDM-000267`; NDM `SRG-APP-000220-NDM-000268`; ASD `APSC-DV-000070`; ASD `APSC-DV-000080`; ASD `APSC-DV-002000` | GUI: System > Settings (Other General Settings, GUI Session Timeout: Idle, Idle in 10 minutes or less) |
| Core: Management access | Idle timeout override and never-timeout options in roles | 1.0.0 | NDM `SRG-APP-000190-NDM-000267`; ASD `APSC-DV-000080`; ASD `APSC-DV-000070` | GUI: User Management > Role (Admin Settings: Override Idle Timeout and Never Timeout disabled) |
| Core: Management access | Login lockout (Max Retry and Lockout Duration in the user password policy) | 7.0.0 or earlier | NDM `SRG-APP-000065-NDM-000214`; NDM `SRG-APP-000435-NDM-000315`; ASD `APSC-DV-000530` | GUI: System > Settings (User Password Policy: Max Retry 3; Lockout Duration 900 seconds or longer) |
| Core: Management access | Logout from the Admin menu | 1.0.0 | NDM `SRG-APP-000296-NDM-000280`; NDM `SRG-APP-000220-NDM-000268`; ASD `APSC-DV-000090` | — |
| Core: Management access | Trusted hosts and login schedule for each user | 1.0.0 | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213`; NDM `SRG-APP-000880-NDM-000290`; ASD `APSC-DV-000490` | GUI: User Management > User List (Restricted Access: IPv4 Trusted Hosts limited to the management network; Login Schedule where access is time-bound) |
| Core: Management access | Maintenance mode (required for reboot, shutdown, firmware upload, license upload, and configuration restore) | 1.0.0 | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000378-NDM-000302`; ASD `APSC-DV-001410` | GUI: User Management > Role (Admin Settings: Set Maintenance Mode only for the administrators who need it) |
| Core: Management access | Glass breaking mode (temporary access to all secrets) | 1.0.0 | NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000343-NDM-000289`; ASD `APSC-DV-000460`; ASD `APSC-DV-000500` | GUI: User Management > Role (Admin Settings: Enter Glass Breaking Mode for only a few administrators); GUI: Log & Report > Email Alert Settings (Critical System Notification: alert when glass breaking mode is activated) |
| Core: Management access | Enforced recording in glass breaking mode | 1.0.0 | NDM `SRG-APP-000343-NDM-000289`; ASD `APSC-DV-000590`; ASD `APSC-DV-000840` | GUI: System > Settings (Video Setting: Enforce recording on glass breaking enabled) |
| Core: Administrator accounts | Default admin account (no password until one is set at the first login) | 1.0.0 | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000153-NDM-000249`; ASD `APSC-DV-003280`; ASD `APSC-DV-003270` | GUI: User Management > User List (set a password of 15 or more characters for admin at the first login; keep admin as the account of last resort) |
| Core: Administrator accounts | Role types (Standard User, Power User, Administrator, and the types added later) | 1.0.0 | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287`; NDM `SRG-APP-000340-NDM-000288`; ASD `APSC-DV-000460`; ASD `APSC-DV-000500` | GUI: User Management > User List (Role Type: the least-privileged type that fits each user's duties) |
| Core: Administrator accounts | Roles with None, Read, and Read/Write access to each feature (six default roles) | 1.0.0 | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000516-NDM-000335`; ASD `APSC-DV-000460`; ASD `APSC-DV-000500`; ASD `APSC-DV-001410` | GUI: User Management > Role (custom roles limited to each administrator's duties; Super Administrator only for the account of last resort and a few administrators) |
| Core: Administrator accounts | Roles from the CLI (access profiles) | 1.0.0 | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000340-NDM-000288` | `config system accprofile`; `edit <ROLE_NAME>`; `set cli enable`; `set system-diagnostics disable`; `next`; `end` |
| Core: Administrator accounts | Local, API, JWT, and remote user types | 1.0.0 | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000148-NDM-000346`; ASD `APSC-DV-001540` | GUI: User Management > User List (User Type: Remote User for administrators, with one Local User as the account of last resort; API and JWT users only for integrations) |
| Core: Administrator accounts | Local and remote users from the CLI | 1.0.0 | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000033-NDM-000212` | `config system admin`; `edit <USERNAME>`; `set remote-auth enable`; `set accprofile <ROLE_NAME>`; `set remote-group <GROUP_NAME>`; `next`; `end` |
| Core: Administrator accounts | User status (enable or disable a user) | 1.0.0 | ASD `APSC-DV-000330`; NDM `SRG-APP-000148-NDM-000346` | GUI: User Management > User List (Status: disabled for users who no longer need access) |
| Core: Administrator accounts | API users and REST API keys | 1.0.0 | NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000408-NDM-000314` | GUI: User Management > User List (API users only for integrations; Re-generate API Key when a key may be exposed) |
| Core: Authentication | Two-factor authentication for users (Email, FortiToken, FortiToken Cloud, and third-party authenticator) | 1.0.0 | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000825-NDM-000180`; NDM `SRG-APP-000156-NDM-000250`; ASD `APSC-DV-001550`; ASD `APSC-DV-001580` | GUI: User Management > User List (Two-Factor Authentication enabled with FortiToken for every local user); `config system admin`; `edit <USERNAME>`; `set two-factor fortitoken`; `set fortitoken <SERIAL_NUMBER>`; `next`; `end` |
| Core: Authentication | FortiTokens (hard and mobile tokens) | 1.0.0 | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000825-NDM-000180`; NDM `SRG-APP-000156-NDM-000250`; ASD `APSC-DV-001550` | GUI: User Management > FortiTokens |
| Core: Authentication | FortiToken Mobile push | 1.0.0 | NDM `SRG-APP-000142-NDM-000245` | GUI: Network > Interfaces (FortiToken Mobile Push and Push Server Status off unless FortiToken Mobile push is used) |
| Core: Authentication | LDAP servers (LDAPS or STARTTLS, server identity check, and group matching) | 1.0.0 | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000172-NDM-000259`; ASD `APSC-DV-001750`; ASD `APSC-DV-002440` | GUI: User Management > LDAP Servers (Secure Connection enabled; Protocol LDAPS or STARTTLS; Certificate: the DoD CA; Server Identity Check enabled) |
| Core: Authentication | LDAP servers from the CLI | 1.0.0 | NDM `SRG-APP-000516-NDM-000336` | `config user ldap`; `edit <NAME>`; `set server <SERVER_IP>`; `set username <LDAP_USERNAME>`; `set password <PASSWORD>`; `next`; `end` |
| Core: Authentication | SAML single sign-on (FortiPAM as the SAML SP) | 1.0.0 | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000820-NDM-000170`; ASD `APSC-DV-001550`; ASD `APSC-DV-001580` | GUI: User Management > Saml Single Sign-On (an identity provider that enforces DoD PKI or MFA) |
| Core: Authentication | RADIUS servers | 1.0.0 | NDM `SRG-APP-000516-NDM-000336` | GUI: User Management > Radius Servers (a long, unique shared secret for each server) |
| Core: Authentication | User groups (local and remote groups) | 1.0.0 | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000153-NDM-000249`; ASD `APSC-DV-000460` | GUI: User Management > User Groups |
| Core: Authentication | Login schedules (recurring and one-time) | 1.0.0 | NDM `SRG-APP-000038-NDM-000213`; ASD `APSC-DV-000490`; ASD `APSC-DV-000300` | GUI: User Management > Schedule (One Time schedules for temporary users, with Pre-expiration event log) |
| Core: Authentication | Authentication scheme and rules for remote servers | 1.0.0 | NDM `SRG-APP-000516-NDM-000336` | — |
| Core: Authentication | User password policy (minimum length, new characters, character requirements, reuse, and expiration) | 1.0.0 | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000170-NDM-000329`; NDM `SRG-APP-000166-NDM-000254`; NDM `SRG-APP-000167-NDM-000255`; NDM `SRG-APP-000168-NDM-000256`; NDM `SRG-APP-000169-NDM-000257`; NDM `SRG-APP-000860-NDM-000250`; ASD `APSC-DV-001680`; ASD `APSC-DV-001690`; ASD `APSC-DV-001700`; ASD `APSC-DV-001710`; ASD `APSC-DV-001720`; ASD `APSC-DV-001730`; ASD `APSC-DV-001770`; ASD `APSC-DV-001780` | GUI: System > Settings (User Password Policy: Password scope enabled; Minimum length 15; Minimum number of new characters 8; Character requirements 1 upper case, 1 lower case, 1 number, 1 special; Allow password reuse disabled; Password expiration 180 days or less) |
| Core: Authentication | Change Password from the Admin menu (local users only) | 1.0.0 | NDM `SRG-APP-000170-NDM-000329`; ASD `APSC-DV-001730` | — |
| Core: Logging | Event logging (system activity, user activity, and HA) | 1.0.0 | NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000027-NDM-000209`; NDM `SRG-APP-000028-NDM-000210`; NDM `SRG-APP-000029-NDM-000211`; NDM `SRG-APP-000319-NDM-000283`; NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000505-NDM-000322`; NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000381-NDM-000305`; NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000100-NDM-000230`; ASD `APSC-DV-000340`; ASD `APSC-DV-000350`; ASD `APSC-DV-000360`; ASD `APSC-DV-000370`; ASD `APSC-DV-000420`; ASD `APSC-DV-000880`; ASD `APSC-DV-000830`; ASD `APSC-DV-000850`; ASD `APSC-DV-000520`; ASD `APSC-DV-001420` | GUI: Log & Report > Log Settings (Event Logging: all events, not Customize) |
| Core: Logging | System event logs (user events, configuration changes, and logins) | 1.0.0 | NDM `SRG-APP-000096-NDM-000226`; NDM `SRG-APP-000097-NDM-000227`; NDM `SRG-APP-000098-NDM-000228`; NDM `SRG-APP-000099-NDM-000229`; NDM `SRG-APP-000100-NDM-000230`; ASD `APSC-DV-000690`; ASD `APSC-DV-000840` | GUI: Log & Report > System Event |
| Core: Logging | Secret event and video logs (secret access, launches, password views, and password changes) | 1.0.0 | NDM `SRG-APP-000504-NDM-000321`; ASD `APSC-DV-000860`; ASD `APSC-DV-000960`; ASD `APSC-DV-000970`; ASD `APSC-DV-000590`; ASD `APSC-DV-000950` | GUI: Log & Report > Secret Event & Video |
| Core: Logging | SSH logging of all shell commands on SSH secrets | 1.0.0 | NDM `SRG-APP-000101-NDM-000231`; ASD `APSC-DV-001030`; ASD `APSC-DV-000590` | GUI: Secret Settings > SSH Filter Profiles (shell commands logged for every SSH secret) |
| Core: Logging | Local log disk and memory storage | 1.0.0 | NDM `SRG-APP-000357-NDM-000293`; NDM `SRG-APP-000120-NDM-000237` | `config log disk setting`; `set status enable`; `end` |
| Core: Logging | Remote syslog server (system and secret logs) | 1.0.0 | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350`; ASD `APSC-DV-001070`; ASD `APSC-DV-001080` | GUI: Log & Report > Log Settings (Send logs to syslog enabled, with the central log server; in Edit in CLI, mode reliable) |
| Core: Logging | FortiAnalyzer logging | 1.0.0 | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350`; ASD `APSC-DV-001070`; ASD `APSC-DV-001080` | GUI: Network > Fabric Connectors (FortiAnalyzer logging to the central FortiAnalyzer); `config log fortianalyzer setting`; `set status enable`; `set server <FAZ_ADDRESS>`; `end` |
| Core: Logging | Email alert settings (critical system, general, and certificate alerts) | 1.0.0 | NDM `SRG-APP-000795-NDM-000130`; NDM `SRG-APP-000360-NDM-000295`; ASD `APSC-DV-001110`; ASD `APSC-DV-003330` | GUI: Log & Report > Email Alert Settings (Enable email notification; Critical System Notification to the SA and ISSO; General: Configuration change and HA status change; Certificate: alerts before expiry) |
| Core: Logging | Log permissions in roles (View Logs, View Reports, View Secret Log, and View Secret Video) | 1.0.0 | NDM `SRG-APP-000119-NDM-000236`; NDM `SRG-APP-000120-NDM-000237`; NDM `SRG-APP-000121-NDM-000238`; ASD `APSC-DV-001280`; ASD `APSC-DV-001290`; ASD `APSC-DV-001300` | GUI: User Management > Role (Admin Settings: View Logs, View Reports, and View Secret Launching Video only for auditors and administrators who need them) |
| Core: Logging | Reports (audit reports) | 1.0.0 | ASD `APSC-DV-001180`; ASD `APSC-DV-001140` | GUI: Log & Report > Reports |
| Core: Logging | User monitor and active sessions | 1.0.0 | NDM `SRG-APP-000343-NDM-000289`; ASD `APSC-DV-000850` | GUI: Monitoring > Active Sessions |
| Core: Logging | Debug settings and trace logs | 1.0.0 | NDM `SRG-APP-000142-NDM-000245`; ASD `APSC-DV-000650` | GUI: Log & Report > Debug Settings (Debug disabled except during troubleshooting) |
| Core: Time | System time and NTP (FortiGuard or a custom server, sync interval) | 1.0.0 | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000925-NDM-000330`; NDM `SRG-APP-000116-NDM-000234`; NDM `SRG-APP-000374-NDM-000299`; ASD `APSC-DV-001250`; ASD `APSC-DV-001260` | GUI: System > Settings (System time: Set Time NTP; Select Server Custom, with DoD-approved NTP servers configured in the CLI) |
| Core: Time | FortiPAM as a local NTP server | 1.0.0 | NDM `SRG-APP-000142-NDM-000245` | GUI: System > Settings (Setup device as local NTP server: False unless it is needed) |
| Core: SNMP | SNMP v1 and v2c communities | 1.0.0 | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000395-NDM-000310` | GUI: System > SNMP (no SNMP v1 or v2c communities) |
| Core: SNMP | SNMP v3 users (authentication and privacy) | 1.0.0 | NDM `SRG-APP-000395-NDM-000310`; ASD `APSC-DV-003330` | GUI: System > SNMP (SNMP v3 users with Authentication and Private; SHA256 or stronger; AES or AES256) |
| Core: SNMP | SNMP agent system information | 1.0.0 | NDM `SRG-APP-000395-NDM-000310` | `config system snmp sysinfo`; `set status enable`; `end` |
| Core: Certificates | Local, CA, and remote certificates, CSRs, and CRLs | 1.0.0 | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000910-NDM-000300`; NDM `SRG-APP-000875-NDM-000280`; NDM `SRG-APP-000175-NDM-000262`; ASD `APSC-DV-002300`; ASD `APSC-DV-001840` | GUI: System > Certificates (server certificates from a DoD CA through a CSR; only DoD root and intermediate CA certificates; current DoD CRLs imported) |
| Core: Certificates | Self-signed Fortinet_CA_SSL CA for generated certificates | 1.0.0 | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000910-NDM-000300`; ASD `APSC-DV-002300` | GUI: System > Certificates (do not use certificates generated by the Fortinet_CA_SSL CA for the GUI) |
| Core: Availability | Active-passive HA cluster (up to three units) | 1.0.0 | NDM `SRG-APP-000516-NDM-000340`; ASD `APSC-DV-003070` | GUI: System > HA (Mode Active-Passive; heartbeat interfaces on a dedicated link; override and device priority set on each unit) |
| Core: Availability | HA cluster password | 1.0.0 | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000412-NDM-000331` | `config system ha`; `set password <HA_PASSWORD>`; `end` |
| Core: Backup | Manual configuration backup with encryption | 1.0.0 | NDM `SRG-APP-000516-NDM-000340`; ASD `APSC-DV-003070`; ASD `APSC-DV-002330` | GUI: System > Backup (manual backups from the Admin menu Configuration > Backup with Encryption enabled) |
| Core: Backup | Automatic configuration backup to an FTP, SFTP, HTTP, or HTTPS server | 1.0.0 | NDM `SRG-APP-000516-NDM-000340`; ASD `APSC-DV-003070`; ASD `APSC-DV-002440` | `config system backup`; `set status enable`; `set cipher <PASSWORD>`; `set type change-based`; `set server-type sftp`; `set server-address <STRING>`; `end` |
| Core: Backup | Configuration revisions and configuration scripts | 1.0.0 | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000516-NDM-000340` | — |
| Core: Firmware | Firmware upload and upgrade (in maintenance mode) | 1.0.0 | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000378-NDM-000302`; ASD `APSC-DV-002630`; ASD `APSC-DV-003240` | GUI: System > Firmware (upgrade to each security release within 30 days); GUI: User Management > Role (Allow Firmware Upgrade & Backups only for the administrators who need it) |
| Core: Firmware | FortiPAM and FortiGuard licenses | 1.0.0 | NDM `SRG-APP-001035-NDM-000340`; ASD `APSC-DV-003240` | GUI: System > FortiPAM License |
| Core: Secret storage | Private data encryption with a custom key (Secure password storage) | 1.0.0 | NDM `SRG-APP-000171-NDM-000258`; NDM `SRG-APP-000231-NDM-000271`; ASD `APSC-DV-002330`; ASD `APSC-DV-002340`; ASD `APSC-DV-002350` | `config system global`; `set private-data-encryption enable`; `end` |
| Core: Secret storage | Trusted Platform Module (TPM) and vTPM storage of the encryption password | 1.0.0 | NDM `SRG-APP-000171-NDM-000258`; ASD `APSC-DV-002350` | `config system global`; `set v-tpm enable`; `end` |
| Core: Secret storage | Viewing secret passwords, passphrases, and SSH keys (View Encrypted Information permission) | 1.0.0 | NDM `SRG-APP-000178-NDM-000264`; ASD `APSC-DV-001850`; ASD `APSC-DV-000960` | GUI: User Management > Role (Secret: View Encrypted Information disabled except for the roles that must see clear text) |
| Core: Secrets | Credential vault (secrets for servers, network devices, and web accounts) | 1.0.0 | ASD `APSC-DV-001610`; ASD `APSC-DV-001540`; ASD `APSC-DV-002330` | GUI: Secrets > Secrets |
| Core: Secrets | Secret sharing permissions (user, group, and device tag) | 1.0.0 | ASD `APSC-DV-000470`; ASD `APSC-DV-000460`; NDM `SRG-APP-000329-NDM-000287` | GUI: Secrets > Secrets (Sharing: only the users and groups that need each secret; Owner and Edit permissions kept to a few users) |
| Core: Secrets | Personal and public folders with inherited secret policies | 1.0.0 | ASD `APSC-DV-000470`; ASD `APSC-DV-000460` | GUI: Secrets > Personal Folder |
| Core: Secrets | Secret policies (password changing, session recording, proxy mode, tunnel encryption, checkout, approval, clipboard, and SSH filter) | 1.0.0 | ASD `APSC-DV-000590`; ASD `APSC-DV-000290`; ASD `APSC-DV-002440`; ASD `APSC-DV-000460` | GUI: Secret Settings > Policies (Session Recording, Proxy Mode, Tunnel Encryption, Requires Checkout, and Requires Approval to Launch Secret enabled for privileged secrets) |
| Core: Secrets | Session recording of launched secrets | 1.0.0 | ASD `APSC-DV-000590`; ASD `APSC-DV-000840`; NDM `SRG-APP-000080-NDM-000220` | GUI: Secret Settings > Policies (Session Recording: Enable) |
| Core: Secrets | Proxy mode and tunnel encryption for launched sessions | 1.0.0 | ASD `APSC-DV-002440`; ASD `APSC-DV-001950` | GUI: Secret Settings > Policies (Proxy Mode: Enable; Tunnel Encryption: Enable) |
| Core: Secrets | Check-out and check-in of secrets (exclusive access) | 1.0.0 | ASD `APSC-DV-000290`; ASD `APSC-DV-000590` | GUI: Secret Settings > Policies (Requires Checkout: Enable; Checkin Password Change enabled) |
| Core: Secrets | Automatic password changing and verification (password rotation) | 1.0.0 | ASD `APSC-DV-000290` | GUI: Secret Settings > Policies (Automatic Password Changing: Enable, at the organization's rotation interval; Automatic Password Verification: Enable) |
| Core: Secrets | Password changers, password policies, and character sets for secrets | 1.0.0 | ASD `APSC-DV-000290` | GUI: Secret Settings > Password Changers |
| Core: Secrets | Approval profiles and approval workflow for secret access | 1.0.0 | ASD `APSC-DV-000460`; ASD `APSC-DV-000500` | GUI: Secret Settings > Approval Profile (approvers other than the requester; tiers as required) |
| Core: Secrets | Secret launchers and templates (native and web launchers) | 1.0.0 | ASD `APSC-DV-001500` | GUI: Secret Settings > Launchers (only the launchers in use) |
| Core: Secrets | Jobs and job requests on secrets | 1.0.0 | ASD `APSC-DV-000460`; ASD `APSC-DV-000520` | GUI: Secrets > Jobs |
| Core: Session control | SSH filter profiles (blocked commands and channels) | 1.0.0 | ASD `APSC-DV-000500`; ASD `APSC-DV-001030` | GUI: Secret Settings > SSH Filter Profiles (block channels that are not needed, such as x11, port-forward, tun-forward, and sftp) |
| Core: Session control | Block RDP clipboard | 1.0.0 | ASD `APSC-DV-002380` | GUI: Secret Settings > Policies (Block Clipboard: Enable where data transfer is not approved) |
| Core: Session control | Antivirus scanning of file transfers | 1.0.0 | ASD `APSC-DV-002380` | GUI: Secret Settings > AntiVirus |
| Core: Session control | Data leak prevention (DLP) sensors for file transfers | 1.0.0 | ASD `APSC-DV-002380` | GUI: Secret Settings > Data Leak Prevention |
| Core: Session control | Maximum launching duration for secret sessions | 1.0.0 | ASD `APSC-DV-002000` | GUI: System > Settings (Other: Max Launching Duration set to the organization's limit) |
| Core: ZTNA | ZTNA tags and ZTNA-based access control to FortiPAM and to secrets | 1.0.0 | NDM `SRG-APP-000038-NDM-000213`; ASD `APSC-DV-000490` | GUI: System > ZTNA |
| Core: Network | Static routes | 1.0.0 | NDM `SRG-APP-000880-NDM-000290` | GUI: Network > Static Routes (management traffic routed through the management network) |
| Core: Network | DNS settings | 1.0.0 | NDM `SRG-APP-000142-NDM-000245` | GUI: Network > DNS Settings |
| Core: Network | Packet capture | 1.0.0 | NDM `SRG-APP-000142-NDM-000245`; ASD `APSC-DV-000960` | GUI: User Management > Role (Network: Packet Capture None except for the administrators who troubleshoot) |
| Core: Platform | Hardware appliances and FortiPAM-VM on KVM and VMware | 1.0.0 | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Platform | FortiClient and the Fortinet Privileged Access Agent browser extension on user endpoints | 1.0.0 | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiPAM 1000G and 3000G hardware platforms | 1.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | CLI commands to check the hard disk and RAID status | 1.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `diagnose system raid status` |
| ZTNA | Simplified ZTNA proxy rule GUI (ZTNA servers and new proxy rules in the CLI only) | 1.1.0 and later | NDM `SRG-APP-000038-NDM-000213`; ASD `APSC-DV-000490` | GUI: System > ZTNA |
| Backup | Backup server port, server certificate check, server CA certificate, and connectivity test | 1.1.0 and later | NDM `SRG-APP-000516-NDM-000340`; ASD `APSC-DV-002440` | `config system backup`; `set server-type https`; `set server-identity-check enable`; `set ca-cert <CA_CERT>`; `end` |
| Session control | DLP sensors, filter rules, and file patterns in the GUI | 1.1.0 and later | ASD `APSC-DV-002380` | GUI: Secret Settings > Data Leak Prevention |
| Secrets | Secret GUI updates (template field values, SFTP service toggle, and service toggles for launchers) | 1.1.0 and later | ASD `APSC-DV-001500` | GUI: Secrets > Secrets (Service Setting: only the services in use) |
| Platform | RAID status and disk health commands on FortiPAM 1000G and 3000G | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `diagnose system disk info` |
| Platform | FortiPAM on Microsoft Hyper-V | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Antivirus and DLP log pages in Log & Report | 1.1.0 and later | ASD `APSC-DV-002380`; NDM `SRG-APP-000095-NDM-000225` | — |
| GUI | General GUI reorganization (folders, requests, approvals, and the Secret Settings menu) | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Approvals | Sending, approving, and denying multiple secret and job requests together | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | Client software integrity check for launchers | 1.1.0 and later | ASD `APSC-DV-002770`; NDM `SRG-APP-000131-NDM-000243` | GUI: Secret Settings > Client Software (an entry with the approved version for each launcher) |
| GUI | Secret name shown when editing a secret | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Licensing | Tooltip when the number of users exceeds the licensed seats | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | Allowed and blocked addresses for a secret (address filter) | 1.1.0 and later | ASD `APSC-DV-000490`; NDM `SRG-APP-000038-NDM-000213` | GUI: Secrets > Secrets (Address Filter: an allowlist of the approved target addresses) |
| Platform | FortiPAM on Microsoft Azure | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | TOTP settings for secrets whose targets require TOTP | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | Target Only secret template (user-specific login to a credential-less target) | 1.1.0 and later | ASD `APSC-DV-001540`; ASD `APSC-DV-001610` | GUI: Secret Settings > Templates |
| Launchers and templates | Editable Launcher pane in default secret templates | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | User and group permissions on secret templates | 1.1.0 and later | ASD `APSC-DV-000460` | GUI: Secret Settings > Templates (template access limited to the users and groups that need it) |
| Launchers and templates | New default secret templates (Cisco XR Router, ESXi Server, Database Server, and others) | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | New default launchers (MySQL CLI, Microsoft SQL CLI, MySQL Shell, PostgreSQL CLI, SSH CLI, SecureCRT, and others) | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Secret Settings > Launchers (remove launchers that are not used) |
| Logging | Debug log download and the trace logs tool in the GUI | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Log & Report > Debug Settings (Debug disabled except during troubleshooting) |
| GUI | Only enabled users listed by default | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Secret video download | 1.1.0 and later | ASD `APSC-DV-001280` | GUI: User Management > Role (View Secret Launching Video only for auditors) |
| Approvals | Timer showing the remaining access time of an approved request | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Token ID for SSH logs and links to the secret log and video | 1.1.0 and later | ASD `APSC-DV-001030`; NDM `SRG-APP-000101-NDM-000231` | — |
| Secrets | Job status column | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Password changing | New default password changers (Cisco XR Router and ESXi) | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Users and authentication | Customized user role type | 1.1.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287`; ASD `APSC-DV-000460` | GUI: User Management > Role (custom roles with only the pages each user needs) |
| Logging | Critical system and general email alerts for each user | 1.1.0 and later | NDM `SRG-APP-000795-NDM-000130`; ASD `APSC-DV-001110` | GUI: User Management > User List (Critical System Email Alert enabled for the SA and ISSO accounts) |
| ZTNA | ZTNA-based access control for folders | 1.1.0 and later | NDM `SRG-APP-000038-NDM-000213`; ASD `APSC-DV-000490` | GUI: Secrets > Personal Folder (ZTNA Control with device tags where endpoint posture is required) |
| Users and authentication | Default everyone user group | 1.1.0 and later | ASD `APSC-DV-000460` | GUI: User Management > User Groups (do not grant secret permissions to the everyone group) |
| Secrets | Cloning secret policies | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | System settings divided into General and Advanced tabs (Admin Session Timeout renamed User Session Timeout) | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Test email service | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management access | Login disclaimer in the GUI, with the last successful login | 1.1.0 and later | NDM `SRG-APP-000068-NDM-000215`; NDM `SRG-APP-000069-NDM-000216`; ASD `APSC-DV-000550`; ASD `APSC-DV-000560`; ASD `APSC-DV-000580` | GUI: System > Settings (Other General Settings, Login Disclaimer: enabled, with the Standard Mandatory DoD Notice and Consent Banner); `config system global`; `set post-login-banner enable`; `end` |
| Secrets | Display number and custom port for the VNC service | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Approvals | Bypass of the request and approval process by secret owners | 1.1.0 and later | ASD `APSC-DV-000460`; ASD `APSC-DV-000500` | GUI: Secret Settings > Policies (Bypass Approval: Disable for privileged secrets) |
| Logging | Automation triggers on event logs (CLI) | 1.1.0 and later | ASD `APSC-DV-000380`; ASD `APSC-DV-000390`; ASD `APSC-DV-000400`; ASD `APSC-DV-000410`; ASD `APSC-DV-000430`; NDM `SRG-APP-000795-NDM-000130` | GUI: Log & Report > Automation (stitches that email the SA and ISSO on account creation, change, disabling, enabling, and removal events) |
| Licensing | Email alerts for license expiry | 1.1.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Log & Report > Email Alert Settings |
| Secrets | Secure import of secrets with an encrypted secret upload template | 1.1.0 and later | ASD `APSC-DV-002330` | GUI: Secrets > Secrets (encrypt the secret upload template; delete the file after import) |
| Session control | Secret launching rate control against DoS attacks | 1.1.2 and later | ASD `APSC-DV-002400`; NDM `SRG-APP-000435-NDM-000315` | — |
| Session control | DLP filter rule shows the filter type | 1.1.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Secret last launch time column | 1.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Users and authentication | Sponsored groups and the sponsor admin role | 1.2.0 and later | NDM `SRG-APP-000033-NDM-000212`; ASD `APSC-DV-000460` | GUI: User Management > Sponsored Groups (sponsor admins only where delegated user management is approved) |
| Secrets | Secret targets created separately, with mandatory classification tags | 1.2.0 and later | ASD `APSC-DV-000460` | GUI: Secrets > Targets |
| Password changing | Regular expressions for the expect string in password changing procedures | 1.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Users and authentication | AntiVirus and DLP profile access control in roles | 1.2.0 and later | NDM `SRG-APP-000033-NDM-000212`; ASD `APSC-DV-001410` | GUI: User Management > Role |
| Launchers and templates | New launchers (HeidiSQL, SSMS, MobaXterm, Xshell), templates, and the ESXi Web password changer | 1.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Secret Settings > Launchers (remove launchers that are not used) |
| GUI | Favorite secrets page | 1.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | RDP event filter profiles (logs of events during RDP sessions) | 1.2.0 and later | ASD `APSC-DV-000840`; ASD `APSC-DV-000590` | GUI: Secret Settings > RDP Event Filter Profile |
| Licensing | Stackable seat license for hardware models | 1.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | System settings GUI reorganization and the Live Recording option | 1.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiPAM on Google Cloud Platform (GCP) | 1.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Password changing | Minimum SSL/TLS version and port for the LDAPS password changer and verification | 1.2.0 and later | ASD `APSC-DV-002440`; ASD `APSC-DV-001750` | `config secret target`; `edit <TARGET_NAME>`; `set ldaps-min-ssl-version TLSv1.2`; `next`; `end` |
| Secrets | Button to generate a secret password from the password policy | 1.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | Bypass of the SSH command filter by secret owners | 1.2.0 and later | ASD `APSC-DV-000500`; ASD `APSC-DV-001030` | GUI: Secret Settings > Policies (Bypass For Owner disabled for the SSH filter) |
| Logging | User location and source location in the user monitor and active sessions | 1.2.0 and later | NDM `SRG-APP-000097-NDM-000227`; ASD `APSC-DV-000690` | — |
| Logging | Report layout customization in the GUI | 1.2.0 and later | ASD `APSC-DV-001180` | GUI: Log & Report > Reports |
| Logging | Secret access audit report | 1.2.0 and later | ASD `APSC-DV-001180`; ASD `APSC-DV-000860` | GUI: Log & Report > Reports |
| Users and authentication | User group permissions | 1.2.0 and later | ASD `APSC-DV-000460` | GUI: User Management > User Groups |
| Platform | FortiPAM on Amazon Web Services (AWS) | 1.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Logs stored on FortiAnalyzer, with the upload interval | 1.2.0 and later | ASD `APSC-DV-001070`; ASD `APSC-DV-001080`; NDM `SRG-APP-000515-NDM-000325` | GUI: Network > Fabric Connectors (FortiAnalyzer upload in real time) |
| Session control | FortiPAM web proxy for browser extension launches (no credentials delivered to the client) | 1.2.0 and later | ASD `APSC-DV-002330`; ASD `APSC-DV-002440` | GUI: Network > Interfaces (Explicit Web Proxy only on one interface, only when web launches use it) |
| Management access | Last failed login time in the disclaimer | 1.2.0 and later | ASD `APSC-DV-000580` | — |
| GUI | Description column in the secret list | 1.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | Deauthenticating a user and disconnecting launched secret sessions | 1.2.0 and later | ASD `APSC-DV-001800`; ASD `APSC-DV-002000` | GUI: Monitoring > User Monitor (Terminate: Deauthenticate & Disconnect for users being removed) |
| Certificates | Download button for the web proxy CA certificate | 1.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management access | Concurrent log-on option for a user account | 1.2.0 and later | NDM `SRG-APP-000001-NDM-000200`; ASD `APSC-DV-000010` | GUI: System > Settings (Concurrent Log-on: Disable); `config system global`; `set admin-concurrent disable`; `end` |
| Users and authentication | View Secret Log and View Secret Video permissions in roles | 1.2.0 and later | ASD `APSC-DV-001280`; NDM `SRG-APP-000121-NDM-000238` | GUI: User Management > Role |
| Session control | Over-the-shoulder monitoring (live recording) | 1.2.0 and later | ASD `APSC-DV-000590`; ASD `APSC-DV-000840` | GUI: System > Settings (Live Recording enabled where live monitoring is required) |
| Network and gateways | Distributed architecture with network gateways (FortiPAM, FortiGate, or FortiProxy) | 1.3.0 and later | NDM `SRG-APP-000880-NDM-000290`; ASD `APSC-DV-002440` | GUI: Network > Secret Gateway |
| Users and authentication | Two-factor authentication status column in the user list | 1.3.0 and later | NDM `SRG-APP-000820-NDM-000170`; ASD `APSC-DV-001550` | — |
| Users and authentication | Automated remote user provisioning with auto provision rules | 1.3.0 and later | ASD `APSC-DV-000330`; NDM `SRG-APP-000516-NDM-000336` | GUI: User Management > Auto Provision Rules (rules that map only approved remote groups to roles) |
| ZTNA | Inherited ZTNA control settings shown for subfolders | 1.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | vTPM for FortiPAM on GCP | 1.3.0 and later | ASD `APSC-DV-002350` | `config system global`; `set v-tpm enable`; `end` |
| Logging | Log export as JSON and CSV files | 1.3.0 and later | ASD `APSC-DV-001180` | — |
| Launchers and templates | Web Telnet launcher | 1.3.0 and later | NDM `SRG-APP-000142-NDM-000245`; ASD `APSC-DV-001500` | GUI: Secret Settings > Launchers (Telnet launchers only where the target supports nothing else, with Tunnel Encryption) |
| Secrets | Password visible only to the user checking out the secret | 1.3.0 and later | ASD `APSC-DV-000290`; ASD `APSC-DV-001850` | GUI: Secret Settings > Policies (Requires Checkout: Enable) |
| Users and authentication | Import of remote LDAP users | 1.3.0 and later | NDM `SRG-APP-000516-NDM-000336` | GUI: User Management > User List |
| Users and authentication | Remote server option when creating a remote user | 1.3.0 and later | NDM `SRG-APP-000516-NDM-000336` | — |
| Management access | Replacement messages (login page, login token page, post-login disclaimer, and DLP pages) | 1.3.0 and later | NDM `SRG-APP-000068-NDM-000215`; ASD `APSC-DV-000550` | GUI: System > Replacement Messages (Login Page: add the Standard Mandatory DoD Notice and Consent Banner text) |
| Users and authentication | User deletion with transfer of owned resources | 1.3.0 and later | ASD `APSC-DV-000370`; ASD `APSC-DV-000330` | GUI: User Management > User List |
| Approvals | Minimum secret permission for approvers | 1.3.0 and later | ASD `APSC-DV-000460` | GUI: Secret Settings > Approval Profile |
| Approvals | Email notification to approver groups | 1.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Sender address for all emails | 1.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Log and video disk encryption | 1.3.0 and later | ASD `APSC-DV-001280`; ASD `APSC-DV-001290`; ASD `APSC-DV-002350`; NDM `SRG-APP-000119-NDM-000236` | `config system maintenance`; `set mode enable`; `end`; `execute disk encryption enable` |
| Approvals | Immediate secret access on approval (Start Upon Approval) | 1.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Approvals | Requester and approver time zones | 1.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Secret creation time column | 1.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Approvals | Customized email templates for secret requests | 1.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | RDP auto TOTP delivery for the FortiAuthenticator agent | 1.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | Auto discovery of accounts and resources (Secret Discovery permission) | 1.3.0 and later | ASD `APSC-DV-000460` | GUI: Secrets > Discovery |
| Platform | Increased secret capacity | 1.3.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Password changing | Dependency updater for service account credentials | 1.3.0 and later | ASD `APSC-DV-000290` | GUI: Secret Settings > Dependency Updater |
| Logging | Service account logs and new secret log columns | 1.3.0 and later | NDM `SRG-APP-000097-NDM-000227`; ASD `APSC-DV-000950` | — |
| Network and gateways | Reverse gateway mode for distributed architecture | 1.4.0 and later | NDM `SRG-APP-000880-NDM-000290`; ASD `APSC-DV-002440` | GUI: Network > Secret Gateway |
| Secrets | Launching a target with associated secret credentials on all launchers | 1.4.0 and later | ASD `APSC-DV-001610` | — |
| Password changing | Maximum credential history in a template | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Active launch monitor replaces the active session monitor | 1.4.0 and later | NDM `SRG-APP-000343-NDM-000289` | GUI: Monitoring > Active Sessions |
| Secrets | Warning for duplicated credentials | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | Launcher (service) permissions in secrets | 1.4.0 and later | ASD `APSC-DV-000460`; ASD `APSC-DV-000470` | GUI: Secrets > Secrets (each user granted only the launchers they need) |
| Launchers and templates | Microsoft SQL, MySQL, and PostgreSQL secret templates | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Full folder path display | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | Website login with TOTP and exact auto filling in the web extension | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Password changing | FortiProduct (Web) template and Web API password changer for FortiGate and FortiProxy | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | Block copy for web-based launchers | 1.4.0 and later | ASD `APSC-DV-002380` | GUI: Secret Settings > Policies (Block Clipboard: Enable) |
| Session control | Ctrl+C and Ctrl+V in Web RDP sessions | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | Certificate Vault template (certificates and private keys as secrets, with expiry monitoring) | 1.4.0 and later | ASD `APSC-DV-002330` | — |
| Session control | SSH filter Allow mode (allow listed commands, deny the rest) | 1.4.0 and later | ASD `APSC-DV-000500`; ASD `APSC-DV-001030` | GUI: Secret Settings > SSH Filter Profiles (Allow mode for targets where the permitted commands are known) |
| Integration | Ansible lookup plugin for API users | 1.4.0 and later | NDM `SRG-APP-000340-NDM-000288` | GUI: User Management > User List (API users only for approved automation, with the narrowest role) |
| Logging | SQL Server Management Studio (SSMS) monitoring and logging | 1.4.0 and later | ASD `APSC-DV-000960`; ASD `APSC-DV-001030` | GUI: Secrets > Targets (SQL Log enabled for Microsoft SQL targets) |
| GUI | Launcher buttons shown as icons | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | Privileged account display for a target | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | System time watermark on session videos | 1.4.0 and later | ASD `APSC-DV-000590`; NDM `SRG-APP-000096-NDM-000226` | GUI: System > Settings (Video Time Watermark enabled) |
| Approvals | Approval links in approval request emails, with an expiry time | 1.4.0 and later | ASD `APSC-DV-000460` | GUI: Secret Settings > Approval Profile (Approval Link Expiry Time short, or approval links not used) |
| Approvals | Custom fields such as a ticket number in secret requests | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | Web Telnet service setting in secrets | 1.4.0 and later | NDM `SRG-APP-000142-NDM-000245`; ASD `APSC-DV-001500` | GUI: Secrets > Secrets (Telnet service disabled unless the target supports nothing else) |
| Session control | Windows application filter on Windows targets | 1.4.0 and later | ASD `APSC-DV-000500` | GUI: Secret Settings > Windows App Control |
| Session control | Launching sessions terminated at the end of a user's login schedule | 1.4.0 and later | ASD `APSC-DV-002000`; ASD `APSC-DV-000490` | GUI: User Management > Schedule (Terminate Launching Session: True) |
| Secrets | Secret import matched to existing targets | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Creation time column for user groups and sponsored groups | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management access | Single login per user (Concurrent Log-on disabled) | 1.4.0 and later | NDM `SRG-APP-000001-NDM-000200`; ASD `APSC-DV-000010` | GUI: System > Settings (Concurrent Log-on: Disable) |
| Backup | Automatic backup of the in-use configuration before a restore | 1.4.0 and later | NDM `SRG-APP-000516-NDM-000340`; ASD `APSC-DV-003070` | — |
| Secret storage | AES-256 protection of passwords and keys | 1.4.0 and later | ASD `APSC-DV-002350`; NDM `SRG-APP-000171-NDM-000258` | — |
| Backup | FTP backup and restore of video and log files | 1.4.0 and later | ASD `APSC-DV-001340` | — |
| Logging | Filters in the report layout | 1.4.0 and later | ASD `APSC-DV-001140`; ASD `APSC-DV-001180` | — |
| Network | Network interface GUI refactor (Access column and Service Access Setting pane) | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | GUI warnings for log and video disk failure | 1.4.0 and later | ASD `APSC-DV-001110`; NDM `SRG-APP-000360-NDM-000295` | — |
| Certificates | ACME and Let's Encrypt certificates | 1.4.0 and later | NDM `SRG-APP-000516-NDM-000344`; ASD `APSC-DV-002300` | GUI: System > Certificates (do not use Let's Encrypt certificates on DoD networks; use DoD-issued certificates) |
| Logging | Automation stitches for email notifications (nine default stitches) | 1.4.0 and later | ASD `APSC-DV-000380`; ASD `APSC-DV-000390`; ASD `APSC-DV-000400`; ASD `APSC-DV-000410`; ASD `APSC-DV-000430`; NDM `SRG-APP-000795-NDM-000130` | GUI: Log & Report > Automation (stitches for account events and secret activity, emailing the SA and ISSO) |
| Users and authentication | FortiToken Cloud trial | 1.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Private data, vTPM, and disk encryption status in the banner and System > Settings | 1.4.0 and later | ASD `APSC-DV-002350` | GUI: System > Settings (Security: check Private Data Encryption, Virtual TPM, and Disk Encryption) |
| Logging | Log and video disk usage charts | 1.4.0 and later | ASD `APSC-DV-001090`; NDM `SRG-APP-000357-NDM-000293` | GUI: Log & Report > Disk Usage |
| Network and gateways | Service gateway mode | 1.5.0 and later | NDM `SRG-APP-000880-NDM-000290` | GUI: Network > Secret Gateway |
| Session control | Agentless mode for web-based secret launch | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Secret event subscription (email notifications of secret events) | 1.5.0 and later | ASD `APSC-DV-000860` | — |
| Launchers and templates | New default templates (Azure Credential, Azure AD Account, VNC Server, and others) and a password changer | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | RealVNC Viewer launcher | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | Launchers for multiple operating systems | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | Launcher start-up timeout | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | Certificate authentication for SSH launches | 1.5.0 and later | ASD `APSC-DV-001810` | — |
| Approvals | Approval by replying to the approval request email | 1.5.0 and later | ASD `APSC-DV-000460` | GUI: System > Settings (Approval Email Server only if email approval is approved) |
| GUI | Secret creation tabs for remote servers and stored certificates or files | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Network and gateways | Health checks for forward gateways | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | RPC parameter in the SQL Server session log | 1.5.0 and later | ASD `APSC-DV-000960` | — |
| Password changing | Web API password changer type with web changers and verifiers | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Password changing | HTTP PATCH method for the Web API password changer | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | Force checkout after an idle time | 1.5.0 and later | ASD `APSC-DV-000290` | GUI: Secret Settings > Policies (Force Checkout Idle time set to the organization's limit) |
| Logging | Configuration, login, and secret access logs on the user details page | 1.5.0 and later | ASD `APSC-DV-000830`; ASD `APSC-DV-000860` | — |
| Users and authentication | Third-party authenticators for user two-factor authentication | 1.5.0 and later | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000156-NDM-000250`; ASD `APSC-DV-001550` | GUI: User Management > User List (Third-Party Authenticator only where FortiToken is not used) |
| Management access | User profile menu (last login time, last login IP, and last failed login) | 1.5.0 and later | ASD `APSC-DV-000580` | — |
| Users and authentication | A user's related secrets and secret logs | 1.5.0 and later | ASD `APSC-DV-000460` | — |
| GUI | Multiple language support | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Session videos sent to external storage through SFTP | 1.5.0 and later | ASD `APSC-DV-001340`; ASD `APSC-DV-001070` | `config secret remote-storage`; `set status enable`; `set server <SERVER>`; `end` |
| Session control | PAC file for the browser extension | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Graphical view in Log & Report | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Licensing | Floating license (VM) | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Setup wizard | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Integration | Terraform provider | 1.5.0 and later | NDM `SRG-APP-000340-NDM-000288` | GUI: User Management > User List (API users only for approved automation) |
| Platform | FortiPAM on Alibaba Cloud | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiPAM on Proxmox | 1.5.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Approvals | Maximum request duration in approval profiles | 1.6.0 and later | ASD `APSC-DV-000460` | GUI: Secret Settings > Approval Profile (Maximum Request Duration set to the organization's limit) |
| Password changing | vCenter template and Web API password changer | 1.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | Unidirectional file transmission control | 1.6.0 and later | ASD `APSC-DV-002380` | GUI: Secrets > Secrets (file transfer only in the approved direction) |
| Approvals | Request exemption on schedule | 1.6.0 and later | ASD `APSC-DV-000460` | GUI: Secret Settings > Approval Profile (request exemptions only when approved) |
| Password changing | Renamed FortiProduct templates and password changers | 1.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | Key-value pair vault | 1.6.0 and later | ASD `APSC-DV-002330` | — |
| Secrets | Smart association (account prefix with the logged-in username) | 1.6.0 and later | ASD `APSC-DV-001540` | — |
| Secrets | Web Launcher access for users with View permission | 1.6.0 and later | ASD `APSC-DV-000460` | — |
| GUI | Secret template selection page | 1.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | Initialization commands in proxy and non-proxy mode | 1.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Password changing | Password reconciliation for Windows AD over LDAPS | 1.6.0 and later | ASD `APSC-DV-000290`; ASD `APSC-DV-002440` | — |
| Secrets | Unix and FortiOS discovery | 1.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Secrets > Discovery |
| Network and gateways | Web Launcher through a service gateway | 1.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | File storage in secrets | 1.6.0 and later | ASD `APSC-DV-002330`; ASD `APSC-DV-002380` | GUI: System > Settings (File Setting: Maximum File Size and Block File With No Extension) |
| Users and authentication | One-time invitation of external users to a secret | 1.6.0 and later | ASD `APSC-DV-000300`; ASD `APSC-DV-001870` | GUI: Monitoring (Invited Users tab: revoke invitations that are no longer needed) |
| Integration | JSON Web Token (JWT) integration with DevOps platforms | 1.6.0 and later | NDM `SRG-APP-000340-NDM-000288`; ASD `APSC-DV-001540` | GUI: User Management > JWT Key Management |
| Users and authentication | Simplified interface for guest and invited users | 1.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Italian language | 1.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Certificates | Custom CA certificate for the web proxy | 1.6.0 and later | ASD `APSC-DV-002300`; NDM `SRG-APP-000910-NDM-000300` | GUI: Network > Interfaces (Explicit Web Proxy, CA Certificate: an organization CA) |
| Logging | FortiAnalyzer Cloud logging | 1.6.0 and later | ASD `APSC-DV-001070` | GUI: Network > Fabric Connectors |
| Logging | Copy the location of a video stored remotely | 1.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Secret configuration page (Settings, Sharing, and Audit tabs) | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | MobaXterm-sftp launcher | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | Antivirus and DLP for secret file uploads | 1.7.0 and later | ASD `APSC-DV-002380` | GUI: Secrets > Secrets (Antivirus Scan and DLP Status enabled for File secrets) |
| Launchers and templates | Configurable SSH terminal types | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Password changing | Default maximum delay for the password changer increased | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | SSH algorithm negotiation strength for secrets and policies | 1.7.0 and later | ASD `APSC-DV-002440`; ASD `APSC-DV-001940` | GUI: Secret Settings > Policies (SSH Algorithm Negotiation: high-encryption) |
| Secrets | Target auto match and creation | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | Native RDP connection diagnostics | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Password changing | PAN-OS and SSH Password For Root (Unix) password changers | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Network and gateways | Targets with the same IP address behind different gateways | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | Discovery auto-onboarding for Windows AD | 1.7.0 and later | ASD `APSC-DV-000460` | GUI: Secrets > Discovery (auto-onboarding rules that place accounts in folders with the right policy) |
| Launchers and templates | OT application launchers (TIA Portal) | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Web Launcher renamed Web Browsing | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | FortiClient script commands, multiprocess mode, and full-screen recording | 1.7.0 and later | ASD `APSC-DV-000590` | — |
| Launchers and templates | Radmin launcher | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management access | Restricting a user to console login only | 1.7.0 and later | NDM `SRG-APP-000408-NDM-000314` | `config system admin`; `edit <USERNAME>`; `set login-restriction-console enable`; `next`; `end` |
| Users and authentication | JWT user type | 1.7.0 and later | NDM `SRG-APP-000340-NDM-000288` | GUI: User Management > JWT Key Management (Lease Duration short) |
| Platform | Up to 3000 users on FortiPAM 1000G | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Export of session videos in playable webm format | 1.7.0 and later | ASD `APSC-DV-001340` | — |
| Logging | SSH log entries linked to the video timestamp | 1.7.0 and later | ASD `APSC-DV-001030`; ASD `APSC-DV-000590` | — |
| Logging | Secret ID, folder ID, and folder path in secret audit reports | 1.7.0 and later | ASD `APSC-DV-001180` | — |
| Management access | Single global minimum TLS version (System > Settings), per interface, and per SQL target | 1.7.0 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; ASD `APSC-DV-002440`; ASD `APSC-DV-001950` | GUI: System > Settings (Security, Minimum SSL Version: TLSv1-2 or TLSv1-3) |
| Logging | Video access audit logs | 1.7.0 and later | ASD `APSC-DV-001280`; ASD `APSC-DV-000860` | — |
| Launchers and templates | Browser extension download from Client Software | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiPAM on Nutanix | 1.7.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | Custom resolution for Web RDP | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | RDP connection failure diagnosis for end users | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | Folder edit refactor | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | DLP log, antivirus log, and requests and jobs tabs on the secret edit page | 1.8.0 and later | ASD `APSC-DV-000860` | — |
| Password changing | Secret password expiry notification | 1.8.0 and later | ASD `APSC-DV-000290` | GUI: System > Settings (Secret Password Expiration Notification) |
| Password changing | Credential replacement for Siemens TIA Portal Cloud | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Password changing | Web API password changer CSRF token extraction and multi-layer JSON bodies | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Password changing | SSH password changer for FortiOS 7.6.3 and higher | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | New line mode for SSH script jobs | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | PowerShell jobs | 1.8.0 and later | ASD `APSC-DV-000520` | — |
| ZTNA | Service Address field type for multiple ZTNA tunnels | 1.8.0 and later | NDM `SRG-APP-000038-NDM-000213` | — |
| Users and authentication | Regular expression match for JWT users | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | Concurrent secret launch limit (global and per user) | 1.8.0 and later | ASD `APSC-DV-002400`; NDM `SRG-APP-000435-NDM-000315` | GUI: System > Settings (Max Launched Sessions set to the organization's limit) |
| Users and authentication | Email address and display name for auto-provisioned SAML users | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Users and authentication | User SSO cache (last-selected SSO provider) | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Users and authentication | Signed SAML assertion and response required | 1.8.0 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000156-NDM-000250` | `config user saml`; `edit <NAME>`; `set require-signed-resp-and-asrt enable`; `next`; `end` |
| System | Proxy FQDN for request email notifications | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Users and authentication | Invited users page and invitation revocation | 1.8.0 and later | ASD `APSC-DV-000300` | GUI: Monitoring (Invited Users tab) |
| Licensing | Concurrent logon licensing (VM) | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Users and authentication | Automatic disabling of inactive auto-provisioned remote users | 1.8.0 and later | ASD `APSC-DV-000320`; ASD `APSC-DV-000330` | GUI: System > Settings (Provisioned User Auto-purging, User Max Inactivity Days: 35) |
| Management access | Allowed roles for the GUI portal of each interface | 1.8.0 and later | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000880-NDM-000290` | `config system interface`; `edit <PORT>`; `set gui-access-role <ROLES>`; `next`; `end` |
| Logging | Key-based SFTP authentication for remote video storage | 1.8.0 and later | ASD `APSC-DV-001340` | GUI: System > Backup (Remote Video Storage, Authentication Method: Keypair) |
| Backup | Key-based SFTP authentication for automatic backup | 1.8.0 and later | NDM `SRG-APP-000516-NDM-000340` | GUI: System > Backup (Configuration Backup, Authentication Method: Keypair) |
| Logging | Session close logs and other secret log enhancements | 1.8.0 and later | ASD `APSC-DV-000850` | — |
| Logging | System and secret logs pushed to the syslog server | 1.8.0 and later | ASD `APSC-DV-001070`; ASD `APSC-DV-001080`; NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350` | GUI: Log & Report > Log Settings (Send logs to syslog enabled) |
| Platform | FortiPAM 1100G hardware model | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiSRA consolidated into FortiPAM | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiPAM on Oracle Cloud Infrastructure (OCI) | 1.8.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | TCP forwarding for native RDP launches | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | Launcher privilege (user or system level) | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | Kerberos authentication for native RDP sessions | 1.9.0 and later | ASD `APSC-DV-002440` | — |
| Network and gateways | Viewer and Owner permissions for secret gateways | 1.9.0 and later | ASD `APSC-DV-000460` | GUI: Network > Secret Gateway |
| Approvals | Approval email server using Microsoft Graph | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | Just-in-time (JIT) privilege through checkout and check-in PowerShell scripts | 1.9.0 and later | ASD `APSC-DV-000460`; ASD `APSC-DV-000500` | GUI: Secrets > JIT Script |
| Secrets | Additional authentication to access or launch secrets | 1.9.0 and later | ASD `APSC-DV-001520` | GUI: Secret Settings > Policies (Access Authentication: Enable for privileged secrets; Bypass For Owner disabled) |
| Network and gateways | Secret gateway chaining | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | Launcher process matcher | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | One secret for multiple approved target hosts | 1.9.0 and later | ASD `APSC-DV-000490` | — |
| Approvals | Revoking approved secret access requests | 1.9.0 and later | ASD `APSC-DV-000460` | GUI: Secrets > Approvals |
| Session control | Load balancing information for Web RDP targets | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Users and authentication | Email address and display name for auto-provisioned LDAP users | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | Non-TOTP two-factor challenges in WebSSH | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Users and authentication | Wildcard remote users | 1.9.0 and later | ASD `APSC-DV-001540` | GUI: User Management > User List (no wildcard users for administrator roles) |
| Users and authentication | SCIM service for identity lifecycle management | 1.9.0 and later | ASD `APSC-DV-000330`; NDM `SRG-APP-000142-NDM-000245` | GUI: User Management > SCIM Service |
| Users and authentication | Message-Authenticator for RADIUS | 1.9.0 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000156-NDM-000250` | `config user radius`; `edit <SERVER>`; `set require-message-authenticator enable`; `next`; `end` |
| Users and authentication | Automatic purging of disabled auto-provisioned users | 1.9.0 and later | ASD `APSC-DV-000330` | GUI: System > Settings (Provisioned User Auto-purging, User Max Disabled Days) |
| Secrets | Guest instructions (instruction profiles) | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: System > Settings (Guest Instruction Feature disabled unless used) |
| Availability | FortiPAM-VM active-passive HA on OCI | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiPAM 400G hardware model | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiPAM 100G hardware model (gateway only) | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management access | New login page with clear-text password view during entry | 1.9.0 and later | NDM `SRG-APP-000178-NDM-000264`; ASD `APSC-DV-001850` | — |
| Network | TCP segmentation offload and generic segmentation offload | 1.9.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | Oracle SQL Developer launcher | 1.9.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Approvals | Blocking self approval | 1.9.1 and later | ASD `APSC-DV-000460`; ASD `APSC-DV-000500` | GUI: Secret Settings > Approval Profile (Self Approval disabled) |
| Secrets | Enforce launching with SSO (the user's own credentials) | 7.0.0 and later | ASD `APSC-DV-001540`; ASD `APSC-DV-001610` | GUI: Secret Settings > Templates (Enforce launching with SSO for domain targets) |
| Secrets | JIT scripts in the secret request approval workflow | 7.0.0 and later | ASD `APSC-DV-000460` | GUI: Secret Settings > Approval Profile |
| Session control | Windows Remote App | 7.0.0 and later | ASD `APSC-DV-000460` | GUI: Secret Settings > Windows App Control |
| Launchers and templates | SSMS-stable launcher with Windows authentication | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Password changing | Web API password changer for FortiOS 7.6.3 and higher | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Secrets | Associated secrets in the secret upload template | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Session control | SSH host key verification | 7.0.0 and later | ASD `APSC-DV-002440`; ASD `APSC-DV-001940` | — |
| Password changing | Visual graph editor for SSH password changers and verifiers | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Launchers and templates | Portable Agent (standalone launch client) | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Users and authentication | SAML metadata import and export | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Users and authentication | LDAP servers through a gateway | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Users and authentication | User certificate authentication for FortiPAM login | 7.0.0 and later | NDM `SRG-APP-000149-NDM-000247`; NDM `SRG-APP-000177-NDM-000263`; NDM `SRG-APP-000175-NDM-000262`; ASD `APSC-DV-001560`; ASD `APSC-DV-001570`; ASD `APSC-DV-001810`; ASD `APSC-DV-001830` | GUI: User Management > Authentication Settings (Enable Certificate Authentication; CA Certificate: DoD root and intermediate CAs); GUI: User Management > User List (Certificate Authentication enabled for each user) |
| Users and authentication | FIDO2 (WebAuthn) passkey sign-in for local users | 7.0.0 and later | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000156-NDM-000250`; ASD `APSC-DV-001550` | GUI: User Management > User List (Passkey only for approved local users) |
| Users and authentication | RADIUS server page redesign and credential test | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Firmware | Dual-signed firmware images | 7.0.0 and later | NDM `SRG-APP-000131-NDM-000243`; ASD `APSC-DV-001430` | — |
| ZTNA | Custom CA for ZTNA EMS certificates | 7.0.0 and later | NDM `SRG-APP-000910-NDM-000300`; ASD `APSC-DV-002300` | — |
| Logging | Secret gateway events | 7.0.0 and later | NDM `SRG-APP-000095-NDM-000225` | GUI: Log & Report > Network Event |
| Management access | Periodic checks for unauthorized configuration changes | 7.0.0 and later | ASD `APSC-DV-002770`; NDM `SRG-APP-000795-NDM-000130` | `config system global`; `set config-period-check enable`; `end` |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current releases. The SRG ID column gives the SRG
requirement each rule implements (for NDM rows it is the first part of the
requirement ID):

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/24-fortipam-feature-version-and-srg-map-requirements.csv) (183 rows).

| SRG | Requirement | Severity | SRG ID | Requirement title |
| --- | --- | --- | --- | --- |
| NDM | `SRG-APP-000001-NDM-000200` | CAT II | `SRG-APP-000001` | The network device must limit the number of concurrent sessions to an organization-defined number for each administrator account and/or administrator account type. |
| NDM | `SRG-APP-000026-NDM-000208` | CAT II | `SRG-APP-000026` | The network device must automatically audit account creation. |
| NDM | `SRG-APP-000027-NDM-000209` | CAT II | `SRG-APP-000027` | The network device must automatically audit account modification. |
| NDM | `SRG-APP-000028-NDM-000210` | CAT II | `SRG-APP-000028` | The network device must automatically audit account disabling actions. |
| NDM | `SRG-APP-000029-NDM-000211` | CAT II | `SRG-APP-000029` | The network device must automatically audit account removal actions. |
| NDM | `SRG-APP-000033-NDM-000212` | CAT I | `SRG-APP-000033` | The network device must be configured to assign appropriate user roles or access levels to authenticated users. |
| NDM | `SRG-APP-000038-NDM-000213` | CAT II | `SRG-APP-000038` | The network device must enforce approved authorizations for controlling the flow of management information within the network device based on information flow control policies. |
| NDM | `SRG-APP-000065-NDM-000214` | CAT II | `SRG-APP-000065` | The network device must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must block any login attempt for 15 minutes. |
| NDM | `SRG-APP-000068-NDM-000215` | CAT II | `SRG-APP-000068` | The network device must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the device. |
| NDM | `SRG-APP-000069-NDM-000216` | CAT II | `SRG-APP-000069` | The network device must retain the Standard Mandatory DoD Notice and Consent Banner on the screen until the administrator acknowledges the usage conditions and takes explicit actions to log on for further access. |
| NDM | `SRG-APP-000080-NDM-000220` | CAT II | `SRG-APP-000080` | The network device must protect against an individual (or process acting on behalf of an individual) falsely denying having performed organization-defined actions to be covered by non-repudiation. |
| NDM | `SRG-APP-000095-NDM-000225` | CAT II | `SRG-APP-000095` | The network device must produce audit log records containing sufficient information to establish what type of event occurred. |
| NDM | `SRG-APP-000096-NDM-000226` | CAT II | `SRG-APP-000096` | The network device must produce audit records containing information to establish when (date and time) the events occurred. |
| NDM | `SRG-APP-000097-NDM-000227` | CAT II | `SRG-APP-000097` | The network device must produce audit records containing information to establish where the events occurred. |
| NDM | `SRG-APP-000098-NDM-000228` | CAT II | `SRG-APP-000098` | The network device must produce audit log records containing information to establish the source of events. |
| NDM | `SRG-APP-000099-NDM-000229` | CAT II | `SRG-APP-000099` | The network device must produce audit records that contain information to establish the outcome of the event. |
| NDM | `SRG-APP-000100-NDM-000230` | CAT II | `SRG-APP-000100` | The network device must generate audit records containing information that establishes the identity of any individual or process associated with the event. |
| NDM | `SRG-APP-000101-NDM-000231` | CAT II | `SRG-APP-000101` | The network device must generate audit records containing the full-text recording of privileged commands. |
| NDM | `SRG-APP-000116-NDM-000234` | CAT II | `SRG-APP-000116` | The network device must use internal system clocks to generate time stamps for audit records. |
| NDM | `SRG-APP-000119-NDM-000236` | CAT II | `SRG-APP-000119` | The network device must protect audit information from unauthorized modification. |
| NDM | `SRG-APP-000120-NDM-000237` | CAT II | `SRG-APP-000120` | The network device must protect audit information from unauthorized deletion. |
| NDM | `SRG-APP-000121-NDM-000238` | CAT II | `SRG-APP-000121` | The network device must protect audit tools from unauthorized access. |
| NDM | `SRG-APP-000131-NDM-000243` | CAT II | `SRG-APP-000131` | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| NDM | `SRG-APP-000142-NDM-000245` | CAT I | `SRG-APP-000142` | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services |
| NDM | `SRG-APP-000148-NDM-000346` | CAT II | `SRG-APP-000148` | The network device must be configured with only one local account to be used as the account of last resort in the event the authentication server is unavailable. |
| NDM | `SRG-APP-000149-NDM-000247` | CAT I | `SRG-APP-000149` | The network device must be configured to use DoD PKI as multi-factor authentication (MFA) for interactive logins. |
| NDM | `SRG-APP-000153-NDM-000249` | CAT II | `SRG-APP-000153` | The network device must be configured to authenticate each administrator prior to authorizing privileges based on assignment of group or role. |
| NDM | `SRG-APP-000156-NDM-000250` | CAT II | `SRG-APP-000156` | The network device must implement replay-resistant authentication mechanisms for network access to privileged accounts. |
| NDM | `SRG-APP-000164-NDM-000252` | CAT II | `SRG-APP-000164` | The network device must enforce a minimum 15-character password length. |
| NDM | `SRG-APP-000166-NDM-000254` | CAT II | `SRG-APP-000166` | The network device must enforce password complexity by requiring that at least one uppercase character be used. |
| NDM | `SRG-APP-000167-NDM-000255` | CAT II | `SRG-APP-000167` | The network device must enforce password complexity by requiring that at least one lowercase character be used. |
| NDM | `SRG-APP-000168-NDM-000256` | CAT II | `SRG-APP-000168` | The network device must enforce password complexity by requiring that at least one numeric character be used. |
| NDM | `SRG-APP-000169-NDM-000257` | CAT II | `SRG-APP-000169` | The network device must enforce password complexity by requiring that at least one special character be used. |
| NDM | `SRG-APP-000170-NDM-000329` | CAT II | `SRG-APP-000170` | The network device must require that when a password is changed, the characters are changed in at least eight of the positions within the password. |
| NDM | `SRG-APP-000171-NDM-000258` | CAT I | `SRG-APP-000171` | The network device must be configured to store passwords using an approved salted key derivation function, preferably using a keyed hash for password-based authentication. |
| NDM | `SRG-APP-000172-NDM-000259` | CAT I | `SRG-APP-000172` | The network device must transmit only encrypted representations of passwords. |
| NDM | `SRG-APP-000175-NDM-000262` | CAT I | `SRG-APP-000175` | The network device must be configured to use DoD approved OCSP responders or CRLs to validate certificates used for PKI-based authentication. |
| NDM | `SRG-APP-000177-NDM-000263` | CAT I | `SRG-APP-000177` | The network device, for PKI-based authentication, must be configured to map validated certificates to unique user accounts. |
| NDM | `SRG-APP-000178-NDM-000264` | CAT I | `SRG-APP-000178` | The network device must obscure feedback of authentication information during the authentication process to protect the information from possible exploitation/use by unauthorized individuals. |
| NDM | `SRG-APP-000179-NDM-000265` | CAT I | `SRG-APP-000179` | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| NDM | `SRG-APP-000190-NDM-000267` | CAT I | `SRG-APP-000190` | The network device must terminate all network connections associated with a device management session at the end of the session, or the session must be terminated after five minutes of inactivity except to fulfill documented and validated mission requirements. |
| NDM | `SRG-APP-000220-NDM-000268` | CAT II | `SRG-APP-000220` | The network device must invalidate session identifiers upon administrator logout or other session termination. |
| NDM | `SRG-APP-000231-NDM-000271` | CAT I | `SRG-APP-000231` | The network device must only allow authorized administrators to view or change the device configuration, system files, and other files stored either in the device or on removable media (such as a flash drive). |
| NDM | `SRG-APP-000296-NDM-000280` | CAT II | `SRG-APP-000296` | The network device must be configured to provide a logout mechanism for administrator-initiated communication sessions. |
| NDM | `SRG-APP-000319-NDM-000283` | CAT II | `SRG-APP-000319` | The network device must automatically audit account enabling actions. |
| NDM | `SRG-APP-000329-NDM-000287` | CAT II | `SRG-APP-000329` | If the network device uses role-based access control, the network device must enforce organization-defined role-based access control policies over defined subjects and objects. |
| NDM | `SRG-APP-000340-NDM-000288` | CAT I | `SRG-APP-000340` | The network device must prevent non-privileged users from executing privileged functions to include disabling, circumventing, or altering implemented security safeguards/countermeasures. |
| NDM | `SRG-APP-000343-NDM-000289` | CAT II | `SRG-APP-000343` | The network device must audit the execution of privileged functions. |
| NDM | `SRG-APP-000357-NDM-000293` | CAT II | `SRG-APP-000357` | The network device must allocate audit record storage capacity in accordance with organization-defined audit record storage requirements. |
| NDM | `SRG-APP-000360-NDM-000295` | CAT II | `SRG-APP-000360` | The network device must generate an immediate real-time alert of all audit failure events requiring real-time alerts. |
| NDM | `SRG-APP-000374-NDM-000299` | CAT II | `SRG-APP-000374` | The network device must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). |
| NDM | `SRG-APP-000378-NDM-000302` | CAT II | `SRG-APP-000378` | The network device must prohibit installation of software without explicit privileged status. |
| NDM | `SRG-APP-000380-NDM-000304` | CAT II | `SRG-APP-000380` | The network device must enforce access restrictions associated with changes to device configuration. |
| NDM | `SRG-APP-000381-NDM-000305` | CAT II | `SRG-APP-000381` | The network device must audit the enforcement actions used to restrict access associated with changes to the device. |
| NDM | `SRG-APP-000395-NDM-000310` | CAT II | `SRG-APP-000395` | The network device must be configured to authenticate SNMP messages using a FIPS-validated Keyed-Hash Message Authentication Code (HMAC). |
| NDM | `SRG-APP-000395-NDM-000347` | CAT II | `SRG-APP-000395` | The network device must authenticate Network Time Protocol sources using authentication that is cryptographically based. |
| NDM | `SRG-APP-000408-NDM-000314` | CAT II | `SRG-APP-000408` | Network devices performing maintenance functions must restrict use of these functions to authorized personnel only. |
| NDM | `SRG-APP-000411-NDM-000330` | CAT I | `SRG-APP-000411` | The network devices must use FIPS-validated Keyed-Hash Message Authentication Code (HMAC) to protect the integrity of nonlocal maintenance and diagnostic communications. |
| NDM | `SRG-APP-000412-NDM-000331` | CAT I | `SRG-APP-000412` | The network device must be configured to implement cryptographic mechanisms using a FIPS 140-2 approved algorithm to protect the confidentiality of remote maintenance sessions |
| NDM | `SRG-APP-000435-NDM-000315` | CAT II | `SRG-APP-000435` | The network device must be configured to protect against known types of denial-of-service (DoS) attacks by employing organization-defined security safeguards. |
| NDM | `SRG-APP-000457-NDM-000352` | CAT II | `SRG-APP-000457` | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| NDM | `SRG-APP-000503-NDM-000320` | CAT II | `SRG-APP-000503` | The network device must generate audit records when successful/unsuccessful logon attempts occur. |
| NDM | `SRG-APP-000504-NDM-000321` | CAT II | `SRG-APP-000504` | The network device must generate audit records for privileged activities or other system-level access. |
| NDM | `SRG-APP-000505-NDM-000322` | CAT II | `SRG-APP-000505` | The network device must generate audit records showing starting and ending time for administrator access to the system. |
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | `SRG-APP-000515` | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000317` | CAT II | `SRG-APP-000516` | The network device must be configured in accordance with the security configuration settings based on DoD security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. |
| NDM | `SRG-APP-000516-NDM-000335` | CAT II | `SRG-APP-000516` | The network device must enforce access restrictions associated with changes to the system components. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | `SRG-APP-000516` | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | `SRG-APP-000516` | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000344` | CAT II | `SRG-APP-000516` | The network device must obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | `SRG-APP-000516` | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000795-NDM-000130` | CAT II | `SRG-APP-000795` | The network device must be configured to alert organization-defined personnel or roles upon detection of unauthorized access, modification, or deletion of audit information. |
| NDM | `SRG-APP-000820-NDM-000170` | CAT II | `SRG-APP-000820` | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| NDM | `SRG-APP-000825-NDM-000180` | CAT II | `SRG-APP-000825` | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that the device meets organization-defined strength of mechanism requirements. |
| NDM | `SRG-APP-000845-NDM-000220` | CAT II | `SRG-APP-000845` | The network device must be configured to verify, when users create or update passwords, the passwords are not found on the list of commonly used, expected, or compromised passwords in IA-5 (1) (a) for password-based authentication. |
| NDM | `SRG-APP-000860-NDM-000250` | CAT II | `SRG-APP-000860` | The network device must be configured to allow user selection of long passwords and passphrases, including spaces and all printable characters for password-based authentication. |
| NDM | `SRG-APP-000875-NDM-000280` | CAT II | `SRG-APP-000875` | The network device must be configured to implement certificate revocation checking to support path discovery and validation for public key-based authentication. |
| NDM | `SRG-APP-000880-NDM-000290` | CAT II | `SRG-APP-000880` | The network device must be configured to protect nonlocal maintenance sessions by separating the maintenance session from other network sessions with the system by logically separated communications paths. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | `SRG-APP-000910` | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | `SRG-APP-000920` | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-000925-NDM-000330` | CAT II | `SRG-APP-000925` | The network device must be configured to compare the internal system clocks on an organization-defined frequency with organization-defined authoritative time source. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | `SRG-APP-001035` | The network device hardware and software must be a version supported by the vendor. |
| ASD | `APSC-DV-000010` | CAT II | `SRG-APP-000001` | The application must provide a capability to limit the number of logon sessions per user. |
| ASD | `APSC-DV-000070` | CAT II | `SRG-APP-000295` | The application must automatically terminate the non-privileged user session and log off non-privileged users after a 15 minute idle time period has elapsed. |
| ASD | `APSC-DV-000080` | CAT II | `SRG-APP-000295` | The application must automatically terminate the admin user session and log off admin users after a 10 minute idle time period is exceeded. |
| ASD | `APSC-DV-000090` | CAT II | `SRG-APP-000296` | Applications requiring user access authentication must provide a logoff capability for user initiated communication session. |
| ASD | `APSC-DV-000290` | CAT II | `SRG-APP-000317` | Shared/group account credentials must be terminated when members leave the group. |
| ASD | `APSC-DV-000300` | CAT II | `SRG-APP-000024` | The application must automatically remove or disable temporary user accounts 72 hours after account creation. |
| ASD | `APSC-DV-000320` | CAT III | `SRG-APP-000025` | The application must automatically disable accounts after a 35 day period of account inactivity. |
| ASD | `APSC-DV-000330` | CAT II | `SRG-APP-000025` | Unnecessary application accounts must be disabled, or deleted. |
| ASD | `APSC-DV-000340` | CAT II | `SRG-APP-000026` | The application must automatically audit account creation. |
| ASD | `APSC-DV-000350` | CAT II | `SRG-APP-000027` | The application must automatically audit account modification. |
| ASD | `APSC-DV-000360` | CAT II | `SRG-APP-000028` | The application must automatically audit account disabling actions. |
| ASD | `APSC-DV-000370` | CAT II | `SRG-APP-000029` | The application must automatically audit account removal actions. |
| ASD | `APSC-DV-000380` | CAT III | `SRG-APP-000291` | The application must notify system administrators (SAs) and information system security officers (ISSOs) when accounts are created. |
| ASD | `APSC-DV-000390` | CAT III | `SRG-APP-000292` | The application must notify system administrators (SAs) and information system security officers (ISSOs) when accounts are modified. |
| ASD | `APSC-DV-000400` | CAT III | `SRG-APP-000293` | The application must notify system administrators (SAs) and information system security officers (ISSOs) of account disabling actions. |
| ASD | `APSC-DV-000410` | CAT III | `SRG-APP-000294` | The application must notify system administrators (SAs) and information system security officers (ISSOs) of account removal actions. |
| ASD | `APSC-DV-000420` | CAT II | `SRG-APP-000319` | The application must automatically audit account enabling actions. |
| ASD | `APSC-DV-000430` | CAT III | `SRG-APP-000320` | The application must notify system administrators (SAs) and information system security officers (ISSOs) of account enabling actions. |
| ASD | `APSC-DV-000460` | CAT I | `SRG-APP-000033` | The application must enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies. |
| ASD | `APSC-DV-000470` | CAT II | `SRG-APP-000328` | The application must enforce organization-defined discretionary access control policies over defined subjects and objects. |
| ASD | `APSC-DV-000490` | CAT II | `SRG-APP-000039` | The application must enforce approved authorizations for controlling the flow of information between interconnected systems based on organization-defined information flow control policies. |
| ASD | `APSC-DV-000500` | CAT II | `SRG-APP-000340` | The application must prevent non-privileged users from executing privileged functions to include disabling, circumventing, or altering implemented security safeguards/countermeasures. |
| ASD | `APSC-DV-000520` | CAT II | `SRG-APP-000343` | The application must audit the execution of privileged functions. |
| ASD | `APSC-DV-000530` | CAT I | `SRG-APP-000065` | The application must enforce the limit of three consecutive invalid logon attempts by a user during a 15 minute time period. |
| ASD | `APSC-DV-000550` | CAT III | `SRG-APP-000068` | The application must display the Standard Mandatory DoW Notice and Consent Banner before granting access to the application. |
| ASD | `APSC-DV-000560` | CAT III | `SRG-APP-000069` | The application must retain the Standard Mandatory DoW Notice and Consent Banner on the screen until users acknowledge the usage conditions and take explicit actions to log on for further access. |
| ASD | `APSC-DV-000580` | CAT III | `SRG-APP-000075` | The application must display the time and date of the users last successful logon. |
| ASD | `APSC-DV-000590` | CAT II | `SRG-APP-000080` | The application must protect against an individual (or process acting on behalf of an individual) falsely denying having performed organization-defined actions to be covered by non-repudiation. |
| ASD | `APSC-DV-000650` | CAT II | `SRG-APP-000089` | The application must not write sensitive data into the application logs. |
| ASD | `APSC-DV-000690` | CAT II | `SRG-APP-000089` | The application must provide audit record generation capability for connecting system IP addresses. |
| ASD | `APSC-DV-000830` | CAT II | `SRG-APP-000503` | The application must generate audit records when successful/unsuccessful logon attempts occur. |
| ASD | `APSC-DV-000840` | CAT II | `SRG-APP-000504` | The application must generate audit records for privileged activities or other system-level access. |
| ASD | `APSC-DV-000850` | CAT II | `SRG-APP-000505` | The application must generate audit records showing starting and ending time for user access to the system. |
| ASD | `APSC-DV-000860` | CAT II | `SRG-APP-000507` | The application must generate audit records when successful/unsuccessful accesses to objects occur. |
| ASD | `APSC-DV-000880` | CAT II | `SRG-APP-000509` | The application must generate audit records for all account creations, modifications, disabling, and termination events. |
| ASD | `APSC-DV-000950` | CAT II | `SRG-APP-000095` | The application must log destination IP addresses. |
| ASD | `APSC-DV-000960` | CAT II | `SRG-APP-000095` | The application must log user actions involving access to data. |
| ASD | `APSC-DV-000970` | CAT II | `SRG-APP-000095` | The application must log user actions involving changes to data. |
| ASD | `APSC-DV-001030` | CAT II | `SRG-APP-000101` | The application must generate audit records containing the full-text recording of privileged commands or the individual identities of group account users. |
| ASD | `APSC-DV-001070` | CAT II | `SRG-APP-000358` | The application must off-load audit records onto a different system or media than the system being audited. |
| ASD | `APSC-DV-001080` | CAT II | `SRG-APP-000515` | The application must be configured to write application logs to a centralized log repository. |
| ASD | `APSC-DV-001090` | CAT II | `SRG-APP-000359` | The application must provide an immediate warning to the SA and ISSO (at a minimum) when allocated audit record storage volume reaches 75% of repository maximum audit record storage capacity. |
| ASD | `APSC-DV-001110` | CAT II | `SRG-APP-000108` | The application must alert the ISSO and SA (at a minimum) in the event of an audit processing failure. |
| ASD | `APSC-DV-001140` | CAT II | `SRG-APP-000115` | The application must provide the capability to filter audit records for events of interest based upon organization-defined criteria. |
| ASD | `APSC-DV-001180` | CAT II | `SRG-APP-000366` | The application must provide a report generation capability that supports on-demand audit review and analysis. |
| ASD | `APSC-DV-001250` | CAT II | `SRG-APP-000116` | The applications must use internal system clocks to generate time stamps for audit records. |
| ASD | `APSC-DV-001260` | CAT II | `SRG-APP-000374` | The application must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). |
| ASD | `APSC-DV-001280` | CAT II | `SRG-APP-000118` | The application must protect audit information from any type of unauthorized read access. |
| ASD | `APSC-DV-001290` | CAT II | `SRG-APP-000119` | The application must protect audit information from unauthorized modification. |
| ASD | `APSC-DV-001300` | CAT II | `SRG-APP-000120` | The application must protect audit information from unauthorized deletion. |
| ASD | `APSC-DV-001340` | CAT II | `SRG-APP-000125` | The application must back up audit records at least every seven days onto a different system or system component than the system or component being audited. |
| ASD | `APSC-DV-001410` | CAT II | `SRG-APP-000380` | The application must enforce access restrictions associated with changes to application configuration. |
| ASD | `APSC-DV-001420` | CAT II | `SRG-APP-000381` | The application must audit who makes configuration changes to the application. |
| ASD | `APSC-DV-001430` | CAT II | `SRG-APP-000131` | The application must have the capability to prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| ASD | `APSC-DV-001500` | CAT II | `SRG-APP-000141` | The application must be configured to disable non-essential capabilities. |
| ASD | `APSC-DV-001510` | CAT II | `SRG-APP-000142` | The application must be configured to use only functions, ports, and protocols permitted to it in the PPSM CAL. |
| ASD | `APSC-DV-001520` | CAT II | `SRG-APP-000389` | The application must require users to reauthenticate when organization-defined circumstances or situations require reauthentication. |
| ASD | `APSC-DV-001540` | CAT I | `SRG-APP-000148` | The application must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| ASD | `APSC-DV-001550` | CAT II | `SRG-APP-000149` | The application must use multifactor (Alt. Token) authentication for network access to privileged accounts. |
| ASD | `APSC-DV-001560` | CAT II | `SRG-APP-000391` | The application must accept Personal Identity Verification (PIV) credentials. |
| ASD | `APSC-DV-001570` | CAT II | `SRG-APP-000392` | The application must electronically verify Personal Identity Verification (PIV) credentials. |
| ASD | `APSC-DV-001580` | CAT II | `SRG-APP-000150` | The application must use multifactor (e.g., CAC, Alt. Token) authentication for network access to non-privileged accounts. |
| ASD | `APSC-DV-001610` | CAT II | `SRG-APP-000153` | The application must ensure users are authenticated with an individual authenticator prior to using a group authenticator. |
| ASD | `APSC-DV-001680` | CAT I | `SRG-APP-000164` | The application must enforce a minimum 15-character password length. |
| ASD | `APSC-DV-001690` | CAT II | `SRG-APP-000166` | The application must enforce password complexity by requiring that at least one uppercase character be used. |
| ASD | `APSC-DV-001700` | CAT II | `SRG-APP-000167` | The application must enforce password complexity by requiring that at least one lowercase character be used. |
| ASD | `APSC-DV-001710` | CAT II | `SRG-APP-000168` | The application must enforce password complexity by requiring that at least one numeric character be used. |
| ASD | `APSC-DV-001720` | CAT II | `SRG-APP-000169` | The application must enforce password complexity by requiring that at least one special character be used. |
| ASD | `APSC-DV-001730` | CAT II | `SRG-APP-000170` | The application must require the change of at least eight of the total number of characters when passwords are changed. |
| ASD | `APSC-DV-001740` | CAT I | `SRG-APP-000171` | The application must only store cryptographic representations of passwords. |
| ASD | `APSC-DV-001750` | CAT I | `SRG-APP-000172` | The application must transmit only cryptographically-protected passwords. |
| ASD | `APSC-DV-001760` | CAT II | `SRG-APP-000173` | The application must enforce 24 hours/1 day as the minimum password lifetime. |
| ASD | `APSC-DV-001770` | CAT II | `SRG-APP-000174` | The application must enforce a 180-day maximum password lifetime restriction. |
| ASD | `APSC-DV-001780` | CAT II | `SRG-APP-000165` | The application must prohibit password reuse for a minimum of five generations. |
| ASD | `APSC-DV-001800` | CAT II | `SRG-APP-000400` | The application must terminate existing user sessions upon account deletion. |
| ASD | `APSC-DV-001810` | CAT I | `SRG-APP-000175` | The application, when utilizing PKI-based authentication, must validate certificates by constructing a certification path (which includes status information) to an accepted trust anchor. |
| ASD | `APSC-DV-001830` | CAT II | `SRG-APP-000177` | The application must map the authenticated identity to the individual user or group account for PKI-based authentication. |
| ASD | `APSC-DV-001840` | CAT II | `SRG-APP-000401` | The application, for PKI-based authentication, must implement a local cache of revocation data to support path discovery and validation in case of the inability to access revocation information via the network. |
| ASD | `APSC-DV-001850` | CAT I | `SRG-APP-000178` | The application must not display passwords/PINs as clear text. |
| ASD | `APSC-DV-001860` | CAT I | `SRG-APP-000179` | The application must use mechanisms meeting the requirements of applicable federal laws, Executive Orders, directives, policies, regulations, standards, and guidance for authentication to a cryptographic module. |
| ASD | `APSC-DV-001870` | CAT II | `SRG-APP-000180` | The application must uniquely identify and authenticate non-organizational users (or processes acting on behalf of non-organizational users). |
| ASD | `APSC-DV-001940` | CAT II | `SRG-APP-000411` | Applications used for non-local maintenance sessions must implement cryptographic mechanisms to protect the integrity of non-local maintenance and diagnostic communications. |
| ASD | `APSC-DV-001950` | CAT II | `SRG-APP-000412` | Applications used for non-local maintenance sessions must implement cryptographic mechanisms to protect the confidentiality of non-local maintenance and diagnostic communications. |
| ASD | `APSC-DV-002000` | CAT II | `SRG-APP-000190` | The application must terminate all network connections associated with a communications session at the end of the session. |
| ASD | `APSC-DV-002040` | CAT II | `SRG-APP-000514` | The application must utilize FIPS-validated cryptographic modules when protecting unclassified information that requires cryptographic protection. |
| ASD | `APSC-DV-002300` | CAT II | `SRG-APP-000427` | The application must only allow the use of DoW-approved certificate authorities for verification of the establishment of protected sessions. |
| ASD | `APSC-DV-002330` | CAT II | `SRG-APP-000231` | The application must protect the confidentiality and integrity of stored information when required by DoW policy or the information owner. |
| ASD | `APSC-DV-002340` | CAT I | `SRG-APP-000428` | The application must implement approved cryptographic mechanisms to prevent unauthorized modification of organization-defined information at rest on organization-defined information system components. |
| ASD | `APSC-DV-002350` | CAT I | `SRG-APP-000429` | The application must use appropriate cryptography in order to protect stored DoW information when required by the information owner or DoW policy. |
| ASD | `APSC-DV-002380` | CAT II | `SRG-APP-000243` | Applications must prevent unauthorized and unintended information transfer via shared system resources. |
| ASD | `APSC-DV-002400` | CAT II | `SRG-APP-000246` | The application must restrict the ability to launch Denial of Service (DoS) attacks against itself or other information systems. |
| ASD | `APSC-DV-002440` | CAT I | `SRG-APP-000439` | The application must protect the confidentiality and integrity of transmitted information. |
| ASD | `APSC-DV-002630` | CAT II | `SRG-APP-000456` | Security-relevant software updates and patches must be kept up to date. |
| ASD | `APSC-DV-002770` | CAT II | `SRG-APP-000473` | The application must perform verification of the correct operation of security functions: upon system startup and/or restart; upon command by a user with privileged access; and/or every 30 days. |
| ASD | `APSC-DV-002900` | CAT II | `SRG-APP-000516` | The ISSO must ensure application audit trails are retained for at least 30 months (12 months active + 18 months cold storage) for applications without SAMI data and five years for applications including SAMI data. |
| ASD | `APSC-DV-002970` | CAT II | `SRG-APP-000516` | The ISSO must ensure if a DoW STIG or NSA guide is not available, a third-party product will be configured by following available guidance. |
| ASD | `APSC-DV-003070` | CAT II | `SRG-APP-000516` | Data backup must be performed at required intervals in accordance with DoW policy. |
| ASD | `APSC-DV-003240` | CAT I | `SRG-APP-000516` | All products must be supported by the vendor or the development team. |
| ASD | `APSC-DV-003270` | CAT II | `SRG-APP-000516` | Unnecessary built-in application accounts must be disabled. |
| ASD | `APSC-DV-003280` | CAT I | `SRG-APP-000516` | Default passwords must be changed. |
| ASD | `APSC-DV-003330` | CAT II | `SRG-APP-000516` | The system must alert an administrator when low resource conditions are encountered. |

### Collecting evidence

Run `get system status` on the CLI and keep the output with the
checklist, together with a configuration backup and the firmware version
from the *System Information* widget. Add screenshots or exports of the
panes the map cites, above all *System > Settings* (General, Email
Settings, and Advanced tabs), *Network > Interfaces*, *User Management >
User List*, *User Management > Role*, *User Management > LDAP Servers*,
*User Management > Authentication Settings*, *Secret Settings >
Policies*, *Secret Settings > Approval Profile*, *Secret Settings > SSH
Filter Profiles*, *Log & Report > Log Settings*, *Log & Report > Email
Alert Settings*, *System > HA*, *System > Certificates*, *System > SNMP*,
and *System > Backup*. Run `execute disk encryption status` and keep the
output. Generate a secret audit report from *Log & Report > Reports*,
export the system and secret logs from the central log server, and keep
the firmware upgrade history and the backup schedule.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiPAM.** Check the
  version column against the FortiPAM release, and check whether the
  feature depends on the model, the platform, the license, or the client
  (FortiClient or the browser extension version).
- **A setting is not where the map says.** The GUI was reorganized in
  several releases (the system settings in 1.1.0 and 1.2.0, the network
  interface page in 1.4.0, and the secret page in 1.7.0). Look for the
  setting under the older name, and check the Administration Guide of your
  release.
- **A command is rejected.** The commands were checked against the 7.0.0
  Administration Guide, because there is no CLI Reference. Use `?` on the
  CLI to list the options available at each level.
- **Users are locked out or cannot log in after hardening.** Check the
  trusted hosts, the login schedule, the allowed roles of the interface's
  GUI portal, the two-factor method, and (on 7.0.0) the certificate
  captive portal and the CA certificate. Remote RADIUS logins fail if the
  server does not send the Message-Authenticator attribute while
  `require-message-authenticator` is enabled.
- **Sessions fail through a TLS inspection device.** Enable *Tunnel
  Encryption* in the secret policy, as the guide requires when a device
  inspects HTTPS between FortiClient and FortiPAM.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (account reviews, checksum checks), by another system (the
  directory, the identity provider, the central log server), or not at
  all. Record how each requirement is met, not just which feature covers
  it.

## Security and Best Practices

- Keep FortiPAM on a vendor-supported release, and install patches
  promptly; on releases before 7.0.0, check the image checksum.
- Set the admin password at the first login and keep it as the one local
  account of last resort; give every other user a remote account, two
  factors, the narrowest role that works, and trusted hosts.
- Limit glass breaking, maintenance mode, CLI access, firmware upgrades,
  and *View Encrypted Information* to a few roles, and alert when glass
  breaking mode is used.
- Set the user password policy to 15 characters with all character types,
  8 new characters, no reuse, and 180-day expiration; set Max Retry to 3
  and Lockout Duration to 900 seconds; set the GUI session timeout to 10
  minutes; and disable concurrent log-on.
- Enable private data encryption, TPM or vTPM, and log and video disk
  encryption, and set the minimum TLS version to TLSv1-2 or higher.
- Record, proxy, and approve privileged sessions, rotate shared
  credentials automatically, and block self-approval.
- Send logs to a central server, store videos on SFTP, use SNMPv3 only,
  trust only DoD CAs, and back up the configuration with encryption.
- Review this map each time Fortinet publishes a FortiPAM release or DISA
  updates the NDM SRG or the ASD STIG.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiPAM Release Notes*, page "What's new", releases 1.0.1
  to 1.9.2 and 7.0.0, and page "Supported features" of release 1.0.0
  (docs.fortinet.com, FortiPAM documentation).
- Fortinet, *FortiPAM 7.0.0 Administration Guide*.
- Fortinet, *FortiPAM 1.0.0 Administration Guide* (for the core
  features).
- DISA Network Device Management SRG V5R5 and Application Security and
  Development STIG V6R5, from the October 2026 STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map), and
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the model for this chapter).

**Knowledge checks:**

1. Why does Chapter 10 assign FortiPAM the ASD STIG as well as the NDM
   SRG, and why does this chapter cite only some of its rules?
2. Where does the version data come from, and what does the 1.0.0
   "Supported features" page contribute?
3. Which secret policy settings make privileged sessions accountable, and
   which requirements do they support?
4. How does password rotation help meet the rule about shared account
   credentials?
5. How is the logon banner displayed on FortiPAM, and how do you record
   the difference from the requirement?
6. Which requirements can FortiPAM not meet exactly, and how do you
   handle them?

## Summary and Completion Checklist

FortiPAM has no STIG, so it is assessed against the NDM SRG for its
management plane and against the Application Security and Development
STIG rules that an administrator can configure or verify. This chapter
maps 366 features to the FortiPAM release that introduced them, to
183 requirements (82 NDM and 101 ASD), and to the FortiPAM
GUI pane or command that configures them: 85 core platform
features, and 281 features from the FortiPAM 1.0.1 through 7.0.0
release notes. Operational features with no direct requirement fall under
the requirement to prohibit unnecessary functions when unused.

- [ ] Can find the release that introduced a FortiPAM feature.
- [ ] Can map a FortiPAM feature to its NDM requirement or ASD rule.
- [ ] Can explain which ASD rules are in scope for an administrator and
  which are developer obligations.
- [ ] Can find the FortiPAM GUI pane or command that meets the
  requirement.
- [ ] Can collect FortiPAM's evidence and record the requirements it
  cannot meet exactly.
