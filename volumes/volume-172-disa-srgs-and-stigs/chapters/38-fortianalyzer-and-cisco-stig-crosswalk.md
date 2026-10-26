# Chapter 38: FortiAnalyzer and Cisco STIG Crosswalk

## Learning Objectives

- Explain why this crosswalk is anchored on FortiAnalyzer's requirements
  rather than on a Cisco STIG, and why no Cisco product is a true
  counterpart to a central log server.
- State plainly that no Cisco STIG implements the Central Log Server SRG,
  and explain what Cisco SNA (Secure Network Analytics) is and is not.
- Match a FortiAnalyzer requirement to Cisco STIG rules by exact SRG ID, or
  by a shared base requirement number after reading both requirement texts.
- Use the Cisco rules on the log-source side to see what a FortiAnalyzer
  receives from Cisco devices, and what it must do with it.
- Tell the four alignment categories apart and record each one correctly.
- Recognize the SNA fix texts that do not match the current SNA
  documentation, and the SNA settings that cannot be combined.

## Theory and Architecture

**No Cisco STIG implements the Central Log Server SRG.** FortiAnalyzer has
no STIG of its own; [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md)
assesses it against the Central Log Server (CLS) SRG V3R5 and, for a few
management-plane items, the Network Device Management (NDM) SRG V5R5, and
maps its features to 65 requirements: 60 CLS and 5
NDM. Cisco publishes no central log server, and none of its 25 STIGs
([Chapter 31](31-cisco-products-stigs-and-srg-mapping.md)) cites a CLS
requirement: measured across every Cisco rule, 0 of the 60 CLS IDs
appear.

**Cisco SNA is the closest Cisco appliance with a STIG, but it is not a log
server.** Cisco Secure Network Analytics (SNA, formerly Stealthwatch) is,
in the words of the DISA overview, an agentless network detection and
response (NDR) solution: it collects flow telemetry from routers, switches,
and firewalls and analyzes behavior to detect threats. Its Fortinet
counterpart would be FortiNDR, whose logs FortiAnalyzer itself collects and
reports on (Chapter 12). The SNA STIG V1R1 has 31 rules (`CSNA-ND-`), all
for the management plane: SNA is assessed as a network device, not as a log
server. So this chapter compares management requirements and the
relationship between log sources and the log server, **not** log-server
functions such as retention, analysis, or reporting, which have no Cisco
STIG counterpart at all.

**Why the anchor is the Fortinet product.** Chapters 33 to 37 list every
rule of a Cisco STIG and find the comparable Fortinet setting. Here no
single Cisco STIG is comparable, so the table turns around: one row for each
of FortiAnalyzer's 65 requirements, with the Cisco rules that
implement the same requirement, SNA first because it is the nearest
appliance, and then every other Cisco STIG.

### Why this is a crosswalk, not a STIG comparison

A STIG is a vendor-specific implementation of one or more SRGs
([Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)).
A crosswalk keeps that distinction:

- **The Cisco rules are references, not requirements for FortiAnalyzer.**
  A FortiAnalyzer finding is recorded against the CLS or NDM requirement in
  the first column, on an SRG-based checklist, as Chapter 12 describes.
- **The SRG ID is the join key.** Two settings align because they implement
  the same requirement, not because they look alike.
- **The two sides cover different ground.** FortiAnalyzer's CLS
  requirements are about receiving, protecting, and analyzing other
  systems' logs. The Cisco STIGs are about each device's own management
  plane, and about **sending** logs. Where a Cisco STIG governs the sending
  side of a log-server requirement, the row lists those rules in their own
  column, so the table shows what FortiAnalyzer receives from Cisco
  devices.

### How the rows are matched

Each FortiAnalyzer requirement was matched in four steps:

1. **Exact SRG ID (NDM rows).** The 5 NDM requirements are matched to
   every Cisco rule that cites the same SRG ID. The rule ID, severity, SRG
   ID, and title come from the Cisco XCCDF files of the October 2026 STIG
   Library Compilation.
2. **Shared base requirement number (CLS rows), as a candidate only.** DISA
   builds the CLS and NDM requirements from the same base requirements, so
   a CLS ID and an NDM ID can share a base number: `SRG-APP-000065-AU-000240`
   and `SRG-APP-000065-NDM-000214` are both the three-failures lockout.
   Measured: 27 of the 60 CLS IDs share a base number
   with at least one Cisco rule. A shared number is **not** a match by
   itself, so both requirement texts were read (the CLS text from the CLS
   SRG V3R5 XCCDF, the NDM text from the NDM SRG V5R5 XCCDF).
   17 CLS requirements have a candidate whose text matches and
   are marked **Equivalent requirement**. For the other 10, every
   candidate was rejected, 67 candidate SRG IDs in all (one
   candidate per CLS requirement and Cisco SRG ID). Most rejections come
   from `SRG-APP-000516`, the catch-all "configuration settings" base
   number: seven CLS requirements (source host identity, TCP transport,
   attack notification, trouble tickets, account-action aggregation,
   severity levels, and trusted path) share it with nine unrelated NDM
   requirements (backups, certificates, authentication servers, log
   servers, and others). The other rejections:
   - `SRG-APP-000148-AU-002270` (uniquely identify and authenticate users)
     against `SRG-APP-000148-NDM-000346` (keep only one local account, the
     account of last resort). The NDM rule limits local accounts; it does
     not ask for unique identification.
   - `SRG-APP-000080-AU-000010` (protect received log data from alteration
     that breaks attribution) against `SRG-APP-000080-NDM-000220`
     (non-repudiation of the device's own administrator actions) and the
     retired `SRG-APP-000080-NDM-000345` (audit all administrator activity).
   - `SRG-APP-000095-AU-000050` (configure log retention by criticality,
     event type, or period) against `SRG-APP-000095-NDM-000225` (audit
     records show the type of event). The same NDM ID **is** accepted for
     `SRG-APP-000095-AU-000680`, whose text matches.
3. **Retired IDs.** Some Cisco rules cite NDM IDs that are not in NDM SRG
   V5R5. Two of them have a current replacement that shares a base number
   with a CLS requirement, and the texts match, so their rules are counted
   with that row: `SRG-APP-000373-NDM-000298` (redundant authoritative time
   sources; current `SRG-APP-000920-NDM-000320`, synchronize system clocks)
   and `SRG-APP-000516-NDM-000351` (supported release; current
   `SRG-APP-001035-NDM-000340`). The second is the only way
   `SRG-APP-001035-AU-000430` finds its Cisco rules, including SNA
   `CSNA-ND-000950`, so 1 Equivalent requirement row rests on
   a retired ID. IOS XR cites the catch-all `SRG-APP-000516-NDM-000317` for
   its log server rule (`CISC-ND-001450`) and its supported-release rule
   (`CISC-ND-001470`); the rows name them with a note.
4. **The log-source side (log-server rows).** For each log-server
   requirement, the Cisco rules that govern the sending side were selected
   by SRG ID and checked by title: the NDM rules to send logs to central log
   servers (two for most Cisco devices) and to off-load audit records; the
   ASA firewall rule to use TCP and the ASA firewall, IPS, VPN, and ISE NAC
   rules to queue records locally while the server is unreachable; the
   audit content rules (what, when, where, source, outcome); the time stamp
   and clock rules; the account action audit rules; and the ASA IPS rule
   that sends records at a set facility and severity. Rules already listed
   as the same or an equivalent requirement are not repeated.

Two cautions apply:

- **CCIs were not used to match requirements.** The catch-all CCI-000366
  links unrelated requirements; every match rests on the SRG ID and the
  requirement texts.
- **Base-number matching misses some topics.** `SRG-APP-000358-AU-000100`
  (off-load log records to a different system) has the same text as the
  NDM off-load requirement `SRG-APP-000515-NDM-000325`, and SNA
  `CSNA-ND-000770` (install updates within 30 days, `SRG-APP-000457`) has
  the same topic as `SRG-APP-000456-AU-000270`, but the base numbers
  differ, so the method does not join them. The rows say so, and the second
  table gives each SNA rule its nearest FortiAnalyzer requirement.

### Where the commands come from

- **FortiAnalyzer commands come from Chapter 12.** Each row reuses the
  command cell of the Chapter 12 features named in the setting column; the
  build fails if that cell is not the Chapter 12 command of a feature that
  Chapter 12 maps to the same requirement. One exception is marked:
  `SRG-APP-000345-AU-000400` (lock until an administrator releases the
  account) is not mapped to a feature in Chapter 12, but Chapter 12's
  notes name `admin-lockout-duration` for it, and the build checks that
  note. A script checked all 105 command blocks in both tables
  against the **FortiAnalyzer 8.0.0 CLI Reference**, as in Chapter 12: each
  `config` path must head a Syntax block or appear in the reference, each
  `set` option must be in that block, each literal value must be a
  documented value, and each `execute` command must match a documented
  command. It was tested with deliberately wrong commands (a misspelled
  lockout option, an option under the wrong path, an undocumented
  `must-contain` value, a nonexistent `config system syslogd` path, `execute
  certificate local create`, an `md4` NTP key type, a misspelled
  `login-max`, and `set status on` for FIPS) and caught all eight.
- **SNA settings start from the fix text and were checked against Cisco's
  SNA documentation**, read on cisco.com through the built-in browser: the
  **Cisco Secure Network Analytics Online Help 7.6.0** (the appliance
  configuration, user management, and update chapters), the **System
  Configuration Guide 7.5.3** (appliance console menus), the **SSL/TLS
  Certificates for Managed Appliances Guide 7.5.3**, and the **Update Guide
  7.6.1**. SNA is configured in its web GUI and appliance console, so each
  cell reads "GUI: path: settings" or "Console (SystemConfig, sysadmin):
  path: settings". **Appliance Configuration** in a path stands for
  *Configure > Global > Central Management*, the *Inventory* tab, the
  *(Ellipsis)* icon of the appliance, *Edit Appliance Configuration*; it
  is followed by the tab (*Appliance*, *Network Services*, or *General*)
  and the section. Quoted text is the documentation's field label. A
  script checked all 35 SNA path items: every path segment and
  every quoted label must appear in the saved excerpt of the page it cites.
  It was tested with the fix texts' labels that the documentation does not
  have (`Number of Unsuccessful Attempts and Duration of Lockout`, `Password
  Minimum Character Length`, `Minimum Number of Upper Case Letters in
  Password`, `SNMP Versions`, `IdP Type`, `Enable DODIN Notifications`,
  `AES256-GCM`, an unlabeled External Services "Enable", and an `Upload
  Update File` menu) and caught all nine.
- Read the command cells as in Chapters 12 and 34: each pair of backticks
  is one block, statements are separated by `;` to fit in a table cell (on
  the CLI, enter each on its own line), and values in `<ANGLE_BRACKETS>` are
  placeholders. Two FortiAnalyzer blocks joined by "and" belong to the two
  features in the setting column, in the same order.
- A dash (**—**) means there is no command, rule, or version for that cell;
  the setting column says why.

**SNA fix text corrections.** Several SNA fix texts do not match the SNA
documentation. The crosswalk uses the documented menus and labels:

- The fix texts start most paths at *SNA Dashboard >> Configure >> Central
  Management*. In the Online Help 7.6.0, the menu is *Configure > Global >
  Central Management* (and *Configure > Global > User Management*). The
  `CSNA-ND-001030` path skips *Edit Appliance Configuration*, and
  `CSNA-ND-000930` calls it *Edit Configuration*.
- `CSNA-ND-000120` names one field, "Number of Unsuccessful Attempts and
  Duration of Lockout". *Session Settings* has two fields, *Number of
  unsuccessful attempts* and *Duration of lockout* (minutes), and the Help
  says that the security lockout does not apply to the admin and sysadmin
  users.
- `CSNA-ND-000130` enters the banner in *Opening Message*; the field is
  *Security Label*, which takes up to 10,000 characters and no semicolons.
- The password policy labels differ: "Password Minimum Character Length"
  (`CSNA-ND-000380`) and "Minimum Number of Characters in Password"
  (`CSNA-ND-001000`) are *Password must be at least ... characters*;
  "Maximum Number of Characters in Password" is *Password must be at most
  ... characters*; "Minimum Number of Upper Case Letters in Password",
  "Lower Case Letters", "Minimum Numbers in Password", and "Minimum Numbers
  of Symbols in Password" (`CSNA-ND-000390` to `CSNA-ND-000420`) are
  *Password must contain a minimum of ... uppercase letters, lowercase
  letters, numbers,* and *symbols*.
- `CSNA-ND-000700` sets "SNMP Versions"; the field is *SNMP Version*. The
  Help lists *HMAC192_SHA256* and stronger authentication protocols and
  *CFB_AES_128* and stronger encryption protocols.
- `CSNA-ND-000350`, `CSNA-ND-000900`, and `CSNA-ND-000970` select an "IdP
  Type"; the field is *Identity Provider Type*, and Microsoft ADFS, Okta,
  Login.gov, and Microsoft Entra ID are supported.
- `CSNA-ND-000640` clicks "Enable DODIN Notifications"; the section is
  *DoDIN Notifications* with an *Enable* check box and a *To Email* field.
- `CSNA-ND-000540` says the backup encryption method is AES256-GCM. The
  Online Help says only that encrypted backup files have a gpg extension;
  confirm the algorithm with Cisco.
- `CSNA-ND-000330` unchecks "Enable" under *External Services*; the check
  box is *Enable Customer Success Metrics*.
- `CSNA-ND-000500` asks for an eight-hour absolute session limit through
  *Request User Re-Authentication for Administrator-Only Functions After*
  480. That field only forces re-authentication for administrator
  functions; the Help says every user session ends after 12 hours and that
  this cannot be changed, so SNA has no eight-hour absolute limit.
- **`CSNA-ND-000010` and `CSNA-ND-000500` conflict.** The Help says
  *Maximum number of concurrent sessions* and *Log Out User Due to
  Inactivity After* cannot be used at the same time; one must stay 0. An SNA
  can meet only one of the two rules; record the other as an open finding.
- `CSNA-ND-000900` adds several servers to one service. A TACACS+ service
  takes only one server, and FIPS mode (`CSNA-ND-000490`) disables TACACS
  and RADIUS authentication, which leaves LDAP or SSO on a FIPS appliance.
- `CSNA-ND-000710` enters an NTP key ID and value; the Online Help does not
  name the key algorithm, so confirm that it is cryptographically based.

### Where the version columns come from

- **FortiAnalyzer version** is the "Introduced (FortiAnalyzer)" entry of the
  Chapter 12 feature whose command is shown; `7.0.0 or earlier` marks a core
  platform feature. Where a row uses two features with different releases,
  the cell names both. Settings that come only from the 8.0.0 CLI Reference
  read *Not in the Chapter 12 feature map (FortiAnalyzer 8.0.0 CLI
  Reference)*.
- **SNA version.** SNA documentation has no command history. Each cell
  names the document and release in which the path and labels were
  verified, for example *Online Help 7.6.0 (no release history)*, and gives
  a first release only where the documentation states one: *7.5.3* for
  HTTP/2, which the System Configuration Guide 7.5.3 says that release
  supports, and *7.1.0 or later* for FIPS mode, which the Help gives as a
  prerequisite. Older releases may place a page elsewhere.
- The other Cisco STIGs have no version column here; their commands and
  versions are in Chapters 32 to 37.

### Prerequisites

A FortiAnalyzer setting often meets its requirement only if something else
is already in place. A **prerequisite** is anything that must exist or be
configured *before* a row's FortiAnalyzer setting can meet the requirement:
the log sources themselves, ADOMs, log storage sized for the retention
period, an external server (RADIUS, TACACS+, or LDAP, a SAML identity
provider, SMTP, an SNMP manager, NTP, a syslog server or SIEM, an SFTP
server), the DoD PKI, FortiToken Cloud, another FortiAnalyzer that receives
aggregated logs, console access for FIPS-CC mode, a FortiCare support
contract, or a license. Settings that the row's own command creates are not
listed again. The prerequisites cover **the FortiAnalyzer side only**; the
Cisco settings and the Cisco rules on the log-source side are not given
prerequisites here.

The 16 prerequisites are Chapter 12's, with the same IDs, wording, and
commands, so that the map and the crosswalk agree; the build script checks
them against the *FortiAnalyzer prerequisites* table of Chapter 12. Only the
16 of Chapter 12's 30 that a row here needs are listed, so the IDs
are not consecutive. They are listed once in *FortiAnalyzer
prerequisites*, and the crosswalk and unmatched-requirement tables name the
IDs each row needs in their **FortiAnalyzer prerequisites** column:

- **Crosswalk rows.** Each row's FortiAnalyzer setting is one or two
  Chapter 12 features, and the row takes those features' IDs from Chapter
  12 (64 rows; where the setting names two features, 24 rows,
  the column lists the IDs of both). No row differs from Chapter 12.
- **Unmatched requirements.** These rows are SNA rules, but their
  FortiAnalyzer setting column names the FortiAnalyzer setting that would
  meet the rule's requirement, so the column lists that setting's
  prerequisites. The 12 rows whose setting is a Chapter 12 feature
  take that feature's IDs. The 2 settings that are not in the
  Chapter 12 feature map, the per-administrator session limit and the local
  certificate request, need nothing beyond the FortiAnalyzer under Chapter
  12's rules.

A dash means the setting needs nothing beyond the FortiAnalyzer itself.
The rows with no FortiAnalyzer command (1 in the crosswalk and
3 in the unmatched-requirement table) always show a dash.

Fortinet publishes no feature matrix for FortiAnalyzer, so the
**licenses** come from the FortiAnalyzer New Features Guides, as in Chapter
12: the FortiCare support contract (P22) on the firmware upgrade rows, from
*Prevent FortiAnalyzers with an expired support contract from upgrading to
a major or minor firmware release* (7.4) and *FortiCare Elite or FortiCare
Premium required to download FortiGuard objects* (8.0), and the indicators
of compromise (IOC) license (P24) on the attack notification row, from
*DNS security report 7.0.3* (7.0). **Model support** is given only where a
document states it: log storage (P3) depends on the hardware model or, on
a FortiAnalyzer-VM, on its virtual disks and license (`execute lvm` exists
only on VM models), and FIPS-CC mode can be enabled only from the console
(P19). Check the License Information widget and the FortiAnalyzer
Administration Guide for your exact model and release before you plan on a
licensed feature.

During an assessment, check a row's prerequisites before its setting: a
correctly configured setting with a missing prerequisite (a syslog receiver
with no log sources sending to it, an alert email with no reachable SMTP
server, PKI administrator login without the DoD CA certificates and CRLs, a
firmware upgrade without a support contract) does not meet the requirement,
and the missing prerequisite is the finding.

### Alignment categories

Every row has one of four categories:

| Category | Meaning |
| --- | --- |
| Same requirement | At least one Cisco STIG rule cites the same SRG ID (NDM rows only). |
| Equivalent requirement | A Cisco rule cites an NDM ID with the same base requirement number, and the two requirement texts were read and match; or it cites a retired NDM ID whose current replacement does. |
| Log-source counterpart only | No Cisco STIG implements this log-server requirement, but Cisco rules govern the sending side, which the log-source column lists. |
| No Cisco STIG counterpart | No Cisco STIG rule implements the requirement or governs its sending side. |

## Design Considerations

- **Record FortiAnalyzer findings against SRG requirements.** Use the
  first column as the checklist for every FortiAnalyzer and keep the Cisco
  rule IDs as references; a FortiAnalyzer is never "compliant with
  `CSNA-ND-000120`".
- **Design the log path from both ends.** Most Cisco NDM rules require two log
  servers and the ASA firewall, IPS, VPN, and ISE NAC rules require local
  queuing while the server is unreachable; FortiAnalyzer must accept TCP
  syslog, preferably over TLS, alert when a device stops logging, and keep
  the source identity and time stamps. Plan the FortiAnalyzer receivers,
  the second log server or SIEM, and the Cisco logging settings together.
- **Use one time source.** The CLS SRG asks that the log server use the
  same NTP source as the devices it serves; the Cisco NDM rules ask for two
  authenticated time sources and UTC time stamps. Point FortiAnalyzer and
  every Cisco device at the same authenticated NTP servers.
- **Take the stricter value where the two differ.** SNA's password policy
  can require eight changed characters; FortiAnalyzer's `change-4-characters`
  requires only four, so meet `SRG-APP-000170-AU-002530` through remote
  authentication (Chapter 12). SNA's lockout exempts the admin and sysadmin
  users; FortiAnalyzer's applies to all administrators.
- **Do not expect SNA to be the log server.** SNA sends its own audit log
  to two syslog-over-TLS destinations (`CSNA-ND-000940`); a FortiAnalyzer
  can be one of them, which makes SNA one more log source.

## Implementation and Automation

### FortiAnalyzer prerequisites

What must be in place before the FortiAnalyzer settings in the crosswalk
can meet their requirements (see *Prerequisites*). The rows are Chapter
12's, unchanged, limited to the IDs this chapter's rows use. The commands
were verified with the same script as the crosswalk; GUI entries name the
pane, and entries that are not FortiAnalyzer settings are described in
words.

[Download the prerequisites as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/38-fortianalyzer-and-cisco-stig-crosswalk-prerequisites.csv) (16 rows).

| ID | Prerequisite | What it enables | How to put it in place | Source |
| --- | --- | --- | --- | --- |
| P1 | Log sources (FortiGates, other Fortinet devices, and syslog devices) set to send logs to the FortiAnalyzer, registered, and authorized | Log collection, per-device quotas, rate limits, integrity checks, and backups, no-logging detection, and the features built on one product's logs (for example FortiMail, FortiWeb, FortiDeceptor, FortiSandbox, FortiNDR, or FortiEDR logs) | On each device, send logs to the FortiAnalyzer's address; then authorize the device in GUI: Device Manager, and check it with `diagnose dvm device list` | FortiAnalyzer 8.0.0 CLI Reference, `config system admin setting` (`unreg_dev_opt`) and `diagnose dvm device list`; Chapter 12 rows *Device registration and authorization* and *Security Fabric authorization* |
| P2 | ADOMs enabled and created, with the devices and administrators assigned to them | Per-ADOM disk quotas, data policies, log rates, time zones, and administrator profiles, ADOM assignment of administrators, Fabric ADOMs, and EMS multitenancy | `config system global; set adom-status enable; end`, then create the ADOMs in the GUI and assign administrators with `config system admin user; edit <ADMIN>; set adom <ADOM>; end` | FortiAnalyzer 8.0.0 CLI Reference, "Administrative Domains" ("Configuring ADOMs": the feature must first be enabled, ADOMs created, and administrators assigned) and `config system global` (`adom-status`) |
| P3 | Log storage sized for the retention period: disks on a hardware unit, or virtual disks on a FortiAnalyzer-VM, within the license's storage limits | Disk quotas, the data policy (retention), and disk-full alerting with room to store logs for the required period | Hardware: a model with enough disk capacity. VM: add a virtual disk, then `execute lvm extend`, and check with `execute lvm info` | FortiAnalyzer 8.0.0 CLI Reference, `execute lvm` (FortiAnalyzer VM models only); FortiAnalyzer 7.2 New Features Guide, "FortiAnalyzer-VM has been added to the Flex-VM offering" (the license sets the daily storage and number of ADOMs) |
| P4 | Reachable RADIUS, TACACS+, or LDAP servers, each with a unique shared secret or bind account, and administrator accounts that use them | Remote administrator authentication, so the authentication server enforces password, inactivity, and lockout rules | An organization RADIUS, TACACS+, or LDAP service, then `config system admin radius; edit <RADIUS>; set server <RADIUS_IP>; set secret <SECRET>; end` and `config system admin user; edit <ADMIN>; set user_type radius; set radius_server <RADIUS>; end` | FortiAnalyzer 8.0.0 CLI Reference, `config system admin radius`, `config system admin tacacs`, `config system admin ldap`, and `config system admin user` (`user_type`, `radius_server`, `tacacs-plus-server`, `ldap-server`); Chapter 12 rows *RADIUS administrator authentication*, *TACACS+ administrator authentication*, and *LDAP administrator authentication* |
| P5 | A SAML identity provider with the FortiAnalyzer registered as a service provider, and the IdP certificate on the FortiAnalyzer | SAML single sign-on for administrators, with signed assertions and requests and SHA-256 or SHA-512 signatures | An organization SAML IdP, then `config system saml; set status enable; set role SP; set idp-entity-id <IDP_ENTITY_ID>; set idp-single-sign-on-url <IDP_SSO_URL>; set idp-cert <IDP_CERT>; end` | FortiAnalyzer 8.0.0 CLI Reference, `config system saml`; Chapter 12 rows *SAML SSO wildcard admin user to match all users on IdP server*, *SAML assertions and SAML requests can be now signed to better support third-party IdPs*, and *SAML SSO supports SHA-256 and SHA-512 for both IdP and SP* |
| P6 | PKI: the DoD CA certificates and CRLs on the FortiAnalyzer, a reachable CRL distribution point, and certificates from that PKI for administrators and log sources | PKI (certificate) administrator login, two-factor authentication (available only for PKI administrators), LDAPS server validation, and syslog client certificate authentication | `config system certificate ca; edit <DOD_CA>; set ca <CA_CERTIFICATE>; end` and `config system certificate crl; edit <DOD_CRL>; set http-url <CRL_URL>; end`, with certificates issued to the administrators and the syslog log sources | FortiAnalyzer 8.0.0 CLI Reference, `config system certificate ca`, `config system certificate crl`, `config system admin user` (`user_type pki-auth`, `ca`; `two-factor-auth` is available when a PKI administrator account is configured), and `config system log settings` (`client-cert-auth`); Chapter 12 rows *PKI (certificate) administrator authentication* and *CA certificates and CRLs* |
| P7 | FortiToken Cloud with a token for each administrator | Two-factor authentication for administrators (FortiToken Cloud email, mobile, or SMS) | FortiToken Cloud, then `config system admin user; edit <ADMIN>; set two-factor-auth ftc-ftm; end` | FortiAnalyzer 8.0.0 CLI Reference, `config system admin user` (`two-factor-auth`); Chapter 12 row *Two-factor authentication (FortiToken Cloud)* |
| P8 | A reachable SMTP server (with STARTTLS and an account if it requires authentication) | Alert email to the ISSO and administrators: disk-full, no-logging, and system alerts, and event handler and scheduled notifications | An organization mail server, then `config system mail; edit <SMTP>; set server <SMTP_IP>; set secure-option starttls; set auth enable; end` | FortiAnalyzer 8.0.0 CLI Reference, `config system mail` and `config system alert-event`; Chapter 12 row *Alert email (SMTP)* |
| P9 | SNMPv3 manager configured with the same user, authentication, and privacy settings | SNMPv3 queries and notifications with SHA-2 authentication and AES privacy | The organization network management system, then `config system snmp user; edit <USER>; set notify-hosts <NMS_IP>; set queries enable; end` | FortiAnalyzer 8.0.0 CLI Reference, `config system snmp user`; Chapter 12 row *SNMPv3* |
| P10 | Authoritative NTP servers and their authentication keys | Synchronized, authenticated time for the FortiAnalyzer's own records and for log receipt time stamps | Organization NTP servers, then `config system ntp; config ntpserver; edit 1; set server <NTP_IP>; set authentication enable; set key-type sha256; set key-id <ID>; set key <KEY>; end; end` | FortiAnalyzer 8.0.0 CLI Reference, `config system ntp`; Chapter 12 rows *NTP server* and *FortiAnalyzer supports NTPv4 with SHA-256 encryption* |
| P11 | A remote syslog server or SIEM that accepts reliable (TCP) syslog with TLS | Off-loading the FortiAnalyzer's own event logs, and forwarding collected logs in real time to a different system | An organization syslog server or SIEM, then `config system syslog; edit <SYSLOG>; set ip <SYSLOG_IP>; set reliable enable; set secure-connection enable; end` for the FortiAnalyzer's own logs, or `config system log-forward; edit 1; set mode forwarding; set server-addr <SIEM_IP>; end` for collected logs | FortiAnalyzer 8.0.0 CLI Reference, `config system syslog` and `config system log-forward`; Chapter 12 rows *Sending FortiAnalyzer event logs to a syslog server* and *Log forwarding to syslog, CEF, or another FortiAnalyzer* |
| P13 | Another FortiAnalyzer: the analyzer that receives aggregated logs, or the server that log fetching pulls from | Log aggregation from a collector to an analyzer, and log fetching between FortiAnalyzer units | On the analyzer, `config system log-forward-service; set accept-aggregation enable; end`; for log fetching, the other unit is the fetch server (`config system log-fetch server-setting`) | FortiAnalyzer 8.0.0 CLI Reference, `config system log-forward-service` (`accept-aggregation`), `config system log-fetch server-setting`, and `config system log-fetch client-profile`; Chapter 12 rows *Log aggregation (collector to analyzer)* and *Log fetching between FortiAnalyzer units* |
| P14 | An SFTP server and account for backups and firmware images | Log and configuration backups to another system, the backup before an upgrade, and loading firmware from the CLI | An organization SFTP server; the backup runs `execute backup all-settings sftp <SERVER_IP> <FILE> <USER> <PASSWORD>` | FortiAnalyzer 8.0.0 CLI Reference, `execute backup`, `execute restore image`, and `config system backup all-settings`; Chapter 12 rows *Log backup to another system*, *Configuration backup*, and *Firmware upgrade* |
| P19 | Console access to the FortiAnalyzer (serial console, or the hypervisor console of a VM) | Enabling FIPS-CC mode, which is available only from the console | A console connection, then `config system fips; set status enable; end` | FortiAnalyzer 8.0.0 CLI Reference, `config system fips` (the enable option is available only through the console); Chapter 12 row *FIPS-CC mode* |
| P22 | A valid FortiCare support contract: the Firmware & General Updates entitlement, and FortiCare Premium or Elite | Upgrades to a higher major or minor release, and object updates from FortiGuard (FortiGate metadata, Internet Service Database, GeoIP, safeguarding) | Purchase and register the contract in FortiCloud; check with `diagnose fmupdate dbcontract` and `diagnose license list` | FortiAnalyzer 7.4 New Features Guide, "Prevent FortiAnalyzers with an expired support contract from upgrading to a major or minor firmware release"; FortiAnalyzer 8.0 New Features Guide, "FortiCare Elite or FortiCare Premium required to download FortiGuard objects" |
| P24 | Indicators of compromise (IOC) service license | IOC detection (compromised hosts) and the charts that depend on it | Purchase and register the license; check with `diagnose license list` or GUI: Dashboards > Status > License Information | FortiAnalyzer 7.0 New Features Guide, "DNS security report 7.0.3" (without IOC, the charts show "No license for the Indicators of Compromise (IOC) service") |

### The crosswalk table

One row per FortiAnalyzer requirement in Chapter 12: 34 management
requirements (29 CLS, then 5 NDM), then 31
log-server function requirements. Severity is the SRG severity of the
requirement; the summary restates the requirement in plain language, and
the requirement title is in Chapter 12's requirement reference. The command
columns follow *Where the commands come from*, the version columns *Where
the version columns come from*, the matching *How the rows are matched*,
and the prerequisite IDs refer to *FortiAnalyzer prerequisites*.

[Download the crosswalk as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/38-fortianalyzer-and-cisco-stig-crosswalk-crosswalk.csv) (65 rows).

| Requirement | Severity | Requirement summary | FortiAnalyzer setting | FortiAnalyzer command | FortiAnalyzer version | FortiAnalyzer prerequisites | Cisco SNA rule | Cisco SNA command | SNA version | Same requirement in other Cisco STIGs | Cisco rules on the log-source side | Alignment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CLS `SRG-APP-000026-AU-000580` | CAT II | Audit the creation of accounts on the log server. | FortiAnalyzer event log (own audit records) | `config system locallog disk setting; set status enable; set severity information; end` | 7.0.0 or earlier | — | — | — | — | ASA `CASA-ND-000090`; IOS XE `CISC-ND-000090`; NX-OS `CISC-ND-000090`; ISE `CSCO-NM-000030`; ACI `CACI-ND-000024` | — | Equivalent requirement |
| CLS `SRG-APP-000033-AU-001610` | CAT I | Enforce approved authorizations (roles) for access to the log server and its data. | Administrator profiles (role-based access); Administrative domains (ADOMs) | `config system admin profile; edit <PROFILE>; set log-viewer read; set report-viewer read; set system-setting none; end` and `config system global; set adom-status enable; end` | 7.0.0 or earlier | — | `CSNA-ND-000100` (CAT I) | GUI: User Management > Create > Data Role: set "Read" or "Read & Write" per component; assign it in the user's "Role Settings", "Data Role". | Online Help 7.6.0 (no release history) | ACI `CACI-ND-000012` | — | Equivalent requirement |
| CLS `SRG-APP-000065-AU-000240` | CAT II | Limit logons to three consecutive failures in 15 minutes. | Administrator lockout | `config system global; set admin-lockout-threshold 3; set admin-lockout-duration <SECONDS>; end` | 7.0.0 or earlier | — | `CSNA-ND-000120` (CAT II) | GUI: Appliance Configuration > General > Session Settings: "Number of unsuccessful attempts" 3; "Duration of lockout" 15. Lockout does not apply to the admin and sysadmin users. | Online Help 7.6.0 (no release history) | IOS `CISC-ND-000150`; IOS XE `CISC-ND-000150`; IOS XR `CISC-ND-000150`; NX-OS `CISC-ND-000150`; ISE `CSCO-NM-000110`; ACI `CACI-ND-000004` | — | Equivalent requirement |
| CLS `SRG-APP-000068-AU-000035` | CAT III | Show the DoD Notice and Consent Banner before logon. | Pre-login banner | `config system global; set pre-login-banner enable; set pre-login-banner-message <DOD_BANNER>; end` | 7.0.0 or earlier | — | `CSNA-ND-000130` (CAT II) | GUI: Appliance Configuration > General > Opening Message: "Security Label": the DoD banner text. No semicolons; 10,000 characters maximum. | Online Help 7.6.0 (no release history) | ASA `CASA-ND-000160`; IOS `CISC-ND-000160`; IOS XE `CISC-ND-000160`; IOS XR `CISC-ND-000160`; NX-OS `CISC-ND-000160`; ISE `CSCO-NM-000120`; ACI `CACI-ND-000003` | — | Equivalent requirement |
| CLS `SRG-APP-000095-AU-000680` | CAT III | The log server's own audit records show what type of event occurred. | FortiAnalyzer event log (own audit records) | `config system locallog disk setting; set status enable; set severity information; end` | 7.0.0 or earlier | — | — | — | — | ASA `CASA-ND-000260` | — | Equivalent requirement |
| CLS `SRG-APP-000141-AU-000090` | CAT II | Disable non-essential capabilities. | Interface administrative access; Disable unused analytics modules | `config system interface; edit <PORT>; set allowaccess https ssh; end` and `config system global; set disable-module <MODULES>; end` | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000148-AU-002270` | CAT I | Uniquely identify and authenticate every user. | Individual administrator accounts; RADIUS administrator authentication | `config system admin user; edit <ADMIN>; set profileid <PROFILE>; set adom <ADOM>; end` and `config system admin radius; edit <RADIUS>; set server <IP>; set secret <SECRET>; set protocol tls; set message-authenticator require; end` | 7.0.0 or earlier | P2, P4 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000149-AU-002280` | CAT II | Use multifactor authentication for network access to privileged accounts. | PKI (certificate) administrator authentication; Two-factor authentication (FortiToken Cloud) | `config system admin user; edit <ADMIN>; set user_type pki-auth; set subject <CERT_SUBJECT>; set ca <CA_CERT>; end` and `config system global; set clt-cert-req enable; end` and `config system admin user; edit <ADMIN>; set two-factor-auth ftc-ftm; end` | 7.0.0 or earlier | P6, P7 | `CSNA-ND-000350` (CAT I) | GUI: User Management > Authentication and Authorization > Create > Authentication Service > SSO: "Identity Provider Type" (Microsoft ADFS is supported), with an IdP that enforces DoD PKI. The IdP performs the PKI logon; SAML request signing is not supported. | Online Help 7.6.0 (no release history) | — | — | Equivalent requirement |
| CLS `SRG-APP-000163-AU-002470` | CAT II | Disable accounts after 35 days of inactivity. | No setting in the FortiAnalyzer 8.0.0 CLI Reference; Chapter 12 meets it on the authentication server or by a documented account review | — | — | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000164-AU-002480` | CAT II | Require passwords of at least 15 characters. | Password policy | `config system password-policy; set status enable; set minimum-length 15; set must-contain upper-case-letter lower-case-letter number non-alphanumeric; set change-4-characters enable; set expire 180; end` | 7.0.0 or earlier | — | `CSNA-ND-000380` (CAT II) | GUI: Appliance Configuration > General > Password Policy: "Password must be at least" 15 characters. Default 16. | Online Help 7.6.0 (no release history) | ASA `CASA-ND-000490`; IOS `CISC-ND-000550`; IOS XE `CISC-ND-000550`; ISE `CSCO-NM-000400`; ACI `CACI-ND-000045` | — | Equivalent requirement |
| CLS `SRG-APP-000166-AU-002490` | CAT III | Require at least one uppercase character in passwords. | Password policy | `config system password-policy; set status enable; set minimum-length 15; set must-contain upper-case-letter lower-case-letter number non-alphanumeric; set change-4-characters enable; set expire 180; end` | 7.0.0 or earlier | — | `CSNA-ND-000390` (CAT II) | GUI: Appliance Configuration > General > Password Policy: "Password must contain a minimum of" 1 "uppercase letters". | Online Help 7.6.0 (no release history) | ASA `CASA-ND-000520`; IOS `CISC-ND-000570`; IOS XE `CISC-ND-000570`; NX-OS `CISC-ND-000570`; ISE `CSCO-NM-000410` | — | Equivalent requirement |
| CLS `SRG-APP-000170-AU-002530` | CAT III | Require at least eight changed characters when a password changes. | Password policy. `change-4-characters` requires only 4 (Chapter 12). | `config system password-policy; set status enable; set minimum-length 15; set must-contain upper-case-letter lower-case-letter number non-alphanumeric; set change-4-characters enable; set expire 180; end` | 7.0.0 or earlier | — | `CSNA-ND-000430` (CAT II) | GUI: Appliance Configuration > General > Password Policy: "Number of characters different from previous password" 8. | Online Help 7.6.0 (no release history) | ASA `CASA-ND-000580`; IOS `CISC-ND-000610`; IOS XE `CISC-ND-000610` | — | Equivalent requirement |
| CLS `SRG-APP-000174-AU-002570` | CAT III | Limit password lifetime to 180 days. | Password policy | `config system password-policy; set status enable; set minimum-length 15; set must-contain upper-case-letter lower-case-letter number non-alphanumeric; set change-4-characters enable; set expire 180; end` | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000175-AU-002630` | CAT I | Validate PKI certificates to a trust anchor, including revocation status. | PKI (certificate) administrator authentication; CA certificates and CRLs | `config system admin user; edit <ADMIN>; set user_type pki-auth; set subject <CERT_SUBJECT>; set ca <CA_CERT>; end` and `config system global; set clt-cert-req enable; end` and `config system certificate ca; edit <CA>; set ca <CERTIFICATE>; end` and `config system certificate crl; edit <CRL>; set http-url <CRL_URL>; end` | 7.0.0 or earlier | P6 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000295-AU-000190` | CAT II | End user sessions after organization-defined conditions. | Idle session timeout | `config system admin setting; set idle_timeout <MINUTES>; end` | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000345-AU-000400` | CAT II | Keep an account locked until an administrator releases it after three failures in 15 minutes. | Administrator lockout (Chapter 12 note: `admin-lockout-duration` unlocks after a set time; set a long duration and document the release procedure) | `config system global; set admin-lockout-threshold 3; set admin-lockout-duration <SECONDS>; end` | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000391-AU-002290` | CAT II | Accept the DoD CAC credential. | PKI (certificate) administrator authentication | `config system admin user; edit <ADMIN>; set user_type pki-auth; set subject <CERT_SUBJECT>; set ca <CA_CERT>; end` and `config system global; set clt-cert-req enable; end` | 7.0.0 or earlier | P6 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000427-AU-000040` | CAT II | Trust only DoD PKI certificate authorities for protected sessions. | PKI (certificate) administrator authentication | `config system admin user; edit <ADMIN>; set user_type pki-auth; set subject <CERT_SUBJECT>; set ca <CA_CERT>; end` and `config system global; set clt-cert-req enable; end` | 7.0.0 or earlier | P6 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000456-AU-000270` | CAT I | Install security-relevant updates within 30 days. | Firmware upgrade | `execute restore image sftp <IMAGE_PATH> <SERVER_IP> <USER> <PASSWORD>` (use a vendor-supported release) | 7.0.0 or earlier | P14, P22 | — (CSNA-ND-000770 covers the same topic under a different base requirement (SRG-APP-000457); see the second table.) | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000503-AU-000280` | CAT II | Audit successful and unsuccessful logons. | FortiAnalyzer event log (own audit records) | `config system locallog disk setting; set status enable; set severity information; end` | 7.0.0 or earlier | — | — | — | — | ASA `CASA-ND-001220`; IOS `CISC-ND-001260`; IOS XE `CISC-ND-001260`; NX-OS `CISC-ND-001260`; ISE `CSCO-NM-000170` | — | Equivalent requirement |
| CLS `SRG-APP-000514-AU-002890` | CAT I | Use FIPS-validated cryptography for signatures, hashes, and encryption. | FIPS-CC mode; HTTPS and SSH management encryption | `config system fips; set status enable; end` and `config system global; set global-ssl-protocol tlsv1.2; set ssl-low-encryption disable; set enc-algorithm high; end` | 7.0.0 or earlier | P19 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000516-AU-000410` | CAT II | Analysis and viewing functions meet DoD trusted path and access rules. | Trusted hosts for administrators; Local-in policies | `config system admin user; edit <ADMIN>; set trusthost1 <IP> <MASK>; end` and `config system local-in-policy; edit 1; set intf <PORT>; set src <IP> <MASK>; set dport 443; set action accept; end` | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000610-AU-000050` | CAT I | Use SHA-2 or stronger for digital signatures. | SAML SSO supports SHA-256 and SHA-512 for both IdP and SP | `config system saml; set digest-method sha256; set signature-algorithm rsa-sha256; set idp-digest-method sha256; set idp-signature-algorithm rsa-sha256; end` | 8.0.0 and later | P5 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000810-AU-000250` | CAT II | Install only software and firmware with a verified, approved signature. | Firmware upgrade | `execute restore image sftp <IMAGE_PATH> <SERVER_IP> <USER> <PASSWORD>` (use a vendor-supported release) | 7.0.0 or earlier | P14, P22 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000815-AU-000260` | CAT II | Authenticate users individually before access to shared accounts. | Individual administrator accounts | `config system admin user; edit <ADMIN>; set profileid <PROFILE>; set adom <ADOM>; end` | 7.0.0 or earlier | P2 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000910-AU-000390` | CAT II | Keep only approved trust anchors in certificate stores. | CA certificates and CRLs | `config system certificate ca; edit <CA>; set ca <CERTIFICATE>; end` and `config system certificate crl; edit <CRL>; set http-url <CRL_URL>; end` | 7.0.0 or earlier | P6 | `CSNA-ND-001030` (CAT II) | GUI: Appliance Configuration > General > Trust Store: "Delete" every certificate that is not an approved trust anchor. | Online Help 7.6.0 (no release history) | — | — | Equivalent requirement |
| CLS `SRG-APP-000915-AU-000400` | CAT II | Protect stored cryptographic keys. | Private data encryption | `config system global; set private-data-encryption enable; end` | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000920-AU-000410` | CAT II | Synchronize system clocks within and between systems. | NTP server; FortiAnalyzer supports NTPv4 with SHA-256 encryption | `config system ntp; set status enable; config ntpserver; edit 1; set server <NTP_IP>; set authentication enable; set key-type sha256; set key-id <ID>; set key <KEY>; end; end` and `config system ntp; config ntpserver; edit 1; set ntpv3 disable; set authentication enable; set key-type sha256; set key-id <ID>; set key <KEY>; end; end` | 7.0.0 or earlier (NTP server); 8.0.0 and later (FortiAnalyzer supports NTPv4 with SHA-256 encryption) | P10 | — | — | — | ASA `CASA-ND-000940`; IOS `CISC-ND-001030`; IOS XE `CISC-ND-001030`; IOS XR `CISC-ND-001030`; NX-OS `CISC-ND-001030`; ISE `CSCO-NM-000230`; ACI `CACI-ND-000056` (includes rules that cite `SRG-APP-000373-NDM-000298`, a retired NDM ID (redundant authoritative time sources), replaced by SRG-APP-000920-NDM-000320) | — | Equivalent requirement |
| CLS `SRG-APP-001035-AU-000430` | CAT I | Run a release the vendor supports. | Firmware upgrade | `execute restore image sftp <IMAGE_PATH> <SERVER_IP> <USER> <PASSWORD>` (use a vendor-supported release) | 7.0.0 or earlier | P14, P22 | `CSNA-ND-000950` (CAT I) | GUI: Central Management > Update Manager: upload the update file from Cisco Software Central; (Ellipsis) > "Install Update". | Online Help 7.6.0; Update Guide 7.6.1 (no release history) | ASA `CASA-ND-001420`; IOS `CISC-ND-001470`; IOS XE `CISC-ND-001470`; IOS XR `CISC-ND-001470`; NX-OS `CISC-ND-001470`; ISE `CSCO-NM-000280`; ACI `CACI-ND-000011` (includes rules that cite `SRG-APP-000516-NDM-000351`, a retired NDM ID (supported release), replaced by SRG-APP-001035-NDM-000340; IOS XR `CISC-ND-001470`, which cites the catch-all SRG-APP-000516-NDM-000317) | — | Equivalent requirement |
| NDM `SRG-APP-000395-NDM-000310` | CAT II | Authenticate SNMP messages with a FIPS-validated HMAC. | SNMPv3 | `config system snmp user; edit <USER>; set security-level auth-priv; set auth-proto sha256; set priv-proto aes256; end` | 7.0.0 or earlier | P9 | `CSNA-ND-000700` (CAT II) | GUI: Appliance Configuration > Network Services > SNMP Agent: "Enable"; "SNMP Version" 3; "Authentication Protocol" HMAC192_SHA256 or stronger; "Encryption Protocol" CFB_AES_128 or stronger. | Online Help 7.6.0 (no release history) | ASA `CASA-ND-001050`; ASA `CASA-ND-001070`; IOS `CISC-ND-001130`; IOS `CISC-ND-001140`; IOS XE `CISC-ND-001130`; IOS XE `CISC-ND-001140`; IOS XR `CISC-ND-001130`; IOS XR `CISC-ND-001140`; NX-OS `CISC-ND-001130`; NX-OS `CISC-ND-001140`; ISE `CSCO-NM-000380`; ACI `CACI-ND-000002` | — | Same requirement |
| NDM `SRG-APP-000395-NDM-000347` | CAT II | Authenticate NTP sources cryptographically. | NTP server; FortiAnalyzer supports NTPv4 with SHA-256 encryption | `config system ntp; set status enable; config ntpserver; edit 1; set server <NTP_IP>; set authentication enable; set key-type sha256; set key-id <ID>; set key <KEY>; end; end` and `config system ntp; config ntpserver; edit 1; set ntpv3 disable; set authentication enable; set key-type sha256; set key-id <ID>; set key <KEY>; end; end` | 7.0.0 or earlier (NTP server); 8.0.0 and later (FortiAnalyzer supports NTPv4 with SHA-256 encryption) | P10 | `CSNA-ND-000710` (CAT II) | GUI: Appliance Configuration > Network Services > NTP Server > (Ellipsis) > Authenticate Connection: key ID and key value; "Apply Authentication". The Online Help does not name the key algorithm; the appliance reboots. | Online Help 7.6.0 (no release history) | ASA `CASA-ND-001080`; IOS `CISC-ND-001150`; IOS XE `CISC-ND-001150`; IOS XR `CISC-ND-001150`; NX-OS `CISC-ND-001150`; ACI `CACI-ND-000008` | — | Same requirement |
| NDM `SRG-APP-000516-NDM-000336` | CAT I | Authenticate administrators through at least one authentication server (two for boundary devices). | RADIUS administrator authentication; TACACS+ administrator authentication | `config system admin radius; edit <RADIUS>; set server <IP>; set secret <SECRET>; set protocol tls; set message-authenticator require; end` and `config system admin tacacs; edit <TACACS>; set server <IP>; set key <KEY>; set authorization enable; end` | 7.0.0 or earlier | P4 | `CSNA-ND-000900` (CAT I) | GUI: User Management > Authentication and Authorization > Create > Authentication Service: RADIUS, TACACS+, LDAP, or SSO; "Add New" in "Servers" for each server. A TACACS+ service takes only one server; a RADIUS service takes several, but FIPS mode disables TACACS and RADIUS, which leaves LDAP or SSO. | Online Help 7.6.0 (no release history) | ASA `CASA-ND-001310`; IOS `CISC-ND-001370`; IOS XE `CISC-ND-001370`; IOS XR `CISC-ND-001370`; NX-OS `CISC-ND-001370`; ISE `CSCO-NM-000270`; ACI `CACI-ND-000009` | — | Same requirement |
| NDM `SRG-APP-000516-NDM-000340` | CAT II | Back up system-level information when changes occur. | Configuration backup | `config system backup all-settings; set status enable; set protocol sftp; set server <IP>; set user <USER>; set passwd <PASSWORD>; set crptpasswd <ENCRYPTION_PASSWORD>; end` | 7.0.0 or earlier | P14 | — | — | — | ASA `CASA-ND-001350`; IOS `CISC-ND-001410`; IOS XE `CISC-ND-001410`; IOS XR `CISC-ND-001410`; NX-OS `CISC-ND-001410` | — | Same requirement |
| NDM `SRG-APP-000516-NDM-000350` | CAT I | Send the device's own logs to at least one central log server (two for boundary devices). | Sending FortiAnalyzer event logs to a syslog server | `config system syslog; edit <SYSLOG>; set ip <SYSLOG_IP>; set reliable enable; set secure-connection enable; end` and `config system locallog syslogd setting; set status enable; set syslog-name <SYSLOG>; end` | 7.0.0 or earlier | P11 | `CSNA-ND-000940` (CAT I) | GUI: Appliance Configuration > Network Services > Audit Log Destination: "Add New": "Server Name or IP Address", "Destination Port" (6514), "Certificate Revocation"; add the syslog server's CA to the "Trust Store". Syslog over TLS; two servers at most. | Online Help 7.6.0 (no release history) | ASA `CASA-ND-001410`; IOS `CISC-ND-001450`; IOS XE `CISC-ND-001450`; IOS XR `CISC-ND-001450`; NX-OS `CISC-ND-001450`; ISE `CSCO-NM-000560`; ACI `CACI-ND-000016` (includes IOS XR `CISC-ND-001450`, which cites the catch-all SRG-APP-000516-NDM-000317) | — | Same requirement |
| CLS `SRG-APP-000080-AU-000010` | CAT II | Protect received log data from alteration that would break attribution. | Log file integrity (hash and authentication code). MD5-based; see Chapter 12. | `config system global; set log-checksum md5-auth; end` and `execute log-integrity <DEVICE> <VDOM> <LOG_FILE>` | 7.0.0 or earlier | P1 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000086-AU-000020` | CAT III | Aggregate log records from the devices and hosts in scope. | Log collection from Fortinet devices (OFTP); Syslog collection from third-party devices | `config system global; set oftp-ssl-protocol tlsv1.2; set enc-algorithm high; end` and `config system log settings; set syslog-over-tls-port 6514; set unencrypted-logging-tcp disable; set unencrypted-logging-udp disable; config client-cert-auth; set mode strict; end; end` | 7.0.0 or earlier | P1, P6 | — | — | — | — | ASA `CASA-ND-001410`; ASA IPS `CASA-IP-000110`; IOS `CISC-ND-001450`; IOS XE `CISC-ND-001450`; IOS XR `CISC-ND-001310`; IOS XR `CISC-ND-001450`; NX-OS `CISC-ND-001310`; NX-OS `CISC-ND-001450`; ISE `CSCO-NM-000210`; ISE `CSCO-NM-000560`; ISE NAC `CSCO-NC-000220`; ACI `CACI-ND-000016`; SNA `CSNA-ND-000940` | Log-source counterpart only |
| CLS `SRG-APP-000086-AU-000030` | CAT III | Keep log time stamps within one second, using the same NTP source as the devices. | NTP server | `config system ntp; set status enable; config ntpserver; edit 1; set server <NTP_IP>; set authentication enable; set key-type sha256; set key-id <ID>; set key <KEY>; end; end` | 7.0.0 or earlier | P10 | — | — | — | — | ASA `CASA-ND-000940`; ASA `CASA-ND-000970`; IOS `CISC-ND-001030`; IOS XE `CISC-ND-001030`; IOS XR `CISC-ND-001030`; IOS XR `CISC-ND-001040`; IOS XR `CISC-ND-001050`; NX-OS `CISC-ND-001030`; NX-OS `CISC-ND-001050`; ISE `CSCO-NM-000230`; ISE `CSCO-NM-000240`; ACI `CACI-ND-000001`; ACI `CACI-ND-000056` | Log-source counterpart only |
| CLS `SRG-APP-000086-AU-000390` | CAT II | Where several log servers exist, aggregate them to a central repository. | Log aggregation (collector to analyzer) | `config system global; set log-mode collector; end` and `config system log-forward; edit 1; set mode aggregation; set server-addr <ANALYZER_IP>; end` | 7.0.0 or earlier | P13 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000089-AU-000400` | CAT II | Keep the DoD-defined attributes of the records the devices send. | Support parsing and addition of third-party application logs to the SIEM DB | GUI: Log View (log parsers) | 7.4.0 and later | P1 | — | — | — | — | ASA `CASA-ND-000260`; ASA `CASA-ND-000270`; ASA `CASA-ND-000280`; ASA `CASA-ND-000290`; ASA `CASA-ND-000300`; ASA `CASA-ND-000320`; ASA FW `CASA-FW-000040`; ASA FW `CASA-FW-000050`; ASA IPS `CASA-IP-000040`; ASA IPS `CASA-IP-000050`; ASA IPS `CASA-IP-000060`; ASA IPS `CASA-IP-000070`; ASA IPS `CASA-IP-000080`; ASA VPN `CASA-VN-000010`; ASA VPN `CASA-VN-000020`; ASA VPN `CASA-VN-000500`; ASA VPN `CASA-VN-000510`; ASA VPN `CASA-VN-000520`; ASA VPN `CASA-VN-000530`; IOS `CISC-ND-000280`; IOS `CISC-ND-000290`; IOS XE `CISC-ND-000280`; IOS XE `CISC-ND-000290`; IOS XE `CISC-ND-000330`; IOS XR `CISC-ND-000280`; IOS XR `CISC-ND-000290`; NX-OS `CISC-ND-000290`; NX-OS `CISC-ND-000330`; ISE `CSCO-NM-000720` | Log-source counterpart only |
| CLS `SRG-APP-000090-AU-000070` | CAT III | Only the ISSM, or roles the ISSM appoints, select which events are retained. | Data policy (log retention by ADOM) | GUI: System Settings, ADOM data policy (Analytics and Archive retention) | 7.0.0 or earlier | P2, P3 | — | — | — | — | ISE `CSCO-NM-000300`; ACI `CACI-ND-000029` | Log-source counterpart only |
| CLS `SRG-APP-000095-AU-000050` | CAT III | Configure log retention by criticality, event type, or retention period. | Data policy (log retention by ADOM); Automatic deletion of logs, reports, and archives | GUI: System Settings, ADOM data policy (Analytics and Archive retention) and `config system auto-delete; config log-auto-deletion; set status enable; set retention months; set value <MONTHS>; end; end` | 7.0.0 or earlier | P2, P3 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000111-AU-000150` | CAT III | Analyze log records across multiple devices for review by authorized users. | Event correlation across devices; FortiView | GUI: Incidents & Events (Handlers, correlation rules) and GUI: FortiView | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000115-AU-000160` | CAT III | Filter log records on demand for events of interest. | Log View: search and filter | GUI: Log View | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000118-AU-000100` | CAT II | Protect stored log data from unauthorized reading. | Administrator profiles (role-based access); Data masking for administrators | `config system admin profile; edit <PROFILE>; set log-viewer read; set report-viewer read; set system-setting none; end` and `config system admin profile; edit <PROFILE>; set datamask enable; set datamask-fields <FIELDS>; end` | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000119-AU-000110` | CAT II | Protect stored log data from unauthorized modification. | Log file integrity (hash and authentication code); Administrator profiles (role-based access) | `config system global; set log-checksum md5-auth; end` and `execute log-integrity <DEVICE> <VDOM> <LOG_FILE>` and `config system admin profile; edit <PROFILE>; set log-viewer read; set report-viewer read; set system-setting none; end` | 7.0.0 or earlier | P1 | — | — | — | IOS `CISC-ND-000380`; IOS XE `CISC-ND-000380` | — | Equivalent requirement |
| CLS `SRG-APP-000120-AU-000120` | CAT II | Protect stored log data from unauthorized deletion. | Keep logs after a device is deleted; Administrator profiles (role-based access) | `config system log settings; set keep-dev-logs enable; end` and `config system admin profile; edit <PROFILE>; set log-viewer read; set report-viewer read; set system-setting none; end` | 7.0.0 or earlier | — | — | — | — | IOS `CISC-ND-000390`; IOS XE `CISC-ND-000390` | — | Equivalent requirement |
| CLS `SRG-APP-000121-AU-000130` | CAT II | Protect the log analysis tools from unauthorized access. | Administrator profiles (role-based access) | `config system admin profile; edit <PROFILE>; set log-viewer read; set report-viewer read; set system-setting none; end` | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000125-AU-000300` | CAT III | Back up the log repository at least weekly to another system. | Log backup to another system | `execute backup logs <DEVICE> sftp <SERVER_IP> <USER> <PASSWORD> <DIRECTORY>` | 7.0.0 or earlier | P1, P14 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000358-AU-000100` | CAT II | Off-load log records to a different system or media. | Log forwarding to syslog, CEF, or another FortiAnalyzer; Log backup to another system | `config system log-forward; edit 1; set mode forwarding; set fwd-server-type syslog; set server-addr <SIEM_IP>; set fwd-reliable enable; set fwd-secure enable; set fwd-max-delay realtime; end` and `execute backup logs <DEVICE> sftp <SERVER_IP> <USER> <PASSWORD> <DIRECTORY>` | 7.0.0 or earlier | P1, P11, P14 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000359-AU-000120` | CAT III | Alert the SA and ISSO when log storage reaches 75 percent. | Disk-full alerting; Alert email (SMTP) | `config system locallog setting; set log-interval-disk-full <MINUTES>; end` and `config system alert-event; edit <ALERT>; config alert-destination; edit 1; set type mail; set to <ISSO_EMAIL>; end; end` and `config system mail; edit <ID>; set server <SMTP_IP>; set secure-option starttls; set auth enable; end` | 7.0.0 or earlier | P3, P8 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000360-AU-000130` | CAT III | Alert the SA and ISSO in real time on audit failures, such as devices that stop sending logs. | No-logging detection for devices; Alert email (SMTP) | `config system locallog setting; set no-log-detection-threshold <MINUTES>; set log-interval-dev-no-logging <MINUTES>; end` and `config system mail; edit <ID>; set server <SMTP_IP>; set secure-option starttls; set auth enable; end` | 7.0.0 or earlier | P1, P8 | `CSNA-ND-000640` (CAT II) | GUI: Appliance Configuration > General > SMTP Configuration: "SMTP Server", "Port", "From Email", "Encryption Type" SMTPS or STARTTLS. General > DoDIN Notifications: "Enable"; "To Email". DoDIN notifications include syslog failures and AIDE detections. | Online Help 7.6.0 (no release history) | ASA `CASA-ND-000930`; IOS `CISC-ND-001000`; IOS XE `CISC-ND-001000`; IOS XR `CISC-ND-001000`; NX-OS `CISC-ND-001000`; ISE `CSCO-NM-000220` | ASA FW `CASA-FW-000090`; ASA IPS `CASA-IP-000130`; ASA VPN `CASA-VN-000080`; ISE NAC `CSCO-NC-000220`; ISE NAC `CSCO-NC-000240` | Equivalent requirement |
| CLS `SRG-APP-000374-AU-000290` | CAT III | Time-stamp records on receipt in a form that maps to UTC. | Log receipt time stamps | See the NTP server row | 7.0.0 or earlier | P10 | — | — | — | IOS XR `CISC-ND-001050`; NX-OS `CISC-ND-001050`; ISE `CSCO-NM-000240`; ACI `CACI-ND-000001` | ASA `CASA-ND-000940`; ASA `CASA-ND-000970`; IOS `CISC-ND-001030`; IOS XE `CISC-ND-001030`; IOS XR `CISC-ND-001030`; IOS XR `CISC-ND-001040`; NX-OS `CISC-ND-001030`; ISE `CSCO-NM-000230`; ACI `CACI-ND-000056` | Equivalent requirement |
| CLS `SRG-APP-000439-AU-004310` | CAT I | Protect the confidentiality and integrity of transmitted information, including logs. | Syslog collection from third-party devices; HTTPS and SSH management encryption | `config system log settings; set syslog-over-tls-port 6514; set unencrypted-logging-tcp disable; set unencrypted-logging-udp disable; config client-cert-auth; set mode strict; end; end` and `config system global; set global-ssl-protocol tlsv1.2; set ssl-low-encryption disable; set enc-algorithm high; end` | 7.0.0 or earlier | P1, P6 | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000515-AU-000110` | CAT III | Off-load records in real time (interconnected systems) or weekly (standalone). | Log forwarding to syslog, CEF, or another FortiAnalyzer | `config system log-forward; edit 1; set mode forwarding; set fwd-server-type syslog; set server-addr <SIEM_IP>; set fwd-reliable enable; set fwd-secure enable; set fwd-max-delay realtime; end` | 7.0.0 or earlier | P11 | — | — | — | IOS XR `CISC-ND-001310`; NX-OS `CISC-ND-001310`; ISE `CSCO-NM-000210` | ASA `CASA-ND-001410`; ASA IPS `CASA-IP-000110`; IOS `CISC-ND-001450`; IOS XE `CISC-ND-001450`; IOS XR `CISC-ND-001450`; NX-OS `CISC-ND-001450`; ISE `CSCO-NM-000560`; ISE NAC `CSCO-NC-000220`; ACI `CACI-ND-000016`; SNA `CSNA-ND-000940` | Equivalent requirement |
| CLS `SRG-APP-000516-AU-000330` | CAT II | Keep the identity of the original source host in each record. | Log collection from Fortinet devices (OFTP); Device registration and authorization | `config system global; set oftp-ssl-protocol tlsv1.2; set enc-algorithm high; end` and `config system admin setting; set unreg_dev_opt add_no_service; end` | 7.0.0 or earlier | P1 | — | — | — | — | ASA `CASA-ND-000280`; ASA `CASA-ND-000290`; ASA IPS `CASA-IP-000060`; ASA IPS `CASA-IP-000070`; ASA VPN `CASA-VN-000510`; ASA VPN `CASA-VN-000520`; IOS `CISC-ND-000290`; IOS XE `CISC-ND-000290`; IOS XR `CISC-ND-000290`; NX-OS `CISC-ND-000290` | Log-source counterpart only |
| CLS `SRG-APP-000516-AU-000340` | CAT II | Use TCP to receive and transmit log records. | Syslog collection from third-party devices; Log forwarding to syslog, CEF, or another FortiAnalyzer | `config system log settings; set syslog-over-tls-port 6514; set unencrypted-logging-tcp disable; set unencrypted-logging-udp disable; config client-cert-auth; set mode strict; end; end` and `config system log-forward; edit 1; set mode forwarding; set fwd-server-type syslog; set server-addr <SIEM_IP>; set fwd-reliable enable; set fwd-secure enable; set fwd-max-delay realtime; end` | 7.0.0 or earlier | P1, P6, P11 | — | — | — | — | ASA FW `CASA-FW-000100` | Log-source counterpart only |
| CLS `SRG-APP-000516-AU-000350` | CAT II | Notify the SA and ISSO when an attack is seen on multiple devices. | Event handlers and alerts; Indicators of compromise (IOC) | GUI: Incidents & Events (Handlers); `config system alert-event` for system alerts and `config system log ioc; set status enable; set notification enable; end` | 7.0.0 or earlier | P8, P24 | — | — | — | — | ASA FW `CASA-FW-000200`; ASA IPS `CASA-IP-000110` | Log-source counterpart only |
| CLS `SRG-APP-000516-AU-000360` | CAT II | Create trouble tickets automatically for defined threats, within seconds. | Incidents | GUI: Incidents & Events (Incidents) | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000516-AU-000370` | CAT II | Aggregate events that show account actions on the devices in scope. | Event correlation across devices | GUI: Incidents & Events (Handlers, correlation rules) | 7.0.0 or earlier | — | — | — | — | — | ASA `CASA-ND-000090`; ASA `CASA-ND-000100`; ASA `CASA-ND-000110`; ASA `CASA-ND-000120`; IOS XE `CISC-ND-000090`; IOS XE `CISC-ND-000100`; IOS XE `CISC-ND-000110`; IOS XE `CISC-ND-000120`; IOS XE `CISC-ND-000880`; NX-OS `CISC-ND-000090`; NX-OS `CISC-ND-000100`; NX-OS `CISC-ND-000110`; NX-OS `CISC-ND-000120`; NX-OS `CISC-ND-000880`; ISE `CSCO-NM-000030`; ISE `CSCO-NM-000040`; ISE `CSCO-NM-000050`; ISE `CSCO-NM-000060`; ISE `CSCO-NM-000070`; ACI `CACI-ND-000024` | Log-source counterpart only |
| CLS `SRG-APP-000516-AU-000380` | CAT II | Configure the defined severity of each event the devices send. | Event handlers and alerts | GUI: Incidents & Events (Handlers); `config system alert-event` for system alerts | 7.0.0 or earlier | P8 | — | — | — | — | ASA IPS `CASA-IP-000120` | Log-source counterpart only |
| CLS `SRG-APP-000745-AU-000120` | CAT II | Review and analyze audit records from many components centrally. | FortiView | GUI: FortiView | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000750-AU-000130` | CAT II | Provide audit reduction for on-demand review. | SQL database for analytics | `config system sql; set status local; end` | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000770-AU-000170` | CAT II | Generate reports on demand. | Reports and report templates | GUI: Reports | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000775-AU-000180` | CAT II | Generate reports for after-the-fact incident investigations. | Reports and report templates; Incidents | GUI: Reports and GUI: Incidents & Events (Incidents) | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |
| CLS `SRG-APP-000790-AU-000210` | CAT II | Process, sort, and search records by defined audit fields. | Log View: search and filter | GUI: Log View | 7.0.0 or earlier | — | — | — | — | — | — | No Cisco STIG counterpart |

### Cisco SNA requirements with no FortiAnalyzer requirement

The 17 SNA rules below match none of FortiAnalyzer's
65 requirements by SRG ID or by an accepted base requirement number;
the other 14 SNA rules are in the crosswalk table. Most are NDM
requirements that the CLS SRG does not repeat (lowercase, number, and
special character rules, concurrent sessions, idle timeout, FIPS
authentication, encryption at rest, file integrity, HTTP/2, and
certificates). The nearest FortiAnalyzer requirement is a topic match only,
not an alignment. The FortiAnalyzer setting is the Chapter 12 feature that
would meet the SNA rule's requirement, or a setting from the 8.0.0 CLI
Reference, verified as above; where none exists the row says so. The
prerequisite IDs are those of the Chapter 12 features shown (see
*FortiAnalyzer prerequisites*).

[Download the unmatched requirements as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/38-fortianalyzer-and-cisco-stig-crosswalk-unmatched.csv) (17 rows).

| Cisco SNA rule | Severity | SRG ID | SNA requirement | Cisco SNA command | SNA version | Nearest FortiAnalyzer requirement | FortiAnalyzer setting | FortiAnalyzer command | FortiAnalyzer version | FortiAnalyzer prerequisites |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CSNA-ND-000010` | CAT II | `SRG-APP-000001-NDM-000200` | The Cisco SNA appliance must be configured to limit the number of concurrent sessions to an organization-defined number for each administrator account. | GUI: Appliance Configuration > General > Session Settings: "Maximum number of concurrent sessions" `<N>`. Cannot be combined with "Log Out User Due to Inactivity After" (CSNA-ND-000500); one of the two must stay 0. | Online Help 7.6.0 (no release history) | — | Per-administrator session limit (not in the Chapter 12 map) | `config system admin user; edit <ADMIN>; set login-max <N>; end` | Not in the Chapter 12 feature map (FortiAnalyzer 8.0.0 CLI Reference) | — |
| `CSNA-ND-000110` | CAT II | `SRG-APP-000038-NDM-000213` | The Cisco SNA appliance must be configured to enforce approved authorizations for controlling the flow of management information within the network device based on information flow control policies. | Console (SystemConfig, sysadmin): Network > Trusted Hosts: list only required hosts, including the other SNA appliances. Cisco asks you to contact Cisco Support before you change the list. | System Configuration Guide 7.5.3 (no release history) | `SRG-APP-000516-AU-000410` | Trusted hosts for administrators; Local-in policies | `config system admin user; edit <ADMIN>; set trusthost1 <IP> <MASK>; end` and `config system local-in-policy; edit 1; set intf <PORT>; set src <IP> <MASK>; set dport 443; set action accept; end` | 7.0.0 or earlier | — |
| `CSNA-ND-000330` | CAT I | `SRG-APP-000142-NDM-000245` | The Cisco SNA appliance must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services. | GUI: Appliance Configuration > Appliance > SSH: clear "Enable SSH". Network Services > SNMP Agent: clear "Enable" if unused. Network Services > Internet Proxy: clear "Enable" if unused. General > External Services: clear "Enable Customer Success Metrics". | Online Help 7.6.0 (no release history) | `SRG-APP-000141-AU-000090` | Interface administrative access; Disable unused analytics modules | `config system interface; edit <PORT>; set allowaccess https ssh; end` and `config system global; set disable-module <MODULES>; end` | 7.0.0 or earlier | — |
| `CSNA-ND-000340` | CAT II | `SRG-APP-000148-NDM-000346` | The Cisco SNA appliance must be configured with only one local account to be used as the account of last resort if the authentication server is unavailable. | GUI: User Management > Users > (Ellipsis) > Edit: keep "local" only for the admin account; "Delete" other local accounts. The built-in admin account cannot be deleted. | Online Help 7.6.0 (no release history) | `SRG-APP-000148-AU-002270` | Individual administrator accounts. FortiAnalyzer has no setting that limits local accounts; keep one local account of last resort by procedure. | `config system admin user; edit <ADMIN>; set profileid <PROFILE>; set adom <ADOM>; end` | 7.0.0 or earlier | P2 |
| `CSNA-ND-000400` | CAT II | `SRG-APP-000167-NDM-000255` | The Cisco SNA appliance must be configured to enforce password complexity by requiring that at least one lowercase character be used. | GUI: Appliance Configuration > General > Password Policy: "Password must contain a minimum of" 1 "lowercase letters". | Online Help 7.6.0 (no release history) | `SRG-APP-000166-AU-002490` | Password policy. `must-contain lower-case-letter`; the CLS SRG asks only for an uppercase character. | `config system password-policy; set status enable; set minimum-length 15; set must-contain upper-case-letter lower-case-letter number non-alphanumeric; set change-4-characters enable; set expire 180; end` | 7.0.0 or earlier | — |
| `CSNA-ND-000410` | CAT II | `SRG-APP-000168-NDM-000256` | The Cisco SNA appliance must be configured to enforce password complexity by requiring that at least one numeric character be used. | GUI: Appliance Configuration > General > Password Policy: "Password must contain a minimum of" 1 "numbers". | Online Help 7.6.0 (no release history) | `SRG-APP-000166-AU-002490` | Password policy. `must-contain number`; the CLS SRG asks only for an uppercase character. | `config system password-policy; set status enable; set minimum-length 15; set must-contain upper-case-letter lower-case-letter number non-alphanumeric; set change-4-characters enable; set expire 180; end` | 7.0.0 or earlier | — |
| `CSNA-ND-000420` | CAT II | `SRG-APP-000169-NDM-000257` | The Cisco SNA appliance must be configured to enforce password complexity by requiring that at least one special character be used. | GUI: Appliance Configuration > General > Password Policy: "Password must contain a minimum of" 1 "symbols". | Online Help 7.6.0 (no release history) | `SRG-APP-000166-AU-002490` | Password policy. `must-contain non-alphanumeric`; the CLS SRG asks only for an uppercase character. | `config system password-policy; set status enable; set minimum-length 15; set must-contain upper-case-letter lower-case-letter number non-alphanumeric; set change-4-characters enable; set expire 180; end` | 7.0.0 or earlier | — |
| `CSNA-ND-000490` | CAT I | `SRG-APP-000179-NDM-000265` | The Cisco SNA appliance must use FIPS 140-3-approved algorithms for authentication to a cryptographic module. | GUI: Appliance Configuration > General > Compliance Mode: "Enable FIPS Encryption Libraries" (and the Common Criteria Encryption Libraries as the CC guide directs). Reboots the appliance; TACACS, RADIUS authentication, and External Services are then unavailable. | 7.1.0 or later (prerequisite in Online Help 7.6.0) | `SRG-APP-000514-AU-002890` | FIPS-CC mode | `config system fips; set status enable; end` | 7.0.0 or earlier | P19 |
| `CSNA-ND-000500` | CAT I | `SRG-APP-000190-NDM-000267` | The Cisco SNA appliance must be configured to terminate sessions after five minutes of inactivity and set an absolute session timeout value of eight hours or less for admin sessions, except to fulfill documented and validated mission requirements. | GUI: Appliance Configuration > General > Protected Sessions Time-Out: "Log Out User Due to Inactivity After" 5; "Request User Re-Authentication for Administrator-Only Functions After" 480. Every session ends after 12 hours (fixed); the 480-minute value only forces re-authentication for administrator functions. Cannot be combined with a concurrent-session limit (CSNA-ND-000010). | Online Help 7.6.0 (no release history) | `SRG-APP-000295-AU-000190` | Idle session timeout. Idle timeout only; the 8.0.0 CLI Reference has no absolute session limit. | `config system admin setting; set idle_timeout <MINUTES>; end` | 7.0.0 or earlier | — |
| `CSNA-ND-000540` | CAT II | `SRG-APP-000231-NDM-000271` | The Cisco SNA appliance must be configured to encrypt information at rest using a DoW-accepted algorithm to protect the confidentiality and integrity of the information. | GUI: Appliance Configuration > General > Backup Configuration Encryption: "Enable Encryption"; "Backup Configuration Password". Encrypted backups have a gpg extension; the Online Help does not name the algorithm. | Online Help 7.6.0 (no release history) | — | Configuration backup; Private data encryption | `config system backup all-settings; set status enable; set protocol sftp; set server <IP>; set user <USER>; set passwd <PASSWORD>; set crptpasswd <ENCRYPTION_PASSWORD>; end` and `config system global; set private-data-encryption enable; end` | 7.0.0 or earlier | P14 |
| `CSNA-ND-000770` | CAT II | `SRG-APP-000457-NDM-000352` | The Cisco SNA appliance must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). | GUI: Central Management > Update Manager: upload the update file from Cisco Software Central; (Ellipsis) > "Install Update". | Online Help 7.6.0; Update Guide 7.6.1 (no release history) | `SRG-APP-000456-AU-000270` | Firmware upgrade. Same topic as CLS SRG-APP-000456-AU-000270 under a different base requirement. | `execute restore image sftp <IMAGE_PATH> <SERVER_IP> <USER> <PASSWORD>` (use a vendor-supported release) | 7.0.0 or earlier | P14, P22 |
| `CSNA-ND-000820` | CAT II | `SRG-APP-000504-NDM-000321` | The Cisco SNA appliance must generate audit records for modifications of critical files on the system. | GUI: Appliance Configuration > Appliance > Advanced Intrusion Detection Environment: "Enable AIDE". | Online Help 7.6.0 (no release history) | — | No file integrity monitoring setting in the FortiAnalyzer 8.0.0 CLI Reference | — | — | — |
| `CSNA-ND-000870` | CAT II | `SRG-APP-000516-NDM-000317` | The Cisco SNA appliance must be configured to use HTTP/2 at a minimum. | Console (SystemConfig, sysadmin): Network > HTTP Version: Yes. The appliance then rejects HTTP/1.1; do not enable it on a Manager used with the Desktop Client or Firepower Management Center. | 7.5.3 (System Configuration Guide 7.5.3) | — | No HTTP version setting in the FortiAnalyzer 8.0.0 CLI Reference | — | — | — |
| `CSNA-ND-000930` | CAT II | `SRG-APP-000516-NDM-000344` | The Cisco SNA appliance must be configured to obtain its public key certificates from an appropriate certificate policy through an approved service provider. | GUI: Appliance Configuration > Appliance > SSL/TLS Appliance Identity: "Update Identity", generate a CSR with "RSA Key Length" 4096 or 8192 (2048 not recommended), "Download CSR", submit to a DoD CA, "Replace Identity". | SSL/TLS Certificates Guide 7.5.3 (no release history) | — | Local certificate request (not in the Chapter 12 map). The 8.0.0 CLI Reference lists key sizes up to 2048 bits; install the signed certificate with `config system certificate local`. | `execute certificate local generate <CERT_NAME> <SUBJECT> 2048` | Not in the Chapter 12 feature map (FortiAnalyzer 8.0.0 CLI Reference) | — |
| `CSNA-ND-000970` | CAT II | `SRG-APP-000820-NDM-000170` | The Cisco SNA appliance must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. | GUI: User Management > Authentication and Authorization > Create > Authentication Service > SSO: "Identity Provider Type", with an IdP that enforces multifactor authentication. | Online Help 7.6.0 (no release history) | `SRG-APP-000149-AU-002280` | Two-factor authentication (FortiToken Cloud); PKI (certificate) administrator authentication | `config system admin user; edit <ADMIN>; set two-factor-auth ftc-ftm; end` and `config system admin user; edit <ADMIN>; set user_type pki-auth; set subject <CERT_SUBJECT>; set ca <CA_CERT>; end` and `config system global; set clt-cert-req enable; end` | 7.0.0 or earlier | P6, P7 |
| `CSNA-ND-001000` | CAT II | `SRG-APP-000860-NDM-000250` | The Cisco SNA appliance must be configured to allow user selection of long passwords and passphrases, including spaces and all printable characters for password-based authentication. | GUI: Appliance Configuration > General > Password Policy: "Password must be at most" 32 or more (default 256); "Password must be at least" 15. | Online Help 7.6.0 (no release history) | — | No setting; administrator passwords take up to 128 characters (8.0.0 CLI Reference, `config system admin user`) | — | — | — |
| `CSNA-ND-001010` | CAT II | `SRG-APP-000875-NDM-000280` | The Cisco SNA appliance must be configured to implement certificate revocation checking to support path discovery and validation for public key-based authentication. | GUI: Appliance Configuration > Network Services > Audit Log Destination: "Certificate Revocation" "Hard Fail". | Online Help 7.6.0 (no release history) | `SRG-APP-000175-AU-002630` | CA certificates and CRLs | `config system certificate ca; edit <CA>; set ca <CERTIFICATE>; end` and `config system certificate crl; edit <CRL>; set http-url <CRL_URL>; end` | 7.0.0 or earlier | P6 |

### Alignment summary

| Requirement group | Same requirement | Equivalent requirement | Log-source counterpart only | No Cisco STIG counterpart | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| Management requirements | 5 | 13 | 0 | 16 | 34 |
| Log-server function requirements | 0 | 5 | 9 | 17 | 31 |
| **Total** | **5** | **18** | **9** | **33** | **65** |

Of FortiAnalyzer's 65 requirements, 5 are implemented by
the same SRG ID in Cisco STIGs (all 5 NDM rows), 18 by an
equivalent requirement, 9 have Cisco rules only on the log-source
side, and 33 have no Cisco STIG counterpart. SNA rules appear in
14 rows. The main points:

- **Management requirements align well.** Lockout, banner, password
  length and complexity, MFA, role-based access, trust anchors, clock
  synchronization, supported releases, SNMP, NTP authentication,
  authentication servers, and sending the device's own logs all have Cisco
  counterparts, most with an SNA rule. The NDM requirements behind them are
  the same ones Chapters 33 to 37 compare.
- **Log-server functions have no Cisco counterpart.** Retention by
  criticality, backup of the log repository, the 75 percent storage alert,
  analysis across devices, on-demand filtering, audit reduction, reports,
  trouble tickets, and correlation are CLS requirements with no Cisco STIG
  rule. SNA analyzes flows, not logs, and its STIG has no such rules.
- **The log-source side is where Cisco and FortiAnalyzer meet.** Cisco
  rules require sending to central log servers, TCP and local queuing on the
  ASA, audit records with type, time, place, source, and outcome, account
  action audit records, and UTC time stamps. FortiAnalyzer's aggregation,
  TCP transport, source identity, attribute retention, account action
  correlation, severity handling, and no-logging alerting receive what those
  rules produce.
- **SNA limits.** SNA cannot combine a concurrent-session limit with an
  idle timeout, has no eight-hour absolute session limit, exempts admin and
  sysadmin from lockout, and loses TACACS and RADIUS in FIPS mode.
- **FortiAnalyzer limits.** As Chapter 12 records, FortiAnalyzer has no
  35-day inactivity disable, unlocks accounts after a set time, requires
  only four changed characters, and records MD5 log checksums.

### Collecting evidence

In a mixed estate, keep one checklist row per FortiAnalyzer requirement,
with the SRG ID and the alignment category from the table, and attach each
platform's evidence:

- **FortiAnalyzer:** the release and the settings in the FortiAnalyzer
  column, as Chapter 12 describes:

  FortiAnalyzer: `get system status`

  FortiAnalyzer: `show full-configuration`

  Add exports of the GUI-configured items: event handlers, report
  schedules, the ADOM data policy and disk quotas, and log forwarding.
- **Cisco SNA:** screenshots of the *Central Management* inventory (release
  and status), of each *Edit Appliance Configuration* section in the SNA
  command column, of *User Management*, and of the appliance console
  *Network* menu (Trusted Hosts and HTTP Version); add the *Audit Logs*
  search (*Support* > *Audit Logs*) that confirms NTP authentication.
- **Cisco log sources:** for every Cisco device that sends logs to the
  FortiAnalyzer, the logging configuration that meets the rules in the
  log-source column, collected as Chapters 33 to 37 describe, and the
  FortiAnalyzer *Device Manager* or Log View entry that shows its logs
  arriving.
- **For every requirement a platform cannot meet:** the open finding, its
  mitigation, and its approval, recorded against the SRG ID.

## Validation and Troubleshooting

- **A FortiAnalyzer requirement seems to have no row.** All 65
  requirements of Chapter 12 have a row; the build fails if one is missing.
  Search for the SRG ID.
- **An assessor asks for the Cisco rule that matches a CLS requirement.**
  Look at the alignment: a Same or Equivalent row names it; a
  Log-source counterpart row names the sending-side rules; otherwise there
  is none, because no Cisco STIG implements the CLS SRG.
- **An SNA field from a fix text is not there.** Check *SNA fix text
  corrections*: the labels and the menu changed. Search the Online Help for
  the section name (*Session Settings*, *Password Policy*, *Audit Log
  Destination*).
- **The SNA rejects an idle timeout.** If *Maximum number of concurrent
  sessions* is not 0, set it to 0 first; the two settings cannot be used at
  the same time.
- **Logs from a Cisco device stop arriving.** Check the Cisco side (TCP,
  queuing, the log server addresses) and the FortiAnalyzer side (receiving
  ports, encryption, device registration), and confirm that the no-logging
  alert fired.

## Security and Best Practices

- Treat the first column as the FortiAnalyzer checklist and record each
  finding against its SRG requirement, with the Cisco rule IDs as
  references.
- Send every Cisco device's logs to two log servers over TCP, with TLS
  where the device supports it, and alert on silence at the FortiAnalyzer.
- Use one authenticated NTP source for FortiAnalyzer, SNA, and every Cisco
  device, and keep UTC time stamps.
- On both FortiAnalyzer and SNA, authenticate administrators through
  directory or SSO services with DoD PKI, lock accounts after three
  failures, and enable FIPS mode.
- Review the crosswalk whenever DISA updates the CLS or NDM SRG or a Cisco
  STIG, or a new FortiAnalyzer or SNA release changes the settings.

## References and Knowledge Checks

**References:**

- DISA Central Log Server SRG V3R5, Network Device Management SRG V5R5, and
  the Cisco STIG packages (SNA V1R1 with its overview, ASA, IOS, IOS XE,
  IOS XR, NX-OS, ISE, and ACI), from the October 2026 STIG Library
  Compilation.
- Cisco, *Cisco Secure Network Analytics Online Help 7.6.0*, *Secure Network
  Analytics System Configuration Guide 7.5.3*, *SSL/TLS Certificates for
  Managed Appliances Guide 7.5.3*, and *Update Guide v7.5.x or v7.6.0 to
  v7.6.1*.
- Fortinet, *FortiAnalyzer 8.0.0 CLI Reference*.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (how STIGs are built from SRGs, and SRG-based assessment),
  [Chapter 07](07-network-device-stigs-management-routing-and-filtering.md)
  (network device STIGs by plane),
  [Chapter 12](12-fortianalyzer-feature-version-and-srg-map.md) (the
  FortiAnalyzer feature and SRG map, source of the rows, commands, and
  versions),
  [Chapter 31](31-cisco-products-stigs-and-srg-mapping.md) (the Cisco STIG
  packages, including SNA),
  [Chapter 33](33-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md),
  [Chapter 34](34-cisco-asa-and-fortigate-stig-crosswalk.md),
  [Chapter 35](35-cisco-ise-and-fortinac-stig-crosswalk.md),
  [Chapter 36](36-cisco-ios-xe-router-and-fortigate-stig-crosswalk.md), and
  [Chapter 37](37-cisco-nx-os-switch-and-fortiswitch-stig-crosswalk.md) (the
  other crosswalks, with the Cisco commands for the rules named here).

**Knowledge checks:**

1. Why does no Cisco STIG rule cite a Central Log Server requirement, and
   what kind of appliance is Cisco SNA?
2. Why is this crosswalk anchored on FortiAnalyzer's requirements rather
   than on a Cisco STIG?
3. `SRG-APP-000148-AU-002270` and `SRG-APP-000148-NDM-000346` share a base
   number. Why are they not the same requirement?
4. How does `SRG-APP-001035-AU-000430` find its Cisco rules, given that no
   Cisco rule cites `SRG-APP-001035`?
5. Which Cisco rules on the log-source side matter for
   `SRG-APP-000516-AU-000340` (TCP) and `SRG-APP-000360-AU-000130` (alert
   on loss of logs)?
6. Which two SNA rules cannot both be met, and why?
7. Name two FortiAnalyzer requirements with no Cisco STIG counterpart.

## Summary and Completion Checklist

No Cisco STIG implements the Central Log Server SRG, and Cisco SNA, the
nearest Cisco appliance with a STIG, is a flow analytics and NDR appliance
assessed only on its management plane. This chapter therefore lists all
65 FortiAnalyzer requirements from Chapter 12 and aligns each with
the Cisco SNA rule and the rules in every other Cisco STIG that implement
the same or an equivalent requirement, matched by exact SRG ID or by a
shared base number after reading both texts (67 base-number
candidates rejected), and with the Cisco rules that govern the sending side
of each log-server requirement: 5 same requirement, 18
equivalent, 9 log-source counterpart only, and 33 with no
Cisco counterpart. It also lists the 17 SNA rules with no
FortiAnalyzer requirement. Every FortiAnalyzer command was checked by script
against the FortiAnalyzer 8.0.0 CLI Reference and Chapter 12, and every SNA
path and label against Cisco's SNA documentation, with the fix text errors
corrected.

- [ ] Can explain why a FortiAnalyzer finding is recorded against a CLS or
  NDM requirement, with Cisco rules as references only.
- [ ] Can match a requirement by SRG ID or base number, and reject a base
  number match whose texts differ.
- [ ] Can use the log-source column to plan Cisco logging to a
  FortiAnalyzer.
- [ ] Can configure the SNA settings with the documented labels, and
  record the SNA rules it cannot meet together.
- [ ] Can name the log-server requirements that no Cisco STIG covers.
