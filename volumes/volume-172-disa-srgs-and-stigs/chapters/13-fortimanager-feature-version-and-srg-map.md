# Chapter 13: FortiManager Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiManager release that introduced a given feature.
- Map each FortiManager feature to the DISA SRG requirement it helps satisfy.
- Find the CLI command, or the GUI location, that configures each feature to
  meet its SRG requirement.
- Use the map to scope an SRG-based assessment of a FortiManager, which has no
  STIG of its own.
- Explain why access control, auditing, and configuration-change control carry
  the most weight on a system that configures every managed device.

## Theory and Architecture

FortiManager has **no DISA STIG** (Chapter 10). It is the central management
system for FortiGates and other Fortinet devices: it holds their configuration,
pushes policy packages and templates to them, and upgrades their firmware.
Chapter 10 assigns it the **Network Device Management (NDM) SRG**. Chapter 03
describes SRG-based assessment. This chapter gives three pieces of information
for every FortiManager feature: **which release introduced it**, **which SRG
requirement it relates to**, and **which command configures it to meet that
requirement**.

Because a FortiManager administrator can change every managed device, the NDM
requirements for **access control** (roles, ADOMs, administrator profiles,
trusted hosts), **auditing** (event logs, off-loading, accounting), and
**configuration-change control** (who may change and install configuration,
and how changes are recorded, approved, and backed up) apply to FortiManager
with more force than to a single device. The map ties most template, script,
policy, and installation features to those requirements.

### Where the version data comes from

Fortinet does not publish a feature matrix for FortiManager. Instead, each
release train has a **New Features Guide** that lists every feature added in
that train and tags it with the patch release that introduced it. The version
column was built from all five guides Fortinet publishes for FortiManager 7.0,
7.2, 7.4, 7.6, and 8.0, which cover FortiManager 7.0.0 through 7.0.4, 7.2.0
through 7.2.10, 7.4.0 through 7.4.9, 7.6.0 through 7.6.7, and 8.0.0 through
8.0.1.

The feature titles come from each guide's table of contents on
docs.fortinet.com, which gives the full titles (the PDF bookmarks shorten long
titles) and folds sub-topics into their parent feature. For 7.0, 7.2, 7.4, and
8.0 the titles were checked against the PDF bookmarks and match. The 7.6 guide
PDF could not be downloaded (the attachment link returned HTTP 403), so its
online table of contents is the only source for 7.6. The example scenarios in
the appendix of the 7.2 guide are not features and are not listed.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that most NDM requirements depend on: management
  access, administrators, auditing, time, certificates, backup, and the central
  management functions themselves. They existed before 7.0.0 and are not in any
  New Features Guide.
- **New features** are every topic in the five New Features Guides, under the
  guide's own category names (the 7.4 *Security Fabric* category is listed as
  *Fabric View*, its name in the other trains).

| Version entry | Meaning |
| --- | --- |
| `7.0.0 or earlier` | A core platform feature, present in 7.0.0 and earlier releases |
| `7.4.2 and later` | Introduced in 7.4.2; later release trains include it |
| `7.2.10+; 7.4.7+; 7.6.3+` | Introduced in several release trains at different patch levels (often backported); the first release in each train is shown |
| `Not in a New Features Guide` | Documented in the 8.0.1 CLI Reference, but no guide records the release that introduced it |

Two cautions apply. First, a feature introduced in a patch release of an older
train (for example 7.4.8) may reach a newer train only in that train's later
patches, so "and later" means later in the same train and, usually, in later
trains. Check the release notes for your exact release. Second, some features
apply only to certain models or licenses (for example FortiAI, the TPM, and
the cloud marketplace features).

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG | Release | Applies to |
| --- | --- | --- |
| **Network Device Management (NDM)** | V5R5 | The FortiManager management plane: administrator accounts, roles, and authentication; sessions and banners; audit records and their protection and off-loading; configuration-change control and backup; cryptography for management traffic; time; and supported, signed firmware |

FortiManager is not a traffic-forwarding device and does not store the managed
devices' logs as its main job, so no other SRG in the library fits it better.
If the optional FortiAnalyzer features are enabled on a FortiManager, assess
that part against the Central Log Server SRG as Chapter 12 describes, or
disable it.

Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiManager meets a
  requirement. Workflow mode implements approval and recording of
  configuration changes, for example.
- **Must be configured to meet a requirement.** The feature is in scope of a
  requirement and has to be set up correctly. Provisioning templates change
  the configuration of managed devices, so access to them must be limited to
  authorized administrators (`SRG-APP-000380-NDM-000304`), for example.
- **No direct requirement.** The feature is operational or cosmetic, such as
  an SD-WAN monitoring widget or a cloud marketplace image. It has no
  requirement of its own, but if it is not needed it falls under the NDM
  requirement to prohibit unnecessary functions
  (`SRG-APP-000142-NDM-000245`).

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially where a requirement is organization-defined.

### Where the commands come from

Every `config` path, `set` option, option value, and `execute` command in the
command column was checked against the **FortiManager 8.0.1 CLI Reference**:
each `set` option against the syntax of the `config` path it is entered under,
and each listed value against the documented values. Read the column this way:

- Statements are separated by `;` to fit in a table cell; on the CLI, enter
  each one on its own line. Values in `<ANGLE_BRACKETS>` are placeholders for
  your own names, addresses, and keys.
- Most template, policy, and installation features are used in the **GUI**.
  For a feature that changes managed devices, the column gives the
  administrator profile permission that limits who can use it (for example
  `set device-profile read` for provisioning templates or
  `set deploy-management none` for installation). Grant `read-write` only in
  the profiles of administrators authorized to make that change.
- Where nothing in the CLI configures a feature, the column names the GUI pane
  (for example *GUI: Policy & Objects*) instead of a CLI command.
- For **"No direct requirement"** rows, a command is shown only when the
  feature can be turned off (for example `set ai-mode disable` for FortiAI or
  `set lldp-transmission disable` for LLDP). A dash (**—**) means there is
  nothing to configure: the feature is a monitoring view, a GUI change, a
  license or platform change, or a capability used only when needed.
- Some rows point to another row (for example, the JSON API backup relies on
  the *Scheduled configuration backup* row).

Some requirements cannot be met exactly with FortiManager settings alone.
Record them on the checklist as open findings with mitigations, or meet them
by procedure:

- **Password change.** The password policy can require that at least 4
  characters change (`change-4-characters`); the NDM SRG requires 8
  (`SRG-APP-000170-NDM-000329`). Use remote authentication (RADIUS, TACACS+,
  LDAP, or PKI) so the authentication server enforces the policy.
- **Compromised passwords.** The 8.0.1 CLI Reference has no setting that checks
  new passwords against a list of commonly used or compromised passwords
  (`SRG-APP-000845-NDM-000220`). Meet it on the authentication server.
- **Account of last resort.** Nothing in FortiManager limits the number of
  local accounts (`SRG-APP-000148-NDM-000346`). Keep one local emergency
  account, make every other administrator a remote (RADIUS, TACACS+, LDAP, or
  PKI) account, and review the account list.
- **Certificate revocation.** `config system certificate crl` holds imported
  CRLs, and the CLI Reference has no OCSP or automatic CRL download setting.
  Keep CRLs current by procedure, or meet `SRG-APP-000175-NDM-000262` and
  `SRG-APP-000875-NDM-000280` on the authentication server.
- **Full-text recording of privileged commands.** The event log records
  configuration changes; full command text (`SRG-APP-000101-NDM-000231`) comes
  from TACACS+ accounting (`cli-cmd-audit`), which needs a TACACS+ server.
- **NTP and SNMP cryptography on older releases.** The New Features Guides
  introduce NTPv4 with SHA-256 (`key-type sha256`) in 8.0.0, and SHA-224 to
  SHA-512 authentication and AES-256 privacy for SNMPv3 in 7.6.0. On older
  releases, record the finding and plan the upgrade.
- **FIPS-CC mode** can be enabled only from the console.

## Design Considerations

- **Treat FortiManager as tier zero.** It can change every managed device, so
  a compromised FortiManager account is a compromise of the whole estate.
  Place it on a dedicated management network, restrict it with trusted hosts
  and local-in policies, and use remote authentication with MFA.
- **Pick the release first, then the features.** If your design depends on a
  feature introduced in a certain release (for example NTPv4 with SHA-256 in
  8.0.0, or USB port control in 8.0.1), that sets the minimum FortiManager
  version, and the firmware must also be a vendor-supported release
  (`SRG-APP-001035-NDM-000340`).
- **Design the administrator profiles before the ADOMs fill up.** Separate who
  may edit templates and policy packages, who may install them, who may run
  scripts, and who may upgrade firmware. The profile permissions in the
  command column are the building blocks.
- **Make every change traceable.** Use workflow mode (or at least workspace
  mode), mandatory change notes, revision history, custom session labels, and
  TACACS+ accounting, and send the event log to a central log server in real
  time.
- **Keep the STIG settings in FortiManager.** The managed FortiGates' STIG
  settings belong in provisioning templates, CLI templates, and policy
  packages, so a reinstall cannot silently remove them. The FortiGate STIGs
  (Chapter 10) define those settings; this chapter covers the FortiManager
  itself.
- **Disable what you do not use.** FortiAI, the FortiAnalyzer features,
  Management Extension Applications, the FortiGuard distribution services,
  Fabric of FortiManager, and cloud features should be off unless they serve a
  documented purpose.

## Implementation and Automation

### The FortiManager feature map

Abbreviation in the SRG column: **NDM** is the Network Device Management SRG.
The requirement titles are listed in the next table. The command column
follows the conventions in *Where the commands come from*.

| Category | Feature | Introduced (FortiManager) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: management access | HTTPS and SSH management encryption | 7.0.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000172-NDM-000259`; NDM `SRG-APP-000179-NDM-000265` | `config system global; set global-ssl-protocol tlsv1.2; set ssl-low-encryption disable; set enc-algorithm high; set ssh-enc-algo aes256-ctr aes256-gcm@openssh.com; set ssh-mac-algo hmac-sha2-256 hmac-sha2-512; end` |
| Core: management access | Interface administrative access | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000408-NDM-000314` | `config system interface; edit <PORT>; set allowaccess https ssh; end` (no `http`, `snmp`, or `fabric` unless required) |
| Core: management access | Trusted hosts for administrators | 7.0.0 or earlier | NDM `SRG-APP-000038-NDM-000213`; NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000880-NDM-000290` | `config system admin user; edit <ADMIN>; set trusthost1 <IP> <MASK>; end` |
| Core: management access | Pre-login banner | 7.0.0 or earlier | NDM `SRG-APP-000068-NDM-000215`; NDM `SRG-APP-000069-NDM-000216` | `config system global; set pre-login-banner enable; set pre-login-banner-message <DOD_BANNER>; end` |
| Core: management access | Post-login access banner | 7.0.0 or earlier | NDM `SRG-APP-000068-NDM-000215` | `config system admin setting; set access-banner enable; set banner-message <DOD_BANNER>; end` |
| Core: management access | Idle session timeout | 7.0.0 or earlier | NDM `SRG-APP-000190-NDM-000267` | `config system admin setting; set idle_timeout 300; set idle_timeout_gui 300; set idle_timeout_api 300; end` |
| Core: management access | Concurrent administrator sessions | 7.0.0 or earlier | NDM `SRG-APP-000001-NDM-000200` | `config system admin setting; set admin-login-max <NUMBER>; end` and `config system admin user; edit <ADMIN>; set login-max <NUMBER>; end` |
| Core: management access | Administrator lockout | 7.0.0 or earlier | NDM `SRG-APP-000065-NDM-000214` | `config system global; set admin-lockout-threshold 3; set admin-lockout-duration 900; set admin-lockout-method user; end` |
| Core: management access | FIPS-CC mode | 7.0.0 or earlier | NDM `SRG-APP-000179-NDM-000265`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330` | `config system fips; set status enable; end` |
| Core: management access | Private data encryption | 7.0.0 or earlier | NDM `SRG-APP-000231-NDM-000271` | `config system global; set private-data-encryption enable; end` |
| Core: management access | Debug tool | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245` | `config system global; set debug-tool disable; end` |
| Core: administrators | Individual administrator accounts | 7.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000153-NDM-000249`; NDM `SRG-APP-000026-NDM-000208` | `config system admin user; edit <ADMIN>; set profileid <PROFILE>; set adom <ADOM>; end` |
| Core: administrators | Account of last resort | 7.0.0 or earlier | NDM `SRG-APP-000148-NDM-000346` | `config system admin user; edit <EMERGENCY_ADMIN>; set user_type local; set profileid <PROFILE>; end` (one local account only; all others remote) |
| Core: administrators | Administrator profiles (role-based access) | 7.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287`; NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set system-setting none; set device-manager read; set policy-objects read; set deploy-management none; end` |
| Core: administrators | Administrative domains (ADOMs) | 7.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000038-NDM-000213`; NDM `SRG-APP-000380-NDM-000304` | `config system global; set adom-status enable; end` |
| Core: administrators | Password policy | 7.0.0 or earlier | NDM `SRG-APP-000164-NDM-000252`; NDM `SRG-APP-000166-NDM-000254`; NDM `SRG-APP-000167-NDM-000255`; NDM `SRG-APP-000168-NDM-000256`; NDM `SRG-APP-000169-NDM-000257`; NDM `SRG-APP-000170-NDM-000329` | `config system password-policy; set status enable; set minimum-length 15; set must-contain upper-case-letter lower-case-letter number non-alphanumeric; set change-4-characters enable; end` |
| Core: administrators | RADIUS administrator authentication | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000156-NDM-000250` | `config system admin radius; edit <RADIUS>; set server <IP>; set secondary-server <IP>; set secret <SECRET>; set protocol tls; set message-authenticator require; end` |
| Core: administrators | TACACS+ administrator authentication | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000153-NDM-000249` | `config system admin tacacs; edit <TACACS>; set server <IP>; set secondary-server <IP>; set key <KEY>; set protocol tls; set authorization enable; end` |
| Core: administrators | LDAP administrator authentication | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000336` | `config system admin ldap; edit <LDAP>; set server <IP>; set secure ldaps; set ca-cert <CA_CERT>; end` |
| Core: administrators | PKI (certificate) administrator authentication | 7.0.0 or earlier | NDM `SRG-APP-000149-NDM-000247`; NDM `SRG-APP-000177-NDM-000263`; NDM `SRG-APP-000175-NDM-000262`; NDM `SRG-APP-000875-NDM-000280` | `config system admin user; edit <ADMIN>; set user_type pki-auth; set subject <CERT_SUBJECT>; set ca <CA_CERT>; end` and `config system global; set clt-cert-req enable; end` |
| Core: administrators | JSON API administrators | 7.0.0 or earlier | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000038-NDM-000213` | `config system admin user; edit <API_ADMIN>; set user_type api; set rpc-permit read-only; set trusthost1 <IP> <MASK>; end` |
| Core: auditing | FortiManager event log (own audit records) | 7.0.0 or earlier | NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000096-NDM-000226`; NDM `SRG-APP-000097-NDM-000227`; NDM `SRG-APP-000098-NDM-000228`; NDM `SRG-APP-000099-NDM-000229`; NDM `SRG-APP-000100-NDM-000230`; NDM `SRG-APP-000092-NDM-000224`; NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000091-NDM-000223`; NDM `SRG-APP-000505-NDM-000322`; NDM `SRG-APP-000026-NDM-000208`; NDM `SRG-APP-000027-NDM-000209`; NDM `SRG-APP-000028-NDM-000210`; NDM `SRG-APP-000029-NDM-000211`; NDM `SRG-APP-000495-NDM-000318` | `config system locallog disk setting; set status enable; set severity information; end` |
| Core: auditing | Event log filters for configuration changes | 7.0.0 or earlier | NDM `SRG-APP-000381-NDM-000305`; NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000504-NDM-000321`; NDM `SRG-APP-000080-NDM-000220` | `config system locallog disk filter; set event enable; set devcfg enable; set dm enable; set dvm enable; set objcfg enable; set scply enable; set system enable; end` |
| Core: auditing | Event log access restriction | 7.0.0 or earlier | NDM `SRG-APP-000119-NDM-000236`; NDM `SRG-APP-000120-NDM-000237`; NDM `SRG-APP-000121-NDM-000238` | `config system admin profile; edit <PROFILE>; set system-setting none; end` (only auditors and security administrators get System Settings) |
| Core: auditing | Event log storage and disk-full alerting | 7.0.0 or earlier | NDM `SRG-APP-000357-NDM-000293`; NDM `SRG-APP-000360-NDM-000295` | `config system locallog disk setting; set log-disk-quota <MB>; set log-disk-full-percentage 75; end` and `config system locallog setting; set log-interval-disk-full <MINUTES>; end` |
| Core: auditing | Sending FortiManager event logs to a syslog server | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000350`; NDM `SRG-APP-000515-NDM-000325` | `config system syslog; edit <SYSLOG>; set ip <SYSLOG_IP>; set reliable enable; end` and `config system locallog syslogd setting; set status enable; set syslog-name <SYSLOG>; set severity information; end` |
| Core: auditing | Sending FortiManager event logs to FortiAnalyzer | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000350`; NDM `SRG-APP-000515-NDM-000325` | `config system locallog fortianalyzer setting; set status realtime; set server <FAZ_IP>; set secure-connection enable; set reliable enable; end` |
| Core: auditing | TACACS+ accounting of CLI commands, configuration changes, and logins | Not in a New Features Guide (in the 8.0.1 CLI Reference) | NDM `SRG-APP-000101-NDM-000231`; NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000503-NDM-000320`; NDM `SRG-APP-000515-NDM-000325` | `config system locallog tacacs+accounting setting; set status enable; set tacacs-name <TACACS>; end` and `config system locallog tacacs+accounting filter; set cli-cmd-audit enable; set config-change-audit enable; set login-audit enable; end` |
| Core: auditing | Alert email (SMTP) | 7.0.0 or earlier | NDM `SRG-APP-000360-NDM-000295`; NDM `SRG-APP-000795-NDM-000130` | `config system mail; edit <ID>; set server <SMTP_IP>; set secure-option starttls; set auth enable; end` |
| Core: time and monitoring | NTP server | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000347`; NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000925-NDM-000330`; NDM `SRG-APP-000374-NDM-000299`; NDM `SRG-APP-000116-NDM-000234` | `config system ntp; set status enable; config ntpserver; edit 1; set server <NTP_IP>; set authentication enable; set key-type sha256; set key-id <ID>; set key <KEY>; end; end` |
| Core: time and monitoring | SNMPv3 | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310` | `config system snmp user; edit <USER>; set security-level auth-priv; set auth-proto sha; set priv-proto aes; end` |
| Core: time and monitoring | SNMP v1 and v2c communities | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245` | `config system snmp community; edit <ID>; set status disable; end` |
| Core: certificates | CA certificates and CRLs | 7.0.0 or earlier | NDM `SRG-APP-000910-NDM-000300`; NDM `SRG-APP-000875-NDM-000280`; NDM `SRG-APP-000175-NDM-000262` | `config system certificate ca; edit <CA>; set ca <CERTIFICATE>; end` and `config system certificate crl; edit <CRL>; set crl <CRL>; end` |
| Core: certificates | Management (HTTPS) server certificate | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000344` | `config system admin setting; set admin_server_cert <DOD_ISSUED_CERT>; end` |
| Core: backup and firmware | Scheduled configuration backup | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340`; NDM `SRG-APP-000516-NDM-000341` | `config system backup all-settings; set status enable; set protocol sftp; set server <IP>; set user <USER>; set passwd <PASSWORD>; set crptpasswd <ENCRYPTION_PASSWORD>; set week_days <DAYS>; set time <HH:MM:SS>; end` |
| Core: backup and firmware | On-demand configuration backup | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340` | `execute backup all-settings sftp <IP:PORT> <FILE> <USER> <PASSWORD>` |
| Core: backup and firmware | FortiManager firmware upgrade | 7.0.0 or earlier | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000131-NDM-000243`; NDM `SRG-APP-000378-NDM-000302`; NDM `SRG-APP-000133-NDM-000244` | `execute restore image sftp <IMAGE_PATH> <IP:PORT> <USER> <PASSWORD>` (use a vendor-supported release) |
| Core: backup and firmware | High availability (HA) | 7.0.0 or earlier | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Core: central management | FortiGate-to-FortiManager (FGFM) management tunnel | 7.0.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330`; NDM `SRG-APP-000516-NDM-000335` | `config system global; set fgfm-ssl-protocol tlsv1.2; set fgfm-cert-exclusive enable; set fgfm-deny-unknown enable; end` |
| Core: central management | Device registration and authorization | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000335`; NDM `SRG-APP-000380-NDM-000304` | `config system admin setting; set allow_register disable; set unreg_dev_opt add_no_service; end` |
| Core: central management | Adding and deleting managed devices | 7.0.0 or earlier | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | `config system admin profile; edit <PROFILE>; set device-op none; end` |
| Core: central management | Policy packages and installation to devices | 7.0.0 or earlier | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000340-NDM-000288` | `config system admin profile; edit <PROFILE>; set adom-policy-packages read; set deploy-management none; end` |
| Core: central management | Provisioning templates | 7.0.0 or earlier | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Core: central management | CLI and TCL scripts | 7.0.0 or earlier | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000142-NDM-000245` | `config system admin profile; edit <PROFILE>; set script-access none; set script-run none; end` and `config system admin setting; set show_tcl_script disable; end` |
| Core: central management | Device configuration revision history and revert | 7.0.0 or earlier | NDM `SRG-APP-000381-NDM-000305`; NDM `SRG-APP-000516-NDM-000340`; NDM `SRG-APP-000080-NDM-000220` | `config system dm; set max-revs <NUMBER>; end` and `config system admin profile; edit <PROFILE>; set config-revert none; set device-revision-deletion none; end` |
| Core: central management | ADOM revision history | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340`; NDM `SRG-APP-000381-NDM-000305` | `config system global; set adom-rev-auto-delete by-revisions; set adom-rev-max-revisions <NUMBER>; end` |
| Core: central management | Workspace mode (ADOM and policy package locking) | 7.0.0 or earlier | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000080-NDM-000220` | `config system global; set workspace-mode normal; end` |
| Core: central management | Workflow mode (change approval) | 7.0.0 or earlier | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000381-NDM-000305`; NDM `SRG-APP-000080-NDM-000220` | `config system global; set workspace-mode workflow; end` and `config system workflow approval-matrix; edit <ADOM>; set mail-server <SMTP>; config approver; edit 1; set member <APPROVERS>; end; end` |
| Core: central management | Install verification against the device configuration | 7.0.0 or earlier | NDM `SRG-APP-000380-NDM-000304` | `config system dm; set verify-install enable; end` |
| Core: central management | Terminal (CLI) access to managed devices | 7.0.0 or earlier | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000340-NDM-000288` | `config system admin profile; edit <PROFILE>; set term-access none; end` |
| Core: central management | FortiGuard Distribution Server for managed devices | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245` | If unused: `config fmupdate service; set avips disable; set query-webfilter disable; set query-antispam disable; end` |
| Core: central management | FortiAnalyzer features on FortiManager | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245` | `config system global; set faz-status disable; end` |
| Device Manager | Model HA Cluster Wizard Improvements | 7.0.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | `config system admin profile; edit <PROFILE>; set device-op none; end` |
| Device Manager | More secure request authorization with OAuth protocol | 7.0.0 and later | NDM `SRG-APP-000516-NDM-000335`; NDM `SRG-APP-000412-NDM-000331` | GUI: Device Manager (Add Device wizard, OAuth method) |
| Device Manager | Normalized interfaces support wildcard definition to match multiple objects | 7.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Device Manager | Centralized view for all detected devices within an ADOM | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | View managed FortiGates and all connected devices in one pane | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | New SD-WAN template | 7.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | SD-WAN monitoring improvements | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | SD-WAN monitoring shows the SD-WAN rule and its status, active selected member for a given SLA | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Improved GUI SD-WAN monitoring : SD-WAN rules view, SD-WAN status | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | SD-WAN real-time monitoring (30 seconds) supported per-device | 7.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Fortinet recommended default IPSec and BGP templates for SD-WAN overlay setup | 7.0.3 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000412-NDM-000331` | `config system admin profile; edit <PROFILE>; set device-profile read; end` (review the IPsec proposals against the FortiGate STIG) |
| Device Manager | Interface template support for meta fields | 7.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Static route template with support for meta fields | 7.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Pre-defined IPsec template with recommended settings | 7.0.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000412-NDM-000331` | `config system admin profile; edit <PROFILE>; set device-profile read; end` (review the IPsec proposals against the FortiGate STIG) |
| Device Manager | Un-assign IPsec template to remove VPN-related configuration | 7.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | CLI Template improvements | 7.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | IPsec template enhanced support for tunnel interface configuration | 7.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Templates support assignment to device groups | 7.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | BGP template to manage all BGP routing configurations | 7.0.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Import IPSec VPN configuration from a managed FortiGate into a IPSec template | 7.0.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Pre-run CLI template runs once on model device to preconfigure it with required settings | 7.0.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | New Model Device page allows assigning script, provisioning template, and template group | 7.0.2 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | `config system admin profile; edit <PROFILE>; set device-op none; end` and `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Improved templates usability with Template Group | 7.0.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Import BGP routing configuration from a managed FortiGate into a template | 7.0.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Template Group supports the FortiAP, FortiSwitch, and FortiExtender templates | 7.0.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Direct export and import configuration | 7.0.4 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000516-NDM-000340` | `config system admin profile; edit <PROFILE>; set device-op none; end` |
| Device Manager | FortiExtenders Profiles used to managed the WAN/LAN extensions and configuration import from FortiGate support | 7.0.4 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiextender read; end` |
| Device Manager | Firmware template | 7.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set fgd-center-fmw-mgmt read; set device-fwm-profile read; end` |
| Central Management | AP Manager displays AP temperature value under Diagnostics and Tools | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiSwitch Manager central management improvements | 7.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | FortiSwitch per-device management improvements | 7.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | Diagnostics and tools for device health monitoring and registration with FortiCloud | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Extender Manager for central managed FortiExtender devices | 7.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiextender read; end` |
| Central Management | FortiExtender Template for ZTP | 7.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiextender read; end` |
| Central Management | Retrieve and display RSSI information for FGT-xx-3G4G models | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Extender Manager displays temperature values of FortiExtender | 7.0.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager can use the FortiGate device's GPS coordinates to localize it on the map | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager centrally manages ZTNA policies using tags retrieved from EMS server via Fabric Connector | 7.0.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Central Management | Access permission for the IPS Admin using the Restricted Admin profile gives granular access to a selected list of ADOMs | 7.0.3 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287` | `config system admin profile; edit <PROFILE>; set type restricted; set ips-filter enable; end` and `config system admin user; edit <ADMIN>; set adom-access specify; set adom <ADOM>; end` |
| Central Management | New "Where Used" function available for IPS Admin to identify IPS Profile usage information with read-only drill-down capability to the firewall policy level | 7.0.3 and later | NDM `SRG-APP-000033-NDM-000212` | `config system admin profile; edit <PROFILE>; set ips-objects read; set ips-lock read; end` |
| Central Management | FortiManager centrally manage FortiProxy devices in the FortiProxy ADOM type | 7.0.3 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | `config system admin user; edit <ADMIN>; set adom <ADOM>; end` |
| Policy and Objects | Policy revision history | 7.0.0 and later | NDM `SRG-APP-000381-NDM-000305`; NDM `SRG-APP-000080-NDM-000220` | GUI: Policy & Objects (policy package revision history) |
| Policy and Objects | Assign multiple Global Policy Packages to the same ADOM, to different local Policy Packages | 7.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set global-policy-packages read; end` |
| Policy and Objects | FortiGate 6000 and 7000 support for hit count | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Policy ID can be set by users when a new policy is being created in the GUI | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Policy hit count added in GUI supports on-demand per-policy package refresh | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config system admin setting; set hitcount-monitor disable; end` |
| Policy and Objects | New IPS signatures monitoring page | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Object revision history | 7.0.0 and later | NDM `SRG-APP-000381-NDM-000305`; NDM `SRG-APP-000516-NDM-000340` | `config system global; set object-revision-status enable; end` |
| Policy and Objects | IPS Baseline profile can be used together with an existing IPS profile | 7.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set ips-objects read; set ips-lock read; end` |
| Policy and Objects | Change note is mandatory for every object and policy change | 7.0.2 and later | NDM `SRG-APP-000080-NDM-000220`; NDM `SRG-APP-000381-NDM-000305` | `config system global; set object-revision-mandatory-note enable; end` |
| Policy and Objects | Per-device mapping for LDAP and FSSO user groups | 7.0.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | IPS admins have increased visibility and can push pending IPS updates to managed FortiGates | 7.0.3 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | `config system admin profile; edit <PROFILE>; set ips-objects read; set ips-lock read; end` |
| Policy and Objects | IPS sensor designed with three layers: header, footer and regular sensors | 7.0.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set ips-objects read; set ips-lock read; end` |
| System | FortiManager verifies if FortiAnalyzer features are disabled before forming HA cluster | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Cluster HA improvements | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Theme mode | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Admin Permission to enable/disable script tab access | 7.0.0 and later | NDM `SRG-APP-000340-NDM-000288`; NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set script-access none; end` |
| System | Admins can use a SAML SSO FortiCloud account to log in to FortiManager | 7.0.0 and later | NDM `SRG-APP-000516-NDM-000336` | If unused: `config system saml; set forticloud-sso disable; end` |
| System | Suggest backup before upgrade | 7.0.2 and later | NDM `SRG-APP-000516-NDM-000340` | `execute backup all-settings sftp <IP:PORT> <FILE> <USER> <PASSWORD>` |
| System | Admin user attributes can be set in the admin profile and override the individual admin settings | 7.0.3 and later | NDM `SRG-APP-000038-NDM-000213`; NDM `SRG-APP-000408-NDM-000314` | `config system admin profile; edit <PROFILE>; set trusthost1 <IP> <MASK>; end` and `config system admin user; edit <ADMIN>; set th-from-profile <TRUSTHOST_INDEX>; end` |
| System | ADOM health check tool reports warnings on devices, configurations, and policy package status | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Managing mixed FortiOS versions 6.2 and 6.4 in a single ADOM | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Managing mixed FortiOS versions 6.4 and 7.0 in a single ADOM | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | ADOM upgrade from 6.4 to 7.0 | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiManager supports hyperscale policy in 6.2 and 6.4 ADOM versions | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Configurable TLS cipher suites and cipher priority order to support GUI access, FGFM tunnel, OFTP and FortiManager Web Services | 7.0.2 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330` | `config system global; config ssl-cipher-suites; edit 1; set cipher <CIPHER>; set version tls1.3; end; end` |
| Management Extensions | CPU and RAM maximum values for Management Extension Applications can be configured in CLI | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management Extensions | New management extension - FortiSOAR | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management Extensions | New management extension - FortiAIOps | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management Extensions | New management extension - Universal Connector | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management Extensions | New management extension - Policy Analyzer | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management Extensions | FortiSigConverter MEA supports ADOMs | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management Extensions | Check for new MEA versions using CLI | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | FortiManager Setup wizard | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | FortiManager VM licenses | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | GUI reorganization | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | FortiManager VM supports Amazon EC2 IMDS version 2 | 7.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | Country list for direct registration | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | Event log easier to read | 7.0.1 and later | NDM `SRG-APP-000095-NDM-000225` | GUI: System Settings (Event Log) |
| Other | Local FortiGuard Distribution Server enhancements | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config fmupdate service; set avips disable; end` |
| Other | NSX-T service template with VDOM support | 7.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | Add TLS-SSL support for local log SYSLOG forwarding | 7.0.1 and later | NDM `SRG-APP-000516-NDM-000350`; NDM `SRG-APP-000515-NDM-000325`; NDM `SRG-APP-000412-NDM-000331` | `config system syslog; edit <SYSLOG>; set ip <SYSLOG_IP>; set secure-connection enable; set ssl-protocol tlsv1.2; end` |
| Other | SNMP monitoring available to monitor the FortiManager built-in FDS/FGD servers | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | QoS monitoring support added for dialup VPN interfaces | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | FortiGuard service supports filtering by ADOM | 7.0.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | Deploying FortiManager-VM on IBM Cloud | 7.0.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Device Inventory adds new chart and columns | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Improved design for onboarding FortiGate HA clusters to prevent auto-link failure | 7.2.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-op none; end` |
| Device Manager | Global device dashboard | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Enhancement to aggregate interface allows creation without specifying the interface members | 7.2.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | FortiManager to add IoT devices based on FortiOS Asset Identity Center | 7.2.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-op none; end` |
| Device Manager | Model device initialization enhancements | 7.2.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-op none; end` |
| Device Manager | Internet service database version checked for model devices | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Perform packet capture on managed FortiGate interfaces and on managed FortiSwitches | 7.2.2 and later | NDM `SRG-APP-000408-NDM-000314` | `config system admin profile; edit <PROFILE>; set device-config read; end` |
| Device Manager | FortiManager supports FortiGate Cloud-Native Firewall as device type | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Interface-based traffic shaping can display real time dropped packets | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | FortiManager detects and displays the out-of-sync status of the FortiGate HA Cluster nodes | 7.2.2 and later | NDM `SRG-APP-000381-NDM-000305` | GUI: Device Manager (configuration status) |
| Device Manager | Improved FortiGate RMA process using zero touch provisioning | 7.2.2 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | `config system admin profile; edit <PROFILE>; set device-op none; end` |
| Device Manager | Device configuration status and Policy Package status messages display specific information about the out of sync cause and how to remediate | 7.2.3 and later | NDM `SRG-APP-000381-NDM-000305` | GUI: Device Manager (configuration and policy package status) |
| Device Manager | Security enhancement to control new VM device registration to FortiManager | 7.2.10+; 7.4.7+; 7.6.3+ | NDM `SRG-APP-000516-NDM-000335` | `config system global; set fgfm-allow-vm disable; set fgfm-deny-unknown enable; end` |
| Device Manager | SD-WAN overlay templates | 7.2.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | SD-WAN Monitor includes new filter to display unhealthy devices or interfaces only | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Pre-built route-maps used for SD-WAN self-healing with BGP routing | 7.2.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | SD-WAN Template added the health-check embedded SLA information | 7.2.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | FortiManager supports multiple interface members in the SD-WAN neighbor configurations | 7.2.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | SD-WAN template enhancement | 7.2.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | IPS template combines configuration for global "IPS Global" and per-vdom "System IPS " / "IPS Settings" | 7.2.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Device blueprints | 7.2.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | `config system admin profile; edit <PROFILE>; set device-op none; end` and `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | CLI templates have increased visibility for troubleshooting | 7.2.0 and later | NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Improved CLI templates with validation and preview functions | 7.2.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Fabric Authorization Template automatically provisions and authorizes LAN Edge devices on the managed FortiGates | 7.2.1 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000516-NDM-000335` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | AP Manager exposes wireless advanced features | 7.2.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-ap read; end` |
| Central Management | AP groups can be now formed with different AP models | 7.2.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-ap read; end` |
| Central Management | AP Manager improvements in naming and tooltips | 7.2.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Configuration enhancement improves multiple port selection in FortiSwitch Templates | 7.2.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | NAC policy added to policy package | 7.2.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Central Management | NAC policy enhanced with FortiLink settings, LAN segments, and NAC policy tags | 7.2.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Central Management | LAN-Edge: Keep VLAN info when cloning FortiSwitch template | 7.2.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | Extender Manager displays the ESN IMEI, phone number, IMSI, and ICCID as columns for all managed FortiExtenders | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | ADOM-level meta variables for general use in scripts, templates, and model devices | 7.2.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | One FortiAnalyzer can be shared across multiple FortiManager ADOMs | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | SAML SSO wildcard admin user to match all users on IdP server | 7.2.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000153-NDM-000249` | `config system admin user; edit <ADMIN>; set user_type sso; set wildcard disable; end` (prefer named accounts) |
| Central Management | Administrative access to FortiManager controlled by IPv4/IPv6 local-in policy | 7.2.0 and later | NDM `SRG-APP-000038-NDM-000213`; NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000435-NDM-000315` | `config system local-in-policy; edit 1; set intf <PORT>; set src <IP> <MASK>; set dport 443; set protocol tcp; set action accept; end` |
| Central Management | AI Analysis link exposed in Device Manager redirects to FortiAIOps MEA | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | IPS administrators have visibility on each IPS profile | 7.2.0 and later | NDM `SRG-APP-000033-NDM-000212` | `config system admin profile; edit <PROFILE>; set ips-objects read; set ips-lock read; end` |
| Central Management | IPS admin install preview for multiple FortiGate devices at once shows the CLI configuration to be installed on each target device | 7.2.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set ips-objects read; set ips-lock read; end` |
| Central Management | IPS diagnostics page for IPS dedicated admin displays CPU, memory, and performance statistics for FortiGates related to IPS processes | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | IoT query service support | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Initiate the RMA process to replace the FortiSwitch or FortiAP units from FortiManager | 7.2.1 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | `config system admin profile; edit <PROFILE>; set device-op none; end` |
| Central Management | FortiManager supports push updates via JSON API for dynamic address groups objects | 7.2.1 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000038-NDM-000213` | `config system admin user; edit <API_ADMIN>; set rpc-permit read-write; set trusthost1 <IP> <MASK>; end` |
| Central Management | FortiManager supports BYOL installation on managed FortiGate VM | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiGates with firmware FOS version 7.0 and version 7.2 can be managed under the same FortiManager 7.0 ADOM | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | ADOM version 7.2 supports policy package installation to the lower version of FortiGate on FortiOS 7.0. | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Improved FortiSwitch Manager and AP Manager dashboards | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Option to automatically unlock the ADOM after installing the Policy Package has been added to the Workspace Mode | 7.2.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system global; set workspace-unlock-after-install enable; end` |
| Central Management | FortiManager supports MFA with FortiToken Cloud | 7.2.2 and later | NDM `SRG-APP-000820-NDM-000170` | `config system admin user; edit <ADMIN>; set two-factor-auth ftc-ftm; end` |
| Central Management | Wildcard admin user is supported in the per-ADOM admin profile | 7.2.2 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000153-NDM-000249` | `config system admin user; edit <ADMIN>; set wildcard disable; end` (prefer named accounts) |
| Central Management | FortiManager supports now the FAZ-BD VM and appliance as managed devices | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | IoT Vulnerabilities has been added to the Asset Identity Center | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Workspace mode is supported for the restricted admin | 7.2.2 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | `config system global; set workspace-mode normal; end` |
| Central Management | Restricted IPS admins can manage the IPS header and footer and perform IPS installations in the global ADOM | 7.2.2 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set ips-objects read; set ips-lock read; end` |
| Central Management | FortiManager displays PSIRT information when a vulnerability is detected for managed devices | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager supports authentication token for API administrators | 7.2.2 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000038-NDM-000213` | `execute api-user generate-key <API_ADMIN>` and `config system admin user; edit <API_ADMIN>; set trusthost1 <IP> <MASK>; end` |
| Central Management | FortiProxy 7.2 ADOM type added support for VDOMs | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Configurable SD-WAN monitor data with custom disk usage | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager added support for IOTV objects and vulnerability download from FDS | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | VPN Monitoring displays IPsec VPN tunnels created by IPSec templates and SD-WAN overlay wizard | 7.2.3+; 7.4.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager supports FortiPAM license validation and central packages download | 7.2.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Proxy settings server URL page enhanced with drag-and-drop and better user experience | 7.2.5+; 7.4.2+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Enforce Device Configuration option allows autolink to push changes on FortiGate management interface during ZTP | 7.2.5+; 7.4.2+ | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-op none; end` |
| Policy and Objects | Policy Packages can use colors for sections | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Firewall policy creator exposed | 7.2.1 and later | NDM `SRG-APP-000381-NDM-000305`; NDM `SRG-APP-000100-NDM-000230` | GUI: Policy & Objects (policy creator column) |
| Policy and Objects | Unused Policies filter in a predefined time frame to help security teams for audit purposes | 7.2.0 and later | NDM `SRG-APP-000381-NDM-000305` | GUI: Policy & Objects (Find Unused Policies) |
| Policy and Objects | The Insert Empty Policy operation will insert a new disabled policy above or below, with no interface pair inheritance from the adjacent policies | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Increased number of multicast policies to 2560 per policy package | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Firewall policy strict search option will return only the results with an exact match | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Inserting a new policy in the Policy Package page will keep the screen focus and position on the newly added policy | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Policy Blocks are supported in the Global ADOM and can be reused in different Global Policy Packages | 7.2.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set global-policy-packages read; end` |
| Policy and Objects | Create new firewall policy page consolidates source and destination object types | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Create a Policy Block from a selection of the policies within Policy Package | 7.2.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Create a new policy based on the logged traffic and traffic hit count | 7.2.4+; 7.4.1+ | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Resolve IP address from FQDN for firewall address type subnet | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | FortiManager supports empty Address Group | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Metadata Variables are supported in Firewall Objects configuration | 7.2.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Additional filters available for IPS sensors | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Monitoring page for the IPS on-hold signatures | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Enhanced object "where used" function | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Factory default firewall addresses and address group for private IP space (RFC1918) | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Virtual IP (VIP) objects defined as an IP range are now searchable by an IP in the range | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | FortiManager added support for FortiGate shared global objects | 7.2.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Object search is done using a persistent search menu, and the search extends to all object types | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Fabric View | Allow multiple Cisco PxGrid connectors in the same ADOM | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Fabric View | FortiManager updated integration with NSX-T | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Fabric View | Flex-VM Fabric Connector to support flex licensing management from FortiManager | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiManager-HA automatic failover enhancement | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiManager-HA support automatic VRRP failover in Azure | 7.2.5+; 7.4.2+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | New firewall admin role with no RW permission on IPS objects | 7.2.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287` | `config system admin profile; edit <PROFILE>; set ips-objects read; end` |
| System | Per-ADOM admin profile | 7.2.1 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287` | `config system admin profile; edit <PROFILE>; set adom-admin enable; end` and `config system admin user; edit <ADMIN>; set adom-access specify; set adom <ADOM>; end` |
| System | FortiManager French GUI support | 7.2.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiManager supports link aggregation of physical ports | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiManager supports VLANs on physical network interfaces | 7.2.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Add LLDP support on FMG and FAZ | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config system interface; edit <PORT>; set lldp-reception disable; set lldp-transmission disable; end` |
| System | FortiManager setup wizard improvement with optional firmware upgrade step | 7.2.1 and later | NDM `SRG-APP-000457-NDM-000352` | GUI: setup wizard (firmware upgrade step) |
| System | TPM hardware module | 7.2.2 and later | NDM `SRG-APP-000231-NDM-000271` | `config system global; set private-data-encryption enable; end` (the TPM option is not in the 8.0.1 CLI Reference) |
| System | Entitlement file can be uploaded during the setup wizard in air-gapped environments | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | SAML assertions and SAML requests can be now signed to better support third-party IdPs | 7.2.3 and later | NDM `SRG-APP-000516-NDM-000336`; NDM `SRG-APP-000156-NDM-000250` | `config system saml; set want-assertions-signed enable; set auth-request-signed enable; end` |
| System | Extended JSON API to support the FortiManager backup operation | 7.2.3 and later | NDM `SRG-APP-000516-NDM-000340` | See the Scheduled configuration backup row |
| Management Extensions | Universal Connector MEA added support for Cisco ACI | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | Automatic configuration synchronization for the members of the auto-scaling group in Public Cloud in case of scale-out/scale-in events | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | Visibility improvement for auto-scaling clusters | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | FortiManager-VM has been added to the Flex-VM offering | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | VM flexible shapes support for Oracle Cloud Infrastructure | 7.2.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | NSX-T connector options can be managed from FortiManager | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | NSX-T connector support for retrieval of North-South service objects | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | FortiManager-VM added support for Oracle Dedicated Region Cloud | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | FortiManager added support for SCCC Alibaba Cloud | 7.2.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Auto-link setting is exposed to control configuration installation during ZTP | 7.4.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-op none; end` |
| Device Manager | LTE modem data usage and status has been added to device monitoring widgets | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Filter function is available for Device Manager table columns | 7.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Firmware Template can filter the FortiGate HA Clusters and trigger upgrade only on cluster with all nodes up | 7.4.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set fgd-center-fmw-mgmt read; set device-fwm-profile read; end` |
| Device Manager | Granular control over what values to keep when a conflict occurs during import | 7.4.4 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Device Manager | FortiManager supports FortiGate HA Cluster with virtual SN | 7.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Automatically set central-management settings for FortiAnalyzer HA cluster members when added to FortiManager | 7.4.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Automated SD-WAN post overlay process creates policies to allow the health-checks traffic to flow between Branch and HUB | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Automated SD-WAN overlay process adds "branch_id" meta variable auto assignment | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | SD-WAN monitoring map integrates with Cloud Assisted Monitoring Service to allow FortiGate interface speed tests from inside FortiManager | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | SDWAN monitoring map enhancements | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | SDWAN template for heterogeneous WAN link types | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | SD-WAN usability improvement allow drag-and-drop of SD-WAN rules and cut/copy and paste before and after operation | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | SD-WAN Monitoring dashboards allows full widgets customization | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Link, SLA, Application, and Rules status monitoring widgets added to SD-WAN Monitor | 7.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Layer-2 physical interface TX, RX, CRC errors, speed, and duplex mode added to SD-WAN monitoring | 7.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Quick access to per-device SD-WAN monitoring added to SD-WAN Monitor Template View | 7.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Preview CLI configuration for the device provisioning templates | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Fortinet factory-default wireless and extender templates | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Jinja Templates have direct access to the device DB to support generation of dynamic configuration | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Fabric Authorization Template is integrated with Device Blueprint and supports meta variables | 7.4.1 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000516-NDM-000335` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Support model FortiGate HA cluster in device blueprint | 7.4.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Factory default SSIDs and AP Profiles configuration updated | 7.4.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-ap read; end` |
| Device Manager | System Provisioning Template supports interface, server mode, and source IP configuration for NTP | 7.4.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | System Templates support metadata variables to configure hostname, time zone, and geographic coordinates | 7.4.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | FortiManager provides a warning for SSLVPN feature removal when upgrading an affected desktop FortiGate model to 7.6 | 7.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Multiple optimizations to the factory default SSID and AP-profiles | 7.4.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-ap read; end` |
| Central Management | Export Managed FortiAPs and import FortiAPs from a CSV file | 7.4.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-ap read; end` |
| Central Management | Per-device VRRP mapping can be used under FortiSwitch Profiles | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | FortiManager allows switchport export to another VDOM, and configuration of the exported port in the destination VDOM | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | FortiSwitch replacement procedure can be executed from FortiManager GUI | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | Custom commands can be assigned/unassigned at once to multiple managed FortiSwitches | 7.4.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | FortiManager creates packet capture for managed FortiSwitches | 7.4.1 and later | NDM `SRG-APP-000408-NDM-000314` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | FortiSwitch packet capture can run an schedule | 7.4.2 and later | NDM `SRG-APP-000408-NDM-000314` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | FortiSwitch devices can be imported from a CSV file | 7.4.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | Central firmware upgrade for FortiExtender MODEM | 7.4.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiextender read; end` |
| Central Management | FortiManager supports install preview for model devices | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set deploy-management none; end` |
| Central Management | FortiManager supports CLI diff in the workflow approval sessions | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000381-NDM-000305` | `config system global; set workspace-mode workflow; end` |
| Central Management | Internet Service database update occurs only if specific policy objects require a FortiGuard update | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager supports uploading and hosting of an external threat feed | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Fabric connector support for FortiManager to connect to a remote FortiAnalyzer | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Various GUI improvements for ZTNA, NAC Policies , SSL VPN to align to FOS | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager support for managing account level entitlements for FortiSandbox Cloud | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Auto-link will only trigger an IPS/Application Control update if the signatures used in the Policy Package require a newer version | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Remote access to FortiOS GUI from FortiManager | 7.4.2 and later | NDM `SRG-APP-000408-NDM-000314`; NDM `SRG-APP-000038-NDM-000213` | If unused: `config system admin setting; set fgt-gui-proxy disable; end`; otherwise `config system admin profile; edit <PROFILE>; set fgt-gui-proxy disable; end` for profiles that do not need it |
| Central Management | FortiManager manages the licenses for air-gapped FortiWeb via the FortIFlex connector | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager manages the licenses for air-gapped FortiGate via the FortiFlex connector | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | ADOM version 7.4 supports FortiOS versions 7.4, 7.2, and 7.0 | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Upstream FortiManager provides delta only updates to downstream FortiManagers in cascade mode | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Firmware upgrade report | 7.4.2 and later | NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set fgd-center-fmw-mgmt read; set device-fwm-profile read; end` |
| Central Management | Meta variables are available in the SSID, FortiSwitch VLANs and FortiSwitch Templates configuration | 7.4.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | Meta variable support in EMS connector allows for installing different connector names and IP addresses on each FortiGate | 7.4.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set fabric-viewer read; end` |
| Central Management | FortiManager can centrally update the SIEM and SOAR content package for FortiAnalyzer | 7.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager detects FortiGate HA clusters operating in MVC mode, provides a warning, and prevents cluster firmware upgrade | 7.4.4+; 7.6.0+ | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set fgd-center-fmw-mgmt read; set device-fwm-profile read; end` |
| Central Management | The VPN Monitor table view can be filtered using the greater than (>) or less than (<) signs on incoming/outgoing bandwidth columns | 7.4.4+; 7.6.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Per-admin feature visibility mode allows each administrator to customize GUI based on their own preference | 7.4.7+; 7.6.2+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `config system global; set gui-feature-visibility-mode per-adom; end` to keep feature visibility under central control |
| Central Management | PxGrid Connector supports Cisco ISE distributed environment | 7.4.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | ADOM upgrade readiness tool | 7.4.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager integration with FortiSASE controller | 7.4.8 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Central policy management and synchronization for FortiSASE | 7.4.8 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Central Management | FortiGuard downloads restricted to FortiManagers with premium or elite support subscriptions | 7.4.9 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Install preview support for partial install | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set deploy-management none; end` |
| Policy and Objects | Policy Package installation added link to the progress report page for installation errors | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Support for IoT Virtual Patching in NAC policies using pre-built severity filters | 7.4.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Policy deletion warning message improved with selected policy number and name reference | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Enable option for persistent policy hit-count on ADOM database | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Partial install pushes only the instructed configuration (JSON API) | 7.4.1 and later | NDM `SRG-APP-000380-NDM-000304` | If unused: `config system global; set partial-install disable; end` |
| Policy and Objects | Policy partial install supports policy reorder/move operation ( JSON API) | 7.4.1 and later | NDM `SRG-APP-000380-NDM-000304` | If unused: `config system global; set partial-install disable; end` |
| Policy and Objects | Policy revision supports the revert policy function | 7.4.2 and later | NDM `SRG-APP-000516-NDM-000340`; NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Policy Block usability improvements | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Support added for "Install On" function for policy blocks | 7.4.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Policy Package consistency check result can be exported as PDF file | 7.4.3 and later | NDM `SRG-APP-000381-NDM-000305` | GUI: Policy & Objects (consistency check) |
| Policy and Objects | Every policy change generates a revision and administrator is prompted to add a change note | 7.4.3 and later | NDM `SRG-APP-000080-NDM-000220`; NDM `SRG-APP-000381-NDM-000305` | `config system global; set object-revision-status enable; set object-revision-mandatory-note enable; end` |
| Policy and Objects | Policy to Log and Log to Policy adds a persistent right-click action on all table columns. | 7.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Import and export meta variables in CSV format | 7.4.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Policy and Objects | Import from an SDN connector IPv6 firewall address type | 7.4.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Cisco ACI connector supports IPv6 firewall address import | 7.4.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Metavariable support added under address group members and dynamic interface configurations | 7.4.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Maximum value for the proxy address table has been increased to 400K | 7.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Fabric View | Updated CSF topology view on FortiManager | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiManager supports different VM type platforms to form the FortiManager cluster | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | A new restricted admin profile can be used to only change the administrators passwords | 7.4.2 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287` | `config system admin profile; edit Password_Change_User; set write-passwd-access specify-by-user; set write-passwd-user-list <USERS>; end` |
| System | Granular admin permission grants IPS Admin access to only IPS objects and prevents changes for regular Firewall Admin on IPS Profiles | 7.4.2 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287` | `config system admin profile; edit <PROFILE>; set ips-objects read; end` |
| System | ADOM 7.2 Policy Package supports installation on FortiGate 7.4 | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | 7.2 ADOM managing mixed FOS versions | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiManager can upgrade multiple ADOMs (same version) at the same time | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiManager supports setting a time zone for each ADOM | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Prevent FortiManagers with an expired support contract from upgrading to a major or minor firmware release | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Automatic system backup setup in GUI to configure a backup schedule and visualize backup history | 7.4.1 and later | NDM `SRG-APP-000516-NDM-000340` | `config system backup all-settings; set status enable; set protocol sftp; set server <IP>; set crptpasswd <ENCRYPTION_PASSWORD>; end` |
| System | FortiManager and FortiAnalyzer support HTTP/2 for improved security, multiplexing, and reduced network latency | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Backup strategy and configuration setup added to the FortiManager setup wizard | 7.4.2 and later | NDM `SRG-APP-000516-NDM-000340` | `config system backup all-settings; set status enable; set protocol sftp; set server <IP>; set crptpasswd <ENCRYPTION_PASSWORD>; end` |
| System | FortiManager system backup and restore operations adds mandatory password, and the backup file is encrypted with AES256 | 7.4.2 and later | NDM `SRG-APP-000516-NDM-000340`; NDM `SRG-APP-000231-NDM-000271` | `config system backup all-settings; set status enable; set protocol sftp; set server <IP>; set crptpasswd <ENCRYPTION_PASSWORD>; end` |
| System | Migrate the FortiManager instance from a different platform supported in the GUI | 7.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Full page configuration available for select menus | 7.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiCare integration into FortiManager for links to documentation, video tutorials, release notes, and more | 7.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiManager supports IPv6 address type for syslog server configuration | 7.4.3 and later | NDM `SRG-APP-000516-NDM-000350` | `config system syslog; edit <SYSLOG>; set ip <SYSLOG_IPV6>; end` |
| System | FortiManager introduces OS firmware levels Feature(F) and Mature(M) | 7.4.4+; 7.6.0+ | NDM `SRG-APP-001035-NDM-000340`; NDM `SRG-APP-000457-NDM-000352` | GUI: Firmware Management (choose a Mature (M) release where possible) |
| Management Extensions | Cisco ACI Connector (Universal Connector) supports Endpoint Security Groups (ESGs) | 7.4.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management Extensions | Azure Connector (Universal Connector) directly communicate with AZURE to resolve and update dynamic firewall objects on managed FortiGates | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Management Extensions | Support Universal Connector for FortiManager HA | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | FortiManager used as single-pane management tool to orchestrate FortiGate deployment in AWS | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | FortiManager supports backups using Azure's enhanced backup policy | 7.4.2 and later | NDM `SRG-APP-000516-NDM-000340` | — |
| Cloud Services | AWS FortiManager-VM HA and EIP | 7.4.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | FortiManager supports M6 and M7 instance types in AWS | 7.4.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | FortiManager can act as proxy relay for individual FortiGate connections to GCP | 7.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | FortiManager can act as proxy relay for individual FortiGate connections to Azure | 7.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Cloud Services | FortiManager supports Azure virtual WAN inbound Software Load Balancer configuration and FortiGate PAYG license information | 7.4.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | New FortiManager UX design | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | Fabric and External connector pages have been reorganized for an enhanced user experience | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | FortiManager connector relay to AWS will proxy all individual FortiGate requests | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | FortiManager key areas have been reorganized to enhance user experience | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | FortiManager imports EPGs entries using the Cisco ACI connector as individual objects | 7.4.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | WAN Optimization Monitor, Cache Monitor, and Peer Monitor widgets are added to the device dashboard | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Add FortiView sessions widget under per-device dashboard | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | SD-WAN Manager section for SD-WAN related configurations | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Static Route Template is integrated with SD-WAN Overlay Template | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Support for multi-HUB (up to 4 HUBs) integrated into the SD-WAN Overlay Template | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | VDOM configuration for HUBs has been included into the SD-WAN Overlay Template | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Traffic segmentation over a single overlay is supported in the SD-WAN Overlay Template | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Certificate/Certificate Template integrated to the SD-WAN Overlay Template | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000516-NDM-000344` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | SD-WAN Overlay Template supports multiple branch device groups | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | SD-WAN Overlay Template can deploy BGP on loopback interfaces | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | SD-WAN Overlay Template supports ADVPN 2.0 and dynamic BGP | 7.6.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | SD-WAN Overlay Template best practices updated | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | SD-WAN Monitor combines multiple filters in the same view | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | CLI script and template supports syntax error detection with suggested corrections and autocomplete | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set script-access read; set script-run none; end` |
| Device Manager | The "Modified" status of the Template Group provides details about changes to individual templates or group membership | 7.6.2 and later | NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Revision control for provisioning templates | 7.6.3 and later | NDM `SRG-APP-000381-NDM-000305`; NDM `SRG-APP-000516-NDM-000340` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | Revision control for scripts and script groups with View Diff function in the CLI format | 7.6.5 and later | NDM `SRG-APP-000381-NDM-000305`; NDM `SRG-APP-000516-NDM-000340` | `config system admin profile; edit <PROFILE>; set script-access read; set script-run none; end` |
| Device Manager | Metadata variable usability improvements for editing, validating, and previewing on devices | 7.6.5 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Device Manager | FortiManager includes an option to allow FortiGate to download firmware directly from FortiGuard during ZTP | 7.6.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set fgd-center-fmw-mgmt read; set device-fwm-profile read; end` |
| Central Management | FortiSwitch Template allows for configuration of port speed and duplex mode | 7.6.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | Configuration changes for Policy & Objects and the device level can be previewed as API or CLI | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set deploy-management none; end` |
| Central Management | IPAM support to configure DHCP on device interface, FortiSwitch VLANs, and SSID under WiFi profiles | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | FortiManager as package update server for FortiNDR | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config fmupdate service; set avips disable; end` |
| Central Management | CLI option enables JSON API event log for both request and response | 7.6.0 and later | NDM `SRG-APP-000095-NDM-000225`; NDM `SRG-APP-000343-NDM-000289`; NDM `SRG-APP-000381-NDM-000305` | `config system global; set jsonapi-log all; end` |
| Central Management | Fabric of FortiManager | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config system interface; edit <PORT>; set allowaccess https ssh; end` (do not allow `fabric`) |
| Central Management | Configuration changes performed on AP Manager, FortiSwitch Manager, and Extender Manager can be previewed in JSON API and CLI format | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set deploy-management none; end` |
| Central Management | FortiOS Firmware Upgrade status shows the image upload progress and upgrade tasks are visible under Device Manager | 7.6.2 and later | NDM `SRG-APP-000381-NDM-000305` | GUI: Device Manager (firmware upgrade tasks) |
| Central Management | FortiGate table size objects threshold is configurable and FortiManager provides warning when this limit is reached during device installation | 7.6.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin setting; set object-threshold-limit enable; set object-threshold-limit-value <PERCENT>; end` |
| Central Management | FortiManager on-premises supports multiple EMS Cloud instances | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Support for external resource threat feed as URL | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | SD-WAN templates add metadata variable support for preferred-source and transport-group | 7.6.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | GUI has increased performance when displaying PSIRT device vulnerabilities notification for large number of devices (over 10k) | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Metadata Variables can be mapped to a device group for devices that share the same configuration | 7.6.3 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | PxGrid connector update to support postured states | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager scripts support the Jinja script type | 7.6.4 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000340-NDM-000288` | `config system admin profile; edit <PROFILE>; set script-access read; set script-run none; end` |
| Central Management | FortiManager GUI supports FortiProxy Kerberos and Domain Controller configurations | 7.6.4 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Central Management | Add a default local user password policy | 7.6.4 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` (the policy applies to FortiGate local users, not FortiManager administrators) |
| Central Management | Automatically onboard and register FortiGates in FortiManager | 7.6.4 and later | NDM `SRG-APP-000516-NDM-000335`; NDM `SRG-APP-000380-NDM-000304` | `config system global; set fgfm-deny-unknown enable; end` and `config system admin profile; edit <PROFILE>; set device-op none; end` |
| Central Management | IPsec template install-on feature allows tunnel changes to be installed on relevant devices | 7.6.5 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | Fabric of FortiManager has automatic failover of managed FortiGates to the reachable FortiManager member | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Managing FortiGate registration to FortiCare | 7.6.7+; 8.0.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager API can be used to get detailed info about IPS signatures and packages | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Certificate Template supports Enrollment over Secure Transport (EST) method | 7.6.7 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000516-NDM-000344` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | FortiManager FortiGuard package manual import and delta export | 7.6.7 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | Proxy Policies are supported under Policy Blocks | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Virtual Wire Pair Policies are supported under Policy Blocks | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Administrators have granular access permission on selected Policy Blocks | 7.6.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287` | `config system admin user; edit <ADMIN>; set policy-block <ADOM>:<POLICY_BLOCK>; end` |
| Policy and Objects | Find Unused Policy function adds Disable option | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Policy screenshot function allows you to copy a selection of policies within the Policy Package as an image | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Policy and Objects | In Workspace mode, administrators can lock Policy Blocks for create, edit, or delete operations | 7.6.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system global; set workspace-mode normal; end` |
| Policy and Objects | In multi-VDOM setup, the Virtual Wire Pair Policy supports metavariable mapping so the VWP Policies can be consolidated under single Policy Package | 7.6.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Threat feed object supports per-device mapping for the source IP address | 7.6.2 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Cross-ADOM object search | 7.6.4 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Fabric View | FortiAIOps connector | 7.6.7+; 8.0.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| FortiAI | FortiAI on FortiManager | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | FortiAI license enforces usage for 3 local administrators | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | FortiAI assistant masks private and sensitive data before sending it to the Cloud | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | SD-WAN overlay configuration using FortiAI | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | FortiAI enhanced VPN operations with new diagnostics cases and help adding a new device to an existing VPN setup | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | FortiAI uses Retrieval-Augmented Generation ( RAG) to enhance and add accuracy to general questions | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | Display FortiAI top-up token quantities in the GUI | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| FortiAI | Feedback function collects overall user satisfaction and suggestions on FortiManager AI | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Model FortiGate HA cluster provisions the same interface number for all cluster members | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiManager HA cluster can sync the FortiGuard package management configuration to the secondary node | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | ADOM Scoped Admin is a new admin profile to permit ADOM users to manage their own admin accounts within the ADOM | 7.6.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287`; NDM `SRG-APP-000026-NDM-000208` | `config system admin profile; edit <PROFILE>; set adom-admin enable; end` |
| System | Password history can be enforced for up to 20 passwords | 7.6.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | `config system password-policy; set password-history <NUMBER>; end` |
| System | Role-based access control for provisioning templates and scripts | 7.6.4 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287`; NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; set script-access read; end` |
| System | ADOM version 7.6 supports FOS versions 7.6, 7.4, 7.2 and 7.0 | 7.6.3 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | Support higher authentication and encryption for SNMP v3 | 7.6.0 and later | NDM `SRG-APP-000395-NDM-000310` | `config system snmp user; edit <USER>; set security-level auth-priv; set auth-proto sha256; set priv-proto aes256; end` |
| System | Support SNMP v3 custom trap port | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiManager detects concurrent backup sessions and returns error message | 7.6.2 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| System | FortiManager's local-in policy supports multiple entries when configuring ports, addresses, and interfaces | 7.6.4 and later | NDM `SRG-APP-000038-NDM-000213`; NDM `SRG-APP-000408-NDM-000314` | `config system local-in-policy; edit 1; set intf <PORT>; set src <IP> <MASK>; set dport 443; set protocol tcp; set action accept; end` |
| System | Legal third party disclosure panel | 7.6.5+; 8.0.0+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | API enhancement to support install preview in the response for multiple devices | 7.6.0 and later | NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set deploy-management none; end` |
| Other | Fabric of FortiManager - License for total number of managed devices is enforced only on FortiManager Supervisor | 7.6.5 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Other | FortiManager KVM images have been validated for Red Hat OpenShift (RHOS) | 7.6.7+; 8.0.1+ | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Centrally manage SD-WAN QoS speed tests from FortiManager | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Device Manager | Local certificates lifecycle management (set validity and renew) and expiry notification alerts | 8.0.0 and later | NDM `SRG-APP-000516-NDM-000344` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | FortiSwitch Template adds override option to modify specific port settings on selected devices | 8.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-fortiswitch read; end` |
| Central Management | Support for FGR-70G-5G-DUAL 5G modems in Extender Manager | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Workspace Mode supports onboarding new devices and creating new policy packages without ADOM lock | 8.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system global; set workspace-mode normal; end` |
| Central Management | Interface-based bandwidth graph uses average bandwidth logic | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiSwitch, FortiAP and FortiExtender templates can be assigned from Fabric Authorization Template | 8.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | Certificate templates can be selected in model device, model HA device, and device blueprint configurations | 8.0.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000516-NDM-000344` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | New workflow mode design to control individual admin sessions with selective approvals | 8.0.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000381-NDM-000305`; NDM `SRG-APP-000080-NDM-000220` | `config system global; set workspace-mode workflow; end` |
| Central Management | Factory default IPsec template to configure FortiClient VPN | 8.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | Central monitoring dashboard for Firewall Users with filters for authentication method and user group | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Maximum length of meta variables value increased to 32768 characters | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Admin profile adds granular control on device manager (Interface, Log & Report, Security Fabric) and Routing | 8.0.0 and later | NDM `SRG-APP-000033-NDM-000212`; NDM `SRG-APP-000329-NDM-000287` | `config system admin profile; edit <PROFILE>; set device-config read; set device-interface read; set device-log read; set device-fabric read; set device-route read; end` |
| Central Management | pxGrid connector is enhanced to display Device Type and Session State | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Enhanced asset details and identity monitoring | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager supports downgrade and roll-back for FortiGuard packages to allow setting a preferred package version for devices | 8.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set fgd_center read; end` |
| Central Management | FortiManager supports importing password-type objects from FortiGate devices with private data encryption | 8.0.0 and later | NDM `SRG-APP-000231-NDM-000271` | `config system global; set private-data-encryption enable; end` |
| Central Management | FortiManager API can be used to get detailed info about IPS | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Drill down on SD-WAN interface bandwidth usage | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | Local user per-device mapping | 8.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Central Management | FortiManager support FortiSASE multitenancy | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager includes a default mapping option for dynamic local certificates | 8.0.1 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000516-NDM-000344` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | FortiManager supports explicit web proxy object management under the FortiProxy ADOM | 8.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Central Management | Stage firmware upgrades for FortiAP, FortiSwitch and FortiExtender | 8.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set fgd-center-fmw-mgmt read; set device-fwm-profile read; end` |
| Central Management | Wildcard normalized interfaces support regex-based interface name matching | 8.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Central Management | Create JSON type metadata variables | 8.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-profile read; end` |
| Central Management | Configure automatic retrieval of policy hit count data | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Central Management | FortiManager supports "install on" feature for EMS Connector | 8.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Central Management | Safe ZTP factory reset to preserve networking settings and keeps the FortiManager connectivity | 8.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set device-op none; end` |
| Policy and Objects | Local In policies are supported in the Global ADOM and in policy blocks | 8.0.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000038-NDM-000213` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Recurring Policy Package installation can be scheduled | 8.0.0 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set deploy-management none; end` |
| Policy and Objects | Configuration imports from FortiGate supports policy blocks | 8.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Policy blocks can be exported to different ADOMs or FortiManager instances | 8.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Policy and Objects | Install Preview for Global Policy Package installation | 8.0.1 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000381-NDM-000305` | `config system admin profile; edit <PROFILE>; set deploy-management none; end` |
| Policy and Objects | Batch policy package install from the global and local ADOMs | 8.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set deploy-management none; end` |
| Policy and Objects | Per-admin mode: sync page shows administrator name and timestamp | 8.0.1 and later | NDM `SRG-APP-000381-NDM-000305`; NDM `SRG-APP-000100-NDM-000230` | GUI: Policy & Objects (per-admin sync page) |
| Policy and Objects | Administrators can create protected objects to prevent regular administrators from modifying or deleting them | 8.0.0 and later | NDM `SRG-APP-000380-NDM-000304`; NDM `SRG-APP-000033-NDM-000212` | `config system global; set gui-object-protect enable; end` and `config system admin profile; edit <PROFILE>; set protected-objects none; end` |
| Policy and Objects | Global objects can be renamed directly in the Global ADOM, with changes automatically propagating to all ADOMs | 8.0.1 and later | NDM `SRG-APP-000380-NDM-000304` | `config system admin profile; edit <PROFILE>; set policy-objects read; end` |
| Fabric View | New external connectors: GuardiCore, Microsoft Azure (Proxy Mode), and Application Centric Infrastructure (ACI Proxy Mode) | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| Fabric View | Central management for ACI features | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | — |
| FortiAI | FortiAI can diagnose, troubleshoot, and remediate slow access to cloud or on-premise servers and applications | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | The Model Context Protocol (MCP) framework used by FortiAI agentic assistants and features on FortiManager | 8.0.0 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | FortiAI enabled on FortiManager supports web proxy deployments | 8.0.1 and later | No direct requirement; if unused, disable (NDM `SRG-APP-000142-NDM-000245`) | If unused: `config system global; set ai-mode disable; end` |
| System | Backup ADOM shared objects synchronization | 8.0.1 and later | NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000038-NDM-000213` | `config system global; set bkup-mode-shared-objs disable; end` for multi-tenant backup ADOMs |
| System | Custom session labels in FortiManager event logs | 8.0.0 and later | NDM `SRG-APP-000100-NDM-000230`; NDM `SRG-APP-000080-NDM-000220` | `config system admin setting; set custom-session-label enable; set custom-session-label-mode unique-per-session; end` |
| System | SAML SSO supports SHA-256 and SHA-512 for both IdP and SP | 8.0.0 and later | NDM `SRG-APP-000179-NDM-000265` | `config system saml; set signature-algorithm rsa-sha256; set digest-method sha256; set idp-signature-algorithm rsa-sha256; set idp-digest-method sha256; end` |
| System | FortiManager supports NTPv4 with SHA-256 encryption | 8.0.0 and later | NDM `SRG-APP-000395-NDM-000347` | `config system ntp; config ntpserver; edit 1; set ntpv3 disable; set authentication enable; set key-type sha256; set key-fmt hex; set key-id <ID>; set key <KEY>; end; end` |
| System | Time-base retention is configurable for the task monitor and event log | 8.0.0 and later | NDM `SRG-APP-000357-NDM-000293` | `config system locallog disk setting; set log-max-days <DAYS>; end` |
| System | Option to disable USB ports on FortiManager hardware | 8.0.1 and later | NDM `SRG-APP-000231-NDM-000271`; NDM `SRG-APP-000142-NDM-000245` | `config system global; set usb-port disable; end` |
| System | FortiManager firmware upgrade enhancements | 8.0.1 and later | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340` | GUI: Firmware Management (scheduled upgrades and vulnerability alerts) |
| Other | Post quantum cryptography (PQC) support | 8.0.0 and later | NDM `SRG-APP-000412-NDM-000331` | — (on by default for TLS 1.3 sessions) |

### Requirement reference

The SRG requirements used in the map, with their severity in the current SRG
release:

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
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
| NDM | `SRG-APP-000080-NDM-000220` | CAT II | The network device must protect against an individual (or process acting on behalf of an individual) falsely denying having performed organization-defined actions to be covered by non-repudiation. |
| NDM | `SRG-APP-000091-NDM-000223` | CAT II | The network device must generate audit records when successful/unsuccessful attempts to access privileges occur. |
| NDM | `SRG-APP-000092-NDM-000224` | CAT II | The network device must initiate session auditing upon startup. |
| NDM | `SRG-APP-000095-NDM-000225` | CAT II | The network device must produce audit log records containing sufficient information to establish what type of event occurred. |
| NDM | `SRG-APP-000096-NDM-000226` | CAT II | The network device must produce audit records containing information to establish when (date and time) the events occurred. |
| NDM | `SRG-APP-000097-NDM-000227` | CAT II | The network device must produce audit records containing information to establish where the events occurred. |
| NDM | `SRG-APP-000098-NDM-000228` | CAT II | The network device must produce audit log records containing information to establish the source of events. |
| NDM | `SRG-APP-000099-NDM-000229` | CAT II | The network device must produce audit records that contain information to establish the outcome of the event. |
| NDM | `SRG-APP-000100-NDM-000230` | CAT II | The network device must generate audit records containing information that establishes the identity of any individual or process associated with the event. |
| NDM | `SRG-APP-000101-NDM-000231` | CAT II | The network device must generate audit records containing the full-text recording of privileged commands. |
| NDM | `SRG-APP-000116-NDM-000234` | CAT II | The network device must use internal system clocks to generate time stamps for audit records. |
| NDM | `SRG-APP-000119-NDM-000236` | CAT II | The network device must protect audit information from unauthorized modification. |
| NDM | `SRG-APP-000120-NDM-000237` | CAT II | The network device must protect audit information from unauthorized deletion. |
| NDM | `SRG-APP-000121-NDM-000238` | CAT II | The network device must protect audit tools from unauthorized access. |
| NDM | `SRG-APP-000131-NDM-000243` | CAT II | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| NDM | `SRG-APP-000133-NDM-000244` | CAT II | The network device must limit privileges to change the software resident within software libraries. |
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
| NDM | `SRG-APP-000172-NDM-000259` | CAT I | The network device must transmit only encrypted representations of passwords. |
| NDM | `SRG-APP-000175-NDM-000262` | CAT I | The network device must be configured to use DoD approved OCSP responders or CRLs to validate certificates used for PKI-based authentication. |
| NDM | `SRG-APP-000177-NDM-000263` | CAT I | The network device, for PKI-based authentication, must be configured to map validated certificates to unique user accounts. |
| NDM | `SRG-APP-000179-NDM-000265` | CAT I | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| NDM | `SRG-APP-000190-NDM-000267` | CAT I | The network device must terminate all network connections associated with a device management session at the end of the session, or the session must be terminated after five minutes of inactivity except to fulfill documented and validated mission requirements. |
| NDM | `SRG-APP-000231-NDM-000271` | CAT I | The network device must only allow authorized administrators to view or change the device configuration, system files, and other files stored either in the device or on removable media (such as a flash drive). |
| NDM | `SRG-APP-000329-NDM-000287` | CAT II | If the network device uses role-based access control, the network device must enforce organization-defined role-based access control policies over defined subjects and objects. |
| NDM | `SRG-APP-000340-NDM-000288` | CAT I | The network device must prevent non-privileged users from executing privileged functions to include disabling, circumventing, or altering implemented security safeguards/countermeasures. |
| NDM | `SRG-APP-000343-NDM-000289` | CAT II | The network device must audit the execution of privileged functions. |
| NDM | `SRG-APP-000357-NDM-000293` | CAT II | The network device must allocate audit record storage capacity in accordance with organization-defined audit record storage requirements. |
| NDM | `SRG-APP-000360-NDM-000295` | CAT II | The network device must generate an immediate real-time alert of all audit failure events requiring real-time alerts. |
| NDM | `SRG-APP-000374-NDM-000299` | CAT II | The network device must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). |
| NDM | `SRG-APP-000378-NDM-000302` | CAT II | The network device must prohibit installation of software without explicit privileged status. |
| NDM | `SRG-APP-000380-NDM-000304` | CAT II | The network device must enforce access restrictions associated with changes to device configuration. |
| NDM | `SRG-APP-000381-NDM-000305` | CAT II | The network device must audit the enforcement actions used to restrict access associated with changes to the device. |
| NDM | `SRG-APP-000395-NDM-000310` | CAT II | The network device must be configured to authenticate SNMP messages using a FIPS-validated Keyed-Hash Message Authentication Code (HMAC). |
| NDM | `SRG-APP-000395-NDM-000347` | CAT II | The network device must authenticate Network Time Protocol sources using authentication that is cryptographically based. |
| NDM | `SRG-APP-000408-NDM-000314` | CAT II | Network devices performing maintenance functions must restrict use of these functions to authorized personnel only. |
| NDM | `SRG-APP-000411-NDM-000330` | CAT I | The network devices must use FIPS-validated Keyed-Hash Message Authentication Code (HMAC) to protect the integrity of nonlocal maintenance and diagnostic communications. |
| NDM | `SRG-APP-000412-NDM-000331` | CAT I | The network device must be configured to implement cryptographic mechanisms using a FIPS 140-2 approved algorithm to protect the confidentiality of remote maintenance sessions |
| NDM | `SRG-APP-000435-NDM-000315` | CAT II | The network device must be configured to protect against known types of denial-of-service (DoS) attacks by employing organization-defined security safeguards. |
| NDM | `SRG-APP-000457-NDM-000352` | CAT II | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| NDM | `SRG-APP-000495-NDM-000318` | CAT II | The network device must generate audit records when successful/unsuccessful attempts to modify administrator privileges occur. |
| NDM | `SRG-APP-000503-NDM-000320` | CAT II | The network device must generate audit records when successful/unsuccessful logon attempts occur. |
| NDM | `SRG-APP-000504-NDM-000321` | CAT II | The network device must generate audit records for privileged activities or other system-level access. |
| NDM | `SRG-APP-000505-NDM-000322` | CAT II | The network device must generate audit records showing starting and ending time for administrator access to the system. |
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000335` | CAT II | The network device must enforce access restrictions associated with changes to the system components. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000341` | CAT II | The network device must support organizational requirements to conduct backups of information system documentation, including security-related documentation, when changes occur or weekly, whichever is sooner. |
| NDM | `SRG-APP-000516-NDM-000344` | CAT II | The network device must obtain its public key certificates from an appropriate certificate policy through an approved service provider. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000795-NDM-000130` | CAT II | The network device must be configured to alert organization-defined personnel or roles upon detection of unauthorized access, modification, or deletion of audit information. |
| NDM | `SRG-APP-000820-NDM-000170` | CAT II | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. |
| NDM | `SRG-APP-000845-NDM-000220` | CAT II | The network device must be configured to verify, when users create or update passwords, the passwords are not found on the list of commonly used, expected, or compromised passwords in IA-5 (1) (a) for password-based authentication. |
| NDM | `SRG-APP-000875-NDM-000280` | CAT II | The network device must be configured to implement certificate revocation checking to support path discovery and validation for public key-based authentication. |
| NDM | `SRG-APP-000880-NDM-000290` | CAT II | The network device must be configured to protect nonlocal maintenance sessions by separating the maintenance session from other network sessions with the system by logically separated communications paths. |
| NDM | `SRG-APP-000910-NDM-000300` | CAT II | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-000925-NDM-000330` | CAT II | The network device must be configured to compare the internal system clocks on an organization-defined frequency with organization-defined authoritative time source. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |

### Collecting evidence

Collect `show full-configuration` and `get system status` from the
FortiManager, and export the items the map points to in the GUI: the
administrator and profile lists, the ADOM list and workspace or workflow
setting, the approval matrix, the event log settings and a sample of the event
log, and the backup schedule. For change control, add a sample of policy
package and device revisions with their change notes. Attach them to the
SRG-based checklist (Chapter 03).

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiManager.** Check the version
  column against your release, then check the license and model: FortiAI, the
  TPM, and the FortiAnalyzer features depend on them.
- **Administrators lose access after the profiles are tightened.** A
  permission set to `none` removes access to that function. Grant `read` to
  those who need to see the configuration and `read-write` only to those who
  change it.
- **Devices cannot connect after FGFM is hardened.** With `fgfm-deny-unknown`
  enabled, devices with unknown serial numbers cannot register on their own;
  add them first (or use a model device), then let them connect.
- **A requirement has no matching feature.** Some NDM requirements are met by
  procedure (for example, the account of last resort or CRL updates) or by
  another system (such as the authentication server or the central log
  server). Record how the requirement is met, not just which feature covers it.

## Security and Best Practices

- Keep FortiManager on a vendor-supported release and track the version
  column when planning upgrades.
- Limit every administrator to the ADOMs and permissions they need, and keep
  installation, scripts, and firmware upgrades in separate profiles.
- Require approval and change notes for configuration changes, and keep the
  revision history long enough to reconstruct any change.
- Use remote or PKI authentication for administrators, with FIPS-capable
  cryptography for HTTPS, SSH, FGFM, syslog, NTP, and SNMP.
- Back up the FortiManager configuration with encryption, off the
  FortiManager, after every change window.
- Review this map each time Fortinet publishes a new FortiManager release
  train or DISA updates the NDM SRG.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiManager New Features Guide*, release trains 7.0, 7.2, 7.4,
  7.6, and 8.0 (docs.fortinet.com, FortiManager documentation).
- Fortinet, *FortiManager 8.0.1 CLI Reference* (docs.fortinet.com).
- DISA Network Device Management SRG V5R5, from the October 2026 STIG Library
  Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map), and
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer map, built the same way).

**Knowledge checks:**

1. Why is a FortiManager assessed against the NDM SRG, and why do its access
   control and change-control requirements matter more than on a single
   device?
2. Where does the version data come from, given that FortiManager has no
   feature matrix?
3. Which administrator profile permissions limit who can change and install
   configuration on managed devices?
4. Which features record, approve, and back up configuration changes?
5. Which NDM requirements does FortiManager not meet exactly, and how do you
   handle them?
6. What applies to a feature marked "No direct requirement"?

## Summary and Completion Checklist

FortiManager has no STIG, so it is assessed against the NDM SRG, with the
weight on access control, auditing, and configuration-change control because
it configures every managed device. This chapter maps 487 features to
the release that introduced them, to the NDM requirement each feature
implements or must be configured to meet, and to the command or GUI location
that configures it: 52 core platform features, and all 435
features from the New Features Guides for FortiManager 7.0 through 8.0.
Operational features with no direct requirement fall under the requirement to
prohibit unnecessary functions when unused.

- [ ] Can find the release that introduced a FortiManager feature.
- [ ] Can map a FortiManager feature to its NDM requirement.
- [ ] Can find the command or GUI location that meets the requirement.
- [ ] Can design administrator profiles that separate template, policy,
  installation, script, and firmware duties.
- [ ] Can scope an SRG-based FortiManager assessment from the map, including
  the requirements met by procedure.
