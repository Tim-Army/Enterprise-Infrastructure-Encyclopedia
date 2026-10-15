# Chapter 35: Cisco ISE and FortiNAC STIG Crosswalk

## Learning Objectives

- Explain why the Cisco ISE STIGs can serve as a checklist for FortiNAC-F,
  which has no STIG, and why a FortiNAC finding is still recorded against an
  SRG requirement.
- Align a Cisco ISE STIG rule with the FortiNAC-F setting that implements
  the same SRG requirement or the same network access control behavior.
- Use the Cisco ISE NDM and NAC STIG rules as a working checklist for a
  FortiNAC-F deployment, and see where FortiNAC meets, partly meets, or
  cannot meet each rule.
- Tell the six alignment categories apart and record each one correctly.
- Find the FortiNAC requirements, above all the AAA Services requirements
  of its RADIUS server, that no ISE rule covers.
- Recognize the ISE fix texts that do not match current ISE software or
  documentation, and the corrected commands and GUI paths.

## Theory and Architecture

**Cisco ISE has a STIG package; FortiNAC has no STIG.** Cisco Identity
Services Engine (ISE) has two STIGs: the ISE NDM STIG V2R4 (51 rules,
`CSCO-NM-`) for the management plane, and the ISE NAC STIG V2R4
(30 rules, `CSCO-NC-`) for the network access control function,
which implements DoD Comply-to-Connect (C2C), 81 rules in all
([Chapter 31](31-cisco-products-stigs-and-srg-mapping.md)). FortiNAC-F has
**no DISA STIG**. As [Chapter 25](25-fortinac-feature-version-and-srg-map.md)
explains, it is assessed against the NDM SRG and the AAA Services SRG, and,
because DISA publishes no NAC SRG, Chapter 25 uses the Cisco ISE NAC STIG as
the expected pattern for the network access function and maps FortiNAC
features to its rule IDs.

That makes this crosswalk different from the others in the series. For the
51 NDM rules, the join key is the SRG ID, as in
[Chapter 33](33-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md).
For the 30 NAC rules, the join key is Chapter 25's own mapping:
Chapter 25 already maps FortiNAC features to 26 of the 30
ISE NAC rule IDs, so this chapter starts from that mapping and adds the ISE
side, the corrected ISE commands, and the rules Chapter 25 left unmapped.

**Scope of the ISE STIGs.** The DISA overview for the ISE package puts the
discovery, profiling, policy-based placement, and monitoring of endpoints in
scope, and leaves guest access and on-device AAA services out of scope of the
NAC STIG (the ISE CA, provisioning portal, identity services, AAA services,
and guest portal are named as out of scope; where they are used, other SRGs
apply). FortiNAC's local RADIUS server and guest accounts are in exactly
that excluded area, which is why the AAA requirements appear only in the
second table of this chapter.

### Why this is a crosswalk, not a STIG comparison

A STIG is a vendor-specific implementation of one or more SRGs
([Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)).
Its rules carry their own check and fix text, and an assessor records a
finding against the rule. A crosswalk keeps that distinction:

- **The ISE rule is a reference, not a requirement for FortiNAC.** A
  FortiNAC system is never "compliant with `CSCO-NC-000030`". Its finding is
  recorded against the SRG requirement the rule implements, on an SRG-based
  checklist, as Chapter 25 describes; for the NAC rules the requirement is
  the `SRG-NET-...-NAC-...` ID in the SRG ID column, which DISA uses in both
  NAC STIGs although it publishes no NAC SRG.
- **The SRG ID is the join key.** Two settings align because they implement
  the same requirement, not because they look alike. An ISE posture policy
  and a FortiNAC endpoint compliance policy align because both implement
  `SRG-NET-000512-NAC-002310`.
- **The two products cover different ground.** The ISE STIGs say nothing
  about RADIUS shared secrets, EAP types, guest account lifetimes, or
  certificate revocation for EAP-TLS, because AAA and guest services are out
  of their scope. Chapter 25 maps FortiNAC features to 82
  requirement IDs; 38 of them (18 NDM and 20 AAA) are
  cited by no ISE rule. The second table lists them.

### How the rules are aligned

Each ISE rule was aligned in four steps:

1. **Take the SRG ID the rule implements.** The rule ID, severity, SRG ID,
   and title come from the two ISE XCCDF files
   (`U_Cisco_ISE_Y26M07_STIG.zip`). The 81 rules cite 73
   distinct SRG IDs; several NAC rules share one ID (five cite
   `SRG-NET-000015-NAC-000020`).
2. **Look for the rule ID or the SRG ID in Chapter 25.** 52 of
   the 81 rules (26 NDM and 26 NAC)
   cite a rule ID or SRG ID that Chapter 25 maps to a FortiNAC feature. The
   NDM requirement text comes from the NDM SRG V5R5 XCCDF; the NAC
   requirement text is the ISE rule title, since there is no NAC SRG.
3. **For the rest, read the requirement and find the setting.** The
   FortiNAC setting was found in the **FortiNAC-F 7.6.0 CLI Reference
   Guide** and the **FortiNAC-F 7.6.0 Administration Guide**, the sources of
   Chapter 25. Where neither guide documents such a setting, the row says
   so.
4. **Judge how well the setting meets the requirement**, and assign one of
   the alignment categories below.

Two cautions apply to the alignment data:

- **CCIs were not used to match requirements.** Many SRG requirements share
  the catch-all CCI-000366 ("security configuration settings"), so a CCI
  match often links unrelated requirements. Every alignment rests on the SRG
  ID, the rule ID, or the requirement text.
- **Three ISE NDM rules cite SRG IDs that are not in NDM SRG V5R5.**
  `CSCO-NM-000230` cites `SRG-APP-000373-NDM-000298` (redundant time
  sources) and `CSCO-NM-000280` cites `SRG-APP-000516-NDM-000351` (supported
  release); the current requirements for the same topics are
  `SRG-APP-000920-NDM-000320` and `SRG-APP-001035-NDM-000340`, which
  Chapter 25 maps. `CSCO-NM-000300` cites `SRG-APP-000516-NDM-000334` (a
  locally developed list of auditable events); the nearest current
  requirement is `SRG-APP-000095-NDM-000225` (record what type of event
  occurred). Those rows are aligned with the current requirement, so the
  current IDs also appear in the second table, which lists IDs that no ISE
  rule cites.
- **Two rules cite an SRG ID that does not describe what they check.**
  `CSCO-NM-000500` (verify the checksum of software downloads) cites the
  HMAC requirement `SRG-APP-000411-NDM-000330`, and `CSCO-NM-000360`
  (disable Wireless Setup) cites the unnecessary-services requirement. Both
  rows are judged on what the rule checks.

### Where the commands come from

- **ISE is configured mostly in its web GUI.** Each GUI path and each
  quoted field label in the ISE command column was checked against the
  **Cisco Identity Services Engine Administrator Guide, Release 3.5**, read
  on cisco.com (all 17 chapters were searched). Cells read "GUI: path (what
  to set)"; quoted labels are the guide's field names. The ISE command
  column uses 87 GUI items.
- **ISE CLI commands** start from the fix text and were checked against the
  **Cisco Identity Services Engine CLI Reference Guide, Release 3.5** (the
  EXEC, EXEC show, and configuration mode chapters; the table uses
  17 command entries). A script checked every statement: it
  must match a command entry, every keyword must appear in that entry's
  syntax or syntax description, every number must lie inside the documented
  range, statements of the `password-policy` submode must follow
  `password-policy`, EXEC and configuration statements may not be mixed, and
  a keyword that the entry's Command History says is no longer supported or
  was removed fails. The script was tested with deliberately wrong commands
  (the fix texts' `password-policy min-password-length 15` on one line,
  `upper-case required 1`, `digit-required 1`, `snmp-server user ... v3
  hash`, `no snmp-server group`, `snmp-server host ... trap`, `write
  memory`, and `application configure disable Wi-Fi setup`, plus an
  undocumented NTP key type, out-of-range values, a submode statement
  without its parent, `copy running-config startup-config`, and a mixed
  block) and caught all of them. It was also tested with the GUI labels the
  fix texts use that the 3.5 guide does not have (`Log Collector Error`,
  `Deny-Access`, and three old paths) and caught those.
- **FortiNAC commands come from Chapter 25**, where the feature maps the
  same requirement, and otherwise from the FortiNAC-F 7.6.0 guides. The build
  fails if a command or pane in a row that names a Chapter 25 feature does
  not appear in that feature's command cell. A script checked every FortiNAC
  command as in Chapter 25: each `config` statement selects the section of
  the 7.6.0 CLI Reference for its context, each `set`, `append`, and
  `unselect` option must appear in that section with documented values and
  ranges, each `get` command must appear in the guide, and each GUI pane must
  appear in the 7.6.0 Administration Guide. It was tested with wrong commands
  (a misspelled context or option, an out-of-range timeout, an undocumented
  value, an NTP authentication option, a banner pane, and `get system
  banner`) and caught all of them.
- Read the command cells as in Chapters 25 and 34: each pair of backticks is
  one block (for FortiNAC, one statement), statements are separated by `;`
  to fit in a table cell (on the CLI, enter each on its own line), and values
  in `<ANGLE_BRACKETS>` are placeholders. ISE configuration commands are
  entered after `configure terminal`; the `password-policy` statement enters
  its own submode.
- A dash (**—**) in a command column means there is no command for the
  requirement on that platform; the setting column says why.

**ISE fix text corrections.** Several ISE fix texts do not match the ISE 3.5
documentation. The crosswalk uses the corrected commands and paths:

- `CSCO-NM-000400` to `CSCO-NM-000440` write `password-policy
  min-password-length 15`, `password-policy upper-case required 1`,
  `lower-case required 1`, `digit-required 1`, and `special-required 1`.
  In the CLI Reference, `password-policy` enters the config-password-policy
  submode, and the options are `min-password-length`, `upper-case-required`,
  `lower-case-required`, `digit-required`, and `special-required`, the last
  four without an argument. The CLI Reference also says that a password
  policy set in the GUI overwrites and takes precedence over the CLI one, so
  the rows give the GUI *Password Policy* page as well.
- `CSCO-NM-000350` removes SNMPv1 with `no snmp-server group <community>
  v1`, which is not an ISE command; the community is removed with `no
  snmp-server community <COMMUNITY> ro`. Its `snmp-server user` and
  `snmp-server host` lines give no authentication algorithm and the host
  line has a `trap` keyword; the 3.5 syntax needs `sha1` to `sha512` and
  `plain` or `hash`, and the host takes `version 3` directly. The crosswalk
  uses `sha256`.
- `CSCO-NM-000360` runs `application configure disable Wi-Fi setup`, which
  does not parse; the Command History of `application configure` says that
  Wireless Setup support was removed in 3.0, so there is nothing to disable
  on ISE 3.0 and later.
- `CSCO-NC-000290` defines an `md5` NTP key, although the requirement asks
  for an AES-based method, and ends with `write memory`. The 3.5 CLI
  Reference adds the `aes128` and `aes256` key types (the 3.1 to 3.4 CLI
  References list only `md5`, `sha1`, `sha256`, and `sha512`), has no
  `write memory` command, and says that from 3.2 `copy` no longer supports
  the running-config and startup-config functions. The crosswalk uses
  `aes256` and no save command.
- `CSCO-NM-000340` gives `request security pki generate-key-pair ... type rsa
  size <512 | 1024 | 2048 | 4096>`, which is Junos OS syntax, not an ISE
  command, and offers 512-bit and 1024-bit keys. On ISE the key type and
  length are chosen in the *Certificate Signing Requests* form; use RSA 2048
  or larger, or ECDSA.
- `CSCO-NM-000220`, `CSCO-NC-000200`, and `CSCO-NC-000210` enable the alarm
  "Log Collector Error"; the 3.5 alarm is named *Log Collection Error*.
- `CSCO-NM-000090` names *Authorization >> Permissions > Policy*; the 3.5
  page is *Administration > System > Admin Access > Authorization > RBAC
  Policy*.
- `CSCO-NC-000020`, `CSCO-NC-000260`, and `CSCO-NC-000270` select
  "Deny-Access"; the authorization profile is *DenyAccess*.
- `CSCO-NC-000120` uses the *Blacklist* endpoint identity group, which the
  3.5 guide calls *Blocked List*.
- `CSCO-NC-000250` points to *Work Centers > Posture > Settings > Posture
  General Settings*, which is not in the 3.5 guide; its own note gives the
  current page, *Administration > System > Settings > Posture > General
  Settings*.
- `CSCO-NC-000240` enables "Use ISE Messaging Service for UDP Syslogs
  delivery to MnT" under *Logging > Log Settings*, a page the 3.5 guide does
  not have. The guide says that from 3.5 the messaging service for the
  built-in UDP targets is enabled by default and keeps about two and a half
  hours of data while the MnT node is unreachable; the crosswalk uses a TCP
  or secure syslog target with *Buffer Messages When Server Down*.
- `CSCO-NC-000040` to `CSCO-NC-000110` place posture requirements under
  *Work Centers >> Posture >> Policy Elements >> Requirements*; the 3.5 guide
  gives *Policy > Policy Elements > Results > Posture > Requirements*.
  `CSCO-NC-000060` checks host IDS/IPS software with a Firewall Condition,
  which the guide describes as a check for firewall products; the crosswalk
  uses a Service Condition, which checks that a service is running.
- `CSCO-NM-000130`, `CSCO-NM-000210`, and `CSCO-NM-000560` say that the
  remote target type is always Syslog and cannot be changed; the 3.5 guide
  offers *TCP Syslog* and *Secure Syslog* target types, which the crosswalk
  uses.

### Where the version columns come from

The crosswalk table has a version column for each platform:

- **ISE version** for a CLI command is the earliest release in the "Command
  History" table of its entry in the 3.5 CLI Reference; where a cell uses
  several commands, it is the latest of those releases. Most entries give
  `2.0.0.306`, the ISE 2.0 build in which the command was introduced; the
  `password-policy` submode options share the history of `password-policy`.
  Where a row depends on a keyword that the Command History does not date,
  the column names the keyword and the earliest CLI Reference that lists it:
  `3.5 (aes256 keyword)` for the AES NTP key, and `3.1 or earlier (sha256
  keyword)` for SNMPv3, because 3.1 is the oldest CLI Reference checked.
  `Not present from 3.0` marks Wireless Setup, which the Command History says
  was removed in 3.0.
- **GUI settings have no command history.** Those cells read `ISE 3.5
  Administrator Guide (no command history)`, the guide in which the path and
  labels were verified. Older releases may place a page elsewhere; several
  fix text paths (above) are from older releases.
- **FortiNAC version** is the "Introduced (FortiNAC-F)" entry of the Chapter
  25 feature that the FortiNAC setting uses. Chapter 25 built that column
  from the release notes of all 23 FortiNAC-F releases; `7.2.0` marks a core
  feature described in the first FortiNAC-F release.
- **Not in the Chapter 25 feature map (FortiNAC-F 7.6.0 guides)** marks a
  FortiNAC setting that comes only from the 7.6.0 guides (the database
  archive age times), so no first release is given.
- A dash (**—**) means the row has no command on that platform.

### Alignment categories

Every row has one of six categories:

| Category | Meaning |
| --- | --- |
| Same requirement | Chapter 25 maps a FortiNAC feature to the same ISE rule ID or SRG ID, and the feature meets the requirement. |
| Equivalent setting | A FortiNAC setting meets the requirement, although Chapter 25 did not map it to this SRG ID. |
| Partial | FortiNAC meets part of the requirement. The setting column says what is missing. |
| Not supported | FortiNAC has no such capability, so it cannot meet the rule. |
| Not applicable | The rule targets a component, role, or protocol that FortiNAC does not have. |
| By procedure | The requirement is met by a process rather than a setting, on both platforms. |

**Partial**, **Not supported**, and **Not applicable** take precedence over
**Same requirement**: where Chapter 25 maps the same ID but FortiNAC does
not fully meet it, the row says so and its setting cell notes that Chapter
25 maps the requirement.

## Design Considerations

- **Record FortiNAC findings against SRG requirements.** In a mixed estate
  the ISE rules give one list of what to check on every NAC system. For
  FortiNAC, record each finding against the SRG ID in the table (an NDM ID,
  or the `SRG-NET-...-NAC-...` ID of the ISE NAC rule), on an SRG-based
  checklist, and keep the ISE rule ID as the reference.
- **Take the stricter value where the two differ.** The ISE GUI accepts an
  administrator idle timeout of 6 to 100 minutes, so the ISE STIG asks for
  **six minutes**, while the NDM SRG asks for **five**; FortiNAC administrator
  profiles and the CLI accept 5. Set 5 on FortiNAC and 6 on ISE, and record
  the ISE value as the vendor limit.
- **Plan FIPS mode and its gap.** Seven ISE NDM rules are met by turning on
  FIPS mode, which needs a restart. FortiNAC-F documents no FIPS mode, so six
  of those rows are Partial on FortiNAC (the replay-resistance rule is met by
  HTTPS and SSH alone); use strong encryption mode, TLS 1.2 and 1.3 only, and
  record the finding (Chapter 25).
- **Check the ISE release before using a fix text.** AES NTP keys need ISE
  3.5, Wireless Setup is gone from 3.0, and several GUI paths in the fix
  texts belong to older releases; see *ISE fix text corrections*.
- **Assess FortiNAC's RADIUS server and guests separately.** The ISE STIGs
  put AAA and guest services out of scope; FortiNAC's local RADIUS server
  and guest accounts are assessed against the AAA Services SRG (the second
  table).

## Implementation and Automation

### The crosswalk table

One row per Cisco ISE STIG rule: 51 ISE-NDM rules, then 30
ISE-NAC rules. Severity is the ISE rule's category. The Requirement column
summarizes what the ISE rule requires in plain language; the SRG ID links it
to the requirement text. FortiNAC has no STIG, so there is no FortiNAC STIG
rule column. The command columns follow the conventions in *Where the
commands come from*, and the version columns those in *Where the version
columns come from*.

[Download the crosswalk as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/35-cisco-ise-and-fortinac-stig-crosswalk-crosswalk.csv) (81 rows).

| ISE rule | Severity | SRG ID | Requirement | ISE command | ISE version | FortiNAC setting | FortiNAC command | FortiNAC version | Alignment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ISE-NDM `CSCO-NM-000010` | CAT III | `SRG-APP-000001-NDM-000200` | Limit concurrent administrator sessions to an organization-defined number for the GUI, and to one for the CLI | GUI: Administration > System > Admin Access > Settings > Access > Session (maximum concurrent sessions for the GUI and the CLI; CLI set to 1) | ISE 3.5 Administrator Guide (no command history) | Not supported: the FortiNAC-F guides document a maximum number of concurrent sessions only for network users and hosts, not for administrators. Allow the Admin UI and SSH only on port1 from management hosts, and record the finding | — | — | Not supported |
| ISE-NDM `CSCO-NM-000020` | CAT II | `SRG-APP-000317-NDM-000282` | Change the passwords of the local CLI and web accounts when someone who knows them leaves the role | GUI: Administration > System > Admin Access > Administrators > Admin Users ("Generate Password") | ISE 3.5 Administrator Guide (no command history) | By procedure: change the CLI admin password and the local Admin UI account of last resort whenever a holder leaves, and keep the new password sealed for emergency use | `config system admin`; `edit admin`; `set password <PASSWORD>`; `end` | 7.2.0 | By procedure |
| ISE-NDM `CSCO-NM-000030` | CAT II | `SRG-APP-000026-NDM-000208` | Audit the creation of administrator accounts, including the local account of last resort | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO, with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Admin auditing log, which records who changed what and when, including administrator accounts | GUI: Logs > Audit Logs | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000040` | CAT II | `SRG-APP-000027-NDM-000209` | Audit the modification of administrator accounts | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO, with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Admin auditing log | GUI: Logs > Audit Logs | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000050` | CAT II | `SRG-APP-000028-NDM-000210` | Audit the disabling of administrator accounts | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO, with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Admin auditing log (Chapter 25 also maps administrator expiration and aging, which disables accounts) | GUI: Logs > Audit Logs | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000060` | CAT II | `SRG-APP-000029-NDM-000211` | Audit the removal of administrator accounts | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO, with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Admin auditing log (Chapter 25 also maps administrator expiration and aging) | GUI: Logs > Audit Logs | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000070` | CAT III | `SRG-APP-000319-NDM-000283` | Audit the enabling of administrator accounts | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO, with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Admin auditing log, which records changes to administrator accounts | GUI: Logs > Audit Logs | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000080` | CAT II | `SRG-APP-000148-NDM-000346` | Keep only one local web administrator account, as the account of last resort | GUI: Administration > System > Admin Access > Administrators > Admin Users (one local administrator in the Super Admin group; all others external) | ISE 3.5 Administrator Guide (no command history) | The CLI admin account and one local Admin UI administrator as the accounts of last resort; every other administrator authenticates through LDAP or RADIUS | `config system admin`; `edit admin`; `set password <PASSWORD>`; `end` | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000090` | CAT I | `SRG-APP-000340-NDM-000288` | Prevent non-privileged users from executing privileged functions | GUI: Administration > System > Admin Access > Administrators > Admin Groups; GUI: Administration > System > Admin Access > Authorization > RBAC Policy | ISE 3.5 Administrator Guide (no command history) | Least-privilege administrator profiles; the System Administrator profile only for a few accounts | GUI: Users & Hosts > Administrators | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000100` | CAT II | `SRG-APP-000343-NDM-000289` | Audit the execution of privileged functions | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO and "AAA Audit", with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Admin auditing log | GUI: Logs > Audit Logs | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000110` | CAT II | `SRG-APP-000065-NDM-000214` | Lock an account for 15 minutes after three consecutive failed logons | GUI: Administration > System > Admin Access > Authentication > Lock/Suspend Settings ("Suspend Or Lock Account With Incorrect Login Attempts" 3; "Suspend Account For n Minutes" 15) | ISE 3.5 Administrator Guide (no command history) | Administrator profile lockout (3 attempts, 900 seconds); Chapter 25 maps the requirement, but the guide says that only the Inactivity Time of the System Administrator profile can be changed, and failures are not counted in a 15-minute window. On 7.6, also set admin-lockout-threshold 3 and admin-lockout-duration 900 for the CLI | GUI: Users & Hosts > Administrators | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000120` | CAT II | `SRG-APP-000068-NDM-000215` | Show the Standard Mandatory DoD Notice and Consent Banner before logon | GUI: Administration > System > Admin Access > Settings > Access > Session ("Pre-login banner" with the DoD banner text) | ISE 3.5 Administrator Guide (no command history) | Not supported: the guides document no logon banner for the Admin UI or SSH (Chapter 25). Reach both only through a jump host or gateway that shows the banner, and record the finding | — | — | Not supported |
| ISE-NDM `CSCO-NM-000130` | CAT II | `SRG-APP-000080-NDM-000220` | Protect against an administrator falsely denying actions (non-repudiation) | GUI: Administration > System > Logging > Remote Logging Targets ("Secure Syslog" target for the central syslog server) | ISE 3.5 Administrator Guide (no command history) | The admin auditing log ties each change to the administrator; send events to the log receivers so that the record is kept off the appliance | GUI: System > Settings > System communication > Log receivers | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000140` | CAT II | `SRG-APP-000091-NDM-000223` | Generate audit records when privileges are accessed | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO and "AAA Audit", with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Admin login events (Admin User Login Success and Admin User Login Failure) logged internally and externally | GUI: Logs > Events > Event management | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000150` | CAT II | `SRG-APP-000495-NDM-000318` | Generate audit records when administrator privileges are modified | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO and "AAA Audit", with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Admin auditing log, which records changes to administrators and administrator profiles | GUI: Logs > Audit Logs | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000160` | CAT II | `SRG-APP-000499-NDM-000319` | Generate audit records when administrator privileges are deleted | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO and "AAA Audit", with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Admin auditing log | GUI: Logs > Audit Logs | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000170` | CAT II | `SRG-APP-000503-NDM-000320` | Generate audit records for successful logons | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO and "AAA Audit", with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Authentication and admin login events, logged internally and externally | GUI: Logs > Events > Event management | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000180` | CAT II | `SRG-APP-000504-NDM-000321` | Generate audit records for privileged activities and other system-level access | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO and "AAA Audit", with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Admin auditing log | GUI: Logs > Audit Logs | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000190` | CAT II | `SRG-APP-000506-NDM-000323` | Generate audit records for concurrent logons from different workstations | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO, with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Admin User Login Success events record each administrator logon, so concurrent logons appear in the event log | GUI: Logs > Events > Event management | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000200` | CAT II | `SRG-APP-000357-NDM-000293` | Limit the storage used by locally stored logs | GUI: Administration > System > Logging > Local Log Settings ("Local Log Storage Period") | ISE 3.5 Administrator Guide (no command history) | Database archive age times for events, alarms, and scan results, with the scheduled archive and purge task | GUI: System > Settings > System management > Database archive (Event/Alarms Age Time) | Not in the Chapter 25 feature map (FortiNAC-F 7.6.0 guides) | Equivalent setting |
| ISE-NDM `CSCO-NM-000210` | CAT II | `SRG-APP-000515-NDM-000325` | Send audit records to a central log server separate from the system | GUI: Administration > System > Logging > Remote Logging Targets ("Secure Syslog" or "TCP Syslog" target) | ISE 3.5 Administrator Guide (no command history) | Log receivers | GUI: System > Settings > System communication > Log receivers | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000220` | CAT II | `SRG-APP-000360-NDM-000295` | Alert one or more people when the log collection process fails | GUI: Administration > System > Settings > Alarm Settings ("Log Collection Error" enabled, with email recipients) | ISE 3.5 Administrator Guide (no command history) | Alarm mappings with email notification; Chapter 25 maps the requirement, but the guides document no alarm when a log receiver stops receiving events or audit processing fails. Alert on missing events at the log server | GUI: Logs > Alarms | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000230` | CAT II | `SRG-APP-000373-NDM-000298` | Synchronize the clock with redundant authoritative time sources (cites a retired SRG ID) | GUI: Administration > System > Settings > System Time (two or more NTP servers) | ISE 3.5 Administrator Guide (no command history) | Two NTP servers; Chapter 25 maps the current requirement for the topic, SRG-APP-000920-NDM-000320 | `config system ntp`; `set ntpserver <NTP_SERVER_1> <NTP_SERVER_2>`; `set ntpsync enable`; `end` | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000240` | CAT II | `SRG-APP-000374-NDM-000299` | Record audit time stamps that map to UTC | `clock timezone UTC` | 2.0.0.306 | Time is stored in UTC in the database; synchronize with NTP | `config system ntp`; `set ntpserver <NTP_SERVER_1> <NTP_SERVER_2>`; `set ntpsync enable`; `end` | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000260` | CAT II | `SRG-APP-000516-NDM-000335` | Restrict who can change the firmware, operating system, and hardware components | GUI: Administration > System > Admin Access > Administrators > Admin Groups (only authorized members in the groups with edit access) | ISE 3.5 Administrator Guide (no command history) | Least-privilege administrator profiles; only a few accounts get the System Administrator profile, which can upgrade firmware and change system settings | GUI: Users & Hosts > Administrators | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000270` | CAT II | `SRG-APP-000516-NDM-000336` | Authenticate administrators through an external authentication server | GUI: Administration > System > Admin Access > Authentication (Password Based, with an external identity source); GUI: Administration > System > Admin Access > Administrators > Admin Groups (group type "External", mapped to the directory group); GUI: Administration > System > Admin Access > Authorization > RBAC Policy | ISE 3.5 Administrator Guide (no command history) | Administrator authentication by LDAP or RADIUS, with profile mappings from directory groups | GUI: Users & Hosts > Administrators | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000280` | CAT II | `SRG-APP-000516-NDM-000351` | Run a release that the vendor still supports (cites a retired SRG ID) | `show version`; GUI: Administration > System > Upgrade | 2.0.0.306; ISE 3.5 Administrator Guide (no command history) | Firmware upgrades to a supported FortiNAC-F release; Chapter 25 maps the current requirement for the topic, SRG-APP-001035-NDM-000340 | GUI: System > Settings > Updates > System | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000300` | CAT II | `SRG-APP-000516-NDM-000334` | Log a locally defined list of auditable events (cites a retired SRG ID) | GUI: Administration > System > Logging > Logging Categories (each category on the local list, with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Enable the events on the local list and log them internally and externally; the nearest current requirement is SRG-APP-000095-NDM-000225, which Chapter 25 maps to this feature | GUI: Logs > Events > Event management | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000330` | CAT III | `SRG-APP-000516-NDM-000341` | Back up the configuration when it changes, or weekly | GUI: Administration > System > Maintenance > Repository (SFTP repository on another system); GUI: Administration > System > Backup & Restore ("Configuration Data Backup", with an encryption key and a schedule) | ISE 3.5 Administrator Guide (no command history) | Scheduled database and system backups copied off the appliance; Chapter 25 maps the system-level backup requirement, SRG-APP-000516-NDM-000340 | GUI: System > Settings > System management > Remote backup configuration | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000340` | CAT II | `SRG-APP-000516-NDM-000344` | Use DoD PKI certificates rather than self-signed certificates | GUI: Administration > System > Certificates > Certificate Signing Requests; GUI: Administration > System > Certificates > Trusted Certificates | ISE 3.5 Administrator Guide (no command history) | DoD-issued server certificates, and only DoD CAs in the trusted certificates | GUI: System > Certificate management | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000350` | CAT I | `SRG-APP-000142-NDM-000245` | Prohibit unnecessary and nonsecure functions, ports, protocols, and services (SNMPv3 only, if SNMP is used) | `snmp-server enable`; `snmp-server user <USER> v3 sha256 plain <AUTH_PASSWORD> <PRIV_PASSWORD>`; `snmp-server host <NMS_IP> version 3 <USER> <ENGINE_ID> sha256 plain <AUTH_PASSWORD> <PRIV_PASSWORD>`; `no snmp-server community <COMMUNITY> ro` | 3.1 or earlier (sha256 keyword) | SNMPv3 AuthPriv, or SNMP disabled; only the services the deployment uses in set allowaccess | GUI: System > Settings > System communication > SNMP | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000360` | CAT I | `SRG-APP-000142-NDM-000245` | Disable Wireless Setup on production systems | — | Not present from 3.0 (Wireless Setup removed) | Not applicable: FortiNAC-F has no Wireless Setup function; Chapter 25 maps the requirement (unnecessary services) to the allowaccess settings | — | — | Not applicable |
| ISE-NDM `CSCO-NM-000370` | CAT II | `SRG-APP-000156-NDM-000250` | Use replay-resistant authentication for privileged network access | GUI: Administration > System > Settings > FIPS Mode ("Enabled") | ISE 3.5 Administrator Guide (no command history) | Admin UI only over HTTPS and the CLI only over SSH, whose TLS and SSH sessions resist replay | `config system interface`; `edit port1`; `unselect allowaccess http-adminui`; `next`; `end` | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000380` | CAT II | `SRG-APP-000395-NDM-000310` | Authenticate SNMP messages with a FIPS-validated HMAC | GUI: Administration > System > Settings > FIPS Mode ("Enabled") | ISE 3.5 Administrator Guide (no command history) | SNMPv3 AuthPriv with SHA1 and AES-128; Chapter 25 maps the requirement, but there is no SHA-2 option and no FIPS mode to show validation | GUI: System > Settings > System communication > SNMP | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000400` | CAT II | `SRG-APP-000164-NDM-000252` | Enforce a minimum password length of 15 characters | `password-policy; min-password-length 15`; GUI: Administration > System > Admin Access > Authentication > Password Policy ("Minimum Length" 15) | 2.0.0.306; ISE 3.5 Administrator Guide (no command history) | Chapter 25 maps the requirement, but there is no length policy: CLI passwords need 8 to 128 characters and local Admin UI passwords have only character rules. Set 15 or more characters by procedure, or authenticate administrators through LDAP or RADIUS | GUI: Users & Hosts > Administrators | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000410` | CAT II | `SRG-APP-000166-NDM-000254` | Require at least one uppercase character in passwords | `password-policy; upper-case-required`; GUI: Administration > System > Admin Access > Authentication > Password Policy ("Uppercase alphabetic characters") | 2.0.0.306; ISE 3.5 Administrator Guide (no command history) | CLI and SSH passwords must contain an uppercase letter (7.6.0 Administration Guide); local Admin UI passwords have no complexity policy | `config system admin`; `edit admin`; `set password <PASSWORD>`; `end` | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000420` | CAT II | `SRG-APP-000167-NDM-000255` | Require at least one lowercase character in passwords | `password-policy; lower-case-required`; GUI: Administration > System > Admin Access > Authentication > Password Policy ("Lowercase alphabetic characters") | 2.0.0.306; ISE 3.5 Administrator Guide (no command history) | CLI and SSH passwords must contain a lowercase letter; local Admin UI passwords have no complexity policy | `config system admin`; `edit admin`; `set password <PASSWORD>`; `end` | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000430` | CAT II | `SRG-APP-000168-NDM-000256` | Require at least one numeric character in passwords | `password-policy; digit-required`; GUI: Administration > System > Admin Access > Authentication > Password Policy ("Numeric characters") | 2.0.0.306; ISE 3.5 Administrator Guide (no command history) | CLI and SSH passwords must contain a number; local Admin UI passwords have no complexity policy | `config system admin`; `edit admin`; `set password <PASSWORD>`; `end` | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000440` | CAT II | `SRG-APP-000169-NDM-000257` | Require at least one special character in passwords | `password-policy; special-required`; GUI: Administration > System > Admin Access > Authentication > Password Policy ("Non-alphanumeric characters") | 2.0.0.306; ISE 3.5 Administrator Guide (no command history) | CLI and SSH passwords must contain one of the listed symbols; local Admin UI passwords have no complexity policy | `config system admin`; `edit admin`; `set password <PASSWORD>`; `end` | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000460` | CAT I | `SRG-APP-000172-NDM-000259` | Protect password authentication with FIPS-validated SHA-2 or stronger | GUI: Administration > System > Settings > FIPS Mode ("Enabled") | ISE 3.5 Administrator Guide (no command history) | Admin UI only over HTTPS; Chapter 25 maps the requirement, but there is no FIPS mode to show FIPS-validated cryptography | `config system interface`; `edit port1`; `unselect allowaccess http-adminui`; `next`; `end` | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000480` | CAT I | `SRG-APP-000179-NDM-000265` | Use FIPS-validated SHA-2 for HMACs, key derivation, random bit generation, and hashing | GUI: Administration > System > Settings > FIPS Mode ("Enabled") | ISE 3.5 Administrator Guide (no command history) | Strong encryption mode; Chapter 25 maps the requirement, but there is no FIPS mode | `config system global`; `set strong-crypto enable`; `end` | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000490` | CAT II | `SRG-APP-000411-NDM-000330` | Use a FIPS-validated HMAC to protect remote maintenance and diagnostic sessions | GUI: Administration > System > Settings > FIPS Mode ("Enabled") | ISE 3.5 Administrator Guide (no command history) | Strong encryption mode; Chapter 25 maps the requirement, but there is no FIPS mode | `config system global`; `set strong-crypto enable`; `end` | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000500` | CAT I | `SRG-APP-000411-NDM-000330` | Verify the checksum of every software download before installing it | `application upgrade prepare <BUNDLE> <REPOSITORY>` | 2.0.0.306 | Signed firmware enforcement and file integrity verification from 7.6.3; on older releases compare the checksum from Fortinet support by procedure. Chapter 25 maps the SRG ID that DISA cites (an HMAC requirement) to strong encryption mode | `get system status` | 7.6.3 and later | Partial |
| ISE-NDM `CSCO-NM-000510` | CAT I | `SRG-APP-000412-NDM-000331` | Use FIPS 140-2 validated cryptography to protect remote maintenance sessions | GUI: Administration > System > Settings > FIPS Mode ("Enabled") | ISE 3.5 Administrator Guide (no command history) | Strong encryption mode, with TLS 1.2 and 1.3 only in the TLS service configurations; Chapter 25 maps the requirement, but there is no FIPS mode | `config system global`; `set strong-crypto enable`; `end` | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000520` | CAT I | `SRG-APP-000190-NDM-000267` | End management sessions after a period of inactivity (six minutes in the ISE STIG; five in the SRG) | GUI: Administration > System > Admin Access > Settings > Session ("Session Idle Timeout" 6) | ISE 3.5 Administrator Guide (no command history) | Inactivity Time of 5 minutes on every administrator profile, including System Administrator; also admin-idle-timeout 5 for the CLI | GUI: Users & Hosts > Administrators | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000530` | CAT II | `SRG-APP-000224-NDM-000270` | Generate session identifiers with a FIPS 140-2 approved random number generator | GUI: Administration > System > Settings > FIPS Mode ("Enabled") | ISE 3.5 Administrator Guide (no command history) | Admin UI sessions over TLS with strong encryption mode; no FIPS mode, and the guides do not describe the random number generator | `config system global`; `set strong-crypto enable`; `end` | 7.2.0 | Partial |
| ISE-NDM `CSCO-NM-000540` | CAT I | `SRG-APP-000231-NDM-000271` | Allow only authorized administrators to view or change the configuration and stored files | GUI: Administration > System > Admin Access > Administrators > Admin Users (one local administrator in the Super Admin group; all others external) | ISE 3.5 Administrator Guide (no command history) | Least-privilege administrator profiles | GUI: Users & Hosts > Administrators | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000550` | CAT II | `SRG-APP-000435-NDM-000315` | Protect the device against denial-of-service attacks with rate limits | `synflood-limit <SYN_PER_SECOND>`; `rate-limit <NAME> <PACKETS_PER_SECOND> port <PORT>` | 2.0.0.306 | Not supported: the 7.6.0 CLI Reference has no SYN flood or rate-limit setting. Allow only the needed services in set allowaccess, protect the appliance with an upstream firewall, and record the finding | — | — | Not supported |
| ISE-NDM `CSCO-NM-000560` | CAT II | `SRG-APP-000516-NDM-000350` | Send log data to at least two central log servers | GUI: Administration > System > Logging > Remote Logging Targets (two targets, "Secure Syslog" or "TCP Syslog") | ISE 3.5 Administrator Guide (no command history) | At least two log receivers | GUI: System > Settings > System communication > Log receivers | 7.2.0 | Same requirement |
| ISE-NDM `CSCO-NM-000650` | CAT II | `SRG-APP-000092-NDM-000224` | Start session auditing at startup | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO and "AAA Audit", with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Enabled events are logged internally and externally from startup | GUI: Logs > Events > Event management | 7.2.0 | Equivalent setting |
| ISE-NDM `CSCO-NM-000720` | CAT II | `SRG-APP-000101-NDM-000231` | Record privileged commands in full text in the audit records | GUI: Administration > System > Logging > Logging Categories ("Administrative and Operational Audit" at INFO, with the remote syslog target selected) | ISE 3.5 Administrator Guide (no command history) | Admin auditing log records Admin UI changes, but CLI changes appear only as CLI Tool, and the guides do not say that CLI commands are recorded in full text | GUI: Logs > Audit Logs | 7.2.0 | Partial |
| ISE-NAC `CSCO-NC-000010` | CAT I | `SRG-NET-000062-NAC-000340` | Use TLS 1.2 or later between the endpoint agent and the NAC server | GUI: Administration > System > Settings > Security Settings ("Allow TLS 1.0", "Allow TLS 1.1", and "Allow Legacy Unsafe TLS Renegotiation for ISE as a Client" unchecked) | ISE 3.5 Administrator Guide (no command history) | TLS service configurations for the Persistent Agent with TLSv1.2 and TLSv1.3 only | GUI: System > Settings > Persistent Agent > Transport configurations | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000020` | CAT I | `SRG-NET-000015-NAC-000020` | Enforce approved access with authorization policies based on endpoint attributes, with deny or restricted access as the default | GUI: Work Centers > Network Access > Policy Sets (default authorization rule "DenyAccess" or a restricted result) | ISE 3.5 Administrator Guide (no command history) | User/host profiles and network access policies that map endpoints to logical networks; unknown endpoints stay in the registration or isolation network | GUI: Policy & Objects > Network access; GUI: Network > Logical networks | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000030` | CAT I | `SRG-NET-000015-NAC-000020` | Profile the endpoints that connect to the network | GUI: Administration > System > Deployment ("Enable Session Services" and "Enable Profiling Service" on each Policy Service node) | ISE 3.5 Administrator Guide (no command history) | Device profiling rules and device types | GUI: Users & Hosts > Device profiling rules | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000040` | CAT I | `SRG-NET-000015-NAC-000020` | Verify that a host-based firewall is running before granting trusted access | GUI: Work Centers > Posture > Policy Elements ("Firewall Condition"); GUI: Policy > Policy Elements > Results > Posture > Requirements; GUI: Work Centers > Posture > Posture Policy | ISE 3.5 Administrator Guide (no command history) | Endpoint compliance scans; Chapter 25 maps the requirement, but the host firewall is checked only through a custom process, service, or registry scan that you write | GUI: Policy & Objects > Endpoint compliance | 7.2.0 | Partial |
| ISE-NAC `CSCO-NC-000050` | CAT I | `SRG-NET-000015-NAC-000020` | Verify that anti-malware software is installed and up to date before granting trusted access | GUI: Work Centers > Posture > Policy Elements > Anti-Malware Condition ("Check against latest AV definition file version, if available"); GUI: Policy > Policy Elements > Results > Posture > Requirements; GUI: Work Centers > Posture > Posture Policy | ISE 3.5 Administrator Guide (no command history) | Anti-virus scans in endpoint compliance policies, with auto-definition updates | GUI: Policy & Objects > Endpoint compliance | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000060` | CAT I | `SRG-NET-000015-NAC-000020` | Verify that authorized host IDS/IPS software is running before granting trusted access | GUI: Policy > Policy Elements > Conditions > Posture > Service Condition; GUI: Policy > Policy Elements > Results > Posture > Requirements; GUI: Work Centers > Posture > Posture Policy | ISE 3.5 Administrator Guide (no command history) | Endpoint compliance scans; Chapter 25 maps the requirement, but host IDS/IPS software is checked only through a custom scan that you write | GUI: Policy & Objects > Endpoint compliance | 7.2.0 | Partial |
| ISE-NAC `CSCO-NC-000070` | CAT II | `SRG-NET-000015-NAC-000040` | Send endpoints that need automated remediation to a separate remediation VLAN | GUI: Work Centers > Network Access > Policy Sets (authorization rule for Session PostureStatus NonCompliant with the remediation VLAN result) | ISE 3.5 Administrator Guide (no command history) | Remediation on scan failure, which moves the host to the remediation network | GUI: Policy & Objects > Endpoint compliance > Scans | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000080` | CAT III | `SRG-NET-000015-NAC-000070` | Notify the user before automated remediation | GUI: Policy > Policy Elements > Results > Posture > Requirements (remediation action text in "Message shown to Agent User") | ISE 3.5 Administrator Guide (no command history) | Persistent Agent notification of the logical network, with user acknowledgment of VLAN changes | GUI: System > Settings > Persistent Agent > Properties | 7.4.0 and later | Same requirement |
| ISE-NAC `CSCO-NC-000090` | CAT II | `SRG-NET-000015-NAC-000080` | Allow only ISSM-approved endpoints, documented in the SSP, to bypass the policy assessment | GUI: Work Centers > Posture > Posture Policy (mandatory requirements for posture-required endpoints; exceptions only for documented devices) | ISE 3.5 Administrator Guide (no command history) | MAC address exclusion only for ISSM-approved devices recorded in the SSP | GUI: System > Settings > User/Host Management > MAC address exclusion | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000100` | CAT II | `SRG-NET-000015-NAC-000100` | Alert the ISSM and SA when security issues that put the network at risk are found | GUI: Administration > System > Logging > Logging Categories ("AAA Audit", "Failed Attempts", and "Posture and Client Provisioning Audit" sent to LogCollector) | ISE 3.5 Administrator Guide (no command history) | Alarm mappings that notify the SA and ISSO by email or SMS | GUI: Logs > Alarms | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000110` | CAT II | `SRG-NET-000015-NAC-000110` | Create a record with enough detail for remediation when an endpoint fails the assessment | GUI: Policy > Policy Elements > Results > Posture > Requirements (remediation action text in "Message shown to Agent User") | ISE 3.5 Administrator Guide (no command history) | Remediation on scan failure, with instructions for the scan failure | GUI: Policy & Objects > Endpoint compliance > Scans | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000120` | CAT II | `SRG-NET-000015-NAC-000120` | Block endpoints and end their connection when critical security issues are found | GUI: Operations > Adaptive Network Control > Policy List (Quarantine action); GUI: Work Centers > Network Access > Policy Sets (global exception rule on Session ANCPolicy, or on the "Blocked List" endpoint identity group) | ISE 3.5 Administrator Guide (no command history) | Security incident rules whose actions disable the host | GUI: Logs > Security Incidents | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000130` | CAT II | `SRG-NET-000015-NAC-000130` | Keep endpoints in the assessment network from reaching other devices except to be assessed or identified | GUI: Work Centers > Network Access > Policy Sets (remediation result that blocks traffic within the VLAN: private VLAN, dACL, ACL, or SGT) | ISE 3.5 Administrator Guide (no command history) | Registration and isolation logical networks with access limited to the portal and remediation resources | GUI: Network > Logical networks | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000140` | CAT II | `SRG-NET-000322-NAC-001230` | Deny or restrict access for endpoints that fail required posture checks | GUI: Work Centers > Network Access > Policy Sets (Session PostureStatus Compliant and NonCompliant rules, the NonCompliant rule with a restricted result) | ISE 3.5 Administrator Guide (no command history) | Network access policies that send non-compliant hosts to a restricted logical network | GUI: Policy & Objects > Network access; GUI: Network > Logical networks | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000150` | CAT II | `SRG-NET-000492-NAC-002100` | Log a record when an endpoint fails authentication | GUI: Administration > System > Logging > Logging Categories ("Failed Attempts" sent to LogCollector) | ISE 3.5 Administrator Guide (no command history) | Authentication failure events, logged internally and externally | GUI: Logs > Events > Event management | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000160` | CAT II | `SRG-NET-000492-NAC-002101` | Log a record when an endpoint fails posture because required security software is missing | GUI: Administration > System > Logging > Logging Categories ("Posture and Client Provisioning Audit" sent to LogCollector) | ISE 3.5 Administrator Guide (no command history) | Security Risk Host and scan failure events, logged internally and externally | GUI: Logs > Events > Event management | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000170` | CAT II | `SRG-NET-000492-NAC-002120` | Alert the SA when endpoints fail the policy assessment for organization-defined infractions | GUI: Administration > System > Logging > Logging Categories ("Posture and Client Provisioning Audit" sent to LogCollector) | ISE 3.5 Administrator Guide (no command history) | Alarm mappings for scan failure events, with email or SMS notification | GUI: Logs > Alarms | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000200` | CAT II | `SRG-NET-000335-NAC-001360` | Send a critical alert to the ISSO and SA when audit processing fails | GUI: Administration > System > Settings > Alarm Settings ("Log Collection Error" enabled, with email recipients) | ISE 3.5 Administrator Guide (no command history) | Event thresholds for disk space mapped to alarms that notify the SA and ISSO; the guides document no alarm when audit processing or a log receiver fails | GUI: Logs > Alarms | 7.2.0 | Partial |
| ISE-NAC `CSCO-NC-000210` | CAT II | `SRG-NET-000335-NAC-001370` | Alert the SA and ISSO when events cannot be written to local storage or the central server | GUI: Administration > System > Settings > Alarm Settings ("Log Collection Error" enabled, with email recipients) | ISE 3.5 Administrator Guide (no command history) | Disk space event thresholds mapped to alarms cover local storage; the guides document no alarm when a log receiver cannot be reached | GUI: Logs > Alarms | 7.2.0 | Partial |
| ISE-NAC `CSCO-NC-000220` | CAT II | `SRG-NET-000336-NAC-001390` | Configure a secondary log server in case the primary is unreachable | GUI: Administration > System > Logging > Remote Logging Targets ("TCP Syslog" or "Secure Syslog" target with "Buffer Messages When Server Down") | ISE 3.5 Administrator Guide (no command history) | At least two log receivers | GUI: System > Settings > System communication > Log receivers | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000230` | CAT II | `SRG-NET-000088-NAC-000440` | Send a critical alert to the ISSO and SA when the central event log cannot be reached | GUI: Administration > System > Logging > Logging Categories ("Internal Operations Diagnostics" sent to LogCollector and LogCollector2) | ISE 3.5 Administrator Guide (no command history) | Not supported: the guides document no event or alarm when a log receiver cannot be reached (Chapter 25). Alert on missing events at the log server or SIEM, and record the finding | — | — | Not supported |
| ISE-NAC `CSCO-NC-000240` | CAT II | `SRG-NET-000089-NAC-000450` | Queue log records locally while the central log server cannot be reached | GUI: Administration > System > Logging > Remote Logging Targets ("TCP Syslog" or "Secure Syslog" target with "Buffer Messages When Server Down") | ISE 3.5 Administrator Guide (no command history) | Not supported: the guides document no local queue for log receivers (Chapter 25); events stay in the local event log until purged. Send to two log receivers, and record the finding | — | — | Not supported |
| ISE-NAC `CSCO-NC-000250` | CAT II | `SRG-NET-000512-NAC-002310` | Detect and track the endpoints attached to the network continuously | GUI: Administration > System > Settings > Posture > General Settings ("Continuous Monitoring Interval") | ISE 3.5 Administrator Guide (no command history) | Network device inventory and discovery, with L2 and L3 polling and MAC notification traps | GUI: Network > Inventory | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000260` | CAT II | `SRG-NET-000148-NAC-000620` | Deny network connection to endpoints that cannot be authenticated with an approved method | GUI: Work Centers > Network Access > Policy Sets (default authorization rule "DenyAccess" or a restricted result) | ISE 3.5 Administrator Guide (no command history) | Unknown and unauthenticated endpoints stay in the registration, isolation, or dead-end networks | GUI: Network > Logical networks | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000270` | CAT II | `SRG-NET-000343-NAC-001460` | Authenticate every endpoint before connecting it and assessing its posture | GUI: Work Centers > Network Access > Policy Sets (default authorization rule "DenyAccess" or a restricted result) | ISE 3.5 Administrator Guide (no command history) | Local RADIUS server for 802.1X with EAP-TLS, EAP-TTLS, PEAP, or TEAP | GUI: Network > RADIUS > Configure Local Server | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000280` | CAT II | `SRG-NET-000343-NAC-001470` | Give endpoints admitted through MAC Authentication Bypass only restricted access | GUI: Work Centers > Network Access > Policy Sets (restricted VLAN, ACL, or SGT results for every MAB authorization rule) | ISE 3.5 Administrator Guide (no command history) | MAB devices only in restricted logical networks | GUI: Policy & Objects > Network access | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000290` | CAT II | `SRG-NET-000550-NAC-002470` | Authenticate NTP servers with an AES-based cryptographic method | `ntp authentication-key <KEY_ID> aes256 plain <KEY>`; `ntp server <NTP_SERVER> key <KEY_ID>` | 3.5 (aes256 keyword) | Not supported: Chapter 25 maps the requirement to the NTP settings, but neither guide documents NTP authentication. Use internal NTP servers reached over the management network, and record the finding | — | — | Not supported |
| ISE-NAC `CSCO-NC-000300` | CAT II | `SRG-NET-000151-NAC-000630` | Authenticate endpoints with a bidirectional, FIPS-validated AES-based mechanism | GUI: Administration > System > Settings > Security Settings ("Allow TLS 1.0", "Allow TLS 1.1", and "Allow Legacy Unsafe TLS Renegotiation for ISE as a Client" unchecked) | ISE 3.5 Administrator Guide (no command history) | EAP-TLS, EAP-TTLS, PEAP, or TEAP with TLS 1.2 and 1.3 only in the local RADIUS server; Chapter 25 maps the requirement, but there is no FIPS mode | GUI: Network > RADIUS > Configure Local Server | 7.2.0 | Partial |
| ISE-NAC `CSCO-NC-000310` | CAT I | `SRG-NET-000512-NAC-002310` | Enforce the posture status of posture-required clients | GUI: Work Centers > Network Access > Policy Sets (Session PostureStatus Compliant and NonCompliant rules, the NonCompliant rule with a restricted result) | ISE 3.5 Administrator Guide (no command history) | Endpoint compliance policies with agents for every posture-required profile | GUI: Policy & Objects > Endpoint compliance | 7.2.0 | Same requirement |
| ISE-NAC `CSCO-NC-000320` | CAT I | `SRG-NET-000512-NAC-002310` | Have a posture policy for posture-required clients | GUI: Work Centers > Posture > Posture Policy (mandatory requirements for each posture-required group) | ISE 3.5 Administrator Guide (no command history) | Endpoint compliance policies and scans for every posture-required profile | GUI: Policy & Objects > Endpoint compliance | 7.2.0 | Same requirement |

### FortiNAC requirements with no Cisco ISE rule

The 38 requirements below are mapped to FortiNAC features in Chapter
25 but are cited by no Cisco ISE STIG rule, so an ISE rule checklist misses
them: 18 NDM and 20 AAA Services SRG requirements. The AAA
requirements cover FortiNAC's local RADIUS server and guest accounts
(secure EAP types, unique RADIUS shared secrets, RadSec, revocation checking,
temporary account removal, and the audit of every authentication), which the
ISE STIGs leave out of scope. The NDM requirements include multifactor
authentication, signed firmware, and the separation of management traffic;
four of them (`SRG-APP-000095-NDM-000225`, `SRG-APP-000516-NDM-000340`,
`SRG-APP-000920-NDM-000320`, and `SRG-APP-001035-NDM-000340`) are the current
requirements behind ISE rules that cite retired or neighboring IDs, so the
crosswalk table also covers them. Add all of them to the FortiNAC checklist.
The requirement text is the SRG title; the setting column lists the Chapter
25 features mapped to the requirement, and the version column gives the
release of the feature whose command is shown.

[Download the unmatched requirements as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/35-cisco-ise-and-fortinac-stig-crosswalk-unmatched.csv) (38 rows).

| SRG | SRG ID | Requirement | FortiNAC setting | FortiNAC command | FortiNAC version |
| --- | --- | --- | --- | --- | --- |
| NDM | `SRG-APP-000033-NDM-000212` | The network device must be configured to assign appropriate user roles or access levels to authenticated users. | Administrators and administrator profiles (permissions, landing page, login availability) | GUI: Users & Hosts > Administrators | 7.2.0 |
| NDM | `SRG-APP-000095-NDM-000225` | The network device must produce audit log records containing sufficient information to establish what type of event occurred. | Events and event management (enable events, thresholds, internal and external logging) | GUI: Logs > Events > Event management | 7.2.0 |
| NDM | `SRG-APP-000100-NDM-000230` | The network device must generate audit records containing information that establishes the identity of any individual or process associated with the event. | Admin auditing log (who changed what and when; CLI changes as CLI Tool) | GUI: Logs > Audit Logs | 7.2.0 |
| NDM | `SRG-APP-000131-NDM-000243` | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. | Secure boot, file integrity verification, and signed firmware enforcement | `get system status` | 7.6.3 and later |
| NDM | `SRG-APP-000149-NDM-000247` | The network device must be configured to use DoD PKI as multi-factor authentication (MFA) for interactive logins. | Multi-factor authentication for administrators (token by SMS or email; individual and global) | GUI: System > Settings > Authentication > Multi-factor Authentication | 7.6.5 and later |
| NDM | `SRG-APP-000153-NDM-000249` | The network device must be configured to authenticate each administrator prior to authorizing privileges based on assignment of group or role. | Administrator authentication by LDAP or RADIUS (Auth Type) and administrator profile mappings | GUI: Users & Hosts > Administrators | 7.2.0 |
| NDM | `SRG-APP-000170-NDM-000329` | The network device must require that when a password is changed, the characters are changed in at least eight of the positions within the password. | Local administrator passwords (character rules; no length or complexity policy) | GUI: Users & Hosts > Administrators | 7.2.0 |
| NDM | `SRG-APP-000378-NDM-000302` | The network device must prohibit installation of software without explicit privileged status. | Firmware upgrades (Updates > System, or execute restore image); Secure boot, file integrity verification, and signed firmware enforcement | GUI: System > Settings > Updates > System | 7.2.0 |
| NDM | `SRG-APP-000380-NDM-000304` | The network device must enforce access restrictions associated with changes to device configuration. | Admin auditing log (who changed what and when; CLI changes as CLI Tool); Admin audit and event logging of port enforcement changes, data exports, and syslog forwarding | GUI: Logs > Audit Logs | 7.2.0 |
| NDM | `SRG-APP-000395-NDM-000347` | The network device must authenticate Network Time Protocol sources using authentication that is cryptographically based. | NTP and time zone (UTC in the database) | `config system ntp`; `set ntpserver <NTP_SERVER_1> <NTP_SERVER_2>`; `set ntpsync enable`; `end` | 7.2.0 |
| NDM | `SRG-APP-000457-NDM-000352` | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). | Firmware upgrades (Updates > System, or execute restore image); Firmware upgrade from the FortiGuard Distribution Network | GUI: System > Settings > Updates > System | 7.2.0 |
| NDM | `SRG-APP-000516-NDM-000340` | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. | Database and system backups (scheduled tasks), remote backup over SSH or FTP, and configuration backup from the CLI; Secure FTP remote backup | GUI: System > Settings > System management > Remote backup configuration; `execute backup config scp <FILE> <SERVER> <USER> <PASSWORD>` | 7.2.0 |
| NDM | `SRG-APP-000820-NDM-000170` | The network device must be configured to implement multifactor authentication for local; network; and/or remote access to privileged accounts; and/or nonprivileged accounts such that one of the factors is provided by a device separate from the system gaining access. | SAML SSO for administrators and users, and FortiCloud SSO for admin login; Multi-factor authentication for administrators (token by SMS or email; individual and global) | GUI: Network > Service Connectors > Admin SAML SSO | 7.6.3 and later |
| NDM | `SRG-APP-000845-NDM-000220` | The network device must be configured to verify, when users create or update passwords, the passwords are not found on the list of commonly used, expected, or compromised passwords in IA-5 (1) (a) for password-based authentication. | Local administrator passwords (character rules; no length or complexity policy) | GUI: Users & Hosts > Administrators | 7.2.0 |
| NDM | `SRG-APP-000880-NDM-000290` | The network device must be configured to protect nonlocal maintenance sessions by separating the maintenance session from other network sessions with the system by logically separated communications paths. | Management (port1) and portal/isolation (port2) interfaces; CLI over SSH and the console; Out-of-band management in high availability configurations (ports 3 to 6) | `config system global`; `set management port1`; `set portal port2`; `end` | 7.2.0 |
| NDM | `SRG-APP-000910-NDM-000300` | The network device must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. | Certificate management (server certificates for Admin UI, portal, agent, and RADIUS; trusted certificates) | GUI: System > Certificate management | 7.2.0 |
| NDM | `SRG-APP-000920-NDM-000320` | The network device must be configured to synchronize system clocks within and between systems or system components. | NTP and time zone (UTC in the database) | `config system ntp`; `set ntpserver <NTP_SERVER_1> <NTP_SERVER_2>`; `set ntpsync enable`; `end` | 7.2.0 |
| NDM | `SRG-APP-001035-NDM-000340` | The network device hardware and software must be a version supported by the vendor. | Firmware upgrades (Updates > System, or execute restore image); FortiNAC-F VM SKUs and FortiNAC-OS (FortiOS-like CLI, firmware image) replacing CentOS 7; Migration of legacy CentOS C-series appliances to FortiNAC-OS; and 2 more | GUI: System > Settings > Updates > System | 7.2.0 |
| AAA | `SRG-APP-000024-AAA-000040` | AAA Services must be configured to automatically remove temporary user accounts after 72 hours. | Guest and contractor accounts, templates, and sponsors | GUI: Users & Hosts > Guests & Contractors > Guest & Contractor templates | 7.2.0 |
| AAA | `SRG-APP-000024-AAA-000050` | AAA Services must be configured to automatically remove authorizations for temporary user accounts after 72 hours. | Guest and contractor accounts, templates, and sponsors; Re-registration period for guest and contractor hosts | GUI: Users & Hosts > Guests & Contractors > Guest & Contractor templates | 7.2.0 |
| AAA | `SRG-APP-000025-AAA-000080` | AAA Services must be configured to automatically disable accounts after a 35-day period of account inactivity. | Aging of host and user records | GUI: System > Settings > User/Host Management > Aging | 7.2.0 |
| AAA | `SRG-APP-000089-AAA-000380` | AAA Services must be configured to audit each authentication and authorization transaction. | Events and event management (enable events, thresholds, internal and external logging); Live authentication logs (LDAP, Local, RADIUS, SAML, Social) | GUI: Logs > Events > Event management | 7.2.0 |
| AAA | `SRG-APP-000142-AAA-000010` | AAA Services must be configured to use secure protocols when connecting to directory services. | LDAP directories (SSL or STARTTLS security protocol, synchronization of users and groups) | GUI: System > Settings > Authentication > Directories | 7.2.0 |
| AAA | `SRG-APP-000142-AAA-000020` | AAA Services must be configured to use protocols that encrypt credentials when authenticating clients, as defined in the PPSM CAL and vulnerability assessments. | Captive portal and portal SSL certificate; RADIUS over TLS (RadSec) for the Local RADIUS Server | GUI: Portal > Portal SSL | 7.2.0 |
| AAA | `SRG-APP-000142-AAA-000680` | AAA Services must be configured to prohibit or restrict the use of organization-defined functions, ports, protocols, and/or services, as defined in the PPSM CAL and vulnerability assessments. | Interface access services (set allowaccess: SSH, Admin UI, SNMP, syslog, RADIUS, agent, DHCP, DNS, and others) | `config system interface`; `edit <PORT>`; `set allowaccess <ACCESS_LIST>`; `next`; `end` | 7.2.0 |
| AAA | `SRG-APP-000148-AAA-000390` | AAA Services must be configured to uniquely identify and authenticate organizational users. | Administrator authentication by LDAP or RADIUS (Auth Type) and administrator profile mappings; Microsoft Entra ID as a native authentication source (802.1X and portal) | GUI: Users & Hosts > Administrators | 7.2.0 |
| AAA | `SRG-APP-000158-AAA-000420` | AAA Services used for 802.1x must be configured to uniquely identify network endpoints (supplicants) before the authenticator establishes any connection. | Local RADIUS server (802.1X EAP termination; EAP types TLS, TTLS, PEAP, MD5, GTC, MSCHAPv2, FAST, TEAP) | GUI: Network > RADIUS > Configure Local Server | 7.2.0 |
| AAA | `SRG-APP-000172-AAA-000520` | AAA Services must be configured to encrypt transmitted credentials using a FIPS-validated cryptographic module. | TLS service configurations (Admin UI, Persistent Agent, and RADIUS EAP certificates, protocols, and ciphers); RADIUS over TLS (RadSec) for the Local RADIUS Server; TEAP for RADIUS clients and TLS 1.3 in the Local RADIUS Server | GUI: System > Settings > Persistent Agent > Transport configurations | 7.2.0 |
| AAA | `SRG-APP-000175-AAA-000570` | AAA Services must be configured to only accept certificates issued by a DoW-approved certificate authority (CA) for Public Key Infrastructure (PKI)-based authentication. | Certificate management (server certificates for Admin UI, portal, agent, and RADIUS; trusted certificates) | GUI: System > Certificate management | 7.2.0 |
| AAA | `SRG-APP-000175-AAA-000580` | AAA Services must be configured to not accept certificates that have been revoked for PKI-based authentication. | OCSP certificate revocation checking for EAP-TLS; OCSP soft-fail flag for certificate-based RADIUS authentication | GUI: Network > RADIUS > Configure Local Server | 7.2.0 |
| AAA | `SRG-APP-000177-AAA-000600` | AAA Services must be configured to map the authenticated identity to the user account for PKI-based authentication. | Client certificate attribute ranking for user authentication (CN, DNS, UPN) | GUI: Network > RADIUS > Configure Local Server | 7.6.5 and later |
| AAA | `SRG-APP-000358-AAA-000280` | AAA Services must be configured to send audit records to a centralized audit server. | Log receivers (Syslog CSV, Syslog CEF, SNMP trap, FortiAnalyzer OFTP) | GUI: System > Settings > System communication > Log receivers | 7.2.0 |
| AAA | `SRG-APP-000394-AAA-000430` | AAA Services used for 802.1x must be configured to authenticate network endpoint devices (supplicants) before the authenticator establishes any connection. | Local RADIUS server (802.1X EAP termination; EAP types TLS, TTLS, PEAP, MD5, GTC, MSCHAPv2, FAST, TEAP); Machine authentication with RBAC based on Active Directory computer groups | GUI: Network > RADIUS > Configure Local Server | 7.2.0 |
| AAA | `SRG-APP-000516-AAA-000440` | AAA Services used for 802.1x must be configured to use secure Extensible Authentication Protocol (EAP), such as EAP-TLS, EAP-TTLS, and PEAP. | Local RADIUS server (802.1X EAP termination; EAP types TLS, TTLS, PEAP, MD5, GTC, MSCHAPv2, FAST, TEAP); TEAP for RADIUS clients and TLS 1.3 in the Local RADIUS Server; TEAP with multiple inner authentication methods (user and machine) | GUI: Network > RADIUS > Configure Local Server | 7.2.0 |
| AAA | `SRG-APP-000516-AAA-000640` | AAA Services must be configured to use a unique shared secret for communication (i.e. RADIUS, TACACS+) with clients requesting authentication services. | RADIUS secrets and RADIUS mode per modeled device; Require Message-Authenticator (BlastRADIUS protection); RADIUS over TLS (RadSec) for the Local RADIUS Server | GUI: Network > Inventory > Device configuration > Model configuration | 7.2.0 |
| AAA | `SRG-APP-000516-AAA-000660` | AAA Services must be configured to place non-authenticated network access requests in the Unauthorized VLAN or the Guest VLAN with limited access. | Rogue host detection and isolation of unknown devices (registration, isolation, and dead-end VLANs); Guest and contractor accounts, templates, and sponsors | GUI: Network > Logical networks | 7.2.0 |
| AAA | `SRG-APP-000875-AAA-000220` | For public key-based authentication, AAA Services must be configured to implement a local cache of revocation data to support path discovery and validation. | OCSP certificate revocation checking for EAP-TLS | GUI: Network > RADIUS > Configure Local Server | 7.2.0 |
| AAA | `SRG-APP-000910-AAA-000230` | AAA Services must be configured to include only approved trust anchors in trust stores or certificate stores managed by the organization. | Certificate management (server certificates for Admin UI, portal, agent, and RADIUS; trusted certificates) | GUI: System > Certificate management | 7.2.0 |

### Alignment summary

| STIG | Same requirement | Equivalent setting | Partial | Not supported | Not applicable | By procedure | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ISE-NDM (V2R4) | 16 | 15 | 15 | 3 | 1 | 1 | 51 |
| ISE-NAC (V2R4) | 22 | 0 | 5 | 3 | 0 | 0 | 30 |
| **Total** | **38** | **15** | **20** | **6** | **1** | **1** | **81** |

FortiNAC meets 53 of the 81 ISE rules' requirements with
a setting (38 through the feature Chapter 25 maps and 15 through
another setting), 20 only in part, and 6 not at all; 1
rule targets an ISE function FortiNAC does not have, and 1 is met by
procedure. Of the 30 NAC rules, FortiNAC meets 22 with the
feature Chapter 25 maps. The main differences:

- **Where the ISE STIG is stricter, or ISE can do more.** ISE has a FIPS
  mode, a pre-login banner, a limit on concurrent administrator sessions,
  SYN-flood and rate limits, buffering of TCP and secure syslog while a
  server is down, an alarm when log collection fails, and, from 3.5, AES
  authentication of NTP. FortiNAC-F documents none of these, so
  `CSCO-NM-000010`, `CSCO-NM-000120`, `CSCO-NM-000550`, `CSCO-NC-000230`,
  `CSCO-NC-000240`, and `CSCO-NC-000290` are Not supported, and the FIPS
  rows are Partial. ISE also enforces password length and complexity for
  administrators in a policy; FortiNAC enforces complexity only for CLI and
  SSH passwords.
- **Where FortiNAC is stricter.** FortiNAC administrator profiles and the
  CLI accept a 5-minute idle timeout, which meets the NDM SRG; ISE cannot go
  below 6 minutes. FortiNAC's Persistent Agent asks the user to acknowledge a
  VLAN change (7.4.0 and later), which goes beyond the ISE rule's message
  before remediation.
- **Posture checks.** FortiNAC scans check anti-virus products and operating
  systems directly, but host firewalls and host IDS/IPS only through custom
  scans that you write (`CSCO-NC-000040` and `CSCO-NC-000060`, Partial, as
  Chapter 25 records); ISE has a Firewall condition and checks other
  security software with Service or Application conditions.
- **Log failure handling.** Both products send events to two log servers,
  but only ISE alarms on a log collection error and buffers TCP and secure
  syslog. On FortiNAC, map disk space events to alarms and alert on missing
  events at the log server or SIEM.

### Collecting evidence

In a mixed estate, keep one checklist row per ISE rule for each NAC system,
with the SRG ID and the alignment category from the table, and attach each
platform's evidence:

- **Cisco ISE:** the release and the CLI settings, from each node:

  ISE: `show version`

  ISE: `show running-config`

  Add screenshots or exports of the GUI pages in the ISE command column,
  above all *Administration > System > Admin Access* (settings,
  authentication, and administrators), *Administration > System > Logging*,
  *Administration > System > Settings*, *Work Centers > Network Access >
  Policy Sets*, and *Work Centers > Posture > Posture Policy*.
- **FortiNAC-F:** the release, and the settings in the FortiNAC column, as
  Chapter 25 describes:

  FortiNAC: `get system status`

  Add screenshots or exports of the panes in the FortiNAC command column,
  the admin auditing log, and the events from the log receivers.
- **For every Partial and Not supported row:** the open finding, its
  mitigation, and its approval, recorded against the SRG ID.

Keep the FortiNAC-only requirements (the second table) on the FortiNAC
checklist as well (Chapter 03 describes SRG-based checklists).

## Validation and Troubleshooting

- **An ISE rule seems to have no row.** Every one of the 81 rules
  has a row; the build script fails if one is missing. Search for the rule
  ID, not the title.
- **An ISE command from a fix text is rejected.** Check *ISE fix text
  corrections* and the release: `password-policy` options are entered in its
  submode, `write memory` does not exist, and `aes256` NTP keys need 3.5. Use
  `?` on the CLI.
- **A GUI path from a fix text is not there.** The fix texts mix paths from
  several ISE releases. Find the page by the field name in the 3.5
  Administrator Guide, or use the menu search in the ISE GUI.
- **The ISE idle timeout will not accept 5.** The GUI range is 6 to 100
  minutes; set 6 and record it, as the ISE STIG does.
- **An assessor asks for the FortiNAC STIG rule.** There is none; show the
  SRG ID in the table and the Chapter 25 mapping, and record the finding on
  an SRG-based checklist.

## Security and Best Practices

- Treat the ISE STIG rules as the checklist for every NAC system, add the
  FortiNAC-only requirements, and record each FortiNAC finding against the
  SRG requirement.
- On both platforms, end idle administrator sessions after 5 minutes where
  the product allows (6 on ISE), lock accounts after three failed logons,
  authenticate administrators through a directory, and allow management only
  over HTTPS and SSH from management hosts.
- Send logs to two log servers over TCP or TLS, and alert on missing events
  at the log server.
- Deny or restrict access by default, keep unknown and non-compliant
  endpoints in restricted networks, and approve every posture exception in
  the SSP.
- Record every Partial and Not supported row as an open finding with its
  mitigation, and review the crosswalk whenever DISA updates the ISE STIG
  package or an SRG, or a new ISE or FortiNAC-F release changes the
  commands.

## References and Knowledge Checks

**References:**

- DISA Cisco ISE NDM STIG V2R4 and NAC STIG V2R4, with the ISE STIG
  overview (`U_Cisco_ISE_Y26M07_STIG.zip`), the Network Device Management
  SRG V5R5, and the AAA Services SRG V2R3, from the October 2026 STIG Library
  Compilation.
- Cisco, *Cisco Identity Services Engine Administrator Guide, Release 3.5*,
  and *Cisco Identity Services Engine CLI Reference Guide, Release 3.5* (with
  the 3.1 to 3.4 CLI References for keyword history).
- Fortinet, *FortiNAC-F 7.6.0 CLI Reference Guide* and *FortiNAC-F 7.6.0
  Administration Guide*.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (how STIGs are built from SRGs, and SRG-based assessment),
  [Chapter 07](07-network-device-stigs-management-routing-and-filtering.md)
  (network device STIGs by plane),
  [Chapter 25](25-fortinac-feature-version-and-srg-map.md) (the FortiNAC
  feature and SRG map, source of the FortiNAC commands, versions, and the
  ISE NAC mapping),
  [Chapter 31](31-cisco-products-stigs-and-srg-mapping.md) (the Cisco STIG
  packages, including the ISE STIGs),
  [Chapter 33](33-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk.md)
  (the FortiSwitch and Cisco Catalyst switch crosswalk), and
  [Chapter 34](34-cisco-asa-and-fortigate-stig-crosswalk.md) (the Cisco ASA
  and FortiGate crosswalk).

**Knowledge checks:**

1. FortiNAC has no STIG. Against what is a FortiNAC finding for an ISE NAC
   rule recorded?
2. Why does Chapter 25 use the Cisco ISE NAC STIG at all, and what does it
   carry over to FortiNAC?
3. Why does the ISE NDM STIG ask for a six-minute idle timeout when the NDM
   SRG asks for five, and what should FortiNAC use?
4. Why does `ntp authentication-key 1 md5 plain <KEY>` from the ISE fix text
   not meet `CSCO-NC-000290`, and which ISE release can meet it?
5. Why do the AAA Services requirements appear only in the second table?
6. Name two ISE rules that FortiNAC cannot meet, and a mitigation for each.
7. How does FortiNAC check a host firewall, and why is that row Partial?

## Summary and Completion Checklist

Cisco ISE has an NDM and a NAC STIG; FortiNAC-F has none, and Chapter 25
maps it to the NDM and AAA Services SRGs and to the ISE NAC rules as the
pattern for network access control. This chapter aligns all 81 ISE
rules (51 NDM and 30 NAC) with the FortiNAC setting and
command that meet the same requirement: 38 through the feature Chapter
25 maps, 15 through another setting, 20 only in part, and 6
not at all. It also lists the 38 FortiNAC requirements that no ISE
rule covers. Every ISE CLI command was checked by script against the ISE 3.5
CLI Reference (with the fix text errors corrected), every ISE GUI path and
label against the ISE 3.5 Administrator Guide, and every FortiNAC command
against the FortiNAC-F 7.6.0 guides.

- [ ] Can explain why a FortiNAC finding is recorded against an SRG
  requirement, with the ISE rule as the reference.
- [ ] Can find an ISE rule in the crosswalk and configure the FortiNAC
  setting that meets the same requirement.
- [ ] Can correct the ISE fix texts that ISE 3.5 rejects or no longer
  documents.
- [ ] Can add the FortiNAC-only requirements, including the AAA Services
  requirements, to a FortiNAC checklist.
- [ ] Can name the ISE capabilities FortiNAC lacks and record them as open
  findings with mitigations.
