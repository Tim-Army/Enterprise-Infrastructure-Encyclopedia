# Chapter 16: FortiWeb Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiWeb OS release that introduced a given feature.
- Map each FortiWeb feature to the Application Layer Gateway (ALG) or
  Network Device Management (NDM) SRG requirement it helps satisfy.
- Find the FortiWeb CLI command that configures each feature to meet its
  requirement.
- Use the map to scope an SRG-based assessment of FortiWeb, which has no STIG
  of its own.
- Choose an operation mode that lets FortiWeb enforce the ALG requirements,
  not just report against them.
- Record the requirements that FortiWeb cannot meet exactly, with their
  mitigations.

## Theory and Architecture

FortiWeb is Fortinet's web application firewall (WAF). It has **no DISA
STIG** (Chapter 10), so it is assessed against SRGs, as described in Chapter
03. Chapter 10 assigns it two: the **Application Layer Gateway (ALG) SRG**
for the WAF itself, the proxy that inspects and filters HTTP and HTTPS
traffic to the protected web applications, and the **Network Device
Management (NDM) SRG** for the management plane, the way administrators log
in to and configure the appliance. For every FortiWeb feature the chapter
gives **which FortiWeb OS release introduced it**, **which requirement it
relates to**, and **which command configures it to meet that requirement**.

FortiWeb is built around a few objects. A **server policy** binds a virtual
server (the address clients connect to) to a server pool (the protected web
servers) and to a **web protection profile**, which names the protection
modules to apply: attack signatures, HTTP protocol constraints, IP
reputation, Geo IP, DoS prevention, bot mitigation, file security, input
validation, API protection, and the rest. Site Publish adds authentication
in front of an application. The protection depends on the **operation
mode**, which the 8.0.8 Administration Guide describes this way:

- **Reverse Proxy** (the default) and **True Transparent Proxy** terminate
  the client connection, inspect the request, and forward it, so FortiWeb
  can block a request, return a block page, and offload TLS.
- **Transparent Inspection** inspects traffic without terminating it; when
  it finds a violation it can only reset the connection, and it supports
  TLS 1.0 to 1.2 only.
- **Offline Protection** watches a copy of the traffic from a SPAN port and
  can only inject TCP resets through a separate blocking port.
- **WCCP** receives traffic redirected to it by a WCCP server, such as a
  FortiGate.

Only the proxy modes enforce the ALG requirements to block traffic and deny
by default. In Transparent Inspection and Offline Protection modes FortiWeb
is closer to a detection system, and the blocking requirements must be met
by another device in the path.

FortiWeb Cloud (the SaaS WAF) and FortiWeb Manager are separate products and
are not covered here. Several FortiWeb features use Fortinet or third-party
cloud services (FortiGuard Advanced Bot Protection, Threat Analytics,
FortiCloud single sign-on, FortiAnalyzer Cloud, FortiWeb Cloud Sandbox,
FortiAI, and Google reCAPTCHA); those services are outside the enclave and
are not assessed here, so use them only if they are authorized for your
environment.

### Where the version data comes from

Fortinet does not publish a feature matrix or a separate New Features Guide
for FortiWeb. The authoritative per-release list is the **"What's new"**
chapter of the **FortiWeb Administration Guide**, which the 7.6 and 8.0
Release Notes point to for their new features. It comes in two forms, and the version column was built
from both, covering all 60 FortiWeb releases Fortinet publishes for the 7.0
to 8.0 trains:

- **7.0, 7.2, and 7.4 trains.** Each release has its own Administration
  Guide, and its "What's new" page lists only the features of that release.
  The pages of all 40 releases were used: 7.0.0 through 7.0.12, 7.2.0
  through 7.2.12, and 7.4.0 through 7.4.13. For 7.2.1 and 7.4.5 the online
  "What's new" link opens an unrelated page (ZTNA troubleshooting), so the
  "What's new" section of the **FortiWeb 7.2.1 and 7.4.5 Release Notes**
  (PDF) was used instead.
- **7.6 and 8.0 trains.** From 7.6 the Administration Guide has one
  cumulative chapter per train, "New Features in 7.6.x releases" and "What's
  New", in which every feature title ends with the release that introduced
  it, for example "(7.6.3)". The chapters of the newest guides were used,
  the **FortiWeb 7.6.10 and 8.0.8 Administration Guides**, read from their
  online tables of contents, covering 7.6.0 through 7.6.10 and 8.0.0
  through 8.0.8. One title without a release (FortiWeb Hyper-V HA Cluster)
  was dated from its page, which gives 7.6.0.

Twenty-four of the 60 releases (7.0.6 through 7.0.12, 7.2.3, 7.2.4, 7.2.9
through 7.2.12, 7.4.5 through 7.4.7, 7.4.10 through 7.4.12, 7.6.6, 7.6.7,
8.0.2, 8.0.4, and 8.0.8) are patch releases with no new features, as their
"What's new" pages or Release Notes say.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that the requirements depend on: management
  access, administrator accounts and authentication, password and lockout
  policy, the login banner, logging, time, SNMP, FIPS-CC mode, firmware and
  backups, high availability, and the WAF itself (server policies, web
  protection profiles, and the main protection modules). They existed before
  FortiWeb 7.0.0 and are not in any of these "What's new" lists; they were
  taken from the FortiWeb 8.0.8 CLI Reference and Administration Guide.
- **New features** are the 417 entries of the "What's new" lists.
  The 7.0 to 7.4 pages have no categories, and the 7.6 and 8.0 categories
  are broad, so the categories were assigned for this chapter, and some
  titles were lightly edited for clarity. An entry listed again in a later
  release or train is one row with both versions: the HTTP/2 RST_STREAM
  check, for example, is listed in 7.2.5, 7.2.6, 7.2.7, and 7.4.1, and the
  HTTP/2 and HTTP/3 constraint hardening in 7.4.13, 7.6.9, and 8.0.6.

| Version entry | Meaning |
| --- | --- |
| `7.0.0 or earlier` | A core feature that predates the oldest "What's new" list used (FortiWeb 7.0.0) |
| `7.4.1 and later` | Introduced in FortiWeb OS 7.4.1 |
| `7.2.5+; 7.4.1+` | Listed in two trains: from 7.2.5 in the 7.2 train and from 7.4.1 in the 7.4 train |

Four cautions apply. First, the version is the **FortiWeb OS** release, and
a feature introduced in a patch release of an older train may reach a newer
train only in a later patch, so "and later" means later in the same train
and, usually, in later trains. Second, the version follows the page that
lists the feature: the 7.4.4 page, for example, lists two settings that it
says are available from 7.6.0 (the traffic packet size and the per-policy
SSL error log). Third, many features apply only to some platforms (hardware
models, FortiWeb-VM, or one public cloud). Fourth, a core row records a
FortiWeb capability, but its command was checked against the 8.0.8 CLI
Reference and may differ on an older release; several settings it uses
arrived later, and the new-feature rows say when (for example NTP
authentication in 7.6.1, SNMPv3 SHA-2 in 7.6.1, and `default-admin` in
8.0.3).

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG column | SRG | Release | Applies to |
| --- | --- | --- | --- |
| **ALG** | Application Layer Gateway SRG | V2R4, benchmark date 01 Jul 2026 | The WAF function: inspection, filtering, and blocking of web traffic, TLS to clients and servers, user authentication through Site Publish, and the attack logs (assigned by Chapter 10) |
| **NDM** | Network Device Management SRG | V5R5, benchmark date 01 Jul 2026 | The management plane: administrator access, authentication, logging, time, SNMP, firmware, and backups (assigned by Chapter 10) |

The ALG SRG is written for every kind of application layer gateway, so not
all of it applies. The requirements for an ALG that is part of a cross-domain
solution (CDS) do not apply to FortiWeb. The requirements for "user access
control" and "user authentication intermediary services" apply only when
FortiWeb authenticates users, which it does through Site Publish. The
content filtering requirements (code injection, SQL injection, malicious
code, DoS) are the core of a WAF assessment.

The requirement IDs are the **rule version IDs** from the XCCDF files, and
the severity is the rule's severity (high = CAT I, medium = CAT II, low =
CAT III). Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiWeb meets a
  requirement. Syntax-based detection implements the requirements to detect
  and prevent SQL injection (ALG `SRG-NET-000319-ALG-000020` and
  `SRG-NET-000318-ALG-000152`), for example.
- **Must be configured to meet a requirement.** The feature is in scope of a
  requirement and has to be set up correctly. HTTPS offloading must use TLS
  1.2 or later with approved ciphers (ALG `SRG-NET-000062-ALG-000150`), for
  example.
- **No direct requirement.** The feature is operational, such as a cloud
  platform, a license, a dashboard, or a load-balancing option. It has no
  requirement of its own, but if it is not needed it falls under the ALG
  requirement not to have unnecessary services and functions enabled (ALG
  `SRG-NET-000131-ALG-000085`); for a management-plane function the NDM
  equivalent is NDM `SRG-APP-000142-NDM-000245`.

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially where a requirement is organization-defined or
depends on how FortiWeb is deployed.

### Where the commands come from

Every command was checked against the **FortiWeb 8.0.8 CLI Reference**, the
newest CLI Reference Fortinet publishes for FortiWeb, and every web UI pane
named in the table against the **FortiWeb 8.0.8 Administration Guide**. The
check was automatic: each `config` path and nested table, each `set` option
against the syntax and examples of the command it is entered under, each
listed option value against the documented values, each `execute` command,
and each GUI pane name. Read the column this way:

- Commands run on the FortiWeb CLI, over SSH or the console. Most WAF
  settings live in a web protection profile
  (`config waf web-protection-profile inline-protection`) or a server policy
  (`config server-policy policy`); `<PROFILE>` and `<POLICY>` are their
  names.
- The CLI Reference prints some keywords in upper case, such as `HTTPS` in
  `set allowaccess HTTPS ssh` and `HTTP` in
  `HTTP-protocol-parameter-restriction`; the commands are given as the
  reference prints them. Check the spelling with `?` on the CLI of your
  release.
- **GUI:** entries name the FortiWeb web UI pane.
- Statements are separated by `;` to fit in a table cell; on the CLI, enter
  each one on its own line. Values in `<ANGLE_BRACKETS>` are placeholders for
  your own names, addresses, and keys.
- For **"No direct requirement"** rows, the command shown is the one that
  disables the feature when it is unused. A dash (**—**) means there is
  nothing to change: the feature is a platform, a license, a performance or
  GUI change, or a capability that is off unless configured.

Some requirements cannot be met exactly with FortiWeb settings. Record them
on the checklist as open findings with mitigations, or meet them another way:

- **Lockout duration unit.** `admin-lockout-threshold` accepts 1 to 10
  attempts (set 3). The CLI Reference names the `admin-lockout-duration`
  value in minutes but describes its range in seconds, with a default of 60
  (NDM `SRG-APP-000065-NDM-000214`). The table sets 900, which is at least
  15 minutes under either reading; confirm the unit on your release.
- **Concurrent sessions.** There is no per-account session limit. The only
  control is single administrator mode in the password policy, which allows
  one administrator to be logged in at a time (NDM
  `SRG-APP-000001-NDM-000200`). Use it, or define the limit as one session
  through remote authentication and procedure.
- **Password rules.** The password policy sets length (8 to 128) and
  character classes, but there is no rule that a new password must change
  at least eight characters (NDM `SRG-APP-000170-NDM-000329`), and the
  administrator password is limited to 32 characters, which bounds long
  passphrases (NDM `SRG-APP-000860-NDM-000250`). Record the finding, and
  prefer PKI or remote authentication for administrators.
- **NTP authentication.** NTP authentication and multiple NTP servers arrive
  in 7.6.1 (NDM `SRG-APP-000395-NDM-000347`). On older releases use an
  internal time source on a protected path and record the finding.
- **SNMPv3 algorithms.** SHA-2 authentication and AES-256 privacy arrive in
  7.6.1; older releases offer SHA-1 or MD5 and AES or DES (NDM
  `SRG-APP-000395-NDM-000310`). Use SHA-1 with AES there, or disable SNMP.
- **Firmware signatures.** The Administration Guide verifies firmware by
  comparing an MD5 checksum from the Fortinet support site, checks image
  integrity when an image is loaded from the boot menu, and verifies VM
  image signatures at boot; there is no setting that requires a signed image
  before installation (NDM `SRG-APP-000131-NDM-000243`). Verify the checksum
  by procedure before every upgrade.
- **Weak TLS signature algorithms.** The 7.6.4 Administration Guide
  documents `restrict-weak-sign-algo` under `config server-policy setting`
  to refuse SHA-1 and SHA-224 signatures, but the 8.0.8 CLI Reference does
  not list it (ALG `SRG-NET-000062-ALG-000150`). Check for it on your
  release; in FIPS-CC mode those algorithms are already refused.
- **Geo IP Allow Mode.** The 7.4.8 Allow Mode (deny every region not listed)
  has no setting in the 8.0.8 CLI Reference; configure it in the web UI.
- **FIPS 140 validation.** FIPS-CC mode restricts the ciphers, and
  `fips-ciphers` mode is available only on FortiWeb-VM in AWS and Azure (NDM
  `SRG-APP-000179-NDM-000265`, ALG `SRG-NET-000510-ALG-000111`). Check the
  NIST Cryptographic Module Validation Program for a current certificate
  for your FortiWeb release before relying on its cryptography.
- **Banner for users.** The pre-login disclaimer covers administrators.
  For users, FortiWeb can show the DoD banner only on the pages it serves
  itself, the Site Publish login pages (ALG `SRG-NET-000041-ALG-000022`); for
  applications without Site Publish, the application must display it.
- **Monitoring-only modes.** In Offline Protection and Transparent
  Inspection modes FortiWeb can only reset connections (ALG
  `SRG-NET-000202-ALG-000124` and `SRG-NET-000019-ALG-000018`). Deploy in
  Reverse Proxy or True Transparent Proxy mode, or meet the blocking
  requirements with another device.

## Design Considerations

- **Pick a proxy operation mode.** Reverse Proxy, or True Transparent Proxy
  where addresses cannot change, lets FortiWeb block, deny by default with
  protected host names, and offload TLS. Keep monitor mode off in production
  server policies.
- **Pick the release first, then the features.** If your design depends on a
  feature introduced in a certain release (for example NTP authentication
  and SNMPv3 SHA-2 in 7.6.1, PBKDF2 password hashing and disabling the
  default admin account in 8.0.3, or configuration file encryption in
  8.0.7), that sets the minimum FortiWeb OS release, and it must be a
  vendor-supported release (NDM `SRG-APP-001035-NDM-000340`).
- **Separate management from data.** Allow HTTPS and SSH only on a dedicated
  management interface, never on the interfaces that carry web traffic,
  restrict administrators with trusted hosts and the firewall admin policy,
  and keep shell access disabled.
- **Use DoD PKI for administrators and users.** Use certificate-based web UI
  login (PKI users in an administrator group) or a remote authentication
  server for administrators, with one local account of last resort; for
  users, verify client certificates against the DoD CAs with CRL or OCSP
  checking.
- **Build a strict web protection profile.** Combine attack signatures,
  syntax-based detection, HTTP protocol constraints, allowed methods,
  protected host names, IP reputation, DoS prevention, file security, and
  input validation, and set their actions to block rather than alert once
  tuning is complete.
- **Turn off what is not used.** Cloud services that are not authorized,
  the web vulnerability scanner, FortiCloud administrator login, threat
  telemetry, shell access, the configuration synchronization port, and SNMP
  v1 and v2c are all functions that need a reason to stay on.

## Implementation and Automation

### The FortiWeb feature map

The SRG column uses the abbreviations defined in *Where the SRG data comes
from*. The requirement titles are listed in the next table. The command
column follows the conventions in *Where the commands come from*.

| Category | Feature | Introduced (FortiWeb OS) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: Management access | Management access per interface (HTTPS, SSH, ping, SNMP, HTTP, Telnet) | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000172-NDM-000259` | `config system interface; edit <MGMT_PORT>; set allowaccess HTTPS ssh; next; end` (management interface only; leave out HTTP and Telnet) |
| Core: Management access | Web UI TLS versions and cipher suites | 7.0.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000179-NDM-000265` | `config system global; set admin-tls-v10 disable; set admin-tls-v11 disable; set admin-tls-v12 enable; set admin-tls-v13 enable; end` |
| Core: Management access | Web UI server certificate | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000344`; NDM `SRG-APP-000910-NDM-000300` | `config system global; set HTTPS-certificate <DOD_ISSUED_ADMIN_CERT>; end` |
| Core: Management access | Administrative HTTP and HTTPS ports | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Management access | Trusted hosts for each administrator | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213` | `config system admin; edit <ADMIN>; set trusthosts <MGMT_SUBNET>; next; end` |
| Core: Management access | Console port | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314` | — (physical access control; the console requires an administrator login) |
| Core: Management access | Idle timeout for web UI and CLI sessions | 7.0.0 or earlier | NDM `SRG-APP-000190-NDM-000267` | `config system global; set admintimeout 10; end` |
| Core: Management access | Pre-login disclaimer (login banner) | 7.0.0 or earlier | NDM `SRG-APP-000068-NDM-000215` | `config system global; set pre-login-banner enable; end` (banner text under System > Config > Replacement Message, Disclaimer tab) |
| Core: Administrator accounts | Local administrator accounts | 7.0.0 or earlier | NDM `SRG-APP-000148-NDM-000346`; NDM `SRG-APP-000153-NDM-000249` | `config system admin; edit <ADMIN>; set type local-user; set access-profile <PROFILE>; set password <PASSWORD_15_CHARS_MIN>; next; end` |
| Core: Administrator accounts | Access profiles (none, read, write, or read-write per permission group) | 7.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000380-NDM-000304` | `config system accprofile; edit <PROFILE>; set admingrp r; set sysgrp r; set loggrp r; next; end` |
| Core: Administrator accounts | Administrative domains (ADOMs) | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Administrator accounts | Password policy (length and character classes) | 7.0.0 or earlier | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000166-NDM-000254`; NDM `SRG-APP-000167-NDM-000255`; NDM `SRG-APP-000168-NDM-000256`; NDM `SRG-APP-000169-NDM-000257` | `config system password-policy; set status enable; set min-length-option enable; set mini-length 15; set character-requirements enable; set min-upper-case-letter 1; set min-lower-case-letter 1; set mini-number 1; set min-non-alphanumeric 1; end` |
| Core: Administrator accounts | Administrator login lockout | 7.0.0 or earlier | NDM `SRG-APP-000065-NDM-000214` | `config system global; set admin-lockout-threshold 3; set admin-lockout-duration 900; end` |
| Core: Administrator accounts | Single administrator mode (one administrator logged in at a time) | 7.0.0 or earlier | NDM `SRG-APP-000001-NDM-000200` | `config system password-policy; set single-admin-mode enable; end` |
| Core: Administrator accounts | Remote administrator authentication (RADIUS, LDAP, TACACS+) through administrator groups | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000148-NDM-000346` | `config user ldap-user; edit <LDAP>; set server <LDAP_SERVER>; set ssl-connection enable; set protocol ldaps; set ca-cert <CA_CERT>; next; end`; `config user admin-usergrp; edit <GROUP>; config members; edit 1; set type ldap; set ldap-name <LDAP>; next; end; next; end`; `config system admin; edit <ADMIN>; set type remote-user; set admin-usergroup <GROUP>; next; end` |
| Core: Administrator accounts | Certificate-based (PKI) web UI login for administrators | 7.0.0 or earlier | NDM `SRG-APP-000149-NDM-000247`; NDM `SRG-APP-000177-NDM-000263`; NDM `SRG-APP-000175-NDM-000262`; NDM `SRG-APP-000875-NDM-000280` | `config user pki-user; edit <PKI_USER>; set cacert <DOD_CA_CERT>; set subject <SUBJECT>; next; end`; `config user admin-usergrp; edit <GROUP>; config members; edit 1; set type pki; next; end; next; end`; `config system global; set admin-HTTPS-pki-required enable; end` |
| Core: Administrator accounts | Administrator two-factor authentication (token code) | 7.0.0 or earlier | NDM `SRG-APP-000820-NDM-000170` | `config system global; set multi-factor-authentication mandatory; end` |
| Core: Logging | Event log (administrator logins, configuration changes, system events) | 7.0.0 or earlier | NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000505-NDM-000322`; NDM `SRG-APP-000380-NDM-000304` | `config log event-log; set status enable; end`; `config log disk; set status enable; set severity information; end` |
| Core: Logging | Event log of failed CLI commands | 7.0.0 or earlier | NDM `SRG-APP-000101-NDM-000231` | `config system global; set record-cli-fail-cmd enable; end` |
| Core: Logging | Attack log (WAF detections with source, URL, policy, and action) | 7.0.0 or earlier | ALG `SRG-NET-000074-ALG-000043`; ALG `SRG-NET-000077-ALG-000046`; ALG `SRG-NET-000079-ALG-000048`; ALG `SRG-NET-000503-ALG-000038` | `config log attack-log; set status enable; end` |
| Core: Logging | Traffic log | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config log traffic-log; set status disable; end` |
| Core: Logging | Remote syslog servers (syslog policies, TLS) | 7.0.0 or earlier | NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000516-NDM-000350`; ALG `SRG-NET-000334-ALG-000050`; ALG `SRG-NET-000511-ALG-000051` | `config log syslog-policy; edit <SYSLOG_POLICY>; config syslog-server-list; edit 1; set server <SYSLOG_SERVER>; set proto tls; next; end; next; end`; `config log syslogd; set status enable; set policy <SYSLOG_POLICY>; end` |
| Core: Logging | Logging to FortiAnalyzer | 7.0.0 or earlier | NDM `SRG-APP-000515-NDM-000325`; ALG `SRG-NET-000334-ALG-000050` | `config log forti-analyzer; set status enable; set fortianalyzer-policy <FAZ_POLICY>; end` |
| Core: Logging | Alert email | 7.0.0 or earlier | NDM `SRG-APP-000360-NDM-000295`; ALG `SRG-NET-000088-ALG-000054`; ALG `SRG-NET-000392-ALG-000141` | `config log alertMail; set status enable; set email-policy <EMAIL_POLICY>; end` |
| Core: Logging | Log disk usage threshold event | 7.0.0 or earlier | NDM `SRG-APP-000357-NDM-000293`; NDM `SRG-APP-000360-NDM-000295`; ALG `SRG-NET-000335-ALG-000053` | `config log event-log; set logdisk-high 80; end` |
| Core: Logging | Log access restricted by access profile (log permission group) | 7.0.0 or earlier | NDM `SRG-APP-000231-NDM-000271`; ALG `SRG-NET-000098-ALG-000056` | `config system accprofile; edit <PROFILE>; set loggrp r; next; end` |
| Core: Time | System time and NTP synchronization | 7.0.0 or earlier | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000374-NDM-000299` | `config system ntp; set ntpsync enable; config ntp-server; edit 1; set server <NTP_SERVER>; next; end; end` |
| Core: SNMP | SNMP v1 and v2c communities | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000395-NDM-000310` | `config system snmp community; edit <ID>; set status disable; next; end` |
| Core: SNMP | SNMPv3 users and traps | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310` | `config system snmp user; edit <SNMP_USER>; set status enable; set security-level authpriv; set auth-proto sha256; set auth-pwd <AUTH_PASSWORD>; set priv-proto aes256; set priv-pwd <PRIV_PASSWORD>; next; end` |
| Core: Cryptography | FIPS-CC mode | 7.0.0 or earlier | NDM `SRG-APP-000179-NDM-000265`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; ALG `SRG-NET-000510-ALG-000111`; ALG `SRG-NET-000510-ALG-000025`; ALG `SRG-NET-000575-ALG-000020` | `config system fips-cc; set status enable; end` |
| Core: Firmware and configuration | Firmware upgrade (web UI, TFTP, or FTP) | 7.0.0 or earlier | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000131-NDM-000243` | `execute restore image tftp <IMAGE> <TFTP_SERVER>` (after checking the image checksum) |
| Core: Firmware and configuration | Configuration backup (manual and scheduled, encrypted) | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340` | `config system backup; edit <BACKUP>; set config-type full-config; set encryption enable; set encryption-passwd <PASSWORD>; set protocol-type sftp; set ftp-server <SERVER>; set schedule_type days; next; end` |
| Core: Firmware and configuration | FortiGuard updates (attack signatures, IP reputation, antivirus, bots) | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000019`; ALG `SRG-NET-000246-ALG-000132`; NDM `SRG-APP-000142-NDM-000245` | `config system autoupdate schedule; set status enable; set frequency every; end` |
| Core: Firmware and configuration | Configuration synchronization between FortiWeb appliances | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Certificates | Server and CA certificates (Server Objects > Certificates) | 7.0.0 or earlier | ALG `SRG-NET-000750-ALG-000140`; ALG `SRG-NET-000755-ALG-000150` | GUI: Server Objects > Certificates > Local |
| Core: High availability | HA clusters (active-passive and active-active) | 7.0.0 or earlier | ALG `SRG-NET-000365-ALG-000123`; ALG `SRG-NET-000362-ALG-000120` | `config system ha; set mode active-passive; set encryption enable; set key <HA_KEY>; end` |
| Core: High availability | Fail-open bypass ports (hardware models) | 7.0.0 or earlier | ALG `SRG-NET-000235-ALG-000118`; ALG `SRG-NET-000365-ALG-000123` | `config system fail-open; set port3-port4 poweroff-cutoff; end` |
| Core: Deployment | Operation modes (reverse proxy, transparent proxy, transparent inspection, offline protection, WCCP) | 7.0.0 or earlier | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000019-ALG-000018` | `config system settings; set opmode reverse-proxy; end` |
| Core: Deployment | Integrated firewall (System > Firewall) | 7.0.0 or earlier | NDM `SRG-APP-000038-NDM-000213`; ALG `SRG-NET-000202-ALG-000124` | `config system firewall firewall-policy; set default-action deny; end` |
| Core: Server policies | Server policies, virtual servers, and server pools | 7.0.0 or earlier | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000362-ALG-000120` | `config server-policy policy; edit <POLICY>; set vserver <VSERVER>; set server-pool <POOL>; set web-protection-profile <PROFILE>; set status enable; next; end` |
| Core: Server policies | Monitor mode (log without blocking) | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000202-ALG-000124` | `config server-policy policy; edit <POLICY>; set monitor-mode disable; next; end` |
| Core: Server policies | Protected host names | 7.0.0 or earlier | ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000202-ALG-000124` | `config server-policy allow-hosts; edit <HOSTS>; set default-action deny; config host-list; edit 1; set host <FQDN>; set action allow; next; end; next; end` |
| Core: Server policies | HTTPS offloading: TLS versions and cipher suites on the client side | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000510-ALG-000111` | `config server-policy policy; edit <POLICY>; set ssl enable; set tls-v10 disable; set tls-v11 disable; set tls-v12 enable; set tls-v13 enable; set ssl-cipher high; next; end` |
| Core: Server policies | TLS to back-end servers and server certificate verification | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000164-ALG-000100` | `config server-policy server-pool; edit <POOL>; config pserver-list; edit <ID>; set ssl enable; set server-certificate-verify enable; set server-certificate-verify-policy <VERIFIER>; next; end; next; end` |
| Core: Server policies | Client certificate verification (CA, CRL, and OCSP) | 7.0.0 or earlier | ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000166-ALG-000101`; ALG `SRG-NET-000355-ALG-000117`; ALG `SRG-NET-000345-ALG-000099` | `config system certificate verify; edit <VERIFIER>; set ca <DOD_CA_GROUP>; set crl <CRL_GROUP>; set strictly-need-cert enable; next; end`; `config server-policy policy; edit <POLICY>; set ssl-client-verify <VERIFIER>; next; end` |
| Core: Server policies | HTTP to HTTPS redirect and HSTS | 7.0.0 or earlier | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000230-ALG-000113` | `config server-policy policy; edit <POLICY>; set HTTP-to-HTTPS enable; set hsts-header enable; next; end` |
| Core: Server policies | TCP SYN flood protection (SYN cookies) | 7.0.0 or earlier | ALG `SRG-NET-000705-ALG-000110`; ALG `SRG-NET-000362-ALG-000112` | `config server-policy policy; edit <POLICY>; set syncookie enable; set half-open-threshold <PACKETS>; next; end` |
| Core: Server policies | Server health checks and load balancing | 7.0.0 or earlier | ALG `SRG-NET-000362-ALG-000120`; ALG `SRG-NET-000365-ALG-000123` | `config server-policy server-pool; edit <POOL>; set health <HEALTH_CHECK>; set lb-algo round-robin; next; end` |
| Core: Server policies | Replacement messages (block and error pages) | 7.0.0 or earlier | ALG `SRG-NET-000273-ALG-000129`; ALG `SRG-NET-000402-ALG-000130` | GUI: System > Config > Replacement Message |
| Core: Web protection | Web protection profiles | 7.0.0 or earlier | ALG `SRG-NET-000018-ALG-000017`; ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000512-ALG-000062` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set signature-rule <SIGNATURE_POLICY>; set HTTP-protocol-parameter-restriction <CONSTRAINTS>; set ip-intelligence enable; next; end` |
| Core: Web protection | Attack signatures (SQL injection, XSS, generic attacks, known exploits, trojans, information disclosure) | 7.0.0 or earlier | ALG `SRG-NET-000318-ALG-000152`; ALG `SRG-NET-000319-ALG-000020`; ALG `SRG-NET-000318-ALG-000014`; ALG `SRG-NET-000319-ALG-000015`; ALG `SRG-NET-000318-ALG-000151`; ALG `SRG-NET-000319-ALG-000153` | `config waf signature; edit <SIGNATURE_POLICY>; config main_class_list; edit 010000000; set action alert_deny; next; end; next; end`; `config waf web-protection-profile inline-protection; edit <PROFILE>; set signature-rule <SIGNATURE_POLICY>; next; end` |
| Core: Web protection | Custom signatures and custom policies | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000018-ALG-000017` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set custom-access-policy <CUSTOM_POLICY>; next; end` |
| Core: Web protection | HTTP protocol constraints | 7.0.0 or earlier | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000380-ALG-000128` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set HTTP-protocol-parameter-restriction <CONSTRAINTS>; next; end` |
| Core: Web protection | Allowed HTTP methods | 7.0.0 or earlier | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000132-ALG-000087` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set allow-method-policy <METHOD_POLICY>; next; end` |
| Core: Web protection | URL access rules | 7.0.0 or earlier | ALG `SRG-NET-000015-ALG-000016`; ALG `SRG-NET-000202-ALG-000124` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set url-access-policy <URL_ACCESS_POLICY>; next; end` |
| Core: Web protection | Parameter validation (input rules) and hidden field protection | 7.0.0 or earlier | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000380-ALG-000128` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set parameter-validation-rule <INPUT_RULES>; set hidden-fields-protection <HIDDEN_FIELDS>; next; end` |
| Core: Web protection | XML and JSON protection | 7.0.0 or earlier | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000380-ALG-000128` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set xml-validation-policy <XML_POLICY>; set json-validation-policy <JSON_POLICY>; next; end` |
| Core: Web protection | Cookie security (signing or encryption, Secure and HttpOnly flags) | 7.0.0 or earlier | ALG `SRG-NET-000230-ALG-000113`; ALG `SRG-NET-000233-ALG-000115` | `config waf cookie-security; edit <COOKIE_POLICY>; set cookie-value-security signed; set secure-cookie enable; set HTTP-only enable; set action alert_deny; next; end`; `config waf web-protection-profile inline-protection; edit <PROFILE>; set cookie-security-policy <COOKIE_POLICY>; next; end` |
| Core: Web protection | Cross-site request forgery (CSRF) protection | 7.0.0 or earlier | ALG `SRG-NET-000230-ALG-000113` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set csrf-protection <CSRF_RULE>; next; end` |
| Core: Web protection | Man-in-the-browser (MiTB) protection | 7.0.0 or earlier | ALG `SRG-NET-000230-ALG-000113`; ALG `SRG-NET-000228-ALG-000108` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set mitb-protection <MITB_POLICY>; next; end` |
| Core: Web protection | Padding oracle protection | 7.0.0 or earlier | ALG `SRG-NET-000230-ALG-000113` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set padding-oracle <PADDING_ORACLE_RULE>; next; end` |
| Core: Web protection | HTTP header security (security response headers) | 7.0.0 or earlier | ALG `SRG-NET-000228-ALG-000108`; ALG `SRG-NET-000288-ALG-000109` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set HTTP-header-security <HEADER_SECURITY_POLICY>; next; end` |
| Core: Web protection | File upload restrictions, antivirus, and FortiSandbox | 7.0.0 or earlier | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000249-ALG-000134`; ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000249-ALG-000146` | `config waf file-upload-restriction-policy; edit <FILE_POLICY>; set av-scan enable; set trojan-detection enable; set action alert_deny; next; end`; `config waf web-protection-profile inline-protection; edit <PROFILE>; set file-upload-policy <FILE_POLICY>; next; end` |
| Core: Access control | IP reputation (FortiGuard IP intelligence) | 7.0.0 or earlier | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000392-ALG-000142` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set ip-intelligence enable; next; end` |
| Core: Access control | IP lists (trusted, blocked, and allow-only addresses) | 7.0.0 or earlier | ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000202-ALG-000124` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set ip-list-policy <IP_LIST>; next; end` |
| Core: Access control | Geo IP blocking | 7.0.0 or earlier | ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000019-ALG-000018` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set geo-block-list-policy <GEO_POLICY>; next; end` |
| Core: DoS protection | Application-layer and network-layer DoS prevention | 7.0.0 or earlier | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000362-ALG-000155`; ALG `SRG-NET-000705-ALG-000110`; ALG `SRG-NET-000392-ALG-000148` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set application-layer-dos-prevention <DOS_POLICY>; next; end` |
| Core: Bot mitigation | Bot mitigation (known bots, threshold-based, biometrics-based, and bot deception) | 7.0.0 or earlier | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000390-ALG-000139` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set bot-mitigate-policy <BOT_POLICY>; next; end` |
| Core: Machine learning | Machine-learning anomaly detection | 7.0.0 or earlier | ALG `SRG-NET-000319-ALG-000153`; ALG `SRG-NET-000390-ALG-000139` | `config waf machine-learning-policy; edit <ID>; set status enable; set action-anomaly alert_deny; next; end` |
| Core: Authentication | Site Publish (authentication offloading and single sign-on for users) | 7.0.0 or earlier | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000138-ALG-000088`; ALG `SRG-NET-000400-ALG-000097`; ALG `SRG-NET-000339-ALG-000090` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set site-publisher-helper <SITE_PUBLISH_POLICY>; next; end` |
| Core: Authentication | Site Publish login pages (replacement messages) | 7.0.0 or earlier | ALG `SRG-NET-000041-ALG-000022` | GUI: System > Config > Replacement Message |
| Core: Authentication | User tracking (session and login monitoring) | 7.0.0 or earlier | ALG `SRG-NET-000213-ALG-000107`; ALG `SRG-NET-000517-ALG-000006`; ALG `SRG-NET-000503-ALG-000038` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set user-tracking-policy <USER_TRACKING_POLICY>; next; end` |
| Core: Access control | X-Forwarded-For and original client IP handling | 7.0.0 or earlier | ALG `SRG-NET-000077-ALG-000046`; ALG `SRG-NET-000735-ALG-000130` | `config waf x-forwarded-for; edit <XFF_RULE>; set block-based-on-original-ip enable; config ip-list; edit 1; set ip <TRUSTED_PROXY_IP>; next; end; next; end`; `config waf web-protection-profile inline-protection; edit <PROFILE>; set x-forwarded-for-rule <XFF_RULE>; next; end` |
| Core: FTP security | FTP security (FTP command restriction and file checks) | 7.0.0 or earlier | ALG `SRG-NET-000512-ALG-000065` | `config server-policy policy; edit <POLICY>; set ftp-protection-profile <FTP_PROFILE>; next; end` |
| Core: Application delivery | Caching, compression, URL rewriting, and acceleration | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Core: Vulnerability scanning | Web vulnerability scanner | 7.0.0 or earlier | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config system feature-visibility; set wvs disable; end` |
| API protection | Machine-learning-based API discovery and protection | 7.0.0 and later | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000319-ALG-000153` | `config waf api-learning-policy; edit <ID>; set status enable; set action-mlapi alert_deny; next; end` |
| GUI | Dashboard widgets and FortiView enhancements (Monitor and FortiView tabs removed) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| WAF actions | Client ID Block Period action (block a client by its FortiWeb client ID instead of its source IP) | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018` | — (an action value offered by the WAF modules) |
| Logging and monitoring | Blocking source IP addresses directly from FortiView | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018` | — (an action in FortiView) |
| Authentication | OAuth 2.0 front-end authentication in Site Publish | 7.0.0 and later | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000138-ALG-000088` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set site-publisher-helper <SITE_PUBLISH_POLICY>; next; end` |
| Signatures | Personally identifiable information signature dictionary in custom rules | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | Credential stuffing defense with the FortiGuard online database | 7.0.0 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000392-ALG-000142` | `config waf user-tracking rule; edit <RULE>; set credential-stuffing-protection enable; next; end` |
| Signatures | Exceptions in syntax-based SQL injection and XSS detection and in bot mitigation | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | Default route priorities (system, HA static, and DHCP routes) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | Multiple wildcard administrator users | 7.0.0 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249` | `config system admin; edit <ADMIN>; set type remote-user; set wildcard enable; set admin-usergroup <GROUP>; next; end` |
| Management access | Shell access over SSH | 7.0.0 and later | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000408-NDM-000314` | `config system global; set shell-access disable; end` |
| Certificates and TLS | SafeNet Network HSM high-availability group | 7.0.0 and later | ALG `SRG-NET-000755-ALG-000150` | — |
| Authentication | LDAP server health check | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — (no ldap-health option found in the 8.0.8 CLI Reference) |
| Logging | Configuration change event logging enhancement | 7.0.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000095-NDM-000225` | `config log event-log; set status enable; end` |
| Logging | Traffic logging off by default (generated only for server policies that enable it) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config log traffic-log; set status disable; end` |
| Licensing | VM16 license (up to 16 vCPUs) | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cloud and VM | FortiWeb-VM on OpenStack license file import method | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cloud and VM | OpenStack Wallaby support | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cloud and VM | FortiWeb-VM in multiple shared back-end pools behind an Azure load balancer | 7.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Access control | Geo IP, IP list, and IP reputation checks at the TCP layer, with Deny (no log) and Period Block actions | 7.0.0 and later | ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000019-ALG-000018` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set ip-list-policy <IP_LIST>; set geo-block-list-policy <GEO_POLICY>; set ip-intelligence enable; next; end` |
| Web protection | Link cloaking | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Access control | Parameter and value data type checks in URL access rules | 7.0.1 and later | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000015-ALG-000016` | `config waf url-access-rule; edit <RULE>; config match-condition; edit 1; set url-access-parameter <PARAMETER_RULE>; next; end; next; end` |
| Custom rules | Custom rule enhancements: Basic Authorization header check, and request and response filters in one rule | 7.0.1 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000018-ALG-000017` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set custom-access-policy <CUSTOM_POLICY>; next; end` |
| Server objects | Cloud connector filters for server pool members (private and public DNS name, instance type) | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Input validation | Bypassing obviously invalid content (very long parameter names, non-printable characters) in the parameter decoder | 7.0.1 and later | ALG `SRG-NET-000380-ALG-000128` | GUI: System > Config > Advanced |
| Machine learning | Anomaly detection enhancements (HMM pre-screening options, NoSQL injection detection) | 7.0.1 and later | ALG `SRG-NET-000319-ALG-000153`; ALG `SRG-NET-000319-ALG-000015` | `config waf machine-learning-policy; edit <ID>; set status enable; set action-anomaly alert_deny; next; end` |
| XML protection | IP address or port override in WSDL | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Access control | Allowed methods checked in method override headers and parameters | 7.0.1 and later | ALG `SRG-NET-000512-ALG-000066` | `config waf allow-method-policy; edit <METHOD_POLICY>; set override-header enable; set override-parameter enable; next; end` |
| Access control | Blocking IP addresses from unknown countries (Geo IP) | 7.0.1 and later | ALG `SRG-NET-000364-ALG-000122` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set geo-block-list-policy <GEO_POLICY>; next; end` (with Unknown Country/Region in the list) |
| Protocol constraints | HTTP protocol constraint exceptions for malformed requests, exception priority, and detailed attack logs | 7.0.1 and later | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000380-ALG-000128` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set HTTP-protocol-parameter-restriction <CONSTRAINTS>; next; end` |
| Server policy | HTTP content routing table status column, search, and priority | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| XML protection | Chunk decoding in XML protection (requests) | 7.0.1 and later | ALG `SRG-NET-000401-ALG-000127` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set xml-validation-policy <XML_POLICY>; next; end` |
| GUI | Web cache statistics in the Throughput widget | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server objects | Virtual server names of up to 192 characters | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | Active-passive HA cluster with unicast heartbeat on KVM | 7.0.1 and later | ALG `SRG-NET-000365-ALG-000123` | `config system ha; set mode active-passive; set encryption enable; set key <HA_KEY>; end` |
| Cloud and VM | Cloud-init for FortiWeb-VM on Google Cloud | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Licensing | Flex-VM licensing | 7.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| ZTNA | Zero Trust Network Access (client certificates, EMS tags, and ZTNA rules) | 7.0.2 and later | ALG `SRG-NET-000015-ALG-000016`; ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000166-ALG-000101` | `config server-policy policy; edit <POLICY>; set ztna-profile <ZTNA_PROFILE>; next; end` |
| ZTNA | FortiClient EMS integration through a fabric connector | 7.0.2 and later | ALG `SRG-NET-000138-ALG-000088` | `config system endpoint-control fctems; edit <EMS>; set server <EMS_SERVER>; set server-verification enable; next; end` |
| Scripting | Lua scripting | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Threat Analytics in FortiWeb Cloud | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — (a cloud service outside the enclave; leave unconfigured unless authorized) |
| GUI | Machine learning menus moved under Web Protection, Bot Mitigation, and API Protection | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | Machine-learning API protection statistics | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI | Domain usage statistics widget | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Access control | X-Forwarded-For full scan against IP reputation | 7.0.2 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000077-ALG-000046` | GUI: Server Objects > X-Forwarded-For |
| Authentication | Credential stuffing check against the local and online databases | 7.0.2 and later | ALG `SRG-NET-000019-ALG-000018` | `config waf user-tracking rule; edit <RULE>; set credential-stuffing-protection enable; next; end` |
| Signatures | Signature sensitivity levels L1 to L4 (CLI) | 7.0.2 and later | ALG `SRG-NET-000318-ALG-000152`; ALG `SRG-NET-000318-ALG-000014`; ALG `SRG-NET-000318-ALG-000151` | `config waf signature; edit <SIGNATURE_POLICY>; set sensitivity-level <LEVEL>; next; end` |
| Access control | HTTP method and protocol checks in URL access rules | 7.0.2 and later | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000015-ALG-000016` | `config waf url-access-rule; edit <RULE>; config match-condition; edit 1; set only-protocol https; next; end; next; end` |
| Server objects | Port and sub-domain matching in protected host names | 7.0.2 and later | ALG `SRG-NET-000364-ALG-000122` | `config server-policy allow-hosts; edit <HOSTS>; config host-list; edit 1; set host <FQDN>; set ignore-port disable; set include-subdomains disable; next; end; next; end` |
| Malware and files | File security: clearing cached ICAP scan results and custom file types | 7.0.2 and later | ALG `SRG-NET-000248-ALG-000133` | `config waf file-upload-restriction-policy; edit <FILE_POLICY>; set icap-server-check enable; next; end` |
| Access control | Allow list at the server policy level | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server policy | Chunked encoding of responses | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config server-policy policy; edit <POLICY>; set chunk-encoding disable; next; end` |
| Server policy | More x509 certificate subject match options in content routing | 7.0.2 and later | ALG `SRG-NET-000166-ALG-000101` | — |
| Server policy | Editing the server pool from an HTTP content routing policy | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates and TLS | SSL cipher groups, and most ciphers available with HTTP/2 | 7.0.2 and later | ALG `SRG-NET-000062-ALG-000150` | `config server-policy policy; edit <POLICY>; set ssl-cipher custom; set ssl-custom-cipher <APPROVED_CIPHERS>; next; end` |
| Authentication | Lower CPU use for SAML authentication | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates and TLS | Intermediate CA (partial certificate chain) validation of client certificates | 7.0.2 and later | ALG `SRG-NET-000164-ALG-000100` | `config system certificate verify; edit <VERIFIER>; set partial-chain disable; next; end` (validate the full path to the DoD root) |
| Certificates and TLS | Let's Encrypt certificate renewal interval and multiple FQDNs | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | Password change for users authenticated by a RADIUS server | 7.0.2 and later | ALG `SRG-NET-000138-ALG-000088` | — |
| Authentication | FortiAuthenticator authorization | 7.0.2 and later | ALG `SRG-NET-000138-ALG-000088`; ALG `SRG-NET-000140-ALG-000094` | — |
| Administrator accounts | More than one ADOM for an administrator | 7.0.2 and later | NDM `SRG-APP-000033-NDM-000212` | `config system admin; edit <ADMIN>; set domains <ADOM_NAME>; next; end` |
| Logging | Signature database version in the event log | 7.0.2 and later | ALG `SRG-NET-000019-ALG-000019` | `config log event-log; set status enable; end` |
| Logging | XML validation attack log details | 7.0.2 and later | ALG `SRG-NET-000074-ALG-000043` | `config log attack-log; set status enable; end` |
| Logging | OWASP API Top 10 attack log field | 7.0.2 and later | ALG `SRG-NET-000074-ALG-000043` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set owasp_api_top10_log_field enable; next; end` |
| Diagnostics | Update history in diagnose system update | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | diagnose debug comlog command | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cloud and VM | Health probe port behind an Azure load balancer | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platforms | Higher certificate maximums on VM16, 4000E, and 4000F | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | Full configuration synchronization in HA on Google Cloud | 7.0.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | Unicast HA heartbeat on VMware | 7.0.2 and later | ALG `SRG-NET-000365-ALG-000123` | — |
| Bot mitigation | ML-based bot detection against Challenge Collapsar (CC) attacks | 7.0.3 and later | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000362-ALG-000155` | `config waf bot-detection-policy; edit <ID>; set model-status enable; set action alert_deny; next; end` |
| Server policy | 100-continue header handling | 7.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | HA failover when proxyd writes a core dump | 7.0.4 and later | ALG `SRG-NET-000365-ALG-000123` | `config server-policy setting; set enable-core-file enable; set corefile-ha-failover enable; end` |
| Certificates and TLS | TLS 1.2 signature algorithm compatibility setting | 7.0.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config server-policy setting; set tls12-compatible-sigalg disable; end` |
| Diagnostics | Core dumps enabled by default, with a limited generation rate | 7.0.5 and later | ALG `SRG-NET-000236-ALG-000119` | `config server-policy setting; set enable-core-file enable; end` |
| API protection | API gateway: per-user rate limits, X-RateLimit headers, API key refresh, dynamic keys, and JWT | 7.2.0 and later | ALG `SRG-NET-000015-ALG-000016`; ALG `SRG-NET-000362-ALG-000112` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set api-management-policy <API_POLICY>; next; end` |
| Input validation | Parameter validation: scan location, maximum number of parameters, and JSON parameters | 7.2.0 and later | ALG `SRG-NET-000401-ALG-000127` | `config waf input-rule; edit <RULE>; set maximum-parameter-number <N>; set json-parameter-support enable; next; end`; `config waf web-protection-profile inline-protection; edit <PROFILE>; set parameter-validation-rule <INPUT_RULES>; next; end` |
| Client management | Client management: multiple threat score profiles, Alert and Alert & Deny actions, signature-only scoring, threat history | 7.2.0 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000390-ALG-000139` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set client-management enable; set threat-score-profile <THREAT_SCORE_PROFILE>; next; end` |
| Signatures | Signature sensitivity levels in the web UI | 7.2.0 and later | ALG `SRG-NET-000318-ALG-000152`; ALG `SRG-NET-000318-ALG-000014`; ALG `SRG-NET-000318-ALG-000151` | GUI: Web Protection > Known Attacks > Signatures |
| Authentication | FortiToken Mobile push notification through a FortiAuthenticator RADIUS server | 7.2.0 and later | ALG `SRG-NET-000140-ALG-000094`; ALG `SRG-NET-000339-ALG-000090` | `config user radius-user; edit <RADIUS>; set fac-push enable; next; end` |
| Server policy | Server policy tags | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | Certificate and host name verification for LDAP over TLS | 7.2.0 and later | ALG `SRG-NET-000138-ALG-000088`; ALG `SRG-NET-000164-ALG-000100` | `config user ldap-user; edit <LDAP>; set ssl-connection enable; set protocol ldaps; set ca-cert <CA_CERT>; next; end` |
| Certificates and TLS | Let's Encrypt TLS-ALPN-01 and DNS-01 challenges | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | User tracking with JSON-format logins | 7.2.0 and later | ALG `SRG-NET-000503-ALG-000038` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set user-tracking-policy <USER_TRACKING_POLICY>; next; end` |
| Scripting | Lua script update: predefined HTTP_REWRITE_BODY script | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Global Resources page (usage and maximum configuration values) | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | HA debug commands | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Debug file download for secondary HA members | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Real-time packet capture and flow debug logs | 7.2.0 and later | NDM `SRG-APP-000408-NDM-000314` | GUI: Network > Packet Capture |
| System | TCP buffer size of up to 3992 KB | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | ASAN executables in the debug symbol file | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Event log for JSON schema upload failures | 7.2.0 and later | NDM `SRG-APP-000095-NDM-000225` | — |
| Administrator accounts | Administrator password hash changed from SHA-1 to SHA-256 | 7.2.0 and later | NDM `SRG-APP-000171-NDM-000258` | — (applies when a password is set or changed) |
| Management access | Disabling the configuration synchronization port (TCP 995) | 7.2.0 and later | NDM `SRG-APP-000142-NDM-000245` | GUI: System > Admin > Settings |
| Administrator accounts | Global menu and global CLI commands hidden from ADOM administrators | 7.2.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000231-NDM-000271` | — |
| Platforms | New platform: FortiWeb 1000F | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Licensing | Flex-VM license import through cloud-init on AWS | 7.2.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Custom rules | Custom rule enhancements: separate HTTP Methods filter (with WebDAV, RPC, and others) and parameter location | 7.2.1 and later | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000019-ALG-000018` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set custom-access-policy <CUSTOM_POLICY>; next; end` |
| Access control | Reverse DNS lookup timeout in URL access rules | 7.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server objects | IP groups | 7.2.1 and later | ALG `SRG-NET-000364-ALG-000122` | `config server-policy ip-group; edit <IP_GROUP>; config members; edit 1; set ip <ADDRESS_RANGE>; next; end; next; end` |
| Scripting | Lua script update: predefined SSL_COMMANDS script | 7.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | JSON protection: schema version check and schema groups | 7.2.1 and later | ALG `SRG-NET-000401-ALG-000127` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set json-validation-policy <JSON_POLICY>; next; end` |
| API protection | OpenAPI "format" (email, uuid) for string types | 7.2.1 and later | ALG `SRG-NET-000401-ALG-000127` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set openapi-validation-policy <OPENAPI_POLICY>; next; end` |
| Application delivery | Insertion of several HTTP headers in a URL rewrite rule | 7.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Security Fabric | TLS host and peer verification for Fetch URL and Quarantine IP | 7.2.1 and later | ALG `SRG-NET-000164-ALG-000100` | `config system fortigate-integration; set server-verification enable; set ca-cert <CA_CERT>; end` |
| ZTNA | Server certificate validation for the FortiClient EMS connector | 7.2.1 and later | ALG `SRG-NET-000164-ALG-000100` | `config system endpoint-control fctems; edit <EMS>; set server-verification enable; set ca-cert <CA_CERT>; next; end` |
| Authentication | Strict TLS verification with a custom CA for OAuth authorization servers | 7.2.1 and later | ALG `SRG-NET-000164-ALG-000100` | `config user oauth-user request; edit <REQUEST>; set tls-check enable; set tls-ca <CA_CERT>; next; end` |
| Load balancing | Least response time and probabilistic weighted least response time algorithms | 7.2.1 and later | ALG `SRG-NET-000362-ALG-000120` | `config server-policy server-pool; edit <POOL>; set lb-algo least-response-time; next; end` |
| Server policy | Request redirection: naked domain to www, and 301 for HTTP to HTTPS | 7.2.1 and later | ALG `SRG-NET-000062-ALG-000150` | `config server-policy policy; edit <POLICY>; set HTTP-to-HTTPS enable; next; end` |
| Load balancing | Health check result sharing across server pools | 7.2.1 and later | ALG `SRG-NET-000365-ALG-000123` | `config server-policy health; edit <HEALTH_CHECK>; set group-id <ID>; set role master; next; end` |
| Management access | Shell access enhancements: command history and trusted hosts | 7.2.1 and later | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000142-NDM-000245` | `config system global; set shell-access disable; end` (if Fortinet support needs shell access, restrict it to trusted hosts) |
| Replacement messages | %%USERNAME%% and %%RAWNAME%% in replacement messages | 7.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates and TLS | RFC 7919 FFDHE groups for inbound and outbound HTTPS (titled "RFC-9719 Comply" in the release notes) | 7.2.1 and later | ALG `SRG-NET-000062-ALG-000150` | `config server-policy policy; edit <POLICY>; set rfc7919-comply enable; next; end` |
| Certificates and TLS | Let's Encrypt RSA keys of 2048, 3072, or 4096 bits | 7.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Attack and traffic packet logs to syslog in JSON over TCP or TLS (ELK) | 7.2.1 and later | ALG `SRG-NET-000334-ALG-000050`; ALG `SRG-NET-000511-ALG-000051` | `config log syslog-policy; edit <SYSLOG_POLICY>; config syslog-server-list; edit 1; set server <SYSLOG_SERVER>; set proto tls; set format json; next; end; next; end` |
| Logging | Host and URL in RBE, CAPTCHA, and reCAPTCHA attack logs | 7.2.1 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| Bot mitigation | Editable Google reCAPTCHA service URL | 7.2.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | ADOM administrators can only view the VIPs of their ADOM | 7.2.1 and later | NDM `SRG-APP-000033-NDM-000212` | — |
| Licensing | Threat Analytics 14-day evaluation license | 7.2.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Management access | Firewall admin policy (administrative access by interface, address, and service) | 7.2.2 and later | NDM `SRG-APP-000038-NDM-000213`; NDM `SRG-APP-000408-NDM-000314` | `config system firewall admin-policy; config firewall-admin-policy-match-list; edit 1; set in-interface <MGMT_PORT>; set src-address <MGMT_SUBNET>; set action accept; next; end; end` |
| Server objects | Uploading IP group members from a CSV file | 7.2.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Access control | IP groups in IP reputation exceptions | 7.2.2 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Authentication | Site Publish rule maximum raised from 216 to 512 | 7.2.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates and TLS | TLS settings for ADFS proxy server pools | 7.2.2 and later | ALG `SRG-NET-000062-ALG-000150` | GUI: Server Objects > Server > Server Pool |
| Cloud and VM | FortiWeb-VM HA on Alibaba Cloud (including SCCC) | 7.2.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cloud and VM | IMDSv2 for FortiWeb-VM on AWS | 7.2.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Protocol constraints | HTTP/2 RST_STREAM check in HTTP protocol constraints | 7.2.5+; 7.4.1+ | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000512-ALG-000066` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set HTTP-protocol-parameter-restriction <CONSTRAINTS>; next; end` |
| Bot mitigation | Counter setting (keep occurrence count) in threshold-based detection | 7.2.8+; 7.4.3+ | ALG `SRG-NET-000362-ALG-000112` | `config waf threshold-based-detection; edit <POLICY>; set keep-occurrence-count enable; next; end` |
| Access control | External IP address auto-retrieval (IP address connector) | 7.4.0 and later | ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000019-ALG-000018` | `config system external-resource; edit <RESOURCE>; set status enable; set protocol HTTPS; set verify-host-cert enable; set ca <CA_CERT>; next; end` |
| API protection | Continuous learning in ML-based API protection | 7.4.0 and later | ALG `SRG-NET-000401-ALG-000127` | `config waf api-learning-policy; edit <ID>; set status enable; next; end` |
| Security Fabric | Automation (actions triggered by event logs) | 7.4.0 and later | NDM `SRG-APP-000360-NDM-000295`; ALG `SRG-NET-000392-ALG-000141` | `config system automation-stitch; edit <STITCH>; set status enable; set trigger <TRIGGER>; next; end` |
| Logging and monitoring | OWASP Top 10 compliance dashboard | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cloud and VM | FortiWeb Kubernetes Ingress Controller | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | gRPC protocol constraints (signature scanning, rate limiting, size limiting) | 7.4.0 and later | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000362-ALG-000112` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set grpc-security-policy <GRPC_POLICY>; next; end` |
| Authentication | OpenID Connect (OIDC) authentication with OAuth | 7.4.0 and later | ALG `SRG-NET-000138-ALG-000063`; ALG `SRG-NET-000138-ALG-000088` | `config user oauth-user server; edit <OAUTH_SERVER>; set oidc enable; next; end` |
| Authentication | Okta OAuth request template | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Bot mitigation | Bot trait checking in biometrics-based detection | 7.4.0 and later | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000390-ALG-000139` | `config waf biometrics-based-detection; edit <POLICY>; set bot-traits enable; next; end` |
| Logging and monitoring | FortiView Log Analysis | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Protocol constraints | HTTP protocol constraint checks (Transfer-Encoding, body length, missing Host, range overlap, multipart) | 7.4.0 and later | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000380-ALG-000128` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set HTTP-protocol-parameter-restriction <CONSTRAINTS>; next; end` |
| Application delivery | More flexible URL rewriting rules (methods, bodies, status codes, header removal and renaming) | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server objects | X-Forwarded-For header enhancement (address position, deleting or merging earlier headers) | 7.4.0 and later | ALG `SRG-NET-000077-ALG-000046` | GUI: Server Objects > X-Forwarded-For |
| Bot mitigation | CAPTCHA challenge difficulty levels | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server objects | Override headers in protected host names | 7.4.0 and later | ALG `SRG-NET-000364-ALG-000122` | `config server-policy allow-hosts; edit <HOSTS>; config host-list; edit 1; set host <FQDN>; set override-headers enable; next; end; next; end` |
| Authentication | Default domain prefix for the NTLM delegation method | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server policy | Multiple IP addresses and ranges in HTTP content routing rules | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Input validation | Cache mode in parameter validation | 7.4.0 and later | ALG `SRG-NET-000401-ALG-000127` | `config waf parameter-validation-rule; edit <RULE>; set cache-mode enable; next; end` |
| Application delivery | Web cache exceptions by HTTP return code | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates and TLS | Predefined allow list entry for Let's Encrypt challenge requests | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Firmware and configuration | Configuration and certificate restore from SFTP and FTP servers | 7.4.0 and later | NDM `SRG-APP-000516-NDM-000340` | `execute restore config sftp <FILE> <SERVER_IP> <PASSWORD>` |
| Load balancing | Session-based (per-transaction) persistence | 7.4.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates and TLS | Use of a previously retrieved CRL when CRL retrieval fails | 7.4.0 and later | ALG `SRG-NET-000345-ALG-000099`; ALG `SRG-NET-000164-ALG-000100` | `config system certificate verify; edit <VERIFIER>; set crl-allow-expired disable; next; end` (enable only temporarily, as the Admin Guide advises) |
| Administrator accounts | Administrator login with FortiCloud accounts (SSO) | 7.4.0 and later | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000516-NDM-000336` | `config system global; set admin-forticloud-sso-login disable; end` |
| Management access | Remote access from FortiCloud | 7.4.0 and later | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000408-NDM-000314` | — (a cloud service outside the enclave; leave unconfigured) |
| API protection | ML-based API protection: schema protection and threat protection | 7.4.1 and later | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000319-ALG-000153` | `config waf api-learning-policy; edit <ID>; set status enable; set action-mlapi alert_deny; next; end` |
| API protection | GraphQL protection | 7.4.1 and later | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000362-ALG-000112` | GUI: API Protection > GraphQL Protection |
| Application delivery | Waiting room | 7.4.1 and later | ALG `SRG-NET-000705-ALG-000110` | `config waf waiting-room-policy; edit <POLICY>; set total-active-users <N>; set new-users-per-min <N>; next; end` |
| Bot mitigation | FortiGuard Advanced Bot Protection (SaaS) policy | 7.4.1 and later | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000390-ALG-000139` | `config system global; set advanced-bot-protection enable; end`; `config waf web-protection-profile inline-protection; edit <PROFILE>; set advanced-bot-protection <ABP_POLICY>; next; end` (a cloud service; use only if authorized) |
| XML protection | XML Signature Wrapping (XSW) detection | 7.4.1 and later | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000230-ALG-000113` | `config waf xml-validation rule; edit <RULE>; set xsw <XSW_RULE>; next; end` |
| XML protection | DTD validation for XML requests | 7.4.1 and later | ALG `SRG-NET-000401-ALG-000127` | `config waf xml-validation rule; edit <RULE>; set dtd-file <DTD_FILE>; next; end` |
| Signatures | Signature enhancements: Hyperscan PII detection in response bodies, and category and sensitivity details | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Bot mitigation | Biometrics-based bot detection accuracy and trait weighting | 7.4.1 and later | ALG `SRG-NET-000362-ALG-000112` | — |
| Bot mitigation | reCAPTCHA v3 | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — (a Google service outside the enclave) |
| Client-side protection | Permissions-Policy header (replacing Feature-Policy) in HTTP header security | 7.4.1 and later | ALG `SRG-NET-000228-ALG-000108`; ALG `SRG-NET-000288-ALG-000109` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set HTTP-header-security <HEADER_SECURITY_POLICY>; next; end` |
| Authentication | Multiple SAML servers in Site Publish | 7.4.1 and later | ALG `SRG-NET-000138-ALG-000088` | — |
| Application delivery | Search of cached items by URL | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | IP address conflict event | 7.4.1 and later | NDM `SRG-APP-000095-NDM-000225` | — |
| Logging | Log type selection (attack, event, traffic) for local storage and log forwarding | 7.4.1 and later | NDM `SRG-APP-000515-NDM-000325`; ALG `SRG-NET-000334-ALG-000050` | GUI: Log&Report > Log Config > Global Log Settings |
| Logging | ZIP compression of alert email attachments | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server policy | HTTP/2 window size setting | 7.4.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Data loss prevention | FortiGuard Data Loss Prevention service | 7.4.2 and later | ALG `SRG-NET-000391-ALG-000140` | GUI: Web Protection > Data Loss Prevention |
| Security Fabric | FortiGSLB connector | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | 2023 OWASP API Security Top 10 categories in attack logs | 7.4.2 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| Licensing | Enterprise bundle license | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | Trust establishment with ADFS servers disabled by default | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| DoS protection | TCP flood prevention moved after the IP list in the scan sequence | 7.4.2 and later | ALG `SRG-NET-000705-ALG-000110` | — |
| Application delivery | Several URL rewriting actions on one request | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Client-side protection | Bypassing the AJAX check in MiTB protection | 7.4.2 and later | ALG `SRG-NET-000230-ALG-000113` | `config waf mitb-rule; edit <RULE>; set ajaxcheck enable; next; end` |
| Client management | Expiration time of the cookiesession1 cookie | 7.4.2 and later | ALG `SRG-NET-000213-ALG-000107` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set http-session-cookie enable; set http-session-timeout <DAYS>; next; end` |
| Licensing | Flex-VM license auto-deployment in deployment templates | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platforms | New platform: FortiWeb 400F | 7.4.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Client management | Delete All and Restore All in the client management monitor | 7.4.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Malware and files | application/octet-stream filename detection for logging | 7.4.3 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| Logging | Traffic log priority (attack logs first when the log queue is nearly full) | 7.4.4 and later | ALG `SRG-NET-000335-ALG-000053` | `config log traffic-log; set low-priority enable; end` |
| Logging | Configurable traffic packet payload size sent to log servers | 7.4.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | SSL error logs, globally and per server policy | 7.4.4+; 7.6.0+ | ALG `SRG-NET-000074-ALG-000043` | `config log attack-log; set status enable; set no-ssl-error disable; end`; `config server-policy policy; edit <POLICY>; set no-ssl-error-log disable; next; end` |
| Access control | Geo IP filtering with Allow Mode (deny all regions not listed) | 7.4.8 and later | ALG `SRG-NET-000364-ALG-000122`; ALG `SRG-NET-000202-ALG-000124` | — (no Allow Mode setting found in the 8.0.8 CLI Reference; configure it in the Geo IP policy in the web UI) |
| Bot mitigation | Login status reporting to Advanced Bot Protection | 7.4.8 and later | ALG `SRG-NET-000362-ALG-000112` | — |
| Diagnostics | Diagnostics for TCP connection termination reasons | 7.4.9 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Protocol constraints | HTTP/2 and HTTP/3 protocol constraint hardening (header line count, initial window size range) | 7.4.13+; 7.6.9+; 8.0.6+ | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000362-ALG-000112` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set HTTP-protocol-parameter-restriction <CONSTRAINTS>; next; end` |
| Protocol | HTTP/3 support | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | Threat protection model update | 7.6.0 and later | ALG `SRG-NET-000319-ALG-000153` | — |
| Client-side protection | Built-in allowed domains in MiTB protection | 7.6.0 and later | ALG `SRG-NET-000230-ALG-000113` | — |
| Web protection | AJAX check for cross-site request forgery (CSRF) requests | 7.6.0 and later | ALG `SRG-NET-000230-ALG-000113` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set csrf-protection <CSRF_RULE>; next; end` |
| DoS protection | DoS protection exception policy | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | Obscuring sensitive data in gRPC API responses | 7.6.0 and later | ALG `SRG-NET-000391-ALG-000140` | — |
| Bot mitigation | Known good bots subcategories | 7.6.0 and later | ALG `SRG-NET-000362-ALG-000112` | — |
| Application delivery | URL rewrite enhancements | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Application delivery | "deflate" compression type | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server objects | Trusted IP addresses for X-Forwarded-For (XFF trust IPs) | 7.6.0 and later | ALG `SRG-NET-000077-ALG-000046`; ALG `SRG-NET-000735-ALG-000130` | `config waf x-forwarded-for; edit <XFF_RULE>; config ip-list; edit 1; set ip <TRUSTED_PROXY_IP>; next; end; next; end` |
| Application delivery | Custom waiting room display page | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Security Fabric | Quarantine IP settings moved to Security Fabric > Fabric Connectors | 7.6.0 and later | ALG `SRG-NET-000019-ALG-000018` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set fortigate-quarantined-ips enable; next; end` |
| Replacement messages | 500 error page enhancement | 7.6.0 and later | ALG `SRG-NET-000273-ALG-000129` | GUI: System > Config > Replacement Message |
| Malware and files | Signature scan of uploaded files | 7.6.0 and later | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000319-ALG-000015` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set signature-extended-detection FileUpload; next; end` |
| Scripting | Lua scripts for content routing | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server policy | HTTP content routing table search | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Load balancing | Server inheriting the server pool health check in TTP mode | 7.6.0 and later | ALG `SRG-NET-000365-ALG-000123` | `config server-policy server-pool; edit <POOL>; config pserver-list; edit <ID>; set health-check-inherit enable; next; end; next; end` |
| Authentication | Password change with the PAP scheme through a RADIUS server | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | Retrieving LDAP user attributes | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | Automatic generation of SAML and OAuth login pages | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Administrator accounts | Administrator single sign-on with SAML | 7.6.0 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000149-NDM-000247` | `config system saml; set status enable; set idp-entity-id <IDP_ENTITY_ID>; set idp-single-sign-on-url <IDP_SSO_URL>; set idp-single-logout-url <IDP_SLO_URL>; end`; `config system sso-admin; edit <ADMIN>; set access-profile <PROFILE>; next; end` |
| Network | Warning message on local port exhaustion | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | FortiWeb performance data in FortiAnalyzer | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Replacement messages | Replacement message enhancements | 7.6.0 and later | ALG `SRG-NET-000273-ALG-000129` | GUI: System > Config > Replacement Message |
| System | Release tags | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Debug command enhancements | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Traffic log enhancements | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | FortiView original source | 7.6.0 and later | ALG `SRG-NET-000077-ALG-000046` | — |
| Logging and monitoring | FortiView Log Analysis enhancement | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI | Displaying configuration in its context | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| High availability | FortiWeb Hyper-V HA cluster with unicast heartbeat | 7.6.0 and later | ALG `SRG-NET-000365-ALG-000123` | — |
| High availability | Synchronizing health check status in HA mode | 7.6.0 and later | ALG `SRG-NET-000365-ALG-000123` | `config system ha; set hlck-sync enable; end` |
| Security Fabric | Security Fabric automation enhancements | 7.6.0 and later | ALG `SRG-NET-000392-ALG-000141` | — |
| Cloud and VM | Ingress Controller enhancements | 7.6.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | Scanning for sensitive data leakage in API endpoints | 7.6.1 and later | ALG `SRG-NET-000391-ALG-000140` | — |
| API protection | ML-based API protection user interface | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Signatures | Abnormal chunk size detection in the signature module | 7.6.1 and later | ALG `SRG-NET-000512-ALG-000066`; ALG `SRG-NET-000380-ALG-000128` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set signature-rule <SIGNATURE_POLICY>; next; end` |
| Web protection | JavaScript event check for CSRF requests | 7.6.1 and later | ALG `SRG-NET-000230-ALG-000113` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set csrf-protection <CSRF_RULE>; next; end` |
| Protocol | HTTP/3 traffic in more modules | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates and TLS | OCSP-based client certificate verification | 7.6.1 and later | ALG `SRG-NET-000164-ALG-000100`; ALG `SRG-NET-000345-ALG-000099` | `config system certificate ocsp-responder; edit <OCSP>; set ocsp-url <DOD_OCSP_URL>; set caching enable; next; end` |
| Certificates and TLS | Wildcard domain names in Let's Encrypt certificates | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| FTP security | Client certificate verification in FTPS connections | 7.6.1 and later | ALG `SRG-NET-000164-ALG-000100` | — |
| Certificates and TLS | Certificate signing requests for administrator certificates | 7.6.1 and later | NDM `SRG-APP-000516-NDM-000344` | GUI: System > Admin > Certificates |
| Time | Multiple NTP servers and NTP authentication (SHA-1, SHA-256, AES-128, AES-256) | 7.6.1 and later | NDM `SRG-APP-000395-NDM-000347`; NDM `SRG-APP-000920-NDM-000320` | `config system ntp; set ntpsync enable; config ntp-server; edit 1; set server <NTP_SERVER>; set authentication enable; set key-type sha256; set key-id <KEY_ID>; set key <KEY>; next; end; end` |
| System | Maximum value changes | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | FortiView bot analysis enhancements | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| SNMP | SNMPv3 SHA-2 authentication and AES-256 privacy | 7.6.1 and later | NDM `SRG-APP-000395-NDM-000310` | `config system snmp user; edit <SNMP_USER>; set security-level authpriv; set auth-proto sha256; set priv-proto aes256; next; end` |
| Diagnostics | Troubleshooting high-CPU-cost PCRE pattern matching | 7.6.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | IPv6 syslog servers | 7.6.1 and later | NDM `SRG-APP-000515-NDM-000325` | — |
| High availability | High-volume active-active HA behind a load balancer | 7.6.1 and later | ALG `SRG-NET-000362-ALG-000120` | — |
| System | Disk expansion (data partition enlarged during the 7.6.2 upgrade) | 7.6.2 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Client-side protection | SSL stripping detection in MiTB protection | 7.6.3 and later | ALG `SRG-NET-000230-ALG-000113`; ALG `SRG-NET-000062-ALG-000150` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set mitb-protection <MITB_POLICY>; next; end` |
| Bot mitigation | Biometrics-based detection enhancements | 7.6.3 and later | ALG `SRG-NET-000362-ALG-000112` | — |
| Signatures | Syntax-based detection enhancements | 7.6.3 and later | ALG `SRG-NET-000318-ALG-000152`; ALG `SRG-NET-000319-ALG-000020`; ALG `SRG-NET-000318-ALG-000014` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set syntax-based-attack-detection <SBD_POLICY>; next; end` |
| API protection | OpenAPI schema validation enhancement | 7.6.3 and later | ALG `SRG-NET-000401-ALG-000127` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set openapi-validation-policy <OPENAPI_POLICY>; next; end` |
| Application delivery | Zstandard (zstd) compression support | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | gRPC over HTTP/1 | 7.6.3 and later | ALG `SRG-NET-000401-ALG-000127` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set grpc-security-policy <GRPC_POLICY>; next; end` |
| Client management | Threat weight configuration enhancements | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | Microsoft Azure OAuth | 7.6.3 and later | ALG `SRG-NET-000138-ALG-000088` | — |
| Cloud and VM | MANA network on Azure | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates and TLS | Securosys Primus HSM | 7.6.3 and later | ALG `SRG-NET-000755-ALG-000150`; ALG `SRG-NET-000062-ALG-000092` | `config server-policy setting; set hsm enable; set hsm-manufacturer primus; end` |
| Malware and files | Region-based connectivity for FortiWeb Cloud Sandbox | 7.6.3 and later | ALG `SRG-NET-000248-ALG-000133` | `config system fortisandbox; set type cloud; set region <REGION>; end` |
| System | TPM-based encryption of configuration passwords and certificates | 7.6.3 and later | ALG `SRG-NET-000755-ALG-000150` | `config system encryption-method; set private-encryption-key enable; end` |
| API protection | API gateway configuration object limits | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI | SOCaaS license status in the dashboard | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cryptography | Expanded cipher support (ECDHE-RSA AES-GCM) in FIPS-CC mode | 7.6.3 and later | ALG `SRG-NET-000510-ALG-000111`; ALG `SRG-NET-000062-ALG-000150` | `config system fips-cc; set status enable; end` |
| Logging | FortiAnalyzer Cloud | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — (a cloud service outside the enclave; use an on-premises FortiAnalyzer) |
| Logging | Logging of SNMPv3 authentication failures | 7.6.3 and later | NDM `SRG-APP-000395-NDM-000310`; NDM `SRG-APP-000503-NDM-000320` | — |
| Diagnostics | Object pool memory leak detection in proxyd | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | CPU and memory monitoring | 7.6.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Data loss prevention | DLP exceptions for fine-grained bypass control | 7.6.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | Learning logic for ML-based API protection | 7.6.4 and later | ALG `SRG-NET-000401-ALG-000127` | — |
| Server objects | Wildcard matching in global cookie allow lists | 7.6.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates and TLS | Restricting weak TLS signature algorithms (SHA-1 and SHA-224) | 7.6.4 and later | ALG `SRG-NET-000062-ALG-000150`; ALG `SRG-NET-000510-ALG-000025` | — (the 7.6.4 Admin Guide documents restrict-weak-sign-algo under config server-policy setting; it is not in the 8.0.8 CLI Reference) |
| Platforms | Higher configuration maximums for the 4000F platform | 7.6.4 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Schema line numbers in OpenAPI validation attack logs | 7.6.4 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| Security Fabric | STIX/TAXII support for the IP address connector | 7.6.4 and later | ALG `SRG-NET-000019-ALG-000018`; ALG `SRG-NET-000392-ALG-000142` | — |
| Server policy | Source IP allow list for bypassing monitor traffic in TTP mode | 7.6.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Server latency event logging | 7.6.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | Custom certificate and key for SAML service provider (SP) metadata | 7.6.8+; 8.0.3+ | ALG `SRG-NET-000230-ALG-000113` | `config user saml-user; edit <SAML_SERVER>; set select-custom-certificate enable; set custom-certificate <CERT>; next; end` |
| Certificates and TLS | Luna HSM enhancements | 7.6.8+; 8.0.7+ | ALG `SRG-NET-000755-ALG-000150` | GUI: System > Config > Luna HSM |
| Custom rules | IP connector as a source IP filter in custom policy rules | 7.6.10 and later | ALG `SRG-NET-000364-ALG-000122` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set custom-access-policy <CUSTOM_POLICY>; next; end` |
| Authentication | Custom port for SAML service provider URLs | 7.6.10 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Configured threshold shown in DoS protection attack logs | 7.6.10 and later | ALG `SRG-NET-000074-ALG-000043`; ALG `SRG-NET-000392-ALG-000148` | — |
| FortiAI | FortiAI integration | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Client-side protection | Client-side security module (menu for client-side features) | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Client-side protection | Client-side protection (monitoring of third-party scripts and page content) | 8.0.0 and later | ALG `SRG-NET-000228-ALG-000108`; ALG `SRG-NET-000288-ALG-000109` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set client-side-protection-policy <CSP_POLICY>; next; end` |
| Client-side protection | Subresource Integrity (SRI) check | 8.0.0 and later | ALG `SRG-NET-000228-ALG-000108`; ALG `SRG-NET-000288-ALG-000109` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set subresource-integrity-policy <SRI_POLICY>; next; end` |
| Client-side protection | Expanded HTTP header security support | 8.0.0 and later | ALG `SRG-NET-000228-ALG-000108` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set HTTP-header-security <HEADER_SECURITY_POLICY>; next; end` |
| Signatures | Syntax-based detection for command injection | 8.0.0 and later | ALG `SRG-NET-000318-ALG-000014`; ALG `SRG-NET-000319-ALG-000015` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set syntax-based-attack-detection <SBD_POLICY>; next; end` |
| Bot mitigation | Puzzle CAPTCHA bot confirmation | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Malware and files | File list module (MD5 and SHA-256 file hash matching) | 8.0.0 and later | ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000249-ALG-000134` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set file-list-policy <FILE_LIST>; next; end` |
| Scripting | Lua enhancements for fine-grained WAF control | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | Mobile token verification in the web protection profile | 8.0.0 and later | ALG `SRG-NET-000230-ALG-000113` | — |
| Bot mitigation | Client ID-based occurrence tracking in threshold-based detection | 8.0.0 and later | ALG `SRG-NET-000362-ALG-000112` | `config waf threshold-based-detection; edit <POLICY>; set tracking-type client-id; next; end` |
| DoS protection | Slow header attack detection | 8.0.0 and later | ALG `SRG-NET-000362-ALG-000112`; ALG `SRG-NET-000362-ALG-000155` | `config waf threshold-based-detection; edit <POLICY>; set slow-attack-detection enable; set slow-attack-action alert_deny; next; end` |
| Custom rules | Syntax-based detection in custom rules | 8.0.0 and later | ALG `SRG-NET-000319-ALG-000020` | — |
| API protection | Zombie API discovery | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Machine learning | URL clustering for machine learning | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Malware and files | File security for large file uploads | 8.0.0 and later | ALG `SRG-NET-000248-ALG-000133` | — |
| Server objects | Duplicating the XFF header to a custom header | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Custom rules | Updated label for authorization header validation in custom rules | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Application delivery | Interaction between web cache and WAF modules | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Replacement messages | Replacement messages per HTTP content routing policy | 8.0.0 and later | ALG `SRG-NET-000273-ALG-000129` | — |
| Scripting | Lua scripting with HTTP/3 | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Application delivery | Image acceleration | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | UPN format in Kerberos constrained delegation | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | Legacy authentication commands removed (Site Publish replaces them) | 8.0.0 and later | ALG `SRG-NET-000138-ALG-000063` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set site-publisher-helper <SITE_PUBLISH_POLICY>; next; end` |
| Certificates and TLS | Primus HSM certificates for administrator web UI access | 8.0.0 and later | NDM `SRG-APP-000516-NDM-000344` | — |
| Certificates and TLS | ACME challenge replication in clustered deployments | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | CPU resource allocation with daemon grouping | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | DNS resolution performance | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Client management | Client management dashboard monitoring | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Flow trace filtering by content routing policy, and debug duration | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Diagnostic command for shared signature instances | 8.0.0 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Watchdog logging and recovery for worker thread failures | 8.0.0 and later | ALG `SRG-NET-000236-ALG-000119` | — |
| High availability | Manual HA failover trigger | 8.0.0 and later | ALG `SRG-NET-000365-ALG-000123` | `execute ha failover status` |
| FortiAI | Analysis of individual attack logs with FortiAI | 8.0.1 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | MCP security for streamable HTTP and SSE | 8.0.3 and later | ALG `SRG-NET-000401-ALG-000127` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set mcp-security-policy <MCP_POLICY>; next; end` |
| Client-side protection | Client-side protection dashboard | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | API discovery and protection enhancements | 8.0.3 and later | ALG `SRG-NET-000401-ALG-000127` | — |
| API protection | JWT verification and mobile token security | 8.0.3 and later | ALG `SRG-NET-000230-ALG-000113`; ALG `SRG-NET-000015-ALG-000016` | `config waf mobile-api-protection-rule; edit <RULE>; set jwt-signature-scan enable; next; end` |
| Signatures | False positive mitigation for signature-based protection | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Signatures | More detection targets (request body) for syntax-based detection | 8.0.3 and later | ALG `SRG-NET-000319-ALG-000020`; ALG `SRG-NET-000319-ALG-000015` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set syntax-based-attack-detection <SBD_POLICY>; next; end` |
| Custom rules | Custom tracking occurrence matching in custom rules | 8.0.3 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Bot mitigation | Source IP control for ML-based bot detection | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Access control | Optional URL access parameters | 8.0.3 and later | ALG `SRG-NET-000401-ALG-000127` | — |
| Malware and files | File name and host information in ICAP file scanning | 8.0.3 and later | ALG `SRG-NET-000248-ALG-000133` | — |
| Authentication | OPTIONS requests bypass authentication | 8.0.3 and later | ALG `SRG-NET-000138-ALG-000063` | — (review: OPTIONS requests reach the server without authentication) |
| Certificates and TLS | ACME External Account Binding (EAB) for third-party certificate providers | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server objects | Comments in IP list entries and HTTP content routing rules | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates and TLS | Post-quantum cryptography (ML-KEM key exchange groups) | 8.0.3 and later | ALG `SRG-NET-000062-ALG-000150` | `config server-policy policy; edit <POLICY>; set tls-v13 enable; set tls-pqc-support enable; set tls-pqc-groups <ML_KEM_GROUPS>; next; end` |
| Scripting | Global key-value table for Lua scripts | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Access control | Original URL match in URL filtering | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | Custom user name source for SAML assertions | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | JWT OIDC ID token forwarding in Site Publish | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | Access token scope enforcement in OAuth resource server mode | 8.0.3 and later | ALG `SRG-NET-000015-ALG-000016` | — |
| Malware and files | Improved antivirus scanning for WAF modules | 8.0.3 and later | ALG `SRG-NET-000248-ALG-000133` | `config system antivirus; set default-db extended; end` |
| Security Fabric | Automation rolling window | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Threat telemetry reporting to FortiGuard | 8.0.3 and later | NDM `SRG-APP-000142-NDM-000245`; ALG `SRG-NET-000131-ALG-000085` | `config system global; set fds-statistics disable; end` |
| Administrator accounts | Disabling the default admin account | 8.0.3 and later | NDM `SRG-APP-000148-NDM-000346` | `config system global; set default-admin disable; end` |
| Administrator accounts | PBKDF2 password hashing | 8.0.3 and later | NDM `SRG-APP-000171-NDM-000258` | `config system password-policy; set login-lockout-upon-downgrade enable; end` |
| Cloud and VM | OCI Dedicated Region Cloud@Customer (DRCC) | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Cryptography | OpenSSL 3.5 | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Security Fabric | SAML authentication request signing (Security Fabric single sign-on) | 8.0.3 and later | NDM `SRG-APP-000516-NDM-000336` | — |
| Tracking | Custom tracking | 8.0.3 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | Adding a source IP to an IP group from the attack logs | 8.0.3 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| High availability | HA primary selection and traffic distribution enhancements | 8.0.3 and later | ALG `SRG-NET-000365-ALG-000123` | — |
| FortiAI | AI-powered site health and posture monitoring with FortiAI | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| FortiAI | AI-assisted Lua scripting with FortiAI | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Signatures | JA4 client fingerprinting | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Client-side protection | Cloud-based script insights for client-side protection | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Client-side protection | JavaScript obfuscation for client-side protection | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Client-side protection | Filtering for HTTP header security rules | 8.0.5 and later | ALG `SRG-NET-000228-ALG-000108` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set HTTP-header-security <HEADER_SECURITY_POLICY>; next; end` |
| Bot mitigation | Cryptographic bot authentication and AI crawler detection | 8.0.5 and later | ALG `SRG-NET-000362-ALG-000112` | — |
| Scripting | JA4 fingerprint access in Lua scripts | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Custom rules | JA4 fingerprints in custom rules | 8.0.5 and later | ALG `SRG-NET-000019-ALG-000018` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set custom-access-policy <CUSTOM_POLICY>; next; end` |
| Access control | URL encryption optimization | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Malware and files | Web shell detection for JSON content | 8.0.5 and later | ALG `SRG-NET-000765-ALG-000170`; ALG `SRG-NET-000248-ALG-000133` | `config waf webshell-detection-policy; edit <POLICY>; set json-file-support enable; next; end` |
| API protection | gRPC IDL file upload enhancements | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates and TLS | Multiple signing certificates per OCSP responder | 8.0.5 and later | ALG `SRG-NET-000164-ALG-000100` | — |
| Server objects | Global allow list expansion | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Server policy | Monitor mode per HTTP content routing entry | 8.0.5 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Scripting | XML parsing in Lua scripts | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | JWT locations for mobile identification | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Load balancing | Server pool member disable behavior | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Protocol | Non-standard HTTP traffic control | 8.0.5 and later | ALG `SRG-NET-000512-ALG-000066` | `config server-policy policy; edit <POLICY>; set allow-nonstd-http disable; next; end` |
| Authentication | RADSEC (RADIUS over TLS) authentication | 8.0.5 and later | ALG `SRG-NET-000138-ALG-000088`; ALG `SRG-NET-000400-ALG-000097` | — |
| Authentication | JWT access tokens for OAuth | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Authentication | OAuth PKCE for Site Publish | 8.0.5 and later | ALG `SRG-NET-000147-ALG-000095` | — |
| Authentication | SAML group membership extraction and header forwarding | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Network | QinQ in true transparent proxy mode | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Replacement messages | Custom headers in replacement messages | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Replacement messages | More content types for 503 Service Unavailable messages | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Software bill of materials (SBOM) and third-party licensing | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Platforms | System specification adjustments for F-series platforms | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Security Fabric | More log fields for automation actions | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging | Attack log filtering for staged signatures | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Firmware and configuration | Critical vulnerability upgrade notifications | 8.0.5 and later | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340` | GUI: System > Config > FortiGuard |
| Logging | Custom client certificate for syslog over TLS | 8.0.5 and later | NDM `SRG-APP-000515-NDM-000325`; ALG `SRG-NET-000334-ALG-000050` | `config log syslog-policy; edit <SYSLOG_POLICY>; config syslog-server-list; edit 1; set proto tls; set local-cert <ADMIN_LOCAL_CERT>; next; end; next; end` |
| GUI | Dashboard interface modernization | 8.0.5 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| GUI | Navigation menu reorganization | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| FortiAI | FortiAI enhancements: visual reports and native tokens | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| API protection | Expanded security inspection for gRPC traffic | 8.0.7 and later | ALG `SRG-NET-000401-ALG-000127` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set grpc-security-policy <GRPC_POLICY>; next; end` |
| Client-side protection | Client-side protection visibility and enforcement (block mode for a client IP range) | 8.0.7 and later | ALG `SRG-NET-000228-ALG-000108`; ALG `SRG-NET-000288-ALG-000109` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set client-side-protection-policy <CSP_POLICY>; next; end` |
| Malware and files | Antivirus scanning and verdict handling enhancements | 8.0.7 and later | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000249-ALG-000134` | `config system antivirus; set default-db extended; end` |
| API protection | MCP validation and attack investigation enhancements | 8.0.7 and later | ALG `SRG-NET-000401-ALG-000127` | — |
| Malware and files | Protection against disguised and AI-generated file threats | 8.0.7 and later | ALG `SRG-NET-000248-ALG-000133`; ALG `SRG-NET-000765-ALG-000170` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set file-upload-policy <FILE_POLICY>; next; end` |
| Signatures | Centralized signature detection for structured and protocol traffic | 8.0.7 and later | ALG `SRG-NET-000318-ALG-000152`; ALG `SRG-NET-000318-ALG-000014`; ALG `SRG-NET-000318-ALG-000151` | `config waf web-protection-profile inline-protection; edit <PROFILE>; set signature-rule <SIGNATURE_POLICY>; next; end` |
| DoS protection | Resource-aware blocking capacity | 8.0.7 and later | ALG `SRG-NET-000705-ALG-000110` | — |
| Logging | OWASP Top 10 2025 alignment | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Sessions and cookies | Enhanced cookie replay protection | 8.0.7 and later | ALG `SRG-NET-000230-ALG-000113`; ALG `SRG-NET-000233-ALG-000115` | `config waf cookie-security; edit <COOKIE_POLICY>; set cookie-replay-protection-type IP; next; end` |
| Bot mitigation | CAPTCHA accessibility (audio CAPTCHA) | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Access control | Host name matching for URL access and URL encryption | 8.0.7 and later | ALG `SRG-NET-000015-ALG-000016` | — |
| API protection | MQTT-aware inspection for WebSocket traffic | 8.0.7 and later | ALG `SRG-NET-000401-ALG-000127` | — |
| API protection | Unicode safety scanning for JSON requests | 8.0.7 and later | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000380-ALG-000128` | `config waf json-validation rule; edit <RULE>; set unicode-safety-scan enable; next; end` |
| Logging | Detailed attack logs for JSON schema validation failures | 8.0.7 and later | ALG `SRG-NET-000074-ALG-000043` | — |
| Certificates and TLS | ML-DSA certificate support | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Certificates and TLS | In-place updates of local certificates | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Input validation | Expanded decoding of encoded request content | 8.0.7 and later | ALG `SRG-NET-000401-ALG-000127`; ALG `SRG-NET-000380-ALG-000128` | `config server-policy policy; edit <POLICY>; set decoding enable; set decoding-depth <DEPTH>; next; end` |
| Client management | Client management scoring redesign | 8.0.7 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Server policy | TCP half-close timeouts for proxied connections | 8.0.7 and later | ALG `SRG-NET-000213-ALG-000107` | `config server-policy policy; edit <POLICY>; set tcp-client-fin-timeout <SECONDS>; set tcp-server-fin-timeout <SECONDS>; next; end` |
| Server policy | Preserving DSCP markings across proxied connections | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | `config server-policy policy; edit <POLICY>; set dscp-forward disable; next; end` |
| Authentication | Multiple domain mappings for Kerberos realms | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Application delivery | LRU eviction for the web cache | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| System | Full log disk encryption (LUKS2) | 8.0.7 and later | ALG `SRG-NET-000098-ALG-000056`; NDM `SRG-APP-000231-NDM-000271` | `execute formatlogdisk luks` (erases the log disk and reboots; export logs first) |
| Firmware and configuration | Automatic firmware patch upgrades | 8.0.7 and later | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-000516-NDM-000335` | `config system fortiguard; set auto-firmware-upgrade disable; end` (when patches are installed through change control within the required time) |
| System | Encryption of stored configuration files | 8.0.7 and later | NDM `SRG-APP-000231-NDM-000271`; ALG `SRG-NET-000755-ALG-000150` | `config system global; set encrypt-cfgfile enable; end` |
| System | Periodic integrity monitoring of configuration files | 8.0.7 and later | NDM `SRG-APP-000380-NDM-000304`; ALG `SRG-NET-000700-ALG-000100` | — (automatic; review the integrity events in the event log) |
| System | Reserved huge-page memory for Intel QAT | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | FortiView bot analysis redesign | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | MCP traffic and security analytics dashboard | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Logging and monitoring | IP and client ID banning from FortiView | 8.0.7 and later | ALG `SRG-NET-000019-ALG-000018` | — |
| Tracking | JA4 fingerprints in custom tracking | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |
| Diagnostics | Machine-learning Redis diagnostics and targeted cleanup | 8.0.7 and later | No direct requirement; if unused, disable (ALG `SRG-NET-000131-ALG-000085`) | — |

### Requirement reference

The requirements used in the map and in this chapter's text, with their
severity in the current SRG releases:

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| ALG | `SRG-NET-000015-ALG-000016` | CAT II | The ALG must enforce approved authorizations for logical access to information and system resources by employing identity-based, role-based, and/or attribute-based security policies. |
| ALG | `SRG-NET-000018-ALG-000017` | CAT II | The ALG must enforce approved authorizations for controlling the flow of information within the network based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. |
| ALG | `SRG-NET-000019-ALG-000018` | CAT II | The ALG must restrict or block harmful or suspicious communications traffic by controlling the flow of information between interconnected networks based on attribute- and content-based inspection of the source, destination, headers, and/or content of the communications traffic. |
| ALG | `SRG-NET-000019-ALG-000019` | CAT II | The ALG must immediately use updates made to policy enforcement mechanisms such as policy filters, rules, signatures, and analysis algorithms for gateway and/or intermediary functions. |
| ALG | `SRG-NET-000041-ALG-000022` | CAT II | The ALG providing user access control intermediary services must display the Standard Mandatory DoD-approved Notice and Consent Banner before granting access to the network. |
| ALG | `SRG-NET-000062-ALG-000092` | CAT II | The ALG that stores secret or private keys must use FIPS-approved key management technology and processes in the production and control of private/secret cryptographic keys. |
| ALG | `SRG-NET-000062-ALG-000150` | CAT II | The ALG that provides intermediary services for TLS must be configured to comply with the required TLS settings in NIST SP 800-52. |
| ALG | `SRG-NET-000074-ALG-000043` | CAT II | The ALG must produce audit records containing information to establish what type of events occurred. |
| ALG | `SRG-NET-000077-ALG-000046` | CAT II | The ALG must produce audit records containing information to establish the source of the events. |
| ALG | `SRG-NET-000079-ALG-000048` | CAT II | The ALG must generate audit records containing information to establish the identity of any individual or process associated with the event. |
| ALG | `SRG-NET-000088-ALG-000054` | CAT II | The ALG must send an alert to, at a minimum, the information system security officer (ISSO) and system administrator (SA) when an audit processing failure occurs. |
| ALG | `SRG-NET-000098-ALG-000056` | CAT II | The ALG must protect audit information from unauthorized read access. |
| ALG | `SRG-NET-000131-ALG-000085` | CAT II | The ALG must not have unnecessary services and functions enabled. |
| ALG | `SRG-NET-000132-ALG-000087` | CAT II | The ALG must be configured to prohibit or restrict the use of functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. |
| ALG | `SRG-NET-000138-ALG-000063` | CAT II | The ALG providing user authentication intermediary services must uniquely identify and authenticate organizational users (or processes acting on behalf of organizational users). |
| ALG | `SRG-NET-000138-ALG-000088` | CAT II | The ALG providing user access control intermediary services must be configured with a pre-established trust relationship and mechanisms with appropriate authorities (e.g., Active Directory or AAA server) which validate user account access authorizations and privileges. |
| ALG | `SRG-NET-000140-ALG-000094` | CAT II | The ALG providing user authentication intermediary services must use multifactor authentication for network access to non-privileged accounts. |
| ALG | `SRG-NET-000147-ALG-000095` | CAT II | The ALG providing user authentication intermediary services must implement replay-resistant authentication mechanisms for network access to nonprivileged accounts. |
| ALG | `SRG-NET-000164-ALG-000100` | CAT II | The ALG that provides intermediary services for TLS must validate certificates used for TLS functions by performing RFC 5280-compliant certification path validation. |
| ALG | `SRG-NET-000166-ALG-000101` | CAT II | The ALG providing PKI-based user authentication intermediary services must map authenticated identities to the user account. |
| ALG | `SRG-NET-000202-ALG-000124` | CAT II | The ALG must deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception). |
| ALG | `SRG-NET-000213-ALG-000107` | CAT II | The ALG must terminate all network connections associated with a communications session at the end of the session, or as follows: for in-band management sessions (privileged sessions), the session must be terminated after 10 minutes of inactivity; and for user sessions (non-privileged session), the session must be terminated after 15 minutes of inactivity. |
| ALG | `SRG-NET-000228-ALG-000108` | CAT II | The ALG must detect, at a minimum, mobile code that is unsigned or exhibiting unusual behavior, has not undergone a risk assessment, or is prohibited for use based on a risk assessment. |
| ALG | `SRG-NET-000230-ALG-000113` | CAT II | The ALG must protect the authenticity of communications sessions. |
| ALG | `SRG-NET-000233-ALG-000115` | CAT II | The ALG must recognize only system-generated session identifiers. |
| ALG | `SRG-NET-000235-ALG-000118` | CAT II | The ALG must fail to a secure state upon failure of initialization, shutdown, or abort actions. |
| ALG | `SRG-NET-000236-ALG-000119` | CAT II | In the event of a system failure of the ALG function, the ALG must save diagnostic information, log system messages, and load the most current security policies, rules, and signatures when restarted. |
| ALG | `SRG-NET-000246-ALG-000132` | CAT II | The ALG providing content filtering must update malicious code protection mechanisms and signature definitions whenever new releases are available in accordance with organizational configuration management policy. |
| ALG | `SRG-NET-000248-ALG-000133` | CAT II | The ALG providing content filtering must be configured to perform real-time scans of files from external sources at network entry/exit points as they are downloaded and prior to being opened or executed. |
| ALG | `SRG-NET-000249-ALG-000134` | CAT II | The ALG providing content filtering must block malicious code upon detection. |
| ALG | `SRG-NET-000249-ALG-000146` | CAT II | The ALG providing content filtering must send an immediate (within seconds) alert to the system administrator, at a minimum, in response to malicious code detection. |
| ALG | `SRG-NET-000273-ALG-000129` | CAT II | The ALG must generate error messages that provide the information necessary for corrective actions without revealing information that could be exploited by adversaries. |
| ALG | `SRG-NET-000288-ALG-000109` | CAT II | The ALG providing content filtering must block or restrict detected prohibited mobile code. |
| ALG | `SRG-NET-000318-ALG-000014` | CAT II | To protect against data mining, the ALG providing content filtering must prevent code injection attacks from being launched against data storage objects, including, at a minimum, databases, database records, queries, and fields. |
| ALG | `SRG-NET-000318-ALG-000151` | CAT II | To protect against data mining, the ALG providing content filtering must prevent code injection attacks launched against application objects including, at a minimum, application URLs and application code. |
| ALG | `SRG-NET-000318-ALG-000152` | CAT II | To protect against data mining, the ALG providing content filtering must prevent SQL injection attacks launched against data storage objects, including, at a minimum, databases, database records, and database fields. |
| ALG | `SRG-NET-000319-ALG-000015` | CAT II | To protect against data mining, the ALG providing content filtering must detect code injection attacks from being launched against data storage objects, including, at a minimum, databases, database records, queries, and fields. |
| ALG | `SRG-NET-000319-ALG-000020` | CAT II | To protect against data mining, the ALG providing content filtering must detect SQL injection attacks launched against data storage objects, including, at a minimum, databases, database records, and database fields. |
| ALG | `SRG-NET-000319-ALG-000153` | CAT II | To protect against data mining, the ALG providing content filtering as part of its intermediary services must detect code injection attacks launched against application objects including, at a minimum, application URLs and application code. |
| ALG | `SRG-NET-000334-ALG-000050` | CAT II | The ALG must off-load audit records onto a centralized log server. |
| ALG | `SRG-NET-000335-ALG-000053` | CAT II | The ALG must provide an immediate real-time alert to, at a minimum, the SCA and ISSO, of all audit failure events where the detection and/or prevention function is unable to write events to either local storage or the centralized server. |
| ALG | `SRG-NET-000339-ALG-000090` | CAT II | The ALG providing user authentication intermediary services must implement multifactor authentication for remote access to nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| ALG | `SRG-NET-000345-ALG-000099` | CAT II | The ALG providing user authentication intermediary services using PKI-based user authentication must implement a local cache of revocation data to support path discovery and validation in case of the inability to access revocation information via the network. |
| ALG | `SRG-NET-000355-ALG-000117` | CAT II | The ALG providing user authentication intermediary services using PKI-based user authentication must only accept end entity certificates issued by DoD PKI or DoD-approved PKI Certification Authorities (CAs) for the establishment of protected sessions. |
| ALG | `SRG-NET-000362-ALG-000112` | CAT II | The ALG providing content filtering must protect against known and unknown types of Denial of Service (DoS) attacks by employing rate-based attack prevention behavior analysis. |
| ALG | `SRG-NET-000362-ALG-000120` | CAT II | The ALG must implement load balancing to limit the effects of known and unknown types of Denial of Service (DoS) attacks. |
| ALG | `SRG-NET-000362-ALG-000155` | CAT II | The ALG providing content filtering must protect against or limit the effects of known and unknown types of Denial of Service (DoS) attacks by employing pattern recognition pre-processors. |
| ALG | `SRG-NET-000364-ALG-000122` | CAT II | The ALG must only allow incoming communications from organization-defined authorized sources routed to organization-defined authorized destinations. |
| ALG | `SRG-NET-000365-ALG-000123` | CAT II | The ALG must fail securely in the event of an operational failure. |
| ALG | `SRG-NET-000380-ALG-000128` | CAT II | The ALG must behave in a predictable and documented manner that reflects organizational and system objectives when invalid inputs are received. |
| ALG | `SRG-NET-000390-ALG-000139` | CAT II | The ALG providing content filtering must continuously monitor inbound communications traffic crossing internal security boundaries for unusual or unauthorized activities or conditions. |
| ALG | `SRG-NET-000391-ALG-000140` | CAT II | The ALG providing content filtering must continuously monitor outbound communications traffic crossing internal security boundaries for unusual/unauthorized activities or conditions. |
| ALG | `SRG-NET-000392-ALG-000141` | CAT II | The ALG providing content filtering must send an alert to, at a minimum, the ISSO and ISSM when detection events occur. |
| ALG | `SRG-NET-000392-ALG-000142` | CAT II | The ALG providing content filtering must generate an alert to, at a minimum, the ISSO and ISSM when threats identified by authoritative sources (e.g., IAVMs or CTOs) are detected. |
| ALG | `SRG-NET-000392-ALG-000148` | CAT II | The ALG providing content filtering must generate an alert to, at a minimum, the ISSO and ISSM when denial of service incidents are detected. |
| ALG | `SRG-NET-000400-ALG-000097` | CAT I | The ALG providing user authentication intermediary services must transmit only encrypted representations of passwords. |
| ALG | `SRG-NET-000401-ALG-000127` | CAT II | The ALG must check the validity of all data inputs except those specifically identified by the organization. |
| ALG | `SRG-NET-000402-ALG-000130` | CAT II | The ALG must reveal error messages only to the ISSO, ISSM, and SCA. |
| ALG | `SRG-NET-000503-ALG-000038` | CAT II | The ALG providing user access control intermediary services must generate audit records when successful/unsuccessful logon attempts occur. |
| ALG | `SRG-NET-000510-ALG-000025` | CAT II | The ALG providing encryption intermediary services must implement NIST FIPS-validated cryptography to generate cryptographic hashes. |
| ALG | `SRG-NET-000510-ALG-000111` | CAT II | The ALG providing encryption intermediary services must use NIST FIPS-validated cryptography to implement encryption services. |
| ALG | `SRG-NET-000511-ALG-000051` | CAT II | The ALG must off-load audit records onto a centralized log server in real time. |
| ALG | `SRG-NET-000512-ALG-000062` | CAT II | The ALG must be configured in accordance with the security configuration settings based on DoD security policy and technology-specific security best practices. |
| ALG | `SRG-NET-000512-ALG-000065` | CAT II | The ALG that provides intermediary services for FTP must inspect inbound and outbound FTP communications traffic for protocol compliance and protocol anomalies. |
| ALG | `SRG-NET-000512-ALG-000066` | CAT II | The ALG that provides intermediary services for HTTP must inspect inbound and outbound HTTP traffic for protocol compliance and protocol anomalies. |
| ALG | `SRG-NET-000517-ALG-000006` | CAT II | The ALG providing user access control intermediary services must automatically terminate a user session when organization-defined conditions or trigger events that require a session disconnect occur. |
| ALG | `SRG-NET-000575-ALG-000020` | CAT II | The ALG must use a FIPS-validated cryptographic module to implement encryption services for unclassified information requiring confidentiality. |
| ALG | `SRG-NET-000700-ALG-000100` | CAT II | The ALG must prevent or restrict changes to the configuration of the system under organization-defined circumstances. |
| ALG | `SRG-NET-000705-ALG-000110` | CAT II | The ALG must employ organization-defined controls by type of denial of service (DoS) to achieve the DoS objective. |
| ALG | `SRG-NET-000735-ALG-000130` | CAT II | The ALG must implement antispoofing mechanisms to prevent adversaries from falsifying the security attributes indicating the successful application of the security process. |
| ALG | `SRG-NET-000750-ALG-000140` | CAT II | The ALG must include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| ALG | `SRG-NET-000755-ALG-000150` | CAT II | The ALG must provide protected storage for cryptographic keys with organization-defined safeguards and/or hardware protected key store. |
| ALG | `SRG-NET-000765-ALG-000170` | CAT II | The ALG must implement signature based and/or nonsignature based malicious code protection mechanisms at system entry and exit points to detect and eradicate malicious code. |
| NDM | `SRG-APP-000001-NDM-000200` | CAT II | The network device must limit the number of concurrent sessions to an organization-defined number for each administrator account and/or administrator account type. |
| NDM | `SRG-APP-000026-NDM-000208` | CAT II | The network device must automatically audit account creation. |
| NDM | `SRG-APP-000033-NDM-000212` | CAT I | The network device must be configured to assign appropriate user roles or access levels to authenticated users. |
| NDM | `SRG-APP-000038-NDM-000213` | CAT II | The network device must enforce approved authorizations for controlling the flow of management information within the network device based on information flow control policies. |
| NDM | `SRG-APP-000065-NDM-000214` | CAT II | The network device must be configured to enforce the limit of three consecutive invalid logon attempts, after which time it must block any login attempt for 15 minutes. |
| NDM | `SRG-APP-000068-NDM-000215` | CAT II | The network device must display the Standard Mandatory DoD Notice and Consent Banner before granting access to the device. |
| NDM | `SRG-APP-000095-NDM-000225` | CAT II | The network device must produce audit log records containing sufficient information to establish what type of event occurred. |
| NDM | `SRG-APP-000101-NDM-000231` | CAT II | The network device must generate audit records containing the full-text recording of privileged commands. |
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
| NDM | `SRG-APP-000171-NDM-000258` | CAT I | The network device must be configured to store passwords using an approved salted key derivation function, preferably using a keyed hash for password-based authentication. |
| NDM | `SRG-APP-000172-NDM-000259` | CAT I | The network device must transmit only encrypted representations of passwords. |
| NDM | `SRG-APP-000175-NDM-000262` | CAT I | The network device must be configured to use DoD approved OCSP responders or CRLs to validate certificates used for PKI-based authentication. |
| NDM | `SRG-APP-000177-NDM-000263` | CAT I | The network device, for PKI-based authentication, must be configured to map validated certificates to unique user accounts. |
| NDM | `SRG-APP-000179-NDM-000265` | CAT I | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| NDM | `SRG-APP-000190-NDM-000267` | CAT I | The network device must terminate all network connections associated with a device management session at the end of the session, or the session must be terminated after five minutes of inactivity except to fulfill documented and validated mission requirements. |
| NDM | `SRG-APP-000231-NDM-000271` | CAT I | The network device must only allow authorized administrators to view or change the device configuration, system files, and other files stored either in the device or on removable media (such as a flash drive). |
| NDM | `SRG-APP-000357-NDM-000293` | CAT II | The network device must allocate audit record storage capacity in accordance with organization-defined audit record storage requirements. |
| NDM | `SRG-APP-000360-NDM-000295` | CAT II | The network device must generate an immediate real-time alert of all audit failure events requiring real-time alerts. |
| NDM | `SRG-APP-000374-NDM-000299` | CAT II | The network device must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). |
| NDM | `SRG-APP-000380-NDM-000304` | CAT II | The network device must enforce access restrictions associated with changes to device configuration. |
| NDM | `SRG-APP-000395-NDM-000310` | CAT II | The network device must be configured to authenticate SNMP messages using a FIPS-validated Keyed-Hash Message Authentication Code (HMAC). |
| NDM | `SRG-APP-000395-NDM-000347` | CAT II | The network device must authenticate Network Time Protocol sources using authentication that is cryptographically based. |
| NDM | `SRG-APP-000408-NDM-000314` | CAT II | Network devices performing maintenance functions must restrict use of these functions to authorized personnel only. |
| NDM | `SRG-APP-000411-NDM-000330` | CAT I | The network devices must use FIPS-validated Keyed-Hash Message Authentication Code (HMAC) to protect the integrity of nonlocal maintenance and diagnostic communications. |
| NDM | `SRG-APP-000412-NDM-000331` | CAT I | The network device must be configured to implement cryptographic mechanisms using a FIPS 140-2 approved algorithm to protect the confidentiality of remote maintenance sessions |
| NDM | `SRG-APP-000457-NDM-000352` | CAT II | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| NDM | `SRG-APP-000503-NDM-000320` | CAT II | The network device must generate audit records when successful/unsuccessful logon attempts occur. |
| NDM | `SRG-APP-000505-NDM-000322` | CAT II | The network device must generate audit records showing starting and ending time for administrator access to the system. |
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000335` | CAT II | The network device must enforce access restrictions associated with changes to the system components. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000344` | CAT II | The network device must obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000820-NDM-000170` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| NDM | `SRG-APP-000860-NDM-000250` | CAT II | The network device must be configured to allow user selection of long passwords and passphrases, including spaces and all printable characters for password-based authentication. |
| NDM | `SRG-APP-000875-NDM-000280` | CAT II | The network device must be configured to implement certificate revocation checking to support path discovery and validation for public key-based authentication. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |

### Collecting evidence

Enter `show` in each configuration section that the map cites, at least
`config system global`, `config system admin`, `config system accprofile`,
`config system password-policy`, `config system interface`,
`config system ntp`, `config system snmp user`, `config system fips-cc`,
`config log syslog-policy`, `config server-policy policy`, and
`config waf web-protection-profile inline-protection`, and run
`get system status` for the release, FIPS-CC state, and log disk state.
Export the event and attack logs from the central log server, record the
operation mode, and keep the FortiGuard update status and the firmware
checksum record with the checklist.

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiWeb.** Check the version
  column against the FortiWeb OS release, and check whether the feature
  applies to your platform (hardware, FortiWeb-VM, or one public cloud).
- **A command is rejected.** The command was checked against the 8.0.8 CLI
  Reference. Older releases may lack the option or spell it differently;
  check the CLI Reference of your release.
- **Attacks are logged but not blocked.** Check the operation mode, monitor
  mode in the server policy, and the action of the module (alert versus
  alert and deny).
- **Administrators cannot log in after hardening.** Check trusted hosts, the
  firewall admin policy, single administrator mode, the lockout, and, for
  PKI login, the PKI user, the administrator group, and the CA certificate.
- **A requirement has no matching feature.** Some requirements are met by
  procedure (firmware checksum, password changes), by another system (the
  authentication server, the central log server, an inline device for
  monitoring-only modes), or not at all on older releases (NTP
  authentication). Record how each requirement is met, not just which
  feature covers it.

## Security and Best Practices

- Keep FortiWeb on a vendor-supported release and install patches promptly,
  through change control or with automatic patch upgrades (8.0.7).
- Set administrator passwords of at least 15 characters, disable the default
  `admin` account (8.0.3 and later) once named accounts exist, and use DoD
  PKI or a remote authentication server for administrator login.
- Allow only HTTPS and SSH on the management interface, with TLS 1.2 or
  later, trusted hosts, and the pre-login banner.
- Send event and attack logs to a central log server over TLS, and use
  SNMPv3 with authentication and privacy only.
- Keep FortiGuard signature, IP reputation, and antivirus updates current,
  and review this map each time Fortinet publishes a FortiWeb release or
  DISA updates the ALG or NDM SRG.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiWeb Administration Guide*, "What's new" pages of releases
  7.0.0 to 7.4.13, and the "New Features in 7.6.x releases" (7.6.10) and
  "What's New" (8.0.8) chapters (docs.fortinet.com, FortiWeb
  documentation).
- Fortinet, *FortiWeb Release Notes* 7.2.1, 7.4.5, 7.6.0 to 7.6.10, 8.0.2 to
  8.0.6, and 8.0.8, section "What's new" (used for 7.2.1 and 7.4.5, and to
  confirm the 7.6 and 8.0 patch releases).
- Fortinet, *FortiWeb 8.0.8 CLI Reference* and *FortiWeb 8.0.8
  Administration Guide*.
- DISA Application Layer Gateway SRG V2R4 and Network Device Management SRG
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

1. Which two SRGs apply to FortiWeb, and which part of the appliance does
   each one cover?
2. Where does the version data come from, given that FortiWeb has no
   feature matrix or separate New Features Guide?
3. Why do Offline Protection and Transparent Inspection modes leave some ALG
   requirements to another device?
4. Which ALG requirements do not apply to FortiWeb, and why?
5. Which requirements can FortiWeb not meet exactly, and how do you handle
   them?
6. What applies to a feature marked "No direct requirement"?

## Summary and Completion Checklist

FortiWeb has no STIG, so it is assessed against the ALG SRG for its web
application firewall and the NDM SRG for its management plane. This chapter
maps 480 features to the FortiWeb OS release that introduced them, to
123 SRG requirements, and to the FortiWeb command that configures them:
76 core platform features, and 404 features from the
"What's new" lists of FortiWeb 7.0.0 through 8.0.8. Operational features
with no direct requirement fall under the requirement to disable unnecessary
functions when unused.

- [ ] Can find the release that introduced a FortiWeb feature.
- [ ] Can map a FortiWeb feature to its ALG or NDM SRG requirement.
- [ ] Can find the FortiWeb command that meets the requirement.
- [ ] Can choose an operation mode that enforces the ALG requirements.
- [ ] Can collect FortiWeb evidence and record the requirements FortiWeb
  cannot meet exactly.
