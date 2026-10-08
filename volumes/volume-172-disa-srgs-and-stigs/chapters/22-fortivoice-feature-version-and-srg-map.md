# Chapter 22: FortiVoice Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiVoice release that introduced a given feature.
- Map each FortiVoice feature to the Enterprise Voice, Video, and
  Messaging (EVVM) or Network Device Management (NDM) SRG requirement it
  helps satisfy.
- Explain which of the EVVM SRGs (session management, endpoint, and
  policy) applies to which part of a FortiVoice deployment.
- Find the FortiVoice web UI pane, or the documented CLI command, that
  configures each feature to meet its requirement.
- Use the map to scope an SRG-based assessment of FortiVoice, which has
  no STIG of its own.
- Record the requirements that FortiVoice cannot meet exactly, with their
  mitigations.

## Theory and Architecture

FortiVoice Enterprise is Fortinet's IP PBX and unified communications
system. The FortiVoice phone system registers IP phones (FortiFone desk,
DECT, and WiFi phones and supported third-party phones), FortiFone
Softclient for desktop and mobile, and analog extensions through FortiVoice
gateways; it routes calls between them and to the outside world over SIP
trunks, PRI and analog trunks, and office peer trunks to other FortiVoice
systems; and it adds voicemail, conferencing, call recording, call center,
chat, SMS, and emergency (E911) calling. It has **no DISA STIG**
(Chapter 10), so it is assessed against SRGs, as described in Chapter 03.
Chapter 10 assigns it the **Enterprise Voice, Video, and Messaging (EVVM)
SRGs** (session management, endpoint, and policy) and the **Network Device
Management (NDM) SRG**. For every FortiVoice feature the chapter gives
**which FortiVoice release introduced it**, **which requirement it relates
to**, and **which web UI pane or command configures it to meet that
requirement**.

FortiVoice runs on FVE hardware appliances and as a virtual machine; this
chapter covers that FortiVoice Enterprise phone system firmware, not the
Fortinet-hosted FortiVoice Cloud service or the firmware of the phones and
gateways themselves. Its configuration uses a few ideas again and again:

- **Two portals.** Administrators use the admin portal
  (`https://<FORTIVOICE>/admin`) and the CLI console; extension users use
  the user portal (`https://<FORTIVOICE>/voice`) and the softclients. The
  admin side is governed by administrator accounts, admin profiles, and
  trusted hosts; the user side by each extension's Web Access settings.
- **Extensions and devices.** An *IP extension* is a number with a SIP
  password, a user password, and a voicemail PIN; a *phone* is a device
  identified by its MAC address and model that is assigned to an extension.
  *Auto-provisioning* sends each phone its configuration file, and can
  generate a default configuration for phones that are not yet assigned.
- **Profiles.** *SIP profiles* set the transport (UDP, TCP, or TLS),
  Secure RTP, codecs, and registration intervals for phones and trunks;
  *phone profiles* set what is pushed to FortiFone phones, such as voice and
  data VLAN tags and the phone admin password; *user privileges* set what
  each group of extensions may do (call forwarding, call restrictions,
  recording, barging, hot desking, trusted hosts for registration).
- **Trunks and survivability.** SIP trunks register with a service
  provider, office peers link FortiVoice systems, and local survivable
  gateways (LSG) keep branch offices working when the main office cannot be
  reached.
- **Security settings.** Intrusion detection, SIP authentication failure
  blocking, the password and PIN policy, the password auditor, web service
  rate limits, account codes, and blocked numbers are under *Security*;
  certificates, SNMP, time, HA, and backups are under *System*; logging,
  call detail records (CDR), and alert email are under *Log & Report*.

### Where the version data comes from

Fortinet publishes no Feature Matrix and no New Features Guide for
FortiVoice. The **Release Notes** of every FortiVoice phone system release,
however, have a "What's new" page with a table of the release's new
features and enhancements, each with a description (and, from 7.2.4, links
to the Administration Guide). docs.fortinet.com lists the FortiVoice
Enterprise trains 5.3, 6.0, 6.4, 7.0, 7.2, 7.4, and 8.0; this chapter
covers the 7.0 train, the oldest 7.x train, through 8.0, the newest. The
version column was built from the "What's new" pages of every release in
those trains: 7.0.0 through 7.0.8, 7.2.0 through 7.2.5, 7.4.0 through
7.4.2, 8.0.0, and 8.0.1 (whose release notes are titled *FortiVoice
Release Notes* instead of *FortiVoice Phone System Release Notes*), 20
releases in all. Two pages list no features: 7.0.4 says that there are no
new features in the release, and 8.0.1 that it contains none. The "What's
changed" pages, which describe changed behavior rather than new features,
were not used.

Each body row of a "What's new" table is one entry, with its title from
the first column and its description from the second; notes and tables
nested in a description (such as the 7.2.3 list of call event filters)
were kept as part of the description. No entry was split or dropped.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: management
  access, administrator accounts and admin profiles, remote authentication,
  the password policy, endpoint registration and provisioning, trunks and
  SIP profiles, user privileges, intrusion detection, logging and call
  records, alerts, SNMP, time, network settings, phone profiles, HA,
  firmware, backups, and certificates. Each one is described in the
  **FortiVoice Phone System 7.0.0 Administration Guide**, so it existed in
  7.0.0 and is not in the release notes lists. Five core rows have a
  different version entry, explained below.
- **New features** are the 113 entries of the "What's new" pages.
  The categories were assigned for this chapter, because the release notes
  list features without categories, and the titles were
  shortened from the release notes text. An entry listed again in a later
  release or train is one row with all its versions.

| Version entry | Meaning |
| --- | --- |
| `7.0.0 or earlier` | A core feature described in the FortiVoice Phone System 7.0.0 Administration Guide, the oldest release covered |
| `7.2.3 and later` | Introduced in FortiVoice 7.2.3 |
| `7.0.5+; 7.2.0+` | Listed in two trains: from 7.0.5 in the 7.0 train and from 7.2.0 in the 7.2 train |
| `5.0.4 (technote)` | Documented in the Fortinet technote *Increasing FortiVoice Enterprise Encryption Level*, which applies to release 5.0.4 and later (the strong cryptography setting) |
| `8.0 (Solution Guide)` | Documented only in the *FortiVoice 8.0 Solution Guide* (per-service cryptography and verification of the SIP user agent) |
| `8.0.0 or earlier` | In the 8.0.0 Administration Guide, but in no release notes page and not found in the 7.0.0 Administration Guide (the SIP registration log and keypad locking) |

Three cautions apply. First, "and later" means later in the same train
and, usually, in later trains; a feature of a patch release may reach a
newer train only in a later patch (the FON-W80B phone and Portuguese
arrived in 7.0.6 and 7.2.0, for example). Second, many features depend on
the model (RAID on FVE-2000F and FVE-5000F, FXS ports on small appliances,
higher limits on FVE-VM-10000 and above), on the phone model (most phone
profile settings apply only to some FortiFone models, and legacy FortiFone
models have limited or no TLS support), or on a license or entitlement
(FortiFone Softclient licenses, Unified Communications Services before
8.0.0, FortiCall, Mass Notifications, FortiCare Premium for the firmware
store). Third, a core row records a FortiVoice capability, but its pane was
checked against the 8.0.0 documents and may be named or placed differently
on an older release, and several settings arrived later, as the new-feature
rows say (web service limits in 7.0.2, RADIUS and SSO for extension web
access in 7.0.5 and 7.2.0, CDR event filters in 7.2.3, and role-based
access control for calls in 7.4.2).

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library. The
EVVM SRGs come from one zip file, `U_EVVM_Y26M07_SRG.zip`, which holds
three SRGs:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **EVVM-SM** | EVVM Session Management SRG | V1R3, benchmark date 01 Jul 2026 | The FortiVoice phone system as the session manager: endpoint and trunk registration and authentication, user and device privileges, call records, encryption of signaling and media, denial-of-service protection, VLANs, time, and DNS (primary SRG) |
| **EVVM-EP** | EVVM Endpoint SRG | V1R3, benchmark date 01 Oct 2025 | The phones and softclients, for the settings that FortiVoice pushes to them: VLAN tags, the phone admin password, auto answer, default credentials, firmware, and configuration updates |
| **EVVM-PM** | EVVM Policy SRG | V1R4, benchmark date 05 Jan 2026 | Site policy that FortiVoice features support: emergency (E911) calling, survivability, softclient approval, the inventory of instruments, video phone cameras and microphones, and commercial SIP providers |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The management plane: administrator access, authentication, passwords, logging, SNMP, time, firmware, backups, and certificates |

The **session management SRG** is the primary SRG, because FortiVoice is
the system that registers endpoints and sets up calls. Its management
requirements overlap with the NDM SRG (banner, concurrent sessions,
lockout, TLS, time); the map gives the NDM requirement for the management
plane and adds the session management requirement where it says something
specific to voice. The **endpoint SRG** applies to the phones and
softclients, which are assessed in their own right (on the phone, on the
access switch, and in the softclient); this chapter uses it only for the
endpoint settings that FortiVoice controls. The **policy SRG** is mostly
about the site, not the product; it is used only where a FortiVoice
feature is how the policy is carried out.

Several EVVM requirements do not apply to FortiVoice, or apply only to
another system:

- **Multilevel precedence and preemption (MLPP)** for command and control
  (C2) users (EVVM-SM `SRG-NET-000225-VVSM-00101`,
  EVVM-SM `SRG-NET-000226-VVSM-00101`, and
  EVVM-SM `SRG-NET-000354-VVSM-00101`): FortiVoice documents no MLPP or
  AS-SIP support, so it cannot serve C2 users that need it.
- **Session Border Controller (SBC) requirements** of the policy SRG
  (SRG-VOIP-000470 through SRG-VOIP-000560): they belong to the SBC or the
  SIP-aware firewall at the enclave boundary, such as FortiGate, not to the
  phone system.
- **VTC periods processing, A/B switches, backup power, and DISN access
  circuits** in the policy SRG: they describe rooms, circuits, and power,
  not FortiVoice settings.
- **Endpoint-only requirements** such as 802.1X
  (EVVM-EP `SRG-NET-000018-VVEP-00102`) and MAC Authentication Bypass
  (EVVM-EP `SRG-NET-000018-VVEP-00106`), the logon banner and last
  logon notice on the endpoint, and its own audit records: they are met on
  the phone, the softclient, or the access switch.

The requirement IDs are the **rule version IDs** from the XCCDF files, and
the severity is the rule's severity (high = CAT I, medium = CAT II, low =
CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiVoice meets a
  requirement. Intrusion detection and SIP authentication failure blocking
  implement attack-resistant endpoint registration
  (EVVM-SM `SRG-NET-000147-VVSM-00101`), for example.
- **Must be configured to meet a requirement.** The feature is in scope of
  a requirement and has to be set up correctly. Generation of a default
  configuration for phones that are not assigned must be turned off to
  prevent auto-registration (EVVM-SM `SRG-NET-000015-VVSM-00101`, CAT I),
  for example.
- **No direct requirement.** The feature is operational, such as a phone
  model, a language, a call center report, or a GUI change. It has no
  requirement of its own, but if it is not needed it falls under the
  session management requirement to disable nonessential capabilities
  (EVVM-SM `SRG-NET-000131-VVSM-00101`).

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially the split between the three EVVM SRGs, and
where a requirement is organization-defined or depends on how FortiVoice
is deployed.

### Where the commands come from

Fortinet publishes **no CLI Reference for FortiVoice**: none of the
FortiVoice Enterprise trains on docs.fortinet.com (5.3 through 8.0) has
one, and the FortiVoice CLI is described only in passing. The command
column therefore names the **web UI pane** from the **FortiVoice Phone
System 8.0.0 Administration Guide** (last updated 17 July 2026), the newest
Administration Guide, for most rows, and uses the CLI only where Fortinet
documents a FortiVoice command: in that guide, and in the **Security**
section of the **FortiVoice 8.0 Solution Guide** (last updated 23
September 2026). The check was automatic: each `config` path, `edit` name,
`set` option, and literal value against the FortiVoice CLI blocks printed
in those two guides (the FortiGate CLI blocks of the Solution Guide were
left out), each `execute`, `get`, or `diagnose` command against their
text, and each GUI pane against the text of the two guides. One pane,
*Security > Call Access > Role Base Access Control*, appears only in the
7.4.2 release notes and not in the 8.0.0 Administration Guide; it was
checked against the release notes. Read the column this way:

- **GUI:** entries name the FortiVoice admin portal pane; the text in
  parentheses names the fields to set.
- Commands run on the FortiVoice CLI, over SSH, the console, or the CLI
  console in the admin portal; the administrator needs the CLI access mode.
- Statements are separated by `;` to fit in a table cell; on the CLI, enter
  each one on its own line. Values in `<ANGLE_BRACKETS>` are placeholders
  for your own values.
- For **"No direct requirement"** rows, the command shown is the one that
  disables the feature when it is unused. A dash (**—**) means there is
  nothing to change: the feature is a platform, a language, a GUI change, a
  behavior change, a report detail, or a capability that is off unless
  configured, or the 8.0.0 documents have no setting for it.

Some requirements cannot be met exactly with FortiVoice settings. Record
them on the checklist as open findings with mitigations, or meet them
another way:

- **No CLI Reference.** Settings without a documented command can be
  checked only in the admin portal, and the few documented commands are
  examples rather than a full syntax. The release notes name one CLI option
  (`from-header-parameters` for SIP trunks) without its configuration
  path. Use the web UI panes and configuration backups as evidence.
- **No logon banner.** The 8.0.0 Administration Guide documents no login
  disclaimer or banner for the admin portal, the user portal, or SSH, so
  the Standard Mandatory DoD Notice and Consent Banner
  (NDM `SRG-APP-000068-NDM-000215`, NDM `SRG-APP-000069-NDM-000216`,
  EVVM-SM `SRG-NET-000041-VVSM-00101`, and
  EVVM-SM `SRG-NET-000042-VVSM-00101`) cannot be shown by FortiVoice
  itself. Where single sign-on is used, show the banner on the identity
  provider's login page; otherwise record the finding.
- **No account lockout.** No setting locks an administrator or extension
  account after failed logins (NDM `SRG-APP-000065-NDM-000214`,
  EVVM-SM `SRG-NET-000395-VVSM-00010`). Intrusion detection and SIP
  authentication failure blocking block the source IP address of SIP
  attacks, and repeat offender control blocks addresses that send bad HTTP
  requests, but neither is an account lockout. Enforce the lockout on the
  LDAP, RADIUS, or SAML server, restrict logins with trusted hosts, and
  record the finding for local accounts.
- **Inactive accounts.** Nothing disables accounts after 35 days of
  inactivity (EVVM-SM `SRG-NET-000004-VVSM-00101`). Review administrator
  accounts and extensions on a schedule, or manage users in the directory
  through LDAP, RADIUS, or SSO.
- **Password rules.** The password and PIN policy sets the minimum length
  (8 by default), the character types, and PIN expiration, and applies to
  administrators, SIP users, and user portal passwords; no setting is
  documented for password expiration, the number of changed characters
  (NDM `SRG-APP-000170-NDM-000329`), or a check against a list of commonly
  used or compromised passwords (NDM `SRG-APP-000845-NDM-000220`). The
  documented defaults are weak (no admin password until one is set, SIP and
  user password voice#321, voicemail PIN 123123), and the policy must stay
  enabled so that an empty admin password is not allowed. Prefer remote
  authentication.
- **No PKI login on FortiVoice itself.** Administrators authenticate
  locally or through LDAP, RADIUS, or single sign-on; two-factor
  authentication is done on FortiAuthenticator or another identity
  provider. FortiVoice has no certificate (CAC) login of its own, so DoD
  PKI multifactor authentication (NDM `SRG-APP-000149-NDM-000247`, CAT I)
  is met only through a SAML identity provider or RADIUS server that
  enforces it. Keep one local account of last resort and record how the
  requirement is met.
- **FIPS-validated cryptography.** The FortiVoice documents describe no
  FIPS or Common Criteria mode (EVVM-SM `SRG-NET-000510-VVSM-00101`,
  NDM `SRG-APP-000412-NDM-000331`, NDM `SRG-APP-000179-NDM-000265`). The
  strong cryptography setting (`set strong-crypto enable` under
  `config system global`) removes SSL 3.0 and weak ciphers, but the
  technote that describes it lists TLS 1.0 and 1.1 and SHA-1 cipher suites
  among those still accepted. Allow only TLS 1.2 and 1.3 with the
  per-service setting (`config system security crypto`), use TLS and
  Secure RTP in every SIP profile, and check the NIST Cryptographic Module
  Validation Program for your release. The Solution Guide prints the global
  TLS version command as `set ssl-version <TLS versions>`, while the older
  technote uses `ssl-versions`; verify the option name on your release with
  the CLI's own help before relying on it.
- **Legacy phones.** Some legacy FortiFone models have limited TLS support
  and others none, so they cannot meet the requirement to protect
  signaling and media (EVVM-SM `SRG-NET-000371-VVSM-00101`, CAT I).
  Replace them, or keep them on an isolated voice VLAN and record the
  finding.
- **Concurrent sessions.** *Maximum Login Session* in the web service
  settings (7.0.2 and later) limits the total number of active admin portal
  sessions, not the number for each account
  (NDM `SRG-APP-000001-NDM-000200`). Set it to the organization-defined
  limit and record the difference.
- **SNMPv3 and NTP.** SNMPv3 users offer SHA1 or MD5 for authentication;
  use SHA1, since no SHA-2 option is documented
  (NDM `SRG-APP-000395-NDM-000310`). No NTP authentication is documented
  (NDM `SRG-APP-000395-NDM-000347`); use NTP servers on the protected
  management network.
- **Log transport and lost log servers.** Remote logging is documented
  only as syslog on UDP port 514 (or FortiAnalyzer on 514), with no TLS,
  and nothing alerts when a log server stops receiving logs
  (NDM `SRG-APP-000360-NDM-000295`); the RESTful service alert covers only
  the CDR and call event servers. Send logs over a protected management
  network to two servers, and alert on missing logs at the log server.
- **Firmware signatures.** The Administration Guide does not say that
  FortiVoice verifies a digital signature on firmware images
  (NDM `SRG-APP-000131-NDM-000243`). Compare the image checksum with the
  one on the Fortinet support site before every upgrade.
- **Bandwidth.** FortiVoice sets the 802.1p priority that phones put on
  voice and data traffic, but it cannot reserve bandwidth
  (EVVM-SM `SRG-NET-000363-VVSM-00019`); configure quality of service on
  the switches and routers.
- **Data that leaves the enclave.** Voicemail and call recording
  transcription and text-to-speech send audio or text to a third-party AI
  platform; the 7.2.3 release notes say that enabling voicemail
  transcription is consent to the upload. Keep them off unless the
  sharing is approved.

## Design Considerations

- **Pick the release first, then the features.** If your design depends on
  a feature introduced in a certain release (web service limits in 7.0.2,
  RADIUS for extension web access in 7.0.5 and 7.2.0, CDR event filters in
  7.2.3, or role-based access control for calls in 7.4.2), that sets the
  minimum FortiVoice release, and it must be a vendor-supported release
  (NDM `SRG-APP-001035-NDM-000340`).
- **Separate voice from data.** Put FortiVoice and the phones on a voice
  VLAN, push voice and data VLAN tags in the phone profiles, use 802.1X or
  MAB on the access switches, and allow only the PPSM-approved SIP, RTP,
  and provisioning ports between the voice VLAN and other networks.
- **Encrypt signaling and media.** Use TLS transport and Secure RTP in
  every SIP profile, assign a DoD-issued certificate to SIP TLS, SIP WSS,
  and HTTPS, provision phones over HTTPS, and turn TFTP off.
- **Close the registration path.** Turn off generation of default
  configuration for phones that are not assigned once the phones are
  deployed, assign each phone by MAC address, set trusted hosts in the user
  privileges, enable SIP user agent verification and intrusion detection,
  and keep registration intervals short enough for the re-registration
  requirements.
- **Keep management and remote users out of band.** Allow HTTPS and SSH
  only on a management interface, set trusted hosts for every
  administrator, and give remote extensions and softclients access through
  a VPN or a SIP-aware firewall rather than open SIP ports.
- **Use the directory.** Authenticate administrators and extension users
  through LDAP over SSL, RADIUS over TLS, or single sign-on, so that account
  management, lockout, and multifactor authentication are enforced in one
  place.
- **Plan for failure.** Use HA or local survivable gateways where calls
  must continue, keep local commercial lines for emergency calls, and back
  up the configuration on a schedule to an SFTP server.
- **Turn off what is not used.** Telnet, HTTP, TFTP, SNMP v1 and v2c,
  vertical service codes, call bridge (DISA), hot desking, SMDR, the
  Security Fabric connection, transcription, and unused trunks all need a
  reason to stay on.

## Implementation and Automation

### The FortiVoice feature map

The SRG column uses the abbreviations defined in *Where the SRG data comes
from*. The requirement titles are listed in the next table. The command
column follows the conventions in *Where the commands come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/22-fortivoice-feature-version-and-srg-map-feature-map.csv) (172 rows).

| Category | Feature | Introduced (FortiVoice) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Management access | Administrative access protocols on each network interface (HTTPS, HTTP, SSH, Telnet, PING, SNMP, TFTP, NTP, LDAP, SIPPnP, and MDNS) | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; EVVM-SM `SRG-NET-000132-VVSM-00101`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000172-NDM-000259` | GUI: System > Network > Network (Advanced Setting, Access: HTTPS and SSH only on the management interface; HTTP, Telnet, and TFTP off everywhere) |
| Core: Management access | Administration ports for HTTP, HTTPS, SSH, and Telnet (80, 443, 22, and 23 by default) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000132-VVSM-00101` | GUI: System > Configuration > Option (Administration Ports: the ports approved in the PPSM CAL) |
| Core: Management access | Idle timeout for administrator sessions | 7.0.0 or earlier | NDM `SRG-APP-000190-NDM-000267`; NDM `SRG-APP-000220-NDM-000268` | GUI: System > Configuration > Option (Idle timeout: 5 minutes or less) |
| Core: Management access | Trusted hosts for each administrator (user-defined subnets or RFC 1918 predefined) | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213`; NDM `SRG-APP-000880-NDM-000290` | GUI: System > Administrator > Administrator (Trusted hosts type User defined, with the management subnets only, never 0.0.0.0/0.0.0.0) |
| Core: Management access | Administrator logout | 7.0.0 or earlier | NDM `SRG-APP-000296-NDM-000280`; NDM `SRG-APP-000220-NDM-000268` | — |
| Core: Management access | Access modes for each administrator (CLI, GUI, and REST API) | 7.0.0 or earlier | NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000408-NDM-000314` | GUI: System > Administrator > Administrator (Access mode: only the modes each administrator needs) |
| Core: Management access | Local server certificates for HTTPS, LDAPS, SIP TLS, and SIP WSS (Fortinet factory certificate by default) | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; EVVM-SM `SRG-NET-000355-VVSM-00010`; NDM `SRG-APP-000910-NDM-000300` | GUI: System > Certificate > Local Certificate (import a DoD-issued certificate and use Assign to for HTTPS, SIP TLS, and SIP WSS) |
| Core: Management access | Strong cryptography for the TLS services (no SSL 3.0 or weak ciphers) | 5.0.4 (technote) | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; EVVM-SM `SRG-NET-000510-VVSM-00101`; EVVM-SM `SRG-NET-000530-VVSM-00010`; EVVM-SM `SRG-NET-000062-VVSM-00010` | `config system global`; `set strong-crypto enable`; `end` |
| Core: Management access | TLS versions, cipher strength, and Diffie-Hellman size for each service (SIP or HTTPS) | 8.0 (Solution Guide) | EVVM-SM `SRG-NET-000530-VVSM-00010`; EVVM-SM `SRG-NET-000062-VVSM-00010`; EVVM-SM `SRG-NET-000371-VVSM-00101`; NDM `SRG-APP-000412-NDM-000331` | `config system security crypto`; `edit sip`; `set strong-crypto enable`; `set ssl-versions tls1_2 tls1_3`; `next`; `end` (and the same for HTTPS) |
| Core: Management access | System security check and daily security audit (password policy, empty admin password, unsafe SIP passwords and PINs, unassigned phones, TFTP, HTTP, trusted hosts, and APNs certificates) | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000317`; EVVM-SM `SRG-NET-000512-VVSM-00130` | GUI: Log & Report > Alert > Category (Daily Security Audit report; clear every red item of the security alert icon in the top banner) |
| Core: Administrator accounts | Default admin account (no password until one is set) and local administrator accounts | 7.0.0 or earlier | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000153-NDM-000249`; EVVM-SM `SRG-NET-000522-VVSM-00010` | GUI: System > Administrator > Administrator (set the admin password at first login; keep one local account of last resort with a password of 15 or more characters) |
| Core: Administrator accounts | Admin profiles (None, Read Only, or Read-Write for each area; super_admin_prof) | 7.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000516-NDM-000335` | GUI: System > Administrator > Admin Profile (super_admin_prof only for the administrators who need it) |
| Core: Administrator accounts | Department administrators limited to their departments | 7.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212` | GUI: System > Administrator > Administrator (Department only, with Departments) |
| Core: Administrator accounts | Removal of administrator accounts that are no longer used | 7.0.0 or earlier | NDM `SRG-APP-000029-NDM-000211`; EVVM-SM `SRG-NET-000004-VVSM-00101` | GUI: System > Administrator > Administrator (delete inactive accounts; no setting disables them automatically) |
| Core: Authentication | LDAP profiles for administrator and extension authentication (secure connection over LDAPS) | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; EVVM-SM `SRG-NET-000138-VVSM-00102`; NDM `SRG-APP-000172-NDM-000259` | GUI: Phone System > LDAP > LDAP Profile (Secure Connection: SSL, with the DoD CA certificate) |
| Core: Authentication | RADIUS profiles for administrator and extension authentication (RADIUS over TLS with a CA certificate) | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000825-NDM-000180`; EVVM-SM `SRG-NET-000138-VVSM-00102` | GUI: Phone System > Profile > RADIUS (Transport protocol TLS and a CA certificate; the RADIUS server enforces DoD PKI or another approved second factor) |
| Core: Authentication | Password and PIN policy for administrators, SIP users, user portal passwords, and voicemail PINs | 7.0.0 or earlier | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000166-NDM-000254`; NDM `SRG-APP-000167-NDM-000255`; NDM `SRG-APP-000168-NDM-000256`; NDM `SRG-APP-000169-NDM-000257` | GUI: Security > Password Policy > Password/PIN Policy (Minimum password length 15, all four character types, applied to Admin user, SIP users, and User passwords; PIN expiration All) |
| Core: Authentication | Empty admin password option | 7.0.0 or earlier | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000148-NDM-000346` | GUI: Security > Password Policy > Password/PIN Policy (keep the policy enabled, so that Allow empty admin password is not offered) |
| Core: Authentication | Password auditor for SIP passwords, user passwords, and voicemail PINs | 7.0.0 or earlier | EVVM-SM `SRG-NET-000343-VVSM-00101`; EVVM-EP `SRG-NET-000015-VVEP-00100` | GUI: Security > Password Policy > Password Auditor (Audit Now, and change every weak password) |
| Core: Authentication | Default SIP user password, default user password, and default voicemail PIN (voice#321 and 123123 unless changed) | 7.0.0 or earlier | EVVM-EP `SRG-NET-000015-VVEP-00100`; EVVM-SM `SRG-NET-000343-VVSM-00101` | GUI: Phone System > Setting > Option (Default Setting: Generated, or Specified with your own values) |
| Core: Authentication | Administrator PIN for provisioning phones and overriding schedules | 7.0.0 or earlier | EVVM-EP `SRG-NET-000015-VVEP-00100`; NDM `SRG-APP-000408-NDM-000314` | GUI: Phone System > Setting > Miscellaneous (PBX Setting: a strong Administrator PIN known only to administrators) |
| Core: Endpoint registration | Screening of incoming calls from unauthenticated sources | 7.0.0 or earlier | EVVM-SM `SRG-NET-000343-VVSM-00101`; EVVM-SM `SRG-NET-000343-VVSM-00102`; EVVM-SM `SRG-NET-000147-VVSM-00101` | GUI: System > Advanced > SIP (Security: leave Accept unauthenticated incoming call cleared) |
| Core: Endpoint registration | SIP password for each extension | 7.0.0 or earlier | EVVM-SM `SRG-NET-000343-VVSM-00101`; EVVM-SM `SRG-NET-000138-VVSM-00101`; EVVM-EP `SRG-NET-000400-VVEP-00033` | GUI: Extension > Extension > IP Extension (Device Setting, Advanced, SIP password: Generate) |
| Core: Endpoint registration | Phones assigned by MAC address and phone model | 7.0.0 or earlier | EVVM-SM `SRG-NET-000148-VVSM-00101`; EVVM-PM `SRG-VOIP-000230` | GUI: Phone System > Device > Phone (add each phone with its MAC address before assigning it to an extension) |
| Core: Endpoint registration | Auto-provisioning, with default configuration for phones that are not assigned | 7.0.0 or earlier | EVVM-SM `SRG-NET-000015-VVSM-00101`; EVVM-SM `SRG-NET-000148-VVSM-00101` | GUI: System > Advanced > Auto Provisioning (clear Not assigned phone after the initial setup) |
| Core: Endpoint registration | Phone auto discovery (SIPPnP multicast and DHCP) and backward provisioning of legacy FortiFone phones (TFTP and mDNS) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000015-VVSM-00101`; EVVM-SM `SRG-NET-000132-VVSM-00101` | GUI: System > Advanced > Auto Provisioning (Auto Discovery and Backward support of legacy FortiFone off when not used) |
| Core: Endpoint registration | Trusted hosts for extension registration in user privileges | 7.0.0 or earlier | EVVM-SM `SRG-NET-000147-VVSM-00101`; EVVM-SM `SRG-NET-000148-VVSM-00101` | GUI: Phone System > Profile > User Privilege (Advanced Setting, Trusted hosts type User defined, with the voice subnets) |
| Core: Endpoint registration | Extension registration intervals (30 minutes internal and 300 seconds external by default; SIP profile interval takes priority) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000338-VVSM-00101` | GUI: System > Advanced > SIP (Internal extension registration interval 180 minutes or less, and Registration interval in Phone System > Profile > SIP 10800 seconds or less) |
| Core: Endpoint registration | Verification of the SIP user agent against the configured phone type | 8.0 (Solution Guide) | EVVM-SM `SRG-NET-000148-VVSM-00101`; EVVM-SM `SRG-NET-000147-VVSM-00101` | `config system sip-setting`; `set verify-user-agent enable`; `end` |
| Core: Endpoint registration | Removal of phones that are not assigned to extensions (a sign of MAC address flooding) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000147-VVSM-00101`; EVVM-SM `SRG-NET-000362-VVSM-00101` | GUI: Dashboard > Status (System Information, Phones not assigned: remove them) |
| Core: Endpoint registration | Extensions that are not in use | 7.0.0 or earlier | EVVM-SM `SRG-NET-000004-VVSM-00101`; EVVM-SM `SRG-NET-000321-VVSM-00101` | GUI: Extension > Extension > IP Extension (clear Enabled on extensions that are not in use) |
| Core: Endpoint registration | SIP registration log (new, expired, and refreshed registrations) | 8.0.0 or earlier | EVVM-SM `SRG-NET-000506-VVSM-00010`; EVVM-SM `SRG-NET-000113-VVSM-00101` | GUI: Log & Report > Log Setting > Local (SIP Registration Log Status enabled, with a retention period) |
| Core: Trunks | SIP trunks to VoIP service providers (registration with password, authentication user name, and realm) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000343-VVSM-00102`; EVVM-SM `SRG-NET-000338-VVSM-00102`; EVVM-SM `SRG-NET-000371-VVSM-00101` | GUI: Trunk > VoIP > SIP (Registration with credentials, Transport protocol TLS where the provider supports it, and Registration interval 60 minutes or less) |
| Core: Trunks | Office peer trunks between FortiVoice systems (symmetric or asymmetric authentication) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000343-VVSM-00102` | GUI: Trunk > Office Peer > Office Peer (Peer Configuration, Authentication: Symmetric or Asymmetric) |
| Core: Trunks | PSTN, PRI, and analog trunks | 7.0.0 or earlier | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Core: Trunks | SIP profiles (UDP, TCP, or TLS transport, Secure RTP, codecs, DTMF, NAT, T.38, and intervals) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000371-VVSM-00101`; EVVM-SM `SRG-NET-000510-VVSM-00101`; EVVM-SM `SRG-NET-000230-VVSM-00101`; EVVM-SM `SRG-NET-000530-VVSM-00010`; EVVM-EP `SRG-NET-000371-VVEP-00037` | GUI: Phone System > Profile > SIP (Transport TLS only and Secure RTP on every profile used by phones and trunks) |
| Core: Trunks | SIP transport ports, RTP port range, and RTP timeouts | 7.0.0 or earlier | EVVM-SM `SRG-NET-000132-VVSM-00101`; EVVM-SM `SRG-NET-000213-VVSM-00101` | GUI: System > Advanced > SIP (ports approved in the PPSM CAL; RTP Timeout and Hold timeout not 0) |
| Core: Trunks | External access hostname and ports for remote extensions and FortiFone Softclient | 7.0.0 or earlier | EVVM-SM `SRG-NET-000132-VVSM-00101` | GUI: System > Advanced > External Access (only the approved external ports; prefer a VPN for remote users) |
| Core: Trunks | SIP session helper (NAT of SIP messages) and internal network type | 7.0.0 or earlier | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | GUI: System > Advanced > SIP (Advanced Setting, SIP session helper) |
| Core: Call privileges | User privileges (call forward, call restrictions, recording, barging, hot desking, user portal, directory, conferences, paging, and outgoing rules) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000321-VVSM-00101`; EVVM-SM `SRG-NET-000322-VVSM-00101` | GUI: Phone System > Profile > User Privilege (the narrowest privilege for each group of extensions) |
| Core: Call privileges | Call restrictions with account codes and personal codes (international, long distance, local, and internal) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000321-VVSM-00101` | GUI: Security > User Privilege > Account Code (and Call Restriction in each user privilege) |
| Core: Call privileges | System prohibited prefixes (900 blocked by default) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000321-VVSM-00101` | GUI: Phone System > Setting > Option (Number Management, System prohibited prefix) |
| Core: Call privileges | Schedules (business hours and holidays) used by dial plans and auto attendants | 7.0.0 or earlier | EVVM-SM `SRG-NET-000315-VVSM-00101` | GUI: Phone System > Profile > Schedule (route calls outside operational hours according to local policy) |
| Core: Call privileges | Hot desking (a guest extension logs in to a host phone) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000018-VVSM-00102`; EVVM-SM `SRG-NET-000018-VVSM-00101` | GUI: Phone System > Profile > User Privilege (Hot Desking, Enable login and Enable hosting off in the default privileges and on only in privileges for users who need it, with Automatic logout hours set) |
| Core: Call privileges | Call barging and monitoring (Allow barging and Allow being barged) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000321-VVSM-00101` | GUI: Phone System > Profile > User Privilege (Monitor/Recording: barging only for supervisors who need it) |
| Core: Call privileges | Blocked numbers and the system block list | 7.0.0 or earlier | EVVM-SM `SRG-NET-000362-VVSM-00101` | GUI: Security > Blocked Number |
| Core: Call privileges | Vertical service codes (call bridge (DISA) and the phone reset and configuration codes \*15 to \*18) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000131-VVSM-00101`; EVVM-SM `SRG-NET-000015-VVSM-00101` | GUI: Call Feature > Feature Code > Vertical Service Code (disable the codes that are not used) |
| Core: Call privileges | Call bridge (DISA) for outgoing calls from an auto attendant | 7.0.0 or earlier | EVVM-SM `SRG-NET-000321-VVSM-00101`; EVVM-SM `SRG-NET-000131-VVSM-00101` | GUI: Call Feature > Auto Attendant > Auto Attendant (Advanced, Call bridge (DISA) off, or with an Account code) |
| Core: Intrusion protection | Intrusion detection with exempt IP addresses and an initial block period | 7.0.0 or earlier | EVVM-SM `SRG-NET-000147-VVSM-00101`; EVVM-SM `SRG-NET-000362-VVSM-00101`; NDM `SRG-APP-000435-NDM-000315` | GUI: Security > Intrusion Detection > Setting (Status Enable, not Monitor Only; exempt only trusted addresses in Security > Intrusion Detection > Exempt IP) |
| Core: Intrusion protection | Automatic blocking of SIP devices after massive SIP authentication failures | 7.0.0 or earlier | EVVM-SM `SRG-NET-000147-VVSM-00101`; EVVM-SM `SRG-NET-000362-VVSM-00101` | `config security sip-authentication-failure`; `set threshold <ATTEMPTS>`; `set interval <SECONDS>`; `set max-notification <NUMBER>`; `end` (review Monitor > Security > Blocked IP) |
| Core: Logging | Local logs (System, Generic, Voice, Fax, and other logs) with log level, file size, rotation, and disk-full action | 7.0.0 or earlier | NDM `SRG-APP-000357-NDM-000293`; NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000027-NDM-000209`; NDM `SRG-APP-000028-NDM-000210`; NDM `SRG-APP-000029-NDM-000211`; EVVM-SM `SRG-NET-000509-VVSM-00010`; NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000100-NDM-000230`; NDM `SRG-APP-000505-NDM-000322` | GUI: Log & Report > Log Setting > Local (System with Configuration change and Admin activity, Generic with Activity, and Voice) |
| Core: Logging | Remote logging to up to three syslog servers or FortiAnalyzer units | 7.0.0 or earlier | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350`; EVVM-SM `SRG-NET-000334-VVSM-00101` | GUI: Log & Report > Log Setting > Remote (two servers, with the System, Generic, and Voice logs) |
| Core: Logging | Protection of logs and call records through admin profiles | 7.0.0 or earlier | NDM `SRG-APP-000119-NDM-000236`; NDM `SRG-APP-000120-NDM-000237`; EVVM-SM `SRG-NET-000098-VVSM-00101`; EVVM-SM `SRG-NET-000099-VVSM-00101`; EVVM-SM `SRG-NET-000100-VVSM-00101` | GUI: System > Administrator > Admin Profile (Read Only or None for the log, call history, and recording areas for administrators who do not manage them) |
| Core: Call records | Call detail records with call flow (direction, disposition, departments, and recordings) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000074-VVSM-00101`; EVVM-SM `SRG-NET-000075-VVSM-00101`; EVVM-SM `SRG-NET-000076-VVSM-00101`; EVVM-SM `SRG-NET-000077-VVSM-00101`; EVVM-SM `SRG-NET-000078-VVSM-00101`; EVVM-SM `SRG-NET-000079-VVSM-00101`; EVVM-SM `SRG-NET-000113-VVSM-00101` | GUI: Monitor > Call History > Call Detail Record |
| Core: Call records | CDR submission to a remote RESTful database server | 7.0.0 or earlier | EVVM-SM `SRG-NET-000334-VVSM-00101`; EVVM-SM `SRG-NET-000273-VVSM-00101` | GUI: Log & Report > CDR > Submit CDR (HTTPS with SSL verification and Password or OAuth authentication; a CDR template and filter that leave out data not needed) |
| Core: Call records | SMDR output to third-party devices | 7.0.0 or earlier | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | GUI: Log & Report > SMDR > SMDR (Enabled cleared when not used, otherwise Trusted hosts set) |
| Core: Call records | Call report profiles and scheduled reports by email | 7.0.0 or earlier | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Core: Alerts | Alert email recipients and categories (critical events, disk full, HA, trunk saturation, trunk connectivity, and security audit) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000088-VVSM-00101`; NDM `SRG-APP-000360-NDM-000295`; NDM `SRG-APP-000795-NDM-000130` | GUI: Log & Report > Alert > Configuration (the ISSO and SA addresses; Critical events, Disk is full, HA events, and Massive SIP authentication failure in Log & Report > Alert > Category) |
| Core: Alerts | Mail server settings for alerts and notifications (SMTP relay with SMTPS) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000530-VVSM-00010` | GUI: System > Configuration > Mail Setting (Use SMTPs) |
| Core: Monitoring | SNMP v1 and v2c communities and SNMP v3 users for queries and traps | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000142-NDM-000245` | GUI: System > Configuration > SNMP (SNMP v3 only, Security level Authentication, privacy, with SHA1; no v1 or v2c communities) |
| Core: Time | System time synchronized with up to 10 NTP servers | 7.0.0 or earlier | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000374-NDM-000299`; EVVM-SM `SRG-NET-000512-VVSM-00101` | GUI: System > Configuration > Time (Synchronize with NTP Server, with two DoD NTP servers) |
| Core: Time | NTP server given to phones through auto-provisioning | 7.0.0 or earlier | EVVM-SM `SRG-NET-000512-VVSM-00101` | GUI: System > Advanced > Auto Provisioning (Server Setting for Phone Configuration, NTP server) |
| Core: Network | DNS servers | 7.0.0 or earlier | EVVM-SM `SRG-NET-000018-VVSM-00103` | GUI: System > Network > DNS (the DNS servers assigned to the VVoIP system) |
| Core: Network | VLAN subinterfaces on the FortiVoice unit | 7.0.0 or earlier | EVVM-SM `SRG-NET-000520-VVSM-00102`; EVVM-SM `SRG-NET-000520-VVSM-00101` | GUI: System > Network > Network (a VLAN interface on the voice VLAN for signaling and media) |
| Core: Network | DHCP server for phones | 7.0.0 or earlier | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | GUI: System > Network > DHCP |
| Core: Network | Capture of voice and fax packets | 7.0.0 or earlier | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Core: Phones | Voice and data VLAN tagging in phone profiles (manual or LLDP) | 7.0.0 or earlier | EVVM-EP `SRG-NET-000018-VVEP-00107`; EVVM-EP `SRG-NET-000029-VVEP-00010`; EVVM-EP `SRG-NET-000018-VVEP-00101`; EVVM-SM `SRG-NET-000520-VVSM-00101` | GUI: Phone System > Profile > Phone (VLAN: Enable VLAN tagging for voice with the voice VLAN ID, and Enable VLAN tagging for data for the PC port) |
| Core: Phones | Phone admin password for advanced settings on the phone | 7.0.0 or earlier | EVVM-EP `SRG-NET-000015-VVEP-00100`; EVVM-EP `SRG-NET-000015-VVEP-00101` | GUI: Phone System > Profile > Phone (Phone Password, Admin password: a strong, non-default password) |
| Core: Phones | Keypad locking on FON-x80/x80B and W80B phones | 8.0.0 or earlier | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Core: Phones | Auto answer on the phone of an extension | 7.0.0 or earlier | EVVM-EP `SRG-NET-000512-VVEP-00103` | GUI: Extension > Extension > IP Extension (Device Setting, Advanced, Auto answer disabled) |
| Core: Phones | Delivery of phone configuration files (provisioning protocol and TFTP service) | 7.0.0 or earlier | EVVM-SM `SRG-NET-000371-VVSM-00101`; EVVM-SM `SRG-NET-000131-VVSM-00101` | GUI: System > Advanced > Service (TFTP port disabled; Provisioning protocol HTTPS in System > Advanced > Auto Provisioning) |
| Core: Phones | FortiFone firmware management | 7.0.0 or earlier | EVVM-EP `SRG-NET-000512-VVEP-00101` | GUI: Managed System > Firmware > FortiFone Firmware (vendor-supported firmware on every phone) |
| Core: Phones | Phone maintenance (configuration updates and reboots) | 7.0.0 or earlier | EVVM-EP `SRG-NET-000512-VVEP-00102` | GUI: System > Maintenance > Phone Maintenance |
| Core: Phones | Remote extensions and FortiFone Softclient for desktop and mobile | 7.0.0 or earlier | EVVM-PM `SRG-VOIP-000280`; EVVM-PM `SRG-VOIP-000270`; EVVM-EP `SRG-NET-000138-VVEP-00029` | GUI: Extension > Extension > IP Extension (softclient licenses only for users covered by the AO approval) |
| Core: Conferencing | Conference calls with a list of participants and kick out | 7.0.0 or earlier | EVVM-SM `SRG-NET-000353-VVSM-00101` | GUI: Monitor > Phone System > Conference |
| Core: Recording | Call recording (personal and system) and archiving to FTP or SFTP | 7.0.0 or earlier | EVVM-SM `SRG-NET-000321-VVSM-00101` | GUI: Call Feature > Call Recording > Policy (recording only where policy allows; archive over SFTP in Call Feature > Call Recording > Archive) |
| Core: Emergency calling | Emergency zone profiles (caller ID, DID callback, location, and alert email) | 7.0.0 or earlier | EVVM-PM `SRG-VOIP-000400`; EVVM-PM `SRG-VOIP-000410`; EVVM-PM `SRG-VOIP-000420` | GUI: Phone System > Profile > Emergency Zone |
| Core: Emergency calling | Location, contact, and emergency information of the FortiVoice system | 7.0.0 or earlier | EVVM-PM `SRG-VOIP-000400`; EVVM-PM `SRG-VOIP-000430` | GUI: Phone System > Setting > Location |
| Core: Survivability | Local survivable gateways and survivability branches | 7.0.0 or earlier | EVVM-PM `SRG-VOIP-000300` | GUI: Managed System > Survivability |
| Core: High availability | Active-passive HA with configuration and data synchronization | 7.0.0 or earlier | EVVM-SM `SRG-NET-000236-VVSM-00101`; EVVM-SM `SRG-NET-000235-VVSM-00101` | GUI: System > High Availability > Configuration (heartbeat on a dedicated link; `diagnose system ha sync` resynchronizes the configuration) |
| Core: Firmware | FortiVoice firmware upgrades | 7.0.0 or earlier | NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-000131-NDM-000243`; NDM `SRG-APP-000378-NDM-000302` | GUI: Dashboard > Status (System Information, Firmware version, Update, after checking the image checksum) |
| Core: Backup | Configuration and user data backups (manual, and scheduled to the local disk or an FTP or SFTP server) | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340`; EVVM-SM `SRG-NET-000236-VVSM-00101` | GUI: System > Maintenance > Configuration (Scheduled Backup with Remote backup over SFTP) |
| Core: Storage | Call data storage on the local disk or a NAS server (NFS or iSCSI) | 7.0.0 or earlier | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | GUI: System > Configuration > Storage |
| Core: Security Fabric | Membership in the Security Fabric of a FortiGate | 7.0.0 or earlier | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | GUI: System > Configuration > Security Fabric (Enabled cleared when not used) |
| Core: Certificates | CA certificates, certificate revocation lists, and OCSP server certificates | 7.0.0 or earlier | NDM `SRG-APP-000910-NDM-000300`; NDM `SRG-APP-000875-NDM-000280`; NDM `SRG-APP-000175-NDM-000262`; EVVM-SM `SRG-NET-000580-VVSM-00010`; EVVM-SM `SRG-NET-000355-VVSM-00010` | GUI: System > Certificate > CA Certificate (DoD root and intermediate CAs only; OCSP server certificates in System > Certificate > Remote) |
| Core: Certificates | APNs and VoIP services certificates for FortiFone Softclient on iPhones | 7.0.0 or earlier | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | GUI: System > Certificate > APNS Push Certificate |
| Administrator accounts | Call History option in admin profiles | 7.0.0 and later | NDM `SRG-APP-000033-NDM-000212`; EVVM-SM `SRG-NET-000098-VVSM-00101` | GUI: System > Administrator > Admin Profile (Call History: None or Read Only for administrators who do not need call records) |
| Emergency calling | Dynamic emergency zones (E911 location identified by IP subnet when a phone moves) | 7.0.0 and later | EVVM-PM `SRG-VOIP-000410`; EVVM-PM `SRG-VOIP-000420` | GUI: Phone System > Profile > Emergency Zone (Dynamic Network Match for each subnet) |
| Platform | FortiFone FON-280B phone | 7.0.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Survivability | FortiVoice FXO and PRI gateways in the local survivable gateway solution | 7.0.0 and later | EVVM-PM `SRG-VOIP-000300` | GUI: Managed System > Survivability |
| Management access | Improved web CLI console | 7.0.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Platform | More managed gateways (80 on FVE-2000F and FVE-VM-2000, 150 on FVE-5000F and FVE-VM-5000) | 7.0.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Call features | Shared line appearance (SLA) groups | 7.0.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | GUI: Extension > Group > SLA Group (no SLA groups unless needed) |
| Messaging | SMS to and from cellular phone numbers through FortiFone Softclient | 7.0.0+; 7.2.3+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — (off unless SMS is enabled on an extension) |
| Authentication | Single sign-on to the admin portal and user portal through a SAML identity provider such as FortiAuthenticator | 7.0.0 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000149-NDM-000247`; EVVM-SM `SRG-NET-000138-VVSM-00102` | GUI: Phone System > Single Sign On > Settings (an identity provider that enforces DoD PKI; administrators with Authentication type Single Sign On in System > Administrator > Administrator) |
| Platform | Yealink W60B DECT IP base station | 7.0.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Softclient | Token-based connection to the Apple Push Notification service | 7.0.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — (the token-based connection is the default) |
| Authentication | Two-factor authentication for the admin portal and user portal (token by email or SMS from FortiAuthenticator) | 7.0.0 and later | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000825-NDM-000180`; NDM `SRG-APP-000149-NDM-000247` | GUI: Phone System > Single Sign On > Settings (two-factor authentication set up on FortiAuthenticator) |
| Audio | MP3 audio files for greetings, announcements, and music on hold | 7.0.1 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Call center | Retention time and maximum records for call center reports | 7.0.2 and later | NDM `SRG-APP-000357-NDM-000293` | GUI: Phone System > Setting > Miscellaneous |
| Call privileges | Call forwarding without the voicemail PIN (Call forwarding PIN toggle) | 7.0.2 and later | EVVM-SM `SRG-NET-000321-VVSM-00101` | GUI: Phone System > Profile > User Privilege (Advanced Setting, Call forwarding PIN enabled) |
| Platform | Multiplatform phone (MPP) firmware for Cisco 78xx and 88xx phones | 7.0.2 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Survivability | Rejection of paging from other branches in the local survivable gateway solution | 7.0.2 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Survivability | Email settings and emergency zones pushed to local survivable gateway branches | 7.0.2 and later | EVVM-PM `SRG-VOIP-000400`; EVVM-PM `SRG-VOIP-000300` | GUI: Managed System > Survivability > Survivability Branch |
| Platform | FortiFone FON-580B phone | 7.0.2 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Platform | FortiVoice FVE-50G2 appliance | 7.0.2 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Platform | FortiVoice gateways FVG-GO04 and FVG-GS04 | 7.0.2 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Survivability | FXS ports on FVE-20E2, FVE-50E6, and FVE-50G2 in the fully managed LSG mode | 7.0.2 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Phones | Phone maintenance job statuses and the last phone configuration update | 7.0.2 and later | EVVM-EP `SRG-NET-000512-VVEP-00102` | GUI: System > Maintenance > Phone Maintenance Job |
| Phones | Registration retry interval for FON-x80/x80B phones | 7.0.2 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Logging | Remote syslog or FortiAnalyzer logging for FVG-GS16 gateways | 7.0.2 and later | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350` | — (set on the gateway, not in the phone system Administration Guide) |
| Denial of service | Web service limits (concurrent requests, active admin portal sessions, request rate, and repeat offenders) | 7.0.2 and later | NDM `SRG-APP-000435-NDM-000315`; EVVM-SM `SRG-NET-000362-VVSM-00101`; NDM `SRG-APP-000001-NDM-000200`; EVVM-SM `SRG-NET-000053-VVSM-00101` | GUI: Security > Rate Limit > Web Service (Maximum Login Session, Admin Portal: the organization-defined limit, never 0; Repeat Offender Control on) |
| Platform | Yealink CP925 and CP965 conference phones | 7.0.2 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Platform | Yealink W70B phone | 7.0.2 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Call records | Department administrators limited to the call detail records of their departments | 7.0.3 and later | EVVM-SM `SRG-NET-000098-VVSM-00101`; NDM `SRG-APP-000033-NDM-000212` | GUI: System > Administrator > Administrator (Department only, with Departments) |
| Managed systems | Batch configuration jobs for managed gateways and survivability branches | 7.0.3+; 7.2.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Phones | Call busy tone on FON-x80/x80B phones | 7.0.3+; 7.2.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Call center | Callback prefix for call queues | 7.0.3 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Managed systems | Default notification email templates on gateways | 7.0.3 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Platform | FortiVoice gateway FVG-GS24 | 7.0.3 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Auto attendant | Voicemail by dialing star and an extension number during the auto attendant greeting | 7.0.3 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Logging | Log entry when local call recordings are deleted at the disk quota | 7.0.3 and later | NDM `SRG-APP-000357-NDM-000293`; NDM `SRG-APP-000095-NDM-000225` | GUI: Log & Report > Log Setting > Local (System logs) |
| Hotel | Opera Cloud support for hotel management | 7.0.3 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Call center | Feature codes \*69 and \*70 to pause and unpause queue agents | 7.0.3 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | GUI: Call Feature > Feature Code > Vertical Service Code (disable the codes when unused) |
| Recording | Recorder warning tone for recorded calls | 7.0.3+; 7.2.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — (disabled by default) |
| Authentication | Token dialog in FortiFone Softclient for mobile for administrators with RADIUS authentication | 7.0.3 and later | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000825-NDM-000180` | GUI: Phone System > Profile > RADIUS |
| Call center | Retry interval and other settings for the remote call center data service | 7.0.5+; 7.2.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Logging | Logs for failures of the call center data service | 7.0.5+; 7.2.0+ | NDM `SRG-APP-000095-NDM-000225` | GUI: Log & Report > Log Setting > Local |
| Authentication | RADIUS authentication for extension web access (user portal, FortiFone Softclient for desktop and mobile) | 7.0.5+; 7.2.0+ | EVVM-SM `SRG-NET-000138-VVSM-00102`; EVVM-SM `SRG-NET-000138-VVSM-00101`; EVVM-EP `SRG-NET-000140-VVEP-00010` | GUI: Extension > Extension > IP Extension (User Setting, Web Access, Authentication type RADIUS, with a RADIUS profile) |
| Platform | FortiFone FON-W80B portable WiFi phone | 7.0.6+; 7.2.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Languages | Portuguese (Portugal) language | 7.0.6+; 7.2.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Phones | User, target firmware, and job history columns for phone firmware and maintenance jobs | 7.0.6 and later | EVVM-EP `SRG-NET-000512-VVEP-00101` | GUI: System > Maintenance > Phone Maintenance Job |
| Call center | On-demand backup of the call center data service | 7.0.6+; 7.2.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Call center | Not-available reasons and times in the agent summary report | 7.0.7+; 7.2.1+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Trunks | Custom parameters in the From header of SIP trunks | 7.0.7+; 7.2.1+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — (the release notes name the CLI option from-header-parameters but not its configuration path) |
| Call center | 300 call center reports on FVE-VM-10000 and above | 7.0.8+; 7.2.2+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Call records | Four CDR database servers on FVE-VM-10000 and above | 7.0.8+; 7.2.2+ | EVVM-SM `SRG-NET-000334-VVSM-00101` | GUI: Log & Report > CDR > Submit CDR |
| Softclient | Switching active calls between devices | 7.2.0 and later | EVVM-SM `SRG-NET-000321-VVSM-00101` | GUI: Phone System > Profile > User Privilege (Switch calls between devices only where approved) |
| Authentication | SSO authentication type for extension web access to the user portal | 7.2.0 and later | EVVM-SM `SRG-NET-000138-VVSM-00102`; EVVM-EP `SRG-NET-000140-VVEP-00010` | GUI: Extension > Extension > IP Extension (User Setting, Web Access, Authentication type SSO, with an SSO profile) |
| Call privileges | Shared line appearance settings in user privileges and extensions | 7.2.0 and later | EVVM-SM `SRG-NET-000321-VVSM-00101` | GUI: Phone System > Profile > User Privilege (Shared Line only where needed) |
| Languages | Arabic language for FON-x80/x80B phones | 7.2.1 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Integrations | Call event submission to a customer relationship management system | 7.2.2 and later | EVVM-SM `SRG-NET-000273-VVSM-00101` | GUI: Log & Report > Call Event > Server (HTTPS to approved servers only, and a policy in Log & Report > Call Event > Policy that sends only the events needed) |
| Endpoints | Decline All for extensions with several endpoints | 7.2.2 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Call privileges | Hot desking guest as the default, primary, or secondary account | 7.2.2 and later | EVVM-SM `SRG-NET-000018-VVSM-00101` | GUI: Phone System > Profile > User Privilege (Hot Desking, with guest as) |
| Emergency calling | PIDF-LO location objects on trunks for emergency calls | 7.2.2 and later | EVVM-PM `SRG-VOIP-000410`; EVVM-PM `SRG-VOIP-000420` | GUI: Phone System > Profile > Emergency Zone (PIDF-LO, and PIDF-LO compatible on the SIP trunk in Trunk > VoIP > SIP, where the provider supports it) |
| Call records | Call event filters for CDR submission (Basic, Call, IVR action, and Other) | 7.2.3 and later | EVVM-SM `SRG-NET-000113-VVSM-00101` | GUI: Log & Report > CDR > Submit CDR (Events: the filters required by local policy) |
| Messaging | Chat between extensions through FortiFone Softclient | 7.2.3 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Firmware | Firmware store (phone firmware from the Fortinet cloud server, with FortiCare Premium) | 7.2.3 and later | EVVM-EP `SRG-NET-000512-VVEP-00101` | GUI: Managed System > Firmware > FortiFone Firmware |
| Platform | FortiFone FON-780B executive video IP phone | 7.2.3 and later | EVVM-PM `SRG-VOIP-000100`; EVVM-PM `SRG-VOIP-000110` | — (camera and microphone use are set by policy; no FortiVoice setting) |
| Logging | Log collection from FortiFone Softclient for desktop | 7.2.3 and later | EVVM-EP `SRG-NET-000334-VVEP-00010` | GUI: Monitor > Extension & Device > Soft FortiFone (collect the logs; retention under Phone Log in Phone System > Setting > Miscellaneous) |
| Transcription | Voicemail transcription by a third-party AI platform (OpenAI or Google Cloud) | 7.2.3 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | GUI: Phone System > Profile > User Privilege (Voicemail, Transcribe off; the audio leaves the enclave) |
| Call center | Search and CSV download of call queues | 7.2.4+; 7.4.0+; 8.0.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Transcription | IVR ticket numbers in call recording transcriptions | 7.2.4+; 8.0.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Conferencing | Conferences kept active after the organizer leaves (Keep session active) | 7.2.4+; 7.4.0+; 8.0.0+ | EVVM-SM `SRG-NET-000213-VVSM-00101` | GUI: Call Feature > Conferencing > User Conferencing (Keep session active off where policy requires a conference to end with its organizer; the same in Admin Conferencing) |
| Languages | Dutch language for phones, softclients, portals, and prompts | 7.2.4+; 7.4.1+; 8.0.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Call center | Up to 20 IVR actions and natural reading of dates | 7.2.4+; 7.4.0+; 8.0.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Certificates | Additional CA certificates on FVE-100F and FVE-200F | 7.2.5 and later | NDM `SRG-APP-000910-NDM-000300` | GUI: System > Certificate > CA Certificate (keep only approved trust anchors) |
| Firmware | Manual upload of FON-780B firmware from the Fortinet Support website | 7.4.0 and later | EVVM-EP `SRG-NET-000512-VVEP-00101` | GUI: Managed System > Firmware > FortiFone Firmware |
| Firmware | Gateway and LSG firmware upgrades from the cloud image server | 7.4.0 and later | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340` | GUI: Managed System > Firmware > FortiVoice Firmware |
| Softclient | Selection of an outgoing number (caller ID) by softclient users | 7.4.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Transcription | Transcription of call recordings in several languages | 7.4.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | GUI: Phone System > Audio > Speech to Text (disabled by default; enable only if approved) |
| Authentication | Google Workspace secure LDAP certificates in LDAP profiles | 7.4.1+; 8.0.0+ | NDM `SRG-APP-000516-NDM-000336`; EVVM-SM `SRG-NET-000580-VVSM-00010` | GUI: Phone System > LDAP > LDAP Profile (Secure Connection) |
| Call routing | Outbound dial plans that start with a pound sign | 7.4.1+; 8.0.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Softclient | Sharing of account pictures or avatars for each phone type | 7.4.1+; 8.0.0+ | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Call privileges | Role-based access control (RBAC) roles for call access, assigned to user privileges and extensions | 7.4.2 and later | EVVM-SM `SRG-NET-000321-VVSM-00101`; EVVM-SM `SRG-NET-000322-VVSM-00101` | GUI: Security > Call Access > Role Base Access Control (from the 7.4.2 release notes; not in the 8.0.0 Administration Guide) |
| Audio | AI text-to-speech audio prompts | 8.0.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Call center | Missed Calls column in the call center console | 8.0.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Phones | Call Forwarded notification on FortiFone phone screens | 8.0.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Trunks | FortiCall trunks from Volli (North American calling with E911 DIDs, managed in the FortiVoice Cloud portal) | 8.0.0 and later | EVVM-PM `SRG-VOIP-000390`; EVVM-PM `SRG-VOIP-000600` | — (provider compliance with STIR/SHAKEN and approval of the commercial connection are checked outside FortiVoice) |
| Integrations | FortiLink deployment and auto-provisioning of FortiFone endpoints from FortiGate | 8.0.0 and later | EVVM-EP `SRG-NET-000015-VVEP-00102`; EVVM-PM `SRG-VOIP-000230` | — (configured on FortiGate) |
| Licensing | Chat, conferencing, Microsoft Teams integration, and Enhanced Call Center included in the FortiVoice license | 8.0.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |
| Mass notifications | Mass Notifications (audio and text alerts to devices and users) | 8.0.0 and later | No direct requirement; if unused, disable (EVVM-SM `SRG-NET-000131-VVSM-00101`) | — |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current SRG releases:

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/22-fortivoice-feature-version-and-srg-map-requirements.csv) (150 rows).

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| EVVM-SM | `SRG-NET-000004-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must automatically disable user accounts after a 35-day period of account inactivity. |
| EVVM-SM | `SRG-NET-000015-VVSM-00101` | CAT I | The Enterprise Voice, Video, and Messaging Session Manager must disable (prevent) auto-registration of Voice Video Endpoints. |
| EVVM-SM | `SRG-NET-000018-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to only enable the extension mobility feature for endpoints on a per user basis. |
| EVVM-SM | `SRG-NET-000018-VVSM-00102` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to globally disable the extension mobility feature for endpoints. |
| EVVM-SM | `SRG-NET-000018-VVSM-00103` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to use DNS servers assigned to support the VVoIP system. |
| EVVM-SM | `SRG-NET-000041-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must display the Standard Mandatory DOD Notice and Consent Banner before granting access to management sessions. |
| EVVM-SM | `SRG-NET-000042-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must retain the Standard Mandatory DOD Notice and Consent Banner on the screen for management sessions until admins acknowledge the usage conditions and take explicit actions to log on for further access. |
| EVVM-SM | `SRG-NET-000053-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must limit the number of concurrent management sessions to an organizationally defined limit. |
| EVVM-SM | `SRG-NET-000062-VVSM-00010` | CAT I | The Enterprise Voice, Video, and Messaging Session Manager must use TLS 1.2 or greater to protect the confidentiality of remote access. |
| EVVM-SM | `SRG-NET-000074-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must produce session (call) records containing the type of session connection. |
| EVVM-SM | `SRG-NET-000075-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must produce session (call) records containing timestamps (date and time) for all session connections. |
| EVVM-SM | `SRG-NET-000076-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must produce session (call) records containing where (location) the connection originated. |
| EVVM-SM | `SRG-NET-000077-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must produce session (call) records containing the identity of the initiator of the call. |
| EVVM-SM | `SRG-NET-000078-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must produce session (call) records containing the outcome (status) of the connection. |
| EVVM-SM | `SRG-NET-000079-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must produce session (call) records containing the identity of the users and identifiers associated with the session. |
| EVVM-SM | `SRG-NET-000088-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must alert the information system security officer (ISSO) and system administrator (SA) (at a minimum) in the event of a session (call) record system failure. |
| EVVM-SM | `SRG-NET-000098-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must protect session (call) records from unauthorized read access. |
| EVVM-SM | `SRG-NET-000099-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must protect session (call) records from unauthorized modification. |
| EVVM-SM | `SRG-NET-000100-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must protect session (call) records from unauthorized deletion. |
| EVVM-SM | `SRG-NET-000113-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must produce session (call) records for events determined to be significant and relevant by local policy. |
| EVVM-SM | `SRG-NET-000131-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to disable nonessential capabilities. |
| EVVM-SM | `SRG-NET-000132-VVSM-00101` | CAT I | The Enterprise Voice, Video, and Messaging Session Manager must only use ports, protocols, and services allowed per the Ports, Protocols, and Services Management (PPSM) Category Assurance List (CAL) and Vulnerability Assessments (VAs). |
| EVVM-SM | `SRG-NET-000138-VVSM-00101` | CAT I | The Enterprise Voice, Video, and Messaging Session Manager must be configured to uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| EVVM-SM | `SRG-NET-000138-VVSM-00102` | CAT I | The Enterprise Voice, Video, and Messaging Session Manager must be configured to use an organizational-level user account management system. |
| EVVM-SM | `SRG-NET-000147-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to implement attack-resistant mechanisms for Voice Video Endpoint registration. |
| EVVM-SM | `SRG-NET-000148-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to uniquely identify each Voice Video Endpoint device before registration. |
| EVVM-SM | `SRG-NET-000213-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to terminate all network connections associated with a communications session at the end of the session. |
| EVVM-SM | `SRG-NET-000225-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager supporting Command and Control (C2) communications must associate multilevel precedence and preemption (MLPP) attributes when exchanged between unified capabilities (UC) systems. |
| EVVM-SM | `SRG-NET-000226-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager supporting Command and Control (C2) communications must validate the integrity of transmitted multilevel precedence and preemption (MLPP) attributes. |
| EVVM-SM | `SRG-NET-000230-VVSM-00101` | CAT I | The Enterprise Voice, Video, and Messaging Session Manager must be configured to use FIPS-validated SHA-2 or higher to protect the authenticity of communications sessions. |
| EVVM-SM | `SRG-NET-000235-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must fail to a secure state if system initialization fails, shutdown fails, or aborts fail. |
| EVVM-SM | `SRG-NET-000236-VVSM-00101` | CAT II | In the event of a system failure, Enterprise Voice, Video, and Messaging Session Managers must be configured to preserve any information necessary to determine cause of failure and any information necessary to return to operations with least disruption to mission processes. |
| EVVM-SM | `SRG-NET-000273-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to generate session (call) records that provide information necessary for corrective actions without revealing personally identifiable information or sensitive information. |
| EVVM-SM | `SRG-NET-000315-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to restrict Enterprise Voice, Video, and Messaging Session Manager access outside of operational hours. |
| EVVM-SM | `SRG-NET-000321-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to enforce changes to privileges of Voice Video Endpoint user access. |
| EVVM-SM | `SRG-NET-000322-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to enforce changes to privileges of Voice Video Endpoint device access. |
| EVVM-SM | `SRG-NET-000334-VVSM-00101` | CAT I | The Enterprise Voice, Video, and Messaging Session Manager must be configured to offload session (call) records to a central log server. |
| EVVM-SM | `SRG-NET-000338-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to require Voice Video Endpoints to re-register at least every three hours. |
| EVVM-SM | `SRG-NET-000338-VVSM-00102` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to require Voice Video peers to re-register (reauthenticate) at least every hour. |
| EVVM-SM | `SRG-NET-000343-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to authenticate each Voice Video Endpoint device before registration. |
| EVVM-SM | `SRG-NET-000343-VVSM-00102` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to authenticate each Voice Video peer (trunk) before registration. |
| EVVM-SM | `SRG-NET-000353-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to provide an indication of current participants in all calls, meetings, and conferences. |
| EVVM-SM | `SRG-NET-000354-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager supporting Command and Control (C2) communications must associate multilevel precedence and preemption (MLPP) attributes when exchanged between unified capabilities (UC) system components. |
| EVVM-SM | `SRG-NET-000355-VVSM-00010` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must only allow the use of DOD-approved PKI certificate authorities when using PKI. |
| EVVM-SM | `SRG-NET-000362-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to protect against or limit the effects of all types of denial-of-service (DoS) attacks by employing organizationally defined security safeguards. |
| EVVM-SM | `SRG-NET-000363-VVSM-00019` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to limit and reserve bandwidth based on priority of the traffic type. |
| EVVM-SM | `SRG-NET-000371-VVSM-00101` | CAT I | The Enterprise Voice, Video, and Messaging Session Manager must be configured to protect the confidentiality and integrity of transmitted configuration files, signaling, and media streams. |
| EVVM-SM | `SRG-NET-000395-VVSM-00010` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager, when using locally stored user accounts, must automatically lock the account until the locked account is released by an administrator when three unsuccessful logon attempts in 15 minutes are exceeded. |
| EVVM-SM | `SRG-NET-000506-VVSM-00010` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must generate session (call) records when concurrent logons from multiple endpoints occur. |
| EVVM-SM | `SRG-NET-000509-VVSM-00010` | CAT II | When using locally stored user accounts, the Enterprise Voice, Video, and Messaging Session Manager must generate audit records for all account creations, modifications, disabling, and termination events. |
| EVVM-SM | `SRG-NET-000510-VVSM-00101` | CAT I | The Enterprise Voice, Video, and Messaging Session Manager must implement NIST FIPS-validated cryptography for communications sessions. |
| EVVM-SM | `SRG-NET-000512-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to use the organization authoritative time source (NTP) to maintain system time. |
| EVVM-SM | `SRG-NET-000512-VVSM-00130` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured in accordance with the security configuration settings based on DOD security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. |
| EVVM-SM | `SRG-NET-000520-VVSM-00101` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to apply 802.1Q VLAN tags to signaling and media traffic. |
| EVVM-SM | `SRG-NET-000520-VVSM-00102` | CAT II | The Enterprise Voice, Video, and Messaging Session Manager must be configured to use a voice or video VLAN, separate from all other VLANs. |
| EVVM-SM | `SRG-NET-000522-VVSM-00010` | CAT II | When using locally stored user accounts, the Enterprise Voice, Video, and Messaging Session Manager must store only cryptographic representations of passwords. |
| EVVM-SM | `SRG-NET-000530-VVSM-00010` | CAT I | The Enterprise Voice, Video, and Messaging Session Manager must be configured to use only TLS 1.2 or greater for all TLS and SSL communications. |
| EVVM-SM | `SRG-NET-000580-VVSM-00010` | CAT II | When using PKI, the Enterprise Voice, Video, and Messaging Session Manager must validate certificates used for Transport Layer Security (TLS) functions by performing RFC 5280-compliant certification path validation. |
| EVVM-EP | `SRG-NET-000015-VVEP-00100` | CAT II | The Enterprise Voice, Video, and Messaging Endpoint must not be configured with any vendor default accounts, PINs, or passwords to access configuration settings. |
| EVVM-EP | `SRG-NET-000015-VVEP-00101` | CAT II | The Enterprise Voice, Video, and Messaging Endpoint must be configured to prevent the configuration or display of configuration settings without the use of a PIN or password. |
| EVVM-EP | `SRG-NET-000015-VVEP-00102` | CAT I | The Enterprise Voice, Video, and Messaging Endpoint must be configured to register with an Enterprise Voice, Video, and Messaging Session Manager. |
| EVVM-EP | `SRG-NET-000018-VVEP-00101` | CAT II | The Enterprise Voice, Video, and Messaging Endpoint PC port must be configured to maintain VLAN separation from the voice video VLAN, or be disabled. |
| EVVM-EP | `SRG-NET-000018-VVEP-00102` | CAT II | The Enterprise Voice, Video, and Messaging Endpoint must be configured to integrate into the implemented 802.1x network access control system. |
| EVVM-EP | `SRG-NET-000018-VVEP-00106` | CAT II | The Enterprise Voice, Video, and Messaging Endpoint not supporting 802.1x must be configured to use MAC Authentication Bypass (MAB) on the access switchport. |
| EVVM-EP | `SRG-NET-000018-VVEP-00107` | CAT II | The Enterprise Voice, Video, and Messaging Endpoint must be configured to use a voice video VLAN, separate from all other VLANs. |
| EVVM-EP | `SRG-NET-000029-VVEP-00010` | CAT II | The Enterprise Voice, Video, and Messaging Endpoint must be configured to apply 802.1Q VLAN tags to signaling and media traffic. |
| EVVM-EP | `SRG-NET-000138-VVEP-00029` | CAT I | The Enterprise Voice, Video, and Messaging Endpoint must be configured to uniquely identify participating users. |
| EVVM-EP | `SRG-NET-000140-VVEP-00010` | CAT II | The Enterprise Voice, Video, and Messaging Endpoint must use multifactor authentication for network access to nonprivileged (nonadmin) accounts. |
| EVVM-EP | `SRG-NET-000334-VVEP-00010` | CAT II | The Enterprise Voice, Video, and Messaging Endpoint must offload audit records onto a different system or media than the system being audited. |
| EVVM-EP | `SRG-NET-000371-VVEP-00037` | CAT I | The Enterprise Voice, Video, and Messaging Endpoint must be configured to use FIPS-compliant algorithms for network traffic. |
| EVVM-EP | `SRG-NET-000400-VVEP-00033` | CAT I | The Enterprise Voice, Video, and Messaging Endpoint, when using passwords or PINs for authentication or authorization, must be configured to cryptographically protect the PIN or password. |
| EVVM-EP | `SRG-NET-000512-VVEP-00101` | CAT I | The Enterprise Voice, Video, and Messaging Endpoint must be configured with a firmware release supported by the vendor. |
| EVVM-EP | `SRG-NET-000512-VVEP-00102` | CAT II | The Enterprise Voice, Video, and Messaging Endpoint must be configured to dynamically implement configuration file changes. |
| EVVM-EP | `SRG-NET-000512-VVEP-00103` | CAT II | The Enterprise Voice, Video, and Messaging Endpoint must be configured to disable any auto answer features. |
| EVVM-PM | `SRG-VOIP-000100` | CAT I | The Enterprise Voice, Video, and Messaging Policy must define operations for VTC and endpoint cameras regarding the ability to pick up and transmit sensitive information. |
| EVVM-PM | `SRG-VOIP-000110` | CAT II | The Enterprise Voice, Video, and Messaging Policy must define operations for endpoint microphones regarding the ability to pick up and transmit sensitive information. |
| EVVM-PM | `SRG-VOIP-000230` | CAT II | An inventory of authorized instruments must be documented and maintained in support of the detection of unauthorized instruments connected to the Enterprise Voice, Video, and Messaging system. |
| EVVM-PM | `SRG-VOIP-000270` | CAT II | Implementing Unified Capabilities (UC) soft clients as the primary voice endpoint must have authorizing official (AO) approval. |
| EVVM-PM | `SRG-VOIP-000280` | CAT II | Deploying Unified Capabilities (UC) soft clients on DOD networks must have authorizing official (AO) approval. |
| EVVM-PM | `SRG-VOIP-000300` | CAT II | The local Enterprise Voice, Video, and Messaging system must have the capability to place intrasite and local phone calls when network connectivity is severed from the remote centrally located session controller. |
| EVVM-PM | `SRG-VOIP-000390` | CAT II | Enclaves with commercial VoIP connections must be approved by the DODIN Waiver Panel and signed by DOD CIO for a permanent alternate connection to the Internet Telephony Service Provider (ITSP). |
| EVVM-PM | `SRG-VOIP-000400` | CAT II | The Fire and Emergency Services (FES) communications over a site's telephone system must be configured to support the Department of Defense Instruction (DODI) 6055.06 telecommunication capabilities. |
| EVVM-PM | `SRG-VOIP-000410` | CAT II | The Fire and Emergency Services (F&ES) communications over a site's private telephone system must provide the originating telephone number to the emergency services answering point or call center through a transfer of Automatic Number Identification (ANI) or Automatic Location Identification (ALI) information. |
| EVVM-PM | `SRG-VOIP-000420` | CAT II | The Fire and Emergency Services (F&ES) communications over a site's private telephone system must provide a direct callback telephone number and physical location of an F&ES caller to the emergency services answering point or call center through a transfer of Automatic Number Identification (ANI) and extended Automatic Location Identification (ALI) information or access to an extended ALI database. |
| EVVM-PM | `SRG-VOIP-000430` | CAT II | The Fire and Emergency Services (F&ES) communications over a site's private telephone system must route emergency calls as a priority call in a nonblocking manner. |
| EVVM-PM | `SRG-VOIP-000600` | CAT II | A site utilizing a commercial VoIP/SIP provider must use a provider compliant with FCC STIR/SHAKEN protocol rules. |
| NDM | `SRG-APP-000001-NDM-000200` | CAT II | The network device must limit the number of concurrent sessions to an organization-defined number for each administrator account and/or administrator account type. |
| NDM | `SRG-APP-000026-NDM-000208` | CAT II | The network device must automatically audit account creation. |
| NDM | `SRG-APP-000027-NDM-000209` | CAT II | The network device must automatically audit account modification. |
| NDM | `SRG-APP-000028-NDM-000210` | CAT II | The network device must automatically audit account disabling actions. |
| NDM | `SRG-APP-000029-NDM-000211` | CAT II | The network device must automatically audit account removal actions. |
| NDM | `SRG-APP-000033-NDM-000212` | CAT I | The network device must be configured to assign appropriate user roles or access levels to authenticated users. |
| NDM | `SRG-APP-000038-NDM-000213` | CAT II | The network device must enforce approved authorizations for controlling the flow of management information within the network device based on information flow control policies. |
| NDM | `SRG-APP-000065-NDM-000214` | CAT II | The network device must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must block any login attempt for 15 minutes. |
| NDM | `SRG-APP-000068-NDM-000215` | CAT II | The network device must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the device. |
| NDM | `SRG-APP-000069-NDM-000216` | CAT II | The network device must retain the Standard Mandatory DoD Notice and Consent Banner on the screen until the administrator acknowledges the usage conditions and takes explicit actions to log on for further access. |
| NDM | `SRG-APP-000095-NDM-000225` | CAT II | The network device must produce audit log records containing sufficient information to establish what type of event occurred. |
| NDM | `SRG-APP-000100-NDM-000230` | CAT II | The network device must generate audit records containing information that establishes the identity of any individual or process associated with the event. |
| NDM | `SRG-APP-000119-NDM-000236` | CAT II | The network device must protect audit information from unauthorized modification. |
| NDM | `SRG-APP-000120-NDM-000237` | CAT II | The network device must protect audit information from unauthorized deletion. |
| NDM | `SRG-APP-000131-NDM-000243` | CAT II | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| NDM | `SRG-APP-000142-NDM-000245` | CAT I | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services |
| NDM | `SRG-APP-000148-NDM-000346` | CAT II | The network device must be configured with only one local account to be used as the account of last resort in the event the authentication server is unavailable. |
| NDM | `SRG-APP-000149-NDM-000247` | CAT I | The network device must be configured to use DoD PKI as multi-factor authentication (MFA) for interactive logins. |
| NDM | `SRG-APP-000153-NDM-000249` | CAT II | The network device must be configured to authenticate each administrator prior to authorizing privileges based on assignment of group or role. |
| NDM | `SRG-APP-000164-NDM-000252` | CAT II | The network device must enforce a minimum 15-character password length. |
| NDM | `SRG-APP-000166-NDM-000254` | CAT II | The network device must enforce password complexity by requiring that at least one uppercase character be used. |
| NDM | `SRG-APP-000167-NDM-000255` | CAT II | The network device must enforce password complexity by requiring that at least one lowercase character be used. |
| NDM | `SRG-APP-000168-NDM-000256` | CAT II | The network device must enforce password complexity by requiring that at least one numeric character be used. |
| NDM | `SRG-APP-000169-NDM-000257` | CAT II | The network device must enforce password complexity by requiring that at least one special character be used. |
| NDM | `SRG-APP-000170-NDM-000329` | CAT II | The network device must require that when a password is changed, the characters are changed in at least eight of the positions within the password. |
| NDM | `SRG-APP-000172-NDM-000259` | CAT I | The network device must transmit only encrypted representations of passwords. |
| NDM | `SRG-APP-000175-NDM-000262` | CAT I | The network device must be configured to use DoD approved OCSP responders or CRLs to validate certificates used for PKI-based authentication. |
| NDM | `SRG-APP-000179-NDM-000265` | CAT I | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| NDM | `SRG-APP-000190-NDM-000267` | CAT I | The network device must terminate all network connections associated with a device management session at the end of the session, or the session must be terminated after five minutes of inactivity except to fulfill documented and validated mission requirements. |
| NDM | `SRG-APP-000220-NDM-000268` | CAT II | The network device must invalidate session identifiers upon administrator logout or other session termination. |
| NDM | `SRG-APP-000231-NDM-000271` | CAT I | The network device must only allow authorized administrators to view or change the device configuration, system files, and other files stored either in the device or on removable media (such as a flash drive). |
| NDM | `SRG-APP-000296-NDM-000280` | CAT II | The network device must be configured to provide a logout mechanism for administrator-initiated communication sessions. |
| NDM | `SRG-APP-000340-NDM-000288` | CAT I | The network device must prevent non-privileged users from executing privileged functions to include disabling, circumventing, or altering implemented security safeguards/countermeasures. |
| NDM | `SRG-APP-000343-NDM-000289` | CAT II | The network device must audit the execution of privileged functions. |
| NDM | `SRG-APP-000357-NDM-000293` | CAT II | The network device must allocate audit record storage capacity in accordance with organization-defined audit record storage requirements. |
| NDM | `SRG-APP-000360-NDM-000295` | CAT II | The network device must generate an immediate real-time alert of all audit failure events requiring real-time alerts. |
| NDM | `SRG-APP-000374-NDM-000299` | CAT II | The network device must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). |
| NDM | `SRG-APP-000378-NDM-000302` | CAT II | The network device must prohibit installation of software without explicit privileged status. |
| NDM | `SRG-APP-000380-NDM-000304` | CAT II | The network device must enforce access restrictions associated with changes to device configuration. |
| NDM | `SRG-APP-000395-NDM-000310` | CAT II | The network device must be configured to authenticate SNMP messages using a FIPS-validated Keyed-Hash Message Authentication Code (HMAC). |
| NDM | `SRG-APP-000395-NDM-000347` | CAT II | The network device must authenticate Network Time Protocol sources using authentication that is cryptographically based. |
| NDM | `SRG-APP-000408-NDM-000314` | CAT II | Network devices performing maintenance functions must restrict use of these functions to authorized personnel only. |
| NDM | `SRG-APP-000411-NDM-000330` | CAT I | The network devices must use FIPS-validated Keyed-Hash Message Authentication Code (HMAC) to protect the integrity of nonlocal maintenance and diagnostic communications. |
| NDM | `SRG-APP-000412-NDM-000331` | CAT I | The network device must be configured to implement cryptographic mechanisms using a FIPS 140-2 approved algorithm to protect the confidentiality of remote maintenance sessions |
| NDM | `SRG-APP-000435-NDM-000315` | CAT II | The network device must be configured to protect against known types of denial-of-service (DoS) attacks by employing organization-defined security safeguards. |
| NDM | `SRG-APP-000457-NDM-000352` | CAT II | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| NDM | `SRG-APP-000503-NDM-000320` | CAT II | The network device must generate audit records when successful/unsuccessful logon attempts occur. |
| NDM | `SRG-APP-000505-NDM-000322` | CAT II | The network device must generate audit records showing starting and ending time for administrator access to the system. |
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000317` | CAT II | The network device must be configured in accordance with the security configuration settings based on DoD security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. |
| NDM | `SRG-APP-000516-NDM-000335` | CAT II | The network device must enforce access restrictions associated with changes to the system components. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000344` | CAT II | The network device must obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000795-NDM-000130` | CAT II | The network device must be configured to alert organization-defined personnel or roles upon detection of unauthorized access, modification, or deletion of audit information. |
| NDM | `SRG-APP-000820-NDM-000170` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| NDM | `SRG-APP-000825-NDM-000180` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that the device meets organization-defined strength of mechanism requirements. |
| NDM | `SRG-APP-000845-NDM-000220` | CAT II | The network device must be configured to verify, when users create or update passwords, the passwords are not found on the list of commonly used, expected, or compromised passwords in IA-5 (1) (a) for password-based authentication. |
| NDM | `SRG-APP-000875-NDM-000280` | CAT II | The network device must be configured to implement certificate revocation checking to support path discovery and validation for public key-based authentication. |
| NDM | `SRG-APP-000880-NDM-000290` | CAT II | The network device must be configured to protect nonlocal maintenance sessions by separating the maintenance session from other network sessions with the system by logically separated communications paths. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |

### Collecting evidence

Run `get system status` (firmware version, serial number, and system time)
and keep the output with the checklist, with a configuration backup from
*System > Maintenance > Configuration*. Add screenshots or exports of the
panes the map cites, above all *System > Network > Network*, *System >
Administrator > Administrator*, *System > Administrator > Admin Profile*,
*System > Configuration > Option*, *Security > Password Policy >
Password/PIN Policy*, *Security > Intrusion Detection > Setting*,
*Security > Rate Limit > Web Service*, *System > Advanced > SIP*, *System >
Advanced > Auto Provisioning*, *Phone System > Profile > SIP*, *Phone
System > Profile > Phone*, *Phone System > Profile > User Privilege*,
*System > Certificate > Local Certificate*, *System > Configuration >
SNMP*, *System > Configuration > Time*, and *Log & Report > Log Setting >
Remote*. Export the password audit from *Security > Password Policy >
Password Auditor*, the system and voice logs and call detail records from
the central log server, and the security audit report, and keep the
firmware upgrade record and the backup schedule.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiVoice.** Check the
  version column against the FortiVoice release, and check whether the
  feature depends on the model, the phone model, a license or entitlement,
  or the node's role in an HA group.
- **A command is rejected.** The commands were checked against the
  examples in the 8.0.0 Administration Guide and the 8.0 Solution Guide,
  because there is no CLI Reference. Older releases may lack the command or
  name its options differently; check the CLI's own help, and make sure the
  administrator has the CLI access mode.
- **A setting is not where the map says.** The menus differ between
  releases and between the Administration Guide and the Solution Guide (the
  user privileges appear under both *Phone System > Profile* and
  *Security*, for example). Look for the setting under the older name, and
  check the Administration Guide of your release.
- **Phones stop registering after hardening.** Check that the SIP profile
  transport matches what the phone supports (legacy models lack TLS), that
  the phone's subnet is in the user privilege trusted hosts, that the
  phone's address is not blocked by intrusion detection, and that user
  agent verification matches the configured phone type.
- **Logs do not reach the log server.** Check the server address, port,
  level, and logging policy under *Log & Report > Log Setting > Remote*, and
  the path from FortiVoice.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (checksum checks, account reviews), by another system (the
  identity provider, the central log server, the access switch, the
  boundary SBC or firewall), or not at all. Record how each requirement is
  met, not just which feature covers it.

## Security and Best Practices

- Keep FortiVoice and the FortiFone firmware on vendor-supported releases,
  and install patches promptly, after checking the image checksum.
- Set the admin password at first login, change the default SIP password,
  user password, voicemail PIN, and administrator PIN, enable the password
  and PIN policy with a minimum length of 15, and audit extension passwords
  regularly.
- Authenticate administrators and users through a directory or identity
  provider that enforces DoD PKI and account lockout, keep one local
  account of last resort, and give each administrator the narrowest admin
  profile and access mode that works.
- Allow only HTTPS and SSH on the management interface, set trusted hosts
  for every administrator and every user privilege, and set the idle
  timeout to 5 minutes or less.
- Enable strong cryptography, allow only TLS 1.2 and 1.3, use TLS and
  Secure RTP in every SIP profile, and replace the factory certificate with
  a DoD-issued certificate.
- Turn off default configuration for phones that are not assigned, TFTP,
  unused vertical service codes, and call bridge (DISA), and enable
  intrusion detection and SIP user agent verification.
- Send logs to two central log servers, synchronize time with DoD NTP
  servers, use SNMPv3 only, and send alerts to the ISSO and SA.
- Review this map each time Fortinet publishes a FortiVoice release or
  DISA updates the EVVM or NDM SRGs.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiVoice Phone System Release Notes*, page "What's new",
  releases 7.0.0 to 7.0.8, 7.2.0 to 7.2.5, 7.4.0 to 7.4.2, and 8.0.0, and
  *FortiVoice Release Notes* 8.0.1 (docs.fortinet.com, FortiVoice
  Enterprise documentation).
- Fortinet, *FortiVoice Phone System 8.0.0 Administration Guide* and
  *FortiVoice 8.0 Solution Guide*.
- Fortinet, *FortiVoice Phone System 7.0.0 Administration Guide* (for the
  core features).
- Fortinet, *Increasing FortiVoice Enterprise Encryption Level* (technote
  for release 5.0.4 and later) and *FortiVoice Ports and Protocols*.
- DISA Enterprise Voice, Video, and Messaging Session Management SRG V1R3,
  Endpoint SRG V1R3, and Policy SRG V1R4, and Network Device Management SRG
  V5R5, from the October 2026 STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map), and
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the model for this chapter).

**Knowledge checks:**

1. Which four SRGs apply to FortiVoice in this chapter, and which part of
   a deployment does each one cover?
2. Why is the session management SRG the primary SRG, and why is the
   endpoint SRG used only for some rows?
3. Where does the version data come from, and why is there no New Features
   Guide or CLI Reference behind the map?
4. Which settings prevent auto-registration of phones, and which CAT I
   requirement do they support?
5. Which default credentials must be changed before FortiVoice goes into
   service?
6. Which requirements can FortiVoice not meet exactly, and how do you
   handle them?

## Summary and Completion Checklist

FortiVoice has no STIG, so it is assessed against the EVVM session
management SRG as a session manager, the EVVM endpoint SRG for the
settings it pushes to phones and softclients, the EVVM policy SRG where
its features carry out site policy, and the NDM SRG for its management
plane. This chapter maps 172 features to the FortiVoice release that
introduced them, to 150 SRG requirements, and to the FortiVoice web UI
pane or command that configures them: 86 core platform features,
and 86 features from the FortiVoice 7.0.0 through 8.0.1 release
notes. Operational features with no direct requirement fall under the
requirement to disable nonessential capabilities when unused.

- [ ] Can find the release that introduced a FortiVoice feature.
- [ ] Can map a FortiVoice feature to its EVVM or NDM SRG requirement.
- [ ] Can explain which EVVM SRG applies to which part of a deployment.
- [ ] Can find the FortiVoice web UI pane or command that meets the
  requirement.
- [ ] Can collect FortiVoice evidence and record the requirements
  FortiVoice cannot meet exactly.
