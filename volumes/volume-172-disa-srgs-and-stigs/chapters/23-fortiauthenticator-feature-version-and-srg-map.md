# Chapter 23: FortiAuthenticator Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiAuthenticator release that introduced a given feature.
- Map each FortiAuthenticator feature to the Authentication,
  Authorization, and Accounting (AAA) Services or Network Device
  Management (NDM) SRG requirement it helps satisfy.
- Explain why the AAA Services SRG is the primary SRG for
  FortiAuthenticator, and where the NDM SRG applies instead.
- Find the FortiAuthenticator GUI pane, or the documented CLI command,
  that configures each feature to meet its requirement.
- Use the map to scope an SRG-based assessment of FortiAuthenticator,
  which has no STIG of its own.
- Record the requirements that FortiAuthenticator cannot meet exactly,
  with their mitigations, and plan for its availability.

## Theory and Architecture

FortiAuthenticator is Fortinet's authentication server. It answers
RADIUS (including RADSEC and 802.1X EAP), TACACS+, and LDAP requests from
network devices and applications; acts as a SAML identity provider and an
OAuth and OpenID Connect server; issues and validates one-time passwords
from FortiToken hardware tokens, FortiToken Mobile, email, and SMS, and
FIDO keys; runs a certificate authority with SCEP, CMPv2, CRLs, and an OCSP
responder; provides self-service and captive portals for users and guests;
and collects user logon data for Fortinet single sign-on (FSSO) to
FortiGate. It has **no DISA STIG** (Chapter 10), so it is assessed against
SRGs, as described in Chapter 03. Chapter 10 assigns it the **AAA Services
SRG** and the **NDM SRG**, and notes that because other devices depend on
it for administrator authentication, its availability and logging carry
extra weight. For every FortiAuthenticator feature the chapter gives
**which FortiAuthenticator release introduced it**, **which requirement it
relates to**, and **which GUI pane or command configures it to meet that
requirement**.

FortiAuthenticator runs on hardware appliances and as a virtual machine.
Its configuration uses a few ideas again and again:

- **One user database, three roles.** Every account is a local user or a
  remote LDAP, RADIUS, or SAML user, and has the role *User*,
  *Sponsor*, or *Administrator*. An administrator is a user account flagged
  as one, with full permission or admin profiles, optional trusted
  management subnets, and optional REST API access. The same account can
  also authenticate through RADIUS.
- **Clients and policies.** A network device must be added as a RADIUS or
  TACACS+ *client*, with a shared secret, before FortiAuthenticator answers
  it. *Policies* (and, from 8.0.2, RADIUS *authentication profiles*) then
  decide the authentication type (password and OTP, EAP-TLS, EAP-TEAP, or
  MAC authentication bypass), the identity sources and realms, the
  authentication factors, and the RADIUS or TACACS+ response.
- **User account policies.** Lockouts, password policies (applied through
  local user groups), token settings, trusted subnets, adaptive MFA, and the
  storage of local passwords are set under *Authentication > User Account
  Policies*.
- **Interfaces decide what is answered.** Each network interface has an
  *Admin access* list (SSH, SNMP, the web interface, the REST API, and the
  Security Fabric) and a *Services* list (RADIUS, RADSEC, TACACS+, LDAP,
  LDAPS, FSSO, OCSP, syslog, SAML IdP, and the web paths for portals, SCEP,
  CRL downloads, SCIM, and OAuth). A service that is not enabled on an
  interface does not answer there.
- **System settings.** System access (strong cryptography, the logon
  warning message, administrator IP lockout, and idle timeouts), HA, SNMP,
  firmware, and backups are under *System > Administration*; certificates
  under *Certificate Management*; logs, remote syslog, and audit reports
  under *Logging*.

### Where the version data comes from

Fortinet publishes no Feature Matrix and no New Features Guide for
FortiAuthenticator. The **Release Notes** of every release, however, have
a "What's new" page with one section for each new feature or
enhancement, and the Administration Guide opens with a "What's new in
FortiAuthenticator" chapter that repeats the entries of its train (the
8.0.3 guide's entries for 8.0.0 through 8.0.3 have the same titles as the
release notes). docs.fortinet.com lists two FortiAuthenticator trains,
**6.6** and **8.0**; the product pages of the older 6.x trains are no
longer published, and there is no 7.x train. This chapter covers both.
The version column was built from the "What's new" pages of every
release in the two trains: 6.6.0 through 6.6.11 and 8.0.0 through 8.0.3,
16 releases in all. Eight pages list no features: 6.6.2, 6.6.6, 6.6.8,
6.6.9, 6.6.10, 6.6.11, 8.0.1, and 8.0.3 each say that the release is a
patch release with no new features. The other pages have 66 entries in
the 6.6 train and 31 in the 8.0 train.

Each section of a "What's new" page is one entry, with its title from the
section heading and its description from the text up to the next section.
The entries were checked one by one against the release notes table of
contents, so that no entry was split or dropped (the 8.0.2 page uses a
lower heading level for its sections than the other pages).

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: management
  access, administrator accounts and admin profiles, remote authentication
  servers, password and lockout policies, tokens and two-factor
  authentication, the RADIUS, TACACS+, LDAP, SAML IdP, and OAuth services,
  the certificate authority, logging and audit reports, SNMP, time, HA,
  firmware, and backups. Each one is described in the **FortiAuthenticator
  6.6.0 Administration Guide**, so it existed in 6.6.0 and is not in the
  release notes lists. Three core rows have a different version entry,
  explained below.
- **New features** are the 97 entries of the "What's new" pages.
  The categories were assigned for this chapter, because the release notes
  list features without categories, and the titles were shortened from the
  release notes text. An entry listed again in a later release or train is
  one row with all its versions.

| Version entry | Meaning |
| --- | --- |
| `6.6.0 or earlier` | A core feature described in the FortiAuthenticator 6.6.0 Administration Guide, the oldest release covered |
| `6.6.3 and later` | Introduced in FortiAuthenticator 6.6.3 |
| `6.6.7+; 8.0.0+` | Listed in two trains: from 6.6.7 in the 6.6 train and from 8.0.0 in the 8.0 train |
| `6.6.2 (release notes)` | Documented on the "Data-at-rest protection" page of the release notes, which first appears in 6.6.2 |
| `8.0.3 or earlier` | In the 8.0.3 Administration Guide, but in no release notes page and not found in the 6.6.0 Administration Guide (the RADIUS Message-Authenticator requirement and LACP bond interfaces) |

Three cautions apply. First, "and later" means later in the same train
and, usually, in later trains; a feature of a 6.6 patch release may reach
the 8.0 train only in a later patch (the exclusion of Windows AD computer
accounts from SSO arrived in 6.6.7 and 8.0.0, for example). Second, many
features depend on the model (the power supply monitor on the 400E and
3000E, hardware RAID, the 300F RAID command), on the platform (VM
licensing models), or on a license (FortiToken Mobile licenses, the SMS
messaging service, FortiToken Cloud, and the user license, against which
8.0.2 and later count monthly active users). Third, a core row records a
FortiAuthenticator capability, but its pane was checked against the 8.0.3
Administration Guide and may be named or placed differently on an older
release, and several settings arrived later, as the new-feature rows say
(the administrative account lock and IP lockout exemptions in 6.6.3, the
CRL check mode for remote LDAP servers in 8.0.0, and authentication
profiles, EAP-TEAP, and OCSP checking of EAP-TLS certificates in 8.0.2).

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **AAA** | Authentication, Authorization, and Accounting Services SRG | V2R3, benchmark date 30 Sep 2026 | FortiAuthenticator as an authentication server: accounts, lockout, passwords, PKI-based authentication, multifactor authentication, 802.1X, shared secrets, audit records, time, and the protocols it offers (primary SRG) |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The management plane: administrator access, the logon banner, roles, idle timeout, cryptography for management, SNMP, firmware, backups, and certificates |

The **AAA Services SRG** is the primary SRG, because authenticating,
authorizing, and accounting for users is what FortiAuthenticator does. Its
requirements cover the user accounts and services that FortiAuthenticator
provides to the rest of the network, including the accounts that other
devices' administrators use through RADIUS and TACACS+. The **NDM SRG**
applies to FortiAuthenticator's own management: its administrator
accounts, GUI and CLI access, and system settings. Where both SRGs have a
requirement for the same setting (password length, lockout, audit
content), the map gives the AAA requirement for the user accounts and the
NDM requirement for FortiAuthenticator's administrators.

Neither SRG has a requirement for redundancy. The availability that
Chapter 10 stresses is therefore not a single row of the map: the HA rows
are mapped to the requirements their own settings touch (the HA link's
encryption and management access), and the design advice in this chapter
treats HA as required for any FortiAuthenticator that network devices use
for administrator logins.

The requirement IDs are the **rule version IDs** from the XCCDF files, and
the severity is the rule's severity (high = CAT I, medium = CAT II, low =
CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiAuthenticator
  meets a requirement. The user account lockout policy implements the
  lockout after three failed logins (AAA `SRG-APP-000065-AAA-000200`), for
  example.
- **Must be configured to meet a requirement.** The feature is in scope
  of a requirement and has to be set up correctly. A remote LDAP server
  must use LDAPS or STARTTLS to meet the requirement for secure protocols
  to directory services (AAA `SRG-APP-000142-AAA-000010`, CAT I), for
  example.
- **No direct requirement.** The feature is operational, such as a REST
  API field, a portal option, an FSSO method, or a GUI change. It has no
  requirement of its own, but if it is not needed it falls under the AAA
  requirement to disable non-essential modules
  (AAA `SRG-APP-000141-AAA-000670`).

The mapping is a starting point for an assessment, not a ruling. Confirm
it with your assessor, especially the split between the AAA and NDM SRGs,
and where a requirement is organization-defined or depends on how
FortiAuthenticator is deployed.

### Where the commands come from

Fortinet publishes **no CLI Reference for FortiAuthenticator**: neither
the 6.6 nor the 8.0 train on docs.fortinet.com has one, and the
Administration Guide says that the CLI is for initial setup, factory
reset, and recovery when the GUI is not reachable. Its *CLI commands*
section lists the few configuration paths (`config system interface`,
`config router static`, `config system dns`, `config system global`, and
`config system ha`) and a short list of bootstrap, `execute`, `get`, and
`diagnose` commands. The command column therefore names the **GUI pane**
from the **FortiAuthenticator 8.0.3 Administration Guide** (dated 21
September 2026), the newest Administration Guide, for almost every row,
and uses the CLI only where that guide prints a command. The check was
automatic: each `config` path, `edit` name, `set` option, and literal
value against the one complete CLI block the guide prints (the initial
interface and route setup), each `execute`, `get`, or `diagnose` command
against the guide's text, and each GUI pane against the guide's text. Read
the column this way:

- **GUI:** entries name the FortiAuthenticator GUI pane; the text in
  parentheses names the fields to set.
- Commands run on the FortiAuthenticator CLI, over SSH or the console.
  Statements are separated by `;` to fit in a table cell; on the CLI,
  enter each one on its own line. Values in `<ANGLE_BRACKETS>` are
  placeholders for your own values.
- For **"No direct requirement"** rows, the entry shown is where the
  feature is turned off when it is unused. A dash (**—**) means there is
  nothing to change: the feature is a platform, a REST API field, a GUI
  change, a behavior change, or a capability that is off unless
  configured.

Some requirements cannot be met exactly with FortiAuthenticator settings.
Record them on the checklist as open findings with mitigations, or meet
them another way:

- **No CLI Reference.** Settings can be checked only in the GUI, through
  the REST API, or in a configuration backup. Use screenshots or exports
  of the panes the map cites, and the user audit report, as evidence.
- **Administrator lockout by address, not by account.** The user account
  lockout policy applies only to accounts with the *User* role. For
  administrators, *System > Administration > System Access* blocks the
  source IP address after a number of failed logins for a set period (1 to
  86,400 seconds), and the *Locked* option (6.6.3 and later) lets an
  administrator lock an account by hand. Neither locks an administrator
  account automatically after three failures
  (NDM `SRG-APP-000065-NDM-000214`). Set the IP lockout to three attempts
  and at least 900 seconds, restrict administrators to trusted management
  subnets, require two-factor authentication, and record the difference.
  For user accounts, the guide documents the maximum number of failed
  attempts but not the 15-minute window of
  AAA `SRG-APP-000065-AAA-000200`; with no lockout period, a locked
  account stays disabled until an administrator re-enables it
  (AAA `SRG-APP-000345-AAA-000210`).
- **Password rules.** Password policies set the minimum length (8 by
  default), the four character types, expiry (at least 14 days), password
  history (up to 24), and a check that the password differs from the
  username. No setting is documented for a minimum password lifetime
  (AAA `SRG-APP-000173-AAA-000530`), the number of changed characters
  (AAA `SRG-APP-000170-AAA-000500`, NDM `SRG-APP-000170-NDM-000329`), a
  check against a list of commonly used or compromised passwords or its
  updates (AAA `SRG-APP-000845-AAA-000170`,
  AAA `SRG-APP-000835-AAA-000150`, AAA `SRG-APP-000840-AAA-000160`,
  NDM `SRG-APP-000845-NDM-000220`), or a tool that helps users choose a
  strong password (AAA `SRG-APP-000865-AAA-000210`). Password policies are
  applied through local user groups; the guide does not say how they apply
  to administrator accounts, so put every local administrator in a group
  with a compliant policy and test it. Prefer remote LDAP accounts, whose
  passwords the directory enforces.
- **No account notifications.** FortiAuthenticator logs administrator
  configuration activities, including changes to accounts, but no setting
  sends a notice to the SA and ISSO when an account is created, changed,
  disabled, enabled, or removed
  (AAA `SRG-APP-000291-AAA-000130`, AAA `SRG-APP-000292-AAA-000140`,
  AAA `SRG-APP-000293-AAA-000150`, AAA `SRG-APP-000294-AAA-000160`,
  AAA `SRG-APP-000320-AAA-000180`). Send the logs to a central log server
  or SIEM over TLS and alert there.
- **DoD PKI for administrators.** Administrators log in with a password
  and a one-time password (FortiToken, FortiToken Mobile, email, or SMS);
  the guide documents no certificate (CAC) login to the FortiAuthenticator
  GUI or CLI, so DoD PKI multifactor authentication for interactive logins
  (NDM `SRG-APP-000149-NDM-000247`, CAT I) cannot be met by
  FortiAuthenticator itself. Require a FortiToken for every administrator,
  keep one local account of last resort, and record the finding.
- **PIV credentials for users.** FortiAuthenticator validates PIV and other
  X.509 certificates for 802.1X through EAP-TLS and EAP-TEAP, with
  certificate bindings or trusted CAs, CRLs, and (8.0.2 and later) OCSP.
  Its SAML IdP, OAuth service, portals, RADIUS password logins, TACACS+,
  and LDAP service use passwords with one-time passwords or FIDO keys
  instead. Multifactor authentication with PIV credentials
  (AAA `SRG-APP-000149-AAA-000400` for privileged users,
  AAA `SRG-APP-000150-AAA-000410` for others) is therefore met only for
  802.1X; for the other services, use a PKI-capable identity provider
  upstream (a remote SAML IdP with the MFA authentication context) or
  record the finding.
- **FIPS-validated cryptography.** The guides describe no FIPS or Common
  Criteria mode (NDM `SRG-APP-000179-NDM-000265`,
  NDM `SRG-APP-000412-NDM-000331`, AAA `SRG-APP-000172-AAA-000520`,
  CAT I). *Require strong cryptography* limits administrative access to
  TLS 1.2 and TLS 1.3 with AES-GCM or AES-CBC, SHA-256 or SHA-384, and
  DHE-2048 or X25519 key exchange, and 6.6.0 and later no longer support
  SHA-1 certificates. Check the NIST Cryptographic Module Validation
  Program for your release.
- **RADIUS and TACACS+ secrets.** RADIUS (outside RADSEC and the EAP
  tunnels) and TACACS+ protect credentials only with the shared secret of
  each client, and the guide documents no TLS for TACACS+. Use RADSEC or
  EAP with TLS where the clients support it, require the
  Message-Authenticator attribute, give every client its own long secret
  (AAA `SRG-APP-000516-AAA-000640`), and carry RADIUS and TACACS+ for
  device administration only on the management network
  (AAA `SRG-APP-000516-AAA-000630`).
- **NTP source address.** NTP servers and NTP authentication are
  configurable, but no setting chooses the source interface of NTP traffic
  (AAA `SRG-APP-000516-AAA-000370`); route the NTP servers through the
  management interface.
- **Concurrent sessions and privileged commands.** No setting limits the
  number of concurrent sessions for each administrator
  (NDM `SRG-APP-000001-NDM-000200`), and the guide does not say that CLI
  commands are logged in full text (NDM `SRG-APP-000101-NDM-000231`) or
  that administrator logout is logged with the logon
  (NDM `SRG-APP-000505-NDM-000322`); check *Logging > Log Access > Log
  Types* on your release. The guide also does not state the time stamp
  granularity of the logs (AAA `SRG-APP-000375-AAA-000330`); check it in
  an exported log.
- **Log transport and lost log servers.** Remote syslog supports TLS with
  a verified server certificate (from 8.0.3 the certificate must also carry
  a valid hostname, or the TLS connection fails), and SNMP traps report
  high disk usage. Nothing alerts when a syslog server stops receiving logs
  (AAA `SRG-APP-000108-AAA-000290`, NDM `SRG-APP-000360-NDM-000295`); alert
  on missing logs at the log server.
- **Firmware integrity.** The release notes say to compare the MD5
  checksum of the image with the one from FortiCloud; the guides do not say
  that FortiAuthenticator verifies a digital signature on firmware images
  (NDM `SRG-APP-000131-NDM-000243`). Download images only from FortiCloud
  over HTTPS and compare the checksum before every upgrade.
- **Inactive and emergency accounts.** Inactive user lockout applies to
  local users only (AAA `SRG-APP-000025-AAA-000080`); disable inactive
  remote users in the directory. The guide does not say whether inactive
  user lockout or automatic purging applies to administrator accounts, so
  check that neither can disable the account of last resort
  (AAA `SRG-APP-000234-AAA-000060`).
- **No STIG.** Without a STIG there is no DoD baseline to check against
  (AAA `SRG-APP-000516-AAA-000690`, NDM `SRG-APP-000516-NDM-000317`);
  use this map and the vendor guidance as the baseline, and record the
  settings that differ from it.

## Design Considerations

- **Pick the release first, then the features.** If your design depends
  on a feature introduced in a certain release (IP lockout exemptions and
  the administrative account lock in 6.6.3, the CRL check mode for remote
  LDAP servers in 8.0.0, or OCSP checking of EAP-TLS certificates and
  EAP-TEAP in 8.0.2), that sets the minimum FortiAuthenticator release,
  and it must be a vendor-supported release
  (NDM `SRG-APP-001035-NDM-000340`).
- **Plan for FortiAuthenticator being down.** Network devices that send
  administrator logins to FortiAuthenticator cannot authenticate their
  administrators while it is unreachable. Use an active-passive HA cluster
  (with a dedicated heartbeat interface from 8.0.2), add load-balancing
  nodes at other sites where needed, configure every network device with
  a secondary RADIUS or TACACS+ server, and keep one local account of last
  resort on every device (NDM `SRG-APP-000148-NDM-000346`).
- **Put it on the management network.** Answer RADIUS and TACACS+ for
  device administration only on an interface in the management network,
  allow GUI and SSH access only there, and keep production and guest
  traffic on other interfaces or VLAN segments
  (AAA `SRG-APP-000516-AAA-000650`).
- **Use the directory and a trusted CA chain.** Import users from LDAP
  over LDAPS or STARTTLS, with the CRL check mode set to all nodes, and
  trust only the DoD root and intermediate CAs in *Certificate Management
  > Certificate Authorities > Trusted CAs*.
- **Make two factors mandatory.** Set RADIUS and TACACS+ policies to
  mandatory password and OTP for administrator logins, enable the PCI DSS
  two-factor authentication flow, and avoid OTP bypass through trusted
  subnets or adaptive MFA unless it is approved.
- **Choose secure EAP methods.** Prefer EAP-TLS or EAP-TEAP with DoD
  certificates, check revocation with CRLs or OCSP, and use PEAP or
  EAP-TTLS only inside their TLS tunnels
  (AAA `SRG-APP-000516-AAA-000440`). Microsoft Intune enrollment through
  SCEP is not supported for Azure Government tenants (GCC, GCC High, GCC
  DoD).
- **Log centrally and protect the logs.** Send logs to two syslog
  servers over TLS, or to FortiAnalyzer, back them up to an SFTP server,
  and keep them for the retention period before automatic deletion.
- **Turn off what is not used.** HTTP, LDAP without TLS, SNMP v1 and v2c,
  the OCSP responder, SCEP, CMP, SCIM, FSSO methods, the SAML IdP reverse
  proxy port, guest portals, and the REST API all need a reason to stay
  on.

## Implementation and Automation

### The FortiAuthenticator feature map

The SRG column uses the abbreviations defined in *Where the SRG data
comes from*. The requirement titles are listed in the next table. The
command column follows the conventions in *Where the commands come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/23-fortiauthenticator-feature-version-and-srg-map-feature-map.csv) (198 rows).

| Category | Feature | Introduced (FortiAuthenticator) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Management access | Administrative access on each network interface (SSH, SNMP, Web Interface, RESTful API, and Security Fabric) | 6.6.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000880-NDM-000290`; AAA `SRG-APP-000516-AAA-000630` | GUI: System > Network > Interfaces (Access Rights, Admin access: Web Interface and SSH only on the interface connected to the management network; SNMP, RESTful API, and Security Fabric only where they are used) |
| Core: Management access | Services that each interface answers (HTTPS, HTTP, RADIUS, RADSEC, TACACS+, LDAP, LDAPS, FSSO, OCSP, Syslog, SAML IdP, and the web service paths under HTTPS and HTTP) | 6.6.0 or earlier | AAA `SRG-APP-000142-AAA-000680`; AAA `SRG-APP-000141-AAA-000670`; AAA `SRG-APP-000142-AAA-000020`; NDM `SRG-APP-000142-NDM-000245` | GUI: System > Network > Interfaces (Access Rights, Services: only the services in use, on the interfaces that serve them; LDAP and HTTP off unless a documented need exists) |
| Core: Management access | Initial interface address and administrative access from the CLI (port1 by default) | 6.6.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000408-NDM-000314` | `config system interface`; `edit port1`; `set ip <IP_ADDRESS>/<NETMASK>`; `set allowaccess https-gui https-api ssh`; `next`; `end` |
| Core: Management access | Require strong cryptography for administrative access (TLS 1.2 and TLS 1.3 cipher suites only) | 6.6.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000179-NDM-000265`; NDM `SRG-APP-000172-NDM-000259`; AAA `SRG-APP-000172-AAA-000520` | GUI: System > Administration > System Access (Require strong cryptography: enabled) |
| Core: Management access | HTTPS certificate for the GUI and HTTP Strict Transport Security (HSTS) | 6.6.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000412-NDM-000331` | GUI: System > Administration > System Access (HTTPS Certificate: a DoD-issued server certificate; HSTS enabled) |
| Core: Management access | Pre-authentication warning message (logon banner) | 6.6.0 or earlier | NDM `SRG-APP-000068-NDM-000215`; NDM `SRG-APP-000069-NDM-000216` | GUI: System > Administration > System Access (Warning message before authentication: enabled); GUI: System > Administration > Replacement Messages (the Standard Mandatory DoD Notice and Consent Banner in the pre-authentication messages under Authentication) |
| Core: Management access | IP lockout for administrator logins (failed attempts counted by source IP address, with a lockout period) | 6.6.0 or earlier | NDM `SRG-APP-000065-NDM-000214`; NDM `SRG-APP-000435-NDM-000315` | GUI: System > Administration > System Access (IP lockout maximum failed login attempts 3; Login IP lockout period 900 seconds or longer) |
| Core: Management access | CLI idle timeout and GUI idle timeout | 6.6.0 or earlier | NDM `SRG-APP-000190-NDM-000267`; NDM `SRG-APP-000220-NDM-000268` | GUI: System > Administration > System Access (CLI idle timeout and GUI idle timeout: 5 minutes; never 0 for the CLI) |
| Core: Management access | Host and domain names that the GUI answers to | 6.6.0 or earlier | NDM `SRG-APP-000038-NDM-000213` | GUI: System > Administration > System Access (Allow all hosts/domain names: disabled; Additional allowed hosts/domain names only as needed) |
| Core: Management access | Trusted management subnets for each administrator | 6.6.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213`; NDM `SRG-APP-000880-NDM-000290` | GUI: Authentication > User Management > Local Users (Restrict admin login from trusted management subnets only, with the management subnets) |
| Core: Management access | Administrator logout | 6.6.0 or earlier | NDM `SRG-APP-000296-NDM-000280`; NDM `SRG-APP-000220-NDM-000268` | — |
| Core: Administrator accounts | Default admin account (no password until one is set at the first login) | 6.6.0 or earlier | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000153-NDM-000249`; AAA `SRG-APP-000148-AAA-000390`; AAA `SRG-APP-000234-AAA-000060`; AAA `SRG-APP-000234-AAA-000070` | GUI: Authentication > User Management > Local Users (set a password of 15 or more characters at the first login; keep admin as the one local account of last resort, without account expiration) |
| Core: Administrator accounts | Administrator role on local and remote LDAP user accounts (Full permission or admin profiles) | 6.6.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000516-NDM-000335` | GUI: Authentication > User Management > Local Users (User Role: Administrator; Full permission only for the administrators who need it, admin profiles for the others) |
| Core: Administrator accounts | Admin profiles (read-only and read/write permission sets; built-in read-only profile) | 6.6.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000378-NDM-000302` | GUI: System > Administration > Admin Profiles (permission sets limited to each administrator's duties) |
| Core: Administrator accounts | Web service (REST API) access and API keys for administrators | 6.6.0 or earlier | NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000408-NDM-000314` | GUI: Authentication > User Management > Local Users (Web service access: only for the administrators and integrations that need it) |
| Core: Administrator accounts | Password of the logged-in administrator required before an administrator account is added, edited, or deleted | 6.6.0 or earlier | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | — |
| Core: Administrator accounts | Sponsor role for guest account management | 6.6.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; AAA `SRG-APP-000815-AAA-000140` | GUI: Authentication > User Account Policies > General (Each sponsor only has access to guest users they created: enabled) |
| Core: Authentication | Two-factor authentication for administrator logins (FortiToken, FortiToken Mobile, email, or SMS one-time passwords) | 6.6.0 or earlier | NDM `SRG-APP-000820-NDM-000170`; NDM `SRG-APP-000825-NDM-000180`; NDM `SRG-APP-000149-NDM-000247`; AAA `SRG-APP-000149-AAA-000400` | GUI: Authentication > User Management > Local Users (One-Time Password (OTP) authentication with a FortiToken for every administrator account) |
| Core: Authentication | Remote LDAP servers (LDAPS or STARTTLS with a CA certificate, secondary server, client certificate) | 6.6.0 or earlier | AAA `SRG-APP-000142-AAA-000010`; NDM `SRG-APP-000516-NDM-000336`; AAA `SRG-APP-000910-AAA-000230`; NDM `SRG-APP-000172-NDM-000259` | GUI: Authentication > Remote Auth. Servers > LDAP (Secure Connection enabled, Protocol LDAPS or STARTTLS, Trusted CA Single with the DoD CA certificate; Use secondary server) |
| Core: Authentication | Remote RADIUS servers (primary and optional secondary server, learning mode for user migration) | 6.6.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; AAA `SRG-APP-000516-AAA-000640` | GUI: Authentication > Remote Auth. Servers > RADIUS (a unique secret for each server; Secondary Server for redundancy) |
| Core: Authentication | Remote TACACS+ servers | 6.6.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; AAA `SRG-APP-000516-AAA-000640` | GUI: Authentication > Remote Auth. Servers > TACACS+ (a unique secret for each server) |
| Core: Authentication | Remote SAML identity providers (authentication context Default or MFA) | 6.6.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; AAA `SRG-APP-000150-AAA-000410` | GUI: Authentication > Remote Auth. Servers > SAML (Authentication context: MFA) |
| Core: Authentication | Password policies (minimum length, complexity, password not equal to username) applied through user groups | 6.6.0 or earlier | AAA `SRG-APP-000164-AAA-000450`; AAA `SRG-APP-000166-AAA-000460`; AAA `SRG-APP-000167-AAA-000470`; AAA `SRG-APP-000168-AAA-000480`; AAA `SRG-APP-000169-AAA-000490`; NDM `SRG-APP-000164-NDM-000252`; AAA `SRG-APP-000860-AAA-000200` | GUI: Authentication > User Account Policies > Passwords (in the default policy and every policy in use: Minimum length 15; Check for password complexity, at least one of each character type; Enforce password not equal to username) |
| Core: Authentication | Password change policy (password expiry, renewal reminders, password history, expiry of random passwords) | 6.6.0 or earlier | AAA `SRG-APP-000174-AAA-000540`; AAA `SRG-APP-000024-AAA-000050` | GUI: Authentication > User Account Policies > Passwords (Enable password expiry with a Maximum password age of 180 days or less; Enforce password history; Enable random password expiry) |
| Core: Authentication | Force password change on next logon | 6.6.0 or earlier | AAA `SRG-APP-000855-AAA-000190` | GUI: Authentication > User Management > Local Users (Force password change on next logon for every account whose password an administrator set) |
| Core: Authentication | Password recovery options (email recovery and security question) | 6.6.0 or earlier | AAA `SRG-APP-000855-AAA-000190` | GUI: Authentication > User Management > Local Users (Password Recovery Options: only the methods the organization approves) |
| Core: Authentication | Local user password storage (enhanced cryptography with bcrypt; administrator and sponsor passwords always bcrypt) | 6.6.0 or earlier | AAA `SRG-APP-000171-AAA-000510`; NDM `SRG-APP-000171-NDM-000258`; AAA `SRG-APP-000231-AAA-000610` | GUI: Authentication > User Account Policies > General (Local User Password Storage, Enhanced cryptography: enabled, which cannot be turned off after 30 days and stops CHAP and MSCHAPv2 for local users) |
| Core: Authentication | User account lockout policy (maximum failed login attempts, lockout period or lock until an administrator re-enables the account) | 6.6.0 or earlier | AAA `SRG-APP-000065-AAA-000200`; AAA `SRG-APP-000345-AAA-000210`; AAA `SRG-APP-000805-AAA-000130` | GUI: Authentication > User Account Policies > Lockouts (User account lockout policy enabled, Maximum failed login attempts 3; Specify lockout period disabled, so that locked accounts stay disabled until an administrator re-enables them) |
| Core: Authentication | Inactive user lockout for local users | 6.6.0 or earlier | AAA `SRG-APP-000025-AAA-000080` | GUI: Authentication > User Account Policies > Lockouts (Inactive user lockout, Lock out inactive users after 35 days) |
| Core: Authentication | IP lockout policy for user logins | 6.6.0 or earlier | AAA `SRG-APP-000065-AAA-000200`; NDM `SRG-APP-000435-NDM-000315` | GUI: Authentication > User Account Policies > Lockouts (IP lockout policy enabled, Maximum failed login attempts 3) |
| Core: Authentication | Account expiration for local users | 6.6.0 or earlier | AAA `SRG-APP-000024-AAA-000040`; AAA `SRG-APP-000024-AAA-000050`; AAA `SRG-APP-000700-AAA-000100` | GUI: Authentication > User Management > Local Users (Enable account expiration, 72 hours or less for temporary accounts) |
| Core: Authentication | Disabling and automatic purging of disabled user accounts | 6.6.0 or earlier | AAA `SRG-APP-000705-AAA-000110`; AAA `SRG-APP-000710-AAA-000120`; AAA `SRG-APP-000023-AAA-000030` | GUI: Authentication > User Account Policies > General (Automatically purge disabled user accounts only for the reasons the organization approves; disable accounts that are no longer associated with a user) |
| Core: Authentication | Individual local, remote LDAP, remote RADIUS, and remote SAML user accounts | 6.6.0 or earlier | AAA `SRG-APP-000148-AAA-000390`; AAA `SRG-APP-000516-AAA-000620`; AAA `SRG-APP-000815-AAA-000140` | GUI: Authentication > User Management > Local Users (one account for each person; no shared or group accounts) |
| Core: Authentication | Remote user synchronization rules (import of directory users and their tokens) | 6.6.0 or earlier | AAA `SRG-APP-000023-AAA-000030`; AAA `SRG-APP-000705-AAA-000110` | GUI: Authentication > User Management > Remote User Sync Rules (synchronize users from the directory instead of creating local accounts) |
| Core: Authentication | User groups (local, remote LDAP, remote RADIUS, remote SAML, and MAC) with a password policy and RADIUS attributes | 6.6.0 or earlier | AAA `SRG-APP-000023-AAA-000030`; NDM `SRG-APP-000033-NDM-000212` | GUI: Authentication > User Management > User Groups (Password policy: a policy that meets the requirements for every local group) |
| Core: Authentication | FortiToken hardware tokens and FortiToken Mobile tokens | 6.6.0 or earlier | AAA `SRG-APP-000149-AAA-000400`; AAA `SRG-APP-000150-AAA-000410`; NDM `SRG-APP-000820-NDM-000170` | GUI: Authentication > User Management > FortiTokens |
| Core: Authentication | Token policy (TOTP and HOTP windows, FortiToken Mobile provisioning and PIN, email and SMS token timeout) | 6.6.0 or earlier | NDM `SRG-APP-000156-NDM-000250`; NDM `SRG-APP-000820-NDM-000170` | GUI: Authentication > User Account Policies > Tokens (TOTP authentication window size 1 minute; Require PIN Enforced; Email/SMS Token timeout 60 seconds) |
| Core: Authentication | PCI DSS 3.2 two-factor authentication flow (all factors collected before success or failure is shown) | 6.6.0 or earlier | NDM `SRG-APP-000825-NDM-000180`; AAA `SRG-APP-000150-AAA-000410` | GUI: Authentication > User Account Policies > General (PCI DSS 3.2 two-factor authentication: enabled) |
| Core: Authentication | FIDO authentication for user accounts | 6.6.0 or earlier | AAA `SRG-APP-000150-AAA-000410`; NDM `SRG-APP-000820-NDM-000170` | GUI: Authentication > User Management > Local Users (FIDO authentication, Register FIDO key) |
| Core: Authentication | Trusted subnets that let users bypass one-time password verification | 6.6.0 or earlier | AAA `SRG-APP-000150-AAA-000410`; AAA `SRG-APP-000149-AAA-000400` | GUI: Authentication > User Account Policies > Trusted Subnets (none, unless the bypass is approved) |
| Core: Authentication | Realms for RADIUS clients, SAML IdP, and portals | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Core: Authentication | Custom user fields | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Core: Authentication | Usage profiles (time and data limits) | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Core: Authentication | Guest users and the sponsor portal | 6.6.0 or earlier | AAA `SRG-APP-000024-AAA-000040`; AAA `SRG-APP-000024-AAA-000050` | GUI: Authentication > User Management > Guest Users (account expiration of 72 hours or less) |
| Core: Authentication | Certificate bindings on user accounts (issuer and common name of the user certificate) | 6.6.0 or earlier | AAA `SRG-APP-000177-AAA-000600` | GUI: Authentication > User Management > Local Users (Certificate Bindings: the DoD issuing CA and the common name for each user) |
| Core: RADIUS service | RADIUS clients with a shared secret for each client (IP address, subnet, or range) | 6.6.0 or earlier | AAA `SRG-APP-000516-AAA-000640`; AAA `SRG-APP-000516-AAA-000630` | GUI: Authentication > RADIUS Service > Clients (a unique secret for each client; IP/Hostname rather than subnets or ranges) |
| Core: RADIUS service | Message-Authenticator attribute required from RADIUS clients | 8.0.3 or earlier | AAA `SRG-APP-000516-AAA-000690`; AAA `SRG-APP-000142-AAA-000020` | GUI: Authentication > RADIUS Service > Clients (Require client to send Message-Authenticator attribute: enabled) |
| Core: RADIUS service | RADIUS policies (Password/OTP, EAP-TLS, and MAC authentication bypass; authentication factors) | 6.6.0 or earlier | AAA `SRG-APP-000149-AAA-000400`; AAA `SRG-APP-000150-AAA-000410`; AAA `SRG-APP-000394-AAA-000430`; NDM `SRG-APP-000820-NDM-000170` | GUI: Authentication > RADIUS Service > Policies (Authentication Methods: Mandatory password and OTP, above all for administrator logins to network devices) |
| Core: RADIUS service | EAP methods and EAP server certificate (PEAP, EAP-TTLS, EAP-TLS, EAP-GTC, and EAP-MSCHAPv2) | 6.6.0 or earlier | AAA `SRG-APP-000516-AAA-000440`; AAA `SRG-APP-000158-AAA-000420`; AAA `SRG-APP-000394-AAA-000430` | GUI: Authentication > RADIUS Service > General (EAP Server Certificate: a DoD-issued certificate; Local CAs and Trusted CAs for EAP-TLS limited to DoD CAs) |
| Core: RADIUS service | EAP-TLS client certificate validation (certificate bindings or trusted CAs, expiry, and revocation by CRL) | 6.6.0 or earlier | AAA `SRG-APP-000175-AAA-000570`; AAA `SRG-APP-000175-AAA-000580`; AAA `SRG-APP-000177-AAA-000600`; AAA `SRG-APP-000394-AAA-000430` | GUI: Authentication > RADIUS Service > Auth Profiles (Client Credential Certificates; Authentication mode Certificate bindings, or Trusted CA(s) with DoD CAs only and a current CRL for each) |
| Core: RADIUS service | Windows AD domain authentication for PEAP-MSCHAPv2 | 6.6.0 or earlier | AAA `SRG-APP-000516-AAA-000440` | GUI: Authentication > Remote Auth. Servers > LDAP (Windows Active Directory Domain Authentication only where PEAP-MSCHAPv2 is required) |
| Core: RADIUS service | Response to unauthorized MAC authentication bypass requests and RADIUS attributes for VLAN assignment | 6.6.0 or earlier | AAA `SRG-APP-000516-AAA-000660`; AAA `SRG-APP-000516-AAA-000650` | GUI: Authentication > RADIUS Service > Policies (RADIUS response: Unauthorized Access-Reject, or Access-Accept with the attributes of the guest or unauthorized VLAN) |
| Core: RADIUS service | RADIUS accounting for usage enforcement and RADIUS Disconnect messages | 6.6.0 or earlier | AAA `SRG-APP-000089-AAA-000380` | GUI: Authentication > RADIUS Service > Clients (Accept RADIUS account messages for usage enforcement and Support RADIUS Disconnect messages only where usage limits are enforced) |
| Core: RADIUS service | RADIUS service ports (authentication 1812, accounting SSO 1813, accounting monitor 1646, RADSEC 2083) | 6.6.0 or earlier | AAA `SRG-APP-000142-AAA-000680` | GUI: Authentication > RADIUS Service > Services (the ports approved in the PPSM CAL) |
| Core: RADIUS service | RADSEC (RADIUS over TLS) | 6.6.0 or earlier | AAA `SRG-APP-000142-AAA-000020`; AAA `SRG-APP-000172-AAA-000520` | GUI: Authentication > RADIUS Service > General (RADSEC Server Certificate: a DoD-issued certificate); GUI: System > Network > Interfaces (Services: RADSEC) |
| Core: RADIUS service | RADIUS accounting proxy | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | GUI: Authentication > RADIUS Service > Accounting Proxy |
| Core: RADIUS service | Custom RADIUS dictionaries | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Core: TACACS+ service | TACACS+ clients with a shared secret for each client | 6.6.0 or earlier | AAA `SRG-APP-000516-AAA-000640`; AAA `SRG-APP-000516-AAA-000630` | GUI: Authentication > TACACS+ Service > Clients (a unique secret for each client; IP Address rather than subnets) |
| Core: TACACS+ service | TACACS+ policies (clients, identity sources, and authentication factors) | 6.6.0 or earlier | AAA `SRG-APP-000149-AAA-000400`; NDM `SRG-APP-000820-NDM-000170` | GUI: Authentication > TACACS+ Service > Policies (two-factor authentication for every administrator of a network device) |
| Core: TACACS+ service | TACACS+ authorization rules (privilege level, non-shell services, and shell commands) | 6.6.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000340-NDM-000288` | GUI: Authentication > TACACS+ Service > Authorization (Default permission for shell commands: Deny, with only the allowed commands for each role) |
| Core: TACACS+ service | Session duration of authenticated TACACS+ users (28,800 seconds by default) | 6.6.0 or earlier | NDM `SRG-APP-000400-NDM-000313` | GUI: Authentication > User Account Policies > General (Session Expiry, TACACS+ authentication: the organization-defined period) |
| Core: LDAP service | LDAP service and directory tree (LDAP server certificate) | 6.6.0 or earlier | AAA `SRG-APP-000142-AAA-000020`; AAA `SRG-APP-000142-AAA-000010` | GUI: Authentication > LDAP Service > General (LDAP server certificate: a DoD-issued certificate); GUI: System > Network > Interfaces (Services: LDAPS rather than LDAP) |
| Core: LDAP service | LDAP browsing permission for user accounts | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | GUI: Authentication > User Management > Local Users (Allow LDAP browsing: off) |
| Core: SAML IdP and OAuth | SAML IdP portal (IdP certificate, signing algorithm, login session timeout) | 6.6.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; AAA `SRG-APP-000150-AAA-000410` | GUI: Authentication > SAML IdP > General (Default IdP certificate: a DoD-issued certificate; Default signing algorithm SHA-256 or stronger; Login session timeout as the organization defines) |
| Core: SAML IdP and OAuth | SAML service providers (server certificate, signing algorithm, and token-based authentication for each SP) | 6.6.0 or earlier | AAA `SRG-APP-000150-AAA-000410`; AAA `SRG-APP-000149-AAA-000400` | GUI: Authentication > SAML IdP > Service Providers (token-based authentication for every SP; no bypass for users from trusted subnets) |
| Core: SAML IdP and OAuth | OAuth service (relying parties, scopes, and policies) | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | GUI: Authentication > OAuth Service > General |
| Core: Portals | Self-service and captive portals (pre-login and post-login services, disclaimer) | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | GUI: Authentication > Portals > Portals |
| Core: Fortinet SSO | Fortinet single sign-on methods (domain controller polling, RADIUS accounting, syslog, FortiClient SSO Mobility Agent) | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | GUI: Fortinet SSO > Settings > Methods |
| Core: Certificate authority | Local CAs (created or imported, private keys optionally on a NetHSM) | 6.6.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; AAA `SRG-APP-000176-AAA-000590` | GUI: Certificate Management > Certificate Authorities > Local CAs (only for the internal uses that the PKI policy allows); GUI: System > Administration > NetHSMs |
| Core: Certificate authority | Trusted CAs (no third-party CA certificates are preinstalled) | 6.6.0 or earlier | AAA `SRG-APP-000910-AAA-000230`; NDM `SRG-APP-000910-NDM-000300`; AAA `SRG-APP-000175-AAA-000570` | GUI: Certificate Management > Certificate Authorities > Trusted CAs (import only the DoD root and intermediate CAs) |
| Core: Certificate authority | Certificate revocation lists (imported CRLs, local CRLs, and automatically downloaded CRLs) | 6.6.0 or earlier | AAA `SRG-APP-000175-AAA-000580`; AAA `SRG-APP-000875-AAA-000220`; NDM `SRG-APP-000875-NDM-000280`; NDM `SRG-APP-000175-NDM-000262` | GUI: Certificate Management > Certificate Authorities > CRLs (a current CRL for every trusted DoD CA) |
| Core: Certificate authority | OCSP responder for the certificates that FortiAuthenticator issues (TCP/2560) | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | GUI: System > Network > Interfaces (Services: OCSP) |
| Core: Certificate authority | User and server certificates (key type, key size, and hash algorithm) | 6.6.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; AAA `SRG-APP-000176-AAA-000590` | GUI: Certificate Management > End Entities > Users (RSA 2048 bits or larger, or ECC; SHA-256 or stronger); GUI: Certificate Management > End Entities > Local Services |
| Core: Certificate authority | Certificate expiry warning email | 6.6.0 or earlier | NDM `SRG-APP-000516-NDM-000344` | GUI: Certificate Management > Policies > General (Warn when a certificate is about to expire) |
| Core: Certificate authority | SCEP server | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | GUI: Certificate Management > SCEP > General (Enable SCEP) |
| Core: Logging | Event logs (category, subcategory, level, action, status, user, and source IP address) | 6.6.0 or earlier | AAA `SRG-APP-000089-AAA-000380`; AAA `SRG-APP-000095-AAA-000220`; AAA `SRG-APP-000096-AAA-000230`; AAA `SRG-APP-000097-AAA-000240`; AAA `SRG-APP-000098-AAA-000250`; AAA `SRG-APP-000099-AAA-000260`; AAA `SRG-APP-000100-AAA-000270`; NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000100-NDM-000230`; NDM `SRG-APP-000503-NDM-000320` | GUI: Logging > Log Access > Logs |
| Core: Logging | Log events for administrator configuration activities and account changes | 6.6.0 or earlier | AAA `SRG-APP-000026-AAA-000090`; AAA `SRG-APP-000027-AAA-000100`; AAA `SRG-APP-000028-AAA-000110`; AAA `SRG-APP-000029-AAA-000120`; AAA `SRG-APP-000319-AAA-000170`; NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000027-NDM-000209`; NDM `SRG-APP-000028-NDM-000210`; NDM `SRG-APP-000029-NDM-000211`; NDM `SRG-APP-000343-NDM-000289` | GUI: Logging > Log Access > Logs |
| Core: Logging | Remote syslog servers (up to 20, with level, facility, and TLS with a verified server certificate) | 6.6.0 or earlier | AAA `SRG-APP-000358-AAA-000280`; NDM `SRG-APP-000516-NDM-000350`; NDM `SRG-APP-000515-NDM-000325` | GUI: Logging > Log Config > Syslog Servers (two servers, Secure Connection enabled); GUI: Logging > Log Config > Log Settings (Send system logs to remote Syslog servers) |
| Core: Logging | Logging to FortiAnalyzer or FortiManager | 6.6.0 or earlier | AAA `SRG-APP-000358-AAA-000280`; NDM `SRG-APP-000515-NDM-000325` | GUI: Logging > Log Config > Log Settings (Send logs to FortiManager/FortiAnalyzer) |
| Core: Logging | Log backup to an FTP server and automatic log deletion (after 12 months by default) | 6.6.0 or earlier | NDM `SRG-APP-000357-NDM-000293`; NDM `SRG-APP-000120-NDM-000237`; NDM `SRG-APP-000515-NDM-000325` | GUI: Logging > Log Config > Log Settings (Enable remote backup to an SFTP server; Enable log auto-deletion only after the retention period) |
| Core: Logging | User audit reports | 6.6.0 or earlier | AAA `SRG-APP-000023-AAA-000030`; AAA `SRG-APP-000025-AAA-000080` | GUI: Logging > Audit Reports > Users Audit (Download User Audit on a schedule and review the role, admin profile, and last used columns) |
| Core: Logging | Debug logs and debug reports | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Core: Monitoring | SNMP v1/v2c communities and SNMP v3 users | 6.6.0 or earlier | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000142-NDM-000245` | GUI: System > Administration > SNMP (SNMP v3 users only, Security level Encryption and authentication; no SNMP v1/v2c communities) |
| Core: Monitoring | SNMP traps and thresholds (lockouts, HA status, disk usage, RAID, authentication failure rate) | 6.6.0 or earlier | AAA `SRG-APP-000108-AAA-000290`; NDM `SRG-APP-000360-NDM-000295`; NDM `SRG-APP-000795-NDM-000130` | GUI: System > Administration > SNMP (Events: User lockout detected, IP lockout detected, HA status is changed, Disk usage is high, RAID status changed, and Auth failure rate threshold exceeded) |
| Core: Monitoring | Locked-out users and locked-out IP addresses monitors | 6.6.0 or earlier | AAA `SRG-APP-000345-AAA-000210` | GUI: Monitor > Authentication > Locked-out Users |
| Core: Monitoring | Dashboard widgets (system information, authentication activity, top user lockouts, disk monitor) | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Core: Messaging | SMTP servers and email services for one-time passwords and notifications | 6.6.0 or earlier | AAA `SRG-APP-000142-AAA-000020` | GUI: System > Messaging > SMTP Servers (an external mail relay, Secure connection STARTTLS, Enable authentication) |
| Core: Messaging | SMS gateways | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | GUI: System > Messaging > SMS Gateways |
| Core: Time | System time, time zone, and NTP (two servers, with authentication) | 6.6.0 or earlier | AAA `SRG-APP-000116-AAA-000320`; AAA `SRG-APP-000516-AAA-000350`; AAA `SRG-APP-000516-AAA-000360`; AAA `SRG-APP-000374-AAA-000340`; NDM `SRG-APP-000395-NDM-000347`; NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000374-NDM-000299` | GUI: System > Dashboard > Status (System Information widget, System Time: NTP enabled with two DoD NTP servers, Enable authentication with a key for each) |
| Core: Network | DNS servers and static routes | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Core: Network | Zero trust tunnels to remote LDAP servers | 6.6.0 or earlier | AAA `SRG-APP-000142-AAA-000010` | GUI: System > Network > Zero Trust Tunnels |
| Core: Network | Packet capture | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Core: Network | LACP bond interfaces (created from the CLI) | 8.0.3 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Core: Availability | HA cluster (active-passive cluster members, IPsec with a shared password, management interface and access, monitored interfaces) | 6.6.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000880-NDM-000290` | GUI: System > Administration > High Availability (Role Cluster member on two units; a strong Password; Management access SSH and Web Interface only; a dedicated link between the units) |
| Core: Availability | Load-balancing HA (standalone primary and up to ten load balancers) | 6.6.0 or earlier | NDM `SRG-APP-000412-NDM-000331` | GUI: System > Administration > High Availability (Role Standalone Primary and Load Balancer; a strong Password) |
| Core: Availability | Firmware upgrade (GUI, CLI from FTP or TFTP, coordinated HA upgrade, upgrade history) | 6.6.0 or earlier | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000131-NDM-000243`; NDM `SRG-APP-000378-NDM-000302` | GUI: System > Administration > Firmware Upgrade (a vendor-supported release; compare the MD5 checksum with the one from FortiCloud before upgrading) |
| Core: Availability | Configuration backup and restore (encrypted backup file) | 6.6.0 or earlier | NDM `SRG-APP-000516-NDM-000340`; AAA `SRG-APP-000231-AAA-000610` | GUI: System > Dashboard > Status (System Information widget, System Configuration: Backup/Restore with Encryption and a password) |
| Core: Availability | Configuration auto-backup to FTP or SFTP servers (secondary server, encryption) | 6.6.0 or earlier | NDM `SRG-APP-000516-NDM-000340` | GUI: System > Administration > Config Auto-backup (enabled, an SFTP server and a Secondary FTP server, Encryption with a password) |
| Core: Availability | FTP servers (FTP or SFTP) for backups | 6.6.0 or earlier | NDM `SRG-APP-000172-NDM-000259` | GUI: System > Administration > FTP Servers (Connection type SFTP) |
| Core: Availability | Data-at-rest protection (AES256 encryption of secrets, salted SHA-256 hashes, encrypted file system) | 6.6.2 (release notes) | AAA `SRG-APP-000231-AAA-000610` | — |
| Core: Availability | Licensing and FortiGuard connections (FortiToken provisioning, messaging service, proxy) | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Core: Availability | RAID and disk replacement | 6.6.0 or earlier | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Fortinet SSO | Remote LDAP user groups included in FSSO and in FortiGate filters | 6.6.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | GUI: Authentication > User Management > User Groups (Include for FSSO: off) |
| RADIUS service | FortiToken Mobile push without a RADIUS Access-Challenge | 6.6.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | GUI: Authentication > RADIUS Service > Policies (Trigger push without RADIUS challenge: off) |
| SAML IdP and OAuth | Authorization code with PKCE grant type for public OAuth clients | 6.6.0 and later | AAA `SRG-APP-000142-AAA-000020` | GUI: Authentication > OAuth Service > Relying Party (Authorization code with PKCE for every public client) |
| Portals | No authentication type for captive portal policies | 6.6.0 and later | AAA `SRG-APP-000148-AAA-000390`; AAA `SRG-APP-000815-AAA-000140` | GUI: Authentication > Portals > Policies (no captive portal policy with the No authentication type unless the access it gives is approved) |
| RADIUS service | Maximum number of concurrent MAC devices for each user in usage profiles | 6.6.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| SAML IdP and OAuth | SAML IdP login session timeout up to 120 days | 6.6.0 and later | NDM `SRG-APP-000400-NDM-000313` | GUI: Authentication > SAML IdP > General (Login session timeout: the organization-defined period, not the maximum) |
| SAML IdP and OAuth | Custom user fields in SAML SP assertion attributes | 6.6.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Portals | Expiry of MAC devices tracked by captive portals | 6.6.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Availability | Selectable configuration subsets synchronized to load-balancing HA nodes | 6.6.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Logging | User audit report limited to administrator and sponsor accounts | 6.6.0 and later | AAA `SRG-APP-000023-AAA-000030`; NDM `SRG-APP-000033-NDM-000212` | GUI: Logging > Audit Reports > Users Audit (Only include administrator & sponsor accounts, for the periodic review of privileged accounts) |
| Authentication | Migration of FortiToken Mobile tokens to FortiToken Cloud | 6.6.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Certificate authority | CMPv2 certificate enrollment server | 6.6.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | GUI: Certificate Management > CMP > General |
| Authentication | SCIM client for provisioning users to service providers | 6.6.0 and later | AAA `SRG-APP-000023-AAA-000030` | GUI: Authentication > SCIM > Service Provider |
| SAML IdP and OAuth | IAM logins and IAM claims in the OAuth service | 6.6.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Fortinet SSO | Username attribute from the LDAP lookup for FortiGate FSSO | 6.6.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| SAML IdP and OAuth | Custom user fields in OAuth relying party claims | 6.6.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| REST API | Company and department fields in the local, LDAP, and RADIUS user endpoints | 6.6.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Authentication | Two-minute cache of successful LDAP authentications | 6.6.0 and later | NDM `SRG-APP-000400-NDM-000313` | — |
| SAML IdP and OAuth | Hardened SAML IdP login with a Use token toggle | 6.6.1 and later | AAA `SRG-APP-000150-AAA-000410` | GUI: Authentication > SAML IdP > Replacement Messages |
| Portals | Delivery methods allowed when users reconfigure FortiToken Mobile in the self-service portal | 6.6.1 and later | AAA `SRG-APP-000855-AAA-000190` | GUI: Authentication > Portals > Portals (Authorized delivery options: only the approved methods) |
| Certificate authority | Subject alternative names for wildcard SCEP enrollment and optional password on renewal | 6.6.1 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| SAML IdP and OAuth | SAML IdP reverse proxy port for FortiProxy Cloud | 6.6.1 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | GUI: System > Network > Interfaces (SAML IdP Reverse Proxy: off) |
| Authentication | Optional secondary remote TACACS+ server | 6.6.1 and later | NDM `SRG-APP-000516-NDM-000336` | GUI: Authentication > Remote Auth. Servers > TACACS+ (Secondary Server for redundancy) |
| Authentication | Offline FortiToken Mobile provisioning for air-gapped FortiAuthenticator devices | 6.6.1 and later | AAA `SRG-APP-000150-AAA-000410` | GUI: Authentication > User Account Policies > Tokens (Provision mode: Offline on networks without Internet access) |
| Authentication | Remote user synchronization rules over SCIM | 6.6.1 and later | AAA `SRG-APP-000023-AAA-000030` | GUI: Authentication > User Management > Remote User Sync Rules |
| Authentication | Import and export of user and user group data through CSV files | 6.6.1 and later | AAA `SRG-APP-000023-AAA-000030` | — |
| Fortinet SSO | Reorganized Fortinet SSO menus | 6.6.1 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Portals | Endorser email address entered by guests at self-registration | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Certificate authority | CRL distribution point and OCSP responder extensions in CMP-issued certificates | 6.6.3 and later | NDM `SRG-APP-000875-NDM-000280` | GUI: Certificate Management > CMP > Enrollment Requests (Other Extensions: the CRL distribution point and OCSP responder URL) |
| Authentication | FortiToken Mobile tokens in third-party MFA applications | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| RADIUS service | IPv6 for RADIUS servers, captive portals, self-service portals, and trusted subnets | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| SAML IdP and OAuth | Conditional consent and login prompts and independent session timeouts for OAuth and OIDC | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Platform | More user groups for each user (users divided by 5) | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Authentication | Data limit for each time interval in usage profiles | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| SAML IdP and OAuth | OIDC logout endpoint that revokes access, refresh, and ID tokens | 6.6.3 and later | NDM `SRG-APP-000220-NDM-000268` | — |
| Authentication | Global FIDO user verification setting | 6.6.3 and later | AAA `SRG-APP-000150-AAA-000410` | GUI: Authentication > User Account Policies > Tokens (FIDO user verification: required) |
| Authentication | Password and OTP concatenation for FortiToken Cloud tokens in RADIUS, TACACS+, and LDAP | 6.6.3 and later | AAA `SRG-APP-000150-AAA-000410` | — |
| Authentication | Guest user passwords set by administrators, custom fields, and new admin profile permissions | 6.6.3 and later | NDM `SRG-APP-000033-NDM-000212` | GUI: System > Administration > Admin Profiles (Can change password of guest user only for the administrators who manage guests) |
| Portals | Password reset with SMS or FortiToken verification | 6.6.3 and later | AAA `SRG-APP-000855-AAA-000190` | GUI: Authentication > Portals > Portals (Password Reset, Verification methods: FortiToken or another approved method) |
| Authentication | Passwords of up to 64 characters for privileged user accounts | 6.6.3 and later | AAA `SRG-APP-000860-AAA-000200` | — |
| Portals | Smart Connect application for Chromebooks | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Fortinet SSO | User groups restricted to the global pre-filter | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| REST API | user_ip field in the authentication and OAuth token endpoints | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Authentication | Administrative account lock (Locked option for local, LDAP, RADIUS, and SAML users) | 6.6.3 and later | AAA `SRG-APP-000710-AAA-000120`; AAA `SRG-APP-000345-AAA-000210` | GUI: Authentication > User Management > Local Users (Locked, for accounts that violate policy) |
| Fortinet SSO | Selectable server certificate for the FortiClient SSO Mobility Agent service (port 8001) | 6.6.3 and later | NDM `SRG-APP-000516-NDM-000344` | GUI: Fortinet SSO > Settings > Methods (Server certificate: the certificate signed by the current CA) |
| Logging | Logs of unusual login activity and of email and mobile number changes | 6.6.3 and later | AAA `SRG-APP-000089-AAA-000380`; AAA `SRG-APP-000027-AAA-000100`; NDM `SRG-APP-000795-NDM-000130` | GUI: Logging > Log Access > Logs |
| Authentication | IP address and subnet exemptions from IP lockout | 6.6.3 and later | AAA `SRG-APP-000065-AAA-000200` | GUI: Authentication > User Account Policies > Lockouts (IP Lockout Exemptions: none, unless approved) |
| Management access | Cross-Origin Resource Sharing (CORS) HTTP headers | 6.6.3 and later | NDM `SRG-APP-000038-NDM-000213` | GUI: System > Administration > System Access (Cross-Origin Resource Sharing (CORS): None, or Selective with the approved origins) |
| Authentication | Adaptive MFA that bypasses OTP verification on a known device | 6.6.3 and later | AAA `SRG-APP-000150-AAA-000410`; AAA `SRG-APP-000149-AAA-000400` | GUI: Authentication > User Account Policies > Adaptive MFA Rules (Known devices: off unless approved) |
| REST API | REST API rate limiting moved and relabeled (Restrict number of authentication requests) | 6.6.3 and later | NDM `SRG-APP-000435-NDM-000315` | GUI: Authentication > OAuth Service > General (Restrict number of authentication requests to: enabled) |
| Certificate authority | ACME account persistence for server certificates | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| REST API | approval_prompt and prompt fields in the OIDC authorization endpoint | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Fortinet SSO | Manual discovery of AD servers for group lookups | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Management access | SCIM path in the HTTPS service access rights of an interface | 6.6.3 and later | AAA `SRG-APP-000142-AAA-000680`; NDM `SRG-APP-000142-NDM-000245` | GUI: System > Network > Interfaces (SCIM (/scim): off unless the SCIM server is used) |
| Authentication | More reasons for purging disabled local users | 6.6.3 and later | AAA `SRG-APP-000705-AAA-000110`; AAA `SRG-APP-000710-AAA-000120` | GUI: Authentication > User Account Policies > General (Purge users that are disabled due to the following reasons: only the approved reasons) |
| RADIUS service | Acct-Session-Id attribute in RADIUS Disconnect-Request messages | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| SAML IdP and OAuth | SAML IdP realms moved to a User Sources tab | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Authentication | CLI command that searches the LDAP directory for the username before the LDAP bind | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | `diagnose authentication radius-force-ldap-user-lookup disable` |
| Monitoring | Access token, refresh token, authorization code, and JWT token tabs in the OAuth token monitor | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| REST API | sub_type field in the FortiTokens endpoint | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| RADIUS service | RADIUS service Certificates tab renamed General, with a maximum fragment size for EAP-TLS | 6.6.3 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Authentication | SCIM synchronization disabled after a configuration restore | 6.6.3 and later | AAA `SRG-APP-000023-AAA-000030` | GUI: Authentication > User Account Policies > General (Re-activate SCIM (client) only after checking the restored configuration) |
| Certificate authority | Delete button for imported CRLs | 6.6.4 and later | AAA `SRG-APP-000175-AAA-000580` | GUI: Certificate Management > Certificate Authorities > CRLs (delete only superseded CRLs) |
| Platform | CLI command that skips RAID creation during a factory reset (FortiAuthenticator 300F) | 6.6.5 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Certificate authority | DNS subject alternative name kept in renewed CMP device certificates | 6.6.5 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Fortinet SSO | Exclusion of Windows AD computer accounts from SSO | 6.6.7+; 8.0.0+ | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Certificate authority | Deletion of a user certificate's private key once it is downloaded | 8.0.0 and later | AAA `SRG-APP-000176-AAA-000590` | GUI: Certificate Management > Policies > General (Delete user certificate's private key once downloaded: enabled) |
| Certificate authority | SCEP with Microsoft Intune and EAP-TLS with Entra ID users and groups | 8.0.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| SAML IdP and OAuth | Required authentication method for IdP-initiated SAML logins (FIDO) | 8.0.0 and later | AAA `SRG-APP-000150-AAA-000410` | GUI: Authentication > SAML IdP > General (IdP Initiated Login: a two-factor method) |
| REST API | Creation and deletion of multiple local users in the local users endpoint | 8.0.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| REST API | X-Request-ID header for tracking end-user operations in logs | 8.0.0 and later | AAA `SRG-APP-000100-AAA-000270` | — |
| Platform | Subscription VM licenses | 8.0.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Availability | Priority override option for active-passive HA | 8.0.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| RADIUS service | Client certificate CN from a user attribute or MAC address, and verification of the MAC address in the certificate for EAP-TLS | 8.0.0 and later | AAA `SRG-APP-000158-AAA-000420`; AAA `SRG-APP-000177-AAA-000600` | GUI: Authentication > RADIUS Service > Auth Profiles (Verify MAC address in CN of client certificate, where device certificates carry the MAC address) |
| SAML IdP and OAuth | Custom multi-value SAML assertion attributes in user groups | 8.0.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| SAML IdP and OAuth | Authorization of users for each SAML service provider (LDAP group subtypes) | 8.0.0 and later | NDM `SRG-APP-000033-NDM-000212` | GUI: Authentication > SAML IdP > Service Providers |
| Portals | FortiGuest guest portals in FortiAuthenticator (beta) | 8.0.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Portals | Legacy self-service portal removed, and administrator logins with the username only | 8.0.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| RADIUS service | CLI command that overrides the ECDH curves for EAP | 8.0.0 and later | AAA `SRG-APP-000516-AAA-000440` | `diagnose authentication radius-eap-ecdh-curve` |
| Authentication | CRL check mode for the secure connection to remote LDAP servers | 8.0.0 and later | AAA `SRG-APP-000142-AAA-000010`; NDM `SRG-APP-000875-NDM-000280` | GUI: Authentication > Remote Auth. Servers > LDAP (CRL Check Mode: All Nodes, with a CRL for every CA in the chain) |
| Logging | SAML and Generic API debug log categories for the web server | 8.0.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Authentication | OTP-only push notification mode | 8.0.0 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| RADIUS service | RADIUS accounting over RADSEC, and verification of RADSEC client certificates | 8.0.0 and later | AAA `SRG-APP-000142-AAA-000020`; AAA `SRG-APP-000910-AAA-000230` | GUI: Authentication > RADIUS Service > General |
| TACACS+ service | TACACS+ client groups | 8.0.2 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| Availability | Separate HA management interface and heartbeat interface | 8.0.2 and later | NDM `SRG-APP-000880-NDM-000290` | GUI: System > Administration > High Availability (Heartbeat Interface: a dedicated interface) |
| Availability | Mixed perpetual and subscription licenses in HA and load-balancing deployments | 8.0.2 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| LDAP service | Authentication factors verified by the LDAP service during an LDAP bind | 8.0.2 and later | AAA `SRG-APP-000150-AAA-000410` | GUI: Authentication > LDAP Service > General (Authentication Methods: password and OTP where the LDAP clients support it) |
| Monitoring | Monthly active users widget and active users monitor | 8.0.2 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| RADIUS service | EAP-TEAP (chained machine and user authentication), authentication profiles, and RADIUS client groups | 8.0.2 and later | AAA `SRG-APP-000516-AAA-000440`; AAA `SRG-APP-000394-AAA-000430` | GUI: Authentication > RADIUS Service > Auth Profiles |
| Certificate authority | Elliptic curve keys for local CA, user, and server certificates | 8.0.2 and later | NDM `SRG-APP-000516-NDM-000344` | GUI: Certificate Management > Certificate Authorities > Local CAs (Key type ECC with an approved key size, or RSA) |
| Portals | Smart Connect application from the Microsoft Store for Windows | 8.0.2 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| RADIUS service | OCSP verification of EAP-TLS client certificates for each authentication profile | 8.0.2 and later | AAA `SRG-APP-000175-AAA-000580`; AAA `SRG-APP-000875-AAA-000220`; NDM `SRG-APP-000875-NDM-000280` | GUI: Authentication > RADIUS Service > Auth Profiles (the OCSP verification mode set to Enable) |
| Troubleshooting | New diagnose debug CLI commands | 8.0.2 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | `diagnose debug clear-all` |
| REST API | display_name field in the local users endpoint | 8.0.2 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| REST API | Endpoints for adding an external IdP through self-service | 8.0.2 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |
| REST API | Built-in Swagger documentation of the REST API | 8.0.2 and later | No direct requirement; if unused, disable (AAA `SRG-APP-000141-AAA-000670`) | — |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current SRG releases:

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/23-fortiauthenticator-feature-version-and-srg-map-requirements.csv) (140 rows).

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| AAA | `SRG-APP-000023-AAA-000030` | CAT II | AAA Services must be configured to provide automated account management functions. |
| AAA | `SRG-APP-000024-AAA-000040` | CAT II | AAA Services must be configured to automatically remove temporary user accounts after 72 hours. |
| AAA | `SRG-APP-000024-AAA-000050` | CAT II | AAA Services must be configured to automatically remove authorizations for temporary user accounts after 72 hours. |
| AAA | `SRG-APP-000025-AAA-000080` | CAT II | AAA Services must be configured to automatically disable accounts after a 35-day period of account inactivity. |
| AAA | `SRG-APP-000026-AAA-000090` | CAT II | AAA Services must be configured to automatically audit account creation. |
| AAA | `SRG-APP-000027-AAA-000100` | CAT II | AAA Services must be configured to automatically audit account modification. |
| AAA | `SRG-APP-000028-AAA-000110` | CAT II | AAA Services must be configured to automatically audit account disabling actions. |
| AAA | `SRG-APP-000029-AAA-000120` | CAT II | AAA Services must be configured to automatically audit account removal actions. |
| AAA | `SRG-APP-000065-AAA-000200` | CAT II | AAA Services must be configured to automatically lock user accounts after three consecutive invalid logon attempts within a 15-minute time period. |
| AAA | `SRG-APP-000089-AAA-000380` | CAT II | AAA Services must be configured to audit each authentication and authorization transaction. |
| AAA | `SRG-APP-000095-AAA-000220` | CAT II | AAA Services configuration audit records must identify what type of events occurred. |
| AAA | `SRG-APP-000096-AAA-000230` | CAT II | AAA Services configuration audit records must identify when (date and time) the events occurred. |
| AAA | `SRG-APP-000097-AAA-000240` | CAT II | AAA Services configuration audit records must identify where the events occurred. |
| AAA | `SRG-APP-000098-AAA-000250` | CAT II | AAA Services configuration audit records must identify the source of the events. |
| AAA | `SRG-APP-000099-AAA-000260` | CAT II | AAA Services configuration audit records must identify the outcome of the events. |
| AAA | `SRG-APP-000100-AAA-000270` | CAT II | AAA Services configuration audit records must identify any individual user or process associated with the event. |
| AAA | `SRG-APP-000108-AAA-000290` | CAT II | AAA Services must be configured to alert the SA and ISSO when any audit processing failure occurs. |
| AAA | `SRG-APP-000116-AAA-000320` | CAT II | AAA Services must be configured to use internal system clocks to generate time stamps for audit records. |
| AAA | `SRG-APP-000141-AAA-000670` | CAT II | AAA Services must be configured to disable non-essential modules. |
| AAA | `SRG-APP-000142-AAA-000010` | CAT I | AAA Services must be configured to use secure protocols when connecting to directory services. |
| AAA | `SRG-APP-000142-AAA-000020` | CAT I | AAA Services must be configured to use protocols that encrypt credentials when authenticating clients, as defined in the PPSM CAL and vulnerability assessments. |
| AAA | `SRG-APP-000142-AAA-000680` | CAT II | AAA Services must be configured to prohibit or restrict the use of organization-defined functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. |
| AAA | `SRG-APP-000148-AAA-000390` | CAT I | AAA Services must be configured to uniquely identify and authenticate organizational users. |
| AAA | `SRG-APP-000149-AAA-000400` | CAT II | AAA Services must be configured to require multifactor authentication using Personal Identity Verification (PIV) credentials for authenticating privileged user accounts. |
| AAA | `SRG-APP-000150-AAA-000410` | CAT II | AAA Services must be configured to require multifactor authentication using common access card (CAC) Personal Identity Verification (PIV) credentials for authenticating nonprivileged user accounts. |
| AAA | `SRG-APP-000158-AAA-000420` | CAT II | AAA Services used for 802.1x must be configured to uniquely identify network endpoints (supplicants) before the authenticator establishes any connection. |
| AAA | `SRG-APP-000164-AAA-000450` | CAT II | AAA Services must be configured to enforce a minimum 15-character password length. |
| AAA | `SRG-APP-000166-AAA-000460` | CAT II | AAA Services must be configured to enforce password complexity by requiring that at least one uppercase character be used. |
| AAA | `SRG-APP-000167-AAA-000470` | CAT II | AAA Services must be configured to enforce password complexity by requiring that at least one lowercase character be used. |
| AAA | `SRG-APP-000168-AAA-000480` | CAT II | AAA Services must be configured to enforce password complexity by requiring that at least one numeric character be used. |
| AAA | `SRG-APP-000169-AAA-000490` | CAT II | AAA Services must be configured to enforce password complexity by requiring that at least one special character be used. |
| AAA | `SRG-APP-000170-AAA-000500` | CAT II | AAA Services must be configured to require the change of at least eight of the total number of characters when passwords are changed. |
| AAA | `SRG-APP-000171-AAA-000510` | CAT I | For password-based authentication, AAA Services must be configured to store passwords using an approved salted key derivation function, preferably using a keyed hash. |
| AAA | `SRG-APP-000172-AAA-000520` | CAT I | AAA Services must be configured to encrypt transmitted credentials using a FIPS-validated cryptographic module. |
| AAA | `SRG-APP-000173-AAA-000530` | CAT II | AAA Services must be configured to enforce 24 hours as the minimum password lifetime. |
| AAA | `SRG-APP-000174-AAA-000540` | CAT II | AAA Services must be configured to enforce a 180-day maximum password lifetime restriction. |
| AAA | `SRG-APP-000175-AAA-000570` | CAT I | AAA Services must be configured to only accept certificates issued by a DoW-approved certificate authority (CA) for Public Key Infrastructure (PKI)-based authentication. |
| AAA | `SRG-APP-000175-AAA-000580` | CAT I | AAA Services must be configured to not accept certificates that have been revoked for PKI-based authentication. |
| AAA | `SRG-APP-000176-AAA-000590` | CAT II | AAA Services must be configured to enforce authorized access to the corresponding private key for PKI-based authentication. |
| AAA | `SRG-APP-000177-AAA-000600` | CAT II | AAA Services must be configured to map the authenticated identity to the user account for PKI-based authentication. |
| AAA | `SRG-APP-000231-AAA-000610` | CAT I | AAA Services must be configured to protect the confidentiality and integrity of all information at rest. |
| AAA | `SRG-APP-000234-AAA-000060` | CAT II | AAA Services must be configured to prevent automatically removing emergency accounts. |
| AAA | `SRG-APP-000234-AAA-000070` | CAT III | AAA Services must be configured to prevent automatically disabling emergency accounts. |
| AAA | `SRG-APP-000291-AAA-000130` | CAT II | AAA Services must be configured to notify the system administrators (SAs) and information system security officer (ISSO) when accounts are created. |
| AAA | `SRG-APP-000292-AAA-000140` | CAT II | AAA Services must be configured to notify the system administrators (SAs) and information system security officer (ISSO) when accounts are modified. |
| AAA | `SRG-APP-000293-AAA-000150` | CAT II | AAA Services must be configured to notify the system administrators (SAs) and information system security officer (ISSO) for account disabling actions. |
| AAA | `SRG-APP-000294-AAA-000160` | CAT II | AAA Services must be configured to notify the system administrators (SAs) and information system security officer (ISSO) for account removal actions. |
| AAA | `SRG-APP-000319-AAA-000170` | CAT II | AAA Services must be configured to automatically audit account enabling actions. |
| AAA | `SRG-APP-000320-AAA-000180` | CAT II | AAA Services must be configured to notify system administrators (SAs) and information system security officer (ISSO) of account enabling actions. |
| AAA | `SRG-APP-000345-AAA-000210` | CAT II | AAA Services must be configured to maintain locks on user accounts until released by an administrator. |
| AAA | `SRG-APP-000358-AAA-000280` | CAT II | AAA Services must be configured to send audit records to a centralized audit server. |
| AAA | `SRG-APP-000374-AAA-000340` | CAT II | AAA Services must be configured to use or map to Coordinated Universal Time (UTC) to record time stamps for audit records. |
| AAA | `SRG-APP-000375-AAA-000330` | CAT II | AAA Services must be configured with a minimum granularity of one second to record time stamps for audit records. |
| AAA | `SRG-APP-000394-AAA-000430` | CAT II | AAA Services used for 802.1x must be configured to authenticate network endpoint devices (supplicants) before the authenticator establishes any connection. |
| AAA | `SRG-APP-000516-AAA-000350` | CAT III | AAA Services must be configured to use at least two NTP servers to synchronize time. |
| AAA | `SRG-APP-000516-AAA-000360` | CAT II | AAA Services must be configured to authenticate all NTP messages received from NTP servers and peers. |
| AAA | `SRG-APP-000516-AAA-000370` | CAT III | AAA Services must be configured to use their loopback or OOB management interface address as the source address when originating NTP traffic. |
| AAA | `SRG-APP-000516-AAA-000440` | CAT II | AAA Services used for 802.1x must be configured to use secure Extensible Authentication Protocol (EAP), such as EAP-TLS, EAP-TTLS, and PEAP. |
| AAA | `SRG-APP-000516-AAA-000620` | CAT II | AAA Services must not be configured with shared accounts. |
| AAA | `SRG-APP-000516-AAA-000630` | CAT II | AAA Services used to authenticate privileged users for device management must be configured to connect to the management network. |
| AAA | `SRG-APP-000516-AAA-000640` | CAT II | AAA Services must be configured to use a unique shared secret for communication (i.e. RADIUS, TACACS+) with clients requesting authentication services. |
| AAA | `SRG-APP-000516-AAA-000650` | CAT II | AAA Services must be configured to use IP segments separate from production VLAN IP segments. |
| AAA | `SRG-APP-000516-AAA-000660` | CAT II | AAA Services must be configured to place non-authenticated network access requests in the Unauthorized VLAN or the Guest VLAN with limited access. |
| AAA | `SRG-APP-000516-AAA-000690` | CAT II | AAA Services must be configured in accordance with the security configuration settings based on DoW security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. |
| AAA | `SRG-APP-000700-AAA-000100` | CAT II | AAA Services must be configured to disable accounts when the accounts have expired. |
| AAA | `SRG-APP-000705-AAA-000110` | CAT II | AAA Services must be configured to disable accounts when the accounts are no longer associated to a user. |
| AAA | `SRG-APP-000710-AAA-000120` | CAT II | AAA Services must be configured to disable accounts when the accounts are in violation of organizational policy. |
| AAA | `SRG-APP-000805-AAA-000130` | CAT II | AAA Services must be configured to automatically generate audit records of the enforcement actions. |
| AAA | `SRG-APP-000815-AAA-000140` | CAT II | AAA Services must be configured to require users to be individually authenticated before granting access to the shared accounts or resources. |
| AAA | `SRG-APP-000835-AAA-000150` | CAT II | For password-based authentication, AAA Services must be configured to update the list of passwords on an organization-defined frequency. |
| AAA | `SRG-APP-000840-AAA-000160` | CAT II | For password-based authentication, AAA Services must be configured to update the list of passwords when organizational passwords are suspected to have been compromised directly or indirectly. |
| AAA | `SRG-APP-000845-AAA-000170` | CAT II | For password-based authentication, AAA Services must be configured to verify when users create or update passwords, and that the passwords are not on the list of commonly-used, expected, or compromised passwords in IA-5 (1) (a). |
| AAA | `SRG-APP-000855-AAA-000190` | CAT II | For password-based authentication, AAA Services must be configured to require immediate selection of a new password upon account recovery. |
| AAA | `SRG-APP-000860-AAA-000200` | CAT II | For password-based authentication, AAA Services must be configured to allow user selection of long passwords and passphrases, including spaces and all printable characters. |
| AAA | `SRG-APP-000865-AAA-000210` | CAT II | For password-based authentication, AAA Services must be configured to employ automated tools to assist the user in selecting strong password authenticators. |
| AAA | `SRG-APP-000875-AAA-000220` | CAT II | For public key-based authentication, AAA Services must be configured to implement a local cache of revocation data to support path discovery and validation. |
| AAA | `SRG-APP-000910-AAA-000230` | CAT II | AAA Services must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
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
| NDM | `SRG-APP-000101-NDM-000231` | CAT II | The network device must generate audit records containing the full-text recording of privileged commands. |
| NDM | `SRG-APP-000120-NDM-000237` | CAT II | The network device must protect audit information from unauthorized deletion. |
| NDM | `SRG-APP-000131-NDM-000243` | CAT II | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| NDM | `SRG-APP-000142-NDM-000245` | CAT I | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services |
| NDM | `SRG-APP-000148-NDM-000346` | CAT II | The network device must be configured with only one local account to be used as the account of last resort in the event the authentication server is unavailable. |
| NDM | `SRG-APP-000149-NDM-000247` | CAT I | The network device must be configured to use DoD PKI as multi-factor authentication (MFA) for interactive logins. |
| NDM | `SRG-APP-000153-NDM-000249` | CAT II | The network device must be configured to authenticate each administrator prior to authorizing privileges based on assignment of group or role. |
| NDM | `SRG-APP-000156-NDM-000250` | CAT II | The network device must implement replay-resistant authentication mechanisms for network access to privileged accounts. |
| NDM | `SRG-APP-000164-NDM-000252` | CAT II | The network device must enforce a minimum 15-character password length. |
| NDM | `SRG-APP-000170-NDM-000329` | CAT II | The network device must require that when a password is changed, the characters are changed in at least eight of the positions within the password. |
| NDM | `SRG-APP-000171-NDM-000258` | CAT I | The network device must be configured to store passwords using an approved salted key derivation function, preferably using a keyed hash for password-based authentication. |
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
| NDM | `SRG-APP-000400-NDM-000313` | CAT II | The network device must prohibit the use of cached authenticators after an organization-defined time period. |
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

Run `get system license-info` on the CLI and keep the output, the
firmware version and serial number from the *System Information* widget,
and a configuration backup with the checklist. Add screenshots or exports
of the panes the map cites, above all *System > Network > Interfaces*,
*System > Administration > System Access*, *System > Administration >
High Availability*, *System > Administration > SNMP*, *Authentication >
User Account Policies > General*, *Authentication > User Account Policies
> Lockouts*, *Authentication > User Account Policies > Passwords*,
*Authentication > User Management > Local Users*, *Authentication > Remote
Auth. Servers > LDAP*, *Authentication > RADIUS Service > Clients*,
*Authentication > RADIUS Service > Policies*, *Authentication > TACACS+
Service > Clients*, *Certificate Management > Certificate Authorities >
Trusted CAs*, *Logging > Log Config > Log Settings*, and *Logging > Log
Config > Syslog Servers*. Download the user audit report from *Logging >
Audit Reports > Users Audit* (once with *Only include administrator &
sponsor accounts*), export the logs from the central log server, and keep
the firmware upgrade history and the backup schedule.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiAuthenticator.** Check
  the version column against the FortiAuthenticator release, and check
  whether the feature depends on the model, the platform, a license, or the
  node's role in an HA cluster (a load-balancing node synchronizes only
  some settings).
- **A setting is not where the map says.** The menus change between
  releases (the RADIUS service *Certificates* tab became *General* in
  6.6.3, the Fortinet SSO menus were reorganized in 6.6.1, and the RADIUS
  policy settings moved to authentication profiles in 8.0.2). Look for the
  setting under the older name, and check the Administration Guide of your
  release.
- **A command is rejected.** The commands were checked against the 8.0.3
  Administration Guide, because there is no CLI Reference. Use `?` on the
  CLI to list the options available at each level.
- **RADIUS clients are rejected after hardening.** Check that the client's
  source address matches the client entry, that the secret matches, that
  the client sends the Message-Authenticator attribute if it is required,
  that a policy matches the request's authentication type, and that the
  user is not locked out (*Monitor > Authentication > Locked-out Users*).
- **Logs do not reach the syslog server.** Check the server, port, level,
  and TLS settings under *Logging > Log Config > Syslog Servers*, that the
  server certificate is issued by the selected CA and (from 8.0.3) carries
  a valid hostname, and the path from FortiAuthenticator.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (checksum checks, account reviews), by another system (the
  directory, the central log server, the network devices, an upstream
  identity provider), or not at all. Record how each requirement is met,
  not just which feature covers it.

## Security and Best Practices

- Keep FortiAuthenticator on a vendor-supported release, and install
  patches promptly after checking the image checksum.
- Set the admin password at the first login, keep it as the one local
  account of last resort, and require a FortiToken for every other
  administrator, with the narrowest admin profile that works and trusted
  management subnets.
- Enable *Require strong cryptography*, the warning message before
  authentication with the DoD banner, a GUI and CLI idle timeout of 5
  minutes, and administrator IP lockout.
- Set password policies with a minimum length of 15 and all character
  types, enable enhanced cryptography for local passwords, and enable the
  user account lockout policy and inactive user lockout.
- Give every RADIUS and TACACS+ client its own secret, require the
  Message-Authenticator attribute, and use RADSEC and EAP-TLS where the
  clients support them.
- Trust only DoD CAs, keep CRLs current, and use LDAPS or STARTTLS to the
  directory.
- Run FortiAuthenticator as an HA cluster, send logs to two central
  servers over TLS, synchronize time with two authenticated DoD NTP
  servers, use SNMPv3 only, and back up the configuration with encryption
  to an SFTP server.
- Review this map each time Fortinet publishes a FortiAuthenticator release
  or DISA updates the AAA Services or NDM SRGs.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiAuthenticator Release Notes*, page "What's new",
  releases 6.6.0 to 6.6.11 and 8.0.0 to 8.0.3 (docs.fortinet.com,
  FortiAuthenticator documentation), and the 8.0.3 pages "Special notices",
  "Image checksums", and "Data-at-rest protection".
- Fortinet, *FortiAuthenticator 8.0.3 Administration Guide*.
- Fortinet, *FortiAuthenticator 6.6.0 Administration Guide* (for the core
  features).
- Fortinet, *FortiAuthenticator 8.0 Ports*.
- DISA Authentication, Authorization, and Accounting Services SRG V2R3 and
  Network Device Management SRG V5R5, from the October 2026 STIG Library
  Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map), and
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, the model for this chapter).

**Knowledge checks:**

1. Why is the AAA Services SRG the primary SRG for FortiAuthenticator, and
   what does the NDM SRG cover?
2. Where does the version data come from, and why are there only two
   release trains in the map?
3. How does administrator lockout differ from user account lockout on
   FortiAuthenticator, and how do you record the difference?
4. Which settings protect RADIUS and TACACS+ traffic, and which AAA
   requirements do they support?
5. Why does FortiAuthenticator's availability matter more than that of
   most devices, and which features address it?
6. Which requirements can FortiAuthenticator not meet exactly, and how do
   you handle them?

## Summary and Completion Checklist

FortiAuthenticator has no STIG, so it is assessed against the AAA Services
SRG as an authentication server and the NDM SRG for its management plane.
This chapter maps 198 features to the FortiAuthenticator release
that introduced them, to 140 SRG requirements, and to the
FortiAuthenticator GUI pane or command that configures them: 102
core platform features, and 96 features from the FortiAuthenticator
6.6.0 through 8.0.3 release notes. Operational features with no direct
requirement fall under the requirement to disable non-essential modules
when unused.

- [ ] Can find the release that introduced a FortiAuthenticator feature.
- [ ] Can map a FortiAuthenticator feature to its AAA or NDM SRG
  requirement.
- [ ] Can explain which SRG applies to the authentication services and
  which to the management plane.
- [ ] Can find the FortiAuthenticator GUI pane or command that meets the
  requirement.
- [ ] Can plan FortiAuthenticator's availability, collect its evidence,
  and record the requirements it cannot meet exactly.
