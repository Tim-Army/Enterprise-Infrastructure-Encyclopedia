# Chapter 25: FortiNAC Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiNAC-F release that introduced a given feature.
- Map each FortiNAC-F feature to the Network Device Management (NDM) SRG
  requirement, the AAA Services SRG requirement, or the network access
  control (NAC) rule it helps satisfy.
- Explain why this chapter uses another vendor's NAC STIG (Cisco ISE) as
  the expected pattern for the network access function, and why those
  rules are not FortiNAC requirements.
- Find the FortiNAC-F CLI command, or the GUI pane, that configures each
  feature to meet its requirement.
- Use the map to scope an SRG-based assessment of FortiNAC-F, which has no
  STIG of its own.
- Record the requirements that FortiNAC-F cannot meet exactly, with their
  mitigations.

## Theory and Architecture

FortiNAC is Fortinet's network access control (NAC) product. It discovers
and inventories the switches, wireless controllers, access points,
firewalls, and VPN gateways of the network; finds every endpoint that
connects to them (through SNMP and CLI polling, MAC notification traps,
RADIUS, DHCP fingerprints, syslog, and integrations); profiles each
endpoint to decide what kind of device it is; checks the posture of
managed computers with its agents; and then enforces access by moving the
endpoint's switch port or SSID session into the right VLAN, applying an
ACL or filter ID, or sending a RADIUS Change of Authorization. Unknown
devices land in a registration network and a captive portal, failing
computers in a remediation network, and dangerous ones in a dead-end
network. FortiNAC can also be the RADIUS server for 802.1X, terminating
EAP itself or proxying to another server.

FortiNAC has **no DISA STIG** (Chapter 10), so it is assessed against
SRGs, as described in Chapter 03. Chapter 10 assigns it the **NDM SRG
plus the requirements for the network access function**, and notes that
DISA publishes STIGs for other NAC products that show the expected
pattern. For every FortiNAC feature the chapter gives **which FortiNAC-F
release introduced it**, **which requirement it relates to**, and **which
CLI command or GUI pane configures it to meet that requirement**.

**Scope: FortiNAC-F, not legacy FortiNAC.** With release F 7.2.0, Fortinet
re-versioned FortiNAC to "F 7.2" to match the Fortinet Fabric numbering
and moved it from CentOS 7 to FortiNAC-OS, a firmware image with a
FortiOS-like CLI. docs.fortinet.com still publishes the legacy FortiNAC
documentation (trains 8.3 to 9.4, with 9.4 release notes up to 9.4.8),
but those releases run on CentOS 7, which the FortiNAC-F release notes say
was coming to end of life by June 2024, and F 7.6 no longer supports
CentOS appliances at all. A legacy system therefore cannot meet the requirement
for a vendor-supported version (NDM `SRG-APP-001035-NDM-000340`), and its
answer to an assessment is migration, not configuration. This chapter
covers only the current FortiNAC-F line, trains **7.2**, **7.4**, and
**7.6**; FortiNAC-F has no 7.0 train, so 7.2.0 is its oldest release.

FortiNAC-F appliances come in a few roles. A **Control and Application
(CA)** server (FNC-CAX-VM or a FortiNAC-CA-500F, 600F, or 700F) does the
work; a **FortiNAC Manager** (FNC-MX-VM or FortiNAC-M-550F) manages many
CAs. Its configuration uses a few ideas again and again:

- **Two interfaces with two jobs.** *port1* is the management interface
  (the Admin UI, SSH, SNMP, RADIUS, syslog, and the agents), and *port2*
  serves the isolation networks (DHCP, DNS, and the captive portal). Which
  services each interface answers is set with `set allowaccess` in the
  CLI; FortiNAC-OS opens only a minimal set of ports by default.
- **The CLI and the Admin UI are separate.** The FortiNAC-OS CLI (over SSH
  or, from 7.6.3, a console in the GUI) configures the appliance: its
  interfaces, routes, DNS, NTP, HA, and global settings. Almost everything
  else, from administrators to policies, lives in the browser-based Admin
  UI, and the CLI accounts and Admin UI accounts are separate.
- **Profiles, policies, and logical networks.** *User/host profiles*
  select endpoints by who and what they are (groups, roles, device types,
  compliance, MDM data). *Network access policies* map a profile to a
  *logical network*, and each device model maps the logical network to a
  VLAN, an ACL, a filter ID, or a CoA profile. *Endpoint compliance
  policies* map a profile to the scans that an agent runs.
- **System settings.** *System > Settings* holds identification (device
  types, vendor OUIs), the Persistent Agent settings and TLS service
  configurations, system communication (log receivers, SNMP, email), and
  system management (NTP, backups, HA, licenses); *Users & Hosts >
  Administrators* holds the administrator accounts and profiles.

### Where the version data comes from

Fortinet publishes no Feature Matrix and no New Features Guide for
FortiNAC-F. Its **Release Notes**, however, have a "What's new" page for
every release, and the Administration Guide of each train repeats the
entries of its first release. docs.fortinet.com lists three FortiNAC-F
trains with 23 releases: **7.2.0 to 7.2.9**, **7.4.0 to 7.4.4**, and
**7.6.0 to 7.6.7**. The release notes are the best source: they are the
only document that lists the changes of every release. The version column
was built from the "What's new" page of all 23 releases (for 7.4, the
page of each release under the train's "What's new" chapter).

- Five pages say that the release has no new features: 7.2.8, 7.4.3,
  7.4.4, 7.6.4, and 7.6.6. The 7.2.4 and 7.2.5 pages only repeat the 7.2.2
  notice about server communication.
- Each heading on a page is one entry (on the 7.2.6 page, each row of its
  table; on the 7.6.1 and 7.6.7 pages, also each paragraph that starts a
  new topic without a heading). Sub-headings are folded into their parent.
  A notice repeated on a later page of the same train is counted once.
- The three trains were maintained in parallel, so the same feature is
  often listed in more than one train (MDM device ownership in 7.2.9,
  7.4.2, and 7.6.3, for example). Each listing is its own entry, and the
  map merges them into one row with one version per train.
- The HSTS entry on the 7.2.0 and 7.4.0 pages says that HSTS for the Admin
  GUI is enabled by default "in versions 9.4.5+, 7.2.4+, and 7.4.0+", so it
  is entered as 7.2.4 and 7.4.0.

That gives 141 entries: 19 in 7.2 (10 in 7.2.0, 1 each in 7.2.1,
7.2.2, 7.2.3, 7.2.4, 7.2.7, and 7.2.9, and 3 in 7.2.6), 27 in 7.4 (12 in
7.4.0, 4 in 7.4.1, and 11 in 7.4.2), and 95 in 7.6 (14 in 7.6.0, 2 in
7.6.1, 4 in 7.6.2, 31 in 7.6.3, 23 in 7.6.5, and 21 in 7.6.7). Each entry
title was taken from its heading and shortened where needed.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: management
  access, administrators and profiles, remote authentication, logging,
  time, SNMP, certificates, backups, firmware, HA, and the NAC functions
  themselves (discovery, profiling, policies, endpoint compliance,
  remediation, the local RADIUS server, guests, and the captive portal).
  Each one is described in the **FortiNAC F 7.2.0 Administration Guide**
  and, for the CLI, the **FortiNAC-OS 7.2.0 CLI Reference**, so it existed
  in the first FortiNAC-F release and is not in the release notes lists.
  Two core rows have a different version entry, explained below.
- **New features** are the 141 entries of the "What's new" pages,
  merged into 119 rows. The categories were assigned for this chapter,
  and the titles were shortened from the release notes text.

| Version entry | Meaning |
| --- | --- |
| `7.2.0` | A core feature described in the FortiNAC F 7.2.0 Administration Guide or the FortiNAC-OS 7.2.0 CLI Reference (the first FortiNAC-F release) |
| `7.6.0 and later` | Introduced in FortiNAC-F 7.6.0 (listed on its "What's new" page) |
| `7.2.9+; 7.4.2+; 7.6.3+` | Listed in each of those releases; the feature is in every later release of the train, and in the trains after the last one listed |
| `7.6 (release not stated)` | Documented in the 7.6.0 CLI Reference but not in the 7.4.0 CLI Reference, and in no "What's new" page (the CLI administrator lockout settings) |
| `7.2 (release not stated)` | Documented in the current revision of the 7.2.0 Administration Guide, but in no "What's new" page (Require Message-Authenticator, the BlastRADIUS protection) |

Three cautions apply. First, Fortinet revises the Administration Guides in
place: the 7.2.0 guide's change log has entries dated 8-12-2024 and
1-8-2026, and it already describes RadSec (introduced in 7.2.1), so a
core row records a capability of the 7.2 train, but a detail of it may
have arrived in a later 7.2 patch. Second, many features depend on the
license (the Plus and Pro license levels), the appliance (CentOS or
FortiNAC-OS, CA or Manager), or a third-party product (an MDM, an OT
platform, a wireless controller). Third, a row records a FortiNAC-F
capability, but its pane was checked against the 7.6.0 Administration
Guide and may be named or placed differently on an older release; the
guide also says that the CLI console is available from 7.6.1, while the
release notes list it in 7.6.3.

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG or STIG | Release | Applies to |
| --- | --- | --- | --- |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The management plane: administrator accounts and profiles, Admin UI and CLI access, lockout, idle timeout, cryptography for management, audit records, logging, time, SNMP, firmware, backups, and certificates |
| **AAA** | AAA Services SRG | V2R3, benchmark date 30 Sep 2026 | FortiNAC as a RADIUS server: 802.1X and EAP, shared secrets and RadSec, directory connections, PKI-based authentication of endpoints, guest and temporary accounts, and the audit of authentication transactions |
| **ISE** | Cisco ISE NAC STIG | V2R4, benchmark date 01 Jul 2026 | The expected pattern for the network access function: authorization by endpoint attributes, profiling, posture checks, remediation, logging and alerting, and authentication of endpoints. **Another vendor's STIG, not a FortiNAC requirement** |

The **NDM SRG** covers FortiNAC's administration, as it does for the
other Fortinet appliances in this volume.

The **AAA Services SRG** covers the RADIUS server inside FortiNAC.
FortiNAC's local RADIUS server terminates 802.1X EAP for wired and
wireless endpoints, proxies RADIUS to other servers, and authenticates
guests and users against local accounts, LDAP directories, and Entra ID.
Those are AAA services, so the map cites the AAA requirements for those
functions: secure EAP types, authenticating supplicants before the
authenticator connects them, unique shared secrets, encrypted credentials,
secure directory protocols, DoD PKI with revocation checking, removal of
temporary (guest) accounts, inactive accounts, the guest VLAN, and the
audit of each authentication. The map does not cite the AAA requirements
for FortiNAC's own administrators; the NDM SRG covers those.

**DISA publishes no NAC SRG.** The October 2026 library has no SRG for
network access control, but it has two STIGs for NAC products, each with
a separate NAC STIG for the access-control function: the **Cisco ISE NAC
STIG** V2R4 (30 rules, in `U_Cisco_ISE_Y26M07_STIG.zip`, beside
the Cisco ISE NDM STIG) and the **Ivanti Policy Secure NAC STIG** V1R1 (8
rules). The rules of both are built from the same requirement IDs of the
form `SRG-NET-nnnnnn-NAC-nnnnnn`, which DISA uses for NAC requirements
(the XCCDF group titles). This chapter uses the **Cisco ISE NAC STIG** as
the pattern for the network access function, because it is the more
complete of the two: it covers authorization, profiling, posture
(anti-malware, host firewall, and host IDS/IPS), remediation, bypass
approval, logging, alerting, MAB, and endpoint authentication, while the
Ivanti STIG has eight rules.

The ISE rules are cited by their STIG IDs, of the form `CSCO-NC-nnnnnn`,
with the abbreviation **ISE**, and the Requirement reference table gives
the SRG ID that each one implements. **Read every ISE entry as "the
pattern that DISA expects of a NAC product", not as a FortiNAC
requirement.** The rule text names Cisco ISE and its Comply-to-Connect
(C2C) steps; what carries over to FortiNAC is the underlying SRG
requirement and the behavior the rule checks. An assessor writing a
FortiNAC checklist should cite the SRG-NET NAC requirement and use the ISE
rule as the model for the check.

The requirement IDs are the **rule version IDs** from the XCCDF files,
and the severity is the rule's severity (high = CAT I, medium = CAT II,
low = CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiNAC meets a
  requirement. Device profiling rules implement the profiling of
  endpoints (ISE `CSCO-NC-000030`, CAT I in the ISE STIG), for example.
- **Must be configured to meet a requirement.** The feature is in scope
  of a requirement and has to be set up correctly. The local RADIUS server
  must allow only secure EAP types such as EAP-TLS, EAP-TTLS, and PEAP
  (AAA `SRG-APP-000516-AAA-000440`), for example.
- **No direct requirement.** The feature is operational, such as a device
  integration, a cloud image, an HA refinement, or a GUI change. It has no
  requirement of its own, but if it is not needed it falls under the NDM
  requirement to prohibit unnecessary functions, ports, protocols, and
  services (NDM `SRG-APP-000142-NDM-000245`). 72 rows are of this
  kind.

The mapping is a starting point for an assessment, not a ruling. Confirm
it with your assessor, especially the use of the Cisco ISE NAC STIG as a
pattern, the choice of AAA requirements, and the split between them.

### Where the commands come from

The **FortiNAC-F 7.6.0 CLI Reference Guide** (revised 15 July 2025), the
newest CLI Reference, is the source for every CLI command. It documents
each configuration context as a table of commands (`config system
global`, `config system interface`, `config system ntp`, `config system
admin`, and others) rather than as a FortiOS-style configuration tree. The
**FortiNAC-F 7.6.0 Administration Guide** is the source for every GUI
pane. docs.fortinet.com offers no PDF of the 7.6 guide, so its 696 online
pages were saved and joined into one text. The check was automatic: each
`config` statement selected the section of the CLI Reference for its
context, and each `set`, `append`, and `unselect` option had to appear in
that section, with each literal value among the documented values (or,
for numbers, in the documented range); each `execute` and `get` command
had to appear in the guide; and each GUI pane had to appear in the
Administration Guide as a page path or in its text. All 76 CLI statements
and 86 GUI panes passed. Read the column this way:

- **GUI:** entries name the FortiNAC Admin UI pane; the text in
  parentheses names the fields to set.
- Commands run on the FortiNAC-OS CLI, over SSH or in the console.
  Statements are separated by `;` to fit in a table cell; on the CLI,
  enter each one on its own line. Values in `<ANGLE_BRACKETS>` are
  placeholders for your own values.
- For **"No direct requirement"** rows, the entry shown is where the
  feature is turned off when it is unused. A dash (**—**) means there is
  nothing to change: the feature is a platform, a device integration, an
  HA behavior, a GUI change, or a capability that is off unless
  configured.

Some requirements cannot be met exactly with FortiNAC-F settings. Record
them on the checklist as open findings with mitigations, or meet them
another way:

- **No FIPS mode.** Neither the 7.6.0 CLI Reference nor the
  Administration Guide describes a FIPS or Common Criteria mode, so
  FIPS-validated cryptography for authentication and for remote management
  (NDM `SRG-APP-000179-NDM-000265`, NDM `SRG-APP-000412-NDM-000331`, CAT I)
  and for transmitted credentials (AAA `SRG-APP-000172-AAA-000520`) cannot
  be shown with a setting. Enable `strong-crypto`, allow only TLS 1.2 and
  TLS 1.3 in every TLS service configuration, and check the NIST
  Cryptographic Module Validation Program for your release.
- **No logon banner.** FortiNAC shows the End User License Agreement the
  first time an administrator logs in, but the guides document no Standard
  Mandatory DoD Notice and Consent Banner for the Admin UI or SSH (NDM
  `SRG-APP-000068-NDM-000215`, NDM `SRG-APP-000069-NDM-000216`). Reach the
  Admin UI and SSH only through a management jump host or gateway that
  displays the banner, and record the finding.
- **Local administrator passwords.** The Admin UI enforces only which
  characters a local administrator password may contain, and the CLI
  requires eight or more characters with the four character types. Neither sets a 15-character minimum, the eight-character change, or
  a check against a list of compromised passwords (NDM
  `SRG-APP-000164-NDM-000252`, NDM `SRG-APP-000170-NDM-000329`, NDM
  `SRG-APP-000845-NDM-000220`), and the guides do not say how passwords
  are stored (NDM `SRG-APP-000171-NDM-000258`). Authenticate administrators
  through LDAP or RADIUS, whose directory enforces the policy, and set the
  local and CLI passwords to 15 or more characters by procedure.
- **Lockout.** Administrator profiles set *Lock Out After Attempts* and a
  *Lock Out Duration* in seconds, with no 15-minute window for counting
  failures (NDM `SRG-APP-000065-NDM-000214`), and the guide says that only
  the *Inactivity Time* of the System Administrator profile can be
  modified. Set every other profile to 3 attempts and 900 seconds, keep
  the System Administrator profile for a few accounts, and on 7.6 set
  `admin-lockout-threshold` and `admin-lockout-duration` for the CLI.
- **Idle timeout.** The NDM SRG asks for five minutes (NDM
  `SRG-APP-000190-NDM-000267`). Set the *Inactivity Time* of every profile,
  including System Administrator, and the CLI `admin-idle-timeout` to 5.
- **Multifactor authentication.** The administrator MFA of 7.6.5 and later
  sends a one-time token by SMS or email; the guides document no DoD PKI
  (CAC) login for the Admin UI (NDM `SRG-APP-000149-NDM-000247`). Use Admin
  SAML SSO (7.6.3 and later) with an identity provider that enforces CAC,
  or the token MFA where SAML is not possible, and record the finding.
- **SNMP and NTP.** SNMPv3 offers MD5 or SHA1 authentication and DES,
  Triple-DES, or AES-128 privacy (NDM `SRG-APP-000395-NDM-000310`): use
  SNMPv3-AuthPriv with SHA1 and AES-128, or disable SNMP. Neither guide
  documents NTP authentication (NDM `SRG-APP-000395-NDM-000347`,
  ISE `CSCO-NC-000290`); use internal NTP servers reached over the
  management network.
- **Audit failures and storage.** The guides document no alert when a log
  receiver stops receiving events or audit processing fails, and no local
  queue of events while a receiver is unreachable (NDM
  `SRG-APP-000360-NDM-000295`, ISE `CSCO-NC-000200`, ISE `CSCO-NC-000210`,
  ISE `CSCO-NC-000230`, ISE `CSCO-NC-000240`). Set event thresholds for
  disk space, map them to alarms, configure two log receivers, and alert
  on missing events at the log server.
- **Audit gaps.** The admin auditing log does not record changes to NTP
  and time zone settings, certificates, Portal SSL settings, alarms, RADIUS
  server defaults, database backup settings, or the license key, and CLI
  changes appear only as *CLI Tool*; the guides do not say that CLI
  commands are recorded in full text (NDM `SRG-APP-000380-NDM-000304`, NDM
  `SRG-APP-000101-NDM-000231`). Live authentication logs are kept for only
  24 hours. Send events to the log receivers, restrict CLI access to a few
  administrators, and review those settings by procedure.
- **Posture checks.** FortiNAC scans check anti-virus products and
  operating systems directly, but the host firewall and host IDS/IPS are
  checked only through custom scans (process, service, or registry checks)
  that you write (ISE `CSCO-NC-000040`, ISE `CSCO-NC-000060`). Build and
  test a custom scan for each required product, or take the posture from
  FortiClient EMS or the MDM.
- **Certificate revocation for EAP-TLS.** The local RADIUS server checks
  revocation through OCSP; the guide documents no CRL or local revocation
  cache (AAA `SRG-APP-000875-AAA-000220`), and *OCSP Soft Fail* (7.6.5)
  passes a valid certificate whose status cannot be retrieved. Enable OCSP
  with a DoD-approved responder and leave Soft Fail disabled.
- **Firmware signatures.** Signed firmware enforcement and file integrity
  verification arrived in 7.6.3 (NDM `SRG-APP-000131-NDM-000243`). On
  older releases, download images only from Fortinet support and compare
  the checksum before every upgrade.
- **No STIG.** Without a STIG there is no DoD baseline to check against
  (NDM `SRG-APP-000516-NDM-000317`); use this map, the NAC pattern of the
  ISE STIG, and the vendor guidance as the baseline, and record the
  settings that differ from it.

## Design Considerations

- **Pick the release first, then the features.** FortiNAC-F 7.6 runs only
  on FortiNAC-OS, so any CentOS appliance must be migrated first. If your
  design depends on a feature introduced in a certain release (signed
  firmware and SAML SSO in 7.6.3, administrator MFA and the OCSP soft-fail
  flag in 7.6.5, live authentication logs and the audit of port
  enforcement changes in 7.6.7), that sets the minimum release, and it
  must be a vendor-supported release (NDM `SRG-APP-001035-NDM-000340`).
- **Keep the planes apart.** Put port1 (management, RADIUS, SNMP, agents)
  on the management network and port2 (DHCP, DNS, and the portal) on the
  isolation networks, and allow on each interface only the services the
  deployment uses (NDM `SRG-APP-000880-NDM-000290`).
- **Decide what every endpoint gets before you enforce.** Define the
  user/host profiles, the logical networks, and the VLANs or ACLs for
  registration, remediation, dead end, guests, MAB devices, and each
  production role, and keep unknown devices out of production networks
  (ISE `CSCO-NC-000020`, ISE `CSCO-NC-000260`).
- **Prefer 802.1X to MAB.** Use EAP-TLS or TEAP with DoD certificates
  where endpoints support it, MAB only for devices that cannot, and put
  MAB devices in restricted networks (ISE `CSCO-NC-000280`); the guide
  itself warns that MAB alone is easy to defeat by MAC spoofing.
- **Write the posture policy down.** The ISE pattern expects a posture
  policy for the clients that the System Security Plan says need one
  (ISE `CSCO-NC-000320`), enforced before trusted access, with remediation
  in a separate network. Record which profiles are scanned, what the scans
  require, and which endpoints or ports are exempt, with ISSM approval
  (ISE `CSCO-NC-000090`).
- **Plan for FortiNAC being down.** Enforcement and the RADIUS service
  stop when FortiNAC is unreachable. Use HA or N+1 failover groups, back
  up the database and system to a remote server over SSH or SFTP, and
  decide how switches behave when the RADIUS server does not answer.
- **Turn off what is not used.** The HTTP Admin UI, SNMP v1 and v2c,
  legacy RADIUS proxy, FTP backups, TLS 1.0 and 1.1, FortiAI Assist,
  integrations and service connectors that nobody uses, and the Squid
  proxy all need a reason to stay on.

## Implementation and Automation

### The FortiNAC feature map

The SRG column uses the abbreviations defined in *Where the SRG data
comes from*; remember that **ISE** entries are the Cisco ISE NAC STIG
rules used as a pattern. The requirement titles are listed in the next
table. The command column follows the conventions in *Where the commands
come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/25-fortinac-feature-version-and-srg-map-feature-map.csv) (172 rows).

| Category | Feature | Introduced (FortiNAC-F) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Management access | Admin UI over HTTPS (TCP 8443) and HTTP (TCP 8080) on the management interface | 7.2.0 | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000172-NDM-000259`; NDM `SRG-APP-000142-NDM-000245` | `config system interface`; `edit port1`; `unselect allowaccess http-adminui`; `next`; `end` |
| Core: Management access | Interface access services (set allowaccess: SSH, Admin UI, SNMP, syslog, RADIUS, agent, DHCP, DNS, and others) | 7.2.0 | NDM `SRG-APP-000142-NDM-000245`; AAA `SRG-APP-000142-AAA-000680` | `config system interface`; `edit <PORT>`; `set allowaccess <ACCESS_LIST>`; `next`; `end` (only the services the deployment uses; SSH and the Admin UI only on port1) |
| Core: Management access | Management (port1) and portal/isolation (port2) interfaces | 7.2.0 | NDM `SRG-APP-000880-NDM-000290` | `config system global`; `set management port1`; `set portal port2`; `end` |
| Core: Management access | CLI over SSH and the console | 7.2.0 | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000880-NDM-000290`; NDM `SRG-APP-000340-NDM-000288` | `config system interface`; `edit port2`; `unselect allowaccess ssh`; `next`; `end` (SSH only on port1) |
| Core: Cryptography | Strong encryption mode for running services | 7.2.0 | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000179-NDM-000265`; NDM `SRG-APP-000411-NDM-000330` | `config system global`; `set strong-crypto enable`; `end` |
| Core: Cryptography | TLS service configurations (Admin UI, Persistent Agent, and RADIUS EAP certificates, protocols, and ciphers) | 7.2.0 | NDM `SRG-APP-000412-NDM-000331`; ISE `CSCO-NC-000010`; AAA `SRG-APP-000172-AAA-000520` | GUI: System > Settings > Persistent Agent > Transport configurations (TLS service settings: TLS Protocol TLSv1.2 and TLSv1.3 only) |
| Core: Admin accounts | Administrators and administrator profiles (permissions, landing page, login availability) | 7.2.0 | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000231-NDM-000271` | GUI: Users & Hosts > Administrators (Profiles tab: least-privilege profiles; System Administrator profile only for a few accounts) |
| Core: Admin accounts | Administrator profile inactivity time | 7.2.0 | NDM `SRG-APP-000190-NDM-000267` | GUI: Users & Hosts > Administrators (Profiles tab, Inactivity Time: 5 minutes or less, also on the System Administrator profile) |
| Core: Admin accounts | CLI administrator idle timeout | 7.2.0 | NDM `SRG-APP-000190-NDM-000267` | `config system global`; `set admin-idle-timeout <MINUTES>`; `end` (5 or less) |
| Core: Admin accounts | Administrator profile lockout (Lock Out After Attempts, Lock Out Duration) | 7.2.0 | NDM `SRG-APP-000065-NDM-000214` | GUI: Users & Hosts > Administrators (Profiles tab: Lock Out After Attempts 3; Lock Out Duration 900 seconds or longer) |
| Core: Admin accounts | CLI administrator lockout threshold and duration | 7.6 (release not stated) | NDM `SRG-APP-000065-NDM-000214` | `config system global`; `set admin-lockout-threshold 3`; `set admin-lockout-duration 900`; `end` |
| Core: Admin accounts | CLI admin account and password (account of last resort) | 7.2.0 | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000164-NDM-000252` | `config system admin`; `edit admin`; `set password <PASSWORD>`; `end` |
| Core: Admin accounts | Administrator expiration and aging (User Expires, User Never Expires, User Inactivity Limit) | 7.2.0 | NDM `SRG-APP-000028-NDM-000210`; NDM `SRG-APP-000029-NDM-000211` | GUI: Users & Hosts > Administrators (Set Expiration for temporary administrators) |
| Core: Remote authentication | Administrator authentication by LDAP or RADIUS (Auth Type) and administrator profile mappings | 7.2.0 | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249`; AAA `SRG-APP-000148-AAA-000390` | GUI: Users & Hosts > Administrators (Auth Type: LDAP or RADIUS; Administrator profile mappings from directory groups) |
| Core: Remote authentication | LDAP directories (SSL or STARTTLS security protocol, synchronization of users and groups) | 7.2.0 | AAA `SRG-APP-000142-AAA-000010`; NDM `SRG-APP-000516-NDM-000336` | GUI: System > Settings > Authentication > Directories (Security Protocol: SSL or STARTTLS) |
| Core: Passwords | Local administrator passwords (character rules; no length or complexity policy) | 7.2.0 | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000170-NDM-000329`; NDM `SRG-APP-000845-NDM-000220` | GUI: Users & Hosts > Administrators (Change Password: 15 or more characters by procedure; see the limitations) |
| Core: Logging | Admin auditing log (who changed what and when; CLI changes as CLI Tool) | 7.2.0 | NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000027-NDM-000209`; NDM `SRG-APP-000100-NDM-000230`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000343-NDM-000289` | GUI: Logs > Audit Logs (grant Admin Auditing only to auditors) |
| Core: Logging | Events and event management (enable events, thresholds, internal and external logging) | 7.2.0 | NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000095-NDM-000225`; ISE `CSCO-NC-000150`; ISE `CSCO-NC-000160`; AAA `SRG-APP-000089-AAA-000380` | GUI: Logs > Events > Event management (enable the authentication, login failure, and Security Risk Host events; Options: Internal & External) |
| Core: Logging | Log receivers (Syslog CSV, Syslog CEF, SNMP trap, FortiAnalyzer OFTP) | 7.2.0 | NDM `SRG-APP-000516-NDM-000350`; NDM `SRG-APP-000515-NDM-000325`; ISE `CSCO-NC-000220`; AAA `SRG-APP-000358-AAA-000280` | GUI: System > Settings > System communication > Log receivers (at least two receivers) |
| Core: Logging | Alarm mappings with email and SMS notification | 7.2.0 | ISE `CSCO-NC-000100`; ISE `CSCO-NC-000170`; NDM `SRG-APP-000360-NDM-000295` | GUI: Logs > Alarms (map security and failure events to alarms that notify the SA and ISSO) |
| Core: Time | NTP and time zone (UTC in the database) | 7.2.0 | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000374-NDM-000299`; NDM `SRG-APP-000395-NDM-000347`; ISE `CSCO-NC-000290` | `config system ntp`; `set ntpserver <NTP_SERVER_1> <NTP_SERVER_2>`; `set ntpsync enable`; `end` |
| Core: SNMP | SNMP agent (SNMPv1/v2c, SNMPv3 AuthPriv and AuthNoPriv) | 7.2.0 | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000142-NDM-000245` | GUI: System > Settings > System communication > SNMP (SNMPv3-AuthPriv with SHA1 and AES-128, or Disable) |
| Core: Certificates | Certificate management (server certificates for Admin UI, portal, agent, and RADIUS; trusted certificates) | 7.2.0 | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000910-NDM-000300`; AAA `SRG-APP-000175-AAA-000570`; AAA `SRG-APP-000910-AAA-000230` | GUI: System > Certificate management (DoD-issued server certificates; only DoD CAs in Trusted Certificates) |
| Core: Backups | Database and system backups (scheduled tasks), remote backup over SSH or FTP, and configuration backup from the CLI | 7.2.0 | NDM `SRG-APP-000516-NDM-000340` | GUI: System > Settings > System management > Remote backup configuration (Enable SSH Remote Backup); `execute backup config scp <FILE> <SERVER> <USER> <PASSWORD>` |
| Core: Firmware | Firmware upgrades (Updates > System, or execute restore image) | 7.2.0 | NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-000378-NDM-000302` | GUI: System > Settings > Updates > System |
| Core: High availability | High availability (primary and secondary servers, shared IP) | 7.2.0 | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: Discovery | Network device inventory and discovery (switches, wireless controllers, firewalls, VPN devices) | 7.2.0 | ISE `CSCO-NC-000250` | GUI: Network > Inventory |
| Core: Discovery | L2 and L3 polling, MAC notification traps, and host location | 7.2.0 | ISE `CSCO-NC-000250` | GUI: Network > L2 polling; GUI: Network > L3 polling |
| Core: Discovery | Rogue host detection and isolation of unknown devices (registration, isolation, and dead-end VLANs) | 7.2.0 | ISE `CSCO-NC-000260`; ISE `CSCO-NC-000130`; AAA `SRG-APP-000516-AAA-000660` | GUI: Network > Logical networks (registration and isolation logical networks with access limited to the portal and remediation resources) |
| Core: Profiling | Device profiling rules and device types | 7.2.0 | ISE `CSCO-NC-000030` | GUI: Users & Hosts > Device profiling rules |
| Core: Profiling | Endpoint fingerprints (DHCP and other fingerprint sources) | 7.2.0 | ISE `CSCO-NC-000030`; ISE `CSCO-NC-000250` | GUI: Users & Hosts > Endpoint Fingerprints |
| Core: Policy | User/host profiles and network access policies (logical networks mapped to VLANs, ACLs, and filter IDs) | 7.2.0 | ISE `CSCO-NC-000020`; ISE `CSCO-NC-000130`; ISE `CSCO-NC-000140` | GUI: Policy & Objects > Network access; GUI: Network > Logical networks |
| Core: Policy | Authentication policies (portal and agent authentication) | 7.2.0 | ISE `CSCO-NC-000270`; ISE `CSCO-NC-000260` | GUI: Policy & Objects > Authentication |
| Core: Endpoint compliance | Endpoint compliance policies and scans (anti-virus, operating system, custom scans, monitors) | 7.2.0 | ISE `CSCO-NC-000310`; ISE `CSCO-NC-000320`; ISE `CSCO-NC-000050`; ISE `CSCO-NC-000040`; ISE `CSCO-NC-000060` | GUI: Policy & Objects > Endpoint compliance (Policies and Scans for every posture-required profile; custom process or service scans for the host firewall and host IDS/IPS) |
| Core: Endpoint compliance | Agents (Persistent, Dissolvable, Passive, and Mobile) | 7.2.0 | ISE `CSCO-NC-000310`; ISE `CSCO-NC-000010` | GUI: System > Settings > Persistent Agent (Transport configurations with TLS) |
| Core: Endpoint compliance | Auto-definition updates for anti-virus and operating system scans | 7.2.0 | ISE `CSCO-NC-000050` | GUI: Policy & Objects > Endpoint compliance > Auto-definition updates |
| Core: Remediation | Remediation on scan failure (remediation VLAN, failure page with instructions) | 7.2.0 | ISE `CSCO-NC-000070`; ISE `CSCO-NC-000110`; ISE `CSCO-NC-000140` | GUI: Policy & Objects > Endpoint compliance > Scans (Remediation - On Failure; Instructions For Scan Failure) |
| Core: Remediation | Quarantine VLAN switching | 7.2.0 | ISE `CSCO-NC-000070` | GUI: System > Settings > Control > Quarantine |
| Core: Security response | Security incidents (events from security devices, rules, triggers, and actions such as disabling a host) | 7.2.0 | ISE `CSCO-NC-000120`; ISE `CSCO-NC-000100` | GUI: Logs > Security Incidents |
| Core: Enforcement | Port groups for enforcement (Forced Registration, Forced Remediation, Role-Based Access, and other system groups) | 7.2.0 | ISE `CSCO-NC-000090`; ISE `CSCO-NC-000260` | GUI: System > Groups (every access port in an enforcement group; document ports left out) |
| Core: Enforcement | MAC address exclusion | 7.2.0 | ISE `CSCO-NC-000090` | GUI: System > Settings > User/Host Management > MAC address exclusion (only ISSM-approved devices, recorded in the SSP) |
| Core: RADIUS | Local RADIUS server (802.1X EAP termination; EAP types TLS, TTLS, PEAP, MD5, GTC, MSCHAPv2, FAST, TEAP) | 7.2.0 | AAA `SRG-APP-000516-AAA-000440`; AAA `SRG-APP-000394-AAA-000430`; AAA `SRG-APP-000158-AAA-000420`; ISE `CSCO-NC-000270`; ISE `CSCO-NC-000300` | GUI: Network > RADIUS > Configure Local Server (Supported EAP Types: TLS, TTLS, PEAP, and TEAP only) |
| Core: RADIUS | RADIUS secrets and RADIUS mode per modeled device | 7.2.0 | AAA `SRG-APP-000516-AAA-000640` | GUI: Network > Inventory > Device configuration > Model configuration (a unique RADIUS Secret for each device) |
| Core: RADIUS | MAC Authentication Bypass (MAB) | 7.2.0 | ISE `CSCO-NC-000280` | GUI: Policy & Objects > Network access (MAB devices only in restricted logical networks) |
| Core: RADIUS | OCSP certificate revocation checking for EAP-TLS | 7.2.0 | AAA `SRG-APP-000175-AAA-000580`; AAA `SRG-APP-000875-AAA-000220` | GUI: Network > RADIUS > Configure Local Server (OCSP Enabled) |
| Core: RADIUS | Require Message-Authenticator (BlastRADIUS protection) | 7.2 (release not stated) | AAA `SRG-APP-000516-AAA-000640` | GUI: Network > RADIUS > Configuration (Require Message-Authenticator: Enabled, or Auto while legacy NAS clients remain) |
| Core: Guests | Guest and contractor accounts, templates, and sponsors | 7.2.0 | AAA `SRG-APP-000024-AAA-000040`; AAA `SRG-APP-000024-AAA-000050`; AAA `SRG-APP-000516-AAA-000660` | GUI: Users & Hosts > Guests & Contractors > Guest & Contractor templates (Account Duration 72 hours or less) |
| Core: Captive portal | Captive portal and portal SSL certificate | 7.2.0 | AAA `SRG-APP-000142-AAA-000020`; ISE `CSCO-NC-000010` | GUI: Portal > Portal SSL |
| Core: Users | Aging of host and user records | 7.2.0 | AAA `SRG-APP-000025-AAA-000080` | GUI: System > Settings > User/Host Management > Aging (35 days of inactivity or less) |
| Core: Integrations | MDM service connectors | 7.2.0 | ISE `CSCO-NC-000020`; ISE `CSCO-NC-000310` | GUI: Network > Service Connectors > MDM Servers |
| Core: Integrations | FortiGate Security Fabric connection and FSSO | 7.2.0 | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `config system interface`; `edit port1`; `unselect allowaccess fsso`; `next`; `end` |
| Core: Isolation services | DHCP and DNS services for isolation networks | 7.2.0 | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `config system interface`; `edit port2`; `unselect allowaccess dhcp dns`; `next`; `end` |
| Core: Visibility | Dashboard, reports, and network sessions | 7.2.0 | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiNAC software re-versioning to F 7.2 (Fortinet Fabric versioning) | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | FortiNAC-F VM SKUs and FortiNAC-OS (FortiOS-like CLI, firmware image) replacing CentOS 7 | 7.2.0 and later | NDM `SRG-APP-001035-NDM-000340` | `get system status` (FortiNAC-OS on FNC-CAX, FNC-MX, or F-series appliances) |
| Authentication | SAML/Shibboleth not available on FortiNAC-OS (until the SAML SSO of 7.6.3) | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Hardware and cloud | AWS secure deployment (SSH keys set up during image deployment) | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Hardware and cloud | Cloud-init bootstrap of the initial VM configuration (AWS, KVM, ESX, Hyper-V) | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Agents | macOS agents natively compatible with the M1 processor | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Visibility | Report of enforced and non-enforced ports and APs/SSIDs (Network Device Summary and Network Inventory) | 7.2.0 and later | ISE `CSCO-NC-000250`; ISE `CSCO-NC-000090` | GUI: Network > Inventory (review non-enforced ports against the SSP) |
| Device integration | Cambium cnPilot APs, Dell EMC N3248P-ON MAC-notification traps, Extreme Campus Controller E3120 | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | FortiGate VDOM modeling enhancements | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | New UI for the policy and logical network views (common search, filtering, drag-and-drop) | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| RADIUS | RADIUS over TLS (RadSec) for the Local RADIUS Server | 7.2.1 and later | AAA `SRG-APP-000142-AAA-000020`; AAA `SRG-APP-000172-AAA-000520`; AAA `SRG-APP-000516-AAA-000640` | GUI: Network > RADIUS > Configuration (RADIUS over TLS (RadSec); Discard Unencrypted Requests and Client Certificate Required where the devices support RadSec); `config system interface`; `edit port1`; `append allowaccess radius-radsec`; `next`; `end` |
| Platform | Enhanced communication method between FortiNAC servers (Manager and CA; configuration required before upgrade) | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Hardware and cloud | F-series hardware (FortiNAC-CA-500F, CA-600F, CA-700F, M-550F) | 7.2.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management access | HSTS enabled by default for the Admin GUI | 7.2.4+; 7.4.0+ | NDM `SRG-APP-000412-NDM-000331` | — |
| Device integration | Meraki MX as RADIUS concentrator/wireless controller | 7.2.6+; 7.4.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| MDM and OT | MS Intune integration enhancements (on-demand API query for a host, certificate-based authentication) | 7.2.6+; 7.4.1+ | ISE `CSCO-NC-000020`; ISE `CSCO-NC-000310` | GUI: Network > Service Connectors > MDM Servers |
| Agents | New agent versions (Windows 9.4.4, macOS/Linux 10.7.2) | 7.2.6 and later | ISE `CSCO-NC-000310` | GUI: System > Settings > Updates > Agent packages |
| Platform | Migration of legacy CentOS C-series appliances to FortiNAC-OS | 7.2.7+; 7.4.0+; 7.6.1+ | NDM `SRG-APP-001035-NDM-000340` | — |
| MDM and OT | Host role from MDM device ownership (Intune, AirWatch, MaaS360, MobileIron, Citrix) | 7.2.9+; 7.4.2+; 7.6.3+ | ISE `CSCO-NC-000020` | GUI: Network > Service Connectors > MDM Servers |
| RADIUS | RADIUS CoA and Disconnect messages with custom attribute profiles assigned to logical networks | 7.4.0 and later | ISE `CSCO-NC-000140`; ISE `CSCO-NC-000280`; ISE `CSCO-NC-000120` | GUI: Network > Logical networks (assign a CoA profile so that access changes take effect at once) |
| RADIUS | EduRoam and the RADIUS service proxy (Proxy virtual servers; legacy proxy deprecated) | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Network > RADIUS > Virtual Servers (delete unused Proxy servers; leave Legacy Proxy Configuration disabled) |
| Backups | Secure FTP remote backup | 7.4.0 and later | NDM `SRG-APP-000516-NDM-000340` | GUI: System > Settings > System management > Remote backup configuration (Enable Secure FTP Remote Backup; disable FTP Remote Backup) |
| Agents | Persistent Agent status notification with the logical network name, and user acknowledgment of VLAN changes | 7.4.0 and later | ISE `CSCO-NC-000080` | GUI: System > Settings > Persistent Agent > Properties |
| Endpoint compliance | Palo Alto XDR and Trend Micro Apex One (Japanese version) detected as anti-virus products | 7.4.0 and later | ISE `CSCO-NC-000050` | GUI: Policy & Objects > Endpoint compliance > Scans |
| Device integration | FortiLAN Cloud FortiAP and FortiSwitch support | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| MDM and OT | Claroty integration | 7.4.0 and later | ISE `CSCO-NC-000250` | GUI: Network > Service Connectors > OT |
| Device integration | Arista Cloud Wireless integration | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Endpoint compliance | Custom Windows registry scan with date comparison | 7.4.0 and later | ISE `CSCO-NC-000320` | GUI: Policy & Objects > Endpoint compliance > Scans |
| Device integration | Mist wireless integration through the Mist Service Connector (Device Management API) | 7.4.1+; 7.6.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | Huawei iMaster Cloud service connector | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | Ruckus R1 Cloud integration | 7.4.1+; 7.6.3+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Endpoint compliance | FortiClient EMS Cloud integration (in addition to on-premises EMS) | 7.4.2+; 7.6.3+ | ISE `CSCO-NC-000310`; ISE `CSCO-NC-000020` | GUI: Network > Service Connectors |
| Profiling | Device Detection database with FortiGuard (over 140 device types) | 7.4.2+; 7.6.3+ | ISE `CSCO-NC-000030` | GUI: System > Settings > Identification > Device types |
| MDM and OT | MS Intune with randomized MACs (Intune Device ID from the user certificate in the RADIUS request) | 7.4.2 and later | ISE `CSCO-NC-000020`; ISE `CSCO-NC-000270` | GUI: Network > Service Connectors > MDM Servers |
| Visibility | Wireless access point security (syslog link-change events against rogue devices posing as APs) | 7.4.2 and later | ISE `CSCO-NC-000250`; ISE `CSCO-NC-000260` | `config system interface`; `edit port1`; `append allowaccess syslog`; `next`; `end` |
| Device integration | Meraki integration polling the Meraki API for devices | 7.4.2+; 7.6.3+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | Ruijie Wireless Controller integration | 7.4.2+; 7.6.3+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | Sophos Wireless integration | 7.4.2+; 7.6.3+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | Juniper Mist Cloud Wireless API integration | 7.4.2+; 7.6.3+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | Yamaha router NVR510 and switch SWX2310 support | 7.4.2+; 7.6.3+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | CentOS appliances no longer supported (7.6 runs only on FortiNAC-OS) | 7.6.0 and later | NDM `SRG-APP-001035-NDM-000340` | `get system status` |
| Platform | Access Point Management removed | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Endpoint compliance | Check Point VPN integration (posture of VPN users and machines) | 7.6.0 and later | ISE `CSCO-NC-000310`; ISE `CSCO-NC-000140` | GUI: Policy & Objects > Network access (VPN logical networks for compliant and non-compliant hosts) |
| Authentication | Machine authentication with RBAC based on Active Directory computer groups | 7.6.0 and later | ISE `CSCO-NC-000270`; AAA `SRG-APP-000394-AAA-000430` | GUI: Policy & Objects > User/host profiles |
| Authentication | Maximum concurrent sessions per user (global and per user) | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| RADIUS | TEAP for RADIUS clients and TLS 1.3 in the Local RADIUS Server | 7.6.0 and later | AAA `SRG-APP-000516-AAA-000440`; AAA `SRG-APP-000172-AAA-000520`; ISE `CSCO-NC-000300` | GUI: Network > RADIUS > Configure Local Server (TLS Configuration: TLS 1.3 and TLS 1.2 only) |
| Device integration | Palo Alto Networks SSO tags for non-VPN environments | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | Cluster custom health check (ICMP, TCP, TCP Echo) | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | FortiNAC Manager Cluster Management (replaces Manager HA) | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | CA management from FortiNAC Manager | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | N+1 failover groups for CAs | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | KEA DHCP as the internal DHCP server for isolated hosts | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `config system interface`; `edit port2`; `unselect allowaccess dhcp`; `next`; `end` |
| GUI | GUI enhancements (OT connector categories, Actions views, portal configuration UI, secondary server UI, SSL certificate installation, Config Wizard) | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy | Temporary port enforcement exception | 7.6.1 and later | ISE `CSCO-NC-000090` | GUI: Network > Inventory > Ports view (Set Temporary Port Exception only with ISSM approval) |
| Management | Centralized management of host and user records from FortiNAC Manager | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy | Endpoint compliance attribute filters in user/host profiles (Compliance Status, Last Compliance Scan) | 7.6.2 and later | ISE `CSCO-NC-000140`; ISE `CSCO-NC-000020` | GUI: Policy & Objects > User/host profiles |
| Management | Squid HTTP proxy on FortiNAC Manager for CA downloads | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `config system interface`; `edit port1`; `unselect allowaccess http-proxy`; `next`; `end` |
| Management access | Out-of-band management in high availability configurations (ports 3 to 6) | 7.6.2 and later | NDM `SRG-APP-000880-NDM-000290` | — |
| Authentication | Microsoft Entra ID as a native authentication source (802.1X and portal) | 7.6.3 and later | ISE `CSCO-NC-000270`; AAA `SRG-APP-000148-AAA-000390` | GUI: Network > RADIUS > Configure Local Server (Authentication Source) |
| Authentication | SAML SSO for administrators and users, and FortiCloud SSO for admin login | 7.6.3 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000820-NDM-000170` | GUI: Network > Service Connectors > Admin SAML SSO (identity provider that enforces DoD PKI; disable Admin FortiCloud SSO) |
| MDM and OT | Armis service connector | 7.6.3 and later | ISE `CSCO-NC-000250` | GUI: Network > Service Connectors |
| Firmware | Secure boot, file integrity verification, and signed firmware enforcement | 7.6.3 and later | NDM `SRG-APP-000131-NDM-000243`; NDM `SRG-APP-000378-NDM-000302` | `get system status` (allow downgrades to unsigned builds only with ISSM approval) |
| Platform | Link aggregation groups on FortiNAC appliances | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | Automated certificate sync from the primary server in HA | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | Faster failover in active-standby HA | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | Independent IP for CA N+1 setups | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | Shared IP for FortiNAC Manager clusters | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | N+1 health check refinement | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| High availability | Split-brain prevention for HA pairs managed by FortiNAC Manager | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Firmware | Firmware upgrade from the FortiGuard Distribution Network | 7.6.3 and later | NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000457-NDM-000352` | GUI: System > Settings > Updates > System |
| RADIUS | TEAP with multiple inner authentication methods (user and machine) | 7.6.3 and later | AAA `SRG-APP-000516-AAA-000440`; ISE `CSCO-NC-000270` | GUI: Network > RADIUS > Configure Local Server (TEAP/FAST PAC Settings; Allow Anonymous In-Band PAC Provisioning disabled) |
| MDM and OT | Vulnerability scanner service connector (Tenable, Qualys) | 7.6.3 and later | ISE `CSCO-NC-000020` | GUI: Network > Service Connectors > Vulnerability Scanners |
| Management access | CLI console in the FortiNAC GUI | 7.6.3 and later | NDM `SRG-APP-000340-NDM-000288` | — |
| Hardware and cloud | OCI and GCP images | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | Alcatel OAW-AP1221, Future Matrix switches, Alaxala AX3660S, FortiPAM and FortiSRA mappings | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Authentication | Remote group mapping for Entra ID in user/host profiles | 7.6.5 and later | ISE `CSCO-NC-000020` | GUI: Policy & Objects > User/host profiles |
| Admin accounts | Multi-factor authentication for administrators (token by SMS or email; individual and global) | 7.6.5 and later | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000149-NDM-000247` | GUI: System > Settings > Authentication > Multi-factor Authentication (Global MFA) |
| High availability | Backup IP for N+1 failover groups | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Guests | Self-registration guest login option in the authentication portal | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Portal > Portal configuration |
| Authentication | External Ethernet adapter (docking station and dongle) management | 7.6.5 and later | ISE `CSCO-NC-000270` | GUI: System > Settings > Identification > Docking Station Management |
| Policy | Allowed hosts per user group and standalone Host Inventory page | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | API token for FortiGate REST calls and SSH public key authentication to network devices | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | SSID description column | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Portal | captive.apple.com allowed DNS exception for macOS captive portal | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| RADIUS | OCSP soft-fail flag for certificate-based RADIUS authentication | 7.6.5 and later | AAA `SRG-APP-000175-AAA-000580` | GUI: Network > RADIUS > Configure Local Server (OCSP Soft Fail disabled) |
| Device integration | VDOM multi-tenancy for FortiGate-managed FortiSwitch and FortiAP | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Certificates | Import of PKCS#12 certificates in the GUI | 7.6.5 and later | NDM `SRG-APP-000516-NDM-000344` | GUI: System > Certificate management |
| Hardware and cloud | Deployment in Alibaba Cloud | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | LDAP group and OU search bar | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Portal | Captive portal over NATted infrastructure with FortiGate | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | Demo license expiration date and grace period | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Certificates | ECC certificates | 7.6.5 and later | NDM `SRG-APP-000516-NDM-000344` | GUI: System > Certificate management |
| Platform | FortiFlex VM licensing | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| RADIUS | Client certificate attribute ranking for user authentication (CN, DNS, UPN) | 7.6.5 and later | AAA `SRG-APP-000177-AAA-000600` | GUI: Network > RADIUS > Configure Local Server (Client Certificate Attribute) |
| High availability | FortiADC as health monitor and virtual IP manager for N+1 groups | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Agents | VLAN switch acknowledgment changes (only when leaving remediation; canceled switches stop; new event) | 7.6.5 and later | ISE `CSCO-NC-000080` | GUI: System > Settings > Persistent Agent > Properties |
| MDM and OT | ServiceNow CMDB integration as MDM | 7.6.5 and later | ISE `CSCO-NC-000250` | GUI: Network > Service Connectors > MDM Servers |
| Logging | ServiceNow ITSM incidents from FortiNAC alarms | 7.6.5 and later | ISE `CSCO-NC-000100` | GUI: Network > Service Connectors > ServiceNow ITSM Integration |
| Device integration | RADIUS-only devices (selector-based configuration without SNMP) | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device integration | Remote groups sent to FortiGate and Palo Alto Networks firewalls | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | IPv6 for the portal, agents, Admin UI, RADIUS, and 802.1X | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Visibility | IP-MAC mapping from DHCP and RADIUS Framed-IP-Address caching | 7.6.7 and later | ISE `CSCO-NC-000250` | GUI: Users & Hosts > Endpoint Fingerprints |
| Device integration | Meraki Service Connector with API polling (SNMP optional) | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management | FortiAI Assist chat assistant | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | GUI: Settings > AI Assist (Enable FortiAI Assist off) |
| Logging | Live authentication logs (LDAP, Local, RADIUS, SAML, Social) | 7.6.7 and later | ISE `CSCO-NC-000150`; AAA `SRG-APP-000089-AAA-000380` | GUI: Logs > Authentication Logs |
| High availability | CA clustering failover health check (true hot standby) | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| GUI | MDM and service connector column on the Host page and in user/host profiles | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Hardware and cloud | OCI DRCC Oman images | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Authentication | Logged-on user handling across user and machine authentication | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Platform | Automatic shutdown of unused captive portal services (dhcpd, named, apache2) | 7.6.7 and later | NDM `SRG-APP-000142-NDM-000245` | — |
| Platform | Perpetual license expiration display | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Logging | Admin audit and event logging of port enforcement changes, data exports, and syslog forwarding | 7.6.7 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000343-NDM-000289` | GUI: Logs > Audit Logs |
| Logging | Additional endpoint and network data and the Hostname field sent to FortiAnalyzer | 7.6.7 and later | NDM `SRG-APP-000516-NDM-000350`; NDM `SRG-APP-000515-NDM-000325` | GUI: System > Settings > System communication > Log receivers |
| High availability | FortiNAC Manager shared IP in public cloud | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Profiling | Regex vendor codes for randomized MAC addresses | 7.6.7 and later | ISE `CSCO-NC-000030` | GUI: System > Settings > Identification > Vendor OUIs |
| Management access | Interface enable/disable and speed/duplex from the CLI | 7.6.7 and later | NDM `SRG-APP-000142-NDM-000245` | `config system interface`; `edit <PORT>`; `set status down`; `next`; `end` (unused ports) |
| RADIUS | Configurable RadSec idle timeout | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Guests | Re-registration period for guest and contractor hosts | 7.6.7 and later | AAA `SRG-APP-000024-AAA-000050` | GUI: Users & Hosts > Guests & Contractors > Guest & Contractor templates (re-registration period: 72 hours or less) |
| Device integration | H3C WX3820X, D-Link DIS-300G-14PSW, Aruba 2930F, Barox switch, Cisco 8300, Transition/Lantronix switches, Altai APs | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current releases. The SRG ID column gives the SRG
requirement each rule implements (for NDM and AAA rows it is the first
part of the requirement ID). ISE rows are the Cisco ISE NAC STIG rules
used as the expected pattern; their titles are shortened by dropping the
closing "required for compliance with C2C Step" phrase:

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/25-fortinac-feature-version-and-srg-map-requirements.csv) (97 rows).

| SRG | Requirement | Severity | SRG ID | Requirement title |
| --- | --- | --- | --- | --- |
| NDM | `SRG-APP-000026-NDM-000208` | CAT II | `SRG-APP-000026` | The network device must automatically audit account creation. |
| NDM | `SRG-APP-000027-NDM-000209` | CAT II | `SRG-APP-000027` | The network device must automatically audit account modification. |
| NDM | `SRG-APP-000028-NDM-000210` | CAT II | `SRG-APP-000028` | The network device must automatically audit account disabling actions. |
| NDM | `SRG-APP-000029-NDM-000211` | CAT II | `SRG-APP-000029` | The network device must automatically audit account removal actions. |
| NDM | `SRG-APP-000033-NDM-000212` | CAT I | `SRG-APP-000033` | The network device must be configured to assign appropriate user roles or access levels to authenticated users. |
| NDM | `SRG-APP-000065-NDM-000214` | CAT II | `SRG-APP-000065` | The network device must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must block any login attempt for 15 minutes. |
| NDM | `SRG-APP-000068-NDM-000215` | CAT II | `SRG-APP-000068` | The network device must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the device. |
| NDM | `SRG-APP-000069-NDM-000216` | CAT II | `SRG-APP-000069` | The network device must retain the Standard Mandatory DoD Notice and Consent Banner on the screen until the administrator acknowledges the usage conditions and takes explicit actions to log on for further access. |
| NDM | `SRG-APP-000095-NDM-000225` | CAT II | `SRG-APP-000095` | The network device must produce audit log records containing sufficient information to establish what type of event occurred. |
| NDM | `SRG-APP-000100-NDM-000230` | CAT II | `SRG-APP-000100` | The network device must generate audit records containing information that establishes the identity of any individual or process associated with the event. |
| NDM | `SRG-APP-000101-NDM-000231` | CAT II | `SRG-APP-000101` | The network device must generate audit records containing the full-text recording of privileged commands. |
| NDM | `SRG-APP-000131-NDM-000243` | CAT II | `SRG-APP-000131` | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| NDM | `SRG-APP-000142-NDM-000245` | CAT I | `SRG-APP-000142` | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services |
| NDM | `SRG-APP-000148-NDM-000346` | CAT II | `SRG-APP-000148` | The network device must be configured with only one local account to be used as the account of last resort in the event the authentication server is unavailable. |
| NDM | `SRG-APP-000149-NDM-000247` | CAT I | `SRG-APP-000149` | The network device must be configured to use DoD PKI as multi-factor authentication (MFA) for interactive logins. |
| NDM | `SRG-APP-000153-NDM-000249` | CAT II | `SRG-APP-000153` | The network device must be configured to authenticate each administrator prior to authorizing privileges based on assignment of group or role. |
| NDM | `SRG-APP-000164-NDM-000252` | CAT II | `SRG-APP-000164` | The network device must enforce a minimum 15-character password length. |
| NDM | `SRG-APP-000170-NDM-000329` | CAT II | `SRG-APP-000170` | The network device must require that when a password is changed, the characters are changed in at least eight of the positions within the password. |
| NDM | `SRG-APP-000171-NDM-000258` | CAT I | `SRG-APP-000171` | The network device must be configured to store passwords using an approved salted key derivation function, preferably using a keyed hash for password-based authentication. |
| NDM | `SRG-APP-000172-NDM-000259` | CAT I | `SRG-APP-000172` | The network device must transmit only encrypted representations of passwords. |
| NDM | `SRG-APP-000179-NDM-000265` | CAT I | `SRG-APP-000179` | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| NDM | `SRG-APP-000190-NDM-000267` | CAT I | `SRG-APP-000190` | The network device must terminate all network connections associated with a device management session at the end of the session, or the session must be terminated after five minutes of inactivity except to fulfill documented and validated mission requirements. |
| NDM | `SRG-APP-000231-NDM-000271` | CAT I | `SRG-APP-000231` | The network device must only allow authorized administrators to view or change the device configuration, system files, and other files stored either in the device or on removable media (such as a flash drive). |
| NDM | `SRG-APP-000340-NDM-000288` | CAT I | `SRG-APP-000340` | The network device must prevent non-privileged users from executing privileged functions to include disabling, circumventing, or altering implemented security safeguards/countermeasures. |
| NDM | `SRG-APP-000343-NDM-000289` | CAT II | `SRG-APP-000343` | The network device must audit the execution of privileged functions. |
| NDM | `SRG-APP-000360-NDM-000295` | CAT II | `SRG-APP-000360` | The network device must generate an immediate real-time alert of all audit failure events requiring real-time alerts. |
| NDM | `SRG-APP-000374-NDM-000299` | CAT II | `SRG-APP-000374` | The network device must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). |
| NDM | `SRG-APP-000378-NDM-000302` | CAT II | `SRG-APP-000378` | The network device must prohibit installation of software without explicit privileged status. |
| NDM | `SRG-APP-000380-NDM-000304` | CAT II | `SRG-APP-000380` | The network device must enforce access restrictions associated with changes to device configuration. |
| NDM | `SRG-APP-000395-NDM-000310` | CAT II | `SRG-APP-000395` | The network device must be configured to authenticate SNMP messages using a FIPS-validated Keyed-Hash Message Authentication Code (HMAC). |
| NDM | `SRG-APP-000395-NDM-000347` | CAT II | `SRG-APP-000395` | The network device must authenticate Network Time Protocol sources using authentication that is cryptographically based. |
| NDM | `SRG-APP-000411-NDM-000330` | CAT I | `SRG-APP-000411` | The network devices must use FIPS-validated Keyed-Hash Message Authentication Code (HMAC) to protect the integrity of nonlocal maintenance and diagnostic communications. |
| NDM | `SRG-APP-000412-NDM-000331` | CAT I | `SRG-APP-000412` | The network device must be configured to implement cryptographic mechanisms using a FIPS 140-2 approved algorithm to protect the confidentiality of remote maintenance sessions |
| NDM | `SRG-APP-000457-NDM-000352` | CAT II | `SRG-APP-000457` | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| NDM | `SRG-APP-000503-NDM-000320` | CAT II | `SRG-APP-000503` | The network device must generate audit records when successful/unsuccessful logon attempts occur. |
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | `SRG-APP-000515` | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000317` | CAT II | `SRG-APP-000516` | The network device must be configured in accordance with the security configuration settings based on DoD security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | `SRG-APP-000516` | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | `SRG-APP-000516` | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000344` | CAT II | `SRG-APP-000516` | The network device must obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | `SRG-APP-000516` | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000820-NDM-000170` | CAT II | `SRG-APP-000820` | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| NDM | `SRG-APP-000845-NDM-000220` | CAT II | `SRG-APP-000845` | The network device must be configured to verify, when users create or update passwords, the passwords are not found on the list of commonly used, expected, or compromised passwords in IA-5 (1) (a) for password-based authentication. |
| NDM | `SRG-APP-000880-NDM-000290` | CAT II | `SRG-APP-000880` | The network device must be configured to protect nonlocal maintenance sessions by separating the maintenance session from other network sessions with the system by logically separated communications paths. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | `SRG-APP-000910` | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | `SRG-APP-000920` | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | `SRG-APP-001035` | The network device hardware and software must be a version supported by the vendor. |
| AAA | `SRG-APP-000024-AAA-000040` | CAT II | `SRG-APP-000024` | AAA Services must be configured to automatically remove temporary user accounts after 72 hours. |
| AAA | `SRG-APP-000024-AAA-000050` | CAT II | `SRG-APP-000024` | AAA Services must be configured to automatically remove authorizations for temporary user accounts after 72 hours. |
| AAA | `SRG-APP-000025-AAA-000080` | CAT II | `SRG-APP-000025` | AAA Services must be configured to automatically disable accounts after a 35-day period of account inactivity. |
| AAA | `SRG-APP-000089-AAA-000380` | CAT II | `SRG-APP-000089` | AAA Services must be configured to audit each authentication and authorization transaction. |
| AAA | `SRG-APP-000142-AAA-000010` | CAT I | `SRG-APP-000142` | AAA Services must be configured to use secure protocols when connecting to directory services. |
| AAA | `SRG-APP-000142-AAA-000020` | CAT I | `SRG-APP-000142` | AAA Services must be configured to use protocols that encrypt credentials when authenticating clients, as defined in the PPSM CAL and vulnerability assessments. |
| AAA | `SRG-APP-000142-AAA-000680` | CAT II | `SRG-APP-000142` | AAA Services must be configured to prohibit or restrict the use of organization-defined functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. |
| AAA | `SRG-APP-000148-AAA-000390` | CAT I | `SRG-APP-000148` | AAA Services must be configured to uniquely identify and authenticate organizational users. |
| AAA | `SRG-APP-000158-AAA-000420` | CAT II | `SRG-APP-000158` | AAA Services used for 802.1x must be configured to uniquely identify network endpoints (supplicants) before the authenticator establishes any connection. |
| AAA | `SRG-APP-000172-AAA-000520` | CAT I | `SRG-APP-000172` | AAA Services must be configured to encrypt transmitted credentials using a FIPS-validated cryptographic module. |
| AAA | `SRG-APP-000175-AAA-000570` | CAT I | `SRG-APP-000175` | AAA Services must be configured to only accept certificates issued by a DoW-approved certificate authority (CA) for Public Key Infrastructure (PKI)-based authentication. |
| AAA | `SRG-APP-000175-AAA-000580` | CAT I | `SRG-APP-000175` | AAA Services must be configured to not accept certificates that have been revoked for PKI-based authentication. |
| AAA | `SRG-APP-000177-AAA-000600` | CAT II | `SRG-APP-000177` | AAA Services must be configured to map the authenticated identity to the user account for PKI-based authentication. |
| AAA | `SRG-APP-000358-AAA-000280` | CAT II | `SRG-APP-000358` | AAA Services must be configured to send audit records to a centralized audit server. |
| AAA | `SRG-APP-000394-AAA-000430` | CAT II | `SRG-APP-000394` | AAA Services used for 802.1x must be configured to authenticate network endpoint devices (supplicants) before the authenticator establishes any connection. |
| AAA | `SRG-APP-000516-AAA-000440` | CAT II | `SRG-APP-000516` | AAA Services used for 802.1x must be configured to use secure Extensible Authentication Protocol (EAP), such as EAP-TLS, EAP-TTLS, and PEAP. |
| AAA | `SRG-APP-000516-AAA-000640` | CAT II | `SRG-APP-000516` | AAA Services must be configured to use a unique shared secret for communication (i.e. RADIUS, TACACS+) with clients requesting authentication services. |
| AAA | `SRG-APP-000516-AAA-000660` | CAT II | `SRG-APP-000516` | AAA Services must be configured to place non-authenticated network access requests in the Unauthorized VLAN or the Guest VLAN with limited access. |
| AAA | `SRG-APP-000875-AAA-000220` | CAT II | `SRG-APP-000875` | For public key-based authentication, AAA Services must be configured to implement a local cache of revocation data to support path discovery and validation. |
| AAA | `SRG-APP-000910-AAA-000230` | CAT II | `SRG-APP-000910` | AAA Services must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| ISE | `CSCO-NC-000010` | CAT I | `SRG-NET-000062-NAC-000340` | The Cisco ISE must use TLS 1.2, at a minimum, to protect the confidentiality of information passed between the endpoint agent and the Cisco ISE. |
| ISE | `CSCO-NC-000020` | CAT I | `SRG-NET-000015-NAC-000020` | The Cisco ISE must enforce approved access by employing authorization policies with specific attributes; such as resource groups, device type, certificate attributes, or any other attributes that are specific to a group of endpoints, and/or mission conditions as defined in the site's Cisco ISE System Security Plan (SSP). |
| ISE | `CSCO-NC-000030` | CAT I | `SRG-NET-000015-NAC-000020` | The Cisco ISE must be configured to profile endpoints connecting to the network. |
| ISE | `CSCO-NC-000040` | CAT I | `SRG-NET-000015-NAC-000020` | The Cisco ISE must verify host-based firewall software is running on posture required clients defined in the NAC System Security Plan (SSP) prior to granting trusted network access. |
| ISE | `CSCO-NC-000050` | CAT I | `SRG-NET-000015-NAC-000020` | The Cisco ISE must verify anti-malware software is installed and up to date on posture required clients defined in the NAC System Security Plan (SSP) prior to granting trusted network access. |
| ISE | `CSCO-NC-000060` | CAT I | `SRG-NET-000015-NAC-000020` | The Cisco ISE must verify host-based IDS/IPS software is authorized and running on posture required clients defined in the NAC System Security Plan (SSP) prior to granting trusted network access. |
| ISE | `CSCO-NC-000070` | CAT II | `SRG-NET-000015-NAC-000040` | For endpoints that require automated remediation, the Cisco ISE must be configured to redirect endpoints to a logically separate VLAN for remediation services. |
| ISE | `CSCO-NC-000080` | CAT III | `SRG-NET-000015-NAC-000070` | The Cisco ISE must be configured to notify the user before proceeding with remediation of the user's endpoint device when automated remediation is used. |
| ISE | `CSCO-NC-000090` | CAT II | `SRG-NET-000015-NAC-000080` | The Cisco ISE must be configured so that all endpoints that are allowed to bypass policy assessment are approved by the Information System Security Manager (ISSM) and documented in the System Security Plan (SSP). |
| ISE | `CSCO-NC-000100` | CAT II | `SRG-NET-000015-NAC-000100` | The Cisco ISE must send an alert to the Information System Security Manager (ISSM) and System Administrator (SA), at a minimum, when security issues are found that put the network at risk. |
| ISE | `CSCO-NC-000110` | CAT II | `SRG-NET-000015-NAC-000110` | When endpoints fail the policy assessment, the Cisco ISE must create a record with sufficient detail suitable for forwarding to a remediation server for automated remediation or sending to the user for manual remediation. |
| ISE | `CSCO-NC-000120` | CAT II | `SRG-NET-000015-NAC-000120` | The Cisco ISE must place client machines on the blacklist and terminate the agent connection when critical security issues are found that put the network at risk. |
| ISE | `CSCO-NC-000130` | CAT II | `SRG-NET-000015-NAC-000130` | The Cisco ISE must be configured so client machines do not communicate with other network devices in the DMZ or subnet except as needed to perform an access client assessment or to identify themselves. |
| ISE | `CSCO-NC-000140` | CAT II | `SRG-NET-000322-NAC-001230` | The Cisco ISE must deny or restrict access for endpoints that fail required posture checks. |
| ISE | `CSCO-NC-000150` | CAT II | `SRG-NET-000492-NAC-002100` | The Cisco ISE must generate a log record when an endpoint fails authentication. |
| ISE | `CSCO-NC-000160` | CAT II | `SRG-NET-000492-NAC-002101` | The Cisco ISE must generate a log record when the client machine fails posture assessment because required security software is missing or has been deleted. |
| ISE | `CSCO-NC-000170` | CAT II | `SRG-NET-000492-NAC-002120` | The Cisco ISE must send an alert to the system administrator, at a minimum, when endpoints fail the policy assessment checks for organization-defined infractions. |
| ISE | `CSCO-NC-000200` | CAT II | `SRG-NET-000335-NAC-001360` | The Cisco ISE must generate a critical alert to be sent to the ISSO and SA (at a minimum) in the event of an audit processing failure. |
| ISE | `CSCO-NC-000210` | CAT II | `SRG-NET-000335-NAC-001370` | The Cisco ISE must provide an alert to, at a minimum, the SA and ISSO of all audit failure events where the detection and/or prevention function is unable to write events to either local storage or the centralized server. |
| ISE | `CSCO-NC-000220` | CAT II | `SRG-NET-000336-NAC-001390` | The Cisco ISE must be configured with a secondary log server in case the primary log is unreachable. |
| ISE | `CSCO-NC-000230` | CAT II | `SRG-NET-000088-NAC-000440` | The Cisco ISE must generate a critical alert to be sent to the ISSO and SA (at a minimum) if it is unable to communicate with the central event log. |
| ISE | `CSCO-NC-000240` | CAT II | `SRG-NET-000089-NAC-000450` | The Cisco ISE must continue to queue traffic log records locally when communication with the central log server is lost and there is an audit archival failure. |
| ISE | `CSCO-NC-000250` | CAT II | `SRG-NET-000512-NAC-002310` | The Cisco ISE must perform continuous detection and tracking of endpoint devices attached to the network. |
| ISE | `CSCO-NC-000260` | CAT II | `SRG-NET-000148-NAC-000620` | The Cisco ISE must deny network connection for endpoints that cannot be authenticated using an approved method. |
| ISE | `CSCO-NC-000270` | CAT II | `SRG-NET-000343-NAC-001460` | The Cisco ISE must authenticate all endpoint devices before establishing a connection and proceeding with posture assessment. |
| ISE | `CSCO-NC-000280` | CAT II | `SRG-NET-000343-NAC-001470` | The Cisco ISE must be configured to dynamically apply restricted access of endpoints that are granted access using MAC Authentication Bypass (MAB). |
| ISE | `CSCO-NC-000290` | CAT II | `SRG-NET-000550-NAC-002470` | Before establishing a connection with a Network Time Protocol (NTP) server, the Cisco ISE must authenticate using a bidirectional, cryptographically based authentication method that uses a FIPS-validated Advanced Encryption Standard (AES) cipher block algorithm to authenticate with the NTP server. |
| ISE | `CSCO-NC-000300` | CAT II | `SRG-NET-000151-NAC-000630` | Before establishing a local, remote, and/or network connection with any endpoint device, the Cisco ISE must use a bidirectional authentication mechanism configured with a FIPS-validated Advanced Encryption Standard (AES) cipher block algorithm to authenticate with the endpoint device. |
| ISE | `CSCO-NC-000310` | CAT I | `SRG-NET-000512-NAC-002310` | The Cisco ISE must enforce posture status assessment for posture required clients defined in the NAC System Security Plan (SSP). |
| ISE | `CSCO-NC-000320` | CAT I | `SRG-NET-000512-NAC-002310` | The Cisco ISE must have a posture policy for posture required clients defined in the NAC System Security Plan (SSP). |

### Collecting evidence

Run `get system status` and `show full-configuration` in the global,
interface, and NTP contexts on the CLI, and keep the output with the
checklist, together with the firmware version from the *System Summary*
dashboard widget and the latest database and system backups. Add
screenshots or exports of the panes the map cites, above all *Users &
Hosts > Administrators* (with the Profiles tab), *System > Settings >
Authentication > Directories*, *System > Settings > Authentication >
Multi-factor Authentication*, *System > Settings > Persistent Agent >
Transport configurations*, *System > Settings > System communication >
Log receivers*, *System > Settings > System communication > SNMP*,
*System > Settings > System management > Remote backup configuration*,
*System > Certificate management*, *Network > RADIUS > Configure Local
Server*, *Policy & Objects > Network access*, *Policy & Objects >
Endpoint compliance*, *System > Groups*, and *System > Settings >
User/Host Management > MAC address exclusion*. Export the admin auditing
log from *Logs > Audit Logs*, the events from the log receivers, and the
scan results report, and keep the firmware upgrade history and the
backup schedule.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiNAC.** Check the version
  column against the FortiNAC-F release, and check whether the feature
  depends on the license level, the appliance type (CA or Manager), or a
  third-party product.
- **A setting is not where the map says.** The policy, portal, and Actions
  views were rewritten in 7.2.0 and 7.6.0, and 7.6.7 added a reorganized
  *Network* menu with configuration selectors for RADIUS-only devices. Look for the setting under the
  older name, and check the Administration Guide of your release.
- **A command is rejected.** The commands were checked against the 7.6.0
  CLI Reference; on 7.2 and 7.4 some options (the CLI lockout settings,
  `http-proxy`, interface `status`) do not exist. Use `help` or the Tab key
  in each context to list the options of your release.
- **Endpoints stop getting access after hardening.** Check the `allowaccess`
  list of each interface (RADIUS, DHCP, DNS, the agent, and syslog all need
  their entries), the RADIUS secret of each device, the TLS protocols of
  the RADIUS and agent TLS service configurations (older agents and
  supplicants may not support TLS 1.3 alone), and the OCSP responder.
- **Administrators are locked out after enabling MFA.** Reset the
  individual and global MFA settings with `execute admin-ui
  reset-mfa-settings` on the CLI, then fix the email or SMS settings.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (account reviews, checksum checks), by another system (the
  directory, the identity provider, the central log server), or not at
  all. Record how each requirement is met, not just which feature covers
  it.

## Security and Best Practices

- Keep FortiNAC-F on a vendor-supported release on FortiNAC-OS, and
  install patches promptly; on releases before 7.6.3, check the image
  checksum.
- Allow only HTTPS for the Admin UI and SSH on port1, enable
  `strong-crypto`, and allow only TLS 1.2 and 1.3 everywhere.
- Authenticate administrators through LDAP over SSL or STARTTLS, RADIUS,
  or SAML with CAC; keep the local and CLI admin accounts as accounts of
  last resort; and give everyone else a least-privilege profile with a
  5-minute inactivity time and a 3-attempt lockout.
- Use EAP-TLS, PEAP, TTLS, or TEAP only, a unique RADIUS secret (or RadSec)
  for each device, OCSP without soft fail, and DoD CAs only.
- Profile every endpoint, enforce posture before trusted access, send
  failing hosts to remediation, and approve every exception in writing.
- Send events to two log receivers, map security events to alarms that
  reach the SA and ISSO, use SNMPv3 only, and back up to a remote server
  over SSH or SFTP.
- Review this map each time Fortinet publishes a FortiNAC-F release or
  DISA updates the NDM SRG, the AAA Services SRG, or the NAC STIGs.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiNAC-F Release Notes*, page "What's new", releases 7.2.0
  to 7.2.9, 7.4.0 to 7.4.4, and 7.6.0 to 7.6.7 (docs.fortinet.com,
  FortiNAC-F documentation).
- Fortinet, *FortiNAC-F 7.6.0 CLI Reference Guide* and *FortiNAC-OS 7.2.0
  CLI Reference* (and the 7.4.0 CLI Reference Guide, for the version of
  the lockout settings).
- Fortinet, *FortiNAC F 7.6.0 Administration Guide* (online) and
  *FortiNAC F 7.2.0 Administration Guide* (for the core features).
- DISA Network Device Management SRG V5R5, AAA Services SRG V2R3, and
  Cisco ISE NAC STIG V2R4 (with the Ivanti Policy Secure NAC STIG V1R1 for
  comparison), from the October 2026 STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map), and
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the model for this chapter).

**Knowledge checks:**

1. Why does this chapter cover FortiNAC-F and not the legacy FortiNAC 9.x
   releases that Fortinet still documents?
2. Why does the map cite Cisco ISE NAC STIG rules, and how should an
   assessor use them on a FortiNAC checklist?
3. Which FortiNAC functions fall under the AAA Services SRG, and which
   under the NDM SRG?
4. Where does the version data come from, and how are features listed in
   more than one train shown?
5. Which features keep unknown and non-compliant endpoints out of
   production networks, and which requirements do they support?
6. Which requirements can FortiNAC-F not meet exactly, and how do you
   handle them?

## Summary and Completion Checklist

FortiNAC has no STIG, so it is assessed against the NDM SRG for its
management plane, the AAA Services SRG for its RADIUS server, and the
Cisco ISE NAC STIG as the pattern that DISA expects of the network access
function. This chapter maps 172 features to the FortiNAC-F release
that introduced them, to 97 requirements (47 NDM, 20
AAA, and 30 ISE), and to the FortiNAC-F CLI command or GUI pane that
configures them: 53 core platform features, and 119 features
from the FortiNAC-F 7.2.0 through 7.6.7 release notes. Operational
features with no direct requirement fall under the requirement to
prohibit unnecessary functions when unused.

- [ ] Can explain the scope choice between FortiNAC-F and legacy
  FortiNAC.
- [ ] Can find the release that introduced a FortiNAC-F feature.
- [ ] Can map a FortiNAC-F feature to its NDM or AAA requirement, or to
  the ISE pattern rule, and explain what the ISE rule means for FortiNAC.
- [ ] Can find the FortiNAC-F CLI command or GUI pane that meets the
  requirement.
- [ ] Can collect FortiNAC-F's evidence and record the requirements it
  cannot meet exactly.
