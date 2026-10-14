# Chapter 33: FortiSwitch and Cisco Catalyst Switch STIG Crosswalk

## Learning Objectives

- Explain why a FortiSwitch is assessed against SRGs and why there is no
  FortiSwitch STIG to compare with the Cisco switch STIGs.
- Align a Cisco IOS XE Switch STIG rule with the FortiSwitch setting that
  meets the same SRG requirement.
- Use the Cisco IOS XE Switch STIG rules as a working checklist for a
  FortiSwitch, and see where FortiSwitch meets, partly meets, or cannot
  meet each rule.
- Tell the six alignment categories apart and record each one correctly on
  an SRG-based checklist.
- Find the FortiSwitch requirements that no Cisco switch rule covers, so
  that the checklist covers both directions.
- Account for FortiLink-managed switches, where the FortiSwitch side of the
  crosswalk is configured on the FortiGate.

## Theory and Architecture

**DISA publishes no FortiSwitch STIG.** A FortiSwitch in a DoD network is
assessed directly against the SRGs that match its functions: the Layer 2
Switch, Network Device Management (NDM), Router, and AAA Services SRGs, as
[Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) maps them.
Cisco Catalyst switches running IOS XE do have STIGs: the Cisco IOS XE
Switch STIG package (C-NDM V3R6, C-L2S V3R2, and C-RTR V3R4, 152
rules in all; [Chapter 31](31-cisco-products-stigs-and-srg-mapping.md) and
[Chapter 32](32-cisco-catalyst-switch-feature-version-and-stig-map.md)).
Those STIGs were written from the same SRGs: every Cisco rule names the SRG
requirement it implements.

This chapter therefore does not compare two STIGs. It aligns the two
platforms **through the SRG requirement each Cisco rule implements**: for
every one of the 152 Cisco rules, it gives the FortiSwitch setting
and FortiSwitchOS command that meet the same requirement, and says how
closely they meet it. An organization that runs both vendors can use the
Cisco rules as the checklist for its FortiSwitches, and see at a glance
where FortiSwitch differs.

### Why this is a crosswalk, not a STIG comparison

A STIG is a vendor-specific implementation of one or more SRGs (Chapter 03).
Its rules carry their own check and fix text, and an assessor records a
finding against the rule. With no FortiSwitch STIG, there is no FortiSwitch
rule to record a finding against: the assessor records it against the SRG
requirement itself, on an SRG-based checklist. A crosswalk keeps that
distinction:

- **The Cisco rule is a reference, not a requirement for FortiSwitch.** A
  FortiSwitch is never "compliant with `CISC-ND-000720`". It meets
  `SRG-APP-000190-NDM-000267`, the requirement that rule implements, and the
  FortiSwitch finding is recorded against that SRG ID.
- **The SRG ID is the join key.** Two settings align because they implement
  the same requirement, not because they look alike. Cisco loop guard and
  FortiSwitch STP loop protection align because both implement
  `SRG-NET-000362-L2S-000023`.
- **The Cisco package covers only part of the SRGs.** The 152 Cisco
  rules cite 150 distinct SRG IDs. Chapter 11 maps FortiSwitch features
  to 60 requirement IDs, of which 26 have no Cisco switch
  rule at all, including all seven AAA Services SRG requirements (the Cisco
  switch STIGs do not use that SRG). The second table in this chapter lists
  them.

### How the rules are aligned

Each Cisco rule was aligned in four steps:

1. **Take the SRG ID the rule implements.** The rule ID, severity, SRG ID,
   and title come from the Cisco IOS XE Switch STIG XCCDF files
   (`U_Cisco_IOS-XE_Switch_Y26M04_STIG.zip`).
2. **Look for the same SRG ID in Chapter 11.** 35 of the
   152 rules cite an SRG ID that Chapter 11 also maps to a
   FortiSwitch feature. These are exact matches: the same requirement, met
   by the feature Chapter 11 names.
3. **For the rest, read the requirement and find the setting.** The
   requirement text comes from the SRG XCCDF files (Layer 2 Switch V3R4, NDM
   V5R5, Router V5R2, and AAA Services V2R3). The FortiSwitch setting that
   meets it was found in the **FortiSwitchOS 8.0.0 CLI Reference**. Where the
   reference has no such setting, the row says so.
4. **Judge how well the setting meets the requirement**, and assign one of
   the alignment categories below.

Two cautions apply to the alignment data:

- **CCIs were not used to match requirements.** Many SRG requirements share
  the catch-all CCI-000366 ("security configuration settings"), so a CCI
  match often links unrelated requirements. Every alignment rests on the
  SRG ID or on the requirement text.
- **2 Cisco rules cite SRG IDs that are no longer in the
  current NDM SRG.** `CISC-ND-001030` cites `SRG-APP-000373-NDM-000298`
  (redundant time sources) and `CISC-ND-001470` cites
  `SRG-APP-000516-NDM-000351` (supported release); neither ID appears in NDM
  SRG V5R5. Their rows name the current requirement that Chapter 11 maps for
  the same topic (`SRG-APP-000920-NDM-000320` and
  `SRG-APP-001035-NDM-000340`).

### Where the commands come from

- **Cisco IOS XE commands come from Chapter 32**, where every command was
  checked against the IOS XE 26.x documentation and the fix texts with
  errors were corrected. Where a Chapter 32 command configures several rules
  at once (the BGP, MPLS, multicast, and perimeter ACL blocks), the
  crosswalk shows only the statements that belong to the rule, keeping the
  mode commands they need. The build script checks that every Cisco
  statement in the table appears in Chapter 32 for the same rule.
- **FortiSwitchOS commands come from the FortiSwitchOS 8.0.0 CLI
  Reference.** A script checked every command against it: each `config`
  path must be a documented syntax block, each nested `config` a documented
  sub-table, each `set` option an option of that path, and each literal
  value one of the documented values or inside the documented range. The
  script was itself tested with deliberately wrong commands (a misspelled
  path, a Cisco-style option, `enable` where FortiSwitchOS wants `enabled`,
  an out-of-range threshold, an undocumented protocol) and caught all of
  them. Commands starting with **FortiGate:** are FortiLink managed-mode
  commands, checked the same way against the **FortiOS 8.0.1 CLI
  Reference**.
- Read the command cells as in Chapters 11 and 32: each pair of backticks is
  one block, statements are separated by `;` to fit in a table cell (on the
  CLI, enter each on its own line), and values in `<ANGLE_BRACKETS>` are
  placeholders for your own names, addresses, and keys. FortiSwitchOS
  commands are standalone switch syntax; on a FortiLink-managed switch, make
  the change on the FortiGate instead (see *Alignment summary*).
- A dash (**—**) in the FortiSwitchOS column means the 8.0.0 CLI Reference
  has no setting for the requirement. The setting column says why.

### Where the version columns come from

The crosswalk table has a version column for each platform, so that you
can see which software release a setting needs:

- **IOS XE version** is the "First listed / Introduced (IOS XE)" entry of
  the Chapter 32 feature map row that supplies the Cisco command shown.
  Chapter 32 built that column from the Catalyst 9300 release notes for
  IOS XE 17.1.x through 26.2.x. Where the crosswalk shows only some
  statements of a Chapter 32 command, the version is that of the first
  Chapter 32 row for the rule that contains all of them. `17.1.1 or
  earlier` means the feature predates the oldest release notes Chapter 32
  used; it is not a claim that the feature appeared in 17.1.1.
- **FortiSwitchOS version** is the "First listed (FortiSwitchOS)" entry of
  the Chapter 11 feature that the FortiSwitch setting uses, with the feature
  name in parentheses. Chapter 11 built that column from every FortiSwitchOS
  feature matrix from 7.0.0 to 8.0.0, so it gives the first release whose
  feature matrix *lists* the feature, which can be later than the release
  that introduced it. `7.0.0 or earlier` means the feature is in the oldest
  matrix Chapter 11 used; entries such as `7.6.4 and later` give the first
  matrix that lists it.
- **Not in the feature matrix (8.0.0 CLI Reference)** marks a FortiSwitchOS
  setting that the feature matrices do not list as a feature, such as the
  idle timeout, lockout, banner, or password policy. These settings come
  only from the 8.0.0 CLI Reference, so no first release is given; check
  the CLI Reference for your release.
- A dash (**—**) in the FortiSwitchOS version column means the row has no
  FortiSwitchOS command: the rule is Not supported or Not applicable, or it
  is met by procedure with nothing to configure.

### Alignment categories

Every row has one of six categories:

| Category | Meaning |
| --- | --- |
| Same requirement | Chapter 11 maps a FortiSwitch feature to the same SRG ID, and the feature meets the requirement. |
| Equivalent setting | A FortiSwitch setting meets the requirement, although Chapter 11 did not map it to this SRG ID. |
| Partial | FortiSwitch meets part of the requirement. The setting column says what is missing. |
| Not supported | FortiSwitch has no such capability (for example MPLS, VPLS, or UDLD), so it cannot meet the rule or take the role the rule secures. |
| Not applicable | The rule targets a component, role, or protocol that FortiSwitch does not have or take (an auxiliary port, a PIM rendezvous point, MSDP), so there is nothing to secure. |
| By procedure | The requirement is met by a process rather than a setting, on both platforms (running a supported release, address planning). |

**Partial**, **Not supported**, and **Not applicable** take precedence over
**Same requirement**: where Chapter 11 maps the same SRG ID but the
FortiSwitch feature does not fully meet it (MD5-only routing protocol
authentication, for example), the row is Partial and its setting cell notes
that Chapter 11 maps the requirement.

## Design Considerations

- **Use the Cisco rules as the checklist, but record against the SRG.** In
  a mixed estate the Cisco rules give one list of what to check on every
  switch. For a FortiSwitch, the finding goes on the SRG-based checklist
  under the SRG ID in the table, with the alignment category and the
  FortiSwitch evidence.
- **Decide each switch's role first.** As in Chapter 32, the C-RTR rules
  depend on the role: perimeter rules apply only to a switch at the enclave
  boundary, PE and P rules only to an MPLS provider switch, and multicast
  rules only where the switch routes multicast. A FortiSwitch cannot be an
  MPLS PE or P switch at all, and it should rarely be the perimeter device:
  its ACLs cannot meet several perimeter rules, and a FortiGate is the
  better perimeter (Chapter 30).
- **Use the same organization-defined values on both platforms.** The
  session limit, idle timeout, lockout values, log servers, time sources,
  and password policy should match across vendors, so that one set of
  values satisfies the requirement everywhere.
- **Plan for FortiLink-managed mode.** Most FortiSwitches are managed by a
  FortiGate. The FortiSwitch side of each row is then configured under the
  FortiGate's `config switch-controller` tree, and the evidence comes from
  the FortiGate.
- **Check the license.** FortiSwitch OSPF, BGP, IS-IS, VRF, and multicast
  routing need the Advanced Features license (Chapter 11). Without it, the
  routing rows describe capabilities the switch does not have, and the
  corresponding RTR rules do not apply.
- **Accept the gaps deliberately.** The Partial and Not supported rows are
  real gaps, not documentation gaps. Record each as an open finding with its
  mitigation, or keep the function on a platform that meets the requirement.

## Implementation and Automation

### The crosswalk table

One row per Cisco IOS XE Switch STIG rule: 42 C-NDM rules, then
22 C-L2S rules, then 88 C-RTR rules. Severity is the Cisco
rule's category. The Requirement column summarizes what the rule requires in
plain language; the SRG ID links it to the requirement text. The command
columns follow the conventions in *Where the commands come from*, and the
version columns those in *Where the version columns come from*.

[Download the crosswalk as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/33-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk-crosswalk.csv) (152 rows).

| Cisco rule | Severity | SRG ID | Requirement | Cisco IOS XE command | IOS XE version | FortiSwitch setting | FortiSwitchOS command | FortiSwitchOS version | Alignment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C-NDM `CISC-ND-000010` | CAT II | `SRG-APP-000001-NDM-000200` | Limit concurrent management sessions to an organization-defined number | `ip http max-connections 2; line vty 0 1; transport input ssh; line vty 2 31; transport input none` | 17.1.1 or earlier | Concurrent administrator login control: stops one administrator name from logging in from two IP addresses at once; FortiSwitchOS has no setting for a maximum number of management sessions | `config system global; set admin-concurrent enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Partial |
| C-NDM `CISC-ND-000090` | CAT II | `SRG-APP-000026-NDM-000208` | Audit the creation of accounts | `logging userinfo; archive; log config; logging enable; logging size 1000; notify syslog contenttype plaintext; hidekeys` | 17.1.1 or earlier | System event logging, which records configuration changes such as new administrator accounts; send the logs off the switch (`CISC-ND-001450`) | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000100` | CAT II | `SRG-APP-000027-NDM-000209` | Audit the modification of accounts | `logging userinfo; archive; log config; logging enable; logging size 1000; notify syslog contenttype plaintext; hidekeys` | 17.1.1 or earlier | System event logging of configuration changes to administrator accounts | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000110` | CAT II | `SRG-APP-000028-NDM-000210` | Audit the disabling of accounts | `logging userinfo; archive; log config; logging enable; logging size 1000; notify syslog contenttype plaintext; hidekeys` | 17.1.1 or earlier | System event logging of configuration changes to administrator accounts | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000120` | CAT II | `SRG-APP-000029-NDM-000211` | Audit the removal of accounts | `logging userinfo; archive; log config; logging enable; logging size 1000; notify syslog contenttype plaintext; hidekeys` | 17.1.1 or earlier | System event logging of configuration changes to administrator accounts | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000140` | CAT II | `SRG-APP-000038-NDM-000213` | Allow management access only from authorized networks and over approved protocols | `ip access-list standard MANAGEMENT_NET; permit <MGMT_SUBNET> <WILDCARD>; exit; line vty 0 31; transport input ssh; access-class MANAGEMENT_NET in` | 17.1.1 or earlier | Trusted hosts on each administrator account, and management protocols allowed only on a dedicated management interface | `config system admin; edit <ADMIN>; set trusthost1 <MGMT_SUBNET> <MASK>; end` `config system interface; edit <MGMT_SVI>; set allowaccess https ssh; end` | 7.6.4 and later (SVI) | Same requirement |
| C-NDM `CISC-ND-000150` | CAT II | `SRG-APP-000065-NDM-000214` | Lock an account for 15 minutes after three failed logons | `login block-for 900 attempts 3 within 120` | 17.1.1 or earlier | Administrator lockout; the default threshold is already 3 attempts, but the default lockout is only 60 seconds | `config system global; set admin-lockout-threshold 3; set admin-lockout-duration 900; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000160` | CAT II | `SRG-APP-000068-NDM-000215` | Show the DoD Notice and Consent Banner before logon | `banner login # <DOD_NOTICE_AND_CONSENT_BANNER_TEXT> #` | 17.1.1 or earlier | Pre-login banner | `config system global; set pre-login-banner "<DOD_NOTICE_AND_CONSENT_BANNER_TEXT>"; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000210` | CAT II | `SRG-APP-000080-NDM-000220` | Audit all administrator activity | `logging userinfo; archive; log config; logging enable; logging size 1000; notify syslog contenttype plaintext; hidekeys` | 17.1.1 or earlier | System and user event logging (configuration changes and logons) | `config log eventfilter; set event enable; set system enable; set user enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000280` | CAT II | `SRG-APP-000096-NDM-000226` | Record the date and time of each audited event | `service timestamps log datetime localtime` | 17.1.1 or earlier | Log records take their time stamp from the system clock; set the time zone and keep the clock synchronized (`CISC-ND-001030`) | `config system global; set timezone <TIMEZONE_NUMBER>; end` `config system ntp; set ntpsync enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000290` | CAT II | `SRG-APP-000097-NDM-000227` | Record where each audited event occurred | `ip access-list extended <ACL_NAME>; deny ip any any log-input` | 17.1.1 or earlier | Event logs identify the switch by its host name; ACL matches can be counted but not logged, so there is no equivalent of the Cisco `log-input` keyword | `config system global; set hostname <HOSTNAME>; end` `config switch acl ingress; edit <ID>; config action; set count enable; end; end` | Not in the feature matrix (8.0.0 CLI Reference) | Partial |
| C-NDM `CISC-ND-000330` | CAT II | `SRG-APP-000101-NDM-000231` | Log the full text of privileged commands | `logging userinfo; archive; log config; logging enable; logging size 1000; notify syslog contenttype plaintext; hidekeys` | 17.1.1 or earlier | System event logging records configuration changes; the 8.0.0 CLI Reference documents no setting that logs the full text of every command entered | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Partial |
| C-NDM `CISC-ND-000380` | CAT II | `SRG-APP-000119-NDM-000236` | Protect audit information from unauthorized modification | `file privilege 15` | 17.1.1 or earlier | Access profiles: give log access (`loggrp`) read-only or none to every profile except the auditors' | `config system accprofile; edit <PROFILE>; set loggrp read; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000390` | CAT II | `SRG-APP-000120-NDM-000237` | Protect audit information from unauthorized deletion | `file privilege 15` | 17.1.1 or earlier | Access profiles: only profiles with read-write log access (`loggrp`) can delete logs | `config system accprofile; edit <PROFILE>; set loggrp read; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000460` | CAT II | `SRG-APP-000133-NDM-000244` | Limit who can change the installed software | `file privilege 15` | 17.1.1 or earlier | Access profiles: grant critical system maintenance (`mntgrp`) and system (`sysgrp`) write access only to the administrators allowed to change firmware | `config system accprofile; edit <PROFILE>; set mntgrp none; set sysgrp read; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000470` | CAT I | `SRG-APP-000142-NDM-000245` | Disable unnecessary and nonsecure functions and services | `no boot network; no ip bootp server; no ip dns server; no ip identd; no ip finger; no ip http server; no ip rcmd rcp-enable; no ip rcmd rsh-enable; no service config; no service finger; no service tcp-small-servers; no service udp-small-servers; no service pad; no service call-home` | 17.1.1 or earlier | Allow only HTTPS and SSH for management (no HTTP or Telnet), and keep SSH version 1 compatibility off | `config system interface; edit <MGMT>; set allowaccess https ssh; end` `config system global; set admin-ssh-v1 disable; end` | 7.0.0 or earlier (HTTP REST APIs for configuration and monitoring) | Same requirement |
| C-NDM `CISC-ND-000490` | CAT II | `SRG-APP-000148-NDM-000346` | Keep only one local account, as the account of last resort | `username <USERNAME> privilege <PRIVILEGE_LEVEL> common-criteria-policy PASSWORD_POLICY secret <PASSWORD>; aaa authentication login default group RADIUS_GROUP local` | 17.1.1 or earlier | One local administrator account, with all others authenticated remotely; local logons can be refused while the authentication server is reachable | `config system global; set admin-restrict-local enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000550` | CAT II | `SRG-APP-000164-NDM-000252` | Require passwords of at least 15 characters | `aaa common-criteria policy PASSWORD_POLICY; min-length 15` | 17.1.1 or earlier | Password policy for administrator passwords (minimum length 8 to 32) | `config system password-policy; set status enable; set apply-to admin-password; set minimum-length 15; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000570` | CAT II | `SRG-APP-000166-NDM-000254` | Require at least one uppercase character in passwords | `aaa common-criteria policy PASSWORD_POLICY; upper-case 1` | 17.1.1 or earlier | Password policy | `config system password-policy; set status enable; set min-upper-case-letter 1; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000580` | CAT II | `SRG-APP-000167-NDM-000255` | Require at least one lowercase character in passwords | `aaa common-criteria policy PASSWORD_POLICY; lower-case 1` | 17.1.1 or earlier | Password policy | `config system password-policy; set status enable; set min-lower-case-letter 1; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000590` | CAT II | `SRG-APP-000168-NDM-000256` | Require at least one numeric character in passwords | `aaa common-criteria policy PASSWORD_POLICY; numeric-count 1` | 17.1.1 or earlier | Password policy | `config system password-policy; set status enable; set min-number 1; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000600` | CAT II | `SRG-APP-000169-NDM-000257` | Require at least one special character in passwords | `aaa common-criteria policy PASSWORD_POLICY; special-case 1` | 17.1.1 or earlier | Password policy | `config system password-policy; set status enable; set min-non-alphanumeric 1; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000610` | CAT II | `SRG-APP-000170-NDM-000329` | Change at least eight character positions when a password changes | `aaa common-criteria policy PASSWORD_POLICY; char-change 8` | 17.1.1 or earlier | Password policy can require only four changed characters (`change-4-characters`), not eight | `config system password-policy; set status enable; set change-4-characters enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Partial |
| C-NDM `CISC-ND-000620` | CAT I | `SRG-APP-000171-NDM-000258` | Store only cryptographic representations (hashes) of passwords | `service password-encryption; enable secret <PASSWORD>` | 17.1.1 or earlier | Administrator passwords are stored hashed; select PBKDF2 with the higher iteration count for new passwords | `config system global; set admin-password-hash pbkdf2-high; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000720` | CAT I | `SRG-APP-000190-NDM-000267` | End management sessions after five minutes of inactivity | `line console 0; exec-timeout 5 0; line vty 0 31; exec-timeout 5 0; exit; ip http timeout-policy idle 300 life <SECONDS> requests <NUMBER>` | 17.1.1 or earlier | Administrator idle timeout; the FortiSwitchOS default is already 5 minutes | `config system global; set admintimeout 5; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000880` | CAT II | `SRG-APP-000319-NDM-000283` | Audit the enabling of accounts | `logging userinfo; archive; log config; logging enable; logging size 1000; notify syslog contenttype plaintext; hidekeys` | 17.1.1 or earlier | System event logging of configuration changes to administrator accounts | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-000980` | CAT II | `SRG-APP-000357-NDM-000293` | Allocate local audit record storage as the organization requires | `logging buffered <BUFFER_SIZE> informational` | 17.1.1 or earlier | Local event log on flash, overwriting the oldest records, with fill-level warnings | `config log disk setting; set status enable; set diskfull overwrite; set full-first-warning-threshold 75; end` | 7.2.0 and later (Save event log in flash memory) | Same requirement |
| C-NDM `CISC-ND-001000` | CAT II | `SRG-APP-000360-NDM-000295` | Alert on audit failures | `logging host <SYSLOG_SERVER_1>; logging host <SYSLOG_SERVER_2>; logging trap critical` | 17.1.1 or earlier | The log disk raises warnings at three fill levels; there is no dedicated alert when syslog delivery fails | `config log disk setting; set full-first-warning-threshold <PERCENT>; set full-second-warning-threshold <PERCENT>; set full-final-warning-threshold <PERCENT>; end` | 7.2.0 and later (Save event log in flash memory) | Partial |
| C-NDM `CISC-ND-001030` | CAT II | `SRG-APP-000373-NDM-000298` | Synchronize the clock with two redundant authoritative time sources | `ntp authenticate; ntp authentication-key 1 hmac-sha2-256 <KEY>; ntp trusted-key 1; ntp server <NTP_SERVER_1> key 1; ntp server <NTP_SERVER_2> key 1` | 17.1.1 or earlier | Two NTP servers (the rule's SRG ID is not in NDM SRG V5R5; Chapter 11 maps NTP to the current requirement `SRG-APP-000920-NDM-000320`) | `config system ntp; set ntpsync enable; config ntpserver; edit 1; set server <NTP_SERVER_1>; next; edit 2; set server <NTP_SERVER_2>; end; end` | 7.6.2 and later (NTP server (IPv4/IPv6)) | Equivalent setting |
| C-NDM `CISC-ND-001130` | CAT II | `SRG-APP-000395-NDM-000310` | Authenticate SNMP messages with a FIPS-validated HMAC | `snmp-server group V3GROUP v3 priv read V3READ write V3WRITE; snmp-server user V3USER V3GROUP v3 auth sha <AUTH_PASSWORD> priv aes 256 <PRIV_PASSWORD>; snmp-server host <NMS_IP_ADDRESS> version 3 priv V3USER` | 17.1.1 or earlier | SNMPv3 user with authentication and privacy, SHA-256 authentication | `config system snmp user; edit <USER>; set security-level auth-priv; set auth-proto sha256; set auth-pwd <AUTH_PASSWORD>; end` | 7.0.0 or earlier (Support for switch SNMP OID) | Same requirement |
| C-NDM `CISC-ND-001140` | CAT II | `SRG-APP-000395-NDM-000310` | Encrypt SNMP messages with a FIPS-approved algorithm | `snmp-server group V3GROUP v3 priv read V3READ write V3WRITE; snmp-server user V3USER V3GROUP v3 auth sha <AUTH_PASSWORD> priv aes 256 <PRIV_PASSWORD>; snmp-server host <NMS_IP_ADDRESS> version 3 priv V3USER` | 17.1.1 or earlier | SNMPv3 user with authentication and privacy, AES-256 privacy | `config system snmp user; edit <USER>; set security-level auth-priv; set priv-proto aes256; set priv-pwd <PRIV_PASSWORD>; end` | 7.0.0 or earlier (Support for switch SNMP OID) | Same requirement |
| C-NDM `CISC-ND-001150` | CAT II | `SRG-APP-000395-NDM-000347` | Authenticate NTP sources cryptographically | `ntp authenticate; ntp authentication-key 1 hmac-sha2-256 <KEY>; ntp trusted-key 1; ntp server <NTP_SERVER_1> key 1; ntp server <NTP_SERVER_2> key 1` | 17.1.1 or earlier | NTP authentication; FortiSwitchOS uses SHA-1 with NTPv4 (MD5 with NTPv3), where the Cisco rule uses HMAC-SHA-256 | `config system ntp; set ntpsync enable; set authentication enable; config ntpserver; edit 1; set server <NTP_IP>; set authentication enable; set key-id <ID>; set key <KEY>; end; end` | 7.6.2 and later (NTP server (IPv4/IPv6)) | Same requirement |
| C-NDM `CISC-ND-001200` | CAT I | `SRG-APP-000411-NDM-000330` | Protect remote maintenance sessions with a FIPS-validated HMAC | `ip ssh version 2; ip ssh server algorithm mac hmac-sha2-512 hmac-sha2-256; ip ssh server algorithm encryption aes256-ctr aes192-ctr aes128-ctr` | 17.1.1 or earlier | FIPS-CC mode and strong cryptography for SSH and HTTPS; FortiSwitchOS has no per-algorithm SSH MAC or cipher list | `config system security; set mode fips-cc; end` `config system global; set strong-crypto enable; end` | 7.6.4 and later (FIPS 140-3 (Level 1) and CC support) | Same requirement |
| C-NDM `CISC-ND-001210` | CAT I | `SRG-APP-000412-NDM-000331` | Encrypt remote maintenance sessions | `ip ssh version 2; ip ssh server algorithm mac hmac-sha2-512 hmac-sha2-256; ip ssh server algorithm encryption aes256-ctr aes192-ctr aes128-ctr` | 17.1.1 or earlier | FIPS-CC mode, strong cryptography, and TLS 1.2 for HTTPS (TLS 1.3 is not supported in FIPS-CC mode) | `config system security; set mode fips-cc; end` `config system global; set strong-crypto enable; end` `config system web; set https-ssl-versions tlsv1-2; end` | 7.6.4 and later (FIPS 140-3 (Level 1) and CC support) | Same requirement |
| C-NDM `CISC-ND-001250` | CAT II | `SRG-APP-000499-NDM-000319` | Log the deletion of administrator privileges | `logging userinfo; archive; log config; logging enable; logging size 1000; notify syslog contenttype plaintext; hidekeys` | 17.1.1 or earlier | System event logging of configuration changes to administrator accounts and access profiles | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-001260` | CAT II | `SRG-APP-000503-NDM-000320` | Log successful and unsuccessful logons | `login on-success log; login on-failure log` | 17.1.1 or earlier | System and user event logging, which records administrator logons | `config log eventfilter; set event enable; set system enable; set user enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-001270` | CAT II | `SRG-APP-000504-NDM-000321` | Log privileged activities | `logging userinfo; archive; log config; logging enable; logging size 1000; notify syslog contenttype plaintext; hidekeys` | 17.1.1 or earlier | System event logging of configuration changes | `config log eventfilter; set event enable; set system enable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-001370` | CAT I | `SRG-APP-000516-NDM-000336` | Use at least two authentication servers for administrator logons | `aaa new-model; radius server RADIUS1; address ipv4 <RADIUS_1_IP> auth-port 1812 acct-port 1813; key <KEY>; exit; radius server RADIUS2; address ipv4 <RADIUS_2_IP> auth-port 1812 acct-port 1813; key <KEY>; exit; aaa group server radius RADIUS_GROUP; server name RADIUS1; server name RADIUS2; exit; aaa authentication login CONSOLE group RADIUS_GROUP local; aaa authentication login LOGIN_AUTHENTICATION group RADIUS_GROUP local; line vty 0 31; login authentication LOGIN_AUTHENTICATION; line console 0; login authentication CONSOLE; exit; ip http authentication aaa login-authentication LOGIN_AUTHENTICATION` | 17.1.1 or earlier | Two RADIUS (or TACACS+) server entries in the group that administrator accounts authenticate against; a FortiSwitchOS RADIUS entry holds one server, so define two | `config user radius; edit <RADIUS_1>; set server <RADIUS_1_IP>; set secret <KEY_1>; next; edit <RADIUS_2>; set server <RADIUS_2_IP>; set secret <KEY_2>; end` `config user group; edit <ADMIN_GROUP>; set member <RADIUS_1> <RADIUS_2>; end` `config system admin; edit <ADMIN>; set remote-auth enable; set remote-group <ADMIN_GROUP>; set wildcard enable; end` | 7.2.0 and later (RADIUS for administrative authentication) | Same requirement |
| C-NDM `CISC-ND-001410` | CAT II | `SRG-APP-000516-NDM-000340` | Back up the configuration whenever it changes | `ip scp server enable; file prompt quiet; event manager applet BACKUP_CONFIG authorization bypass; event syslog pattern "%SYS-5-CONFIG_I"; action 1 cli command "enable"; action 2 info type routername; action 3 cli command "copy running-config scp://<USER>@<SCP_SERVER>/<PATH>/$_info_routername-running-config"; action 4 syslog priority informational msg "Configuration backup executed for $_info_routername"` | 17.1.1 or earlier | Automation stitch: a configuration-change trigger runs a CLI script that copies the configuration to an SFTP server (the script holds the SFTP credential); local revisions are also kept at logout | `config system automation-trigger; edit <TRIGGER>; set trigger-type event-based; set event-type config-change; end` `config system automation-action; edit <ACTION>; set action-type cli-script; set script "execute backup config sftp <FILE> <SFTP_SERVER> <USER> <PASSWORD>"; end` `config system automation-stitch; edit <STITCH>; set trigger <TRIGGER>; set action <ACTION>; end` `config system global; set revision-backup-on-logout enable; end` | 7.2.0 and later (Automation stitches) | Same requirement |
| C-NDM `CISC-ND-001440` | CAT II | `SRG-APP-000516-NDM-000344` | Obtain public key certificates from an approved (DoD) certificate authority | `crypto pki trustpoint <TRUSTPOINT>; enrollment url <DOD_CA_ENROLLMENT_URL>` | 17.1.1 or earlier | SCEP enrollment of the switch certificate from the DoD CA | `config system certificate local; edit <CERT_NAME>; set scep-url <DOD_CA_SCEP_URL>; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-NDM `CISC-ND-001450` | CAT I | `SRG-APP-000516-NDM-000350` | Send logs to at least two central log servers | `logging host <SYSLOG_SERVER_1>; logging host <SYSLOG_SERVER_2>; logging trap critical` | 17.1.1 or earlier | Reliable (TCP), encrypted syslog to two of the three syslog destinations | `config log syslogd setting; set status enable; set server <SYSLOG_SERVER_1>; set mode reliable; set enc-algorithm high; end` `config log syslogd2 setting; set status enable; set server <SYSLOG_SERVER_2>; set mode reliable; set enc-algorithm high; end` | 7.0.0 or earlier (Reliable syslog) | Same requirement |
| C-NDM `CISC-ND-001470` | CAT I | `SRG-APP-000516-NDM-000351` | Run a software release the vendor still supports | `show version` `install add file <IMAGE> activate commit` | 17.1.1 or earlier | Run a FortiSwitchOS release Fortinet supports and check the running version (the rule's SRG ID is not in NDM SRG V5R5; Chapter 11 maps the current requirement `SRG-APP-001035-NDM-000340`) | `get system status` | Not in the feature matrix (8.0.0 CLI Reference) | By procedure |
| C-L2S `CISC-L2-000020` | CAT I | `SRG-NET-000148-L2S-000015` | Identify and authenticate every endpoint before it connects | `aaa new-model; radius server RADIUS_1; address ipv4 <RADIUS_1_IP>; key <KEY>; exit; radius server RADIUS_2; address ipv4 <RADIUS_2_IP>; key <KEY>; exit; aaa group server radius RADIUS_SERVERS; server name RADIUS_1; server name RADIUS_2; exit; aaa authentication dot1x default group RADIUS_SERVERS; dot1x system-auth-control; interface range <HOST_PORTS>; switchport mode access; authentication host-mode single-host; dot1x pae authenticator; authentication port-control auto; mab` | 17.1.1 or earlier | 802.1X with MAC authentication bypass on host ports, against a RADIUS server group | `config switch interface; edit <HOST_PORT>; config port-security; set port-security-mode 802.1X-mac-based; set mac-auth-bypass enable; end; set security-groups <GROUP>; end` `config user group; edit <GROUP>; set member <RADIUS_1> <RADIUS_2>; end` | 7.0.0 or earlier (802.1X MAC-based mode) | Same requirement |
| C-L2S `CISC-L2-000030` | CAT II | `SRG-NET-000168-L2S-000019` | Authenticate VTP messages with the strongest available hash | `vtp password <PASSWORD>` | 17.1.1 or earlier | FortiSwitch does not run VTP; it only floods Cisco VTP frames when `flood-vtp` is enabled (disabled by default) | `config switch global; set flood-vtp disable; end` | — | Not applicable |
| C-L2S `CISC-L2-000040` | CAT II | `SRG-NET-000193-L2S-000020` | Manage excess bandwidth to limit flooding denial-of-service attacks | `class-map match-all VOICE; match ip dscp ef; exit; class-map match-all SCAVENGER; match ip dscp cs1; exit; policy-map QOS_POLICY; class VOICE; priority level 1; class SCAVENGER; bandwidth percent 5; class class-default; bandwidth percent 25; exit; exit; interface <UPLINK_PORT>; service-policy output QOS_POLICY` | 17.1.1 or earlier | Egress QoS policy with weighted queues on uplinks (ACL policers and MAC learning limits also apply) | `config switch qos qos-policy; edit <POLICY>; set schedule weighted; end` `config switch interface; edit <UPLINK_PORT>; set qos-policy <POLICY>; end` | 7.0.0 or earlier (802.1p support, including priority queuing trunk and WRED) | Same requirement |
| C-L2S `CISC-L2-000090` | CAT III | `SRG-NET-000362-L2S-000021` | Enable Root Guard on ports facing access switches | `interface range <ACCESS_SWITCH_PORTS>; spanning-tree guard root` | 17.1.1 or earlier | STP root guard | `config switch interface; edit <ACCESS_SWITCH_PORT>; set stp-root-guard enabled; end` | 7.0.0 or earlier (STP root guard) | Same requirement |
| C-L2S `CISC-L2-000100` | CAT II | `SRG-NET-000362-L2S-000022` | Enable BPDU Guard on user-facing and untrusted ports | `interface range <HOST_PORTS>; spanning-tree bpduguard enable` | 17.1.1 or earlier | STP BPDU guard | `config switch interface; edit <HOST_PORT>; set stp-bpdu-guard enabled; end` | 7.0.0 or earlier (STP BPDU guard) | Same requirement |
| C-L2S `CISC-L2-000110` | CAT II | `SRG-NET-000362-L2S-000023` | Enable STP Loop Guard | `spanning-tree loopguard default` | 17.1.1 or earlier | STP loop protection, the counterpart of Cisco loop guard; FortiSwitch loop guard (`loop-guard`, the feature Chapter 11 maps) detects loops with its own probe frames and can be added | `config switch interface; edit <PORT>; set stp-loop-protection enabled; set loop-guard enabled; end` | 7.0.0 or earlier (Loop guard) | Same requirement |
| C-L2S `CISC-L2-000120` | CAT II | `SRG-NET-000362-L2S-000024` | Enable Unknown Unicast Flood Blocking on host ports | `interface range <HOST_PORTS>; switchport block unicast` | 17.1.1 or earlier | Per-port storm control with only unknown unicast enabled and a rate of 0 drops all unknown unicast; the port has one rate for all enabled traffic types, so it cannot also rate-limit broadcast (`CISC-L2-000160`) | `config switch physical-port; edit <HOST_PORT>; set storm-control-mode override; config storm-control; set unknown-unicast enable; set broadcast disable; set unknown-multicast disable; set rate 0; end; end` | 7.0.0 or earlier (Per-port storm control) | Partial |
| C-L2S `CISC-L2-000130` | CAT II | `SRG-NET-000362-L2S-000025` | Enable DHCP snooping on all user VLANs | `ip dhcp snooping; ip dhcp snooping vlan <USER_VLANS>` | 17.1.1 or earlier | DHCP snooping per VLAN, with the uplink trusted | `config switch vlan; edit <VLAN>; set dhcp-snooping enable; end` `config switch interface; edit <UPLINK>; set dhcp-snooping trusted; end` | 7.0.0 or earlier (DHCP snooping) | Same requirement |
| C-L2S `CISC-L2-000140` | CAT II | `SRG-NET-000362-L2S-000026` | Enable IP Source Guard on user-facing and untrusted ports | `interface range <HOST_PORTS>; ip verify source` | 17.1.1 or earlier | IP source guard | `config switch interface; edit <HOST_PORT>; set ip-source-guard enable; end` | 7.0.0 or earlier (IP source guard (IPv4)) | Same requirement |
| C-L2S `CISC-L2-000150` | CAT II | `SRG-NET-000362-L2S-000027` | Enable Dynamic ARP Inspection on all user VLANs | `ip arp inspection vlan <USER_VLANS>` | 17.1.1 or earlier | Dynamic ARP inspection per VLAN, with the uplink trusted | `config switch vlan; edit <VLAN>; set arp-inspection enable; end` `config switch interface; edit <UPLINK>; set arp-inspection-trust trusted; end` | 7.0.0 or earlier (Dynamic ARP inspection (IPv4)) | Same requirement |
| C-L2S `CISC-L2-000160` | CAT III | `SRG-NET-000512-L2S-000001` | Configure storm control on all host-facing ports | `interface range <HOST_PORTS>; storm-control unicast level bps 62000000; storm-control broadcast level bps 20000000` | 17.1.1 or earlier | Per-port storm control; FortiSwitchOS rates are in packets per second, Cisco levels in bits per second | `config switch physical-port; edit <HOST_PORT>; set storm-control-mode override; config storm-control; set broadcast enable; set unknown-unicast enable; set rate <PPS>; end; end` | 7.0.0 or earlier (Per-port storm control) | Same requirement |
| C-L2S `CISC-L2-000170` | CAT III | `SRG-NET-000512-L2S-000002` | Enable IGMP or MLD snooping on all VLANs | `ip igmp snooping` | 17.1.1 or earlier | IGMP and MLD snooping per VLAN | `config switch vlan; edit <VLAN>; set igmp-snooping enable; set mld-snooping enable; end` | 7.0.0 or earlier (IGMP snooping) | Same requirement |
| C-L2S `CISC-L2-000180` | CAT II | `SRG-NET-000512-L2S-000003` | Run Rapid STP where VLANs span switches with redundant links | `spanning-tree mode rapid-pvst` | 17.1.1 or earlier | FortiSwitchOS runs MSTP, which uses rapid convergence; enable it on every port, with Rapid PVST+ interoperation on ports that face Cisco switches | `config switch stp settings; set status enable; end` `config switch interface; edit <PORT>; set stp-state enabled; set rpvst-port enabled; end` | 7.0.0 or earlier (MSTP instances) | Same requirement |
| C-L2S `CISC-L2-000190` | CAT II | `SRG-NET-000512-L2S-000004` | Enable UDLD to protect against one-way links | `udld enable` | 17.1.1 or earlier | FortiSwitchOS has no UDLD; STP loop protection reduces the effect of a one-way link on a blocking port | `config switch interface; edit <PORT>; set stp-loop-protection enabled; end` | — | Not supported |
| C-L2S `CISC-L2-000200` | CAT II | `SRG-NET-000512-L2S-000005` | Enable all trunk links statically | `interface <TRUNK_PORT>; switchport trunk encapsulation dot1q; switchport mode trunk; switchport nonegotiate` | 17.1.1 or earlier | FortiSwitchOS has no trunk negotiation (no DTP), so tagged VLANs are always set statically per port; set link aggregation groups (FortiSwitchOS "trunks") to static or LACP explicitly | `config switch interface; edit <TRUNK_PORT>; set native-vlan <NATIVE_VLAN>; set allowed-vlans <VLANS>; end` `config switch trunk; edit <TRUNK>; set mode static; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | Same requirement |
| C-L2S `CISC-L2-000210` | CAT II | `SRG-NET-000512-L2S-000007` | Put disabled ports in an unused VLAN | `interface range <UNUSED_PORTS>; switchport access vlan <UNUSED_VLAN>; shutdown` | 17.1.1 or earlier | Native VLAN set to an unused VLAN, and the port shut down | `config switch interface; edit <UNUSED_PORT>; set native-vlan <UNUSED_VLAN>; end` `config switch physical-port; edit <UNUSED_PORT>; set status down; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | Equivalent setting |
| C-L2S `CISC-L2-000220` | CAT II | `SRG-NET-000512-L2S-000008` | Keep the default VLAN off host-facing ports | `interface range <HOST_PORTS>; switchport mode access; switchport access vlan <USER_VLAN>` | 17.1.1 or earlier | Native VLAN on host ports set to a user VLAN (the FortiSwitchOS default native VLAN is 1) | `config switch interface; edit <HOST_PORT>; set native-vlan <USER_VLAN>; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | Equivalent setting |
| C-L2S `CISC-L2-000230` | CAT II | `SRG-NET-000512-L2S-000009` | Prune the default VLAN from trunks that do not need it | `interface <TRUNK_PORT>; switchport trunk allowed vlan except 1,<UNUSED_VLAN>` | 17.1.1 or earlier | Allowed VLAN list on tagged ports that leaves out VLAN 1, with a native VLAN other than 1 | `config switch interface; edit <TRUNK_PORT>; set native-vlan <NATIVE_VLAN>; set allowed-vlans <VLANS>; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | Same requirement |
| C-L2S `CISC-L2-000240` | CAT II | `SRG-NET-000512-L2S-000010` | Keep management traffic off the default VLAN | `interface vlan <MGMT_VLAN>; ip address <IP_ADDRESS> <MASK>; no shutdown` | 17.1.1 or earlier | Management switch virtual interface (SVI) on a dedicated management VLAN | `config system interface; edit <MGMT_SVI>; set interface internal; set vlanid <MGMT_VLAN>; set ip <IP_ADDRESS> <MASK>; set allowaccess https ssh; end` | 7.6.4 and later (SVI) | Equivalent setting |
| C-L2S `CISC-L2-000250` | CAT II | `SRG-NET-000512-L2S-000011` | Configure user-facing and untrusted ports as access ports | `interface range <HOST_PORTS>; switchport mode access; switchport access vlan <USER_VLAN>` | 17.1.1 or earlier | Native VLAN only, with tagged frames discarded | `config switch interface; edit <HOST_PORT>; set native-vlan <USER_VLAN>; set discard-mode all-tagged; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | Same requirement |
| C-L2S `CISC-L2-000260` | CAT II | `SRG-NET-000512-L2S-000012` | Use a native VLAN other than the default VLAN on 802.1Q trunks | `interface <TRUNK_PORT>; switchport trunk native vlan <NATIVE_VLAN>` | 17.1.1 or earlier | Native VLAN on tagged ports set to a dedicated VLAN other than 1 | `config switch interface; edit <TRUNK_PORT>; set native-vlan <NATIVE_VLAN>; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | Same requirement |
| C-L2S `CISC-L2-000270` | CAT III | `SRG-NET-000512-L2S-000013` | Assign no access ports to the native VLAN | `interface range <HOST_PORTS>; switchport mode access; switchport access vlan <USER_VLAN>` | 17.1.1 or earlier | Host ports use user VLANs, never the native VLAN of the tagged ports | `config switch interface; edit <HOST_PORT>; set native-vlan <USER_VLAN>; end` | 7.0.0 or earlier (forced-untagged or force-tagged setting on switch interfaces) | Equivalent setting |
| C-RTR `CISC-RT-000010` | CAT II | `SRG-NET-000018-RTR-000001` | Enforce approved information flow control on routed traffic | `ip access-list extended <ACL_NAME>; permit tcp any <DEST_SUBNET> <WILDCARD> eq <PORT>; deny ip any any log-input; exit; interface vlan <VLAN_ID>; ip access-group <ACL_NAME> out` | 17.1.1 or earlier | Ingress ACLs on ports and routed interfaces | `config switch acl ingress; edit <ID>; set ingress-interface <PORT>; config classifier; set src-ip-prefix <IP> <MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | Same requirement |
| C-RTR `CISC-RT-000050` | CAT II | `SRG-NET-000168-RTR-000078` | Authenticate routing protocols with FIPS 198-1 algorithms and keys with lifetimes of no more than 180 days | `key chain OSPF_KEY_CHAIN; key 1; key-string <KEY>; cryptographic-algorithm hmac-sha-256; send-lifetime <START_TIME> duration 15552000; accept-lifetime <START_TIME> duration 15552000; exit; exit; interface <L3_INTERFACE>; ip ospf authentication key-chain OSPF_KEY_CHAIN` | 17.1.1 or earlier | OSPF, RIP, and IS-IS authenticate with MD5 or plain text only, and BGP with a TCP MD5 password; none is a FIPS 198-1 algorithm; RIP and IS-IS key chains support key lifetimes (Chapter 11 maps these protocols to this requirement and records the MD5 gap) | `config router ospf; config interface; edit <INTERFACE>; set authentication md5; config md5-keys; edit 1; set key <KEY>; end; end; end` `config router key-chain; edit <KEYCHAIN>; config key; edit 1; set key-string <KEY>; set accept-lifetime <START> <END>; set send-lifetime <START> <END>; end; end` | 7.0.0 or earlier (OSPF (IPv4/IPv6)) | Partial |
| C-RTR `CISC-RT-000060` | CAT III | `SRG-NET-000019-RTR-000007` | Disable inactive Layer 3 interfaces | `interface <UNUSED_L3_INTERFACE>; shutdown` | 17.1.1 or earlier | Interface administrative status | `config system interface; edit <UNUSED_L3_INTERFACE>; set status down; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-RTR `CISC-RT-000090` | CAT II | `SRG-NET-000362-RTR-000109` | Disable zero-touch deployment features on an operational network | `no boot network; no service config` | 17.1.1 or earlier | Disable FortiEdge Cloud provisioning and automatic ISL formation (auto-network) on a standalone switch; a FortiLink-managed switch is provisioned by its FortiGate | `config system flan-cloud; set status disable; end` `config switch auto-network; set status disable; end` | 7.0.0 or earlier (FortiEdge Cloud configuration) | Equivalent setting |
| C-RTR `CISC-RT-000120` | CAT I | `SRG-NET-000362-RTR-000110` | Protect the control plane against denial-of-service attacks | `cpp system-default` `show policy-map control-plane` | 17.1.1 or earlier | FortiSwitchOS has no configurable control plane policing; OSPF database overflow protection (the setting Chapter 11 maps) and storm control limit some control-plane load | `config router ospf; set database-overflow enable; set database-overflow-max-external-lsa <LSAS>; end` | 7.0.0 or earlier (OSPF database overflow protection (IPv4)) | Partial |
| C-RTR `CISC-RT-000150` | CAT II | `SRG-NET-000362-RTR-000111` | Disable gratuitous ARP on external interfaces | `no ip gratuitous-arps` | 17.1.1 or earlier | No setting stops FortiSwitch interfaces from sending gratuitous ARP; the `gratuitous-arp` security check on some models drops received gratuitous ARP packets instead | — | — | Not supported |
| C-RTR `CISC-RT-000160` | CAT III | `SRG-NET-000362-RTR-000112` | Disable IP directed broadcast on all interfaces | `interface <L3_INTERFACE>; no ip directed-broadcast` | 17.1.1 or earlier | No directed-broadcast setting; an ingress ACL can drop packets sent to a subnet broadcast address | `config switch acl ingress; edit <ID>; set ingress-interface <PORT>; config classifier; set dst-ip-prefix <SUBNET_BROADCAST_IP> <HOST_MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | Partial |
| C-RTR `CISC-RT-000170` | CAT II | `SRG-NET-000362-RTR-000113` | Disable ICMP unreachable messages on external interfaces | `interface <EXTERNAL_INTERFACE>; no ip unreachables` | 17.1.1 or earlier | No setting to stop the switch from sending ICMP unreachable messages | — | — | Not supported |
| C-RTR `CISC-RT-000180` | CAT II | `SRG-NET-000362-RTR-000114` | Disable ICMP mask reply messages on external interfaces | `interface <EXTERNAL_INTERFACE>; no ip mask-reply` | 17.1.1 or earlier | No setting for ICMP mask replies | — | — | Not supported |
| C-RTR `CISC-RT-000190` | CAT II | `SRG-NET-000362-RTR-000115` | Disable ICMP redirect messages on external interfaces | `interface <EXTERNAL_INTERFACE>; no ip redirects` | 17.1.1 or earlier | ICMP redirect setting per interface | `config system interface; edit <EXTERNAL_INTERFACE>; set icmp-redirect disable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-RTR `CISC-RT-000200` | CAT III | `SRG-NET-000078-RTR-000001` | Log all packets dropped by interface ACLs | `ip access-list extended <ACL_NAME>; deny ip any any log-input` | 17.1.1 or earlier | ACL counters show how many packets each policy dropped; FortiSwitchOS ACLs cannot log individual packets | `config switch acl ingress; edit <ID>; config action; set drop enable; set count enable; end; end` `get switch acl counters ingress` | 7.0.0 or earlier (ACL (IPv4 ingress)) | Partial |
| C-RTR `CISC-RT-000210` | CAT II | `SRG-NET-000076-RTR-000001` | Record where each dropped-packet event occurred | `ip access-list extended <ACL_NAME>; deny ip any any log-input` | 17.1.1 or earlier | ACL counters per policy and port; no per-packet log records | `config switch acl ingress; edit <ID>; config action; set count enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | Partial |
| C-RTR `CISC-RT-000220` | CAT II | `SRG-NET-000077-RTR-000001` | Record the source of each dropped-packet event | `ip access-list extended <ACL_NAME>; deny ip any any log-input` | 17.1.1 or earlier | ACL counters per policy; no per-packet log records with the source address | `config switch acl ingress; edit <ID>; config action; set count enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | Partial |
| C-RTR `CISC-RT-000230` | CAT III | `SRG-NET-000019-RTR-000001` | Disable the auxiliary port | `line aux 0; no exec; transport input none` | 17.1.1 or earlier | FortiSwitch has no auxiliary (modem) port; the console port is covered by the administrator authentication rules | — | — | Not applicable |
| C-RTR `CISC-RT-000235` | CAT II | `SRG-NET-000512-RTR-000100` | Enable Cisco Express Forwarding | `ip cef; ipv6 cef` | 17.1.1 or earlier | CEF is the Cisco forwarding architecture; FortiSwitch routes in hardware with no equivalent setting | — | — | Not applicable |
| C-RTR `CISC-RT-000236` | CAT III | `SRG-NET-000512-RTR-000012` | Advertise a hop limit of at least 32 in IPv6 router advertisements | `ipv6 hop-limit 128` | 17.1.1 or earlier | IPv6 router advertisement hop limit per interface | `config system interface; edit <INTERFACE>; config ipv6; set ip6-hop-limit 64; end; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-RTR `CISC-RT-000237` | CAT II | `SRG-NET-000512-RTR-000013` | Do not use IPv6 site-local unicast addresses | — | 17.1.1 or earlier | Address planning: assign no FEC0::/10 addresses | — | — | By procedure |
| C-RTR `CISC-RT-000240` | CAT I | `SRG-NET-000202-RTR-000001` | Perimeter: deny traffic by default and allow by exception | `ip access-list extended EXTERNAL_ACL_INBOUND; deny ip any any option any-options; deny ip <BOGON_PREFIX> <WILDCARD> any log-input; permit tcp any any established; permit tcp host <PEER_IP> host <LOCAL_IP> eq bgp; deny ip any any log-input; exit; interface <EXTERNAL_INTERFACE>; ip access-group EXTERNAL_ACL_INBOUND in` | 17.1.1 or earlier | Ingress ACLs can permit approved traffic and drop the rest, but FortiSwitchOS ACLs have no implicit deny and no established-session match, so an explicit drop policy must cover everything not permitted | `config switch acl ingress; edit <ID>; set ingress-interface <EXTERNAL_PORT>; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | Partial |
| C-RTR `CISC-RT-000250` | CAT II | `SRG-NET-000019-RTR-000002` | Perimeter: control traffic between interconnected networks by policy | `ip access-list extended EXTERNAL_ACL_INBOUND; deny ip any any option any-options; deny ip <BOGON_PREFIX> <WILDCARD> any log-input; permit tcp any any established; permit tcp host <PEER_IP> host <LOCAL_IP> eq bgp; deny ip any any log-input; exit; interface <EXTERNAL_INTERFACE>; ip access-group EXTERNAL_ACL_INBOUND in` | 17.1.1 or earlier | Ingress ACLs on the external ports | `config switch acl ingress; edit <ID>; set ingress-interface <EXTERNAL_PORT>; config classifier; set src-ip-prefix <SOURCE> <MASK>; set dst-ip-prefix <DESTINATION> <MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | Equivalent setting |
| C-RTR `CISC-RT-000260` | CAT II | `SRG-NET-000364-RTR-000109` | Perimeter: route inbound traffic only from authorized sources to authorized destinations | `ip access-list extended EXTERNAL_ACL_INBOUND; deny ip any any option any-options; deny ip <BOGON_PREFIX> <WILDCARD> any log-input; permit tcp any any established; permit tcp host <PEER_IP> host <LOCAL_IP> eq bgp; deny ip any any log-input; exit; interface <EXTERNAL_INTERFACE>; ip access-group EXTERNAL_ACL_INBOUND in` | 17.1.1 or earlier | Ingress ACLs matching source, destination, and service | `config switch acl ingress; edit <ID>; set ingress-interface <EXTERNAL_PORT>; config classifier; set src-ip-prefix <SOURCE> <MASK>; set dst-ip-prefix <DESTINATION> <MASK>; set service <SERVICE>; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | Equivalent setting |
| C-RTR `CISC-RT-000270` | CAT II | `SRG-NET-000364-RTR-000110` | Perimeter: block inbound packets with bogon source addresses | `ip access-list extended EXTERNAL_ACL_INBOUND; deny ip <BOGON_PREFIX> <WILDCARD> any log-input; exit; interface <EXTERNAL_INTERFACE>; ip access-group EXTERNAL_ACL_INBOUND in` | 17.1.1 or earlier | Ingress ACL dropping bogon source prefixes | `config switch acl ingress; edit <ID>; set ingress-interface <EXTERNAL_PORT>; config classifier; set src-ip-prefix <BOGON_PREFIX> <MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | Equivalent setting |
| C-RTR `CISC-RT-000310` | CAT I | `SRG-NET-000205-RTR-000014` | Perimeter: drop outbound packets with illegitimate source addresses (egress filter or uRPF) | `interface <INTERNAL_INTERFACE>; ip verify unicast source reachable-via rx; ip access-group EGRESS_FILTER in` | 17.1.1 or earlier | Unicast reverse path forwarding (source check) on internal interfaces | `config system interface; edit <INTERNAL_INTERFACE>; set src-check strict; end` | 7.0.0 or earlier (uRPF) | Same requirement |
| C-RTR `CISC-RT-000320` | CAT II | `SRG-NET-000205-RTR-000003` | Perimeter: filter traffic into the enclave as DoD Instruction 8551.01 requires | `ip access-list extended EXTERNAL_ACL_INBOUND; deny ip any any option any-options; deny ip <BOGON_PREFIX> <WILDCARD> any log-input; permit tcp any any established; permit tcp host <PEER_IP> host <LOCAL_IP> eq bgp; deny ip any any log-input; exit; interface <EXTERNAL_INTERFACE>; ip access-group EXTERNAL_ACL_INBOUND in` | 17.1.1 or earlier | Ingress ACLs built from the PPSM ports, protocols, and services list, using custom ACL services | `config switch acl service custom; edit <SERVICE>; set protocol TCP/UDP/SCTP; set tcp-portrange <PORT>; end` `config switch acl ingress; edit <ID>; set ingress-interface <EXTERNAL_PORT>; config classifier; set service <SERVICE>; end; end` | 7.4.3 and later (ACL service (IPv4)) | Equivalent setting |
| C-RTR `CISC-RT-000330` | CAT II | `SRG-NET-000205-RTR-000004` | Perimeter: filter ingress traffic inbound on the external interface | `ip access-list extended EXTERNAL_ACL_INBOUND; deny ip any any option any-options; deny ip <BOGON_PREFIX> <WILDCARD> any log-input; permit tcp any any established; permit tcp host <PEER_IP> host <LOCAL_IP> eq bgp; deny ip any any log-input; exit; interface <EXTERNAL_INTERFACE>; ip access-group EXTERNAL_ACL_INBOUND in` | 17.1.1 or earlier | Ingress ACLs on the external ports | `config switch acl ingress; edit <ID>; set ingress-interface <EXTERNAL_PORT>; config classifier; set src-ip-prefix <SOURCE> <MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | Equivalent setting |
| C-RTR `CISC-RT-000340` | CAT II | `SRG-NET-000205-RTR-000005` | Perimeter: filter egress traffic inbound on the internal interface | `interface <INTERNAL_INTERFACE>; ip verify unicast source reachable-via rx; ip access-group EGRESS_FILTER in` | 17.1.1 or earlier | Strict unicast reverse path forwarding on the internal interfaces, or an ingress ACL on the internal ports | `config system interface; edit <INTERNAL_INTERFACE>; set src-check strict; end` | 7.0.0 or earlier (uRPF) | Equivalent setting |
| C-RTR `CISC-RT-000350` | CAT II | `SRG-NET-000205-RTR-000015` | Perimeter: block all packets with IP options | `ip access-list extended EXTERNAL_ACL_INBOUND; deny ip any any option any-options; exit; interface <EXTERNAL_INTERFACE>; ip access-group EXTERNAL_ACL_INBOUND in` | 17.1.1 or earlier | FortiSwitchOS ACL classifiers cannot match IP options | — | — | Not supported |
| C-RTR `CISC-RT-000360` | CAT III | `SRG-NET-000364-RTR-000111` | Perimeter: disable LLDP on external interfaces | `interface <EXTERNAL_INTERFACE>; no lldp transmit` | 17.1.1 or earlier | LLDP status per physical port | `config switch physical-port; edit <EXTERNAL_PORT>; set lldp-status disable; end` | 7.0.0 or earlier (LLDP transmit) | Equivalent setting |
| C-RTR `CISC-RT-000370` | CAT III | `SRG-NET-000364-RTR-000111` | Perimeter: disable CDP on external interfaces | `interface <EXTERNAL_INTERFACE>; no cdp enable` | 17.1.1 or earlier | CDP status per physical port | `config switch physical-port; edit <EXTERNAL_PORT>; set cdp-status disable; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-RTR `CISC-RT-000380` | CAT II | `SRG-NET-000364-RTR-000112` | Perimeter: disable proxy ARP on external interfaces | `interface <EXTERNAL_INTERFACE>; no ip proxy-arp` | 17.1.1 or earlier | The 8.0.0 CLI Reference documents no proxy ARP function, so there is nothing to disable; confirm by test | — | — | Not applicable |
| C-RTR `CISC-RT-000390` | CAT II | `SRG-NET-000364-RTR-000113` | Perimeter: block all outbound management traffic | `ip access-list extended EXTERNAL_ACL_OUTBOUND; deny tcp any any eq tacacs log-input; deny tcp any any eq 22 log-input; deny udp any any eq snmp log-input; deny udp any any eq snmptrap log-input; deny udp any any eq syslog log-input; permit tcp any any eq www; deny ip any any log-input; exit; interface <EXTERNAL_INTERFACE>; ip access-group EXTERNAL_ACL_OUTBOUND out` | 17.1.1 or earlier | Egress ACL on the external ports that drops management protocols (SSH, TACACS+, SNMP, syslog) defined as custom ACL services | `config switch acl service custom; edit <MGMT_SERVICE>; set protocol TCP/UDP/SCTP; set tcp-portrange <MGMT_TCP_PORTS>; set udp-portrange <MGMT_UDP_PORTS>; end` `config switch acl egress; edit <ID>; set interface <EXTERNAL_PORT>; config classifier; set service <MGMT_SERVICE>; end; config action; set drop enable; end; end` | 7.4.3 and later (ACL (IPv4 egress)) | Equivalent setting |
| C-RTR `CISC-RT-000391` | CAT II | `SRG-NET-000512-RTR-000014` | Perimeter: suppress IPv6 router advertisements on external interfaces | `interface <EXTERNAL_INTERFACE>; ipv6 nd ra suppress` | 17.1.1 or earlier | Stop sending router advertisements on the interface, and RA guard on the external ports | `config system interface; edit <EXTERNAL_INTERFACE>; config ipv6; set ip6-send-adv disable; end; end` `config switch raguard-policy; edit <POLICY>; set device-role host; end` `config switch interface; edit <EXTERNAL_PORT>; config raguard; edit 1; set raguard-policy <POLICY>; set vlan-list <VLANS>; end; end` | 7.0.0 or earlier (IPv6 RA guard) | Same requirement |
| C-RTR `CISC-RT-000392` | CAT II | `SRG-NET-000364-RTR-000200` | Perimeter: drop IPv6 packets with an undetermined transport | `ipv6 access-list FILTER_IPV6; deny ipv6 any any undetermined-transport log; exit; interface <EXTERNAL_INTERFACE>; ipv6 traffic-filter FILTER_IPV6 in` | 17.1.1 or earlier | FortiSwitchOS ACL classifiers cannot match IPv6 extension headers or an undetermined upper-layer protocol | — | — | Not supported |
| C-RTR `CISC-RT-000393` | CAT II | `SRG-NET-000364-RTR-000201` | Perimeter: drop IPv6 packets with a Routing Header type 0, 1, or 3 to 255 | `ipv6 access-list FILTER_IPV6; permit ipv6 any host <HOME_AGENT_IPV6> routing-type 2; deny ipv6 any any routing log; exit; interface <EXTERNAL_INTERFACE>; ipv6 traffic-filter FILTER_IPV6 in` | 17.1.1 or earlier | FortiSwitchOS ACL classifiers cannot match IPv6 routing headers | — | — | Not supported |
| C-RTR `CISC-RT-000394` | CAT II | `SRG-NET-000364-RTR-000202` | Perimeter: drop IPv6 Hop-by-Hop headers with invalid option types | `ipv6 access-list FILTER_IPV6; deny ipv6 any any hbh log; exit; interface <EXTERNAL_INTERFACE>; ipv6 traffic-filter FILTER_IPV6 in` | 17.1.1 or earlier | FortiSwitchOS ACL classifiers cannot match IPv6 Hop-by-Hop options | — | — | Not supported |
| C-RTR `CISC-RT-000395` | CAT II | `SRG-NET-000364-RTR-000203` | Perimeter: drop IPv6 Destination Option headers with invalid option types | `ipv6 access-list FILTER_IPV6; deny ipv6 any any dest-option-type log; exit; interface <EXTERNAL_INTERFACE>; ipv6 traffic-filter FILTER_IPV6 in` | 17.1.1 or earlier | FortiSwitchOS ACL classifiers cannot match IPv6 Destination Options | — | — | Not supported |
| C-RTR `CISC-RT-000396` | CAT II | `SRG-NET-000364-RTR-000204` | Perimeter: drop IPv6 extension headers with the Endpoint Identification option | `ipv6 access-list FILTER_IPV6; deny ipv6 any any undetermined-transport log; permit ipv6 any host <HOME_AGENT_IPV6> routing-type 2; deny ipv6 any any routing log; deny ipv6 any any hbh log; deny ipv6 any any dest-option-type log; deny ipv6 any any log; exit; interface <EXTERNAL_INTERFACE>; ipv6 nd ra suppress; ipv6 traffic-filter FILTER_IPV6 in` | 17.1.1 or earlier | FortiSwitchOS ACL classifiers cannot match IPv6 extension header options | — | — | Not supported |
| C-RTR `CISC-RT-000397` | CAT II | `SRG-NET-000364-RTR-000205` | Perimeter: drop IPv6 Destination Option headers with the NSAP address option | `ipv6 access-list FILTER_IPV6; deny ipv6 any any undetermined-transport log; permit ipv6 any host <HOME_AGENT_IPV6> routing-type 2; deny ipv6 any any routing log; deny ipv6 any any hbh log; deny ipv6 any any dest-option-type log; deny ipv6 any any log; exit; interface <EXTERNAL_INTERFACE>; ipv6 nd ra suppress; ipv6 traffic-filter FILTER_IPV6 in` | 17.1.1 or earlier | FortiSwitchOS ACL classifiers cannot match IPv6 extension header options | — | — | Not supported |
| C-RTR `CISC-RT-000398` | CAT II | `SRG-NET-000364-RTR-000206` | Perimeter: drop IPv6 Hop-by-Hop or Destination Option headers with undefined option types | `ipv6 access-list FILTER_IPV6; deny ipv6 any any undetermined-transport log; permit ipv6 any host <HOME_AGENT_IPV6> routing-type 2; deny ipv6 any any routing log; deny ipv6 any any hbh log; deny ipv6 any any dest-option-type log; deny ipv6 any any log; exit; interface <EXTERNAL_INTERFACE>; ipv6 nd ra suppress; ipv6 traffic-filter FILTER_IPV6 in` | 17.1.1 or earlier | FortiSwitchOS ACL classifiers cannot match IPv6 extension header options | — | — | Not supported |
| C-RTR `CISC-RT-000450` | CAT II | `SRG-NET-000205-RTR-000012` | Permit management traffic only through the out-of-band management interface | `ip access-list extended INGRESS_MANAGEMENT_ACL; permit tcp any host <MGMT_IP_ADDRESS> eq 22; permit udp any host <MGMT_IP_ADDRESS> eq 161; permit icmp any host <MGMT_IP_ADDRESS>; deny ip any any log-input; exit; ip access-list extended EGRESS_MANAGEMENT_ACL; deny ip any any log-input; exit; interface <MGMT_INTERFACE>; ip access-group INGRESS_MANAGEMENT_ACL in; ip access-group EGRESS_MANAGEMENT_ACL out` | 17.1.1 or earlier | Management protocols allowed only on the dedicated management port, with no management access on in-band interfaces | `config system interface; edit mgmt; set allowaccess https ssh snmp; end` | Not in the feature matrix (8.0.0 CLI Reference) | Equivalent setting |
| C-RTR `CISC-RT-000470` | CAT III | `SRG-NET-000362-RTR-000124` | BGP: enable the Generalized TTL Security Mechanism (GTSM) | `router bgp <ASN>; neighbor <EBGP_PEER> ttl-security hops 1` | 17.1.1 or earlier | eBGP TTL security per neighbor | `config router bgp; config neighbor; edit <EBGP_PEER>; set ebgp-ttl-security-hops 1; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | Equivalent setting |
| C-RTR `CISC-RT-000480` | CAT II | `SRG-NET-000230-RTR-000002` | BGP: use a unique key for each autonomous system peered with | `router bgp <ASN>; neighbor <EBGP_PEER> password <UNIQUE_KEY>` | 17.1.1 or earlier | Per-neighbor BGP password (TCP MD5, as on the Cisco side) | `config router bgp; config neighbor; edit <EBGP_PEER>; set password <UNIQUE_KEY>; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | Equivalent setting |
| C-RTR `CISC-RT-000490` | CAT II | `SRG-NET-000018-RTR-000002` | BGP: reject inbound advertisements of bogon prefixes | `ip prefix-list PREFIX_FILTER deny <BOGON_PREFIX> le 32; router bgp <ASN>; neighbor <EBGP_PEER> prefix-list PREFIX_FILTER in` | 17.1.1 or earlier | Inbound prefix list on each eBGP neighbor | `config router prefix-list; edit PREFIX_FILTER; config rule; edit 1; set action deny; set prefix <BOGON_PREFIX> <MASK>; set le 32; end; end` `config router bgp; config neighbor; edit <EBGP_PEER>; set prefix-list-in PREFIX_FILTER; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | Same requirement |
| C-RTR `CISC-RT-000500` | CAT II | `SRG-NET-000018-RTR-000003` | BGP: reject inbound advertisements of the local AS's own prefixes | `ip prefix-list PREFIX_FILTER deny <LOCAL_AS_PREFIX> le 32; router bgp <ASN>; neighbor <EBGP_PEER> prefix-list PREFIX_FILTER in` | 17.1.1 or earlier | Inbound prefix list on each eBGP neighbor | `config router prefix-list; edit PREFIX_FILTER; config rule; edit 2; set action deny; set prefix <LOCAL_AS_PREFIX> <MASK>; set le 32; end; end` `config router bgp; config neighbor; edit <EBGP_PEER>; set prefix-list-in PREFIX_FILTER; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | Equivalent setting |
| C-RTR `CISC-RT-000510` | CAT II | `SRG-NET-000018-RTR-000004` | BGP: reject advertisements from a CE for prefixes not allocated to that customer | `router bgp <ASN>; neighbor <CE_PEER> prefix-list <CUSTOMER_PREFIX_LIST> in` | 17.1.1 or earlier | Inbound prefix list per customer neighbor | `config router bgp; config neighbor; edit <CE_PEER>; set prefix-list-in <CUSTOMER_PREFIX_LIST>; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | Equivalent setting |
| C-RTR `CISC-RT-000520` | CAT II | `SRG-NET-000018-RTR-000005` | BGP: advertise only customer and local AS prefixes | `ip prefix-list CE_PREFIX_ADVERTISEMENTS permit <CUSTOMER_PREFIX> le 32; router bgp <ASN>; neighbor <CE_PEER> prefix-list CE_PREFIX_ADVERTISEMENTS out` | 17.1.1 or earlier | Outbound prefix list per neighbor | `config router prefix-list; edit CE_PREFIX_ADVERTISEMENTS; config rule; edit 1; set action permit; set prefix <CUSTOMER_PREFIX> <MASK>; set le 32; end; end` `config router bgp; config neighbor; edit <CE_PEER>; set prefix-list-out CE_PREFIX_ADVERTISEMENTS; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | Equivalent setting |
| C-RTR `CISC-RT-000530` | CAT II | `SRG-NET-000205-RTR-000006` | BGP: do not advertise IP core prefixes | `ip prefix-list CE_PREFIX_ADVERTISEMENTS permit <CUSTOMER_PREFIX> le 32; router bgp <ASN>; neighbor <CE_PEER> prefix-list CE_PREFIX_ADVERTISEMENTS out` | 17.1.1 or earlier | Outbound prefix list that denies the core prefixes | `config router prefix-list; edit CE_PREFIX_ADVERTISEMENTS; config rule; edit 2; set action deny; set prefix <CORE_PREFIX> <MASK>; set le 32; end; end` `config router bgp; config neighbor; edit <CE_PEER>; set prefix-list-out CE_PREFIX_ADVERTISEMENTS; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | Equivalent setting |
| C-RTR `CISC-RT-000540` | CAT III | `SRG-NET-000018-RTR-000006` | BGP: reject routes whose AS_PATH does not start with the peer's AS | `router bgp <ASN>; bgp enforce-first-as` | 17.1.1 or earlier | First-AS enforcement per neighbor | `config router bgp; config neighbor; edit <EBGP_PEER>; set enforce-first-as enable; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | Equivalent setting |
| C-RTR `CISC-RT-000550` | CAT III | `SRG-NET-000018-RTR-000010` | BGP: reject CE routes whose originating AS does not belong to that customer | `ip as-path access-list 10 permit ^<CUSTOMER_ASN>$; router bgp <ASN>; neighbor <CE_PEER> filter-list 10 in` | 17.1.1 or earlier | AS path list applied inbound to the customer neighbor | `config router aspath-list; edit <ASPATH_LIST>; config rule; edit 1; set action permit; set regexp <CUSTOMER_ASN_REGEX>; end; end` `config router bgp; config neighbor; edit <CE_PEER>; set filter-list-in <ASPATH_LIST>; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | Equivalent setting |
| C-RTR `CISC-RT-000560` | CAT II | `SRG-NET-000362-RTR-000117` | BGP: limit the number of prefixes accepted from each peer | `router bgp <ASN>; neighbor <EBGP_PEER> maximum-prefix <MAXIMUM>` | 17.1.1 or earlier | Maximum prefixes per neighbor | `config router bgp; config neighbor; edit <EBGP_PEER>; set maximum-prefix <MAXIMUM>; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | Equivalent setting |
| C-RTR `CISC-RT-000570` | CAT III | `SRG-NET-000362-RTR-000118` | BGP: accept no inbound prefixes longer than /24 | `ip prefix-list PREFIX_FILTER permit 0.0.0.0/0 ge 8 le 24; router bgp <ASN>; neighbor <EBGP_PEER> prefix-list PREFIX_FILTER in` | 17.1.1 or earlier | Inbound prefix list rule that permits only prefixes of /8 to /24 | `config router prefix-list; edit PREFIX_FILTER; config rule; edit 3; set action permit; set prefix any; set ge 8; set le 24; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | Equivalent setting |
| C-RTR `CISC-RT-000580` | CAT III | `SRG-NET-000512-RTR-000001` | BGP: source iBGP sessions from a loopback address | `router bgp <ASN>; neighbor <IBGP_PEER> update-source Loopback0` | 17.1.1 or earlier | Loopback interface used as the update source for iBGP neighbors | `config system interface; edit <LOOPBACK>; set type loopback; set ip <LOOPBACK_IP> <HOST_MASK>; end` `config router bgp; config neighbor; edit <IBGP_PEER>; set update-source <LOOPBACK>; end; end` | 7.0.0 or earlier (BGP (IPv4/IPv6)) | Equivalent setting |
| C-RTR `CISC-RT-000590` | CAT III | `SRG-NET-000512-RTR-000002` | MPLS: source LDP sessions from a loopback address | `mpls ldp router-id Loopback0 force` | 17.1.1 or earlier | FortiSwitchOS has no MPLS or LDP | — | — | Not supported |
| C-RTR `CISC-RT-000600` | CAT III | `SRG-NET-000512-RTR-000003` | MPLS: synchronize the IGP with LDP | `router ospf <PROCESS_ID>; mpls ldp sync` | 17.1.1 or earlier | FortiSwitchOS has no MPLS or LDP | — | — | Not supported |
| C-RTR `CISC-RT-000610` | CAT III | `SRG-NET-000193-RTR-000001` | MPLS: pace RSVP-TE messages | `ip rsvp signalling rate-limit burst 9 maxsize 2100 period 30` | 17.1.1 or earlier | FortiSwitchOS has no MPLS traffic engineering or RSVP-TE | — | — | Not supported |
| C-RTR `CISC-RT-000620` | CAT II | `SRG-NET-000512-RTR-000004` | MPLS: disable TTL propagation | `no mpls ip propagate-ttl` | 17.1.1 or earlier | FortiSwitchOS has no MPLS | — | — | Not supported |
| C-RTR `CISC-RT-000630` | CAT I | `SRG-NET-000512-RTR-000005` | PE: bind each VRF to the right interfaces to keep L3VPNs separate | `ip vrf <VRF_NAME>; rd <RD>; route-target import <RT>; route-target export <RT>; exit; interface <CE_INTERFACE>; ip vrf forwarding <VRF_NAME>` | 17.1.1 or earlier | VRF-lite: interfaces can be bound to VRFs (the setting Chapter 11 maps), but FortiSwitchOS has no MPLS L3VPN, so it cannot act as a PE | `config router vrf; edit <VRF>; set vrfid <ID>; end` `config system interface; edit <INTERFACE>; set vrf <VRF>; end` | 7.0.0 or earlier (VRF (IPv4/IPv6)) | Partial |
| C-RTR `CISC-RT-000640` | CAT I | `SRG-NET-000512-RTR-000006` | PE: give each VRF the right route targets | `ip vrf <VRF_NAME>; rd <RD>; route-target import <RT>; route-target export <RT>; exit; interface <CE_INTERFACE>; ip vrf forwarding <VRF_NAME>` | 17.1.1 or earlier | No MPLS L3VPN; FortiSwitchOS route targets exist only for BGP EVPN VXLAN | — | — | Not supported |
| C-RTR `CISC-RT-000650` | CAT II | `SRG-NET-000512-RTR-000007` | PE: give each VRF the right route distinguisher | `ip vrf <VRF_NAME>; rd <RD>; route-target import <RT>; route-target export <RT>; exit; interface <CE_INTERFACE>; ip vrf forwarding <VRF_NAME>` | 17.1.1 or earlier | No MPLS L3VPN; FortiSwitchOS route distinguishers exist only for BGP EVPN VXLAN | — | — | Not supported |
| C-RTR `CISC-RT-000660` | CAT II | `SRG-NET-000343-RTR-000001` | PE: authenticate targeted LDP sessions for L2VPN with a FIPS-approved MAC | `mpls ldp neighbor <PEER_IP> password <PASSWORD>` | 17.1.1 or earlier | FortiSwitchOS has no MPLS L2VPN or LDP | — | — | Not supported |
| C-RTR `CISC-RT-000670` | CAT I | `SRG-NET-000512-RTR-000008` | PE: set the right VC ID for each VPWS attachment circuit | `interface <CE_INTERFACE>; xconnect <PEER_IP> <VC_ID> encapsulation mpls` | 17.1.1 or earlier | FortiSwitchOS has no VPWS pseudowires | — | — | Not supported |
| C-RTR `CISC-RT-000680` | CAT I | `SRG-NET-000512-RTR-000009` | PE: define VPLS attachment circuits with a unique VPN ID per customer VLAN | `l2 vfi <VFI_NAME> manual; vpn id <VPN_ID>; neighbor <PE_IP> encapsulation mpls; bridge-domain <BD_ID>` | 17.1.1 or earlier | FortiSwitchOS has no VPLS | — | — | Not supported |
| C-RTR `CISC-RT-000690` | CAT III | `SRG-NET-000512-RTR-000010` | PE: enforce split horizon for all pseudowires in a VPLS bridge domain | `l2 vfi <VFI_NAME> manual; vpn id <VPN_ID>; neighbor <PE_IP> encapsulation mpls; bridge-domain <BD_ID>` | 17.1.1 or earlier | FortiSwitchOS has no VPLS | — | — | Not supported |
| C-RTR `CISC-RT-000700` | CAT II | `SRG-NET-000193-RTR-000002` | PE: set storm control thresholds on VPLS CE-facing interfaces | `interface <CE_INTERFACE>; storm-control broadcast level bps <RATE>` | 17.1.1 or earlier | FortiSwitchOS has no VPLS; storm control itself is covered by `CISC-L2-000160` | — | — | Not supported |
| C-RTR `CISC-RT-000710` | CAT III | `SRG-NET-000362-RTR-000119` | PE: run IGMP or MLD snooping in each VPLS bridge domain | `bridge-domain <BD_ID>; ip igmp snooping` | 17.1.1 or earlier | FortiSwitchOS has no VPLS; VLAN snooping is covered by `CISC-L2-000170` | — | — | Not supported |
| C-RTR `CISC-RT-000720` | CAT II | `SRG-NET-000192-RTR-000002` | PE: limit the MAC addresses learned in each VPLS bridge domain | `bridge-domain <BD_ID>; mac limit maximum addresses <MAXIMUM>` | 17.1.1 or earlier | FortiSwitchOS has no VPLS; per-port and per-VLAN MAC learning limits exist outside VPLS | — | — | Not supported |
| C-RTR `CISC-RT-000730` | CAT I | `SRG-NET-000205-RTR-000007` | PE: block traffic destined to the IP core infrastructure | `ip access-list extended BLOCK_TO_CORE; deny ip any <CORE_PREFIX> <WILDCARD> log-input; permit ip any any; exit; interface <CE_INTERFACE>; ip access-group BLOCK_TO_CORE in` | 17.1.1 or earlier | The rule is for an MPLS PE, a role FortiSwitch cannot take; an ingress ACL can drop traffic to core prefixes at another edge | `config switch acl ingress; edit <ID>; set ingress-interface <EDGE_PORT>; config classifier; set dst-ip-prefix <CORE_PREFIX> <MASK>; end; config action; set drop enable; end; end` | — | Not applicable |
| C-RTR `CISC-RT-000740` | CAT II | `SRG-NET-000205-RTR-000008` | PE: enable loose uRPF on CE-facing interfaces | `interface <CE_INTERFACE>; ip verify unicast source reachable-via any` | 17.1.1 or earlier | The rule is for an MPLS PE, a role FortiSwitch cannot take; loose source checking exists for other edges | `config system interface; edit <EDGE_INTERFACE>; set src-check loose; end` | — | Not applicable |
| C-RTR `CISC-RT-000750` | CAT II | `SRG-NET-000205-RTR-000016` | PE: drop or ignore all packets with IP options | `ip options drop` | 17.1.1 or earlier | The rule is for an MPLS PE, a role FortiSwitch cannot take; FortiSwitchOS ACLs cannot match IP options in any role (`CISC-RT-000350`) | — | — | Not applicable |
| C-RTR `CISC-RT-000760` | CAT III | `SRG-NET-000193-RTR-000113` | PE: enforce a QoS policy that favors mission-critical traffic | `class-map match-all VOICE; match ip dscp ef; exit; class-map match-all SCAVENGER; match ip dscp cs1; exit; policy-map QOS_POLICY; class VOICE; priority level 1; class SCAVENGER; bandwidth percent 5; class class-default; bandwidth percent 25; exit; exit; interface <UPLINK_PORT>; service-policy output QOS_POLICY` | 17.1.1 or earlier | The rule is for an MPLS PE, a role FortiSwitch cannot take; QoS policies exist for other roles (`CISC-RT-000780`) | — | — | Not applicable |
| C-RTR `CISC-RT-000770` | CAT III | `SRG-NET-000193-RTR-000114` | P (MPLS core): enforce a QoS policy that favors mission-critical traffic | `class-map match-all VOICE; match ip dscp ef; exit; class-map match-all SCAVENGER; match ip dscp cs1; exit; policy-map QOS_POLICY; class VOICE; priority level 1; class SCAVENGER; bandwidth percent 5; class class-default; bandwidth percent 25; exit; exit; interface <UPLINK_PORT>; service-policy output QOS_POLICY` | 17.1.1 or earlier | The rule is for an MPLS provider core switch, a role FortiSwitch cannot take | — | — | Not applicable |
| C-RTR `CISC-RT-000780` | CAT II | `SRG-NET-000193-RTR-000112` | Enforce a QoS policy that limits packet-flooding denial-of-service attacks | `class-map match-all VOICE; match ip dscp ef; exit; class-map match-all SCAVENGER; match ip dscp cs1; exit; policy-map QOS_POLICY; class VOICE; priority level 1; class SCAVENGER; bandwidth percent 5; class class-default; bandwidth percent 25; exit; exit; interface <UPLINK_PORT>; service-policy output QOS_POLICY` | 17.1.1 or earlier | Egress QoS policy on uplinks, with ACL policers for flood-prone traffic | `config switch qos qos-policy; edit <POLICY>; set schedule weighted; end` `config switch interface; edit <UPLINK_PORT>; set qos-policy <POLICY>; end` | 7.0.0 or earlier (802.1p support, including priority queuing trunk and WRED) | Equivalent setting |
| C-RTR `CISC-RT-000790` | CAT II | `SRG-NET-000019-RTR-000003` | Multicast: disable PIM on interfaces that do not need multicast routing | `interface <NON_MULTICAST_INTERFACE>; no ip pim sparse-mode` | 17.1.1 or earlier | PIM-SSM configured only on the interfaces that route multicast | `config router multicast; config interface; edit <INTERFACE>; set pim-mode ssm-mode; end; end` | 7.2.8 and later (PIM-SSM (IPv4)) | Same requirement |
| C-RTR `CISC-RT-000800` | CAT II | `SRG-NET-000019-RTR-000004` | Multicast: bind a PIM neighbor filter to PIM interfaces | `ip access-list standard PIM_NEIGHBORS; permit <PIM_NEIGHBOR_IP>; exit; interface <PIM_INTERFACE>; ip pim neighbor-filter PIM_NEIGHBORS` | 17.1.1 or earlier | PIM runs only where configured (the setting Chapter 11 maps), but FortiSwitchOS has no PIM neighbor filter | `config router multicast; config interface; edit <INTERFACE>; set pim-mode ssm-mode; end; end` | 7.2.8 and later (PIM-SSM (IPv4)) | Partial |
| C-RTR `CISC-RT-000810` | CAT III | `SRG-NET-000019-RTR-000005` | Multicast edge: set boundaries for administratively scoped multicast | `ip access-list standard MULTICAST_SCOPE; deny 239.0.0.0 0.255.255.255; permit any; exit; interface <PIM_INTERFACE>; ip multicast boundary MULTICAST_SCOPE` | 17.1.1 or earlier | No multicast boundary setting; an ingress ACL on the boundary ports can drop 239.0.0.0/8 traffic, but it does not filter PIM or IGMP control messages for those groups | `config switch acl ingress; edit <ID>; set ingress-interface <BOUNDARY_PORT>; config classifier; set dst-ip-prefix <ADMIN_SCOPED_PREFIX> <MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) | Partial |
| C-RTR `CISC-RT-000820` | CAT III | `SRG-NET-000362-RTR-000120` | RP: limit the multicast forwarding cache (PIM and MSDP source-active state) | `ip access-list extended PIM_REGISTER_FILTER; deny ip any <GROUP> <WILDCARD>; permit ip host <SOURCE> any; deny ip any any; exit; ip pim accept-register list PIM_REGISTER_FILTER; ip pim register-rate-limit <RATE>; ip access-list standard PIM_JOIN_FILTER; deny <GROUP> <WILDCARD>; permit any; exit; ip pim accept-rp <RP_ADDRESS> PIM_JOIN_FILTER; ip pim spt-threshold infinity` | 17.1.1 or earlier | FortiSwitchOS supports PIM-SSM only, which has no rendezvous point | — | — | Not applicable |
| C-RTR `CISC-RT-000830` | CAT III | `SRG-NET-000019-RTR-000013` | RP: filter PIM Register messages for unwanted groups and sources | `ip access-list extended PIM_REGISTER_FILTER; deny ip any <GROUP> <WILDCARD>; permit ip host <SOURCE> any; deny ip any any; exit; ip pim accept-register list PIM_REGISTER_FILTER` | 17.1.1 or earlier | FortiSwitchOS supports PIM-SSM only, which has no rendezvous point or Register messages | — | — | Not applicable |
| C-RTR `CISC-RT-000840` | CAT III | `SRG-NET-000019-RTR-000014` | RP: filter PIM Join messages for unwanted groups | `ip access-list standard PIM_JOIN_FILTER; deny <GROUP> <WILDCARD>; permit any; exit; ip pim accept-rp <RP_ADDRESS> PIM_JOIN_FILTER` | 17.1.1 or earlier | FortiSwitchOS supports PIM-SSM only, which has no rendezvous point | — | — | Not applicable |
| C-RTR `CISC-RT-000850` | CAT II | `SRG-NET-000362-RTR-000121` | RP: rate-limit PIM Register messages | `ip pim register-rate-limit <RATE>` | 17.1.1 or earlier | FortiSwitchOS supports PIM-SSM only, which has no Register messages | — | — | Not applicable |
| C-RTR `CISC-RT-000860` | CAT III | `SRG-NET-000364-RTR-000114` | DR: let hosts join only approved multicast groups (IGMP and MLD report filter) | `ip access-list standard IGMP_JOIN_FILTER; deny <GROUP> <WILDCARD>; permit any; exit; interface vlan <USER_VLAN>; ip igmp access-group IGMP_JOIN_FILTER` | 17.1.1 or earlier | FortiSwitchOS has no IGMP or MLD join filter on routed interfaces | — | — | Not supported |
| C-RTR `CISC-RT-000870` | CAT II | `SRG-NET-000364-RTR-000115` | DR: let hosts join groups only from approved sources | `ip access-list standard IGMP_JOIN_FILTER; deny <GROUP> <WILDCARD>; permit any; exit; interface vlan <USER_VLAN>; ip igmp access-group IGMP_JOIN_FILTER` | 17.1.1 or earlier | FortiSwitchOS has no IGMP or MLD source filter on routed interfaces | — | — | Not supported |
| C-RTR `CISC-RT-000880` | CAT II | `SRG-NET-000362-RTR-000122` | DR: limit the multicast route states created by IGMP and MLD reports | `interface vlan <USER_VLAN>; ip igmp limit <NUMBER>` | 17.1.1 or earlier | FortiSwitchOS has no limit on IGMP or MLD groups per interface | — | — | Not supported |
| C-RTR `CISC-RT-000890` | CAT II | `SRG-NET-000362-RTR-000123` | DR: set the SPT threshold to infinity where Any Source Multicast is used | `ip pim spt-threshold infinity` | 17.1.1 or earlier | FortiSwitchOS supports PIM-SSM only, so there is no shared tree or SPT switchover | — | — | Not applicable |
| C-RTR `CISC-RT-000900` | CAT II | `SRG-NET-000364-RTR-000116` | MSDP: accept MSDP packets only from known peers | `ip msdp peer <PEER_IP> connect-source Loopback0 remote-as <ASN>; ip access-list extended EXTERNAL_ACL_INBOUND; permit tcp host <PEER_IP> host <LOCAL_IP> eq 639; deny tcp any host <LOCAL_IP> eq 639` | 17.1.1 or earlier | FortiSwitchOS does not run MSDP | — | — | Not applicable |
| C-RTR `CISC-RT-000910` | CAT II | `SRG-NET-000343-RTR-000002` | MSDP: authenticate all received MSDP packets | `ip msdp password peer <PEER_IP> <PASSWORD>` | 17.1.1 or earlier | FortiSwitchOS does not run MSDP | — | — | Not applicable |
| C-RTR `CISC-RT-000920` | CAT III | `SRG-NET-000018-RTR-000007` | MSDP: filter received source-active messages for unwanted groups and sources | `ip msdp sa-filter in <PEER_IP> list INBOUND_MSDP_SA_FILTER` | 17.1.1 or earlier | FortiSwitchOS does not run MSDP | — | — | Not applicable |
| C-RTR `CISC-RT-000930` | CAT III | `SRG-NET-000018-RTR-000008` | MSDP: filter source-active messages sent to external peers | `ip msdp sa-filter out <PEER_IP> list OUTBOUND_MSDP_SA_FILTER` | 17.1.1 or earlier | FortiSwitchOS does not run MSDP | — | — | Not applicable |
| C-RTR `CISC-RT-000940` | CAT III | `SRG-NET-000018-RTR-000009` | MSDP: limit source-active messages accepted from each peer | `ip msdp sa-limit <PEER_IP> <NUMBER>` | 17.1.1 or earlier | FortiSwitchOS does not run MSDP | — | — | Not applicable |
| C-RTR `CISC-RT-000950` | CAT III | `SRG-NET-000512-RTR-000011` | MSDP: source MSDP traffic from a loopback address | `ip msdp peer <PEER_IP> connect-source Loopback0 remote-as <ASN>` | 17.1.1 or earlier | FortiSwitchOS does not run MSDP | — | — | Not applicable |

### FortiSwitch requirements with no Cisco switch rule

The 26 SRG requirements below are mapped to FortiSwitch features
in Chapter 11 but are cited by no Cisco IOS XE Switch STIG rule, so a Cisco
rule checklist misses them. They are the AAA Services SRG requirements
(802.1X and RADIUS behavior), the Layer 2 Switch SRG's general requirements
(network access control, separation, alternate paths), the VRRP
authentication requirement, and NDM requirements such as FIPS mode and
signed firmware; two of the NDM requirements (clock synchronization and
vendor-supported versions) are the current versions of the older SRG IDs
that `CISC-ND-001030` and `CISC-ND-001470` cite. Add them to the FortiSwitch
checklist. The requirement text is the SRG title; the
setting column lists the Chapter 11 features mapped to the requirement, and
the version column gives the first listed release of the feature whose
command is shown (see *Where the version columns come from*).

[Download the unmatched requirements as CSV](https://tim-army.github.io/Enterprise-Infrastructure-Encyclopedia/data/volume-172-disa-srgs-and-stigs/33-fortiswitch-and-cisco-catalyst-switch-stig-crosswalk-unmatched.csv) (26 rows).

| SRG | Requirement ID | Requirement | FortiSwitch setting | FortiSwitchOS command | FortiSwitchOS version |
| --- | --- | --- | --- | --- | --- |
| NDM | `SRG-APP-000033-NDM-000212` | The network device must be configured to assign appropriate user roles or access levels to authenticated users. | Access profiles assigned to administrator accounts (Chapter 11 also maps centralized, cloud, and REST API management to this requirement) | `config system accprofile; edit <PROFILE>; set sysgrp read; end` `config system admin; edit <ADMIN>; set accprofile <PROFILE>; end` | Not in the feature matrix (8.0.0 CLI Reference) |
| NDM | `SRG-APP-000131-NDM-000243` | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. | OS image signature verification; Configuration file verification; CLI reports if BIOS and firmware signatures are valid | `diagnose sys firmware info` | 7.4.0 and later (OS image signature verification) |
| NDM | `SRG-APP-000179-NDM-000265` | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. | LINCE support; FIPS 140-3 (Level 1) and CC support; FedRAMP support | `config system security; set mode fips-cc; end` | 7.6.4 and later (FIPS 140-3 (Level 1) and CC support) |
| NDM | `SRG-APP-000374-NDM-000299` | The network device must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). | Time zone, with the clock synchronized by NTP (Chapter 11 also maps PTP clock synchronization) | `config system global; set timezone <TIMEZONE_NUMBER>; end` | Not in the feature matrix (8.0.0 CLI Reference) |
| NDM | `SRG-APP-000457-NDM-000352` | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). | Centralized firmware management; CPLD software upgrade support for OS; Firmware image rotation (dual-firmware image support) | `config system global; set image-rotation enable; end` | 7.0.0 or earlier (Firmware image rotation (dual-firmware image support)) |
| NDM | `SRG-APP-000515-NDM-000325` | The network device must off-load audit records onto a different system or media than the system being audited. | Syslog collection; Reliable syslog | `config log syslogd setting; set status enable; set server <SYSLOG_IP>; set mode reliable; set enc-algorithm high; end` | 7.0.0 or earlier (Reliable syslog) |
| NDM | `SRG-APP-000920-NDM-000320` | The network device must be configured to synchronize system clocks within and between systems or system components. | PTP version-2 transparent clock; PTP layer-2 boundary clock; Layer-3 PTP; Use PTP to synchronize system clock; and 2 more | `config system ntp; set ntpsync enable; set authentication enable; config ntpserver; edit 1; set server <NTP_IP>; set authentication enable; set key-id <ID>; set key <KEY>; end; end` | 7.6.2 and later (NTP server (IPv4/IPv6)) |
| NDM | `SRG-APP-000925-NDM-000330` | The network device must be configured to compare the internal system clocks on an organization-defined frequency with organization-defined authoritative time source. | NTP synchronization interval (Chapter 11 maps automatic clock source selection) | `config system ntp; set ntpsync enable; set syncinterval <MINUTES>; end` | Not in the feature matrix (8.0.0 CLI Reference) |
| NDM | `SRG-APP-001035-NDM-000340` | The network device hardware and software must be a version supported by the vendor. | A FortiSwitchOS release Fortinet supports; check the running version (Chapter 11 maps centralized firmware management) | `get system status` | Not in the feature matrix (8.0.0 CLI Reference) |
| L2S | `SRG-NET-000057-L2S-000005` | The layer 2 switch must dynamically associate security attributes with organization-defined subjects in accordance with organization-defined security policies as information is created and combined. | Host quarantine; Integrated FortiGate network access control (NAC) function; NAC LAN segments; Matching FortiClient EMS tags in NAC policies; and 12 more | FortiGate: `config switch-controller quarantine; set quarantine enable; config targets; edit <MAC>; end` | 7.0.0 or earlier (Host quarantine) |
| L2S | `SRG-NET-000131-L2S-000014` | The layer 2 switch must be configured to disable non-essential capabilities. | Disable unused ports and features (Chapter 11 marks every operational feature that falls under this requirement when unused) | `config switch physical-port; edit <PORT>; set status down; end` | Not in the feature matrix (8.0.0 CLI Reference) |
| L2S | `SRG-NET-000235-L2S-000031` | The layer 2 switch must be configured to fail securely in the event of an operational failure. | Firmware image rotation (dual-firmware image support); Tagged VLAN support for authserver-timeout | `config system global; set image-rotation enable; end` | 7.0.0 or earlier (Firmware image rotation (dual-firmware image support)) |
| L2S | `SRG-NET-000325-L2S-000041` | The layer 2 switch must uniquely identify and authenticate source by organization, system, application, and/or individual for information transfer. | FortiLink Secure Fabric authentication; MACsec: PSK mode; MACsec: Dynamic-CAK mode | `config switch macsec profile; edit <PROFILE>; set macsec-mode static-cak; set cipher_suite GCM-AES-256; config mka-psk; edit <KEY>; set mka-cak <CAK>; set mka-ckn <CKN>; end; end` `config switch physical-port; edit <PORT>; set security-mode macsec; set macsec-profile <PROFILE>; end` | 7.0.0 or earlier (MACsec: PSK mode) |
| L2S | `SRG-NET-000343-L2S-000016` | The layer 2 switch must authenticate all network-connected endpoint devices before establishing any connection. | Integrated FortiGate network access control (NAC) function; NAC and 802.1X on same port; 802.1X port mode; 802.1X MAC-based mode; and 4 more | `config switch interface; edit <PORT>; config port-security; set port-security-mode 802.1X; end; set security-groups <GROUP>; end` | 7.0.0 or earlier (802.1X port mode) |
| L2S | `SRG-NET-000512-L2S-000100` | The layer 2 switch must be configured in accordance with the security configuration settings based on DoD security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. | Automated detection and recommendations; Automation stitches (zero-touch provisioning automation); IP conflict detection and notification; ACL (IPv4 ingress); and 3 more | `config switch acl ingress; edit <ID>; set ingress-interface <PORT>; config classifier; set src-ip-prefix <IP> <MASK>; end; config action; set drop enable; end; end` | 7.0.0 or earlier (ACL (IPv4 ingress)) |
| L2S | `SRG-NET-000520-L2S-000105` | The layer 2 switch must dynamically associate security attributes with organization-defined objects in accordance with organization-defined security policies as information is created and combined. | Matching FortiClient EMS tags in NAC policies; Matching IoT/OT vulnerabilities in NAC policies; Matching FortiVoice tags in NAC policies; Dynamic port policies (DPP) | FortiGate: `config user nac-policy; edit <POLICY>; set category ems-tag; set ems-tag <TAG>; end` | 7.0.0 or earlier (Matching FortiClient EMS tags in NAC policies) |
| L2S | `SRG-NET-000715-L2S-000120` | The layer 2 switch must implement physically or logically separate subnetworks to isolate organization-defined critical system components and functions. | Block intra-VLAN traffic; Host quarantine; NAC LAN segments; FortiSwitch VLANs over VXLAN; and 7 more | FortiGate: `config system interface; edit <VLAN_INTERFACE>; set switch-controller-access-vlan enable; end` | 7.0.0 or earlier (Block intra-VLAN traffic) |
| L2S | `SRG-NET-000760-L2S-000160` | The layer 2 switch must establish organization-defined alternate communications paths for system operations organizational command and control. | Link aggregation group size; LAG min-max bundle; Multi-stage load balancing; VXLAN: ECMP; and 12 more | `config switch trunk; edit <TRUNK>; set mode lacp-active; set members <PORTS>; end` | 7.0.0 or earlier (Link aggregation group size) |
| RTR | `SRG-NET-000230-RTR-000001` | The router must be configured to implement message authentication for all control plane protocols. | VRRP (Chapter 11 maps it here); FortiSwitchOS has no VRRP authentication option, so record the gap and keep VRRP on trusted segments | — | — |
| AAA | `SRG-APP-000023-AAA-000030` | AAA Services must be configured to provide automated account management functions. | RADIUS accounting server support | `config user radius; edit <RADIUS>; config acct-server; edit 1; set status enable; set server <IP>; set secret <SECRET>; end; end` | 7.0.0 or earlier (RADIUS accounting server support) |
| AAA | `SRG-APP-000142-AAA-000020` | AAA Services must be configured to use protocols that encrypt credentials when authenticating clients, as defined in the PPSM CAL and vulnerability assessments. | 802.1X: RadSec (IPv4) | `config user radius; edit <RADIUS>; set transport-type TLS; set radsec-tls-min-ver TLSv1-2; set radsec-cert-validate enable; end` | 7.6.4 and later (802.1X: RadSec (IPv4)) |
| AAA | `SRG-APP-000158-AAA-000420` | AAA Services used for 802.1x must be configured to uniquely identify network endpoints (supplicants) before the authenticator establishes any connection. | 802.1X MAC-based mode | `config switch interface; edit <PORT>; config port-security; set port-security-mode 802.1X-mac-based; end; set security-groups <GROUP>; end` | 7.0.0 or earlier (802.1X MAC-based mode) |
| AAA | `SRG-APP-000172-AAA-000520` | AAA Services must be configured to encrypt transmitted credentials using a FIPS-validated cryptographic module. | RADIUS for administrative authentication; 802.1X: RadSec (IPv4) | `config user radius; edit <RADIUS>; set transport-type TLS; set radsec-tls-min-ver TLSv1-2; set radsec-cert-validate enable; end` | 7.6.4 and later (802.1X: RadSec (IPv4)) |
| AAA | `SRG-APP-000394-AAA-000430` | AAA Services used for 802.1x must be configured to authenticate network endpoint devices (supplicants) before the authenticator establishes any connection. | 802.1X port mode | `config switch interface; edit <PORT>; config port-security; set port-security-mode 802.1X; end; set security-groups <GROUP>; end` | 7.0.0 or earlier (802.1X port mode) |
| AAA | `SRG-APP-000516-AAA-000440` | AAA Services used for 802.1x must be configured to use secure Extensible Authentication Protocol (EAP), such as EAP-TLS, EAP-TTLS, and PEAP. | EAP pass-through | `config switch interface; edit <PORT>; config port-security; set eap-passthru enable; end; end` | 7.0.0 or earlier (EAP pass-through) |
| AAA | `SRG-APP-000516-AAA-000640` | AAA Services must be configured to use a unique shared secret for communication (i.e. RADIUS, TACACS+) with clients requesting authentication services. | RADIUS for administrative authentication; TACACS+ for administrative authentication; RADIUS CoA and disconnect messages | `config user radius; edit <RADIUS>; set server <IP>; set secret <SECRET>; end` `config system admin; edit <ADMIN>; set remote-auth enable; set remote-group <GROUP>; end` | 7.2.0 and later (RADIUS for administrative authentication) |

### Alignment summary

| STIG | Same requirement | Equivalent setting | Partial | Not supported | Not applicable | By procedure | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| C-NDM (V3R6) | 11 | 25 | 5 | 0 | 0 | 1 | 42 |
| C-L2S (V3R2) | 15 | 4 | 1 | 1 | 1 | 0 | 22 |
| C-RTR (V3R4) | 5 | 26 | 10 | 27 | 19 | 1 | 88 |
| **Total** | **31** | **55** | **16** | **28** | **20** | **2** | **152** |

FortiSwitch meets 86 of the 152 Cisco rules' requirements
with a setting (31 through the feature Chapter 11 maps and 55
through another setting), and 2 more by procedure. 16 are met
only in part, 28 describe capabilities FortiSwitch does not have, and
20 do not apply. Most of the gaps are in the C-RTR STIG; the C-NDM
and C-L2S rules, which apply to every switch, are almost all met. The main
differences:

- **Management defaults.** The Cisco rules make you configure what
  FortiSwitchOS partly does by default. The FortiSwitchOS administrator
  idle timeout defaults to **5 minutes**, which already meets
  `CISC-ND-000720`; on IOS XE, `exec-timeout 5 0` must be set on every line
  and the HTTP idle timeout set to 300 seconds. The FortiSwitchOS lockout
  threshold defaults to **3 attempts**, but its lockout duration defaults to
  **60 seconds**, so `admin-lockout-duration 900` must be set for
  `CISC-ND-000150`. FortiSwitchOS has no limit on the number of management
  sessions (`CISC-ND-000010` is Partial).
- **Two-server rules.** The Cisco rules require two authentication servers
  (`CISC-ND-001370`), two log servers (`CISC-ND-001450`), and two time
  sources (`CISC-ND-001030`). FortiSwitchOS meets all three, but differently:
  a RADIUS or TACACS+ entry holds one server, so define two entries and make
  both members of the administrators' user group; syslog has three separate
  destinations (`syslogd`, `syslogd2`, `syslogd3`); NTP takes a list of
  servers.
- **Where FortiSwitch can be stricter.** FortiSwitchOS syslog can use
  reliable (TCP) transport with encryption (`set mode reliable` and
  `set enc-algorithm high`), where the Chapter 32 command sends plain
  syslog. SNMPv3 users can authenticate with SHA-256 to SHA-512, where the
  Chapter 32 command uses SHA. Administrator passwords can be stored with
  PBKDF2 (`admin-password-hash pbkdf2-high`).
- **Where FortiSwitch is weaker.** The password policy can require only four
  changed characters, not eight (`CISC-ND-000610`). NTP authentication uses
  SHA-1 (NTPv4) or MD5 (NTPv3), where the Cisco command uses HMAC-SHA-256.
  FortiSwitchOS has no per-algorithm SSH cipher or MAC list; FIPS-CC mode
  and `strong-crypto` stand in for the Cisco algorithm lists. ACLs count
  matches but cannot log packets, so the rules that rely on Cisco
  `log-input` are Partial.
- **Routing protocol authentication.** As Chapter 11 documents, FortiSwitchOS
  OSPF, RIP, and IS-IS authenticate neighbors with MD5 or plain text only,
  and BGP with a TCP MD5 password; there is no FIPS 198-1 option and no VRRP
  authentication. `CISC-RT-000050` is therefore Partial: configure MD5 and
  key lifetimes, record the open finding, and limit routing protocols to
  dedicated, filtered interfaces or use static routing.
- **Perimeter filtering.** FortiSwitchOS ACLs can match addresses, services,
  VLANs, and DSCP, which meets most perimeter ACL rules. They cannot match IP
  options or IPv6 extension headers (`CISC-RT-000350` and
  `CISC-RT-000392` to `CISC-RT-000398` are Not supported), and they have no
  implicit deny (`CISC-RT-000240` is Partial). FortiSwitchOS has no setting
  for ICMP unreachables, ICMP mask replies, or gratuitous ARP.
- **MPLS and multicast roles.** FortiSwitchOS has no MPLS, LDP, RSVP-TE,
  L3VPN, VPWS, or VPLS, so the MPLS and PE rules are Not supported, and the
  PE and P rules about generic features are Not applicable because the role
  cannot exist. VRF-lite exists (`CISC-RT-000630` is Partial). FortiSwitchOS
  multicast routing is PIM-SSM only, so the rendezvous point, SPT threshold,
  and MSDP rules are Not applicable, while the designated router's IGMP join
  filter and limit rules are Not supported.
- **Layer 2 differences.** FortiSwitchOS has no UDLD (`CISC-L2-000190`) and
  does not run VTP (`CISC-L2-000030`). Unknown unicast flood blocking is done
  with storm control at a rate of 0, which shares the port's single storm
  control rate with broadcast control (`CISC-L2-000120` is Partial). In
  FortiSwitchOS a "trunk" is a link aggregation group; tagged VLANs on a
  port are set with `native-vlan` and `allowed-vlans`, and there is no
  trunk negotiation to disable.

**FortiLink-managed mode.** When a FortiGate manages the switch, the
FortiGate owns the switch configuration and overwrites changes made on the
switch. Make the FortiSwitch side of each row under the FortiGate's
`config switch-controller` tree. For example, the port guards
(`CISC-L2-000090`, `CISC-L2-000100`, `CISC-L2-000140`):

FortiGate: `config switch-controller managed-switch; edit <SWITCH_SN>; config ports; edit <PORT>; set stp-bpdu-guard enabled; set stp-root-guard enabled; set ip-source-guard enable; end; end`

The switch's syslog destination (`CISC-ND-001450`) and SNMPv3 user
(`CISC-ND-001130` and `CISC-ND-001140`):

FortiGate: `config switch-controller remote-log; edit <NAME>; set status enable; set server <SYSLOG_IP>; end`

FortiGate: `config switch-controller snmp-user; edit <USER>; set security-level auth-priv; set auth-proto sha256; set priv-proto aes256; end`

Management protocols on the switch's management and internal interfaces
(`CISC-ND-000470`):

FortiGate: `config switch-controller security-policy local-access; edit <POLICY>; set mgmt-allowaccess https ssh; end`

Settings with no `switch-controller` equivalent, such as the lockout
duration or the password policy, can be pushed as a custom command that the
FortiGate applies to the switch:

FortiGate: `config switch-controller custom-command; edit <CMD_NAME>; set command <SWITCH_CLI_TEXT>; end`

FortiGate: `config switch-controller managed-switch; edit <SWITCH_SN>; config custom-command; edit 1; set command-name <CMD_NAME>; end; end`

### Collecting evidence

In a mixed estate, keep one checklist row per Cisco rule for each switch,
with the SRG ID and alignment category from the table, and attach each
platform's evidence:

- **Cisco switches:** the Chapter 32 evidence (`show version`, `show
  running-config`, and the section, logging, AAA, and protocol outputs).
- **Standalone FortiSwitches:** `get system status` for the release, and
  `show full-configuration` for the settings in the FortiSwitchOS column.
  Add `get system password-policy`, `get system ntp`, `get switch
  security-feature`, `get switch stp settings`, `get switch interface`, and
  `get switch acl counters all` for the rows they cover, and for routed
  switches `get router info bfd neighbor` and the routing protocol outputs
  your design uses.
- **FortiLink-managed FortiSwitches:** the FortiGate's `switch-controller`
  configuration (the managed switch entry, its ports, and any custom
  commands) as well as `get system status` from the switch.
- **For every Partial and Not supported row:** the open finding, its
  mitigation, and its approval, recorded against the SRG ID.

Keep the AAA Services and other Chapter 11-only requirements (the second
table) on the FortiSwitch checklist as well, with their evidence (Chapter 03
describes SRG-based checklists).

## Validation and Troubleshooting

- **A Cisco rule seems to have no FortiSwitch row.** Every one of the
  152 rules has a row; the build script fails if one is missing.
  Search the table for the rule ID, not the rule title: the Requirement
  column paraphrases the title.
- **A FortiSwitchOS command is rejected.** Check the release and model. The
  commands were checked against the 8.0.0 CLI Reference; some options exist
  only on some models (the `switch security-feature` checks, for example)
  or only with the Advanced Features license. Use `?` on the CLI.
- **A change made on the switch disappears.** The switch is
  FortiLink-managed; the FortiGate overwrote it. Make the change under
  `config switch-controller` on the FortiGate, or as a custom command.
- **An assessor asks for the FortiSwitch STIG rule.** There is none. Show
  the SRG-based checklist, the SRG ID in the table, and the Cisco rule only
  as the reference that implements the same requirement.
- **Hosts lose connectivity after unknown unicast flood blocking.** A storm
  control rate of 0 drops every enabled traffic type on the port. Make sure
  only `unknown-unicast` is enabled on that port, or use a non-zero rate.
- **Routing adjacencies fail between a Cisco and a FortiSwitch router.** The
  Cisco side uses HMAC-SHA-256 key chains (Chapter 32); FortiSwitchOS OSPF
  supports MD5 only. Both ends must use the same method, so a mixed
  adjacency must fall back to MD5 and both platforms then carry the Partial
  finding for that link.

## Security and Best Practices

- Treat the Cisco IOS XE Switch STIG rules as the minimum checklist for
  every switch, and add the Chapter 11-only requirements for FortiSwitch.
- On FortiSwitch, set the lockout duration to 900 seconds, keep the
  5-minute idle timeout, set the DoD pre-login banner, use a 15-character
  password policy, and allow only HTTPS and SSH from trusted hosts.
- Use two authentication servers, two reliable encrypted syslog servers,
  and two authenticated NTP servers, and SNMPv3 with SHA-256 or stronger and
  AES-256.
- Enable FIPS-CC mode where DoD policy requires FIPS-validated cryptography,
  and test management access afterward (FIPS-CC mode disables TLS 1.3).
- On host ports, use 802.1X with MAB, BPDU guard, IP source guard, storm
  control, and a non-default native VLAN with tagged frames discarded; use
  DHCP snooping and dynamic ARP inspection on user VLANs.
- Keep FortiSwitches out of perimeter, MPLS, and multicast rendezvous point
  roles, where the table shows gaps; use a FortiGate or a platform with the
  needed capability.
- Record every Partial and Not supported row as an open finding with its
  mitigation, and review the crosswalk whenever DISA updates the Cisco IOS
  XE Switch STIGs or an SRG, or Fortinet releases a new FortiSwitchOS
  version.

## References and Knowledge Checks

**References:**

- DISA Cisco IOS XE Switch NDM STIG V3R6, L2S STIG V3R2, and RTR STIG V3R4
  (`U_Cisco_IOS-XE_Switch_Y26M04_STIG.zip`), and the Layer 2 Switch SRG
  V3R4, Network Device Management SRG V5R5, Router SRG V5R2, and AAA
  Services SRG V2R3, from the October 2026 STIG Library Compilation.
- Fortinet, *FortiSwitchOS 8.0.0 CLI Reference*, and *FortiOS 8.0.1 CLI
  Reference* (FortiLink managed-mode commands).
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (how STIGs are built from SRGs, and SRG-based assessment),
  [Chapter 07](07-network-device-stigs-management-routing-and-filtering.md)
  (network device STIGs by plane),
  [Chapter 11](11-fortiswitch-feature-version-and-srg-map.md) (the
  FortiSwitch feature and SRG map),
  [Chapter 31](31-cisco-products-stigs-and-srg-mapping.md) (the Cisco STIG
  packages and router roles), and
  [Chapter 32](32-cisco-catalyst-switch-feature-version-and-stig-map.md)
  (the Cisco Catalyst switch feature and STIG map, source of the Cisco
  commands).

**Knowledge checks:**

1. Why is it wrong to say a FortiSwitch is compliant with a Cisco STIG
   rule, and what is the finding recorded against instead?
2. What links a Cisco rule to a FortiSwitch setting in this crosswalk, and
   why were CCIs not used?
3. Which FortiSwitchOS default already meets a Cisco rule, and which
   default must be changed to meet `CISC-ND-000150`?
4. How does FortiSwitchOS meet the two-authentication-server rule when a
   RADIUS entry holds only one server?
5. Why are the MPLS rules Not supported but the rendezvous point rules Not
   applicable?
6. Name two SRG requirements a Cisco rule checklist would miss on a
   FortiSwitch.
7. Where do you configure the port guards on a FortiLink-managed switch,
   and why not on the switch itself?

## Summary and Completion Checklist

There is no FortiSwitch STIG, so a FortiSwitch is assessed against the
SRGs, and the Cisco IOS XE Switch STIGs implement those same SRGs. This
chapter aligns all 152 Cisco rules (42 C-NDM, 22
C-L2S, and 88 C-RTR) with the FortiSwitch setting and FortiSwitchOS
command that meet the same SRG requirement: 31 through the feature
Chapter 11 maps, 55 through another setting, 2 by procedure,
16 only in part, 28 not supported, and 20 not applicable.
It also lists the 26 FortiSwitch requirements that no Cisco rule
covers. Every FortiSwitchOS and FortiOS command was checked by script
against the vendor's CLI reference, and every Cisco command comes from
Chapter 32.

- [ ] Can explain why FortiSwitch is assessed against SRGs and the Cisco
  rules are only a reference.
- [ ] Can find a Cisco rule in the crosswalk and configure the FortiSwitch
  setting that meets the same requirement.
- [ ] Can assign and record the alignment category for each rule.
- [ ] Can add the Chapter 11-only requirements to a FortiSwitch checklist.
- [ ] Can make the FortiSwitch changes on the FortiGate for a
  FortiLink-managed switch, and collect evidence from both platforms.
