# Chapter 12: FortiAnalyzer Feature, Version, and SRG Map

## Learning Objectives

- Find the FortiAnalyzer release that introduced a given feature.
- Map each FortiAnalyzer feature to the DISA SRG requirement it helps satisfy.
- Find the CLI command, or the GUI location, that configures each feature to
  meet its SRG requirement.
- Use the map to scope an SRG-based assessment of a FortiAnalyzer, which has no
  STIG of its own.
- Tell the difference between a feature that *implements* a Central Log Server
  requirement and one that only needs to be disabled when unused.

## Theory and Architecture

FortiAnalyzer has **no DISA STIG** (Chapter 10). It is the central log server
that the FortiGate STIGs depend on, so it is assessed directly against the
**Central Log Server SRG**, with the **Network Device Management (NDM) SRG** for
the few management-plane requirements the Central Log Server SRG does not
cover. Chapter 03 describes SRG-based assessment. This chapter gives three
pieces of information for every FortiAnalyzer feature: **which release
introduced it**, **which SRG requirement it relates to**, and **which command
configures it to meet that requirement**.

### Where the version data comes from

Fortinet does not publish a feature matrix for FortiAnalyzer. Instead, each
release train has a **New Features Guide** that lists every feature added in
that train and tags it with the patch release that introduced it. The version
column was built from all five guides Fortinet publishes for FortiAnalyzer 7.0,
7.2, 7.4, 7.6, and 8.0, covering FortiAnalyzer 7.0.0 through 8.0.1.

The table has two groups of rows:

- **Core platform features** (categories starting with *Core:*) are the
  long-standing capabilities that most Central Log Server requirements depend
  on: log collection, storage, forwarding, analysis, administration, and
  security. They existed before 7.0.0 and are not in any New Features Guide.
- **New features** are every topic in the five New Features Guides, under the
  guide's own category names.

| Version entry | Meaning |
| --- | --- |
| `7.0.0 or earlier` | A core platform feature, present in 7.0.0 and earlier releases |
| `7.4.1 and later` | Introduced in 7.4.1; later release trains include it |
| `7.6.7+; 8.0.0+` | Introduced in two release trains at different patch levels (often backported); the first release in each train is shown |

Two cautions apply. First, a feature introduced in a patch release of an older
train (for example 7.0.3) may reach a newer train only in that train's later
patches, so "and later" means later in the same train and, usually, in later
trains. Check the release notes for your exact release. Second, some features
apply only to certain models or licenses (for example FortiAI, the OT Security
Service, and SOC subscription features).

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG | Release | Applies to |
| --- | --- | --- |
| **Central Log Server (CLS)** | V3R5 | Log aggregation, storage, protection, analysis, alerting, and reporting, plus the log server's own accounts, authentication, and cryptography |
| **Network Device Management (NDM)** | V5R5 | Management-plane items the CLS SRG does not cover: SNMP, NTP authentication, authentication servers, configuration backup, and off-loading the FortiAnalyzer's own logs |

Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how FortiAnalyzer meets a
  requirement. Event handlers implement the CLS requirement to alert on
  attacks seen across multiple devices, for example.
- **Must be configured to meet a requirement.** The feature is in scope of a
  requirement and has to be set up correctly. Log forwarding must use
  reliable, encrypted transport, for example.
- **No direct requirement.** The feature is operational or cosmetic, such as
  an SD-WAN chart or a GUI theme. It has no requirement of its own, but if it
  is not needed it falls under the CLS requirement to disable non-essential
  capabilities (`SRG-APP-000141-AU-000090`).

The mapping is a starting point for an assessment, not a ruling. Confirm it
with your assessor, especially where a requirement is organization-defined.

### Where the commands come from

Every `config` path, `set` option, and option value in the command column was
checked against the **FortiAnalyzer 8.0.0 CLI Reference**. Read the column
this way:

- Statements are separated by `;` to fit in a table cell; on the CLI, enter
  each one on its own line. Values in `<ANGLE_BRACKETS>` are placeholders for
  your own names, addresses, and keys.
- Much of FortiAnalyzer is configured in the **GUI**: reports, event handlers,
  incidents, playbooks, and connectors. For those features, the column names
  the GUI pane (for example *GUI: Reports* or *GUI: Incidents & Events*)
  instead of a CLI command.
- For **"No direct requirement"** rows, a command is shown only when the
  feature can be turned off (for example `set ai-mode disable` for FortiAI or
  `set disable-module ot-view` for the OT views). A dash (**—**) means there is
  nothing to configure: the feature is a report layout, a chart, a license
  change, or a platform capability.
- Some rows point to another row (for example, log receipt time stamps rely on
  the *NTP server* row).

Some requirements cannot be met exactly with FortiAnalyzer settings alone.
Record them on the checklist as open findings with mitigations, or meet them
by procedure:

- **Password change.** The password policy can require that at least 4
  characters change (`change-4-characters`); the CLS SRG requires 8
  (`SRG-APP-000170-AU-002530`). Use remote authentication (RADIUS, TACACS+,
  LDAP, or PKI) so the authentication server enforces the policy.
- **Log file integrity hash.** `log-checksum` records MD5 hashes (`md5` or
  `md5-auth`), which are not a FIPS-approved hash. Enable it for tamper
  detection, run FortiAnalyzer in FIPS-CC mode, and protect the logs with
  access control and off-loading as well.
- **Account inactivity.** The 8.0.0 CLI Reference has no setting that disables
  accounts after 35 days of inactivity (`SRG-APP-000163-AU-002470`). Meet it on
  the remote authentication server or by a documented account review.
- **Lockout.** `admin-lockout-duration` locks an account for a set number of
  seconds; the SRG asks for the account to stay locked until an administrator
  releases it (`SRG-APP-000345-AU-000400`). Set a long duration and document
  the release procedure, or enforce lockout on the authentication server.
- **FIPS-CC mode** can be enabled only from the console.

## Design Considerations

- **Pick the release first, then the features.** If your design depends on a
  feature introduced in a certain release (for example NTPv4 with SHA-256 in
  8.0.0), that sets the minimum FortiAnalyzer version, and the firmware must
  also be a vendor-supported release (`SRG-APP-001035-AU-000430`).
- **Configure the core features first.** The heaviest CLS requirements (CAT I)
  are about access control, authentication, cryptography, transmission
  protection, and supported software. The core platform rows cover all of
  them.
- **Plan storage and retention together.** ADOM disk quotas, the data policy,
  disk-full alerting at 75 percent, and weekly backups of the log repository to
  another system all come from the CLS SRG.
- **Disable what you do not use.** FortiAI, the OT views, SOC modules, and
  cloud management features should be off unless they serve a documented
  purpose.
- **Forward, do not just store.** The CLS SRG expects log records to be
  off-loaded to a different system in real time; use log forwarding with
  reliable, TLS-protected transport to a second log server or SIEM.

## Implementation and Automation

### The FortiAnalyzer feature map

Abbreviations in the SRG column: **CLS** is the Central Log Server SRG and
**NDM** the Network Device Management SRG. The requirement titles are listed
in the next table. The command column follows the conventions in *Where the
commands come from*.

[Download the feature map as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/12-fortianalyzer-feature-version-and-srg-map-feature-map.csv) (349 rows).

| Category | Feature | Introduced (FortiAnalyzer) | SRG requirement(s) | Command to satisfy the requirement |
| --- | --- | --- | --- | --- |
| Core: log collection | Log collection from Fortinet devices (OFTP) | 7.0.0 or earlier | CLS `SRG-APP-000086-AU-000020`; CLS `SRG-APP-000516-AU-000330`; CLS `SRG-APP-000516-AU-000340`; CLS `SRG-APP-000439-AU-004310` | `config system global; set oftp-ssl-protocol tlsv1.2; set enc-algorithm high; end` |
| Core: log collection | Syslog collection from third-party devices | 7.0.0 or earlier | CLS `SRG-APP-000086-AU-000020`; CLS `SRG-APP-000516-AU-000340`; CLS `SRG-APP-000439-AU-004310` | `config system log settings; set syslog-over-tls-port 6514; set unencrypted-logging-tcp disable; set unencrypted-logging-udp disable; config client-cert-auth; set mode strict; end; end` |
| Core: log collection | Device registration and authorization | 7.0.0 or earlier | CLS `SRG-APP-000033-AU-001610`; CLS `SRG-APP-000516-AU-000330` | `config system admin setting; set unreg_dev_opt add_no_service; end` |
| Core: log collection | Log receipt time stamps | 7.0.0 or earlier | CLS `SRG-APP-000374-AU-000290`; CLS `SRG-APP-000086-AU-000030` | See the NTP server row |
| Core: log collection | No-logging detection for devices | 7.0.0 or earlier | CLS `SRG-APP-000360-AU-000130` | `config system locallog setting; set no-log-detection-threshold <MINUTES>; set log-interval-dev-no-logging <MINUTES>; end` |
| Core: log storage | Per-ADOM disk quota | 7.0.0 or earlier | CLS `SRG-APP-000359-AU-000120` | `execute log adom disk-quota <ADOM> <MB>` |
| Core: log storage | Per-device disk quota | 7.0.0 or earlier | CLS `SRG-APP-000359-AU-000120` | `execute log device disk-quota <DEVICE_ID> <MB>` |
| Core: log storage | Data policy (log retention by ADOM) | 7.0.0 or earlier | CLS `SRG-APP-000095-AU-000050`; CLS `SRG-APP-000090-AU-000070` | GUI: System Settings, ADOM data policy (Analytics and Archive retention) |
| Core: log storage | Disk-full alerting | 7.0.0 or earlier | CLS `SRG-APP-000359-AU-000120` | `config system locallog setting; set log-interval-disk-full <MINUTES>; end` and `config system alert-event; edit <ALERT>; config alert-destination; edit 1; set type mail; set to <ISSO_EMAIL>; end; end` |
| Core: log storage | Log file integrity (hash and authentication code) | 7.0.0 or earlier | CLS `SRG-APP-000080-AU-000010`; CLS `SRG-APP-000119-AU-000110` | `config system global; set log-checksum md5-auth; end` and `execute log-integrity <DEVICE> <VDOM> <LOG_FILE>` |
| Core: log storage | Keep logs after a device is deleted | 7.0.0 or earlier | CLS `SRG-APP-000120-AU-000120` | `config system log settings; set keep-dev-logs enable; end` |
| Core: log storage | Log backup to another system | 7.0.0 or earlier | CLS `SRG-APP-000125-AU-000300`; CLS `SRG-APP-000358-AU-000100` | `execute backup logs <DEVICE> sftp <SERVER_IP> <USER> <PASSWORD> <DIRECTORY>` |
| Core: log storage | Automatic deletion of logs, reports, and archives | 7.0.0 or earlier | CLS `SRG-APP-000095-AU-000050` | `config system auto-delete; config log-auto-deletion; set status enable; set retention months; set value <MONTHS>; end; end` |
| Core: log forwarding | Log forwarding to syslog, CEF, or another FortiAnalyzer | 7.0.0 or earlier | CLS `SRG-APP-000358-AU-000100`; CLS `SRG-APP-000515-AU-000110`; CLS `SRG-APP-000516-AU-000340`; CLS `SRG-APP-000439-AU-004310` | `config system log-forward; edit 1; set mode forwarding; set fwd-server-type syslog; set server-addr <SIEM_IP>; set fwd-reliable enable; set fwd-secure enable; set fwd-max-delay realtime; end` |
| Core: log forwarding | Log aggregation (collector to analyzer) | 7.0.0 or earlier | CLS `SRG-APP-000086-AU-000390` | `config system global; set log-mode collector; end` and `config system log-forward; edit 1; set mode aggregation; set server-addr <ANALYZER_IP>; end` |
| Core: log forwarding | Log fetching between FortiAnalyzer units | 7.0.0 or earlier | CLS `SRG-APP-000086-AU-000390`; CLS `SRG-APP-000439-AU-004310` | `config system log-fetch client-profile; edit 1; set server-ip <SERVER_IP>; set secure-connection enable; end` |
| Core: analysis | Log View: search and filter | 7.0.0 or earlier | CLS `SRG-APP-000115-AU-000160`; CLS `SRG-APP-000790-AU-000210` | GUI: Log View |
| Core: analysis | FortiView | 7.0.0 or earlier | CLS `SRG-APP-000745-AU-000120`; CLS `SRG-APP-000111-AU-000150` | GUI: FortiView |
| Core: analysis | SQL database for analytics | 7.0.0 or earlier | CLS `SRG-APP-000750-AU-000130` | `config system sql; set status local; end` |
| Core: analysis | Reports and report templates | 7.0.0 or earlier | CLS `SRG-APP-000770-AU-000170`; CLS `SRG-APP-000775-AU-000180` | GUI: Reports |
| Core: analysis | Event handlers and alerts | 7.0.0 or earlier | CLS `SRG-APP-000516-AU-000350`; CLS `SRG-APP-000516-AU-000380`; CLS `SRG-APP-000360-AU-000130` | GUI: Incidents & Events (Handlers); `config system alert-event` for system alerts |
| Core: analysis | Incidents | 7.0.0 or earlier | CLS `SRG-APP-000516-AU-000360`; CLS `SRG-APP-000775-AU-000180` | GUI: Incidents & Events (Incidents) |
| Core: analysis | Indicators of compromise (IOC) | 7.0.0 or earlier | CLS `SRG-APP-000516-AU-000350` | `config system log ioc; set status enable; set notification enable; end` |
| Core: analysis | Event correlation across devices | 7.0.0 or earlier | CLS `SRG-APP-000111-AU-000150`; CLS `SRG-APP-000516-AU-000350`; CLS `SRG-APP-000516-AU-000370` | GUI: Incidents & Events (Handlers, correlation rules) |
| Core: administration | Administrative domains (ADOMs) | 7.0.0 or earlier | CLS `SRG-APP-000033-AU-001610`; CLS `SRG-APP-000118-AU-000100` | `config system global; set adom-status enable; end` |
| Core: administration | Individual administrator accounts | 7.0.0 or earlier | CLS `SRG-APP-000148-AU-002270`; CLS `SRG-APP-000815-AU-000260` | `config system admin user; edit <ADMIN>; set profileid <PROFILE>; set adom <ADOM>; end` |
| Core: administration | Administrator profiles (role-based access) | 7.0.0 or earlier | CLS `SRG-APP-000033-AU-001610`; CLS `SRG-APP-000118-AU-000100`; CLS `SRG-APP-000119-AU-000110`; CLS `SRG-APP-000120-AU-000120`; CLS `SRG-APP-000121-AU-000130` | `config system admin profile; edit <PROFILE>; set log-viewer read; set report-viewer read; set system-setting none; end` |
| Core: administration | Trusted hosts for administrators | 7.0.0 or earlier | CLS `SRG-APP-000516-AU-000410` | `config system admin user; edit <ADMIN>; set trusthost1 <IP> <MASK>; end` |
| Core: administration | Password policy | 7.0.0 or earlier | CLS `SRG-APP-000164-AU-002480`; CLS `SRG-APP-000166-AU-002490`; CLS `SRG-APP-000170-AU-002530`; CLS `SRG-APP-000174-AU-002570` | `config system password-policy; set status enable; set minimum-length 15; set must-contain upper-case-letter lower-case-letter number non-alphanumeric; set change-4-characters enable; set expire 180; end` |
| Core: administration | Administrator lockout | 7.0.0 or earlier | CLS `SRG-APP-000065-AU-000240` | `config system global; set admin-lockout-threshold 3; set admin-lockout-duration <SECONDS>; end` |
| Core: administration | Idle session timeout | 7.0.0 or earlier | CLS `SRG-APP-000295-AU-000190` | `config system admin setting; set idle_timeout <MINUTES>; end` |
| Core: administration | Pre-login banner | 7.0.0 or earlier | CLS `SRG-APP-000068-AU-000035` | `config system global; set pre-login-banner enable; set pre-login-banner-message <DOD_BANNER>; end` |
| Core: administration | RADIUS administrator authentication | 7.0.0 or earlier | CLS `SRG-APP-000148-AU-002270`; NDM `SRG-APP-000516-NDM-000336` | `config system admin radius; edit <RADIUS>; set server <IP>; set secret <SECRET>; set protocol tls; set message-authenticator require; end` |
| Core: administration | TACACS+ administrator authentication | 7.0.0 or earlier | CLS `SRG-APP-000148-AU-002270`; NDM `SRG-APP-000516-NDM-000336` | `config system admin tacacs; edit <TACACS>; set server <IP>; set key <KEY>; set authorization enable; end` |
| Core: administration | LDAP administrator authentication | 7.0.0 or earlier | CLS `SRG-APP-000148-AU-002270`; NDM `SRG-APP-000516-NDM-000336` | `config system admin ldap; edit <LDAP>; set server <IP>; set secure ldaps; set ca-cert <CA_CERT>; end` |
| Core: administration | PKI (certificate) administrator authentication | 7.0.0 or earlier | CLS `SRG-APP-000175-AU-002630`; CLS `SRG-APP-000391-AU-002290`; CLS `SRG-APP-000149-AU-002280`; CLS `SRG-APP-000427-AU-000040` | `config system admin user; edit <ADMIN>; set user_type pki-auth; set subject <CERT_SUBJECT>; set ca <CA_CERT>; end` and `config system global; set clt-cert-req enable; end` |
| Core: administration | Two-factor authentication (FortiToken Cloud) | 7.0.0 or earlier | CLS `SRG-APP-000149-AU-002280` | `config system admin user; edit <ADMIN>; set two-factor-auth ftc-ftm; end` |
| Core: administration | FortiAnalyzer event log (own audit records) | 7.0.0 or earlier | CLS `SRG-APP-000095-AU-000680`; CLS `SRG-APP-000503-AU-000280`; CLS `SRG-APP-000026-AU-000580` | `config system locallog disk setting; set status enable; set severity information; end` |
| Core: administration | Sending FortiAnalyzer event logs to a syslog server | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000350`; CLS `SRG-APP-000358-AU-000100` | `config system syslog; edit <SYSLOG>; set ip <SYSLOG_IP>; set reliable enable; set secure-connection enable; end` and `config system locallog syslogd setting; set status enable; set syslog-name <SYSLOG>; end` |
| Core: administration | Alert email (SMTP) | 7.0.0 or earlier | CLS `SRG-APP-000360-AU-000130`; CLS `SRG-APP-000359-AU-000120` | `config system mail; edit <ID>; set server <SMTP_IP>; set secure-option starttls; set auth enable; end` |
| Core: security | HTTPS and SSH management encryption | 7.0.0 or earlier | CLS `SRG-APP-000439-AU-004310`; CLS `SRG-APP-000514-AU-002890` | `config system global; set global-ssl-protocol tlsv1.2; set ssl-low-encryption disable; set enc-algorithm high; end` |
| Core: security | Interface administrative access | 7.0.0 or earlier | CLS `SRG-APP-000141-AU-000090`; CLS `SRG-APP-000516-AU-000410` | `config system interface; edit <PORT>; set allowaccess https ssh; end` |
| Core: security | Local-in policies | 7.0.0 or earlier | CLS `SRG-APP-000516-AU-000410` | `config system local-in-policy; edit 1; set intf <PORT>; set src <IP> <MASK>; set dport 443; set action accept; end` |
| Core: security | FIPS-CC mode | 7.0.0 or earlier | CLS `SRG-APP-000514-AU-002890` | `config system fips; set status enable; end` |
| Core: security | Private data encryption | 7.0.0 or earlier | CLS `SRG-APP-000915-AU-000400` | `config system global; set private-data-encryption enable; end` |
| Core: security | CA certificates and CRLs | 7.0.0 or earlier | CLS `SRG-APP-000910-AU-000390`; CLS `SRG-APP-000175-AU-002630` | `config system certificate ca; edit <CA>; set ca <CERTIFICATE>; end` and `config system certificate crl; edit <CRL>; set http-url <CRL_URL>; end` |
| Core: security | SNMPv3 | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310` | `config system snmp user; edit <USER>; set security-level auth-priv; set auth-proto sha256; set priv-proto aes256; end` |
| Core: security | NTP server | 7.0.0 or earlier | CLS `SRG-APP-000920-AU-000410`; CLS `SRG-APP-000086-AU-000030`; NDM `SRG-APP-000395-NDM-000347` | `config system ntp; set status enable; config ntpserver; edit 1; set server <NTP_IP>; set authentication enable; set key-type sha256; set key-id <ID>; set key <KEY>; end; end` |
| Core: security | Firmware upgrade | 7.0.0 or earlier | CLS `SRG-APP-000456-AU-000270`; CLS `SRG-APP-001035-AU-000430`; CLS `SRG-APP-000810-AU-000250` | `execute restore image sftp <IMAGE_PATH> <SERVER_IP> <USER> <PASSWORD>` (use a vendor-supported release) |
| Core: security | Configuration backup | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340` | `config system backup all-settings; set status enable; set protocol sftp; set server <IP>; set user <USER>; set passwd <PASSWORD>; set crptpasswd <ENCRYPTION_PASSWORD>; end` |
| Core: security | Data masking for administrators | 7.0.0 or earlier | CLS `SRG-APP-000118-AU-000100` | `config system admin profile; edit <PROFILE>; set datamask enable; set datamask-fields <FIELDS>; end` |
| Core: security | High availability (HA) | 7.0.0 or earlier | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Core: security | Disable unused analytics modules | 7.0.0 or earlier | CLS `SRG-APP-000141-AU-000090` | `config system global; set disable-module <MODULES>; end` |
| Device Manager | World map added to the Device Manager | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Device Manager | Model device support for central logging | 7.0.0 and later | CLS `SRG-APP-000086-AU-000020`; CLS `SRG-APP-000516-AU-000330` | GUI: Device Manager (add a model device) |
| Device Manager | Security Fabric authorization | 7.0.1 and later | CLS `SRG-APP-000033-AU-001610`; CLS `SRG-APP-000516-AU-000330` | GUI: Device Manager (authorize devices) |
| Device Manager | Support for six major versions of FortiOS | 7.0.5+; 7.2.1+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Device Manager | Improved secure SD-WAN monitor | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Device Manager | SD-WAN application performance monitoring | 7.0.3 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | FortiOS connector health check | 7.0.0 and later | CLS `SRG-APP-000360-AU-000130` | GUI: Fabric View (connectors) |
| Security Operations (SOC) | Attach FortiMail connector actions to incidents | 7.0.0 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Incidents & Events (Incidents) |
| Security Operations (SOC) | SIEM correlation and analysis | 7.0.0 and later | CLS `SRG-APP-000111-AU-000150`; CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | Importing and exporting playbooks | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | FortiGuard outbreak detection service | 7.0.0 and later | CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Outbreak Alerts) |
| Security Operations (SOC) | Manage subnets | 7.0.0 and later | CLS `SRG-APP-000115-AU-000160` | GUI: Incidents & Events (subnet lists) |
| Security Operations (SOC) | EMS API support for FortiAnalyzer to notify and tag suspicious endpoints | 7.0.1 and later | CLS `SRG-APP-000516-AU-000350` | GUI: Fabric View (EMS connector) |
| Security Operations (SOC) | FortiClient event handler update | 7.0.0 and later | CLS `SRG-APP-000516-AU-000350`; CLS `SRG-APP-000516-AU-000380` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | FortiDeceptor default handler | 7.0.0 and later | CLS `SRG-APP-000516-AU-000350`; CLS `SRG-APP-000516-AU-000380` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | IPS signatures on-hold event handler | 7.0.0 and later | CLS `SRG-APP-000516-AU-000350`; CLS `SRG-APP-000516-AU-000380` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | NOC event handlers | 7.0.0 and later | CLS `SRG-APP-000360-AU-000130` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | Allowlisting on Event Handlers | 7.0.1 and later | CLS `SRG-APP-000516-AU-000380` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | Assign events for alert triage | 7.0.1 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Incidents & Events (Events) |
| Security Operations (SOC) | Filter syntax enhancement | 7.0.1 and later | CLS `SRG-APP-000115-AU-000160`; CLS `SRG-APP-000790-AU-000210` | GUI: Log View |
| Security Operations (SOC) | IPS signature lookup | 7.0.3 and later | CLS `SRG-APP-000775-AU-000180` | GUI: Log View |
| Security Operations (SOC) | IOC detection support for FortiMail logs | 7.0.3 and later | CLS `SRG-APP-000516-AU-000350` | `config system log ioc; set status enable; end` |
| Security Operations (SOC) | Subnet filter for Log View | 7.0.3 and later | CLS `SRG-APP-000115-AU-000160` | GUI: Log View |
| Security Operations (SOC) | Event handler configuration improvements | 7.0.3 and later | CLS `SRG-APP-000516-AU-000380` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | Shadow IT Monitoring Service | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Data sources tuning | 7.0.0 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | Asset and Identity Dashboards | 7.0.0 and later | CLS `SRG-APP-000745-AU-000120` | GUI: Asset and Identity Center |
| Security Operations (SOC) | Personalized custom views | 7.0.0 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | SD-WAN monitoring improvement | 7.0.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | FortiView monitors for FortiMail | 7.0.3 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | Threat research monitor | 7.0.3 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Log and Report | Improve log forwarding bandwidth efficiency | 7.0.0 and later | CLS `SRG-APP-000358-AU-000100` | `config system log-forward; edit <ID>; set fwd-compression enable; end` |
| Log and Report | Per-device log receiving rate limit | 7.0.0 and later | CLS `SRG-APP-000086-AU-000020` | `config system log ratelimit; set mode manual; config ratelimits; edit 1; set filter-type devid; set filter <DEVICE_ID>; set ratelimit <LOGS_PER_SEC>; end; end` |
| Log and Report | Mask user data in log forwarder | 7.0.0 and later | CLS `SRG-APP-000118-AU-000100` | `config system log-forward; edit <ID>; set log-masking-status enable; set log-masking-fields user srcip; set log-masking-key <KEY>; end` |
| Log and Report | FortiEDR Central Manager logging | 7.0.0 and later | CLS `SRG-APP-000086-AU-000020` | — |
| Log and Report | FortiAI logging on FortiAnalyzer | 7.0.1 and later | CLS `SRG-APP-000086-AU-000020` | — |
| Log and Report | Log forwarding enhancement | 7.0.1 and later | CLS `SRG-APP-000358-AU-000100`; CLS `SRG-APP-000515-AU-000110` | `config system log-forward; edit <ID>; set fwd-max-delay realtime; set fwd-reliable enable; set fwd-secure enable; end` |
| Log and Report | FortiSOAR central logging | 7.0.2 and later | CLS `SRG-APP-000086-AU-000020` | — |
| Log and Report | ZTNA traffic logs | 7.0.3 and later | CLS `SRG-APP-000086-AU-000020` | — |
| Log and Report | Improved caching mechanism for reports | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | `config system report auto-cache` (performance tuning) |
| Log and Report | FortiDeceptor report | 7.0.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Central UEBA table for custom reporting and widgets | 7.0.0 and later | CLS `SRG-APP-000770-AU-000170`; CLS `SRG-APP-000516-AU-000370` | GUI: Reports |
| Log and Report | FortiSandbox CTAP report | 7.0.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Organize reports in folders | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | Additional charts for SD-WAN reporting | 7.0.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | SD-WAN Summary Report | 7.0.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | FortiView support for FortiWeb | 7.0.1 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Log and Report | Shadow IT monitoring for cloud application and users | 7.0.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | FortiAI report and event handler | 7.0.2 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | FortiSandbox CTAP report update | 7.0.2 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Asset and identity report | 7.0.3 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Improved report time filter | 7.0.3 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | DNS security report | 7.0.3 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Dataset editor update | 7.0.3 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports (Datasets) |
| System | FortiAnalyzer HA graceful upgrade | 7.0.0 and later | CLS `SRG-APP-000456-AU-000270` | `config system ha; set mode a-p; end` (upgrade the HA cluster per the Upgrade Guide) |
| System | Theme mode | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| System | Add operation permissions to Admin profile | 7.0.0 and later | CLS `SRG-APP-000033-AU-001610` | `config system admin profile; edit <PROFILE>; set device-op none; end` |
| System | Admins can use a SAML SSO FortiCloud account to log in to FortiAnalyzer | 7.0.0 and later | CLS `SRG-APP-000148-AU-002270` | If unused: `config system saml; set forticloud-sso disable; end` |
| System | Suggest backup before upgrade | 7.0.2 and later | NDM `SRG-APP-000516-NDM-000340` | `execute backup all-settings sftp <SERVER_IP> <FILE> <USER> <PASSWORD>` |
| System | Admin user attributes can be set in the admin profile and override the individual admin settings | 7.0.3 and later | CLS `SRG-APP-000033-AU-001610`; CLS `SRG-APP-000516-AU-000410` | `config system admin profile; edit <PROFILE>; set trusthost1 <IP> <MASK>; end` and `config system admin user; edit <ADMIN>; set th-from-profile <TRUSTHOST_INDEX>; end` |
| System | Support for link aggregation | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| System | Migrate to Fabric ADOM | 7.0.2 and later | CLS `SRG-APP-000033-AU-001610` | — |
| Management Extensions | New management extension - FortiSOAR | 7.0.0 and later | CLS `SRG-APP-000141-AU-000090` | — |
| Management Extensions | New management extension - FortiSIEM Collector | 7.0.1 and later | CLS `SRG-APP-000086-AU-000390` | — |
| Management Extensions | Check for new MEA versions using CLI | 7.0.1 and later | CLS `SRG-APP-000456-AU-000270` | — |
| Other | FortiAnalyzer Setup wizard | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Other | FortiAnalyzer VM licenses | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Other | CSF support for multiple VDOMs | 7.0.0 and later | CLS `SRG-APP-000516-AU-000330` | — |
| Other | FortiAnalyzer Federation | 7.0.0 and later | CLS `SRG-APP-000086-AU-000390`; CLS `SRG-APP-000033-AU-001610` | — |
| Other | FortiAnalyzer VM supports Amazon EC2 IMDS version 2 | 7.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Other | Event log easier to read | 7.0.1 and later | CLS `SRG-APP-000095-AU-000680` | GUI: System Settings (Event Log) |
| Other | Migrate a FortiAnalyzer-VM license to VM-S | 7.0.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Other | SD-WAN application bandwidth per interface widget | 7.0.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Other | Deploying FortiAnalyzer-VM on IBM Cloud | 7.0.4 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Device Manager | Device Group | 7.2.0 and later | CLS `SRG-APP-000033-AU-001610` | GUI: Device Manager (device groups) |
| System | SAML SSO wildcard admin user to match all users on IdP server | 7.2.0 and later | CLS `SRG-APP-000148-AU-002270`; CLS `SRG-APP-000815-AU-000260` | `config system admin user; edit <ADMIN>; set user_type sso; set wildcard disable; end` (prefer named accounts) |
| Fabric View | OAuth 2.0 authentication for webhook connectors | 7.2.0 and later | CLS `SRG-APP-000439-AU-004310` | GUI: Fabric View (webhook connectors) |
| Security Operations (SOC) | Use ServiceNow connector in playbooks | 7.2.0 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Fabric View (connectors) and Incidents & Events (Automation) |
| Security Operations (SOC) | Network reconnaissance events detection | 7.2.0 and later | CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | Shadow IT events detection | 7.2.0 and later | CLS `SRG-APP-000516-AU-000380` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | New event handlers for NOC monitoring | 7.2.0 and later | CLS `SRG-APP-000360-AU-000130` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | Include IOC detected on FortiGate local traffic in FortiAnalyzer IOC view | 7.2.0 and later | CLS `SRG-APP-000516-AU-000350` | `config system log ioc; set status enable; end` |
| Security Operations (SOC) | Rule based event correlation | 7.2.2 and later | CLS `SRG-APP-000111-AU-000150`; CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Handlers, correlation rules) |
| Security Operations (SOC) | Data exfiltration detection | 7.2.2 and later | CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | SD-WAN chart to include more ADVPN shortcut information | 7.2.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | SD-WAN chart for MOS scoring | 7.2.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Add ZTNA dashboard to FortiView | 7.2.0 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | IoT visibility | 7.2.0 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | Traffic shaping charts | 7.2.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | CASB Apps Access widget | 7.2.1 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | Auto-refresh on FortiSoC dashboard elements | 7.2.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Rename Outbreak Alerts Service to Outbreak Detection Service | 7.2.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | Summary dashboard for event logs | 7.2.0 and later | CLS `SRG-APP-000745-AU-000120` | GUI: Log View |
| Log and Report | Log caching enhancement | 7.2.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | FortiNDR logging and reporting enhancements | 7.2.1 and later | CLS `SRG-APP-000086-AU-000020`; CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Security events consolidated page | 7.2.1 and later | CLS `SRG-APP-000745-AU-000120` | GUI: Log View |
| Log and Report | Log View right-click filtering supports OR, AND, and Replace | 7.2.3 and later | CLS `SRG-APP-000115-AU-000160` | GUI: Log View |
| Log and Report | Report in JSON format | 7.2.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Report cache control | 7.2.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | `config system report auto-cache` (performance tuning) |
| Log and Report | Upgrade report editor | 7.2.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Improve data visualization for the web usage report | 7.2.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | 360 Security Report | 7.2.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | VPN report update | 7.2.1 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Application risk and control report update | 7.2.1 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Bandwidth and applications report update | 7.2.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | Security events and incidents summary report update | 7.2.1 and later | CLS `SRG-APP-000770-AU-000170`; CLS `SRG-APP-000775-AU-000180` | GUI: Reports |
| Log and Report | High bandwidth application usage report update | 7.2.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | Cyber-bullying indicators report update | 7.2.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | Self-harm and risk indicators report update | 7.2.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | Use device metadata in datasets and reports | 7.2.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports (Datasets) |
| Log and Report | Search by object names | 7.2.0 and later | CLS `SRG-APP-000790-AU-000210` | GUI: Log View |
| Log and Report | Generate system event log when daemon crashes | 7.2.2 and later | CLS `SRG-APP-000095-AU-000680` | `config system locallog setting; set log-daemon-crash enable; end` |
| System | Global log search across FortiAnalyzer Fabric members | 7.2.1 and later | CLS `SRG-APP-000790-AU-000210`; CLS `SRG-APP-000086-AU-000390` | GUI: Log View (Fabric supervisor) |
| System | FortiAnalyzer French GUI support | 7.2.3 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| System | FortiAnalyzer supports VLANs on physical network interfaces | 7.2.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| System | FortiAnalyzer Fabric usability improvements | 7.2.0 and later | CLS `SRG-APP-000086-AU-000390` | GUI: System Settings (Fabric Management) |
| System | Add LLDP support on FMG and FAZ | 7.2.1 and later | CLS `SRG-APP-000141-AU-000090` | If unused, leave LLDP disabled on the interface (GUI: System Settings, Network) |
| System | Mandatory FortiCare/FortiCloud registration | 7.2.1 and later | CLS `SRG-APP-000456-AU-000270` | — |
| System | SAML assertions and SAML requests can be now signed to better support third-party IdPs | 7.2.3 and later | CLS `SRG-APP-000148-AU-002270`; CLS `SRG-APP-000080-AU-000010` | `config system saml; set want-assertions-signed enable; set auth-request-signed enable; end` |
| Cloud Services | VM flexible shapes support for Oracle Cloud Infrastructure | 7.2.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Cloud Services | FortiAnalyzer-VM has been added to the Flex-VM offering | 7.2.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Cloud Services | FortiAnalyzer-VM supported in OCI DRCC | 7.2.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Cloud Services | FortiAnalyzer management from FortiCloud via SSO | 7.2.5 and later | CLS `SRG-APP-000148-AU-002270` | If unused: `config system central-management; set type none; end` |
| Device Manager | Support FortiGate HA vSN | 7.4.0 and later | CLS `SRG-APP-000516-AU-000330` | — |
| Fabric View | Reference individual fabric devices | 7.4.1 and later | CLS `SRG-APP-000516-AU-000330` | — |
| Fabric View | Webhook connector to support MS Teams | 7.4.0 and later | CLS `SRG-APP-000360-AU-000130`; CLS `SRG-APP-000516-AU-000350` | GUI: Fabric View (webhook connectors) |
| Fabric View | Webhook enhancement | 7.4.4 and later | CLS `SRG-APP-000360-AU-000130`; CLS `SRG-APP-000516-AU-000350` | GUI: Fabric View (webhook connectors) |
| Fabric View | Report generation from EMS connector data | 7.4.4 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Security Operations (SOC) | Playbook event trigger correlation rules | 7.4.1 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Incidents & Events (Automation) |
| Security Operations (SOC) | New predefined correlation event handlers | 7.4.0 and later | CLS `SRG-APP-000111-AU-000150`; CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | Update to the Event Handler rule configuration | 7.4.2 and later | CLS `SRG-APP-000516-AU-000380` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | SD-WAN Cloud Assisted Monitoring service widgets | 7.4.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Data leak prevention monitor in FortiView | 7.4.1 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | FortiProxy central visibility | 7.4.1 and later | CLS `SRG-APP-000086-AU-000020`; CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | Compromised hosts improvements | 7.4.2 and later | CLS `SRG-APP-000516-AU-000350` | `config system log ioc; set status enable; set notification enable; end` |
| Security Operations (SOC) | Replay attacks in the Threat Map | 7.4.2 and later | CLS `SRG-APP-000775-AU-000180` | GUI: FortiView |
| Security Operations (SOC) | Sankey view for SASE network | 7.4.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Managed endpoint vulnerability dashboard | 7.4.4 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | New charts in the Asset Identity Center | 7.4.0 and later | CLS `SRG-APP-000516-AU-000370` | GUI: Asset and Identity Center |
| Security Operations (SOC) | FortiSoC GUI reorganization | 7.4.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Notifications for new Outbreak Alerts | 7.4.1 and later | CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Outbreak Alerts) |
| Security Operations (SOC) | MITRE ATT&CK matrices for Enterprise and ICS | 7.4.1 and later | CLS `SRG-APP-000775-AU-000180` | GUI: Incidents & Events |
| Security Operations (SOC) | Deliver reports, event handlers, and SIEM rules as FortiGuard packages | 7.4.2 and later | CLS `SRG-APP-000456-AU-000270` | — |
| Security Operations (SOC) | MITRE information included in outbreak detection | 7.4.2 and later | CLS `SRG-APP-000775-AU-000180` | GUI: Incidents & Events (Outbreak Alerts) |
| Log and Report | FortiAnalyzer supports FortiWeb Cloud attack logs | 7.4.0 and later | CLS `SRG-APP-000086-AU-000020` | — |
| Log and Report | Support parsing and addition of third-party application logs to the SIEM DB | 7.4.0 and later | CLS `SRG-APP-000086-AU-000020`; CLS `SRG-APP-000089-AU-000400` | GUI: Log View (log parsers) |
| Log and Report | Per-ADOM log rate | 7.4.0 and later | CLS `SRG-APP-000086-AU-000020` | `config system log ratelimit; set mode manual; config ratelimits; edit 1; set filter-type adom; set filter <ADOM>; set ratelimit <LOGS_PER_SEC>; end; end` |
| Log and Report | Support EMS multitenancy via FortiAnalyzer ADOMs | 7.4.1 and later | CLS `SRG-APP-000033-AU-001610` | — |
| Log and Report | Logging support for FortiCASB | 7.4.1 and later | CLS `SRG-APP-000086-AU-000020` | — |
| Log and Report | Logging support for FortiPAM | 7.4.1 and later | CLS `SRG-APP-000086-AU-000020` | — |
| Log and Report | Logging support for FortiToken Cloud | 7.4.1 and later | CLS `SRG-APP-000086-AU-000020` | — |
| Log and Report | Support parsing and addition of third-party application logs to the SIEM DB in JSON format | 7.4.1 and later | CLS `SRG-APP-000086-AU-000020`; CLS `SRG-APP-000089-AU-000400` | GUI: Log View (log parsers) |
| Log and Report | FortiAnalyzer supports packet header information for FortiWeb traffic log | 7.4.1 and later | CLS `SRG-APP-000089-AU-000400` | — |
| Log and Report | Support additional log fields for long live session logs | 7.4.2 and later | CLS `SRG-APP-000089-AU-000400` | — |
| Log and Report | Support FortiWeb performance statistics logs | 7.4.3 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | Fluentd support for public cloud integration | 7.4.0 and later | CLS `SRG-APP-000358-AU-000100`; CLS `SRG-APP-000439-AU-004310` | `config system log-forward; edit <ID>; set fwd-server-type fwd-via-output-plugin; set fwd-output-plugin-id <PLUGIN>; end` |
| Log and Report | Report guidance | 7.4.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | PCI Security Rating Report | 7.4.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Cyber Threats Assessment Report update | 7.4.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Threat Report update | 7.4.0 and later | CLS `SRG-APP-000770-AU-000170`; CLS `SRG-APP-000775-AU-000180` | GUI: Reports |
| Log and Report | FSBP Security Rating Report | 7.4.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | CIS Controls Security Rating report | 7.4.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Shadow IT Report | 7.4.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | FortiADC Report | 7.4.1 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | ZTNA Report | 7.4.1 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | FortiEDR Report | 7.4.1 and later | CLS `SRG-APP-000770-AU-000170`; CLS `SRG-APP-000775-AU-000180` | GUI: Reports |
| Log and Report | ISO 27001:2022 Compliance Security Rating Report | 7.4.1 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Exporting a report with settings | 7.4.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | DLP report | 7.4.1 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | PCI DSS security rating report update | 7.4.1 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | HIPAA report | 7.4.2 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | SOC2 compliance report | 7.4.3 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Endpoint security vulnerability report | 7.4.4 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Time zone settings per ADOMs/Reports | 7.4.0 and later | CLS `SRG-APP-000086-AU-000030` | — |
| Log and Report | New API to restore logs | 7.4.0 and later | CLS `SRG-APP-000125-AU-000300` | — |
| Log and Report | Download PCAP files in encrypted and ZIP format | 7.4.1 and later | CLS `SRG-APP-000118-AU-000100` | `config system log pcap-file; set download-mode zip-with-password; end` |
| System | Geo-redundant High Availability (HA) | 7.4.0 and later | CLS `SRG-APP-000086-AU-000390` | `config system ha; set mode a-p; set unicast enable; end` |
| System | A new restricted admin profile can be used to only change the administrators passwords | 7.4.2 and later | CLS `SRG-APP-000033-AU-001610` | `config system admin profile; edit <PROFILE>; set write-passwd-access specify-by-user; set write-passwd-user-list <USERS>; end` |
| System | Per-ADOM admin profile | 7.4.2 and later | CLS `SRG-APP-000033-AU-001610` | `config system admin profile; edit <PROFILE>; set scope adom; end` |
| System | DNS settings per ADOM | 7.4.3 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| System | FortiAnalyzer GUI enhancements | 7.4.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| System | Fabric of FAZ topology chart | 7.4.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| System | Fabric of FAZ: member authorization with supervisor | 7.4.0 and later | CLS `SRG-APP-000086-AU-000390`; CLS `SRG-APP-000033-AU-001610` | `config system soc-fabric; set status enable; set role supervisor; set secure-connection enable; config trusted-list; edit 1; set serial <MEMBER_SN>; end; end` |
| System | Fabric of FAZ global FortiView support | 7.4.0 and later | CLS `SRG-APP-000745-AU-000120`; CLS `SRG-APP-000086-AU-000390` | GUI: FortiView (Fabric supervisor) |
| System | Fabric of FAZ: Central report support and creating Fabric groups | 7.4.0 and later | CLS `SRG-APP-000770-AU-000170`; CLS `SRG-APP-000086-AU-000390` | GUI: Reports (Fabric supervisor) |
| System | Prevent FortiAnalyzers with an expired support contract from upgrading to a major or minor firmware release | 7.4.0 and later | CLS `SRG-APP-001035-AU-000430` | — |
| System | FortiManager and FortiAnalyzer support HTTP/2 for improved security, multiplexing, and reduced network latency | 7.4.1 and later | CLS `SRG-APP-000439-AU-004310` | `config system global; set httpd-ssl-protocol tlsv1.3 tlsv1.2; end` |
| System | Backup strategy and configuration setup added to the FortiAnalyzer setup wizard | 7.4.2 and later | NDM `SRG-APP-000516-NDM-000340`; CLS `SRG-APP-000125-AU-000300` | `config system backup all-settings; set status enable; set protocol sftp; set server <IP>; end` |
| System | FortiAnalyzer fabric HA awareness | 7.4.3 and later | CLS `SRG-APP-000086-AU-000390` | — |
| System | FortiAnalyzer supports IPv6 address type for syslog server configuration | 7.4.3 and later | NDM `SRG-APP-000516-NDM-000350` | `config system syslog; edit <SYSLOG>; set ip <IPV6>; set reliable enable; set secure-connection enable; end` |
| System | FortiAnalyzer introduces OS firmware levels Feature(F) and Mature(M) | 7.4.4+; 7.6.0+ | CLS `SRG-APP-001035-AU-000430` | — |
| Cloud Services | FortiAnalyzer supports FortiCare Elite Service | 7.4.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Cloud Services | FortiAnalyzer supports M6 and M7 instance types in AWS | 7.4.3 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Operational Technology | Operational Technology (OT) Security Service | 7.4.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | If unused: `config system global; set disable-module ot-view; end` |
| Operational Technology | OT Purdue Model in a consolidated Asset & Identity Center Dashboard | 7.4.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | If unused: `config system global; set disable-module ot-view; end` |
| Operational Technology | OT Security Risk Report | 7.4.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Operational Technology | NERC CIP compliance security rating report (OT) | 7.4.3 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Other | Licensing adjustment | 7.4.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Fabric View | Ingest logs or event data through API polling | 7.6.2 and later | CLS `SRG-APP-000086-AU-000020` | GUI: Fabric View (connectors) |
| Security Operations (SOC) | Native SOAR connectors | 7.6.0 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Fabric View (connectors) |
| Security Operations (SOC) | New connectors for automation | 7.6.0 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Fabric View (connectors) |
| Security Operations (SOC) | Cloning predefined playbooks, indicators, and reports | 7.6.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Execute playbook from incident | 7.6.2 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Incidents & Events (Incidents) |
| Security Operations (SOC) | Support FortiEDR connectors | 7.6.3 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Fabric View (connectors) |
| Security Operations (SOC) | Unified incident response page | 7.6.0 and later | CLS `SRG-APP-000516-AU-000360`; CLS `SRG-APP-000775-AU-000180` | GUI: Incidents & Events (Incidents) |
| Security Operations (SOC) | Incident analysis re-design | 7.6.0 and later | CLS `SRG-APP-000775-AU-000180` | GUI: Incidents & Events (Incidents) |
| Security Operations (SOC) | Export incident | 7.6.0 and later | CLS `SRG-APP-000775-AU-000180` | GUI: Incidents & Events (Incidents) |
| Security Operations (SOC) | New indicators page | 7.6.0 and later | CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Indicators) |
| Security Operations (SOC) | Indicator enrichment | 7.6.0 and later | CLS `SRG-APP-000775-AU-000180` | GUI: Incidents & Events (Indicators) |
| Security Operations (SOC) | Automatically raise actionable events for incident investigation | 7.6.0 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | Raise an incident when an outbreak is detected | 7.6.0 and later | CLS `SRG-APP-000516-AU-000360`; CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Outbreak Alerts) |
| Security Operations (SOC) | Merge basic event handler and correlation event handler GUIs | 7.6.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Event handlers: use SIEM database | 7.6.2 and later | CLS `SRG-APP-000111-AU-000150` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | New event handlers for ZTNA login based breach detections | 7.6.2 and later | CLS `SRG-APP-000516-AU-000370`; CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | Safeguarding event handler | 7.6.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Block IP, URL, or domain from incident | 7.6.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Content package update page | 7.6.3 and later | CLS `SRG-APP-000456-AU-000270` | — |
| Security Operations (SOC) | Scheduled alert email notifications | 7.6.3 and later | CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (notification profiles) |
| Security Operations (SOC) | FortiAnalyzer Cloud Connector | 7.6.3 and later | CLS `SRG-APP-000358-AU-000100` | GUI: Fabric View (connectors) |
| Security Operations (SOC) | Alert ingestion service | 7.6.3 and later | CLS `SRG-APP-000086-AU-000020` | GUI: Fabric View (connectors) |
| Security Operations (SOC) | Geo-alerting and MS Exchange event handlers | 7.6.3 and later | CLS `SRG-APP-000516-AU-000370`; CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | Automatic event suppression | 7.6.3 and later | CLS `SRG-APP-000516-AU-000380` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | Reduce delay and improve notification performance | 7.6.4 and later | CLS `SRG-APP-000516-AU-000350` | — |
| Security Operations (SOC) | Excessive email sending detection | 7.6.4 and later | CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | IoT Dashboard | 7.6.0 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | Email metrics dashboard | 7.6.0 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | SOC dashboard for alerts and incidents | 7.6.0 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | SD-WAN FortiView dashboard redesign | 7.6.4 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | XDR dashboard | 7.6.4 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | Using SIEM database for the asset & identity tables | 7.6.2 and later | CLS `SRG-APP-000516-AU-000370` | GUI: Asset and Identity Center |
| Security Operations (SOC) | UEBA: assets and identities with risk score | 7.6.4 and later | CLS `SRG-APP-000516-AU-000370` | `config system log ueba; set ip-unique-scope adom; end` |
| Security Operations (SOC) | Connector to Windows Active Directory | 7.6.5 and later | CLS `SRG-APP-000516-AU-000370` | GUI: Fabric View (connectors) |
| Security Operations (SOC) | Safeguarding keywords | 7.6.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Update Outbreak Alerts GUI | 7.6.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Enable SOC remote access for the Managed FortiAnalyzer Service | 7.6.5 and later | CLS `SRG-APP-000516-AU-000410` | If unused: `config system central-management; set socaas-remote-access disable; end` |
| Security Operations (SOC) | FortiSOC Connector | 7.6.7 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Fabric View (connectors) |
| Log and Report | Reorganize menus in Log View | 7.6.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | Add device log data and GUI columns into web filter traffic | 7.6.0 and later | CLS `SRG-APP-000089-AU-000400` | — |
| Log and Report | Support FortiAP as device type | 7.6.2 and later | CLS `SRG-APP-000086-AU-000020` | — |
| Log and Report | User experience improvements for Log View | 7.6.2 and later | CLS `SRG-APP-000790-AU-000210` | GUI: Log View |
| Log and Report | FortiMail Log View improvement | 7.6.4 and later | CLS `SRG-APP-000790-AU-000210` | GUI: Log View |
| Log and Report | Decode the attackcontext field in IPS logs | 7.6.3 and later | CLS `SRG-APP-000089-AU-000400` | `config system log-forward; edit <ID>; set fwd-syslog-decode-b64 enable; end` |
| Log and Report | New metrics for SD-WAN monitoring | 7.6.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | NIST CSF Compliance Report | 7.6.0 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Safeguarding report | 7.6.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | NGFW assessment report | 7.6.2 and later | CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | Bandwidth and applications report (SIEM) | 7.6.2 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | Anomaly login report | 7.6.7+; 8.0.0+ | CLS `SRG-APP-000516-AU-000370`; CLS `SRG-APP-000770-AU-000170` | GUI: Reports |
| Log and Report | FortiDeceptor incident report | 7.6.7+; 8.0.0+ | CLS `SRG-APP-000770-AU-000170`; CLS `SRG-APP-000775-AU-000180` | GUI: Reports |
| Log and Report | Object usage APIs | 7.6.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | Add normalized log fields | 7.6.0 and later | CLS `SRG-APP-000089-AU-000400` | — |
| Log and Report | Expanding log parsers for third-party applications through syslog | 7.6.0 and later | CLS `SRG-APP-000086-AU-000020`; CLS `SRG-APP-000089-AU-000400` | GUI: Log View (log parsers) |
| Log and Report | Migrate logs to ClickHouse | 7.6.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| FortiAI | FortiAI license | 7.6.0 and later | CLS `SRG-APP-000141-AU-000090` | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | Using FortiAI | 7.6.0 and later | CLS `SRG-APP-000141-AU-000090` | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | FortiAI data privacy | 7.6.0 and later | CLS `SRG-APP-000141-AU-000090`; CLS `SRG-APP-000118-AU-000100` | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | FortiAI uses Retrieval-Augmented Generation (RAG) to enhance accuracy | 7.6.2 and later | CLS `SRG-APP-000141-AU-000090` | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | FortiAI event monitor and threat hunting enhancements | 7.6.2 and later | CLS `SRG-APP-000141-AU-000090` | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | Display FortiAI top-up token quantities in the GUI | 7.6.3 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| FortiAI | Feedback function collects overall user satisfaction and suggestions on FortiAnalyzer AI | 7.6.5 and later | CLS `SRG-APP-000141-AU-000090` | If unused: `config system global; set ai-mode disable; end` |
| System | FortiAnalyzer detects concurrent backup sessions and returns error message | 7.6.2 and later | NDM `SRG-APP-000516-NDM-000340` | — |
| System | Event log for FortiAnalyzer API Calls | 7.6.3 and later | CLS `SRG-APP-000095-AU-000680` | `config system global; set jsonapi-log all; end` |
| System | Legal third party disclosure panel | 7.6.5+; 8.0.0+ | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| System | Role-based access control with FortiAnalyzer Fabric | 7.6.3 and later | CLS `SRG-APP-000033-AU-001610` | GUI: System Settings (Fabric Management) |
| System | New FortiAnalyzer Fabric management page | 7.6.3 and later | CLS `SRG-APP-000086-AU-000390` | GUI: System Settings (Fabric Management) |
| System | Members not counted for ADOM limits on the supervisor | 7.6.4 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Other | Improve collapse function for the GUI tree menu | 7.6.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Other | Support for FortiTIP service integration | 7.6.4 and later | CLS `SRG-APP-000141-AU-000090` | — |
| Security Operations (SOC) | Playbook editor improvements | 8.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | Alert explorer improvements | 8.0.0 and later | CLS `SRG-APP-000745-AU-000120` | GUI: Incidents & Events |
| Security Operations (SOC) | Machine learning for anomaly detection | 8.0.0 and later | CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | GUI support for machine learning for anomaly detection | 8.0.1 and later | CLS `SRG-APP-000516-AU-000350` | GUI: Incidents & Events (Handlers) |
| Security Operations (SOC) | Raise incidents for on-premise FortiNDR detections | 8.0.1 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Incidents & Events (Incidents) |
| Security Operations (SOC) | AI Access Visibility dashboard | 8.0.0 and later | CLS `SRG-APP-000745-AU-000120` | GUI: FortiView |
| Security Operations (SOC) | Improvements to the user experience in the Asset and Identity Center | 8.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | FortiMQ connector for automated blocking | 8.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Security Operations (SOC) | SIEM Collector on FortiAnalyzer | 8.0.1 and later | CLS `SRG-APP-000086-AU-000020`; CLS `SRG-APP-000086-AU-000390` | — |
| Log and Report | FortiData incident support | 8.0.0 and later | CLS `SRG-APP-000516-AU-000360` | GUI: Incidents & Events (Incidents) |
| Log and Report | FortiAnalyzer Fluentd supports the Azure Monitor Log Ingestion API | 8.0.0 and later | CLS `SRG-APP-000358-AU-000100`; CLS `SRG-APP-000439-AU-004310` | `config system log-forward; edit <ID>; set fwd-server-type fwd-via-output-plugin; set fwd-output-plugin-id <PLUGIN>; end` |
| Log and Report | Shadow-AI report | 8.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| Log and Report | FortiNDR Incident Report | 8.0.1 and later | CLS `SRG-APP-000770-AU-000170`; CLS `SRG-APP-000775-AU-000180` | GUI: Reports |
| Log and Report | OT Network Traffic and Policy Optimization Report | 8.0.1 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| FortiAI | FortiAI alert triage agent | 8.0.0 and later | CLS `SRG-APP-000141-AU-000090` | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | FortiAI threat posture timeline | 8.0.0 and later | CLS `SRG-APP-000141-AU-000090` | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | Account-level FortiAI token top-up | 8.0.0 and later | No direct requirement; if unused, disable (CLS `SRG-APP-000141-AU-000090`) | — |
| FortiAI | FortiAI assistant prompt suggestions by role | 8.0.1 and later | CLS `SRG-APP-000141-AU-000090` | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | FortiAI agents | 8.0.1 and later | CLS `SRG-APP-000141-AU-000090` | If unused: `config system global; set ai-mode disable; end` |
| FortiAI | FortiAI enabled on FortiAnalyzer supports web proxy deployments | 8.0.1 and later | CLS `SRG-APP-000439-AU-004310` | `config system web-proxy; set status enable; set address <PROXY_IP>; set port <PORT>; end` |
| System | Custom session labels in FortiAnalyzer event logs | 8.0.0 and later | CLS `SRG-APP-000095-AU-000680` | `config system admin setting; set custom-session-label enable; set custom-session-label-mode unique-per-session; end` |
| System | SAML SSO supports SHA-256 and SHA-512 for both IdP and SP | 8.0.0 and later | CLS `SRG-APP-000610-AU-000050`; CLS `SRG-APP-000148-AU-002270` | `config system saml; set digest-method sha256; set signature-algorithm rsa-sha256; set idp-digest-method sha256; set idp-signature-algorithm rsa-sha256; end` |
| System | FortiAnalyzer supports NTPv4 with SHA-256 encryption | 8.0.0 and later | CLS `SRG-APP-000920-AU-000410`; NDM `SRG-APP-000395-NDM-000347` | `config system ntp; config ntpserver; edit 1; set ntpv3 disable; set authentication enable; set key-type sha256; set key-id <ID>; set key <KEY>; end; end` |
| System | Time-base retention is configurable for the task monitor and event log | 8.0.0 and later | CLS `SRG-APP-000095-AU-000050` | `config system locallog disk setting; set log-max-days <DAYS>; end` |
| System | Assign access to multiple fabric groups for a single admin | 8.0.0 and later | CLS `SRG-APP-000033-AU-001610` | GUI: System Settings (Administrators) |
| System | FortiAnalyzer Fabric Supervisor HA | 8.0.0 and later | CLS `SRG-APP-000086-AU-000390` | `config system ha; set mode a-p; end` |
| System | Threat Hunting on the FortiAnalyzer Fabric Supervisor | 8.0.1 and later | CLS `SRG-APP-000775-AU-000180`; CLS `SRG-APP-000086-AU-000390` | GUI: Incidents & Events (Threat Hunting) |
| Other | FortiCare Elite or FortiCare Premium required to download FortiGuard objects | 8.0.0 and later | CLS `SRG-APP-000456-AU-000270` | — |

### Requirement reference

The SRG requirements used in the map, with their severity in the current SRG
releases:

[Download the requirement reference as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/12-fortianalyzer-feature-version-and-srg-map-requirements.csv) (65 rows).

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| CLS | `SRG-APP-000026-AU-000580` | CAT II | The Central Log Server must automatically audit account creation. |
| CLS | `SRG-APP-000033-AU-001610` | CAT I | The Central Log Server must be configured to enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies. |
| CLS | `SRG-APP-000065-AU-000240` | CAT II | The Central Log Server must enforce the limit of three consecutive invalid logon attempts by a user during a 15 minute time period. |
| CLS | `SRG-APP-000068-AU-000035` | CAT III | The Central Log Server must display the Standard Mandatory DoW Notice and Consent Banner before granting access to the Central Log Server. |
| CLS | `SRG-APP-000080-AU-000010` | CAT II | The Central Log Server must be configured to protect the data sent from hosts and devices from being altered in a way that may prevent the attribution of an action to an individual (or process acting on behalf of an individual). |
| CLS | `SRG-APP-000086-AU-000020` | CAT III | The Central Log Server must be configured to aggregate log records from organization-defined devices and hosts within its scope of coverage. |
| CLS | `SRG-APP-000086-AU-000030` | CAT III | Time stamps recorded on the log records in the Central Log Server must be configured to synchronize to within one second of the host server or, if NTP is configured directly in the log server, the NTP time source must be the same as the host and devices within its scope of coverage. |
| CLS | `SRG-APP-000086-AU-000390` | CAT II | Where multiple log servers are installed in the enclave, each log server must be configured to aggregate log records to a central aggregation server or other consolidated events repository. |
| CLS | `SRG-APP-000089-AU-000400` | CAT II | The Central Log Server must be configured to retain the DoW-defined attributes of the log records sent by the devices and hosts. |
| CLS | `SRG-APP-000090-AU-000070` | CAT III | The Central Log Server must be configured to allow only the Information System Security Manager (ISSM) (or individuals or roles appointed by the ISSM) to select which auditable events are to be retained. |
| CLS | `SRG-APP-000095-AU-000050` | CAT III | The System Administrator (SA) and Information System Security Manager (ISSM) must configure the retention of the log records based on criticality level, event type, and/or retention period, at a minimum. |
| CLS | `SRG-APP-000095-AU-000680` | CAT III | The Central Log Server must produce audit records containing information to establish what type of events occurred. |
| CLS | `SRG-APP-000111-AU-000150` | CAT III | The Central Log Server must be configured to perform analysis of log records across multiple devices and hosts in the enclave that can be reviewed by authorized individuals. |
| CLS | `SRG-APP-000115-AU-000160` | CAT III | The Central Log Server must be configured to perform on-demand filtering of the log records for events of interest based on organization-defined criteria. |
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
| CLS | `SRG-APP-000174-AU-002570` | CAT III | The Central Log Server must be configured to enforce a 180-day maximum password lifetime restriction. |
| CLS | `SRG-APP-000175-AU-002630` | CAT I | The Central Log Server, when utilizing PKI-based authentication, must validate certificates by constructing a certification path (which includes status information) to an accepted trust anchor. |
| CLS | `SRG-APP-000295-AU-000190` | CAT II | The Central Log Server must automatically terminate a user session after organization-defined conditions or trigger events requiring session disconnect. |
| CLS | `SRG-APP-000345-AU-000400` | CAT II | The Central Log Server must automatically lock the account until the locked account is released by an administrator when three unsuccessful login attempts in 15 minutes are exceeded. |
| CLS | `SRG-APP-000358-AU-000100` | CAT II | The Central Log Server must be configured to off-load log records onto a different system or media than the system being audited. |
| CLS | `SRG-APP-000359-AU-000120` | CAT III | The Central Log Server must be configured to send an immediate alert to the System Administrator (SA) and Information System Security Officer (ISSO) (at a minimum) when allocated log record storage volume reaches 75 percent of the repository maximum log record storage capacity. |
| CLS | `SRG-APP-000360-AU-000130` | CAT III | For the host and devices within its scope of coverage, the Central Log Server must be configured to send a real-time alert to the System Administrator (SA) and Information System Security Officer (ISSO) (at a minimum) of all audit failure events, such as loss of communications with hosts and devices, or if log records are no longer being received. |
| CLS | `SRG-APP-000374-AU-000290` | CAT III | Upon receipt of the log record from hosts and devices, the Central Log Server must be configured to record time stamps of the time of receipt that can be mapped to Coordinated Universal Time (UTC). |
| CLS | `SRG-APP-000391-AU-002290` | CAT II | The Central Log Server must be configured to accept the DoW common access card (CAC) credential to support identity management and personal authentication. |
| CLS | `SRG-APP-000427-AU-000040` | CAT II | The Central Log Server must only allow the use of DoW Public Key Infrastructure (PKI)-established certificate authorities for verification of the establishment of protected sessions. |
| CLS | `SRG-APP-000439-AU-004310` | CAT I | The Central Log Server must be configured to protect the confidentiality and integrity of transmitted information. |
| CLS | `SRG-APP-000456-AU-000270` | CAT I | The Central Log Server must install security-relevant software updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| CLS | `SRG-APP-000503-AU-000280` | CAT II | The Central Log Server must generate audit records when successful/unsuccessful logon attempts occur. |
| CLS | `SRG-APP-000514-AU-002890` | CAT I | The Central Log Server must implement NIST FIPS-validated cryptography for the following: to provision digital signatures; to generate cryptographic hashes; and/or to protect unclassified information requiring confidentiality and cryptographic protection. |
| CLS | `SRG-APP-000515-AU-000110` | CAT III | The Central Log Server must be configured to off-load interconnected systems in real time and off-load standalone systems weekly, at a minimum. |
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
| CLS | `SRG-APP-000790-AU-000210` | CAT II | The Central Log Server must implement the capability to process, sort, and search audit records for events of interest based on organization-defined audit fields within audit records. |
| CLS | `SRG-APP-000810-AU-000250` | CAT II | The Central Log Server must prevent the installation of organization-defined software and firmware components without verification that the component has been digitally signed using a certificate that is recognized and approved by the organization. |
| CLS | `SRG-APP-000815-AU-000260` | CAT II | The Central Log Server must require users to be individually authenticated before granting access to the shared accounts or resources. |
| CLS | `SRG-APP-000910-AU-000390` | CAT II | The Central Log Server must include only approved trust anchors in trust stores or certificate stores managed by the organization. |
| CLS | `SRG-APP-000915-AU-000400` | CAT II | The Central Log Server must provide protected storage for cryptographic keys with organization-defined safeguards and/or hardware protected key store. |
| CLS | `SRG-APP-000920-AU-000410` | CAT II | The Central Log Server must synchronize system clocks within and between systems or system components. |
| CLS | `SRG-APP-001035-AU-000430` | CAT I | The Central Log Server must be a version supported by the vendor. |
| NDM | `SRG-APP-000395-NDM-000310` | CAT II | The network device must be configured to authenticate SNMP messages using a FIPS-validated Keyed-Hash Message Authentication Code (HMAC). |
| NDM | `SRG-APP-000395-NDM-000347` | CAT II | The network device must authenticate Network Time Protocol sources using authentication that is cryptographically based. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |

### Collecting evidence

Collect `show full-configuration` and `get system status` from the
FortiAnalyzer, and export the GUI-configured items the map points to: the
event handler list, report schedules, the ADOM data policy and disk quotas,
and the log forwarding settings. Attach them to the SRG-based checklist
(Chapter 03).

## Validation and Troubleshooting

- **A feature in the map is missing on your FortiAnalyzer.** Check the version
  column against your release, then check the license: FortiAI, the OT
  Security Service, and several SOC features need a subscription.
- **Logs stop arriving after you disable unencrypted logging.** The devices
  are still sending plain syslog or unencrypted OFTP. Move them to TLS first,
  then disable the unencrypted listeners.
- **A requirement has no matching feature.** Some CLS requirements are met by
  procedure (for example, backup retention or account reviews) or by another
  system (such as the authentication server or a SIEM). Record how the
  requirement is met, not just which feature covers it.

## Security and Best Practices

- Keep FortiAnalyzer on a vendor-supported release and track the version
  column when planning upgrades.
- Protect the logs as evidence: restrict administrator profiles, enable log
  checksums, forward logs to a second system, and back up the log repository.
- Use remote or PKI authentication for administrators, with FIPS-capable
  cryptography for every management and log transport.
- Review this map each time Fortinet publishes a new FortiAnalyzer release
  train or DISA updates the Central Log Server SRG.

## References and Knowledge Checks

**References:**

- Fortinet, *FortiAnalyzer New Features Guide*, release trains 7.0, 7.2, 7.4,
  7.6, and 8.0 (docs.fortinet.com, FortiAnalyzer documentation).
- Fortinet, *FortiAnalyzer 8.0.0 CLI Reference* (docs.fortinet.com).
- DISA Central Log Server SRG V3R5 and Network Device Management SRG V5R5,
  from the October 2026 STIG Library Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products), and
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch map, built the same way).

**Knowledge checks:**

1. Why is a FortiAnalyzer assessed against the Central Log Server SRG?
2. Where does the version data come from, given that FortiAnalyzer has no
   feature matrix?
3. Which core features protect logs from alteration and deletion?
4. Which commands make log forwarding meet the real-time, reliable, and
   encrypted transport requirements?
5. Which CLS requirements does FortiAnalyzer not meet exactly, and how do you
   handle them?
6. What applies to a feature marked "No direct requirement"?

## Summary and Completion Checklist

FortiAnalyzer has no STIG, so it is assessed against the Central Log Server
SRG, with the NDM SRG for a few management-plane items. This chapter maps
349 features to the release that introduced them, to the SRG requirement
each feature implements or must be configured to meet, and to the command or
GUI location that configures it: 53 core platform features, and all
296 features from the New Features Guides for FortiAnalyzer 7.0 through
8.0. Operational features with no direct requirement fall under the
requirement to disable non-essential capabilities when unused.

- [ ] Can find the release that introduced a FortiAnalyzer feature.
- [ ] Can map a FortiAnalyzer feature to its SRG requirement.
- [ ] Can find the command or GUI location that meets the requirement.
- [ ] Can scope an SRG-based FortiAnalyzer assessment from the map, including
  the requirements met by procedure.
